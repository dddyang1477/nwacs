#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
极简飞书Webhook测试 - 最简单的版本
"""
import sys

print("="*60)
print("🚀 开始飞书Webhook测试")
print("="*60)

# 1. 测试requests库
print("\n[1/4] 检查requests库...")
try:
    import requests
    print("✅ requests库已安装")
except ImportError:
    print("❌ requests库未安装，尝试安装...")
    try:
        import subprocess
        result = subprocess.run([sys.executable, "-m", "pip", "install", "requests"],
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ requests库安装成功")
            import requests
        else:
            print(f"❌ 安装失败: {result.stderr}")
            sys.exit(1)
    except Exception as e:
        print(f"❌ 安装失败: {e}")
        sys.exit(1)

# 2. 测试Webhook URL
print("\n[2/4] 配置Webhook URL...")
WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/b415339e-f6f4-4e2f-978e-5e56f44a18f6"
print(f"✅ Webhook URL: {WEBHOOK_URL}")

# 3. 发送测试消息
print("\n[3/4] 发送测试消息...")
test_message = "🧪 NWACS飞书测试 - " + __import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')

data = {
    "msg_type": "text",
    "content": {
        "text": test_message
    }
}

print(f"📤 正在发送: {test_message}")

try:
    response = requests.post(WEBHOOK_URL, json=data, timeout=15)
    print(f"📥 收到响应: {response.status_code}")
    print(f"📝 响应内容: {response.text}")

    result = response.json()
    if result.get("code") == 0:
        print("\n✅✅✅ 飞书Webhook测试成功！")
        print("请检查您的飞书是否收到了测试消息！")
    else:
        print(f"\n❌ 发送失败，错误码: {result.get('code')}")
        print(f"错误信息: {result.get('msg', '未知错误')}")

except requests.exceptions.Timeout:
    print("\n❌ 连接超时，请检查网络连接")
except requests.exceptions.ConnectionError as e:
    print(f"\n❌ 连接失败: {e}")
    print("请检查网络是否正常，或防火墙是否阻止了请求")
except Exception as e:
    print(f"\n❌ 发生错误: {e}")

# 4. 完成
print("\n[4/4] 测试完成")
print("="*60)
