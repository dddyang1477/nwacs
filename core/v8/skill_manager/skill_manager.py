#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS V8.0 Skill管理器
核心功能：
1. Skill注册与管理
2. 智能Skill匹配
3. Skill执行调度
4. 结果整合
"""

import sys
import json
import time
import importlib
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
from enum import Enum

try:
    sys.stdout.reconfigure(encoding='utf-8')
except (AttributeError, OSError):
    pass

class SkillType(Enum):
    """Skill类型枚举"""
    WORLD_BUILDING = "world_building"      # 世界观构造
    CHARACTER_DESIGN = "character_design"  # 角色设计
    PLOT_DESIGN = "plot_design"            # 情节设计
    SCENE_DESCRIPTION = "scene_description" # 场景描写
    DIALOGUE_WRITING = "dialogue_writing"  # 对话写作
    COMBAT_DESIGN = "combat_design"        # 战斗设计
    STYLE_REFINEMENT = "style_refinement"  # 风格润色
    OUTLINE_GENERATION = "outline_generation" # 大纲生成
    NOVEL_WRITING = "novel_writing"        # 小说创作
    PROOFREADING = "proofreading"          # 校对审核
    MARKET_ANALYSIS = "market_analysis"    # 市场分析

class SkillMetadata:
    """Skill元数据"""
    
    def __init__(self, skill_id: str, name: str, skill_type: SkillType, 
                 description: str, tags: List[str], 
                 input_schema: Dict[str, Any], output_schema: Dict[str, Any],
                 priority: int = 50, enabled: bool = True):
        self.skill_id = skill_id
        self.name = name
        self.skill_type = skill_type
        self.description = description
        self.tags = tags
        self.input_schema = input_schema
        self.output_schema = output_schema
        self.priority = priority
        self.enabled = enabled
        self.last_used = None
        self.usage_count = 0
    
    def to_dict(self):
        return {
            "skill_id": self.skill_id,
            "name": self.name,
            "skill_type": self.skill_type.value,
            "description": self.description,
            "tags": self.tags,
            "priority": self.priority,
            "enabled": self.enabled,
            "usage_count": self.usage_count
        }

class Skill:
    """Skill基类"""
    
    def __init__(self, metadata: SkillMetadata):
        self.metadata = metadata
        self.engine = None
    
    def set_engine(self, engine):
        """设置创作引擎"""
        self.engine = engine
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """执行Skill"""
        self.metadata.usage_count += 1
        self.metadata.last_used = datetime.now()
        return self._execute(**kwargs)
    
    def _execute(self, **kwargs) -> Dict[str, Any]:
        """子类实现具体逻辑"""
        raise NotImplementedError("子类必须实现_execute方法")

class WorldBuildingSkill(Skill):
    """世界观构造Skill"""
    
    def __init__(self):
        metadata = SkillMetadata(
            skill_id="world_building",
            name="世界观构造师",
            skill_type=SkillType.WORLD_BUILDING,
            description="构建完整的小说世界观，包括地理、历史、文化、势力等",
            tags=["玄幻", "都市", "科幻", "奇幻", "世界观"],
            input_schema={
                "type": "object",
                "properties": {
                    "world_type": {"type": "string", "description": "世界类型"},
                    "elements": {"type": "array", "items": {"type": "string"}, "description": "需要构建的元素"}
                },
                "required": ["world_type"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "world_name": {"type": "string"},
                    "geography": {"type": "object"},
                    "history": {"type": "object"},
                    "cultures": {"type": "array"},
                    "forces": {"type": "array"},
                    "rules": {"type": "array"}
                }
            },
            priority=90
        )
        super().__init__(metadata)
    
    def _execute(self, **kwargs):
        world_type = kwargs.get("world_type", "玄幻")
        elements = kwargs.get("elements", ["geography", "history", "cultures", "forces", "rules"])
        
        prompt = f"""请构建一个{world_type}世界的世界观：

需要构建的元素：{', '.join(elements)}

