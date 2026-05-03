#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS V8.0 角色模板系统
确保小说创作中角色始终一致：性格、人物属性、剧情
"""

import sys
import json
import os
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "sk-f3246fbd1eef446e9a11d78efefd9bba"
BASE_URL = "https://api.deepseek.com"

def call_deepseek(prompt, system_prompt=None, temperature=0.7):
    """调用DeepSeek API"""
    import requests
    try:
        url = f"{BASE_URL}/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        data = {
            "model": "deepseek-chat",
            "messages": messages,
            "temperature": temperature,
            "max_tokens": 8000
        }
        response = requests.post(url, headers=headers, json=data, timeout=300)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"   ❌ DeepSeek调用失败: {e}")
        return None


class CharacterTemplate:
    """角色模板类"""

    def __init__(self, name, role_type="protagonist"):
        self.name = name
        self.role_type = role_type  # protagonist, heroine, antagonist, supporting
        self.template = {
            "name": name,
            "role_type": role_type,
            "basic_info": {
                "age": "",
                "gender": "",
                "appearance": "",
                "background": ""
            },
            "personality": {
                "core_traits": [],
                "strengths": [],
                "weaknesses": [],
                "speaking_style": "",
                "behavior_patterns": []
            },
            "abilities": {
                "combat_ability": "",
                "special_skills": [],
                "cultivation_realm": "",
                "weapons": []
            },
            "relationships": {},
            "character_arc": {
                "starting_state": "",
                "development": "",
                "ending_state": ""
            },
            "consistency_rules": [
                "不得改变核心性格特征",
                "行为必须符合人物设定",
                "语言风格保持一致"
            ],
            "appearance_log": [],
            "behavior_log": [],
            "dialogue_log": []
        }

    def to_dict(self):
        return self.template

    def get_context_prompt(self):
        """生成角色上下文提示"""
        lines = []
        lines.append(f"【角色：{self.name}】")
        lines.append(f"身份：{self.role_type}")

        basic = self.template["basic_info"]
        if basic.get("appearance"):
            lines.append(f"外貌：{basic['appearance']}")

        pers = self.template["personality"]
        if pers.get("core_traits"):
            lines.append(f"核心性格：{', '.join(pers['core_traits'])}")
        if pers.get("speaking_style"):
            lines.append(f"说话风格：{pers['speaking_style']}")

        abilities = self.template["abilities"]
        if abilities.get("cultivation_realm"):
            lines.append(f"境界：{abilities['cultivation_realm']}")

        return "\n".join(lines)


class CharacterTemplateManager:
    """角色模板管理器"""

    def __init__(self, novel_name):
        self.novel_name = novel_name
        self.characters_dir = f"novels/{novel_name}/characters"
        os.makedirs(self.characters_dir, exist_ok=True)
        self.template_file = f"{self.characters_dir}/character_templates.json"
        self.characters = {}
        self.load_templates()

    def load_templates(self):
        """加载角色模板"""
        if os.path.exists(self.template_file):
            try:
                with open(self.template_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for name, template_data in data.items():
                        char = CharacterTemplate(name)
                        char.template = template_data
                        self.characters[name] = char
                print(f"   ✅ 已加载 {len(self.characters)} 个角色模板")
            except Exception as e:
                print(f"   ⚠️ 加载角色模板失败: {e}")

    def save_templates(self):
        """保存角色模板"""
        data = {name: char.to_dict() for name, char in self.characters.items()}
        with open(self.template_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"   ✅ 已保存 {len(self.characters)} 个角色模板")

    def create_character(self, name, role_type="protagonist"):
        """创建新角色"""
        char = CharacterTemplate(name, role_type)
        self.characters[name] = char
        return char

    def get_character(self, name):
        """获取角色"""
        return self.characters.get(name)

    def list_characters(self):
        """列出所有角色"""
        return list(self.characters.keys())

    def get_all_characters_context(self):
        """获取所有角色的上下文提示"""
        lines = ["\n【小说角色设定】"]
        for char in self.characters.values():
            lines.append(char.get_context_prompt())
            lines.append("")
        return "\n".join(lines)

    def update_character_behavior(self, name, scene_description):
        """更新角色行为日志（用于后续检查一致性）"""
        if name in self.characters:
            self.characters[name].template["behavior_log"].append({
                "scene": scene_description,
                "timestamp": datetime.now().isoformat()
            })

    def update_character_dialogue(self, name, dialogue):
        """更新角色对话日志"""
        if name in self.characters:
            self.characters[name].template["dialogue_log"].append({
                "dialogue": dialogue,
                "timestamp": datetime.now().isoformat()
            })

    def check_consistency(self, name, proposed_action):
        """检查角色行为一致性"""
        if name not in self.characters:
            return True, ""

        char = self.characters[name]
        traits = char.template["personality"]["core_traits"]
        rules = char.template["consistency_rules"]

        warnings = []

        for trait in traits:
            if trait.lower() not in proposed_action.lower():
                warnings.append(f"注意：当前行为可能与角色核心性格「{trait}」不符")

        return len(warnings) == 0, "\n".join(warnings)


def design_characters_with_deepseek(novel_name, genre):
    """使用DeepSeek设计角色模板"""
    print("\n" + "="*60)
    print("🎭 使用DeepSeek设计角色模板")
    print("="*60)

    prompt = f"""请为小说《{novel_name}》（{genre}类型）设计主要角色模板：

