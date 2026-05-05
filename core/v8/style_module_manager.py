#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS AI风格模块系统 - StyleModuleManager v2.0

对标 NovelAI AI Modules，核心能力：
1. 风格模块市场 - 预训练风格包库
2. 一键切换 - 运行时动态切换写作风格
3. 风格混合 - 多风格按权重融合，支持渐变过渡
4. 自定义训练 - 从样本文本提取风格模块
5. 风格对比 - 同段文字多风格输出对比
6. 风格分析 - 分析文本匹配哪种风格
7. 一致性检查 - 跨章节风格一致性校验
8. 风格推荐 - 基于题材/内容智能推荐
9. 风格演变 - 追踪风格随时间变化
10. 场景预设 - 不同场景类型的风格预设

内置风格模块：
- 古风典雅 / 现代简约 / 热血燃爆 / 悬疑冷峻
- 言情细腻 / 玄幻磅礴 / 科幻理性 / 幽默诙谐
- 现实主义 / 诗意朦胧
"""

import json
import os
import re
import uuid
import copy
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
from collections import Counter, defaultdict


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


class SceneType(Enum):
    ACTION = ("动作场景", "战斗/追逐/激烈冲突")
    DIALOGUE = ("对话场景", "人物对话/辩论/谈判")
    DESCRIPTION = ("描写场景", "环境/氛围/景物描写")
    INNER_MONOLOGUE = ("内心独白", "心理活动/回忆/思考")
    TRANSITION = ("过渡场景", "时间/空间转换")
    CLIMAX = ("高潮场景", "故事高潮/关键转折")
    EXPOSITION = ("说明场景", "背景介绍/设定说明")


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
    avg_sentence_length: float = 25.0
    dialogue_ratio: float = 0.3
    description_ratio: float = 0.4
    emotion_intensity: float = 0.5
    pace: str = "medium"
    tone: str = "neutral"
    created_at: str = ""
    updated_at: str = ""
    usage_count: int = 0

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
            "avg_sentence_length": self.avg_sentence_length,
            "dialogue_ratio": self.dialogue_ratio,
            "description_ratio": self.description_ratio,
            "emotion_intensity": self.emotion_intensity,
            "pace": self.pace,
            "tone": self.tone,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "usage_count": self.usage_count,
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
            avg_sentence_length=data.get("avg_sentence_length", 25.0),
            dialogue_ratio=data.get("dialogue_ratio", 0.3),
            description_ratio=data.get("description_ratio", 0.4),
            emotion_intensity=data.get("emotion_intensity", 0.5),
            pace=data.get("pace", "medium"),
            tone=data.get("tone", "neutral"),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", ""),
            usage_count=data.get("usage_count", 0),
        )


@dataclass
class StyleAnalysisResult:
    module_id: str
    module_name: str
    match_score: float
    matched_features: List[str]
    suggestions: List[str]


@dataclass
class StylePreset:
    preset_id: str
    name: str
    scene_type: SceneType
    module_weights: Dict[str, float]
    description: str
    additional_rules: List[str] = field(default_factory=list)


class StyleModuleManager:
    """AI风格模块管理器 v2.0"""

    def __init__(self, storage_dir: str = None):
        if storage_dir is None:
            storage_dir = os.path.join(os.path.dirname(__file__), "..", "style_modules")
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)

        self.modules: Dict[str, StyleModule] = {}
        self.active_module: Optional[StyleModule] = None
        self.active_blend: Dict[str, float] = {}
        self.presets: Dict[str, StylePreset] = {}
        self._style_history: List[Dict] = []
        self._transition_queue: List[Dict] = []

        self._load()

    def _get_filepath(self) -> str:
        return os.path.join(self.storage_dir, "style_modules.json")

    def _get_presets_path(self) -> str:
        return os.path.join(self.storage_dir, "style_presets.json")

    def _get_history_path(self) -> str:
        return os.path.join(self.storage_dir, "style_history.json")

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

        presets_path = self._get_presets_path()
        if os.path.exists(presets_path):
            with open(presets_path, "r", encoding="utf-8") as f:
                presets_data = json.load(f)
            for p in presets_data.get("presets", []):
                preset = StylePreset(
                    preset_id=p["preset_id"],
                    name=p["name"],
                    scene_type=SceneType(p["scene_type"]),
                    module_weights=p["module_weights"],
                    description=p["description"],
                    additional_rules=p.get("additional_rules", []),
                )
                self.presets[preset.preset_id] = preset
        else:
            self._init_builtin_presets()

        history_path = self._get_history_path()
        if os.path.exists(history_path):
            with open(history_path, "r", encoding="utf-8") as f:
                self._style_history = json.load(f)

    def save(self):
        data = {
            "version": "2.0",
            "updated_at": datetime.now().isoformat(),
            "active_module": self.active_module.module_id if self.active_module else "",
            "active_blend": self.active_blend,
            "modules": [m.to_dict() for m in self.modules.values()],
        }
        with open(self._get_filepath(), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        with open(self._get_presets_path(), "w", encoding="utf-8") as f:
            json.dump({
                "updated_at": datetime.now().isoformat(),
                "presets": [
                    {
                        "preset_id": p.preset_id,
                        "name": p.name,
                        "scene_type": p.scene_type.value,
                        "module_weights": p.module_weights,
                        "description": p.description,
                        "additional_rules": p.additional_rules,
                    }
                    for p in self.presets.values()
                ],
            }, f, ensure_ascii=False, indent=2)

        with open(self._get_history_path(), "w", encoding="utf-8") as f:
            json.dump(self._style_history[-200:], f, ensure_ascii=False, indent=2)

    def _record_history(self, action: str, detail: str = ""):
        self._style_history.append({
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "detail": detail,
            "active_style": self.active_module.name if self.active_module else "混合",
        })

    def _extract_features(self, text: str) -> Dict:
        sentences = re.split(r'[。！？；\n]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 3]

        if not sentences:
            return {}

        lengths = [len(s) for s in sentences]
        avg_len = sum(lengths) / len(lengths)

        dialogue_lines = len(re.findall(r'[""「」](.+?)[""「」]', text))
        total_chars = len(text)
        dialogue_ratio = (dialogue_lines * 15) / max(total_chars, 1)

        desc_markers = len(re.findall(
            r'(?:看见|望去|只见|放眼|环顾|打量|凝视|观察|呈现|展现|弥漫|笼罩|映照)',
            text
        ))
        description_ratio = (desc_markers * 20) / max(total_chars, 1)

        emotion_words = len(re.findall(
            r'(?:愤怒|悲伤|喜悦|恐惧|惊讶|厌恶|激动|感动|心痛|温暖|冰冷|压抑|兴奋|绝望|希望)',
            text
        ))
        emotion_intensity = min(emotion_words / max(len(sentences), 1), 1.0)

        exclamation_count = len(re.findall(r'[！!]', text))
        question_count = len(re.findall(r'[？?]', text))
        ellipsis_count = len(re.findall(r'[……]', text))

        if avg_len < 15:
            pace = "fast"
        elif avg_len < 30:
            pace = "medium"
        else:
            pace = "slow"

        if emotion_intensity > 0.3:
            tone = "intense"
        elif emotion_intensity > 0.1:
            tone = "moderate"
        else:
            tone = "calm"

        return {
            "avg_sentence_length": avg_len,
            "dialogue_ratio": dialogue_ratio,
            "description_ratio": description_ratio,
            "emotion_intensity": emotion_intensity,
            "exclamation_count": exclamation_count,
            "question_count": question_count,
            "ellipsis_count": ellipsis_count,
            "pace": pace,
            "tone": tone,
            "sentence_count": len(sentences),
            "total_chars": total_chars,
        }

    def register_module(self, module: StyleModule):
        now = datetime.now().isoformat()
        if not module.created_at:
            module.created_at = now
        module.updated_at = now
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
            self.active_module.usage_count += 1
            self.active_blend = {}
            self._record_history("activate", module_id)
            self.save()
            return True
        return False

    def blend(self, weights: Dict[str, float]) -> bool:
        total = sum(weights.values())
        if total == 0:
            return False
        normalized = {k: v / total for k, v in weights.items()}
        for mid in normalized:
            if mid not in self.modules:
                return False
        self.active_blend = normalized
        self.active_module = None
        for mid in normalized:
            self.modules[mid].usage_count += 1
        self._record_history("blend", str(normalized))
        self.save()
        return True

    def schedule_transition(self, target_module_id: str,
                            over_chapters: int = 3) -> bool:
        """计划风格渐变过渡"""
        if target_module_id not in self.modules:
            return False

        current_id = self.active_module.module_id if self.active_module else None
        if not current_id:
            return False

        self._transition_queue = []
        for i in range(over_chapters):
            progress = (i + 1) / over_chapters
            weights = {
                current_id: 1.0 - progress,
                target_module_id: progress,
            }
            self._transition_queue.append({
                "chapter_offset": i,
                "weights": weights,
                "description": f"第{i+1}/{over_chapters}步渐变",
            })

        self.save()
        return True

    def get_transition_for_chapter(self, chapter_offset: int) -> Optional[Dict]:
        """获取指定章节偏移的渐变权重"""
        for step in self._transition_queue:
            if step["chapter_offset"] == chapter_offset:
                return step
        return None

    def clear_transition(self):
        self._transition_queue = []
        self.save()

    def get_active_prompt(self) -> str:
        if self.active_module:
            return self.active_module.system_prompt
        if self.active_blend:
            parts = []
            for mid, weight in sorted(self.active_blend.items(),
                                       key=lambda x: x[1], reverse=True):
                if weight < 0.1:
                    continue
                module = self.modules[mid]
                parts.append(f"[{module.name} 权重{weight:.0%}]\n{module.system_prompt}")
            return "\n\n".join(parts)
        return ""

    def get_active_rules(self) -> List[str]:
        if self.active_module:
            return list(self.active_module.writing_rules)
        if self.active_blend:
            rules = []
            for mid, weight in self.active_blend.items():
                if weight >= 0.3:
                    rules.extend(self.modules[mid].writing_rules)
            return list(dict.fromkeys(rules))
        return []

    def get_active_vocabulary(self) -> Dict[str, float]:
        if self.active_module:
            return dict(self.active_module.vocabulary_bias)
        if self.active_blend:
            merged = {}
            for mid, weight in self.active_blend.items():
                for word, bias in self.modules[mid].vocabulary_bias.items():
                    merged[word] = merged.get(word, 0) + bias * weight
            return dict(sorted(merged.items(), key=lambda x: x[1], reverse=True)[:50])
        return {}

    def get_active_forbidden(self) -> List[str]:
        if self.active_module:
            return list(self.active_module.forbidden_patterns)
        if self.active_blend:
            forbidden = []
            for mid, weight in self.active_blend.items():
                if weight >= 0.3:
                    forbidden.extend(self.modules[mid].forbidden_patterns)
            return list(set(forbidden))
        return []

    def list_modules(self, category: StyleCategory = None) -> List[StyleModule]:
        modules = list(self.modules.values())
        if category:
            modules = [m for m in modules if m.category == category]
        return modules

    def analyze_style(self, text: str) -> List[StyleAnalysisResult]:
        """分析文本匹配哪些风格"""
        features = self._extract_features(text)
        if not features:
            return []

        results = []
        for module in self.modules.values():
            score = 0.0
            matched = []

            len_diff = abs(features["avg_sentence_length"] - module.avg_sentence_length)
            len_score = max(0, 1.0 - len_diff / 50)
            score += len_score * 0.15
            if len_score > 0.7:
                matched.append(f"句长匹配({features['avg_sentence_length']:.0f}≈{module.avg_sentence_length:.0f})")

            dia_diff = abs(features["dialogue_ratio"] - module.dialogue_ratio)
            dia_score = max(0, 1.0 - dia_diff * 2)
            score += dia_score * 0.1

            desc_diff = abs(features["description_ratio"] - module.description_ratio)
            desc_score = max(0, 1.0 - desc_diff * 2)
            score += desc_score * 0.1

            emo_diff = abs(features["emotion_intensity"] - module.emotion_intensity)
            emo_score = max(0, 1.0 - emo_diff * 2)
            score += emo_score * 0.15
            if emo_score > 0.7:
                matched.append("情感强度匹配")

            if features["pace"] == module.pace:
                score += 0.15
                matched.append(f"节奏匹配({module.pace})")

            if features["tone"] == module.tone:
                score += 0.1
                matched.append(f"语调匹配({module.tone})")

            text_words = set(re.findall(r'[\u4e00-\u9fff]{2,}', text))
            module_words = set(module.vocabulary_bias.keys())
            common = text_words & module_words
            if common:
                vocab_score = min(len(common) / 20, 0.25)
                score += vocab_score
                if vocab_score > 0.1:
                    matched.append(f"词汇匹配({len(common)}个)")

            suggestions = []
            if score > 0.4:
                suggestions.append(f"推荐使用「{module.name}」风格")
                if module.writing_rules:
                    suggestions.append(f"关键规则: {module.writing_rules[0]}")

            results.append(StyleAnalysisResult(
                module_id=module.module_id,
                module_name=module.name,
                match_score=round(score, 3),
                matched_features=matched,
                suggestions=suggestions,
            ))

        results.sort(key=lambda r: r.match_score, reverse=True)
        return results

    def recommend_style(self, genre: str = None, content_type: str = None,
                        target_emotion: str = None) -> List[Tuple[StyleModule, float]]:
        """基于需求智能推荐风格"""
        recommendations = []

        genre_style_map = {
            "仙侠": ["style_classical", "style_fantasy"],
            "玄幻": ["style_fantasy", "style_hotblood"],
            "都市": ["style_realistic", "style_romance"],
            "言情": ["style_romance", "style_poetic"],
            "悬疑": ["style_suspense", "style_realistic"],
            "科幻": ["style_scifi", "style_realistic"],
            "轻小说": ["style_humor", "style_hotblood"],
            "历史": ["style_classical", "style_realistic"],
            "竞技": ["style_hotblood", "style_realistic"],
            "恐怖": ["style_suspense", "style_classical"],
        }

        emotion_style_map = {
            "热血": ["style_hotblood", "style_fantasy"],
            "温馨": ["style_romance", "style_poetic"],
            "紧张": ["style_suspense", "style_hotblood"],
            "悲伤": ["style_poetic", "style_romance"],
            "搞笑": ["style_humor", "style_realistic"],
            "震撼": ["style_fantasy", "style_classical"],
            "冷静": ["style_scifi", "style_suspense"],
        }

        candidate_scores = defaultdict(float)

        if genre and genre in genre_style_map:
            for i, mid in enumerate(genre_style_map[genre]):
                candidate_scores[mid] += 0.5 - i * 0.15

        if target_emotion and target_emotion in emotion_style_map:
            for i, mid in enumerate(emotion_style_map[target_emotion]):
                candidate_scores[mid] += 0.4 - i * 0.1

        if content_type:
            if "战斗" in content_type or "动作" in content_type:
                candidate_scores["style_hotblood"] += 0.3
                candidate_scores["style_fantasy"] += 0.2
            if "对话" in content_type:
                candidate_scores["style_humor"] += 0.2
                candidate_scores["style_realistic"] += 0.2
            if "描写" in content_type:
                candidate_scores["style_classical"] += 0.2
                candidate_scores["style_poetic"] += 0.3
            if "心理" in content_type:
                candidate_scores["style_romance"] += 0.3
                candidate_scores["style_poetic"] += 0.2

        for mid, score in candidate_scores.items():
            if mid in self.modules:
                recommendations.append((self.modules[mid], round(score, 2)))

        recommendations.sort(key=lambda x: x[1], reverse=True)
        return recommendations

    def extract_style_from_text(self, text: str, name: str,
                                 category: StyleCategory) -> StyleModule:
        """从样本文本中提取风格模块"""
        features = self._extract_features(text)

        sentences = re.split(r'[。！？；\n]', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 5]

        words = re.findall(r'[\u4e00-\u9fff]+', text)
        word_freq = Counter(words)
        top_words = word_freq.most_common(30)

        vocab_bias = {}
        for word, count in top_words:
            vocab_bias[word] = min(count / max(len(sentences), 1), 1.0)

        if features.get("avg_sentence_length", 25) < 15:
            pattern = "短句为主，节奏明快"
        elif features.get("avg_sentence_length", 25) < 30:
            pattern = "中短句结合，张弛有度"
        else:
            pattern = "长句为主，铺陈细腻"

        rules = [
            f"平均句长约{features.get('avg_sentence_length', 25):.0f}字",
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
            avg_sentence_length=features.get("avg_sentence_length", 25),
            dialogue_ratio=features.get("dialogue_ratio", 0.3),
            description_ratio=features.get("description_ratio", 0.4),
            emotion_intensity=features.get("emotion_intensity", 0.5),
            pace=features.get("pace", "medium"),
            tone=features.get("tone", "neutral"),
        )
        self.register_module(module)
        return module

    def train_from_samples(self, samples: List[str], name: str,
                           category: StyleCategory) -> StyleModule:
        """从多个样本训练风格模块"""
        combined = "\n".join(samples)
        return self.extract_style_from_text(combined, name, category)

    def compare_styles(self, text: str, module_ids: List[str]) -> Dict[str, Dict]:
        """同段文字多风格改写建议"""
        results = {}
        for mid in module_ids:
            if mid in self.modules:
                module = self.modules[mid]
                results[module.name] = {
                    "module_id": mid,
                    "category": module.category.label,
                    "rules": module.writing_rules,
                    "vocabulary": list(module.vocabulary_bias.keys())[:10],
                    "prompt": module.system_prompt,
                    "forbidden": module.forbidden_patterns,
                    "pace": module.pace,
                    "tone": module.tone,
                }
        return results

    def check_consistency(self, chapters: List[str]) -> List[Dict]:
        """检查多章节风格一致性"""
        if len(chapters) < 2:
            return []

        chapter_features = []
        for i, ch in enumerate(chapters):
            features = self._extract_features(ch)
            features["chapter_index"] = i
            chapter_features.append(features)

        issues = []
        baseline = chapter_features[0]

        for i, feat in enumerate(chapter_features[1:], 1):
            chapter_issues = []

            len_change = abs(feat["avg_sentence_length"] - baseline["avg_sentence_length"])
            if len_change > 15:
                chapter_issues.append(
                    f"句长变化过大 ({baseline['avg_sentence_length']:.0f}→{feat['avg_sentence_length']:.0f})"
                )

            emo_change = abs(feat["emotion_intensity"] - baseline["emotion_intensity"])
            if emo_change > 0.4:
                chapter_issues.append(
                    f"情感强度突变 ({baseline['emotion_intensity']:.2f}→{feat['emotion_intensity']:.2f})"
                )

            if feat["pace"] != baseline["pace"]:
                chapter_issues.append(
                    f"节奏变化 ({baseline['pace']}→{feat['pace']})"
                )

            if chapter_issues:
                issues.append({
                    "chapter": i,
                    "issues": chapter_issues,
                    "severity": "warning" if len(chapter_issues) >= 2 else "info",
                })

        return issues

    def get_style_evolution(self) -> List[Dict]:
        """获取风格演变历史"""
        return [
            {
                "time": h["timestamp"],
                "action": h["action"],
                "style": h["active_style"],
                "detail": h["detail"],
            }
            for h in self._style_history[-50:]
        ]

    def add_preset(self, preset: StylePreset):
        self.presets[preset.preset_id] = preset
        self.save()

    def get_presets_for_scene(self, scene_type: SceneType) -> List[StylePreset]:
        return [p for p in self.presets.values() if p.scene_type == scene_type]

    def apply_preset(self, preset_id: str) -> bool:
        if preset_id not in self.presets:
            return False
        preset = self.presets[preset_id]
        return self.blend(preset.module_weights)

    def export_module(self, module_id: str, filepath: str) -> bool:
        if module_id not in self.modules:
            return False
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.modules[module_id].to_dict(), f, ensure_ascii=False, indent=2)
        return True

    def import_module(self, filepath: str) -> Optional[str]:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        module = StyleModule.from_dict(data)
        if module.module_id in self.modules:
            module.module_id = str(uuid.uuid4())[:8]
        self.register_module(module)
        return module.module_id

    def get_stats(self) -> dict:
        by_category = {}
        for cat in StyleCategory:
            count = len(self.list_modules(cat))
            if count > 0:
                by_category[cat.label] = count

        most_used = sorted(
            self.modules.values(),
            key=lambda m: m.usage_count,
            reverse=True
        )[:5]

        return {
            "total_modules": len(self.modules),
            "total_presets": len(self.presets),
            "active_style": self.active_module.name if self.active_module else (
                "混合风格" if self.active_blend else "无"
            ),
            "by_category": by_category,
            "most_used": [(m.name, m.usage_count) for m in most_used],
            "history_count": len(self._style_history),
            "transition_active": len(self._transition_queue) > 0,
        }

    def _init_builtin_presets(self):
        builtins = [
            StylePreset(
                preset_id="preset_action",
                name="动作场景预设",
                scene_type=SceneType.ACTION,
                module_weights={"style_hotblood": 0.7, "style_fantasy": 0.3},
                description="战斗/追逐场景，节奏快，冲击力强",
                additional_rules=["短句为主", "动作描写细致", "每段结尾留悬念"],
            ),
            StylePreset(
                preset_id="preset_dialogue",
                name="对话场景预设",
                scene_type=SceneType.DIALOGUE,
                module_weights={"style_realistic": 0.6, "style_humor": 0.4},
                description="人物对话场景，自然流畅，有个性",
                additional_rules=["对话简短有力", "每句体现人物性格", "适当加入动作描写"],
            ),
            StylePreset(
                preset_id="preset_description",
                name="描写场景预设",
                scene_type=SceneType.DESCRIPTION,
                module_weights={"style_classical": 0.5, "style_poetic": 0.5},
                description="环境/氛围描写，意境优美",
                additional_rules=["多感官描写", "动静结合", "景语皆情语"],
            ),
            StylePreset(
                preset_id="preset_monologue",
                name="内心独白预设",
                scene_type=SceneType.INNER_MONOLOGUE,
                module_weights={"style_romance": 0.6, "style_poetic": 0.4},
                description="心理活动/回忆场景，情感细腻",
                additional_rules=["情感层次丰富", "善用比喻", "节奏舒缓"],
            ),
            StylePreset(
                preset_id="preset_climax",
                name="高潮场景预设",
                scene_type=SceneType.CLIMAX,
                module_weights={"style_hotblood": 0.5, "style_fantasy": 0.3, "style_suspense": 0.2},
                description="故事高潮/关键转折，情绪饱满",
                additional_rules=["节奏紧凑", "情感渲染强烈", "每段都是爆点"],
            ),
            StylePreset(
                preset_id="preset_exposition",
                name="说明场景预设",
                scene_type=SceneType.EXPOSITION,
                module_weights={"style_realistic": 0.5, "style_scifi": 0.3, "style_modern": 0.2},
                description="背景介绍/设定说明，清晰易懂",
                additional_rules=["逻辑清晰", "避免信息堆砌", "融入叙事不枯燥"],
            ),
        ]
        for preset in builtins:
            self.presets[preset.preset_id] = preset

    def _init_builtin_modules(self):
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
                    "苍穹": 0.9, "云霄": 0.8, "浩瀚": 0.8,
                    "巍峨": 0.8, "缥缈": 0.9, "凌厉": 0.7, "磅礴": 0.8,
                    "沧桑": 0.7, "风华": 0.8, "绝代": 0.7, "倾城": 0.7,
                },
                sentence_patterns=["四六骈文", "五言七言", "长短交错"],
                forbidden_patterns=["卧槽", "牛逼", "666", "绝绝子"],
                example_text="苍穹之上，一道剑光划破长空。那少年负手而立，衣袂飘飘，目光如电，扫视着脚下万里山河。",
                avg_sentence_length=28.0,
                dialogue_ratio=0.25,
                description_ratio=0.5,
                emotion_intensity=0.4,
                pace="slow",
                tone="moderate",
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
                avg_sentence_length=12.0,
                dialogue_ratio=0.2,
                description_ratio=0.3,
                emotion_intensity=0.9,
                pace="fast",
                tone="intense",
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
                    "寂静": 0.8, "黑暗": 0.7, "压抑": 0.8,
                    "诡异": 0.7, "寒意": 0.7, "死寂": 0.8, "阴冷": 0.7,
                },
                sentence_patterns=["短句为主", "细节堆叠", "留白结尾"],
                forbidden_patterns=["显然", "明显", "毫无疑问"],
                example_text="他推开门。\n房间里很暗。窗帘拉得严严实实，只有一缕光从缝隙中挤进来，落在地板中央。那里什么都没有。但灰尘的分布不对。",
                avg_sentence_length=14.0,
                dialogue_ratio=0.3,
                description_ratio=0.45,
                emotion_intensity=0.3,
                pace="medium",
                tone="calm",
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
                avg_sentence_length=32.0,
                dialogue_ratio=0.35,
                description_ratio=0.35,
                emotion_intensity=0.8,
                pace="slow",
                tone="intense",
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
                avg_sentence_length=26.0,
                dialogue_ratio=0.2,
                description_ratio=0.5,
                emotion_intensity=0.7,
                pace="medium",
                tone="intense",
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
                avg_sentence_length=18.0,
                dialogue_ratio=0.45,
                description_ratio=0.25,
                emotion_intensity=0.6,
                pace="fast",
                tone="moderate",
            ),
            StyleModule(
                module_id="style_realistic",
                name="现实主义",
                category=StyleCategory.REALISTIC,
                description="贴近生活，细节真实，社会洞察，适合都市/现实题材",
                system_prompt="""你是一位现实主义作家。请以现实主义风格写作：
