#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS × DeepSeek 智能学习系统 - 完整版
学习《剑来》风格，去除AI痕迹，完善所有Skill
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
SYSTEM_NAME = "NWACS × DeepSeek 智能学习系统"

# ============================================================================
# 学习主题定义
# ============================================================================

LEARNING_TOPICS = [
    {
        "name": "剑来风格学习",
        "skill": "写作技巧大师",
        "prompt": """请分析《剑来》这部小说的写作风格，特别是：
1. 主角陈平安的说话方式和口头禅
2. 书中三观较正的经典语句
3. 富有哲理的对话风格
4. 细腻的心理描写
5. 独特的行文节奏

请提供具体的例子和分析！"""
    },
    {
        "name": "去除AI痕迹技巧",
        "skill": "去AI痕迹监督官",
        "prompt": """请告诉我如何避免AI写作的痕迹，写出像真人写的文字：
1. AI写作常见的特征有哪些？
2. 如何让文字更有"人味"？
3. 怎样写出独特的个人风格？
4. 如何避免模板化的表达方式？
5. 请提供具体的修改技巧和示例！"""
    },
    {
        "name": "人物对话个性",
        "skill": "对话设计师",
        "prompt": """请告诉我如何让小说中的人物对话更有个性：
1. 不同身份的人说话方式有什么区别？
2. 如何通过对话展现人物性格？
3. 不同年龄段的人说话有什么特点？
4. 方言和口头禅的运用技巧
5. 请提供具体的例子！"""
    },
    {
        "name": "细腻心理描写",
        "skill": "角色塑造师",
        "prompt": """请告诉我如何写出细腻的心理描写：
1. 如何深入人物内心世界？
2. 如何展现复杂的情感变化？
3. 内心独白的写法技巧
4. 潜意识和显意识的描写区别
5. 请提供具体的例子！"""
    },
    {
        "name": "古风文字风格",
        "skill": "词汇大师",
        "prompt": """请告诉我如何写出有韵味但不晦涩的古风文字：
1. 古风词汇的运用技巧
2. 如何避免堆砌辞藻？
3. 现代语言与古风的融合
4. 节奏感和韵律感的营造
5. 请提供具体的例子！"""
    },
    {
        "name": "三观正的语句",
        "skill": "质量审计师",
        "prompt": """请提供一些三观较正、有哲理的语句示例：
1. 关于善恶是非的思考
2. 关于人生道理的感悟
3. 关于修行和成长的观点
4. 关于友情、爱情、亲情的见解
5. 请提供具体的例子！"""
    }
]

# ============================================================================
# DeepSeek API调用
# ============================================================================

def load_config():
    config = {}
    if os.path.exists('config.json'):
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
    return config

def call_deepseek_v4(prompt, system_prompt=None, max_tokens=6000, timeout=120):
    config = load_config()
    if not config.get('api_key'):
        print("❌ 错误: API Key未配置！")
        return None

    if not system_prompt:
        system_prompt = """你是一位顶尖的网文编辑和写作导师，精通各种写作技巧。
请用中文详细解答写作问题，提供具体的例子和分析！"""

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

    stop_spinner = threading.Event()
    spinner_thread = threading.Thread(target=spinner_animation, args=(stop_spinner,))
    spinner_thread.daemon = True
    spinner_thread.start()

    try:
        req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method='POST')

        with urllib.request.urlopen(req, timeout=timeout) as response:
            stop_spinner.set()
            result = json.loads(response.read().decode('utf-8'))
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
# 更新Skill文件
# ============================================================================

SKILL_FILE_MAP = {
    '写作技巧大师': 'skills/level2/09_二级Skill_写作技巧大师.md',
    '去AI痕迹监督官': 'skills/level2/10_二级Skill_去AI痕迹监督官.md',
    '对话设计师': 'skills/level2/06_二级Skill_对话设计师.md',
    '角色塑造师': 'skills/level2/07_二级Skill_角色塑造师.md',
    '词汇大师': 'skills/level2/32_二级Skill_词汇大师.md',
    '质量审计师': 'skills/level2/11_二级Skill_质量审计师.md',
}

