#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 题材特化生成配置 - GenreProfileManager

对标 WebNovelAI Genre-Specific AI Training / Sudowrite Genre Conventions

核心能力：
1. 题材特化提示词 - 每种题材有专属的系统提示词和写作规则
2. 节奏模板 - 不同题材的章节节奏控制参数
3. 爽点配置 - 网文各题材的核心爽点模式
4. 禁忌规则 - 各题材应避免的写作陷阱
5. 动态切换 - 根据当前写作题材自动加载对应配置

内置题材：
- 玄幻 / 都市 / 言情 / 悬疑 / 科幻 / 历史 / 游戏 / 末世 / 无限流 / 仙侠
"""

import json
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum


class GenreType(Enum):
    XUANHUAN = ("玄幻", "xuanhuan")
    XIANXIA = ("仙侠", "xianxia")
    URBAN = ("都市", "urban")
    ROMANCE = ("言情", "romance")
    SUSPENSE = ("悬疑", "suspense")
    SCIFI = ("科幻", "scifi")
    HISTORICAL = ("历史", "historical")
    GAMING = ("游戏", "gaming")
    POSTAPOCALYPTIC = ("末世", "postapocalyptic")
    INFINITE_FLOW = ("无限流", "infinite_flow")

    def __init__(self, label: str, key: str):
        self.label = label
        self.key = key


@dataclass
class GenreProfile:
    genre: GenreType
    system_prompt: str
    writing_rules: List[str]
    pace_template: Dict[str, Any]
    pleasure_points: List[Dict[str, str]]
    taboos: List[str]
    chapter_structure: Dict[str, Any]
    character_archetypes: List[Dict[str, str]]
    world_building_essentials: List[str]
    dialogue_style: str
    description_style: str
    recommended_models: List[str]


class GenreProfileManager:
    """题材特化生成配置管理器"""

    PROFILES = {
        GenreType.XUANHUAN: GenreProfile(
            genre=GenreType.XUANHUAN,
            system_prompt="""你是一位精通玄幻小说的资深网文作家。玄幻小说的核心是"修炼升级"与"世界观展开"。

写作时必须遵循以下原则：
1. 修炼体系清晰：每个境界的名称、特征、突破方式必须明确
2. 战斗描写热血：战斗场景要有画面感，招式名称要有意境
3. 机缘合理分配：主角的成长要有节奏，不能一步登天
4. 世界观层层展开：不要一次性倒出所有设定，随剧情逐步揭示
5. 情感线自然融入：感情发展要符合人物性格和剧情逻辑""",

            writing_rules=[
                "每章必须有修炼或战斗相关的内容推进",
                "境界突破要有仪式感，描写要详细",
                "战斗场景至少占章节的30%",
                "功法/武技/法宝的获取要有代价",
                "主角不能无理由变强，每次突破要有铺垫",
                "反派要有合理的动机，不能纯粹为坏而坏",
                "地图要逐步扩大：家族→城市→国家→大陆→位面",
            ],

            pace_template={
                "chapter_rhythm": "快慢交替",
                "action_ratio": 0.35,
                "dialogue_ratio": 0.25,
                "description_ratio": 0.20,
                "inner_monologue_ratio": 0.10,
                "exposition_ratio": 0.10,
                "avg_paragraph_length": "中短",
                "cliffhanger_frequency": "每3-5章一次大悬念",
            },

            pleasure_points=[
                {"name": "境界突破", "description": "主角突破到新境界，实力大幅提升",
                 "frequency": "每20-30章一次"},
                {"name": "打脸逆袭", "description": "主角在公开场合碾压曾经看不起他的人",
                 "frequency": "每10-15章一次"},
                {"name": "获得至宝", "description": "主角获得稀有法宝/功法/丹药",
                 "frequency": "每15-20章一次"},
                {"name": "越级战斗", "description": "主角以弱胜强，击败高境界对手",
                 "frequency": "每20-30章一次"},
                {"name": "势力扩张", "description": "主角建立或扩大自己的势力",
                 "frequency": "每50-80章一次"},
            ],

            taboos=[
                "主角性格前后矛盾",
                "修炼体系混乱（境界名称/等级不一致）",
                "战力崩坏（前期高手后期变杂兵）",
                "女性角色沦为花瓶",
                '过度使用\u201c恐怖如斯\u201d、\u201c倒吸一口凉气\u201d等烂俗表达',
                "主角获得能力后不展示就直接跳到下一个",
            ],

            chapter_structure={
                "opening": "承接上章悬念或直接进入场景",
                "middle": "核心事件展开 + 战斗/冲突 + 能力展示",
                "ending": "悬念钩子或境界突破预告",
                "ideal_length": "2500-4000字",
            },

            character_archetypes=[
                {"role": "主角", "types": ["废柴逆袭", "重生复仇", "天才少年", "穿越异界"]},
                {"role": "女主", "types": ["冷艳师姐", "活泼师妹", "魔族公主", "神秘女帝"]},
                {"role": "导师", "types": ["戒指老爷爷", "隐世高人", "宗门长老"]},
                {"role": "兄弟", "types": ["热血胖子", "冷酷剑客", "忠厚大汉"]},
                {"role": "反派", "types": ["傲慢少主", "野心宗主", "幕后黑手"]},
            ],

            world_building_essentials=[
                "修炼境界体系（至少5个大境界，每个有3-4个小境界）",
                "势力分布（宗门/家族/皇朝/散修）",
                "地理架构（大陆/海域/秘境/禁地）",
                "功法体系（属性/等级/稀有度）",
                "资源体系（灵石/丹药/法宝等级）",
            ],

            dialogue_style="古风与现代结合，主角对话偏现代口语，高人对话偏文言古风",

            description_style="战斗场景用短句加速，环境描写用工笔细描，境界突破用宏大排比",

            recommended_models=["deepseek-chat", "deepseek-reasoner"],
        ),

        GenreType.URBAN: GenreProfile(
            genre=GenreType.URBAN,
            system_prompt="""你是一位精通都市小说的资深网文作家。都市小说的核心是"身份反差"与"现实爽感"。

