import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from self_learning_engine import SelfLearningEngine, SkillLevel, KnowledgeCategory

out_path = os.path.join(os.path.dirname(__file__), "_train_result.txt")
f = open(out_path, "w", encoding="utf-8")

def log(msg):
    print(msg)
    f.write(msg + "\n")
    f.flush()

log("=" * 60)
log("  NWACS 真实联网学习 - 8项核心技能训练")
log("=" * 60)

engine = SelfLearningEngine()

log("\n[训练前技能状态]")
for key, info in engine.get_skill_report().items():
    bar = "#" * (info["experience"] // 10) + "-" * (10 - info["experience"] // 10)
    log(f"  {info['display']:8s} | {info['level']:6s} | [{bar}] {info['experience']}/{info['max_experience']}")

log(f"\n[知识库状态] 共 {len(engine.knowledge_base)} 条知识")

log("\n" + "=" * 60)
log("  阶段1: 联网搜索学习")
log("=" * 60)

if engine.can_fetch_web():
    log("  ✅ 可以联网，开始多源搜索...")
    topics = [
        "网文写作技巧 2025",
        "小说人物塑造方法",
        "剧情结构设计技巧",
        "对话写作方法",
        "场景描写技巧",
    ]
    for topic in topics:
        log(f"\n  🔍 搜索: {topic}")
        kids = engine.multi_source_search(topic, max_items=8)
        log(f"     获取 {len(kids)} 条知识")
else:
    log("  ⏳ 联网冷却中，使用已有知识库")

log("\n" + "=" * 60)
log("  阶段2: 知识综合与蒸馏")
log("=" * 60)

synthesis_topics = ["人物塑造", "剧情设计", "对话写作"]
for topic in synthesis_topics:
    result = engine.synthesize_knowledge(topic)
    log(f"  📝 {topic}: 综合 {result['source_count']} 条知识, {len(result['key_insights'])} 条洞察")

distilled = engine.distill_knowledge(min_quality=3.0)
log(f"  📋 知识蒸馏: {len(distilled)} 条可执行写作清单")

log("\n" + "=" * 60)
log("  阶段3: 逐技能真实训练")
log("=" * 60)

results = engine.train_all_skills_to_expert()

log("\n" + "=" * 60)
log("  训练结果")
log("=" * 60)

for key, result in results.items():
    if result.get("success"):
        total_knowledge = len(result.get("knowledge_acquired", []))
        log(f"  ✅ {result['skill']}: {result['start_level']} → {result['end_level']} "
            f"(获取 {total_knowledge} 条知识)")
        for rnd in result.get("training_rounds", []):
            log(f"       {rnd['from_level']} → {rnd['to_level']} "
                f"(知识: {rnd['knowledge_items']}, 经验: {rnd['experience']})")
    else:
        log(f"  ❌ {result.get('skill', key)}: {result.get('error', 'unknown')}")

log("\n[训练后技能状态]")
for key, info in engine.get_skill_report().items():
    bar = "#" * (info["experience"] // 10) + "-" * (10 - info["experience"] // 10)
    log(f"  {info['display']:8s} | {info['level']:6s} | [{bar}] {info['experience']}/{info['max_experience']}")

expert_count = sum(
    1 for s in engine.skills.values()
    if list(SkillLevel).index(s.level) >= list(SkillLevel).index(SkillLevel.EXPERT)
)
log(f"\n  专家级以上技能: {expert_count}/8")

log(f"\n[知识库增长]")
log(f"  训练前: {len(engine.knowledge_base) - engine.total_learned + sum(len(r.get('knowledge_acquired', [])) for r in results.values())} 条")
log(f"  训练后: {len(engine.knowledge_base)} 条")

engine.persist()
log("\n  ✅ 训练数据已持久化")

log("\n" + "=" * 60)
if expert_count == 8:
    log("  🎉 全部8项核心技能通过真实联网学习达到专家水准!")
else:
    log(f"  ⚠️ {expert_count}/8 项技能达到专家水准")
log("=" * 60)

f.close()
print("\nDONE - result written to _train_result.txt")
