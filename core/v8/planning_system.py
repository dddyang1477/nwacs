#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Planning System — NWACS 升级规划系统

核心功能:
1. 卷节拍表 — 卷级结构规划（三幕式/英雄之旅/网文节奏）
2. 时间线管理 — 故事时间线追踪与倒计时
3. 结构化章纲 — CBN/CPNs/CEN 三级节点体系
4. 章纲解析 — 从大纲文件自动提取结构化章纲
5. 执行指令 — 每章的写作执行指令生成
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


@dataclass
class VolumeBeatSheet:
    volume_id: int
    volume_name: str
    chapter_start: int
    chapter_end: int
    act_structure: str = "three_act"
    beats: List[Dict[str, Any]] = field(default_factory=list)
    climax_chapter: int = 0
    midpoint_chapter: int = 0
    created_at: str = field(default_factory=_utc_now_iso)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "volume_id": self.volume_id,
            "volume_name": self.volume_name,
            "chapter_start": self.chapter_start,
            "chapter_end": self.chapter_end,
            "act_structure": self.act_structure,
            "beats": self.beats,
            "climax_chapter": self.climax_chapter,
            "midpoint_chapter": self.midpoint_chapter,
            "created_at": self.created_at,
        }


@dataclass
class ChapterOutline:
    chapter: int
    title: str = ""
    goal: str = ""
    cbn: str = ""
    cpns: List[str] = field(default_factory=list)
    cen: str = ""
    must_cover_nodes: List[str] = field(default_factory=list)
    forbidden_zones: List[str] = field(default_factory=list)
    time_anchor: str = ""
    chapter_span: str = ""
    countdown: str = ""
    hook_type: str = ""
    hook_strength: str = ""
    key_entities: List[str] = field(default_factory=list)
    strand: str = ""
    antagonist_tier: str = ""
    obstacles: List[str] = field(default_factory=list)
    cost: str = ""
    chapter_end_open_question: str = ""
    source: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "chapter": self.chapter,
            "title": self.title,
            "goal": self.goal,
            "cbn": self.cbn,
            "cpns": self.cpns,
            "cen": self.cen,
            "must_cover_nodes": self.must_cover_nodes,
            "forbidden_zones": self.forbidden_zones,
            "time_anchor": self.time_anchor,
            "chapter_span": self.chapter_span,
            "countdown": self.countdown,
            "hook_type": self.hook_type,
            "hook_strength": self.hook_strength,
            "key_entities": self.key_entities,
            "strand": self.strand,
            "antagonist_tier": self.antagonist_tier,
            "obstacles": self.obstacles,
            "cost": self.cost,
            "chapter_end_open_question": self.chapter_end_open_question,
            "source": self.source,
        }


