#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project Memory — NWACS 项目记忆与模式学习模块 v3.0

核心功能:
1. 模式学习 — 从审查反馈中提取可复用的写作模式
2. 长期记忆 — 跨章节的知识积累与检索
3. 反模式库 — 自动收集应避免的写作模式
4. 实体注册表 — 角色/地点/物品/组织实体管理与关系图谱
5. 语义搜索 — TF-IDF 关键词检索 + 模糊匹配
6. 可插拔存储后端 — JSON文件后端 + 抽象接口
7. 记忆快照 — 保存/恢复记忆状态
8. 实体检测 — 从章节文本自动提取实体
"""

from __future__ import annotations

import json
import math
import re
import uuid
from abc import ABC, abstractmethod
from collections import Counter
from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _uid() -> str:
    return str(uuid.uuid4())[:12]


@dataclass
class MemoryPattern:
    pattern_type: str
    description: str
    category: str = ""
    importance: str = "medium"
    source_chapter: Optional[int] = None
    learned_at: str = field(default_factory=_utc_now_iso)
    updated_at: str = field(default_factory=_utc_now_iso)
    usage_count: int = 0
    effectiveness: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "pattern_type": self.pattern_type,
            "description": self.description,
            "category": self.category,
            "importance": self.importance,
            "source_chapter": self.source_chapter,
            "learned_at": self.learned_at,
            "updated_at": self.updated_at,
            "usage_count": self.usage_count,
            "effectiveness": self.effectiveness,
        }


@dataclass
class EntityRecord:
    """实体记录 — 实体注册表管理"""
    entity_id: str
    name: str
    entity_type: str
    aliases: List[str] = field(default_factory=list)
    attributes: Dict[str, Any] = field(default_factory=dict)
    first_appearance: int = 0
    last_appearance: int = 0
    appearance_count: int = 0
    relationships: List[Dict[str, Any]] = field(default_factory=list)
    notes: str = ""
    created_at: str = field(default_factory=_utc_now_iso)
    updated_at: str = field(default_factory=_utc_now_iso)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "entity_type": self.entity_type,
            "aliases": self.aliases,
            "attributes": self.attributes,
            "first_appearance": self.first_appearance,
            "last_appearance": self.last_appearance,
            "appearance_count": self.appearance_count,
            "relationships": self.relationships,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class StorageBackend(ABC):
    """可插拔存储后端抽象接口"""

    @abstractmethod
    def load(self, key: str) -> Optional[Dict[str, Any]]:
        ...

    @abstractmethod
    def save(self, key: str, data: Dict[str, Any]) -> None:
        ...

    @abstractmethod
    def delete(self, key: str) -> bool:
        ...

    @abstractmethod
    def list_keys(self, prefix: str = "") -> List[str]:
        ...

    @abstractmethod
    def health_check(self) -> Dict[str, Any]:
        ...


class JSONFileBackend(StorageBackend):
    """JSON文件存储后端"""

    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def _key_to_path(self, key: str) -> Path:
        safe_key = re.sub(r'[<>:"/\\|?*]', '_', key)
        return self.base_dir / f"{safe_key}.json"

    def load(self, key: str) -> Optional[Dict[str, Any]]:
        path = self._key_to_path(key)
        if not path.exists():
            return None
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return None

    def save(self, key: str, data: Dict[str, Any]) -> None:
        path = self._key_to_path(key)
        tmp = path.with_suffix(path.suffix + ".tmp")
        tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        tmp.replace(path)

    def delete(self, key: str) -> bool:
        path = self._key_to_path(key)
        if path.exists():
            path.unlink()
            return True
        return False

    def list_keys(self, prefix: str = "") -> List[str]:
        keys = []
        for p in self.base_dir.glob("*.json"):
            name = p.stem
            if not prefix or name.startswith(prefix):
                keys.append(name)
        return keys

    def health_check(self) -> Dict[str, Any]:
        return {
            "backend": "JSONFileBackend",
            "base_dir": str(self.base_dir),
            "exists": self.base_dir.exists(),
            "file_count": len(list(self.base_dir.glob("*.json"))),
        }


class ProjectMemory:
    """项目记忆系统 — 模式学习与长期记忆闭环 v3.0"""

    PATTERN_TYPES = [
        "writing_technique",
        "anti_pattern",
        "reader_feedback",
        "pacing_rule",
        "character_voice",
        "dialogue_style",
        "description_style",
        "hook_pattern",
        "cool_point_pattern",
        "transition_pattern",
        "emotion_expression",
        "world_building_rule",
        "genre_convention",
        "other",
    ]

    CATEGORIES = [
        "style",
        "structure",
        "character",
        "plot",
        "dialogue",
        "description",
        "pacing",
        "ai_avoidance",
        "reader_engagement",
        "world_building",
    ]

    ENTITY_TYPES = ["character", "location", "item", "organization", "concept", "event"]

    RELATIONSHIP_TYPES = [
        "ally", "enemy", "family", "master_student", "lover",
        "rival", "subordinate", "superior", "friend", "neutral",
        "located_in", "owns", "belongs_to", "created_by", "member_of",
    ]

    def __init__(self, project_root: str = ""):
        self.project_root = Path(project_root) if project_root else Path(".")
        self.memory_dir = self.project_root / ".webnovel"
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        self._memory_path = self.memory_dir / "project_memory.json"
        self._patterns_cache: Optional[List[MemoryPattern]] = None

        self._entity_dir = self.memory_dir / "entities"
        self._entity_dir.mkdir(parents=True, exist_ok=True)
        self._entity_backend = JSONFileBackend(self._entity_dir)
        self._entity_cache: Optional[Dict[str, EntityRecord]] = None

        self._snapshot_dir = self.memory_dir / "snapshots"
        self._snapshot_dir.mkdir(parents=True, exist_ok=True)
        self._snapshot_backend = JSONFileBackend(self._snapshot_dir)

        self._stopwords: Set[str] = set()

    def _load_patterns(self) -> List[MemoryPattern]:
        if not self._memory_path.exists():
            return []
        try:
            data = json.loads(self._memory_path.read_text(encoding="utf-8"))
            patterns_data = data.get("patterns", [])
            if not isinstance(patterns_data, list):
                return []
            return [
                MemoryPattern(
                    pattern_type=p.get("pattern_type", "other"),
                    description=p.get("description", ""),
                    category=p.get("category", ""),
                    importance=p.get("importance", "medium"),
                    source_chapter=p.get("source_chapter"),
                    learned_at=p.get("learned_at", ""),
                    updated_at=p.get("updated_at", ""),
                    usage_count=p.get("usage_count", 0),
                    effectiveness=p.get("effectiveness", 0.0),
                )
                for p in patterns_data
            ]
        except (json.JSONDecodeError, KeyError):
            return []

    def _save_patterns(self, patterns: List[MemoryPattern]) -> None:
        data = {
            "meta": {
                "version": "1.0.0",
                "updated_at": _utc_now_iso(),
                "total_patterns": len(patterns),
            },
            "patterns": [p.to_dict() for p in patterns],
        }
        tmp_path = self._memory_path.with_suffix(self._memory_path.suffix + ".tmp")
        tmp_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        tmp_path.replace(self._memory_path)
        self._patterns_cache = None

    def _get_patterns(self) -> List[MemoryPattern]:
        if self._patterns_cache is None:
            self._patterns_cache = self._load_patterns()
        return self._patterns_cache

    def add_pattern(
        self,
        pattern_type: str,
        description: str,
        category: str = "",
        importance: str = "medium",
        source_chapter: Optional[int] = None,
    ) -> Dict[str, Any]:
        pattern_type = (pattern_type or "other").strip() or "other"
        description = (description or "").strip()

        if not description:
            return {"status": "error", "error": "description 不能为空"}

        patterns = self._get_patterns()

        for p in patterns:
            if p.pattern_type == pattern_type and p.description == description:
                p.usage_count += 1
                p.updated_at = _utc_now_iso()
                self._save_patterns(patterns)
                return {"status": "skipped", "reason": "duplicate", "pattern": p.to_dict()}

        pattern = MemoryPattern(
            pattern_type=pattern_type,
            description=description,
            category=category,
            importance=importance,
            source_chapter=source_chapter,
        )
        patterns.append(pattern)
        self._save_patterns(patterns)

        return {"status": "success", "pattern": pattern.to_dict()}

    def learn_from_review(
        self,
        review_result: Dict[str, Any],
        chapter: int,
    ) -> List[Dict[str, Any]]:
        results = []
        issues = review_result.get("issues", [])

        for issue in issues:
            category = issue.get("category", "")
            severity = issue.get("severity", "low")
            description = issue.get("description", "")
            fix_hint = issue.get("fix_hint", "")

            if severity in ("critical", "high") and fix_hint:
                result = self.add_pattern(
                    pattern_type="anti_pattern",
                    description=f"[{category}] {description}",
                    category="ai_avoidance" if category == "ai_flavor" else category,
                    importance="high" if severity == "critical" else "medium",
                    source_chapter=chapter,
                )
                results.append(result)

            if fix_hint and severity == "medium":
                result = self.add_pattern(
                    pattern_type="writing_technique",
                    description=fix_hint,
                    category=category,
                    importance="medium",
                    source_chapter=chapter,
                )
                results.append(result)

        return results

    def learn_writing_pattern(
        self,
        description: str,
        pattern_type: str = "writing_technique",
        category: str = "style",
        chapter: Optional[int] = None,
    ) -> Dict[str, Any]:
        return self.add_pattern(
            pattern_type=pattern_type,
            description=description,
            category=category,
            importance="medium",
            source_chapter=chapter,
        )

    def get_patterns_by_type(
        self,
        pattern_type: str,
        limit: int = 20,
    ) -> List[Dict[str, Any]]:
        patterns = self._get_patterns()
        filtered = [p for p in patterns if p.pattern_type == pattern_type]
        filtered.sort(key=lambda p: p.learned_at, reverse=True)
        return [p.to_dict() for p in filtered[:limit]]

    def get_patterns_by_category(
        self,
        category: str,
        limit: int = 20,
    ) -> List[Dict[str, Any]]:
        patterns = self._get_patterns()
        filtered = [p for p in patterns if p.category == category]
        filtered.sort(key=lambda p: p.importance == "high", reverse=True)
        return [p.to_dict() for p in filtered[:limit]]

    def get_anti_patterns(self, limit: int = 20) -> List[Dict[str, Any]]:
        return self.get_patterns_by_type("anti_pattern", limit)

    def get_writing_techniques(self, limit: int = 20) -> List[Dict[str, Any]]:
        return self.get_patterns_by_type("writing_technique", limit)

    def get_high_importance_patterns(self, limit: int = 10) -> List[Dict[str, Any]]:
        patterns = self._get_patterns()
        filtered = [p for p in patterns if p.importance == "high"]
        filtered.sort(key=lambda p: p.usage_count, reverse=True)
        return [p.to_dict() for p in filtered[:limit]]

    def search_patterns(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        patterns = self._get_patterns()
        query_lower = query.lower()
        results = [
            p for p in patterns
            if query_lower in p.description.lower()
            or query_lower in p.category.lower()
            or query_lower in p.pattern_type.lower()
        ]
        results.sort(key=lambda p: p.importance == "high", reverse=True)
        return [p.to_dict() for p in results[:limit]]

    def build_context_injection(self, chapter: int) -> str:
        patterns = self._get_patterns()
        if not patterns:
            return ""

        anti_patterns = [p for p in patterns if p.pattern_type == "anti_pattern"]
        techniques = [p for p in patterns if p.pattern_type == "writing_technique"]

        parts: List[str] = []

        if anti_patterns:
            recent_anti = sorted(anti_patterns, key=lambda p: p.learned_at, reverse=True)[:5]
            parts.append("## 项目反模式（应避免）")
            for p in recent_anti:
                parts.append(f"- {p.description}")
            parts.append("")

        if techniques:
            recent_tech = sorted(techniques, key=lambda p: p.usage_count, reverse=True)[:5]
            parts.append("## 项目写作技法（已验证有效）")
            for p in recent_tech:
                parts.append(f"- {p.description}")
            parts.append("")

        return "\n".join(parts)

    def get_memory_stats(self) -> Dict[str, Any]:
        patterns = self._get_patterns()
        type_counts: Dict[str, int] = {}
        category_counts: Dict[str, int] = {}
        importance_counts: Dict[str, int] = {}

        for p in patterns:
            type_counts[p.pattern_type] = type_counts.get(p.pattern_type, 0) + 1
            category_counts[p.category] = category_counts.get(p.category, 0) + 1
            importance_counts[p.importance] = importance_counts.get(p.importance, 0) + 1

        return {
            "total_patterns": len(patterns),
            "by_type": type_counts,
            "by_category": category_counts,
            "by_importance": importance_counts,
            "last_updated": self._memory_path.stat().st_mtime if self._memory_path.exists() else 0,
        }

    def export_memory(self) -> Dict[str, Any]:
        patterns = self._get_patterns()
        return {
            "meta": {
                "version": "1.0.0",
                "exported_at": _utc_now_iso(),
                "total_patterns": len(patterns),
            },
            "patterns": [p.to_dict() for p in patterns],
            "stats": self.get_memory_stats(),
        }

    def clear_memory(self) -> None:
        self._save_patterns([])

    # ============================================================
    # 实体注册表 — Entity Registry
    # ============================================================

    def _load_entities(self) -> Dict[str, EntityRecord]:
        entities: Dict[str, EntityRecord] = {}
        for key in self._entity_backend.list_keys():
            data = self._entity_backend.load(key)
            if data:
                entities[key] = EntityRecord(
                    entity_id=data.get("entity_id", key),
                    name=data.get("name", ""),
                    entity_type=data.get("entity_type", "character"),
                    aliases=data.get("aliases", []),
                    attributes=data.get("attributes", {}),
                    first_appearance=data.get("first_appearance", 0),
                    last_appearance=data.get("last_appearance", 0),
                    appearance_count=data.get("appearance_count", 0),
                    relationships=data.get("relationships", []),
                    notes=data.get("notes", ""),
                    created_at=data.get("created_at", ""),
                    updated_at=data.get("updated_at", ""),
                )
        return entities

    def _get_entities(self) -> Dict[str, EntityRecord]:
        if self._entity_cache is None:
            self._entity_cache = self._load_entities()
        return self._entity_cache

    def _save_entity(self, entity: EntityRecord) -> None:
        entity.updated_at = _utc_now_iso()
        self._entity_backend.save(entity.entity_id, entity.to_dict())
        if self._entity_cache is not None:
            self._entity_cache[entity.entity_id] = entity

    def register_entity(
        self,
        name: str,
        entity_type: str = "character",
        aliases: Optional[List[str]] = None,
        attributes: Optional[Dict[str, Any]] = None,
        chapter: int = 0,
        notes: str = "",
    ) -> Dict[str, Any]:
        entity_type = entity_type if entity_type in self.ENTITY_TYPES else "character"
        entity_id = _uid()

        existing = self.find_entity_by_name(name)
        if existing:
            entity = existing
            if chapter > 0:
                entity.last_appearance = max(entity.last_appearance, chapter)
                entity.appearance_count += 1
            if aliases:
                for a in aliases:
                    if a not in entity.aliases:
                        entity.aliases.append(a)
            if attributes:
                entity.attributes.update(attributes)
            if notes:
                entity.notes = notes
            self._save_entity(entity)
            return {"status": "updated", "entity": entity.to_dict()}

        entity = EntityRecord(
            entity_id=entity_id,
            name=name,
            entity_type=entity_type,
            aliases=aliases or [],
            attributes=attributes or {},
            first_appearance=chapter,
            last_appearance=chapter,
            appearance_count=1 if chapter > 0 else 0,
            notes=notes,
        )
        self._save_entity(entity)
        return {"status": "created", "entity": entity.to_dict()}

    def find_entity_by_name(self, name: str) -> Optional[EntityRecord]:
        entities = self._get_entities()
        name_lower = name.strip().lower()
        for entity in entities.values():
            if entity.name.lower() == name_lower:
                return entity
            for alias in entity.aliases:
                if alias.lower() == name_lower:
                    return entity
        return None

    def get_entity(self, entity_id: str) -> Optional[Dict[str, Any]]:
        entities = self._get_entities()
        entity = entities.get(entity_id)
        return entity.to_dict() if entity else None

    def get_entities_by_type(self, entity_type: str) -> List[Dict[str, Any]]:
        entities = self._get_entities()
        return [
            e.to_dict() for e in entities.values()
            if e.entity_type == entity_type
        ]

    def get_all_entities(self) -> List[Dict[str, Any]]:
        return [e.to_dict() for e in self._get_entities().values()]

    def update_entity(
        self,
        entity_id: str,
        updates: Dict[str, Any],
    ) -> Optional[Dict[str, Any]]:
        entities = self._get_entities()
        entity = entities.get(entity_id)
        if not entity:
            return None

        if "name" in updates:
            entity.name = updates["name"]
        if "entity_type" in updates and updates["entity_type"] in self.ENTITY_TYPES:
            entity.entity_type = updates["entity_type"]
        if "aliases" in updates:
            entity.aliases = updates["aliases"]
        if "attributes" in updates:
            entity.attributes.update(updates["attributes"])
        if "notes" in updates:
            entity.notes = updates["notes"]
        if "chapter" in updates:
            ch = updates["chapter"]
            entity.last_appearance = max(entity.last_appearance, ch)
            entity.appearance_count += 1

        self._save_entity(entity)
        return entity.to_dict()

    def delete_entity(self, entity_id: str) -> bool:
        entities = self._get_entities()
        if entity_id not in entities:
            return False
        del entities[entity_id]
        if self._entity_cache is not None:
            del self._entity_cache[entity_id]
        return self._entity_backend.delete(entity_id)

    # ============================================================
    # 实体关系图谱 — Relationship Graph
    # ============================================================

    def add_relationship(
        self,
        from_entity_id: str,
        to_entity_id: str,
        relation_type: str,
        strength: int = 50,
        description: str = "",
        chapter: int = 0,
    ) -> Dict[str, Any]:
        entities = self._get_entities()
        from_entity = entities.get(from_entity_id)
        to_entity = entities.get(to_entity_id)

        if not from_entity or not to_entity:
            return {"status": "error", "error": "实体不存在"}

        relation_type = relation_type if relation_type in self.RELATIONSHIP_TYPES else "neutral"

        rel = {
            "target_id": to_entity_id,
            "target_name": to_entity.name,
            "relation_type": relation_type,
            "strength": max(0, min(100, strength)),
            "description": description,
            "established_chapter": chapter,
            "created_at": _utc_now_iso(),
        }

        existing = [r for r in from_entity.relationships if r.get("target_id") == to_entity_id]
        if existing:
            existing[0].update(rel)
        else:
            from_entity.relationships.append(rel)

        reverse_type = self._reverse_relation(relation_type)
        reverse_rel = {
            "target_id": from_entity_id,
            "target_name": from_entity.name,
            "relation_type": reverse_type,
            "strength": max(0, min(100, strength)),
            "description": description,
            "established_chapter": chapter,
            "created_at": _utc_now_iso(),
        }

        rev_existing = [r for r in to_entity.relationships if r.get("target_id") == from_entity_id]
        if rev_existing:
            rev_existing[0].update(reverse_rel)
        else:
            to_entity.relationships.append(reverse_rel)

        self._save_entity(from_entity)
        self._save_entity(to_entity)

        return {
            "status": "success",
            "from": from_entity.name,
            "to": to_entity.name,
            "relation_type": relation_type,
        }

    def _reverse_relation(self, relation_type: str) -> str:
        reverse_map = {
            "ally": "ally", "enemy": "enemy", "family": "family",
            "master_student": "master_student", "lover": "lover",
            "rival": "rival", "friend": "friend", "neutral": "neutral",
            "subordinate": "superior", "superior": "subordinate",
            "located_in": "contains", "owns": "belongs_to",
            "belongs_to": "owns", "created_by": "created",
            "member_of": "contains",
        }
        return reverse_map.get(relation_type, relation_type)

    def get_entity_relationships(self, entity_id: str) -> List[Dict[str, Any]]:
        entity = self._get_entities().get(entity_id)
        return entity.relationships if entity else []

    def get_relationship_graph(self) -> Dict[str, Any]:
        entities = self._get_entities()
        nodes = []
        edges = []
        seen_edges: Set[Tuple[str, str]] = set()

        for entity in entities.values():
            nodes.append({
                "id": entity.entity_id,
                "name": entity.name,
                "type": entity.entity_type,
                "appearances": entity.appearance_count,
            })
            for rel in entity.relationships:
                edge_key = tuple(sorted([entity.entity_id, rel["target_id"]]))
                if edge_key not in seen_edges:
                    seen_edges.add(edge_key)
                    edges.append({
                        "from": entity.entity_id,
                        "to": rel["target_id"],
                        "type": rel["relation_type"],
                        "strength": rel.get("strength", 50),
                    })

        return {"nodes": nodes, "edges": edges}

    # ============================================================
    # 语义搜索 — Semantic Search (TF-IDF)
    # ============================================================

    def _tokenize(self, text: str) -> List[str]:
        if not self._stopwords:
            self._stopwords = {
                "的", "了", "在", "是", "我", "有", "和", "就", "不", "人", "都", "一",
                "一个", "上", "也", "很", "到", "说", "要", "去", "你", "会", "着",
                "没有", "看", "好", "自己", "这", "他", "她", "它", "们", "那", "些",
                "什么", "怎么", "如何", "可以", "这个", "那个", "还是", "只是", "但是",
                "因为", "所以", "如果", "虽然", "而且", "然后", "之后", "之前", "已经",
                "正在", "一直", "一定", "一样", "一种", "一些", "可能", "应该", "需要",
            }

        text = re.sub(r'[^\u4e00-\u9fff\w]', ' ', text.lower())
        tokens = []
        i = 0
        chars = list(text)
        while i < len(chars):
            if chars[i] == ' ':
                i += 1
                continue
            if '\u4e00' <= chars[i] <= '\u9fff':
                bigram = chars[i]
                if i + 1 < len(chars) and '\u4e00' <= chars[i + 1] <= '\u9fff':
                    bigram += chars[i + 1]
                if bigram not in self._stopwords and len(bigram) >= 1:
                    tokens.append(bigram)
                i += 1
            else:
                word = ""
                while i < len(chars) and chars[i] not in (' ',) and not ('\u4e00' <= chars[i] <= '\u9fff'):
                    word += chars[i]
                    i += 1
                if word and word not in self._stopwords:
                    tokens.append(word)
        return tokens

    def _compute_tfidf(
        self,
        documents: List[Tuple[str, str]],
        query: str,
    ) -> List[Tuple[str, float]]:
        all_tokens = [self._tokenize(doc) for _, doc in documents]
        query_tokens = self._tokenize(query)

        if not query_tokens:
            return [(doc_id, 0.0) for doc_id, _ in documents]

        N = len(documents)
        df: Dict[str, int] = {}
        for tokens in all_tokens:
            for token in set(tokens):
                df[token] = df.get(token, 0) + 1

        scores: List[Tuple[str, float]] = []
        for idx, (doc_id, _) in enumerate(documents):
            tokens = all_tokens[idx]
            tf = Counter(tokens)
            score = 0.0
            for qt in query_tokens:
                if qt in tf and qt in df:
                    tf_val = tf[qt] / max(len(tokens), 1)
                    idf_val = math.log((N + 1) / (df[qt] + 1)) + 1
                    score += tf_val * idf_val
            scores.append((doc_id, score))

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores

    def semantic_search(
        self,
        query: str,
        search_in: str = "all",
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []

        if search_in in ("all", "patterns"):
            patterns = self._get_patterns()
            docs = [(f"pattern_{i}", p.description) for i, p in enumerate(patterns)]
            scored = self._compute_tfidf(docs, query)
            for doc_id, score in scored:
                if score > 0:
                    idx = int(doc_id.split("_")[1])
                    results.append({
                        "type": "pattern",
                        "score": round(score, 4),
                        "data": patterns[idx].to_dict(),
                    })

        if search_in in ("all", "entities"):
            entities = self._get_entities()
            docs = []
            for eid, entity in entities.items():
                text = f"{entity.name} {' '.join(entity.aliases)} {entity.notes} {' '.join(entity.attributes.values() if isinstance(entity.attributes, dict) else [])}"
                docs.append((eid, text))
            scored = self._compute_tfidf(docs, query)
            for eid, score in scored:
                if score > 0:
                    results.append({
                        "type": "entity",
                        "score": round(score, 4),
                        "data": entities[eid].to_dict(),
                    })

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:limit]

    # ============================================================
    # 记忆快照 — Memory Snapshots
    # ============================================================

    def create_snapshot(self, label: str = "") -> Dict[str, Any]:
        snapshot_id = _uid()
        patterns = self._get_patterns()
        entities = self._get_entities()

        snapshot = {
            "snapshot_id": snapshot_id,
            "label": label or f"snapshot_{snapshot_id}",
            "created_at": _utc_now_iso(),
            "patterns": [p.to_dict() for p in patterns],
            "entities": [e.to_dict() for e in entities.values()],
            "stats": self.get_memory_stats(),
        }

        self._snapshot_backend.save(snapshot_id, snapshot)
        return {
            "status": "success",
            "snapshot_id": snapshot_id,
            "label": snapshot["label"],
            "patterns_count": len(patterns),
            "entities_count": len(entities),
        }

    def restore_snapshot(self, snapshot_id: str) -> Dict[str, Any]:
        snapshot = self._snapshot_backend.load(snapshot_id)
        if not snapshot:
            return {"status": "error", "error": f"快照 {snapshot_id} 不存在"}

        patterns_data = snapshot.get("patterns", [])
        restored_patterns = [
            MemoryPattern(
                pattern_type=p.get("pattern_type", "other"),
                description=p.get("description", ""),
                category=p.get("category", ""),
                importance=p.get("importance", "medium"),
                source_chapter=p.get("source_chapter"),
                learned_at=p.get("learned_at", ""),
                updated_at=p.get("updated_at", ""),
                usage_count=p.get("usage_count", 0),
                effectiveness=p.get("effectiveness", 0.0),
            )
            for p in patterns_data
        ]
        self._save_patterns(restored_patterns)

        entities_data = snapshot.get("entities", [])
        for edata in entities_data:
            entity = EntityRecord(
                entity_id=edata.get("entity_id", _uid()),
                name=edata.get("name", ""),
                entity_type=edata.get("entity_type", "character"),
                aliases=edata.get("aliases", []),
                attributes=edata.get("attributes", {}),
                first_appearance=edata.get("first_appearance", 0),
                last_appearance=edata.get("last_appearance", 0),
                appearance_count=edata.get("appearance_count", 0),
                relationships=edata.get("relationships", []),
                notes=edata.get("notes", ""),
                created_at=edata.get("created_at", ""),
                updated_at=edata.get("updated_at", ""),
            )
            self._save_entity(entity)

        self._entity_cache = None
        self._patterns_cache = None

        return {
            "status": "success",
            "snapshot_id": snapshot_id,
            "label": snapshot.get("label", ""),
            "patterns_restored": len(restored_patterns),
            "entities_restored": len(entities_data),
        }

    def list_snapshots(self) -> List[Dict[str, Any]]:
        snapshots = []
        for key in self._snapshot_backend.list_keys():
            data = self._snapshot_backend.load(key)
            if data:
                snapshots.append({
                    "snapshot_id": key,
                    "label": data.get("label", ""),
                    "created_at": data.get("created_at", ""),
                    "patterns_count": len(data.get("patterns", [])),
                    "entities_count": len(data.get("entities", [])),
                })
        snapshots.sort(key=lambda s: s.get("created_at", ""), reverse=True)
        return snapshots

    def delete_snapshot(self, snapshot_id: str) -> bool:
        return self._snapshot_backend.delete(snapshot_id)

    # ============================================================
    # 实体检测 — Entity Detection from Text
    # ============================================================

    def detect_entities_from_text(
        self,
        text: str,
        chapter: int = 0,
        known_names: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        detected: Dict[str, List[str]] = {
            "characters": [],
            "locations": [],
            "items": [],
            "organizations": [],
        }

        known_set = set(known_names or [])

        name_pattern = r'(?:([\u4e00-\u9fff]{2,4})(?:说道|问道|喊道|笑道|怒道|冷声道|淡淡道|缓缓道|低声道|大声道|开口道|回答|回应|开口))'
        names_found = re.findall(name_pattern, text)
        for name in names_found:
            if name not in known_set and name not in detected["characters"]:
                detected["characters"].append(name)

        location_suffixes = r'(?:山|峰|谷|城|镇|村|殿|阁|楼|塔|洞|府|界|域|国|宗|派|门|院|宫|寺|观|岛|海|湖|河|林|原|崖|渊)'
        location_pattern = rf'([\u4e00-\u9fff]{{2,6}}{location_suffixes})'
        locations_found = re.findall(location_pattern, text)
        for loc in locations_found:
            if loc not in detected["locations"]:
                detected["locations"].append(loc)

        item_pattern = r'(?:([\u4e00-\u9fff]{2,5}(?:剑|刀|枪|棍|鞭|弓|戟|斧|锤|扇|针|鼎|炉|塔|镜|珠|符|阵|丹|药|甲|袍|令|牌|印|石|玉|环|戒|镯|佩|卷|书|册|图|录|谱|经|典|诀|法|术|功)))'
        items_found = re.findall(item_pattern, text)
        for item in items_found:
            if item not in detected["items"]:
                detected["items"].append(item)

        org_pattern = r'(?:([\u4e00-\u9fff]{2,6}(?:宗|派|门|教|帮|会|盟|阁|楼|殿|宫|府|院|堂|庄|堡|城|国|朝|族|氏|家|族|谷|岛|山|峰|塔|寺|观|庵|斋|坊|馆|店|行|号|社|团|队|组|军|营|卫|司|局|处|部|院|所)))'
        orgs_found = re.findall(org_pattern, text)
        for org in orgs_found:
            if org not in detected["organizations"] and org not in detected["locations"]:
                detected["organizations"].append(org)

        registered: Dict[str, List[str]] = {
            "characters": [],
            "locations": [],
            "items": [],
            "organizations": [],
        }

        for entity_type, names in detected.items():
            for name in names[:10]:
                result = self.register_entity(
                    name=name,
                    entity_type="character" if entity_type == "characters" else (
                        "location" if entity_type == "locations" else (
                            "item" if entity_type == "items" else "organization"
                        )
                    ),
                    chapter=chapter,
                )
                registered[entity_type].append({
                    "name": name,
                    "status": result.get("status", "unknown"),
                })

        return {
            "detected": {k: v[:10] for k, v in detected.items()},
            "registered": registered,
            "total_detected": sum(len(v) for v in detected.values()),
        }

    # ============================================================
    # 存储后端管理
    # ============================================================

    def get_storage_health(self) -> Dict[str, Any]:
        return {
            "patterns_backend": {
                "type": "JSONFile",
                "path": str(self._memory_path),
                "exists": self._memory_path.exists(),
            },
            "entity_backend": self._entity_backend.health_check(),
            "snapshot_backend": self._snapshot_backend.health_check(),
        }

    def get_entity_stats(self) -> Dict[str, Any]:
        entities = self._get_entities()
        type_counts: Dict[str, int] = {}
        total_relationships = 0

        for entity in entities.values():
            type_counts[entity.entity_type] = type_counts.get(entity.entity_type, 0) + 1
            total_relationships += len(entity.relationships)

        return {
            "total_entities": len(entities),
            "by_type": type_counts,
            "total_relationships": total_relationships // 2,
            "entities_with_most_appearances": sorted(
                [{"name": e.name, "count": e.appearance_count} for e in entities.values()],
                key=lambda x: x["count"], reverse=True,
            )[:5],
        }

    def get_fingerprint(self) -> Dict[str, Any]:
        fp_path = self._memory_path.parent / "writing_fingerprint.json"
        if fp_path.exists():
            try:
                with open(fp_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"[ProjectMemory] Failed to load fingerprint: {e}")
        return {}

    def generate_fingerprint(self, chapters: List[Dict], genres: List[str], styles: List[str]) -> Dict[str, Any]:
        from llm_interface import llm, GenerationParams

        combined_text = ""
        for ch in chapters:
            combined_text += f"\n--- 第{ch.get('chapter', '?')}章 ---\n{ch.get('text', '')[:2000]}"

        prompt = f"""你是一位专业的写作风格分析师。请分析以下小说章节的写作风格特征，生成"写作指纹"。

