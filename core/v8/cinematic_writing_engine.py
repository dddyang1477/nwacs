#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 影视感写作引擎 - CinematicWritingEngine

核心能力：
1. 镜头语言技法库 - 远景/中景/特写/运镜/蒙太奇
2. 场景调度系统 - 空间布局/光影/色彩/声音设计
3. 感官描写矩阵 - 五感+动觉+温度觉+平衡觉
4. 节奏控制系统 - 快慢交替/张弛有度/情绪曲线
5. 联网学习模块 - 抓取真实写作技巧并内化
6. 影视感增强器 - 将普通文本改写为影视感文本

设计原则：
- 不是简单堆砌形容词，而是用镜头思维组织文字
- 每个场景都可以被"拍摄"
- 读者脑中自动生成画面
"""

import json
import os
import re
import time
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


# ================================================================
# 镜头类型枚举
# ================================================================

class ShotType(Enum):
    """镜头类型"""
    EXTREME_LONG = ("极远景", "展现宏大场景，人物渺小，强调环境压迫感或史诗感")
    LONG = ("远景", "人物全身+环境，建立空间关系，交代场景全貌")
    FULL = ("全景", "人物全身，展示动作和姿态")
    MEDIUM = ("中景", "人物膝盖以上，最常用的叙事镜头，兼顾动作与表情")
    CLOSE_UP = ("特写", "面部或物体细节，强调情绪和关键信息")
    EXTREME_CLOSE = ("大特写", "眼睛/手指/关键物品，极强的情感冲击力")
    OVER_SHOULDER = ("过肩镜头", "从角色背后拍摄，增强代入感和对话张力")
    POV = ("主观镜头", "角色视角，读者看到角色所看，感受角色所感")
    DUTCH_ANGLE = ("倾斜镜头", "画面倾斜，表现不安/混乱/心理失衡")
    TRACKING = ("跟拍镜头", "跟随角色移动，增强动感和连续性")
    CRANE = ("升降镜头", "从高处下降或从低处升起，揭示信息或升华情感")


class SenseType(Enum):
    """感官类型"""
    VISUAL = ("视觉", "颜色/形状/光影/动作/空间关系")
    AUDITORY = ("听觉", "声音大小/音色/节奏/远近/回声")
    TACTILE = ("触觉", "温度/质地/压力/湿度/疼痛")
    OLFACTORY = ("嗅觉", "气味类型/浓度/来源/联想")
    GUSTATORY = ("味觉", "酸甜苦辣咸/口感/温度")
    KINESTHETIC = ("动觉", "身体运动感/速度/力量/平衡/重心变化")
    THERMAL = ("温度觉", "冷热变化/温差对比")
    PROPRIOCEPTIVE = ("本体觉", "身体位置感/肌肉张力/内脏感觉")


# ================================================================
# 数据结构
# ================================================================

@dataclass
class CinematicTechnique:
    """影视感技法"""
    name: str
    category: str
    description: str
    example_before: str
    example_after: str
    applicable_scenes: List[str]
    difficulty: str = "medium"


@dataclass
class SceneAnalysis:
    """场景分析结果"""
    shot_types_used: List[str]
    sense_types_used: List[str]
    pace: str
    cinematic_score: float
    suggestions: List[str]
    highlight_lines: List[str]


@dataclass
class WebLearningResult:
    """联网学习结果"""
    source_url: str
    topic: str
    key_techniques: List[str]
    examples: List[Dict[str, str]]
    fetched_at: str
    expires_at: str


# ================================================================
# 影视感写作技法库
# ================================================================

CINEMATIC_TECHNIQUES: List[CinematicTechnique] = [
    # ---- 镜头语言 ----
    CinematicTechnique(
        name="远景建立空间",
        category="镜头语言",
        description="开篇用远景交代环境全貌，让读者脑中建立空间坐标系。先画地图，再放人物。",
        example_before="林晨走进了大殿。大殿很宏伟，让他感到震撼。",
        example_after="大殿的穹顶高得仿佛没有尽头，七十二根盘龙柱如巨人的肋骨撑起整片空间。林晨站在门口，身影被拉成一道细长的墨痕——在这庞然巨物面前，他渺小得像一粒尘埃。",
        applicable_scenes=["场景引入", "新地图展开", "势力展示"],
    ),
    CinematicTechnique(
        name="特写聚焦情绪",
        category="镜头语言",
        description="关键时刻切特写，聚焦一个细节让情绪放大十倍。一滴汗、一根颤抖的手指、一个破碎的茶杯。",
        example_before="她非常紧张，手在发抖。",
        example_after="镜头推近——她的指尖。指甲深深掐进掌心，指节泛白，一滴血从指缝渗出，沿着手腕的青色血管缓缓滑落。",
        applicable_scenes=["情绪高潮", "关键抉择", "秘密揭露"],
    ),
    CinematicTechnique(
        name="主观镜头代入",
        category="镜头语言",
        description="切换到角色视角，让读者通过角色的眼睛看世界。所见即所感。",
        example_before="他看到了敌人，敌人很强大。",
        example_after="他的视线穿过飞扬的尘土——首先看到的是一双靴子。黑色的，沾着干涸的血迹。视线往上，铠甲、披风、最后是一张他这辈子都不会忘记的脸。",
        applicable_scenes=["首次遭遇强敌", "重逢场景", "发现真相"],
    ),
    CinematicTechnique(
        name="蒙太奇压缩时间",
        category="镜头语言",
        description="用一组快速切换的画面表现时间流逝或过程推进，避免流水账。",
        example_before="他修炼了三年，终于突破了。",
        example_after="春。瀑布下的少年咬着牙，水花四溅。\n秋。落叶飘过肩头，他的呼吸不再急促。\n冬。冰棱在发梢凝结，他的身体纹丝不动。\n春。瀑布倒流。",
        applicable_scenes=["修炼突破", "时间跨度", "成长蜕变"],
    ),
    CinematicTechnique(
        name="慢镜头放大瞬间",
        category="镜头语言",
        description="关键时刻放慢节奏，把一秒掰成十秒写，每个细节都是子弹时间。",
        example_before="剑刺了过来，他躲开了。",
        example_after="剑尖破空——他能看见空气在剑锋两侧被劈开的纹路。一滴雨水落在剑身上，被切成两半。他的瞳孔收缩，身体开始后仰——但剑更快。时间在这一刻被拉成一根无限细的丝线。",
        applicable_scenes=["生死瞬间", "关键一击", "重大发现"],
    ),

    # ---- 场景调度 ----
    CinematicTechnique(
        name="光影塑造氛围",
        category="场景调度",
        description="用光说话。逆光=神秘/威胁，侧光=立体/矛盾，顶光=压抑/审判，暖光=安全/温馨。",
        example_before="房间里很暗，气氛很诡异。",
        example_after="只有一盏油灯。火苗在穿堂风中摇晃，把所有人的影子拉得忽长忽短，像一群在地板上挣扎的鬼魂。他的脸一半在光里，一半在暗中——光里的那只眼睛在笑，暗里的那只没有。",
        applicable_scenes=["悬疑场景", "权力交锋", "情感对峙"],
    ),
    CinematicTechnique(
        name="色彩情绪映射",
        category="场景调度",
        description="用色彩传递情绪。红色=危险/激情，蓝色=冷静/忧郁，金色=神圣/权力，灰色=压抑/绝望。",
        example_before="战场很惨烈。",
        example_after="这不是他记忆中的草原。绿色被从大地上抹去了——只剩下三种颜色：铁锈的红、灰烬的黑、以及尸体皮肤上那种不正常的蜡黄。",
        applicable_scenes=["战斗场景", "情绪转折", "世界观展示"],
    ),
    CinematicTechnique(
        name="声音层次设计",
        category="场景调度",
        description="声音分三层：前景声（对话/动作）、环境声（风/雨/人群）、内心声（心跳/耳鸣/幻听）。三层叠加产生沉浸感。",
        example_before="周围很吵，他听不清对方在说什么。",
        example_after="声音像被扔进了搅拌机。摊贩的叫卖、马蹄敲击石板、孩子的哭闹——所有这些在他耳边搅成一团噪音。但穿过这层噪音，他清晰地听到了自己的心跳。咚。咚。咚。越来越快。",
        applicable_scenes=["城市场景", "战斗场景", "心理压力"],
    ),
    CinematicTechnique(
        name="空间纵深调度",
        category="场景调度",
        description="前中后景分层。前景=当前焦点，中景=环境信息，后景=潜在威胁或伏笔。",
        example_before="他在街上走着，突然有人跟踪他。",
        example_after="前景：他的手按在剑柄上，指节发白。\n中景：街边小贩正在收摊，铁锅碰撞发出刺耳声响。\n后景：人群中，一个戴斗笠的身影始终保持着三十步的距离。他快，那人也快。他慢，那人也慢。",
        applicable_scenes=["跟踪/追逐", "潜入场景", "危机预感"],
    ),

    # ---- 感官描写 ----
    CinematicTechnique(
        name="五感交响",
        category="感官描写",
        description="每个场景至少调动3种感官。不是罗列，而是让它们像交响乐一样同时奏响。",
        example_before="市场很热闹。",
        example_after="视觉：猩红的辣椒铺了一地，金色的油炸点心在铁锅里翻滚。\n听觉：铁匠铺的锤声像心跳一样规律，面馆老板的吆喝穿透三条街。\n嗅觉：烤肉的焦香和药材的苦味在空气中打架，谁也赢不了谁。",
        applicable_scenes=["场景引入", "氛围营造", "世界构建"],
    ),
    CinematicTechnique(
        name="通感修辞",
        category="感官描写",
        description="用A感官描述B感官体验。声音有了颜色，气味有了形状，让描写超越物理限制。",
        example_before="她的声音很好听。",
        example_after="她的声音像冬天里第一口热茶——从舌尖滑进喉咙，带着茉莉的清香和蜂蜜的甜，最后在胸腔里炸开一小团暖意。",
        applicable_scenes=["人物出场", "情感场景", "意境营造"],
    ),
    CinematicTechnique(
        name="身体记忆唤醒",
        category="感官描写",
        description="用身体感受触发记忆和情感。不是'他想起'，而是'他的身体记得'。",
        example_before="他想起小时候被父亲打的经历。",
        example_after="皮带破空的声音。他的后背先于大脑做出了反应——肩胛骨收紧，脊椎僵硬，一股凉意从尾椎骨窜上后脑勺。二十三年了，他的身体还记得。",
        applicable_scenes=["创伤回忆", "情感触发", "角色深度"],
    ),

    # ---- 节奏控制 ----
    CinematicTechnique(
        name="短句加速",
        category="节奏控制",
        description="战斗/追逐/紧急场景：砍掉所有修饰，主谓宾，句号。心跳节奏。",
        example_before="他快速地跑过走廊，身后追兵越来越近，他感到非常恐惧。",
        example_after="跑。\n转角。\n再跑。\n身后的脚步声密如鼓点。\n不能停。\n肺在燃烧。\n不能停。\n出口——",
        applicable_scenes=["追逐", "战斗高潮", "紧急逃生"],
    ),
    CinematicTechnique(
        name="长句沉溺",
        category="节奏控制",
        description="情感/回忆/意境场景：用长句让读者沉进去，像慢慢沉入温水。",
        example_before="夕阳很美，他感到很平静。",
        example_after="夕阳把整片天空烧成了暗红色，像一张被火焰舔过的宣纸，边缘卷曲着金色的余烬，而他就站在这片燃烧的天空下，第一次觉得——活着，好像也不是一件太坏的事。",
        applicable_scenes=["情感沉淀", "意境描写", "章节收尾"],
    ),
    CinematicTechnique(
        name="段落呼吸法",
        category="节奏控制",
        description="长段落后接短段落，紧张后接松弛。像呼吸一样，一吸一呼，读者才不会窒息。",
        example_before="（连续10段高强度战斗描写）",
        example_after="（5段战斗 + 1段环境空镜 + 1段内心独白 + 5段战斗）",
        applicable_scenes=["长篇战斗", "连续高潮", "情绪起伏"],
    ),

    # ---- 动作设计 ----
    CinematicTechnique(
        name="动作链条",
        category="动作设计",
        description="动作不是孤立的，是因果链条。A导致B，B触发C。每个动作都是上一个动作的必然结果。",
        example_before="他拔出剑，冲向敌人，一剑刺出。",
        example_after="拇指推剑格——剑鞘飞出——脚掌碾地——身体前倾——剑尖画弧——从下往上——挑！",
        applicable_scenes=["战斗场景", "动作描写", "技能展示"],
    ),
    CinematicTechnique(
        name="反应用动作写",
        category="动作设计",
        description="不写'他感到震惊'，写他做了什么。情绪必须外化为可视动作。",
        example_before="听到这个消息，他非常震惊。",
        example_after="茶杯停在了半空。三秒。他缓缓把茶杯放回桌面，瓷器与木头接触时发出一声极轻的响。然后他笑了——但笑意没有到达眼睛。",
        applicable_scenes=["情绪反应", "对话场景", "信息揭露"],
    ),

    # ---- 对话影视化 ----
    CinematicTechnique(
        name="对话+画面交替",
        category="对话影视化",
        description="对话不是广播剧。每2-3句对话插入一个画面描写——动作/表情/环境反应。",
        example_before="A说：'你为什么要这样做？' B说：'我没有选择。' A说：'你总是这样说。'",
        example_after="'你为什么要这样做？'\n窗外的雨突然大了。\n'我没有选择。'\n他的手指摩挲着茶杯边缘，一圈，又一圈。\n'你总是这样说。'\n茶杯裂了。不是摔的——是被捏碎的。",
        applicable_scenes=["关键对话", "情感对峙", "真相揭露"],
    ),
    CinematicTechnique(
        name="潜台词视觉化",
        category="对话影视化",
        description="角色说的和想的不一样。用动作/表情/环境暗示真实想法。",
        example_before="'我不在乎。'她说，但其实她很在乎。",
        example_after="'我不在乎。'\n她说这话的时候在笑。但她的手——她把手藏到了桌子下面。",
        applicable_scenes=["情感掩饰", "权力博弈", "口是心非"],
    ),
]


# ================================================================
# 联网学习模块
# ================================================================

class WebLearningModule:
    """联网学习模块 - 从真实写作资源中学习技法"""

    CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".cinematic_cache")
    CACHE_DURATION = timedelta(hours=24)

    LEARNING_SOURCES = [
        {
            "url": "https://www.zhihu.com/question/23579338",
            "topic": "小说中的镜头语言运用",
            "keywords": ["镜头语言", "视角切换", "画面感", "场景描写"],
        },
        {
            "url": "https://www.zhihu.com/question/20823849",
            "topic": "如何提升小说的画面感和代入感",
            "keywords": ["画面感", "代入感", "五感描写", "细节描写"],
        },
        {
            "url": "https://www.zhihu.com/question/20491031",
            "topic": "网络小说写作技巧大全",
            "keywords": ["写作技巧", "节奏控制", "爽点设计", "人物塑造"],
        },
    ]

    def __init__(self):
        os.makedirs(self.CACHE_DIR, exist_ok=True)

    def learn(self, force_refresh: bool = False) -> List[WebLearningResult]:
        """执行联网学习，返回学习结果"""
        results = []

        for source in self.LEARNING_SOURCES:
            cache_key = hashlib.md5(source["url"].encode()).hexdigest()
            cache_file = os.path.join(self.CACHE_DIR, f"{cache_key}.json")

            if not force_refresh and self._is_cache_valid(cache_file):
                with open(cache_file, "r", encoding="utf-8") as f:
                    cached = json.load(f)
                results.append(WebLearningResult(**cached))
                continue

            result = self._fetch_and_parse(source)
            if result:
                results.append(result)
                self._save_cache(cache_file, result)

        return results

    def _is_cache_valid(self, cache_file: str) -> bool:
        if not os.path.exists(cache_file):
            return False
        mtime = datetime.fromtimestamp(os.path.getmtime(cache_file))
        return datetime.now() - mtime < self.CACHE_DURATION

    def _fetch_and_parse(self, source: Dict) -> Optional[WebLearningResult]:
        """抓取网页并解析写作技巧"""
        try:
            import requests
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                              "AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/120.0.0.0 Safari/537.36"
            }
            resp = requests.get(source["url"], headers=headers, timeout=15)
            resp.raise_for_status()
            html = resp.text

            techniques = self._extract_techniques(html, source["keywords"])
            examples = self._extract_examples(html)

            now = datetime.now()
            return WebLearningResult(
                source_url=source["url"],
                topic=source["topic"],
                key_techniques=techniques,
                examples=examples,
                fetched_at=now.isoformat(),
                expires_at=(now + self.CACHE_DURATION).isoformat(),
            )
        except Exception as e:
            print(f"   ⚠️ 联网学习失败 ({source['url']}): {e}")
            return None

    def _extract_techniques(self, html: str, keywords: List[str]) -> List[str]:
        """从HTML中提取写作技巧"""
        techniques = []
        text = re.sub(r'<[^>]+>', ' ', html)
        text = re.sub(r'\s+', ' ', text)

        patterns = [
            r'(?:技巧|方法|手法|秘诀)[：:]\s*(.{10,80}?)(?:[。！？\n]|$)',
            r'(?:关键是|核心是|重点是|要诀是)\s*(.{10,80}?)(?:[。！？\n]|$)',
            r'(?:建议|推荐|可以尝试)\s*(.{10,80}?)(?:[。！？\n]|$)',
        ]

        for pattern in patterns:
            matches = re.findall(pattern, text)
            for m in matches:
                m = m.strip()
                if len(m) >= 10 and m not in techniques:
                    techniques.append(m)

        if not techniques:
            techniques = [
                f"关于{kw}：多观察生活中的细节，将其转化为文字",
                f"提升{kw}：阅读优秀作品，分析其写作手法",
            ]
            for kw in keywords[:2]:
                pass

        return techniques[:10]

    def _extract_examples(self, html: str) -> List[Dict[str, str]]:
        """从HTML中提取写作示例"""
        examples = []
        text = re.sub(r'<[^>]+>', ' ', html)
        text = re.sub(r'\s+', ' ', text)

        example_patterns = [
            r'(?:例如|比如|举例|如)\s*(.{20,150}?)(?:[。！？]|$)',
            r'(?:原文|原句|改写前)[：:]\s*(.{20,150}?)(?:[。！？]|$)',
            r'(?:修改后|改写后|优化后)[：:]\s*(.{20,150}?)(?:[。！？]|$)',
        ]

        for pattern in example_patterns:
            matches = re.findall(pattern, text)
            for m in matches:
                m = m.strip()
                if 10 <= len(m) <= 200:
                    examples.append({"text": m, "source": "web"})

        return examples[:5]

    def _save_cache(self, cache_file: str, result: WebLearningResult):
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(result.__dict__, f, ensure_ascii=False, indent=2)

    def get_learning_summary(self) -> str:
        """获取学习摘要，用于注入提示词"""
        results = self.learn()
        if not results:
            return ""

        summary_parts = ["【联网学习的写作技法】"]
        for r in results:
            summary_parts.append(f"\n来源: {r.topic}")
            for i, tech in enumerate(r.key_techniques[:3], 1):
                summary_parts.append(f"  {i}. {tech}")

        return "\n".join(summary_parts)


# ================================================================
# 影视感写作引擎
# ================================================================

class CinematicWritingEngine:
    """影视感写作引擎 - 核心类"""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv(
            "DEEPSEEK_API_KEY",
            "sk-f3246fbd1eef446e9a11d78efefd9bba"
        )
        self.base_url = "https://api.deepseek.com"
        self.web_learner = WebLearningModule()
        self.techniques = CINEMATIC_TECHNIQUES
        self._technique_index = self._build_index()

    def _build_index(self) -> Dict[str, List[CinematicTechnique]]:
        index = {}
        for t in self.techniques:
            index.setdefault(t.category, []).append(t)
        return index

    def get_categories(self) -> List[str]:
        return list(self._technique_index.keys())

    def get_techniques_by_category(self, category: str) -> List[CinematicTechnique]:
        return self._technique_index.get(category, [])

    def get_techniques_for_scene(self, scene_type: str) -> List[CinematicTechnique]:
        matched = []
        for t in self.techniques:
            if any(s in scene_type for s in t.applicable_scenes):
                matched.append(t)
        return matched

    def build_system_prompt(self, genre: str = "玄幻",
                            intensity: str = "high",
                            include_web_learning: bool = True) -> str:
        """构建影视感写作系统提示词"""

        prompt = f"""你是一位精通影视化写作的顶级{genre}小说作家。你的文字不是被"阅读"的，而是被"看见"的。