写作时必须遵循以下原则：
1. 身份设定要有冲击力：兵王/神医/神豪/高手回归都市的反差感
2. 打脸要有层次：从小人物到大家族，从本地到国际
3. 商战要专业：涉及商业的情节要有基本逻辑
4. 感情线要真实：都市情感要接地气，不能太悬浮
5. 现实元素要准确：涉及现实职业/行业的内容要做功课""",

            writing_rules=[
                "每章至少有一个'打脸'或'震惊'场景",
                "主角的能力展示要循序渐进",
                "商业/职场描写要有真实感",
                "女性角色要有独立人格",
                "反派要有合理的利益动机",
                "都市背景细节要真实（地名/品牌/文化）",
            ],

            pace_template={
                "chapter_rhythm": "紧凑推进",
                "action_ratio": 0.20,
                "dialogue_ratio": 0.35,
                "description_ratio": 0.15,
                "inner_monologue_ratio": 0.15,
                "exposition_ratio": 0.15,
                "avg_paragraph_length": "中短",
                "cliffhanger_frequency": "每2-3章一次",
            },

            pleasure_points=[
                {"name": "身份揭露", "description": "主角的真实身份被揭露，震惊众人",
                 "frequency": "每15-20章一次"},
                {"name": "实力碾压", "description": "主角用专业能力碾压对手",
                 "frequency": "每5-10章一次"},
                {"name": "英雄救美", "description": "主角在关键时刻救下女主",
                 "frequency": "每20-30章一次"},
                {"name": "商业逆袭", "description": "主角在商战中击败对手",
                 "frequency": "每30-50章一次"},
            ],

            taboos=[
                "女性角色过度物化",
                "主角无底线装逼",
                "商战描写过于儿戏",
                "所有女性都爱上主角",
                '过度使用\u201c恐怖如斯\u201d等玄幻用语',
            ],

            chapter_structure={
                "opening": "日常场景切入或承接上章冲突",
                "middle": "冲突升级 + 能力展示 + 打脸/反转",
                "ending": "悬念或下一冲突的预告",
                "ideal_length": "2000-3500字",
            },

            character_archetypes=[
                {"role": "主角", "types": ["兵王回归", "神医圣手", "神豪归来", "高手下山"]},
                {"role": "女主", "types": ["冷艳总裁", "温柔医生", "活泼记者", "傲娇千金"]},
                {"role": "兄弟", "types": ["铁血战友", "商界盟友", "技术天才"]},
                {"role": "反派", "types": ["商业对手", "豪门纨绔", "国际势力"]},
            ],

            world_building_essentials=[
                "主角隐藏身份的背景故事",
                "都市势力格局（家族/商会/地下势力）",
                "主角能力来源的合理解释",
                "关键地点的设定（公司/会所/别墅）",
            ],

            dialogue_style="现代口语化，符合角色社会阶层，商界人士用词专业，日常对话接地气",

            description_style="简洁明快，重点描写关键场景和人物状态，避免冗长环境描写",

            recommended_models=["deepseek-chat"],
        ),

        GenreType.ROMANCE: GenreProfile(
            genre=GenreType.ROMANCE,
            system_prompt="""你是一位精通言情小说的资深网文作家。言情小说的核心是"情感张力"与"关系发展"。