- 细节真实可信，源于生活
- 人物塑造立体，有优点也有缺点
- 社会观察敏锐，反映时代
- 语言朴实有力，不矫揉造作
- 情感真挚，不刻意煽情""",
                writing_rules=[
                    "细节要真实，符合生活逻辑",
                    "人物要有缺点，不能完美",
                    "对话符合人物身份和时代背景",
                    "情感表达克制，用行动代替抒情",
                    "社会背景要真实可信",
                ],
                vocabulary_bias={
                    "生活": 0.7, "现实": 0.7, "平凡": 0.6, "真实": 0.7,
                    "挣扎": 0.6, "无奈": 0.6, "坚持": 0.6, "改变": 0.6,
                    "日常": 0.6, "琐碎": 0.5, "普通": 0.6, "人间": 0.6,
                },
                sentence_patterns=["白描手法", "细节堆叠", "平淡收尾"],
                forbidden_patterns=["天选之子", "命中注定"],
                example_text="他每天早上六点起床，坐一个半小时的地铁去上班。车厢里挤满了和他一样的人——面无表情，盯着手机，等待新的一天把自己碾碎。",
                avg_sentence_length=22.0,
                dialogue_ratio=0.35,
                description_ratio=0.4,
                emotion_intensity=0.4,
                pace="medium",
                tone="calm",
            ),
            StyleModule(
                module_id="style_poetic",
                name="诗意朦胧",
                category=StyleCategory.POETIC,
                description="意境优美，留白丰富，含蓄隽永，适合文艺/散文风格",
                system_prompt="""你是一位富有诗意的作家。请以诗意朦胧风格写作：
