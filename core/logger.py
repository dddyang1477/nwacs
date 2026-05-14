#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 统一日志系统
所有模块使用统一的日志记录
"""
import os
import sys
import logging
from pathlib import Path
from datetime import datetime
from logging.handlers import RotatingFileHandler

# 尝试导入配置管理器
try:
    from core.config_manager import config
    LOG_DIR = config.LOG_DIR
    PROJECT_ROOT = config.PROJECT_ROOT
except:
    # 如果配置管理器还未创建，使用默认值
    PROJECT_ROOT = Path(__file__).parent.parent
    LOG_DIR = PROJECT_ROOT / "logs"

LOG_DIR.mkdir(exist_ok=True)

class NWACSLogger:
    """NWACS统一日志记录器"""

    _loggers = {}

    @classmethod
    def get_logger(cls, name: str = "NWACS", log_file: str = None):
        """获取日志记录器"""
        if name in cls._loggers:
            return cls._loggers[name]

        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        # 避免重复添加handler
        if not logger.handlers:
            # 控制台处理器
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.INFO)
            console_formatter = logging.Formatter(
                '[%(asctime)s] %(levelname)s - %(message)s',
                datefmt='%H:%M:%S'
            )
            console_handler.setFormatter(console_formatter)
            logger.addHandler(console_handler)

            # 文件处理器
            if log_file is None:
                log_file = f"nwacs_{datetime.now().strftime('%Y%m%d')}.log"

            log_path = LOG_DIR / log_file
            file_handler = RotatingFileHandler(
                log_path,
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5,
                encoding='utf-8'
            )
            file_handler.setLevel(logging.DEBUG)
            file_formatter = logging.Formatter(
                '[%(asctime)s] %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)

        cls._loggers[name] = logger
        return logger

    @classmethod
    def info(cls, message: str, name: str = "NWACS"):
        """记录INFO级别日志"""
        logger = cls.get_logger(name)
        logger.info(message)

    @classmethod
    def debug(cls, message: str, name: str = "NWACS"):
        """记录DEBUG级别日志"""
        logger = cls.get_logger(name)
        logger.debug(message)

    @classmethod
    def warning(cls, message: str, name: str = "NWACS"):
        """记录WARNING级别日志"""
        logger = cls.get_logger(name)
        logger.warning(message)

    @classmethod
    def error(cls, message: str, name: str = "NWACS"):
        """记录ERROR级别日志"""
        logger = cls.get_logger(name)
        logger.error(message)

    @classmethod
    def critical(cls, message: str, name: str = "NWACS"):
        """记录CRITICAL级别日志"""
        logger = cls.get_logger(name)
        logger.critical(message)


# 快捷函数
def get_logger(name: str = "NWACS"):
    """获取日志记录器"""
    return NWACSLogger.get_logger(name)

def log_info(message: str, name: str = "NWACS"):
    """记录INFO日志"""
    NWACSLogger.info(message, name)

def log_debug(message: str, name: str = "NWACS"):
    """记录DEBUG日志"""
    NWACSLogger.debug(message, name)

def log_warning(message: str, name: str = "NWACS"):
    """记录WARNING日志"""
    NWACSLogger.warning(message, name)

def log_error(message: str, name: str = "NWACS"):
    """记录ERROR日志"""
    NWACSLogger.error(message, name)
