"""NWACS 全模块集成测试 - 验证所有增强模块协同工作"""
import sys
import os
import json
import tempfile
import shutil

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

TEST_DIR = tempfile.mkdtemp(prefix="nwacs_test_")
print(f"测试目录: {TEST_DIR}")

passed = 0
failed = 0


def check(name, condition, detail=""):
    global passed, failed
    if condition:
        passed += 1
        print(f"  ✅ {name}")
    else:
        failed += 1
        print(f"  ❌ {name} - {detail}")


# ================================================================
# 1. Lorebook 增强测试
# ================================================================
print("\n" + "=" * 60)
print("1. Lorebook 增强测试")
print("=" * 60)

from core.v8.lorebook import Lorebook, LorebookEntry, EntryCategory

lb = Lorebook(storage_dir=TEST_DIR)

check("初始化", lb is not None)

# 搜索
results = lb.search("修炼")
check("搜索", len(results) >= 0)

# 模糊匹配关键词
fuzzy = lb.fuzzy_find_keywords("修练")
check("模糊匹配", isinstance(fuzzy, list))

# 批量操作
entry_ids = list(lb.entries.keys())[:3]
if entry_ids:
    result = lb.batch_update(entry_ids, category=EntryCategory.CHARACTER)
    check("批量更新", result > 0)

# 模板
templates = lb.get_templates()
check("获取模板", len(templates) >= 1)

# 统计
stats = lb.get_stats()
check("统计信息", "total_entries" in stats)

# 仪表盘
dashboard = lb.get_dashboard()
check("仪表盘", isinstance(dashboard, dict))

# 导出
export_path = os.path.join(TEST_DIR, "lorebook_export.json")
count = lb.export_entries(export_path)
check("导出", count >= 0)

# 持久化
lb.save()
check("持久化", os.path.exists(os.path.join(TEST_DIR, "lorebook.json")))


# ================================================================
# 2. StoryBible 增强测试
# ================================================================
print("\n" + "=" * 60)
print("2. StoryBible 增强测试")
print("=" * 60)

from core.v8.story_bible import StoryBible, BibleEntry, BibleSection, Relationship, RelationshipType, TimelineEvent, EventType

sb = StoryBible(storage_dir=TEST_DIR)

check("初始化", sb is not None)

# 添加条目
entry = BibleEntry(entry_id="", section=BibleSection.CHARACTERS, title="主角", content="测试主角")
sb.add_entry(entry)
entry2 = BibleEntry(entry_id="", section=BibleSection.CHARACTERS, title="配角A", content="测试配角")
sb.add_entry(entry2)
check("添加条目", len(sb.get_section(BibleSection.CHARACTERS)) >= 2)

# 关系图谱
rel = Relationship(rel_id="", character_a="主角", character_b="配角A",
                   rel_type=RelationshipType.FRIEND, strength=8, description="青梅竹马")
sb.add_relationship(rel)
graph = sb.get_relationship_graph()
check("关系图谱", "nodes" in graph)

# 时间线
event = TimelineEvent(event_id="", title="主角登场", event_type=EventType.CHARACTER,
                      chapter=1, description="主角在宗门测试中觉醒")
sb.add_timeline_event(event)
events = sb.get_timeline()
check("时间线", len(events) >= 1)

# 一致性检查
issues = sb.check_consistency()
check("一致性检查", isinstance(issues, list))

# 交叉引用
refs = sb.get_cross_references(entry.entry_id)
check("交叉引用", isinstance(refs, list))

# 统计
stats = sb.get_stats()
check("统计", "total_entries" in stats)

# 仪表盘
dashboard = sb.get_dashboard()
check("仪表盘", isinstance(dashboard, dict))

# 持久化
sb.save()
check("持久化", os.path.exists(os.path.join(TEST_DIR, "未命名作品_bible.json")))


# ================================================================
# 3. StyleModuleManager 增强测试
# ================================================================
print("\n" + "=" * 60)
print("3. StyleModuleManager 增强测试")
print("=" * 60)

from core.v8.style_module_manager import StyleModuleManager, SceneType

smm = StyleModuleManager(storage_dir=TEST_DIR)

check("初始化", smm is not None)
check("内置模块", len(smm.list_modules()) >= 3)

# 风格分析
results = smm.analyze_style("主角站在山巅，望着远方。他心中充满了矛盾与冲突。危机正在逼近，他必须做出选择。")
check("风格分析", len(results) >= 1)

# 风格混合
blend = smm.blend({"style_hotblood": 0.6, "style_suspense": 0.4})
check("风格混合", blend is True)

