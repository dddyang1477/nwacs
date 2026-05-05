#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS v7.0 性能优化模块
提供缓存、异步任务、性能监控等功能
"""

import os
import json
import time
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from typing import Any, Optional, Callable
from functools import wraps
import threading


class CacheManager:
    """缓存管理器"""

    def __init__(self, cache_dir: Path = None, max_age_seconds: int = 3600):
        self.cache_dir = cache_dir or (Path(__file__).parent.parent / "user_data" / "cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.max_age = max_age_seconds
        self.memory_cache = {}
        self._lock = threading.Lock()

    def _get_cache_key(self, key: str) -> str:
        """生成缓存key的hash"""
        return hashlib.md5(key.encode()).hexdigest()

    def _get_cache_path(self, key: str) -> Path:
        """获取缓存文件路径"""
        cache_key = self._get_cache_key(key)
        return self.cache_dir / f"{cache_key}.json"

    def get(self, key: str) -> Optional[Any]:
        """获取缓存"""
        # 先检查内存缓存
        with self._lock:
            if key in self.memory_cache:
                cached = self.memory_cache[key]
                if time.time() - cached['timestamp'] < self.max_age:
                    return cached['data']
                else:
                    del self.memory_cache[key]

        # 检查文件缓存
        cache_path = self._get_cache_path(key)
        if cache_path.exists():
            try:
                with open(cache_path, 'r', encoding='utf-8') as f:
                    cached = json.load(f)

                if time.time() - cached['timestamp'] < self.max_age:
                    # 更新内存缓存
                    with self._lock:
                        self.memory_cache[key] = cached
                    return cached['data']
                else:
                    cache_path.unlink()
            except Exception:
                pass

        return None

    def set(self, key: str, data: Any) -> bool:
        """设置缓存"""
        cached = {
            'data': data,
            'timestamp': time.time()
        }

        # 更新内存缓存
        with self._lock:
            self.memory_cache[key] = cached

        # 更新文件缓存
        cache_path = self._get_cache_path(key)
        try:
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(cached, f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False

    def delete(self, key: str) -> bool:
        """删除缓存"""
        with self._lock:
            if key in self.memory_cache:
                del self.memory_cache[key]

        cache_path = self._get_cache_path(key)
        if cache_path.exists():
            cache_path.unlink()
            return True
        return False

    def clear_all(self) -> int:
        """清空所有缓存"""
        count = 0
        with self._lock:
            self.memory_cache.clear()

        for cache_file in self.cache_dir.glob("*.json"):
            cache_file.unlink()
            count += 1

        return count

    def get_stats(self) -> dict:
        """获取缓存统计"""
        file_count = len(list(self.cache_dir.glob("*.json")))
        memory_count = len(self.memory_cache)

        total_size = sum(f.stat().st_size for f in self.cache_dir.glob("*.json"))

        return {
            "memory_entries": memory_count,
            "file_entries": file_count,
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / 1024 / 1024, 2)
        }


class AsyncTaskQueue:
    """异步任务队列"""

    def __init__(self):
        self.tasks = {}
        self.results = {}
        self._lock = threading.Lock()

    def add_task(self, task_id: str, task_func: Callable, *args, **kwargs) -> str:
        """添加异步任务"""
        with self._lock:
            self.tasks[task_id] = {
                'func': task_func,
                'args': args,
                'kwargs': kwargs,
                'status': 'pending',
                'created_at': time.time()
            }
            self.results[task_id] = None

        # 启动后台线程执行
        thread = threading.Thread(target=self._run_task, args=(task_id,))
        thread.daemon = True
        thread.start()

        return task_id

    def _run_task(self, task_id: str):
        """运行任务"""
        with self._lock:
            if task_id not in self.tasks:
                return
            task = self.tasks[task_id]
            task['status'] = 'running'
            task['started_at'] = time.time()

        try:
            result = task['func'](*task['args'], **task['kwargs'])
            with self._lock:
                self.results[task_id] = {'success': True, 'data': result}
                self.tasks[task_id]['status'] = 'completed'
        except Exception as e:
            with self._lock:
                self.results[task_id] = {'success': False, 'error': str(e)}
                self.tasks[task_id]['status'] = 'failed'
        finally:
            with self._lock:
                self.tasks[task_id]['completed_at'] = time.time()

    def get_result(self, task_id: str, timeout: float = 30.0) -> Optional[dict]:
        """获取任务结果"""
        start = time.time()
        while time.time() - start < timeout:
            with self._lock:
                if task_id in self.results:
                    result = self.results[task_id]
                    if result:
                        return result
                if task_id in self.tasks:
                    status = self.tasks[task_id]['status']
                    if status in ['completed', 'failed']:
                        return self.results.get(task_id)

            time.sleep(0.1)

        return None

    def get_status(self, task_id: str) -> Optional[dict]:
        """获取任务状态"""
        with self._lock:
            if task_id in self.tasks:
                task = self.tasks[task_id].copy()
                if 'func' in task:
                    del task['func']
                if 'args' in task:
                    del task['args']
                if 'kwargs' in task:
                    del task['kwargs']
                return task
        return None

    def list_tasks(self) -> list:
        """列出所有任务"""
        with self._lock:
            return [
                {
                    'task_id': tid,
                    'status': t['status'],
                    'created_at': t['created_at']
                }
                for tid, t in self.tasks.items()
            ]


class PerformanceMonitor:
    """性能监控器"""

    def __init__(self):
        self.metrics = []
        self.start_time = time.time()
        self._lock = threading.Lock()

    def record(self, operation: str, duration: float, success: bool = True):
        """记录性能指标"""
        with self._lock:
            self.metrics.append({
                'operation': operation,
                'duration': duration,
                'success': success,
                'timestamp': time.time()
            })

            # 保持最近1000条记录
            if len(self.metrics) > 1000:
                self.metrics = self.metrics[-1000:]

    def get_stats(self, operation: str = None) -> dict:
        """获取性能统计"""
        with self._lock:
            if operation:
                metrics = [m for m in self.metrics if m['operation'] == operation]
            else:
                metrics = self.metrics

            if not metrics:
                return {
                    'total_calls': 0,
                    'success_rate': 0,
                    'avg_duration': 0,
                    'min_duration': 0,
                    'max_duration': 0
                }

            durations = [m['duration'] for m in metrics]
            successes = [m['success'] for m in metrics]

            return {
                'total_calls': len(metrics),
                'success_rate': sum(successes) / len(successes) * 100,
                'avg_duration': sum(durations) / len(durations),
                'min_duration': min(durations),
                'max_duration': max(durations),
                'total_duration': sum(durations)
            }

    def get_top_operations(self, limit: int = 10) -> list:
        """获取最耗时操作"""
        with self._lock:
            operation_stats = {}
            for m in self.metrics:
                op = m['operation']
                if op not in operation_stats:
                    operation_stats[op] = []
                operation_stats[op].append(m['duration'])

            results = []
            for op, durations in operation_stats.items():
                results.append({
                    'operation': op,
                    'calls': len(durations),
                    'avg_duration': sum(durations) / len(durations),
                    'total_duration': sum(durations)
                })

            results.sort(key=lambda x: x['total_duration'], reverse=True)
            return results[:limit]


def timed_cache(cache_manager: CacheManager, cache_key: str):
    """缓存装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 生成缓存key
            key = f"{cache_key}:{str(args)}:{str(kwargs)}"

            # 尝试获取缓存
            cached = cache_manager.get(key)
            if cached is not None:
                return cached

            # 执行函数
            result = func(*args, **kwargs)

            # 缓存结果
            cache_manager.set(key, result)

            return result
        return wrapper
    return decorator