写作时必须遵循以下原则：
1. 感情发展要有层次：从初识到心动到误会到和解到深爱
2. 人物要有苏感：男女主都要有让人心动的特质
3. 冲突要合理：不能为虐而虐，矛盾要有说服力
4. 甜虐要有节奏：不能一直甜也不能一直虐
5. 细节要动人：通过小事和细节展现感情""",

            writing_rules=[
                "每章至少有一个情感互动场景",
                "男女主的互动要有化学反应",
                "内心独白要细腻真实",
                "配角要有自己的故事线",
                "场景描写要营造氛围感",
                "对话要体现人物关系的微妙变化",
            ],

            pace_template={
                "chapter_rhythm": "情感驱动",
                "action_ratio": 0.05,
                "dialogue_ratio": 0.40,
                "description_ratio": 0.20,
                "inner_monologue_ratio": 0.25,
                "exposition_ratio": 0.10,
                "avg_paragraph_length": "中长",
                "cliffhanger_frequency": "每章结尾留情感钩子",
            },

            pleasure_points=[
                {"name": "心动瞬间", "description": "男女主之间产生心动的关键时刻",
                 "frequency": "每5-10章一次"},
                {"name": "甜蜜互动", "description": "男女主的甜蜜日常或浪漫场景",
                 "frequency": "每3-5章一次"},
                {"name": "误会解除", "description": "重大误会被澄清，感情升温",
                 "frequency": "每20-30章一次"},
                {"name": "告白/确认关系", "description": "感情关系的里程碑事件",
                 "frequency": "每30-50章一次"},
            ],

            taboos=[
                "感情发展过于突兀",
                "女性角色恋爱脑无自我",
                "男性角色过于完美不真实",
                "为虐而虐的强行误会",
                "第三者插足的狗血套路过度使用",
            ],

            chapter_structure={
                "opening": "情感状态展示或承接上章情感节点",
                "middle": "情感互动 + 关系推进 + 小冲突/甜蜜",
                "ending": "情感悬念或关系变化的预告",
                "ideal_length": "2000-3500字",
            },

            character_archetypes=[
                {"role": "女主", "types": ["独立女性", "软萌甜心", "冷艳女王", "元气少女"]},
                {"role": "男主", "types": ["霸道总裁", "温润如玉", "邪魅狂狷", "禁欲系"]},
                {"role": "闺蜜", "types": ["毒舌闺蜜", "暖心姐妹", "事业搭档"]},
                {"role": "情敌", "types": ["白月光", "青梅竹马", "商业联姻对象"]},
            ],

            world_building_essentials=[
                "男女主的背景设定（家庭/职业/过往情史）",
                "关键场景（初遇地点/定情地点/冲突地点）",
                "关系发展的关键节点时间线",
            ],

            dialogue_style="自然口语化，体现人物性格和情感状态，暧昧期对话要有潜台词",

            description_style="细腻感性，注重氛围营造，通过环境映射人物内心",

            recommended_models=["deepseek-chat"],
        ),

        GenreType.SUSPENSE: GenreProfile(
            genre=GenreType.SUSPENSE,
            system_prompt="""你是一位精通悬疑小说的资深作家。悬疑小说的核心是"信息控制"与"逻辑严密"。

