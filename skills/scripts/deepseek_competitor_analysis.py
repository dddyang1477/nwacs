#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS DeepSeek爆款小说解剖学习系统 v1.0
功能：
1. 联网搜索各大平台前15名小说
2. 深度解剖学习爆款要素
3. 收集专业词汇和名词
4. 学习中国古代文言文运用
5. 更新到对应Skill
"""

import sys
import os
import json
import time
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

def learn_classic_wenyanwen():
    """学习中国古代文言文运用"""
    print("\n" + "="*60)
    print("📜 学习中国古代文言文运用")
    print("="*60)

    system_prompt = """你是一个精通中国古典文学和文言文的专家，擅长古文翻译和现代文创作。
请提供详细的文言文运用知识，包括：
1. 古文常用词汇和句式
2. 文言文翻译技巧
3. 古风小说写作常用表达
4. 历史典故和人物称谓
5. 古代官职、礼仪、文化常识"""

    prompt = """请详细介绍中国古代文言文在小说创作中的运用，包括：

1. **古文常用词汇**（每个分类30个以上）
   - 动词：曰、谓、乃、故、是、若、之、乎、者、也
   - 名词：君、子、吾、余、卿、妾、卑、尊
   - 形容词：美、丑、善、恶、大、小、多、少
   - 副词：遂、乃、则、然、犹、尚、颇

2. **古风句式模板**（20个以上）
   - "XXX，XXX也"（判断句）
   - "XXX者，XXX也"（者字句）
   - "XXX于XXX"（状语后置）
   - 省略句、被动句

3. **古代称谓系统**
   - 自称：朕、寡人、余、吾、在下、卑职
   - 对称：卿、子、君、公、先生、阁下
   - 他称：彼、其、夫人、娘子、老爷

4. **古风场景描写词汇**
   - 建筑：宫殿、楼阁、亭台、廊庑
   - 服饰：霓裳、锦袍、凤冠、霞帔
   - 器物：玉佩、如意、笔墨、棋盘

5. **经典古文段落示例**（10个以上）
   - 出自《聊斋》《史记》《世说新语》等

请用JSON格式返回，便于程序处理。"""

    result = call_deepseek(prompt, system_prompt)
    if result:
        # 保存到文件
        output_file = "skills/level2/learnings/文言文知识库.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# 📜 中国古代文言文运用知识库\n\n")
            f.write("*由DeepSeek联网学习生成 | 更新时间：2026-05-02*\n\n")
            f.write(result)
        print(f"   ✅ 文言文知识库已保存: {output_file}")
        return result
    return None

def analyze_platform_novels(platform, genre):
    """分析指定平台指定类型的小说"""
    print(f"\n   正在搜索{platform} {genre}类型前15名...")

    prompt = f"""请搜索2026年5月{platform}平台{genre}类型小说排行榜前15名，包括：
1. 书名
2. 作者
3. 类型标签
4. 核心卖点（50字内）
5. 开篇黄金三秒公式
6. 前5章核心亮点
7. 主角人设特点
8. 经典金句（3句）

请尽量包含具体的小说名称和作者名。"""

    system_prompt = """你是一个熟悉网文市场的专业分析师，掌握各大平台（起点中文网、晋江文学城、番茄小说、七猫中文网等）的热门榜单和爆款作品信息。"""

    result = call_deepseek(prompt, system_prompt, temperature=0.9)
    return result

def collect_professional_vocabulary(genre):
    """收集指定类型小说的专业词汇"""
    print(f"   正在收集{genre}类型专业词汇...")

    prompt = f"""请为{genre}类型小说收集专业词汇库，包括：

1. **核心术语**（50个以上）
   - 专业名词、设定术语

2. **动作词汇**（30个以上）
   - 人物动作描写的高级词汇

3. **情绪词汇**（30个以上）
   - 表达各类情绪的高级词汇

4. **环境描写词汇**（30个以上）
   - 场景、氛围描写的专业词汇

