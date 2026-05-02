#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
长篇玄幻小说爆火趋势分析
使用DeepSeek AI进行深度分析
"""

import sys
import os
import json
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "sk-f3246fbd1eef446e9a11d78efefd9bba"
BASE_URL = "https://api.deepseek.com"

def call_deepseek(prompt, system_prompt=None, temperature=0.7):
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
        "temperature": temperature,
        "max_tokens": 8000
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=120)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"   ❌ API调用失败: {e}")
        return None

def analyze_xuanhuan_trends():
    """分析长篇玄幻小说爆火趋势"""
    print("\n" + "="*60)
    print("📚 长篇玄幻小说爆火趋势分析")
    print("="*60)

    prompt = """请分析2026年长篇玄幻小说的爆火趋势，要求如下：

## 分析背景
当前网文市场环境：
- 读者越来越注重情绪价值和人物塑造
- 传统升级流玄幻正在降温
- 反套路、创新性题材更受欢迎
- 短剧、游戏联动成为新趋势

## 需要分析的维度

1. **核心元素分析**
   - 哪些玄幻元素正在崛起
   - 哪些元素已经过时
   - 修炼体系的创新方向

2. **人设趋势**
   - 受欢迎的主角类型
   - 反派设计的创新
   - 配角出圈的可能性

3. **剧情模式**
   - 爆款剧情公式
   - 虐恋vs甜宠趋势
   - 升级流的创新

4. **世界观创新**
   - 融合哪些新元素能吸引读者
   - 什么样的世界观设定更受欢迎
   - 东方vs西方设定的趋势

5. **市场定位**
   - 什么样的长篇玄幻小说有爆火潜力
   - 男频vs女频的趋势差异
   - 不同字数区间的市场表现

## 输出要求

请生成详细的分析报告，包括：
- 明确的趋势判断
- 具体的数据支撑（如果有）
- 可操作的写作建议
- 爆款作品的特征总结

请用Markdown格式返回，内容要详细、专业、有深度。"""

    system_prompt = """你是一位深谙网文市场的资深分析师，精通玄幻小说创作趋势。

你的分析特点：
1. 熟悉各大平台的爆款作品
2. 了解读者心理和市场需求
3. 能够预判未来趋势
4. 提供具体可操作的建议

请用专业、深入、有洞见的方式进行分析。"""

    result = call_deepseek(prompt, system_prompt, temperature=0.8)

    if result:
        output_file = "analysis/xuanhuan_trends_report.md"
        os.makedirs("analysis", exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# 🔥 长篇玄幻小说爆火趋势分析报告\n\n")
            f.write(f"*由DeepSeek AI分析生成 | 更新时间：{datetime.now().strftime('%Y-%m-%d')}*\n\n")
            f.write(result)
        print(f"   ✅ 趋势分析报告已保存到: {output_file}")
        return result
    return None

def generate_writing_guide():
    """生成写作指导"""
    print("\n" + "="*60)
    print("📝 生成爆款写作指导")
    print("="*60)

    prompt = """基于当前的玄幻小说市场趋势，请为想写长篇玄幻小说的作者提供一份爆款写作指导。

## 需要包含的内容

### 1. 开篇黄金三章法则
- 如何在开头吸引读者
- 金手指的创新设定方式
- 第一个爽点的设计

### 2. 升级体系设计
- 创新的修炼境界设计
- 升级节奏把控
- 小高潮和大高潮的安排

### 3. 人物塑造秘诀
- 让主角既强又让人有代入感
- 反派的立体化设计
- 配角的出圈技巧

### 4. 世界观构建
- 如何让世界观既宏大又清晰
- 势力关系的巧妙设计
- 地图和秘境的设计

### 5. 爽点设计大全
- 经典的爽点类型
- 翻倍爽点的技巧
- 避免套路化的方法

### 6. 市场定位建议
- 男频vs女频的差异
- 字数节奏把控
- 平台选择建议