## 小说信息
- 题材：{', '.join(genres) if genres else '未指定'}
- 风格：{', '.join(styles) if styles else '未指定'}

## 章节内容（节选）
{combined_text[:4000]}

## 分析要求
请从以下维度分析写作风格，返回纯JSON：

1. **句式风格** (sentence_style)：短句/长句/混合，平均句长偏好
2. **节奏偏好** (pacing)：快节奏/慢节奏/中等，场景切换频率
3. **对话占比** (dialogue_ratio)：高/适中/低
4. **叙事视角** (pov)：第一人称/第三人称/多视角
5. **描写密度** (description_density)：高/中/低
6. **情感基调** (emotional_tone)：热血/冷静/幽默/沉重/混合
7. **风格规则** (style_rules)：至少5条具体的写作规则，用于指导后续章节保持风格一致

返回JSON格式：
{{"style_profile": {{"sentence_style": "...", "pacing": "...", "dialogue_ratio": "...", "pov": "...", "description_density": "...", "emotional_tone": "..."}}, "style_rules": ["规则1", "规则2", ...], "locked": false}}"""

        try:
            response = llm(prompt, GenerationParams(temperature=0.4, max_tokens=1500))
            json_str = response
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0]
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0]
            fp = json.loads(json_str.strip())
            fp["generated_at"] = _utc_now_iso()
            fp["chapter_count"] = len(chapters)
            fp["genres"] = genres
            fp["styles"] = styles

            fp_path = self._memory_path.parent / "writing_fingerprint.json"
            with open(fp_path, 'w', encoding='utf-8') as f:
                json.dump(fp, f, ensure_ascii=False, indent=2)

            return fp
        except Exception as e:
            return {"error": str(e)[:200], "style_profile": {}, "style_rules": [], "locked": False}

    def lock_fingerprint(self) -> None:
        fp_path = self._memory_path.parent / "writing_fingerprint.json"
        fp = {}
        if fp_path.exists():
            try:
                with open(fp_path, 'r', encoding='utf-8') as f:
                    fp = json.load(f)
            except Exception as e:
                print(f"[ProjectMemory] Failed to load fingerprint for lock: {e}")
        fp["locked"] = True
        fp["locked_at"] = _utc_now_iso()
        with open(fp_path, 'w', encoding='utf-8') as f:
            json.dump(fp, f, ensure_ascii=False, indent=2)

    def unlock_fingerprint(self) -> None:
        fp_path = self._memory_path.parent / "writing_fingerprint.json"
        fp = {}
        if fp_path.exists():
            try:
                with open(fp_path, 'r', encoding='utf-8') as f:
                    fp = json.load(f)
            except Exception as e:
                print(f"[ProjectMemory] Failed to load fingerprint for unlock: {e}")
        fp["locked"] = False
        with open(fp_path, 'w', encoding='utf-8') as f:
            json.dump(fp, f, ensure_ascii=False, indent=2)

    def check_style_consistency(self, chapter: int, text: str) -> Dict[str, Any]:
        from llm_interface import llm, GenerationParams

        fp = self.get_fingerprint()
        if not fp or not fp.get('style_profile'):
            return {"consistency_score": 100, "deviations": [], "note": "无写作指纹，无法检查"}

        style_profile = fp.get('style_profile', {})
        style_rules = fp.get('style_rules', [])

        prompt = f"""你是一位严格的写作风格审查员。请检查以下章节是否与写作指纹一致。

