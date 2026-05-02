#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS V8.0 智能小说生成器 - 自动选择模式
核心原则：质量优先，逐章写作，确保剧情一致！
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
    print("="*60)

def show_mode_menu():
    print("\n请选择生成模式：")
    print("  1. 🎯 高质量逐章模式（强烈推荐）")
    print("     - 质量优先，逐章写作")
    print("     - 每章前回顾前面剧情")
    print("     - 每章生成后可审查、不满意可重写")
    print("  2. 📝 剧情连贯模式")
    print("     - 连续生成，但确保剧情一致")
    print("     - 支持断点续传")
    print("  3. ⚡ 快速生成模式")
    print("     - 适合短篇测试")
    print("     - 不保证剧情连贯性")
    
    choice = input("\n请选择 (1/2/3，默认=1): ").strip()
    return choice if choice else "1"

def get_mode_info(choice):
    modes = {
        "1": {
            "name": "高质量逐章模式",
            "script": "core/v8/quality_novel_generator.py",
            "desc": """你选择了高质量逐章模式！

特点：
- ✅ 质量优先，不追求速度
- ✅ 逐章写作，不批量生成
- ✅ 每章前回顾前面剧情，确保一致
- ✅ 每章生成后可审查，不满意可重写
- ✅ 支持暂停和继续生成

推荐使用！"""
        },
        "2": {
            "name": "剧情连贯模式",
            "script": "core/v8/smart_novel_generator.py",
            "desc": """你选择了剧情连贯模式！

特点：
- ✅ 保证角色设定和剧情连贯
- ✅ 支持断点续传
- ✅ 速度适中"""
        },
        "3": {
            "name": "快速生成模式",
            "script": "core/v8/novel_generator.py",
            "desc": """你选择了快速生成模式！

特点：
- ⚡ 生成速度快
- ⚠️ 不保证剧情连贯
- 适合短篇测试"""
        }
    }
    return modes.get(choice, modes["1"])

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
