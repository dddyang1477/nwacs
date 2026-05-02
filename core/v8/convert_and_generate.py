#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小说格式转换与章节生成脚本
将大纲和章节转换为txt格式，并生成第6-10章
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

def markdown_to_txt(md_content):
    """将markdown内容转换为纯文本"""
    lines = md_content.split('\n')
    txt_lines = []
    for line in lines:
        # 移除markdown标题符号
        if line.startswith('#'):
            line = line.replace('#', '').strip()
            # 添加分隔线
            txt_lines.append('=' * 60)
            txt_lines.append(line)
            txt_lines.append('=' * 60)
        elif line.startswith('---'):
            continue
        else:
            txt_lines.append(line)
    return '\n'.join(txt_lines)

def convert_outline_to_txt():
    """将大纲转换为txt格式"""
    print("\n" + "="*60)
    print("📖 转换小说大纲为txt格式")
    print("="*60)
    
    if os.path.exists("novel/04_outline.md"):
        with open("novel/04_outline.md", 'r', encoding='utf-8') as f:
            content = f.read()
        
        txt_content = markdown_to_txt(content)
        output_file = "novel/《天机道主》小说大纲.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(txt_content)
        print(f"   ✅ 大纲已转换: {output_file}")
    else:
        print("   ❌ 大纲文件不存在")

def convert_chapters_1_5_to_txt():
    """将1-5章转换为txt格式"""
    print("\n" + "="*60)
    print("📖 转换第1-5章为txt格式")
    print("="*60)
    
    if os.path.exists("novel/chapters_01_05.md"):
        with open("novel/chapters_01_05.md", 'r', encoding='utf-8') as f:
            content = f.read()
        
        txt_content = markdown_to_txt(content)
        output_file = "novel/《天机道主》第1-5章.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(txt_content)
        print(f"   ✅ 第1-5章已转换: {output_file}")
    else:
        print("   ❌ 章节文件不存在")

def generate_chapter_6():
    """生成第6章"""
    print("\n" + "="*60)
    print("📝 生成第6章：长老召见")
    print("="*60)

    prompt = """请为长篇玄幻小说《天机道主》撰写第6章。

## 小说核心设定
- 主角：叶青云，前世天算师，拥有因果推演能力
- 身份：刚刚升为外门弟子，因识破林逸勾结魔教有功
- 背景：青云宗，大长老要亲自召见主角

## 第6章要求
**核心目标**：主角与大长老的初次交锋，揭开更多秘密

**必须包含**：
1. 大长老的试探：用各种手段考验主角
2. 主角的应对：用智慧化解，不显山露水
3. 揭示秘密：大长老知道主角的一些底细
4. 资源倾斜：主角获得修炼资源和进入藏经阁的资格
5. 新的任务：大长老交给主角一个秘密任务

**字数**：2000-3000字
**风格**：智斗为主，对话要精彩
**结尾钩子**：引出更大的阴谋

请开始撰写第6章。"""

    system_prompt = """你是一位顶尖的玄幻小说作家，擅长写智斗和对话。
写作要点：
1. 对话要符合人物身份
2. 智慧的较量要精彩
3. 埋笔要自然
4. 节奏要适中"""

    result = call_deepseek(prompt, system_prompt, temperature=0.85)
    return result

def generate_chapter_7():
    """生成第7章"""
    print("\n" + "="*60)
    print("📝 生成第7章：藏经秘辛")
    print("="*60)

    prompt = """请为长篇玄幻小说《天机道主》撰写第7章。

## 小说核心设定
- 主角：叶青云，获得进入藏经阁的资格
- 核心目标：寻找《因果真经》残卷
- 背景：藏经阁有三层，第三层是禁地

## 第7章要求
**核心目标**：主角在藏经阁的探索，发现重要线索

**必须包含**：
1. 进入藏经阁，遇到守护长老
2. 第一层和第二层的探索（铺垫）
3. 发现第三层的秘密入口
4. 进入第三层，发现上古遗迹和《因果真经》残卷
5. 守护长老的真实身份（可能是友非敌）
6. 获得重要线索：关于主角父亲的失踪

**字数**：2000-3000字
**风格**：悬疑、探险、智斗
**结尾钩子**：主角发现父亲失踪的真相与宗门有关

请开始撰写第7章。"""

    system_prompt = """你是一位顶尖的玄幻小说作家，擅长写悬疑和探险。
写作要点：
1. 氛围营造要到位
2. 发现过程要有逻辑
3. 秘密要慢慢揭开
4. 节奏要有张有弛"""

    result = call_deepseek(prompt, system_prompt, temperature=0.85)
    return result

