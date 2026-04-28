#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 学习效果评估系统 v2.0
评估学习效果，量化学习成果
新增：更多评估指标、学习进度追踪、个性化建议
"""

import json
import os
import statistics
from datetime import datetime, timedelta
from logger import logger

class LearningEvaluator:
    def __init__(self):
        self.evaluation_records = []
        self.skill_improvement = {}
        self.learning_progress = {}  # 学习进度追踪
        self.topic_mastery = {}      # 主题掌握程度
        self.load_records()
    
    def load_records(self):
        """加载历史评估记录"""
        if os.path.exists('learning_evaluation.json'):
            try:
                with open('learning_evaluation.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.evaluation_records = data.get('records', [])
                    self.skill_improvement = data.get('skill_improvement', {})
                logger.info("学习评估记录加载成功")
            except Exception as e:
                logger.log_exception(e, "load_records")
    
    def save_records(self):
        """保存评估记录"""
        try:
            data = {
                'records': self.evaluation_records,
                'skill_improvement': self.skill_improvement,
                'last_update': datetime.now().isoformat()
            }
            with open('learning_evaluation.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.debug("学习评估记录保存成功")
        except Exception as e:
            logger.log_exception(e, "save_records")
    
    def evaluate_learning(self, topic, skill_name=None, metrics=None):
        """评估单次学习效果"""
        if metrics is None:
            metrics = {}
        
        # 扩展评估指标
        evaluation = {
            'topic': topic,
            'skill_name': skill_name,
            'timestamp': datetime.now().isoformat(),
            'duration': metrics.get('duration', 30),  # 学习时长（分钟）
            'metrics': {
                # 认知维度
                'knowledge_acquisition': metrics.get('knowledge_acquisition', 80),
                'understanding_depth': metrics.get('understanding_depth', 75),
                'retention_rate': metrics.get('retention_rate', 85),
                'comprehension_level': metrics.get('comprehension_level', 78),
                
                # 技能维度
                'skill_improvement': metrics.get('skill_improvement', 75),
                'application_ability': metrics.get('application_ability', 70),
                'problem_solving': metrics.get('problem_solving', 72),
                'creativity_enhancement': metrics.get('creativity_enhancement', 68),
                
                # 行为维度
                'learning_efficiency': metrics.get('learning_efficiency', 75),
                'focus_level': metrics.get('focus_level', 80),
                'active_participation': metrics.get('active_participation', 75),
                'practice_frequency': metrics.get('practice_frequency', 70)
            },
            'overall_score': 0,
            'feedback': '',
            'mastery_level': '',
            'suggestions': []
        }
        
        # 计算综合评分
        evaluation['overall_score'] = self.calculate_overall_score(evaluation['metrics'])
        
        # 确定掌握程度
        evaluation['mastery_level'] = self.determine_mastery_level(evaluation['overall_score'])
        
        # 生成反馈和建议
        evaluation['feedback'] = self.generate_feedback(evaluation)
        evaluation['suggestions'] = self.generate_personalized_suggestions(evaluation)
        
        # 更新学习进度和主题掌握程度
        self.update_learning_progress(topic, evaluation)
        self.update_topic_mastery(topic, evaluation['overall_score'])
        
        # 更新Skill改进记录
        if skill_name:
            self.update_skill_improvement(skill_name, evaluation['overall_score'])
        
        # 保存记录
        self.evaluation_records.append(evaluation)
        self.save_records()
        
        logger.info("学习评估完成: %s, 综合评分: %d, 掌握程度: %s" % 
                   (topic, evaluation['overall_score'], evaluation['mastery_level']))
        return evaluation
    
    def determine_mastery_level(self, score):
        """确定主题掌握程度"""
        if score >= 95:
            return "精通"
        elif score >= 85:
            return "熟练"
        elif score >= 75:
            return "掌握"
        elif score >= 65:
            return "了解"
        elif score >= 50:
            return "入门"
        else:
            return "未掌握"
    
    def calculate_overall_score(self, metrics):
        """计算综合评分"""
        # 加权计算，认知维度占40%，技能维度占40%，行为维度占20%
        weights = {
            # 认知维度 (40%)
            'knowledge_acquisition': 0.12,
            'understanding_depth': 0.10,
            'retention_rate': 0.10,
            'comprehension_level': 0.08,
            
            # 技能维度 (40%)
            'skill_improvement': 0.12,
            'application_ability': 0.10,
            'problem_solving': 0.10,
            'creativity_enhancement': 0.08,
            
            # 行为维度 (20%)
            'learning_efficiency': 0.06,
            'focus_level': 0.06,
            'active_participation': 0.04,
            'practice_frequency': 0.04
        }
        
        total = 0
        for key, weight in weights.items():
            total += metrics.get(key, 0) * weight
        
        return round(total)
    
    def update_learning_progress(self, topic, evaluation):
        """更新学习进度"""
        if topic not in self.learning_progress:
            self.learning_progress[topic] = {
                'total_learning_time': 0,
                'learning_count': 0,
                'average_score': 0,
                'last_learning_time': None,
                'mastery_progress': 0
            }
        
        self.learning_progress[topic]['total_learning_time'] += evaluation['duration']
        self.learning_progress[topic]['learning_count'] += 1
        self.learning_progress[topic]['last_learning_time'] = datetime.now().isoformat()
        
        # 计算平均分数
        scores = [e['overall_score'] for e in self.evaluation_records if e['topic'] == topic]
        if scores:
            self.learning_progress[topic]['average_score'] = round(sum(scores) / len(scores))
            # 计算掌握进度 (0-100%)
            self.learning_progress[topic]['mastery_progress'] = min(100, self.learning_progress[topic]['average_score'])
    
    def update_topic_mastery(self, topic, score):
        """更新主题掌握程度"""
        if topic not in self.topic_mastery:
            self.topic_mastery[topic] = {
                'scores': [],
                'average_score': 0,
                'mastery_level': '未掌握',
                'trend': 0
            }
        
        self.topic_mastery[topic]['scores'].append({
            'score': score,
            'timestamp': datetime.now().isoformat()
        })
        
        scores = self.topic_mastery[topic]['scores']
        self.topic_mastery[topic]['average_score'] = round(sum(s['score'] for s in scores) / len(scores))
        self.topic_mastery[topic]['mastery_level'] = self.determine_mastery_level(self.topic_mastery[topic]['average_score'])
        
        # 计算趋势
        if len(scores) >= 2:
            recent_scores = [s['score'] for s in scores[-3:]]
            if len(recent_scores) >= 2:
                self.topic_mastery[topic]['trend'] = recent_scores[-1] - recent_scores[0]
    
    def generate_personalized_suggestions(self, evaluation):
        """生成个性化建议"""
        suggestions = []
        score = evaluation['overall_score']
        metrics = evaluation['metrics']
        topic = evaluation['topic']
        
        # 根据各维度指标生成建议
        if metrics.get('knowledge_acquisition', 0) < 70:
            suggestions.append(f"建议增加对「{topic}」基础知识的学习时间")
        
        if metrics.get('application_ability', 0) < 70:
            suggestions.append(f"建议多做「{topic}」相关的实践练习")
        
        if metrics.get('retention_rate', 0) < 75:
            suggestions.append(f"建议采用间隔重复学习法巩固「{topic}」的知识")
        
        if metrics.get('focus_level', 0) < 70:
            suggestions.append("建议在学习时减少干扰，提高专注度")
        
        if metrics.get('practice_frequency', 0) < 60:
            suggestions.append("建议增加练习频率，熟能生巧")
        
        # 根据综合评分生成建议
        if score >= 90:
            suggestions.append("学习效果优秀！建议尝试更深入的学习内容")
        elif score >= 80:
            suggestions.append("学习效果良好！建议拓展相关领域的学习")
        elif score >= 70:
            suggestions.append(f"建议针对「{topic}」的薄弱环节进行强化训练")
        elif score >= 60:
            suggestions.append(f"建议重新学习「{topic}」的核心内容")
        else:
            suggestions.append(f"「{topic}」掌握程度较低，建议系统性地重新学习")
        
        return suggestions
    
    def generate_feedback(self, evaluation):
        """生成评估反馈"""
        score = evaluation['overall_score']
        
        if score >= 90:
            return "优秀！学习效果非常好，知识掌握扎实，建议继续保持。"
        elif score >= 80:
            return "良好！学习效果不错，建议加强实践应用。"
        elif score >= 70:
            return "中等！学习效果一般，建议回顾重点内容。"
        elif score >= 60:
            return "及格！学习效果有待提高，建议增加学习时间。"
        else:
            return "不及格！学习效果较差，建议重新学习相关内容。"
    
    def update_skill_improvement(self, skill_name, score):
        """更新Skill改进记录"""
        if skill_name not in self.skill_improvement:
            self.skill_improvement[skill_name] = {
                'scores': [],
                'improvement_trend': 0,
                'last_updated': datetime.now().isoformat()
            }
        
        self.skill_improvement[skill_name]['scores'].append({
            'score': score,
            'timestamp': datetime.now().isoformat()
        })
        
        # 计算改进趋势
        scores = self.skill_improvement[skill_name]['scores']
        if len(scores) >= 2:
            recent = [s['score'] for s in scores[-3:]]
            if len(recent) >= 2:
                trend = recent[-1] - recent[0]
                self.skill_improvement[skill_name]['improvement_trend'] = trend
        
        self.skill_improvement[skill_name]['last_updated'] = datetime.now().isoformat()
    
    def generate_report(self):
        """生成学习效果报告"""
        if not self.evaluation_records:
            return "暂无评估记录"
        
        report = {
            'summary': {
                'total_evaluations': len(self.evaluation_records),
                'average_score': self.get_average_score(),
                'top_topics': self.get_top_topics(),
                'weak_areas': self.get_weak_areas()
            },
            'skill_analysis': self.analyze_skill_improvement(),
            'recommendations': self.generate_recommendations(),
            'generated_at': datetime.now().isoformat()
        }
        
        return report
    
    def get_average_score(self):
        """计算平均评分"""
        if not self.evaluation_records:
            return 0
        
        total = sum(e['overall_score'] for e in self.evaluation_records)
        return round(total / len(self.evaluation_records))
    
    def get_top_topics(self):
        """获取学习效果最好的主题"""
        if not self.evaluation_records:
            return []
        
        sorted_records = sorted(self.evaluation_records, key=lambda x: x['overall_score'], reverse=True)
        return [r['topic'] for r in sorted_records[:3]]
    
    def get_weak_areas(self):
        """识别薄弱领域"""
        if not self.evaluation_records:
            return []
        
        sorted_records = sorted(self.evaluation_records, key=lambda x: x['overall_score'])
        return [r['topic'] for r in sorted_records[:2]]
    
    def analyze_skill_improvement(self):
        """分析Skill改进情况"""
        analysis = {}
        for skill_name, data in self.skill_improvement.items():
            scores = [s['score'] for s in data['scores']]
            if scores:
                analysis[skill_name] = {
                    'average_score': round(sum(scores) / len(scores)),
                    'improvement_trend': data['improvement_trend'],
                    'evaluation_count': len(scores)
                }
        return analysis
    
    def generate_recommendations(self):
        """生成改进建议"""
        recommendations = []
        avg_score = self.get_average_score()
        
        if avg_score < 70:
            recommendations.append("建议增加学习时间，重点复习评分较低的主题。")
        
        weak_areas = self.get_weak_areas()
        if weak_areas:
            recommendations.append("建议加强以下领域的学习：%s" % ", ".join(weak_areas))
        
        # 检查改进趋势
        for skill_name, data in self.skill_improvement.items():
            if data['improvement_trend'] < 0:
                recommendations.append("%s 的学习效果有所下降，建议调整学习方法。" % skill_name)
        
        if not recommendations:
            recommendations.append("学习效果良好，继续保持！")
        
        return recommendations

# 测试评估系统
if __name__ == "__main__":
    evaluator = LearningEvaluator()
    
    # 模拟评估
    evaluator.evaluate_learning("情感描写技巧", "对话设计师", {
        'knowledge_acquisition': 85,
        'skill_improvement': 80,
        'application_ability': 75,
        'retention_rate': 90,
        'depth_of_learning': 82
    })
    
    evaluator.evaluate_learning("人物刻画方法", "角色性格塑造师", {
        'knowledge_acquisition': 78,
        'skill_improvement': 75,
        'application_ability': 70,
        'retention_rate': 85,
        'depth_of_learning': 76
    })
    
    # 生成报告
    report = evaluator.generate_report()
    print("\n学习效果评估报告:")
    print(json.dumps(report, ensure_ascii=False, indent=2))