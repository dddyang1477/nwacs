#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 记忆管理系统 - MemoryManager
核心功能：
1. 会话记忆 - 存储对话历史和上下文
2. 角色记忆 - 管理所有角色档案
3. 情节记忆 - 追踪剧情节点和伏笔
4. 世界记忆 - 世界观设定持久化
5. 知识片段 - 写作中积累的知识点
6. 上下文窗口 - 智能裁剪，控制记忆大小

设计原则：
- 纯本地存储，零API调用
- JSON持久化，启动即加载
- LRU淘汰策略，控制内存占用
- 标签索引，快速检索
"""

import json
import os
import time
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from collections import OrderedDict
from dataclasses import dataclass, field, asdict


@dataclass
class MemoryEntry:
    """记忆条目"""
    entry_id: str
    memory_type: str  # conversation, character, plot, world, knowledge
    content: str
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: str = ""
    updated_at: str = ""
    access_count: int = 0
    importance: int = 5  # 1-10, 越高越重要

    def __post_init__(self):
        now = datetime.now().isoformat()
        if not self.created_at:
            self.created_at = now
        if not self.updated_at:
            self.updated_at = now


class MemoryStore:
    """分类记忆存储"""

    def __init__(self, store_type: str, max_entries: int = 500):
        self.store_type = store_type
        self.max_entries = max_entries
        self.entries: OrderedDict[str, MemoryEntry] = OrderedDict()
        self.tag_index: Dict[str, List[str]] = {}

    def add(self, entry: MemoryEntry) -> str:
        if entry.entry_id in self.entries:
            self.entries.move_to_end(entry.entry_id)
        else:
            self.entries[entry.entry_id] = entry
            if len(self.entries) > self.max_entries:
                self._evict()

        for tag in entry.tags:
            if tag not in self.tag_index:
                self.tag_index[tag] = []
            if entry.entry_id not in self.tag_index[tag]:
                self.tag_index[tag].append(entry.entry_id)

        return entry.entry_id

    def get(self, entry_id: str) -> Optional[MemoryEntry]:
        entry = self.entries.get(entry_id)
        if entry:
            entry.access_count += 1
            self.entries.move_to_end(entry_id)
        return entry

    def search_by_tags(self, tags: List[str]) -> List[MemoryEntry]:
        if not tags:
            return []
        candidate_ids = set(self.tag_index.get(tags[0], []))
        for tag in tags[1:]:
            candidate_ids &= set(self.tag_index.get(tag, []))
        return [self.entries[eid] for eid in candidate_ids if eid in self.entries]

    def search_by_content(self, keyword: str) -> List[MemoryEntry]:
        keyword_lower = keyword.lower()
        return [
            entry for entry in self.entries.values()
            if keyword_lower in entry.content.lower()
        ]

    def get_recent(self, n: int = 10) -> List[MemoryEntry]:
        items = list(self.entries.values())
        return items[-n:]

    def get_important(self, threshold: int = 7) -> List[MemoryEntry]:
        return [e for e in self.entries.values() if e.importance >= threshold]

    def delete(self, entry_id: str) -> bool:
        if entry_id in self.entries:
            entry = self.entries[entry_id]
            for tag in entry.tags:
                if tag in self.tag_index and entry_id in self.tag_index[tag]:
                    self.tag_index[tag].remove(entry_id)
            del self.entries[entry_id]
            return True
        return False

    def _evict(self):
        """淘汰最旧且重要性最低的条目"""
        candidates = sorted(
            self.entries.items(),
            key=lambda x: (x[1].importance, x[1].access_count)
        )
        if candidates:
            oldest_id = candidates[0][0]
            self.delete(oldest_id)

    def to_dict(self) -> Dict:
        return {
            "store_type": self.store_type,
            "entries": {k: asdict(v) for k, v in self.entries.items()},
            "tag_index": self.tag_index
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "MemoryStore":
        store = cls(data["store_type"])
        for eid, edata in data.get("entries", {}).items():
            entry = MemoryEntry(**edata)
            store.entries[eid] = entry
        store.tag_index = data.get("tag_index", {})
        return store


class MemoryManager:
    """记忆管理器 - 统一管理所有记忆"""

    def __init__(self, storage_dir: str = None):
        if storage_dir is None:
            storage_dir = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "memory_storage"
            )
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)

        self.stores: Dict[str, MemoryStore] = {
            "conversation": MemoryStore("conversation", max_entries=200),
            "character": MemoryStore("character", max_entries=100),
            "plot": MemoryStore("plot", max_entries=200),
            "world": MemoryStore("world", max_entries=100),
            "knowledge": MemoryStore("knowledge", max_entries=300),
        }

        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.stats = {
            "total_adds": 0,
            "total_retrievals": 0,
            "total_deletes": 0,
        }

        self._load_all()

    def _generate_id(self, content: str, prefix: str = "") -> str:
        raw = f"{prefix}{content}{time.time()}"
        return hashlib.md5(raw.encode()).hexdigest()[:12]

    def remember(self, memory_type: str, content: str,
                 tags: List[str] = None, importance: int = 5,
                 metadata: Dict = None) -> str:
        """存储一条记忆"""
        if memory_type not in self.stores:
            raise ValueError(f"未知记忆类型: {memory_type}")

        entry = MemoryEntry(
            entry_id=self._generate_id(content, memory_type),
            memory_type=memory_type,
            content=content,
            tags=tags or [],
            metadata=metadata or {},
            importance=min(max(importance, 1), 10),
        )

        self.stores[memory_type].add(entry)
        self.stats["total_adds"] += 1
        return entry.entry_id

    def recall(self, memory_type: str, entry_id: str) -> Optional[MemoryEntry]:
        """按ID召回记忆"""
        store = self.stores.get(memory_type)
        if store:
            self.stats["total_retrievals"] += 1
            return store.get(entry_id)
        return None

    def recall_by_tags(self, memory_type: str, tags: List[str]) -> List[MemoryEntry]:
        """按标签召回记忆"""
        store = self.stores.get(memory_type)
        if store:
            self.stats["total_retrievals"] += 1
            return store.search_by_tags(tags)
        return []

    def recall_by_keyword(self, memory_type: str, keyword: str) -> List[MemoryEntry]:
        """按关键词搜索记忆"""
        store = self.stores.get(memory_type)
        if store:
            self.stats["total_retrievals"] += 1
            return store.search_by_content(keyword)
        return []

    def recall_recent(self, memory_type: str, n: int = 10) -> List[MemoryEntry]:
        """获取最近的记忆"""
        store = self.stores.get(memory_type)
        if store:
            return store.get_recent(n)
        return []

    def recall_important(self, memory_type: str, threshold: int = 7) -> List[MemoryEntry]:
        """获取重要记忆"""
        store = self.stores.get(memory_type)
        if store:
            return store.get_important(threshold)
        return []

    def forget(self, memory_type: str, entry_id: str) -> bool:
        """删除一条记忆"""
        store = self.stores.get(memory_type)
        if store:
            self.stats["total_deletes"] += 1
            return store.delete(entry_id)
        return False

    def build_context(self, memory_types: List[str] = None,
                      max_tokens: int = 4000) -> str:
        """构建上下文窗口 - 用于注入AI提示词"""
        if memory_types is None:
            memory_types = ["character", "plot", "world"]

        context_parts = []

        for mtype in memory_types:
            store = self.stores.get(mtype)
            if not store:
                continue

            important = store.get_important(threshold=6)
            recent = store.get_recent(n=5)

            seen_ids = set()
            entries = []

            for e in important + recent:
                if e.entry_id not in seen_ids:
                    entries.append(e)
                    seen_ids.add(e.entry_id)

            if entries:
                type_names = {
                    "character": "角色信息",
                    "plot": "剧情节点",
                    "world": "世界观设定",
                    "conversation": "对话历史",
                    "knowledge": "知识点",
                }
                context_parts.append(f"【{type_names.get(mtype, mtype)}】")
                for e in entries[:10]:
                    context_parts.append(f"- {e.content[:200]}")

        context = "\n".join(context_parts)
        if len(context) > max_tokens * 2:
            context = context[:max_tokens * 2] + "\n...(上下文已截断)"
        return context

    def save_character(self, name: str, profile: Dict[str, Any]) -> str:
        """保存角色档案"""
        content = json.dumps(profile, ensure_ascii=False)
        tags = ["角色", profile.get("role", "未知"), profile.get("gender", "未知")]
        return self.remember("character", content, tags=tags,
                            importance=profile.get("importance", 7),
                            metadata={"name": name, "role": profile.get("role")})

    def save_plot_point(self, chapter: int, title: str, summary: str,
                        plot_type: str = "main") -> str:
        """保存剧情节点"""
        content = f"第{chapter}章 {title}: {summary}"
        tags = ["剧情", plot_type, f"第{chapter}章"]
        return self.remember("plot", content, tags=tags,
                            importance=8 if plot_type == "main" else 5,
                            metadata={"chapter": chapter, "type": plot_type})

    def save_world_setting(self, category: str, setting: str) -> str:
        """保存世界观设定"""
        tags = ["世界观", category]
        return self.remember("world", setting, tags=tags, importance=9,
                            metadata={"category": category})

    def save_conversation(self, role: str, message: str) -> str:
        """保存对话记录"""
        tags = ["对话", role]
        return self.remember("conversation", f"[{role}] {message}",
                            tags=tags, importance=3,
                            metadata={"role": role, "timestamp": datetime.now().isoformat()})

    def save_knowledge(self, topic: str, content: str, source: str = "user") -> str:
        """保存知识点"""
        tags = ["知识", topic]
        return self.remember("knowledge", content, tags=tags, importance=6,
                            metadata={"topic": topic, "source": source})

    def get_character_context(self) -> str:
        """获取角色上下文（用于注入提示词）"""
        entries = self.recall_important("character", threshold=5)
        if not entries:
            return "暂无角色信息"
        lines = []
        for e in entries:
            try:
                profile = json.loads(e.content)
                lines.append(f"{profile.get('name', '未知')}: {profile.get('role', '')} - {profile.get('description', '')[:100]}")
            except json.JSONDecodeError:
                lines.append(e.content[:150])
        return "\n".join(lines)

    def get_plot_context(self) -> str:
        """获取剧情上下文"""
        entries = self.recall_recent("plot", n=20)
        if not entries:
            return "暂无剧情记录"
        return "\n".join(e.content[:200] for e in entries)

    def persist(self):
        """持久化所有记忆到磁盘"""
        data = {
            "session_id": self.session_id,
            "stats": self.stats,
            "stores": {k: v.to_dict() for k, v in self.stores.items()},
            "saved_at": datetime.now().isoformat(),
        }
        filepath = os.path.join(self.storage_dir, "memory_snapshot.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _load_all(self):
        """从磁盘加载记忆"""
        filepath = os.path.join(self.storage_dir, "memory_snapshot.json")
        if not os.path.exists(filepath):
            return

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.session_id = data.get("session_id", self.session_id)
            self.stats = data.get("stats", self.stats)

            for store_name, store_data in data.get("stores", {}).items():
                if store_name in self.stores:
                    self.stores[store_name] = MemoryStore.from_dict(store_data)
        except (json.JSONDecodeError, KeyError) as e:
            print(f"  ⚠️ 记忆加载失败: {e}，使用空白记忆")

    def get_summary(self) -> Dict[str, Any]:
        """获取记忆系统摘要"""
        return {
            "session_id": self.session_id,
            "stats": self.stats,
            "store_sizes": {
                name: len(store.entries)
                for name, store in self.stores.items()
            },
            "total_entries": sum(
                len(store.entries) for store in self.stores.values()
            ),
        }

    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            "total_adds": self.stats["total_adds"],
            "total_retrievals": self.stats["total_retrievals"],
            "total_deletes": self.stats["total_deletes"],
            "store_sizes": {
                name: len(store.entries)
                for name, store in self.stores.items()
            },
            "total_entries": sum(
                len(store.entries) for store in self.stores.values()
            ),
        }

    def search_by_tag(self, tag: str) -> List[MemoryEntry]:
        """按标签搜索记忆条目"""
        results = []
        for store in self.stores.values():
            for entry in store.entries:
                if tag in entry.tags:
                    results.append(entry)
        return results

    def clear_session(self):
        """清除当前会话记忆（保留角色和世界观）"""
        for mtype in ["conversation", "knowledge"]:
            self.stores[mtype] = MemoryStore(mtype, max_entries=self.stores[mtype].max_entries)
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")


if __name__ == "__main__":
    print("=" * 60)
    print("🧠 NWACS 记忆管理系统测试")
    print("=" * 60)

    mm = MemoryManager()

    mm.save_character("叶青云", {
        "name": "叶青云",
        "role": "主角",
        "gender": "男",
        "age": 18,
        "description": "天机道主传人，性格坚毅果敢",
        "importance": 9,
    })

    mm.save_character("苏婉儿", {
        "name": "苏婉儿",
        "role": "女主",
        "gender": "女",
        "age": 17,
        "description": "青云宗天才弟子，性格清冷",
        "importance": 8,
    })

    mm.save_plot_point(1, "觉醒", "叶青云在天台觉醒天机盘", "main")
    mm.save_plot_point(2, "入门", "叶青云进入青云宗修炼", "main")
    mm.save_world_setting("修炼体系", "炼气→筑基→金丹→元婴→化神→渡劫→大乘")
    mm.save_conversation("user", "帮我写第一章的开头")
    mm.save_conversation("assistant", "好的，第一章：觉醒...")
    mm.save_knowledge("黄金三章", "前500字必须出现核心设定/金手指/冲突点")

    summary = mm.get_summary()
    print(f"\n记忆摘要: {json.dumps(summary, ensure_ascii=False, indent=2)}")

    context = mm.build_context()
    print(f"\n上下文窗口 ({len(context)}字符):")
    print(context[:500])

    mm.persist()
    print("\n✅ 记忆已持久化到磁盘")
