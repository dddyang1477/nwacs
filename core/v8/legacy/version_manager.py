#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 版本管理与历史回溯系统 - VersionManager v2.0

核心能力：
1. 章节快照 - 每次保存自动创建版本快照
2. 版本对比 - 任意两个版本间diff对比（文本/HTML可视化）
3. 回滚恢复 - 一键回滚到任意历史版本
4. 分支管理 - 支持多分支并行创作
5. 变更日志 - 自动生成修改记录
6. 导出归档 - 完整版本历史打包导出
7. 三路合并 - 分支间智能合并
8. 自动保存 - 可配置间隔的自动保存
9. 版本图 - 版本树可视化数据
10. 搜索快照 - 按内容/标签搜索历史版本
"""

import json
import os
import re
import hashlib
import shutil
import difflib
import uuid
import threading
import time
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum


class SnapshotType(Enum):
    AUTO = "自动保存"
    MANUAL = "手动保存"
    MILESTONE = "里程碑"
    BRANCH = "分支点"
    MERGE = "合并点"
    ROLLBACK = "回滚点"


@dataclass
class VersionSnapshot:
    snapshot_id: str
    chapter: int
    content: str
    word_count: int
    snapshot_type: SnapshotType
    timestamp: str
    message: str = ""
    tags: List[str] = field(default_factory=list)
    parent_snapshot: str = ""
    branch_name: str = "main"
    content_hash: str = ""
    merge_parents: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "snapshot_id": self.snapshot_id,
            "chapter": self.chapter,
            "content": self.content,
            "word_count": self.word_count,
            "snapshot_type": self.snapshot_type.value,
            "timestamp": self.timestamp,
            "message": self.message,
            "tags": self.tags,
            "parent_snapshot": self.parent_snapshot,
            "branch_name": self.branch_name,
            "content_hash": self.content_hash,
            "merge_parents": self.merge_parents,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "VersionSnapshot":
        type_map = {t.value: t for t in SnapshotType}
        return cls(
            snapshot_id=data["snapshot_id"],
            chapter=data["chapter"],
            content=data["content"],
            word_count=data["word_count"],
            snapshot_type=type_map.get(data["snapshot_type"], SnapshotType.AUTO),
            timestamp=data["timestamp"],
            message=data.get("message", ""),
            tags=data.get("tags", []),
            parent_snapshot=data.get("parent_snapshot", ""),
            branch_name=data.get("branch_name", "main"),
            content_hash=data.get("content_hash", ""),
            merge_parents=data.get("merge_parents", []),
        )


@dataclass
class DiffResult:
    added_lines: int
    removed_lines: int
    modified_lines: int
    total_changes: int
    change_ratio: float
    unified_diff: str
    html_diff: str = ""
    word_diff: List[Dict] = field(default_factory=list)


@dataclass
class AutoSaveConfig:
    enabled: bool = True
    interval_seconds: int = 300
    max_auto_snapshots: int = 50
    chapters_to_watch: List[int] = field(default_factory=list)


class VersionManager:
    """版本管理与历史回溯 v2.0"""

    def __init__(self, novel_title: str = "未命名作品", storage_dir: str = None):
        self.novel_title = novel_title
        if storage_dir is None:
            storage_dir = os.path.join(os.path.dirname(__file__), "..", "version_storage")
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)

        self.snapshots: Dict[str, VersionSnapshot] = {}
        self.current_branch = "main"
        self.branches: Dict[str, str] = {}
        self.auto_save_config = AutoSaveConfig()
        self._auto_save_timer: Optional[threading.Timer] = None
        self._dirty_chapters: Dict[int, str] = {}
        self._load()

    def _get_filepath(self) -> str:
        safe_name = re.sub(r'[<>:"/\\|?*]', '_', self.novel_title)
        return os.path.join(self.storage_dir, f"{safe_name}_versions.json")

    def _get_archive_dir(self) -> str:
        safe_name = re.sub(r'[<>:"/\\|?*]', '_', self.novel_title)
        return os.path.join(self.storage_dir, f"{safe_name}_archive")

    def _get_config_path(self) -> str:
        safe_name = re.sub(r'[<>:"/\\|?*]', '_', self.novel_title)
        return os.path.join(self.storage_dir, f"{safe_name}_config.json")

    def _load(self):
        filepath = self._get_filepath()
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.current_branch = data.get("current_branch", "main")
            self.branches = data.get("branches", {"main": ""})
            for snap_data in data.get("snapshots", []):
                snapshot = VersionSnapshot.from_dict(snap_data)
                self.snapshots[snapshot.snapshot_id] = snapshot

        config_path = self._get_config_path()
        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                config_data = json.load(f)
            self.auto_save_config = AutoSaveConfig(
                enabled=config_data.get("auto_save_enabled", True),
                interval_seconds=config_data.get("auto_save_interval", 300),
                max_auto_snapshots=config_data.get("max_auto_snapshots", 50),
                chapters_to_watch=config_data.get("chapters_to_watch", []),
            )

    def save(self):
        data = {
            "novel_title": self.novel_title,
            "current_branch": self.current_branch,
            "branches": self.branches,
            "updated_at": datetime.now().isoformat(),
            "total_snapshots": len(self.snapshots),
            "snapshots": [s.to_dict() for s in self.snapshots.values()],
        }
        with open(self._get_filepath(), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        with open(self._get_config_path(), "w", encoding="utf-8") as f:
            json.dump({
                "auto_save_enabled": self.auto_save_config.enabled,
                "auto_save_interval": self.auto_save_config.interval_seconds,
                "max_auto_snapshots": self.auto_save_config.max_auto_snapshots,
                "chapters_to_watch": self.auto_save_config.chapters_to_watch,
            }, f, ensure_ascii=False, indent=2)

    def _compute_hash(self, content: str) -> str:
        return hashlib.md5(content.encode("utf-8")).hexdigest()[:12]

    def create_snapshot(self, chapter: int, content: str,
                        snapshot_type: SnapshotType = SnapshotType.AUTO,
                        message: str = "", tags: List[str] = None,
                        parent_id: str = "") -> str:
        snapshot_id = str(uuid.uuid4())[:12]
        word_count = len(content)
        content_hash = self._compute_hash(content)

        if not parent_id and self.branches.get(self.current_branch):
            parent_id = self.branches[self.current_branch]

        snapshot = VersionSnapshot(
            snapshot_id=snapshot_id,
            chapter=chapter,
            content=content,
            word_count=word_count,
            snapshot_type=snapshot_type,
            timestamp=datetime.now().isoformat(),
            message=message,
            tags=tags or [],
            parent_snapshot=parent_id,
            branch_name=self.current_branch,
            content_hash=content_hash,
        )

        self.snapshots[snapshot_id] = snapshot
        self.branches[self.current_branch] = snapshot_id
        self._prune_auto_snapshots()
        self.save()
        return snapshot_id

    def _prune_auto_snapshots(self):
        auto_snaps = [
            (sid, s) for sid, s in self.snapshots.items()
            if s.snapshot_type == SnapshotType.AUTO
            and s.branch_name == self.current_branch
        ]
        auto_snaps.sort(key=lambda x: x[1].timestamp)

        excess = len(auto_snaps) - self.auto_save_config.max_auto_snapshots
        for sid, _ in auto_snaps[:excess]:
            del self.snapshots[sid]

    def get_snapshot(self, snapshot_id: str) -> Optional[VersionSnapshot]:
        return self.snapshots.get(snapshot_id)

    def get_chapter_history(self, chapter: int) -> List[VersionSnapshot]:
        history = [
            s for s in self.snapshots.values()
            if s.chapter == chapter and s.branch_name == self.current_branch
        ]
        history.sort(key=lambda s: s.timestamp)
        return history

    def get_latest(self, chapter: int = None) -> Optional[VersionSnapshot]:
        candidates = list(self.snapshots.values())
        if chapter is not None:
            candidates = [s for s in candidates if s.chapter == chapter]
        candidates = [s for s in candidates if s.branch_name == self.current_branch]
        if not candidates:
            return None
        return max(candidates, key=lambda s: s.timestamp)

    def diff(self, snapshot_a: str, snapshot_b: str) -> Optional[DiffResult]:
        snap_a = self.snapshots.get(snapshot_a)
        snap_b = self.snapshots.get(snapshot_b)
        if not snap_a or not snap_b:
            return None

        lines_a = snap_a.content.splitlines(keepends=True)
        lines_b = snap_b.content.splitlines(keepends=True)

        differ = difflib.unified_diff(
            lines_a, lines_b,
            fromfile=f"版本{snapshot_a[:8]}",
            tofile=f"版本{snapshot_b[:8]}",
            lineterm="",
        )
        unified = "\n".join(differ)

        matcher = difflib.SequenceMatcher(None, lines_a, lines_b)
        added = removed = modified = 0
        word_changes = []

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == "insert":
                added += j2 - j1
                for j in range(j1, j2):
                    word_changes.append({"type": "added", "line": j, "content": lines_b[j].strip()})
            elif tag == "delete":
                removed += i2 - i1
                for i in range(i1, i2):
                    word_changes.append({"type": "removed", "line": i, "content": lines_a[i].strip()})
            elif tag == "replace":
                modified += max(i2 - i1, j2 - j1)
                for i in range(i1, i2):
                    word_changes.append({"type": "removed", "line": i, "content": lines_a[i].strip()})
                for j in range(j1, j2):
                    word_changes.append({"type": "added", "line": j, "content": lines_b[j].strip()})

        total = added + removed + modified
        max_lines = max(len(lines_a), len(lines_b), 1)
        ratio = total / max_lines

        html_diff = self._generate_html_diff(lines_a, lines_b, snap_a, snap_b)

        return DiffResult(
            added_lines=added,
            removed_lines=removed,
            modified_lines=modified,
            total_changes=total,
            change_ratio=ratio,
            unified_diff=unified,
            html_diff=html_diff,
            word_diff=word_changes,
        )

    def _generate_html_diff(self, lines_a: List[str], lines_b: List[str],
                            snap_a: VersionSnapshot, snap_b: VersionSnapshot) -> str:
        differ = difflib.HtmlDiff(tabsize=2, wrapcolumn=80)
        return differ.make_table(
            lines_a, lines_b,
            fromdesc=f"版本 {snap_a.snapshot_id[:8]} ({snap_a.timestamp})",
            todesc=f"版本 {snap_b.snapshot_id[:8]} ({snap_b.timestamp})",
            context=True, numlines=3,
        )

    def three_way_merge(self, base_id: str, ours_id: str,
                        theirs_id: str) -> Tuple[Optional[str], List[str]]:
        """三路合并"""
        base = self.snapshots.get(base_id)
        ours = self.snapshots.get(ours_id)
        theirs = self.snapshots.get(theirs_id)

        if not base or not ours or not theirs:
            return None, ["无法找到所有版本"]

        base_lines = base.content.splitlines(keepends=True)
        ours_lines = ours.content.splitlines(keepends=True)
        theirs_lines = theirs.content.splitlines(keepends=True)

        matcher = difflib.SequenceMatcher(None, base_lines, ours_lines)
        ours_edits = list(matcher.get_opcodes())

        matcher2 = difflib.SequenceMatcher(None, base_lines, theirs_lines)
        theirs_edits = list(matcher2.get_opcodes())

        merged_lines = list(base_lines)
        conflicts = []

        for tag, i1, i2, j1, j2 in theirs_edits:
            conflict = False
            for otag, oi1, oi2, oj1, oj2 in ours_edits:
                if max(i1, oi1) < min(i2, oi2):
                    if tag != otag or j1 != oj1 or j2 != oj2:
                        conflict = True
                        conflicts.append(
                            f"冲突: 行{i1}-{i2}, 我们的修改与他们的修改重叠"
                        )
                        break

            if not conflict:
                if tag == "insert":
                    for j in range(j1, j2):
                        merged_lines.insert(i1 + (j - j1), theirs_lines[j])
                elif tag == "delete":
                    for i in range(i1, i2):
                        if i < len(merged_lines):
                            merged_lines[i] = ""
                elif tag == "replace":
                    for i in range(i1, i2):
                        if i < len(merged_lines):
                            merged_lines[i] = ""
                    for j in range(j1, j2):
                        merged_lines.insert(i1 + (j - j1), theirs_lines[j])

        merged_content = "".join(merged_lines)

        if conflicts:
            merged_content = (
                "⚠️ 合并存在冲突，以下为自动合并结果（冲突部分保留了我们的版本）:\n\n"
                + merged_content
            )

        return merged_content, conflicts

    def rollback(self, snapshot_id: str) -> Optional[str]:
        target = self.snapshots.get(snapshot_id)
        if not target:
            return None

        return self.create_snapshot(
            chapter=target.chapter,
            content=target.content,
            snapshot_type=SnapshotType.ROLLBACK,
            message=f"回滚到版本 {snapshot_id[:8]}",
            tags=["rollback"],
            parent_id=snapshot_id,
        )

    def create_branch(self, branch_name: str, from_snapshot: str = "") -> bool:
        if branch_name in self.branches:
            return False
        if not from_snapshot:
            from_snapshot = self.branches.get(self.current_branch, "")

        if from_snapshot and from_snapshot in self.snapshots:
            snap = self.snapshots[from_snapshot]
            branch_point_id = self.create_snapshot(
                chapter=snap.chapter,
                content=snap.content,
                snapshot_type=SnapshotType.BRANCH,
                message=f"分支点: {branch_name}",
                tags=["branch", branch_name],
            )
            self.branches[branch_name] = branch_point_id
        else:
            self.branches[branch_name] = ""

        self.save()
        return True

    def switch_branch(self, branch_name: str) -> bool:
        if branch_name not in self.branches:
            return False
        self.current_branch = branch_name
        self.save()
        return True

    def merge_branch(self, source_branch: str, target_branch: str = "main") -> bool:
        if source_branch not in self.branches or target_branch not in self.branches:
            return False

        source_tip = self.branches[source_branch]
        target_tip = self.branches[target_branch]

        if source_tip and source_tip in self.snapshots:
            snapshot = self.snapshots[source_tip]
            merge_snap = VersionSnapshot(
                snapshot_id=str(uuid.uuid4())[:12],
                chapter=snapshot.chapter,
                content=snapshot.content,
                word_count=snapshot.word_count,
                snapshot_type=SnapshotType.MERGE,
                timestamp=datetime.now().isoformat(),
                message=f"合并分支 {source_branch} → {target_branch}",
                tags=["merge", source_branch],
                branch_name=target_branch,
                parent_snapshot=target_tip,
                merge_parents=[source_tip, target_tip],
                content_hash=self._compute_hash(snapshot.content),
            )
            self.snapshots[merge_snap.snapshot_id] = merge_snap
            self.branches[target_branch] = merge_snap.snapshot_id
            self.save()

        return True

    def get_version_graph(self) -> Dict:
        """获取版本图数据（用于可视化）"""
        nodes = []
        edges = []

        for snap in self.snapshots.values():
            node_type = "milestone" if snap.snapshot_type == SnapshotType.MILESTONE else (
                "branch" if snap.snapshot_type == SnapshotType.BRANCH else (
                    "merge" if snap.snapshot_type == SnapshotType.MERGE else "normal"
                )
            )

            nodes.append({
                "id": snap.snapshot_id[:8],
                "label": f"Ch{snap.chapter} {snap.snapshot_type.value}",
                "type": node_type,
                "branch": snap.branch_name,
                "timestamp": snap.timestamp,
                "word_count": snap.word_count,
                "message": snap.message,
            })

            if snap.parent_snapshot and snap.parent_snapshot in self.snapshots:
                edges.append({
                    "source": snap.parent_snapshot[:8],
                    "target": snap.snapshot_id[:8],
                    "type": "parent",
                })

            for mp in snap.merge_parents:
                if mp in self.snapshots:
                    edges.append({
                        "source": mp[:8],
                        "target": snap.snapshot_id[:8],
                        "type": "merge",
                    })

        return {"nodes": nodes, "edges": edges}

    def search_snapshots(self, query: str, branch: str = None,
                         chapter: int = None, max_results: int = 20) -> List[VersionSnapshot]:
        """搜索快照"""
        results = []
        query_lower = query.lower()

        for snap in self.snapshots.values():
            if branch and snap.branch_name != branch:
                continue
            if chapter is not None and snap.chapter != chapter:
                continue

            score = 0
            if query_lower in snap.content.lower():
                score += 5
            if query_lower in snap.message.lower():
                score += 3
            for tag in snap.tags:
                if query_lower in tag.lower():
                    score += 2

            if score > 0:
                results.append((score, snap))

        results.sort(key=lambda x: x[0], reverse=True)
        return [snap for _, snap in results[:max_results]]

    def get_change_log(self, limit: int = 20) -> List[Dict]:
        sorted_snaps = sorted(
            self.snapshots.values(),
            key=lambda s: s.timestamp,
            reverse=True,
        )
        log = []
        for snap in sorted_snaps[:limit]:
            log.append({
                "snapshot_id": snap.snapshot_id[:8],
                "chapter": snap.chapter,
                "type": snap.snapshot_type.value,
                "timestamp": snap.timestamp,
                "message": snap.message,
                "word_count": snap.word_count,
                "branch": snap.branch_name,
            })
        return log

    def export_snapshot(self, snapshot_id: str, filepath: str) -> bool:
        snap = self.snapshots.get(snapshot_id)
        if not snap:
            return False
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"章节: {snap.chapter}\n")
            f.write(f"版本: {snap.snapshot_id}\n")
            f.write(f"时间: {snap.timestamp}\n")
            f.write(f"类型: {snap.snapshot_type.value}\n")
            f.write(f"分支: {snap.branch_name}\n")
            f.write(f"字数: {snap.word_count}\n")
            if snap.message:
                f.write(f"备注: {snap.message}\n")
            f.write("\n---\n\n")
            f.write(snap.content)
        return True

    def export_archive(self, output_dir: str = None) -> str:
        if output_dir is None:
            output_dir = self._get_archive_dir()
        os.makedirs(output_dir, exist_ok=True)

        for snap in self.snapshots.values():
            filename = f"ch{snap.chapter:04d}_{snap.snapshot_id[:8]}_{snap.branch_name}.txt"
            filepath = os.path.join(output_dir, filename)
            self.export_snapshot(snap.snapshot_id, filepath)

        manifest = {
            "novel_title": self.novel_title,
            "exported_at": datetime.now().isoformat(),
            "total_snapshots": len(self.snapshots),
            "branches": self.branches,
        }
        with open(os.path.join(output_dir, "manifest.json"), "w", encoding="utf-8") as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)

        return output_dir

    def start_auto_save(self, content_provider: callable = None):
        """启动自动保存"""
        if not self.auto_save_config.enabled:
            return

        def _auto_save_loop():
            while self.auto_save_config.enabled:
                time.sleep(self.auto_save_config.interval_seconds)
                if content_provider:
                    for chapter, content in self._dirty_chapters.items():
                        if content:
                            self.create_snapshot(
                                chapter=chapter,
                                content=content,
                                snapshot_type=SnapshotType.AUTO,
                                message="自动保存",
                            )
                    self._dirty_chapters.clear()

        self._auto_save_timer = threading.Thread(target=_auto_save_loop, daemon=True)
        self._auto_save_timer.start()

    def stop_auto_save(self):
        self.auto_save_config.enabled = False
        self.save()

    def mark_dirty(self, chapter: int, content: str):
        self._dirty_chapters[chapter] = content

    def compare_with_external(self, snapshot_id: str,
                              external_text: str) -> Optional[DiffResult]:
        """与外部文本对比"""
        snap = self.snapshots.get(snapshot_id)
        if not snap:
            return None

        lines_a = snap.content.splitlines(keepends=True)
        lines_b = external_text.splitlines(keepends=True)

        differ = difflib.unified_diff(
            lines_a, lines_b,
            fromfile=f"版本{snapshot_id[:8]}",
            tofile="外部文本",
            lineterm="",
        )
        unified = "\n".join(differ)

        matcher = difflib.SequenceMatcher(None, lines_a, lines_b)
        added = removed = modified = 0
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == "insert":
                added += j2 - j1
            elif tag == "delete":
                removed += i2 - i1
            elif tag == "replace":
                modified += max(i2 - i1, j2 - j1)

        total = added + removed + modified
        max_lines = max(len(lines_a), len(lines_b), 1)
        ratio = total / max_lines

        return DiffResult(
            added_lines=added,
            removed_lines=removed,
            modified_lines=modified,
            total_changes=total,
            change_ratio=ratio,
            unified_diff=unified,
        )

    def get_stats(self) -> dict:
        total_words = sum(s.word_count for s in self.snapshots.values())
        by_type = {}
        for st in SnapshotType:
            count = sum(1 for s in self.snapshots.values() if s.snapshot_type == st)
            if count > 0:
                by_type[st.value] = count

        by_branch = {}
        for snap in self.snapshots.values():
            by_branch[snap.branch_name] = by_branch.get(snap.branch_name, 0) + 1

        chapters_tracked = len(set(s.chapter for s in self.snapshots.values()))

        return {
            "total_snapshots": len(self.snapshots),
            "total_branches": len(self.branches),
            "current_branch": self.current_branch,
            "total_words_tracked": total_words,
            "chapters_tracked": chapters_tracked,
            "by_type": by_type,
            "by_branch": by_branch,
            "auto_save_enabled": self.auto_save_config.enabled,
            "auto_save_interval_minutes": self.auto_save_config.interval_seconds // 60,
        }