写作时必须遵循以下原则：
1. 线索要合理分布：不能一次性给出所有线索，也不能完全不給
2. 红鲱鱼要巧妙：误导线索要合理但不能欺骗读者
3. 反转要有铺垫：所有反转在前面都要有伏笔
4. 逻辑要严密：每个推理环节都要经得起推敲
5. 氛围要到位：通过环境描写营造紧张感和不安感""",

            writing_rules=[
                "每章至少埋设一个线索或推进一个疑点",
                "推理过程要展示思考逻辑",
                "红鲱鱼（误导线索）要合理",
                "真相揭示要有层次感",
                "人物行为要有合理动机",
                "时间线要精确无误",
            ],

            pace_template={
                "chapter_rhythm": "逐步收紧",
                "action_ratio": 0.15,
                "dialogue_ratio": 0.30,
                "description_ratio": 0.20,
                "inner_monologue_ratio": 0.20,
                "exposition_ratio": 0.15,
                "avg_paragraph_length": "中",
                "cliffhanger_frequency": "每章结尾留悬念",
            },

            pleasure_points=[
                {"name": "线索发现", "description": "主角发现关键线索",
                 "frequency": "每3-5章一次"},
                {"name": "推理突破", "description": "主角通过推理取得突破",
                 "frequency": "每10-15章一次"},
                {"name": "反转揭露", "description": "重大反转或真相揭露",
                 "frequency": "每20-30章一次"},
                {"name": "真凶现身", "description": "真正的凶手/幕后黑手浮出水面",
                 "frequency": "每30-50章一次"},
            ],

            taboos=[
                "线索矛盾（前后给出的线索不一致）",
                "机械降神（突然出现的新设定解决问题）",
                "凶手是之前从未出现过的角色",
                "推理过程跳跃太大",
                "过度依赖巧合推动剧情",
            ],

            chapter_structure={
                "opening": "承接上章悬念或发现新线索",
                "middle": "线索追踪 + 推理分析 + 危险逼近",
                "ending": "新悬念或危险升级",
                "ideal_length": "2500-4000字",
            },

            character_archetypes=[
                {"role": "侦探", "types": ["天才侦探", "硬汉刑警", "法医专家", "心理侧写师"]},
                {"role": "助手", "types": ["忠实搭档", "技术专家", "记者盟友"]},
                {"role": "嫌疑人", "types": ["表面无辜", "动机明确", "行为可疑"]},
                {"role": "真凶", "types": ["高智商犯罪", "连环杀手", "复仇者"]},
            ],

            world_building_essentials=[
                "案件时间线（精确到小时）",
                "人物不在场证明矩阵",
                "关键物证清单",
                "所有角色的隐藏动机",
            ],

            dialogue_style="审讯对话要犀利有压迫感，日常对话中暗藏线索，嫌疑人对话要有破绽",

            description_style="冷峻克制，通过细节和环境营造不安感，关键场景用慢镜头放大",

            recommended_models=["deepseek-chat", "deepseek-reasoner"],
        ),

        GenreType.SCIFI: GenreProfile(
            genre=GenreType.SCIFI,
            system_prompt="""你是一位精通科幻小说的资深作家。科幻小说的核心是"科学设定"与"人文思考"。

写作时必须遵循以下原则：
1. 科学设定要自洽：技术/理论不需要完全真实，但要在设定内逻辑自洽
2. 硬科幻要准确：涉及真实科学概念时要查证
3. 软科幻重人文：技术只是背景，核心是人性和社会
4. 未来感要具体：通过细节展现未来世界的不同
5. 科技伦理要探讨：好的科幻必然涉及科技带来的伦理问题""",

            writing_rules=[
                "科技设定要在首次出现时给出清晰描述",
                "技术细节要准确（如涉及真实科学）",
                "未来社会的运行逻辑要合理",
                "AI/外星生命的行为要有内在逻辑",
                "科技带来的社会变革要具体展现",
            ],

            pace_template={
                "chapter_rhythm": "探索驱动",
                "action_ratio": 0.20,
                "dialogue_ratio": 0.25,
                "description_ratio": 0.25,
                "inner_monologue_ratio": 0.15,
                "exposition_ratio": 0.15,
                "avg_paragraph_length": "中",
                "cliffhanger_frequency": "每3-5章一次",
            },

            pleasure_points=[
                {"name": "科技展示", "description": "展示令人惊叹的未来科技",
                 "frequency": "每5-10章一次"},
                {"name": "理论突破", "description": "主角在科学/技术上取得突破",
                 "frequency": "每15-20章一次"},
                {"name": "首次接触", "description": "与外星文明/AI的首次深度接触",
                 "frequency": "每20-30章一次"},
                {"name": "伦理抉择", "description": "面对科技带来的重大伦理抉择",
                 "frequency": "每30-50章一次"},
            ],

            taboos=[
                "科技设定前后矛盾",
                "伪科学冒充真科学（除非明确是软科幻）",
                "技术解决方案过于简单",
                "外星文明过于拟人化（除非有合理解释）",
                "忽视科技发展的社会影响",
            ],

            chapter_structure={
                "opening": "科技场景展示或承接上章发现",
                "middle": "科技探索 + 理论推演 + 冲突/发现",
                "ending": "新发现或科技伦理困境",
                "ideal_length": "2500-4000字",
            },

            character_archetypes=[
                {"role": "主角", "types": ["科学家", "工程师", "探险家", "AI研究员"]},
                {"role": "搭档", "types": ["AI助手", "外星盟友", "技术天才"]},
                {"role": "反派", "types": ["科技公司", "外星势力", "失控AI"]},
            ],

            world_building_essentials=[
                "核心技术/理论的详细设定",
                "未来社会结构（政府/企业/组织）",
                "太空/异星环境描述",
                "科技发展时间线",
            ],

            dialogue_style="专业讨论要有技术深度，日常对话展现未来生活细节",

            description_style="科技场景用精确语言描述，异星环境用陌生化手法，未来都市用细节堆砌真实感",

            recommended_models=["deepseek-chat", "deepseek-reasoner"],
        ),

        GenreType.POSTAPOCALYPTIC: GenreProfile(
            genre=GenreType.POSTAPOCALYPTIC,
            system_prompt="""你是一位精通末世小说的资深网文作家。末世小说的核心是"生存压力"与"人性考验"。

