#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 大模型连接优化模块
功能：余额检测、限流重试、本地缓存、多模型支持
"""

import os
import time
import json
import hashlib
from datetime import datetime, timedelta
from logger import logger

class LLMConnectionOptimizer:
    """大模型连接优化器"""
    
    def __init__(self):
        self.api_key = None
        self.base_url = None
        self.model = None
        self.enabled = False
        
        # 限流控制
        self.request_count = 0
        self.request_limit = 100  # 每小时最多 100 次请求
        self.last_request_time = 0
        self.request_interval = 2  # 最小请求间隔（秒）
        
        # 重试机制
        self.max_retries = 3
        self.retry_delay = 1  # 重试延迟（秒）
        
        # 本地缓存
        self.cache = {}
        self.cache_file = "llm_response_cache.json"
        self.cache_expiry = 3600  # 缓存有效期 1 小时
        
        # 余额检测
        self.balance = None
        self.last_balance_check = 0
        self.balance_check_interval = 3600  # 每小时检查一次余额
        
        # 多模型配置
        self.models_config = {
            'deepseek-chat': {
                'priority': 1,
                'cost_per_1k': 0.001,
                'max_tokens': 4096,
                'suitable_for': ['创作', '分析', '总结']
            },
            'deepseek-coder': {
                'priority': 2,
                'cost_per_1k': 0.001,
                'max_tokens': 4096,
                'suitable_for': ['代码生成', '代码优化']
            },
            'gpt-3.5-turbo': {
                'priority': 3,
                'cost_per_1k': 0.002,
                'max_tokens': 4096,
                'suitable_for': ['对话', '翻译']
            }
        }
        
        self._load_config()
        self._load_cache()
    
    def _load_config(self):
        """加载配置"""
        config_file = 'config.json'
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                self.api_key = config.get('api_key')
                self.base_url = config.get('base_url')
                self.model = config.get('model', 'deepseek-chat')
                self.enabled = config.get('enabled', True)
                
                logger.info("大模型配置已加载：%s" % self.model)
            except Exception as e:
                logger.log_exception(e, "加载大模型配置")
    
    def _load_cache(self):
        """加载缓存"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    self.cache = json.load(f)
                logger.info("大模型响应缓存已加载，共 %d 条" % len(self.cache))
            except Exception:
                self.cache = {}
    
    def _save_cache(self):
        """保存缓存"""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.log_exception(e, "保存缓存")
    
    def _generate_cache_key(self, prompt, model, temperature):
        """生成缓存键"""
        key_str = "%s|%s|%s" % (prompt, model, temperature)
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def get_from_cache(self, prompt, model, temperature=0.7):
        """从缓存获取响应"""
        cache_key = self._generate_cache_key(prompt, model, temperature)
        
        if cache_key in self.cache:
            cache_data = self.cache[cache_key]
            cache_time = datetime.fromisoformat(cache_data['timestamp'])
            
            # 检查缓存是否过期
            if datetime.now() - cache_time < timedelta(seconds=self.cache_expiry):
                logger.debug("命中缓存")
                return cache_data['response']
            else:
                # 删除过期缓存
                del self.cache[cache_key]
                self._save_cache()
        
        return None
    
    def save_to_cache(self, prompt, model, temperature, response):
        """保存响应到缓存"""
        cache_key = self._generate_cache_key(prompt, model, temperature)
        
        self.cache[cache_key] = {
            'prompt': prompt[:100],  # 只保存前 100 字用于识别
            'response': response,
            'model': model,
            'temperature': temperature,
            'timestamp': datetime.now().isoformat(),
            'tokens_used': len(response) // 4  # 估算 token 数
        }
        
        self._save_cache()
        logger.debug("响应已缓存")
    
    def check_rate_limit(self):
        """检查请求限流"""
        current_time = time.time()
        
        # 检查请求间隔
        if current_time - self.last_request_time < self.request_interval:
            wait_time = self.request_interval - (current_time - self.last_request_time)
            logger.debug("触发限流，等待 %.2f 秒" % wait_time)
            time.sleep(wait_time)
        
        # 检查每小时请求数
        if self.request_count >= self.request_limit:
            logger.warning("达到每小时请求上限，等待 60 秒")
            time.sleep(60)
            self.request_count = 0
        
        self.request_count += 1
        self.last_request_time = current_time
    
    def check_balance(self, client):
        """检查 API 余额（模拟实现，实际需要根据 API 文档实现）"""
        current_time = time.time()
        
        # 避免频繁检查
        if current_time - self.last_balance_check < self.balance_check_interval:
            return self.balance
        
        try:
            # 注意：DeepSeek API 目前没有官方的余额查询接口
            # 这里使用模拟实现，实际项目中需要根据 API 文档调整
            self.balance = {
                'available': True,  # 假设余额充足
                'amount': 100.0,  # 模拟余额
                'last_check': datetime.now().isoformat()
            }
            
            self.last_balance_check = current_time
            logger.info("余额检查完成：%.2f" % self.balance['amount'])
            
            return self.balance
            
        except Exception as e:
            logger.log_exception(e, "检查余额")
            self.balance = {'available': True, 'amount': 100.0}
            return self.balance
    
    def execute_with_retry(self, func, *args, **kwargs):
        """带重试的执行"""
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                # 检查限流
                self.check_rate_limit()
                
                # 执行请求
                result = func(*args, **kwargs)
                return result
                
            except Exception as e:
                last_error = e
                logger.warning("请求失败（第 %d 次）: %s" % (attempt + 1, str(e)))
                
                if attempt < self.max_retries - 1:
                    # 等待后重试
                    wait_time = self.retry_delay * (2 ** attempt)  # 指数退避
                    logger.info("等待 %.2f 秒后重试..." % wait_time)
                    time.sleep(wait_time)
        
        # 所有重试失败
        logger.error("所有重试失败：%s" % str(last_error))
        raise last_error
    
    def select_best_model(self, task_type):
        """根据任务类型选择最佳模型"""
        suitable_models = []
        
        for model_name, config in self.models_config.items():
            if task_type in config['suitable_for']:
                suitable_models.append((model_name, config['priority']))
        
        if suitable_models:
            # 选择优先级最高的
            suitable_models.sort(key=lambda x: x[1])
            selected = suitable_models[0][0]
            logger.info("为任务 '%s' 选择模型：%s" % (task_type, selected))
            return selected
        
        # 默认使用配置的模型
        return self.model
    
    def estimate_cost(self, text_length, model=None):
        """估算成本"""
        model = model or self.model
        tokens = text_length // 4  # 估算 token 数
        
        if model in self.models_config:
            cost_per_1k = self.models_config[model]['cost_per_1k']
            estimated_cost = (tokens / 1000) * cost_per_1k
            return estimated_cost
        
        return 0.0
    
    def get_statistics(self):
        """获取统计信息"""
        return {
            'request_count': self.request_count,
            'cache_size': len(self.cache),
            'balance': self.balance,
            'enabled': self.enabled,
            'current_model': self.model
        }


# 全局优化器实例
llm_optimizer = LLMConnectionOptimizer()


def get_llm_optimizer():
    """获取大模型优化器实例"""
    return llm_optimizer
