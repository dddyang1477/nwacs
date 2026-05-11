#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS Story Bible - 集中式创作圣经 v2.0

对标 Sudowrite Story Bible，核心能力：
1. 统一管理 - 角色/世界观/大纲/伏笔/场景一站式
2. 交叉引用 - 条目间自动关联，点击跳转
3. 一致性校验 - 跨条目设定冲突检测
4. 版本快照 - 每次修改自动保存历史
5. 导出报告 - 生成完整设定文档
6. 关系图谱 - 角色关系网络可视化数据
7. 时间线管理 - 故事事件时间轴
8. 进度追踪 - 写作进度与里程碑
9. 场景映射 - 场景到章节的映射关系
10. 研究资料 - 结构化研究素材管理

设计原则：
- 单一数据源(Single Source of Truth)
- 所有模块通过StoryBible获取设定
- 与Lorebook/NovelMemoryManager无缝集成
"""

import json
import os
import re
import copy
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict


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
    TIMELINE = "时间线"
    RELATIONSHIPS = "关系图谱"


class RelationshipType(Enum):
    FAMILY = ("亲属", "血缘关系")
    FRIEND = ("朋友", "友谊关系")
    LOVER = ("恋人", "爱情关系")
    RIVAL = ("对手", "竞争关系")
    ENEMY = ("敌人", "敌对关系")
    MASTER_STUDENT = ("师徒", "师徒关系")
    SUPERIOR_SUBORDINATE = ("上下级", "从属关系")
    ALLIANCE = ("盟友", "同盟关系")
    BETRAYER = ("背叛", "背叛关系")
    MYSTERIOUS = ("神秘", "未知关系")

    def __init__(self, label: str, description: str):
        self.label = label
        self.description = description


class EventType(Enum):
    BACKSTORY = "背景事件"
    INCITING = "激励事件"
    TURNING_POINT = "转折点"
    CLIMAX = "高潮事件"
    RESOLUTION = "结局事件"
    SUBPLOT = "支线事件"
    CHARACTER = "角色事件"
    WORLDBUILDING = "世界观事件"


class MilestoneType(Enum):
    OUTLINE_COMPLETE = "大纲完成"
    FIRST_DRAFT = "初稿完成"
    REVISION = "修订完成"
    FINAL = "终稿完成"
    PUBLISH = "发布"


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
    status: str = "active"
    priority: int = 3

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
            "status": self.status,
            "priority": self.priority,
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
            status=data.get("status", "active"),
            priority=data.get("priority", 3),
        )


@dataclass
class Relationship:
    rel_id: str
    character_a: str
    character_b: str
    rel_type: RelationshipType
    strength: int
    description: str
    first_established_chapter: int = 0
    evolution: List[Dict] = field(default_factory=list)
    is_mutual: bool = True
    is_secret: bool = False

    def to_dict(self) -> dict:
        return {
            "rel_id": self.rel_id,
            "character_a": self.character_a,
            "character_b": self.character_b,
            "rel_type": self.rel_type.label,
            "strength": self.strength,
            "description": self.description,
            "first_established_chapter": self.first_established_chapter,
            "evolution": self.evolution,
            "is_mutual": self.is_mutual,
            "is_secret": self.is_secret,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Relationship":
        type_map = {t.label: t for t in RelationshipType}
        return cls(
            rel_id=data["rel_id"],
            character_a=data["character_a"],
            character_b=data["character_b"],
            rel_type=type_map.get(data["rel_type"], RelationshipType.MYSTERIOUS),
            strength=data.get("strength", 5),
            description=data.get("description", ""),
            first_established_chapter=data.get("first_established_chapter", 0),
            evolution=data.get("evolution", []),
            is_mutual=data.get("is_mutual", True),
            is_secret=data.get("is_secret", False),
        )


@dataclass
class TimelineEvent:
    event_id: str
    title: str
    event_type: EventType
    chapter: int
    description: str
    date_in_story: str = ""
    involved_characters: List[str] = field(default_factory=list)
    involved_locations: List[str] = field(default_factory=list)
    causes: List[str] = field(default_factory=list)
    consequences: List[str] = field(default_factory=list)
    importance: int = 5
    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "event_id": self.event_id,
            "title": self.title,
            "event_type": self.event_type.value,
            "chapter": self.chapter,
            "description": self.description,
            "date_in_story": self.date_in_story,
            "involved_characters": self.involved_characters,
            "involved_locations": self.involved_locations,
            "causes": self.causes,
            "consequences": self.consequences,
            "importance": self.importance,
            "tags": self.tags,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "TimelineEvent":
        type_map = {t.value: t for t in EventType}
        return cls(
            event_id=data["event_id"],
            title=data["title"],
            event_type=type_map.get(data["event_type"], EventType.SUBPLOT),
            chapter=data.get("chapter", 0),
            description=data.get("description", ""),
            date_in_story=data.get("date_in_story", ""),
            involved_characters=data.get("involved_characters", []),
            involved_locations=data.get("involved_locations", []),
            causes=data.get("causes", []),
            consequences=data.get("consequences", []),
            importance=data.get("importance", 5),
            tags=data.get("tags", []),
        )


@dataclass
class Milestone:
    milestone_id: str
    milestone_type: MilestoneType
    target_chapter: int
    description: str
    target_date: str = ""
    completed_date: str = ""
    is_completed: bool = False
    notes: str = ""

    def to_dict(self) -> dict:
        return {
            "milestone_id": self.milestone_id,
            "milestone_type": self.milestone_type.value,
            "target_chapter": self.target_chapter,
            "description": self.description,
            "target_date": self.target_date,
            "completed_date": self.completed_date,
            "is_completed": self.is_completed,
            "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Milestone":
        type_map = {t.value: t for t in MilestoneType}
        return cls(
            milestone_id=data["milestone_id"],
            milestone_type=type_map.get(data["milestone_type"], MilestoneType.FIRST_DRAFT),
            target_chapter=data.get("target_chapter", 0),
            description=data.get("description", ""),
            target_date=data.get("target_date", ""),
            completed_date=data.get("completed_date", ""),
            is_completed=data.get("is_completed", False),
            notes=data.get("notes", ""),
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
    """集中式创作圣经 v2.0"""

    def __init__(self, novel_title: str = "未命名作品", storage_dir: str = None):
        self.novel_title = novel_title
        if storage_dir is None:
            storage_dir = os.path.join(os.path.dirname(__file__), "..", "bible_storage")
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)

        self.entries: Dict[str, Dict[str, BibleEntry]] = {}
        self.relationships: Dict[str, Relationship] = {}
        self.timeline_events: Dict[str, TimelineEvent] = {}
        self.milestones: Dict[str, Milestone] = {}
        self._history: List[Dict] = []
        self._tag_index: Dict[str, Set[Tuple[str, str]]] = defaultdict(set)
        self._character_index: Dict[str, Set[str]] = defaultdict(set)

        self._load()

    def _get_filepath(self) -> str:
        safe_name = re.sub(r'[<>:"/\\|?*]', '_', self.novel_title)
        return os.path.join(self.storage_dir, f"{safe_name}_bible.json")

    def _get_history_path(self) -> str:
        safe_name = re.sub(r'[<>:"/\\|?*]', '_', self.novel_title)
        return os.path.join(self.storage_dir, f"{safe_name}_history.json")

    def _get_relationships_path(self) -> str:
        safe_name = re.sub(r'[<>:"/\\|?*]', '_', self.novel_title)
        return os.path.join(self.storage_dir, f"{safe_name}_relationships.json")

    def _get_timeline_path(self) -> str:
        safe_name = re.sub(r'[<>:"/\\|?*]', '_', self.novel_title)
        return os.path.join(self.storage_dir, f"{safe_name}_timeline.json")

    def _get_milestones_path(self) -> str:
        safe_name = re.sub(r'[<>:"/\\|?*]', '_', self.novel_title)
        return os.path.join(self.storage_dir, f"{safe_name}_milestones.json")

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
                    self._index_entry(entry)

        history_path = self._get_history_path()
        if os.path.exists(history_path):
            with open(history_path, "r", encoding="utf-8") as f:
                self._history = json.load(f)

        rel_path = self._get_relationships_path()
        if os.path.exists(rel_path):
            with open(rel_path, "r", encoding="utf-8") as f:
                rel_data = json.load(f)
            for r in rel_data.get("relationships", []):
                rel = Relationship.from_dict(r)
                self.relationships[rel.rel_id] = rel

        tl_path = self._get_timeline_path()
        if os.path.exists(tl_path):
            with open(tl_path, "r", encoding="utf-8") as f:
                tl_data = json.load(f)
            for e in tl_data.get("events", []):
                event = TimelineEvent.from_dict(e)
                self.timeline_events[event.event_id] = event

        ms_path = self._get_milestones_path()
        if os.path.exists(ms_path):
            with open(ms_path, "r", encoding="utf-8") as f:
                ms_data = json.load(f)
            for m in ms_data.get("milestones", []):
                milestone = Milestone.from_dict(m)
                self.milestones[milestone.milestone_id] = milestone

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

        with open(self._get_relationships_path(), "w", encoding="utf-8") as f:
            json.dump({
                "updated_at": datetime.now().isoformat(),
                "relationships": [r.to_dict() for r in self.relationships.values()],
            }, f, ensure_ascii=False, indent=2)

        with open(self._get_timeline_path(), "w", encoding="utf-8") as f:
            json.dump({
                "updated_at": datetime.now().isoformat(),
                "events": [e.to_dict() for e in self.timeline_events.values()],
            }, f, ensure_ascii=False, indent=2)

        with open(self._get_milestones_path(), "w", encoding="utf-8") as f:
            json.dump({
                "updated_at": datetime.now().isoformat(),
                "milestones": [m.to_dict() for m in self.milestones.values()],
            }, f, ensure_ascii=False, indent=2)

    def _index_entry(self, entry: BibleEntry):
        for tag in entry.tags:
            self._tag_index[tag.lower()].add((entry.section.value, entry.entry_id))

        if entry.section == BibleSection.CHARACTERS:
            name = entry.metadata.get("name", entry.title)
            self._character_index[name.lower()].add(entry.entry_id)

    def _unindex_entry(self, entry: BibleEntry):
        for tag in entry.tags:
            key = (entry.section.value, entry.entry_id)
            if tag.lower() in self._tag_index:
                self._tag_index[tag.lower()].discard(key)

        if entry.section == BibleSection.CHARACTERS:
            name = entry.metadata.get("name", entry.title)
            if name.lower() in self._character_index:
                self._character_index[name.lower()].discard(entry.entry_id)

    def _snapshot(self, action: str, entry_id: str, section: str):
        self._history.append({
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "entry_id": entry_id,
            "section": section,
        })

    def _extract_key_terms(self, text: str) -> Set[str]:
        chinese_words = set(re.findall(r'[\u4e00-\u9fff]{2,}', text.lower()))
        english_words = set(re.findall(r'[a-zA-Z]{3,}', text.lower()))
        return chinese_words | english_words

    def _jaccard_similarity(self, set_a: Set[str], set_b: Set[str]) -> float:
        if not set_a or not set_b:
            return 0.0
        intersection = len(set_a & set_b)
        union = len(set_a | set_b)
        return intersection / union if union > 0 else 0.0

    def add_entry(self, entry: BibleEntry) -> str:
        if not entry.entry_id:
            entry.entry_id = str(uuid.uuid4())[:8]
        now = datetime.now().isoformat()
        entry.created_at = now
        entry.updated_at = now

        section_name = entry.section.value
        if section_name not in self.entries:
            self.entries[section_name] = {}
        self.entries[section_name][entry.entry_id] = entry
        self._index_entry(entry)
        self._snapshot("add", entry.entry_id, section_name)
        self.save()
        return entry.entry_id

    def update_entry(self, entry_id: str, section: BibleSection, **kwargs) -> bool:
        section_name = section.value
        if section_name not in self.entries or entry_id not in self.entries[section_name]:
            return False

        entry = self.entries[section_name][entry_id]
        self._unindex_entry(entry)

        for key, value in kwargs.items():
            if hasattr(entry, key):
                setattr(entry, key, value)

        entry.updated_at = datetime.now().isoformat()
        entry.version += 1
        self._index_entry(entry)
        self._snapshot("update", entry_id, section_name)
        self.save()
        return True

    def remove_entry(self, entry_id: str, section: BibleSection) -> bool:
        section_name = section.value
        if section_name not in self.entries or entry_id not in self.entries[section_name]:
            return False
        self._unindex_entry(self.entries[section_name][entry_id])
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
        for section_name, entry_id in self._tag_index.get(tag.lower(), set()):
            entry = self.entries.get(section_name, {}).get(entry_id)
            if entry:
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

    def search(self, query: str, sections: List[BibleSection] = None,
               max_results: int = 20) -> List[Tuple[BibleEntry, float]]:
        """全文搜索所有条目"""
        results = []
        query_lower = query.lower()
        query_terms = self._extract_key_terms(query)

        target_sections = sections or list(BibleSection)
        for section in target_sections:
            for entry in self.get_section(section):
                score = 0.0

                if query_lower in entry.title.lower():
                    score = max(score, 0.9)
                if query_lower in entry.content.lower():
                    score = max(score, 0.7)

                entry_terms = self._extract_key_terms(entry.content)
                entry_terms.update(self._extract_key_terms(entry.title))
                term_score = self._jaccard_similarity(query_terms, entry_terms) * 0.5
                score = max(score, term_score)

                if score > 0.1:
                    results.append((entry, score))

        results.sort(key=lambda x: x[1], reverse=True)
        return results[:max_results]

    def get_cross_references(self, entry_id: str) -> List[BibleEntry]:
        refs = []
        for section_entries in self.entries.values():
            for entry in section_entries.values():
                if entry_id in entry.references:
                    refs.append(entry)
        return refs

    def auto_link_references(self):
        """自动发现并建立交叉引用"""
        all_entries = []
        for section_entries in self.entries.values():
            all_entries.extend(section_entries.values())

        for entry in all_entries:
            entry_terms = self._extract_key_terms(entry.content)
            for other in all_entries:
                if other.entry_id == entry.entry_id:
                    continue
                other_terms = self._extract_key_terms(other.title)
                if other_terms & entry_terms:
                    if other.entry_id not in entry.references:
                        entry.references.append(other.entry_id)

        self.save()

    def check_consistency(self) -> List[ConsistencyIssue]:
        """跨条目一致性校验"""
        issues = []

        characters = self.get_section(BibleSection.CHARACTERS)
        world_entries = self.get_section(BibleSection.WORLD_BUILDING)
        plot_entries = self.get_section(BibleSection.PLOT_OUTLINE)

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

        for char in characters:
            abilities = char.metadata.get("abilities", [])
            if isinstance(abilities, list):
                for ability in abilities:
                    if isinstance(ability, dict):
                        ability_name = ability.get("name", "")
                        found_in_world = False
                        for we in world_entries:
                            if ability_name in we.content:
                                found_in_world = True
                                break
                        if not found_in_world and ability_name:
                            issues.append(ConsistencyIssue(
                                entry_a=char.entry_id,
                                entry_b="",
                                field="ability",
                                value_a=ability_name,
                                value_b="未定义",
                                severity="info",
                                description=f"角色 {char.title} 的能力 '{ability_name}' 未在世界观中说明",
                            ))

        all_locations = set()
        for we in world_entries:
            loc_matches = re.findall(r'([\u4e00-\u9fff]{2,}(?:城|国|域|界|山|海|谷|林|殿|阁|宗|派|门))', we.content)
            all_locations.update(loc_matches)

        for pe in plot_entries:
            for loc in all_locations:
                if loc in pe.content:
                    break

        return issues

    def add_relationship(self, rel: Relationship) -> str:
        if not rel.rel_id:
            rel.rel_id = str(uuid.uuid4())[:8]
        self.relationships[rel.rel_id] = rel
        self.save()
        return rel.rel_id

    def remove_relationship(self, rel_id: str) -> bool:
        if rel_id in self.relationships:
            del self.relationships[rel_id]
            self.save()
            return True
        return False

    def get_character_relationships(self, character_name: str) -> List[Relationship]:
        """获取某角色的所有关系"""
        results = []
        name_lower = character_name.lower()
        for rel in self.relationships.values():
            if (rel.character_a.lower() == name_lower or
                    rel.character_b.lower() == name_lower):
                results.append(rel)
        return results

    def get_relationship_graph(self) -> Dict:
        """获取关系图谱数据（用于可视化）"""
        nodes = []
        edges = []
        char_set = set()

        characters = self.get_section(BibleSection.CHARACTERS)
        for char in characters:
            name = char.metadata.get("name", char.title)
            if name not in char_set:
                char_set.add(name)
                nodes.append({
                    "id": name,
                    "label": name,
                    "type": "character",
                    "role": char.metadata.get("role", "配角"),
                    "status": char.metadata.get("status", "存活"),
                })

        for rel in self.relationships.values():
            if rel.character_a not in char_set:
                char_set.add(rel.character_a)
                nodes.append({
                    "id": rel.character_a,
                    "label": rel.character_a,
                    "type": "character",
                    "role": "未知",
                })
            if rel.character_b not in char_set:
                char_set.add(rel.character_b)
                nodes.append({
                    "id": rel.character_b,
                    "label": rel.character_b,
                    "type": "character",
                    "role": "未知",
                })

            edges.append({
                "source": rel.character_a,
                "target": rel.character_b,
                "type": rel.rel_type.label,
                "strength": rel.strength,
                "description": rel.description,
                "is_secret": rel.is_secret,
            })

        return {"nodes": nodes, "edges": edges}

    def add_timeline_event(self, event: TimelineEvent) -> str:
        if not event.event_id:
            event.event_id = str(uuid.uuid4())[:8]
        self.timeline_events[event.event_id] = event
        self.save()
        return event.event_id

    def remove_timeline_event(self, event_id: str) -> bool:
        if event_id in self.timeline_events:
            del self.timeline_events[event_id]
            self.save()
            return True
        return False

    def get_timeline(self, sort_by: str = "chapter") -> List[TimelineEvent]:
        """获取排序后的时间线"""
        events = list(self.timeline_events.values())
        if sort_by == "chapter":
            events.sort(key=lambda e: e.chapter)
        elif sort_by == "importance":
            events.sort(key=lambda e: e.importance, reverse=True)
        elif sort_by == "date":
            events.sort(key=lambda e: e.date_in_story)
        return events

    def get_chapter_events(self, chapter: int) -> List[TimelineEvent]:
        """获取某章节的所有事件"""
        return [e for e in self.timeline_events.values() if e.chapter == chapter]

    def get_causal_chain(self, event_id: str) -> List[TimelineEvent]:
        """获取事件的因果链"""
        chain = []
        visited = set()
        queue = [event_id]

        while queue:
            current_id = queue.pop(0)
            if current_id in visited:
                continue
            visited.add(current_id)
            event = self.timeline_events.get(current_id)
            if event:
                chain.append(event)
                for cause_id in event.causes:
                    if cause_id not in visited:
                        queue.append(cause_id)
                for cons_id in event.consequences:
                    if cons_id not in visited:
                        queue.append(cons_id)

        chain.sort(key=lambda e: e.chapter)
        return chain

    def add_milestone(self, milestone: Milestone) -> str:
        if not milestone.milestone_id:
            milestone.milestone_id = str(uuid.uuid4())[:8]
        self.milestones[milestone.milestone_id] = milestone
        self.save()
        return milestone.milestone_id

    def complete_milestone(self, milestone_id: str) -> bool:
        if milestone_id in self.milestones:
            ms = self.milestones[milestone_id]
            ms.is_completed = True
            ms.completed_date = datetime.now().isoformat()
            self.save()
            return True
        return False

    def get_progress(self) -> Dict:
        """获取写作进度概览"""
        milestones_list = list(self.milestones.values())
        completed = sum(1 for m in milestones_list if m.is_completed)
        total = len(milestones_list)

        plot_entries = self.get_section(BibleSection.PLOT_OUTLINE)
        total_chapters_planned = len(plot_entries)

        scene_entries = self.get_section(BibleSection.SCENES)
        total_scenes = len(scene_entries)

        char_entries = self.get_section(BibleSection.CHARACTERS)
        total_characters = len(char_entries)

        fs_entries = self.get_section(BibleSection.FORESHADOWING)
        total_foreshadowing = len(fs_entries)

        return {
            "milestones_completed": completed,
            "milestones_total": total,
            "milestone_progress": round(completed / max(total, 1) * 100, 1),
            "chapters_planned": total_chapters_planned,
            "total_scenes": total_scenes,
            "total_characters": total_characters,
            "total_foreshadowing": total_foreshadowing,
            "last_updated": datetime.now().isoformat(),
        }

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
            "relationship_count": len(self.relationships),
            "timeline_event_count": len(self.timeline_events),
            "milestone_count": len(self.milestones),
        }
        for section in BibleSection:
            entries = self.get_section(section)
            if entries:
                stats["by_section"][section.value] = len(entries)
                stats["total_entries"] += len(entries)
        return stats

    def get_dashboard(self) -> Dict:
        """获取完整仪表盘"""
        stats = self.get_stats()
        progress = self.get_progress()
        consistency_issues = self.check_consistency()

        return {
            "stats": stats,
            "progress": progress,
            "consistency_issue_count": len(consistency_issues),
            "consistency_issues": [
                {"severity": i.severity, "description": i.description}
                for i in consistency_issues[:10]
            ],
            "top_characters_by_relationships": sorted(
                [(name, len(self.get_character_relationships(name)))
                 for name in self._character_index],
                key=lambda x: x[1], reverse=True
            )[:10],
        }

    def export_full_report(self, filepath: str = None, format: str = "markdown") -> str:
        """导出完整设定报告"""
        if format == "html":
            return self._export_html(filepath)
        return self._export_markdown(filepath)

    def _export_markdown(self, filepath: str = None) -> str:
        lines = []
        lines.append(f"# {self.novel_title} - 创作圣经")
        lines.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")

        for section in BibleSection:
            if section in (BibleSection.TIMELINE, BibleSection.RELATIONSHIPS):
                continue
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

        if self.timeline_events:
            lines.append("## 时间线")
            lines.append("")
            for event in self.get_timeline():
                lines.append(f"- **第{event.chapter}章**: {event.title} ({event.event_type.value})")
                lines.append(f"  {event.description}")
            lines.append("")

        if self.relationships:
            lines.append("## 角色关系")
            lines.append("")
            for rel in self.relationships.values():
                lines.append(f"- {rel.character_a} → {rel.character_b}: {rel.rel_type.label} (强度:{rel.strength})")
            lines.append("")

        report = "\n".join(lines)
        if filepath:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(report)
        return report

    def _export_html(self, filepath: str = None) -> str:
        md_content = self._export_markdown()
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>{self.novel_title} - 创作圣经</title>
    <style>
        body {{ font-family: 'Microsoft YaHei', sans-serif; max-width: 900px; margin: 0 auto; padding: 20px; line-height: 1.8; }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #2980b9; margin-top: 30px; border-bottom: 1px solid #bdc3c7; }}
        h3 {{ color: #34495e; }}
        .content {{ white-space: pre-wrap; background: #f8f9fa; padding: 15px; border-radius: 5px; }}
    </style>
</head>
<body>
{md_content.replace(chr(10), '<br>')}
</body>
</html>"""
        if filepath:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(html)
        return html

    def export_section(self, section: BibleSection, filepath: str,
                       format: str = "json") -> int:
        entries = self.get_section(section)
        if format == "json":
            data = {
                "section": section.value,
                "exported_at": datetime.now().isoformat(),
                "entries": [e.to_dict() for e in entries],
            }
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        elif format == "markdown":
            lines = [f"# {section.value}", ""]
            for entry in entries:
                lines.append(f"## {entry.title}")
                lines.append(entry.content)
                lines.append("")
            with open(filepath, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))
        return len(entries)

    def import_section(self, section: BibleSection, filepath: str) -> int:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        count = 0
        for entry_data in data.get("entries", []):
            entry = BibleEntry.from_dict(entry_data)
            entry.section = section
            if entry.entry_id in self.entries.get(section.value, {}):
                entry.entry_id = str(uuid.uuid4())[:8]
            self.add_entry(entry)
            count += 1
        return count

    def rollback(self, steps: int = 1) -> bool:
        if steps > len(self._history):
            return False
        self._history = self._history[:-steps]
        self.save()
        return True

    def merge_from(self, other: "StoryBible", sections: List[BibleSection] = None):
        if sections is None:
            sections = list(BibleSection)
        for section in sections:
            other_entries = other.get_section(section)
            for entry in other_entries:
                if entry.entry_id not in self.entries.get(section.value, {}):
                    self.add_entry(copy.deepcopy(entry))

        for rel in other.relationships.values():
            if rel.rel_id not in self.relationships:
                self.relationships[rel.rel_id] = copy.deepcopy(rel)

        for event in other.timeline_events.values():
            if event.event_id not in self.timeline_events:
                self.timeline_events[event.event_id] = copy.deepcopy(event)

        self.save()

    def create_snapshot(self, name: str) -> str:
        """创建完整快照"""
        snapshot_id = str(uuid.uuid4())[:8]
        snapshot_dir = os.path.join(self.storage_dir, "snapshots")
        os.makedirs(snapshot_dir, exist_ok=True)

        snapshot_data = {
            "snapshot_id": snapshot_id,
            "name": name,
            "created_at": datetime.now().isoformat(),
            "entries": {
                sn: [e.to_dict() for e in entries.values()]
                for sn, entries in self.entries.items()
            },
            "relationships": [r.to_dict() for r in self.relationships.values()],
            "timeline_events": [e.to_dict() for e in self.timeline_events.values()],
            "milestones": [m.to_dict() for m in self.milestones.values()],
        }

        filepath = os.path.join(snapshot_dir, f"{snapshot_id}.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(snapshot_data, f, ensure_ascii=False, indent=2)

        return snapshot_id

    def list_snapshots(self) -> List[Dict]:
        snapshot_dir = os.path.join(self.storage_dir, "snapshots")
        if not os.path.exists(snapshot_dir):
            return []

        snapshots = []
        for filename in os.listdir(snapshot_dir):
            if filename.endswith(".json"):
                filepath = os.path.join(snapshot_dir, filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                snapshots.append({
                    "snapshot_id": data["snapshot_id"],
                    "name": data["name"],
                    "created_at": data["created_at"],
                })

        snapshots.sort(key=lambda s: s["created_at"], reverse=True)
        return snapshots
