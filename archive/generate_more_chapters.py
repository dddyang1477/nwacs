#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS与DeepSeek协作生成第2-10章小说
"""

import os
import sys
import json
import urllib.request
import urllib.error
import time

sys.stdout.reconfigure(encoding='utf-8')

def load_config():
    config = {}
    if os.path.exists('config.json'):
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
    return config

def call_deepseek_v4(prompt, system_prompt=None):
    config = load_config()
    if not config.get('api_key'):
        print("ERROR: API Key not configured")
        return None

    if not system_prompt:
        system_prompt = """你是一位顶尖玄幻网文大神，擅长苟道流、黑暗流、智斗流。
你创作的小说节奏紧凑、爽点密集、画面感强、悬念钩子、不水文。
每章约3000-3500字，300字一小爽点，1000字一大爽点，每章结尾必留悬念。"""

    url = config.get('base_url', 'https://api.deepseek.com/v1') + '/chat/completions'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {config.get("api_key")}'
    }

    data = {
        'model': config.get('model', 'deepseek-v4-pro'),
        'messages': [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': prompt}
        ],
        'temperature': 0.8,
        'max_tokens': 6000
    }

    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method='POST')

    try:
        with urllib.request.urlopen(req, timeout=180) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result['choices'][0]['message']['content']
    except Exception as e:
        print(f"API Error: {e}")
        return None

def generate_chapter_2():
    print("  正在生成第2章...")
    prompt = """请为小说《长生仙逆：从苟道毒修开始》创作第2章：

第2章：苟道十戒，毒丹初炼

承接第1章结尾：
- 林玄杀死了王霸，需要制造不在场证明
- 林玄制定"苟道十戒"
- 在废丹窑中学习炼丹，利用废弃丹药炼出"杂毒丹"
- 天道碎片的能力：可看到丹药品相的"气运值"
- 炼出第一枚有价值的丹药："隐气丹"（隐藏修为）
- 暗中布局：收集宗门情报
- 结尾悬念：外门长老要查废丹窑

请创作完整的第2章，约3000字，爽点密集！"""
    return call_deepseek_v4(prompt)

def generate_chapter_3():
    print("  正在生成第3章...")
    prompt = """请为小说《长生仙逆：从苟道毒修开始》创作第3章：

第3章：杂毒丹成，鱼目混珠

承接第2章结尾：
- 林玄用杂毒丹把废丹窑的看守放倒，无声无息
- 制造"意外中毒"的假象
- 在废丹窑深处发现一个隐藏的密室
- 密室中是上任长老的笔记，记载着宗门的黑暗秘密
- 发现：宗门暗中贩卖凡人给魔道炼制血丹
- 结尾悬念：上任长老不是死了，而是被灭口

请创作完整的第3章，约3000字，爽点密集！"""
    return call_deepseek_v4(prompt)

def generate_chapter_4():
    print("  正在生成第4章...")
    prompt = """请为小说《长生仙逆：从苟道毒修开始》创作第4章：

第4章：隐气丹成，低调炼气

承接第3章结尾：
- 林玄成功炼制出"隐气丹"，可隐藏真实修为
- 修为悄悄提升到炼气三层，但对外只显示炼气一层
- 天道碎片的另一个能力：可看到他人的"杀运"
- 发现王霸身上缠绕着浓重的杀运，迟早会横死
- 暗中收集王霸的罪证，准备借力打力
- 结尾悬念：王霸要对林玄下黑手（注意这里王霸其实已经死了，林玄要处理后果）

请创作完整的第4章，约3000字，爽点密集！"""
    return call_deepseek_v4(prompt)

def generate_chapter_5():
    print("  正在生成第5章...")
    prompt = """请为小说《长生仙逆：从苟道毒修开始》创作第5章：

第5章：王霸寻事，毒针反杀

承接第4章结尾：
- 王霸要对林玄下黑手，但林玄早有准备
- 在周围布下"毒雾迷阵"
- 用"无影毒针"反杀王霸
- 但留了活口，让王霸"意外"摔下山崖成了傻子
- 制造完美的不在场证明
- 从王霸身上搜到了与魔道勾结的证据
- 结尾悬念：王霸背后有人，开始调查

请创作完整的第5章，约3000字，爽点密集！"""
    return call_deepseek_v4(prompt)

def generate_chapter_6():
    print("  正在生成第6章...")
    prompt = """请为小说《长生仙逆：从苟道毒修开始》创作第6章：

第6章：长老查案，金蝉脱壳

承接第5章结尾：
- 执法长老调查王霸案
- 林玄早有准备，把嫌疑引向另一个仇人
- 用"移魂毒香"让执法长老产生幻觉，看到虚假线索
- 成功金蝉脱壳
- 执法长老把锅扣给了魔道奸细
- 林玄暗中获得王霸的储物袋，搜刮战利品
- 结尾悬念：储物袋中有一封密信，指向更大的阴谋

请创作完整的第6章，约3000字，爽点密集！"""
    return call_deepseek_v4(prompt)

def generate_chapter_7():
    print("  正在生成第7章...")
    prompt = """请为小说《长生仙逆：从苟道毒修开始》创作第7章：

第7章：密信解密，长生初现

承接第6章结尾：
- 密信中提到了"长生会"和"药园计划"
- 原来凡人国度是仙门圈养的"药园"
- 每百年收割一次生灵炼制血丹
- 林玄发现自己的家乡就是下一个目标
- 天道碎片预警：三个月后，家乡将被"收割"
- 必须尽快提升实力，阻止这场灾难
- 结尾悬念：家乡的危机迫在眉睫

