"""
NWACS 智能AI痕迹检测与人性化处理引擎
基于业界最佳实践的AI写作痕迹检测标准深度优化
涵盖42种AI写作模式检测，分为内容/语言/风格/交流/翻译腔五大类
整合翻译腔修正 + 中文特有AI模式检测
"""

import re
from typing import Dict, List, Tuple, Optional

AI_VOCABULARY = [
    "此外", "至关重要", "深入探讨", "强调", "持久的", "增强", "培养", "获得",
    "突出", "相互作用", "复杂", "复杂性", "格局", "关键性的", "展示",
    "织锦", "证明", "宝贵的", "充满活力的", "彰显", "凸显", "标志着",
    "见证了", "作为……的证明", "作为……的体现", "奠定了……基础",
    "不断演变的", "关键转折点", "不可磨灭的印记", "深深植根于",
    "无缝", "直观", "强大的", "革命性的", "开创性的",
]

EXAGGERATED_SIGNIFICANCE = [
    "作为", "充当", "标志着", "见证了", "是……的体现", "是……的证明",
    "是……的提醒", "极其重要的", "至关重要的", "核心的", "关键性的作用",
    "关键性的时刻", "凸显了其重要性", "强调了其意义", "反映了更广泛的",
    "象征着其持续的", "永恒的", "持久的", "为……做出贡献", "为……奠定基础",
    "标志着……塑造着", "代表着一个转变", "标志着一个转变", "关键转折点",
    "不断演变的格局", "焦点", "不可磨灭的印记", "深深植根于",
]

PROMOTIONAL_LANGUAGE = [
    "拥有（夸张用法）", "充满活力的", "丰富的（比喻）", "深刻的",
    "增强其", "展示", "体现", "致力于", "自然之美", "坐落于",
    "位于……的中心", "开创性的（比喻）", "著名的", "令人叹为观止的",
    "必游之地", "迷人的",
]

VAGUE_ATTRIBUTION = [
    "行业报告显示", "观察者指出", "专家认为", "一些批评者认为",
    "多个来源", "多个出版物", "据称", "据悉", "据了解",
]

FILLER_PHRASES = [
    ("为了实现这一目标", "为了实现"),
    ("由于……的事实", "因为"),
    ("在这个时间点", "现在"),
    ("在您需要帮助的情况下", "如果您需要帮助"),
    ("具有处理的能力", "可以处理"),
    ("值得注意的是……", ""),
    ("需要指出的是", ""),
    ("众所周知", ""),
    ("不言而喻", ""),
]

NEGATIVE_PARALLELISM = [
    r"不仅……而且……",
    r"这不仅仅是关于……，而是……",
    r"不单单是……，更是……",
    r"不只是……，还是……",
]

RULE_OF_THREE_PATTERN = re.compile(
    r"([^，。；]+)、([^，。；]+)和([^，。；]+(?:的)?(?:体验|感受|能力|格局|趋势|创新|突破|发展|进步|成就))"
)

DASH_OVERUSE_PATTERN = re.compile(r"——")

COLLABORATIVE_TRACES = [
    "希望这对您有帮助", "当然！", "一定！", "您说得完全正确！",
    "您想要……", "请告诉我", "这是一个……", "让我来……",
    "好的，我来", "没问题", "很高兴为您",
]

KNOWLEDGE_CUTOFF = [
    "截至", "根据我最后的训练更新", "虽然具体细节有限",
    "基于可用信息", "在现成资料中", "据我所知",
]

SYCOPHANTIC_TONE = [
    "好问题！", "您说得完全正确", "这是一个很好的观点",
    "非常棒的观察", "您提出了一个极好的问题",
]

GENERIC_POSITIVE_CONCLUSIONS = [
    "未来看起来光明", "激动人心的时代即将到来",
    "继续追求卓越的旅程", "向正确方向迈出的重要一步",
    "前景一片光明", "未来可期", "值得期待",
]

# ═══════════════════ 翻译腔检测模式 ═══════════════════
TRANSLATIONESE_PASSIVE = [
    r"被……所",
    r"为……所",
    r"受到……的",
    r"得到……的",
    r"遭到……的",
    r"被(?:人们|大家|众人)",
]

TRANSLATIONESE_CLAUSE = [
    (r"当.{2,15}时[，,]", "当...时句式"),
    (r"在.{2,15}之后[，,]", "在...之后句式"),
    (r"随着.{2,15}的.{2,10}", "随着...的...句式"),
    (r"对于.{2,15}来说", "对于...来说句式"),
    (r"关于.{2,15}的问题", "关于...的问题句式"),
]

TRANSLATIONESE_NOMINALIZATION = [
    (r"进行.{2,10}(?:处理|操作|分析|研究|调查|讨论|思考)", "进行+名词化"),
    (r"作出.{2,10}(?:决定|判断|选择|回应|反应|贡献)", "作出+名词化"),
    (r"加以.{2,10}(?:利用|控制|管理|保护|限制|规范)", "加以+名词化"),
    (r"给予.{2,10}(?:支持|帮助|关注|重视|回应)", "给予+名词化"),
    (r"产生.{2,10}(?:影响|作用|效果|变化|反应)", "产生+名词化"),
]

TRANSLATIONESE_ABSTRACT_SUBJECT = [
    r"(?:的|之)(?:发生|出现|存在|发展|变化|形成|产生|进行)",
]

