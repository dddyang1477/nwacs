#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 硬核角色命名引擎 - CharacterNameEngine
核心功能：
1. 大模型驱动命名 - 基于DeepSeek深度理解角色背景生成名字
2. 命运绑定 - 名字与角色性格、命运、故事背景深度绑定
3. 多风格支持 - 古风/现代/玄幻/武侠/科幻/悬疑/恐怖
4. 深度寓意 - 不只是字面意思，而是角色命运的隐喻和伏笔
5. 称号系统 - 道号/绰号/尊称/江湖名号
6. 组织命名 - 宗门/家族/组织/地名
7. 融入创作流程 - 与剧情/大纲生成同步

设计原则：
- 名字要有"刀锋感"——不软不套路，每个名字都有故事
- 名字是角色的第一印象，必须一击即中
- 寓意要深到能当伏笔用
"""

import json
import re
import random
from typing import Dict, List, Optional, Any, Tuple
from llm_interface import GenerationParams
from dataclasses import dataclass, field
from enum import Enum


class NameStyle(Enum):
    """命名风格"""
    CLASSICAL = "classical"           # 古典雅致
    SHARP = "sharp"                   # 锋芒毕露
    MYSTERIOUS = "mysterious"         # 神秘莫测
    DOMINEERING = "domineering"       # 霸气侧漏
    ELEGANT = "elegant"               # 温润如玉
    DARK = "dark"                     # 暗黑深沉
    RUSTIC = "rustic"                 # 朴实无华
    FUTURISTIC = "futuristic"         # 未来科幻
    STREET = "street"                 # 街头江湖
    SCHOLARLY = "scholarly"           # 书卷气


class CharacterRole(Enum):
    """角色定位"""
    PROTAGONIST = "protagonist"
    ANTAGONIST = "antagonist"
    MENTOR = "mentor"
    LOVE_INTEREST = "love_interest"
    RIVAL = "rival"
    SIDEKICK = "sidekick"
    VILLAIN = "villain"
    ANTI_HERO = "anti_hero"
    TRAGIC_HERO = "tragic_hero"
    HIDDEN_MASTER = "hidden_master"
    COMIC_RELIEF = "comic_relief"
    WISE_ELDER = "wise_elder"


@dataclass
class CharacterProfile:
    """角色画像"""
    role: str = "protagonist"
    gender: str = "male"
    age: str = "young"
    personality: str = ""
    background: str = ""
    fate: str = ""
    ability: str = ""
    weakness: str = ""
    arc: str = ""


@dataclass
class NameResult:
    """命名结果"""
    full_name: str
    surname: str
    given_name: str
    style: str
    meaning: str              # 深层寓意（可作伏笔）
    literal_meaning: str       # 字面意思
    fate_connection: str       # 与命运的关联
    personality_match: str     # 与性格的匹配
    aliases: List[str] = field(default_factory=list)
    titles: List[str] = field(default_factory=list)
    score: int = 0
    alternatives: List[str] = field(default_factory=list)


class CharacterNameEngine:
    """硬核角色命名引擎"""

    def __init__(self, llm_interface=None):
        self._llm = llm_interface
        self._cache: Dict[str, List[NameResult]] = {}
        self._used_names: set = set()

    @property
    def llm(self):
        if self._llm is None:
            from llm_interface import llm as _llm
            self._llm = _llm
        return self._llm

    def generate_character_names(
        self,
        genre: str,
        profile: CharacterProfile,
        count: int = 5,
        style: str = None,
        story_context: str = "",
    ) -> List[NameResult]:
        """
        为核心角色生成名字

        参数:
            genre: 题材类型（玄幻/都市/仙侠/科幻/悬疑/言情/历史/游戏/恐怖/武侠）
            profile: 角色画像
            count: 生成数量
            style: 命名风格偏好
            story_context: 故事背景上下文
        """
        cache_key = f"{genre}_{profile.role}_{profile.gender}_{profile.personality[:20]}"
        if cache_key in self._cache:
            cached = self._cache[cache_key]
            available = [n for n in cached if n.full_name not in self._used_names]
            if len(available) >= count:
                return available[:count]

        style_guide = self._get_style_guide(genre, style)

        prompt = f"""你是一位顶级网络文学命名大师，曾为100+部爆款小说设计角色名字。
