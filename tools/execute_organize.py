#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS目录整理脚本
安全地移动和整理项目文件
"""

import os
import shutil
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent

# 文件移动规则
MOVE_RULES = {
    # 小说相关文件
    "novels/缄默天师": [
        "小说大纲_缄默天师.txt"
    ],

    # 文档
    "docs": [
        "FEISHU_DEBUG.md",
        "NWACS_v7.0_二次优化完成总结.md",
        "NWACS_v7.0_优化完成总结.md",
        "NWACS全面优化完成总结.md",
        "NWACS最终优化完成总结.md",
        "QUICK_START.md",
        "WRITING_TOOLS_GUIDE.md",
        "项目状态报告.md",
        "飞书指令服务器配置指南.md"
    ],

    # 批处理脚本
    "scripts/bat": [
        "install_ngrok.bat",
        "install_ngrok_en.bat",
        "learn_now.bat",
        "quick_learning_test.bat",
        "run_learning_test.bat",
        "run_test.bat",
        "run_test_en.bat",
        "start_auto_learn.bat",
        "start_feishu_server.bat",
        "start_nwacs.bat",
        "start_nwacs_main.bat",
        "start_server.bat",
        "启动API服务.bat",
        "启动DeepSeek评测.bat",
        "启动NWACS.bat",
        "启动创作引擎.bat",
        "启动功能测试.bat",
        "启动团队协作.bat",
        "启动微信集成.bat",
        "启动知识库管理.bat",
        "启动诊断工具.bat",
        "启动超级启动器.bat",
        "启动飞书指令服务器.bat",
        "启动飞书集成.bat"
    ],

    # PowerShell脚本
    "scripts/ps1": [
        "test_feishu.ps1"
    ],

    # 测试文件
    "tests": [
        "enterprise_comparison.py",
        "feishu_auto_demo.py",
        "feishu_command_server.py",
        "feishu_debug.py",
        "feishu_final_test.py",
        "feishu_simple_test.py",
        "feishu_test_send.py",
        "manual_feishu_test.py",
        "quick_check.py",
        "quick_feishu_test.py",
        "quick_learning_test.py",
        "run_learning_quick.py",
        "run_learning_test.py",
        "setup_feishu.py",
        "simple_evaluator.py",
        "simple_feishu_test.py",
        "simple_test.py",
        "test_feishu.py",
        "test_output.py",
        "test_port.py",
        "test_python_env.py",
        "test_server.py"
    ],

    # 临时测试文件
    "temp_tests": [
        "deepseek_classics_learning.py",
        "start_auto_learn.py"
    ],

    # 核心技能文件
    "skills": [
        "deepseek_learning_engine.py",
        "deepseek_online_optimize.py",
        "feishu_server_v2.py",
        "feishu_deepseek_diagnosis.py",
        "simple_learning.py",
        "specialized_learning.py"
    ],

    # 核心文件
    "core": [
        "config.json",
        "main.py",
        "nwacs_main.py",
        "server_simple.py"
    ],

    # 工具报告
    "tools": [
        "deepseek_optimization_report.txt"
    ]
}

def move_file(src, dst):
    """安全移动文件"""
    src_path = PROJECT_ROOT / src
    dst_path = PROJECT_ROOT / dst

    if not src_path.exists():
        print(f"  跳过（不存在）: {src}")
        return False

    if dst_path.exists():
        print(f"  跳过（目标已存在）: {src} -> {dst}")
        return False

    # 确保目标目录存在
    dst_path.parent.mkdir(parents=True, exist_ok=True)

    shutil.move(str(src_path), str(dst_path))
    print(f"  ✅ 移动: {src} -> {dst}")
    return True

def main():
    print("="*60)
    print("NWACS目录整理")
    print("="*60)
    print()

    moved_count = 0

    # 按规则移动文件
    for target_dir, files in MOVE_RULES.items():
        print(f"\n📂 移动到 {target_dir}/:")
        print("-"*40)
        for filename in files:
            target_file = f"{target_dir}/{filename}"
            if move_file(filename, target_file):
                moved_count += 1

    print()
    print("="*60)
    print(f"整理完成！共移动 {moved_count} 个文件")
    print("="*60)
    print()

    # 显示根目录剩余文件
    print("根目录剩余文件：")
    print("-"*40)
    remaining_files = [f for f in PROJECT_ROOT.iterdir()
                      if f.is_file() and not f.name.startswith('.')]
    for f in remaining_files:
        print(f"  {f.name}")

if __name__ == "__main__":
    main()
