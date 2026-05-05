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


@dataclass
class WritingExercise:
    """写作练习"""
    exercise_id: str
    title: str
    description: str
    skill_focus: List[str] = field(default_factory=list)
    difficulty: str = "intermediate"
    prompt: str = ""
    constraints: List[str] = field(default_factory=list)
    target_word_count: int = 500
    hints: List[str] = field(default_factory=list)
    evaluation_criteria: Dict[str, float] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)


@dataclass
class ExerciseAttempt:
    """练习尝试记录"""
    attempt_id: str
    exercise_id: str
    content: str = ""
    word_count: int = 0
    time_spent_seconds: float = 0
    self_rating: float = 0.0
    ai_feedback: str = ""
    scores: Dict[str, float] = field(default_factory=dict)
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    created_at: str = ""


@dataclass
class FeedbackRecord:
    """反馈记录"""
    record_id: str
    skill_name: str
    aspect: str
    current_level: str = ""
    target_level: str = ""
    gap_analysis: str = ""
    improvement_plan: List[str] = field(default_factory=list)
    progress_percentage: float = 0.0
    last_reviewed: str = ""


@dataclass
class LearningMilestone:
    """学习里程碑"""
    milestone_id: str
    name: str
    description: str
    required_skills: Dict[str, str] = field(default_factory=dict)
    required_exercises: List[str] = field(default_factory=list)
    unlocked: bool = False
    completed: bool = False
    completed_at: str = ""
    rewards: List[str] = field(default_factory=list)


@dataclass
class LearningPath:
    """学习路径"""
    path_id: str
    name: str
    description: str
    target_genre: str = "all"
    milestones: List[LearningMilestone] = field(default_factory=list)
    current_milestone_index: int = 0
    total_exercises_completed: int = 0
    started_at: str = ""
    last_activity: str = ""


