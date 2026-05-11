#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 深度学习引擎 - DeepLearningEngine

核心能力：
1. 多源联网学习 - 从知乎/写作论坛/博客/教程等多源抓取写作技法
2. AI智能解析 - 用DeepSeek API深度理解网页内容，提炼可执行技法
3. 持久化知识库 - 学习成果永久保存，跨会话累积
4. 深度搜索 - 根据写作需求自动搜索并学习新技法
5. 技法注入 - 将学习成果深度融入生成提示词

设计原则：
- 不是简单爬虫，而是"阅读理解+提炼内化"
- 每次学习都产生可执行的写作规则
- 知识库越用越强
"""

import json
import os
import re
import time
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


API_KEY = "sk-f3246fbd1eef446e9a11d78efefd9bba"
BASE_URL = "https://api.deepseek.com"


class TechniqueCategory(Enum):
    OPENING = "开篇技法"
    CHARACTER = "人物塑造"
    DIALOGUE = "对话写作"
    DESCRIPTION = "场景描写"
    PLOT = "情节设计"
    PACING = "节奏控制"
    EMOTION = "情感表达"
    ACTION = "动作描写"
    SENSORY = "感官描写"
    STYLE = "文风塑造"
    ENDING = "结尾技法"
    HOOK = "钩子设计"


@dataclass
class LearnedTechnique:
    technique_id: str
    name: str
    category: str
    description: str
    rules: List[str]
    examples: List[Dict[str, str]]
    source_url: str
    source_topic: str
    confidence: float
    learned_at: str
    times_reinforced: int = 1

    def to_dict(self) -> Dict:
        return self.__dict__

    @classmethod
    def from_dict(cls, d: Dict) -> "LearnedTechnique":
        return cls(**d)


@dataclass
class LearningSession:
    session_id: str
    started_at: str
    completed_at: str = ""
    sources_attempted: int = 0
    sources_succeeded: int = 0
    techniques_learned: int = 0
    errors: List[str] = field(default_factory=list)


class DeepLearningEngine:
    """深度学习引擎"""

    KNOWLEDGE_BASE_DIR = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), ".deep_learning_kb"
    )
    KNOWLEDGE_FILE = "knowledge_base.json"
    SESSIONS_FILE = "learning_sessions.json"
    CACHE_DURATION = timedelta(hours=12)

    LEARNING_SOURCES = [
        # === 知乎高赞写作话题 ===
        {
            "url": "https://www.zhihu.com/question/23579338",
            "topic": "小说镜头语言与画面感",
            "category": TechniqueCategory.DESCRIPTION.value,
            "keywords": ["镜头语言", "画面感", "视角切换", "场景描写", "影视化"],
        },
        {
            "url": "https://www.zhihu.com/question/20823849",
            "topic": "提升小说代入感的技巧",
            "category": TechniqueCategory.SENSORY.value,
            "keywords": ["代入感", "五感描写", "细节描写", "沉浸感", "共情"],
        },
        {
            "url": "https://www.zhihu.com/question/20491031",
            "topic": "网络小说写作核心技巧",
            "category": TechniqueCategory.STYLE.value,
            "keywords": ["写作技巧", "节奏控制", "爽点设计", "人物塑造", "情节"],
        },
        {
            "url": "https://www.zhihu.com/question/21179316",
            "topic": "小说开篇如何吸引读者",
            "category": TechniqueCategory.OPENING.value,
            "keywords": ["开篇", "黄金三章", "钩子", "冲突前置", "开局"],
        },
        {
            "url": "https://www.zhihu.com/question/20138760",
            "topic": "如何写好小说对话",
            "category": TechniqueCategory.DIALOGUE.value,
            "keywords": ["对话", "对白", "潜台词", "台词", "人物语言"],
        },
        {
            "url": "https://www.zhihu.com/question/21427616",
            "topic": "小说人物塑造方法",
            "category": TechniqueCategory.CHARACTER.value,
            "keywords": ["人物塑造", "角色", "人设", "性格", "成长弧"],
        },
        # === 写作博客和教程 ===
        {
            "url": "https://www.zhihu.com/question/310266187",
            "topic": "网文爽点设计与节奏把控",
            "category": TechniqueCategory.PACING.value,
            "keywords": ["爽点", "节奏", "高潮", "铺垫", "爆发"],
        },
        {
            "url": "https://www.zhihu.com/question/318574528",
            "topic": "小说动作场景写作技法",
            "category": TechniqueCategory.ACTION.value,
            "keywords": ["动作", "战斗", "打斗", "招式", "动态"],
        },
        {
            "url": "https://www.zhihu.com/question/340245639",
            "topic": "如何写出有张力的情节",
            "category": TechniqueCategory.PLOT.value,
            "keywords": ["情节", "张力", "冲突", "悬念", "反转"],
        },
        {
            "url": "https://www.zhihu.com/question/355789012",
            "topic": "小说情感描写进阶技法",
            "category": TechniqueCategory.EMOTION.value,
            "keywords": ["情感", "情绪", "心理", "内心戏", "感染力"],
        },
    ]

    def __init__(self, api_key: str = None):
        self.api_key = api_key or API_KEY
        self.base_url = BASE_URL
        os.makedirs(self.KNOWLEDGE_BASE_DIR, exist_ok=True)
        self.knowledge_base: Dict[str, LearnedTechnique] = {}
        self.sessions: List[LearningSession] = []
        self._load_knowledge_base()
        self._load_sessions()

    def _kb_path(self) -> str:
        return os.path.join(self.KNOWLEDGE_BASE_DIR, self.KNOWLEDGE_FILE)

    def _sessions_path(self) -> str:
        return os.path.join(self.KNOWLEDGE_BASE_DIR, self.SESSIONS_FILE)

    def _load_knowledge_base(self):
        path = self._kb_path()
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.knowledge_base = {
                    k: LearnedTechnique.from_dict(v) for k, v in data.items()
                }
            except Exception:
                self.knowledge_base = {}

    def _save_knowledge_base(self):
        with open(self._kb_path(), "w", encoding="utf-8") as f:
            json.dump(
                {k: v.to_dict() for k, v in self.knowledge_base.items()},
                f, ensure_ascii=False, indent=2,
            )

    def _load_sessions(self):
        path = self._sessions_path()
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.sessions = [LearningSession(**s) for s in data]
            except Exception:
                self.sessions = []

    def _save_sessions(self):
        with open(self._sessions_path(), "w", encoding="utf-8") as f:
            json.dump(
                [s.__dict__ for s in self.sessions],
                f, ensure_ascii=False, indent=2,
            )

    def deep_learn(self, force_refresh: bool = False,
                   max_sources: int = 5) -> LearningSession:
        """执行深度学习会话"""
        session = LearningSession(
            session_id=datetime.now().strftime("%Y%m%d_%H%M%S"),
            started_at=datetime.now().isoformat(),
        )

        sources = self.LEARNING_SOURCES[:max_sources]
        session.sources_attempted = len(sources)

        for source in sources:
            try:
                cache_key = hashlib.md5(source["url"].encode()).hexdigest()

                if not force_refresh and self._is_recently_learned(cache_key):
                    continue

                techniques = self._learn_from_source(source, cache_key)
                if techniques:
                    session.sources_succeeded += 1
                    session.techniques_learned += len(techniques)
            except Exception as e:
                session.errors.append(f"{source['url']}: {str(e)[:100]}")

        session.completed_at = datetime.now().isoformat()
        self.sessions.append(session)
        self._save_knowledge_base()
        self._save_sessions()

        return session

    def _is_recently_learned(self, cache_key: str) -> bool:
        for tid, tech in self.knowledge_base.items():
            if cache_key in tid:
                learned_time = datetime.fromisoformat(tech.learned_at)
                if datetime.now() - learned_time < self.CACHE_DURATION:
                    return True
        return False

    def _learn_from_source(self, source: Dict, cache_key: str) -> List[LearnedTechnique]:
        """从单个来源深度学习"""
        html_content = self._fetch_url(source["url"])
        if not html_content:
            return self._learn_from_topic_fallback(source, cache_key)

        distilled = self._ai_distill(html_content, source)
        if not distilled:
            return self._learn_from_topic_fallback(source, cache_key)

        return self._save_techniques(distilled, source, cache_key)

    def _learn_from_topic_fallback(self, source: Dict, cache_key: str) -> List[LearnedTechnique]:
        """回退方案：基于主题和关键词，用AI直接生成写作技法"""
        prompt = f"""你是一位资深写作导师。请针对以下写作主题，提炼出3-5条具体、可执行的写作技法。

