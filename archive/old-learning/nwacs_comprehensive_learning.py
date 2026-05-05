#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 全能联网学习系统
收集词汇、地名、功法、物品、人物描述、名言警句等
分析热门小说的卖点、修辞手法、情景、剧情
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

VERSION = "4.0"
SYSTEM_NAME = "NWACS 全能联网学习系统"

# ============================================================================
# 配置
# ============================================================================

def load_config():
    config = {}
    if os.path.exists('config.json'):
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
    return config

# ============================================================================
# 全能学习主题定义
# ============================================================================

LEARNING_CATEGORIES = {
    "词汇收集": {
        "topics": [
            "玄幻小说词汇 光影类 鎏金 碎银 氤氲 斑驳",
            "玄幻小说动作动词 凝睇 沉吟 踉跄 思忖",
            "玄幻小说情感形容词 凄切 欣悦 震怒 悚然",
            "仙侠小说场景描写词汇 云雾缭绕 仙气缥缈",
            "玄幻小说神态描写词汇 眸光流转 眉目含情"
        ],
        "skill": "词汇大师"
    },
    
    "地名收集": {
        "topics": [
            "玄幻小说门派名称 大全 青云门 玄天宗",
            "玄幻小说城池名称 长安城 洛阳城 姑苏城",
            "玄幻小说秘境名称 幽冥秘境 太古遗迹 天魔窟",
            "玄幻小说海洋名称 东海龙宫 南海普陀",
            "玄幻小说山川名称 不周山 昆仑山 蓬莱岛"
        ],
        "skill": "世界观构造师"
    },
    
    "功法收集": {
        "topics": [
            "玄幻小说功法名称 九转玄功 天魔诀 如来神掌",
            "玄幻小说剑法名称 万剑归宗 天外飞仙 独孤九剑",
            "玄幻小说炼丹术 三昧真火 九转丹成",
            "玄幻小说阵法名称 两仪微尘阵 周天星辰阵",
            "玄幻小说炼体术 混沌不灭体 金刚不坏身"
        ],
        "skill": "战斗设计师"
    },
    
    "物品收集": {
        "topics": [
            "玄幻小说法宝 番天印 打神鞭 玲珑塔",
            "玄幻小说丹药 九转金丹 蟠桃 人参果",
            "玄幻小说武器 轩辕剑 干将莫邪 倚天剑",
            "玄幻小说坐骑 青龙白虎 朱雀玄武",
            "玄幻小说灵植 菩提树 人参果树 蟠桃树"
        ],
        "skill": "世界观构造师"
    },
    
    "人物描述": {
        "topics": [
            "玄幻小说男主外貌描写 剑眉星目 面如冠玉",
            "玄幻小说女主外貌描写 倾国倾城 沉鱼落雁",
            "玄幻小说老者外貌描写 仙风道骨 鹤发童颜",
            "玄幻小说反派外貌描写 面如冠玉 心如蛇蝎",
            "玄幻小说人物气质描写 温文尔雅 狂傲不羁"
        ],
        "skill": "角色塑造师"
    },
    
    "名言警句": {
        "topics": [
            "玄幻小说经典语录 三观正 热血",
            "剑来经典语录 陈平安",
            "玄幻小说战斗宣言 我命由我不由天",
            "玄幻小说感情语录 执子之手 与子偕老",
            "玄幻小说哲理语录 道法自然"
        ],
        "skill": "写作技巧大师"
    },
    
    "热门小说分析": {
        "topics": [
            "剑来 烽火戏诸侯 卖点分析 写作手法",
            "庆余年 猫腻 卖点分析 写作技巧",
            "诡秘之主 乌贼 卖点分析 设定创新",
            "全职高手 蝴蝶蓝 卖点分析 人物刻画",
            "凡人修仙传 忘语 卖点分析 苟道写法"
        ],
        "skill": "市场分析师"
    },
    
    "修辞手法": {
        "topics": [
            "玄幻小说比喻描写技巧 生动形象",
            "玄幻小说夸张手法 气吞山河 毁天灭地",
            "玄幻小说对偶描写 对仗工整",
            "玄幻小说通感描写 视听味触",
            "玄幻小说象征手法 以物喻人"
        ],
        "skill": "写作技巧大师"
    },
    
    "情景描写": {
        "topics": [
            "玄幻小说战斗场景描写 热血沸腾",
            "玄幻小说爱情场景描写 缠绵悱恻",
            "玄幻小说恐怖场景描写 毛骨悚然",
            "玄幻小说唯美场景描写 诗情画意",
            "玄幻小说悲伤场景描写 催人泪下"
        ],
        "skill": "场景构造师"
    },
    
    "剧情设计": {
        "topics": [
            "玄幻小说开局写法 黄金三章",
            "玄幻小说冲突设计 环环相扣",
            "玄幻小说伏笔埋设 草蛇灰线",
            "玄幻小说高潮设计 燃爆全场",
            "玄幻小说结局设计 余韵无穷"
        ],
        "skill": "剧情构造师"
    }
}

