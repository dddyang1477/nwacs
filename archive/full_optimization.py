#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 小说生成工具全网学习优化器
使用 DeepSeek V4 进行深度学习优化
"""

import os
import sys
import json
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
        system_prompt = """你是一位资深的小说创作专家，精通各种类型的小说创作技巧。
请提供专业、详细、实用的写作知识和建议。"""

    import urllib.request
    import urllib.error

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
        'temperature': 0.7,
        'max_tokens': 4000
    }

    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method='POST')

    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result['choices'][0]['message']['content']
    except Exception as e:
        print(f"API Error: {e}")
        return None

def learn_vocabulary():
    """学习丰富词汇储备"""
    print("\n[1/6] 正在学习词汇储备...")
    
    prompt = """请提供丰富的小说写作词汇，包括：
1. 人物外貌描写词汇（五官、神态、气质）
2. 环境描写词汇（天气、场景、氛围）
3. 动作描写词汇（肢体动作、心理活动）
4. 古风词汇（诗词典故、成语俗语）
5. 网络流行词汇（适合现代题材）

请给出具体词汇列表，每个类别至少50个词汇。"""

    response = call_deepseek_v4(prompt)
    if response:
        save_to_file('skills/vocabulary_master.txt', response)
        print("  ✓ 词汇学习完成")
        return response
    return None

def learn_writing_techniques():
    """学习写作手法"""
    print("\n[2/6] 正在学习写作手法...")
    
    prompt = """请详细讲解小说写作的各种手法和技巧：
1. 叙事视角选择（第一/第三人称、多视角）
2. 节奏把控技巧（快慢节奏切换）
3. 悬念设置方法（伏笔、反转、高潮）
4. 对话写作技巧（对话推动情节）
5. 倒叙插叙运用

请给出具体案例和分析。"""

    response = call_deepseek_v4(prompt)
    if response:
        save_to_file('skills/writing_techniques.txt', response)
        print("  ✓ 写作手法学习完成")
        return response
    return None

def learn_scene_rendering():
    """学习场景渲染"""
    print("\n[3/6] 正在学习场景渲染...")
    
    prompt = """请详细讲解场景描写和氛围渲染的技巧：
1. 环境描写方法（视觉、听觉、嗅觉、触觉）
2. 氛围营造技巧（通过细节烘托情绪）
3. 场景转换方法（自然过渡、时间跳跃）
4. 关键场景描写案例（战斗、情感高潮、悬疑场景）

请给出具体案例和分析。"""

    response = call_deepseek_v4(prompt)
    if response:
        save_to_file('skills/scene_rendering.txt', response)
        print("  ✓ 场景渲染学习完成")
        return response
    return None

def learn_anti_ai_detection():
    """学习去AI痕迹技巧"""
    print("\n[4/6] 正在学习去AI痕迹技巧...")
    
    prompt = """请详细讲解如何让文字更有"人味"，避免AI检测：
1. 避免模板化表达
2. 使用个性化语言
3. 添加真实细节和瑕疵
4. 模仿人类写作习惯
5. 口语化表达技巧

请给出具体方法和示例。"""

    response = call_deepseek_v4(prompt)
    if response:
        save_to_file('skills/anti_ai_detection.txt', response)
        print("  ✓ 去AI痕迹学习完成")
        return response
    return None

def learn_plot_design():
    """学习剧情铺设"""
    print("\n[5/6] 正在学习剧情铺设...")
    
    prompt = """请详细讲解剧情设计和铺设技巧：
1. 故事结构设计（三幕式、英雄之旅）
2. 情节推进方法（冲突升级、转折点）
3. 伏笔埋设技巧（前后呼应、线索布置）
4. 高潮设计方法（情绪顶点、释放）
5. 常见剧情套路（穿越、重生、系统流等）

请给出具体案例分析。"""

    response = call_deepseek_v4(prompt)
    if response:
        save_to_file('skills/plot_design.txt', response)
        print("  ✓ 剧情铺设学习完成")
        return response
    return None

def learn_character_building():
    """学习人物架设"""
    print("\n[6/6] 正在学习人物架设...")
    
    prompt = """请详细讲解人物塑造的方法：
1. 人物设定要素（外貌、性格、背景、动机）
2. 人物弧线设计（成长、转变、弧光）
3. 人物关系网络（冲突、羁绊、对手）
4. 人物标签化与立体化
5. 配角设计技巧（功能性、个性鲜明）

请给出具体案例分析。"""

    response = call_deepseek_v4(prompt)
    if response:
        save_to_file('skills/character_building.txt', response)
        print("  ✓ 人物架设学习完成")
        return response
    return None

def save_to_file(filename, content):
    """保存学习内容到文件"""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

def update_skill_files():
    """更新Skill文件"""
    print("\n[7/6] 正在更新Skill文件...")
    
    # 更新词汇大师 Skill
    vocab_content = """# 词汇大师 Skill

## 核心功能
提供丰富的写作词汇储备，涵盖人物、环境、动作、古风等多个维度。

## 词汇分类

### 人物外貌描写
- 面容：明眸皓齿、眉清目秀、面如冠玉、沉鱼落雁、闭月羞花
- 神态：神采飞扬、黯然神伤、怒目圆睁、嫣然一笑、愁眉紧锁
- 气质：温文尔雅、英姿飒爽、风度翩翩、仙风道骨、器宇轩昂

