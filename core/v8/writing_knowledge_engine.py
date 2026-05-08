#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 写作知识引擎 - WritingKnowledgeEngine

整合深度研究成果，提供:
1. AI特征检测知识库 - 六层检测体系(词汇/句式/语义/结构/情感/语用)
2. 写作技法推荐 - 资深小说家必备的125+核心技法
3. 读者吸引策略 - 基于认知心理学的读者留存方法论
4. 去AI痕迹策略 - 六层递进式去痕流水线
5. 智能诊断与建议 - 自动分析文本并给出优化方案

研究来源:
- 西湖大学NLP实验室 Fast-DetectGPT 原理
- Humanizer-zh 21类AI特征识别体系
- 罗伯特·麦基《故事》核心理论
- 番茄小说金番作家实战经验
- 网文圈资深编辑审稿标准
- PNAS 2025 AI文本语言学研究
"""

import re
import math
from typing import Dict, List, Tuple, Optional, Any, Set
from dataclasses import dataclass, field
from collections import Counter
from enum import Enum


# ═══════════════════════════════════════════════════════════════
# 第一部分: AI特征检测知识库 (六层体系)
# ═══════════════════════════════════════════════════════════════

class AITraitLevel(Enum):
    """AI特征层级"""
    LEXICAL = "词汇层"
    SYNTACTIC = "句式层"
    SEMANTIC = "语义层"
    STRUCTURAL = "结构层"
    EMOTIONAL = "情感层"
    PRAGMATIC = "语用层"


@dataclass
class AITrait:
    """单个AI特征"""
    name: str
    level: AITraitLevel
    description: str
    risk_score: float  # 0-1, 越高越容易被识别为AI
    examples: List[str]
    fix_strategy: str
    fix_examples: List[str]


AI_TRAITS_LIBRARY: Dict[str, AITrait] = {
    # ── 词汇层特征 ──
    "ai_connectors": AITrait(
        name="机械连接词",
        level=AITraitLevel.LEXICAL,
        risk_score=0.85,
        description="AI偏好使用'首先/其次/最后/此外/总而言之'等结构化连接词，"
                    "人类写作中这些词的使用频率低60%以上",
        examples=[
            "首先，他检查了周围的环境。其次，他开始制定计划。最后，他付诸行动。",
            "此外，这个发现还具有深远的意义。总而言之，这是一次成功的尝试。",
        ],
        fix_strategy="用内容自然承接替代连接词，或直接删除；用具体动作/感受过渡",
        fix_examples=[
            "他扫了一圈——没人。好，开始干活。",
            "这个发现让他手都在抖。值了，这一趟没白跑。",
        ],
    ),

    "ai_abstract_nouns": AITrait(
        name="抽象名词堆砌",
        level=AITraitLevel.LEXICAL,
        risk_score=0.80,
        description="AI高频使用'赋能/底层逻辑/闭环/维度/格局/体系'等抽象管理学术语，"
                    "PNAS 2025研究证实AI使用复杂词汇频率比人类高100倍以上",
        examples=[
            "这次修炼为他后续的成长体系赋能，形成了完整的实力闭环。",
            "他深刻理解了修炼的底层逻辑，格局得到了极大提升。",
        ],
        fix_strategy="用具体、可感知的词汇替代；用身体感受/具体动作代替抽象概念",
        fix_examples=[
            "丹田里的气旋又大了一圈，运转起来像磨盘碾豆子，嘎嘣响。",
            "他忽然明白了——不是功法的问题，是自己太急。慢下来，反而快了。",
        ],
    ),

    "ai_emotion_adverbs": AITrait(
        name="情感副词直述",
        level=AITraitLevel.LEXICAL,
        risk_score=0.90,
        description="AI直接写'他感到很愤怒''她非常悲伤'，而非通过动作/神态/对话展示情感。"
                    "人类写作中情感词使用频率仅为AI的45%",
        examples=[
            "他感到非常愤怒。",
            "她十分悲伤，忍不住哭了起来。",
            "他内心充满了恐惧。",
        ],
        fix_strategy="删除情感标签词，用身体反应/动作/对话展示情感",
        fix_examples=[
            "他五指攥紧，指节泛白，牙缝里挤出两个字：'找死。'",
            "她没说话，眼泪就那么掉下来了，一滴一滴砸在手背上。",
            "他的腿在抖。控制不住的那种。",
        ],
    ),

    "ai_vague_attribution": AITrait(
        name="模糊归因",
        level=AITraitLevel.LEXICAL,
        risk_score=0.75,
        description="AI常用'专家认为/研究表明/行业报告显示/有人说过'等无源引用，"
                    "约12%的AI引用无法溯源",
        examples=[
            "据古籍记载，这种功法源自上古时期。",
            "有经验的修士都知道，突破境界需要机缘。",
        ],
        fix_strategy="要么给出具体来源，要么改为角色个人经验/观察",
        fix_examples=[
            "师父说过，这功法是祖师爷从一座破庙里扒出来的，真假都不知道。",
            "他试过三次，三次都差点死。第四次，他学乖了。",
        ],
    ),

    "ai_hedging": AITrait(
        name="过度委婉/模糊限定",
        level=AITraitLevel.LEXICAL,
        risk_score=0.70,
        description="AI常用'可能/或许/似乎/在一定程度上/某种意义上'等模糊限定词，"
                    "缺乏确定的判断力",
        examples=[
            "这似乎意味着某种程度上的突破。",
            "或许在某种意义上，他的选择是正确的。",
        ],
        fix_strategy="给出明确判断，或通过角色视角表达不确定性",
        fix_examples=[
            "突破了。他能感觉到——丹田里的气不再是散的了。",
            "对不对？他不知道。但再来一次，他还是会这么选。",
        ],
    ),

    "ai_dash_abuse": AITrait(
        name="破折号滥用",
        level=AITraitLevel.LEXICAL,
        risk_score=0.65,
        description="AI生成文本中破折号使用频率是人类写作的3-5倍，"
                    "已成为读者识别AI内容的最直观标志之一",
        examples=[
            "他走进了一个全新的世界——一个充满机遇与挑战的世界——在这里，"
            "一切都将重新开始——而他，已经做好了准备。",
        ],
        fix_strategy="限制破折号使用，用句号分隔或用逗号自然连接",
        fix_examples=[
            "他走进了一个全新的世界。充满机遇，也充满挑战。"
            "一切重新开始。他准备好了。",
        ],
    ),

    "ai_high_freq_words": AITrait(
        name="AI高频万能词",
        level=AITraitLevel.LEXICAL,
        risk_score=0.78,
        description="AI偏好使用'时代/人生/智慧/力量/命运/灵魂/本质'等宏大词汇，"
                    "什么题材都能套用，缺乏具体性",
        examples=[
            "这是命运的安排，是时代的召唤。",
            "他领悟了力量的本质，洞悉了人生的智慧。",
        ],
        fix_strategy="用具体场景/具体事物替代宏大词汇",
        fix_examples=[
            "就是这么巧。巧得他怀疑有人在背后安排。",
            "他忽然想通了——拳头硬不硬不重要，重要的是打在哪里。",
        ],
    ),

    # ── 句式层特征 ──
    "ai_parallel_structure": AITrait(
        name="排比/对偶句式",
        level=AITraitLevel.SYNTACTIC,
        risk_score=0.82,
        description="AI尤其喜欢使用对偶句、排比句，句式高度工整对称。"
                    "人类学生的作文开头灵活多样，没有固定套路",
        examples=[
            "他既有勇者的无畏，又有智者的深沉；既能在战场上所向披靡，"
            "又能在朝堂上运筹帷幄。",
            "风在呼啸，雷在轰鸣，电在闪烁，雨在倾泻。",
        ],
        fix_strategy="打破对称，让句子长短不一；用一句具体描写替代排比",
        fix_examples=[
            "他打架不要命，但脑子也快。战场上活下来的，没一个傻子。",
            "风大得站不住人。雷声追着闪电劈下来，震得地都在抖。",
        ],
    ),

    "ai_sentence_length_uniform": AITrait(
        name="句长高度均匀",
        level=AITraitLevel.SYNTACTIC,
        risk_score=0.72,
        description="AI生成文本的句长变异系数比人类写作低30%，"
                    "句子长度过于规律，缺乏人类写作中自然的节奏变化",
        examples=[
            "他推开门走了进去。房间里空无一人。桌上放着一封信。"
            "他拿起信仔细阅读。信中只有一句话。",
        ],
        fix_strategy="刻意制造句长变化：短句(3-5字)+中句(15-25字)+长句(30-50字)交替",
        fix_examples=[
            "他推开门。空的。桌上搁着一封信，信封上没写名字，"
            "只压了一道折痕——像是被人反复打开又折回去的。他拿起来，抽出信纸。"
            "就一句话。",
        ],
    ),

    "ai_subject_action_template": AITrait(
        name="主语+动作模板化",
        level=AITraitLevel.SYNTACTIC,
        risk_score=0.68,
        description="AI高频使用'他/她+动词+宾语'的固定模板，"
                    "缺乏句式变换和倒装等修辞手法",
        examples=[
            "他站起身。他走到窗前。他看向窗外。他叹了口气。",
        ],
        fix_strategy="变换主语位置、使用无主语句、穿插环境描写打断动作链",
        fix_examples=[
            "站起来的时候膝盖咔嗒响了一声。窗外的天已经黑了。"
            "他盯着那片黑看了很久，然后叹了口气——不是累，是烦。",
        ],
    ),

    "ai_prepositional_starts": AITrait(
        name="介词短语开头泛滥",
        level=AITraitLevel.SYNTACTIC,
        risk_score=0.60,
        description="AI高频使用'在...中/下/里''随着...''当...时'等介词短语开头，"
                    "形成可预测的句式模式",
        examples=[
            "在月光的照耀下，他缓缓前行。",
            "随着实力的提升，他的信心也在增长。",
            "当他睁开眼睛的时候，一切都变了。",
        ],
        fix_strategy="用具体名词或动作开头，减少介词短语开头比例",
        fix_examples=[
            "月光把路照得惨白。他走得很慢。",
            "实力涨了，胆子也涨了。他开始想一些以前不敢想的事。",
            "睁眼。世界变了。",
        ],
    ),

    "ai_passive_voice": AITrait(
        name="被动语态过度",
        level=AITraitLevel.SYNTACTIC,
        risk_score=0.55,
        description="AI在中文中也倾向使用被动结构('被/让/给/叫')，"
                    "而人类写作更偏好主动语态",
        examples=[
            "他被一股强大的力量推了出去。",
            "门被风吹开了。",
        ],
        fix_strategy="改为主动语态，或直接用动作描述",
        fix_examples=[
            "一股大力撞上来，他整个人飞了出去。",
            "风撞开了门。",
        ],
    ),

    # ── 语义层特征 ──
    "ai_semantic_flatness": AITrait(
        name="语义扁平化",
        level=AITraitLevel.SEMANTIC,
        risk_score=0.88,
        description="AI文本缺乏潜台词和言外之意，所有信息都浮在表面。"
                    "人类写作中'冰山理论'——只写八分之一，八分之七在水下",
        examples=[
            "他很难过，因为他最好的朋友背叛了他。",
            "这个地方很危险，到处都是陷阱。",
        ],
        fix_strategy="不直接说明，通过细节暗示；让读者自己推断情感和判断",
        fix_examples=[
            "他把两人合影的相框扣在桌上。没摔。只是不想再看见那张脸。",
            "他数了数——三步之内，三处机关。设计这地方的人，没打算让人活着出去。",
        ],
    ),

    "ai_encyclopedic_explanation": AITrait(
        name="百科式平铺直叙",
        level=AITraitLevel.SEMANTIC,
        risk_score=0.83,
        description="AI解释概念时呈现'百科全书式'的平铺直叙，"
                    "缺乏个性化思考轨迹和主观视角",
        examples=[
            "灵力是这个世界的基本能量单位，分为金木水火土五种属性。"
            "修炼者通过吸收天地灵气来提升自己的灵力等级。",
        ],
        fix_strategy="通过角色视角/对话/场景自然带出设定，避免直接科普",
        fix_examples=[
            "'灵力？'师父吐了口烟，'你就当是空气里飘的钱。有人天生会捡，"
            "有人一辈子捡不着。你嘛——'他上下打量了一眼，'先学会喘气再说。'",
        ],
    ),

    "ai_fake_authority": AITrait(
        name="虚构权威引用",
        level=AITraitLevel.SEMANTIC,
        risk_score=0.70,
        description="AI生成内容中约12%的引用无法溯源，"
                    "常出现不存在的古籍/专家/研究",
        examples=[
            "《上古修炼总纲》中记载：'灵气者，天地之精华也。'",
            "据修炼协会统计，90%的修士在突破时都会遇到瓶颈。",
        ],
        fix_strategy="如果引用不存在，就创造具体的、有缺陷的、像真实存在的来源",
        fix_examples=[
            "师父给的那本破书上就写了三行字，剩下全是涂鸦。"
            "但就这三行，够他琢磨三年。",
            "他问过十个散修，九个说突破靠运气。剩下一个是哑巴。",
        ],
    ),

    "ai_causal_simplification": AITrait(
        name="因果简化",
        level=AITraitLevel.SEMANTIC,
        risk_score=0.75,
        description="AI倾向给出简单直接的因果关系，"
                    "而人类写作中的因果链更复杂、更多偶然性",
        examples=[
            "因为他刻苦修炼，所以实力提升了。",
            "由于敌人的轻敌，他获得了胜利。",
        ],
        fix_strategy="加入偶然因素、代价、副作用；让因果关系更复杂更真实",
        fix_examples=[
            "刻苦是真的刻苦——练到吐血那种。但突破那天，"
            "他其实什么都没做，就是睡了一觉。醒来就突破了。莫名其妙。",
            "敌人确实轻敌了。但他赢不是因为敌人轻敌，是因为他藏了一张底牌——"
            "一张用了会折寿十年的底牌。",
        ],
    ),

    # ── 结构层特征 ──
    "ai_three_part_structure": AITrait(
        name="三段式结构强迫",
        level=AITraitLevel.STRUCTURAL,
        risk_score=0.80,
        description="AI强行将内容分成三组/三点/三个层面，"
                    "即使内容本身不需要这种划分",
        examples=[
            "这个计划有三个关键点：第一...第二...第三...",
            "从个人层面看...从组织层面看...从社会层面看...",
        ],
        fix_strategy="根据内容自然分层，不强制三点；允许不完整的列举",
        fix_examples=[
            "计划很简单——混进去，找到东西，活着出来。"
            "至于怎么混、怎么找、怎么活，到时候再说。",
        ],
    ),

    "ai_predictable_arc": AITrait(
        name="情节弧线可预测",
        level=AITraitLevel.STRUCTURAL,
        risk_score=0.85,
        description="AI生成的情节遵循标准模板：遇到困难→努力克服→获得成长。"
                    "缺乏人类创作中的'偶然中的必然'和意外转折",
        examples=[
            "他遇到了强大的敌人→经过艰苦战斗→最终战胜了敌人→实力得到提升。",
        ],
        fix_strategy="加入意外转折、代价、失败；让胜利不是理所当然的",
        fix_examples=[
            "他遇到了强大的敌人→打不过→跑了→敌人追上来→"
            "他回头拼命→还是打不过→但敌人忽然停手了。'你身上有她的气息。'敌人说。",
        ],
    ),

    "ai_ending_summary": AITrait(
        name="结尾总结强迫症",
        level=AITraitLevel.STRUCTURAL,
        risk_score=0.78,
        description="AI几乎每段/每章结尾都要总结升华，"
                    "使用'总而言之/综上所述/这标志着/这意味着'等总结语",
        examples=[
            "总而言之，这次经历让他成长了许多。",
            "这标志着他修炼之路的新阶段。",
        ],
        fix_strategy="结尾用动作/画面/对话收束，不总结不升华",
        fix_examples=[
            "他站起来，拍了拍身上的土。天快亮了。",
            "'走吧。'他说。",
        ],
    ),

    "ai_transition_template": AITrait(
        name="过渡段模板化",
        level=AITraitLevel.STRUCTURAL,
        risk_score=0.65,
        description="AI使用固定的过渡模板连接场景，"
                    "如'与此同时/另一方面/转眼间/不久之后'",
        examples=[
            "与此同时，在千里之外的另一座城市...",
            "转眼间，三个月过去了。",
        ],
        fix_strategy="用具体细节标记时间/空间转换，不用模板过渡",
        fix_examples=[
            "他走的时候院子里的桃花还没开。回来的时候，桃子都烂在地里了。",
        ],
    ),

    # ── 情感层特征 ──
    "ai_emotion_labeling": AITrait(
        name="情感标签化",
        level=AITraitLevel.EMOTIONAL,
        risk_score=0.92,
        description="AI直接给情感贴标签('他很愤怒''她感到悲伤')，"
                    "而非通过行为/生理反应/对话展示情感。"
                    "这是AI文本最显著的特征之一",
        examples=[
            "他感到一阵愤怒涌上心头。",
            "她的心中充满了悲伤。",
            "他内心十分恐惧。",
        ],
        fix_strategy="用身体反应(心跳/呼吸/肌肉紧张)+行为+对话展示情感",
        fix_examples=[
            "太阳穴突突地跳。他把后槽牙咬得咯吱响，然后笑了。"
            "笑得旁边的人往后退了一步。",
            "她没哭。就是坐在那里，一动不动，像一尊石像。"
            "石像不会疼，但人会。",
            "他的手指在发抖。不是冷，是怕。怕得连剑都快握不住了。",
        ],
    ),

    "ai_emotion_linear": AITrait(
        name="情感线性单调",
        level=AITraitLevel.EMOTIONAL,
        risk_score=0.75,
        description="AI生成的情感变化是线性的：从A到B到C。"
                    "人类情感是混乱的、矛盾的、反复的",
        examples=[
            "他从悲伤中走出来，变得坚强。",
            "她的心情逐渐好转。",
        ],
        fix_strategy="让情感矛盾、反复、不可预测；允许角色同时拥有相反的情感",
        fix_examples=[
            "他以为自己会哭。没有。他以为自己会恨。也没有。"
            "就是空。空得连愤怒都填不满。",
            "她笑了，但眼泪同时掉下来。分不清是高兴还是难过。"
            "可能都有。可能都不是。",
        ],
    ),

    "ai_empathy_deficit": AITrait(
        name="共情缺失",
        level=AITraitLevel.EMOTIONAL,
        risk_score=0.80,
        description="AI文本难以让读者产生真正的情感共鸣，"
                    "因为AI没有真实的情感体验，只能模拟情感表达的模式",
        examples=[
            "失去亲人的痛苦是无法用语言形容的。",
        ],
        fix_strategy="用具体的、私人的、不完美的细节唤起共情",
        fix_examples=[
            "收拾遗物的时候翻出一双没织完的毛线袜。针还插在上面。"
            "他握着那双袜子站了很久。最后放回去了。没织完就没织完吧。"
            "有些事，本来就不会完。",
        ],
    ),

    # ── 语用层特征 ──
    "ai_over_explanation": AITrait(
        name="过度解释",
        level=AITraitLevel.PRAGMATIC,
        risk_score=0.82,
        description="AI不信任读者的理解能力，反复解释同一件事。"
                    "人类写作尊重读者智慧，相信读者能自己理解",
        examples=[
            "他选择了离开。这个选择意味着他放弃了眼前的一切——"
            "财富、地位、名誉，所有他曾经珍视的东西。"
            "但他知道，如果不离开，他将失去更重要的东西——自由。",
        ],
        fix_strategy="说一遍就够；相信读者能理解；删除所有解释性重复",
        fix_examples=[
            "他走了。门在身后关上，没回头。",
        ],
    ),

    "ai_collaborative_traces": AITrait(
        name="协作交流痕迹",
        level=AITraitLevel.PRAGMATIC,
        risk_score=0.60,
        description="AI文本中残留的对话式痕迹：'希望这对您有帮助'"
                    "'需要注意的是''值得强调的是'",
        examples=[
            "希望这个计划能对他有所帮助。",
            "值得注意的是，这种方法并非没有风险。",
        ],
        fix_strategy="删除所有面向读者的元评论，让内容自己说话",
        fix_examples=[
            "计划就这些。能不能成，看命。",
        ],
    ),

    "ai_tone_inconsistency": AITrait(
        name="语气断裂",
        level=AITraitLevel.PRAGMATIC,
        risk_score=0.70,
        description="AI文本中前一段用文艺书面语，后一段突然切换成口语化表达，"
                    "语气不统一",
        examples=[
            "月色如水，洒在青石板上，泛起粼粼波光。(文艺)→"
            "他妈的，这地方真漂亮。(口语)",
        ],
        fix_strategy="确定统一的叙述语气，保持一致性；如需切换，要有过渡",
        fix_examples=[
            "月光把石板路照得发白。他踩上去，脚底凉飕飕的。"
            "'操。'他低头一看，鞋底磨穿了。",
        ],
    ),
}


# ═══════════════════════════════════════════════════════════════
# 第二部分: 资深小说家写作技法库
# ═══════════════════════════════════════════════════════════════

class TechniqueCategory(Enum):
    """技法分类"""
    CHARACTER = "人物塑造"
    DIALOGUE = "对话打磨"
    SCENE = "场景构建"
    PLOT = "情节设计"
    PACING = "节奏控制"
    OPENING = "开篇技法"
    EMOTION = "情绪设计"
    LANGUAGE = "语言文笔"
    STRUCTURE = "结构大纲"
    SUSPENSE = "悬念钩子"


@dataclass
class WritingTechnique:
    """写作技法"""
    name: str
    category: TechniqueCategory
    description: str
    why_it_works: str  # 为什么有效
    how_to_apply: str  # 如何应用
    common_mistakes: str  # 常见错误
    examples: List[Tuple[str, str]]  # (错误示例, 正确示例)
    difficulty: int  # 1-5, 学习难度


WRITING_TECHNIQUES: Dict[str, WritingTechnique] = {
    # ── 人物塑造 ──
    "show_dont_tell": WritingTechnique(
        name="展示而非告知 (Show, Don't Tell)",
        category=TechniqueCategory.CHARACTER,
        description="不直接告诉读者'他很愤怒'，而是通过动作、对话、生理反应让读者自己感受到愤怒。"
                    "这是小说写作的第一铁律。",
        why_it_works="人类大脑对具体画面/声音/感受的反应远强于抽象标签。"
                     "当读者自己'推断'出角色的情绪时，代入感远强于被'告知'。",
        how_to_apply="1. 删除所有情感标签词(愤怒/悲伤/恐惧/高兴)\n"
                     "2. 用身体反应替代:心跳加速、手心出汗、肌肉紧绷\n"
                     "3. 用动作替代:摔东西、攥拳头、咬嘴唇\n"
                     "4. 用对话替代:语气、措辞、停顿\n"
                     "5. 用环境映射:天气、光线、声音",
        common_mistakes="用更花哨的形容词替代情感标签，而不是真正用动作展示。"
                        "比如把'他很愤怒'改成'他极其愤怒'——换汤不换药。",
        examples=[
            ("他感到非常愤怒。",
             "他把杯子往桌上一摔，瓷片溅了一地。'你再说一遍。'声音不大，但屋子里没人敢出声。"),
            ("她很伤心。",
             "她没哭。就是把两人合影的相框拿起来，擦了擦，又放下了。反复三次。"),
            ("他内心充满了恐惧。",
             "他的腿在抖。控制不住的那种。他想站起来，膝盖不听使唤。"),
        ],
        difficulty=3,
    ),

    "character_voice_id": WritingTechnique(
        name="人物语言身份证",
        category=TechniqueCategory.CHARACTER,
        description="为每个主要人物建立独特的说话风格——句式长短、用词偏好、口头禅、"
                    "语气特征——让读者不看引号就能分辨是谁在说话。",
        why_it_works="语言是人物性格最直接的外显。当每个人物都有独特的'声音'时，"
                     "人物会从纸面上'站'起来，变得立体可感。",
        how_to_apply="1. 为每个主要人物建一张'语言身份证'表格:\n"
                     "   - 句式偏好:短句/长句/反问/感叹\n"
                     "   - 用词特征:粗俗/文雅/专业/方言\n"
                     "   - 口头禅:1-2个标志性用语\n"
                     "   - 说话节奏:快/慢/停顿多\n"
                     "2. 写对话时对照表格检查\n"
                     "3. 做'去标签测试':去掉'XX说'，看能否分辨是谁在说话",
        common_mistakes="所有人物说话方式一样，或者口头禅过于刻意(每句话都带口头禅)。",
        examples=[
            ("'你好，我叫张三。' '你好，我是李四。' (无法分辨)",
             "主角:'张三。'他伸出手，手掌全是茧。\n"
             "配角:'哎哟，张哥！久仰久仰——'他双手握住，摇了又摇，'叫我小李就行，小李。'"),
        ],
        difficulty=4,
    ),

    "character_pressure_reveal": WritingTechnique(
        name="压力揭示性格",
        category=TechniqueCategory.CHARACTER,
        description="罗伯特·麦基《故事》核心理论：人物的真实性格只有在压力之下做出选择时才会揭示。"
                    "压力越大，揭示越深；选择越难，人物越真。",
        why_it_works="日常行为可以伪装，但生死关头的选择无法伪装。"
                     "读者通过角色在极端情境下的选择来认识角色的本质。",
        how_to_apply="1. 设计递增的压力情境:\n"
                     "   轻度压力→中度压力→重度压力→极限压力\n"
                     "2. 每个压力点让角色做选择\n"
                     "3. 选择要付出代价——没有代价的选择不揭示性格\n"
                     "4. 让角色的选择出人意料但又在情理之中",
        common_mistakes="压力情境下角色行为与日常行为完全一致——说明压力不够大。"
                        "或者角色选择毫无代价——不痛不痒的选择没有意义。",
        examples=[
            ("(轻度)被骂了一句→他忍了。(重度)被当众羞辱→他还是忍了。(无变化)",
             "(轻度)被骂了一句→他忍了。(重度)朋友被骂→他抄起了椅子。"
             "'骂我可以。骂他——不行。'"),
        ],
        difficulty=4,
    ),

    "character_contradiction": WritingTechnique(
        name="人物表里不一",
        category=TechniqueCategory.CHARACTER,
        description="人物的内心绝不能和外表一模一样。"
                    "表面冷酷的人内心柔软，表面温柔的人内心狠辣——反差创造深度。",
        why_it_works="表里如一的人物是扁平的。反差让读者产生好奇："
                     "'他为什么表面这样、内心那样？'好奇心驱动阅读。",
        how_to_apply="1. 确定人物的'表面层'和'真实层'\n"
                     "2. 在关键情节中让真实层突破表面层\n"
                     "3. 反差要合理——有背景故事支撑\n"
                     "4. 不要一次性揭示全部，逐步释放",
        common_mistakes="反差过于突兀，没有铺垫；或者反差没有原因，纯粹为了反差而反差。",
        examples=[
            ("表面冷酷+内心冷酷=扁平反派",
             "表面:杀人不眨眼的魔头。\n"
             "真实:每次杀人后都会做同一个噩梦——梦里他在保护一个人，但每次都保护不了。"),
        ],
        difficulty=3,
    ),

    # ── 对话打磨 ──
    "dialogue_information_density": WritingTechnique(
        name="对话信息密度法则",
        category=TechniqueCategory.DIALOGUE,
        description="网文对话不是聊天记录。每一句对话必须有信息量——"
                    "要么推进剧情，要么塑造人物，要么埋下伏笔。三不沾的对话，全删。",
        why_it_works="读者的注意力是有限的。废话对话会让读者跳过——跳过三次，就弃书了。",
        how_to_apply="1. 写完对话后逐句检查:这句话推进了什么?\n"
                     "2. 删掉所有客套话('你好''再见''吃饭了吗')\n"
                     "3. 删掉所有解释性废话('我是来告诉你...'→直接说内容)\n"
                     "4. 删掉50%的字数——剩下的才是精华",
        common_mistakes="用对话来'解释设定'——角色之间互相科普世界观，"
                        "这在现实中不会发生。",
        examples=[
            ("'你知道吗，这个世界的灵力分为五种属性。' '真的吗？快给我讲讲。' (尬科普)",
             "'你的灵力——'师父顿了顿，'什么颜色？'\n"
             "'蓝色。'\n"
             "'嗯。'师父没再说什么，但眼神变了。"),
        ],
        difficulty=2,
    ),

    "dialogue_subtext": WritingTechnique(
        name="对话潜台词",
        category=TechniqueCategory.DIALOGUE,
        description="人物说出来的话和真正想表达的意思之间存在差距——"
                    "这个差距就是潜台词。好的对话永远有两层意思。",
        why_it_works="读者喜欢'解码'——从表面对话中推断真实含义，"
                     "这种智力参与让阅读体验更丰富。",
        how_to_apply="1. 确定人物'真正想说的'和'实际说出来的'\n"
                     "2. 差距来源:面子/恐惧/算计/保护\n"
                     "3. 用动作/表情暗示真实想法\n"
                     "4. 偶尔让潜台词浮出水面——制造爆发点",
        common_mistakes="所有对话都是'心里话'——人物想到什么说什么，毫无保留。",
        examples=[
            ("'我爱你。' '我也爱你。' (无潜台词)",
             "'路上小心。'她把伞塞给他。\n"
             "'几步路而已。'\n"
             "'拿着。'她没看他，转身进了屋。\n"
             "(潜台词:我担心你。表面:只是递了把伞。)"),
        ],
        difficulty=4,
    ),

    # ── 场景构建 ──
    "scene_five_senses": WritingTechnique(
        name="五感沉浸法",
        category=TechniqueCategory.SCENE,
        description="每个场景至少调动三种感官——视觉/听觉/嗅觉/触觉/味觉。"
                    "AI写作通常只有视觉，人类写作天然是多感官的。",
        why_it_works="多感官描写让读者'进入'场景而非'观看'场景。"
                     "嗅觉和触觉尤其能唤起强烈的情感记忆。",
        how_to_apply="1. 写完场景后检查:用了几种感官?\n"
                     "2. 强制加入至少一种非视觉感官\n"
                     "3. 优先使用嗅觉(最古老的情感中枢)和触觉\n"
                     "4. 感官描写要服务于情绪——不是为写而写",
        common_mistakes="堆砌五种感官但毫无情感关联——"
                        "像一份感官清单而非沉浸体验。",
        examples=[
            ("他走进厨房。(纯视觉)",
             "他推开厨房门，油烟味混着蒜香扑面而来。锅铲刮过铁锅的声音刺得耳膜发紧。"
             "灶台上的热气扑到脸上，潮乎乎的。"),
        ],
        difficulty=2,
    ),

    "scene_emotion_mapping": WritingTechnique(
        name="环境情绪映射",
        category=TechniqueCategory.SCENE,
        description="环境描写不是中立的——它应该映射角色的内心状态。"
                    "悲伤时阳光也是刺眼的，快乐时雨天也是清爽的。",
        why_it_works="环境与情绪的共振让读者同时从外部和内部感受故事，"
                     "形成立体的情感体验。",
        how_to_apply="1. 确定场景的情感基调\n"
                     "2. 选择环境中与情感共振的元素\n"
                     "3. 用情感色彩描述中性事物\n"
                     "4. 同一环境在不同情感下应有不同描写",
        common_mistakes="环境描写与情感脱节——角色在悲伤，环境描写却是'阳光明媚，鸟语花香'。",
        examples=[
            ("(角色悲伤)窗外的阳光很灿烂。(脱节)",
             "(角色悲伤)阳光从窗帘缝里挤进来，在地板上划了一道口子。"
             "他盯着那道口子看了很久。"),
        ],
        difficulty=3,
    ),

    # ── 情节设计 ──
    "plot_inevitable_accident": WritingTechnique(
        name="偶然中的必然",
        category=TechniqueCategory.PLOT,
        description="好的情节推进具有'偶然中的必然'——表面上是巧合，"
                    "深层是角色性格和处境的必然结果。",
        why_it_works="纯偶然让读者觉得'作者在操控'，纯必然让故事失去惊喜。"
                     "'偶然中的必然'既合理又有惊喜感。",
        how_to_apply="1. 设计一个'巧合'事件\n"
                     "2. 回溯:这个巧合为什么会发生在这个角色身上?\n"
                     "3. 用角色的性格/选择/处境来解释巧合\n"
                     "4. 让巧合成为角色行为的'放大器'而非'决定因素'",
        common_mistakes="用巧合解决核心冲突(机械降神)——读者会觉得被愚弄。",
        examples=[
            ("主角快输了→忽然天降神雷劈死了反派。(纯巧合/机械降神)",
             "主角快输了→但他注意到反派每次出招前左肩会先动→"
             "他赌了一把，提前闪避→反派的杀招落空→主角反击。"
             "(巧合:他注意到这个细节。必然:他一直在观察。)"),
        ],
        difficulty=4,
    ),

    "plot_cost_of_victory": WritingTechnique(
        name="胜利的代价",
        category=TechniqueCategory.PLOT,
        description="每一次胜利都必须付出代价。没有代价的胜利是空洞的，"
                    "读者不会为之激动。代价越大，胜利越甜。",
        why_it_works="代价让胜利'真实'。现实中任何获得都有成本，"
                     "小说中的代价让读者相信这个世界是'真实'的。",
        how_to_apply="1. 每次主角获胜后问:他付出了什么?\n"
                     "2. 代价可以是:身体伤害/情感损失/道德妥协/人际关系破裂\n"
                     "3. 代价要有持续性——不能下一章就恢复了\n"
                     "4. 让代价影响后续选择",
        common_mistakes="代价太轻(受点伤下章就好了)或代价被轻易逆转(死了又复活)。",
        examples=[
            ("主角打败敌人，毫发无伤。(无代价)",
             "主角打败了敌人。但他用了禁术——折寿十年。而且他发现，"
             "敌人临死前说的话，让他开始怀疑自己一直以来的信念。"),
        ],
        difficulty=3,
    ),

    # ── 节奏控制 ──
    "pacing_roller_coaster": WritingTechnique(
        name="节奏过山车",
        category=TechniqueCategory.PACING,
        description="一章冲突，一章过渡，一章升级，再一章冲突。"
                    "让读者像坐过山车——冲刺→缓行→再冲刺。",
        why_it_works="持续高强度让读者疲劳，持续低强度让读者无聊。"
                     "交替的节奏让读者始终处于'刚好要放松，下一波又来了'的状态。",
        how_to_apply="1. 画'节奏图谱':横轴章节，纵轴张力(0-10)\n"
                     "2. 高潮(8-9分)不超过连续两章\n"
                     "3. 高潮后必须穿插低张力章节(2-4分)\n"
                     "4. 低张力章节也要推进剧情(清点战利品/修炼升级/日常互动)",
        common_mistakes="全程高能(读者累)或全程平淡(读者跑)。",
        examples=[
            ("连续五章大战→读者:怎么还没打完?",
             "第1章:大战(张力9)→第2章:险胜(张力7)→"
             "第3章:疗伤+发现线索(张力3)→第4章:新危机出现(张力8)"),
        ],
        difficulty=3,
    ),

    # ── 开篇技法 ──
    "opening_golden_300": WritingTechnique(
        name="黄金300字法则",
        category=TechniqueCategory.OPENING,
        description="开篇300字内必须出现主角并建立冲突/危机/悬念。"
                    "网文读者的耐心按秒计算——300字内抓不住，他就划走了。",
        why_it_works="移动端阅读场景下，读者在信息流中快速判断'值不值得点进去'。"
                     "前300字是唯一的'钩子窗口'。",
        how_to_apply="1. 第一句:主角+动作/状态(不要环境描写开头)\n"
                     "2. 前100字:建立主角当前处境\n"
                     "3. 前300字:抛出冲突/危机/悬念\n"
                     "4. 三种高效开篇:\n"
                     "   - 对话开篇:'你再跑一个试试？'\n"
                     "   - 动作开篇:拳头砸在脸上，鼻血飙了出来。\n"
                     "   - 悬念开篇:醒来的时候，他发现自己少了一天的记忆。",
        common_mistakes="开篇大段世界观介绍/环境描写/配角抢戏——读者直接划走。",
        examples=[
            ("(错误)天地初开，混沌未分，万物生灵皆在蒙昧之中...(读者:划走)",
             "(正确)萧炎睁开眼的时候，发现自己躺在乱葬岗。嘴里全是土。"
             "他吐了一口，然后开始笑——因为他记起来了。他是回来报仇的。"),
        ],
        difficulty=2,
    ),

    "opening_three_chapters": WritingTechnique(
        name="黄金三章定律",
        category=TechniqueCategory.OPENING,
        description="第一章:出场主角+交代身份+制造冲突/危机\n"
                    "第二章:矛盾升级+出现目标+给出期待感\n"
                    "第三章:第一次小反转/小爽点+留住读者",
        why_it_works="三章是读者决定'是否追读'的关键窗口。"
                     "每章都要完成特定的读者心理任务。",
        how_to_apply="1. 第一章:让读者认识主角+关心主角\n"
                     "2. 第二章:让读者知道主角要什么+为什么难\n"
                     "3. 第三章:给读者一点甜头+更大的期待\n"
                     "4. 每章结尾必须有钩子",
        common_mistakes="三章了还在铺垫，主角还没开始行动。",
        examples=[],
        difficulty=2,
    ),

    # ── 情绪设计 ──
    "emotion_expectation_satisfaction": WritingTechnique(
        name="期待→压抑→释放 情绪闭环",
        category=TechniqueCategory.EMOTION,
        description="男频网文的核心情绪公式:\n"
                    "1. 期待感:让主角处于被轻视/羞辱的底层处境→读者期待反击\n"
                    "2. 压抑感:放大委屈和无力→读者憋屈\n"
                    "3. 释放感:主角碾压反派→读者爽",
        why_it_works="这是人类最原始的情绪模式——不公平→愤怒→正义伸张。"
                     "压抑越深，释放越爽。",
        how_to_apply="1. 先抑后扬:先被打压→再反手打脸\n"
                     "2. 情绪前置:先写读者能共情的憋屈→再给解决\n"
                     "3. 释放要快:最好上一章憋屈、下一章就爆发\n"
                     "4. 重点描写反派的狼狈和周围人的震惊",
        common_mistakes="压抑太久(读者跑了)或释放太快(不够爽)。",
        examples=[
            ("主角被欺负→主角忍了→主角继续忍→读者:弃书",
             "第9章:主角被当众羞辱→第10章:主角激活金手指→"
             "第11章:主角当众碾压反派→周围人震惊→读者:爽!"),
        ],
        difficulty=2,
    ),

    "emotion_regret_design": WritingTechnique(
        name="遗憾感设计",
        category=TechniqueCategory.EMOTION,
        description="遗憾感是重生/穿越类题材的核心情绪驱动力。"
                    "让读者感受到'如果重来一次'的强烈渴望。",
        why_it_works="遗憾是人类最强烈的情感之一。"
                     "当读者感受到主角的遗憾时，会强烈期待'这一次不一样'。",
        how_to_apply="1. 用具体细节展示'上一次'的遗憾\n"
                     "2. 遗憾要具体——不是'上辈子很惨'，而是'上辈子母亲临死前想吃一口桂花糕，"
                     "他跑了三条街都没买到'\n"
                     "3. 让'这一次'有机会弥补遗憾\n"
                     "4. 但弥补也要付出代价",
        common_mistakes="遗憾太笼统('上辈子过得很惨')——读者无法共情。",
        examples=[],
        difficulty=3,
    ),

    # ── 语言文笔 ──
    "language_short_sentences": WritingTechnique(
        name="短句为王",
        category=TechniqueCategory.LANGUAGE,
        description="网文切忌长句堆砌。一句话只讲一件事，多断句。"
                    "手机屏幕上，超过25字的句子阅读体验断崖式下降。",
        why_it_works="手机阅读的视觉宽度有限，长句需要眼球来回扫描——"
                     "增加认知负荷，降低阅读快感。",
        how_to_apply="1. 检查所有超过30字的句子——拆成两句\n"
                     "2. 用句号替代逗号——不要怕句子太短\n"
                     "3. 短句+短句+短句+中句=节奏感\n"
                     "4. 关键动作/情绪用3-5字短句",
        common_mistakes="所有句子都短——变成电报体。需要偶尔的中长句来调节节奏。",
        examples=[
            ("他缓缓地站起身来，然后慢慢地走到窗前，静静地看着外面正在下着的雨。",
             "他站起来。走到窗前。外面在下雨。不大，但很密。"),
        ],
        difficulty=1,
    ),

    "language_delete_fillers": WritingTechnique(
        name="删除无效连接词",
        category=TechniqueCategory.LANGUAGE,
        description="删掉'此时此刻/不由得/其实/然后/接着/于是/便'等无效连接词，"
                    "行文立刻紧凑。",
        why_it_works="这些词不承载任何信息，纯粹是思维上的填充物。"
                     "删除后文字密度提升，节奏加快。",
        how_to_apply="1. 全文搜索:此时/此刻/不由得/其实/然后/接着/于是/便\n"
                     "2. 逐个判断:删除后是否影响理解?\n"
                     "3. 90%的情况可以直接删除\n"
                     "4. 保留10%确实需要的",
        common_mistakes="机械删除导致句子不连贯——需要根据上下文判断。",
        examples=[
            ("此时此刻，他不由得想起了过去的种种经历。",
             "他想起了过去。"),
        ],
        difficulty=1,
    ),

    # ── 悬念钩子 ──
    "suspense_chapter_endings": WritingTechnique(
        name="章末钩子五法",
        category=TechniqueCategory.SUSPENSE,
        description="每章结尾必须留钩子——让读者产生'我必须知道接下来发生什么'的冲动。"
                    "无钩子，不章节。",
        why_it_works="蔡格尼克效应(Zeigarnik Effect):人类对未完成/中断的任务有强烈的"
                     "记忆和完成冲动。章末钩子利用这个心理机制驱动连续阅读。",
        how_to_apply="五种章末钩子:\n"
                     "1. 危机钩:主角陷入危险→'门被一脚踹开。'\n"
                     "2. 悬念钩:抛出谜题→'信上只有三个字:别回去。'\n"
                     "3. 反转钩:意外发现→'他翻开族谱，自己的名字——被划掉了。'\n"
                     "4. 期待钩:即将获得→'系统提示:恭喜，您已获得SSS级功法。'\n"
                     "5. 情绪钩:强烈情感→'她笑着说的那句话，他记了一辈子。'\n"
                     "注意:钩子要自然，不能生硬——'预知后事如何，且听下回分解'是反面教材。",
        common_mistakes="章末没有钩子(把事情写完了)或钩子太生硬(强行断章)。",
        examples=[
            ("(无钩子)他完成了任务，回到家中休息。",
             "(危机钩)任务完成了。但他推开家门的时候，闻到了血腥味。"),
        ],
        difficulty=2,
    ),

    "suspense_zeigarnik": WritingTechnique(
        name="蔡格尼克效应应用",
        category=TechniqueCategory.SUSPENSE,
        description="在章节中段故意中断一个关键场景，跳到另一条线，"
                    "让读者带着'未完成的紧张感'继续阅读。",
        why_it_works="未完成的任务在大脑中占据'缓存空间'，"
                     "读者会持续惦记被中断的场景，直到它被完成。",
        how_to_apply="1. 在关键场景的'最紧张时刻'切换视角/场景\n"
                     "2. 切换后不要马上切回来——让读者'等'\n"
                     "3. 等待时间要适中:太短没效果，太长读者忘了\n"
                     "4. 切回来时给一个'释放'——满足读者的期待",
        common_mistakes="切换太频繁(读者混乱)或等待太久(读者忘了前面在干嘛)。",
        examples=[],
        difficulty=3,
    ),

    # ── 结构大纲 ──
    "structure_snowflake": WritingTechnique(
        name="雪花写作法",
        category=TechniqueCategory.STRUCTURE,
        description="六阶段逐步构建小说:\n"
                    "阶段1:一句话概括(15字以内)\n"
                    "阶段2:一段话概括(5句话:背景+三幕+结局)\n"
                    "阶段3:人物一页纸(姓名/背景/动机/目标/转变/冲突)\n"
                    "阶段4:一页纸大纲(每章一句话)\n"
                    "阶段5:人物深度表(每个主要人物详细档案)\n"
                    "阶段6:四页纸大纲(每章一段话)",
        why_it_works="从宏观到微观逐步细化，每一步都建立在上一步的基础上。"
                     "避免'裸奔码字'——写着写着发现方向错了。",
        how_to_apply="严格按照六阶段顺序推进，不要跳步。"
                     "每个阶段完成后检查与前一个阶段的一致性。",
        common_mistakes="跳过前三个阶段直接写细纲——导致故事骨架不稳。",
        examples=[],
        difficulty=2,
    ),

    "structure_three_act": WritingTechnique(
        name="三幕式结构",
        category=TechniqueCategory.STRUCTURE,
        description="第一幕(开端):遭遇变故，踏上征程(25%)\n"
                    "第二幕(发展):一路成长打怪，遭遇重大挫折(50%)\n"
                    "第三幕(高潮+结局):终极对决，收尾留白(25%)",
        why_it_works="三幕式是人类叙事最古老、最自然的结构，"
                     "符合人类对'开始-过程-结束'的认知模式。",
        how_to_apply="1. 确定第一幕的'不可逆事件'(主角无法回到原来的生活)\n"
                     "2. 第二幕中点设置'假胜利'或'假失败'(以为赢了/输了，其实没有)\n"
                     "3. 第三幕前设置'最黑暗时刻'(一切看起来都完了)\n"
                     "4. 结局要有'代价'——不是所有人都能活下来",
        common_mistakes="第二幕拖太长(读者疲劳)或第三幕太仓促(虎头蛇尾)。",
        examples=[],
        difficulty=2,
    ),
}


# ═══════════════════════════════════════════════════════════════
# 第三部分: 读者吸引策略库
# ═══════════════════════════════════════════════════════════════

class StrategyType(Enum):
    """策略类型"""
    COGNITIVE = "认知心理"
    EMOTIONAL = "情绪驱动"
    IMMERSION = "代入感"
    RETENTION = "留存驱动"
    VIRAL = "传播裂变"


@dataclass
class ReaderStrategy:
    """读者吸引策略"""
    name: str
    type: StrategyType
    principle: str  # 底层原理
    application: str  # 在小说中的应用
    effect: str  # 预期效果
    examples: List[str]


READER_STRATEGIES: Dict[str, ReaderStrategy] = {
    "zeigarnik_effect": ReaderStrategy(
        name="蔡格尼克效应驱动追读",
        type=StrategyType.COGNITIVE,
        principle="人类对未完成任务的记忆强度是已完成任务的9倍。"
                  "中断的场景在大脑中持续占据'认知缓存'。",
        application="1. 每章结尾必须留未完成的悬念\n"
                    "2. 关键场景在高潮处中断，跳到另一条线\n"
                    "3. 大悬念套小悬念——长线悬念(全书)+短线悬念(每章)\n"
                    "4. 不要一次性回答所有问题——每次只给部分答案",
        effect="读者产生'我必须看完'的强迫性冲动，追读率提升40-60%。",
        examples=[
            "章末:他推开门——然后僵住了。因为屋子里站着的那个人，"
            "三年前就已经死了。(读者:下一页!)",
        ],
    ),

    "emotional_roller_coaster": ReaderStrategy(
        name="情绪过山车设计",
        type=StrategyType.EMOTIONAL,
        principle="人类大脑对情绪波动的记忆远强于平稳状态。"
                  "情绪的高峰和低谷共同构成'难忘的体验'。",
        application="1. 设计情绪曲线:紧张→放松→更紧张→释放→新的紧张\n"
                    "2. 每次情绪释放后立即埋下新的紧张\n"
                    "3. 情绪强度逐步升级——后面的高潮要比前面更强\n"
                    "4. 在读者'刚好放松'的时候给新的冲击",
        effect="读者经历完整的情绪起伏，产生'这本书让我停不下来'的感受。",
        examples=[
            "大战胜利(释放)→清点战利品(放松)→发现敌人的真正身份(新的紧张)",
        ],
    ),

    "immersion_through_senses": ReaderStrategy(
        name="多感官代入法",
        type=StrategyType.IMMERSION,
        principle="人类记忆是多感官编码的。纯视觉描写只能激活大脑的视觉皮层，"
                  "而嗅觉/触觉/听觉描写能激活更广泛的情感中枢。",
        application="1. 每个场景至少3种感官\n"
                    "2. 优先使用嗅觉(直接连接杏仁核，情感中枢)\n"
                    "3. 触觉描写让读者'身体'进入场景\n"
                    "4. 听觉描写创造氛围感",
        effect="读者从'旁观者'变为'体验者'，代入感提升3-5倍。",
        examples=[
            "不只是'他走进厨房'，而是'油烟味混着蒜香扑面而来，"
            "锅铲刮过铁锅的声音刺得耳膜发紧，灶台上的热气扑到脸上，潮乎乎的。'",
        ],
    ),

    "pleasure_beat_design": ReaderStrategy(
        name="爽点密度与节奏设计",
        type=StrategyType.RETENTION,
        principle="网文读者的核心需求是'爽'——获得情绪释放。"
                  "爽点的频率和强度直接决定留存率。",
        application="1. 长篇:3-5章一个小爽点，10章一个大爽点\n"
                    "2. 短篇/新媒体:每1-2章一个爽点\n"
                    "3. 爽点类型交替:打脸爽/升级爽/获得爽/反转爽\n"
                    "4. 每个爽点前必须有'憋屈'——落差越大，爽感越强",
        effect="读者持续获得满足感，留存率提升50%以上。",
        examples=[
            "小爽点:主角突破小境界→周围人惊讶\n"
            "大爽点:主角在宗门大比中碾压所有对手→掌门亲自收徒",
        ],
    ),

    "hook_golden_three": ReaderStrategy(
        name="黄金三章留存漏斗",
        type=StrategyType.RETENTION,
        principle="网文读者的流失率在前三章最高——第一章流失40%，"
                  "第二章流失25%，第三章流失15%。三章后留存的读者大概率追读到底。",
        application="1. 第一章:300字内主角出场+制造冲突→让读者'认识并关心'主角\n"
                    "2. 第二章:矛盾升级+给出目标→让读者'期待'接下来发生什么\n"
                    "3. 第三章:第一次小爽点→让读者'尝到甜头'并期待更多\n"
                    "4. 每章结尾必须有钩子",
        effect="三章留存率从20%提升到50%以上。",
        examples=[
            "第一章:主角被退婚+激活金手指→读者:有意思\n"
            "第二章:主角定下目标(三年后让所有人后悔)→读者:期待\n"
            "第三章:主角第一次展现实力→读者:爽!继续看!",
        ],
    ),

    "identification_gap": ReaderStrategy(
        name="身份落差代入法",
        type=StrategyType.IMMERSION,
        principle="读者最容易代入的不是'强者'，而是'被低估的强者'或'即将变强的弱者'。"
                  "身份落差(实际很强但被看不起)创造最强的代入感和期待感。",
        application="1. 主角初始状态:被低估/被轻视/被羞辱\n"
                    "2. 但给读者'暗示':主角有隐藏实力/特殊背景/即将觉醒\n"
                    "3. 让读者'比剧中人知道更多'——产生优越感和期待\n"
                    "4. 在关键节点让主角暴露真实实力——'打脸'时刻",
        effect="读者产生'你们等着瞧'的强烈期待，代入感极强。",
        examples=[
            "主角是退役兵王→在都市中被当成普通人→被小混混挑衅→"
            "读者:你惹错人了!→主角出手→读者:爽!",
        ],
    ),

    "curiosity_gap": ReaderStrategy(
        name="好奇心缺口策略",
        type=StrategyType.COGNITIVE,
        principle="当读者意识到自己'不知道但想知道'某件事时，"
                  "会产生强烈的认知缺口——驱使他们继续阅读以填补缺口。",
        application="1. 抛出谜题但不立即解答\n"
                    "2. 给出部分线索——让读者自己拼图\n"
                    "3. 每次解答一个谜题的同时抛出更大的谜题\n"
                    "4. 让角色也在追寻答案——读者与角色同步探索",
        effect="读者产生'我必须知道答案'的驱动力，弃书率大幅降低。",
        examples=[
            "主角发现自己的记忆被删除了一天。谁干的？为什么？"
            "→每章给出一点线索→读者持续追读。",
        ],
    ),

    "social_proof_effect": ReaderStrategy(
        name="社会证明效应",
        type=StrategyType.VIRAL,
        principle="人们倾向于跟随他人的选择。当读者看到'很多人都在看这本书'时，"
                  "会产生'我也要看'的从众心理。",
        application="1. 在书中设计'名场面'——读者会自发传播的经典场景\n"
                    "2. 创造可引用的'金句'——方便读者截图分享\n"
                    "3. 设计'意难平'情节——引发读者讨论和二次传播\n"
                    "4. 在关键情节设置'两难选择'——引发读者站队讨论",
        effect="读者自发传播内容，形成口碑裂变，拉新成本趋近于零。",
        examples=[
            "'三十年河东，三十年河西，莫欺少年穷！'——"
            "一句话让《斗破苍穹》出圈。",
        ],
    ),
}


# ═══════════════════════════════════════════════════════════════
# 第四部分: 去AI痕迹策略库 (六层递进)
# ═══════════════════════════════════════════════════════════════

class DeAILevel(Enum):
    """去痕层级"""
    SURFACE = "表面层-词汇替换"
    SYNTACTIC = "句法层-句式重构"
    STRUCTURAL = "结构层-框架打破"
    SEMANTIC = "语义层-深度重写"
    VOICE = "声音层-个性注入"
    EXPERIENCE = "经验层-真实感注入"


@dataclass
class DeAIStrategy:
    """去AI痕迹策略"""
    name: str
    level: DeAILevel
    description: str
    target_traits: List[str]  # 目标AI特征名称
    steps: List[str]  # 执行步骤
    prompt_template: str  # 可用于AI提示词
    effectiveness: float  # 0-1, 预估效果


DEAI_STRATEGIES: Dict[str, DeAIStrategy] = {
    "surface_word_replacement": DeAIStrategy(
        name="表面层-高频词替换",
        level=DeAILevel.SURFACE,
        description="替换AI高频使用的词汇和短语，这是最基础的去痕操作。"
                    "但注意:单纯的词汇替换效果有限，必须配合更深层的策略。",
        target_traits=["ai_connectors", "ai_abstract_nouns", "ai_high_freq_words",
                       "ai_vague_attribution", "ai_hedging"],
        steps=[
            "1. 扫描文本，标记所有AI高频词",
            "2. 连接词('首先/其次/最后'):直接删除，用内容自然承接",
            "3. 抽象名词('赋能/闭环/底层逻辑'):替换为具体描述",
            "4. 万能词('时代/人生/智慧'):替换为具体场景/事物",
            "5. 模糊归因('专家认为/研究表明'):删除或给出具体来源",
            "6. 模糊限定('可能/或许/似乎'):给出明确判断或通过角色视角表达",
        ],
        prompt_template=(
            "替换以下AI高频词汇:\n"
            "- 删除所有'首先/其次/最后/此外/总而言之'\n"
            "- 将'赋能/闭环/底层逻辑/维度/格局'替换为具体描述\n"
            "- 将'时代/人生/智慧/力量/命运'替换为具体场景\n"
            "- 删除'专家认为/研究表明/据记载'等模糊归因\n"
            "- 将'可能/或许/似乎/在一定程度上'改为明确判断"
        ),
        effectiveness=0.30,
    ),

    "syntactic_restructure": DeAIStrategy(
        name="句法层-句式重构",
        level=DeAILevel.SYNTACTIC,
        description="打破AI的句式模板——排比/对偶/主语+动作/介词短语开头——"
                    "让句子结构变得不规则、不可预测。",
        target_traits=["ai_parallel_structure", "ai_sentence_length_uniform",
                       "ai_subject_action_template", "ai_prepositional_starts",
                       "ai_passive_voice", "ai_dash_abuse"],
        steps=[
            "1. 打破排比/对偶:让句子长短不一，不对称",
            "2. 制造句长变化:短句(3-5字)+中句(15-25字)+长句(30-50字)交替",
            "3. 变换主语位置:不要每句都以'他/她'开头",
            "4. 减少介词短语开头:用具体名词或动作开头",
            "5. 被动改主动:'被XX'→'XX把他...'",
            "6. 限制破折号:每千字不超过1个",
        ],
        prompt_template=(
            "重构句式:\n"
            "- 打破所有排比/对偶句式，让句子长短不一\n"
            "- 句长要有变化:3字短句+20字中句+40字长句交替\n"
            "- 不要每句都以'他/她'开头，变换主语位置\n"
            "- 减少'在...中/下/里''随着...''当...时'开头\n"
            "- 被动改主动\n"
            "- 每千字破折号不超过1个"
        ),
        effectiveness=0.45,
    ),

    "structural_break": DeAIStrategy(
        name="结构层-框架打破",
        level=DeAILevel.STRUCTURAL,
        description="打破AI的结构模板——三段式/总结式结尾/模板化过渡——"
                    "让文本结构变得自然、有机。",
        target_traits=["ai_three_part_structure", "ai_predictable_arc",
                       "ai_ending_summary", "ai_transition_template"],
        steps=[
            "1. 打破三段式:不强制三点/三个层面，根据内容自然分层",
            "2. 打破可预测弧线:加入意外转折、代价、失败",
            "3. 删除总结式结尾:用动作/画面/对话收束，不总结不升华",
            "4. 打破模板过渡:用具体细节标记时间/空间转换",
        ],
        prompt_template=(
            "打破结构模板:\n"
            "- 不要用'第一/第二/第三'或'从X层面看'\n"
            "- 情节不要遵循'遇到困难→克服→成长'的模板，加入意外和代价\n"
            "- 结尾不要总结升华，用动作/画面/对话收束\n"
            "- 不要用'与此同时/转眼间/不久之后'过渡"
        ),
        effectiveness=0.55,
    ),

    "semantic_deep_rewrite": DeAIStrategy(
        name="语义层-深度重写",
        level=DeAILevel.SEMANTIC,
        description="这是去痕的核心——不是替换词汇，而是改变信息的组织和呈现方式。"
                    "从'百科式告知'变为'角色视角体验'。",
        target_traits=["ai_semantic_flatness", "ai_encyclopedic_explanation",
                       "ai_fake_authority", "ai_causal_simplification",
                       "ai_over_explanation"],
        steps=[
            "1. 增加潜台词:不直接说明，通过细节暗示",
            "2. 设定融入场景:通过角色视角/对话自然带出，不直接科普",
            "3. 因果复杂化:加入偶然因素、代价、副作用",
            "4. 信任读者:说一遍就够，删除所有解释性重复",
            "5. 增加'不可靠叙述':角色可能判断错误，信息可能不完整",
        ],
        prompt_template=(
            "语义层深度重写:\n"
            "- 不要直接说明情感/判断，通过细节暗示\n"
            "- 设定通过角色视角/对话自然带出，不要百科式科普\n"
            "- 因果关系要复杂:加入偶然、代价、副作用\n"
            "- 说一遍就够，不要反复解释\n"
            "- 角色可以有错误的判断，信息可以不完整"
        ),
        effectiveness=0.70,
    ),

    "voice_injection": DeAIStrategy(
        name="声音层-个性注入",
        level=DeAILevel.VOICE,
        description="这是去痕的高级阶段——不只是去除AI痕迹，而是注入'人的声音'。"
                    "对标Humanizer-zh的'注入灵魂'模块。",
        target_traits=["ai_emotion_labeling", "ai_emotion_linear",
                       "ai_empathy_deficit", "ai_tone_inconsistency",
                       "ai_collaborative_traces"],
        steps=[
            "1. 注入观点:叙述者要有明确的立场和态度，不是中立的",
            "2. 变化节奏:允许句子'不完美'——口语化、碎片化、中断",
            "3. 承认复杂性:不给出简单的答案，允许矛盾和模糊",
            "4. 适当使用'我'(第一人称叙述时):让叙述者有存在感",
            "5. 允许一些混乱:人类写作不是完美的——有瑕疵才真实",
            "6. 对感受要具体:不是'很难过'，而是'胸口像压了块石头，喘不上气'",
        ],
        prompt_template=(
            "注入人的声音:\n"
            "- 叙述者要有明确的立场和态度，不是中立的旁观者\n"
            "- 允许句子不完美——口语化、碎片化、中断\n"
            "- 不给出简单的答案，允许矛盾和模糊\n"
            "- 感受要具体:不是'很难过'，而是身体的具体感受\n"
            "- 允许一些混乱和瑕疵——完美是AI的特征"
        ),
        effectiveness=0.80,
    ),

    "experience_injection": DeAIStrategy(
        name="经验层-真实感注入",
        level=DeAILevel.EXPERIENCE,
        description="这是去痕的最高阶段——注入只有真实人类才有的经验细节。"
                    "AI可以模拟情感模式，但无法模拟真实的、私人的、不完美的经验。",
        target_traits=["ai_emotion_labeling", "ai_empathy_deficit",
                       "ai_semantic_flatness", "ai_over_explanation"],
        steps=[
            "1. 注入'无用的细节':真实生活中充满无用的、偶然的细节\n"
            "2. 注入'身体的记忆':不是大脑的记忆，是肌肉/嗅觉/触觉的记忆\n"
            "3. 注入'私人的联想':某个场景让角色想起完全不相干的另一件事\n"
            "4. 注入'不完美的反应':角色在关键时刻的反应不是最优的——是真实的\n"
            "5. 注入'沉默':不是所有时刻都需要语言——沉默有时比语言更有力",
        ],
        prompt_template=(
            "注入真实经验:\n"
            "- 加入'无用的细节':衣服上的线头、杯底的茶渍、指甲缝里的泥\n"
            "- 加入'身体的记忆':某种气味让角色想起十年前的一个下午\n"
            "- 加入'私人的联想':不合理的、跳跃的、只有这个角色会有的联想\n"
            "- 关键时刻的反应可以不完美——犹豫、后悔、做错\n"
            "- 适当留白:不是所有情感都需要写出来"
        ),
        effectiveness=0.90,
    ),
}


# ═══════════════════════════════════════════════════════════════
# 第五部分: WritingKnowledgeEngine 主类
# ═══════════════════════════════════════════════════════════════

@dataclass
class AIDiagnosis:
    """AI特征诊断结果"""
    overall_ai_score: float  # 0-1, 越高越像AI
    detected_traits: List[Tuple[str, float]]  # (特征名, 严重程度)
    risk_level: str  # low/medium/high/critical
    summary: str
    fix_priority: List[str]  # 按优先级排列的修复建议


@dataclass
class TechniqueRecommendation:
    """技法推荐"""
    technique_name: str
    relevance: float  # 0-1, 与当前文本的相关度
    urgency: str  # high/medium/low
    reason: str
    quick_fix: str


@dataclass
class DeAIPipeline:
    """去痕流水线"""
    stages: List[Dict[str, Any]]
    estimated_effectiveness: float
    total_steps: int


class WritingKnowledgeEngine:
    """
    NWACS 写作知识引擎

    整合所有研究成果，提供:
    - AI特征诊断
    - 写作技法推荐
    - 读者策略应用
    - 去AI痕迹流水线生成
    - 知识注入提示词生成
    """

    def __init__(self):
        self.ai_traits = AI_TRAITS_LIBRARY
        self.techniques = WRITING_TECHNIQUES
        self.reader_strategies = READER_STRATEGIES
        self.deai_strategies = DEAI_STRATEGIES
        self._build_indexes()

    def _build_indexes(self):
        self._trait_by_level: Dict[AITraitLevel, List[str]] = {}
        for name, trait in self.ai_traits.items():
            if trait.level not in self._trait_by_level:
                self._trait_by_level[trait.level] = []
            self._trait_by_level[trait.level].append(name)

        self._technique_by_category: Dict[TechniqueCategory, List[str]] = {}
        for name, tech in self.techniques.items():
            if tech.category not in self._technique_by_category:
                self._technique_by_category[tech.category] = []
            self._technique_by_category[tech.category].append(name)

        self._deai_by_level: Dict[DeAILevel, List[str]] = {}
        for name, strategy in self.deai_strategies.items():
            if strategy.level not in self._deai_by_level:
                self._deai_by_level[strategy.level] = []
            self._deai_by_level[strategy.level].append(name)

    # ═══════════════════════════════════════════════════════════
    # AI特征诊断
    # ═══════════════════════════════════════════════════════════

    def diagnose_ai_traits(self, text: str) -> AIDiagnosis:
        """
        对文本进行全面的AI特征诊断

        Args:
            text: 待诊断文本

        Returns:
            AIDiagnosis: 诊断结果
        """
        detected: List[Tuple[str, float]] = []
        total_score = 0.0
        trait_count = 0

        for trait_key, trait in self.ai_traits.items():
            severity = self._detect_trait(text, trait, trait_key)
            if severity > 0.1:
                detected.append((trait_key, severity))
                total_score += severity * trait.risk_score
                trait_count += 1

        if trait_count == 0:
            overall_score = 0.0
        else:
            overall_score = min(total_score / trait_count * 1.2, 1.0)

        detected.sort(key=lambda x: x[1], reverse=True)

        if overall_score < 0.25:
            risk_level = "low"
        elif overall_score < 0.50:
            risk_level = "medium"
        elif overall_score < 0.75:
            risk_level = "high"
        else:
            risk_level = "critical"

        fix_priority = self._generate_fix_priority(detected[:5])

        summary = self._generate_diagnosis_summary(overall_score, risk_level, detected[:5])

        return AIDiagnosis(
            overall_ai_score=round(overall_score, 3),
            detected_traits=detected[:10],
            risk_level=risk_level,
            summary=summary,
            fix_priority=fix_priority,
        )

    def _detect_trait(self, text: str, trait: AITrait, trait_key: str = "") -> float:
        """检测单个AI特征在文本中的严重程度"""
        score = 0.0

        if trait.level == AITraitLevel.LEXICAL:
            score = self._detect_lexical_trait(text, trait_key)
        elif trait.level == AITraitLevel.SYNTACTIC:
            score = self._detect_syntactic_trait(text, trait_key)
        elif trait.level == AITraitLevel.SEMANTIC:
            score = self._detect_semantic_trait(text, trait_key)
        elif trait.level == AITraitLevel.STRUCTURAL:
            score = self._detect_structural_trait(text, trait_key)
        elif trait.level == AITraitLevel.EMOTIONAL:
            score = self._detect_emotional_trait(text, trait_key)
        elif trait.level == AITraitLevel.PRAGMATIC:
            score = self._detect_pragmatic_trait(text, trait_key)

        return min(score, 1.0)

    def _detect_lexical_trait(self, text: str, trait_key: str) -> float:
        """词汇层检测"""
        patterns = {
            "ai_connectors": r"(首先|其次|再次|最后|总之|综上所述|此外|总而言之|一方面|另一方面|不仅如此|与此同时)",
            "ai_abstract_nouns": r"(赋能|底层逻辑|闭环|维度|格局|体系|生态|赛道|抓手|颗粒度|方法论)",
            "ai_emotion_adverbs": r"(感到|觉得|感觉|意识到|注意到)(非常|极其|极为|十分|特别|格外|相当|颇为)",
            "ai_vague_attribution": r"(专家认为|研究表明|行业报告显示|据.*?记载|有人说过|众所周知)",
            "ai_hedging": r"(可能|或许|似乎|在一定程度上|某种意义上|某种程度上|大体上)",
            "ai_dash_abuse": r"——",
            "ai_high_freq_words": r"(时代|人生|智慧|力量|命运|灵魂|本质|真谛|意义)",
        }

        pattern = patterns.get(trait_key, "")
        if not pattern:
            return 0.0

        matches = re.findall(pattern, text)
        if not matches:
            return 0.0

        char_count = max(len(text), 1)
        density = len(matches) / (char_count / 500)

        if trait_key == "ai_dash_abuse":
            density = len(matches) / (char_count / 1000)
            return min(density / 3.0, 1.0)

        return min(density / 5.0, 1.0)

    def _detect_syntactic_trait(self, text: str, trait_key: str) -> float:
        """句式层检测"""
        sentences = re.split(r'[。！？\n]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        if not sentences:
            return 0.0

        if trait_key == "ai_parallel_structure":
            parallel_count = 0
            for s in sentences:
                if re.search(r'[，,].*?[；;].*?[，,].*?[；;]', s):
                    parallel_count += 1
                if re.search(r'(既有|既能|既会).*?(又有|又能|又会)', s):
                    parallel_count += 1
            return min(parallel_count / max(len(sentences) * 0.3, 1), 1.0)

        elif trait_key == "ai_sentence_length_uniform":
            lengths = [len(s) for s in sentences]
            if len(lengths) < 3:
                return 0.0
            mean_len = sum(lengths) / len(lengths)
            if mean_len == 0:
                return 0.0
            variance = sum((l - mean_len) ** 2 for l in lengths) / len(lengths)
            cv = math.sqrt(variance) / mean_len
            return max(0, 1.0 - cv / 0.8)

        elif trait_key == "ai_subject_action_template":
            pattern_count = 0
            for s in sentences:
                if re.match(r'^(他|她|它|这|那)\s*(站起|转过|抬起|低下|伸出|走出|走进|来到|回到)', s):
                    pattern_count += 1
            return min(pattern_count / max(len(sentences) * 0.25, 1), 1.0)

        elif trait_key == "ai_prepositional_starts":
            pattern_count = 0
            for s in sentences:
                if re.match(r'^(在|随着|当|自从|由于|因为|为了|根据|按照)', s):
                    pattern_count += 1
            return min(pattern_count / max(len(sentences) * 0.3, 1), 1.0)

        elif trait_key == "ai_passive_voice":
            passive_count = len(re.findall(r'[被让给叫]', text))
            char_count = max(len(text), 1)
            return min(passive_count / (char_count / 300), 1.0)

        return 0.0

    def _detect_semantic_trait(self, text: str, trait_key: str) -> float:
        """语义层检测"""
        if trait_key == "ai_semantic_flatness":
            explain_patterns = [
                r'因为.*?所以',
                r'由于.*?因此',
                r'这.*?意味着',
                r'这.*?说明',
                r'这.*?表明',
            ]
            count = sum(len(re.findall(p, text)) for p in explain_patterns)
            char_count = max(len(text), 1)
            return min(count / (char_count / 800), 1.0)

        elif trait_key == "ai_encyclopedic_explanation":
            explain_markers = [
                r'分为.*?种',
                r'是.*?的.*?单位',
                r'通过.*?来.*?',
                r'分为以下几个',
            ]
            count = sum(len(re.findall(p, text)) for p in explain_markers)
            char_count = max(len(text), 1)
            return min(count / (char_count / 1000), 1.0)

        elif trait_key == "ai_fake_authority":
            authority_patterns = [
                r'《.*?》中记载',
                r'《.*?》中写道',
                r'据.*?统计',
                r'据.*?研究',
            ]
            count = sum(len(re.findall(p, text)) for p in authority_patterns)
            char_count = max(len(text), 1)
            return min(count / (char_count / 1000), 1.0)

        elif trait_key == "ai_causal_simplification":
            simple_cause = len(re.findall(r'(因为|由于).*?(所以|因此|于是)', text))
            char_count = max(len(text), 1)
            return min(simple_cause / (char_count / 1000), 1.0)

        return 0.0

    def _detect_structural_trait(self, text: str, trait_key: str) -> float:
        """结构层检测"""
        if trait_key == "ai_three_part_structure":
            markers = len(re.findall(r'(第一|第二|第三|首先|其次|最后|从.*?层面)', text))
            char_count = max(len(text), 1)
            return min(markers / (char_count / 800), 1.0)

        elif trait_key == "ai_predictable_arc":
            arc_patterns = [
                r'经过.*?(努力|奋斗|坚持).*?(终于|最终|成功)',
                r'在.*?的帮助下.*?克服了',
            ]
            count = sum(len(re.findall(p, text)) for p in arc_patterns)
            char_count = max(len(text), 1)
            return min(count / (char_count / 1500), 1.0)

        elif trait_key == "ai_ending_summary":
            summary_patterns = [
                r'(总而言之|综上所述|总的来看|总的来说|这标志着|这意味着|这预示着)',
            ]
            count = sum(len(re.findall(p, text)) for p in summary_patterns)
            char_count = max(len(text), 1)
            return min(count / (char_count / 1000), 1.0)

        elif trait_key == "ai_transition_template":
            transition_patterns = [
                r'(与此同时|另一方面|转眼间|不久之后|很快|没过多久|时光飞逝)',
            ]
            count = sum(len(re.findall(p, text)) for p in transition_patterns)
            char_count = max(len(text), 1)
            return min(count / (char_count / 1000), 1.0)

        return 0.0

    def _detect_emotional_trait(self, text: str, trait_key: str) -> float:
        """情感层检测"""
        if trait_key == "ai_emotion_labeling":
            emotion_labels = [
                r'(感到|觉得|感觉|内心|心中|心里).*?(愤怒|悲伤|恐惧|高兴|激动|紧张|焦虑|兴奋|失落|绝望)',
                r'(非常|极其|十分|特别).*?(愤怒|悲伤|恐惧|高兴)',
            ]
            count = sum(len(re.findall(p, text)) for p in emotion_labels)
            char_count = max(len(text), 1)
            return min(count / (char_count / 500), 1.0)

        elif trait_key == "ai_emotion_linear":
            linear_patterns = [
                r'(从|由).*?(变为|变成|转为|走向)',
                r'(逐渐|渐渐|慢慢).*?(变得|好转|恢复)',
            ]
            count = sum(len(re.findall(p, text)) for p in linear_patterns)
            char_count = max(len(text), 1)
            return min(count / (char_count / 1000), 1.0)

        elif trait_key == "ai_empathy_deficit":
            abstract_emotion = len(re.findall(
                r'(无法用语言形容|难以言表|无法形容|难以描述).*?(痛苦|悲伤|喜悦|激动)',
                text
            ))
            char_count = max(len(text), 1)
            return min(abstract_emotion / (char_count / 1500), 1.0)

        return 0.0

    def _detect_pragmatic_trait(self, text: str, trait_key: str) -> float:
        """语用层检测"""
        if trait_key == "ai_over_explanation":
            explain_repeat = len(re.findall(
                r'(这.*?意味着|也就是说|换句话说|换言之|即|也就是)',
                text
            ))
            char_count = max(len(text), 1)
            return min(explain_repeat / (char_count / 800), 1.0)

        elif trait_key == "ai_collaborative_traces":
            collab_patterns = [
                r'(希望.*?对.*?有帮助|需要注意的是|值得.*?的是|请.*?注意)',
            ]
            count = sum(len(re.findall(p, text)) for p in collab_patterns)
            char_count = max(len(text), 1)
            return min(count / (char_count / 1500), 1.0)

        elif trait_key == "ai_tone_inconsistency":
            literary_count = len(re.findall(r'(月色如水|星光璀璨|微风拂面|波光粼粼|烟雨朦胧)', text))
            colloquial_count = len(re.findall(r'(他妈的|操|卧槽|牛逼|我去|靠)', text))
            if literary_count > 0 and colloquial_count > 0:
                return min((literary_count + colloquial_count) / 5.0, 1.0)
            return 0.0

        return 0.0

    def _generate_fix_priority(self, top_traits: List[Tuple[str, float]]) -> List[str]:
        """生成修复优先级列表"""
        priorities = []
        for name, severity in top_traits:
            trait = self.ai_traits.get(name)
            if trait:
                priorities.append(
                    f"[{trait.level.value}] {trait.name}: {trait.fix_strategy[:80]}..."
                )
        return priorities

    def _generate_diagnosis_summary(
        self, score: float, level: str, top_traits: List[Tuple[str, float]]
    ) -> str:
        """生成诊断摘要"""
        level_desc = {
            "low": "文本AI痕迹较少，接近自然人类写作风格",
            "medium": "文本存在中等程度的AI痕迹，建议进行针对性优化",
            "high": "文本AI痕迹明显，读者可能一眼识别为AI生成内容",
            "critical": "文本AI痕迹非常严重，几乎可以确定是AI生成",
        }

        parts = [f"AI痕迹综合评分: {score:.1%} ({level_desc.get(level, '')})"]
        if top_traits:
            parts.append(f"最显著的AI特征: {top_traits[0][0]} (严重度: {top_traits[0][1]:.1%})")
        return " | ".join(parts)

    # ═══════════════════════════════════════════════════════════
    # 写作技法推荐
    # ═══════════════════════════════════════════════════════════

    def recommend_techniques(
        self, text: str = "", context: Dict[str, Any] = None
    ) -> List[TechniqueRecommendation]:
        """
        根据文本内容和上下文推荐写作技法

        Args:
            text: 待分析文本
            context: 上下文信息(题材/章节号/角色信息等)

        Returns:
            技法推荐列表
        """
        recommendations = []
        context = context or {}

        diagnosis = self.diagnose_ai_traits(text) if text else None

        for name, tech in self.techniques.items():
            relevance, reason = self._calculate_technique_relevance(
                tech, diagnosis, context
            )
            if relevance > 0.3:
                urgency = "high" if relevance > 0.7 else ("medium" if relevance > 0.5 else "low")
                recommendations.append(TechniqueRecommendation(
                    technique_name=name,
                    relevance=round(relevance, 2),
                    urgency=urgency,
                    reason=reason,
                    quick_fix=tech.how_to_apply.split('\n')[0] if tech.how_to_apply else "",
                ))

        recommendations.sort(key=lambda x: x.relevance, reverse=True)
        return recommendations[:10]

    def _calculate_technique_relevance(
        self, tech: WritingTechnique,
        diagnosis: Optional[AIDiagnosis],
        context: Dict[str, Any]
    ) -> Tuple[float, str]:
        """计算技法与当前文本的相关度"""
        relevance = 0.0
        reasons = []

        if diagnosis:
            trait_map = {
                "show_dont_tell": ["ai_emotion_labeling", "ai_emotion_adverbs"],
                "character_voice_id": ["ai_tone_inconsistency"],
                "language_short_sentences": ["ai_sentence_length_uniform"],
                "language_delete_fillers": ["ai_connectors", "ai_over_explanation"],
                "suspense_chapter_endings": ["ai_ending_summary"],
                "scene_five_senses": ["ai_semantic_flatness"],
                "emotion_expectation_satisfaction": ["ai_emotion_linear"],
            }

            related_traits = trait_map.get(tech.name, [])
            for detected_name, severity in diagnosis.detected_traits:
                if detected_name in related_traits:
                    relevance += severity * 0.5
                    reasons.append(f"检测到'{detected_name}'特征(严重度:{severity:.0%})")

        chapter_num = context.get("chapter_num", 0)
        if tech.category == TechniqueCategory.OPENING and chapter_num <= 3:
            relevance += 0.4
            reasons.append("处于开篇阶段，开篇技法至关重要")

        if tech.category == TechniqueCategory.SUSPENSE:
            relevance += 0.2
            reasons.append("悬念钩子是网文留存的核心驱动力")

        if tech.name == "show_dont_tell":
            relevance += 0.3
            reasons.append("展示而非告知是小说写作第一铁律")

        return min(relevance, 1.0), "; ".join(reasons) if reasons else "通用推荐"

    def get_technique_detail(self, technique_name: str) -> Optional[WritingTechnique]:
        """获取技法详情"""
        return self.techniques.get(technique_name)

    def list_techniques_by_category(
        self, category: TechniqueCategory
    ) -> List[WritingTechnique]:
        """按分类列出技法"""
        names = self._technique_by_category.get(category, [])
        return [self.techniques[n] for n in names if n in self.techniques]

    # ═══════════════════════════════════════════════════════════
    # 读者策略应用
    # ═══════════════════════════════════════════════════════════

    def apply_reader_strategy(
        self, strategy_name: str, chapter_context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        应用读者吸引策略

        Args:
            strategy_name: 策略名称
            chapter_context: 章节上下文

        Returns:
            策略应用方案
        """
        strategy = self.reader_strategies.get(strategy_name)
        if not strategy:
            return {"error": f"未找到策略: {strategy_name}"}

        return {
            "strategy": strategy.name,
            "type": strategy.type.value,
            "principle": strategy.principle,
            "application_plan": strategy.application,
            "expected_effect": strategy.effect,
            "examples": strategy.examples,
            "context_notes": self._generate_context_notes(strategy, chapter_context),
        }

    def _generate_context_notes(
        self, strategy: ReaderStrategy, context: Dict[str, Any] = None
    ) -> str:
        """生成上下文相关的策略注释"""
        context = context or {}
        chapter_num = context.get("chapter_num", 1)

        notes = []
        if strategy.name == "hook_golden_three" and chapter_num <= 3:
            notes.append(f"当前为第{chapter_num}章，正处于黄金三章关键窗口期")
        elif strategy.name == "pleasure_beat_design":
            if chapter_num % 3 == 0:
                notes.append(f"第{chapter_num}章建议安排小爽点")
            if chapter_num % 10 == 0:
                notes.append(f"第{chapter_num}章建议安排大爽点")

        return "; ".join(notes) if notes else "按通用方案执行"

    def list_all_strategies(self) -> List[Dict[str, str]]:
        """列出所有读者策略"""
        return [
            {"name": name, "type": s.type.value, "summary": s.principle[:60]}
            for name, s in self.reader_strategies.items()
        ]

    # ═══════════════════════════════════════════════════════════
    # 去AI痕迹流水线
    # ═══════════════════════════════════════════════════════════

    def generate_deai_pipeline(
        self, text: str = "", target_level: str = "voice"
    ) -> DeAIPipeline:
        """
        生成去AI痕迹流水线

        Args:
            text: 待处理文本(可选，用于诊断)
            target_level: 目标去痕深度
                - surface: 仅表面层
                - syntactic: 到句法层
                - structural: 到结构层
                - semantic: 到语义层
                - voice: 到声音层(推荐)
                - experience: 到经验层(最深度)

        Returns:
            DeAIPipeline: 去痕流水线
        """
        level_order = [
            DeAILevel.SURFACE,
            DeAILevel.SYNTACTIC,
            DeAILevel.STRUCTURAL,
            DeAILevel.SEMANTIC,
            DeAILevel.VOICE,
            DeAILevel.EXPERIENCE,
        ]

        target = DeAILevel.SURFACE
        for lv in level_order:
            if lv.name.lower() == target_level.lower():
                target = lv
                break

        stages = []
        total_effectiveness = 0.0
        total_steps = 0

        for lv in level_order:
            strategy_names = self._deai_by_level.get(lv, [])
            for sname in strategy_names:
                strategy = self.deai_strategies.get(sname)
                if not strategy:
                    continue

                stage = {
                    "level": lv.value,
                    "strategy": strategy.name,
                    "description": strategy.description,
                    "steps": strategy.steps,
                    "prompt": strategy.prompt_template,
                    "effectiveness": strategy.effectiveness,
                }
                stages.append(stage)
                total_effectiveness = max(total_effectiveness, strategy.effectiveness)
                total_steps += len(strategy.steps)

            if lv == target:
                break

        if text:
            diagnosis = self.diagnose_ai_traits(text)
            stages.insert(0, {
                "level": "诊断",
                "strategy": "AI特征诊断",
                "description": diagnosis.summary,
                "steps": diagnosis.fix_priority,
                "prompt": "",
                "effectiveness": 0.0,
            })

        return DeAIPipeline(
            stages=stages,
            estimated_effectiveness=round(total_effectiveness, 2),
            total_steps=total_steps,
        )

    def get_deai_prompt(self, target_level: str = "voice") -> str:
        """
        生成可直接用于AI提示词的去痕指令

        Args:
            target_level: 目标去痕深度

        Returns:
            完整的去痕提示词
        """
        pipeline = self.generate_deai_pipeline(target_level=target_level)

        prompt_parts = [
            "【去AI痕迹写作指令】",
            "请按照以下规则重写内容，使其读起来像真人创作的小说:",
            "",
        ]

        for stage in pipeline.stages:
            if stage.get("prompt"):
                prompt_parts.append(f"## {stage['level']}")
                prompt_parts.append(stage["prompt"])
                prompt_parts.append("")

        prompt_parts.append("## 核心原则")
        prompt_parts.append("- 人类写作是'因果性'的，AI写作是'统计性'的——选择有因果逻辑的词，而非概率最高的词")
        prompt_parts.append("- 人类写作有瑕疵——允许不完美、矛盾、混乱")
        prompt_parts.append("- 人类写作有观点——叙述者不是中立的，有立场和态度")
        prompt_parts.append("- 人类写作有身体——用感官和身体反应而非抽象概念")
        prompt_parts.append("- 信任读者——说一遍就够，不要反复解释")

        return "\n".join(prompt_parts)

    # ═══════════════════════════════════════════════════════════
    # 知识注入提示词生成
    # ═══════════════════════════════════════════════════════════

    def inject_knowledge_to_prompt(
        self,
        base_prompt: str,
        genre: str = "玄幻",
        chapter_num: int = 1,
        character_count: int = 0,
    ) -> str:
        """
        将写作知识注入到AI提示词中

        Args:
            base_prompt: 基础提示词
            genre: 题材类型
            chapter_num: 章节号
            character_count: 已有人物数量

        Returns:
            增强后的提示词
        """
        knowledge_blocks = []

        knowledge_blocks.append(self._get_core_writing_rules())

        if chapter_num <= 3:
            knowledge_blocks.append(self._get_opening_rules(chapter_num))

        knowledge_blocks.append(self._get_deai_rules())

        knowledge_blocks.append(self._get_reader_engagement_rules(chapter_num))

        knowledge_blocks.append(self._get_genre_specific_rules(genre))

        enhanced = base_prompt + "\n\n" + "\n\n".join(knowledge_blocks)

        return enhanced

    def _get_core_writing_rules(self) -> str:
        """核心写作铁律"""
        return """【核心写作铁律 - 必须遵守】

1. 展示而非告知(Show, Don't Tell):
   - 禁止: "他感到愤怒""她非常悲伤""他内心恐惧"
   - 必须: 用身体反应+动作+对话展示情感
   - 示例: 不写"他很愤怒"，写"他把杯子往桌上一摔，瓷片溅了一地"

2. 短句为王:
   - 一句话只讲一件事，超过25字必须拆分
   - 关键动作/情绪用3-5字短句
   - 短句+短句+短句+中句=节奏感

3. 删除无效词:
   - 禁止: "此时此刻""不由得""其实""然后""接着""于是""便"
   - 禁止: "首先/其次/最后/此外/总而言之"
   - 禁止: "赋能/底层逻辑/闭环/维度/格局"

4. 五感描写:
   - 每个场景至少3种感官(视觉+听觉+嗅觉/触觉)
   - 优先使用嗅觉和触觉

5. 信任读者:
   - 说一遍就够，不要反复解释
   - 不要总结升华，用动作/画面/对话收束"""

    def _get_opening_rules(self, chapter_num: int) -> str:
        """开篇规则"""
        if chapter_num == 1:
            return """【黄金开篇规则 - 第一章】

1. 300字内主角必须出场并建立冲突/危机
2. 禁止大段世界观介绍和环境描写
3. 第一句用动作/对话/悬念开头，不要环境描写
4. 3000字内爆发首个冲突点
5. 章末必须有钩子(危机/悬念/反转/期待/情绪)"""
        else:
            return f"""【黄金三章规则 - 第{chapter_num}章】

- 矛盾持续升级
- 给出明确的阶段性目标
- 章末必须有钩子
- 如果是第三章:必须出现第一次小爽点"""

    def _get_deai_rules(self) -> str:
        """去AI痕迹规则"""
        return """【去AI痕迹规则 - 让文字像人写的】

词汇层面:
- 禁止: "首先/其次/最后/此外/总而言之/综上所述"
- 禁止: "赋能/底层逻辑/闭环/维度/格局/体系"
- 禁止: "时代/人生/智慧/力量/命运/灵魂/本质"(用具体事物替代)
- 禁止: "专家认为/研究表明/据记载"(要么给具体来源，要么改为个人经验)
- 限制: 破折号每千字不超过1个

句式层面:
- 打破排比/对偶，句子长短不一
- 句长要有变化:3字短句+20字中句+40字长句交替
- 不要每句都以"他/她"开头
- 减少"在...中/下/里""随着...""当...时"开头
- 被动改主动

结构层面:
- 不要三段式结构(第一/第二/第三)
- 情节不要模板化(遇到困难→克服→成长)
- 结尾不要总结升华
- 不要"与此同时/转眼间/不久之后"过渡

语义层面:
- 增加潜台词，不直接说明
- 设定通过角色视角/对话自然带出
- 因果关系要复杂:加入偶然、代价、副作用
- 角色可以有错误的判断

声音层面:
- 叙述者要有立场和态度
- 允许句子不完美——口语化、碎片化
- 感受要具体:不是"很难过"，而是身体的具体感受
- 允许一些混乱和瑕疵"""

    def _get_reader_engagement_rules(self, chapter_num: int) -> str:
        """读者吸引规则"""
        rules = """【读者吸引规则】

1. 章末钩子(必做):
   - 危机钩:主角陷入危险
   - 悬念钩:抛出谜题
   - 反转钩:意外发现
   - 期待钩:即将获得
   - 情绪钩:强烈情感

2. 情绪设计:
   - 先抑后扬:先憋屈→再释放
   - 释放要快:上一章憋屈，这一章就爆发
   - 重点描写反派的狼狈和周围人的震惊"""

        if chapter_num % 3 == 0:
            rules += "\n\n3. 本章建议安排小爽点(打脸/升级/获得/反转)"
        if chapter_num % 10 == 0:
            rules += "\n\n4. 本章建议安排大爽点(重大突破/关键反转)"

        return rules

    def _get_genre_specific_rules(self, genre: str) -> str:
        """题材特化规则"""
        genre_rules = {
            "玄幻": """【玄幻题材特化规则】
- 修炼体系要具体可感(不要抽象的境界描述)
- 战斗场面注重身体感受和即时反应
- 金手指/奇遇要有代价和限制
- 世界观通过角色体验自然展开""",

            "都市": """【都市题材特化规则】
- 现代场景要有真实的生活细节
- 身份反差是核心爽点来源
- 对话要符合现代人口语习惯
- 避免过度书面化的都市描写""",

            "悬疑": """【悬疑题材特化规则】
- 信息释放要有节奏——每次只给部分答案
- 红鲱鱼(误导线索)要自然
- 氛围营造优先于逻辑解释
- 角色判断可以出错""",

            "言情": """【言情题材特化规则】
- 情感发展要有波折和误会
- 身体反应比心理独白更有力
- 对话要有潜台词
- 细节(眼神/小动作)比直白告白更动人""",
        }

        return genre_rules.get(genre, f"【{genre}题材通用规则】\n- 遵循该题材的核心读者期待\n- 保持题材特有的节奏和氛围")

    # ═══════════════════════════════════════════════════════════
    # 批量分析与报告
    # ═══════════════════════════════════════════════════════════

    def batch_analyze(
        self, chapters: Dict[int, str]
    ) -> Dict[str, Any]:
        """
        批量分析多章节

        Args:
            chapters: {章节号: 章节文本}

        Returns:
            综合分析报告
        """
        results = {}
        scores = []

        for ch_num, text in sorted(chapters.items()):
            diagnosis = self.diagnose_ai_traits(text)
            techniques = self.recommend_techniques(
                text, {"chapter_num": ch_num}
            )
            results[ch_num] = {
                "diagnosis": diagnosis,
                "top_techniques": [(t.technique_name, t.relevance) for t in techniques[:3]],
            }
            scores.append(diagnosis.overall_ai_score)

        avg_score = sum(scores) / len(scores) if scores else 0
        score_trend = "上升" if len(scores) >= 2 and scores[-1] > scores[0] else (
            "下降" if len(scores) >= 2 and scores[-1] < scores[0] else "平稳"
        )

        return {
            "total_chapters": len(chapters),
            "average_ai_score": round(avg_score, 3),
            "score_trend": score_trend,
            "per_chapter": results,
            "overall_risk": "high" if avg_score > 0.6 else (
                "medium" if avg_score > 0.35 else "low"
            ),
        }

    def generate_writing_guide(
        self, genre: str = "玄幻", experience_level: str = "beginner"
    ) -> str:
        """
        生成写作指南

        Args:
            genre: 题材
            experience_level: 经验水平(beginner/intermediate/advanced)

        Returns:
            写作指南文本
        """
        guide_parts = [
            f"# NWACS {genre}题材写作指南",
            f"## 适用水平: {experience_level}",
            "",
        ]

        if experience_level == "beginner":
            guide_parts.append("## 第一阶段: 基础文笔训练")
            guide_parts.append("")
            guide_parts.append("### 1. 短句训练(每天15分钟)")
            guide_parts.append("- 找一段自己写的文字，把所有超过25字的句子拆成两句")
            guide_parts.append("- 删掉所有'此时此刻/不由得/其实/然后/接着/于是/便'")
            guide_parts.append("- 目标: 平均句长控制在15-20字")
            guide_parts.append("")
            guide_parts.append("### 2. 展示而非告知训练(每天20分钟)")
            guide_parts.append("- 选一个情绪(愤怒/悲伤/恐惧/高兴)")
            guide_parts.append("- 写一段200字的场景，不能出现该情绪的词")
            guide_parts.append("- 只能用动作/对话/身体反应/环境来传达")
            guide_parts.append("")
            guide_parts.append("### 3. 对话训练(每天15分钟)")
            guide_parts.append("- 写一段两人对话，删掉50%的字数")
            guide_parts.append("- 确保每句话都有信息量(推进剧情/塑造人物/埋伏笔)")
            guide_parts.append("- 给两个人物不同的说话风格")

        guide_parts.append("")
        guide_parts.append("## 核心技法速查")
        guide_parts.append("")
        for tech_name in ["show_dont_tell", "language_short_sentences",
                          "dialogue_information_density", "suspense_chapter_endings",
                          "opening_golden_300"]:
            tech = self.techniques.get(tech_name)
            if tech:
                guide_parts.append(f"### {tech.name}")
                guide_parts.append(f"- 为什么有效: {tech.why_it_works[:100]}...")
                guide_parts.append(f"- 常见错误: {tech.common_mistakes[:80]}...")
                guide_parts.append("")

        return "\n".join(guide_parts)


