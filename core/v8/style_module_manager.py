#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS AI风格模块系统 - StyleModuleManager

对标 NovelAI AI Modules，核心能力：
1. 风格模块市场 - 预训练风格包库
2. 一键切换 - 运行时动态切换写作风格
3. 风格混合 - 多风格按权重融合
4. 自定义训练 - 从样本文本提取风格模块
5. 风格对比 - 同段文字多风格输出对比

内置风格模块：
- 古风典雅 / 现代简约 / 热血燃爆 / 悬疑冷峻
- 言情细腻 / 玄幻磅礴 / 科幻理性 / 幽默诙谐
"""

import json
import os
import re
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from collections import Counter


class StyleCategory(Enum):
    CLASSICAL = ("古风典雅", "古典文学风格，文言韵味，辞藻华丽")
    MODERN = ("现代简约", "现代白话风格，简洁明快，贴近生活")
    HOT_BLOODED = ("热血燃爆", "激情澎湃，节奏紧凑，爽感十足")
    SUSPENSE = ("悬疑冷峻", "冷静克制，层层递进，氛围压抑")
    ROMANCE = ("言情细腻", "情感丰富，心理描写深入，温柔缱绻")
    FANTASY = ("玄幻磅礴", "气势恢宏，想象力丰富，设定宏大")
    SCIFI = ("科幻理性", "逻辑严密，科技感强，理性克制")
    HUMOR = ("幽默诙谐", "轻松有趣，吐槽犀利，节奏明快")
    REALISTIC = ("现实主义", "贴近生活，细节真实，社会洞察")
    POETIC = ("诗意朦胧", "意境优美，留白丰富，含蓄隽永")

    def __init__(self, label: str, description: str):
        self.label = label
        self.description = description


@dataclass
class StyleModule:
    module_id: str
    name: str
    category: StyleCategory
    description: str
    system_prompt: str
    writing_rules: List[str] = field(default_factory=list)
    vocabulary_bias: Dict[str, float] = field(default_factory=dict)
    sentence_patterns: List[str] = field(default_factory=list)
    forbidden_patterns: List[str] = field(default_factory=list)
    example_text: str = ""
    tags: List[str] = field(default_factory=list)
    version: str = "1.0"
    author: str = "NWACS"

    def to_dict(self) -> dict:
        return {
            "module_id": self.module_id,
            "name": self.name,
            "category": self.category.label,
            "description": self.description,
            "system_prompt": self.system_prompt,
            "writing_rules": self.writing_rules,
            "vocabulary_bias": self.vocabulary_bias,
            "sentence_patterns": self.sentence_patterns,
            "forbidden_patterns": self.forbidden_patterns,
            "example_text": self.example_text,
            "tags": self.tags,
            "version": self.version,
            "author": self.author,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "StyleModule":
        cat_map = {c.label: c for c in StyleCategory}
        return cls(
            module_id=data["module_id"],
            name=data["name"],
            category=cat_map.get(data["category"], StyleCategory.MODERN),
            description=data["description"],
            system_prompt=data["system_prompt"],
            writing_rules=data.get("writing_rules", []),
            vocabulary_bias=data.get("vocabulary_bias", {}),
            sentence_patterns=data.get("sentence_patterns", []),
            forbidden_patterns=data.get("forbidden_patterns", []),
            example_text=data.get("example_text", ""),
            tags=data.get("tags", []),
            version=data.get("version", "1.0"),
            author=data.get("author", "NWACS"),
        )


class StyleModuleManager:
    """AI风格模块管理器"""

    def __init__(self, storage_dir: str = None):
        if storage_dir is None:
            storage_dir = os.path.join(os.path.dirname(__file__), "..", "style_modules")
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)

        self.modules: Dict[str, StyleModule] = {}
        self.active_module: Optional[StyleModule] = None
        self.active_blend: Dict[str, float] = {}
        self._load()

    def _get_filepath(self) -> str:
        return os.path.join(self.storage_dir, "style_modules.json")

    def _load(self):
        filepath = self._get_filepath()
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            for mod_data in data.get("modules", []):
                module = StyleModule.from_dict(mod_data)
                self.modules[module.module_id] = module
            active_id = data.get("active_module", "")
            if active_id and active_id in self.modules:
                self.active_module = self.modules[active_id]
            self.active_blend = data.get("active_blend", {})
        else:
            self._init_builtin_modules()

    def save(self):
        data = {
            "version": "1.0",
            "updated_at": datetime.now().isoformat(),
            "active_module": self.active_module.module_id if self.active_module else "",
            "active_blend": self.active_blend,
            "modules": [m.to_dict() for m in self.modules.values()],
        }
        with open(self._get_filepath(), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def register_module(self, module: StyleModule):
        self.modules[module.module_id] = module
        self.save()

    def unregister_module(self, module_id: str) -> bool:
        if module_id in self.modules:
            if self.active_module and self.active_module.module_id == module_id:
                self.active_module = None
            del self.modules[module_id]
            self.save()
            return True
        return False

    def activate(self, module_id: str) -> bool:
        if module_id in self.modules:
            self.active_module = self.modules[module_id]
            self.active_blend = {}
            self.save()
            return True
        return False

    def blend(self, weights: Dict[str, float]) -> bool:
        """多风格混合"""
        total = sum(weights.values())
        if total == 0:
            return False
        normalized = {k: v / total for k, v in weights.items()}
        for mid in normalized:
            if mid not in self.modules:
                return False
        self.active_blend = normalized
        self.active_module = None
        self.save()
        return True

    def get_active_prompt(self) -> str:
        """获取当前激活风格的system prompt"""
        if self.active_module:
            return self.active_module.system_prompt
        if self.active_blend:
            parts = []
            for mid, weight in self.active_blend.items():
                module = self.modules[mid]
                parts.append(f"[{module.name} 权重{weight:.0%}]\n{module.system_prompt}")
            return "\n\n".join(parts)
        return ""

    def get_active_rules(self) -> List[str]:
        if self.active_module:
            return self.active_module.writing_rules
        if self.active_blend:
            rules = []
            for mid, weight in self.active_blend.items():
                if weight >= 0.3:
                    rules.extend(self.modules[mid].writing_rules)
            return list(set(rules))
        return []

    def get_active_vocabulary(self) -> Dict[str, float]:
        if self.active_module:
            return self.active_module.vocabulary_bias
        if self.active_blend:
            merged = {}
            for mid, weight in self.active_blend.items():
                for word, bias in self.modules[mid].vocabulary_bias.items():
                    merged[word] = merged.get(word, 0) + bias * weight
            return merged
        return {}

    def list_modules(self, category: StyleCategory = None) -> List[StyleModule]:
        modules = list(self.modules.values())
        if category:
            modules = [m for m in modules if m.category == category]
        return modules

    def extract_style_from_text(self, text: str, name: str,
                                 category: StyleCategory) -> StyleModule:
        """从样本文本中提取风格模块"""
        import uuid

        sentences = re.split(r'[。！？；\n]', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 5]

        lengths = [len(s) for s in sentences]
        avg_len = sum(lengths) / max(len(lengths), 1)

        words = re.findall(r'[\u4e00-\u9fff]+', text)
        word_freq = Counter(words)
        top_words = word_freq.most_common(30)

        vocab_bias = {}
        for word, count in top_words:
            vocab_bias[word] = min(count / max(len(sentences), 1), 1.0)

        if avg_len < 15:
            pattern = "短句为主，节奏明快"
        elif avg_len < 30:
            pattern = "中短句结合，张弛有度"
        else:
            pattern = "长句为主，铺陈细腻"

        rules = [
            f"平均句长约{avg_len:.0f}字",
            f"高频词汇: {', '.join([w for w, _ in top_words[:10]])}",
            pattern,
        ]

        module = StyleModule(
            module_id=str(uuid.uuid4())[:8],
            name=name,
            category=category,
            description=f"从文本中提取的{category.label}风格",
            system_prompt=f"请以{category.label}风格写作。{pattern}。",
            writing_rules=rules,
            vocabulary_bias=vocab_bias,
            example_text=text[:500],
            tags=["extracted", category.label],
        )
        self.register_module(module)
        return module

    def compare_styles(self, text: str, module_ids: List[str]) -> Dict[str, str]:
        """同段文字多风格改写建议"""
        results = {}
        for mid in module_ids:
            if mid in self.modules:
                module = self.modules[mid]
                results[module.name] = {
                    "rules": module.writing_rules,
                    "vocabulary": list(module.vocabulary_bias.keys())[:10],
                    "prompt": module.system_prompt,
                }
        return results

    def get_stats(self) -> dict:
        by_category = {}
        for cat in StyleCategory:
            count = len(self.list_modules(cat))
            if count > 0:
                by_category[cat.label] = count

        return {
            "total_modules": len(self.modules),
            "active_style": self.active_module.name if self.active_module else (
                "混合风格" if self.active_blend else "无"
            ),
            "by_category": by_category,
        }

    def _init_builtin_modules(self):
        """初始化内置风格模块"""
        builtins = [
            StyleModule(
                module_id="style_classical",
                name="古风典雅",
                category=StyleCategory.CLASSICAL,
                description="古典文学风格，文言韵味，辞藻华丽，适合仙侠/历史题材",
                system_prompt="""你是一位精通古典文学的作家。请以古风典雅风格写作：
