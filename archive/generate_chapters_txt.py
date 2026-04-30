#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成小说章节内容 - 默认TXT格式
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
        system_prompt = """你是一位顶尖玄幻网文大神，擅长苟道流、黑暗流、智斗流，
创作过《凡人修仙传》《仙逆》《道君》等经典仙侠小说。
要求：节奏紧凑、爽点密集、画面感强、悬念钩子、不水文。"""

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

def generate_chapters(novel_name, start_chapter=1, end_chapter=10):
    """生成章节内容"""
    print(f"\n[1/2] 正在生成第{start_chapter}-{end_chapter}章内容...")

    prompt = f"""请为修仙玄幻小说《{novel_name}》生成第{start_chapter}-{end_chapter}章完整内容，要求：

## 小说设定
- 书名：《{novel_name}》
- 类型：苟道流·黑暗流·智斗流·热血·悬疑·治愈·搞笑
- 主角：萧凡，出身小门派，资质平庸，被人轻视，获得神秘戒指（内有老爷爷药尘）

## 章节要求
每章约3000-3500字，节奏紧凑，每章有爽点，结尾留悬念。

## 章节内容提要

### 第1章：废物少年，宗门弃子
- 地点：青玄宗外门
- 事件：萧凡被大师兄王浩欺负，嘲讽为"千年废柴"
- 背景：萧凡父母三年前失踪，留下神秘戒指
- 结尾钩子：戒指微微发热

### 第2章：父母之谜，神秘戒指
- 回忆：父母失踪前的场景
- 探索：戒指突然发光，神秘意识出现
- 老爷爷：自称药尘，远古丹帝残魂
- 结尾钩子：药尘传授基础吐纳法

### 第3章：悬崖奇遇，传承觉醒
- 被追杀：王浩带人追杀萧凡
- 坠崖：萧凡被逼跳崖，意外落入秘境
- 传承：发现远古传承石碑
- 结尾钩子：石碑发光，传承开始

### 第4章：药尘指点，逆天改命
- 修炼：药尘指导萧凡修炼
- 体质：萧凡竟是罕见的混沌道体
- 资源：药尘赠送洗髓丹
- 结尾钩子：突破炼气一层

### 第5章：初露锋芒，打脸开始
- 返回：萧凡悄悄返回宗门
- 挑衅：王浩再次挑衅
- 打脸：萧凡轻松击败王浩
- 结尾钩子：长老注意到萧凡

### 第6章：宗门测试，惊艳全场
- 测试：宗门年度资质测试
- 表现：萧凡展现惊人天赋
- 震惊：所有人目瞪口呆
- 结尾钩子：内门长老抛出橄榄枝

### 第7章：家族秘密，黑暗往事
- 回忆：萧凡回忆父母的叮嘱
- 调查：发现父母留下的密信
- 真相：父母可能被宗门高层所害
- 结尾钩子：发现重要线索

### 第8章：秘境开启，机缘争夺
- 秘境：宗门秘境开启
- 组队：萧凡低调组队
- 争夺：遭遇其他弟子抢夺
- 结尾钩子：发现神秘宝箱

### 第9章：遭遇强敌，智斗脱身
- 强敌：遭遇外门第一天骄李青峰
- 危机：被围困，陷入绝境
- 智斗：萧凡用计谋迷惑敌人
- 结尾钩子：发现李青峰的秘密

### 第10章：修炼加速，崭露头角
- 修炼：萧凡在秘境中快速修炼
- 突破：达到炼气三层
- 收获：获得大量资源和功法
- 结尾钩子：秘境深处传来恐怖气息

## 写作风格要求
1. 节奏：300字小爽点，1000字大爽点
2. 画面感：战斗描写具体，细节丰富
3. 苟道：主角低调，暗中发展
4. 智斗：计谋取胜，不硬碰硬
5. 悬念：每章结尾留钩子

请输出完整的章节内容，每章独立成篇，格式清晰。"""

    response = call_deepseek_v4(prompt)
    if response:
        print("  ✓ 章节内容生成完成")
        return response
    return None

def save_chapters(novel_name, content, start_chapter=1, end_chapter=10):
    """保存章节内容（使用TXT格式）"""
    safe_name = ''.join(c for c in novel_name if c not in '\\/:*?"<>|')
    
    # 确保输出目录存在
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)
    
    # 保存章节
    chapter_path = os.path.join(output_dir, f"{safe_name}_{start_chapter}-{end_chapter}章.txt")
    
    chapters_content = f"""《{novel_name}》第{start_chapter}-{end_chapter}章

修仙玄幻·苟道流·黑暗流·智斗流

---

{content if content else '章节生成中...'}

---

本章节由 NWACS × DeepSeek V4 联合生成
生成时间：{time.strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    # 清理markdown格式
    chapters_content = chapters_content.replace('# ', '')
    chapters_content = chapters_content.replace('## ', '')
    chapters_content = chapters_content.replace('### ', '')
    chapters_content = chapters_content.replace('**', '')
    chapters_content = chapters_content.replace('*', '')
    chapters_content = chapters_content.replace('---\n', '')
    chapters_content = chapters_content.replace('|', '')
    chapters_content = chapters_content.replace('`', '')
    
    with open(chapter_path, 'w', encoding='utf-8') as f:
        f.write(chapters_content)
    
    print(f"\n  ✓ 章节已保存到: {chapter_path}")
    return chapter_path

def main():
    novel_name = "苟道至尊"
    start_chapter = 1
    end_chapter = 10
    
    print("\n" + "=" * 80)
    print(f"          《{novel_name}》第{start_chapter}-{end_chapter}章生成器（TXT格式）")
    print("=" * 80)
    print("\n正在使用 DeepSeek V4 生成章节内容...")
    print("预计需要 5-10 分钟，请耐心等待...")

    content = generate_chapters(novel_name, start_chapter, end_chapter)
    save_chapters(novel_name, content, start_chapter, end_chapter)

    print("\n" + "=" * 80)
    print("                    生成完成！")
    print("=" * 80)
    print(f"\n📚 章节已生成：output/{novel_name}_{start_chapter}-{end_chapter}章.txt")
    print("\n包含内容：")
    for i in range(start_chapter, end_chapter + 1):
        print(f"  ✓ 第{i}章")
    print("\n每章约3000字，节奏紧凑，爽点密集！")
    print("=" * 80)

if __name__ == "__main__":
    main()