def generate_chapter_8():
    """生成第8章"""
    print("\n" + "="*60)
    print("📝 生成第8章：因果修炼")
    print("="*60)

    prompt = """请为长篇玄幻小说《天机道主》撰写第8章。

## 小说核心设定
- 主角：叶青云，获得《因果真经》残卷
- 修炼体系：因果修炼，需要特殊资源
- 背景：主角开始正式修炼

## 第8章要求
**核心目标**：主角开始修炼因果真经，实力提升

**必须包含**：
1. 修炼因果真经的困难和代价
2. 主角利用天机推演优化修炼方法
3. 第一次修炼成果：修为突破到炼气四层
4. 苏沐雪的进步：冰凤血脉开始觉醒
5. 主角发现因果修炼的真正秘密（与天道有关）
6. 新的威胁：执法长老林啸天开始怀疑主角

**字数**：2000-3000字
**风格**：修炼描写、情感互动、悬疑铺垫
**结尾钩子**：林啸天开始调查主角

请开始撰写第8章。"""

    system_prompt = """你是一位顶尖的玄幻小说作家，擅长写修炼和情感。
写作要点：
1. 修炼过程要详细但不枯燥
2. 情感互动要自然
3. 铺垫要到位
4. 节奏要适中"""

    result = call_deepseek(prompt, system_prompt, temperature=0.85)
    return result

def generate_chapter_9():
    """生成第9章"""
    print("\n" + "="*60)
    print("📝 生成第9章：暗流涌动")
    print("="*60)

    prompt = """请为长篇玄幻小说《天机道主》撰写第9章。

## 小说核心设定
- 主角：叶青云，炼气四层，开始崭露头角
- 敌人：林啸天（执法长老），开始调查主角
- 背景：宗门内暗流涌动，各方势力开始关注主角

## 第9章要求
**核心目标**：主角与林啸天的暗中交锋

**必须包含**：
1. 林啸天的调查：派人跟踪主角
2. 主角的反侦察：利用因果线发现跟踪者
3. 主角设局：让跟踪者"意外"暴露
4. 林啸天的愤怒：意识到主角不简单
5. 大长老的态度：似乎在保护主角
6. 新的人物登场：神秘女子（可能是女主之一）

**字数**：2000-3000字
**风格**：智斗、悬疑、布局
**结尾钩子**：神秘女子主动接近主角

请开始撰写第9章。"""

    system_prompt = """你是一位顶尖的玄幻小说作家，擅长写智斗和悬疑。
写作要点：
1. 智斗要精彩
2. 人物互动要到位
3. 新角色要有特点
4. 节奏要紧张"""

    result = call_deepseek(prompt, system_prompt, temperature=0.85)
    return result

def generate_chapter_10():
    """生成第10章"""
    print("\n" + "="*60)
    print("📝 生成第10章：秘境开启")
    print("="*60)

    prompt = """请为长篇玄幻小说《天机道主》撰写第10章。

## 小说核心设定
- 主角：叶青云，炼气四层，准备参加秘境试炼
- 背景：青云宗一年一度的秘境试炼开始
- 目标：主角进入秘境，寻找机缘

## 第10章要求
**核心目标**：秘境试炼开启，主角踏上新的征程

**必须包含**：
1. 秘境试炼的介绍：规则、奖励、危险
2. 各方势力的动向：林啸天安排人对付主角
3. 主角的准备：利用因果推演预测危险
4. 秘境开启：各种意外发生
5. 进入秘境：主角与苏沐雪、神秘女子一同进入
6. 第一个挑战：秘境入口的考验

**字数**：2000-3000字
**风格**：宏大场面、悬疑、冒险
**结尾钩子**：秘境中发现与主角父亲有关的线索

请开始撰写第10章。"""

    system_prompt = """你是一位顶尖的玄幻小说作家，擅长写宏大场面和冒险。
写作要点：
1. 场面要宏大
2. 人物互动要自然
3. 悬念要到位
4. 节奏要快"""

    result = call_deepseek(prompt, system_prompt, temperature=0.85)
    return result

def main():
    print("="*60)
    print("📖 小说格式转换与章节生成")
    print("="*60)

    # 转换大纲和1-5章为txt格式
    convert_outline_to_txt()
    convert_chapters_1_5_to_txt()

    # 生成第6-10章
    chapters = []
    chapter_names = [
        ("第6章：长老召见", generate_chapter_6),
        ("第7章：藏经秘辛", generate_chapter_7),
        ("第8章：因果修炼", generate_chapter_8),
        ("第9章：暗流涌动", generate_chapter_9),
        ("第10章：秘境开启", generate_chapter_10),
    ]

    for i, (name, func) in enumerate(chapter_names, 6):
        result = func()
        if result:
            chapters.append(result)
            print(f"   ✅ 第{i}章完成")
        else:
            print(f"   ❌ 第{i}章失败")

    # 保存第6-10章为txt格式
    if chapters:
        full_content = []
        full_content.append("《天机道主》第6-10章\n")
        full_content.append("=" * 60 + "\n")
        full_content.append(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        full_content.append("=" * 60 + "\n\n")
        
        for chapter in chapters:
            txt_content = markdown_to_txt(chapter)
            full_content.append(txt_content)
            full_content.append("\n\n")
        
        output_file = "novel/《天机道主》第6-10章.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.writelines(full_content)
        print(f"\n   ✅ 第6-10章已保存为txt格式")

    print("\n" + "="*60)
    print("🎉 任务完成！")
    print("="*60)
    print("\n生成的txt文件：")
    print("  1. novel/《天机道主》小说大纲.txt")
    print("  2. novel/《天机道主》第1-5章.txt")
    print("  3. novel/《天机道主》第6-10章.txt")

if __name__ == "__main__":
    main()