要求：
1. 世界名称：独特且符合类型
2. 地理：包含大陆、海洋、山脉等
3. 历史：重要事件和时间线
4. 文化：宗教、习俗、语言
5. 势力：主要势力和关系
6. 规则：世界法则和力量体系

请用JSON格式返回。"""
        
        result = self.engine.generate(prompt, system_prompt="你是一位专业的世界观构建师，擅长创造完整的虚构世界。")
        
        try:
            return json.loads(result)
        except:
            return {"world_name": f"{world_type}世界", "description": result}

class CharacterDesignSkill(Skill):
    """角色设计Skill"""
    
    def __init__(self):
        metadata = SkillMetadata(
            skill_id="character_design",
            name="角色塑造师",
            skill_type=SkillType.CHARACTER_DESIGN,
            description="设计立体丰满的小说角色",
            tags=["角色", "人设", "人物", "主角", "配角"],
            input_schema={
                "type": "object",
                "properties": {
                    "character_type": {"type": "string", "description": "角色类型"},
                    "world_type": {"type": "string", "description": "所属世界类型"},
                    "role": {"type": "string", "description": "角色定位"}
                },
                "required": ["character_type", "role"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "age": {"type": "integer"},
                    "appearance": {"type": "string"},
                    "personality": {"type": "string"},
                    "background": {"type": "string"},
                    "goals": {"type": "array"},
                    "abilities": {"type": "array"},
                    "flaws": {"type": "array"}
                }
            },
            priority=85
        )
        super().__init__(metadata)
    
    def _execute(self, **kwargs):
        character_type = kwargs.get("character_type", "男性")
        world_type = kwargs.get("world_type", "玄幻")
        role = kwargs.get("role", "主角")
        
        prompt = f"""请设计一个{world_type}世界中的{role}角色：

角色类型：{character_type}

要求包含：
1. 姓名（符合世界风格）
2. 年龄
3. 外貌特征
4. 性格特点
5. 背景故事
6. 目标与动机
7. 技能/能力
8. 缺点与弱点

请用JSON格式返回。"""
        
        result = self.engine.generate(prompt, system_prompt="你是一位专业的角色设计师，擅长创作立体的人物形象。")
        
        try:
            return json.loads(result)
        except:
            return {"name": "角色", "description": result}

class PlotDesignSkill(Skill):
    """情节设计Skill"""
    
    def __init__(self):
        metadata = SkillMetadata(
            skill_id="plot_design",
            name="剧情构造师",
            skill_type=SkillType.PLOT_DESIGN,
            description="设计紧凑有趣的故事情节",
            tags=["剧情", "情节", "故事", "大纲", "结构"],
            input_schema={
                "type": "object",
                "properties": {
                    "theme": {"type": "string", "description": "故事主题"},
                    "length": {"type": "integer", "description": "章节数"},
                    "genre": {"type": "string", "description": "小说类型"}
                },
                "required": ["theme", "length"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "summary": {"type": "string"},
                    "chapters": {"type": "array", "items": {"type": "object"}}
                }
            },
            priority=80
        )
        super().__init__(metadata)
    
    def _execute(self, **kwargs):
        theme = kwargs.get("theme", "冒险")
        length = kwargs.get("length", 10)
        genre = kwargs.get("genre", "玄幻")
        
        prompt = f"""请设计一个{genre}小说的情节大纲：

主题：{theme}
章节数：{length}章

要求：
1. 小说标题
2. 故事简介
3. {length}章的章节标题和内容提要
4. 包含起承转合
5. 有明确的高潮和结局

