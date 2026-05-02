#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 飞书配置向导
引导用户完成飞书配置
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.config_manager import config
from core.logger import NWACSLogger
from core.adapters.feishu_adapter import FeishuAdapter

def print_banner():
    """打印横幅"""
    print("="*70)
    print("🔧 NWACS 飞书配置向导")
    print("="*70)
    print()

def check_current_config():
    """检查当前配置"""
    print("[1/5] 检查当前配置...")
    print()

    webhook = config.feishu_webhook_url
    enabled = config.feishu_enabled

    print(f"   飞书启用: {'是' if enabled else '否'}")
    print(f"   Webhook: {webhook if webhook else '未配置'}")
    print()

    return bool(webhook)

def test_current_connection():
    """测试当前连接"""
    print("[2/5] 测试当前连接...")
    print()

    feishu = FeishuAdapter()
    result = feishu.test_connection()

    if result:
        print("   ✅ 连接测试成功！")
    else:
        print("   ❌ 连接测试失败")

    print()
    return result

def update_webhook():
    """更新Webhook"""
    print("[3/5] 更新Webhook...")
    print()

    print("请输入新的Webhook URL:")
    print("格式: https://open.feishu.cn/open-apis/bot/v2/hook/xxx")
    print()

    new_webhook = input("> ").strip()

    if new_webhook:
        config.set("webhook_url", new_webhook)
        config.save()
        print(f"   ✅ Webhook已更新: {new_webhook[:50]}...")
    else:
        print("   ⚠️ 跳过更新")

    print()
    return new_webhook

def test_new_connection():
    """测试新连接"""
    print("[4/5] 测试新连接...")
    print()

    feishu = FeishuAdapter()
    result = feishu.send_message("🧪 配置向导测试消息", "✅ NWACS配置成功")

    if result:
        print("   ✅ 测试消息发送成功！")
    else:
        print("   ❌ 测试消息发送失败")

    print()
    return result

def show_next_steps():
    """显示后续步骤"""
    print("[5/5] 后续步骤...")
    print()

    print("="*70)
    print("📋 后续步骤:")
    print()
    print("1. 启动飞书集成服务器:")
    print("   py feishu_server_v2.py")
    print()
    print("2. 配置双向通信（可选）:")
    print("   - 下载ngrok: https://ngrok.com/download")
    print("   - 运行: ngrok http 8088")
    print("   - 在飞书机器人配置消息订阅")
    print()
    print("3. 查看帮助:")
    print("   运行 start_nwacs_main.bat 查看主菜单")
    print()
    print("="*70)

def main():
    """主函数"""
    print_banner()

    print("欢迎使用NWACS飞书配置向导！")
    print("这个向导将帮助您配置飞书集成。")
    print()

    # 检查配置
    has_config = check_current_config()

    # 测试当前连接
    if has_config:
        test_current_connection()

    # 询问是否更新
    print("是否要更新Webhook配置? (y/n)")
    choice = input("> ").strip().lower()

    if choice == 'y':
        update_webhook()
        test_new_connection()

    # 显示后续步骤
    show_next_steps()

    print()
    print("配置向导完成！")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n配置向导已取消")
    except Exception as e:
        print(f"\n\n发生错误: {e}")
