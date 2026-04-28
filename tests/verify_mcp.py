#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证MCP服务器是否正常工作
"""

import subprocess
import sys
import json

def test_mcp_server():
    """测试MCP服务器"""
    print("=== 测试MCP服务器 ===")
    
    # 启动MCP服务器
    proc = subprocess.Popen(
        [sys.executable, 'simple_mcp_server.py'],
        cwd='e:\\Program Files (x86)\\Trae CN\\github\\NWACS',
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding='utf-8'
    )
    
    try:
        # 等待服务器启动
        import time
        time.sleep(1)
        
        # 测试1: 获取服务描述
        print("\n1. 测试 describe 命令...")
        proc.stdin.write(json.dumps({"action": "describe"}) + "\n")
        proc.stdin.flush()
        
        response = proc.stdout.readline()
        print(f"   响应: {response.strip()}")
        
        # 测试2: 获取函数列表
        print("\n2. 测试 list_functions 命令...")
        proc.stdin.write(json.dumps({"action": "list_functions"}) + "\n")
        proc.stdin.flush()
        
        response = proc.stdout.readline()
        print(f"   响应: {response.strip()[:100]}...")
        
        # 测试3: 执行 generate_outline
        print("\n3. 测试 generate_outline 命令...")
        proc.stdin.write(json.dumps({
            "action": "execute",
            "name": "generate_outline",
            "arguments": {"genre": "玄幻修仙", "theme": "逆袭"}
        }) + "\n")
        proc.stdin.flush()
        
        response = proc.stdout.readline()
        print(f"   响应: {response.strip()[:100]}...")
        
        print("\n=== 测试完成 ===")
        
    except Exception as e:
        print(f"\n测试失败: {e}")
        
        # 获取stderr输出
        stderr = proc.communicate()[1]
        print(f"错误信息: {stderr}")
    finally:
        proc.stdin.close()
        proc.terminate()
        proc.wait()

if __name__ == "__main__":
    test_mcp_server()