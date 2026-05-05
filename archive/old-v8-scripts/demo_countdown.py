#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 倒计时功能演示脚本
快速展示v2.0的新功能
"""

import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("="*60)
print("     NWACS 自动学习系统 v2.0 - 功能演示")
print("="*60)
print()

print("📋 新增功能:")
print("   ✅ 空闲倒计时显示")
print("   ✅ 学习冷却倒计时")
print("   ✅ 系统预热倒计时")
print("   ✅ 每秒更新状态")
print()
print("="*60)
print("⏳ 系统预热倒计时（3秒）")
print("="*60)

def format_time(seconds):
    """格式化时间显示"""
    if seconds >= 3600:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    elif seconds >= 60:
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"
    else:
        return f"{int(seconds):02d}秒"

# 演示预热倒计时
for i in range(3, 0, -1):
    print(f"\r⏳ 系统预热中... {format_time(i)}", end='', flush=True)
    time.sleep(1)

print("\n")
print("="*60)
print("⏱️  空闲倒计时演示（10秒）")
print("="*60)
print(" 提示: 请保持10秒不操作鼠标键盘来观察效果！")
print()

for i in range(10, 0, -1):
    status = "活跃" if i % 2 == 0 else "空闲"
    
    if status == "活跃":
        idle_display = f"⏱️ 距学习触发 {format_time(i)}"
    else:
        idle_display = f"⏳ 已空闲 {format_time(10-i)}"
    
    # 冷却状态交替
    cooldown = i * 100 if i > 5 else 0
    if cooldown > 0:
        cooldown_display = f" | 🛑 冷却 {format_time(cooldown)}"
    else:
        cooldown_display = " | ✅ 就绪"
    
    print(f"\r{status:^8} | {idle_display} {cooldown_display}", end='', flush=True)
    time.sleep(1)

print("\n")
print("="*60)
print("🚀 倒计时功能演示完成！")
print("="*60)
print()
print("💡 使用方式:")
print("   1. 运行完整监控: py auto_idle_learning.py")
print("   2. 或双击: 启动自动学习.bat")
print()
print("⏱️ 说明:")
print("   - 系统预热: 启动后等待30秒")
print("   - 空闲触发: 10分钟无操作自动学习")
print("   - 冷却间隔: 两次学习之间间隔1小时")
print()
print("="*60)
