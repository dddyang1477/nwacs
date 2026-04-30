#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
百万字长篇小说规划与生成系统
从第1章到第200章完整规划
"""

import os
import sys
import json
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

VERSION = "1.0"

VOLUMES = [
    {
        "name": "第一卷：凡人之路",
        "chapters": 20,
        "theme": "顾长青从凡人觉醒，踏上修仙路，揭露父亲死亡真相",
        "start": 1,
        "end": 20
    },
    {
        "name": "第二卷：初入仙门",
        "chapters": 20,
        "theme": "在苍云宗外门站稳脚跟，与王天辰第一次交锋",
        "start": 21,
        "end": 40
    },
    {
        "name": "第三卷：外门风云",
        "chapters": 20,
        "theme": "在外门大比中崭露头角，进入内门，危机四伏",
        "start": 41,
        "end": 60
    },
    {
        "name": "第四卷：内门潜修",
        "chapters": 20,
        "theme": "在内门低调修炼，积蓄实力，寻找机会",
        "start": 61,
        "end": 80
    },
    {
        "name": "第五卷：秘境探索",
        "chapters": 20,
        "theme": "宗门秘境探索，发现更多关于父亲死亡的线索",
        "start": 81,
        "end": 100
    },
    {
        "name": "第六卷：宗门阴谋",
        "chapters": 20,
        "theme": "揭露王天辰背后的宗门阴谋，第一次正面冲突",
        "start": 101,
        "end": 120
    },
    {
        "name": "第七卷：逃亡之路",
        "chapters": 20,
        "theme": "被宗门追杀，逃亡中成长，接触更广阔的修仙界",
        "start": 121,
        "end": 140
    },
    {
        "name": "第八卷：纵横修仙",
        "chapters": 20,
        "theme": "在修仙界扬名立万，实力增强，组建势力",
        "start": 141,
        "end": 160
    },
    {
        "name": "第九卷：重回宗门",
        "chapters": 20,
        "theme": "实力足够后回到苍云宗，开始复仇",
        "start": 161,
        "end": 180
    },
    {
        "name": "第十卷：长生仙逆",
        "chapters": 20,
        "theme": "最终决战，真相大白，踏上长生路",
        "start": 181,
        "end": 200
    }
]

CHAPTER_SUMMARY_TEMPLATE = [
    # 第一卷（已有第1-30章，继续到第40章进入第二卷）
    "末法时代", "望气之术", "父亲的遗产", "毒经救人", "十年之约",
    "初入苍云", "棋逢对手", "秘境开启", "劫运教阴谋", "暗夜逃亡",
    "苏瑶解毒", "长老试探", "暗中调查", "天机阁密约", "太清宫邀请",
    "劫运教伏击", "窃运术小成", "宗门大比", "王天成的阴谋", "秘境深处",
    "父亲真相", "幽冥毒龙传承", "姜雪晴的过去", "三方势力", "外门大比",
    "内门考核", "王天成出手", "绝境逢生", "真相大白", "十年之约",
    # 第二卷（第31-50章）
    "第一个师父", "修炼路上", "洞府生活", "外门历练", "第一次杀人",
    "血色试炼", "秘境寻宝", "丹炉崩溃", "宗门追杀", "逃出生天",
    "再次相见", "小露一手", "反杀", "第一次交锋", "声名鹊起",
    "丹会", "技惊四座", "炼丹天才", "王动的心思", "招揽",
    # 第三卷（第51-70章）
    "打脸", "我拒绝", "冲突", "执法队", "谁给你的勇气",
    "墨岩真人", "外门大比开始", "第一战", "震惊", "黑马",
    "势如破竹", "八强", "激战", "林琅天", "最终之战",
    "第一", "奖励", "内门选拔", "临行前", "父女相见",
    # 继续扩展更多章节...
]

def generate_volume_plan(volume_idx):
    volume = VOLUMES[volume_idx]
    plan = f"\n{'='*80}\n"
    plan += f"{volume['name']}\n"
    plan += f"{'='*80}\n"
    plan += f"\n主题：{volume['theme']}\n"
    plan += f"\n章节规划（第{volume['start']}章-第{volume['end']}章）：\n\n"
    
    for chapter_num in range(volume['start'], volume['end'] + 1):
        idx = chapter_num - 1
        if idx < len(CHAPTER_SUMMARY_TEMPLATE):
            summary = CHAPTER_SUMMARY_TEMPLATE[idx]
        else:
            summary = "情节继续发展，故事持续展开"
        plan += f"  第{chapter_num:03d}章：{summary}\n"
    
    return plan

def save_full_plan():
    os.makedirs('output/', exist_ok=True)
    filename = 'output/百万字小说_完整规划.txt'
    
    full_plan = f"""
{'='*80}
        《长生仙逆》百万字长篇小说完整规划
{'='*80}

创作时间：{datetime.now().strftime('%Y-%m-%d')}
总卷数：10卷
总章节：200章
预估总字数：1,000,000 字

{'='*80}
                   分卷规划
{'='*80}
"""

    for i, volume in enumerate(VOLUMES):
        full_plan += generate_volume_plan(i)
        full_plan += "\n\n"

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(full_plan)
    
    return filename

def main():
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     NWACS 百万字长篇小说规划系统 v{VERSION}                        ║
║                                                              ║
║     书名：《长生仙逆》                                          ║
║     目标：10卷 × 20章 = 200章，总计约100万字                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)

    print("\n📊 规划概览:")
    for volume in VOLUMES:
        print(f"   {volume['name']}：{volume['chapters']}章")
    
    print(f"\n总目标：{len(VOLUMES)}卷 × 20章 = 200章")
    print(f"预估字数：200章 × 5000字 = 1,000,000 字")

    # 生成规划文件
    print(f"\n💾 正在生成完整规划...")
    filename = save_full_plan()
    print(f"✅ 完整规划已保存到：{filename}")

    print(f"\n{'='*80}")
    print(f"下一步建议:")
    print(f"  1. 查看规划文档：{filename}")
    print(f"  2. 使用百万字生成系统，按需生成后续章节")
    print(f"  3. 或选择特定章节范围进行生成")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    main()
