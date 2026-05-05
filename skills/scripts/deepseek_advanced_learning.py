#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS DeepSeek高级写作技巧学习系统
深入学习爆款小说的高级技巧和创作规律
"""

import sys
import json
import time
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "sk-f3246fbd1eef446e9a11d78efefd9bba"
BASE_URL = "https://api.deepseek.com"

def call_deepseek(prompt, system_prompt=None, temperature=0.8):
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
        "max_tokens": 6000
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=120)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"   ❌ API调用失败: {e}")
        return None

def learn_advanced_writing_techniques():
    """学习高级写作技巧"""
    print("\n" + "="*60)
    print("📖 学习高级写作技巧")
    print("="*60)

    system_prompt = """你是一位资深的小说写作导师，擅长剖析爆款小说的高级写作技巧。
请提供详尽、实用、可操作的写作技巧指导。"""

    prompt = """请详细介绍小说创作的高级写作技巧，包括：

1. **人物塑造高阶技巧**（30条以上）
   - 人物弧光设计
   - 人物关系网构建
   - 人物成长轨迹规划
   - 人物标签设定

2. **情节设计高阶技巧**（30条以上）
   - 多线叙事交织
   - 伏笔回收体系
   - 反转与铺垫
   - 节奏把控

3. **场景描写高阶技巧**（25条以上）
   - 五感描写
   - 氛围营造
   - 视角切换
   - 蒙太奇手法

4. **对话写作高阶技巧**（20条以上）
   - 潜台词设计
   - 人物语言风格化
   - 暗示与误导
   - 冲突对话

5. **情绪共鸣高阶技巧**（25条以上）
   - 读者情绪调动
   - 情感高潮设计
   - 悲剧/喜剧技巧
   - 代入感强化

请用JSON格式返回，包含技巧名称、说明、示例。"""

    result = call_deepseek(prompt, system_prompt, temperature=0.7)
    if result:
        output_file = "skills/level2/learnings/高级写作技巧库.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# 📖 高级写作技巧库\n\n")
            f.write("*由DeepSeek联网学习生成 | 更新时间：2026-05-02*\n\n")
            f.write(result)
        print(f"   ✅ 高级写作技巧库已保存")
        return True
    return False

def learn_novel_templates():
    """学习小说创作模板"""
    print("\n" + "="*60)
    print("📐 学习小说创作模板")
    print("="*60)

    prompt = """请提供各类小说的创作模板，包括：

1. **开篇模板库**（30个以上）
   - 各类小说的黄金开篇
   - 不同平台风格的开篇
   - 爆款开篇解析

2. **章节结构模板库**（25个以上）
   - 标准章节结构
   - 高潮章节结构
   - 过渡章节结构
   - 对话密集章节结构

3. **结尾模板库**（20个以上）
   - 爆款结局模板
   - 悬念留存模板
   - 情感收尾模板
   - 系列开篇模板

4. **类型化模板库**（每个类型5个以上）
   - 玄幻修仙模板
   - 都市异能模板
   - 女频言情模板
   - 悬疑推理模板
   - 科幻未来模板

请用JSON格式返回，包含模板名称、结构、示例、适用场景。"""

    system_prompt = """你是一位专业的小说模板设计师，擅长提炼和总结各类爆款小说的创作模式。"""

    result = call_deepseek(prompt, system_prompt, temperature=0.7)
    if result:
        output_file = "skills/level2/learnings/小说创作模板库.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# 📐 小说创作模板库\n\n")
            f.write("*由DeepSeek联网学习生成 | 更新时间：2026-05-02*\n\n")
            f.write(result)
        print(f"   ✅ 小说创作模板库已保存")
        return True
    return False

def deep_analyze_top_novels():
    """深度分析Top小说"""
    print("\n" + "="*60)
    print("🔍 深度分析Top小说")
    print("="*60)

    prompt = """请深度分析2026年最火的5本长篇小说，包括：

**每本小说分析：**
1. **基本信息**
   - 书名
   - 作者
   - 平台
   - 字数
   - 类型

2. **开篇分析**
   - 黄金三秒设计
   - 核心钩子
   - 期待感营造
   - 读者评论摘录

3. **世界观分析**
   - 世界设定
   - 力量体系
   - 社会结构
   - 创新点

4. **人物分析**
   - 主角人设
   - 人物弧光
   - 配角亮点
   - 读者最爱角色

5. **剧情结构分析**
   - 三幕结构
   - 主线设计
   - 支线安排
   - 节奏曲线

6. **爆款要素拆解**
   - 核心卖点
   - 爽点密度
   - 反转设计
   - 成功原因

7. **可复制经验**
   - 写作技巧总结
   - 可复用模式
   - 学习建议

