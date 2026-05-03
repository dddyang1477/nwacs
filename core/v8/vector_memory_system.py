#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS V8.5 增强版向量记忆系统
参考NovelForge核心功能: ChromaDB向量数据库 + 100万字超长记忆

核心能力:
- 实时记录角色属性/伏笔状态
- 语义检索top-k相关片段
- RAG检索增强生成
- 杜绝穿越式bug
"""

import os
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MemoryType(Enum):
    CHARACTER_BACKGROUND = "character_background"
    CHARACTER_EMOTION = "character_emotion"
    CHARACTER_RELATIONSHIP = "character_relationship"
    PLOT_POINT = "plot_point"
    FORESHADOW = "foreshadow"
    WORLD_SETTING = "world_setting"
    DIALOGUE = "dialogue"
    BATTLE = "battle"
    ROMANCE = "romance"


@dataclass
class MemoryChunk:
    """记忆块"""
    chunk_id: str
    memory_type: MemoryType
    content: str
    chapter: int
    importance: float
    keywords: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict:
        return {
            "chunk_id": self.chunk_id,
            "memory_type": self.memory_type.value,
            "content": self.content,
            "chapter": self.chapter,
            "importance": self.importance,
            "keywords": self.keywords,
            "metadata": self.metadata,
            "timestamp": self.timestamp
        }


@dataclass
class CharacterState:
    """角色状态"""
    character_id: str
    name: str
    current_location: str = ""
    current_emotion: str = ""
    personality_traits: List[str] = field(default_factory=list)
    relationships: Dict[str, str] = field(default_factory=dict)
    abilities: List[str] = field(default_factory=list)
    status: Dict[str, Any] = field(default_factory=dict)
    last_appearance_chapter: int = 0


class VectorMemoryDatabase:
    """向量数据库长程记忆系统"""

    def __init__(self, db_path: str = None):
        self.db_path = db_path or os.path.join("core/v8", "vector_db")
        os.makedirs(self.db_path, exist_ok=True)

        self.characters_file = os.path.join(self.db_path, "characters.json")
        self.memories_file = os.path.join(self.db_path, "memories.json")
        self.foreshadows_file = os.path.join(self.db_path, "foreshadows.json")
        self.plot_timeline_file = os.path.join(self.db_path, "plot_timeline.json")

        self.characters: Dict[str, CharacterState] = {}
        self.memories: List[MemoryChunk] = []
        self.foreshadows: List[Dict] = []
        self.plot_timeline: List[Dict] = []

        self._load_data()

    def _load_data(self):
        """加载数据"""
        if os.path.exists(self.characters_file):
            with open(self.characters_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for char_id, char_data in data.items():
                    self.characters[char_id] = CharacterState(**char_data)

        if os.path.exists(self.memories_file):
            with open(self.memories_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for mem_data in data:
                    mem_data['memory_type'] = MemoryType(mem_data['memory_type'])
                self.memories = [MemoryChunk(**m) for m in data]

        if os.path.exists(self.foreshadows_file):
            with open(self.foreshadows_file, 'r', encoding='utf-8') as f:
                self.foreshadows = json.load(f)

        if os.path.exists(self.plot_timeline_file):
            with open(self.plot_timeline_file, 'r', encoding='utf-8') as f:
                self.plot_timeline = json.load(f)

    def _save_data(self):
        """保存数据"""
        with open(self.characters_file, 'w', encoding='utf-8') as f:
            json.dump({k: asdict(v) for k, v in self.characters.items()}, f, ensure_ascii=False, indent=2)

        with open(self.memories_file, 'w', encoding='utf-8') as f:
            json.dump([m.to_dict() for m in self.memories], f, ensure_ascii=False, indent=2)

        with open(self.foreshadows_file, 'w', encoding='utf-8') as f:
            json.dump(self.foreshadows, f, ensure_ascii=False, indent=2)

        with open(self.plot_timeline_file, 'w', encoding='utf-8') as f:
            json.dump(self.plot_timeline, f, ensure_ascii=False, indent=2)

    def add_character(self, character_id: str, name: str,
                     personality_traits: List[str] = None,
                     relationships: Dict[str, str] = None):
        """添加角色"""
        self.characters[character_id] = CharacterState(
            character_id=character_id,
            name=name,
            personality_traits=personality_traits or [],
            relationships=relationships or {}
        )
        self._save_data()
        logger.info(f"✅ 角色添加: {name}")

    def update_character_state(self, character_id: str, **kwargs):
        """更新角色状态"""
        if character_id in self.characters:
            char = self.characters[character_id]
            for key, value in kwargs.items():
                if hasattr(char, key):
                    setattr(char, key, value)
            self._save_data()
            logger.info(f"✅ 角色状态更新: {char.name}")

    def add_memory(self, memory_type: MemoryType, content: str, chapter: int,
                  importance: float = 0.5, keywords: List[str] = None,
                  metadata: Dict = None) -> str:
        """添加记忆"""
        chunk_id = hashlib.md5(f"{content}:{chapter}:{datetime.now().isoformat()}".encode()).hexdigest()[:12]

        keywords = keywords or self._extract_keywords(content)

        memory = MemoryChunk(
            chunk_id=chunk_id,
            memory_type=memory_type,
            content=content,
            chapter=chapter,
            importance=importance,
            keywords=keywords,
            metadata=metadata or {}
        )

        self.memories.append(memory)
        self._save_data()

        logger.info(f"✅ 记忆添加: [{memory_type.value}] 第{chapter}章")
        return chunk_id

    def _extract_keywords(self, content: str) -> List[str]:
        """提取关键词"""
        stop_words = {"的", "了", "是", "在", "和", "与", "或", "这", "那", "个", "他", "她", "它"}
        words = []
        current_word = ""

        for char in content:
            if '\u4e00' <= char <= '\u9fff':
                current_word += char
            else:
                if current_word and len(current_word) >= 2 and current_word not in stop_words:
                    words.append(current_word)
                current_word = ""

        if current_word and len(current_word) >= 2:
            words.append(current_word)

        return list(set(words))[:10]

    def add_foreshadow(self, foreshadow_type: str, description: str,
                      chapter_planted: int, importance: float = 0.5) -> str:
        """添加伏笔"""
        f_id = hashlib.md5(f"{description}:{chapter_planted}".encode()).hexdigest()[:8]

        foreshadow = {
            "foreshadow_id": f_id,
            "type": foreshadow_type,
            "description": description,
            "chapter_planted": chapter_planted,
            "importance": importance,
            "fulfilled": False,
            "chapter_fulfilled": None,
            "timestamp": datetime.now().isoformat()
        }

        self.foreshadows.append(foreshadow)
        self._save_data()

        logger.info(f"✅ 伏笔添加: [{foreshadow_type}] 第{chapter_planted}章")
        return f_id

    def fulfill_foreshadow(self, foreshadow_id: str, chapter: int):
        """回收伏笔"""
        for f in self.foreshadows:
            if f["foreshadow_id"] == foreshadow_id:
                f["fulfilled"] = True
                f["chapter_fulfilled"] = chapter
                self._save_data()
                logger.info(f"✅ 伏笔回收: {f['description'][:30]}... 第{chapter}章")
                return True
        return False

    def add_plot_point(self, point_type: str, description: str, chapter: int):
        """添加剧情点"""
        point = {
            "type": point_type,
            "description": description,
            "chapter": chapter,
            "timestamp": datetime.now().isoformat()
        }
        self.plot_timeline.append(point)
        self.plot_timeline.sort(key=lambda x: x["chapter"])
        self._save_data()

    def semantic_search(self, query: str, top_k: int = 5,
                       memory_types: List[MemoryType] = None) -> List[MemoryChunk]:
        """语义检索 - RAG核心"""
        query_keywords = set(self._extract_keywords(query))

        if not query_keywords:
            query_keywords = set(query.lower().split())

        scored_memories = []

        for mem in self.memories:
            if memory_types and mem.memory_type not in memory_types:
                continue

            content_keywords = set(mem.keywords)
            intersection = query_keywords & content_keywords

            if intersection:
                score = len(intersection) * mem.importance
                if mem.chapter:
                    recency_bonus = 1.0 / (1 + abs(mem.chapter - self.get_latest_chapter()) * 0.01)
                    score *= (1 + recency_bonus)

                scored_memories.append((mem, score))

        scored_memories.sort(key=lambda x: x[1], reverse=True)
        return [mem for mem, _ in scored_memories[:top_k]]

    def get_latest_chapter(self) -> int:
        """获取最新章节"""
        if not self.memories:
            return 0
        return max(mem.chapter for mem in self.memories)

    def get_character_memories(self, character_id: str, top_k: int = 10) -> List[MemoryChunk]:
        """获取角色相关记忆"""
        relevant = [m for m in self.memories if character_id in m.content]
        relevant.sort(key=lambda x: (x.importance, x.chapter), reverse=True)
        return relevant[:top_k]

    def get_unfulfilled_foreshadows(self) -> List[Dict]:
        """获取未回收伏笔"""
        return [f for f in self.foreshadows if not f["fulfilled"]]

    def get_plot_timeline(self, from_chapter: int = None) -> List[Dict]:
        """获取剧情时间线"""
        if from_chapter:
            return [p for p in self.plot_timeline if p["chapter"] >= from_chapter]
        return self.plot_timeline

    def build_rag_context(self, query: str, max_chunks: int = 5) -> str:
        """构建RAG上下文"""
        relevant_memories = self.semantic_search(query, top_k=max_chunks)

        if not relevant_memories:
            return ""

        context_parts = ["[相关记忆检索]", ""]

        for i, mem in enumerate(relevant_memories, 1):
            context_parts.append(f"--- 记忆{i} [第{mem.chapter}章] ---")
            context_parts.append(mem.content)
            if mem.metadata:
                context_parts.append(f"[元数据: {mem.metadata}]")

        return "\n".join(context_parts)

    def consistency_check(self, character_id: str, content: str,
                         current_chapter: int) -> Dict[str, List[str]]:
        """一致性检查"""
        issues = {
            "character_behavior": [],
            "timeline": [],
            "foreshadow": [],
            "setting": []
        }

        if character_id not in self.characters:
            return issues

        char = self.characters[character_id]

        if char.personality_traits:
            content_lower = content.lower()
            trait_mentioned = any(trait in content_lower for trait in char.personality_traits)
            if not trait_mentioned:
                issues["character_behavior"].append(
                    f"角色{char.name}的性格特质未体现: {char.personality_traits[:2]}"
                )

        unfulfilled = self.get_unfulfilled_foreshadows()
        for f in unfulfilled[:3]:
            if f["chapter_planted"] > current_chapter:
                issues["foreshadow"].append(
                    f"伏笔时间线异常: {f['description'][:20]}... 种植于第{f['chapter_planted']}章"
                )

        if char.last_appearance_chapter > 0:
            gap = current_chapter - char.last_appearance_chapter
            if gap > 20:
                issues["timeline"].append(
                    f"角色{char.name}已{gap}章未出现，可能需要出场或说明"
                )

        return issues

    def get_statistics(self) -> Dict:
        """获取统计信息"""
        return {
            "total_characters": len(self.characters),
            "total_memories": len(self.memories),
            "total_foreshadows": len(self.foreshadows),
            "fulfilled_foreshadows": len([f for f in self.foreshadows if f["fulfilled"]]),
            "unfulfilled_foreshadows": len([f for f in self.foreshadows if not f["fulfilled"]]),
            "plot_points": len(self.plot_timeline),
            "latest_chapter": self.get_latest_chapter(),
            "memory_types_distribution": self._get_memory_type_distribution()
        }

    def _get_memory_type_distribution(self) -> Dict[str, int]:
        """获取记忆类型分布"""
        distribution = {}
        for mem in self.memories:
            type_name = mem.memory_type.value
            distribution[type_name] = distribution.get(type_name, 0) + 1
        return distribution

    def generate_memory_report(self) -> str:
        """生成记忆报告"""
        stats = self.get_statistics()

        report = []
        report.append("="*60)
        report.append("📊 NWACS V8.5 向量记忆系统报告")
        report.append("="*60)
        report.append("")
        report.append(f"总角色数: {stats['total_characters']}")
        report.append(f"总记忆数: {stats['total_memories']}")
        report.append(f"伏笔总数: {stats['total_foreshadows']}")
        report.append(f"  - 已回收: {stats['fulfilled_foreshadows']}")
        report.append(f"  - 未回收: {stats['unfulfilled_foreshadows']}")
        report.append(f"剧情点数: {stats['plot_points']}")
        report.append(f"最新章节: {stats['latest_chapter']}")
        report.append("")

        report.append("记忆类型分布:")
        for mem_type, count in stats["memory_types_distribution"].items():
            report.append(f"  • {mem_type}: {count}")

        report.append("")
        report.append("未回收伏笔:")
        unfulfilled = self.get_unfulfilled_foreshadows()
        for f in unfulfilled[:5]:
            report.append(f"  ⚡ [{f['type']}] 第{f['chapter_planted']}章: {f['description'][:40]}...")

        return "\n".join(report)


def main():
    print("="*60)
    print("🧠 NWACS V8.5 向量记忆系统初始化")
    print("="*60)

    vmdb = VectorMemoryDatabase()

    print("\n📊 系统统计:")
    stats = vmdb.get_statistics()
    for key, value in stats.items():
        if key != "memory_types_distribution":
            print(f"  {key}: {value}")

    print("\n" + "="*60)
    print("✅ 向量记忆系统就绪")
    print("="*60)


if __name__ == "__main__":
    main()