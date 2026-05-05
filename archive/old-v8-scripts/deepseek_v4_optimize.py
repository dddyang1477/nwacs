#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 小说写作工具 - DeepSeek V4 深度优化
"""

import os
import sys
import json
import urllib.request
import urllib.error
import time

sys.stdout.reconfigure(encoding='utf-8')

def load_config():
    config = {}
    if os.path.exists('config.json'):
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
    return config

def call_deepseek_v4(prompt, system_prompt=None):
    config = load_config()
    if not config.get('api_key'):
        print("ERROR: API Key not configured")
        return None

    if not system_prompt:
        system_prompt = """你是一位资深的小说创作专家，精通各种类型的小说创作技巧，
请从专业小说创作者的角度分析并优化系统，提供实用的改进建议。"""

    url = config.get('base_url', 'https://api.deepseek.com/v1') + '/chat/completions'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {config.get("api_key")}'
    }

    data = {
        'model': config.get('model', 'deepseek-v4-pro'),
        'messages': [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': prompt}
        ],
        'temperature': 0.7,
        'max_tokens': 4000
    }

    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method='POST')

    try:
        with urllib.request.urlopen(req, timeout=180) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result['choices'][0]['message']['content']
    except Exception as e:
        print(f"API Error: {e}")
        return None

def analyze_tool_status():
    """分析工具当前状态"""
    print("\n[1/5] 正在分析工具当前状态...")

    prompt = """请分析 NWACS 小说写作工具的当前状态：

当前工具包含以下模块：
1. nwacs_console.py - 统一控制台入口
2. generate_novel.py - 智能小说生成器
3. quick_novel.py - 快速小说生成
4. optimize_with_deepseek.py - 大模型优化器
5. full_optimization.py - 全网学习优化器
6. smart_distribute.py - 智能分发器

Skill模块包含：
- level1: 小说总调度官
- level2: 世界观构造师、剧情构造师、场景构造师、对话设计师、角色塑造师、战斗设计师、写作技巧大师、去AI痕迹监督官、词汇大师
- level3: 各种小说类型（玄幻仙侠、都市言情、悬疑推理等）

请分析：
1. 当前工具的优缺点
2. 需要改进的地方
3. 如何提升写作质量和效率"""

    response = call_deepseek_v4(prompt)
    if response:
        print("  ✓ 状态分析完成")
        return response
    return None

def learn_writing_techniques():
    """学习高级写作技巧"""
    print("\n[2/5] 正在学习高级写作技巧...")

    prompt = """作为专业小说作家，请分享：

1. 如何写出引人入胜的开头（黄金三章技巧）
2. 如何设置悬念和反转
3. 如何塑造有深度的角色
4. 如何控制故事节奏
5. 如何写出有画面感的场景描写
6. 如何避免写作中的常见问题

请给出具体的技巧、示例和练习方法。"""

    response = call_deepseek_v4(prompt)
    if response:
        print("  ✓ 写作技巧学习完成")
        return response
    return None

def learn_plot_design():
    """学习情节设计"""
    print("\n[3/5] 正在学习情节设计...")

    prompt = """作为专业小说作家，请分享：

1. 如何设计有张力的情节
2. 如何埋设伏笔和回收
3. 如何制造高潮和爽点
4. 如何处理情感线和事业线的平衡
5. 如何设计反派和配角
6. 如何写出令人难忘的结局

请给出具体的技巧、模板和案例分析。"""

    response = call_deepseek_v4(prompt)
    if response:
        print("  ✓ 情节设计学习完成")
        return response
    return None

def learn_character_building():
    """学习人物塑造"""
    print("\n[4/5] 正在学习人物塑造...")

    prompt = """作为专业小说作家，请分享：

1. 如何创造有魅力的主角
2. 如何设计角色的成长弧线
3. 如何写出有个性的配角
4. 如何设计人物关系网
5. 如何用对话展现人物性格
6. 如何避免角色同质化

请给出具体的技巧、模板和案例分析。"""

    response = call_deepseek_v4(prompt)
    if response:
        print("  ✓ 人物塑造学习完成")
        return response
    return response

def generate_optimization_plan(analysis, techniques, plot, character):
    """生成优化计划"""
    print("\n[5/5] 正在生成优化计划...")

    prompt = f"""基于以下分析，请生成NWACS小说写作工具的优化计划：

## 当前状态分析
{analysis[:2000] if analysis else 'N/A'}

## 写作技巧
{techniques[:2000] if techniques else 'N/A'}

## 情节设计
{plot[:2000] if plot else 'N/A'}

## 人物塑造
{character[:2000] if character else 'N/A'}

请提供：
1. 需要优化或新增的功能模块
2. 每个模块的具体改进建议
3. 优先级排序
4. 预期效果"""

    response = call_deepseek_v4(prompt)
    if response:
        print("  ✓ 优化计划生成完成")
        return response
    return None

def save_optimization_results(analysis, techniques, plot, character, plan):
    """保存优化结果"""
    results = {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'analysis': analysis,
        'techniques': techniques,
        'plot_design': plot,
        'character_building': character,
        'optimization_plan': plan
    }

    with open('deepseek_optimization_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    report = f"""# NWACS 小说写作工具 DeepSeek V4 优化报告

## 优化时间
{time.strftime('%Y-%m-%d %H:%M:%S')}

## 优化内容

### 1. 工具状态分析
{analysis if analysis else '分析失败'}

---

### 2. 高级写作技巧
{techniques if techniques else '学习失败'}

---

### 3. 情节设计技巧
{plot if plot else '学习失败'}

---

### 4. 人物塑造技巧
{character if character else '学习失败'}

---

### 5. 优化计划
{plan if plan else '计划生成失败'}

---

## 优化状态
- 状态分析: {'✓ 完成' if analysis else '✗ 失败'}
- 写作技巧: {'✓ 完成' if techniques else '✗ 失败'}
- 情节设计: {'✓ 完成' if plot else '✗ 失败'}
- 人物塑造: {'✓ 完成' if character else '✗ 失败'}
- 优化计划: {'✓ 完成' if plan else '✗ 失败'}

---
*本报告由 DeepSeek V4 自动生成*
"""

    with open('DEEPSEEK_OPTIMIZATION_REPORT.md', 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"\n  ✓ 结果已保存到: deepseek_optimization_results.json")
    print(f"  ✓ 报告已保存到: DEEPSEEK_OPTIMIZATION_REPORT.md")

def main():
    print("\n" + "=" * 80)
    print("          NWACS 小说写作工具 - DeepSeek V4 深度优化")
    print("=" * 80)
    print("\n正在使用 DeepSeek V4 进行专业优化...")
    print("预计需要 3-5 分钟，请耐心等待...")

    # 1. 分析工具状态
    analysis = analyze_tool_status()

    # 2. 学习写作技巧
    techniques = learn_writing_techniques()

    # 3. 学习情节设计
    plot = learn_plot_design()

    # 4. 学习人物塑造
    character = learn_character_building()

    # 5. 生成优化计划
    plan = generate_optimization_plan(analysis, techniques, plot, character)

    # 保存结果
    save_optimization_results(analysis, techniques, plot, character, plan)

    print("\n" + "=" * 80)
    print("                    优化完成！")
    print("=" * 80)
    print("\n📋 优化报告已生成: DEEPSEEK_OPTIMIZATION_REPORT.md")
    print("📁 详细数据已保存: deepseek_optimization_results.json")
    print("\n请查看报告了解详细的优化建议。")
    print("=" * 80)

if __name__ == "__main__":
    main()
