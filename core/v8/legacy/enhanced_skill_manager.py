#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 增强Skill管理器 - EnhancedSkillManager
核心功能：
1. 统一注册 - 所有Skill的注册/发现/索引
2. 生命周期 - Skill的加载/激活/休眠/卸载
3. 优先级调度 - 基于优先级的Skill调度
4. 组合编排 - 多个Skill组合成工作流
5. 热更新 - 运行时动态加载新Skill
6. 依赖解析 - 自动解析Skill间依赖关系

设计原则：
- 每个Skill是独立的功能单元
- Skill间通过管理器通信，不直接依赖
- 支持Skill的热插拔
"""

import os
import json
import importlib
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum


class SkillStatus(Enum):
    """Skill状态"""
    REGISTERED = "已注册"
    LOADED = "已加载"
    ACTIVE = "活跃"
    PAUSED = "已暂停"
    ERROR = "错误"


class SkillPriority(Enum):
    """Skill优先级"""
    CRITICAL = 0
    HIGH = 1
    MEDIUM = 2
    LOW = 3
    OPTIONAL = 4


@dataclass
class SkillMeta:
    """Skill元数据"""
    name: str
    version: str
    description: str
    author: str = "NWACS"
    category: str = "general"
    priority: SkillPriority = SkillPriority.MEDIUM
    dependencies: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    config: Dict = field(default_factory=dict)


@dataclass
class SkillInfo:
    """Skill完整信息"""
    meta: SkillMeta
    status: SkillStatus = SkillStatus.REGISTERED
    handler: Optional[Callable] = None
    instance: Any = None
    call_count: int = 0
    last_result: Any = None
    error_count: int = 0


class SkillWorkflow:
    """Skill工作流 - 多个Skill的组合编排"""

    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.steps: List[Dict] = []

    def add_step(self, skill_name: str, input_map: Dict = None,
                 condition: Callable = None):
        self.steps.append({
            "skill": skill_name,
            "input_map": input_map or {},
            "condition": condition,
        })

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "description": self.description,
            "steps": [
                {"skill": s["skill"], "input_map": s["input_map"]}
                for s in self.steps
            ],
        }


class EnhancedSkillManager:
    """增强Skill管理器"""

    def __init__(self, engine=None):
        self.skills: Dict[str, SkillInfo] = {}
        self.workflows: Dict[str, SkillWorkflow] = {}
        self.engine = engine
        self.skill_dir = os.path.dirname(os.path.abspath(__file__))

        self._register_builtin_skills()
        self._register_builtin_workflows()

    def _register_builtin_skills(self):
        """注册内置Skill"""
        builtins = [
            SkillMeta(
                name="character_creation",
                version="2.0",
                description="角色创建Skill - 生成完整角色设定",
                category="character",
                priority=SkillPriority.HIGH,
                tags=["角色", "创建", "设定"],
            ),
            SkillMeta(
                name="plot_generation",
                version="2.0",
                description="剧情生成Skill - 生成剧情构思和大纲",
                category="plot",
                priority=SkillPriority.HIGH,
                tags=["剧情", "构思", "大纲"],
            ),
            SkillMeta(
                name="ai_detection",
                version="2.0",
                description="AI检测Skill - 检测文本AI痕迹",
                category="quality",
                priority=SkillPriority.MEDIUM,
                tags=["检测", "AI", "质量"],
            ),
            SkillMeta(
                name="text_rewrite",
                version="2.0",
                description="文本去痕Skill - 去除AI痕迹",
                category="quality",
                priority=SkillPriority.MEDIUM,
                tags=["去痕", "改写", "质量"],
            ),
            SkillMeta(
                name="world_building",
                version="1.5",
                description="世界观构建Skill - 构建完整世界观",
                category="world",
                priority=SkillPriority.MEDIUM,
                tags=["世界观", "设定", "构建"],
            ),
            SkillMeta(
                name="dialogue_enhance",
                version="1.5",
                description="对话增强Skill - 优化角色对话",
                category="writing",
                priority=SkillPriority.LOW,
                tags=["对话", "优化", "写作"],
            ),
            SkillMeta(
                name="chapter_outline",
                version="2.0",
                description="章节大纲Skill - 生成逐章大纲",
                category="plot",
                priority=SkillPriority.HIGH,
                tags=["大纲", "章节", "规划"],
            ),
            SkillMeta(
                name="style_transfer",
                version="1.0",
                description="风格迁移Skill - 转换写作风格",
                category="writing",
                priority=SkillPriority.LOW,
                tags=["风格", "转换", "写作"],
            ),
            SkillMeta(
                name="conflict_design",
                version="1.5",
                description="冲突设计Skill - 设计角色冲突矩阵",
                category="plot",
                priority=SkillPriority.MEDIUM,
                tags=["冲突", "设计", "剧情"],
            ),
            SkillMeta(
                name="foreshadowing",
                version="1.0",
                description="伏笔管理Skill - 埋设和回收伏笔",
                category="plot",
                priority=SkillPriority.LOW,
                tags=["伏笔", "管理", "剧情"],
            ),
        ]

        for meta in builtins:
            self.skills[meta.name] = SkillInfo(meta=meta)

    def _register_builtin_workflows(self):
        """注册内置工作流"""
        wf = SkillWorkflow("full_chapter", "完整章节生成工作流")
        wf.add_step("character_creation")
        wf.add_step("plot_generation")
        wf.add_step("chapter_outline")
        wf.add_step("ai_detection")
        wf.add_step("text_rewrite")
        self.workflows["full_chapter"] = wf

        wf2 = SkillWorkflow("character_pack", "角色包生成工作流")
        wf2.add_step("character_creation")
        wf2.add_step("dialogue_enhance")
        self.workflows["character_pack"] = wf2

        wf3 = SkillWorkflow("world_pack", "世界观构建工作流")
        wf3.add_step("world_building")
        wf3.add_step("conflict_design")
        self.workflows["world_pack"] = wf3

    def register_skill(self, meta: SkillMeta, handler: Callable = None) -> bool:
        """注册新Skill"""
        if meta.name in self.skills:
            print(f"  ⚠️ Skill已存在: {meta.name}")
            return False

        self.skills[meta.name] = SkillInfo(meta=meta, handler=handler)
        return True

    def unregister_skill(self, name: str) -> bool:
        """注销Skill"""
        if name not in self.skills:
            return False

        info = self.skills[name]
        if info.status == SkillStatus.ACTIVE:
            self.deactivate_skill(name)

        del self.skills[name]
        return True

    def activate_skill(self, name: str) -> bool:
        """激活Skill"""
        if name not in self.skills:
            return False

        info = self.skills[name]

        for dep in info.meta.dependencies:
            if dep not in self.skills:
                print(f"  ❌ 依赖Skill不存在: {dep}")
                return False
            if self.skills[dep].status != SkillStatus.ACTIVE:
                self.activate_skill(dep)

        info.status = SkillStatus.ACTIVE
        return True

    def deactivate_skill(self, name: str) -> bool:
        """停用Skill"""
        if name not in self.skills:
            return False

        dependents = [
            n for n, s in self.skills.items()
            if name in s.meta.dependencies and s.status == SkillStatus.ACTIVE
        ]
        if dependents:
            print(f"  ⚠️ 以下Skill依赖{name}: {dependents}")
            return False

        self.skills[name].status = SkillStatus.PAUSED
        return True

    def execute_skill(self, name: str, **inputs) -> Dict[str, Any]:
        """执行Skill"""
        if name not in self.skills:
            return {"success": False, "error": f"Skill不存在: {name}"}

        info = self.skills[name]

        if info.status != SkillStatus.ACTIVE:
            if not self.activate_skill(name):
                return {"success": False, "error": f"Skill激活失败: {name}"}

        try:
            result = self._dispatch_skill(name, inputs)
            info.call_count += 1
            info.last_result = result
            return {"success": True, "data": result}
        except Exception as e:
            info.error_count += 1
            info.status = SkillStatus.ERROR
            return {"success": False, "error": str(e)}

    def _dispatch_skill(self, name: str, inputs: Dict) -> Any:
        """分发Skill执行"""
        if name == "character_creation":
            return self._skill_character_creation(inputs)

        elif name == "plot_generation":
            return self._skill_plot_generation(inputs)

        elif name == "ai_detection":
            return self._skill_ai_detection(inputs)

        elif name == "text_rewrite":
            return self._skill_text_rewrite(inputs)

        elif name == "world_building":
            return self._skill_world_building(inputs)

        elif name == "dialogue_enhance":
            return self._skill_dialogue_enhance(inputs)

        elif name == "chapter_outline":
            return self._skill_chapter_outline(inputs)

        elif name == "style_transfer":
            return self._skill_style_transfer(inputs)

        elif name == "conflict_design":
            return self._skill_conflict_design(inputs)

        elif name == "foreshadowing":
            return self._skill_foreshadowing(inputs)

        return {"message": f"Skill {name} 无具体实现"}

    def _skill_character_creation(self, inputs: Dict) -> Dict:
        genre = inputs.get("genre", "xuanhuan")
        gender = inputs.get("gender", "male")
        role = inputs.get("role", "主角")

        try:
            from character_name_generator import CharacterNameGenerator
            gen = CharacterNameGenerator()
            return gen.generate_full_character_name(genre, gender)
        except ImportError:
            return {"full_name": f"{genre}_{role}", "meaning": "默认角色"}

    def _skill_plot_generation(self, inputs: Dict) -> Dict:
        try:
            from plot_brainstorm_engine import PlotBrainstormEngine
            engine = PlotBrainstormEngine()
            ideas = engine.brainstorm_ideas(
                inputs.get("genre", "玄幻"),
                inputs.get("theme", ""),
                inputs.get("count", 3),
            )
            return {"ideas": ideas}
        except ImportError:
            return {"ideas": []}

    def _skill_ai_detection(self, inputs: Dict) -> Dict:
        text = inputs.get("text", "")
        try:
            from enhanced_ai_detector import EnhancedAIDetector
            detector = EnhancedAIDetector()
            report = detector.detect(text)
            return {"score": report.overall_score, "level": report.level}
        except ImportError:
            try:
                from ai_detector_and_rewriter import AIDetectorAndRewriter
                detector = AIDetectorAndRewriter()
                return {"score": detector.detect_ai_score(text)}
            except ImportError:
                return {"score": 0}

    def _skill_text_rewrite(self, inputs: Dict) -> Dict:
        text = inputs.get("text", "")
        intensity = inputs.get("intensity", "medium")
        try:
            from enhanced_ai_detector import EnhancedAIDetector
            detector = EnhancedAIDetector()
            rewritten, report = detector.rewrite(text, intensity)
            return {
                "rewritten": rewritten,
                "original_score": report.original_score,
                "final_score": report.final_score,
            }
        except ImportError:
            return {"rewritten": text}

    def _skill_world_building(self, inputs: Dict) -> Dict:
        return {
            "world_name": inputs.get("name", "未命名世界"),
            "elements": ["地理", "历史", "势力", "规则", "文化"],
            "status": "基础框架已生成",
        }

    def _skill_dialogue_enhance(self, inputs: Dict) -> Dict:
        return {"message": "对话增强Skill - 需要AI引擎支持"}

    def _skill_chapter_outline(self, inputs: Dict) -> Dict:
        try:
            from plot_brainstorm_engine import PlotBrainstormEngine, PlotArcType
            engine = PlotBrainstormEngine()
            arc = engine.design_plot_arc(
                PlotArcType.THREE_ACT,
                inputs.get("chapters", 30),
                inputs.get("genre", "玄幻"),
            )
            outline = engine.generate_chapter_outline(arc)
            return {"outline": outline}
        except ImportError:
            return {"outline": []}

    def _skill_style_transfer(self, inputs: Dict) -> Dict:
        return {"message": "风格迁移Skill - 需要AI引擎支持"}

    def _skill_conflict_design(self, inputs: Dict) -> Dict:
        characters = inputs.get("characters", ["主角", "反派", "配角"])
        try:
            from plot_brainstorm_engine import PlotBrainstormEngine
            engine = PlotBrainstormEngine()
            matrix = engine.design_conflict_matrix(characters)
            return {"conflict_matrix": matrix}
        except ImportError:
            return {"conflict_matrix": {}}

    def _skill_foreshadowing(self, inputs: Dict) -> Dict:
        return {
            "active_foreshadowing": [],
            "resolved_foreshadowing": [],
            "message": "伏笔管理Skill已就绪",
        }

    def execute_workflow(self, workflow_name: str, **inputs) -> Dict[str, Any]:
        """执行工作流"""
        if workflow_name not in self.workflows:
            return {"success": False, "error": f"工作流不存在: {workflow_name}"}

        wf = self.workflows[workflow_name]
        results = {}
        context = {**inputs}

        for step in wf.steps:
            skill_name = step["skill"]
            input_map = step["input_map"]
            condition = step.get("condition")

            if condition and not condition(context):
                continue

            step_inputs = {}
            for target_key, source_key in input_map.items():
                step_inputs[target_key] = context.get(source_key)
            step_inputs.update({k: v for k, v in context.items() if k not in step_inputs})

            result = self.execute_skill(skill_name, **step_inputs)
            results[skill_name] = result

            if result["success"]:
                context[f"_{skill_name}_result"] = result["data"]

        return {
            "success": True,
            "workflow": workflow_name,
            "steps": results,
            "context": {k: v for k, v in context.items() if not k.startswith("_")},
        }

    def list_skills(self, category: str = None, status: SkillStatus = None) -> List[Dict]:
        """列出Skill"""
        result = []
        for name, info in self.skills.items():
            if category and info.meta.category != category:
                continue
            if status and info.status != status:
                continue
            result.append({
                "name": name,
                "version": info.meta.version,
                "description": info.meta.description,
                "category": info.meta.category,
                "status": info.status.value,
                "priority": info.meta.priority.name,
                "calls": info.call_count,
            })
        return result

    def list_workflows(self) -> List[Dict]:
        """列出工作流"""
        return [wf.to_dict() for wf in self.workflows.values()]

    def get_skill_report(self) -> Dict:
        """获取Skill运行报告"""
        total = len(self.skills)
        active = sum(1 for s in self.skills.values() if s.status == SkillStatus.ACTIVE)
        errors = sum(1 for s in self.skills.values() if s.status == SkillStatus.ERROR)
        total_calls = sum(s.call_count for s in self.skills.values())
        total_errors = sum(s.error_count for s in self.skills.values())

        return {
            "total_skills": total,
            "active_skills": active,
            "error_skills": errors,
            "total_calls": total_calls,
            "total_errors": total_errors,
            "workflows": len(self.workflows),
        }


if __name__ == "__main__":
    print("=" * 60)
    print("⚙️ 增强Skill管理器测试")
    print("=" * 60)

    manager = EnhancedSkillManager()

    print("\n【Skill列表】")
    for skill in manager.list_skills():
        print(f"  {skill['name']} v{skill['version']} [{skill['category']}] - {skill['status']}")

    print("\n【工作流列表】")
    for wf in manager.list_workflows():
        print(f"  {wf['name']}: {' → '.join(s['skill'] for s in wf['steps'])}")

    print("\n【执行角色创建Skill】")
    result = manager.execute_skill("character_creation", genre="xuanhuan", gender="male")
    if result["success"]:
        print(f"  {json.dumps(result['data'], ensure_ascii=False, indent=2)}")

    print("\n【执行AI检测Skill】")
    result = manager.execute_skill("ai_detection", text="林晨缓缓地站起身，宛如一只蝴蝶。")
    if result["success"]:
        print(f"  AI分数: {result['data']['score']}/100 ({result['data']['level']})")

    print("\n【执行冲突设计Skill】")
    result = manager.execute_skill("conflict_design", characters=["叶青云", "魔尊", "剑圣", "苏婉儿"])
    if result["success"]:
        matrix = result["data"].get("conflict_matrix", {})
        for a, conflicts in matrix.items():
            for b, c in conflicts.items():
                print(f"  {a} ↔ {b}: {c[:50]}...")

    print("\n【Skill运行报告】")
    report = manager.get_skill_report()
    print(f"  总Skill: {report['total_skills']}")
    print(f"  活跃: {report['active_skills']}")
    print(f"  总调用: {report['total_calls']}")
    print(f"  工作流: {report['workflows']}")