# ============================================================================
# DeepSeek API调用
# ============================================================================

def call_deepseek_v4(prompt, system_prompt=None, max_tokens=8000, timeout=180):
    config = load_config()
    if not config.get('api_key'):
        print("❌ 错误: API Key未配置！")
        return None

    if not system_prompt:
        system_prompt = """你是一位顶尖的网络小说研究专家，精通玄幻仙侠小说的创作。
请用中文详细回答，收集丰富的词汇、地名、功法等素材，并分析热门小说的写作技巧。
请提供具体的例子和分析！"""

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
        'max_tokens': max_tokens
    }

    print(f"\n⏳ 正在调用DeepSeek V4...")
    
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
# 保存学习成果
# ============================================================================

def save_learning_result(category, topic, content):
    """保存学习成果"""
    os.makedirs('learning/comprehensive', exist_ok=True)
    
    # 保存单个主题
    safe_topic = ''.join(c for c in topic[:20] if c not in '\\/:*?"<>|')
    filename = f"{category}_{safe_topic}.txt"
    filepath = os.path.join('learning/comprehensive', filename)
    
    header = f"""{category} - {topic}
{'='*60}
学习时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*60}

"""
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(header)
        f.write(content)
    
    print(f"✅ 已保存: {filepath}")
    
    # 更新汇总文件
    update_summary_file(category, topic, content)

def update_summary_file(category, topic, content):
    """更新汇总文件"""
    summary_file = 'learning/comprehensive/学习汇总.md'
    
    # 读取现有内容
    if os.path.exists(summary_file):
        with open(summary_file, 'r', encoding='utf-8') as f:
            content_md = f.read()
    else:
        content_md = f"""# NWACS 全能学习汇总
{'='*60}
更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*60}

"""
    
    # 添加新内容
    content_md += f"""

## {category} - {topic}

{content}

---
"""
    
    # 保存
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(content_md)

# ============================================================================
# 主流程
# ============================================================================

