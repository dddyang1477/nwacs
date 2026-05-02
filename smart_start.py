#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS V8.0 智能小说生成器 - 自动选择模式
功能：
1. 根据小说长度自动选择合适的生成模式
2. 简单易用的界面
3. 自动识别并使用最适合的方式
"""

import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

def print_header():
    print("="*60)
    print("📖 NWACS V8.0 智能小说生成器")
    print("="*60)

def ask_novel_info():
    print("\n请输入小说信息：")
    name = input("小说名称: ").strip()
    if not name:
        name = "我的小说"
    
    print("\n请选择小说长度：")
    print("  1. 短篇 (1-5章)")
    print("  2. 中篇 (6-20章)")
    print("  3. 长篇 (20章以上)")
    choice = input("\n请选择 (1/2/3): ").strip()
    
    length_map = {
        "1": "short",
        "2": "medium",
        "3": "long"
    }
    length = length_map.get(choice, "medium")
    
    return name, length

def recommend_mode(length):
    if length == "short":
        return "fast", "快速生成模式", "novel_generator.py"
    else:
        return "smart", "剧情连贯模式", "smart_novel_generator.py"

def explain_choice(mode_name, reason):
    print("\n" + "="*60)
    print(f"🎯 智能选择: {mode_name}")
    print("="*60)
    print(f"\n推荐理由：")
    for line in reason.split('\n'):
        print(f"  {line}")

def confirm():
    response = input("\n确认开始生成？(Y/n): ").strip().lower()
    return response != "n"

def main():
    print_header()
    
    print("\n这个工具会根据你的小说长度，自动选择最合适的生成模式！")
    
    name, length = ask_novel_info()
    
    mode, mode_name, script = recommend_mode(length)
    
    reasons = {
        "short": """你的小说是短篇（1-5章），章节少
- 快速生成模式即可满足需求
- 不需要复杂的剧情连贯系统
- 生成速度更快""",
        
        "medium": """你的小说是中篇（6-20章）
- 使用剧情连贯模式
- 确保角色、设定前后一致
- 剧情连贯更重要""",
        
        "long": """你的小说是长篇（20章以上）
- 使用剧情连贯模式
- 长篇小说需要更稳定的剧情连贯性
- 支持断点续传功能""",
    }
    
    explain_choice(mode_name, reasons[length])
    
    if confirm():
        print(f"\n启动 {mode_name}...")
        script_path = f"core/v8/{script}"
        
        if os.path.exists(script_path):
            os.system(f'py {script_path}')
        else:
            print(f"❌ 找不到脚本: {script_path}")
    else:
        print("\n好的，已取消")

if __name__ == "__main__":
    main()
