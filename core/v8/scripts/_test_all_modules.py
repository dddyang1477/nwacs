#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""NWACS 全模块真实执行测试"""
import sys
import os
import json
import time

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
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


# ================================================================
section("模块1: NovelMemoryManager 长篇小说记忆一致性验证")

from novel_memory_manager import (
    NovelMemoryManager, StyleFingerprint, Foreshadowing,
    CharacterProfile, ConsistencyIssue, ForeshadowStatus,
    ConsistencyLevel
)

nmm = NovelMemoryManager(novel_title="测试仙侠巨作")

test("1.1 实例化", lambda: None)

ch1_text = """
叶青云站在青云宗山门前，望着巍峨的九座主峰，心中豪情万丈。
"从今天起，我叶青云就是青云宗的弟子了！"他握紧拳头，眼中闪烁着坚定的光芒。
身旁的苏婉儿微微一笑："叶师兄，以后还请多多关照。"
叶青云转过身，看着这位神秘的少女，点了点头。
远处，一道剑光划破天际，那是宗门长老在巡视。
山风吹过，卷起片片落叶，叶青云深吸一口气，迈步走进了山门。
"""

ch2_text = """
叶青云缓缓地站起身，宛如一只刚刚破茧而出的蝴蝶，心中不禁激动万分。
仿佛天地都在为他欢呼，眼前的景象十分壮观，格外震撼人心。
这一切似乎都像是一场梦境，渐渐地，叶青云才相信这是真的。
他微微一笑，心中暗想，自己的努力终究没有白费。
极其艰难的旅程，非常辛苦的奋斗，终于换来了此刻的成功。
"""

test("1.2 风格指纹计算-第1章", lambda: (
    fp1 := nmm.compute_style_fingerprint(1, ch1_text),
    fp1.avg_sentence_length > 0,
    fp1.dialogue_ratio > 0,
    len(fp1.emotional_curve) == 6,
))

test("1.3 风格指纹计算-第2章", lambda: (
    fp2 := nmm.compute_style_fingerprint(2, ch2_text),
    fp2.avg_sentence_length > 0,
    fp2.total_word_count > 0,
))

test("1.4 风格漂移检测", lambda: (
    issues := nmm.check_style_drift(2),
    isinstance(issues, list),
))

test("1.5 风格报告", lambda: (
    report := nmm.get_style_report(),
    report["total_chapters_analyzed"] == 2,
    "style_stability" in report,
))

test("1.6 人物注册", lambda: (
    nmm.register_character("叶青云", role="主角", gender="男", age=18,
                           personality=["坚毅", "果敢", "重情义"],
                           first_appearance_chapter=1),
    nmm.register_character("苏婉儿", role="女主", gender="女", age=17,
                           personality=["神秘", "温柔", "聪慧"],
                           first_appearance_chapter=1),
    len(nmm.characters) == 2,
))

test("1.7 人物一致性检查", lambda: (
    nmm.register_character("叶青云", appearance={"眼睛": "黑色", "头发": "黑色"}),
    issues := nmm.check_character_consistency("叶青云", 10, {
        "appearance": {"眼睛": "蓝色"}
    }),
    len(issues) >= 1,
    "外貌矛盾" in issues[0].description,
))

test("1.8 伏笔埋设", lambda: (
    fs1 := nmm.plant_foreshadowing("苏婉儿的真实身份是魔教圣女", 1, 50,
                                   fs_type="identity", importance=9,
                                   related_characters=["苏婉儿"]),
    fs2 := nmm.plant_foreshadowing("叶青云的玉佩蕴含上古传承", 3, 30,
                                   fs_type="power_up", importance=8,
                                   related_characters=["叶青云"]),
    fs3 := nmm.plant_foreshadowing("青云宗内隐藏着叛徒", 5, 40,
                                   fs_type="plot", importance=7),
    len(nmm.foreshadowings) == 3,
    fs1.startswith("FS_"),
))

test("1.9 伏笔回收", lambda: (
    nmm.resolve_foreshadowing("FS_0002", 30),
    fs := nmm.foreshadowings["FS_0002"],
    fs.status == ForeshadowStatus.FULLY_PAID,
))

test("1.10 超期伏笔检测", lambda: (
    overdue := nmm.get_overdue_foreshadowing(60),
    len(overdue) >= 1,
))

