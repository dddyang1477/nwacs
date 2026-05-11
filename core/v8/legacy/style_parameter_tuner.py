#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
风格参数精细调节器 (Style Parameter Tuner)

对标 FeelFish 的"古风浓度""悬疑感强度"等风格参数滑块调节。
提供10+维度的风格参数精细控制，让创作者像调音台一样精确控制文风。

核心能力:
- 10维风格参数: 古风浓度/悬疑感/热血度/甜度/黑暗度/幽默感/文学性/口语化/节奏速度/描写密度
- 参数预设: 内置各题材最佳参数组合
- 参数混合: 支持多风格融合(如"古风+悬疑")
- 参数转提示词: 将参数自动转换为AI提示词指令
- 参数对比: 对比不同参数组合的生成效果
"""

import json
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from enum import Enum


class StyleDimension(Enum):
    CLASSICAL = "classical"           # 古风浓度 0-100
    SUSPENSE = "suspense"             # 悬疑感 0-100
    PASSION = "passion"               # 热血度 0-100
    ROMANCE = "romance"               # 甜度 0-100
    DARKNESS = "darkness"             # 黑暗度 0-100
    HUMOR = "humor"                   # 幽默感 0-100
    LITERARY = "literary"             # 文学性 0-100
    COLLOQUIAL = "colloquial"         # 口语化 0-100
    PACE = "pace"                     # 节奏速度 0-100
    DESCRIPTION = "description"       # 描写密度 0-100
    DIALOGUE_RATIO = "dialogue_ratio" # 对话比例 0-100
    SENTENCE_VARIETY = "sentence_variety"  # 句法变化度 0-100


@dataclass
class StyleProfile:
    name: str
    description: str
    parameters: Dict[str, int]    # {dimension_name: value 0-100}
    tags: List[str] = field(default_factory=list)


STYLE_PRESETS: Dict[str, StyleProfile] = {
    "古风仙侠": StyleProfile(
        name="古风仙侠",
        description="典雅古朴的仙侠文风，适合古典仙侠、修真题材",
        parameters={
            "classical": 85, "suspense": 40, "passion": 60,
            "romance": 30, "darkness": 35, "humor": 15,
            "literary": 75, "colloquial": 10, "pace": 50,
            "description": 70, "dialogue_ratio": 35, "sentence_variety": 60,
        },
        tags=["仙侠", "修真", "古典", "东方玄幻"],
    ),
    "热血爽文": StyleProfile(
        name="热血爽文",
        description="快节奏高爽点的网文风格，适合玄幻、都市爽文",
        parameters={
            "classical": 20, "suspense": 50, "passion": 90,
            "romance": 20, "darkness": 30, "humor": 40,
            "literary": 25, "colloquial": 65, "pace": 85,
            "description": 40, "dialogue_ratio": 50, "sentence_variety": 55,
        },
        tags=["玄幻", "都市", "爽文", "升级流"],
    ),
    "悬疑推理": StyleProfile(
        name="悬疑推理",
        description="紧张压抑的悬疑氛围，适合推理、悬疑、惊悚题材",
        parameters={
            "classical": 15, "suspense": 90, "passion": 30,
            "romance": 10, "darkness": 70, "humor": 10,
            "literary": 50, "colloquial": 35, "pace": 60,
            "description": 65, "dialogue_ratio": 45, "sentence_variety": 50,
        },
        tags=["悬疑", "推理", "惊悚", "犯罪"],
    ),
    "甜宠言情": StyleProfile(
        name="甜宠言情",
        description="温暖甜蜜的言情风格，适合现代言情、甜宠文",
        parameters={
            "classical": 10, "suspense": 20, "passion": 25,
            "romance": 90, "darkness": 5, "humor": 50,
            "literary": 35, "colloquial": 60, "pace": 40,
            "description": 55, "dialogue_ratio": 65, "sentence_variety": 40,
        },
        tags=["言情", "甜宠", "现代", "恋爱"],
    ),
    "黑暗史诗": StyleProfile(
        name="黑暗史诗",
        description="沉重宏大的黑暗风格，适合黑暗奇幻、末世、克苏鲁",
        parameters={
            "classical": 40, "suspense": 75, "passion": 50,
            "romance": 10, "darkness": 90, "humor": 5,
            "literary": 70, "colloquial": 15, "pace": 45,
            "description": 75, "dialogue_ratio": 30, "sentence_variety": 55,
        },
        tags=["黑暗", "奇幻", "末世", "克苏鲁", "史诗"],
    ),
    "轻松搞笑": StyleProfile(
        name="轻松搞笑",
        description="轻松幽默的搞笑风格，适合搞笑、日常、吐槽流",
        parameters={
            "classical": 10, "suspense": 15, "passion": 30,
            "romance": 25, "darkness": 5, "humor": 90,
            "literary": 15, "colloquial": 85, "pace": 65,
            "description": 30, "dialogue_ratio": 60, "sentence_variety": 70,
        },
        tags=["搞笑", "日常", "吐槽", "轻松"],
    ),
    "文学性写作": StyleProfile(
        name="文学性写作",
        description="注重文学性和艺术表达的纯文学风格",
        parameters={
            "classical": 50, "suspense": 35, "passion": 30,
            "romance": 40, "darkness": 40, "humor": 20,
            "literary": 90, "colloquial": 15, "pace": 30,
            "description": 80, "dialogue_ratio": 30, "sentence_variety": 80,
        },
        tags=["纯文学", "严肃文学", "文艺", "实验"],
    ),
    "科幻硬核": StyleProfile(
        name="科幻硬核",
        description="理性克制的科幻风格，适合硬科幻、赛博朋克",
        parameters={
            "classical": 10, "suspense": 55, "passion": 35,
            "romance": 10, "darkness": 50, "humor": 15,
            "literary": 45, "colloquial": 30, "pace": 50,
            "description": 55, "dialogue_ratio": 40, "sentence_variety": 45,
        },
        tags=["科幻", "赛博朋克", "硬科幻", "未来"],
    ),
}


class StyleParameterTuner:
    """风格参数精细调节器"""

    def __init__(self):
        self.presets = dict(STYLE_PRESETS)
        self.custom_profiles: Dict[str, StyleProfile] = {}
        self.active_profile: Optional[StyleProfile] = None

    def list_presets(self) -> List[Dict]:
        """列出所有预设风格"""
        return [
            {
                "name": p.name,
                "description": p.description,
                "tags": p.tags,
                "parameter_count": len(p.parameters),
            }
            for p in self.presets.values()
        ]

    def get_preset(self, name: str) -> Optional[StyleProfile]:
        """获取预设风格"""
        return self.presets.get(name)

    def activate_preset(self, name: str) -> bool:
        """激活预设风格"""
        preset = self.presets.get(name)
        if preset:
            self.active_profile = preset
            return True
        return False

    def create_custom(self, name: str, description: str,
                      parameters: Dict[str, int],
                      tags: List[str] = None) -> StyleProfile:
        """创建自定义风格"""
        validated = {}
        for dim in StyleDimension:
            value = parameters.get(dim.value, 50)
            validated[dim.value] = max(0, min(100, int(value)))

        profile = StyleProfile(
            name=name,
            description=description,
            parameters=validated,
            tags=tags or [],
        )
        self.custom_profiles[name] = profile
        return profile

    def blend(self, profile_a: str, profile_b: str,
              ratio: float = 0.5, blend_name: str = None) -> StyleProfile:
        """
        混合两种风格

        Args:
            profile_a: 风格A名称
            profile_b: 风格B名称
            ratio: 混合比例(0=纯A, 1=纯B)
            blend_name: 混合风格名称
        """
        a = self.presets.get(profile_a) or self.custom_profiles.get(profile_a)
        b = self.presets.get(profile_b) or self.custom_profiles.get(profile_b)

        if not a or not b:
            raise ValueError(f"风格不存在: {profile_a if not a else profile_b}")

        ratio = max(0.0, min(1.0, ratio))
        blended_params = {}

        for dim in StyleDimension:
            val_a = a.parameters.get(dim.value, 50)
            val_b = b.parameters.get(dim.value, 50)
            blended_params[dim.value] = int(val_a * (1 - ratio) + val_b * ratio)

        name = blend_name or f"{a.name}+{b.name}({int(ratio*100)}%)"
        profile = StyleProfile(
            name=name,
            description=f"混合风格: {a.name} {int((1-ratio)*100)}% + {b.name} {int(ratio*100)}%",
            parameters=blended_params,
            tags=list(set(a.tags + b.tags)),
        )
        self.custom_profiles[name] = profile
        return profile

    def adjust(self, profile_name: str,
               adjustments: Dict[str, int]) -> StyleProfile:
        """
        微调风格参数

        Args:
            profile_name: 风格名称
            adjustments: {dimension: delta} 调整量(-100到+100)
        """
        source = self.presets.get(profile_name) or self.custom_profiles.get(profile_name)
        if not source:
            raise ValueError(f"风格不存在: {profile_name}")

        new_params = dict(source.parameters)
        for dim, delta in adjustments.items():
            if dim in new_params:
                new_params[dim] = max(0, min(100, new_params[dim] + delta))

        new_name = f"{profile_name}(微调)"
        profile = StyleProfile(
            name=new_name,
            description=f"基于 {profile_name} 微调",
            parameters=new_params,
            tags=list(source.tags),
        )
        self.custom_profiles[new_name] = profile
        return profile

    def to_prompt_instructions(self, profile: StyleProfile = None) -> str:
        """
        将风格参数转换为AI提示词指令

        对标 FeelFish 的"古风浓度""悬疑感强度"等滑块自动转换为提示词。
        """
        profile = profile or self.active_profile
        if not profile:
            return ""

        params = profile.parameters
        instructions = []

        classical = params.get("classical", 50)
        if classical >= 70:
            instructions.append(
                f"使用典雅的古风文笔，多用四字成语和文言句式，"
                f"避免现代词汇。古风浓度: {classical}/100"
            )
        elif classical >= 40:
            instructions.append(
                f"适当融入古风元素，在对话和描写中使用部分典雅词汇。"
                f"古风浓度: {classical}/100"
            )
        elif classical <= 20:
            instructions.append("使用现代白话文写作，避免文言词汇。")

        suspense = params.get("suspense", 50)
        if suspense >= 70:
            instructions.append(
                f"营造强烈的悬疑氛围：多用暗示和留白，控制信息释放节奏，"
                f"让读者始终保持好奇。悬疑感: {suspense}/100"
            )
        elif suspense >= 40:
            instructions.append(
                f"适当加入悬疑元素，在关键情节设置悬念。悬疑感: {suspense}/100"
            )

        passion = params.get("passion", 50)
        if passion >= 70:
            instructions.append(
                f"保持高昂的热血基调：战斗描写要有冲击力，"
                f"关键时刻要有燃点。热血度: {passion}/100"
            )

        romance = params.get("romance", 50)
        if romance >= 70:
            instructions.append(
                f"突出情感线的甜度：增加细腻的心理描写和甜蜜互动，"
                f"让读者感受到角色之间的化学反应。甜度: {romance}/100"
            )

        darkness = params.get("darkness", 50)
        if darkness >= 70:
            instructions.append(
                f"采用黑暗沉重的基调：描写人性的阴暗面，"
                f"氛围压抑但不绝望。黑暗度: {darkness}/100"
            )
        elif darkness <= 20:
            instructions.append("保持轻松明亮的基调，避免过于沉重的描写。")

        humor = params.get("humor", 50)
        if humor >= 70:
            instructions.append(
                f"加入大量幽默元素：吐槽、反差萌、冷幽默，"
                f"让读者会心一笑。幽默感: {humor}/100"
            )

        literary = params.get("literary", 50)
        if literary >= 70:
            instructions.append(
                f"注重文学性表达：使用比喻、象征等修辞手法，"
                f"追求语言的审美价值。文学性: {literary}/100"
            )

        colloquial = params.get("colloquial", 50)
        if colloquial >= 70:
            instructions.append(
                f"使用高度口语化的表达：对话要像真人说话，"
                f"加入语气词、口头禅、不完整句。口语化: {colloquial}/100"
            )

        pace = params.get("pace", 50)
        if pace >= 70:
            instructions.append(
                f"保持快节奏叙事：减少冗长描写，用短句和动作推进情节。"
                f"节奏速度: {pace}/100"
            )
        elif pace <= 30:
            instructions.append(
                f"采用舒缓的叙事节奏：充分展开细节描写和心理活动。"
                f"节奏速度: {pace}/100"
            )

        description = params.get("description", 50)
        if description >= 70:
            instructions.append(
                f"增加描写密度：环境、人物、氛围都要细致刻画，"
                f"每个场景至少包含2种感官细节。描写密度: {description}/100"
            )
        elif description <= 30:
            instructions.append(
                f"精简描写：用最少的笔墨勾勒场景，重点放在情节推进。"
                f"描写密度: {description}/100"
            )

        dialogue_ratio = params.get("dialogue_ratio", 50)
        if dialogue_ratio >= 70:
            instructions.append(
                f"提高对话比例：用对话推进情节，减少叙述性文字。"
                f"对话比例: {dialogue_ratio}/100"
            )

        sentence_variety = params.get("sentence_variety", 50)
        if sentence_variety >= 70:
            instructions.append(
                f"大幅变化句法结构：长短句剧烈交替，"
                f"避免连续3句以上相同句式。句法变化度: {sentence_variety}/100"
            )

        return "\n".join(instructions)

    def to_system_prompt(self, profile: StyleProfile = None) -> str:
        """生成完整的系统提示词(含风格参数)"""
        profile = profile or self.active_profile
        if not profile:
            return ""

        instructions = self.to_prompt_instructions(profile)

        return f"""【写作风格配置: {profile.name}】
{profile.description}

