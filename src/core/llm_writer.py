#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 大模型创作接口
连接大模型与Skill进行文学创作
"""

import json
import os
import time
from datetime import datetime
from logger import logger

class LLMWriter:
    """大模型创作器"""

    def __init__(self):
        self.llm_client = None
        self.enabled = False
        self.skill_knowledge = {}
        self.model = 'gpt-3.5-turbo'
        self._init_llm_client()

    def _init_llm_client(self):
        """初始化大模型客户端"""
        try:
            import openai

            config = self._load_config()
            api_key = config.get('api_key') or os.environ.get('OPENAI_API_KEY') or os.environ.get('DEEPSEEK_API_KEY')
            base_url = config.get('base_url') or os.environ.get('OPENAI_BASE_URL')
            self.model = config.get('model', 'gpt-3.5-turbo')

            if api_key and config.get('enabled', False):
                if base_url:
                    self.llm_client = openai.OpenAI(api_key=api_key, base_url=base_url)
                else:
                    self.llm_client = openai.OpenAI(api_key=api_key)
                self.enabled = True
                logger.info("大模型客户端已初始化")
            else:
                logger.info("未启用或未配置API密钥，大模型功能未启用")
        except ImportError:
            logger.info("openai库未安装，大模型功能未启用")
        except Exception as e:
            logger.log_exception(e, "初始化大模型客户端")

    def _load_config(self):
        """从配置文件加载设置"""
        config_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config.json')
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def load_skill_knowledge(self, skill_name=None):
        """加载Skill知识库"""
        kb_file = "skill_knowledge_base.json"
        if os.path.exists(kb_file):
            try:
                with open(kb_file, 'r', encoding='utf-8') as f:
                    self.skill_knowledge = json.load(f)
                logger.info("知识库已加载")
            except Exception as e:
                logger.log_exception(e, "加载知识库")

    def write_with_skill(self, skill_name, prompt, max_tokens=2000, temperature=0.7):
        """使用指定Skill知识进行创作"""
        if not self.enabled:
            return {"error": "大模型未启用"}

        try:
            enhanced_prompt = self._build_enhanced_prompt(skill_name, prompt)

            response = self.llm_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._get_system_prompt(skill_name)},
                    {"role": "user", "content": enhanced_prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )

            result = response.choices[0].message.content

            return {
                'skill_name': skill_name,
                'content': result,
                'model': self.model,
                'timestamp': datetime.now().isoformat(),
                'prompt_tokens': response.usage.prompt_tokens,
                'completion_tokens': response.usage.completion_tokens
            }

        except Exception as e:
            logger.log_exception(e, "write_with_skill")
            return {"error": str(e)}

    def _get_system_prompt(self, skill_name):
        """获取系统提示词"""
        skill_prompts = {
            '短篇小说爽文大师': """你是一位专业的短篇小说爽文作家，擅长创作高爽点、高完读率的短篇故事。
熟悉2025-2026年热门题材：都市脑洞、战神赘婿、重生复仇、穿书系统等。
请按照以下原则创作：
1. 开篇100字抓住读者
2. 爽点密集，节奏明快
3. 人物鲜明，冲突明确
4. 结局留有回味""",

            '写作技巧大师': """你是一位资深写作导师，精通各种写作技巧和风格。
擅长：风格定位、修辞手法、节奏控制、去AI化写作。
请提供专业的写作建议和润色服务。""",

            '剧情构造师': """你是一位专业的剧情设计师，擅长构建精彩的故事结构。
精通：三幕式结构、伏笔埋设、节奏控制、反转设计。
请帮助设计紧凑精彩的剧情。""",

            '角色塑造师': """你是一位人物塑造专家，擅长创造鲜活立体的角色。
精通：性格刻画、动机设定、人物弧光、关系网络构建。
请帮助塑造令人难忘的角色。""",

            '世界观构造师': """你是一位世界构建大师，擅长创造独特而自洽的世界观。
精通：规则设计、历史背景、势力设定、细节丰富。
请帮助构建引人入胜的世界。""",

            '战斗设计师': """你是一位战斗场景描写专家，擅长创造紧张刺激的战斗场面。
精通：招式设计、节奏控制、场面描写、境界差异。
请帮助设计精彩的战斗场景。""",

            '对话设计师': """你是一位对话写作专家，擅长创作自然生动的对话。
精通：个性塑造、潜台词设计、节奏控制、情感表达。
请帮助创作精彩的对话。"""
        }

        return skill_prompts.get(skill_name, """你是一位专业的小说创作助手，擅长各种类型的文学创作。""")

    def _build_enhanced_prompt(self, skill_name, prompt):
        """构建增强提示词"""
        related_knowledge = self._get_related_knowledge(skill_name)

        if related_knowledge:
            knowledge_str = "\n参考知识：\n" + "\n".join(related_knowledge[:3])
        else:
            knowledge_str = ""

        return f"""请根据以下要求进行创作：

{prompt}

{knowledge_str}

请输出完整的创作内容，保持自然流畅的风格。"""

    def _get_related_knowledge(self, skill_name):
        """获取相关知识"""
        knowledge_items = []

        for key, data in self.skill_knowledge.items():
            if data.get('skill_name') == skill_name:
                content = data.get('content', [])
                for item in content:
                    if 'key_points' in item:
                        knowledge_items.extend(item['key_points'])
                    if 'tips' in item:
                        knowledge_items.extend(item['tips'])

        return knowledge_items

    def collaborative_write(self, skill_names, prompt):
        """多Skill协作创作"""
        if not self.enabled:
            return {"error": "大模型未启用"}

        try:
            all_knowledge = []
            for skill_name in skill_names:
                knowledge = self._get_related_knowledge(skill_name)
                all_knowledge.extend(knowledge)

            system_prompt = self._get_collaborative_system_prompt(skill_names)

            knowledge_str = ""
            if all_knowledge:
                knowledge_str = "\n参考知识（来自多个Skill）：\n" + "\n".join(all_knowledge[:5])

            user_prompt = f"""{prompt}

{knowledge_str}

请输出完整的创作内容。"""

            response = self.llm_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=3000
            )

            result = response.choices[0].message.content

            return {
                'skills': skill_names,
                'content': result,
                'model': self.model,
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            logger.log_exception(e, "collaborative_write")
            return {"error": str(e)}

    def _get_collaborative_system_prompt(self, skill_names):
        """获取协作系统提示词"""
        prompts = []
        for name in skill_names:
            prompt = self._get_system_prompt(name)
            prompts.append(f"【{name}】\n{prompt}")

        return "\n\n".join(prompts) + "\n\n请综合运用以上所有Skill的专业知识进行创作。"


_writer_instance = None

def get_llm_writer():
    """获取大模型创作器单例"""
    global _writer_instance
    if _writer_instance is None:
        _writer_instance = LLMWriter()
    return _writer_instance


if __name__ == "__main__":
    print("=====================================")
    print("    NWACS 大模型创作接口测试")
    print("=====================================")

    writer = get_llm_writer()

    if not writer.enabled:
        print("大模型未启用，请在config.json中配置API密钥")
        exit(1)

    writer.load_skill_knowledge()

    test_prompt = """请写一个都市脑洞短篇爽文开头（1000字左右）
要求：
1. 现代都市背景
2. 反套路金手指
3. 开篇即爽点
4. 留下悬念"""

    print("\n正在创作...")
    result = writer.write_with_skill('短篇小说爽文大师', test_prompt)

    if 'error' in result:
        print(f"错误: {result['error']}")
    else:
        print("\n创作完成！")
        print("=" * 60)
        print(result['content'][:500] + "..." if len(result['content']) > 500 else result['content'])