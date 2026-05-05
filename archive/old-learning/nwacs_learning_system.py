#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS × DeepSeek 智能学习优化系统
✨ 学习《剑来》风格，去除AI痕迹，完善所有Skill
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
# 配置模块
# ============================================================================

def load_config():
    config = {}
    if os.path.exists('config.json'):
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
    return config

# ============================================================================
# 学习主题定义
# ============================================================================

LEARNING_TOPICS = [
    {
        "name": "剑来风格学习",
        "description": "学习《剑来》中陈平安的说话方式、个性文字风格、三观较正的语句",
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
        "description": "学习如何写出像真人写的文字，避免AI写作的痕迹",
        "prompt": """请告诉我如何避免AI写作的痕迹，写出像真人写的文字：
1. AI写作常见的特征有哪些？
2. 如何让文字更有"人味"？
3. 怎样写出独特的个人风格？
4. 如何避免模板化的表达方式？
5. 请提供具体的修改技巧和示例！"""
    },
    {
        "name": "人物对话个性",
        "description": "学习如何让每个角色说话都有自己的特点",
        "prompt": """请告诉我如何让小说中的人物对话更有个性：
1. 不同身份的人说话方式有什么区别？
2. 如何通过对话展现人物性格？
3. 不同年龄段的人说话有什么特点？
4. 方言和口头禅的运用技巧
5. 请提供具体的例子！"""
    },
    {
        "name": "细腻心理描写",
        "description": "学习细腻的心理描写技巧",
        "prompt": """请告诉我如何写出细腻的心理描写：
1. 如何深入人物内心世界？
2. 如何展现复杂的情感变化？
3. 内心独白的写法技巧
4. 潜意识和显意识的描写区别
5. 请提供具体的例子！"""
    },
    {
        "name": "古风文字风格",
        "description": "学习古风文字的写法，有韵味不晦涩",
        "prompt": """请告诉我如何写出有韵味但不晦涩的古风文字：
1. 古风词汇的运用技巧
2. 如何避免堆砌辞藻？
3. 现代语言与古风的融合
4. 节奏感和韵律感的营造
5. 请提供具体的例子！"""
    },
    {
        "name": "三观正的语句",
        "description": "学习写出三观较正、有哲理的语句",
        "prompt": """请提供一些三观较正、有哲理的语句示例：
1. 关于善恶是非的思考
2. 关于人生道理的感悟
3. 关于修行和成长的观点
4. 关于友情、爱情、亲情的见解
5. 请提供具体的例子！"""
    }
]

# ============================================================================
# DeepSeek API调用（优化版）
# ============================================================================

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

def save_learning_result(topic_name, content):
    safe_name = ''.join(c for c in topic_name if c not in '\\/:*?"<>|')
    filename = f"{safe_name}.txt"
    
    os.makedirs('learning', exist_ok=True)
    filepath = os.path.join('learning', filename)
    
    header = f"""{topic_name}
{'=' * 60}
学习时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'=' * 60}

"""
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(header)
        f.write(content)
    
    print(f"✅ 学习成果已保存: {filepath}")
    return filepath

# ============================================================================
# 更新Skill文件
# ============================================================================

def update_skill_files(learning_content):
    """更新所有Skill文件"""
    skills_dir = 'skills'
    
    if not os.path.exists(skills_dir):
        os.makedirs(skills_dir)
    
    # 更新或创建各个Skill
    skill_files = [
        ("CharacterMaster.txt", "角色塑造大师 - 人物对话个性"),
        ("PlotMaster.txt", "剧情构造大师 - 情节设计"),
        ("GoldenPhraseMaster.txt", "词汇大师 - 古风文字风格"),
        ("StyleMaster.txt", "写作风格大师 - 去除AI痕迹"),
        ("DialogueMaster.txt", "对话大师 - 人物对话技巧"),
        ("PsychologyMaster.txt", "心理描写大师 - 细腻心理描写"),
    ]
    
    for filename, description in skill_files:
        filepath = os.path.join(skills_dir, filename)
        
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                existing_content = f.read()
        else:
            existing_content = f"""# {description}
{'=' * 60}

"""
        
        new_content = existing_content + f"\n\n【学习更新 - {datetime.now().strftime('%Y-%m-%d')}】\n\n{learning_content}\n"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ 更新Skill: {filepath}")

# ============================================================================
# 学习主流程
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
    
    all_learning_content = ""
    
    for topic in LEARNING_TOPICS:
        print(f"\n{'='*60}")
        print(f"🎯 正在学习: {topic['name']}")
        print(f"{'='*60}")
        
        content = call_deepseek_v4(topic['prompt'])
        if content:
            all_learning_content += f"\n\n{'='*60}\n"
            all_learning_content += f"【{topic['name']}】\n"
            all_learning_content += f"{'='*60}\n\n"
            all_learning_content += content
            
            save_learning_result(topic['name'], content)
            print(f"\n📚 学习完成: {topic['name']}")
        else:
            print(f"\n❌ 学习失败: {topic['name']}")
    
    # 更新所有Skill文件
    if all_learning_content:
        print(f"\n{'='*60}")
        print("📦 正在更新所有Skill文件...")
        print(f"{'='*60}")
        update_skill_files(all_learning_content)
    
    print(f"\n{'='*60}")
    print("🎉 学习优化完成！")
    print(f"{'='*60}")
    print("\n📊 学习成果总结:")
    print(f"   ✅ 学习了 {len(LEARNING_TOPICS)} 个主题")
    print(f"   ✅ 更新了所有Skill文件")
    print(f"   ✅ 去除AI痕迹技巧已掌握")
    print(f"   ✅ 《剑来》风格学习完成")
    print(f"\n📂 学习文件保存位置: learning/")

# ============================================================================
# 主程序
# ============================================================================

def main():
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║           {SYSTEM_NAME} v{VERSION}                          ║
║           ✨ 智能学习优化系统                                 ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # 检查配置
    config = load_config()
    if not config.get('api_key'):
        print("❌ API Key未配置！")
        print("请先运行 nwacs_deepseek_v3.py 配置DeepSeek")
        return
    
    # 开始学习
    start_learning()

if __name__ == "__main__":
    main()
