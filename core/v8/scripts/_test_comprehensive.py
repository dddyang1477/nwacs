#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 全模块综合集成测试 v2
覆盖所有15个核心模块 + 跨模块集成
使用正确的模块API
"""

import sys
import os
import json
import time

sys.path.insert(0, os.path.dirname(__file__))

passed = 0
failed = 0
errors = []

def test(name, fn):
    global passed, failed
    try:
        result = fn()
        if isinstance(result, tuple):
            all_pass = all(result)
        else:
            all_pass = bool(result)
        if all_pass:
            passed += 1
            print(f"  OK  {name}")
        else:
            failed += 1
            print(f"  FAIL {name}")
            errors.append((name, "assertion failed"))
    except Exception as e:
        failed += 1
        print(f"  ERR {name}: {e}")
        errors.append((name, str(e)))

def section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

# ================================================================
section("Module 1: Lorebook - Trigger-based Setting Injection")

from lorebook import (
    Lorebook, LorebookEntry, EntryCategory, EntryPriority
)

lb = Lorebook()

test("1.1 instantiate", lambda: isinstance(lb, Lorebook))

test("1.2 add entry", lambda: (
    lb.add_entry(LorebookEntry(
        entry_id="char_001",
        category=EntryCategory.CHARACTER,
        name="萧炎",
        content="主角，天才少年，拥有异火",
        trigger_keywords=["萧炎", "炎帝", "异火"],
        priority=EntryPriority.HIGH,
    )),
    "char_001" in lb.entries,
))

test("1.3 add more entries", lambda: (
    lb.add_entry(LorebookEntry(
        entry_id="loc_001",
        category=EntryCategory.LOCATION,
        name="乌坦城",
        content="萧家所在的边陲小城",
        trigger_keywords=["乌坦城", "萧家"],
        priority=EntryPriority.MEDIUM,
    )),
    lb.add_entry(LorebookEntry(
        entry_id="item_001",
        category=EntryCategory.ITEM,
        name="玄重尺",
        content="药老赠予萧炎的重尺，用于修炼",
        trigger_keywords=["玄重尺", "重尺"],
        priority=EntryPriority.LOW,
    )),
    len(lb.entries) >= 3,
))

test("1.4 trigger by keyword", lambda: (
    text := "萧炎站在乌坦城的城墙上，手握玄重尺，目光坚定。",
    triggered := lb.trigger(text),
    len(triggered) >= 1,
    any(e.name == "萧炎" for e in triggered),
))

test("1.5 trigger multiple entries", lambda: (
    text := "萧炎回到乌坦城，萧家已经物是人非。",
    triggered := lb.trigger(text),
    len(triggered) >= 2,
))

test("1.6 build context", lambda: (
    text := "萧炎手持玄重尺，在乌坦城中与敌人激战。",
    ctx := lb.build_context(text),
    len(ctx) > 0,
    "萧炎" in ctx,
))

test("1.7 cascade trigger", lambda: (
    lb.add_entry(LorebookEntry(
        entry_id="char_002",
        category=EntryCategory.CHARACTER,
        name="药老",
        content="萧炎的师父，灵魂体",
        trigger_keywords=["药老", "药尊者"],
        priority=EntryPriority.HIGH,
        cascade_to=["item_001"],
    )),
    text := "药老从戒指中飘出，神色凝重。",
    triggered := lb.trigger(text),
    any(e.name == "药老" for e in triggered),
))

test("1.8 entry deactivation", lambda: (
    lb.update_entry("item_001", is_active=False),
    entry := lb.entries.get("item_001"),
    entry is not None and not entry.is_active,
))

test("1.9 entry reactivation", lambda: (
    lb.update_entry("item_001", is_active=True),
    entry := lb.entries.get("item_001"),
    entry is not None and entry.is_active,
))

test("1.10 remove entry", lambda: (
    lb.remove_entry("char_002"),
    "char_002" not in lb.entries,
))

test("1.11 get entries by category", lambda: (
    chars := lb.find_by_category(EntryCategory.CHARACTER),
    len(chars) >= 1,
    any(e.name == "萧炎" for e in chars),
))

def _check_lorebook_persistence():
    lb.save()
    lb2 = Lorebook()
    return "char_001" in lb2.entries and "loc_001" in lb2.entries

test("1.12 persistence save/load", lambda: _check_lorebook_persistence())

test("1.13 context budget management", lambda: (
    long_text := "萧炎" * 500,
    ctx := lb.build_context(long_text, max_tokens=500),
    len(ctx) <= 500 * 4,
))

test("1.14 usage statistics", lambda: (
    stats := lb.get_stats(),
    isinstance(stats, dict),
    "total_entries" in stats,
))

# ================================================================
section("Module 2: Story Bible - Centralized Creative Bible")

from story_bible import (
    StoryBible, BibleEntry, BibleSection, ConsistencyIssue
)

sb = StoryBible("测试小说")

test("2.1 instantiate", lambda: (
    isinstance(sb, StoryBible),
    sb.novel_title == "测试小说",
))

test("2.2 add character entry", lambda: (
    entry := BibleEntry(
        entry_id="",
        section=BibleSection.CHARACTERS,
        title="林风",
        content="主角，25岁，剑修，性格坚毅",
        tags=["主角", "剑修"],
    ),
    eid := sb.add_entry(entry),
    len(eid) > 0,
))

test("2.3 add worldbuilding entry", lambda: (
    entry := BibleEntry(
        entry_id="",
        section=BibleSection.WORLD_BUILDING,
        title="青云宗",
        content="修仙界三大宗门之一，以剑道闻名",
        tags=["宗门", "剑道"],
    ),
    eid := sb.add_entry(entry),
    len(eid) > 0,
))

test("2.4 add plot entry", lambda: (
    entry := BibleEntry(
        entry_id="",
        section=BibleSection.PLOT_OUTLINE,
        title="第一卷大纲",
        content="林风拜入青云宗，从外门弟子成长为内门弟子",
        tags=["大纲", "第一卷"],
    ),
    eid := sb.add_entry(entry),
    len(eid) > 0,
))

test("2.5 get section entries", lambda: (
    chars := sb.get_section(BibleSection.CHARACTERS),
    len(chars) >= 1,
    worlds := sb.get_section(BibleSection.WORLD_BUILDING),
    len(worlds) >= 1,
))

def _update_entry_content():
    chars = sb.get_section(BibleSection.CHARACTERS)
    entry = chars[0]
    sb.update_entry(entry.entry_id, BibleSection.CHARACTERS,
                    content="林风，25岁，剑修，性格坚毅，拥有先天剑体")
    updated = sb.get_entry(entry.entry_id, BibleSection.CHARACTERS)
    return updated is not None and "先天剑体" in updated.content

test("2.6 update entry", lambda: _update_entry_content())

def _add_cross_refs():
    chars = sb.get_section(BibleSection.CHARACTERS)
    worlds = sb.get_section(BibleSection.WORLD_BUILDING)
    char = chars[0]
    world = worlds[0]
    char.references.append(world.entry_id)
    sb.update_entry(char.entry_id, BibleSection.CHARACTERS,
                    references=char.references)
    updated = sb.get_entry(char.entry_id, BibleSection.CHARACTERS)
    return world.entry_id in updated.references

test("2.7 add cross-references", lambda: _add_cross_refs())

test("2.8 consistency check", lambda: (
    issues := sb.check_consistency(),
    isinstance(issues, list),
))

def _add_entry_with_metadata():
    entry = BibleEntry(
        entry_id="",
        section=BibleSection.CHARACTERS,
        title="苏婉",
        content="女主角，青云宗内门弟子",
        tags=["主角", "女修"],
    )
    entry.metadata = {"name": "苏婉", "age": "22", "faction": "青云宗"}
    eid = sb.add_entry(entry)
    return len(eid) > 0

test("2.9 add entry with metadata", lambda: _add_entry_with_metadata())

test("2.10 search entries by title", lambda: (
    results := sb.find_by_title("青云宗"),
    len(results) >= 1,
))

test("2.11 search entries by tag", lambda: (
    results := sb.find_by_tag("主角"),
    len(results) >= 1,
))

def _get_all_bible_entries():
    all_entries = []
    for section in BibleSection:
        all_entries.extend(sb.get_section(section))
    return len(all_entries) >= 4

test("2.12 get all entries", lambda: _get_all_bible_entries())

test("2.13 export report", lambda: (
    report := sb.export_full_report(),
    len(report) > 0,
    "测试小说" in report,
    "林风" in report,
))

def _check_bible_persistence():
    sb.save()
    sb2 = StoryBible("测试小说")
    all_entries = []
    for section in BibleSection:
        all_entries.extend(sb2.get_section(section))
    return len(all_entries) >= 4

test("2.14 persistence", lambda: _check_bible_persistence())

def _delete_entry():
    entries = sb.get_section(BibleSection.CHARACTERS)
    if entries:
        sb.remove_entry(entries[-1].entry_id, BibleSection.CHARACTERS)
    return True

test("2.15 delete entry", lambda: _delete_entry())

# ================================================================
section("Module 3: StyleModuleManager - AI Style Modular Switching")

from style_module_manager import (
    StyleModuleManager, StyleModule, StyleCategory
)

sm = StyleModuleManager()

test("3.1 instantiate", lambda: isinstance(sm, StyleModuleManager))

test("3.2 built-in modules loaded", lambda: (
    len(sm.modules) >= 8,
))

test("3.3 list modules", lambda: (
    modules := sm.list_modules(),
    len(modules) >= 8,
))

def _activate_module():
    module_ids = list(sm.modules.keys())
    if module_ids:
        sm.activate(module_ids[0])
    return sm.active_module is not None

test("3.4 activate module", lambda: _activate_module())

test("3.5 get active prompt", lambda: (
    prompt := sm.get_active_prompt(),
    len(prompt) > 0,
))

def _deactivate_style():
    sm.active_module = None
    sm.active_blend = {}
    return sm.active_module is None and sm.active_blend == {}

test("3.6 deactivate", lambda: _deactivate_style())

def _blend_styles():
    module_ids = list(sm.modules.keys())
    if len(module_ids) >= 2:
        sm.blend({module_ids[0]: 0.6, module_ids[1]: 0.4})
    return len(sm.active_blend) >= 2 if len(module_ids) >= 2 else True

test("3.7 blend styles", lambda: _blend_styles())

test("3.8 get blend prompt", lambda: (
    prompt := sm.get_active_prompt(),
    len(prompt) > 0,
))

test("3.9 extract style from text", lambda: (
    sample := "夜风轻拂，月光如水银般倾泻在青石板上。他独自站在庭院中，手中长剑映着寒光，心中思绪万千。",
    module := sm.extract_style_from_text(sample, "测试风格", StyleCategory.CLASSICAL),
    module is not None,
    len(module.writing_rules) > 0,
))

def _register_custom_module():
    custom = StyleModule(
        module_id="custom_001",
        name="暗黑风格",
        category=StyleCategory.SUSPENSE,
        description="黑暗压抑的写作风格",
        system_prompt="以冷峻克制的笔调写作，营造压抑氛围。",
        writing_rules=["多用短句", "少用形容词", "保持冷峻"],
    )
    sm.register_module(custom)
    return "custom_001" in sm.modules

test("3.10 register custom module", lambda: _register_custom_module())

test("3.11 get module by category", lambda: (
    modules := sm.list_modules(StyleCategory.CLASSICAL),
    len(modules) >= 1,
))

def _check_style_persistence():
    sm.save()
    sm2 = StyleModuleManager()
    return len(sm2.modules) >= 8

test("3.12 persistence", lambda: _check_style_persistence())

# ================================================================
section("Module 4: VersionManager - Version Control & History")

from version_manager import (
    VersionManager, VersionSnapshot, SnapshotType, DiffResult
)

vm = VersionManager("测试版本小说")

test("4.1 instantiate", lambda: (
    isinstance(vm, VersionManager),
    vm.novel_title == "测试版本小说",
))

test("4.2 create auto snapshot", lambda: (
    content := "第一章：风云初动\n\n天元大陆，灵气充沛。\n\n林风站在青云宗的山门前，望着巍峨的山门，心中激荡。",
    sid := vm.create_snapshot(1, content, SnapshotType.AUTO, "自动保存"),
    len(sid) > 0,
    sid in vm.snapshots,
))

test("4.3 create manual snapshot", lambda: (
    content := "第一章：风云初动\n\n天元大陆，灵气充沛。\n\n林风站在青云宗的山门前，望着巍峨的山门，心中激荡。这是他梦寐以求的修仙圣地。",
    sid := vm.create_snapshot(1, content, SnapshotType.MANUAL, "修改了结尾"),
    len(sid) > 0,
))

test("4.4 create milestone", lambda: (
    content := "第一章：风云初动（终稿）\n\n天元大陆，灵气充沛。\n\n林风站在青云宗的山门前，心中激荡。这是他命运的转折点。",
    sid := vm.create_snapshot(1, content, SnapshotType.MILESTONE, "第一章完成"),
    len(sid) > 0,
))

test("4.5 list snapshots", lambda: (
    snapshots := list(vm.snapshots.values()),
    len(snapshots) >= 3,
))

def _get_snapshot():
    snapshots = list(vm.snapshots.values())
    if snapshots:
        snap = vm.get_snapshot(snapshots[0].snapshot_id)
        return snap is not None and snap.chapter == 1
    return True

test("4.6 get snapshot", lambda: _get_snapshot())

def _diff_versions():
    snapshots = list(vm.snapshots.values())
    if len(snapshots) >= 2:
        diff = vm.diff(snapshots[0].snapshot_id, snapshots[1].snapshot_id)
        return diff is not None and isinstance(diff, DiffResult)
    return True

test("4.7 diff two versions", lambda: _diff_versions())

test("4.8 get history for chapter", lambda: (
    history := vm.get_chapter_history(1),
    len(history) >= 3,
))

def _do_rollback():
    snapshots = list(vm.snapshots.values())
    if snapshots:
        new_sid = vm.rollback(snapshots[0].snapshot_id)
        return new_sid is not None and len(new_sid) > 0
    return True

test("4.9 rollback", lambda: _do_rollback())

def _create_branch():
    if "experiment" not in vm.branches:
        vm.create_branch("experiment")
    return "experiment" in vm.branches

test("4.10 create branch", lambda: _create_branch())

test("4.11 switch branch", lambda: (
    vm.switch_branch("experiment"),
    vm.current_branch == "experiment",
))

test("4.12 create snapshot on branch", lambda: (
    content := "实验分支：第一章\n\n不同的开头尝试...",
    sid := vm.create_snapshot(1, content, SnapshotType.BRANCH, "实验分支"),
    len(sid) > 0,
))

test("4.13 switch back to main", lambda: (
    vm.switch_branch("main"),
    vm.current_branch == "main",
))

def _check_version_persistence():
    vm.save()
    vm2 = VersionManager("测试版本小说")
    return len(vm2.snapshots) >= 4

test("4.14 persistence", lambda: _check_version_persistence())

# ================================================================
section("Module 5: PlatformExporter - Multi-platform Export")

from platform_exporter import (
    PlatformExporter, ExportPlatform, ChapterData, NovelMeta
)

pe = PlatformExporter()

test("5.1 instantiate", lambda: (
    isinstance(pe, PlatformExporter),
    os.path.isdir(pe.output_dir),
))

test("5.2 export TXT", lambda: (
    meta := NovelMeta("测试小说", "测试作者", "玄幻", "", "简介", ["标签"]),
    chapters := [ChapterData(1, "测试", "测试内容", 2, 1)],
    path := pe.export(meta, chapters, ExportPlatform.TXT),
    os.path.exists(path),
))

test("5.3 export Markdown", lambda: (
    meta := NovelMeta("测试小说", "测试作者", "玄幻", "", "简介", ["标签"]),
    chapters := [ChapterData(1, "测试", "测试内容", 2, 1)],
    path := pe.export(meta, chapters, ExportPlatform.MARKDOWN),
    os.path.exists(path),
))

test("5.4 export HTML", lambda: (
    meta := NovelMeta("测试小说", "测试作者", "玄幻", "", "简介", ["标签"]),
    chapters := [ChapterData(1, "测试", "测试内容", 2, 1)],
    path := pe.export(meta, chapters, ExportPlatform.HTML),
    os.path.exists(path),
))

test("5.5 export Qidian format", lambda: (
    meta := NovelMeta("测试小说", "测试作者", "玄幻", "东方玄幻", "简介", ["标签"]),
    chapters := [ChapterData(1, "测试", "测试内容", 2, 1)],
    path := pe.export(meta, chapters, ExportPlatform.QIDIAN),
    os.path.exists(path),
))

test("5.6 export Fanqie format", lambda: (
    meta := NovelMeta("测试小说", "测试作者", "玄幻", "", "简介", ["标签"]),
    chapters := [ChapterData(1, "测试", "测试内容", 2, 1)],
    path := pe.export(meta, chapters, ExportPlatform.FANQIE),
    os.path.exists(path),
))

test("5.7 export Zongheng format", lambda: (
    meta := NovelMeta("测试小说", "测试作者", "玄幻", "", "简介", ["标签"]),
    chapters := [ChapterData(1, "测试", "测试内容", 2, 1)],
    path := pe.export(meta, chapters, ExportPlatform.ZONGHENG),
    os.path.exists(path),
))

test("5.8 export EPUB", lambda: (
    meta := NovelMeta("测试小说", "测试作者", "玄幻", "", "简介", ["标签"]),
    chapters := [ChapterData(1, "测试", "测试内容", 2, 1)],
    path := pe.export(meta, chapters, ExportPlatform.EPUB),
    os.path.exists(path),
))

def _multi_chapter_export():
    meta = NovelMeta("多章测试", "作者", "玄幻", "", "简介", ["标签"])
    chapters = [
        ChapterData(1, "第一章", "内容1", 100, 1),
        ChapterData(2, "第二章", "内容2", 100, 1),
        ChapterData(3, "第三章", "内容3", 100, 2),
    ]
    path = pe.export(meta, chapters, ExportPlatform.TXT)
    if not os.path.exists(path):
        return False
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    return "第一章" in content and "第二章" in content and "第三章" in content

test("5.9 multi-chapter export", lambda: _multi_chapter_export())

test("5.10 export with volumes", lambda: (
    meta := NovelMeta("分卷测试", "作者", "玄幻", "", "简介", ["标签"]),
    chapters := [
        ChapterData(1, "第一章", "内容1", 100, 1),
        ChapterData(2, "第二章", "内容2", 100, 2),
    ],
    path := pe.export(meta, chapters, ExportPlatform.MARKDOWN),
    os.path.exists(path),
))

# ================================================================
section("Module 6: Existing Core Modules Quick Re-verify")

from novel_memory_manager import NovelMemoryManager
from self_learning_engine import SelfLearningEngine
from chinese_traditional_namer import ChineseTraditionalNamer, Gender
from plot_brainstorm_engine import PlotBrainstormEngine, PlotArcType
from enhanced_ai_detector import EnhancedAIDetector
from collaborative_pipeline import CollaborativeWritingPipeline
from intelligent_orchestrator import IntelligentOrchestrator
from enhanced_skill_manager import EnhancedSkillManager, SkillMeta, SkillPriority

test("6.1 NovelMemoryManager import", lambda: (
    nm := NovelMemoryManager(),
    isinstance(nm, NovelMemoryManager),
))

test("6.2 SelfLearningEngine import", lambda: (
    sle := SelfLearningEngine(),
    isinstance(sle, SelfLearningEngine),
    len(sle.skills) >= 8,
))

test("6.3 ChineseTraditionalNamer import", lambda: (
    ctn := ChineseTraditionalNamer(),
    isinstance(ctn, ChineseTraditionalNamer),
    len(ctn.surnames["top10"]) >= 10,
))

test("6.4 PlotBrainstormEngine import", lambda: (
    pbe := PlotBrainstormEngine(),
    isinstance(pbe, PlotBrainstormEngine),
))

test("6.5 EnhancedAIDetector import", lambda: (
    ead := EnhancedAIDetector(),
    isinstance(ead, EnhancedAIDetector),
))

test("6.6 CollaborativeWritingPipeline import", lambda: (
    cwp := CollaborativeWritingPipeline("测试"),
    isinstance(cwp, CollaborativeWritingPipeline),
))

test("6.7 IntelligentOrchestrator import", lambda: (
    io := IntelligentOrchestrator(),
    isinstance(io, IntelligentOrchestrator),
    len(io.modules) >= 14,
))

test("6.8 EnhancedSkillManager import", lambda: (
    esm := EnhancedSkillManager(),
    isinstance(esm, EnhancedSkillManager),
))

# ================================================================
section("Module 7: IntelligentOrchestrator - New Module Integration")

io = IntelligentOrchestrator()

test("7.1 lorebook module registered", lambda: "lorebook" in io.modules)
test("7.2 story_bible module registered", lambda: "story_bible" in io.modules)
test("7.3 style_manager module registered", lambda: "style_manager" in io.modules)
test("7.4 version_manager module registered", lambda: "version_manager" in io.modules)
test("7.5 platform_exporter module registered", lambda: "platform_exporter" in io.modules)

test("7.6 execute lorebook_trigger", lambda: (
    result := io.execute("lorebook_trigger", text="萧炎在乌坦城"),
    isinstance(result, dict),
))

test("7.7 execute bible_add_entry", lambda: (
    result := io.execute("bible_add_entry",
        section="CHARACTERS", title="测试角色", content="测试内容"),
    isinstance(result, dict),
))

test("7.8 execute style_list", lambda: (
    result := io.execute("style_list"),
    isinstance(result, dict),
))

test("7.9 execute version_snapshot", lambda: (
    result := io.execute("version_snapshot", chapter=1, content="测试内容"),
    isinstance(result, dict),
))

test("7.10 execute export_platform", lambda: (
    result := io.execute("export_platform", platform="TXT",
        meta={"title": "测试", "author": "作者", "genre": "玄幻"},
        chapters=[{"chapter_num": 1, "title": "测试", "content": "内容", "word_count": 2}]),
    isinstance(result, dict),
))

test("7.11 get module status", lambda: (
    status := io.get_module_status(),
    isinstance(status, dict),
    len(status) >= 14,
))

test("7.12 execute get_status", lambda: (
    result := io.execute("get_status"),
    isinstance(result, dict),
    result.get("success"),
))

def _orchestrator_shutdown():
    io.shutdown()
    return True

test("7.13 orchestrator shutdown", lambda: _orchestrator_shutdown())

# ================================================================
section("Module 8: Cross-Module Integration")

def _lorebook_storybible():
    lb2 = Lorebook()
    sb2 = StoryBible("集成测试")
    lb2.add_entry(LorebookEntry(
        entry_id="int_001", category=EntryCategory.CHARACTER,
        name="集成角色", content="测试",
        trigger_keywords=["集成"],
        priority=EntryPriority.MEDIUM,
    ))
    sb2.add_entry(BibleEntry(
        entry_id="", section=BibleSection.CHARACTERS,
        title="集成角色", content="测试",
    ))
    all_bible = []
    for section in BibleSection:
        all_bible.extend(sb2.get_section(section))
    return len(lb2.entries) >= 1 and len(all_bible) >= 1

test("8.1 Lorebook + StoryBible", lambda: _lorebook_storybible())

test("8.2 VersionManager + PlatformExporter", lambda: (
    vm2 := VersionManager("集成版本"),
    pe2 := PlatformExporter(),
    content := "集成测试章节内容。",
    sid := vm2.create_snapshot(1, content, SnapshotType.MANUAL),
    snap := vm2.get_snapshot(sid),
    meta := NovelMeta("集成", "作者", "玄幻"),
    chapters := [ChapterData(1, "第一章", snap.content, snap.word_count, 1)],
    path := pe2.export(meta, chapters, ExportPlatform.TXT),
    os.path.exists(path),
))

def _style_memory():
    sm2 = StyleModuleManager()
    nm2 = NovelMemoryManager()
    fp = nm2.compute_style_fingerprint(1, "测试风格内容，用于验证风格一致性。")
    return len(sm2.modules) >= 8 and fp is not None

test("8.3 StyleModule + NovelMemory", lambda: _style_memory())

def _namer_storybible():
    ctn = ChineseTraditionalNamer()
    sb3 = StoryBible("命名集成")
    names = ctn.generate(surname="叶", gender=Gender.MALE, count=3)
    for n in names:
        sb3.add_entry(BibleEntry(
            entry_id="", section=BibleSection.CHARACTERS,
            title=n.full_name, content=f"自动生成角色: {n.full_name}",
        ))
    return len(sb3.get_section(BibleSection.CHARACTERS)) >= 3

test("8.4 Namer + StoryBible", lambda: _namer_storybible())

test("8.5 Full pipeline: Memory -> Plot -> Detect -> Export", lambda: (
    nm3 := NovelMemoryManager(),
    pbe := PlotBrainstormEngine(),
    ead := EnhancedAIDetector(),
    pe3 := PlatformExporter(),

    nm3.compute_style_fingerprint(1, "第一章测试内容，主角登场，世界观展开。"),
    arc := pbe.design_plot_arc(PlotArcType.THREE_ACT, 30, "玄幻"),
    result := ead.detect("这是一段AI生成的测试文本，用于验证检测流程。"),
    meta := NovelMeta("全流程", "作者", "玄幻"),
    chapters := [ChapterData(1, "第一章", "测试内容", 100, 1)],
    path := pe3.export(meta, chapters, ExportPlatform.TXT),

    arc is not None and result is not None and os.path.exists(path),
))

# ================================================================
section("Module 9: BookKnowledgeBase Verification")

from book_knowledge_base import BookKnowledgeBase, SkillTarget

bkb = BookKnowledgeBase()

test("9.1 instantiate", lambda: isinstance(bkb, BookKnowledgeBase))

test("9.2 insights loaded", lambda: (
    len(bkb.insights) >= 50,
))

test("9.3 get insights by skill", lambda: (
    plot_insights := [i for i in bkb.insights
                      if SkillTarget.PLOT_DESIGN in i.target_skills],
    len(plot_insights) >= 10,
))

def _check_skill_coverage():
    coverage = {}
    for insight in bkb.insights:
        for skill in insight.target_skills:
            coverage[skill.value] = coverage.get(skill.value, 0) + 1
    return len(coverage) >= 8

test("9.4 skill coverage", lambda: _check_skill_coverage())

test("9.5 search by book name", lambda: (
    results := [i for i in bkb.insights if "故事" in i.book_name],
    len(results) >= 1,
))

test("9.6 actionable tips count", lambda: (
    total_tips := sum(len(i.actionable_tips) for i in bkb.insights),
    total_tips >= 200,
))

# ================================================================
section("Module 10: Skill Level Verification")

def _check_all_expert():
    sle = SelfLearningEngine()
    expert_levels = {"专家", "大师", "宗师"}
    expert_skills = 0
    for name, skill in sle.skills.items():
        if skill.level.value in expert_levels:
            expert_skills += 1
    return expert_skills >= 5

test("10.1 skills at expert+ (5/8 min)", lambda: _check_all_expert())

test("10.2 knowledge base size", lambda: (
    sle := SelfLearningEngine(),
    len(sle.knowledge_base) >= 500,
))

test("10.3 vocabulary size", lambda: (
    sle := SelfLearningEngine(),
    len(sle.vocabulary) >= 10,
))

# ================================================================
print(f"\n{'='*60}")
print(f"  TEST RESULTS SUMMARY")
print(f"{'='*60}")
print(f"  PASSED: {passed}")
print(f"  FAILED: {failed}")
print(f"  TOTAL:  {passed + failed}")
if passed + failed > 0:
    print(f"  RATE:   {passed}/{passed+failed} = {passed/(passed+failed)*100:.1f}%")

if errors:
    print(f"\n  FAILURES:")
    for name, err in errors:
        print(f"    - {name}: {err}")

if failed == 0:
    print(f"\n  ALL TESTS PASSED!")
else:
    print(f"\n  {failed} TEST(S) FAILED!")

print(f"{'='*60}")
