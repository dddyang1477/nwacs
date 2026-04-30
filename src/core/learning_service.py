#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 自动学习服务 v1.0
独立运行的自动学习守护进程
"""

import time
import threading
import os
import signal
import sys
from datetime import datetime
from logger import logger

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from auto_learning import AutoLearningSystem

class LearningService:
    """自动学习服务"""
    
    def __init__(self):
        self.running = False
        self.learning_system = None
        self.watchdog_thread = None
        self.activity_thread = None
        
        # 注册信号处理
        signal.signal(signal.SIGINT, self.handle_shutdown)
        signal.signal(signal.SIGTERM, self.handle_shutdown)
    
    def start(self):
        """启动服务"""
        logger.info("=" * 60)
        logger.info("    NWACS 自动学习服务启动")
        logger.info("=" * 60)
        
        self.running = True
        
        # 启动自动学习系统
        self.learning_system = AutoLearningSystem()
        
        # 启动看门狗线程（监控服务状态）
        self.watchdog_thread = threading.Thread(target=self.watchdog_loop)
        self.watchdog_thread.daemon = False
        self.watchdog_thread.start()
        
        # 启动活动模拟线程（测试用）
        self.activity_thread = threading.Thread(target=self.simulate_activity)
        self.activity_thread.daemon = False
        self.activity_thread.start()
        
        logger.info("自动学习服务已启动")
        
        # 保持主线程运行
        while self.running:
            time.sleep(1)
    
    def watchdog_loop(self):
        """看门狗循环"""
        while self.running:
            try:
                # 检查学习系统状态
                if self.learning_system:
                    stats = self.learning_system.get_stats()
                    logger.debug("学习系统状态: 学习次数=%d, 错误次数=%d" % 
                               (stats['learning_count'], stats['error_count']))
                
                # 每30秒检查一次
                time.sleep(30)
            except Exception as e:
                logger.log_exception(e, "watchdog_loop")
    
    def simulate_activity(self):
        """模拟用户活动（测试空闲检测）"""
        # 前2分钟模拟有活动，之后进入空闲状态
        for i in range(120):
            if self.learning_system:
                self.learning_system.record_activity()
            time.sleep(1)
        
        logger.info("活动模拟结束，系统进入空闲检测模式")
        
        # 之后每5分钟模拟一次短暂活动
        while self.running:
            time.sleep(300)  # 5分钟
            if self.learning_system:
                self.learning_system.record_activity()
                logger.debug("模拟用户活动")
    
    def handle_shutdown(self, signum, frame):
        """处理关机信号"""
        logger.info("收到关机信号，正在停止服务...")
        self.running = False
        
        if self.learning_system:
            stats = self.learning_system.get_stats()
            logger.info("服务停止统计: 学习次数=%d, 错误次数=%d" % 
                       (stats['learning_count'], stats['error_count']))
        
        logger.info("自动学习服务已停止")
        sys.exit(0)

def main():
    """主函数"""
    try:
        service = LearningService()
        service.start()
    except Exception as e:
        logger.log_exception(e, "main")
        print("服务启动失败:", str(e))
        sys.exit(1)

if __name__ == "__main__":
    main()