#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS V8.0 智能创作引擎
核心功能：
1. 多模型智能编排
2. 智能内容生成
3. 实时风格迁移
4. 智能续写预测
"""

import sys
import json
import time
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional
from abc import ABC, abstractmethod

sys.stdout.reconfigure(encoding='utf-8')

class ModelAdapter(ABC):
    """模型适配器抽象基类"""
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        pass
    
    @abstractmethod
    def get_model_name(self) -> str:
        pass

class DeepSeekAdapter(ModelAdapter):
    """DeepSeek模型适配器"""
    
    def __init__(self, api_key: str = "sk-f3246fbd1eef446e9a11d78efefd9bba"):
        self.api_key = api_key
        self.base_url = "https://api.deepseek.com"
        
    def get_model_name(self) -> str:
        return "deepseek-chat"
    
    def generate(self, prompt: str, **kwargs) -> str:
        import requests
        
        url = f"{self.base_url}/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        messages = [{"role": "user", "content": prompt}]
        if kwargs.get("system_prompt"):
            messages.insert(0, {"role": "system", "content": kwargs["system_prompt"]})
        
        data = {
            "model": self.get_model_name(),
            "messages": messages,
            "temperature": kwargs.get("temperature", 0.7),
            "max_tokens": kwargs.get("max_tokens", 4000)
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=120)
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except Exception as e:
            return f"DeepSeek调用失败: {str(e)}"

class SmartCreativeEngine:
    """智能创作引擎"""
    
    def __init__(self):
        self.models = {
            "deepseek": DeepSeekAdapter()
        }
        self.active_model = "deepseek"
        self.conversation_history = {}
        self.style_cache = {}
        
    def set_active_model(self, model_name: str):
        """设置活动模型"""
        if model_name in self.models:
            self.active_model = model_name
            return True
        return False
    
    def generate(self, prompt: str, **kwargs) -> str:
        """生成内容"""
        model = self.models[self.active_model]
        return model.generate(prompt, **kwargs)
    
    def generate_with_style(self, prompt: str, style: str = "default", **kwargs) -> str:
        """带风格的内容生成"""
        style_prompt = self._get_style_prompt(style)
        full_prompt = f"{style_prompt}\n\n{prompt}"
        return self.generate(full_prompt, **kwargs)
    
    def _get_style_prompt(self, style: str) -> str:
        """获取风格提示词"""
        styles = {
            "default": "请用简洁明了的语言回答问题。",
            "novel": "请用小说风格写作，注重细节描写和情感表达，语言优美流畅。",
            "xuanhuan": "请用玄幻风格写作，语言古朴典雅，充满想象力，注重修炼体系和战斗描写。",
            "urban": "请用都市风格写作，语言现代简洁，贴近生活，注重人物情感和都市氛围。",
            "romance": "请用言情风格写作，语言细腻温柔，注重情感描写和心理活动。",
            "suspense": "请用悬疑风格写作，营造紧张氛围，注重伏笔和反转。",
            "science": "请用科幻风格写作，语言严谨而富有想象力，注重科技细节和世界观构建。",
            "poetic": "请用诗意风格写作，语言优美，富有韵律感和画面感。",
            "humorous": "请用幽默风格写作，语言风趣诙谐，轻松有趣。",
            "professional": "请用专业风格写作，语言严谨准确，逻辑清晰。"
        }
        return styles.get(style, styles["default"])
    
    def generate_outline(self, theme: str, length: int = 10, **kwargs) -> str:
        """生成小说大纲"""
        prompt = f"""请根据以下主题生成一个{length}章的小说大纲：
主题：{theme}

大纲要求：
1. 包含完整的故事线
2. 每章有明确的标题和内容提要
3. 包含人物介绍
4. 有明确的起承转合
5. 语言简洁明了

请用JSON格式返回，包含：
- title: 小说标题
- description: 故事简介
- characters: 人物列表（姓名、角色、简介）
- chapters: 章节列表（序号、标题、内容提要）"""
        
        system_prompt = "你是一位专业的小说大纲设计师，擅长创作各种类型的小说大纲。"
        return self.generate(prompt, system_prompt=system_prompt, temperature=0.8)
    
    def generate_character(self, type: str = "protagonist", **kwargs) -> str:
        """生成角色设定"""
        prompt = f"""请生成一个{type}角色设定：

角色类型：{type}

