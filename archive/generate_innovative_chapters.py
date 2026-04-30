#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基于创新设定生成小说章节
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
        system_prompt = """你是一位顶尖玄幻网文大神，擅长创新设定、反套路剧情、轻松搞笑风格。
你的小说新颖独特，主角运气爆棚，智斗为主，笑点密集。"""

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
        'temperature': 0.85,
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

def generate_chapters():
    """生成前10章内容"""
    print("\n[1/2] 正在生成创新小说前10章...")

    prompt = """请为创新玄幻小说《气运之王》生成前10章完整内容，要求：

## 小说设定
- 书名：《气运之王》
- 类型：反套路·轻松搞笑·智斗流·气运修炼
- 主角：陈凡，平民出身，杂货铺老板儿子，锦鲤体质（运气爆棚）
- 金手指：锦鲤体质，走路捡灵石，买包子吃出传承

## 核心设定
- 世界由气运驱动，每个人都有命运线
- 修炼体系：聚气→凝运→化运→转运→造运→承运→掌运→天运→帝运
- 女主1：苏小厨，吃货少女，食神之体
- 女主2：林玄机，天机阁少阁主，能看命运线
- 女主3：白玲珑，九尾狐族公主

## 章节要求
每章约3000字，轻松搞笑，智斗为主，不虐主，爽点密集。

## 章节内容

### 第1章：锦鲤少年，买包子吃出传承
- 陈凡去买包子，吃出一枚古朴玉佩
- 玉佩融入体内，获得上古传承
- 老板以为他偷东西，结果他随手掏出更多灵石
- 结尾：玉佩发出微光，提示有奇遇

### 第2章：柴房寻宝，气运爆棚
- 帮父亲整理柴房，发现隐藏的密室
- 密室里全是修炼资源
- 随便拿个破罐子都是上古法器
- 结尾：父亲惊讶地看着陈凡

### 第3章：河边奇遇，锦鲤认主
- 去河边洗衣服，遇到一条会说话的锦鲤
- 锦鲤说他气运逆天，非要认他为主
- 锦鲤告诉他修炼方法
- 结尾：陈凡开始修炼

### 第4章：酒楼风波，美食结缘
- 去酒楼吃饭，遇到美女厨师苏小厨
- 苏小厨做的菜能提升修为
- 陈凡指出菜品缺陷，苏小厨震惊
- 结尾：苏小厨邀请陈凡合作

### 第5章：算卦少女，命运之线
- 街上遇到神秘少女林玄机
- 林玄机说他的命运线与众不同
- 劫运教的人出现，想抢夺陈凡的气运
- 结尾：林玄机出手相救

### 第6章：初次修炼，气运突破
- 在锦鲤指导下修炼
- 直接从聚气一层突破到凝运初期
- 引动天地异象，惊动全城
- 结尾：宗门来人想收他为徒

### 第7章：宗门测试，轻松碾压
- 参加青云盟的入门测试
- 测试运气，陈凡抽到最高难度却轻松通过
- 其他天才一脸懵逼
- 结尾：获得第一名，奖励丰厚

### 第8章：妖族公主，傲娇驾到
- 九尾狐族公主白玲珑突然出现
- 想借陈凡的气运修炼
- 陈凡各种拒绝，白玲珑各种纠缠
- 结尾：白玲珑决定赖着不走

### 第9章：秘境探险，满载而归
- 进入宗门秘境
- 别人遇到危险，陈凡遇到宝藏
- 轻松获得各种珍稀资源
- 结尾：发现秘境深处的秘密

### 第10章：劫运来袭，气运对抗
- 劫运教正式出手
- 想用厄运术对付陈凡
- 结果被陈凡的锦鲤体质反弹
- 结尾：陈凡获得劫运教的秘密情报

## 写作风格
1. 轻松搞笑，笑点密集
2. 主角靠运气和智慧解决问题
3. 不虐主，爽点多多
4. 每章结尾留悬念

请输出完整章节内容。"""

    response = call_deepseek_v4(prompt)
    if response:
        print("  ✓ 章节生成完成")
        return response
    return None

def save_chapters(content):
    """保存章节内容"""
    novel_name = "气运之王"
    safe_name = ''.join(c for c in novel_name if c not in '\\/:*?"<>|')
    
    os.makedirs('output', exist_ok=True)
    chapter_path = os.path.join('output', f"{safe_name}_前10章.txt")
    
    chapters_content = f"""《{novel_name}》前10章

【创新玄幻·反套路·轻松搞笑】

---

{content if content else '章节生成中...'}

---

本章节由 NWACS × DeepSeek V4 联合生成
生成时间：{time.strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    # 清理格式
    chapters_content = chapters_content.replace('# ', '')
    chapters_content = chapters_content.replace('## ', '')
    chapters_content = chapters_content.replace('**', '')
    chapters_content = chapters_content.replace('*', '')
    
    with open(chapter_path, 'w', encoding='utf-8') as f:
        f.write(chapters_content)
    
    print(f"\n  ✓ 章节已保存到: {chapter_path}")
    return chapter_path

def main():
    print("\n" + "=" * 80)
    print("          《气运之王》前10章生成器")
    print("          创新反套路设定")
    print("=" * 80)
    print("\n正在生成创新剧情章节...")
    print("预计需要 5-10 分钟...")

    content = generate_chapters()
    save_chapters(content)

    print("\n" + "=" * 80)
    print("                    生成完成！")
    print("=" * 80)
    print("\n📚 章节已生成：output/气运之王_前10章.txt")
    print("\n创新看点：")
    print("  ✓ 反套路：主角运气爆棚，不惨不虐")
    print("  ✓ 轻松搞笑：笑点密集")
    print("  ✓ 智斗流：靠智慧解决问题")
    print("  ✓ 锦鲤体质：走路捡灵石")
    print("  ✓ 美食元素：烹饪提升修为")
    print("=" * 80)

if __name__ == "__main__":
    main()
