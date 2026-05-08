#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS AI智能润色器 - AIPolisher

参考万文通/笔灵/笔仗等主流AI去痕工具的核心能力：
1. 多级处理流水线 - 轻度润色 → 中度改写 → 深度重构
2. AI痕迹模式库 - 20+种AI生成文本特征模式
3. 风格转换引擎 - 学术/网文/口语/文学等多种风格
4. 语义保留改写 - 改表达不改意思，保留专业术语
5. 格式无损处理 - 保留段落/标点/排版结构

设计原则：
- 不是简单同义词替换，而是语义级重构
- 四级流水线层层递进，从轻到重
- 每次改写都有"改写前→改写后→修改说明"对照
"""

import json
import os
import random
import re
import time
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


API_KEY = "sk-f3246fbd1eef446e9a11d78efefd9bba"
BASE_URL = "https://api.deepseek.com"


class PolishLevel(Enum):
    LIGHT = ("轻度润色", "仅优化语句通顺度，修正语病错字，不改变原意和风格")
    MEDIUM = ("中度改写", "调整句式结构，丰富表达，去除AI模板化痕迹")
    DEEP = ("深度重构", "语义级重构，打散AI句式，注入人类写作特征")
    CREATIVE = ("创意重写", "保留核心意思，完全重新组织语言和结构")


class WritingStyle(Enum):
    WEB_NOVEL = ("网文风格", "口语化、节奏感强、爽点密集、对话生动")
    LITERARY = ("文学风格", "语言优美、意境深远、修辞丰富、节奏舒缓")
    ACADEMIC = ("学术风格", "严谨规范、逻辑清晰、术语准确、客观中立")
    JOURNALISTIC = ("新闻风格", "简洁明了、信息密集、客观报道、时效性强")
    CASUAL = ("口语风格", "自然随意、贴近生活、亲切感强、句式灵活")
    CINEMATIC = ("影视风格", "镜头语言、画面感强、感官丰富、节奏多变")


@dataclass
class PolishResult:
    original: str
    polished: str
    level: str
    style: str
    changes: List[Dict[str, str]]
    ai_trace_before: float
    ai_trace_after: float
    quality_before: float
    quality_after: float
    processing_time: float
    word_count_change: Tuple[int, int]


AI_TRACE_PATTERNS = [
    # === 内容模式 (6种) ===
    {
        "name": "过度强调意义",
        "pattern": r'(?:作为[^，,。]{2,20}(?:体现|证明|象征|标志|缩影)|凸显了[^，,。]{2,20}(?:重要性|意义|价值))',
        "description": "AI偏好赋予事物过度意义，人类写作更直接",
        "severity": "high",
    },
    {
        "name": "过度强调知名度",
        "pattern": r'(?:被[^，,。]{2,15}(?:誉为|称为|评为|视为)|广受[^，,。]{2,10}(?:好评|关注|赞誉))',
        "description": "AI反复列举知名度而不提供上下文",
        "severity": "medium",
    },
    {
        "name": "宣传广告式语言",
        "pattern": r'(?:颠覆[^，,。]{2,10}(?:式|性)|革命性|划时代|前所未有|无与伦比)',
        "description": "AI偏好的夸大宣传用语",
        "severity": "high",
    },
    {
        "name": "模糊归因",
        "pattern": r'(?:专家认为|业内人士指出|行业报告显示|研究表明|数据显示|据了解|据悉)',
        "description": "AI使用模糊来源增加可信度",
        "severity": "high",
    },
    {
        "name": "提纲式结构",
        "pattern": r'(?:挑战与[^，,。]{2,10}(?:展望|对策|建议)|问题与[^，,。]{2,10}(?:对策|出路))',
        "description": "AI偏好的二元对立标题结构",
        "severity": "medium",
    },
    {
        "name": "肤浅分析结尾",
        "pattern": r'(?:通过[^，,。]{5,30}(?:实现|达成|完成|促进|推动)[^，,。]{2,10}(?:发展|进步|提升))',
        "description": "AI万能公式句式，分析流于表面",
        "severity": "high",
    },

    # === 语言语法模式 (6种) ===
    {
        "name": "AI高频词汇",
        "pattern": r'(?:此外|至关重要|深入探讨|不可忽视|毋庸置疑|不言而喻|显而易见)',
        "description": "AI过度使用的高频学术词汇",
        "severity": "high",
    },
    {
        "name": "避免使用'是'",
        "pattern": r'(?:作为|代表|标志着|意味着|体现为|表现为|呈现出)',
        "description": "AI刻意避免简单系动词，用复杂表达替代",
        "severity": "medium",
    },
    {
        "name": "否定式排比",
        "pattern": r'(?:不是[^，,。]{3,20}(?:而是|也不是)[^，,。]{3,20})',
        "description": "AI偏好的'不是...而是...'排比结构",
        "severity": "medium",
    },
    {
        "name": "三段式法则",
        "pattern": r'(?:第一[，,].*?第二[，,].*?第三|首先[，,].*?其次[，,].*?(?:最后|再次|此外))',
        "description": "AI强行将想法分成三组",
        "severity": "high",
    },
    {
        "name": "刻意换词",
        "pattern": r'',
        "description": "AI为避免重复而过度使用同义词",
        "severity": "low",
        "check_func": "check_synonym_overuse",
    },
    {
        "name": "虚假范围",
        "pattern": r'从[^，,。]{2,10}到[^，,。]{2,10}',
        "description": "AI偏好的'从X到Y'虚假范围表达",
        "severity": "medium",
    },

    # === 风格模式 (6种) ===
    {
        "name": "破折号过度使用",
        "pattern": r'——',
        "description": "AI大量使用破折号连接句子",
        "severity": "medium",
    },
    {
        "name": "总分总模板句",
        "pattern": r'(?:总的来说|综上所述|总而言之|概括而言|总体来看|总的来看)',
        "description": "AI偏好的总结句式",
        "severity": "high",
    },
    {
        "name": "值得注意的是",
        "pattern": r'(?:值得注意的是|值得一提的是|需要指出的是|不容忽视的是|需要说明的是)',
        "description": "AI高频过渡词，显得机械刻板",
        "severity": "high",
    },
    {
        "name": "万能开头句式",
        "pattern": r'随着[^，,。]{3,20}(?:发展|进步|演变|推进|深入|变化)',
        "description": "AI万能开头句式'随着...的发展'",
        "severity": "high",
    },
    {
        "name": "万能结尾句式",
        "pattern": r'(?:让我们[^，,。]{3,20}(?:携手|共同|一起)|相信[^，,。]{3,20}(?:未来|明天))',
        "description": "AI万能结尾空泛号召",
        "severity": "high",
    },
    {
        "name": "成语排比",
        "pattern": r'(?:[^\s]{2}){3,}(?:、[^\s]{2}){2,}',
        "description": "AI偏好的四字词语排比",
        "severity": "medium",
    },

    # === 交流模式 (3种) ===
    {
        "name": "协作交流痕迹",
        "pattern": r'(?:希望[^，,。]{2,20}(?:对您|对你|能帮|有帮)|如果[^，,。]{2,20}(?:有帮助|有疑问|需要))',
        "description": "AI协作式结尾，暴露AI身份",
        "severity": "high",
    },
    {
        "name": "知识截止日期",
        "pattern": r'(?:截至[^，,。]{2,20}(?:为止|目前)|根据[^，,。]{2,20}(?:最新|目前).*?数据)',
        "description": "AI知识截止日期免责声明",
        "severity": "medium",
    },
    {
        "name": "谄媚语态",
        "pattern": r'(?:非常[^，,。]{2,10}(?:感谢|荣幸|高兴)|很[^，,。]{2,10}(?:高兴|荣幸|期待))',
        "description": "AI过度礼貌的谄媚表达",
        "severity": "low",
    },

    # === 网文小说特有AI痕迹 ===
    {
        "name": "情感直述",
        "pattern": r'(?:他感到|他觉得|他认为|他心想|他意识到|他明白|他察觉)',
        "description": "直接陈述情感而非外化表现（网文大忌）",
        "severity": "high",
    },
    {
        "name": "程度副词堆砌",
        "pattern": r'(?:非常|十分|极其|特别|相当|尤为|格外|颇为|甚是)',
        "description": "AI过度使用程度副词",
        "severity": "medium",
    },
    {
        "name": "的的不绝",
        "pattern": r'[^，,。]{10,}(?:的[^，,。]{2,10}){3,}',
        "description": "连续使用多个'的'，AI典型特征",
        "severity": "medium",
    },
    {
        "name": "万能动词",
        "pattern": r'(?:进行|做出|加以|予以|给予|展开|开展)(?:了)?(?:一[^，,。]*?)?(?:的)?',
        "description": "AI偏好的虚化动词",
        "severity": "high",
    },
    {
        "name": "具有重要(意义|价值)",
        "pattern": r'具有重要的?(?:意义|价值|作用|影响|地位)',
        "description": "AI万能评价句式",
        "severity": "high",
    },
    {
        "name": "在...过程中/背景下",
        "pattern": r'在[^，,。]{4,20}(?:过程中|背景下|基础上|前提下|条件下)',
        "description": "AI高频状语框架",
        "severity": "medium",
    },
    {
        "name": "呈现出...态势/趋势",
        "pattern": r'呈现出[^，,。]{3,20}(?:态势|趋势|特征|特点|格局)',
        "description": "AI万能描述句式",
        "severity": "high",
    },
    {
        "name": "逻辑连接词密集",
        "pattern": r'(?:因此|所以|于是|从而|进而|因而|故此)',
        "description": "AI过度使用因果连接词",
        "severity": "medium",
    },
    {
        "name": "可以(看出|发现|说|认为)",
        "pattern": r'可以(?:看出|发现|说|认为|预见|想象|理解)',
        "description": "AI推测性表达过多",
        "severity": "medium",
    },
    {
        "name": "本章结束/未完待续",
        "pattern": r'(?:本章[结完]|未完待续|欲知后事|且听下回)',
        "description": "网文AI常见结尾模板",
        "severity": "high",
    },

    # === 结构模式 ===
    {
        "name": "主谓宾简单句重复",
        "pattern": r'',
        "description": "连续3句以上相同主谓宾结构",
        "severity": "medium",
        "check_func": "check_repeated_sentence_structure",
    },
    {
        "name": "段落长度均匀",
        "pattern": r'',
        "description": "每段长度过于均匀（AI特征）",
        "severity": "low",
        "check_func": "check_uniform_paragraphs",
    },
    {
        "name": "缺乏人称变化",
        "pattern": r'',
        "description": "全文主语单一，缺乏视角切换",
        "severity": "low",
        "check_func": "check_subject_diversity",
    },

    # === 新增：句式层面AI痕迹 (8种) ===
    {
        "name": "被动语态泛滥",
        "pattern": r'(?:被|受到|遭到|得到|获得|得以|受到|遭到)[^，,。]{2,15}(?:了)?',
        "description": "AI过度使用被动语态，人类写作偏好主动语态",
        "severity": "medium",
    },
    {
        "name": "长定语堆砌",
        "pattern": r'[^，,。]{30,}的[^，,。]{10,}的',
        "description": "AI在一个句子中堆砌多个'的'字定语",
        "severity": "medium",
    },
    {
        "name": "完美对称句",
        "pattern": r'',
        "description": "连续两句字数完全相同且结构对称",
        "severity": "low",
        "check_func": "check_perfect_symmetry",
    },
    {
        "name": "无主语流水句",
        "pattern": r'(?:通过|根据|基于|随着|针对|对于)[^，,。]{10,40}[，,][^，,。]{10,}',
        "description": "AI偏好的无主语长状语开头句式",
        "severity": "high",
    },
    {
        "name": "过度使用分号",
        "pattern": r'；[^；]{5,30}；',
        "description": "AI用分号制造伪复杂句式",
        "severity": "low",
    },
    {
        "name": "每段以主题句开头",
        "pattern": r'',
        "description": "每段第一句都是概括性主题句（AI论文特征）",
        "severity": "medium",
        "check_func": "check_topic_sentence_pattern",
    },
    {
        "name": "过度使用冒号解释",
        "pattern": r'：[^：]{10,50}：[^：]{10,}',
        "description": "AI用冒号层层解释，显得说教",
        "severity": "low",
    },
    {
        "name": "缺乏省略句",
        "pattern": r'',
        "description": "全文无省略号、无断句、无留白",
        "severity": "medium",
        "check_func": "check_lack_of_ellipsis",
    },

    # === 新增：用词层面AI痕迹 (8种) ===
    {
        "name": "抽象名词堆砌",
        "pattern": r'(?:性|化|度|率|力|感|观|论|学|法|式|型|态|体|系|制|器){2,}',
        "description": "AI堆砌'XX性''XX化'等抽象名词后缀",
        "severity": "high",
    },
    {
        "name": "万能形容词",
        "pattern": r'(?:显著|明显|突出|卓越|优异|良好|优秀|出色|杰出)',
        "description": "AI偏好的万能正面形容词",
        "severity": "medium",
    },
    {
        "name": "数据模糊化",
        "pattern": r'(?:大幅|显著|明显|极大|巨大|相当|一定|某种|某些)(?:提升|提高|增加|降低|减少|改善|优化)',
        "description": "AI用模糊副词替代具体数据",
        "severity": "high",
    },
    {
        "name": "过度使用'这''那'指代",
        "pattern": r'(?:这[^，,。]{2,15}(?:意味着|表明|说明|反映|体现|显示))',
        "description": "AI频繁使用'这意味着'等指代总结",
        "severity": "medium",
    },
    {
        "name": "缺乏口语词",
        "pattern": r'',
        "description": "全文无'说实话''说白了''你猜怎么着'等口语词",
        "severity": "low",
        "check_func": "check_lack_of_colloquial",
    },
    {
        "name": "缺乏语气词",
        "pattern": r'',
        "description": "全文无'呢''吧''啊''嘛'等语气助词",
        "severity": "low",
        "check_func": "check_lack_of_modal_particles",
    },
    {
        "name": "成语密集",
        "pattern": r'(?:[\u4e00-\u9fff]{4}){3,}',
        "description": "连续使用3个以上四字成语（AI炫技特征）",
        "severity": "medium",
    },
    {
        "name": "缺乏专有名词",
        "pattern": r'',
        "description": "全文缺乏具体品牌/地名/人名/作品名",
        "severity": "low",
        "check_func": "check_lack_of_proper_nouns",
    },

    # === 新增：逻辑层面AI痕迹 (6种) ===
    {
        "name": "完美因果链",
        "pattern": r'(?:因为[^，,。]{5,30}(?:所以|因此|因而)[^，,。]{5,30})',
        "description": "AI构建过于完美的因果关系链",
        "severity": "medium",
    },
    {
        "name": "缺乏思维跳跃",
        "pattern": r'',
        "description": "全文逻辑过于连贯，缺乏人类思维的跳跃和旁逸",
        "severity": "low",
        "check_func": "check_lack_of_logic_jumps",
    },
    {
        "name": "缺乏反问",
        "pattern": r'',
        "description": "全文无反问句，AI倾向陈述句",
        "severity": "low",
        "check_func": "check_lack_of_rhetorical_questions",
    },
    {
        "name": "缺乏让步",
        "pattern": r'',
        "description": "全文无论证让步（'当然''不过''话虽如此'），AI倾向线性论证",
        "severity": "medium",
        "check_func": "check_lack_of_concession",
    },
    {
        "name": "结论过于确定",
        "pattern": r'(?:一定|必然|绝对|肯定|毫无疑问|毋庸置疑|显然|必定)',
        "description": "AI给出过于确定的结论，人类倾向保留不确定性",
        "severity": "high",
    },
    {
        "name": "缺乏个人经验引用",
        "pattern": r'',
        "description": "全文无'我记得''有一次''我遇到过'等个人经验",
        "severity": "medium",
        "check_func": "check_lack_of_personal_experience",
    },

    # === GPTZero 7组件检测对抗模式 (12种) ===
    {
        "name": "Perplexity过低（文本过于可预测）",
        "pattern": r'',
        "description": "GPTZero核心指标：文本过于流畅可预测→低困惑度→AI特征。需注入意外词汇和非常规搭配",
        "severity": "high",
        "check_func": "check_low_perplexity_indicators",
    },
    {
        "name": "Burstiness过低（句长方差太小）",
        "pattern": r'',
        "description": "GPTZero核心指标：句长过于均匀→低爆发度→AI特征。需制造句长剧烈波动",
        "severity": "high",
        "check_func": "check_low_burstiness",
    },
    {
        "name": "缺乏通感修辞",
        "pattern": r'',
        "description": "AI几乎不使用通感（感官交叉描写），这是人类写作的高级特征",
        "severity": "medium",
        "check_func": "check_lack_of_synesthesia",
    },
    {
        "name": "缺乏回文/交错结构",
        "pattern": r'',
        "description": "Chiasmus（回文）是AI几乎不会使用的修辞结构",
        "severity": "medium",
        "check_func": "check_lack_of_chiasmus",
    },
    {
        "name": "缺乏烟火气/本土化细节",
        "pattern": r'',
        "description": "AI文本缺乏中国本土生活细节（撸串/麻将/人情世故）",
        "severity": "medium",
        "check_func": "check_lack_of_local_color",
    },
    {
        "name": "缺乏情绪外化动作链",
        "pattern": r'',
        "description": "AI倾向直接陈述情绪，人类用动作链外化情绪",
        "severity": "high",
        "check_func": "check_lack_of_emotion_externalization",
    },
    {
        "name": "缺乏段落呼吸变化",
        "pattern": r'',
        "description": "AI段落长度均匀，人类段落有明显长短变化",
        "severity": "medium",
        "check_func": "check_lack_of_paragraph_breathing",
    },
    {
        "name": "缺乏潜台词对话",
        "pattern": r'',
        "description": "AI对话直白如信息交换，人类对话话里有话",
        "severity": "high",
        "check_func": "check_lack_of_subtext_dialogue",
    },
    {
        "name": "缺乏特指锚定",
        "pattern": r'',
        "description": "AI用泛指，人类用特指（具体到哪一个/哪一根/哪一次）",
        "severity": "medium",
        "check_func": "check_lack_of_specific_anchors",
    },
    {
        "name": "缺乏思维跳跃/旁逸",
        "pattern": r'',
        "description": "AI逻辑过于连贯，人类思维有跳跃和旁逸斜出",
        "severity": "low",
        "check_func": "check_lack_of_digression",
    },
    {
        "name": "缺乏不完美表达",
        "pattern": r'',
        "description": "AI文本过于完美整洁，人类写作有口语词/停顿/语法瑕疵",
        "severity": "medium",
        "check_func": "check_lack_of_imperfection_markers",
    },
    {
        "name": "缺乏光影色彩描写",
        "pattern": r'',
        "description": "AI缺乏用光影和色彩暗示情绪的能力（张爱玲技法）",
        "severity": "medium",
        "check_func": "check_lack_of_light_color_emotion",
    },

    # === 朱雀AI检测专用模式（15种） ===
    {
        "name": "朱雀-情感平滑度过低",
        "pattern": r'',
        "description": "朱雀核心指标：全文情绪波动过于平稳，缺乏-8到+7的剧烈起伏",
        "severity": "high",
        "check_func": "check_zhuque_emotional_flatness",
    },
    {
        "name": "朱雀-缺乏主观抱怨/错误经验",
        "pattern": r'',
        "description": "朱雀三维降重法核心：缺乏'这鬼天气''谁TMD说''老子不答应'等主观抱怨",
        "severity": "high",
        "check_func": "check_zhuque_lack_of_complaint",
    },
    {
        "name": "朱雀-缺乏超小样本叙事",
        "pattern": r'',
        "description": "朱雀三维降重法核心：缺乏'我楼下保安''上周陪我妈'等个人微小叙事",
        "severity": "high",
        "check_func": "check_zhuque_lack_of_micro_narrative",
    },
    {
        "name": "朱雀-逻辑链过于完整",
        "pattern": r'(?:因为[^，,。]{5,30}(?:所以|因此|因而)[^，,。]{5,30})',
        "description": "朱雀核心指标：AI构建过于完美的因果链，人类会倒叙和情绪跳跃",
        "severity": "high",
    },
    {
        "name": "朱雀-缺乏情绪撕裂",
        "pattern": r'',
        "description": "朱雀对抗技法：缺乏恨到极致突然温柔、笑到一半突然哭的情绪撕裂",
        "severity": "medium",
        "check_func": "check_zhuque_lack_of_emotional_tear",
    },
    {
        "name": "朱雀-缺乏本土烟火气",
        "pattern": r'',
        "description": "朱雀对抗技法：缺乏大排档/棋牌室/递烟/敬酒/给面子等本土细节",
        "severity": "medium",
        "check_func": "check_zhuque_lack_of_local_color_extended",
    },
    {
        "name": "朱雀-缺乏角色缺陷",
        "pattern": r'',
        "description": "朱雀对抗技法：角色过于完美，缺乏路怒症/怕打针/分不清左右等真实缺陷",
        "severity": "medium",
        "check_func": "check_zhuque_lack_of_character_flaws",
    },
    {
        "name": "朱雀-缺乏自我纠正",
        "pattern": r'',
        "description": "朱雀对抗技法：缺乏'等等，不对''重新想一下''这个结论可能有问题'等思考过程",
        "severity": "medium",
        "check_func": "check_zhuque_lack_of_self_correction",
    },
    {
        "name": "朱雀-缺乏重复强调",
        "pattern": r'',
        "description": "朱雀对抗技法：缺乏'这个点很重要，真的很重要'等人类重复强调习惯",
        "severity": "low",
        "check_func": "check_zhuque_lack_of_repetition_emphasis",
    },
    {
        "name": "朱雀-缺乏倒叙/插叙",
        "pattern": r'',
        "description": "朱雀对抗技法：全文线性叙事，缺乏倒叙和插叙的人类非线性思维",
        "severity": "medium",
        "check_func": "check_zhuque_lack_of_flashback",
    },
    {
        "name": "朱雀-缺乏潜台词密度",
        "pattern": r'',
        "description": "朱雀对抗技法：对话过于直白如信息交换，缺乏话里有话的潜台词",
        "severity": "high",
        "check_func": "check_zhuque_lack_of_subtext_density",
    },
    {
        "name": "朱雀-缺乏物件细节锚定",
        "pattern": r'',
        "description": "朱雀对抗技法：缺乏缺口茶杯/磨损戒指/泛黄照片等物件细节",
        "severity": "medium",
        "check_func": "check_zhuque_lack_of_object_detail",
    },
    {
        "name": "朱雀-段落节奏均匀",
        "pattern": r'',
        "description": "朱雀核心指标：段落长度过于均匀，缺乏长短交替的呼吸感",
        "severity": "high",
        "check_func": "check_zhuque_uniform_paragraph_rhythm",
    },
    {
        "name": "朱雀-缺乏意外转折",
        "pattern": r'',
        "description": "朱雀核心指标：情节发展过于可预测，缺乏'突然''没想到''居然'等意外",
        "severity": "high",
        "check_func": "check_zhuque_lack_of_surprise_twist",
    },
    {
        "name": "朱雀-缺乏感官不平衡",
        "pattern": r'',
        "description": "朱雀对抗技法：视觉描写占比过高(>70%)，缺乏听觉/嗅觉/触觉/味觉",
        "severity": "medium",
        "check_func": "check_zhuque_sensory_imbalance",
    },
]



class AIPolisher:
    """AI智能润色器 - 50+种AI痕迹模式 + 12类人工特征注入"""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or API_KEY
        self.base_url = BASE_URL
        self.patterns = AI_TRACE_PATTERNS

    def detect_ai_traces(self, text: str) -> Dict:
        """多维度AI痕迹检测（v2.0 相对评分 — 基于文本长度归一化）"""
        results = {
            "total_score": 0,
            "max_score": 100,
            "patterns_found": [],
            "high_severity_count": 0,
            "medium_severity_count": 0,
            "low_severity_count": 0,
            "suggestions": [],
        }

        text_len = max(len(text), 1)
        raw_score = 0

        for pattern in self.patterns:
            min_len = pattern.get("min_text_length", 0)
            if text_len < min_len:
                continue

            pname = pattern.get("name", "")
            is_lack_pattern = "缺乏" in pname or pname.startswith("朱雀-")
            if is_lack_pattern and text_len < 1500:
                continue

            if pattern.get("pattern"):
                matches = re.findall(pattern["pattern"], text)
                if matches:
                    count = len(matches)
                    severity_weight = {"high": 2, "medium": 1, "low": 1}
                    weight = severity_weight.get(pattern["severity"], 1)
                    score = min(count * weight, 5)

                    results["patterns_found"].append({
                        "name": pattern["name"],
                        "count": count,
                        "severity": pattern["severity"],
                        "score": score,
                        "description": pattern["description"],
                    })
                    raw_score += score
                    results[f"{pattern['severity']}_severity_count"] += 1

            elif "check_func" in pattern:
                check_method = getattr(self, pattern["check_func"], None)
                if check_method:
                    found, score = check_method(text)
                    if found:
                        results["patterns_found"].append({
                            "name": pattern["name"],
                            "count": 1,
                            "severity": pattern["severity"],
                            "score": score,
                            "description": pattern["description"],
                        })
                        raw_score += score
                        results[f"{pattern['severity']}_severity_count"] += 1

        density_factor = max(text_len / 600, 0.6)
        normalized_score = raw_score / density_factor
        results["total_score"] = min(round(normalized_score), 100)

        if results["total_score"] >= 50:
            results["level"] = "high"
            results["suggestions"].append("AI痕迹明显，建议深度重构")
        elif results["total_score"] >= 25:
            results["level"] = "medium"
            results["suggestions"].append("存在一定AI痕迹，建议中度改写")
        else:
            results["level"] = "low"
            results["suggestions"].append("AI痕迹较少，可轻度润色或直接使用")

        if results["high_severity_count"] >= 3:
            results["suggestions"].append(
                f"发现{results['high_severity_count']}个高危AI特征，优先处理"
            )

        return results

    def check_repeated_sentence_structure(self, text: str) -> Tuple[bool, int]:
        sentences = re.split(r'[。！？]', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 5]
        if len(sentences) < 4:
            return False, 0

        repeated = 0
        for i in range(len(sentences) - 2):
            s1 = re.sub(r'[的地得了着过]', '', sentences[i])
            s2 = re.sub(r'[的地得了着过]', '', sentences[i + 1])
            s3 = re.sub(r'[的地得了着过]', '', sentences[i + 2])
            if len(s1) > 3 and len(s2) > 3 and len(s3) > 3:
                if (abs(len(s1) - len(s2)) <= 3 and abs(len(s2) - len(s3)) <= 3):
                    repeated += 1

        return repeated >= 2, min(repeated * 5, 15)

    def check_uniform_paragraphs(self, text: str) -> Tuple[bool, int]:
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        if len(paragraphs) < 4:
            return False, 0

        lengths = [len(p) for p in paragraphs]
        avg_len = sum(lengths) / len(lengths)
        uniform_count = sum(1 for l in lengths if abs(l - avg_len) / max(avg_len, 1) < 0.2)

        return uniform_count >= len(paragraphs) * 0.7, 8

    def check_subject_diversity(self, text: str) -> Tuple[bool, int]:
        sentences = re.split(r'[。！？]', text)
        subjects = []
        for s in sentences:
            s = s.strip()
            if len(s) > 5:
                first_word = s[:2]
                subjects.append(first_word)

        if len(subjects) < 5:
            return False, 0

        unique_ratio = len(set(subjects)) / len(subjects)
        return unique_ratio < 0.3, int((1 - unique_ratio) * 10)

    def check_synonym_overuse(self, text: str) -> Tuple[bool, int]:
        words = re.findall(r'[\u4e00-\u9fff]{2,4}', text)
        if len(words) < 30:
            return False, 0

        freq: Dict[str, int] = {}
        for w in words:
            freq[w] = freq.get(w, 0) + 1

        rare_words = sum(1 for c in freq.values() if c == 1)
        total_unique = len(freq)
        if total_unique == 0:
            return False, 0

        rare_ratio = rare_words / total_unique
        return rare_ratio > 0.75, min(int(rare_ratio * 5), 5)

    def check_perfect_symmetry(self, text: str) -> Tuple[bool, int]:
        sentences = re.split(r'[。！？]', text)
        symmetric_count = 0
        for i in range(len(sentences) - 1):
            s1 = sentences[i].strip()
            s2 = sentences[i + 1].strip()
            if len(s1) > 5 and len(s2) > 5 and abs(len(s1) - len(s2)) <= 1:
                symmetric_count += 1
        score = min(5, symmetric_count * 2)
        return symmetric_count >= 3, score

    def check_topic_sentence_pattern(self, text: str) -> Tuple[bool, int]:
        paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
        if len(paragraphs) < 3:
            return False, 0
        topic_patterns = [
            r'^(?:在|随着|当|对于|关于|从|根据|通过|基于)',
            r'^(?:首先|其次|最后|第一|第二|第三|一方面|另一方面)',
            r'^(?:总的来看|综上所述|整体而言|从.*来看)',
        ]
        topic_count = 0
        for p in paragraphs:
            for pat in topic_patterns:
                if re.match(pat, p):
                    topic_count += 1
                    break
        ratio = topic_count / len(paragraphs)
        return ratio > 0.5, int(ratio * 10)

    def check_lack_of_ellipsis(self, text: str) -> Tuple[bool, int]:
        has_ellipsis = '…' in text or '...' in text
        has_dash = '——' in text or '—' in text
        if not has_ellipsis and not has_dash:
            return True, 5
        if not has_ellipsis:
            return True, 5
        return False, 0

    def check_lack_of_colloquial(self, text: str) -> Tuple[bool, int]:
        colloquial_patterns = [
            r'说实话', r'说白了', r'你猜怎么着', r'说真的',
            r'老实说', r'不瞒你说', r'讲真', r'其实吧',
            r'怎么说呢', r'有意思的是', r'你懂的',
        ]
        found = sum(1 for p in colloquial_patterns if re.search(p, text))
        if found == 0:
            return True, 5
        if found < 2:
            return True, 4
        return False, 0

    def check_lack_of_modal_particles(self, text: str) -> Tuple[bool, int]:
        particles = ['呢', '吧', '啊', '嘛', '呗', '啦', '哦', '哟']
        found = sum(1 for p in particles if p in text)
        if found == 0:
            return True, 5
        if found < 3:
            return True, 4
        return False, 0

    def check_lack_of_proper_nouns(self, text: str) -> Tuple[bool, int]:
        proper_patterns = [
            r'(?:[A-Z][a-z]+(?:\s[A-Z][a-z]+)*)',  # 英文专有名词
            r'(?:《[^》]+》)',  # 书名号
            r'(?:[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤川青藏琼宁][A-Z]?\d{4,5}[A-Za-z]?)',  # 车牌号
        ]
        found = sum(1 for p in proper_patterns if re.search(p, text))
        if found < 2:
            return True, 5
        return False, 0

    def check_lack_of_logic_jumps(self, text: str) -> Tuple[bool, int]:
        jump_markers = [
            r'话说回来', r'扯远了', r'跑题了', r'突然想到',
            r'对了', r'顺便说一句', r'插一句', r'等等',
        ]
        found = sum(1 for m in jump_markers if re.search(m, text))
        if found == 0:
            return True, 5
        return False, 0

    def check_lack_of_rhetorical_questions(self, text: str) -> Tuple[bool, int]:
        rhetorical = re.findall(r'[^。！？]*[？?]', text)
        if len(rhetorical) == 0:
            return True, 5
        if len(rhetorical) < 2:
            return True, 4
        return False, 0

    def check_lack_of_concession(self, text: str) -> Tuple[bool, int]:
        concession_markers = [
            r'当然', r'不过', r'话虽如此', r'虽说',
            r'诚然', r'不可否认', r'退一步说', r'换个角度看',
        ]
        found = sum(1 for m in concession_markers if re.search(m, text))
        if found == 0:
            return True, 5
        if found < 2:
            return True, 3
        return False, 0

    def check_lack_of_personal_experience(self, text: str) -> Tuple[bool, int]:
        experience_markers = [
            r'我记得', r'有一次', r'我遇到过', r'我经历过',
            r'我见过', r'我听说', r'我认识.*人', r'我.*朋友',
        ]
        found = sum(1 for m in experience_markers if re.search(m, text))
        if found == 0:
            return True, 5
        return False, 0

    def check_low_perplexity_indicators(self, text: str) -> Tuple[bool, int]:
        """检测Perplexity过低特征：文本过于流畅可预测"""
        sentences = re.split(r'[。！？]', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 5]
        if len(sentences) < 5:
            return False, 0

        predictable_count = 0
        predictable_patterns = [
            r'^(?:他|她|它|我|你|我们|他们|她们)[的地得]',
            r'^(?:在|随着|当|对于|关于|从|根据|通过|基于)',
            r'^(?:首先|其次|最后|第一|第二|第三)',
            r'^(?:因此|所以|于是|从而|进而)',
            r'^(?:这|那)(?:意味着|表明|说明|反映)',
        ]
        for s in sentences:
            for pat in predictable_patterns:
                if re.match(pat, s):
                    predictable_count += 1
                    break

        ratio = predictable_count / len(sentences)
        if ratio > 0.5:
            return True, int(ratio * 15)
        if ratio > 0.3:
            return True, int(ratio * 10)
        return False, 0

    def check_low_burstiness(self, text: str) -> Tuple[bool, int]:
        """检测Burstiness过低：句长方差太小"""
        sentences = re.split(r'[。！？\n]', text)
        lengths = [len(s.strip()) for s in sentences if len(s.strip()) > 3]
        if len(lengths) < 8:
            return False, 0

        avg_len = sum(lengths) / len(lengths)
        variance = sum((l - avg_len) ** 2 for l in lengths) / len(lengths)
        std_dev = variance ** 0.5

        if std_dev < 5:
            return True, 5
        if std_dev < 8:
            return True, 4
        if std_dev < 12:
            return True, 2
        return False, 0

    def check_lack_of_synesthesia(self, text: str) -> Tuple[bool, int]:
        """检测缺乏通感修辞"""
        synesthesia_patterns = [
            r'(?:声音|笑声|歌声|琴声|风声|雨声).{0,10}(?:像|如|似|仿佛).{0,10}(?:光|色|闪|亮|暗|明)',
            r'(?:光|色|影|暗|明).{0,10}(?:像|如|似|仿佛).{0,10}(?:声|音|响|鸣)',
            r'(?:香|味|气|臭).{0,10}(?:像|如|似|仿佛).{0,10}(?:声|音|光|色)',
            r'(?:冷|热|暖|凉|冰|烫).{0,10}(?:像|如|似|仿佛).{0,10}(?:声|音|光|色)',
        ]
        found = sum(1 for p in synesthesia_patterns if re.search(p, text))
        if found == 0:
            return True, 5
        return False, 0

    def check_lack_of_chiasmus(self, text: str) -> Tuple[bool, int]:
        """检测缺乏回文/交错结构"""
        chiasmus_patterns = [
            r'(.{2,8})(?:不是|并非|没有).{2,8}\1',
            r'(.{2,8}).{2,8}(?:是|就是|才是).{2,8}\1',
            r'(.{2,8}).{2,8}(?:换|换回|换来).{2,8}\1',
        ]
        found = sum(1 for p in chiasmus_patterns if re.search(p, text))
        if found == 0:
            return True, 5
        return False, 0

    def check_lack_of_local_color(self, text: str) -> Tuple[bool, int]:
        """检测缺乏烟火气/本土化细节"""
        local_markers = [
            r'撸串', r'烧烤', r'大排档', r'麻将', r'茶馆', r'棋牌室',
            r'豆浆', r'油条', r'煎饼', r'火锅', r'串串', r'麻辣烫',
            r'老天爷', r'祖宗', r'面子', r'人情', r'关系', r'走后门',
            r'递烟', r'敬酒', r'红包', r'份子钱', r'赶集', r'庙会',
            r'绿皮火车', r'小灵通', r'BB机', r'IC卡', r'公用电话',
        ]
        found = sum(1 for m in local_markers if re.search(m, text))
        if found == 0:
            return True, 5
        if found < 2:
            return True, 3
        return False, 0

    def check_lack_of_emotion_externalization(self, text: str) -> Tuple[bool, int]:
        """检测缺乏情绪外化动作链"""
        direct_emotion = len(re.findall(
            r'(?:他感到|他觉得|他认为|他心想|他意识到|他明白|他察觉|'
            r'她感到|她觉得|她认为|她心想|她意识到|她明白|她察觉)',
            text
        ))
        action_chains = len(re.findall(
            r'(?:攥|握|掐|捏|按|敲|拍|踢|踹|撞|推|拉|扯|撕|咬|'
            r'咽|吞|吸|呼|喘|抖|颤|缩|退|冲|扑|跪|倒|摔|跌)',
            text
        ))

        if direct_emotion > 3 and action_chains < 5:
            return True, 5
        if direct_emotion > 1 and action_chains < 3:
            return True, 5
        return False, 0

    def check_lack_of_paragraph_breathing(self, text: str) -> Tuple[bool, int]:
        """检测缺乏段落呼吸变化"""
        paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
        if len(paragraphs) < 5:
            return False, 0

        lengths = [len(p) for p in paragraphs]
        avg_len = sum(lengths) / len(lengths)

        consecutive_uniform = 0
        max_consecutive = 0
        for l in lengths:
            if abs(l - avg_len) / max(avg_len, 1) < 0.25:
                consecutive_uniform += 1
                max_consecutive = max(max_consecutive, consecutive_uniform)
            else:
                consecutive_uniform = 0

        if max_consecutive >= 5:
            return True, 5
        if max_consecutive >= 3:
            return True, 5
        return False, 0

    def check_lack_of_subtext_dialogue(self, text: str) -> Tuple[bool, int]:
        """检测缺乏潜台词对话"""
        dialogue_lines = re.findall(r'["""][^""""]{5,80}["""]', text)
        dialogue_lines += re.findall(r"'[^']{5,80}'", text)

        if len(dialogue_lines) < 3:
            return False, 0

        flat_dialogue = 0
        for line in dialogue_lines:
            if re.search(r'(?:你好|谢谢|对不起|没关系|再见|好的|是的|不是|可以|不行)', line):
                flat_dialogue += 1
            if re.search(r'^(?:我|你|他|她)(?:觉得|认为|想|要|会|能)', line):
                flat_dialogue += 1

        ratio = flat_dialogue / len(dialogue_lines)
        if ratio > 0.6:
            return True, 5
        if ratio > 0.3:
            return True, 5
        return False, 0

    def check_lack_of_specific_anchors(self, text: str) -> Tuple[bool, int]:
        """检测缺乏特指锚定"""
        specific_patterns = [
            r'第[一二三四五六七八九十\d]+[个根次条把张只]',
            r'\d+[年月日时分秒]',
            r'[《〈][^》〉]+[》〉]',
            r'[A-Z][a-z]+(?:\s[A-Z][a-z]+)*',
            r'(?:牌|型号|编号|代码)[：:]\S+',
        ]
        found = sum(1 for p in specific_patterns if re.search(p, text))
        text_len = len(text)
        density = found / (text_len / 1000) if text_len > 0 else 0

        if density < 0.5:
            return True, 5
        if density < 1.0:
            return True, 4
        return False, 0

    def check_lack_of_digression(self, text: str) -> Tuple[bool, int]:
        """检测缺乏思维跳跃/旁逸"""
        digression_markers = [
            r'话说回来', r'扯远了', r'跑题了', r'突然想到',
            r'对了', r'顺便说一句', r'插一句', r'等等',
            r'有意思的是', r'说来也怪', r'不知怎么',
        ]
        found = sum(1 for m in digression_markers if re.search(m, text))
        if found == 0:
            return True, 5
        return False, 0

    def check_lack_of_imperfection_markers(self, text: str) -> Tuple[bool, int]:
        """检测缺乏不完美表达"""
        imperfection_markers = [
            r'…', r'\.\.\.', r'——', r'—',
            r'说实话', r'说白了', r'你猜怎么着', r'说真的',
            r'老实说', r'不瞒你说', r'讲真', r'其实吧',
            r'怎么说呢', r'你懂的', r'有点迷', r'这里要划重点',
            r'嗯', r'呃', r'那个', r'就是',
        ]
        found = sum(1 for m in imperfection_markers if re.search(m, text))
        text_len_k = len(text) / 1000 if len(text) > 0 else 1
        density = found / text_len_k

        if density < 1:
            return True, 5
        if density < 2:
            return True, 4
        return False, 0

    def check_lack_of_light_color_emotion(self, text: str) -> Tuple[bool, int]:
        """检测缺乏光影色彩描写"""
        light_color_patterns = [
            r'(?:光|影|暗|明|亮|黑|白|红|蓝|绿|黄|紫|灰|金|银|'
            r'昏|暗|淡|浓|浅|深|暖|冷|柔|刺|灼|寒)',
            r'(?:夕阳|落日|晨曦|暮色|月色|星光|烛光|灯光|火光|'
            r'霞光|余晖|曙光|夜色|黄昏|黎明|傍晚)',
            r'(?:色|彩|调|泽|晕|芒|辉|斑|纹|影)',
        ]
        found = sum(1 for p in light_color_patterns if re.search(p, text))
        text_len_k = len(text) / 1000 if len(text) > 0 else 1
        density = found / text_len_k

        if density < 3:
            return True, 5
        if density < 5:
            return True, 4
        return False, 0

    # ============================================================
    # 朱雀AI检测专用检测函数（15种）
    # ============================================================

    def check_zhuque_emotional_flatness(self, text: str) -> Tuple[bool, int]:
        """朱雀-检测情感平滑度过低"""
        high_emotion = len(re.findall(
            r'(?:怒吼|咆哮|尖叫|大哭|狂笑|暴怒|崩溃|绝望|疯狂|'
            r'颤抖|哆嗦|瘫|跪|砸|摔|撕|踹|撞)',
            text
        ))
        low_emotion = len(re.findall(
            r'(?:沉默|安静|平静|淡淡|轻轻|缓缓|默默|静静|'
            r'叹息|苦笑|愣|怔|呆)',
            text
        ))
        text_len_k = len(text) / 1000 if len(text) > 0 else 1

        if high_emotion == 0 and low_emotion > 3:
            return True, 5
        if high_emotion < text_len_k:
            return True, 5
        if high_emotion < text_len_k * 2:
            return True, 4
        return False, 0

    def check_zhuque_lack_of_complaint(self, text: str) -> Tuple[bool, int]:
        """朱雀-检测缺乏主观抱怨/错误经验"""
        complaint_patterns = [
            r'(?:鬼天气|绝了|TMD|妈的|卧槽|我靠|坑爹|要命|'
            r'受不了|崩溃了|疯了|有毒|离谱|无语|服了)',
            r'(?:老子|老娘|本小姐|本大爷|你大爷)',
            r'(?:谁(?:TM|他妈|特么).*?(?:说|告诉|讲))',
            r'(?:吃了一个月泡面|熬夜熬到|加班加到|排队排了)',
        ]
        found = sum(1 for p in complaint_patterns if re.search(p, text))
        if found == 0:
            return True, 5
        if found < 2:
            return True, 5
        return False, 0

    def check_zhuque_lack_of_micro_narrative(self, text: str) -> Tuple[bool, int]:
        """朱雀-检测缺乏超小样本叙事"""
        micro_patterns = [
            r'(?:我楼下|我隔壁|我同事|我朋友|我同学|我亲戚|'
            r'我家|我妈|我爸|我老婆|我老公|我孩子)',
            r'(?:上周|昨天|前天|今天早上|刚才|刚刚)',
            r'(?:有一次|有一回|记得.*?年|那年|那时候)',
            r'(?:陪.*?(?:逛|买|去|看|吃|喝))',
        ]
        found = sum(1 for p in micro_patterns if re.search(p, text))
        if found == 0:
            return True, 5
        if found < 2:
            return True, 5
        return False, 0

    def check_zhuque_lack_of_emotional_tear(self, text: str) -> Tuple[bool, int]:
        """朱雀-检测缺乏情绪撕裂"""
        tear_patterns = [
            r'(?:恨|怒|气|骂|吼|砸|摔).{5,50}(?:温柔|软|轻|笑|爱|想|念)',
            r'(?:笑|乐|喜|欢|爱).{5,50}(?:哭|泪|痛|伤|悲|恨)',
            r'(?:但|却|可|不过).{0,10}(?:偷偷|悄悄|默默|暗暗)',
        ]
        found = sum(1 for p in tear_patterns if re.search(p, text))
        if found == 0:
            return True, 5
        return False, 0

    def check_zhuque_lack_of_local_color_extended(self, text: str) -> Tuple[bool, int]:
        """朱雀-检测缺乏本土烟火气（扩展版）"""
        local_extended = [
            r'大排档', r'棋牌室', r'菜市场', r'广场舞', r'太极拳',
            r'递烟', r'敬酒', r'给面子', r'走后门', r'托关系',
            r'份子钱', r'压岁钱', r'拜年', r'串门', r'唠嗑',
            r'绿皮火车', r'硬座', r'站票', r'黄牛', r'票贩子',
            r'小灵通', r'BP机', r'IC卡', r'公用电话', r'寻呼台',
            r'录像厅', r'游戏厅', r'网吧包夜', r'租书店',
            r'二八大杠', r'凤凰牌', r'永久牌', r'飞鸽牌',
            r'的确良', r'喇叭裤', r'蛤蟆镜', r'回力鞋',
        ]
        found = sum(1 for m in local_extended if re.search(m, text))
        if found == 0:
            return True, 5
        if found < 2:
            return True, 4
        return False, 0

    def check_zhuque_lack_of_character_flaws(self, text: str) -> Tuple[bool, int]:
        """朱雀-检测缺乏角色缺陷"""
        flaw_patterns = [
            r'(?:怕|恐惧|害怕|不敢).{0,5}(?:打针|抽血|高|黑|鬼|蛇|老鼠|蟑螂)',
            r'(?:路怒|暴脾气|急脾气|臭脾气|倔脾气)',
            r'(?:分不清|搞不懂|记不住|学不会|做不好)',
            r'(?:强迫症|洁癖|拖延症|选择困难|社恐)',
            r'(?:嗜好|癖好|瘾|迷|控).{0,5}(?:烟|酒|咖啡|茶|游戏|麻将)',
        ]
        found = sum(1 for p in flaw_patterns if re.search(p, text))
        if found == 0:
            return True, 5
        return False, 0

    def check_zhuque_lack_of_self_correction(self, text: str) -> Tuple[bool, int]:
        """朱雀-检测缺乏自我纠正"""
        correction_patterns = [
            r'(?:等等|不对|等一下|慢着|且慢)',
            r'(?:重新想|再想想|仔细想|琢磨|斟酌)',
            r'(?:这个结论|这个判断|这个想法).{0,10}(?:有问题|不对|不准确|太草率)',
            r'(?:我.*?(?:错了|搞错了|弄错了|误会了|想多了))',
        ]
        found = sum(1 for p in correction_patterns if re.search(p, text))
        if found == 0:
            return True, 5
        return False, 0

    def check_zhuque_lack_of_repetition_emphasis(self, text: str) -> Tuple[bool, int]:
        """朱雀-检测缺乏重复强调"""
        emphasis_patterns = [
            r'(.{2,10})[，,]\s*\1',
            r'(?:很重要|非常.*?重要|关键|核心|根本).{0,20}(?:很重要|非常.*?重要|关键|核心|根本)',
            r'(?:真的|确实|的确|实在).{0,10}(?:真的|确实|的确|实在)',
            r'(?:别不信|不骗你|说真的|讲真|实话)',
        ]
        found = sum(1 for p in emphasis_patterns if re.search(p, text))
        if found == 0:
            return True, 5
        return False, 0

    def check_zhuque_lack_of_flashback(self, text: str) -> Tuple[bool, int]:
        """朱雀-检测缺乏倒叙/插叙"""
        flashback_patterns = [
            r'(?:那年|那时候|当年|从前|曾经|过去|以前)',
            r'(?:回忆起|回想起|想起|记得|记忆)',
            r'(?:如果.*?年|假如.*?年|要是.*?年)',
            r'(?:画面.*?闪|镜头.*?切|时间.*?倒)',
        ]
        found = sum(1 for p in flashback_patterns if re.search(p, text))
        if found == 0:
            return True, 5
        if found < 2:
            return True, 3
        return False, 0

    def check_zhuque_lack_of_subtext_density(self, text: str) -> Tuple[bool, int]:
        """朱雀-检测缺乏潜台词密度"""
        dialogue_lines = re.findall(r'["""][^""""]{5,80}["""]', text)
        dialogue_lines += re.findall(r"'[^']{5,80}'", text)

        if len(dialogue_lines) < 3:
            return True, 5

        subtext_indicators = [
            r'(?:其实|实际上|说白了|意思是|暗示|暗指)',
            r'(?:话里有话|弦外之音|言外之意)',
            r'(?:表面.*?实际|嘴上.*?心里|说着.*?想着)',
        ]
        subtext_count = sum(
            1 for line in dialogue_lines
            for pat in subtext_indicators
            if re.search(pat, line)
        )

        ratio = subtext_count / len(dialogue_lines)
        if ratio < 0.2:
            return True, 5
        if ratio < 0.4:
            return True, 5
        return False, 0

    def check_zhuque_lack_of_object_detail(self, text: str) -> Tuple[bool, int]:
        """朱雀-检测缺乏物件细节锚定"""
        object_patterns = [
            r'(?:缺口|磨损|泛黄|褪色|生锈|裂缝|补丁).{0,5}(?:茶杯|戒指|照片|衣服|鞋|表|书|信|刀|剑)',
            r'(?:缺了|少了|掉了|断了|碎了|裂了).{0,5}(?:口|角|块|根|条|片)',
            r'(?:第[一二三四五六七八九十\d]+[个根次条把张只件])',
            r'(?:刻着|写着|画着|印着|绣着).{2,10}(?:字|名|日期|图案|花纹)',
        ]
        found = sum(1 for p in object_patterns if re.search(p, text))
        text_len_k = len(text) / 1000 if len(text) > 0 else 1
        density = found / text_len_k

        if density < 0.5:
            return True, 5
        if density < 1.0:
            return True, 4
        return False, 0

    def check_zhuque_uniform_paragraph_rhythm(self, text: str) -> Tuple[bool, int]:
        """朱雀-检测段落节奏均匀"""
        paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
        if len(paragraphs) < 5:
            return False, 0

        lengths = [len(p) for p in paragraphs]
        avg_len = sum(lengths) / len(lengths)
        variance = sum((l - avg_len) ** 2 for l in lengths) / len(lengths)
        std_dev = variance ** 0.5

        if std_dev < avg_len * 0.3:
            return True, 5
        if std_dev < avg_len * 0.5:
            return True, 5
        if std_dev < avg_len * 0.7:
            return True, 4
        return False, 0

    def check_zhuque_lack_of_surprise_twist(self, text: str) -> Tuple[bool, int]:
        """朱雀-检测缺乏意外转折"""
        surprise_patterns = [
            r'(?:突然|忽然|猛地|骤然|陡然|蓦地)',
            r'(?:没想到|想不到|没料到|出乎意料|意料之外)',
            r'(?:居然|竟然|居|竟)',
            r'(?:谁知|哪知|怎料|岂料|不料)',
            r'(?:反转|逆转|翻盘|逆袭|翻车)',
        ]
        found = sum(1 for p in surprise_patterns if re.search(p, text))
        text_len_k = len(text) / 1000 if len(text) > 0 else 1
        density = found / text_len_k

        if density < 1:
            return True, 5
        if density < 2:
            return True, 5
        if density < 3:
            return True, 3
        return False, 0

    def check_zhuque_sensory_imbalance(self, text: str) -> Tuple[bool, int]:
        """朱雀-检测感官不平衡"""
        visual = len(re.findall(
            r'(?:看|见|望|观|瞧|瞅|盯|瞪|瞟|瞥|视|'
            r'光|色|彩|亮|暗|明|黑|白|红|蓝|绿|黄)',
            text
        ))
        auditory = len(re.findall(
            r'(?:听|闻|声|音|响|鸣|叫|喊|吼|说|唱|'
            r'静|吵|闹|噪|嗡|轰|啪|咚|哗|滴)',
            text
        ))
        olfactory = len(re.findall(
            r'(?:闻|嗅|香|臭|味|气|腥|骚|酸|甜|苦|辣|'
            r'烟|雾|蒸|熏|呛|刺鼻)',
            text
        ))
        tactile = len(re.findall(
            r'(?:摸|碰|触|按|压|捏|掐|抓|握|攥|'
            r'冷|热|暖|凉|冰|烫|温|湿|干|滑|糙|硬|软)',
            text
        ))

        total = visual + auditory + olfactory + tactile
        if total == 0:
            return False, 0

        visual_ratio = visual / total
        if visual_ratio > 0.7:
            return True, 5
        if visual_ratio > 0.6:
            return True, 4
        return False, 0

    def polish(self, text: str, level: PolishLevel = PolishLevel.MEDIUM,
               style: WritingStyle = WritingStyle.WEB_NOVEL,
               preserve_terms: List[str] = None) -> PolishResult:
        """智能润色主入口"""
        start_time = time.time()

        ai_trace_before = self.detect_ai_traces(text)
        quality_before = self._assess_quality_local(text)

        polished = self._ai_polish(text, level, style, preserve_terms)

        polished = self._post_humanize(polished)

        ai_trace_after = self.detect_ai_traces(polished)
        quality_after = self._assess_quality_local(polished)

        changes = self._generate_diff(text, polished)

        return PolishResult(
            original=text,
            polished=polished,
            level=level.value[0],
            style=style.value[0],
            changes=changes,
            ai_trace_before=ai_trace_before["total_score"],
            ai_trace_after=ai_trace_after["total_score"],
            quality_before=quality_before,
            quality_after=quality_after,
            processing_time=round(time.time() - start_time, 1),
            word_count_change=(len(text), len(polished)),
        )

    def _post_humanize(self, text: str) -> str:
        """
        后处理人类化层 — 在AI改写后做规则层面的自然化
        原则：只做安全的、不会引入新AI痕迹的变换
        """
        result = text

        sentences = re.split(r'(?<=[。！？])', result)
        if len(sentences) > 6:
            new_sentences = []
            for i, s in enumerate(sentences):
                new_sentences.append(s)
                if (i >= 2 and len(s) > 30
                        and random.random() < 0.12
                        and not s.rstrip().endswith('？')
                        and not s.rstrip().endswith('！')):
                    new_sentences.append("……")
            result = ''.join(new_sentences)

        paras = result.split('\n\n')
        if len(paras) >= 5:
            lengths = [len(p) for p in paras]
            avg_len = sum(lengths) / len(lengths)
            new_paras = []
            for para in paras:
                if len(para) > avg_len * 2.2 and random.random() < 0.35:
                    mid = len(para) // 2
                    split_point = para.rfind('。', mid - 60, mid + 60)
                    if split_point == -1:
                        split_point = para.find('。', mid)
                        if split_point == -1:
                            split_point = mid
                    split_point += 1
                    new_paras.append(para[:split_point].strip())
                    new_paras.append(para[split_point:].strip())
                else:
                    new_paras.append(para)
            result = '\n\n'.join(new_paras)

        return result

    def _ai_polish(self, text: str, level: PolishLevel,
                   style: WritingStyle,
                   preserve_terms: List[str] = None) -> str:
        """调用DeepSeek API进行智能润色（few-shot示例驱动 + 高温度创造性）"""

        preserve_instruction = ""
        if preserve_terms:
            preserve_instruction = (
                f"\n【必须保留的术语/名称】\n{', '.join(preserve_terms)}\n"
                f"以上词汇绝对不能修改或替换。"
            )

        level_map = {
            PolishLevel.LIGHT: ("轻度润色", "仅优化通顺度，不改变句式结构"),
            PolishLevel.MEDIUM: ("中度改写", "调整句式，丰富词汇，打破模板化"),
            PolishLevel.DEEP: ("深度重构", "语义级重构，打散AI句式，注入人类特征"),
            PolishLevel.CREATIVE: ("创意重写", "保留核心情节，完全重组语言和结构"),
        }
        level_name, level_desc = level_map[level]

        system_prompt = f"""你是一位拥有15年写作经验的顶级网文作家。你的任务是将文本改写为自然的人类写作风格，让AI检测器无法识别。

核心原则：
1. 句长必须有剧烈变化 — 短句3-5字，长句30-50字，交替出现
2. 用动作和感官替代形容词 — 不写"他愤怒"，写"他一拳砸在桌上，茶杯跳了起来"
3. 每段至少1处意外用词 — 打破读者的预期
4. 对话要有潜台词 — 说A意思是B
5. 章末留白 — 不说完，卡在临界点
6. 保留轻微不完美 — 口语词、思考停顿、省略号

只输出改写后的文本，不要任何解释。"""

        few_shot_examples = """
【Few-Shot 示例 — 学习这种改写方式】

示例1：
❌ AI痕迹版：
"林晨缓缓地站起身，心中不禁激动万分。眼前的景象十分壮观，格外震撼人心。他微微一笑，心中暗想，自己的努力终究没有白费。"

✅ 人类改写版：
"林晨站起来。
腿有点麻。
眼前的景象让他愣了两秒——操，这他妈是真的？嘴角扯了一下，没笑出来。三年。值了。"

示例2：
❌ AI痕迹版：
"夜色深沉，月光如水般洒在大地上。叶青云站在山巅，俯瞰着脚下的万家灯火，心中涌起一股难以言喻的豪情。他知道，从今天起，一切都将不同。"

✅ 人类改写版：
"月亮被云吃了半口。
叶青云蹲在山顶那块歪脖子石头上，嘴里叼着根草茎。山下灯火像撒了一地的碎金子。他吐掉草茎，站起来。
风灌进袖子，凉飕飕的。
'开始了。'
他没说出口，但手指已经攥紧了剑柄。"

示例3：
❌ AI痕迹版：
"通过不断的修炼和实战，他的实力得到了显著提升。这不仅体现在修为境界的突破上，更重要的是他对武道的理解达到了一个全新的高度。"

✅ 人类改写版：
"打了三个月，死了七次——当然，是差点死了七次。
现在他出拳的时候，能听见骨头缝里噼里啪啦响，像炒豆子。师父说这叫'通窍'。他不关心叫什么，他只知道，下次再遇到那条黑蛇，他能把蛇头拧下来当球踢。"
"""

        prompt = f"""任务：{level_name} — {level_desc}
目标风格：{style.value[0]} — {style.value[1]}
{preserve_instruction}

{few_shot_examples}

请用以上示例中的改写方式处理以下文本。记住：
- 句长剧烈变化（3字短句 ↔ 50字长句交替）
- 用动作替代形容词（show, don't tell）
- 每段至少1处意外用词
- 对话有潜台词
- 保留轻微不完美

只输出改写后的完整文本，不要任何解释说明，不要用markdown代码块包裹。

原文：
{text}"""

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
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt},
                    ],
                    "temperature": 0.95,
                    "max_tokens": 16000,
                },
                timeout=300,
            )
            resp.raise_for_status()
            content = resp.json()["choices"][0]["message"]["content"]
            content = re.sub(r'```.*?\n|```', '', content).strip()
            return content
        except Exception as e:
            print(f"   [FAIL] AI润色失败: {e}")
            return text

    def _assess_quality_local(self, text: str) -> float:
        """本地快速质量评估"""
        score = 50.0

        if len(text) >= 4000:
            score += 15
        elif len(text) >= 2000:
            score += 8
        elif len(text) >= 500:
            score += 3

        paragraphs = [p for p in text.split('\n\n') if p.strip()]
        if len(paragraphs) >= 8:
            score += 10
        elif len(paragraphs) >= 4:
            score += 5

        sentences = re.split(r'[。！？]', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 3]
        if sentences:
            avg_len = sum(len(s) for s in sentences) / len(sentences)
            if 15 <= avg_len <= 45:
                score += 10
            elif 10 <= avg_len <= 60:
                score += 5

        dialogue_count = len(re.findall(r'["""][^""""]+["""]', text))
        dialogue_count += len(re.findall(r"'[^']+'", text))
        if dialogue_count >= 5:
            score += 10
        elif dialogue_count >= 2:
            score += 5

        unique_chars = len(set(text))
        if unique_chars >= 500:
            score += 10
        elif unique_chars >= 200:
            score += 5

        return min(score, 100)

    def _generate_diff(self, original: str, polished: str) -> List[Dict[str, str]]:
        """生成改写对照"""
        changes = []
        orig_sentences = re.split(r'(?<=[。！？])', original)
        pol_sentences = re.split(r'(?<=[。！？])', polished)

        for i, (o, p) in enumerate(zip(orig_sentences, pol_sentences)):
            o = o.strip()
            p = p.strip()
            if o and p and o != p and len(o) > 5:
                changes.append({
                    "position": f"第{i + 1}句",
                    "before": o[:100],
                    "after": p[:100],
                })

        return changes[:10]

    def pipeline_polish(self, text: str, style: WritingStyle = WritingStyle.WEB_NOVEL,
                        target_ai_score: float = 20.0,
                        preserve_terms: List[str] = None) -> PolishResult:
        """流水线润色 - 自动选择处理级别直到达标"""
        current_text = text
        last_result = None

        levels = [PolishLevel.LIGHT, PolishLevel.MEDIUM, PolishLevel.DEEP]

        for level in levels:
            traces = self.detect_ai_traces(current_text)
            if traces["total_score"] <= target_ai_score:
                break

            result = self.polish(current_text, level, style, preserve_terms)
            current_text = result.polished
            last_result = result

        if last_result is None:
            last_result = self.polish(text, PolishLevel.LIGHT, style, preserve_terms)

        return last_result

    def format_polish_report(self, result: PolishResult) -> str:
        """格式化润色报告"""
        report = []
        report.append("=" * 60)
        report.append("[AI智能润色报告]")
        report.append("=" * 60)
        report.append(f"  处理级别: {result.level}")
        report.append(f"  目标风格: {result.style}")
        report.append(f"  处理耗时: {result.processing_time}秒")
        report.append(f"  字数变化: {result.word_count_change[0]} -> {result.word_count_change[1]}")
        report.append(f"  AI痕迹: {result.ai_trace_before:.0f} -> {result.ai_trace_after:.0f}")
        report.append(f"  质量评分: {result.quality_before:.0f} -> {result.quality_after:.0f}")

        if result.changes:
            report.append(f"\n  主要修改 ({len(result.changes)}处):")
            for i, change in enumerate(result.changes[:5], 1):
                report.append(f"\n  {i}. {change['position']}")
                report.append(f"     [OLD] {change['before'][:80]}")
                report.append(f"     [NEW] {change['after'][:80]}")

        return "\n".join(report)