TRANSLATIONESE_CONJUNCTION_PILE = [
    (r"(?:然而|但是|但|可是)[^。]{0,10}(?:因此|所以|于是|因而)", "转折+因果连用"),
    (r"(?:因为|由于)[^。]{0,10}(?:所以|因此|于是)", "因果连词堆砌"),
    (r"(?:虽然|尽管)[^。]{0,10}(?:但是|但|然而|可是)", "让步+转折连用"),
]

# ═══════════════════ 中文特有AI模式 ═══════════════════
EMOTION_LABEL_OVERUSE = [
    "不禁", "不由得", "忍不住", "情不自禁", "不由自主",
    "莫名", "没来由地", "鬼使神差地",
]

UNIVERSAL_ADJECTIVES = [
    "强大无比", "深不可测", "恐怖如斯", "神秘莫测",
    "美轮美奂", "气势磅礴", "惊天动地", "震古烁今",
    "前所未有", "匪夷所思", "不可思议",
]

CLICHE_ACTION = [
    "微微一笑", "嘴角上扬", "眼中闪过", "眸光一凝",
    "深吸一口气", "倒吸一口凉气", "瞳孔一缩",
    "心头一颤", "浑身一震", "脸色一变",
    "目光一凝", "神色一凛", "心中一沉",
]

DIALOGUE_TAG_SINGLE = [
    (r"(?:说道|问道|答道|喊道|叫道|吼道|怒道|笑道|哭道|叹道|冷道){3,}", "对话标签单一"),
]

TIME_TRANSITION_CLICHE = [
    "与此同时", "就在这时", "转眼间", "片刻之后",
    "不知过了多久", "时光飞逝", "日月如梭",
    "光阴似箭", "弹指一挥间",
]

OVER_EXPLANATION = [
    "也就是说", "换句话说", "这意味着", "换言之",
    "简单来说", "总而言之", "综上所述", "归根结底",
    "从某种意义上说", "严格来说",
]

SYMMETRIC_SENTENCE = [
    r"一边.{2,10}一边.{2,10}",
    r"既.{2,10}又.{2,10}",
    r"时而.{2,10}时而.{2,10}",
]

IDIOM_PILE = re.compile(r"(?:[\u4e00-\u9fff]{4}){3,}")

EXCLAMATION_OVERUSE = re.compile(r"！{2,}|!{2,}")

ELLIPSIS_OVERUSE = re.compile(r"……|\.{3,}")

DEGREE_ADVERB_PILE = [
    "非常", "极其", "十分", "特别", "格外",
    "异常", "无比", "绝顶", "万分",
]

INFO_DUMP_PATTERN = re.compile(r"[^。]{120,}")

EMPTY_DESCRIPTION = [
    r"一股.{2,8}(?:气息|力量|能量|波动|感觉)",
    r"一种.{2,8}(?:感觉|体验|氛围|气息)",
    r"充满了.{2,8}(?:气息|味道|感觉|氛围)",
]

FORCED_TENSION = [
    r"空气仿佛凝固",
    r"时间仿佛静止",
    r"气氛.{2,6}(?:紧张|凝重|压抑|诡异)",
    r"一股.{2,6}(?:寒意|杀意|威压|气势)",
]

PSEUDO_PROFOUND = [
    "命运的安排", "冥冥之中", "天意如此",
    "因果循环", "宿命的对决", "注定的相遇",
    "天道轮回", "命运齿轮",
]

REPETITIVE_STRUCTURE = re.compile(r"(.{10,30})\1")

SENTENCE_LENGTH_UNIFORM = re.compile(r"^[^。]{30,60}。[^。]{30,60}。[^。]{30,60}。", re.MULTILINE)

WEAK_VERB_CHAIN = [
    r"(?:看了看|想了想|说了说|走了走|看了看)",
    r"(?:看了一下|想了一下|说了一下)",
]

PASSIVE_VOICE_OVERUSE = re.compile(r"被.{2,10}(?:了|的|地|得)")

EMPTY_TRANSITION = [
    "话分两头", "花开两朵各表一枝", "暂且不提",
    "按下不表", "却说", "且说",
]

FORCED_PARALLEL = re.compile(r"(?:有人.{3,15}，有人.{3,15}，还有人.{3,15})")

NUMBER_PILE = re.compile(r"(?:一|两|三|四|五|六|七|八|九|十)(?:种|个|道|股|缕|丝|抹|片|阵)")

# ═══════════════════ NWACS 深度语言检测模式 ═══════════════════
LONG_PREMODIFIER = re.compile(r".{15,}的.{10,}的")

PRONOUN_OVERUSE_PATTERNS = [
    (r"他.{0,5}他.{0,5}他", "第三人称代词密集"),
    (r"她.{0,5}她.{0,5}她", "第三人称代词密集"),
    (r"它.{0,5}它.{0,5}它", "代词密集"),
]

TENSE_MARKER_OVERUSE = [
    ("了", "了"),
    ("着", "着"),
    ("过", "过"),
]

CATEGORY_WORD_REDUNDANCY = [
    "问题", "情况", "状态", "方面", "领域",
    "过程", "方式", "方法", "程度", "水平",
    "工作", "活动", "现象", "行为", "关系",
]

UNCLEAR_REFERENCE = re.compile(r"(?:这|那|其)(?:个|种|些|样|般)")

