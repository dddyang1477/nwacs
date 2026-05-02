#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
《天机道主》第1-5章生成脚本
基于已设计的novel outline生成开篇章节
"""

import sys
import os
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "sk-f3246fbd1eef446e9a11d78efefd9bba"
BASE_URL = "https://api.deepseek.com"

def call_deepseek(prompt, system_prompt=None, temperature=0.85):
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
        response = requests.post(url, headers=headers, json=data, timeout=180)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"   ❌ API调用失败: {e}")
        return None

def generate_chapter_1():
    """生成第1章"""
    print("\n" + "="*60)
    print("📝 生成第1章：废物与棋子")
    print("="*60)

    prompt = """请为长篇玄幻小说《天机道主》撰写第1章。

## 小说核心设定
- 主角：叶青云，前世是天道文明最后一位"天算师"，掌握因果推演能力
- 穿越身份：青云宗外门杂役，修为炼气一层，废物中的废物
- 背景：这是一个修炼至上的世界，修炼境界分为：启灵境→聚气境→凝丹境→化婴境→出窍境→分神境→合体境→渡劫境→大乘境
- 核心能力：主角拥有"天机棋子"，可以推演因果、操控因果线
- 风格：苟道流、智斗流、热血、悬疑、治愈、搞笑

## 第1章要求
**核心目标**：开篇即高能，打破读者预期，建立主角人设

**必须包含**：
1. 开场即冲突：主角被当众羞辱（被长老之子林逸踩脸）
2. 主角性格展示：表面废物，实则心智如妖，有前世记忆
3. 金手指暗示：天机棋子濒死激活
4. 第一个爽点：主角用智谋反杀，第一个小胜利
5. 埋笔：暗示林逸背后有人操控，主角的处境危险

**字数**：2000-3000字
**风格**：节奏快、信息密度高、每句话都有用
**结尾钩子**：留下悬念，让读者想看下一章

## 世界观背景（简要）
- 青云宗：下等宗门，在天枢域边缘
- 三大古派：天墟阁、冰魄宫、星宿门（九域统治者）
- 天机之子：每隔三千年出现一批，被天道选中，互相厮杀，最终胜者成为天道宿主

请开始撰写第1章。"""

    system_prompt = """你是一位顶尖的玄幻小说作家，擅长写让人欲罢不能的开篇。
你的写作特点：
1. 开篇第一句话就抓住读者
2. 节奏飞快，不水字数
3. 每章结尾留钩子
4. 人物对话符合性格
5. 爽点自然流露，不生硬"""

    result = call_deepseek(prompt, system_prompt, temperature=0.85)
    return result

def generate_chapter_2():
    """生成第2章"""
    print("\n" + "="*60)
    print("📝 生成第2章：因果初显")
    print("="*60)

    prompt = """请为长篇玄幻小说《天机道主》撰写第2章。

## 小说核心设定
- 主角：叶青云，前世天算师，穿越到青云宗外门杂役身上
- 核心能力：天机棋子，因果推演，操控因果线
- 风格：苟道流、智斗流

## 第2章要求
**核心目标**：展示主角的智斗能力，埋下重要伏笔

**必须包含**：
1. 主角利用天机棋子的能力，第一次推演成功
2. 发现《因果真经》残卷的线索
3. 与女主苏沐雪的初遇（她是唯一没有嘲笑主角的人）
4. 展示主角的苟道策略：表面废物，暗中布局
5. 林逸的威胁：林逸是长老之子，不会善罢甘休

**字数**：2000-3000字
**风格**：信息量大、智斗精彩、感情线铺垫
**结尾钩子**：暗示更大的阴谋

## 苏沐雪人设（本章出场）
- 身份：青云宗外门弟子，第一美女
- 外貌：冰肌玉骨，素裙飘飘，眼神清冷但善良
- 特点：拥有"冰凤血脉"（被误认为废血脉）
- 与主角关系：每天给主角送饭，是主角唯一的温暖

请开始撰写第2章。"""

    system_prompt = """你是一位顶尖的玄幻小说作家，擅长写智斗和情感铺垫。
写作要点：
1. 展示主角的智慧，不是武力
2. 感情戏要细腻但不过分
3. 埋笔要自然，不刻意
4. 节奏适中，张弛有度"""

    result = call_deepseek(prompt, system_prompt, temperature=0.85)
    return result

def generate_chapter_3():
    """生成第3章"""
    print("\n" + "="*60)
    print("📝 生成第3章：天机推演")
    print("="*60)

    prompt = """请为长篇玄幻小说《天机道主》撰写第3章。

## 小说核心设定
- 主角：叶青云，前世天算师，拥有因果推演能力
- 核心设定：等价交换——修炼有代价，力量不是免费
- 风格：苟道流、悬疑

## 第3章要求
**核心目标**：深入展示天机棋子的能力，揭示世界观一角

**必须包含**：
1. 主角第一次完整使用天机推演能力
2. 推演结果：发现林逸背后有人指使，是宗门内部斗争
3. 主角开始布局：用因果线在暗处布局
4. 发现宗门藏经阁的秘密（第七层有上古遗迹）
5. 搞笑元素：主角自言自语吐槽自己的处境

**字数**：2000-3000字
**风格**：智斗为主，搞笑为辅
**结尾钩子**：发现林逸背后的人身份不简单

