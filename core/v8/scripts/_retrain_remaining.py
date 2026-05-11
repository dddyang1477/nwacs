#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""补训剩余3项技能到专家水准"""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from self_learning_engine import SelfLearningEngine, SkillLevel

OUTPUT = os.path.join(os.path.dirname(__file__), "_retrain_result.txt")
f = open(OUTPUT, "w", encoding="utf-8")

def log(msg):
    print(msg)
    f.write(msg + "\n")
    f.flush()

engine = SelfLearningEngine()

log("=" * 60)
log("  补训: 对话写作 / 节奏控制 / 伏笔设计 → 专家")
log("=" * 60)

log("\n[训练前状态]")
for key, info in engine.get_skill_report().items():
    bar = "#" * (info["experience"] // 10) + "-" * (10 - info["experience"] // 10)
    log(f"  {info['display']:8s} | {info['level']:6s} | [{bar}] {info['experience']}/{info['max_experience']}")

remaining = ["对话写作", "节奏控制", "伏笔设计"]

for skill_name in remaining:
    log(f"\n{'=' * 60}")
    log(f"  训练: {skill_name}")
    log(f"{'=' * 60}")

    max_attempts = 5
    for attempt in range(max_attempts):
        skill = None
        for key, s in engine.skills.items():
            if s.name == skill_name:
                skill = s
                break

        if not skill:
            break

        level_order = list(SkillLevel)
        current_idx = level_order.index(skill.level)
        expert_idx = level_order.index(SkillLevel.EXPERT)

        if current_idx >= expert_idx:
            log(f"  ✅ 已达到专家水准: {skill.level.value}")
            break

        log(f"  第{attempt + 1}轮: {skill.level.value} → 目标专家")

        if engine.can_fetch_web():
            log(f"    🔍 联网搜索...")
            kids = engine.multi_source_search(f"{skill_name} 写作技巧 深度方法", max_items=10)
            log(f"    获取 {len(kids)} 条知识")
            for kid in kids:
                engine.use_knowledge(kid)
            exp_gain = len(kids) * 15
        else:
            log(f"    📚 知识库深度学习...")
            related = engine.search_knowledge(skill_name, limit=10)
            distilled = engine.distill_knowledge(min_quality=3.0)
            relevant = [d for d in distilled if skill_name in d.get("title", "")
                        or any(skill_name in tip for tip in d.get("key_tips", []))]
            exp_gain = max(len(related) * 10, len(relevant) * 8, 15)
            log(f"    知识库匹配: {len(related)}条相关, {len(relevant)}条蒸馏")

        skill.experience += exp_gain
        skill.usage_count += 1
        skill.success_count += 1

        while skill.experience >= skill.max_experience:
            skill.experience -= skill.max_experience
            skill.max_experience = int(skill.max_experience * 1.5)
            engine._level_up_skill(skill)

        log(f"    → {skill.level.value} (exp: {skill.experience}/{skill.max_experience})")

        if skill.level.value in ["专家", "大师", "宗师"]:
            break

        time.sleep(1)

log(f"\n{'=' * 60}")
log("  训练完成 - 最终状态")
log(f"{'=' * 60}")

expert_count = 0
for key, info in engine.get_skill_report().items():
    level_idx = list(SkillLevel).index(SkillLevel(info["level"]))
    expert_idx = list(SkillLevel).index(SkillLevel.EXPERT)
    bar = "#" * (info["experience"] // 10) + "-" * (10 - info["experience"] // 10)
    status = "✅" if level_idx >= expert_idx else "⏳"
    if level_idx >= expert_idx:
        expert_count += 1
    log(f"  {status} {info['display']:8s} | {info['level']:6s} | [{bar}] {info['experience']}/{info['max_experience']}")

log(f"\n  专家水准: {expert_count}/8")

if expert_count == 8:
    log("\n  🎉 全部8项核心技能达到专家水准!")
else:
    log(f"\n  ⚠️ {expert_count}/8 项达到专家水准")

engine.persist()
log("\n  ✅ 数据已持久化")
f.close()
print(f"\n  报告: {OUTPUT}")