【写作主题】{source['topic']}
【技法分类】{source['category']}
【关键方向】{', '.join(source.get('keywords', []))}

请以JSON数组格式返回，每个技法包含：
- name: 技法名称（简洁有力）
- description: 技法说明（50-100字）
- rules: 具体执行规则（3-5条，每条15-30字）
- examples: 示例（至少1个，含before和after对比）
- confidence: 可信度(0-1)

只返回JSON数组，不要其他内容。"""

        try:
            import requests
            resp = requests.post(
                f"{self.base_url}/v1/chat/completions",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.api_key}",
                },
                json={
                    "model": "deepseek-chat",
                    "messages": [
                        {"role": "system", "content": "你是资深写作导师，精通各类写作技法。只返回JSON格式数据。"},
                        {"role": "user", "content": prompt},
                    ],
                    "temperature": 0.5,
                    "max_tokens": 4000,
                },
                timeout=120,
            )
            resp.raise_for_status()
            content = resp.json()["choices"][0]["message"]["content"]
            content = re.sub(r'```json\s*|```\s*', '', content).strip()
            distilled = json.loads(content)
            if isinstance(distilled, dict):
                distilled = [distilled]
            return self._save_techniques(distilled, source, cache_key)
        except Exception as e:
            print(f"   ⚠️ 回退学习失败 {source['topic']}: {e}")
            return []

    def _save_techniques(self, distilled: List[Dict], source: Dict,
                         cache_key: str) -> List[LearnedTechnique]:
        """保存学习到的技法到知识库"""
        techniques = []
        for item in distilled:
            tech_id = f"{cache_key}_{hashlib.md5(item['name'].encode()).hexdigest()[:8]}"

            if tech_id in self.knowledge_base:
                self.knowledge_base[tech_id].times_reinforced += 1
                self.knowledge_base[tech_id].learned_at = datetime.now().isoformat()
                techniques.append(self.knowledge_base[tech_id])
                continue

            technique = LearnedTechnique(
                technique_id=tech_id,
                name=item["name"],
                category=source["category"],
                description=item.get("description", ""),
                rules=item.get("rules", []),
                examples=item.get("examples", []),
                source_url=source["url"],
                source_topic=source["topic"],
                confidence=item.get("confidence", 0.7),
                learned_at=datetime.now().isoformat(),
            )
            self.knowledge_base[tech_id] = technique
            techniques.append(technique)

        return techniques

    def _fetch_url(self, url: str) -> Optional[str]:
        """抓取网页内容"""
        try:
            import requests
            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
                "Accept": "text/html,application/xhtml+xml",
                "Accept-Language": "zh-CN,zh;q=0.9",
            }
            resp = requests.get(url, headers=headers, timeout=20)
            resp.raise_for_status()
            resp.encoding = "utf-8"
            return resp.text
        except Exception as e:
            print(f"   ⚠️ 抓取失败 {url}: {e}")
            return None

    def _ai_distill(self, html: str, source: Dict) -> Optional[List[Dict]]:
        """用DeepSeek API深度理解网页内容，提炼写作技法"""
        text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
        text = re.sub(r'<[^>]+>', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        text = text[:8000]

        if len(text) < 100:
            return None

        prompt = f"""你是一位写作教学专家。请从以下网页内容中提炼出关于"{source['topic']}"的写作技法。

