#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS Skill连通性修复工具
建立Skill之间的关联，形成完整的创作系统
"""

import os
import sys
import re
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

VERSION = "1.0"

# ============================================================================
# Skill关联定义
# ============================================================================

SKILL_CONNECTIONS = {
    "世界观构造师": {
        "description": "构建小说世界的基础框架",
        "provides": ["世界规则", "大陆体系", "势力分布", "历史背景"],
        "requires": [],
        "connects_to": ["剧情构造师", "场景构造师", "角色塑造师"],
        "example_ref": "根据【世界观构造师】设定的{世界规则}，设计【剧情构造师】中的势力冲突"
    },
    
    "剧情构造师": {
        "description": "设计故事情节和叙事结构",
        "provides": ["情节设计", "伏笔埋设", "节奏控制", "高潮设计"],
        "requires": ["世界观构造师"],
        "connects_to": ["角色塑造师", "战斗设计师", "场景构造师"],
        "example_ref": "根据【剧情构造师】设计的{情节}，让【角色塑造师】调整人物成长轨迹"
    },
    
    "角色塑造师": {
        "description": "塑造人物形象和性格",
        "provides": ["人物设定", "性格刻画", "成长弧线", "关系网络"],
        "requires": ["世界观构造师", "剧情构造师"],
        "connects_to": ["对话设计师", "战斗设计师"],
        "example_ref": "根据【角色塑造师】的{人物关系}，设计【对话设计师】的对话风格"
    },
    
    "战斗设计师": {
        "description": "设计战斗场景和动作描写",
        "provides": ["招式设计", "场面描写", "战斗节奏", "能力对决"],
        "requires": ["角色塑造师"],
        "connects_to": ["场景构造师", "剧情构造师"],
        "example_ref": "根据【战斗设计师】的{战斗}，让【场景构造师】设计战斗环境"
    },
    
    "场景构造师": {
        "description": "描绘环境和氛围",
        "provides": ["环境描写", "氛围营造", "空间布局", "场景转换"],
        "requires": ["世界观构造师"],
        "connects_to": ["战斗设计师", "剧情构造师"],
        "example_ref": "根据【场景构造师】的{场景}，配合【战斗设计师】描写战斗氛围"
    },
    
    "对话设计师": {
        "description": "创作人物对话",
        "provides": ["对话设计", "个性塑造", "潜台词", "情感表达"],
        "requires": ["角色塑造师"],
        "connects_to": ["写作技巧大师", "情感共鸣师"],
        "example_ref": "根据【对话设计师】的{对话}，让【写作技巧大师】优化语言风格"
    },
    
    "写作技巧大师": {
        "description": "提供写作指导和质量把控",
        "provides": ["风格定位", "修辞运用", "视角选择", "节奏控制"],
        "requires": ["对话设计师", "场景构造师"],
        "connects_to": ["去AI痕迹监督官", "质量审计师"],
        "example_ref": "根据【写作技巧大师】的{技巧}，让【去AI痕迹监督官】检查AI痕迹"
    },
    
    "去AI痕迹监督官": {
        "description": "检测和去除AI写作痕迹",
        "provides": ["AI检测", "人类化改造", "风格优化", "质量评估"],
        "requires": ["写作技巧大师"],
        "connects_to": ["质量审计师"],
        "example_ref": "【去AI痕迹监督官】优化后提交给【质量审计师】最终审核"
    },
    
    "质量审计师": {
        "description": "审核小说质量",
        "provides": ["质量评估", "结构检查", "逻辑验证", "体验优化"],
        "requires": ["写作技巧大师", "去AI痕迹监督官"],
        "connects_to": [],
        "example_ref": "【质量审计师】是最后一道关卡，确保作品质量"
    },
    
    "词汇大师": {
        "description": "提供丰富的词汇素材",
        "provides": ["词汇收集", "描写素材", "风格优化", "修辞丰富"],
        "requires": [],
        "connects_to": ["写作技巧大师", "场景构造师", "对话设计师"],
        "example_ref": "【词汇大师】为【写作技巧大师】提供丰富的词汇支持"
    },
    
    "选题策划大师": {
        "description": "分析市场趋势策划选题",
        "provides": ["热点追踪", "题材创新", "市场定位", "平台分析"],
        "requires": ["市场分析师"],
        "connects_to": ["大纲架构师", "剧情构造师"],
        "example_ref": "根据【选题策划大师】的{选题}，让【大纲架构师】设计大纲"
    },
    
    "大纲架构师": {
        "description": "设计长篇大纲结构",
        "provides": ["长篇结构", "情节串联", "逻辑闭环", "支线设计"],
        "requires": ["选题策划大师"],
        "connects_to": ["剧情构造师", "角色塑造师"],
        "example_ref": "【大纲架构师】设计大纲后，交给【剧情构造师】细化情节"
    },
    
    "节奏控制大师": {
        "description": "控制故事节奏",
        "provides": ["爽点设计", "节奏把控", "高潮安排", "悬念设置"],
        "requires": ["剧情构造师"],
        "connects_to": ["情感共鸣师", "写作技巧大师"],
        "example_ref": "【节奏控制大师】设计的节奏，配合【情感共鸣师】增强读者体验"
    },
    
    "情感共鸣师": {
        "description": "触动读者情感",
        "provides": ["共情写作", "情绪调动", "情感铺垫", "共鸣设计"],
        "requires": ["角色塑造师", "节奏控制大师"],
        "connects_to": ["写作技巧大师", "对话设计师"],
        "example_ref": "【情感共鸣师】设计的情感，配合【对话设计师】展现人物内心"
    },
    
    "市场分析师": {
        "description": "分析市场趋势",
        "provides": ["平台分析", "读者画像", "爆款分析", "趋势预测"],
        "requires": [],
        "connects_to": ["选题策划大师", "IP运营师", "数据分析师"],
        "example_ref": "【市场分析师】提供数据支持给【选题策划大师】"
    },
    
    "IP运营师": {
        "description": "IP开发和粉丝运营",
        "provides": ["衍生开发", "粉丝运营", "品牌建设", "版权保护"],
        "requires": ["市场分析师"],
        "connects_to": ["数据分析师"],
        "example_ref": "【IP运营师】根据【数据分析师】的数据制定运营策略"
    },
    
    "数据分析师": {
        "description": "数据分析驱动优化",
        "provides": ["阅读数据", "留存分析", "优化策略", "AB测试"],
        "requires": ["市场分析师"],
        "connects_to": ["IP运营师"],
        "example_ref": "【数据分析师】分析数据后反馈给【IP运营师】优化策略"
    }
}

# ============================================================================
# 修复Skill文件
# ============================================================================

def get_skill_filename(skill_name):
    """获取Skill文件名"""
    mapping = {
        "世界观构造师": "03_二级Skill_世界观构造师.md",
        "剧情构造师": "04_二级Skill_剧情构造师.md",
        "角色塑造师": "07_二级Skill_角色塑造师.md",
        "战斗设计师": "08_二级Skill_战斗设计师.md",
        "场景构造师": "05_二级Skill_场景构造师.md",
        "对话设计师": "06_二级Skill_对话设计师.md",
        "写作技巧大师": "09_二级Skill_写作技巧大师.md",
        "去AI痕迹监督官": "10_二级Skill_去AI痕迹监督官.md",
        "质量审计师": "11_二级Skill_质量审计师.md",
        "词汇大师": "32_二级Skill_词汇大师.md",
        "选题策划大师": "12_二级Skill_选题策划大师.md",
        "大纲架构师": "13_二级Skill_大纲架构师.md",
        "节奏控制大师": "14_二级Skill_节奏控制大师.md",
        "情感共鸣师": "15_二级Skill_情感共鸣师.md",
        "市场分析师": "16_二级Skill_市场分析师.md",
        "IP运营师": "17_二级Skill_IP运营师.md",
        "数据分析师": "18_二级Skill_数据分析师.md"
    }
    return mapping.get(skill_name)

def fix_skill_file(skill_name, skill_info):
    """修复单个Skill文件，建立连通性"""
    filename = get_skill_filename(skill_name)
    if not filename:
        return False, f"未找到文件名映射: {skill_name}"
    
    filepath = f'skills/level2/{filename}'
    
    if not os.path.exists(filepath):
        return False, f"Skill文件不存在: {filepath}"
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已有关联部分
        if '## Skill关联网络' in content:
            return True, "已有关联部分，跳过"
        
        # 构建关联部分
        connections_section = f"""