请用JSON格式返回。"""
        
        result = self.engine.generate(prompt, system_prompt="你是一位专业的情节设计师，擅长构建吸引人的故事结构。")
        
        try:
            return json.loads(result)
        except:
            return {"title": theme, "description": result}

class SceneDescriptionSkill(Skill):
    """场景描写Skill"""
    
    def __init__(self):
        metadata = SkillMetadata(
            skill_id="scene_description",
            name="场景构造师",
            skill_type=SkillType.SCENE_DESCRIPTION,
            description="创作生动的场景描写",
            tags=["场景", "环境", "描写", "氛围"],
            input_schema={
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "地点"},
                    "time": {"type": "string", "description": "时间"},
                    "characters": {"type": "array", "items": {"type": "string"}, "description": "人物"},
                    "mood": {"type": "string", "description": "氛围"}
                },
                "required": ["location", "time"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "description": {"type": "string"},
                    "atmosphere": {"type": "string"},
                    "key_elements": {"type": "array"}
                }
            },
            priority=75
        )
        super().__init__(metadata)
    
    def _execute(self, **kwargs):
        location = kwargs.get("location", "未知地点")
        time = kwargs.get("time", "某个时刻")
        characters = kwargs.get("characters", [])
        mood = kwargs.get("mood", "中性")
        
        char_str = ", ".join(characters) if characters else "无人"
        
        prompt = f"""请描写一个场景：

地点：{location}
时间：{time}
人物：{char_str}
氛围：{mood}

要求：
1. 环境描写细致生动
2. 包含感官细节（视觉、听觉、嗅觉等）
3. 营造{self._get_mood_description(mood)}的氛围
4. 不少于300字

请用小说风格写作。"""
        
        result = self.engine.generate(prompt, system_prompt="你是一位专业的场景描写师，擅长营造各种氛围。")
        
        return {"description": result, "atmosphere": mood, "key_elements": [location, time]}
    
    def _get_mood_description(self, mood: str) -> str:
        mood_map = {
            "紧张": "紧张压抑",
            "温馨": "温馨舒适",
            "恐怖": "阴森恐怖",
            "浪漫": "浪漫唯美",
            "神秘": "神秘诡异",
            "悲伤": "悲伤凄凉",
            "欢乐": "欢乐热闹",
            "中性": "平静自然"
        }
        return mood_map.get(mood, mood)

class DialogueWritingSkill(Skill):
    """对话写作Skill"""
    
    def __init__(self):
        metadata = SkillMetadata(
            skill_id="dialogue_writing",
            name="对话设计师",
            skill_type=SkillType.DIALOGUE_WRITING,
            description="创作生动的对话",
            tags=["对话", "台词", "人物对话"],
            input_schema={
                "type": "object",
                "properties": {
                    "characters": {"type": "array", "items": {"type": "string"}, "description": "人物列表"},
                    "topic": {"type": "string", "description": "对话主题"},
                    "emotion": {"type": "string", "description": "情绪"}
                },
                "required": ["characters", "topic"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "dialogue": {"type": "string"},
                    "character_voices": {"type": "array"}
                }
            },
            priority=70
        )
        super().__init__(metadata)
    
    def _execute(self, **kwargs):
        characters = kwargs.get("characters", ["人物A", "人物B"])
        topic = kwargs.get("topic", "日常对话")
        emotion = kwargs.get("emotion", "中性")
        
        prompt = f"""请创作一段对话：

人物：{', '.join(characters)}
话题：{topic}
情绪：{emotion}

要求：
1. 符合人物性格设定
2. 对话自然真实
3. 包含潜台词
4. 推动情节发展
5. 不少于5句对话