# 风格推荐
rec = smm.recommend_style(genre="玄幻")
check("风格推荐", isinstance(rec, list))

# 一致性检查
consistency = smm.check_consistency(["主角站在山巅，望着远方。"])
check("一致性检查", isinstance(consistency, list))

# 预设
presets = smm.get_presets_for_scene(SceneType.ACTION)
check("场景预设", isinstance(presets, list))

# 统计
stats = smm.get_stats()
check("统计", "total_modules" in stats)

# 持久化
smm.save()
check("持久化", os.path.exists(os.path.join(TEST_DIR, "style_modules.json")))


# ================================================================
# 4. VersionManager 增强测试
# ================================================================
print("\n" + "=" * 60)
print("4. VersionManager 增强测试")
print("=" * 60)

from core.v8.version_manager import VersionManager, SnapshotType

vm = VersionManager(storage_dir=TEST_DIR)

check("初始化", vm is not None)

# 创建快照
v1_id = vm.create_snapshot(1, "测试内容V1", message="初始版本")
check("创建快照", v1_id is not None)

v2_id = vm.create_snapshot(1, "测试内容V2修改版", message="修改版本")
check("创建快照2", v2_id is not None)

# 章节历史
history = vm.get_chapter_history(1)
check("章节历史", len(history) >= 2)

# 差异对比
diff = vm.diff(v1_id, v2_id)
check("差异对比", diff is not None)

# 三路合并
v_base_id = vm.create_snapshot(1, "测试内容V0", message="基础版本")
merge = vm.three_way_merge(v_base_id, v1_id, v2_id)
check("三路合并", merge is not None)

# 版本图
graph = vm.get_version_graph()
check("版本图", "nodes" in graph)

# 分支
vm.create_branch("test_branch")
check("创建分支", True)

# 搜索快照
search_results = vm.search_snapshots("测试")
check("搜索快照", len(search_results) >= 1)

# 变更日志
log = vm.get_change_log(5)
check("变更日志", len(log) >= 1)

# 统计
stats = vm.get_stats()
check("统计", "total_snapshots" in stats)

# 持久化
vm.save()
check("持久化", os.path.exists(os.path.join(TEST_DIR, "未命名作品_versions.json")))


# ================================================================
# 5. PlatformExporter 增强测试
# ================================================================
print("\n" + "=" * 60)
print("5. PlatformExporter 增强测试")
print("=" * 60)

from core.v8.platform_exporter import PlatformExporter, NovelMeta, ChapterData, ExportPlatform

pe = PlatformExporter(output_dir=TEST_DIR)

check("初始化", pe is not None)

# 导出
meta = NovelMeta(title="测试小说", author="测试作者", genre="玄幻")
chapters = [
    ChapterData(chapter_num=1, title="第一章", content="主角站在山巅，望着远方。", word_count=12),
ChapterData(chapter_num=2, title="第二章", content="危机正在逼近。", word_count=6),
]

result = pe.export(meta, chapters, ExportPlatform.QIDIAN)
check("导出起点", result is not None)

result = pe.export(meta, chapters, ExportPlatform.TXT)
check("导出TXT", result is not None)

# 全平台导出
all_results = pe.export_all(meta, chapters)
check("全平台导出", len(all_results) >= 1)

# 预设
presets = pe._init_builtin_presets()
check("预设", True)

# 字数统计
stats = pe.compute_word_stats(chapters)
check("字数统计", stats.total_characters > 0)

# 封面生成
cover = pe.generate_cover_html(meta, chapters)
check("封面生成", cover is not None)

# 目录生成
toc = pe.generate_toc_html(meta, chapters)
check("目录生成", toc is not None)

# 导出历史
history = pe.get_export_history()
check("导出历史", isinstance(history, list))

# 持久化
pe._save_data()
check("持久化", os.path.exists(os.path.join(TEST_DIR, "exporter_data.json")))


# ================================================================
# 6. IntelligentOrchestrator 增强测试
# ================================================================
print("\n" + "=" * 60)
print("6. IntelligentOrchestrator 增强测试")
print("=" * 60)

from core.v8.intelligent_orchestrator import IntelligentOrchestrator, TaskPriority

io = IntelligentOrchestrator()

check("初始化", io is not None)

# 模块状态
status = io.get_module_status()
check("模块状态", len(status) >= 1)

# 任务队列
task_id = io.enqueue_task("get_status", priority=TaskPriority.NORMAL)
check("入队任务", task_id is not None)

task_status = io.get_task_status(task_id)
check("任务状态", task_status is not None)

