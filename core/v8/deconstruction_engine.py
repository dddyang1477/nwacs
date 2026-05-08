#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI拆书/爆款分析引擎 (Deconstruction Engine)

对标 星月写作 的"AI拆书"功能。
深度解析爆款网文的结构、节奏、套路，提取可复用的创作模式。
支持雪花写作法六阶段引导，帮助新手建立系统创作思维。

核心能力:
- 爆款拆解: 分析章节结构、爽点分布、节奏模式
- 套路提取: 识别并归类常见网文套路
- 结构模板: 基于雪花写作法的六阶段创作引导
- 对标分析: 将当前作品与爆款进行结构对比
- 黄金模板库: 内置各题材经典结构模板
"""

import re
import json
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from collections import Counter, defaultdict


class SnowflakeStage(Enum):
    IDEA = 1           # 一句话概括
    EXPAND = 2         # 扩展为一段话
    CHARACTERS = 3     # 角色设计
    SYNOPSIS = 4       # 情节大纲
    CHAPTERS = 5       # 章节规划
    DRAFT = 6          # 初稿写作


@dataclass
class ChapterStructure:
    chapter_num: int
    word_count: int
    opening_type: str          # 开篇类型: 冲突/悬念/日常/倒叙
    main_conflict: str         # 主要冲突
    beat_types: List[str]      # 爽点类型列表
    climax_position: float     # 高潮位置(0-1)
    ending_type: str           # 结尾类型: 钩子/收束/预告
    pov_character: str         # 视角角色
    key_events: List[str]      # 关键事件


@dataclass
class DeconstructionResult:
    title: str
    total_chapters: int
    total_words: int
    genre: str
    chapters: List[ChapterStructure]
    beat_distribution: Dict[str, int]     # 爽点类型分布
    pace_pattern: List[float]             # 节奏模式
    hook_pattern: List[float]             # 钩子模式
    character_arcs: Dict[str, List[str]]  # 角色弧光
    reusable_patterns: List[str]          # 可复用模式
    structure_score: int                  # 结构评分


GENRE_TEMPLATES: Dict[str, Dict] = {
    "玄幻": {
        "name": "玄幻经典结构",
        "stages": [
            ("废柴开局", "主角处于底层，遭受欺压，展示困境"),
            ("金手指觉醒", "获得特殊能力/宝物/传承，命运转折"),
            ("初露锋芒", "首次展示实力，小范围打脸"),
            ("势力崛起", "建立自己的势力/团队，扩大影响力"),
            ("大敌当前", "遭遇强大对手，面临生死危机"),
            ("绝境突破", "在绝境中突破，实力飞跃"),
            ("名动天下", "一战成名，进入更高层次的世界"),
        ],
        "beat_ratio": {"face_slap": 0.25, "power_up": 0.25, "conflict": 0.20,
                       "harvest": 0.15, "reveal": 0.10, "emotional": 0.05},
        "chapter_length": (2500, 4000),
        "hook_frequency": 0.8,
    },
    "都市": {
        "name": "都市爽文结构",
        "stages": [
            ("身份揭示", "隐藏身份/能力被逐步揭示"),
            ("打脸装逼", "用实力碾压看不起自己的人"),
            ("势力扩张", "商业/势力版图不断扩大"),
            ("红颜知己", "多位女性角色依次登场"),
            ("强敌来袭", "更强大的对手出现"),
            ("终极对决", "与最终BOSS的决战"),
        ],
        "beat_ratio": {"face_slap": 0.35, "harvest": 0.20, "emotional": 0.15,
                       "power_up": 0.10, "conflict": 0.10, "reveal": 0.10},
        "chapter_length": (2000, 3500),
        "hook_frequency": 0.85,
    },
    "言情": {
        "name": "言情经典结构",
        "stages": [
            ("初遇", "男女主首次相遇，建立第一印象"),
            ("冲突", "因性格/立场差异产生矛盾"),
            ("靠近", "被迫相处，逐渐了解对方"),
            ("心动", "一方或双方产生好感"),
            ("误会/分离", "因误会或外力被迫分开"),
            ("追妻/追夫", "一方主动挽回"),
            ("和解", "误会解除，感情升温"),
            ("圆满", "修成正果或留有遗憾"),
        ],
        "beat_ratio": {"emotional": 0.35, "conflict": 0.20, "reveal": 0.15,
                       "face_slap": 0.10, "harvest": 0.10, "power_up": 0.10},
        "chapter_length": (2000, 3500),
        "hook_frequency": 0.7,
    },
    "悬疑": {
        "name": "悬疑经典结构",
        "stages": [
            ("案件发生", "核心事件/案件发生"),
            ("初步调查", "主角开始调查，收集线索"),
            ("误导", "出现误导性线索/嫌疑人"),
            ("深入", "发现更深层的秘密"),
            ("反转", "重大反转，真相开始浮现"),
            ("危机", "主角陷入危险"),
            ("真相", "揭示最终真相"),
        ],
        "beat_ratio": {"reveal": 0.30, "suspense": 0.25, "conflict": 0.20,
                       "climax": 0.15, "emotional": 0.10},
        "chapter_length": (2500, 4000),
        "hook_frequency": 0.9,
    },
    "科幻": {
        "name": "科幻经典结构",
        "stages": [
            ("世界观建立", "展示未来/异世界设定"),
            ("技术/能力展示", "展示核心科技或特殊能力"),
            ("危机浮现", "技术/能力带来的问题浮现"),
            ("探索真相", "深入探索背后的真相"),
            ("伦理困境", "面临技术伦理的选择"),
            ("终极抉择", "在多个方案中做出选择"),
            ("新平衡", "建立新的秩序或平衡"),
        ],
        "beat_ratio": {"reveal": 0.25, "conflict": 0.20, "power_up": 0.15,
                       "climax": 0.15, "suspense": 0.15, "emotional": 0.10},
        "chapter_length": (2500, 4500),
        "hook_frequency": 0.75,
    },
}


class DeconstructionEngine:
    """AI拆书/爆款分析引擎"""

    def __init__(self):
        self.templates = GENRE_TEMPLATES
        self._analysis_cache: Dict[str, DeconstructionResult] = {}

    def deconstruct(self, title: str, chapters: Dict[int, str],
                    genre: str = "玄幻") -> DeconstructionResult:
        """
        拆解一部完整作品

        Args:
            title: 作品标题
            chapters: {章节号: 章节文本}
            genre: 题材类型

        Returns:
            DeconstructionResult: 拆解结果
        """
        chapter_structures = []
        total_words = 0

        for num in sorted(chapters.keys()):
            text = chapters[num]
            total_words += len(text)
            structure = self._analyze_chapter(text, num)
            chapter_structures.append(structure)

        beat_dist = defaultdict(int)
        for ch in chapter_structures:
            for bt in ch.beat_types:
                beat_dist[bt] += 1

        pace_pattern = self._extract_pace_pattern(chapter_structures)
        hook_pattern = self._extract_hook_pattern(chapter_structures)
        character_arcs = self._extract_character_arcs(chapters)
        reusable = self._extract_reusable_patterns(chapter_structures, genre)
        score = self._evaluate_structure(chapter_structures, genre)

        result = DeconstructionResult(
            title=title,
            total_chapters=len(chapters),
            total_words=total_words,
            genre=genre,
            chapters=chapter_structures,
            beat_distribution=dict(beat_dist),
            pace_pattern=pace_pattern,
            hook_pattern=hook_pattern,
            character_arcs=character_arcs,
            reusable_patterns=reusable,
            structure_score=score,
        )

        self._analysis_cache[title] = result
        return result

    def _analyze_chapter(self, text: str, num: int) -> ChapterStructure:
        """分析单章结构"""
        opening = self._detect_opening_type(text)
        conflict = self._detect_main_conflict(text)
        beats = self._detect_beat_types(text)
        climax_pos = self._detect_climax_position(text)
        ending = self._detect_ending_type(text)
        pov = self._detect_pov(text)
        events = self._extract_key_events(text)

        return ChapterStructure(
            chapter_num=num,
            word_count=len(text),
            opening_type=opening,
            main_conflict=conflict,
            beat_types=beats,
            climax_position=climax_pos,
            ending_type=ending,
            pov_character=pov,
            key_events=events,
        )

    def _detect_opening_type(self, text: str) -> str:
        """检测开篇类型"""
        first_200 = text[:200]

        if re.search(r'杀|战|打|冲突|对峙|剑拔弩张', first_200):
            return "冲突"
        if re.search(r'难道|莫非|诡异|奇怪|不对劲|秘密', first_200):
            return "悬念"
        if re.search(r'昨天|记得|曾经|那年|从前|回忆', first_200):
            return "倒叙"
        return "日常"

    def _detect_main_conflict(self, text: str) -> str:
        """检测主要冲突"""
        patterns = [
            (r'生死|命悬一线|绝境|必死', "生死危机"),
            (r'追杀|围剿|围攻|包围', "被追杀"),
            (r'比试|对决|挑战|擂台', "对决挑战"),
            (r'阴谋|陷阱|圈套|算计', "阴谋陷阱"),
            (r'争夺|抢夺|竞拍|争抢', "资源争夺"),
            (r'误会|误解|偏见|歧视', "误会偏见"),
        ]

        for pattern, conflict_type in patterns:
            if re.search(pattern, text):
                return conflict_type

        return "其他冲突"

    def _detect_beat_types(self, text: str) -> List[str]:
        """检测爽点类型"""
        beat_patterns = {
            "face_slap": r'打脸|反转|震惊|目瞪口呆|不敢置信|啪啪',
            "power_up": r'突破|晋级|升级|觉醒|蜕变|涅槃',
            "harvest": r'获得|得到|收获|宝物|神器|秘籍',
            "reveal": r'原来|真相|秘密|竟然是|没想到',
            "emotional": r'泪流|哭泣|感动|温暖|心痛|愤怒',
            "conflict": r'战斗|厮杀|激战|对决|杀意',
            "suspense": r'难道|莫非|诡异|奇怪|不对劲',
            "climax": r'巅峰|极致|最强|碾压|毁天灭地',
        }

        found = []
        for beat_type, pattern in beat_patterns.items():
            if re.search(pattern, text):
                found.append(beat_type)

        return found if found else ["transition"]

    def _detect_climax_position(self, text: str) -> float:
        """检测高潮位置(0-1)"""
        climax_keywords = r'巅峰|极致|最强|碾压|毁天灭地|最后一击|绝杀'
        matches = list(re.finditer(climax_keywords, text))

        if not matches:
            return 0.5

        positions = [m.start() / len(text) for m in matches]
        return sum(positions) / len(positions)

    def _detect_ending_type(self, text: str) -> str:
        """检测结尾类型"""
        last_20_percent = text[int(len(text) * 0.8):]

        if re.search(r'欲知后事|且听下回|未完待续|下章', last_20_percent):
            return "预告"
        if re.search(r'突然|忽然|猛地|就在这时|正在此时', last_20_percent):
            return "钩子"
        if re.search(r'？|…|——', last_20_percent):
            return "悬念"
        return "收束"

    def _detect_pov(self, text: str) -> str:
        """检测视角角色"""
        first_person = len(re.findall(r'我[^们]', text[:500]))
        third_person_he = len(re.findall(r'他[^们]', text[:500]))
        third_person_she = len(re.findall(r'她[^们]', text[:500]))

        if first_person > third_person_he and first_person > third_person_she:
            return "第一人称"
        if third_person_he > third_person_she:
            return "男主视角"
        return "女主视角"

    def _extract_key_events(self, text: str) -> List[str]:
        """提取关键事件"""
        events = []

        event_patterns = [
            (r'(突破|晋级|升级)了?[^。！？\n]{0,30}', "升级事件"),
            (r'(获得|得到|收获)了?[^。！？\n]{0,30}', "获得事件"),
            (r'(杀死|击败|打败|战胜)了?[^。！？\n]{0,30}', "战斗事件"),
            (r'(发现|得知|知道)了?[^。！？\n]{0,30}', "发现事件"),
        ]

        for pattern, event_type in event_patterns:
            for match in re.finditer(pattern, text):
                events.append(f"{event_type}: {match.group()[:50]}")

        return events[:5]

    def _extract_pace_pattern(self, chapters: List[ChapterStructure]) -> List[float]:
        """提取节奏模式"""
        if not chapters:
            return []

        pattern = []
        for ch in chapters:
            pace = len(ch.beat_types) / max(ch.word_count / 1000, 1)
            pattern.append(round(min(pace, 5.0), 2))

        return pattern

    def _extract_hook_pattern(self, chapters: List[ChapterStructure]) -> List[float]:
        """提取钩子模式"""
        pattern = []
        for ch in chapters:
            if ch.ending_type in ("钩子", "悬念", "预告"):
                pattern.append(1.0)
            else:
                pattern.append(0.0)

        return pattern

    def _extract_character_arcs(self, chapters: Dict[int, str]) -> Dict[str, List[str]]:
        """提取角色弧光"""
        arcs = defaultdict(list)

        for num in sorted(chapters.keys()):
            text = chapters[num]
            names = re.findall(r'(?:[李王张刘陈杨赵黄周吴][\u4e00-\u9fa5]{1,2})', text)
            for name in set(names[:5]):
                arcs[name].append(f"第{num}章出场")

        return dict(arcs)

    def _extract_reusable_patterns(self, chapters: List[ChapterStructure],
                                    genre: str) -> List[str]:
        """提取可复用的创作模式"""
        patterns = []

        openings = Counter(ch.opening_type for ch in chapters)
        if openings:
            top_opening = openings.most_common(1)[0]
            patterns.append(f"开篇偏好: {top_opening[0]}型({top_opening[1]}/{len(chapters)}章)")

        endings = Counter(ch.ending_type for ch in chapters)
        hook_rate = sum(1 for e, t in endings.items() if t in ("钩子", "悬念", "预告"))
        patterns.append(f"章末钩子率: {hook_rate}/{len(chapters)} ({hook_rate/len(chapters)*100:.0f}%)")

        all_beats = []
        for ch in chapters:
            all_beats.extend(ch.beat_types)
        beat_counter = Counter(all_beats)
        top_beats = beat_counter.most_common(3)
        patterns.append(f"核心爽点: {', '.join(f'{b}({c}次)' for b, c in top_beats)}")

        avg_words = sum(ch.word_count for ch in chapters) / len(chapters) if chapters else 0
        patterns.append(f"平均章长: {avg_words:.0f}字")

        template = self.templates.get(genre, {})
        if template:
            patterns.append(f"对标模板: {template.get('name', genre)}")

        return patterns

    def _evaluate_structure(self, chapters: List[ChapterStructure],
                            genre: str) -> int:
        """评估结构质量"""
        if not chapters:
            return 0

        score = 50

        hook_rate = sum(1 for ch in chapters
                        if ch.ending_type in ("钩子", "悬念", "预告")) / len(chapters)
        score += int(hook_rate * 20)

        beat_variety = len(set(
            bt for ch in chapters for bt in ch.beat_types
        ))
        score += min(beat_variety * 3, 15)

        opening_variety = len(set(ch.opening_type for ch in chapters))
        score += min(opening_variety * 3, 10)

        template = self.templates.get(genre, {})
        if template:
            ideal_beat_ratio = template.get("beat_ratio", {})
            actual_beats = Counter(
                bt for ch in chapters for bt in ch.beat_types
            )
            total = sum(actual_beats.values()) or 1
            for beat_type, ideal_ratio in ideal_beat_ratio.items():
                actual_ratio = actual_beats.get(beat_type, 0) / total
                diff = abs(actual_ratio - ideal_ratio)
                if diff < 0.1:
                    score += 2

        return min(100, score)

    def get_snowflake_guide(self, stage: SnowflakeStage,
                            context: Dict = None) -> str:
        """
        雪花写作法引导

        基于雪花写作法(Snowflake Method)的六阶段创作引导，
        帮助新手从一句话逐步构建完整小说。
        """
        context = context or {}

        guides = {
            SnowflakeStage.IDEA: """【阶段1: 一句话概括】

