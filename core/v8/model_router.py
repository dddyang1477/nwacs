#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多模型协同路由系统 (Model Router)

对标 FeelFish 的多模型适配能力。
支持 DeepSeek / OpenAI / Anthropic / Qwen 等多厂商模型，
根据任务类型自动路由到最优模型，支持故障转移和成本优化。

核心能力:
- 任务感知路由: 创作→Claude, 逻辑→DeepSeek, 翻译→Qwen
- 故障转移链: 主模型失败自动切换备用模型
- 成本优化: 简单任务用便宜模型
- 负载均衡: 多API Key轮转
- 模型性能评分: 基于历史成功率动态调整权重
"""

import os
import time
import json
import hashlib
from typing import Dict, List, Optional, Tuple, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict


class TaskType(Enum):
    CREATIVE_WRITING = "creative_writing"      # 创意写作
    LOGIC_REASONING = "logic_reasoning"         # 逻辑推理
    POLISH_REWRITE = "polish_rewrite"           # 润色改写
    TRANSLATION = "translation"                 # 翻译
    SUMMARIZATION = "summarization"             # 摘要
    CODE_GENERATION = "code_generation"         # 代码生成
    DIALOGUE = "dialogue"                       # 对话生成
    WORLD_BUILDING = "world_building"           # 世界观构建
    PLOT_OUTLINE = "plot_outline"               # 情节大纲
    CHARACTER_DESIGN = "character_design"       # 角色设计
    DEAI_REWRITE = "deai_rewrite"              # 去AI痕迹改写
    GENERAL = "general"                         # 通用


class ModelProvider(Enum):
    DEEPSEEK = "deepseek"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    QWEN = "qwen"
    ZHIPU = "zhipu"
    MOONSHOT = "moonshot"
    BYTEDANCE = "bytedance"


@dataclass
class ModelConfig:
    provider: ModelProvider
    model_name: str
    api_key: str = ""
    api_base: str = ""
    max_tokens: int = 8192
    temperature: float = 0.7
    cost_per_1k_input: float = 0.0
    cost_per_1k_output: float = 0.0
    priority: int = 5
    enabled: bool = True
    rate_limit_per_minute: int = 60


@dataclass
class ModelStats:
    total_calls: int = 0
    success_calls: int = 0
    fail_calls: int = 0
    total_latency_ms: float = 0.0
    total_cost: float = 0.0
    last_error: str = ""
    last_success_time: float = 0.0

    @property
    def success_rate(self) -> float:
        if self.total_calls == 0:
            return 1.0
        return self.success_calls / self.total_calls

    @property
    def avg_latency_ms(self) -> float:
        if self.total_calls == 0:
            return 0.0
        return self.total_latency_ms / self.total_calls


@dataclass
class RouterConfig:
    enable_cost_optimization: bool = True
    enable_fallback: bool = True
    max_retries: int = 3
    retry_delay_ms: int = 1000
    stats_window_size: int = 100
    min_success_rate: float = 0.5


TASK_MODEL_MAPPING: Dict[TaskType, List[Tuple[ModelProvider, str, int]]] = {
    TaskType.CREATIVE_WRITING: [
        (ModelProvider.ANTHROPIC, "claude-sonnet-4-20250514", 10),
        (ModelProvider.DEEPSEEK, "deepseek-chat", 8),
        (ModelProvider.OPENAI, "gpt-4o", 7),
        (ModelProvider.QWEN, "qwen-plus", 6),
    ],
    TaskType.LOGIC_REASONING: [
        (ModelProvider.DEEPSEEK, "deepseek-reasoner", 10),
        (ModelProvider.OPENAI, "o4-mini", 8),
        (ModelProvider.ANTHROPIC, "claude-sonnet-4-20250514", 7),
    ],
    TaskType.POLISH_REWRITE: [
        (ModelProvider.ANTHROPIC, "claude-sonnet-4-20250514", 10),
        (ModelProvider.DEEPSEEK, "deepseek-chat", 8),
        (ModelProvider.OPENAI, "gpt-4o", 7),
    ],
    TaskType.TRANSLATION: [
        (ModelProvider.QWEN, "qwen-plus", 10),
        (ModelProvider.DEEPSEEK, "deepseek-chat", 8),
        (ModelProvider.OPENAI, "gpt-4o", 7),
    ],
    TaskType.SUMMARIZATION: [
        (ModelProvider.DEEPSEEK, "deepseek-chat", 10),
        (ModelProvider.OPENAI, "gpt-4o-mini", 8),
        (ModelProvider.QWEN, "qwen-plus", 7),
    ],
    TaskType.CODE_GENERATION: [
        (ModelProvider.DEEPSEEK, "deepseek-chat", 10),
        (ModelProvider.ANTHROPIC, "claude-sonnet-4-20250514", 8),
        (ModelProvider.OPENAI, "gpt-4o", 7),
    ],
    TaskType.DIALOGUE: [
        (ModelProvider.ANTHROPIC, "claude-sonnet-4-20250514", 10),
        (ModelProvider.DEEPSEEK, "deepseek-chat", 8),
        (ModelProvider.QWEN, "qwen-plus", 7),
    ],
    TaskType.WORLD_BUILDING: [
        (ModelProvider.DEEPSEEK, "deepseek-chat", 10),
        (ModelProvider.ANTHROPIC, "claude-sonnet-4-20250514", 8),
        (ModelProvider.OPENAI, "gpt-4o", 7),
    ],
    TaskType.PLOT_OUTLINE: [
        (ModelProvider.DEEPSEEK, "deepseek-chat", 10),
        (ModelProvider.ANTHROPIC, "claude-sonnet-4-20250514", 8),
        (ModelProvider.OPENAI, "gpt-4o", 7),
    ],
    TaskType.CHARACTER_DESIGN: [
        (ModelProvider.ANTHROPIC, "claude-sonnet-4-20250514", 10),
        (ModelProvider.DEEPSEEK, "deepseek-chat", 8),
        (ModelProvider.OPENAI, "gpt-4o", 7),
    ],
    TaskType.DEAI_REWRITE: [
        (ModelProvider.ANTHROPIC, "claude-sonnet-4-20250514", 10),
        (ModelProvider.DEEPSEEK, "deepseek-chat", 8),
        (ModelProvider.OPENAI, "gpt-4o", 7),
    ],
    TaskType.GENERAL: [
        (ModelProvider.DEEPSEEK, "deepseek-chat", 10),
        (ModelProvider.OPENAI, "gpt-4o", 8),
        (ModelProvider.ANTHROPIC, "claude-sonnet-4-20250514", 7),
    ],
}

COST_EFFICIENT_ALTERNATIVES: Dict[str, str] = {
    "deepseek-chat": "deepseek-chat",
    "deepseek-reasoner": "deepseek-chat",
    "gpt-4o": "gpt-4o-mini",
    "claude-sonnet-4-20250514": "claude-haiku-4-20250514",
    "qwen-plus": "qwen-turbo",
}


class ModelRouter:
    """多模型协同路由系统"""

    def __init__(self, config: RouterConfig = None):
        self.config = config or RouterConfig()
        self.models: Dict[str, ModelConfig] = {}
        self.stats: Dict[str, ModelStats] = defaultdict(ModelStats)
        self._call_history: List[Dict] = []
        self._rate_limit_tracker: Dict[str, List[float]] = defaultdict(list)
        self._load_from_env()

    def _load_from_env(self):
        """从环境变量加载模型配置"""
        env_mappings = {
            "DEEPSEEK_API_KEY": (ModelProvider.DEEPSEEK, "deepseek-chat",
                                 "https://api.deepseek.com/v1"),
            "OPENAI_API_KEY": (ModelProvider.OPENAI, "gpt-4o",
                               "https://api.openai.com/v1"),
            "ANTHROPIC_API_KEY": (ModelProvider.ANTHROPIC, "claude-sonnet-4-20250514",
                                  "https://api.anthropic.com/v1"),
            "QWEN_API_KEY": (ModelProvider.QWEN, "qwen-plus",
                             "https://dashscope.aliyuncs.com/compatible-mode/v1"),
            "ZHIPU_API_KEY": (ModelProvider.ZHIPU, "glm-4-plus",
                              "https://open.bigmodel.cn/api/paas/v4"),
            "MOONSHOT_API_KEY": (ModelProvider.MOONSHOT, "moonshot-v1-8k",
                                 "https://api.moonshot.cn/v1"),
        }

        for env_key, (provider, model, base) in env_mappings.items():
            api_key = os.environ.get(env_key, "")
            if api_key:
                self.register_model(ModelConfig(
                    provider=provider,
                    model_name=model,
                    api_key=api_key,
                    api_base=os.environ.get(f"{env_key}_BASE", base),
                ))

    def register_model(self, config: ModelConfig):
        """注册模型"""
        key = f"{config.provider.value}:{config.model_name}"
        self.models[key] = config
        if key not in self.stats:
            self.stats[key] = ModelStats()

    def unregister_model(self, provider: ModelProvider, model_name: str):
        """注销模型"""
        key = f"{provider.value}:{model_name}"
        self.models.pop(key, None)

    def get_available_models(self) -> List[ModelConfig]:
        """获取所有可用模型"""
        return [m for m in self.models.values() if m.enabled]

    def route(self, task_type: TaskType,
              content: str = "",
              system_prompt: str = "",
              temperature: float = None,
              max_tokens: int = None,
              force_model: str = None,
              cost_sensitive: bool = False) -> Tuple[str, Dict[str, Any]]:
        """
        智能路由 — 根据任务类型选择最优模型

        Returns:
            (response_text, metadata)
        """
        t0 = time.time()

        if force_model:
            candidates = [self.models[force_model]] if force_model in self.models else []
        else:
            candidates = self._select_candidates(task_type, cost_sensitive)

        if not candidates:
            raise RuntimeError(f"没有可用模型处理任务: {task_type.value}")

        last_error = None
        for attempt in range(self.config.max_retries):
            for model_cfg in candidates:
                model_key = f"{model_cfg.provider.value}:{model_cfg.model_name}"

                if not self._check_rate_limit(model_key, model_cfg):
                    continue

                if self.stats[model_key].success_rate < self.config.min_success_rate:
                    if attempt == 0:
                        continue

                try:
                    response = self._call_model(
                        model_cfg, content, system_prompt,
                        temperature or model_cfg.temperature,
                        max_tokens or model_cfg.max_tokens,
                    )

                    latency = (time.time() - t0) * 1000
                    self._record_success(model_key, latency, model_cfg, content)

                    return response, {
                        "model": model_key,
                        "provider": model_cfg.provider.value,
                        "latency_ms": latency,
                        "attempt": attempt + 1,
                        "task_type": task_type.value,
                    }

                except Exception as e:
                    last_error = e
                    self._record_failure(model_key, str(e))
                    continue

            if attempt < self.config.max_retries - 1:
                time.sleep(self.config.retry_delay_ms / 1000 * (attempt + 1))

        raise RuntimeError(
            f"所有模型调用失败 (任务: {task_type.value}, 尝试: {self.config.max_retries})"
            f"\n最后错误: {last_error}"
        )

    def _select_candidates(self, task_type: TaskType,
                           cost_sensitive: bool) -> List[ModelConfig]:
        """选择候选模型 — 按优先级排序"""
        mapping = TASK_MODEL_MAPPING.get(task_type, TASK_MODEL_MAPPING[TaskType.GENERAL])

        candidates = []
        for provider, model_name, base_priority in mapping:
            key = f"{provider.value}:{model_name}"
            if key not in self.models or not self.models[key].enabled:
                if cost_sensitive:
                    alt = COST_EFFICIENT_ALTERNATIVES.get(model_name, model_name)
                    alt_key = f"{provider.value}:{alt}"
                    if alt_key in self.models and self.models[alt_key].enabled:
                        key = alt_key
                    else:
                        continue
                else:
                    continue

            model_cfg = self.models[key]
            stats = self.stats[key]

            adjusted_priority = base_priority
            adjusted_priority += stats.success_rate * 3
            adjusted_priority -= (stats.avg_latency_ms / 1000) * 0.5

            candidates.append((adjusted_priority, model_cfg))

        candidates.sort(key=lambda x: x[0], reverse=True)
        return [c[1] for c in candidates]

    def _call_model(self, model_cfg: ModelConfig, content: str,
                    system_prompt: str, temperature: float,
                    max_tokens: int) -> str:
        """调用具体模型API"""
        import requests

        headers = {
            "Authorization": f"Bearer {model_cfg.api_key}",
            "Content-Type": "application/json",
        }

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": content})

        payload = {
            "model": model_cfg.model_name,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        if model_cfg.provider == ModelProvider.ANTHROPIC:
            headers["anthropic-version"] = "2023-06-01"
            payload.pop("model")
            payload["model"] = model_cfg.model_name
            if "max_tokens" in payload:
                payload["max_tokens"] = min(payload["max_tokens"], 4096)

        resp = requests.post(
            f"{model_cfg.api_base}/chat/completions",
            headers=headers,
            json=payload,
            timeout=120,
        )
        resp.raise_for_status()
        data = resp.json()

        if "choices" in data and len(data["choices"]) > 0:
            return data["choices"][0]["message"]["content"]
        elif "content" in data:
            return data["content"][0]["text"]

        raise RuntimeError(f"无法解析模型响应: {str(data)[:200]}")

    def _check_rate_limit(self, model_key: str, model_cfg: ModelConfig) -> bool:
        """检查速率限制"""
        now = time.time()
        window_start = now - 60

        self._rate_limit_tracker[model_key] = [
            t for t in self._rate_limit_tracker[model_key] if t > window_start
        ]

        return len(self._rate_limit_tracker[model_key]) < model_cfg.rate_limit_per_minute

    def _record_success(self, model_key: str, latency_ms: float,
                        model_cfg: ModelConfig, content: str):
        """记录成功调用"""
        stats = self.stats[model_key]
        stats.total_calls += 1
        stats.success_calls += 1
        stats.total_latency_ms += latency_ms
        stats.last_success_time = time.time()

        input_tokens = len(content) // 2
        output_tokens = 500
        stats.total_cost += (
            model_cfg.cost_per_1k_input * input_tokens / 1000
            + model_cfg.cost_per_1k_output * output_tokens / 1000
        )

        self._rate_limit_tracker[model_key].append(time.time())

        self._call_history.append({
            "model": model_key,
            "success": True,
            "latency_ms": latency_ms,
            "time": time.time(),
        })

        if len(self._call_history) > self.config.stats_window_size:
            self._call_history = self._call_history[-self.config.stats_window_size:]

    def _record_failure(self, model_key: str, error: str):
        """记录失败调用"""
        stats = self.stats[model_key]
        stats.total_calls += 1
        stats.fail_calls += 1
        stats.last_error = error

        self._call_history.append({
            "model": model_key,
            "success": False,
            "error": error,
            "time": time.time(),
        })

    def get_stats(self) -> Dict[str, Dict]:
        """获取所有模型统计"""
        result = {}
        for key, stats in self.stats.items():
            result[key] = {
                "total_calls": stats.total_calls,
                "success_rate": round(stats.success_rate * 100, 1),
                "avg_latency_ms": round(stats.avg_latency_ms, 0),
                "total_cost": round(stats.total_cost, 4),
                "last_error": stats.last_error[:100] if stats.last_error else "",
            }
        return result

    def get_recommendation(self, task_type: TaskType) -> Dict:
        """获取任务类型的最佳模型推荐"""
        candidates = self._select_candidates(task_type, cost_sensitive=False)
        if not candidates:
            return {"error": "无可用模型"}

        best = candidates[0]
        key = f"{best.provider.value}:{best.model_name}"
        stats = self.stats[key]

        return {
            "recommended_model": key,
            "provider": best.provider.value,
            "success_rate": round(stats.success_rate * 100, 1),
            "avg_latency_ms": round(stats.avg_latency_ms, 0),
            "alternatives": [
                f"{c.provider.value}:{c.model_name}" for c in candidates[1:4]
            ],
        }

    def health_check(self) -> Dict:
        """健康检查 — 检测所有模型状态"""
        results = {}
        for key, cfg in self.models.items():
            stats = self.stats[key]
            status = "healthy"
            if stats.success_rate < 0.5 and stats.total_calls > 5:
                status = "degraded"
            if stats.success_rate < 0.2 and stats.total_calls > 10:
                status = "unhealthy"
            if not cfg.enabled:
                status = "disabled"

            results[key] = {
                "status": status,
                "success_rate": round(stats.success_rate * 100, 1),
                "total_calls": stats.total_calls,
                "enabled": cfg.enabled,
            }

        return results