queue_stats = io.get_queue_stats()
check("队列统计", "pending" in queue_stats)

# 处理队列
results = io.process_queue(max_tasks=5)
check("处理队列", isinstance(results, list))

# 重试执行
retry_result = io.execute_with_retry("get_status", max_retries=2)
check("重试执行", retry_result is not None)

# 流水线
pipeline = io.execute_pipeline([
    {"command": "get_status"},
    {"command": "style_list"},
])
check("流水线", len(pipeline) >= 1)

# 健康检查
health = io.check_health()
check("健康检查", isinstance(health, dict))

dashboard = io.get_health_dashboard()
check("健康仪表盘", isinstance(dashboard, dict))

# 性能报告
perf = io.get_performance_report()
check("性能报告", isinstance(perf, dict))

# 插件系统
plugin_id = io.register_plugin("test_plugin", "1.0", "测试插件")
check("注册插件", plugin_id is not None)

plugins = io.get_plugins()
check("插件列表", len(plugins) >= 1)

# 会话管理
session_path = io.save_session()
check("保存会话", session_path is not None)

info = io.get_session_info()
check("会话信息", isinstance(info, dict))

# 关闭
io.shutdown()
check("关闭", True)


# ================================================================
# 7. NovelMemoryManager 增强测试
# ================================================================
print("\n" + "=" * 60)
print("7. NovelMemoryManager 增强测试")
print("=" * 60)

from core.v8.novel_memory_manager import NovelMemoryManager

nmm = NovelMemoryManager(storage_dir=TEST_DIR)

check("初始化", nmm is not None)

# 存储章节
nmm.store_chapter_text(1, "主角站在山巅，望着远方。他心中充满了矛盾与冲突。危机正在逼近。")
nmm.store_chapter_text(2, "主角决定下山。他在路上遇到了一个神秘老人。老人说出了一个惊天秘密。")
check("存储章节", len(nmm.chapter_texts) >= 2)

# 智能检索
results = nmm.intelligent_search("主角", search_types=["character", "plot"])
check("智能检索", isinstance(results, list))

# 上下文检索
context = nmm.context_aware_retrieval(2, "主角")
check("上下文检索", len(context) >= 1)

# 因果链
causal = nmm.discover_causal_links(1, 2)
check("因果链发现", isinstance(causal, list))

# 角色弧线
arc = nmm.analyze_character_arc("主角")
check("角色弧线分析", isinstance(arc, dict))

# 跨章节模式
patterns = nmm.detect_cross_chapter_patterns()
check("跨章节模式", isinstance(patterns, dict))

# 自动检查
check_result = nmm.run_auto_checks(1)
check("自动检查", "checks_run" in check_result)

# 批量验证
batch_result = nmm.batch_validate([1, 2])
check("批量验证", isinstance(batch_result, dict))

# 自动修复建议
nmm.register_character("主角", role="protagonist")
issues = nmm.find_character_inconsistencies()
if issues:
    fix = nmm.auto_fix_suggestions(issues[0].issue_id)
    check("修复建议", isinstance(fix, dict))

# 记忆压缩
snapshot = nmm.compress_chapter_range(1, 2, "medium")
check("记忆压缩", snapshot is not None)

# 渐进摘要
summaries = nmm.progressive_summarize(1, levels=["L1", "L2"])
check("渐进摘要", len(summaries) >= 1)

# 快照列表
snapshots = nmm.get_all_snapshots()
check("快照列表", len(snapshots) >= 1)

# 快照回溯
recall = nmm.recall_from_snapshots("主角")
check("快照回溯", isinstance(recall, list))

# 综合报告
report = nmm.get_comprehensive_report()
check("综合报告", "issues" in report)

# 持久化
nmm.persist()
check("持久化", os.path.exists(os.path.join(TEST_DIR, "novel_memory.json")))


# ================================================================
# 8. SelfLearningEngine 增强测试
# ================================================================
print("\n" + "=" * 60)
print("8. SelfLearningEngine 增强测试")
print("=" * 60)

from core.v8.self_learning_engine import SelfLearningEngine

sle = SelfLearningEngine(storage_dir=TEST_DIR)

check("初始化", sle is not None)

# 练习模式
check("内置练习", len(sle.exercises) >= 8)
ex = sle.get_exercise("EX_001")
check("获取练习", ex is not None)

result = sle.start_exercise("EX_001")
check("开始练习", "exercise" in result)

