#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 长篇小说记忆一致性验证系统 - NovelMemoryManager

专为100万字以上长篇小说设计，核心能力：

1. 写作风格指纹 (Style Fingerprint)
   - 句长分布 / 对话占比 / 描写占比 / 高频词模式
   - 章节间风格偏移检测 → 防止AI写作风格漂移
   - 情感曲线追踪

2. 剧情一致性验证 (Plot Consistency)
   - 时间线校验 → 防止时间矛盾
   - 因果链追踪 → 事件前后逻辑自洽
   - 地点/势力一致性 → 防止设定冲突
   - 实力体系校验 → 防止战力崩坏

3. 伏笔管理系统 (Foreshadowing Tracker)
   - 伏笔注册(埋设章节+预期回收章节+类型)
   - 未回收伏笔告警
   - 伏笔回收率统计
   - 超期未回收提醒

4. 人物一致性验证 (Character Consistency)
   - 人物档案(外貌/性格/能力/口头禅)
   - 人物关系图谱
   - 对话风格指纹
   - 跨章节人物行为一致性检查

设计原则：
- 纯本地计算，零API依赖
- 支持增量更新，百万字级别性能
- JSON持久化，断点续写
"""

import json
import os
import re
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from collections import Counter, defaultdict
from enum import Enum


class ForeshadowStatus(Enum):
    PLANTED = "已埋设"
    HINTED = "已暗示"
    PARTIALLY_PAID = "部分回收"
    FULLY_PAID = "已回收"
    ABANDONED = "已废弃"


class ConsistencyLevel(Enum):
    CONSISTENT = "一致"
    MINOR_DRIFT = "轻微偏移"
    NOTICEABLE_DRIFT = "明显偏移"
    MAJOR_CONFLICT = "严重冲突"


class EmotionalState(Enum):
    """情感状态"""
    JOY = ("喜", 1.0)
    ANGER = ("怒", 0.5)
    SORROW = ("哀", 0.0)
    SURPRISE = ("惊", 0.7)
    FEAR = ("惧", 0.3)
    CALM = ("静", 0.5)
    TENSION = ("紧张", 0.4)
    TOUCHING = ("感动", 0.8)

    def __init__(self, label: str, baseline: float):
        self.label = label
        self.baseline = baseline


class PacingType(Enum):
    """节奏类型"""
    FAST = "快节奏"
    MODERATE = "中节奏"
    SLOW = "慢节奏"
    CLIMAX = "高潮"


@dataclass
class EmotionalArcPoint:
    """情感弧线节点"""
    chapter: int
    dominant_emotion: str
    emotion_scores: Dict[str, float] = field(default_factory=dict)
    intensity: float = 0.0
    transition_from_prev: str = ""


@dataclass
class PacingProfile:
    """节奏曲线"""
    chapter: int
    pacing_type: PacingType = PacingType.MODERATE
    action_density: float = 0.0
    dialogue_density: float = 0.0
    description_density: float = 0.0
    paragraph_variation: float = 0.0
    climax_proximity: float = 0.0


@dataclass
class DialogueFingerprint:
    """对话风格指纹"""
    character_name: str
    avg_sentence_length: float = 0.0
    exclamation_ratio: float = 0.0
    question_ratio: float = 0.0
    catchphrase_usage: Dict[str, int] = field(default_factory=dict)
    formality_level: float = 0.5
    unique_words: Set[str] = field(default_factory=set)


@dataclass
class WorldRule:
    """世界观规则"""
    rule_id: str
    category: str
    rule: str
    established_chapter: int
    exceptions: List[str] = field(default_factory=list)
    last_verified_chapter: int = 0


@dataclass
class StyleFingerprint:
    """写作风格指纹"""
    chapter: int
    avg_sentence_length: float = 0.0
    sentence_length_std: float = 0.0
    dialogue_ratio: float = 0.0
    description_ratio: float = 0.0
    action_ratio: float = 0.0
    inner_thought_ratio: float = 0.0
    paragraph_count: int = 0
    avg_paragraph_length: float = 0.0
    top_words: List[Tuple[str, int]] = field(default_factory=list)
    emotional_curve: List[float] = field(default_factory=list)
    unique_word_count: int = 0
    total_word_count: int = 0
    computed_at: str = ""


@dataclass
class Foreshadowing:
    """伏笔记录"""
    fs_id: str
    description: str
    planted_chapter: int
    expected_payoff_chapter: int
    actual_payoff_chapter: Optional[int] = None
    status: ForeshadowStatus = ForeshadowStatus.PLANTED
    type: str = "plot"
    importance: int = 5
    related_characters: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    created_at: str = ""
    resolved_at: str = ""


@dataclass
class CharacterProfile:
    """人物档案"""
    name: str
    aliases: List[str] = field(default_factory=list)
    role: str = "配角"
    gender: str = "男"
    age: int = 0
    appearance: Dict[str, str] = field(default_factory=dict)
    personality: List[str] = field(default_factory=list)
    abilities: List[Dict[str, Any]] = field(default_factory=list)
    catchphrases: List[str] = field(default_factory=list)
    speech_style: Dict[str, Any] = field(default_factory=dict)
    relationships: Dict[str, str] = field(default_factory=dict)
    first_appearance_chapter: int = 0
    last_appearance_chapter: int = 0
    status: str = "存活"
    notes: str = ""


@dataclass
class ConsistencyIssue:
    """一致性问题"""
    issue_id: str
    category: str
    severity: ConsistencyLevel
    description: str
    chapter: int
    related_chapters: List[int] = field(default_factory=list)
    suggestion: str = ""
    resolved: bool = False


@dataclass
class RetrievalResult:
    """智能检索结果"""
    result_id: str
    content_type: str
    chapter: int
    content: str
    relevance_score: float = 0.0
    matched_keywords: List[str] = field(default_factory=list)
    context_before: str = ""
    context_after: str = ""
    source_section: str = ""


@dataclass
class CausalLink:
    """因果链节点"""
    link_id: str
    cause_event: str
    effect_event: str
    cause_chapter: int
    effect_chapter: int
    confidence: float = 0.5
    evidence: List[str] = field(default_factory=list)
    link_type: str = "direct"


@dataclass
class CharacterArcPoint:
    """角色弧线节点"""
    character_name: str
    chapter: int
    arc_stage: str = "exposition"
    trait_changes: Dict[str, Any] = field(default_factory=dict)
    key_events: List[str] = field(default_factory=list)
    growth_score: float = 0.0


@dataclass
class MemorySnapshot:
    """记忆快照（用于压缩）"""
    snapshot_id: str
    chapter_range: Tuple[int, int]
    summary: str = ""
    key_characters: List[str] = field(default_factory=list)
    key_events: List[str] = field(default_factory=list)
    key_settings: List[str] = field(default_factory=list)
    unresolved_threads: List[str] = field(default_factory=list)
    word_count: int = 0
    compression_ratio: float = 0.0
    created_at: str = ""


@dataclass
class AutoCheckRule:
    """自动检查规则"""
    rule_id: str
    name: str
    category: str
    check_function: str
    severity_threshold: ConsistencyLevel = ConsistencyLevel.MINOR_DRIFT
    enabled: bool = True
    schedule: str = "on_chapter"
    last_run_chapter: int = 0
    total_issues_found: int = 0


class NovelMemoryManager:
    """长篇小说记忆一致性验证管理器"""

    def __init__(self, storage_dir: str = None, novel_title: str = "未命名作品"):
        if storage_dir is None:
            storage_dir = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "novel_memory"
            )
        self.storage_dir = storage_dir
        self.novel_title = novel_title
        os.makedirs(storage_dir, exist_ok=True)

        self.characters: Dict[str, CharacterProfile] = {}
        self.foreshadowings: Dict[str, Foreshadowing] = {}
        self.style_fingerprints: Dict[int, StyleFingerprint] = {}
        self.issues: List[ConsistencyIssue] = []
        self.plot_events: List[Dict] = []
        self.world_settings: Dict[str, Any] = {}
        self.timeline: Dict[int, Dict] = {}

        self.fs_counter = 0
        self.issue_counter = 0
        self.total_words_processed = 0
        self.conversations: List[Dict] = []

        self.emotional_arc: List[EmotionalArcPoint] = []
        self.pacing_profiles: Dict[int, PacingProfile] = {}
        self.dialogue_fingerprints: Dict[str, DialogueFingerprint] = {}
        self.world_rules: Dict[str, WorldRule] = {}
        self.chapter_quality_scores: Dict[int, Dict] = {}
        self.conflict_density: Dict[int, float] = {}
        self.rule_counter = 0

        self.causal_links: Dict[str, CausalLink] = {}
        self.character_arcs: Dict[str, List[CharacterArcPoint]] = {}
        self.memory_snapshots: Dict[str, MemorySnapshot] = {}
        self.auto_check_rules: Dict[str, AutoCheckRule] = {}
        self.chapter_texts: Dict[int, str] = {}
        self.link_counter = 0
        self.snapshot_counter = 0
        self.retrieval_counter = 0

        self._init_auto_check_rules()
        self._load_all()

    # ================================================================
    # 流水线兼容方法
    # ================================================================

    def save_plot_point(self, chapter: int, title: str,
                        summary: str, point_type: str = "general"):
        """保存剧情节点（流水线兼容接口）"""
        self.record_plot_event(
            chapter=chapter,
            event=f"{title}: {summary}",
            event_type=point_type,
        )

    def save_conversation(self, role: str, content: str):
        """保存对话/系统消息（流水线兼容接口）"""
        self.conversations.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
        })

    def build_context(self, categories: List[str] = None,
                      max_chars: int = 3000) -> str:
        """构建上下文文本（流水线兼容接口）"""
        parts = []

        if categories is None or "character" in categories:
            if self.characters:
                char_lines = ["【角色信息】"]
                for name, profile in list(self.characters.items())[:10]:
                    char_lines.append(
                        f"  {name}({profile.role}): "
                        f"性格={'/'.join(profile.personality[:3]) if profile.personality else '未知'}, "
                        f"首登场第{profile.first_appearance_chapter}章"
                    )
                parts.append("\n".join(char_lines))

        if categories is None or "plot" in categories:
            if self.plot_events:
                plot_lines = ["【剧情摘要】"]
                for event in self.plot_events[-10:]:
                    plot_lines.append(
                        f"  第{event['chapter']}章: {event['event'][:80]}"
                    )
                parts.append("\n".join(plot_lines))

        if categories is None or "world" in categories:
            if self.world_settings:
                world_lines = ["【世界观设定】"]
                for key, value in list(self.world_settings.items())[:10]:
                    world_lines.append(f"  {key}: {str(value)[:100]}")
                parts.append("\n".join(world_lines))

        context = "\n\n".join(parts)
        if len(context) > max_chars:
            context = context[:max_chars] + "\n...(上下文已截断)"
        return context

    # ================================================================
    # 写作风格指纹
    # ================================================================

    def compute_style_fingerprint(self, chapter: int, text: str) -> StyleFingerprint:
        """计算单章写作风格指纹"""
        sentences = re.split(r'[。！？\n]+', text)
        sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 1]

        if not sentences:
            return StyleFingerprint(chapter=chapter)

        sent_lengths = [len(s) for s in sentences]
        avg_len = sum(sent_lengths) / len(sent_lengths)
        variance = sum((l - avg_len) ** 2 for l in sent_lengths) / len(sent_lengths)
        std_len = variance ** 0.5

        dialogue_lines = len(re.findall(r'[""「」『』].*?[""「」『』]', text))
        dialogue_chars = sum(len(m) for m in re.findall(r'[""「」『』].*?[""「」『」]', text))
        total_chars = len(text)
        dialogue_ratio = dialogue_chars / max(total_chars, 1)

        desc_markers = len(re.findall(r'(只见|望去|看去|眼前|远处|近处|周围|四周)', text))
        desc_ratio = desc_markers / max(len(sentences), 1)

        action_markers = len(re.findall(r'(出手|挥|斩|刺|劈|砍|轰|爆|闪|冲|飞|跃)', text))
        action_ratio = action_markers / max(len(sentences), 1)

        thought_markers = len(re.findall(r'(心想|暗想|心中|暗道|默念|思忖)', text))
        thought_ratio = thought_markers / max(len(sentences), 1)

        paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
        para_lengths = [len(p) for p in paragraphs]

        words = re.findall(r'[\u4e00-\u9fff]{2,4}', text)
        word_freq = Counter(words).most_common(20)

        emotional_keywords = {
            '喜': ['笑', '喜', '乐', '欢', '悦', '高兴', '开心'],
            '怒': ['怒', '愤', '恨', '气', '恼', '吼', '喝'],
            '哀': ['悲', '哀', '伤', '哭', '泪', '痛', '苦'],
            '惊': ['惊', '震', '愣', '呆', '愕', '诧', '骇'],
            '惧': ['怕', '恐', '惧', '畏', '怯', '寒', '栗'],
            '静': ['静', '默', '沉', '淡', '冷', '宁', '寂'],
        }
        emotional_scores = []
        for emo, keywords in emotional_keywords.items():
            score = sum(text.count(kw) for kw in keywords) / max(len(sentences), 1)
            emotional_scores.append(round(score, 4))

        unique_words = len(set(re.findall(r'[\u4e00-\u9fff]+', text)))

        fp = StyleFingerprint(
            chapter=chapter,
            avg_sentence_length=round(avg_len, 2),
            sentence_length_std=round(std_len, 2),
            dialogue_ratio=round(dialogue_ratio, 4),
            description_ratio=round(desc_ratio, 4),
            action_ratio=round(action_ratio, 4),
            inner_thought_ratio=round(thought_ratio, 4),
            paragraph_count=len(paragraphs),
            avg_paragraph_length=round(sum(para_lengths) / max(len(paragraphs), 1), 2),
            top_words=word_freq,
            emotional_curve=emotional_scores,
            unique_word_count=unique_words,
            total_word_count=len(text),
            computed_at=datetime.now().isoformat(),
        )

        self.style_fingerprints[chapter] = fp
        self.total_words_processed += len(text)
        return fp

    def check_style_drift(self, chapter: int,
                          threshold: float = 0.3) -> List[ConsistencyIssue]:
        """检测风格漂移"""
        issues = []
        current = self.style_fingerprints.get(chapter)
        if not current:
            return issues

        recent_chapters = sorted(
            [ch for ch in self.style_fingerprints if ch < chapter],
            reverse=True
        )[:5]

        if not recent_chapters:
            return issues

        baselines = [self.style_fingerprints[ch] for ch in recent_chapters]
        avg_dialogue = sum(b.dialogue_ratio for b in baselines) / len(baselines)
        avg_sent_len = sum(b.avg_sentence_length for b in baselines) / len(baselines)
        avg_desc = sum(b.description_ratio for b in baselines) / len(baselines)

        if avg_dialogue > 0 and abs(current.dialogue_ratio - avg_dialogue) / avg_dialogue > threshold:
            issues.append(ConsistencyIssue(
                issue_id=f"style_{self.issue_counter + 1}",
                category="风格漂移",
                severity=ConsistencyLevel.NOTICEABLE_DRIFT,
                description=f"第{chapter}章对话占比({current.dialogue_ratio:.2%})与前5章均值({avg_dialogue:.2%})偏差过大",
                chapter=chapter,
                suggestion="检查是否AI生成内容过多，或叙事节奏突变",
            ))
            self.issue_counter += 1

        if avg_sent_len > 0 and abs(current.avg_sentence_length - avg_sent_len) / avg_sent_len > threshold:
            issues.append(ConsistencyIssue(
                issue_id=f"style_{self.issue_counter + 1}",
                category="风格漂移",
                severity=ConsistencyLevel.MINOR_DRIFT,
                description=f"第{chapter}章平均句长({current.avg_sentence_length})与前5章均值({avg_sent_len:.1f})偏差过大",
                chapter=chapter,
                suggestion="检查句式是否过于单一或冗长",
            ))
            self.issue_counter += 1

        self.issues.extend(issues)
        return issues

    def get_style_report(self) -> Dict:
        """获取全书风格报告"""
        if not self.style_fingerprints:
            return {"message": "暂无风格数据"}

        chapters = sorted(self.style_fingerprints.keys())
        fps = [self.style_fingerprints[ch] for ch in chapters]

        return {
            "total_chapters_analyzed": len(chapters),
            "total_words": self.total_words_processed,
            "avg_sentence_length": round(sum(f.avg_sentence_length for f in fps) / len(fps), 2),
            "avg_dialogue_ratio": round(sum(f.dialogue_ratio for f in fps) / len(fps), 4),
            "avg_description_ratio": round(sum(f.description_ratio for f in fps) / len(fps), 4),
            "avg_action_ratio": round(sum(f.action_ratio for f in fps) / len(fps), 4),
            "style_stability": self._compute_style_stability(fps),
            "chapter_fingerprints": {
                ch: {
                    "avg_sent_len": fp.avg_sentence_length,
                    "dialogue_ratio": fp.dialogue_ratio,
                    "action_ratio": fp.action_ratio,
                }
                for ch, fp in self.style_fingerprints.items()
            },
        }

    def _compute_style_stability(self, fps: List[StyleFingerprint]) -> str:
        """计算风格稳定性评级"""
        if len(fps) < 2:
            return "数据不足"

        dialogue_variance = sum(
            abs(fps[i].dialogue_ratio - fps[i - 1].dialogue_ratio)
            for i in range(1, len(fps))
        ) / (len(fps) - 1)

        if dialogue_variance < 0.05:
            return "非常稳定"
        elif dialogue_variance < 0.10:
            return "稳定"
        elif dialogue_variance < 0.20:
            return "有波动"
        return "波动较大"

    # ================================================================
    # 伏笔管理
    # ================================================================

    def plant_foreshadowing(self, description: str, planted_chapter: int,
                            expected_payoff_chapter: int,
                            fs_type: str = "plot",
                            importance: int = 5,
                            related_characters: List[str] = None,
                            tags: List[str] = None) -> str:
        """埋设伏笔"""
        self.fs_counter += 1
        fs_id = f"FS_{self.fs_counter:04d}"

        fs = Foreshadowing(
            fs_id=fs_id,
            description=description,
            planted_chapter=planted_chapter,
            expected_payoff_chapter=expected_payoff_chapter,
            type=fs_type,
            importance=importance,
            related_characters=related_characters or [],
            tags=tags or [],
            created_at=datetime.now().isoformat(),
        )

        self.foreshadowings[fs_id] = fs
        return fs_id

    def resolve_foreshadowing(self, fs_id: str,
                              actual_chapter: int) -> bool:
        """回收伏笔"""
        if fs_id not in self.foreshadowings:
            return False

        fs = self.foreshadowings[fs_id]
        fs.status = ForeshadowStatus.FULLY_PAID
        fs.actual_payoff_chapter = actual_chapter
        fs.resolved_at = datetime.now().isoformat()
        return True

    def get_unresolved_foreshadowing(self,
                                     current_chapter: int = None) -> List[Foreshadowing]:
        """获取未回收的伏笔"""
        unresolved = []
        for fs in self.foreshadowings.values():
            if fs.status in [ForeshadowStatus.PLANTED, ForeshadowStatus.HINTED]:
                unresolved.append(fs)

        if current_chapter:
            unresolved.sort(key=lambda f: (
                0 if f.expected_payoff_chapter <= current_chapter else 1,
                f.expected_payoff_chapter
            ))

        return unresolved

    def get_overdue_foreshadowing(self,
                                  current_chapter: int) -> List[Foreshadowing]:
        """获取超期未回收的伏笔"""
        overdue = []
        for fs in self.foreshadowings.values():
            if (fs.status in [ForeshadowStatus.PLANTED, ForeshadowStatus.HINTED]
                    and fs.expected_payoff_chapter < current_chapter):
                overdue.append(fs)
        return overdue

    def get_foreshadowing_stats(self) -> Dict:
        """伏笔统计"""
        total = len(self.foreshadowings)
        resolved = sum(1 for f in self.foreshadowings.values()
                       if f.status == ForeshadowStatus.FULLY_PAID)
        unresolved = total - resolved

        return {
            "total": total,
            "resolved": resolved,
            "unresolved": unresolved,
            "resolution_rate": round(resolved / max(total, 1) * 100, 1),
            "by_type": Counter(f.type for f in self.foreshadowings.values()),
            "by_importance": Counter(f.importance for f in self.foreshadowings.values()),
        }

    # ================================================================
    # 人物一致性
    # ================================================================

    def register_character(self, name: str, **kwargs) -> CharacterProfile:
        """注册/更新人物档案"""
        if name in self.characters:
            profile = self.characters[name]
            for key, value in kwargs.items():
                if hasattr(profile, key) and value is not None:
                    setattr(profile, key, value)
        else:
            profile = CharacterProfile(name=name, **kwargs)
            self.characters[name] = profile

        return profile

    def check_character_consistency(self, name: str,
                                    chapter: int,
                                    claimed_traits: Dict[str, Any]) -> List[ConsistencyIssue]:
        """检查人物一致性"""
        issues = []
        profile = self.characters.get(name)
        if not profile:
            return issues

        if "appearance" in claimed_traits:
            for key, value in claimed_traits["appearance"].items():
                if key in profile.appearance and profile.appearance[key] != value:
                    issues.append(ConsistencyIssue(
                        issue_id=f"char_{self.issue_counter + 1}",
                        category="人物一致性",
                        severity=ConsistencyLevel.NOTICEABLE_DRIFT,
                        description=f"「{name}」外貌矛盾: {key} 原为「{profile.appearance[key]}」,第{chapter}章变为「{value}」",
                        chapter=chapter,
                        suggestion=f"统一「{name}」的{key}描述",
                    ))
                    self.issue_counter += 1

        if "abilities" in claimed_traits:
            existing_abilities = {a.get("name") for a in profile.abilities}
            for ability in claimed_traits["abilities"]:
                if ability.get("name") not in existing_abilities:
                    profile.abilities.append(ability)

        self.issues.extend(issues)
        return issues

    def get_character_relationship_graph(self) -> Dict[str, Dict[str, str]]:
        """获取人物关系图谱"""
        graph = {}
        for name, profile in self.characters.items():
            graph[name] = dict(profile.relationships)
        return graph

    def find_character_inconsistencies(self) -> List[ConsistencyIssue]:
        """扫描全部人物一致性问题"""
        all_issues = []

        for name, profile in self.characters.items():
            if profile.first_appearance_chapter > 0 and profile.last_appearance_chapter > 0:
                gap = profile.last_appearance_chapter - profile.first_appearance_chapter
                if gap > 100 and profile.status == "存活":
                    all_issues.append(ConsistencyIssue(
                        issue_id=f"char_{self.issue_counter + 1}",
                        category="人物一致性",
                        severity=ConsistencyLevel.MINOR_DRIFT,
                        description=f"「{name}」已连续{gap}章未出场，请确认是否遗忘该角色",
                        chapter=profile.last_appearance_chapter,
                        suggestion=f"考虑安排「{name}」在近期章节出场或交代去向",
                    ))
                    self.issue_counter += 1

        self.issues.extend(all_issues)
        return all_issues

    # ================================================================
    # 剧情一致性验证
    # ================================================================

    def record_plot_event(self, chapter: int, event: str,
                          event_type: str = "general",
                          characters: List[str] = None,
                          location: str = "",
                          tags: List[str] = None) -> int:
        """记录剧情事件"""
        event_record = {
            "id": len(self.plot_events) + 1,
            "chapter": chapter,
            "event": event,
            "type": event_type,
            "characters": characters or [],
            "location": location,
            "tags": tags or [],
            "timestamp": datetime.now().isoformat(),
        }
        self.plot_events.append(event_record)

        if chapter not in self.timeline:
            self.timeline[chapter] = {"events": [], "locations": set(), "characters": set()}
        self.timeline[chapter]["events"].append(event)
        if location:
            self.timeline[chapter]["locations"].add(location)
        if characters:
            self.timeline[chapter]["characters"].update(characters)

        return event_record["id"]

    def verify_timeline(self) -> List[ConsistencyIssue]:
        """验证时间线一致性"""
        issues = []
        sorted_chapters = sorted(self.timeline.keys())

        for i in range(1, len(sorted_chapters)):
            prev_ch = sorted_chapters[i - 1]
            curr_ch = sorted_chapters[i]

            prev_locations = self.timeline[prev_ch].get("locations", set())
            curr_locations = self.timeline[curr_ch].get("locations", set())

            if prev_locations and curr_locations:
                for loc in curr_locations:
                    if loc not in prev_locations:
                        prev_loc_str = "、".join(prev_locations)
                        issues.append(ConsistencyIssue(
                            issue_id=f"timeline_{self.issue_counter + 1}",
                            category="时间线",
                            severity=ConsistencyLevel.MINOR_DRIFT,
                            description=f"第{curr_ch}章出现新地点「{loc}」，前章地点为「{prev_loc_str}」，请确认地点切换是否合理",
                            chapter=curr_ch,
                            related_chapters=[prev_ch, curr_ch],
                            suggestion="添加地点切换的过渡描写",
                        ))
                        self.issue_counter += 1

        self.issues.extend(issues)
        return issues

    def verify_power_system(self, character_name: str,
                            claimed_level: str,
                            chapter: int) -> Optional[ConsistencyIssue]:
        """验证实力体系一致性"""
        profile = self.characters.get(character_name)
        if not profile:
            return None

        for ability in profile.abilities:
            if ability.get("type") == "cultivation":
                prev_level = ability.get("level", "")
                if prev_level and prev_level != claimed_level:
                    levels = ["炼气", "筑基", "金丹", "元婴", "化神", "炼虚", "合体", "大乘", "渡劫"]
                    if prev_level in levels and claimed_level in levels:
                        prev_idx = levels.index(prev_level)
                        curr_idx = levels.index(claimed_level)
                        if curr_idx < prev_idx:
                            issue = ConsistencyIssue(
                                issue_id=f"power_{self.issue_counter + 1}",
                                category="实力体系",
                                severity=ConsistencyLevel.MAJOR_CONFLICT,
                                description=f"「{character_name}」实力倒退: 第{chapter}章为「{claimed_level}」，但之前已是「{prev_level}」",
                                chapter=chapter,
                                suggestion=f"修正实力描述，保持{prev_level}或更高",
                            )
                            self.issue_counter += 1
                            self.issues.append(issue)
                            return issue

        return None

    # ================================================================
    # 情感弧线验证
    # ================================================================

    def track_emotional_arc(self, chapter: int, text: str) -> EmotionalArcPoint:
        """追踪单章情感弧线"""
        emotion_keywords = {
            "喜": ["笑", "喜", "乐", "欢", "悦", "高兴", "开心", "欣", "愉", "畅"],
            "怒": ["怒", "愤", "恨", "气", "恼", "吼", "喝", "斥", "暴", "戾"],
            "哀": ["悲", "哀", "伤", "哭", "泪", "痛", "苦", "凄", "惨", "凉"],
            "惊": ["惊", "震", "愣", "呆", "愕", "诧", "骇", "讶", "异", "奇"],
            "惧": ["怕", "恐", "惧", "畏", "怯", "寒", "栗", "颤", "抖", "缩"],
            "静": ["静", "默", "沉", "淡", "冷", "宁", "寂", "幽", "谧", "安"],
            "紧张": ["紧", "绷", "悬", "急", "迫", "焦", "躁", "促", "逼", "险"],
            "感动": ["感", "动", "暖", "温", "柔", "情", "爱", "恩", "义", "忠"],
        }

        sentences = re.split(r'[。！？\n]+', text)
        sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 1]
        total_sentences = max(len(sentences), 1)

        scores = {}
        for emotion, keywords in emotion_keywords.items():
            count = sum(text.count(kw) for kw in keywords)
            scores[emotion] = round(count / total_sentences, 4)

        dominant = max(scores, key=scores.get)
        intensity = scores[dominant]

        prev_transition = ""
        if self.emotional_arc:
            prev = self.emotional_arc[-1]
            if prev.dominant_emotion != dominant:
                prev_transition = f"{prev.dominant_emotion}→{dominant}"

        point = EmotionalArcPoint(
            chapter=chapter,
            dominant_emotion=dominant,
            emotion_scores=scores,
            intensity=intensity,
            transition_from_prev=prev_transition,
        )
        self.emotional_arc.append(point)
        return point

    def verify_emotional_consistency(self) -> List[ConsistencyIssue]:
        """验证情感弧线一致性"""
        issues = []
        if len(self.emotional_arc) < 3:
            return issues

        for i in range(2, len(self.emotional_arc)):
            prev2 = self.emotional_arc[i - 2]
            prev1 = self.emotional_arc[i - 1]
            curr = self.emotional_arc[i]

            if (prev2.dominant_emotion == "喜" and prev1.dominant_emotion == "喜"
                    and curr.dominant_emotion == "哀" and curr.intensity > 0.5):
                issues.append(ConsistencyIssue(
                    issue_id=f"emo_{self.issue_counter + 1}",
                    category="情感弧线",
                    severity=ConsistencyLevel.NOTICEABLE_DRIFT,
                    description=f"第{curr.chapter}章情感急转直下(喜→哀)，请确认转折是否有充分铺垫",
                    chapter=curr.chapter,
                    suggestion="在情感转折前增加过渡描写或伏笔暗示",
                ))
                self.issue_counter += 1

            if curr.intensity < 0.05:
                issues.append(ConsistencyIssue(
                    issue_id=f"emo_{self.issue_counter + 1}",
                    category="情感弧线",
                    severity=ConsistencyLevel.MINOR_DRIFT,
                    description=f"第{curr.chapter}章情感强度过低({curr.intensity:.3f})，可能缺乏情感张力",
                    chapter=curr.chapter,
                    suggestion="增加角色的情感反应描写，提升读者代入感",
                ))
                self.issue_counter += 1

        self.issues.extend(issues)
        return issues

    def get_emotional_arc_report(self) -> Dict:
        """获取情感弧线报告"""
        if not self.emotional_arc:
            return {"message": "暂无情感数据"}

        return {
            "total_points": len(self.emotional_arc),
            "dominant_emotions": Counter(
                p.dominant_emotion for p in self.emotional_arc
            ),
            "avg_intensity": round(
                sum(p.intensity for p in self.emotional_arc) / len(self.emotional_arc), 4
            ),
            "transitions": [
                {"chapter": p.chapter, "emotion": p.dominant_emotion,
                 "intensity": p.intensity, "transition": p.transition_from_prev}
                for p in self.emotional_arc
            ],
        }

    # ================================================================
    # 节奏曲线分析
    # ================================================================

    def analyze_pacing(self, chapter: int, text: str) -> PacingProfile:
        """分析章节节奏"""
        sentences = re.split(r'[。！？\n]+', text)
        sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 1]
        total_sentences = max(len(sentences), 1)

        action_keywords = ["出手", "挥", "斩", "刺", "劈", "砍", "轰", "爆", "闪",
                           "冲", "飞", "跃", "击", "杀", "战", "斗", "攻", "防", "破"]
        dialogue_pattern = re.findall(r'[""「」『』].*?[""「」『」]', text)
        desc_keywords = ["只见", "望去", "看去", "眼前", "远处", "近处", "周围", "四周",
                         "弥漫", "笼罩", "浮现", "呈现", "映照"]

        action_count = sum(text.count(kw) for kw in action_keywords)
        dialogue_chars = sum(len(d) for d in dialogue_pattern)
        desc_count = sum(text.count(kw) for kw in desc_keywords)

        action_density = round(action_count / total_sentences, 4)
        dialogue_density = round(dialogue_chars / max(len(text), 1), 4)
        description_density = round(desc_count / total_sentences, 4)

        paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
        para_lengths = [len(p) for p in paragraphs]
        if len(para_lengths) > 1:
            para_variation = round(
                sum(abs(para_lengths[i] - para_lengths[i - 1])
                    for i in range(1, len(para_lengths))) / (len(para_lengths) - 1), 2
            )
        else:
            para_variation = 0

        if action_density > 0.3:
            pacing = PacingType.FAST
        elif dialogue_density > 0.3:
            pacing = PacingType.MODERATE
        elif description_density > 0.2:
            pacing = PacingType.SLOW
        else:
            pacing = PacingType.MODERATE

        profile = PacingProfile(
            chapter=chapter,
            pacing_type=pacing,
            action_density=action_density,
            dialogue_density=dialogue_density,
            description_density=description_density,
            paragraph_variation=para_variation,
        )
        self.pacing_profiles[chapter] = profile
        return profile

    def verify_pacing_balance(self) -> List[ConsistencyIssue]:
        """验证节奏平衡性"""
        issues = []
        if len(self.pacing_profiles) < 3:
            return issues

        sorted_chapters = sorted(self.pacing_profiles.keys())
        for i in range(len(sorted_chapters) - 2):
            ch1, ch2, ch3 = sorted_chapters[i], sorted_chapters[i + 1], sorted_chapters[i + 2]
            p1, p2, p3 = (self.pacing_profiles[ch1],
                          self.pacing_profiles[ch2],
                          self.pacing_profiles[ch3])

            if p1.pacing_type == p2.pacing_type == p3.pacing_type == PacingType.FAST:
                issues.append(ConsistencyIssue(
                    issue_id=f"pace_{self.issue_counter + 1}",
                    category="节奏曲线",
                    severity=ConsistencyLevel.NOTICEABLE_DRIFT,
                    description=f"第{ch1}-{ch3}章连续快节奏，读者可能疲劳，建议插入慢节奏过渡章",
                    chapter=ch3,
                    suggestion="在第{ch2}章后插入日常/感情/修炼等慢节奏内容",
                ))
                self.issue_counter += 1

            if p1.pacing_type == p2.pacing_type == p3.pacing_type == PacingType.SLOW:
                issues.append(ConsistencyIssue(
                    issue_id=f"pace_{self.issue_counter + 1}",
                    category="节奏曲线",
                    severity=ConsistencyLevel.MINOR_DRIFT,
                    description=f"第{ch1}-{ch3}章连续慢节奏，可能拖沓，建议插入冲突或转折",
                    chapter=ch3,
                    suggestion="增加小冲突、新信息或悬念来提升节奏",
                ))
                self.issue_counter += 1

        self.issues.extend(issues)
        return issues

    def get_pacing_report(self) -> Dict:
        """获取节奏报告"""
        if not self.pacing_profiles:
            return {"message": "暂无节奏数据"}

        return {
            "total_chapters": len(self.pacing_profiles),
            "pacing_distribution": Counter(
                p.pacing_type.value for p in self.pacing_profiles.values()
            ),
            "avg_action_density": round(
                sum(p.action_density for p in self.pacing_profiles.values())
                / len(self.pacing_profiles), 4
            ),
            "avg_dialogue_density": round(
                sum(p.dialogue_density for p in self.pacing_profiles.values())
                / len(self.pacing_profiles), 4
            ),
            "chapters": {
                ch: {"type": p.pacing_type.value, "action": p.action_density}
                for ch, p in self.pacing_profiles.items()
            },
        }

    # ================================================================
    # 对话一致性验证
    # ================================================================

    def extract_dialogue_fingerprint(self, character_name: str,
                                     dialogues: List[str]) -> DialogueFingerprint:
        """提取角色对话风格指纹"""
        if not dialogues:
            return DialogueFingerprint(character_name=character_name)

        lengths = [len(d) for d in dialogues]
        avg_len = sum(lengths) / len(lengths)

        exclamation = sum(1 for d in dialogues if '！' in d or '!' in d) / len(dialogues)
        question = sum(1 for d in dialogues if '？' in d or '?' in d) / len(dialogues)

        catchphrases = Counter()
        for d in dialogues:
            words = re.findall(r'[\u4e00-\u9fff]{2,4}', d)
            catchphrases.update(words)

        formal_markers = ["您", "请", "阁下", "大人", "前辈", "师尊", "恕", "敢问"]
        casual_markers = ["老子", "他娘的", "操", "靠", "妈的", "卧槽", "尼玛"]
        formal_count = sum(d.count(m) for m in formal_markers for d in dialogues)
        casual_count = sum(d.count(m) for m in casual_markers for d in dialogues)
        formality = 0.5
        if formal_count + casual_count > 0:
            formality = formal_count / (formal_count + casual_count)

        unique = set()
        for d in dialogues:
            unique.update(re.findall(r'[\u4e00-\u9fff]+', d))

        fp = DialogueFingerprint(
            character_name=character_name,
            avg_sentence_length=round(avg_len, 2),
            exclamation_ratio=round(exclamation, 4),
            question_ratio=round(question, 4),
            catchphrase_usage=dict(catchphrases.most_common(20)),
            formality_level=round(formality, 4),
            unique_words=unique,
        )
        self.dialogue_fingerprints[character_name] = fp
        return fp

    def check_dialogue_consistency(self, character_name: str,
                                   new_dialogues: List[str],
                                   chapter: int) -> List[ConsistencyIssue]:
        """检查对话风格一致性"""
        issues = []
        existing = self.dialogue_fingerprints.get(character_name)
        if not existing or not new_dialogues:
            return issues

        new_fp = self.extract_dialogue_fingerprint(
            f"{character_name}_ch{chapter}", new_dialogues
        )

        if existing.avg_sentence_length > 0:
            len_diff = abs(new_fp.avg_sentence_length - existing.avg_sentence_length)
            if len_diff > existing.avg_sentence_length * 0.5:
                issues.append(ConsistencyIssue(
                    issue_id=f"dialogue_{self.issue_counter + 1}",
                    category="对话一致性",
                    severity=ConsistencyLevel.NOTICEABLE_DRIFT,
                    description=f"「{character_name}」第{chapter}章对话长度({new_fp.avg_sentence_length:.0f}字)与历史({existing.avg_sentence_length:.0f}字)偏差过大",
                    chapter=chapter,
                    suggestion=f"检查「{character_name}」的对话风格是否保持一致",
                ))
                self.issue_counter += 1

        if existing.formality_level > 0:
            form_diff = abs(new_fp.formality_level - existing.formality_level)
            if form_diff > 0.4:
                issues.append(ConsistencyIssue(
                    issue_id=f"dialogue_{self.issue_counter + 1}",
                    category="对话一致性",
                    severity=ConsistencyLevel.MINOR_DRIFT,
                    description=f"「{character_name}」第{chapter}章语气正式度({new_fp.formality_level:.2f})与历史({existing.formality_level:.2f})偏差过大",
                    chapter=chapter,
                    suggestion=f"统一「{character_name}」的说话语气",
                ))
                self.issue_counter += 1

        self.issues.extend(issues)
        return issues

    # ================================================================
    # 世界观一致性验证
    # ================================================================

    def register_world_rule(self, category: str, rule: str,
                            chapter: int) -> str:
        """注册世界观规则"""
        self.rule_counter += 1
        rule_id = f"RULE_{self.rule_counter:04d}"

        self.world_rules[rule_id] = WorldRule(
            rule_id=rule_id,
            category=category,
            rule=rule,
            established_chapter=chapter,
            last_verified_chapter=chapter,
        )
        return rule_id

    def verify_world_rules(self, chapter: int,
                           claimed_rules: List[Dict]) -> List[ConsistencyIssue]:
        """验证世界观规则一致性"""
        issues = []

        for claimed in claimed_rules:
            for rule_id, rule in self.world_rules.items():
                if rule.category == claimed.get("category", ""):
                    if rule.rule != claimed.get("rule", ""):
                        issues.append(ConsistencyIssue(
                            issue_id=f"world_{self.issue_counter + 1}",
                            category="世界观一致性",
                            severity=ConsistencyLevel.MAJOR_CONFLICT,
                            description=f"世界观规则冲突: 第{rule.established_chapter}章「{rule.rule}」vs 第{chapter}章「{claimed.get('rule', '')}」",
                            chapter=chapter,
                            related_chapters=[rule.established_chapter, chapter],
                            suggestion=f"统一{rule.category}的设定，选择其一或说明例外情况",
                        ))
                        self.issue_counter += 1
                    else:
                        rule.last_verified_chapter = chapter

        self.issues.extend(issues)
        return issues

    def get_world_rules_report(self) -> Dict:
        """获取世界观规则报告"""
        return {
            "total_rules": len(self.world_rules),
            "by_category": Counter(r.category for r in self.world_rules.values()),
            "rules": [
                {
                    "id": r.rule_id,
                    "category": r.category,
                    "rule": r.rule,
                    "established": r.established_chapter,
                    "last_verified": r.last_verified_chapter,
                }
                for r in self.world_rules.values()
            ],
        }

    # ================================================================
    # 章节质量评分
    # ================================================================

    def score_chapter_quality(self, chapter: int, text: str) -> Dict:
        """综合评分章节质量"""
        sentences = re.split(r'[。！？\n]+', text)
        sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 1]
        total_sentences = max(len(sentences), 1)

        sent_lengths = [len(s) for s in sentences]
        avg_sent_len = sum(sent_lengths) / len(sent_lengths)
        sent_variance = sum((l - avg_sent_len) ** 2 for l in sent_lengths) / len(sent_lengths)

        variety_score = min(100, sent_variance ** 0.5 * 10)

        dialogue_chars = sum(len(m) for m in re.findall(r'[""「」『』].*?[""「」『」]', text))
        dialogue_score = min(100, (dialogue_chars / max(len(text), 1)) * 200)

        action_keywords = ["出手", "挥", "斩", "刺", "劈", "砍", "轰", "爆", "闪",
                           "冲", "飞", "跃", "击", "杀", "战", "斗", "攻", "防", "破"]
        action_count = sum(text.count(kw) for kw in action_keywords)
        action_score = min(100, (action_count / total_sentences) * 200)

        emotion_keywords = ["笑", "怒", "悲", "惊", "怕", "哭", "泪", "痛", "喜", "忧"]
        emotion_count = sum(text.count(kw) for kw in emotion_keywords)
        emotion_score = min(100, (emotion_count / total_sentences) * 150)

        paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
        para_lengths = [len(p) for p in paragraphs]
        if len(para_lengths) > 1:
            para_variation = sum(
                abs(para_lengths[i] - para_lengths[i - 1])
                for i in range(1, len(para_lengths))
            ) / (len(para_lengths) - 1)
            structure_score = min(100, max(30, 100 - para_variation / 5))
        else:
            structure_score = 50

        word_count = len(text)
        if word_count < 2000:
            length_score = max(20, word_count / 20)
        elif word_count < 5000:
            length_score = 80 + (word_count - 2000) / 150
        else:
            length_score = min(100, 100 - (word_count - 5000) / 200)

        scores = {
            "句式多样性": round(variety_score, 1),
            "对话丰富度": round(dialogue_score, 1),
            "动作密度": round(action_score, 1),
            "情感表达": round(emotion_score, 1),
            "段落结构": round(structure_score, 1),
            "篇幅适中": round(length_score, 1),
        }

        weights = {
            "句式多样性": 0.15, "对话丰富度": 0.20,
            "动作密度": 0.20, "情感表达": 0.20,
            "段落结构": 0.10, "篇幅适中": 0.15,
        }
        overall = sum(scores[k] * weights[k] for k in scores)

        result = {
            "chapter": chapter,
            "overall_score": round(overall, 1),
            "grade": self._score_to_grade(overall),
            "dimension_scores": scores,
            "word_count": word_count,
            "sentence_count": total_sentences,
            "paragraph_count": len(paragraphs),
        }
        self.chapter_quality_scores[chapter] = result
        return result

    def _score_to_grade(self, score: float) -> str:
        if score >= 90:
            return "S - 卓越"
        elif score >= 80:
            return "A - 优秀"
        elif score >= 70:
            return "B - 良好"
        elif score >= 60:
            return "C - 合格"
        return "D - 需改进"

    def get_quality_report(self) -> Dict:
        """获取质量评分报告"""
        if not self.chapter_quality_scores:
            return {"message": "暂无评分数据"}

        scores = list(self.chapter_quality_scores.values())
        return {
            "total_chapters_scored": len(scores),
            "avg_overall_score": round(
                sum(s["overall_score"] for s in scores) / len(scores), 1
            ),
            "grade_distribution": Counter(s["grade"] for s in scores),
            "best_chapter": max(scores, key=lambda s: s["overall_score"]),
            "worst_chapter": min(scores, key=lambda s: s["overall_score"]),
            "chapters": {
                s["chapter"]: {"score": s["overall_score"], "grade": s["grade"]}
                for s in scores
            },
        }

    # ================================================================
    # 冲突密度追踪
    # ================================================================

    def track_conflict_density(self, chapter: int, text: str) -> float:
        """追踪章节冲突密度"""
        conflict_keywords = [
            "冲突", "矛盾", "对抗", "战斗", "厮杀", "对决", "较量",
            "争执", "争吵", "辩论", "对峙", "威胁", "挑战", "阻碍",
            "危机", "危险", "陷阱", "阴谋", "背叛", "暗算", "伏击",
            "突破", "瓶颈", "考验", "试炼", "劫难", "天劫", "心魔",
        ]

        sentences = re.split(r'[。！？\n]+', text)
        sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 1]
        total_sentences = max(len(sentences), 1)

        conflict_sentences = sum(
            1 for s in sentences
            if any(kw in s for kw in conflict_keywords)
        )
        density = round(conflict_sentences / total_sentences, 4)
        self.conflict_density[chapter] = density
        return density

    def verify_conflict_requirements(self) -> List[ConsistencyIssue]:
        """验证冲突密度要求"""
        issues = []
        for chapter, density in self.conflict_density.items():
            if density < 0.05:
                issues.append(ConsistencyIssue(
                    issue_id=f"conflict_{self.issue_counter + 1}",
                    category="冲突密度",
                    severity=ConsistencyLevel.MINOR_DRIFT,
                    description=f"第{chapter}章冲突密度过低({density:.2%})，可能缺乏张力",
                    chapter=chapter,
                    suggestion="每章至少安排一个小冲突或悬念，保持读者阅读动力",
                ))
                self.issue_counter += 1

        self.issues.extend(issues)
        return issues

    def get_conflict_report(self) -> Dict:
        """获取冲突密度报告"""
        if not self.conflict_density:
            return {"message": "暂无冲突数据"}

        densities = list(self.conflict_density.values())
        return {
            "total_chapters": len(self.conflict_density),
            "avg_density": round(sum(densities) / len(densities), 4),
            "max_density": max(densities),
            "min_density": min(densities),
            "low_conflict_chapters": [
                ch for ch, d in self.conflict_density.items() if d < 0.05
            ],
            "chapters": dict(self.conflict_density),
        }

    def get_comprehensive_report(self) -> Dict:
        """获取综合一致性报告"""
        return {
            "novel_title": self.novel_title,
            "total_words": self.total_words_processed,
            "style": self.get_style_report(),
            "emotional_arc": self.get_emotional_arc_report(),
            "pacing": self.get_pacing_report(),
            "foreshadowing": self.get_foreshadowing_stats(),
            "characters": {
                "total": len(self.characters),
                "list": [
                    {
                        "name": p.name,
                        "role": p.role,
                        "first_chapter": p.first_appearance_chapter,
                        "last_chapter": p.last_appearance_chapter,
                        "status": p.status,
                    }
                    for p in self.characters.values()
                ],
            },
            "world_rules": self.get_world_rules_report(),
            "quality": self.get_quality_report(),
            "conflict": self.get_conflict_report(),
            "issues": {
                "total": len(self.issues),
                "unresolved": sum(1 for i in self.issues if not i.resolved),
                "by_category": Counter(i.category for i in self.issues),
                "by_severity": Counter(i.severity.value for i in self.issues),
                "recent": [
                    {
                        "category": i.category,
                        "description": i.description,
                        "chapter": i.chapter,
                        "severity": i.severity.value,
                    }
                    for i in self.issues[-10:]
                ],
            },
            "plot_events_count": len(self.plot_events),
        }

    def get_issues_by_severity(self,
                               min_severity: ConsistencyLevel = None) -> List[ConsistencyIssue]:
        """按严重程度筛选问题"""
        if min_severity is None:
            return list(self.issues)

        severity_order = {
            ConsistencyLevel.CONSISTENT: 0,
            ConsistencyLevel.MINOR_DRIFT: 1,
            ConsistencyLevel.NOTICEABLE_DRIFT: 2,
            ConsistencyLevel.MAJOR_CONFLICT: 3,
        }

        return [
            i for i in self.issues
            if severity_order.get(i.severity, 0) >= severity_order.get(min_severity, 0)
        ]

    # ================================================================
    # 智能检索系统 (Intelligent Retrieval)
    # ================================================================

    def store_chapter_text(self, chapter: int, text: str):
        """存储章节原文用于检索"""
        self.chapter_texts[chapter] = text

    def intelligent_search(self, query: str,
                           search_types: List[str] = None,
                           chapters: List[int] = None,
                           min_relevance: float = 0.2,
                           max_results: int = 20,
                           include_context: bool = True) -> List[RetrievalResult]:
        """智能检索 - 跨所有记忆维度搜索

        支持搜索类型:
        - 'character': 人物信息
        - 'plot': 剧情事件
        - 'setting': 世界观设定
        - 'foreshadowing': 伏笔
        - 'dialogue': 对话内容
        - 'text': 原文内容
        - 'rule': 世界观规则
        """
        if search_types is None:
            search_types = ['character', 'plot', 'setting', 'foreshadowing', 'text', 'rule']

        results: List[RetrievalResult] = []
        query_terms = self._tokenize_query(query)

        if 'character' in search_types:
            results.extend(self._search_characters(query, query_terms, chapters))

        if 'plot' in search_types:
            results.extend(self._search_plot_events(query, query_terms, chapters))

        if 'setting' in search_types:
            results.extend(self._search_settings(query, query_terms))

        if 'foreshadowing' in search_types:
            results.extend(self._search_foreshadowings(query, query_terms, chapters))

        if 'text' in search_types and self.chapter_texts:
            results.extend(self._search_chapter_texts(query, query_terms, chapters,
                                                       include_context))

        if 'rule' in search_types:
            results.extend(self._search_world_rules(query, query_terms))

        results = [r for r in results if r.relevance_score >= min_relevance]
        results.sort(key=lambda r: r.relevance_score, reverse=True)
        return results[:max_results]

    def _tokenize_query(self, query: str) -> List[str]:
        """分词查询"""
        tokens = []
        for i in range(len(query)):
            if i + 2 <= len(query):
                tokens.append(query[i:i + 2])
            if i + 3 <= len(query):
                tokens.append(query[i:i + 3])
        tokens.append(query)
        return list(set(tokens))

    def _search_characters(self, query: str, terms: List[str],
                           chapters: List[int] = None) -> List[RetrievalResult]:
        """搜索人物信息"""
        results = []
        for name, profile in self.characters.items():
            if chapters and profile.first_appearance_chapter not in chapters:
                continue

            score = 0.0
            matched = []

            if query in name:
                score += 1.0
                matched.append(name)
            for alias in profile.aliases:
                if query in alias:
                    score += 0.8
                    matched.append(alias)

            search_text = f"{profile.role} {' '.join(profile.personality)} "
            search_text += f"{' '.join(profile.catchphrases)} {profile.notes}"
            for term in terms:
                if term in search_text:
                    score += 0.3
                    matched.append(term)

            if score > 0:
                content = (f"【{name}】角色: {profile.role}, "
                           f"性格: {'/'.join(profile.personality[:5])}, "
                           f"首登场: 第{profile.first_appearance_chapter}章, "
                           f"状态: {profile.status}")
                self.retrieval_counter += 1
                results.append(RetrievalResult(
                    result_id=f"RET_{self.retrieval_counter:06d}",
                    content_type="character",
                    chapter=profile.first_appearance_chapter,
                    content=content,
                    relevance_score=min(score, 1.0),
                    matched_keywords=matched,
                    source_section="人物档案",
                ))
        return results

    def _search_plot_events(self, query: str, terms: List[str],
                            chapters: List[int] = None) -> List[RetrievalResult]:
        """搜索剧情事件"""
        results = []
        for event in self.plot_events:
            if chapters and event['chapter'] not in chapters:
                continue

            score = 0.0
            matched = []
            event_text = f"{event['event']} {event.get('type', '')} "
            event_text += f"{' '.join(event.get('characters', []))} "
            event_text += f"{event.get('location', '')} {' '.join(event.get('tags', []))}"

            for term in terms:
                if term in event_text:
                    score += 0.4
                    matched.append(term)

            if query in event['event']:
                score += 0.8
                matched.append(query)

            if score > 0:
                self.retrieval_counter += 1
                results.append(RetrievalResult(
                    result_id=f"RET_{self.retrieval_counter:06d}",
                    content_type="plot",
                    chapter=event['chapter'],
                    content=event['event'],
                    relevance_score=min(score, 1.0),
                    matched_keywords=matched,
                    source_section="剧情事件",
                ))
        return results

    def _search_settings(self, query: str, terms: List[str]) -> List[RetrievalResult]:
        """搜索世界观设定"""
        results = []
        for key, value in self.world_settings.items():
            score = 0.0
            matched = []
            search_text = f"{key} {str(value)}"

            for term in terms:
                if term in search_text:
                    score += 0.4
                    matched.append(term)

            if query in key:
                score += 0.8
                matched.append(key)

            if score > 0:
                self.retrieval_counter += 1
                results.append(RetrievalResult(
                    result_id=f"RET_{self.retrieval_counter:06d}",
                    content_type="setting",
                    chapter=0,
                    content=f"{key}: {str(value)[:200]}",
                    relevance_score=min(score, 1.0),
                    matched_keywords=matched,
                    source_section="世界观设定",
                ))
        return results

    def _search_foreshadowings(self, query: str, terms: List[str],
                               chapters: List[int] = None) -> List[RetrievalResult]:
        """搜索伏笔"""
        results = []
        for fs in self.foreshadowings.values():
            if chapters and fs.planted_chapter not in chapters:
                continue

            score = 0.0
            matched = []
            search_text = (f"{fs.description} {fs.type} "
                           f"{' '.join(fs.related_characters)} "
                           f"{' '.join(fs.tags)}")

            for term in terms:
                if term in search_text:
                    score += 0.4
                    matched.append(term)

            if query in fs.description:
                score += 0.8
                matched.append(query)

            if score > 0:
                self.retrieval_counter += 1
                results.append(RetrievalResult(
                    result_id=f"RET_{self.retrieval_counter:06d}",
                    content_type="foreshadowing",
                    chapter=fs.planted_chapter,
                    content=f"[{fs.status.value}] {fs.description} "
                            f"(埋设第{fs.planted_chapter}章, 预期回收第{fs.expected_payoff_chapter}章)",
                    relevance_score=min(score, 1.0),
                    matched_keywords=matched,
                    source_section="伏笔管理",
                ))
        return results

    def _search_chapter_texts(self, query: str, terms: List[str],
                              chapters: List[int] = None,
                              include_context: bool = True) -> List[RetrievalResult]:
        """搜索原文内容"""
        results = []
        target_chapters = chapters if chapters else sorted(self.chapter_texts.keys())

        for ch in target_chapters:
            if ch not in self.chapter_texts:
                continue
            text = self.chapter_texts[ch]

            idx = text.find(query)
            if idx >= 0:
                context_before = text[max(0, idx - 50):idx] if include_context else ""
                context_after = text[idx + len(query):idx + len(query) + 50] if include_context else ""

                self.retrieval_counter += 1
                results.append(RetrievalResult(
                    result_id=f"RET_{self.retrieval_counter:06d}",
                    content_type="text",
                    chapter=ch,
                    content=text[max(0, idx - 20):idx + len(query) + 20],
                    relevance_score=0.9,
                    matched_keywords=[query],
                    context_before=context_before,
                    context_after=context_after,
                    source_section="原文内容",
                ))
            else:
                score = 0.0
                matched = []
                for term in terms:
                    if term in text:
                        score += 0.2
                        matched.append(term)
                if score >= 0.4:
                    first_idx = text.find(matched[0]) if matched else 0
                    self.retrieval_counter += 1
                    results.append(RetrievalResult(
                        result_id=f"RET_{self.retrieval_counter:06d}",
                        content_type="text",
                        chapter=ch,
                        content=text[max(0, first_idx - 20):first_idx + 80],
                        relevance_score=min(score, 0.7),
                        matched_keywords=matched,
                        source_section="原文内容",
                    ))
        return results

    def _search_world_rules(self, query: str, terms: List[str]) -> List[RetrievalResult]:
        """搜索世界观规则"""
        results = []
        for rule in self.world_rules.values():
            score = 0.0
            matched = []
            search_text = f"{rule.category} {rule.rule} {' '.join(rule.exceptions)}"

            for term in terms:
                if term in search_text:
                    score += 0.4
                    matched.append(term)

            if query in rule.rule:
                score += 0.8
                matched.append(query)

            if score > 0:
                self.retrieval_counter += 1
                results.append(RetrievalResult(
                    result_id=f"RET_{self.retrieval_counter:06d}",
                    content_type="rule",
                    chapter=rule.established_chapter,
                    content=f"[{rule.category}] {rule.rule}",
                    relevance_score=min(score, 1.0),
                    matched_keywords=matched,
                    source_section="世界观规则",
                ))
        return results

    def context_aware_retrieval(self, current_chapter: int,
                                query: str,
                                context_window: int = 10) -> Dict:
        """上下文感知检索 - 基于当前写作位置智能检索相关信息

        自动识别当前章节附近最相关的人物、伏笔、设定
        """
        nearby_chapters = list(range(
            max(1, current_chapter - context_window),
            current_chapter + 1
        ))

        results = self.intelligent_search(
            query=query,
            chapters=nearby_chapters,
            max_results=15,
            include_context=True,
        )

        active_characters = []
        for name, profile in self.characters.items():
            if (profile.last_appearance_chapter >= current_chapter - context_window
                    and profile.status == "存活"):
                active_characters.append({
                    "name": name,
                    "role": profile.role,
                    "last_seen": profile.last_appearance_chapter,
                })

        pending_foreshadowing = []
        for fs in self.foreshadowings.values():
            if fs.status in [ForeshadowStatus.PLANTED, ForeshadowStatus.HINTED]:
                if (fs.expected_payoff_chapter <= current_chapter + context_window
                        and fs.expected_payoff_chapter >= current_chapter - 5):
                    pending_foreshadowing.append({
                        "id": fs.fs_id,
                        "description": fs.description,
                        "expected_chapter": fs.expected_payoff_chapter,
                        "urgency": "高" if fs.expected_payoff_chapter <= current_chapter else "中",
                    })

        return {
            "query": query,
            "current_chapter": current_chapter,
            "context_window": context_window,
            "search_results": [
                {
                    "type": r.content_type,
                    "chapter": r.chapter,
                    "content": r.content,
                    "score": r.relevance_score,
                }
                for r in results
            ],
            "active_characters": active_characters,
            "pending_foreshadowing": pending_foreshadowing,
            "nearby_issues": [
                {
                    "category": i.category,
                    "description": i.description,
                    "chapter": i.chapter,
                }
                for i in self.issues
                if i.chapter in nearby_chapters and not i.resolved
            ],
        }

    # ================================================================
    # 关联推理引擎 (Association Reasoning)
    # ================================================================

    def discover_causal_links(self, start_chapter: int = 1,
                              end_chapter: int = None) -> List[CausalLink]:
        """自动发现因果链 - 分析剧情事件间的因果关系"""
        if end_chapter is None:
            end_chapter = max(self.chapter_texts.keys()) if self.chapter_texts else start_chapter

        new_links = []
        events_in_range = [
            e for e in self.plot_events
            if start_chapter <= e['chapter'] <= end_chapter
        ]
        events_in_range.sort(key=lambda e: e['chapter'])

        causal_patterns = [
            (["获得", "发现", "得到", "觉醒", "突破"], ["使用", "展示", "击败", "解决", "进入"]),
            (["遭遇", "遇到", "碰见"], ["结识", "同行", "合作", "对抗"]),
            (["受伤", "中毒", "被困"], ["治疗", "解毒", "逃脱", "突破"]),
            (["威胁", "挑衅", "宣战"], ["反击", "战斗", "对决", "报复"]),
            (["失踪", "消失", "离开"], ["寻找", "追踪", "发现", "重逢"]),
            (["承诺", "约定", "誓言"], ["履行", "兑现", "赴约", "完成"]),
        ]

        for i, cause_event in enumerate(events_in_range):
            for j in range(i + 1, min(i + 10, len(events_in_range))):
                effect_event = events_in_range[j]
                chapter_gap = effect_event['chapter'] - cause_event['chapter']

                if chapter_gap > 50:
                    continue

                confidence = 0.0
                evidence = []
                link_type = "direct"

                for cause_patterns, effect_patterns in causal_patterns:
                    cause_match = any(p in cause_event['event'] for p in cause_patterns)
                    effect_match = any(p in effect_event['event'] for p in effect_patterns)
                    if cause_match and effect_match:
                        confidence += 0.4
                        evidence.append(
                            f"模式匹配: {cause_event['event'][:30]} → {effect_event['event'][:30]}"
                        )

                shared_characters = (
                    set(cause_event.get('characters', []))
                    & set(effect_event.get('characters', []))
                )
                if shared_characters:
                    confidence += 0.3
                    evidence.append(f"共享角色: {', '.join(shared_characters)}")

                if cause_event.get('location') == effect_event.get('location'):
                    confidence += 0.15
                    evidence.append(f"同地点: {cause_event['location']}")

                if chapter_gap <= 3:
                    confidence += 0.15
                    evidence.append(f"时间邻近(间隔{chapter_gap}章)")

                confidence = min(confidence, 1.0)

                if confidence >= 0.4:
                    self.link_counter += 1
                    link = CausalLink(
                        link_id=f"LINK_{self.link_counter:06d}",
                        cause_event=cause_event['event'][:100],
                        effect_event=effect_event['event'][:100],
                        cause_chapter=cause_event['chapter'],
                        effect_chapter=effect_event['chapter'],
                        confidence=round(confidence, 2),
                        evidence=evidence,
                        link_type=link_type,
                    )
                    self.causal_links[link.link_id] = link
                    new_links.append(link)

        return new_links

    def get_causal_chain(self, event_text: str,
                         direction: str = "both",
                         max_depth: int = 5) -> Dict:
        """获取事件的因果链

        direction: 'forward'(结果), 'backward'(原因), 'both'(双向)
        """
        chain = {
            "event": event_text,
            "causes": [],
            "effects": [],
            "full_chain": [],
        }

        for link in self.causal_links.values():
            if event_text[:30] in link.effect_event:
                chain["causes"].append({
                    "event": link.cause_event,
                    "chapter": link.cause_chapter,
                    "confidence": link.confidence,
                })
            if event_text[:30] in link.cause_event:
                chain["effects"].append({
                    "event": link.effect_event,
                    "chapter": link.effect_chapter,
                    "confidence": link.confidence,
                })

        visited = set()
        queue = [(event_text, 0, "root")]
        while queue and len(chain["full_chain"]) < max_depth * 2:
            current, depth, direction_tag = queue.pop(0)
            if current[:30] in visited or depth >= max_depth:
                continue
            visited.add(current[:30])

            chain["full_chain"].append({
                "event": current[:80],
                "depth": depth,
                "direction": direction_tag,
            })

            for link in self.causal_links.values():
                if current[:30] in link.cause_event:
                    queue.append((link.effect_event, depth + 1, "forward"))
                if current[:30] in link.effect_event:
                    queue.append((link.cause_event, depth + 1, "backward"))

        return chain

    def analyze_character_arc(self, character_name: str) -> Dict:
        """分析角色弧线 - 追踪角色在整本书中的成长轨迹"""
        profile = self.characters.get(character_name)
        if not profile:
            return {"error": f"未找到角色: {character_name}"}

        arc_points = []
        appearances = [
            e for e in self.plot_events
            if character_name in e.get('characters', [])
        ]
        appearances.sort(key=lambda e: e['chapter'])

        arc_stages = [
            (0, 0.1, "exposition", "登场亮相"),
            (0.1, 0.25, "setup", "建立目标"),
            (0.25, 0.4, "growth", "成长历练"),
            (0.4, 0.55, "crisis", "遭遇危机"),
            (0.55, 0.7, "transformation", "蜕变转折"),
            (0.7, 0.85, "mastery", "掌握力量"),
            (0.85, 1.0, "resolution", "结局归宿"),
        ]

        total_chapters = max(self.chapter_texts.keys()) if self.chapter_texts else 100

        for event in appearances:
            progress = event['chapter'] / max(total_chapters, 1)
            stage = "exposition"
            stage_label = "登场亮相"
            for low, high, s, label in arc_stages:
                if low <= progress < high:
                    stage = s
                    stage_label = label
                    break

            growth_score = progress * 100

            trait_changes = {}
            if profile.personality:
                trait_changes["personality"] = profile.personality[:3]
            if profile.abilities:
                trait_changes["abilities_count"] = len(profile.abilities)

            arc_point = CharacterArcPoint(
                character_name=character_name,
                chapter=event['chapter'],
                arc_stage=stage,
                trait_changes=trait_changes,
                key_events=[event['event'][:80]],
                growth_score=round(growth_score, 1),
            )
            arc_points.append(arc_point)

        if character_name not in self.character_arcs:
            self.character_arcs[character_name] = []
        self.character_arcs[character_name].extend(arc_points)

        return {
            "character": character_name,
            "role": profile.role,
            "total_appearances": len(appearances),
            "first_appearance": profile.first_appearance_chapter,
            "last_appearance": profile.last_appearance_chapter,
            "arc_stages": [
                {
                    "chapter": p.chapter,
                    "stage": p.arc_stage,
                    "growth": p.growth_score,
                    "events": p.key_events,
                }
                for p in arc_points
            ],
            "arc_completeness": self._evaluate_arc_completeness(arc_points),
        }

    def _evaluate_arc_completeness(self,
                                    arc_points: List[CharacterArcPoint]) -> str:
        """评估角色弧线完整度"""
        if not arc_points:
            return "无数据"

        stages_seen = set(p.arc_stage for p in arc_points)
        total_stages = 7

        if len(stages_seen) >= 6:
            return "完整"
        elif len(stages_seen) >= 4:
            return "较完整"
        elif len(stages_seen) >= 2:
            return "发展中"
        return "初始阶段"

    def detect_cross_chapter_patterns(self) -> Dict:
        """跨章节模式检测 - 发现重复使用的叙事模式"""
        patterns = {
            "repeated_phrases": defaultdict(list),
            "structure_patterns": defaultdict(list),
            "emotional_cycles": [],
            "pacing_cycles": [],
        }

        for ch, text in self.chapter_texts.items():
            phrases = re.findall(r'[\u4e00-\u9fff]{4,8}', text)
            phrase_counts = Counter(phrases)
            for phrase, count in phrase_counts.most_common(10):
                if count >= 3:
                    patterns["repeated_phrases"][phrase].append(ch)

        for ch, fp in self.style_fingerprints.items():
            if fp.dialogue_ratio > 0.4:
                patterns["structure_patterns"]["对话为主"].append(ch)
            elif fp.action_ratio > 0.3:
                patterns["structure_patterns"]["动作为主"].append(ch)
            elif fp.description_ratio > 0.3:
                patterns["structure_patterns"]["描写为主"].append(ch)

        if len(self.emotional_arc) >= 5:
            for i in range(len(self.emotional_arc) - 4):
                window = self.emotional_arc[i:i + 5]
                emotions = [p.dominant_emotion for p in window]
                if emotions == emotions[::-1]:
                    patterns["emotional_cycles"].append({
                        "start_chapter": window[0].chapter,
                        "end_chapter": window[-1].chapter,
                        "pattern": " → ".join(emotions),
                    })

        sorted_pacing = sorted(self.pacing_profiles.items())
        if len(sorted_pacing) >= 4:
            for i in range(len(sorted_pacing) - 3):
                window = sorted_pacing[i:i + 4]
                types = [p[1].pacing_type.value for p in window]
                if types[0] == types[2] and types[1] == types[3]:
                    patterns["pacing_cycles"].append({
                        "start_chapter": window[0][0],
                        "end_chapter": window[-1][0],
                        "pattern": " → ".join(types),
                    })

        return {
            "repeated_phrases": {
                phrase: {"count": len(chapters), "chapters": chapters[:5]}
                for phrase, chapters in patterns["repeated_phrases"].items()
                if len(chapters) >= 3
            },
            "structure_patterns": dict(patterns["structure_patterns"]),
            "emotional_cycles": patterns["emotional_cycles"][:5],
            "pacing_cycles": patterns["pacing_cycles"][:5],
        }

    # ================================================================
    # 自动检查系统 (Automatic Checking)
    # ================================================================

    def _init_auto_check_rules(self):
        """初始化自动检查规则"""
        default_rules = [
            ("ACR_001", "风格漂移检查", "style", "check_style_drift",
             ConsistencyLevel.NOTICEABLE_DRIFT, "on_chapter"),
            ("ACR_002", "时间线验证", "timeline", "verify_timeline",
             ConsistencyLevel.MINOR_DRIFT, "on_chapter"),
            ("ACR_003", "伏笔超期检查", "foreshadowing", "check_overdue_foreshadowing",
             ConsistencyLevel.NOTICEABLE_DRIFT, "on_chapter"),
            ("ACR_004", "节奏平衡检查", "pacing", "verify_pacing_balance",
             ConsistencyLevel.MINOR_DRIFT, "every_3_chapters"),
            ("ACR_005", "情感弧线检查", "emotional", "verify_emotional_consistency",
             ConsistencyLevel.MINOR_DRIFT, "every_5_chapters"),
            ("ACR_006", "冲突密度检查", "conflict", "verify_conflict_requirements",
             ConsistencyLevel.MINOR_DRIFT, "every_5_chapters"),
            ("ACR_007", "人物一致性扫描", "character", "find_character_inconsistencies",
             ConsistencyLevel.MINOR_DRIFT, "every_10_chapters"),
            ("ACR_008", "世界观规则验证", "world", "verify_all_world_rules",
             ConsistencyLevel.MAJOR_CONFLICT, "every_10_chapters"),
        ]

        for rule_id, name, category, func, threshold, schedule in default_rules:
            self.auto_check_rules[rule_id] = AutoCheckRule(
                rule_id=rule_id,
                name=name,
                category=category,
                check_function=func,
                severity_threshold=threshold,
                schedule=schedule,
            )

    def run_auto_checks(self, chapter: int,
                        rules: List[str] = None) -> Dict:
        """运行自动检查

        根据规则调度自动决定哪些检查需要执行
        """
        results = {
            "chapter": chapter,
            "timestamp": datetime.now().isoformat(),
            "checks_run": [],
            "total_issues_found": 0,
            "issues_by_severity": defaultdict(int),
        }

        target_rules = (
            [self.auto_check_rules[r] for r in rules if r in self.auto_check_rules]
            if rules
            else list(self.auto_check_rules.values())
        )

        for rule in target_rules:
            if not rule.enabled:
                continue

            should_run = False
            if rule.schedule == "on_chapter":
                should_run = True
            elif rule.schedule == "every_3_chapters":
                should_run = (chapter % 3 == 0)
            elif rule.schedule == "every_5_chapters":
                should_run = (chapter % 5 == 0)
            elif rule.schedule == "every_10_chapters":
                should_run = (chapter % 10 == 0)

            if not should_run:
                continue

            issues_before = len(self.issues)
            check_result = self._execute_check(rule, chapter)
            new_issues = len(self.issues) - issues_before

            rule.last_run_chapter = chapter
            rule.total_issues_found += new_issues

            results["checks_run"].append({
                "rule_id": rule.rule_id,
                "name": rule.name,
                "issues_found": new_issues,
                "details": check_result,
            })
            results["total_issues_found"] += new_issues

            for issue in self.issues[issues_before:]:
                results["issues_by_severity"][issue.severity.value] += 1

        return results

    def _execute_check(self, rule: AutoCheckRule, chapter: int) -> Any:
        """执行具体检查"""
        func_map = {
            "check_style_drift": lambda: self.check_style_drift(chapter),
            "verify_timeline": lambda: self.verify_timeline(),
            "check_overdue_foreshadowing": lambda: self.get_overdue_foreshadowing(chapter),
            "verify_pacing_balance": lambda: self.verify_pacing_balance(),
            "verify_emotional_consistency": lambda: self.verify_emotional_consistency(),
            "verify_conflict_requirements": lambda: self.verify_conflict_requirements(),
            "find_character_inconsistencies": lambda: self.find_character_inconsistencies(),
            "verify_all_world_rules": lambda: self._verify_all_world_rules(),
        }

        func = func_map.get(rule.check_function)
        if func:
            return func()
        return None

    def _verify_all_world_rules(self) -> List[ConsistencyIssue]:
        """验证所有世界观规则"""
        issues = []
        for rule in self.world_rules.values():
            if rule.last_verified_chapter < rule.established_chapter:
                issues.append(ConsistencyIssue(
                    issue_id=f"world_{self.issue_counter + 1}",
                    category="世界观一致性",
                    severity=ConsistencyLevel.MINOR_DRIFT,
                    description=f"规则「{rule.rule}」自第{rule.established_chapter}章建立后未再验证",
                    chapter=rule.established_chapter,
                    suggestion="在近期章节中确认此规则仍然有效",
                ))
                self.issue_counter += 1
        self.issues.extend(issues)
        return issues

    def batch_validate(self, chapters: List[int]) -> Dict:
        """批量验证 - 对多个章节一次性运行全部检查"""
        results = {
            "chapters": chapters,
            "timestamp": datetime.now().isoformat(),
            "per_chapter": {},
            "summary": {
                "total_issues": 0,
                "critical_issues": 0,
                "chapters_with_issues": 0,
            },
        }

        for ch in sorted(chapters):
            ch_result = self.run_auto_checks(ch)
            results["per_chapter"][ch] = ch_result
            results["summary"]["total_issues"] += ch_result["total_issues_found"]
            if ch_result["total_issues_found"] > 0:
                results["summary"]["chapters_with_issues"] += 1

        results["summary"]["critical_issues"] = sum(
            1 for i in self.issues
            if i.severity == ConsistencyLevel.MAJOR_CONFLICT and not i.resolved
        )

        return results

    def auto_fix_suggestions(self, issue_id: str) -> Dict:
        """为指定问题生成自动修复建议"""
        issue = None
        for i in self.issues:
            if i.issue_id == issue_id:
                issue = i
                break

        if not issue:
            return {"error": f"未找到问题: {issue_id}"}

        suggestions = {
            "issue": issue.description,
            "category": issue.category,
            "auto_fixable": False,
            "fix_suggestions": [],
            "related_data": {},
        }

        if issue.category == "人物一致性":
            suggestions["auto_fixable"] = True
            suggestions["fix_suggestions"].append(
                "自动统一外貌描述为最近一次出现的版本"
            )
            suggestions["fix_suggestions"].append(
                "在人物档案中标记此特征为「可变」"
            )

        elif issue.category == "风格漂移":
            suggestions["auto_fixable"] = False
            suggestions["fix_suggestions"].append(
                f"建议重写第{issue.chapter}章中偏离风格的部分"
            )
            suggestions["fix_suggestions"].append(
                "参考前5章的风格参数进行调整"
            )
            if issue.chapter in self.style_fingerprints:
                fp = self.style_fingerprints[issue.chapter]
                suggestions["related_data"]["current_style"] = {
                    "dialogue_ratio": fp.dialogue_ratio,
                    "avg_sentence_length": fp.avg_sentence_length,
                }

        elif issue.category == "时间线":
            suggestions["auto_fixable"] = True
            suggestions["fix_suggestions"].append(
                "自动添加地点切换过渡段落模板"
            )
            suggestions["fix_suggestions"].append(
                "在章节开头插入时间/地点标记"
            )

        elif issue.category == "实力体系":
            suggestions["auto_fixable"] = True
            suggestions["fix_suggestions"].append(
                "自动将实力描述修正为历史最高等级"
            )

        elif issue.category == "冲突密度":
            suggestions["auto_fixable"] = False
            suggestions["fix_suggestions"].append(
                "建议在章节中插入小型冲突或悬念"
            )
            suggestions["fix_suggestions"].append(
                "可添加: 新对手出现 / 意外消息 / 能力限制 / 时间压力"
            )

        return suggestions

    def resolve_issue(self, issue_id: str) -> bool:
        """标记问题为已解决"""
        for issue in self.issues:
            if issue.issue_id == issue_id:
                issue.resolved = True
                return True
        return False

    def get_check_schedule_status(self) -> Dict:
        """获取检查调度状态"""
        return {
            "total_rules": len(self.auto_check_rules),
            "enabled_rules": sum(1 for r in self.auto_check_rules.values() if r.enabled),
            "rules": [
                {
                    "id": r.rule_id,
                    "name": r.name,
                    "schedule": r.schedule,
                    "enabled": r.enabled,
                    "last_run": r.last_run_chapter,
                    "total_issues": r.total_issues_found,
                }
                for r in self.auto_check_rules.values()
            ],
        }

    # ================================================================
    # 记忆压缩系统 (Memory Compression)
    # ================================================================

    def compress_chapter_range(self, start_chapter: int,
                               end_chapter: int,
                               compression_level: str = "medium") -> MemorySnapshot:
        """压缩章节范围 - 将多章内容压缩为结构化摘要

        compression_level: 'light'(保留50%), 'medium'(保留25%), 'deep'(保留10%)
        """
        self.snapshot_counter += 1
        snapshot_id = f"SNAP_{self.snapshot_counter:06d}"

        chapters_in_range = [
            ch for ch in sorted(self.chapter_texts.keys())
            if start_chapter <= ch <= end_chapter
        ]

        total_words = sum(
            len(self.chapter_texts.get(ch, "")) for ch in chapters_in_range
        )

        key_characters = []
        for name, profile in self.characters.items():
            if start_chapter <= profile.first_appearance_chapter <= end_chapter:
                key_characters.append(f"{name}({profile.role})")
            elif (profile.last_appearance_chapter >= start_chapter
                  and profile.first_appearance_chapter <= end_chapter):
                if name not in [kc.split("(")[0] for kc in key_characters]:
                    key_characters.append(f"{name}({profile.role})")

        key_events = []
        for event in self.plot_events:
            if start_chapter <= event['chapter'] <= end_chapter:
                key_events.append(
                    f"第{event['chapter']}章: {event['event'][:80]}"
                )

        key_settings = []
        for ch in chapters_in_range:
            if ch in self.timeline:
                for loc in self.timeline[ch].get("locations", set()):
                    if loc not in key_settings:
                        key_settings.append(loc)

        unresolved_threads = []
        for fs in self.foreshadowings.values():
            if (fs.planted_chapter <= end_chapter
                    and fs.status in [ForeshadowStatus.PLANTED, ForeshadowStatus.HINTED]):
                unresolved_threads.append(
                    f"[{fs.type}] {fs.description[:80]} (埋设第{fs.planted_chapter}章)"
                )

        summary = self._generate_range_summary(
            start_chapter, end_chapter, chapters_in_range,
            key_characters, key_events, compression_level
        )

        compression_ratios = {"light": 0.5, "medium": 0.25, "deep": 0.1}
        ratio = compression_ratios.get(compression_level, 0.25)

        snapshot = MemorySnapshot(
            snapshot_id=snapshot_id,
            chapter_range=(start_chapter, end_chapter),
            summary=summary,
            key_characters=key_characters[:15],
            key_events=key_events[:20],
            key_settings=key_settings[:10],
            unresolved_threads=unresolved_threads[:10],
            word_count=total_words,
            compression_ratio=ratio,
            created_at=datetime.now().isoformat(),
        )

        self.memory_snapshots[snapshot_id] = snapshot
        return snapshot

    def _generate_range_summary(self, start: int, end: int,
                                 chapters: List[int],
                                 characters: List[str],
                                 events: List[str],
                                 level: str) -> str:
        """生成章节范围摘要"""
        parts = [f"第{start}-{end}章摘要 (共{len(chapters)}章)"]

        if characters:
            parts.append(f"主要人物: {', '.join(characters[:8])}")

        if events:
            level_limits = {"light": 10, "medium": 6, "deep": 3}
            limit = level_limits.get(level, 6)
            parts.append("关键事件:")
            for event in events[:limit]:
                parts.append(f"  • {event}")

        style_info = []
        for ch in chapters:
            if ch in self.style_fingerprints:
                fp = self.style_fingerprints[ch]
                style_info.append(fp)
        if style_info:
            avg_dialogue = sum(s.dialogue_ratio for s in style_info) / len(style_info)
            avg_action = sum(s.action_ratio for s in style_info) / len(style_info)
            parts.append(f"风格特征: 对话占比{avg_dialogue:.1%}, 动作密度{avg_action:.1%}")

        return "\n".join(parts)

    def progressive_summarize(self, chapter: int,
                              levels: List[str] = None) -> Dict:
        """渐进式总结 - 对内容进行多层压缩

        层级:
        - L1: 详细摘要 (保留80%关键信息)
        - L2: 中等摘要 (保留50%)
        - L3: 核心摘要 (保留20%)
        - L4: 一句话总结
        """
        if levels is None:
            levels = ["L1", "L2", "L3", "L4"]

        text = self.chapter_texts.get(chapter, "")
        if not text:
            return {"error": f"第{chapter}章无原文数据"}

        sentences = re.split(r'[。！？\n]+', text)
        sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 5]

        summaries = {}

        if "L1" in levels:
            key_sentences = self._extract_key_sentences(sentences, top_n=15)
            summaries["L1_详细摘要"] = "。".join(key_sentences) + "。"

        if "L2" in levels:
            key_sentences = self._extract_key_sentences(sentences, top_n=8)
            summaries["L2_中等摘要"] = "。".join(key_sentences) + "。"

        if "L3" in levels:
            key_sentences = self._extract_key_sentences(sentences, top_n=3)
            summaries["L3_核心摘要"] = "。".join(key_sentences) + "。"

        if "L4" in levels:
            one_liner = self._generate_one_liner(chapter, sentences)
            summaries["L4_一句话"] = one_liner

        return {
            "chapter": chapter,
            "original_length": len(text),
            "sentence_count": len(sentences),
            "summaries": summaries,
        }

    def _extract_key_sentences(self, sentences: List[str],
                                top_n: int = 10) -> List[str]:
        """提取关键句子"""
        important_markers = [
            "突然", "然而", "但是", "终于", "竟然", "原来",
            "发现", "决定", "突破", "觉醒", "获得", "失去",
            "战斗", "对决", "危机", "秘密", "真相",
        ]

        dialogue_pattern = re.compile(r'[""「」『』]')

        scored = []
        for sent in sentences:
            score = 0.0
            for marker in important_markers:
                if marker in sent:
                    score += 1.0
            if dialogue_pattern.search(sent):
                score += 0.5
            if len(sent) > 30:
                score += 0.3
            scored.append((score, sent))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [s for _, s in scored[:top_n]]

    def _generate_one_liner(self, chapter: int,
                            sentences: List[str]) -> str:
        """生成一句话总结"""
        characters_in_chapter = set()
        for event in self.plot_events:
            if event['chapter'] == chapter:
                for char in event.get('characters', []):
                    characters_in_chapter.add(char)

        char_str = "、".join(list(characters_in_chapter)[:3]) if characters_in_chapter else "主角"

        if chapter in self.style_fingerprints:
            fp = self.style_fingerprints[chapter]
            if fp.action_ratio > 0.3:
                action_type = "战斗/行动"
            elif fp.dialogue_ratio > 0.3:
                action_type = "对话/交流"
            elif fp.description_ratio > 0.2:
                action_type = "探索/观察"
            else:
                action_type = "推进剧情"
        else:
            action_type = "推进剧情"

        key_sents = self._extract_key_sentences(sentences, top_n=1)
        core_event = key_sents[0][:60] if key_sents else "剧情发展"

        return f"第{chapter}章: {char_str}在{action_type}中, {core_event}"

    def get_memory_snapshot(self, snapshot_id: str) -> Optional[MemorySnapshot]:
        """获取记忆快照"""
        return self.memory_snapshots.get(snapshot_id)

    def get_all_snapshots(self) -> List[Dict]:
        """获取所有记忆快照"""
        return [
            {
                "id": s.snapshot_id,
                "range": f"第{s.chapter_range[0]}-{s.chapter_range[1]}章",
                "word_count": s.word_count,
                "compression": f"{s.compression_ratio:.0%}",
                "characters": len(s.key_characters),
                "events": len(s.key_events),
                "created": s.created_at,
            }
            for s in sorted(
                self.memory_snapshots.values(),
                key=lambda x: x.chapter_range[0]
            )
        ]

    def recall_from_snapshots(self, query: str,
                              max_snapshots: int = 5) -> List[Dict]:
        """从压缩快照中召回相关信息"""
        results = []
        for snap in self.memory_snapshots.values():
            score = 0.0
            matched = []

            if query in snap.summary:
                score += 1.0
                matched.append("摘要匹配")

            for char in snap.key_characters:
                if query in char:
                    score += 0.6
                    matched.append(f"人物: {char}")

            for event in snap.key_events:
                if query in event:
                    score += 0.5
                    matched.append(f"事件: {event[:50]}")

            for thread in snap.unresolved_threads:
                if query in thread:
                    score += 0.4
                    matched.append(f"线索: {thread[:50]}")

            if score > 0:
                results.append({
                    "snapshot_id": snap.snapshot_id,
                    "range": f"第{snap.chapter_range[0]}-{snap.chapter_range[1]}章",
                    "score": min(score, 2.0),
                    "matched": matched[:5],
                    "summary": snap.summary[:300],
                    "key_events": snap.key_events[:5],
                })

        results.sort(key=lambda r: r["score"], reverse=True)
        return results[:max_snapshots]

    # ================================================================
    # 持久化
    # ================================================================

    def persist(self):
        """持久化全部数据"""
        data = {
            "novel_title": self.novel_title,
            "total_words_processed": self.total_words_processed,
            "fs_counter": self.fs_counter,
            "issue_counter": self.issue_counter,
            "characters": {
                name: {
                    "name": p.name,
                    "aliases": p.aliases,
                    "role": p.role,
                    "gender": p.gender,
                    "age": p.age,
                    "appearance": p.appearance,
                    "personality": p.personality,
                    "abilities": p.abilities,
                    "catchphrases": p.catchphrases,
                    "speech_style": p.speech_style,
                    "relationships": p.relationships,
                    "first_appearance_chapter": p.first_appearance_chapter,
                    "last_appearance_chapter": p.last_appearance_chapter,
                    "status": p.status,
                    "notes": p.notes,
                }
                for name, p in self.characters.items()
            },
            "foreshadowings": {
                fs_id: {
                    "fs_id": f.fs_id,
                    "description": f.description,
                    "planted_chapter": f.planted_chapter,
                    "expected_payoff_chapter": f.expected_payoff_chapter,
                    "actual_payoff_chapter": f.actual_payoff_chapter,
                    "status": f.status.value,
                    "type": f.type,
                    "importance": f.importance,
                    "related_characters": f.related_characters,
                    "tags": f.tags,
                    "created_at": f.created_at,
                    "resolved_at": f.resolved_at,
                }
                for fs_id, f in self.foreshadowings.items()
            },
            "style_fingerprints": {
                str(ch): {
                    "chapter": fp.chapter,
                    "avg_sentence_length": fp.avg_sentence_length,
                    "sentence_length_std": fp.sentence_length_std,
                    "dialogue_ratio": fp.dialogue_ratio,
                    "description_ratio": fp.description_ratio,
                    "action_ratio": fp.action_ratio,
                    "inner_thought_ratio": fp.inner_thought_ratio,
                    "paragraph_count": fp.paragraph_count,
                    "avg_paragraph_length": fp.avg_paragraph_length,
                    "top_words": fp.top_words,
                    "emotional_curve": fp.emotional_curve,
                    "unique_word_count": fp.unique_word_count,
                    "total_word_count": fp.total_word_count,
                    "computed_at": fp.computed_at,
                }
                for ch, fp in self.style_fingerprints.items()
            },
            "issues": [
                {
                    "issue_id": i.issue_id,
                    "category": i.category,
                    "severity": i.severity.value,
                    "description": i.description,
                    "chapter": i.chapter,
                    "related_chapters": i.related_chapters,
                    "suggestion": i.suggestion,
                    "resolved": i.resolved,
                }
                for i in self.issues
            ],
            "plot_events": self.plot_events,
            "world_settings": self.world_settings,
            "conversations": self.conversations,
            "emotional_arc": [
                {
                    "chapter": p.chapter,
                    "dominant_emotion": p.dominant_emotion,
                    "emotion_scores": p.emotion_scores,
                    "intensity": p.intensity,
                    "transition_from_prev": p.transition_from_prev,
                }
                for p in self.emotional_arc
            ],
            "pacing_profiles": {
                str(ch): {
                    "chapter": p.chapter,
                    "pacing_type": p.pacing_type.value,
                    "action_density": p.action_density,
                    "dialogue_density": p.dialogue_density,
                    "description_density": p.description_density,
                    "paragraph_variation": p.paragraph_variation,
                }
                for ch, p in self.pacing_profiles.items()
            },
            "dialogue_fingerprints": {
                name: {
                    "character_name": fp.character_name,
                    "avg_sentence_length": fp.avg_sentence_length,
                    "exclamation_ratio": fp.exclamation_ratio,
                    "question_ratio": fp.question_ratio,
                    "catchphrase_usage": fp.catchphrase_usage,
                    "formality_level": fp.formality_level,
                    "unique_words": list(fp.unique_words),
                }
                for name, fp in self.dialogue_fingerprints.items()
            },
            "world_rules": {
                rid: {
                    "rule_id": r.rule_id,
                    "category": r.category,
                    "rule": r.rule,
                    "established_chapter": r.established_chapter,
                    "exceptions": r.exceptions,
                    "last_verified_chapter": r.last_verified_chapter,
                }
                for rid, r in self.world_rules.items()
            },
            "chapter_quality_scores": self.chapter_quality_scores,
            "conflict_density": self.conflict_density,
            "rule_counter": self.rule_counter,
            "timeline": {
                str(ch): {
                    "events": data["events"],
                    "locations": list(data["locations"]),
                    "characters": list(data["characters"]),
                }
                for ch, data in self.timeline.items()
            },
            "saved_at": datetime.now().isoformat(),
        }

        data["causal_links"] = {
            lid: {
                "link_id": l.link_id,
                "cause_event": l.cause_event,
                "effect_event": l.effect_event,
                "cause_chapter": l.cause_chapter,
                "effect_chapter": l.effect_chapter,
                "confidence": l.confidence,
                "evidence": l.evidence,
                "link_type": l.link_type,
            }
            for lid, l in self.causal_links.items()
        }

        data["character_arcs"] = {
            name: [
                {
                    "character_name": p.character_name,
                    "chapter": p.chapter,
                    "arc_stage": p.arc_stage,
                    "trait_changes": p.trait_changes,
                    "key_events": p.key_events,
                    "growth_score": p.growth_score,
                }
                for p in points
            ]
            for name, points in self.character_arcs.items()
        }

        data["memory_snapshots"] = {
            sid: {
                "snapshot_id": s.snapshot_id,
                "chapter_range": list(s.chapter_range),
                "summary": s.summary,
                "key_characters": s.key_characters,
                "key_events": s.key_events,
                "key_settings": s.key_settings,
                "unresolved_threads": s.unresolved_threads,
                "word_count": s.word_count,
                "compression_ratio": s.compression_ratio,
                "created_at": s.created_at,
            }
            for sid, s in self.memory_snapshots.items()
        }

        data["auto_check_rules"] = {
            rid: {
                "rule_id": r.rule_id,
                "name": r.name,
                "category": r.category,
                "check_function": r.check_function,
                "severity_threshold": r.severity_threshold.value,
                "enabled": r.enabled,
                "schedule": r.schedule,
                "last_run_chapter": r.last_run_chapter,
                "total_issues_found": r.total_issues_found,
            }
            for rid, r in self.auto_check_rules.items()
        }

        data["chapter_texts"] = self.chapter_texts
        data["link_counter"] = self.link_counter
        data["snapshot_counter"] = self.snapshot_counter
        data["retrieval_counter"] = self.retrieval_counter

        filepath = os.path.join(self.storage_dir, "novel_memory.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _load_all(self):
        """从磁盘加载"""
        filepath = os.path.join(self.storage_dir, "novel_memory.json")
        if not os.path.exists(filepath):
            return

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.novel_title = data.get("novel_title", self.novel_title)
            self.total_words_processed = data.get("total_words_processed", 0)
            self.fs_counter = data.get("fs_counter", 0)
            self.issue_counter = data.get("issue_counter", 0)

            for name, cd in data.get("characters", {}).items():
                self.characters[name] = CharacterProfile(**cd)

            for fs_id, fd in data.get("foreshadowings", {}).items():
                fd["status"] = ForeshadowStatus(fd["status"])
                self.foreshadowings[fs_id] = Foreshadowing(**fd)

            for ch_str, fd in data.get("style_fingerprints", {}).items():
                self.style_fingerprints[int(ch_str)] = StyleFingerprint(**fd)

            for idata in data.get("issues", []):
                idata["severity"] = ConsistencyLevel(idata["severity"])
                self.issues.append(ConsistencyIssue(**idata))

            self.plot_events = data.get("plot_events", [])
            self.world_settings = data.get("world_settings", {})
            self.conversations = data.get("conversations", [])

            for ed in data.get("emotional_arc", []):
                self.emotional_arc.append(EmotionalArcPoint(**ed))

            for ch_str, pd in data.get("pacing_profiles", {}).items():
                pd["pacing_type"] = PacingType(pd["pacing_type"])
                self.pacing_profiles[int(ch_str)] = PacingProfile(**pd)

            for name, fd in data.get("dialogue_fingerprints", {}).items():
                fd["unique_words"] = set(fd.get("unique_words", []))
                self.dialogue_fingerprints[name] = DialogueFingerprint(**fd)

            for rid, rd in data.get("world_rules", {}).items():
                self.world_rules[rid] = WorldRule(**rd)

            self.chapter_quality_scores = data.get("chapter_quality_scores", {})
            self.conflict_density = data.get("conflict_density", {})
            self.rule_counter = data.get("rule_counter", 0)

            for lid, ld in data.get("causal_links", {}).items():
                self.causal_links[lid] = CausalLink(**ld)

            for name, points in data.get("character_arcs", {}).items():
                self.character_arcs[name] = [
                    CharacterArcPoint(**p) for p in points
                ]

            for sid, sd in data.get("memory_snapshots", {}).items():
                sd["chapter_range"] = tuple(sd["chapter_range"])
                self.memory_snapshots[sid] = MemorySnapshot(**sd)

            for rid, rd in data.get("auto_check_rules", {}).items():
                rd["severity_threshold"] = ConsistencyLevel(rd["severity_threshold"])
                self.auto_check_rules[rid] = AutoCheckRule(**rd)

            self.chapter_texts = data.get("chapter_texts", {})
            self.chapter_texts = {
                int(k): v for k, v in self.chapter_texts.items()
            }
            self.link_counter = data.get("link_counter", 0)
            self.snapshot_counter = data.get("snapshot_counter", 0)
            self.retrieval_counter = data.get("retrieval_counter", 0)

            for ch_str, td in data.get("timeline", {}).items():
                self.timeline[int(ch_str)] = {
                    "events": td["events"],
                    "locations": set(td["locations"]),
                    "characters": set(td["characters"]),
                }

        except (json.JSONDecodeError, KeyError, TypeError) as e:
            print(f"  ⚠️ 记忆加载失败: {e}，使用空白记忆")


if __name__ == "__main__":
    print("=" * 60)
    print("📚 长篇小说记忆一致性验证系统测试")
    print("=" * 60)

    nmm = NovelMemoryManager(novel_title="测试仙侠")

    ch1_text = """
    叶青云站在青云宗山门前，望着巍峨的九座主峰，心中豪情万丈。
    "从今天起，我叶青云就是青云宗的弟子了！"他握紧拳头，眼中闪烁着坚定的光芒。
    身旁的苏婉儿微微一笑："叶师兄，以后还请多多关照。"
    叶青云转过身，看着这位神秘的少女，点了点头。
    远处，一道剑光划破天际，那是宗门长老在巡视。
    """

    ch2_text = """
    叶青云缓缓地站起身，宛如一只刚刚破茧而出的蝴蝶，心中不禁激动万分。
    仿佛天地都在为他欢呼，眼前的景象十分壮观，格外震撼人心。
    这一切似乎都像是一场梦境，渐渐地，叶青云才相信这是真的。
    他微微一笑，心中暗想，自己的努力终究没有白费。
    极其艰难的旅程，非常辛苦的奋斗，终于换来了此刻的成功。
    """

    print("\n【风格指纹计算】")
    fp1 = nmm.compute_style_fingerprint(1, ch1_text)
    fp2 = nmm.compute_style_fingerprint(2, ch2_text)
    print(f"  第1章: 句长={fp1.avg_sentence_length}, 对话占比={fp1.dialogue_ratio:.2%}")
    print(f"  第2章: 句长={fp2.avg_sentence_length}, 对话占比={fp2.dialogue_ratio:.2%}")

    print("\n【风格漂移检测】")
    drift_issues = nmm.check_style_drift(2)
    for issue in drift_issues:
        print(f"  ⚠️ {issue.description}")

    print("\n【人物注册】")
    nmm.register_character("叶青云", role="主角", gender="男", age=18,
                           personality=["坚毅", "果敢", "重情义"],
                           first_appearance_chapter=1)
    nmm.register_character("苏婉儿", role="女主", gender="女", age=17,
                           personality=["神秘", "温柔", "聪慧"],
                           first_appearance_chapter=1)
    print(f"  已注册 {len(nmm.characters)} 个角色")

    print("\n【人物一致性检查】")
    char_issues = nmm.check_character_consistency("叶青云", 5, {
        "appearance": {"眼睛": "蓝色", "头发": "白色"}
    })
    nmm.register_character("叶青云", appearance={"眼睛": "黑色", "头发": "黑色"})
    char_issues2 = nmm.check_character_consistency("叶青云", 10, {
        "appearance": {"眼睛": "蓝色"}
    })
    for issue in char_issues2:
        print(f"  ⚠️ {issue.description}")

    print("\n【伏笔管理】")
    fs1 = nmm.plant_foreshadowing("苏婉儿的真实身份是魔教圣女", 1, 50,
                                  fs_type="identity", importance=9,
                                  related_characters=["苏婉儿"])
    fs2 = nmm.plant_foreshadowing("叶青云的玉佩蕴含上古传承", 3, 30,
                                  fs_type="power_up", importance=8,
                                  related_characters=["叶青云"])
    print(f"  已埋设 {len(nmm.foreshadowings)} 个伏笔")
    overdue = nmm.get_overdue_foreshadowing(60)
    print(f"  超期未回收: {len(overdue)} 个")
    for o in overdue:
        print(f"    ⚠️ {o.fs_id}: {o.description} (预期第{o.expected_payoff_chapter}章回收)")

    print("\n【剧情事件记录】")
    nmm.record_plot_event(1, "叶青云加入青云宗", "entry", ["叶青云"], "青云宗山门")
    nmm.record_plot_event(1, "叶青云与苏婉儿初次见面", "meeting", ["叶青云", "苏婉儿"], "青云宗山门")
    nmm.record_plot_event(5, "叶青云进入秘境", "adventure", ["叶青云"], "上古秘境")
    print(f"  已记录 {len(nmm.plot_events)} 个事件")

    print("\n【时间线验证】")
    timeline_issues = nmm.verify_timeline()
    for issue in timeline_issues:
        print(f"  ⚠️ {issue.description}")

    print("\n【综合报告】")
    report = nmm.get_comprehensive_report()
    print(f"  总字数: {report['total_words']}")
    print(f"  角色数: {report['characters']['total']}")
    print(f"  问题数: {report['issues']['total']} (未解决: {report['issues']['unresolved']})")
    print(f"  问题分类: {dict(report['issues']['by_category'])}")

    nmm.persist()
    print("\n✅ 数据已持久化")