用一句话概括你的故事核心。这句话应包含:
1. 主角是谁
2. 主角想要什么
3. 阻碍是什么
4. 故事的独特卖点

格式示例:
"一个被家族抛弃的废柴少年[主角]，意外获得上古传承[转折]，
在强者为尊的世界中[背景]一步步踏上巅峰[目标]，
却发现这一切背后隐藏着惊天阴谋[悬念]"

请写出你的一句话概括:""",

            SnowflakeStage.EXPAND: """【阶段2: 扩展为一段话】

将一句话扩展为5句话的段落:
第1句: 故事背景和开场状态
第2句: 第一个重大事件/转折
第3句: 故事中段的冲突升级
第4句: 高潮/最大危机
第5句: 结局/新的开始

请基于你的一句话概括，写出这段扩展:""",

            SnowflakeStage.CHARACTERS: """【阶段3: 角色设计】

为每个主要角色设计:
- 姓名与身份
- 核心目标(想要什么)
- 核心动机(为什么想要)
- 性格特点(3个形容词)
- 致命缺陷/弱点
- 成长弧光(从___变成___)
- 与其他角色的关系

至少设计: 主角、反派、导师/伙伴、情感对象""",

            SnowflakeStage.SYNOPSIS: """【阶段4: 情节大纲】