请创作完整的第7章，约3000字，爽点密集！"""
    return call_deepseek_v4(prompt)

def generate_chapter_8():
    print("  正在生成第8章...")
    prompt = """请为小说《长生仙逆：从苟道毒修开始》创作第8章：

第8章：秘境开启，浑水摸鱼

承接第7章结尾：
- 宗门小秘境"毒龙谷"开启
- 林玄报名参加，想在秘境中找机缘
- 暗中布局：在秘境入口布下毒阵，准备浑水摸鱼
- 遇到其他宗门弟子，表面客气暗中较量
- 天道碎片能力：可看到秘境中的"气运点"
- 找到一枚"毒龙丹"，是上古毒修的遗产
- 结尾悬念：毒龙谷深处有恐怖的存在苏醒

请创作完整的第8章，约3000字，爽点密集！"""
    return call_deepseek_v4(prompt)

def generate_chapter_9():
    print("  正在生成第9章...")
    prompt = """请为小说《长生仙逆：从苟道毒修开始》创作第9章：

第9章：毒龙苏醒，血战求生

承接第8章结尾：
- 上古毒龙的残魂苏醒
- 众人惊慌失措，死伤惨重
- 林玄苟在角落，暗中观察，准备逃跑
- 但发现毒龙的残魂虚弱，是绝佳的机缘
- 用"天道碎片"的能力，沟通毒龙残魂
- 毒龙残魂发现林玄是"命运之外的人"，愿意传功
- 林玄获得"毒龙真解"
- 结尾悬念：宗门高层发现秘境异常，要下来查探

请创作完整的第9章，约3000字，爽点密集！"""
    return call_deepseek_v4(prompt)

def generate_chapter_10():
    print("  正在生成第10章...")
    prompt = """请为小说《长生仙逆：从苟道毒修开始》创作第10章：

第10章：传承到手，暗中离谷

承接第9章结尾：
- 林玄获得毒龙传承，修为暴增到炼气七层
- 但继续藏拙，对外只显示炼气三层
- 用毒丹把受伤的宗门弟子"救"醒
- 制造"林玄舍命救人"的假象
- 获得宗门奖励，身份提升
- 暗中布下毒阵，消除自己在秘境中的痕迹
- 离开毒龙谷，准备回家乡阻止灾难
- 结尾悬念：在谷口遇到一位神秘女子，她好像能看穿林玄的伪装

请创作完整的第10章，约3000字，爽点密集！"""
    return call_deepseek_v4(prompt)

def save_chapters_to_file(chapters):
    print("\n正在保存完整小说...")
    novel_name = "长生仙逆：从苟道毒修开始"
    safe_name = "长生仙逆从苟道毒修开始"
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)

    file_path = os.path.join(output_dir, f"{safe_name}.txt")

    full_content = f"""《{novel_name}》前10章
======
修仙玄幻·苟道流·黑暗流·智斗流
======

{chapters}

======
本小说由 NWACS × DeepSeek V4 联合创作
NWACS提供框架与大纲
DeepSeek弥补内容创作缺陷
生成时间：{time.strftime('%Y-%m-%d %H:%M:%S')}
"""

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(full_content)

    print(f"  ✓ 小说已保存到：{file_path}")
    return file_path

def main():
    print("\n" + "=" * 80)
    print("          NWACS × DeepSeek 小说协作系统")
    print("          正在生成第2-10章...")
    print("=" * 80)

    # 先读取已有的第一章
    existing_chapter = ""
    try:
        with open('output/长生仙逆从苟道毒修开始.txt', 'r', encoding='utf-8') as f:
            existing_chapter = f.read()
        # 只保留第一章内容
        lines = existing_chapter.split('\n')
        first_chapter = []
        for line in lines:
            first_chapter.append(line)
            if "======" in line and len(first_chapter) > 100:
                break
        existing_chapter = '\n'.join(first_chapter)
    except Exception as e:
        print(f"读取第一章失败：{e}")
        return

    # 生成后续章节
    all_chapters = existing_chapter + "\n\n"

    chapters = [
        ("2", generate_chapter_2),
        ("3", generate_chapter_3),
        ("4", generate_chapter_4),
        ("5", generate_chapter_5),
        ("6", generate_chapter_6),
        ("7", generate_chapter_7),
        ("8", generate_chapter_8),
        ("9", generate_chapter_9),
        ("10", generate_chapter_10),
    ]

    for chapter_num, func in chapters:
        content = func()
        if content:
            all_chapters += f"\n\n{content}\n"
            print(f"  ✓ 第{chapter_num}章完成！")

    file_path = save_chapters_to_file(all_chapters)

    print("\n" + "=" * 80)
    print("                    全部章节生成完成！")
    print("=" * 80)
    print(f"\n📖 小说文件：{file_path}")
    print("\n🎯 创作说明：")
    print("  - NWACS提供：小说框架、大纲设定、世界体系")
    print("  - DeepSeek弥补：情节创作、角色对话、细节描写")
    print("\n📚 小说内容：")
    print("  - 第1-10章完整内容")
    print("  - 每章约3000字")
    print("  - 300字一小爽点，1000字一大爽点")
    print("  - 每章结尾必留悬念")
    print("=" * 80)

if __name__ == "__main__":
    main()