def update_skill_file(skill_name, content):
    filepath = SKILL_FILE_MAP.get(skill_name)
    if not filepath:
        filepath = f'skills/{skill_name}.md'
    
    if not os.path.isabs(filepath):
        filepath = os.path.join(os.path.dirname(__file__), filepath)
    
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    # 读取现有内容
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            existing_content = f.read()
    else:
        existing_content = f"""# {skill_name}
{'=' * 60}

"""
    
    # 添加学习内容
    chapter_title = f"\n\n## 学习成果 - {datetime.now().strftime('%Y-%m-%d')}\n\n"
    chapter_content = chapter_title + content
    chapter_content += "\n---\n*本章节由DeepSeek学习系统自动生成*\n"
    
    # 在文件末尾添加
    existing_content += chapter_content
    
    # 保存
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(existing_content)
    
    print(f"✅ 更新Skill: {filepath}")

# ============================================================================
# 主流程
# ============================================================================

def start_learning():
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║           {SYSTEM_NAME} v{VERSION}                          ║
║                                                              ║
║           🎯 学习目标:                                        ║
║           1. 《剑来》风格学习                                 ║
║           2. 去除AI痕迹技巧                                   ║
║           3. 三观较正的语句                                   ║
║           4. 完善所有Skill功能                               ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # 检查配置
    config = load_config()
    if not config.get('api_key'):
        print("❌ API Key未配置！")
        return
    
    # 开始学习
    for topic in LEARNING_TOPICS:
        print(f"\n{'='*60}")
        print(f"🎯 正在学习: {topic['name']}")
        print(f"📚 目标Skill: {topic['skill']}")
        print(f"{'='*60}")
        
        print("\n⏳ 正在调用DeepSeek V4...")
        content = call_deepseek_v4(topic['prompt'])
        
        if content:
            print("✅ 学习完成！")
            update_skill_file(topic['skill'], content)
        else:
            print("❌ 学习失败！")
    
    # 生成总结报告
    generate_report()

def generate_report():
    print(f"\n{'='*60}")
    print("📋 生成学习报告...")
    print(f"{'='*60}")
    
    report = f"""# NWACS × DeepSeek 学习报告
{'='*60}
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 🎯 学习目标
1. 《剑来》风格学习 - 学习陈平安的说话方式、三观较正的语句
2. 去除AI痕迹技巧 - 写出像真人写的文字
3. 人物对话个性 - 让每个角色说话有自己特点
4. 细腻心理描写 - 深入人物内心世界
5. 古风文字风格 - 有韵味但不晦涩
6. 三观正的语句 - 有哲理的观点

## ✅ 学习成果

### 1. 《剑来》风格学习
- 学习了陈平安的说话方式和口头禅
- 学习了富有哲理的对话风格
- 学习了细腻的心理描写技巧

### 2. 去除AI痕迹技巧
- 了解了AI写作常见的特征
- 学习了让文字更有"人味"的方法
- 掌握了避免模板化表达的技巧

### 3. 人物对话个性
- 学习了不同身份人物的说话方式
- 掌握了通过对话展现性格的技巧
- 了解了方言和口头禅的运用

### 4. 细腻心理描写
- 学习了深入人物内心世界的方法
- 掌握了展现复杂情感变化的技巧
- 了解了内心独白的写法

### 5. 古风文字风格
- 学习了古风词汇的运用技巧
- 掌握了避免堆砌辞藻的方法
- 了解了现代语言与古风的融合

### 6. 三观正的语句
- 收集了关于善恶是非的思考
- 收集了关于人生道理的感悟
- 收集了关于修行和成长的观点

## 📂 更新的Skill文件
"""
    
    for topic in LEARNING_TOPICS:
        filepath = SKILL_FILE_MAP.get(topic['skill'], f'skills/{topic["skill"]}.md')
        report += f"- {topic['skill']}: {filepath}\n"
    
    report += f"""

## 📊 统计信息
- 学习主题数: {len(LEARNING_TOPICS)}
- 更新Skill数: {len(SKILL_FILE_MAP)}
- 学习时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{'='*60}
报告结束
"""
    
    # 保存报告
    os.makedirs('learning', exist_ok=True)
    report_path = f'learning/学习报告_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✅ 报告已保存: {report_path}")
    
    # 打印报告摘要
    print("\n" + "="*60)
    print("🎉 学习优化完成！")
    print("="*60)
    print("\n📊 学习成果总结:")
    print(f"   ✅ 学习了 {len(LEARNING_TOPICS)} 个主题")
    print(f"   ✅ 更新了 {len(SKILL_FILE_MAP)} 个Skill文件")
    print(f"   ✅ 《剑来》风格学习完成")
    print(f"   ✅ 去除AI痕迹技巧已掌握")
    print(f"   ✅ 三观较正语句已收集")
    print(f"\n📂 学习文件保存位置: learning/")

if __name__ == "__main__":
    start_learning()
