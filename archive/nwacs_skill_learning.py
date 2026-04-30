#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS Skill联网学习优化系统
增强Skill职能化，学习写作技巧
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

VERSION = "5.0"
SYSTEM_NAME = "NWACS Skill联网学习优化系统"

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
# Skill定义与学习主题
# ============================================================================

SKILL_DEFINITIONS = {
    "世界观构造师": {
        "description": "构建完整的小说世界体系",
        "functions": ["世界规则设定", "大陆体系构建", "势力分布设计", "历史背景编写"],
        "learning_topics": [
            "玄幻世界构建技巧",
            "世界规则一致性维护",
            "历史架空背景构建",
            "地域特色体现"
        ]
    },
    "剧情构造师": {
        "description": "设计精彩的故事情节",
        "functions": ["情节设计", "伏笔埋设", "节奏控制", "高潮设计"],
        "learning_topics": [
            "三幕式结构设计",
            "悬疑反转设计技巧",
            "伏笔埋设与回收",
            "剧情节奏控制"
        ]
    },
    "角色塑造师": {
        "description": "塑造生动的人物形象",
        "functions": ["人物设定", "性格刻画", "成长弧线", "关系网络"],
        "learning_topics": [
            "角色性格刻画方法",
            "人物动机设定",
            "角色成长弧光设计",
            "人物关系网络构建"
        ]
    },
    "战斗设计师": {
        "description": "设计精彩的战斗场景",
        "functions": ["招式设计", "场面描写", "战斗节奏", "能力对决"],
        "learning_topics": [
            "战斗场景描写技巧",
            "招式命名艺术",
            "战斗节奏控制",
            "特殊能力对决设计"
        ]
    },
    "场景构造师": {
        "description": "描绘逼真的场景环境",
        "functions": ["环境描写", "氛围营造", "空间布局", "场景转换"],
        "learning_topics": [
            "环境氛围营造",
            "感官细节描写",
            "空间布局设计",
            "地域特色体现"
        ]
    },
    "对话设计师": {
        "description": "创作生动的人物对话",
        "functions": ["对话设计", "个性塑造", "潜台词", "情感表达"],
        "learning_topics": [
            "对话个性塑造",
            "潜台词设计",
            "对话节奏控制",
            "情感对话描写"
        ]
    },
    "写作技巧大师": {
        "description": "提供专业写作指导",
        "functions": ["风格定位", "修辞运用", "视角选择", "节奏控制"],
        "learning_topics": [
            "风格定位与统一",
            "修辞手法运用",
            "叙事视角选择",
            "去AI化写作方法"
        ]
    },
    "去AI痕迹监督官": {
        "description": "检测并去除AI写作痕迹",
        "functions": ["AI检测", "人类化改造", "风格优化", "质量评估"],
        "learning_topics": [
            "AI痕迹识别技巧",
            "自然语言优化",
            "人类风格模拟",
            "文本质量评估"
        ]
    },
    "质量审计师": {
        "description": "审核小说质量",
        "functions": ["质量评估", "结构检查", "逻辑验证", "体验优化"],
        "learning_topics": [
            "小说质量评估标准",
            "结构完整性检查",
            "人物一致性检查",
            "读者体验优化"
        ]
    },
    "词汇大师": {
        "description": "提供丰富的词汇素材",
        "functions": ["词汇收集", "描写素材", "风格优化", "修辞丰富"],
        "learning_topics": [
            "词汇收集与整理",
            "描写素材积累",
            "语言风格优化",
            "修辞丰富度提升"
        ]
    }
}

# ============================================================================
# DeepSeek API调用
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
# 更新Skill文件
# ============================================================================

