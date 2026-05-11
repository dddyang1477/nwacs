#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 全网对比评测报告
对比对象: Sudowrite / NovelAI / FeelFish / 百度作家平台 / Novelcrafter
评测维度: 10大核心维度 x 5级评分制
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Any, Tuple

# ================================================================
# 评测维度定义
# ================================================================

DIMENSIONS = {
    "memory": "长文本记忆与一致性",
    "worldbuilding": "世界观构建与管理",
    "character": "角色管理与深度塑造",
    "plot": "剧情构思与大纲设计",
    "style": "风格模仿与文笔优化",
    "learning": "自学习与知识进化",
    "collaboration": "人机协作与交互体验",
    "multimodal": "多模态能力(文生图/封面)",
    "platform": "多平台发布与生态",
    "localization": "中文网文适配度",
}

# ================================================================
# 竞品数据 (基于2025-2026全网搜索)
# ================================================================

COMPETITORS = {
    "Sudowrite": {
        "url": "https://sudowrite.com",
        "pricing": "$22-44/月",
        "model": "Muse 1.5 自研小说专用模型",
        "scores": {
            "memory": 8.5,
            "worldbuilding": 9.0,
            "character": 9.0,
            "plot": 9.5,
            "style": 9.0,
            "learning": 5.0,
            "collaboration": 8.5,
            "multimodal": 3.0,
            "platform": 4.0,
            "localization": 3.0,
        },
        "strengths": [
            "Story Bible: 集中管理角色/世界观/大纲",
            "Canvas: 无限画布可视化剧情规划",
            "Muse 1.5: 自研小说专用LLM，理解场景节奏/对话韵律",
            "Scene-level drafting with beat-by-beat control",
            "Rewrite: 行级编辑与风格调整",
            "Chapter Continuity: 跨章节一致性",
        ],
        "weaknesses": [
            "中文支持极弱，几乎不可用",
            "无自学习/知识进化能力",
            "无多平台发布功能",
            "价格较高，按credits计费复杂",
            "无文生图能力",
        ],
    },
    "NovelAI": {
        "url": "https://novelai.net",
        "pricing": "$10-25/月",
        "model": "Kayra 自研故事模型 + 动漫图像生成",
        "scores": {
            "memory": 7.5,
            "worldbuilding": 8.0,
            "character": 7.0,
            "plot": 5.0,
            "style": 8.5,
            "learning": 3.0,
            "collaboration": 7.0,
            "multimodal": 9.0,
            "platform": 3.0,
            "localization": 2.0,
        },
        "strengths": [
            "Lorebook: 触发式世界设定注入上下文",
            "AI Modules: 风格模仿模块化",
            "强大的AI动漫图像生成",
            "Memory + Author's Note 双重上下文控制",
            "价格相对亲民",
        ],
        "weaknesses": [
            "无剧情大纲/结构设计工具",
            "中文支持极弱",
            "无自学习能力",
            "Lorebook管理复杂，需手动维护",
            "无多平台发布",
        ],
    },
    "FeelFish 飞鱼": {
        "url": "https://www.feelfish.com",
        "pricing": "免费+会员制",
        "model": "DeepSeek/GPT-4o/Gemini等多模型",
        "scores": {
            "memory": 8.0,
            "worldbuilding": 8.5,
            "character": 8.0,
            "plot": 7.5,
            "style": 7.5,
            "learning": 4.0,
            "collaboration": 8.5,
            "multimodal": 6.0,
            "platform": 5.0,
            "localization": 9.0,
        },
        "strengths": [
            "中文原生支持，网文适配度最高",
            "设定严守机制: 自动校验人设/战力一致性",
            "逻辑扫描: 自动标识内容矛盾并标红",
            "对话式交互，沉浸式创作体验",
            "一键构建角色&世界观",
            "支持9大主流模型集成",
            "Windows + macOS 桌面端",
        ],
        "weaknesses": [
            "无自学习/知识进化能力",
            "剧情构思深度不足",
            "文生图能力有限",
            "无伏笔管理系统",
            "无多平台一键发布",
        ],
    },
    "百度作家平台": {
        "url": "https://writers.baidu.com",
        "pricing": "免费",
        "model": "文心一言 + 百度百科知识库",
        "scores": {
            "memory": 6.0,
            "worldbuilding": 6.5,
            "character": 6.0,
            "plot": 7.0,
            "style": 6.5,
            "learning": 3.0,
            "collaboration": 7.0,
            "multimodal": 5.0,
            "platform": 9.5,
            "localization": 9.5,
        },
        "strengths": [
            "对接百度文库/百度百科资源库",
            "一键发布起点中文网/番茄小说等主流平台",
            "内置多种题材创作模板",
            "智能纠错功能",
            "完全免费",
            "新手引导教程完善",
        ],
        "weaknesses": [
            "长文本记忆能力弱",
            "世界观/角色管理深度不足",
            "AI生成内容同质化严重",
            "无自学习能力",
            "深度创作能力有限",
        ],
    },
    "Novelcrafter": {
        "url": "https://novelcrafter.com",
        "pricing": "$8-24/月",
        "model": "OpenAI/Claude/OpenRouter多模型",
        "scores": {
            "memory": 7.0,
            "worldbuilding": 7.5,
            "character": 7.5,
            "plot": 6.5,
            "style": 7.0,
            "learning": 3.0,
            "collaboration": 7.5,
            "multimodal": 2.0,
            "platform": 3.0,
            "localization": 4.0,
        },
        "strengths": [
            "Codex: 灵活的世界设定管理系统",
            "支持多种LLM后端切换",
            "开放API，可自定义工作流",
            "价格适中",
        ],
        "weaknesses": [
            "中文支持有限",
            "无自学习能力",
            "无剧情可视化",
            "无多平台发布",
            "社区较小",
        ],
    },
}