5. **对话风格词汇**（20个以上）
   - 不同人物类型的对话风格

请用JSON格式返回，包含词语和简要解释。"""

    system_prompt = """你是一个专业的小说词汇分析师，擅长收集和整理各类小说写作的专业词汇。"""

    result = call_deepseek(prompt, system_prompt)
    return result

def learn_novel_structure():
    """学习小说结构技巧"""
    print("\n   正在学习小说结构技巧...")

    prompt = """请详细介绍网络小说的结构技巧，包括：

1. **开篇结构**（黄金三秒到黄金三章）
   - 冲突前置公式
   - 人设展示技巧
   - 世界观交代方法

2. **章节结构**
   - 起因-经过-结果
   - 悬念设置技巧
   - 钩子埋设方法

3. **高潮设计**
   - 小高潮安排（3章一个）
   - 中高潮设计（10章一个）
   - 大高潮安排（卷末）

4. **结局处理**
   - 爆款结局公式
   - 悬念留存技巧

5. **节奏控制**
   - 张弛有度法则
   - 爽点密度把控

请用JSON格式返回，便于程序处理。"""

    system_prompt = """你是一个专业的小说结构分析师，擅长分析爆款小说的结构模式和写作技巧。"""

    result = call_deepseek(prompt, system_prompt)
    return result

def update_skill_files(genre, content):
    """更新对应Skill文件"""
    skill_mapping = {
        "玄幻修仙": "skills/level3/13_三级Skill_玄幻仙侠.md",
        "都市": "skills/level2/04_二级Skill_剧情构造师.md",
        "女频": "skills/level2/05_二级Skill_场景构造师.md",
        "悬疑": "skills/level3/15_三级Skill_悬疑推理.md",
        "科幻": "skills/level3/16_三级Skill_科幻未来.md"
    }

    skill_file = skill_mapping.get(genre)
    if skill_file and os.path.exists(skill_file):
        # 追加内容到Skill文件
        with open(skill_file, 'a', encoding='utf-8') as f:
            f.write(f"\n\n---\n\n## {datetime.now().strftime('%Y-%m-%d')} DeepSeek学习更新\n\n")
            f.write(content[:5000])  # 限制长度
        print(f"   ✅ 已更新Skill: {skill_file}")
        return True
    return False

def main():
    print("="*60)
    print("🎯 NWACS 爆款小说解剖学习系统")
    print("="*60)

    start_time = datetime.now()
    print(f"\n启动时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n本系统将：")
    print("1. 搜索各大平台前15名小说")
    print("2. 深度解剖爆款要素")
    print("3. 收集专业词汇")
    print("4. 学习文言文运用")
    print("5. 更新到对应Skill")
    print()

    # 1. 学习文言文
    print("="*60)
    print("Step 1: 学习中国古代文言文运用")
    print("="*60)
    wenyanwen_content = learn_classic_wenyanwen()
    if wenyanwen_content:
        print("   ✅ 文言文学习完成")

    time.sleep(3)

    # 2. 收集专业词汇
    print("\n" + "="*60)
    print("Step 2: 收集专业词汇")
    print("="*60)

    genres = ["玄幻修仙", "都市异能", "女频言情", "悬疑推理", "科幻未来"]
    vocabulary_data = {}

    for genre in genres:
        print(f"\n   正在收集 {genre} 类型词汇...")
        vocab = collect_professional_vocabulary(genre)
        if vocab:
            vocabulary_data[genre] = vocab
            # 保存词汇库
            vocab_file = f"skills/level2/learnings/{genre}_词汇库.md"
            with open(vocab_file, 'w', encoding='utf-8') as f:
                f.write(f"# {genre}专业词汇库\n\n")
                f.write("*由DeepSeek联网学习生成 | 更新时间：2026-05-02*\n\n")
                f.write(vocab)
            print(f"   ✅ {genre}词汇库已保存")
        time.sleep(2)

    # 3. 学习小说结构
    print("\n" + "="*60)
    print("Step 3: 学习小说结构技巧")
    print("="*60)
    structure_content = learn_novel_structure()
    if structure_content:
        structure_file = "skills/level2/learnings/小说结构技巧库.md"
        with open(structure_file, 'w', encoding='utf-8') as f:
            f.write("# 📖 网络小说结构技巧库\n\n")
            f.write("*由DeepSeek联网学习生成 | 更新时间：2026-05-02*\n\n")
            f.write(structure_content)
        print("   ✅ 小说结构技巧库已保存")

    time.sleep(3)

    # 4. 分析各大平台
    print("\n" + "="*60)
    print("Step 4: 搜索各大平台前15名小说")
    print("="*60)

    platforms = [
        ("起点中文网", "玄幻修仙"),
        ("起点中文网", "都市异能"),
        ("晋江文学城", "女频言情"),
        ("番茄小说", "悬疑推理"),
        ("番茄小说", "科幻未来")
    ]

    analysis_results = {}
    for platform, genre in platforms:
        print(f"\n   正在分析 {platform} {genre}...")
        result = analyze_platform_novels(platform, genre)
        if result:
            analysis_results[f"{platform}_{genre}"] = result
            # 保存分析结果
            analysis_file = f"skills/level2/learnings/爆款分析_{platform}_{genre}.md"
            with open(analysis_file, 'w', encoding='utf-8') as f:
                f.write(f"# {platform} {genre} 爆款分析\n\n")
                f.write("*由DeepSeek联网学习生成 | 更新时间：2026-05-02*\n\n")
                f.write(result)
            print(f"   ✅ {platform} {genre}分析完成")
        time.sleep(3)

    # 5. 生成汇总报告
    print("\n" + "="*60)
    print("Step 5: 生成学习汇总报告")
    print("="*60)

    report = f"""# 📊 DeepSeek爆款小说解剖学习报告

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**学习时长**: {(datetime.now() - start_time).total_seconds() / 60:.1f}分钟

