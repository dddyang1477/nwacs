#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS V8.x 一体化写作协作引擎
集成所有V8模块，让NWACS成为真正的一体化写作工具
"""

import sys
import os
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class NWACSUnifiedEngine:
    """NWACS一体化引擎 - 整合所有V8模块与Skill系统"""

    def __init__(self):
        self.version = "9.0"
        print("="*70)
        print(f"🚀 NWACS V{self.version} 一体化写作协作引擎")
        print("="*70)

        # 模块容器
        self.modules = {}
        self.skills = {}
        self.workflows = {}
        self.session = {}

        # 初始化所有模块
        self._initialize_core_modules()
        self._initialize_skills()
        self._initialize_workflows()
        self._print_status()

    def _initialize_core_modules(self):
        """初始化V8核心模块"""
        print("\n📦 初始化核心模块...")

        # 1. 爆款分析器
        try:
            from bestseller_analyzer import BestsellerAnalyzer, HotspotType
            self.modules['bestseller_analyzer'] = BestsellerAnalyzer()
            print("   ✅ bestseller_analyzer 已加载")
        except Exception as e:
            print(f"   ⚠️ bestseller_analyzer 加载失败: {e}")
            self.modules['bestseller_analyzer'] = None

        # 2. 高级写作技巧
        try:
            from advanced_writing_techniques import AdvancedWritingTechniques, WritingSkill
            self.modules['writing_techniques'] = AdvancedWritingTechniques()
            print("   ✅ advanced_writing_techniques 已加载")
        except Exception as e:
            print(f"   ⚠️ advanced_writing_techniques 加载失败: {e}")
            self.modules['writing_techniques'] = None

        # 3. Skill适配器
        try:
            from skill_adapter import V8SkillAdapter, V8SelfLearner
            self.modules['skill_adapter'] = V8SkillAdapter()
            self.modules['self_learner'] = V8SelfLearner(self.modules['skill_adapter'])
            print("   ✅ skill_adapter 已加载")
        except Exception as e:
            print(f"   ⚠️ skill_adapter 加载失败: {e}")
            self.modules['skill_adapter'] = None
            self.modules['self_learner'] = None

        # 4. 专业提示词库
        try:
            from professional_prompt_library import ProfessionalPromptLibrary
            self.modules['prompt_library'] = ProfessionalPromptLibrary()
            print("   ✅ professional_prompt_library 已加载")
        except Exception as e:
            print(f"   ⚠️ professional_prompt_library 加载失败: {e}")
            self.modules['prompt_library'] = None

        # 5. 感官增强引擎
        try:
            from sensory_enhancement_engine import SensoryEnhancementEngine
            self.modules['sensory_engine'] = SensoryEnhancementEngine()
            print("   ✅ sensory_enhancement_engine 已加载")
        except Exception as e:
            print(f"   ⚠️ sensory_enhancement_engine 加载失败: {e}")
            self.modules['sensory_engine'] = None

        # 6. 向量记忆系统
        try:
            from vector_memory_system import VectorMemorySystem
            self.modules['vector_memory'] = VectorMemorySystem()
            print("   ✅ vector_memory_system 已加载")
        except Exception as e:
            print(f"   ⚠️ vector_memory_system 加载失败: {e}")
            self.modules['vector_memory'] = None

        # 7. AI漫剧创作模块
        try:
            from comic_drama_module import AIComicDramaModule
            self.modules['comic_drama'] = AIComicDramaModule()
            print("   ✅ comic_drama_module 已加载")
        except Exception as e:
            print(f"   ⚠️ comic_drama_module 加载失败: {e}")
            self.modules['comic_drama'] = None

    def _initialize_skills(self):
        """初始化可用的Skill"""
        print("\n🎯 注册写作技能...")

        self.skills = {
            # ========== 爆款分析类 ==========
            "爆款分析": {
                "id": "bestseller_analysis",
                "module": "bestseller_analyzer",
                "description": "分析10万+爆款小说，提取写作公式",
                "capabilities": ["套路识别", "公式提取", "趋势分析"],
                "icon": "📊"
            },
            "公众号爆款": {
                "id": "wechat_article",
                "module": "skill_adapter",
                "description": "生成10万+公众号爆款文章",
                "capabilities": ["标题优化", "开头钩子", "情感共鸣"],
                "icon": "📱"
            },

            # ========== 写作技巧类 ==========
            "悬念设置": {
                "id": "suspense",
                "module": "skill_adapter",
                "description": "设置悬念，吸引读者持续阅读",
                "capabilities": ["信息差", "伏笔埋设", "节奏控制"],
                "icon": "🔍"
            },
            "反转设计": {
                "id": "twist",
                "module": "skill_adapter",
                "description": "设计惊人反转，震撼读者",
                "capabilities": ["人设反转", "剧情反转", "结局反转"],
                "icon": "💥"
            },
            "群像叙事": {
                "id": "group_narrative",
                "module": "skill_adapter",
                "description": "多视角叙事，像《十日终焉》一样精彩",
                "capabilities": ["视角切换", "角色同步", "线索汇聚"],
                "icon": "👥"
            },
            "守护主题": {
                "id": "guard_theme",
                "module": "skill_adapter",
                "description": "打造《斩神》式守护主题",
                "capabilities": ["家国情怀", "个人守护", "情感升华"],
                "icon": "🛡️"
            },

            # ========== 世界观类 ==========
            "世界观构建": {
                "id": "world_building_v8",
                "module": "skill_adapter",
                "description": "构建《诡秘之主》式严谨世界观",
                "capabilities": ["体系设计", "势力设定", "规则制定"],
                "icon": "🌍"
            },
            "升级体系": {
                "id": "level_system",
                "module": "skill_adapter",
                "description": "设计清晰的等级体系和进阶路径",
                "capabilities": ["等级划分", "进阶规则", "境界命名", "能力差异"],
                "icon": "📈"
            },

            # ========== 增强类 ==========
            "感官增强": {
                "id": "sensory_enhance",
                "module": "sensory_engine",
                "description": "六感描写，让读者身临其境",
                "capabilities": ["视觉", "听觉", "嗅觉", "触觉", "味觉", "直觉"],
                "icon": "🎨"
            },
            "爽点设计": {
                "id": "cool_point",
                "module": "skill_adapter",
                "description": "设计密集且合理的爽点，让读者追更上头",
                "capabilities": ["先抑后扬", "打脸套路", "升级爽感", "期待感营造"],
                "icon": "🔥"
            },
            "金手指设计": {
                "id": "golden_finger",
                "module": "skill_adapter",
                "description": "设计有边界的金手指，让主角开挂但不无敌",
                "capabilities": ["系统流", "重生流", "特殊体质", "边界限制"],
                "icon": "✨"
            },
            "黄金三章": {
                "id": "golden_three",
                "module": "skill_adapter",
                "description": "开篇300字秒抓读者，黄金三章定生死",
                "capabilities": ["钩子开头", "金手指亮相", "悬念收尾"],
                "icon": "⭐"
            },

            # ========== 言情类 ==========
            "甜宠设计": {
                "id": "sweet_pet",
                "module": "skill_adapter",
                "description": "设计甜蜜宠溺的情节，细节让读者嗑糖",
                "capabilities": ["反差萌", "日常甜", "护妻/夫", "吃醋梗"],
                "icon": "🍬"
            },
            "情感线": {
                "id": "emotion_line",
                "module": "skill_adapter",
                "description": "设计感情发展节奏，双向奔赴或虐恋情深",
                "capabilities": ["双向暗恋", "追妻火葬场", "先婚后爱", "虐心误会"],
                "icon": "💗"
            },
            "人设塑造": {
                "id": "character_shaping",
                "module": "skill_adapter",
                "description": "塑造讨喜但不完美的人设，有成长有缺陷",
                "capabilities": ["反差设计", "成长轨迹", "小缺点", "独特魅力"],
                "icon": "🎭"
            },

            # ========== AI漫剧类 ==========
            "漫剧剧本创作": {
                "id": "comic_drama_script",
                "module": "comic_drama",
                "description": "将小说转换为AI漫剧剧本，生成分镜脚本",
                "capabilities": ["小说转剧本", "分镜设计", "镜头语言", "提示词生成"],
                "icon": "🎬"
            },
            "漫剧分镜生成": {
                "id": "comic_drama_storyboard",
                "module": "comic_drama",
                "description": "生成漫剧分镜脚本和AI绘图提示词",
                "capabilities": ["分镜设计", "镜头规划", "提示词生成", "格式导出"],
                "icon": "📖"
            }
        }

        for skill_name, skill_info in self.skills.items():
            print(f"   {skill_info['icon']} {skill_name}")

    def _initialize_workflows(self):
        """初始化写作工作流"""
        print("\n📋 注册写作工作流...")

        self.workflows = {
            "玄幻小说创作": {
                "steps": [
                    {"skill": "爆款分析", "action": "分析玄幻爆款"},
                    {"skill": "世界观构建", "action": "构建修炼体系"},
                    {"skill": "升级体系", "action": "设计等级进阶"},
                    {"skill": "黄金三章", "action": "设计钩子开头"},
                    {"skill": "金手指设计", "action": "设计有边界金手指"},
                    {"skill": "爽点设计", "action": "密集爽点节奏"},
                    {"skill": "守护主题", "action": "设定守护目标"},
                    {"skill": "感官增强", "action": "增强六感描写"}
                ],
                "description": "玄幻修仙小说完整创作流程（8步）"
            },
            "悬疑小说创作": {
                "steps": [
                    {"skill": "爆款分析", "action": "分析悬疑爆款"},
                    {"skill": "黄金三章", "action": "强悬疑开篇"},
                    {"skill": "悬念设置", "action": "三层真相洋葱结构"},
                    {"skill": "反转设计", "action": "真线索+假线索误导"},
                    {"skill": "人设塑造", "action": "半真半假人物"},
                    {"skill": "感官增强", "action": "营造紧张氛围"}
                ],
                "description": "悬疑推理小说完整创作流程（6步）"
            },
            "都市甜宠文": {
                "steps": [
                    {"skill": "爆款分析", "action": "分析甜宠爆款"},
                    {"skill": "人设塑造", "action": "霸总+独立女主"},
                    {"skill": "黄金三章", "action": "契约/一夜/重逢开局"},
                    {"skill": "甜宠设计", "action": "日常撒糖"},
                    {"skill": "情感线", "action": "双向奔赴"},
                    {"skill": "爽点设计", "action": "虐渣打脸"}
                ],
                "description": "现代都市甜宠文完整创作流程（6步）"
            },
            "都市虐恋文": {
                "steps": [
                    {"skill": "爆款分析", "action": "分析虐恋爆款"},
                    {"skill": "人设塑造", "action": "虐心人设设计"},
                    {"skill": "黄金三章", "action": "制造误会"},
                    {"skill": "情感线", "action": "相爱相杀"},
                    {"skill": "反转设计", "action": "追妻火葬场"},
                    {"skill": "甜宠设计", "action": "后期发糖"}
                ],
                "description": "现代都市虐恋文完整创作流程（6步）"
            },
            "重生复仇文": {
                "steps": [
                    {"skill": "爆款分析", "action": "分析复仇爆款"},
                    {"skill": "金手指设计", "action": "重生记忆"},
                    {"skill": "黄金三章", "action": "重生开局+复仇目标"},
                    {"skill": "爽点设计", "action": "层层打脸"},
                    {"skill": "人设塑造", "action": "从软弱到强大"},
                    {"skill": "情感线", "action": "弥补遗憾"}
                ],
                "description": "重生复仇爽文完整创作流程（6步）"
            },
            "公众号爆文": {
                "steps": [
                    {"skill": "公众号爆款", "action": "生成爆款标题"},
                    {"skill": "悬念设置", "action": "钩子开头"},
                    {"skill": "反转设计", "action": "中间反转"},
                    {"skill": "感官增强", "action": "情感共鸣收尾"}
                ],
                "description": "公众号10万+爆文创作流程（4步）"
            },
            "AI漫剧创作": {
                "steps": [
                    {"skill": "爆款分析", "action": "分析漫剧爆款"},
                    {"skill": "世界观构建", "action": "构建世界观"},
                    {"skill": "漫剧剧本创作", "action": "小说转剧本"},
                    {"skill": "漫剧分镜生成", "action": "生成分镜提示词"}
                ],
                "description": "AI漫剧完整创作流程（4步）"
            }
        }

        for workflow_name, workflow_info in self.workflows.items():
            print(f"   📝 {workflow_name} ({len(workflow_info['steps'])}步)")

    def _print_status(self):
        """打印系统状态"""
        loaded = sum(1 for m in self.modules.values() if m is not None)
        print(f"\n✅ 系统就绪：{loaded}/{len(self.modules)} 模块加载成功")
        print(f"✅ {len(self.skills)} 个写作技能可用")
        print(f"✅ {len(self.workflows)} 个工作流已注册")
        print("="*70)

    def execute_skill(self, skill_name: str, **kwargs) -> Dict[str, Any]:
        """执行单个Skill"""
        if skill_name not in self.skills:
            return {"status": "error", "message": f"Skill {skill_name} 不存在"}

        skill_info = self.skills[skill_name]
        print(f"\n🎯 执行技能: {skill_info['icon']} {skill_name}")

        try:
            if skill_info['module'] == 'skill_adapter':
                adapter = self.modules.get('skill_adapter')
                if adapter:
                    result = adapter.execute_skill(skill_info['id'], **kwargs)
                    return result
            elif skill_info['module'] == 'bestseller_analyzer':
                analyzer = self.modules.get('bestseller_analyzer')
                if analyzer:
                    result = analyzer.get_bestseller_recommendations(kwargs.get('genre', 'all'))
                    return {"status": "success", "result": result}
            elif skill_info['module'] == 'sensory_engine':
                engine = self.modules.get('sensory_engine')
                if engine:
                    text = kwargs.get('text', '')
                    result = engine.enhance_scene_description(text)
                    return {"status": "success", "result": result}
            elif skill_info['module'] == 'writing_techniques':
                tech = self.modules.get('writing_techniques')
                if tech:
                    result = tech.enhance_opening(kwargs.get('genre', '玄幻'))
                    return {"status": "success", "result": result}
            elif skill_info['module'] == 'comic_drama':
                comic = self.modules.get('comic_drama')
                if comic:
                    novel_text = kwargs.get('novel_text', '夜色降临，主角站在屋顶...')
                    episode_count = kwargs.get('episode_count', 5)
                    result = comic.novel_to_comic_script(novel_text, episode_count)
                    return {"status": "success", "result": result}

            return {"status": "error", "message": f"模块 {skill_info['module']} 未加载"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def run_workflow(self, workflow_name: str, **kwargs) -> Dict[str, Any]:
        """运行完整的写作工作流"""
        if workflow_name not in self.workflows:
            return {"status": "error", "message": f"工作流 {workflow_name} 不存在"}

        workflow = self.workflows[workflow_name]
        print(f"\n🚀 启动工作流: {workflow_name}")
        print("="*70)

        results = []
        start_time = time.time()

        for i, step in enumerate(workflow['steps'], 1):
            print(f"\n📌 步骤 {i}/{len(workflow['steps'])}: {step['skill']}")
            print(f"   行动: {step['action']}")

            result = self.execute_skill(step['skill'], **kwargs)
            results.append({
                "step": i,
                "skill": step['skill'],
                "action": step['action'],
                "result": result
            })

            if result.get('status') == 'success':
                print("   ✅ 执行成功")
            else:
                print(f"   ❌ 执行失败: {result.get('message')}")

        total_time = time.time() - start_time

        return {
            "status": "success",
            "workflow": workflow_name,
            "total_steps": len(workflow['steps']),
            "total_time": round(total_time, 2),
            "results": results
        }

    def list_skills(self) -> List[Dict[str, Any]]:
        """列出所有可用的Skill"""
        skills_list = []
        for name, info in self.skills.items():
            skills_list.append({
                "name": name,
                "icon": info['icon'],
                "description": info['description'],
                "capabilities": info['capabilities']
            })
        return skills_list

    def list_workflows(self) -> List[Dict[str, Any]]:
        """列出所有可用的工作流"""
        workflows_list = []
        for name, info in self.workflows.items():
            workflows_list.append({
                "name": name,
                "description": info['description'],
                "steps": len(info['steps'])
            })
        return workflows_list

    def get_help(self) -> str:
        """获取帮助信息"""
        help_text = """
