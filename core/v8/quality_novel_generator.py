#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DeepSeek + NWACS 逐章生成小说第31-100章
根据优化配置逐章生成，确保剧情连贯性
"""

import sys
import os
import json
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

def load_optimized_config():
    """加载优化配置"""
    with open("core/v8/engine/optimized_settings.json", 'r', encoding='utf-8') as f:
        return json.load(f)

def load_plot_state():
    """加载剧情状态"""
    with open("novel/plot_state.json", 'r', encoding='utf-8') as f:
        return json.load(f)

def save_plot_state(state):
    """保存剧情状态"""
    with open("novel/plot_state.json", 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def save_chapter(chapter_num, content):
    """保存单章"""
    filename = f"novel/第{chapter_num}章.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"《天机道主》第{chapter_num}章\n")
        f.write("="*60 + "\n")
        f.write(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*60 + "\n\n")
        f.write(content)
    print(f"   💾 第{chapter_num}章已保存")
    return filename

def get_chapter_outline(chapter_num, state, config):
    """获取章节大纲要求"""
    
    # 第31-40章：楚凌霄追杀、苏沐雪危机
    if 31 <= chapter_num <= 40:
        outlines = {
            31: {
                "title": "第31章：天衍圣地的阴影",
                "summary": "楚凌霄终于确认叶青云的存在，开始布局追杀。叶青云感受到被监视的压力。",
                "plot_updates": {
                    "楚凌霄.location": "已确认叶青云存在",
                    "叶青云.status": "感受到被监视"
                },
                "key_points": ["楚凌霄派人调查", "叶青云察觉异常", "增加过渡日常"]
            },
            32: {
                "title": "第32章：因果线的波动",
                "summary": "叶青云使用推演能力时发现异常，因果线出现波动。推演能力首次受到干扰。",
                "plot_updates": {
                    "能力受限": "推演出现干扰"
                },
                "key_points": ["推演能力首次受限", "发现天道监控", "增加能力代价描写"]
            },
            33: {
                "title": "第33章：苏沐雪的决断",
                "summary": "苏沐雪主动提出帮助叶青云分担压力，展现独立决策能力。",
                "plot_updates": {
                    "苏沐雪.主动性": "开始主动参与决策"
                },
                "key_points": ["苏沐雪独立行动", "提出不同看法", "两人讨论策略"]
            },
            34: {
                "title": "第34章：落凤城的暗流",
                "summary": "叶青云来到落凤城，开始为建立天机阁做准备。遇到当地势力的试探。",
                "plot_updates": {
                    "叶青云.location": "落凤城"
                },
                "key_points": ["新地图展开", "遭遇当地势力", "展示智慧布局"]
            },
            35: {
                "title": "第35章：王铁柱登场",
                "summary": "叶青云在落凤城遇到王铁柱。胖子喊着救命撞进叶青云的世界。",
                "plot_updates": {
                    "王铁柱.appearance": "已出场"
                },
                "key_points": ["王铁柱出场", "因果免疫体质初显", "搞笑与悬念并存"]
            },
            36: {
                "title": "第36章：天机阁初创",
                "summary": "叶青云开始建立天机阁，遇到了资金和人员的问题。",
                "plot_updates": {
                    "天机阁.status": "初创阶段"
                },
                "key_points": ["建立过程艰难", "解决资金问题", "收服第一批追随者"]
            },
            37: {
                "title": "第37章：情报网络的雏形",
                "summary": "天机阁开始发挥作用，收集到第一条重要情报。",
                "plot_updates": {
                    "天机阁.capability": "开始运转"
                },
                "key_points": ["情报收集", "发现其他天机之子线索", "展示信息差优势"]
            },
            38: {
                "title": "第38章：楚凌霄的试探",
                "summary": "楚凌霄派人试探叶青云，叶青云巧妙化解，展现智谋。",
                "plot_updates": {},
                "key_points": ["与楚凌霄势力首次交锋", "借刀杀人", "保护天机阁"]
            },
            39: {
                "title": "第39章：危机降临",
                "summary": "苏沐雪被楚凌霄的人抓走，叶青云面临艰难抉择。",
                "plot_updates": {
                    "苏沐雪.status": "被抓走"
                },
                "key_points": ["苏沐雪被抓", "叶青云内心挣扎", "设置重大危机"]
            },
            40: {
                "title": "第40章：因果的代价",
                "summary": "叶青云强行使用推演能力救人，付出沉重代价（精神力枯竭）。",
                "plot_updates": {
                    "叶青云.代价": "精神力严重消耗"
                },
                "key_points": ["强行推演的后果", "展现能力代价", "为营救埋下伏笔"]
            }
        }
        return outlines.get(chapter_num, {"title": f"第{chapter_num}章", "summary": "剧情继续发展", "key_points": []})
    
    # 第41-50章：天机阁发展、楚凌霄追杀升级
    elif 41 <= chapter_num <= 50:
        outlines = {
            41: {
                "title": "第41章：营救行动",
                "summary": "叶青云制定营救计划，利用天机阁的情报网络。",
                "plot_updates": {},
                "key_points": ["制定计划", "利用情报网", "展示布局能力"]
            },
            42: {
                "title": "第42章：楚凌霄的陷阱",
                "summary": "楚凌霄设下陷阱，叶青云意识到自己被算计了。",
                "plot_updates": {
                    "楚凌霄.status": "设下陷阱"
                },
                "key_points": ["楚凌霄的布局", "叶青云陷入危机", "展示对手智慧"]
            },
            43: {
                "title": "第43章：绝境逢生",
                "summary": "叶青云在绝境中找到突破口，利用因果反噬。",
                "plot_updates": {},
                "key_points": ["绝境中的机会", "利用因果律", "反杀成功"]
            },
            44: {
                "title": "第44章：苏沐雪的觉醒",
                "summary": "苏沐雪在被困时血脉完全觉醒，展现净化能力。",
                "plot_updates": {
                    "苏沐雪.bloodline": "冰凤血脉完全觉醒"
                },
                "key_points": ["血脉完全觉醒", "因果净化能力展现", "女性主角独立性"]
            },
            45: {
                "title": "第45章：真相的碎片",
                "summary": "发现楚凌霄因果之眼的秘密，他是天道的监控器。",
                "plot_updates": {
                    "楚凌霄.秘密": "因果之眼是天道监控器"
                },
                "key_points": ["揭示楚凌霄秘密", "天道监控真相", "增加世界观深度"]
            },
            46: {
                "title": "第46章：天机阁的扩张",
                "summary": "天机阁在落凤城站稳脚跟，开始扩张势力。",
                "plot_updates": {
                    "天机阁.status": "开始扩张"
                },
                "key_points": ["势力扩张", "新的追随者", "资源积累"]
            },
            47: {
                "title": "第47章：魔教的影子",
                "summary": "发现魔教的存在，魔教其实是上一代天机之子的反抗组织。",
                "plot_updates": {
                    "魔教.identity": "上一代天机之子的反抗组织"
                },
                "key_points": ["魔教真相", "弑神者组织", "引入新势力"]
            },
            48: {
                "title": "第48章：父亲的线索",
                "summary": "叶青云通过天机阁的情报，发现父亲失踪与青云宗有关的证据。",
                "plot_updates": {
                    "叶青云父亲": "确认与青云宗有关"
                },
                "key_points": ["父亲线索", "青云宗的秘密", "复仇动机强化"]
            },
            49: {
                "title": "第49章：林逸的变化",
                "summary": "林逸被废后加入魔教，被改造成魔修。",
                "plot_updates": {
                    "林逸.status": "被魔教改造"
                },
                "key_points": ["林逸归来", "魔修身份", "新的变数"]
            },
            50: {
                "title": "第50章：楚凌霄的觉醒",
                "summary": "楚凌霄开始怀疑自己的身份，意识被天道侵蚀。",
                "plot_updates": {
                    "楚凌霄.status": "开始怀疑自我"
                },
                "key_points": ["楚凌霄内心挣扎", "天道侵蚀", "悲剧色彩加深"]
            }
        }
        return outlines.get(chapter_num, {"title": f"第{chapter_num}章", "summary": "剧情继续发展", "key_points": []})
    
    # 第51-60章：棋手对决
    elif 51 <= chapter_num <= 60:
        outlines = {
            51: {
                "title": "第51章：三年之约",
                "summary": "叶青云与楚凌霄对峙，提出三年之约——届时一决胜负。",
                "plot_updates": {},
                "key_points": ["与楚凌霄对峙", "三年之约", "智谋较量"]
            },
            52: {
                "title": "第52章：各自筹谋",
                "summary": "叶青云利用三年时间布局，楚凌霄也在准备。",
                "plot_updates": {
                    "时间跳跃": "三年"
                },
                "key_points": ["时间跳跃", "双方各自准备", "展示成长"]
            },
            53: {
                "title": "第53章：天机乱象的征兆",
                "summary": "天机乱象的前兆出现，世界开始变得混乱。",
                "plot_updates": {
                    "天机乱象.status": "即将到来"
                },
                "key_points": ["异象频发", "天机紊乱", "大劫将至"]
            },
            54: {
                "title": "第54章：叶青云的修为突破",
                "summary": "三年修炼，叶青云突破到筑基期。",
                "plot_updates": {
                    "叶青云.修为": "筑基期"
                },
                "key_points": ["修为突破", "因果推演增强", "成长展示"]
            },
            55: {
                "title": "第55章：天机阁的势力",
                "summary": "天机阁成为一流势力，拥有了自己的情报网和战力。",
                "plot_updates": {
                    "天机阁.status": "一流势力"
                },
                "key_points": ["势力成型", "情报网完善", "拥有战将"]
            },
            56: {
                "title": "第56章：苏沐雪的成长",
                "summary": "苏沐雪修为提升，因果净化能力更加纯熟。",
                "plot_updates": {
                    "苏沐雪.修为": "筑基期"
                },
                "key_points": ["女主成长", "能力深化", "独立战斗"]
            },
            57: {
                "title": "第57章：王铁柱的秘密",
                "summary": "王铁柱身世揭晓，他是上一代天机之子留下的保险。",
                "plot_updates": {
                    "王铁柱.秘密": "上一代天机之子之子"
                },
                "key_points": ["身世揭晓", "因果免疫真相", "重要伏笔回收"]
            },
            58: {
                "title": "第58章：魔教教主的邀请",
                "summary": "魔教教主邀请叶青云加入弑神者组织。",
                "plot_updates": {},
                "key_points": ["魔教邀请", "弑神者组织", "叶青云的抉择"]
            },
            59: {
                "title": "第59章：拒绝与结盟",
                "summary": "叶青云拒绝加入但提出结盟，共同对抗天道。",
                "plot_updates": {
                    "魔教.关系": "结盟"
                },
                "key_points": ["拒绝加入", "提出结盟", "共同目标"]
            },
            60: {
                "title": "第60章：天机乱象爆发",
                "summary": "天机乱象正式爆发，所有天机之子被强制卷入。",
                "plot_updates": {
                    "天机乱象.status": "爆发"
                },
                "key_points": ["天机乱象开始", "天机之子被卷入", "大战将起"]
            }
        }
        return outlines.get(chapter_num, {"title": f"第{chapter_num}章", "summary": "剧情继续发展", "key_points": []})
    
    # 第61-70章：天机乱象
    elif 61 <= chapter_num <= 70:
        outlines = {
            61: {
                "title": "第61章：被迫入局",
                "summary": "叶青云被天机乱象强制拉入秘境，面对其他天机之子。",
                "plot_updates": {},
                "key_points": ["进入秘境", "遇见其他天机之子", "被迫战斗"]
            },
            62: {
                "title": "第62章：天机之子的聚集",
                "summary": "各路天机之子齐聚秘境，局势复杂。",
                "plot_updates": {},
                "key_points": ["天机之子汇聚", "多方势力", "复杂局势"]
            },
            63: {
                "title": "第63章：第一个敌人",
                "summary": "叶青云遭遇第一个天机之子对手，展现智谋。",
                "plot_updates": {},
                "key_points": ["首次天机之子对决", "智斗取胜", "展示实力"]
            },
            64: {
                "title": "第64章：楚凌霄的猎杀",
                "summary": "楚凌霄开始猎杀其他天机之子，因果之眼发威。",
                "plot_updates": {
                    "楚凌霄.action": "猎杀天机之子"
                },
                "key_points": ["楚凌霄出击", "因果之眼威力", "残忍猎杀"]
            },
            65: {
                "title": "第65章：苏沐雪的净化",
                "summary": "苏沐雪的净化能力可以帮助被天道污染的天机之子。",
                "plot_updates": {},
                "key_points": ["净化能力用处", "拯救同伴", "女主作用关键"]
            },
            66: {
                "title": "第66章：王铁柱的体质",
                "summary": "王铁柱的因果免疫体质让他成为关键棋子。",
                "plot_updates": {},
                "key_points": ["因果免疫用处", "关键棋子", "打破僵局"]
            },
            67: {
                "title": "第67章：叶青云的布局",
                "summary": "叶青云暗中布局，利用因果线操控局面。",
                "plot_updates": {},
                "key_points": ["暗中布局", "因果线操控", "展示算力"]
            },
            68: {
                "title": "第68章：林逸的抉择",
                "summary": "林逸发现自己的身世——他是上一代天机之子的遗孤。",
                "plot_updates": {
                    "林逸.身世": "上一代天机之子遗孤"
                },
                "key_points": ["林逸身世", "父母被天道所杀", "立场转变"]
            },
            69: {
                "title": "第69章：林逸的背叛",
                "summary": "林逸选择帮助叶青云，背叛了魔教（虽然是卧底）。",
                "plot_updates": {
                    "林逸.立场": "帮助叶青云"
                },
                "key_points": ["林逸选择", "背叛魔教", "成为叶青云棋子"]
            },
            70: {
                "title": "第70章：魔教教主的真相",
                "summary": "魔教教主现身，揭示上一代天机之子对抗天道的完整历史。",
                "plot_updates": {
                    "魔教教主.identity": "上一代天机之子"
                },
                "key_points": ["教主现身", "完整历史", "更多真相"]
            }
        }
        return outlines.get(chapter_num, {"title": f"第{chapter_num}章", "summary": "剧情继续发展", "key_points": []})
    
    # 第71-80章：终极对决准备
    elif 71 <= chapter_num <= 80:
        outlines = {
            71: {
                "title": "第71章：因果逆转的准备",
                "summary": "叶青云开始准备因果逆转大阵，需要收集材料。",
                "plot_updates": {},
                "key_points": ["准备大阵", "收集材料", "困难重重"]
            },
            72: {
                "title": "第72章：楚凌霄的过去",
                "summary": "楚凌霄回忆过去，发现自己的师姐也是天机之子。",
                "plot_updates": {
                    "楚凌霄.师姐": "也是天机之子"
                },
                "key_points": ["师姐线索", "悲剧伏笔", "楚凌霄内心"]
            },
            73: {
                "title": "第73章：叶青云与楚凌霄的对话",
                "summary": "两人在秘境中相遇，展开哲学对话。",
                "plot_updates": {},
                "key_points": ["命运讨论", "理念碰撞", "惺惺相惜"]
            },
            74: {
                "title": "第74章：师姐的出现",
                "summary": "楚凌霄的师姐出现，但已被天道控制。",
                "plot_updates": {
                    "楚凌霄.师姐.status": "被天道控制"
                },
                "key_points": ["师姐现身", "被控制真相", "悲剧加深"]
            },
            75: {
                "title": "第75章：被迫动手",
                "summary": "楚凌霄被迫与师姐战斗，叶青云目睹这一切。",
                "plot_updates": {},
                "key_points": ["被迫战斗", "师姐被控制", "悲剧高潮"]
            },
            76: {
                "title": "第76章：第一百个天机之子",
                "summary": "楚凌霄杀死师姐——他的第一百个天机之子。",
                "plot_updates": {
                    "楚凌霄.击杀数": 100
                },
                "key_points": ["杀死师姐", "第一百个", "楚凌霄崩溃"]
            },
            77: {
                "title": "第77章：楚凌霄的崩溃",
                "summary": "楚凌霄杀死师姐后彻底崩溃，意识开始觉醒。",
                "plot_updates": {
                    "楚凌霄.status": "意识觉醒"
                },
                "key_points": ["意识觉醒", "看清真相", "内心崩塌"]
            },
            78: {
                "title": "第78章：天道的獠牙",
                "summary": "天道直接出手，展现真正力量。",
                "plot_updates": {
                    "天道.status": "直接出手"
                },
                "key_points": ["天道显现", "压倒性力量", "绝望氛围"]
            },
            79: {
                "title": "第79章：叶青云的计划",
                "summary": "叶青云揭示自己的完整计划——不是成为天道宿主，而是杀死天道。",
                "plot_updates": {
                    "叶青云.目标": "杀死天道"
                },
                "key_points": ["完整计划", "杀死天道", "震撼揭示"]
            },
            80: {
                "title": "第80章：最后的准备",
                "summary": "叶青云开始布置因果逆转大阵的最后准备。",
                "plot_updates": {},
                "key_points": ["最后准备", "大阵布置", "决战前夕"]
            }
        }
        return outlines.get(chapter_num, {"title": f"第{chapter_num}章", "summary": "剧情继续发展", "key_points": []})
    
    # 第81-90章：大决战
    elif 81 <= chapter_num <= 90:
        outlines = {
            81: {
                "title": "第81章：王铁柱的牺牲",
                "summary": "王铁柱跳入因果逆转大阵，用凡人之躯承受天道反噬。",
                "plot_updates": {
                    "王铁柱.status": "牺牲"
                },
                "key_points": ["王铁柱牺牲", "保护叶青云", "感人场面"]
            },
            82: {
                "title": "第82章：因果逆转",
                "summary": "因果逆转大阵启动，天道被反向追踪。",
                "plot_updates": {},
                "key_points": ["大阵启动", "天道被追踪", "关键时刻"]
            },
            83: {
                "title": "第83章：楚凌霄的觉悟",
                "summary": "楚凌霄恢复全部意识，决定帮助叶青云。",
                "plot_updates": {
                    "楚凌霄.status": "恢复意识，决定帮助叶青云"
                },
                "key_points": ["意识恢复", "决定帮助", "牺牲准备"]
            },
            84: {
                "title": "第84章：楚凌霄的自爆",
                "summary": "楚凌霄自爆金丹，用气运帮助叶青云封印天道。",
                "plot_updates": {
                    "楚凌霄.status": "自爆"
                },
                "key_points": ["自爆金丹", "气运贡献", "悲剧英雄"]
            },
            85: {
                "title": "第85章：天道的封印",
                "summary": "叶青云用三千年因果线封印天道。",
                "plot_updates": {
                    "天道.status": "被封印"
                },
                "key_points": ["封印天道", "因果线束缚", "终极一战"]
            },
            86: {
                "title": "第86章：胜利的代价",
                "summary": "叶青云的意识被困在因果之网中，成为新的天道。",
                "plot_updates": {
                    "叶青云.status": "成为新的天道守护者"
                },
                "key_points": ["代价付出", "意识被困", "新天道诞生"]
            },
            87: {
                "title": "第87章：天机乱象的结束",
                "summary": "所有天机之子重获自由，天机乱象结束。",
                "plot_updates": {
                    "天机乱象.status": "结束"
                },
                "key_points": ["乱象结束", "天机之子自由", "新时代开始"]
            },
            88: {
                "title": "第88章：苏沐雪的等待",
                "summary": "苏沐雪在因果之网外等待叶青云。",
                "plot_updates": {},
                "key_points": ["苏沐雪等待", "因果之网外", "守望"]
            },
            89: {
                "title": "第89章：三千年之约",
                "summary": "叶青云承诺三千年后会回来找苏沐雪。",
                "plot_updates": {},
                "key_points": ["三千年约定", "叶青云的承诺", "情感高潮"]
            },
            90: {
                "title": "第90章：新的开始",
                "summary": "叶青云以新天道的身份开始守护世界，苏沐雪开始等待。",
                "plot_updates": {},
                "key_points": ["新天道", "守护世界", "等待开始"]
            }
        }
        return outlines.get(chapter_num, {"title": f"第{chapter_num}章", "summary": "剧情继续发展", "key_points": []})
    
    # 第91-100章：尾声与结局
    elif 91 <= chapter_num <= 100:
        outlines = {
            91: {
                "title": "第91章：天机阁的未来",
                "summary": "天机阁在新世界中继续发展，成为守护者组织。",
                "plot_updates": {},
                "key_points": ["天机阁延续", "守护者组织", "传承"]
            },
            92: {
                "title": "第92章：王铁柱的遗产",
                "summary": "王铁柱牺牲后，他的三个老婆继承他的意志。",
                "plot_updates": {
                    "王铁柱.遗产": "三个老婆继承意志"
                },
                "key_points": ["三个老婆", "继承意志", "搞笑番外"]
            },
            93: {
                "title": "第93章：林逸的救赎",
                "summary": "林逸找到自己的救赎方式，为叶青云守护落凤城。",
                "plot_updates": {},
                "key_points": ["林逸救赎", "守护落凤城", "反派洗白"]
            },
            94: {
                "title": "第94章：楚凌霄的遗产",
                "summary": "楚凌霄的因果之眼成为叶青云的一部分。",
                "plot_updates": {
                    "楚凌霄.遗产": "因果之眼被叶青云继承"
                },
                "key_points": ["因果之眼传承", "楚凌霄遗产", "永恒"]
            },
            95: {
                "title": "第95章：因果之网中的叶青云",
                "summary": "叶青云在因果之网中的生活和新职责。",
                "plot_updates": {},
                "key_points": ["新天道生活", "守护职责", "孤独"]
            },
            96: {
                "title": "第96章：苏沐雪的修炼",
                "summary": "苏沐雪开始刻苦修炼，期待与叶青云重逢。",
                "plot_updates": {},
                "key_points": ["女主修炼", "期待重逢", "希望"]
            },
            97: {
                "title": "第97章：一千年后",
                "summary": "一千年过去，世界发生巨大变化。",
                "plot_updates": {
                    "时间跳跃": "一千年"
                },
                "key_points": ["时间跳跃", "世界变化", "沧海桑田"]
            },
            98: {
                "title": "第98章：两千年后",
                "summary": "两千年后，苏沐雪已是绝世强者。",
                "plot_updates": {
                    "时间跳跃": "两千年"
                },
                "key_points": ["女主变强", "依然等待", "坚定"]
            },
            99: {
                "title": "第99章：重逢",
                "summary": "三千年之约到来，叶青云与苏沐雪重逢。",
                "plot_updates": {},
                "key_points": ["重逢时刻", "三千年等待", "感人"]
            },
            100: {
                "title": "第100章：新的传说",
                "summary": "叶青云从天道中解脱，与苏沐雪一同离开，开始新生活。开放式结局。",
                "plot_updates": {
                    "结局": "开放式结局"
                },
                "key_points": ["叶青云解脱", "两人离开", "新的旅程", "完结"]
            }
        }
        return outlines.get(chapter_num, {"title": f"第{chapter_num}章", "summary": "剧情继续发展", "key_points": []})
    
    else:
        return {"title": f"第{chapter_num}章", "summary": "剧情继续发展", "key_points": []}

def generate_chapter(chapter_num, state, config):
    """生成单章内容"""
    print(f"\n" + "="*60)
    print(f"📝 生成第{chapter_num}章")
    print("="*60)
    
    outline = get_chapter_outline(chapter_num, state, config)
    state_json = json.dumps(state, ensure_ascii=False, indent=2)
    config_rules = json.dumps(config, ensure_ascii=False, indent=2)
    
    prompt = f"""请根据以下信息生成《天机道主》第{chapter_num}章。

