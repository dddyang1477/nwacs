#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS-Orchestrator v4.0
外部编排器 — 脱离 Trae 的 Agent 自动化引擎
支持：Kimi / DeepSeek / OpenAI 兼容接口
"""

import os
import json
import time
import re
import sqlite3
from datetime import datetime
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, asdict
from pathlib import Path

import openai
from openai import OpenAI

# ==================== 配置加载 ====================

@dataclass
class ModelConfig:
    name: str
    api_key: str
    base_url: str
    model_id: str
    max_tokens: int = 8192
    temperature: float = 0.7

@dataclass  
class AgentConfig:
    name: str
    prompt_file: str
    model: str  # 指向 ModelConfig.name
    priority: int = 1
    max_retries: int = 3
    timeout: int = 120

class ConfigManager:
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.models: Dict[str, ModelConfig] = {}
        self.agents: Dict[str, AgentConfig] = {}
        self._load_models()
        self._load_agents()

    def _load_models(self):
        """加载模型配置"""
        models_file = self.config_dir / "models.json"
        if not models_file.exists():
            self._create_default_models()

        with open(models_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        for name, cfg in data.items():
            self.models[name] = ModelConfig(**cfg)
        print(f"已加载 {len(self.models)} 个模型配置")

    def _load_agents(self):
        """加载 Agent 配置"""
        agents_file = self.config_dir / "agents.json"
        if not agents_file.exists():
            self._create_default_agents()

        with open(agents_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        for name, cfg in data.items():
            self.agents[name] = AgentConfig(**cfg)
        print(f"已加载 {len(self.agents)} 个 Agent 配置")

    def _create_default_models(self):
        """创建默认模型配置模板"""
        default = {
            "kimi-k2.6": {
                "name": "kimi-k2.6",
                "api_key": "YOUR_KIMI_API_KEY",
                "base_url": "https://api.moonshot.cn/v1",
                "model_id": "kimi-k2.6",
                "max_tokens": 8192,
                "temperature": 0.7
            },
            "deepseek-v3.2": {
                "name": "deepseek-v3.2",
                "api_key": "YOUR_DEEPSEEK_API_KEY",
                "base_url": "https://api.deepseek.com/v1",
                "model_id": "deepseek-chat",
                "max_tokens": 8192,
                "temperature": 0.7
            }
        }
        os.makedirs(self.config_dir, exist_ok=True)
        with open(self.config_dir / "models.json", "w", encoding="utf-8") as f:
            json.dump(default, f, indent=2, ensure_ascii=False)
        print("已创建默认模型配置模板，请编辑 config/models.json 填入真实 API Key")

    def _create_default_agents(self):
        """创建默认 Agent 配置"""
        default = {
            "调度官": {
                "name": "调度官",
                "prompt_file": "agents/调度官.md",
                "model": "kimi-k2.6",
                "priority": 1,
                "max_retries": 3,
                "timeout": 120
            },
            "剧情构造师": {
                "name": "剧情构造师",
                "prompt_file": "agents/剧情构造师.md",
                "model": "deepseek-v3.2",
                "priority": 2,
                "max_retries": 3,
                "timeout": 120
            },
            "场景构造师": {
                "name": "场景构造师",
                "prompt_file": "agents/场景构造师.md",
                "model": "deepseek-v3.2",
                "priority": 2,
                "max_retries": 3,
                "timeout": 120
            },
            "对话设计师": {
                "name": "对话设计师",
                "prompt_file": "agents/对话设计师.md",
                "model": "deepseek-v3.2",
                "priority": 2,
                "max_retries": 3,
                "timeout": 120
            },
            "去AI监督官": {
                "name": "去AI监督官",
                "prompt_file": "agents/去AI监督官.md",
                "model": "kimi-k2.6",
                "priority": 3,
                "max_retries": 3,
                "timeout": 120
            },
            "质量审计师": {
                "name": "质量审计师",
                "prompt_file": "agents/质量审计师.md",
                "model": "kimi-k2.6",
                "priority": 3,
                "max_retries": 3,
                "timeout": 120
            }
        }
        os.makedirs(self.config_dir, exist_ok=True)
        with open(self.config_dir / "agents.json", "w", encoding="utf-8") as f:
            json.dump(default, f, indent=2, ensure_ascii=False)
        print("已创建默认 Agent 配置，请确保 agents/ 目录下有对应的 .md 文件")

    def get_model(self, name: str) -> ModelConfig:
        if name not in self.models:
            raise ValueError(f"未知模型: {name}")
        return self.models[name]

    def get_agent(self, name: str) -> AgentConfig:
        if name not in self.agents:
            raise ValueError(f"未知Agent: {name}")
        return self.agents[name]


# ==================== LLM 客户端 ====================

class LLMClient:
    def __init__(self, config: ModelConfig):
        self.config = config
        self.client = OpenAI(
            api_key=config.api_key,
            base_url=config.base_url
        )
        self.call_count = 0
        self.total_tokens = 0

    def chat(self, system_prompt: str, user_message: str, 
             temperature: float = None, max_tokens: int = None) -> Dict:
        """调用模型，返回结果+用量统计"""
        temp = temperature or self.config.temperature
        max_tok = max_tokens or self.config.max_tokens

        try:
            response = self.client.chat.completions.create(
                model=self.config.model_id,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=temp,
                max_tokens=max_tok
            )

            self.call_count += 1
            usage = response.usage
            self.total_tokens += usage.total_tokens

            return {
                "success": True,
                "content": response.choices[0].message.content,
                "model": self.config.model_id,
                "prompt_tokens": usage.prompt_tokens,
                "completion_tokens": usage.completion_tokens,
                "total_tokens": usage.total_tokens,
                "cost_usd": self._calculate_cost(usage.prompt_tokens, usage.completion_tokens)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "model": self.config.model_id
            }

    def _calculate_cost(self, prompt_tokens: int, completion_tokens: int) -> float:
        """计算单次调用成本（USD）"""
        # 价格表（每百万token）
        pricing = {
            "kimi-k2.6": {"input": 0.60, "output": 2.50},
            "kimi-k2.5": {"input": 0.60, "output": 2.50},
            "deepseek-chat": {"input": 0.14, "output": 0.28},
            "deepseek-reasoner": {"input": 0.55, "output": 2.19}
        }

        model_pricing = pricing.get(self.config.model_id, {"input": 0.50, "output": 1.50})
        input_cost = (prompt_tokens / 1_000_000) * model_pricing["input"]
        output_cost = (completion_tokens / 1_000_000) * model_pricing["output"]
        return round(input_cost + output_cost, 6)


# ==================== Agent 执行器 ====================

class AgentExecutor:
    def __init__(self, config_manager: ConfigManager):
        self.config = config_manager
        self.clients: Dict[str, LLMClient] = {}
        self.history: List[Dict] = []
        self._init_clients()

    def _init_clients(self):
        """初始化所有模型客户端"""
        for name, model_cfg in self.config.models.items():
            if model_cfg.api_key and not model_cfg.api_key.startswith("YOUR_"):
                self.clients[name] = LLMClient(model_cfg)
                print(f"初始化模型客户端: {name}")
            else:
                print(f"跳过未配置模型: {name}")

    def load_prompt(self, prompt_file: str) -> str:
        """加载 Agent System Prompt"""
        path = Path(prompt_file)
        if not path.exists():
            # 尝试从 agents/ 目录查找
            path = Path("agents") / prompt_file

        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        return f"# 角色: {prompt_file}\n（Prompt文件未找到，使用默认配置）"

    def execute(self, agent_name: str, task_input: str, 
                context_files: List[str] = None) -> Dict:
        """
        执行单个 Agent

        Args:
            agent_name: Agent名称
            task_input: 任务输入
            context_files: 需要读取的上下文文件路径列表
        """
        agent_cfg = self.config.get_agent(agent_name)
        model_cfg = self.config.get_model(agent_cfg.model)

        if agent_cfg.model not in self.clients:
            return {"success": False, "error": f"模型 {agent_cfg.model} 未初始化"}

        client = self.clients[agent_cfg.model]
        system_prompt = self.load_prompt(agent_cfg.prompt_file)

        # 构建用户消息（附加上下文文件）
        user_message = task_input
        if context_files:
            context_parts = ["【上下文文件】"]
            for file_path in context_files:
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        # 截断过长内容
                        if len(content) > 10000:
                            content = content[:10000] + "\n...（已截断）"
                        context_parts.append(f"\n--- {file_path} ---\n{content}")
                except Exception as e:
                    context_parts.append(f"\n--- {file_path} ---\n[读取失败: {e}]")
            user_message = "\n".join(context_parts) + "\n\n【任务】\n" + task_input

        # 执行调用
        print(f"执行 Agent: {agent_name} | 模型: {agent_cfg.model}")
        start_time = time.time()

        result = client.chat(system_prompt, user_message)
        result["agent"] = agent_name
        result["duration_sec"] = round(time.time() - start_time, 2)
        result["timestamp"] = datetime.now().isoformat()

        self.history.append(result)

        if result["success"]:
            print(f"{agent_name} 完成 | 耗时: {result['duration_sec']}s | "
                  f"Token: {result.get('total_tokens', 0)} | 成本: ${result.get('cost_usd', 0)}")
        else:
            print(f"{agent_name} 失败 | 错误: {result.get('error', '未知')}")

        return result

    def get_cost_report(self) -> Dict:
        """生成成本报告"""
        total_cost = sum(h.get("cost_usd", 0) for h in self.history if h.get("success"))
        total_tokens = sum(h.get("total_tokens", 0) for h in self.history if h.get("success"))

        by_agent = {}
        for h in self.history:
            if not h.get("success"):
                continue
            agent = h["agent"]
            if agent not in by_agent:
                by_agent[agent] = {"calls": 0, "tokens": 0, "cost_usd": 0}
            by_agent[agent]["calls"] += 1
            by_agent[agent]["tokens"] += h.get("total_tokens", 0)
            by_agent[agent]["cost_usd"] += h.get("cost_usd", 0)

        return {
            "total_calls": len(self.history),
            "successful_calls": sum(1 for h in self.history if h.get("success")),
            "total_tokens": total_tokens,
            "total_cost_usd": round(total_cost, 4),
            "total_cost_cny": round(total_cost * 7.2, 4),
            "by_agent": by_agent
        }


# ==================== 流水线编排 ====================

class Pipeline:
    def __init__(self, executor: AgentExecutor):
        self.executor = executor
        self.steps: List[Dict] = []
        self.results: List[Dict] = []

    def add_step(self, agent_name: str, task: str, 
                 context_files: List[str] = None,
                 condition: Callable = None):
        """添加流水线步骤"""
        self.steps.append({
            "agent": agent_name,
            "task": task,
            "context_files": context_files or [],
            "condition": condition
        })

    def run(self, initial_input: str = "") -> List[Dict]:
        """执行完整流水线"""
        print(f"\n{'='*60}")
        print(f"NWACS 流水线启动 | 共 {len(self.steps)} 个步骤")
        print(f"{'='*60}\n")

        current_input = initial_input

        for i, step in enumerate(self.steps, 1):
            print(f"\nStep {i}/{len(self.steps)}: {step['agent']}")
            print("-" * 40)

            # 检查条件
            if step["condition"] and not step["condition"](self.results):
                print(f"条件不满足，跳过 {step['agent']}")
                continue

            # 构建任务输入
            task = step["task"]
            if current_input:
                task = f"【前置输出】\n{current_input}\n\n【当前任务】\n{task}"

            # 执行
            result = self.executor.execute(
                step["agent"],
                task,
                step["context_files"]
            )

            self.results.append(result)

            if result["success"]:
                current_input = result["content"]
            else:
                print(f"步骤失败，流水线中断")
                break

        # 输出成本报告
        report = self.executor.get_cost_report()
        print(f"\n{'='*60}")
        print("流水线成本报告")
        print(f"{'='*60}")
        print(f"总调用: {report['total_calls']} | 成功: {report['successful_calls']}")
        print(f"总Token: {report['total_tokens']:,}")
        print(f"总成本: ${report['total_cost_usd']} (约 ¥{report['total_cost_cny']})")
        print(f"\n按Agent统计:")
        for agent, data in report["by_agent"].items():
            print(f"  {agent}: {data['calls']}次 | {data['tokens']:,}token | ${round(data['cost_usd'], 4)}")

        return self.results


# ==================== 快捷函数 ====================

def create_default_project():
    """创建默认项目结构"""
    dirs = ["config", "agents", "output", "output/chapters", "output/review"]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    print("项目结构已创建")
    print("目录: config/, agents/, output/")


if __name__ == "__main__":
    create_default_project()
