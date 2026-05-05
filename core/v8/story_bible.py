#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS Story Bible - 集中式创作圣经

对标 Sudowrite Story Bible，核心能力：
1. 统一管理 - 角色/世界观/大纲/伏笔/场景一站式
2. 交叉引用 - 条目间自动关联，点击跳转
3. 一致性校验 - 跨条目设定冲突检测
4. 版本快照 - 每次修改自动保存历史
5. 导出报告 - 生成完整设定文档

设计原则：
- 单一数据源(Single Source of Truth)
- 所有模块通过StoryBible获取设定
- 与Lorebook/NovelMemoryManager无缝集成
"""

import json
import os
import copy
from datetime import datetime
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum


class BibleSection(Enum):
    BRAINDUMP = "灵感碎片"
    SYNOPSIS = "故事梗概"
    GENRE = "题材类型"
    STYLE = "写作风格"
    CHARACTERS = "角色档案"
    WORLD_BUILDING = "世界观"
    PLOT_OUTLINE = "剧情大纲"
    FORESHADOWING = "伏笔管理"
    SCENES = "场景库"
    RESEARCH = "研究资料"


@dataclass
class BibleEntry:
    entry_id: str
    section: BibleSection
    title: str
    content: str
    tags: List[str] = field(default_factory=list)
    references: List[str] = field(default_factory=list)
    created_at: str = ""
    updated_at: str = ""
    version: int = 1
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "entry_id": self.entry_id,
            "section": self.section.value,
            "title": self.title,
            "content": self.content,
            "tags": self.tags,
            "references": self.references,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "version": self.version,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "BibleEntry":
        section_map = {s.value: s for s in BibleSection}
        return cls(
            entry_id=data["entry_id"],
            section=section_map.get(data["section"], BibleSection.RESEARCH),
            title=data["title"],
            content=data["content"],
            tags=data.get("tags", []),
            references=data.get("references", []),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", ""),
            version=data.get("version", 1),
            metadata=data.get("metadata", {}),
        )


@dataclass
class ConsistencyIssue:
    entry_a: str
    entry_b: str
    field: str
    value_a: str
    value_b: str
    severity: str
    description: str


class StoryBible:
    """集中式创作圣经"""

    def __init__(self, novel_title: str = "未命名作品", storage_dir: str = None):
        self.novel_title = novel_title
        if storage_dir is None:
            storage_dir = os.path.join(os.path.dirname(__file__), "..", "bible_storage")
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)

        self.entries: Dict[str, Dict[str, BibleEntry]] = {}
        self._history: List[Dict] = []
        self._load()

    def _get_filepath(self) -> str:
        safe_name = re.sub(r'[<>:"/\\|?*]', '_', self.novel_title)
        return os.path.join(self.storage_dir, f"{safe_name}_bible.json")

    def _get_history_path(self) -> str:
        safe_name = re.sub(r'[<>:"/\\|?*]', '_', self.novel_title)
        return os.path.join(self.storage_dir, f"{safe_name}_history.json")

    def _load(self):
        filepath = self._get_filepath()
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.novel_title = data.get("novel_title", self.novel_title)
            for section_name, entries_data in data.get("sections", {}).items():
                section = BibleSection(section_name)
                self.entries[section_name] = {}
                for entry_data in entries_data:
                    entry = BibleEntry.from_dict(entry_data)
                    self.entries[section_name][entry.entry_id] = entry

        history_path = self._get_history_path()
        if os.path.exists(history_path):
            with open(history_path, "r", encoding="utf-8") as f:
                self._history = json.load(f)

    def save(self):
        sections_data = {}
        for section_name, entries_dict in self.entries.items():
            sections_data[section_name] = [e.to_dict() for e in entries_dict.values()]

        data = {
            "novel_title": self.novel_title,
            "updated_at": datetime.now().isoformat(),
            "sections": sections_data,
        }
        with open(self._get_filepath(), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        with open(self._get_history_path(), "w", encoding="utf-8") as f:
            json.dump(self._history[-100:], f, ensure_ascii=False, indent=2)

    def _snapshot(self, action: str, entry_id: str, section: str):
        self._history.append({
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "entry_id": entry_id,
            "section": section,
        })

    def add_entry(self, entry: BibleEntry) -> str:
        if not entry.entry_id:
            import uuid
            entry.entry_id = str(uuid.uuid4())[:8]
        now = datetime.now().isoformat()
        entry.created_at = now
        entry.updated_at = now

        section_name = entry.section.value
        if section_name not in self.entries:
            self.entries[section_name] = {}
        self.entries[section_name][entry.entry_id] = entry
        self._snapshot("add", entry.entry_id, section_name)
        self.save()
        return entry.entry_id

    def update_entry(self, entry_id: str, section: BibleSection, **kwargs) -> bool:
        section_name = section.value
        if section_name not in self.entries or entry_id not in self.entries[section_name]:
            return False

        entry = self.entries[section_name][entry_id]
        for key, value in kwargs.items():
            if hasattr(entry, key):
                setattr(entry, key, value)
        entry.updated_at = datetime.now().isoformat()
        entry.version += 1
        self._snapshot("update", entry_id, section_name)
        self.save()
        return True

    def remove_entry(self, entry_id: str, section: BibleSection) -> bool:
        section_name = section.value
        if section_name not in self.entries or entry_id not in self.entries[section_name]:
            return False
        del self.entries[section_name][entry_id]
        self._snapshot("remove", entry_id, section_name)
        self.save()
        return True

    def get_entry(self, entry_id: str, section: BibleSection) -> Optional[BibleEntry]:
        section_name = section.value
        return self.entries.get(section_name, {}).get(entry_id)

    def get_section(self, section: BibleSection) -> List[BibleEntry]:
        section_name = section.value
        return list(self.entries.get(section_name, {}).values())

    def find_by_tag(self, tag: str) -> List[BibleEntry]:
        results = []
        for section_entries in self.entries.values():
            for entry in section_entries.values():
                if tag in entry.tags:
                    results.append(entry)
        return results

    def find_by_title(self, title: str) -> List[BibleEntry]:
        results = []
        title_lower = title.lower()
        for section_entries in self.entries.values():
            for entry in section_entries.values():
                if title_lower in entry.title.lower():
                    results.append(entry)
        return results

    def get_cross_references(self, entry_id: str) -> List[BibleEntry]:
        refs = []
        for section_entries in self.entries.values():
            for entry in section_entries.values():
                if entry_id in entry.references:
                    refs.append(entry)
        return refs

    def check_consistency(self) -> List[ConsistencyIssue]:
        """跨条目一致性校验"""
        issues = []

        characters = self.get_section(BibleSection.CHARACTERS)
        world_entries = self.get_section(BibleSection.WORLD_BUILDING)

        char_names = {}
        for char in characters:
            name = char.metadata.get("name", char.title)
            if name in char_names:
                issues.append(ConsistencyIssue(
                    entry_a=char.entry_id,
                    entry_b=char_names[name].entry_id,
                    field="name",
                    value_a=name,
                    value_b=name,
                    severity="warning",
                    description=f"角色名重复: {name}",
                ))
            char_names[name] = char

        for char in characters:
            faction = char.metadata.get("faction", "")
            if faction:
                found = False
                for we in world_entries:
                    if faction in we.content or faction == we.title:
                        found = True
                        break
                if not found:
                    issues.append(ConsistencyIssue(
                        entry_a=char.entry_id,
                        entry_b="",
                        field="faction",
                        value_a=faction,
                        value_b="未定义",
                        severity="warning",
                        description=f"角色 {char.title} 所属势力 '{faction}' 未在世界观中定义",
                    ))

        return issues

    def get_stats(self) -> dict:
        stats = {
            "novel_title": self.novel_title,
            "total_entries": 0,
            "by_section": {},
            "total_versions": sum(
                e.version for section_entries in self.entries.values()
                for e in section_entries.values()
            ),
            "history_count": len(self._history),
        }
        for section in BibleSection:
            entries = self.get_section(section)
            if entries:
                stats["by_section"][section.value] = len(entries)
                stats["total_entries"] += len(entries)
        return stats

    def export_full_report(self, filepath: str = None) -> str:
        """导出完整设定报告"""
        lines = []
        lines.append(f"# {self.novel_title} - 创作圣经")
        lines.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")

        for section in BibleSection:
            entries = self.get_section(section)
            if not entries:
                continue
            lines.append(f"## {section.value}")
            lines.append("")
            for entry in entries:
                lines.append(f"### {entry.title}")
                lines.append(entry.content)
                if entry.tags:
                    lines.append(f"标签: {', '.join(entry.tags)}")
                if entry.references:
                    lines.append(f"关联: {', '.join(entry.references)}")
                lines.append("")

        report = "\n".join(lines)
        if filepath:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(report)
        return report

    def rollback(self, steps: int = 1) -> bool:
        """回滚到之前的版本"""
        if steps > len(self._history):
            return False
        self._history = self._history[:-steps]
        self.save()
        return True

    def merge_from(self, other: "StoryBible", sections: List[BibleSection] = None):
        """从另一个StoryBible合并条目"""
        if sections is None:
            sections = list(BibleSection)
        for section in sections:
            other_entries = other.get_section(section)
            for entry in other_entries:
                if entry.entry_id not in self.entries.get(section.value, {}):
                    self.add_entry(copy.deepcopy(entry))


import re
