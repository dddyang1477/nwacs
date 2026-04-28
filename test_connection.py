#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MCP服务器与Skill联通性测试脚本
测试所有MCP工具和Skill之间的连接状态
"""

import subprocess
import json
import time
import os

def test_python_mcp_server():
    """测试Python MCP服务器"""
    print("\n" + "="*60)
    print("🔧 测试 Python MCP 服务器")
    print("="*60)
    
    try:
        process = subprocess.Popen(
            ["python", "simple_mcp_server.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd="e:\\Program Files (x86)\\Trae CN\\github\\NWACS",
            text=True,
            encoding="utf-8"
        )
        
        # 发送测试请求
        test_request = json.dumps({
            "method": "tools/list",
            "params": {}
        }) + "\n"
        
        stdout, stderr = process.communicate(input=test_request, timeout=30)
        
        if process.returncode == 0:
            try:
                response = json.loads(stdout.strip())
                tools = response.get("tools", [])
                print(f"✅ Python MCP服务器连接成功")
                print(f"📦 可用工具数量: {len(tools)}")
                for tool in tools:
                    print(f"   - {tool.get('name', '未知工具')}: {tool.get('description', '')}")
                return True
            except json.JSONDecodeError:
                print(f"⚠️ 响应解析失败: {stdout[:200]}")
                return False
        else:
            print(f"❌ Python MCP服务器启动失败")
            print(f"错误信息: {stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Python MCP服务器超时")
        return False
    except Exception as e:
        print(f"❌ Python MCP服务器测试异常: {str(e)}")
        return False

def test_node_mcp_server():
    """测试Node.js MCP服务器"""
    print("\n" + "="*60)
    print("🔧 测试 Node.js MCP 服务器")
    print("="*60)
    
    try:
        process = subprocess.Popen(
            ["node", "novel-mcp-server-v2/dist/index.js"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd="e:\\Program Files (x86)\\Trae CN\\github\\NWACS",
            text=True,
            encoding="utf-8"
        )
        
        # 发送测试请求
        test_request = json.dumps({
            "jsonrpc": "2.0",
            "id": "test-001",
            "method": "tools/list",
            "params": {}
        }) + "\n"
        
        stdout, stderr = process.communicate(input=test_request, timeout=30)
        
        if process.returncode == 0:
            try:
                response = json.loads(stdout.strip())
                tools = response.get("tools", [])
                print(f"✅ Node.js MCP服务器连接成功")
                print(f"📦 可用工具数量: {len(tools)}")
                for tool in tools:
                    print(f"   - {tool.get('name', '未知工具')}: {tool.get('description', '')}")
                return True
            except json.JSONDecodeError:
                print(f"⚠️ 响应解析失败")
                print(f"原始响应: {stdout[:500]}")
                return False
        else:
            print(f"❌ Node.js MCP服务器启动失败")
            print(f"错误信息: {stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Node.js MCP服务器超时")
        return False
    except Exception as e:
        print(f"❌ Node.js MCP服务器测试异常: {str(e)}")
        return False

def test_skill_integration():
    """测试Skill集成"""
    print("\n" + "="*60)
    print("🔧 测试 Skill 集成")
    print("="*60)
    
    skills_config = "config/20_TraeCN_Skills配置.json"
    
    if not os.path.exists(skills_config):
        print(f"❌ 配置文件不存在: {skills_config}")
        return False
    
    try:
        with open(skills_config, "r", encoding="utf-8") as f:
            config = json.load(f)
        
        primary_skills = config.get("primary", [])
        secondary_skills = config.get("secondary", [])
        tertiary_skills = config.get("tertiary", [])
        
        print(f"📊 Skill体系结构:")
        print(f"   • 一级Skill: {len(primary_skills)} 个")
        for skill in primary_skills:
            print(f"     - {skill.get('name', '未知')}")
        
        print(f"   • 二级Skill: {len(secondary_skills)} 个")
        print(f"   • 三级Skill: {len(tertiary_skills)} 个")
        
        # 检查关键Skill是否存在
        key_skills = ["小说总调度官", "写作技巧大师", "角色塑造师", "词汇大师"]
        for key_skill in key_skills:
            found = False
            for skill in primary_skills + secondary_skills:
                if key_skill in skill.get("name", ""):
                    found = True
                    print(f"✅ {key_skill} - 已配置")
                    break
            if not found:
                print(f"❌ {key_skill} - 未找到")
        
        return True
        
    except Exception as e:
        print(f"❌ Skill配置解析失败: {str(e)}")
        return False

def test_tool_execution():
    """测试工具执行"""
    print("\n" + "="*60)
    print("🔧 测试工具执行")
    print("="*60)
    
    try:
        process = subprocess.Popen(
            ["python", "simple_mcp_server.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd="e:\\Program Files (x86)\\Trae CN\\github\\NWACS",
            text=True,
            encoding="utf-8"
        )
        
        # 测试generate_outline工具
        test_request = json.dumps({
            "method": "execute",
            "params": {
                "name": "generate_outline",
                "arguments": {
                    "genre": "玄幻",
                    "length": 5
                }
            }
        }) + "\n"
        
        stdout, stderr = process.communicate(input=test_request, timeout=60)
        
        if process.returncode == 0:
            try:
                response = json.loads(stdout.strip())
                if response.get("success", False):
                    outline = response.get("outline", "")
                    print(f"✅ generate_outline 工具执行成功")
                    print(f"📝 生成大纲预览: {outline[:100]}...")
                    return True
                else:
                    print(f"❌ generate_outline 工具执行失败")
                    print(f"错误信息: {response.get('error', '未知错误')}")
                    return False
            except json.JSONDecodeError:
                print(f"⚠️ 响应解析失败")
                return False
        else:
            print(f"❌ 工具执行失败")
            print(f"错误信息: {stderr}")
            return False
            
    except Exception as e:
        print(f"❌ 工具执行测试异常: {str(e)}")
        return False

def main():
    """主测试函数"""
    print("🚀 MCP服务器与Skill联通性测试")
    print("="*60)
    
    results = []
    
    # 测试Python MCP服务器
    results.append(("Python MCP服务器", test_python_mcp_server()))
    
    # 测试Node.js MCP服务器
    results.append(("Node.js MCP服务器", test_node_mcp_server()))
    
    # 测试Skill集成
    results.append(("Skill集成", test_skill_integration()))
    
    # 测试工具执行
    results.append(("工具执行", test_tool_execution()))
    
    # 输出测试总结
    print("\n" + "="*60)
    print("📊 测试结果汇总")
    print("="*60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for name, success in results:
        status = "✅ 通过" if success else "❌ 失败"
        print(f"{name}: {status}")
    
    print(f"\n总体结果: {passed}/{total} 通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！MCP服务器与Skill联通性良好")
    else:
        print("\n⚠️ 部分测试失败，请检查相关配置")

if __name__ == "__main__":
    main()