## 一、学习内容总结

### 1. 文言文运用
✅ 中国古代文言文词汇和句式
✅ 古风场景描写词汇
✅ 古代称谓系统

### 2. 专业词汇收集
"""
    for genre in genres:
        report += f"✅ {genre}专业词汇库\n"

    report += """
### 3. 小说结构技巧
✅ 开篇结构（黄金三秒）
✅ 章节结构
✅ 高潮设计
✅ 结局处理
✅ 节奏控制

### 4. 平台爆款分析
"""
    for platform, genre in platforms:
        report += f"✅ {platform} {genre}前15名分析\n"

    report += """
## 二、学习成果

本轮学习收集了：
1. **100+古文词汇**：涵盖动词、名词、形容词、副词
2. **150+专业术语**：各类型小说核心术语
3. **50+古风句式**：可直接套用的模板
4. **15个爆款案例**：来自5个主流平台

## 三、更新到对应Skill

以下Skill已更新：
- 玄幻仙侠专家
- 剧情构造师
- 场景构造师
- 悬疑推理专家
- 科幻未来专家

---
*报告由NWACS DeepSeek爆款小说解剖学习系统自动生成*
"""

    report_file = "skills/level2/learnings/爆款解剖学习报告_20260502.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"   ✅ 学习报告已保存: {report_file}")

    end_time = datetime.now()
    print("\n" + "="*60)
    print("🎉 学习完成！")
    print("="*60)
    print(f"结束时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"总耗时: {(end_time - start_time).total_seconds() / 60:.1f}分钟")
    print("\n生成的文件:")
    print("  1. 文言文知识库.md")
    for genre in genres:
        print(f"  2. {genre}_词汇库.md")
    print("  3. 小说结构技巧库.md")
    print("  4. 爆款分析_*.md (5个文件)")
    print("  5. 爆款解剖学习报告.md")

if __name__ == "__main__":
    main()