def async_task(task_id: str):
    """异步任务装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 这里简化处理，实际应该用AsyncTaskQueue
            return func(*args, **kwargs)
        return wrapper
    return decorator


# 全局实例
cache_manager = CacheManager()
task_queue = AsyncTaskQueue()
perf_monitor = PerformanceMonitor()


def main():
    """演示"""
    print("="*60)
    print("🚀 NWACS性能优化模块演示")
    print("="*60)

    # 缓存演示
    print("\n📦 缓存管理演示")
    cache = CacheManager()

    cache.set("test_key", {"data": "test_value"})
    result = cache.get("test_key")
    print(f"  设置缓存: test_key")
    print(f"  获取缓存: {result}")

    stats = cache.get_stats()
    print(f"  缓存统计: {stats}")

    # 性能监控演示
    print("\n📊 性能监控演示")

    perf_monitor.record("novel_generation", 2.5, True)
    perf_monitor.record("novel_generation", 3.1, True)
    perf_monitor.record("quality_check", 0.5, True)

    stats = perf_monitor.get_stats()
    print(f"  小说生成性能: {stats}")

    top_ops = perf_monitor.get_top_operations()
    print(f"  最耗时操作: {top_ops}")

    print("\n✅ 性能优化模块演示完成！")


if __name__ == "__main__":
    main()
