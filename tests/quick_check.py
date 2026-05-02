#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS快速检测脚本
检测重要文件的编码、语法等问题
"""

import ast
import json
from pathlib import Path

def main():
    print("="*60)
    print("🔍 NWACS快速检测")
    print("="*60)

    files_to_check = [
        "deepseek_learning_engine.py",
        "core/feishu/nwacs_feishu.py",
        "core/wechat/nwacs_wechat.py",
        "core/nwacs_diagnostic.py"
    ]

    all_ok = True

    for filepath in files_to_check:
        fp = Path(filepath)
        if not fp.exists():
            print(f"\n❌ 文件不存在: {filepath}")
            all_ok = False
            continue

        print(f"\n📄 检查: {filepath}")

        # 1. 检查编码
        try:
            with open(fp, 'r', encoding='utf-8') as f:
                f.read()
            print("  ✅ 编码: UTF-8")
        except Exception as e:
            print(f"  ❌ 编码错误: {e}")
            all_ok = False

        # 2. 检查Python语法
        if filepath.endswith('.py'):
            try:
                with open(fp, 'r', encoding='utf-8') as f:
                    content = f.read()
                ast.parse(content)
                print("  ✅ Python语法: 正常")
            except SyntaxError as e:
                print(f"  ❌ 语法错误: 第{e.lineno}行 - {e}")
                all_ok = False
            except Exception as e:
                print(f"  ⚠️ 解析错误: {e}")

    # 检查JSON文件
    json_files = [
        "config/feishu_config.json",
        "config/wechat_config.json"
    ]

    for filepath in json_files:
        fp = Path(filepath)
        if not fp.exists():
            continue

        print(f"\n📄 检查: {filepath}")
        try:
            with open(fp, 'r', encoding='utf-8') as f:
                json.load(f)
            print("  ✅ JSON格式: 正常")
        except json.JSONDecodeError as e:
            print(f"  ❌ JSON错误: {e}")
            all_ok = False

    print("\n" + "="*60)
    if all_ok:
        print("✅ 所有检查通过！")
    else:
        print("⚠️ 发现部分问题")
    print("="*60)

if __name__ == "__main__":
    main()