## Skill关联网络

### 核心职能
{skill_info['description']}

### 提供能力
"""
        
        for item in skill_info['provides']:
            connections_section += f"- **{item}**：本Skill提供的核心能力\n"
        
        if skill_info['requires']:
            connections_section += "\n### 依赖Skill\n"
            for req in skill_info['requires']:
                connections_section += f"- 【{req}】：本Skill需要的基础能力支持\n"
        
        if skill_info['connects_to']:
            connections_section += "\n### 协作Skill\n"
            for conn in skill_info['connects_to']:
                connections_section += f"- 【{conn}】：与本Skill协作的Skill\n"
        
        if skill_info['example_ref']:
            connections_section += f"\n### 协作示例\n"
            connections_section += f"{skill_info['example_ref']}\n"
        
        # 协作流程
        connections_section += "\n### 推荐创作流程\n"
        connections_section += "1. 【世界观构造师】构建基础框架\n"
        connections_section += "2. 【剧情构造师】设计情节结构\n"
        connections_section += "3. 【角色塑造师】塑造人物形象\n"
        connections_section += "4. 【大纲架构师】设计长篇大纲\n"
        connections_section += "5. 【场景构造师】描绘环境氛围\n"
        connections_section += "6. 【战斗设计师】设计战斗场景\n"
        connections_section += "7. 【对话设计师】创作人物对话\n"
        connections_section += "8. 【写作技巧大师】优化写作技巧\n"
        connections_section += "9. 【去AI痕迹监督官】去除AI痕迹\n"
        connections_section += "10. 【质量审计师】最终质量审核\n"
        
        # 添加到文件末尾
        content += connections_section
        
        # 保存
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True, "关联已添加"
    
    except Exception as e:
        return False, f"修复失败: {str(e)}"

# ============================================================================
# 创建Skill协作总览文件
# ============================================================================

def create_collaboration_overview():
    """创建Skill协作总览文件"""
    overview = """# NWACS Skill协作总览

