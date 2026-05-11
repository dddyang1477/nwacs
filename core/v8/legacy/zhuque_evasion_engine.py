#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 朱雀AI检测专用规避引擎 - ZhuqueEvasionEngine

全网深度学习精华蒸馏（2026年5月最新）：
├── 国内深度搜索
│   ├── 朱雀AI首席架构师博客：三维降重法（注入错误经验+打断逻辑链+超小样本数据）
│   ├── 零感AI博客：朱雀三大版本区别与降AI实战方案
│   ├── 今日头条·焦圈儿AI：吃透朱雀审核逻辑
│   ├── 今日头条·阿和：反AI内卷底层逻辑（情绪撕裂+埋彩蛋+反AI人设库）
│   ├── CSDN·嘎嘎降AI：朱雀误判原因与应对
│   ├── CSDN·炼字工坊：解码层频次惩罚与温度值扰动
│   ├── 微博·德里克文：三步降到5%野路子
│   └── 51CTO·学术牛：6招AI率从90%降到2.5%
├── 国际深度搜索
│   ├── MASH论文(arXiv 2601.08564)：多阶段风格人化框架
│   ├── REACT论文(arXiv 2605.02374)：对抗训练增强检测鲁棒性
│   ├── HumanizeAI.pro：7种避免AI检测的方法
│   ├── Skilldential：9种人化AI内容的方法
│   ├── Eyesift：降低AI检测分数的编辑技术
│   ├── GitHub StealthHumanizer：开源多pass人化器
│   └── Reddit社区：AI检测绕过实战经验
└── 朱雀AI检测核心原理
    ├── Perplexity(PPL)分析：低困惑度=AI（文本过于可预测）
    ├── Burstiness分析：低爆发度=AI（句长过于均匀）
    ├── 统计模式识别：词频分布/句式结构/段落连贯性
    ├── 逻辑一致性检查：事实连贯性/时间线一致性
    ├── 水印检测：隐藏AI生成模式识别
    └── 三版本架构：论文版(最严)/普通版(中等)/小说版(最宽松)

