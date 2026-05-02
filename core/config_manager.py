#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 统一配置管理器
配置中心化管理，所有模块从这里获取配置
"""
import os
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any

class ConfigManager:
    """NWACS统一配置管理器"""

    _instance = None
    _config = None

    def __new__(cls):
        """单例模式"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """初始化"""
        if self._config is None:
            self._load_config()

    @property
    def PROJECT_ROOT(self) -> Path:
        """项目根目录"""
        return Path(__file__).parent.parent

    @property
    def CONFIG_DIR(self) -> Path:
        """配置目录"""
        return self.PROJECT_ROOT / "config"

    @property
    def LOG_DIR(self) -> Path:
        """日志目录"""
        log_dir = self.PROJECT_ROOT / "logs"
        log_dir.mkdir(exist_ok=True)
        return log_dir

    @property
    def LEARNING_DIR(self) -> Path:
        """学习目录"""
        return self.PROJECT_ROOT / "skills" / "level2" / "learnings"

    def _load_config(self):
        """加载配置"""
        config_path = self.CONFIG_DIR / "feishu_config.json"

        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    self._config = json.load(f)
            except Exception as e:
                print(f"[Config] 配置加载失败: {e}")
                self._config = self._get_default_config()
        else:
            self._config = self._get_default_config()

    def _get_default_config(self) -> Dict[str, Any]:
        """获取默认配置"""
        return {
            "enable": True,
            "webhook_url": "",
            "secret": "",
            "push_events": [
                "task_start",
                "task_progress",
                "task_complete",
                "learning_complete",
                "quality_warning"
            ],
            "feature_flags": {
                "enable_progress_push": True,
                "enable_learning_report": True,
                "enable_markdown": True
            }
        }

    def get(self, key: str, default: Any = None) -> Any:
        """获取配置项"""
        keys = key.split('.')
        value = self._config

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default

        return value

    def set(self, key: str, value: Any):
        """设置配置项"""
        keys = key.split('.')
        config = self._config

        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]

        config[keys[-1]] = value

    def save(self):
        """保存配置到文件"""
        config_path = self.CONFIG_DIR / "feishu_config.json"

        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"[Config] 保存配置失败: {e}")
            return False

    @property
    def feishu_webhook_url(self) -> str:
        """飞书Webhook URL"""
        return self.get("webhook_url", "")

    @property
    def feishu_enabled(self) -> bool:
        """飞书是否启用"""
        return self.get("enable", False)

    @property
    def deepseek_api_key(self) -> str:
        """DeepSeek API Key"""
        return self.get("deepseek_api_key", "sk-f3246fbd1eef446e9a11d78efefd9bba")

    @property
    def deepseek_api_url(self) -> str:
        """DeepSeek API URL"""
        return self.get("deepseek_api_url", "https://api.deepseek.com/v1/chat/completions")

    def get_log_path(self, name: str) -> Path:
        """获取日志文件路径"""
        return self.LOG_DIR / f"{name}_{datetime.now().strftime('%Y%m%d')}.log"

    def __repr__(self):
        return f"ConfigManager(root={self.PROJECT_ROOT})"


# 全局配置实例
config = ConfigManager()