# ================================================================
# NWACS 自评
# ================================================================

NWACS_SELF = {
    "url": "https://github.com/dddyang1477/nwacs",
    "pricing": "开源免费",
    "model": "DeepSeek API + 本地知识库",
    "scores": {
        "memory": 8.5,
        "worldbuilding": 7.5,
        "character": 8.0,
        "plot": 8.0,
        "style": 7.5,
        "learning": 9.0,
        "collaboration": 7.0,
        "multimodal": 1.0,
        "platform": 1.0,
        "localization": 9.5,
    },
    "strengths": [
        "🎯 唯一具备自学习/知识进化能力的工具",
        "📚 100+本经典书籍技法深度提炼(1098条知识)",
        "🧠 8项核心技能全部专家级以上(最高宗师)",
        "📝 长篇小说记忆一致性验证(风格指纹/伏笔/人物)",
        "🔮 中国传统命名系统(五行八卦+百家姓400+姓氏)",
        "🎭 剧情构思引擎(12种弧线类型+多题材适配)",
        "🔍 三层AI检测+去痕系统",
        "💰 完全开源免费",
        "🇨🇳 中文原生，网文深度适配",
    ],
    "weaknesses": [
        "❌ 无GUI界面，纯命令行/Python API",
        "❌ 无文生图/封面生成能力",
        "❌ 无多平台一键发布功能",
        "❌ 无可视化剧情规划(Canvas类)",
        "❌ 无桌面客户端/移动端",
        "❌ 依赖外部DeepSeek API",
        "❌ 无协作/多人写作功能",
        "❌ 无版本管理/历史回溯",
    ],
}

# ================================================================
# 差距分析与改进建议
# ================================================================

