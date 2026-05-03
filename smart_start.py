#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS V8.0 智能小说生成器 - 自动选择模式
核心原则：质量优先，逐章写作，确保剧情一致！
用户无需输入提示词，系统自动完成一切！
"""

import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

def print_header():
    print("="*60)
    print("📖 NWACS V8.0 智能小说生成器")
    print("="*60)
    print("\n【核心原则】")
    print("  ✅ 质量优先，不追求速度")
    print("  ✅ 逐章写作，不批量生成")
    print("  ✅ 确保剧情、角色设定前后一致")
    print("  ✅ 用户无需输入提示词，系统全自动！")
    print("="*60)

def show_mode_menu():
    print("\n请选择生成模式：")
    print("  0. 🚀 全自动写作系统（强烈推荐⭐⭐⭐⭐⭐）")
    print("     【用户只需提供小说名称，系统全自动完成一切】")
    print("     - 自动分析任务")
    print("     - 自动生成角色名字")
    print("     - 自动构建世界观")
    print("     - 自动设计角色")
    print("     - 自动设计剧情")
    print("     - 自动创作章节")
    print("     - 自动质量审查")
    print("  1. 🔧 Skill协作编排系统（完整写作流水线）")
    print("     - 7阶段完整写作流程")
    print("     - Skill之间有序协作")
    print("     - 需手动确认每个阶段")
    print("  2. 🎯 高质量逐章模式")
    print("     - 质量优先，逐章写作")
    print("     - 每章生成后可审查、不满意可重写")
    print("  3. 📝 剧情连贯模式")
    print("     - 连续生成，但确保剧情一致")
    print("     - 支持断点续传")
    print("  4. ⚡ 快速生成模式")
    print("     - 适合短篇测试")
    print("     - 不保证剧情连贯性")

    choice = input("\n请选择 (0/1/2/3/4，默认=0): ").strip()
    return choice if choice else "0"

def get_mode_info(choice):
    modes = {
        "0": {
            "name": "全自动写作系统",
            "script": "core/v8/auto_writer.py",
            "desc": """你选择了全自动写作系统！⭐⭐⭐⭐⭐

【特点】
- ✅ 用户无需输入任何提示词！
- ✅ 系统自动分析需要什么
- ✅ 系统自动调度Skill
- ✅ 系统自动按顺序执行
- ✅ 从头到尾全自动完成

【流程】
1. 自动生成角色名字
2. 自动构建世界观
3. 自动设计角色
4. 自动设计剧情
5. 自动创作章节
6. 自动质量审查

强烈推荐！最适合想一键写小说的用户！"""
        },
        "1": {
            "name": "Skill协作编排系统",
            "script": "core/v8/skill_orchestrator.py",
            "desc": """你选择了Skill协作编排系统！

特点：
- ✅ 7阶段完整写作流程
- ✅ Skill之间有序协作
- ✅ 前阶段输出作为后阶段输入
- ✅ 需手动确认每个阶段"""
        },
        "2": {
            "name": "高质量逐章模式",
            "script": "core/v8/quality_novel_generator.py",
            "desc": """你选择了高质量逐章模式！

特点：
- ✅ 质量优先，不追求速度
- ✅ 逐章写作，不批量生成
- ✅ 每章生成后可审查，不满意可重写"""
        },
        "3": {
            "name": "剧情连贯模式",
            "script": "core/v8/smart_novel_generator.py",
            "desc": """你选择了剧情连贯模式！

特点：
- ✅ 保证角色设定和剧情连贯
- ✅ 支持断点续传"""
        },
        "4": {
            "name": "快速生成模式",
            "script": "core/v8/novel_generator.py",
            "desc": """你选择了快速生成模式！

特点：
- ⚡ 生成速度快
- ⚠️ 不保证剧情连贯
- 适合短篇测试"""
        }
    }
    return modes.get(choice, modes["0"])

def confirm():
    response = input("\n确认开始？(Y/n): ").strip().lower()
    return response != "n"

def main():
    print_header()

    choice = show_mode_menu()
    mode_info = get_mode_info(choice)

    print("\n" + "="*60)
    print(f"🎯 选择了: {mode_info['name']}")
    print("="*60)
    print(mode_info['desc'])

    if confirm():
        print(f"\n启动 {mode_info['name']}...")

        if os.path.exists(mode_info['script']):
            os.system(f'py {mode_info["script"]}')
        else:
            print(f"❌ 找不到脚本: {mode_info['script']}")
    else:
        print("\n好的，已取消")

if __name__ == "__main__":
    main()
