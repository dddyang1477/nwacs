#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS Skill自主学习管理器
为所有Skill添加独立的自主学习能力
"""

import time
import threading
import json
import os
from datetime import datetime
from logger import logger

class SkillLearner:
    """单个Skill的学习器"""
    
    def __init__(self, skill_name, skill_type, learning_topics):
        self.skill_name = skill_name
        self.skill_type = skill_type
        self.learning_topics = learning_topics
        self.is_learning = False
        self.learning_count = 0
        self.error_count = 0
        self.last_learning_time = 0
        self.learning_interval = 1800  # 每30分钟学习一次
        self._topic_index = 0
        
        logger.info("初始化Skill学习器: %s" % skill_name)
    
    def start_learning_loop(self):
        """启动学习循环"""
        thread = threading.Thread(target=self.learning_loop)
        thread.daemon = False
        thread.start()
    
    def learning_loop(self):
        """学习循环"""
        logger.debug("%s 学习循环启动" % self.skill_name)
        
        while True:
            try:
                current_time = time.time()
                
                # 检查是否需要学习
                if current_time - self.last_learning_time >= self.learning_interval:
                    if not self.is_learning:
                        self.execute_learning()
                
                time.sleep(60)  # 每分钟检查一次
            except Exception as e:
                logger.log_exception(e, "%s learning_loop" % self.skill_name)
                self.error_count += 1
    
    def execute_learning(self):
        """执行学习"""
        self.is_learning = True
        self.last_learning_time = time.time()
        
        try:
            # 选择学习主题
            topic = self.select_topic()
            logger.info("%s 正在学习: %s" % (self.skill_name, topic))
            
            # 模拟学习过程
            self.simulate_learning(topic)
            
            # 更新学习记录
            self.update_learning_record(topic)
            
            self.learning_count += 1
            logger.info("%s 学习完成" % self.skill_name)
            
        except Exception as e:
            logger.log_exception(e, "%s execute_learning" % self.skill_name)
            self.error_count += 1
        finally:
            self.is_learning = False
    
    def select_topic(self):
        """选择下一个学习主题"""
        if not self.learning_topics:
            return "通用写作技巧"
        
        topic = self.learning_topics[self._topic_index]
        self._topic_index = (self._topic_index + 1) % len(self.learning_topics)
        return topic
    
    def simulate_learning(self, topic):
        """模拟学习过程"""
        logger.debug("%s 正在深入学习: %s" % (self.skill_name, topic))
        time.sleep(2)  # 模拟学习时间
        
        # 模拟学习成果
        learning_outcome = {
            'topic': topic,
            'skill_name': self.skill_name,
            'learned_points': self.generate_learning_points(topic),
            'timestamp': datetime.now().isoformat()
        }
        
        return learning_outcome
    
    def generate_learning_points(self, topic):
        """生成学习要点（模拟）"""
        points = []
        
        if '情感' in topic:
            points = ["微表情描写技巧", "情感递进表达", "心理活动刻画"]
        elif '人物' in topic:
            points = ["角色弧光设计", "性格一致性", "动机合理性"]
        elif '剧情' in topic:
            points = ["节奏控制", "冲突设计", "伏笔埋设"]
        elif '世界观' in topic:
            points = ["规则一致性", "细节丰富度", "独特性"]
        elif '战斗' in topic:
            points = ["招式设计", "节奏控制", "场面描写"]
        else:
            points = ["写作技巧提升", "语言表达优化", "风格统一"]
        
        return points
    
    def update_learning_record(self, topic):
        """更新学习记录"""
        record = {
            'skill_name': self.skill_name,
            'skill_type': self.skill_type,
            'topic': topic,
            'timestamp': datetime.now().isoformat(),
            'learning_count': self.learning_count
        }
        
        # 保存到学习记录文件
        self._save_to_record(record)
    
    def _save_to_record(self, record):
        """保存记录到文件"""
        record_file = "skill_learning_records.json"
        
        try:
            if os.path.exists(record_file):
                # 检查文件是否为空
                file_size = os.path.getsize(record_file)
                if file_size == 0:
                    records = []
                else:
                    with open(record_file, 'r', encoding='utf-8') as f:
                        try:
                            records = json.load(f)
                        except json.JSONDecodeError:
                            # 文件内容不是有效JSON，重新初始化
                            records = []
            else:
                records = []
            
            records.append(record)
            
            with open(record_file, 'w', encoding='utf-8') as f:
                json.dump(records, f, ensure_ascii=False, indent=2)
            
        except Exception as e:
            logger.log_exception(e, "%s _save_to_record" % self.skill_name)
    
    def get_stats(self):
        """获取统计信息"""
        return {
            'skill_name': self.skill_name,
            'skill_type': self.skill_type,
            'learning_count': self.learning_count,
            'error_count': self.error_count,
            'is_learning': self.is_learning,
            'last_learning_time': self.last_learning_time,
            'learning_topics': self.learning_topics
        }

class SkillLearningManager:
    """Skill学习管理器"""
    
    def __init__(self):
        self.skill_learners = {}
        self.running = False
        
        # 定义各Skill的学习主题
        self.skill_topics = {
            '世界观构造师': [
                '玄幻世界构建技巧',
                '都市异能设定方法',
                '科幻世界规则设计',
                '历史架空背景构建',
                '世界规则一致性维护'
            ],
            '剧情构造师': [
                '三幕式结构设计',
                '英雄之旅模板应用',
                '悬疑反转设计技巧',
                '伏笔埋设与回收',
                '剧情节奏控制'
            ],
            '角色塑造师': [
                '角色性格刻画方法',
                '人物动机设定',
                '角色成长弧光设计',
                '人物关系网络构建',
                '反派角色塑造技巧'
            ],
            '战斗设计师': [
                '战斗场景描写技巧',
                '招式命名艺术',
                '战斗节奏控制',
                '不同境界战斗差异',
                '特殊能力对决设计'
            ],
            '场景构造师': [
                '环境氛围营造',
                '感官细节描写',
                '空间布局设计',
                '场景转换技巧',
                '地域特色体现'
            ],
            '对话设计师': [
                '对话个性塑造',
                '潜台词设计',
                '对话节奏控制',
                '情感对话描写',
                '冲突对话设计'
            ],
            '写作技巧大师': [
                '风格定位与统一',
                '修辞手法运用',
                '叙事视角选择',
                '节奏控制技巧',
                '去AI化写作方法'
            ],
            '去AI痕迹监督官': [
                'AI痕迹识别技巧',
                '自然语言优化',
                '人类风格模拟',
                '文本质量评估',
                '写作风格多样性'
            ],
            '质量审计师': [
                '小说质量评估标准',
                '结构完整性检查',
                '人物一致性检查',
                '逻辑合理性验证',
                '读者体验优化'
            ],
            '学习大师': [
                '网络小说趋势分析',
                '经典文学研究',
                '写作技巧创新',
                '跨领域知识融合',
                '学习方法优化'
            ],
            '规则掌控者': [
                '自然规则设定',
                '社会规则构建',
                '特殊规则设计',
                '规则一致性维护',
                '规则冲突解决'
            ],
            '词汇大师': [
                '词汇收集与整理',
                '描写素材积累',
                '语言风格优化',
                '专业术语应用',
                '修辞丰富度提升'
            ]
        }
    
    def initialize_learners(self):
        """初始化所有Skill学习器"""
        logger.info("初始化所有Skill学习器")
        
        for skill_name, topics in self.skill_topics.items():
            learner = SkillLearner(skill_name, 'secondary', topics)
            self.skill_learners[skill_name] = learner
        
        logger.info("已初始化 %d 个Skill学习器" % len(self.skill_learners))
    
    def start_all_learners(self):
        """启动所有学习器"""
        self.running = True
        
        for skill_name, learner in self.skill_learners.items():
            learner.start_learning_loop()
            logger.info("启动Skill学习器: %s" % skill_name)
        
        logger.info("所有Skill学习器已启动")
    
    def stop_all_learners(self):
        """停止所有学习器"""
        self.running = False
        logger.info("所有Skill学习器已停止")
    
    def get_all_stats(self):
        """获取所有学习器统计"""
        stats = {}
        for skill_name, learner in self.skill_learners.items():
            stats[skill_name] = learner.get_stats()
        return stats
    
    def print_status(self):
        """打印状态"""
        print("=" * 60)
        print("            Skill自主学习状态")
        print("=" * 60)
        
        for skill_name, stats in self.get_all_stats().items():
            print(f"\n【{skill_name}】")
            print(f"  学习次数: {stats['learning_count']}")
            print(f"  错误次数: {stats['error_count']}")
            print(f"  学习中: {'是' if stats['is_learning'] else '否'}")
            print(f"  当前学习主题: {stats['learning_topics'][stats['_topic_index']] if hasattr(stats, '_topic_index') else '未知'}")
        
        print("\n" + "=" * 60)

# 独立运行测试
if __name__ == "__main__":
    print("=====================================")
    print("    NWACS Skill自主学习管理器")
    print("=====================================")
    
    # 创建管理器
    manager = SkillLearningManager()
    manager.initialize_learners()
    
    # 启动所有学习器
    print("\n启动所有Skill学习器...")
    manager.start_all_learners()
    
    # 显示状态
    print("\n当前状态:")
    manager.print_status()
    
    # 保持运行
    try:
        while True:
            time.sleep(60)
            # 每分钟更新一次状态
            print("\n更新状态:")
            manager.print_status()
    except KeyboardInterrupt:
        manager.stop_all_learners()
        print("\nSkill学习管理器已停止")