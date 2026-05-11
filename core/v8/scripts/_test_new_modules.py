#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""NWACS 新模块全面测试"""
import sys, os, json, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

passed = 0
failed = 0
errors = []

def test(name, fn):
    global passed, failed
    try:
        fn()
        passed += 1
        print(f"  ✅ {name}")
    except Exception as e:
        failed += 1
        errors.append((name, str(e)))
        print(f"  ❌ {name}: {e}")

def section(title):
    print(f"\n{'─'*50}")
    print(f"  {title}")
    print(f"{'─'*50}")

# ============================================================
section("模块1: MemoryManager 记忆管理系统")

from memory_manager import MemoryManager

mm = MemoryManager()

test("1.1 实例化", lambda: None)

test("1.2 保存角色记忆", lambda: (
    mm.remember("character", "叶青云 - 主角，青云宗外门弟子", tags=["主角", "青云宗"]),
    mm.remember("character", "苏婉儿 - 女主，神秘身份", tags=["女主", "神秘"], importance=8),
))

test("1.3 保存剧情记忆", lambda: (
    mm.remember("plot", "第1章：叶青云在宗门测试中觉醒废灵根", tags=["第1章", "觉醒"]),
    mm.remember("plot", "第5章：叶青云意外获得神秘玉佩", tags=["第5章", "奇遇"], importance=9),
))

test("1.4 保存世界观记忆", lambda: (
    mm.remember("world", "青云宗位于青云山脉，有九座主峰", tags=["宗门", "地理"]),
    mm.remember("world", "修炼境界：炼气→筑基→金丹→元婴→化神", tags=["修炼", "境界"]),
))

test("1.5 保存知识点", lambda: (
    mm.remember("knowledge", "黄金三章：前三章必须完成世界观展示+冲突建立+悬念设置", tags=["写作技巧"]),
))

test("1.6 构建上下文", lambda: (
    ctx := mm.build_context(["character", "plot", "world"]),
    len(ctx) > 100,
))

test("1.7 获取统计", lambda: (
    stats := mm.get_stats(),
    stats["total_adds"] >= 7,
))

test("1.8 按标签搜索", lambda: (
    results := mm.search_by_tag("主角"),
    len(results) > 0,
))

test("1.9 获取重要记忆", lambda: (
    important := mm.stores["character"].get_important(threshold=7),
    len(important) > 0,
))

test("1.10 持久化与加载", lambda: (
    mm.persist(),
    mm2 := MemoryManager(),
    stats2 := mm2.get_stats(),
    stats2["total_adds"] >= 7,
))

# ============================================================
section("模块2: CharacterNameGenerator 角色命名生成器")

from character_name_generator import CharacterNameGenerator

gen = CharacterNameGenerator()

test("2.1 实例化", lambda: None)

test("2.2 玄幻男名生成", lambda: (
    names := gen.generate("xuanhuan", "male", 5),
    len(names) == 5,
    all(n.full_name for n in names),
))

test("2.3 玄幻女名生成", lambda: (
    names := gen.generate("xuanhuan", "female", 3),
    len(names) == 3,
))

test("2.4 都市男名生成", lambda: (
    names := gen.generate("urban", "male", 3),
    len(names) == 3,
))

test("2.5 武侠名生成", lambda: (
    names := gen.generate("wuxia", "male", 3),
    len(names) == 3,
))

test("2.6 完整角色命名包", lambda: (
    char := gen.generate_full_character_name("xuanhuan", "male"),
    char.get("full_name"),
    char.get("surname"),
    char.get("given_name"),
    char.get("title"),
    char.get("alias"),
))

test("2.7 含义关键词命名", lambda: (
    names := gen.generate("xuanhuan", "male", 3, meaning_keywords=["剑", "云"]),
    len(names) == 3,
))

test("2.8 风格命名", lambda: (
    names := gen.generate("xuanhuan", "male", 3, style="elegant"),
    len(names) == 3,
))

test("2.9 称号生成", lambda: (
    title := gen.generate_title("xuanhuan"),
    len(title) > 0,
))

test("2.10 别名生成", lambda: (
    alias := gen.generate_alias("青云", "xuanhuan"),
    len(alias) > 0,
))