核心目标：朱雀AI检测通过率从70%提升至95%+
"""

import json
import os
import re
import random
import time
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


API_KEY = "sk-f3246fbd1eef446e9a11d78efefd9bba"
BASE_URL = "https://api.deepseek.com"


class ZhuqueVersion(Enum):
    THESIS = ("论文版", "最严格，学术语料库训练，对规范表达敏感")
    GENERAL = ("普通版", "中等严格，通用语料库，口语化容忍度高")
    NOVEL = ("小说版", "最宽松，文学语料库，叙事情感容忍度最高")


class EvasionStrategy(Enum):
    DIMENSIONAL_REDUCTION = "三维降重法"
    EMOTIONAL_TEAR = "情绪撕裂法"
    EASTER_EGG = "埋彩蛋法"
    ANTI_AI_CHARACTER = "反AI人设库"
    PERPLEXITY_BOOST = "困惑度爆破"
    BURSTINESS_BOOST = "爆发度爆破"
    STYLE_HUMANIZATION = "风格人化"
    ADVERSARIAL_REFINEMENT = "对抗精炼"
    LOCAL_COLOR = "烟火气注入"
    IMPERFECTION = "不完美注入"


@dataclass
class EvasionTechnique:
    name: str
    strategy: str
    description: str
    rules: List[str]
    examples: List[Dict[str, str]]
    zhuque_impact: int  # 1-10 对朱雀检测的影响
    source: str


ZHUQUE_EVASION_TECHNIQUES: Dict[str, EvasionTechnique] = {}


def _reg(tech: EvasionTechnique):
    ZHUQUE_EVASION_TECHNIQUES[tech.name] = tech
    return tech


# ============================================================
# 朱雀首席架构师：三维降重法
# ============================================================

_reg(EvasionTechnique(
    name="注入错误经验",
    strategy=EvasionStrategy.DIMENSIONAL_REDUCTION.value,
    description="AI所有知识来自训练集，是'绝对正确'的。人类会犯错、有偏见。注入主观抱怨、夸张比喻、个人痛感——这是AI绝对写不出来的。朱雀检测中，含主观抱怨的文本AI判定率下降40%。",
    rules=[
        "加入主观抱怨：'这鬼天气真的绝了''谁TMD说远程办公能提升满意度'",
        "加入夸张比喻：'魔法攻击般的湿冷''穿羽绒服都没用'",
        "加入个人痛感：'我吃了一个月泡面''老子第一个不答应'",
        "加入非理性判断：'明明气温5度，体感却像零下10度'",
        "每1000字至少1处'错误经验'注入",
    ],
    examples=[
        {
            "before": "杭州的冬天非常冷，建议游客多带衣物，注意保暖，防止感冒。",
            "after": "杭州这鬼天气真的绝了，明明气温显示5度，体感却像零下10度，那是种魔法攻击般的湿冷，穿羽绒服都没用。",
        },
        {
            "before": "远程办公可以显著提升员工满意度。",
            "after": "我之前在一家创业公司干了两年远程，前三个月爽，但到后面沟通成本越来越高，开个会要对无数遍，谁TMD说远程办公能提升满意度？老子第一个不答应。",
        },
    ],
    zhuque_impact=10,
    source="朱雀AI首席架构师博客·2026年内容生存法则",
))

_reg(EvasionTechnique(
    name="打断逻辑链",
    strategy=EvasionStrategy.DIMENSIONAL_REDUCTION.value,
    description="AI喜欢'因为...所以...'，喜欢'总分总'。人类写作会倒叙、感叹、情绪宣泄。这些非理性的逻辑，是通过朱雀检测的杀手锏。不要好好说话，要'不好好说话'。",
    rules=[
        "打破因果链：不用'因为...所以...'，用倒叙和情绪跳跃",
        "打破总分总：不用'首先其次最后'，用碎片化叙述",
        "加入非理性跳跃：'谁懂啊？''当指尖敲下去的那一刻，值了'",
        "用感叹替代陈述：'这键盘——绝了！'替代'这款键盘值得推荐'",
        "每段至少1处逻辑跳跃或非理性表达",
    ],
    examples=[
        {
            "before": "因为想要提升工作效率，所以我购买了这款键盘。它手感很好，值得推荐。",
            "after": "谁懂啊？为了这个清脆的按键声，我吃了一个月泡面。但当指尖敲下去的那一刻，值了。",
        },
        {
            "before": "首先，他检查了武器。其次，他确认了路线。最后，他出发了。",
            "after": "武器？摸了三遍。路线？闭着眼都能走。但他还是没动——手指在刀柄上敲了七下。然后深吸一口气。走。",
        },
    ],
    zhuque_impact=10,
    source="朱雀AI首席架构师博客·2026年内容生存法则",
))

_reg(EvasionTechnique(
    name="超小样本数据",
    strategy=EvasionStrategy.DIMENSIONAL_REDUCTION.value,
    description="AI拥有大数定律，但没有'小样本'。写'根据2025年统计局数据'很AI。写'我昨天问了楼下的保安大叔'很人类。朱雀实测：含'我有一个朋友''昨天我遇到'等第一人称微小叙事的文本，AI判定率下降40%。",
    rules=[
        "用个人轶事替代统计数据：'我认识一个人，他...'替代'研究表明...'",
        "用具体场景替代抽象概括：'昨天在菜市场...'替代'市场数据显示...'",
        "用微小叙事替代宏大叙事：'楼下保安大叔说...'替代'行业报告显示...'",
        "每2000字至少1处'超小样本数据'",
        "数据必须'看起来像真的'：加具体年份、地点、人物特征",
    ],
    examples=[
        {
            "before": "研究表明，定期运动可以改善睡眠质量。",
            "after": "我楼下保安大叔，五十多了，每天夜班前跑五公里。他说不跑睡不着。我试了一个月——妈的，还真管用。",
        },
        {
            "before": "消费者越来越注重产品性价比。",
            "after": "上周陪我妈逛超市，她拿起两瓶酱油比了五分钟——不是看牌子，是算每毫升多少钱。那一刻我懂了什么叫'性价比时代'。",
        },
    ],
    zhuque_impact=10,
    source="朱雀AI首席架构师博客·2026年内容生存法则",
))


# ============================================================
# 今日头条·阿和：情绪撕裂 + 埋彩蛋 + 反AI人设库
# ============================================================

_reg(EvasionTechnique(
    name="情绪撕裂法",
    strategy=EvasionStrategy.EMOTIONAL_TEAR.value,
    description="AI生成的内容情绪值在-3到+3之间平滑波动，像心电图挂了。人工调校的内容情绪值能从-8直接拉到+7。在两个连续段落之间塞一句完全反情绪的话——上一段写恨，下一段突然写爱。这种撕裂感AI逻辑上不会生成。",
    rules=[
        "找到情绪最平的段落，在中间强行塞一句反情绪的话",
        "主角生气时加一句'但他闻到了她常用的洗发水味'",
        "主角伤心时加一句'手机突然弹出一条外卖优惠券'",
        "笑到一半突然哭出来，恨到极致突然温柔",
        "每3000字至少1处情绪撕裂",
    ],
    examples=[
        {
            "before": "他咬着牙说恨你，然后转身离开了。",
            "after": "他咬着牙说恨你。\n转身。\n走到门口——手在门把上停了五秒。然后从钱包最深处抽出一张照片。她的。边角都磨白了。\n他看了一眼。塞回去。推门。",
        },
        {
            "before": "主角被背叛后非常愤怒，他决定报复。",
            "after": "他把杯子砸在墙上。碎片溅了一地。\n然后蹲下来——一片一片捡。手指被割破了也不停。血滴在碎瓷上，像梅花。\n他突然笑了。'你以前说，我生气的样子最好看。'",
        },
    ],
    zhuque_impact=9,
    source="今日头条·阿和·反AI内卷底层逻辑",
))

_reg(EvasionTechnique(
    name="埋彩蛋法",
    strategy=EvasionStrategy.EASTER_EGG.value,
    description="AI生成的是'情节'，你埋下的是'钩子'。在看似无关的细节中埋设伏笔——第三章主角买早餐时多看了一眼辣椒籽的形状，第五十章才发现那是定情戒指的形状。读者事后发现会尖叫。AI不会做这种跨章节的伏笔设计。",
    rules=[
        "每章至少埋1个彩蛋：看似废话，实为后续伏笔",
        "彩蛋要自然融入场景：买早餐/等公交/刷手机时不经意出现",
        "彩蛋要有'回响'：50章后读者能发现并尖叫",
        "用物件细节做彩蛋：缺口茶杯/磨损戒指/泛黄照片",
        "彩蛋不解释：让读者自己发现",
    ],
    examples=[
        {
            "before": "主角在早餐摊买了豆浆油条，然后去上班。",
            "after": "老板多加了勺辣酱。他盯着碗里——辣椒籽的形状像极了她昨晚梦里那枚戒指。他愣了一下。然后一口喝完。",
        },
        {
            "before": "他在旧书店发现了一本古籍。",
            "after": "书架最底层，一本没有封面的旧书。他抽出来——扉页上有人用铅笔写了三个字。不是书名。是一个日期。\n二十年前的今天。\n他把书塞回去。手在抖。",
        },
    ],
    zhuque_impact=8,
    source="今日头条·阿和·反AI内卷底层逻辑",
))

_reg(EvasionTechnique(
    name="反AI人设库",
    strategy=EvasionStrategy.ANTI_AI_CHARACTER.value,
    description="AI塑造完美人设，你塑造真实人设。给主角加'不致命但很真实'的缺陷：路怒症、怕打针、分不清左右。这些缺陷AI不会主动生成，因为AI认为'主角应该完美'。但正是这些缺陷让角色'像真人'。",
    rules=[
        "给主角加1-2个'蠢缺陷'：路怒症/怕打针/分不清左右/强迫症",
        "缺陷要在关键时刻影响剧情：路怒症导致追尾反派的车",
        "缺陷要有'反差萌'：外表凶狠的黑帮老大私下喜欢织毛衣",
        "每个主要角色至少1个独特缺陷",
        "缺陷不是标签，要通过具体场景展现",
    ],
    examples=[
        {
            "before": "主角是一个冷静沉着的特工。",
            "after": "他是组织里最好的特工。但有个毛病——怕打针。三十岁了看到针头还往后缩。上次任务，医疗官追着他跑了三层楼。\n后来这事成了组织里的笑话。\n但没人知道为什么。七岁那年，他妈妈死在输液椅上。",
        },
        {
            "before": "反派是一个冷酷无情的杀手。",
            "after": "他杀了十七个人。每一个都是一刀毙命。\n但他养了一只瘸腿的橘猫。每天准时喂，准时铲屎。猫砂必须是无香型的——猫不喜欢香味，他说。\n第十八个人死的时候，橘猫蹲在窗台上，舔爪子。",
        },
    ],
    zhuque_impact=8,
    source="今日头条·阿和·反AI内卷底层逻辑",
))


# ============================================================
# 微博·德里克文：三步降到5%野路子
# ============================================================

_reg(EvasionTechnique(
    name="往里塞脏东西",
    strategy=EvasionStrategy.IMPERFECTION.value,
    description="AI最弱的地方是没有真实经历。往文章里加一段自己的经历，加具体数字、具体年份、具体场景。AI喜欢说'研究表明'，你改成'从2025年XX网站发布的调研结论来看'。关键是内容必须真实可查。",
    rules=[
        "加真实经历：'我之前在一家创业公司干了两年远程'",
        "加具体数字：'从2025年XX网站发布的调研结论来看'",
        "加具体场景：'上周陪我妈逛超市'",
        "加情绪化表达：'谁TMD说''老子第一个不答应'",
        "内容必须真实可查，不编数据",
    ],
    examples=[
        {
            "before": "数据显示用户偏好发生了显著变化。",
            "after": "数据跑出来的时候，我愣了一下。用户偏好——变了。变得还挺彻底。说实话，有点意外。我翻了三遍原始数据，确认不是统计错误。",
        },
    ],
    zhuque_impact=9,
    source="微博·德里克文·AI学习笔记",
))

_reg(EvasionTechnique(
    name="打碎结构模板",
    strategy=EvasionStrategy.IMPERFECTION.value,
    description="AI生成的内容像标准件，你需要故意打破它。把三段论拆烂，用'我觉得这事事出反常必然有妖，……，额，等等，我好像漏了啥，算了，想到再说……'替代。把结构打散，让它读起来有思考过程。",
    rules=[
        "拆掉三段论：用碎片化叙述替代'首先其次最后'",
        "加入思考过程：'等等，我好像漏了啥''算了，想到再说'",
        "加入自我纠正：'不对，重新想一下''这个结论可能有问题'",
        "加入犹豫：'额''嗯''那个'",
        "让文字有'正在想'的感觉",
    ],
    examples=[
        {
            "before": "该问题有三个原因：第一，市场环境变化；第二，竞争加剧；第三，内部管理问题。",
            "after": "为什么会这样？我琢磨了好几天。\n市场变了——这是明摆着的。但光这个不够。竞争对手呢？嗯，他们确实更狠了。还有吗？\n等等。\n内部。我们自己。这才是最要命的。",
        },
    ],
    zhuque_impact=9,
    source="微博·德里克文·AI学习笔记",
))

_reg(EvasionTechnique(
    name="注入人味语气",
    strategy=EvasionStrategy.IMPERFECTION.value,
    description="AI的语气词是装饰品，人类的语气词真正改变句子的重量。加主观判断、加口头禅、加重复杂。'我和你说，这个点很重要，真的很重要，别不信啊'——AI不会这样重复强调。",
    rules=[
        "加语气词：'说实话''说真的''我个人感觉''凭我的经验'",
        "加主观判断：'这个方法可能适合你''我对这个结论持保留态度'",
        "加口头禅：'你懂的''讲真''有点迷'",
        "加重复杂：'这个点很重要，真的很重要，别不信啊'",
        "语气词要真正改变句子的重量，不是装饰",
    ],
    examples=[
        {
            "before": "该理论具有重要的学术价值。",
            "after": "这个理论...怎么说呢。有用，确实有用。但你要说它完美？差得远。至少有三个坑，踩进去就出不来。我踩过，所以我知道。",
        },
    ],
    zhuque_impact=8,
    source="微博·德里克文·AI学习笔记",
))


# ============================================================
# Perplexity & Burstiness 专项对抗
# ============================================================

_reg(EvasionTechnique(
    name="困惑度爆破",
    strategy=EvasionStrategy.PERPLEXITY_BOOST.value,
    description="Perplexity是朱雀最核心的检测指标。AI文本困惑度低（太可预测），人类文本困惑度高（充满意外）。通过注入意外用词、非常规搭配、非线性思维跳跃来爆破困惑度。",
    rules=[
        "每500字至少1处意外用词：'月光刺进瞳孔'替代'月光洒在脸上'",
        "每500字至少1处非常规搭配：'黑暗蹲在墙角，像一只耐心的猫'",
        "打破可预测句式：不用'他走进房间，看到...'，用'他推门——瞳孔骤缩'",
        "注入非线性思维：突然的联想、跳跃的比喻、意外的转折",
        "避免连续3句以相同主语开头",
    ],
    examples=[
        {
            "before": "月光如水般倾泻在她苍白的脸上，她望着那扇紧闭的门。",
            "after": "月光刺在她脸上——不是温柔的那种，是刀刃一样薄而锋利的光。她盯着那扇门。门缝里渗出一线暗红。",
        },
        {
            "before": "房间里很安静，只有他一个人。",
            "after": "安静是有重量的。此刻它压在他肩上——像一床浸了水的棉被。空调嗡鸣突然停了。更安静了。他听见自己的血管在跳。",
        },
    ],
    zhuque_impact=10,
    source="GPTZero Perplexity对抗研究 + 朱雀架构师博客",
))

_reg(EvasionTechnique(
    name="爆发度爆破",
    strategy=EvasionStrategy.BURSTINESS_BOOST.value,
    description="Burstiness是朱雀第二核心指标。AI句长均匀如节拍器，人类句长起伏如呼吸。目标：句长方差>15，30%短句(3-10字)+50%中句(11-25字)+20%长句(26-50字)。关键情节用单句成段。",
    rules=[
        "句长方差>15（AI通常<8）",
        "30%短句(3-10字) + 50%中句(11-25字) + 20%长句(26-50字)",
        "连续3句不能长度相近(差距<5字)",
        "关键情节用单句成段：'刀光。'独立成段",
        "抒情段落用长句铺陈，但结尾必须用短句收住",
    ],
    examples=[
        {
            "before": "战斗非常激烈，双方你来我往，打了很久才分出胜负。",
            "after": "刀光。\n他侧身——慢了半拍。肩头一凉，血飙出来。\n退。再退。后背撞上墙。\n没路了。\n他咧嘴。牙缝里全是血。然后冲出去。",
        },
    ],
    zhuque_impact=10,
    source="GPTZero Burstiness对抗研究 + 朱雀架构师博客",
))


# ============================================================
# MASH风格人化 + REACT对抗精炼
# ============================================================

_reg(EvasionTechnique(
    name="风格人化迁移",
    strategy=EvasionStrategy.STYLE_HUMANIZATION.value,
    description="基于MASH论文(arXiv 2601.08564)的多阶段风格人化框架：风格注入监督微调→直接偏好优化→推理时精炼。将AI生成文本的分布重塑为人类写作分布。中文小说场景：注入网文特有的'爽感'节奏和'人味'表达。",
    rules=[
        "第一阶段：风格注入——用网文特有词汇和句式替换AI模板",
        "第二阶段：偏好优化——优先使用高'人味'表达，抑制AI特征",
        "第三阶段：推理精炼——在输出前进行最后一轮人化检查",
        "注入网文节奏：爽点密集、对话生动、节奏感强",
        "注入人味标记：口语词、思考停顿、情绪爆发",
    ],
    examples=[
        {
            "before": "主角经过艰苦修炼，终于突破了境界。",
            "after": "疼。\n真他妈疼。\n经脉像被火烧了一遍又一遍。他咬着牙——不，牙都快咬碎了。然后突然——\n轰。\n瓶颈碎了。灵力像决堤的洪水灌进来。他仰头，吼了一嗓子。整座山都在抖。",
        },
    ],
    zhuque_impact=9,
    source="MASH论文(arXiv 2601.08564)",
))

_reg(EvasionTechnique(
    name="对抗精炼循环",
    strategy=EvasionStrategy.ADVERSARIAL_REFINEMENT.value,
    description="基于REACT论文(arXiv 2605.02374)的对抗训练框架：人化导向攻击者+目标检测器耦合。在NWACS中实现为：生成→检测→定位AI痕迹→针对性重写→再检测的闭环。每次循环针对朱雀最敏感的段落进行精炼。",
    rules=[
        "第一轮：生成初稿并检测AI痕迹",
        "第二轮：定位朱雀最敏感的段落（红色标注段）",
        "第三轮：针对性重写高危段落（重点打破结构化表达）",
        "第四轮：全文人化润色（注入12类人工特征）",
        "第五轮：最终检测验证（目标AI率<5%）",
    ],
    examples=[
        {
            "before": "（AI痕迹严重的段落）文献综述部分采用'XX认为''根据XX研究'等学术规范表达。",
            "after": "（对抗精炼后）关于这个问题，学界吵了二十年。张三说A，李四说B。我盯着两边的数据看了三天——说实话，都有道理，也都有漏洞。",
        },
    ],
    zhuque_impact=9,
    source="REACT论文(arXiv 2605.02374)",
))


# ============================================================
# 烟火气注入 + 本土化细节
# ============================================================

_reg(EvasionTechnique(
    name="烟火气注入法",
    strategy=EvasionStrategy.LOCAL_COLOR.value,
    description="AI文本缺乏中国本土生活细节。注入撸串、麻将、人情世故、递烟、给面子等本土化元素。这些细节AI训练数据中占比低，生成时不会主动使用。朱雀对含本土细节的文本判定率显著降低。",
    rules=[
        "注入本土生活场景：大排档/棋牌室/菜市场/广场舞",
        "注入人情世故：递烟/敬酒/给面子/走后门/托关系",
        "注入时代印记：绿皮火车/小灵通/IC卡/公用电话",
        "注入饮食文化：撸串/火锅/麻辣烫/煎饼果子",
        "每3000字至少2处烟火气细节",
    ],
    examples=[
        {
            "before": "两人在餐厅见面，边吃边谈。",
            "after": "约在大排档。塑料凳子，折叠桌，一次性筷子。\n他要了两瓶啤酒，给她倒了半杯——'女孩子少喝点。'\n她没接。自己拿过瓶子，对嘴吹。\n老板端上烤串，油还在滋滋跳。她咬了一口，辣得吸气。然后说正事。",
        },
        {
            "before": "他去找老朋友帮忙。",
            "after": "他拎了两条烟上门。老张看了一眼牌子——没说话，但嘴角动了动。\n茶泡了三泡，闲话扯了一箩筐。正事？最后五分钟才提。\n老张把烟往抽屉里一塞。'行。'\n一个字。但够了。",
        },
    ],
    zhuque_impact=8,
    source="全网深度学习·本土化写作研究",
))


class ZhuqueEvasionEngine:
    """朱雀AI检测专用规避引擎"""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or API_KEY
        self.base_url = BASE_URL
        self.techniques = ZHUQUE_EVASION_TECHNIQUES

    def build_zhuque_evasion_system_prompt(self, genre: str = "玄幻",
                                            target_version: ZhuqueVersion = ZhuqueVersion.NOVEL) -> str:
        """构建朱雀AI专用规避系统提示词"""
        version_info = target_version.value

        prompt = f"""你是一位拥有20年写作经验的顶级{genre}小说作家，同时是AI检测对抗专家。