- 多用四字成语和文言句式
- 注重意境营造和留白
- 辞藻华丽但不堆砌
- 节奏舒缓，如行云流水
- 善用对仗、排比等修辞""",
                writing_rules=[
                    "多用四字成语，如'风起云涌''剑气纵横'",
                    "句式以四六骈文为主，长短交错",
                    "描写重意境轻细节，留白三分",
                    "对话半文半白，符合古风韵味",
                    "避免现代词汇和网络用语",
                ],
                vocabulary_bias={
                    "苍穹": 0.9, "云霄": 0.8, "苍穹": 0.9, "浩瀚": 0.8,
                    "巍峨": 0.8, "缥缈": 0.9, "凌厉": 0.7, "磅礴": 0.8,
                    "沧桑": 0.7, "风华": 0.8, "绝代": 0.7, "倾城": 0.7,
                },
                sentence_patterns=["四六骈文", "五言七言", "长短交错"],
                forbidden_patterns=["卧槽", "牛逼", "666", "绝绝子"],
                example_text="苍穹之上，一道剑光划破长空。那少年负手而立，衣袂飘飘，目光如电，扫视着脚下万里山河。",
            ),
            StyleModule(
                module_id="style_hotblood",
                name="热血燃爆",
                category=StyleCategory.HOT_BLOODED,
                description="激情澎湃，节奏紧凑，爽感十足，适合玄幻/竞技题材",
                system_prompt="""你是一位擅长热血爽文的作家。请以热血燃爆风格写作：
