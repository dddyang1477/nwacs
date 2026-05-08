#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
爽点节奏分析器 (Pleasure Beat Analyzer)

对标 星月写作 的"爽点节奏控制器"。
分析网文章节的节奏分布，检测爽点密度、情绪曲线、冲突强度，
提供节奏优化建议，确保每章都有足够的阅读快感。

核心能力:
- 爽点检测: 打脸/升级/收获/揭秘/情感爆发 5类爽点
- 情绪曲线: 绘制章节情绪起伏图
- 节奏评分: 0-100分，评估章节节奏健康度
- 优化建议: 指出节奏问题并给出具体修改方案
- 黄金三章检测: 验证开篇是否满足网文黄金三章法则
"""

import re
import json
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from collections import Counter


class BeatType(Enum):
    FACE_SLAP = "face_slap"           # 打脸/反转
    POWER_UP = "power_up"             # 升级/突破
    HARVEST = "harvest"               # 收获/获得
    REVEAL = "reveal"                 # 揭秘/真相
    EMOTIONAL = "emotional"           # 情感爆发
    CONFLICT = "conflict"             # 冲突/对抗
    SUSPENSE = "suspense"             # 悬念/钩子
    CLIMAX = "climax"                 # 高潮
    RELIEF = "relief"                 # 舒缓/过渡
    HOOK = "hook"                     # 钩子/章末悬念


@dataclass
class Beat:
    type: BeatType
    position: int          # 字符位置
    intensity: float       # 0.0-1.0
    text_snippet: str      # 相关文本片段
    line_number: int = 0


@dataclass
class RhythmProfile:
    total_beats: int
    beat_density: float           # 每千字爽点数
    emotion_curve: List[float]    # 情绪曲线(10段采样)
    conflict_curve: List[float]   # 冲突曲线
    pace_variance: float          # 节奏变化度
    hook_strength: float          # 章末钩子强度
    score: int                    # 综合评分 0-100
    issues: List[str]             # 问题列表
    suggestions: List[str]        # 优化建议


BEAT_PATTERNS: Dict[BeatType, List[Tuple[str, float]]] = {
    BeatType.FACE_SLAP: [
        ("打脸|反转|啪啪|脸肿|震惊|目瞪口呆|不敢置信|怎么可能", 0.8),
        ("冷笑|嘲讽|不屑|轻视|看不起|小瞧", 0.5),
        ("众人皆惊|全场哗然|一片死寂|鸦雀无声", 0.7),
        ("脸色大变|面色铁青|哑口无言|说不出话", 0.6),
    ],
    BeatType.POWER_UP: [
        ("突破|晋级|升级|进阶|觉醒|蜕变|涅槃", 0.9),
        ("瓶颈松动|桎梏破碎|豁然开朗|茅塞顿开", 0.7),
        ("实力暴涨|修为大增|功力精进|突飞猛进", 0.8),
        ("领悟|顿悟|参透|明悟|融会贯通", 0.6),
    ],
    BeatType.HARVEST: [
        ("获得|得到|收获|入手|到手|取得", 0.6),
        ("宝物|神器|秘籍|丹药|功法|机缘", 0.7),
        ("意外之喜|天降横财|捡到宝|发了", 0.5),
        ("储物袋|空间戒指|纳戒|乾坤袋", 0.4),
    ],
    BeatType.REVEAL: [
        ("原来|真相|秘密|隐情|内幕|缘由", 0.7),
        ("竟然是|居然是|没想到|不料|谁知", 0.8),
        ("恍然大悟|如梦初醒|幡然醒悟|终于明白", 0.7),
        ("身世|来历|背景|前世|宿命|因果", 0.6),
    ],
    BeatType.EMOTIONAL: [
        ("泪流满面|泣不成声|热泪盈眶|泪如雨下", 0.9),
        ("心如刀绞|痛彻心扉|撕心裂肺|肝肠寸断", 0.8),
        ("愤怒|暴怒|怒火|怒不可遏|勃然大怒", 0.7),
        ("感动|温暖|欣慰|释然|如释重负", 0.6),
    ],
    BeatType.CONFLICT: [
        ("战斗|厮杀|激战|大战|对决|交锋", 0.8),
        ("杀意|杀气|杀机|杀心|动了杀心", 0.7),
        ("对峙|僵持|剑拔弩张|一触即发", 0.6),
        ("受伤|吐血|重伤|奄奄一息|命悬一线", 0.7),
    ],
    BeatType.SUSPENSE: [
        ("难道|莫非|该不会|会不会|莫非是", 0.5),
        ("不对劲|诡异|奇怪|蹊跷|反常", 0.6),
        ("隐隐|似乎|好像|仿佛|如同", 0.3),
        ("伏笔|暗示|端倪|蛛丝马迹|苗头", 0.5),
    ],
    BeatType.CLIMAX: [
        ("巅峰|极致|极限|最强|无敌|碾压", 0.8),
        ("毁天灭地|天崩地裂|日月无光|山河变色", 0.9),
        ("最后一击|致命一击|绝杀|必杀", 0.8),
        ("胜负已分|尘埃落定|大局已定|已成定局", 0.7),
    ],
    BeatType.RELIEF: [
        ("休息|调息|恢复|疗伤|养伤", 0.4),
        ("日常|闲聊|谈笑|说笑|寒暄", 0.3),
        ("平静|宁静|安详|祥和|岁月静好", 0.3),
    ],
    BeatType.HOOK: [
        ("欲知后事|且听下回|预知后事|请看下章", 0.9),
        ("突然|忽然|猛地|骤然|陡然", 0.6),
        ("就在这时|正在此时|恰在此时|说时迟那时快", 0.5),
        ("未完待续|且看下回|下章更精彩", 0.8),
    ],
}

EMOTION_KEYWORDS = {
    "positive_high": ["狂喜", "兴奋", "激动", "热血沸腾", "豪情万丈", "意气风发"],
    "positive_mid": ["高兴", "欣慰", "满足", "温暖", "期待", "憧憬"],
    "positive_low": ["平静", "淡然", "从容", "释然", "安心", "踏实"],
    "negative_low": ["失落", "遗憾", "惆怅", "无奈", "疲惫", "迷茫"],
    "negative_mid": ["悲伤", "愤怒", "恐惧", "焦虑", "压抑", "痛苦"],
    "negative_high": ["绝望", "崩溃", "疯狂", "暴怒", "撕心裂肺", "万念俱灰"],
}


class PleasureBeatAnalyzer:
    """爽点节奏分析器"""

    def __init__(self):
        self._compiled_patterns: Dict[BeatType, List[Tuple[re.Pattern, float]]] = {}
        self._compile_patterns()

    def _compile_patterns(self):
        for beat_type, patterns in BEAT_PATTERNS.items():
            compiled = [(re.compile(p), w) for p, w in patterns]
            self._compiled_patterns[beat_type] = compiled

    def analyze(self, text: str, chapter_num: int = 1,
                is_opening: bool = False) -> RhythmProfile:
        """
        分析章节节奏

        Args:
            text: 章节文本
            chapter_num: 章节号
            is_opening: 是否为开篇章节(用于黄金三章检测)

        Returns:
            RhythmProfile: 节奏分析结果
        """
        beats = self._detect_beats(text)
        char_count = len(text)

        beat_density = len(beats) / (char_count / 1000) if char_count > 0 else 0

        emotion_curve = self._compute_emotion_curve(text)
        conflict_curve = self._compute_conflict_curve(beats, char_count)

        pace_variance = self._compute_pace_variance(text)

        hook_strength = self._evaluate_hook(text, beats)

        issues, suggestions = self._diagnose(
            beats, beat_density, emotion_curve, conflict_curve,
            pace_variance, hook_strength, char_count, is_opening, chapter_num,
        )

        score = self._compute_score(
            beat_density, emotion_curve, conflict_curve,
            pace_variance, hook_strength, len(issues),
        )

        return RhythmProfile(
            total_beats=len(beats),
            beat_density=round(beat_density, 2),
            emotion_curve=emotion_curve,
            conflict_curve=conflict_curve,
            pace_variance=round(pace_variance, 2),
            hook_strength=round(hook_strength, 2),
            score=score,
            issues=issues,
            suggestions=suggestions,
        )

    def _detect_beats(self, text: str) -> List[Beat]:
        """检测所有爽点"""
        beats = []
        lines = text.split('\n')
        char_pos = 0

        for line_num, line in enumerate(lines, 1):
            for beat_type, patterns in self._compiled_patterns.items():
                for pattern, weight in patterns:
                    for match in pattern.finditer(line):
                        intensity = weight * (1.0 + len(match.group()) / 20)
                        intensity = min(intensity, 1.0)

                        beats.append(Beat(
                            type=beat_type,
                            position=char_pos + match.start(),
                            intensity=round(intensity, 2),
                            text_snippet=match.group(),
                            line_number=line_num,
                        ))

            char_pos += len(line) + 1

        beats.sort(key=lambda b: b.position)

        filtered = []
        last_positions: Dict[BeatType, int] = {}
        min_distance = 50

        for beat in beats:
            last_pos = last_positions.get(beat.type, -min_distance - 1)
            if beat.position - last_pos >= min_distance:
                filtered.append(beat)
                last_positions[beat.type] = beat.position

        return filtered

    def _compute_emotion_curve(self, text: str) -> List[float]:
        """计算情绪曲线(10段采样)"""
        segment_size = max(len(text) // 10, 1)
        curve = []

        for i in range(10):
            start = i * segment_size
            end = start + segment_size if i < 9 else len(text)
            segment = text[start:end]

            score = 0.0
            total_weight = 0.0

            for category, keywords in EMOTION_KEYWORDS.items():
                if "positive" in category:
                    if "high" in category:
                        weight = 1.0
                    elif "mid" in category:
                        weight = 0.6
                    else:
                        weight = 0.3
                else:
                    if "high" in category:
                        weight = -1.0
                    elif "mid" in category:
                        weight = -0.6
                    else:
                        weight = -0.3

                for kw in keywords:
                    count = segment.count(kw)
                    if count > 0:
                        score += weight * count
                        total_weight += abs(weight) * count

            if total_weight > 0:
                score = score / total_weight
            score = (score + 1) / 2
            score = max(0.0, min(1.0, score))
            curve.append(round(score, 2))

        return curve

    def _compute_conflict_curve(self, beats: List[Beat],
                                 char_count: int) -> List[float]:
        """计算冲突曲线"""
        if char_count == 0:
            return [0.0] * 10

        segment_size = char_count / 10
        curve = []

        for i in range(10):
            start = i * segment_size
            end = start + segment_size

            segment_beats = [
                b for b in beats
                if start <= b.position < end
                and b.type in (BeatType.CONFLICT, BeatType.CLIMAX, BeatType.FACE_SLAP)
            ]

            if segment_beats:
                intensity = sum(b.intensity for b in segment_beats) / len(segment_beats)
            else:
                intensity = 0.0

            curve.append(round(intensity, 2))

        return curve

    def _compute_pace_variance(self, text: str) -> float:
        """计算节奏变化度(句长方差)"""
        sentences = re.split(r'[。！？\n]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        if len(sentences) < 2:
            return 0.0

        lengths = [len(s) for s in sentences]
        mean_len = sum(lengths) / len(lengths)
        variance = sum((l - mean_len) ** 2 for l in lengths) / len(lengths)

        normalized = min(variance / 100, 1.0)
        return normalized

    def _evaluate_hook(self, text: str, beats: List[Beat]) -> float:
        """评估章末钩子强度"""
        last_20_percent = text[int(len(text) * 0.8):]

        hook_beats = [b for b in beats if b.type == BeatType.HOOK
                      and b.position >= len(text) * 0.8]

        suspense_beats = [b for b in beats if b.type == BeatType.SUSPENSE
                          and b.position >= len(text) * 0.7]

        score = 0.0

        if hook_beats:
            score += sum(b.intensity for b in hook_beats) / len(hook_beats) * 0.6

        if suspense_beats:
            score += sum(b.intensity for b in suspense_beats) / len(suspense_beats) * 0.4

        question_marks = last_20_percent.count('？') + last_20_percent.count('?')
        score += min(question_marks * 0.1, 0.2)

        ellipsis_count = last_20_percent.count('…') + last_20_percent.count('...')
        score += min(ellipsis_count * 0.05, 0.1)

        return min(score, 1.0)

    def _diagnose(self, beats: List[Beat], beat_density: float,
                  emotion_curve: List[float], conflict_curve: List[float],
                  pace_variance: float, hook_strength: float,
                  char_count: int, is_opening: bool,
                  chapter_num: int) -> Tuple[List[str], List[str]]:
        """诊断节奏问题"""
        issues = []
        suggestions = []

        if beat_density < 1.0:
            issues.append(f"爽点密度过低({beat_density}/千字)，读者容易失去兴趣")
            suggestions.append("建议每2000字至少安排2-3个爽点(打脸/升级/收获)")
        elif beat_density > 5.0:
            issues.append(f"爽点密度过高({beat_density}/千字)，可能导致审美疲劳")
            suggestions.append("建议适当加入舒缓段落，让读者有喘息空间")

        beat_types = Counter(b.type for b in beats)
        if BeatType.FACE_SLAP not in beat_types and BeatType.POWER_UP not in beat_types:
            issues.append("缺少核心爽点(打脸/升级)，章节缺乏阅读快感")
            suggestions.append("建议加入至少1处打脸或升级情节")

        if BeatType.HOOK not in beat_types:
            issues.append("章末缺少钩子，读者没有追读动力")
            suggestions.append("章末应设置悬念或预告下章精彩内容")

        if BeatType.RELIEF not in beat_types and len(beats) > 5:
            suggestions.append("建议加入1-2处舒缓段落，形成张弛有度的节奏")

        if emotion_curve:
            emotion_range = max(emotion_curve) - min(emotion_curve)
            if emotion_range < 0.3:
                issues.append(f"情绪起伏不足(振幅{emotion_range:.2f})，章节平淡")
                suggestions.append("情绪应有明显起伏：平静→紧张→爆发→舒缓")

        if conflict_curve:
            max_conflict = max(conflict_curve)
            if max_conflict < 0.3 and len(beats) > 3:
                issues.append("冲突强度不足，缺乏张力")
                suggestions.append("增加对抗性情节，提升冲突烈度")

        if pace_variance < 0.1:
            issues.append(f"句长过于均匀(方差{pace_variance:.2f})，AI痕迹明显")
            suggestions.append("长短句交替：短句制造紧张，长句铺陈氛围")

        if hook_strength < 0.3:
            issues.append(f"章末钩子强度不足({hook_strength:.2f})")
            suggestions.append("章末应卡在关键转折点：危机降临/真相将揭/强敌出现")

        if is_opening and chapter_num <= 3:
            if beat_density < 2.0:
                issues.append("⚠️ 黄金三章法则：开篇爽点密度不足，读者可能弃书")
                suggestions.append("前三章必须密集输出：第1章建立冲突，第2章展示金手指，第3章首次打脸")

            if BeatType.CONFLICT not in beat_types:
                issues.append("⚠️ 黄金三章法则：开篇缺少冲突，无法建立读者期待")
                suggestions.append("第1章必须在500字内建立核心冲突")

        if char_count < 1500:
            issues.append(f"章节过短({char_count}字)，信息量不足")
            suggestions.append("建议每章2000-4000字，确保情节完整")

        return issues, suggestions

    def _compute_score(self, beat_density: float, emotion_curve: List[float],
                       conflict_curve: List[float], pace_variance: float,
                       hook_strength: float, issue_count: int) -> int:
        """计算综合评分"""
        score = 50.0

        if 1.5 <= beat_density <= 4.0:
            score += 15
        elif 1.0 <= beat_density <= 5.0:
            score += 8

        if emotion_curve:
            emotion_range = max(emotion_curve) - min(emotion_curve)
            if emotion_range > 0.5:
                score += 10
            elif emotion_range > 0.3:
                score += 5

        if conflict_curve:
            max_conflict = max(conflict_curve)
            if max_conflict > 0.6:
                score += 10
            elif max_conflict > 0.4:
                score += 5

        if pace_variance > 0.2:
            score += 8
        elif pace_variance > 0.1:
            score += 4

        if hook_strength > 0.6:
            score += 7
        elif hook_strength > 0.3:
            score += 3

        score -= issue_count * 5

        return max(0, min(100, int(score)))

    def compare_chapters(self, chapters: Dict[int, str]) -> Dict[int, RhythmProfile]:
        """批量分析多章节奏"""
        results = {}
        for num, text in chapters.items():
            results[num] = self.analyze(text, num)
        return results

    def get_rhythm_report(self, profile: RhythmProfile) -> str:
        """生成可读的节奏报告"""
        lines = []
        lines.append("=" * 50)
        lines.append(f"📊 节奏分析报告 (评分: {profile.score}/100)")
        lines.append("=" * 50)
        lines.append(f"  爽点总数: {profile.total_beats}")
        lines.append(f"  爽点密度: {profile.beat_density}/千字")
        lines.append(f"  节奏变化度: {profile.pace_variance}")
        lines.append(f"  章末钩子: {profile.hook_strength}")

        if profile.emotion_curve:
            curve_viz = "".join(
                "█" if v > 0.7 else "▓" if v > 0.5 else "▒" if v > 0.3 else "░"
                for v in profile.emotion_curve
            )
            lines.append(f"  情绪曲线: {curve_viz}")

        if profile.issues:
            lines.append(f"\n⚠️ 发现 {len(profile.issues)} 个问题:")
            for issue in profile.issues:
                lines.append(f"  ❌ {issue}")

        if profile.suggestions:
            lines.append(f"\n💡 优化建议:")
            for sug in profile.suggestions:
                lines.append(f"  ✅ {sug}")

        return "\n".join(lines)
