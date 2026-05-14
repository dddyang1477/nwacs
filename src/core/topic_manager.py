#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 学习主题动态扩展系统 v2.0
支持动态添加、删除和优先级调整学习主题
新增：智能主题推荐、学习效果分析、个性化建议
"""

import json
import os
import statistics
from datetime import datetime, timedelta
from logger import logger

class DynamicTopicManager:
    def __init__(self):
        self.topics = []
        self.topic_config_file = 'learning_topics.json'
        self.skill_proficiency = {}  # 技能熟练度
        self.load_topics()
        self.load_skill_proficiency()
    
    def load_topics(self):
        """加载学习主题配置"""
        if os.path.exists(self.topic_config_file):
            try:
                with open(self.topic_config_file, 'r', encoding='utf-8') as f:
                    self.topics = json.load(f).get('topics', [])
                logger.info("学习主题配置加载成功，共 %d 个主题" % len(self.topics))
            except Exception as e:
                logger.log_exception(e, "load_topics")
                self.load_default_topics()
        else:
            self.load_default_topics()
    
    def load_skill_proficiency(self):
        """加载技能熟练度数据"""
        proficiency_file = 'skill_proficiency.json'
        if os.path.exists(proficiency_file):
            try:
                with open(proficiency_file, 'r', encoding='utf-8') as f:
                    self.skill_proficiency = json.load(f)
                logger.info("技能熟练度数据加载成功")
            except Exception as e:
                logger.log_exception(e, "load_skill_proficiency")
                self.init_default_proficiency()
        else:
            self.init_default_proficiency()
    
    def init_default_proficiency(self):
        """初始化默认技能熟练度"""
        self.skill_proficiency = {
            '写作技巧大师': 70,
            '世界观构造师': 65,
            '对话设计师': 60,
            '角色性格塑造师': 65,
            '主线剧情设计师': 68,
            '环境氛围营造师': 55,
            '战斗招式设计师': 50,
            '风格指导师': 62,
            '修辞策略师': 58,
            '叙事技巧师': 60
        }
        self.save_skill_proficiency()
    
    def save_skill_proficiency(self):
        """保存技能熟练度"""
        try:
            with open('skill_proficiency.json', 'w', encoding='utf-8') as f:
                json.dump(self.skill_proficiency, f, ensure_ascii=False, indent=2)
            logger.debug("技能熟练度数据保存成功")
        except Exception as e:
            logger.log_exception(e, "save_skill_proficiency")
    
    def update_skill_proficiency(self, skill_name, score):
        """更新技能熟练度"""
        if skill_name in self.skill_proficiency:
            # 平滑更新，取当前值和新评分的加权平均
            current = self.skill_proficiency[skill_name]
            self.skill_proficiency[skill_name] = round((current * 3 + score) / 4)
        else:
            self.skill_proficiency[skill_name] = score
        self.save_skill_proficiency()
    
    def load_default_topics(self):
        """加载默认学习主题"""
        self.topics = [
            {"id": 1, "topic": "2026 热门小说 分析", "skill": "写作技巧大师", "priority": 10, "category": "趋势分析", "difficulty": "medium"},
            {"id": 2, "topic": "2026 写作技巧书籍 推荐", "skill": "写作技巧大师", "priority": 10, "category": "技巧学习", "difficulty": "easy"},
            {"id": 3, "topic": "最新写作技巧书籍", "skill": "写作技巧大师", "priority": 9, "category": "技巧学习", "difficulty": "medium"},
            {"id": 4, "topic": "文学理论 新发展", "skill": "写作技巧大师", "priority": 8, "category": "理论学习", "difficulty": "hard"},
            {"id": 5, "topic": "跨媒介创作技巧", "skill": "写作技巧大师", "priority": 7, "category": "技巧学习", "difficulty": "medium"},
            {"id": 6, "topic": "2026 网络小说 趋势", "skill": "世界观构造师", "priority": 10, "category": "趋势分析", "difficulty": "easy"},
            {"id": 7, "topic": "情感描写技巧 微动作微表情", "skill": "对话设计师", "priority": 10, "category": "技巧学习", "difficulty": "medium"},
            {"id": 8, "topic": "人物刻画方法 情感小说", "skill": "角色性格塑造师", "priority": 9, "category": "人物塑造", "difficulty": "medium"},
            {"id": 9, "topic": "剧情构造技巧 故事合理性", "skill": "主线剧情设计师", "priority": 9, "category": "剧情设计", "difficulty": "medium"},
            {"id": 10, "topic": "悬疑推理小说创作技巧", "skill": "主线剧情设计师", "priority": 7, "category": "剧情设计", "difficulty": "hard"},
            {"id": 11, "topic": "科幻小说世界构建", "skill": "世界观构造师", "priority": 6, "category": "世界观", "difficulty": "hard"},
            {"id": 12, "topic": "历史小说写作技巧", "skill": "世界观构造师", "priority": 6, "category": "世界观", "difficulty": "medium"},
            {"id": 13, "topic": "女频小说创作技巧", "skill": "角色性格塑造师", "priority": 8, "category": "人物塑造", "difficulty": "medium"},
            {"id": 14, "topic": "节奏控制与章节设计", "skill": "主线剧情设计师", "priority": 8, "category": "剧情设计", "difficulty": "medium"},
            {"id": 15, "topic": "场景描写与氛围营造", "skill": "环境氛围营造师", "priority": 7, "category": "场景设计", "difficulty": "medium"},
            {"id": 16, "topic": "战斗场景设计技巧", "skill": "战斗招式设计师", "priority": 7, "category": "战斗设计", "difficulty": "hard"},
            {"id": 17, "topic": "风格多样性训练", "skill": "风格指导师", "priority": 6, "category": "风格训练", "difficulty": "medium"},
            {"id": 18, "topic": "修辞技巧进阶", "skill": "修辞策略师", "priority": 6, "category": "技巧学习", "difficulty": "hard"},
            {"id": 19, "topic": "非线性叙事技巧", "skill": "叙事技巧师", "priority": 5, "category": "剧情设计", "difficulty": "hard"},
            {"id": 20, "topic": "读者心理分析", "skill": "写作技巧大师", "priority": 7, "category": "理论学习", "difficulty": "medium"}
        ]
        self.save_topics()
        logger.info("已加载默认学习主题")
    
    def save_topics(self):
        """保存主题配置"""
        try:
            data = {
                'topics': self.topics,
                'last_update': datetime.now().isoformat()
            }
            with open(self.topic_config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.debug("学习主题配置保存成功")
        except Exception as e:
            logger.log_exception(e, "save_topics")
    
    def add_topic(self, topic, skill, priority=5, category="其他"):
        """添加新的学习主题"""
        new_id = max(t['id'] for t in self.topics) + 1 if self.topics else 1
        
        new_topic = {
            'id': new_id,
            'topic': topic,
            'skill': skill,
            'priority': priority,
            'category': category,
            'added_at': datetime.now().isoformat(),
            'learning_count': 0,
            'last_learning_at': None,
            'average_score': 0
        }
        
        self.topics.append(new_topic)
        self.save_topics()
        logger.info("添加学习主题: %s" % topic)
        return new_topic
    
    def remove_topic(self, topic_id):
        """删除学习主题"""
        for i, topic in enumerate(self.topics):
            if topic['id'] == topic_id:
                removed = self.topics.pop(i)
                self.save_topics()
                logger.info("删除学习主题: %s" % removed['topic'])
                return True
        logger.warning("未找到主题ID: %d" % topic_id)
        return False
    
    def update_topic_priority(self, topic_id, new_priority):
        """更新主题优先级"""
        for topic in self.topics:
            if topic['id'] == topic_id:
                old_priority = topic['priority']
                topic['priority'] = new_priority
                self.save_topics()
                logger.info("更新主题优先级: %s (%d → %d)" % (topic['topic'], old_priority, new_priority))
                return True
        logger.warning("未找到主题ID: %d" % topic_id)
        return False
    
    def get_topics_by_priority(self):
        """按优先级排序获取主题"""
        return sorted(self.topics, key=lambda x: x['priority'], reverse=True)
    
    def get_topics_by_category(self, category):
        """按分类获取主题"""
        return [t for t in self.topics if t['category'] == category]
    
    def get_topic_by_id(self, topic_id):
        """按ID获取主题"""
        for topic in self.topics:
            if topic['id'] == topic_id:
                return topic
        return None
    
    def update_topic_stats(self, topic_id, score):
        """更新主题学习统计"""
        for topic in self.topics:
            if topic['id'] == topic_id:
                topic['learning_count'] += 1
                topic['last_learning_at'] = datetime.now().isoformat()
                
                # 更新平均评分
                if topic['average_score'] == 0:
                    topic['average_score'] = score
                else:
                    topic['average_score'] = round(
                        (topic['average_score'] * (topic['learning_count'] - 1) + score) / topic['learning_count']
                    )
                
                # 根据学习效果调整优先级
                self.adjust_priority_based_on_score(topic)
                self.save_topics()
                return True
        return False
    
    def adjust_priority_based_on_score(self, topic):
        """根据学习效果调整优先级"""
        score = topic['average_score']
        if score >= 90:
            # 学习效果优秀，降低优先级（已掌握）
            if topic['priority'] > 1:
                topic['priority'] -= 1
        elif score < 70:
            # 学习效果较差，提高优先级（需要加强）
            if topic['priority'] < 10:
                topic['priority'] += 1
    
    def get_recommended_topics(self, count=5, skill_focus=None, difficulty_filter=None):
        """获取智能推荐学习主题"""
        # 过滤条件
        filtered_topics = self.topics
        
        # 按技能过滤
        if skill_focus:
            filtered_topics = [t for t in filtered_topics if t['skill'] == skill_focus]
        
        # 按难度过滤
        if difficulty_filter:
            filtered_topics = [t for t in filtered_topics if t.get('difficulty') == difficulty_filter]
        
        # 计算推荐分数
        scored_topics = []
        for topic in filtered_topics:
            score = self.calculate_recommendation_score(topic)
            scored_topics.append((topic, score))
        
        # 按推荐分数排序
        scored_topics.sort(key=lambda x: -x[1])
        
        # 返回推荐主题
        recommendations = []
        for topic, score in scored_topics[:count]:
            recommendations.append({
                'topic': topic['topic'],
                'skill': topic['skill'],
                'priority': topic['priority'],
                'category': topic['category'],
                'difficulty': topic.get('difficulty', 'medium'),
                'learning_count': topic.get('learning_count', 0),
                'average_score': topic.get('average_score', 0),
                'recommendation_score': round(score, 2)
            })
        
        logger.info("生成了 %d 个推荐学习主题" % len(recommendations))
        return recommendations
    
    def calculate_recommendation_score(self, topic):
        """计算主题推荐分数"""
        score = 0
        
        # 基础优先级 (30%)
        score += topic['priority'] * 0.03
        
        # 技能熟练度因素 (25%) - 熟练度越低，越需要学习
        skill_name = topic['skill']
        proficiency = self.skill_proficiency.get(skill_name, 50)
        score += (100 - proficiency) * 0.0025
        
        # 学习次数因素 (20%) - 学习次数越少，越需要学习
        learning_count = topic.get('learning_count', 0)
        score += max(0, (10 - learning_count)) * 0.02
        
        # 学习效果因素 (15%) - 平均分数越低，越需要学习
        avg_score = topic.get('average_score', 0)
        if avg_score > 0:
            score += (100 - avg_score) * 0.0015
        
        # 难度匹配因素 (10%) - 根据熟练度匹配难度
        difficulty = topic.get('difficulty', 'medium')
        difficulty_bonus = self.get_difficulty_bonus(proficiency, difficulty)
        score += difficulty_bonus
        
        return score
    
    def get_difficulty_bonus(self, proficiency, difficulty):
        """根据熟练度和难度计算匹配奖励"""
        # 新手适合简单，进阶适合中等，高手适合困难
        if proficiency < 50:
            # 初学者
            if difficulty == 'easy':
                return 1.5
            elif difficulty == 'medium':
                return 0.5
            else:
                return -1
        elif proficiency < 70:
            # 进阶者
            if difficulty == 'easy':
                return 0.5
            elif difficulty == 'medium':
                return 1.5
            else:
                return 0.5
        else:
            # 高手
            if difficulty == 'easy':
                return -0.5
            elif difficulty == 'medium':
                return 0.5
            else:
                return 1.5
    
    def get_personalized_recommendations(self, count=5):
        """获取个性化推荐"""
        # 识别薄弱技能
        weak_skills = self.get_weak_skills()
        
        recommendations = []
        
        # 优先推荐薄弱技能的学习主题
        for skill in weak_skills[:3]:
            skill_topics = self.get_recommended_topics(count=2, skill_focus=skill)
            recommendations.extend(skill_topics)
        
        # 如果推荐不足，补充通用推荐
        if len(recommendations) < count:
            remaining = count - len(recommendations)
            general_recs = self.get_recommended_topics(count=remaining)
            recommendations.extend(general_recs)
        
        return recommendations[:count]
    
    def get_weak_skills(self, threshold=60):
        """获取熟练度低于阈值的技能"""
        weak_skills = []
        for skill, proficiency in self.skill_proficiency.items():
            if proficiency < threshold:
                weak_skills.append((skill, proficiency))
        
        # 按熟练度排序
        weak_skills.sort(key=lambda x: x[1])
        return [skill for skill, _ in weak_skills]
    
    def get_categories(self):
        """获取所有分类"""
        categories = set(t['category'] for t in self.topics)
        return sorted(list(categories))
    
    def get_stats(self):
        """获取主题统计信息"""
        stats = {
            'total_topics': len(self.topics),
            'categories': self.get_categories(),
            'topics_by_category': {},
            'average_priority': 0,
            'most_learned_topic': None,
            'least_learned_topic': None
        }
        
        # 按分类统计
        for category in stats['categories']:
            stats['topics_by_category'][category] = len(self.get_topics_by_category(category))
        
        # 平均优先级
        if self.topics:
            stats['average_priority'] = round(sum(t['priority'] for t in self.topics) / len(self.topics))
        
        # 学习次数最多和最少的主题
        if self.topics:
            stats['most_learned_topic'] = max(self.topics, key=lambda x: x['learning_count'])['topic']
            stats['least_learned_topic'] = min(self.topics, key=lambda x: x['learning_count'])['topic']
        
        return stats

# 测试主题管理器
if __name__ == "__main__":
    manager = DynamicTopicManager()
    
    # 添加新主题
    manager.add_topic("恐怖小说氛围营造", "环境氛围营造师", priority=7, category="场景设计")
    
    # 获取推荐主题
    recommended = manager.get_recommended_topics(3)
    print("\n推荐学习主题:")
    for t in recommended:
        print("  - %s (优先级: %d)" % (t['topic'], t['priority']))
    
    # 获取统计信息
    stats = manager.get_stats()
    print("\n主题统计:")
    print(json.dumps(stats, ensure_ascii=False, indent=2))