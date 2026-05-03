#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS V8.0 Skill适配器
将V8核心模块（bestseller_analyzer, advanced_writing_techniques）接入Skill系统
支持写作时调用爆款分析、写作技巧、自我学习更新
"""

import sys
import os
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from bestseller_analyzer import BestsellerAnalyzer, HotspotType
    from advanced_writing_techniques import AdvancedWritingTechniques, WritingSkill
    V8_MODULES_AVAILABLE = True
except ImportError as e:
    V8_MODULES_AVAILABLE = False
    print(f"⚠️ V8模块导入失败: {e}")


class V8SkillAdapter:
    """V8模块Skill适配器"""

    def __init__(self):
        self.analyzer = None
        self.techniques = None
        self.learning_enabled = True
        self.last_update = None
        self.update_interval = 3600

        if V8_MODULES_AVAILABLE:
            self._init_v8_modules()
        else:
            print("❌ V8模块不可用")

    def _init_v8_modules(self):
        """初始化V8模块"""
        try:
            self.analyzer = BestsellerAnalyzer()
            self.techniques = AdvancedWritingTechniques()
            print("✅ V8模块初始化成功")
            print(f"   • 爆款分析器: {len(self.analyzer.formulas)} 个写作公式")
            print(f"   • 写作技巧: {len(self.techniques.skills)} 个技能")
        except Exception as e:
            print(f"❌ V8模块初始化失败: {e}")
            self.learning_enabled = False

    def get_skill_registry(self) -> Dict[str, Any]:
        """获取Skill注册表"""
        if not V8_MODULES_AVAILABLE:
            return {}

        skills = {}

        for skill_type in WritingSkill:
            skills[skill_type.value] = {
                "name": self.techniques.skills[skill_type].name if skill_type in self.techniques.skills else skill_type.value,
                "type": "writing_technique",
                "enabled": True,
                "description": self.techniques.skills[skill_type].description if skill_type in self.techniques.skills else ""
            }

        skills["bestseller_analysis"] = {
            "name": "爆款分析",
            "type": "analysis",
            "enabled": True,
            "description": "分析爆款小说结构、提取写作公式"
        }

        skills["suspense_twist"] = {
            "name": "悬念反转",
            "type": "writing_technique",
            "enabled": True,
            "description": "知乎盐言故事式悬念反转技巧"
        }

        skills["wechat_article"] = {
            "name": "公众号爆款",
            "type": "content_creation",
            "enabled": True,
            "description": "10万+爆款文章写作公式"
        }

        skills["group_narrative"] = {
            "name": "群像叙事",
            "type": "writing_technique",
            "enabled": True,
            "description": "十日终焉式多视角叙事"
        }

        skills["world_building_v8"] = {
            "name": "世界观构建",
            "type": "writing_technique",
            "enabled": True,
            "description": "诡秘之主式严谨世界观"
        }

        skills["guard_theme"] = {
            "name": "守护主题",
            "type": "writing_technique",
            "enabled": True,
            "description": "斩神式家国情怀守护主题"
        }

        return skills

    def execute_skill(self, skill_name: str, **kwargs) -> Dict[str, Any]:
        """执行Skill"""
        if not V8_MODULES_AVAILABLE:
            return {"status": "error", "message": "V8模块不可用"}

        try:
            if skill_name == "bestseller_analysis":
                return self._execute_bestseller_analysis(**kwargs)
            elif skill_name in ["suspense", "twist", "suspense_twist"]:
                return self._execute_suspense_twist(**kwargs)
            elif skill_name == "wechat_article":
                return self._execute_wechat_article(**kwargs)
            elif skill_name in ["group_narrative", "group_narrative"]:
                return self._execute_group_narrative(**kwargs)
            elif skill_name == "world_building_v8":
                return self._execute_world_building(**kwargs)
            elif skill_name == "guard_theme":
                return self._execute_guard_theme(**kwargs)
            elif skill_name in [s.value for s in WritingSkill]:
                return self._execute_writing_skill(skill_name, **kwargs)
            else:
                return {"status": "error", "message": f"未知Skill: {skill_name}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def _execute_bestseller_analysis(self, **kwargs) -> Dict[str, Any]:
        """执行爆款分析"""
        genre = kwargs.get("genre", "all")
        return {
            "status": "success",
            "result": self.analyzer.get_bestseller_recommendations(genre)
        }

    def _execute_suspense_twist(self, **kwargs) -> Dict[str, Any]:
        """执行悬念反转技巧"""
        setup = kwargs.get("setup", "")
        misdirection = kwargs.get("misdirection", "")
        revelation = kwargs.get("revelation", "")

        result = self.techniques.enhance_twist(setup, misdirection, revelation)
        return {
            "status": "success",
            "result": result
        }

    def _execute_wechat_article(self, **kwargs) -> Dict[str, Any]:
        """执行公众号爆款文章"""
        content_type = kwargs.get("content_type", "emotion")
        result = self.techniques.enhance_wechat_article(content_type)
        return {
            "status": "success",
            "result": result
        }

    def _execute_group_narrative(self, **kwargs) -> Dict[str, Any]:
        """执行群像叙事"""
        characters = kwargs.get("characters", ["主角1", "主角2"])
        scenes = kwargs.get("scenes", ["场景1", "场景2"])
        result = self.techniques.enhance_group_narrative(characters, scenes)
        return {
            "status": "success",
            "result": result
        }

    def _execute_world_building(self, **kwargs) -> Dict[str, Any]:
        """执行世界观构建"""
        core_concept = kwargs.get("core_concept", "")
        rule_system = kwargs.get("rule_system", "")
        specific = kwargs.get("specific_manifestation", "")
        result = self.techniques.enhance_world_building(core_concept, rule_system, specific)
        return {
            "status": "success",
            "result": result
        }

    def _execute_guard_theme(self, **kwargs) -> Dict[str, Any]:
        """执行守护主题"""
        character = kwargs.get("character", "主角")
        what_to_guard = kwargs.get("what_to_guard", "家园")
        threat = kwargs.get("threat", "敌人")
        result = self.techniques.enhance_guard_theme(character, what_to_guard, threat)
        return {
            "status": "success",
            "result": result
        }

    def _execute_writing_skill(self, skill_name: str, **kwargs) -> Dict[str, Any]:
        """执行通用写作技巧"""
        skill = WritingSkill(skill_name)
        if skill not in self.techniques.skills:
            return {"status": "error", "message": f"Skill {skill_name} 未找到"}

        templates = self.techniques.skills[skill].templates
        examples = self.techniques.skills[skill].examples

        return {
            "status": "success",
            "name": self.techniques.skills[skill].name,
            "description": self.techniques.skills[skill].description,
            "templates": templates,
            "examples": examples
        }

    def check_for_updates(self) -> bool:
        """检查更新"""
        current_time = time.time()
        if self.last_update and (current_time - self.last_update) < self.update_interval:
            return False

        self.last_update = current_time
        return True

    def get_system_status(self) -> Dict[str, Any]:
        """获取系统状态"""
        return {
            "v8_modules_available": V8_MODULES_AVAILABLE,
            "analyzer_initialized": self.analyzer is not None,
            "techniques_initialized": self.techniques is not None,
            "skill_count": len(self.get_skill_registry()),
            "learning_enabled": self.learning_enabled,
            "last_update": self.last_update
        }


class V8SelfLearner:
    """V8模块自我学习器"""

    def __init__(self, adapter: V8SkillAdapter):
        self.adapter = adapter
        self.learned_topics = []
        self.learning_history = []

    def learn_from_result(self, skill_name: str, params: Dict, result: Any, rating: float):
        """从使用结果中学习"""
        learning_entry = {
            "timestamp": datetime.now().isoformat(),
            "skill_name": skill_name,
            "params": params,
            "rating": rating,
            "feedback": self._extract_feedback(result, rating)
        }
        self.learning_history.append(learning_entry)

        if rating >= 4.0:
            self.learned_topics.append({
                "topic": params.get("topic", "general"),
                "skill": skill_name,
                "count": 1
            })

    def _extract_feedback(self, result: Any, rating: float) -> str:
        """提取反馈"""
        if rating >= 4.5:
            return "优秀"
        elif rating >= 4.0:
            return "良好"
        elif rating >= 3.0:
            return "一般"
        else:
            return "需改进"

    def get_learning_stats(self) -> Dict[str, Any]:
        """获取学习统计"""
        total = len(self.learning_history)
        if total == 0:
            return {"total_learnings": 0}

        ratings = [h["rating"] for h in self.learning_history]
        avg_rating = sum(ratings) / total

        return {
            "total_learnings": total,
            "average_rating": round(avg_rating, 2),
            "learned_topics_count": len(self.learned_topics),
            "excellent_count": len([r for r in ratings if r >= 4.5]),
            "good_count": len([r for r in ratings if 4.0 <= r < 4.5])
        }


def main():
    print("="*60)
    print("🔧 NWACS V8.0 Skill适配器测试")
    print("="*60)

    adapter = V8SkillAdapter()

    status = adapter.get_system_status()
    print("\n📊 系统状态:")
    for key, value in status.items():
        print(f"  • {key}: {value}")

    print("\n📋 Skill注册表:")
    registry = adapter.get_skill_registry()
    for skill_id, info in registry.items():
        print(f"  • [{info['type']}] {info['name']}: {info['description']}")

    print("\n🧪 技能测试:")

    print("\n1. 测试爆款分析:")
    result = adapter.execute_skill("bestseller_analysis", genre="玄幻")
    if result["status"] == "success":
        print("   ✅ 爆款分析执行成功")

    print("\n2. 测试悬念反转:")
    result = adapter.execute_skill("suspense_twist",
                                   setup="他以为自己是赢家",
                                   misdirection="所有证据都指向另一个人",
                                   revelation="真正的幕后黑手竟然是他最信任的人")
    if result["status"] == "success":
        print("   ✅ 悬念反转执行成功")

    print("\n3. 测试公众号爆款:")
    result = adapter.execute_skill("wechat_article", content_type="emotion")
    if result["status"] == "success":
        print("   ✅ 公众号爆款执行成功")

    print("\n4. 测试群像叙事:")
    result = adapter.execute_skill("group_narrative",
                                   characters=["林七夜", "赵空城"],
                                   scenes=["林七夜面对众神", "赵空城的抉择"])
    if result["status"] == "success":
        print("   ✅ 群像叙事执行成功")

    print("\n5. 测试守护主题:")
    result = adapter.execute_skill("guard_theme",
                                   character="林七夜",
                                   what_to_guard="大夏",
                                   threat="神明")
    if result["status"] == "success":
        print("   ✅ 守护主题执行成功")

    print("\n" + "="*60)
    print("✅ V8 Skill适配器测试完成")
    print("="*60)


if __name__ == "__main__":
    main()
