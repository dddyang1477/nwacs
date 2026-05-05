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

import os
import time
import json
from collections import Counter
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


class TaskPriority(Enum):
    LOW = 0
    NORMAL = 1
    HIGH = 2
    CRITICAL = 3


class TaskStatus(Enum):
    PENDING = "等待中"
    RUNNING = "执行中"
    COMPLETED = "已完成"
    FAILED = "失败"
    RETRYING = "重试中"
    CANCELLED = "已取消"


@dataclass
class ScheduledTask:
    task_id: str
    command: str
    kwargs: Dict[str, Any] = field(default_factory=dict)
    priority: TaskPriority = TaskPriority.NORMAL
    status: TaskStatus = TaskStatus.PENDING
    created_at: str = ""
    started_at: str = ""
    completed_at: str = ""
    result: Any = None
    error: str = ""
    retry_count: int = 0
    max_retries: int = 3
    retry_delay: float = 1.0
    dependencies: List[str] = field(default_factory=list)
    timeout_seconds: float = 300


@dataclass
class HealthReport:
    module_name: str
    status: str
    uptime_seconds: float = 0
    last_heartbeat: str = ""
    error_count: int = 0
    avg_response_ms: float = 0
    memory_usage_mb: float = 0
    health_score: float = 100
    warnings: List[str] = field(default_factory=list)