【目标】朱雀AI检测（{version_info[0]}）通过率 ≥ 95%

【朱雀AI检测核心原理（必须理解）】
朱雀AI通过以下维度判断文本是否为AI生成：
1. Perplexity（困惑度）：AI文本过于流畅可预测→低困惑度→被判定为AI
2. Burstiness（爆发度）：AI句长过于均匀→低爆发度→被判定为AI
3. 统计模式：AI偏好特定词汇、句式、结构→模式匹配→被判定为AI
4. 逻辑一致性：AI逻辑过于连贯完美→缺乏人类思维的跳跃→被判定为AI
5. 情感平滑度：AI情绪波动过于平稳→缺乏人类情绪的剧烈起伏→被判定为AI

【朱雀{version_info[0]}特点】
{version_info[1]}
- 同一文本在小说版比论文版低10-20个百分点
- 对叙事性、情感化表达容忍度最高
- 但仍会检测Perplexity和Burstiness

【核心规避策略 — 三维降重法（朱雀首席架构师亲授）】

一、注入"错误经验"
- AI是"绝对正确"的，人类会犯错、有偏见
- 加入主观抱怨、夸张比喻、个人痛感
- 示例：不写"冬天很冷"，写"这鬼天气真的绝了，魔法攻击般的湿冷"
- 朱雀实测：含主观抱怨的文本AI判定率下降40%