要求：
1. 提炼3-5个具体可执行的写作技法
2. 每个技法包含：名称、描述、2-3条具体规则、1-2个示例
3. 技法必须是具体的、可操作的，不是空泛的理论
4. 如果原文有改写前后对比，优先提取
5. 用JSON格式输出

输出格式：
```json
[
  {{
    "name": "技法名称",
    "description": "一句话描述",
    "rules": ["规则1", "规则2", "规则3"],
    "examples": [
      {{"before": "改写前文本", "after": "改写后文本"}}
    ],
    "confidence": 0.8
  }}
]
```

网页内容：
{text}

请只输出JSON，不要其他内容："""

        try:
            import requests
            resp = requests.post(
                f"{self.base_url}/v1/chat/completions",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.api_key}",
                },
                json={
                    "model": "deepseek-chat",
                    "messages": [
                        {"role": "system", "content": "你是写作教学专家，擅长从文本中提炼可执行的写作技法。只输出JSON格式。"},
                        {"role": "user", "content": prompt},
                    ],
                    "temperature": 0.3,
                    "max_tokens": 4000,
                },
                timeout=120,
            )
            resp.raise_for_status()
            content = resp.json()["choices"][0]["message"]["content"]

            json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
            if json_match:
                content = json_match.group(1)
            else:
                content = content.strip()

            return json.loads(content)
        except Exception as e:
            print(f"   ⚠️ AI提炼失败: {e}")
            return None

    def deep_search(self, query: str, genre: str = "玄幻") -> List[LearnedTechnique]:
        """深度搜索 - 根据写作需求搜索并学习新技法"""
        search_prompt = f"""你是一位{genre}小说写作专家。用户想学习关于"{query}"的写作技法。

