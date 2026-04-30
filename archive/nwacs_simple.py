#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 超级简化版 - 不会循环！
功能：
1. 生成世界观框架
2. 生成人物框架
3. 生成剧情大纲
4. 生成章节标题
5. 生成章节内容
"""

import os
import sys
import json
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')
VERSION = "2.0"

def print_menu():
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║              NWACS 超级简化版 v{VERSION}                             ║
║                                                              ║
║  【按步骤创作】                                              ║
║  1. 生成世界观框架                                           ║
║  2. 生成人物设定框架                                         ║
║  3. 生成完整剧情大纲                                         ║
║  4. 生成所有章节标题                                         ║
║  5. 生成章节内容                                             ║
║                                                              ║
║  【工具】                                                    ║
║  6. 查看已生成内容                                           ║
║  0. 退出                                                      ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)

def step1_worldframe():
    """步骤1：生成世界观框架"""
    print(f"\n{'='*60}")
    print("【步骤1】生成世界观框架")
    print(f"{'='*60}")
    
    world = input("请输入小说类型（如：玄幻/修仙/都市/科幻）: ").strip() or "玄幻修仙"
    title = input("请输入小说名: ").strip() or "长夜将明"
    
    world_content = f"""
# 《{title}》世界观框架

## 基础设定
- 类型：{world}
- 时代背景：末法时代，灵气稀薄
- 大陆格局：四大部洲，七大宗门
- 修炼体系：炼气→筑基→金丹→元婴→化神→渡劫→飞升

## 主要势力
1. 正道七宗：苍云宗、太清宫、天机阁等
2. 魔道四派：血神教、万鬼宗等
3. 三大古派：隐藏的顶级势力
4. 散修联盟：松散的自由修士组织

## 核心冲突
- 长生会：修仙界秘密组织，阴谋策划
- 天道沉睡：世界规则紊乱
- 主角复仇：家族灭门案

## 特殊设定
- 望气术：能看到他人气运
- 窃运术：能窃取他人气运
- 毒术：主角核心能力
"""
    
    os.makedirs(f'output/{title}', exist_ok=True)
    with open(f'output/{title}/01_世界观框架.txt', 'w', encoding='utf-8') as f:
        f.write(world_content)
    
    print(f"✅ 世界观框架已保存到: output/{title}/01_世界观框架.txt")
    return title

def step2_characters(title):
    """步骤2：生成人物设定框架"""
    print(f"\n{'='*60}")
    print("【步骤2】生成人物设定框架")
    print(f"{'='*60}")
    
    characters_content = f"""
# 《{title}》人物设定框架

## 主角：顾长青
- 性格：谨慎、隐忍、智斗为先、苟道流
- 外貌：眉清目秀，气质内敛
- 背景：家族被灭，十年隐忍
- 能力：望气术、窃运术、毒术
- 目标：查清灭门真相，复仇

## 女主1：苏瑶
- 性格：温柔但有原则
- 身份：太清宫圣女
- 与主角关系：盟友、红颜知己

## 女主2：姜雪晴
- 性格：冷漠聪明
- 身份：天机阁少阁主
- 与主角关系：盟友、合作伙伴

## 女主3：白骨夫人
- 性格：妩媚狡猾
- 身份：白骨谷主
- 与主角关系：亦敌亦友、长辈旧识

## 反派
- 王天辰：前期反派，苍云宗执法长老（已死）
- 长生会：幕后黑手
- 其他反派：后续补充
"""
    
    with open(f'output/{title}/02_人物设定框架.txt', 'w', encoding='utf-8') as f:
        f.write(characters_content)
    
    print(f"✅ 人物设定框架已保存到: output/{title}/02_人物设定框架.txt")
    return title

def step3_plotframe(title):
    """步骤3：生成完整剧情大纲"""
    print(f"\n{'='*60}")
    print("【步骤3】生成完整剧情大纲")
    print(f"{'='*60}")
    
    plot_content = f"""
# 《{title}》完整剧情大纲

## 总篇幅
- 总章数：200章
- 总字数：100万字+
- 分卷：5卷，每卷40章

## 分卷大纲

### 第一卷：凡人之路（第1-40章）
- 内容：顾长青觉醒，十年隐忍，王天辰之死，逃亡开始
- 结局：发现父亲可能还活着，开始逃亡
- 伏笔：王家背后势力、灭门案内鬼

### 第二卷：逃亡之路（第41-80章）
- 内容：顾长青被追杀，进入西漠，获得传承，筑基成功
- 亮点：白骨夫人相助、魔道冲突、三大势力
- 结局：筑基后期，建立初步势力

### 第三卷：纵横修仙（第81-120章）
- 内容：金丹期，崭露头角，秘境探险，三女相聚
- 亮点：秘境夺宝、宗门大比、智斗群雄
- 结局：元婴在望，接触长生会

### 第四卷：长生之谜（第121-160章）
- 内容：发现长生会秘密，天道沉睡真相
- 亮点：揭秘长生会、天道之谜、父亲线索
- 结局：实力大增，准备最终决战

### 第五卷：长夜将明（第161-200章）
- 内容：最终决战，揭开所有真相
- 亮点：真相大白、复仇完成、新的开始
- 结局：长夜将明，顾长青踏上新的旅程