- 短句为主，节奏紧凑如鼓点
- 大量动作描写和感官刺激
- 情绪渲染强烈，让读者热血沸腾
- 善用感叹号和短段落制造冲击力
- 每段结尾留钩子，让人欲罢不能""",
                writing_rules=[
                    "短句为主，每句不超过20字",
                    "多用感叹号和省略号制造张力",
                    "每200字一个小高潮，每章一个大高潮",
                    "战斗描写细致，拳拳到肉",
                    "主角台词要有气势，金句频出",
                ],
                vocabulary_bias={
                    "爆发": 0.9, "碾压": 0.9, "震撼": 0.8, "恐怖": 0.8,
                    "疯狂": 0.8, "燃烧": 0.9, "沸腾": 0.8, "咆哮": 0.7,
                    "毁灭": 0.7, "无敌": 0.8, "逆天": 0.8, "绝世": 0.7,
                },
                sentence_patterns=["短句连击", "三段式递进", "感叹收尾"],
                forbidden_patterns=["也许", "大概", "可能", "似乎"],
                example_text="一拳！\n天地变色！\n那一拳轰出，空间都在颤抖。没有人能挡住这一拳。没有人！",
            ),
            StyleModule(
                module_id="style_suspense",
                name="悬疑冷峻",
                category=StyleCategory.SUSPENSE,
                description="冷静克制，层层递进，氛围压抑，适合悬疑/推理题材",
                system_prompt="""你是一位悬疑推理作家。请以悬疑冷峻风格写作：
