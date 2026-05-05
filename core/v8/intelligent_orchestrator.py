#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 智能编排层 - IntelligentOrchestrator
核心功能：
1. 统一入口 - 所有功能的统一调度中心
2. 智能路由 - 根据用户意图自动选择合适的模块
3. 模块注册 - 动态注册/卸载功能模块
4. 状态管理 - 全局状态追踪与同步
5. 事件总线 - 模块间松耦合通信
6. 性能监控 - 各模块调用耗时统计

设计原则：
- 编排层不执行业务逻辑，只做调度
- 模块间通过事件总线通信，不直接依赖
- 所有模块懒加载，按需激活
"""

import time
import json
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum


class ModuleStatus(Enum):
    """模块状态"""
    UNLOADED = "未加载"
    LOADED = "已加载"
    ACTIVE = "活跃中"
    ERROR = "错误"


@dataclass
class ModuleInfo:
    """模块信息"""
    name: str
    description: str
    status: ModuleStatus = ModuleStatus.UNLOADED
    instance: Any = None
    call_count: int = 0
    total_time_ms: float = 0
    last_error: str = ""
    dependencies: List[str] = field(default_factory=list)


class EventBus:
    """事件总线 - 模块间松耦合通信"""

    def __init__(self):
        self._listeners: Dict[str, List[Callable]] = {}

    def on(self, event: str, callback: Callable):
        if event not in self._listeners:
            self._listeners[event] = []
        self._listeners[event].append(callback)

    def emit(self, event: str, **data):
        for callback in self._listeners.get(event, []):
            try:
                callback(data)
            except Exception as e:
                print(f"  ⚠️ 事件处理失败 [{event}]: {e}")

    def clear(self):
        self._listeners.clear()


class IntelligentOrchestrator:
    """智能编排器"""

    def __init__(self):
        self.modules: Dict[str, ModuleInfo] = {}
        self.events = EventBus()
        self.global_state: Dict[str, Any] = {
            "session_start": datetime.now().isoformat(),
            "active_novel": None,
            "current_chapter": 0,
            "total_api_calls": 0,
            "total_tokens_used": 0,
        }
        self.command_history: List[Dict] = []

        self._register_builtin_modules()

    def _register_builtin_modules(self):
        """注册内置模块"""
        builtins = [
            ("novel_memory", "长篇小说记忆一致性验证系统", []),
            ("namer", "中国传统命名系统(五行八卦风水)", []),
            ("plotter", "剧情构思引擎", ["novel_memory"]),
            ("detector", "AI检测器(基础)", []),
            ("enhanced_detector", "AI检测器(增强)", []),
            ("engine", "创作引擎(DeepSeek)", []),
            ("learning_engine", "自学习进化引擎", []),
            ("pipeline", "写作协作流水线", ["novel_memory", "engine", "plotter", "detector"]),
            ("skill_manager", "Skill管理器", ["engine"]),
        ]

        for name, desc, deps in builtins:
            self.modules[name] = ModuleInfo(
                name=name, description=desc, dependencies=deps
            )

    def load_module(self, name: str) -> bool:
        """加载模块"""
        if name not in self.modules:
            print(f"  ❌ 未知模块: {name}")
            return False

        info = self.modules[name]
        if info.status == ModuleStatus.ACTIVE:
            return True

        for dep in info.dependencies:
            if not self.load_module(dep):
                print(f"  ❌ 依赖模块加载失败: {dep}")
                return False

        try:
            instance = self._create_module_instance(name)
            info.instance = instance
            info.status = ModuleStatus.ACTIVE
            self.events.emit("module_loaded", module=name)
            return True
        except Exception as e:
            info.status = ModuleStatus.ERROR
            info.last_error = str(e)
            print(f"  ❌ 模块加载失败 [{name}]: {e}")
            return False

    def _create_module_instance(self, name: str):
        """创建模块实例"""
        if name == "novel_memory":
            from novel_memory_manager import NovelMemoryManager
            return NovelMemoryManager()

        elif name == "namer":
            from chinese_traditional_namer import ChineseTraditionalNamer
            return ChineseTraditionalNamer()

        elif name == "plotter":
            from plot_brainstorm_engine import PlotBrainstormEngine
            memory = self.modules.get("novel_memory")
            engine = self.modules.get("engine")
            return PlotBrainstormEngine(
                memory_manager=memory.instance if memory and memory.instance else None,
                creative_engine=engine.instance if engine and engine.instance else None,
            )

        elif name == "detector":
            from ai_detector_and_rewriter import AIDetectorAndRewriter
            return AIDetectorAndRewriter()

        elif name == "enhanced_detector":
            from enhanced_ai_detector import EnhancedAIDetector
            return EnhancedAIDetector()

        elif name == "engine":
            from engine.creative_engine import SmartCreativeEngine
            return SmartCreativeEngine()

        elif name == "learning_engine":
            from self_learning_engine import SelfLearningEngine
            return SelfLearningEngine()

        elif name == "pipeline":
            from collaborative_pipeline import CollaborativeWritingPipeline
            return CollaborativeWritingPipeline(
                memory_manager=self._get_instance("novel_memory"),
                creative_engine=self._get_instance("engine"),
                name_generator=self._get_instance("namer"),
                plot_engine=self._get_instance("plotter"),
                ai_detector=self._get_instance("detector"),
                enhanced_detector=self._get_instance("enhanced_detector"),
            )

        elif name == "skill_manager":
            from skill_manager.skill_manager import SkillManagerBuilder
            manager = SkillManagerBuilder.create_default_manager()
            engine = self._get_instance("engine")
            if engine:
                manager.set_engine(engine)
            return manager

        return None

    def _get_instance(self, name: str):
        """获取模块实例"""
        info = self.modules.get(name)
        return info.instance if info and info.instance else None

    def execute(self, command: str, **kwargs) -> Dict[str, Any]:
        """执行命令 - 智能路由"""
        t0 = time.time()
        self.command_history.append({
            "command": command,
            "kwargs": kwargs,
            "time": datetime.now().isoformat(),
        })

        result = {"success": False, "command": command, "data": None, "error": None}

        try:
            if command == "generate_names":
                result = self._cmd_generate_names(**kwargs)

            elif command == "brainstorm_plot":
                result = self._cmd_brainstorm_plot(**kwargs)

            elif command == "design_plot_arc":
                result = self._cmd_design_plot_arc(**kwargs)

            elif command == "detect_ai":
                result = self._cmd_detect_ai(**kwargs)

            elif command == "rewrite_text":
                result = self._cmd_rewrite_text(**kwargs)

            elif command == "run_pipeline":
                result = self._cmd_run_pipeline(**kwargs)

            elif command == "save_memory":
                result = self._cmd_save_memory(**kwargs)

            elif command == "get_context":
                result = self._cmd_get_context(**kwargs)

            elif command == "get_status":
                result = self._cmd_get_status()

            elif command == "create_character":
                result = self._cmd_create_character(**kwargs)

            else:
                result["error"] = f"未知命令: {command}"

        except Exception as e:
            result["error"] = str(e)

        result["duration_ms"] = (time.time() - t0) * 1000
        return result

    def _cmd_generate_names(self, **kwargs) -> Dict:
        self.load_module("namer")
        namer = self._get_instance("namer")
        if not namer:
            return {"success": False, "error": "命名模块未加载"}

        from chinese_traditional_namer import Gender
        gender = Gender.MALE if kwargs.get("gender", "male") == "male" else Gender.FEMALE
        surname = kwargs.get("surname")
        count = kwargs.get("count", 5)
        strategy = kwargs.get("strategy", "balanced")

        names = namer.generate(surname=surname, gender=gender, count=count, strategy=strategy)
        return {
            "success": True,
            "data": [
                {
                    "full_name": n.full_name,
                    "surname": n.surname,
                    "given_name": n.given_name,
                    "generation_char": n.generation_char,
                    "element": n.element.chinese_name,
                    "trigram": n.trigram.chinese_name if n.trigram else "",
                    "meaning": n.meaning,
                    "score": n.score,
                }
                for n in names
            ],
        }

    def _cmd_brainstorm_plot(self, **kwargs) -> Dict:
        self.load_module("plotter")
        plotter = self._get_instance("plotter")
        if not plotter:
            return {"success": False, "error": "剧情模块未加载"}

        ideas = plotter.brainstorm_ideas(
            kwargs.get("genre", "玄幻"),
            kwargs.get("theme", ""),
            kwargs.get("count", 5),
        )
        return {"success": True, "data": ideas}

    def _cmd_design_plot_arc(self, **kwargs) -> Dict:
        self.load_module("plotter")
        plotter = self._get_instance("plotter")
        if not plotter:
            return {"success": False, "error": "剧情模块未加载"}

        from plot_brainstorm_engine import PlotArcType

        arc_type_map = {
            "three_act": PlotArcType.THREE_ACT,
            "hero": PlotArcType.HERO_JOURNEY,
            "revenge": PlotArcType.REVENGE_ARC,
            "growth": PlotArcType.GROWTH_ARC,
        }

        arc_type = arc_type_map.get(kwargs.get("arc_type", "three_act"), PlotArcType.THREE_ACT)
        arc = plotter.design_plot_arc(arc_type, kwargs.get("chapters", 30), kwargs.get("genre", "玄幻"))
        exported = plotter.export_plot(arc)

        return {"success": True, "data": exported}

    def _cmd_detect_ai(self, **kwargs) -> Dict:
        self.load_module("enhanced_detector")
        detector = self._get_instance("enhanced_detector")
        if not detector:
            self.load_module("detector")
            detector = self._get_instance("detector")

        if not detector:
            return {"success": False, "error": "检测模块未加载"}

        text = kwargs.get("text", "")
        if hasattr(detector, 'detect'):
            report = detector.detect(text)
            return {
                "success": True,
                "data": {
                    "score": report.overall_score,
                    "level": report.level,
                    "suggestions": report.suggestions,
                },
            }

        score = detector.detect_ai_score(text)
        return {"success": True, "data": {"score": score}}

    def _cmd_rewrite_text(self, **kwargs) -> Dict:
        self.load_module("enhanced_detector")
        detector = self._get_instance("enhanced_detector")
        if not detector:
            self.load_module("detector")
            detector = self._get_instance("detector")

        if not detector:
            return {"success": False, "error": "检测模块未加载"}

        text = kwargs.get("text", "")
        intensity = kwargs.get("intensity", "medium")

        if hasattr(detector, 'rewrite'):
            rewritten, report = detector.rewrite(text, intensity)
            return {
                "success": True,
                "data": {
                    "rewritten": rewritten,
                    "original_score": report.original_score,
                    "final_score": report.final_score,
                    "reduction": report.reduction,
                },
            }

        rewritten = detector.rewrite_remove_ai(text)
        return {"success": True, "data": {"rewritten": rewritten}}

    def _cmd_run_pipeline(self, **kwargs) -> Dict:
        self.load_module("pipeline")
        pipeline = self._get_instance("pipeline")
        if not pipeline:
            return {"success": False, "error": "流水线模块未加载"}

        pipeline.novel_title = kwargs.get("title", "未命名作品")
        summary = pipeline.run(
            genre=kwargs.get("genre", "玄幻"),
            theme=kwargs.get("theme", ""),
            chapter_count=kwargs.get("chapter_count", 1),
            starting_chapter=kwargs.get("starting_chapter", 1),
        )

        return {"success": True, "data": summary}

    def _cmd_save_memory(self, **kwargs) -> Dict:
        self.load_module("novel_memory")
        memory = self._get_instance("novel_memory")
        if not memory:
            return {"success": False, "error": "记忆模块未加载"}

        content = kwargs.get("content", "")
        chapter = kwargs.get("chapter", 1)
        tags = kwargs.get("tags", [])

        memory.record_plot_event(chapter, content, tags=tags)
        return {"success": True, "data": {"message": "已记录"}}

    def _cmd_get_context(self, **kwargs) -> Dict:
        self.load_module("novel_memory")
        memory = self._get_instance("novel_memory")
        if not memory:
            return {"success": False, "error": "记忆模块未加载"}

        report = memory.get_comprehensive_report()
        return {"success": True, "data": report}

    def _cmd_get_status(self) -> Dict:
        status = {
            "session": self.global_state,
            "modules": {
                name: {
                    "status": info.status.value,
                    "calls": info.call_count,
                    "total_time_ms": info.total_time_ms,
                }
                for name, info in self.modules.items()
            },
            "command_count": len(self.command_history),
        }
        return {"success": True, "data": status}

    def _cmd_create_character(self, **kwargs) -> Dict:
        self.load_module("namer")
        self.load_module("novel_memory")

        namer = self._get_instance("namer")
        memory = self._get_instance("novel_memory")

        if not namer:
            return {"success": False, "error": "命名模块未加载"}

        from chinese_traditional_namer import Gender
        gender = Gender.MALE if kwargs.get("gender", "male") == "male" else Gender.FEMALE
        surname = kwargs.get("surname")
        role = kwargs.get("role", "主角")
        birth_year = kwargs.get("birth_year")
        birth_month = kwargs.get("birth_month")
        birth_day = kwargs.get("birth_day")

        if birth_year:
            names = namer.generate_with_birth(
                surname=surname, year=birth_year,
                month=birth_month or 1, day=birth_day or 1,
                gender=gender, count=1
            )
        else:
            names = namer.generate(surname=surname, gender=gender, count=1)

        if not names:
            return {"success": False, "error": "命名失败"}

        char_data = {
            "full_name": names[0].full_name,
            "surname": names[0].surname,
            "given_name": names[0].given_name,
            "generation_char": names[0].generation_char,
            "element": names[0].element.chinese_name,
            "trigram": names[0].trigram.chinese_name if names[0].trigram else "",
            "meaning": names[0].meaning,
            "score": names[0].score,
            "role": role,
            "gender": gender.value,
        }

        if memory:
            memory.register_character(
                names[0].full_name,
                role=role,
                gender=gender.value,
                first_appearance_chapter=kwargs.get("chapter", 1),
            )

        return {"success": True, "data": char_data}

    def get_module_status(self) -> Dict[str, Dict]:
        """获取所有模块状态"""
        return {
            name: {
                "status": info.status.value,
                "description": info.description,
                "dependencies": info.dependencies,
                "calls": info.call_count,
                "error": info.last_error,
            }
            for name, info in self.modules.items()
        }

    def shutdown(self):
        """关闭编排器"""
        for info in self.modules.values():
            if info.instance and hasattr(info.instance, 'persist'):
                try:
                    info.instance.persist()
                except Exception:
                    pass

        self.events.clear()
        self.global_state["session_end"] = datetime.now().isoformat()


if __name__ == "__main__":
    print("=" * 60)
    print("🎯 智能编排器测试")
    print("=" * 60)

    orch = IntelligentOrchestrator()

    print("\n【模块状态】")
    for name, info in orch.get_module_status().items():
        print(f"  {name}: {info['status']} - {info['description']}")

    print("\n【生成角色名】")
    result = orch.execute("generate_names", genre="xuanhuan", gender="male", count=3)
    if result["success"]:
        for name in result["data"]:
            print(f"  {name['full_name']} — {name['meaning']}")

    print("\n【剧情构思】")
    result = orch.execute("brainstorm_plot", genre="玄幻", count=2)
    if result["success"]:
        for idea in result["data"]:
            print(f"  📌 {idea['template']}: {idea['opening_scene'][:60]}...")

    print("\n【AI检测】")
    test_text = "林晨缓缓地站起身，宛如一只蝴蝶，心中不禁激动万分。"
    result = orch.execute("detect_ai", text=test_text)
    if result["success"]:
        print(f"  AI分数: {result['data']['score']}/100 ({result['data']['level']})")

    print("\n【创建角色】")
    result = orch.execute("create_character", genre="xuanhuan", gender="female", role="女主")
    if result["success"]:
        print(f"  {json.dumps(result['data'], ensure_ascii=False, indent=2)}")

    print("\n【编排器状态】")
    result = orch.execute("get_status")
    if result["success"]:
        s = result["data"]
        print(f"  活跃模块: {sum(1 for m in s['modules'].values() if m['status'] == '活跃中')}")
        print(f"  命令数: {s['command_count']}")

    orch.shutdown()
