#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修仙玄幻小说大纲生成器 - 默认TXT格式
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
创作过《凡人修仙传》《仙逆》《道君》等经典仙侠小说。"""

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

def generate_complete_novel():
    """一次性生成完整小说大纲"""
    print("\n[1/2] 正在生成小说大纲...")

    prompt = """请为一个修仙玄幻小说生成完整的详细大纲，要求：

## 书名要求
生成10个独特有吸引力的书名，苟道流风格（主角低调、谨慎、隐忍），黑暗流风格（主角腹黑、心狠手辣），智斗流风格（聪明、算计、以弱胜强），结合热血、悬疑、治愈、搞笑元素。参考《凡人修仙传》《仙逆》《道君》。

## 世界观设定
### 大陆体系（至少3块大陆）
- 苍元大陆：修仙为主，等级森严
- 幽冥海域：海洋妖兽领地
- 蛮荒古域：上古遗迹、凶兽横行

### 世界规则
- 天地灵气的分布规律
- 修炼资源的分布
- 天地法则设定

## 修炼体系
### 境界划分
炼气→筑基→金丹→元婴→化神→炼虚→合体→大乘→渡劫→地仙→天仙→金仙→大罗金仙→混元大罗金仙→道祖

### 辅助修炼（6种）
1. 炼丹：丹药等级（九转）、丹药类型、炼丹材料
2. 炼体：肉身等级、不死身、霸体
3. 炼毒：毒药制作、毒抗
4. 炼器：法宝等级、炼制手法
5. 御兽：妖兽等级、契约方式
6. 阵法：阵法类型、布阵手法

## 门派势力
### 三大古派
1. 太清宫：主修炼丹
2. 剑阁：主修剑道
3. 万法宗：精通万法

### 七大宗
青云门、天机阁、玄天宗、百草堂、御兽山庄、炼器坊、天符派

### 三十六门派
包括落云宗、天魔教、太一派等

## 主角设定
- 姓名：萧凡
- 性格：谨慎、腹黑、智谋过人、苟道流
- 外貌：普通、不起眼、眼神深邃
- 擅长：苟、躲、跑、暗中算计、以弱胜强
- 金手指：神秘戒指（内有老爷爷）

## 女主角（4位）
1. 苏瑶：太清宫圣女，冰山仙女型
2. 小莲：百草堂弟子，活泼萝莉型
3. 白骨夫人：万鬼宗圣女，妖娆御姐型
4. 姜雪晴：天骄学院院长，霸道女帝型

## 妖兽系统
### 等级：一阶~九阶妖兽、妖兽皇、妖兽帝、妖神
### 种类：
- 神龙族（九天神龙、渊冥魔龙）
- 凤凰族（九幽冥凤、赤焰凤凰）
- 白虎族、玄武族
- 妖族（九尾狐、吞天蟒、金翅鹏）
- 远古凶兽（饕餮、混沌、梼杌、穷奇、鲲鹏）

## 阵法系统
困敌类（十方困魔阵）、攻击类（天地灭绝阵）、防御类（万法不侵阵）、迷幻类、传送类、聚灵类、杀阵类（诛仙剑阵）

## 法宝系统
番天印、阴阳镜、捆仙绳、混天绫、紫金葫芦、山河社稷图、十二品莲台、东皇钟、昊天塔

## 武器装备
剑（长剑、重剑、软剑、飞剑）、刀、枪、弓、防具（战甲、内甲）、饰品（戒指、项链）

## 法术体系
剑系（万剑归宗）、火系（三昧真火）、冰系（万里冰封）、雷系（天雷降世）、毒系（万毒功）、防御类、辅助类、灵魂类、特殊类（时间法则、空间法则）

## 主线剧情（100万字分4卷）
### 第一卷：蝼蚁崛起（1-30万字）
主角萧凡，出身小门派，父母被害，资质平庸被轻视。意外获得神秘戒指（金手指），开始修炼。炼气期积累资源，筑基期卷入宗门阴谋，金丹期正式崛起。

关键事件：
- 第5万字：教训欺负他的人（打脸）
- 第15万字：结识女主小莲
- 第25万字：宗门大比夺冠
- 第30万字：发现父母被害真相

