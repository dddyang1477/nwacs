#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 飞书发送测试
直接测试NWACS发送消息到飞书
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

print("="*70)
print("NWACS Feishu Send Test")
print("="*70)
print()

try:
    from core.feishu.nwacs_feishu import NWACSFeishuIntegration
    print("✅ Loading integration...")
    
    integration = NWACSFeishuIntegration()
    print("✅ Integration loaded!")
    print()
    
    print("Sending test message...")
    test_result = integration.send_custom_message(
        "🎉 NWACS 测试成功",
        f"""✅ NWACS飞书连接测试成功！

时间：
📅 {__import__('datetime').datetime.now().strftime('%Y-%m-%d')}
🕐 {__import__('datetime').datetime.now().strftime('%H:%M:%S')}

可用命令：
• status - 系统状态
• learn - 开始学习
• help - 显示帮助

测试完成！"""
    )
    
    print()
    if test_result:
        print("="*70)
        print("✅✅✅ TEST SUCCESS! Check your Feishu!")
        print("="*70)
    else:
        print("❌ Test failed!")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