你的名字不是随便拼凑的——每个名字都是角色命运的隐喻，是故事伏笔的起点。

## 命名任务
- 题材：{genre}
- 角色定位：{profile.role}（{self._role_desc(profile.role)}）
- 性别：{profile.gender}
- 年龄段：{profile.age}
- 性格特征：{profile.personality or '待定'}
- 背景故事：{profile.background or '待定'}
- 命运走向：{profile.fate or '待定'}
- 能力特长：{profile.ability or '待定'}
- 性格缺陷：{profile.weakness or '待定'}
- 角色弧光：{profile.arc or '待定'}
- 故事背景：{story_context or '待定'}

## 命名铁律（必须遵守）
1. **拒绝套路**：禁止使用"天/云/辰/宇/昊/轩/逸/尘/雪/月/瑶/璃"等烂大街的字
2. **要有刀锋感**：名字读出来要有力量，要么锋利要么厚重，不能软绵绵
3. **命运隐喻**：名字必须暗示角色的命运走向，可以当伏笔用
4. **辨识度第一**：读者看一眼就能记住，不能和市面上任何角色撞名
5. **符合题材**：{genre}题材的名字要有该题材的气质
6. **性格外化**：名字要能体现角色的核心性格

{style_guide}

## 输出格式
返回JSON数组，每个名字包含：
- full_name: 完整姓名
- surname: 姓氏
- given_name: 名字
- style: 风格标签
- meaning: 深层寓意（50-100字，解释这个名字如何暗示角色命运，如何作为故事伏笔）
- literal_meaning: 字面意思（20字以内）
- fate_connection: 与命运的关联（30-50字）
- personality_match: 与性格的匹配（30-50字）
- aliases: 可能的别名/绰号（2-3个）
- titles: 可能的称号/尊称（1-2个）
- score: 综合评分（1-100）

只返回JSON数组，不要任何解释。"""

        try:
            result = self.llm.generate_json(
                prompt,
                system_prompt="你是顶级网络文学命名大师。只返回JSON数组。",
                params=GenerationParams(temperature=0.95, max_tokens=3000),
                fallback=[]
            )

            names = []
            if isinstance(result, list):
                items = result
            elif isinstance(result, dict):
                items = result.get('names', result.get('characters', []))
            else:
                items = []

            for item in items[:count]:
                name = NameResult(
                    full_name=item.get('full_name', ''),
                    surname=item.get('surname', ''),
                    given_name=item.get('given_name', ''),
                    style=item.get('style', style or ''),
                    meaning=item.get('meaning', ''),
                    literal_meaning=item.get('literal_meaning', ''),
                    fate_connection=item.get('fate_connection', ''),
                    personality_match=item.get('personality_match', ''),
                    aliases=item.get('aliases', []),
                    titles=item.get('titles', []),
                    score=item.get('score', 0),
                )
                if name.full_name and name.full_name not in self._used_names:
                    names.append(name)

            if names:
                self._cache[cache_key] = names
                return names

        except Exception as e:
            pass

        return self._fallback_names(genre, profile, count)

    def generate_cast(
        self,
        genre: str,
        story_context: str = "",
        protagonist_profile: CharacterProfile = None,
        count: int = 4,
    ) -> Dict[str, List[NameResult]]:
        """
        为整个故事生成角色阵容

        返回: {"protagonist": [...], "antagonist": [...], "supporting": [...]}
        """
        result = {}

        if protagonist_profile:
            result['protagonist'] = self.generate_character_names(
                genre, protagonist_profile, count=3, story_context=story_context
            )

        antagonist = CharacterProfile(
            role="antagonist", gender="male",
            personality="与主角对立但有自己的信念",
            background="与主角的命运交织",
            fate="与主角的最终对决",
        )
        result['antagonist'] = self.generate_character_names(
            genre, antagonist, count=3, story_context=story_context
        )

        supporting_roles = [
            CharacterProfile(role="love_interest", gender="female",
                           personality="坚韧独立，是主角的精神支柱"),
            CharacterProfile(role="mentor", gender="male",
                           personality="深不可测，引导主角成长"),
            CharacterProfile(role="rival", gender="male",
                           personality="亦敌亦友，与主角互相成就"),
            CharacterProfile(role="sidekick", gender="male",
                           personality="忠诚可靠，是主角的左膀右臂"),
        ]

        result['supporting'] = []
        for profile in supporting_roles[:max(1, count - 2)]:
            names = self.generate_character_names(
                genre, profile, count=2, story_context=story_context
            )
            result['supporting'].extend(names)

        return result

    def generate_title(self, genre: str, character_name: str,
                       personality: str = "", ability: str = "",
                       style: str = "domineering") -> List[str]:
        """为角色生成称号/道号/绰号"""
        prompt = f"""你是顶级网络文学命名大师。为以下角色生成称号：

