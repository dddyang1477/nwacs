#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 创作数据统计面板
功能：字数统计、学习统计、进度可视化、数据导出
"""

import os
import json
from datetime import datetime, timedelta
from logger import logger

class WritingStatsDashboard:
    """创作数据统计面板"""
    
    def __init__(self):
        self.stats_file = "writing_stats.json"
        self.daily_records = []
        self.learning_records = []
        self.project_stats = {}
        
        self._load_stats()
    
    def _load_stats(self):
        """加载统计数据"""
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.daily_records = data.get('daily_records', [])
                    self.learning_records = data.get('learning_records', [])
                    self.project_stats = data.get('project_stats', {})
                logger.info("统计数据已加载")
            except Exception as e:
                logger.log_exception(e, "加载统计数据")
                self.daily_records = []
                self.learning_records = []
                self.project_stats = {}
    
    def _save_stats(self):
        """保存统计数据"""
        try:
            data = {
                'daily_records': self.daily_records,
                'learning_records': self.learning_records,
                'project_stats': self.project_stats
            }
            
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.log_exception(e, "保存统计数据")
    
    def record_writing(self, project_name, word_count, chapter_count=0):
        """记录写作"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        # 查找今日记录
        today_record = None
        for record in self.daily_records:
            if record['date'] == today and record['project'] == project_name:
                today_record = record
                break
        
        if today_record:
            # 更新记录
            today_record['word_count'] += word_count
            today_record['chapter_count'] += chapter_count
            today_record['last_updated'] = datetime.now().isoformat()
        else:
            # 新增记录
            self.daily_records.append({
                'date': today,
                'project': project_name,
                'word_count': word_count,
                'chapter_count': chapter_count,
                'timestamp': datetime.now().isoformat()
            })
        
        # 更新项目统计
        if project_name not in self.project_stats:
            self.project_stats[project_name] = {
                'total_words': 0,
                'total_chapters': 0,
                'start_date': today,
                'last_writing_date': today
            }
        
        self.project_stats[project_name]['total_words'] += word_count
        self.project_stats[project_name]['total_chapters'] += chapter_count
        self.project_stats[project_name]['last_writing_date'] = today
        
        self._save_stats()
        logger.info("已记录写作：%s +%d 字" % (project_name, word_count))
    
    def record_learning(self, skill_name, topic, duration_minutes=0):
        """记录学习"""
        self.learning_records.append({
            'skill_name': skill_name,
            'topic': topic,
            'duration_minutes': duration_minutes,
            'timestamp': datetime.now().isoformat()
        })
        
        # 保持记录数量
        if len(self.learning_records) > 1000:
            self.learning_records = self.learning_records[-1000:]
        
        self._save_stats()
        logger.debug("已记录学习：%s - %s" % (skill_name, topic))
    
    def get_daily_summary(self, date=None):
        """获取每日摘要"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        # 查找指定日期记录
        day_records = [r for r in self.daily_records if r['date'] == date]
        
        if not day_records:
            return {
                'date': date,
                'message': '今日暂无写作记录',
                'total_words': 0,
                'total_chapters': 0
            }
        
        total_words = sum(r['word_count'] for r in day_records)
        total_chapters = sum(r['chapter_count'] for r in day_records)
        
        return {
            'date': date,
            'projects': len(day_records),
            'total_words': total_words,
            'total_chapters': total_chapters,
            'details': day_records
        }
    
    def get_weekly_summary(self):
        """获取每周摘要"""
        today = datetime.now()
        week_start = today - timedelta(days=today.weekday())
        
        weekly_data = {}
        
        for i in range(7):
            date = (week_start + timedelta(days=i)).strftime("%Y-%m-%d")
            day_summary = self.get_daily_summary(date)
            weekly_data[date] = day_summary
        
        total_words = sum(d['total_words'] for d in weekly_data.values())
        
        return {
            'week_start': week_start.strftime("%Y-%m-%d"),
            'week_end': (week_start + timedelta(days=6)).strftime("%Y-%m-%d"),
            'daily_data': weekly_data,
            'total_words': total_words,
            'avg_daily_words': total_words / 7
        }
    
    def get_project_summary(self, project_name):
        """获取项目摘要"""
        if project_name not in self.project_stats:
            return {'message': '项目不存在'}
        
        stats = self.project_stats[project_name]
        
        # 计算写作天数
        project_records = [r for r in self.daily_records if r['project'] == project_name]
        writing_days = len(set(r['date'] for r in project_records))
        
        return {
            'project_name': project_name,
            'total_words': stats['total_words'],
            'total_chapters': stats['total_chapters'],
            'start_date': stats['start_date'],
            'last_writing_date': stats['last_writing_date'],
            'writing_days': writing_days,
            'avg_daily_words': stats['total_words'] / writing_days if writing_days > 0 else 0
        }
    
    def get_learning_summary(self, skill_name=None):
        """获取学习摘要"""
        if skill_name:
            records = [r for r in self.learning_records if r['skill_name'] == skill_name]
        else:
            records = self.learning_records
        
        if not records:
            return {'message': '暂无学习记录'}
        
        # 按 Skill 统计
        skill_stats = {}
        for record in records:
            skill = record['skill_name']
            if skill not in skill_stats:
                skill_stats[skill] = {
                    'count': 0,
                    'topics': set(),
                    'total_duration': 0
                }
            
            skill_stats[skill]['count'] += 1
            skill_stats[skill]['topics'].add(record['topic'])
            skill_stats[skill]['total_duration'] += record.get('duration_minutes', 0)
        
        # 转换为可序列化格式
        result = {
            'total_learning_count': len(records),
            'skills': {}
        }
        
        for skill, stats in skill_stats.items():
            result['skills'][skill] = {
                'learning_count': stats['count'],
                'unique_topics': len(stats['topics']),
                'total_duration_minutes': stats['total_duration'],
                'avg_duration_minutes': stats['total_duration'] / stats['count'] if stats['count'] > 0 else 0
            }
        
        return result
    
    def get_achievement_badges(self):
        """获取成就徽章"""
        badges = []
        
        # 写作成就
        total_words = sum(r['word_count'] for r in self.daily_records)
        
        if total_words >= 1000000:
            badges.append({'name': '百万字作家', 'description': '累计写作 100 万字', 'icon': '🏆'})
        elif total_words >= 100000:
            badges.append({'name': '十万字作家', 'description': '累计写作 10 万字', 'icon': '📝'})
        elif total_words >= 10000:
            badges.append({'name': '万字新手', 'description': '累计写作 1 万字', 'icon': '✏️'})
        
        # 坚持成就
        if len(self.daily_records) >= 30:
            badges.append({'name': '坚持写作 30 天', 'description': '连续写作 30 天', 'icon': '🔥'})
        
        # 学习成就
        if len(self.learning_records) >= 100:
            badges.append({'name': '学习达人', 'description': '学习 100 次', 'icon': '📚'})
        
        return badges
    
    def export_report(self, format='text'):
        """导出报告"""
        report = []
        report.append("=" * 60)
        report.append("    NWACS 创作数据统计报告")
        report.append("=" * 60)
        report.append("")
        
        # 总体统计
        total_words = sum(r['word_count'] for r in self.daily_records)
        total_learning = len(self.learning_records)
        total_projects = len(self.project_stats)
        
        report.append("【总体统计】")
        report.append("  累计写作字数：%d" % total_words)
        report.append("  累计学习次数：%d" % total_learning)
        report.append("  项目数量：%d" % total_projects)
        report.append("")
        
        # 今日数据
        today_summary = self.get_daily_summary()
        report.append("【今日数据】")
        report.append("  日期：%s" % today_summary['date'])
        report.append("  写作字数：%d" % today_summary['total_words'])
        report.append("  写作章节：%d" % today_summary['total_chapters'])
        report.append("")
        
        # 本周数据
        weekly_summary = self.get_weekly_summary()
        report.append("【本周数据】")
        report.append("  周期：%s ~ %s" % (weekly_summary['week_start'], weekly_summary['week_end']))
        report.append("  总字数：%d" % weekly_summary['total_words'])
        report.append("  日均字数：%.0f" % weekly_summary['avg_daily_words'])
        report.append("")
        
        # 成就徽章
        badges = self.get_achievement_badges()
        if badges:
            report.append("【成就徽章】")
            for badge in badges:
                report.append("  %s %s" % (badge['icon'], badge['name']))
        report.append("")
        
        report.append("=" * 60)
        
        if format == 'text':
            return "\n".join(report)
        elif format == 'json':
            return json.dumps({
                'total_words': total_words,
                'total_learning': total_learning,
                'total_projects': total_projects,
                'today': today_summary,
                'weekly': weekly_summary,
                'badges': badges
            }, ensure_ascii=False, indent=2)
    
    def clear_data(self):
        """清空数据"""
        self.daily_records = []
        self.learning_records = []
        self.project_stats = {}
        self._save_stats()
        logger.info("统计数据已清空")


# 全局统计面板实例
stats_dashboard = WritingStatsDashboard()


def get_stats_dashboard():
    """获取统计面板实例"""
    return stats_dashboard
