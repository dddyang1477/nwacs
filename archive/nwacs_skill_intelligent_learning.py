#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS Skill智能学习系统
通过DeepSeek帮助每个Skill更新智能化
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

VERSION = "3.0"
SYSTEM_NAME = "Skill智能学习系统"

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
# Skill智能学习定义
# ============================================================================

SKILL_LEARNING_PLANS = {
    "世界观构造师": {
        "description": "构建完整的小说世界体系",
        "functions": ["世界规则设定", "大陆体系构建", "势力分布设计", "历史背景编写"],
        "intelligence_upgrades": [
            "增加世界构建的逻辑性检查功能",
            "完善世界规则的一致性验证",
            "增加历史背景的时间线生成",
            "增强势力关系的动态演化模拟",
            "添加世界设定的可视化展示功能"
        ],
        "humanization_upgrades": [
            "增加世界构建的示例模板",
            "添加更友好的提示词设计",
            "增强错误提示的引导性",
            "添加新手引导功能",
            "增加多种风格的世界设定选项"
        ]
    },
    
    "剧情构造师": {
        "description": "设计精彩的故事情节",
        "functions": ["情节设计", "伏笔埋设", "节奏控制", "高潮设计"],
        "intelligence_upgrades": [
            "增加情节逻辑的连贯性检查",
            "完善伏笔埋设和回收的自动检测",
            "添加节奏控制的智能建议",
            "增强高潮设计的多样性",
            "添加情节冲突的动态生成"
        ],
        "humanization_upgrades": [
            "增加多种情节模板库",
            "添加可视化的情节时间线",
            "增强伏笔追踪的直观展示",
            "添加情节节奏的调节建议",
            "增加新手友好的情节设计引导"
        ]
    },
    
    "角色塑造师": {
        "description": "塑造生动的人物形象",
        "functions": ["人物设定", "性格刻画", "成长弧线", "关系网络"],
        "intelligence_upgrades": [
            "增加人物性格的一致性检查",
            "完善人物成长弧线的逻辑验证",
            "添加人物关系的动态演化",
            "增强人物对话的个性化生成",
            "添加人物心理的深层分析"
        ],
        "humanization_upgrades": [
            "增加人物设定的示例模板库",
            "添加人物档案的可视化展示",
            "增强人物关系网络的图式展示",
            "添加人物对话的风格指南",
            "增加新手友好的人物设定引导"
        ]
    },
    
    "战斗设计师": {
        "description": "设计精彩的战斗场景",
        "functions": ["招式设计", "场面描写", "战斗节奏", "能力对决"],
        "intelligence_upgrades": [
            "增加战斗逻辑的合理性检查",
            "完善招式系统的一致性验证",
            "添加战斗节奏的智能调节",
            "增强战斗场景的动态渲染",
            "添加能力对决的平衡性分析"
        ],
        "humanization_upgrades": [
            "增加多种战斗模板库",
            "添加招式命名的创意提示",
            "增强战斗场景的描述示例",
            "添加战斗节奏的调节建议",
            "增加新手友好的战斗设计引导"
        ]
    },
    
    "场景构造师": {
        "description": "描绘逼真的场景环境",
        "functions": ["环境描写", "氛围营造", "空间布局", "场景转换"],
        "intelligence_upgrades": [
            "增加场景描写的画面感检查",
            "完善氛围营造的情绪一致性",
            "添加空间布局的合理性验证",
            "增强场景转换的流畅性优化",
            "添加场景信息的记忆化管理"
        ],
        "humanization_upgrades": [
            "增加场景描写的示例库",
            "添加氛围营造的情绪指南",
            "增强场景转换的衔接建议",
            "添加空间布局的可视化描述",
            "增加新手友好的场景设计引导"
        ]
    },
    
    "对话设计师": {
        "description": "创作生动的人物对话",
        "functions": ["对话设计", "个性塑造", "潜台词", "情感表达"],
        "intelligence_upgrades": [
            "增加对话个性化的一致性检查",
            "完善潜台词的深层含义分析",
            "添加对话节奏的智能调节",
            "增强情感表达的真实性验证",
            "添加对话信息的记忆化追踪"
        ],
        "humanization_upgrades": [
            "增加对话模板库",
            "添加个性说话风格指南",
            "增强潜台词设计的示例",
            "添加情感表达的提示词库",
            "增加新手友好的对话设计引导"
        ]
    },
    
    "写作技巧大师": {
        "description": "提供专业写作指导",
        "functions": ["风格定位", "修辞运用", "视角选择", "节奏控制"],
        "intelligence_upgrades": [
            "增加写作风格的自动识别",
            "完善修辞运用的合理建议",
            "添加视角选择的智能推荐",
            "增强节奏控制的动态调节",
            "添加写作技巧的个性化建议"
        ],
        "humanization_upgrades": [
            "增加写作风格的示例库",
            "添加修辞运用的案例详解",
            "增强视角选择的对比说明",
            "添加节奏控制的调节建议",
            "增加新手友好的写作指导"
        ]
    },
    
    "去AI痕迹监督官": {
        "description": "检测并去除AI写作痕迹",
        "functions": ["AI检测", "人类化改造", "风格优化", "质量评估"],
        "intelligence_upgrades": [
            "增加AI痕迹的智能检测",
            "完善人类化改造的智能建议",
            "添加风格优化的自动评估",
            "增强质量检查的多角度分析",
            "添加文本质量的评分系统"
        ],
        "humanization_upgrades": [
            "增加AI痕迹的检测示例库",
            "添加人类化改造的具体建议",
            "增强风格优化的对比展示",
            "添加质量评估的详细报告",
            "增加新手友好的检测引导"
        ]
    },
    
    "质量审计师": {
        "description": "审核小说质量",
        "functions": ["质量评估", "结构检查", "逻辑验证", "体验优化"],
        "intelligence_upgrades": [
            "增加质量评估的多角度分析",
            "完善结构检查的系统性审核",
            "添加逻辑验证的自动纠错",
            "增强体验优化的智能建议",
            "添加质量评分的可视化展示"
        ],
        "humanization_upgrades": [
            "增加质量评估的示例报告",
            "添加结构检查的清单模板",
            "增强逻辑验证的引导说明",
            "添加体验优化的建议列表",
            "增加新手友好的审核引导"
        ]
    },
    
    "词汇大师": {
        "description": "提供丰富的词汇素材",
        "functions": ["词汇收集", "描写素材", "风格优化", "修辞丰富"],
        "intelligence_upgrades": [
            "增加词汇库的智能分类",
            "完善描写素材的场景化推荐",
            "添加风格优化的个性化建议",
            "增强修辞运用的智能提示",
            "添加词汇记忆和学习系统"
        ],
        "humanization_upgrades": [
            "增加词汇分类的直观展示",
            "添加描写素材的示例库",
            "增强风格优化的对比效果",
            "添加修辞运用的案例说明",
            "增加新手友好的词汇学习"
        ]
    },
    
    "选题策划大师": {
        "description": "分析市场趋势，策划热门选题",
        "functions": ["热点追踪", "题材创新", "市场定位", "平台分析"],
        "intelligence_upgrades": [
            "增加热点趋势的智能分析",
            "完善题材创新的创意建议",
            "添加市场定位的智能评估",
            "增强平台分析的多角度比较",
            "添加选题策划的成功率预测"
        ],
        "humanization_upgrades": [
            "增加热点趋势的可视化展示",
            "添加题材创新的示例库",
            "增强市场定位的案例分析",
            "添加平台分析的对比报告",
            "增加新手友好的策划引导"
        ]
    },
    
    "大纲架构师": {
        "description": "设计完整的大纲结构",
        "functions": ["长篇结构规划", "情节串联", "逻辑闭环", "支线设计"],
        "intelligence_upgrades": [
            "增加大纲结构的完整性检查",
            "完善情节串联的逻辑验证",
            "添加逻辑闭环的自动检测",
            "增强支线设计的平衡性分析",
            "添加大纲结构的可视化展示"
        ],
        "humanization_upgrades": [
            "增加大纲结构的示例模板库",
            "添加情节串联的示例说明",
            "增强逻辑闭环的检查清单",
            "添加支线设计的平衡建议",
            "增加新手友好的大纲引导"
        ]
    },
    
    "节奏控制大师": {
        "description": "控制故事节奏，保持读者阅读兴趣",
        "functions": ["爽点设计", "节奏把控", "高潮安排", "悬念设置"],
        "intelligence_upgrades": [
            "增加爽点设计的智能建议",
            "完善节奏把控的动态调节",
            "添加高潮安排的时间线规划",
            "增强悬念设置的层次感设计",
            "添加阅读兴趣的动态分析"
        ],
        "humanization_upgrades": [
            "增加爽点设计的示例库",
            "添加节奏把控的调节指南",
            "增强高潮安排的案例分析",
            "添加悬念设置的设计技巧",
            "增加新手友好的节奏引导"
        ]
    },
    
    "情感共鸣师": {
        "description": "触动读者情感，产生强烈代入感",
        "functions": ["共情写作", "情绪调动", "情感铺垫", "共鸣设计"],
        "intelligence_upgrades": [
            "增加情感共鸣的智能分析",
            "完善情绪调动的节奏控制",
            "添加情感铺垫的层次设计",
            "增强共鸣设计的个性化建议",
            "添加读者反应的预测分析"
        ],
        "humanization_upgrades": [
            "增加情感共鸣的示例库",
            "添加情绪调动的案例分析",
            "增强情感铺垫的设计说明",
            "添加共鸣设计的实用建议",
            "增加新手友好的情感引导"
        ]
    },
    
    "市场分析师": {
        "description": "分析市场趋势和读者需求",
        "functions": ["平台分析", "读者画像", "爆款分析", "趋势预测"],
        "intelligence_upgrades": [
            "增加平台分析的智能比较",
            "完善读者画像的深度分析",
            "添加爆款分析的规律总结",
            "增强趋势预测的智能算法",
            "添加市场定位的智能建议"
        ],
        "humanization_upgrades": [
            "增加平台分析的对比报告",
            "添加读者画像的可视化展示",
            "增强爆款分析的案例详解",
            "添加趋势预测的直观图表",
            "增加新手友好的分析引导"
        ]
    },
    
    "IP运营师": {
        "description": "IP开发与粉丝运营，提升作品商业价值",
        "functions": ["衍生开发", "粉丝运营", "品牌建设", "版权保护"],
        "intelligence_upgrades": [
            "增加衍生开发的智能建议",
            "完善粉丝运营的策略分析",
            "添加品牌建设的形象设计",
            "增强版权保护的风险评估",
            "添加IP价值的动态评估"
        ],
        "humanization_upgrades": [
            "增加衍生开发的示例库",
            "添加粉丝运营的案例分析",
            "增强品牌建设的设计指南",
            "添加版权保护的实用建议",
            "增加新手友好的运营引导"
        ]
    },
    
    "数据分析师": {
        "description": "数据分析驱动创作优化",
        "functions": ["阅读数据", "留存分析", "优化策略", "AB测试"],
        "intelligence_upgrades": [
            "增加阅读数据的智能分析",
            "完善留存分析的深度解读",
            "添加优化策略的智能建议",
            "增强AB测试的结果分析",
            "添加数据驱动的创作优化"
        ],
        "humanization_upgrades": [
            "增加数据分析的可视化展示",
            "添加留存分析的案例说明",
            "增强优化策略的实用建议",
            "添加AB测试的设计指南",
            "增加新手友好的分析引导"
        ]
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
        system_prompt = """你是一位顶尖的AI技能优化专家，精通AI助手的人性化和智能化设计。
请用中文详细回答优化建议，提供具体的实现方案和示例！"""

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
# Skill文件更新
# ============================================================================

def update_skill_file(skill_name, skill_data):
    """更新单个Skill文件"""
    print(f"\n{'='*60}")
    print(f"🎯 正在优化Skill: {skill_name}")
    print(f"{'='*60}")
    
    # 构建学习提示
    prompt = f"""请作为顶尖的AI技能优化专家，为【{skill_name}】这个Skill提供全面的智能化和人性化升级方案。

【Skill基本信息】
- 描述：{skill_data['description']}
- 核心功能：{', '.join(skill_data['functions'])}

【智能化升级需求】
请针对以下方面提供详细的实现方案：
{chr(10).join([f'{i+1}. {upgrade}' for i, upgrade in enumerate(skill_data['intelligence_upgrades'])])}

【人性化升级需求】
请针对以下方面提供详细的实现方案：
{chr(10).join([f'{i+1}. {upgrade}' for i, upgrade in enumerate(skill_data['humanization_upgrades'])])}

【优化要求】
1. 请提供具体的实现代码或伪代码示例
2. 请增加更多用户友好的设计
3. 请提供新手引导和学习路径
4. 请增加错误处理和容错机制
5. 请添加示例库和模板功能
6. 请提供详细的使用说明

请用清晰的结构化方式输出！"""

    # 调用DeepSeek
    content = call_deepseek_v4(prompt)
    
    if content:
        # 保存学习成果
        save_skill_learning(skill_name, content)
        return True
    else:
        print(f"❌ {skill_name}优化失败！")
        return False

def save_skill_learning(skill_name, content):
    """保存Skill学习成果"""
    safe_name = ''.join(c for c in skill_name if c not in '\\/:*?"<>|')
    
    # 保存到Skill文件
    skill_file_path = f'skills/level2/skill_{safe_name}_智能升级.md'
    
    os.makedirs(os.path.dirname(skill_file_path), exist_ok=True)
    
    header = f"""# {skill_name} 智能升级报告
{'='*60}

## 📊 升级概况
- 升级时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- 升级系统：{SYSTEM_NAME} v{VERSION}

## 🎯 升级目标
"""
    
    with open(skill_file_path, 'w', encoding='utf-8') as f:
        f.write(header)
        f.write(content)
    
    print(f"✅ Skill升级文件已保存: {skill_file_path}")
    
    # 同时保存到learning目录
    os.makedirs('learning/skill_upgrades', exist_ok=True)
    learning_file = f'learning/skill_upgrades/{safe_name}_升级报告.md'
    
    with open(learning_file, 'w', encoding='utf-8') as f:
        f.write(header)
        f.write(content)
    
    print(f"✅ 学习文件已保存: {learning_file}")

# ============================================================================
# 主流程
# ============================================================================

def start_intelligent_learning():
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║           {SYSTEM_NAME} v{VERSION}                              ║
║                                                              ║
║           🤖 智能升级：使Skill更加智能化                        ║
║           💡 人性化设计：使Skill更加用户友好                    ║
║           📚 全面优化：共{len(SKILL_LEARNING_PLANS)}个Skill等待升级    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # 检查配置
    config = load_config()
    if not config.get('api_key'):
        print("❌ API Key未配置！")
        return
    
    success_count = 0
    total_count = len(SKILL_LEARNING_PLANS)
    
    # 依次优化每个Skill
    for skill_name, skill_data in SKILL_LEARNING_PLANS.items():
        if update_skill_file(skill_name, skill_data):
            success_count += 1
        
        print(f"\n📊 进度: {success_count}/{total_count} ({success_count*100//total_count}%)")
    
    # 生成总结报告
    generate_summary_report(success_count, total_count)

def generate_summary_report(success_count, total_count):
    print(f"\n{'='*60}")
    print("📋 生成总结报告...")
    print(f"{'='*60}")
    
    report = f"""# NWACS Skill智能升级总结报告
{'='*60}

## 📊 升级概况
- 升级时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- 升级系统：{SYSTEM_NAME} v{VERSION}
- 总Skill数：{total_count}
- 成功升级：{success_count}
- 成功率：{success_count*100//total_count}%

## 🤖 智能化升级
### 主要优化方向
1. 智能分析和建议功能
2. 自动化检查和验证
3. 记忆化和学习系统
4. 预测和推荐算法
5. 个性化定制

## 💡 人性化升级
### 主要优化方向
1. 新手友好引导
2. 直观可视化展示
3. 丰富的示例库
4. 详细的使用说明
5. 错误提示和修复建议

## 📚 升级的Skill列表
"""
    
    for skill_name in SKILL_LEARNING_PLANS.keys():
        report += f"- ✅ {skill_name}\n"
    
    report += f"""
## 🎯 下一步建议
1. 测试新升级的功能
2. 收集用户反馈
3. 根据反馈持续优化
4. 扩展更多技能
5. 建立学习社区

## 📂 文件位置
- Skill升级文件：skills/level2/skill_xxx_智能升级.md
- 学习报告：learning/skill_upgrades/

{'='*60}
报告结束
"""
    
    # 保存报告
    os.makedirs('learning', exist_ok=True)
    report_path = f'learning/Skill智能升级总结报告_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✅ 总结报告已保存: {report_path}")
    
    # 打印总结
    print("\n" + "="*60)
    print("🎉 Skill智能升级完成！")
    print("="*60)
    print(f"\n📊 升级统计:")
    print(f"   ✅ 成功升级 {success_count}/{total_count} 个Skill")
    print(f"   🤖 智能化提升完成")
    print(f"   💡 人性化设计完成")
    print(f"\n📂 报告位置: {report_path}")

if __name__ == "__main__":
    start_intelligent_learning()