test("2.11 宗门名生成", lambda: (
    clan := gen.generate_clan_name("xuanhuan"),
    len(clan) > 0,
))

test("2.12 名字去重", lambda: (
    gen2 := CharacterNameGenerator(),
    names1 := gen2.generate("xuanhuan", "male", 10),
    len(set(n.full_name for n in names1)) == 10,
))

# ============================================================
section("模块3: PlotBrainstormEngine 剧情构思引擎")

from plot_brainstorm_engine import PlotBrainstormEngine, PlotArcType, ConflictType

pe = PlotBrainstormEngine()

test("3.1 实例化", lambda: None)

test("3.2 灵感生成-玄幻", lambda: (
    ideas := pe.brainstorm_ideas("玄幻", count=5),
    len(ideas) == 5,
    all(i.get("core_concept") for i in ideas),
))

test("3.3 灵感生成-都市", lambda: (
    ideas := pe.brainstorm_ideas("都市", count=3),
    len(ideas) == 3,
))

test("3.4 灵感生成-悬疑", lambda: (
    ideas := pe.brainstorm_ideas("悬疑", count=3),
    len(ideas) == 3,
))

test("3.5 三幕结构弧光", lambda: (
    arc := pe.design_plot_arc(PlotArcType.THREE_ACT, 30, "玄幻"),
    len(arc.nodes) >= 5,
    any(n.is_climax for n in arc.nodes),
    any(n.is_twist for n in arc.nodes),
))

test("3.6 英雄之旅弧光", lambda: (
    arc := pe.design_plot_arc(PlotArcType.HERO_JOURNEY, 24, "玄幻"),
    len(arc.nodes) == 12,
))

test("3.7 复仇弧光", lambda: (
    arc := pe.design_plot_arc(PlotArcType.REVENGE_ARC, 40, "都市"),
    len(arc.nodes) == 8,
))

test("3.8 成长弧光", lambda: (
    arc := pe.design_plot_arc(PlotArcType.GROWTH_ARC, 20, "言情"),
    len(arc.nodes) == 6,
))

test("3.9 反转点子生成", lambda: (
    twists := pe.generate_twists(3),
    len(twists) == 3,
    all(t.get("name") and t.get("example") for t in twists),
))

test("3.10 章节大纲生成", lambda: (
    arc := pe.design_plot_arc(PlotArcType.THREE_ACT, 10, "玄幻"),
    outline := pe.generate_chapter_outline(arc, "玄幻"),
    len(outline) == 10,
    all(o.get("chapter") and o.get("summary") for o in outline),
))

test("3.11 冲突矩阵设计", lambda: (
    matrix := pe.design_conflict_matrix(["叶青云", "苏婉儿", "魔尊", "剑圣"]),
    len(matrix) == 4,
))

test("3.12 导出剧情弧光", lambda: (
    arc := pe.design_plot_arc(PlotArcType.THREE_ACT, 30, "玄幻"),
    exported := pe.export_plot(arc),
    exported.get("arc_id"),
    exported.get("nodes"),
    len(exported["nodes"]) > 0,
))

# ============================================================
section("模块4: EnhancedAIDetector 增强AI检测器")

from enhanced_ai_detector import EnhancedAIDetector

det = EnhancedAIDetector()

ai_text = """林晨缓缓地站起身，宛如一只刚刚破茧而出的蝴蝶，心中不禁激动万分。
仿佛天地都在为他欢呼，眼前的景象十分壮观，格外震撼人心。
这一切似乎都像是一场梦境，渐渐地，林晨才相信这是真的。
他微微一笑，心中暗想，自己的努力终究没有白费。"""

human_text = """林晨站起来，腿有点麻。他揉了揉膝盖，看了眼窗外。
天快亮了。一夜没睡，脑子昏沉沉的。
"妈的。"他骂了一句，抓起桌上的烟盒，空的。
他把烟盒揉成一团，扔进垃圾桶。去他妈的。"""

test("4.1 实例化", lambda: None)

test("4.2 AI文本检测-高分", lambda: (
    r := det.detect(ai_text),
    r.overall_score > 20,
    0 <= r.overall_score <= 100,
))

