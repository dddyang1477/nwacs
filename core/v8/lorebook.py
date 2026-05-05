#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS Lorebook - 触发式设定注入系统

对标 NovelAI Lorebook，核心能力：
1. 设定条目管理 - 角色/地点/物品/概念/事件
2. 触发关键词 - 关键词出现时自动注入相关设定
3. 级联触发 - 条目A触发后可连带触发条目B
4. 上下文预算管理 - 智能控制注入量，避免超token
5. 优先级排序 - 高优先级条目优先注入
6. 动态更新 - 随故事推进自动更新条目内容

设计原则：
- 纯本地计算，零API依赖
- JSON持久化，支持导入导出
- 与NovelMemoryManager无缝集成
"""

import json
import os
import re
from datetime import datetime
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum


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
        }

    @classmethod
    def from_dict(cls, data: dict) -> "LorebookEntry":
        priority_map = {p.weight: p for p in EntryPriority}
        category_map = {c.value: c for c in EntryCategory}
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
        )


class Lorebook:
    """触发式设定注入系统"""

    def __init__(self, storage_dir: str = None):
        if storage_dir is None:
            storage_dir = os.path.join(os.path.dirname(__file__), "..", "lorebook_storage")
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)

        self.entries: Dict[str, LorebookEntry] = {}
        self._keyword_index: Dict[str, Set[str]] = {}
        self._load()

        self.max_context_tokens = 4000
        self.max_entries_per_trigger = 8

    def _get_filepath(self) -> str:
        return os.path.join(self.storage_dir, "lorebook.json")

    def _load(self):
        filepath = self._get_filepath()
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            for entry_data in data.get("entries", []):
                entry = LorebookEntry.from_dict(entry_data)
                self.entries[entry.entry_id] = entry
                self._index_keywords(entry)
        else:
            self._init_default_entries()

    def save(self):
        data = {
            "version": "1.0",
            "updated_at": datetime.now().isoformat(),
            "total_entries": len(self.entries),
            "entries": [e.to_dict() for e in self.entries.values()],
        }
        with open(self._get_filepath(), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

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

    def add_entry(self, entry: LorebookEntry) -> str:
        if not entry.entry_id:
            import uuid
            entry.entry_id = str(uuid.uuid4())[:8]
        self.entries[entry.entry_id] = entry
        self._index_keywords(entry)
        self.save()
        return entry.entry_id

    def update_entry(self, entry_id: str, **kwargs) -> bool:
        if entry_id not in self.entries:
            return False
        entry = self.entries[entry_id]
        old_keywords = list(entry.trigger_keywords)
        for key, value in kwargs.items():
            if hasattr(entry, key):
                setattr(entry, key, value)
        if "trigger_keywords" in kwargs:
            self._unindex_keywords(LorebookEntry(
                entry_id=entry_id, name="", category=EntryCategory.CUSTOM,
                content="", trigger_keywords=old_keywords
            ))
            self._index_keywords(entry)
        self.save()
        return True

    def remove_entry(self, entry_id: str) -> bool:
        if entry_id not in self.entries:
            return False
        self._unindex_keywords(self.entries[entry_id])
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
        return None

    def trigger(self, text: str, current_chapter: int = 0,
                max_entries: int = None) -> List[LorebookEntry]:
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

    def get_stats(self) -> dict:
        total = len(self.entries)
        by_category = {}
        for cat in EntryCategory:
            count = len(self.find_by_category(cat))
            if count > 0:
                by_category[cat.value] = count

        total_triggers = sum(e.usage_count for e in self.entries.values())
        active = sum(1 for e in self.entries.values() if e.is_active)

        return {
            "total_entries": total,
            "active_entries": active,
            "by_category": by_category,
            "total_triggers": total_triggers,
            "keyword_count": len(self._keyword_index),
        }

    def export_entries(self, filepath: str, category: EntryCategory = None):
        entries = list(self.entries.values())
        if category:
            entries = [e for e in entries if e.category == category]
        data = {
            "exported_at": datetime.now().isoformat(),
            "entries": [e.to_dict() for e in entries],
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def import_entries(self, filepath: str) -> int:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        count = 0
        for entry_data in data.get("entries", []):
            entry = LorebookEntry.from_dict(entry_data)
            if entry.entry_id not in self.entries:
                self.entries[entry.entry_id] = entry
                self._index_keywords(entry)
                count += 1
        self.save()
        return count

    def _init_default_entries(self):
        """初始化默认条目模板"""
        defaults = [
            LorebookEntry(
                entry_id="tpl_protagonist",
                name="主角模板",
                category=EntryCategory.CHARACTER,
                content="姓名：[待设定]\n性别：[待设定]\n年龄：[待设定]\n外貌特征：[待设定]\n性格特点：[待设定]\n核心能力：[待设定]\n背景故事：[待设定]\n核心动机：[待设定]",
                trigger_keywords=["主角", "主人公"],
                priority=EntryPriority.CRITICAL,
            ),
            LorebookEntry(
                entry_id="tpl_world",
                name="世界观模板",
                category=EntryCategory.RULE,
                content="世界名称：[待设定]\n时代背景：[待设定]\n力量体系：[待设定]\n社会结构：[待设定]\n主要势力：[待设定]\n核心冲突：[待设定]",
                trigger_keywords=["世界", "设定", "背景"],
                priority=EntryPriority.HIGH,
            ),
            LorebookEntry(
                entry_id="tpl_location",
                name="地点模板",
                category=EntryCategory.LOCATION,
                content="地点名称：[待设定]\n地理位置：[待设定]\n环境特征：[待设定]\n所属势力：[待设定]\n重要事件：[待设定]",
                trigger_keywords=["地点", "场景", "位置"],
                priority=EntryPriority.MEDIUM,
            ),
        ]
        for entry in defaults:
            self.entries[entry.entry_id] = entry
            self._index_keywords(entry)
        self.save()
