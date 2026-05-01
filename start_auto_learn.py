#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 自动学习快速启动器
直接运行此脚本即可启动自动空闲学习监控
"""

import os
import sys
import subprocess

def start_auto_learn():
    """启动自动空闲学习监控器"""

    script_dir = os.path.dirname(os.path.abspath(__file__))
    auto_learn_script = os.path.join(script_dir, 'core', 'auto_idle_learning.py')
    learning_script = os.path.join(script_dir, 'core', 'comprehensive_learning.py')

    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║         NWACS 自动空闲学习系统 启动器                        ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)

    print(f"自动学习脚本: {auto_learn_script}")
    print(f"学习模块脚本: {learning_script}")
    print()

    if not os.path.exists(auto_learn_script):
        print(f"❌ 错误: 找不到自动学习脚本: {auto_learn_script}")
        return

    if not os.path.exists(learning_script):
        print(f"❌ 错误: 找不到学习模块脚本: {learning_script}")
        return

    print("🚀 正在启动自动空闲学习监控器...")
    print()
    print("功能说明:")
    print("   - 电脑空闲 10 分钟后自动启动联网学习")
    print("   - 学习间隔为 1 小时（避免过于频繁）")
    print("   - 按 Ctrl+C 可随时退出")
    print()
    print("="*60)
    print()

    try:
        subprocess.run([sys.executable, auto_learn_script, '-t', '600', '-s', learning_script])
    except KeyboardInterrupt:
        print("\n\n👋 已退出自动学习系统")
    except Exception as e:
        print(f"\n❌ 启动失败: {e}")

if __name__ == "__main__":
    start_auto_learn()