def get_polisher() -> AIPolisher:
    """获取润色器单例"""
    if not hasattr(get_polisher, "_instance"):
        get_polisher._instance = AIPolisher()
    return get_polisher._instance


if __name__ == "__main__":
    print("=" * 60)
    print("AIPolisher 独立测试")
    print("=" * 60)

    polisher = AIPolisher()

    test_text = """值得注意的是，随着修仙世界的不断发展，林晨在修炼过程中呈现出显著的进步态势。
    通过不断的努力和坚持，他不仅提升了修为，而且增强了战斗能力。
    首先，他的灵力储备大幅增加。其次，他的战斗技巧日益精进。
    总的来说，林晨已经具备了挑战更高境界的实力，这具有重要的意义。
    他感到非常兴奋，觉得自己的努力没有白费。"""

    print("\n=== AI痕迹检测 ===")
    traces = polisher.detect_ai_traces(test_text)
    print(f"  AI痕迹总分: {traces['total_score']}/{traces['max_score']}")
    print(f"  等级: {traces['level']}")
    print(f"  高危特征: {traces['high_severity_count']}个")
    print(f"  发现模式:")
    for p in traces["patterns_found"]:
        print(f"    - {p['name']} ({p['severity']}): {p['count']}处, +{p['score']}分")

    print("\n=== 智能润色 ===")
    result = polisher.polish(test_text, PolishLevel.MEDIUM, WritingStyle.WEB_NOVEL)
    print(polisher.format_polish_report(result))
    print(f"\n润色后文本:\n{result.polished[:300]}...")
