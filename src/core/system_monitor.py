#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 系统监控面板 v2.0
提供系统状态监控和可视化展示
新增：真实性能监控、任务队列监控、学习进度追踪
"""

import os
import time
import json
import threading
from datetime import datetime
from logger import logger

# 尝试导入psutil进行真实性能监控
try:
    import psutil
    HAS_PSUTIL = True
    logger.info("已导入psutil，支持真实性能监控")
except ImportError:
    HAS_PSUTIL = False
    logger.warning("未安装psutil，将使用模拟数据")

class SystemMonitor:
    def __init__(self):
        self.start_time = datetime.now()
        self.metrics = {
            'learning': {
                'total_learning': 0,
                'successful_learning': 0,
                'failed_learning': 0,
                'average_score': 0,
                'last_learning_time': None,
                'learning_speed': 0,  # 学习次数/小时
                'learning_trend': 0   # 趋势变化
            },
            'skills': {
                'total_skills': 0,
                'active_skills': 0,
                'executed_count': 0,
                'error_count': 0,
                'success_rate': 0,
                'avg_response_time': 0
            },
            'system': {
                'uptime': 0,
                'memory_usage': 0,
                'memory_usage_percent': 0,
                'cpu_usage': 0,
                'cpu_cores': 0,
                'disk_usage': 0,
                'disk_usage_percent': 0,
                'network_status': 'unknown',
                'error_count': 0
            },
            'topics': {
                'total_topics': 0,
                'categories': [],
                'last_update': None,
                'avg_priority': 0
            },
            'tasks': {
                'pending_tasks': 0,
                'active_tasks': 0,
                'completed_tasks': 0,
                'failed_tasks': 0,
                'avg_task_duration': 0
            }
        }
        
        # 性能历史记录
        self.performance_history = []
        self.history_max_length = 60  # 保留60条记录
        
        # 启动监控线程
        self.monitor_thread = threading.Thread(target=self.monitor_loop)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        
        logger.info("系统监控面板初始化完成")
    
    def monitor_loop(self):
        """监控循环"""
        while True:
            self.update_system_metrics()
            self.record_performance()
            time.sleep(30)  # 每30秒更新一次
    
    def update_learning_metrics(self, success=True, score=0):
        """更新学习指标"""
        self.metrics['learning']['total_learning'] += 1
        
        if success:
            self.metrics['learning']['successful_learning'] += 1
            self.metrics['learning']['last_learning_time'] = datetime.now().isoformat()
            
            # 更新平均评分
            current_avg = self.metrics['learning']['average_score']
            if current_avg == 0:
                self.metrics['learning']['average_score'] = score
            else:
                total = current_avg * (self.metrics['learning']['successful_learning'] - 1) + score
                self.metrics['learning']['average_score'] = round(total / self.metrics['learning']['successful_learning'])
        else:
            self.metrics['learning']['failed_learning'] += 1
    
    def update_skill_metrics(self, total_skills, active_skills, executed_count, error_count):
        """更新Skill指标"""
        self.metrics['skills']['total_skills'] = total_skills
        self.metrics['skills']['active_skills'] = active_skills
        self.metrics['skills']['executed_count'] = executed_count
        self.metrics['skills']['error_count'] = error_count
    
    def update_system_metrics(self):
        """更新系统指标"""
        # 计算运行时间
        uptime = datetime.now() - self.start_time
        self.metrics['system']['uptime'] = str(uptime).split('.')[0]
        
        # 使用psutil获取真实性能数据
        if HAS_PSUTIL:
            self.metrics['system']['memory_usage'] = self._get_memory_usage()
            self.metrics['system']['memory_usage_percent'] = self._get_memory_usage_percent()
            self.metrics['system']['cpu_usage'] = self._get_cpu_usage()
            self.metrics['system']['cpu_cores'] = psutil.cpu_count()
            self.metrics['system']['disk_usage'] = self._get_disk_usage()
            self.metrics['system']['disk_usage_percent'] = self._get_disk_usage_percent()
            self.metrics['system']['network_status'] = self._get_network_status()
        else:
            # 使用模拟数据
            self.metrics['system']['memory_usage'] = self._get_memory_usage()
            self.metrics['system']['memory_usage_percent'] = 25
            self.metrics['system']['cpu_usage'] = self._get_cpu_usage()
            self.metrics['system']['cpu_cores'] = 4
            self.metrics['system']['disk_usage'] = 10240
            self.metrics['system']['disk_usage_percent'] = 30
            self.metrics['system']['network_status'] = 'unknown'
    
    def update_topic_metrics(self, total_topics, categories, last_update, avg_priority=0):
        """更新主题指标"""
        self.metrics['topics']['total_topics'] = total_topics
        self.metrics['topics']['categories'] = categories
        self.metrics['topics']['last_update'] = last_update
        self.metrics['topics']['avg_priority'] = avg_priority
    
    def update_task_metrics(self, pending_tasks, active_tasks, completed_tasks, failed_tasks, avg_duration=0):
        """更新任务队列指标"""
        self.metrics['tasks']['pending_tasks'] = pending_tasks
        self.metrics['tasks']['active_tasks'] = active_tasks
        self.metrics['tasks']['completed_tasks'] = completed_tasks
        self.metrics['tasks']['failed_tasks'] = failed_tasks
        self.metrics['tasks']['avg_task_duration'] = avg_duration
    
    def _get_memory_usage(self):
        """获取内存使用（MB）"""
        if HAS_PSUTIL:
            mem = psutil.virtual_memory()
            return round(mem.used / (1024 * 1024))
        return 128  # MB（模拟）
    
    def _get_memory_usage_percent(self):
        """获取内存使用百分比"""
        if HAS_PSUTIL:
            mem = psutil.virtual_memory()
            return mem.percent
        return 25
    
    def _get_cpu_usage(self):
        """获取CPU使用百分比"""
        if HAS_PSUTIL:
            return round(psutil.cpu_percent(interval=1))
        return 5  # %（模拟）
    
    def _get_disk_usage(self):
        """获取磁盘使用（MB）"""
        if HAS_PSUTIL:
            disk = psutil.disk_usage('/')
            return round(disk.used / (1024 * 1024))
        return 10240  # MB（模拟）
    
    def _get_disk_usage_percent(self):
        """获取磁盘使用百分比"""
        if HAS_PSUTIL:
            disk = psutil.disk_usage('/')
            return disk.percent
        return 30
    
    def _get_network_status(self):
        """获取网络状态"""
        if HAS_PSUTIL:
            try:
                # 检查网络连接
                net_io = psutil.net_io_counters()
                if net_io.bytes_sent > 0 or net_io.bytes_recv > 0:
                    return 'connected'
                return 'disconnected'
            except:
                return 'unknown'
        return 'unknown'
    
    def record_performance(self):
        """记录性能历史"""
        record = {
            'timestamp': datetime.now().isoformat(),
            'cpu_usage': self.metrics['system']['cpu_usage'],
            'memory_usage_percent': self.metrics['system']['memory_usage_percent'],
            'active_tasks': self.metrics['tasks']['active_tasks'],
            'pending_tasks': self.metrics['tasks']['pending_tasks']
        }
        
        self.performance_history.append(record)
        
        # 保持历史记录在限制范围内
        if len(self.performance_history) > self.history_max_length:
            self.performance_history.pop(0)
    
    def get_performance_trend(self):
        """获取性能趋势"""
        if len(self.performance_history) < 2:
            return {'cpu_trend': 0, 'memory_trend': 0}
        
        # 计算趋势（最近10条记录的变化）
        recent = self.performance_history[-10:]
        first_cpu = recent[0]['cpu_usage']
        last_cpu = recent[-1]['cpu_usage']
        first_mem = recent[0]['memory_usage_percent']
        last_mem = recent[-1]['memory_usage_percent']
        
        return {
            'cpu_trend': last_cpu - first_cpu,
            'memory_trend': last_mem - first_mem
        }
    
    def get_status_summary(self):
        """获取状态摘要"""
        summary = {
            'status': 'running',
            'start_time': self.start_time.isoformat(),
            'current_time': datetime.now().isoformat(),
            'metrics': self.metrics
        }
        return summary
    
    def generate_report(self):
        """生成监控报告"""
        self.update_system_metrics()
        
        report = {
            'title': 'NWACS 系统监控报告',
            'generated_at': datetime.now().isoformat(),
            'system_status': self._get_system_status(),
            'performance_trend': self.get_performance_trend(),
            'learning_summary': self._get_learning_summary(),
            'skill_summary': self._get_skill_summary(),
            'topic_summary': self._get_topic_summary(),
            'task_summary': self._get_task_summary(),
            'recommendations': self._generate_recommendations()
        }
        
        return report
    
    def _get_system_status(self):
        """获取系统状态"""
        return {
            'uptime': self.metrics['system']['uptime'],
            'memory_usage': "%d MB" % self.metrics['system']['memory_usage'],
            'memory_usage_percent': "%d%%" % self.metrics['system']['memory_usage_percent'],
            'cpu_usage': "%d%%" % self.metrics['system']['cpu_usage'],
            'cpu_cores': self.metrics['system']['cpu_cores'],
            'disk_usage': "%d MB" % self.metrics['system']['disk_usage'],
            'disk_usage_percent': "%d%%" % self.metrics['system']['disk_usage_percent'],
            'network_status': self.metrics['system']['network_status'],
            'error_count': self.metrics['system']['error_count']
        }
    
    def _get_learning_summary(self):
        """获取学习摘要"""
        total = self.metrics['learning']['total_learning']
        success = self.metrics['learning']['successful_learning']
        failure = self.metrics['learning']['failed_learning']
        
        success_rate = round((success / total) * 100) if total > 0 else 0
        
        return {
            'total_learning': total,
            'successful_learning': success,
            'failed_learning': failure,
            'success_rate': "%d%%" % success_rate,
            'average_score': self.metrics['learning']['average_score'],
            'learning_speed': self.metrics['learning']['learning_speed'],
            'learning_trend': self.metrics['learning']['learning_trend'],
            'last_learning_time': self.metrics['learning']['last_learning_time']
        }
    
    def _get_skill_summary(self):
        """获取Skill摘要"""
        executed = self.metrics['skills']['executed_count']
        errors = self.metrics['skills']['error_count']
        success_rate = round(((executed - errors) / executed) * 100) if executed > 0 else 0
        
        return {
            'total_skills': self.metrics['skills']['total_skills'],
            'active_skills': self.metrics['skills']['active_skills'],
            'executed_count': executed,
            'error_count': errors,
            'success_rate': "%d%%" % success_rate,
            'avg_response_time': "%dms" % self.metrics['skills']['avg_response_time']
        }
    
    def _get_topic_summary(self):
        """获取主题摘要"""
        return {
            'total_topics': self.metrics['topics']['total_topics'],
            'categories': self.metrics['topics']['categories'],
            'category_count': len(self.metrics['topics']['categories']),
            'avg_priority': self.metrics['topics']['avg_priority'],
            'last_update': self.metrics['topics']['last_update']
        }
    
    def _get_task_summary(self):
        """获取任务队列摘要"""
        total = self.metrics['tasks']['completed_tasks'] + self.metrics['tasks']['failed_tasks'] + self.metrics['tasks']['pending_tasks']
        success_rate = round((self.metrics['tasks']['completed_tasks'] / total) * 100) if total > 0 else 0
        
        return {
            'pending_tasks': self.metrics['tasks']['pending_tasks'],
            'active_tasks': self.metrics['tasks']['active_tasks'],
            'completed_tasks': self.metrics['tasks']['completed_tasks'],
            'failed_tasks': self.metrics['tasks']['failed_tasks'],
            'total_tasks': total,
            'success_rate': "%d%%" % success_rate,
            'avg_task_duration': "%dms" % self.metrics['tasks']['avg_task_duration']
        }
    
    def _generate_recommendations(self):
        """生成建议"""
        recommendations = []
        
        # 检查学习成功率
        total = self.metrics['learning']['total_learning']
        success = self.metrics['learning']['successful_learning']
        
        if total > 0:
            success_rate = (success / total) * 100
            if success_rate < 80:
                recommendations.append("学习成功率较低（%.1f%%），建议检查网络连接和学习配置。" % success_rate)
        
        # 检查学习评分
        avg_score = self.metrics['learning']['average_score']
        if avg_score > 0 and avg_score < 70:
            recommendations.append("学习效果评分较低（%d分），建议调整学习方法或增加学习时间。" % avg_score)
        
        # 检查Skill错误率
        executed = self.metrics['skills']['executed_count']
        errors = self.metrics['skills']['error_count']
        if executed > 0:
            error_rate = (errors / executed) * 100
            if error_rate > 10:
                recommendations.append("Skill执行错误率较高（%.1f%%），建议检查Skill配置。" % error_rate)
        
        # 检查内存使用
        mem_usage = self.metrics['system']['memory_usage_percent']
        if mem_usage > 80:
            recommendations.append("内存使用率较高（%d%%），建议关闭不必要的程序或增加内存。" % mem_usage)
        
        # 检查磁盘使用
        disk_usage = self.metrics['system']['disk_usage_percent']
        if disk_usage > 85:
            recommendations.append("磁盘空间紧张（%d%%），建议清理不必要的文件。" % disk_usage)
        
        # 检查任务队列
        pending = self.metrics['tasks']['pending_tasks']
        if pending > 10:
            recommendations.append("任务队列积压（%d个待处理任务），建议增加处理线程数。" % pending)
        
        # 检查网络状态
        if self.metrics['system']['network_status'] == 'disconnected':
            recommendations.append("网络连接断开，建议检查网络配置。")
        
        # 性能趋势警告
        trend = self.get_performance_trend()
        if trend['cpu_trend'] > 20:
            recommendations.append("CPU使用率持续上升，建议优化任务调度。")
        if trend['memory_trend'] > 15:
            recommendations.append("内存使用率持续上升，建议检查内存泄漏。")
        
        if not recommendations:
            recommendations.append("系统运行正常，继续保持！")
        
        return recommendations
    
    def print_dashboard(self):
        """打印监控面板"""
        report = self.generate_report()
        
        print("=" * 65)
        print("           NWACS 系统监控面板 v2.0")
        print("=" * 65)
        print("生成时间: %s" % report['generated_at'])
        print()
        
        # 系统状态
        print("【系统状态】")
        sys = report['system_status']
        print("  运行时间: %s" % sys['uptime'])
        print("  CPU核心: %d | CPU使用率: %s" % (sys['cpu_cores'], sys['cpu_usage']))
        print("  内存使用: %s (%s)" % (sys['memory_usage'], sys['memory_usage_percent']))
        print("  磁盘使用: %s (%s)" % (sys['disk_usage'], sys['disk_usage_percent']))
        print("  网络状态: %s" % sys['network_status'])
        print("  错误次数: %d" % sys['error_count'])
        print()
        
        # 性能趋势
        trend = report['performance_trend']
        print("【性能趋势】")
        print("  CPU趋势: %+d%% | 内存趋势: %+d%%" % (trend['cpu_trend'], trend['memory_trend']))
        print()
        
        # 学习摘要
        print("【学习统计】")
        learn = report['learning_summary']
        print("  总学习次数: %d" % learn['total_learning'])
        print("  成功/失败: %d/%d" % (learn['successful_learning'], learn['failed_learning']))
        print("  成功率: %s" % learn['success_rate'])
        print("  平均评分: %d" % learn['average_score'])
        print("  学习速度: %d 次/小时" % learn['learning_speed'])
        print("  学习趋势: %+d" % learn['learning_trend'])
        print("  上次学习: %s" % (learn['last_learning_time'] or "从未"))
        print()
        
        # Skill摘要
        print("【Skill状态】")
        skill = report['skill_summary']
        print("  总Skill数: %d" % skill['total_skills'])
        print("  活跃Skill数: %d" % skill['active_skills'])
        print("  执行次数: %d" % skill['executed_count'])
        print("  错误次数: %d" % skill['error_count'])
        print("  成功率: %s" % skill['success_rate'])
        print("  平均响应时间: %s" % skill['avg_response_time'])
        print()
        
        # 主题摘要
        print("【学习主题】")
        topic = report['topic_summary']
        print("  总主题数: %d" % topic['total_topics'])
        print("  分类数: %d" % topic['category_count'])
        print("  平均优先级: %d" % topic['avg_priority'])
        print("  分类: %s" % ", ".join(topic['categories']))
        print()
        
        # 任务队列
        tasks = report['task_summary']
        print("【任务队列】")
        print("  待处理任务: %d" % tasks['pending_tasks'])
        print("  活跃任务: %d" % tasks['active_tasks'])
        print("  已完成任务: %d" % tasks['completed_tasks'])
        print("  失败任务: %d" % tasks['failed_tasks'])
        print("  总任务数: %d" % tasks['total_tasks'])
        print("  任务成功率: %s" % tasks['success_rate'])
        print("  平均任务时长: %s" % tasks['avg_task_duration'])
        print()
        
        # 建议
        print("【系统建议】")
        for i, rec in enumerate(report['recommendations'], 1):
            print("  %d. %s" % (i, rec))
        
        print("=" * 65)

# 测试监控面板
if __name__ == "__main__":
    import time
    monitor = SystemMonitor()
    
    # 等待监控线程启动
    time.sleep(1)
    
    # 模拟一些数据
    monitor.update_learning_metrics(success=True, score=85)
    monitor.update_learning_metrics(success=True, score=78)
    monitor.update_learning_metrics(success=False)
    monitor.update_skill_metrics(total_skills=52, active_skills=10, executed_count=100, error_count=5)
    monitor.update_topic_metrics(total_topics=20, categories=["技巧学习", "趋势分析", "人物塑造", "剧情设计", "世界观"], 
                                last_update=datetime.now().isoformat(), avg_priority=7)
    monitor.update_task_metrics(pending_tasks=3, active_tasks=2, completed_tasks=15, failed_tasks=1, avg_duration=1500)
    
    # 打印监控面板
    monitor.print_dashboard()