角色名：{character_name}
题材：{genre}
性格：{personality or '待定'}
能力：{ability or '待定'}
风格：{style}

要求：
1. 称号要有江湖味/玄幻味，不能软
2. 要体现角色的核心特质
3. 读起来要有气势
4. 生成3-5个不同风格的称号

返回JSON：{{"titles": ["称号1", "称号2", ...]}}"""

        try:
            result = self.llm.generate_json(
                prompt,
                system_prompt="你是顶级命名大师。只返回JSON。",
                fallback={"titles": []}
            )
            return result.get('titles', [])
        except Exception:
            return []

    def generate_organization_name(self, genre: str, org_type: str,
                                    description: str = "",
                                    count: int = 5) -> List[Dict]:
        """
        生成组织/宗门/家族名称

        参数:
            genre: 题材
            org_type: 组织类型（sect/clan/guild/company/agency/cult/gang）
            description: 组织描述
            count: 生成数量
        """
        org_type_desc = {
            'sect': '修仙宗门',
            'clan': '家族/世家',
            'guild': '公会/行会',
            'company': '公司/企业',
            'agency': '机构/组织',
            'cult': '教派/邪教',
            'gang': '帮派/社团',
        }

        prompt = f"""你是顶级网络文学命名大师。为以下组织命名：

题材：{genre}
组织类型：{org_type_desc.get(org_type, org_type)}
组织描述：{description or '待定'}

要求：
1. 名字要有辨识度和气势
2. 要符合{genre}题材的气质
3. 暗示组织的性质和地位
4. 生成{count}个名字

返回JSON数组：[{{"name": "...", "meaning": "...", "style": "..."}}]"""

        try:
            result = self.llm.generate_json(
                prompt,
                system_prompt="你是顶级命名大师。只返回JSON数组。",
                fallback=[]
            )
            if isinstance(result, list):
                return result[:count]
            return []
        except Exception:
            return []

    def generate_location_name(self, genre: str, location_type: str,
                                description: str = "",
                                count: int = 5) -> List[Dict]:
        """生成地名"""
        prompt = f"""你是顶级网络文学命名大师。为以下地点命名：

题材：{genre}
地点类型：{location_type}
地点描述：{description or '待定'}

要求：
1. 名字要有画面感和氛围
2. 要符合{genre}题材的世界观
3. 暗示地点的功能和氛围
4. 生成{count}个名字