MISSING_SUBJECT = re.compile(r"^[。！？\n]*(?:在|从|对|把|被|让|给|向|跟|和|与|同|比|除了|关于|对于)[^。！？\n]{10,}[。！？]", re.MULTILINE)

MODIFIER_PILE_UP = re.compile(r"(?:的[^的]{2,10}){3,}")

FUNCTION_WORD_OVERUSE = [
    (r"的.{0,3}的.{0,3}的.{0,3}的", "「的」字密集"),
    (r"地.{0,3}地.{0,3}地", "「地」字密集"),
    (r"得.{0,3}得.{0,3}得", "「得」字密集"),
]

MIXED_REGISTER_PATTERNS = [
    (r"(?:吾|汝|尔|之乎者也|矣|焉|哉)", "文言词混入白话"),
    (r"(?:卧槽|牛逼|我靠|特么|尼玛|草|淦)", "粗俗词混入书面"),
]


def detect_ai_traces(text: str) -> Dict:
    """检测文本中的AI写作痕迹，返回详细的检测报告（51种模式）"""
    results = {
        "total_score": 0,
        "max_score": 100,
        "traces_found": [],
        "category_scores": {},
        "suggestions": [],
        "ai_probability": 0,
    }

    content_traces = _detect_content_patterns(text)
    language_traces = _detect_language_patterns(text)
    style_traces = _detect_style_patterns(text)
    communication_traces = _detect_communication_patterns(text)
    translationese_traces = _detect_translationese_patterns(text)
    chinese_ai_traces = _detect_chinese_ai_patterns(text)
    nwacs_style_traces = _detect_nwacs_style_patterns(text)

    all_traces = content_traces + language_traces + style_traces + communication_traces + translationese_traces + chinese_ai_traces + nwacs_style_traces

    results["traces_found"] = all_traces
    results["category_scores"] = {
        "content": max(0, 20 - len(content_traces) * 3),
        "language": max(0, 20 - len(language_traces) * 3),
        "style": max(0, 20 - len(style_traces) * 3),
        "communication": max(0, 20 - len(communication_traces) * 3),
        "translationese": max(0, 10 - len(translationese_traces) * 2),
        "chinese_ai": max(0, 10 - len(chinese_ai_traces) * 2),
        "nwacs_style": max(0, 10 - len(nwacs_style_traces) * 2),
    }

    total_deduction = len(all_traces) * 3
    results["total_score"] = max(0, 100 - total_deduction)
    results["ai_probability"] = min(95, len(all_traces) * 6)

    if len(all_traces) <= 2:
        results["level"] = "优秀"
        results["level_desc"] = "文本自然流畅，AI痕迹极少，接近人类写作水平"
    elif len(all_traces) <= 5:
        results["level"] = "良好"
        results["level_desc"] = "存在少量AI痕迹，建议微调个别表达"
    elif len(all_traces) <= 10:
        results["level"] = "一般"
        results["level_desc"] = "AI痕迹明显，需要重点修改多处表达"
    elif len(all_traces) <= 18:
        results["level"] = "较差"
        results["level_desc"] = "AI痕迹严重，建议大幅重写或使用去AI重写功能"
    else:
        results["level"] = "极差"
        results["level_desc"] = "高度疑似AI生成，强烈建议使用去AI重写功能全面修改"

    results["suggestions"] = _generate_suggestions(all_traces)

    return results


def _detect_content_patterns(text: str) -> List[Dict]:
    traces = []

    for phrase in EXAGGERATED_SIGNIFICANCE:
        if phrase in text:
            traces.append({
                "category": "content",
                "pattern": "过度强调意义",
                "found": phrase,
                "severity": "medium",
                "fix": "用具体事实替代抽象拔高，直接陈述发生了什么",
            })
            break

    for phrase in PROMOTIONAL_LANGUAGE:
        if phrase in text:
            traces.append({
                "category": "content",
                "pattern": "宣传式语言",
                "found": phrase,
                "severity": "medium",
                "fix": "用中性客观的描述替代夸张的形容词",
            })
            break

    for phrase in VAGUE_ATTRIBUTION:
        if phrase in text:
            traces.append({
                "category": "content",
                "pattern": "模糊归因",
                "found": phrase,
                "severity": "high",
                "fix": "提供具体的来源、数据或人物，而非模糊的权威",
            })
            break

    ing_patterns = [
        (r"突出了[^。]{4,20}(?:的重要性|的意义|的作用)", "肤浅分析"),
        (r"强调了[^。]{4,20}(?:的重要性|的意义|的作用)", "肤浅分析"),
        (r"彰显了[^。]{4,20}(?:的重要性|的意义|的作用)", "肤浅分析"),
        (r"确保了[^。]{4,20}(?:的|能够)", "肤浅分析"),
        (r"反映了[^。]{4,20}(?:的|与)", "肤浅分析"),
    ]
    for pat, name in ing_patterns:
        if re.search(pat, text):
            traces.append({
                "category": "content",
                "pattern": "肤浅分析句式",
                "found": re.search(pat, text).group(0)[:30] if re.search(pat, text) else pat,
                "severity": "low",
                "fix": "删除这些空洞的总结性短语，让事实自己说话",
            })
            break

    challenge_patterns = ["尽管……面临", "尽管存在这些挑战", "挑战与遗产", "未来展望"]
    for phrase in challenge_patterns:
        if phrase in text:
            traces.append({
                "category": "content",
                "pattern": "公式化挑战段落",
                "found": phrase,
                "severity": "medium",
                "fix": "将挑战具体化，用实际数据和事件替代模板化表述",
            })
            break

    return traces


