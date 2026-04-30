#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重新生成前10章 - 优化版
✨ 画面影视感 + 读者带入感
"""

import os
import sys
import json
import urllib.request
import urllib.error
import time
import threading
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

# ============================================================================
# 配置模块
# ============================================================================

def load_config():
    config = {}
    if os.path.exists('config.json'):
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
    return config

# ============================================================================
# 写作手法优化
# ============================================================================

WRITING_TIPS = """【画面影视感】
- 镜头语言：远景（天地）→中景（人物）→特写（细节）
- 多感官描写：视觉、听觉、嗅觉、触觉、味觉
- 动态描写：不要静态画面，要写出流动感
- 色彩运用：红、黑、金、紫等色彩营造氛围

【读者带入感】
- POV视角：深入主角内心，细腻的心理活动
- 对话风格：每个角色说话要有自己的特点
- 情感共鸣：让读者感同身受

【节奏控制】
- 每章约3000字
- 300字一小爽点，1000字一大爽点
- 每章结尾必须留悬念钩子
"""

def get_enhanced_system_prompt():
    return f"""你是一位顶尖玄幻网文大神，创作过《凡人修仙传》《仙逆》《遮天》等名著。

【核心写作原则】
1. 画面影视感：
   - 用镜头语言：远景（天地）→中景（人物）→特写（细节）
   - 多感官描写：视觉、听觉、嗅觉、触觉、味觉
   - 动态画面：写出流动感，不要静态描写
   - 色彩运用：用红、黑、金、紫等色营造氛围

2. 读者带入感：
   - POV视角：深入主角内心，细腻的心理活动
   - 对话风格：每个角色说话要有自己的特点
   - 情感共鸣：让读者感同身受，喜怒哀乐都能传递
   - 细节真实：微表情、小动作、场景变化都要写

3. 节奏控制：
   - 300字小爽点，1000字大爽点
   - 每章结尾必须留悬念钩子
   - 张弛有度：战斗场面和日常场景交替

【写作要求】
每章约3000字，不水文，每句话都要有信息量。
{WRITING_TIPS}
"""

# ============================================================================
# API调用（优化版）
# ============================================================================

def call_deepseek_v4(prompt, system_prompt=None, max_tokens=8000, timeout=180):
    """调用DeepSeek V4 API（优化版）"""
    config = load_config()
    if not config.get('api_key'):
        print("❌ 错误: API Key未配置！")
        return None

    if not system_prompt:
        system_prompt = get_enhanced_system_prompt()

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
        'max_tokens': max_tokens
    }

    print(f"\n⏳ 正在调用DeepSeek V4...")
    print(f"   预计等待时间: {timeout/60:.1f}分钟")
    print(f"   正在生成内容，请稍候...")

    stop_spinner = threading.Event()
    spinner_thread = threading.Thread(target=spinner_animation, args=(stop_spinner,))
    spinner_thread.daemon = True
    spinner_thread.start()

    try:
        req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method='POST')

        with urllib.request.urlopen(req, timeout=timeout) as response:
            stop_spinner.set()
            result = json.loads(response.read().decode('utf-8'))
            print(f"✅ API调用成功！")
            return result['choices'][0]['message']['content']

    except urllib.error.HTTPError as e:
        stop_spinner.set()
        print(f"❌ HTTP错误: {e.code} - {e.reason}")
        if e.code == 429:
            print("   ⚠️  请求过于频繁，请稍后重试")
        elif e.code == 402:
            print("   ⚠️  API余额不足，请充值")
        return None
    except Exception as e:
        stop_spinner.set()
        print(f"❌ API调用失败: {e}")
        return None

def spinner_animation(stop_event):
    spinner = ['|', '/', '-', '\\']
    idx = 0
    while not stop_event.is_set():
        sys.stdout.write(f"\r   {spinner[idx]}")
        sys.stdout.flush()
        idx = (idx + 1) % 4
        time.sleep(0.2)

# ============================================================================
# 保存文件
# ============================================================================

def save_to_txt(novel_name, content, chapter_range=""):
    safe_name = ''.join(c for c in novel_name if c not in '\\/:*?"<>|')
    
    if chapter_range:
        filename = f"{safe_name}_{chapter_range}.txt"
    else:
        filename = f"{safe_name}.txt"
    
    os.makedirs('output', exist_ok=True)
    filepath = os.path.join('output', filename)
    
    header = f"""{novel_name}
{'=' * 60}
修仙玄幻·苟道流·黑暗流·智斗流
生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'=' * 60}

"""
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(header)
        f.write(content)
        f.write(f"\n\n{'=' * 60}\n")
        f.write("本小说由 NWACS × DeepSeek V4 联合创作\n")
        f.write("✨ 画面影视感 + 读者带入感优化版\n")
    
    print(f"\n✅ 已保存: {filepath}")
    return filepath

# ============================================================================
# 生成前10章
# ============================================================================

def generate_first_10_chapters():
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║           NWACS × DeepSeek V4                                ║
║           重新生成前10章 - 优化版                             ║
║           ✨ 画面影视感 + 读者带入感                        ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    prompt = """请为小说《长生仙逆：从苟道毒修开始》创作前10章完整内容。

