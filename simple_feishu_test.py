#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的飞书Webhook测试脚本
"""
import sys
import requests
import json
from datetime import datetime

# 您的飞书Webhook URL
WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/b415339e-f6f4-4e2f-978e-5e56f44a18f6"

def test_webhook():
    """测试飞书Webhook"""
    print("="*60)
    print("🧪 飞书Webhook直接测试")
    print("="*60)
    
    print(f"\nWebhook URL: {WEBHOOK_URL}")
    print(f"\n测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 测试1: 发送简单文本消息
    print("\n" + "-"*60)
    print("测试1: 发送简单文本消息")
    print("-"*60)
    
    data1 = {
        "msg_type": "text",
        "content": {
            "text": f"🧪 NWACS飞书集成测试消息\n\n测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n这是一条测试消息！"
        }
    }
    
    try:
        print(f"正在发送请求...")
        response = requests.post(WEBHOOK_URL, json=data1, timeout=10)
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        result = response.json()
        if result.get("code") == 0:
            print("✅ 文本消息发送成功！")
        else:
            print(f"❌ 文本消息发送失败: {result}")
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return False
    
    # 测试2: 发送富文本消息
    print("\n" + "-"*60)
    print("测试2: 发送富文本消息")
    print("-"*60)
    
    data2 = {
        "msg_type": "interactive",
        "card": {
            "config": {
                "wide_screen_mode": True
            },
            "header": {
                "template": "blue",
                "title": {
                    "tag": "plain_text",
                    "content": "🎉 NWACS飞书集成测试成功"
                }
            },
            "elements": [
                {
                    "tag": "markdown",
                    "content": "**测试时间**: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n**测试状态**: ✅ 成功\n**消息类型**: 富文本卡片"
                }
            ]
        }
    }
    
    try:
        print(f"正在发送富文本请求...")
        response = requests.post(WEBHOOK_URL, json=data2, timeout=10)
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        result = response.json()
        if result.get("code") == 0:
            print("✅ 富文本消息发送成功！")
            return True
        else:
            print(f"❌ 富文本消息发送失败: {result}")
            return False
            
    except Exception as e:
        print(f"❌ 富文本请求异常: {e}")
        return False

if __name__ == "__main__":
    print("飞书Webhook调试工具")
    print("="*60)
    
    success = test_webhook()
    
    print("\n" + "="*60)
    if success:
        print("✅ 飞书Webhook测试完成！")
    else:
        print("❌ 飞书Webhook测试失败，请检查配置")
    print("="*60)
    
    sys.exit(0 if success else 1)
