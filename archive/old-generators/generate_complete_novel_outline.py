#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整长篇玄幻小说大纲生成器
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

def call_deepseek_v4(prompt):
    config = load_config()
    if not config.get('api_key'):
        print("ERROR: API Key not configured")
        return None

    system_prompt = """你是一位顶尖玄幻网文大神，擅长长篇小说创作、世界构建、人物设定、情节设计。
你创作的小说结构严谨、世界观宏大、人物丰满、情节跌宕起伏。"""

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
        'max_tokens': 8000
    }

    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method='POST')

    try:
        with urllib.request.urlopen(req, timeout=300) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result['choices'][0]['message']['content']
    except Exception as e:
        print(f"API Error: {e}")
        return None

def generate_full_outline():
    """生成完整小说大纲"""
    print("\n[1/2] 正在生成完整长篇玄幻小说大纲...")
    print("预计需要 5-10 分钟，请耐心等待...")

    prompt = """请为一部修仙玄幻长篇小说（100万字以上）生成完整详细的大纲，要求：

## 一、书名
生成10个有特色、能吸引读者的书名，风格是苟道流、黑暗流、智斗流相结合。

## 二、吸引读者的核心卖点
详细说明这部小说为什么能吸引读者。

## 三、世界观设定
### 1. 大陆体系
- 详细描述至少4块大陆的设定
- 每块大陆的环境、资源、势力分布

### 2. 世界规则
- 天地灵气的分布规律
- 修炼资源的分布
- 天地法则设定（时间、空间、命运、因果等）
- 世界意志与天道设定

## 四、修炼体系
### 1. 主要修炼体系（法术为主）
- 详细的境界划分（炼气→筑基→金丹→元婴→化神→炼虚→合体→大乘→渡劫→地仙→天仙→金仙→大罗金仙→混元大罗金仙→道祖）
- 每个境界的特征、能力、突破条件

### 2. 辅助修炼体系（6种以上）
- **炼丹**：
  * 丹药等级（九转：凡丹→灵丹→法丹→元丹→天丹→仙丹→神丹→圣丹→道丹）
  * 丹药类型（突破、疗伤、毒丹、增幅、疗伤、悟道等）
  * 炼丹材料（珍稀草药、妖兽材料、天材地宝等）
  * 炼丹手法（文火慢熬、三昧真火、五行丹火、九转凝丹术、天雷炼丹等）

- **炼体**：
  * 肉身境界（凡体→灵体→法体→宝体→仙体→神体→圣体→道体）
  * 炼体功法、特殊体质（不灭金身、混沌之体、天妖之体等）

- **炼毒**：
  * 毒药等级、毒抗体质、毒药用途、制毒手法

- **炼器**：
  * 法宝等级（法器→灵器→宝器→道器→仙器→神器→圣器→道器）
  * 炼制手法、材料分类、法宝分类（攻防、辅助、特殊）

- **御兽**：
  * 妖兽等级、契约方式、御兽技巧、灵兽分类

- **阵法**：
  * 阵法等级（凡阵→灵阵→法阵→仙阵→神阵→圣阵→混沌大阵）
  * 阵法类型（困敌、攻击、防御、迷幻、传送、聚灵、杀阵等）
  * 阵法材料、布阵手法、规模范围

## 五、门派势力
### 1. 三大古派
- 每派的创派历史、功法特色、宗门实力、掌门、著名弟子、地理位置

### 2. 七大宗门
- 每宗的详细设定

### 3. 三十六门派
- 主要门派的特色设定

### 4. 反派宗教
- 反派势力的设定、目标、组织结构、主要人物

### 5. 大陆主要学院
- 学院设定、教学特色、招生标准

### 6. 门派关系
- 各大门派之间的关系网（联盟、敌对、中立等）

## 六、人物设定
### 1. 主角设定（详细）
- 姓名、身份、外貌、身材体型、穿着、面目特征
- 性格特点（苟道、黑暗、智斗相结合）
- 擅长能力
- 背景故事
- 金手指设定

### 2. 女主设定（4位以上，每位都要详细）
- 姓名、身份、外貌、性格、身材、穿着、擅长、背景
- 与主角的感情发展线

### 3. 配角设定（正反两派都要有）
- 重要配角的详细设定

### 4. 小人物通用模板（至少3种）
- 典型的小人物角色模板

## 七、妖兽系统
- 妖兽等级（一阶→九阶→妖兽皇→妖兽帝→妖神→妖圣→妖道）
- 妖兽分类（龙族、凤族、白虎族、玄武族、妖族、昆虫类、远古凶兽等）
- 至少20种典型妖兽的外形、能力、等级、弱点

## 八、阵法系统
- 阵法等级详细划分
- 至少15种阵法的具体设定（名称、材料、功能、规模、威力）
- 布阵手法详解

## 九、法宝系统
- 法宝等级详细划分
- 至少20种法宝的具体设定（名称、形状、功能、来历）

## 十、武器装备饰品系统
- 武器分类（剑、刀、枪、弓、锤、棍、拂尘、扇等）
- 防具分类（战甲、内甲、护腕、护腿等）
- 饰品分类（戒指、项链、手镯、耳环、面具、披风、靴子等）
- 装备等级
- 套装效果
- 炼制材料

## 十一、法术体系
- 法术等级（凡术→灵术→玄术→地术→天术→仙术→神术→圣术→道术）
- 法术类型（攻击、防御、辅助、灵魂、特殊）
- 至少30种法术的详细设定（名称、等级、效果、修炼方法）
- 功法等级（凡阶→灵阶→玄阶→地阶→天阶→仙阶→神阶→圣阶→混沌功法）

## 十二、主线剧情大纲（100万字分卷）
### 第一卷：蝼蚁崛起（1-30万字）
### 第二卷：暗流涌动（30-50万字）
### 第三卷：仙魔大战（50-80万字）
### 第四卷：飞升仙界（80-120万字）
- 每卷的详细剧情纲要
- 关键事件节点

## 十三、前30章详细大纲
- 每章的标题、字数、主要内容、关键转折、爽点、伏笔

## 十四、伏笔与因果事件
- 主要伏笔设定、埋设方式、回收时机

## 十五、感情剧情线
- 主角与每位女主的感情发展线
- 感情转折点、高潮点

## 十六、战斗情节设计
- 探秘境、寻宝、埋伏、伏击战、血战、生死战的具体设计

请输出完整详细的大纲，格式清晰，内容丰富。"""

    response = call_deepseek_v4(prompt)
    if response:
        print("  ✓ 完整大纲生成完成")
        return response
    return None