## 写作指纹（目标风格）
- 句式风格：{style_profile.get('sentence_style', '')}
- 节奏偏好：{style_profile.get('pacing', '')}
- 对话占比：{style_profile.get('dialogue_ratio', '')}
- 叙事视角：{style_profile.get('pov', '')}
- 描写密度：{style_profile.get('description_density', '')}
- 情感基调：{style_profile.get('emotional_tone', '')}

## 风格规则
{chr(10).join(f'- {r}' for r in style_rules) if style_rules else '无'}

## 待检查章节（第{chapter}章）
{text[:3000]}

## 输出要求
返回纯JSON，评估一致性得分（0-100）和偏差列表：
{{"consistency_score": 85, "deviations": [{{"aspect": "句式风格", "expected": "...", "actual": "...", "suggestion": "..."}}]}}"""

        try:
            response = llm(prompt, GenerationParams(temperature=0.3, max_tokens=800))
            json_str = response
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0]
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0]
            return json.loads(json_str.strip())
        except Exception as e:
            return {"consistency_score": 50, "deviations": [{"description": f"检查失败: {str(e)[:100]}"}]}


class TruthFilesManager:
    """7真相文件记忆系统 — 叙事一致性引擎

    管理七个核心真相文件，确保长篇小说在以下维度保持一致性:
    1. current_state   — 世界状态：角色位置、关系网络、已知信息、情感状态
    2. particle_ledger — 资源账本：物品、金钱、物资数量及衰减追踪
    3. pending_hooks   — 未闭合伏笔：铺垫、对读者的承诺、未解决冲突
    4. chapter_summaries — 章节摘要：每章核心事件、情感变化、关键决策
    5. subplot_progress — 支线进度：各条辅线的推进状态和关键节点
    6. emotional_arcs   — 情感弧线：主要角色的情感变化曲线
    7. character_matrix — 角色矩阵：角色关系、动机、能力变化
    """

    TRUTH_FILES = [
        "current_state",
        "particle_ledger",
        "pending_hooks",
        "chapter_summaries",
        "subplot_progress",
        "emotional_arcs",
        "character_matrix",
    ]

    def __init__(self, project_dir):
        self.truth_dir = Path(project_dir) / "truth_files"
        self.truth_dir.mkdir(parents=True, exist_ok=True)
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._init_truth_files()

    def _init_truth_files(self) -> None:
        templates = {
            "current_state": {
                "world_time": "",
                "locations": {},
                "character_positions": {},
                "known_information": [],
                "active_conflicts": [],
                "atmosphere": "",
                "last_updated_chapter": 0,
            },
            "particle_ledger": {
                "items": {},
                "currency": {},
                "resources": {},
                "last_updated_chapter": 0,
            },
            "pending_hooks": {
                "hooks": [],
                "promises_to_reader": [],
                "unresolved_conflicts": [],
                "last_updated_chapter": 0,
            },
            "chapter_summaries": {
                "chapters": {},
                "last_updated_chapter": 0,
            },
            "subplot_progress": {
                "subplots": {},
                "last_updated_chapter": 0,
            },
            "emotional_arcs": {
                "characters": {},
                "last_updated_chapter": 0,
            },
            "character_matrix": {
                "characters": {},
                "relationships": [],
                "last_updated_chapter": 0,
            },
        }

        for name in self.TRUTH_FILES:
            path = self.truth_dir / f"{name}.json"
            if not path.exists():
                path.write_text(json.dumps(templates[name], ensure_ascii=False, indent=2), encoding="utf-8")

    def _load(self, name: str) -> Dict[str, Any]:
        if name in self._cache:
            return self._cache[name]
        path = self.truth_dir / f"{name}.json"
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            self._cache[name] = data
            return data
        return {}

    def _save(self, name: str, data: Dict[str, Any]) -> None:
        path = self.truth_dir / f"{name}.json"
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        self._cache[name] = data

    def update_current_state(
        self,
        chapter: int,
        world_time: str = "",
        locations: Optional[Dict[str, str]] = None,
        character_positions: Optional[Dict[str, str]] = None,
        known_information: Optional[List[str]] = None,
        active_conflicts: Optional[List[str]] = None,
        atmosphere: str = "",
    ) -> Dict[str, Any]:
        data = self._load("current_state")
        if world_time:
            data["world_time"] = world_time
        if locations:
            data["locations"].update(locations)
        if character_positions:
            data["character_positions"].update(character_positions)
        if known_information:
            for info in known_information:
                if info not in data["known_information"]:
                    data["known_information"].append(info)
        if active_conflicts:
            for conflict in active_conflicts:
                if conflict not in data["active_conflicts"]:
                    data["active_conflicts"].append(conflict)
        if atmosphere:
            data["atmosphere"] = atmosphere
        data["last_updated_chapter"] = chapter
        self._save("current_state", data)
        return {"status": "success", "file": "current_state", "chapter": chapter}

    def update_particle_ledger(
        self,
        chapter: int,
        items: Optional[Dict[str, Dict[str, Any]]] = None,
        currency: Optional[Dict[str, int]] = None,
        resources: Optional[Dict[str, int]] = None,
    ) -> Dict[str, Any]:
        data = self._load("particle_ledger")
        if items:
            for name, info in items.items():
                if name in data["items"]:
                    data["items"][name].update(info)
                else:
                    data["items"][name] = info
        if currency:
            for k, v in currency.items():
                data["currency"][k] = data["currency"].get(k, 0) + v
        if resources:
            for k, v in resources.items():
                data["resources"][k] = data["resources"].get(k, 0) + v
        data["last_updated_chapter"] = chapter
        self._save("particle_ledger", data)
        return {"status": "success", "file": "particle_ledger", "chapter": chapter}

    def add_hook(
        self,
        chapter: int,
        hook_description: str,
        hook_type: str = "foreshadowing",
        expected_resolution_chapter: Optional[int] = None,
        related_characters: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        data = self._load("pending_hooks")
        hook = {
            "id": _uid(),
            "description": hook_description,
            "type": hook_type,
            "planted_chapter": chapter,
            "expected_resolution_chapter": expected_resolution_chapter,
            "related_characters": related_characters or [],
            "status": "pending",
            "created_at": _utc_now_iso(),
        }
        data["hooks"].append(hook)
        data["last_updated_chapter"] = chapter
        self._save("pending_hooks", data)
        return {"status": "success", "hook_id": hook["id"], "chapter": chapter}

    def resolve_hook(self, hook_id: str, resolution_chapter: int, resolution_note: str = "") -> Dict[str, Any]:
        data = self._load("pending_hooks")
        for hook in data["hooks"]:
            if hook["id"] == hook_id:
                hook["status"] = "resolved"
                hook["resolved_chapter"] = resolution_chapter
                hook["resolution_note"] = resolution_note
                hook["resolved_at"] = _utc_now_iso()
                self._save("pending_hooks", data)
                return {"status": "success", "hook_id": hook_id, "resolved": True}
        return {"status": "error", "error": f"Hook {hook_id} not found"}

    def get_pending_hooks(self) -> List[Dict[str, Any]]:
        data = self._load("pending_hooks")
        return [h for h in data["hooks"] if h.get("status") == "pending"]

    def add_chapter_summary(
        self,
        chapter: int,
        title: str = "",
        core_events: Optional[List[str]] = None,
        emotional_changes: Optional[List[str]] = None,
        key_decisions: Optional[List[str]] = None,
        character_appearances: Optional[Dict[str, str]] = None,
        word_count: int = 0,
    ) -> Dict[str, Any]:
        data = self._load("chapter_summaries")
        data["chapters"][str(chapter)] = {
            "title": title,
            "core_events": core_events or [],
            "emotional_changes": emotional_changes or [],
            "key_decisions": key_decisions or [],
            "character_appearances": character_appearances or {},
            "word_count": word_count,
            "recorded_at": _utc_now_iso(),
        }
        data["last_updated_chapter"] = chapter
        self._save("chapter_summaries", data)
        return {"status": "success", "chapter": chapter}

    def update_subplot(
        self,
        subplot_id: str,
        chapter: int,
        progress_description: str = "",
        milestone_reached: Optional[str] = None,
        status: str = "active",
    ) -> Dict[str, Any]:
        data = self._load("subplot_progress")
        if subplot_id not in data["subplots"]:
            data["subplots"][subplot_id] = {
                "id": subplot_id,
                "name": subplot_id,
                "status": "active",
                "progress_log": [],
                "milestones": [],
                "created_at": _utc_now_iso(),
            }
        sp = data["subplots"][subplot_id]
        sp["status"] = status
        if progress_description:
            sp["progress_log"].append({
                "chapter": chapter,
                "description": progress_description,
                "timestamp": _utc_now_iso(),
            })
        if milestone_reached:
            sp["milestones"].append({
                "chapter": chapter,
                "milestone": milestone_reached,
                "timestamp": _utc_now_iso(),
            })
        data["last_updated_chapter"] = chapter
        self._save("subplot_progress", data)
        return {"status": "success", "subplot_id": subplot_id, "chapter": chapter}

    def update_emotional_arc(
        self,
        character_name: str,
        chapter: int,
        emotional_state: str = "",
        intensity: int = 50,
        trigger_event: str = "",
        arc_phase: str = "",
    ) -> Dict[str, Any]:
        data = self._load("emotional_arcs")
        if character_name not in data["characters"]:
            data["characters"][character_name] = {
                "name": character_name,
                "arc_points": [],
                "current_state": "",
                "current_intensity": 50,
                "overall_arc": "",
            }
        char = data["characters"][character_name]
        if emotional_state:
            char["current_state"] = emotional_state
        char["current_intensity"] = intensity
        char["arc_points"].append({
            "chapter": chapter,
            "state": emotional_state,
            "intensity": intensity,
            "trigger": trigger_event,
            "arc_phase": arc_phase,
            "timestamp": _utc_now_iso(),
        })
        data["last_updated_chapter"] = chapter
        self._save("emotional_arcs", data)
        return {"status": "success", "character": character_name, "chapter": chapter}

    def update_character_matrix(
        self,
        character_name: str,
        chapter: int,
        role: str = "",
        motivation: str = "",
        ability_changes: Optional[List[str]] = None,
        relationships: Optional[List[Dict[str, Any]]] = None,
        current_goal: str = "",
    ) -> Dict[str, Any]:
        data = self._load("character_matrix")
        if character_name not in data["characters"]:
            data["characters"][character_name] = {
                "name": character_name,
                "role": role,
                "first_appearance": chapter,
                "motivation_history": [],
                "ability_changes": [],
                "current_goal": "",
                "status": "active",
            }
        char = data["characters"][character_name]
        if role:
            char["role"] = role
        if motivation:
            char["motivation_history"].append({
                "chapter": chapter,
                "motivation": motivation,
                "timestamp": _utc_now_iso(),
            })
        if ability_changes:
            for change in ability_changes:
                char["ability_changes"].append({
                    "chapter": chapter,
                    "change": change,
                    "timestamp": _utc_now_iso(),
                })
        if current_goal:
            char["current_goal"] = current_goal
        if relationships:
            for rel in relationships:
                existing = next((r for r in data["relationships"] if r["from"] == character_name and r["to"] == rel.get("to")), None)
                if existing:
                    existing.update(rel)
                else:
                    data["relationships"].append({
                        "from": character_name,
                        "to": rel.get("to", ""),
                        "type": rel.get("type", "neutral"),
                        "strength": rel.get("strength", 50),
                        "last_updated_chapter": chapter,
                    })
        data["last_updated_chapter"] = chapter
        self._save("character_matrix", data)
        return {"status": "success", "character": character_name, "chapter": chapter}

    def get_context_for_chapter(self, chapter: int) -> str:
        """为章节生成获取完整的叙事上下文注入"""
        parts = []

        state = self._load("current_state")
        if state.get("character_positions"):
            parts.append("## 当前世界状态")
            parts.append(f"- 时间：{state.get('world_time', '未知')}")
            parts.append(f"- 氛围：{state.get('atmosphere', '未知')}")
            for name, pos in state.get("character_positions", {}).items():
                parts.append(f"- {name} 位于：{pos}")
            if state.get("active_conflicts"):
                parts.append(f"- 活跃冲突：{', '.join(state['active_conflicts'])}")

        ledger = self._load("particle_ledger")
        if ledger.get("items") or ledger.get("currency"):
            parts.append("\n## 资源状态")
            for name, info in ledger.get("items", {}).items():
                qty = info.get("quantity", "?")
                parts.append(f"- {name}：{qty}")
            for k, v in ledger.get("currency", {}).items():
                parts.append(f"- {k}：{v}")

        hooks = self._load("pending_hooks")
        pending = [h for h in hooks.get("hooks", []) if h.get("status") == "pending"]
        if pending:
            parts.append("\n## 待闭合伏笔（必须在后续章节中呼应）")
            for h in pending:
                parts.append(f"- [第{h.get('planted_chapter', '?')}章埋下] {h.get('description', '')}")

        matrix = self._load("character_matrix")
        if matrix.get("characters"):
            parts.append("\n## 角色当前状态")
            for name, char in matrix.get("characters", {}).items():
                parts.append(f"- {name}（{char.get('role', '未知')}）：目标={char.get('current_goal', '未知')}")

        arcs = self._load("emotional_arcs")
        if arcs.get("characters"):
            parts.append("\n## 角色情感状态")
            for name, char in arcs.get("characters", {}).items():
                parts.append(f"- {name}：{char.get('current_state', '未知')}（强度{char.get('current_intensity', 50)}）")

        return "\n".join(parts) if parts else ""

    def get_all_truth_files(self) -> Dict[str, Any]:
        result = {}
        for name in self.TRUTH_FILES:
            result[name] = self._load(name)
        return result

    def get_truth_file(self, name: str) -> Optional[Dict[str, Any]]:
        if name in self.TRUTH_FILES:
            return self._load(name)
        return None

    def clear_cache(self) -> None:
        self._cache.clear()