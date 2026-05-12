#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 词汇疲劳检测系统 — Vocabulary Fatigue Detector

核心功能:
1. 词汇频率追踪 — 跨章节追踪词语使用频率
2. 疲劳词检测 — 识别过度使用的词汇和短语
3. 陈词滥调检测 — 识别网文常见套话
4. 句式重复检测 — 检测重复的句子开头和段落结构
5. 词汇多样性评估 — Type-Token Ratio 等指标
6. 替换建议 — 为疲劳词提供替代方案
"""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


@dataclass
class FatigueWord:
    word: str
    total_count: int
    chapters_appeared: List[int]
    fatigue_level: str
    category: str
    suggestions: List[str] = field(default_factory=list)
    first_seen_chapter: int = 0
    last_seen_chapter: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "word": self.word,
            "total_count": self.total_count,
            "chapters_appeared": self.chapters_appeared,
            "fatigue_level": self.fatigue_level,
            "category": self.category,
            "suggestions": self.suggestions,
            "first_seen_chapter": self.first_seen_chapter,
            "last_seen_chapter": self.last_seen_chapter,
        }


@dataclass
class ChapterVocabularyStats:
    chapter: int
    total_chars: int
    total_words: int
    unique_chars: int
    unique_words: int
    type_token_ratio: float
    top_repeated_words: List[Tuple[str, int]]
    top_repeated_bigrams: List[Tuple[str, int]]
    sentence_starter_repetition: Dict[str, int]
    paragraph_opener_repetition: Dict[str, int]
    cliche_count: int
    fatigue_score: float
    created_at: str = field(default_factory=_utc_now_iso)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "chapter": self.chapter,
            "total_chars": self.total_chars,
            "total_words": self.total_words,
            "unique_chars": self.unique_chars,
            "unique_words": self.unique_words,
            "type_token_ratio": round(self.type_token_ratio, 4),
            "top_repeated_words": [
                {"word": w, "count": c} for w, c in self.top_repeated_words[:15]
            ],
            "top_repeated_bigrams": [
                {"bigram": b, "count": c} for b, c in self.top_repeated_bigrams[:10]
            ],
            "sentence_starter_repetition": dict(
                sorted(self.sentence_starter_repetition.items(), key=lambda x: -x[1])[:10]
            ),
            "paragraph_opener_repetition": dict(
                sorted(self.paragraph_opener_repetition.items(), key=lambda x: -x[1])[:10]
            ),
            "cliche_count": self.cliche_count,
            "fatigue_score": round(self.fatigue_score, 1),
            "created_at": self.created_at,
        }


class FatigueDetector:
    """词汇疲劳检测器"""

    CLICHE_PATTERNS: List[Tuple[str, str, str]] = [
        (r"一股.{1,6}气息", "气息模板", "用具体感官描写替代抽象'气息'"),
        (r"眼中闪过.{1,8}光芒", "眼神模板", "用微表情或动作替代眼神描写"),
        (r"心中.{1,6}(?:一|的)(?:震|动|惊|凛|暖|寒|痛|喜|怒|悲)", "心中X模板", "用身体反应替代心理描述"),
        (r"嘴角.{1,6}(?:扬|翘|抽|扯|勾)", "嘴角模板", "用更独特的表情描写替代"),
        (r"深吸.{1,4}口气", "深吸气模板", "用其他紧张/放松的身体语言替代"),
        (r"不由.{1,4}(?:得|地|的)", "不由地模板", "删除或替换为具体动作"),
        (r"缓缓.{1,4}(?:地|的)", "缓缓地模板", "用具体速度描写替代"),
        (r"淡淡.{1,4}(?:地|的|一笑|说道|开口)", "淡淡地模板", "用具体语气描写替代"),
        (r"微微.{1,4}(?:一|地|的)(?:笑|点头|皱眉|摇头|叹息)", "微微X模板", "用更精确的动作描写替代"),
        (r"目光.{1,6}(?:落|扫|看|望|盯|凝|投)", "目光模板", "用头部/身体动作替代目光描写"),
        (r"沉默.{1,6}(?:片刻|良久|一会儿|了一阵)", "沉默模板", "用具体的时间或动作描写替代"),
        (r"气氛.{1,6}(?:凝重|尴尬|紧张|压抑|诡异|微妙)", "气氛模板", "通过角色反应间接展示气氛"),
        (r"不知.{1,6}(?:过了多久|什么时候|为什么|如何是好)", "不知X模板", "用具体描写替代模糊表达"),
        (r"仿佛.{1,10}(?:一切|整个世界|时间|天地)", "仿佛模板", "用具体比喻替代模糊的'仿佛'"),
        (r"一股.{1,6}(?:暖流|寒流|力量|冲动|勇气)", "一股X模板", "用具体身体感受替代"),
        (r"瞳孔.{1,4}(?:微缩|放大|一缩|猛缩)", "瞳孔模板", "用面部整体反应替代"),
        (r"心头.{1,4}(?:一|微|狂|猛)(?:震|跳|颤|动|热|凉)", "心头X模板", "用全身反应替代局部描写"),
        (r"脑海.{1,6}(?:浮现|闪过|回荡|响起|一片空白)", "脑海模板", "用具体回忆或感受替代"),
        (r"下意识.{1,6}(?:地|的|摸了摸|看向|后退|握紧)", "下意识模板", "删除'下意识'，直接写动作"),
        (r"不知为何.{1,10}", "不知为何模板", "删除或给出具体原因"),
    ]

    SENTENCE_STARTER_PATTERNS: List[str] = [
        r"^(?:他|她|它|他们|她们)",
        r"^(?:这时|此刻|此时|当下|现在)",
        r"^(?:突然|忽然|猛地|骤然)",
        r"^(?:只见|只听得|只感到|只觉得)",
        r"^(?:原来|其实|事实上|实际上)",
        r"^(?:不过|但是|然而|可是|却)",
        r"^(?:于是|接着|然后|随后|之后)",
        r"^(?:因为|所以|因此|故而)",
        r"^(?:如果|倘若|假如|若是)",
        r"^(?:虽然|尽管|即便|就算)",
        r"^(?:在|从|对|把|被|让|给)",
        r"^(?:一个|一种|一股|一阵|一片)",
    ]

    FATIGUE_WORD_CATEGORIES: Dict[str, List[str]] = {
        "连接词": ["然而", "但是", "不过", "因此", "所以", "于是", "接着", "然后", "随后",
                   "此外", "另外", "同时", "与此同时", "另一方面", "不仅如此"],
        "程度副词": ["非常", "十分", "极其", "格外", "特别", "相当", "颇为", "异常",
                     "无比", "极度", "万分", "甚是"],
        "模糊词": ["似乎", "仿佛", "好像", "大概", "或许", "也许", "可能", "隐约",
                   "某种", "某些", "某种程度", "某种意义上"],
        "神态词": ["微微一笑", "淡淡一笑", "苦笑", "冷笑", "笑了笑", "笑道",
                   "皱眉", "眉头一皱", "眉头微皱", "眉头紧锁"],
        "动作词": ["缓缓", "慢慢", "轻轻", "重重", "狠狠", "猛地", "突然",
                   "转身", "回头", "抬头", "低头", "点头", "摇头"],
        "心理词": ["心想", "暗想", "心中", "心里", "心底", "内心深处",
                   "不由得", "忍不住", "不禁", "不由自主"],
        "视觉词": ["看到", "看见", "望去", "望去只见", "映入眼帘",
                   "出现在眼前", "眼前", "目光所及"],
        "听觉词": ["听到", "听见", "传来", "响起", "回荡", "回响"],
    }

    REPLACEMENT_SUGGESTIONS: Dict[str, List[str]] = {
        "然而": ["可", "但", "偏偏", "谁料", "哪知", "不料", "谁知"],
        "但是": ["可", "不过", "只是", "偏偏", "哪想到"],
        "因此": ["于是", "就这样", "便", "自然", "顺理成章地"],
        "突然": ["猛地", "骤然", "霍地", "霎时", "陡然", "冷不丁"],
        "缓缓": ["慢慢", "徐徐", "款款", "不紧不慢地", "一步一步地"],
        "似乎": ["好像", "仿佛", "隐约", "恍惚间", "依稀"],
        "非常": ["极", "甚", "格外", "出奇地", "惊人地"],
        "微微一笑": ["嘴角微扬", "轻笑一声", "抿嘴", "莞尔", "唇角一勾"],
        "心想": ["暗忖", "思忖", "转念", "心道", "暗自盘算"],
        "看到": ["望见", "瞥见", "瞅见", "映入眼帘的", "目光所及之处"],
        "听到": ["耳畔传来", "隐约听见", "传入耳中", "只听", "闻得"],
        "转身": ["回身", "扭身", "旋身", "掉头", "折身"],
        "点头": ["颔首", "应了一声", "嗯了声", "表示同意"],
        "摇头": ["摆首", "晃了晃脑袋", "不以为然"],
        "不由得": ["忍不住", "不禁", "鬼使神差地", "身不由己地"],
        "淡淡": ["浅浅", "轻轻", "若有若无地", "漫不经心地"],
        "微微": ["略略", "稍稍", "隐隐", "几不可察地"],
    }

    def __init__(self, project_dir: Path):
        self.project_dir = Path(project_dir)
        self.data_dir = self.project_dir / "fatigue_data"
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.chapter_stats: Dict[int, ChapterVocabularyStats] = {}
        self.global_word_freq: Counter = Counter()
        self.global_bigram_freq: Counter = Counter()
        self.fatigue_words: List[FatigueWord] = []
        self._load()

    def _get_file_path(self, name: str) -> Path:
        return self.data_dir / f"{name}.json"

    def _load(self) -> None:
        stats_path = self._get_file_path("chapter_stats")
        if stats_path.exists():
            try:
                with open(stats_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                for ch_str, stats_dict in data.items():
                    ch = int(ch_str)
                    self.chapter_stats[ch] = ChapterVocabularyStats(**stats_dict)
            except Exception as e:
                print(f"[FatigueDetector] Failed to load chapter_stats: {e}")

        freq_path = self._get_file_path("global_freq")
        if freq_path.exists():
            try:
                with open(freq_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.global_word_freq = Counter(data.get("words", {}))
                self.global_bigram_freq = Counter(data.get("bigrams", {}))
            except Exception as e:
                print(f"[FatigueDetector] Failed to load global_freq: {e}")

        fatigue_path = self._get_file_path("fatigue_words")
        if fatigue_path.exists():
            try:
                with open(fatigue_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.fatigue_words = [FatigueWord(**item) for item in data]
            except Exception as e:
                print(f"[FatigueDetector] Failed to load fatigue_words: {e}")

    def _save(self) -> None:
        stats_dict = {str(ch): s.to_dict() for ch, s in self.chapter_stats.items()}
        with open(self._get_file_path("chapter_stats"), 'w', encoding='utf-8') as f:
            json.dump(stats_dict, f, ensure_ascii=False, indent=2)

        with open(self._get_file_path("global_freq"), 'w', encoding='utf-8') as f:
            json.dump({
                "words": dict(self.global_word_freq.most_common(500)),
                "bigrams": dict(self.global_bigram_freq.most_common(300)),
            }, f, ensure_ascii=False, indent=2)

        with open(self._get_file_path("fatigue_words"), 'w', encoding='utf-8') as f:
            json.dump([fw.to_dict() for fw in self.fatigue_words], f, ensure_ascii=False, indent=2)

    def _extract_words(self, text: str) -> List[str]:
        """提取中文词汇（2-4字词）"""
        cleaned = re.sub(r'[^\u4e00-\u9fff]', '', text)
        words = []
        i = 0
        while i < len(cleaned):
            for wlen in [4, 3, 2]:
                if i + wlen <= len(cleaned):
                    words.append(cleaned[i:i + wlen])
            i += 1
        return words

    def _extract_bigrams(self, text: str) -> List[str]:
        """提取中文二元组"""
        cleaned = re.sub(r'[^\u4e00-\u9fff]', '', text)
        return [cleaned[i:i + 2] for i in range(len(cleaned) - 1)]

    def _extract_sentence_starters(self, text: str) -> List[str]:
        """提取句子开头"""
        sentences = re.split(r'[。！？\n]+', text)
        starters = []
        for s in sentences:
            s = s.strip()
            if len(s) >= 2:
                starters.append(s[:4] if len(s) >= 4 else s)
        return starters

    def _extract_paragraph_openers(self, text: str) -> List[str]:
        """提取段落开头"""
        paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
        openers = []
        for p in paragraphs:
            if len(p) >= 4:
                openers.append(p[:6] if len(p) >= 6 else p)
        return openers

    def _detect_cliches(self, text: str) -> List[Dict[str, str]]:
        """检测陈词滥调"""
        found = []
        for pattern, name, suggestion in self.CLICHE_PATTERNS:
            matches = re.findall(pattern, text)
            for m in matches:
                found.append({
                    "pattern_name": name,
                    "matched_text": m if isinstance(m, str) else str(m),
                    "suggestion": suggestion,
                })
        return found

    def _classify_sentence_starter(self, starter: str) -> str:
        """分类句子开头"""
        for i, pattern in enumerate(self.SENTENCE_STARTER_PATTERNS):
            if re.match(pattern, starter):
                categories = [
                    "代词开头", "时间词开头", "突发词开头", "感知词开头",
                    "转折词开头", "转折词开头", "顺序词开头",
                    "因果词开头", "假设词开头", "让步词开头",
                    "介词开头", "数量词开头",
                ]
                return categories[i] if i < len(categories) else "其他"
        return "其他"

    def analyze_chapter(self, chapter: int, text: str) -> ChapterVocabularyStats:
        """分析单章词汇使用情况"""
        cleaned = re.sub(r'[^\u4e00-\u9fff]', '', text)
        total_chars = len(cleaned)
        words = self._extract_words(text)
        bigrams = self._extract_bigrams(text)
        sentence_starters = self._extract_sentence_starters(text)
        paragraph_openers = self._extract_paragraph_openers(text)

        word_counter = Counter(words)
        bigram_counter = Counter(bigrams)
        starter_counter = Counter(sentence_starters)
        opener_counter = Counter(paragraph_openers)

        unique_chars = len(set(cleaned))
        unique_words = len(set(words))
        type_token_ratio = unique_words / max(len(words), 1)

        cliches = self._detect_cliches(text)

        starter_classification: Dict[str, int] = defaultdict(int)
        for starter, count in starter_counter.items():
            cat = self._classify_sentence_starter(starter)
            starter_classification[cat] += count

        fatigue_score = self._calculate_fatigue_score(
            word_counter, bigram_counter, starter_classification, len(cliches), total_chars
        )

        stats = ChapterVocabularyStats(
            chapter=chapter,
            total_chars=total_chars,
            total_words=len(words),
            unique_chars=unique_chars,
            unique_words=unique_words,
            type_token_ratio=type_token_ratio,
            top_repeated_words=word_counter.most_common(30),
            top_repeated_bigrams=bigram_counter.most_common(20),
            sentence_starter_repetition=dict(starter_classification),
            paragraph_opener_repetition=dict(opener_counter.most_common(15)),
            cliche_count=len(cliches),
            fatigue_score=fatigue_score,
        )

        self.chapter_stats[chapter] = stats
        self.global_word_freq.update(word_counter)
        self.global_bigram_freq.update(bigram_counter)
        self._update_fatigue_words(chapter, word_counter)
        self._save()

        return stats

    def _calculate_fatigue_score(
        self, word_counter: Counter, bigram_counter: Counter,
        starter_classification: Dict[str, int], cliche_count: int, total_chars: int,
    ) -> float:
        """计算词汇疲劳分数（0-100，越高越疲劳）"""
        score = 0.0

        if total_chars > 0:
            top_word_ratio = sum(c for _, c in word_counter.most_common(10)) / total_chars
            if top_word_ratio > 0.15:
                score += 30
            elif top_word_ratio > 0.10:
                score += 20
            elif top_word_ratio > 0.07:
                score += 10

        max_starter_cat = max(starter_classification.values()) if starter_classification else 0
        total_starters = sum(starter_classification.values())
        if total_starters > 0 and max_starter_cat / total_starters > 0.4:
            score += 25
        elif total_starters > 0 and max_starter_cat / total_starters > 0.3:
            score += 15

        score += min(cliche_count * 3, 25)

        if total_chars > 0:
            bigram_top_ratio = sum(c for _, c in bigram_counter.most_common(5)) / total_chars
            if bigram_top_ratio > 0.08:
                score += 20
            elif bigram_top_ratio > 0.05:
                score += 10

        return min(100, score)

    def _update_fatigue_words(self, chapter: int, word_counter: Counter) -> None:
        """更新疲劳词列表"""
        existing_words = {fw.word: fw for fw in self.fatigue_words}

        for category, word_list in self.FATIGUE_WORD_CATEGORIES.items():
            for word in word_list:
                count = word_counter.get(word, 0)
                if count == 0:
                    continue

                if word in existing_words:
                    fw = existing_words[word]
                    fw.total_count += count
                    if chapter not in fw.chapters_appeared:
                        fw.chapters_appeared.append(chapter)
                    fw.last_seen_chapter = chapter
                else:
                    suggestions = self.REPLACEMENT_SUGGESTIONS.get(word, [])
                    fw = FatigueWord(
                        word=word,
                        total_count=count,
                        chapters_appeared=[chapter],
                        fatigue_level="low",
                        category=category,
                        suggestions=suggestions,
                        first_seen_chapter=chapter,
                        last_seen_chapter=chapter,
                    )
                    self.fatigue_words.append(fw)
                    existing_words[word] = fw

        for fw in self.fatigue_words:
            chapters_count = len(fw.chapters_appeared)
            if fw.total_count >= 30 or (chapters_count >= 5 and fw.total_count / chapters_count >= 6):
                fw.fatigue_level = "critical"
            elif fw.total_count >= 20 or (chapters_count >= 3 and fw.total_count / chapters_count >= 5):
                fw.fatigue_level = "high"
            elif fw.total_count >= 10 or (chapters_count >= 2 and fw.total_count / chapters_count >= 4):
                fw.fatigue_level = "medium"
            else:
                fw.fatigue_level = "low"

    def get_chapter_fatigue_report(self, chapter: int) -> Dict[str, Any]:
        """获取单章词汇疲劳报告"""
        stats = self.chapter_stats.get(chapter)
        if not stats:
            return {"error": f"第{chapter}章尚未分析"}

        cliches = self._detect_cliches("")

        return {
            "chapter": chapter,
            "stats": stats.to_dict(),
            "fatigue_level": self._fatigue_level_label(stats.fatigue_score),
            "warnings": self._generate_fatigue_warnings(stats),
            "suggestions": self._generate_fatigue_suggestions(stats),
        }

    def _fatigue_level_label(self, score: float) -> str:
        if score >= 70:
            return "严重疲劳 — 急需大幅替换重复词汇"
        elif score >= 50:
            return "中度疲劳 — 建议替换高频重复词"
        elif score >= 30:
            return "轻度疲劳 — 注意部分词汇重复"
        else:
            return "健康 — 词汇使用自然多样"

    def _generate_fatigue_warnings(self, stats: ChapterVocabularyStats) -> List[str]:
        warnings = []

        if stats.type_token_ratio < 0.15:
            warnings.append(f"⚠️ 词汇多样性极低（TTR={stats.type_token_ratio:.3f}），大量词汇重复使用")
        elif stats.type_token_ratio < 0.25:
            warnings.append(f"⚡ 词汇多样性偏低（TTR={stats.type_token_ratio:.3f}），建议丰富用词")

        if stats.cliche_count >= 10:
            warnings.append(f"🔴 陈词滥调过多（{stats.cliche_count}处），严重损害文笔质感")
        elif stats.cliche_count >= 5:
            warnings.append(f"🟡 陈词滥调偏多（{stats.cliche_count}处），建议替换为独特表达")

        starter_cats = stats.sentence_starter_repetition
        total = sum(starter_cats.values())
        if total > 0:
            for cat, count in starter_cats.items():
                ratio = count / total
                if ratio > 0.35:
                    warnings.append(f"🔴 句子开头「{cat}」占比{ratio:.0%}，句式严重单调")
                elif ratio > 0.25:
                    warnings.append(f"🟡 句子开头「{cat}」占比{ratio:.0%}，建议变化句式")

        return warnings

    def _generate_fatigue_suggestions(self, stats: ChapterVocabularyStats) -> List[str]:
        suggestions = []

        if stats.type_token_ratio < 0.25:
            suggestions.append("📝 使用同义词替换重复词汇，扩大词汇量")
            suggestions.append("📝 用具体名词替代泛化词汇（如用「檀木椅」替代「椅子」）")

        if stats.cliche_count >= 5:
            suggestions.append("🔄 将模板化表达替换为独特的、符合角色个性的描写")

        starter_cats = stats.sentence_starter_repetition
        total = sum(starter_cats.values())
        if total > 0:
            max_cat = max(starter_cats, key=starter_cats.get)
            if starter_cats[max_cat] / total > 0.25:
                suggestions.append(f"🔄 减少「{max_cat}」开头的句子，用动作、对话、环境描写交替开头")

        top_words = stats.top_repeated_words[:5]
        if top_words:
            words_str = "、".join([w for w, _ in top_words if len(w) >= 2][:3])
            if words_str:
                suggestions.append(f"🔄 高频词「{words_str}」出现过多，请检查是否有更精准的替代词")

        return suggestions

    def get_overall_fatigue_report(self) -> Dict[str, Any]:
        """获取整体词汇疲劳报告"""
        if not self.chapter_stats:
            return {"error": "暂无分析数据"}

        all_chapters = sorted(self.chapter_stats.keys())
        avg_ttr = sum(s.type_token_ratio for s in self.chapter_stats.values()) / len(self.chapter_stats)
        avg_fatigue = sum(s.fatigue_score for s in self.chapter_stats.values()) / len(self.chapter_stats)
        total_cliches = sum(s.cliche_count for s in self.chapter_stats.values())

        critical_fatigue = [fw for fw in self.fatigue_words if fw.fatigue_level == "critical"]
        high_fatigue = [fw for fw in self.fatigue_words if fw.fatigue_level == "high"]

        chapter_trend = [
            {"chapter": ch, "fatigue_score": self.chapter_stats[ch].fatigue_score,
             "ttr": round(self.chapter_stats[ch].type_token_ratio, 4)}
            for ch in all_chapters
        ]

        return {
            "total_chapters_analyzed": len(all_chapters),
            "chapter_range": f"第{all_chapters[0]}章 - 第{all_chapters[-1]}章",
            "average_ttr": round(avg_ttr, 4),
            "average_fatigue_score": round(avg_fatigue, 1),
            "overall_level": self._fatigue_level_label(avg_fatigue),
            "total_cliches_found": total_cliches,
            "critical_fatigue_words": [fw.to_dict() for fw in critical_fatigue],
            "high_fatigue_words": [fw.to_dict() for fw in high_fatigue],
            "chapter_trend": chapter_trend,
            "global_top_words": self.global_word_freq.most_common(20),
            "global_top_bigrams": self.global_bigram_freq.most_common(15),
        }

    def get_word_replacement_suggestions(self, word: str) -> Dict[str, Any]:
        """获取单个词汇的替换建议"""
        suggestions = self.REPLACEMENT_SUGGESTIONS.get(word, [])

        fw = None
        for f in self.fatigue_words:
            if f.word == word:
                fw = f
                break

        return {
            "word": word,
            "suggestions": suggestions,
            "fatigue_info": fw.to_dict() if fw else None,
            "global_count": self.global_word_freq.get(word, 0),
        }

    def build_fatigue_avoidance_prompt(self, chapter: int) -> str:
        """构建词汇疲劳规避提示词，注入到章节生成prompt中"""
        critical = [fw for fw in self.fatigue_words if fw.fatigue_level == "critical"]
        high = [fw for fw in self.fatigue_words if fw.fatigue_level == "high"]

        parts = ["\n## 📝 词汇疲劳规避指令\n"]

        if critical:
            parts.append("### 🚫 严禁使用的疲劳词（已严重过度使用）")
            for fw in critical[:8]:
                alts = "、".join(fw.suggestions[:3]) if fw.suggestions else "请自行替换"
                parts.append(f"- **{fw.word}**（已使用{fw.total_count}次）→ 替代: {alts}")

        if high:
            parts.append("\n### ⚠️ 尽量避免的高频词")
            for fw in high[:5]:
                alts = "、".join(fw.suggestions[:3]) if fw.suggestions else "请自行替换"
                parts.append(f"- **{fw.word}**（已使用{fw.total_count}次）→ 替代: {alts}")

        parts.append("\n### 词汇多样性原则")
        parts.append("- 同一词汇在同一段内不重复出现超过2次")
        parts.append("- 用具体名词替代泛化词汇")
        parts.append("- 用独特动作替代模板化神态描写")
        parts.append("- 句子开头多样化：动作/对话/环境/心理交替")
        parts.append("- 避免「眼中闪过」「心中一震」「嘴角微扬」等模板表达")

        return "\n".join(parts)


class HumanReviewGates:
    """人工审查关卡系统 — 章节发布前的质量关卡

    每个关卡是一个必须通过（或警告）的检查点。
    只有所有阻断级关卡通过，章节才能标记为"可发布"。
    """

    GATE_DEFINITIONS: List[Dict[str, Any]] = [
        {
            "id": "ai_trace",
            "name": "AI痕迹检测",
            "description": "检测文本中的AI写作痕迹，确保内容自然",
            "category": "quality",
            "blocking": True,
            "threshold": 70,
            "threshold_desc": "AI痕迹分数需 >= 70（满分100，越高越好）",
        },
        {
            "id": "vocabulary_fatigue",
            "name": "词汇疲劳检测",
            "description": "检测词汇重复使用和陈词滥调",
            "category": "quality",
            "blocking": False,
            "threshold": 60,
            "threshold_desc": "疲劳分数需 <= 60（满分100，越低越好）",
        },
        {
            "id": "retention_power",
            "name": "追读力检测",
            "description": "检测钩子、爽点、微兑现等读者留存要素",
            "category": "engagement",
            "blocking": False,
            "threshold": 50,
            "threshold_desc": "追读力分数需 >= 50（满分100）",
        },
        {
            "id": "word_count",
            "name": "字数达标",
            "description": "检查章节字数是否达到设定目标",
            "category": "basic",
            "blocking": True,
            "threshold": 0.85,
            "threshold_desc": "实际字数需 >= 目标字数的85%",
        },
        {
            "id": "consistency",
            "name": "角色一致性",
            "description": "检查角色名字、性格、能力是否与设定一致",
            "category": "consistency",
            "blocking": True,
            "threshold": 1,
            "threshold_desc": "无角色名错误或性格偏离",
        },
        {
            "id": "pacing",
            "name": "节奏检测",
            "description": "检查章节节奏是否有变化，避免单调",
            "category": "style",
            "blocking": False,
            "threshold": 60,
            "threshold_desc": "节奏变化分数需 >= 60",
        },
        {
            "id": "dialogue_balance",
            "name": "对话平衡",
            "description": "检查对话与叙述的比例是否合理",
            "category": "style",
            "blocking": False,
            "threshold": 0.15,
            "threshold_desc": "对话占比需 >= 15%",
        },
        {
            "id": "hook_quality",
            "name": "钩子质量",
            "description": "检查开篇钩子和章末悬念是否有效",
            "category": "engagement",
            "blocking": True,
            "threshold": 1,
            "threshold_desc": "至少1个有效钩子",
        },
    ]

    def __init__(self, project_dir: Path):
        self.project_dir = Path(project_dir)
        self.data_dir = self.project_dir / "review_gates"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.gate_results: Dict[int, Dict[str, Any]] = {}
        self._load()

    def _load(self) -> None:
        fp = self.data_dir / "gate_results.json"
        if fp.exists():
            try:
                with open(fp, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.gate_results = {int(k): v for k, v in data.items()}
            except Exception:
                pass

    def _save(self) -> None:
        fp = self.data_dir / "gate_results.json"
        with open(fp, 'w', encoding='utf-8') as f:
            json.dump(self.gate_results, f, ensure_ascii=False, indent=2)

    def evaluate_chapter(
        self, chapter: int,
        ai_trace_score: float = 0,
        fatigue_score: float = 100,
        retention_score: float = 0,
        word_count: int = 0,
        target_word_count: int = 4000,
        consistency_issues: int = 0,
        pacing_score: float = 0,
        dialogue_ratio: float = 0,
        hook_count: int = 0,
    ) -> Dict[str, Any]:
        """评估章节是否通过所有审查关卡"""
        gate_scores = {
            "ai_trace": ai_trace_score,
            "vocabulary_fatigue": 100 - fatigue_score,
            "retention_power": retention_score,
            "word_count": word_count / max(target_word_count, 1),
            "consistency": 1 if consistency_issues == 0 else max(0, 1 - consistency_issues * 0.3),
            "pacing": pacing_score,
            "dialogue_balance": dialogue_ratio,
            "hook_quality": min(hook_count, 3) / 3,
        }

        results = []
        blocking_failed = []
        warning_failed = []
        all_passed = True

        for gate_def in self.GATE_DEFINITIONS:
            gate_id = gate_def["id"]
            score = gate_scores.get(gate_id, 0)
            passed = score >= gate_def["threshold"]

            gate_result = {
                "gate_id": gate_id,
                "name": gate_def["name"],
                "description": gate_def["description"],
                "category": gate_def["category"],
                "blocking": gate_def["blocking"],
                "threshold": gate_def["threshold"],
                "threshold_desc": gate_def["threshold_desc"],
                "actual_score": round(score, 2),
                "passed": passed,
                "status": "✅ 通过" if passed else "❌ 未通过",
            }

            if not passed:
                if gate_def["blocking"]:
                    blocking_failed.append(gate_result)
                    all_passed = False
                else:
                    warning_failed.append(gate_result)

            results.append(gate_result)

        overall_status = "approved" if all_passed else ("blocked" if blocking_failed else "warning")

        chapter_result = {
            "chapter": chapter,
            "overall_status": overall_status,
            "status_label": {
                "approved": "✅ 全部通过 — 可以发布",
                "blocked": "🚫 有关卡未通过 — 必须修复",
                "warning": "⚠️ 有警告 — 建议优化后发布",
            }.get(overall_status, ""),
            "gates": results,
            "blocking_failed": blocking_failed,
            "warning_failed": warning_failed,
            "passed_count": sum(1 for r in results if r["passed"]),
            "total_count": len(results),
            "evaluated_at": _utc_now_iso(),
        }

        self.gate_results[chapter] = chapter_result
        self._save()

        return chapter_result

    def get_chapter_gates(self, chapter: int) -> Optional[Dict[str, Any]]:
        """获取章节审查关卡结果"""
        return self.gate_results.get(chapter)

    def get_all_gates_summary(self) -> Dict[str, Any]:
        """获取所有章节关卡汇总"""
        if not self.gate_results:
            return {"error": "暂无审查数据"}

        chapters = sorted(self.gate_results.keys())
        total = len(chapters)
        approved = sum(1 for ch in chapters if self.gate_results[ch]["overall_status"] == "approved")
        blocked = sum(1 for ch in chapters if self.gate_results[ch]["overall_status"] == "blocked")
        warning = sum(1 for ch in chapters if self.gate_results[ch]["overall_status"] == "warning")

        gate_fail_counts: Dict[str, int] = defaultdict(int)
        for ch in chapters:
            for gate in self.gate_results[ch]["gates"]:
                if not gate["passed"]:
                    gate_fail_counts[gate["name"]] += 1

        return {
            "total_chapters": total,
            "approved": approved,
            "blocked": blocked,
            "warning": warning,
            "approval_rate": round(approved / total * 100, 1) if total > 0 else 0,
            "most_failed_gates": sorted(gate_fail_counts.items(), key=lambda x: -x[1])[:5],
            "chapter_summary": [
                {
                    "chapter": ch,
                    "status": self.gate_results[ch]["overall_status"],
                    "passed": self.gate_results[ch]["passed_count"],
                    "total": self.gate_results[ch]["total_count"],
                }
                for ch in chapters
            ],
        }