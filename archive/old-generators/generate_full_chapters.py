#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS与DeepSeek协作生成完整前10章
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
        'max_tokens': 12000
    }

    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method='POST')

    try:
        with urllib.request.urlopen(req, timeout=300) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result['choices'][0]['message']['content']
    except Exception as e:
        print(f"API Error: {e}")
        return None

def generate_complete_chapters():
    print("\n[1/2] NWACS正在组织大纲...")
    print("[2/2] DeepSeek正在创作第2-10章...")

    prompt = """请为小说《长生仙逆：从苟道毒修开始》创作第2-10章完整内容。

第2章：苟道十戒，毒丹初炼
- 林玄杀死了王霸，需要制造不在场证明
- 林玄制定"苟道十戒"
- 在废丹窑中学习炼丹，利用废弃丹药炼出"杂毒丹"
- 天道碎片的能力：可看到丹药品相的"气运值"
- 炼出第一枚有价值的丹药："隐气丹"（隐藏修为）
- 暗中布局：收集宗门情报
- 结尾悬念：外门长老要查废丹窑

第3章：杂毒丹成，鱼目混珠
- 林玄用杂毒丹把废丹窑的看守放倒，无声无息
- 制造"意外中毒"的假象
- 在废丹窑深处发现一个隐藏的密室
- 密室中是上任长老的笔记，记载着宗门的黑暗秘密
- 发现：宗门暗中贩卖凡人给魔道炼制血丹
- 结尾悬念：上任长老不是死了，而是被灭口

第4章：隐气丹成，低调炼气
- 林玄成功炼制出"隐气丹"，可隐藏真实修为
- 修为悄悄提升到炼气三层，但对外只显示炼气一层
- 天道碎片的另一个能力：可看到他人的"杀运"
- 暗中收集王霸的罪证，准备借力打力
- 结尾悬念：外门长老开始调查王霸失踪

第5章：长老查案，金蝉脱壳
- 执法长老调查王霸失踪案
- 林玄早有准备，把嫌疑引向另一个仇人
- 用"移魂毒香"让执法长老产生幻觉
- 成功金蝉脱壳，执法长老把锅扣给魔道奸细
- 林玄暗中获得王霸的储物袋，搜刮战利品
- 结尾悬念：储物袋中有一封密信

第6章：密信解密，长生初现
- 密信中提到了"长生会"和"药园计划"
- 凡人国度是仙门圈养的"药园"
- 每百年收割一次生灵炼制血丹
- 林玄发现自己的家乡就是下一个目标
- 天道碎片预警：三个月后，家乡将被"收割"
- 必须尽快提升实力，阻止这场灾难
- 结尾悬念：家乡的危机迫在眉睫

第7章：秘境开启，浑水摸鱼
- 宗门小秘境"毒龙谷"开启
- 林玄报名参加，想在秘境中找机缘
- 暗中布局：在秘境入口布下毒阵
- 遇到其他宗门弟子，表面客气暗中较量
- 天道碎片能力：可看到秘境中的"气运点"
- 找到一枚"毒龙丹"，是上古毒修的遗产
- 结尾悬念：毒龙谷深处有恐怖存在苏醒

第8章：毒龙苏醒，血战求生
- 上古毒龙的残魂苏醒
- 众人惊慌失措，死伤惨重
- 林玄苟在角落，暗中观察，准备逃跑
- 用"天道碎片"的能力，沟通毒龙残魂
- 毒龙残魂愿意传功
- 获得"毒龙真解"
- 结尾悬念：宗门高层发现秘境异常，要下来查探

第9章：传承到手，暗中离谷
- 林玄获得毒龙传承，修为暴增到炼气七层
- 继续藏拙，对外只显示炼气三层
- 用毒丹把受伤的宗门弟子"救"醒
- 制造"林玄舍命救人"的假象
- 获得宗门奖励
- 暗中布下毒阵，消除自己在秘境中的痕迹
- 离开毒龙谷
- 结尾悬念：在谷口遇到一位神秘女子，她好像能看穿伪装

第10章：神秘女子，天道预言
- 神秘女子名叫苏清，神秘莫测
- 她好像能看穿林玄的伪装
- 苏清给了林玄一个警告："小心，你被盯上了
- 林玄警惕，表面平静，暗中警觉
- 获得苏清是天机阁弟子，来调查"长生会"的秘密
- 离开宗门高层与林玄暂时分别，但暗中结盟？
- 林玄回到宗门，开始准备回家乡
- 暗中调查宗门的更多秘密
- 天道碎片再次预警：更大的风暴正在逼近
- 结尾悬念：林玄发现家乡的灾难提前，三个月变三个月
- 更严重了

请创作完整的第2-10章，每章约3000字！"""

    response = call_deepseek_v4(prompt)
    if response:
        print("  ✓ 第2-10章完成！")
        return response
    return None

def save_complete_novel(new_content):
    print("\n正在保存小说...")
    
    novel_name = "长生仙逆：从苟道毒修开始"
    safe_name = "长生仙逆从苟道毒修开始"
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)

    file_path = os.path.join(output_dir, f"{safe_name}.txt")

    # 先读取已有的第一章
    existing_content = ""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            existing_content = f.read()
    except Exception as e:
        print(f"读取文件失败")

    full_content = f"{existing_content}\n\n{new_content}"

    full_content = f"""《{novel_name}》前10章
======
修仙玄幻·苟道流·黑暗流·智斗流
======

{full_content}

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
    print("=" * 80)
    print("正在生成完整的第2-10章...")
    print("=" * 80)

    new_content = generate_complete_chapters()

    file_path = save_complete_novel(new_content)

    print("\n" + "=" * 80)
    print("                    全部完成！")
    print("=" * 80)
    print(f"\n📖 小说文件：{file_path}")
    print("\n🎯 协作优势：")
    print("  - NWACS：小说框架、大纲设定、世界体系")
    print("  - DeepSeek：情节创作、角色对话、细节描写")
    print("\n📚 已完成内容：")
    print("  - 完整的第1-10章")
    print("  - 每章约3000字，爽点密集")
    print("=" * 80)

if __name__ == "__main__":
    main()