- 冷静克制的叙述语调
- 细节描写精准，每个细节都可能是线索
- 信息有节奏地释放，层层剥茧
- 氛围营造压抑紧张
- 对话简短有力，话中有话""",
                writing_rules=[
                    "叙述语调冷静客观，不带情绪",
                    "细节描写精准，环境/物品/动作都要具体",
                    "每段释放一个新信息或加深一个疑问",
                    "对话简短，每句不超过15字",
                    "善用环境烘托心理，不直接写情绪",
                ],
                vocabulary_bias={
                    "沉默": 0.8, "凝视": 0.7, "阴影": 0.8, "冰冷": 0.7,
                    "寂静": 0.8, "凝视": 0.7, "黑暗": 0.7, "压抑": 0.8,
                    "诡异": 0.7, "寒意": 0.7, "死寂": 0.8, "阴冷": 0.7,
                },
                sentence_patterns=["短句为主", "细节堆叠", "留白结尾"],
                forbidden_patterns=["显然", "明显", "毫无疑问"],
                example_text="他推开门。\n房间里很暗。窗帘拉得严严实实，只有一缕光从缝隙中挤进来，落在地板中央。那里什么都没有。但灰尘的分布不对。",
            ),
            StyleModule(
                module_id="style_romance",
                name="言情细腻",
                category=StyleCategory.ROMANCE,
                description="情感丰富，心理描写深入，温柔缱绻，适合言情/都市题材",
                system_prompt="""你是一位言情小说作家。请以言情细腻风格写作：
- 大量心理描写和内心独白
- 情感变化细腻，层层递进
- 对话温柔含蓄，言外之意丰富
- 细节描写侧重感官和情绪
- 节奏舒缓，给情感发酵空间""",
                writing_rules=[
                    "心理描写占比40%以上",
                    "情感变化要有层次，不能突兀",
                    "对话要有言外之意，每句都有潜台词",
                    "善用比喻写情感，如'心像被揉碎的玫瑰'",
                    "场景描写服务于情感，景语皆情语",
                ],
                vocabulary_bias={
                    "温柔": 0.9, "心动": 0.8, "思念": 0.8, "温暖": 0.7,
                    "柔软": 0.8, "甜蜜": 0.7, "心疼": 0.8, "依恋": 0.7,
                    "悸动": 0.8, "缱绻": 0.7, "缠绵": 0.7, "眷恋": 0.7,
                },
                sentence_patterns=["长句铺陈", "内心独白", "比喻收尾"],
                forbidden_patterns=["干就完了", "直接拿下"],
                example_text="她看着他离去的背影，心里某个角落悄悄塌陷了。那种感觉很奇怪，像春天的第一场雨，来得无声无息，却让整颗心都湿润了。",
            ),
            StyleModule(
                module_id="style_fantasy",
                name="玄幻磅礴",
                category=StyleCategory.FANTASY,
                description="气势恢宏，想象力丰富，设定宏大，适合玄幻/仙侠题材",
                system_prompt="""你是一位玄幻小说作家。请以玄幻磅礴风格写作：
- 世界观宏大，设定新奇
- 战斗场面气势恢宏
- 修炼体系清晰，等级分明
- 语言要有史诗感
- 善用夸张和对比突出力量差距""",
                writing_rules=[
                    "世界观设定要新奇且有内在逻辑",
                    "战斗描写要有层次感，从试探到全力",
                    "力量体系要清晰，每次突破都要有仪式感",
                    "场景描写要宏大，善用空间尺度对比",
                    "对话要有宗师风范或少年意气",
                ],
                vocabulary_bias={
                    "天地": 0.9, "大道": 0.8, "苍穹": 0.9, "万古": 0.8,
                    "永恒": 0.7, "混沌": 0.8, "法则": 0.7, "领域": 0.7,
                    "镇压": 0.8, "横扫": 0.8, "诸天": 0.7, "寰宇": 0.7,
                },
                sentence_patterns=["宏大开场", "力量递进", "史诗收尾"],
                forbidden_patterns=["小打小闹", "差不多"],
                example_text="那一掌拍下，天地为之色变。万里云海翻涌，雷霆万钧之力自九天之上倾泻而下，仿佛要将整片大陆都拍入地底。",
            ),
            StyleModule(
                module_id="style_humor",
                name="幽默诙谐",
                category=StyleCategory.HUMOR,
                description="轻松有趣，吐槽犀利，节奏明快，适合轻小说/搞笑题材",
                system_prompt="""你是一位幽默作家。请以幽默诙谐风格写作：