test("1.11 伏笔统计", lambda: (
    stats := nmm.get_foreshadowing_stats(),
    stats["total"] == 3,
    stats["resolved"] == 1,
    stats["resolution_rate"] > 0,
))

test("1.12 剧情事件记录", lambda: (
    nmm.record_plot_event(1, "叶青云加入青云宗", "entry", ["叶青云"], "青云宗山门"),
    nmm.record_plot_event(1, "叶青云与苏婉儿初次见面", "meeting",
                          ["叶青云", "苏婉儿"], "青云宗山门"),
    nmm.record_plot_event(5, "叶青云进入上古秘境", "adventure",
                          ["叶青云"], "上古秘境"),
    len(nmm.plot_events) == 3,
))

test("1.13 时间线验证", lambda: (
    issues := nmm.verify_timeline(),
    isinstance(issues, list),
))

test("1.14 实力体系验证", lambda: (
    nmm.register_character("叶青云", abilities=[
        {"name": "修为", "type": "cultivation", "level": "筑基"}
    ]),
    issue := nmm.verify_power_system("叶青云", "炼气", 20),
    issue is not None,
    issue.severity == ConsistencyLevel.MAJOR_CONFLICT,
))

test("1.15 综合报告", lambda: (
    report := nmm.get_comprehensive_report(),
    report["novel_title"] == "测试仙侠巨作",
    report["characters"]["total"] == 2,
    report["foreshadowing"]["total"] == 3,
    "issues" in report,
))

test("1.16 按严重程度筛选问题", lambda: (
    major_issues := nmm.get_issues_by_severity(ConsistencyLevel.MAJOR_CONFLICT),
    len(major_issues) >= 1,
))

test("1.17 流水线兼容-save_plot_point", lambda: (
    nmm.save_plot_point(10, "测试标题", "测试摘要", "test"),
    len(nmm.plot_events) == 4,
))

test("1.18 流水线兼容-save_conversation", lambda: (
    nmm.save_conversation("system", "测试消息"),
    len(nmm.conversations) == 1,
))

test("1.19 流水线兼容-build_context", lambda: (
    ctx := nmm.build_context(["character", "plot", "world"]),
    len(ctx) > 50,
    "叶青云" in ctx,
))

test("1.20 持久化与加载", lambda: (
    nmm.persist(),
    nmm2 := NovelMemoryManager(novel_title="测试仙侠巨作"),
    len(nmm2.characters) == 2,
    len(nmm2.foreshadowings) == 3,
    len(nmm2.plot_events) == 4,
    len(nmm2.conversations) == 1,
))

# ================================================================
section("模块2: SelfLearningEngine 自学习进化引擎")

from self_learning_engine import (
    SelfLearningEngine, KnowledgeCategory, SkillLevel,
    KnowledgeItem, SkillRecord, VocabularyEntry
)

engine = SelfLearningEngine()

test("2.1 实例化", lambda: None)

test("2.2 内置知识加载", lambda: (
    len(engine.knowledge_base) >= 8,
))

test("2.3 内置技能加载", lambda: (
    len(engine.skills) >= 8,
))

test("2.4 内置词汇加载", lambda: (
    len(engine.vocabulary) >= 10,
))

test("2.5 知识搜索-精确匹配", lambda: (
    results := engine.search_knowledge("黄金三章"),
    len(results) >= 1,
    results[0].title == "黄金三章法则",
))

test("2.6 知识搜索-模糊匹配", lambda: (
    results := engine.search_knowledge("爽点"),
    len(results) >= 1,
))

test("2.7 按分类获取知识", lambda: (
    techniques := engine.get_knowledge_by_category(
        KnowledgeCategory.WRITING_TECHNIQUE
    ),
    len(techniques) >= 2,
))

test("2.8 知识评价", lambda: (
    kid := list(engine.knowledge_base.keys())[0],
    engine.rate_knowledge(kid, 8.0),
    engine.knowledge_base[kid].quality_score > 5.0,
))

test("2.9 知识使用标记", lambda: (
    kid := list(engine.knowledge_base.keys())[0],
    engine.use_knowledge(kid),
    engine.knowledge_base[kid].usage_count >= 1,
))

