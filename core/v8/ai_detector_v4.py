#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS V8.0 AI Detector V4
Multi-dimensional AI feature detection and optimization system
"""

import re
import json
import math
import random
from typing import Dict, List, Tuple, Optional
from collections import Counter
import time


class MultiDimensionDetector:
    """Multi-dimensional Detection Matrix"""
    
    def __init__(self):
        self.connection_words = [
            '首先', '其次', '然后', '最后', '因此', '所以', '但是', '然而',
            '而且', '此外', '另外', '总之', '综上所述', '由此可见'
        ]
        self.abstract_words = [
            '系统', '方法', '问题', '情况', '因素', '方面', '领域', '层面',
            '维度', '角度', '程度', '范围', '过程', '机制'
        ]
        self.emotion_words = [
            '开心', '难过', '愤怒', '惊喜', '感动', '遗憾', '期待', '担心',
            '满意', '失望', '激动', '平静', '紧张', '放松'
        ]
        self.personal_markers = [
            '我觉得', '我认为', '我个人', '在我看来', '我的经验',
            '我记得', '我注意到', '我发现', '我理解', '我感受'
        ]
        
    def lexical_analysis(self, text: str) -> Dict:
        """Lexical level analysis"""
        words = list(text)
        word_count = len(words)
        
        conn_count = sum(text.count(w) for w in self.connection_words)
        conn_freq = conn_count / max(word_count, 1)
        
        word_freq = Counter(text.split())
        total_words = len(text.split())
        unique_words = len(word_freq)
        repetition_rate = 1 - (unique_words / max(total_words, 1))
        
        diversity = len(set(text)) / max(len(text), 1)
        
        return {
            "connection_frequency": conn_freq,
            "repetition_rate": repetition_rate,
            "lexical_diversity": diversity,
            "connection_count": conn_count
        }
    
    def syntactic_analysis(self, text: str) -> Dict:
        """Syntactic level analysis"""
        sentences = re.split(r'[。！？\n]', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences:
            return {"avg_sentence_length": 0, "regularity": 0, "symmetry": 0}
        
        sentence_lengths = [len(s) for s in sentences]
        avg_length = sum(sentence_lengths) / len(sentences)
        length_variance = sum((l - avg_length) ** 2 for l in sentence_lengths) / len(sentences)
        
        regularity = 1 / (1 + length_variance / 1000)
        
        symmetry = self._calculate_symmetry(sentences)
        
        return {
            "avg_sentence_length": avg_length,
            "regularity": regularity,
            "symmetry": symmetry,
            "sentence_count": len(sentences)
        }
    
    def semantic_analysis(self, text: str) -> Dict:
        """Semantic level analysis"""
        emotion_count = sum(text.count(w) for w in self.emotion_words)
        emotion_density = emotion_count / max(len(text), 1)
        
        abstract_count = sum(text.count(w) for w in self.abstract_words)
        abstract_level = abstract_count / max(len(text), 1)
        
        detail_patterns = [
            r'\d+',
            r'[A-Z][a-z]+',
            r'"[^"]*"',
            r'《[^》]*》'
        ]
        detail_count = sum(len(re.findall(pattern, text)) for pattern in detail_patterns)
        
        return {
            "emotion_density": emotion_density,
            "abstract_level": abstract_level,
            "detail_count": detail_count
        }
    
    def style_analysis(self, text: str) -> Dict:
        """Style level analysis"""
        personal_count = sum(text.count(m) for m in self.personal_markers)
        
        oral_markers = ['嗯', '啊', '呢', '吧', '嘛', '哦', '哈', '啦']
        oral_count = sum(text.count(m) for m in oral_markers)
        oral_level = oral_count / max(len(text), 1)
        
        sentences = re.split(r'[。！？\n]', text)
        sentence_emotions = []
        for s in sentences:
            emotion_score = sum(s.count(w) for w in self.emotion_words)
            sentence_emotions.append(emotion_score)
        
        emotion_volatility = 0
        if len(sentence_emotions) > 1:
            emotion_volatility = max(sentence_emotions) - min(sentence_emotions)
        
        return {
            "personal_marker_count": personal_count,
            "oral_level": oral_level,
            "emotion_volatility": emotion_volatility
        }
    
    def _calculate_symmetry(self, sentences: List[str]) -> float:
        """Calculate structural symmetry"""
        if len(sentences) < 2:
            return 0
        
        symmetry_score = 0
        for i in range(len(sentences) - 1):
            s1, s2 = sentences[i], sentences[i+1]
            if len(s1) > 0 and len(s2) > 0:
                ratio = min(len(s1), len(s2)) / max(len(s1), len(s2))
                if ratio > 0.8:
                    symmetry_score += 1
        
        return symmetry_score / (len(sentences) - 1)
    
    def full_analysis(self, text: str) -> Dict:
        """Complete multi-dimensional analysis"""
        return {
            "lexical": self.lexical_analysis(text),
            "syntactic": self.syntactic_analysis(text),
            "semantic": self.semantic_analysis(text),
            "style": self.style_analysis(text)
        }


class IntelligentScoringEngine:
    """Intelligent Scoring Engine"""
    
    def __init__(self):
        self.base_score = 30
        
    def calculate_score(self, analysis_result: Dict) -> int:
        """Calculate comprehensive score"""
        score = self.base_score
        
        lexical = analysis_result.get("lexical", {})
        repetition_rate = lexical.get("repetition_rate", 0)
        if repetition_rate > 0.3:
            score -= int((repetition_rate - 0.3) * 50)
        
        syntactic = analysis_result.get("syntactic", {})
        regularity = syntactic.get("regularity", 0)
        if regularity > 0.7:
            score -= int((regularity - 0.7) * 100)
        
        style = analysis_result.get("style", {})
        emotion_volatility = style.get("emotion_volatility", 0)
        if emotion_volatility < 2:
            score -= 10
        
        oral_level = style.get("oral_level", 0)
        if oral_level > 0.05:
            score += 10
        
        personal_count = style.get("personal_marker_count", 0)
        if personal_count > 2:
            score += 15
        
        semantic = analysis_result.get("semantic", {})
        detail_count = semantic.get("detail_count", 0)
        if detail_count > 3:
            score += 10
        
        return max(0, min(100, score))


class DeepOptimizer:
    """Deep Optimization Engine"""
    
    def __init__(self):
        self.oral_replacements = {
            '但是': ['不过', '可是', '但话说回来'],
            '因此': ['所以', '这样一来', '结果'],
            '然而': ['可', '不过', '但'],
            '首先': ['一开始', '最开始', '先说'],
            '其次': ['然后', '接下来', '再说'],
            '最后': ['到头来', '最终', '末了']
        }
        
        self.emotion_variations = {
            '开心': ['高兴', '兴奋', '愉悦', '欣喜'],
            '难过': ['伤心', '沮丧', '低落', '郁闷'],
            '愤怒': ['生气', '恼火', '气愤', '不爽'],
            '感动': ['触动', '打动', '感染', '震撼']
        }
        
    def optimize_text(self, text: str, analysis_result: Dict) -> str:
        """Deep optimize text"""
        optimized = text
        
        optimized = self._alternate_voice(optimized)
        optimized = self._mix_sentence_length(optimized)
        optimized = self._oral_replacement(optimized)
        optimized = self._diversify_emotions(optimized)
        optimized = self._break_regularity(optimized)
        optimized = self._add_details(optimized)
        optimized = self._enhance_personal_style(optimized)
        
        return optimized
    
    def _alternate_voice(self, text: str) -> str:
        """Alternate active and passive voice"""
        sentences = re.split(r'([。！？\n])', text)
        result = []
        
        for i, sentence in enumerate(sentences):
            if i % 4 == 2 and len(sentence) > 10:
                if '把' in sentence:
                    sentence = sentence.replace('把', '被')
            result.append(sentence)
        
        return ''.join(result)
    
    def _mix_sentence_length(self, text: str) -> str:
        """Mix long and short sentences"""
        sentences = re.split(r'([。！？\n])', text)
        result = []
        
        for i, sentence in enumerate(sentences):
            if len(sentence) > 30 and i % 3 == 1:
                if '，' in sentence:
                    parts = sentence.split('，')
                    if len(parts) >= 3:
                        sentence = '，'.join(parts[:2]) + '。' + '，'.join(parts[2:])
            result.append(sentence)
        
        return ''.join(result)
    
    def _oral_replacement(self, text: str) -> str:
        """Oral style replacement"""
        for formal, oral_list in self.oral_replacements.items():
            if formal in text:
                replacement = random.choice(oral_list)
                text = text.replace(formal, replacement, 1)
        return text
    
    def _diversify_emotions(self, text: str) -> str:
        """Diversify emotion words"""
        for emotion, variations in self.emotion_variations.items():
            if emotion in text:
                replacement = random.choice(variations)
                text = text.replace(emotion, replacement, 1)
        return text
    
    def _break_regularity(self, text: str) -> str:
        """Break regular structure"""
        if random.random() < 0.3:
            markers = ['嗯', '其实', '说实话', '讲真']
            text = random.choice(markers) + '，' + text
        
        if random.random() < 0.2:
            interjections = ['啊', '哦', '哈']
            text = text + '！' + random.choice(interjections)
        
        return text
    
    def _add_details(self, text: str) -> str:
        """Add specific details"""
        if random.random() < 0.3:
            numbers = ['三', '五', '七', '十', '几十']
            text = text.replace('很多', f'{random.choice(numbers)}个')
        
        if random.random() < 0.2:
            examples = ['比如', '例如', '就像']
            text = text + '，' + random.choice(examples) + '上次我遇到的情况就是这样'
        
        return text
    
    def _enhance_personal_style(self, text: str) -> str:
        """Enhance personal style"""
        if random.random() < 0.4:
            markers = ['我觉得', '在我看来', '我个人认为', '以我的经验']
            text = random.choice(markers) + '，' + text
        
        if random.random() < 0.2:
            experiences = ['记得有一次', '之前遇到', '我有个朋友']
            text = text + '。' + random.choice(experiences) + '也遇到过类似情况'
        
        return text


class RealTimeMonitor:
    """Real-time Monitoring Module"""
    
    def __init__(self, detector: MultiDimensionDetector, 
                 scorer: IntelligentScoringEngine,
                 optimizer: DeepOptimizer):
        self.detector = detector
        self.scorer = scorer
        self.optimizer = optimizer
        self.history = []
        self.threshold = 60
        
    def monitor_text(self, text: str, auto_optimize: bool = True) -> Dict:
        """Real-time text monitoring"""
        start_time = time.time()
        
        analysis = self.detector.full_analysis(text)
        score = self.scorer.calculate_score(analysis)
        
        warnings = []
        if score < self.threshold:
            warnings.append(f"AI features detected, score: {score}")
        
        optimized_text = text
        optimization_effect = None
        if auto_optimize and score < self.threshold:
            optimized_text = self.optimizer.optimize_text(text, analysis)
            
            new_analysis = self.detector.full_analysis(optimized_text)
            new_score = self.scorer.calculate_score(new_analysis)
            optimization_effect = {
                "original_score": score,
                "new_score": new_score,
                "improvement": new_score - score
            }
        
        record = {
            "timestamp": time.time(),
            "original_text": text,
            "score": score,
            "warnings": warnings,
            "optimized": auto_optimize and score < self.threshold,
            "optimization_effect": optimization_effect,
            "processing_time": time.time() - start_time
        }
        self.history.append(record)
        
        return {
            "score": score,
            "analysis": analysis,
            "warnings": warnings,
            "optimized_text": optimized_text,
            "optimization_effect": optimization_effect,
            "processing_time": time.time() - start_time
        }
    
    def get_statistics(self) -> Dict:
        """Get monitoring statistics"""
        if not self.history:
            return {"total_checks": 0}
        
        scores = [r["score"] for r in self.history]
        return {
            "total_checks": len(self.history),
            "average_score": sum(scores) / len(scores),
            "min_score": min(scores),
            "max_score": max(scores),
            "optimization_count": sum(1 for r in self.history if r["optimized"]),
            "warning_count": sum(len(r["warnings"]) for r in self.history)
        }
    
    def get_recent_alerts(self, count: int = 5) -> List[Dict]:
        """Get recent alerts"""
        alerts = [r for r in self.history if r["warnings"]]
        return alerts[-count:]


class NWACS_V4:
    """NWACS V8.0 AI Detector V4"""
    
    def __init__(self):
        self.detector = MultiDimensionDetector()
        self.scorer = IntelligentScoringEngine()
        self.optimizer = DeepOptimizer()
        self.monitor = RealTimeMonitor(self.detector, self.scorer, self.optimizer)
        
    def analyze_text(self, text: str, auto_optimize: bool = True) -> Dict:
        """Complete text analysis"""
        return self.monitor.monitor_text(text, auto_optimize)
    
    def batch_analyze(self, texts: List[str]) -> List[Dict]:
        """Batch analyze texts"""
        results = []
        for text in texts:
            result = self.analyze_text(text)
            results.append(result)
        return results
    
    def get_system_status(self) -> Dict:
        """Get system status"""
        return {
            "version": "V4.0",
            "components": {
                "detector": "MultiDimensionDetector",
                "scorer": "IntelligentScoringEngine",
                "optimizer": "DeepOptimizer",
                "monitor": "RealTimeMonitor"
            },
            "statistics": self.monitor.get_statistics()
        }


if __name__ == "__main__":
    nwacs = NWACS_V4()
    
    test_text = """
    首先，我们需要分析这个问题。其次，我们要考虑多个因素。最后，我们可以得出结论。
    这个系统具有很多优点，但是也存在一些问题。因此，我们需要进一步研究。
    综上所述，这个方案是可行的，但是还需要完善。
    """
    
    result = nwacs.analyze_text(test_text, auto_optimize=True)
    
    print("=" * 50)
    print("NWACS V8.0 - AI Detector V4")
    print("=" * 50)
    print(f"\nOriginal Text Score: {result['score']}/100")
    
    if result['warnings']:
        print("\nWarnings:")
        for warning in result['warnings']:
            print(f"  - {warning}")
    
    if result['optimization_effect']:
        effect = result['optimization_effect']
        print(f"\nOptimization Effect:")
        print(f"  Original Score: {effect['original_score']}")
        print(f"  Optimized Score: {effect['new_score']}")
        print(f"  Improvement: +{effect['improvement']} points")
    
    print(f"\nOptimized Text:")
    print(result['optimized_text'])
    
    print(f"\nProcessing Time: {result['processing_time']:.3f}s")
    
    print("\n" + "=" * 50)
    print("System Status:")
    status = nwacs.get_system_status()
    print(json.dumps(status, ensure_ascii=False, indent=2))