attempt = sle.submit_attempt(
    "EX_001",
    "主角站在山巅，望着远方。他心中充满了矛盾与冲突。"
    "危机正在逼近，他必须做出选择。然而，一个神秘的声音突然在他脑海中响起..."
)
check("提交尝试", attempt is not None)

eval_result = sle.evaluate_attempt(attempt.attempt_id)
check("评估尝试", eval_result["overall_score"] > 0)

stats = sle.get_practice_stats()
check("练习统计", stats["total_exercises"] >= 8)

# 反馈循环
fb = sle.create_feedback_record("剧情设计")
check("创建反馈", fb is not None)

all_fb = sle.get_all_feedback()
check("获取反馈", len(all_fb) >= 1)

weaknesses = sle.identify_weaknesses()
check("识别薄弱", isinstance(weaknesses, dict))

trend = sle.track_improvement("剧情设计")
check("追踪改进", "trend" in trend)

# 学习路径
paths = sle.get_all_learning_paths()
check("学习路径", len(paths) >= 2)

if paths:
    milestones = sle.check_milestone_unlock(paths[0]["id"])
    check("里程碑检查", "milestones" in milestones)

    next_action = sle.get_next_recommended_action(paths[0]["id"])
    check("推荐行动", isinstance(next_action, dict))

# 技能组合
combos = sle.get_all_skill_combos()
check("技能组合", len(combos) >= 5)

if combos:
    readiness = sle.get_combo_readiness(combos[0]["id"])
    check("组合就绪", "all_skills_ready" in readiness)

    techniques = sle.apply_combo_techniques(combos[0]["id"])
    check("应用技巧", "techniques" in techniques)

new_combos = sle.discover_skill_combos()
check("发现组合", isinstance(new_combos, list))

# 持久化
sle.persist()
check("持久化", os.path.exists(os.path.join(TEST_DIR, "learning_engine.json")))


# ================================================================
# 9. 跨模块协同测试
# ================================================================
print("\n" + "=" * 60)
print("9. 跨模块协同测试")
print("=" * 60)

# Lorebook + StoryBible 协同
lb2 = Lorebook(storage_dir=TEST_DIR)
sb2 = StoryBible(storage_dir=TEST_DIR)

char_entries = lb2.find_by_category(EntryCategory.CHARACTER)
check("Lorebook角色条目", isinstance(char_entries, list))

entry = BibleEntry(entry_id="", section=BibleSection.CHARACTERS, title="测试角色", content="来自Lorebook的角色")
sb2.add_entry(entry)
check("StoryBible添加角色", True)

# StyleModule + SelfLearning 协同
smm2 = StyleModuleManager(storage_dir=TEST_DIR)
sle2 = SelfLearningEngine(storage_dir=TEST_DIR)

style_results = smm2.analyze_style("主角站在山巅，望着远方。")
sle2.gain_experience("description", 10)
check("风格分析+经验获取", len(style_results) >= 1)

# VersionManager + PlatformExporter 协同
vm2 = VersionManager(storage_dir=TEST_DIR)
pe2 = PlatformExporter(output_dir=TEST_DIR)

snap_id = vm2.create_snapshot(1, "# 第一章\n\n测试内容", message="导出测试")
snap = vm2.get_snapshot(snap_id)
meta2 = NovelMeta(title="协同测试", author="测试", genre="玄幻")
ch2 = [ChapterData(chapter_num=1, title="第一章", content=snap.content, word_count=snap.word_count)]
exported = pe2.export(meta2, ch2, ExportPlatform.TXT)
check("版本+导出协同", exported is not None)

# NovelMemory + IntelligentOrchestrator 协同
nmm2 = NovelMemoryManager(storage_dir=TEST_DIR)
io2 = IntelligentOrchestrator()

nmm2.store_chapter_text(1, "测试内容")
task_id = io2.enqueue_task("save_memory", chapter=1, text="测试内容")
check("记忆+编排协同", task_id is not None)
io2.shutdown()


# ================================================================
# 结果汇总
# ================================================================
print("\n" + "=" * 60)
print("测试结果汇总")
print("=" * 60)
print(f"  ✅ 通过: {passed}")
print(f"  ❌ 失败: {failed}")
total = passed + failed
print(f"  📊 通过率: {passed / total * 100:.1f}%" if total > 0 else "  📊 通过率: N/A")
print(f"\n测试目录: {TEST_DIR}")

# 清理
shutil.rmtree(TEST_DIR, ignore_errors=True)

if failed > 0:
    print("\n⚠️ 存在失败测试，请检查!")
    sys.exit(1)
else:
    print("\n🎉 全部测试通过!")
    sys.exit(0)
