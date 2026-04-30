#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 学习内容智能分发模块
功能：智能匹配 Skill、避免重复学习、精准分发
"""

import json
import os
import re
from datetime import datetime
from logger import logger

class SmartLearningDistributor:
    """智能学习分发器"""
    
    def __init__(self):
        self.skill_topic_map = {}
        self.learning_history = []
        self.history_file = "learning_history.json"
        
        # Skill 与主题的映射关系
        self.skill_keywords = {
            '短篇小说爽文大师': ['短篇', '爽文', '爆款', '节奏', '开篇', '反转', '狗血', '甜宠', '虐恋'],
            '世界观构造师': ['世界', '规则', '设定', '地理', '历史', '体系', '修炼', '境界'],
            '剧情构造师': ['剧情', '结构', '三幕', '高潮', '伏笔', '转折', '线索'],
            '角色塑造师': ['角色', '人物', '性格', '背景', '成长', '关系', '动机'],
            '场景构造师': ['场景', '环境', '氛围', '空间', '描写', '感官'],
            '对话设计师': ['对话', '台词', '语气', '个性', '交流', '冲突'],
            '战斗设计师': ['战斗', '招式', '技能', '对决', '打斗', '特效'],
            '写作技巧大师': ['技巧', '文笔', '风格', '修辞', '表达', '优化'],
            '去 AI 痕迹监督官': ['AI', '痕迹', '自然', '人性化', '去 AI 化'],
            '词汇大师': ['词汇', '名词', '素材', '命名', '形容', '描写'],
            '规则掌控者': ['规则', '法则', '自然', '物理', '逻辑'],
            '质量审计师': ['质量', '标准', '评估', '审核', '检查'],
            '学习大师': ['学习', '趋势', '热点', '分析', '计划']
        }
        
        self._load_history()
    
    def _load_history(self):
        """加载学习历史"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.learning_history = json.load(f)
                logger.info("学习历史已加载，共 %d 条记录" % len(self.learning_history))
            except Exception:
                self.learning_history = []
    
    def _save_history(self):
        """保存学习历史"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.learning_history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.log_exception(e, "保存学习历史")
    
    def match_skill(self, topic):
        """智能匹配最适合的 Skill"""
        scores = {}
        
        # 计算每个 Skill 的匹配度
        for skill, keywords in self.skill_keywords.items():
            score = 0
            
            # 关键词匹配
            for keyword in keywords:
                if keyword in topic:
                    score += 10
            
            # 语义相似度（简化版：计算共同字符）
            topic_chars = set(topic)
            for keyword in keywords:
                keyword_chars = set(keyword)
                common = len(topic_chars & keyword_chars)
                score += common * 0.5
            
            scores[skill] = score
        
        # 返回匹配度最高的 Skill
        if scores:
            best_match = max(scores.items(), key=lambda x: x[1])
            logger.debug("主题 '%s' 匹配 Skill: %s (得分：%.1f)" % 
                        (topic, best_match[0], best_match[1]))
            return best_match[0]
        
        return '学习大师'  # 默认
    
    def should_learn(self, skill_name, topic):
        """判断是否需要学习（避免重复）"""
        current_time = datetime.now()
        
        # 检查最近是否学习过相同主题
        for record in self.learning_history[-50:]:  # 只检查最近 50 条
            if (record['skill_name'] == skill_name and 
                record['topic'] == topic):
                
                record_time = datetime.fromisoformat(record['timestamp'])
                time_diff = (current_time - record_time).total_seconds()
                
                # 24 小时内不重复学习同一主题
                if time_diff < 86400:
                    logger.debug("%s 在 24 小时内已学习过 '%s'，跳过" % (skill_name, topic))
                    return False
        
        return True
    
    def distribute_learning(self, learning_result):
        """智能分发学习内容到多个 Skill"""
        topic = learning_result.get('topic', '')
        skill_name = learning_result.get('skill_name', '')
        
        # 1. 判断是否需要学习
        if not self.should_learn(skill_name, topic):
            return {'distributed': False, 'reason': '重复学习'}
        
        # 2. 匹配最适合的 Skill
        best_skill = self.match_skill(topic)
        
        # 3. 如果当前 Skill 不是最佳匹配，建议分发到最佳 Skill
        if best_skill != skill_name:
            logger.info("建议将 '%s' 分发到 %s（当前：%s）" % 
                       (topic, best_skill, skill_name))
        
        # 4. 记录学习历史
        self.learning_history.append({
            'skill_name': skill_name,
            'topic': topic,
            'timestamp': datetime.now().isoformat(),
            'matched_skill': best_skill,
            'key_points_count': len(learning_result.get('key_points', []))
        })
        
        # 保持历史记录数量
        if len(self.learning_history) > 1000:
            self.learning_history = self.learning_history[-1000:]
        
        self._save_history()
        
        return {
            'distributed': True,
            'target_skill': best_skill,
            'current_skill': skill_name,
            'topic': topic
        }
    
    def get_learning_suggestions(self, skill_name):
        """为 Skill 提供学习建议"""
        # 分析该 Skill 的历史学习记录
        skill_records = [r for r in self.learning_history if r['skill_name'] == skill_name]
        
        if not skill_records:
            return {
                'suggestion': '该 Skill 尚未开始学习，建议从基础主题开始',
                'recommended_topics': self._get_recommended_topics(skill_name)
            }
        
        # 分析学习频率
        recent_records = skill_records[-10:]
        if len(recent_records) < 3:
            return {
                'suggestion': '学习频率较低，建议增加学习次数',
                'recommended_topics': self._get_recommended_topics(skill_name)
            }
        
        # 分析学习内容分布
        topics = [r['topic'] for r in recent_records]
        unique_topics = len(set(topics))
        
        if unique_topics < 3:
            return {
                'suggestion': '学习内容较为单一，建议拓展学习范围',
                'recommended_topics': self._get_recommended_topics(skill_name)
            }
        
        return {
            'suggestion': '学习状态良好，继续保持',
            'recent_count': len(recent_records),
            'unique_topics': unique_topics
        }
    
    def _get_recommended_topics(self, skill_name):
        """推荐学习主题"""
        base_topics = {
            '短篇小说爽文大师': [
                '2026 年短篇爽文趋势',
                '爆款开篇技巧',
                '反转剧情设计',
                '读者心理把握'
            ],
            '世界观构造师': [
                '玄幻世界体系构建',
                '修炼等级设定',
                '地理环境设计',
                '社会结构规划'
            ],
            '剧情构造师': [
                '三幕式结构优化',
                '伏笔埋设技巧',
                '高潮设计方法',
                '多线叙事技巧'
            ],
            '角色塑造师': [
                '立体人物塑造',
                '角色成长弧线',
                '人物关系设计',
                '动机与冲突'
            ],
            '写作技巧大师': [
                '文笔优化技巧',
                '节奏把控方法',
                '对话描写技巧',
                '环境描写手法'
            ]
        }
        
        return base_topics.get(skill_name, ['写作基础技巧'])
    
    def generate_learning_report(self):
        """生成学习报告"""
        if not self.learning_history:
            return {'message': '暂无学习记录'}
        
        # 统计各 Skill 学习次数
        skill_stats = {}
        for record in self.learning_history:
            skill = record['skill_name']
            if skill not in skill_stats:
                skill_stats[skill] = {
                    'count': 0,
                    'topics': set(),
                    'total_points': 0
                }
            
            skill_stats[skill]['count'] += 1
            skill_stats[skill]['topics'].add(record['topic'])
            skill_stats[skill]['total_points'] += record.get('key_points_count', 0)
        
        # 转换为可序列化格式
        report = {
            'total_learning_count': len(self.learning_history),
            'skills': {}
        }
        
        for skill, stats in skill_stats.items():
            report['skills'][skill] = {
                'learning_count': stats['count'],
                'unique_topics': len(stats['topics']),
                'total_key_points': stats['total_points'],
                'avg_points_per_learning': stats['total_points'] / stats['count'] if stats['count'] > 0 else 0
            }
        
        return report


# 全局分发器实例
distributor = SmartLearningDistributor()


def get_learning_distributor():
    """获取学习分发器实例"""
    return distributor