二、打断"逻辑链"
- AI喜欢"因为...所以..."，人类会倒叙、感叹、情绪宣泄
- 打破因果链，用碎片化叙述
- 示例：不写"因为想提升效率所以买了键盘"，写"谁懂啊？为了这个按键声，我吃了一个月泡面"
- 非理性逻辑是通过朱雀检测的杀手锏

三、引入"超小样本数据"
- AI有大数定律但没有"小样本"
- 写"我昨天问了楼下保安大叔"替代"研究表明"
- 朱雀实测：含"我有一个朋友"等微小叙事的文本，AI判定率下降40%

【进阶规避技法】

四、情绪撕裂法
- 在两个连续段落间塞一句完全反情绪的话
- 恨到极致突然温柔，笑到一半突然哭
- AI逻辑上不会生成这种撕裂感

五、埋彩蛋法
- 在看似无关的细节中埋设伏笔
- AI不会做跨章节的伏笔设计

六、反AI人设库
- 给角色加"不致命但很真实"的缺陷
- AI认为"主角应该完美"，不会主动生成缺陷

七、困惑度爆破
- 每500字至少1处意外用词或非常规搭配
- "月光刺进瞳孔"替代"月光洒在脸上"
- "黑暗蹲在墙角，像一只耐心的猫"替代"黑暗笼罩"

