#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试MCP协议格式
"""

import json
import sys

# 模拟Trae CN发送的请求格式
test_requests = [
    # 请求1: 获取服务描述
    json.dumps({"action": "describe"}),
    # 请求2: 获取函数列表
    json.dumps({"action": "list_functions"}),
    # 请求3: 执行函数
    json.dumps({
        "action": "execute",
        "name": "generate_outline",
        "arguments": {"genre": "玄幻修仙", "theme": "逆袭"}
    })
]

def test_mcp_protocol():
    """测试MCP协议"""
    print("Testing MCP Protocol Format...")
    
    # 将测试请求写入临时文件
    input_file = "mcp_test_input.txt"
    output_file = "mcp_test_output.txt"
    
    with open(input_file, 'w', encoding='utf-8') as f:
        for req in test_requests:
            f.write(req + "\n")
    
    # 运行MCP服务器测试
    import subprocess
    proc = subprocess.Popen(
        ['python', 'mcp_novel_stdin.py'],
        cwd='e:\\Program Files (x86)\\Trae CN\\github\\NWACS',
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding='gbk'
    )
    
    try:
        # 发送测试请求
        for req in test_requests:
            proc.stdin.write(req + "\n")
            proc.stdin.flush()
            
            # 读取响应
            response = proc.stdout.readline()
            print(f"Request: {req[:50]}...")
            print(f"Response: {response.strip()}")
            print()
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        proc.stdin.close()
        proc.terminate()
        proc.wait()

if __name__ == "__main__":
    test_mcp_protocol()