@dataclass
class PluginInfo:
    plugin_id: str
    name: str
    version: str
    description: str
    author: str = ""
    enabled: bool = True
    hooks: List[str] = field(default_factory=list)
    config: Dict[str, Any] = field(default_factory=dict)
    loaded_at: str = ""


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

        self.task_queue: List[ScheduledTask] = []
        self._task_counter = 0
        self._task_results: Dict[str, Any] = {}

        self.plugins: Dict[str, PluginInfo] = {}
        self._plugin_hooks: Dict[str, List[Callable]] = {}
        self._plugin_counter = 0

        self.health_reports: Dict[str, HealthReport] = {}
        self._session_start_time = datetime.now()
        self._error_counts: Dict[str, int] = {}
        self._response_times: Dict[str, List[float]] = {}

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
            ("lorebook", "触发式设定注入系统(Lorebook)", []),
            ("story_bible", "集中式创作圣经(Story Bible)", []),
            ("style_manager", "AI风格模块化切换系统", []),
            ("version_manager", "版本管理与历史回溯", []),
            ("platform_exporter", "多平台格式化导出", ["novel_memory"]),
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
            from .novel_memory_manager import NovelMemoryManager
            return NovelMemoryManager()

        elif name == "namer":
            from .chinese_traditional_namer import ChineseTraditionalNamer
            return ChineseTraditionalNamer()

        elif name == "plotter":
            from .plot_brainstorm_engine import PlotBrainstormEngine
            memory = self.modules.get("novel_memory")
            engine = self.modules.get("engine")
            return PlotBrainstormEngine(
                memory_manager=memory.instance if memory and memory.instance else None,
                creative_engine=engine.instance if engine and engine.instance else None,
            )

        elif name == "detector":
            from .ai_detector_and_rewriter import AIDetectorAndRewriter
            return AIDetectorAndRewriter()

        elif name == "enhanced_detector":
            from .enhanced_ai_detector import EnhancedAIDetector
            return EnhancedAIDetector()

        elif name == "engine":
            from engine.creative_engine import SmartCreativeEngine
            return SmartCreativeEngine()

        elif name == "learning_engine":
            from .self_learning_engine import SelfLearningEngine
            return SelfLearningEngine()

        elif name == "pipeline":
            from .collaborative_pipeline import CollaborativeWritingPipeline
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

        elif name == "lorebook":
            from .lorebook import Lorebook
            return Lorebook()

        elif name == "story_bible":
            from .story_bible import StoryBible
            return StoryBible()

        elif name == "style_manager":
            from .style_module_manager import StyleModuleManager
            return StyleModuleManager()

        elif name == "version_manager":
            from .version_manager import VersionManager
            return VersionManager()

        elif name == "platform_exporter":
            from .platform_exporter import PlatformExporter
            return PlatformExporter()

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

            elif command == "lorebook_trigger":
                result = self._cmd_lorebook_trigger(**kwargs)

            elif command == "lorebook_add_entry":
                result = self._cmd_lorebook_add_entry(**kwargs)

            elif command == "bible_add_entry":
                result = self._cmd_bible_add_entry(**kwargs)

            elif command == "bible_check_consistency":
                result = self._cmd_bible_check_consistency()

            elif command == "style_activate":
                result = self._cmd_style_activate(**kwargs)

            elif command == "style_list":
                result = self._cmd_style_list()

            elif command == "version_snapshot":
                result = self._cmd_version_snapshot(**kwargs)

            elif command == "version_diff":
                result = self._cmd_version_diff(**kwargs)

            elif command == "version_rollback":
                result = self._cmd_version_rollback(**kwargs)

            elif command == "export_platform":
                result = self._cmd_export_platform(**kwargs)

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

    def _cmd_lorebook_trigger(self, **kwargs) -> Dict:
        self.load_module("lorebook")
        lorebook = self._get_instance("lorebook")
        if not lorebook:
            return {"success": False, "error": "Lorebook模块未加载"}

        text = kwargs.get("text", "")
        chapter = kwargs.get("chapter", 0)
        triggered = lorebook.trigger(text, chapter)
        context = lorebook.build_context(text, chapter)

        return {
            "success": True,
            "data": {
                "triggered_count": len(triggered),
                "entries": [
                    {"name": e.name, "category": e.category.value, "priority": e.priority.label}
                    for e in triggered
                ],
                "context": context,
            },
        }

    def _cmd_lorebook_add_entry(self, **kwargs) -> Dict:
        self.load_module("lorebook")
        lorebook = self._get_instance("lorebook")
        if not lorebook:
            return {"success": False, "error": "Lorebook模块未加载"}

        from lorebook import LorebookEntry, EntryCategory, EntryPriority

        cat_map = {c.value: c for c in EntryCategory}
        pri_map = {p.weight: p for p in EntryPriority}

        entry = LorebookEntry(
            entry_id="",
            name=kwargs.get("name", ""),
            category=cat_map.get(kwargs.get("category", "自定义"), EntryCategory.CUSTOM),
            content=kwargs.get("content", ""),
            trigger_keywords=kwargs.get("keywords", []),
            priority=pri_map.get(kwargs.get("priority", 3), EntryPriority.MEDIUM),
        )
        eid = lorebook.add_entry(entry)
        return {"success": True, "data": {"entry_id": eid}}

    def _cmd_bible_add_entry(self, **kwargs) -> Dict:
        self.load_module("story_bible")
        bible = self._get_instance("story_bible")
        if not bible:
            return {"success": False, "error": "StoryBible模块未加载"}

        from story_bible import BibleEntry, BibleSection

        sec_map = {s.value: s for s in BibleSection}
        entry = BibleEntry(
            entry_id="",
            section=sec_map.get(kwargs.get("section", "研究资料"), BibleSection.RESEARCH),
            title=kwargs.get("title", ""),
            content=kwargs.get("content", ""),
            tags=kwargs.get("tags", []),
        )
        eid = bible.add_entry(entry)
        return {"success": True, "data": {"entry_id": eid}}

    def _cmd_bible_check_consistency(self) -> Dict:
        self.load_module("story_bible")
        bible = self._get_instance("story_bible")
        if not bible:
            return {"success": False, "error": "StoryBible模块未加载"}

        issues = bible.check_consistency()
        return {
            "success": True,
            "data": {
                "issue_count": len(issues),
                "issues": [
                    {"entry_a": i.entry_a, "entry_b": i.entry_b,
                     "field": i.field, "severity": i.severity,
                     "description": i.description}
                    for i in issues
                ],
            },
        }

    def _cmd_style_activate(self, **kwargs) -> Dict:
        self.load_module("style_manager")
        style_mgr = self._get_instance("style_manager")
        if not style_mgr:
            return {"success": False, "error": "风格模块未加载"}

        module_id = kwargs.get("module_id", "")
        if module_id:
            ok = style_mgr.activate(module_id)
            if not ok:
                return {"success": False, "error": f"风格模块不存在: {module_id}"}

        active = style_mgr.active_module
        return {
            "success": True,
            "data": {
                "active_style": active.name if active else "无",
                "rules": style_mgr.get_active_rules(),
                "prompt": style_mgr.get_active_prompt()[:200],
            },
        }

    def _cmd_style_list(self) -> Dict:
        self.load_module("style_manager")
        style_mgr = self._get_instance("style_manager")
        if not style_mgr:
            return {"success": False, "error": "风格模块未加载"}

        modules = style_mgr.list_modules()
        return {
            "success": True,
            "data": [
                {"id": m.module_id, "name": m.name, "category": m.category.label,
                 "description": m.description}
                for m in modules
            ],
        }

    def _cmd_version_snapshot(self, **kwargs) -> Dict:
        self.load_module("version_manager")
        ver_mgr = self._get_instance("version_manager")
        if not ver_mgr:
            return {"success": False, "error": "版本管理模块未加载"}

        from version_manager import SnapshotType
        snap_id = ver_mgr.create_snapshot(
            chapter=kwargs.get("chapter", 1),
            content=kwargs.get("content", ""),
            snapshot_type=SnapshotType.MANUAL,
            message=kwargs.get("message", ""),
        )
        return {"success": True, "data": {"snapshot_id": snap_id}}

    def _cmd_version_diff(self, **kwargs) -> Dict:
        self.load_module("version_manager")
        ver_mgr = self._get_instance("version_manager")
        if not ver_mgr:
            return {"success": False, "error": "版本管理模块未加载"}

        diff = ver_mgr.diff(kwargs.get("snap_a", ""), kwargs.get("snap_b", ""))
        if not diff:
            return {"success": False, "error": "版本对比失败"}

        return {
            "success": True,
            "data": {
                "added": diff.added_lines,
                "removed": diff.removed_lines,
                "modified": diff.modified_lines,
                "total_changes": diff.total_changes,
                "change_ratio": diff.change_ratio,
            },
        }

    def _cmd_version_rollback(self, **kwargs) -> Dict:
        self.load_module("version_manager")
        ver_mgr = self._get_instance("version_manager")
        if not ver_mgr:
            return {"success": False, "error": "版本管理模块未加载"}

        new_id = ver_mgr.rollback(kwargs.get("snapshot_id", ""))
        if not new_id:
            return {"success": False, "error": "回滚失败"}

        return {"success": True, "data": {"new_snapshot_id": new_id}}

    def _cmd_export_platform(self, **kwargs) -> Dict:
        self.load_module("platform_exporter")
        exporter = self._get_instance("platform_exporter")
        if not exporter:
            return {"success": False, "error": "导出模块未加载"}

        from platform_exporter import NovelMeta, ChapterData, ExportPlatform

        plat_map = {p.label: p for p in ExportPlatform}
        platform = plat_map.get(kwargs.get("platform", "通用TXT"), ExportPlatform.TXT)

        chapters = []
        for ch_data in kwargs.get("chapters", []):
            chapters.append(ChapterData(
                chapter_num=ch_data.get("num", 1),
                title=ch_data.get("title", ""),
                content=ch_data.get("content", ""),
                word_count=ch_data.get("words", 0),
            ))

        meta = NovelMeta(
            title=kwargs.get("title", "未命名作品"),
            author=kwargs.get("author", "未知作者"),
            genre=kwargs.get("genre", "其他"),
            synopsis=kwargs.get("synopsis", ""),
            tags=kwargs.get("tags", []),
        )

        path = exporter.export(meta, chapters, platform)
        return {"success": True, "data": {"output_path": path}}

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

    def enqueue_task(self, command: str, priority: TaskPriority = TaskPriority.NORMAL,
                     max_retries: int = 3, retry_delay: float = 1.0,
                     dependencies: List[str] = None,
                     timeout_seconds: float = 300, **kwargs) -> str:
        self._task_counter += 1
        task_id = f"TASK_{self._task_counter:06d}"

        task = ScheduledTask(
            task_id=task_id,
            command=command,
            kwargs=kwargs,
            priority=priority,
            created_at=datetime.now().isoformat(),
            max_retries=max_retries,
            retry_delay=retry_delay,
            dependencies=dependencies or [],
            timeout_seconds=timeout_seconds,
        )

        self.task_queue.append(task)
        self.task_queue.sort(key=lambda t: t.priority.value, reverse=True)
        self.events.emit("task_enqueued", task_id=task_id, command=command)
        return task_id

    def execute_task(self, task: ScheduledTask) -> Any:
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.now().isoformat()

        try:
            result = self.execute(task.command, **task.kwargs)
            if result.get("success"):
                task.status = TaskStatus.COMPLETED
                task.result = result
            else:
                if task.retry_count < task.max_retries:
                    task.status = TaskStatus.RETRYING
                    task.retry_count += 1
                    task.error = result.get("error", "未知错误")
                    import time as _time
                    _time.sleep(task.retry_delay * (2 ** (task.retry_count - 1)))
                    return self.execute_task(task)
                else:
                    task.status = TaskStatus.FAILED
                    task.error = result.get("error", "未知错误")
        except Exception as e:
            if task.retry_count < task.max_retries:
                task.status = TaskStatus.RETRYING
                task.retry_count += 1
                task.error = str(e)
                import time as _time
                _time.sleep(task.retry_delay * (2 ** (task.retry_count - 1)))
                return self.execute_task(task)
            else:
                task.status = TaskStatus.FAILED
                task.error = str(e)

        task.completed_at = datetime.now().isoformat()
        self._task_results[task.task_id] = task.result
        self.events.emit("task_completed", task_id=task.task_id,
                         status=task.status.value)
        return task.result

    def process_queue(self, max_tasks: int = 10) -> List[Dict]:
        results = []
        processed = 0

        pending = [t for t in self.task_queue
                   if t.status == TaskStatus.PENDING]

        for task in pending:
            if processed >= max_tasks:
                break

            deps_met = all(
                dep in self._task_results
                for dep in task.dependencies
            )
            if not deps_met:
                continue

            result = self.execute_task(task)
            results.append({
                "task_id": task.task_id,
                "command": task.command,
                "status": task.status.value,
                "result": result,
            })
            processed += 1

        return results

    def cancel_task(self, task_id: str) -> bool:
        for task in self.task_queue:
            if task.task_id == task_id:
                if task.status in [TaskStatus.PENDING, TaskStatus.RETRYING]:
                    task.status = TaskStatus.CANCELLED
                    task.completed_at = datetime.now().isoformat()
                    return True
        return False

    def get_task_status(self, task_id: str) -> Optional[Dict]:
        for task in self.task_queue:
            if task.task_id == task_id:
                return {
                    "task_id": task.task_id,
                    "command": task.command,
                    "priority": task.priority.name,
                    "status": task.status.value,
                    "retry_count": task.retry_count,
                    "error": task.error,
                    "created_at": task.created_at,
                    "completed_at": task.completed_at,
                }
        return None

    def get_queue_stats(self) -> Dict:
        status_counts = Counter(t.status.value for t in self.task_queue)
        priority_counts = Counter(t.priority.name for t in self.task_queue)
        return {
            "total_tasks": len(self.task_queue),
            "by_status": dict(status_counts),
            "by_priority": dict(priority_counts),
            "pending": sum(1 for t in self.task_queue
                          if t.status == TaskStatus.PENDING),
            "failed": sum(1 for t in self.task_queue
                         if t.status == TaskStatus.FAILED),
            "completed": sum(1 for t in self.task_queue
                            if t.status == TaskStatus.COMPLETED),
        }

    def execute_with_retry(self, command: str, max_retries: int = 3,
                           base_delay: float = 1.0, **kwargs) -> Dict:
        last_error = None
        for attempt in range(max_retries + 1):
            try:
                result = self.execute(command, **kwargs)
                if result.get("success"):
                    result["attempts"] = attempt + 1
                    return result
                last_error = result.get("error", "未知错误")
            except Exception as e:
                last_error = str(e)

            if attempt < max_retries:
                delay = base_delay * (2 ** attempt)
                import time as _time
                _time.sleep(delay)

        return {
            "success": False,
            "command": command,
            "error": last_error,
            "attempts": max_retries + 1,
        }

    def execute_pipeline(self, steps: List[Dict]) -> List[Dict]:
        results = []
        context = {}

        for i, step in enumerate(steps):
            command = step.get("command", "")
            kwargs = {**step.get("kwargs", {}), **context}
            on_failure = step.get("on_failure", "stop")

            result = self.execute(command, **kwargs)
            results.append({
                "step": i + 1,
                "command": command,
                "success": result.get("success", False),
                "data": result.get("data"),
                "error": result.get("error"),
            })

            if result.get("success"):
                if result.get("data"):
                    context.update(result["data"]
                                   if isinstance(result["data"], dict)
                                   else {"_last_result": result["data"]})
            else:
                if on_failure == "stop":
                    break
                elif on_failure == "continue":
                    continue

        return results

    def record_response_time(self, module_name: str, duration_ms: float):
        if module_name not in self._response_times:
            self._response_times[module_name] = []
        self._response_times[module_name].append(duration_ms)
        if len(self._response_times[module_name]) > 100:
            self._response_times[module_name] = \
                self._response_times[module_name][-100:]

    def record_error(self, module_name: str):
        self._error_counts[module_name] = \
            self._error_counts.get(module_name, 0) + 1

    def check_health(self, module_name: str = None) -> Dict:
        if module_name:
            return self._check_module_health(module_name)

        results = {}
        for name in self.modules:
            results[name] = self._check_module_health(name)
        return results

    def _check_module_health(self, module_name: str) -> Dict:
        info = self.modules.get(module_name)
        if not info:
            return {"error": f"模块不存在: {module_name}"}

        uptime = (datetime.now() - self._session_start_time).total_seconds()
        error_count = self._error_counts.get(module_name, 0)
        response_times = self._response_times.get(module_name, [])
        avg_response = (sum(response_times) / len(response_times)
                        if response_times else 0)

        health_score = 100.0
        warnings = []

        if info.status == ModuleStatus.ERROR:
            health_score -= 50
            warnings.append("模块处于错误状态")
        if error_count > 10:
            health_score -= 20
            warnings.append(f"错误次数过多({error_count})")
        if avg_response > 5000:
            health_score -= 15
            warnings.append(f"平均响应时间过长({avg_response:.0f}ms)")
        if info.status == ModuleStatus.UNLOADED:
            health_score -= 10
            warnings.append("模块未加载")

        health_score = max(0, health_score)

        report = HealthReport(
            module_name=module_name,
            status=info.status.value,
            uptime_seconds=uptime,
            last_heartbeat=datetime.now().isoformat(),
            error_count=error_count,
            avg_response_ms=round(avg_response, 2),
            health_score=health_score,
            warnings=warnings,
        )
        self.health_reports[module_name] = report

        return {
            "module": module_name,
            "status": info.status.value,
            "health_score": health_score,
            "error_count": error_count,
            "avg_response_ms": round(avg_response, 2),
            "warnings": warnings,
        }

    def get_health_dashboard(self) -> Dict:
        all_health = self.check_health()
        modules_healthy = sum(
            1 for h in all_health.values()
            if isinstance(h, dict) and h.get("health_score", 0) >= 80
        )
        modules_warning = sum(
            1 for h in all_health.values()
            if isinstance(h, dict) and 50 <= h.get("health_score", 0) < 80
        )
        modules_critical = sum(
            1 for h in all_health.values()
            if isinstance(h, dict) and h.get("health_score", 0) < 50
        )

        return {
            "timestamp": datetime.now().isoformat(),
            "session_uptime_seconds": (
                datetime.now() - self._session_start_time
            ).total_seconds(),
            "total_modules": len(self.modules),
            "healthy": modules_healthy,
            "warning": modules_warning,
            "critical": modules_critical,
            "overall_health": "healthy" if modules_critical == 0 else (
                "warning" if modules_critical <= 2 else "critical"
            ),
            "modules": all_health,
            "queue_stats": self.get_queue_stats(),
        }

    def get_performance_report(self) -> Dict:
        report = {
            "timestamp": datetime.now().isoformat(),
            "session_duration_seconds": (
                datetime.now() - self._session_start_time
            ).total_seconds(),
            "total_commands": len(self.command_history),
            "modules": {},
        }

        for name, info in self.modules.items():
            response_times = self._response_times.get(name, [])
            report["modules"][name] = {
                "status": info.status.value,
                "call_count": info.call_count,
                "total_time_ms": info.total_time_ms,
                "avg_response_ms": (
                    sum(response_times) / len(response_times)
                    if response_times else 0
                ),
                "min_response_ms": min(response_times) if response_times else 0,
                "max_response_ms": max(response_times) if response_times else 0,
                "error_count": self._error_counts.get(name, 0),
            }

        return report

    def register_plugin(self, name: str, version: str, description: str,
                        author: str = "", hooks: List[str] = None,
                        config: Dict[str, Any] = None) -> str:
        self._plugin_counter += 1
        plugin_id = f"PLUGIN_{self._plugin_counter:04d}"

        self.plugins[plugin_id] = PluginInfo(
            plugin_id=plugin_id,
            name=name,
            version=version,
            description=description,
            author=author,
            hooks=hooks or [],
            config=config or {},
            loaded_at=datetime.now().isoformat(),
        )

        for hook in (hooks or []):
            if hook not in self._plugin_hooks:
                self._plugin_hooks[hook] = []

        self.events.emit("plugin_registered", plugin_id=plugin_id, name=name)
        return plugin_id

    def unregister_plugin(self, plugin_id: str) -> bool:
        if plugin_id in self.plugins:
            plugin = self.plugins[plugin_id]
            for hook in plugin.hooks:
                if hook in self._plugin_hooks:
                    self._plugin_hooks[hook] = [
                        h for h in self._plugin_hooks[hook]
                        if getattr(h, '__plugin_id__', '') != plugin_id
                    ]
            del self.plugins[plugin_id]
            self.events.emit("plugin_unregistered", plugin_id=plugin_id)
            return True
        return False

    def register_hook(self, hook_name: str, callback: Callable,
                      plugin_id: str = None):
        if hook_name not in self._plugin_hooks:
            self._plugin_hooks[hook_name] = []
        if plugin_id:
            callback.__plugin_id__ = plugin_id
        self._plugin_hooks[hook_name].append(callback)

    def trigger_hook(self, hook_name: str, **data) -> List[Any]:
        results = []
        for callback in self._plugin_hooks.get(hook_name, []):
            try:
                result = callback(data)
                results.append(result)
            except Exception as e:
                results.append({"error": str(e)})
        return results

    def get_plugins(self) -> List[Dict]:
        return [
            {
                "plugin_id": p.plugin_id,
                "name": p.name,
                "version": p.version,
                "description": p.description,
                "author": p.author,
                "enabled": p.enabled,
                "hooks": p.hooks,
            }
            for p in self.plugins.values()
        ]

    def save_session(self, filepath: str = None) -> str:
        if filepath is None:
            filepath = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "sessions",
                f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        session_data = {
            "global_state": self.global_state,
            "command_history": self.command_history[-500:],
            "module_status": {
                name: {
                    "status": info.status.value,
                    "call_count": info.call_count,
                    "total_time_ms": info.total_time_ms,
                }
                for name, info in self.modules.items()
            },
            "task_queue": [
                {
                    "task_id": t.task_id,
                    "command": t.command,
                    "priority": t.priority.name,
                    "status": t.status.value,
                }
                for t in self.task_queue
            ],
            "plugins": [
                {
                    "plugin_id": p.plugin_id,
                    "name": p.name,
                    "version": p.version,
                    "enabled": p.enabled,
                }
                for p in self.plugins.values()
            ],
            "saved_at": datetime.now().isoformat(),
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(session_data, f, ensure_ascii=False, indent=2)

        return filepath

    def load_session(self, filepath: str) -> bool:
        if not os.path.exists(filepath):
            return False

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.global_state.update(data.get("global_state", {}))
            self.command_history = data.get("command_history", [])

            for name, status_data in data.get("module_status", {}).items():
                if name in self.modules:
                    self.modules[name].call_count = status_data.get("call_count", 0)
                    self.modules[name].total_time_ms = status_data.get("total_time_ms", 0)

            return True
        except (json.JSONDecodeError, KeyError) as e:
            print(f"  ⚠️ 会话加载失败: {e}")
            return False

    def get_session_info(self) -> Dict:
        return {
            "session_start": self.global_state.get("session_start"),
            "uptime_seconds": (
                datetime.now() - self._session_start_time
            ).total_seconds(),
            "active_novel": self.global_state.get("active_novel"),
            "current_chapter": self.global_state.get("current_chapter", 0),
            "total_api_calls": self.global_state.get("total_api_calls", 0),
            "total_tokens_used": self.global_state.get("total_tokens_used", 0),
            "commands_executed": len(self.command_history),
            "modules_loaded": sum(
                1 for info in self.modules.values()
                if info.status == ModuleStatus.ACTIVE
            ),
            "plugins_registered": len(self.plugins),
            "tasks_pending": sum(
                1 for t in self.task_queue
                if t.status == TaskStatus.PENDING
            ),
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