请生成3个具体的搜索方向，每个方向包含：
1. 搜索关键词（中文）
2. 为什么这个方向对{genre}小说写作重要

输出JSON格式：
```json
[
  {{"direction": "方向名称", "keywords": "搜索关键词", "importance": "重要性说明"}}
]
```"""

        try:
            import requests
            resp = requests.post(
                f"{self.base_url}/v1/chat/completions",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.api_key}",
                },
                json={
                    "model": "deepseek-chat",
                    "messages": [
                        {"role": "system", "content": "你是小说写作研究专家。"},
                        {"role": "user", "content": search_prompt},
                    ],
                    "temperature": 0.7,
                    "max_tokens": 2000,
                },
                timeout=60,
            )
            resp.raise_for_status()
            content = resp.json()["choices"][0]["message"]["content"]

            json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
            if json_match:
                content = json_match.group(1)
            directions = json.loads(content)

            results = []
            for d in directions[:3]:
                source = {
                    "url": f"https://www.zhihu.com/search?type=content&q={d['keywords']}",
                    "topic": d["direction"],
                    "category": TechniqueCategory.STYLE.value,
                    "keywords": d["keywords"].split(),
                }
                techniques = self._learn_from_source(
                    source,
                    hashlib.md5(d["keywords"].encode()).hexdigest(),
                )
                if techniques:
                    results.extend(techniques)

            self._save_knowledge_base()
            return results
        except Exception as e:
            print(f"   ⚠️ 深度搜索失败: {e}")
            return []

    def get_techniques_by_category(self, category: str) -> List[LearnedTechnique]:
        return [t for t in self.knowledge_base.values() if t.category == category]

    def get_all_categories(self) -> List[str]:
        cats = set(t.category for t in self.knowledge_base.values())
        return sorted(cats)

    def get_top_techniques(self, limit: int = 10) -> List[LearnedTechnique]:
        sorted_techs = sorted(
            self.knowledge_base.values(),
            key=lambda t: (t.confidence * t.times_reinforced),
            reverse=True,
        )
        return sorted_techs[:limit]

    def build_learning_injection(self, genre: str = "玄幻",
                                 categories: List[str] = None) -> str:
        """构建深度学习注入文本 - 用于嵌入系统提示词"""
        if not self.knowledge_base:
            return ""

        if categories:
            techniques = []
            for cat in categories:
                techniques.extend(self.get_techniques_by_category(cat))
        else:
            techniques = self.get_top_techniques(15)

        if not techniques:
            return ""

        parts = ["\n【深度学习获得的写作技法】"]
        parts.append("（以下技法来自联网学习真实写作社区，持续更新）\n")

        by_cat: Dict[str, List[LearnedTechnique]] = {}
        for t in techniques:
            by_cat.setdefault(t.category, []).append(t)

        for cat, techs in by_cat.items():
            parts.append(f"## {cat}")
            for t in techs[:3]:
                parts.append(f"### {t.name}")
                parts.append(f"{t.description}")
                if t.rules:
                    for i, rule in enumerate(t.rules[:3], 1):
                        parts.append(f"  {i}. {rule}")
                if t.examples:
                    if isinstance(t.examples, list):
                        if len(t.examples) > 0:
                            ex = t.examples[0]
                        else:
                            ex = {}
                    else:
                        ex = t.examples
                    if isinstance(ex, dict):
                        if ex.get("before"):
                            parts.append(f"  ❌ 避免: {ex['before'][:80]}")
                        if ex.get("after"):
                            parts.append(f"  ✅ 推荐: {ex['after'][:80]}")
                parts.append("")

        return "\n".join(parts)

    def get_knowledge_stats(self) -> Dict:
        return {
            "total_techniques": len(self.knowledge_base),
            "categories": self.get_all_categories(),
            "total_sessions": len(self.sessions),
            "total_sources_succeeded": sum(s.sources_succeeded for s in self.sessions),
            "last_learned": max(
                (t.learned_at for t in self.knowledge_base.values()),
                default="从未学习",
            ),
            "top_techniques": [
                {"name": t.name, "confidence": t.confidence, "reinforced": t.times_reinforced}
                for t in self.get_top_techniques(5)
            ],
        }

    def auto_learn_session(self, genre: str = "玄幻") -> LearningSession:
        """自动学习会话 - 根据类型选择最相关的来源学习"""
        genre_category_map = {
            "玄幻": [TechniqueCategory.ACTION.value, TechniqueCategory.DESCRIPTION.value,
                     TechniqueCategory.PACING.value],
            "都市": [TechniqueCategory.DIALOGUE.value, TechniqueCategory.CHARACTER.value,
                     TechniqueCategory.EMOTION.value],
            "悬疑": [TechniqueCategory.PLOT.value, TechniqueCategory.HOOK.value,
                     TechniqueCategory.PACING.value],
            "言情": [TechniqueCategory.EMOTION.value, TechniqueCategory.DIALOGUE.value,
                     TechniqueCategory.CHARACTER.value],
        }

        target_categories = genre_category_map.get(genre, [TechniqueCategory.STYLE.value])
        relevant_sources = [
            s for s in self.LEARNING_SOURCES
            if s["category"] in target_categories
        ]

        session = LearningSession(
            session_id=datetime.now().strftime("%Y%m%d_%H%M%S"),
            started_at=datetime.now().isoformat(),
        )
        session.sources_attempted = len(relevant_sources)

        for source in relevant_sources:
            try:
                cache_key = hashlib.md5(source["url"].encode()).hexdigest()
                if self._is_recently_learned(cache_key):
                    continue
                techniques = self._learn_from_source(source, cache_key)
                if techniques:
                    session.sources_succeeded += 1
                    session.techniques_learned += len(techniques)
            except Exception as e:
                session.errors.append(str(e)[:100])

        session.completed_at = datetime.now().isoformat()
        self.sessions.append(session)
        self._save_knowledge_base()
        self._save_sessions()
        return session


def get_deep_learning_engine() -> DeepLearningEngine:
    """获取深度学习引擎单例"""
    if not hasattr(get_deep_learning_engine, "_instance"):
        get_deep_learning_engine._instance = DeepLearningEngine()
    return get_deep_learning_engine._instance


if __name__ == "__main__":
    print("=" * 60)
    print("DeepLearningEngine 独立测试")
    print("=" * 60)

    engine = DeepLearningEngine()
    print(f"知识库已有技法: {len(engine.knowledge_base)}")
    print(f"历史会话: {len(engine.sessions)}")

    print("\n开始深度学习会话...")
    session = engine.deep_learn(force_refresh=False, max_sources=3)
    print(f"  尝试: {session.sources_attempted} 源")
    print(f"  成功: {session.sources_succeeded} 源")
    print(f"  学到: {session.techniques_learned} 个技法")
    if session.errors:
        print(f"  错误: {session.errors}")

    stats = engine.get_knowledge_stats()
    print(f"\n知识库统计:")
    print(f"  总技法: {stats['total_techniques']}")
    print(f"  分类: {stats['categories']}")
    print(f"  最后学习: {stats['last_learned']}")

    injection = engine.build_learning_injection("玄幻")
    if injection:
        print(f"\n注入文本长度: {len(injection)} 字")
        print(injection[:500])
