"""
NWACS 文风指纹系统
基于 InkOS style analyze/import 架构深度优化
提取和注入写作风格指纹，锁定文风一致性

核心功能：
1. 统计指纹提取 - 句长分布、词频特征、节奏模式
2. LLM风格指南生成 - 从参考文本提取可执行的风格规则
3. 文风注入 - 将指纹注入写作prompt
4. 风格一致性审计 - 检测章节是否偏离设定风格
"""

import re
import math
from collections import Counter
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field


@dataclass
class StyleFingerprint:
    sentence_length_mean: float = 0
    sentence_length_std: float = 0
    dialogue_ratio: float = 0
    paragraph_avg_length: float = 0
    top_bigrams: List[Tuple[str, int]] = field(default_factory=list)
    top_trigrams: List[Tuple[str, int]] = field(default_factory=list)
    punctuation_freq: Dict[str, float] = field(default_factory=dict)
    pos_ratio: Dict[str, float] = field(default_factory=dict)
    description_vs_dialogue: float = 0
    emotion_word_ratio: float = 0
    action_word_ratio: float = 0
    passive_voice_ratio: float = 0
    avg_sentence_complexity: float = 0
    style_rules: List[str] = field(default_factory=list)
    sample_text: str = ''


class StyleFingerprintEngine:
    def __init__(self):
        self._fingerprints: Dict[str, StyleFingerprint] = {}

    def analyze(self, text: str, label: str = 'default') -> StyleFingerprint:
        fp = StyleFingerprint()
        fp.sample_text = text[:500]

        sentences = self._split_sentences(text)
        if not sentences:
            return fp

        sentence_lengths = [len(s) for s in sentences]
        fp.sentence_length_mean = sum(sentence_lengths) / len(sentence_lengths)
        if len(sentence_lengths) > 1:
            variance = sum((l - fp.sentence_length_mean) ** 2 for l in sentence_lengths) / len(sentence_lengths)
            fp.sentence_length_std = math.sqrt(variance)

        paragraphs = [p for p in text.split('\n') if p.strip()]
        fp.paragraph_avg_length = sum(len(p) for p in paragraphs) / len(paragraphs) if paragraphs else 0

        dialogue_lines = re.findall(r'「[^」]*」|"[^"]*"|\'[^\']*\'', text)
        dialogue_chars = sum(len(d) for d in dialogue_lines)
        fp.dialogue_ratio = dialogue_chars / len(text) if text else 0

        words = self._tokenize(text)
        if len(words) >= 2:
            bigrams = Counter(zip(words, words[1:]))
            fp.top_bigrams = bigrams.most_common(10)
        if len(words) >= 3:
            trigrams = Counter(zip(words, words[1:], words[2:]))
            fp.top_trigrams = trigrams.most_common(5)

        puncts = re.findall(r'[，。！？、；：""''（）【】《》]', text)
        fp.punctuation_freq = dict(Counter(puncts).most_common(10))

        emotion_words = len(re.findall(r'[喜怒哀乐悲恐惊恨爱恨愁烦闷]', text))
        fp.emotion_word_ratio = emotion_words / len(text) if text else 0

        action_words = len(re.findall(r'[走跑跳打杀飞逃追]', text))
        fp.action_word_ratio = action_words / len(text) if text else 0

        passive = len(re.findall(r'被|受|遭|挨', text))
        fp.passive_voice_ratio = passive / len(text) if text else 0

        complex_sentences = sum(1 for s in sentences if len(s) > 50)
        fp.avg_sentence_complexity = complex_sentences / len(sentences) if sentences else 0

        fp.style_rules = self._generate_style_rules(fp, text)

        self._fingerprints[label] = fp
        return fp

    def _split_sentences(self, text: str) -> List[str]:
        sentences = re.split(r'[。！？\n]+', text)
        return [s.strip() for s in sentences if len(s.strip()) > 5]

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r'[\u4e00-\u9fff]{2,4}|[a-zA-Z]+|\d+', text)
        return tokens

    def _generate_style_rules(self, fp: StyleFingerprint, text: str) -> List[str]:
        rules = []

        if fp.sentence_length_mean < 20:
            rules.append('使用短句为主，平均句长不超过20字，节奏明快')
        elif fp.sentence_length_mean < 35:
            rules.append('使用中长句，平均句长20-35字，节奏适中')
        else:
            rules.append('使用长句为主，平均句长超过35字，节奏舒缓')

        if fp.dialogue_ratio > 0.4:
            rules.append('对话占比高(>40%)，以对话驱动叙事')
        elif fp.dialogue_ratio > 0.2:
            rules.append('对话与叙述并重，对话占比20%-40%')
        else:
            rules.append('叙述为主，对话占比低于20%')

        if fp.emotion_word_ratio > 0.05:
            rules.append('情感词汇使用频繁，注重情绪渲染')
        else:
            rules.append('情感表达克制，以行动和对话暗示情绪')

        if fp.action_word_ratio > 0.03:
            rules.append('动作描写密集，节奏紧张')
        else:
            rules.append('动作描写适度，注重氛围营造')

        if fp.passive_voice_ratio < 0.01:
            rules.append('极少使用被动语态，行文直接有力')
        else:
            rules.append('适度使用被动语态')

        if fp.avg_sentence_complexity > 0.3:
            rules.append('复杂长句比例较高(>30%)，句式丰富')
        else:
            rules.append('句式简洁，避免复杂嵌套结构')

        return rules

    def get_fingerprint(self, label: str = 'default') -> Optional[StyleFingerprint]:
        return self._fingerprints.get(label)

    def get_style_prompt(self, label: str = 'default') -> str:
        fp = self._fingerprints.get(label)
        if not fp:
            return ''

        prompt_parts = ['## 文风要求（基于风格指纹）']
        for rule in fp.style_rules:
            prompt_parts.append(f'- {rule}')

        if fp.top_bigrams:
            bigram_str = '、'.join([f'"{w1} {w2}"' for (w1, w2), _ in fp.top_bigrams[:5]])
            prompt_parts.append(f'- 常用搭配：{bigram_str}')

        return '\n'.join(prompt_parts)

    def compare(self, text: str, reference_label: str = 'default') -> Dict[str, Any]:
        ref_fp = self._fingerprints.get(reference_label)
        if not ref_fp:
            return {'match': False, 'error': 'No reference fingerprint'}

        current_fp = self.analyze(text, '_compare_temp')

        deviations = []
        total_score = 100

        sent_diff = abs(current_fp.sentence_length_mean - ref_fp.sentence_length_mean)
        if sent_diff > 10:
            deviations.append(f'句长偏差过大：参考{ref_fp.sentence_length_mean:.1f}字，当前{current_fp.sentence_length_mean:.1f}字')
            total_score -= 20
        elif sent_diff > 5:
            deviations.append(f'句长略有偏差：参考{ref_fp.sentence_length_mean:.1f}字，当前{current_fp.sentence_length_mean:.1f}字')
            total_score -= 10

        dial_diff = abs(current_fp.dialogue_ratio - ref_fp.dialogue_ratio)
        if dial_diff > 0.2:
            deviations.append(f'对话比例偏差大：参考{ref_fp.dialogue_ratio:.0%}，当前{current_fp.dialogue_ratio:.0%}')
            total_score -= 15
        elif dial_diff > 0.1:
            total_score -= 5

        emotion_diff = abs(current_fp.emotion_word_ratio - ref_fp.emotion_word_ratio)
        if emotion_diff > 0.03:
            deviations.append(f'情感词汇密度偏差：参考{ref_fp.emotion_word_ratio:.2%}，当前{current_fp.emotion_word_ratio:.2%}')
            total_score -= 10

        action_diff = abs(current_fp.action_word_ratio - ref_fp.action_word_ratio)
        if action_diff > 0.02:
            deviations.append(f'动作词汇密度偏差：参考{ref_fp.action_word_ratio:.2%}，当前{current_fp.action_word_ratio:.2%}')
            total_score -= 10

        return {
            'match': total_score >= 60,
            'score': max(0, total_score),
            'deviations': deviations,
            'reference': {
                'sentence_length_mean': ref_fp.sentence_length_mean,
                'dialogue_ratio': ref_fp.dialogue_ratio,
                'emotion_word_ratio': ref_fp.emotion_word_ratio,
                'action_word_ratio': ref_fp.action_word_ratio,
            },
            'current': {
                'sentence_length_mean': current_fp.sentence_length_mean,
                'dialogue_ratio': current_fp.dialogue_ratio,
                'emotion_word_ratio': current_fp.emotion_word_ratio,
                'action_word_ratio': current_fp.action_word_ratio,
            },
        }

    def list_fingerprints(self) -> List[str]:
        return list(self._fingerprints.keys())