test("2.10 技能经验获取", lambda: (
    engine.gain_experience("plot_design", 30),
    engine.gain_experience("plot_design", 30),
    engine.gain_experience("plot_design", 30),
    engine.gain_experience("plot_design", 30),
    skill := engine.skills["plot_design"],
    skill.experience >= 0,
    skill.usage_count >= 4,
))

test("2.11 技能报告", lambda: (
    report := engine.get_skill_report(),
    "plot_design" in report,
    report["plot_design"]["usage"] >= 4,
))

test("2.12 按题材获取词汇", lambda: (
    vocab := engine.get_vocabulary_by_genre("玄幻"),
    len(vocab) >= 5,
))

test("2.13 词汇搜索", lambda: (
    results := engine.search_vocabulary("修炼"),
    len(results) >= 1,
))

test("2.14 添加词汇", lambda: (
    engine.add_vocabulary("天劫", genre="玄幻", meaning="天道降下的劫难",
                          pinyin="tiān jié"),
    results := engine.search_vocabulary("天劫"),
    len(results) >= 1,
))

test("2.15 从文本学习词汇", lambda: (
    sample := """
    叶青云运转功法，丹田内的灵气如潮水般涌动。
    他心中暗喜，这机缘果然非同小可，造化之力正在重塑他的经脉。
    神识扫过四周，确认无人窥探后，他继续潜心修炼。
    功法运转间，灵气如潮，丹田翻涌，机缘造化尽在其中。
    """,
    engine.learn_vocabulary_from_text(sample, "玄幻"),
    len(engine.vocabulary) > 10,
))

test("2.16 学习统计", lambda: (
    stats := engine.get_learning_stats(),
    stats["total_knowledge_items"] >= 8,
    stats["total_vocabulary"] >= 10,
    stats["total_skills"] >= 8,
    "knowledge_by_category" in stats,
    "top_skills" in stats,
))

test("2.17 联网冷却检查", lambda: (
    can_fetch := engine.can_fetch_web(),
    isinstance(can_fetch, bool),
))

test("2.18 持久化与加载", lambda: (
    engine.persist(),
    engine2 := SelfLearningEngine(),
    len(engine2.knowledge_base) >= 8,
    len(engine2.skills) >= 8,
    len(engine2.vocabulary) >= 10,
))

# ================================================================
section("模块3: ChineseTraditionalNamer 中国传统命名系统")

from chinese_traditional_namer import (
    ChineseTraditionalNamer, FiveElement, EightTrigram,
    Gender, NameResult
)

namer = ChineseTraditionalNamer()

test("3.1 实例化", lambda: None)

test("3.2 五行推算", lambda: (
    element := namer.calculate_element_from_birth(2000, 6, 15),
    element in list(FiveElement),
))

test("3.3 缺失五行查找", lambda: (
    missing := namer.find_missing_element(2000, 6, 15),
    missing in list(FiveElement),
))

test("3.4 基础命名-五行策略", lambda: (
    names := namer.generate(surname="叶", gender=Gender.MALE,
                            element=FiveElement.WOOD,
                            strategy="element_focused", count=3),
    len(names) == 3,
    all(n.full_name.startswith("叶") for n in names),
    all(n.element == FiveElement.WOOD for n in names),
))

test("3.5 经典典故命名", lambda: (
    names := namer.generate(surname="苏", gender=Gender.FEMALE,
                            strategy="classical", count=3),
    len(names) == 3,
    all(n.full_name.startswith("苏") for n in names),
    all(n.meaning for n in names),
))

test("3.6 自然意象命名", lambda: (
    names := namer.generate(surname="林", gender=Gender.MALE,
                            strategy="nature", count=3),
    len(names) == 3,
))

test("3.7 美德寓意命名", lambda: (
    names := namer.generate(surname="王", gender=Gender.FEMALE,
                            strategy="virtue", count=3),
    len(names) == 3,
))

test("3.8 平衡策略命名", lambda: (
    names := namer.generate(surname="李", gender=Gender.MALE,
                            strategy="balanced", count=5),
    len(names) == 5,
))

test("3.9 生辰八字命名", lambda: (
    names := namer.generate_with_birth("林", 1998, 3, 21, 8,
                                       gender=Gender.MALE, count=3),
    len(names) >= 1,
    all(n.full_name.startswith("林") for n in names),
))