def _detect_language_patterns(text: str) -> List[Dict]:
    traces = []

    vocab_count = 0
    found_vocab = []
    for word in AI_VOCABULARY:
        if word in text:
            vocab_count += 1
            found_vocab.append(word)
    if vocab_count >= 3:
        traces.append({
            "category": "language",
            "pattern": "AI高频词汇",
            "found": "、".join(found_vocab[:5]),
            "severity": "high",
            "fix": f"替换或删除这些AI高频词：{'、'.join(found_vocab[:5])}",
        })

    copula_patterns = [
        (r"作为[^，。]{2,15}(?:的|一个)", "系动词回避"),
        (r"拥有[^，。]{2,15}(?:的|一个)", "系动词回避"),
        (r"设有[^，。]{2,15}(?:的|一个)", "系动词回避"),
    ]
    for pat, name in copula_patterns:
        if re.search(pat, text):
            traces.append({
                "category": "language",
                "pattern": "系动词回避",
                "found": re.search(pat, text).group(0)[:30],
                "severity": "low",
                "fix": "用简单的「是」「有」替代复杂结构",
            })
            break

    for pat in NEGATIVE_PARALLELISM:
        if re.search(pat, text):
            traces.append({
                "category": "language",
                "pattern": "否定式排比",
                "found": "不仅……而且……",
                "severity": "medium",
                "fix": "直接陈述事实，删除「不仅……而且……」结构",
            })
            break

    if RULE_OF_THREE_PATTERN.search(text):
        m = RULE_OF_THREE_PATTERN.search(text)
        traces.append({
            "category": "language",
            "pattern": "三段式法则",
            "found": m.group(0)[:40],
            "severity": "low",
            "fix": "改为两项或四项，打破机械的三段式结构",
        })

    synonym_pattern = re.compile(r"([^。]{5,15})(?:面临|遭遇|碰到|遇到)([^。]{5,15})")
    matches = synonym_pattern.findall(text)
    if len(matches) >= 2:
        traces.append({
            "category": "language",
            "pattern": "刻意换词",
            "found": f"多处同义词替换",
            "severity": "low",
            "fix": "保持用词一致性，不要刻意替换同义词",
        })

    return traces


def _detect_style_patterns(text: str) -> List[Dict]:
    traces = []

    dashes = DASH_OVERUSE_PATTERN.findall(text)
    if len(dashes) >= 3:
        traces.append({
            "category": "style",
            "pattern": "破折号过度使用",
            "found": f"共{len(dashes)}处破折号",
            "severity": "medium",
            "fix": "将破折号替换为逗号或句号，或重新组织句子",
        })

    emoji_pattern = re.compile(r"[\U0001F300-\U0001F9FF\u2600-\u27BF\u2B50\u2705\u274C\u2753\u2757\u2795-\u2797\u2728\u26A0\u26A1\u267B\u2615\u2696\u270F\u23F0\u231B]")
    emojis = emoji_pattern.findall(text)
    if emojis:
        traces.append({
            "category": "style",
            "pattern": "表情符号",
            "found": f"共{len(emojis)}个表情符号",
            "severity": "low",
            "fix": "在正式写作中删除表情符号，用文字表达情感",
        })

    bold_list_pattern = re.compile(r"(?:- |• |\d+\.)\s*\*\*[^*]+\*\*[：:]")
    if bold_list_pattern.search(text):
        traces.append({
            "category": "style",
            "pattern": "内联标题列表",
            "found": "粗体标题+冒号的列表格式",
            "severity": "low",
            "fix": "将列表改写为自然段落",
        })

    return traces


def _detect_communication_patterns(text: str) -> List[Dict]:
    traces = []

    for phrase in COLLABORATIVE_TRACES:
        if phrase in text:
            traces.append({
                "category": "communication",
                "pattern": "协作交流痕迹",
                "found": phrase,
                "severity": "high",
                "fix": "删除所有对话式、客服式的语句",
            })
            break

    for phrase in KNOWLEDGE_CUTOFF:
        if phrase in text:
            traces.append({
                "category": "communication",
                "pattern": "知识截止声明",
                "found": phrase,
                "severity": "medium",
                "fix": "删除免责声明，直接陈述已知信息",
            })
            break

    for phrase in SYCOPHANTIC_TONE:
        if phrase in text:
            traces.append({
                "category": "communication",
                "pattern": "谄媚语气",
                "found": phrase,
                "severity": "medium",
                "fix": "保持专业中立的语气",
            })
            break

    for phrase in GENERIC_POSITIVE_CONCLUSIONS:
        if phrase in text:
            traces.append({
                "category": "communication",
                "pattern": "通用积极结论",
                "found": phrase,
                "severity": "medium",
                "fix": "用具体的后续计划或数据替代空洞的乐观结尾",
            })
            break

    filler_count = 0
    for orig, _ in FILLER_PHRASES:
        if orig in text:
            filler_count += 1
    if filler_count >= 2:
        traces.append({
            "category": "communication",
            "pattern": "填充短语",
            "found": f"共{filler_count}处填充短语",
            "severity": "low",
            "fix": "删除冗余的填充词，让表达更简洁",
        })

    return traces


