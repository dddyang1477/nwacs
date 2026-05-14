#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS DeepSeek Diagnosis Script
使用DeepSeek分析飞书集成问题
"""
import sys
import json
import traceback
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

print("="*80)
print("NWACS DeepSeek Diagnostic Tool")
print("="*80)
print()

def load_config():
    """加载配置"""
    config_path = PROJECT_ROOT / "config" / "feishu_config.json"
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        print(f"✅ Config loaded: {config.get('webhook_url', 'N/A')}")
        return config
    except Exception as e:
        print(f"❌ Config load error: {e}")
        return None

def test_feishu_code():
    """测试飞书代码"""
    print("\n📋 Testing Feishu Integration Code...")
    try:
        from core.feishu.nwacs_feishu import NWACSFeishuIntegration
        print("✅ Feishu module imported successfully")
        return True
    except Exception as e:
        print(f"❌ Feishu module import error: {e}")
        return False

def create_diagnostic_prompt(config):
    """创建诊断提示词"""
    return f"""
请分析NWACS飞书集成问题！

当前情况：
- NWACS有两个方向的飞书集成
- 方向1：NWACS→飞书（发送消息）
- 方向2：飞书→NWACS（接收消息）

当前配置：
- Webhook地址：{config.get('webhook_url', 'N/A') if config else 'N/A'}
- 配置状态：{'已启用' if config and config.get('enable') else '未启用'}

遇到的问题：
- 用户测试时两个方向都没收到消息
- 在飞书群中@机器人，消息有勾选标记但没有回复
- NWACS服务器运行正常但没收到飞书的请求

请分析：
1. 为什么NWACS发送的消息飞书收不到？
2. 为什么飞书的消息没有发送到NWACS？
3. 当前代码的实现可能有什么问题？
4. 给出完整的解决方案

请提供可操作的步骤！
"""

def call_deepseek_for_diagnosis(prompt):
    """调用DeepSeek诊断"""
    print("\n🤖 Calling DeepSeek for diagnosis...")
    try:
        import requests
        
        API_KEY = "sk-f3246fbd1eef446e9a11d78efefd9bba"
        API_URL = "https://api.deepseek.com/v1/chat/completions"
        
        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "你是NWACS飞书集成专家。提供技术诊断和解决方案。"},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }
        
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(API_URL, json=data, headers=headers, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ DeepSeek response received!")
            return result.get("choices", [{}])[0].get("message", {}).get("content", "")
        else:
            print(f"❌ DeepSeek API error: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ DeepSeek call error: {e}")
        return None

def main():
    print("="*80)
    print("Starting DeepSeek Diagnosis")
    print("="*80)
    
    config = load_config()
    test_feishu_code()
    
    prompt = create_diagnostic_prompt(config)
    diagnosis = call_deepseek_for_diagnosis(prompt)
    
    if diagnosis:
        print("\n" + "="*80)
        print("📊 DEEPSEEK DIAGNOSIS RESULT")
        print("="*80)
        print(diagnosis)
        print("="*80)
        
        save_path = PROJECT_ROOT / "feishu_diagnosis_report.txt"
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write("NWACS FEISHU INTEGRATION DIAGNOSIS REPORT\n")
            f.write("="*80 + "\n")
            f.write(diagnosis)
        print(f"\n✅ Report saved: {save_path}")
    
    print("\nDone!")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        traceback.print_exc()
