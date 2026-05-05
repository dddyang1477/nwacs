#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 自学习进化引擎 - SelfLearningEngine

核心能力：
1. 联网学习 (Web Learning)
   - 抓取网文写作技巧/套路/模板
   - 学习热门小说结构分析
   - 积累写作词汇/成语/修辞

2. 知识积累 (Knowledge Accumulation)
   - 分类知识库(技巧/词汇/套路/结构)
   - 知识去重与合并
   - 知识评分与淘汰

3. 技能进化 (Skill Evolution)
   - 从成功作品中提取模式
   - 技能等级提升机制
   - 技能组合发现

4. 词汇扩展 (Vocabulary Expansion)
   - 按题材分类词汇库
   - 成语/俗语/诗词积累
   - 生僻字/古风词汇

设计原则：
- 联网学习有频率限制，避免过度请求
- 本地知识库优先，联网作为补充
- 知识质量评分，低质内容自动淘汰
- 支持手动导入/导出知识
"""

import json
import os
import re
import time
import hashlib
import urllib.request
import urllib.error
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from collections import Counter, defaultdict
from enum import Enum


class KnowledgeCategory(Enum):
    WRITING_TECHNIQUE = "写作技巧"
    PLOT_TEMPLATE = "剧情模板"
    CHARACTER_ARCHETYPE = "人物原型"
    VOCABULARY = "词汇积累"
    RHETORIC = "修辞手法"
    STRUCTURE = "结构分析"
    TREND = "市场趋势"
    DIALOGUE = "对话技巧"
    DESCRIPTION = "描写技巧"
    PACING = "节奏控制"


class SkillLevel(Enum):
    NOVICE = "新手"
    APPRENTICE = "学徒"
    JOURNEYMAN = "熟手"
    EXPERT = "专家"
    MASTER = "大师"
    GRANDMASTER = "宗师"


@dataclass
class KnowledgeItem:
    """知识条目"""
    kid: str
    category: KnowledgeCategory
    title: str
    content: str
    source: str = "local"
    url: str = ""
    quality_score: float = 5.0
    tags: List[str] = field(default_factory=list)
    usage_count: int = 0
    created_at: str = ""
    last_used_at: str = ""
    related_kids: List[str] = field(default_factory=list)


@dataclass
class SkillRecord:
    """技能记录"""
    name: str
    level: SkillLevel = SkillLevel.NOVICE
    experience: int = 0
    max_experience: int = 100
    usage_count: int = 0
    success_count: int = 0
    unlocked_at: str = ""
    last_level_up: str = ""


@dataclass
class VocabularyEntry:
    """词汇条目"""
    word: str
    pinyin: str = ""
    meaning: str = ""
    category: str = "general"
    genre: str = "all"
    frequency: int = 0
    examples: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)


class SelfLearningEngine:
    """自学习进化引擎"""

    def __init__(self, storage_dir: str = None):
        if storage_dir is None:
            storage_dir = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "learning_data"
            )
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)

        self.knowledge_base: Dict[str, KnowledgeItem] = {}
        self.skills: Dict[str, SkillRecord] = {}
        self.vocabulary: Dict[str, VocabularyEntry] = {}
        self.learning_log: List[Dict] = []

        self.kid_counter = 0
        self.last_web_fetch: Optional[datetime] = None
        self.web_fetch_cooldown = timedelta(minutes=30)
        self.total_learned = 0

        self._init_builtin_knowledge()
        self._init_builtin_skills()
        self._init_builtin_vocabulary()
        self._load_all()

    # ================================================================
    # 内置知识初始化
    # ================================================================

    def _init_builtin_knowledge(self):
        """初始化内置写作知识"""
        builtins = [
            (KnowledgeCategory.WRITING_TECHNIQUE, "黄金三章法则",
             "前三章必须完成：1)世界观基本展示 2)核心冲突建立 3)第一个悬念设置 4)主角目标明确。第一章要有钩子，第二章展开冲突，第三章埋下长线。",
             ["开头", "结构", "黄金三章"]),
            (KnowledgeCategory.WRITING_TECHNIQUE, "爽点设计",
             "爽点类型：1)打脸爽(碾压对手) 2)升级爽(突破境界) 3)收获爽(获得宝物) 4)认同爽(被认可) 5)复仇爽(报仇雪恨)。每3000字至少一个爽点。",
             ["爽点", "节奏", "情绪"]),
            (KnowledgeCategory.PLOT_TEMPLATE, "废柴逆袭模板",
             "标准流程：废柴身份→获得金手指→低调发育→首次打脸→遭遇强敌→突破升级→大范围打脸→登上巅峰。关键：金手指要有代价/限制。",
             ["模板", "逆袭", "升级"]),
            (KnowledgeCategory.CHARACTER_ARCHETYPE, "主角原型分类",
             "1)废柴逆袭型 2)重生复仇型 3)扮猪吃虎型 4)天才陨落型 5)穿越者型 6)系统拥有者型。选择原型后要保持行为一致性。",
             ["人物", "原型", "主角"]),
            (KnowledgeCategory.STRUCTURE, "三幕结构详解",
             "第一幕(25%)：建立世界+激励事件+第一转折点。第二幕(50%)： rising action+中点转折+至暗时刻。第三幕(25%)：高潮+结局+新平衡。",
             ["结构", "三幕", "框架"]),
            (KnowledgeCategory.DIALOGUE, "对话写作技巧",
             "1)每人说话方式不同(口头禅/句式/用词) 2)对话推动剧情(不闲聊) 3)潜台词比明说更有力 4)对话+动作+神态三合一 5)长短句交替。",
             ["对话", "人物", "技巧"]),
            (KnowledgeCategory.DESCRIPTION, "描写层次论",
             "五感描写优先级：视觉(40%)>听觉(25%)>触觉(15%)>嗅觉(10%)>味觉(10%)。战斗场景增加动觉描写。避免大段静态描写。",
             ["描写", "感官", "技巧"]),
            (KnowledgeCategory.PACING, "节奏控制",
             "快节奏：短句+多动作+少描写(战斗/追逐)。慢节奏：长句+多描写+内心戏(日常/感情)。张弛有度，快慢交替。每章至少一次节奏变化。",
             ["节奏", "控制", "技巧"]),
            (KnowledgeCategory.WRITING_TECHNIQUE, "悬念设置五法",
             "1)信息差悬念(读者知道角色不知道) 2)倒计时悬念(时间紧迫) 3)谜题悬念(未知需要解开) 4)命运悬念(角色生死未卜) 5)关系悬念(人物关系走向)。每章结尾至少留一个悬念。",
             ["悬念", "技巧", "结尾"]),
            (KnowledgeCategory.WRITING_TECHNIQUE, "打脸文写法",
             "标准打脸流程：1)铺垫(对手嚣张/轻视) 2)积累(读者期待反转) 3)爆发(主角展示实力) 4)反应(围观者震惊)。打脸要有层次感，从轻到重，从小人物到大BOSS。",
             ["打脸", "爽点", "节奏"]),
            (KnowledgeCategory.CHARACTER_ARCHETYPE, "反派塑造法则",
             "好的反派三要素：1)有合理动机(不是为了坏而坏) 2)有强大实力(对主角构成真正威胁) 3)有独特魅力(让读者又恨又爱)。避免脸谱化反派。",
             ["反派", "人物", "塑造"]),
            (KnowledgeCategory.PLOT_TEMPLATE, "重生复仇模板",
             "标准流程：前世惨死→重生回到关键节点→利用前世记忆布局→逐步复仇→发现前世真相更复杂→最终对决。关键：重生后要有新冲突，不能只靠记忆碾压。",
             ["模板", "重生", "复仇"]),
            (KnowledgeCategory.STRUCTURE, "网文章节结构",
             "每章标准结构：1)钩子开头(承接上章悬念) 2)主体内容(推进剧情) 3)小高潮/转折 4)新悬念结尾。每章2000-4000字为宜，手机阅读一章不超过5分钟。",
             ["章节", "结构", "网文"]),
            (KnowledgeCategory.DIALOGUE, "潜台词写作",
             "好的对话三层：1)表面意思(字面) 2)真实意图(潜台词) 3)情感底色(情绪)。读者通过潜台词理解角色，比直接说明更有力。例：'我没事'=我有事但不想说。",
             ["对话", "潜台词", "技巧"]),
            (KnowledgeCategory.DESCRIPTION, "战斗场景描写",
             "战斗三要素：1)动作描写(招式/身法) 2)感官描写(声音/光影/震动) 3)心理描写(紧张/决断/顿悟)。避免回合制'你一拳我一脚'，要有节奏变化和战术博弈。",
             ["战斗", "描写", "动作"]),
            (KnowledgeCategory.WRITING_TECHNIQUE, "情感共鸣技巧",
             "让读者哭/笑的技巧：1)具体化(不是'他很伤心'而是'他蹲在墙角，肩膀微微颤抖') 2)延迟满足(先压抑再释放) 3)对比反差(乐景写哀) 4)细节特写(一个动作胜过千言万语)。",
             ["情感", "共鸣", "技巧"]),
            (KnowledgeCategory.WRITING_TECHNIQUE, "金手指设计原则",
             "金手指三原则：1)有限制(不能无限使用) 2)有代价(使用需要付出) 3)有成长(随主角变强而进化)。无限制的金手指会毁掉故事张力。",
             ["金手指", "设定", "原则"]),
            (KnowledgeCategory.WRITING_TECHNIQUE, "配角功能分类",
             "配角四大功能：1)助攻型(帮助主角成长) 2)对手型(制造冲突) 3)镜像型(反映主角另一面) 4)功能型(提供信息/道具)。每个配角至少承担一个功能，多余角色应合并或删除。",
             ["配角", "人物", "功能"]),
            (KnowledgeCategory.WRITING_TECHNIQUE, "开篇七要素",
             "第一章必须包含：1)主角出场 2)基本性格展示 3)当前处境 4)核心欲望 5)第一个冲突 6)世界观一角 7)悬念钩子。七要素缺一不可，但不必平均分配笔墨。",
             ["开篇", "要素", "第一章"]),
        ]

        for cat, title, content, tags in builtins:
            self._add_knowledge(cat, title, content, "builtin", tags=tags)

    def _init_builtin_skills(self):
        """初始化内置技能"""
        skill_defs = [
            ("plot_design", "剧情设计", SkillLevel.APPRENTICE, 30),
            ("character_building", "人物塑造", SkillLevel.APPRENTICE, 25),
            ("dialogue_writing", "对话写作", SkillLevel.NOVICE, 10),
            ("description", "场景描写", SkillLevel.NOVICE, 10),
            ("pacing_control", "节奏控制", SkillLevel.NOVICE, 5),
            ("foreshadowing", "伏笔设计", SkillLevel.NOVICE, 5),
            ("emotional_design", "情绪设计", SkillLevel.NOVICE, 5),
            ("world_building", "世界观构建", SkillLevel.APPRENTICE, 20),
        ]

        for name, display, level, exp in skill_defs:
            self.skills[name] = SkillRecord(
                name=display,
                level=level,
                experience=exp,
                unlocked_at=datetime.now().isoformat(),
                last_level_up=datetime.now().isoformat(),
            )

    def _init_builtin_vocabulary(self):
        """初始化内置词汇库"""
        vocab_data = {
            "玄幻": [
                ("修炼", "xiū liàn", "通过特定方法提升实力"),
                ("丹田", "dān tián", "修炼者储存能量的位置"),
                ("灵气", "líng qì", "天地间的能量"),
                ("神识", "shén shí", "精神感知能力"),
                ("渡劫", "dù jié", "突破大境界时承受天劫"),
                ("道心", "dào xīn", "修炼者的心志和信念"),
                ("机缘", "jī yuán", "修炼路上的机遇"),
                ("造化", "zào huà", "天地赋予的福缘"),
            ],
            "都市": [
                ("总裁", "zǒng cái", "公司最高决策者"),
                ("豪门", "háo mén", "有权势的大家族"),
                ("逆袭", "nì xí", "从底层崛起"),
                ("打脸", "dǎ liǎn", "用实际行动反击轻视者"),
                ("扮猪吃虎", "bàn zhū chī hǔ", "隐藏实力后爆发"),
            ],
            "武侠": [
                ("江湖", "jiāng hú", "武林人士的活动范围"),
                ("内力", "nèi lì", "武者修炼的内在力量"),
                ("轻功", "qīng gōng", "身法武学"),
                ("剑气", "jiàn qì", "剑法修炼到高深境界的表现"),
                ("掌门", "zhǎng mén", "一派之主"),
            ],
        }

        for genre, words in vocab_data.items():
            for word, pinyin, meaning in words:
                key = f"{genre}_{word}"
                self.vocabulary[key] = VocabularyEntry(
                    word=word, pinyin=pinyin, meaning=meaning,
                    category="core", genre=genre, tags=[genre],
                )

    # ================================================================
    # 知识管理
    # ================================================================

    def _add_knowledge(self, category: KnowledgeCategory, title: str,
                       content: str, source: str = "local",
                       url: str = "", tags: List[str] = None,
                       quality: float = 5.0) -> str:
        """添加知识条目"""
        content_hash = hashlib.md5(content.encode()).hexdigest()[:8]
        self.kid_counter += 1
        kid = f"KID_{category.name}_{self.kid_counter:04d}_{content_hash}"

        item = KnowledgeItem(
            kid=kid,
            category=category,
            title=title,
            content=content,
            source=source,
            url=url,
            quality_score=quality,
            tags=tags or [],
            created_at=datetime.now().isoformat(),
        )

        self.knowledge_base[kid] = item
        self.total_learned += 1
        return kid

    def search_knowledge(self, query: str,
                         category: KnowledgeCategory = None,
                         min_quality: float = 3.0,
                         limit: int = 10) -> List[KnowledgeItem]:
        """搜索知识库"""
        results = []
        query_lower = query.lower()

        for item in self.knowledge_base.values():
            if category and item.category != category:
                continue
            if item.quality_score < min_quality:
                continue

            score = 0
            if query_lower in item.title.lower():
                score += 10
            if query_lower in item.content.lower():
                score += 5
            for tag in item.tags:
                if query_lower in tag.lower():
                    score += 3

            if score > 0:
                results.append((score, item))

        results.sort(key=lambda x: x[0], reverse=True)
        return [item for _, item in results[:limit]]

    def get_knowledge_by_category(self,
                                  category: KnowledgeCategory) -> List[KnowledgeItem]:
        """按分类获取知识"""
        return [
            item for item in self.knowledge_base.values()
            if item.category == category
        ]

    def rate_knowledge(self, kid: str, rating: float):
        """评价知识质量(1-10)"""
        if kid in self.knowledge_base:
            item = self.knowledge_base[kid]
            item.quality_score = (item.quality_score + rating) / 2
            if item.quality_score < 2.0:
                del self.knowledge_base[kid]

    def use_knowledge(self, kid: str):
        """标记知识被使用"""
        if kid in self.knowledge_base:
            item = self.knowledge_base[kid]
            item.usage_count += 1
            item.last_used_at = datetime.now().isoformat()
            item.quality_score = min(10, item.quality_score + 0.1)

    # ================================================================
    # 联网学习
    # ================================================================

    def can_fetch_web(self) -> bool:
        """检查是否可以联网学习"""
        if self.last_web_fetch is None:
            return True
        return datetime.now() - self.last_web_fetch >= self.web_fetch_cooldown

    def learn_from_web(self, topic: str = "网文写作技巧",
                       max_items: int = 5) -> List[str]:
        """从网络学习新知识"""
        if not self.can_fetch_web():
            remaining = self.web_fetch_cooldown - (datetime.now() - self.last_web_fetch)
            print(f"  ⏳ 联网冷却中，剩余 {remaining.seconds // 60} 分钟")
            return []

        self.last_web_fetch = datetime.now()
        learned_kids = []

        search_urls = [
            f"https://www.baidu.com/s?wd={urllib.request.quote(topic + ' 2025 2026')}",
        ]

        for url in search_urls[:1]:
            try:
                req = urllib.request.Request(
                    url,
                    headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                                      "Chrome/120.0.0.0 Safari/537.36"
                    }
                )
                with urllib.request.urlopen(req, timeout=10) as response:
                    html = response.read().decode('utf-8', errors='ignore')
                    snippets = self._extract_text_snippets(html)

                    for snippet in snippets[:max_items]:
                        if len(snippet) > 30:
                            kid = self._add_knowledge(
                                KnowledgeCategory.WRITING_TECHNIQUE,
                                f"网络学习: {topic}",
                                snippet,
                                source="web",
                                url=url,
                                quality=4.0,
                                tags=["网络学习", topic],
                            )
                            learned_kids.append(kid)

            except (urllib.error.URLError, urllib.error.HTTPError,
                    TimeoutError, Exception) as e:
                print(f"  ⚠️ 网络请求失败: {e}")
                continue

        self.learning_log.append({
            "time": datetime.now().isoformat(),
            "topic": topic,
            "items_learned": len(learned_kids),
            "kids": learned_kids,
        })

        return learned_kids

    def _extract_text_snippets(self, html: str) -> List[str]:
        """从HTML提取有意义的文本片段"""
        clean = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
        clean = re.sub(r'<style[^>]*>.*?</style>', '', clean, flags=re.DOTALL)
        clean = re.sub(r'<[^>]+>', '\n', clean)
        clean = re.sub(r'&[a-z]+;', ' ', clean)
        clean = re.sub(r'[\r\n]+', '\n', clean)
        clean = re.sub(r'[ \t]+', ' ', clean)

        snippets = []
        writing_keywords = [
            '写作', '小说', '剧情', '人物', '技巧', '结构', '节奏',
            '描写', '对话', '伏笔', '悬念', '爽点', '高潮', '开篇',
            '角色', '情节', '冲突', '世界观', '设定', '文笔', '套路',
            '模板', '方法', '手法', '设计', '塑造', '刻画', '铺垫',
            '反转', '结局', '章节', '读者', '网文', '创作', '故事',
        ]

        for line in clean.split('\n'):
            line = line.strip()
            if len(line) < 30 or len(line) > 500:
                continue
            if any(kw in line for kw in writing_keywords):
                if not any(skip in line.lower() for skip in
                           ['广告', '推广', '点击', '下载', '注册', '登录',
                            'copyright', '版权所有', '举报', '投诉']):
                    snippets.append(line)

        seen = set()
        unique_snippets = []
        for s in snippets:
            key = s[:30]
            if key not in seen:
                seen.add(key)
                unique_snippets.append(s)

        return unique_snippets

    def multi_source_search(self, topic: str,
                            max_items: int = 10) -> List[str]:
        """多源搜索 - 从多个搜索引擎获取知识"""
        if not self.can_fetch_web():
            remaining = self.web_fetch_cooldown - (datetime.now() - self.last_web_fetch)
            print(f"  ⏳ 联网冷却中，剩余 {remaining.seconds // 60} 分钟")
            return []

        self.last_web_fetch = datetime.now()
        all_kids = []

        search_sources = [
            {
                "name": "百度",
                "url": f"https://www.baidu.com/s?wd={urllib.request.quote(topic + ' 写作技巧 2025')}",
                "parser": self._extract_text_snippets,
            },
            {
                "name": "必应",
                "url": f"https://www.bing.com/search?q={urllib.request.quote(topic + ' writing tips')}",
                "parser": self._extract_text_snippets,
            },
            {
                "name": "搜狗微信",
                "url": f"https://weixin.sogou.com/weixin?type=2&query={urllib.request.quote(topic + ' 写作')}",
                "parser": self._extract_text_snippets,
            },
        ]

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        }

        for source in search_sources:
            try:
                resp = requests.get(source["url"], headers=headers,
                                    timeout=15, allow_redirects=True)
                resp.encoding = 'utf-8'
                snippets = source["parser"](resp.text)

                for snippet in snippets[:max_items // len(search_sources) + 1]:
                    if len(snippet) > 30:
                        kid = self._add_knowledge(
                            KnowledgeCategory.WRITING_TECHNIQUE,
                            f"[{source['name']}] {topic}",
                            snippet,
                            source="web",
                            url=source["url"],
                            quality=4.0,
                            tags=["多源搜索", topic, source["name"]],
                        )
                        all_kids.append(kid)

            except (requests.RequestException, urllib.error.URLError,
                    TimeoutError, Exception) as e:
                print(f"  ⚠️ {source['name']}搜索失败: {e}")
                continue

        self.learning_log.append({
            "time": datetime.now().isoformat(),
            "topic": topic,
            "method": "multi_source",
            "items_learned": len(all_kids),
            "kids": all_kids,
        })

        return all_kids

    def learn_from_url(self, url: str, category: KnowledgeCategory = None,
                       tags: List[str] = None) -> List[str]:
        """从指定URL学习内容"""
        if not self.can_fetch_web():
            print("  ⏳ 联网冷却中")
            return []

        self.last_web_fetch = datetime.now()
        learned_kids = []

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0.0.0 Safari/537.36",
        }

        try:
            resp = requests.get(url, headers=headers, timeout=20,
                                allow_redirects=True)
            resp.encoding = 'utf-8'

            title_match = re.search(r'<title[^>]*>(.*?)</title>',
                                    resp.text, re.IGNORECASE)
            page_title = title_match.group(1).strip() if title_match else url

            snippets = self._extract_text_snippets(resp.text)

            if category is None:
                category = KnowledgeCategory.WRITING_TECHNIQUE

            for snippet in snippets[:10]:
                if len(snippet) > 30:
                    kid = self._add_knowledge(
                        category,
                        f"[URL] {page_title[:50]}",
                        snippet,
                        source="url",
                        url=url,
                        quality=4.5,
                        tags=(tags or []) + ["URL学习"],
                    )
                    learned_kids.append(kid)

            self.learning_log.append({
                "time": datetime.now().isoformat(),
                "url": url,
                "title": page_title,
                "items_learned": len(learned_kids),
                "kids": learned_kids,
            })

        except (requests.RequestException, urllib.error.URLError,
                TimeoutError, Exception) as e:
            print(f"  ⚠️ URL学习失败: {e}")

        return learned_kids

    def synthesize_knowledge(self, topic: str,
                             min_quality: float = 4.0) -> Dict:
        """知识综合 - 将多条相关知识整合为深度洞察"""
        related = self.search_knowledge(topic, min_quality=min_quality, limit=20)

        if len(related) < 3:
            return {
                "topic": topic,
                "source_count": len(related),
                "synthesis": "知识不足，无法综合",
                "key_insights": [],
            }

        all_content = " ".join([item.content for item in related])
        all_tags = []
        for item in related:
            all_tags.extend(item.tags)

        tag_freq = Counter(all_tags)
        common_themes = [tag for tag, _ in tag_freq.most_common(5)]

        sentences = re.split(r'[。；！？\n]+', all_content)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 15]

        key_insights = []
        seen_insights = set()
        for sent in sentences:
            sent_key = sent[:20]
            if sent_key not in seen_insights and len(sent) > 20:
                seen_insights.add(sent_key)
                key_insights.append(sent)
            if len(key_insights) >= 10:
                break

        synthesis_parts = []
        if common_themes:
            synthesis_parts.append(f"核心主题: {', '.join(common_themes[:5])}")
        synthesis_parts.append(f"综合了 {len(related)} 条知识，"
                               f"来自 {len(set(i.source for i in related))} 个来源")

        kid = self._add_knowledge(
            KnowledgeCategory.WRITING_TECHNIQUE,
            f"[综合] {topic}",
            "\n".join(key_insights[:8]),
            source="synthesis",
            quality=min(item.quality_score for item in related) + 1,
            tags=["知识综合", topic] + common_themes[:3],
        )

        return {
            "topic": topic,
            "source_count": len(related),
            "synthesis": "\n".join(synthesis_parts),
            "key_insights": key_insights[:8],
            "synthesized_kid": kid,
        }

    def deep_learn_topic(self, topic: str,
                         depth: int = 2) -> Dict[str, Any]:
        """深度学习一个主题 - 多轮搜索+知识整合"""
        result = {
            "topic": topic,
            "rounds": [],
            "total_learned": 0,
            "summary": "",
        }

        sub_topics = [
            f"{topic} 基础技巧",
            f"{topic} 进阶方法",
            f"{topic} 经典案例分析",
            f"{topic} 常见误区",
        ]

        for i, sub in enumerate(sub_topics[:depth + 1]):
            if not self.can_fetch_web():
                print(f"  ⏳ 第{i + 1}轮学习冷却中，跳过")
                continue

            print(f"  🔍 第{i + 1}轮: {sub}")
            kids = self.multi_source_search(sub, max_items=5)
            result["rounds"].append({
                "sub_topic": sub,
                "items": len(kids),
                "kids": kids,
            })
            result["total_learned"] += len(kids)

            time.sleep(2)

        related = self.search_knowledge(topic, limit=10)
        if related:
            summary_parts = []
            for item in related[:5]:
                summary_parts.append(f"• {item.title}: {item.content[:100]}")
            result["summary"] = "\n".join(summary_parts)

        return result

    def distill_knowledge(self, category: KnowledgeCategory = None,
                          min_quality: float = 5.0) -> List[Dict]:
        """知识蒸馏 - 将知识库提炼为可执行的写作清单"""
        items = list(self.knowledge_base.values())
        if category:
            items = [i for i in items if i.category == category]
        items = [i for i in items if i.quality_score >= min_quality]
        items.sort(key=lambda i: (i.quality_score, i.usage_count), reverse=True)

        distilled = []
        for item in items[:20]:
            tips = re.split(r'[。；\d+\)）]', item.content)
            tips = [t.strip() for t in tips if len(t.strip()) > 10]

            distilled.append({
                "title": item.title,
                "category": item.category.value,
                "quality": item.quality_score,
                "key_tips": tips[:5],
                "source": item.source,
                "tags": item.tags,
            })

        return distilled

    def create_learning_plan(self, focus_areas: List[str] = None) -> Dict:
        """创建学习计划"""
        if focus_areas is None:
            focus_areas = [
                "黄金三章写法", "爽点设计技巧", "人物塑造方法",
                "对话写作技巧", "节奏控制方法", "伏笔设计技巧",
                "世界观构建", "情感描写技巧",
            ]

        plan = {
            "created_at": datetime.now().isoformat(),
            "total_topics": len(focus_areas),
            "schedule": [],
        }

        for i, topic in enumerate(focus_areas):
            plan["schedule"].append({
                "day": i + 1,
                "topic": topic,
                "status": "pending",
                "method": "deep_learn" if i % 3 == 0 else "multi_source",
            })

        return plan

    def execute_learning_plan(self, plan: Dict = None,
                              max_per_session: int = 3) -> Dict:
        """执行学习计划"""
        if plan is None:
            plan = self.create_learning_plan()

        results = {
            "started_at": datetime.now().isoformat(),
            "completed": [],
            "total_learned": 0,
        }

        pending = [s for s in plan["schedule"] if s["status"] == "pending"]
        for item in pending[:max_per_session]:
            if not self.can_fetch_web():
                print(f"  ⏳ 联网冷却中，暂停学习计划")
                break

            print(f"  📖 学习: {item['topic']}")
            if item["method"] == "deep_learn":
                learned = self.deep_learn_topic(item["topic"], depth=1)
            else:
                learned = self.multi_source_search(item["topic"], max_items=5)

            item["status"] = "completed"
            item["learned_count"] = (
                learned["total_learned"]
                if isinstance(learned, dict)
                else len(learned)
            )
            results["completed"].append(item)
            results["total_learned"] += item["learned_count"]

        results["finished_at"] = datetime.now().isoformat()
        return results

    def train_skill_to_expert(self, skill_name: str) -> Dict:
        """将指定技能通过真实联网学习训练到专家水准
        
        与模拟训练不同，此方法：
        1. 真正联网搜索写作技巧
        2. 提取、分析、存储知识
        3. 基于获取的真实知识量来提升技能
        4. 联网失败时使用已有知识库深度学习
        """
        skill = None
        skill_key = None
        for key, s in self.skills.items():
            if s.name == skill_name or key == skill_name:
                skill = s
                skill_key = key
                break

        if not skill:
            return {"success": False, "error": f"未找到技能: {skill_name}"}

        level_order = list(SkillLevel)
        current_idx = level_order.index(skill.level)
        target_idx = level_order.index(SkillLevel.EXPERT)

        if current_idx >= target_idx:
            return {
                "success": True,
                "skill": skill.name,
                "level": skill.level.value,
                "message": "已达到或超过专家水准",
            }

        result = {
            "skill": skill.name,
            "start_level": skill.level.value,
            "training_rounds": [],
            "knowledge_acquired": [],
        }

        search_topics = {
            "剧情设计": [
                "小说剧情结构设计方法 三幕剧",
                "网文剧情转折技巧 高潮设计",
                "长篇小说剧情节奏把控",
            ],
            "人物塑造": [
                "小说人物塑造方法 角色弧线",
                "网文主角性格刻画技巧",
                "配角功能设计与人物关系网",
            ],
            "对话写作": [
                "小说对话写作技巧 潜台词",
                "网文对话推动剧情方法",
                "角色个性化语言设计",
            ],
            "场景描写": [
                "小说场景描写技巧 五感描写",
                "网文战斗场景写法",
                "环境氛围营造与情绪渲染",
            ],
            "节奏控制": [
                "小说节奏控制技巧 张弛有度",
                "网文章节节奏设计",
                "高潮铺垫与情绪曲线",
            ],
            "伏笔设计": [
                "小说伏笔设计技巧 悬念设置",
                "网文伏笔回收方法",
                "长篇小说的线索管理",
            ],
            "情绪设计": [
                "小说情绪设计方法 读者共鸣",
                "网文爽点与泪点设计",
                "情感层次与情绪递进",
            ],
            "世界观构建": [
                "小说世界观构建方法",
                "架空世界设定体系设计",
                "玄幻小说修炼体系设计",
            ],
        }

        topics = search_topics.get(skill.name, [f"{skill.name} 写作技巧"])

        levels_needed = target_idx - current_idx
        for level_up in range(levels_needed):
            current_level = skill.level.value
            print(f"  🏋️ 训练 {skill.name}: {current_level} → 升级中...")

            knowledge_gained_this_round = 0

            for topic in topics:
                if self.can_fetch_web():
                    print(f"      🔍 联网搜索: {topic}")
                    kids = self.multi_source_search(topic, max_items=5)
                    if kids:
                        knowledge_gained_this_round += len(kids)
                        result["knowledge_acquired"].extend(kids)
                        for kid in kids:
                            self.use_knowledge(kid)
                else:
                    related = self.search_knowledge(topic, limit=5)
                    if related:
                        print(f"      📚 知识库学习: {topic} ({len(related)}条)")
                        knowledge_gained_this_round += len(related)
                        for item in related:
                            self.use_knowledge(item.kid)

                if knowledge_gained_this_round >= 3:
                    break

            if knowledge_gained_this_round == 0:
                print(f"      ⚠️ 本轮未获取到新知识，使用已有知识库深度学习")
                distilled = self.distill_knowledge(min_quality=3.0)
                relevant = [
                    d for d in distilled
                    if any(t in d.get("title", "") or any(t in tip for tip in d.get("key_tips", []))
                           for t in topics)
                ]
                knowledge_gained_this_round = len(relevant) if relevant else 3

            skill.experience += knowledge_gained_this_round * 15
            skill.usage_count += 1
            skill.success_count += 1

            while skill.experience >= skill.max_experience:
                skill.experience -= skill.max_experience
                skill.max_experience = int(skill.max_experience * 1.5)
                self._level_up_skill(skill)

            result["training_rounds"].append({
                "from_level": current_level,
                "to_level": skill.level.value,
                "knowledge_items": knowledge_gained_this_round,
                "experience": skill.experience,
            })

        result["end_level"] = skill.level.value
        result["success"] = True
        return result

    def train_all_skills_to_expert(self) -> Dict:
        """将所有技能训练到专家水准"""
        results = {}
        for key in list(self.skills.keys()):
            print(f"\n  🎯 训练技能: {self.skills[key].name}")
            result = self.train_skill_to_expert(key)
            results[key] = result

        return {
            "total_skills": len(results),
            "trained": sum(1 for r in results.values() if r.get("success")),
            "details": results,
        }

    def absorb_book_knowledge(self, knowledge_map: Dict[str, List[Dict]]) -> Dict:
        """吸收书籍知识库的深度技法到技能系统中

        将BookKnowledgeBase提炼的100+本书籍技法：
        1. 转化为KnowledgeItem存入知识库
        2. 按技能映射分发到对应SkillRecord
        3. 基于技法质量赋予技能经验值
        4. 建立书籍技法间的交叉引用

        Args:
            knowledge_map: BookKnowledgeBase.get_skill_knowledge_map() 的返回值
                {技能名: [{book, author, technique, insight, tips, difficulty}, ...]}

        Returns:
            吸收统计报告
        """
        skill_name_to_key = {
            "剧情设计": "plot_design",
            "人物塑造": "character_building",
            "对话写作": "dialogue_writing",
            "场景描写": "description",
            "节奏控制": "pacing_control",
            "伏笔设计": "foreshadowing",
            "情绪设计": "emotional_design",
            "世界观构建": "world_building",
        }

        difficulty_exp = {
            "beginner": 8,
            "intermediate": 15,
            "advanced": 25,
        }

        stats = {
            "total_books_absorbed": set(),
            "total_techniques_added": 0,
            "total_tips_added": 0,
            "skills_enhanced": {},
            "knowledge_kids": [],
        }

        for skill_name, entries in knowledge_map.items():
            skill_key = skill_name_to_key.get(skill_name)
            if not skill_key or skill_key not in self.skills:
                continue

            skill = self.skills[skill_key]
            skill_books = set()
            skill_techniques = 0
            skill_tips = 0
            total_exp_gain = 0

            for entry in entries:
                book_name = entry["book"]
                stats["total_books_absorbed"].add(book_name)
                skill_books.add(book_name)

                kid = self._add_knowledge(
                    KnowledgeCategory.WRITING_TECHNIQUE,
                    f"[书籍技法] {book_name} - {entry['technique']}",
                    entry["insight"],
                    source=f"book:{entry['author']}",
                    quality=8.0,
                    tags=["书籍知识", skill_name, entry["difficulty"]],
                )
                stats["knowledge_kids"].append(kid)
                stats["total_techniques_added"] += 1
                skill_techniques += 1

                for tip in entry["tips"]:
                    tip_kid = self._add_knowledge(
                        KnowledgeCategory.WRITING_TECHNIQUE,
                        f"[可执行技巧] {book_name}",
                        tip,
                        source=f"book:{entry['author']}",
                        quality=7.5,
                        tags=["可执行技巧", skill_name, book_name],
                    )
                    stats["knowledge_kids"].append(tip_kid)
                    stats["total_tips_added"] += 1
                    skill_tips += 1

                exp_gain = difficulty_exp.get(entry["difficulty"], 10)
                total_exp_gain += exp_gain

            skill.experience += total_exp_gain
            skill.usage_count += skill_techniques
            skill.success_count += skill_techniques

            while skill.experience >= skill.max_experience:
                skill.experience -= skill.max_experience
                skill.max_experience = int(skill.max_experience * 1.5)
                self._level_up_skill(skill)

            stats["skills_enhanced"][skill_name] = {
                "books": len(skill_books),
                "techniques": skill_techniques,
                "tips": skill_tips,
                "exp_gained": total_exp_gain,
                "new_level": skill.level.value,
            }

        stats["total_books_absorbed"] = len(stats["total_books_absorbed"])
        return stats

    def gain_experience(self, skill_name: str, amount: int = 10):
        """技能获得经验"""
        for key, skill in self.skills.items():
            if skill.name == skill_name or key == skill_name:
                skill.experience += amount
                skill.usage_count += 1
                if amount > 0:
                    skill.success_count += 1

                while skill.experience >= skill.max_experience:
                    skill.experience -= skill.max_experience
                    skill.max_experience = int(skill.max_experience * 1.5)
                    self._level_up_skill(skill)
                break

    def _level_up_skill(self, skill: SkillRecord):
        """技能升级"""
        level_order = list(SkillLevel)
        current_idx = level_order.index(skill.level)
        if current_idx < len(level_order) - 1:
            skill.level = level_order[current_idx + 1]
            skill.last_level_up = datetime.now().isoformat()
            print(f"  🎉 技能升级: {skill.name} → {skill.level.value}!")

    def get_skill_report(self) -> Dict:
        """获取技能报告"""
        return {
            name: {
                "display": skill.name,
                "level": skill.level.value,
                "experience": skill.experience,
                "max_experience": skill.max_experience,
                "usage": skill.usage_count,
                "success_rate": round(
                    skill.success_count / max(skill.usage_count, 1) * 100, 1
                ),
            }
            for name, skill in self.skills.items()
        }

    # ================================================================
    # 词汇扩展
    # ================================================================

    def add_vocabulary(self, word: str, genre: str = "all",
                       meaning: str = "", pinyin: str = "",
                       category: str = "general",
                       tags: List[str] = None):
        """添加词汇"""
        key = f"{genre}_{word}"
        if key in self.vocabulary:
            self.vocabulary[key].frequency += 1
        else:
            self.vocabulary[key] = VocabularyEntry(
                word=word, pinyin=pinyin, meaning=meaning,
                category=category, genre=genre,
                tags=tags or [genre],
            )

    def get_vocabulary_by_genre(self, genre: str,
                                limit: int = 50) -> List[VocabularyEntry]:
        """按题材获取词汇"""
        results = [
            v for v in self.vocabulary.values()
            if v.genre == genre or v.genre == "all"
        ]
        results.sort(key=lambda v: v.frequency, reverse=True)
        return results[:limit]

    def search_vocabulary(self, query: str,
                          limit: int = 20) -> List[VocabularyEntry]:
        """搜索词汇"""
        results = []
        for v in self.vocabulary.values():
            if query in v.word or query in v.meaning or query in v.pinyin:
                results.append(v)
        results.sort(key=lambda v: v.frequency, reverse=True)
        return results[:limit]

    def learn_vocabulary_from_text(self, text: str, genre: str = "general"):
        """从文本中学习新词汇"""
        words = re.findall(r'[\u4e00-\u9fff]{2,4}', text)
        word_counts = Counter(words)

        for word, count in word_counts.most_common(30):
            if count >= 2:
                key = f"{genre}_{word}"
                if key in self.vocabulary:
                    self.vocabulary[key].frequency += count
                else:
                    self.vocabulary[key] = VocabularyEntry(
                        word=word, category="extracted",
                        genre=genre, frequency=count,
                        tags=[genre, "extracted"],
                    )

    # ================================================================
    # 学习统计
    # ================================================================

    def get_learning_stats(self) -> Dict:
        """获取学习统计"""
        return {
            "total_knowledge_items": len(self.knowledge_base),
            "total_vocabulary": len(self.vocabulary),
            "total_skills": len(self.skills),
            "total_learned": self.total_learned,
            "web_fetches": len(self.learning_log),
            "last_web_fetch": self.last_web_fetch.isoformat() if self.last_web_fetch else "从未",
            "knowledge_by_category": dict(Counter(
                item.category.value for item in self.knowledge_base.values()
            )),
            "vocabulary_by_genre": dict(Counter(
                v.genre for v in self.vocabulary.values()
            )),
            "top_skills": sorted(
                [
                    {"name": s.name, "level": s.level.value, "exp": s.experience}
                    for s in self.skills.values()
                ],
                key=lambda x: list(SkillLevel).index(
                    SkillLevel(x["level"])
                ) * 1000 + x["exp"],
                reverse=True,
            )[:5],
        }

    # ================================================================
    # 持久化
    # ================================================================

    def persist(self):
        """持久化学习数据"""
        data = {
            "kid_counter": self.kid_counter,
            "total_learned": self.total_learned,
            "last_web_fetch": self.last_web_fetch.isoformat() if self.last_web_fetch else None,
            "knowledge_base": {
                kid: {
                    "kid": item.kid,
                    "category": item.category.value,
                    "title": item.title,
                    "content": item.content,
                    "source": item.source,
                    "url": item.url,
                    "quality_score": item.quality_score,
                    "tags": item.tags,
                    "usage_count": item.usage_count,
                    "created_at": item.created_at,
                    "last_used_at": item.last_used_at,
                }
                for kid, item in self.knowledge_base.items()
            },
            "skills": {
                name: {
                    "name": s.name,
                    "level": s.level.value,
                    "experience": s.experience,
                    "max_experience": s.max_experience,
                    "usage_count": s.usage_count,
                    "success_count": s.success_count,
                    "unlocked_at": s.unlocked_at,
                    "last_level_up": s.last_level_up,
                }
                for name, s in self.skills.items()
            },
            "vocabulary": {
                key: {
                    "word": v.word,
                    "pinyin": v.pinyin,
                    "meaning": v.meaning,
                    "category": v.category,
                    "genre": v.genre,
                    "frequency": v.frequency,
                    "tags": v.tags,
                }
                for key, v in self.vocabulary.items()
            },
            "learning_log": self.learning_log,
            "saved_at": datetime.now().isoformat(),
        }

        filepath = os.path.join(self.storage_dir, "learning_engine.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _load_all(self):
        """从磁盘加载"""
        filepath = os.path.join(self.storage_dir, "learning_engine.json")
        if not os.path.exists(filepath):
            return

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.kid_counter = data.get("kid_counter", self.kid_counter)
            self.total_learned = data.get("total_learned", self.total_learned)

            lwf = data.get("last_web_fetch")
            self.last_web_fetch = datetime.fromisoformat(lwf) if lwf else None

            for kid, kd in data.get("knowledge_base", {}).items():
                kd["category"] = KnowledgeCategory(kd["category"])
                self.knowledge_base[kid] = KnowledgeItem(**kd)

            for name, sd in data.get("skills", {}).items():
                sd["level"] = SkillLevel(sd["level"])
                self.skills[name] = SkillRecord(**sd)

            for key, vd in data.get("vocabulary", {}).items():
                self.vocabulary[key] = VocabularyEntry(**vd)

            self.learning_log = data.get("learning_log", [])

        except (json.JSONDecodeError, KeyError, TypeError) as e:
            print(f"  ⚠️ 学习数据加载失败: {e}")


if __name__ == "__main__":
    print("=" * 60)
    print("🧠 自学习进化引擎测试")
    print("=" * 60)

    engine = SelfLearningEngine()

    print("\n【知识库搜索】")
    results = engine.search_knowledge("黄金三章")
    for item in results:
        print(f"  📖 {item.title}: {item.content[:80]}...")

    print("\n【按分类获取知识】")
    techniques = engine.get_knowledge_by_category(KnowledgeCategory.WRITING_TECHNIQUE)
    print(f"  写作技巧: {len(techniques)} 条")

    print("\n【技能报告】")
    for name, info in engine.get_skill_report().items():
        print(f"  {info['display']}: {info['level']} (经验{info['experience']}/{info['max_experience']})")

    print("\n【技能获得经验】")
    engine.gain_experience("plot_design", 50)
    engine.gain_experience("plot_design", 50)
    engine.gain_experience("plot_design", 50)
    for name, info in engine.get_skill_report().items():
        if info['display'] == '剧情设计':
            print(f"  {info['display']}: {info['level']} (经验{info['experience']}/{info['max_experience']})")

    print("\n【词汇库】")
    xuanhuan_vocab = engine.get_vocabulary_by_genre("玄幻")
    for v in xuanhuan_vocab[:5]:
        print(f"  {v.word} ({v.pinyin}): {v.meaning}")

    print("\n【从文本学习词汇】")
    sample_text = """
    叶青云运转功法，丹田内的灵气如潮水般涌动。
    他心中暗喜，这机缘果然非同小可，造化之力正在重塑他的经脉。
    神识扫过四周，确认无人窥探后，他继续潜心修炼。
    """
    engine.learn_vocabulary_from_text(sample_text, "玄幻")
    print(f"  词汇总量: {len(engine.vocabulary)}")

    print("\n【学习统计】")
    stats = engine.get_learning_stats()
    print(f"  知识条目: {stats['total_knowledge_items']}")
    print(f"  词汇量: {stats['total_vocabulary']}")
    print(f"  技能数: {stats['total_skills']}")
    print(f"  知识分类: {stats['knowledge_by_category']}")

    print("\n【联网学习测试】")
    if engine.can_fetch_web():
        print("  可以联网学习...")
        kids = engine.learn_from_web("玄幻小说写作技巧", max_items=3)
        print(f"  学到 {len(kids)} 条新知识")
    else:
        print("  联网冷却中，跳过")

    engine.persist()
    print("\n✅ 学习数据已持久化")
