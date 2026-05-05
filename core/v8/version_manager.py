#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 版本管理与历史回溯系统 - VersionManager

核心能力：
1. 章节快照 - 每次保存自动创建版本快照
2. 版本对比 - 任意两个版本间diff对比
3. 回滚恢复 - 一键回滚到任意历史版本
4. 分支管理 - 支持多分支并行创作
5. 变更日志 - 自动生成修改记录
6. 导出归档 - 完整版本历史打包导出
"""

import json
import os
import hashlib
import shutil
import difflib
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class SnapshotType(Enum):
    AUTO = "自动保存"
    MANUAL = "手动保存"
    MILESTONE = "里程碑"
    BRANCH = "分支点"


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
        )


@dataclass
class DiffResult:
    added_lines: int
    removed_lines: int
    modified_lines: int
    total_changes: int
    change_ratio: float
    unified_diff: str


class VersionManager:
    """版本管理与历史回溯"""

    def __init__(self, novel_title: str = "未命名作品", storage_dir: str = None):
        self.novel_title = novel_title
        if storage_dir is None:
            storage_dir = os.path.join(os.path.dirname(__file__), "..", "version_storage")
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)

        self.snapshots: Dict[str, VersionSnapshot] = {}
        self.current_branch = "main"
        self.branches: Dict[str, str] = {"main": ""}
        self._load()

    def _get_filepath(self) -> str:
        safe_name = re.sub(r'[<>:"/\\|?*]', '_', self.novel_title)
        return os.path.join(self.storage_dir, f"{safe_name}_versions.json")

    def _get_archive_dir(self) -> str:
        safe_name = re.sub(r'[<>:"/\\|?*]', '_', self.novel_title)
        return os.path.join(self.storage_dir, f"{safe_name}_archive")

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

    def create_snapshot(self, chapter: int, content: str,
                        snapshot_type: SnapshotType = SnapshotType.AUTO,
                        message: str = "", tags: List[str] = None,
                        parent_id: str = "") -> str:
        """创建版本快照"""
        import uuid

        snapshot_id = str(uuid.uuid4())[:12]
        word_count = len(content)

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
        )

        self.snapshots[snapshot_id] = snapshot
        self.branches[self.current_branch] = snapshot_id
        self.save()
        return snapshot_id

    def get_snapshot(self, snapshot_id: str) -> Optional[VersionSnapshot]:
        return self.snapshots.get(snapshot_id)

    def get_chapter_history(self, chapter: int) -> List[VersionSnapshot]:
        """获取某章节的所有版本历史"""
        history = [
            s for s in self.snapshots.values()
            if s.chapter == chapter and s.branch_name == self.current_branch
        ]
        history.sort(key=lambda s: s.timestamp)
        return history

    def get_latest(self, chapter: int = None) -> Optional[VersionSnapshot]:
        """获取最新版本"""
        candidates = list(self.snapshots.values())
        if chapter is not None:
            candidates = [s for s in candidates if s.chapter == chapter]
        candidates = [s for s in candidates if s.branch_name == self.current_branch]
        if not candidates:
            return None
        return max(candidates, key=lambda s: s.timestamp)

    def diff(self, snapshot_a: str, snapshot_b: str) -> Optional[DiffResult]:
        """对比两个版本"""
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

    def rollback(self, snapshot_id: str) -> Optional[str]:
        """回滚到指定版本（创建新快照）"""
        target = self.snapshots.get(snapshot_id)
        if not target:
            return None

        return self.create_snapshot(
            chapter=target.chapter,
            content=target.content,
            snapshot_type=SnapshotType.MANUAL,
            message=f"回滚到版本 {snapshot_id[:8]}",
            tags=["rollback"],
            parent_id=snapshot_id,
        )

    def create_branch(self, branch_name: str, from_snapshot: str = "") -> bool:
        """创建分支"""
        if branch_name in self.branches:
            return False
        if not from_snapshot:
            from_snapshot = self.branches.get(self.current_branch, "")
        self.branches[branch_name] = from_snapshot
        self.save()
        return True

    def switch_branch(self, branch_name: str) -> bool:
        """切换分支"""
        if branch_name not in self.branches:
            return False
        self.current_branch = branch_name
        self.save()
        return True

    def merge_branch(self, source_branch: str, target_branch: str = "main") -> bool:
        """合并分支"""
        if source_branch not in self.branches or target_branch not in self.branches:
            return False
        source_tip = self.branches[source_branch]
        if source_tip and source_tip in self.snapshots:
            snapshot = self.snapshots[source_tip]
            self.create_snapshot(
                chapter=snapshot.chapter,
                content=snapshot.content,
                snapshot_type=SnapshotType.MANUAL,
                message=f"合并分支 {source_branch} → {target_branch}",
                tags=["merge", source_branch],
            )
        return True

    def get_change_log(self, limit: int = 20) -> List[Dict]:
        """获取变更日志"""
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

    def export_archive(self, output_dir: str = None) -> str:
        """导出完整版本归档"""
        if output_dir is None:
            output_dir = self._get_archive_dir()
        os.makedirs(output_dir, exist_ok=True)

        for snap in self.snapshots.values():
            filename = f"ch{snap.chapter:04d}_{snap.snapshot_id[:8]}_{snap.branch_name}.txt"
            filepath = os.path.join(output_dir, filename)
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

        manifest = {
            "novel_title": self.novel_title,
            "exported_at": datetime.now().isoformat(),
            "total_snapshots": len(self.snapshots),
            "branches": self.branches,
        }
        with open(os.path.join(output_dir, "manifest.json"), "w", encoding="utf-8") as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)

        return output_dir

    def get_stats(self) -> dict:
        total_words = sum(s.word_count for s in self.snapshots.values())
        by_type = {}
        for st in SnapshotType:
            count = sum(1 for s in self.snapshots.values() if s.snapshot_type == st)
            if count > 0:
                by_type[st.value] = count

        return {
            "total_snapshots": len(self.snapshots),
            "total_branches": len(self.branches),
            "current_branch": self.current_branch,
            "total_words_tracked": total_words,
            "by_type": by_type,
        }


import re