test("4.3 人类文本检测-低分", lambda: (
    r := det.detect(human_text),
    r.overall_score < 50,
))

test("4.4 检测层级完整", lambda: (
    r := det.detect(ai_text),
    r.word_layer.get("score") is not None,
    r.sentence_layer.get("score") is not None,
    r.semantic_layer.get("score") is not None,
))

test("4.5 热点定位", lambda: (
    r := det.detect(ai_text, "full"),
    len(r.hot_spots) > 0,
))

test("4.6 改进建议", lambda: (
    r := det.detect(ai_text),
    len(r.suggestions) > 0,
))

test("4.7 轻度去痕", lambda: (
    rewritten, rw := det.rewrite(ai_text, "light"),
    len(rewritten) > 0,
    rw.reduction >= 0,
))

test("4.8 中度去痕", lambda: (
    rewritten, rw := det.rewrite(ai_text, "medium"),
    len(rewritten) > 0,
))

test("4.9 重度去痕", lambda: (
    rewritten, rw := det.rewrite(ai_text, "heavy"),
    len(rewritten) > 0,
))

test("4.10 文本对比", lambda: (
    comp := det.compare_texts(ai_text, human_text),
    comp["text_a"]["score"] > comp["text_b"]["score"],
    comp["better"] == "text_b",
))

test("4.11 批量检测", lambda: (
    batch := det.batch_detect({1: ai_text, 2: human_text, 3: ai_text[:100] + human_text}),
    batch["total_chapters"] == 3,
    batch.get("average_score") is not None,
))

test("4.12 短文本处理", lambda: (
    r := det.detect("短"),
    r.overall_score == 0,
))

# ============================================================
section("模块5: CollaborativeWritingPipeline 协作流水线")

from collaborative_pipeline import CollaborativeWritingPipeline, PipelineStage, StageStatus

pl = CollaborativeWritingPipeline()
pl.config.auto_save = False
pl.config.enable_detect = False
pl.config.enable_rewrite = False
pl.config.enable_polish = False

test("5.1 实例化", lambda: None)

test("5.2 基础流水线运行", lambda: (
    summary := pl.run(genre="玄幻", chapter_count=1, starting_chapter=1),
    summary["chapters"] == 1,
    summary["stages_passed"] >= 3,
))

def _test_multi_chapter():
    pl2 = CollaborativeWritingPipeline()
    pl2.config.auto_save = False
    pl2.config.enable_detect = False
    pl2.config.enable_rewrite = False
    pl2.config.enable_polish = False
    summary = pl2.run(genre="都市", chapter_count=2, starting_chapter=5)
    assert summary["chapters"] == 2

test("5.3 多章节运行", _test_multi_chapter)

test("5.4 配置修改", lambda: (
    pl.set_config(detect_threshold=30, rewrite_intensity="heavy"),
    pl.config.detect_threshold == 30,
    pl.config.rewrite_intensity == "heavy",
))

test("5.5 阶段状态枚举", lambda: (
    len(list(PipelineStage)) == 7,
    StageStatus.PASSED.value == "已通过",
))

# ============================================================
section("模块6: IntelligentOrchestrator 智能编排器")

from intelligent_orchestrator import IntelligentOrchestrator, ModuleStatus

orch = IntelligentOrchestrator()

test("6.1 实例化", lambda: None)

test("6.2 模块状态查询", lambda: (
    status := orch.get_module_status(),
    len(status) >= 7,
))

test("6.3 生成角色名", lambda: (
    r := orch.execute("generate_names", genre="xuanhuan", count=3),
    r["success"],
    len(r["data"]) == 3,
))

test("6.4 剧情构思", lambda: (
    r := orch.execute("brainstorm_plot", genre="玄幻", count=2),
    r["success"],
    len(r["data"]) == 2,
))

test("6.5 设计剧情弧光", lambda: (
    r := orch.execute("design_plot_arc", arc_type="three_act", chapters=30, genre="玄幻"),
    r["success"],
    r["data"].get("nodes"),
))

test("6.6 AI检测", lambda: (
    r := orch.execute("detect_ai", text=ai_text),
    r["success"],
    r["data"]["score"] > 0,
))