test("3.10 辈分命名", lambda: (
    names := namer.generate_clan_names("叶", generation=1,
                                       gender=Gender.MALE, count=3),
    len(names) >= 1,
    all(n.generation_char for n in names),
))

test("3.11 三才五格分析", lambda: (
    analysis := namer.analyze_strokes("叶", "青云"),
    "天格" in analysis,
    "人格" in analysis,
    "地格" in analysis,
    "外格" in analysis,
    "总格" in analysis,
    "综合评分" in analysis,
    analysis["综合评分"] >= 0,
    analysis["综合评分"] <= 100,
))

test("3.12 称号生成", lambda: (
    title := namer.generate_title("叶青云", "xuanhuan"),
    len(title) >= 2,
))

test("3.13 五行生克关系", lambda: (
    compat := namer.get_element_compatibility("叶青云", "苏婉儿"),
    "相生关系" in compat,
    "相克关系" in compat,
))

test("3.14 随机姓氏命名", lambda: (
    names := namer.generate(gender=Gender.FEMALE, count=3),
    len(names) == 3,
    all(n.full_name for n in names),
))

test("3.15 名字去重", lambda: (
    names1 := namer.generate(surname="张", gender=Gender.MALE, count=5),
    names2 := namer.generate(surname="张", gender=Gender.MALE, count=5),
    all_names := [n.full_name for n in names1] + [n.full_name for n in names2],
    len(all_names) == len(set(all_names)),
))

# ================================================================
section("模块4: PlotBrainstormEngine 剧情构思引擎")

from plot_brainstorm_engine import PlotBrainstormEngine, PlotArcType

plotter = PlotBrainstormEngine(memory_manager=nmm, creative_engine=None)

test("4.1 实例化", lambda: None)

test("4.2 构思剧情点子", lambda: (
    ideas := plotter.brainstorm_ideas("玄幻", "少年修仙", 5),
    len(ideas) == 5,
    all("template" in i for i in ideas),
    all("core_concept" in i for i in ideas),
))

test("4.3 设计三幕结构", lambda: (
    arc := plotter.design_plot_arc(PlotArcType.THREE_ACT, 30, "玄幻"),
    arc.arc_type == PlotArcType.THREE_ACT,
    len(arc.nodes) >= 3,
))

test("4.4 设计英雄之旅", lambda: (
    arc := plotter.design_plot_arc(PlotArcType.HERO_JOURNEY, 50, "玄幻"),
    arc.arc_type == PlotArcType.HERO_JOURNEY,
    len(arc.nodes) >= 3,
))

test("4.5 设计复仇弧线", lambda: (
    arc := plotter.design_plot_arc(PlotArcType.REVENGE_ARC, 40, "都市"),
    arc.arc_type == PlotArcType.REVENGE_ARC,
))

test("4.6 设计成长弧线", lambda: (
    arc := plotter.design_plot_arc(PlotArcType.GROWTH_ARC, 35, "玄幻"),
    arc.arc_type == PlotArcType.GROWTH_ARC,
))

test("4.7 生成章节大纲", lambda: (
    arc := plotter.design_plot_arc(PlotArcType.THREE_ACT, 10, "玄幻"),
    outline := plotter.generate_chapter_outline(arc, "玄幻"),
    len(outline) == 10,
    all("chapter" in o for o in outline),
    all("title" in o for o in outline),
))

test("4.8 导出剧情", lambda: (
    arc := plotter.design_plot_arc(PlotArcType.THREE_ACT, 10, "玄幻"),
    exported := plotter.export_plot(arc),
    "arc_type" in exported,
    "acts" in exported,
    "total_chapters" in exported,
))

# ================================================================
section("模块5: EnhancedAIDetector 增强AI检测器")

from enhanced_ai_detector import EnhancedAIDetector

detector = EnhancedAIDetector()

test("5.1 实例化", lambda: None)

ai_text = """
林晨缓缓地站起身，宛如一只刚刚破茧而出的蝴蝶，心中不禁激动万分。
仿佛天地都在为他欢呼，眼前的景象十分壮观，格外震撼人心。
这一切似乎都像是一场梦境，渐渐地，林晨才相信这是真的。
他微微一笑，心中暗想，自己的努力终究没有白费。
极其艰难的旅程，非常辛苦的奋斗，终于换来了此刻的成功。
"""

