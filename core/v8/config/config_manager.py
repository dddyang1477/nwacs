#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS V8.0 配置管理系统
核心功能：
1. 配置加载与解析
2. 配置验证
3. 动态配置更新
4. 配置版本管理
"""

import sys
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional, List
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding='utf-8')
except (AttributeError, OSError):
    pass

class ConfigValidator:
    """配置验证器"""
    
    @staticmethod
    def validate_api_keys(config: Dict[str, Any]) -> List[str]:
        """验证API密钥"""
        errors = []
        
        # 验证DeepSeek API密钥
        deepseek_key = config.get("deepseek", {}).get("api_key", "")
        if not deepseek_key or len(deepseek_key) < 10:
            errors.append("DeepSeek API密钥无效")
        
        return errors
    
    @staticmethod
    def validate_paths(config: Dict[str, Any]) -> List[str]:
        """验证路径配置"""
        errors = []
        
        paths = config.get("paths", {})
        required_dirs = ["data", "logs", "skills", "knowledge_base"]
        
        for dir_name in required_dirs:
            dir_path = paths.get(dir_name)
            if dir_path:
                if not os.path.exists(dir_path):
                    try:
                        os.makedirs(dir_path, exist_ok=True)
                    except Exception as e:
                        errors.append(f"无法创建目录 {dir_path}: {e}")
        
        return errors
    
    @staticmethod
    def validate_model_config(config: Dict[str, Any]) -> List[str]:
        """验证模型配置"""
        errors = []
        
        models = config.get("models", {})
        if not models:
            errors.append("未配置任何AI模型")
        
        for model_name, model_config in models.items():
            if not model_config.get("enabled", True):
                continue
            
            if not model_config.get("api_key") and not model_config.get("local_path"):
                errors.append(f"模型 {model_name} 缺少API密钥或本地路径")
        
        return errors
    
    @staticmethod
    def validate_all(config: Dict[str, Any]) -> List[str]:
        """全面验证配置"""
        errors = []
        errors.extend(ConfigValidator.validate_api_keys(config))
        errors.extend(ConfigValidator.validate_paths(config))
        errors.extend(ConfigValidator.validate_model_config(config))
        return errors

class ConfigManager:
    """配置管理器"""
    
    _instance = None
    _config = None
    _config_path = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def initialize(self, config_path: str = None):
        """初始化配置管理器"""
        self._config_path = config_path or "config/config.json"
        self.load_config()
    
    def load_config(self):
        """加载配置文件"""
        default_config = self._get_default_config()
        
        if os.path.exists(self._config_path):
            try:
                with open(self._config_path, 'r', encoding='utf-8') as f:
                    self._config = json.load(f)
                # 合并默认配置
                self._config = self._merge_configs(default_config, self._config)
            except Exception as e:
                print(f"加载配置文件失败，使用默认配置: {e}")
                self._config = default_config
        else:
            self._config = default_config
            self.save_config()
        
        # 验证配置
        errors = ConfigValidator.validate_all(self._config)
        if errors:
            print("配置验证警告:")
            for error in errors:
                print(f"  - {error}")
    
    def _get_default_config(self) -> Dict[str, Any]:
        """获取默认配置"""
        return {
            "version": "8.0.0",
            "name": "NWACS V8.0",
            "description": "Novel Writing AI Collaborative System",
            "author": "NWACS Team",
            "created_at": datetime.now().isoformat(),
            
            "deepseek": {
                "api_key": "sk-f3246fbd1eef446e9a11d78efefd9bba",
                "base_url": "https://api.deepseek.com",
                "timeout": 120,
                "max_tokens": 8000,
                "temperature": 0.7
            },
            
            "models": {
                "deepseek": {
                    "enabled": True,
                    "api_key": "sk-f3246fbd1eef446e9a11d78efefd9bba",
                    "model_name": "deepseek-chat"
                }
            },
            
            "paths": {
                "data": "data",
                "logs": "logs",
                "skills": "skills",
                "knowledge_base": "knowledge_base",
                "output": "output",
                "novels": "novels"
            },
            
            "server": {
                "host": "127.0.0.1",
                "port": 8000,
                "debug": True,
                "workers": 4
            },
            
            "logging": {
                "level": "INFO",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "file_max_bytes": 10485760,
                "file_backup_count": 5
            },
            
            "feishu": {
                "enabled": True,
                "webhook_url": "https://open.feishu.cn/open-apis/bot/v2/hook/c808e5d5-1912-4795-9347-a05cc15c5b89",
                "secret": "",
                "push_events": ["task_start", "task_progress", "task_complete", "learning_complete", "quality_warning"],
                "feature_flags": {
                    "enable_progress_push": True,
                    "enable_learning_report": True,
                    "enable_markdown": True
                }
            },
            
            "features": {
                "creative_engine": True,
                "skill_manager": True,
                "knowledge_base": True,
                "multi_model": True,
                "real_time_collaboration": False,
                "web_ui": True,
                "api_gateway": True
            },
            
            "performance": {
                "cache_enabled": True,
                "cache_ttl": 3600,
                "rate_limit": 100,
                "rate_limit_window": 60
            }
        }
    
    def _merge_configs(self, default: Dict[str, Any], custom: Dict[str, Any]) -> Dict[str, Any]:
        """合并配置"""
        result = default.copy()
        
        def merge_dict(d1: Dict, d2: Dict):
            for key, value in d2.items():
                if key in d1 and isinstance(d1[key], dict) and isinstance(value, dict):
                    merge_dict(d1[key], value)
                else:
                    d1[key] = value
        
        merge_dict(result, custom)
        return result
    
    def save_config(self):
        """保存配置文件"""
        config_dir = os.path.dirname(self._config_path)
        if config_dir and not os.path.exists(config_dir):
            os.makedirs(config_dir, exist_ok=True)
        
        with open(self._config_path, 'w', encoding='utf-8') as f:
            json.dump(self._config, f, indent=2, ensure_ascii=False)
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值"""
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """设置配置值"""
        keys = key.split('.')
        config = self._config
        
        for i, k in enumerate(keys[:-1]):
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
        self.save_config()
    
    def get_all(self) -> Dict[str, Any]:
        """获取所有配置"""
        return self._config
    
    def validate(self) -> List[str]:
        """验证配置"""
        return ConfigValidator.validate_all(self._config)

