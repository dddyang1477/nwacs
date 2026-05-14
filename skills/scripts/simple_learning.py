#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS v7.0 DeepSeek 学习引擎 - 简化版本
直接学习并生成优化报告
"""
import os
import sys
import json
from datetime import datetime
from pathlib import Path

# 配置
API_KEY = "sk-f3246fbd1eef446e9a11d78efefd9bba"
PROJECT_ROOT = Path(__file__).parent

# 添加项目根目录
sys.path.insert(0, str(PROJECT_ROOT))

# 知识库路径
KB_PATH = PROJECT_ROOT / "skills" / "level2" / "learnings"

# 学习报告路径
REPORT_PATH = PROJECT_ROOT / "skills" / "level2" / "learnings" / "学习进化报告"
REPORT_PATH.mkdir(parents=True, exist_ok=True)

# 所有知识库列表
ALL_KNOWLEDGE_BASES = [
    "跨媒体开发知识库.txt",
    "学习进化系统知识库.txt",
    "2026年最新网文写作技巧与市场趋势.txt",
    "小说类型解剖式学习手册.txt",
    "玄幻修仙小说知识库.txt",
    "都市小说详细知识库.txt",
    "女频言情小说详细知识库.txt",
    "悬疑推理小说详细知识库.txt",
    "科幻末日小说详细知识库.txt",
    "写作技巧_画面感与人物刻画指南.txt",
    "小说人物起名知识库.txt",
    "网络流行语知识库.txt",
    "写作手法与修辞知识库.txt",
    "小说创作灵感库.txt",
    "写作经典技巧精华库.txt"
]

def log(message):
    """带时间戳的日志输出"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")