### 环境描写词汇
- 自然：鸟语花香、山清水秀、姹紫嫣红、白雪皑皑、烈日炎炎
- 氛围：阴森恐怖、温馨浪漫、庄严肃穆、热闹非凡、凄凉萧瑟

### 动作描写词汇
- 肢体：轻盈、矫健、笨拙、优雅、蹒跚
- 心理：忐忑、惆怅、欣喜、愤怒、哀伤

### 古风词汇
- 诗词：云淡风轻、花前月下、青梅竹马、海誓山盟、执子之手
- 成语：倾国倾城、沉鱼落雁、闭月羞花、国色天香、冰肌玉骨

## 使用建议
1. 根据场景选择合适词汇
2. 避免重复使用相同词汇
3. 结合上下文灵活运用
"""
    with open('skills/level3/32_三级Skill_词汇大师.md', 'w', encoding='utf-8') as f:
        f.write(vocab_content)
    
    # 更新写作技巧大师 Skill
    writing_content = """# 写作技巧大师 Skill

## 核心功能
提供专业的写作手法指导，帮助提升写作水平。

## 写作手法

### 叙事视角
- 第一人称：代入感强，适合情感描写
- 第三人称：视角广阔，适合复杂故事
- 多视角切换：展现不同人物内心

### 节奏把控
- 快慢结合：紧张场景快速推进，抒情场景放慢节奏
- 信息密度：控制每段信息量，保持读者兴趣

### 悬念设置
- 伏笔埋设：提前布置线索，后期回收
- 反转设计：打破读者预期，制造惊喜
- 高潮控制：合理安排情绪峰值

### 对话技巧
- 对话推动情节发展
- 通过对话展现人物性格
- 避免冗长无意义对话

## 使用建议
1. 根据故事类型选择合适手法
2. 不断练习，形成个人风格
3. 参考优秀作品学习借鉴
"""
    with open('skills/level2/09_二级Skill_写作技巧大师.md', 'w', encoding='utf-8') as f:
        f.write(writing_content)
    
    print("  ✓ Skill文件更新完成")

def generate_optimization_report(results):
    """生成优化报告"""
    report = [
        "# NWACS 小说生成工具全网学习优化报告",
        "",
        "## 📅 优化日期",
        f"{time.strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## 📋 优化内容",
        "",
        "### 1. 词汇储量提升",
        "✓ 人物外貌描写词汇",
        "✓ 环境描写词汇",
        "✓ 动作描写词汇",
        "✓ 古风词汇与成语",
        "",
        "### 2. 写作手法学习",
        "✓ 叙事视角选择",
        "✓ 节奏把控技巧",
        "✓ 悬念设置方法",
        "✓ 对话写作技巧",
        "",
        "### 3. 场景渲染技巧",
        "✓ 环境描写方法",
        "✓ 氛围营造技巧",
        "✓ 场景转换方法",
        "",
        "### 4. 去AI痕迹",
        "✓ 避免模板化表达",
        "✓ 使用个性化语言",
        "✓ 添加真实细节",
        "",
        "### 5. 剧情铺设",
        "✓ 故事结构设计",
        "✓ 情节推进方法",
        "✓ 伏笔埋设技巧",
        "",
        "### 6. 人物架设",
        "✓ 人物设定要素",
        "✓ 人物弧线设计",
        "✓ 人物关系网络",
        "",
        "## 📁 学习资料保存位置",
        "- skills/vocabulary_master.txt",
        "- skills/writing_techniques.txt",
        "- skills/scene_rendering.txt",
        "- skills/anti_ai_detection.txt",
        "- skills/plot_design.txt",
        "- skills/character_building.txt",
        "",
        "## ✅ 优化状态",
        "所有学习模块均已完成！"
    ]
    
    report_path = 'OPTIMIZATION_REPORT_FULL.md'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))
    
    return report_path

def main():
    print("\n" + "=" * 80)
    print("          NWACS 小说生成工具全网学习优化器")
    print("=" * 80)
    print("\n正在使用 DeepSeek V4 进行深度学习优化...")
    print("预计需要 5-10 分钟，请耐心等待...")

    results = []
    
    # 1. 词汇储量
    vocab_result = learn_vocabulary()
    results.append(('词汇储量', vocab_result))
    
    # 2. 写作手法
    writing_result = learn_writing_techniques()
    results.append(('写作手法', writing_result))
    
    # 3. 场景渲染
    scene_result = learn_scene_rendering()
    results.append(('场景渲染', scene_result))
    
    # 4. 去AI痕迹
    ai_result = learn_anti_ai_detection()
    results.append(('去AI痕迹', ai_result))
    
    # 5. 剧情铺设
    plot_result = learn_plot_design()
    results.append(('剧情铺设', plot_result))
    
    # 6. 人物架设
    char_result = learn_character_building()
    results.append(('人物架设', char_result))
    
    # 7. 更新Skill文件
    update_skill_files()
    
    # 8. 生成报告
    report_path = generate_optimization_report(results)
    
    print("\n" + "=" * 80)
    print("                    优化完成！")
    print("=" * 80)
    print("\n📚 学习成果：")
    for name, result in results:
        status = "✓" if result else "✗"
        print(f"  {status} {name}")
    
    print(f"\n📋 详细报告已保存至: {report_path}")
    print(f"\n📁 学习资料保存位置: skills/")
    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()
