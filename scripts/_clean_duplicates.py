#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""清理第一轮重组脚本产生的重复文件"""
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(BASE, "skills")

def safe_delete(path):
    if os.path.exists(path):
        os.remove(path)
        print(f"  🗑️ {os.path.basename(path)}")
        return True
    return False

# level1 重复: 删除 01_小说总调度官.md (保留 02_一级Skill_小说总调度官.md)
safe_delete(os.path.join(SKILLS, "level1", "01_小说总调度官.md"))
safe_delete(os.path.join(SKILLS, "level1", "README.md"))

# level2 重复: 删除第一轮脚本创建的新格式文件 (保留原始 0X_二级Skill_*.md)
level2 = os.path.join(SKILLS, "level2")
new_format_files = [
    "01_世界观构造师.md", "02_剧情构造师.md", "03_场景构造师.md",
    "04_对话设计师.md", "05_角色塑造师.md", "06_战斗设计师.md",
    "07_写作技巧大师.md", "08_去AI痕迹监督官.md", "09_质量审计师.md",
    "10_选题策划大师.md", "11_大纲架构师.md", "12_节奏控制大师.md",
    "13_情感共鸣师.md", "14_一键AI消痕师.md", "15_市场分析师.md",
    "16_AI工作流大师.md", "17_IP运营师.md", "18_小说拆书师.md",
    "19_数据分析师.md", "20_描写增强师.md", "21_版权保护师.md",
    "22_市场分析师_扩展.md", "23_创新灵感生成器.md", "24_读者心理分析师.md",
    "25_发布规划师.md", "26_学习大师.md", "27_规则掌控者.md",
    "28_词汇大师.md", "29_题材选择大师.md", "30_短篇小说爽文大师.md",
]

for f in new_format_files:
    safe_delete(os.path.join(level2, f))

print("\n✅ 重复文件清理完成")

# 最终统计
for sub in ["level1", "level2", "level3", "masters", "scripts", "references"]:
    d = os.path.join(SKILLS, sub)
    if os.path.isdir(d):
        count = len(os.listdir(d))
        print(f"  📁 {sub}/ : {count} 项")