## 章节大纲
标题：{outline['title']}
摘要：{outline['summary']}
关键情节点：{', '.join(outline.get('key_points', []))}

## 当前剧情状态
```json
{state_json}
```

## NWACS优化配置规则
```json
{config_rules}
```

## 写作要求
1. **严格遵循优化配置**：
   - 因果推演能力必须有消耗和代价
   - 人物情感发展必须有合理铺垫
   - 女主角必须有独立行动和决策
   - 配角必须有复杂动机
   - 剧情节奏必须张弛有度

2. **章节要求**：
   - 字数：2000-3000字
   - 每章结尾留钩子
   - 符合整体风格（热血、悬疑、治愈、搞笑）
   - 智斗为主，爽点密集

3. **必须包含**：
   - 本章核心剧情
   - 与前后章节的衔接
   - 符合人物性格的行为和对话
   - 适当的情感互动

请开始撰写第{chapter_num}章。"""

    system_prompt = """你是一位顶尖的玄幻小说作家，擅长写长篇连载小说。
写作特点：
1. 严格遵循能力限制（因果推演有代价）
2. 人物塑造有深度
3. 情感发展自然合理
4. 剧情节奏张弛有度
5. 每章结尾留钩子"""

    result = call_deepseek(prompt, system_prompt, temperature=0.85)
    
    if result:
        # 更新剧情状态
        if 'plot_updates' in outline:
            for key, value in outline['plot_updates'].items():
                if '.' in key:
                    parts = key.split('.')
                    if parts[0] in state.get('character_states', {}):
                        state['character_states'][parts[0]][parts[1]] = value
                else:
                    state[key] = value
        
        state['current_chapter'] = chapter_num
        
        # 保存章节
        save_chapter(chapter_num, result)
        
        # 保存更新后的状态
        save_plot_state(state)
        
        print(f"   ✅ 第{chapter_num}章完成")
        return result
    else:
        print(f"   ❌ 第{chapter_num}章失败")
        return None

def main():
    print("="*60)
    print("📖 DeepSeek + NWACS 逐章生成第31-100章")
    print("="*60)
    
    # 加载配置和状态
    config = load_optimized_config()
    state = load_plot_state()
    
    start_chapter = state['current_chapter'] + 1
    end_chapter = 100
    
    print(f"\n当前状态：第{state['current_chapter']}章")
    print(f"计划生成：第{start_chapter}-{end_chapter}章")
    print(f"总计：{end_chapter - start_chapter + 1}章")
    
    # 生成所有章节
    all_chapters = []
    for chapter_num in range(start_chapter, end_chapter + 1):
        result = generate_chapter(chapter_num, state, config)
        if result:
            all_chapters.append((chapter_num, result))
        
        # 每5章输出一次进度
        if chapter_num % 5 == 0:
            print(f"\n   📊 进度：已完成第{chapter_num}章")
    
    # 生成完整章节集
    if all_chapters:
        output_file = "novel/《天机道主》第31-100章.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("《天机道主》第31-100章\n")
            f.write("="*60 + "\n")
            f.write(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*60 + "\n\n")
            
            for chapter_num, content in all_chapters:
                f.write(f"\n{'='*60}\n")
                f.write(f"第{chapter_num}章\n")
                f.write(f"{'='*60}\n\n")
                f.write(content)
                f.write("\n\n")
        
        print(f"\n   💾 完整章节集已保存：{output_file}")
    
    print("\n" + "="*60)
    print("🎉 全部完成！")
    print("="*60)
    print(f"\n共生成 {len(all_chapters)} 章")
    print(f"当前状态：第{state['current_chapter']}章")
    print(f"\n文件已保存至 novel/ 目录")

if __name__ == "__main__":
    main()