#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS Lorebook - 触发式设定注入系统 v2.0

对标 NovelAI Lorebook，核心能力：
1. 设定条目管理 - 角色/地点/物品/概念/事件/势力/规则
2. 触发关键词 - 关键词出现时自动注入相关设定
3. 级联触发 - 条目A触发后可连带触发条目B
4. 上下文预算管理 - 智能控制注入量，避免超token
5. 优先级排序 - 高优先级条目优先注入
6. 动态更新 - 随故事推进自动更新条目内容
7. 全文搜索 - 模糊匹配+内容搜索+拼音搜索
8. 批量操作 - 批量激活/停用/删除/导出
9. 模板库 - 按题材分类的预设条目模板
10. 冲突检测 - 自动发现条目间矛盾
11. 智能推荐 - 基于内容相似度推荐关联条目
12. 分析仪表盘 - 触发效率/覆盖率/使用趋势

设计原则：
- 纯本地计算，零API依赖
- JSON持久化，支持JSON/CSV导入导出
- 与NovelMemoryManager无缝集成
"""

import json
import os
import re
import csv
import io
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional, Set, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
from collections import Counter, defaultdict


class EntryCategory(Enum):
    CHARACTER = "角色"
    LOCATION = "地点"
    ITEM = "物品"
    CONCEPT = "概念"
    EVENT = "事件"
    FACTION = "势力"
    RULE = "规则"
    CUSTOM = "自定义"


class EntryPriority(Enum):
    CRITICAL = (5, "关键")
    HIGH = (4, "高")
    MEDIUM = (3, "中")
    LOW = (2, "低")
    BACKGROUND = (1, "背景")

    def __init__(self, weight: int, label: str):
        self.weight = weight
        self.label = label


class EntryStatus(Enum):
    DRAFT = "草稿"
    ACTIVE = "活跃"
    ARCHIVED = "已归档"
    DEPRECATED = "已废弃"


class ConflictSeverity(Enum):
    CRITICAL = ("严重", 100)
    MAJOR = ("重要", 70)
    MINOR = ("轻微", 30)
    INFO = ("提示", 10)

    def __init__(self, label: str, score: int):
        self.label = label
        self.score = score


@dataclass
class LorebookEntry:
    entry_id: str
    name: str
    category: EntryCategory
    content: str
    trigger_keywords: List[str] = field(default_factory=list)
    priority: EntryPriority = EntryPriority.MEDIUM
    cascade_to: List[str] = field(default_factory=list)
    chapter_introduced: int = 0
    chapter_expires: int = 0
    is_active: bool = True
    usage_count: int = 0
    last_triggered: str = ""
    notes: str = ""
    status: EntryStatus = EntryStatus.ACTIVE
    folder: str = ""
    tags: List[str] = field(default_factory=list)
    aliases: List[str] = field(default_factory=list)
    related_entries: List[str] = field(default_factory=list)
    completeness: float = 0.0
    created_at: str = ""
    updated_at: str = ""
    version: int = 1

    def to_dict(self) -> dict:
        return {
            "entry_id": self.entry_id,
            "name": self.name,
            "category": self.category.value,
            "content": self.content,
            "trigger_keywords": self.trigger_keywords,
            "priority": self.priority.weight,
            "cascade_to": self.cascade_to,
            "chapter_introduced": self.chapter_introduced,
            "chapter_expires": self.chapter_expires,
            "is_active": self.is_active,
            "usage_count": self.usage_count,
            "last_triggered": self.last_triggered,
            "notes": self.notes,
            "status": self.status.value,
            "folder": self.folder,
            "tags": self.tags,
            "aliases": self.aliases,
            "related_entries": self.related_entries,
            "completeness": self.completeness,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "version": self.version,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "LorebookEntry":
        priority_map = {p.weight: p for p in EntryPriority}
        category_map = {c.value: c for c in EntryCategory}
        status_map = {s.value: s for s in EntryStatus}
        return cls(
            entry_id=data["entry_id"],
            name=data["name"],
            category=category_map.get(data["category"], EntryCategory.CUSTOM),
            content=data["content"],
            trigger_keywords=data.get("trigger_keywords", []),
            priority=priority_map.get(data.get("priority", 3), EntryPriority.MEDIUM),
            cascade_to=data.get("cascade_to", []),
            chapter_introduced=data.get("chapter_introduced", 0),
            chapter_expires=data.get("chapter_expires", 0),
            is_active=data.get("is_active", True),
            usage_count=data.get("usage_count", 0),
            last_triggered=data.get("last_triggered", ""),
            notes=data.get("notes", ""),
            status=status_map.get(data.get("status", "活跃"), EntryStatus.ACTIVE),
            folder=data.get("folder", ""),
            tags=data.get("tags", []),
            aliases=data.get("aliases", []),
            related_entries=data.get("related_entries", []),
            completeness=data.get("completeness", 0.0),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", ""),
            version=data.get("version", 1),
        )


@dataclass
class SearchResult:
    entry: LorebookEntry
    score: float
    match_type: str
    matched_on: str


@dataclass
class EntryConflict:
    entry_a: LorebookEntry
    entry_b: LorebookEntry
    severity: ConflictSeverity
    description: str
    conflicting_fields: List[str]


@dataclass
class TriggerAnalysis:
    entry_id: str
    entry_name: str
    total_triggers: int
    trigger_rate: float
    keywords_effectiveness: Dict[str, int]
    cascade_effectiveness: float
    recommendation: str


class Lorebook:
    """触发式设定注入系统 v2.0"""

    def __init__(self, storage_dir: str = None):
        if storage_dir is None:
            storage_dir = os.path.join(os.path.dirname(__file__), "..", "lorebook_storage")
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)

        self.entries: Dict[str, LorebookEntry] = {}
        self._keyword_index: Dict[str, Set[str]] = {}
        self._folder_index: Dict[str, Set[str]] = {}
        self._tag_index: Dict[str, Set[str]] = {}
        self._content_index: Dict[str, Set[str]] = {}
        self._version_history: Dict[str, List[dict]] = {}

        self.max_context_tokens = 4000
        self.max_entries_per_trigger = 8
        self.fuzzy_match_threshold = 0.75

        self._load()

    def _get_filepath(self) -> str:
        return os.path.join(self.storage_dir, "lorebook.json")

    def _get_history_path(self) -> str:
        return os.path.join(self.storage_dir, "lorebook_history.json")

    def _get_templates_path(self) -> str:
        return os.path.join(self.storage_dir, "lorebook_templates.json")

    def _load(self):
        filepath = self._get_filepath()
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            for entry_data in data.get("entries", []):
                entry = LorebookEntry.from_dict(entry_data)
                self.entries[entry.entry_id] = entry
                self._index_all(entry)
        else:
            self._init_default_entries()

        history_path = self._get_history_path()
        if os.path.exists(history_path):
            with open(history_path, "r", encoding="utf-8") as f:
                self._version_history = json.load(f)

    def save(self):
        data = {
            "version": "2.0",
            "updated_at": datetime.now().isoformat(),
            "total_entries": len(self.entries),
            "entries": [e.to_dict() for e in self.entries.values()],
        }
        with open(self._get_filepath(), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        with open(self._get_history_path(), "w", encoding="utf-8") as f:
            json.dump(self._version_history, f, ensure_ascii=False, indent=2)

    def _index_all(self, entry: LorebookEntry):
        self._index_keywords(entry)
        self._index_folder(entry)
        self._index_tags(entry)
        self._index_content(entry)

    def _unindex_all(self, entry: LorebookEntry):
        self._unindex_keywords(entry)
        self._unindex_folder(entry)
        self._unindex_tags(entry)
        self._unindex_content(entry)

    def _index_keywords(self, entry: LorebookEntry):
        for kw in entry.trigger_keywords:
            kw_lower = kw.lower()
            if kw_lower not in self._keyword_index:
                self._keyword_index[kw_lower] = set()
            self._keyword_index[kw_lower].add(entry.entry_id)

    def _unindex_keywords(self, entry: LorebookEntry):
        for kw in entry.trigger_keywords:
            kw_lower = kw.lower()
            if kw_lower in self._keyword_index:
                self._keyword_index[kw_lower].discard(entry.entry_id)
                if not self._keyword_index[kw_lower]:
                    del self._keyword_index[kw_lower]

    def _index_folder(self, entry: LorebookEntry):
        if entry.folder:
            if entry.folder not in self._folder_index:
                self._folder_index[entry.folder] = set()
            self._folder_index[entry.folder].add(entry.entry_id)

    def _unindex_folder(self, entry: LorebookEntry):
        if entry.folder and entry.folder in self._folder_index:
            self._folder_index[entry.folder].discard(entry.entry_id)
            if not self._folder_index[entry.folder]:
                del self._folder_index[entry.folder]

    def _index_tags(self, entry: LorebookEntry):
        for tag in entry.tags:
            tag_lower = tag.lower()
            if tag_lower not in self._tag_index:
                self._tag_index[tag_lower] = set()
            self._tag_index[tag_lower].add(entry.entry_id)

    def _unindex_tags(self, entry: LorebookEntry):
        for tag in entry.tags:
            tag_lower = tag.lower()
            if tag_lower in self._tag_index:
                self._tag_index[tag_lower].discard(entry.entry_id)
                if not self._tag_index[tag_lower]:
                    del self._tag_index[tag_lower]

    def _index_content(self, entry: LorebookEntry):
        words = set(re.findall(r'[\u4e00-\u9fff\w]+', entry.content.lower()))
        words.update(re.findall(r'[\u4e00-\u9fff\w]+', entry.name.lower()))
        for word in words:
            if len(word) < 2:
                continue
            if word not in self._content_index:
                self._content_index[word] = set()
            self._content_index[word].add(entry.entry_id)

    def _unindex_content(self, entry: LorebookEntry):
        words = set(re.findall(r'[\u4e00-\u9fff\w]+', entry.content.lower()))
        words.update(re.findall(r'[\u4e00-\u9fff\w]+', entry.name.lower()))
        for word in words:
            if len(word) < 2:
                continue
            if word in self._content_index:
                self._content_index[word].discard(entry.entry_id)
                if not self._content_index[word]:
                    del self._content_index[word]

    def _save_version(self, entry_id: str, entry_data: dict):
        if entry_id not in self._version_history:
            self._version_history[entry_id] = []
        self._version_history[entry_id].append({
            "timestamp": datetime.now().isoformat(),
            "version": len(self._version_history[entry_id]) + 1,
            "data": entry_data,
        })
        if len(self._version_history[entry_id]) > 50:
            self._version_history[entry_id] = self._version_history[entry_id][-50:]

    def _levenshtein_distance(self, s1: str, s2: str) -> int:
        if len(s1) < len(s2):
            return self._levenshtein_distance(s2, s1)
        if len(s2) == 0:
            return len(s1)
        prev_row = list(range(len(s2) + 1))
        for i, c1 in enumerate(s1):
            curr_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = prev_row[j + 1] + 1
                deletions = curr_row[j] + 1
                substitutions = prev_row[j] + (c1 != c2)
                curr_row.append(min(insertions, deletions, substitutions))
            prev_row = curr_row
        return prev_row[-1]

    def _similarity_score(self, s1: str, s2: str) -> float:
        if not s1 or not s2:
            return 0.0
        max_len = max(len(s1), len(s2))
        if max_len == 0:
            return 1.0
        distance = self._levenshtein_distance(s1.lower(), s2.lower())
        return 1.0 - (distance / max_len)

    def _jaccard_similarity(self, set_a: Set[str], set_b: Set[str]) -> float:
        if not set_a or not set_b:
            return 0.0
        intersection = len(set_a & set_b)
        union = len(set_a | set_b)
        return intersection / union if union > 0 else 0.0

    def _extract_key_terms(self, text: str) -> Set[str]:
        chinese_words = set(re.findall(r'[\u4e00-\u9fff]{2,}', text.lower()))
        english_words = set(re.findall(r'[a-zA-Z]{3,}', text.lower()))
        return chinese_words | english_words

    def _calculate_completeness(self, entry: LorebookEntry) -> float:
        score = 0.0
        checks = 0

        if entry.name and entry.name.strip():
            score += 1
        checks += 1

        if entry.content and len(entry.content.strip()) > 20:
            score += min(len(entry.content.strip()) / 200, 1.0)
        checks += 1

        if entry.trigger_keywords:
            score += min(len(entry.trigger_keywords) / 5, 1.0)
        checks += 1

        if entry.category != EntryCategory.CUSTOM:
            score += 1
        checks += 1

        if entry.tags:
            score += min(len(entry.tags) / 3, 1.0)
        checks += 1

        if entry.notes and len(entry.notes.strip()) > 10:
            score += 0.5
        checks += 1

        return score / checks if checks > 0 else 0.0

    def add_entry(self, entry: LorebookEntry) -> str:
        if not entry.entry_id:
            entry.entry_id = str(uuid.uuid4())[:8]
        now = datetime.now().isoformat()
        if not entry.created_at:
            entry.created_at = now
        entry.updated_at = now
        entry.completeness = self._calculate_completeness(entry)
        self.entries[entry.entry_id] = entry
        self._index_all(entry)
        self._save_version(entry.entry_id, entry.to_dict())
        self.save()
        return entry.entry_id

    def update_entry(self, entry_id: str, **kwargs) -> bool:
        if entry_id not in self.entries:
            return False
        entry = self.entries[entry_id]
        old_keywords = list(entry.trigger_keywords)
        old_folder = entry.folder
        old_tags = list(entry.tags)

        self._unindex_all(entry)

        for key, value in kwargs.items():
            if hasattr(entry, key):
                setattr(entry, key, value)

        entry.updated_at = datetime.now().isoformat()
        entry.version += 1
        entry.completeness = self._calculate_completeness(entry)

        self._index_all(entry)
        self._save_version(entry_id, entry.to_dict())
        self.save()
        return True

    def remove_entry(self, entry_id: str) -> bool:
        if entry_id not in self.entries:
            return False
        self._unindex_all(self.entries[entry_id])
        del self.entries[entry_id]
        self.save()
        return True

    def get_entry(self, entry_id: str) -> Optional[LorebookEntry]:
        return self.entries.get(entry_id)

    def find_by_keyword(self, keyword: str) -> List[LorebookEntry]:
        kw_lower = keyword.lower()
        entry_ids = self._keyword_index.get(kw_lower, set())
        return [self.entries[eid] for eid in entry_ids if eid in self.entries]

    def find_by_category(self, category: EntryCategory) -> List[LorebookEntry]:
        return [e for e in self.entries.values() if e.category == category]

    def find_by_name(self, name: str) -> Optional[LorebookEntry]:
        name_lower = name.lower()
        for entry in self.entries.values():
            if entry.name.lower() == name_lower:
                return entry
            for alias in entry.aliases:
                if alias.lower() == name_lower:
                    return entry
        return None

    def find_by_folder(self, folder: str) -> List[LorebookEntry]:
        entry_ids = self._folder_index.get(folder, set())
        return [self.entries[eid] for eid in entry_ids if eid in self.entries]

    def find_by_tag(self, tag: str) -> List[LorebookEntry]:
        entry_ids = self._tag_index.get(tag.lower(), set())
        return [self.entries[eid] for eid in entry_ids if eid in self.entries]

    def list_folders(self) -> List[str]:
        return sorted(self._folder_index.keys())

    def list_tags(self) -> List[Tuple[str, int]]:
        return sorted(
            [(tag, len(ids)) for tag, ids in self._tag_index.items()],
            key=lambda x: x[1], reverse=True
        )

    def search(self, query: str, categories: List[EntryCategory] = None,
               folders: List[str] = None, tags: List[str] = None,
               active_only: bool = False, min_score: float = 0.3,
               max_results: int = 20) -> List[SearchResult]:
        """全文搜索 - 支持模糊匹配和内容搜索"""
        results: List[SearchResult] = []
        query_lower = query.lower()
        query_terms = self._extract_key_terms(query)

        for entry in self.entries.values():
            if active_only and not entry.is_active:
                continue
            if categories and entry.category not in categories:
                continue
            if folders and entry.folder not in folders:
                continue
            if tags and not set(tags) & set(entry.tags):
                continue

            best_score = 0.0
            match_type = ""
            matched_on = ""

            name_score = self._similarity_score(query, entry.name)
            if name_score > best_score:
                best_score = name_score
                match_type = "名称匹配"
                matched_on = entry.name

            for alias in entry.aliases:
                alias_score = self._similarity_score(query, alias)
                if alias_score > best_score:
                    best_score = alias_score
                    match_type = "别名匹配"
                    matched_on = alias

            for kw in entry.trigger_keywords:
                kw_score = self._similarity_score(query, kw)
                if kw_score > best_score:
                    best_score = kw_score
                    match_type = "关键词匹配"
                    matched_on = kw

            if query_lower in entry.content.lower():
                content_score = 0.85
                if content_score > best_score:
                    best_score = content_score
                    match_type = "内容匹配"
                    matched_on = "正文内容"

            if query_terms:
                entry_terms = self._extract_key_terms(entry.content)
                entry_terms.update(self._extract_key_terms(entry.name))
                term_score = self._jaccard_similarity(query_terms, entry_terms) * 0.7
                if term_score > best_score:
                    best_score = term_score
                    match_type = "语义匹配"
                    matched_on = "关键术语"

            if best_score >= min_score:
                results.append(SearchResult(
                    entry=entry, score=best_score,
                    match_type=match_type, matched_on=matched_on
                ))

        results.sort(key=lambda r: r.score, reverse=True)
        return results[:max_results]

    def fuzzy_find_keywords(self, text: str, threshold: float = None) -> List[Tuple[str, str, float]]:
        """在文本中模糊匹配关键词，返回(文本片段, 匹配关键词, 相似度)"""
        if threshold is None:
            threshold = self.fuzzy_match_threshold

        matches = []
        text_words = re.findall(r'[\u4e00-\u9fff\w]+', text.lower())

        for i, word in enumerate(text_words):
            if len(word) < 2:
                continue
            for keyword in self._keyword_index:
                score = self._similarity_score(word, keyword)
                if score >= threshold:
                    context_start = max(0, i - 2)
                    context_end = min(len(text_words), i + 3)
                    context = ''.join(text_words[context_start:context_end])
                    matches.append((context, keyword, score))

        matches.sort(key=lambda m: m[2], reverse=True)
        seen = set()
        unique_matches = []
        for ctx, kw, score in matches:
            if kw not in seen:
                seen.add(kw)
                unique_matches.append((ctx, kw, score))
        return unique_matches

    def trigger(self, text: str, current_chapter: int = 0,
                max_entries: int = None, use_fuzzy: bool = True) -> List[LorebookEntry]:
        """扫描文本，返回匹配的触发条目"""
        if max_entries is None:
            max_entries = self.max_entries_per_trigger

        text_lower = text.lower()
        triggered_ids: Set[str] = set()
        triggered_entries: List[LorebookEntry] = []

        for keyword, entry_ids in self._keyword_index.items():
            if keyword in text_lower:
                for eid in entry_ids:
                    if eid not in triggered_ids:
                        entry = self.entries.get(eid)
                        if entry and entry.is_active:
                            if entry.chapter_expires > 0 and current_chapter > entry.chapter_expires:
                                continue
                            triggered_ids.add(eid)
                            triggered_entries.append(entry)

        if use_fuzzy:
            fuzzy_matches = self.fuzzy_find_keywords(text)
            for _, kw, _ in fuzzy_matches:
                for eid in self._keyword_index.get(kw, set()):
                    if eid not in triggered_ids:
                        entry = self.entries.get(eid)
                        if entry and entry.is_active:
                            triggered_ids.add(eid)
                            triggered_entries.append(entry)

        triggered_entries.sort(key=lambda e: e.priority.weight, reverse=True)

        cascade_ids: Set[str] = set()
        for entry in triggered_entries[:max_entries]:
            for cascade_eid in entry.cascade_to:
                if cascade_eid not in triggered_ids and cascade_eid not in cascade_ids:
                    cascade_ids.add(cascade_eid)

        for eid in cascade_ids:
            entry = self.entries.get(eid)
            if entry and entry.is_active:
                triggered_entries.append(entry)

        result = triggered_entries[:max_entries]

        now = datetime.now().isoformat()
        for entry in result:
            entry.usage_count += 1
            entry.last_triggered = now

        return result

    def build_context(self, text: str, current_chapter: int = 0,
                      max_tokens: int = None) -> str:
        """构建注入上下文文本"""
        if max_tokens is None:
            max_tokens = self.max_context_tokens

        triggered = self.trigger(text, current_chapter)
        if not triggered:
            return ""

        context_parts = []
        total_chars = 0
        char_limit = max_tokens * 3

        for entry in triggered:
            header = f"[{entry.category.value}: {entry.name}]"
            body = entry.content
            part = f"{header}\n{body}"
            if total_chars + len(part) > char_limit:
                truncated = part[:char_limit - total_chars - 20] + "..."
                context_parts.append(truncated)
                break
            context_parts.append(part)
            total_chars += len(part)

        return "\n\n".join(context_parts)

    def batch_activate(self, entry_ids: List[str]) -> int:
        count = 0
        for eid in entry_ids:
            if eid in self.entries:
                self.entries[eid].is_active = True
                self.entries[eid].status = EntryStatus.ACTIVE
                count += 1
        if count:
            self.save()
        return count

    def batch_deactivate(self, entry_ids: List[str]) -> int:
        count = 0
        for eid in entry_ids:
            if eid in self.entries:
                self.entries[eid].is_active = False
                self.entries[eid].status = EntryStatus.ARCHIVED
                count += 1
        if count:
            self.save()
        return count

    def batch_delete(self, entry_ids: List[str]) -> int:
        count = 0
        for eid in entry_ids:
            if eid in self.entries:
                self._unindex_all(self.entries[eid])
                del self.entries[eid]
                count += 1
        if count:
            self.save()
        return count

    def batch_update(self, entry_ids: List[str], **kwargs) -> int:
        count = 0
        for eid in entry_ids:
            if eid in self.entries:
                self.update_entry(eid, **kwargs)
                count += 1
        return count

    def move_to_folder(self, entry_ids: List[str], folder: str) -> int:
        count = 0
        for eid in entry_ids:
            if eid in self.entries:
                self.update_entry(eid, folder=folder)
                count += 1
        return count

    def add_tags(self, entry_ids: List[str], tags: List[str]) -> int:
        count = 0
        for eid in entry_ids:
            if eid in self.entries:
                entry = self.entries[eid]
                new_tags = list(set(entry.tags) | set(tags))
                self.update_entry(eid, tags=new_tags)
                count += 1
        return count

    def detect_conflicts(self) -> List[EntryConflict]:
        """检测条目间的潜在冲突"""
        conflicts = []
        entry_list = list(self.entries.values())

        for i in range(len(entry_list)):
            for j in range(i + 1, len(entry_list)):
                a = entry_list[i]
                b = entry_list[j]

                if a.category != b.category:
                    continue

                a_terms = self._extract_key_terms(a.content)
                b_terms = self._extract_key_terms(b.content)
                similarity = self._jaccard_similarity(a_terms, b_terms)

                if similarity < 0.3:
                    continue

                conflicting_fields = []

                if a.name.lower() == b.name.lower() and a.entry_id != b.entry_id:
                    conflicting_fields.append("名称重复")
                    conflicts.append(EntryConflict(
                        entry_a=a, entry_b=b,
                        severity=ConflictSeverity.CRITICAL,
                        description=f"两个条目名称相同: '{a.name}'",
                        conflicting_fields=conflicting_fields,
                    ))
                    continue

                a_lines = {line.split('：')[0].strip() for line in a.content.split('\n') if '：' in line}
                b_lines = {line.split('：')[0].strip() for line in b.content.split('\n') if '：' in line}
                common_fields = a_lines & b_lines

                if common_fields:
                    for field in common_fields:
                        a_val = next((line.split('：')[1].strip() for line in a.content.split('\n')
                                      if line.startswith(field)), "")
                        b_val = next((line.split('：')[1].strip() for line in b.content.split('\n')
                                      if line.startswith(field)), "")
                        if a_val and b_val and a_val != b_val:
                            conflicting_fields.append(field)

                if conflicting_fields:
                    severity = ConflictSeverity.MAJOR if len(conflicting_fields) > 1 else ConflictSeverity.MINOR
                    conflicts.append(EntryConflict(
                        entry_a=a, entry_b=b,
                        severity=severity,
                        description=f"字段冲突: {', '.join(conflicting_fields)}",
                        conflicting_fields=conflicting_fields,
                    ))

        conflicts.sort(key=lambda c: c.severity.score, reverse=True)
        return conflicts

    def suggest_related(self, entry_id: str, max_suggestions: int = 5) -> List[LorebookEntry]:
        """基于内容相似度推荐关联条目"""
        if entry_id not in self.entries:
            return []

        source = self.entries[entry_id]
        source_terms = self._extract_key_terms(source.content)
        source_terms.update(self._extract_key_terms(source.name))

        scored = []
        for other in self.entries.values():
            if other.entry_id == entry_id:
                continue
            other_terms = self._extract_key_terms(other.content)
            other_terms.update(self._extract_key_terms(other.name))
            score = self._jaccard_similarity(source_terms, other_terms)

            if source.category == other.category:
                score *= 1.3

            if other.entry_id in source.related_entries:
                score *= 1.5

            if score > 0.1:
                scored.append((other, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        return [entry for entry, _ in scored[:max_suggestions]]

    def suggest_keywords(self, entry_id: str, max_suggestions: int = 8) -> List[str]:
        """为条目智能推荐触发关键词"""
        if entry_id not in self.entries:
            return []

        entry = self.entries[entry_id]
        content_terms = self._extract_key_terms(entry.content)
        name_terms = self._extract_key_terms(entry.name)

        existing_kw = set(kw.lower() for kw in entry.trigger_keywords)

        candidates = set()
        candidates.update(name_terms)
        candidates.update(content_terms)

        for term in name_terms:
            for ct in content_terms:
                if term in ct and term != ct:
                    candidates.add(ct)

        candidates.difference_update(existing_kw)

        scored = []
        for candidate in candidates:
            if len(candidate) < 2:
                continue
            score = 0
            if candidate in entry.name:
                score += 3
            if candidate in entry.content:
                score += 1
            if len(candidate) >= 3:
                score += 1
            scored.append((candidate, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        return [kw for kw, _ in scored[:max_suggestions]]

    def analyze_triggers(self) -> List[TriggerAnalysis]:
        """分析触发效率"""
        analyses = []
        total_chapters = max(
            (e.chapter_introduced for e in self.entries.values() if e.chapter_introduced > 0),
            default=1
        )

        for entry in self.entries.values():
            kw_effectiveness = {}
            for kw in entry.trigger_keywords:
                kw_effectiveness[kw] = entry.usage_count

            cascade_eff = 0.0
            if entry.cascade_to:
                cascade_triggers = sum(
                    self.entries[eid].usage_count
                    for eid in entry.cascade_to if eid in self.entries
                )
                cascade_eff = cascade_triggers / len(entry.cascade_to) if entry.cascade_to else 0

            trigger_rate = entry.usage_count / max(total_chapters, 1)

            if trigger_rate < 0.5:
                recommendation = "建议增加触发关键词或降低优先级"
            elif trigger_rate > 5:
                recommendation = "触发频繁，检查是否关键词过于宽泛"
            elif entry.usage_count == 0:
                recommendation = "从未被触发，检查关键词是否有效"
            else:
                recommendation = "触发效率正常"

            analyses.append(TriggerAnalysis(
                entry_id=entry.entry_id,
                entry_name=entry.name,
                total_triggers=entry.usage_count,
                trigger_rate=round(trigger_rate, 2),
                keywords_effectiveness=kw_effectiveness,
                cascade_effectiveness=round(cascade_eff, 2),
                recommendation=recommendation,
            ))

        analyses.sort(key=lambda a: a.total_triggers, reverse=True)
        return analyses

    def get_stats(self) -> dict:
        total = len(self.entries)
        by_category = {}
        for cat in EntryCategory:
            count = len(self.find_by_category(cat))
            if count > 0:
                by_category[cat.value] = count

        by_status = {}
        for status in EntryStatus:
            count = sum(1 for e in self.entries.values() if e.status == status)
            if count > 0:
                by_status[status.value] = count

        total_triggers = sum(e.usage_count for e in self.entries.values())
        active = sum(1 for e in self.entries.values() if e.is_active)

        avg_completeness = (
            sum(e.completeness for e in self.entries.values()) / total
            if total > 0 else 0
        )

        unused = sum(1 for e in self.entries.values() if e.usage_count == 0 and e.is_active)

        return {
            "total_entries": total,
            "active_entries": active,
            "by_category": by_category,
            "by_status": by_status,
            "total_triggers": total_triggers,
            "keyword_count": len(self._keyword_index),
            "folder_count": len(self._folder_index),
            "tag_count": len(self._tag_index),
            "avg_completeness": round(avg_completeness, 2),
            "unused_entries": unused,
        }

    def get_dashboard(self) -> dict:
        """获取完整分析仪表盘数据"""
        stats = self.get_stats()
        conflicts = self.detect_conflicts()
        trigger_analysis = self.analyze_triggers()

        top_triggered = trigger_analysis[:5]
        never_triggered = [a for a in trigger_analysis if a.total_triggers == 0]
        over_triggered = [a for a in trigger_analysis if a.trigger_rate > 5]

        return {
            "stats": stats,
            "conflict_count": len(conflicts),
            "critical_conflicts": [c for c in conflicts if c.severity == ConflictSeverity.CRITICAL],
            "top_triggered": [
                {"name": a.entry_name, "triggers": a.total_triggers, "rate": a.trigger_rate}
                for a in top_triggered
            ],
            "never_triggered_count": len(never_triggered),
            "over_triggered_count": len(over_triggered),
            "recommendations": [
                a.recommendation for a in trigger_analysis
                if a.recommendation != "触发效率正常"
            ][:10],
        }

    def get_entry_versions(self, entry_id: str) -> List[dict]:
        return self._version_history.get(entry_id, [])

    def restore_version(self, entry_id: str, version_index: int) -> bool:
        if entry_id not in self._version_history:
            return False
        versions = self._version_history[entry_id]
        if version_index < 0 or version_index >= len(versions):
            return False

        old_data = versions[version_index]["data"]
        entry = LorebookEntry.from_dict(old_data)
        self._unindex_all(self.entries[entry_id])
        self.entries[entry_id] = entry
        self._index_all(entry)
        entry.version += 1
        entry.updated_at = datetime.now().isoformat()
        self._save_version(entry_id, entry.to_dict())
        self.save()
        return True

    def export_entries(self, filepath: str, category: EntryCategory = None,
                       folder: str = None, format: str = "json") -> int:
        entries = list(self.entries.values())
        if category:
            entries = [e for e in entries if e.category == category]
        if folder:
            entries = [e for e in entries if e.folder == folder]

        if format == "csv":
            return self._export_csv(filepath, entries)
        else:
            return self._export_json(filepath, entries)

    def _export_json(self, filepath: str, entries: List[LorebookEntry]) -> int:
        data = {
            "exported_at": datetime.now().isoformat(),
            "format_version": "2.0",
            "entry_count": len(entries),
            "entries": [e.to_dict() for e in entries],
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return len(entries)

    def _export_csv(self, filepath: str, entries: List[LorebookEntry]) -> int:
        fieldnames = [
            "entry_id", "name", "category", "content", "trigger_keywords",
            "priority", "cascade_to", "chapter_introduced", "chapter_expires",
            "is_active", "status", "folder", "tags", "aliases", "notes"
        ]
        with open(filepath, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            for entry in entries:
                row = entry.to_dict()
                row["trigger_keywords"] = "|".join(entry.trigger_keywords)
                row["cascade_to"] = "|".join(entry.cascade_to)
                row["tags"] = "|".join(entry.tags)
                row["aliases"] = "|".join(entry.aliases)
                writer.writerow(row)
        return len(entries)

    def import_entries(self, filepath: str, format: str = None) -> int:
        if format is None:
            ext = os.path.splitext(filepath)[1].lower()
            format = "csv" if ext == ".csv" else "json"

        if format == "csv":
            return self._import_csv(filepath)
        else:
            return self._import_json(filepath)

    def _import_json(self, filepath: str) -> int:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        count = 0
        for entry_data in data.get("entries", []):
            entry = LorebookEntry.from_dict(entry_data)
            if entry.entry_id in self.entries:
                entry.entry_id = str(uuid.uuid4())[:8]
            self.add_entry(entry)
            count += 1
        return count

    def _import_csv(self, filepath: str) -> int:
        count = 0
        with open(filepath, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                entry = LorebookEntry(
                    entry_id=row.get("entry_id", str(uuid.uuid4())[:8]),
                    name=row.get("name", ""),
                    category=EntryCategory(row.get("category", "自定义")),
                    content=row.get("content", ""),
                    trigger_keywords=[kw.strip() for kw in row.get("trigger_keywords", "").split("|") if kw.strip()],
                    priority=EntryPriority(int(row.get("priority", 3))),
                    cascade_to=[eid.strip() for eid in row.get("cascade_to", "").split("|") if eid.strip()],
                    chapter_introduced=int(row.get("chapter_introduced", 0)),
                    chapter_expires=int(row.get("chapter_expires", 0)),
                    is_active=row.get("is_active", "True").lower() == "true",
                    status=EntryStatus(row.get("status", "活跃")),
                    folder=row.get("folder", ""),
                    tags=[t.strip() for t in row.get("tags", "").split("|") if t.strip()],
                    aliases=[a.strip() for a in row.get("aliases", "").split("|") if a.strip()],
                    notes=row.get("notes", ""),
                )
                if entry.entry_id in self.entries:
                    entry.entry_id = str(uuid.uuid4())[:8]
                self.add_entry(entry)
                count += 1
        return count

    def get_templates(self, genre: str = None) -> List[dict]:
        """获取按题材分类的条目模板"""
        templates_path = self._get_templates_path()
        if os.path.exists(templates_path):
            with open(templates_path, "r", encoding="utf-8") as f:
                all_templates = json.load(f)
        else:
            all_templates = self._build_template_library()

        if genre:
            return [t for t in all_templates if t.get("genre") == genre]
        return all_templates

    def create_from_template(self, template_id: str, overrides: dict = None) -> Optional[str]:
        """从模板创建条目"""
        templates = self.get_templates()
        template = next((t for t in templates if t.get("id") == template_id), None)
        if not template:
            return None

        entry = LorebookEntry(
            entry_id=str(uuid.uuid4())[:8],
            name=template.get("name", "新条目"),
            category=EntryCategory(template.get("category", "自定义")),
            content=template.get("content", ""),
            trigger_keywords=template.get("trigger_keywords", []),
            priority=EntryPriority(template.get("priority", 3)),
            tags=template.get("tags", []),
            notes=template.get("notes", ""),
        )

        if overrides:
            for key, value in overrides.items():
                if hasattr(entry, key):
                    setattr(entry, key, value)

        return self.add_entry(entry)

    def _build_template_library(self) -> List[dict]:
        """构建按题材分类的模板库"""
        templates = [
            {
                "id": "tpl_xianxia_protagonist",
                "genre": "仙侠",
                "name": "仙侠主角模板",
                "category": "角色",
                "content": "姓名：[待设定]\n道号：[待设定]\n性别：[待设定]\n年龄/骨龄：[待设定]\n外貌特征：[待设定]\n灵根属性：[待设定]\n修为境界：炼气期→筑基期→金丹期→元婴期→化神期→合体期→大乘期→渡劫期\n本命法宝：[待设定]\n核心功法：[待设定]\n性格特点：[待设定]\n背景故事：[待设定]\n修仙动机：[待设定]\n金手指：[待设定]",
                "trigger_keywords": ["主角", "主人公", "修士"],
                "priority": 5,
                "tags": ["仙侠", "主角", "模板"],
            },
            {
                "id": "tpl_xianxia_sect",
                "genre": "仙侠",
                "name": "仙侠宗门模板",
                "category": "势力",
                "content": "宗门名称：[待设定]\n宗门等级：下等→中等→上等→顶级→圣地\n掌门/宗主：[待设定]\n太上长老：[待设定]\n核心弟子：[待设定]\n宗门功法：[待设定]\n宗门位置：[待设定]\n护山大阵：[待设定]\n宗门历史：[待设定]\n敌对势力：[待设定]\n盟友势力：[待设定]",
                "trigger_keywords": ["宗门", "门派", "势力"],
                "priority": 4,
                "tags": ["仙侠", "宗门", "势力"],
            },
            {
                "id": "tpl_xianxia_realm",
                "genre": "仙侠",
                "name": "修仙境界体系",
                "category": "规则",
                "content": "境界体系：\n第一境：[待设定] - 寿元X年，能力描述\n第二境：[待设定] - 寿元X年，能力描述\n第三境：[待设定] - 寿元X年，能力描述\n第四境：[待设定] - 寿元X年，能力描述\n第五境：[待设定] - 寿元X年，能力描述\n\n突破条件：[待设定]\n天劫设定：[待设定]\n境界压制规则：[待设定]",
                "trigger_keywords": ["境界", "修为", "突破", "升级"],
                "priority": 5,
                "tags": ["仙侠", "境界", "体系"],
            },
            {
                "id": "tpl_xuanhuan_protagonist",
                "genre": "玄幻",
                "name": "玄幻主角模板",
                "category": "角色",
                "content": "姓名：[待设定]\n性别：[待设定]\n年龄：[待设定]\n外貌特征：[待设定]\n血脉/体质：[待设定]\n斗气/魔力等级：斗者→斗师→大斗师→斗灵→斗王→斗皇→斗宗→斗尊→斗圣→斗帝\n核心斗技/魔法：[待设定]\n契约兽/魔宠：[待设定]\n性格特点：[待设定]\n背景故事：[待设定]\n核心动机：[待设定]\n金手指：[待设定]",
                "trigger_keywords": ["主角", "主人公", "斗者", "魔法师"],
                "priority": 5,
                "tags": ["玄幻", "主角", "模板"],
            },
            {
                "id": "tpl_xuanhuan_world",
                "genre": "玄幻",
                "name": "玄幻大陆设定",
                "category": "规则",
                "content": "大陆名称：[待设定]\n大陆格局：东域/西域/南域/北域/中州\n主要种族：人族/精灵/矮人/兽人/龙族/魔族\n力量体系：斗气/魔法/武魂/血脉\n主要帝国：[待设定]\n学院/宗门：[待设定]\n禁地/秘境：[待设定]\n上古遗迹：[待设定]\n历史大事件：[待设定]",
                "trigger_keywords": ["大陆", "世界", "设定", "格局"],
                "priority": 4,
                "tags": ["玄幻", "世界观", "设定"],
            },
            {
                "id": "tpl_urban_protagonist",
                "genre": "都市",
                "name": "都市主角模板",
                "category": "角色",
                "content": "姓名：[待设定]\n性别：[待设定]\n年龄：[待设定]\n职业：[待设定]\n外貌特征：[待设定]\n特殊能力/背景：兵王回归/神医传人/修真者入世/重生者/系统拥有者\n社会关系：[待设定]\n财富状况：[待设定]\n性格特点：[待设定]\n核心冲突：[待设定]\n成长目标：[待设定]",
                "trigger_keywords": ["主角", "主人公", "总裁", "兵王"],
                "priority": 5,
                "tags": ["都市", "主角", "模板"],
            },
            {
                "id": "tpl_urban_power",
                "genre": "都市",
                "name": "都市势力格局",
                "category": "势力",
                "content": "势力名称：[待设定]\n势力类型：家族/公司/地下势力/官方组织\n势力等级：三流→二流→一流→顶级→霸主\n掌权者：[待设定]\n核心成员：[待设定]\n势力范围：[待设定]\n资产规模：[待设定]\n敌对势力：[待设定]\n盟友势力：[待设定]",
                "trigger_keywords": ["家族", "公司", "势力", "集团"],
                "priority": 3,
                "tags": ["都市", "势力", "格局"],
            },
            {
                "id": "tpl_suspense_case",
                "genre": "悬疑",
                "name": "悬疑案件模板",
                "category": "事件",
                "content": "案件名称：[待设定]\n案件类型：谋杀/失踪/盗窃/绑架/阴谋\n案发时间：[待设定]\n案发地点：[待设定]\n受害者：[待设定]\n嫌疑人列表：[待设定]\n关键线索：[待设定]\n红鲱鱼(误导线索)：[待设定]\n真相：[待设定]\n反转点：[待设定]\n与主线关联：[待设定]",
                "trigger_keywords": ["案件", "线索", "调查", "真相"],
                "priority": 4,
                "tags": ["悬疑", "案件", "推理"],
            },
            {
                "id": "tpl_suspense_clue",
                "genre": "悬疑",
                "name": "线索链模板",
                "category": "概念",
                "content": "线索编号：[待设定]\n发现章节：[待设定]\n发现方式：[待设定]\n线索内容：[待设定]\n表面含义：[待设定]\n真实含义：[待设定]\n指向的下一条线索：[待设定]\n关联人物：[待设定]\n是否已被解读：[待设定]",
                "trigger_keywords": ["线索", "证据", "发现"],
                "priority": 3,
                "tags": ["悬疑", "线索", "推理"],
            },
            {
                "id": "tpl_scifi_tech",
                "genre": "科幻",
                "name": "科幻科技设定",
                "category": "概念",
                "content": "技术名称：[待设定]\n技术等级：民用/军用/禁忌/失落科技\n技术原理：[待设定]\n发明者/发现者：[待设定]\n应用场景：[待设定]\n技术限制：[待设定]\n副作用/代价：[待设定]\n社会影响：[待设定]\n相关技术：[待设定]",
                "trigger_keywords": ["科技", "技术", "发明", "装置"],
                "priority": 3,
                "tags": ["科幻", "科技", "设定"],
            },
            {
                "id": "tpl_scifi_world",
                "genre": "科幻",
                "name": "科幻世界观设定",
                "category": "规则",
                "content": "时代设定：近未来(50年)/远未来(500年)/星际时代\n人类状态：地球文明/星际殖民/后末日\n科技水平：[待设定]\n社会制度：[待设定]\n外星文明：[待设定]\nAI地位：[待设定]\n核心矛盾：[待设定]\n历史关键事件：[待设定]",
                "trigger_keywords": ["未来", "星际", "文明", "时代"],
                "priority": 4,
                "tags": ["科幻", "世界观", "设定"],
            },
            {
                "id": "tpl_romance_couple",
                "genre": "言情",
                "name": "言情CP模板",
                "category": "角色",
                "content": "角色A姓名：[待设定]\n角色B姓名：[待设定]\n初遇场景：[待设定]\n初遇章节：[待设定]\n关系发展阶段：陌生人→相识→暧昧→确定关系→矛盾→分离→重逢→HE/BE\n性格互补/冲突：[待设定]\n共同经历：[待设定]\n关系障碍：家庭反对/身份差距/误会/第三者/命运\n甜蜜时刻：[待设定]\n虐心时刻：[待设定]",
                "trigger_keywords": ["CP", "情侣", "感情", "恋爱"],
                "priority": 4,
                "tags": ["言情", "CP", "感情线"],
            },
            {
                "id": "tpl_history_dynasty",
                "genre": "历史",
                "name": "历史朝代设定",
                "category": "规则",
                "content": "朝代名称：[待设定]\n参考历史朝代：[待设定]\n在位皇帝：[待设定]\n年号：[待设定]\n政治制度：[待设定]\n官僚体系：[待设定]\n军事制度：[待设定]\n经济状况：[待设定]\n文化特点：[待设定]\n外部威胁：[待设定]\n内部矛盾：[待设定]",
                "trigger_keywords": ["朝代", "朝廷", "皇帝", "天下"],
                "priority": 4,
                "tags": ["历史", "朝代", "设定"],
            },
            {
                "id": "tpl_game_system",
                "genre": "游戏",
                "name": "游戏系统设定",
                "category": "规则",
                "content": "游戏名称：[待设定]\n游戏类型：MMORPG/VR沉浸式/全息/异界游戏\n等级系统：[待设定]\n职业体系：[待设定]\n技能系统：[待设定]\n装备系统：[待设定]\n货币系统：[待设定]\n公会/阵营：[待设定]\n副本/任务：[待设定]\n特殊机制：[待设定]\n现实与游戏关联：[待设定]",
                "trigger_keywords": ["系统", "等级", "技能", "装备", "副本"],
                "priority": 5,
                "tags": ["游戏", "系统", "设定"],
            },
            {
                "id": "tpl_horror_entity",
                "genre": "恐怖",
                "name": "恐怖存在模板",
                "category": "概念",
                "content": "存在名称：[待设定]\n存在类型：鬼魂/诅咒/怪物/不可名状/心理恐怖\n起源：[待设定]\n出现规律：[待设定]\n能力/特性：[待设定]\n弱点/克制方法：[待设定]\n受害者特征：[待设定]\n恐怖等级：心理不适→轻度恐惧→极度恐惧→SAN值归零\n与主线关联：[待设定]",
                "trigger_keywords": ["鬼", "怪物", "恐怖", "诅咒"],
                "priority": 4,
                "tags": ["恐怖", "怪物", "设定"],
            },
        ]

        with open(self._get_templates_path(), "w", encoding="utf-8") as f:
            json.dump(templates, f, ensure_ascii=False, indent=2)

        return templates

    def _init_default_entries(self):
        defaults = [
            LorebookEntry(
                entry_id="tpl_protagonist",
                name="主角模板",
                category=EntryCategory.CHARACTER,
                content="姓名：[待设定]\n性别：[待设定]\n年龄：[待设定]\n外貌特征：[待设定]\n性格特点：[待设定]\n核心能力：[待设定]\n背景故事：[待设定]\n核心动机：[待设定]",
                trigger_keywords=["主角", "主人公"],
                priority=EntryPriority.CRITICAL,
                tags=["模板", "主角"],
            ),
            LorebookEntry(
                entry_id="tpl_world",
                name="世界观模板",
                category=EntryCategory.RULE,
                content="世界名称：[待设定]\n时代背景：[待设定]\n力量体系：[待设定]\n社会结构：[待设定]\n主要势力：[待设定]\n核心冲突：[待设定]",
                trigger_keywords=["世界", "设定", "背景"],
                priority=EntryPriority.HIGH,
                tags=["模板", "世界观"],
            ),
            LorebookEntry(
                entry_id="tpl_location",
                name="地点模板",
                category=EntryCategory.LOCATION,
                content="地点名称：[待设定]\n地理位置：[待设定]\n环境特征：[待设定]\n所属势力：[待设定]\n重要事件：[待设定]",
                trigger_keywords=["地点", "场景", "位置"],
                priority=EntryPriority.MEDIUM,
                tags=["模板", "地点"],
            ),
        ]
        for entry in defaults:
            entry.completeness = self._calculate_completeness(entry)
            self.entries[entry.entry_id] = entry
            self._index_all(entry)
        self.save()