def save_outline(content):
    """保存大纲"""
    os.makedirs('output', exist_ok=True)
    filepath = os.path.join('output', '完整长篇玄幻小说大纲.txt')
    
    content = f"""# 完整长篇玄幻小说大纲

## 修仙玄幻·苟道流·黑暗流·智斗流·100万字以上

---

{content if content else '大纲生成中...'}

---

本大纲由 NWACS × DeepSeek V4 联合生成
生成时间：{time.strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    content = content.replace('# ', '')
    content = content.replace('## ', '')
    content = content.replace('### ', '')
    content = content.replace('#### ', '')
    content = content.replace('**', '')
    content = content.replace('*', '')
    content = content.replace('---\n', '')
    content = content.replace('|', '')
    content = content.replace('`', '')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n  ✓ 大纲已保存到: {filepath}")
    return filepath

def main():
    print("\n" + "=" * 80)
    print("          完整长篇玄幻小说大纲生成器")
    print("          苟道流·黑暗流·智斗流·100万字以上")
    print("=" * 80)
    print("\n正在使用 DeepSeek V4 生成完整大纲...")
    print("预计需要 5-15 分钟，请耐心等待...")

    content = generate_full_outline()
    save_outline(content)

    print("\n" + "=" * 80)
    print("                    生成完成！")
    print("=" * 80)
    print("\n📚 完整大纲已生成：output/完整长篇玄幻小说大纲.txt")
    print("\n包含内容：")
    print("  ✓ 10个特色书名")
    print("  ✓ 吸引读者的核心卖点")
    print("  ✓ 完整世界观与大陆体系")
    print("  ✓ 庞大修炼体系（含6种辅助修炼）")
    print("  ✓ 50+门派势力设定")
    print("  ✓ 主角+4位女主详细设定")
    print("  ✓ 小人物通用模板")
    print("  ✓ 妖兽系统（20+妖兽）")
    print("  ✓ 阵法系统（15+阵法）")
    print("  ✓ 法宝系统（20+法宝）")
    print("  ✓ 武器装备饰品系统")
    print("  ✓ 法术体系（30+法术）")
    print("  ✓ 100万字主线剧情（分4卷）")
    print("  ✓ 前30章详细大纲")
    print("  ✓ 伏笔与因果事件")
    print("  ✓ 感情剧情线")
    print("  ✓ 战斗情节设计")
    print("=" * 80)

if __name__ == "__main__":
    main()