请开始撰写第3章。"""

    system_prompt = """你是一位顶尖的玄幻小说作家，擅长写智斗和悬疑。
写作要点：
1. 推演过程要精彩，不是简单的"知道了"
2. 布局要有逻辑，让读者佩服主角的智慧
3. 搞笑要自然，不是硬塞
4. 每句话都有信息量"""

    result = call_deepseek(prompt, system_prompt, temperature=0.85)
    return result

def generate_chapter_4():
    """生成第4章"""
    print("\n" + "="*60)
    print("📝 生成第4章：暗箭难防")
    print("="*60)

    prompt = """请为长篇玄幻小说《天机道主》撰写第4章。

## 小说核心设定
- 主角：叶青云，苟道流主角，表面废物实则智慧超群
- 敌人：林逸（长老之子，炼气七层，嚣张跋扈）
- 世界观：青云宗是个下等宗门，但内部斗争激烈

## 第4章要求
**核心目标**：林逸的第二次威胁，主角被动应战

**必须包含**：
1. 林逸设下毒计：让主角在宗门任务中"意外"死亡
2. 主角用天机推演提前预知陷阱
3. 反杀开始：主角将计就计，让林逸的阴谋暴露
4. 苏沐雪的担忧：她发现了主角的异常
5. 情感线推进：苏沐雪给主角送药，主角内心触动

**字数**：2000-3000字
**风格**：危机感强，智斗精彩，情感温暖
**结尾钩子**：林逸的阴谋暴露，但更大的危机即将到来

请开始撰写第4章。"""

    system_prompt = """你是一位顶尖的玄幻小说作家，擅长写危机和反转。
写作要点：
1. 危机要有压迫感
2. 反转要让读者拍案叫绝
3. 感情戏要温暖人心
4. 节奏要快，不拖沓"""

    result = call_deepseek(prompt, system_prompt, temperature=0.85)
    return result

def generate_chapter_5():
    """生成第5章"""
    print("\n" + "="*60)
    print("📝 生成第5章：因果初成")
    print("="*60)

    prompt = """请为长篇玄幻小说《天机道主》撰写第5章。

## 小说核心设定
- 主角：叶青云，智斗流主角，擅长因果推演和布局
- 本章重点：主角的第一次小高潮——林逸当众出丑

## 第5章要求
**核心目标**：第一个爽点高潮，主角初露锋芒

**必须包含**：
1. 宗门任务开始：林逸等着看主角的笑话
2. 主角早已布下因果线，等待收割
3. 第一个反转：林逸自己踩进了陷阱
4. 打脸时刻：林逸当众暴露勾结魔教的证据
5. 震惊众人：废物杂役竟然让林逸吃瘪
6. 苏沐雪的震惊和好奇：她开始注意到主角

**字数**：2000-3000字
**风格**：爽点密集、打脸痛快、节奏燃爆
**结尾钩子**：长老会介入，主角获得宗门资源倾斜，但危险也在逼近

请开始撰写第5章。"""

    system_prompt = """你是一位顶尖的玄幻小说作家，擅长写爽点和高潮。
写作要点：
1. 爽点要密集，要让读者感到"爽"
2. 打脸要有理有据，不是无脑碾压
3. 节奏要快，一波接一波
4. 结尾要有余味，留下期待"""

    result = call_deepseek(prompt, system_prompt, temperature=0.85)
    return result

def main():
    print("="*60)
    print("📝 《天机道主》第1-5章生成")
    print("="*60)

    chapters = []
    chapter_names = [
        ("第1章：废物与棋子", generate_chapter_1),
        ("第2章：因果初显", generate_chapter_2),
        ("第3章：天机推演", generate_chapter_3),
        ("第4章：暗箭难防", generate_chapter_4),
        ("第5章：因果初成", generate_chapter_5),
    ]

    full_content = []
    full_content.append("# 📝 《天机道主》第1-5章\n\n")
    full_content.append(f"*由DeepSeek+NWACS生成 | {datetime.now().strftime('%Y-%m-%d')}*\n\n")
    full_content.append("---\n\n")

    for i, (name, func) in enumerate(chapter_names, 1):
        print(f"\n生成中 {i}/5: {name}")
        result = func()
        if result:
            chapters.append(result)
            full_content.append(result)
            full_content.append("\n---\n\n")
            print(f"   ✅ 第{i}章完成")
        else:
            print(f"   ❌ 第{i}章失败")

    if chapters:
        output_file = "novel/chapters_01_05.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.writelines(full_content)

        print("\n" + "="*60)
        print("🎉 章节生成完成！")
        print("="*60)
        print(f"\n文件已保存: {output_file}")
        print(f"共生成 {len(chapters)} 章")
        print(f"\n文件路径: novel/chapters_01_05.md")

        print("\n" + "="*60)
        print("📖 内容预览")
        print("="*60)

        for i, chapter in enumerate(chapters, 1):
            lines = chapter.strip().split('\n')
            title_line = ""
            for line in lines:
                if line.strip() and not line.strip().startswith('#'):
                    title_line = line.strip()
                    break
            if len(title_line) > 50:
                title_line = title_line[:50] + "..."
            print(f"\n第{i}章: {title_line}")

if __name__ == "__main__":
    main()