#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS V8.6 爆款小说拆解系统
参考: 笔灵AI爆款拆解引擎

核心功能:
- 爆款小说结构分析
- 写作公式提取
- 套路模式识别
- 素材库管理
- 市场趋势分析
"""

import os
import json
import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from collections import Counter


class HotspotType(Enum):
    READ_PARISING = "read_rasing"
    EMOTIONAL_IMPACT = "emotional_impact"
    PLOT_REVERSAL = "plot_reversal"
    CHARACTER_CHARM = "character_charm"
    TENSION_BUILDING = "tension_building"
    CLIMAX_SCENE = "climax_scene"


@dataclass
class HotspotAnalysis:
    """爽点分析"""
    hotspot_type: HotspotType
    location: str
    description: str
    intensity: float
    techniques: List[str]


@dataclass
class StructureAnalysis:
    """结构分析"""
    chapter_num: int
    opening_hook: str
    development: str
    climax: str
    ending_hook: str
    word_count: int
    pacing_score: float


@dataclass
class CharacterAnalysis:
    """角色分析"""
    name: str
    role: str
    personality_traits: List[str]
    character_arc: str
    memorable_quotes: List[str]
    interaction_patterns: List[str]


@dataclass
class BestsellerReport:
    """爆款拆解报告"""
    title: str
    author: str
    genre: str
    total_chapters: int
    average_word_count: int
    structure: List[StructureAnalysis]
    characters: List[CharacterAnalysis]
    hotspots: List[HotspotAnalysis]
    writing_formulas: List[str]
    market_positioning: str
    key_takeaways: List[str]


class BestsellerAnalyzer:
    """爆款小说分析器"""

    def __init__(self):
        self.patterns = self._load_writing_patterns()
        self.formulas = self._load_writing_formulas()
        self.bestseller_database = self._load_bestseller_database()
    
    def _load_bestseller_database(self) -> Dict:
        """加载2020-2026年爆款小说数据库"""
        return {
            "qidian_xuanhuan": [
                {"rank": 1, "title": "夜无疆", "author": "辰东", "score": "9.8", "key_features": ["永夜危机设定", "全新修炼体系", "主角弧光鲜明", "势力博弈"], "data": "月票榜TOP3，收藏破百万，抖音话题1200万+"},
                {"rank": 2, "title": "诡秘之主", "author": "爱潜水的乌贼", "score": "9.9", "key_features": ["蒸汽朋克+克苏鲁", "魔药序列体系", "悬疑推理天花板", "群像塑造"], "data": "动画化加持，跨圈层传播，抖音话题2800万+"},
                {"rank": 3, "title": "玄鉴仙族", "author": "季越人", "score": "9.8", "key_features": ["无系统流", "家族经营", "硬核修炼", "严谨设定"], "data": "阅读指数榜冠军，抖音话题讨论120万+"},
                {"rank": 4, "title": "凡人修仙传", "author": "忘语", "score": "9.7", "key_features": ["凡人逆袭", "低调务实", "修仙生态真实", "细节饱满"], "data": "起点总点击超12亿，经典代表作"},
                {"rank": 5, "title": "斗破苍穹", "author": "天蚕土豆", "score": "9.6", "key_features": ["退婚流开创者", "斗气升级体系", "清晰成长线", "莫欺少年穷"], "data": "起点总点击超10亿，文化符号"}
            ],
            "fanqie_novel": [
                {"rank": 1, "title": "十日终焉", "author": "杀虫队队员", "score": "9.9", "key_features": ["十日循环设定", "多视角叙事", "智斗解谜", "人性探讨"], "data": "番茄巅峰榜TOP1，233万人在读，抖音话题破5亿"},
                {"rank": 2, "title": "我在精神病院学斩神", "author": "三九音域", "score": "9.8", "key_features": ["都市高武", "神明降临", "守护主题", "家国情怀"], "data": "番茄巅峰榜TOP2，267万人跟读，抖音话题超8亿"},
                {"rank": 3, "title": "冒姓琅琊", "author": "东周公子南", "score": "9.7", "key_features": ["穿越历史", "权谋斗争", "学术细节", "门阀垄断"], "data": "番茄巅峰榜TOP4，9次登顶"},
                {"rank": 4, "title": "我不是戏神", "author": "三九音域", "score": "9.6", "key_features": ["穿越玄幻", "戏道修炼", "非遗元素", "文明救赎"], "data": "番茄高分完结，抖音视频点赞超3000万"},
                {"rank": 5, "title": "诸神愚戏", "author": "一月九十秋", "score": "9.4", "key_features": ["神明降临", "谎言成真", "资本黑幕", "信仰人性"], "data": "番茄巅峰榜TOP3，2025最强黑马"}
            ],
            "jjwxc_romance": [
                {"rank": 1, "title": "难哄", "author": "竹已", "score": "9.8", "key_features": ["青梅竹马", "破镜重圆", "细腻情感", "双向奔赴"], "data": "晋江总榜TOP1，212亿积分"},
                {"rank": 2, "title": "砸锅卖铁去上学", "author": "红刺北", "score": "9.7", "key_features": ["星际未来", "女强成长", "爽文路线", "科技元素"], "data": "晋江总榜TOP2，197亿积分"},
                {"rank": 3, "title": "偷偷藏不住", "author": "竹已", "score": "9.6", "key_features": ["暗恋成真", "年下恋", "校园到都市", "甜宠治愈"], "data": "晋江总榜TOP3，196亿积分，影视化改编"},
                {"rank": 4, "title": "穿进赛博游戏后干掉BOSS成功上位", "author": "桉柏", "score": "9.7", "key_features": ["赛博朋克", "游戏穿越", "女强爽文", "智斗升级"], "data": "晋江总榜TOP4，190亿积分"},
                {"rank": 5, "title": "陷入我们的热恋", "author": "耳东兔子", "score": "9.5", "key_features": ["校园青春", "双向暗恋", "热血成长", "情感治愈"], "data": "晋江总榜TOP5，161亿积分"}
            ],
            "top_patterns": [
                "守护主题热度最高",
                "时间循环设定热门",
                "克苏鲁元素流行",
                "群像叙事受欢迎",
                "家国情怀加分",
                "多视角叙事流行",
                "智斗解谜元素",
                "情感共鸣重要"
            ]
        }

    def _load_writing_patterns(self) -> Dict:
        """加载网文套路模式 - 2020-2026爆款小说综合分析"""
        return {
            "golden_three_chapters": {
                "name": "黄金三章法则",
                "description": "开头三章必须抓住读者",
                "elements": [
                    "第一章：困境/机遇出现",
                    "第二章：冲突/对手出现",
                    "第三章：小高潮/悬念"
                ]
            },
            "tianshui_chapter": {
                "name": "天水章节公式",
                "description": "每10章一个小高潮",
                "formula": "压抑(3章)→转折(1章)→爆发(2章)→余韵(2章)→新伏笔(2章)"
            },
            "爽点类型": {
                "打脸": ["对方目瞪口呆", "主角淡定反击", "围观群众惊叹"],
                "碾压": ["实力悬殊", "轻松击败", "对手绝望"],
                "收获": ["获得宝物", "突破境界", "美人倾心"],
                "复仇": ["隐忍", "收集证据", "公开对决"],
                "装逼": ["低调出场", "被轻视", "展现实力", "众人震惊"],
                "反转": ["所有人都以为主角输了", "突然揭示真相", "众人震惊"],
                "守护": ["主角保护重要的人", "对手想要伤害", "主角爆发", "成功守护"],
                "觉醒": ["主角看似平凡", "关键时刻觉醒特殊能力", "震撼全场"]
            },
            "人物模板": {
                "退婚流": ["天赋被封印", "未婚妻退婚", "金手指开启", "打脸未婚妻"],
                "重生流": ["前世悲惨", "重活一世", "复仇/弥补", "改变命运"],
                "穿越流": ["原世界死亡", "穿越异世", "适应环境", "开始冒险"],
                "系统流": ["获得系统", "完成任务", "获得奖励", "不断提升"],
                "无限流": ["卷入神秘空间", "参与死亡游戏", "解谜求生", "不断成长"],
                "都市高武": ["都市背景", "神明/超凡降临", "觉醒能力", "守护家园"],
                "克苏鲁风": ["神秘世界观", "未知恐怖", "推理解谜", "人性挣扎"],
                "群像流": ["多个视角", "角色各自成长", "最终汇聚", "共同对抗"]
            },
            "2020-2026爆款套路": {
                "诡秘之主模式": ["独特世界观设定", "严谨升级体系", "群像塑造", "悬疑推理"],
                "斗破苍穹模式": ["清晰成长线", "阶段性目标", "定期打脸", "感情线辅助"],
                "斩神模式": ["守护主题", "家国情怀", "热血战斗", "情感共鸣"],
                "十日终焉模式": ["时间循环", "多视角叙事", "智斗解谜", "人性探讨"],
                "夜无疆模式": ["宏大世界观", "全新修炼体系", "主角弧光", "势力博弈"],
                "盐言悬疑模式": ["强情节弱冗余", "多层反转", "人性洞察", "现实映射"]
            },
            "悬念反转技巧": {
                "核心口诀": "明线误导，暗线藏真；细节说话，台词留缝",
                "伏笔类型": {
                    "细节伏笔": ["用物品、动作、习惯藏真相", "不解释、不强调", "读者第一次看会忽略，二刷会炸"],
                    "台词伏笔": ["说半句真话，半句假话", "台词能同时解释假身份和真身份"],
                    "视角偏差伏笔": ["利用主角视角盲区", "只写主角看到的，不写真实心理"],
                    "因果倒置伏笔": ["先给结果，再露原因", "巧合多到不正常"]
                },
                "反转类型": {
                    "人设反转": ["白切黑", "打破刻板印象", "身份互换"],
                    "情节反转": ["真相反转", "选择反转", "绝境反转"],
                    "结局反转": ["欧亨利式结尾", "意料之外情理之中"]
                },
                "3+1伏笔结构": ["开篇轻伏笔", "中段强误导", "反转前点破", "反转揭晓"]
            }
        }

    def _load_writing_formulas(self) -> Dict:
        """加载写作公式 - 2020-2026爆款小说综合分析"""
        return {
            "开头公式": [
                "困境开场 + 金手指出现 + 快速立人设",
                "冲突引入 + 悬念设置 + 期待感建立",
                "日常转危机 + 主角应对 + 展示能力",
                "倒叙开场 + 未来片段 + 回到过去"
            ],
            "困境公式": [
                "生存困境 + 绝境求生意志",
                "情感困境 + 内心挣扎",
                "身份困境 + 身世之谜",
                "选择困境 + 两难抉择"
            ],
            "打脸公式": [
                "被轻视/嘲讽 → 暗中准备 → 关键时刻反击 → 对方震惊 → 围观者惊叹",
                "误会主角 → 主角隐忍 → 真相大白 → 打脸时刻 → 获得好处",
                "扮猪吃虎 → 被质疑 → 展现实力 → 震撼全场"
            ],
            "感情线公式": [
                "欢喜冤家 → 日久生情 → 误会分离 → 真相大白 → 修成正果",
                "暗恋 → 试探 → 表白被拒 → 努力提升 → 再次追求 → 成功",
                "救赎型 → 互相治愈 → 共同成长 → 双向奔赴"
            ],
            "升级公式": [
                "设定目标 → 遇到困难 → 获取资源 → 刻苦修炼 → 突破成功 → 新的目标",
                "被困 → 领悟 → 突破 → 展示 → 获得认可",
                "规则破解 → 系统利用 → 资源整合 → 实力飙升"
            ],
            "悬念公式": [
                "提出问题 → 暗示关联 → 逐步揭示 → 高潮揭露",
                "埋下伏笔 → 多次暗示 → 关键时刻引爆",
                "多线悬念 → 平行展开 → 最终汇聚 → 惊天反转"
            ],
            "无限流公式": [
                "规则介绍 → 适应环境 → 发现漏洞 → 智斗解谜 → 通关",
                "团队协作 → 分工明确 → 各自发挥 → 共同破局"
            ],
            "克苏鲁风公式": [
                "异常事件 → 调查深入 → 发现真相 → 理智挣扎 → 抉择结局",
                "神秘符号 → 禁忌知识 → 不可名状 → 人性考验"
            ],
            "都市高武公式": [
                "平静生活 → 异变降临 → 觉醒能力 → 加入组织 → 守护家园",
                "神明降临 → 代理人之战 → 势力博弈 → 文明存续"
            ],
            "悬念反转公式": [
                "明线误导 → 暗线藏真 → 伏笔回收 → 震撼反转",
                "3+1结构: 开篇轻伏笔 → 中段强误导 → 反转前点破 → 反转揭晓",
                "人设反转: 表面形象 → 隐藏线索 → 关键时刻揭露真相",
                "结局反转: 铺垫暗示 → 误导强化 → 欧亨利式收尾"
            ],
            "短篇悬疑公式": [
                "强开场(反常/悬念) → 快速铺垫 → 多重反转 → 余味结尾",
                "规则设定 → 打破规则 → 重建规则 → 升华主题",
                "有限时空 → 密集信息 → 层层解密 → 瞬间爆发"
            ],
            "公众号爆款公式": {
                "核心公式": "爆款=强情绪+真细节+短节奏+好标题+强结构+高互动",
                "标题公式": [
                    "数字+结果: 《3个技巧，让你文章阅读量翻10倍》",
                    "痛点+方案: 《写作没逻辑?用这招彻底解决》",
                    "反差+悬念: 《月薪3千和3万，差的不是努力，而是这一点》",
                    "人群+共鸣: 《写给所有熬夜改方案的打工人》"
                ],
                "开头公式": [
                    "痛点提问: 你有没有过写了3小时，却没人看的崩溃?",
                    "场景代入: 凌晨2点，我看着聊天框里打了又删的消息，突然懂了",
                    "结果前置: 用这套方法，我30天写出5篇10W+",
                    "颠覆认知: 写不好文章，根本不是因为文笔差"
                ],
                "结构公式": [
                    "黄金三段式: 开头炸场(痛点/场景/金句) → 中段故事+细节+金句 → 结尾升华+互动",
                    "SCQA结构: 场景(S) → 冲突(C) → 问题(Q) → 答案(A)",
                    "冲突-反转-升华: 制造矛盾/困境 → 打破预期 → 提炼观点/金句"
                ],
                "结尾公式": [
                    "金句升华: 后来我才懂，父母不是不爱你，只是方式不同",
                    "开放式提问: 你有没有过不敢回家里微信的瞬间?",
                    "反转留白: 我笑着挂电话，却哭了一小时，这事永远不告诉她",
                    "号召共鸣: 愿我们都能在平凡日子里，活出自己的光"
                ]
            },
            "公众号内容类型": {
                "职场技能类(25%)": ["职业发展", "工作技巧", "职场沟通"],
                "情感生活类(20%)": ["情感故事", "生活感悟", "人际关系"],
                "健康养生类(18%)": ["健康知识", "养生方法", "疾病预防"],
                "科技前沿类(15%)": ["科技资讯", "产品评测", "技术趋势"],
                "教育学习类(12%)": ["学习方法", "教育理念", "知识分享"]
            },
            "公众号爆款特征": {
                "标题特征": {
                    "长度": "20-50字符最优",
                    "类型": ["颠覆认知型", "痛点焦虑型", "数字干货型", "悬念好奇型", "人间清醒型", "对比反差型", "人群精准型", "种草带货型"]
                },
                "内容特征": {
                    "长度": "500-3000字符最优",
                    "排版": "简约美观，分段清晰，多用小标题",
                    "节奏": "短句分段，句子短，信息点密"
                },
                "传播特征": {
                    "核心": "引发共鸣、建立认同",
                    "关键": "有收藏价值、转发能体现自己的深度"
                }
            }
        }

    def analyze_novel(self, text: str, metadata: Dict = None) -> BestsellerReport:
        """分析小说内容"""
        metadata = metadata or {}

        chapters = self._split_chapters(text)
        structure = self._analyze_structure(chapters)
        characters = self._analyze_characters(text)
        hotspots = self._analyze_hotspots(text)
        formulas = self._extract_formulas(text, hotspots)

        return BestsellerReport(
            title=metadata.get("title", "未知"),
            author=metadata.get("author", "未知"),
            genre=metadata.get("genre", "玄幻"),
            total_chapters=len(chapters),
            average_word_count=sum(c.word_count for c in structure) // max(len(structure), 1),
            structure=structure,
            characters=characters,
            hotspots=hotspots,
            writing_formulas=formulas,
            market_positioning=self._analyze_market_positioning(metadata),
            key_takeaways=self._generate_takeaways(hotspots, formulas)
        )

    def _split_chapters(self, text: str) -> List[str]:
        """分割章节"""
        chapter_pattern = r"第[一二三四五六七八九十百千万\d]+章"
        chapters = re.split(chapter_pattern, text)
        return [c.strip() for c in chapters if c.strip()]

    def _analyze_structure(self, chapters: List[str]) -> List[StructureAnalysis]:
        """分析结构"""
        structure = []

        for i, chapter_text in enumerate(chapters[:20]):
            words = len(chapter_text)

            first_100 = chapter_text[:100] if len(chapter_text) > 100 else chapter_text
            last_100 = chapter_text[-100:] if len(chapter_text) > 100 else chapter_text

            structure.append(StructureAnalysis(
                chapter_num=i + 1,
                opening_hook=self._extract_opening_hook(first_100),
                development=self._extract_development(chapter_text),
                climax=self._extract_climax(chapter_text),
                ending_hook=self._extract_ending_hook(last_100),
                word_count=words,
                pacing_score=self._calculate_pacing_score(chapter_text)
            ))

        return structure

    def _extract_opening_hook(self, text: str) -> str:
        """提取开头钩子"""
        hooks = []
        if any(kw in text for kw in ["突然", "没想到", "赫然"]):
            hooks.append("突发事件")
        if any(kw in text for kw in ["此时", "就在", "正当"]):
            hooks.append("时机把控")
        if any(kw in text for kw in ["只见", "但见", "却见"]):
            hooks.append("场景切入")
        return "/".join(hooks) if hooks else "一般开头"

    def _extract_development(self, text: str) -> str:
        """提取发展部分"""
        development_patterns = [
            "于是", "接下来", "然后", "此时",
            "然而", "不过", "只是", "虽然"
        ]
        for pattern in development_patterns:
            if pattern in text:
                return f"使用连接词: {pattern}"
        return "叙述发展"

    def _extract_climax(self, text: str) -> str:
        """提取高潮部分"""
        climax_markers = ["轰", "爆", "惊", "怒", "战", "斗"]
        for marker in climax_markers:
            if marker in text:
                return f"高潮标记: {marker}"
        return "一般情节"

    def _extract_ending_hook(self, text: str) -> str:
        """提取结尾钩子"""
        hooks = []
        if any(kw in text for kw in ["欲知", "想知道", "究竟"]):
            hooks.append("悬念提问")
        if any(kw in text for kw in ["突然", "就在此时", "刹那间"]):
            hooks.append("突发事件")
        if any(kw in text for kw in ["不知道", "是否会", "能否"]):
            hooks.append("结果未知")
        return "/".join(hooks) if hooks else "一般结尾"

    def _calculate_pacing_score(self, text: str) -> float:
        """计算节奏得分"""
        short_sentences = len([s for s in re.split(r'[。！？]', text) if len(s) < 10])
        total_sentences = len(re.split(r'[。！？]', text))
        if total_sentences == 0:
            return 0.5

        short_ratio = short_sentences / total_sentences

        action_markers = ["轰", "爆", "杀", "战", "斗", "斩", "踢", "打"]
        action_count = sum(text.count(marker) for marker in action_markers)

        score = min(1.0, (short_ratio * 0.3 + min(action_count / 10, 1) * 0.7))
        return round(score, 2)

    def _analyze_characters(self, text: str) -> List[CharacterAnalysis]:
        """分析角色"""
        characters = []

        name_patterns = [
            r"【([^】]+)】",
            r"([^：\s]{2,4})(?:说道|说|问道|答道|叹道|怒道|笑道)",
            r"（([^）]+)）"
        ]

        names = set()
        for pattern in name_patterns:
            matches = re.findall(pattern, text)
            names.update(matches)

        for name in list(names)[:5]:
            characters.append(CharacterAnalysis(
                name=name,
                role=self._identify_role(text, name),
                personality_traits=self._extract_traits(text, name),
                character_arc=self._extract_arc(text, name),
                memorable_quotes=self._extract_quotes(text, name),
                interaction_patterns=self._extract_interactions(text, name)
            ))

        return characters

    def _identify_role(self, text: str, name: str) -> str:
        """识别角色定位"""
        context = text[:500] if len(text) > 500 else text
        if any(kw in context for kw in ["主角", "男主", "女主"]):
            return "主角"
        if any(kw in context for kw in ["师父", "长老", "掌门"]):
            return "长辈"
        if any(kw in context for kw in ["师兄", "师姐", "师弟"]):
            return "同门"
        if any(kw in context for kw in ["敌人", "反派", "仇人"]):
            return "对手"
        return "配角"

    def _extract_traits(self, text: str, name: str) -> List[str]:
        """提取性格特征"""
        traits = []
        trait_markers = {
            "冷静": ["冷静", "沉着", "淡定"],
            "果断": ["果断", "干脆", "毫不犹豫"],
            "机智": ["机智", "聪明", "灵活"],
            "狂傲": ["狂傲", "高傲", "自负"],
            "腹黑": ["腹黑", "阴险", "狡诈"]
        }

        for trait, markers in trait_markers.items():
            if any(m in text for m in markers):
                traits.append(trait)

        return traits[:5]

    def _extract_arc(self, text: str, name: str) -> str:
        """提取角色弧光"""
        arcs = []
        if "突破" in text and "境界" in text:
            arcs.append("成长型")
        if "复仇" in text:
            arcs.append("复仇型")
        if "救赎" in text or "弥补" in text:
            arcs.append("救赎型")
        return "/".join(arcs) if arcs else "稳定型"

    def _extract_quotes(self, text: str, name: str) -> List[str]:
        """提取经典台词"""
        quotes = []
        patterns = [
            rf"{name}(?:说道|说|叹道|怒道|笑道)[：:\"]([^\"。]{10,30})[\"。]",
            rf"\"([^\"]{5,20})\"[，,]?{name}"
        ]

        for pattern in patterns:
            matches = re.findall(pattern, text)
            quotes.extend(matches)

        return quotes[:3]

    def _extract_interactions(self, text: str, name: str) -> List[str]:
        """提取互动模式"""
        interactions = []
        if "联手" in text or "合作" in text:
            interactions.append("合作")
        if "对战" in text or "对决" in text:
            interactions.append("对决")
        if "帮助" in text or "扶持" in text:
            interactions.append("帮助")
        return interactions

    def _analyze_hotspots(self, text: str) -> List[HotspotAnalysis]:
        """分析爽点"""
        hotspots = []

        hotspot_rules = {
            HotspotType.READ_PARISING: {
                "markers": ["目瞪口呆", "震惊", "不敢相信", "愣住"],
                "weight": 1.0
            },
            HotspotType.PLOT_REVERSAL: {
                "markers": ["没想到", "竟然", "原来", "真相是"],
                "weight": 0.9
            },
            HotspotType.CHARACTER_CHARM: {
                "markers": ["霸气", "帅气", "冷酷", "温柔"],
                "weight": 0.7
            },
            HotspotType.TENSION_BUILDING: {
                "markers": ["危机", "危险", "困境", "绝境"],
                "weight": 0.8
            }
        }

        for hotspot_type, rule in hotspot_rules.items():
            for marker in rule["markers"]:
                if marker in text:
                    hotspots.append(HotspotAnalysis(
                        hotspot_type=hotspot_type,
                        location=f"标记: {marker}",
                        description=f"{hotspot_type.value}类型",
                        intensity=rule["weight"],
                        techniques=self._extract_techniques(text, marker)
                    ))

        return hotspots

    def _extract_techniques(self, text: str, marker: str) -> List[str]:
        """提取技巧"""
        techniques = []
        idx = text.find(marker)
        if idx > 0:
            before = text[max(0, idx-50):idx]
            after = text[idx:min(len(text), idx+50)]

            if any(kw in before for kw in ["只见", "但见"]):
                techniques.append("视觉冲击")
            if any(kw in after for kw in ["!", "！"]):
                techniques.append("情感爆发")
            if len(before) > 100:
                techniques.append("前后对比")

        return techniques

    def _extract_formulas(self, text: str, hotspots: List[HotspotAnalysis]) -> List[str]:
        """提取写作公式"""
        formulas = []

        for hotspot in hotspots:
            if hotspot.hotspot_type == HotspotType.READ_PARISING:
                formulas.append("打脸公式: 震惊反应 + 事实揭示 + 对方后悔")
            elif hotspot.hotspot_type == HotspotType.PLOT_REVERSAL:
                formulas.append("反转公式: 误导 + 暗示 + 真相揭示")

        if len(text) > 5000:
            formulas.append("长篇公式: 单元剧情 + 主线推进 + 阶段性高潮")

        return list(set(formulas))

    def _analyze_market_positioning(self, metadata: Dict) -> str:
        """分析市场定位"""
        genre = metadata.get("genre", "玄幻")
        target = metadata.get("target_platform", "通用")

        positioning_map = {
            ("玄幻", "起点"): "男频升级流，主打热血战斗",
            ("玄幻", "晋江"): "女频修仙，感情线为主",
            ("都市", "番茄"): "快节奏打脸，爽文为主",
            ("言情", "晋江"): "甜虐交织，情感细腻"
        }

        return positioning_map.get((genre, target), f"{genre}题材，{target}平台")

    def _generate_takeaways(self, hotspots: List[HotspotAnalysis],
                           formulas: List[str]) -> List[str]:
        """生成要点总结"""
        takeaways = []

        hotspot_counts = Counter(h.hotspot_type.value for h in hotspots)
        if hotspot_counts:
            top_hotspot = hotspot_counts.most_common(1)[0][0]
            takeaways.append(f"核心爽点类型: {top_hotspot}")

        if formulas:
            takeaways.append(f"主要写作公式: {formulas[0]}")

        takeaways.append("建议：开头300字必须出现核心冲突或金手指")

        return takeaways

    def get_bestseller_recommendations(self, genre: str = "all") -> str:
        """获取爆款小说推荐"""
        result = []
        result.append("="*60)
        result.append("📚 NWACS V8.6 2020-2026爆款小说推荐")
        result.append("="*60)
        
        if genre in ["all", "玄幻", "仙侠"]:
            result.append("\n🔥 起点玄幻/仙侠 TOP5:")
            result.append("-"*60)
            for book in self.bestseller_database["qidian_xuanhuan"]:
                result.append(f"{book['rank']}. 《{book['title']}》 作者:{book['author']} 评分:{book['score']}")
                result.append(f"   核心特色: {', '.join(book['key_features'])}")
                result.append(f"   数据: {book['data']}")
        
        if genre in ["all", "都市", "悬疑"]:
            result.append("\n🍅 番茄小说 TOP5:")
            result.append("-"*60)
            for book in self.bestseller_database["fanqie_novel"]:
                result.append(f"{book['rank']}. 《{book['title']}》 作者:{book['author']} 评分:{book['score']}")
                result.append(f"   核心特色: {', '.join(book['key_features'])}")
                result.append(f"   数据: {book['data']}")
        
        if genre in ["all", "言情", "现言"]:
            result.append("\n💖 晋江言情 TOP5:")
            result.append("-"*60)
            for book in self.bestseller_database["jjwxc_romance"]:
                result.append(f"{book['rank']}. 《{book['title']}》 作者:{book['author']} 评分:{book['score']}")
                result.append(f"   核心特色: {', '.join(book['key_features'])}")
                result.append(f"   数据: {book['data']}")
        
        result.append("\n✨ 2020-2026爆款套路总结:")
        result.append("-"*60)
        for i, pattern in enumerate(self.bestseller_database["top_patterns"], 1):
            result.append(f"  {i}. {pattern}")
        
        result.append("\n" + "="*60)
        return "\n".join(result)
    
    def generate_template_prompt(self, report: BestsellerReport) -> str:
        """根据拆解报告生成模板提示词"""
        prompt = f"""基于以下爆款小说的写作公式，请创作一个新故事。

小说类型：{report.genre}
市场定位：{report.market_positioning}

关键写作公式：
{chr(10).join(report.writing_formulas)}

核心爽点设计：
{chr(10).join(report.key_takeaways)}

请按照以上公式创作一个{report.total_chapters}章的故事大纲。"""

        return prompt


def main():
    print("="*60)
    print("📊 NWACS V8.6 爆款小说拆解系统")
    print("="*60)

    analyzer = BestsellerAnalyzer()

    print("\n📚 写作公式库:")
    for category, formulas in list(analyzer.formulas.items())[:3]:
        print(f"  {category}:")
        for formula in formulas[:2]:
            print(f"    • {formula}")

    print("\n🔥 爽点类型:")
    for htype in HotspotType:
        print(f"  • {htype.value}")

    print("\n📋 分析模式:")
    for pattern_name, pattern in list(analyzer.patterns.items())[:3]:
        print(f"  {pattern_name}: {pattern.get('description', '')}")
    
    print("\n" + analyzer.get_bestseller_recommendations())

    print("\n" + "="*60)
    print("✅ 爆款拆解系统就绪")
    print("="*60)


if __name__ == "__main__":
    main()