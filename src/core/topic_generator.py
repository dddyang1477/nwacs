#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 智能学习主题生成模块
功能：动态生成、热点分析、优先级排序、自动更新
"""

import json
import os
import random
from datetime import datetime
from logger import logger

class SmartTopicGenerator:
    """智能学习主题生成器"""
    
    def __init__(self):
        self.base_topics = {
            '短篇小说爽文大师': [
                {'topic': '2026 年短篇爽文趋势', 'priority': 10, 'category': '趋势'},
                {'topic': '爆款开篇的 10 种写法', 'priority': 9, 'category': '技巧'},
                {'topic': '反转剧情设计技巧', 'priority': 9, 'category': '技巧'},
                {'topic': '读者心理把握', 'priority': 8, 'category': '理论'},
                {'topic': '狗血剧情套路解析', 'priority': 8, 'category': '套路'},
                {'topic': '甜宠文核心要素', 'priority': 7, 'category': '题材'},
                {'topic': '虐恋文情感节奏', 'priority': 7, 'category': '题材'},
                {'topic': '爽文节奏把控', 'priority': 9, 'category': '技巧'}
            ],
            '世界观构造师': [
                {'topic': '玄幻世界体系构建', 'priority': 10, 'category': '体系'},
                {'topic': '修炼等级设定大全', 'priority': 9, 'category': '设定'},
                {'topic': '地理环境设计技巧', 'priority': 8, 'category': '技巧'},
                {'topic': '社会结构规划方法', 'priority': 8, 'category': '理论'},
                {'topic': '力量体系平衡设计', 'priority': 9, 'category': '体系'},
                {'topic': '世界规则制定原则', 'priority': 8, 'category': '规则'}
            ],
            '剧情构造师': [
                {'topic': '三幕式结构优化', 'priority': 10, 'category': '结构'},
                {'topic': '伏笔埋设技巧', 'priority': 9, 'category': '技巧'},
                {'topic': '高潮设计方法', 'priority': 9, 'category': '技巧'},
                {'topic': '多线叙事技巧', 'priority': 8, 'category': '技巧'},
                {'topic': '剧情节奏把控', 'priority': 9, 'category': '节奏'},
                {'topic': '悬念设置艺术', 'priority': 8, 'category': '技巧'}
            ],
            '角色塑造师': [
                {'topic': '立体人物塑造方法', 'priority': 10, 'category': '技巧'},
                {'topic': '角色成长弧线设计', 'priority': 9, 'category': '设计'},
                {'topic': '人物关系网络构建', 'priority': 8, 'category': '关系'},
                {'topic': '角色动机与冲突', 'priority': 9, 'category': '理论'},
                {'topic': '反派角色塑造技巧', 'priority': 8, 'category': '技巧'},
                {'topic': '主角魅力塑造', 'priority': 8, 'category': '技巧'}
            ],
            '写作技巧大师': [
                {'topic': '文笔优化技巧', 'priority': 9, 'category': '技巧'},
                {'topic': '节奏把控方法', 'priority': 10, 'category': '节奏'},
                {'topic': '对话描写技巧', 'priority': 8, 'category': '技巧'},
                {'topic': '环境描写手法', 'priority': 7, 'category': '技巧'},
                {'topic': '心理描写深度', 'priority': 8, 'category': '技巧'},
                {'topic': '动作描写生动性', 'priority': 7, 'category': '技巧'}
            ],
            '词汇大师': [
                {'topic': '山海经神兽词汇', 'priority': 9, 'category': '素材'},
                {'topic': '古风描写词汇', 'priority': 8, 'category': '素材'},
                {'topic': '现代流行词汇', 'priority': 7, 'category': '素材'},
                {'topic': '情感描写词汇', 'priority': 8, 'category': '素材'},
                {'topic': '场景描写词汇', 'priority': 7, 'category': '素材'}
            ]
        }
        
        # 热点话题（定期更新）
        self.hot_topics = [
            {'topic': '短剧改编热潮分析', 'priority': 10, 'trending': True},
            {'topic': '新媒体文特点', 'priority': 9, 'trending': True},
            {'topic': 'Z 世代读者偏好', 'priority': 8, 'trending': True},
            {'topic': 'AI 辅助写作技巧', 'priority': 7, 'trending': True}
        ]
        
        # 学习历史
        self.learning_history = []
        self.history_file = "topic_learning_history.json"
        
        self._load_history()
    
    def _load_history(self):
        """加载学习历史"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.learning_history = json.load(f)
            except Exception:
                self.learning_history = []
    
    def _save_history(self):
        """保存学习历史"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.learning_history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.log_exception(e, "保存学习历史")
    
    def generate_topics(self, skill_name, count=5):
        """为 Skill 生成学习主题列表"""
        if skill_name not in self.base_topics:
            logger.warning("未找到 Skill '%s' 的基础主题" % skill_name)
            return self._generate_generic_topics(count)
        
        # 获取基础主题
        base = self.base_topics[skill_name]
        
        # 计算每个主题的优先级分数
        scored_topics = []
        for topic in base:
            score = self._calculate_topic_score(skill_name, topic)
            scored_topics.append({
                **topic,
                'score': score
            })
        
        # 添加热点话题
        for hot in self.hot_topics:
            hot['score'] = hot['priority'] * 1.2  # 热点话题加分
            scored_topics.append(hot)
        
        # 按分数排序
        scored_topics.sort(key=lambda x: x['score'], reverse=True)
        
        # 返回指定数量的主题
        result = scored_topics[:count]
        
        logger.debug("为 %s 生成 %d 个学习主题" % (skill_name, len(result)))
        return result
    
    def _calculate_topic_score(self, skill_name, topic):
        """计算主题优先级分数"""
        base_score = topic.get('priority', 5)
        
        # 时间衰减：最近学过的主题分数降低
        for record in self.learning_history[-20:]:
            if record.get('topic') == topic['topic']:
                learn_time = datetime.fromisoformat(record['timestamp'])
                days_diff = (datetime.now() - learn_time).days
                
                if days_diff < 3:
                    base_score *= 0.3  # 3 天内学过的主题大幅降低优先级
                elif days_diff < 7:
                    base_score *= 0.6  # 7 天内适度降低
        
        # 热点话题加分
        if topic.get('trending'):
            base_score *= 1.5
        
        # 类别偏好：技巧类优先
        category_bonus = {
            '技巧': 1.2,
            '趋势': 1.3,
            '体系': 1.1,
            '设定': 1.0
        }
        
        category = topic.get('category', '')
        if category in category_bonus:
            base_score *= category_bonus[category]
        
        return base_score
    
    def select_next_topic(self, skill_name):
        """选择下一个学习主题"""
        topics = self.generate_topics(skill_name, count=10)
        
        if not topics:
            return "通用写作技巧"
        
        # 使用轮盘赌算法选择（优先级高的概率大）
        total_score = sum(t['score'] for t in topics)
        if total_score == 0:
            return random.choice(topics)['topic']
        
        import random
        rand = random.uniform(0, total_score)
        current = 0
        
        for topic in topics:
            current += topic['score']
            if rand <= current:
                # 记录选择
                self._record_learning(skill_name, topic['topic'])
                return topic['topic']
        
        return topics[0]['topic']
    
    def _record_learning(self, skill_name, topic):
        """记录学习"""
        self.learning_history.append({
            'skill_name': skill_name,
            'topic': topic,
            'timestamp': datetime.now().isoformat()
        })
        
        # 保持历史记录数量
        if len(self.learning_history) > 500:
            self.learning_history = self.learning_history[-500:]
        
        self._save_history()
    
    def _generate_generic_topics(self, count):
        """生成通用主题"""
        generic = [
            {'topic': '写作基础技巧', 'priority': 5},
            {'topic': '故事结构分析', 'priority': 5},
            {'topic': '读者心理研究', 'priority': 5},
            {'topic': '热门题材趋势', 'priority': 6},
            {'topic': '创作灵感收集', 'priority': 4}
        ]
        
        return random.sample(generic, min(count, len(generic)))
    
    def add_custom_topic(self, skill_name, topic, priority=5, category='自定义'):
        """添加自定义主题"""
        if skill_name not in self.base_topics:
            self.base_topics[skill_name] = []
        
        self.base_topics[skill_name].append({
            'topic': topic,
            'priority': priority,
            'category': category
        })
        
        logger.info("已添加自定义主题：%s -> %s" % (skill_name, topic))
    
    def remove_learned_topic(self, skill_name, topic):
        """标记主题为已学习"""
        self._record_learning(skill_name, topic)
        logger.debug("主题已标记为已学习：%s" % topic)
    
    def get_learning_statistics(self):
        """获取学习统计"""
        if not self.learning_history:
            return {'message': '暂无学习记录'}
        
        # 按 Skill 统计
        skill_stats = {}
        for record in self.learning_history:
            skill = record['skill_name']
            if skill not in skill_stats:
                skill_stats[skill] = {
                    'count': 0,
                    'topics': set(),
                    'categories': set()
                }
            
            skill_stats[skill]['count'] += 1
            skill_stats[skill]['topics'].add(record['topic'])
        
        # 转换为可序列化格式
        result = {
            'total_learning_count': len(self.learning_history),
            'skills': {}
        }
        
        for skill, stats in skill_stats.items():
            result['skills'][skill] = {
                'learning_count': stats['count'],
                'unique_topics': len(stats['topics'])
            }
        
        return result
    
    def suggest_learning_plan(self, skill_name, days=7):
        """为 Skill 建议学习计划"""
        topics = self.generate_topics(skill_name, count=days)
        
        plan = {
            'skill_name': skill_name,
            'duration_days': days,
            'daily_topics': []
        }
        
        for i, topic in enumerate(topics[:days]):
            plan['daily_topics'].append({
                'day': i + 1,
                'topic': topic['topic'],
                'priority': topic['priority'],
                'category': topic.get('category', '未知')
            })
        
        return plan


# 全局生成器实例
topic_generator = SmartTopicGenerator()


def get_topic_generator():
    """获取主题生成器实例"""
    return topic_generator
