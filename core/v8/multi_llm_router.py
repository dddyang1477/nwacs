#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS V8.5 多LLM智能路由系统
参考FeelFish多模型支持: DeepSeek/OpenAI/Claude/智谱GLM智能路由

核心能力:
- 多模型智能路由
- 自动Fallback机制
- 任务类型匹配
- 负载均衡
"""

import os
import json
import time
import logging
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TaskType(Enum):
    PLOT_GENERATION = "plot_generation"
    CHARACTER_DIALOGUE = "character_dialogue"
    BATTLE_SCENE = "battle_scene"
    ROMANCE_SCENE = "romance_scene"
    WORLD_BUILDING = "world_building"
    QUALITY_CHECK = "quality_check"
    SENSORY_ENHANCE = "sensory_enhance"
    PLOT_REVIEW = "plot_review"
    CREATIVE_BRAINSTORM = "creative_brainstorm"
    TEXT_OPTIMIZE = "text_optimize"


class LLMProvider(Enum):
    DEEPSEEK = "deepseek"
    OPENAI = "openai"
    CLAUDE = "claude"
    ZHIPU = "zhipu"
    LOCAL = "local"


@dataclass
class LLMConfig:
    """LLM提供商配置"""
    provider: LLMProvider
    name: str
    api_key_env: str
    base_url: str
    models: List[str]
    default_model: str
    strengths: List[str]
    priority: int
    is_available: bool = False
    current_load: float = 0.0


@dataclass
class LLMResponse:
    """LLM响应"""
    content: str
    provider: LLMProvider
    model: str
    success: bool
    error: Optional[str] = None
    tokens_used: Optional[int] = None
    latency_ms: Optional[float] = None
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class TaskRequest:
    """任务请求"""
    task_type: TaskType
    prompt: str
    system_prompt: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 2000
    preferred_provider: Optional[LLMProvider] = None
    fallback_enabled: bool = True


class MultiLLMRouter:
    """多LLM智能路由系统"""

    def __init__(self):
        self.providers: Dict[LLMProvider, LLMConfig] = {}
        self.request_history: List[Dict] = []
        self.fallback_chain: List[LLMProvider] = []

        self._init_providers()
        self._build_fallback_chain()

    def _init_providers(self):
        """初始化LLM提供商"""
        configs = {
            LLMProvider.DEEPSEEK: LLMConfig(
                provider=LLMProvider.DEEPSEEK,
                name="DeepSeek",
                api_key_env="DEEPSEEK_API_KEY",
                base_url="https://api.deepseek.com/v1",
                models=["deepseek-chat", "deepseek-coder"],
                default_model="deepseek-chat",
                strengths=["逻辑推理", "代码生成", "中文优化", "网文写作"],
                priority=1
            ),
            LLMProvider.OPENAI: LLMConfig(
                provider=LLMProvider.OPENAI,
                name="OpenAI GPT",
                api_key_env="OPENAI_API_KEY",
                base_url="https://api.openai.com/v1",
                models=["gpt-4", "gpt-3.5-turbo"],
                default_model="gpt-3.5-turbo",
                strengths=["通用生成", "创意写作", "上下文理解"],
                priority=2
            ),
            LLMProvider.CLAUDE: LLMConfig(
                provider=LLMProvider.CLAUDE,
                name="Claude",
                api_key_env="ANTHROPIC_API_KEY",
                base_url="https://api.anthropic.com/v1",
                models=["claude-3-opus", "claude-3-sonnet"],
                default_model="claude-3-sonnet",
                strengths=["长文本生成", "风格控制", "安全性高", "创意写作"],
                priority=3
            ),
            LLMProvider.ZHIPU: LLMConfig(
                provider=LLMProvider.ZHIPU,
                name="智谱GLM",
                api_key_env="ZHIPU_API_KEY",
                base_url="https://open.bigmodel.cn/api/paas/v4",
                models=["glm-4", "glm-3-turbo"],
                default_model="glm-4",
                strengths=["中文创作", "知识问答", "快速响应"],
                priority=4
            ),
            LLMProvider.LOCAL: LLMConfig(
                provider=LLMProvider.LOCAL,
                name="Local Model",
                api_key_env="",
                base_url="http://localhost:8000/v1",
                models=["local-model"],
                default_model="local-model",
                strengths=["完全控制", "隐私保护", "无成本"],
                priority=5
            )
        }

        for provider, config in configs.items():
            api_key = os.environ.get(config.api_key_env, "")
            if api_key or provider == LLMProvider.LOCAL:
                config.is_available = True
                logger.info(f"✅ 提供商可用: {config.name}")
            else:
                logger.info(f"⚠️ 提供商不可用: {config.name} (未设置{config.api_key_env})")

            self.providers[provider] = config

    def _build_fallback_chain(self):
        """构建Fallback链"""
        available = [p for p, c in self.providers.items() if c.is_available]
        available.sort(key=lambda p: self.providers[p].priority)
        self.fallback_chain = available
        logger.info(f"📋 Fallback链: {[p.value for p in self.fallback_chain]}")

    def route_task(self, task_type: TaskType,
                  preferred_provider: Optional[LLMProvider] = None) -> LLMProvider:
        """智能路由任务到最佳模型"""
        task_routing = {
            TaskType.PLOT_GENERATION: [LLMProvider.DEEPSEEK, LLMProvider.ZHIPU, LLMProvider.OPENAI],
            TaskType.CHARACTER_DIALOGUE: [LLMProvider.CLAUDE, LLMProvider.DEEPSEEK],
            TaskType.BATTLE_SCENE: [LLMProvider.DEEPSEEK, LLMProvider.OPENAI],
            TaskType.ROMANCE_SCENE: [LLMProvider.CLAUDE, LLMProvider.ZHIPU],
            TaskType.WORLD_BUILDING: [LLMProvider.ZHIPU, LLMProvider.DEEPSEEK],
            TaskType.QUALITY_CHECK: [LLMProvider.CLAUDE],
            TaskType.SENSORY_ENHANCE: [LLMProvider.OPENAI, LLMProvider.CLAUDE],
            TaskType.PLOT_REVIEW: [LLMProvider.CLAUDE, LLMProvider.DEEPSEEK],
            TaskType.CREATIVE_BRAINSTORM: [LLMProvider.CLAUDE, LLMProvider.OPENAI, LLMProvider.DEEPSEEK],
            TaskType.TEXT_OPTIMIZE: [LLMProvider.CLAUDE, LLMProvider.DEEPSEEK]
        }

        preferred_list = task_routing.get(task_type, [LLMProvider.DEEPSEEK])

        if preferred_provider and preferred_provider in self.fallback_chain:
            return preferred_provider

        for provider in preferred_list:
            if provider in self.fallback_chain:
                return provider

        return self.fallback_chain[0] if self.fallback_chain else LLMProvider.DEEPSEEK

    def get_fallback_chain(self, start_provider: LLMProvider = None) -> List[LLMProvider]:
        """获取fallback链"""
        if start_provider:
            try:
                start_idx = self.fallback_chain.index(start_provider)
                return self.fallback_chain[start_idx:]
            except ValueError:
                return self.fallback_chain

        return self.fallback_chain.copy()

    def generate_with_fallback(self, request: TaskRequest) -> LLMResponse:
        """使用Fallback机制生成"""
        primary_provider = self.route_task(
            request.task_type,
            request.preferred_provider
        )

        fallback_providers = self.get_fallback_chain(primary_provider)

        last_error = None

        for provider in fallback_providers:
            if not request.fallback_enabled and provider != primary_provider:
                break

            config = self.providers[provider]

            logger.info(f"尝试提供商: {config.name}")

            try:
                response = self._call_provider(config, request)

                if response.success:
                    self._record_request(provider, request, response)
                    return response

                last_error = response.error

            except Exception as e:
                logger.error(f"提供商{call_provider.__name__}异常: {e}")
                last_error = str(e)

        return LLMResponse(
            content="",
            provider=LLMProvider.DEEPSEEK,
            model="",
            success=False,
            error=f"All providers failed. Last error: {last_error}"
        )

    def _call_provider(self, config: LLMConfig, request: TaskRequest) -> LLMResponse:
        """调用LLM提供商"""
        start_time = time.time()

        if config.provider == LLMProvider.DEEPSEEK:
            return self._call_deepseek(config, request)
        elif config.provider == LLMProvider.OPENAI:
            return self._call_openai(config, request)
        elif config.provider == LLMProvider.CLAUDE:
            return self._call_claude(config, request)
        elif config.provider == LLMProvider.ZHIPU:
            return self._call_zhipu(config, request)
        else:
            return LLMResponse(
                content="",
                provider=config.provider,
                model=config.default_model,
                success=False,
                error="Unsupported provider"
            )

    def _call_deepseek(self, config: LLMConfig, request: TaskRequest) -> LLMResponse:
        """调用DeepSeek API"""
        import requests

        api_key = os.environ.get(config.api_key_env)
        if not api_key:
            return LLMResponse(
                content="",
                provider=config.provider,
                model=config.default_model,
                success=False,
                error="API key not found"
            )

        try:
            url = f"{config.base_url}/chat/completions"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }

            messages = []
            if request.system_prompt:
                messages.append({"role": "system", "content": request.system_prompt})
            messages.append({"role": "user", "content": request.prompt})

            data = {
                "model": config.default_model,
                "messages": messages,
                "temperature": request.temperature,
                "max_tokens": request.max_tokens
            }

            response = requests.post(url, headers=headers, json=data, timeout=120)
            response.raise_for_status()

            result = response.json()
            latency = (time.time() - start_time) * 1000

            return LLMResponse(
                content=result["choices"][0]["message"]["content"],
                provider=config.provider,
                model=config.default_model,
                success=True,
                latency_ms=latency
            )

        except Exception as e:
            return LLMResponse(
                content="",
                provider=config.provider,
                model=config.default_model,
                success=False,
                error=str(e)
            )

    def _call_openai(self, config: LLMConfig, request: TaskRequest) -> LLMResponse:
        """调用OpenAI API"""
        import requests

        api_key = os.environ.get(config.api_key_env)
        if not api_key:
            return LLMResponse(
                content="",
                provider=config.provider,
                model=config.default_model,
                success=False,
                error="API key not found"
            )

        try:
            url = f"{config.base_url}/chat/completions"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }

            messages = []
            if request.system_prompt:
                messages.append({"role": "system", "content": request.system_prompt})
            messages.append({"role": "user", "content": request.prompt})

            data = {
                "model": config.default_model,
                "messages": messages,
                "temperature": request.temperature,
                "max_tokens": request.max_tokens
            }

            response = requests.post(url, headers=headers, json=data, timeout=120)
            response.raise_for_status()

            result = response.json()
            latency = (time.time() - start_time) * 1000

            return LLMResponse(
                content=result["choices"][0]["message"]["content"],
                provider=config.provider,
                model=config.default_model,
                success=True,
                latency_ms=latency
            )

        except Exception as e:
            return LLMResponse(
                content="",
                provider=config.provider,
                model=config.default_model,
                success=False,
                error=str(e)
            )

    def _call_claude(self, config: LLMConfig, request: TaskRequest) -> LLMResponse:
        """调用Claude API"""
        import requests

        api_key = os.environ.get(config.api_key_env)
        if not api_key:
            return LLMResponse(
                content="",
                provider=config.provider,
                model=config.default_model,
                success=False,
                error="API key not found"
            )

        try:
            url = f"{config.base_url}/messages"
            headers = {
                "Content-Type": "application/json",
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01"
            }

            messages = []
            if request.system_prompt:
                messages.append({"role": "user", "content": request.system_prompt})
            messages.append({"role": "user", "content": request.prompt})

            data = {
                "model": config.default_model,
                "messages": messages,
                "temperature": request.temperature,
                "max_tokens": request.max_tokens
            }

            response = requests.post(url, headers=headers, json=data, timeout=120)
            response.raise_for_status()

            result = response.json()
            latency = (time.time() - start_time) * 1000

            return LLMResponse(
                content=result["content"][0]["text"],
                provider=config.provider,
                model=config.default_model,
                success=True,
                latency_ms=latency
            )

        except Exception as e:
            return LLMResponse(
                content="",
                provider=config.provider,
                model=config.default_model,
                success=False,
                error=str(e)
            )

    def _call_zhipu(self, config: LLMConfig, request: TaskRequest) -> LLMResponse:
        """调用智谱GLM API"""
        import requests

        api_key = os.environ.get(config.api_key_env)
        if not api_key:
            return LLMResponse(
                content="",
                provider=config.provider,
                model=config.default_model,
                success=False,
                error="API key not found"
            )

        try:
            url = f"{config.base_url}/chat/completions"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }

            messages = []
            if request.system_prompt:
                messages.append({"role": "system", "content": request.system_prompt})
            messages.append({"role": "user", "content": request.prompt})

            data = {
                "model": config.default_model,
                "messages": messages,
                "temperature": request.temperature,
                "max_tokens": request.max_tokens
            }

            response = requests.post(url, headers=headers, json=data, timeout=120)
            response.raise_for_status()

            result = response.json()
            latency = (time.time() - start_time) * 1000

            return LLMResponse(
                content=result["choices"][0]["message"]["content"],
                provider=config.provider,
                model=config.default_model,
                success=True,
                latency_ms=latency
            )

        except Exception as e:
            return LLMResponse(
                content="",
                provider=config.provider,
                model=config.default_model,
                success=False,
                error=str(e)
            )

    def _record_request(self, provider: LLMProvider, request: TaskRequest, response: LLMResponse):
        """记录请求历史"""
        self.request_history.append({
            "timestamp": datetime.now().isoformat(),
            "task_type": request.task_type.value,
            "provider": provider.value,
            "success": response.success,
            "latency_ms": response.latency_ms
        })

        if len(self.request_history) > 1000:
            self.request_history = self.request_history[-500:]

    def get_statistics(self) -> Dict:
        """获取统计信息"""
        stats = {
            "total_requests": len(self.request_history),
            "providers": {},
            "success_rate": {}
        }

        for provider in LLMProvider:
            provider_requests = [r for r in self.request_history if r["provider"] == provider.value]
            if provider_requests:
                success_count = sum(1 for r in provider_requests if r["success"])
                stats["providers"][provider.value] = len(provider_requests)
                stats["success_rate"][provider.value] = success_count / len(provider_requests)

        return stats

    def generate_routing_prompt(self, task_type: TaskType, context: str = "") -> str:
        """生成路由提示词"""
        routing_guide = {
            TaskType.PLOT_GENERATION: "剧情生成需要逻辑严密、节奏把控强，建议使用DeepSeek",
            TaskType.CHARACTER_DIALOGUE: "角色对话需要情感细腻、性格鲜明，建议使用Claude",
            TaskType.BATTLE_SCENE: "战斗场景需要紧张激烈、动作描写生动，建议使用DeepSeek",
            TaskType.ROMANCE_SCENE: "爱情场景需要情感丰富、氛围营造，建议使用Claude",
            TaskType.QUALITY_CHECK: "质量检查需要严谨细致，建议使用Claude"
        }

        guide = routing_guide.get(task_type, "使用默认路由策略")

        prompt = f"""任务类型: {task_type.value}
{guide}

上下文: {context or '无'}

请根据以上信息生成对应的内容。"""

        return prompt


def main():
    print("="*60)
    print("🔀 NWACS V8.5 多LLM智能路由系统")
    print("="*60)

    router = MultiLLMRouter()

    print("\n📊 提供商状态:")
    for provider, config in router.providers.items():
        status = "✅ 可用" if config.is_available else "❌ 不可用"
        print(f"  {config.name}: {status}")

    print("\n📋 Fallback链:")
    for i, provider in enumerate(router.fallback_chain, 1):
        print(f"  {i}. {provider.value}")

    print("\n🗺️ 任务路由表:")
    for task_type in TaskType:
        routed = router.route_task(task_type)
        print(f"  {task_type.value}: {routed.value}")

    print("\n" + "="*60)
    print("✅ 多LLM路由系统就绪")
    print("="*60)


if __name__ == "__main__":
    main()