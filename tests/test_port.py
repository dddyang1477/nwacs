#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最简化测试脚本
"""
import sys
import socket

print("="*60)
print("测试脚本启动")
print("="*60)
print(f"Python: {sys.version}")
print(f"PID: {sys.pid}")
print()

# 测试端口
PORT = 8088
print(f"测试端口 {PORT}...")

# 检查端口是否被占用
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result = sock.connect_ex(('localhost', PORT))
if result == 0:
    print(f"❌ 端口 {PORT} 已被占用")
else:
    print(f"✅ 端口 {PORT} 可用")
sock.close()

print()
print("测试完成")
