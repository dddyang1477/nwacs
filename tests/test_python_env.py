#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
极简版NWACS服务器测试
诊断问题
"""
import sys
print("="*60)
print("Python测试")
print("="*60)
print(f"Python版本: {sys.version}")
print(f"Python路径: {sys.executable}")
print()

# 测试导入
print("测试模块导入...")
try:
    import json
    print("✅ json")
except:
    print("❌ json")

try:
    import time
    print("✅ time")
except:
    print("❌ time")

try:
    from http.server import HTTPServer
    print("✅ HTTPServer")
except:
    print("❌ HTTPServer")

try:
    from http.server import BaseHTTPRequestHandler
    print("✅ BaseHTTPRequestHandler")
except:
    print("❌ BaseHTTPRequestHandler")

print()
print("测试完成")