- 吐槽犀利，反转出人意料
- 对话生动有趣，充满机锋
- 善用夸张和反差制造笑点
- 节奏明快，包袱密集
- 叙事者语气轻松，像朋友聊天""",
                writing_rules=[
                    "每段至少一个笑点或反转",
                    "对话要有机锋，你来我往",
                    "善用反差：严肃场景+搞笑反应",
                    "叙事者可以打破第四面墙吐槽",
                    "节奏要快，包袱要密，不拖泥带水",
                ],
                vocabulary_bias={
                    "离谱": 0.8, "绝了": 0.7, "好家伙": 0.7, "没想到": 0.7,
                    "笑死": 0.7, "翻车": 0.7, "打脸": 0.8, "真香": 0.7,
                    "社死": 0.7, "破防": 0.7, "摆烂": 0.6, "躺平": 0.6,
                },
                sentence_patterns=["铺垫+反转", "吐槽+打脸", "夸张+真相"],
                forbidden_patterns=[],
                example_text="我，青云宗第一天才，今天被一只鸡追了三条街。\n说出去谁信？我自己都不信。但那只鸡——它真的会武功！",
            ),
            StyleModule(
                module_id="style_realistic",
                name="现实主义",
                category=StyleCategory.REALISTIC,
                description="贴近生活，细节真实，社会洞察，适合严肃文学/乡土题材",
                system_prompt="""你是一位现实主义作家。请以现实主义风格写作：
- 细节真实可信，源于生活观察
- 人物塑造立体，有好有坏有灰度
- 社会洞察深刻，反映时代问题
- 语言朴实有力，不追求华丽
- 情感克制，用事实说话""",
                writing_rules=[
                    "细节必须真实，不能凭空想象",
                    "人物要有缺点，不能完美",
                    "社会背景要准确，反映真实矛盾",
                    "语言朴实，避免华丽辞藻",
                    "情感通过行为和细节表达，不直接抒情",
                ],
                vocabulary_bias={
                    "生活": 0.7, "现实": 0.7, "平凡": 0.7, "真实": 0.7,
                    "艰辛": 0.6, "挣扎": 0.7, "无奈": 0.6, "坚持": 0.6,
                    "希望": 0.6, "改变": 0.6, "命运": 0.7, "时代": 0.7,
                },
                sentence_patterns=["白描叙事", "细节堆叠", "留白结尾"],
                forbidden_patterns=["天选之子", "一夜暴富"],
                example_text="老张在工厂干了二十年。每天六点起床，骑四十分钟自行车，到车间正好七点半。他从来没迟到过。今天也是。",
            ),
            StyleModule(
                module_id="style_poetic",
                name="诗意朦胧",
                category=StyleCategory.POETIC,
                description="意境优美，留白丰富，含蓄隽永，适合散文/文艺小说",
                system_prompt="""你是一位富有诗意的作家。请以诗意朦胧风格写作：
- 意境优先，故事服务于意境
- 大量留白，让读者自己填补
- 语言如诗，有韵律和节奏
- 善用通感和意象
- 情感含蓄，不直接表达""",
                writing_rules=[
                    "意境优先于情节",
                    "留白至少30%，不写满",
                    "语言要有韵律感，可朗读检验",
                    "善用通感：颜色有温度，声音有形状",
                    "情感通过意象表达，如'雨打在心上'",
                ],
                vocabulary_bias={
                    "月光": 0.8, "微风": 0.7, "细雨": 0.8, "黄昏": 0.7,
                    "落叶": 0.7, "花开": 0.7, "流水": 0.7, "浮云": 0.7,
                    "梦境": 0.8, "回忆": 0.7, "远方": 0.7, "时光": 0.7,
                },
                sentence_patterns=["意象开场", "留白过渡", "余韵收尾"],
                forbidden_patterns=["然后", "接着", "之后"],
                example_text="雨落在青石板上。\n一滴，又一滴。\n她站在巷口，撑着一把油纸伞。伞下的阴影遮住了半张脸，只露出一双眼睛——像深秋的湖水。",
            ),
        ]

        for module in builtins:
            self.modules[module.module_id] = module

        self.active_module = self.modules.get("style_classical")
        self.save()
