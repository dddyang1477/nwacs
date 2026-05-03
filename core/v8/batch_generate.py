#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量生成《天机道主》第11-100章脚本
以5章为一组，跟踪剧情状态，确保连贯性
"""

import sys
import os
import json
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "sk-f3246fbd1eef446e9a11d78efefd9bba"
BASE_URL = "https://api.deepseek.com"

# 剧情状态跟踪
PLOT_STATE = {
    "current_chapter": 10,
    "character_states": {
        "叶青云": {
            "修为": "炼气四层",
            "location": "青云宗",
            "goals": ["寻找父亲失踪真相", "收集天机之子信息", "反杀天道"],
            "secrets": ["拥有因果推演能力", "知道天机之子真相", "穿越者"]
        },
        "苏沐雪": {
            "修为": "炼气三层",
            "location": "青云宗",
            "bloodline": "冰凤血脉（已部分觉醒）",
            "relationship_with_ye": "信任、有好感"
        },
        "林啸天": {
            "修为": "金丹期",
            "status": "怀疑叶青云",
            "action": "正在调查主角"
        },
        "楚凌霄": {
            "修为": "金丹期",
            "location": "未出场",
            "knowledge": "不知道叶青云的存在"
        },
        "王铁柱": {
            "appearance": "未出场"
        }
    },
    "plot_points_completed": [
        "叶青云穿越",
        "觉醒天机棋子",
        "算计林逸",
        "进入藏经阁",
        "见到大长老",
        "获得修炼资源"
    ],
    "next_plot_points": [
        "王铁柱出场",
        "楚凌霄出场",
        "发现天机之子真相",
        "苏沐雪血脉觉醒",
        "离开青云宗",
        "建立天机阁"
    ],
    "hidden_secrets": {
        "叶青云父亲": "失踪与青云宗有关",
        "楚凌霄因果之眼": "是天道监控器",
        "魔教": "是上一代天机之子的反抗组织"
    }
}

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

def save_plot_state():
    """保存剧情状态"""
    state_file = "novel/plot_state.json"
    with open(state_file, 'w', encoding='utf-8') as f:
        json.dump(PLOT_STATE, f, ensure_ascii=False, indent=2)
    print(f"   💾 剧情状态已保存")

def load_plot_state():
    """加载剧情状态"""
    state_file = "novel/plot_state.json"
    if os.path.exists(state_file):
        global PLOT_STATE
        with open(state_file, 'r', encoding='utf-8') as f:
            PLOT_STATE = json.load(f)
        print(f"   📂 剧情状态已加载，当前至第{PLOT_STATE['current_chapter']}章")

def get_chapter_prompt(chapter_num):
    """根据章节号生成对应的提示词"""
    
    chapter_templates = {
        11: {
            "title": "第11章：秘境初体验",
            "content": """叶青云进入青云秘境，遇到第一个试炼。在秘境中，他发现了与父亲有关的线索——一枚刻着"叶"字的玉佩！""",
            "plot_updates": {
                "character_states.叶青云.location": "青云秘境",
                "plot_points_completed": "+= ['进入青云秘境']"
            }
        },
        12: {
            "title": "第12章：因果真经最后一页",
            "content": """叶青云在秘境中找到一处上古遗迹，终于看到了《因果真经》的最后一页！上面记载着封印天道的方法——但需要所有天机之子的气运作为祭品！""",
            "plot_updates": {
                "hidden_secrets.因果真经最后一页": "已发现",
                "plot_points_completed": "+= ['发现封印天道的方法']"
            }
        },
        13: {
            "title": "第13章：王铁柱登场",
            "content": """叶青云在秘境中遇到了一个胖乎乎的年轻人——王铁柱！这胖子刚出场就喊着"救命啊，我还没娶媳妇呢！"然后用身体帮叶青云挡下了致命一击！叶青云震惊发现：这个凡人竟然拥有因果免疫体质！""",
            "plot_updates": {
                "character_states.王铁柱.appearance": "已出场",
                "character_states.王铁柱.location": "青云秘境",
                "plot_points_completed": "+= ['王铁柱登场']"
            }
        },
        14: {
            "title": "第14章：因果免疫",
            "content": """叶青云收王铁柱为徒，开始测试他的因果免疫体质。所有因果术法对王铁柱都无效！叶青云意识到：这胖子就是自己一直在找的"保险"！""",
            "plot_updates": {
                "plot_points_completed": "+= ['发现王铁柱因果免疫体质']"
            }
        },
        15: {
            "title": "第15章：秘境大比",
            "content": """青云秘境中的年轻弟子开始互相厮杀，争夺机缘。林啸天安排的人终于出手——目标正是叶青云！叶青云利用因果线，让那几人互相残杀，坐收渔翁之利。""",
            "plot_updates": {}
        },
        16: {
            "title": "第16章：楚凌霄出场",
            "content": """天衍圣地的圣子楚凌霄终于登场了！他带着"因果之眼"，一眼就看穿了叶青云布下的因果线！但楚凌霄只看到叶青云炼气四层的修为，不屑地说："这种蝼蚁，也配让我动手？"叶青云故意示弱，让楚凌霄不屑于杀他——这正是他想要的效果！""",
            "plot_updates": {
                "character_states.楚凌霄.location": "青云秘境",
                "character_states.楚凌霄.knowledge": "知道叶青云的存在，但不屑于杀",
                "plot_points_completed": "+= ['楚凌霄出场']"
            }
        },
        17: {
            "title": "第17章：因果之眼",
            "content": """叶青云暗中观察楚凌霄的因果之眼，通过天机推演，他发现了一个恐怖的真相——楚凌霄的眼睛根本不是天赋，而是天道植入的监控器！""",
            "plot_updates": {
                "hidden_secrets.楚凌霄因果之眼": "已发现是天道监控器"
            }
        },
        18: {
            "title": "第18章：苏沐雪遇险",
            "content": """苏沐雪在秘境中被妖兽围攻，叶青云暗中出手相救。在战斗中，苏沐雪的冰凤血脉再次觉醒——这次，她展现出了"因果净化"的能力！""",
            "plot_updates": {
                "character_states.苏沐雪.bloodline": "冰凤血脉（因果净化能力觉醒）"
            }
        },
        19: {
            "title": "第19章：天道诅咒",
            "content": """苏沐雪的血脉觉醒引起了天道的注意！天道降下诅咒，试图控制苏沐雪！叶青云用因果线锁住苏沐雪，表面上冷酷，实则是在保护她！""",
            "plot_updates": {
                "hidden_secrets.苏沐雪身上的因果诅咒": "已出现"
            }
        },
        20: {
            "title": "第20章：雪地等待",
            "content": """苏沐雪被叶青云锁住后，非但没有怨恨，反而在雪地等了他三天三夜！当叶青云出现时，她只说了一句："我知道你在保护我。"两人终于确认了彼此的心意！""",
            "plot_updates": {
                "character_states.苏沐雪.relationship_with_ye": "已互定终身"
            }
        }
    }
    
    # 后续章节的通用模板
    if chapter_num in chapter_templates:
        template = chapter_templates[chapter_num]
    else:
        # 根据章节范围生成通用模板
        if 21 <= chapter_num <= 30:
            template = {
                "title": f"第{chapter_num}章：离开青云宗",
                "content": """叶青云带着苏沐雪和王铁柱离开青云宗，以"历练"为名开始建立自己的势力。在凡间，他们以"天机阁"为名——表面是算命占卜的江湖组织，实则是收集情报、布局因果的超级网络！""",
                "plot_updates": {}
            }
        elif 31 <= chapter_num <= 40:
            template = {
                "title": f"第{chapter_num}章：天机阁成立",
                "content": """天机阁在凡间迅速发展，叶青云开始收集其他天机之子的信息。同时，楚凌霄也在不断调查叶青云，两人的博弈越来越精彩！""",
                "plot_updates": {}
            }
        elif 41 <= chapter_num <= 50:
            template = {
                "title": f"第{chapter_num}章：魔教教主",
                "content": """魔教教主现身！叶青云发现，所谓的"魔教"根本不是邪教，而是上一代天机之子建立的反抗组织——"弑神者"！""",
                "plot_updates": {}
            }
        elif 51 <= chapter_num <= 60:
            template = {
                "title": f"第{chapter_num}章：林逸归来",
                "content": """被废修为的林逸回来了！他被魔教改造，成为魔修！但叶青云没有杀他，反而让他成为自己的"因果替身"——用来转移天衍圣地的注意力！""",
                "plot_updates": {}
            }
        elif 61 <= chapter_num <= 70:
            template = {
                "title": f"第{chapter_num}章：楚凌霄的追杀",
                "content": """楚凌霄终于发现叶青云不简单，开始全力追杀！但叶青云利用因果线，让楚凌霄每次都扑空，反而帮他除掉了不少对手！""",
                "plot_updates": {}
            }
        elif 71 <= chapter_num <= 80:
            template = {
                "title": f"第{chapter_num}章：上一代天机之子的真相",
                "content": """魔教教主揭示了上一代天机之子的真相——他们不是被天道选中，而是被天道制造出来的"食物"！每三千年，天道就会制造一批天机之子，让他们互相厮杀，最终吞噬他们的气运！""",
                "plot_updates": {}
            }
        elif 81 <= chapter_num <= 90:
            template = {
                "title": f"第{chapter_num}章：因果之眼的秘密",
                "content": """楚凌霄终于发现了自己眼睛的秘密——他的"因果之眼"根本不是天赋，而是天道植入的监控器！他每杀一个天机之子，自己的意识就会消失一部分！""",
                "plot_updates": {}
            }
        elif 91 <= chapter_num <= 100:
            template = {
                "title": f"第{chapter_num}章：楚凌霄的崩溃",
                "content": """楚凌霄在叶青云的设计下，亲手杀死了第一百个天机之子——他的师姐！楚凌霄终于恢复了全部意识，看到了师姐临死前留下的信，彻底崩溃！""",
                "plot_updates": {}
            }
        else:
            template = {
                "title": f"第{chapter_num}章",
                "content": """剧情继续发展...""",
                "plot_updates": {}
            }
    
    return template

def generate_chapter(chapter_num):
    """生成单章"""
    print(f"\n" + "="*60)
    print(f"📝 生成第{chapter_num}章")
    print("="*60)
    
    template = get_chapter_prompt(chapter_num)
    
    state_json = json.dumps(PLOT_STATE, ensure_ascii=False, indent=2)
    
    prompt = f"""请为长篇玄幻小说《天机道主》撰写第{chapter_num}章。