def _detect_translationese_patterns(text: str) -> List[Dict]:
    """检测翻译腔模式"""
    traces = []

    for pat in TRANSLATIONESE_PASSIVE:
        if re.search(pat, text):
            m = re.search(pat, text)
            traces.append({
                "category": "translationese",
                "pattern": "西式被动语态",
                "found": m.group(0)[:30],
                "severity": "medium",
                "fix": "改为主动语态，用「有人」「人们」或直接省略被动主语",
            })
            break

    for pat, name in TRANSLATIONESE_CLAUSE:
        if re.search(pat, text):
            m = re.search(pat, text)
            traces.append({
                "category": "translationese",
                "pattern": f"西式从句: {name}",
                "found": m.group(0)[:30],
                "severity": "low",
                "fix": "拆分为短句，或改为中文习惯的流水句",
            })
            break

    for pat, name in TRANSLATIONESE_NOMINALIZATION:
        if re.search(pat, text):
            m = re.search(pat, text)
            traces.append({
                "category": "translationese",
                "pattern": f"名词化弱动词: {name}",
                "found": m.group(0)[:30],
                "severity": "medium",
                "fix": "直接用动词替代「进行/作出/加以+名词」结构",
            })
            break

    for pat in TRANSLATIONESE_ABSTRACT_SUBJECT:
        if re.search(pat, text):
            m = re.search(pat, text)
            traces.append({
                "category": "translationese",
                "pattern": "抽象名词主语",
                "found": m.group(0)[:30],
                "severity": "low",
                "fix": "用具体的人或事物作主语，避免「XX的发生/出现」",
            })
            break

    for pat, name in TRANSLATIONESE_CONJUNCTION_PILE:
        if re.search(pat, text):
            m = re.search(pat, text)
            traces.append({
                "category": "translationese",
                "pattern": f"连接词堆砌: {name}",
                "found": m.group(0)[:30],
                "severity": "medium",
                "fix": "中文靠语序表达逻辑，删除多余的连接词",
            })
            break

    return traces


