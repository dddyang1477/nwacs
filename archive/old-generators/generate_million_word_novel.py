#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 百万字长篇小说生成系统
分卷、分章节、智能生成、完整100万字+
"""

import os
import sys
import json
import time
import threading
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

VERSION = "1.0"
NOVEL_TITLE = "长生仙逆"
TOTAL_CHAPTERS = 200  # 200章，每章5000字，总计100万字

def load_config():
    config = {}
    if os.path.exists('config.json'):
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
    return config

def call_deepseek(prompt, system_prompt=None, max_tokens=10000):
    config = load_config()
    if not config.get('api_key'):
        print("❌ 错误：API Key未配置！")
        return None

    url = config.get('base_url', 'https://api.deepseek.com/v1') + '/chat/completions'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {config.get("api_key")}'
    }

    data = {
        'model': config.get('model', 'deepseek-v4-pro'),
        'messages': [
            {'role': 'system', 'content': system_prompt or "你是一位优秀的玄幻小说作家，擅长长篇小说创作"},
            {'role': 'user', 'content': prompt}
        ],
        'temperature': 0.85,
        'max_tokens': max_tokens
    }

    print(f"\r⏳ 正在生成...", end='', flush=True)

    try:
        import urllib.request
        req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)
        
        with urllib.request.urlopen(req, timeout=180) as response:
            result = json.loads(response.read().decode('utf-8'))
            print(f"\r✅ 生成完成   ", end='', flush=True)
            return result['choices'][0]['message']['content']
    except Exception as e:
        print(f"\r❌ 生成失败: {e}", end='', flush=True)
        return None

def generate_chapter(chapter_num, chapter_title, summary, novel_context):
    """生成单章内容"""
    prompt = f"""请创作《长生仙逆》第{chapter_num}章：{chapter_title}

摘要：{summary}

要求：
1. 这是第{chapter_num}章，位于200章的长篇小说中
2. 请写至少4000字
3. 保持与前面章节的连贯性
4. 风格：苟道流、智斗为主、黑暗风、《剑来》风格
5. 主角：顾长青，性格谨慎隐忍，擅长毒术
6. 女主：苏瑶、姜雪晴、白骨夫人
7. 反派：王天辰及修仙界各方势力
8. 世界观：修仙界弱肉强食，充满阴谋
9. 语言：自然流畅，无AI痕迹，有画面感

前面章节回顾：
{novel_context[:5000]}

请开始创作！"""
    
    content = call_deepseek(prompt, max_tokens=12000)
    return content

def save_chapter(chapter_num, title, content):
    """保存单章"""
    os.makedirs('output/长生仙逆/', exist_ok=True)
    filename = f'output/长生仙逆/第{chapter_num:03d}章_{title}.txt'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"第{chapter_num}章：{title}\n\n")
        f.write(content)
    return filename

def save_full_novel(all_chapters, title, description):
    """保存完整小说"""
    os.makedirs('output/', exist_ok=True)
    filename = f'output/{title}_完整版.txt'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write(f"《{title}》\n")
        f.write("="*80 + "\n\n")
        f.write(description + "\n\n")
        f.write("="*80 + "\n\n")
        f.write(f"创作时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"总章节数：{len(all_chapters)}\n")
        f.write(f"预估字数：{len(all_chapters)*5000:+,}字\n\n")
        
        for chapter in all_chapters:
            f.write("\n" + "="*80 + "\n")
            f.write(f"第{chapter['num']}章：{chapter['title']}\n")
            f.write("="*80 + "\n\n")
            f.write(chapter['content'] + "\n")
    
    return filename

def generate_outline():
    """生成完整小说大纲"""
    prompt = """请为《长生仙逆》创作完整大纲，要求：

1. 分10卷，每卷20章，总计200章
2. 每卷有明确的主题和冲突
3. 主角：顾长青，性格谨慎，苟道流，擅长毒术
4. 世界观：修仙界黑暗现实，弱肉强食
5. 请详细规划10卷，每卷20章的情节大纲
6. 要求达到：
   - 长篇小说，200章，总字数100万字+
   - 每卷有明确的卷名、主题
   - 每章有标题、摘要、核心冲突
   - 注重智斗和苟道风格
   - 女主：苏瑶、姜雪晴、白骨夫人
   - 反派：王天辰及修仙界各方势力