【核心写作原则：用镜头写作】

1. 镜头意识：
   - 每个场景开始前，先在脑中确定机位和景别
   - 远景建立空间 → 中景推进叙事 → 特写引爆情绪
   - 镜头要有变化：推、拉、摇、移、跟、升、降
   - 关键瞬间使用慢镜头，把一秒掰成十秒写

2. 场景调度：
   - 前中后景分层：前景焦点 + 中景信息 + 后景伏笔
   - 光影说话：逆光=威胁，侧光=矛盾，暖光=安全
   - 色彩即情绪：红=危险/激情，蓝=冷静/忧郁，灰=压抑
   - 声音三层：前景声+环境声+内心声同时奏响

3. 感官矩阵（每个场景至少3种感官）：
   - 视觉(40%)：颜色、形状、光影、动作、空间关系
   - 听觉(25%)：音量、音色、节奏、远近、回声
   - 触觉(15%)：温度、质地、压力、湿度
   - 嗅觉(10%)：气味类型、浓度、来源
   - 味觉(5%)：酸甜苦辣咸、口感
   - 动觉(5%)：速度感、力量感、平衡感

4. 节奏控制：
   - 战斗/追逐：短句。主谓宾。句号。心跳节奏。
   - 情感/意境：长句。让读者沉进去。
   - 段落呼吸法：紧张后必有松弛，长段落后接短段落。
   - 每500字至少一次节奏变化。

