#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 角色语音注入系统 - CharacterVoiceInjector

对标 Sudowrite Character Voice Consistency / WebNovelAI Character Profile Management

核心能力：
1. 角色语音档案 - 为每个角色建立说话风格指纹
2. 生成时注入 - 在提示词中自动注入角色语音约束
3. 对话一致性 - 确保同一角色跨章节说话风格一致
4. 角色区分度 - 确保不同角色说话风格有明显差异
5. 场景感知 - 根据场景情绪调整角色语音强度

设计原则：
- 零API调用，纯本地规则引擎
- 与NovelMemoryManager角色档案联动
- 可配置的注入强度
"""

import json
import os
import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class SpeechRegister(Enum):
    FORMAL = "正式"
    CASUAL = "随意"
    ROUGH = "粗犷"
    ELEGANT = "文雅"
    COLD = "冷漠"
    WARM = "热情"
    SARCASTIC = "讽刺"
    NAIVE = "天真"
    WISE = "睿智"
    ARROGANT = "傲慢"
    HUMBLE = "谦卑"
    MYSTERIOUS = "神秘"


class EmotionTone(Enum):
    ANGRY = "愤怒"
    SAD = "悲伤"
    HAPPY = "高兴"
    FEARFUL = "恐惧"
    CALM = "平静"
    EXCITED = "激动"
    NERVOUS = "紧张"
    CONFIDENT = "自信"
    DESPERATE = "绝望"
    LOVING = "深情"


@dataclass
class CharacterVoiceProfile:
    name: str
    speech_register: SpeechRegister = SpeechRegister.CASUAL
    sentence_length: str = "medium"
    vocabulary_level: str = "common"
    catchphrases: List[str] = field(default_factory=list)
    filler_words: List[str] = field(default_factory=list)
    speech_quirks: List[str] = field(default_factory=list)
    taboo_words: List[str] = field(default_factory=list)
    dialogue_ratio: float = 0.5
    interruption_tendency: float = 0.3
    honorifics_usage: bool = True
    dialect_markers: List[str] = field(default_factory=list)
    emotional_range: List[EmotionTone] = field(default_factory=list)
    voice_description: str = ""


class CharacterVoiceInjector:
    """角色语音注入系统"""

    VOICE_TEMPLATES = {
        "冷酷大佬": {
            "speech_register": SpeechRegister.COLD,
            "sentence_length": "short",
            "vocabulary_level": "precise",
            "catchphrases": ["有意思", "滚", "找死"],
            "speech_quirks": ["话少但每句都有分量", "喜欢用反问", "从不解释"],
            "taboo_words": ["对不起", "求求你", "我怕"],
            "dialogue_ratio": 0.3,
            "interruption_tendency": 0.7,
            "voice_description": "说话简短有力，每句话不超过15个字，语气冰冷不带感情，偶尔用反问句施压",
        },
        "废柴逆袭": {
            "speech_register": SpeechRegister.CASUAL,
            "sentence_length": "medium",
            "vocabulary_level": "common",
            "catchphrases": ["三十年河东三十年河西", "莫欺少年穷"],
            "speech_quirks": ["前期说话犹豫带省略号", "后期说话果断有力", "对敌人放狠话"],
            "taboo_words": [],
            "dialogue_ratio": 0.5,
            "interruption_tendency": 0.2,
            "voice_description": "前期说话犹豫不决常用省略号，获得力量后变得果断，对敌人会放狠话",
        },
        "温润如玉": {
            "speech_register": SpeechRegister.ELEGANT,
            "sentence_length": "medium",
            "vocabulary_level": "refined",
            "catchphrases": ["无妨", "有我在", "慢慢来"],
            "speech_quirks": ["说话前会先微笑", "从不打断别人", "用词温和从不尖锐"],
            "taboo_words": ["滚", "去死", "废物"],
            "dialogue_ratio": 0.4,
            "interruption_tendency": 0.1,
            "voice_description": "说话温文尔雅，用词考究但不做作，总是先微笑再开口，从不打断别人",
        },
        "邪魅狂狷": {
            "speech_register": SpeechRegister.ARROGANT,
            "sentence_length": "varied",
            "vocabulary_level": "colorful",
            "catchphrases": ["女人，你逃不掉的", "有趣", "你以为呢"],
            "speech_quirks": ["喜欢用上扬的尾音", "说话时喜欢靠近对方", "经常用暧昧的双关语"],
            "taboo_words": [],
            "dialogue_ratio": 0.6,
            "interruption_tendency": 0.6,
            "voice_description": "说话张扬自信，喜欢用暧昧双关，尾音上扬，经常打断别人来主导对话",
        },
        "重生复仇": {
            "speech_register": SpeechRegister.COLD,
            "sentence_length": "medium",
            "vocabulary_level": "precise",
            "catchphrases": ["上辈子欠我的，这辈子还", "你以为我不知道吗"],
            "speech_quirks": ["说话暗藏机锋", "表面客气实则威胁", "偶尔流露出前世记忆的沧桑"],
            "taboo_words": [],
            "dialogue_ratio": 0.45,
            "interruption_tendency": 0.4,
            "voice_description": "表面客气但话里有话，偶尔流露出超越年龄的沧桑感，对仇人说话冰冷刺骨",
        },
        "天真少女": {
            "speech_register": SpeechRegister.NAIVE,
            "sentence_length": "short_to_medium",
            "vocabulary_level": "simple",
            "catchphrases": ["真的吗", "好厉害", "为什么"],
            "speech_quirks": ["喜欢用感叹词", "说话时眼睛会发光", "经常问为什么"],
            "taboo_words": [],
            "dialogue_ratio": 0.55,
            "interruption_tendency": 0.3,
            "voice_description": "说话天真烂漫，喜欢用感叹词，对什么都好奇，经常问为什么",
        },
        "睿智老者": {
            "speech_register": SpeechRegister.WISE,
            "sentence_length": "long",
            "vocabulary_level": "refined",
            "catchphrases": ["年轻人", "天机不可泄露", "一切皆有定数"],
            "speech_quirks": ["说话前会先叹气或沉默", "喜欢用比喻和典故", "话只说一半"],
            "taboo_words": [],
            "dialogue_ratio": 0.35,
            "interruption_tendency": 0.1,
            "voice_description": "说话慢条斯理，喜欢用比喻和典故，话只说一半让人琢磨，偶尔叹气",
        },
        "霸道总裁": {
            "speech_register": SpeechRegister.ARROGANT,
            "sentence_length": "short",
            "vocabulary_level": "precise",
            "catchphrases": ["我的人谁敢碰", "给你三秒钟", "这件事没得商量"],
            "speech_quirks": ["用命令句", "从不征求别人意见", "说话时眼神压迫"],
            "taboo_words": ["对不起", "请", "麻烦你"],
            "dialogue_ratio": 0.4,
            "interruption_tendency": 0.8,
            "voice_description": "说话霸道直接，用命令句，从不征求别人意见，气场强大",
        },
    }

    def __init__(self):
        self.profiles: Dict[str, CharacterVoiceProfile] = {}

    def create_profile(self, name: str, template: str = None,
                       custom: Dict = None) -> CharacterVoiceProfile:
        if template and template in self.VOICE_TEMPLATES:
            t = self.VOICE_TEMPLATES[template]
            profile = CharacterVoiceProfile(
                name=name,
                speech_register=t["speech_register"],
                sentence_length=t["sentence_length"],
                vocabulary_level=t["vocabulary_level"],
                catchphrases=list(t.get("catchphrases", [])),
                speech_quirks=list(t.get("speech_quirks", [])),
                taboo_words=list(t.get("taboo_words", [])),
                dialogue_ratio=t.get("dialogue_ratio", 0.5),
                interruption_tendency=t.get("interruption_tendency", 0.3),
                voice_description=t.get("voice_description", ""),
            )
        else:
            profile = CharacterVoiceProfile(name=name)
            if custom:
                for key, value in custom.items():
                    if hasattr(profile, key):
                        setattr(profile, key, value)

        self.profiles[name] = profile
        return profile

    def get_profile(self, name: str) -> Optional[CharacterVoiceProfile]:
        return self.profiles.get(name)

    def build_voice_constraint(self, name: str,
                                scene_emotion: EmotionTone = None) -> str:
        profile = self.profiles.get(name)
        if not profile:
            return ""

        parts = [f"【{name}的说话风格约束 - 必须严格遵守】"]

        parts.append(f"- 语域: {profile.speech_register.value}")
        parts.append(f"- 句长偏好: {profile.sentence_length}")

        if profile.catchphrases:
            parts.append(f"- 口头禅(可适当使用): {', '.join(profile.catchphrases)}")

        if profile.speech_quirks:
            parts.append(f"- 说话习惯: {'; '.join(profile.speech_quirks)}")

        if profile.taboo_words:
            parts.append(f"- 禁用词汇(绝对不能使用): {', '.join(profile.taboo_words)}")

        if profile.voice_description:
            parts.append(f"- 整体风格: {profile.voice_description}")

        if scene_emotion:
            emotion_modifiers = {
                EmotionTone.ANGRY: "句长缩短30%，语气更尖锐，可适当使用短促的句子",
                EmotionTone.SAD: "句长增加20%，语气低沉，可加入省略号和停顿",
                EmotionTone.EXCITED: "句长缩短，语速加快，可加入感叹号",
                EmotionTone.FEARFUL: "句长不稳定，语气颤抖，可加入重复和结巴",
                EmotionTone.CONFIDENT: "句长稳定，语气坚定，减少疑问句",
                EmotionTone.DESPERATE: "句长混乱，语气急促，可打破常规说话习惯",
            }
            modifier = emotion_modifiers.get(scene_emotion, "")
            if modifier:
                parts.append(f"- 当前情绪({scene_emotion.value})调整: {modifier}")

        return "\n".join(parts)

    def build_full_injection_prompt(self, active_characters: List[str],
                                     scene_emotion: EmotionTone = None,
                                     scene_context: str = "") -> str:
        if not active_characters:
            return ""

        parts = ["\n【角色语音一致性约束 - 以下规则必须在生成对话时严格遵守】\n"]

        for name in active_characters:
            constraint = self.build_voice_constraint(name, scene_emotion)
            if constraint:
                parts.append(constraint)
                parts.append("")

        parts.append("【重要提醒】")
        parts.append("- 每个角色的对话必须严格符合其说话风格约束")
        parts.append("- 不同角色的对话必须有明显区分度，读者仅凭说话方式就能分辨是谁在说话")
        parts.append("- 禁止所有角色用同一种方式说话")

        if scene_context:
            parts.append(f"\n【当前场景】{scene_context}")

        return "\n".join(parts)

    def check_dialogue_consistency(self, name: str, dialogue: str) -> Dict:
        profile = self.profiles.get(name)
        if not profile:
            return {"consistent": True, "issues": [], "score": 1.0}

        issues = []
        score = 1.0

        for word in profile.taboo_words:
            if word in dialogue:
                issues.append(f"使用了禁用词「{word}」")
                score -= 0.2

        sentences = re.split(r'[。！？]', dialogue)
        sentences = [s.strip() for s in sentences if s.strip()]

        if profile.sentence_length == "short":
            long_sentences = [s for s in sentences if len(s) > 20]
            if long_sentences:
                issues.append(f"有{len(long_sentences)}句超过20字，不符合短句风格")
                score -= 0.1 * min(len(long_sentences), 5)
        elif profile.sentence_length == "long":
            short_sentences = [s for s in sentences if len(s) < 8]
            if len(short_sentences) > len(sentences) * 0.5:
                issues.append("短句过多，不符合长句风格")
                score -= 0.15

        if profile.speech_register == SpeechRegister.FORMAL:
            casual_markers = ["呗", "嘛", "啦", "哦", "嗯", "哈"]
            found = [m for m in casual_markers if m in dialogue]
            if found:
                issues.append(f"使用了口语化标记: {found}")
                score -= 0.1

        if profile.speech_register == SpeechRegister.COLD:
            warm_markers = ["谢谢", "太好了", "真开心", "好感动"]
            found = [m for m in warm_markers if m in dialogue]
            if found:
                issues.append(f"冷漠角色使用了温暖表达: {found}")
                score -= 0.15

        score = max(0.0, score)

        return {
            "character": name,
            "consistent": len(issues) == 0,
            "issues": issues,
            "score": score,
            "dialogue_preview": dialogue[:100] + "..." if len(dialogue) > 100 else dialogue,
        }

    def get_character_distinction_report(self, char_names: List[str]) -> Dict:
        profiles = {}
        for name in char_names:
            p = self.profiles.get(name)
            if p:
                profiles[name] = p

        if len(profiles) < 2:
            return {"distinct": True, "score": 1.0, "issues": []}

        issues = []
        names = list(profiles.keys())

        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                p1 = profiles[names[i]]
                p2 = profiles[names[j]]

                similarities = []
                if p1.speech_register == p2.speech_register:
                    similarities.append(f"语域相同({p1.speech_register.value})")
                if p1.sentence_length == p2.sentence_length:
                    similarities.append(f"句长偏好相同({p1.sentence_length})")
                if p1.vocabulary_level == p2.vocabulary_level:
                    similarities.append(f"词汇水平相同({p1.vocabulary_level})")

                if similarities:
                    issues.append(f"「{names[i]}」与「{names[j]}」: {'; '.join(similarities)}")

        score = max(0.0, 1.0 - len(issues) * 0.15)

        return {
            "distinct": len(issues) == 0,
            "score": score,
            "issues": issues,
            "character_count": len(profiles),
        }

    def export_profiles(self) -> List[Dict]:
        result = []
        for name, profile in self.profiles.items():
            result.append({
                "name": name,
                "speech_register": profile.speech_register.value,
                "sentence_length": profile.sentence_length,
                "catchphrases": profile.catchphrases,
                "speech_quirks": profile.speech_quirks,
                "taboo_words": profile.taboo_words,
                "voice_description": profile.voice_description,
            })
        return result


if __name__ == "__main__":
    print("=" * 60)
    print("角色语音注入系统 - 功能验证")
    print("=" * 60)

    injector = CharacterVoiceInjector()

    print("\n[1] 创建角色语音档案...")
    injector.create_profile("叶青云", template="废柴逆袭")
    injector.create_profile("冷月", template="冷酷大佬")
    injector.create_profile("白老", template="睿智老者")
    injector.create_profile("小蝶", template="天真少女")

    for name in ["叶青云", "冷月", "白老", "小蝶"]:
        p = injector.get_profile(name)
        print(f"  {name}: {p.speech_register.value}, 口头禅={p.catchphrases}")

    print("\n[2] 生成语音约束...")
    for name in ["叶青云", "冷月"]:
        constraint = injector.build_voice_constraint(name)
        print(f"\n  --- {name} ---")
        for line in constraint.split('\n')[:5]:
            print(f"  {line}")

    print("\n[3] 完整注入提示词...")
    prompt = injector.build_full_injection_prompt(
        ["叶青云", "冷月", "白老"],
        scene_emotion=EmotionTone.ANGRY,
        scene_context="宗门大殿，叶青云被诬陷偷取宗门至宝"
    )
    print(f"  注入长度: {len(prompt)}字符")
    print(f"  预览: {prompt[:200]}...")

    print("\n[4] 对话一致性检查...")
    test_dialogues = {
        "叶青云": "你...你们凭什么说是我偷的？我连藏宝阁都没去过！",
        "冷月": "证据。拿出来。否则——死。",
    }
    for name, dialogue in test_dialogues.items():
        result = injector.check_dialogue_consistency(name, dialogue)
        status = "✅" if result["consistent"] else "❌"
        print(f"  {status} {name}: 分数={result['score']:.2f}, 问题={result['issues']}")

    print("\n[5] 角色区分度报告...")
    report = injector.get_character_distinction_report(
        ["叶青云", "冷月", "白老", "小蝶"]
    )
    print(f"  区分度: {report['score']:.2f}")
    print(f"  问题: {report['issues']}")

    print("\n✅ 角色语音注入系统验证完成")
