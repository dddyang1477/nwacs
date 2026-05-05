#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""最终修复 level2/level3 编号"""
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(BASE, "skills")

def ren(src, dst):
    if os.path.exists(src) and not os.path.exists(dst):
        os.rename(src, dst)
        print(f"  ✅ {os.path.basename(src)} -> {os.path.basename(dst)}")
    elif os.path.exists(dst):
        print(f"  ⚠️ 目标已存在: {os.path.basename(dst)}")

level2 = os.path.join(SKILLS, "level2")

# 消除重复编号，使编号连续 03-32
renames = [
    ("22_二级Skill_创新灵感生成器.md", "25_二级Skill_创新灵感生成器.md"),
    ("23_二级Skill_读者心理分析师.md", "26_二级Skill_读者心理分析师.md"),
    ("24_二级Skill_发布规划师.md", "27_二级Skill_发布规划师.md"),
    ("30_二级Skill_学习大师.md", "28_二级Skill_学习大师.md"),
    ("30_二级Skill_短篇小说爽文大师.md", "29_二级Skill_短篇小说爽文大师.md"),
    ("31_二级Skill_规则掌控者.md", "30_二级Skill_规则掌控者.md"),
    ("32_二级Skill_词汇大师.md", "31_二级Skill_词汇大师.md"),
    ("40_二级Skill_题材选择大师.md", "32_二级Skill_题材选择大师.md"),
]

for old, new in renames:
    ren(os.path.join(level2, old), os.path.join(level2, new))

# 验证: 检查是否还有重复编号
print("\n验证 level2 编号:")
files = sorted([f for f in os.listdir(level2) if f[0].isdigit() and f.endswith(".md")])
nums = {}
for f in files:
    num = f.split("_")[0]
    if num not in nums:
        nums[num] = []
    nums[num].append(f)

has_dup = False
for num, fs in sorted(nums.items()):
    if len(fs) > 1:
        print(f"  ❌ 编号 {num} 重复: {fs}")
        has_dup = True

if not has_dup:
    print(f"  ✅ 无重复编号，共 {len(nums)} 个Skill")
    for num, fs in sorted(nums.items()):
        print(f"     {num}: {fs[0]}")

print("\n✅ 完成")