写作时必须遵循以下原则：
1. 生存感要真实：资源匮乏的压迫感要时刻存在
2. 人性要复杂：末世中的人性既有黑暗也有光明
3. 能力成长要有代价：每次变强都要付出相应代价
4. 基地建设要合理：从零开始的势力建设要有逻辑
5. 希望感要保留：再黑暗的末世也要有一丝希望""",

            writing_rules=[
                "资源管理要真实（食物/水/弹药/药品）",
                "丧尸/怪物的威胁要持续存在",
                "人性的黑暗与光明都要展现",
                "基地建设要有阶段性进展",
                "团队成员的牺牲要有意义",
            ],

            pace_template={
                "chapter_rhythm": "高压推进",
                "action_ratio": 0.35,
                "dialogue_ratio": 0.20,
                "description_ratio": 0.20,
                "inner_monologue_ratio": 0.15,
                "exposition_ratio": 0.10,
                "avg_paragraph_length": "中短",
                "cliffhanger_frequency": "每2-3章一次危机",
            },

            pleasure_points=[
                {"name": "物资发现", "description": "发现大量生存物资",
                 "frequency": "每10-15章一次"},
                {"name": "能力觉醒", "description": "主角觉醒/升级特殊能力",
                 "frequency": "每20-30章一次"},
                {"name": "基地升级", "description": "基地防御/规模大幅提升",
                 "frequency": "每30-50章一次"},
                {"name": "收复失地", "description": "从丧尸/怪物手中收复重要区域",
                 "frequency": "每50-80章一次"},
            ],

            taboos=[
                "物资无限（破坏生存压迫感）",
                "主角从不面临道德困境",
                "所有幸存者都是好人/坏人",
                "丧尸威胁忽强忽弱",
                "忽视心理压力对人物的影响",
            ],

            chapter_structure={
                "opening": "危机场景或日常生存状态",
                "middle": "战斗/探索 + 资源获取 + 人性冲突",
                "ending": "新危机预告或生存状态变化",
                "ideal_length": "2500-4000字",
            },

            character_archetypes=[
                {"role": "主角", "types": ["重生者", "能力觉醒", "军人", "普通幸存者"]},
                {"role": "核心团队", "types": ["战力担当", "技术专家", "医疗人员", "侦察兵"]},
                {"role": "反派", "types": ["暴君领袖", "掠夺者", "邪教教主", "疯狂科学家"]},
            ],

            world_building_essentials=[
                "末世起因（病毒/核战/天灾/未知）",
                "丧尸/怪物设定（类型/等级/弱点）",
                "幸存者势力分布",
                "安全区/危险区地图",
            ],

            dialogue_style="紧张环境下对话简短有力，安全区对话展现人物关系，团队讨论要有策略性",

            description_style="废墟场景用荒凉美学，战斗用紧凑短句，安全区用对比手法展现珍贵",

            recommended_models=["deepseek-chat"],
        ),
    }

    def __init__(self):
        self.active_profile: Optional[GenreProfile] = None
        self.active_genre: Optional[GenreType] = None

    def set_genre(self, genre: GenreType) -> GenreProfile:
        profile = self.PROFILES.get(genre)
        if profile is None:
            available = [g.label for g in self.PROFILES]
            raise ValueError(f"不支持的题材: {genre.label}。可用题材: {available}")

        self.active_profile = profile
        self.active_genre = genre
        return profile

    def get_active_profile(self) -> Optional[GenreProfile]:
        return self.active_profile

    def get_system_prompt(self) -> str:
        if not self.active_profile:
            return ""
        return self.active_profile.system_prompt

    def get_writing_rules_prompt(self) -> str:
        if not self.active_profile:
            return ""

        rules = self.active_profile.writing_rules
        parts = ["\n【本题材写作规则 - 必须遵守】"]
        for i, rule in enumerate(rules, 1):
            parts.append(f"{i}. {rule}")
        return "\n".join(parts)

    def get_taboos_prompt(self) -> str:
        if not self.active_profile:
            return ""

        taboos = self.active_profile.taboos
        parts = ["\n【本题材禁忌 - 严格避免】"]
        for i, taboo in enumerate(taboos, 1):
            parts.append(f"❌ {taboo}")
        return "\n".join(parts)

    def get_chapter_structure_prompt(self) -> str:
        if not self.active_profile:
            return ""

        cs = self.active_profile.chapter_structure
        parts = ["\n【章节结构要求】"]
        parts.append(f"- 开头: {cs['opening']}")
        parts.append(f"- 中间: {cs['middle']}")
        parts.append(f"- 结尾: {cs['ending']}")
        parts.append(f"- 目标字数: {cs['ideal_length']}")
        return "\n".join(parts)

    def get_pleasure_points_guide(self) -> str:
        if not self.active_profile:
            return ""

        points = self.active_profile.pleasure_points
        parts = ["\n【本题材核心爽点 - 在合适位置安排】"]
        for pp in points:
            parts.append(f"- {pp['name']}: {pp['description']} (建议{pp['frequency']})")
        return "\n".join(parts)

    def get_full_generation_context(self, include_pleasure: bool = True) -> str:
        if not self.active_profile:
            return ""

        parts = [
            self.get_system_prompt(),
            self.get_writing_rules_prompt(),
            self.get_taboos_prompt(),
            self.get_chapter_structure_prompt(),
        ]

        if include_pleasure:
            parts.append(self.get_pleasure_points_guide())

        parts.append(f"\n【风格指导】")
        parts.append(f"- 对话风格: {self.active_profile.dialogue_style}")
        parts.append(f"- 描写风格: {self.active_profile.description_style}")

        return "\n".join(parts)

    def list_genres(self) -> List[Dict]:
        result = []
        for genre, profile in self.PROFILES.items():
            result.append({
                "name": genre.label,
                "key": genre.key,
                "pleasure_points": len(profile.pleasure_points),
                "writing_rules": len(profile.writing_rules),
                "taboos": len(profile.taboos),
                "recommended_models": profile.recommended_models,
            })
        return result

    def get_genre_by_name(self, name: str) -> Optional[GenreType]:
        name_lower = name.lower()
        for genre in GenreType:
            if genre.label == name or genre.key == name_lower:
                return genre
        return None


if __name__ == "__main__":
    print("=" * 60)
    print("题材特化生成配置 - 功能验证")
    print("=" * 60)

    manager = GenreProfileManager()

    print("\n[1] 可用题材列表...")
    for g in manager.list_genres():
        print(f"  {g['name']}({g['key']}): {g['writing_rules']}条规则, "
              f"{g['pleasure_points']}个爽点, 推荐模型={g['recommended_models']}")

    print("\n[2] 玄幻题材配置...")
    manager.set_genre(GenreType.XUANHUAN)
    profile = manager.get_active_profile()
    print(f"  题材: {profile.genre.label}")
    print(f"  规则数: {len(profile.writing_rules)}")
    print(f"  爽点数: {len(profile.pleasure_points)}")
    print(f"  禁忌数: {len(profile.taboos)}")

    print("\n[3] 完整生成上下文预览...")
    context = manager.get_full_generation_context()
    print(f"  总长度: {len(context)}字符")
    print(f"  预览:\n{context[:500]}...")

    print("\n[4] 切换到都市题材...")
    manager.set_genre(GenreType.URBAN)
    context2 = manager.get_full_generation_context(include_pleasure=False)
    print(f"  都市题材上下文: {len(context2)}字符")

    print("\n✅ 题材特化生成配置验证完成")