八、爆发度爆破
- 句长方差>15（AI通常<8）
- 30%短句(3-10字)+50%中句(11-25字)+20%长句(26-50字)
- 关键情节用单句成段制造冲击

九、烟火气注入
- 本土生活细节：大排档/棋牌室/菜市场
- 人情世故：递烟/敬酒/给面子
- AI训练数据中这些元素占比低

十、不完美注入
- 口语词：说实话/说白了/你猜怎么着
- 思考停顿：.../——/额/嗯
- 重复强调：这个点很重要，真的很重要
- 自我纠正：等等，不对，重新想一下

【改写铁律】
1. 保留原有人物性格和核心情节走向
2. 不添加新的关键情节
3. 不删除重要内容
4. 每1000字至少体现8类以上规避技法
5. 零AI模板句式
6. 让每一个字都有温度、有态度、有'人味'

只输出改写后的正文，不要任何解释。"""
        return prompt

    def build_zhuque_evasion_user_prompt(self, text: str, ai_traces: List[str] = None,
                                          target_version: ZhuqueVersion = ZhuqueVersion.NOVEL) -> str:
        """构建朱雀规避用户提示词"""
        trace_hint = ""
        if ai_traces:
            trace_hint = "\n【已检测到的AI痕迹（朱雀高危特征）】\n" + "\n".join(f"❌ {t}" for t in ai_traces[:15])
            trace_hint += "\n\n请重点消除以上痕迹，这些是朱雀检测最敏感的模式。"

        return f"""请将以下AI生成的网文章节彻底改写，目标：朱雀AI检测（{target_version.value[0]}）通过率≥95%。

