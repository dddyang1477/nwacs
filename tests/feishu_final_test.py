# -*- coding: utf-8 -*-
"""
NWACS飞书测试脚本 - 修复编码问题
"""
import json
import sys
from datetime import datetime

print("="*60)
print("NWACS 飞书测试 - 编码修复版")
print("="*60)

try:
    import requests
    print("✅ requests库已加载")
except ImportError as e:
    print(f"❌ requests库未安装: {e}")
    sys.exit(1)

WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/d22b9add-1188-4593-8bbb-15bc87647a56"
print(f"📡 Webhook URL: {WEBHOOK_URL}")

# 测试消息
test_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
test_messages = [
    "✅ NWACS系统状态正常",
    "🚀 测试消息 - 中文正常显示",
    "🎉 知识库更新完成",
    "📝 学习引擎正在运行"
]

selected_msg = test_messages[0] + " - " + test_time

print(f"\n📤 发送消息: {selected_msg}")

# 构建数据
data = {
    "msg_type": "text",
    "content": {
        "text": selected_msg
    }
}

print("\n🔧 构建请求:")
print(f"   数据: {json.dumps(data, ensure_ascii=False, indent=2)}")

try:
    # 设置UTF-8编码header
    headers = {
        'Content-Type': 'application/json; charset=utf-8'
    }
    
    # 手动序列化并编码为UTF-8
    json_data = json.dumps(data, ensure_ascii=False).encode('utf-8')
    
    print(f"\n🚀 发送请求...")
    response = requests.post(WEBHOOK_URL, headers=headers, data=json_data, timeout=10)
    
    print(f"\n📥 响应:")
    print(f"   状态码: {response.status_code}")
    print(f"   内容: {response.text}")
    
    result = response.json()
    
    if result.get("code") == 0:
        print("\n✅✅✅ 飞书消息发送成功！")
        print("\n请检查您的飞书群，消息应该显示正确的中文！")
    else:
        print(f"\n❌ 发送失败，错误码: {result.get('code')}")
        print(f"   错误信息: {result.get('msg', '未知错误')}")

except requests.exceptions.Timeout:
    print("\n❌ 连接超时")
except requests.exceptions.ConnectionError as e:
    print(f"\n❌ 连接失败: {e}")
except Exception as e:
    print(f"\n❌ 发生错误: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