SKILL_FILE_MAP = {
    '世界观构造师': 'skills/level2/03_二级Skill_世界观构造师.md',
    '剧情构造师': 'skills/level2/04_二级Skill_剧情构造师.md',
    '角色塑造师': 'skills/level2/07_二级Skill_角色塑造师.md',
    '战斗设计师': 'skills/level2/08_二级Skill_战斗设计师.md',
    '场景构造师': 'skills/level2/05_二级Skill_场景构造师.md',
    '对话设计师': 'skills/level2/06_二级Skill_对话设计师.md',
    '写作技巧大师': 'skills/level2/09_二级Skill_写作技巧大师.md',
    '去AI痕迹监督官': 'skills/level2/10_二级Skill_去AI痕迹监督官.md',
    '质量审计师': 'skills/level2/11_二级Skill_质量审计师.md',
    '词汇大师': 'skills/level2/32_二级Skill_词汇大师.md',
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
        # 创建新文件，包含Skill定义
        skill_def = SKILL_DEFINITIONS.get(skill_name, {})
        existing_content = f"""# {skill_name}
{'='*60}

## 职能描述
{skill_def.get('description', '暂无描述')}

## 核心职能
"""
        for func in skill_def.get('functions', []):
            existing_content += f"- {func}\n"
        existing_content += "\n## 学习主题\n"
        for topic in skill_def.get('learning_topics', []):
            existing_content += f"- {topic}\n"
        existing_content += "\n"
    
    # 添加学习内容
    chapter_title = f"\n\n## 联网学习成果 - {datetime.now().strftime('%Y-%m-%d')}\n"
    
    # 检查是否已存在相同内容
    if chapter_title in existing_content:
        print(f"⏭️ 跳过（内容已存在）: {skill_name}")
        return False
    
    chapter_content = chapter_title + content
    chapter_content += "\n---\n*本章节由DeepSeek联网学习系统自动生成*\n"
    
    existing_content += chapter_content
    
    # 保存
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(existing_content)
    
    print(f"✅ 更新成功: {skill_name}")
    return True

# ============================================================================
# 主学习流程
# ============================================================================

def start_learning():
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║           {SYSTEM_NAME} v{VERSION}                           ║
║                                                              ║
║           🎯 学习目标:                                        ║
║           1. 增强Skill职能化                                 ║
║           2. 学习写作技巧                                     ║
║           3. 联网优化内容库                                   ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # 检查配置
    config = load_config()
    if not config.get('api_key'):
        print("❌ API Key未配置！")
        return
    
    updated_count = 0
    
    # 为每个Skill进行联网学习
    for skill_name, skill_def in SKILL_DEFINITIONS.items():
        print(f"\n{'='*60}")
        print(f"🎯 正在优化: {skill_name}")
        print(f"📋 描述: {skill_def['description']}")
        print(f"{'='*60}")
        
        # 构建学习提示
        topics = skill_def['learning_topics']
        functions = skill_def['functions']
        
        prompt = f"""请为【{skill_name}】提供详细的学习内容，增强其职能化。

## 职能描述
{skill_def['description']}

## 核心职能
{', '.join(functions)}

## 需要学习的主题
{chr(10).join([f"- {t}" for t in topics])}

## 请提供以下内容：
1. **核心概念**: 该职能的核心定义和重要性
2. **实用技巧**: 具体的操作方法和技巧
3. **案例分析**: 实际例子和分析
4. **进阶方法**: 高级技巧和进阶应用
5. **常见问题**: 常见错误和解决方法

请用清晰、结构化的方式输出！"""
        
        # 调用DeepSeek学习
        content = call_deepseek_v4(prompt)
        
        if content:
            if update_skill_file(skill_name, content):
                updated_count += 1
        else:
            print(f"❌ 学习失败: {skill_name}")
    
    # 生成报告
    generate_report(updated_count)

def generate_report(updated_count):
    print(f"\n{'='*60}")
    print("📋 生成学习报告...")
    print(f"{'='*60}")
    
    report = f"""# NWACS Skill联网学习报告
{'='*60}
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 🎯 学习目标
1. 增强Skill职能化
2. 学习写作技巧
3. 联网优化内容库

## ✅ 学习成果

### 更新的Skill列表

"""
    
    for skill_name, skill_def in SKILL_DEFINITIONS.items():
        report += f"""#### {skill_name}
- **描述**: {skill_def['description']}
- **职能**: {', '.join(skill_def['functions'])}
- **学习主题**: {', '.join(skill_def['learning_topics'])}

"""
    
    report += f"""

## 📂 更新的文件

"""
    
    for skill_name, filepath in SKILL_FILE_MAP.items():
        report += f"- {skill_name}: {filepath}\n"
    
    report += f"""

## 📊 统计信息
- 总Skill数: {len(SKILL_DEFINITIONS)}
- 更新成功: {updated_count}
- 更新失败: {len(SKILL_DEFINITIONS) - updated_count}
- 更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 💡 职能化增强

每个Skill现在具备以下职能：
- **世界观构造师**: 世界规则设定、大陆体系构建、势力分布设计、历史背景编写
- **剧情构造师**: 情节设计、伏笔埋设、节奏控制、高潮设计
- **角色塑造师**: 人物设定、性格刻画、成长弧线、关系网络
- **战斗设计师**: 招式设计、场面描写、战斗节奏、能力对决
- **场景构造师**: 环境描写、氛围营造、空间布局、场景转换
- **对话设计师**: 对话设计、个性塑造、潜台词、情感表达
- **写作技巧大师**: 风格定位、修辞运用、视角选择、节奏控制
- **去AI痕迹监督官**: AI检测、人类化改造、风格优化、质量评估
- **质量审计师**: 质量评估、结构检查、逻辑验证、体验优化
- **词汇大师**: 词汇收集、描写素材、风格优化、修辞丰富

{'='*60}
报告结束
"""
    
    # 保存报告
    os.makedirs('learning', exist_ok=True)
    report_path = f'learning/Skill联网学习报告_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✅ 报告已保存: {report_path}")
    
    # 打印总结
    print("\n" + "="*60)
    print("🎉 Skill联网学习优化完成！")
    print("="*60)
    print(f"\n📊 更新统计:")
    print(f"   ✅ 更新了 {updated_count}/{len(SKILL_DEFINITIONS)} 个Skill")
    print(f"   ✅ 增强了Skill职能化")
    print(f"   ✅ 学习了写作技巧")
    print(f"\n📂 学习报告: {report_path}")

if __name__ == "__main__":
    start_learning()