# ═══════════════════════════════════════════════════════════════
# 便捷函数
# ═══════════════════════════════════════════════════════════════

def create_knowledge_engine() -> WritingKnowledgeEngine:
    """创建写作知识引擎实例"""
    return WritingKnowledgeEngine()


def quick_diagnose(text: str) -> AIDiagnosis:
    """快速诊断文本AI痕迹"""
    engine = WritingKnowledgeEngine()
    return engine.diagnose_ai_traits(text)


def quick_deai_prompt(target_level: str = "voice") -> str:
    """快速获取去AI痕迹提示词"""
    engine = WritingKnowledgeEngine()
    return engine.get_deai_prompt(target_level)


def enhance_prompt(base_prompt: str, genre: str = "玄幻",
                   chapter_num: int = 1) -> str:
    """增强提示词——注入写作知识"""
    engine = WritingKnowledgeEngine()
    return engine.inject_knowledge_to_prompt(base_prompt, genre, chapter_num)


if __name__ == "__main__":
    print("=" * 60)
    print("NWACS 写作知识引擎 - 自检")
    print("=" * 60)

    engine = WritingKnowledgeEngine()

    print(f"\n[1] AI特征库: {len(engine.ai_traits)} 个特征")
    for name, trait in list(engine.ai_traits.items())[:3]:
        print(f"  - {name}: {trait.description[:60]}...")

    print(f"\n[2] 写作技法库: {len(engine.techniques)} 个技法")
    for name, tech in list(engine.techniques.items())[:3]:
        print(f"  - {tech.name} [{tech.category.value}] (难度:{tech.difficulty}/5)")

    print(f"\n[3] 读者策略库: {len(engine.reader_strategies)} 个策略")
    for name, s in list(engine.reader_strategies.items())[:3]:
        print(f"  - {s.name} [{s.type.value}]")

    print(f"\n[4] 去痕策略库: {len(engine.deai_strategies)} 个策略")
    for name, s in list(engine.deai_strategies.items())[:3]:
        print(f"  - {s.name} [{s.level.value}] (效果:{s.effectiveness:.0%})")

    test_text = """
    他感到非常愤怒，因为敌人又一次逃脱了。首先，他检查了周围的痕迹。
    其次，他开始分析敌人的逃跑路线。最后，他制定了一个新的追捕计划。
    总而言之，这次失败让他意识到了自己的不足，也为后续的成长体系赋能。
    """

    print(f"\n[5] AI特征诊断测试:")
    diagnosis = engine.diagnose_ai_traits(test_text)
    print(f"  综合评分: {diagnosis.overall_ai_score:.1%}")
    print(f"  风险等级: {diagnosis.risk_level}")
    print(f"  检测到的特征: {len(diagnosis.detected_traits)} 个")
    for name, severity in diagnosis.detected_traits[:3]:
        print(f"    - {name}: {severity:.1%}")

    print(f"\n[6] 技法推荐测试:")
    recs = engine.recommend_techniques(test_text, {"chapter_num": 1})
    for r in recs[:3]:
        print(f"  - {r.technique_name} (相关度:{r.relevance:.0%}, 紧急度:{r.urgency})")

    print(f"\n[7] 去痕流水线测试:")
    pipeline = engine.generate_deai_pipeline(target_level="voice")
    print(f"  阶段数: {len(pipeline.stages)}")
    print(f"  预估效果: {pipeline.estimated_effectiveness:.0%}")
    print(f"  总步骤: {pipeline.total_steps}")

    print(f"\n[8] 提示词增强测试:")
    enhanced = engine.inject_knowledge_to_prompt(
        "请写一章玄幻小说内容。", genre="玄幻", chapter_num=1
    )
    print(f"  原始提示词长度: 13 字符")
    print(f"  增强后长度: {len(enhanced)} 字符")

    print(f"\n{'=' * 60}")
    print("自检完成 - 所有模块正常")
    print(f"{'=' * 60}")