请用剧本格式写作。"""
        
        result = self.engine.generate(prompt, system_prompt="你是一位专业的对话作家，擅长创作生动有趣的对话。")
        
        return {"dialogue": result, "character_voices": characters}

class SkillManager:
    """Skill管理器"""
    
    def __init__(self):
        self.skills: Dict[str, Skill] = {}
        self.skill_types: Dict[SkillType, List[str]] = {}
        self.engine = None
    
    def set_engine(self, engine):
        """设置创作引擎"""
        self.engine = engine
        for skill in self.skills.values():
            skill.set_engine(engine)
    
    def register_skill(self, skill: Skill):
        """注册Skill"""
        if skill.metadata.enabled:
            self.skills[skill.metadata.skill_id] = skill
            skill.set_engine(self.engine)
            
            if skill.metadata.skill_type not in self.skill_types:
                self.skill_types[skill.metadata.skill_type] = []
            self.skill_types[skill.metadata.skill_type].append(skill.metadata.skill_id)
    
    def get_skill(self, skill_id: str) -> Optional[Skill]:
        """获取Skill"""
        return self.skills.get(skill_id)
    
    def get_skills_by_type(self, skill_type: SkillType) -> List[Skill]:
        """按类型获取Skill"""
        skill_ids = self.skill_types.get(skill_type, [])
        return [self.skills[sid] for sid in skill_ids]
    
    def find_matching_skills(self, query: str) -> List[Skill]:
        """查找匹配的Skill"""
        query_lower = query.lower()
        matches = []
        
        for skill in self.skills.values():
            if (query_lower in skill.metadata.name.lower() or
                query_lower in skill.metadata.description.lower() or
                any(query_lower in tag.lower() for tag in skill.metadata.tags)):
                matches.append(skill)
        
        matches.sort(key=lambda s: s.metadata.priority, reverse=True)
        return matches
    
    def execute_skill(self, skill_id: str, **kwargs) -> Dict[str, Any]:
        """执行Skill"""
        skill = self.get_skill(skill_id)
        if skill:
            return skill.execute(**kwargs)
        return {"error": f"Skill {skill_id} not found"}
    
    def execute_pipeline(self, skill_ids: List[str], context: Dict[str, Any]) -> Dict[str, Any]:
        """执行Skill流水线"""
        results = {}
        current_context = context.copy()
        
        for skill_id in skill_ids:
            skill = self.get_skill(skill_id)
            if skill:
                try:
                    result = skill.execute(**current_context)
                    results[skill_id] = result
                    current_context.update(result)
                except Exception as e:
                    results[skill_id] = {"error": str(e)}
        
        return {"results": results, "final_context": current_context}
    
    def get_skill_list(self) -> List[Dict[str, Any]]:
        """获取Skill列表"""
        return [skill.metadata.to_dict() for skill in self.skills.values()]

class SkillManagerBuilder:
    """Skill管理器构建器"""
    
    @staticmethod
    def create_default_manager() -> SkillManager:
        """创建默认Skill管理器"""
        manager = SkillManager()
        
        # 注册内置Skill
        manager.register_skill(WorldBuildingSkill())
        manager.register_skill(CharacterDesignSkill())
        manager.register_skill(PlotDesignSkill())
        manager.register_skill(SceneDescriptionSkill())
        manager.register_skill(DialogueWritingSkill())
        
        return manager

if __name__ == "__main__":
    print("="*60)
    print("🚀 NWACS V8.0 Skill管理器测试")
    print("="*60)
    
    from core.v8.engine.creative_engine import SmartCreativeEngine
    
    # 创建引擎和管理器
    engine = SmartCreativeEngine()
    skill_manager = SkillManagerBuilder.create_default_manager()
    skill_manager.set_engine(engine)
    
    print("\n1. 获取Skill列表...")
    skills = skill_manager.get_skill_list()
    print(f"✅ 已注册 {len(skills)} 个Skill")
    for skill in skills:
        print(f"   - {skill['name']} ({skill['skill_id']})")
    
    print("\n2. 测试世界观构造师...")
    result = skill_manager.execute_skill("world_building", world_type="玄幻")
    print("✅ 世界观构造完成")
    
    print("\n3. 测试角色塑造师...")
    result = skill_manager.execute_skill("character_design", character_type="男性", role="主角", world_type="玄幻")
    print("✅ 角色设计完成")
    
    print("\n4. 测试情节构造师...")
    result = skill_manager.execute_skill("plot_design", theme="废柴逆袭", length=5, genre="玄幻")
    print("✅ 情节设计完成")
    
    print("\n5. 测试场景构造师...")
    result = skill_manager.execute_skill("scene_description", location="青云宗", time="清晨", mood="庄严")
    print("✅ 场景描写完成")
    
    print("\n6. 测试对话设计师...")
    result = skill_manager.execute_skill("dialogue_writing", characters=["林动", "林琅天"], topic="比武挑战", emotion="紧张")
    print("✅ 对话创作完成")
    
    print("\n" + "="*60)
    print("🎉 Skill管理器测试完成！")
    print("="*60)