- 意境优先，画面感强
- 大量留白，让读者想象
- 语言优美如诗，但不晦涩
- 情感含蓄，意在言外
- 善用意象和隐喻""",
                writing_rules=[
                    "每段营造一个意象或画面",
                    "留白至少30%，不写满",
                    "善用通感，如'听见了花香'",
                    "情感含蓄，用景物暗示",
                    "结尾要有余韵，让人回味",
                ],
                vocabulary_bias={
                    "月光": 0.8, "微风": 0.7, "细雨": 0.8, "黄昏": 0.7,
                    "落叶": 0.7, "花开": 0.7, "流水": 0.7, "浮云": 0.7,
                    "梦境": 0.8, "回忆": 0.7, "远方": 0.7, "时光": 0.7,
                },
                sentence_patterns=["意象开场", "留白过渡", "余韵收尾"],
                forbidden_patterns=["然后", "接着", "之后"],
                example_text="雨落在青石板上。\n一滴，又一滴。\n她站在巷口，撑着一把油纸伞。伞下的阴影遮住了半张脸，只露出一双眼睛——像深秋的湖水。",
                avg_sentence_length=20.0,
                dialogue_ratio=0.15,
                description_ratio=0.6,
                emotion_intensity=0.5,
                pace="slow",
                tone="moderate",
            ),
            StyleModule(
                module_id="style_scifi",
                name="科幻理性",
                category=StyleCategory.SCIFI,
                description="逻辑严密，科技感强，理性克制，适合科幻/硬核题材",
                system_prompt="""你是一位科幻作家。请以科幻理性风格写作：
