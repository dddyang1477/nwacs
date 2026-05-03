#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS一体化引擎 - 完整演示示例
展示V8模块与Skill系统如何协作工作
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def demo_1_initialize_engine():
    """演示1: 初始化一体化引擎"""
    print("\n" + "="*70)
    print("🎯 演示1: 初始化NWACS一体化引擎")
    print("="*70)

    from nwacs_unified_engine import NWACSUnifiedEngine
    engine = NWACSUnifiedEngine()

    return engine


def demo_2_list_skills(engine):
    """演示2: 列出所有可用技能"""
    print("\n" + "="*70)
    print("📋 演示2: 列出所有可用技能")
    print("="*70)

    skills = engine.list_skills()
    print(f"\n共 {len(skills)} 个技能可用:\n")

    for skill in skills:
        print(f"  {skill['icon']} {skill['name']}")
        print(f"     描述: {skill['description']}")
        print(f"     能力: {', '.join(skill['capabilities'])}")
        print()


def demo_3_list_workflows(engine):
    """演示3: 列出所有工作流"""
    print("\n" + "="*70)
    print("📁 演示3: 列出所有写作工作流")
    print("="*70)

    workflows = engine.list_workflows()
    print(f"\n共 {len(workflows)} 个工作流可用:\n")

    for workflow in workflows:
        print(f"  📝 {workflow['name']}")
        print(f"     描述: {workflow['description']}")
        print(f"     步骤: {workflow['steps']} 步")
        print()


def demo_4_execute_single_skill(engine):
    """演示4: 执行单个技能"""
    print("\n" + "="*70)
    print("🎯 演示4: 执行单个技能 - 爆款分析")
    print("="*70)

    result = engine.execute_skill("爆款分析", genre="玄幻")
    if result.get('status') == 'success':
        print("\n✅ 爆款分析执行成功！")
        output = str(result.get('result', ''))
        # 只显示前800字符
        if len(output) > 800:
            output = output[:800] + "\n...(内容已截断，完整内容请查看V8.7报告)"
        print(f"\n结果:\n{output}")
    else:
        print(f"\n❌ 执行失败: {result.get('message')}")


def demo_5_execute_another_skill(engine):
    """演示5: 执行另一个技能 - 公众号爆款"""
    print("\n" + "="*70)
    print("📱 演示5: 执行技能 - 公众号爆款写作")
    print("="*70)

    result = engine.execute_skill("公众号爆款", content_type="emotion")
    if result.get('status') == 'success':
        print("\n✅ 公众号爆款技能执行成功！")
        output = str(result.get('result', ''))
        if len(output) > 900:
            output = output[:900] + "\n...(内容已截断，完整内容请执行查看)"
        print(f"\n结果:\n{output}")
    else:
        print(f"\n❌ 执行失败: {result.get('message')}")


def demo_6_execute_suspense_twist(engine):
    """演示6: 执行悬念反转技能"""
    print("\n" + "="*70)
    print("🔍💥 演示6: 执行技能 - 悬念设置 + 反转设计")
    print("="*70)

    result = engine.execute_skill("反转设计",
        setup="主角林默以为自己只是普通穿越者",
        misdirection="所有人都认为他是废柴",
        revelation="原来他才是这个世界最后的天机师！")

    if result.get('status') == 'success':
        print("\n✅ 反转设计技能执行成功！")
        output = str(result.get('result', ''))
        if len(output) > 700:
            output = output[:700] + "\n...(内容已截断)"
        print(f"\n结果:\n{output}")
    else:
        print(f"\n❌ 执行失败: {result.get('message')}")


def demo_7_show_help(engine):
    """演示7: 显示帮助"""
    print("\n" + "="*70)
    print("❓ 演示7: 显示使用帮助")
    print("="*70)
    print(engine.get_help())


def demo_8_smart_novel_generator():
    """演示8: 智能小说生成器（简化版）"""
    print("\n" + "="*70)
    print("📖 演示8: 智能小说生成器预览")
    print("="*70)

    print("""
智能小说生成器特点:
  ✅ 写作时自动调用技能支持
  ✅ 章节创作前先分析爆款
  ✅ 自动设计悬念和反转
  ✅ 增强感官描写
  ✅ 交互式写作模式

使用方式:
  from smart_novel_generator_enhanced import SmartNovelGenerator
  generator = SmartNovelGenerator()
  generator.interactive_writing_mode()  # 交互模式
  # 或
  generator.generate_chapter_with_skills(1)  # 生成单章
""")


def main():
    """主演示函数"""
    print("\n" + "="*70)
    print("🚀 NWACS一体化引擎 - 完整功能演示")
    print("="*70)
    print("\n本演示将展示:")
    print("  1. 初始化一体化引擎")
    print("  2. 查看所有可用技能")
    print("  3. 查看所有写作工作流")
    print("  4. 执行单个技能（爆款分析）")
    print("  5. 执行公众号爆款写作技能")
    print("  6. 执行悬念反转技能")
    print("  7. 显示使用帮助")
    print("  8. 预览智能小说生成器")

    input("\n按回车键开始演示...")

    # 演示1: 初始化引擎
    engine = demo_1_initialize_engine()

    if not engine:
        print("\n❌ 引擎初始化失败，演示终止")
        return

    input("\n按回车键继续...")

    # 演示2: 列出技能
    demo_2_list_skills(engine)
    input("\n按回车键继续...")

    # 演示3: 列出工作流
    demo_3_list_workflows(engine)
    input("\n按回车键继续...")

    # 演示4: 执行爆款分析
    demo_4_execute_single_skill(engine)
    input("\n按回车键继续...")

    # 演示5: 执行公众号爆款
    demo_5_execute_another_skill(engine)
    input("\n按回车键继续...")

    # 演示6: 执行悬念反转
    demo_6_execute_suspense_twist(engine)
    input("\n按回车键继续...")

    # 演示7: 显示帮助
    demo_7_show_help(engine)
    input("\n按回车键继续...")

    # 演示8: 智能小说生成器
    demo_8_smart_novel_generator()

    # 完成
    print("\n" + "="*70)
    print("🎉 演示完成！")
    print("="*70)
    print("\n💡 提示: 请查看 core/v8/ 目录下的新增文件:")
    print("  - nwacs_unified_engine.py: 一体化引擎核心")
    print("  - smart_novel_generator_enhanced.py: 智能小说生成器")
    print("  - nwacs_demo.py: 本演示文件")
    print("\n💡 还可以运行 smart_novel_generator_enhanced.py 体验交互式写作！")


if __name__ == "__main__":
    main()
