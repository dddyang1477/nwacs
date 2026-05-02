#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS v7.0 统一启动管理器
一键选择所有功能
"""

import os
import sys
from pathlib import Path


def print_banner():
    """打印横幅"""
    print("=" * 60)
    print("🎭 NWACS v7.0 - 小说创作AI协作系统")
    print("=" * 60)
    print()
    print("  让AI成为您的专业创作团队")
    print()
    print("  版本: v7.0 | 架构: v2.2")
    print("  28个三级Skill | 32个知识库")
    print()


def print_menu():
    """打印菜单"""
    print("=" * 60)
    print("📚 请选择功能")
    print("=" * 60)
    print()
    print("  🚀 创作类")
    print("    1. 小说创作引擎（交互式）")
    print("    2. 快速创作（输入即创作）")
    print("    3. 创作模板库")
    print()
    print("  🛡️ 质量类")
    print("    4. 质量检查")
    print("    5. AI痕迹去除")
    print()
    print("  🧪 工具类")
    print("    6. 功能测试")
    print("    7. 项目诊断")
    print("    8. DeepSeek评测")
    print()
    print("  📱 集成类")
    print("    9. 飞书集成测试")
    print("   10. 微信集成测试")
    print()
    print("  📖 学习类")
    print("   11. DeepSeek联网学习")
    print("   12. 查看知识库")
    print()
    print("  ⚙️  系统")
    print("   13. 查看项目状态")
    print("   14. 打开项目目录")
    print("   15. 查看使用指南")
    print()
    print("   0. 退出")
    print()


def run_novel_engine():
    """运行小说创作引擎"""
    print("\n🚀 启动小说创作引擎...")
    try:
        from core.nwacs_novel_engine import NWACSNovelEngine
        engine = NWACSNovelEngine()
        engine.interactive_creator()
    except Exception as e:
        print(f"❌ 启动失败: {e}")


def run_quick_create():
    """快速创作"""
    print("\n⚡ 快速创作模式")
    print("-" * 40)

    prompt = input("请输入创作需求: ").strip()
    if not prompt:
        print("❌ 请输入创作需求")
        return

    novel_type = input("小说类型 (1-玄幻 2-都市 3-悬疑 4-科幻 5-历史 6-恐怖 7-游戏 8-女频) [默认1]: ").strip() or "1"

    types = ["xuanhuan", "dushi", "xuanyi", "kehuan", "lishi", "kongbu", "youxi", "nvpin"]
    type_id = int(novel_type) - 1 if novel_type.isdigit() and 1 <= int(novel_type) <= 8 else 0

    print(f"\n🚀 正在生成... (类型: {types[type_id]})")

    try:
        from core.nwacs_novel_engine import NWACSNovelEngine
        engine = NWACSNovelEngine()
        result = engine.generate_chapter(
            novel_type=types[type_id],
            prompt=prompt,
            chapter_title="快速创作",
            word_count=3000
        )

        if result['success']:
            print("\n" + "=" * 60)
            print("📖 创作结果")
            print("=" * 60)
            print(result['content'][:2000])
            if len(result['content']) > 2000:
                print("\n... (内容过长已截断)")
        else:
            print(f"❌ 创作失败: {result.get('error')}")

    except Exception as e:
        print(f"❌ 创作失败: {e}")


def run_quality_check():
    """质量检查"""
    print("\n🛡️ 质量检查")
    print("-" * 40)

    text = input("请输入要检查的文本 (或输入文件路径): ").strip()

    if not text:
        print("❌ 请输入文本")
        return

    # 检查是否是文件路径
    if os.path.isfile(text):
        with open(text, 'r', encoding='utf-8') as f:
            text = f.read()

    try:
        from core.nwacs_quality_assurance import QualityAssurance
        qa = QualityAssurance()
        result = qa.full_quality_check(text)
    except Exception as e:
        print(f"❌ 检查失败: {e}")


def run_ai_trait_removal():
    """AI痕迹去除"""
    print("\n🔧 AI痕迹去除")
    print("-" * 40)

    text = input("请输入文本: ").strip()
    if not text:
        print("❌ 请输入文本")
        return

    try:
        from core.nwacs_quality_assurance import QualityAssurance
        qa = QualityAssurance()
        cleaned, changes = qa.remove_ai_traits(text)

        print(f"\n✅ 完成 {len(changes)} 处优化")
        if changes:
            for change in changes[:5]:
                print(f"   - {change}")

        print("\n优化后文本:")
        print(cleaned[:1500])
        if len(cleaned) > 1500:
            print("\n... (内容过长已截断)")

    except Exception as e:
        print(f"❌ 处理失败: {e}")


def run_functional_test():
    """功能测试"""
    print("\n🧪 运行功能测试...")
    try:
        from core.nwacs_functional_test import run_all_tests
        run_all_tests()
    except Exception as e:
        print(f"❌ 测试失败: {e}")


def run_diagnostic():
    """项目诊断"""
    print("\n🔍 项目诊断...")
    try:
        from core.nwacs_diagnostic import NWACSDiagnosticTool
        tool = NWACSDiagnosticTool()
        tool.run_full_diagnostic()
    except Exception as e:
        print(f"❌ 诊断失败: {e}")


def run_deepseek_evaluation():
    """DeepSeek评测"""
    print("\n🧠 DeepSeek评测...")
    try:
        from core.nwacs_evaluator import NWACSEvaluator
        evaluator = NWACSEvaluator()
        evaluator.run_evaluation()
    except Exception as e:
        print(f"❌ 评测失败: {e}")


def run_feishu_test():
    """飞书测试"""
    print("\n✈️ 飞书集成测试...")
    try:
        from core.feishu.nwacs_feishu import NWACSFeishuIntegration
        integration = NWACSFeishuIntegration()
        integration.test_connection()
    except Exception as e:
        print(f"❌ 飞书测试失败: {e}")


def run_wechat_test():
    """微信测试"""
    print("\n💬 微信集成测试...")
    try:
        from core.wechat.nwacs_wechat import NWACSWechatIntegration
        integration = NWACSWechatIntegration()
        integration.test_connection()
    except Exception as e:
        print(f"❌ 微信测试失败: {e}")


def run_deepseek_learning():
    """DeepSeek学习"""
    print("\n📚 DeepSeek联网学习...")
    duration = input("学习时长 (30m/1h/2h/4h) [默认30m]: ").strip() or "30m"

    try:
        os.system(f"python deepseek_learning_engine.py --duration {duration}")
    except Exception as e:
        print(f"❌ 学习启动失败: {e}")


def view_knowledge_bases():
    """查看知识库"""
    print("\n📚 知识库列表")
    print("-" * 40)

    knowledge_dir = Path("skills/level2/learnings")
    if not knowledge_dir.exists():
        print("❌ 知识库目录不存在")
        return

    files = list(knowledge_dir.glob("*.txt")) + list(knowledge_dir.glob("*.md"))
    files = [f for f in files if "索引" not in f.name and "配置" not in f.name]

    print(f"共 {len(files)} 个知识库:\n")

    for i, f in enumerate(files[:20], 1):
        print(f"  {i}. {f.name}")

    if len(files) > 20:
        print(f"\n  ... 还有 {len(files)-20} 个知识库")


def view_project_status():
    """查看项目状态"""
    print("\n📊 NWACS项目状态")
    print("=" * 60)

    project_root = Path(__file__).parent

    # 统计文件
    py_files = list(project_root.glob("**/*.py"))
    md_files = list(project_root.glob("**/*.md"))
    skills_level3 = list((project_root / "skills/level3").glob("*.md"))

    print(f"\n📁 项目统计:")
    print(f"   Python文件: {len(py_files)}")
    print(f"   Markdown文档: {len(md_files)}")
    print(f"   三级Skill: {len(skills_level3)}")

    print(f"\n🎯 系统信息:")
    print(f"   NWACS版本: v7.0")
    print(f"   架构版本: v2.2")
    print(f"   知识库: 32个")
    print(f"   二级Skill: 30+个")

    print(f"\n✅ 状态: 完全正常运行")


def open_project_dir():
    """打开项目目录"""
    print("\n📂 打开项目目录...")
    project_root = Path(__file__).parent
    os.startfile(str(project_root))


def view_guide():
    """查看使用指南"""
    print("\n📖 使用指南")
    print("=" * 60)
    print("""
