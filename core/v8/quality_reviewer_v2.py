#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS V8.0 质量检测系统 V2
由DeepSeek联网升级优化
升级时间：2026-05-03 13:33:11
"""

我来为您生成完整的NWACS V8.0系统升级版质量检测系统代码：

```python
import re
import json
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum
from collections import Counter

class QualityLevel(Enum):
    S = "S级(90+)"
    A = "A级(80+)"
    B = "B级(70+)"
    C = "C级(60+)"
    D = "D级(<60)"

@dataclass
class QualityReport:
    """质量检测报告"""
    total_score: float = 0.0
    logic_score: float = 0.0
    consistency_score: float = 0.0
    literary_score: float = 0.0
    readability_score: float = 0.0
    innovation_score: float = 0.0
    market_score: float = 0.0
    quality_level: QualityLevel = QualityLevel.D
    issues: List[Dict] = field(default_factory=list)
    suggestions: List[Dict] = field(default_factory=list)
    detailed_analysis: Dict = field(default_factory=dict)

class NWACS_V8:
    """NWACS V8.0 质量检测系统"""
    
    def __init__(self):
        self.max_score = 100
        self.weights = {
            "logic": 0.20,
            "consistency": 0.20,
            "literary": 0.20,
            "readability": 0.20,
            "innovation": 0.10,
            "market": 0.10
        }
        
        # 初始化检测引擎
        self.logic_engine = LogicEngine()
        self.consistency_engine = ConsistencyEngine()
        self.literary_engine = LiteraryEngine()
        self.readability_engine = ReadabilityEngine()
        self.innovation_engine = InnovationEngine()
        self.market_engine = MarketEngine()
        
        # 改进建议模板
        self.suggestion_templates = self._init_suggestion_templates()
    
    def _init_suggestion_templates(self) -> Dict:
        """初始化改进建议模板"""
        return {
            "logic": {
                "causality": "因果关系不够清晰，建议补充过渡情节或解释",
                "timeline": "时间线存在矛盾，请检查事件顺序",
                "spatial": "空间逻辑存在问题，建议统一场景描述"
            },
            "consistency": {
                "character": "角色性格出现不一致，建议保持角色行为逻辑",
                "world": "世界观规则被打破，请检查设定一致性",
                "plot": "前后剧情存在矛盾，建议梳理情节发展"
            },
            "literary": {
                "language": "语言表达可以更优美，建议使用更丰富的修辞手法",
                "description": "描写不够生动，建议增加感官细节",
                "emotion": "情感表达不够真挚，建议深化情感描写"
            },
            "readability": {
                "rhythm": "节奏把控可以更好，建议调整段落长度",
                "hook": "缺少吸引人的钩子，建议在关键位置设置悬念",
                "highlight": "爽点安排不够合理，建议优化高潮部分"
            },
            "innovation": {
                "plot": "情节创新度不足，建议加入独特元素",
                "character": "人物设定较为常见，建议增加特色",
                "setting": "世界观设定缺乏新意，建议创新"
            },
            "market": {
                "acceptance": "读者接受度可能不高，建议调整内容方向",
                "platform": "平台适配性不足，建议了解平台偏好",
                "value": "商业价值有待提升，建议优化变现点"
            }
        }
    
    def analyze_text(self, text: str, context: Optional[Dict] = None) -> QualityReport:
        """分析文本质量"""
        report = QualityReport()
        
        # 1. 逻辑性检测
        logic_result = self.logic_engine.analyze(text)
        report.logic_score = logic_result["score"]
        report.detailed_analysis["logic"] = logic_result["details"]
        
        # 2. 一致性检测
        consistency_result = self.consistency_engine.analyze(text, context)
        report.consistency_score = consistency_result["score"]
        report.detailed_analysis["consistency"] = consistency_result["details"]
        
        # 3. 文学性检测
        literary_result = self.literary_engine.analyze(text)
        report.literary_score = literary_result["score"]
        report.detailed_analysis["literary"] = literary_result["details"]
        
        # 4. 可读性检测
        readability_result = self.readability_engine.analyze(text)
        report.readability_score = readability_result["score"]
        report.detailed_analysis["readability"] = readability_result["details"]
        
        # 5. 创新性检测
        innovation_result = self.innovation_engine.analyze(text, context)
        report.innovation_score = innovation_result["score"]
        report.detailed_analysis["innovation"] = innovation_result["details"]
        
        # 6. 市场性检测
        market_result = self.market_engine.analyze(text)
        report.market_score = market_result["score"]
        report.detailed_analysis["market"] = market_result["details"]
        
        # 计算总分
        report.total_score = self._calculate_total_score(report)
        
        # 确定等级
        report.quality_level = self._determine_level(report.total_score)
        
        # 生成问题和建议
        report.issues = self._collect_issues(report)
        report.suggestions = self._generate_suggestions(report)
        
        return report
    
    def _calculate_total_score(self, report: QualityReport) -> float:
        """计算总分"""
        total = (
            report.logic_score * self.weights["logic"] +
            report.consistency_score * self.weights["consistency"] +
            report.literary_score * self.weights["literary"] +
            report.readability_score * self.weights["readability"] +
            report.innovation_score * self.weights["innovation"] +
            report.market_score * self.weights["market"]
        )
        return round(total, 2)
    
    def _determine_level(self, score: float) -> QualityLevel:
        """确定质量等级"""
        if score >= 90:
            return QualityLevel.S
        elif score >= 80:
            return QualityLevel.A
        elif score >= 70:
            return QualityLevel.B
        elif score >= 60:
            return QualityLevel.C
        else:
            return QualityLevel.D
    
    def _collect_issues(self, report: QualityReport) -> List[Dict]:
        """收集所有问题"""
        issues = []
        
        # 检查各维度问题
        dimension_checks = [
            ("logic", report.logic_score, "逻辑性"),
            ("consistency", report.consistency_score, "一致性"),
            ("literary", report.literary_score, "文学性"),
            ("readability", report.readability_score, "可读性"),
            ("innovation", report.innovation_score, "创新性"),
            ("market", report.market_score, "市场性")
        ]
        
        for dim, score, name in dimension_checks:
            if score < 60:
                issues.append({
                    "dimension": dim,
                    "name": name,
                    "severity": "high",
                    "score": score,
                    "description": f"{name}得分较低({score}分)，需要重点改进"
                })
            elif score < 75:
                issues.append({
                    "dimension": dim,
                    "name": name,
                    "severity": "medium",
                    "score": score,
                    "description": f"{name}有待提升({score}分)"
                })
        
        return issues
    
    def _generate_suggestions(self, report: QualityReport) -> List[Dict]:
        """生成改进建议"""
        suggestions = []
        priority = 0
        
        # 根据各维度得分生成建议
        for dim, score in [
            ("logic", report.logic_score),
            ("consistency", report.consistency_score),
            ("literary", report.literary_score),
            ("readability", report.readability_score),
            ("innovation", report.innovation_score),
            ("market", report.market_score)
        ]:
            if score < 70:
                priority += 1
                templates = self.suggestion_templates[dim]
                
                # 根据具体问题选择建议
                for issue_type, suggestion in templates.items():
                    suggestions.append({
                        "dimension": dim,
                        "priority": priority,
                        "issue_type": issue_type,
                        "suggestion": suggestion,
                        "example": self._get_example(dim, issue_type)
                    })
        
        # 按优先级排序
        suggestions.sort(key=lambda x: x["priority"])
        
        return suggestions
    
    def _get_example(self, dimension: str, issue_type: str) -> str:
        """获取改进示例"""
        examples = {
            "logic": {
                "causality": "示例：'因为...所以...'结构，确保事件有明确的因果联系",
                "timeline": "示例：使用时间标记词如'三天后'、'与此同时'保持时间线清晰",
                "spatial": "示例：保持场景描述的一致性，如'从东门进入'后不应突然出现在西侧"
            },
            "consistency": {
                "character": "示例：角色性格应保持一致，如设定为'冷静'的角色不应突然暴躁",
                "world": "示例：魔法世界应保持规则一致，如'火球术'每次使用效果应相同",
                "plot": "示例：检查前后剧情是否矛盾，如角色不应同时出现在两个地方"
            },
            "literary": {
                "language": "示例：'夕阳如血'比'太阳很红'更具文学性",
                "description": "示例：'空气中飘来桂花的甜香'比'有桂花香'更生动",
                "emotion": "示例：'他紧握的双拳微微颤抖'比'他很生气'更富情感"
            },
            "readability": {
                "rhythm": "示例：紧张场景用短句，抒情场景用长句",
                "hook": "示例：章节结尾设置悬念，如'门后站着的人让他震惊'",
                "highlight": "示例：每3-5章设置一个小高潮，10章一个大高潮"
            },
            "innovation": {
                "plot": "示例：在传统修仙体系中加入科技元素",
                "character": "示例：创造具有独特能力或背景的角色",
                "setting": "示例：设计与众不同的世界观，如'情绪魔法'体系"
            },
            "market": {
                "acceptance": "示例：了解目标读者群体的阅读偏好",
                "platform": "示例：根据平台特点调整更新频率和章节长度",
                "value": "示例：设计合理的付费点和互动环节"
            }
        }
        
        return examples.get(dimension, {}).get(issue_type, "暂无示例")

class LogicEngine:
    """逻辑性检测引擎"""
    
    def analyze(self, text: str) -> Dict:
        """分析逻辑性"""
        score = 100
        details = {
            "causality": self._check_causality(text),
            "timeline": self._check_timeline(text),
            "spatial": self._check_spatial(text)
        }
        
        # 根据检测结果扣分
        for check_name, check_result in details.items():
            if not check_result["passed"]:
                score -= check_result["deduction"]
        
        return {"score": max(0, score), "details": details}
    
    def _check_causality(self, text: str) -> Dict:
        """检查因果关系"""
        issues = []
        deduction = 0
        
        # 检测因果连接词使用
        cause_effect_patterns = [
            (r'因为.*所以', '因果逻辑清晰'),
            (r'由于.*因此', '因果逻辑清晰'),
            (r'导致', '因果逻辑清晰')
        ]
        
        cause_count = 0
        for pattern, _ in cause_effect_patterns:
            cause_count += len(re.findall(pattern, text))
        
        if cause_count < 2:
            issues.append("因果关系表达不足")
            deduction = 15
        
        return {
            "passed": deduction < 10,
            "issues": issues,
            "deduction": deduction,
            "cause_count": cause_count
        }
    
    def _check_timeline(self, text: str) -> Dict:
        """检查时间线"""
        issues = []
        deduction = 0
        
        # 检查时间标记词
        time_markers = ['昨天', '今天', '明天', '上午', '下午', '晚上', '小时后', '天后']
        marker_count = sum(1 for marker in time_markers if marker in text)
        
        if marker_count < 3:
            issues.append("时间标记不足")
            deduction = 10
        
        # 检查时间矛盾
        time_conflicts = self._detect_time_conflicts(text)
        if time_conflicts:
            issues.extend(time_conflicts)
            deduction += 15
        
        return {
            "passed": deduction < 10,
            "issues": issues,
            "deduction": deduction,
            "marker_count": marker_count
        }
    
    def _detect_time_conflicts(self, text: str) -> List[str]:
        """检测时间矛盾"""
        conflicts = []
        
        # 简单的矛盾检测
        if '同时' in text and '第二天' in text:
            context = text[text.find('同时'):text.find('同时')+100]
            if '第二天' in context:
                conflicts.append("'同时'和'第二天'可能存在时间矛盾")
        
        return conflicts
    
    def _check_spatial(self, text: str) -> Dict:
        """检查空间逻辑"""
        issues = []
        deduction = 0
        
        # 检查空间描述一致性
        location_patterns = [
            (r'进入.*房间', '进入'),
            (r'走出.*房间', '走出'),
            (r'来到.*地方', '移动')
        ]
        
        location_changes = []
        for pattern, action in location_patterns:
            matches = re.findall(pattern, text)
            location_changes.extend([(action, match) for match in matches])
        
        if len(location_changes) > 5:
            issues.append("场景切换过于频繁")
            deduction = 10
        
        return {
            "passed": deduction < 10,
            "issues": issues,
            "deduction": deduction,
            "location_changes": len(location_changes)
        }

class ConsistencyEngine:
    """一致性检测引擎"""
    
    def analyze(self, text: str, context: Optional[Dict] = None) -> Dict:
        """分析一致性"""
        score = 100
        details = {
            "character": self._check_character_consistency(text, context),
            "world": self._check_world_consistency(text, context),
            "plot": self._check_plot_consistency(text)
        }
        
        for check_name, check_result in details.items():
            if not check_result["passed"]:
                score -= check_result["deduction"]
        
        return {"score": max(0, score), "details": details}
    
    def _check_character_consistency(self, text: str, context: Optional[Dict]) -> Dict:
        """检查角色一致性"""
        issues = []
        deduction = 0
        
        # 检查角色行为一致性
        if context and "character_traits" in context:
            for char, traits in context["character_traits"].items():
                if char in text:
                    for trait in traits:
                        if trait["type"] == "personality":
                            # 检查性格一致性
                            if not self._verify_personality_consistency(text, char, trait["value"]):
                                issues.append(f"角色'{char}'的性格'{trait['value']}'存在不一致")
                                deduction += 10
        
        return {
            "passed": deduction < 10,
            "issues": issues,
            "deduction": deduction
        }
    
    def _verify_personality_consistency(self, text: str, character: str, personality: str) -> bool:
        """验证角色性格一致性"""
        # 简单的一致性检查
        if personality == "冷静":
            emotional_words = ['愤怒', '激动', '暴躁', '冲动']
            for word in emotional_words:
                if word in text and character in text:
                    return False
        return True
    
    def _check_world_consistency(self, text: str, context: Optional[Dict]) -> Dict:
        """检查世界观一致性"""
        issues = []
        deduction = 0
        
        if context and "world_rules" in context:
            for rule in context["world_rules"]:
                if rule["type"] == "magic" and "魔法" in text:
                    if not self._verify_magic_rules(text, rule["rules"]):
                        issues.append(f"魔法规则'{rule['name']}'被违反")
                        deduction += 15
        
        return {
            "passed": deduction < 10,
            "issues": issues,
            "deduction": deduction
        }
    
    def _verify_magic_rules(self, text: str, rules: List[str]) -> bool:
        """验证魔法规则"""
        # 简单的规则验证
        for rule in rules:
            if "限制" in rule and "无限" in text:
                return False
        return True
    
    def _check_plot_consistency(self, text: str) -> Dict:
        """检查剧情一致性"""
        issues = []
        deduction = 0
        
        # 检查关键事件重复
        events = re.findall(r'[。！？]', text)
        if len(events) > 100:
            # 检查是否有重复事件描述
            sentences = re.split(r'[。！？]', text)
            for i in range(len(sentences)-1):
                if sentences[i] and sentences[i+1]:
                    similarity = self._calculate_similarity(sentences[i], sentences[i+1])
                    if similarity > 0.8:
                        issues.append(f"存在相似事件描述: '{sentences[i][:20]}...'")
                        deduction += 10
                        break
        
        return {
            "passed": deduction < 10,
            "issues": issues,
            "deduction": deduction
        }
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """计算文本相似度"""
        # 简单的基于词袋的相似度计算
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1 & words2
        union = words1 | words2
        
        return len(intersection) / len(union)

class LiteraryEngine:
    """文学性检测引擎"""
    
    def analyze(self, text: str) -> Dict:
        """分析文学性"""
        score = 100
        details = {
            "language": self._check_language_quality(text),
            "description": self._check_description_quality(text),
            "emotion": self._check_emotional_expression(text)
        }
        
        for check_name, check_result in details.items():
            if not check_result["passed"]:
                score -= check_result["deduction"]
        
        return {"score": max(0, score), "details": details}
    
    def _check_language_quality(self, text: str) -> Dict:
        """检查语言质量"""
        issues = []
        deduction = 0
        
        # 检查修辞手法使用
        rhetorical_devices = {
            '比喻': ['像', '如同', '仿佛', '似'],
            '拟人': ['仿佛', '好像', '似乎'],
            '排比': ['是', '有', '在']
        }
        
        device_count = 0
        for device, markers in rhetorical_devices.items():
            for marker in markers:
                device_count += text.count(marker)
        
        if device_count < 5:
            issues.append(f"修辞手法使用不足(当前{device_count}处)")
            deduction = 15
        
        # 检查词汇丰富度
        words = text.split()
        unique_words = len(set(words))
        if unique_words < 50:
            issues.append("词汇量不足")
            deduction += 10
        
        return {
            "passed": deduction < 10,
            "issues": issues,
            "deduction": deduction,
            "device_count": device_count,
            "unique_words": unique_words
        }
    
    def _check_description_quality(self, text: str) -> Dict:
        """检查描写质量"""
        issues = []
        deduction = 0
        
        # 检查感官描写
        sensory_words = {
            '视觉': ['看到', '看见', '呈现', '展现'],
            '听觉': ['听到', '听见', '声音', '声响'],
            '嗅觉': ['闻到', '气味', '香味', '臭味'],
            '触觉': ['触摸', '感觉', '触感', '温度'],
            '味觉': ['品尝', '味道', '滋味', '口感']
        }
        
        sensory_count = 0
        for sense, words in sensory_words.items():
            for word in words:
                sensory_count += text.count(word)
        
        if sensory_count < 3:
            issues.append("感官描写不足")
            deduction = 15
        
        # 检查细节描写
        detail_patterns = [r'的.*的', r'着', r'了']
        detail_count = sum(len(re.findall(pattern, text)) for pattern in detail_patterns)
        
        if detail_count < 10:
            issues.append("细节描写不够丰富")
            deduction += 10
        
        return {
            "passed": deduction < 10,
            "issues": issues,
            "deduction": deduction,
            "sensory_count": sensory_count,
            "detail_count": detail_count
        }
    
    def _check_emotional_expression(self, text: str) -> Dict:
        """检查情感表达"""
        issues = []
        deduction = 0
        
        # 检查情感词汇
        emotion_words = {
            '喜悦': ['开心', '快乐', '高兴', '喜悦', '欢喜'],
            '悲伤': ['悲伤', '伤心', '难过', '痛苦', '哀伤'],
            '愤怒': ['愤怒', '生气', '恼怒', '气愤', '暴怒'],
            '恐惧': ['恐惧', '害怕', '惊慌', '惊恐', '畏惧'],
            '惊讶': ['惊讶', '惊奇', '震惊', '诧异', '意外']
        }
        
        emotion_count = 0
        for emotion, words in emotion_words.items():
            for word in words:
                emotion_count += text.count(word)
        
        if emotion_count < 2:
            issues.append("情感表达不足")
            deduction = 15
        
        # 检查情感描写深度
        deep_emotion_patterns = [
            r'心中[的].*[感]',
            r'内心[深处]',
            r'情绪[波动]'
        ]
        
        deep_count = sum(len(re.findall(pattern, text)) for pattern in deep_emotion_patterns)
        if deep_count < 1:
            issues.append("情感描写缺乏深度")
            deduction += 10
        
        return {
            "passed": deduction < 10,
            "issues": issues,
            "deduction": deduction,
            "emotion_count": emotion_count,
            "deep_count": deep_count
        }

class ReadabilityEngine:
    """可读性检测引擎"""
    
    def analyze(self, text: str) -> Dict:
        """分析可读性"""
        score = 100
        details = {
            "rhythm": self._check_rhythm(text),
            "hook": self._check_hooks(text),
            "highlight": self._check_highlights(text)
        }
        
        for check_name, check_result in details.items():
            if not check_result["passed"]:
                score -= check_result["deduction"]
        
        return {"score": max(0, score), "details": details}
    
    def _check_rhythm(self, text: str) -> Dict:
        """检查节奏"""
        issues = []
        deduction = 0
        
        # 检查段落长度
        paragraphs = text.split('\n')
        avg_para_length = sum(len(p) for p in paragraphs) / max(len(paragraphs), 1)
        
        if avg_para_length > 500:
            issues.append("段落过长，建议适当分段")
            deduction = 10
        elif avg_para_length < 50:
            issues.append("段落过短，影响阅读流畅性")
            deduction = 5
        
        # 检查句子长度变化
        sentences = re.split(r'[。！？]', text)
        sentence_lengths = [len(s) for s in sentences if s.strip()]
        
        if sentence_lengths:
            max_len = max(sentence_lengths)
            min_len = min(sentence_lengths)
            if max_len - min_len < 10:
                issues.append("句子长度变化不足，节奏单一")
                deduction += 10
        
        return {
            "passed": deduction < 10,
            "issues": issues,
            "deduction": deduction,
            "avg_para_length": avg_para_length
        }
    
    def _check_hooks(self, text: str) -> Dict:
        """检查钩子设置"""
        issues = []
        deduction = 0
        
        # 检查悬念设置
        hook_patterns = [
            r'突然',
            r'竟然',
            r'没想到',
            r'究竟',
            r'到底',
            r'悬念'
        ]
        
        hook_count = sum(len(re.findall(pattern, text)) for pattern in hook_patterns)
        
        if hook_count < 2:
            issues.append("悬念设置不足")
            deduction = 15
        
        # 检查章节结尾
        if len(text) > 1000:
            last_100 = text[-100:]
            if not any(pattern in last_100 for pattern in ['？', '！', '...', '——']):
                issues.append("章节结尾缺乏悬念")
                deduction += 10
        
        return {
            "passed": deduction < 10,
            "issues": issues,
            "deduction": deduction,
            "hook_count": hook_count
        }
    
    def _check_highlights(self, text: str) -> Dict:
        """检查爽点安排"""
        issues = []
        deduction = 0
        
        # 检查高潮点
        highlight_patterns = [
            r'终于',
            r'成功',
            r'胜利',
            r'突破',
            r'升级',
            r'获得'
        ]
        
        highlight_count = sum(len(re.findall(pattern, text)) for pattern in highlight_patterns)
        
        if highlight_count < 3:
            issues.append("爽点安排不足")
            deduction = 15
        
        # 检查高潮分布
        if len(text) > 2000:
            first_half = text[:len(text)//2]
            second_half = text[len(text)//2:]
            
            first_highlights = sum(len(re.findall(pattern, first_half)) for pattern in highlight_patterns)
            second_highlights = sum(len(re.findall(pattern, second_half)) for pattern in highlight_patterns)
            
            if second_highlights < first_highlights:
                issues.append("高潮分布不均匀，后半部分缺乏爽点")
                deduction += 10
        
        return {
            "passed": deduction < 10,
            "issues": issues,
            "deduction": deduction,
            "highlight_count": highlight_count
        }

class InnovationEngine:
    """创新性检测引擎"""
    
    def analyze(self, text: str, context: Optional[Dict] = None) -> Dict:
        """分析创新性"""
        score = 100
        details = {
            "plot": self._check_plot_innovation(text),
            "character": self._check_character_innovation(text),
            "setting": self._check_setting_innovation(text, context)
        }
        
        for check_name, check_result in details.items():
            if not check_result["passed"]:
                score -= check_result["deduction"]
        
        return {"score": max(0, score), "details": details}
    
    def _check_plot_innovation(self, text: str) -> Dict:
        """检查情节创新"""
        issues = []
        deduction = 0
        
        # 检测常见套路
        cliche_patterns = [
            r'穿越',
            r'重生',
            r'系统',
            r'金手指',
            r'退婚',
            r'废材'
        ]
        
        cliche_count = sum(len(re.findall(pattern, text)) for pattern in cliche_patterns)
        
        if cliche_count > 3:
            issues.append(f"使用{cliche_count}个常见套路，创新度不足")
            deduction = 15
        
        # 检测独特元素
        unique_patterns = [
            r'独创',
            r'独特',
            r'新颖',
            r'前所未有'
        ]
        
        unique_count = sum(len(re.findall(pattern, text)) for pattern in unique_patterns)
        
        if unique_count < 1:
            issues.append("缺乏独特元素")
            deduction += 10
        
        return {
            "passed": deduction < 10,
            "issues": issues,
            "deduction": deduction,
            "cliche_count": cliche_count,
            "unique_count": unique_count
        }
    
    def _check_character_innovation(self, text: str) -> Dict:
        """检查人物创新"""
        issues = []
        deduction = 0
        
        # 检测常见角色类型
        common_characters = [
            '主角', '配角', '反派', '女主', '男主'
        ]
        
        common_count = sum(text.count(char) for char in common_characters)
        
        if common_count > 10:
            issues.append("角色类型较为常见")
            deduction = 10
        
        # 检测角色特色
        unique_traits = [
            r'特殊能力',
            r'独特技能',
            r'与众不同',
            r'特别之处'
        ]
        
        trait_count = sum(len(re.findall(pattern, text)) for pattern in unique_traits)
        
        if trait_count < 1:
            issues.append("角色缺乏特色")
            deduction += 10
        
        return {
            "passed": deduction < 10,
            "issues": issues,
            "deduction": deduction,
            "common_count": common_count,
            "trait_count": trait_count
        }
    
    def _check_setting_innovation(self, text: str, context: Optional[Dict]) -> Dict:
        """检查设定创新"""
        issues = []
        deduction = 0
        
        # 检测常见世界观
        common_settings = [
            '修真', '魔法', '科幻', '末世', '古代'
        ]
        
        setting_count = sum(1 for setting in common_settings if setting in text)
        
        if setting_count > 2:
            issues.append("世界观设定较为常见")
            deduction = 10
        
        # 检测独特设定
        unique_settings = [
            r'独特[的]?世界',
            r'特殊[的]?规则',
            r'创新[的]?体系'
        ]
        
        unique_count = sum(len(re.findall(pattern, text)) for pattern in unique_settings)
        
        if unique_count < 1:
            issues.append("缺乏独特的世界观设定")
            deduction += 10
        
        return {
            "passed": deduction < 10,
            "issues": issues,
            "deduction": deduction,
            "setting_count": setting_count,
            "unique_count": unique_count
        }

class MarketEngine:
    """市场性检测引擎"""
    
    def analyze(self, text: str) -> Dict:
        """分析市场性"""
        score = 100
        details = {
            "acceptance": self._check_reader_acceptance(text),
            "platform": self._check_platform_compatibility(text),
            "value": self._check_commercial_value(text)
        }
        
        for check_name, check_result in details.items():
            if not check_result["passed"]:
                score -= check_result["deduction"]
        
        return {"score": max(0, score), "details": details}
    
    def _check_reader_acceptance(self, text: str) -> Dict:
        """检查读者接受度"""
        issues = []
        deduction = 0
        
        # 检测热门元素
        popular_elements = [
            '爽文', '甜文', '虐文', '搞笑', '热血'
        ]
        
        popular_count = sum(1 for element in popular_elements if element in text)
        
        if popular_count < 1:
            issues.append("缺乏热门元素")
            deduction = 10
        
        # 检测读者友好度
        friendly_patterns = [
            r'易懂',
            r'轻松',
            r'愉快',
            r'有趣'
        ]
        
        friendly_count = sum(len(re.findall(pattern, text)) for pattern in friendly_patterns)
        
        if friendly_count < 1:
            issues.append("可读性有待提升")
            deduction += 10
        
        return {
            "passed": deduction < 10,
            "issues": issues,
            "deduction": deduction,
            "popular_count": popular_count,
            "friendly_count": friendly_count
        }
    
    def _check_platform_compatibility(self, text: str) -> Dict:
        """检查平台适配性"""
        issues = []
        deduction = 0
        
        # 检查章节长度
        if len(text) > 5000:
            issues.append("章节过长，建议控制在2000-3000字")
            deduction = 10
        elif len(text) < 500:
            issues.append("章节过短，建议增加内容")
            deduction = 5
        
        # 检查更新频率相关
        update_markers = ['待续', '未完待续', '下章', '下一章']
        if not any(marker in text for marker in update_markers):
            issues.append("缺少章节结束标记")
            deduction += 5
        
        return {
            "passed": deduction < 10,
            "issues": issues,
            "deduction": deduction,
            "text_length": len(text)
        }
    
    def _check_commercial_value(self, text: str) -> Dict:
        """检查商业价值"""
        issues = []
        deduction = 0
        
        # 检测付费点
        payment_points = [
            r'VIP',
            r'付费',
            r'订阅',
            r'打赏',
            r'推荐'
        ]
        
        payment_count = sum(len(re.findall(pattern, text)) for pattern in payment_points)
        
        if payment_count < 1:
            issues.append("缺乏明确的付费点设计")
            deduction = 10
        
        # 检测互动元素
        interaction_elements = [
            r'投票',
            r'评论',
            r'互动',
            r'讨论'
        ]
        
        interaction_count = sum(len(re.findall(pattern, text)) for pattern in interaction_elements)
        
        if interaction_count < 1:
            issues.append("缺乏读者互动元素")
            deduction += 10
        
        return {
            "passed": deduction < 10,
            "issues": issues,
            "deduction": deduction,
            "payment_count": payment_count,
            "interaction_count": interaction_count
        }

def main():
    """主函数：演示系统使用"""
    # 创建检测系统实例
    system = NWACS_V8()
    
    # 示例文本
    sample_text = """
    李明站在窗前，望着远处的夕阳。他心中充满了复杂的情绪，既有对过去的怀念，也有对未来的期待。
    
    突然，门被推开了。他的好友张华冲了进来，脸上带着兴奋的表情。
    
    "李明，你猜我发现了什么？"张华激动地说。
    
    李明转过身，看着好友兴奋的样子，心中涌起一股暖流。他微笑着问道："什么好消息让你这么高兴？"
    
    "我找到了传说中的秘境入口！"张华压低声音说，"就在城外的古墓里。"
    
    李明的眼睛亮了起来。他知道那个传说，据说秘境里藏着远古时代的宝物和知识。
    
    "我们什么时候去？"李明问道，声音里带着一丝急切。
    
    "今晚就去，"张华说，"趁其他人还不知道这个消息。"
    
    夜幕降临，两人悄悄离开了城市，向古墓的方向走去。月光下，他们的影子拉得很长，像是两个冒险者踏上了未知的旅程。
    """
    
    # 上下文信息
    context = {
        "character_traits": {
            "