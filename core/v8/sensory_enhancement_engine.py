#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS V8.5 感官描写增强引擎
参考Sudowrite的Describe功能: 五感(视/听/嗅/触/味/动觉)扩写

核心能力:
- 多维度感官描写扩展
- 场景类型智能匹配
- 情感渲染增强
- 氛围营造
"""

import os
import json
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SensoryDimension(Enum):
    VISUAL = "visual"
    AUDITORY = "auditory"
    OLFACTORY = "olfactory"
    TACTILE = "tactile"
    GUSTATORY = "gustatory"
    KINESTHETIC = "kinesthetic"


@dataclass
class SensoryEnhancement:
    """感官增强配置"""
    dimension: SensoryDimension
    keywords: List[str]
    description_template: str
    intensity: float = 0.5


class SensoryEnhancementEngine:
    """感官描写增强引擎"""

    def __init__(self):
        self.enhancement_lib = self._load_enhancement_library()
        self.scene_templates = self._load_scene_templates()

    def _load_enhancement_library(self) -> Dict[str, Dict]:
        return {
            "visual": {
                "keywords": ["光", "色", "形", "影", "景", "象", "视", "看", "观", "睹"],
                "descriptions": {
                    "bright": ["光芒万丈", "金光灿烂", "耀眼夺目", "熠熠生辉", "光彩照人"],
                    "dark": ["昏暗阴沉", "漆黑一片", "暗无天日", "幽暗深邃", "黑幕降临"],
                    "colorful": ["五彩斑斓", "绚丽多彩", "万紫千红", "色彩缤纷", "流光溢彩"],
                    "clear": ["清晰可见", "一清二楚", "明镜止水", "澄澈透明", "历历在目"]
                }
            },
            "auditory": {
                "keywords": ["声", "音", "响", "听", "闻", "鸣", "唱", "语", "话", "音"],
                "descriptions": {
                    "loud": ["震耳欲聋", "响彻云霄", "惊天动地", "震天动地", "轰鸣不止"],
                    "quiet": ["鸦雀无声", "寂静无声", "万籁俱寂", "悄然无声", "静若处子"],
                    "melodic": ["悠扬动听", "婉转悠扬", "余音绕梁", "娓娓动听", "悦耳动听"],
                    "harsh": ["刺耳尖锐", "聒噪刺耳", "喧嚣嘈杂", "噪声震耳", "杂乱无章"]
                }
            },
            "olfactory": {
                "keywords": ["香", "臭", "味", "嗅", "芳", "腥", "膻", "腐", "新", "清"],
                "descriptions": {
                    "fragrant": ["芳香四溢", "香气扑鼻", "芬芳馥郁", "沁人心脾", "芳香怡人"],
                    "foul": ["臭气熏天", "腥臭扑鼻", "腐臭难闻", "令人作呕", "污浊腥臭"],
                    "fresh": ["清新怡人", "清爽新鲜", "空气清新", "淡雅清香", "心旷神怡"],
                    "heavy": ["浓郁厚重", "气味浓烈", "味道刺鼻", "厚重沉闷", "浊气上扬"]
                }
            },
            "tactile": {
                "keywords": ["触", "感", "温", "冷", "热", "凉", "软", "硬", "粗", "滑", "痛", "痒"],
                "descriptions": {
                    "cold": ["冰冷刺骨", "寒气逼人", "冰凉彻骨", "冻彻心扉", "寒冷刺骨"],
                    "hot": ["滚烫灼热", "热气腾腾", "酷热难耐", "火热灸人", "汗流浃背"],
                    "soft": ["柔软舒适", "轻柔绵软", "丝滑柔顺", "温软如玉", "软绵绵的"],
                    "hard": ["坚硬如铁", "硬邦邦", "坚不可摧", "牢固结实", "钢铁般坚硬"]
                }
            },
            "gustatory": {
                "keywords": ["味", "甜", "苦", "酸", "辣", "咸", "鲜", "香", "淡", "浓"],
                "descriptions": {
                    "sweet": ["甘甜可口", "甜蜜诱人", "甜入心扉", "蜜糖般甘甜", "香甜四溢"],
                    "bitter": ["苦涩难当", "苦不堪言", "苦涩如胆", "辛酸苦涩", "苦楚滋味"],
                    "spicy": ["辛辣刺激", "辣味十足", "麻辣鲜香", "辣到冒火", "火热刺激"],
                    "delicious": ["美味可口", "鲜嫩多汁", "香鲜无比", "味道鲜美", "口感极佳"]
                }
            },
            "kinesthetic": {
                "keywords": ["动", "静", "速", "力", "量", "势", "动", "快", "慢", "稳", "飘", "落"],
                "descriptions": {
                    "fast": ["风驰电掣", "快如闪电", "疾如流星", "迅速如风", "迅捷无比"],
                    "slow": ["缓慢悠长", "悠然自得", "慢条斯理", "从容不迫", "舒缓绵长"],
                    "powerful": ["力大无穷", "势不可挡", "力量磅礴", "威力惊人", "震撼人心"],
                    "gentle": ["轻柔细腻", "温和柔美", "轻柔婉转", "温柔体贴", "柔和细腻"]
                }
            }
        }

    def _load_scene_templates(self) -> Dict[str, Dict]:
        return {
            "battle": {
                "name": "战斗场景",
                "primary_senses": ["visual", "kinesthetic", "auditory"],
                "secondary_senses": ["tactile"],
                "emotions": ["紧张", "激烈", "热血", "危险"],
                "templates": {
                    "visual": "刀光剑影交错，光芒如闪电划破长空",
                    "auditory": "金铁交鸣声震耳欲聋，杀伐之音响彻云霄",
                    "kinesthetic": "速度快如闪电，力量势不可挡",
                    "tactile": "感受到敌人的杀意和兵器的冰冷"
                }
            },
            "romance": {
                "name": "爱情场景",
                "primary_senses": ["visual", "tactile", "gustatory"],
                "secondary_senses": ["olfactory", "auditory"],
                "emotions": ["甜蜜", "温馨", "心动", "羞涩"],
                "templates": {
                    "visual": "月光如水，洒落在她温柔的脸庞上",
                    "tactile": "指尖触碰的瞬间，仿佛有电流穿过",
                    "gustatory": "呼吸间是对方身上淡淡的清香",
                    "olfactory": "空气中弥漫着甜蜜温馨的气息"
                }
            },
            "horror": {
                "name": "恐怖场景",
                "primary_senses": ["visual", "auditory", "olfactory"],
                "secondary_senses": ["tactile"],
                "emotions": ["恐惧", "紧张", "不安", "毛骨悚然"],
                "templates": {
                    "visual": "黑暗中仿佛有什么东西在蠢蠢欲动",
                    "auditory": "诡异的声响在耳边回荡，令人胆寒",
                    "olfactory": "空气中弥漫着腐朽和死亡的气息",
                    "tactile": "冰冷的感觉从脊背蔓延全身"
                }
            },
            "daily": {
                "name": "日常场景",
                "primary_senses": ["visual", "auditory"],
                "secondary_senses": ["gustatory", "tactile"],
                "emotions": ["平静", "温馨", "悠闲", "舒适"],
                "templates": {
                    "visual": "阳光温暖地洒落，岁月静好",
                    "auditory": "鸟鸣声清脆悦耳，生活安宁祥和",
                    "gustatory": "茶香袅袅，味道清香甘醇",
                    "tactile": "微风拂过脸颊，温柔舒适"
                }
            },
            "fantasy": {
                "name": "玄幻场景",
                "primary_senses": ["visual", "kinesthetic"],
                "secondary_senses": ["tactile", "auditory"],
                "emotions": ["震撼", "壮观", "神秘", "超凡"],
                "templates": {
                    "visual": "灵光璀璨，道韵流转，天地灵气汇聚",
                    "kinesthetic": "灵力汹涌澎湃，如浩瀚星河",
                    "tactile": "能量波动震动着每一寸肌肤",
                    "auditory": "大道之音在脑海中回响"
                }
            }
        }

    def enhance_text(self, text: str, scene_type: str = "daily",
                    dimensions: List[str] = None,
                    intensity: float = 0.7) -> str:
        """增强文本的感官描写"""
        if dimensions is None:
            template = self.scene_templates.get(scene_type, self.scene_templates["daily"])
            dimensions = template["primary_senses"]

        enhanced_parts = []

        for dim_str in dimensions:
            try:
                dim = SensoryDimension(dim_str)
            except ValueError:
                continue

            enhancement = self._generate_enhancement(dim, text, intensity)
            if enhancement:
                enhanced_parts.append(enhancement)

        if enhanced_parts:
            return text + "\n\n" + "\n".join(enhanced_parts)
        return text

    def _generate_enhancement(self, dimension: SensoryDimension,
                             context: str, intensity: float) -> str:
        """生成指定维度的增强描写"""
        dim_key = dimension.value

        if dim_key not in self.enhancement_lib:
            return ""

        lib = self.enhancement_lib[dim_key]

        relevant_keywords = []
        for kw in lib["keywords"]:
            if kw in context:
                relevant_keywords.append(kw)

        if not relevant_keywords:
            relevant_keywords = lib["keywords"][:3]

        descriptions = []
        for desc_list in lib["descriptions"].values():
            descriptions.extend(desc_list)

        import random
        selected_descs = random.sample(descriptions, min(3, len(descriptions)))

        sense_names = {
            "visual": "【视觉】",
            "auditory": "【听觉】",
            "olfactory": "【嗅觉】",
            "tactile": "【触觉】",
            "gustatory": "【味觉】",
            "kinesthetic": "【动觉】"
        }

        header = sense_names.get(dim_key, f"【{dim_key}】")

        return f"{header} {'，'.join(selected_descs[:2])}"

    def generate_scene_description(self, scene_type: str,
                                   context: str = "") -> Dict[str, str]:
        """生成完整场景描述"""
        template = self.scene_templates.get(scene_type, self.scene_templates["daily"])

        descriptions = {}

        for dim_str in template["primary_senses"]:
            try:
                dim = SensoryDimension(dim_str)
            except ValueError:
                continue

            if context:
                desc = self._generate_enhancement(dim, context, 0.8)
            else:
                desc = self._generate_enhancement(dim, template["name"], 0.8)

            descriptions[dim_str] = desc

        return {
            "scene_type": template["name"],
            "descriptions": descriptions,
            "emotions": template["emotions"],
            "full_description": "\n".join(descriptions.values())
        }

    def batch_enhance_dialogue(self, dialogues: List[Dict[str, str]],
                               scene_type: str = "daily") -> List[Dict[str, str]]:
        """批量增强对话描写"""
        enhanced = []

        for dialogue in dialogues:
            speaker = dialogue.get("speaker", "")
            content = dialogue.get("content", "")

            enhanced_content = self.enhance_text(content, scene_type)
            enhanced.append({
                "speaker": speaker,
                "content": enhanced_content
            })

        return enhanced

    def create_sensory_prompt(self, scene_type: str, emotion: str = None) -> str:
        """创建感官描写提示词"""
        template = self.scene_templates.get(scene_type, self.scene_templates["daily"])

        prompt_parts = [f"场景类型: {template['name']}"]

        if emotion:
            prompt_parts.append(f"情感基调: {emotion}")
        else:
            prompt_parts.append(f"情感基调: {', '.join(template['emotions'][:2])}")

        prompt_parts.append("描写要求:")
        prompt_parts.append("- 从视觉、听觉、嗅觉、触觉、味觉、动觉多维度展开")
        prompt_parts.append("- 使用具体形象的感官词汇")
        prompt_parts.append("- 增强读者的沉浸感和代入感")

        return "\n".join(prompt_parts)

    def get_available_dimensions(self) -> List[str]:
        """获取可用的感官维度"""
        return [dim.value for dim in SensoryDimension]

    def get_scene_types(self) -> List[str]:
        """获取可用的场景类型"""
        return list(self.scene_templates.keys())


def main():
    print("="*60)
    print("✨ NWACS V8.5 感官描写增强引擎")
    print("="*60)

    engine = SensoryEnhancementEngine()

    print("\n可用感官维度:")
    for dim in engine.get_available_dimensions():
        print(f"  • {dim}")

    print("\n可用场景类型:")
    for scene in engine.get_scene_types():
        print(f"  • {scene}")

    print("\n" + "-"*60)
    print("示例：玄幻战斗场景增强")
    print("-"*60)

    sample_text = "叶青云催动灵力，一道剑光斩向敌人"

    enhanced = engine.enhance_text(sample_text, scene_type="fantasy")
    print(f"\n原文: {sample_text}")
    print(f"\n增强后:\n{enhanced}")

    print("\n" + "-"*60)
    print("生成场景描述")
    print("-"*60)

    scene_desc = engine.generate_scene_description("romance", "月光下的相遇")
    print(f"\n场景类型: {scene_desc['scene_type']}")
    print(f"情感: {', '.join(scene_desc['emotions'])}")
    print(f"\n描写:\n{scene_desc['full_description']}")

    print("\n" + "="*60)
    print("✅ 感官描写增强引擎就绪")
    print("="*60)


if __name__ == "__main__":
    main()