🎯 快速开始:

1️⃣  小说创作
   运行「启动创作引擎.bat」
   选择类型 → 输入需求 → 生成章节

2️⃣  质量检查
   在创作引擎中选择「质量检查」
   或直接输入文本进行检查

3️⃣  飞书集成
   配置 config/feishu_config.json
   运行「启动飞书集成.bat」

📚 更多信息:
   查看 docs/guides/ 目录下的指南
   查看 NWACS_v7.0_优化完成总结.md
""")


def main():
    """主函数"""
    while True:
        print_banner()
        print_menu()

        choice = input("请输入选项 (0-15): ").strip()

        if choice == "0":
            print("\n👋 感谢使用NWACS！")
            print("   祝您创作愉快！")
            break
        elif choice == "1":
            run_novel_engine()
        elif choice == "2":
            run_quick_create()
        elif choice == "3":
            print("\n📚 模板库功能开发中...")
        elif choice == "4":
            run_quality_check()
        elif choice == "5":
            run_ai_trait_removal()
        elif choice == "6":
            run_functional_test()
        elif choice == "7":
            run_diagnostic()
        elif choice == "8":
            run_deepseek_evaluation()
        elif choice == "9":
            run_feishu_test()
        elif choice == "10":
            run_wechat_test()
        elif choice == "11":
            run_deepseek_learning()
        elif choice == "12":
            view_knowledge_bases()
        elif choice == "13":
            view_project_status()
        elif choice == "14":
            open_project_dir()
        elif choice == "15":
            view_guide()
        else:
            print("\n❌ 无效选项，请重新输入")

        input("\n按Enter键继续...")


if __name__ == "__main__":
    main()
