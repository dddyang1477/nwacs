#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS目录整理优化
使用DeepSeek分析当前目录结构并生成整理方案
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# 添加项目根目录到路径
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

# DeepSeek API配置
API_KEY = "sk-f3246fbd1eef446e9a11d78efefd9bba"
BASE_URL = "https://api.deepseek.com"

# 当前目录结构
CURRENT_DIRS = [
    ".git", ".trae", "archive", "backup", "config", "core", "docs",
    "examples", "learning", "logs", "maintenance", "manuscripts",
    "novel-mcp-server-v2", "novels", "novel_creation", "novel_project",
    "output", "records", "skills", "src", "temp_backup", "tests", "tools",
    "web_ui", "__pycache__"
]

CURRENT_FILES = [
    "config.json", "deepseek_classics_learning.py", "deepseek_learning_engine.py",
    "deepseek_online_optimize.py", "deepseek_optimization_report.txt",
    "enterprise_comparison.py", "feishu_auto_demo.py", "feishu_command_server.py",
    "FEISHU_DEBUG.md", "feishu_debug.py", "feishu_deepseek_diagnosis.py",
    "feishu_final_test.py", "feishu_server_v2.py", "feishu_simple_test.py",
    "feishu_test_send.py", "install_ngrok.bat", "install_ngrok_en.bat",
    "learn_now.bat", "main.py", "manual_feishu_test.py", "nwacs_main.py",
    "NWACS_v7.0_二次优化完成总结.md", "NWACS_v7.0_优化完成总结.md",
    "NWACS全面优化完成总结.md", "NWACS最终优化完成总结.md",
    "quick_check.py", "quick_feishu_test.py", "quick_learning_test.bat",
    "quick_learning_test.py", "QUICK_START.md", "run_learning_quick.py",
    "run_learning_test.bat", "run_learning_test.py", "run_test.bat",
    "run_test_en.bat", "server_simple.py", "setup_feishu.py",
    "simple_evaluator.py", "simple_feishu_test.py", "simple_learning.py",
    "simple_test.py", "specialized_learning.py", "start_auto_learn.bat",
    "start_auto_learn.py", "start_feishu_server.bat", "start_feishu_server.py",
    "start_nwacs.bat", "start_nwacs_main.bat", "start_server.bat",
    "test_feishu.ps1", "test_feishu.py", "test_output.py", "test_port.py",
    "test_python_env.py", "test_server.py", "WRITING_TOOLS_GUIDE.md",
    "启动API服务.bat", "启动DeepSeek评测.bat", "启动NWACS.bat",
    "启动创作引擎.bat", "启动功能测试.bat", "启动团队协作.bat",
    "启动微信集成.bat", "启动知识库管理.bat", "启动诊断工具.bat",
    "启动超级启动器.bat", "启动飞书指令服务器.bat", "启动飞书集成.bat",
    "小说大纲_缄默天师.txt", "项目状态报告.md", "飞书指令服务器配置指南.md"
]

def call_deepseek(prompt, system_prompt=None):
    """调用DeepSeek API"""
    import requests

    url = f"{BASE_URL}/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    data = {
        "model": "deepseek-chat",
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 4000
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=60)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"API调用失败: {e}")
        return None

def generate_organization_plan():
    """生成目录整理方案"""

    system_prompt = """你是一个专业的项目架构师和文件系统整理专家。你的任务是为一个AI小说创作系统（NWACS）设计一个清晰、合理的目录结构。

请考虑以下原则：
1. 核心代码与资源分离
2. 小说输出专门管理
3. 测试脚本集中存放
4. 文档独立组织
5. 工具脚本归类
6. 保留git历史
7. 提供迁移脚本
"""

    prompt = f"""请分析以下NWACS项目的当前目录结构，并生成一个整理优化方案：

当前目录：
- 文件夹：{CURRENT_DIRS}
- 根目录文件：{CURRENT_FILES}

请生成：
1. 推荐的新目录结构（用树状图表示）
2. 文件归类方案（每个文件该移动到哪里）
3. 迁移脚本（Python或PowerShell脚本）
4. 注意事项和验证步骤

特别要求：
- 小说输出统一放在 novels/小说名/ 目录下
- 测试脚本放在 tests/ 下
- 临时测试脚本放在 temp_tests/ 下
- 文档保持在 docs/ 下
- 批处理启动脚本放在 scripts/ 下
- 核心代码保持在 core/、skills/ 下
- 配置保持在 config/ 下
- 不要移动 .git 文件夹

请用中文回答，格式清晰易读。
"""

    result = call_deepseek(prompt, system_prompt)
    return result

def main():
    print("="*60)
    print("NWACS目录整理优化")
    print("="*60)
    print()

    print("正在分析目录结构并生成整理方案...")
    plan = generate_organization_plan()

    if plan:
        print()
        print("="*60)
        print("整理方案生成完成！")
        print("="*60)
        print()
        print(plan)

        # 保存方案
        plan_file = PROJECT_ROOT / "directory_organization_plan.txt"
        with open(plan_file, 'w', encoding='utf-8') as f:
            f.write(plan)
        print()
        print(f"方案已保存到: {plan_file}")

    else:
        print("生成方案失败，请检查网络连接或API密钥")

if __name__ == "__main__":
    main()