class PlanningSystem:
    """升级规划系统 — 卷节拍表/时间线/结构化章纲"""

    BEAT_TEMPLATES = {
        "three_act": [
            {"name": "开场钩子", "position": 0.0, "desc": "强力开场，抓住读者注意力"},
            {"name": "日常世界", "position": 0.05, "desc": "展示主角的日常状态"},
            {"name": "激励事件", "position": 0.12, "desc": "打破日常的事件，推动主角行动"},
            {"name": "第一幕转折", "position": 0.25, "desc": "主角做出不可逆的决定，进入新世界"},
            {"name": "探索与试炼", "position": 0.35, "desc": "在新世界中学习规则，结交盟友"},
            {"name": "中点转折", "position": 0.50, "desc": "重大事件改变故事走向，赌注升级"},
            {"name": "危机升级", "position": 0.62, "desc": "情况恶化，盟友背叛或重大损失"},
            {"name": "至暗时刻", "position": 0.75, "desc": "主角最低谷，一切看似失败"},
            {"name": "觉醒与反击", "position": 0.82, "desc": "主角获得新认知/力量，开始反击"},
            {"name": "高潮对决", "position": 0.90, "desc": "最终对决，核心冲突解决"},
            {"name": "结局与余韵", "position": 0.97, "desc": "冲突解决后的新平衡，埋下续集伏笔"},
        ],
        "webnovel_rhythm": [
            {"name": "黄金开篇", "position": 0.0, "desc": "前三章：钩子→世界→冲突"},
            {"name": "首次爽点", "position": 0.08, "desc": "第3-5章：第一次打脸/突破"},
            {"name": "世界观展开", "position": 0.15, "desc": "通过冒险展示世界观规则"},
            {"name": "首次大高潮", "position": 0.25, "desc": "第一卷高潮：击败第一个重要对手"},
            {"name": "能力升级期", "position": 0.35, "desc": "获得新能力/金手指进化"},
            {"name": "势力冲突", "position": 0.50, "desc": "卷入更大势力纷争，赌注升级"},
            {"name": "重大挫折", "position": 0.62, "desc": "遭遇重大失败，失去重要之物"},
            {"name": "绝境突破", "position": 0.75, "desc": "在绝境中突破，实力飞跃"},
            {"name": "身份揭露", "position": 0.85, "desc": "重要身份/秘密被揭露"},
            {"name": "卷末大战", "position": 0.95, "desc": "本卷最终大战，核心冲突阶段性解决"},
        ],
    }

    CHAPTER_HEADING_RE = re.compile(
        r"^(#{1,6})\s*第\s*([0-9零〇一二两三四五六七八九十]+)\s*章\b.*$",
        re.MULTILINE,
    )

    CHINESE_NUMERALS = {
        "零": 0, "〇": 0, "一": 1, "二": 2, "两": 2,
        "三": 3, "四": 4, "五": 5, "六": 6,
        "七": 7, "八": 8, "九": 9,
    }

    DIRECTIVE_FIELD_MAP = {
        "目标": "goal", "本章目标": "goal", "章目标": "goal",
        "阻力": "obstacles", "障碍": "obstacles",
        "代价": "cost",
        "时间锚点": "time_anchor", "时间": "time_anchor",
        "章内跨度": "chapter_span", "章节跨度": "chapter_span",
        "倒计时状态": "countdown", "倒计时": "countdown",
        "cbn": "cbn", "CBN": "cbn",
        "cpns": "cpns", "CPNs": "cpns",
        "cen": "cen", "CEN": "cen",
        "必须覆盖节点": "must_cover_nodes",
        "本章禁区": "forbidden_zones",
        "章末未闭合问题": "chapter_end_open_question", "章末问题": "chapter_end_open_question",
        "钩子类型": "hook_type", "钩子强度": "hook_strength",
        "关键实体": "key_entities", "涉及实体": "key_entities",
        "strand": "strand",
        "反派层级": "antagonist_tier",
    }

    DIRECTIVE_LIST_FIELDS = {"cpns", "must_cover_nodes", "forbidden_zones", "key_entities", "obstacles"}

    def __init__(self, project_root: str = ""):
        self.project_root = Path(project_root) if project_root else Path(".")
        self.planning_dir = self.project_root / ".webnovel" / "planning"
        self.planning_dir.mkdir(parents=True, exist_ok=True)

    def create_volume_beat_sheet(
        self,
        volume_id: int,
        volume_name: str,
        chapter_start: int,
        chapter_end: int,
        act_structure: str = "three_act",
    ) -> VolumeBeatSheet:
        template = self.BEAT_TEMPLATES.get(act_structure, self.BEAT_TEMPLATES["three_act"])
        total_chapters = chapter_end - chapter_start + 1

        beats = []
        for beat_template in template:
            chapter_offset = int(beat_template["position"] * total_chapters)
            beat_chapter = chapter_start + chapter_offset
            beats.append({
                "name": beat_template["name"],
                "chapter": min(beat_chapter, chapter_end),
                "position": beat_template["position"],
                "desc": beat_template["desc"],
                "status": "pending",
            })

        midpoint_chapter = chapter_start + int(0.5 * total_chapters)
        climax_chapter = chapter_start + int(0.9 * total_chapters)

        beat_sheet = VolumeBeatSheet(
            volume_id=volume_id,
            volume_name=volume_name,
            chapter_start=chapter_start,
            chapter_end=chapter_end,
            act_structure=act_structure,
            beats=beats,
            climax_chapter=min(climax_chapter, chapter_end),
            midpoint_chapter=min(midpoint_chapter, chapter_end),
        )

        path = self.planning_dir / f"volume_{volume_id:03d}_beats.json"
        tmp_path = path.with_suffix(path.suffix + ".tmp")
        tmp_path.write_text(
            json.dumps(beat_sheet.to_dict(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        tmp_path.replace(path)

        return beat_sheet

    def get_volume_beat_sheet(self, volume_id: int) -> Optional[VolumeBeatSheet]:
        path = self.planning_dir / f"volume_{volume_id:03d}_beats.json"
        if not path.exists():
            return None
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            return VolumeBeatSheet(
                volume_id=data.get("volume_id", volume_id),
                volume_name=data.get("volume_name", ""),
                chapter_start=data.get("chapter_start", 0),
                chapter_end=data.get("chapter_end", 0),
                act_structure=data.get("act_structure", "three_act"),
                beats=data.get("beats", []),
                climax_chapter=data.get("climax_chapter", 0),
                midpoint_chapter=data.get("midpoint_chapter", 0),
                created_at=data.get("created_at", ""),
            )
        except (json.JSONDecodeError, KeyError):
            return None

    def get_beat_for_chapter(self, chapter: int) -> Optional[Dict[str, Any]]:
        for vol_file in sorted(self.planning_dir.glob("volume_*_beats.json")):
            try:
                data = json.loads(vol_file.read_text(encoding="utf-8"))
                if data.get("chapter_start", 0) <= chapter <= data.get("chapter_end", 0):
                    for beat in data.get("beats", []):
                        if beat.get("chapter") == chapter:
                            return beat
                    for beat in data.get("beats", []):
                        if beat.get("chapter", 0) <= chapter:
                            closest = beat
                    return closest if 'closest' in dir() else None
            except (json.JSONDecodeError, KeyError):
                continue
        return None

    def parse_chapter_outline(
        self,
        outline_text: str,
        chapter: int,
    ) -> ChapterOutline:
        text = str(outline_text or "")
        outline = ChapterOutline(chapter=chapter, source="parsed")

        if not text or text.startswith("⚠️"):
            return outline

        current_field = ""
        for raw_line in text.splitlines():
            stripped = raw_line.strip()
            if not stripped:
                current_field = ""
                continue

            if self.CHAPTER_HEADING_RE.match(stripped):
                current_field = ""
                continue

            cleaned = self._clean_line(stripped)
            matched_field = ""
            matched_value = ""

            for label, field in self.DIRECTIVE_FIELD_MAP.items():
                match = re.match(rf"^{re.escape(label)}\s*[：:]\s*(.*)$", cleaned, re.IGNORECASE)
                if match:
                    matched_field = field
                    matched_value = match.group(1).strip()
                    break

            if matched_field:
                current_field = matched_field
                self._set_outline_field(outline, matched_field, matched_value)
                continue

            if current_field:
                self._set_outline_field(outline, current_field, cleaned)

        return outline

    def _clean_line(self, line: str) -> str:
        text = str(line or "").strip()
        text = re.sub(r"^[\-\*•]+\s*", "", text)
        text = re.sub(r"^\d+[\.、]\s*", "", text)
        return text.strip()

    def _set_outline_field(self, outline: ChapterOutline, field: str, value: str) -> None:
        value = self._clean_line(value)
        if not value:
            return

        if field in self.DIRECTIVE_LIST_FIELDS:
            current = getattr(outline, field, [])
            if not isinstance(current, list):
                current = []
            split_values = [part.strip() for part in re.split(r"[、,，；;|]+", value) if part.strip()]
            for item in split_values or [value]:
                if item not in current:
                    current.append(item)
            setattr(outline, field, current)
            return

        if hasattr(outline, field) and not getattr(outline, field):
            setattr(outline, field, value)

    def build_execution_directive(
        self,
        outline: ChapterOutline,
        beat: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        directive: Dict[str, Any] = {
            "chapter": outline.chapter,
            "title": outline.title,
            "goal": outline.goal,
            "time_anchor": outline.time_anchor,
            "chapter_span": outline.chapter_span,
            "countdown": outline.countdown,
            "plot_structure": {
                "CBN": outline.cbn,
                "CPNs": outline.cpns,
                "CEN": outline.cen,
                "must_cover_nodes": outline.must_cover_nodes,
                "forbidden_zones": outline.forbidden_zones,
            },
            "hook": {
                "type": outline.hook_type,
                "strength": outline.hook_strength,
                "end_question": outline.chapter_end_open_question,
            },
            "entities": {
                "key": outline.key_entities,
                "strand": outline.strand,
                "antagonist_tier": outline.antagonist_tier,
            },
            "constraints": {
                "obstacles": outline.obstacles,
                "cost": outline.cost,
            },
        }

        if beat:
            directive["beat_context"] = {
                "beat_name": beat.get("name", ""),
                "beat_desc": beat.get("desc", ""),
                "beat_status": beat.get("status", "pending"),
            }

        return directive

    def build_chapter_context_payload(
        self,
        chapter: int,
        outline_text: str = "",
        previous_summaries: Optional[List[str]] = None,
        state_summary: str = "",
    ) -> Dict[str, Any]:
        outline = self.parse_chapter_outline(outline_text, chapter)
        beat = self.get_beat_for_chapter(chapter)
        directive = self.build_execution_directive(outline, beat)

        return {
            "chapter": chapter,
            "outline": outline.to_dict(),
            "beat": beat,
            "execution_directive": directive,
            "previous_summaries": previous_summaries or [],
            "state_summary": state_summary,
            "generated_at": _utc_now_iso(),
        }

    def create_timeline_entry(
        self,
        chapter: int,
        event: str,
        time_point: str = "",
        location: str = "",
        characters: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        timeline_path = self.planning_dir / "timeline.json"
        timeline: Dict[str, Any] = {"entries": []}

        if timeline_path.exists():
            try:
                timeline = json.loads(timeline_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                pass

        entry = {
            "chapter": chapter,
            "event": event,
            "time_point": time_point,
            "location": location,
            "characters": characters or [],
            "recorded_at": _utc_now_iso(),
        }

        entries = timeline.get("entries", [])
        entries.append(entry)
        entries.sort(key=lambda e: e.get("chapter", 0))
        timeline["entries"] = entries
        timeline["updated_at"] = _utc_now_iso()

        tmp_path = timeline_path.with_suffix(timeline_path.suffix + ".tmp")
        tmp_path.write_text(json.dumps(timeline, ensure_ascii=False, indent=2), encoding="utf-8")
        tmp_path.replace(timeline_path)

        return entry

    def get_timeline(self, start_chapter: int = 0, end_chapter: int = 9999) -> List[Dict[str, Any]]:
        timeline_path = self.planning_dir / "timeline.json"
        if not timeline_path.exists():
            return []

        try:
            timeline = json.loads(timeline_path.read_text(encoding="utf-8"))
            entries = timeline.get("entries", [])
            return [
                e for e in entries
                if start_chapter <= e.get("chapter", 0) <= end_chapter
            ]
        except (json.JSONDecodeError, KeyError):
            return []

    def get_chapter_countdown(self, chapter: int) -> Optional[str]:
        outline_path = self.planning_dir / f"chapter_{chapter:04d}_outline.json"
        if not outline_path.exists():
            return None
        try:
            data = json.loads(outline_path.read_text(encoding="utf-8"))
            return data.get("countdown")
        except (json.JSONDecodeError, KeyError):
            return None

    def save_chapter_outline(self, outline: ChapterOutline) -> None:
        path = self.planning_dir / f"chapter_{outline.chapter:04d}_outline.json"
        tmp_path = path.with_suffix(path.suffix + ".tmp")
        tmp_path.write_text(
            json.dumps(outline.to_dict(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        tmp_path.replace(path)

    def load_chapter_outline(self, chapter: int) -> Optional[ChapterOutline]:
        path = self.planning_dir / f"chapter_{chapter:04d}_outline.json"
        if not path.exists():
            return None
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            return ChapterOutline(
                chapter=data.get("chapter", chapter),
                title=data.get("title", ""),
                goal=data.get("goal", ""),
                cbn=data.get("cbn", ""),
                cpns=data.get("cpns", []),
                cen=data.get("cen", ""),
                must_cover_nodes=data.get("must_cover_nodes", []),
                forbidden_zones=data.get("forbidden_zones", []),
                time_anchor=data.get("time_anchor", ""),
                chapter_span=data.get("chapter_span", ""),
                countdown=data.get("countdown", ""),
                hook_type=data.get("hook_type", ""),
                hook_strength=data.get("hook_strength", ""),
                key_entities=data.get("key_entities", []),
                strand=data.get("strand", ""),
                antagonist_tier=data.get("antagonist_tier", ""),
                obstacles=data.get("obstacles", []),
                cost=data.get("cost", ""),
                chapter_end_open_question=data.get("chapter_end_open_question", ""),
                source=data.get("source", ""),
            )
        except (json.JSONDecodeError, KeyError):
            return None