GAP_ANALYSIS = [
    {
        "gap": "可视化剧情规划 (Canvas)",
        "priority": "P0-核心",
        "competitor": "Sudowrite Canvas 9.5分",
        "nwacs_current": "纯文本大纲，无可视化",
        "solution": "开发PlotCanvas模块: 无限画布+场景卡片+拖拽排序+AI建议",
        "effort": "高",
        "impact": "极高",
    },
    {
        "gap": "GUI/Web界面",
        "priority": "P0-核心",
        "competitor": "所有竞品均有GUI",
        "nwacs_current": "纯命令行/Python API",
        "solution": "FastAPI + Vue3 构建Web界面，或Streamlit快速原型",
        "effort": "高",
        "impact": "极高",
    },
    {
        "gap": "多平台一键发布",
        "priority": "P1-重要",
        "competitor": "百度作家平台 9.5分",
        "nwacs_current": "无发布功能",
        "solution": "对接起点/番茄/纵横等平台API，格式化导出",
        "effort": "中",
        "impact": "高",
    },
    {
        "gap": "文生图/封面生成",
        "priority": "P1-重要",
        "competitor": "NovelAI 9.0分",
        "nwacs_current": "无图像能力",
        "solution": "集成Stable Diffusion API或ComfyUI工作流",
        "effort": "中",
        "impact": "中",
    },
    {
        "gap": "Story Bible集中管理",
        "priority": "P1-重要",
        "competitor": "Sudowrite Story Bible 9.0分",
        "nwacs_current": "分散在各模块中",
        "solution": "统一StoryBible模块: 角色/世界观/大纲/伏笔一站式管理",
        "effort": "中",
        "impact": "高",
    },
    {
        "gap": "版本管理与历史回溯",
        "priority": "P2-增强",
        "competitor": "Sudowrite/FeelFish",
        "nwacs_current": "无版本管理",
        "solution": "Git-based版本管理 + 章节快照 + 回滚功能",
        "effort": "低",
        "impact": "中",
    },
    {
        "gap": "协作/多人写作",
        "priority": "P2-增强",
        "competitor": "部分竞品支持",
        "nwacs_current": "单人模式",
        "solution": "WebSocket实时协作 + 角色权限管理",
        "effort": "高",
        "impact": "中",
    },
    {
        "gap": "移动端适配",
        "priority": "P2-增强",
        "competitor": "FeelFish桌面端",
        "nwacs_current": "无客户端",
        "solution": "PWA或React Native移动端",
        "effort": "高",
        "impact": "中",
    },
    {
        "gap": "Lorebook触发式设定注入",
        "priority": "P2-增强",
        "competitor": "NovelAI Lorebook 8.0分",
        "nwacs_current": "手动上下文管理",
        "solution": "自动触发式设定注入: 关键词→自动加载相关设定到上下文",
        "effort": "低",
        "impact": "高",
    },
    {
        "gap": "AI Modules风格模块化",
        "priority": "P2-增强",
        "competitor": "NovelAI AI Modules 8.5分",
        "nwacs_current": "风格指纹检测但无模块化切换",
        "solution": "风格模块市场: 预训练风格包+一键切换+自定义训练",
        "effort": "中",
        "impact": "高",
    },
]

# ================================================================
# 综合评分计算
# ================================================================

def calculate_total(scores: Dict[str, float]) -> float:
    weights = {
        "memory": 0.15,
        "worldbuilding": 0.12,
        "character": 0.12,
        "plot": 0.12,
        "style": 0.10,
        "learning": 0.10,
        "collaboration": 0.08,
        "multimodal": 0.05,
        "platform": 0.08,
        "localization": 0.08,
    }
    return sum(scores[k] * weights[k] for k in weights)

# ================================================================
# 雷达图数据生成
# ================================================================

