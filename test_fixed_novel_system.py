#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试修复后的小说生成系统
"""
import sys
from pathlib import Path

# 添加 core 目录到路径
sys.path.insert(0, str(Path(__file__).parent / "core"))

print("="*60)
print("测试 NWACS 小说生成系统修复验证")
print("="*60)
print()

from novel_project_manager import NovelProjectManager

print("1️⃣ 第一次测试：创建新项目...")
print()
# 第一次测试 - 新项目，清除旧数据
manager1 = NovelProjectManager("测试新小说1", reset_project=True)
manager1.generate_world_framework()
manager1.generate_character_framework()
manager1.generate_plot_framework()

prot1 = manager1.character_framework.protagonist
prot_name1 = prot1.get('name', 'N/A')
world1 = manager1.world_framework.world_name

print()
print("="*60)
print()

print("2️⃣ 第二次测试：创建另一个新项目...")
print()
# 第二次测试 - 另一个新项目，验证随机不同的数据
manager2 = NovelProjectManager("测试新小说2", reset_project=True)
manager2.generate_world_framework()
manager2.generate_character_framework()
manager2.generate_plot_framework()

prot2 = manager2.character_framework.protagonist
prot_name2 = prot2.get('name', 'N/A')
world2 = manager2.world_framework.world_name

print()
print("="*60)
print("📊 对比结果")
print("="*60)
print()

print(f"项目1:")
print(f"  - 世界名: {world1}")
print(f"  - 主角名: {prot_name1}")
print()

print(f"项目2:")
print(f"  - 世界名: {world2}")
print(f"  - 主角名: {prot_name2}")
print()

if prot_name1 != prot_name2 or world1 != world2:
    print("✅ 修复成功！两个项目有不同的名字和设定")
    print("   命名系统已正常工作！")
else:
    print("⚠️  可能存在问题，需要进一步检查")

print()
print("="*60)
print("🎉 系统修复验证完成！")
print("="*60)