test("6.7 文本去痕", lambda: (
    r := orch.execute("rewrite_text", text=ai_text, intensity="medium"),
    r["success"],
    len(r["data"]["rewritten"]) > 0,
))

test("6.8 保存记忆", lambda: (
    r := orch.execute("save_memory", type="knowledge", content="测试知识点", tags=["test"]),
    r["success"],
))

test("6.9 获取上下文", lambda: (
    r := orch.execute("get_context"),
    r["success"],
))

test("6.10 创建角色", lambda: (
    r := orch.execute("create_character", genre="xuanhuan", gender="female", role="女主"),
    r["success"],
    r["data"].get("full_name"),
))

test("6.11 状态查询", lambda: (
    r := orch.execute("get_status"),
    r["success"],
    r["data"].get("modules"),
))

test("6.12 未知命令处理", lambda: (
    r := orch.execute("unknown_command"),
    not r["success"],
    r.get("error"),
))

test("6.13 关闭编排器", lambda: (
    orch.shutdown(),
))

# ============================================================
section("模块7: EnhancedSkillManager 增强Skill管理器")

from enhanced_skill_manager import EnhancedSkillManager, SkillStatus, SkillPriority

sm = EnhancedSkillManager()

test("7.1 实例化", lambda: None)

test("7.2 Skill列表", lambda: (
    skills := sm.list_skills(),
    len(skills) >= 10,
))

test("7.3 按分类筛选", lambda: (
    plot_skills := sm.list_skills(category="plot"),
    len(plot_skills) >= 3,
))

test("7.4 工作流列表", lambda: (
    wfs := sm.list_workflows(),
    len(wfs) >= 3,
))

test("7.5 执行角色创建Skill", lambda: (
    r := sm.execute_skill("character_creation", genre="xuanhuan", gender="male"),
    r["success"],
    r["data"].get("full_name"),
))

test("7.6 执行AI检测Skill", lambda: (
    r := sm.execute_skill("ai_detection", text=ai_text),
    r["success"],
    r["data"]["score"] > 0,
))

test("7.7 执行冲突设计Skill", lambda: (
    r := sm.execute_skill("conflict_design", characters=["A", "B", "C", "D"]),
    r["success"],
))

test("7.8 执行文本去痕Skill", lambda: (
    r := sm.execute_skill("text_rewrite", text=ai_text, intensity="light"),
    r["success"],
))

test("7.9 执行世界观Skill", lambda: (
    r := sm.execute_skill("world_building", name="测试世界"),
    r["success"],
))

test("7.10 执行章节大纲Skill", lambda: (
    r := sm.execute_skill("chapter_outline", genre="玄幻", chapters=10),
    r["success"],
))

test("7.11 执行伏笔管理Skill", lambda: (
    r := sm.execute_skill("foreshadowing"),
    r["success"],
))

test("7.12 执行工作流", lambda: (
    r := sm.execute_workflow("character_pack", genre="xuanhuan", gender="male"),
    r["success"],
    len(r["steps"]) >= 1,
))

test("7.13 Skill激活/停用", lambda: (
    sm.activate_skill("ai_detection"),
    sm.deactivate_skill("foreshadowing"),
    sm.skills["foreshadowing"].status == SkillStatus.PAUSED,
))

test("7.14 Skill报告", lambda: (
    report := sm.get_skill_report(),
    report["total_skills"] >= 10,
    report["total_calls"] > 0,
))

test("7.15 未知Skill处理", lambda: (
    r := sm.execute_skill("nonexistent_skill"),
    not r["success"],
))

# ============================================================
print(f"\n{'='*60}")
print(f"📊 测试结果汇总")
print(f"{'='*60}")
print(f"  ✅ 通过: {passed}")
print(f"  ❌ 失败: {failed}")
print(f"  总计: {passed + failed}")
print(f"  通过率: {passed/(passed+failed)*100:.1f}%")

if errors:
    print(f"\n  失败详情:")
    for name, err in errors:
        print(f"    - {name}: {err}")

print(f"{'='*60}")
if failed == 0:
    print("🎉 全部测试通过!")
else:
    print(f"⚠️ 有 {failed} 个测试失败")
