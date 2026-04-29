#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试大模型连接
"""

import json
import os
import sys

def test_llm_connection():
    print("=" * 60)
    print("    大模型连接测试")
    print("=" * 60)
    
    # 1. 检查配置文件
    print("\n[1/4] 检查配置文件...")
    config_file = "config.json"
    if os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        print("  OK 配置文件已找到")
        print("    api_key: %s" % ("已配置" if config.get('api_key') else "未配置"))
        print("    base_url: %s" % config.get('base_url', '未配置'))
        print("    model: %s" % config.get('model', '未配置'))
        print("    enabled: %s" % config.get('enabled', False))
    else:
        print("  FAIL 配置文件不存在: %s" % config_file)
        return
    
    # 2. 检查openai库
    print("\n[2/4] 检查openai库...")
    try:
        import openai
        print("  OK openai库已安装")
    except ImportError:
        print("  FAIL openai库未安装")
        print("    请运行: pip install openai")
        return
    
    # 3. 测试连接
    print("\n[3/4] 测试大模型连接...")
    api_key = config.get('api_key')
    base_url = config.get('base_url')
    model = config.get('model', 'deepseek-chat')
    
    try:
        if base_url:
            client = openai.OpenAI(api_key=api_key, base_url=base_url)
        else:
            client = openai.OpenAI(api_key=api_key)
        
        # 测试API调用
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": "Hello, test connection"}
            ],
            max_tokens=10
        )
        
        print("  OK 大模型连接成功！")
        print("    Response: %s" % response.choices[0].message.content.strip())
        
    except Exception as e:
        print("  FAIL 连接失败: %s" % str(e))
        return
    
    # 4. 总结
    print("\n[4/4] 测试总结")
    print("=" * 60)
    print("  大模型连接测试: OK")
    print("=" * 60)

if __name__ == "__main__":
    test_llm_connection()