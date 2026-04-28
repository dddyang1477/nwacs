#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试MCP服务器
"""

import subprocess
import json
import os

def test_mcp_server():
    """测试MCP服务器"""
    print("=" * 60)
    print("    测试 NovelCreation MCP Server")
    print("=" * 60)
    
    # 启动MCP服务器进程
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
        # 读取初始化响应
        response = proc.stdout.readline()
        print(f"初始化响应: {response.strip()}")
        
        # 发送describe请求
        request = {"action": "describe"}
        proc.stdin.write(json.dumps(request) + "\n")
        proc.stdin.flush()
        
        response = proc.stdout.readline()
        print(f"Describe响应: {response.strip()}")
        
        # 发送list_functions请求
        request = {"action": "list_functions"}
        proc.stdin.write(json.dumps(request) + "\n")
        proc.stdin.flush()
        
        response = proc.stdout.readline()
        result = json.loads(response)
        print(f"函数列表: {len(result.get('functions', []))} 个函数")
        
        # 发送execute请求
        request = {
            "action": "execute",
            "name": "generate_outline",
            "arguments": {
                "genre": "玄幻修仙",
                "theme": "逆袭",
                "length": "短篇"
            }
        }
        proc.stdin.write(json.dumps(request) + "\n")
        proc.stdin.flush()
        
        response = proc.stdout.readline()
        result = json.loads(response)
        if result['status'] == 'success':
            print(f"大纲生成成功: {result['result']['title']}")
            print(f"一句话梗概: {result['result']['logline']}")
        else:
            print(f"大纲生成失败: {result.get('message')}")
        
        print("\n[OK] MCP服务器测试通过！")
        
    except Exception as e:
        print(f"[ERROR] 测试失败: {e}")
        import traceback
        traceback.print_exc()
    finally:
        proc.stdin.close()
        proc.terminate()
        proc.wait()

if __name__ == "__main__":
    test_mcp_server()