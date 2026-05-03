#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""V8模块导入测试"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("="*60)
print("🔍 V8模块导入测试")
print("="*60)

print("\n1. 测试 advanced_writing_techniques...")
try:
    from advanced_writing_techniques import AdvancedWritingTechniques, WritingSkill
    print("   ✅ AdvancedWritingTechniques 导入成功")
    print(f"   ✅ WritingSkill 数量: {len([s for s in WritingSkill])}")
except Exception as e:
    print(f"   ❌ 导入失败: {e}")

print("\n2. 测试 bestseller_analyzer...")
try:
    from bestseller_analyzer import BestsellerAnalyzer, HotspotType
    print("   ✅ BestsellerAnalyzer 导入成功")
    analyzer = BestsellerAnalyzer()
    print(f"   ✅ 写作公式数量: {len(analyzer.formulas)}")
    print(f"   ✅ 爆款套路数量: {len(analyzer.patterns)}")
except Exception as e:
    print(f"   ❌ 导入失败: {e}")

print("\n3. 测试 WritingSkill 枚举...")
try:
    for skill in WritingSkill:
        print(f"   • {skill.value}: {skill.name}")
except Exception as e:
    print(f"   ❌ 枚举测试失败: {e}")

print("\n" + "="*60)
print("✅ 测试完成")
print("="*60)