## 小说核心设定
- 主角：叶青云，前世天算师，拥有因果推演能力
- 世界观：天玄大陆，九重天境修炼体系
- 核心设定：天机乱象，天道制造天机之子互相厮杀

## 当前剧情状态
```json
{state_json}
```

## 本章核心剧情
{template['content']}

## 本章要求
**字数**：2000-3000字
**风格**：符合前面章节的风格，智斗为主，爽点密集，情感自然
**结尾钩子**：每章结尾留下悬念
**连贯性**：确保与前面章节的剧情连贯，人物性格一致

请开始撰写第{chapter_num}章。"""

    system_prompt = """你是一位顶尖的玄幻小说作家，擅长写长篇连载小说。
写作要点：
1. 确保剧情连贯性，人物性格一致
2. 每章结尾留下钩子
3. 智斗要精彩，爽点要密集
4. 情感描写要自然
5. 节奏要适中"""

    result = call_deepseek(prompt, system_prompt, temperature=0.85)
    
    if result:
        # 更新剧情状态
        PLOT_STATE["current_chapter"] = chapter_num
        
        # 保存剧情状态
        save_plot_state()
        
        print(f"   ✅ 第{chapter_num}章完成")
        return result
    else:
        print(f"   ❌ 第{chapter_num}章失败")
        return None

def check_plot_coherence():
    """检测剧情连贯性一致性"""
    print("\n" + "="*60)
    print("🔍 检测剧情连贯性一致性")
    print("="*60)
    
    prompt = f"""请检测《天机道主》第1-100章的剧情连贯性一致性。