5. 动作设计：
   - 动作是因果链条，不是孤立招式
   - 情绪必须外化为可视动作（不写"他愤怒"，写他做了什么）
   - 反应用动作写，不用形容词写

6. 对话影视化：
   - 每2-3句对话插入画面描写
   - 潜台词用动作/表情暗示
   - 对话不是广播剧，要有空间感和身体感

7. 蒙太奇技巧：
   - 时间跨度用一组快速切换的画面表现
   - 避免"三年后"这种粗暴跳转

【禁止事项】
- 禁止大段静态心理描写（内心戏必须外化）
- 禁止"他感到""他觉得""他心想"（用动作和感官替代）
- 禁止形容词堆砌（一个精准动词胜过三个形容词）
- 禁止平铺直叙的流水账
- 禁止"本章结束""未完待续"等元叙述

【影视感强度: {intensity}】
"""

        if include_web_learning:
            try:
                from deep_learning_engine import get_deep_learning_engine
                dl_engine = get_deep_learning_engine()
                dl_injection = dl_engine.build_learning_injection(genre)
                if dl_injection:
                    prompt += f"\n{dl_injection}\n"
            except ImportError:
                web_summary = self.web_learner.get_learning_summary()
                if web_summary:
                    prompt += f"\n{web_summary}\n"

        prompt += "\n现在，请用镜头语言创作。让每一个字都能被拍摄。"
        return prompt

    def build_chapter_prompt(self, chapter_num: int, title: str,
                             summary: str, key_points: List[str],
                             genre: str = "玄幻",
                             target_words: int = 4000) -> str:
        """构建单章影视感写作提示词"""

        points_text = "\n".join(f"  - {p}" for p in key_points)

        return f"""请创作第{chapter_num}章：{title}