请设计以下角色：

1. **主角**（1人）
   - 姓名、年龄、性别
   - 外貌特征
   - 背景故事
   - 核心性格特征（3-5个）
   - 性格优点和缺点
   - 说话风格
   - 行为模式
   - 修炼境界（如果是玄幻）
   - 特殊能力/技能
   - 人物关系

2. **女主/男主**（1-2人）
   - 同上的完整设定

3. **重要配角**（3-5人）
   - 简要设定

4. **反派**（1-2人）
   - 动机和目标
   - 与主角的关系

请以JSON格式返回，包含完整的角色设定。

JSON格式：
{{
  "角色名称": {{
    "role_type": "protagonist/heroine/antagonist/supporting",
    "basic_info": {{
      "age": "",
      "gender": "",
      "appearance": "",
      "background": ""
    }},
    "personality": {{
      "core_traits": [],
      "strengths": [],
      "weaknesses": [],
      "speaking_style": "",
      "behavior_patterns": []
    }},
    "abilities": {{
      "combat_ability": "",
      "special_skills": [],
      "cultivation_realm": "",
      "weapons": []
    }},
    "relationships": {{}},
    "character_arc": {{
      "starting_state": "",
      "development": "",
      "ending_state": ""
    }}
  }}
}}"""

    system_prompt = "你是一位专业的小说人物塑造师，擅长设计立体、有魅力、性格鲜明的角色。"

    print("   ⏳ DeepSeek正在设计角色...")
    result = call_deepseek(prompt, system_prompt, temperature=0.7)

    if result:
        manager = CharacterTemplateManager(novel_name)

        try:
            char_data = json.loads(result)

            for name, data in char_data.items():
                role_type = data.get("role_type", "supporting")
                char = manager.create_character(name, role_type)
                char.template.update(data)

            manager.save_templates()

            print(f"\n   ✅ 已创建 {len(char_data)} 个角色模板")
            return manager

        except json.JSONDecodeError:
            print("   ⚠️ 解析角色数据失败，尝试保存为文本")
            with open(f"novels/{novel_name}/characters/raw_character_design.md", 'w', encoding='utf-8') as f:
                f.write(result)
            return None

    return None


def display_character_templates(manager):
    """显示角色模板"""
    if not manager:
        print("   ❌ 没有角色模板")
        return

    print("\n" + "="*60)
    print("🎭 角色模板总览")
    print("="*60)

    for char in manager.characters.values():
        print(f"\n【{char.name}】- {char.role_type}")
        print(f"  外貌：{char.template['basic_info'].get('appearance', '未设定')[:50]}...")
        print(f"  性格：{', '.join(char.template['personality'].get('core_traits', []))}")
        print(f"  境界：{char.template['abilities'].get('cultivation_realm', '未设定')}")


def main():
    print("="*60)
    print("🎭 NWACS V8.0 角色模板系统")
    print("="*60)
    print("\n确保小说创作中角色始终一致！")
    print("="*60)

    novel_name = input("\n请输入小说名称: ").strip()
    if not novel_name:
        novel_name = "测试小说"

    manager = CharacterTemplateManager(novel_name)

    if manager.list_characters():
        print("\n检测到已存在的角色模板！")
        display_character_templates(manager)

        choice = input("\n要重新设计角色吗？(y/N): ").strip().lower()
        if choice == "y":
            manager = None
    else:
        choice = "y"

    if manager is None or not manager.list_characters():
        genre = input("请输入小说类型（默认=玄幻）: ").strip() or "玄幻"
        manager = design_characters_with_deepseek(novel_name, genre)

    if manager:
        display_character_templates(manager)

        print("\n📁 角色模板已保存到:")
        print(f"   {manager.template_file}")

        print("\n【角色模板系统特点】")
        print("   ✅ 所有角色性格设定一致")
        print("   ✅ 在写作时可调用角色上下文")
        print("   ✅ 检查角色行为一致性")
        print("   ✅ 记录角色行为和对话日志")


if __name__ == "__main__":
    main()