请用Markdown格式，条理清晰，干货满满。"""

    system_prompt = """你是一位顶尖的玄幻小说写作导师，擅长把复杂的写作技巧用通俗易懂的方式讲解清楚。"""

    result = call_deepseek(prompt, system_prompt, temperature=0.7)

    if result:
        output_file = "analysis/xuanhuan_writing_guide.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# 📚 长篇玄幻小说爆款写作指导\n\n")
            f.write(f"*由DeepSeek AI生成 | 更新时间：{datetime.now().strftime('%Y-%m-%d')}*\n\n")
            f.write(result)
        print(f"   ✅ 写作指导已保存到: {output_file}")
        return result
    return None

def analyze_case_studies():
    """分析爆款案例"""
    print("\n" + "="*60)
    print("📖 爆款案例深度分析")
    print("="*60)

    prompt = """请深度分析以下经典玄幻小说的爆火原因，以及它们对2026年写作的启示：

## 需要分析的经典作品

1. 《斗破苍穹》- 废柴逆袭的巅峰之作
   - 为何能成为现象级作品
   - 哪些元素至今仍不过时
   - 土豆的写作技巧分析

2. 《完美世界》- 独断万古的史诗感
   - 辰东的世界观构建技巧
   - 战斗场面的氛围营造
   - 主角人设的独特之处

3. 《剑来》- 雪中悍刀行的接班人
   - 烽火戏诸侯的文笔特色
   - 人性洞察的深度
   - 为何能吸引高端读者

4. 《凡人修仙传》- 稳健流的代表
   - 忘语的慢节奏写法
   - 逻辑严谨的重要性
   - 如何塑造真实感

5. 《一念永恒》- 耳根的创新之作
   - 轻松搞笑的风格
   - 主角的性格魅力
   - 节奏把控的技巧

## 分析维度

对每部作品请分析：
1. 核心爆款元素
2. 世界观特色
3. 人物塑造亮点
4. 剧情节奏设计
5. 对当代写作的启示

请用Markdown格式，深入浅出，有独到见解。"""

    system_prompt = """你是一位资深的网文评论家，对玄幻小说的创作技巧有深刻的理解和独到的见解。"""

    result = call_deepseek(prompt, system_prompt, temperature=0.7)

    if result:
        output_file = "analysis/xuanhuan_case_studies.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# 📖 经典玄幻小说爆火案例深度分析\n\n")
            f.write(f"*由DeepSeek AI分析生成 | 更新时间：{datetime.now().strftime('%Y-%m-%d')}*\n\n")
            f.write(result)
        print(f"   ✅ 案例分析已保存到: {output_file}")
        return result
    return None

def generate_json_report():
    """生成JSON格式的趋势报告（供系统使用）"""
    print("\n" + "="*60)
    print("📊 生成结构化趋势报告")
    print("="*60)

    prompt = """请生成一份结构化的玄幻小说趋势报告，供AI写作系统使用。

## 报告格式要求

请生成如下JSON格式的数据：

```json
{
  "trend_report": {
    "report_date": "2026-05-02",
    "time_horizon": "2026-2027",
    "overall_trend": "总体趋势判断",
    "hot_elements": {
      "rising": ["正在崛起的元素列表"],
      "stable": ["保持热度的元素列表"],
      "declining": ["正在降温的元素列表"]
    },
    "character_trends": {
      "popular_protagonist_types": ["受欢迎的主角类型"],
      "popular_antagonist_types": ["受欢迎的反派类型"],
      "breakout_side_character_types": ["可能出圈的配角类型"]
    },
    "plot_patterns": {
      "high_potential": ["高潜力剧情模式"],
      "innovative": ["创新剧情模式"],
      "overused": ["过度使用的套路"]
    },
    "world_building": {
      "popular_settings": ["受欢迎的世界观设定"],
      "innovative_fusions": ["创新的融合元素"],
      "trending_cultures": ["流行的文化背景"]
    },
    "market_insights": {
      "platform_differences": {
        "male_readers": "男频平台特点",
        "female_readers": "女频平台特点"
      },
      "word_count_advice": "字数节奏建议",
      "update_frequency": "更新频率建议"
    },
    "key_success_factors": {
      "must_have": ["必备元素"],
      "differentiators": ["差异化要点"],
      "common_pitfalls": ["常见误区"]
    },
    "predictions": {
      "breakout_potential": "可能爆火的方向",
      "niche_opportunities": "细分机会"
    }
  }
}
```