【本章概要】
{summary}

【关键情节点】
{points_text}

【影视感写作要求】
- 开篇用远景建立场景空间感
- 至少使用3种镜头类型（远景/中景/特写/主观镜头/慢镜头）
- 每个场景调动至少3种感官
- 战斗/冲突场景使用短句加速节奏
- 情感场景使用长句+感官细节
- 对话中穿插画面描写（每2-3句对话插入一个画面）
- 情绪用动作外化，不写"他感到"
- 关键瞬间使用慢镜头放大细节
- 结尾留一个视觉化的钩子

【硬性要求】
- 字数不少于{target_words}字
- 内容充实，拒绝灌水
- 直接输出章节正文，不要标题和元叙述"""

    def analyze_scene(self, text: str) -> SceneAnalysis:
        """分析文本的影视感程度"""
        shot_types_found = []
        sense_types_found = []

        shot_keywords = {
            "远景": ["远望", "俯瞰", "天际", "地平线", "广袤", "一望无际", "苍穹"],
            "特写": ["指尖", "瞳孔", "嘴角", "眉梢", "青筋", "汗珠", "泪痕"],
            "慢镜头": ["缓缓", "慢慢", "一点一点", "逐", "寸"],
            "主观镜头": ["视线", "目光所及", "映入眼帘", "眼前"],
            "蒙太奇": ["画面切换", "与此同时", "镜头一转"],
        }

        sense_keywords = {
            "视觉": ["颜色", "光", "暗", "红", "蓝", "金", "黑", "白", "影"],
            "听觉": ["声音", "响", "轰鸣", "低语", "尖叫", "沉默", "回音", "嗡"],
            "触觉": ["冰冷", "滚烫", "粗糙", "光滑", "刺痛", "麻木"],
            "嗅觉": ["气味", "香", "臭", "腥", "焦", "腐"],
            "动觉": ["速度", "力量", "冲击", "震动", "失衡", "旋转"],
        }

        for shot, keywords in shot_keywords.items():
            if any(kw in text for kw in keywords):
                shot_types_found.append(shot)

        for sense, keywords in sense_keywords.items():
            if any(kw in text for kw in keywords):
                sense_types_found.append(sense)

        short_sentences = len(re.findall(r'[^。！？]{1,15}[。！？]', text))
        long_sentences = len(re.findall(r'[^。！？]{40,}[。！？]', text))
        total_sentences = max(len(re.findall(r'[。！？]', text)), 1)

        if short_sentences / total_sentences > 0.3:
            pace = "快速"
        elif long_sentences / total_sentences > 0.3:
            pace = "缓慢"
        else:
            pace = "适中"

        cinematic_score = min(100, (
            len(shot_types_found) * 15 +
            len(sense_types_found) * 10 +
            (10 if pace == "适中" else 5) +
            min(20, text.count("\n\n") * 2)
        ))

        suggestions = []
        if len(shot_types_found) < 2:
            suggestions.append("建议增加镜头变化（远景→中景→特写）")
        if len(sense_types_found) < 3:
            suggestions.append("建议增加感官描写（至少3种感官）")
        if "慢镜头" not in shot_types_found:
            suggestions.append("关键瞬间可使用慢镜头放大细节")
        if text.count("\n\n") < 3:
            suggestions.append("建议增加段落呼吸空间")

        highlight_lines = []
        for line in text.split("\n"):
            line = line.strip()
            if len(line) > 20 and any(
                kw in line for kw in ["指尖", "瞳孔", "光影", "声音", "气味", "温度"]
            ):
                highlight_lines.append(line[:80])

        return SceneAnalysis(
            shot_types_used=shot_types_found,
            sense_types_used=sense_types_found,
            pace=pace,
            cinematic_score=cinematic_score,
            suggestions=suggestions,
            highlight_lines=highlight_lines[:5],
        )

    def enhance_cinematic_quality(self, text: str, genre: str = "玄幻",
                                  intensity: str = "high") -> str:
        """使用DeepSeek API增强文本的影视感"""
        system_prompt = self.build_system_prompt(genre, intensity, include_web_learning=False)

        prompt = f"""请将以下文本改写为影视感更强的版本。保持原意和情节不变，但用镜头语言重新组织文字。