【主角设定】
- 林玄：炼气期修士，在废丹窑监守
- 金手指：融合天道碎片，成为"命运之外的人"
- 性格：谨慎小心，苟道流，不暴露底牌

【画面影视感】
- 镜头语言：远景（天地）→中景（人物）→特写（细节）
- 多感官描写：视觉、听觉、嗅觉、触觉、味觉都要有
- 动态描写：不要静态画面，要写出流动感
- 色彩运用：用红、黑、金、紫等色彩营造氛围

【读者带入感】
- POV视角：深入林玄内心，细腻的心理活动
- 对话风格：每个角色说话要有自己的特点
- 情感共鸣：让读者感同身受

【节奏控制】
- 每章约3000字
- 300字一小爽点，1000字一大爽点
- 每章结尾必须留悬念钩子

请创作前10章：

第1章：毒窟少年，天道碎片
- 林玄在废丹窑监守三年
- 在废弃丹药中发现黑色碎片
- 碎片融合，成为"命运之外的人"
- 暗中观察宗门黑暗

第2章：苟道十戒，毒丹初炼
- 林玄制定"苟道十戒"
- 在废丹窑中学习炼丹
- 利用废弃丹药炼出"杂毒丹"
- 天道碎片能力：看到丹药气运
- 炼制"隐气丹"隐藏修为

第3章：杂毒丹成，鱼目混珠
- 用杂毒丹放倒废丹窑看守
- 制造意外中毒的假象
- 在废丹窑深处发现密室
- 密室中是上任长老的笔记
- 发现宗门与魔道勾结，贩卖凡人

第4章：隐气丹成，低调炼气
- 成功炼制隐气丹
- 修为悄悄提升到炼气三层
- 对外只显示炼气一层
- 天道碎片另一能力：看到他人杀运
- 发现王霸身上环绕浓厚杀运

第5章：王霸寻事，毒针反杀
- 王霸带人堵林玄
- 林玄早有准备，布下毒雾迷阵
- 用无影毒针反杀王霸
- 但留活口，让王霸"意外"摔下山崖成傻子
- 制造完美不在场证明
- 从王霸身上搜出与魔道勾结的证据

第6章：长老查案，金蝉脱壳
- 执法长老调查王霸案
- 林玄早有准备，把嫌疑引向另一个仇人
- 用移魂毒香让执法长老产生幻觉
- 成功金蝉脱壳
- 执法长老把锅扣给魔道奸细
- 林玄获得王霸的储物袋，搜刮战利品

第7章：密信解密，长生初现
- 密信中提到"长生会"和"药园计划"
- 原来凡人国度是仙门圈养的"药园"
- 每百年收割一次炼制血丹
- 林玄发现自己家乡是下一个目标
- 天道碎片预警：三个月后家乡将被收割
- 必须尽快提升实力阻止灾难

第8章：秘境开启，浑水摸鱼
- 宗门小秘境"毒龙谷"开启
- 林玄报名参加，寻找机缘
- 暗中在秘境入口布下毒阵
- 遇到其他宗门弟子，表面客气暗中较量
- 天道碎片能力：看到秘境中的气运点
- 找到一枚"毒龙丹"，上古毒修的遗产

第9章：毒龙苏醒，血战求生
- 上古毒龙残魂苏醒
- 众人惊慌失措，死伤惨重
- 林玄苟在角落，暗中观察，准备逃跑
- 发现毒龙残魂虚弱，是绝佳机缘
- 用天道碎片能力沟通毒龙残魂
- 毒龙残魂发现林玄是"命运之外的人"，愿意传功
- 林玄获得"毒龙真解"
- 宗门高层发现秘境异常，要下来查探

第10章：传承到手，暗中离谷
- 林玄获得毒龙传承，修为暴增到炼气七层
- 但继续藏拙，对外只显示炼气三层
- 用毒丹把受伤的宗门弟子"救"醒
- 制造"林玄舍命救人"的假象
- 获得宗门奖励，身份提升
- 暗中布下毒阵，消除自己在秘境中的痕迹
- 离开毒龙谷，准备回家乡阻止灾难
- 在谷口遇到神秘女子苏清，她好像能看穿林玄的伪装

请开始创作前10章，要求画面影视感+读者带入感！"""
    
    print("\n📖 正在生成前10章内容...")
    print("   (约30000字，每章3000字)")
    
    content = call_deepseek_v4(prompt, max_tokens=8000, timeout=180)
    if content:
        novel_name = "长生仙逆从苟道毒修开始"
        save_to_txt(novel_name, content, "1-10章(优化版)")
        print("\n✅ 前10章优化版生成完成！")
        print("   包含画面影视感 + 读者带入感优化")
        return content
    return None

if __name__ == "__main__":
    generate_first_10_chapters()
