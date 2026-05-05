#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS V8.0 知识库管理系统
核心功能：
1. 知识库索引与检索
2. 知识图谱构建
3. 智能知识匹配
4. 动态知识更新
"""

import sys
import json
import os
import re
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding='utf-8')
except (AttributeError, OSError):
    pass

class KnowledgeItem:
    """知识条目"""
    
    def __init__(self, item_id: str, title: str, content: str, 
                 category: str, tags: List[str], source: str = "unknown",
                 created_at: datetime = None, updated_at: datetime = None):
        self.item_id = item_id
        self.title = title
        self.content = content
        self.category = category
        self.tags = tags
        self.source = source
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
        self.access_count = 0
    
    def to_dict(self):
        return {
            "item_id": self.item_id,
            "title": self.title,
            "category": self.category,
            "tags": self.tags,
            "source": self.source,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "access_count": self.access_count
        }

class KnowledgeCategory:
    """知识分类"""
    
    def __init__(self, category_id: str, name: str, description: str = "", 
                 parent_id: str = None, children: List[str] = None):
        self.category_id = category_id
        self.name = name
        self.description = description
        self.parent_id = parent_id
        self.children = children or []
        self.item_count = 0
    
    def to_dict(self):
        return {
            "category_id": self.category_id,
            "name": self.name,
            "description": self.description,
            "parent_id": self.parent_id,
            "children": self.children,
            "item_count": self.item_count
        }

class KnowledgeBase:
    """知识库"""
    
    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.items: Dict[str, KnowledgeItem] = {}
        self.categories: Dict[str, KnowledgeCategory] = {}
        self.tag_index: Dict[str, List[str]] = {}
        self.search_index = {}
        
    def add_category(self, category: KnowledgeCategory):
        """添加分类"""
        self.categories[category.category_id] = category
        
        # 更新父分类的子分类列表
        if category.parent_id and category.parent_id in self.categories:
            self.categories[category.parent_id].children.append(category.category_id)
    
    def add_item(self, item: KnowledgeItem):
        """添加知识条目"""
        self.items[item.item_id] = item
        
        # 更新分类计数
        if item.category in self.categories:
            self.categories[item.category].item_count += 1
        
        # 更新标签索引
        for tag in item.tags:
            if tag not in self.tag_index:
                self.tag_index[tag] = []
            self.tag_index[tag].append(item.item_id)
        
        # 构建搜索索引
        self._build_search_index(item)
    
    def _build_search_index(self, item: KnowledgeItem):
        """构建搜索索引"""
        text = f"{item.title} {item.content}"
        words = self._extract_keywords(text)
        
        for word in words:
            if word not in self.search_index:
                self.search_index[word] = []
            self.search_index[word].append(item.item_id)
    
    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        # 移除标点符号
        text = re.sub(r'[^\w\s]', '', text)
        words = text.split()
        # 过滤短词和常见词
        common_words = {"的", "是", "在", "有", "和", "了", "他", "她", "它", "我", "你", "他"}
        return [w for w in words if len(w) >= 2 and w not in common_words]
    
    def search(self, query: str) -> List[Tuple[str, float]]:
        """搜索知识条目"""
        keywords = self._extract_keywords(query)
        scores = {}
        
        for keyword in keywords:
            if keyword in self.search_index:
                for item_id in self.search_index[keyword]:
                    if item_id not in scores:
                        scores[item_id] = 0
                    scores[item_id] += 1
        
        # 按分数排序
        results = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return results[:20]
    
    def search_by_tag(self, tag: str) -> List[str]:
        """按标签搜索"""
        return self.tag_index.get(tag, [])
    
    def search_by_category(self, category_id: str) -> List[str]:
        """按分类搜索"""
        results = []
        
        def collect_items(cat_id: str):
            for item_id, item in self.items.items():
                if item.category == cat_id:
                    results.append(item_id)
            if cat_id in self.categories:
                for child in self.categories[cat_id].children:
                    collect_items(child)
        
        collect_items(category_id)
        return results
    
    def get_item(self, item_id: str) -> Optional[KnowledgeItem]:
        """获取知识条目"""
        item = self.items.get(item_id)
        if item:
            item.access_count += 1
        return item
    
    def delete_item(self, item_id: str):
        """删除知识条目"""
        if item_id in self.items:
            item = self.items[item_id]
            
            # 更新分类计数
            if item.category in self.categories:
                self.categories[item.category].item_count -= 1
            
            # 更新标签索引
            for tag in item.tags:
                if tag in self.tag_index:
                    self.tag_index[tag].remove(item_id)
            
            del self.items[item_id]
    
    def update_item(self, item_id: str, **kwargs):
        """更新知识条目"""
        if item_id in self.items:
            item = self.items[item_id]
            
            if 'title' in kwargs:
                item.title = kwargs['title']
            if 'content' in kwargs:
                item.content = kwargs['content']
            if 'category' in kwargs:
                # 更新旧分类计数
                if item.category in self.categories:
                    self.categories[item.category].item_count -= 1
                item.category = kwargs['category']
                # 更新新分类计数
                if item.category in self.categories:
                    self.categories[item.category].item_count += 1
            if 'tags' in kwargs:
                # 移除旧标签
                for tag in item.tags:
                    if tag in self.tag_index:
                        self.tag_index[tag].remove(item_id)
                item.tags = kwargs['tags']
                # 添加新标签
                for tag in item.tags:
                    if tag not in self.tag_index:
                        self.tag_index[tag] = []
                    self.tag_index[tag].append(item_id)
            
            item.updated_at = datetime.now()
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            "total_items": len(self.items),
            "total_categories": len(self.categories),
            "total_tags": len(self.tag_index),
            "items_per_category": {cat_id: cat.item_count for cat_id, cat in self.categories.items()},
            "top_tags": sorted(self.tag_index.items(), key=lambda x: len(x[1]), reverse=True)[:10]
        }

class KnowledgeBaseLoader:
    """知识库加载器"""
    
    @staticmethod
    def load_from_directory(directory: str) -> KnowledgeBase:
        """从目录加载知识库"""
        kb = KnowledgeBase(name=os.path.basename(directory))
        
        # 加载分类
        categories_file = os.path.join(directory, "categories.json")
        if os.path.exists(categories_file):
            with open(categories_file, 'r', encoding='utf-8') as f:
                categories_data = json.load(f)
                for cat_data in categories_data:
                    category = KnowledgeCategory(
                        category_id=cat_data['category_id'],
                        name=cat_data['name'],
                        description=cat_data.get('description', ''),
                        parent_id=cat_data.get('parent_id'),
                        children=cat_data.get('children', [])
                    )
                    kb.add_category(category)
        
        # 加载知识条目
        items_dir = os.path.join(directory, "items")
        if os.path.exists(items_dir):
            for filename in os.listdir(items_dir):
                if filename.endswith('.json'):
                    filepath = os.path.join(items_dir, filename)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            item_data = json.load(f)
                            item = KnowledgeItem(
                                item_id=item_data['item_id'],
                                title=item_data['title'],
                                content=item_data['content'],
                                category=item_data['category'],
                                tags=item_data.get('tags', []),
                                source=item_data.get('source', 'file'),
                                created_at=datetime.fromisoformat(item_data.get('created_at', datetime.now().isoformat())),
                                updated_at=datetime.fromisoformat(item_data.get('updated_at', datetime.now().isoformat()))
                            )
                            kb.add_item(item)
                    except Exception as e:
                        print(f"加载知识条目失败 {filename}: {e}")
        
        return kb
    
    @staticmethod
    def load_from_markdown(directory: str) -> KnowledgeBase:
        """从Markdown文件加载知识库"""
        kb = KnowledgeBase(name=os.path.basename(directory))
        
        # 创建默认分类
        default_category = KnowledgeCategory(
            category_id="default",
            name="默认分类",
            description="默认知识分类"
        )
        kb.add_category(default_category)
        
        # 遍历Markdown文件
        for root, dirs, files in os.walk(directory):
            for filename in files:
                if filename.endswith('.md'):
                    filepath = os.path.join(root, filename)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # 从文件名提取标题
                        title = os.path.splitext(filename)[0]
                        
                        # 提取标签（从文件内容中的标签行）
                        tags = []
                        for line in content.split('\n')[:20]:
                            if line.startswith('tags:'):
                                tags = [t.strip() for t in line[5:].split(',')]
                                break
                        
                        item = KnowledgeItem(
                            item_id=filename,
                            title=title,
                            content=content,
                            category="default",
                            tags=tags,
                            source=f"markdown:{filepath}"
                        )
                        kb.add_item(item)
                    except Exception as e:
                        print(f"加载Markdown文件失败 {filename}: {e}")
        
        return kb

class KnowledgeBaseManager:
    """知识库管理器"""
    
    def __init__(self):
        self.knowledge_bases: Dict[str, KnowledgeBase] = {}
        self.active_kb: str = None
    
    def load_knowledge_base(self, name: str, directory: str):
        """加载知识库"""
        kb = KnowledgeBaseLoader.load_from_markdown(directory)
        kb.name = name
        self.knowledge_bases[name] = kb
        
        if not self.active_kb:
            self.active_kb = name
    
    def set_active_kb(self, name: str):
        """设置活动知识库"""
        if name in self.knowledge_bases:
            self.active_kb = name
            return True
        return False
    
    def search(self, query: str, kb_name: str = None) -> List[Tuple[str, float]]:
        """搜索知识"""
        target_kb = self.knowledge_bases.get(kb_name or self.active_kb)
        if target_kb:
            return target_kb.search(query)
        return []
    
    def get_item(self, item_id: str, kb_name: str = None) -> Optional[KnowledgeItem]:
        """获取知识条目"""
        target_kb = self.knowledge_bases.get(kb_name or self.active_kb)
        if target_kb:
            return target_kb.get_item(item_id)
        return None
    
    def get_all_kb_names(self) -> List[str]:
        """获取所有知识库名称"""
        return list(self.knowledge_bases.keys())
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        stats = {}
        for name, kb in self.knowledge_bases.items():
            stats[name] = kb.get_statistics()
        return stats

if __name__ == "__main__":
    print("="*60)
    print("🚀 NWACS V8.0 知识库管理系统测试")
    print("="*60)
    
    kb_manager = KnowledgeBaseManager()
    
    print("\n1. 加载学习知识库...")
    kb_manager.load_knowledge_base("学习知识库", "skills/level2/learnings")
    print(f"✅ 知识库加载完成")
    
    print("\n2. 获取知识库列表...")
    kb_names = kb_manager.get_all_kb_names()
    print(f"已加载知识库: {kb_names}")
    
    print("\n3. 获取统计信息...")
    stats = kb_manager.get_statistics()
    for kb_name, kb_stats in stats.items():
        print(f"   - {kb_name}: {kb_stats['total_items']} 条知识")
    
    print("\n4. 测试搜索功能...")
    results = kb_manager.search("写作技巧")
    print(f"✅ 搜索 '写作技巧' 找到 {len(results)} 条结果")
    
    print("\n5. 测试获取知识条目...")
    # 获取第一条搜索结果
    if results:
        item_id = results[0][0]
        item = kb_manager.get_item(item_id)
        if item:
            print(f"   - 标题: {item.title}")
            print(f"   - 分类: {item.category}")
            print(f"   - 标签: {item.tags}")
    
    print("\n" + "="*60)
    print("🎉 知识库管理系统测试完成！")
    print("="*60)