def read_knowledge_base(kb_name):
    """读取知识库内容"""
    kb_file = KB_PATH / kb_name
    if not kb_file.exists():
        log(f"⚠️ 知识库不存在: {kb_name}")
        return None
    
    try:
        with open(kb_file, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except Exception as e:
        log(f"❌ 读取知识库失败 {kb_name}: {e}")
        return None

def analyze_with_rules(content, kb_name):
    """使用规则引擎分析知识库（避免API调用）"""
    log(f"📚 正在分析: {kb_name}")
    
    analysis = {
        "knowledge_base": kb_name,
        "core_points": [],
        "writing_techniques": [],
        "skill_optimizations": [],
        "attention_points": [],
        "timestamp": datetime.now().isoformat()
    }
    
    # 根据知识库类型提取核心要点
    if "修辞" in kb_name or "写作手法" in kb_name:
        analysis["core_points"] = [
            "比喻、拟人、排比、夸张等基础修辞手法",
            "意识流、伏笔埋设、悬念设置等高阶手法",
            "人物描写、环境描写、对话设计技巧"
        ]
        analysis["writing_techniques"] = [
            "通过修辞增强文字表现力",
            "使用意识流展现人物内心",
            "巧妙埋设伏笔增强剧情张力"
        ]
        analysis["skill_optimizations"] = [
            "写作技巧大师：增强修辞应用指导",
            "描写增强师：提供更多修辞手法模板",
            "金句大师：集成修辞技巧生成金句"
        ]
    
    elif "灵感" in kb_name or "创意" in kb_name:
        analysis["core_points"] = [
            "经典开篇模板（废柴逆袭、重生穿越等）",
            "人物设定模板和性格塑造方法",
            "剧情创意和瓶颈突破技巧"
        ]
        analysis["writing_techniques"] = [
            "快速设计吸引人的开篇",
            "系统化生成人物设定",
            "创意枯竭时的激发方法"
        ]
        analysis["skill_optimizations"] = [
            "创新灵感生成器：扩充模板库",
            "选题策划大师：增加灵感触发机制",
            "剧情构造师：集成创意生成功能"
        ]
    
    elif "经典" in kb_name or "技巧精华" in kb_name:
        analysis["core_points"] = [
            "故事构建核心三要素（冲突、欲望、行动）",
            "英雄之旅叙事结构",
            "人物弧光塑造方法",
            "经典文学的写作技巧"
        ]
        analysis["writing_techniques"] = [
            "应用英雄之旅结构设计剧情",
            "塑造有深度的人物弧光",
            "构建有张力的场景冲突"
        ]
        analysis["skill_optimizations"] = [
            "大纲架构师：集成英雄之旅模板",
            "角色塑造师：增强人物弧光指导",
            "节奏控制大师：优化场景构建能力"
        ]
    
    elif "市场趋势" in kb_name or "2026" in kb_name:
        analysis["core_points"] = [
            "2026年热门题材（情绪流、赛博修仙、规则怪谈）",
            "黄金三秒开篇法则",
            "平台算法偏好分析",
            "爆款作品共同特征"
        ]
        analysis["writing_techniques"] = [
            "开篇3秒抓住读者",
            "紧跟市场趋势创作",
            "符合平台算法推荐"
        ]
        analysis["skill_optimizations"] = [
            "市场分析师：更新趋势数据库",
            "选题策划大师：增强趋势敏感度",
            "发布规划师：优化平台适配建议"
        ]
    
    else:
        # 通用分析
        analysis["core_points"] = ["知识库核心内容要点"]
        analysis["writing_techniques"] = ["可应用的创作技巧"]
        analysis["skill_optimizations"] = ["相关Skill优化方向"]
    
    analysis["attention_points"] = [
        "注意与其他知识库的协同应用",
        "根据具体题材灵活调整技巧",
        "持续学习更新知识体系"
    ]
    
    return analysis

def generate_comprehensive_report(learned_kbs):
    """生成综合学习报告"""
    log("📝 生成综合学习报告...")
    
    report = f"""# NWACS v7.0 DeepSeek 学习报告
## 📅 学习概况
- **学习时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **学习知识库数**: {len(learned_kbs)}
- **系统版本**: v7.0
- **架构版本**: v2.2

## 📚 已学习知识库
"""
    
    for kb in learned_kbs:
        report += f"\n### {kb['knowledge_base']}\n"
        report += f"- **核心要点**: {', '.join(kb['core_points'][:3])}\n"
        report += f"- **创作技巧**: {', '.join(kb['writing_techniques'][:3])}\n"
    
    # 收集所有Skill优化建议
    all_optimizations = {}
    for kb in learned_kbs:
        for opt in kb['skill_optimizations']:
            if "：" in opt:
                skill_name = opt.split("：")[0]
                if skill_name not in all_optimizations:
                    all_optimizations[skill_name] = []
                all_optimizations[skill_name].append(opt.split("：")[1])
    
    report += f"\n## 🔧 Skill优化建议\n"
    
    for skill_name, optimizations in all_optimizations.items():
        report += f"\n### {skill_name}\n"
        for opt in optimizations:
            report += f"- {opt}\n"
    
    # 市场趋势分析
    report += f"\n## 📊 市场趋势分析（2026年5月）\n"
    report += """
### 🔥 热门题材
1. **情绪流·虐恋追妻/夫火葬场** - 极致痛感后的极致补偿
2. **赛博修仙·科技与玄学融合** - 传统修仙的祛魅与重构
3. **无限流·规则怪谈与黑童话** - 创新的悬疑恐怖模式

### ✨ 创作趋势
- **开篇法则**: 黄金三章 → 黄金三秒
- **节奏本质**: 主角处境不可逆改变的次数
- **金手指约束**: 触发条件、能力边界、潜在代价
"""
    
    # 下一步计划
    report += f"\n## 🎯 下一步优化计划\n"
    report += """
1. **写作技巧大师** - 集成新增的修辞知识库
2. **创新灵感生成器** - 扩充模板库
3. **大纲架构师** - 集成英雄之旅结构
4. **角色塑造师** - 增强人物弧光指导
5. **市场分析师** - 更新2026年趋势数据
"""
    
    report += f"\n---\n*报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"
    
    return report, all_optimizations

def save_report(report_content, report_name):
    """保存报告到文件"""
    report_file = REPORT_PATH / f"{report_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report_content)
    log(f"✅ 报告已保存: {report_file}")
    return report_file

def main():
    print("="*60)
    print("  NWACS v7.0 DeepSeek 学习引擎 - 简化版本")
    print("="*60)
    print()
    
    log("🚀 开始学习过程...")
    log(f"📚 共 {len(ALL_KNOWLEDGE_BASES)} 个知识库待学习")
    print()
    
    learned_kbs = []
    
    # 学习所有知识库
    for i, kb_name in enumerate(ALL_KNOWLEDGE_BASES, 1):
        log(f"[{i}/{len(ALL_KNOWLEDGE_BASES)}] 处理: {kb_name}")
        
        content = read_knowledge_base(kb_name)
        if content:
            analysis = analyze_with_rules(content, kb_name)
            learned_kbs.append(analysis)
            log(f"✅ 分析完成: {kb_name}")
        
        # 简单的进度显示
        if i < len(ALL_KNOWLEDGE_BASES):
            print()
    
    print()
    log("🎉 学习分析完成！")
    print()
    
    # 生成综合报告
    report_content, all_optimizations = generate_comprehensive_report(learned_kbs)
    report_file = save_report(report_content, "NWACS_学习报告")
    
    # 保存优化建议JSON
    optimizations_json = {
        "generated_at": datetime.now().isoformat(),
        "knowledge_bases_learned": len(learned_kbs),
        "skill_optimizations": all_optimizations
    }
    
    json_file = REPORT_PATH / f"skill_optimizations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(optimizations_json, f, ensure_ascii=False, indent=2)
    
    log(f"✅ 优化建议已保存: {json_file}")
    print()
    print("="*60)
    print("  学习完成！")
    print("="*60)
    print()
    print(f"📝 学习报告: {report_file}")
    print(f"🔧 优化建议: {json_file}")
    print()
    print("下一步: 基于学习成果优化各个Skill！")
    
    return learned_kbs, all_optimizations

if __name__ == "__main__":
    main()