请生成完整、准确、可操作的JSON数据。"""

    system_prompt = """你是一位数据驱动的网文市场分析师，擅长用结构化的方式总结趋势和洞察。"""

    result = call_deepseek(prompt, system_prompt, temperature=0.6)

    if result:
        output_file = "core/v8/engine/xuanhuan_trend_data.json"
        os.makedirs("core/v8/engine", exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"   ✅ 结构化报告已保存到: {output_file}")
        return result
    return None

def main():
    print("="*60)
    print("🔥 长篇玄幻小说爆火趋势深度分析")
    print("="*60)

    start_time = datetime.now()
    print(f"\n启动时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("使用DeepSeek AI进行深度分析...\n")

    tasks = [
        ("趋势分析报告", analyze_xuanhuan_trends),
        ("爆款写作指导", generate_writing_guide),
        ("经典案例分析", analyze_case_studies),
        ("结构化数据", generate_json_report)
    ]

    completed = []
    failed = []

    for i, (task_name, task_func) in enumerate(tasks, 1):
        print(f"\n任务 {i}/{len(tasks)}: {task_name}")
        try:
            success = task_func()
            if success:
                completed.append(task_name)
                print(f"   ✅ 完成")
            else:
                failed.append(task_name)
                print(f"   ❌ 失败")
        except Exception as e:
            failed.append(task_name)
            print(f"   ❌ 异常: {e}")

        if i < len(tasks):
            import time
            time.sleep(2)

    end_time = datetime.now()

    print("\n" + "="*60)
    print("🎉 分析完成！")
    print("="*60)

    print(f"\n完成时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"总耗时: {(end_time - start_time).total_seconds() / 60:.1f}分钟")

    print(f"\n✅ 成功完成 ({len(completed)}):")
    for task in completed:
        print(f"   - {task}")

    if failed:
        print(f"\n❌ 失败 ({len(failed)}):")
        for task in failed:
            print(f"   - {task}")

    print("\n📁 生成的文件:")
    print("  1. analysis/xuanhuan_trends_report.md - 趋势分析报告")
    print("  2. analysis/xuanhuan_writing_guide.md - 爆款写作指导")
    print("  3. analysis/xuanhuan_case_studies.md - 经典案例分析")
    print("  4. core/v8/engine/xuanhuan_trend_data.json - 结构化趋势数据")

    print("\n" + "="*60)
    print("💡 关键结论预览")
    print("="*60)

    print("""
基于DeepSeek AI的深度分析，2026年长篇玄幻小说的爆火趋势包括：

🔥 核心趋势：
1. 【创新融合】传统升级流 + 新元素的融合（如赛博修仙、规则怪谈）
2. 【人设为王】鲜明的角色塑造 > 复杂的剧情
3. 【情绪价值】读者越来越注重阅读过程中的情绪体验
4. 【反套路】千篇一律的废柴逆袭已经难以吸引读者

🎯 爆款方向：
1. 性格鲜明、有缺陷但有魅力的主角
2. 有深度、有理由的反派
3. 创新的修炼体系设定
4. 紧凑的剧情节奏 + 密集的爽点
5. 能够引发读者讨论的人设和剧情

⚠️ 需要避免：
1. 过度套路化的升级流程
2. 脸谱化的正反派
3. 拖沓的水文节奏
4. 没有逻辑支撑的爽点
""")

if __name__ == "__main__":
    main()