def _detect_chinese_ai_patterns(text: str) -> List[Dict]:
    """检测中文特有的AI写作模式"""
    traces = []

    emotion_count = sum(1 for w in EMOTION_LABEL_OVERUSE if w in text)
    if emotion_count >= 2:
        found_words = [w for w in EMOTION_LABEL_OVERUSE if w in text]
        traces.append({
            "category": "chinese_ai",
            "pattern": "情感标签过度",
            "found": "、".join(found_words[:3]),
            "severity": "medium",
            "fix": "用行为和对话展示情感，而非直接贴标签",
        })

    adj_count = sum(1 for w in UNIVERSAL_ADJECTIVES if w in text)
    if adj_count >= 2:
        found_adj = [w for w in UNIVERSAL_ADJECTIVES if w in text]
        traces.append({
            "category": "chinese_ai",
            "pattern": "万能形容词堆砌",
            "found": "、".join(found_adj[:3]),
            "severity": "high",
            "fix": "用具体的感官细节替代空洞的形容词",
        })

    cliche_count = sum(1 for w in CLICHE_ACTION if w in text)
    if cliche_count >= 2:
        found_cliche = [w for w in CLICHE_ACTION if w in text]
        traces.append({
            "category": "chinese_ai",
            "pattern": "套路化动作描写",
            "found": "、".join(found_cliche[:3]),
            "severity": "high",
            "fix": "设计独特的动作细节，避免「微微一笑」「眼中闪过」等套路",
        })

    for pat, name in DIALOGUE_TAG_SINGLE:
        matches = re.findall(pat, text)
        if len(matches) >= 3:
            traces.append({
                "category": "chinese_ai",
                "pattern": name,
                "found": f"共{len(matches)}处单一对话标签",
                "severity": "medium",
                "fix": "用动作、神态、环境替代「XX道」，或直接省略对话标签",
            })
            break

    time_count = sum(1 for w in TIME_TRANSITION_CLICHE if w in text)
    if time_count >= 2:
        found_time = [w for w in TIME_TRANSITION_CLICHE if w in text]
        traces.append({
            "category": "chinese_ai",
            "pattern": "套路化时间过渡",
            "found": "、".join(found_time[:3]),
            "severity": "low",
            "fix": "用具体事件或场景切换替代「与此同时」「转眼间」",
        })

    explain_count = sum(1 for w in OVER_EXPLANATION if w in text)
    if explain_count >= 2:
        found_explain = [w for w in OVER_EXPLANATION if w in text]
        traces.append({
            "category": "chinese_ai",
            "pattern": "过度解释",
            "found": "、".join(found_explain[:3]),
            "severity": "medium",
            "fix": "信任读者理解力，删除「也就是说」「这意味着」等解释性短语",
        })

    for pat in SYMMETRIC_SENTENCE:
        if re.search(pat, text):
            m = re.search(pat, text)
            traces.append({
                "category": "chinese_ai",
                "pattern": "对称句式",
                "found": m.group(0)[:30],
                "severity": "low",
                "fix": "打破对称结构，让句子长度和节奏自然变化",
            })
            break

    idiom_matches = IDIOM_PILE.findall(text)
    if len(idiom_matches) >= 4:
        traces.append({
            "category": "chinese_ai",
            "pattern": "成语堆砌",
            "found": f"共{len(idiom_matches)}处连续四字词",
            "severity": "medium",
            "fix": "减少成语密度，用具体描写替代概括性成语",
        })

    excl_matches = EXCLAMATION_OVERUSE.findall(text)
    if len(excl_matches) >= 3:
        traces.append({
            "category": "chinese_ai",
            "pattern": "感叹号滥用",
            "found": f"共{len(excl_matches)}处连续感叹号",
            "severity": "low",
            "fix": "用文字本身的力量传达情感，减少感叹号依赖",
        })

    ellipsis_matches = ELLIPSIS_OVERUSE.findall(text)
    if len(ellipsis_matches) >= 5:
        traces.append({
            "category": "chinese_ai",
            "pattern": "省略号滥用",
            "found": f"共{len(ellipsis_matches)}处省略号",
            "severity": "low",
            "fix": "用具体描写替代省略号，让留白更有力量",
        })

    degree_count = sum(1 for w in DEGREE_ADVERB_PILE if w in text)
    if degree_count >= 3:
        found_degree = [w for w in DEGREE_ADVERB_PILE if w in text]
        traces.append({
            "category": "chinese_ai",
            "pattern": "程度副词堆砌",
            "found": "、".join(found_degree[:3]),
            "severity": "low",
            "fix": "删除「非常」「极其」等程度副词，用具体描写展示程度",
        })

    info_dumps = INFO_DUMP_PATTERN.findall(text)
    if len(info_dumps) >= 3:
        traces.append({
            "category": "chinese_ai",
            "pattern": "信息密度不均",
            "found": f"共{len(info_dumps)}处超长句子(>120字)",
            "severity": "medium",
            "fix": "将长句拆分为短句群，控制信息释放节奏",
        })

    for pat in EMPTY_DESCRIPTION:
        if re.search(pat, text):
            m = re.search(pat, text)
            traces.append({
                "category": "chinese_ai",
                "pattern": "空洞氛围描写",
                "found": m.group(0)[:30],
                "severity": "medium",
                "fix": "用具体的感官细节替代「一股XX气息」等空洞描写",
            })
            break

    for pat in FORCED_TENSION:
        if re.search(pat, text):
            m = re.search(pat, text)
            traces.append({
                "category": "chinese_ai",
                "pattern": "强行制造紧张感",
                "found": m.group(0)[:30],
                "severity": "medium",
                "fix": "通过情节和人物反应自然营造紧张，而非直接描述气氛",
            })
            break

    pseudo_count = sum(1 for w in PSEUDO_PROFOUND if w in text)
    if pseudo_count >= 2:
        found_pseudo = [w for w in PSEUDO_PROFOUND if w in text]
        traces.append({
            "category": "chinese_ai",
            "pattern": "伪深刻表述",
            "found": "、".join(found_pseudo[:3]),
            "severity": "medium",
            "fix": "用具体的情节因果替代「命运的安排」「冥冥之中」等空洞表述",
        })

    repetitive = REPETITIVE_STRUCTURE.findall(text)
    if len(repetitive) >= 2:
        traces.append({
            "category": "chinese_ai",
            "pattern": "重复句式结构",
            "found": f"共{len(repetitive)}处重复结构",
            "severity": "low",
            "fix": "变化句式结构，避免同一模式反复出现",
        })

    if SENTENCE_LENGTH_UNIFORM.search(text):
        traces.append({
            "category": "chinese_ai",
            "pattern": "句子长度均匀",
            "found": "连续多句长度相近",
            "severity": "low",
            "fix": "混合长短句，创造节奏变化",
        })

    for pat in WEAK_VERB_CHAIN:
        if re.search(pat, text):
            traces.append({
                "category": "chinese_ai",
                "pattern": "弱动词链",
                "found": "看了看/想了想等弱动词重复",
                "severity": "low",
                "fix": "用精准的单一动词替代弱动词重复",
            })
            break

    passive_count = len(PASSIVE_VOICE_OVERUSE.findall(text))
    if passive_count >= 4:
        traces.append({
            "category": "chinese_ai",
            "pattern": "被动语态过度",
            "found": f"共{passive_count}处「被」字句",
            "severity": "medium",
            "fix": "将被动句改为主动句，中文习惯主动表达",
        })

    empty_trans_count = sum(1 for w in EMPTY_TRANSITION if w in text)
    if empty_trans_count >= 1:
        found_trans = [w for w in EMPTY_TRANSITION if w in text]
        traces.append({
            "category": "chinese_ai",
            "pattern": "说书人过渡语",
            "found": "、".join(found_trans),
            "severity": "low",
            "fix": "用场景切换或时间跳跃自然过渡，避免「话分两头」等传统套话",
        })

    if FORCED_PARALLEL.search(text):
        m = FORCED_PARALLEL.search(text)
        traces.append({
            "category": "chinese_ai",
            "pattern": "强行排比",
            "found": m.group(0)[:40],
            "severity": "low",
            "fix": "排比应自然产生于内容需要，而非刻意制造",
        })

    number_matches = NUMBER_PILE.findall(text)
    if len(number_matches) >= 6:
        traces.append({
            "category": "chinese_ai",
            "pattern": "数量词堆砌",
            "found": f"共{len(number_matches)}处数量词",
            "severity": "low",
            "fix": "减少「一种」「一股」「一道」等数量词的使用频率",
        })

    return traces


