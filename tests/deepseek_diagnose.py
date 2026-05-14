#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS DeepSeek智能诊断与修复
使用DeepSeek API诊断Python环境和系统问题
"""
import os
import sys
import json
import subprocess
from pathlib import Path

# DeepSeek API配置
API_KEY = "sk-f3246fbd1eef446e9a11d78efefd9bba"
API_URL = "https://api.deepseek.com/v1/chat/completions"

PROJECT_ROOT = Path(__file__).parent

print("="*70)
print("🔍 NWACS DeepSeek智能诊断")
print("="*70)
print()

def check_environment():
    """检查环境问题"""
    print("[1/3] 检查环境...")
    issues = []

    # 检查Python
    try:
        result = subprocess.run([sys.executable, "--version"],
                              capture_output=True, text=True, timeout=5)
        print(f"   Python: {result.stdout.strip()}")
    except Exception as e:
        issues.append(f"Python执行失败: {e}")

    # 检查模块导入
    modules_to_check = ["http.server", "json", "pathlib", "subprocess"]
    for mod in modules_to_check:
        try:
            __import__(mod)
            print(f"   ✅ {mod}")
        except:
            print(f"   ❌ {mod}")
            issues.append(f"模块导入失败: {mod}")

    return issues

def ask_deepseek_diagnosis(issues):
    """使用DeepSeek诊断问题"""
    print()
    print("[2/3] DeepSeek分析中...")

    prompt = f"""
我正在运行一个Python服务器脚本，但在Windows PowerShell上没有任何反应。

Python版本: {sys.version}
问题列表: {issues}

可能的原因：
1. Python未正确安装或路径问题
2. 脚本执行被阻止（如执行策略）
3. 端口被占用
4. 编码问题导致输出不显示

请分析最可能的问题，并提供：
1. 诊断结论
2. 具体的PowerShell命令来验证
3. 修复步骤

请用中文回答，命令要具体可执行。
"""

    try:
        import requests

        data = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.post(API_URL, json=data, headers=headers, timeout=30)
        result = response.json()

        if "choices" in result:
            diagnosis = result["choices"][0]["message"]["content"]
            print()
            print("="*70)
            print("🔍 DeepSeek诊断结果:")
            print("="*70)
            print(diagnosis)
            print("="*70)
            return diagnosis
        else:
            print(f"   API错误: {result}")
            return None

    except Exception as e:
        print(f"   DeepSeek请求失败: {e}")
        return None

def main():
    print()
    issues = check_environment()
    diagnosis = ask_deepseek_diagnosis(issues)

    print()
    print("[3/3] 生成修复方案...")

    if diagnosis:
        # 保存诊断结果
        report_path = PROJECT_ROOT / "诊断报告.txt"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(f"NWACS诊断报告\n")
            f.write(f"时间: 2026-05-02\n")
            f.write(f"Python版本: {sys.version}\n")
            f.write(f"问题: {', '.join(issues)}\n\n")
            f.write("DeepSeek诊断:\n")
            f.write(diagnosis)

        print(f"   ✅ 诊断报告已保存: {report_path}")

    print()
    print("="*70)
    print("请根据DeepSeek的诊断结果执行修复命令")
    print("="*70)

if __name__ == "__main__":
    main()