## 当前剧情状态
```json
{json.dumps(PLOT_STATE, ensure_ascii=False, indent=2)}
```

## 检测要求
请从以下几个方面进行检测：
1. **人物一致性**：人物性格、能力是否一致，是否有逻辑矛盾
2. **剧情连贯性**：前后剧情是否连贯，是否有明显bug
3. **设定一致性**：世界观、修炼体系、设定是否一致
4. **埋笔回收**：重要埋笔是否有铺垫，是否准备回收
5. **节奏合理性**：节奏是否合理，爽点分布是否均匀

请给出详细的检测报告。"""

    system_prompt = """你是一位专业的小说编辑，擅长检测长篇小说的剧情连贯性。
检测要点：
1. 客观公正，找出真正的问题
2. 给出具体的改进建议
3. 不仅指出问题，还要给出解决方案"""

    result = call_deepseek(prompt, system_prompt, temperature=0.7)
    
    if result:
        report_file = "novel/plot_coherence_report.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write("《天机道主》剧情连贯性检测报告\n")
            f.write("="*60 + "\n\n")
            f.write(f"检测时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(result)
        print(f"   ✅ 检测报告已保存：{report_file}")
        return result
    else:
        print(f"   ❌ 检测失败")
        return None

def main():
    print("="*60)
    print("📖 《天机道主》批量生成脚本")
    print("="*60)
    
    # 加载之前的剧情状态
    load_plot_state()
    
    # 确定起始和结束章节（先演示生成到30章，可修改为100）
    start_chapter = PLOT_STATE["current_chapter"] + 1
    end_chapter = 30  # 可修改为100
    
    print(f"\n计划生成第{start_chapter}-{end_chapter}章，共{end_chapter - start_chapter + 1}章")
    
    all_chapters = []
    
    # 按5章一组生成
    for group_start in range(start_chapter, end_chapter + 1, 5):
        group_end = min(group_start + 4, end_chapter)
        print(f"\n" + "="*60)
        print(f"📦 生成第{group_start}-{group_end}章")
        print("="*60)
        
        for chapter_num in range(group_start, group_end + 1):
            chapter_content = generate_chapter(chapter_num)
            if chapter_content:
                all_chapters.append((chapter_num, chapter_content))
                
                # 每生成5章保存一次
                if chapter_num % 5 == 0:
                    save_group_chapters(group_start, chapter_num, all_chapters[-5:])
        
        # 每组结束后休息一下
        if group_end < end_chapter:
            print("   ⏸️  休息5秒...")
            import time
            time.sleep(5)
    
    # 保存所有章节
    if all_chapters:
        save_all_chapters(all_chapters)
    
    # 检测剧情连贯性
    coherence_report = check_plot_coherence()
    
    print("\n" + "="*60)
    print("🎉 任务完成！")
    print("="*60)
    print(f"\n共生成 {len(all_chapters)} 章（第{start_chapter}-{PLOT_STATE['current_chapter']}章）")
    print(f"剧情连贯性检测已完成")

def save_group_chapters(start, end, chapters):
    """保存一组章节"""
    filename = f"novel/第{start}-{end}章.txt"
    content = []
    content.append(f"《天机道主》第{start}-{end}章\n")
    content.append("="*60 + "\n")
    content.append(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    content.append("="*60 + "\n\n")
    
    for chapter_num, chapter_content in chapters:
        content.append(chapter_content)
        content.append("\n\n" + "="*60 + "\n\n")
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.writelines(content)
    print(f"   💾 已保存：{filename}")

def save_all_chapters(chapters):
    """保存所有章节"""
    filename = "novel/《天机道主》第11-100章.txt"
    content = []
    content.append("《天机道主》第11-100章\n")
    content.append("="*60 + "\n")
    content.append(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    content.append("="*60 + "\n\n")
    
    for chapter_num, chapter_content in chapters:
        content.append(chapter_content)
        content.append("\n\n" + "="*60 + "\n\n")
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.writelines(content)
    print(f"   💾 完整章节集已保存：{filename}")

if __name__ == "__main__":
    main()