{instructions}

请严格按照以上风格参数进行创作。"""

    def compare_profiles(self, profile_a: str, profile_b: str) -> Dict[str, Any]:
        """对比两个风格配置的差异"""
        a = self.presets.get(profile_a) or self.custom_profiles.get(profile_a)
        b = self.presets.get(profile_b) or self.custom_profiles.get(profile_b)

        if not a or not b:
            return {"error": "风格不存在"}

        differences = {}
        for dim in StyleDimension:
            val_a = a.parameters.get(dim.value, 50)
            val_b = b.parameters.get(dim.value, 50)
            diff = val_b - val_a
            if abs(diff) >= 10:
                differences[dim.value] = {
                    "dimension": dim.value,
                    "profile_a": val_a,
                    "profile_b": val_b,
                    "difference": diff,
                    "direction": "↑" if diff > 0 else "↓",
                }

        return {
            "profile_a": a.name,
            "profile_b": b.name,
            "differences": differences,
            "total_dimensions_changed": len(differences),
        }

    def export_profile(self, name: str) -> Optional[Dict]:
        """导出风格配置"""
        profile = self.presets.get(name) or self.custom_profiles.get(name)
        if not profile:
            return None

        return {
            "name": profile.name,
            "description": profile.description,
            "parameters": profile.parameters,
            "tags": profile.tags,
        }

    def import_profile(self, data: Dict) -> StyleProfile:
        """导入风格配置"""
        return self.create_custom(
            name=data.get("name", "导入风格"),
            description=data.get("description", ""),
            parameters=data.get("parameters", {}),
            tags=data.get("tags", []),
        )
