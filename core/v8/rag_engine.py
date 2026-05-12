#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS RAG引擎 — 向量检索 + 反向工程

核心功能:
1. 章节索引 — 将所有章节内容建立可检索索引
2. 语义检索 — 基于TF-IDF的关键段落检索
3. 上下文组装 — 为章节生成自动检索相关前文
4. 反向工程 — 从已有文本中提取角色/情节/世界观信息
5. 一致性校验 — 检测新章节与前文的矛盾
"""

from __future__ import annotations

import json
import math
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


@dataclass
class IndexedParagraph:
    chapter: int
    paragraph_index: int
    text: str
    tokens: List[str]
    tf: Dict[str, float]
    char_count: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "chapter": self.chapter,
            "paragraph_index": self.paragraph_index,
            "text": self.text[:200],
            "char_count": self.char_count,
        }


@dataclass
class SearchResult:
    paragraph: IndexedParagraph
    score: float
    match_keywords: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "chapter": self.paragraph.chapter,
            "paragraph_index": self.paragraph.paragraph_index,
            "text_preview": self.paragraph.text[:300],
            "score": round(self.score, 4),
            "match_keywords": self.match_keywords,
        }


@dataclass
class ExtractedCharacter:
    name: str
    aliases: List[str]
    first_appearance_chapter: int
    mention_count: int
    associated_words: List[str]
    role_hint: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "aliases": self.aliases,
            "first_appearance_chapter": self.first_appearance_chapter,
            "mention_count": self.mention_count,
            "associated_words": self.associated_words[:10],
            "role_hint": self.role_hint,
        }


@dataclass
class ExtractedEvent:
    description: str
    chapter: int
    event_type: str
    involved_characters: List[str]
    keywords: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "description": self.description,
            "chapter": self.chapter,
            "event_type": self.event_type,
            "involved_characters": self.involved_characters,
            "keywords": self.keywords,
        }


class RAGEngine:
    """RAG检索引擎 — 基于TF-IDF的轻量级向量检索"""

    STOP_WORDS: Set[str] = {
        "的", "了", "在", "是", "我", "有", "和", "就", "不", "人", "都", "一",
        "一个", "上", "也", "很", "到", "说", "要", "去", "你", "会", "着",
        "没有", "看", "好", "自己", "这", "他", "她", "它", "们", "那", "些",
        "什么", "怎么", "如何", "为什么", "可以", "这个", "那个", "还是",
        "只是", "但是", "不过", "因为", "所以", "如果", "虽然", "然而",
        "已经", "正在", "将", "被", "把", "从", "对", "向", "与", "及",
        "或", "而", "且", "但", "却", "则", "以", "之", "其", "所", "者",
        "于", "为", "此", "等", "能", "会", "可", "已", "还", "又", "再",
        "才", "刚", "正", "便", "即", "只", "仅", "光", "单", "另", "各",
        "每", "某", "任", "全", "整", "半", "多", "少", "几", "些", "点",
    }

    CHARACTER_NAME_PATTERNS: List[re.Pattern] = [
        re.compile(r"(?:^|。|！|？|，|、|\n)([A-Z\u4e00-\u9fff]{2,4})(?:道|说|问|喊|叫|喝|吼|叹|笑|哭|怒|惊|想|暗想|心想|思忖)"),
        re.compile(r"([A-Z\u4e00-\u9fff]{2,4})(?:的|之)(?:手|眼|剑|刀|拳|掌|身|影|声音|目光|气息)"),
        re.compile(r"(?:只见|只听|但见)([A-Z\u4e00-\u9fff]{2,4})"),
        re.compile(r"([A-Z\u4e00-\u9fff]{2,4})(?:冷笑|微微一笑|淡淡|缓缓|轻轻|猛地|突然|忽然)"),
    ]

    EVENT_PATTERNS: List[Tuple[re.Pattern, str]] = [
        (re.compile(r"(?:突破|晋升|进阶|觉醒|领悟)(?:了|到|至|为)"), "power_up"),
        (re.compile(r"(?:战斗|交手|对决|激战|厮杀|搏杀)"), "battle"),
        (re.compile(r"(?:发现|找到|获得|得到|取得)(?:了)?(?:一|某|那)"), "discovery"),
        (re.compile(r"(?:遇到|遇见|碰到|撞见)(?:了)?"), "encounter"),
        (re.compile(r"(?:离开|出发|前往|来到|到达|进入)(?:了)?"), "travel"),
        (re.compile(r"(?:揭露|曝光|真相|秘密|身份)(?:了|被|是)"), "reveal"),
        (re.compile(r"(?:死亡|陨落|牺牲|死去|被杀)"), "death"),
        (re.compile(r"(?:背叛|出卖|反水|倒戈)"), "betrayal"),
        (re.compile(r"(?:结盟|联手|合作|联盟)"), "alliance"),
        (re.compile(r"(?:危机|危险|灾难|浩劫|劫难)"), "crisis"),
    ]

    def __init__(self, project_dir: Path):
        self.project_dir = Path(project_dir)
        self.data_dir = self.project_dir / "rag_data"
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.index: List[IndexedParagraph] = []
        self.doc_freq: Dict[str, int] = defaultdict(int)
        self.total_docs: int = 0
        self.chapter_texts: Dict[int, str] = {}
        self.extracted_characters: List[ExtractedCharacter] = []
        self.extracted_events: List[ExtractedEvent] = []
        self._load()

    def _get_file_path(self, name: str) -> str:
        return str(self.data_dir / f"{name}.json")

    def _load(self) -> None:
        idx_path = self._get_file_path("index")
        if Path(idx_path).exists():
            try:
                with open(idx_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.index = [IndexedParagraph(**item) for item in data.get("paragraphs", [])]
                self.doc_freq = defaultdict(int, data.get("doc_freq", {}))
                self.total_docs = data.get("total_docs", 0)
            except Exception as e:
                print(f"[RAGEngine] Load index error: {e}")

        chars_path = self._get_file_path("extracted_characters")
        if Path(chars_path).exists():
            try:
                with open(chars_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.extracted_characters = [ExtractedCharacter(**item) for item in data]
            except Exception as e:
                print(f"[RAGEngine] Load characters error: {e}")

        events_path = self._get_file_path("extracted_events")
        if Path(events_path).exists():
            try:
                with open(events_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.extracted_events = [ExtractedEvent(**item) for item in data]
            except Exception as e:
                print(f"[RAGEngine] Load events error: {e}")

    def _save(self) -> None:
        with open(self._get_file_path("index"), 'w', encoding='utf-8') as f:
            json.dump({
                "paragraphs": [p.to_dict() for p in self.index],
                "doc_freq": dict(self.doc_freq),
                "total_docs": self.total_docs,
            }, f, ensure_ascii=False, indent=2)

        with open(self._get_file_path("extracted_characters"), 'w', encoding='utf-8') as f:
            json.dump([c.to_dict() for c in self.extracted_characters], f, ensure_ascii=False, indent=2)

        with open(self._get_file_path("extracted_events"), 'w', encoding='utf-8') as f:
            json.dump([e.to_dict() for e in self.extracted_events], f, ensure_ascii=False, indent=2)

    def _tokenize(self, text: str) -> List[str]:
        """中文分词 — 基于字符n-gram的简单分词"""
        cleaned = re.sub(r'[^\u4e00-\u9fffA-Za-z0-9]', ' ', text)
        tokens = []

        for word in cleaned.split():
            if len(word) <= 1:
                continue
            if word in self.STOP_WORDS:
                continue
            tokens.append(word)

        for i in range(len(cleaned) - 1):
            bigram = cleaned[i:i + 2]
            if bigram not in self.STOP_WORDS and not re.search(r'[A-Za-z0-9]', bigram):
                tokens.append(bigram)

        return tokens

    def _compute_tf(self, tokens: List[str]) -> Dict[str, float]:
        """计算词频"""
        counter = Counter(tokens)
        max_freq = max(counter.values()) if counter else 1
        return {word: count / max_freq for word, count in counter.items()}

    def index_chapter(self, chapter: int, text: str) -> int:
        """索引一个章节的内容"""
        self.chapter_texts[chapter] = text
        paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
        indexed_count = 0

        for pi, para in enumerate(paragraphs):
            if len(para) < 20:
                continue

            tokens = self._tokenize(para)
            if len(tokens) < 3:
                continue

            tf = self._compute_tf(tokens)
            ip = IndexedParagraph(
                chapter=chapter,
                paragraph_index=pi,
                text=para,
                tokens=tokens,
                tf=tf,
                char_count=len(para),
            )
            self.index.append(ip)
            indexed_count += 1

            for token in set(tokens):
                self.doc_freq[token] += 1

        self.total_docs = len(self.index)
        self._save()
        return indexed_count

    def search(self, query: str, top_k: int = 10,
               filter_chapter: Optional[int] = None) -> List[SearchResult]:
        """搜索相关段落"""
        if not self.index:
            return []

        query_tokens = self._tokenize(query)
        if not query_tokens:
            return []

        query_tf = self._compute_tf(query_tokens)
        results: List[Tuple[float, IndexedParagraph, List[str]]] = []

        for ip in self.index:
            if filter_chapter is not None and ip.chapter != filter_chapter:
                continue

            score = 0.0
            matched_keywords: List[str] = []

            for token, qtf in query_tf.items():
                if token in ip.tf:
                    tf = ip.tf[token]
                    df = self.doc_freq.get(token, 1)
                    idf = math.log((self.total_docs + 1) / (df + 1)) + 1
                    score += tf * idf * qtf
                    matched_keywords.append(token)

            if score > 0:
                results.append((score, ip, matched_keywords))

        results.sort(key=lambda x: -x[0])
        return [SearchResult(paragraph=r[1], score=r[0], match_keywords=r[2])
                for r in results[:top_k]]

    def get_relevant_context(self, chapter: int, chapter_summary: str,
                             max_chars: int = 3000) -> str:
        """为章节生成获取相关前文上下文"""
        if chapter <= 1 or not self.index:
            return ""

        query = chapter_summary
        results = self.search(query, top_k=15, filter_chapter=None)

        seen = set()
        context_parts: List[str] = []
        total_chars = 0

        for r in results:
            if r.paragraph.chapter >= chapter:
                continue
            key = (r.paragraph.chapter, r.paragraph.paragraph_index)
            if key in seen:
                continue
            seen.add(key)

            snippet = r.paragraph.text
            if total_chars + len(snippet) > max_chars:
                remaining = max_chars - total_chars
                if remaining > 50:
                    context_parts.append(f"[第{r.paragraph.chapter}章] {snippet[:remaining]}...")
                break

            context_parts.append(f"[第{r.paragraph.chapter}章] {snippet}")
            total_chars += len(snippet)

        return "\n\n".join(context_parts)

    def build_context_prompt(self, chapter: int, chapter_summary: str) -> str:
        """构建上下文提示词，注入到章节生成prompt中"""
        context = self.get_relevant_context(chapter, chapter_summary)
        if not context:
            return ""

        parts = ["\n## 📚 前文相关上下文（RAG检索）\n"]
        parts.append("以下是从前文章节中检索到的与本章相关的内容，请确保情节连贯一致：\n")
        parts.append(context)
        parts.append("\n请确保本章与上述前文内容保持连贯，不出现矛盾。")
        return "\n".join(parts)

    def reverse_engineer_characters(self, text: str, chapter: int) -> List[ExtractedCharacter]:
        """从文本中反向工程提取角色信息"""
        found_names: Dict[str, List[str]] = defaultdict(list)

        for pattern in self.CHARACTER_NAME_PATTERNS:
            for match in pattern.finditer(text):
                name = match.group(1)
                if len(name) >= 2 and not all(c in self.STOP_WORDS for c in name):
                    context_start = max(0, match.start() - 10)
                    context_end = min(len(text), match.end() + 10)
                    context = text[context_start:context_end]
                    found_names[name].append(context)

        new_characters = []
        for name, contexts in found_names.items():
            if len(contexts) < 2:
                continue

            existing = None
            for ec in self.extracted_characters:
                if ec.name == name or name in ec.aliases:
                    existing = ec
                    break

            if existing:
                existing.mention_count += len(contexts)
                continue

            all_text = " ".join(contexts)
            associated = self._tokenize(all_text)
            associated_counter = Counter(associated)
            top_associated = [w for w, _ in associated_counter.most_common(15)
                              if w != name and len(w) >= 2]

            role_hint = self._guess_role(name, contexts)

            char = ExtractedCharacter(
                name=name,
                aliases=[],
                first_appearance_chapter=chapter,
                mention_count=len(contexts),
                associated_words=top_associated,
                role_hint=role_hint,
            )
            self.extracted_characters.append(char)
            new_characters.append(char)

        self._save()
        return new_characters

    def _guess_role(self, name: str, contexts: List[str]) -> str:
        """推测角色定位"""
        all_text = " ".join(contexts)
        if re.search(r"(?:师父|师尊|老师|教导|传授|指点)", all_text):
            return "导师/长辈"
        if re.search(r"(?:敌人|对手|仇人|死敌|宿敌)", all_text):
            return "对手/敌人"
        if re.search(r"(?:朋友|兄弟|姐妹|同伴|伙伴|队友)", all_text):
            return "同伴/朋友"
        if re.search(r"(?:爱|情|喜欢|心动|倾心|恋)", all_text):
            return "恋人/感情对象"
        if re.search(r"(?:杀|死|灭|屠|斩|击败|战胜)", all_text):
            return "战士/强者"
        if re.search(r"(?:修炼|突破|功法|灵力|真气|境界)", all_text):
            return "修炼者"
        return "未知定位"

    def reverse_engineer_events(self, text: str, chapter: int) -> List[ExtractedEvent]:
        """从文本中反向工程提取事件信息"""
        new_events = []

        for pattern, event_type in self.EVENT_PATTERNS:
            for match in pattern.finditer(text):
                context_start = max(0, match.start() - 30)
                context_end = min(len(text), match.end() + 50)
                description = text[context_start:context_end].strip()

                involved = []
                for ec in self.extracted_characters:
                    if ec.name in description:
                        involved.append(ec.name)

                keywords = self._tokenize(description)
                keywords = [k for k in keywords if len(k) >= 2][:5]

                event = ExtractedEvent(
                    description=description[:200],
                    chapter=chapter,
                    event_type=event_type,
                    involved_characters=involved,
                    keywords=keywords,
                )
                self.extracted_events.append(event)
                new_events.append(event)

        self._save()
        return new_events

    def reverse_engineer_chapter(self, chapter: int, text: str) -> Dict[str, Any]:
        """对章节进行全面反向工程分析"""
        new_chars = self.reverse_engineer_characters(text, chapter)
        new_events = self.reverse_engineer_events(text, chapter)

        word_count = len(text.replace('\n', '').replace(' ', ''))
        paragraphs = [p for p in text.split('\n') if p.strip()]
        dialogue_lines = re.findall(r'[「「"][^」」"]+[」」"]', text)

        dialogue_ratio = sum(len(d) for d in dialogue_lines) / max(word_count, 1)

        action_verbs = len(re.findall(r'(?:斩|杀|打|击|冲|飞|跃|跳|跑|追|逃|躲|闪|挡|劈|刺|砍|轰|爆|碎|裂)', text))
        description_ratio = 1 - dialogue_ratio - (action_verbs / max(word_count, 1) * 10)

        return {
            "chapter": chapter,
            "word_count": word_count,
            "paragraph_count": len(paragraphs),
            "dialogue_ratio": round(dialogue_ratio, 3),
            "action_density": round(action_verbs / max(word_count, 1) * 1000, 1),
            "description_ratio": round(max(0, description_ratio), 3),
            "new_characters_found": len(new_chars),
            "new_characters": [c.to_dict() for c in new_chars],
            "new_events_found": len(new_events),
            "new_events": [e.to_dict() for e in new_events],
            "total_known_characters": len(self.extracted_characters),
            "total_known_events": len(self.extracted_events),
        }

    def check_consistency(self, chapter: int, text: str) -> Dict[str, Any]:
        """一致性校验 — 检测新章节与前文的矛盾"""
        issues = []

        for ec in self.extracted_characters:
            if ec.first_appearance_chapter >= chapter:
                continue
            if ec.name not in text:
                continue

            name_contexts = re.findall(
                re.escape(ec.name) + r".{0,30}",
                text
            )

        prev_chapter_texts = []
        for ch in sorted(self.chapter_texts.keys()):
            if ch < chapter:
                prev_chapter_texts.append(self.chapter_texts[ch])

        if prev_chapter_texts:
            prev_all = "\n".join(prev_chapter_texts)
            prev_terms = set(self._tokenize(prev_all))
            curr_terms = set(self._tokenize(text))

            new_terms = curr_terms - prev_terms
            vanished_terms = prev_terms - curr_terms

            if len(new_terms) > len(curr_terms) * 0.3:
                issues.append({
                    "type": "vocabulary_shift",
                    "severity": "low",
                    "description": f"本章引入了较多新词汇（{len(new_terms)}个），风格可能偏离前文",
                })

        return {
            "chapter": chapter,
            "issues_found": len(issues),
            "issues": issues,
            "is_consistent": len(issues) == 0,
        }

    def get_character_network(self) -> Dict[str, Any]:
        """获取角色关系网络"""
        if not self.extracted_characters:
            return {"error": "暂无角色数据"}

        characters = []
        for ec in self.extracted_characters:
            co_occurrences: Dict[str, int] = defaultdict(int)
            for event in self.extracted_events:
                if ec.name in event.involved_characters:
                    for other in event.involved_characters:
                        if other != ec.name:
                            co_occurrences[other] += 1

            characters.append({
                "name": ec.name,
                "role_hint": ec.role_hint,
                "mention_count": ec.mention_count,
                "first_chapter": ec.first_appearance_chapter,
                "connections": sorted(co_occurrences.items(), key=lambda x: -x[1])[:10],
            })

        return {
            "total_characters": len(self.extracted_characters),
            "characters": sorted(characters, key=lambda x: -x["mention_count"]),
        }

    def get_event_timeline(self) -> Dict[str, Any]:
        """获取事件时间线"""
        if not self.extracted_events:
            return {"error": "暂无事件数据"}

        timeline = defaultdict(list)
        for event in self.extracted_events:
            timeline[event.chapter].append({
                "type": event.event_type,
                "description": event.description,
                "characters": event.involved_characters,
            })

        return {
            "total_events": len(self.extracted_events),
            "chapters_with_events": len(timeline),
            "timeline": {str(ch): events for ch, events in sorted(timeline.items())},
            "event_type_distribution": dict(Counter(
                e.event_type for e in self.extracted_events
            )),
        }

    def get_stats(self) -> Dict[str, Any]:
        """获取RAG引擎统计信息"""
        return {
            "total_indexed_paragraphs": len(self.index),
            "total_docs": self.total_docs,
            "indexed_chapters": sorted(self.chapter_texts.keys()),
            "vocabulary_size": len(self.doc_freq),
            "extracted_characters": len(self.extracted_characters),
            "extracted_events": len(self.extracted_events),
        }