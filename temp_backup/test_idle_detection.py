#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 空闲检测功能测试脚本
快速验证系统是否能够正常检测空闲时间
"""

import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

try:
    import ctypes
    user32 = ctypes.windll.user32
    KERNEL32 = ctypes.WinDLL('kernel32.dll')
    WINDOWS_API_AVAILABLE = True
except Exception as e:
    print(f"⚠️ Windows API导入失败: {e}")
    WINDOWS_API_AVAILABLE = False


def get_idle_time():
    """获取当前系统空闲时间"""
    if not WINDOWS_API_AVAILABLE:
        return 0
        
    try:
        last_input_info = ctypes.c_ulong()
        user32.GetLastInputInfo(ctypes.byref(last_input_info))
        current_tick = KERNEL32.GetTickCount()
        idle_ms = current_tick - last_input_info.value
        return idle_ms / 1000.0
    except Exception as e:
        print(f"❌ 获取空闲时间失败: {e}")
        return 0


def test_idle_detection():
    """测试空闲检测功能"""
    print("="*60)
    print("          NWACS 空闲检测功能测试")
    print("="*60)
    print()
    print(f"📊 Windows API状态: {'✅ 已加载' if WINDOWS_API_AVAILABLE else '❌ 未加载'}")
    print()
    
    if not WINDOWS_API_AVAILABLE:
        print("⚠️  无法进行空闲检测，请确保在Windows上运行！")
        return False
    
    print("🚀 开始测试（10秒后停止）")
    print("⏱️  请随意移动鼠标或敲击键盘来测试检测功能")
    print()
    print(f"{'时间':<12} {'状态':<8} {'空闲时间':<15}")
    print("="*40)
    
    start_time = time.time()
    while time.time() - start_time < 10:
        idle_time = get_idle_time()
        is_idle = idle_time >= 5  # 5秒空闲为阈值
        
        status = "空闲" if is_idle else "活跃"
        idle_display = f"{idle_time:.1f}秒"
        
        print(f"\r{time.strftime('%H:%M:%S'): <12} {status: <8} {idle_display: <15}", end='', flush=True)
        
        time.sleep(1)
    
    print("\n")
    print("="*60)
    print("✅ 测试完成！")
    print("="*60)
    return True


if __name__ == "__main__":
    test_idle_detection()
    print()
    print("💡 提示: 要启动完整的自动空闲学习功能，请运行:")
    print("   py auto_idle_learning.py")
