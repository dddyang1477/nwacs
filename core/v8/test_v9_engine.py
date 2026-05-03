#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试NWACS V9.0一体化引擎
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("="*70)
print("🧪 NWACS V9.0 一体化引擎测试")
print("="*70)

# 初始化引擎
try:
    from nwacs_unified_engine import NWACSUnifiedEngine
    engine = NWACSUnifiedEngine()
    print("\n✅ 引擎初始化成功！")
    
    # 列出工作流
    print("\n📋 可用工作流：")
    for wf in engine.list_workflows():
        print(f'   📝 {wf["name"]}: {wf["description"]}')
    
    # 列出技能
    print(f"\n🎯 可用技能数：{len(engine.list_skills())}个")
    
except Exception as e:
    print(f"\n❌ 初始化失败：{e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70)
print("🎉 测试完成！")
print("="*70)