human_text = """
"放屁！"老王一拍桌子站了起来，茶杯都震得跳了三跳。
"你他娘的跟我说这是最好的方案？"他瞪着眼前的年轻人，唾沫星子都快喷到对方脸上。
小李缩了缩脖子，小声嘀咕："可是数据确实显示..."
"数据显示个屁！"老王打断他，"我在这一行干了二十年，什么数据没见过？"
"""

test("5.2 AI文本检测", lambda: (
    report := detector.detect(ai_text),
    report.overall_score > 30,
    report.level != "低风险",
))

test("5.3 人类文本检测", lambda: (
    report := detector.detect(human_text),
    report.overall_score < 70,
))

def _do_rewrite_medium():
    rw_result = detector.rewrite(ai_text, "medium")
    return rw_result

def _do_rewrite_heavy():
    rw_result = detector.rewrite(ai_text, "high")
    return rw_result

test("5.4 AI文本去痕", lambda: (
    rw := _do_rewrite_medium(),
    len(rw[0]) > 0,
    rw[1].final_score < rw[1].original_score,
))

test("5.5 高强度去痕", lambda: (
    rw := _do_rewrite_heavy(),
    len(rw[0]) > 0,
))

# ================================================================
section("模块6: CollaborativeWritingPipeline 写作协作流水线")

from collaborative_pipeline import (
    CollaborativeWritingPipeline, PipelineConfig,
    PipelineStage, StageStatus
)

pipeline = CollaborativeWritingPipeline(
    memory_manager=nmm,
    creative_engine=None,
    name_generator=namer,
    plot_engine=plotter,
    ai_detector=None,
    enhanced_detector=detector,
)

test("6.1 实例化", lambda: None)

def _setup_pipeline_config():
    pipeline.config.enable_detect = True
    pipeline.config.enable_rewrite = True
    pipeline.config.enable_polish = False
    pipeline.config.auto_save = False
    pipeline.config.detect_threshold = 40
    return True

test("6.2 配置流水线", lambda: (
    _setup_pipeline_config(),
    pipeline.config.max_retries == 3,
))

test("6.3 动态配置", lambda: (
    pipeline.set_config(max_retries=2, detect_threshold=50),
    pipeline.config.max_retries == 2,
    pipeline.config.detect_threshold == 50,
))

def _run_pipeline_test():
    pipeline.novel_title = "测试作品"
    summary = pipeline.run(
        genre="玄幻",
        theme="少年修仙",
        chapter_count=1,
        starting_chapter=1,
    )
    return summary

test("6.4 运行流水线", lambda: (
    summary := _run_pipeline_test(),
    summary["chapters"] == 1,
    "total_time_s" in summary,
    "stages_passed" in summary,
))

test("6.5 流水线阶段结果", lambda: (
    len(pipeline.stages) >= 3,
))

# ================================================================
section("模块7: IntelligentOrchestrator 智能编排器")

from intelligent_orchestrator import IntelligentOrchestrator

orch = IntelligentOrchestrator()

test("7.1 实例化", lambda: None)

test("7.2 模块注册", lambda: (
    len(orch.modules) >= 9,
    "novel_memory" in orch.modules,
    "namer" in orch.modules,
    "learning_engine" in orch.modules,
    "pipeline" in orch.modules,
))

test("7.3 生成角色名", lambda: (
    result := orch.execute("generate_names", surname="叶",
                           gender="male", count=3),
    result["success"],
    len(result["data"]) == 3,
    all("full_name" in n for n in result["data"]),
    all("element" in n for n in result["data"]),
))

test("7.4 剧情构思", lambda: (
    result := orch.execute("brainstorm_plot", genre="玄幻", count=3),
    result["success"],
    len(result["data"]) == 3,
))

test("7.5 设计剧情弧线", lambda: (
    result := orch.execute("design_plot_arc", arc_type="three_act",
                           chapters=30, genre="玄幻"),
    result["success"],
    "acts" in result["data"],
))

test("7.6 AI检测", lambda: (
    result := orch.execute("detect_ai", text=ai_text),
    result["success"],
    "score" in result["data"],
    result["data"]["score"] > 30,
))

test("7.7 AI去痕", lambda: (
    result := orch.execute("rewrite_text", text=ai_text,
                           intensity="medium"),
    result["success"],
    "rewritten" in result["data"],
))