def start_comprehensive_learning():
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║           {SYSTEM_NAME} v{VERSION}                              ║
║                                                              ║
║           📚 学习内容：                                      ║
║           ✅ 收集词汇、丰富词语                               ║
║           ✅ 收集地名、功法、物品                             ║
║           ✅ 收集人物描述、名言警句                           ║
║           ✅ 分析热门小说卖点、修辞手法                       ║
║           ✅ 分析情景描写、剧情设计                           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # 检查配置
    config = load_config()
    if not config.get('api_key'):
        print("❌ API Key未配置！")
        return
    
    # 统计
    total_categories = len(LEARNING_CATEGORIES)
    total_topics = sum(len(cat['topics']) for cat in LEARNING_CATEGORIES.values())
    
    print(f"\n📊 学习统计:")
    print(f"   总分类：{total_categories} 个")
    print(f"   总主题：{total_topics} 个")
    print(f"   预计时间：约 {total_topics * 2} 分钟")
    
    category_count = 0
    topic_count = 0
    
    # 按分类学习
    for category, data in LEARNING_CATEGORIES.items():
        category_count += 1
        print(f"\n{'='*60}")
        print(f"📚 正在学习分类：{category}")
        print(f"   目标Skill：{data['skill']}")
        print(f"   进度：{category_count}/{total_categories}")
        print(f"{'='*60}")
        
        for topic in data['topics']:
            topic_count += 1
            print(f"\n⏳ [{topic_count}/{total_topics}] 正在学习：{topic[:30]}...")
            
            # 构建学习提示
            prompt = f"""请为小说创作提供丰富的素材：

主题：{topic}

请提供：
1. 至少20个具体的词汇/名称/描写
2. 每个词汇/名称的详细解释
3. 在小说中的运用示例
4. 相关的扩展词汇或名称

请用列表形式，分类整理！"""
            
            # 调用DeepSeek
            content = call_deepseek_v4(prompt)
            
            if content:
                save_learning_result(category, topic, content)
                print(f"✅ [{topic_count}/{total_topics}] 完成！")
            else:
                print(f"❌ [{topic_count}/{total_topics}] 失败！")
            
            time.sleep(2)  # 避免请求过快
    
    # 生成最终报告
    generate_final_report(topic_count)

def generate_final_report(success_count):
    print(f"\n{'='*60}")
    print("📋 生成最终报告...")
    print(f"{'='*60}")
    
    report = f"""# NWACS 全能联网学习报告
{'='*60}
学习时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📊 学习统计
- 学习分类: {len(LEARNING_CATEGORIES)} 个
- 学习主题: {success_count} 个
- 学习系统: {SYSTEM_NAME} v{VERSION}

## 📚 学习内容分类

### 1. 词汇收集
收集丰富的玄幻小说词汇，包括光影类、动作类、情感类等

### 2. 地名收集
收集门派名称、城池名称、秘境名称、山川名称等

### 3. 功法收集
收集功法名称、剑法名称、炼丹术、阵法、炼体术等

### 4. 物品收集
收集法宝、丹药、武器、坐骑、灵植等

### 5. 人物描述
收集男主、女主、老者、反派等各类人物的外貌和气质描写

### 6. 名言警句
收集经典语录、战斗宣言、感情语录、哲理语录等

### 7. 热门小说分析
分析《剑来》《庆余年》《诡秘之主》等热门小说的卖点

### 8. 修辞手法
学习比喻、夸张、对偶、通感、象征等修辞技巧

### 9. 情景描写
学习战斗、爱情、恐怖、唯美、悲伤等场景的描写技巧

### 10. 剧情设计
学习开局写法、冲突设计、伏笔埋设、高潮设计、结局设计等

## 📂 生成文件
- learning/comprehensive/学习汇总.md（汇总文件）
- learning/comprehensive/分类_主题.txt（单项文件）

## 💡 学习成果
通过全能联网学习，系统现在拥有：
- 丰富的词汇库
- 完善的地名库
- 系统的功法体系库
- 详细的物品描述库
- 多样的人物模板库
- 深刻的名言警句库
- 热门小说的分析报告
- 专业的写作技巧库

{'='*60}
报告结束
"""
    
    # 保存报告
    os.makedirs('learning/comprehensive', exist_ok=True)
    report_path = 'learning/comprehensive/全能学习报告.md'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✅ 报告已保存: {report_path}")
    
    # 打印总结
    print("\n" + "="*60)
    print("🎉 全能联网学习完成！")
    print("="*60)
    print(f"\n📊 学习统计:")
    print(f"   ✅ 完成 {success_count} 个主题的学习")
    print(f"   ✅ 收集词汇、地名、功法、物品等素材")
    print(f"   ✅ 分析热门小说的卖点")
    print(f"   ✅ 学习修辞手法和情景描写")
    print(f"\n📂 学习文件位置: learning/comprehensive/")

if __name__ == "__main__":
    start_comprehensive_learning()
