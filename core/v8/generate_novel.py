#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2026年爆火玄幻小说生成器
结合DeepSeek和NWACS共同创作
"""

import sys
import os
import json
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "sk-f3246fbd1eef446e9a11d78efefd9bba"
BASE_URL = "https://api.deepseek.com"

def call_deepseek(prompt, system_prompt=None, temperature=0.8):
    """调用DeepSeek API"""
    import requests
    try:
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
        response = requests.post(url, headers=headers, json=data, timeout=120)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"   ❌ API调用失败: {e}")
        return None

def generate_worldview():
    """生成完整的世界观"""
    print("\n" + "="*60)
    print("🌍 构建完整世界观")
    print("="*60)
    
    prompt = """请为一部2026年爆火的长篇玄幻小说构建完整的世界观。

要求要素：
1. 大陆名称和地理体系（包含多个区域）
2. 修炼体系（以修炼法术为主，炼丹、炼体、炼毒、炼器、御兽、阵法为辅）
3. 修炼境界（详细的等级划分）
4. 时间历史背景（包含上古、中古、近古等重要时期，有秘密埋笔）
5. 门派体系（三大古派、七大宗、三十门派，反派宗教，主要学院）
6. 世界观核心悬念（隐藏的真相、历史的谎言）
7. 世界观与现实社会的隐喻（如阶级固化、信息茧房等）

要求详细、有深度、有埋笔、适合150万字以上长篇小说。"""
    
    system_prompt = """你是一位顶尖的玄幻世界观设计大师，擅长构建逻辑自洽、有深度、有悬念的世界观系统。
你的设定特点：
1. 历史有多层真相，层层揭开
2. 修炼体系有代价，力量不是免费的
3. 门派之间有复杂的利益关系和历史恩怨
4. 有现实社会的隐喻，引发读者思考"""
    
    result = call_deepseek(prompt, system_prompt, temperature=0.8)
    
    if result:
        output_file = "novel/01_worldview.md"
        os.makedirs("novel", exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# 🌍 世界观设定\n\n")
            f.write(f"*由DeepSeek+NWACS生成 | {datetime.now().strftime('%Y-%m-%d')}*\n\n")
            f.write(result)
        print(f"   ✅ 世界观设定已保存")
        return result
    return None

def generate_characters():
    """生成主要人物模板"""
    print("\n" + "="*60)
    print("👥 设计主要人物")
    print("="*60)
    
    prompt = """请为一部2026年爆火的长篇玄幻小说设计完整的人物体系。

要求要素：
1. 男主角（1位）：苟道流、智斗流、有矛盾性格、有缺陷但有魅力
   - 性格特点、身材体型、服装及面目特征、擅长能力、成长弧光
2. 女主角（多位，至少4位）：性格鲜明、有独立人格、不是花瓶
   - 每位女主的性格、外形、擅长、与男主的关系发展
3. 重要配角（5-8位）：有独立故事线、能出圈的角色
4. 反派角色（多位）：不是脸谱化、有自己的"正确"、与主角有理念冲突
5. 小人物通用模板（5种典型）：用于填充故事世界

人物设计要符合2026年趋势：
- 主角：智者型、矛盾型、有秘密、不是完美英雄
- 反派：立场对立型、镜像型、系统型
- 配角：独立人格、悲剧美感、技能特色"""
    
    system_prompt = """你是一位顶尖的人物塑造大师，擅长设计立体、有魅力、能引发读者共鸣的角色。
你设计的人物特点：
1. 每个角色都有清晰的目标和恐惧
2. 角色之间有复杂的情感和利益关系
3. 正派和反派的界限不是绝对的
4. 人物有成长弧光，从开始到结束会变化"""
    
    result = call_deepseek(prompt, system_prompt, temperature=0.8)
    
    if result:
        output_file = "novel/02_characters.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# 👥 人物设定\n\n")
            f.write(f"*由DeepSeek+NWACS生成 | {datetime.now().strftime('%Y-%m-%d')}*\n\n")
            f.write(result)
        print(f"   ✅ 人物设定已保存")
        return result
    return None

def generate_systems():
    """生成修炼、丹药、阵法、法宝、法术等系统"""
    print("\n" + "="*60)
    print("⚙️  构建各种系统")
    print("="*60)
    
    prompt = """请为一部2026年爆火的长篇玄幻小说构建完整的系统体系。