## 系统架构

NWACS小说创作系统由多个专业Skill组成，形成完整的创作流水线。

## Skill分类

### 核心创作Skill
- 世界观构造师、剧情构造师、角色塑造师、战斗设计师、场景构造师、对话设计师

### 技巧优化Skill
- 写作技巧大师、去AI痕迹监督官、质量审计师、词汇大师

### 商业化Skill
- 选题策划大师、大纲架构师、节奏控制大师、情感共鸣师

### 运营分析Skill
- 市场分析师、IP运营师、数据分析师

## 协作关系图

```
[市场分析师] → [选题策划大师] → [大纲架构师]
                                    ↓
                            [剧情构造师]
                                    ↓
[世界观构造师] → [角色塑造师] → [对话设计师] → [写作技巧大师]
                                    ↓                    ↓
                            [场景构造师]        [去AI痕迹监督官]
                                    ↓                    ↓
                            [战斗设计师]        [质量审计师]
```

## 创作流程

1. **市场分析**：市场分析师分析趋势
2. **选题策划**：选题策划大师确定题材
3. **世界观构建**：世界观构造师设计世界
4. **大纲设计**：大纲架构师设计长篇结构
5. **情节设计**：剧情构造师设计具体情节
6. **角色塑造**：角色塑造师塑造人物
7. **场景描绘**：场景构造师描绘环境
8. **战斗设计**：战斗设计师设计战斗
9. **对话创作**：对话设计师创作对话
10. **技巧优化**：写作技巧大师优化技巧
11. **去AI痕迹**：去AI痕迹监督官检查
12. **质量审计**：质量审计师最终审核

## Skill能力矩阵

| Skill | 世界观 | 情节 | 人物 | 场景 | 对话 | 技巧 |
|-------|--------|------|------|------|------|------|
| 世界观构造师 | ★ | ○ | ○ | ★ | ○ | ○ |
| 剧情构造师 | ○ | ★ | ★ | ○ | ○ | ○ |
| 角色塑造师 | ○ | ★ | ★ | ○ | ★ | ○ |
| 场景构造师 | ★ | ○ | ○ | ★ | ○ | ○ |
| 战斗设计师 | ○ | ★ | ○ | ★ | ○ | ○ |
| 对话设计师 | ○ | ○ | ★ | ○ | ★ | ○ |
| 写作技巧大师 | ○ | ○ | ○ | ○ | ★ | ★ |

★=核心能力 ○=辅助能力

---
*更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    filepath = 'skills/level2/00_Skill协作总览.md'
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(overview)
    
    return filepath

# ============================================================================
# 主流程
# ============================================================================

def main():
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║           Skill连通性修复工具 v{VERSION}                          ║
║                                                              ║
║           🔗 建立Skill之间的关联                               ║
║           📋 形成完整的创作系统                                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    success_count = 0
    fail_count = 0
    
    print("\n🔧 正在修复Skill文件...\n")
    
    for skill_name, skill_info in SKILL_CONNECTIONS.items():
        success, message = fix_skill_file(skill_name, skill_info)
        
        if success:
            print(f"✅ {skill_name}: {message}")
            success_count += 1
        else:
            print(f"❌ {skill_name}: {message}")
            fail_count += 1
    
    print(f"\n📊 修复统计: {success_count} 成功, {fail_count} 失败")
    
    # 创建协作总览
    print("\n📋 创建Skill协作总览文件...")
    overview_path = create_collaboration_overview()
    print(f"✅ 总览文件已创建: {overview_path}")
    
    print("\n" + "="*60)
    print("🎉 Skill连通性修复完成！")
    print("="*60)
    
    print("\n📋 修复内容：")
    print("   ✅ 添加了每个Skill的关联网络")
    print("   ✅ 明确了Skill之间的依赖关系")
    print("   ✅ 建立了Skill之间的协作流程")
    print("   ✅ 创建了Skill协作总览文件")
    print("\n🔗 现在所有Skill都连接在一起了！")

if __name__ == "__main__":
    main()
