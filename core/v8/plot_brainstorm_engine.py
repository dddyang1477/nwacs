#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 剧情构思引擎 - PlotBrainstormEngine
核心功能：
1. 剧情灵感生成 - 基于题材/主题/角色生成剧情点子
2. 冲突结构设计 - 主线冲突/支线冲突/人物冲突矩阵
3. 剧情弧光设计 - 起承转合/三幕结构/英雄之旅
4. 反转设计 - 剧情反转/身份反转/认知反转
5. 章节大纲 - 逐章情节规划
6. 伏笔管理 - 埋设/回收伏笔追踪

设计原则：
- 本地模板引擎提供基础构思
- 可选API调用增强创意深度
- 结构化输出，便于后续写作
"""

import json
import random
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum


class PlotArcType(Enum):
    """剧情弧光类型"""
    HERO_JOURNEY = "英雄之旅"
    THREE_ACT = "三幕结构"
    RISE_FALL = "起落结构"
    MYSTERY_UNVEIL = "揭秘结构"
    REVENGE_ARC = "复仇弧光"
    GROWTH_ARC = "成长弧光"


class ConflictType(Enum):
    """冲突类型"""
    PERSON_VS_PERSON = "人与人"
    PERSON_VS_SELF = "人与自我"
    PERSON_VS_SOCIETY = "人与社会"
    PERSON_VS_NATURE = "人与自然"
    PERSON_VS_FATE = "人与命运"
    PERSON_VS_SYSTEM = "人与系统"


@dataclass
class PlotNode:
    """剧情节点"""
    node_id: str
    chapter: int
    title: str
    description: str
    conflict_type: ConflictType
    characters_involved: List[str]
    is_climax: bool = False
    is_twist: bool = False
    foreshadowing: List[str] = field(default_factory=list)
    payoff: List[str] = field(default_factory=list)
    emotional_beat: str = "neutral"


@dataclass
class PlotArc:
    """剧情弧光"""
    arc_id: str
    name: str
    arc_type: PlotArcType
    description: str
    nodes: List[PlotNode] = field(default_factory=list)
    start_chapter: int = 1
    end_chapter: int = 10
    status: str = "planned"


class PlotTemplateLibrary:
    """剧情模板库"""

    # 经典剧情模板
    CLASSIC_PLOTS = {
        "废柴逆袭": {
            "description": "主角从底层崛起，一路打脸升级",
            "stages": [
                "废柴身份展示（被欺凌/被看不起）",
                "获得金手指（系统/传承/奇遇）",
                "低调发育（暗中积累实力）",
                "首次打脸（小范围展现实力）",
                "遭遇强敌（被压制/陷入危机）",
                "突破升级（获得新能力/境界提升）",
                "大范围打脸（公开场合碾压对手）",
                "登上巅峰（成为最强）",
            ],
            "best_for": ["玄幻", "都市", "游戏"],
        },
        "重生复仇": {
            "description": "主角重生回到过去，利用先知优势复仇",
            "stages": [
                "前世悲惨结局（被背叛/被害死）",
                "重生觉醒（回到关键时间点）",
                "确认记忆（验证前世记忆真实性）",
                "提前布局（抢占先机/改变关键事件）",
                "首次复仇（报复第一个仇人）",
                "蝴蝶效应（改变引发新问题）",
                "逐层复仇（从外围到核心）",
                "最终对决（面对最大仇人）",
            ],
            "best_for": ["都市", "言情", "历史"],
        },
        "扮猪吃虎": {
            "description": "主角隐藏实力，在关键时刻爆发",
            "stages": [
                "隐藏身份（伪装成普通人/弱者）",
                "被轻视（周围人看不起主角）",
                "暗中行动（以隐藏身份解决问题）",
                "危机降临（重大威胁出现）",
                "被迫暴露（不得不展现实力）",
                "震惊全场（所有人目瞪口呆）",
                "身份揭露（真实身份曝光）",
                "新的开始（以真实身份面对世界）",
            ],
            "best_for": ["都市", "玄幻", "言情"],
        },
        "末世生存": {
            "description": "在末日环境中求生存、建势力",
            "stages": [
                "末日降临（灾难突然发生）",
                "初始求生（获取基本资源/避难）",
                "遭遇人性（面对其他幸存者的善恶）",
                "建立据点（找到/建造安全基地）",
                "势力扩张（收拢幸存者/扩大地盘）",
                "资源争夺（与其他势力冲突）",
                "发现真相（末日背后的秘密）",
                "重建文明（或发现新出路）",
            ],
            "best_for": ["科幻", "都市", "玄幻"],
        },
        "悬疑探案": {
            "description": "通过线索逐步揭开谜团",
            "stages": [
                "案件发生（诡异事件/谋杀/失踪）",
                "主角介入（主动或被动卷入）",
                "初步调查（收集表面线索）",
                "第一个反转（表面真相被推翻）",
                "深入调查（发现更深层线索）",
                "遭遇危险（调查触怒幕后势力）",
                "第二个反转（真凶另有其人）",
                "真相大白（揭露最终真相）",
            ],
            "best_for": ["悬疑", "都市", "历史"],
        },
        "修仙问道": {
            "description": "主角踏上修仙之路，追求长生大道",
            "stages": [
                "仙缘初现（意外接触修仙世界）",
                "入门修炼（拜入宗门/获得功法）",
                "宗门竞争（同门较量/资源争夺）",
                "外出历练（离开宗门闯荡）",
                "秘境探险（进入秘境获取机缘）",
                "正邪冲突（卷入正邪大战）",
                "飞升之劫（渡劫飞升的关键）",
                "仙界新篇（飞升后面临新挑战）",
            ],
            "best_for": ["玄幻", "仙侠"],
        },
    }

    # 冲突模板
    CONFLICT_TEMPLATES = {
        "三角恋": {
            "setup": "A喜欢B，B喜欢C，C喜欢A",
            "tension": "情感纠葛+误会+选择困难",
            "resolution": "有人退出/有人觉醒/意外事件打破僵局",
        },
        "身份对立": {
            "setup": "两个角色因身份/立场对立",
            "tension": "理念冲突+被迫合作+互相理解",
            "resolution": "一方妥协/第三方介入/共同敌人出现",
        },
        "资源争夺": {
            "setup": "多方势力争夺同一资源",
            "tension": "明争暗斗+联盟背叛+渔翁得利",
            "resolution": "资源真相揭露/重新分配/共同开发",
        },
        "理念冲突": {
            "setup": "新旧观念/不同价值观碰撞",
            "tension": "说服与反抗+实践检验+代价显现",
            "resolution": "融合创新/一方证明正确/第三方方案",
        },
    }

    # 反转模板
    TWIST_TEMPLATES = [
        {
            "name": "身份反转",
            "description": "看似普通的人其实是关键人物",
            "example": "一直帮助主角的老乞丐，其实是退隐的绝世高手",
        },
        {
            "name": "立场反转",
            "description": "以为是敌人的人其实是盟友",
            "example": "一直追杀主角的刺客，其实是在保护主角",
        },
        {
            "name": "真相反转",
            "description": "表面真相背后有更大的真相",
            "example": "以为是意外死亡，其实是精心策划的谋杀",
        },
        {
            "name": "时间反转",
            "description": "时间线被重新解读",
            "example": "以为是预知未来，其实是曾经经历过的过去",
        },
        {
            "name": "动机反转",
            "description": "角色的真实动机与表面不同",
            "example": "反派毁灭世界是为了拯救更多人",
        },
    ]


class PlotBrainstormEngine:
    """剧情构思引擎"""

    def __init__(self, memory_manager=None, creative_engine=None):
        self.templates = PlotTemplateLibrary()
        self.memory = memory_manager
        self.engine = creative_engine
        self.generated_plots: List[PlotArc] = []
        self.plot_counter = 0

    def brainstorm_ideas(self, genre: str, theme: str = "",
                         count: int = 5) -> List[Dict[str, str]]:
        """生成剧情灵感点子"""
        ideas = []

        matching_templates = [
            name for name, tmpl in self.templates.CLASSIC_PLOTS.items()
            if genre in tmpl["best_for"] or not genre
        ]

        if not matching_templates:
            matching_templates = list(self.templates.CLASSIC_PLOTS.keys())

        for i in range(count):
            template_name = random.choice(matching_templates)
            template = self.templates.CLASSIC_PLOTS[template_name]

            stage = random.choice(template["stages"])
            twist = random.choice(self.templates.TWIST_TEMPLATES)

            idea = {
                "id": f"idea_{self.plot_counter + i + 1}",
                "template": template_name,
                "core_concept": f"基于「{template_name}」模板的{genre}故事",
                "opening_scene": self._generate_opening_scene(genre, template),
                "key_conflict": self._generate_conflict_idea(genre),
                "suggested_twist": twist["description"],
                "emotional_core": random.choice([
                    "热血燃爆", "虐心催泪", "爽快解压",
                    "悬疑紧张", "温馨治愈", "黑色幽默",
                ]),
            }
            ideas.append(idea)

        self.plot_counter += count
        return ideas

    def _generate_opening_scene(self, genre: str,
                                template: Dict) -> str:
        """生成开场场景描述"""
        openings = {
            "玄幻": [
                "少年在宗门测试中觉醒废灵根，被所有人嘲笑",
                "山村少年意外捡到一枚神秘玉佩，命运从此改变",
                "天才陨落，从云端跌入泥潭，未婚妻当众退婚",
            ],
            "都市": [
                "退役兵王回到都市，在公交车上遇到美女总裁被调戏",
                "外卖小哥送餐时意外救下被追杀的神秘老人",
                "破产富二代在出租屋里醒来，手机弹出一条神秘短信",
            ],
            "悬疑": [
                "法医在解剖室发现尸体手中握着一张写有自己名字的纸条",
                "小区连续发生失踪案，监控录像里出现同一个不存在的人",
                "收到一封来自三年前已死之人的邮件",
            ],
            "言情": [
                "婚礼当天，新郎逃婚，女主在雨中遇到了真正的命中注定",
                "被迫嫁给传闻中残暴的王爷，却发现他并非表面那样",
                "重生回到被渣男抛弃的那一天，这次她选择先甩了他",
            ],
        }

        pool = openings.get(genre, openings["玄幻"])
        return random.choice(pool)

    def _generate_conflict_idea(self, genre: str) -> str:
        """生成冲突点子"""
        conflict = random.choice(list(self.templates.CONFLICT_TEMPLATES.items()))
        name, detail = conflict
        return f"「{name}」: {detail['setup']} → {detail['tension']} → {detail['resolution']}"

    def design_plot_arc(self, arc_type: PlotArcType,
                        total_chapters: int = 30,
                        genre: str = "玄幻") -> PlotArc:
        """设计完整剧情弧光"""
        self.plot_counter += 1
        arc = PlotArc(
            arc_id=f"arc_{self.plot_counter}",
            name=f"{arc_type.value} - {genre}",
            arc_type=arc_type,
            description=f"基于{arc_type.value}结构的{genre}剧情弧光",
            start_chapter=1,
            end_chapter=total_chapters,
        )

        if arc_type == PlotArcType.THREE_ACT:
            arc.nodes = self._build_three_act(total_chapters, genre)
        elif arc_type == PlotArcType.HERO_JOURNEY:
            arc.nodes = self._build_hero_journey(total_chapters, genre)
        elif arc_type == PlotArcType.REVENGE_ARC:
            arc.nodes = self._build_revenge_arc(total_chapters, genre)
        elif arc_type == PlotArcType.GROWTH_ARC:
            arc.nodes = self._build_growth_arc(total_chapters, genre)
        else:
            arc.nodes = self._build_three_act(total_chapters, genre)

        self.generated_plots.append(arc)
        return arc

    def _build_three_act(self, chapters: int, genre: str) -> List[PlotNode]:
        """构建三幕结构"""
        nodes = []
        act1_end = max(1, chapters // 4)
        act2_end = max(act1_end + 1, chapters * 3 // 4)

        nodes.append(PlotNode(
            node_id="act1_start", chapter=1,
            title="平凡世界", description="展示主角的日常和内心渴望",
            conflict_type=ConflictType.PERSON_VS_SELF,
            characters_involved=["主角"], emotional_beat="平静",
        ))

        nodes.append(PlotNode(
            node_id="act1_inciting", chapter=max(2, act1_end // 2),
            title="激励事件", description="打破日常的重大事件发生",
            conflict_type=ConflictType.PERSON_VS_FATE,
            characters_involved=["主角"], emotional_beat="震惊",
            is_twist=True,
        ))

        nodes.append(PlotNode(
            node_id="act1_end", chapter=act1_end,
            title="跨过门槛", description="主角做出不可逆的决定，进入新世界",
            conflict_type=ConflictType.PERSON_VS_SELF,
            characters_involved=["主角"], emotional_beat="决心",
        ))

        mid = (act1_end + act2_end) // 2
        nodes.append(PlotNode(
            node_id="act2_midpoint", chapter=mid,
            title="中点转折", description="重大揭露或假胜利/假失败",
            conflict_type=ConflictType.PERSON_VS_PERSON,
            characters_involved=["主角", "反派"], emotional_beat="紧张",
            is_twist=True,
        ))

        nodes.append(PlotNode(
            node_id="act2_low", chapter=act2_end - 1,
            title="至暗时刻", description="主角遭遇最大失败，一切似乎无望",
            conflict_type=ConflictType.PERSON_VS_SELF,
            characters_involved=["主角"], emotional_beat="绝望",
        ))

        nodes.append(PlotNode(
            node_id="act3_climax", chapter=act2_end,
            title="最终对决", description="主角与反派的终极决战",
            conflict_type=ConflictType.PERSON_VS_PERSON,
            characters_involved=["主角", "反派"], emotional_beat="燃",
            is_climax=True,
        ))

        nodes.append(PlotNode(
            node_id="act3_resolution", chapter=chapters,
            title="新的平衡", description="世界恢复平静，主角完成蜕变",
            conflict_type=ConflictType.PERSON_VS_SELF,
            characters_involved=["主角"], emotional_beat="释然",
        ))

        return nodes

    def _build_hero_journey(self, chapters: int, genre: str) -> List[PlotNode]:
        """构建英雄之旅结构"""
        nodes = []
        step_chapters = max(1, chapters // 12)

        journey_steps = [
            ("ordinary_world", "平凡世界", "主角在平凡世界中生活"),
            ("call_to_adventure", "冒险召唤", "命运向主角发出召唤"),
            ("refusal", "拒绝召唤", "主角因恐惧而拒绝"),
            ("mentor", "遇见导师", "导师出现给予指引"),
            ("cross_threshold", "跨越门槛", "主角进入非凡世界"),
            ("tests_allies", "考验与盟友", "遭遇考验，结识盟友"),
            ("approach", "接近核心", "接近最大的挑战"),
            ("ordeal", "核心考验", "面对最大的恐惧与挑战"),
            ("reward", "获得奖赏", "战胜考验获得奖赏"),
            ("road_back", "归途", "带着奖赏返回"),
            ("resurrection", "复活", "经历最后的净化与转变"),
            ("return", "带着灵药归来", "以全新的自我回归平凡世界"),
        ]

        for i, (step_id, title, desc) in enumerate(journey_steps):
            ch = min(i * step_chapters + 1, chapters)
            is_climax = (step_id == "ordeal")
            is_twist = (step_id in ["call_to_adventure", "ordeal", "resurrection"])

            nodes.append(PlotNode(
                node_id=step_id, chapter=ch,
                title=title, description=desc,
                conflict_type=ConflictType.PERSON_VS_SELF if i < 4 else ConflictType.PERSON_VS_PERSON,
                characters_involved=["主角"],
                is_climax=is_climax, is_twist=is_twist,
                emotional_beat="燃" if is_climax else "紧张",
            ))

        return nodes

    def _build_revenge_arc(self, chapters: int, genre: str) -> List[PlotNode]:
        """构建复仇弧光"""
        nodes = []
        step = max(1, chapters // 8)

        revenge_steps = [
            ("betrayal", "背叛", "主角被最信任的人背叛"),
            ("fall", "坠落", "主角失去一切，跌入谷底"),
            ("survival", "求生", "在绝境中挣扎求生"),
            ("power_up", "觉醒", "获得复仇的力量/机会"),
            ("first_blood", "初尝复仇", "第一次成功复仇"),
            ("escalation", "冲突升级", "复仇引发更大的冲突"),
            ("revelation", "真相揭露", "发现背叛背后更大的真相"),
            ("final_showdown", "最终对决", "与最终仇敌的决战"),
        ]

        for i, (step_id, title, desc) in enumerate(revenge_steps):
            ch = min(i * step + 1, chapters)
            nodes.append(PlotNode(
                node_id=step_id, chapter=ch,
                title=title, description=desc,
                conflict_type=ConflictType.PERSON_VS_PERSON,
                characters_involved=["主角", "仇敌"],
                is_climax=(step_id == "final_showdown"),
                is_twist=(step_id in ["betrayal", "revelation"]),
                emotional_beat="燃" if step_id == "final_showdown" else "愤怒",
            ))

        return nodes

    def _build_growth_arc(self, chapters: int, genre: str) -> List[PlotNode]:
        """构建成长弧光"""
        nodes = []
        step = max(1, chapters // 6)

        growth_steps = [
            ("flaw", "缺陷展示", "展示主角的核心缺陷"),
            ("desire", "渴望觉醒", "主角意识到自己想要什么"),
            ("struggle", "挣扎尝试", "尝试改变但屡屡失败"),
            ("catalyst", "催化剂事件", "重大事件迫使主角改变"),
            ("transformation", "蜕变", "主角克服缺陷，完成蜕变"),
            ("proof", "证明", "在新挑战中证明自己的成长"),
        ]

        for i, (step_id, title, desc) in enumerate(growth_steps):
            ch = min(i * step + 1, chapters)
            nodes.append(PlotNode(
                node_id=step_id, chapter=ch,
                title=title, description=desc,
                conflict_type=ConflictType.PERSON_VS_SELF,
                characters_involved=["主角"],
                is_climax=(step_id == "transformation"),
                is_twist=(step_id == "catalyst"),
                emotional_beat="感动" if step_id == "transformation" else "期待",
            ))

        return nodes

    def generate_twists(self, count: int = 3) -> List[Dict]:
        """生成剧情反转点子"""
        twists = random.sample(
            self.templates.TWIST_TEMPLATES,
            min(count, len(self.templates.TWIST_TEMPLATES))
        )
        return [
            {"name": t["name"], "description": t["description"],
             "example": t["example"]}
            for t in twists
        ]

    def generate_chapter_outline(self, plot_arc: PlotArc,
                                 genre: str = "玄幻") -> List[Dict]:
        """基于剧情弧光生成逐章大纲"""
        outline = []
        nodes_by_chapter = {}

        for node in plot_arc.nodes:
            ch = node.chapter
            if ch not in nodes_by_chapter:
                nodes_by_chapter[ch] = []
            nodes_by_chapter[ch].append(node)

        for ch in range(plot_arc.start_chapter, plot_arc.end_chapter + 1):
            chapter_info = {
                "chapter": ch,
                "title": f"第{ch}章",
                "summary": "",
                "key_events": [],
                "characters": [],
                "emotional_beat": "neutral",
                "has_twist": False,
                "has_climax": False,
            }

            if ch in nodes_by_chapter:
                for node in nodes_by_chapter[ch]:
                    chapter_info["title"] = node.title
                    chapter_info["summary"] = node.description
                    chapter_info["key_events"].append(node.description)
                    chapter_info["characters"].extend(node.characters_involved)
                    chapter_info["emotional_beat"] = node.emotional_beat
                    if node.is_twist:
                        chapter_info["has_twist"] = True
                    if node.is_climax:
                        chapter_info["has_climax"] = True

            if not chapter_info["summary"]:
                chapter_info["summary"] = self._fill_chapter(ch, plot_arc, genre)

            chapter_info["characters"] = list(set(chapter_info["characters"]))
            outline.append(chapter_info)

        return outline

    def _fill_chapter(self, ch: int, arc: PlotArc, genre: str) -> str:
        """填充章节内容描述"""
        prev_nodes = [n for n in arc.nodes if n.chapter < ch]
        next_nodes = [n for n in arc.nodes if n.chapter > ch]

        if prev_nodes and next_nodes:
            return f"承接「{prev_nodes[-1].title}」，铺垫「{next_nodes[0].title}」"
        elif prev_nodes:
            return f"延续「{prev_nodes[-1].title}」的发展"
        elif next_nodes:
            return f"为「{next_nodes[0].title}」做铺垫"
        return "剧情过渡章节"

    def design_conflict_matrix(self, characters: List[str]) -> Dict[str, Dict[str, str]]:
        """设计角色冲突矩阵"""
        matrix = {}
        conflict_types = list(self.templates.CONFLICT_TEMPLATES.keys())

        for i, char_a in enumerate(characters):
            matrix[char_a] = {}
            for j, char_b in enumerate(characters):
                if i >= j:
                    continue
                conflict = random.choice(conflict_types)
                detail = self.templates.CONFLICT_TEMPLATES[conflict]
                matrix[char_a][char_b] = f"{conflict}: {detail['setup']}"

        return matrix

    def generate_with_ai(self, prompt_type: str, **kwargs) -> Optional[str]:
        """使用AI增强剧情构思（需要creative_engine）"""
        if not self.engine:
            return None

        prompts = {
            "plot_idea": f"请为{kwargs.get('genre', '玄幻')}小说生成3个独特的剧情创意，每个包含核心冲突和情感主线。",
            "chapter_detail": f"请为第{kwargs.get('chapter', 1)}章写详细的剧情展开，包含场景、对话要点和情感节奏。",
            "character_arc": f"请为角色{kwargs.get('name', '主角')}设计完整的角色弧光，包含起点、转折和终点。",
            "world_conflict": f"请为{kwargs.get('world', '玄幻世界')}设计3个核心世界观冲突。",
        }

        prompt = prompts.get(prompt_type, "")
        if not prompt:
            return None

        return self.engine.generate(prompt, system_prompt="你是顶级小说剧情设计师，擅长构建引人入胜的故事结构。")

    def export_plot(self, plot_arc: PlotArc) -> Dict:
        """导出剧情弧光为字典"""
        return {
            "arc_id": plot_arc.arc_id,
            "name": plot_arc.name,
            "arc_type": plot_arc.arc_type.value,
            "description": plot_arc.description,
            "chapters": f"{plot_arc.start_chapter}-{plot_arc.end_chapter}",
            "nodes": [
                {
                    "chapter": n.chapter,
                    "title": n.title,
                    "description": n.description,
                    "is_climax": n.is_climax,
                    "is_twist": n.is_twist,
                    "emotional_beat": n.emotional_beat,
                }
                for n in plot_arc.nodes
            ],
        }


if __name__ == "__main__":
    print("=" * 60)
    print("💡 NWACS 剧情构思引擎测试")
    print("=" * 60)

    engine = PlotBrainstormEngine()

    print("\n【灵感生成 - 玄幻 x5】")
    ideas = engine.brainstorm_ideas("玄幻", count=5)
    for idea in ideas:
        print(f"  📌 {idea['template']}: {idea['opening_scene'][:60]}...")

    print("\n【三幕结构剧情弧光】")
    arc = engine.design_plot_arc(PlotArcType.THREE_ACT, 30, "玄幻")
    for node in arc.nodes:
        markers = []
        if node.is_climax:
            markers.append("🔥高潮")
        if node.is_twist:
            markers.append("🔄反转")
        marker_str = " ".join(markers)
        print(f"  第{node.chapter:2d}章 {node.title}: {node.description} {marker_str}")

    print("\n【英雄之旅剧情弧光】")
    arc2 = engine.design_plot_arc(PlotArcType.HERO_JOURNEY, 24, "玄幻")
    print(f"  共{len(arc2.nodes)}个节点")

    print("\n【反转点子 x3】")
    twists = engine.generate_twists(3)
    for t in twists:
        print(f"  🔄 {t['name']}: {t['example']}")

    print("\n【角色冲突矩阵】")
    matrix = engine.design_conflict_matrix(["叶青云", "苏婉儿", "魔尊", "剑圣"])
    for a, conflicts in matrix.items():
        for b, c in conflicts.items():
            print(f"  {a} ↔ {b}: {c}")

    print("\n【导出剧情弧光】")
    exported = engine.export_plot(arc)
    print(f"  {json.dumps(exported, ensure_ascii=False, indent=2)[:500]}...")
