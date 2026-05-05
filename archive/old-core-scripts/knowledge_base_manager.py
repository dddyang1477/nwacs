#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS用户知识库管理系统
让用户创建、管理和使用私有知识库
"""

import os
import json
import uuid
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional


class UserKnowledgeBase:
    """用户知识库"""

    def __init__(self, project_root: Path = None):
        self.project_root = project_root or Path(__file__).parent.parent
        self.user_kb_dir = self.project_root / "user_data" / "knowledge_bases"
        self.user_kb_dir.mkdir(parents=True, exist_ok=True)
        self.index_file = self.user_kb_dir / "index.json"
        self._init_index()

    def _init_index(self):
        """初始化索引"""
        if not self.index_file.exists():
            self._save_index({})

    def _load_index(self) -> Dict:
        """加载索引"""
        with open(self.index_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _save_index(self, index: Dict):
        """保存索引"""
        with open(self.index_file, 'w', encoding='utf-8') as f:
            json.dump(index, f, ensure_ascii=False, indent=2)

    def create_knowledge_base(self, name: str, description: str = "", kb_type: str = "custom") -> Dict:
        """创建知识库"""
        kb_id = str(uuid.uuid4())[:8]
        kb_info = {
            "id": kb_id,
            "name": name,
            "description": description,
            "type": kb_type,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "entries": 0,
            "tags": []
        }

        # 保存知识库信息
        index = self._load_index()
        index[kb_id] = kb_info
        self._save_index(index)

        # 创建知识库文件
        kb_file = self.user_kb_dir / f"{kb_id}.json"
        with open(kb_file, 'w', encoding='utf-8') as f:
            json.dump({"entries": []}, f, ensure_ascii=False, indent=2)

        return kb_info

    def add_entry(self, kb_id: str, question: str, answer: str, tags: List[str] = None) -> bool:
        """添加条目到知识库"""
        index = self._load_index()
        if kb_id not in index:
            return False

        kb_file = self.user_kb_dir / f"{kb_id}.json"
        with open(kb_file, 'r', encoding='utf-8') as f:
            kb_data = json.load(f)

        entry = {
            "id": str(uuid.uuid4())[:12],
            "question": question,
            "answer": answer,
            "tags": tags or [],
            "created_at": datetime.now().isoformat()
        }

        kb_data["entries"].append(entry)
        index[kb_id]["entries"] = len(kb_data["entries"])
        index[kb_id]["updated_at"] = datetime.now().isoformat()

        with open(kb_file, 'w', encoding='utf-8') as f:
            json.dump(kb_data, f, ensure_ascii=False, indent=2)
        self._save_index(index)

        return True

    def search_knowledge_base(self, kb_id: str, query: str, limit: int = 5) -> List[Dict]:
        """搜索知识库"""
        kb_file = self.user_kb_dir / f"{kb_id}.json"
        if not kb_file.exists():
            return []

        with open(kb_file, 'r', encoding='utf-8') as f:
            kb_data = json.load(f)

        results = []
        query_lower = query.lower()

        for entry in kb_data["entries"]:
            score = 0
            if query_lower in entry["question"].lower():
                score += 2
            if query_lower in entry["answer"].lower():
                score += 1
            if any(query_lower in tag.lower() for tag in entry.get("tags", [])):
                score += 3

            if score > 0:
                results.append({
                    "entry": entry,
                    "score": score
                })

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:limit]

    def get_all_knowledge_bases(self) -> List[Dict]:
        """获取所有知识库"""
        index = self._load_index()
        return list(index.values())

    def delete_knowledge_base(self, kb_id: str) -> bool:
        """删除知识库"""
        index = self._load_index()
        if kb_id not in index:
            return False

        kb_file = self.user_kb_dir / f"{kb_id}.json"
        if kb_file.exists():
            kb_file.unlink()

        del index[kb_id]
        self._save_index(index)
        return True

    def get_knowledge_base_content(self, kb_id: str) -> Optional[Dict]:
        """获取知识库完整内容"""
        kb_file = self.user_kb_dir / f"{kb_id}.json"
        if not kb_file.exists():
            return None

        with open(kb_file, 'r', encoding='utf-8') as f:
            return json.load(f)


class KnowledgeBaseManager:
    """知识库管理器"""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.user_kb = UserKnowledgeBase(self.project_root)

    def list_knowledge_bases(self) -> Dict:
        """列出所有知识库"""
        user_kbs = self.user_kb.get_all_knowledge_bases()

        return {
            "success": True,
            "user_knowledge_bases": user_kbs,
            "total": len(user_kbs)
        }

    def create_knowledge_base(self, name: str, description: str = "", kb_type: str = "custom") -> Dict:
        """创建知识库"""
        kb_info = self.user_kb.create_knowledge_base(name, description, kb_type)
        return {
            "success": True,
            "knowledge_base": kb_info
        }

    def add_knowledge_entry(self, kb_id: str, question: str, answer: str, tags: List[str] = None) -> Dict:
        """添加知识条目"""
        success = self.user_kb.add_entry(kb_id, question, answer, tags)
        if success:
            return {"success": True, "message": "知识条目添加成功"}
        return {"success": False, "error": "知识库不存在"}

    def search_knowledge(self, kb_id: str, query: str, limit: int = 5) -> Dict:
        """搜索知识"""
        results = self.user_kb.search_knowledge_base(kb_id, query, limit)
        return {
            "success": True,
            "query": query,
            "results": results,
            "count": len(results)
        }

    def get_knowledge_base(self, kb_id: str) -> Dict:
        """获取知识库"""
        kb_info = None
        index = self.user_kb._load_index()
        if kb_id in index:
            kb_info = index[kb_id]

        content = self.user_kb.get_knowledge_base_content(kb_id)

        if kb_info and content:
            return {
                "success": True,
                "knowledge_base": kb_info,
                "content": content
            }
        return {"success": False, "error": "知识库不存在"}

    def delete_knowledge_base(self, kb_id: str) -> Dict:
        """删除知识库"""
        success = self.user_kb.delete_knowledge_base(kb_id)
        if success:
            return {"success": True, "message": "知识库删除成功"}
        return {"success": False, "error": "知识库不存在"}


def interactive_manager():
    """交互式知识库管理"""
    manager = KnowledgeBaseManager()

    print("="*60)
    print("📚 NWACS用户知识库管理系统")
    print("="*60)

    while True:
        print("\n请选择操作:")
        print("  1. 查看所有知识库")
        print("  2. 创建知识库")
        print("  3. 添加知识条目")
        print("  4. 搜索知识")
        print("  5. 查看知识库内容")
        print("  6. 删除知识库")
        print("  0. 退出")

        choice = input("\n请输入选项: ").strip()

        if choice == "0":
            break

        elif choice == "1":
            result = manager.list_knowledge_bases()
            print(f"\n共有 {result['total']} 个知识库:")
            for kb in result['user_knowledge_bases']:
                print(f"  - {kb['name']} ({kb['id']}) - {kb['entries']}条")

        elif choice == "2":
            name = input("知识库名称: ").strip()
            desc = input("描述(可选): ").strip()
            kb_type = input("类型(默认custom): ").strip() or "custom"
            result = manager.create_knowledge_base(name, desc, kb_type)
            if result['success']:
                print(f"\n✅ 知识库创建成功: {result['knowledge_base']['id']}")

        elif choice == "3":
            kb_id = input("知识库ID: ").strip()
            question = input("问题: ").strip()
            answer = input("答案: ").strip()
            tags = input("标签(逗号分隔): ").strip()
            tags_list = [t.strip() for t in tags.split(",")] if tags else []
            result = manager.add_knowledge_entry(kb_id, question, answer, tags_list)
            print(f"\n{'✅' if result['success'] else '❌'} {result.get('message') or result.get('error')}")

        elif choice == "4":
            kb_id = input("知识库ID: ").strip()
            query = input("搜索关键词: ").strip()
            result = manager.search_knowledge(kb_id, query)
            print(f"\n找到 {result['count']} 条结果:")
            for r in result['results']:
                print(f"\n  匹配度: {r['score']}")
                print(f"  问题: {r['entry']['question']}")
                print(f"  答案: {r['entry']['answer'][:100]}...")

        elif choice == "5":
            kb_id = input("知识库ID: ").strip()
            result = manager.get_knowledge_base(kb_id)
            if result['success']:
                print(f"\n知识库: {result['knowledge_base']['name']}")
                print(f"描述: {result['knowledge_base']['description']}")
                print(f"条目数: {len(result['content']['entries'])}")
            else:
                print(f"\n❌ {result['error']}")

        elif choice == "6":
            kb_id = input("知识库ID: ").strip()
            confirm = input(f"确认删除知识库 {kb_id}？(y/n): ").strip().lower()
            if confirm == 'y':
                result = manager.delete_knowledge_base(kb_id)
                print(f"\n{'✅' if result['success'] else '❌'} {result.get('message') or result.get('error')}")

        else:
            print("\n无效选项")


if __name__ == "__main__":
    interactive_manager()
