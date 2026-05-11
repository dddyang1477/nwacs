#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS RAG向量记忆系统 - RAGVectorMemory

对标炼字工坊 RAG向量防崩盘 / Sudowrite Story Bible / AI_NovelGenerator 语义检索引擎

核心能力：
1. 语义向量化 - 将角色/设定/剧情/伏笔转为向量嵌入
2. FAISS向量检索 - 毫秒级语义相似度搜索
3. 上下文自动注入 - 生成前自动检索相关前文，注入提示词
4. 增量更新 - 新章节自动向量化，无需重建索引
5. 混合检索 - 语义搜索 + 关键词搜索双路融合

设计原则：
- 纯本地计算，零API依赖（使用sentence-transformers本地模型）
- 轻量级模型（paraphrase-multilingual-MiniLM-L12-v2，~470MB）
- 首次使用时自动下载模型
- 与NovelMemoryManager无缝集成
"""

import json
import os
import hashlib
import time
import pickle
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
import numpy as np


class MemoryChunkType(Enum):
    CHARACTER = "角色信息"
    PLOT_EVENT = "剧情事件"
    WORLD_SETTING = "世界观设定"
    FORESHADOWING = "伏笔"
    CHAPTER_TEXT = "章节原文"
    WORLD_RULE = "世界规则"
    DIALOGUE = "对话片段"
    LOCATION = "地点描述"
    ITEM = "关键物品"


@dataclass
class MemoryChunk:
    chunk_id: str
    chunk_type: MemoryChunkType
    content: str
    chapter: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    embedding: Optional[np.ndarray] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class VectorSearchResult:
    chunk: MemoryChunk
    score: float
    rank: int = 0


class RAGVectorMemory:
    """RAG向量记忆系统"""

    def __init__(self, persist_dir: str = None):
        if persist_dir is None:
            persist_dir = os.path.join(os.path.dirname(__file__), "..", "..", "vector_memory")
        self.persist_dir = persist_dir
        os.makedirs(persist_dir, exist_ok=True)

        self.chunks: Dict[str, MemoryChunk] = {}
        self._embedding_model = None
        self._faiss_index = None
        self._chunk_id_list: List[str] = []
        self._embedding_dim = 384
        self._model_name = "paraphrase-multilingual-MiniLM-L12-v2"
        self._chunk_counter = 0

        self._load_state()

    def _get_embedding_model(self):
        if self._embedding_model is None:
            try:
                from sentence_transformers import SentenceTransformer
                print(f"[RAG向量记忆] 加载嵌入模型: {self._model_name}")
                self._embedding_model = SentenceTransformer(self._model_name)
                print(f"[RAG向量记忆] 模型加载完成, 维度: {self._embedding_dim}")
            except ImportError:
                raise ImportError(
                    "需要安装 sentence-transformers: pip install sentence-transformers"
                )
            except Exception as e:
                print(f"[RAG向量记忆] 模型加载失败，使用回退模式: {e}")
                self._embedding_model = None
        return self._embedding_model

    def _get_faiss_index(self):
        if self._faiss_index is None:
            try:
                import faiss
                self._faiss_index = faiss.IndexFlatIP(self._embedding_dim)
                if self._chunk_id_list:
                    embeddings = []
                    valid_ids = []
                    for cid in self._chunk_id_list:
                        chunk = self.chunks.get(cid)
                        if chunk and chunk.embedding is not None:
                            embeddings.append(chunk.embedding)
                            valid_ids.append(cid)
                    if embeddings:
                        emb_array = np.array(embeddings, dtype=np.float32)
                        faiss.normalize_L2(emb_array)
                        self._faiss_index.add(emb_array)
                    self._chunk_id_list = valid_ids
            except ImportError:
                raise ImportError(
                    "需要安装 faiss-cpu: pip install faiss-cpu"
                )
        return self._faiss_index

    def _encode(self, texts: List[str]) -> Optional[np.ndarray]:
        model = self._get_embedding_model()
        if model is None:
            return None
        embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
        return embeddings.astype(np.float32)

    def add_chunk(self, content: str, chunk_type: MemoryChunkType,
                  chapter: int = 0, metadata: Dict = None) -> str:
        self._chunk_counter += 1
        chunk_id = f"chunk_{self._chunk_counter:08d}"

        chunk = MemoryChunk(
            chunk_id=chunk_id,
            chunk_type=chunk_type,
            content=content,
            chapter=chapter,
            metadata=metadata or {},
        )

        embedding = self._encode([content])
        if embedding is not None:
            chunk.embedding = embedding[0]
            try:
                import faiss
                index = self._get_faiss_index()
                vec = embedding[0].reshape(1, -1)
                faiss.normalize_L2(vec)
                index.add(vec)
            except Exception:
                pass

        self.chunks[chunk_id] = chunk
        self._chunk_id_list.append(chunk_id)
        return chunk_id

    def add_chunks_batch(self, items: List[Tuple[str, MemoryChunkType, int, Dict]]) -> List[str]:
        texts = [item[0] for item in items]
        embeddings = self._encode(texts)

        chunk_ids = []
        new_embeddings = []

        for i, (content, chunk_type, chapter, metadata) in enumerate(items):
            self._chunk_counter += 1
            chunk_id = f"chunk_{self._chunk_counter:08d}"

            chunk = MemoryChunk(
                chunk_id=chunk_id,
                chunk_type=chunk_type,
                content=content,
                chapter=chapter,
                metadata=metadata or {},
            )

            if embeddings is not None:
                chunk.embedding = embeddings[i]
                new_embeddings.append(embeddings[i])

            self.chunks[chunk_id] = chunk
            self._chunk_id_list.append(chunk_id)
            chunk_ids.append(chunk_id)

        if new_embeddings:
            try:
                import faiss
                index = self._get_faiss_index()
                emb_array = np.array(new_embeddings, dtype=np.float32)
                faiss.normalize_L2(emb_array)
                index.add(emb_array)
            except Exception:
                pass

        return chunk_ids

    def search(self, query: str, top_k: int = 10,
               chunk_types: List[MemoryChunkType] = None,
               min_score: float = 0.3,
               chapter_range: Tuple[int, int] = None) -> List[VectorSearchResult]:
        query_embedding = self._encode([query])
        if query_embedding is None:
            return self._fallback_keyword_search(query, top_k, chunk_types, min_score, chapter_range)

        try:
            import faiss
            index = self._get_faiss_index()
            if index.ntotal == 0:
                return []

            vec = query_embedding[0].reshape(1, -1)
            faiss.normalize_L2(vec)

            search_k = min(top_k * 3, index.ntotal)
            scores, indices = index.search(vec, search_k)

            results = []
            for rank, (score, idx) in enumerate(zip(scores[0], indices[0])):
                if idx < 0 or idx >= len(self._chunk_id_list):
                    continue
                chunk_id = self._chunk_id_list[idx]
                chunk = self.chunks.get(chunk_id)
                if not chunk:
                    continue

                if chunk_types and chunk.chunk_type not in chunk_types:
                    continue
                if chapter_range:
                    if chunk.chapter < chapter_range[0] or chunk.chapter > chapter_range[1]:
                        continue
                if score < min_score:
                    continue

                results.append(VectorSearchResult(chunk=chunk, score=float(score), rank=rank))

                if len(results) >= top_k:
                    break

            return results

        except Exception as e:
            print(f"[RAG向量记忆] FAISS搜索失败，回退关键词搜索: {e}")
            return self._fallback_keyword_search(query, top_k, chunk_types, min_score, chapter_range)

    def _fallback_keyword_search(self, query: str, top_k: int,
                                  chunk_types: List[MemoryChunkType],
                                  min_score: float,
                                  chapter_range: Tuple[int, int]) -> List[VectorSearchResult]:
        results = []
        query_lower = query.lower()

        for chunk_id, chunk in self.chunks.items():
            if chunk_types and chunk.chunk_type not in chunk_types:
                continue
            if chapter_range:
                if chunk.chapter < chapter_range[0] or chunk.chapter > chapter_range[1]:
                    continue

            content_lower = chunk.content.lower()
            score = 0.0
            if query_lower in content_lower:
                score = 0.7
            else:
                query_terms = query_lower.split()
                matched = sum(1 for t in query_terms if t in content_lower)
                if query_terms:
                    score = matched / len(query_terms) * 0.5

            if score >= min_score:
                results.append(VectorSearchResult(chunk=chunk, score=score))

        results.sort(key=lambda r: r.score, reverse=True)
        for i, r in enumerate(results[:top_k]):
            r.rank = i
        return results[:top_k]

    def context_aware_retrieve(self, current_chapter: int,
                                query: str = "",
                                context_window: int = 10,
                                top_k: int = 15) -> Dict:
        chapter_start = max(1, current_chapter - context_window)

        if query:
            semantic_results = self.search(
                query=query,
                top_k=top_k,
                chapter_range=(chapter_start, current_chapter),
                min_score=0.25,
            )
        else:
            semantic_results = self.search(
                query=f"第{current_chapter}章 剧情 角色 设定",
                top_k=top_k,
                chapter_range=(chapter_start, current_chapter),
                min_score=0.2,
            )

        character_chunks = self.search(
            query=query or "角色 人物 性格 外貌 能力",
            top_k=5,
            chunk_types=[MemoryChunkType.CHARACTER],
            min_score=0.2,
        )

        foreshadowing_chunks = self.search(
            query=query or "伏笔 线索 悬念",
            top_k=5,
            chunk_types=[MemoryChunkType.FORESHADOWING],
            min_score=0.2,
        )

        world_chunks = self.search(
            query=query or "世界观 设定 规则 体系",
            top_k=5,
            chunk_types=[MemoryChunkType.WORLD_SETTING, MemoryChunkType.WORLD_RULE],
            min_score=0.2,
        )

        return {
            "current_chapter": current_chapter,
            "context_window": context_window,
            "semantic_context": [
                {"content": r.chunk.content[:300], "score": r.score, "chapter": r.chunk.chapter,
                 "type": r.chunk.chunk_type.value}
                for r in semantic_results
            ],
            "active_characters": [
                {"content": r.chunk.content[:200], "score": r.score}
                for r in character_chunks
            ],
            "pending_foreshadowing": [
                {"content": r.chunk.content[:200], "score": r.score}
                for r in foreshadowing_chunks
            ],
            "world_context": [
                {"content": r.chunk.content[:200], "score": r.score}
                for r in world_chunks
            ],
        }

    def build_context_prompt(self, current_chapter: int,
                              query: str = "",
                              max_tokens: int = 2000) -> str:
        retrieved = self.context_aware_retrieve(current_chapter, query, top_k=20)

        parts = []

        if retrieved["active_characters"]:
            parts.append("【当前活跃角色】")
            for c in retrieved["active_characters"][:5]:
                parts.append(f"- {c['content']}")

        if retrieved["world_context"]:
            parts.append("\n【世界观设定】")
            for w in retrieved["world_context"][:3]:
                parts.append(f"- {w['content']}")

        if retrieved["pending_foreshadowing"]:
            parts.append("\n【待回收伏笔】")
            for f in retrieved["pending_foreshadowing"][:3]:
                parts.append(f"- {f['content']}")

        if retrieved["semantic_context"]:
            parts.append("\n【前文相关剧情】")
            for s in retrieved["semantic_context"][:5]:
                parts.append(f"- [第{s['chapter']}章] {s['content']}")

        context = "\n".join(parts)
        if len(context) > max_tokens * 2:
            context = context[:max_tokens * 2] + "\n...(上下文已截断)"

        return context

    def index_from_novel_memory(self, memory_manager) -> int:
        from novel_memory_manager import NovelMemoryManager
        count = 0

        for name, profile in memory_manager.characters.items():
            content = f"角色「{name}」: 性别{profile.gender}, 年龄{profile.age}, "
            content += f"外貌{profile.appearance}, 性格{profile.personality}, "
            content += f"角色定位{profile.role}, 首次出场第{profile.first_appearance_chapter}章"
            if profile.speech_style:
                content += f", 说话风格: {profile.speech_style}"
            if profile.catchphrase:
                content += f", 口头禅: {profile.catchphrase}"
            self.add_chunk(content, MemoryChunkType.CHARACTER,
                           chapter=profile.first_appearance_chapter,
                           metadata={"name": name, "role": profile.role})
            count += 1

        for event in memory_manager.plot_events:
            content = f"第{event['chapter']}章: {event['event']}"
            if event.get('type'):
                content += f" [{event['type']}]"
            if event.get('characters'):
                content += f" 涉及: {', '.join(event['characters'])}"
            self.add_chunk(content, MemoryChunkType.PLOT_EVENT,
                           chapter=event['chapter'],
                           metadata={"type": event.get('type', '')})
            count += 1

        for key, value in memory_manager.world_settings.items():
            content = f"世界观设定「{key}」: {str(value)[:500]}"
            self.add_chunk(content, MemoryChunkType.WORLD_SETTING,
                           metadata={"key": key})
            count += 1

        for fs in memory_manager.foreshadowings.values():
            content = f"伏笔: {fs.description} (埋设第{fs.planted_chapter}章, "
            content += f"预期回收第{fs.expected_payoff_chapter}章, 状态{fs.status.value})"
            self.add_chunk(content, MemoryChunkType.FORESHADOWING,
                           chapter=fs.planted_chapter,
                           metadata={"status": fs.status.value})
            count += 1

        for rule in memory_manager.world_rules:
            content = f"世界规则: {rule.get('rule', '')} - {rule.get('description', '')}"
            self.add_chunk(content, MemoryChunkType.WORLD_RULE)
            count += 1

        for ch, text in memory_manager.chapter_texts.items():
            paragraphs = text.split('\n')
            for i in range(0, len(paragraphs), 3):
                chunk_text = '\n'.join(paragraphs[i:i+3]).strip()
                if len(chunk_text) > 50:
                    self.add_chunk(chunk_text, MemoryChunkType.CHAPTER_TEXT,
                                   chapter=ch)
                    count += 1

        self._save_state()
        return count

    def get_stats(self) -> Dict:
        index_size = 0
        try:
            if self._faiss_index is not None:
                index_size = self._faiss_index.ntotal
        except Exception:
            pass

        type_counts = {}
        for chunk in self.chunks.values():
            t = chunk.chunk_type.value
            type_counts[t] = type_counts.get(t, 0) + 1

        return {
            "total_chunks": len(self.chunks),
            "indexed_vectors": index_size,
            "embedding_dim": self._embedding_dim,
            "model": self._model_name,
            "by_type": type_counts,
            "persist_dir": self.persist_dir,
        }

    def _save_state(self):
        state = {
            "chunk_counter": self._chunk_counter,
            "chunk_id_list": self._chunk_id_list,
            "chunks": {
                cid: {
                    "chunk_id": c.chunk_id,
                    "chunk_type": c.chunk_type.value,
                    "content": c.content,
                    "chapter": c.chapter,
                    "metadata": c.metadata,
                    "created_at": c.created_at,
                }
                for cid, c in self.chunks.items()
            },
        }
        state_path = os.path.join(self.persist_dir, "rag_state.json")
        with open(state_path, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)

        if self._faiss_index is not None and self._faiss_index.ntotal > 0:
            try:
                import faiss
                index_path = os.path.join(self.persist_dir, "faiss_index.bin")
                faiss.write_index(self._faiss_index, index_path)
            except Exception:
                pass

    def _load_state(self):
        state_path = os.path.join(self.persist_dir, "rag_state.json")
        if not os.path.exists(state_path):
            return

        try:
            with open(state_path, "r", encoding="utf-8") as f:
                state = json.load(f)

            self._chunk_counter = state.get("chunk_counter", 0)
            self._chunk_id_list = state.get("chunk_id_list", [])

            for cid, cdata in state.get("chunks", {}).items():
                chunk = MemoryChunk(
                    chunk_id=cdata["chunk_id"],
                    chunk_type=MemoryChunkType(cdata["chunk_type"]),
                    content=cdata["content"],
                    chapter=cdata.get("chapter", 0),
                    metadata=cdata.get("metadata", {}),
                    created_at=cdata.get("created_at", ""),
                )
                self.chunks[cid] = chunk

            index_path = os.path.join(self.persist_dir, "faiss_index.bin")
            if os.path.exists(index_path):
                try:
                    import faiss
                    self._faiss_index = faiss.read_index(index_path)
                except Exception:
                    pass

        except Exception as e:
            print(f"[RAG向量记忆] 状态加载失败: {e}")

    def clear(self):
        self.chunks.clear()
        self._chunk_id_list.clear()
        self._faiss_index = None
        self._chunk_counter = 0
        state_path = os.path.join(self.persist_dir, "rag_state.json")
        index_path = os.path.join(self.persist_dir, "faiss_index.bin")
        for p in [state_path, index_path]:
            if os.path.exists(p):
                os.remove(p)


if __name__ == "__main__":
    print("=" * 60)
    print("RAG向量记忆系统 - 功能验证")
    print("=" * 60)

    rag = RAGVectorMemory()

    print("\n[1] 添加记忆块...")
    rag.add_chunk("主角叶青云，废柴体质，被退婚羞辱后获得上古传承",
                  MemoryChunkType.CHARACTER, chapter=1)
    rag.add_chunk("青云宗位于东荒大陆，以剑修闻名，宗主为化神期修士",
                  MemoryChunkType.WORLD_SETTING, chapter=1)
    rag.add_chunk("叶青云在家族大比中一鸣惊人，击败了所有看不起他的人",
                  MemoryChunkType.PLOT_EVENT, chapter=50)
    rag.add_chunk("神秘老者在禁地中传授叶青云九天剑诀",
                  MemoryChunkType.PLOT_EVENT, chapter=30)

    print(f"  已添加: {len(rag.chunks)} 个记忆块")

    print("\n[2] 语义搜索测试...")
    queries = [
        "主角获得了什么能力",
        "宗门在哪里",
        "主角如何证明自己",
    ]

    for q in queries:
        results = rag.search(q, top_k=3)
        print(f"\n  查询: 「{q}」")
        if results:
            for r in results[:2]:
                print(f"    [{r.score:.3f}] {r.chunk.content[:80]}...")
        else:
            print(f"    (无结果 - 可能模型未加载，使用回退模式)")

    print(f"\n[3] 统计: {rag.get_stats()}")
    print("\n✅ RAG向量记忆系统验证完成")
