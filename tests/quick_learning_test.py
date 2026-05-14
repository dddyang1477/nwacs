#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 快速学习测试 - 立即运行学习并发送飞书通知
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

print("="*70)
print("🚀 NWACS 快速学习测试")
print("="*70)
print()

print("[1/3] 初始化系统...")
try:
    from core.comprehensive_learning import AutoLearningSystem
    print("   ✅ 模块加载成功")
except Exception as e:
    print(f"   ❌ 模块加载失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()
print("[2/3] 运行学习...")
try:
    learning = AutoLearningSystem()
    print("   ✅ 系统初始化成功")

    print()
    print("   正在执行学习...")
    learning.run_learning_cycle(update_skills=True)
    print("   ✅ 学习完成")

except Exception as e:
    print(f"   ❌ 学习失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()
print("[3/3] 检查飞书...")
if learning.feishu_integration:
    print("   ✅ 飞书集成已就绪")
else:
    print("   ⚠️ 飞书未初始化")

print()
print("="*70)
print("✅ 测试完成！")
print("请检查飞书群是否收到学习完成通知")
print("="*70)