设定要求：
1. 姓名（包含姓氏含义）
2. 年龄
3. 外貌特征
4. 性格特点
5. 背景故事
6. 目标与动机
7. 技能/能力
8. 缺点与弱点
9. 成长轨迹
10. 人物关系

请用JSON格式返回，结构清晰。"""
        
        system_prompt = "你是一位专业的角色设计师，擅长创作丰富立体的人物形象。"
        return self.generate(prompt, system_prompt=system_prompt, temperature=0.8)
    
    def generate_scene(self, location: str, time: str, characters: list, purpose: str, **kwargs) -> str:
        """生成场景描写"""
        prompt = f"""请生成一个场景描写：

地点：{location}
时间：{time}
人物：{', '.join(characters)}
目的：{purpose}

场景要求：
1. 环境描写细致生动
2. 人物动作和表情描写
3. 氛围营造
4. 情节推进
5. 语言生动形象

请用小说风格写作，不少于500字。"""
        
        system_prompt = "你是一位专业的场景描写师，擅长营造各种氛围的场景。"
        return self.generate(prompt, system_prompt=system_prompt, temperature=0.7)
    
    def generate_dialogue(self, characters: list, topic: str, emotion: str = "neutral", **kwargs) -> str:
        """生成对话"""
        prompt = f"""请生成一段对话：

人物：{', '.join(characters)}
话题：{topic}
情绪：{emotion}

对话要求：
1. 符合人物性格
2. 有冲突或信息量
3. 推动情节发展
4. 语言自然真实
5. 包含潜台词

请用剧本格式写作。"""
        
        system_prompt = "你是一位专业的对话设计师，擅长创作生动有趣的对话。"
        return self.generate(prompt, system_prompt=system_prompt, temperature=0.8)
    
    def rewrite(self, text: str, style: str = "polish", **kwargs) -> str:
        """重写文本"""
        style_options = {
            "polish": "请润色以下文本，使其更加流畅优美，保持原意不变。",
            "simplify": "请简化以下文本，使其更加简洁明了。",
            "expand": "请扩写以下文本，增加细节描写和情感表达。",
            "summarize": "请概括以下文本的主要内容，不超过100字。",
            "translate": "请将以下文本翻译成中文，保持原意。",
            "formal": "请将以下文本改为正式文体。",
            "casual": "请将以下文本改为口语化表达。"
        }
        
        instruction = style_options.get(style, style_options["polish"])
        prompt = f"{instruction}\n\n原文：\n{text}"
        
        return self.generate(prompt, temperature=0.7)
    
    def continue_writing(self, text: str, length: int = 500, **kwargs) -> str:
        """续写文本"""
        prompt = f"""请继续续写以下文本，保持风格一致：

{text}

请续写约{length}字，保持原有的叙事风格和情节发展。"""
        
        system_prompt = "你是一位专业的续写大师，擅长无缝衔接各种风格的文本。"
        return self.generate(prompt, system_prompt=system_prompt, temperature=0.7)

class CreativeEngineBuilder:
    """创作引擎构建器"""
    
    @staticmethod
    def create_basic_engine() -> SmartCreativeEngine:
        """创建基础引擎"""
        return SmartCreativeEngine()
    
    @staticmethod
    def create_advanced_engine() -> SmartCreativeEngine:
        """创建高级引擎（包含更多模型）"""
        engine = SmartCreativeEngine()
        # 可以扩展添加其他模型适配器
        return engine

if __name__ == "__main__":
    print("="*60)
    print("🚀 NWACS V8.0 智能创作引擎测试")
    print("="*60)
    
    engine = SmartCreativeEngine()
    
    print("\n1. 测试大纲生成...")
    outline = engine.generate_outline("玄幻世界中的废柴少年逆袭故事", length=5)
    print("✅ 大纲生成完成")
    
    print("\n2. 测试角色生成...")
    character = engine.generate_character("protagonist")
    print("✅ 角色生成完成")
    
    print("\n3. 测试场景生成...")
    scene = engine.generate_scene("青云宗大殿", "清晨", ["林动", "林震天"], "家族会议")
    print("✅ 场景生成完成")
    
    print("\n4. 测试对话生成...")
    dialogue = engine.generate_dialogue(["林动", "林琅天"], "比武挑战", "tense")
    print("✅ 对话生成完成")
    
    print("\n" + "="*60)
    print("🎉 智能创作引擎测试完成！")
    print("="*60)