"""

    content = call_deepseek(prompt, max_tokens=20000)
    return content

def main():
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║         NWACS 百万字长篇小说生成系统 v{VERSION}                   ║
║                                                              ║
║         书名：{NOVEL_TITLE}                                     ║
║         目标：{TOTAL_CHAPTERS}章，100万字+                          ║
║                                                              ║
║         进度：每章5000字，完整创作                                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)

    # 检查配置
    config = load_config()
    if not config.get('api_key'):
        print("\n❌ 请先配置API Key！")
        return

    # 询问开始
    response = input("\n🚀 开始生成百万字小说？(yes/no): ").lower()
    if response not in ['yes', 'y']:
        print("已取消。")
        return

    # 生成大纲
    print("\n📖 1. 生成完整小说大纲...")
    outline = generate_outline()
    if outline:
        os.makedirs('output/', exist_ok=True)
        with open('output/长生仙逆_完整大纲.txt', 'w', encoding='utf-8') as f:
            f.write(outline)
        print(f"✅ 大纲已保存到 output/长生仙逆_完整大纲.txt")
    else:
        print("❌ 大纲生成失败")
        return

    # 确认开始生成章节
    input("\n按 Enter 开始生成章节...")

    # 分卷生成
    chapters_per_volume = 20
    all_chapters = []
    chapter_summaries = [
        # 第一卷：凡人之路
        "末法时代", "望气之术", "父亲的遗产", "毒经救人", "十年之约",
        "初入苍云", "棋逢对手", "秘境开启", "劫运教阴谋", "暗夜逃亡",
        "苏瑶解毒，初见端倪", "长老试探，危机四伏", "暗中调查，真相浮现",
        "天机阁密约", "太清宫邀请", "劫运教伏击", "窃运术小成",
        "宗门大比，预选赛", "王天成的阴谋", "秘境深处",

        # 第二卷：修仙入门
        "父亲真相", "幽冥毒龙传承", "姜雪晴的过去", "三方势力",
        "外门大比", "内门考核", "王天成出手", "绝境逢生", "真相大白",
        "十年之约", "第一个师父", "修炼路上", "洞府生活", "外门历练",
        "第一次杀人", "血色试炼", "秘境寻宝", "丹炉崩溃", "宗门追杀",

        # 第三卷：纵横外门
        "逃出生天", "再次相见", "小露一手", "反杀", "第一次交锋",
        "声名鹊起", "丹会", "技惊四座", "炼丹天才", "王动的心思",
        "招揽", "打脸", "我拒绝", "冲突", "执法队",
        "谁给你的勇气", "墨岩真人", "外门大比开始", "第一战", "震惊"
    ]

    for chapter_num in range(1, TOTAL_CHAPTERS + 1):
        print(f"\n{'='*60}")
        print(f"📖 正在生成第{chapter_num}章（共{TOTAL_CHAPTERS}章）")
        print(f"{'='*60}")

        # 获取章节主题
        idx = min(chapter_num - 1, len(chapter_summaries) - 1)
        title = f"第{chapter_num}章"
        summary = chapter_summaries[idx] if chapter_num <= len(chapter_summaries) else "情节继续发展"

        # 构建上下文
        context = f"前面已生成{len(all_chapters)}章"
        if all_chapters:
            context += "\n最近5章内容概要："
            for i, chapter in enumerate(all_chapters[-5:]):
                context += f"\n{i+1}. {chapter['title']}"

        # 生成章节
        content = generate_chapter(chapter_num, title, summary, context)
        
        if content:
            filename = save_chapter(chapter_num, title, content)
            all_chapters.append({'num': chapter_num, 'title': title, 'content': content})
            print(f"\n✅ 第{chapter_num}章已保存到 {filename}")
            
            # 每10章保存一次完整版
            if chapter_num % 10 == 0:
                print(f"\n💾 保存中间完整版...")
                save_full_novel(all_chapters, "长生仙逆", "正在创作中")
            
            # 短暂延迟
            time.sleep(2)
        else:
            print(f"\n❌ 第{chapter_num}章生成失败，继续尝试...")
            continue

    # 最后保存完整小说
    print(f"\n{'='*60}")
    print("🎉 百万字小说创作完成！")
    print(f"{'='*60}")

    final_path = save_full_novel(all_chapters, NOVEL_TITLE, "长篇玄幻修仙小说，苟道流，智斗为主")

    print(f"\n📖 完整小说已保存：{final_path}")
    print(f"📊 完成章节：{len(all_chapters)}")
    print(f"📚 预估字数：{len(all_chapters)*5000:+,} 字")

if __name__ == "__main__":
    main()