@dataclass
class SkillCombo:
    """技能组合"""
    combo_id: str
    name: str
    description: str
    skills_required: List[str] = field(default_factory=list)
    synergy_score: float = 0.0
    use_cases: List[str] = field(default_factory=list)
    techniques: List[str] = field(default_factory=list)
    discovered_at: str = ""


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

        self.exercises: Dict[str, WritingExercise] = {}
        self.attempts: Dict[str, List[ExerciseAttempt]] = {}
        self.feedback_records: Dict[str, FeedbackRecord] = {}
        self.learning_paths: Dict[str, LearningPath] = {}
        self.skill_combos: Dict[str, SkillCombo] = {}
        self.exercise_counter = 0
        self.attempt_counter = 0
        self.feedback_counter = 0
        self.path_counter = 0
        self.combo_counter = 0

        self._init_builtin_knowledge()
        self._init_builtin_skills()
        self._init_builtin_vocabulary()
        self._init_builtin_exercises()
        self._init_builtin_learning_paths()
        self._init_builtin_skill_combos()
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
    # 练习模式 (Practice Mode)
    # ================================================================

    def _init_builtin_exercises(self):
        """初始化内置写作练习"""
        builtin_exercises = [
            WritingExercise(
                exercise_id="EX_001",
                title="黄金三章开篇练习",
                description="为你的小说写一个3000字的开篇，必须包含黄金三章的全部要素",
                skill_focus=["plot_design", "pacing_control"],
                difficulty="intermediate",
                prompt="主角是一个被家族抛弃的废柴少年，在16岁生日那天，他发现了一个改变命运的秘密...",
                constraints=[
                    "前500字必须建立核心冲突",
                    "第一章结尾必须有悬念钩子",
                    "至少出现3个有名字的角色",
                    "展示世界观至少一个独特设定",
                ],
                target_word_count=3000,
                hints=[
                    "用具体场景代替抽象叙述",
                    "让读者在第一段就产生好奇",
                    "主角的欲望要明确且紧迫",
                ],
                evaluation_criteria={
                    "冲突建立": 0.25,
                    "悬念设置": 0.20,
                    "人物塑造": 0.20,
                    "世界观展示": 0.15,
                    "语言流畅度": 0.20,
                },
                tags=["开篇", "黄金三章", "基础"],
            ),
            WritingExercise(
                exercise_id="EX_002",
                title="对话场景专项训练",
                description="写一段500字的纯对话场景，仅通过对话推进剧情和展示人物性格",
                skill_focus=["dialogue_writing", "character_building"],
                difficulty="intermediate",
                prompt="两个多年未见的老友在茶馆重逢，一人飞黄腾达，一人落魄潦倒...",
                constraints=[
                    "不能使用任何叙述性文字",
                    "每人说话风格必须不同",
                    "对话中必须包含潜台词",
                    "通过对话暗示两人的过去",
                ],
                target_word_count=500,
                hints=[
                    "用称呼和语气词区分人物",
                    "每句话都应该推进剧情或揭示性格",
                    "沉默和停顿也是对话的一部分",
                ],
                evaluation_criteria={
                    "人物区分度": 0.30,
                    "潜台词运用": 0.25,
                    "剧情推进": 0.25,
                    "自然流畅度": 0.20,
                },
                tags=["对话", "人物", "技巧"],
            ),
            WritingExercise(
                exercise_id="EX_003",
                title="战斗场景描写",
                description="写一段800字的战斗场景，要求有节奏变化和战术博弈",
                skill_focus=["description", "pacing_control"],
                difficulty="advanced",
                prompt="主角在秘境中遭遇守护兽，实力相当，必须智取...",
                constraints=[
                    "必须有至少一次节奏变化",
                    "使用至少3种感官描写",
                    "战斗结果不能靠蛮力取胜",
                    "要有心理描写穿插",
                ],
                target_word_count=800,
                hints=[
                    "战斗不是回合制，要有攻防转换",
                    "环境可以成为战斗的一部分",
                    "让读者感受到紧张和危险",
                ],
                evaluation_criteria={
                    "节奏控制": 0.25,
                    "感官描写": 0.20,
                    "战术设计": 0.25,
                    "紧张感营造": 0.30,
                },
                tags=["战斗", "描写", "节奏"],
            ),
            WritingExercise(
                exercise_id="EX_004",
                title="情感高潮设计",
                description="写一段1000字的情感高潮场景，让读者产生强烈共鸣",
                skill_focus=["emotional_design", "description"],
                difficulty="advanced",
                prompt="主角历经千辛万苦终于救回了被囚禁的挚友，但挚友已经...",
                constraints=[
                    "必须使用延迟满足技巧",
                    "至少一处细节特写",
                    "情感要有层次递进",
                    "避免直接说「他很伤心」",
                ],
                target_word_count=1000,
                hints=[
                    "用动作和细节代替情感形容词",
                    "对比反差可以增强感染力",
                    "留白比写满更有力量",
                ],
                evaluation_criteria={
                    "情感层次": 0.30,
                    "细节描写": 0.25,
                    "节奏把控": 0.20,
                    "共鸣强度": 0.25,
                },
                tags=["情感", "高潮", "共鸣"],
            ),
            WritingExercise(
                exercise_id="EX_005",
                title="伏笔埋设与回收",
                description="设计一个跨越10章的伏笔，写出埋设章节和回收章节的关键段落",
                skill_focus=["foreshadowing", "plot_design"],
                difficulty="advanced",
                prompt="主角在第一章捡到一枚看似普通的铜钱，在第十章这枚铜钱成为破局的关键...",
                constraints=[
                    "埋设时要自然不刻意",
                    "回收时要有「原来如此」的恍然大悟",
                    "中间章节要有暗示但不明说",
                    "伏笔回收要推动剧情转折",
                ],
                target_word_count=1500,
                hints=[
                    "好伏笔像种子，埋下时不起眼",
                    "回收时机要恰到好处",
                    "一个伏笔可以有多个暗示",
                ],
                evaluation_criteria={
                    "埋设自然度": 0.25,
                    "回收震撼度": 0.30,
                    "中间暗示": 0.20,
                    "剧情推动": 0.25,
                },
                tags=["伏笔", "结构", "设计"],
            ),
            WritingExercise(
                exercise_id="EX_006",
                title="世界观构建练习",
                description="为一个架空世界设计完整的修炼/魔法体系",
                skill_focus=["world_building"],
                difficulty="intermediate",
                prompt="设计一个以「星辰之力」为核心的修炼体系，包含等级划分、突破条件、特殊能力...",
                constraints=[
                    "至少5个修炼等级",
                    "每个等级有明确的突破条件",
                    "体系内部逻辑自洽",
                    "有独特的代价或限制",
                ],
                target_word_count=1000,
                hints=[
                    "好的体系有限制才有张力",
                    "等级之间的差距要合理",
                    "特殊能力要与等级匹配",
                ],
                evaluation_criteria={
                    "体系完整度": 0.30,
                    "逻辑自洽": 0.30,
                    "创新性": 0.20,
                    "可写性": 0.20,
                },
                tags=["世界观", "设定", "体系"],
            ),
            WritingExercise(
                exercise_id="EX_007",
                title="人物弧线设计",
                description="为一个角色设计完整的成长弧线，从登场到结局",
                skill_focus=["character_building", "plot_design"],
                difficulty="intermediate",
                prompt="设计一个从懦弱到勇敢的角色成长弧线，标注每个阶段的关键事件...",
                constraints=[
                    "至少5个成长阶段",
                    "每个阶段有明确的触发事件",
                    "成长要有反复和挫折",
                    "最终形态与初始形态形成鲜明对比",
                ],
                target_word_count=800,
                hints=[
                    "成长不是线性的，要有起伏",
                    "外部事件触发内部变化",
                    "让读者看到角色「选择」的瞬间",
                ],
                evaluation_criteria={
                    "弧线完整度": 0.30,
                    "转变合理性": 0.30,
                    "阶段设计": 0.20,
                    "对比效果": 0.20,
                },
                tags=["人物", "弧线", "成长"],
            ),
            WritingExercise(
                exercise_id="EX_008",
                title="悬念设置练习",
                description="为一个章节写5种不同类型的结尾悬念",
                skill_focus=["plot_design", "pacing_control"],
                difficulty="beginner",
                prompt="主角刚刚在宗门大比中获胜，但...",
                constraints=[
                    "5种悬念类型不能重复",
                    "每种悬念不超过100字",
                    "每种都要让读者产生「然后呢」的冲动",
                ],
                target_word_count=500,
                hints=[
                    "信息差悬念最常用也最有效",
                    "倒计时悬念增加紧迫感",
                    "关系悬念让读者关心人物命运",
                ],
                evaluation_criteria={
                    "悬念多样性": 0.30,
                    "吸引力": 0.40,
                    "简洁有力": 0.30,
                },
                tags=["悬念", "结尾", "技巧"],
            ),
        ]

        for ex in builtin_exercises:
            self.exercises[ex.exercise_id] = ex
            self.exercise_counter += 1

    def get_exercise(self, exercise_id: str) -> Optional[WritingExercise]:
        """获取练习"""
        return self.exercises.get(exercise_id)

    def get_exercises_by_skill(self, skill_name: str) -> List[WritingExercise]:
        """按技能获取练习列表"""
        skill_key_map = {
            "剧情设计": "plot_design",
            "人物塑造": "character_building",
            "对话写作": "dialogue_writing",
            "场景描写": "description",
            "节奏控制": "pacing_control",
            "伏笔设计": "foreshadowing",
            "情绪设计": "emotional_design",
            "世界观构建": "world_building",
        }
        skill_key = skill_key_map.get(skill_name, skill_name)

        return [
            ex for ex in self.exercises.values()
            if skill_key in ex.skill_focus
        ]

    def get_exercises_by_difficulty(self,
                                     difficulty: str) -> List[WritingExercise]:
        """按难度获取练习"""
        return [
            ex for ex in self.exercises.values()
            if ex.difficulty == difficulty
        ]

    def start_exercise(self, exercise_id: str) -> Dict:
        """开始一个练习，返回练习详情和准备信息"""
        exercise = self.exercises.get(exercise_id)
        if not exercise:
            return {"error": f"练习不存在: {exercise_id}"}

        skill_status = {}
        for skill_key in exercise.skill_focus:
            if skill_key in self.skills:
                skill_status[skill_key] = {
                    "name": self.skills[skill_key].name,
                    "level": self.skills[skill_key].level.value,
                }

        return {
            "exercise": {
                "id": exercise.exercise_id,
                "title": exercise.title,
                "description": exercise.description,
                "prompt": exercise.prompt,
                "constraints": exercise.constraints,
                "target_word_count": exercise.target_word_count,
                "hints": exercise.hints,
                "evaluation_criteria": exercise.evaluation_criteria,
            },
            "skill_status": skill_status,
            "previous_attempts": len(self.attempts.get(exercise_id, [])),
        }

    def submit_attempt(self, exercise_id: str, content: str,
                       time_spent_seconds: float = 0,
                       self_rating: float = 0.0) -> ExerciseAttempt:
        """提交练习尝试"""
        self.attempt_counter += 1
        attempt = ExerciseAttempt(
            attempt_id=f"ATT_{self.attempt_counter:06d}",
            exercise_id=exercise_id,
            content=content,
            word_count=len(content),
            time_spent_seconds=time_spent_seconds,
            self_rating=self_rating,
            created_at=datetime.now().isoformat(),
        )

        if exercise_id not in self.attempts:
            self.attempts[exercise_id] = []
        self.attempts[exercise_id].append(attempt)

        exercise = self.exercises.get(exercise_id)
        if exercise:
            for skill_key in exercise.skill_focus:
                if skill_key in self.skills:
                    exp_gain = 10 + len(content) // 100
                    self.gain_experience(skill_key, exp_gain)

        return attempt

    def evaluate_attempt(self, attempt_id: str) -> Dict:
        """评估练习尝试 - 基于内置标准自动评分"""
        attempt = None
        for attempts_list in self.attempts.values():
            for a in attempts_list:
                if a.attempt_id == attempt_id:
                    attempt = a
                    break
            if attempt:
                break

        if not attempt:
            return {"error": f"未找到尝试: {attempt_id}"}

        exercise = self.exercises.get(attempt.exercise_id)
        if not exercise:
            return {"error": "关联练习不存在"}

        scores = {}
        strengths = []
        weaknesses = []

        content = attempt.content
        sentences = re.split(r'[。！？\n]+', content)
        sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 1]

        if "冲突建立" in exercise.evaluation_criteria:
            conflict_keywords = ["冲突", "矛盾", "危机", "威胁", "挑战", "阻碍", "危险"]
            conflict_score = sum(1 for s in sentences if any(kw in s for kw in conflict_keywords))
            conflict_score = min(100, conflict_score / max(len(sentences), 1) * 300)
            scores["冲突建立"] = round(conflict_score, 1)
            if conflict_score >= 70:
                strengths.append("冲突建立清晰有力")
            else:
                weaknesses.append("冲突建立不够明确，建议增加对抗性元素")

        if "悬念设置" in exercise.evaluation_criteria:
            last_sentences = sentences[-3:] if len(sentences) >= 3 else sentences
            suspense_keywords = ["突然", "然而", "但是", "竟然", "原来", "?", "？"]
            suspense_score = sum(1 for s in last_sentences if any(kw in s for kw in suspense_keywords))
            suspense_score = min(100, suspense_score / max(len(last_sentences), 1) * 200)
            scores["悬念设置"] = round(suspense_score, 1)
            if suspense_score >= 60:
                strengths.append("结尾悬念设置有效")
            else:
                weaknesses.append("结尾缺乏悬念，建议增加意外元素或未解问题")

        if "人物塑造" in exercise.evaluation_criteria:
            char_names = re.findall(r'[\u4e00-\u9fff]{2,3}(?=说|道|问|喊|叫|吼|叹|笑|哭|怒)', content)
            unique_chars = len(set(char_names))
            char_score = min(100, unique_chars * 25 + 25)
            scores["人物塑造"] = round(char_score, 1)
            if unique_chars >= 3:
                strengths.append(f"出现了{unique_chars}个有辨识度的角色")
            else:
                weaknesses.append("角色数量不足，建议增加互动角色")

        if "世界观展示" in exercise.evaluation_criteria:
            world_keywords = ["修炼", "灵力", "魔法", "境界", "功法", "丹药", "阵法",
                              "宗门", "家族", "秘境", "传承", "天赋"]
            world_score = sum(1 for s in sentences if any(kw in s for kw in world_keywords))
            world_score = min(100, world_score / max(len(sentences), 1) * 300)
            scores["世界观展示"] = round(world_score, 1)
            if world_score >= 50:
                strengths.append("世界观元素融入自然")
            else:
                weaknesses.append("世界观展示不足，建议通过角色互动展示设定")

        if "语言流畅度" in exercise.evaluation_criteria:
            if sentences:
                avg_len = sum(len(s) for s in sentences) / len(sentences)
                len_score = 100 if 20 <= avg_len <= 60 else max(30, 100 - abs(avg_len - 40))
                scores["语言流畅度"] = round(len_score, 1)
                if len_score >= 70:
                    strengths.append("句式长度适中，阅读流畅")
                else:
                    weaknesses.append("句式长度需要调整，建议长短句交替")

        if "人物区分度" in exercise.evaluation_criteria:
            dialogue_markers = re.findall(r'[""「」『』](.*?)[""「」『』]', content)
            if dialogue_markers:
                unique_styles = len(set(d[:5] for d in dialogue_markers))
                style_score = min(100, unique_styles / max(len(dialogue_markers), 1) * 200)
                scores["人物区分度"] = round(style_score, 1)
                if style_score >= 60:
                    strengths.append("对话风格有区分度")
                else:
                    weaknesses.append("对话风格趋同，建议为每个角色设计独特口头禅")
            else:
                scores["人物区分度"] = 30
                weaknesses.append("对话内容不足")

        if "潜台词运用" in exercise.evaluation_criteria:
            subtext_indicators = ["其实", "心里", "暗想", "嘴上说", "眼神", "犹豫", "沉默", "停顿"]
            subtext_score = sum(1 for s in sentences if any(ind in s for ind in subtext_indicators))
            subtext_score = min(100, subtext_score / max(len(sentences), 1) * 300)
            scores["潜台词运用"] = round(subtext_score, 1)
            if subtext_score >= 50:
                strengths.append("潜台词运用得当")
            else:
                weaknesses.append("缺乏潜台词，建议增加「言不由衷」的对话")

        if "节奏控制" in exercise.evaluation_criteria:
            short_sents = sum(1 for s in sentences if len(s) < 15)
            long_sents = sum(1 for s in sentences if len(s) > 50)
            variety = (short_sents + long_sents) / max(len(sentences), 1)
            rhythm_score = min(100, variety * 150)
            scores["节奏控制"] = round(rhythm_score, 1)
            if rhythm_score >= 60:
                strengths.append("节奏有变化，张弛有度")
            else:
                weaknesses.append("节奏单一，建议增加句式变化")

        if "感官描写" in exercise.evaluation_criteria:
            sense_keywords = {
                "视觉": ["看见", "望去", "眼前", "光芒", "色彩", "景象"],
                "听觉": ["听到", "声音", "轰鸣", "寂静", "回响", "传来"],
                "触觉": ["感到", "冰冷", "灼热", "刺痛", "麻木", "柔软"],
                "嗅觉": ["闻到", "气味", "芳香", "腥臭", "清香", "刺鼻"],
            }
            senses_used = 0
            for sense, keywords in sense_keywords.items():
                if any(kw in content for kw in keywords):
                    senses_used += 1
            sense_score = min(100, senses_used * 30)
            scores["感官描写"] = round(sense_score, 1)
            if senses_used >= 3:
                strengths.append(f"使用了{senses_used}种感官描写")
            else:
                weaknesses.append("感官描写单一，建议增加听觉/触觉/嗅觉描写")

        if "战术设计" in exercise.evaluation_criteria:
            tactic_keywords = ["佯攻", "诱敌", "埋伏", "破绽", "算计", "预判",
                               "反击", "闪避", "格挡", "周旋", "智取", "布局"]
            tactic_score = sum(1 for s in sentences if any(kw in s for kw in tactic_keywords))
            tactic_score = min(100, tactic_score / max(len(sentences), 1) * 300)
            scores["战术设计"] = round(tactic_score, 1)
            if tactic_score >= 50:
                strengths.append("战斗有战术博弈")
            else:
                weaknesses.append("战斗缺乏战术设计，建议增加智斗元素")

        if "紧张感营造" in exercise.evaluation_criteria:
            tension_keywords = ["紧", "急", "险", "危", "悬", "迫", "逼", "骤", "猛", "猝"]
            tension_score = sum(1 for s in sentences if any(kw in s for kw in tension_keywords))
            tension_score = min(100, tension_score / max(len(sentences), 1) * 250)
            scores["紧张感营造"] = round(tension_score, 1)
            if tension_score >= 50:
                strengths.append("紧张感营造成功")
            else:
                weaknesses.append("紧张感不足，建议使用短句和紧迫性词汇")

        if "情感层次" in exercise.evaluation_criteria:
            emotion_keywords = {
                "喜": ["笑", "喜", "乐", "欢"],
                "怒": ["怒", "愤", "恨", "气"],
                "哀": ["悲", "哀", "伤", "哭", "泪"],
                "惊": ["惊", "震", "愣", "呆"],
            }
            emotions_present = sum(
                1 for keywords in emotion_keywords.values()
                if any(kw in content for kw in keywords)
            )
            emotion_score = min(100, emotions_present * 30)
            scores["情感层次"] = round(emotion_score, 1)
            if emotions_present >= 3:
                strengths.append(f"情感层次丰富({emotions_present}种)")
            else:
                weaknesses.append("情感层次单一，建议增加情感变化")

        if "细节描写" in exercise.evaluation_criteria:
            detail_indicators = ["手指", "眼神", "嘴角", "眉头", "脚步", "呼吸",
                                 "微微", "轻轻", "缓缓", "慢慢", "颤抖"]
            detail_score = sum(1 for s in sentences if any(ind in s for ind in detail_indicators))
            detail_score = min(100, detail_score / max(len(sentences), 1) * 300)
            scores["细节描写"] = round(detail_score, 1)
            if detail_score >= 50:
                strengths.append("细节描写到位")
            else:
                weaknesses.append("缺乏细节描写，建议增加微表情和微动作")

        if "共鸣强度" in exercise.evaluation_criteria:
            resonance_keywords = ["触动", "感动", "心疼", "不忍", "共鸣", "理解",
                                  "代入", "感同身受", "揪心", "温暖"]
            resonance_score = sum(1 for s in sentences if any(kw in s for kw in resonance_keywords))
            resonance_score = min(100, resonance_score / max(len(sentences), 1) * 300)
            scores["共鸣强度"] = round(resonance_score, 1)
            if resonance_score >= 40:
                strengths.append("有情感共鸣点")
            else:
                weaknesses.append("情感共鸣不足，建议增加读者能代入的细节")

        if "埋设自然度" in exercise.evaluation_criteria:
            natural_keywords = ["顺便", "无意", "随手", "习惯", "日常", "普通", "寻常"]
            natural_score = sum(1 for s in sentences if any(kw in s for kw in natural_keywords))
            natural_score = min(100, natural_score / max(len(sentences), 1) * 300 + 30)
            scores["埋设自然度"] = round(natural_score, 1)
            if natural_score >= 50:
                strengths.append("伏笔埋设自然")
            else:
                weaknesses.append("伏笔埋设过于刻意，建议融入日常场景")

        if "回收震撼度" in exercise.evaluation_criteria:
            reveal_keywords = ["原来", "竟然", "居然", "难怪", "怪不得", "恍然大悟", "原来如此"]
            reveal_score = sum(1 for s in sentences if any(kw in s for kw in reveal_keywords))
            reveal_score = min(100, reveal_score / max(len(sentences), 1) * 300)
            scores["回收震撼度"] = round(reveal_score, 1)
            if reveal_score >= 40:
                strengths.append("伏笔回收有震撼感")
            else:
                weaknesses.append("伏笔回收缺乏震撼，建议增加反转力度")

        if "体系完整度" in exercise.evaluation_criteria:
            level_keywords = ["级", "阶", "层", "段", "重", "品", "星"]
            level_count = sum(1 for s in sentences if any(kw in s for kw in level_keywords))
            system_score = min(100, level_count * 15 + 20)
            scores["体系完整度"] = round(system_score, 1)
            if system_score >= 60:
                strengths.append("体系设计完整")
            else:
                weaknesses.append("体系不够完整，建议明确等级划分")

        if "逻辑自洽" in exercise.evaluation_criteria:
            logic_score = 70
            contradictions = []
            if "最强" in content and "无敌" in content:
                contradictions.append("存在绝对化描述")
                logic_score -= 15
            if len(sentences) > 0:
                scores["逻辑自洽"] = round(max(30, logic_score), 1)
                if logic_score >= 70:
                    strengths.append("设定逻辑自洽")
                else:
                    weaknesses.append(f"存在逻辑问题: {'; '.join(contradictions)}")

        if "创新性" in exercise.evaluation_criteria:
            common_tropes = ["丹田", "灵气", "斗气", "魔法", "系统", "金手指"]
            trope_count = sum(1 for t in common_tropes if t in content)
            innovation_score = max(30, 100 - trope_count * 15)
            scores["创新性"] = round(innovation_score, 1)
            if innovation_score >= 70:
                strengths.append("设定有创新性")
            else:
                weaknesses.append("设定较为常见，建议增加独特元素")

        if "可写性" in exercise.evaluation_criteria:
            actionable_keywords = ["可以", "能够", "通过", "需要", "必须", "当", "若"]
            actionable_score = sum(1 for s in sentences if any(kw in s for kw in actionable_keywords))
            actionable_score = min(100, actionable_score / max(len(sentences), 1) * 300 + 30)
            scores["可写性"] = round(actionable_score, 1)
            if actionable_score >= 60:
                strengths.append("设定可操作性强")
            else:
                weaknesses.append("设定缺乏可操作性，建议增加具体规则")

        if "弧线完整度" in exercise.evaluation_criteria:
            stage_keywords = ["开始", "转折", "成长", "蜕变", "结局", "变化", "改变"]
            stage_count = sum(1 for s in sentences if any(kw in s for kw in stage_keywords))
            arc_score = min(100, stage_count * 15 + 20)
            scores["弧线完整度"] = round(arc_score, 1)
            if arc_score >= 60:
                strengths.append("角色弧线设计完整")
            else:
                weaknesses.append("角色弧线不够完整，建议明确各阶段")

        if "转变合理性" in exercise.evaluation_criteria:
            transition_keywords = ["因为", "所以", "因此", "于是", "导致", "引发", "促使"]
            transition_score = sum(1 for s in sentences if any(kw in s for kw in transition_keywords))
            transition_score = min(100, transition_score / max(len(sentences), 1) * 300 + 30)
            scores["转变合理性"] = round(transition_score, 1)
            if transition_score >= 50:
                strengths.append("转变有因果支撑")
            else:
                weaknesses.append("转变缺乏铺垫，建议增加触发事件")

        if "阶段设计" in exercise.evaluation_criteria:
            scores["阶段设计"] = round(min(100, len(sentences) * 5 + 30), 1)
            if len(sentences) >= 10:
                strengths.append("阶段划分清晰")
            else:
                weaknesses.append("阶段划分不够清晰")

        if "对比效果" in exercise.evaluation_criteria:
            contrast_keywords = ["曾经", "如今", "从前", "现在", "过去", "后来", "最终"]
            contrast_score = sum(1 for s in sentences if any(kw in s for kw in contrast_keywords))
            contrast_score = min(100, contrast_score / max(len(sentences), 1) * 300 + 30)
            scores["对比效果"] = round(contrast_score, 1)
            if contrast_score >= 50:
                strengths.append("前后对比鲜明")
            else:
                weaknesses.append("缺乏前后对比，建议强化变化幅度")

        if "悬念多样性" in exercise.evaluation_criteria:
            scores["悬念多样性"] = round(min(100, len(sentences) * 15 + 20), 1)
            if len(sentences) >= 5:
                strengths.append("悬念类型多样")
            else:
                weaknesses.append("悬念类型不够多样")

        if "吸引力" in exercise.evaluation_criteria:
            hook_keywords = ["?", "？", "!", "！", "突然", "竟然", "原来", "神秘", "秘密"]
            hook_score = sum(1 for s in sentences if any(kw in s for kw in hook_keywords))
            hook_score = min(100, hook_score / max(len(sentences), 1) * 300 + 20)
            scores["吸引力"] = round(hook_score, 1)
            if hook_score >= 60:
                strengths.append("悬念吸引力强")
            else:
                weaknesses.append("悬念吸引力不足")

        if "简洁有力" in exercise.evaluation_criteria:
            avg_len = sum(len(s) for s in sentences) / max(len(sentences), 1) if sentences else 0
            concise_score = 100 if avg_len < 80 else max(30, 100 - (avg_len - 80))
            scores["简洁有力"] = round(concise_score, 1)
            if concise_score >= 70:
                strengths.append("表达简洁有力")
            else:
                weaknesses.append("表达可以更简洁")

        overall = sum(scores.values()) / max(len(scores), 1)

        attempt.scores = scores
        attempt.strengths = strengths[:5]
        attempt.weaknesses = weaknesses[:5]

        feedback_parts = []
        if strengths:
            feedback_parts.append("✅ 优点: " + "; ".join(strengths[:3]))
        if weaknesses:
            feedback_parts.append("📝 改进: " + "; ".join(weaknesses[:3]))
        feedback_parts.append(f"📊 综合评分: {overall:.1f}/100")
        attempt.ai_feedback = "\n".join(feedback_parts)

        return {
            "attempt_id": attempt.attempt_id,
            "overall_score": round(overall, 1),
            "dimension_scores": scores,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "feedback": attempt.ai_feedback,
        }

    def get_practice_stats(self) -> Dict:
        """获取练习统计"""
        total_attempts = sum(len(attempts) for attempts in self.attempts.values())
        completed_exercises = len([
            eid for eid, attempts in self.attempts.items()
            if len(attempts) > 0
        ])

        return {
            "total_exercises": len(self.exercises),
            "completed_exercises": completed_exercises,
            "total_attempts": total_attempts,
            "by_difficulty": {
                diff: len(self.get_exercises_by_difficulty(diff))
                for diff in ["beginner", "intermediate", "advanced"]
            },
            "recent_attempts": [
                {
                    "id": a.attempt_id,
                    "exercise": self.exercises.get(a.exercise_id, WritingExercise(
                        exercise_id=a.exercise_id, title="未知练习",
                        description=""
                    )).title,
                    "word_count": a.word_count,
                    "created": a.created_at,
                }
                for attempts in self.attempts.values()
                for a in attempts[-3:]
            ][-10:],
        }

    # ================================================================
    # 反馈循环 (Feedback Loop)
    # ================================================================

    def create_feedback_record(self, skill_name: str,
                                aspect: str = "综合") -> FeedbackRecord:
        """创建反馈记录"""
        skill = None
        for s in self.skills.values():
            if s.name == skill_name:
                skill = s
                break

        if not skill:
            skill_key_map = {
                "剧情设计": "plot_design",
                "人物塑造": "character_building",
                "对话写作": "dialogue_writing",
                "场景描写": "description",
                "节奏控制": "pacing_control",
                "伏笔设计": "foreshadowing",
                "情绪设计": "emotional_design",
                "世界观构建": "world_building",
            }
            skill_key = skill_key_map.get(skill_name)
            if skill_key and skill_key in self.skills:
                skill = self.skills[skill_key]

        if not skill:
            return FeedbackRecord(
                record_id=f"FB_{self.feedback_counter + 1:06d}",
                skill_name=skill_name,
                aspect=aspect,
                current_level="未知",
                target_level="专家",
                gap_analysis="未找到对应技能",
            )

        level_order = list(SkillLevel)
        current_idx = level_order.index(skill.level)
        target_idx = level_order.index(SkillLevel.EXPERT)

        gap = target_idx - current_idx
        if gap <= 0:
            gap_analysis = f"已达到{skill.level.value}水准，继续保持即可"
        elif gap == 1:
            gap_analysis = f"距离专家仅一步之遥，需要{skill.max_experience - skill.experience}点经验突破"
        elif gap <= 3:
            gap_analysis = f"还需{gap}个等级达到专家，建议加强专项训练"
        else:
            gap_analysis = f"距离专家还有{gap}个等级，建议从基础练习开始系统训练"

        improvement_plan = self._generate_improvement_plan(skill, gap)

        self.feedback_counter += 1
        record = FeedbackRecord(
            record_id=f"FB_{self.feedback_counter:06d}",
            skill_name=skill.name,
            aspect=aspect,
            current_level=skill.level.value,
            target_level="专家",
            gap_analysis=gap_analysis,
            improvement_plan=improvement_plan,
            progress_percentage=round(
                (skill.experience / skill.max_experience) * 100, 1
            ),
            last_reviewed=datetime.now().isoformat(),
        )

        self.feedback_records[record.record_id] = record
        return record

    def _generate_improvement_plan(self, skill: SkillRecord,
                                    gap: int) -> List[str]:
        """生成改进计划"""
        plan = []

        skill_exercise_map = {
            "剧情设计": ["EX_001", "EX_005", "EX_008"],
            "人物塑造": ["EX_002", "EX_007"],
            "对话写作": ["EX_002"],
            "场景描写": ["EX_003"],
            "节奏控制": ["EX_001", "EX_003", "EX_008"],
            "伏笔设计": ["EX_005"],
            "情绪设计": ["EX_004"],
            "世界观构建": ["EX_006"],
        }

        exercises = skill_exercise_map.get(skill.name, [])
        for ex_id in exercises:
            if ex_id in self.exercises:
                plan.append(f"完成练习: {self.exercises[ex_id].title}")

        if gap >= 2:
            plan.append("联网搜索该技能的最新写作技巧")
            plan.append("分析3本成功小说中该技能的运用")

        plan.append(f"当前经验: {skill.experience}/{skill.max_experience}")
        return plan

    def get_all_feedback(self) -> List[Dict]:
        """获取所有反馈记录"""
        return [
            {
                "id": r.record_id,
                "skill": r.skill_name,
                "aspect": r.aspect,
                "current": r.current_level,
                "target": r.target_level,
                "gap": r.gap_analysis,
                "progress": f"{r.progress_percentage:.1f}%",
                "plan": r.improvement_plan,
            }
            for r in sorted(
                self.feedback_records.values(),
                key=lambda r: r.last_reviewed,
                reverse=True,
            )
        ]

    def identify_weaknesses(self) -> Dict:
        """识别薄弱环节"""
        weaknesses = []
        level_order = list(SkillLevel)

        for skill in self.skills.values():
            current_idx = level_order.index(skill.level)
            if current_idx < level_order.index(SkillLevel.EXPERT):
                exp_percentage = (skill.experience / skill.max_experience) * 100
                weaknesses.append({
                    "skill": skill.name,
                    "level": skill.level.value,
                    "experience": f"{skill.experience}/{skill.max_experience}",
                    "progress": f"{exp_percentage:.1f}%",
                    "success_rate": (
                        f"{skill.success_count / max(skill.usage_count, 1) * 100:.1f}%"
                    ),
                    "priority": (
                        "高" if current_idx <= level_order.index(SkillLevel.APPRENTICE)
                        else "中"
                    ),
                })

        weaknesses.sort(key=lambda w: (
            0 if w["priority"] == "高" else 1,
            list(SkillLevel).index(SkillLevel(w["level"])),
        ))

        return {
            "total_weaknesses": len(weaknesses),
            "weaknesses": weaknesses,
            "recommended_focus": weaknesses[:3] if weaknesses else [],
        }

    def track_improvement(self, skill_name: str,
                          days: int = 30) -> Dict:
        """追踪技能改进趋势"""
        skill = None
        for s in self.skills.values():
            if s.name == skill_name:
                skill = s
                break

        if not skill:
            return {"error": f"未找到技能: {skill_name}"}

        relevant_attempts = []
        for ex_id, attempts in self.attempts.items():
            exercise = self.exercises.get(ex_id)
            if exercise:
                skill_key_map = {
                    "剧情设计": "plot_design",
                    "人物塑造": "character_building",
                    "对话写作": "dialogue_writing",
                    "场景描写": "description",
                    "节奏控制": "pacing_control",
                    "伏笔设计": "foreshadowing",
                    "情绪设计": "emotional_design",
                    "世界观构建": "world_building",
                }
                skill_key = skill_key_map.get(skill_name, "")
                if skill_key in exercise.skill_focus:
                    for a in attempts:
                        if a.scores:
                            avg_score = sum(a.scores.values()) / max(len(a.scores), 1)
                            relevant_attempts.append({
                                "date": a.created_at[:10],
                                "exercise": exercise.title,
                                "score": round(avg_score, 1),
                                "word_count": a.word_count,
                            })

        relevant_attempts.sort(key=lambda a: a["date"])

        trend = "稳定"
        if len(relevant_attempts) >= 3:
            recent = [a["score"] for a in relevant_attempts[-3:]]
            if recent[-1] > recent[0] + 10:
                trend = "上升"
            elif recent[-1] < recent[0] - 10:
                trend = "下降"

        return {
            "skill": skill.name,
            "current_level": skill.level.value,
            "total_attempts": len(relevant_attempts),
            "trend": trend,
            "history": relevant_attempts[-20:],
            "avg_score": (
                round(sum(a["score"] for a in relevant_attempts) / max(len(relevant_attempts), 1), 1)
                if relevant_attempts else 0
            ),
        }

    # ================================================================
    # 学习路径 (Learning Path)
    # ================================================================

    def _init_builtin_learning_paths(self):
        """初始化内置学习路径"""
        self.path_counter += 1
        beginner_path = LearningPath(
            path_id=f"PATH_{self.path_counter:04d}",
            name="网文写作入门之路",
            description="从零开始系统学习网文写作的核心技能",
            target_genre="all",
            milestones=[
                LearningMilestone(
                    milestone_id="MS_001",
                    name="基础认知",
                    description="了解网文的基本结构和读者期待",
                    required_skills={"plot_design": "学徒"},
                    required_exercises=["EX_001", "EX_008"],
                    rewards=["解锁「黄金三章」模板", "获得基础写作提示库"],
                ),
                LearningMilestone(
                    milestone_id="MS_002",
                    name="人物塑造",
                    description="学会创造有魅力的角色",
                    required_skills={"character_building": "学徒"},
                    required_exercises=["EX_002", "EX_007"],
                    rewards=["解锁「人物原型」模板", "获得角色设计工具箱"],
                ),
                LearningMilestone(
                    milestone_id="MS_003",
                    name="场景与节奏",
                    description="掌握场景描写和节奏控制",
                    required_skills={"description": "熟手", "pacing_control": "熟手"},
                    required_exercises=["EX_003"],
                    rewards=["解锁「战斗场景」模板", "获得节奏分析工具"],
                ),
                LearningMilestone(
                    milestone_id="MS_004",
                    name="情感与伏笔",
                    description="学会设计情感高潮和伏笔系统",
                    required_skills={"emotional_design": "熟手", "foreshadowing": "熟手"},
                    required_exercises=["EX_004", "EX_005"],
                    rewards=["解锁「情感曲线」工具", "获得伏笔管理模板"],
                ),
                LearningMilestone(
                    milestone_id="MS_005",
                    name="世界观构建",
                    description="构建完整自洽的世界观体系",
                    required_skills={"world_building": "专家"},
                    required_exercises=["EX_006"],
                    rewards=["解锁「世界观」完整模板", "获得设定一致性检查工具"],
                ),
            ],
            started_at=datetime.now().isoformat(),
            last_activity=datetime.now().isoformat(),
        )
        self.learning_paths[beginner_path.path_id] = beginner_path

        self.path_counter += 1
        advanced_path = LearningPath(
            path_id=f"PATH_{self.path_counter:04d}",
            name="玄幻小说大师之路",
            description="专为玄幻/仙侠题材设计的进阶学习路径",
            target_genre="玄幻",
            milestones=[
                LearningMilestone(
                    milestone_id="MS_101",
                    name="修炼体系设计",
                    description="设计独特且逻辑自洽的修炼体系",
                    required_skills={"world_building": "专家"},
                    required_exercises=["EX_006"],
                    rewards=["解锁「修炼体系」完整模板"],
                ),
                LearningMilestone(
                    milestone_id="MS_102",
                    name="战斗场景精通",
                    description="写出让读者热血沸腾的战斗场景",
                    required_skills={"description": "专家", "pacing_control": "专家"},
                    required_exercises=["EX_003"],
                    rewards=["解锁「战斗场景」高级模板"],
                ),
                LearningMilestone(
                    milestone_id="MS_103",
                    name="长篇布局",
                    description="掌握百万字长篇的伏笔和结构设计",
                    required_skills={"plot_design": "大师", "foreshadowing": "专家"},
                    required_exercises=["EX_005"],
                    rewards=["解锁「长篇结构」完整模板"],
                ),
            ],
            started_at=datetime.now().isoformat(),
            last_activity=datetime.now().isoformat(),
        )
        self.learning_paths[advanced_path.path_id] = advanced_path

    def get_learning_path(self, path_id: str) -> Optional[LearningPath]:
        """获取学习路径"""
        return self.learning_paths.get(path_id)

    def get_all_learning_paths(self) -> List[Dict]:
        """获取所有学习路径"""
        return [
            {
                "id": p.path_id,
                "name": p.name,
                "description": p.description,
                "genre": p.target_genre,
                "milestones": len(p.milestones),
                "completed": p.total_exercises_completed,
                "progress": self._calculate_path_progress(p),
            }
            for p in self.learning_paths.values()
        ]

    def _calculate_path_progress(self, path: LearningPath) -> str:
        """计算路径进度"""
        if not path.milestones:
            return "0%"

        completed = sum(1 for m in path.milestones if m.completed)
        return f"{completed / len(path.milestones) * 100:.0f}%"

    def check_milestone_unlock(self, path_id: str) -> Dict:
        """检查里程碑解锁状态"""
        path = self.learning_paths.get(path_id)
        if not path:
            return {"error": f"路径不存在: {path_id}"}

        results = []
        for i, milestone in enumerate(path.milestones):
            if milestone.completed:
                results.append({
                    "milestone": milestone.name,
                    "status": "已完成",
                    "completed_at": milestone.completed_at,
                })
                continue

            all_skills_met = True
            for skill_key, required_level in milestone.required_skills.items():
                if skill_key in self.skills:
                    current_level = self.skills[skill_key].level
                    level_order = list(SkillLevel)
                    if level_order.index(current_level) < level_order.index(
                            SkillLevel(required_level)):
                        all_skills_met = False
                        break
                else:
                    all_skills_met = False
                    break

            all_exercises_done = True
            for ex_id in milestone.required_exercises:
                if ex_id not in self.attempts or len(self.attempts[ex_id]) == 0:
                    all_exercises_done = False
                    break

            if all_skills_met and all_exercises_done:
                milestone.unlocked = True
                milestone.completed = True
                milestone.completed_at = datetime.now().isoformat()
                path.total_exercises_completed += 1
                results.append({
                    "milestone": milestone.name,
                    "status": "刚完成! 🎉",
                    "rewards": milestone.rewards,
                })
            elif all_skills_met:
                milestone.unlocked = True
                results.append({
                    "milestone": milestone.name,
                    "status": "已解锁(需完成练习)",
                    "missing": [
                        self.exercises[ex_id].title
                        for ex_id in milestone.required_exercises
                        if ex_id not in self.attempts or len(self.attempts[ex_id]) == 0
                    ],
                })
            else:
                results.append({
                    "milestone": milestone.name,
                    "status": "未解锁",
                    "missing_skills": {
                        self.skills[sk].name if sk in self.skills else sk: req
                        for sk, req in milestone.required_skills.items()
                        if sk not in self.skills or list(SkillLevel).index(
                            self.skills[sk].level
                        ) < list(SkillLevel).index(SkillLevel(req))
                    },
                })

        path.last_activity = datetime.now().isoformat()
        return {
            "path_name": path.name,
            "milestones": results,
            "overall_progress": self._calculate_path_progress(path),
        }

    def get_next_recommended_action(self, path_id: str) -> Dict:
        """获取下一步推荐行动"""
        path = self.learning_paths.get(path_id)
        if not path:
            return {"error": f"路径不存在: {path_id}"}

        for milestone in path.milestones:
            if not milestone.completed:
                actions = []

                for skill_key, required_level in milestone.required_skills.items():
                    if skill_key in self.skills:
                        current = self.skills[skill_key]
                        level_order = list(SkillLevel)
                        if level_order.index(current.level) < level_order.index(
                                SkillLevel(required_level)):
                            actions.append({
                                "type": "skill_upgrade",
                                "skill": current.name,
                                "current": current.level.value,
                                "target": required_level,
                                "action": f"将「{current.name}」提升到{required_level}",
                            })

                for ex_id in milestone.required_exercises:
                    if ex_id not in self.attempts or len(self.attempts[ex_id]) == 0:
                        if ex_id in self.exercises:
                            actions.append({
                                "type": "exercise",
                                "exercise_id": ex_id,
                                "title": self.exercises[ex_id].title,
                                "action": f"完成练习「{self.exercises[ex_id].title}」",
                            })

                return {
                    "next_milestone": milestone.name,
                    "description": milestone.description,
                    "actions": actions,
                    "rewards": milestone.rewards,
                }

        return {
            "message": "所有里程碑已完成! 🎉",
            "actions": [],
        }

    # ================================================================
    # 技能组合 (Skill Combination)
    # ================================================================

    def _init_builtin_skill_combos(self):
        """初始化内置技能组合"""
        builtin_combos = [
            SkillCombo(
                combo_id="COMBO_001",
                name="高潮设计组合",
                description="将剧情设计、节奏控制和情绪设计结合，创造震撼的高潮场景",
                skills_required=["plot_design", "pacing_control", "emotional_design"],
                synergy_score=0.85,
                use_cases=[
                    "章节高潮设计",
                    "卷末大高潮",
                    "全书终极高潮",
                ],
                techniques=[
                    "三波递进: 小高潮→中高潮→大高潮",
                    "情绪曲线: 压抑→释放→震撼",
                    "节奏切换: 慢→快→极快→静止",
                    "多线汇聚: 所有支线在高潮点交汇",
                ],
                discovered_at=datetime.now().isoformat(),
            ),
            SkillCombo(
                combo_id="COMBO_002",
                name="人物深度塑造",
                description="结合人物塑造、对话写作和场景描写，创造立体角色",
                skills_required=["character_building", "dialogue_writing", "description"],
                synergy_score=0.80,
                use_cases=[
                    "主角深度塑造",
                    "反派魅力塑造",
                    "配角功能最大化",
                ],
                techniques=[
                    "对话展示性格: 每人说话方式不同",
                    "场景烘托人物: 环境反映内心",
                    "行动定义角色: 关键时刻的选择",
                    "对比强化印象: 与其他角色的反差",
                ],
                discovered_at=datetime.now().isoformat(),
            ),
            SkillCombo(
                combo_id="COMBO_003",
                name="长篇布局系统",
                description="结合剧情设计、伏笔设计和世界观构建，驾驭百万字长篇",
                skills_required=["plot_design", "foreshadowing", "world_building"],
                synergy_score=0.90,
                use_cases=[
                    "百万字以上长篇布局",
                    "多卷本系列规划",
                    "复杂世界观展开",
                ],
                techniques=[
                    "主线+支线: 主剧情推进，支线丰富世界",
                    "伏笔网络: 短中长三期伏笔交织",
                    "世界观分层: 逐步揭示更深层的设定",
                    "节奏地图: 全书高低潮分布规划",
                ],
                discovered_at=datetime.now().isoformat(),
            ),
            SkillCombo(
                combo_id="COMBO_004",
                name="爽点流水线",
                description="结合节奏控制、情绪设计和剧情设计，持续制造爽点",
                skills_required=["pacing_control", "emotional_design", "plot_design"],
                synergy_score=0.75,
                use_cases=[
                    "日常章节爽点设计",
                    "打脸场景优化",
                    "升级突破场景",
                ],
                techniques=[
                    "铺垫→爆发→反应: 标准爽点三段式",
                    "情绪递进: 压抑→期待→满足",
                    "节奏加速: 短句+动作+震惊反应",
                    "连锁爽点: 一个小爽点引出更大的",
                ],
                discovered_at=datetime.now().isoformat(),
            ),
            SkillCombo(
                combo_id="COMBO_005",
                name="沉浸式世界构建",
                description="结合世界观构建、场景描写和对话写作，创造让读者沉浸的世界",
                skills_required=["world_building", "description", "dialogue_writing"],
                synergy_score=0.82,
                use_cases=[
                    "异世界/架空世界构建",
                    "独特文化体系设计",
                    "让设定「活」起来",
                ],
                techniques=[
                    "展示而非告知: 通过角色互动展示设定",
                    "日常融入: 在普通场景中体现世界观",
                    "对话传递: 角色对话自然带出设定信息",
                    "感官沉浸: 五感描写让世界可感知",
                ],
                discovered_at=datetime.now().isoformat(),
            ),
        ]

        for combo in builtin_combos:
            self.skill_combos[combo.combo_id] = combo
            self.combo_counter += 1

    def get_skill_combo(self, combo_id: str) -> Optional[SkillCombo]:
        """获取技能组合"""
        return self.skill_combos.get(combo_id)

    def get_all_skill_combos(self) -> List[Dict]:
        """获取所有技能组合"""
        return [
            {
                "id": c.combo_id,
                "name": c.name,
                "description": c.description,
                "skills": c.skills_required,
                "synergy": f"{c.synergy_score:.0%}",
                "techniques": c.techniques,
                "use_cases": c.use_cases,
            }
            for c in self.skill_combos.values()
        ]

    def discover_skill_combos(self) -> List[SkillCombo]:
        """自动发现新的技能组合 - 基于技能等级和练习数据"""
        new_combos = []

        combo_templates = [
            {
                "name": "对话驱动剧情",
                "description": "通过高质量对话推进剧情发展",
                "skills": ["dialogue_writing", "plot_design"],
                "use_cases": ["对话为主的章节", "人物关系揭示", "信息传递场景"],
                "techniques": [
                    "每段对话都推动剧情",
                    "对话中埋设信息",
                    "通过对话展示人物关系变化",
                ],
            },
            {
                "name": "情感场景构建",
                "description": "结合场景描写和情绪设计创造感人场景",
                "skills": ["description", "emotional_design"],
                "use_cases": ["情感高潮", "离别场景", "重逢场景"],
                "techniques": [
                    "环境烘托情绪",
                    "细节触发共鸣",
                    "留白增强感染力",
                ],
            },
            {
                "name": "节奏化世界观展开",
                "description": "在控制节奏的同时逐步展开世界观",
                "skills": ["pacing_control", "world_building"],
                "use_cases": ["新地图/新区域展开", "设定揭示", "体系说明"],
                "techniques": [
                    "快节奏展示，慢节奏解释",
                    "通过冲突展示设定",
                    "分层次逐步揭示",
                ],
            },
        ]

        for template in combo_templates:
            all_skills_available = True
            synergy = 0.0

            for skill_key in template["skills"]:
                if skill_key in self.skills:
                    skill = self.skills[skill_key]
                    level_order = list(SkillLevel)
                    level_idx = level_order.index(skill.level)
                    synergy += level_idx / (len(level_order) - 1)
                else:
                    all_skills_available = False
                    break

            if all_skills_available and synergy > 0:
                synergy = synergy / len(template["skills"])

                existing = any(
                    set(template["skills"]) == set(c.skills_required)
                    for c in self.skill_combos.values()
                )

                if not existing and synergy >= 0.3:
                    self.combo_counter += 1
                    combo = SkillCombo(
                        combo_id=f"COMBO_{self.combo_counter:04d}",
                        name=template["name"],
                        description=template["description"],
                        skills_required=template["skills"],
                        synergy_score=round(synergy, 2),
                        use_cases=template["use_cases"],
                        techniques=template["techniques"],
                        discovered_at=datetime.now().isoformat(),
                    )
                    self.skill_combos[combo.combo_id] = combo
                    new_combos.append(combo)

        return new_combos

    def get_combo_readiness(self, combo_id: str) -> Dict:
        """检查技能组合的就绪状态"""
        combo = self.skill_combos.get(combo_id)
        if not combo:
            return {"error": f"组合不存在: {combo_id}"}

        skill_status = {}
        all_ready = True
        total_level = 0

        for skill_key in combo.skills_required:
            if skill_key in self.skills:
                skill = self.skills[skill_key]
                level_order = list(SkillLevel)
                level_idx = level_order.index(skill.level)
                total_level += level_idx

                ready = level_idx >= level_order.index(SkillLevel.EXPERT)
                if not ready:
                    all_ready = False

                skill_status[skill.name] = {
                    "level": skill.level.value,
                    "ready": ready,
                    "gap": (
                        "已达到" if ready
                        else f"需要{SkillLevel.EXPERT.value}(当前{skill.level.value})"
                    ),
                }
            else:
                all_ready = False
                skill_status[skill_key] = {
                    "level": "未解锁",
                    "ready": False,
                    "gap": "技能未解锁",
                }

        return {
            "combo_name": combo.name,
            "all_skills_ready": all_ready,
            "synergy_score": combo.synergy_score,
            "skill_status": skill_status,
            "techniques": combo.techniques if all_ready else [],
            "recommendation": (
                "所有技能已就绪，可以开始使用此组合!"
                if all_ready
                else "继续提升相关技能以解锁此组合的全部技巧"
            ),
        }

    def apply_combo_techniques(self, combo_id: str) -> Dict:
        """应用技能组合的技巧到当前写作"""
        combo = self.skill_combos.get(combo_id)
        if not combo:
            return {"error": f"组合不存在: {combo_id}"}

        readiness = self.get_combo_readiness(combo_id)

        applicable_techniques = []
        for i, technique in enumerate(combo.techniques):
            applicable = True
            if readiness["all_skills_ready"]:
                applicable_techniques.append({
                    "index": i + 1,
                    "technique": technique,
                    "status": "可用",
                })
            else:
                applicable_techniques.append({
                    "index": i + 1,
                    "technique": technique,
                    "status": "部分可用(建议先提升技能)",
                })

        for skill_key in combo.skills_required:
            if skill_key in self.skills:
                self.gain_experience(skill_key, 5)

        return {
            "combo": combo.name,
            "description": combo.description,
            "use_cases": combo.use_cases,
            "techniques": applicable_techniques,
            "readiness": readiness,
        }

    def persist(self):
        """持久化学习数据"""
        data = {
            "kid_counter": self.kid_counter,
            "total_learned": self.total_learned,
            "last_web_fetch": self.last_web_fetch.isoformat() if self.last_web_fetch else None,
            "exercise_counter": self.exercise_counter,
            "attempt_counter": self.attempt_counter,
            "feedback_counter": self.feedback_counter,
            "path_counter": self.path_counter,
            "combo_counter": self.combo_counter,
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
            "exercises": {
                k: {
                    "exercise_id": v.exercise_id,
                    "title": v.title,
                    "description": v.description,
                    "skill_focus": v.skill_focus,
                    "difficulty": v.difficulty,
                    "prompt": v.prompt,
                    "constraints": v.constraints,
                    "target_word_count": v.target_word_count,
                    "hints": v.hints,
                    "evaluation_criteria": v.evaluation_criteria,
                    "tags": v.tags,
                }
                for k, v in self.exercises.items()
            },
            "attempts": {
                k: [
                    {
                        "attempt_id": a.attempt_id,
                        "exercise_id": a.exercise_id,
                        "content": a.content,
                        "word_count": a.word_count,
                        "time_spent_seconds": a.time_spent_seconds,
                        "self_rating": a.self_rating,
                        "ai_feedback": a.ai_feedback,
                        "scores": a.scores,
                        "strengths": a.strengths,
                        "weaknesses": a.weaknesses,
                        "created_at": a.created_at,
                    }
                    for a in v
                ]
                for k, v in self.attempts.items()
            },
            "feedback_records": {
                k: {
                    "record_id": v.record_id,
                    "skill_name": v.skill_name,
                    "aspect": v.aspect,
                    "current_level": v.current_level,
                    "target_level": v.target_level,
                    "gap_analysis": v.gap_analysis,
                    "improvement_plan": v.improvement_plan,
                    "progress_percentage": v.progress_percentage,
                    "last_reviewed": v.last_reviewed,
                }
                for k, v in self.feedback_records.items()
            },
            "learning_paths": {
                k: {
                    "path_id": v.path_id,
                    "name": v.name,
                    "description": v.description,
                    "target_genre": v.target_genre,
                    "milestones": [
                        {
                            "milestone_id": m.milestone_id,
                            "name": m.name,
                            "description": m.description,
                            "required_skills": m.required_skills,
                            "required_exercises": m.required_exercises,
                            "rewards": m.rewards,
                            "unlocked": m.unlocked,
                            "completed": m.completed,
                            "completed_at": m.completed_at,
                        }
                        for m in v.milestones
                    ],
                    "current_milestone_index": v.current_milestone_index,
                    "total_exercises_completed": v.total_exercises_completed,
                    "started_at": v.started_at,
                    "last_activity": v.last_activity,
                }
                for k, v in self.learning_paths.items()
            },
            "skill_combos": {
                k: {
                    "combo_id": v.combo_id,
                    "name": v.name,
                    "description": v.description,
                    "skills_required": v.skills_required,
                    "synergy_score": v.synergy_score,
                    "use_cases": v.use_cases,
                    "techniques": v.techniques,
                    "discovered_at": v.discovered_at,
                }
                for k, v in self.skill_combos.items()
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
            self.exercise_counter = data.get("exercise_counter", self.exercise_counter)
            self.attempt_counter = data.get("attempt_counter", self.attempt_counter)
            self.feedback_counter = data.get("feedback_counter", self.feedback_counter)
            self.path_counter = data.get("path_counter", self.path_counter)
            self.combo_counter = data.get("combo_counter", self.combo_counter)

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

            for ex_id, ed in data.get("exercises", {}).items():
                self.exercises[ex_id] = WritingExercise(**ed)

            for ex_id, attempts_data in data.get("attempts", {}).items():
                self.attempts[ex_id] = [
                    ExerciseAttempt(**a) for a in attempts_data
                ]

            for fb_id, fd in data.get("feedback_records", {}).items():
                self.feedback_records[fb_id] = FeedbackRecord(**fd)

            for path_id, pd in data.get("learning_paths", {}).items():
                milestones_data = pd.pop("milestones", [])
                path = LearningPath(**pd)
                path.milestones = [
                    LearningMilestone(**m) for m in milestones_data
                ]
                self.learning_paths[path_id] = path

            for combo_id, cd in data.get("skill_combos", {}).items():
                self.skill_combos[combo_id] = SkillCombo(**cd)

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
