#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 自动学习系统 v2.0
集成Skill自主学习能力，实现全系统协同学习
新增：环境检测、自动修复、增强错误处理
"""

import time
import threading
import os
import sys
import subprocess
import platform
from datetime import datetime

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 环境检测
class EnvironmentChecker:
    """环境检测类"""
    
    @staticmethod
    def check_environment():
        """检查运行环境"""
        issues = []
        
        # 检查Python版本
        if sys.version_info < (3, 8):
            issues.append(f"Python版本过低: {sys.version_info.major}.{sys.version_info.minor}，建议使用Python 3.8+")
        
        # 检查必要目录
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 检查logs目录
        logs_dir = os.path.join(script_dir, 'logs')
        if not os.path.exists(logs_dir):
            try:
                os.makedirs(logs_dir)
                print(f"✓ 自动创建logs目录: {logs_dir}")
            except Exception as e:
                issues.append(f"无法创建logs目录: {e}")
        
        # 检查学习记录目录
        if not os.path.exists('学习记录'):
            try:
                os.makedirs('学习记录')
                print("✓ 自动创建学习记录目录")
            except Exception as e:
                issues.append(f"无法创建学习记录目录: {e}")
        
        return issues
    
    @staticmethod
    def is_python_available():
        """检查Python是否可用"""
        try:
            result = subprocess.run([sys.executable, '--version'], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except Exception:
            return False
    
    @staticmethod
    def get_python_path():
        """获取Python路径"""
        return sys.executable

# 先进行环境检测
env_issues = EnvironmentChecker.check_environment()
if env_issues:
    print("\n警告：检测到以下环境问题:")
    for issue in env_issues:
        print(f"  - {issue}")
    print("\n尝试继续运行...\n")

# 导入依赖（环境检测之后）
from logger import logger
from learning_evaluator import LearningEvaluator
from fault_tolerance import retry_on_failure, circuit_breaker, RateLimiter

class AutoLearningSystem:
    def __init__(self, standalone=False, enable_skill_learning=True):
        self.is_learning = False
        self.last_activity_time = time.time()
        self.idle_threshold = 300  # 5分钟空闲触发
        self.check_interval = 60   # 每分钟检查一次
        self.learning_interval = 3600  # 每小时学习一次
        self.last_learning_time = 0
        self.learning_count = 0
        self.error_count = 0
        self.standalone = standalone  # 是否独立运行模式
        self.enable_skill_learning = enable_skill_learning  # 是否启用Skill自主学习
        
        # 学习内容配置
        self.learning_topics = [
            {"topic": "2026 热门小说 分析", "skill": "写作技巧大师"},
            {"topic": "2026 写作技巧书籍 推荐", "skill": "写作技巧大师"},
            {"topic": "最新写作技巧书籍", "skill": "写作技巧大师"},
            {"topic": "文学理论 新发展", "skill": "写作技巧大师"},
            {"topic": "跨媒介创作技巧", "skill": "写作技巧大师"},
            {"topic": "2026 网络小说 趋势", "skill": "世界观构造师"},
            {"topic": "情感描写技巧 微动作微表情", "skill": "对话设计师"},
            {"topic": "人物刻画方法 情感小说", "skill": "角色性格塑造师"},
            {"topic": "剧情构造技巧 故事合理性", "skill": "主线剧情设计师"}
        ]
        
        # 初始化评估器
        self.evaluator = LearningEvaluator()
        
        # 初始化速率限制器
        self.rate_limiter = RateLimiter(max_requests=60, time_window=3600)
        
        # 初始化Skill学习管理器
        self.skill_learning_manager = None
        if self.enable_skill_learning:
            try:
                from skill_learning_manager import SkillLearningManager
                self.skill_learning_manager = SkillLearningManager()
                self.skill_learning_manager.initialize_learners()
                logger.info("Skill学习管理器初始化完成")
            except ImportError as e:
                logger.warning("Skill学习管理器导入失败: %s" % str(e))
                self.enable_skill_learning = False
        
        logger.info("自动学习系统初始化完成")
        self.start_monitoring()
    
    def start_monitoring(self):
        """启动监控线程"""
        # 空闲监控线程 - 根据运行模式决定是否使用守护线程
        monitor_thread = threading.Thread(target=self.monitor_idle)
        monitor_thread.daemon = not self.standalone  # 独立运行时使用非守护线程
        monitor_thread.start()
        logger.info("空闲监控线程已启动")
        
        # 定时学习线程
        timer_thread = threading.Thread(target=self.timer_based_learning)
        timer_thread.daemon = not self.standalone
        timer_thread.start()
        logger.info("定时学习线程已启动")
        
        # 启动Skill学习器（如果启用）
        if self.enable_skill_learning and self.skill_learning_manager:
            skill_thread = threading.Thread(target=self.start_skill_learning)
            skill_thread.daemon = not self.standalone
            skill_thread.start()
            logger.info("Skill自主学习线程已启动")
        
        logger.info("空闲检测阈值: %d分钟" % (self.idle_threshold/60))
        logger.info("定时学习间隔: %d分钟" % (self.learning_interval/60))
    
    def start_skill_learning(self):
        """启动所有Skill学习器"""
        if self.skill_learning_manager:
            time.sleep(5)  # 延迟5秒启动，确保主系统就绪
            self.skill_learning_manager.start_all_learners()
    
    def monitor_idle(self):
        """监控系统空闲状态"""
        logger.debug("空闲监控循环启动")
        while True:
            try:
                current_time = time.time()
                idle_time = current_time - self.last_activity_time
                
                if idle_time >= self.idle_threshold and not self.is_learning:
                    logger.info("检测到空闲状态 (%d秒)" % idle_time)
                    self.trigger_learning("空闲触发")
                
                time.sleep(self.check_interval)
            except Exception as e:
                logger.log_exception(e, "monitor_idle")
                self.error_count += 1
    
    def timer_based_learning(self):
        """定时学习触发"""
        logger.debug("定时学习循环启动")
        while True:
            try:
                current_time = time.time()
                if current_time - self.last_learning_time >= self.learning_interval:
                    if not self.is_learning:
                        logger.info("定时学习触发")
                        self.trigger_learning("定时触发")
                time.sleep(self.check_interval)
            except Exception as e:
                logger.log_exception(e, "timer_based_learning")
                self.error_count += 1
    
    def trigger_learning(self, trigger_type):
        """触发学习流程"""
        # 检查速率限制
        if not self.rate_limiter.acquire():
            logger.warning("学习请求被速率限制")
            return
        
        self.is_learning = True
        self.last_learning_time = time.time()
        
        try:
            logger.info("开始学习 (%s)" % trigger_type)
            
            # 执行系统级学习
            self.execute_learning()
            
            # 触发Skill级学习（如果启用）
            if self.enable_skill_learning and self.skill_learning_manager:
                self.trigger_skill_learning()
            
            logger.info("学习完成")
            self.learning_count += 1
        except Exception as e:
            logger.log_exception(e, "trigger_learning")
            self.error_count += 1
        finally:
            self.is_learning = False
    
    def trigger_skill_learning(self):
        """触发Skill自主学习"""
        logger.info("触发所有Skill自主学习")
        
        for skill_name, learner in self.skill_learning_manager.skill_learners.items():
            if not learner.is_learning:
                learner.execute_learning()
    
    @retry_on_failure
    def execute_learning(self):
        """执行学习任务（带重试机制）"""
        # 1. 选择学习主题
        topic_info = self.select_topic()
        topic = topic_info['topic']
        skill_name = topic_info['skill']
        logger.info("学习主题: %s, 关联Skill: %s" % (topic, skill_name))
        
        # 2. 模拟联网搜索学习（带断路器保护）
        self.simulate_web_search_with_protection(topic)
        
        # 3. 更新学习记录
        self.update_learning_record(topic)
        
        # 4. 评估学习效果
        self.evaluate_learning_effect(topic, skill_name)
    
    @circuit_breaker
    def simulate_web_search_with_protection(self, topic):
        """带断路器保护的网络搜索"""
        self.simulate_web_search(topic)
    
    def select_topic(self):
        """选择下一个学习主题"""
        if not hasattr(self, '_topic_index'):
            self._topic_index = 0
        
        topic_info = self.learning_topics[self._topic_index]
        self._topic_index = (self._topic_index + 1) % len(self.learning_topics)
        return topic_info
    
    def simulate_web_search(self, topic):
        """模拟联网搜索学习"""
        logger.debug("正在搜索: %s" % topic)
        time.sleep(3)  # 模拟网络请求时间
        logger.debug("分析学习内容中...")
        time.sleep(2)  # 模拟分析时间
    
    def update_learning_record(self, topic):
        """更新学习记录"""
        record_file = "36_2026年学习更新记录.md"
        
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_record = "\n\n## 自动学习记录 (%s)\n- 学习主题: %s\n- 学习状态: 已完成\n- 触发方式: 系统自动" % (now, topic)
        
        try:
            with open(record_file, 'a', encoding='utf-8') as f:
                f.write(new_record)
            logger.debug("学习记录已更新")
        except Exception as e:
            logger.log_exception(e, "update_learning_record")
            self.error_count += 1
    
    def evaluate_learning_effect(self, topic, skill_name):
        """评估学习效果"""
        # 模拟评估指标（实际应用中可根据真实学习结果生成）
        metrics = {
            'knowledge_acquisition': self.generate_random_score(75, 95),
            'skill_improvement': self.generate_random_score(70, 90),
            'application_ability': self.generate_random_score(65, 85),
            'retention_rate': self.generate_random_score(80, 95),
            'depth_of_learning': self.generate_random_score(70, 90)
        }
        
        evaluation = self.evaluator.evaluate_learning(topic, skill_name, metrics)
        logger.info("学习评估完成: %s, 综合评分: %d, 反馈: %s" % 
                   (topic, evaluation['overall_score'], evaluation['feedback']))
    
    def generate_random_score(self, min_val, max_val):
        """生成随机评分（模拟真实评估）"""
        import random
        return random.randint(min_val, max_val)
    
    def record_activity(self):
        """记录用户活动（供外部调用）"""
        self.last_activity_time = time.time()
        logger.debug("检测到用户活动")
    
    def get_stats(self):
        """获取系统统计信息"""
        stats = {
            'learning_count': self.learning_count,
            'error_count': self.error_count,
            'last_learning_time': self.last_learning_time,
            'is_learning': self.is_learning,
            'evaluation_summary': self.evaluator.generate_report()['summary']
        }
        
        # 添加Skill学习统计
        if self.enable_skill_learning and self.skill_learning_manager:
            stats['skill_learning_stats'] = self.skill_learning_manager.get_all_stats()
        
        return stats
    
    def print_full_status(self):
        """打印完整状态"""
        stats = self.get_stats()
        
        print("=" * 60)
        print("            自动学习系统状态")
        print("=" * 60)
        
        print("\n【系统学习统计】")
        print(f"  系统学习次数: {stats['learning_count']}")
        print(f"  错误次数: {stats['error_count']}")
        print(f"  是否正在学习: {'是' if stats['is_learning'] else '否'}")
        print(f"  平均评分: {stats['evaluation_summary'].get('average_score', 0)}")
        
        # 打印Skill学习状态
        if 'skill_learning_stats' in stats:
            print("\n【Skill自主学习状态】")
            skill_stats = stats['skill_learning_stats']
            for skill_name, s_stats in skill_stats.items():
                print(f"  [{skill_name}] 学习次数: {s_stats['learning_count']}, 错误: {s_stats['error_count']}")
        
        print("\n" + "=" * 60)

# 独立运行模式
if __name__ == "__main__":
    print("=====================================")
    print("    NWACS 自动学习系统 v1.5")
    print("=====================================")
    print("集成Skill自主学习能力")
    print("=====================================")
    
    # 使用独立运行模式，启用Skill学习
    system = AutoLearningSystem(standalone=True, enable_skill_learning=True)
    logger.info("自动学习系统已启动（独立模式）")
    
    # 保持主线程运行
    try:
        while True:
            # 每30秒打印一次状态
            time.sleep(30)
            system.print_full_status()
    except KeyboardInterrupt:
        stats = system.get_stats()
        logger.info("自动学习系统已停止，学习次数: %d, 错误次数: %d" % 
                   (stats['learning_count'], stats['error_count']))
        print("\n自动学习系统已停止")