╔══════════════════════════════════════════════════════════════╗
║               NWACS 一体化引擎 使用帮助                        ║
╠══════════════════════════════════════════════════════════════╣
║                                                               ║
║  1. 查看技能列表: engine.list_skills()                       ║
║  2. 查看工作流: engine.list_workflows()                       ║
║  3. 执行单个技能: engine.execute_skill(skill_name, **kwargs)  ║
║  4. 运行工作流: engine.run_workflow(workflow_name, **kwargs)  ║
║                                                               ║
║  示例:                                                       ║
║    - 分析玄幻爆款: engine.execute_skill("爆款分析", genre="玄幻")║
║    - 设计悬念反转: engine.execute_skill("反转设计", ...)     ║
║    - 运行玄幻创作: engine.run_workflow("玄幻小说创作")         ║
║                                                               ║
╚══════════════════════════════════════════════════════════════╝
        """
        return help_text


def main():
    """演示NWACS一体化引擎"""
    engine = NWACSUnifiedEngine()

    # 打印帮助
    print(engine.get_help())

    # 示例1: 列出技能
    print("\n📋 可用技能:")
    for skill in engine.list_skills():
        print(f"   {skill['icon']} {skill['name']}: {skill['description']}")

    # 示例2: 列出工作流
    print("\n📁 可用工作流:")
    for workflow in engine.list_workflows():
        print(f"   📝 {workflow['name']}: {workflow['description']}")

    # 示例3: 执行单个技能
    print("\n" + "="*70)
    print("🎯 示例1: 执行单个技能 - 爆款分析")
    print("="*70)
    result = engine.execute_skill("爆款分析", genre="玄幻")
    if result.get('status') == 'success' and result.get('result'):
        print(result['result'][:500] + "..." if len(str(result['result'])) > 500 else result['result'])

    # 示例4: 执行公众号爆款技能
    print("\n" + "="*70)
    print("📱 示例2: 公众号爆款写作")
    print("="*70)
    result = engine.execute_skill("公众号爆款", content_type="emotion")
    if result.get('status') == 'success' and result.get('result'):
        print(result['result'][:600] + "..." if len(str(result['result'])) > 600 else result['result'])

    print("\n" + "="*70)
    print("🎉 NWACS一体化引擎演示完成！")
    print("💡 提示: 调用 run_workflow() 来运行完整写作流程")
    print("="*70)


if __name__ == "__main__":
    main()
