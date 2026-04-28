#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 容错机制系统 v1.0
提供重试、降级、熔断等容错能力
"""

import time
import threading
from logger import logger

class RetryDecorator:
    """重试装饰器"""
    
    def __init__(self, max_retries=3, delay=1, backoff=2):
        self.max_retries = max_retries
        self.delay = delay
        self.backoff = backoff
    
    def __call__(self, func):
        def wrapper(*args, **kwargs):
            last_exception = None
            delay = self.delay
            
            for attempt in range(self.max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    logger.warning("第 %d 次尝试失败: %s" % (attempt + 1, str(e)))
                    
                    if attempt < self.max_retries - 1:
                        logger.info("等待 %d 秒后重试..." % delay)
                        time.sleep(delay)
                        delay *= self.backoff
            
            logger.error("重试 %d 次后仍然失败" % self.max_retries)
            raise last_exception
        
        return wrapper

class CircuitBreaker:
    """断路器模式实现"""
    
    def __init__(self, failure_threshold=5, recovery_timeout=30):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.is_open = False
        self.last_failure_time = 0
        self.lock = threading.Lock()
    
    def __call__(self, func):
        def wrapper(*args, **kwargs):
            with self.lock:
                # 检查断路器状态
                if self.is_open:
                    # 检查是否可以尝试恢复
                    if time.time() - self.last_failure_time >= self.recovery_timeout:
                        logger.info("断路器尝试恢复")
                        self.is_open = False
                        self.failure_count = 0
                    else:
                        logger.error("断路器已打开，拒绝请求")
                        raise CircuitBreakerError("Circuit breaker is open")
            
            try:
                result = func(*args, **kwargs)
                # 成功时重置计数器
                with self.lock:
                    self.failure_count = 0
                return result
            except Exception as e:
                with self.lock:
                    self.failure_count += 1
                    self.last_failure_time = time.time()
                    
                    if self.failure_count >= self.failure_threshold:
                        logger.warning("断路器打开，失败次数: %d" % self.failure_count)
                        self.is_open = True
                
                raise
        
        return wrapper

class CircuitBreakerError(Exception):
    """断路器异常"""
    pass

class FallbackDecorator:
    """降级装饰器"""
    
    def __init__(self, fallback_func=None):
        self.fallback_func = fallback_func
    
    def __call__(self, func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.warning("主函数执行失败，使用降级方案: %s" % str(e))
                
                if self.fallback_func:
                    try:
                        return self.fallback_func(*args, **kwargs)
                    except Exception as fallback_e:
                        logger.error("降级方案也失败了: %s" % str(fallback_e))
                        raise
                else:
                    logger.error("没有设置降级方案")
                    raise
        
        return wrapper

class RateLimiter:
    """速率限制器"""
    
    def __init__(self, max_requests=100, time_window=60):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = []
        self.lock = threading.Lock()
    
    def acquire(self):
        """获取请求许可"""
        with self.lock:
            now = time.time()
            # 移除时间窗口外的请求记录
            self.requests = [r for r in self.requests if now - r < self.time_window]
            
            if len(self.requests) >= self.max_requests:
                return False
            
            self.requests.append(now)
            return True
    
    def __call__(self, func):
        def wrapper(*args, **kwargs):
            if not self.acquire():
                raise RateLimitError("Rate limit exceeded")
            return func(*args, **kwargs)
        
        return wrapper

class RateLimitError(Exception):
    """速率限制异常"""
    pass

class ResourceProtector:
    """资源保护器"""
    
    def __init__(self, max_concurrent=10):
        self.max_concurrent = max_concurrent
        self.current_concurrent = 0
        self.lock = threading.Lock()
    
    def acquire(self):
        """获取资源"""
        with self.lock:
            if self.current_concurrent >= self.max_concurrent:
                return False
            self.current_concurrent += 1
            return True
    
    def release(self):
        """释放资源"""
        with self.lock:
            if self.current_concurrent > 0:
                self.current_concurrent -= 1
    
    def __call__(self, func):
        def wrapper(*args, **kwargs):
            if not self.acquire():
                raise ResourceExhaustedError("Resource exhausted")
            
            try:
                return func(*args, **kwargs)
            finally:
                self.release()
        
        return wrapper

class ResourceExhaustedError(Exception):
    """资源耗尽异常"""
    pass

# 全局容错组件
retry_on_failure = RetryDecorator(max_retries=3, delay=1, backoff=2)
circuit_breaker = CircuitBreaker(failure_threshold=5, recovery_timeout=30)
rate_limiter = RateLimiter(max_requests=100, time_window=60)
resource_protector = ResourceProtector(max_concurrent=10)

# 测试容错机制
if __name__ == "__main__":
    # 测试重试机制
    @retry_on_failure
    def unstable_function(fail_times=2):
        if not hasattr(unstable_function, 'call_count'):
            unstable_function.call_count = 0
        unstable_function.call_count += 1
        
        if unstable_function.call_count <= fail_times:
            raise ValueError("故意失败第 %d 次" % unstable_function.call_count)
        
        return "成功！调用次数: %d" % unstable_function.call_count
    
    try:
        result = unstable_function()
        print("重试测试结果:", result)
    except Exception as e:
        print("重试测试失败:", str(e))
    
    # 测试断路器
    @circuit_breaker
    def always_fail():
        raise ValueError("总是失败")
    
    for i in range(6):
        try:
            always_fail()
        except Exception as e:
            print("断路器测试 %d:" % (i+1), str(e))