需要构建的系统：
1. **修炼体系**：
   - 法术修炼体系（主体系）
   - 辅助修炼（炼丹、炼体、炼毒、炼器、御兽、阵法）
   - 境界等级划分，每个境界的特点和突破条件

2. **丹药系统**：
   - 丹药等级
   - 常见丹药、草药、毒药（每种的名称、外形、用途、用法）
   - 炼丹手法

3. **阵法系统**：
   - 阵法材料
   - 常见阵法（功能、规模、材料、布置方法）

4. **法宝系统**：
   - 法宝等级
   - 法宝形状、功能、炼制材料

5. **武器装备饰品系统**：
   - 常见武器、装备、饰品（形状、功能、炼制材料）

6. **法术系统**：
   - 法术等级体系
   - 各系法术名称、描述、威力、消耗

7. **妖兽系统**：
   - 妖兽等级
   - 常见妖兽（外形、能力、栖息地、弱点）

要求：系统要庞杂但有逻辑，适合长篇小说展开。"""
    
    system_prompt = """你是一位顶尖的玄幻系统设计大师，擅长构建复杂但逻辑自洽的修炼系统。
你设计的系统特点：
1. 每个系统都有代价，没有免费的午餐
2. 系统之间有关联，可以组合使用
3. 有深度，不是简单的数值堆叠
4. 有创新，不是重复老套路"""
    
    result = call_deepseek(prompt, system_prompt, temperature=0.8)
    
    if result:
        output_file = "novel/03_systems.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# ⚙️  系统设定\n\n")
            f.write(f"*由DeepSeek+NWACS生成 | {datetime.now().strftime('%Y-%m-%d')}*\n\n")
            f.write(result)
        print(f"   ✅ 系统设定已保存")
        return result
    return None

def generate_outline():
    """生成小说大纲和章节规划"""
    print("\n" + "="*60)
    print("📖 生成小说大纲")
    print("="*60)
    
    prompt = """请为一部2026年爆火的150万字以上长篇玄幻小说生成完整的大纲和章节规划。

小说要素：
- 类型：苟道流、智斗流、黑暗流、幕后流相结合
- 风格：热血、悬疑、治愈、搞笑相结合
- 字数：150万字以上
- 主角：智者型、有秘密、苟道发育、智斗取胜
- 剧情：多条主线辅线、埋笔、因果事件、反转

要求大纲包含：
1. **小说核心概念**（一句话简介、核心主题）
2. **主线剧情**（完整的故事脉络）
3. **多条辅线**（至少3条重要辅线）
4. **主要情节节点**（重要的情节点和反转点）
5. **埋笔和因果事件**（至少10个重要埋笔）
6. **分卷大纲**（按20-30万字一卷划分，每卷的剧情）
7. **章节规划**（每卷的章节安排，至少100章的规划）
8. **剧情节奏**（爽点密度、情绪曲线管理）

要符合2026年趋势：
- 开篇即高能
- 世界观悬念+情感羁绊×抉择压力
- 甜虐比例7:3
- 有现实社会隐喻"""
    
    system_prompt = """你是一位顶尖的玄幻小说大纲设计大师，擅长设计节奏紧凑、悬念迭起、情感饱满的长篇小说大纲。
你设计的大纲特点：
1. 开篇即抓住读者
2. 节奏松紧有度，爽点密集
3. 埋笔层层揭开，反转出人意料
4. 情感线与剧情线交织
5. 有深度，不只是爽文"""
    
    result = call_deepseek(prompt, system_prompt, temperature=0.8)
    
    if result:
        output_file = "novel/04_outline.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# 📖 小说大纲\n\n")
            f.write(f"*由DeepSeek+NWACS生成 | {datetime.now().strftime('%Y-%m-%d')}*\n\n")
            f.write(result)
        print(f"   ✅ 大纲已保存")
        return result
    return None

def generate_chapters():
    """生成小说开篇章节"""
    print("\n" + "="*60)
    print("📝 生成开篇章节")
    print("="*60)
    
    prompt = """请为这部2026年爆火的长篇玄幻小说撰写开篇章节（第1-10章）。