class ConfigBuilder:
    """配置构建器"""
    
    @staticmethod
    def create_default_config() -> ConfigManager:
        """创建默认配置管理器"""
        config_manager = ConfigManager()
        config_manager.initialize()
        return config_manager
    
    @staticmethod
    def create_from_file(config_path: str) -> ConfigManager:
        """从文件创建配置管理器"""
        config_manager = ConfigManager()
        config_manager.initialize(config_path)
        return config_manager

if __name__ == "__main__":
    print("="*60)
    print("🚀 NWACS V8.0 配置管理系统测试")
    print("="*60)
    
    config = ConfigBuilder.create_default_config()
    
    print("\n1. 获取配置值...")
    version = config.get("version")
    print(f"   - 版本: {version}")
    
    api_key = config.get("deepseek.api_key")
    print(f"   - DeepSeek API Key: {api_key[:10]}...")
    
    server_port = config.get("server.port")
    print(f"   - 服务器端口: {server_port}")
    
    print("\n2. 设置配置值...")
    config.set("server.debug", False)
    debug = config.get("server.debug")
    print(f"   - 调试模式已设置为: {debug}")
    
    print("\n3. 验证配置...")
    errors = config.validate()
    if errors:
        print("   ❌ 配置验证失败:")
        for error in errors:
            print(f"      - {error}")
    else:
        print("   ✅ 配置验证通过")
    
    print("\n4. 获取统计信息...")
    all_config = config.get_all()
    print(f"   - 配置键数量: {len(all_config.keys())}")
    
    print("\n" + "="*60)
    print("🎉 配置管理系统测试完成！")
    print("="*60)