返回JSON数组：[{{"name": "...", "meaning": "...", "atmosphere": "..."}}]"""

        try:
            result = self.llm.generate_json(
                prompt,
                system_prompt="你是顶级命名大师。只返回JSON数组。",
                fallback=[]
            )
            if isinstance(result, list):
                return result[:count]
            return []
        except Exception:
            return []

    def generate_power_system_names(self, genre: str, system_type: str,
                                     description: str = "",
                                     count: int = 8) -> List[Dict]:
        """
        生成力量体系命名（境界/等级/技能名）

        参数:
            genre: 题材
            system_type: 体系类型（cultivation/skill/rank/tech）
            description: 体系描述
            count: 生成数量
        """
        prompt = f"""你是顶级网络文学世界观设计师。为以下力量体系命名：

题材：{genre}
体系类型：{system_type}
体系描述：{description or '待定'}

要求：
1. 名字要有层次感和递进关系
2. 要符合{genre}题材的力量体系逻辑
3. 每个名字都要有气势和辨识度
4. 生成{count}个等级/境界名称，从低到高排列

返回JSON：{{"system_name": "...", "levels": [{{"name": "...", "description": "...", "rank": 1}}]}}"""

        try:
            result = self.llm.generate_json(
                prompt,
                system_prompt="你是顶级世界观设计师。只返回JSON。",
                fallback={}
            )
            return result.get('levels', [])
        except Exception:
            return []

    def _get_style_guide(self, genre: str, style: str = None) -> str:
        """获取命名风格指南"""
        guides = {
            '玄幻': """
## 玄幻命名风格指南
- 姓氏要有古韵：复姓优先（慕容、上官、独孤、南宫、东方、西门、北冥、皇甫、欧阳、轩辕、令狐、端木、公孙、尉迟、司马、诸葛）
- 名字要有"道韵"：用字要有修炼感，但不能套路化
- 避免：天、云、辰、宇、昊、轩、逸、尘、渊、玄、霄、凌、风、霆
- 推荐方向：用兵器/自然/星象/古文典故中的冷门字
- 示例好名字：殷无邪、谢云流、燕归人、柳残阳、铁中棠""",

            '仙侠': """
## 仙侠命名风格指南
- 要有"仙气"但不飘渺，要有"侠骨"但不粗犷
- 道号要体现修炼道路：太虚/紫霄/青云/碧落/黄泉/九天/万古/混元/无极
- 名字要有"出世感"，但也要有"入世情"
- 避免：常见的修仙网文用字
- 示例好名字：李忘生、叶孤城、西门吹雪、花满楼""",

            '都市': """
## 都市命名风格指南
- 要有现代感但不俗气
- 名字要暗示社会地位和性格
- 商战类：名字要有精英感
- 兵王类：名字要有硬汉感
- 避免：伟/强/磊/军/勇/杰/涛/明/辉/鹏 等过于常见的字
- 示例好名字：陆沉舟、顾临渊、沈惊蛰、傅云深""",

            '科幻': """
## 科幻命名风格指南
- 未来感：可以用代号/编号/音译名
- 赛博朋克：名字要有科技感和疏离感
- 星际战争：名字要有史诗感
- 末世流：名字要有生存感和粗粝感
- 示例好名字：零、K、艾萨克·陈、诺娃、灰烬""",

            '悬疑': """
## 悬疑命名风格指南
- 名字要有"谜题感"，暗示角色不简单
- 侦探类：名字要有理性感和洞察力
- 犯罪类：名字要有危险感和神秘感
- 心理悬疑：名字要有双重性，暗示表里不一
- 示例好名字：秦明、方木、罗飞、严良""",

            '言情': """
## 言情命名风格指南
- 男主名要有苏感但不油腻
- 女主名要有辨识度，不能是烂大街的"若曦""紫萱""沐晴"
- 霸总类：名字要有压迫感和掌控感
- 甜宠类：名字要有温暖感
- 虐恋类：名字要有破碎感
- 示例好名字：傅慎行、沈知节、陆延舟、顾清欢""",

            '历史': """