def _detect_nwacs_style_patterns(text: str) -> List[Dict]:
    """检测NWACS深度语言特有的AI写作模式（长定语、代词过度、范畴词冗余等）"""
    traces = []

    long_premod = LONG_PREMODIFIER.findall(text)
    if len(long_premod) >= 2:
        traces.append({
            "category": "nwacs_style",
            "pattern": "长定语前置",
            "found": f"共{len(long_premod)}处长定语结构",
            "severity": "medium",
            "fix": "将长定语拆分为短句或后置，中文习惯短定语前置、长定语后置",
        })

    for pat, name in PRONOUN_OVERUSE_PATTERNS:
        matches = re.findall(pat, text)
        if len(matches) >= 3:
            traces.append({
                "category": "nwacs_style",
                "pattern": name,
                "found": f"共{len(matches)}处代词密集区",
                "severity": "medium",
                "fix": "用人名或具体称谓替代部分代词，避免连续使用同一代词",
            })
            break

    tense_counts = {}
    for marker, name in TENSE_MARKER_OVERUSE:
        count = text.count(marker)
        if count > len(text) * 0.04:
            tense_counts[name] = count
    if tense_counts:
        worst = max(tense_counts, key=tense_counts.get)
        traces.append({
            "category": "nwacs_style",
            "pattern": f"时态标记过度（「{worst}」字）",
            "found": f"「{worst}」出现{tense_counts[worst]}次，占比{tense_counts[worst]/len(text)*100:.1f}%",
            "severity": "low",
            "fix": "中文靠语序表达时态，减少「了」「着」「过」的使用频率",
        })

    category_count = sum(1 for w in CATEGORY_WORD_REDUNDANCY if w in text)
    if category_count >= 4:
        found_cat = [w for w in CATEGORY_WORD_REDUNDANCY if w in text]
        traces.append({
            "category": "nwacs_style",
            "pattern": "范畴词冗余",
            "found": "、".join(found_cat[:5]),
            "severity": "medium",
            "fix": "删除「问题」「情况」「状态」等不增加信息的范畴词",
        })

    unclear_refs = UNCLEAR_REFERENCE.findall(text)
    if len(unclear_refs) > len(text) * 0.015:
        traces.append({
            "category": "nwacs_style",
            "pattern": "指代不明",
            "found": f"共{len(unclear_refs)}处「这/那/其」指代",
            "severity": "medium",
            "fix": "明确指代对象，用具体名词替代「这」「那」「其」",
        })

    missing_subj = MISSING_SUBJECT.findall(text)
    if len(missing_subj) >= 2:
        traces.append({
            "category": "nwacs_style",
            "pattern": "主语缺失",
            "found": f"共{len(missing_subj)}句缺少主语",
            "severity": "high",
            "fix": "为每个句子补上明确的主语，中文虽可省略主语但不宜过多",
        })

    modifier_piles = MODIFIER_PILE_UP.findall(text)
    if len(modifier_piles) >= 2:
        traces.append({
            "category": "nwacs_style",
            "pattern": "修饰语堆砌",
            "found": f"共{len(modifier_piles)}处「的」字密集区",
            "severity": "medium",
            "fix": "拆分多层修饰语，每层「的」不超过2个",
        })

    for pat, name in FUNCTION_WORD_OVERUSE:
        matches = re.findall(pat, text)
        if len(matches) >= 3:
            traces.append({
                "category": "nwacs_style",
                "pattern": f"虚词过度（{name}）",
                "found": f"共{len(matches)}处虚词密集区",
                "severity": "low",
                "fix": "减少「的」「地」「得」的密度，用实词替代虚词结构",
            })
            break

    for pat, name in MIXED_REGISTER_PATTERNS:
        if re.search(pat, text):
            m = re.search(pat, text)
            traces.append({
                "category": "nwacs_style",
                "pattern": f"语体混杂（{name}）",
                "found": m.group(0)[:20],
                "severity": "low",
                "fix": "保持全文语体一致，避免文言与白话、粗俗与书面混杂",
            })
            break

    return traces


def _generate_suggestions(traces: List[Dict]) -> List[str]:
    suggestions = []
    categories = set(t["category"] for t in traces)

    if "content" in categories:
        suggestions.append("📝 内容层面：用具体事实替代抽象拔高，删除「标志着」「见证了」等夸大表述")
    if "language" in categories:
        suggestions.append("🔤 语言层面：替换AI高频词汇，打破三段式结构，简化句式")
    if "style" in categories:
        suggestions.append("🎨 风格层面：减少破折号使用，删除表情符号和格式化列表")
    if "communication" in categories:
        suggestions.append("💬 交流层面：删除客服式语句和空洞的乐观结尾")
    if "translationese" in categories:
        suggestions.append("🌐 翻译腔层面：改被动为主动，拆西式从句，用动词替代名词化结构")
    if "chinese_ai" in categories:
        suggestions.append("🀄 中文AI模式：减少套路化描写，用具体细节替代万能形容词和成语堆砌")
    if "nwacs_style" in categories:
        suggestions.append("🔬 深度语言检测：拆分长定语、明确指代、补全主语、删除范畴词冗余")

    suggestions.append("✨ 核心原则：直接陈述事实、变化句子节奏、信任读者理解力、注入真实个性")

    return suggestions