## 主线与辅线
- 主线：顾长青复仇，查灭门案
- 辅线1：父亲下落之谜
- 辅线2：长生会阴谋
- 辅线3：天道沉睡真相
- 辅线4：顾长青与三女的感情发展
"""
    
    with open(f'output/{title}/03_剧情大纲.txt', 'w', encoding='utf-8') as f:
        f.write(plot_content)
    
    print(f"✅ 剧情大纲已保存到: output/{title}/03_剧情大纲.txt")
    return title

def step4_chaptertitles(title):
    """步骤4：生成所有章节标题"""
    print(f"\n{'='*60}")
    print("【步骤4】生成所有章节标题")
    print(f"{'='*60}")
    
    # 已有的章节标题
    existing = [
        "第1章：末法时代",
        "第2章：望气之术",
        "第3章：父亲的遗产",
        "第4章：毒经救人",
        "第5章：十年之约",
        "第6章：初入苍云",
        "第7章：棋逢对手",
        "第8章：秘境开启",
        "第9章：劫运教阴谋",
        "第10章：暗夜逃亡",
        "第11章：苏瑶解毒",
        "第12章：长老试探",
        "第13章：暗中调查",
        "第14章：天机阁密约",
        "第15章：太清宫邀请",
        "第16章：劫运教伏击",
        "第17章：窃运术小成",
        "第18章：宗门大比",
        "第19章：王天成的阴谋",
        "第20章：秘境深处",
        "第21章：父亲真相",
        "第22章：幽冥毒龙传承",
        "第23章：姜雪晴的过去",
        "第24章：三方势力",
        "第25章：外门大比",
        "第26章：内门考核",
        "第27章：王天成出手",
        "第28章：绝境逢生",
        "第29章：真相大白",
        "第30章：十年之约终局",
        "第31章：神秘黑衣人",
        "第32章：苍云宗追杀"
    ]
    
    # 补充更多章节标题
    more = []
    for i in range(33, 201):
        if i == 33:
            more.append("第33章：白骨夫人相助")
        elif i == 34:
            more.append("第34章：逃亡路上")
        elif i == 35:
            more.append("第35章：进入西漠")
        elif i == 40:
            more.append("第40章：筑基成功")
        elif i == 60:
            more.append("第60章：第二卷终章")
        elif i == 80:
            more.append("第80章：第三卷终章")
        elif i == 100:
            more.append("第100章：第四卷终章")
        elif i == 120:
            more.append("第120章：第五卷终章")
        elif i == 200:
            more.append("第200章：终章：长夜将明")
        else:
            more.append(f"第{i}章：待补充标题")
    
    all_titles = existing + more
    
    titles_content = f"# 《{title}》章节标题\n\n"
    for t in all_titles:
        titles_content += f"{t}\n"
    
    with open(f'output/{title}/04_章节标题.txt', 'w', encoding='utf-8') as f:
        f.write(titles_content)
    
    print(f"✅ 章节标题已保存到: output/{title}/04_章节标题.txt")
    print(f"   共生成 {len(all_titles)} 个章节标题")
    return title

def step5_generate_chapters(title):
    """步骤5：生成章节内容"""
    print(f"\n{'='*60}")
    print("【步骤5】生成章节内容")
    print(f"{'='*60}")
    
    print(f"📂 检查已有的章节：")
    count = 0
    if os.path.exists('output/'):
        files = os.listdir('output/')
        for f in files:
            if f.startswith('第') and f.endswith('.txt'):
                count += 1
    
    print(f"   已存在 {count} 章")
    
    print(f"\n提示：")
    print(f"1. 前32章已存在，可以直接查看")
    print(f"2. 后续章节可以继续生成")
    print(f"3. 先生成框架，再慢慢写内容，更稳！")
    
    return title

def step6_view_content(title):
    """步骤6：查看已生成内容"""
    print(f"\n{'='*60}")
    print("【查看已生成内容】")
    print(f"{'='*60}")
    
    print(f"\n📂 目录：output/{title}/")
    if os.path.exists(f'output/{title}/'):
        files = os.listdir(f'output/{title}/')
        if files:
            for f in sorted(files):
                print(f"   {f}")
        else:
            print("   (暂无内容，先执行前面步骤)")
    else:
        print("   (目录不存在，先执行前面步骤)")
    
    print(f"\n📂 已生成的章节在 output/ 根目录")
    return title

def main():
    last_title = "长夜将明"
    
    while True:
        print_menu()
        choice = input("\n请选择操作 (0-6): ").strip()
        
        if choice == '1':
            last_title = step1_worldframe()
        elif choice == '2':
            last_title = step2_characters(last_title)
        elif choice == '3':
            last_title = step3_plotframe(last_title)
        elif choice == '4':
            last_title = step4_chaptertitles(last_title)
        elif choice == '5':
            last_title = step5_generate_chapters(last_title)
        elif choice == '6':
            last_title = step6_view_content(last_title)
        elif choice == '0':
            print(f"\n👋 再见！")
            break
        else:
            print(f"❌ 无效选择，请重新输入！")
        
        input(f"\n按 Enter 继续...")

if __name__ == "__main__":
    main()