## 历史命名风格指南
- 要有时代感，符合历史背景
- 权谋类：名字要有城府感
- 争霸类：名字要有王者之气
- 种田类：名字要有朴实感
- 科举类：名字要有书卷气
- 示例好名字：萧定权、顾逢恩、许七安、魏渊""",

            '游戏': """
## 游戏命名风格指南
- 游戏ID要有辨识度和记忆点
- 电竞类：名字要有竞技感和攻击性
- 全息游戏：名字要有沉浸感和角色感
- 系统流：名字要有反差感（平凡真名+霸气游戏名）
- 示例好名字：君莫笑、叶修、一叶之秋、大漠孤烟""",

            '恐怖': """
## 恐怖命名风格指南
- 名字要有"寒意"，读起来让人脊背发凉
- 灵异类：名字要有阴阳两界的模糊感
- 规则怪谈：名字要有秩序感和诡异感的冲突
- 克苏鲁：名字要有不可名状感
- 民俗恐怖：名字要有乡土感和禁忌感
- 示例好名字：沈言、白夜、顾眠、林异""",

            '武侠': """
## 武侠命名风格指南
- 要有"侠气"和"江湖味"
- 传统武侠：名字要有风骨
- 高武流：名字要有力量感
- 国术流：名字要有传承感
- 剑客流：名字要有锋芒感
- 避免：无忌/孤城/寻欢/留香 等已被经典作品占用的名字
- 示例好名字：燕十三、谢晓峰、李寻欢、傅红雪""",
        }

        base = guides.get(genre, guides['玄幻'])

        if style:
            style_additions = {
                'sharp': '\n额外要求：名字要有刀锋般的锐利感，读起来像出鞘的剑。',
                'mysterious': '\n额外要求：名字要有神秘感，让人捉摸不透，暗示角色有隐藏身份。',
                'domineering': '\n额外要求：名字要有霸气，读起来让人心生敬畏。',
                'elegant': '\n额外要求：名字要温润如玉，有君子之风。',
                'dark': '\n额外要求：名字要有暗黑气质，暗示角色内心的阴影。',
                'rustic': '\n额外要求：名字要朴实无华，大巧不工。',
            }
            base += style_additions.get(style, '')

        return base

    def _role_desc(self, role: str) -> str:
        descriptions = {
            'protagonist': '主角，故事的核心',
            'antagonist': '反派/对手，与主角对立',
            'mentor': '导师/引路人',
            'love_interest': '恋人/情感线核心',
            'rival': '竞争者/宿敌',
            'sidekick': '伙伴/助手',
            'villain': '纯粹的反派',
            'anti_hero': '反英雄，灰色角色',
            'tragic_hero': '悲剧英雄',
            'hidden_master': '隐藏高手',
            'comic_relief': '搞笑担当',
            'wise_elder': '智慧长者',
        }
        return descriptions.get(role, role)

    def _fallback_names(self, genre: str, profile: CharacterProfile, count: int) -> List[NameResult]:
        """后备名字生成（本地规则引擎，但比旧版更硬核）"""
        hardcore_names = {
            '玄幻': {
                'male': [
                    ('殷无邪', '殷', '无邪', 'sharp', '无邪非天真，而是看透世间虚伪后的纯粹', '没有邪念', '以纯粹之心对抗污浊世界', '外冷内热，看似冷漠实则至情至性'),
                    ('谢云流', '谢', '云流', 'elegant', '云流即命运如云般漂泊不定，暗示主角颠沛流离的一生', '云般流动', '注定漂泊，无处为家', '洒脱不羁，随遇而安'),
                    ('燕归人', '燕', '归人', 'mysterious', '归人暗示主角终将回到某个地方，是命运的闭环', '归来的旅人', '离开是为了更好的归来', '执着于某个目标，不达目的不罢休'),
                    ('柳残阳', '柳', '残阳', 'dark', '残阳如血，暗示主角经历过惨烈的过去', '残缺的夕阳', '从废墟中崛起', '坚韧不屈，在绝境中爆发'),
                    ('铁中棠', '铁', '中棠', 'domineering', '铁骨铮铮，海棠花开，刚柔并济', '铁中的海棠', '在铁血中保持柔情', '外表刚硬内心柔软'),
                ],
                'female': [
                    ('秦疏影', '秦', '疏影', 'elegant', '疏影横斜水清浅，暗示主角如暗香般低调但无法忽视', '稀疏的影子', '在暗处影响大局', '低调内敛，实力深藏'),
                    ('沈惊蛰', '沈', '惊蛰', 'sharp', '惊蛰是万物复苏的节气，暗示主角将唤醒沉睡的力量', '惊动蛰伏', '一鸣惊人，改变世界', '平时低调，关键时刻爆发'),
                    ('顾清霜', '顾', '清霜', 'mysterious', '清霜冷冽，暗示主角外表清冷内心炽热', '清澈的霜', '冰封的外表下是炽热的灵魂', '外冷内热，不善表达'),
                ],
            },
            '都市': {
                'male': [
                    ('陆沉舟', '陆', '沉舟', 'domineering', '沉舟侧畔千帆过，暗示主角在逆境中崛起', '沉没的船', '置之死地而后生', '沉稳果断，破釜沉舟'),
                    ('顾临渊', '顾', '临渊', 'sharp', '临渊羡鱼不如退而结网，暗示主角是行动派', '面临深渊', '在危险边缘行走', '胆大心细，敢于冒险'),
                    ('傅云深', '傅', '云深', 'mysterious', '云深不知处，暗示主角深不可测', '云层深处', '隐藏真实身份和实力', '深藏不露，城府极深'),
                ],
                'female': [
                    ('苏幕遮', '苏', '幕遮', 'elegant', '幕遮即帷幕，暗示主角有隐藏的一面', '帷幕遮挡', '揭开真相的关键人物', '表面温柔，内心强大'),
                    ('姜知意', '姜', '知意', 'sharp', '知意即洞察人心，暗示主角善于看透本质', '知晓心意', '洞察一切的智者', '聪明敏锐，看透人心'),
                ],
            },
            '武侠': {
                'male': [
                    ('燕十三', '燕', '十三', 'sharp', '十三是不吉利的数字，暗示主角命途多舛', '数字十三', '与命运抗争', '孤独的剑客，不被理解'),
                    ('傅红雪', '傅', '红雪', 'dark', '红雪即血染白雪，暗示主角背负血海深仇', '红色的雪', '复仇是唯一的信念', '冷酷决绝，为复仇而生'),
                    ('萧别离', '萧', '别离', 'mysterious', '别离是人生常态，暗示主角注定孤独', '告别分离', '不断失去，不断前行', '看透世事，洒脱不羁'),
                ],
                'female': [
                    ('花弄影', '花', '弄影', 'elegant', '云破月来花弄影，暗示主角如花般美丽但易逝', '花影摇曳', '美丽而短暂的绽放', '外表柔弱内心坚韧'),
                    ('水灵光', '水', '灵光', 'mysterious', '灵光一闪即逝，暗示主角是转瞬即逝的奇迹', '水的灵光', '改变一切的关键人物', '神秘莫测，来去无踪'),
                ],
            },
        }

        genre_names = hardcore_names.get(genre, hardcore_names['玄幻'])
        gender_names = genre_names.get(profile.gender, genre_names['male'])

        results = []
        for item in gender_names[:count]:
            name = NameResult(
                full_name=item[0], surname=item[1], given_name=item[2],
                style=item[3], meaning=item[4], literal_meaning=item[5],
                fate_connection=item[6], personality_match=item[7],
                score=random.randint(75, 95),
            )
            if name.full_name not in self._used_names:
                results.append(name)

        return results

    def mark_name_used(self, full_name: str):
        self._used_names.add(full_name)

    def clear_used_names(self):
        self._used_names.clear()

    def clear_cache(self):
        self._cache.clear()


name_engine = CharacterNameEngine()