#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 书籍知识库 - 从100+本经典书籍中深度提炼写作技法精华

覆盖四大类书籍：
  A. 写作技法书 - 故事/麦基、故事写作大师班/克卢碧、小说的骨架/维兰德 等
  B. 文学名著 - 红楼梦、活着、白鹿原、围城、边城 等
  C. 工具词典 - 描写词典、成语词典、神话人物词典 等
  D. 文化哲学 - 人间词话、乡土中国、万古江河 等

每条技法映射到8项核心技能：剧情设计/人物塑造/对话写作/场景描写/节奏控制/伏笔设计/情绪设计/世界观构建
"""

from typing import Dict, List
from dataclasses import dataclass, field
from enum import Enum


class SkillTarget(Enum):
    PLOT_DESIGN = "剧情设计"
    CHARACTER_BUILDING = "人物塑造"
    DIALOGUE_WRITING = "对话写作"
    SCENE_DESCRIPTION = "场景描写"
    PACING_CONTROL = "节奏控制"
    FORESHADOWING = "伏笔设计"
    EMOTIONAL_DESIGN = "情绪设计"
    WORLD_BUILDING = "世界观构建"


@dataclass
class BookInsight:
    book_name: str
    author: str
    category: str
    core_technique: str
    detailed_insight: str
    target_skills: List[SkillTarget]
    actionable_tips: List[str]
    difficulty: str = "intermediate"


class BookKnowledgeBase:

    def __init__(self):
        self.insights: List[BookInsight] = []
        self._init_all_insights()

    def _init_all_insights(self):
        self._init_writing_craft_books()
        self._init_literary_masterpieces()
        self._init_reference_dictionaries()
        self._init_cultural_philosophy()

    # ================================================================
    # A. 写作技法书
    # ================================================================

    def _init_writing_craft_books(self):
        craft = [

            BookInsight(
                book_name="故事", author="罗伯特·麦基", category="写作技法",
                core_technique="故事三角理论与鸿沟原理",
                detailed_insight=(
                    "麦基提出'故事三角'：顶端经典设计(大情节)，左下小情节(极简主义)，右下反情节(反结构)。"
                    "核心概念'鸿沟'(Gap)：角色期望与现实之间的差距是故事动力源泉。每场景都应在期望与结果间打开鸿沟，"
                    "角色行动→期望结果→实际不同→更大行动，循环推进。激励事件必须彻底打破主角生活平衡。"
                    "高潮须是主角与对抗力量的终极对决。用'负面之负面'原则：困境须不断加深。"
                ),
                target_skills=[SkillTarget.PLOT_DESIGN, SkillTarget.CHARACTER_BUILDING, SkillTarget.PACING_CONTROL],
                actionable_tips=[
                    "每场景设置'期望vs结果'鸿沟，角色行动后结果必须出乎意料",
                    "激励事件放前25%，彻底打破平衡、不可逆转",
                    "高潮须主角与对抗力量终极对决，不可由外力解决",
                    "用'负面之负面'：困境不断加深而非简单重复",
                    "场景设计遵循'价值转折'：每场景结束须有正/负价值变化",
                ], difficulty="advanced",
            ),

            BookInsight(
                book_name="故事写作大师班", author="约翰·克卢碧", category="写作技法",
                core_technique="22步故事结构法与欲望驱动",
                detailed_insight=(
                    "克卢碧将故事分解为22步骤，核心是'欲望'(Desire)：主角须有清晰、具体、可见的欲望目标。"
                    "故事=欲望+障碍+行动。七大关键步骤：1)弱点/需求 2)欲望 3)对手 4)计划 5)战斗 6)自我揭示 7)新平衡。"
                    "每角色都有'道德弱点'和'心理需求'，故事本质是角色克服弱点、满足需求的过程。"
                    "对手不是简单坏人，而是与主角争夺同一目标的人，且须比主角更强。"
                ),
                target_skills=[SkillTarget.PLOT_DESIGN, SkillTarget.CHARACTER_BUILDING, SkillTarget.FORESHADOWING],
                actionable_tips=[
                    "主角须有具体可见的欲望目标(非抽象'幸福')",
                    "对手须与主角争夺同一目标，实力强于主角",
                    "每主要角色都要有'道德弱点→心理需求'设定",
                    "故事中点须是主角从被动转主动的转折",
                    "自我揭示时刻：主角须认识到自己弱点并做出改变",
                ], difficulty="advanced",
            ),

            BookInsight(
                book_name="小说的骨架", author="凯蒂·维兰德", category="写作技法",
                core_technique="提纲先行法与场景卡片系统",
                detailed_insight=(
                    "维兰德主张'提纲不是束缚而是地图'。核心方法：1)一句话概括小说核心 2)扩展为一段话(含主要冲突和结局) "
                    "3)分解为场景卡片(每卡片=一场景) 4)用'如果……会怎样？'不断追问深化。场景卡片含：视点角色、场景目标、"
                    "冲突类型、转折点、信息揭示。强调'因果关系链'：每场景须因前场景而发生，用'因此'和'但是'连接而非'然后'。"
                ),
                target_skills=[SkillTarget.PLOT_DESIGN, SkillTarget.PACING_CONTROL, SkillTarget.FORESHADOWING],
                actionable_tips=[
                    "一句话概括：当[事件]发生时，[主角]必须[行动]否则[后果]",
                    "场景间用'因此/但是'连接，杜绝'然后'式流水账",
                    "每场景卡片明确：谁、想要什么、障碍是什么、结果如何",
                    "提纲标注每场景信息揭示点(读者知道了什么新信息)",
                    "用'如果……会怎样？'对每情节节点追问3次",
                ], difficulty="intermediate",
            ),

            BookInsight(
                book_name="这样写出好故事", author="詹姆斯·贝尔", category="写作技法",
                core_technique="LOCK系统与场景张力公式",
                detailed_insight=(
                    "LOCK系统：Lead(主角)、Objective(目标)、Confrontation(对抗)、Knockout(结局)。"
                    "主角须有趣且有缺陷，目标须关乎生死(物理/职业/心理)，对抗须持续升级，结局须让读者满意。"
                    "场景张力公式：目标+障碍+结果(通常是挫折)=张力。'两扇门原则'：第一扇门(激励事件)推主角入故事，"
                    "第二扇门(中点)让主角无法回头。每50页须有一重大事件改变故事方向。"
                ),
                target_skills=[SkillTarget.PLOT_DESIGN, SkillTarget.PACING_CONTROL, SkillTarget.EMOTIONAL_DESIGN],
                actionable_tips=[
                    "用LOCK四要素检查故事骨架是否完整",
                    "每50页(约2-3万字)设置不可逆重大事件",
                    "场景张力=目标+障碍+挫折，三者缺一不可",
                    "第一扇门(激励事件)须让主角别无选择",
                    "结局须主角与对抗力量终极对决，不可由外力/巧合解决",
                ], difficulty="intermediate",
            ),

            BookInsight(
                book_name="写好前五十页", author="杰夫·格尔克", category="写作技法",
                core_technique="前50页必须完成的9项任务",
                detailed_insight=(
                    "前50页是编辑和读者决定是否继续的关键。须完成9项任务：1)建立故事世界 2)引入主角并让读者关心ta "
                    "3)展示主角日常生活(以便后续打破) 4)建立核心欲望 5)引入对抗力量 6)设置核心冲突 "
                    "7)建立故事基调 8)暗示主题 9)50页结束前发生第一个重大转折。"
                    "关键原则：'展示而非告知'在前50页尤其重要，用行动和细节代替说明。"
                ),
                target_skills=[SkillTarget.PLOT_DESIGN, SkillTarget.CHARACTER_BUILDING, SkillTarget.WORLD_BUILDING],
                actionable_tips=[
                    "前50页须让读者知道：谁、在哪里、想要什么、阻碍是什么",
                    "第1页就要有冲突或悬念，不能从平静日常开始",
                    "主角出场展示'标志性动作'或'标志性特征'",
                    "前50页至少埋3个伏笔(后续50-100页内回收)",
                    "用'展示而非告知'检查每段：是否在说教而非呈现？",
                ], difficulty="intermediate",
            ),

            BookInsight(
                book_name="写作的诞生", author="多萝西娅·布兰德", category="写作技法",
                core_technique="作家双重人格理论与无意识写作",
                detailed_insight=(
                    "布兰德提出每作家都有'双重人格'：艺术家(无意识、感性、灵感)和批评家(有意识、理性、编辑)。"
                    "写作时先让艺术家自由发挥(晨间写作)，再让批评家修改润色。核心练习：每天醒来第一件事写500-1000字，"
                    "不修改、不评判、不停笔。训练无意识写作能力，绕过内在批评者。"
                ),
                target_skills=[SkillTarget.DIALOGUE_WRITING, SkillTarget.SCENE_DESCRIPTION, SkillTarget.EMOTIONAL_DESIGN],
                actionable_tips=[
                    "每天固定时间'无意识写作'15分钟，不停笔不修改",
                    "写作和修改分两时段进行，不要边写边改",
                    "用'定时写作法'：设定25分钟专注写作不中断",
                    "记录灵感：随身带笔记本捕捉任何闪现想法",
                    "阅读时用'作家眼光'分析：作者为什么这样写？",
                ], difficulty="beginner",
            ),

            BookInsight(
                book_name="九宫格写作法", author="山口拓朗", category="写作技法",
                core_technique="九宫格信息整理与结构化写作",
                detailed_insight=(
                    "九宫格写作法将主题放中心格，周围8格填相关信息，形成结构化思维。适用于：1)角色设定(中心=角色名，"
                    "8格=外貌/性格/背景/欲望/恐惧/关系/习惯/秘密) 2)情节设计(中心=核心事件，8格=起因/发展/转折/冲突/"
                    "人物反应/后果/伏笔/主题) 3)场景描写(中心=场景，8格=视觉/听觉/嗅觉/触觉/味觉/情绪/时间/氛围)。"
                ),
                target_skills=[SkillTarget.PLOT_DESIGN, SkillTarget.CHARACTER_BUILDING, SkillTarget.SCENE_DESCRIPTION],
                actionable_tips=[
                    "用九宫格做角色设定：中心=角色名，8格填满角色维度",
                    "用九宫格做场景规划：中心=场景目的，8格=五感+情绪+时间+氛围",
                    "用九宫格做情节检查：中心=章节目标，8格=各要素是否到位",
                    "九宫格填不满说明设定不够丰富，继续追问",
                    "多九宫格串联：角色九宫格→情节九宫格→场景九宫格",
                ], difficulty="beginner",
            ),

            BookInsight(
                book_name="卡片笔记写作法", author="申克·阿伦斯", category="写作技法",
                core_technique="卢曼卡片盒笔记法与知识网络构建",
                detailed_insight=(
                    "卢曼用卡片盒(Zettelkasten)方法写了70多本书和400多篇论文。核心：1)每条笔记只记一个想法，用自己的话写 "
                    "2)笔记间建立链接 3)按主题聚类但允许跨主题连接 4)定期回顾整理。对小说写作：每角色/情节/设定/伏笔都是"
                    "一张卡片，卡片间建立关系链接，形成完整'故事网络'。灵感来自卡片间意外连接。"
                ),
                target_skills=[SkillTarget.PLOT_DESIGN, SkillTarget.FORESHADOWING, SkillTarget.WORLD_BUILDING],
                actionable_tips=[
                    "为每角色创建独立卡片，记录所有相关信息",
                    "为每伏笔创建卡片，标注埋设位置和回收位置",
                    "卡片间建立链接：角色A→与角色B关系→共同参与剧情",
                    "定期回顾卡片，寻找可建立新连接的点",
                    "用卡片法管理长篇小说复杂信息网络",
                ], difficulty="intermediate",
            ),

            BookInsight(
                book_name="模板写作法", author="山口拓朗", category="写作技法",
                core_technique="列举型/结论优先型/故事型三大模板",
                detailed_insight=(
                    "三大万能模板：1)列举型：结论→列举要点→总结 2)结论优先型：结论→理由→具体例→总结 "
                    "3)故事型：困境→转机→行动→结果→感悟。对小说：故事型模板天然适合情节设计；列举型适合世界观说明；"
                    "结论优先型适合角色内心独白和议论。模板不是限制而是脚手架。"
                ),
                target_skills=[SkillTarget.PLOT_DESIGN, SkillTarget.DIALOGUE_WRITING, SkillTarget.WORLD_BUILDING],
                actionable_tips=[
                    "用故事型模板设计每情节单元：困境→转机→行动→结果→感悟",
                    "用列举型模板组织世界观设定：分类→要点→关联",
                    "用结论优先型模板写角色内心独白：观点→理由→例证→结论",
                    "模板间可嵌套：大故事套小故事，层层递进",
                    "先套模板写初稿，再打破模板创新",
                ], difficulty="beginner",
            ),

            BookInsight(
                book_name="写出我心", author="娜塔莉·戈德堡", category="写作技法",
                core_technique="自由写作法与细节的力量",
                detailed_insight=(
                    "戈德堡核心教导：'闭嘴，开始写'。自由写作规则：1)手不要停 2)不要删除 3)不要担心拼写语法 "
                    "4)放松控制 5)别想、别逻辑化 6)直击要害。'细节就是力量'：不说'花'而说'天竺葵'，不说'鸟'而说'鹪鹩'。"
                    "具体细节让文字活起来。'写作是90%的倾听'：倾听世界、倾听内心、倾听文字本身的声音。"
                ),
                target_skills=[SkillTarget.SCENE_DESCRIPTION, SkillTarget.DIALOGUE_WRITING, SkillTarget.EMOTIONAL_DESIGN],
                actionable_tips=[
                    "每天10分钟自由写作练习，不停笔不修改",
                    "用具体名词代替抽象名词：'交通工具'→'破旧二八自行车'",
                    "描写时追问：什么颜色？什么声音？什么气味？什么质感？",
                    "写情感不写'他很伤心'，写'他蹲在墙角，肩膀微微颤抖'",
                    "倾听生活中对话，记录有特色表达方式",
                ], difficulty="beginner",
            ),

            BookInsight(
                book_name="学会写作", author="粥佐罗", category="写作技法",
                core_technique="新媒体写作爆款公式与用户思维",
                detailed_insight=(
                    "爆款文章公式：好选题(50%)+好标题(20%)+好内容(20%)+好排版(10%)。对网文启示："
                    "1)选题=题材选择(玄幻/都市/言情赛道决定天花板) 2)标题=书名和章节名(决定点击率) "
                    "3)内容=正文质量(决定留存率) 4)排版=段落和节奏(决定阅读体验)。"
                    "'用户思维'：时刻想读者需要什么、期待什么、在什么场景阅读。网文是'服务型写作'非'表达型写作'。"
                ),
                target_skills=[SkillTarget.PLOT_DESIGN, SkillTarget.PACING_CONTROL, SkillTarget.EMOTIONAL_DESIGN],
                actionable_tips=[
                    "选题决定80%成败：选对题材赛道比写得好更重要",
                    "每章标题要有吸引力和信息量，让读者产生点击欲望",
                    "用'用户思维'检查每章：读者看完会有什么感受？",
                    "手机阅读场景下段落不超3-4行，每章2000-4000字",
                    "开头3秒定生死：第一章第一段必须有钩子",
                ], difficulty="intermediate",
            ),

            BookInsight(
                book_name="小说课", author="毕飞宇", category="写作技法",
                core_technique="细读法与小说家的眼光",
                detailed_insight=(
                    "毕飞宇以小说家眼光细读经典揭示写作奥秘。核心：1)'小说的逻辑'：小说有自身逻辑非现实逻辑，"
                    "角色行为须符合角色自身逻辑。2)'留白的艺术'：不说比说更有力，海明威冰山理论——只写八分之一。"
                    "3)'视角即权力'：选谁视角就是赋予谁话语权，视角切换须有意为之。4)'语言的节奏'：长短句交替、"
                    "重复与变化，语言本身就是音乐。"
                ),
                target_skills=[SkillTarget.CHARACTER_BUILDING, SkillTarget.DIALOGUE_WRITING, SkillTarget.SCENE_DESCRIPTION],
                actionable_tips=[
                    "检查角色行为是否符合角色自身逻辑，非作者强行安排",
                    "学会留白：删掉所有读者自己能推断出的内容",
                    "视角切换要有明确目的，同场景内尽量不频繁切换",
                    "朗读自己文字，检查语言节奏是否流畅",
                    "用'细读法'分析喜欢作品：逐段分析作者为什么这样写",
                ], difficulty="advanced",
            ),

            BookInsight(
                book_name="如何写砸一本小说", author="霍华德·米特尔马克", category="写作技法",
                core_technique="反面教材法：200种毁掉小说的方式",
                detailed_insight=(
                    "通过展示200种最常见写作错误反向教学。核心教训：1)情节错误：巧合解决冲突、主角被动等待、反派太弱、"
                    "结局无铺垫 2)角色错误：主角完美无缺、配角比主角有趣、角色行为不一致 3)语言错误：过度修饰、陈词滥调、"
                    "对话标签滥用、信息倾倒 4)结构错误：开头太慢、中间拖沓、结尾仓促。知道什么不该做比知道该做什么更重要。"
                ),
                target_skills=[SkillTarget.PLOT_DESIGN, SkillTarget.CHARACTER_BUILDING, SkillTarget.PACING_CONTROL],
                actionable_tips=[
                    "检查：冲突是否由主角主动解决？(不能用巧合/天降神兵)",
                    "检查：反派是否对主角构成真正威胁？(不能太弱)",
                    "检查：是否有信息倾倒？(大段说明性文字)",
                    "检查：对话标签是否过度使用？(不要每对话都加副词修饰)",
                    "检查：结局是否有铺垫？(不能突然冒出新设定解决问题)",
                ], difficulty="intermediate",
            ),

            BookInsight(
                book_name="小说写作叙事技巧指南", author="珍妮特·伯罗薇", category="写作技法",
                core_technique="叙事距离控制与时间处理",
                detailed_insight=(
                    "伯罗薇系统讲解叙事技巧：1)叙事距离：从远距离(全知概括)到近距离(内心独白)是连续光谱，"
                    "好叙事在两者间灵活切换。2)时间处理：概述(压缩时间)、场景(实时展示)、停顿(描写/评论)、"
                    "省略(跳过)。四种方式交替创造节奏。3)展示vs讲述：非二元对立而是比例问题。关键时刻展示，过渡内容讲述。"
                ),
                target_skills=[SkillTarget.PLOT_DESIGN, SkillTarget.PACING_CONTROL, SkillTarget.SCENE_DESCRIPTION],
                actionable_tips=[
                    "关键情节用'场景'(实时展示)，过渡内容用'概述'(压缩时间)",
                    "叙事距离有意控制：高潮拉近(内心独白)，过渡拉远(概括叙述)",
                    "用'停顿'技巧在紧张时刻插入描写制造悬念延迟",
                    "用'省略'跳过读者可自行推断内容",
                    "展示vs讲述比例：关键场景80%展示，过渡段落80%讲述",
                ], difficulty="advanced",
            ),

            BookInsight(
                book_name="写作辞林", author="袁晖", category="写作技法",
                core_technique="分类词汇积累与语境化运用",
                detailed_insight=(
                    "《写作辞林》按主题分类收录大量词汇和表达方式，涵盖写人、写景、写事、写情四大板块。核心价值："
                    "1)提供丰富同义表达避免重复 2)展示词汇在不同语境中用法差异 3)收录经典文学作品范例。"
                    "对网文写作：建立自己分类词汇库，按'战斗/日常/情感/风景/心理'等场景分类积累，写作时快速调用。"
                ),
                target_skills=[SkillTarget.SCENE_DESCRIPTION, SkillTarget.DIALOGUE_WRITING, SkillTarget.EMOTIONAL_DESIGN],
                actionable_tips=[
                    "建立个人分类词汇库：按场景/情绪/动作分类",
                    "每场景类型积累20-50个核心词汇和表达",
                    "避免高频词重复：'说'可替换为低语/呢喃/吼道/冷声道",
                    "学习经典作品中词汇运用，理解语境差异",
                    "定期更新词汇库，淘汰陈词滥调吸收新鲜表达",
                ], difficulty="beginner",
            ),

            BookInsight(
                book_name="小说创造基本技巧", author="克里斯托弗·沃格勒", category="写作技法",
                core_technique="英雄之旅12阶段模型",
                detailed_insight=(
                    "沃格勒将坎贝尔'英雄之旅'简化为12阶段：1)平凡世界 2)冒险召唤 3)拒绝召唤 4)遇见导师 "
                    "5)跨越第一道门槛 6)考验/盟友/敌人 7)接近最深洞穴 8)磨难(核心考验) 9)奖励 10)返回之路 "
                    "11)复活(最终考验) 12)携万能药返回。每阶段对应角色成长一步。网文中'废柴逆袭''重生复仇'等"
                    "模板本质都是英雄之旅变体。理解原型结构才能灵活变通。"
                ),
                target_skills=[SkillTarget.PLOT_DESIGN, SkillTarget.CHARACTER_BUILDING, SkillTarget.WORLD_BUILDING],
                actionable_tips=[
                    "用英雄之旅12阶段检查长篇小说整体结构",
                    "每阶段对应角色一次成长或认知升级",
                    "网文模板是英雄之旅变体：废柴逆袭=平凡世界→跨越门槛→磨难→复活",
                    "导师角色不一定是人，可是书/记忆/顿悟",
                    "磨难阶段(第8阶段)须是主角最接近死亡/失败时刻",
                ], difficulty="intermediate",
            ),

            BookInsight(
                book_name="小说写作进阶技巧", author="唐纳德·马斯", category="写作技法",
                core_technique="微张力技术与情感放大器",
                detailed_insight=(
                    "马斯提出'微张力'(Micro-tension)概念：非大冲突而是字里行间持续紧张感。技术：1)对话中微张力："
                    "每句对话都有隐藏冲突或未说出的话 2)描写中微张力：环境描写暗示即将发生的事 3)内心独白中微张力："
                    "角色内心矛盾和犹豫。'情感放大器'：在情感高潮前设置'情感抑制'，让读者期待释放，释放时效果加倍。"
                ),
                target_skills=[SkillTarget.DIALOGUE_WRITING, SkillTarget.EMOTIONAL_DESIGN, SkillTarget.PACING_CONTROL],
                actionable_tips=[
                    "在平静场景中埋入微张力：一句带刺的话、一个不安眼神",
                    "对话中让角色'说一套想一套'制造潜台词张力",
                    "环境描写暗示情绪：阴沉天空=压抑心情",
                    "情感高潮前先抑制：想哭时先忍住，释放时更有力",
                    "每页至少一处微张力，让读者始终处于轻微不安中",
                ], difficulty="advanced",
            ),

            BookInsight(
                book_name="小说的骨架：好提纲成就好故事", author="凯蒂·维兰德", category="写作技法",
                core_technique="提纲层次结构与动态调整",
                detailed_insight=(
                    "维兰德深入讲解提纲层次：1)故事层面提纲(整体结构) 2)章节层面提纲(每章目标) 3)场景层面提纲(每场景节拍)。"
                    "提纲非一成不变而是'活文档'：写作中发现更好方向时应修改提纲而非死守。关键：提纲中标注'情感节拍'——"
                    "每场景结束时读者情绪应该是什么。用颜色标记：红色=冲突场景，蓝色=情感场景，绿色=过渡场景。"
                ),
                target_skills=[SkillTarget.PLOT_DESIGN, SkillTarget.PACING_CONTROL, SkillTarget.EMOTIONAL_DESIGN],
                actionable_tips=[
                    "建立三层提纲：故事→章节→场景，逐层细化",
                    "提纲标注每场景'情感节拍'(读者情绪目标)",
                    "提纲是活文档：发现更好方向就修改提纲",
                    "用颜色标记提纲：红=冲突，蓝=情感，绿=过渡",
                    "检查提纲节奏：红蓝绿交替，避免同色连续出现",
                ], difficulty="intermediate",
            ),
        ]
        self.insights.extend(craft)

    # ================================================================
    # B. 文学名著
    # ================================================================

    def _init_literary_masterpieces(self):
        lit = [

            BookInsight(
                book_name="红楼梦", author="曹雪芹", category="文学名著",
                core_technique="草蛇灰线法与人物群像塑造",
                detailed_insight=(
                    "《红楼梦》是长篇小说技法巅峰教材。1)'草蛇灰线，伏脉千里'：伏笔埋设极致艺术。第五回判词和曲子预示"
                    "所有主要角色命运，但读者初读浑然不觉。伏笔可埋几百回再回收。2)人物群像塑造：400多人物各有特色。技法："
                    "对比法(黛玉vs宝钗)、映衬法(晴雯是黛玉影子，袭人是宝钗影子)、层层皴染法(多次出场逐步丰富人物)。"
                    "3)对话个性化：每人语言风格独一无二，王熙凤泼辣、林黛玉尖刻、薛宝钗圆融，听其言如见其人。"
                ),
                target_skills=[SkillTarget.CHARACTER_BUILDING, SkillTarget.FORESHADOWING, SkillTarget.DIALOGUE_WRITING],
                actionable_tips=[
                    "学习'草蛇灰线'：早期章节埋看似无关细节，后期揭示深意",
                    "用'影子人物'丰富主角：配角是主角某一面放大或对照",
                    "对话个性化：为每主要角色设计独特口头禅和句式习惯",
                    "用'层层皴染法'：多次出场逐步揭示角色不同侧面",
                    "长篇伏笔可跨数百章回收，但要确保读者能回忆起",
                ], difficulty="advanced",
            ),

            BookInsight(
                book_name="活着", author="余华", category="文学名著",
                core_technique="极简叙事的力量与苦难中的温情",
                detailed_insight=(
                    "余华用最朴素语言讲最沉重故事。1)语言极简：几乎不用形容词和成语，用最简单词汇产生最大冲击力。"
                    "'以轻写重'——用平静语调写惨烈死亡，反差产生震撼。2)第一人称沉浸感：福贵讲自己故事，读者仿佛坐对面听。"
                    "3)节奏控制：死亡事件一个接一个，但每次死亡间都有温情缓冲，让读者在绝望中看到希望再打破。"
                    "这种'希望-破灭'循环比一路黑暗到底更有力。4)细节力量：有庆的鞋、家珍的头发——具体细节让抽象痛苦可触可感。"
                ),
                target_skills=[SkillTarget.EMOTIONAL_DESIGN, SkillTarget.PACING_CONTROL, SkillTarget.SCENE_DESCRIPTION],
                actionable_tips=[
                    "尝试'以轻写重'：用平静语调写激烈情感",
                    "设计'希望-破灭'循环：给读者希望再打破，比一直绝望有力",
                    "用具体细节承载情感：不说'他很穷'，说'他只有一双鞋还是破的'",
                    "极简语言力量：删掉所有不必要形容词和成语",
                    "第一人称叙事时语言风格须符合叙述者身份和性格",
                ], difficulty="intermediate",
            ),

            BookInsight(
                book_name="白鹿原", author="陈忠实", category="文学名著",
                core_technique="史诗叙事与地域文化深度融合",
                detailed_insight=(
                    "《白鹿原》是'一个民族的秘史'。1)史诗结构：以白鹿两家三代人命运折射半世纪中国历史。"
                    "个人命运与时代洪流交织——大历史推动小人物，小人物反映大历史。2)地域文化深度融入：关中方言、民俗、"
                    "饮食、建筑、宗族制度——文化不是背景板而是故事有机组成部分。3)复杂人性：无纯粹好人坏人，"
                    "白嘉轩固执、鹿子霖圆滑、田小娥悲剧——每角色都有其合理性。4)象征系统：白鹿作为核心象征贯穿全书。"
                ),
                target_skills=[SkillTarget.WORLD_BUILDING, SkillTarget.CHARACTER_BUILDING, SkillTarget.PLOT_DESIGN],
                actionable_tips=[
                    "将地域文化深度融入故事：方言/民俗/饮食/建筑是情节要素",
                    "设计核心象征物贯穿全书(如白鹿)，赋予故事深层意义",
                    "人物避免脸谱化：每角色都要有其行为内在合理性",
                    "个人命运与宏大背景交织：大事件推动个人选择",
                    "家族叙事结构：通过代际冲突和传承制造长线张力",
                ], difficulty="advanced",
            ),

            BookInsight(
                book_name="平凡的世界", author="路遥", category="文学名著",
                core_technique="现实主义的力量与奋斗叙事",
                detailed_insight=(
                    "《平凡的世界》展示现实主义小说持久魅力。1)奋斗叙事经典结构：困境→挣扎→小成功→更大困境→再挣扎→成长。"
                    "孙少平成长弧线是教科书级别。2)双线叙事：孙少安(农村线)和孙少平(城市线)交织展现同一时代不同面向。"
                    "3)情感真实性：不煽情但动人。田晓霞之死无大段抒情，只有孙少平独自赴约细节——真实比煽情更有力。"
                    "4)时代细节精准：每生活细节都经得起推敲，构建坚实世界感。"
                ),
                target_skills=[SkillTarget.CHARACTER_BUILDING, SkillTarget.EMOTIONAL_DESIGN, SkillTarget.PLOT_DESIGN],
                actionable_tips=[
                    "设计'困境→挣扎→小成功→更大困境'螺旋上升结构",
                    "双线/多线叙事时每条线要有独立节奏和主题",
                    "情感高潮用细节而非抒情：一个动作胜过千言万语",
                    "时代/世界细节要经得起推敲，构建读者信任感",
                    "主角成长须是'有代价的成长'：每次进步都伴随失去",
                ], difficulty="intermediate",
            ),

            BookInsight(
                book_name="围城", author="钱锺书", category="文学名著",
                core_technique="讽刺艺术与知识分子语言",
                detailed_insight=(
                    "《围城》是讽刺小说巅峰。1)比喻艺术：钱锺书比喻出人意料又精准无比。'忠厚老实人的恶毒，像饭里的砂砾"
                    "或者出骨鱼片里未净的刺，给人一种不期待的伤痛。'——将抽象感受具象化且具象得令人拍案。"
                    "2)知识分子语言：人物对话充满机锋、双关、典故，语言本身就是人物塑造。3)结构上'围城'意象："
                    "婚姻是围城、工作是围城、人生是围城——核心意象贯穿全书。4)叙述者声音：有态度有智慧的评论者。"
                ),
                target_skills=[SkillTarget.DIALOGUE_WRITING, SkillTarget.CHARACTER_BUILDING, SkillTarget.SCENE_DESCRIPTION],
                actionable_tips=[
                    "比喻要出人意料又精准：将抽象感受用具体新鲜意象表达",
                    "为核心主题设计贯穿全书意象(如'围城')",
                    "对话要体现角色智识水平和性格特征",
                    "叙述者可有态度：适当评论增加文本智性魅力",
                    "讽刺要义：不是直接嘲笑而是让读者自己发现荒谬",
                ], difficulty="advanced",
            ),

            BookInsight(
                book_name="边城", author="沈从文", category="文学名著",
                core_technique="诗意叙事与留白美学",
                detailed_insight=(
                    "《边城》展示'少即是多'的极致。1)诗意叙事：语言如诗节奏舒缓，每句子都精心打磨。2)留白艺术："
                    "翠翠父母之死、大佬之死、傩送去向——重要事件不直接写而是侧面交代或留白。3)风景即心情："
                    "茶峒山水不是背景而是角色，风景描写承载情感。4)开放式结局：'这个人也许永远不回来了，也许明天回来'——"
                    "不给出答案比给出答案更有余韵。"
                ),
                target_skills=[SkillTarget.SCENE_DESCRIPTION, SkillTarget.EMOTIONAL_DESIGN, SkillTarget.PACING_CONTROL],
                actionable_tips=[
                    "学习留白：重要事件可通过侧面交代给读者想象空间",
                    "风景描写承载情感：环境不是背景而是角色心情外化",
                    "开放式结局技巧：不给出确定答案让读者自己完成故事",
                    "诗意不等于华丽：朴素语言也可有诗意，关键在节奏和意象",
                    "缓慢叙事力量：不是所有故事都需要快节奏",
                ], difficulty="intermediate",
            ),

            BookInsight(
                book_name="呼兰河传", author="萧红", category="文学名著",
                core_technique="儿童视角与散文化叙事",
                detailed_insight=(
                    "萧红用儿童眼光看世界产生独特叙事效果。1)儿童视角双重性：表面不谙世事童真，深层成年人悲悯。"
                    "残酷事实被'过滤'后呈现反而更触目惊心。2)散文化叙事：无紧凑情节线，以空间(呼兰河城)为结构，"
                    "一章写一条街、一个人、一件事。'空间叙事'适合构建地方志式小说。3)重复力量：'我家是荒凉的'——"
                    "重复不是啰嗦而是情感叠加。4)群像中个体：写群体但通过具体个体故事让群体活起来。"
                ),
                target_skills=[SkillTarget.SCENE_DESCRIPTION, SkillTarget.EMOTIONAL_DESIGN, SkillTarget.WORLD_BUILDING],
                actionable_tips=[
                    "尝试儿童视角：用天真眼光写残酷事，反差产生力量",
                    "空间叙事结构：以地点而非时间为线索组织故事",
                    "有意重复：关键意象和句式重复可叠加情感",
                    "写群体时通过具体个体呈现，避免空泛群像描写",
                    "散文化叙事适合构建氛围和世界感，但需控制节奏",
                ], difficulty="advanced",
            ),

            BookInsight(
                book_name="四世同堂", author="老舍", category="文学名著",
                core_technique="京味语言与群像命运交响",
                detailed_insight=(
                    "老舍语言艺术和结构能力在《四世同堂》达巅峰。1)京味语言：地道北京话让每角色活起来。"
                    "语言地域特色是人物塑造最有力工具。2)群像结构：小羊圈胡同十几户人家各有自己故事线，"
                    "但在战争大背景下交织。'多声部'结构需精心设计每条线节奏和交汇点。3)对比结构："
                    "瑞宣犹豫vs瑞全决绝、钱默吟转变、冠晓荷堕落——通过对比让人物更鲜明。"
                ),
                target_skills=[SkillTarget.DIALOGUE_WRITING, SkillTarget.CHARACTER_BUILDING, SkillTarget.PLOT_DESIGN],
                actionable_tips=[
                    "用方言/地域语言塑造人物：语言风格即人物性格",
                    "多线群像结构：设计每条线独立节奏和交汇节点",
                    "用对比让人物更鲜明：犹豫vs决绝、坚守vs堕落",
                    "大事件作为背景：战争/灾难不一定是主角而是推动力",
                    "长篇需要'呼吸感'：紧张和松弛交替让读者有喘息空间",
                ], difficulty="advanced",
            ),

            BookInsight(
                book_name="蛙", author="莫言", category="文学名著",
                core_technique="书信体叙事与魔幻现实主义",
                detailed_insight=(
                    "莫言在《蛙》中展示书信体小说独特魅力。1)书信体结构：五封长信+一部话剧打破传统叙事框架。"
                    "书信体让叙述者有明确倾诉对象增强情感直接性。2)魔幻现实主义：现实与幻觉交织，青蛙意象贯穿全书——"
                    "魔幻不是逃避现实而是用超现实方式揭示更深真实。3)罪与赎主题：姑姑一生是'罪与赎'完整弧线，"
                    "从坚定执行→怀疑→忏悔→寻求救赎——完整角色弧线设计。"
                ),
                target_skills=[SkillTarget.PLOT_DESIGN, SkillTarget.EMOTIONAL_DESIGN, SkillTarget.WORLD_BUILDING],
                actionable_tips=[
                    "尝试书信体/日记体等非传统叙事形式",
                    "设计贯穿全书意象(如'蛙')赋予多重象征意义",
                    "角色弧线设计：坚定→怀疑→忏悔→救赎完整转变",
                    "魔幻元素要有现实根基：超现实是为揭示更深真实",
                    "叙事形式创新要为内容服务，不能为形式而形式",
                ], difficulty="advanced",
            ),

            BookInsight(
                book_name="嫌疑人X的献身", author="东野圭吾", category="文学名著",
                core_technique="诡计叙事与情感反转",
                detailed_insight=(
                    "东野圭吾展示推理小说技法极致。1)叙述性诡计：利用读者认知盲区。开头就告诉读者'真相'，"
                    "但那'真相'本身就是诡计一部分。2)双重结构：表面推理内核爱情。类型小说深度来自类型超越。"
                    "3)信息控制：作者知道什么、角色知道什么、读者知道什么——三者信息差是悬念来源。"
                    "4)结局反转：所有线索前文都有铺垫但读者直到最后才恍然大悟。反转力量来自铺垫充分。"
                ),
                target_skills=[SkillTarget.PLOT_DESIGN, SkillTarget.FORESHADOWING, SkillTarget.EMOTIONAL_DESIGN],
                actionable_tips=[
                    "利用读者认知盲区设计叙述性诡计",
                    "信息差设计：作者>读者>角色 或 读者>角色>其他角色",
                    "反转须有充分铺垫：让读者回看时发现'原来如此'",
                    "类型小说深度来自类型超越：推理+爱情、玄幻+哲学",
                    "结局情感冲击力来自前期对角色深度塑造",
                ], difficulty="advanced",
            ),

            BookInsight(
                book_name="一句顶一万句", author="刘震云", category="文学名著",
                core_technique="说话的艺术与'绕'的美学",
                detailed_insight=(
                    "刘震云创造独特'说话体'小说。1)'绕'的叙事艺术：一件事不直接说而是绕来绕去，绕的过程中"
                    "带出无数相关人和事。'绕'不是啰嗦而是用看似离题方式逼近核心。2)对话驱动叙事：全书靠对话推进，"
                    "对话就是情节。3)普通人哲学：最朴素对话中含最深人生智慧。'日子是过以后，不是过以前'——一句话的力量。"
                ),
                target_skills=[SkillTarget.DIALOGUE_WRITING, SkillTarget.PLOT_DESIGN, SkillTarget.CHARACTER_BUILDING],
                actionable_tips=[
                    "学习'绕'的叙事：通过看似离题叙述逼近核心",
                    "对话即情节：让对话本身推动故事发展",
                    "在朴素对话中埋入人生智慧让读者回味",
                    "用对话展示人物关系：谁和谁能说得上话",
                    "长篇对话要有节奏：紧张对话和松弛对话交替",
                ], difficulty="advanced",
            ),

            BookInsight(
                book_name="半生缘", author="张爱玲", category="文学名著",
                core_technique="苍凉美学与心理洞察",
                detailed_insight=(
                    "张爱玲技法在《半生缘》中炉火纯青。1)心理描写精准：不直接写心理而是通过动作、对话、环境折射心理。"
                    "曼桢被囚禁时心理状态通过她数日子细节呈现。2)时间残酷：'我们回不去了'——六字写尽半生沧桑。"
                    "3)苍凉美学：不写大团圆写'遗憾的美'。错过、误会、时机不对——'不完美'比完美更有文学力量。"
                    "4)细节象征：手套、戒指、信——日常物品承载情感记忆成为情节推动力。"
                ),
                target_skills=[SkillTarget.EMOTIONAL_DESIGN, SkillTarget.CHARACTER_BUILDING, SkillTarget.SCENE_DESCRIPTION],
                actionable_tips=[
                    "通过动作和细节折射心理而非直接说明",
                    "用日常物品承载情感记忆(手套/戒指/信)",
                    "写'遗憾的美'：不完美结局往往更有力量",
                    "时间跨度处理：用关键细节标记时间流逝",
                    "对话中未尽之言比说出来话更重要",
                ], difficulty="advanced",
            ),

            BookInsight(
                book_name="金锁记", author="张爱玲", category="文学名著",
                core_technique="意象系统与病态心理刻画",
                detailed_insight=(
                    "《金锁记》是张爱玲技法集中展示。1)月亮意象系统：三十年前月亮、年轻人眼中月亮、老年人眼中月亮——"
                    "同意象在不同语境产生不同含义构成完整意象系统。2)病态心理渐进刻画：曹七巧从受害者变加害者，"
                    "每步转变都有充分心理铺垫。3)语言华丽与精准：张爱玲语言如锦缎华丽但不空洞，每比喻都精准服务人物和主题。"
                ),
                target_skills=[SkillTarget.CHARACTER_BUILDING, SkillTarget.EMOTIONAL_DESIGN, SkillTarget.SCENE_DESCRIPTION],
                actionable_tips=[
                    "设计贯穿全文意象系统(如月亮)在不同语境赋予不同含义",
                    "角色转变要有渐进铺垫：受害者→加害者每步都要合理",
                    "华丽语言要服务内容：每比喻都要有叙事功能",
                    "写病态心理时保持克制：让读者自己判断非作者评判",
                    "中篇小说密度：每场景每细节都不能浪费",
                ], difficulty="advanced",
            ),

            BookInsight(
                book_name="长恨歌", author="王安忆", category="文学名著",
                core_technique="城市叙事与女性命运史诗",
                detailed_insight=(
                    "王安忆用细腻笔触写上海和女人。1)城市作为角色：上海不是背景而是有生命角色。弄堂、鸽子、流言——"
                    "城市有自己呼吸和心跳。2)女性命运史诗结构：王琦瑶一生是上海40年变迁缩影。个人史=城市史。"
                    "3)细密叙事：不厌其烦描写日常生活细节——穿衣、吃饭、聊天——在日常中见时代见命运。"
                    "4)时间层次：过去和现在不断交织，回忆不是插叙而是叙事有机部分。"
                ),
                target_skills=[SkillTarget.WORLD_BUILDING, SkillTarget.CHARACTER_BUILDING, SkillTarget.SCENE_DESCRIPTION],
                actionable_tips=[
                    "将场景(城市/村镇/世界)当角色写赋予生命和性格",
                    "个人命运与时代/世界变迁交织：个人史=世界史",
                    "在日常细节中展示时代特征：穿衣/吃饭/聊天反映大背景",
                    "时间层次处理：过去和现在交织，回忆是叙事有机部分",
                    "细密叙事需控制节奏：密中有疏避免读者疲劳",
                ], difficulty="advanced",
            ),

            BookInsight(
                book_name="在细雨中呼喊", author="余华", category="文学名著",
                core_technique="记忆叙事与时间重构",
                detailed_insight=(
                    "余华第一部长篇展示记忆叙事独特魅力。1)记忆非线性：不按时间顺序而按记忆逻辑——重要先回忆不重要的跳过。"
                    "这种结构更接近真实记忆方式。2)儿童视角残酷：用孩子眼睛看成人世界荒诞和残酷，天真叙述与残酷内容形成巨大张力。"
                    "3)碎片拼贴：看似零散回忆碎片最终拼成完整图景。"
                ),
                target_skills=[SkillTarget.PLOT_DESIGN, SkillTarget.EMOTIONAL_DESIGN, SkillTarget.SCENE_DESCRIPTION],
                actionable_tips=[
                    "尝试记忆叙事：按情感重要性而非时间顺序组织故事",
                    "碎片拼贴结构：零散片段最终拼成完整图景",
                    "儿童视角+残酷内容=巨大张力",
                    "非线性叙事需锚点：用重复意象/场景帮助读者定位",
                    "记忆叙事适合第一人称增强真实感和沉浸感",
                ], difficulty="advanced",
            ),

            BookInsight(
                book_name="青蛇", author="李碧华", category="文学名著",
                core_technique="经典重构与女性视角翻转",
                detailed_insight=(
                    "李碧华展示如何重构经典故事。1)视角翻转：白蛇传主角从白素贞变小青，从配角视角重新讲述经典。"
                    "2)情欲书写：大胆而细腻的情欲描写，不低俗而有文学性。3)古今交织：古代故事融入现代意识让经典与当代对话。"
                    "4)语言妖娆：李碧华语言风格独特——妖娆、犀利、一针见血。"
                ),
                target_skills=[SkillTarget.PLOT_DESIGN, SkillTarget.CHARACTER_BUILDING, SkillTarget.WORLD_BUILDING],
                actionable_tips=[
                    "经典重构核心是视角翻转：从配角/反派角度重新讲述",
                    "情欲描写要有文学性：含蓄比直白更有力",
                    "古代背景可融入现代意识让故事与当代读者对话",
                    "语言风格要服务故事基调：妖娆故事用妖娆语言",
                    "重构经典时保留核心元素，改变的是视角和解读",
                ], difficulty="intermediate",
            ),

            BookInsight(
                book_name="撒哈拉的故事", author="三毛", category="文学名著",
                core_technique="异域书写与真诚的力量",
                detailed_insight=(
                    "三毛展示'真诚'的写作力量。1)异域书写：撒哈拉沙漠在三毛笔下不是猎奇背景而是真实生活空间。"
                    "异域感来自细节真实而非刻意渲染。2)第一人称魅力：三毛散文体小说让读者感觉在读朋友信——亲切真诚不设防。"
                    "3)苦难中浪漫：在艰苦环境中发现美和趣味——这种态度比苦难本身更打动人心。4)短篇连缀结构：每故事独立成篇但合在一起构成完整图景。"
                ),
                target_skills=[SkillTarget.SCENE_DESCRIPTION, SkillTarget.EMOTIONAL_DESIGN, SkillTarget.WORLD_BUILDING],
                actionable_tips=[
                    "异域/奇幻世界真实感来自细节而非渲染",
                    "第一人称叙事要真诚：像给朋友写信一样写作",
                    "在黑暗中发现光：苦难中温情比单纯苦难更动人",
                    "短篇连缀结构：独立故事+整体图景",
                    "旅行/异域题材核心不是风景而是人",
                ], difficulty="intermediate",
            ),

            BookInsight(
                book_name="雪国", author="川端康成", category="文学名著",
                core_technique="日本美学与虚无之美",
                detailed_insight=(
                    "川端康成展示日本美学文学表达。1)物哀美学：对万物消逝的感伤和审美。雪国美是虚幻的美、即将消逝的美。"
                    "2)留白与暗示：大量留白，不写比写更有力。岛村和驹子关系始终朦胧，正是朦胧产生美感。"
                    "3)季节感：雪景不仅是背景更是主题和情绪载体。4)开头神来之笔：'穿过县界长长的隧道，便是雪国。'——一句话建立整个世界。"
                ),
                target_skills=[SkillTarget.SCENE_DESCRIPTION, SkillTarget.EMOTIONAL_DESIGN, SkillTarget.WORLD_BUILDING],
                actionable_tips=[
                    "学习'物哀'美学：写即将消逝的美比永恒美更动人",
                    "大量留白：不写比写更有力让读者自己填补空白",
                    "季节/环境作为情绪载体：雪=纯净+寒冷+虚幻",
                    "开头一句话建立世界：用最精炼语言锚定整个故事氛围",
                    "朦胧人物关系：不定义不解释保持暧昧美感",
                ], difficulty="advanced",
            ),

            BookInsight(
                book_name="世说新语", author="刘义庆", category="文学名著",
                core_technique="笔记体叙事与人物品藻",
                detailed_insight=(
                    "《世说新语》是笔记体小说源头。1)极简叙事：最短故事只有十几个字但人物形象跃然纸上。"
                    "2)人物品藻：通过一个动作、一句话、一个细节品评人物。'以事写人'比直接描述性格更有效。"
                    "3)分类结构：按人物类型(德行/言语/政事/文学等)分类而非按时间或情节。适合构建人物群像。"
                    "4)留白极致：只写最精彩片段其余留给读者想象。"
                ),
                target_skills=[SkillTarget.CHARACTER_BUILDING, SkillTarget.DIALOGUE_WRITING, SkillTarget.SCENE_DESCRIPTION],
                actionable_tips=[
                    "学习'以事写人'：通过一个动作/一句话展示性格",
                    "极简叙事魅力：删掉所有不必要过渡和解释",
                    "分类结构组织人物群像：按类型而非时间排列",
                    "只写最精彩片段：每片段都要有独立闪光点",
                    "笔记体适合构建人物素材库和世界观碎片",
                ], difficulty="intermediate",
            ),

            BookInsight(
                book_name="浮生六记", author="沈复", category="文学名著",
                core_technique="自传体散文与日常诗意",
                detailed_insight=(
                    "《浮生六记》展示如何在日常生活中发现诗意。1)日常诗意：种花、喝茶、赏月、游山——最普通生活在沈复笔下"
                    "充满诗意。不是生活本身诗意而是观看生活的眼光诗意。2)真情实感：写妻子芸娘部分感人至深因为每细节都真实。"
                    "3)闲笔妙用：看似无关闲笔(怎么种兰花、怎么布置房间)反而最见性情。4)哀而不伤：写苦难时保持克制不煽情但动人。"
                ),
                target_skills=[SkillTarget.SCENE_DESCRIPTION, SkillTarget.EMOTIONAL_DESIGN, SkillTarget.CHARACTER_BUILDING],
                actionable_tips=[
                    "在日常中发现诗意：不是写什么而是怎么看待",
                    "真情实感力量：真实细节比虚构情节更动人",
                    "闲笔见性情：看似无关细节最能展示角色性格",
                    "写苦难时保持克制：哀而不伤比煽情更有力",
                    "自传体叙事：用'我'视角写增强真实感和亲切感",
                ], difficulty="intermediate",
            ),

            BookInsight(
                book_name="文化苦旅", author="余秋雨", category="文学名著",
                core_technique="文化大散文与历史想象",
                detailed_insight=(
                    "余秋雨开创'文化大散文'写法。1)历史现场还原：站在古迹前想象历史——'在场感'让历史不再是枯燥记载。"
                    "2)学者+文人双重身份：学术功底保证内容深度，文学才华保证表达优美。3)宏大叙事与个人感悟结合："
                    "从个人旅行体验上升到文明反思。4)语言节奏感：长短句交替、排比与对仗，语言本身有音乐性。"
                ),
                target_skills=[SkillTarget.WORLD_BUILDING, SkillTarget.SCENE_DESCRIPTION, SkillTarget.EMOTIONAL_DESIGN],
                actionable_tips=[
                    "历史/世界观要有'在场感'：让读者感觉身临其境",
                    "宏大叙事需个人视角锚点：从具体体验上升到普遍思考",
                    "语言要有节奏感：长短句交替、排比与散句交替",
                    "知识性内容要有情感温度：冷知识+热情感",
                    "游记/探索类叙事：空间移动带动思考和情感变化",
                ], difficulty="intermediate",
            ),

            BookInsight(
                book_name="病隙碎笔", author="史铁生", category="文学名著",
                core_technique="苦难中的哲学思考与随笔体",
                detailed_insight=(
                    "史铁生在病痛中写下思考展示写作终极意义。1)苦难作为思考起点：不是抱怨苦难而是从苦难出发思考生命意义。"
                    "2)随笔体自由：不追求体系想到哪写到哪但每碎片都有深度。3)真诚到残酷：对自己处境和想法毫不掩饰。"
                    "4)宗教维度引入：对信仰思考赋予文本超越性。"
                ),
                target_skills=[SkillTarget.EMOTIONAL_DESIGN, SkillTarget.CHARACTER_BUILDING, SkillTarget.WORLD_BUILDING],
                actionable_tips=[
                    "角色苦难要有哲学深度：不只是受苦而是通过受苦理解生命",
                    "随笔体适合内心独白和哲学思考",
                    "真诚是最高技巧：不掩饰不美化不煽情",
                    "为角色设计信仰/信念系统赋予行为更深层动机",
                    "苦难书写要避免自怜：思考比感受更重要",
                ], difficulty="advanced",
            ),

            BookInsight(
                book_name="人间草木/人间有至味", author="汪曾祺", category="文学名著",
                core_technique="平淡中的韵味与生活美学",
                detailed_insight=(
                    "汪曾祺文字如清茶平淡中有至味。1)平淡力量：不追求华丽辞藻用最朴素语言写最普通事物但读来韵味悠长。"
                    "2)食物即文化：写吃不是写食谱而是写人情、写故乡、写记忆。3)短句节奏：汪曾祺句子很短但节奏感极好。"
                    "4)幽默感：不刻意幽默而是对生活会心一笑。"
                ),
                target_skills=[SkillTarget.SCENE_DESCRIPTION, SkillTarget.DIALOGUE_WRITING, SkillTarget.EMOTIONAL_DESIGN],
                actionable_tips=[
                    "平淡中有至味：朴素语言+深厚底蕴",
                    "通过日常事物(食物/植物)写人情和记忆",
                    "短句节奏感：句子短但节奏不急促",
                    "幽默要不刻意：对生活会心一笑而非刻意搞笑",
                    "生活细节积累：好日常描写来自对生活细致观察",
                ], difficulty="intermediate",
            ),

            BookInsight(
                book_name="雅舍小品", author="梁实秋", category="文学名著",
                core_technique="幽默小品文与绅士的笔调",
                detailed_insight=(
                    "梁实秋小品文展示幽默最高境界。1)绅士幽默：不尖刻不低俗不卖弄，温文尔雅中见智慧。"
                    "2)小题大做：从最普通话题(男人/女人/吃饭/睡觉)写出大道理。3)引经据典自然：中西典故信手拈来但不让人觉得掉书袋。"
                    "4)结尾艺术：每篇结尾都有点睛之笔让人回味。"
                ),
                target_skills=[SkillTarget.DIALOGUE_WRITING, SkillTarget.SCENE_DESCRIPTION, SkillTarget.EMOTIONAL_DESIGN],
                actionable_tips=[
                    "幽默最高境界是温文尔雅中智慧",
                    "小题大做：从日常小事写出普遍道理",
                    "引经据典要自然：知识是底蕴不是装饰",
                    "每段/每章结尾要有余韵：让人回味的一句话",
                    "小品文结构适合角色随笔/番外/日常章节",
                ], difficulty="intermediate",
            ),

            BookInsight(
                book_name="海边的房间", author="黄丽群", category="文学名著",
                core_technique="都市奇情与精准的冷酷",
                detailed_insight=(
                    "黄丽群短篇展示当代华语写作新可能。1)都市感精准捕捉：现代都市人孤独、疏离、扭曲——"
                    "用冷静到近乎冷酷笔调写出。2)反转艺术：每故事都有出人意料反转但反转不是噱头而是人性揭示。"
                    "3)语言精密度：每词都经精心选择没有废字。"
                ),
                target_skills=[SkillTarget.PLOT_DESIGN, SkillTarget.EMOTIONAL_DESIGN, SkillTarget.CHARACTER_BUILDING],
                actionable_tips=[
                    "都市题材要有当代感：写当下孤独和疏离",
                    "反转要服务人性揭示不能为反转而反转",
                    "语言要精密：每词都要有存在理由",
                    "冷静笔调写激烈情感：反差产生力量",
                    "短篇小说密度：每细节都要承担多重功能",
                ], difficulty="advanced",
            ),

            BookInsight(
                book_name="望江南", author="王旭烽", category="文学名著",
                core_technique="茶文化叙事与家族史诗",
                detailed_insight=(
                    "王旭烽将茶文化与家族叙事完美融合。1)专业知识文学化：茶知识不是枯燥科普而是融入人物命运和情节发展。"
                    "2)江南美学呈现：语言如江南烟雨温润细腻。3)家族叙事代际结构：通过几代人命运展示时代变迁。"
                ),
                target_skills=[SkillTarget.WORLD_BUILDING, SkillTarget.SCENE_DESCRIPTION, SkillTarget.PLOT_DESIGN],
                actionable_tips=[
                    "专业知识要融入情节和人物不能是独立知识板块",
                    "地域美学通过语言风格呈现：江南故事用江南语言",
                    "家族叙事用代际结构：每代人面对不同时代命题",
                    "选一个专业领域(茶/酒/瓷/画)作为故事文化根基",
                    "文化底蕴是故事底色不是炫耀资本",
                ], difficulty="intermediate",
            ),

            BookInsight(
                book_name="焦虑的人", author="弗雷德里克·巴克曼", category="文学名著",
                core_technique="多视角拼图与温暖反转",
                detailed_insight=(
                    "巴克曼展示如何写'温暖'故事。1)多视角拼图：每角色看到事件一部分，读者拼凑完整图景。"
                    "2)温暖反转：你以为的坏人其实有苦衷，你以为的蠢事其实有深意。3)幽默与温情平衡：笑中带泪叙事节奏。"
                ),
                target_skills=[SkillTarget.PLOT_DESIGN, SkillTarget.EMOTIONAL_DESIGN, SkillTarget.CHARACTER_BUILDING],
                actionable_tips=[
                    "多视角拼图：每角色只看到真相一部分",
                    "温暖反转：让读者重新审视之前对人物判断",
                    "幽默和温情交替：笑中带泪节奏",
                    "每角色都要有让人共情的点",
                    "群像剧中每角色都要有自己完整弧线",
                ], difficulty="intermediate",
            ),

            BookInsight(
                book_name="父亲", author="梁晓声", category="文学名著",
                core_technique="亲情书写与时代记忆",
                detailed_insight=(
                    "梁晓声写父亲写出整个时代。1)从个人到时代：写父亲一生就是写中国几十年变迁。"
                    "2)细节情感承载：父亲某个习惯、某句话、某个动作——具体细节承载深厚情感。"
                    "3)不煽情的深情：最深感情用最朴素语言表达。"
                ),
                target_skills=[SkillTarget.EMOTIONAL_DESIGN, SkillTarget.CHARACTER_BUILDING, SkillTarget.SCENE_DESCRIPTION],
                actionable_tips=[
                    "亲情书写：通过具体细节承载情感",
                    "个人史=时代史：一个人一生折射整个时代",
                    "不煽情的深情：最深感情用最朴素语言",
                    "为角色设计'标志性细节'：一个习惯/动作/口头禅",
                    "代际关系是长线情感张力重要来源",
                ], difficulty="intermediate",
            ),

            BookInsight(
                book_name="余华中短篇小说", author="余华", category="文学名著",
                core_technique="先锋叙事与暴力的诗意化",
                detailed_insight=(
                    "余华短篇展示先锋文学技法。1)暴力冷静书写：用最平静语调写最暴力事，反差产生震撼。"
                    "2)重复与变奏：同一事件从不同角度反复书写每次都有新揭示。3)现实荒诞化：现实本身比虚构更荒诞只需如实写出。"
                ),
                target_skills=[SkillTarget.EMOTIONAL_DESIGN, SkillTarget.PLOT_DESIGN, SkillTarget.SCENE_DESCRIPTION],
                actionable_tips=[
                    "冷静写暴力/冲突：平静语调+激烈内容=巨大张力",
                    "重复与变奏：同一主题从不同角度反复书写",
                    "现实荒诞感：如实写出有时比刻意虚构更有力",
                    "短篇密度：每字都要承担多重功能",
                    "先锋技法要服务内容不能为先锋而先锋",
                ], difficulty="advanced",
            ),

            BookInsight(
                book_name="有如候鸟", author="周晓枫", category="文学名著",
                core_technique="散文的密度与感官的极致开发",
                detailed_insight=(
                    "周晓枫散文展示语言极致密度。1)感官全方位开发：视觉、听觉、嗅觉、触觉、味觉——每种感官都被推到极致。"
                    "2)比喻密集轰炸：一个接一个比喻每个都精准而新鲜。3)散文叙事性：在散文中融入故事元素。"
                ),
                target_skills=[SkillTarget.SCENE_DESCRIPTION, SkillTarget.EMOTIONAL_DESIGN],
                actionable_tips=[
                    "感官描写极致：每种感官都要被充分调动",
                    "比喻要密集而精准：一个不够就用两个三个",
                    "散文可叙事，叙事可散文化",
                    "语言密度：每句子都要有信息量和美感",
                ], difficulty="advanced",
            ),

            BookInsight(
                book_name="张枣的诗", author="张枣", category="文学名著",
                core_technique="诗歌语言与意象的陌生化",
                detailed_insight=(
                    "张枣诗歌为小说语言提供丰富养分。1)意象陌生化：'只要想起一生中后悔的事，梅花便落满了南山'——"
                    "将抽象情感用具体而陌生意象表达。2)语言音乐性：张枣诗有极强音乐感可以朗读。"
                    "3)古典与现代融合：传统意象用现代语言重新表达。"
                ),
                target_skills=[SkillTarget.SCENE_DESCRIPTION, SkillTarget.EMOTIONAL_DESIGN, SkillTarget.DIALOGUE_WRITING],
                actionable_tips=[
                    "学习意象陌生化：用新鲜具体意象表达抽象情感",
                    "语言要有音乐性：写完后朗读检查节奏",
                    "古典意象+现代语言=独特文学质感",
                    "诗歌技巧可用于小说中关键抒情段落",
                ], difficulty="advanced",
            ),

            BookInsight(
                book_name="水问", author="简媜", category="文学名著",
                core_technique="诗化散文与女性书写",
                detailed_insight=(
                    "简媜散文如诗如画。1)诗化语言：散文语言密度接近诗歌。2)自然意象丰富运用：水、月、花、树——"
                    "自然意象承载情感和哲思。3)女性视角独特：细腻、敏感、深刻。"
                ),
                target_skills=[SkillTarget.SCENE_DESCRIPTION, SkillTarget.EMOTIONAL_DESIGN],
                actionable_tips=[
                    "诗化语言用于关键场景描写",
                    "自然意象承载情感：水=柔情/流逝，月=思念/孤独",
                    "女性视角细腻：关注男性视角易忽略细节",
                ], difficulty="intermediate",
            ),

            BookInsight(
                book_name="武则天", author="苏童", category="文学名著",
                core_technique="历史人物的心理重构",
                detailed_insight=(
                    "苏童展示如何写历史人物。1)历史人物心理化：不写历史事件写人物内心。"
                    "2)权力与性别交织：女性在男权社会中生存策略。3)幽暗意识书写：不回避人性阴暗面。"
                ),
                target_skills=[SkillTarget.CHARACTER_BUILDING, SkillTarget.EMOTIONAL_DESIGN, SkillTarget.WORLD_BUILDING],
                actionable_tips=[
                    "历史/架空人物要有心理深度：不只写做了什么更写为什么",
                    "权力斗争核心是人性而非计谋",
                    "女性角色复杂性：不只是'强'或'弱'二元",
                    "幽暗意识：好角色要有阴暗面",
                ], difficulty="intermediate",
            ),
        ]
        self.insights.extend(lit)

    # ================================================================
    # C. 工具词典
    # ================================================================

    def _init_reference_dictionaries(self):
        dicts = [

            BookInsight(
                book_name="写作成语词典", author="多人", category="工具词典",
                core_technique="成语的精准运用与语境适配",
                detailed_insight=(
                    "成语是汉语写作精华但需精准运用。1)成语语境适配：同意思有多个成语可选，选最贴合语境的。"
                    "2)成语节奏功能：四字成语天然有节奏感可调节句子节奏。3)成语活用与化用：不一定原封不动使用可拆解化用。"
                    "4)避免成语堆砌：成语是调味料不是主菜。每千字3-5个为宜。"
                ),
                target_skills=[SkillTarget.SCENE_DESCRIPTION, SkillTarget.DIALOGUE_WRITING],
                actionable_tips=[
                    "建立个人常用成语库按场景/情绪分类",
                    "成语选择三原则：准确、新鲜、有节奏感",
                    "每千字使用3-5个成语为宜过多则显堆砌",
                    "学会化用成语：'望梅止渴'→'那希望如远方的梅林'",
                    "战斗/动作场景多用动词性成语增加节奏感",
                ], difficulty="beginner",
            ),

            BookInsight(
                book_name="文学描写词典", author="多人", category="工具词典",
                core_technique="分类描写范本与多角度描写法",
                detailed_insight=(
                    "《文学描写词典》按主题收录经典文学作品中描写片段。1)多角度描写：同一事物可从外观/功能/情感/象征多角度描写。"
                    "2)描写层次：由远及近、由外到内、由整体到细节。3)动态描写vs静态描写：让静止事物'动'起来。"
                ),
                target_skills=[SkillTarget.SCENE_DESCRIPTION, SkillTarget.WORLD_BUILDING],
                actionable_tips=[
                    "学习多角度描写：同一场景从不同角度写3个版本",
                    "描写要有层次：远→近、外→内、整体→细节",
                    "静态事物动态化：'山'→'山峦起伏如巨兽的脊背'",
                    "建立个人描写片段库按场景类型分类",
                ], difficulty="beginner",
            ),

            BookInsight(
                book_name="最佳描写系列词典(景色/外貌/心理/男性/女性)", author="多人", category="工具词典",
                core_technique="专项描写的词汇库与模板化思维",
                detailed_insight=(
                    "系列描写词典提供按性别、类型分类的描写范本。1)性别差异描写：男女描写重点和语言风格应有差异。"
                    "2)外貌描写功能化：不只是'长什么样'更是性格/身份/命运暗示。3)心理描写层次：表层想法→深层动机→潜意识。"
                    "4)景色描写情绪化：同一景色在不同情绪下应有不同写法。"
                ),
                target_skills=[SkillTarget.SCENE_DESCRIPTION, SkillTarget.CHARACTER_BUILDING, SkillTarget.EMOTIONAL_DESIGN],
                actionable_tips=[
                    "外貌描写要暗示性格和命运：鹰钩鼻=精明/阴险",
                    "心理描写三层：想法→动机→潜意识",
                    "景色随情绪变化：开心的雨=滋润，悲伤的雨=哭泣",
                    "男性描写重行动和力量，女性描写重细节和气质",
                    "建立分性别、分类型的描写模板库",
                ], difficulty="intermediate",
            ),

            BookInsight(
                book_name="写作借鉴词典", author="多人", category="工具词典",
                core_technique="经典句式的学习与化用",
                detailed_insight=(
                    "《写作借鉴词典》收录经典文学作品中精彩句式。1)句式学习：分析经典句子结构理解为什么好。"
                    "2)化用而非抄袭：学习句式结构填入自己内容。3)句式多样性：长短句、整散句、陈述/疑问/感叹交替。"
                    "长短句比例建议：短句30%+中句50%+长句20%。"
                ),
                target_skills=[SkillTarget.DIALOGUE_WRITING, SkillTarget.SCENE_DESCRIPTION],
                actionable_tips=[
                    "每天分析一个经典句式：结构+节奏+用词",
                    "化用练习：保留句式结构替换内容",
                    "检查句式多样性：连续5句不能同一句式",
                    "长短句比例：短句30%+中句50%+长句20%",
                ], difficulty="intermediate",
            ),

            BookInsight(
                book_name="中国神话人物词典", author="多人", category="工具词典",
                core_technique="神话原型的现代转化",
                detailed_insight=(
                    "《中国神话人物词典》是玄幻/仙侠写作宝库。1)神话原型提取：每神话人物代表一种原型(英雄/智者/叛逆者/母亲)。"
                    "2)神话体系构建：中国神话非单一体系而是多元融合。3)神话现代转化：古老神话用现代叙事重新激活。"
                ),
                target_skills=[SkillTarget.WORLD_BUILDING, SkillTarget.CHARACTER_BUILDING, SkillTarget.PLOT_DESIGN],
                actionable_tips=[
                    "从神话中提取角色原型：孙悟空=叛逆英雄，观音=慈悲导师",
                    "构建神话体系：不同来源神话如何共存于同一世界",
                    "神话现代转化：古老神话+现代价值观=新鲜故事",
                    "神话人物词典是玄幻/仙侠世界观素材宝库",
                ], difficulty="intermediate",
            ),

            BookInsight(
                book_name="读书词典", author="多人", category="工具词典",
                core_technique="跨学科知识积累与融会贯通",
                detailed_insight=(
                    "《读书词典》涵盖各学科基础知识。1)跨学科知识重要性：好小说需要历史/哲学/科学/艺术等多学科支撑。"
                    "2)知识文学转化：专业知识要转化为读者能理解的叙事。3)知识储备深度决定小说厚度。"
                ),
                target_skills=[SkillTarget.WORLD_BUILDING, SkillTarget.PLOT_DESIGN],
                actionable_tips=[
                    "建立跨学科知识卡片：历史/哲学/科学/艺术",
                    "专业知识要'翻译'成读者能理解的叙事",
                    "知识储备深度=小说厚度",
                    "定期阅读非虚构类书籍扩充知识面",
                ], difficulty="intermediate",
            ),
        ]
        self.insights.extend(dicts)

    # ================================================================
    # D. 文化哲学
    # ================================================================

    def _init_cultural_philosophy(self):
        culture = [

            BookInsight(
                book_name="人间词话", author="王国维", category="文化哲学",
                core_technique="境界说与三层审美结构",
                detailed_insight=(
                    "王国维'境界说'对小说写作有深刻启示。1)三层境界：'昨夜西风凋碧树，独上高楼，望尽天涯路'(立)→"
                    "'衣带渐宽终不悔，为伊消得人憔悴'(守)→'众里寻他千百度，蓦然回首，那人却在灯火阑珊处'(得)。"
                    "2)有我之境vs无我之境：'泪眼问花花不语'是有我，'采菊东篱下，悠然见南山'是无我。"
                    "3)隔与不隔：好描写让读者感觉'如在目前'(不隔)，差描写让读者感觉'雾里看花'(隔)。"
                ),
                target_skills=[SkillTarget.SCENE_DESCRIPTION, SkillTarget.EMOTIONAL_DESIGN, SkillTarget.WORLD_BUILDING],
                actionable_tips=[
                    "用'不隔'原则检查描写：读者能否'看到'你写的场景？",
                    "角色成长可对应三层境界：立志→坚守→顿悟",
                    "有我之境=主观情感投射，无我之境=客观呈现",
                    "好文字让读者忘记文字本身直接'看到'画面",
                ], difficulty="advanced",
            ),

            BookInsight(
                book_name="人类群星闪耀时", author="斯蒂芬·茨威格", category="文化哲学",
                core_technique="历史关键时刻的戏剧化书写",
                detailed_insight=(
                    "茨威格展示如何将历史写成比小说更精彩故事。1)关键时刻聚焦：不写一生只写决定命运那个瞬间。"
                    "2)心理描写深度：历史人物内心世界被充分挖掘。3)叙事节奏掌控：在历史事实基础上进行文学化节奏设计。"
                ),
                target_skills=[SkillTarget.PLOT_DESIGN, SkillTarget.CHARACTER_BUILDING, SkillTarget.EMOTIONAL_DESIGN],
                actionable_tips=[
                    "聚焦关键时刻：不写角色一生写决定命运瞬间",
                    "历史/架空人物心理深度决定故事感染力",
                    "在事实基础上进行文学化节奏设计",
                    "每角色都要有'群星闪耀时'——决定性高光时刻",
                ], difficulty="intermediate",
            ),

            BookInsight(
                book_name="苏东坡传", author="林语堂", category="文化哲学",
                core_technique="人物传记的文学化与性格魅力塑造",
                detailed_insight=(
                    "林语堂笔下苏东坡是中国文化中最有魅力人格。1)多才多艺角色设计：苏东坡是诗人/画家/美食家/工程师/政治家——"
                    "多维度让角色立体。2)逆境中豁达：最高级人格魅力是在苦难中保持幽默和热爱。"
                    "3)缺点让角色可爱：苏东坡固执、嘴快、不合时宜——缺点不是减分项而是加分项。"
                ),
                target_skills=[SkillTarget.CHARACTER_BUILDING, SkillTarget.EMOTIONAL_DESIGN],
                actionable_tips=[
                    "给角色多维度才能：不只是'强者'还有才艺和趣味",
                    "逆境中态度定义角色：苦难中保持幽默=最高级魅力",
                    "缺点让角色可爱：完美=无趣，有缺点=真实",
                    "人物传记写法可用于角色背景故事设计",
                ], difficulty="intermediate",
            ),

            BookInsight(
                book_name="陶庵梦忆", author="张岱", category="文化哲学",
                core_technique="回忆录式的繁华与苍凉",
                detailed_insight=(
                    "张岱在明亡后回忆昔日繁华产生独特文学效果。1)繁华与苍凉对比：越是写昔日繁华越显出今日苍凉。"
                    "2)细节深情：湖心亭看雪、金山夜戏——具体场景承载深沉情感。3)小品文精致：每篇短小精悍但余韵悠长。"
                ),
                target_skills=[SkillTarget.EMOTIONAL_DESIGN, SkillTarget.SCENE_DESCRIPTION],
                actionable_tips=[
                    "繁华与苍凉对比：写乐景是为衬哀情",
                    "具体场景承载深沉情感：一个场景胜过千言万语",
                    "小品文结构适合角色回忆/番外",
                    "回忆叙事：过去和现在交织产生情感张力",
                ], difficulty="advanced",
            ),

            BookInsight(
                book_name="万古江河", author="许倬云", category="文化哲学",
                core_technique="大历史观与文明的比较视野",
                detailed_insight=(
                    "许倬云大历史观为世界观构建提供宏大框架。1)文明比较视野：中国文化非孤立而是在与其他文明互动中形成。"
                    "2)长时段变迁：以千年为单位看历史看到深层结构变化。3)民间视角：不只写帝王将相更写普通人生活。"
                ),
                target_skills=[SkillTarget.WORLD_BUILDING, SkillTarget.PLOT_DESIGN],
                actionable_tips=[
                    "世界观构建要有比较视野：不同文明/种族/势力互动",
                    "设计'长时段'历史变迁：千年尺度世界史",
                    "不只写顶层人物也要写普通人在世界中生活",
                    "文明碰撞和融合是史诗级冲突来源",
                ], difficulty="advanced",
            ),

            BookInsight(
                book_name="乡土中国", author="费孝通", category="文化哲学",
                core_technique="社会结构的文学转化",
                detailed_insight=(
                    "费孝通对中国乡土社会分析为小说提供深层社会结构。1)差序格局：中国社会人际关系如涟漪以自我为中心向外扩散。"
                    "2)熟人社会：乡土社会是熟人社会规则不同于陌生人社会。3)礼治秩序：维持社会秩序的是礼而非法。"
                ),
                target_skills=[SkillTarget.WORLD_BUILDING, SkillTarget.CHARACTER_BUILDING],
                actionable_tips=[
                    "设计社会结构：不同社会有不同人际关系模式",
                    "差序格局可用于设计宗门/家族人际关系",
                    "熟人社会vs陌生人社会规则差异=冲突来源",
                    "礼治vs法治冲突是传统vs现代经典主题",
                ], difficulty="advanced",
            ),

            BookInsight(
                book_name="存在主义的咖啡馆", author="莎拉·贝克韦尔", category="文化哲学",
                core_technique="哲学思想的叙事化",
                detailed_insight=(
                    "贝克韦尔将存在主义哲学写成引人入胜故事。1)哲学思想叙事化：把抽象思想变成具体人物和故事。"
                    "2)思想与人生交织：哲学家思想来自他们人生经历。3)自由/选择/责任：存在主义核心主题是强大故事驱动力。"
                ),
                target_skills=[SkillTarget.CHARACTER_BUILDING, SkillTarget.EMOTIONAL_DESIGN, SkillTarget.WORLD_BUILDING],
                actionable_tips=[
                    "哲学思想要叙事化：通过角色选择和行动体现思想",
                    "自由/选择/责任是强大角色驱动力",
                    "角色世界观来自其人生经历",
                    "存在主义主题：荒谬/自由/焦虑/本真性",
                ], difficulty="advanced",
            ),

            BookInsight(
                book_name="拥抱逝水年华", author="阿兰·德波顿", category="文化哲学",
                core_technique="日常生活的哲学解读",
                detailed_insight=(
                    "德波顿展示如何从日常生活中提炼哲学。1)日常深度：最普通事物(火车/机场/食物)都有哲学维度。"
                    "2)普鲁斯特启示：记忆、时间、爱情——文学如何探讨永恒主题。3)雅俗共赏：深奥思想用通俗语言表达。"
                ),
                target_skills=[SkillTarget.EMOTIONAL_DESIGN, SkillTarget.SCENE_DESCRIPTION],
                actionable_tips=[
                    "从日常中提炼深度：普通场景+哲学思考=文学质感",
                    "记忆和时间是永恒主题：如何用叙事处理时间",
                    "深奥思想用通俗语言：不装腔作势",
                ], difficulty="intermediate",
            ),

            BookInsight(
                book_name="唐代衣食住行研究", author="黄正建", category="文化哲学",
                core_technique="历史日常生活的精准还原",
                detailed_insight=(
                    "对唐代日常生活研究为历史/架空小说提供坚实细节基础。1)衣食住行真实性：读者通过日常细节感受时代真实。"
                    "2)物质文化叙事功能：一件衣服、一顿饭可展示身份/性格/时代。3)细节准确性建立读者信任。"
                ),
                target_skills=[SkillTarget.WORLD_BUILDING, SkillTarget.SCENE_DESCRIPTION],
                actionable_tips=[
                    "架空世界也要有'衣食住行'细节设计",
                    "物质文化展示身份和性格：穿什么=是什么人",
                    "细节准确性建立读者对世界信任",
                    "研究真实历史为架空世界提供灵感",
                ], difficulty="intermediate",
            ),
        ]
        self.insights.extend(culture)

    # ================================================================
    # 查询与分发接口
    # ================================================================

    def get_all_insights(self) -> List[BookInsight]:
        return self.insights

    def get_insights_by_skill(self, skill: SkillTarget) -> List[BookInsight]:
        return [i for i in self.insights if skill in i.target_skills]

    def get_insights_by_category(self, category: str) -> List[BookInsight]:
        return [i for i in self.insights if i.category == category]

    def get_insights_by_difficulty(self, difficulty: str) -> List[BookInsight]:
        return [i for i in self.insights if i.difficulty == difficulty]

    def get_skill_knowledge_map(self) -> Dict[str, List[Dict]]:
        skill_map = {}
        for skill in SkillTarget:
            insights = self.get_insights_by_skill(skill)
            skill_map[skill.value] = [
                {
                    "book": i.book_name,
                    "author": i.author,
                    "technique": i.core_technique,
                    "insight": i.detailed_insight,
                    "tips": i.actionable_tips,
                    "difficulty": i.difficulty,
                }
                for i in insights
            ]
        return skill_map

    def get_statistics(self) -> Dict:
        skill_counts = {}
        for skill in SkillTarget:
            skill_counts[skill.value] = len(self.get_insights_by_skill(skill))
        category_counts = {}
        for i in self.insights:
            category_counts[i.category] = category_counts.get(i.category, 0) + 1
        return {
            "total_books": len(set(i.book_name for i in self.insights)),
            "total_insights": len(self.insights),
            "by_skill": skill_counts,
            "by_category": category_counts,
            "total_actionable_tips": sum(len(i.actionable_tips) for i in self.insights),
        }


if __name__ == "__main__":
    kb = BookKnowledgeBase()
    stats = kb.get_statistics()
    print("=" * 60)
    print("  NWACS 书籍知识库统计")
    print("=" * 60)
    print(f"  收录书籍: {stats['total_books']} 本")
    print(f"  提炼技法: {stats['total_insights']} 条")
    print(f"  可执行技巧: {stats['total_actionable_tips']} 条")
    print(f"\n  按技能分布:")
    for skill, count in stats['by_skill'].items():
        bar = "#" * (count // 2)
        print(f"    {skill}: {count} {bar}")
    print(f"\n  按书籍类别:")
    for cat, count in stats['by_category'].items():
        print(f"    {cat}: {count} 条")