- 科技设定要有科学依据
- 逻辑严密，因果链清晰
- 语言精准，避免模糊表达
- 在硬核设定中融入人文关怀
- 善用数据和专业术语增强可信度""",
                writing_rules=[
                    "科技设定要有内在逻辑",
                    "专业术语使用准确",
                    "因果链清晰，每个结果都有原因",
                    "在理性中保留人文温度",
                    "避免魔法式解决（Deus ex Machina）",
                ],
                vocabulary_bias={
                    "系统": 0.7, "数据": 0.7, "算法": 0.7, "维度": 0.7,
                    "量子": 0.7, "基因": 0.7, "网络": 0.6, "程序": 0.6,
                    "模拟": 0.6, "意识": 0.7, "现实": 0.6, "虚拟": 0.6,
                },
                sentence_patterns=["逻辑推导", "数据支撑", "人文反思"],
                forbidden_patterns=["莫名其妙", "不知为何"],
                example_text="当量子计算机第137次模拟宇宙大爆炸时，一个异常数据出现了。那不是随机噪声——那是一段有序信息，像是某种智慧生命留下的签名。",
                avg_sentence_length=24.0,
                dialogue_ratio=0.25,
                description_ratio=0.4,
                emotion_intensity=0.3,
                pace="medium",
                tone="calm",
            ),
            StyleModule(
                module_id="style_modern",
                name="现代简约",
                category=StyleCategory.MODERN,
                description="现代白话风格，简洁明快，贴近生活，通用性最强",
                system_prompt="""你是一位现代作家。请以现代简约风格写作：