将扩展段落拆分为完整的情节大纲:
- 三幕结构: 建置(25%) → 对抗(50%) → 结局(25%)
- 每幕3-5个关键情节点
- 标注每个情节点的爽点类型
- 确保因果链完整: 因为A所以B因此C

格式:
第一幕: 建置
  1. [情节点] → [爽点类型]
  2. ...""",

            SnowflakeStage.CHAPTERS: """【阶段5: 章节规划】

将情节大纲拆分为具体章节:
- 每章2000-4000字
- 每章至少1个核心冲突
- 每章至少1个爽点
- 章末必须有钩子
- 标注每章的POV角色

格式:
第1章: [章节标题]
  核心冲突: ...
  爽点类型: ...
  章末钩子: ...
  字数预估: ...""",

            SnowflakeStage.DRAFT: """【阶段6: 初稿写作】

开始写作初稿，遵循以下原则:
1. 先完成再完美 — 不要边写边改
2. 保持节奏 — 每天固定字数目标
3. 对话先行 — 先写对话再补描写
4. 卡文跳过 — 写不下去就跳，回头再补
5. 章末必钩 — 每章结尾留悬念

写作时注意:
- 用动作替代形容词
- 对话要符合角色性格
- 感官细节至少2种
- 长短句交替""",
        }

        return guides.get(stage, "未知阶段")

    def compare_with_template(self, chapters: Dict[int, str],
                               genre: str) -> Dict[str, Any]:
        """与题材模板进行对比分析"""
        template = self.templates.get(genre)
        if not template:
            return {"error": f"未找到题材模板: {genre}"}

        result = self.deconstruct("当前作品", chapters, genre)

        ideal_stages = len(template["stages"])
        actual_chapters = len(chapters)

        comparison = {
            "template_name": template["name"],
            "ideal_stages": ideal_stages,
            "actual_chapters": actual_chapters,
            "coverage": f"{min(actual_chapters / ideal_stages * 100, 100):.0f}%",
            "ideal_chapter_length": template["chapter_length"],
            "actual_avg_length": result.total_words // max(actual_chapters, 1),
            "ideal_hook_rate": template["hook_frequency"],
            "actual_hook_rate": sum(result.hook_pattern) / max(len(result.hook_pattern), 1),
            "beat_alignment": {},
        }

        ideal_beats = template["beat_ratio"]
        actual_beats = result.beat_distribution
        total_actual = sum(actual_beats.values()) or 1

        for beat_type, ideal_ratio in ideal_beats.items():
            actual_ratio = actual_beats.get(beat_type, 0) / total_actual
            comparison["beat_alignment"][beat_type] = {
                "ideal": f"{ideal_ratio*100:.0f}%",
                "actual": f"{actual_ratio*100:.0f}%",
                "status": "✅" if abs(actual_ratio - ideal_ratio) < 0.1 else "⚠️",
            }

        return comparison

    def get_genre_templates(self) -> Dict[str, str]:
        """获取所有可用题材模板"""
        return {genre: info["name"] for genre, info in self.templates.items()}
