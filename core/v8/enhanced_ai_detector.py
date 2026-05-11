#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS AI检测机制 — EnhancedAIDetector v3.0
融合多维度AI写作模式检测引擎

核心检测维度:
- 24种AI写作模式 — 四层检测体系(内容/语言/风格/沟通)
- 填充短语检测 — 二元对比/戏剧化断句/掌声句/表演式诚实
- 三级检测体系 — Tier1(立即标记)/Tier2(强指标)/Tier3(中等指标)
- 五维质量评分 — 直接性/节奏感/信任度/真实性/简洁性
- 情感平淡检测 — 情感平淡/词汇同质化/互联网用语过度

升级内容 v3.0:
1. Burstiness计算 — B=(σ/μ)×100, B<30=AI, B>50=人类
2. 结构分析 — 段落均匀度/对称章节/主题句模板检测
3. 三级检测体系 — Tier1(立即标记)/Tier2(强指标)/Tier3(中等指标)
4. 30秒测试 — "这段文字能发给行业里任何人吗？"
5. 新增填充短语模式 — 二元对比/戏剧化断句/掌声句/表演式诚实
6. 新增情感平淡模式 — 情感平淡/词汇同质化/互联网用语过度
"""

import re
import random
import json
import math
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from collections import Counter


@dataclass
class HumanizerPattern:
    """NWACS AI写作模式检测单元"""
    id: int
    name: str
    category: str  # content/language/style/communication
    keywords: List[str] = field(default_factory=list)
    regex_patterns: List[str] = field(default_factory=list)
    description: str = ""
    severity: float = 0.5  # 0-1, 越高越严重


@dataclass
class DetectionReport:
    """检测报告 v3.0"""
    overall_score: int
    level: str  # low/medium/high/very_high
    word_layer: Dict
    sentence_layer: Dict
    semantic_layer: Dict
    humanizer_layer: Dict = field(default_factory=dict)
    quality_scores: Dict = field(default_factory=dict)
    soul_check: Dict = field(default_factory=dict)
    burstiness: Dict = field(default_factory=dict)        # v3.0: burstiness分析
    structure_analysis: Dict = field(default_factory=dict) # v3.0: 结构分析
    tier_detection: Dict = field(default_factory=dict)     # v3.0: 三级检测
    thirty_second_test: Dict = field(default_factory=dict) # v3.0: 30秒测试
    hot_spots: List[Dict] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)


@dataclass
class StructuralIssue:
    """结构层问题"""
    category: str  # uniformity/symmetry/template/rhythm
    description: str
    severity: float
    details: Dict = field(default_factory=dict)


@dataclass
class TierPattern:
    """三级检测模式"""
    tier: int  # 1/2/3
    name: str
    patterns: List[str] = field(default_factory=list)
    regex: List[str] = field(default_factory=list)
    confidence: float = 0.5  # AI概率


@dataclass
class RewriteReport:
    """去痕报告"""
    original_score: int
    final_score: int
    reduction: int
    changes_made: int
    replaced_words: List[Tuple[str, str]]
    modified_sentences: int
    quality_before: Dict = field(default_factory=dict)
    quality_after: Dict = field(default_factory=dict)


class EnhancedAIDetector:
    """增强版AI检测器 v3.0 — 多项目融合"""

    def __init__(self):
        self._init_word_layer()
        self._init_sentence_layer()
        self._init_semantic_layer()
        self._init_humanizer_patterns()
        self._init_quality_dimensions()
        self._init_filler_patterns()
        self._init_tier_patterns()
        self._init_structure_checks()

    # ============================================================
    # 原有三层检测 (保留并增强)
    # ============================================================

    def _init_word_layer(self):
        """词汇层特征库 — NWACS 高频AI词汇检测"""
        self.high_risk_words = {
            "AI高频词": [
                "此外", "至关重要", "深入探讨", "强调", "持久的",
                "增强", "培养", "获得", "突出", "相互作用",
                "复杂", "复杂性", "格局", "关键性的", "展示",
                "织锦", "证明", "宝贵的", "充满活力的",
            ],
            "夸大象征": [
                "作为", "标志着", "见证了", "是……的体现", "是……的证明",
                "是……的提醒", "极其重要的", "核心的", "关键性的作用",
                "凸显了其重要性", "反映了更广泛的", "象征着其持续的",
                "为……奠定基础", "标志着……塑造着", "关键转折点",
                "不断演变的格局", "不可磨灭的印记", "深深植根于",
            ],
            "宣传广告语": [
                "拥有", "坐落于", "位于……的中心", "令人叹为观止的",
                "必游之地", "迷人的", "开创性的", "著名的",
                "自然之美", "致力于", "深刻的", "丰富的",
            ],
            "模糊归因": [
                "行业报告显示", "观察者指出", "专家认为",
                "一些批评者认为", "多个来源", "多个出版物",
            ],
            "否定式排比": [
                "不仅……而且", "不仅仅是……而是",
                "这不只是……这更是", "并非……而是",
            ],
            "填充短语": [
                "值得注意的是", "为了实现这一目标",
                "由于……的事实", "在这个时间点",
                "在您需要……的情况下", "具有……的能力",
            ],
            "通用积极结论": [
                "未来看起来光明", "激动人心的时代即将到来",
                "向正确方向迈出的重要一步", "继续追求卓越",
            ],
        }

        self.medium_risk_words = {
            "三段式法则": [
                "无缝、直观和强大", "创新、灵感和行业洞察",
                "主题演讲、小组讨论和社交机会",
            ],
            "系动词回避": [
                "作为……充当", "代表……标志着",
                "拥有……设有", "提供……展示",
            ],
            "虚假范围": [
                "从……到……", "从X到Y",
            ],
            "过度限定": [
                "可以潜在地可能被认为", "可能会对……产生一些影响",
                "在一定程度上", "在某种意义上",
            ],
        }

        self.low_risk_words = {
            "过渡词": ["此时", "此刻", "这时", "那时候", "就在这时"],
            "强调词": ["确实", "的确", "真的", "实在", "真正"],
            "协作痕迹": [
                "希望这对您有帮助", "当然", "一定",
                "您说得完全正确", "您想要", "请告诉我",
                "这是一个……的概述",
            ],
            "知识截止免责": [
                "截至", "根据我最后的训练更新",
                "虽然具体细节有限", "基于可用信息",
            ],
        }

    def _init_sentence_layer(self):
        """句式层特征库"""
        self.sentence_patterns = [
            (r"^(然而|但是|可是|不过|却)", 0.4, "转折句开头"),
            (r"^(他|她|它|这|那)\s*(站起身|转过身|抬起头|低下头|走出|走进|来到|回到)", 0.5, "主语+动作模板"),
            (r"^在.*?(的|中|下|里|上)", 0.3, "在...的/中/下句式"),
            (r"^随着.*?(，|。)", 0.3, "随着...句式"),
            (r"^只见.*?(，|。)", 0.4, "只见...句式"),
            (r"^只(听|感|觉).*?(，|。)", 0.4, "只听/感/觉...句式"),
            (r"^一股.*?(的|之感|之情)", 0.3, "一股...的句式"),
            (r"^.*?，.*?，.*?，.*?，", 0.2, "逗号密集句"),
            (r"^.{50,}$", 0.2, "超长句"),
            (r"^.{1,5}$", 0.1, "超短句密集"),
            (r"—.*?—", 0.3, "破折号过度使用"),           # 模式13
            (r"^.*?不仅.*?而且.*?$", 0.4, "否定式排比"),   # 模式9
        ]

    def _init_semantic_layer(self):
        """语义层特征库"""
        self.semantic_patterns = {
            "情感递进模板": r".*?(不禁|不由得|忍不住).*?(激动|感动|兴奋|紧张|害怕).*?",
            "环境呼应模板": r".*?(阳光|月光|星光|灯光).*?(洒|照|映|落).*?",
            "心理活动模板": r".*?(心中|心里|内心).*?(想|思索|暗忖|暗道|默念).*?",
            "动作链模板": r".*?(站起身|转过身).*?(走|跑|冲|奔).*?",
            "总结升华模板": r".*?(这|那)\s*(一刻|一瞬间|一刹那).*?(终于|才|仿佛).*?",
            "肤浅分析模板": r".*?(突出|强调|彰显|确保|反映|象征|为……做出贡献|培养|促进|涵盖|展示).*?$",  # 模式3
            "提纲式挑战模板": r".*?(尽管|虽然).*?(面临|存在).*?(挑战|问题).*?",  # 模式6
        }

    # ============================================================
    # NWACS 24种AI写作模式 (核心检测引擎)
    # ============================================================

    def _init_humanizer_patterns(self):
        """初始化 NWACS 24种AI写作模式"""
        self.humanizer_patterns: List[HumanizerPattern] = []

        # === 内容模式 (6种) ===
        self.humanizer_patterns.append(HumanizerPattern(
            id=1, category="content",
            name="过度强调意义和遗产",
            keywords=["作为", "标志着", "见证了", "是……的体现", "是……的证明",
                       "极其重要的", "关键性的作用", "凸显了其重要性",
                       "反映了更广泛的", "象征着其持续的", "为……奠定基础",
                       "关键转折点", "不断演变的格局", "不可磨灭的印记"],
            regex_patterns=[r"作为.*?的(证明|体现|提醒|象征)",
                          r"标志着.*?的(关键时刻|转变|里程碑)",
                          r"为.*?奠定了.*?的基础"],
            description="LLM通过添加关于任意方面如何代表或促进更广泛主题的陈述来夸大重要性",
            severity=0.8,
        ))

        self.humanizer_patterns.append(HumanizerPattern(
            id=2, category="content",
            name="过度强调知名度和媒体报道",
            keywords=["独立报道", "地方媒体", "国家媒体", "区域媒体",
                       "由知名专家撰写", "活跃的社交媒体账号"],
            regex_patterns=[r"被.*?(引用|报道|提及)",
                          r"在社交媒体上拥有.*?粉丝"],
            description="LLM反复强调知名度主张，通常列出来源而不提供上下文",
            severity=0.6,
        ))

        self.humanizer_patterns.append(HumanizerPattern(
            id=3, category="content",
            name="以-ing结尾的肤浅分析",
            keywords=["突出", "强调", "彰显", "确保", "反映", "象征",
                       "为……做出贡献", "培养", "促进", "涵盖", "展示"],
            regex_patterns=[r"(突出|强调|彰显|确保|反映|象征|培养|促进|涵盖|展示).*?$"],
            description="AI在句子末尾添加现在分词短语来增加虚假深度",
            severity=0.7,
        ))

        self.humanizer_patterns.append(HumanizerPattern(
            id=4, category="content",
            name="宣传和广告式语言",
            keywords=["拥有", "坐落于", "位于……的中心", "令人叹为观止的",
                       "必游之地", "迷人的", "开创性的", "著名的",
                       "自然之美", "致力于", "深刻的", "充满活力的", "丰富的"],
            regex_patterns=[r"坐落于.*?的.*?(中心|区域|地带)",
                          r"拥有.*?(丰富的|深厚的|悠久的)"],
            description="LLM倾向使用夸张的宣传性语言，尤其对文化遗产话题",
            severity=0.7,
        ))

        self.humanizer_patterns.append(HumanizerPattern(
            id=5, category="content",
            name="模糊归因和含糊措辞",
            keywords=["行业报告显示", "观察者指出", "专家认为",
                       "一些批评者认为", "多个来源", "据称", "据悉"],
            regex_patterns=[r"(专家|观察者|批评者|分析人士).*?(认为|指出|表示|称)",
                          r"(多个|众多|大量).*?(来源|报告|研究|出版物)"],
            description="AI将观点归因于模糊的权威而不提供具体来源",
            severity=0.6,
        ))

        self.humanizer_patterns.append(HumanizerPattern(
            id=6, category="content",
            name="提纲式的挑战与未来展望",
            keywords=["尽管其", "面临若干挑战", "尽管存在这些挑战",
                       "挑战与遗产", "未来展望", "未来的道路"],
            regex_patterns=[r"尽管.*?(面临|存在).*?(挑战|问题|困难)",
                          r"(未来展望|未来的道路|前景展望)"],
            description="LLM生成公式化的挑战部分，缺乏具体内容",
            severity=0.5,
        ))

        # === 语言和语法模式 (6种) ===
        self.humanizer_patterns.append(HumanizerPattern(
            id=7, category="language",
            name="过度使用的AI词汇",
            keywords=["此外", "至关重要", "深入探讨", "强调", "持久的",
                       "增强", "培养", "获得", "突出", "相互作用",
                       "复杂", "复杂性", "格局", "关键性的", "展示",
                       "织锦", "证明", "宝贵的", "充满活力的", "与……保持一致"],
            regex_patterns=[],
            description="这些词在2023年后的AI文本中出现频率远高于人类写作",
            severity=0.9,
        ))

        self.humanizer_patterns.append(HumanizerPattern(
            id=8, category="language",
            name="避免使用'是'(系动词回避)",
            keywords=["作为", "代表", "标志着", "充当", "拥有", "设有", "提供"],
            regex_patterns=[r"(作为|代表|标志着|充当)\s*(一个|一种|一项)"],
            description="LLM用复杂的结构替代简单的系动词'是'",
            severity=0.5,
        ))

        self.humanizer_patterns.append(HumanizerPattern(
            id=9, category="language",
            name="否定式排比",
            keywords=["不仅……而且", "不仅仅是……而是",
                       "这不只是……这更是", "并非……而是"],
            regex_patterns=[r"不仅.*?而且",
                          r"不仅仅是.*?而是",
                          r"这不只是.*?这更是"],
            description="'不仅……而且……'等结构被过度使用",
            severity=0.6,
        ))

        self.humanizer_patterns.append(HumanizerPattern(
            id=10, category="language",
            name="三段式法则过度使用",
            keywords=[],
            regex_patterns=[r"(?:[^，。]+，){2,}[^，。]+(?:和|与|及)[^，。]+",
                          r"[^，。]+、[^，。]+和[^，。]+"],
            description="LLM强行将想法分成三组以显得全面",
            severity=0.5,
        ))

        self.humanizer_patterns.append(HumanizerPattern(
            id=11, category="language",
            name="刻意换词(同义词循环)",
            keywords=[],
            regex_patterns=[r"(主人公|主要角色|中心人物|英雄).*?(主人公|主要角色|中心人物|英雄)"],
            description="AI因重复惩罚代码导致过度使用同义词替换同一实体",
            severity=0.4,
        ))

        self.humanizer_patterns.append(HumanizerPattern(
            id=12, category="language",
            name="虚假范围",
            keywords=["从……到……"],
            regex_patterns=[r"从.*?到.*?的.*?(旅程|转变|演变|过渡)"],
            description="LLM使用'从X到Y'结构但X和Y不在有意义的尺度上",
            severity=0.4,
        ))

        # === 风格模式 (6种) ===
        self.humanizer_patterns.append(HumanizerPattern(
            id=13, category="style",
            name="破折号过度使用",
            keywords=[],
            regex_patterns=[r"—"],
            description="LLM使用破折号(—)比人类更频繁，模仿有力销售文案",
            severity=0.5,
        ))

        self.humanizer_patterns.append(HumanizerPattern(
            id=14, category="style",
            name="粗体过度使用",
            keywords=[],
            regex_patterns=[r"\*\*[^*]+\*\*"],
            description="AI聊天机器人机械地用粗体强调短语",
            severity=0.3,
        ))

        self.humanizer_patterns.append(HumanizerPattern(
            id=15, category="style",
            name="内联标题垂直列表",
            keywords=[],
            regex_patterns=[r"[-•]\s*\*\*[^*:]+\*\*\s*[:：]"],
            description="AI输出列表，项目以粗体标题开头后跟冒号",
            severity=0.4,
        ))

        self.humanizer_patterns.append(HumanizerPattern(
            id=16, category="style",
            name="标题中的标题大写",
            keywords=[],
            regex_patterns=[],
            description="AI将标题中所有主要单词大写(中文中较少见)",
            severity=0.1,
        ))

        self.humanizer_patterns.append(HumanizerPattern(
            id=17, category="style",
            name="表情符号装饰",
            keywords=[],
            regex_patterns=[r"[🚀💡✅🎯🔥💪✨🎉📊📈🔍💼🏆🎨🔧📝🎓🌟💎⚡🔮🎭]"],
            description="AI聊天机器人经常用表情符号装饰标题或项目符号",
            severity=0.3,
        ))

        self.humanizer_patterns.append(HumanizerPattern(
            id=18, category="style",
            name="弯引号/英文引号",
            keywords=[],
            regex_patterns=[r"[\u201c\u201d\u2018\u2019]"],
            description="ChatGPT使用弯引号而非直引号，中文中使用英文引号",
            severity=0.2,
        ))

        # === 交流模式和填充词 (6种) ===
        self.humanizer_patterns.append(HumanizerPattern(
            id=19, category="communication",
            name="协作交流痕迹",
            keywords=["希望这对您有帮助", "当然", "一定",
                       "您说得完全正确", "您想要", "请告诉我",
                       "这是一个……的概述", "如果您想让我扩展"],
            regex_patterns=[r"希望这(对您|对你)有(帮助|所帮助)",
                          r"(如果您|如果你).*?(请告诉我|请让我知道)"],
            description="作为聊天机器人对话的文本被粘贴为内容",
            severity=0.8,
        ))

        self.humanizer_patterns.append(HumanizerPattern(
            id=20, category="communication",
            name="知识截止日期免责声明",
            keywords=["截至", "根据我最后的训练更新",
                       "虽然具体细节有限", "基于可用信息",
                       "在现成资料中没有广泛记录"],
            regex_patterns=[r"截至\s*\d{4}年",
                          r"根据我.*?的(训练|知识|数据)",
                          r"虽然.*?(有限|稀缺|不多)"],
            description="关于信息不完整的AI免责声明留在文本中",
            severity=0.7,
        ))

        self.humanizer_patterns.append(HumanizerPattern(
            id=21, category="communication",
            name="谄媚/卑躬屈膝的语气",
            keywords=["好问题", "您说得完全正确", "这是一个很好的观点",
                       "您的观察非常敏锐", "我很高兴您问到这个问题"],
            regex_patterns=[r"(好问题|很好的问题|非常好的问题)",
                          r"(您说得|你说得).*?(正确|对|很有道理)"],
            description="过于积极、讨好的语言",
            severity=0.6,
        ))

        self.humanizer_patterns.append(HumanizerPattern(
            id=22, category="communication",
            name="填充短语",
            keywords=["值得注意的是", "为了实现这一目标",
                       "由于……的事实", "在这个时间点",
                       "在您需要……的情况下", "具有……的能力",
                       "数据显示", "研究表明"],
            regex_patterns=[r"值得(注意|关注|一提)的是",
                          r"为了(实现|达成|完成)这一目标",
                          r"在这个(时间点|阶段|时刻)"],
            description="冗余的填充短语使文本臃肿",
            severity=0.5,
        ))

        self.humanizer_patterns.append(HumanizerPattern(
            id=23, category="communication",
            name="过度限定",
            keywords=["可以潜在地可能被认为", "可能会对……产生一些影响",
                       "在一定程度上", "在某种意义上", "似乎", "或许"],
            regex_patterns=[r"(可能|或许|似乎|好像).*?(可能|或许|似乎|好像)"],
            description="过度限定陈述使文本缺乏自信",
            severity=0.4,
        ))

        self.humanizer_patterns.append(HumanizerPattern(
            id=24, category="communication",
            name="通用积极结论",
            keywords=["未来看起来光明", "激动人心的时代即将到来",
                       "向正确方向迈出的重要一步", "继续追求卓越",
                       "前景一片光明", "未来可期"],
            regex_patterns=[r"(未来|前景|前途).*?(光明|美好|可期|无限)",
                          r"向.*?方向.*?迈出.*?(重要|关键|坚实)的.*?(一步|步伐)"],
            description="模糊的乐观结尾，缺乏具体内容",
            severity=0.5,
        ))

    # ============================================================
    # 五维度质量评分系统 (新增)
    # ============================================================

    def _init_quality_dimensions(self):
        """初始化五维度质量评分标准"""
        self.quality_dimensions = {
            "directness": {
                "name": "直接性",
                "description": "直接陈述事实还是绕圈宣告？",
                "weight": 0.20,
                "anti_patterns": [
                    r"作为.*?的(证明|体现|象征)",
                    r"标志着.*?的",
                    r"值得注意的是",
                    r"需要指出的是",
                    r"不可否认的是",
                ],
            },
            "rhythm": {
                "name": "节奏",
                "description": "句子长度是否变化？",
                "weight": 0.20,
                "check": self._check_rhythm,
            },
            "trust": {
                "name": "信任度",
                "description": "是否尊重读者智慧？",
                "weight": 0.20,
                "anti_patterns": [
                    r"也就是说",
                    r"换句话说",
                    r"这意味着",
                    r"顾名思义",
                    r"显而易见",
                ],
            },
            "authenticity": {
                "name": "真实性",
                "description": "听起来像真人说话吗？",
                "weight": 0.20,
                "anti_patterns": [
                    r"无缝.*?直观.*?强大",
                    r"创新.*?灵感.*?洞察",
                    r"不仅.*?而且",
                    r"希望这(对您|对你)有(帮助|所帮助)",
                ],
            },
            "conciseness": {
                "name": "精炼度",
                "description": "还有可删减的内容吗？",
                "weight": 0.20,
                "anti_patterns": [
                    r"在这个时间点",
                    r"由于.*?的事实",
                    r"为了实现这一目标",
                    r"在.*?的情况下",
                    r"具有.*?的能力",
                ],
            },
        }

    def _check_rhythm(self, text: str) -> float:
        """检查句子节奏变化"""
        sentences = re.split(r'[。！？\n]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        if len(sentences) < 3:
            return 0.5

        lengths = [len(s) for s in sentences]
        avg_len = sum(lengths) / len(lengths)

        same_length_count = 0
        for i in range(len(lengths) - 1):
            if abs(lengths[i] - lengths[i + 1]) < 5:
                same_length_count += 1

        ratio = same_length_count / max(len(lengths) - 1, 1)
        return max(0, 1 - ratio)

    # ============================================================
    # v3.0 新增: 填充短语与公式化结构检测
    # ============================================================

    def _init_filler_patterns(self):
        """初始化填充短语和公式化结构"""
        self.filler_phrases = {
            "喉清开场": [
                "事情是这样的", "这么说吧", "你听我说", "听好了",
                "Here's the thing", "Let me be clear", "The truth is",
                "I'm going to be honest", "Full stop",
            ],
            "强调拐杖": [
                "这一点很重要", "这很关键", "这才是重点",
                "This matters because", "The real question is",
                "And that's okay", "Let that sink in",
            ],
            "表演式诚实": [
                "说实话", "老实说", "不瞒你说", "讲真",
                "To be honest", "I'll be honest with you",
                "Not gonna lie",
            ],
            "掌声句": [
                "这就是关键所在", "这才是真正的力量",
                "That's it. That's the thing.", "Structure matters.",
                "Clarity. That's the foundation.",
            ],
            "二元对比结构": [
                "不是……而是……", "并非……而是……",
                "It's not X. It's Y.", "Not because X. Because Y.",
            ],
            "戏剧化断句": [
                "短句。断句。强调。", "不。可。能。",
            ],
            "问答自嗨": [
                "为什么？因为……", "怎么做？很简单……",
                "答案是什么？……", "So what's the answer?",
            ],
            "通用开场白": [
                "在当今……时代", "随着……的发展",
                "In today's fast-paced world",
                "In the rapidly evolving landscape",
            ],
            "空洞大词": [
                "赋能", "闭环", "智慧时代", "底层逻辑",
                "降维打击", "颗粒度", "对齐", "拉通",
                "leveraging", "synergies", "ecosystem",
            ],
        }

        self.slop_structures = {
            "三段式列举": r"([^，。]+、[^，。]+和[^，。]+)",
            "二元对比": r"(不是|并非|不是……而是).*?(而是|而是……)",
            "问答自答": r"(为什么|怎么做|答案是什么).*?[？?].*?(因为|很简单|……)",
            "掌声句模式": r"^.{1,15}$",  # 极短独立句
            "喉清开场": r"^(事情是这样的|这么说吧|你听我说|Here's the thing)",
        }

    # ============================================================
    # v3.0 新增: 三级检测体系 (claude-slop-detector)
    # ============================================================

    def _init_tier_patterns(self):
        """初始化三级检测模式"""
        self.tier_patterns: List[TierPattern] = []

        # === Tier 1: 几乎肯定是AI — 立即标记 ===
        self.tier_patterns.append(TierPattern(
            tier=1, name="人工热情",
            patterns=["delve into", "the answer surprised me",
                       "here's what blew my mind", "game-changing",
                       "让人震惊的是", "颠覆性的", "划时代的"],
            confidence=0.95,
        ))
        self.tier_patterns.append(TierPattern(
            tier=1, name="协作痕迹残留",
            patterns=["Certainly, here is", "I'm sorry, but I don't have",
                       "希望这对您有帮助", "如果您想让我扩展",
                       "这是一个……的概述"],
            confidence=0.99,
        ))
        self.tier_patterns.append(TierPattern(
            tier=1, name="签名词密集",
            patterns=["delve", "tapestry", "landscape", "crucial",
                       "intricate", "multifaceted", "paramount"],
            regex=[r"(delve|tapestry|landscape|crucial|intricate)"],
            confidence=0.90,
        ))
        self.tier_patterns.append(TierPattern(
            tier=1, name="完美三段式重复",
            patterns=[],
            regex=[r"([^，。]+、[^，。]+和[^，。]+.*?){3,}"],
            confidence=0.90,
        ))

        # === Tier 2: 强指标 — 70-90% AI概率 ===
        self.tier_patterns.append(TierPattern(
            tier=2, name="低Burstiness",
            patterns=[],
            regex=[],
            confidence=0.85,
        ))
        self.tier_patterns.append(TierPattern(
            tier=2, name="段落长度均匀",
            patterns=[],
            regex=[],
            confidence=0.75,
        ))
        self.tier_patterns.append(TierPattern(
            tier=2, name="破折号高频",
            patterns=[],
            regex=[r"—"],
            confidence=0.80,
        ))
        self.tier_patterns.append(TierPattern(
            tier=2, name="设置短语密集",
            patterns=["Here's", "The truth is", "Let me be clear",
                       "这么说吧", "事情是这样的"],
            confidence=0.70,
        ))
        self.tier_patterns.append(TierPattern(
            tier=2, name="公式化结构重复",
            patterns=[],
            regex=[r"(不是.*?而是.*?){2,}"],
            confidence=0.85,
        ))

        # === Tier 3: 中等指标 — 40-60% AI概率 ===
        self.tier_patterns.append(TierPattern(
            tier=3, name="企业黑话密度",
            patterns=["leverage", "synergy", "ecosystem", "robust",
                       "streamline", "facilitate", "optimize",
                       "赋能", "闭环", "对齐", "拉通", "颗粒度"],
            confidence=0.50,
        ))
        self.tier_patterns.append(TierPattern(
            tier=3, name="牛津逗号一致性",
            patterns=[],
            regex=[],
            confidence=0.40,
        ))
        self.tier_patterns.append(TierPattern(
            tier=3, name="问答节奏",
            patterns=[],
            regex=[r"(为什么|如何|怎样).*?[？?].*?(因为|首先|答案)"],
            confidence=0.55,
        ))
        self.tier_patterns.append(TierPattern(
            tier=3, name="项目符号完美平行",
            patterns=[],
            regex=[],
            confidence=0.60,
        ))
        self.tier_patterns.append(TierPattern(
            tier=3, name="通用热情",
            patterns=["Great question!", "Excellent point!",
                       "好问题！", "非常好的观点！"],
            confidence=0.45,
        ))

    # ============================================================
    # v3.0 新增: 结构分析
    # ============================================================

    def _init_structure_checks(self):
        """初始化结构层检查"""
        self.structure_checks = {
            "段落均匀度": "检查所有段落长度是否过于均匀",
            "对称章节": "检查章节/段落是否有相同的结构弧线",
            "主题句模板": "检查是否每段都是主题句-论据-结论模式",
            "句子节奏均匀": "检查句子长度是否像节拍器",
            "过度平衡": "检查章节是否被过度平衡（每节相同长度）",
        }

    # ============================================================
    # v3.0 新增: Burstiness 计算
    # ============================================================

    def _calculate_burstiness(self, text: str) -> Dict:
        """计算 Burstiness — 句子长度变化率

        B = (σ / μ) × 100
        B < 30: 可能是AI (节拍器节奏)
        B > 50: 可能是人类 (爵士乐节奏)

        基于对大量文章的分析
        """
        sentences = re.split(r'[。！？\n]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        if len(sentences) < 5:
            return {
                "burstiness": 0,
                "level": "insufficient_data",
                "interpretation": "句子数量不足，无法计算",
                "sentence_count": len(sentences),
            }

        lengths = [len(s) for s in sentences]
        mean_len = sum(lengths) / len(lengths)

        if mean_len == 0:
            return {"burstiness": 0, "level": "error", "interpretation": "计算错误"}

        variance = sum((x - mean_len) ** 2 for x in lengths) / len(lengths)
        std_dev = math.sqrt(variance)

        burstiness = (std_dev / mean_len) * 100

        if burstiness < 20:
            level = "very_low"
            interpretation = "句子长度极度均匀，强烈AI特征（节拍器节奏）"
        elif burstiness < 30:
            level = "low"
            interpretation = "句子长度较均匀，可能是AI（节拍器节奏）"
        elif burstiness < 50:
            level = "medium"
            interpretation = "句子长度有一定变化，可能是AI或轻度编辑"
        elif burstiness < 70:
            level = "high"
            interpretation = "句子长度变化较大，接近人类写作"
        else:
            level = "very_high"
            interpretation = "句子长度剧烈变化，强烈人类特征（爵士乐节奏）"

        length_distribution = {
            "short (<10字)": sum(1 for l in lengths if l < 10),
            "medium (10-30字)": sum(1 for l in lengths if 10 <= l <= 30),
            "long (>30字)": sum(1 for l in lengths if l > 30),
        }

        return {
            "burstiness": round(burstiness, 1),
            "level": level,
            "interpretation": interpretation,
            "mean_length": round(mean_len, 1),
            "std_dev": round(std_dev, 1),
            "sentence_count": len(sentences),
            "length_distribution": length_distribution,
            "thresholds": {"ai_likely": "<30", "human_likely": ">50"},
        }

    # ============================================================
    # v3.0 新增: 结构分析
    # ============================================================

    def _analyze_structure(self, text: str) -> Dict:
        """结构层分析 — 段落均匀度/对称性/模板检测"""
        issues = []

        paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
        if len(paragraphs) < 3:
            return {"issues": [], "score": 10, "paragraph_count": len(paragraphs)}

        # 1. 段落均匀度检查
        para_lengths = [len(p) for p in paragraphs]
        para_mean = sum(para_lengths) / len(para_lengths)
        para_variance = sum((x - para_mean) ** 2 for x in para_lengths) / len(para_lengths)
        para_cv = (math.sqrt(para_variance) / para_mean) if para_mean > 0 else 0

        if para_cv < 0.3:
            issues.append({
                "category": "uniformity",
                "description": "段落长度过于均匀（CV<0.3），AI典型特征",
                "severity": 0.8,
                "details": {"cv": round(para_cv, 2), "mean_length": round(para_mean, 0)},
            })

        # 2. 对称章节检查
        if len(paragraphs) >= 4:
            first_half_avg = sum(para_lengths[:len(paragraphs)//2]) / (len(paragraphs)//2)
            second_half_avg = sum(para_lengths[len(paragraphs)//2:]) / (len(paragraphs) - len(paragraphs)//2)
            symmetry_ratio = abs(first_half_avg - second_half_avg) / max(first_half_avg, second_half_avg, 1)

            if symmetry_ratio < 0.15:
                issues.append({
                    "category": "symmetry",
                    "description": "前后半部分段落长度高度对称，AI典型特征",
                    "severity": 0.6,
                    "details": {"symmetry_ratio": round(symmetry_ratio, 2)},
                })

        # 3. 主题句-论据-结论模板检测
        template_count = 0
        for para in paragraphs:
            sentences_in_para = re.split(r'[。！？]', para)
            sentences_in_para = [s.strip() for s in sentences_in_para if s.strip()]
            if len(sentences_in_para) >= 3:
                first = sentences_in_para[0]
                last = sentences_in_para[-1]
                if (len(first) < 30 and len(last) < 30 and
                    (re.search(r'(是|在于|需要|应该|可以|必须)', first) or
                     re.search(r'(因此|所以|总之|综上|由此可见)', last))):
                    template_count += 1

        if template_count >= len(paragraphs) * 0.5:
            issues.append({
                "category": "template",
                "description": f"主题句-论据-结论模板段落过多({template_count}/{len(paragraphs)})",
                "severity": 0.7,
                "details": {"template_count": template_count, "total": len(paragraphs)},
            })

        # 4. 句子节奏均匀度
        all_sentences = re.split(r'[。！？\n]+', text)
        all_sentences = [s.strip() for s in all_sentences if s.strip()]
        if len(all_sentences) >= 5:
            sent_lengths = [len(s) for s in all_sentences]
            sent_mean = sum(sent_lengths) / len(sent_lengths)
            consecutive_same = 0
            for i in range(len(sent_lengths) - 2):
                if (abs(sent_lengths[i] - sent_lengths[i+1]) < 3 and
                    abs(sent_lengths[i+1] - sent_lengths[i+2]) < 3):
                    consecutive_same += 1

            if consecutive_same >= 3:
                issues.append({
                    "category": "rhythm",
                    "description": f"连续3句以上长度相同出现{consecutive_same}次，节奏单调",
                    "severity": 0.65,
                    "details": {"consecutive_same_count": consecutive_same},
                })

        score = max(0, 10 - len(issues) * 2.5)
        return {
            "issues": issues,
            "score": round(score, 1),
            "max_score": 10,
            "paragraph_count": len(paragraphs),
            "level": "优秀" if score >= 8 else "良好" if score >= 6 else "需要修订",
        }

    # ============================================================
    # v3.0 新增: 三级检测
    # ============================================================

    def _detect_tier_patterns(self, text: str) -> Dict:
        """三级检测 — Tier1(立即标记)/Tier2(强指标)/Tier3(中等指标)"""
        tier_results = {1: [], 2: [], 3: []}
        tier_scores = {1: 0, 2: 0, 3: 0}

        for tp in self.tier_patterns:
            match_count = 0
            for pat in tp.patterns:
                match_count += text.count(pat)
            for regex_str in tp.regex:
                try:
                    match_count += len(re.findall(regex_str, text))
                except re.error:
                    pass

            if match_count > 0:
                entry = {
                    "name": tp.name,
                    "matches": match_count,
                    "confidence": tp.confidence,
                }
                tier_results[tp.tier].append(entry)
                tier_scores[tp.tier] += match_count * tp.confidence * 10

        tier_scores = {k: min(int(v), 100) for k, v in tier_scores.items()}

        overall_tier_score = (
            tier_scores[1] * 0.5 +
            tier_scores[2] * 0.35 +
            tier_scores[3] * 0.15
        )

        return {
            "tier1_immediate_flags": tier_results[1],
            "tier2_strong_indicators": tier_results[2],
            "tier3_moderate_indicators": tier_results[3],
            "tier_scores": tier_scores,
            "overall_tier_score": round(overall_tier_score, 1),
            "total_flags": sum(len(v) for v in tier_results.values()),
        }

    # ============================================================
    # v3.0 新增: 30秒测试
    # ============================================================

    def _thirty_second_test(self, text: str) -> Dict:
        """30秒测试 — "这段文字能发给行业里任何人吗？"

        如果答案是"是"——这就是AI slop。
        AI默认生成普遍适用的内容——技术上对每个人都有效，但与任何人都没有共鸣。
        """
        generic_indicators = []

        has_specific_names = bool(re.search(
            r'(张三|李四|王五|小明|小红|老王|老李|小张|阿|某公司|某品牌)',
            text
        ))
        if not has_specific_names:
            generic_indicators.append("缺少具体人名/品牌名")

        has_specific_places = bool(re.search(
            r'(北京|上海|广州|深圳|杭州|成都|重庆|武汉|南京|西安|长沙|郑州|济南|青岛|大连|厦门)',
            text
        ))
        if not has_specific_places:
            generic_indicators.append("缺少具体地名")

        has_specific_numbers = bool(re.search(
            r'\d+[个只次元块条张根颗粒座家间辆艘]|\d+%|\d+万|\d+亿|\d+年|\d+月',
            text
        ))
        if not has_specific_numbers:
            generic_indicators.append("缺少具体数量和单位")

        has_personal_voice = bool(re.search(
            r'(我觉得|我认为|我在想|让我|困扰|不安|兴奋|担心|后悔|庆幸|妈的|操|靠|卧槽|牛逼|绝了)',
            text
        ))
        if not has_personal_voice:
            generic_indicators.append("缺少个人语气和情感")

        has_unique_detail = bool(re.search(
            r'(那天|那次|当时|记得|想起|突然|猛地|一下子|差点|居然|竟然|偏偏|刚好)',
            text
        ))
        if not has_unique_detail:
            generic_indicators.append("缺少独特细节和意外感")

        score = len(generic_indicators)
        is_generic = score >= 3

        return {
            "is_generic": is_generic,
            "score": score,
            "max_score": 5,
            "indicators": generic_indicators,
            "verdict": (
                "这段文字太通用——可以发给行业里任何人，缺乏具体性"
                if is_generic else
                "这段文字有具体细节，通过了30秒测试"
            ),
            "test_description": "这段文字能发给行业里任何人吗？如果是=AI slop",
        }

    # ============================================================
    # v3.0 新增: 填充短语与公式化结构检测
    # ============================================================

    def _detect_filler_patterns(self, text: str) -> Dict:
        """检测填充短语和公式化结构"""
        detected = {}
        total_hits = 0

        for category, phrases in self.filler_phrases.items():
            cat_hits = {}
            for phrase in phrases:
                count = text.count(phrase)
                if count > 0:
                    cat_hits[phrase] = count
                    total_hits += count
            if cat_hits:
                detected[category] = cat_hits

        structure_hits = {}
        for name, pattern in self.slop_structures.items():
            try:
                matches = re.findall(pattern, text)
                if matches:
                    structure_hits[name] = len(matches)
                    total_hits += len(matches)
            except re.error:
                pass

        text_len = max(len(text), 1)
        density = total_hits / (text_len / 100)
        score = min(int(density * 20), 50)

        return {
            "phrase_hits": detected,
            "structure_hits": structure_hits,
            "total_hits": total_hits,
            "density": round(density, 2),
            "score": score,
        }

    # ============================================================
    # 核心检测方法
    # ============================================================

    def detect(self, text: str, detail_level: str = "full") -> DetectionReport:
        """完整检测 v3.0 — 四层 + 五维度 + 灵魂检查 + Burstiness + 结构分析 + 三级检测 + 30秒测试"""
        if not text or len(text) < 50:
            return DetectionReport(
                overall_score=0, level="low",
                word_layer={}, sentence_layer={}, semantic_layer={},
                humanizer_layer={}, quality_scores={}, soul_check={},
                burstiness={}, structure_analysis={},
                tier_detection={}, thirty_second_test={},
                hot_spots=[], suggestions=["文本过短，无法有效检测"]
            )

        word_result = self._detect_word_layer(text)
        sentence_result = self._detect_sentence_layer(text)
        semantic_result = self._detect_semantic_layer(text)
        humanizer_result = self._detect_humanizer_patterns(text)
        quality_scores = self._score_quality(text)
        soul_check = self._check_soul(text)
        burstiness = self._calculate_burstiness(text)
        structure_analysis = self._analyze_structure(text)
        tier_detection = self._detect_tier_patterns(text)
        thirty_second_test = self._thirty_second_test(text)
        filler_patterns = self._detect_filler_patterns(text)

        overall = int(
            word_result["score"] * 0.12 +
            sentence_result["score"] * 0.12 +
            semantic_result["score"] * 0.10 +
            humanizer_result["score"] * 0.18 +
            (50 - quality_scores["total"]) * 0.15 +
            (100 - burstiness.get("burstiness", 50)) * 0.08 +
            (10 - structure_analysis.get("score", 10)) * 0.10 +
            tier_detection.get("overall_tier_score", 0) * 0.10 +
            (thirty_second_test.get("score", 0) / 5) * 100 * 0.05
        )

        level = self._score_to_level(overall)
        hot_spots = self._find_hot_spots(text) if detail_level == "full" else []
        suggestions = self._generate_suggestions(
            word_result, sentence_result, semantic_result,
            humanizer_result, quality_scores, soul_check,
            burstiness, structure_analysis, tier_detection,
            thirty_second_test, filler_patterns,
        )

        return DetectionReport(
            overall_score=overall,
            level=level,
            word_layer=word_result,
            sentence_layer=sentence_result,
            semantic_layer=semantic_result,
            humanizer_layer=humanizer_result,
            quality_scores=quality_scores,
            soul_check=soul_check,
            burstiness=burstiness,
            structure_analysis=structure_analysis,
            tier_detection=tier_detection,
            thirty_second_test=thirty_second_test,
            hot_spots=hot_spots,
            suggestions=suggestions,
        )

    def _detect_word_layer(self, text: str) -> Dict:
        """词汇层检测"""
        hits = {}
        total_hits = 0

        for category, words in {**self.high_risk_words, **self.medium_risk_words, **self.low_risk_words}.items():
            cat_hits = {}
            for word in words:
                count = text.count(word)
                if count > 0:
                    cat_hits[word] = count
                    total_hits += count * (3 if category in self.high_risk_words else 2 if category in self.medium_risk_words else 1)
            if cat_hits:
                hits[category] = cat_hits

        text_len = max(len(text), 1)
        density = total_hits / (text_len / 100)
        score = min(int(density * 15), 40)

        return {"hits": hits, "total_hits": total_hits, "density": round(density, 2), "score": score}

    def _detect_sentence_layer(self, text: str) -> Dict:
        """句式层检测"""
        sentences = re.split(r'[。！？\n]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        pattern_hits = {}
        total_pattern_score = 0

        for pattern, weight, name in self.sentence_patterns:
            matches = []
            for i, sent in enumerate(sentences):
                if re.search(pattern, sent):
                    matches.append({"index": i, "text": sent[:80]})
            if matches:
                pattern_hits[name] = {"count": len(matches), "ratio": len(matches) / max(len(sentences), 1)}
                total_pattern_score += len(matches) * weight * 10

        score = min(int(total_pattern_score), 35)
        return {"patterns": pattern_hits, "total_sentences": len(sentences), "score": score}

    def _detect_semantic_layer(self, text: str) -> Dict:
        """语义层检测"""
        pattern_hits = {}

        for name, pattern in self.semantic_patterns.items():
            matches = re.findall(pattern, text)
            if matches:
                pattern_hits[name] = len(matches)

        total = sum(pattern_hits.values())
        score = min(int(total * 5), 25)

        return {"patterns": pattern_hits, "total_matches": total, "score": score}

    # ============================================================
    # NWACS 24模式检测 (核心)
    # ============================================================

    def _detect_humanizer_patterns(self, text: str) -> Dict:
        """检测 NWACS 24种AI写作模式"""
        detected = []
        category_scores = {"content": 0, "language": 0, "style": 0, "communication": 0}
        total_score = 0

        for pattern in self.humanizer_patterns:
            match_count = 0

            for kw in pattern.keywords:
                count = text.count(kw)
                if count > 0:
                    match_count += count

            for regex_str in pattern.regex_patterns:
                try:
                    matches = re.findall(regex_str, text)
                    match_count += len(matches)
                except re.error:
                    pass

            if match_count > 0:
                severity = min(match_count * pattern.severity * 10, 100)
                detected.append({
                    "id": pattern.id,
                    "name": pattern.name,
                    "category": pattern.category,
                    "matches": match_count,
                    "severity": round(severity, 1),
                    "description": pattern.description,
                })
                category_scores[pattern.category] += severity
                total_score += severity

        total_score = min(int(total_score), 100)

        return {
            "detected_patterns": detected,
            "total_patterns_detected": len(detected),
            "category_scores": {k: min(int(v), 100) for k, v in category_scores.items()},
            "score": total_score,
            "top_patterns": sorted(detected, key=lambda x: x["severity"], reverse=True)[:5],
        }

    # ============================================================
    # 五维度质量评分 (新增)
    # ============================================================

    def _score_quality(self, text: str) -> Dict:
        """五维度质量评分 (50分制)"""
        scores = {}

        for dim_key, dim in self.quality_dimensions.items():
            if dim_key == "rhythm" and "check" in dim:
                raw = dim["check"](text)
                scores[dim_key] = {
                    "name": dim["name"],
                    "score": round(raw * 10, 1),
                    "description": dim["description"],
                }
            else:
                anti_count = 0
                for pattern in dim.get("anti_patterns", []):
                    try:
                        anti_count += len(re.findall(pattern, text))
                    except re.error:
                        pass
                raw = max(0, 1 - anti_count * 0.15)
                scores[dim_key] = {
                    "name": dim["name"],
                    "score": round(raw * 10, 1),
                    "description": dim["description"],
                }

        total = round(sum(s["score"] for s in scores.values()), 1)
        level = "优秀" if total >= 45 else "良好" if total >= 35 else "需要修订"

        return {
            "dimensions": scores,
            "total": total,
            "level": level,
            "max_score": 50,
        }

    # ============================================================
    # 灵魂注入检测 (新增)
    # ============================================================

    def _check_soul(self, text: str) -> Dict:
        """检测文本是否有'人味'"""
        sentences = re.split(r'[。！？\n]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        if len(sentences) < 3:
            return {"has_soul": False, "score": 0, "issues": ["文本过短"]}

        issues = []

        lengths = [len(s) for s in sentences]
        unique_lengths = len(set(lengths))
        if unique_lengths < len(lengths) * 0.3:
            issues.append("句子长度过于均匀，缺乏节奏变化")

        has_short = any(len(s) <= 10 for s in sentences)
        has_long = any(len(s) >= 30 for s in sentences)
        if not (has_short and has_long):
            issues.append("缺少长短句交替，节奏单调")

        has_first_person = bool(re.search(r"[我我们]", text))
        has_opinion = bool(re.search(r"(我觉得|我认为|我在想|让我|困扰|不安|兴奋|担心)", text))
        if not has_opinion:
            issues.append("缺乏个人观点和情感表达")

        has_specific = bool(re.search(r"\d+年|\d+月|\d+个|\d+次|\d+%", text))
        if not has_specific:
            issues.append("缺乏具体数据和细节")

        has_imperfection = bool(re.search(r"(嗯|呃|那个|就是|然后|妈的|操|靠|卧槽)", text))
        if not has_imperfection:
            issues.append("过于完美，缺乏人类的不完美表达")

        has_humor = bool(re.search(r"(笑|哈哈|滑稽|讽刺|荒谬|离谱|搞笑)", text))
        if not has_humor:
            issues.append("缺乏幽默或锋芒")

        score = max(0, 10 - len(issues) * 1.5)

        return {
            "has_soul": len(issues) <= 2,
            "score": round(score, 1),
            "max_score": 10,
            "issues": issues,
            "positives": [
                p for p, ok in [
                    ("有长短句交替", has_short and has_long),
                    ("有第一人称视角", has_first_person),
                    ("有个人观点表达", has_opinion),
                    ("有具体数据细节", has_specific),
                    ("有不完美表达", has_imperfection),
                    ("有幽默或锋芒", has_humor),
                ] if ok
            ],
        }

    # ============================================================
    # 热点定位和建议生成
    # ============================================================

    def _find_hot_spots(self, text: str) -> List[Dict]:
        """定位AI痕迹热点 — NWACS 模式检测"""
        paragraphs = text.split('\n')
        hot_spots = []

        for i, para in enumerate(paragraphs):
            if len(para) < 20:
                continue

            local_score = 0
            for words in self.high_risk_words.values():
                for w in words:
                    local_score += para.count(w) * 3
            for words in self.medium_risk_words.values():
                for w in words:
                    local_score += para.count(w) * 2

            for pattern in self.humanizer_patterns:
                for kw in pattern.keywords:
                    local_score += para.count(kw) * int(pattern.severity * 5)

            if local_score >= 5:
                hot_spots.append({
                    "paragraph": i + 1,
                    "score": local_score,
                    "preview": para[:100],
                })

        hot_spots.sort(key=lambda x: x["score"], reverse=True)
        return hot_spots[:5]

    def _score_to_level(self, score: int) -> str:
        if score < 20:
            return "low"
        elif score < 40:
            return "medium"
        elif score < 60:
            return "high"
        return "very_high"

    def _generate_suggestions(self, word: Dict, sentence: Dict, semantic: Dict,
                               humanizer: Dict = None, quality: Dict = None,
                               soul: Dict = None, burstiness: Dict = None,
                               structure: Dict = None, tier: Dict = None,
                               thirty_sec: Dict = None, slop: Dict = None) -> List[str]:
        """生成改进建议 v3.0 — 整合所有检测维度"""
        suggestions = []

        if word["score"] > 20:
            suggestions.append("词汇层AI痕迹较重，建议替换高频AI特征词")
        if sentence["score"] > 20:
            suggestions.append("句式结构过于规整，建议增加句式变化")
        if semantic["score"] > 15:
            suggestions.append("语义模式过于模板化，建议增加个性化表达")

        if humanizer:
            top = humanizer.get("top_patterns", [])
            if top:
                names = [p["name"] for p in top[:3]]
                suggestions.append(f"NWACS检测到: {', '.join(names)}")

            cat_scores = humanizer.get("category_scores", {})
            worst_cat = max(cat_scores.items(), key=lambda x: x[1]) if cat_scores else None
            if worst_cat and worst_cat[1] > 30:
                cat_names = {"content": "内容模式", "language": "语言语法", "style": "风格", "communication": "交流模式"}
                suggestions.append(f"{cat_names.get(worst_cat[0], worst_cat[0])}问题最严重({worst_cat[1]}分)")

        if quality:
            if quality["total"] < 35:
                suggestions.append(f"质量评分偏低({quality['total']}/50)，需要大幅修订")
            dims = quality.get("dimensions", {})
            worst_dim = min(dims.items(), key=lambda x: x[1]["score"]) if dims else None
            if worst_dim and worst_dim[1]["score"] < 6:
                suggestions.append(f"'{worst_dim[1]['name']}'维度最弱({worst_dim[1]['score']}/10)")

        if soul:
            if not soul.get("has_soul"):
                suggestions.append("文本缺乏'人味'，建议注入个人观点和具体细节")
            for issue in soul.get("issues", [])[:2]:
                suggestions.append(f"灵魂缺失: {issue}")

        if burstiness:
            b = burstiness.get("burstiness", 50)
            if b < 30:
                suggestions.append(f"Burstiness={b}（节拍器节奏），句子长度过于均匀，建议增加长短句交替")
            elif b < 50:
                suggestions.append(f"Burstiness={b}（中等），建议进一步增加句子长度变化")

        if structure:
            for issue in structure.get("issues", []):
                suggestions.append(f"结构问题: {issue['description']}")

        if tier:
            t1 = tier.get("tier1_immediate_flags", [])
            if t1:
                names = [f["name"] for f in t1]
                suggestions.append(f"⚠️ Tier1立即标记: {', '.join(names)}")
            t2 = tier.get("tier2_strong_indicators", [])
            if t2:
                names = [f["name"] for f in t2[:2]]
                suggestions.append(f"Tier2强指标: {', '.join(names)}")

        if thirty_sec:
            if thirty_sec.get("is_generic"):
                suggestions.append(f"30秒测试未通过: {thirty_sec.get('verdict', '')}")

        if slop:
            if slop.get("total_hits", 0) > 3:
                suggestions.append(f"检测到{slop['total_hits']}处填充短语模式，建议消除填充短语和公式化结构")

        if not suggestions:
            suggestions.append("AI痕迹较少，保持当前写作风格即可")

        return suggestions

    # ============================================================
    # 智能去痕重写
    # ============================================================

    def rewrite(self, text: str, intensity: str = "medium") -> Tuple[str, RewriteReport]:
        """智能去痕重写 v3.0

        ⚠️ 重要：机械字符串替换已被证明会制造更多AI可检测模式。
        真正的去痕应该通过AI引擎配合专门的去AI系统提示词来完成。
        此方法现在只做安全的、非破坏性的预处理。
        """
        original = self.detect(text)
        quality_before = original.quality_scores

        result = self._safe_preprocess(text)

        final = self.detect(result)
        quality_after = final.quality_scores
        reduction = original.overall_score - final.overall_score

        if reduction <= 0:
            print(f"  ⚠️ 本地预处理未降低AI痕迹分数 ({original.overall_score}→{final.overall_score})")
            print(f"  💡 建议使用AI引擎配合去AI系统提示词进行深度改写")

        return result, RewriteReport(
            original_score=original.overall_score,
            final_score=final.overall_score,
            reduction=reduction,
            changes_made=0,
            replaced_words=[],
            modified_sentences=0,
            quality_before=quality_before,
            quality_after=quality_after,
        )

    def _safe_preprocess(self, text: str) -> str:
        """安全预处理 — 只做不破坏文本质量的微调"""
        result = text

        result = re.sub(r'\.{4,}', '...', result)
        result = re.sub(r'[！？]{3,}', lambda m: m.group()[:2], result)

        paragraphs = result.split('\n')
        if len(paragraphs) > 1:
            lengths = [len(p) for p in paragraphs if p.strip()]
            if lengths and max(lengths) / (sum(lengths) / len(lengths)) > 4:
                long_paras = [i for i, p in enumerate(paragraphs)
                              if len(p) > sum(lengths) / len(lengths) * 2.5]
                for i in long_paras:
                    if i < len(paragraphs):
                        mid = len(paragraphs[i]) // 2
                        for sep in ['。', '！', '？']:
                            pos = paragraphs[i].find(sep, mid - 50, mid + 50)
                            if pos > 0:
                                paragraphs[i] = (paragraphs[i][:pos + 1] + '\n\n'
                                                 + paragraphs[i][pos + 1:].lstrip())
                                break

        result = '\n'.join(paragraphs)
        return result

    def _light_rewrite(self, text: str, replaced: List) -> str:
        """轻度去痕 - 仅替换最高风险词"""
        replacements = {
            "宛如": "像", "仿佛": "好像", "犹如": "像",
            "不禁": "忍不住", "不由得": "不自觉地",
            "缓缓地": "慢慢", "渐渐地": "逐步",
        }
        for old, new in replacements.items():
            if old in text:
                text = text.replace(old, new)
                replaced.append((old, new))
        return text

    def _medium_rewrite(self, text: str, replaced: List) -> str:
        """中度去痕"""
        text = self._light_rewrite(text, replaced)

        extra = {
            "非常": "很", "极其": "特别", "十分": "很",
            "微微一笑": "笑了笑", "淡淡一笑": "轻轻一笑",
            "心中暗想": "心想", "心中思索": "思索着",
            "站起身": "站起来", "转过身": "转过来",
        }
        for old, new in extra.items():
            if old in text:
                text = text.replace(old, new)
                replaced.append((old, new))
        return text

    def _heavy_rewrite(self, text: str, replaced: List) -> str:
        """重度去痕"""
        text = self._medium_rewrite(text, replaced)

        heavy = {
            "轻轻地": "轻轻", "悄悄地": "悄悄",
            "感到": "觉得", "感觉": "觉得",
            "此时": "这会儿", "此刻": "现在",
            "只见": "", "只听": "", "只觉": "",
        }
        for old, new in heavy.items():
            if old in text:
                text = text.replace(old, new)
                replaced.append((old, new))
        return text

    def _vary_sentence_structure(self, text: str) -> str:
        """变化句式结构"""
        sentences = re.split(r'(?<=[。！？])', text)
        result = []

        for i, sent in enumerate(sentences):
            if not sent.strip():
                result.append(sent)
                continue

            if random.random() < 0.15 and len(sent) > 15:
                if sent.startswith(('他', '她', '它')):
                    parts = sent.split('，', 1)
                    if len(parts) == 2:
                        sent = parts[1].strip() + '，' + parts[0]

            result.append(sent)

        return ''.join(result)

    def _add_natural_imperfections(self, text: str) -> str:
        """添加自然瑕疵"""
        if random.random() < 0.2:
            fillers = ["嗯", "呃", "那个", "就是", "然后"]
            filler = random.choice(fillers)
            idx = text.find("，", len(text) // 3)
            if idx > 0:
                text = text[:idx + 1] + filler + "，" + text[idx + 1:]

        return text

    # ============================================================
    # 批量检测和对比
    # ============================================================

    def batch_detect(self, chapters: Dict[int, str]) -> Dict:
        """批量检测多章节"""
        results = {}
        total_score = 0

        for ch, content in chapters.items():
            report = self.detect(content)
            results[ch] = {
                "score": report.overall_score,
                "level": report.level,
                "hot_spots_count": len(report.hot_spots),
                "quality_total": report.quality_scores.get("total", 0),
                "soul_score": report.soul_check.get("score", 0),
                "humanizer_patterns": report.humanizer_layer.get("total_patterns_detected", 0),
                "burstiness": report.burstiness.get("burstiness", 0),
                "structure_score": report.structure_analysis.get("score", 10),
                "tier_score": report.tier_detection.get("overall_tier_score", 0),
                "thirty_sec_passed": not report.thirty_second_test.get("is_generic", True),
            }
            total_score += report.overall_score

        avg_score = total_score / max(len(chapters), 1)

        return {
            "chapters": results,
            "average_score": round(avg_score, 1),
            "average_level": self._score_to_level(int(avg_score)),
            "total_chapters": len(chapters),
        }

    def compare_texts(self, text_a: str, text_b: str) -> Dict:
        """对比两段文本的AI痕迹"""
        report_a = self.detect(text_a)
        report_b = self.detect(text_b)

        return {
            "text_a": {
                "score": report_a.overall_score,
                "level": report_a.level,
                "quality": report_a.quality_scores.get("total", 0),
                "soul": report_a.soul_check.get("score", 0),
                "burstiness": report_a.burstiness.get("burstiness", 0),
                "thirty_sec_passed": not report_a.thirty_second_test.get("is_generic", True),
            },
            "text_b": {
                "score": report_b.overall_score,
                "level": report_b.level,
                "quality": report_b.quality_scores.get("total", 0),
                "soul": report_b.soul_check.get("score", 0),
                "burstiness": report_b.burstiness.get("burstiness", 0),
                "thirty_sec_passed": not report_b.thirty_second_test.get("is_generic", True),
            },
            "difference": report_a.overall_score - report_b.overall_score,
            "better": "text_a" if report_a.overall_score < report_b.overall_score else "text_b",
        }

    def diagnose_deep(self, text: str) -> Dict:
        """深度AI特征诊断"""
        try:
            from writing_knowledge_engine import WritingKnowledgeEngine
            engine = WritingKnowledgeEngine()
        except ImportError:
            return {
                "overall_ai_score": 0,
                "risk_level": "unknown",
                "summary": "知识引擎不可用，回退到基础检测",
                "detected_traits": [],
                "fix_priority": [],
                "deai_pipeline": None,
                "recommended_techniques": [],
            }

        diagnosis = engine.diagnose_ai_traits(text)
        pipeline = engine.generate_deai_pipeline(text, "voice")
        context = {
            "genre": "玄幻",
            "chapter_num": 1,
            "ai_score": diagnosis.overall_ai_score,
        }
        techniques = engine.recommend_techniques(context=context)

        return {
            "overall_ai_score": diagnosis.overall_ai_score,
            "risk_level": diagnosis.risk_level,
            "summary": diagnosis.summary,
            "detected_traits": [
                {"key": t[0], "severity": round(t[1], 3)}
                for t in diagnosis.detected_traits
            ],
            "fix_priority": diagnosis.fix_priority,
            "deai_pipeline": {
                "stages": pipeline.stages,
                "estimated_effectiveness": pipeline.estimated_effectiveness,
                "total_steps": pipeline.total_steps,
            },
            "recommended_techniques": [
                {"name": t.technique_name, "relevance": t.relevance, "urgency": t.urgency}
                for t in techniques
            ],
        }

    # ============================================================
    # NWACS 快速检查清单 (交付前检查)
    # ============================================================

    def quick_checklist(self, text: str) -> Dict:
        """NWACS 快速检查清单 — 6项交付前检查"""
        checks = []

        sentences = re.split(r'[。！？\n]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        lengths = [len(s) for s in sentences]

        consecutive_same = 0
        for i in range(len(lengths) - 2):
            if abs(lengths[i] - lengths[i + 1]) < 3 and abs(lengths[i + 1] - lengths[i + 2]) < 3:
                consecutive_same += 1
        checks.append({
            "item": "连续三个句子长度相同？",
            "passed": consecutive_same == 0,
            "detail": f"发现{consecutive_same}处连续相同长度" if consecutive_same > 0 else "句子长度变化良好",
        })

        paragraphs = text.split('\n')
        ends_with_short = sum(1 for p in paragraphs if p.strip() and len(p.strip()) < 30)
        checks.append({
            "item": "段落以简洁的单行结尾？",
            "passed": ends_with_short > 0,
            "detail": f"{ends_with_short}个短段落" if ends_with_short > 0 else "缺少短段落收尾",
        })

        dash_count = text.count('—') + text.count('--')
        checks.append({
            "item": "揭示前有破折号？",
            "passed": dash_count <= 2,
            "detail": f"发现{dash_count}处破折号" if dash_count > 2 else "破折号使用合理",
        })

        metaphor_explained = bool(re.search(r"(也就是说|换句话说|这意味着|顾名思义)", text))
        checks.append({
            "item": "解释隐喻或比喻？",
            "passed": not metaphor_explained,
            "detail": "存在过度解释" if metaphor_explained else "信任读者理解力",
        })

        connector_count = len(re.findall(r"(此外|然而|但是|可是|不过|因此|所以|总之)", text))
        checks.append({
            "item": "使用了'此外''然而'等连接词？",
            "passed": connector_count <= 3,
            "detail": f"发现{connector_count}处连接词" if connector_count > 3 else "连接词使用合理",
        })

        triple_count = len(re.findall(r"[^，。]+、[^，。]+和[^，。]+", text))
        checks.append({
            "item": "三段式列举？",
            "passed": triple_count <= 2,
            "detail": f"发现{triple_count}处三段式" if triple_count > 2 else "列举方式自然",
        })

        passed = sum(1 for c in checks if c["passed"])
        return {
            "checks": checks,
            "passed": passed,
            "total": len(checks),
            "all_passed": passed == len(checks),
        }


if __name__ == "__main__":
    print("=" * 60)
    print("🔍 增强版AI检测器 v3.0 — 多项目融合测试")
    print("=" * 60)

    detector = EnhancedAIDetector()

    ai_text = """
    林晨缓缓地站起身，宛如一只刚刚破茧而出的蝴蝶，心中不禁激动万分。
    仿佛天地都在为他欢呼，眼前的景象十分壮观，格外震撼人心。
    这一切似乎都像是一场梦境，渐渐地，林晨才相信这是真的。
    他微微一笑，心中暗想，自己的努力终究没有白费。
    极其艰难的旅程，非常辛苦的奋斗，终于换来了此刻的成功。
    此外，这次经历作为他人生中极其重要的转折点，标志着一段全新旅程的开始。
    这不仅是一次胜利，更是对自我的超越，为未来的发展奠定了坚实的基础。
    """

    human_text = """
    林晨站起来，腿有点麻。他揉了揉膝盖，看了眼窗外。
    天快亮了。一夜没睡，脑子昏沉沉的。
    "妈的。"他骂了一句，抓起桌上的烟盒，空的。
    他把烟盒揉成一团，扔进垃圾桶。去他妈的。
    """

    print("\n【AI文本检测】")
    report = detector.detect(ai_text)
    print(f"  总分: {report.overall_score}/100 ({report.level})")
    print(f"  词汇层: {report.word_layer['score']}/40")
    print(f"  句式层: {report.sentence_layer['score']}/35")
    print(f"  语义层: {report.semantic_layer['score']}/25")
    print(f"  NWACS模式层: {report.humanizer_layer['score']}/100")
    print(f"  检测到模式: {report.humanizer_layer['total_patterns_detected']}/24")
    print(f"  质量评分: {report.quality_scores['total']}/50 ({report.quality_scores['level']})")
    print(f"  灵魂评分: {report.soul_check['score']}/10")
    print(f"  Burstiness: {report.burstiness.get('burstiness', 'N/A')} ({report.burstiness.get('level', 'N/A')})")
    print(f"  结构分析: {report.structure_analysis.get('score', 'N/A')}/10")
    print(f"  三级检测: {report.tier_detection.get('overall_tier_score', 'N/A')}")
    print(f"  30秒测试: {'通过' if not report.thirty_second_test.get('is_generic', True) else '未通过'}")
    print(f"  热点: {len(report.hot_spots)}处")
    print(f"  建议: {report.suggestions[:3]}")

    print("\n【人类文本检测】")
    report2 = detector.detect(human_text)
    print(f"  总分: {report2.overall_score}/100 ({report2.level})")
    print(f"  质量评分: {report2.quality_scores['total']}/50 ({report2.quality_scores['level']})")
    print(f"  灵魂评分: {report2.soul_check['score']}/10")
    print(f"  Burstiness: {report2.burstiness.get('burstiness', 'N/A')} ({report2.burstiness.get('level', 'N/A')})")
    print(f"  30秒测试: {'通过' if not report2.thirty_second_test.get('is_generic', True) else '未通过'}")

    print("\n【快速检查清单】")
    checklist = detector.quick_checklist(ai_text)
    for c in checklist["checks"]:
        status = "✅" if c["passed"] else "❌"
        print(f"  {status} {c['item']} — {c['detail']}")

    print("\n【对比检测】")
    comp = detector.compare_texts(ai_text, human_text)
    print(f"  AI文本: {comp['text_a']['score']}分 (质量{comp['text_a']['quality']}/50)")
    print(f"  人类文本: {comp['text_b']['score']}分 (质量{comp['text_b']['quality']}/50)")
    print(f"  更优: {comp['better']}")

    print("\n【快速检查清单 - AI文本】")
    checklist = detector.quick_checklist(ai_text)
    print(f"  通过: {checklist['passed']}/{checklist['total']}")
    for c in checklist["checks"]:
        status = "✅" if c["passed"] else "❌"
        print(f"  {status} {c['item']}: {c['detail']}")

    print("\n【快速检查清单 - 人类文本】")
    checklist2 = detector.quick_checklist(human_text)
    print(f"  通过: {checklist2['passed']}/{checklist2['total']}")
    for c in checklist2["checks"]:
        status = "✅" if c["passed"] else "❌"
        print(f"  {status} {c['item']}: {c['detail']}")

    print("\n【中度去痕】")
    rewritten, rw_report = detector.rewrite(ai_text, "medium")
    print(f"  原始分数: {rw_report.original_score} → 去痕后: {rw_report.final_score}")
    print(f"  降低: {rw_report.reduction}分")

    print("\n【批量检测】")
    chapters = {
        1: ai_text,
        2: human_text,
        3: "这是一段混合文本。" + ai_text[:100],
    }
    batch = detector.batch_detect(chapters)
    print(f"  平均分: {batch['average_score']} ({batch['average_level']})")
    for ch, info in batch['chapters'].items():
        print(f"  第{ch}章: {info['score']}分 ({info['level']}) 质量{info['quality_total']}/50")