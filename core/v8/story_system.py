#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Story System — NWACS 故事系统核心模块 v3.0

核心功能:
1. MASTER_SETTING — 故事主设定（调性/禁忌/题材画像）
2. Volume Contracts — 卷级合同（节奏/结构/伏笔）
3. Chapter Contracts — 章级合同（必须节点/禁区/风格指引）
4. CHAPTER_COMMIT — 章节提交与投影链
5. Story Runtime — 运行时合同（动态裁决层）
6. State Snapshots — 状态快照与回滚
7. Book Lock — 书籍锁定防并发编辑
8. Control Document — 控制文档管理

设计原则:
- .story-system/ 是主链真源
- .webnovel/ 是投影/read-model
- 合同驱动写作，而非自由发挥
- 每次重大变更前自动创建快照
- 并发编辑通过书籍锁保护
"""

from __future__ import annotations

import json
import os
import re
import uuid
from copy import deepcopy
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _atomic_write_json(path: Path, data: Dict[str, Any]) -> None:
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp_path.replace(path)


@dataclass
class StoryContract:
    contract_id: str
    contract_type: str
    version: int = 1
    created_at: str = field(default_factory=_utc_now_iso)
    updated_at: str = field(default_factory=_utc_now_iso)
    data: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ChapterCommit:
    commit_id: str
    chapter: int
    status: str = "pending"
    review_result: Dict[str, Any] = field(default_factory=dict)
    fulfillment_result: Dict[str, Any] = field(default_factory=dict)
    extraction_result: Dict[str, Any] = field(default_factory=dict)
    state_deltas: List[Dict[str, Any]] = field(default_factory=list)
    entity_deltas: List[Dict[str, Any]] = field(default_factory=list)
    accepted_events: List[Dict[str, Any]] = field(default_factory=list)
    created_at: str = field(default_factory=_utc_now_iso)
    meta: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class StateSnapshot:
    """状态快照 — 可保存/恢复的完整状态"""
    snapshot_id: str
    chapter: int
    label: str = ""
    state_data: Dict[str, Any] = field(default_factory=dict)
    master_setting_snapshot: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=_utc_now_iso)
    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class BookLock:
    """书籍锁 — 防并发编辑"""
    lock_id: str
    locked_by: str = ""
    locked_at: str = field(default_factory=_utc_now_iso)
    expires_at: str = ""
    lock_reason: str = ""
    is_active: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @property
    def is_expired(self) -> bool:
        if not self.expires_at:
            return False
        return _utc_now_iso() > self.expires_at


class StorySystem:
    """故事系统 — 管理故事合同、章节提交和投影链"""

    def __init__(self, project_root: str):
        self.project_root = Path(project_root).expanduser().resolve()
        self.story_system_dir = self.project_root / ".story-system"
        self.webnovel_dir = self.project_root / ".webnovel"
        self._ensure_dirs()

    def _ensure_dirs(self) -> None:
        for d in [
            self.story_system_dir,
            self.story_system_dir / "volumes",
            self.story_system_dir / "chapters",
            self.story_system_dir / "reviews",
            self.story_system_dir / "commits",
            self.webnovel_dir,
            self.webnovel_dir / "summaries",
            self.webnovel_dir / "reports",
            self.webnovel_dir / "tmp",
        ]:
            d.mkdir(parents=True, exist_ok=True)

    def _load_json(self, path: Path) -> Dict[str, Any]:
        if not path.exists():
            return {}
        return json.loads(path.read_text(encoding="utf-8"))

    def _save_json(self, path: Path, data: Dict[str, Any]) -> None:
        _atomic_write_json(path, data)

    def init_master_setting(
        self,
        title: str,
        genre: str,
        sub_genre: str = "",
        tone: str = "",
        style: str = "",
        protagonist_name: str = "",
        protagonist_desire: str = "",
        protagonist_flaw: str = "",
        core_conflict: str = "",
        world_type: str = "",
        power_system: str = "",
        taboos: Optional[List[str]] = None,
        anti_patterns: Optional[List[str]] = None,
        genre_profile: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        master = {
            "meta": {
                "version": "1.0.0",
                "created_at": _utc_now_iso(),
                "updated_at": _utc_now_iso(),
                "title": title,
                "genre": genre,
                "sub_genre": sub_genre,
            },
            "tone_and_style": {
                "tone": tone,
                "style": style,
                "narrative_voice": "",
                "pacing_default": "medium",
                "dialogue_ratio": "medium",
                "description_density": "medium",
            },
            "protagonist": {
                "name": protagonist_name,
                "core_desire": protagonist_desire,
                "fatal_flaw": protagonist_flaw,
                "initial_state": "",
                "growth_arc": "",
                "voice_characteristics": [],
            },
            "story_engine": {
                "core_conflict": core_conflict,
                "world_type": world_type,
                "power_system": power_system,
                "central_mystery": "",
                "endgame_vision": "",
            },
            "constraints": {
                "taboos": taboos or [],
                "anti_patterns": anti_patterns or [],
                "hard_rules": [],
                "style_priorities": [],
            },
            "genre_profile": genre_profile or {},
            "foreshadowing_registry": [],
            "character_registry": [],
            "world_rules": [],
        }
        path = self.story_system_dir / "MASTER_SETTING.json"
        self._save_json(path, master)
        self._sync_to_state({"master_setting_initialized": True})
        return master

    def get_master_setting(self) -> Dict[str, Any]:
        return self._load_json(self.story_system_dir / "MASTER_SETTING.json")

    def update_master_setting(self, updates: Dict[str, Any]) -> Dict[str, Any]:
        master = self.get_master_setting()
        _deep_update(master, updates)
        master["meta"]["updated_at"] = _utc_now_iso()
        self._save_json(self.story_system_dir / "MASTER_SETTING.json", master)
        return master

    def create_volume_contract(
        self,
        volume_id: int,
        volume_name: str,
        chapter_range: Tuple[int, int],
        core_conflict: str,
        volume_climax: str,
        pacing_strategy: str = "standard",
        strand_distribution: Optional[Dict[str, List[int]]] = None,
        cool_point_density: str = "medium",
        foreshadowing_plan: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        contract = {
            "meta": {
                "version": "1.0.0",
                "created_at": _utc_now_iso(),
                "volume_id": volume_id,
                "volume_name": volume_name,
                "chapter_start": chapter_range[0],
                "chapter_end": chapter_range[1],
            },
            "structure": {
                "core_conflict": core_conflict,
                "volume_climax": volume_climax,
                "midpoint_twist": "",
                "crisis_chain": [],
                "volume_end_hook": "",
            },
            "pacing": {
                "strategy": pacing_strategy,
                "cool_point_density": cool_point_density,
                "strand_distribution": strand_distribution or {},
                "beat_sheet": {},
            },
            "foreshadowing": foreshadowing_plan or [],
            "characters_in_volume": [],
            "world_rules_introduced": [],
        }
        path = self.story_system_dir / "volumes" / f"volume_{volume_id:03d}.json"
        self._save_json(path, contract)
        return contract

    def get_volume_contract(self, volume_id: int) -> Dict[str, Any]:
        return self._load_json(
            self.story_system_dir / "volumes" / f"volume_{volume_id:03d}.json"
        )

    def create_chapter_contract(
        self,
        chapter: int,
        volume_id: int,
        chapter_title: str = "",
        chapter_goal: str = "",
        time_anchor: str = "",
        chapter_span: str = "",
        countdown: Optional[str] = None,
        cbn: Optional[str] = None,
        cpns: Optional[List[str]] = None,
        cen: Optional[str] = None,
        must_cover_nodes: Optional[List[str]] = None,
        forbidden_zones: Optional[List[str]] = None,
        style_priority: str = "",
        pacing_strategy: str = "",
        anti_patterns: Optional[List[str]] = None,
        chapter_end_open_question: str = "",
    ) -> Dict[str, Any]:
        contract = {
            "meta": {
                "version": "1.0.0",
                "created_at": _utc_now_iso(),
                "chapter": chapter,
                "volume_id": volume_id,
                "title": chapter_title,
            },
            "chapter_directive": {
                "goal": chapter_goal,
                "time_anchor": time_anchor,
                "chapter_span": chapter_span,
                "countdown": countdown,
                "chapter_end_open_question": chapter_end_open_question,
            },
            "plot_structure": {
                "CBN": cbn or "",
                "CPNs": cpns or [],
                "CEN": cen or "",
                "must_cover_nodes": must_cover_nodes or [],
                "forbidden_zones": forbidden_zones or [],
            },
            "reasoning": {
                "style_priority": style_priority,
                "pacing_strategy": pacing_strategy,
                "anti_patterns": anti_patterns or [],
            },
            "dynamic_context": {},
            "fulfillment_status": "pending",
        }
        path = self.story_system_dir / "chapters" / f"chapter_{chapter:04d}.json"
        self._save_json(path, contract)
        return contract

    def get_chapter_contract(self, chapter: int) -> Dict[str, Any]:
        return self._load_json(
            self.story_system_dir / "chapters" / f"chapter_{chapter:04d}.json"
        )

    def create_review_contract(
        self,
        chapter: int,
        review_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        contract = {
            "meta": {
                "version": "1.0.0",
                "created_at": _utc_now_iso(),
                "chapter": chapter,
            },
            "issues": review_data.get("issues", []),
            "summary": review_data.get("summary", ""),
            "blocking_count": review_data.get("blocking_count", 0),
            "overall_status": review_data.get("overall_status", "pending"),
        }
        path = self.story_system_dir / "reviews" / f"chapter_{chapter:04d}.review.json"
        self._save_json(path, contract)
        return contract

    def get_review_contract(self, chapter: int) -> Dict[str, Any]:
        return self._load_json(
            self.story_system_dir / "reviews" / f"chapter_{chapter:04d}.review.json"
        )

    def build_chapter_commit(
        self,
        chapter: int,
        review_result: Dict[str, Any],
        fulfillment_result: Dict[str, Any],
        extraction_result: Dict[str, Any],
    ) -> Dict[str, Any]:
        issues = review_result.get("issues", [])
        blocking_count = sum(1 for i in issues if i.get("blocking"))
        missed_nodes = fulfillment_result.get("missed_nodes", [])
        pending_items = fulfillment_result.get("pending", [])

        if blocking_count > 0 or missed_nodes or pending_items:
            status = "rejected"
        else:
            status = "accepted"

        commit = {
            "commit_id": str(uuid.uuid4()),
            "chapter": chapter,
            "status": status,
            "meta": {
                "created_at": _utc_now_iso(),
                "blocking_count": blocking_count,
                "missed_nodes": missed_nodes,
                "pending_items": pending_items,
            },
            "review": review_result,
            "fulfillment": fulfillment_result,
            "extraction": extraction_result,
            "projections": {
                "state": "pending",
                "index": "pending",
                "summary": "pending",
                "memory": "pending",
                "vector": "pending",
            },
        }

        path = self.story_system_dir / "commits" / f"commit_ch{chapter:04d}.json"
        self._save_json(path, commit)
        return commit

    def apply_projections(self, commit: Dict[str, Any]) -> Dict[str, Any]:
        chapter = commit["chapter"]
        extraction = commit.get("extraction", {})

        self._project_state(chapter, extraction)
        self._project_summary(chapter, extraction)
        self._project_memory(extraction)

        commit["projections"] = {
            "state": "done",
            "index": "done",
            "summary": "done",
            "memory": "done",
            "vector": "skipped",
        }
        commit["meta"]["chapter_status"] = "committed"

        path = self.story_system_dir / "commits" / f"commit_ch{chapter:04d}.json"
        self._save_json(path, commit)
        return commit

    def _project_state(self, chapter: int, extraction: Dict[str, Any]) -> None:
        state_path = self.webnovel_dir / "state.json"
        state = self._load_json(state_path)

        progress = state.setdefault("progress", {})
        progress["current_chapter"] = chapter

        protagonist_state = state.setdefault("protagonist_state", {})
        for delta in extraction.get("state_deltas", []):
            entity_id = delta.get("entity_id", "")
            field = delta.get("field", "")
            new_val = delta.get("new", "")
            if entity_id == "protagonist" or delta.get("is_protagonist"):
                _set_nested(protagonist_state, field, new_val)

        strand_tracker = state.setdefault("strand_tracker", {"history": []})
        dominant = extraction.get("dominant_strand", "")
        if dominant:
            strand_tracker["history"].append({
                "chapter": chapter,
                "dominant": dominant,
                "timestamp": _utc_now_iso(),
            })
            if len(strand_tracker["history"]) > 20:
                strand_tracker["history"] = strand_tracker["history"][-20:]

        plot_threads = state.setdefault("plot_threads", {})
        foreshadowing = plot_threads.setdefault("foreshadowing", [])
        for event in extraction.get("accepted_events", []):
            if event.get("event_type") == "open_loop_created":
                payload = event.get("payload", {})
                foreshadowing.append({
                    "content": payload.get("content", ""),
                    "chapter": chapter,
                    "status": "active",
                    "urgency": payload.get("urgency", 50),
                    "expected_payoff": payload.get("expected_payoff", ""),
                })
            elif event.get("event_type") in ("open_loop_closed", "promise_paid_off"):
                payload = event.get("payload", {})
                for item in foreshadowing:
                    if item.get("content") == payload.get("content", ""):
                        item["status"] = "resolved"
                        item["resolved_chapter"] = chapter

        self._save_json(state_path, state)

    def _project_summary(self, chapter: int, extraction: Dict[str, Any]) -> None:
        summary_text = extraction.get("summary_text", "")
        scenes = extraction.get("scenes", [])
        entities = extraction.get("entities_appeared", [])
        state_deltas = extraction.get("state_deltas", [])

        summary_path = self.webnovel_dir / "summaries" / f"ch{chapter:04d}.md"
        lines = [
            f"---",
            f"chapter: {chapter:04d}",
            f"time: \"{extraction.get('time_anchor', '')}\"",
            f"location: \"{extraction.get('location', '')}\"",
            f"characters: {json.dumps([e.get('name', '') for e in entities], ensure_ascii=False)}",
            f"state_changes: {json.dumps([d.get('entity_id', '') + ': ' + d.get('old', '') + '→' + d.get('new', '') for d in state_deltas], ensure_ascii=False)}",
            f"hook_type: \"{extraction.get('hook_type', '')}\"",
            f"hook_strength: \"{extraction.get('hook_strength', '')}\"",
            f"---",
            f"",
            f"## 剧情摘要",
            f"",
            f"{summary_text}",
            f"",
        ]

        if scenes:
            lines.append("## 场景索引")
            lines.append("")
            for i, scene in enumerate(scenes):
                lines.append(f"- 场景{i+1}: {scene.get('location', '')} — {scene.get('summary', '')}")

        summary_path.write_text("\n".join(lines), encoding="utf-8")

    def _project_memory(self, extraction: Dict[str, Any]) -> None:
        memory_path = self.webnovel_dir / "memory_scratchpad.json"
        memory = self._load_json(memory_path)

        long_term = memory.setdefault("long_term", [])
        for event in extraction.get("accepted_events", []):
            if event.get("event_type") in (
                "world_rule_revealed",
                "character_state_changed",
                "relationship_changed",
            ):
                entry = {
                    "event_type": event["event_type"],
                    "payload": event.get("payload", {}),
                    "recorded_at": _utc_now_iso(),
                }
                if entry not in long_term:
                    long_term.append(entry)

        if len(long_term) > 100:
            memory["long_term"] = long_term[-100:]

        self._save_json(memory_path, memory)

    def _sync_to_state(self, updates: Dict[str, Any]) -> None:
        state_path = self.webnovel_dir / "state.json"
        state = self._load_json(state_path)
        _deep_update(state, updates)
        self._save_json(state_path, state)

    def build_runtime_context(
        self,
        chapter: int,
        template: str = "plot",
    ) -> Dict[str, Any]:
        master = self.get_master_setting()
        chapter_contract = self.get_chapter_contract(chapter)

        volume_id = 1
        if chapter_contract:
            volume_id = chapter_contract.get("meta", {}).get("volume_id", 1)
        volume_contract = self.get_volume_contract(volume_id)

        recent_commits = []
        for prev_ch in range(max(1, chapter - 3), chapter):
            commit_path = self.story_system_dir / "commits" / f"commit_ch{prev_ch:04d}.json"
            if commit_path.exists():
                recent_commits.append(self._load_json(commit_path))

        state = self._load_json(self.webnovel_dir / "state.json")

        urgent_loops = []
        foreshadowing = (
            state.get("plot_threads", {}).get("foreshadowing", [])
            if isinstance(state.get("plot_threads"), dict)
            else []
        )
        for item in foreshadowing:
            if isinstance(item, dict) and item.get("status") in ("active", "未回收"):
                if item.get("urgency", 0) > 50:
                    urgent_loops.append(item)

        protagonist_state = state.get("protagonist_state", {})

        memory_pack = self._load_json(self.webnovel_dir / "memory_scratchpad.json")

        return {
            "meta": {
                "context_contract_version": "1.0.0",
                "context_weight_stage": "pre_write",
            },
            "story_contract": {
                "master": master,
                "volume": volume_contract,
                "chapter": chapter_contract,
            },
            "runtime_status": {
                "protagonist": protagonist_state,
                "progress": state.get("progress", {}),
                "strand_tracker": state.get("strand_tracker", {}),
            },
            "latest_commit": recent_commits[-1] if recent_commits else {},
            "urgent_loops": urgent_loops[:3],
            "active_rules": master.get("world_rules", [])[:5],
            "memory_pack": {
                "long_term_count": len(memory_pack.get("long_term", [])),
                "recent_patterns": memory_pack.get("patterns", [])[-5:],
            },
            "reader_signal": self._build_reader_signal(chapter),
            "genre_profile": master.get("genre_profile", {}),
            "writing_guidance": self._build_writing_guidance(master, chapter_contract),
            "anti_patterns": master.get("constraints", {}).get("anti_patterns", []),
        }

    def _build_reader_signal(self, chapter: int) -> Dict[str, Any]:
        state = self._load_json(self.webnovel_dir / "state.json")
        signals = state.get("reader_signals", {})
        return {
            "hook_strength_trend": signals.get("hook_trend", []),
            "cool_point_density": signals.get("cool_point_density", "medium"),
            "micro_payoff_rate": signals.get("micro_payoff_rate", 0.0),
            "debt_tracker": signals.get("debt_tracker", []),
        }

    def _build_writing_guidance(
        self,
        master: Dict[str, Any],
        chapter_contract: Dict[str, Any],
    ) -> Dict[str, Any]:
        reasoning = chapter_contract.get("reasoning", {}) if chapter_contract else {}
        tone = master.get("tone_and_style", {})

        return {
            "style_priority": reasoning.get("style_priority", tone.get("style", "")),
            "pacing_strategy": reasoning.get("pacing_strategy", tone.get("pacing_default", "medium")),
            "dialogue_ratio": tone.get("dialogue_ratio", "medium"),
            "description_density": tone.get("description_density", "medium"),
            "anti_patterns_active": reasoning.get("anti_patterns", []),
            "taboos_active": master.get("constraints", {}).get("taboos", []),
        }

    def register_foreshadowing(
        self,
        content: str,
        chapter: int,
        urgency: int = 50,
        expected_payoff: str = "",
        level: str = "chapter",
    ) -> None:
        master = self.get_master_setting()
        registry = master.setdefault("foreshadowing_registry", [])
        registry.append({
            "id": str(uuid.uuid4())[:8],
            "content": content,
            "planted_chapter": chapter,
            "status": "active",
            "urgency": urgency,
            "expected_payoff": expected_payoff,
            "level": level,
            "created_at": _utc_now_iso(),
        })
        master["meta"]["updated_at"] = _utc_now_iso()
        self._save_json(self.story_system_dir / "MASTER_SETTING.json", master)

    def resolve_foreshadowing(self, content: str, chapter: int) -> bool:
        master = self.get_master_setting()
        registry = master.get("foreshadowing_registry", [])
        resolved = False
        for item in registry:
            if item.get("content") == content and item.get("status") == "active":
                item["status"] = "resolved"
                item["resolved_chapter"] = chapter
                resolved = True
        if resolved:
            master["meta"]["updated_at"] = _utc_now_iso()
            self._save_json(self.story_system_dir / "MASTER_SETTING.json", master)
        return resolved

    def get_open_loops(self, max_urgency: bool = False) -> List[Dict[str, Any]]:
        master = self.get_master_setting()
        registry = master.get("foreshadowing_registry", [])
        active = [item for item in registry if item.get("status") == "active"]
        if max_urgency:
            active.sort(key=lambda x: x.get("urgency", 0), reverse=True)
        return active

    def add_world_rule(
        self,
        rule_content: str,
        domain: str = "",
        scope: str = "global",
    ) -> None:
        master = self.get_master_setting()
        rules = master.setdefault("world_rules", [])
        rules.append({
            "id": str(uuid.uuid4())[:8],
            "content": rule_content,
            "domain": domain,
            "scope": scope,
            "established_chapter": 0,
            "created_at": _utc_now_iso(),
        })
        master["meta"]["updated_at"] = _utc_now_iso()
        self._save_json(self.story_system_dir / "MASTER_SETTING.json", master)

    def add_character_to_registry(
        self,
        name: str,
        entity_id: str = "",
        role: str = "supporting",
        tier: str = "core",
        attributes: Optional[Dict[str, Any]] = None,
    ) -> str:
        entity_id = entity_id or _slugify(name)
        master = self.get_master_setting()
        registry = master.setdefault("character_registry", [])

        for char in registry:
            if char.get("entity_id") == entity_id:
                if attributes:
                    char["attributes"].update(attributes)
                char["updated_at"] = _utc_now_iso()
                self._save_json(self.story_system_dir / "MASTER_SETTING.json", master)
                return entity_id

        registry.append({
            "entity_id": entity_id,
            "name": name,
            "role": role,
            "tier": tier,
            "attributes": attributes or {},
            "first_appearance": 0,
            "created_at": _utc_now_iso(),
            "updated_at": _utc_now_iso(),
        })
        master["meta"]["updated_at"] = _utc_now_iso()
        self._save_json(self.story_system_dir / "MASTER_SETTING.json", master)
        return entity_id

    def get_character(self, entity_id: str) -> Optional[Dict[str, Any]]:
        master = self.get_master_setting()
        for char in master.get("character_registry", []):
            if char.get("entity_id") == entity_id:
                return char
        return None

    def build_anti_patterns_from_review(
        self,
        review_issues: List[Dict[str, Any]],
    ) -> List[str]:
        patterns = []
        for issue in review_issues:
            if issue.get("category") == "ai_flavor" and issue.get("severity") in ("high", "critical"):
                desc = issue.get("description", "")
                if desc and desc not in patterns:
                    patterns.append(desc)
        return patterns

    # ============================================================
    # 状态快照与回滚
    # ============================================================

    def create_snapshot(
        self,
        chapter: int,
        label: str = "",
        tags: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """创建状态快照 — 保存当前完整状态"""
        snapshot_id = str(uuid.uuid4())[:12]
        state = self._load_json(self.webnovel_dir / "state.json")
        master = self.get_master_setting()

        snapshot = StateSnapshot(
            snapshot_id=snapshot_id,
            chapter=chapter,
            label=label or f"ch{chapter:04d}_auto",
            state_data=deepcopy(state),
            master_setting_snapshot=deepcopy(master),
            tags=tags or [],
        )

        snap_dir = self.story_system_dir / "snapshots"
        snap_dir.mkdir(parents=True, exist_ok=True)
        self._save_json(snap_dir / f"{snapshot_id}.json", snapshot.to_dict())

        index_path = snap_dir / "index.json"
        index = self._load_json(index_path)
        entries = index.get("entries", [])
        entries.append({
            "snapshot_id": snapshot_id,
            "chapter": chapter,
            "label": snapshot.label,
            "created_at": snapshot.created_at,
            "tags": snapshot.tags,
        })
        if len(entries) > 50:
            entries = entries[-50:]
        index["entries"] = entries
        self._save_json(index_path, index)

        return snapshot.to_dict()

    def restore_snapshot(self, snapshot_id: str) -> Dict[str, Any]:
        """从快照恢复状态 — 完整回滚"""
        snap_dir = self.story_system_dir / "snapshots"
        snap_path = snap_dir / f"{snapshot_id}.json"

        if not snap_path.exists():
            return {"success": False, "error": f"快照 {snapshot_id} 不存在"}

        snap_data = self._load_json(snap_path)

        self._save_json(
            self.webnovel_dir / "state.json",
            snap_data.get("state_data", {}),
        )
        self._save_json(
            self.story_system_dir / "MASTER_SETTING.json",
            snap_data.get("master_setting_snapshot", {}),
        )

        return {
            "success": True,
            "snapshot_id": snapshot_id,
            "chapter": snap_data.get("chapter", 0),
            "label": snap_data.get("label", ""),
            "restored_at": _utc_now_iso(),
        }

    def list_snapshots(
        self,
        limit: int = 20,
        tag: str = "",
    ) -> List[Dict[str, Any]]:
        """列出所有快照"""
        snap_dir = self.story_system_dir / "snapshots"
        index_path = snap_dir / "index.json"
        index = self._load_json(index_path)
        entries = index.get("entries", [])

        if tag:
            entries = [e for e in entries if tag in e.get("tags", [])]

        entries.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        return entries[:limit]

    def delete_snapshot(self, snapshot_id: str) -> Dict[str, Any]:
        """删除指定快照"""
        snap_dir = self.story_system_dir / "snapshots"
        snap_path = snap_dir / f"{snapshot_id}.json"

        if not snap_path.exists():
            return {"success": False, "error": f"快照 {snapshot_id} 不存在"}

        snap_path.unlink()

        index_path = snap_dir / "index.json"
        index = self._load_json(index_path)
        entries = index.get("entries", [])
        index["entries"] = [e for e in entries if e.get("snapshot_id") != snapshot_id]
        self._save_json(index_path, index)

        return {"success": True, "deleted": snapshot_id}

    # ============================================================
    # 书籍锁定
    # ============================================================

    def acquire_lock(
        self,
        locked_by: str = "user",
        reason: str = "",
        ttl_minutes: int = 30,
    ) -> Dict[str, Any]:
        """获取书籍锁 — 防并发编辑"""
        lock_path = self.story_system_dir / "book.lock"

        existing = self._load_json(lock_path)
        if existing:
            existing_lock = BookLock(
                lock_id=existing.get("lock_id", ""),
                locked_by=existing.get("locked_by", ""),
                locked_at=existing.get("locked_at", ""),
                expires_at=existing.get("expires_at", ""),
                lock_reason=existing.get("lock_reason", ""),
                is_active=existing.get("is_active", True),
            )
            if existing_lock.is_active and not existing_lock.is_expired:
                return {
                    "success": False,
                    "error": f"书籍已被 {existing_lock.locked_by} 锁定",
                    "existing_lock": existing_lock.to_dict(),
                }

        from datetime import timedelta
        expires = (datetime.now(timezone.utc) + timedelta(minutes=ttl_minutes)).isoformat(
            timespec="seconds"
        ).replace("+00:00", "Z")

        lock = BookLock(
            lock_id=str(uuid.uuid4())[:12],
            locked_by=locked_by,
            locked_at=_utc_now_iso(),
            expires_at=expires,
            lock_reason=reason,
            is_active=True,
        )

        self._save_json(lock_path, lock.to_dict())
        return {"success": True, "lock": lock.to_dict()}

    def release_lock(self, locked_by: str = "") -> Dict[str, Any]:
        """释放书籍锁"""
        lock_path = self.story_system_dir / "book.lock"

        existing = self._load_json(lock_path)
        if not existing:
            return {"success": True, "message": "无活跃锁"}

        if locked_by and existing.get("locked_by") != locked_by:
            return {
                "success": False,
                "error": f"锁由 {existing.get('locked_by')} 持有，无法释放",
            }

        lock_path.unlink(missing_ok=True)
        return {"success": True, "message": "锁已释放"}

    def check_lock(self) -> Dict[str, Any]:
        """检查书籍锁状态"""
        lock_path = self.story_system_dir / "book.lock"
        existing = self._load_json(lock_path)

        if not existing:
            return {"locked": False, "message": "无活跃锁"}

        lock = BookLock(
            lock_id=existing.get("lock_id", ""),
            locked_by=existing.get("locked_by", ""),
            locked_at=existing.get("locked_at", ""),
            expires_at=existing.get("expires_at", ""),
            lock_reason=existing.get("lock_reason", ""),
            is_active=existing.get("is_active", True),
        )

        if lock.is_expired:
            return {"locked": False, "message": "锁已过期", "expired_lock": lock.to_dict()}

        return {"locked": lock.is_active, "lock": lock.to_dict()}

    def force_release_lock(self) -> Dict[str, Any]:
        """强制释放锁（管理员操作）"""
        lock_path = self.story_system_dir / "book.lock"
        lock_path.unlink(missing_ok=True)
        return {"success": True, "message": "锁已强制释放"}

    # ============================================================
    # 控制文档
    # ============================================================

    def get_control_document(self) -> Dict[str, Any]:
        """获取控制文档 — 项目元信息"""
        ctrl_path = self.story_system_dir / "control.json"
        ctrl = self._load_json(ctrl_path)

        if not ctrl:
            ctrl = {
                "project_name": "",
                "created_at": _utc_now_iso(),
                "updated_at": _utc_now_iso(),
                "current_chapter": 0,
                "current_volume": 1,
                "total_words": 0,
                "status": "drafting",
                "chapter_index": {},
                "config": {
                    "auto_snapshot": True,
                    "snapshot_interval_chapters": 5,
                    "lock_ttl_minutes": 30,
                },
            }
            self._save_json(ctrl_path, ctrl)

        return ctrl

    def update_control_document(self, updates: Dict[str, Any]) -> Dict[str, Any]:
        """更新控制文档"""
        ctrl = self.get_control_document()
        _deep_update(ctrl, updates)
        ctrl["updated_at"] = _utc_now_iso()
        self._save_json(self.story_system_dir / "control.json", ctrl)
        return ctrl

    def update_chapter_index(
        self,
        chapter: int,
        info: Dict[str, Any],
    ) -> Dict[str, Any]:
        """更新章节索引"""
        ctrl = self.get_control_document()
        chapter_index = ctrl.setdefault("chapter_index", {})
        chapter_index[str(chapter)] = {
            **chapter_index.get(str(chapter), {}),
            **info,
            "indexed_at": _utc_now_iso(),
        }
        ctrl["updated_at"] = _utc_now_iso()
        self._save_json(self.story_system_dir / "control.json", ctrl)
        return ctrl

    def auto_snapshot_if_needed(self, chapter: int) -> Optional[Dict[str, Any]]:
        """根据配置自动创建快照"""
        ctrl = self.get_control_document()
        config = ctrl.get("config", {})

        if not config.get("auto_snapshot", True):
            return None

        interval = config.get("snapshot_interval_chapters", 5)
        if chapter % interval == 0:
            return self.create_snapshot(
                chapter=chapter,
                label=f"auto_ch{chapter:04d}",
                tags=["auto", f"ch{chapter}"],
            )

        return None

    def get_project_health(self) -> Dict[str, Any]:
        master = self.get_master_setting()
        state = self._load_json(self.webnovel_dir / "state.json")

        open_loops = self.get_open_loops()
        urgent_loops = [l for l in open_loops if l.get("urgency", 0) > 70]

        commits_dir = self.story_system_dir / "commits"
        commit_count = len(list(commits_dir.glob("commit_ch*.json"))) if commits_dir.exists() else 0

        return {
            "master_setting_exists": bool(master),
            "open_loops_count": len(open_loops),
            "urgent_loops_count": len(urgent_loops),
            "total_commits": commit_count,
            "current_chapter": state.get("progress", {}).get("current_chapter", 0),
            "total_words": state.get("progress", {}).get("total_words", 0),
            "character_count": len(master.get("character_registry", [])),
            "world_rules_count": len(master.get("world_rules", [])),
            "health_status": "critical" if urgent_loops else "healthy",
        }


def _deep_update(target: Dict, source: Dict) -> None:
    for key, value in source.items():
        if key in target and isinstance(target[key], dict) and isinstance(value, dict):
            _deep_update(target[key], value)
        else:
            target[key] = deepcopy(value)


def _set_nested(d: Dict, key: str, value: Any) -> None:
    parts = key.split(".")
    for part in parts[:-1]:
        d = d.setdefault(part, {})
    d[parts[-1]] = value


def _slugify(text: str) -> str:
    text = re.sub(r"[^\w\u4e00-\u9fff]", "_", text.lower())
    text = re.sub(r"_+", "_", text).strip("_")
    return text or "unknown"