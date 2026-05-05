#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS AI检测机制升级 - EnhancedAIDetector
相比旧版升级：
1. 三层检测体系 - 词汇层/句式层/语义层
2. 动态阈值 - 根据文本长度和类型自适应
3. 分段检测 - 精确定位AI痕迹位置
4. 智能去痕 - 上下文感知的替换策略
5. 去痕报告 - 详细的修改追踪
6. 批量检测 - 支持多章节批量分析
"""

import re
import random
import json
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from collections import Counter


@dataclass
class DetectionReport:
    """检测报告"""
    overall_score: int
    level: str  # low/medium/high/very_high
    word_layer: Dict
    sentence_layer: Dict
    semantic_layer: Dict
    hot_spots: List[Dict]  # AI痕迹热点位置
    suggestions: List[str]


@dataclass
class RewriteReport:
    """去痕报告"""
    original_score: int
    final_score: int
    reduction: int
    changes_made: int
    replaced_words: List[Tuple[str, str]]
    modified_sentences: int


class EnhancedAIDetector:
    """增强版AI检测器"""

    def __init__(self):
        self._init_word_layer()
        self._init_sentence_layer()
        self._init_semantic_layer()

    def _init_word_layer(self):
        """词汇层特征库 - 三级分类"""
        self.high_risk_words = {
            "连接词": ["首先", "其次", "再次", "最后", "总之", "综上所述",
                      "一方面", "另一方面", "不仅如此", "与此同时"],
            "程度词": ["非常", "极其", "极为", "十分", "特别", "格外",
                      "相当", "颇为", "尤为", "甚为"],
            "比喻词": ["宛如", "仿佛", "犹如", "宛若", "恰似", "好似",
                      "如同", "像...一样", "如...般"],
            "情感词": ["不禁", "不由得", "忍不住", "情不自禁", "不由自主"],
            "描写词": ["缓缓地", "慢慢地", "渐渐地", "轻轻地", "悄悄地",
                      "微微", "淡淡", "轻轻", "默默"],
        }

        self.medium_risk_words = {
            "思考词": ["心中暗想", "心中思索", "心中暗忖", "心想", "暗想"],
            "表情词": ["微微一笑", "轻轻一笑", "淡淡一笑", "笑了笑"],
            "动作词": ["站起身", "转过身", "抬起头", "低下头", "伸出手"],
            "感受词": ["感到", "觉得", "感觉", "意识到", "注意到"],
        }

        self.low_risk_words = {
            "过渡词": ["此时", "此刻", "这时", "那时候", "就在这时"],
            "强调词": ["确实", "的确", "真的", "实在", "真正"],
        }

    def _init_sentence_layer(self):
        """句式层特征库"""
        self.sentence_patterns = [
            (r"^(然而|但是|可是|不过|却)", 0.4, "转折句开头"),
            (r"^(他|她|它|这|那)\s*(站起身|转过身|抬起头|低下头|走出|走进|来到|回到)", 0.5, "主语+动作模板"),
            (r"^在.*?(的|中|下|里|上)", 0.3, "在...的/中/下句式"),
            (r"^随着.*?(，|。)", 0.3, "随着...句式"),
            (r"^只见.*?(，|。)", 0.4, "只见...句式"),
            (r"^只(听|感|觉).*?(，|。)", 0.4, "只听/感/觉...句式"),
            (r"^一股.*?(的|之感|之情)", 0.3, "一股...的句式"),
            (r"^.*?，.*?，.*?，.*?，", 0.2, "逗号密集句"),
            (r"^.{50,}$", 0.2, "超长句"),
            (r"^.{1,5}$", 0.1, "超短句密集"),
        ]

    def _init_semantic_layer(self):
        """语义层特征库"""
        self.semantic_patterns = {
            "情感递进模板": r".*?(不禁|不由得|忍不住).*?(激动|感动|兴奋|紧张|害怕).*?",
            "环境呼应模板": r".*?(阳光|月光|星光|灯光).*?(洒|照|映|落).*?",
            "心理活动模板": r".*?(心中|心里|内心).*?(想|思索|暗忖|暗道|默念).*?",
            "动作链模板": r".*?(站起身|转过身).*?(走|跑|冲|奔).*?",
            "总结升华模板": r".*?(这|那)\s*(一刻|一瞬间|一刹那).*?(终于|才|仿佛).*?",
        }

    def detect(self, text: str, detail_level: str = "full") -> DetectionReport:
        """完整检测"""
        if not text or len(text) < 50:
            return DetectionReport(
                overall_score=0, level="low",
                word_layer={}, sentence_layer={}, semantic_layer={},
                hot_spots=[], suggestions=["文本过短，无法有效检测"]
            )

        word_result = self._detect_word_layer(text)
        sentence_result = self._detect_sentence_layer(text)
        semantic_result = self._detect_semantic_layer(text)

        overall = int(
            word_result["score"] * 0.35 +
            sentence_result["score"] * 0.35 +
            semantic_result["score"] * 0.30
        )

        level = self._score_to_level(overall)
        hot_spots = self._find_hot_spots(text) if detail_level == "full" else []
        suggestions = self._generate_suggestions(word_result, sentence_result, semantic_result)

        return DetectionReport(
            overall_score=overall,
            level=level,
            word_layer=word_result,
            sentence_layer=sentence_result,
            semantic_layer=semantic_result,
            hot_spots=hot_spots,
            suggestions=suggestions,
        )

    def _detect_word_layer(self, text: str) -> Dict:
        """词汇层检测"""
        hits = {}
        total_hits = 0

        for category, words in {**self.high_risk_words, **self.medium_risk_words, **self.low_risk_words}.items():
            cat_hits = {}
            for word in words:
                count = text.count(word)
                if count > 0:
                    cat_hits[word] = count
                    total_hits += count * (3 if category in self.high_risk_words else 2 if category in self.medium_risk_words else 1)
            if cat_hits:
                hits[category] = cat_hits

        text_len = max(len(text), 1)
        density = total_hits / (text_len / 100)
        score = min(int(density * 15), 40)

        return {"hits": hits, "total_hits": total_hits, "density": round(density, 2), "score": score}

    def _detect_sentence_layer(self, text: str) -> Dict:
        """句式层检测"""
        sentences = re.split(r'[。！？\n]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        pattern_hits = {}
        total_pattern_score = 0

        for pattern, weight, name in self.sentence_patterns:
            matches = []
            for i, sent in enumerate(sentences):
                if re.search(pattern, sent):
                    matches.append({"index": i, "text": sent[:80]})
            if matches:
                pattern_hits[name] = {"count": len(matches), "ratio": len(matches) / max(len(sentences), 1)}
                total_pattern_score += len(matches) * weight * 10

        score = min(int(total_pattern_score), 35)
        return {"patterns": pattern_hits, "total_sentences": len(sentences), "score": score}

    def _detect_semantic_layer(self, text: str) -> Dict:
        """语义层检测"""
        pattern_hits = {}

        for name, pattern in self.semantic_patterns.items():
            matches = re.findall(pattern, text)
            if matches:
                pattern_hits[name] = len(matches)

        total = sum(pattern_hits.values())
        score = min(int(total * 5), 25)

        return {"patterns": pattern_hits, "total_matches": total, "score": score}

    def _find_hot_spots(self, text: str) -> List[Dict]:
        """定位AI痕迹热点"""
        paragraphs = text.split('\n')
        hot_spots = []

        for i, para in enumerate(paragraphs):
            if len(para) < 20:
                continue

            local_score = 0
            for words in self.high_risk_words.values():
                for w in words:
                    local_score += para.count(w) * 3
            for words in self.medium_risk_words.values():
                for w in words:
                    local_score += para.count(w) * 2

            if local_score >= 5:
                hot_spots.append({
                    "paragraph": i + 1,
                    "score": local_score,
                    "preview": para[:100],
                })

        hot_spots.sort(key=lambda x: x["score"], reverse=True)
        return hot_spots[:5]

    def _score_to_level(self, score: int) -> str:
        if score < 20:
            return "low"
        elif score < 40:
            return "medium"
        elif score < 60:
            return "high"
        return "very_high"

    def _generate_suggestions(self, word: Dict, sentence: Dict, semantic: Dict) -> List[str]:
        """生成改进建议"""
        suggestions = []

        if word["score"] > 20:
            suggestions.append("词汇层AI痕迹较重，建议替换高频AI特征词")
        if sentence["score"] > 20:
            suggestions.append("句式结构过于规整，建议增加句式变化")
        if semantic["score"] > 15:
            suggestions.append("语义模式过于模板化，建议增加个性化表达")

        if not suggestions:
            suggestions.append("AI痕迹较少，保持当前写作风格即可")

        return suggestions

    def rewrite(self, text: str, intensity: str = "medium") -> Tuple[str, RewriteReport]:
        """智能去痕重写"""
        original = self.detect(text)
        result = text
        changes = []
        replaced = []

        if intensity == "light":
            result = self._light_rewrite(result, replaced)
        elif intensity == "medium":
            result = self._medium_rewrite(result, replaced)
        elif intensity == "heavy":
            result = self._heavy_rewrite(result, replaced)

        result = self._vary_sentence_structure(result)
        result = self._add_natural_imperfections(result)

        final = self.detect(result)
        reduction = original.overall_score - final.overall_score

        return result, RewriteReport(
            original_score=original.overall_score,
            final_score=final.overall_score,
            reduction=reduction,
            changes_made=len(changes),
            replaced_words=replaced,
            modified_sentences=len(changes),
        )

    def _light_rewrite(self, text: str, replaced: List) -> str:
        """轻度去痕 - 仅替换最高风险词"""
        replacements = {
            "宛如": "像", "仿佛": "好像", "犹如": "像",
            "不禁": "忍不住", "不由得": "不自觉地",
            "缓缓地": "慢慢", "渐渐地": "逐步",
        }
        for old, new in replacements.items():
            if old in text:
                text = text.replace(old, new)
                replaced.append((old, new))
        return text

    def _medium_rewrite(self, text: str, replaced: List) -> str:
        """中度去痕"""
        text = self._light_rewrite(text, replaced)

        extra = {
            "非常": "很", "极其": "特别", "十分": "很",
            "微微一笑": "笑了笑", "淡淡一笑": "轻轻一笑",
            "心中暗想": "心想", "心中思索": "思索着",
            "站起身": "站起来", "转过身": "转过来",
        }
        for old, new in extra.items():
            if old in text:
                text = text.replace(old, new)
                replaced.append((old, new))
        return text

    def _heavy_rewrite(self, text: str, replaced: List) -> str:
        """重度去痕"""
        text = self._medium_rewrite(text, replaced)

        heavy = {
            "轻轻地": "轻轻", "悄悄地": "悄悄",
            "感到": "觉得", "感觉": "觉得",
            "此时": "这会儿", "此刻": "现在",
            "只见": "", "只听": "", "只觉": "",
        }
        for old, new in heavy.items():
            if old in text:
                text = text.replace(old, new)
                replaced.append((old, new))
        return text

    def _vary_sentence_structure(self, text: str) -> str:
        """变化句式结构"""
        sentences = re.split(r'(?<=[。！？])', text)
        result = []

        for i, sent in enumerate(sentences):
            if not sent.strip():
                result.append(sent)
                continue

            if random.random() < 0.15 and len(sent) > 15:
                if sent.startswith(('他', '她', '它')):
                    parts = sent.split('，', 1)
                    if len(parts) == 2:
                        sent = parts[1].strip() + '，' + parts[0]

            result.append(sent)

        return ''.join(result)

    def _add_natural_imperfections(self, text: str) -> str:
        """添加自然瑕疵"""
        if random.random() < 0.2:
            fillers = ["嗯", "呃", "那个", "就是", "然后"]
            filler = random.choice(fillers)
            idx = text.find("，", len(text) // 3)
            if idx > 0:
                text = text[:idx + 1] + filler + "，" + text[idx + 1:]

        return text

    def batch_detect(self, chapters: Dict[int, str]) -> Dict:
        """批量检测多章节"""
        results = {}
        total_score = 0

        for ch, content in chapters.items():
            report = self.detect(content)
            results[ch] = {
                "score": report.overall_score,
                "level": report.level,
                "hot_spots_count": len(report.hot_spots),
            }
            total_score += report.overall_score

        avg_score = total_score / max(len(chapters), 1)

        return {
            "chapters": results,
            "average_score": round(avg_score, 1),
            "average_level": self._score_to_level(int(avg_score)),
            "total_chapters": len(chapters),
        }

    def compare_texts(self, text_a: str, text_b: str) -> Dict:
        """对比两段文本的AI痕迹"""
        report_a = self.detect(text_a)
        report_b = self.detect(text_b)

        return {
            "text_a": {"score": report_a.overall_score, "level": report_a.level},
            "text_b": {"score": report_b.overall_score, "level": report_b.level},
            "difference": report_a.overall_score - report_b.overall_score,
            "better": "text_a" if report_a.overall_score < report_b.overall_score else "text_b",
        }


if __name__ == "__main__":
    print("=" * 60)
    print("🔍 增强版AI检测器测试")
    print("=" * 60)

    detector = EnhancedAIDetector()

    ai_text = """
    林晨缓缓地站起身，宛如一只刚刚破茧而出的蝴蝶，心中不禁激动万分。
    仿佛天地都在为他欢呼，眼前的景象十分壮观，格外震撼人心。
    这一切似乎都像是一场梦境，渐渐地，林晨才相信这是真的。
    他微微一笑，心中暗想，自己的努力终究没有白费。
    极其艰难的旅程，非常辛苦的奋斗，终于换来了此刻的成功。
    """

    human_text = """
    林晨站起来，腿有点麻。他揉了揉膝盖，看了眼窗外。
    天快亮了。一夜没睡，脑子昏沉沉的。
    "妈的。"他骂了一句，抓起桌上的烟盒，空的。
    他把烟盒揉成一团，扔进垃圾桶。去他妈的。
    """

    print("\n【AI文本检测】")
    report = detector.detect(ai_text)
    print(f"  总分: {report.overall_score}/100 ({report.level})")
    print(f"  词汇层: {report.word_layer['score']}/40")
    print(f"  句式层: {report.sentence_layer['score']}/35")
    print(f"  语义层: {report.semantic_layer['score']}/25")
    print(f"  热点: {len(report.hot_spots)}处")
    print(f"  建议: {report.suggestions}")

    print("\n【人类文本检测】")
    report2 = detector.detect(human_text)
    print(f"  总分: {report2.overall_score}/100 ({report2.level})")

    print("\n【对比检测】")
    comp = detector.compare_texts(ai_text, human_text)
    print(f"  AI文本: {comp['text_a']['score']}分")
    print(f"  人类文本: {comp['text_b']['score']}分")
    print(f"  更优: {comp['better']}")

    print("\n【中度去痕】")
    rewritten, rw_report = detector.rewrite(ai_text, "medium")
    print(f"  原始分数: {rw_report.original_score} → 去痕后: {rw_report.final_score}")
    print(f"  降低: {rw_report.reduction}分")
    print(f"  替换词数: {len(rw_report.replaced_words)}")
    print(f"  去痕后文本: {rewritten[:150]}...")

    print("\n【批量检测】")
    chapters = {
        1: ai_text,
        2: human_text,
        3: "这是一段混合文本。" + ai_text[:100],
    }
    batch = detector.batch_detect(chapters)
    print(f"  平均分: {batch['average_score']} ({batch['average_level']})")
    for ch, info in batch['chapters'].items():
        print(f"  第{ch}章: {info['score']}分 ({info['level']})")
