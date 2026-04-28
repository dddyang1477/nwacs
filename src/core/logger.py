#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 日志记录系统 v1.0
提供统一的日志记录功能
"""

import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

class Logger:
    def __init__(self, name='NWACS', log_dir='logs'):
        self.name = name
        self.log_dir = log_dir
        
        # 创建日志目录
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # 初始化日志记录器
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # 避免重复添加处理器
        if self.logger.handlers:
            return
        
        # 创建格式化器
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # 文件处理器（带轮转）
        file_handler = RotatingFileHandler(
            os.path.join(log_dir, f'{name}.log'),
            maxBytes=1024 * 1024 * 10,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        
        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        
        # 添加处理器
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def debug(self, message):
        """调试级别日志"""
        self.logger.debug(message)
    
    def info(self, message):
        """信息级别日志"""
        self.logger.info(message)
    
    def warning(self, message):
        """警告级别日志"""
        self.logger.warning(message)
    
    def error(self, message, exc_info=False):
        """错误级别日志"""
        self.logger.error(message, exc_info=exc_info)
    
    def critical(self, message, exc_info=False):
        """严重错误级别日志"""
        self.logger.critical(message, exc_info=exc_info)
    
    def log_exception(self, exc, context=''):
        """记录异常信息"""
        self.error(f"Exception in {context}: {type(exc).__name__}: {exc}", exc_info=True)

# 创建全局日志实例
logger = Logger()

if __name__ == "__main__":
    # 测试日志功能
    logger.info("日志系统初始化成功")
    logger.debug("这是一条调试消息")
    logger.warning("这是一条警告消息")
    logger.error("这是一条错误消息")
    
    try:
        raise ValueError("测试异常")
    except Exception as e:
        logger.log_exception(e, "测试异常处理")