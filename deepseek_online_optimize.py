#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS DeepSeek 在线优化分析
使用DeepSeek联网分析系统并提供优化建议
"""
import os
import sys
import json
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent
API_KEY = "sk-f3246fbd1eef446e9a11d78efefd9bba"
API_URL = "https://api.deepseek.com/v1/chat/completions"

print("="*80)
print("🚀 NWACS DeepSeek 在线优化分析")
print("="*80)
print()
print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

def load_system_info():
    """加载系统信息"""
    info = {
        "files": [],
        "config": None,
        "skills": [],
        "knowledge_bases": []
    }

    # 扫描文件
    for ext in ['*.py', '*.md', '*.json', '*.txt', '*.bat']:
        files = list(PROJECT_ROOT.rglob(ext))
        for f in files[:20]:
            if 'node_modules' not in str(f) and '__pycache__' not in str(f):
                info["files"].append(f.name)

    # 加载配置
    config_path = PROJECT_ROOT / "config" / "feishu_config.json"
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            info["config"] = json.load(f)

    # 统计Skill文件
    skills_dir = PROJECT_ROOT / "skills" / "level2"
    if skills_dir.exists():
        info["skills"] = [f.name for f in skills_dir.glob("*.md")]

    # 统计知识库
    kb_dir = PROJECT_ROOT / "skills" / "level2" / "learnings"
    if kb_dir.exists():
        info["knowledge_bases"] = [f.name for f in kb_dir.glob("*.txt")]

    return info

def create_optimization_prompt(system_info):
    """创建优化提示词"""
    prompt = f"""
# NWACS (Novel Writing AI Collaborative System) v7.0 系统分析

## 系统概况
- 版本: v7.0
- 架构: v2.2
- 时间: {datetime.now().strftime('%Y-%m-%d')}

## 文件结构
主要文件: {', '.join(system_info['files'][:15])}

## 配置情况
飞书配置: {'已配置' if system_info['config'] else '未配置'}
Webhook: {system_info['config'].get('webhook_url', 'N/A') if system_info['config'] else 'N/A'}

## Skill系统
共有 {len(system_info['skills'])} 个Skill文件
包括: {', '.join(system_info['skills'][:10])}

## 知识库
共有 {len(system_info['knowledge_bases'])} 个知识库
包括: {', '.join(system_info['knowledge_bases'][:10])}

## 当前完成的功能
1. ✅ 35个知识库系统
2. ✅ 28个Level 3 Skill (v7.0/v8.0)
3. ✅ 核心Skill优化 (写作技巧、创新灵感、大纲架构)
4. ✅ 飞书单向通信 (NWACS→飞书)
5. ✅ DeepSeek联网学习引擎
6. ✅ 自动空闲学习系统

## 已知的限制
1. 飞书双向通信需要ngrok内网穿透
2. Python环境有时需要使用 'py' 命令
3. 批处理文件编码问题

## 需要分析的问题
请分析以下方面：

1. **系统架构优化**
   - 当前架构是否合理？
   - 有哪些可以优化的地方？

2. **功能完整性**
   - 相比企业级写作工具还缺什么？
   - 知识储备是否充足？

3. **代码质量**
   - 核心代码是否有bug或问题？
   - 哪些地方可以改进？

4. **用户体验**
   - 启动和配置流程是否顺畅？
   - 有哪些可以简化的地方？

5. **具体优化建议**
   - 列出3-5个最优先的优化项
   - 每个优化项给出具体实施步骤

请用中文回答，给出详细的技术建议！
"""
    return prompt

def call_deepseek(prompt):
    """调用DeepSeek API"""
    print("🤖 正在联网分析...")
    print()

    try:
        import requests

        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "你是NWACS系统优化专家，擅长分析系统架构、优化代码、提升用户体验。"},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 2000
        }

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.post(API_URL, json=data, headers=headers, timeout=60)

        if response.status_code == 200:
            result = response.json()
            content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
            return content
        else:
            print(f"❌ API错误: {response.status_code}")
            return None

    except Exception as e:
        print(f"❌ DeepSeek调用失败: {e}")
        return None

def main():
    print("📊 加载系统信息...")
    system_info = load_system_info()

    print(f"   文件数: {len(system_info['files'])}")
    print(f"   Skill数: {len(system_info['skills'])}")
    print(f"   知识库: {len(system_info['knowledge_bases'])}")
    print()

    print("🔍 正在联网分析系统...")
    prompt = create_optimization_prompt(system_info)

    analysis = call_deepseek(prompt)

    if analysis:
        print()
        print("="*80)
        print("📊 DEEPSEEK 分析结果")
        print("="*80)
        print(analysis)
        print("="*80)

        # 保存报告
        report_path = PROJECT_ROOT / "deepseek_optimization_report.txt"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(f"NWACS DeepSeek 优化分析报告\n")
            f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*80 + "\n\n")
            f.write(analysis)

        print()
        print(f"✅ 报告已保存: {report_path}")
    else:
        print("❌ 分析失败")

    print()
    print("完成!")

if __name__ == "__main__":
    main()