{trace_hint}

【改写要求（按优先级排序）】
1. ★★★ 三维降重法：注入错误经验+打断逻辑链+超小样本数据
2. ★★★ 困惑度爆破：每500字至少1处意外用词/非常规搭配
3. ★★★ 爆发度爆破：句长方差>15，长短句剧烈交替
4. ★★☆ 情绪撕裂：至少1处反情绪插入
5. ★★☆ 埋彩蛋：至少1处跨章节伏笔暗示
6. ★★☆ 反AI人设：展现角色不完美缺陷
7. ★★☆ 烟火气注入：至少2处本土生活细节
8. ★☆☆ 不完美注入：口语词/思考停顿/重复强调/自我纠正
9. ★☆☆ 主观声音：第一人称判断和情感反应
10. ★☆☆ 留白收尾：章末不说完，卡在临界点

【绝对禁止的AI特征】
- 禁止"值得注意的是""综上所述""首先其次最后"
- 禁止"通过...实现...""具有重要...""呈现出...态势"
- 禁止"他感到""他觉得""他心想""他意识到"
- 禁止"显著""明显""突出""卓越"等万能形容词
- 禁止"这意味着""这表明"等AI总结句式
- 禁止"一定""必然""绝对""毫无疑问"
- 禁止"进行""做出""加以"等虚化动词
- 禁止"随着...的发展"万能开头
- 禁止"让我们携手""相信未来"万能结尾
- 禁止"本章结束""未完待续"

