#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
强制输出测试脚本
"""
import sys

# 强制刷新输出
def print_flush(msg):
    print(msg, flush=True)

print_flush("="*60)
print_flush("🔵 测试脚本开始")
print_flush("="*60)
print_flush(f"Python版本: {sys.version.split()[0]}")
print_flush(f"脚本路径: {__file__}")
print_flush("")

# 测试循环
print_flush("🔵 开始循环...")
for i in range(5):
    print_flush(f"   [{i+1}/5] 测试中...")
    import time
    time.sleep(1)

print_flush("")
print_flush("✅ 测试完成！")
print_flush("="*60)