def build_humanize_prompt(text: str, detection_result: Dict) -> str:
    """构建人性化改写提示词"""
    traces = detection_result.get("traces_found", [])
    if not traces:
        return ""

    traces_desc = []
    for t in traces:
        traces_desc.append(f"- [{t['category']}] {t['pattern']}：发现「{t['found']}」→ {t['fix']}")

    prompt = f"""你是一位资深文字编辑，专门去除AI写作痕迹。请对以下文本进行人性化改写。

## 检测到的AI痕迹
{chr(10).join(traces_desc)}

## 改写铁律
1. **删除填充短语** - 去除开场白和强调性拐杖词
2. **打破公式结构** - 避免二元对比、戏剧性分段、修辞性设置
3. **变化节奏** - 混合句子长度。两项优于三项。段落结尾要多样化
4. **信任读者** - 直接陈述事实，跳过软化、辩解和手把手引导
5. **删除金句** - 如果听起来像可引用的语句，重写它
6. **注入灵魂** - 有观点、变化节奏、承认复杂性、适当使用第一人称

## 关键原则
- 用「是」「有」替代「作为」「拥有」等复杂结构
- 删除「此外」「至关重要」「深入探讨」等AI高频词
- 将破折号替换为逗号或句号
- 用具体细节替代模糊的「专家认为」「行业报告显示」
- 删除空洞的乐观结尾，用具体计划替代
- 拆分长定语，将「XX的XX的XX」改为短句群
- 明确指代，用具体名词替代模糊的「这」「那」「其」
- 补全主语，避免连续多句缺少主语
- 删除「问题」「情况」「状态」等不增加信息的范畴词
- 减少「了」「着」「过」的密度，中文靠语序表达时态

## 原文
{text}

## 输出要求
直接输出改写后的文本，不要包含任何说明、分析或元信息。保持原文的核心信息和情节不变，只改变表达方式。"""

    return prompt


def build_ai_detection_report_prompt(text: str) -> str:
    """构建AI痕迹检测报告提示词"""
    prompt = f"""你是一位专业的AI写作痕迹检测专家。请对以下文本进行全面的AI痕迹检测分析。

## 检测维度（基于NWACS六层智能检测标准）

### 第一层：词汇层检测
- AI高频词汇（此外、至关重要、深入探讨、强调、格局、织锦等）
- 机械连接词过度使用（首先/其次/最后/总而言之）
- 抽象名词堆砌（赋能/底层逻辑/闭环/维度/体系）
- 情感副词直述（他感到很愤怒/她非常悲伤）
- 万能形容词（强大无比/深不可测/恐怖如斯）
- 程度副词堆砌（非常/极其/十分/特别/格外）

### 第二层：句式层检测
- 否定式排比（不仅……而且……）
- 三段式法则过度使用
- 破折号过度使用
- 对话标签单一（说道/问道/喊道连续使用）
- 对称句式（一边……一边……/既……又……）
- 被动语态过度（被……所/为……所）
- 长定语前置（XX的XX的XX结构）

### 第三层：语义层检测
- 过度强调意义、遗产和更广泛的趋势
- 宣传和广告式语言
- 模糊归因和含糊措辞
- 刻意换词（同义词循环）
- 肤浅分析句式（突出了/强调了/彰显了）
- 伪深刻表达（命运的安排/冥冥之中/天道轮回）

### 第四层：结构层检测
- 公式化挑战段落
- 提纲式的"挑战与未来展望"部分
- 信息倾泻（单句超过120字）
- 时间过渡套路（与此同时/就在这时/转眼间）
- 过度解释（也就是说/换句话说/这意味着）
- 空泛描写（一股XX气息/一种XX感觉）

### 第五层：情感层检测
- 情感标签过度（不禁/不由得/忍不住/情不自禁）
- 强制紧张（空气仿佛凝固/时间仿佛静止）
- 通用积极结论（未来可期/前景光明）
- 表情符号过度使用
- 感叹号过度使用

### 第六层：语用层检测
- 协作交流痕迹（希望这对您有帮助/当然！）
- 知识截止日期免责声明
- 谄媚/卑躬屈膝的语气（好问题！/您说得完全正确）
- 填充短语（值得注意的是/需要指出的是）
- 翻译腔（当...时/在...之后/随着...的...）
- 语体混杂（文言与白话、粗俗与书面混杂）

### 深度语言检测（NWACS增强）
- 代词过度使用（他/她/它连续出现）
- 时态标记过度（了/着/过密度过高）
- 范畴词冗余（问题/情况/状态等空洞词）
- 指代不明（这/那/其无明确先行词）
- 主语缺失（连续多句无主语）
- 修饰语堆砌（多层「的」字结构）
- 虚词过度（的/地/得密度过高）
- 成语堆砌（连续多个四字成语）
- 数字堆砌（多种/多道/多股等量化词密集）

## 输出格式
请以JSON格式输出检测结果：
```json
{{
  "ai_score": 0-100的AI痕迹评分（越高越像AI写的）,
  "human_score": 0-100的人类写作评分,
  "level": "优秀/良好/一般/较差/极差",
  "issues": [
    {{"category": "词汇层/句式层/语义层/结构层/情感层/语用层", "pattern": "具体模式名", "description": "发现的具体问题", "severity": "critical/high/medium/low", "fix": "修改建议"}}
  ],
  "overall_suggestion": "总体修改建议"
}}
```

## 待检测文本
{text}"""

    return prompt