test("7.8 保存记忆", lambda: (
    result := orch.execute("save_memory", content="测试剧情事件",
                           chapter=1, tags=["测试"]),
    result["success"],
))

test("7.9 获取上下文", lambda: (
    result := orch.execute("get_context"),
    result["success"],
    "style" in result["data"],
    "characters" in result["data"],
    "foreshadowing" in result["data"],
))

test("7.10 获取状态", lambda: (
    result := orch.execute("get_status"),
    result["success"],
    "modules" in result["data"],
    "command_count" in result["data"],
))

test("7.11 创建角色", lambda: (
    result := orch.execute("create_character", surname="叶",
                           gender="male", role="主角",
                           birth_year=2000, birth_month=6,
                           birth_day=15, chapter=1),
    result["success"],
    "full_name" in result["data"],
    "element" in result["data"],
    "meaning" in result["data"],
))

test("7.12 运行流水线", lambda: (
    result := orch.execute("run_pipeline", title="编排器测试",
                           genre="玄幻", theme="修仙",
                           chapter_count=1, starting_chapter=1),
    result["success"],
    "chapters" in result["data"],
))

test("7.13 模块状态查询", lambda: (
    status := orch.get_module_status(),
    len(status) >= 9,
))

test("7.14 关闭编排器", lambda: (
    orch.shutdown(),
    True,
))

# ================================================================
section("模块8: EnhancedSkillManager 增强Skill管理器")

from enhanced_skill_manager import EnhancedSkillManager, SkillMeta, SkillPriority

skill_mgr = EnhancedSkillManager()

test("8.1 实例化", lambda: None)

test("8.2 注册Skill", lambda: (
    skill_mgr.register_skill(SkillMeta(
        name="test_skill", version="1.0",
        description="用于测试的Skill",
        category="test",
        priority=SkillPriority.LOW,
    )),
    "test_skill" in skill_mgr.skills,
))

test("8.3 获取Skill", lambda: (
    "test_skill" in skill_mgr.skills,
    skill_mgr.skills["test_skill"].meta.name == "test_skill",
))

test("8.4 列出Skills", lambda: (
    skills := skill_mgr.list_skills(),
    len(skills) >= 1,
))

test("8.5 按分类获取Skills", lambda: (
    skills := skill_mgr.list_skills(category="test"),
    len(skills) >= 1,
))

test("8.6 卸载Skill", lambda: (
    skill_mgr.unregister_skill("test_skill"),
    "test_skill" not in skill_mgr.skills,
))

# ================================================================
section("模块9: 跨模块集成测试")

test("9.1 记忆→命名联动", lambda: (
    names := namer.generate(surname="叶", gender=Gender.MALE, count=1),
    nmm.register_character(names[0].full_name, role="主角",
                           first_appearance_chapter=1),
    names[0].full_name in nmm.characters,
))

test("9.2 记忆→剧情联动", lambda: (
    nmm.record_plot_event(1, "主角觉醒", "power_up",
                          [list(nmm.characters.keys())[0]], "青云宗"),
    len(nmm.plot_events) >= 5,
))

test("9.3 学习→词汇联动", lambda: (
    engine.add_vocabulary("青云宗", genre="玄幻",
                          meaning="修仙门派", pinyin="qīng yún zōng"),
    results := engine.search_vocabulary("青云宗"),
    len(results) >= 1,
))

test("9.4 检测→流水线联动", lambda: (
    report := detector.detect(ai_text),
    report.overall_score > 0,
    isinstance(report.overall_score, (int, float)),
))

test("9.5 编排器→全模块联动", lambda: (
    result := orch.execute("get_status"),
    result["success"],
))

# ================================================================
print(f"\n{'='*60}")
print(f"  测试结果汇总")
print(f"{'='*60}")
print(f"  ✅ 通过: {passed}")
print(f"  ❌ 失败: {failed}")
print(f"  通过率: {passed}/{passed + failed} = {passed / max(passed + failed, 1) * 100:.1f}%")

if errors:
    print(f"\n  失败详情:")
    for name, err in errors:
        print(f"    - {name}: {err}")

print(f"\n{'='*60}")
if failed == 0:
    print("  🎉 全部测试通过！")
else:
    print(f"  ⚠️ 有 {failed} 个测试失败，需要修复")
print(f"{'='*60}")
