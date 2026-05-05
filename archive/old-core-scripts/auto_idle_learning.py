#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 自动空闲学习监控器 v2.0
电脑空闲10分钟后自动启动联网学习
新增功能：倒计时显示、冷却时间显示
"""

import time
import os
import sys
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

VERSION = "2.0"

try:
    import ctypes
    user32 = ctypes.windll.user32
    KERNEL32 = ctypes.WinDLL('kernel32.dll')
    WINDOWS_API_AVAILABLE = True
except ImportError:
    WINDOWS_API_AVAILABLE = False
    print("⚠️ Windows API不可用，将使用模拟模式")

class IdleLearningMonitor:
    """空闲学习监控器"""
    
    def __init__(self, idle_threshold=600, learning_script=None):
        """
        初始化监控器
        
        Args:
            idle_threshold: 空闲时间阈值（秒），默认600秒（10分钟）
            learning_script: 学习脚本路径，默认使用全能联网学习系统
        """
        self.idle_threshold = idle_threshold
        self.learning_script = learning_script or 'core/comprehensive_learning.py'
        self.is_idle = False
        self.start_time = time.time()
        self.last_learning_time = 0
        self.min_interval = 3600  # 学习间隔1小时
        self.running = False
        
    def format_time(self, seconds):
        """格式化时间显示"""
        if seconds >= 3600:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            secs = int(seconds % 60)
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        elif seconds >= 60:
            minutes = int(seconds // 60)
            secs = int(seconds % 60)
            return f"{minutes:02d}:{secs:02d}"
        else:
            return f"{int(seconds):02d}秒"
        
    def get_idle_time(self):
        """获取系统空闲时间（秒）"""
        if not WINDOWS_API_AVAILABLE:
            return 0
            
        try:
            last_input_info = ctypes.c_ulong()
            user32.GetLastInputInfo(ctypes.byref(last_input_info))
            current_tick = KERNEL32.GetTickCount()
            
            # 获取正确的空闲时间（处理环绕问题）
            idle_ms = current_tick - last_input_info.value
            
            # Windows的GetTickCount会在49.7天后环绕，确保计算正确
            if idle_ms < 0:
                idle_ms = idle_ms + (1 << 32)  # 处理环绕问题
            
            return idle_ms / 1000.0
        except Exception as e:
            print(f"❌ 获取空闲时间失败: {e}")
            return 0
    
    def check_should_learn(self):
        """检查是否应该启动学习"""
        current_time = time.time()
        
        # 检查冷却期
        if current_time - self.last_learning_time < self.min_interval:
            return False
        
        # 检查空闲时间
        idle_time = self.get_idle_time()
        return idle_time >= self.idle_threshold
    
    def get_cooldown_remaining(self):
        """获取剩余冷却时间"""
        current_time = time.time()
        elapsed = current_time - self.last_learning_time
        if elapsed >= self.min_interval:
            return 0
        return self.min_interval - elapsed
    
    def start_learning(self):
        """启动学习"""
        print(f"\n{'='*60}")
        print(f"🚀 检测到电脑空闲超过{self.idle_threshold}秒")
        print(f"📚 自动启动联网学习...")
        print(f"{'='*60}\n")
        
        self.last_learning_time = time.time()
        
        # 执行学习脚本
        try:
            os.system(f'py "{self.learning_script}"')
        except Exception as e:
            print(f"❌ 启动学习失败: {e}")
    
    def monitor(self):
        """监控循环"""
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║           NWACS 自动空闲学习监控器 v{VERSION}                    ║
║                                                              ║
║           ⏱️  空闲阈值: {self.idle_threshold}秒 (10分钟)                    ║
║           📚 学习脚本: {self.learning_script}                     ║
║           ⏰ 学习间隔: {self.min_interval}秒 (1小时)                       ║
║                                                              ║
║           提示: 电脑空闲超过10分钟自动开始学习                   ║
║                按 Ctrl+C 退出                                 ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
        """)
        
        self.running = True
        self.start_time = time.time()
        last_print_time = 0
        
        while self.running:
            try:
                current_time = time.time()
                
                # 启动后等待30秒再开始检测
                if current_time - self.start_time < 30:
                    remaining = 30 - (current_time - self.start_time)
                    print(f"\r⏳ 系统预热中... {self.format_time(remaining)}", end='', flush=True)
                    time.sleep(1)
                    continue
                
                idle_time = self.get_idle_time()
                is_currently_idle = idle_time >= self.idle_threshold
                
                # 获取冷却倒计时
                cooldown = self.get_cooldown_remaining()
                
                # 检测空闲状态变化
                if is_currently_idle and not self.is_idle:
                    self.is_idle = True
                    print(f"\n⏰ 检测到电脑空闲（{idle_time:.0f}秒），准备启动学习...")
                    
                    if self.check_should_learn():
                        self.start_learning()
                    else:
                        print(f"⏸️  学习冷却中，跳过本次学习")
                
                elif not is_currently_idle and self.is_idle:
                    self.is_idle = False
                    print(f"\n👤 检测到用户活动，停止监控")
                
                # 显示详细状态（每秒更新一次）
                if current_time - last_print_time >= 1:
                    status = "空闲" if is_currently_idle else "活跃"
                    
                    # 空闲倒计时
                    if is_currently_idle:
                        idle_display = f"⏳ 已空闲 {self.format_time(idle_time)}"
                    else:
                        time_remaining = max(0, self.idle_threshold - idle_time)
                        idle_display = f"⏱️ 距学习触发 {self.format_time(time_remaining)}"
                    
                    # 冷却倒计时
                    if cooldown > 0:
                        cooldown_display = f" | 🛑 冷却 {self.format_time(cooldown)}"
                    else:
                        cooldown_display = " | ✅ 就绪"
                    
                    print(f"\r{status:^8} | {idle_display} {cooldown_display}", end='', flush=True)
                    last_print_time = current_time
                
                time.sleep(1)  # 每秒检查一次
                
            except KeyboardInterrupt:
                print("\n\n⚠️  用户中断，退出监控")
                break
            except Exception as e:
                print(f"\n❌ 监控错误: {e}")
                time.sleep(1)
        
        print("\n✅ 监控器已退出")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='NWACS 自动空闲学习监控器 v2.0')
    parser.add_argument('-t', '--threshold', type=int, default=600,
                        help='空闲时间阈值（秒），默认600秒（10分钟）')
    parser.add_argument('-s', '--script', type=str, default='core/comprehensive_learning.py',
                        help='学习脚本路径')
    
    args = parser.parse_args()
    
    monitor = IdleLearningMonitor(
        idle_threshold=args.threshold,
        learning_script=args.script
    )
    monitor.monitor()

if __name__ == "__main__":
    main()
