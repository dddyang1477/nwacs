"""
NWACS 节奏编织系统
基于 webnovel-writer Strand Weave 架构深度优化
追踪和管理小说的三条核心线索：主线/感情线/世界观线

核心功能：
1. Quest/Fire/Constellation 三线追踪
2. 节奏红线监控 - 防止某一线断档过长
3. 章节节奏分析 - 自动识别每章的三线占比
4. 节奏优化建议 - 当某线断档时给出提醒
"""

import re
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from collections import defaultdict


@dataclass
class StrandRecord:
    chapter: int
    quest_ratio: float
    fire_ratio: float
    constellation_ratio: float
    dominant_strand: str
    quest_content: List[str] = field(default_factory=list)
    fire_content: List[str] = field(default_factory=list)
    constellation_content: List[str] = field(default_factory=list)


STRAND_KEYWORDS = {
    'quest': [
        '战斗', '对决', '突破', '升级', '任务', '目标', '挑战', '危机',
        '敌人', '对手', '阴谋', '秘密', '真相', '关键', '核心', '冲突',
        '决战', '厮杀', '对抗', '争夺', '守护', '拯救', '毁灭', '威胁',
    ],
    'fire': [
        '温柔', '关心', '守护', '陪伴', '信任', '理解', '默契', '心动',
        '脸红', '心跳', '拥抱', '牵手', '眼神', '微笑', '感动', '温暖',
        '思念', '牵挂', '约定', '承诺', '告白', '恋爱', '情感', '羁绊',
    ],
    'constellation': [
        '世界', '大陆', '帝国', '宗门', '势力', '传说', '历史', '远古',
        '秘境', '遗迹', '法则', '天道', '规则', '秩序', '文明', '种族',
        '神灵', '魔界', '仙界', '位面', '宇宙', '星辰', '维度', '时空',
    ],
}


class StrandWeaveEngine:
    def __init__(self):
        self.records: List[StrandRecord] = []
        self._chapter_analysis: Dict[int, StrandRecord] = {}

    def analyze_chapter(self, chapter_num: int, content: str) -> StrandRecord:
        paragraphs = [p for p in content.split('\n') if p.strip() and len(p) > 10]
        total_paras = len(paragraphs)
        if total_paras == 0:
            return StrandRecord(chapter=chapter_num, quest_ratio=0, fire_ratio=0,
                                constellation_ratio=0, dominant_strand='none')

        quest_count = 0
        fire_count = 0
        constellation_count = 0
        quest_content = []
        fire_content = []
        constellation_content = []

        for para in paragraphs:
            q_score = sum(1 for kw in STRAND_KEYWORDS['quest'] if kw in para)
            f_score = sum(1 for kw in STRAND_KEYWORDS['fire'] if kw in para)
            c_score = sum(1 for kw in STRAND_KEYWORDS['constellation'] if kw in para)

            max_score = max(q_score, f_score, c_score)
            if max_score == 0:
                continue

            if q_score == max_score:
                quest_count += 1
                if len(quest_content) < 3:
                    quest_content.append(para[:50])
            elif f_score == max_score:
                fire_count += 1
                if len(fire_content) < 3:
                    fire_content.append(para[:50])
            else:
                constellation_count += 1
                if len(constellation_content) < 3:
                    constellation_content.append(para[:50])

        total = quest_count + fire_count + constellation_count
        if total == 0:
            return StrandRecord(chapter=chapter_num, quest_ratio=0, fire_ratio=0,
                                constellation_ratio=0, dominant_strand='none')

        record = StrandRecord(
            chapter=chapter_num,
            quest_ratio=quest_count / total,
            fire_ratio=fire_count / total,
            constellation_ratio=constellation_count / total,
            dominant_strand='quest' if quest_count >= fire_count and quest_count >= constellation_count
            else 'fire' if fire_count >= constellation_count else 'constellation',
            quest_content=quest_content,
            fire_content=fire_content,
            constellation_content=constellation_content,
        )
        self._chapter_analysis[chapter_num] = record
        self.records.append(record)
        return record

    def get_rhythm_report(self) -> Dict[str, Any]:
        if not self.records:
            return {'status': 'no_data', 'message': '暂无章节数据'}

        quest_ratios = [r.quest_ratio for r in self.records]
        fire_ratios = [r.fire_ratio for r in self.records]
        const_ratios = [r.constellation_ratio for r in self.records]

        avg_quest = sum(quest_ratios) / len(quest_ratios) if quest_ratios else 0
        avg_fire = sum(fire_ratios) / len(fire_ratios) if fire_ratios else 0
        avg_const = sum(const_ratios) / len(const_ratios) if const_ratios else 0

        last_quest = 0
        last_fire = 0
        last_const = 0
        for i, r in enumerate(self.records):
            if r.quest_ratio > 0.1:
                last_quest = i + 1
            if r.fire_ratio > 0.1:
                last_fire = i + 1
            if r.constellation_ratio > 0.1:
                last_const = i + 1

        current_chapter = len(self.records)
        warnings = []
        if current_chapter - last_quest > 5:
            warnings.append(f'⚠️ 主线(Quest)已断档{current_chapter - last_quest}章，建议立即回归主线')
        if current_chapter - last_fire > 10:
            warnings.append(f'⚠️ 感情线(Fire)已断档{current_chapter - last_fire}章，建议加入感情戏')
        if current_chapter - last_const > 15:
            warnings.append(f'⚠️ 世界观线(Constellation)已断档{current_chapter - last_const}章，建议展开世界观')

        return {
            'status': 'active',
            'total_chapters': current_chapter,
            'average_ratios': {
                'quest': round(avg_quest, 2),
                'fire': round(avg_fire, 2),
                'constellation': round(avg_const, 2),
            },
            'ideal_ratios': {
                'quest': 0.60,
                'fire': 0.20,
                'constellation': 0.20,
            },
            'last_appearance': {
                'quest': last_quest,
                'fire': last_fire,
                'constellation': last_const,
            },
            'warnings': warnings,
            'chapter_details': [
                {
                    'chapter': r.chapter,
                    'quest': round(r.quest_ratio, 2),
                    'fire': round(r.fire_ratio, 2),
                    'constellation': round(r.constellation_ratio, 2),
                    'dominant': r.dominant_strand,
                }
                for r in self.records[-20:]
            ],
        }

    def get_strand_suggestion(self, chapter_num: int) -> str:
        report = self.get_rhythm_report()
        if report['status'] == 'no_data':
            return '建议从主线(Quest)开始写作'

        warnings = report.get('warnings', [])
        if warnings:
            return warnings[0]

        ratios = report['average_ratios']
        if ratios['quest'] < 0.5:
            return '主线占比偏低，建议加强剧情推进'
        elif ratios['fire'] < 0.15:
            return '感情线占比偏低，建议加入人物互动'
        elif ratios['constellation'] < 0.15:
            return '世界观线占比偏低，建议展开世界设定'
        else:
            return '节奏均衡，继续保持'

    def get_chapter_strand(self, chapter_num: int) -> Optional[StrandRecord]:
        return self._chapter_analysis.get(chapter_num)

    def get_strand_history(self) -> List[Dict]:
        return [
            {
                'chapter': r.chapter,
                'quest': round(r.quest_ratio, 2),
                'fire': round(r.fire_ratio, 2),
                'constellation': round(r.constellation_ratio, 2),
                'dominant': r.dominant_strand,
            }
            for r in self.records
        ]