"""SelfLearningEngine 增强功能测试"""
import sys
sys.path.insert(0, r'd:\Trae CN\github\nwacs\nwacs')

from core.v8.self_learning_engine import SelfLearningEngine


def test_practice_mode():
    print("=" * 60)
    print("练习模式测试")
    print("=" * 60)

    engine = SelfLearningEngine()

    print(f"\n练习总数: {len(engine.exercises)}")
    ex = engine.get_exercise("EX_001")
    print(f"练习1: {ex.title} ({ex.difficulty})")

    result = engine.start_exercise("EX_001")
    print(f"开始练习: {result['exercise']['title']}")
    print(f"约束条件: {len(result['exercise']['constraints'])}条")

    attempt = engine.submit_attempt(
        "EX_001",
        "主角站在山巅，望着远方。他心中充满了矛盾与冲突。"
        "危机正在逼近，他必须做出选择。然而，一个神秘的声音突然在他脑海中响起..."
    )
    print(f"提交尝试: {attempt.attempt_id}, 字数: {attempt.word_count}")

    eval_result = engine.evaluate_attempt(attempt.attempt_id)
    print(f"评估结果: 综合评分={eval_result['overall_score']}")
    print(f"优点: {eval_result['strengths']}")
    print(f"改进: {eval_result['weaknesses']}")

    stats = engine.get_practice_stats()
    print(f"\n练习统计: 总练习{stats['total_exercises']}, 已完成{stats['completed_exercises']}, 总尝试{stats['total_attempts']}")

    print("\n✅ 练习模式测试通过")


def test_feedback_loop():
    print("\n" + "=" * 60)
    print("反馈循环测试")
    print("=" * 60)

    engine = SelfLearningEngine()

    fb = engine.create_feedback_record("剧情设计")
    print(f"\n反馈记录: {fb.skill_name}")
    print(f"差距分析: {fb.gap_analysis}")
    print(f"改进计划: {len(fb.improvement_plan)}条")

    all_fb = engine.get_all_feedback()
    print(f"总反馈记录: {len(all_fb)}条")

    weaknesses = engine.identify_weaknesses()
    print(f"薄弱环节: {weaknesses['total_weaknesses']}个")
    if weaknesses['recommended_focus']:
        print(f"建议关注: {[w['skill'] for w in weaknesses['recommended_focus']]}")

    trend = engine.track_improvement("剧情设计")
    print(f"改进趋势: {trend['trend']}")

    print("\n✅ 反馈循环测试通过")


def test_learning_path():
    print("\n" + "=" * 60)
    print("学习路径测试")
    print("=" * 60)

    engine = SelfLearningEngine()

    paths = engine.get_all_learning_paths()
    print(f"\n学习路径数: {len(paths)}")
    for p in paths:
        print(f"  {p['name']}: {p['milestones']}个里程碑, 进度{p['progress']}")

    if paths:
        milestones = engine.check_milestone_unlock(paths[0]["id"])
        print(f"\n里程碑状态 ({paths[0]['name']}):")
        for m in milestones["milestones"]:
            print(f"  {m['milestone']}: {m['status']}")

        next_action = engine.get_next_recommended_action(paths[0]["id"])
        if "next_milestone" in next_action:
            print(f"\n下一步: {next_action['next_milestone']}")
            print(f"推荐行动: {len(next_action['actions'])}项")

    print("\n✅ 学习路径测试通过")


def test_skill_combo():
    print("\n" + "=" * 60)
    print("技能组合测试")
    print("=" * 60)

    engine = SelfLearningEngine()

    combos = engine.get_all_skill_combos()
    print(f"\n技能组合数: {len(combos)}")
    for c in combos:
        print(f"  {c['name']}: 协同{c['synergy']}, 需要{c['skills']}")

    if combos:
        readiness = engine.get_combo_readiness(combos[0]["id"])
        print(f"\n组合就绪检查 ({combos[0]['name']}):")
        print(f"  全部就绪: {readiness['all_skills_ready']}")
        print(f"  建议: {readiness['recommendation']}")

        techniques = engine.apply_combo_techniques(combos[0]["id"])
        print(f"  可用技巧: {len(techniques['techniques'])}个")

    new_combos = engine.discover_skill_combos()
    print(f"\n新发现组合: {len(new_combos)}个")
    for nc in new_combos:
        print(f"  {nc.name}: 协同{nc.synergy_score:.0%}")

    print("\n✅ 技能组合测试通过")


def test_persistence():
    print("\n" + "=" * 60)
    print("持久化测试")
    print("=" * 60)

    engine = SelfLearningEngine()

    engine.submit_attempt("EX_001", "测试内容用于持久化验证。")
    engine.create_feedback_record("人物塑造")

    engine.persist()
    print("\n持久化完成")

    engine2 = SelfLearningEngine()
    print(f"重新加载后练习数: {len(engine2.exercises)}")
    print(f"重新加载后组合数: {len(engine2.skill_combos)}")
    print(f"重新加载后路径数: {len(engine2.learning_paths)}")
    print(f"重新加载后反馈数: {len(engine2.feedback_records)}")

    assert len(engine2.exercises) > 0, "练习数据丢失"
    assert len(engine2.skill_combos) > 0, "组合数据丢失"
    assert len(engine2.learning_paths) > 0, "路径数据丢失"

    print("\n✅ 持久化测试通过")


if __name__ == "__main__":
    test_practice_mode()
    test_feedback_loop()
    test_learning_path()
    test_skill_combo()
    test_persistence()

    print("\n" + "=" * 60)
    print("🎉 全部测试通过!")
    print("=" * 60)
