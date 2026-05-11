#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 书籍知识分发与技能训练一体化脚本

流程：
  阶段1: 加载BookKnowledgeBase，获取技能→知识映射表
  阶段2: 将书籍技法吸收到SelfLearningEngine知识库
  阶段3: 联网搜索补充最新写作技巧
  阶段4: 逐技能训练到专家水准
  阶段5: 全模块集成验证
  阶段6: 生成最终报告
"""

import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from book_knowledge_base import BookKnowledgeBase, SkillTarget
from self_learning_engine import SelfLearningEngine, SkillLevel, KnowledgeCategory

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
REPORT_PATH = os.path.join(OUTPUT_DIR, "_distribution_report.txt")


def log(msg: str, f=None):
    print(msg)
    if f:
        f.write(msg + "\n")
        f.flush()


def main():
    f = open(REPORT_PATH, "w", encoding="utf-8")

    log("=" * 70, f)
    log("  NWACS 书籍知识分发与技能训练 - 一体化执行", f)
    log("=" * 70, f)
    log(f"  开始时间: {time.strftime('%Y-%m-%d %H:%M:%S')}", f)

    # ================================================================
    # 阶段1: 加载书籍知识库
    # ================================================================
    log("\n" + "=" * 70, f)
    log("  阶段1: 加载BookKnowledgeBase", f)
    log("=" * 70, f)

    kb = BookKnowledgeBase()
    kb_stats = kb.get_statistics()
    log(f"  收录书籍: {kb_stats['total_books']} 本", f)
    log(f"  提炼技法: {kb_stats['total_insights']} 条", f)
    log(f"  可执行技巧: {kb_stats['total_actionable_tips']} 条", f)

    knowledge_map = kb.get_skill_knowledge_map()
    log(f"\n  技能→知识映射:", f)
    for skill_name, entries in knowledge_map.items():
        log(f"    {skill_name}: {len(entries)} 条技法", f)

    # ================================================================
    # 阶段2: 吸收书籍知识到SelfLearningEngine
    # ================================================================
    log("\n" + "=" * 70, f)
    log("  阶段2: 吸收书籍技法到SelfLearningEngine", f)
    log("=" * 70, f)

    engine = SelfLearningEngine()

    log("\n  [吸收前技能状态]", f)
    for key, info in engine.get_skill_report().items():
        bar = "#" * (info["experience"] // 10) + "-" * (10 - info["experience"] // 10)
        log(f"    {info['display']:8s} | {info['level']:6s} | [{bar}] "
            f"{info['experience']}/{info['max_experience']}", f)

    absorb_stats = engine.absorb_book_knowledge(knowledge_map)

    log(f"\n  [吸收结果]", f)
    log(f"    吸收书籍: {absorb_stats['total_books_absorbed']} 本", f)
    log(f"    新增技法: {absorb_stats['total_techniques_added']} 条", f)
    log(f"    新增技巧: {absorb_stats['total_tips_added']} 条", f)

    log(f"\n  [各技能增强详情]", f)
    for skill_name, detail in absorb_stats["skills_enhanced"].items():
        log(f"    {skill_name}: {detail['books']}本书 {detail['techniques']}技法 "
            f"{detail['tips']}技巧 +{detail['exp_gained']}exp → {detail['new_level']}", f)

    log(f"\n  [吸收后技能状态]", f)
    for key, info in engine.get_skill_report().items():
        bar = "#" * (info["experience"] // 10) + "-" * (10 - info["experience"] // 10)
        log(f"    {info['display']:8s} | {info['level']:6s} | [{bar}] "
            f"{info['experience']}/{info['max_experience']}", f)

    # ================================================================
    # 阶段3: 联网搜索补充最新技巧
    # ================================================================
    log("\n" + "=" * 70, f)
    log("  阶段3: 联网搜索补充最新写作技巧", f)
    log("=" * 70, f)

    if engine.can_fetch_web():
        log("  可以联网，开始多源搜索...", f)
        search_topics = [
            "网文写作技巧 2025 2026 最新",
            "小说人物塑造深度方法",
            "长篇小说剧情结构设计",
            "对话写作高级技巧 潜台词",
            "场景描写五感运用方法",
            "小说节奏控制 张弛有度",
            "伏笔设计悬念设置技巧",
            "读者情绪共鸣设计方法",
            "架空世界观构建体系",
        ]
        total_web_learned = 0
        for topic in search_topics:
            log(f"\n  🔍 搜索: {topic}", f)
            kids = engine.multi_source_search(topic, max_items=8)
            log(f"     获取 {len(kids)} 条知识", f)
            total_web_learned += len(kids)
            time.sleep(1)
        log(f"\n  联网学习总计: {total_web_learned} 条", f)
    else:
        log("  联网冷却中，使用已有知识库深度学习", f)
        for skill_name in ["人物塑造", "剧情设计", "对话写作", "场景描写"]:
            result = engine.synthesize_knowledge(skill_name)
            log(f"  📝 {skill_name}: 综合 {result['source_count']} 条知识, "
                f"{len(result['key_insights'])} 条洞察", f)

    # ================================================================
    # 阶段4: 逐技能训练到专家水准
    # ================================================================
    log("\n" + "=" * 70, f)
    log("  阶段4: 逐技能训练到专家水准", f)
    log("=" * 70, f)

    training_results = engine.train_all_skills_to_expert()

    log(f"\n  [训练结果]", f)
    for key, result in training_results.get("details", {}).items():
        if result.get("success"):
            if "start_level" in result:
                total_knowledge = len(result.get("knowledge_acquired", []))
                log(f"  ✅ {result['skill']}: {result['start_level']} → {result['end_level']} "
                    f"(获取 {total_knowledge} 条知识)", f)
                for rnd in result.get("training_rounds", []):
                    log(f"       {rnd['from_level']} → {rnd['to_level']} "
                        f"(知识: {rnd['knowledge_items']}, 经验: {rnd['experience']})", f)
            else:
                log(f"  ✅ {result['skill']}: {result['level']} ({result.get('message', '已达标')})", f)
        else:
            log(f"  ❌ {result.get('skill', key)}: {result.get('error', 'unknown')}", f)

    # ================================================================
    # 阶段5: 全模块集成验证
    # ================================================================
    log("\n" + "=" * 70, f)
    log("  阶段5: 全模块集成验证", f)
    log("=" * 70, f)

    verification_results = {}

    # 5.1 验证SelfLearningEngine
    log("\n  [5.1 SelfLearningEngine验证]", f)
    try:
        stats = engine.get_learning_stats()
        log(f"    知识条目: {stats['total_knowledge_items']}", f)
        log(f"    词汇总量: {stats['total_vocabulary']}", f)
        log(f"    技能数量: {stats['total_skills']}", f)
        log(f"    累计学习: {stats['total_learned']}", f)
        verification_results["self_learning_engine"] = "PASS"
    except Exception as e:
        log(f"    ❌ 失败: {e}", f)
        verification_results["self_learning_engine"] = f"FAIL: {e}"

    # 5.2 验证技能等级
    log("\n  [5.2 技能等级验证]", f)
    level_order = list(SkillLevel)
    expert_idx = level_order.index(SkillLevel.EXPERT)
    expert_count = 0
    for key, info in engine.get_skill_report().items():
        skill_level = SkillLevel(info["level"])
        current_idx = level_order.index(skill_level)
        status = "✅ 专家+" if current_idx >= expert_idx else "⏳ 训练中"
        if current_idx >= expert_idx:
            expert_count += 1
        log(f"    {info['display']:8s} | {info['level']:6s} | {status}", f)
    log(f"\n    专家水准: {expert_count}/8", f)
    verification_results["skill_levels"] = f"{expert_count}/8 expert"

    # 5.3 验证BookKnowledgeBase
    log("\n  [5.3 BookKnowledgeBase验证]", f)
    try:
        for skill in SkillTarget:
            insights = kb.get_insights_by_skill(skill)
            log(f"    {skill.value}: {len(insights)} 条技法", f)
        verification_results["book_knowledge_base"] = "PASS"
    except Exception as e:
        log(f"    ❌ 失败: {e}", f)
        verification_results["book_knowledge_base"] = f"FAIL: {e}"

    # 5.4 验证其他核心模块
    log("\n  [5.4 核心模块导入验证]", f)
    modules_to_verify = [
        ("novel_memory_manager", "NovelMemoryManager"),
        ("chinese_traditional_namer", "ChineseTraditionalNamer"),
        ("plot_brainstorm_engine", "PlotBrainstormEngine"),
        ("enhanced_ai_detector", "EnhancedAIDetector"),
        ("collaborative_pipeline", "CollaborativeWritingPipeline"),
        ("intelligent_orchestrator", "IntelligentOrchestrator"),
        ("enhanced_skill_manager", "EnhancedSkillManager"),
    ]

    for module_name, class_name in modules_to_verify:
        try:
            mod = __import__(module_name)
            cls = getattr(mod, class_name, None)
            if cls:
                log(f"    ✅ {module_name}.{class_name}", f)
                verification_results[module_name] = "PASS"
            else:
                log(f"    ⚠️ {module_name} 导入成功但未找到 {class_name}", f)
                verification_results[module_name] = "WARN: class not found"
        except Exception as e:
            log(f"    ❌ {module_name}: {e}", f)
            verification_results[module_name] = f"FAIL: {e}"

    # ================================================================
    # 阶段6: 持久化与最终报告
    # ================================================================
    log("\n" + "=" * 70, f)
    log("  阶段6: 持久化与最终报告", f)
    log("=" * 70, f)

    engine.persist()
    log("  ✅ 学习数据已持久化", f)

    final_stats = engine.get_learning_stats()
    log(f"\n  [最终学习统计]", f)
    log(f"    知识条目总数: {final_stats['total_knowledge_items']}", f)
    log(f"    词汇总量: {final_stats['total_vocabulary']}", f)
    log(f"    联网学习次数: {final_stats['web_fetches']}", f)
    log(f"    上次联网: {final_stats['last_web_fetch']}", f)

    log(f"\n  [最终技能状态]", f)
    for key, info in engine.get_skill_report().items():
        bar = "#" * (info["experience"] // 10) + "-" * (10 - info["experience"] // 10)
        log(f"    {info['display']:8s} | {info['level']:6s} | [{bar}] "
            f"{info['experience']}/{info['max_experience']} "
            f"(成功率: {info['success_rate']}%)", f)

    # 总结
    log("\n" + "=" * 70, f)
    log("  执行总结", f)
    log("=" * 70, f)

    total_pass = sum(1 for v in verification_results.values() if v == "PASS")
    total_checks = len(verification_results)
    log(f"  集成验证: {total_pass}/{total_checks} 通过", f)

    if expert_count == 8:
        log(f"\n  🎉 全部8项核心技能达到专家水准!", f)
    elif expert_count >= 6:
        log(f"\n  ✅ {expert_count}/8 项技能达到专家水准，剩余技能接近专家", f)
    else:
        log(f"\n  ⚠️ {expert_count}/8 项技能达到专家水准，需继续训练", f)

    log(f"\n  完成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}", f)
    log(f"  报告文件: {REPORT_PATH}", f)

    f.close()

    # 输出到控制台
    print(f"\n  完整报告已保存到: {REPORT_PATH}")

    return {
        "expert_count": expert_count,
        "verification_pass": total_pass,
        "verification_total": total_checks,
        "knowledge_items": final_stats["total_knowledge_items"],
    }


if __name__ == "__main__":
    result = main()
    print(f"\n  返回码: {result}")
