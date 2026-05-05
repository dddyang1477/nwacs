#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 新增Skill优化系统
添加顶级签约作者需要的核心技能
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

VERSION = "6.0"
SYSTEM_NAME = "NWACS 新增Skill优化系统"

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
# 新增Skill定义
# ============================================================================

NEW_SKILLS = {
    "选题策划大师": {
        "description": "分析市场趋势，策划热门选题，提高签约成功率",
        "functions": ["热点追踪", "题材创新", "市场定位", "平台分析"],
        "learning_topics": [
            "2025-2026年热门题材分析",
            "爆款选题规律总结",
            "平台偏好与读者画像",
            "创新题材与差异化定位"
        ]
    },
    "大纲架构师": {
        "description": "设计完整的大纲结构，确保长篇故事逻辑闭环",
        "functions": ["长篇结构规划", "情节串联", "逻辑闭环", "支线设计"],
        "learning_topics": [
            "三幕式结构设计",
            "英雄之旅模板应用",
            "多线并行叙事技巧",
            "支线与主线的呼应"
        ]
    },
    "节奏控制大师": {
        "description": "控制故事节奏，保持读者阅读兴趣",
        "functions": ["爽点设计", "节奏把控", "高潮安排", "悬念设置"],
        "learning_topics": [
            "网文爽点设计公式",
            "节奏快慢的交替运用",
            "高潮与低谷的布局",
            "悬念与解谜的节奏"
        ]
    },
    "情感共鸣师": {
        "description": "触动读者情感，产生强烈代入感",
        "functions": ["共情写作", "情绪调动", "情感铺垫", "共鸣设计"],
        "learning_topics": [
            "情感共鸣的触发机制",
            "情绪调动的写作技巧",
            "虐点与爽点的平衡",
            "读者心理预期管理"
        ]
    },
    "市场分析师": {
        "description": "分析市场趋势和读者需求，指导创作方向",
        "functions": ["平台分析", "读者画像", "爆款分析", "趋势预测"],
        "learning_topics": [
            "各大平台偏好分析",
            "爆款文的共同特征",
            "读者年龄段与喜好",
            "未来趋势预测方法"
        ]
    },
    "IP运营师": {
        "description": "IP开发与粉丝运营，提升作品商业价值",
        "functions": ["衍生开发", "粉丝运营", "品牌建设", "版权保护"],
        "learning_topics": [
            "IP衍生开发方向",
            "粉丝互动与运营",
            "个人品牌建设",
            "版权保护与授权"
        ]
    },
    "数据分析师": {
        "description": "数据分析驱动创作优化",
        "functions": ["阅读数据", "留存分析", "优化策略", "AB测试"],
        "learning_topics": [
            "关键数据指标解读",
            "留存率分析方法",
            "数据驱动的优化策略",
            "实验与假设验证"
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
# 创建Skill文件
# ============================================================================

SKILL_FILE_MAP = {
    '选题策划大师': 'skills/level2/12_二级Skill_选题策划大师.md',
    '大纲架构师': 'skills/level2/13_二级Skill_大纲架构师.md',
    '节奏控制大师': 'skills/level2/14_二级Skill_节奏控制大师.md',
    '情感共鸣师': 'skills/level2/15_二级Skill_情感共鸣师.md',
    '市场分析师': 'skills/level2/16_二级Skill_市场分析师.md',
    'IP运营师': 'skills/level2/17_二级Skill_IP运营师.md',
    '数据分析师': 'skills/level2/18_二级Skill_数据分析师.md',
}

def create_skill_file(skill_name, content):
    filepath = SKILL_FILE_MAP.get(skill_name)
    
    if not filepath:
        filepath = f'skills/{skill_name}.md'
    
    if not os.path.isabs(filepath):
        filepath = os.path.join(os.path.dirname(__file__), filepath)
    
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    skill_def = NEW_SKILLS.get(skill_name, {})
    
    # 创建新文件内容
    new_content = f"""# {skill_name}
{'='*60}

## 职能描述
{skill_def.get('description', '暂无描述')}

## 核心职能
"""
    
    for func in skill_def.get('functions', []):
        new_content += f"- {func}\n"
    
    new_content += f"""
## 学习主题
"""
    
    for topic in skill_def.get('learning_topics', []):
        new_content += f"- {topic}\n"
    
    new_content += f"""
## 联网学习成果 - {datetime.now().strftime('%Y-%m-%d')}

{content}

---
*本章节由DeepSeek联网学习系统自动生成*
"""
    
    # 保存
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ 创建成功: {skill_name}")
    return True

# ============================================================================
# 主流程
# ============================================================================

def start_creation():
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║           {SYSTEM_NAME} v{VERSION}                           ║
║                                                              ║
║           🎯 新增目标:                                        ║
║           1. 选题策划大师                                     ║
║           2. 大纲架构师                                      ║
║           3. 节奏控制大师                                    ║
║           4. 情感共鸣师                                      ║
║           5. 市场分析师                                      ║
║           6. IP运营师                                        ║
║           7. 数据分析师                                      ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # 检查配置
    config = load_config()
    if not config.get('api_key'):
        print("❌ API Key未配置！")
        return
    
    created_count = 0
    
    # 创建每个Skill
    for skill_name, skill_def in NEW_SKILLS.items():
        print(f"\n{'='*60}")
        print(f"🎯 正在创建: {skill_name}")
        print(f"📋 描述: {skill_def['description']}")
        print(f"{'='*60}")
        
        # 构建学习提示
        topics = skill_def['learning_topics']
        functions = skill_def['functions']
        
        prompt = f"""请为【{skill_name}】提供详细的专业内容。

## 职能描述
{skill_def['description']}

## 核心职能
{', '.join(functions)}

## 需要学习的主题
{chr(10).join([f"- {t}" for t in topics])}

## 请提供以下内容：
1. **核心概念**: 该职能的核心定义和重要性
2. **实用技巧**: 具体的操作方法和技巧
3. **案例分析**: 实际例子和分析（结合网络小说案例）
4. **进阶方法**: 高级技巧和进阶应用
5. **常见问题**: 常见错误和解决方法
6. **行业洞察**: 作为顶级签约作者的经验分享

请用清晰、结构化的方式输出！"""
        
        # 调用DeepSeek学习
        content = call_deepseek_v4(prompt)
        
        if content:
            if create_skill_file(skill_name, content):
                created_count += 1
        else:
            print(f"❌ 创建失败: {skill_name}")
    
    # 生成报告
    generate_report(created_count)

def generate_report(created_count):
    print(f"\n{'='*60}")
    print("📋 生成创建报告...")
    print(f"{'='*60}")
    
    report = f"""# NWACS 新增Skill报告
{'='*60}
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 🎯 新增目标
1. 选题策划大师
2. 大纲架构师
3. 节奏控制大师
4. 情感共鸣师
5. 市场分析师
6. IP运营师
7. 数据分析师

## ✅ 创建成果

"""
    
    for skill_name, skill_def in NEW_SKILLS.items():
        report += f"""### {skill_name}
- **描述**: {skill_def['description']}
- **职能**: {', '.join(skill_def['functions'])}
- **学习主题**: {', '.join(skill_def['learning_topics'])}

"""
    
    report += f"""

## 📂 创建的文件

"""
    
    for skill_name, filepath in SKILL_FILE_MAP.items():
        report += f"- {skill_name}: {filepath}\n"
    
    report += f"""

## 📊 统计信息
- 总Skill数: {len(NEW_SKILLS)}
- 创建成功: {created_count}
- 创建失败: {len(NEW_SKILLS) - created_count}
- 创建时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 💡 能力增强

新增的7个Skill大幅增强了NWACS的商业化能力：

### 内容创作能力
- **选题策划大师**: 热点追踪、题材创新、市场定位
- **大纲架构师**: 长篇结构规划、情节串联
- **节奏控制大师**: 爽点设计、节奏把控
- **情感共鸣师**: 共情写作、情绪调动

### 商业化能力
- **市场分析师**: 平台分析、读者画像、爆款分析
- **IP运营师**: 衍生开发、粉丝运营、品牌建设
- **数据分析师**: 阅读数据、留存分析、优化策略

{'='*60}
报告结束
"""
    
    # 保存报告
    os.makedirs('learning', exist_ok=True)
    report_path = f'learning/新增Skill报告_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✅ 报告已保存: {report_path}")
    
    # 打印总结
    print("\n" + "="*60)
    print("🎉 新增Skill创建完成！")
    print("="*60)
    print(f"\n📊 创建统计:")
    print(f"   ✅ 创建了 {created_count}/{len(NEW_SKILLS)} 个新Skill")
    print(f"   ✅ 内容创作能力大幅增强")
    print(f"   ✅ 商业化能力全面提升")
    print(f"\n📂 创建报告: {report_path}")

if __name__ == "__main__":
    start_creation()