要求：
1. **第1章**：开篇即高能，打破读者预期，建立主角人设、核心冲突和第一个爽点
2. **第2-5章**：快速引入世界观，引入情感锚点，展示主角苟道和智斗特点
3. **第6-10章**：第一个小高潮，主角第一次用智斗解决问题，埋下重要埋笔

风格要求：
- 苟道流：主角谨慎、不装逼、暗中发育
- 智斗流：靠信息差和布局取胜，不是靠武力碾压
- 有悬念：每章结尾留钩子
- 有搞笑：适当的笑点，不沉闷
- 有治愈：温馨的情感时刻
- 有热血：关键时刻让人激动

字数：每章约2000-3000字"""
    
    system_prompt = """你是一位顶尖的玄幻小说作家，擅长写节奏紧凑、悬念迭起、人物鲜明的开篇。
你写作的特点：
1. 开篇一句话抓住读者
2. 每章结尾留钩子
3. 人物对话符合性格
4. 爽点不生硬，自然流露
5. 张弛有度，有节奏"""
    
    result = call_deepseek(prompt, system_prompt, temperature=0.85)
    
    if result:
        output_file = "novel/05_chapters.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# 📝 开篇章节\n\n")
            f.write(f"*由DeepSeek+NWACS生成 | {datetime.now().strftime('%Y-%m-%d')}*\n\n")
            f.write(result)
        print(f"   ✅ 开篇章节已保存")
        return result
    return None

def generate_summary():
    """生成完整的小说创作总结"""
    print("\n" + "="*60)
    print("📋 生成创作总结")
    print("="*60)
    
    prompt = """请为这部2026年爆火的长篇玄幻小说生成一份完整的创作总结和快速参考手册。

包含内容：
1. **小说基本信息**（书名、类型、字数、核心卖点）
2. **一句话简介**（吸引人的简介）
3. **核心亮点总结**（为什么这部小说能爆火）
4. **人物快速表**（所有主要人物的一句话介绍）
5. **世界观快速参考**（关键设定速查）
6. **剧情节奏指南**（每多少章一个爽点、一个高潮）
7. **写作风格要点**（保持风格的关键）
8. **后续剧情提示**（后续可以展开的方向）"""
    
    system_prompt = """你是一位专业的小说策划编辑，擅长总结和提炼作品的核心卖点。"""
    
    result = call_deepseek(prompt, system_prompt, temperature=0.7)
    
    if result:
        output_file = "novel/README.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# 📚 2026年爆火玄幻小说\n\n")
            f.write(f"*由DeepSeek+NWACS共同创作 | {datetime.now().strftime('%Y-%m-%d')}*\n\n")
            f.write(result)
        print(f"   ✅ 创作总结已保存")
        return result
    return None

def main():
    print("="*60)
    print("🔥 2026年爆火玄幻小说生成器")
    print("="*60)
    
    start_time = datetime.now()
    print(f"\n启动时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("正在使用DeepSeek+NWACS共同创作...\n")
    
    tasks = [
        ("世界观设定", generate_worldview),
        ("人物设定", generate_characters),
        ("系统设定", generate_systems),
        ("小说大纲", generate_outline),
        ("开篇章节", generate_chapters),
        ("创作总结", generate_summary)
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
    print("🎉 小说生成完成！")
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
    print("  1. novel/README.md - 小说创作总结（必读）")
    print("  2. novel/01_worldview.md - 完整世界观设定")
    print("  3. novel/02_characters.md - 主要人物设定")
    print("  4. novel/03_systems.md - 修炼、丹药、阵法等系统")
    print("  5. novel/04_outline.md - 小说大纲和章节规划")
    print("  6. novel/05_chapters.md - 开篇章节（第1-10章）")
    
    print("\n" + "="*60)
    print("📖 小说核心卖点预览")
    print("="*60)
    print("""
✨ 类型：苟道流 + 智斗流 + 黑暗流 + 幕后流
🎭 风格：热血 + 悬疑 + 治愈 + 搞笑
📚 字数：150万字以上
🌟 核心亮点：
   - 智者型主角，靠信息差和布局取胜
   - 有代价的修炼，力量不是免费的
   - 多层世界观真相，层层揭开
   - 立场对立型反派，不是脸谱化
   - 甜虐交织，情感线与剧情线深度绑定
   - 有现实社会隐喻，引发读者思考
""")

if __name__ == "__main__":
    main()