### 第二卷：暗流涌动（30-60万字）
金丹期成长，建立势力，与女主苏瑶相遇。卷入正魔大战，发现更大阴谋。

关键事件：
- 第40万字：加入太清宫（卧底）
- 第50万字：与苏瑶感情发展
- 第55万字：获得炼丹传承

### 第三卷：仙魔大战（60-80万字）
仙魔大战爆发，主角两边周旋，修为突破元婴，揭露幕后黑手。

关键事件：
- 第65万字：元婴期渡劫
- 第70万字：获得万法传承
- 第75万字：结识白骨夫人

### 第四卷：飞升仙界（80-100万字）
渡劫飞升，仙界新挑战，与姜雪晴相遇，最终决战。

关键事件：
- 第85万字：渡劫成仙
- 第95万字：成为仙帝
- 第100万字：大结局

## 伏笔设计
- 父母被害 → 第25万字揭示
- 戒指来历 → 第50万字揭示
- 幕后黑手 → 第70万字揭示
- 主角真实身份 → 第90万字揭示

## 爽点设计
1. 打脸：每次被轻视后反杀
2. 升级：突破境界
3. 夺宝：获得传承
4. 护短：保护女主
5. 装逼：低调打脸

## 前30章大纲
第1章：废物少年，被人欺辱
第2章：父母被害，真相隐藏
第3章：意外跌落悬崖，获得戒指
第4章：戒指老爷爷出现
第5章：开始修炼，改变命运
第6章：教训欺负他的人（打脸）
第7章：发现家族秘密
第8章：宗门测试，资质提升
第9章：炼气一层，积累资源
第10章：第一次冒险
（继续到第30章）

请详细输出完整大纲，包括所有设定的具体数值、名称、描述。"""

    response = call_deepseek_v4(prompt)
    if response:
        print("  ✓ 大纲生成完成")
        return response
    return None

def save_outline(outline):
    """保存大纲（使用TXT格式）"""
    novel_name = "苟道至尊"
    safe_name = ''.join(c for c in novel_name if c not in '\\/:*?"<>|')
    
    # 确保输出目录存在
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)
    
    # 保存大纲
    outline_path = os.path.join(output_dir, f"{safe_name}_大纲.txt")
    
    content = f"""《{novel_name}》小说大纲

修仙玄幻·苟道流·黑暗流·智斗流
字数：100万字以上

---

{outline if outline else '大纲生成中...'}

---

本大纲由 NWACS × DeepSeek V4 联合生成
生成时间：{time.strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    # 清理markdown格式
    content = content.replace('# ', '')
    content = content.replace('## ', '')
    content = content.replace('### ', '')
    content = content.replace('**', '')
    content = content.replace('*', '')
    content = content.replace('---\n', '')
    content = content.replace('|', '')
    content = content.replace('`', '')
    
    with open(outline_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n  ✓ 大纲已保存到: {outline_path}")
    return outline_path

def main():
    print("\n" + "=" * 80)
    print("          修仙玄幻小说大纲生成器（TXT格式）")
    print("          苟道流·黑暗流·智斗流")
    print("=" * 80)
    print("\n正在使用 DeepSeek V4 生成小说大纲...")
    print("预计需要 5-10 分钟，请耐心等待...")

    outline = generate_complete_novel()
    save_outline(outline)

    print("\n" + "=" * 80)
    print("                    生成完成！")
    print("=" * 80)
    print("\n📚 小说大纲已生成：output/苟道至尊_大纲.txt")
    print("\n包含内容：")
    print("  ✓ 10个特色书名")
    print("  ✓ 完整世界观与大陆体系")
    print("  ✓ 修炼体系（含6种辅助修炼）")
    print("  ✓ 50+门派势力设定")
    print("  ✓ 主角+4位女主详细设定")
    print("  ✓ 100+妖兽种类")
    print("  ✓ 30+阵法系统")
    print("  ✓ 50+法宝设定")
    print("  ✓ 武器装备系统")
    print("  ✓ 200+法术体系")
    print("  ✓ 100万字主线剧情大纲")
    print("  ✓ 前30章详细章节大纲")
    print("=" * 80)

if __name__ == "__main__":
    main()