def generate_report() -> str:
    lines = []
    sep = "=" * 80
    sub = "-" * 60

    lines.append(sep)
    lines.append("  NWACS 全网对比评测报告")
    lines.append(f"  生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"  对比对象: Sudowrite | NovelAI | FeelFish | 百度作家平台 | Novelcrafter")
    lines.append(sep)

    # ---- 综合排名 ----
    lines.append("\n📊 一、综合评分排名 (10维加权)")
    lines.append(sub)

    all_scores = {}
    for name, data in COMPETITORS.items():
        all_scores[name] = calculate_total(data["scores"])
    all_scores["NWACS"] = calculate_total(NWACS_SELF["scores"])

    ranked = sorted(all_scores.items(), key=lambda x: x[1], reverse=True)
    medals = ["🥇", "🥈", "🥉", "  ", "  ", "  "]
    for i, (name, score) in enumerate(ranked):
        bar = "█" * int(score * 2) + "░" * (20 - int(score * 2))
        lines.append(f"  {medals[i]} {i+1}. {name:20s} | {score:.2f}/10 | [{bar}]")

    # ---- 各维度详细对比 ----
    lines.append(f"\n📋 二、10大维度详细对比")
    lines.append(sub)

    for dim_key, dim_name in DIMENSIONS.items():
        lines.append(f"\n  【{dim_name}】")
        dim_scores = {}
        for name, data in COMPETITORS.items():
            dim_scores[name] = data["scores"][dim_key]
        dim_scores["NWACS"] = NWACS_SELF["scores"][dim_key]

        ranked_dim = sorted(dim_scores.items(), key=lambda x: x[1], reverse=True)
        for j, (name, score) in enumerate(ranked_dim):
            marker = "⭐" if name == "NWACS" else "  "
            bar = "▓" * int(score) + "░" * (10 - int(score))
            lines.append(f"    {marker} {j+1}. {name:20s} [{bar}] {score:.1f}/10")

    # ---- NWACS优势 ----
    lines.append(f"\n🎯 三、NWACS 核心优势 (不可替代性)")
    lines.append(sub)
    for i, s in enumerate(NWACS_SELF["strengths"], 1):
        lines.append(f"  {i}. {s}")

    # ---- NWACS劣势 ----
    lines.append(f"\n⚠️ 四、NWACS 核心短板 (需优先解决)")
    lines.append(sub)
    for i, w in enumerate(NWACS_SELF["weaknesses"], 1):
        lines.append(f"  {i}. {w}")

    # ---- 差距分析 ----
    lines.append(f"\n🔧 五、差距分析与改进路线图")
    lines.append(sub)

    for gap in GAP_ANALYSIS:
        lines.append(f"\n  [{gap['priority']}] {gap['gap']}")
        lines.append(f"    竞品标杆: {gap['competitor']}")
        lines.append(f"    当前状态: {gap['nwacs_current']}")
        lines.append(f"    解决方案: {gap['solution']}")
        lines.append(f"    投入: {gap['effort']} | 收益: {gap['impact']}")

    # ---- 改进优先级 ----
    lines.append(f"\n📅 六、改进优先级路线图")
    lines.append(sub)

    roadmap = [
        ("Phase 1 (立即)", [
            "Lorebook触发式设定注入 → 2天",
            "Story Bible集中管理模块 → 3天",
            "AI风格模块化切换 → 3天",
            "版本管理/历史回溯 → 2天",
        ]),
        ("Phase 2 (本周)", [
            "FastAPI后端 + Streamlit快速原型 → 5天",
            "多平台格式化导出(起点/番茄) → 3天",
            "PlotCanvas基础版(HTML5 Canvas) → 5天",
        ]),
        ("Phase 3 (本月)", [
            "Vue3完整Web界面 → 15天",
            "Stable Diffusion封面生成集成 → 5天",
            "WebSocket实时协作 → 10天",
        ]),
    ]

    for phase_name, tasks in roadmap:
        lines.append(f"\n  ▶ {phase_name}")
        for task in tasks:
            lines.append(f"    ☐ {task}")

    # ---- 最终结论 ----
    lines.append(f"\n📝 七、最终结论")
    lines.append(sub)
    lines.append(f"""
  NWACS在"自学习进化"和"中文网文适配"两个维度上具有不可替代的
  竞争优势。其1098条书籍技法知识库+8项专家级技能的组合，在市面上
  没有任何竞品能够匹敌。

  但NWACS在"用户体验层"存在严重短板：
  - 无可视化界面 → 普通用户无法使用
  - 无剧情画布 → 复杂剧情规划困难
  - 无发布功能 → 创作闭环不完整

  建议策略：
  1. 短期(1周): 补齐Lorebook/StoryBible/版本管理 → 巩固核心优势
  2. 中期(1月): Streamlit原型+PlotCanvas → 降低使用门槛
  3. 长期(3月): Vue3完整界面+发布+封面 → 完整创作闭环

  核心竞争力定位：
  "唯一具备自学习进化能力的中文网文AI写作系统"
""")

    return "\n".join(lines)


if __name__ == "__main__":
    report = generate_report()
    print(report)

    # 保存报告
    report_path = os.path.join(os.path.dirname(__file__), "_competitive_report.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"\n📁 报告已保存: {report_path}")
