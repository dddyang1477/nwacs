#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书集成调试脚本
测试NWACS飞书链接是否正常工作
"""
import sys
import json
from pathlib import Path

# 添加项目根目录到路径
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from core.feishu.nwacs_feishu import NWACSFeishuIntegration, CONFIG_PATH
except Exception as e:
    print(f"❌ 导入模块失败: {e}")
    sys.exit(1)

def test_config():
    """测试配置文件"""
    print("="*60)
    print("📋 配置文件测试")
    print("="*60)
    
    if not CONFIG_PATH.exists():
        print(f"❌ 配置文件不存在: {CONFIG_PATH}")
        return False
    
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            config = json.load(f)
        print(f"✅ 配置文件读取成功: {CONFIG_PATH}")
        
        enable = config.get('enable', False)
        webhook_url = config.get('webhook_url', '')
        
        print(f"   - enable: {enable}")
        print(f"   - webhook_url: {'已配置' if webhook_url else '未配置'}")
        if webhook_url:
            print(f"   - webhook: {webhook_url[:50]}...")
        
        if enable and webhook_url:
            return True
        else:
            if not enable:
                print("⚠️ 飞书推送未启用")
            if not webhook_url:
                print("⚠️ webhook_url为空")
            return False
            
    except Exception as e:
        print(f"❌ 读取配置文件失败: {e}")
        return False

def test_imports():
    """测试依赖库"""
    print("\n" + "="*60)
    print("📦 依赖库测试")
    print("="*60)
    
    required_modules = [
        'requests',
    ]
    
    all_good = True
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module} 导入成功")
        except ImportError:
            print(f"❌ {module} 导入失败")
            print(f"   请安装: pip install {module}")
            all_good = False
    
    return all_good

def test_feishu_bot():
    """测试飞书机器人"""
    print("\n" + "="*60)
    print("🤖 飞书机器人测试")
    print("="*60)
    
    try:
        integration = NWACSFeishuIntegration()
        print("✅ 集成模块初始化成功")
        
        if integration.bot.enable:
            print("\n正在发送测试消息...")
            success = integration.test_connection()
            return success
        else:
            print("\n⚠️ 飞书推送未启用，请先配置webhook_url")
            print(f"   配置文件: {CONFIG_PATH}")
            return False
            
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("🔧 NWACS 飞书集成调试工具")
    print("="*60)
    
    # 1. 测试依赖库
    if not test_imports():
        print("\n❌ 依赖库不完整，请先安装缺失的库")
        return False
    
    # 2. 测试配置
    if not test_config():
        print("\n❌ 配置检查失败，请检查配置文件")
        return False
    
    # 3. 测试飞书机器人
    if not test_feishu_bot():
        print("\n❌ 飞书机器人测试失败")
        return False
    
    print("\n" + "="*60)
    print("✅ 所有测试通过！飞书集成工作正常")
    print("="*60)
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