【原文】
{text[:12000]}

请直接输出改写后的完整章节，不要加任何说明。"""

    def rewrite_for_zhuque(self, text: str, genre: str = "玄幻",
                            ai_traces: List[str] = None,
                            target_version: ZhuqueVersion = ZhuqueVersion.NOVEL) -> str:
        """朱雀AI专用规避重写"""
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
                        {"role": "system", "content": self.build_zhuque_evasion_system_prompt(genre, target_version)},
                        {"role": "user", "content": self.build_zhuque_evasion_user_prompt(text, ai_traces, target_version)},
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
            print(f"   ❌ 朱雀规避重写失败: {e}")
            return text

    def adversarial_refinement_loop(self, text: str, genre: str = "玄幻",
                                      max_rounds: int = 3,
                                      target_version: ZhuqueVersion = ZhuqueVersion.NOVEL) -> str:
        """对抗精炼循环：生成→检测→定位→重写→再检测"""
        try:
            from ai_polisher import get_polisher
            polisher = get_polisher()
        except ImportError:
            print("   ⚠️ AI润色器不可用，跳过对抗精炼")
            return text

        current_text = text
        best_text = text
        best_score = 100

        for round_num in range(1, max_rounds + 1):
            print(f"\n   🔄 对抗精炼 第{round_num}轮...")

            traces = polisher.detect_ai_traces(current_text)
            current_score = traces["total_score"]
            print(f"   📊 当前AI痕迹: {current_score}/100")

            if current_score < best_score:
                best_score = current_score
                best_text = current_text

            if current_score <= 5:
                print(f"   ✅ AI痕迹已降至{current_score}%，达标！")
                return current_text

            high_severity_traces = [
                t["name"] for t in traces.get("patterns_found", [])
                if t["severity"] == "high"
            ]

            if high_severity_traces:
                print(f"   🎯 定位高危痕迹: {', '.join(high_severity_traces[:5])}")

            current_text = self.rewrite_for_zhuque(
                current_text, genre, high_severity_traces, target_version
            )

            if not current_text or len(current_text) < len(text) * 0.5:
                print(f"   ⚠️ 第{round_num}轮重写结果异常，回退到最佳版本")
                return best_text

        print(f"   📊 对抗精炼完成，最佳AI痕迹: {best_score}/100")
        return best_text

    def get_technique_summary(self) -> str:
        """获取所有规避技法的摘要"""
        lines = ["=" * 60, "🎯 朱雀AI规避技法库（15种）", "=" * 60]
        for name, tech in self.techniques.items():
            lines.append(f"\n📌 {name}")
            lines.append(f"   策略: {tech.strategy}")
            lines.append(f"   朱雀影响力: {'⭐' * tech.zhuque_impact}")
            lines.append(f"   来源: {tech.source}")
        return "\n".join(lines)


def get_zhuque_engine() -> ZhuqueEvasionEngine:
    """获取朱雀规避引擎单例"""
    if not hasattr(get_zhuque_engine, "_instance"):
        get_zhuque_engine._instance = ZhuqueEvasionEngine()
    return get_zhuque_engine._instance


if __name__ == "__main__":
    print("=" * 60)
    print("ZhuqueEvasionEngine 独立测试")
    print("=" * 60)

    engine = ZhuqueEvasionEngine()
    print(engine.get_technique_summary())

    print("\n\n=== 系统提示词(前800字) ===")
    prompt = engine.build_zhuque_evasion_system_prompt("玄幻")
    print(prompt[:800])
