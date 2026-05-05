#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS v7.0 超级启动器
一键启动所有功能
"""

import os
import sys
import webbrowser
from pathlib import Path
from datetime import datetime


def print_banner():
    """打印横幅"""
    print("="*70)
    print("🎭 NWACS v7.0 超级启动器")
    print("   Novel Writing AI Collaborative System")
    print("="*70)
    print()
    print("  版本: v7.0 | 架构: v2.2 | API: v2.0")
    print("  28个三级Skill | 32个知识库 | 135+ Python文件")
    print()


def print_main_menu():
    """打印主菜单"""
    print("="*70)
    print("📚 请选择功能分类")
    print("="*70)
    print()
    print("  🚀 A. 创作中心 - 小说创作相关功能")
    print("  🛡️ B. 质量中心 - 质量检查相关功能")
    print("  📚 C. 知识中心 - 知识库管理")
    print("  👥 D. 协作中心 - 团队协作功能")
    print("  🧪 E. 工具中心 - 诊断、测试、评测")
    print("  📱 F. 集成中心 - 飞书、微信等外部集成")
    print("  🌐 G. Web服务 - API服务和Web界面")
    print("  📖 H. 文档中心 - 查看使用指南")
    print()
    print("  ⚡ S. 快速开始 - 一键启动Web界面")
    print("  📊 X. 系统状态 - 查看完整系统状态")
    print()
    print("  0. 退出")
    print()


def run_quick_start():
    """快速开始 - 启动Web界面"""
    print("\n⚡ 快速开始模式")
    print("-"*40)

    # 检查依赖
    try:
        import flask
        import openai
    except ImportError:
        print("❌ 缺少依赖库，正在安装...")
        os.system("pip install flask openai")
        print("✅ 依赖安装完成")

    # 启动API服务
    print("\n🚀 正在启动API服务...")
    print("   等待服务启动...")
    print()

    # 启动浏览器
    webbrowser.open('http://localhost:5000')

    # 运行服务
    os.system("python core/api_server_v2.py")


def show_system_status():
    """显示系统状态"""
    print("\n📊 NWACS v7.0 系统状态")
    print("="*70)

    project_root = Path(__file__).parent

    # 文件统计
    py_files = list(project_root.glob("**/*.py"))
    md_files = list(project_root.glob("**/*.md"))
    skills_level3 = list((project_root / "skills/level3").glob("*.md"))
    skills_level2 = list((project_root / "skills/level2").glob("*.md"))

    # 核心模块
    core_modules = [
        "nwacs_novel_engine.py",
        "nwacs_quality_assurance.py",
        "nwacs_diagnostic.py",
        "nwacs_evaluator.py",
        "nwacs_launcher.py",
        "knowledge_base_manager.py",
        "team_collaboration.py",
        "performance_optimizer.py",
        "api_server_v2.py"
    ]

    print(f"\n📁 文件统计:")
    print(f"   Python文件: {len(py_files)}")
    print(f"   Markdown文档: {len(md_files)}")
    print(f"   三级Skill: {len(skills_level3)}")
    print(f"   二级Skill: {len(skills_level2)}")

    print(f"\n🎯 系统信息:")
    print(f"   NWACS版本: v7.0")
    print(f"   架构版本: v2.2")
    print(f"   API版本: v2.0")
    print(f"   知识库: 32个")

    print(f"\n⚙️ 核心模块:")
    for module in core_modules:
        path = project_root / "core" / module
        status = "✅" if path.exists() else "❌"
        print(f"   {status} {module}")

    # 检查外部集成
    print(f"\n📱 外部集成:")
    feishu = project_root / "core/feishu/nwacs_feishu.py"
    wechat = project_root / "core/wechat/nwacs_wechat.py"
    print(f"   {'✅' if feishu.exists() else '❌'} 飞书集成")
    print(f"   {'✅' if wechat.exists() else '❌'} 微信集成")

    # 检查启动脚本
    print(f"\n🚀 启动脚本:")
    scripts = [
        "启动NWACS.bat",
        "启动API服务.bat",
        "启动创作引擎.bat",
        "启动知识库管理.bat",
        "启动团队协作.bat"
    ]
    for script in scripts:
        path = project_root / script
        print(f"   {'✅' if path.exists() else '❌'} {script}")

    print(f"\n💡 建议操作:")
    print(f"   输入 'S' 快速启动Web界面")
    print(f"   输入 'G' 启动API服务和Web界面")
    print()


def open_file(filepath: str):
    """打开文件"""
    project_root = Path(__file__).parent
    full_path = project_root / filepath

    if full_path.exists():
        print(f"\n📖 打开文件: {filepath}")
        os.startfile(str(full_path))
    else:
        print(f"\n❌ 文件不存在: {filepath}")


def run_api_server():
    """运行API服务"""
    print("\n🌐 启动API服务...")
    print("-"*40)
    print("📍 访问地址: http://localhost:5000")
    print("🌐 Web界面: http://localhost:5000/")
    print()
    os.system("python core/api_server_v2.py")


def main():
    """主函数"""
    while True:
        print_banner()
        print_main_menu()

        choice = input("请输入选项: ").strip().upper()

        if choice == "0":
            print("\n👋 感谢使用NWACS！祝您创作愉快！\n")
            break

        elif choice == "S":
            run_quick_start()

        elif choice == "X":
            show_system_status()
            input("\n按Enter键继续...")

        elif choice == "A":
            while True:
                os.system('cls' if os.name == 'nt' else 'clear')
                print_banner()
                print("="*70)
                print("  🚀 创作中心")
                print("="*70)
                print()
                print("    1. 交互式小说创作引擎")
                print("    2. 快速创作模式")
                print("    3. 查看创作模板库")
                print()
                print("    0. 返回主菜单")
                print()

                sub_choice = input("请选择: ").strip()

                if sub_choice == "0":
                    break
                elif sub_choice == "1":
                    print("\n🚀 启动创作引擎...")
                    try:
                        from core.nwacs_novel_engine import NWACSNovelEngine
                        engine = NWACSNovelEngine()
                        engine.interactive_creator()
                    except Exception as e:
                        print(f"❌ 启动失败: {e}")
                    input("\n按Enter键继续...")

                elif sub_choice == "2":
                    print("\n⚡ 快速创作模式")
                    print("-"*40)
                    try:
                        from core.nwacs_launcher import run_quick_create
                        run_quick_create()
                    except Exception as e:
                        print(f"❌ 启动失败: {e}")
                    input("\n按Enter键继续...")

                elif sub_choice == "3":
                    open_file("docs/guides/小说创作模板库.md")
                    input("\n按Enter键继续...")

        elif choice == "B":
            while True:
                os.system('cls' if os.name == 'nt' else 'clear')
                print_banner()
                print("="*70)
                print("  🛡️ 质量中心")
                print("="*70)
                print()
                print("    1. 质量检查")
                print("    2. AI痕迹去除")
                print("    3. 可读性分析")
                print()
                print("    0. 返回主菜单")
                print()

                sub_choice = input("请选择: ").strip()

                if sub_choice == "0":
                    break
                elif sub_choice == "1":
                    try:
                        from core.nwacs_launcher import run_quality_check
                        run_quality_check()
                    except Exception as e:
                        print(f"❌ 启动失败: {e}")
                    input("\n按Enter键继续...")

                elif sub_choice == "2":
                    try:
                        from core.nwacs_launcher import run_ai_trait_removal
                        run_ai_trait_removal()
                    except Exception as e:
                        print(f"❌ 启动失败: {e}")
                    input("\n按Enter键继续...")

        elif choice == "C":
            while True:
                os.system('cls' if os.name == 'nt' else 'clear')
                print_banner()
                print("="*70)
                print("  📚 知识中心")
                print("="*70)
                print()
                print("    1. 用户知识库管理")
                print("    2. 查看系统知识库")
                print("    3. DeepSeek联网学习")
                print()
                print("    0. 返回主菜单")
                print()

                sub_choice = input("请选择: ").strip()

                if sub_choice == "0":
                    break
                elif sub_choice == "1":
                    print("\n📚 启动知识库管理...")
                    os.system("python core/knowledge_base_manager.py")
                    input("\n按Enter键继续...")

                elif sub_choice == "2":
                    try:
                        from core.nwacs_launcher import view_knowledge_bases
                        view_knowledge_bases()
                    except Exception as e:
                        print(f"❌ 启动失败: {e}")
                    input("\n按Enter键继续...")

                elif sub_choice == "3":
                    print("\n📚 DeepSeek联网学习...")
                    duration = input("学习时长 (30m/1h/2h/4h) [默认30m]: ").strip() or "30m"
                    os.system(f"python deepseek_learning_engine.py --duration {duration}")
                    input("\n按Enter键继续...")

        elif choice == "D":
            while True:
                os.system('cls' if os.name == 'nt' else 'clear')
                print_banner()
                print("="*70)
                print("  👥 协作中心")
                print("="*70)
                print()
                print("    1. 团队协作演示")
                print("    2. 用户管理")
                print("    3. 项目管理")
                print()
                print("    0. 返回主菜单")
                print()

                sub_choice = input("请选择: ").strip()

                if sub_choice == "0":
                    break
                elif sub_choice == "1":
                    print("\n👥 启动团队协作演示...")
                    os.system("python core/team_collaboration.py")
                    input("\n按Enter键继续...")

        elif choice == "E":
            while True:
                os.system('cls' if os.name == 'nt' else 'clear')
                print_banner()
                print("="*70)
                print("  🧪 工具中心")
                print("="*70)
                print()
                print("    1. 项目功能测试")
                print("    2. 项目健康诊断")
                print("    3. DeepSeek全面评测")
                print("    4. 性能优化演示")
                print()
                print("    0. 返回主菜单")
                print()

                sub_choice = input("请选择: ").strip()

                if sub_choice == "0":
                    break
                elif sub_choice == "1":
                    print("\n🧪 运行功能测试...")
                    try:
                        from core.nwacs_functional_test import run_all_tests
                        run_all_tests()
                    except Exception as e:
                        print(f"❌ 测试失败: {e}")
                    input("\n按Enter键继续...")

                elif sub_choice == "2":
                    print("\n🔍 运行项目诊断...")
                    try:
                        from core.nwacs_diagnostic import NWACSDiagnosticTool
                        tool = NWACSDiagnosticTool()
                        tool.run_full_diagnostic()
                    except Exception as e:
                        print(f"❌ 诊断失败: {e}")
                    input("\n按Enter键继续...")

                elif sub_choice == "3":
                    print("\n🧠 DeepSeek全面评测...")
                    try:
                        from core.nwacs_evaluator import NWACSEvaluator
                        evaluator = NWACSEvaluator()
                        evaluator.run_evaluation()
                    except Exception as e:
                        print(f"❌ 评测失败: {e}")
                    input("\n按Enter键继续...")

                elif sub_choice == "4":
                    print("\n⚡ 性能优化演示...")
                    try:
                        from core.performance_optimizer import main
                        main()
                    except Exception as e:
                        print(f"❌ 演示失败: {e}")
                    input("\n按Enter键继续...")

        elif choice == "F":
            while True:
                os.system('cls' if os.name == 'nt' else 'clear')
                print_banner()
                print("="*70)
                print("  📱 集成中心")
                print("="*70)
                print()
                print("    1. 飞书集成测试")
                print("    2. 微信集成测试")
                print("    3. 配置飞书")
                print("    4. 配置微信")
                print()
                print("    0. 返回主菜单")
                print()

                sub_choice = input("请选择: ").strip()

                if sub_choice == "0":
                    break
                elif sub_choice == "1":
                    print("\n✈️ 飞书集成测试...")
                    try:
                        from core.feishu.nwacs_feishu import NWACSFeishuIntegration
                        integration = NWACSFeishuIntegration()
                        integration.test_connection()
                    except Exception as e:
                        print(f"❌ 测试失败: {e}")
                    input("\n按Enter键继续...")

                elif sub_choice == "2":
                    print("\n💬 微信集成测试...")
                    try:
                        from core.wechat.nwacs_wechat import NWACSWechatIntegration
                        integration = NWACSWechatIntegration()
                        integration.test_connection()
                    except Exception as e:
                        print(f"❌ 测试失败: {e}")
                    input("\n按Enter键继续...")

                elif sub_choice == "3":
                    open_file("config/feishu_config.json")
                    input("\n按Enter键继续...")

                elif sub_choice == "4":
                    open_file("config/wechat_config.json")
                    input("\n按Enter键继续...")

        elif choice == "G":
            while True:
                os.system('cls' if os.name == 'nt' else 'clear')
                print_banner()
                print("="*70)
                print("  🌐 Web服务")
                print("="*70)
                print()
                print("    1. 启动API服务(v2)")
                print("    2. 打开Web界面")
                print("    3. 查看API文档")
                print()
                print("    0. 返回主菜单")
                print()

                sub_choice = input("请选择: ").strip()

                if sub_choice == "0":
                    break
                elif sub_choice == "1":
                    run_api_server()

                elif sub_choice == "2":
                    webbrowser.open('http://localhost:5000')
                    print("\n🌐 已在浏览器中打开Web界面")
                    input("\n按Enter键继续...")

                elif sub_choice == "3":
                    open_file("docs/guides/API使用说明.md")
                    input("\n按Enter键继续...")

        elif choice == "H":
            while True:
                os.system('cls' if os.name == 'nt' else 'clear')
                print_banner()
                print("="*70)
                print("  📖 文档中心")
                print("="*70)
                print()
                print("    1. 快速开始指南")
                print("    2. 完整优化总结")
                print("    3. 系统架构文档")
                print("    4. 项目状态报告")
                print("    5. 创作模板库")
                print("    6. API使用说明")
                print()
                print("    0. 返回主菜单")
                print()

                sub_choice = input("请选择: ").strip()

                if sub_choice == "0":
                    break
                elif sub_choice == "1":
                    open_file("docs/guides/快速开始指南.md")
                    input("\n按Enter键继续...")

                elif sub_choice == "2":
                    open_file("NWACS全面优化完成总结.md")
                    input("\n按Enter键继续...")

                elif sub_choice == "3":
                    open_file("docs/architecture/01_系统架构框架.md")
                    input("\n按Enter键继续...")

                elif sub_choice == "4":
                    open_file("项目状态报告.md")
                    input("\n按Enter键继续...")

                elif sub_choice == "5":
                    open_file("docs/guides/小说创作模板库.md")
                    input("\n按Enter键继续...")

                elif sub_choice == "6":
                    open_file("docs/guides/API使用说明.md")
                    input("\n按Enter键继续...")

        else:
            print("\n❌ 无效选项，请重新输入")
            input("\n按Enter键继续...")


if __name__ == "__main__":
    main()