**请分析5本小说，覆盖不同类型：**
1. 玄幻修仙
2. 都市异能
3. 女频言情
4. 悬疑推理
5. 科幻未来

请用JSON格式返回，详尽、实用。"""

    system_prompt = """你是一位资深的网文分析师，掌握2026年最新的爆款小说数据和趋势。"""

    result = call_deepseek(prompt, system_prompt, temperature=0.8)
    if result:
        output_file = "skills/level2/learnings/Top小说深度分析.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# 🔍 Top小说深度分析\n\n")
            f.write("*由DeepSeek联网学习生成 | 更新时间：2026-05-02*\n\n")
            f.write(result)
        print(f"   ✅ Top小说深度分析已保存")
        return True
    return False

def learn_marketing_and_algorithm():
    """学习平台算法和营销知识"""
    print("\n" + "="*60)
    print("📊 学习平台算法和营销知识")
    print("="*60)

    prompt = """请详细介绍网文平台的推荐算法和营销策略，包括：

1. **各平台算法解析**
   - 起点中文网推荐机制
   - 番茄小说推荐机制
   - 晋江文学城推荐机制
   - 其他主流平台算法特点

2. **书皮和简介优化**
   - 爆款书名公式
   - 简介钩子设计
   - 封面设计要点
   - 标签选择技巧

3. **更新策略**
   - 更新时间选择
   - 更新字数建议
   - 存稿准备
   - 预热与冲榜

4. **读者互动策略**
   - 书评区运营
   - 本章说回复
   - 加更活动设计
   - 读者群运营

5. **数据监测与优化**
   - 关键数据指标
   - 数据解读方法
   - 问题定位与优化
   - A/B测试实践

请用JSON格式返回，实用、可操作。"""

    system_prompt = """你是一位资深的网文运营专家，精通各平台算法和营销策略。"""

    result = call_deepseek(prompt, system_prompt, temperature=0.7)
    if result:
        output_file = "skills/level2/learnings/平台算法与营销库.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# 📊 平台算法与营销库\n\n")
            f.write("*由DeepSeek联网学习生成 | 更新时间：2026-05-02*\n\n")
            f.write(result)
        print(f"   ✅ 平台算法与营销库已保存")
        return True
    return False

def generate_skill_upgrade_suggestions():
    """生成Skill升级建议"""
    print("\n" + "="*60)
    print("💡 生成Skill升级建议")
    print("="*60)

    prompt = """基于前面的学习内容，为NWACS系统提供Skill升级建议，包括：

1. **现有Skill增强建议**
   - 世界观构造师增强
   - 剧情构造师增强
   - 角色塑造师增强
   - 场景构造师增强
   - 对话设计师增强
   - 战斗设计师增强
   - 写作技巧大师增强

2. **新Skill设计建议**
   - 算法优化师（针对平台算法）
   - 爆款书皮设计师
   - 营销策划师
   - 读者互动师
   - 数据分析专家
   - 节奏控制大师
   - 情绪共振师

3. **Skill协作优化**
   - 多Skill协作流程
   - 依赖关系优化
   - 并行执行策略

请用JSON格式返回，包含Skill名称、功能描述、优化方案、优先级。"""

    system_prompt = """你是一位AI写作系统架构师，擅长设计和优化Skill系统。"""

    result = call_deepseek(prompt, system_prompt, temperature=0.7)
    if result:
        output_file = "skills/level2/learnings/Skill升级建议库.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# 💡 Skill升级建议库\n\n")
            f.write("*由DeepSeek联网学习生成 | 更新时间：2026-05-02*\n\n")
            f.write(result)
        print(f"   ✅ Skill升级建议库已保存")
        return True
    return False

def main():
    print("="*60)
    print("🚀 NWACS DeepSeek高级学习系统")
    print("="*60)

    start_time = datetime.now()
    print(f"\n启动时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    tasks = [
        ("高级写作技巧", learn_advanced_writing_techniques),
        ("小说创作模板", learn_novel_templates),
        ("Top小说深度分析", deep_analyze_top_novels),
        ("平台算法与营销", learn_marketing_and_algorithm),
        ("Skill升级建议", generate_skill_upgrade_suggestions)
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
            time.sleep(3)

    end_time = datetime.now()

    print("\n" + "="*60)
    print("🎉 学习完成！")
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

    print("\n生成的文件:")
    print("  1. 高级写作技巧库.md")
    print("  2. 小说创作模板库.md")
    print("  3. Top小说深度分析.md")
    print("  4. 平台算法与营销库.md")
    print("  5. Skill升级建议库.md")

    print("\n💡 学习内容已保存，可用于：")
    print("  - 提升写作技巧")
    print("  - 创作模板复用")
    print("  - 平台算法优化")
    print("  - Skill系统升级")

if __name__ == "__main__":
    main()