改写要求：
- 增加镜头变化（远景/中景/特写/慢镜头）
- 丰富感官描写（至少3种感官）
- 优化节奏（战斗加速，情感减速）
- 情绪外化为可视动作
- 对话中插入画面描写
- 保持原有字数的80%-120%

原文：
{text}

请直接输出改写后的文本："""

        try:
            import requests
            url = f"{self.base_url}/v1/chat/completions"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            data = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.8,
                "max_tokens": 16000,
            }
            resp = requests.post(url, headers=headers, json=data, timeout=180)
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"   ❌ 影视感增强失败: {e}")
            return text

    def generate_cinematic_chapter(self, chapter_num: int, title: str,
                                   summary: str, key_points: List[str],
                                   genre: str = "玄幻",
                                   target_words: int = 4000) -> str:
        """直接生成影视感章节"""
        system_prompt = self.build_system_prompt(genre, "high")
        user_prompt = self.build_chapter_prompt(
            chapter_num, title, summary, key_points, genre, target_words
        )

        try:
            import requests
            url = f"{self.base_url}/v1/chat/completions"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            data = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "temperature": 0.85,
                "max_tokens": 16000,
            }
            resp = requests.post(url, headers=headers, json=data, timeout=300)
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"   ❌ 影视感章节生成失败: {e}")
            return ""

    def get_technique_cheatsheet(self) -> str:
        """生成技法速查表"""
        lines = [
            "=" * 60,
            "🎬 影视感写作技法速查表",
            "=" * 60,
        ]
        for category, techniques in self._technique_index.items():
            lines.append(f"\n【{category}】")
            for t in techniques:
                lines.append(f"  ▶ {t.name}")
                lines.append(f"    {t.description[:60]}...")
                lines.append(f"    适用: {', '.join(t.applicable_scenes[:3])}")
        return "\n".join(lines)


# ================================================================
# 便捷函数
# ================================================================

_cinematic_engine: Optional[CinematicWritingEngine] = None


def get_cinematic_engine() -> CinematicWritingEngine:
    global _cinematic_engine
    if _cinematic_engine is None:
        _cinematic_engine = CinematicWritingEngine()
    return _cinematic_engine


def enhance_text_cinematic(text: str, genre: str = "玄幻") -> str:
    return get_cinematic_engine().enhance_cinematic_quality(text, genre)


def analyze_text_cinematic(text: str) -> SceneAnalysis:
    return get_cinematic_engine().analyze_scene(text)


def get_cinematic_system_prompt(genre: str = "玄幻") -> str:
    return get_cinematic_engine().build_system_prompt(genre)


# ================================================================
# 自测
# ================================================================

if __name__ == "__main__":
    engine = CinematicWritingEngine()

    print("=" * 60)
    print("🎬 影视感写作引擎 - 自测")
    print("=" * 60)

    print(f"\n技法分类: {engine.get_categories()}")
    print(f"技法总数: {len(engine.techniques)}")

    test_text = """
    林晨走进了大殿。大殿很宏伟，让他感到震撼。
    他看到了殿中的长老们，他们看起来很威严。
    林晨感到紧张，但他努力保持镇定。
    长老问他是否准备好了，他说准备好了。
    """

    print("\n📝 原始文本:")
    print(test_text)

    print("\n🔍 场景分析:")
    analysis = engine.analyze_scene(test_text)
    print(f"  镜头类型: {analysis.shot_types_used}")
    print(f"  感官类型: {analysis.sense_types_used}")
    print(f"  节奏: {analysis.pace}")
    print(f"  影视感评分: {analysis.cinematic_score}/100")
    print(f"  建议: {analysis.suggestions}")

    print("\n🎬 影视感增强:")
    enhanced = engine.enhance_cinematic_quality(test_text)
    print(enhanced[:500])

    print("\n📋 技法速查表:")
    print(engine.get_technique_cheatsheet()[:500])

    print("\n✅ 自测完成")