- 语言简洁明快，不拖泥带水
- 贴近当代生活，接地气
- 节奏适中，阅读轻松
- 对话自然流畅，符合口语习惯
- 描写精准但不冗长""",
                writing_rules=[
                    "语言简洁，每句表达一个意思",
                    "对话符合当代口语习惯",
                    "描写精准，避免过度修饰",
                    "节奏适中，不赶也不拖",
                    "适合大多数现代题材",
                ],
                vocabulary_bias={
                    "简单": 0.5, "直接": 0.5, "清楚": 0.5, "明白": 0.5,
                    "自然": 0.5, "轻松": 0.5, "日常": 0.5, "普通": 0.5,
                },
                sentence_patterns=["简洁叙述", "自然对话", "精准描写"],
                forbidden_patterns=[],
                example_text="他走进咖啡馆，点了一杯美式。窗外的阳光很好，照在桌面上，暖洋洋的。他翻开笔记本，开始写今天的章节。",
                avg_sentence_length=20.0,
                dialogue_ratio=0.35,
                description_ratio=0.35,
                emotion_intensity=0.4,
                pace="medium",
                tone="moderate",
            ),
        ]

        for module in builtins:
            self.modules[module.module_id] = module

        self.active_module = self.modules.get("style_classical")
        self.save()
