#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 飞书极简测试 - 直接发送
完全独立，不依赖其他模块
"""
import json
import requests
import sys
from datetime import datetime

print("="*80)
print("NWACS Feishu MINIMAL TEST")
print("="*80)
print()

# 直接配置
WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/c808e5d5-1912-4795-9347-a05cc15c5b89"

print(f"🎯 Target: {WEBHOOK_URL}")
print()

# 准备测试消息
message_data = {
    "msg_type": "text",
    "content": {
        "text": f"""🎉 NWACS 飞书测试成功！

时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

这是一条测试消息！
"""
    }
}

print("📤 Sending test message...")
print(f"📋 Data: {json.dumps(message_data, ensure_ascii=False)}")
print()

try:
    headers = {
        'Content-Type': 'application/json; charset=utf-8'
    }
    
    json_data = json.dumps(message_data, ensure_ascii=False).encode('utf-8')
    
    response = requests.post(WEBHOOK_URL, headers=headers, data=json_data, timeout=10)
    
    print("="*80)
    print(f"📨 Response Status: {response.status_code}")
    print(f"📨 Response Body: {response.text}")
    print("="*80)
    
    result = response.json()
    
    if result.get("code") == 0:
        print("\n✅✅✅ SUCCESS! Check your Feishu!")
        print("You should see the test message!")
    else:
        print(f"\n❌ FAILED! Code: {result.get('code')}, Message: {result.get('msg')}")
        
except requests.exceptions.Timeout:
    print("\n❌ TIMEOUT!")
except requests.exceptions.ConnectionError as e:
    print(f"\n❌ CONNECTION ERROR: {e}")
    print("Check your internet or firewall!")
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\nDone!")
