#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 空闲检测学习模块
电脑空闲一定时间后自动启动学习系统
"""

import time
import threading
import os
from datetime import datetime
from logger import logger

try:
    import ctypes
    user32 = ctypes.windll.user32
    KERNEL32 = ctypes.WinDLL('kernel32.dll')
except ImportError:
    logger.warning("Windows API不可用，空闲检测功能受限")
    user32 = None

class IdleMonitor:
    """电脑空闲状态监控器"""

    def __init__(self, idle_threshold=600):
        """
        初始化空闲监控器
        
        Args:
            idle_threshold: 空闲时间阈值（秒），默认10分钟(600秒)
        """
        self.idle_threshold = idle_threshold
        self.is_idle = False
        self.last_activity_time = time.time()
        self.monitor_thread = None
        self.running = False
        self.on_idle_callback = None
        self.start_time = 0  # 记录启动时间，避免启动时误触发

    def get_idle_time(self):
        """获取系统空闲时间（秒）"""
        if user32 is None:
            return 0

        try:
            last_input_info = ctypes.c_ulong()
            user32.GetLastInputInfo(ctypes.byref(last_input_info))
            current_tick = KERNEL32.GetTickCount()
            idle_ms = current_tick - last_input_info.value
            return idle_ms / 1000.0
        except Exception as e:
            logger.log_exception(e, "获取空闲时间")
            return 0

    def check_idle(self):
        """检查是否空闲"""
        idle_time = self.get_idle_time()
        return idle_time >= self.idle_threshold

    def monitor_loop(self):
        """监控循环"""
        logger.info("空闲监控器已启动，阈值: %d秒" % self.idle_threshold)

        while self.running:
            # 启动后等待30秒再开始检测，避免启动时误触发
            if time.time() - self.start_time < 30:
                time.sleep(5)
                continue

            idle_time = self.get_idle_time()
            is_currently_idle = idle_time >= self.idle_threshold

            # 检测空闲状态变化
            if is_currently_idle and not self.is_idle:
                self.is_idle = True
                logger.info("检测到电脑空闲（%d秒），触发学习系统" % idle_time)
                if self.on_idle_callback:
                    try:
                        self.on_idle_callback()
                    except Exception as e:
                        logger.log_exception(e, "空闲回调")

            elif not is_currently_idle and self.is_idle:
                self.is_idle = False
                logger.info("检测到用户活动")

            time.sleep(30)  # 每30秒检查一次

    def start(self, callback=None):
        """启动监控"""
        self.on_idle_callback = callback
        self.running = True
        self.start_time = time.time()  # 记录启动时间
        self.monitor_thread = threading.Thread(target=self.monitor_loop)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()

    def stop(self):
        """停止监控"""
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join()


class AutoLearningScheduler:
    """自动学习调度器"""

    def __init__(self):
        # 从配置文件读取阈值
        threshold = 600  # 默认10分钟
        try:
            import json
            config_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config.json')
            if os.path.exists(config_file):
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    threshold = config.get('idle_threshold', 600)
        except Exception:
            pass
        
        self.idle_monitor = IdleMonitor(idle_threshold=threshold)
        self.learning_manager = None
        self.learning_running = False
        self.last_learning_time = 0
        self.min_interval = 3600  # 每小时最多学习一次

    def set_learning_manager(self, manager):
        """设置学习管理器"""
        self.learning_manager = manager

    def on_idle_detected(self):
        """空闲检测回调"""
        now = time.time()

        # 检查是否在冷却期内
        if now - self.last_learning_time < self.min_interval:
            logger.info("学习冷却中，跳过本次学习")
            return

        # 启动学习
        if not self.learning_running:
            self.start_learning()

    def start_learning(self):
        """启动学习"""
        try:
            self.learning_running = True
            self.last_learning_time = time.time()

            logger.info("=" * 60)
            logger.info("自动学习系统启动 - %s" % datetime.now())
            logger.info("=" * 60)

            if self.learning_manager:
                # 执行单次学习（非循环）
                self.learning_manager.initialize_learners()

                # 让每个Skill学习一次
                for skill_name, learner in self.learning_manager.skill_learners.items():
                    try:
                        learner.execute_learning()
                    except Exception as e:
                        logger.log_exception(e, "%s 自动学习" % skill_name)

                logger.info("自动学习完成")

        finally:
            self.learning_running = False

    def start(self):
        """启动调度器"""
        logger.info("自动学习调度器启动")
        self.idle_monitor.start(callback=self.on_idle_detected)

    def stop(self):
        """停止调度器"""
        self.idle_monitor.stop()
        logger.info("自动学习调度器已停止")


# 全局单例
_scheduler_instance = None

def get_auto_scheduler():
    """获取自动调度器单例"""
    global _scheduler_instance
    if _scheduler_instance is None:
        _scheduler_instance = AutoLearningScheduler()
    return _scheduler_instance


# 独立运行测试
if __name__ == "__main__":
    print("=====================================")
    print("    NWACS 空闲检测学习模块测试")
    print("=====================================")
    print("空闲阈值: 10分钟")
    print("按 Ctrl+C 退出")
    print("=====================================")

    scheduler = get_auto_scheduler()
    scheduler.start()

    try:
        while True:
            time.sleep(60)
            idle_time = scheduler.idle_monitor.get_idle_time()
            print("\n当前空闲时间: %.1f秒 | 空闲状态: %s" % (
                idle_time, 
                "空闲" if scheduler.idle_monitor.is_idle else "活跃"
            ))
    except KeyboardInterrupt:
        scheduler.stop()
        print("\n自动学习调度器已停止")