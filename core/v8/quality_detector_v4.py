#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS V8.0 Quality Detector V4
Multi-dimensional quality assessment system
"""

import json
import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum
import math
from collections import defaultdict


class QualityLevel(Enum):
    S = "S-Level(Excellent)"
    A = "A-Level(Good)"
    B = "B-Level(Fair)"
    C = "C-Level(Pass)"
    D = "D-Level(Fail)"


@dataclass
class QualityDimension:
    name: str
    weight: float
    score: float = 0.0
    sub_items: List[str] = field(default_factory=list)
    issues: List[Dict] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)


@dataclass
class QualityReport:
    total_score: float = 0.0
    level: QualityLevel = QualityLevel.D
    dimensions: Dict[str, QualityDimension] = field(default_factory=dict)
    radar_data: Dict[str, float] = field(default_factory=dict)
    critical_issues: List[Dict] = field(default_factory=list)
    improvement_suggestions: List[Dict] = field(default_factory=list)
    passed_gate: bool = False


class NWACSQualitySystemV4:
    """NWACS V8.0 Quality Detection System V4"""
    
    def __init__(self, work_type: str = "novel"):
        self.work_type = work_type
        self.quality_gate = {
            "min_total_score": 60,
            "min_dimension_score": 40,
            "auto_block": True
        }
        self._init_default_weights()
        
    def _init_default_weights(self):
        self.weights = {
            "novel": {
                "Logic": 0.20,
                "Consistency": 0.20,
                "Literariness": 0.20,
                "Readability": 0.20,
                "Innovation": 0.10,
                "Marketability": 0.10
            },
            "essay": {
                "Logic": 0.25,
                "Consistency": 0.15,
                "Literariness": 0.25,
                "Readability": 0.20,
                "Innovation": 0.10,
                "Marketability": 0.05
            },
            "poetry": {
                "Logic": 0.10,
                "Consistency": 0.10,
                "Literariness": 0.35,
                "Readability": 0.20,
                "Innovation": 0.15,
                "Marketability": 0.10
            }
        }
        
    def analyze(self, text: str) -> QualityReport:
        report = QualityReport()
        
        self._analyze_logic(report, text)
        self._analyze_consistency(report, text)
        self._analyze_literariness(report, text)
        self._analyze_readability(report, text)
        self._analyze_innovation(report, text)
        self._analyze_marketability(report, text)
        
        report.total_score = self._calculate_total_score(report)
        report.level = self._determine_level(report.total_score)
        report.radar_data = self._generate_radar_data(report)
        report.improvement_suggestions = self._generate_improvement_suggestions(report)
        report.passed_gate = self._check_quality_gate(report)
        
        return report
    
    def _analyze_logic(self, report: QualityReport, text: str):
        dimension = QualityDimension(
            name="Logic",
            weight=self.weights.get(self.work_type, self.weights["novel"])["Logic"],
            sub_items=["Cause-Effect", "Timeline", "Space Logic", "Motivation"]
        )
        
        issues = []
        score = 100
        
        cause_effect_patterns = [
            (r'因为.*所以', 5),
            (r'由于.*因此', 5),
            (r'导致', 3),
            (r'结果', 3)
        ]
        cause_effect_score = self._check_patterns(text, cause_effect_patterns)
        
        time_patterns = [
            (r'\d{4}年', 3),
            (r'[上中下]午', 2),
            (r'[昨今明]天', 2),
            (r'[前后]来', 2)
        ]
        time_score = self._check_patterns(text, time_patterns)
        
        space_patterns = [
            (r'[东南西北]边', 2),
            (r'[上下左右]方', 2),
            (r'[内外前后]', 2)
        ]
        space_score = self._check_patterns(text, space_patterns)
        
        motive_patterns = [
            (r'为了', 3),
            (r'想要', 2),
            (r'打算', 2),
            (r'希望', 2)
        ]
        motive_score = self._check_patterns(text, motive_patterns)
        
        dimension.score = min(100, (cause_effect_score + time_score + space_score + motive_score) * 5)
        
        contradictions = self._find_contradictions(text)
        if contradictions:
            dimension.score -= len(contradictions) * 10
            issues.extend(contradictions)
        
        dimension.issues = issues
        report.dimensions["Logic"] = dimension
    
    def _analyze_consistency(self, report: QualityReport, text: str):
        dimension = QualityDimension(
            name="Consistency",
            weight=self.weights.get(self.work_type, self.weights["novel"])["Consistency"],
            sub_items=["Character", "World Rules", "Plot", "Details"]
        )
        
        issues = []
        score = 100
        
        character_consistency = self._check_character_consistency(text)
        if character_consistency["issues"]:
            score -= len(character_consistency["issues"]) * 15
            issues.extend(character_consistency["issues"])
        
        world_rules = self._check_world_rules(text)
        if world_rules["issues"]:
            score -= len(world_rules["issues"]) * 10
            issues.extend(world_rules["issues"])
        
        plot_consistency = self._check_plot_consistency(text)
        if plot_consistency["issues"]:
            score -= len(plot_consistency["issues"]) * 12
            issues.extend(plot_consistency["issues"])
        
        detail_consistency = self._check_detail_consistency(text)
        if detail_consistency["issues"]:
            score -= len(detail_consistency["issues"]) * 8
            issues.extend(detail_consistency["issues"])
        
        dimension.score = max(0, score)
        dimension.issues = issues
        report.dimensions["Consistency"] = dimension
    
    def _analyze_literariness(self, report: QualityReport, text: str):
        dimension = QualityDimension(
            name="Literariness",
            weight=self.weights.get(self.work_type, self.weights["novel"])["Literariness"],
            sub_items=["Language", "Description", "Emotion", "Atmosphere"]
        )
        
        score = 100
        issues = []
        
        beautiful_language = self._check_beautiful_language(text)
        score += beautiful_language["score"]
        if beautiful_language["issues"]:
            issues.extend(beautiful_language["issues"])
        
        vivid_description = self._check_vivid_description(text)
        score += vivid_description["score"]
        if vivid_description["issues"]:
            issues.extend(vivid_description["issues"])
        
        emotional_authenticity = self._check_emotional_authenticity(text)
        score += emotional_authenticity["score"]
        if emotional_authenticity["issues"]:
            issues.extend(emotional_authenticity["issues"])
        
        artistic_conception = self._check_artistic_conception(text)
        score += artistic_conception["score"]
        if artistic_conception["issues"]:
            issues.extend(artistic_conception["issues"])
        
        dimension.score = max(0, min(100, score))
        dimension.issues = issues
        report.dimensions["Literariness"] = dimension
    
    def _analyze_readability(self, report: QualityReport, text: str):
        dimension = QualityDimension(
            name="Readability",
            weight=self.weights.get(self.work_type, self.weights["novel"])["Readability"],
            sub_items=["Rhythm", "Hooks", "Pleasure Points", "Experience"]
        )
        
        score = 100
        issues = []
        
        rhythm_control = self._check_rhythm_control(text)
        score += rhythm_control["score"]
        if rhythm_control["issues"]:
            issues.extend(rhythm_control["issues"])
        
        hook_setting = self._check_hook_setting(text)
        score += hook_setting["score"]
        if hook_setting["issues"]:
            issues.extend(hook_setting["issues"])
        
        pleasure_points = self._check_pleasure_points(text)
        score += pleasure_points["score"]
        if pleasure_points["issues"]:
            issues.extend(pleasure_points["issues"])
        
        reading_experience = self._check_reading_experience(text)
        score += reading_experience["score"]
        if reading_experience["issues"]:
            issues.extend(reading_experience["issues"])
        
        dimension.score = max(0, min(100, score))
        dimension.issues = issues
        report.dimensions["Readability"] = dimension
    
    def _analyze_innovation(self, report: QualityReport, text: str):
        dimension = QualityDimension(
            name="Innovation",
            weight=self.weights.get(self.work_type, self.weights["novel"])["Innovation"],
            sub_items=["Plot", "Character", "Setting", "Expression"]
        )
        
        score = 50
        issues = []
        
        innovation_elements = self._check_innovation_elements(text)
        score += innovation_elements["score"]
        if innovation_elements["issues"]:
            issues.extend(innovation_elements["issues"])
        
        unique_expression = self._check_unique_expression(text)
        score += unique_expression["score"]
        if unique_expression["issues"]:
            issues.extend(unique_expression["issues"])
        
        dimension.score = max(0, min(100, score))
        dimension.issues = issues
        report.dimensions["Innovation"] = dimension
    
    def _analyze_marketability(self, report: QualityReport, text: str):
        dimension = QualityDimension(
            name="Marketability",
            weight=self.weights.get(self.work_type, self.weights["novel"])["Marketability"],
            sub_items=["Reader Acceptance", "Platform Fit", "Commercial Value", "Spread Potential"]
        )
        
        score = 50
        issues = []
        
        market_elements = self._check_market_elements(text)
        score += market_elements["score"]
        if market_elements["issues"]:
            issues.extend(market_elements["issues"])
        
        platform_adaptation = self._check_platform_adaptation(text)
        score += platform_adaptation["score"]
        if platform_adaptation["issues"]:
            issues.extend(platform_adaptation["issues"])
        
        dimension.score = max(0, min(100, score))
        dimension.issues = issues
        report.dimensions["Marketability"] = dimension
    
    def _calculate_total_score(self, report: QualityReport) -> float:
        total = 0.0
        for name, dimension in report.dimensions.items():
            total += dimension.score * dimension.weight
        return round(total, 2)
    
    def _determine_level(self, score: float) -> QualityLevel:
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
    
    def _generate_radar_data(self, report: QualityReport) -> Dict[str, float]:
        return {
            name: dimension.score
            for name, dimension in report.dimensions.items()
        }
    
    def _generate_improvement_suggestions(self, report: QualityReport) -> List[Dict]:
        suggestions = []
        
        for name, dimension in report.dimensions.items():
            if dimension.score < 60:
                suggestion = {
                    "dimension": name,
                    "current_score": dimension.score,
                    "priority": "High" if dimension.score < 40 else "Medium",
                    "issues": dimension.issues[:3],
                    "suggestions": self._get_improvement_suggestions(name, dimension)
                }
                suggestions.append(suggestion)
        
        suggestions.sort(key=lambda x: x["current_score"])
        
        return suggestions
    
    def _get_improvement_suggestions(self, dimension_name: str, dimension: QualityDimension) -> List[str]:
        suggestions_map = {
            "Logic": [
                "Strengthen cause-effect relationships",
                "Ensure timeline coherence",
                "Maintain spatial logic consistency",
                "Clarify character motivations"
            ],
            "Consistency": [
                "Keep character personalities consistent",
                "Follow world-building rules",
                "Check plot contradictions",
                "Maintain detail consistency"
            ],
            "Literariness": [
                "Enrich rhetorical devices",
                "Enhance vivid descriptions",
                "Deepen emotional expression",
                "Create unique atmosphere"
            ],
            "Readability": [
                "Adjust chapter rhythm",
                "Set more suspense hooks",
                "Arrange pleasure points reasonably",
                "Optimize reading flow"
            ],
            "Innovation": [
                "Try novel plot designs",
                "Create unique characters",
                "Innovate world settings",
                "Explore new expressions"
            ],
            "Marketability": [
                "Follow reader preference trends",
                "Adapt to platform requirements",
                "Enhance commercial value",
                "Increase shareability"
            ]
        }
        
        return suggestions_map.get(dimension_name, ["Focus on improving this dimension"])
    
    def _check_quality_gate(self, report: QualityReport) -> bool:
        if report.total_score < self.quality_gate["min_total_score"]:
            return False
        
        for dimension in report.dimensions.values():
            if dimension.score < self.quality_gate["min_dimension_score"]:
                return False
        
        return True
    
    def _check_patterns(self, text: str, patterns: List[Tuple[str, int]]) -> int:
        score = 0
        for pattern, weight in patterns:
            matches = re.findall(pattern, text)
            score += len(matches) * weight
        return score
    
    def _find_contradictions(self, text: str) -> List[Dict]:
        contradictions = []
        
        time_pattern = r'(\d{4})年'
        years = re.findall(time_pattern, text)
        if len(years) >= 2:
            if int(years[-1]) < int(years[0]):
                contradictions.append({
                    "type": "Time Contradiction",
                    "detail": f"Timeline confusion: {years[0]} -> {years[-1]}",
                    "severity": "High"
                })
        
        space_pattern = r'[东南西北]边'
        spaces = re.findall(space_pattern, text)
        if len(spaces) >= 4:
            if '东边' in spaces and '西边' in spaces:
                contradictions.append({
                    "type": "Space Contradiction",
                    "detail": "Simultaneous east and west descriptions",
                    "severity": "Medium"
                })
        
        return contradictions
    
    def _check_character_consistency(self, text: str) -> Dict:
        result = {"issues": [], "score": 0}
        
        character_pattern = r'[他她它]'
        characters = re.findall(character_pattern, text)
        
        if len(set(characters)) > 3:
            result["issues"].append({
                "type": "Character Pronoun Confusion",
                "detail": "Multiple character pronouns may confuse readers",
                "severity": "Medium"
            })
        
        return result
    
    def _check_world_rules(self, text: str) -> Dict:
        result = {"issues": [], "score": 0}
        
        rule_patterns = [
            (r'不能.*却', "Rule Contradiction"),
            (r'可以.*但.*不能', "Rule Conflict"),
            (r'必须.*却.*没有', "Rule Violation")
        ]
        
        for pattern, issue_type in rule_patterns:
            if re.search(pattern, text):
                result["issues"].append({
                    "type": issue_type,
                    "detail": f"Found inconsistent rule: {pattern}",
                    "severity": "High"
                })
        
        return result
    
    def _check_plot_consistency(self, text: str) -> Dict:
        result = {"issues": [], "score": 0}
        
        plot_turns = re.findall(r'突然|意外|转折', text)
        if len(plot_turns) > 5:
            result["issues"].append({
                "type": "Too Many Plot Turns",
                "detail": "Frequent plot turns may affect story coherence",
                "severity": "Medium"
            })
        
        return result
    
    def _check_detail_consistency(self, text: str) -> Dict:
        result = {"issues": [], "score": 0}
        
        numbers = re.findall(r'\d+', text)
        if len(numbers) > 10:
            for i in range(len(numbers) - 1):
                if abs(int(numbers[i]) - int(numbers[i+1])) > 1000:
                    result["issues"].append({
                        "type": "Number Contradiction",
                        "detail": f"Numbers {numbers[i]} and {numbers[i+1]} differ too much",
                        "severity": "Low"
                    })
        
        return result
    
    def _check_beautiful_language(self, text: str) -> Dict:
        result = {"issues": [], "score": 0}
        
        rhetoric_patterns = [
            (r'像.*一样', 2),
            (r'仿佛', 2),
            (r'如同', 2),
            (r'比喻', 1),
            (r'拟人', 1)
        ]
        
        rhetoric_score = self._check_patterns(text, rhetoric_patterns)
        result["score"] = rhetoric_score
        
        if rhetoric_score < 5:
            result["issues"].append({
                "type": "Insufficient Rhetoric",
                "detail": "Consider adding more rhetorical devices",
                "severity": "Low"
            })
        
        return result
    
    def _check_vivid_description(self, text: str) -> Dict:
        result = {"issues": [], "score": 0}
        
        sensory_patterns = [
            (r'看到|看见', 2),
            (r'听到|听见', 2),
            (r'闻到|嗅到', 2),
            (r'感到|感觉', 2),
            (r'触摸|触碰', 2)
        ]
        
        sensory_score = self._check_patterns(text, sensory_patterns)
        result["score"] = sensory_score
        
        if sensory_score < 8:
            result["issues"].append({
                "type": "Insufficient Sensory Description",
                "detail": "Add more sensory descriptions for immersion",
                "severity": "Medium"
            })
        
        return result
    
    def _check_emotional_authenticity(self, text: str) -> Dict:
        result = {"issues": [], "score": 0}
        
        emotion_patterns = [
            (r'高兴|快乐|开心', 2),
            (r'悲伤|难过|痛苦', 2),
            (r'愤怒|生气|恼火', 2),
            (r'恐惧|害怕|担忧', 2),
            (r'感动|温暖|幸福', 2)
        ]
        
        emotion_score = self._check_patterns(text, emotion_patterns)
        result["score"] = emotion_score
        
        if emotion_score < 6:
            result["issues"].append({
                "type": "Insufficient Emotional Expression",
                "detail": "Add more emotional descriptions for reader resonance",
                "severity": "Medium"
            })
        
        return result
    
    def _check_artistic_conception(self, text: str) -> Dict:
        result = {"issues": [], "score": 0}
        
        artistic_patterns = [
            (r'月光|星光|日光', 3),
            (r'微风|清风|和风', 3),
            (r'流水|溪水|河水', 3),
            (r'花开|花落|花谢', 3),
            (r'落叶|秋叶|枯叶', 3)
        ]
        
        artistic_score = self._check_patterns(text, artistic_patterns)
        result["score"] = artistic_score
        
        if artistic_score < 6:
            result["issues"].append({
                "type": "Insufficient Atmosphere",
                "detail": "Add more atmospheric descriptions",
                "severity": "Low"
            })
        
        return result
    
    def _check_rhythm_control(self, text: str) -> Dict:
        result = {"issues": [], "score": 0}
        
        paragraphs = text.split('\n')
        avg_paragraph_length = sum(len(p) for p in paragraphs) / max(len(paragraphs), 1)
        
        if avg_paragraph_length > 500:
            result["issues"].append({
                "type": "Paragraph Too Long",
                "detail": "Average paragraph too long, consider breaking up",
                "severity": "Medium"
            })
            result["score"] = -10
        elif avg_paragraph_length < 50:
            result["issues"].append({
                "type": "Paragraph Too Short",
                "detail": "Paragraphs too fragmented, consider merging",
                "severity": "Low"
            })
            result["score"] = -5
        else:
            result["score"] = 10
        
        return result
    
    def _check_hook_setting(self, text: str) -> Dict:
        result = {"issues": [], "score": 0}
        
        hook_patterns = [
            (r'为什么|怎么回事', 3),
            (r'突然|意外|不料', 3),
            (r'秘密|真相|谜团', 3),
            (r'究竟|到底', 2),
            (r'悬念|伏笔', 2)
        ]
        
        hook_score = self._check_patterns(text, hook_patterns)
        result["score"] = hook_score
        
        if hook_score < 8:
            result["issues"].append({
                "type": "Insufficient Suspense",
                "detail": "Add more suspense and hooks to engage readers",
                "severity": "High"
            })
        
        return result
    
    def _check_pleasure_points(self, text: str) -> Dict:
        result = {"issues": [], "score": 0}
        
        pleasure_patterns = [
            (r'成功|胜利|战胜', 3),
            (r'获得|得到|拥有', 3),
            (r'突破|超越|升级', 3),
            (r'复仇|反击|逆袭', 3),
            (r'惊喜|意外之喜', 2)
        ]
        
        pleasure_score = self._check_patterns(text, pleasure_patterns)
        result["score"] = pleasure_score
        
        if pleasure_score < 8:
            result["issues"].append({
                "type": "Insufficient Pleasure Points",
                "detail": "Add more satisfying moments for readers",
                "severity": "Medium"
            })
        
        return result
    
    def _check_reading_experience(self, text: str) -> Dict:
        result = {"issues": [], "score": 0}
        
        sentences = re.split(r'[。！？]', text)
        avg_sentence_length = sum(len(s) for s in sentences) / max(len(sentences), 1)
        
        if avg_sentence_length > 100:
            result["issues"].append({
                "type": "Sentence Too Long",
                "detail": "Average sentence too long, consider splitting",
                "severity": "Medium"
            })
            result["score"] = -10
        elif avg_sentence_length < 10:
            result["issues"].append({
                "type": "Sentence Too Short",
                "detail": "Sentences too brief, consider enriching",
                "severity": "Low"
            })
            result["score"] = -5
        else:
            result["score"] = 10
        
        return result
    
    def _check_innovation_elements(self, text: str) -> Dict:
        result = {"issues": [], "score": 0}
        
        innovation_patterns = [
            (r'创新|独特|新颖', 3),
            (r'前所未有|史无前例', 3),
            (r'突破|颠覆|革命', 3),
            (r'与众不同|别具一格', 2)
        ]
        
        innovation_score = self._check_patterns(text, innovation_patterns)
        result["score"] = innovation_score
        
        return result
    
    def _check_unique_expression(self, text: str) -> Dict:
        result = {"issues": [], "score": 0}
        
        unique_patterns = [
            (r'不是.*而是', 2),
            (r'与其.*不如', 2),
            (r'看似.*实则', 2),
            (r'虽然.*但是', 1)
        ]
        
        unique_score = self._check_patterns(text, unique_patterns)
        result["score"] = unique_score
        
        return result
    
    def _check_market_elements(self, text: str) -> Dict:
        result = {"issues": [], "score": 0}
        
        market_patterns = [
            (r'爱情|恋爱|感情', 2),
            (r'冒险|探索|发现', 2),
            (r'成长|蜕变|进化', 2),
            (r'战斗|对决|较量', 2),
            (r'友情|友谊|伙伴', 2)
        ]
        
        market_score = self._check_patterns(text, market_patterns)
        result["score"] = market_score
        
        if market_score < 6:
            result["issues"].append({
                "type": "Insufficient Market Elements",
                "detail": "Add popular elements for market appeal",
                "severity": "Medium"
            })
        
        return result
    
    def _check_platform_adaptation(self, text: str) -> Dict:
        result = {"issues": [], "score": 0}
        
        word_count = len(text)
        if word_count < 1000:
            result["issues"].append({
                "type": "Word Count Too Low",
                "detail": f"Current word count {word_count}, recommend 1000+",
                "severity": "High"
            })
            result["score"] = -20
        elif word_count > 10000:
            result["issues"].append({
                "type": "Word Count Too High",
                "detail": f"Current word count {word_count}, consider condensing",
                "severity": "Low"
            })
            result["score"] = -5
        else:
            result["score"] = 10
        
        return result
    
    def generate_report(self, report: QualityReport) -> str:
        output = []
        output.append("=" * 60)
        output.append(f"NWACS V8.0 Quality Detection Report (V4)")
        output.append("=" * 60)
        output.append(f"Work Type: {self.work_type}")
        output.append(f"Total Score: {report.total_score:.2f}")
        output.append(f"Level: {report.level.value}")
        output.append(f"Gate Status: {'Passed' if report.passed_gate else 'Failed'}")
        output.append("")
        
        output.append("[Six Dimensions Score]")
        for name, dimension in report.dimensions.items():
            bar = "=" * int(dimension.score / 10) + "-" * (10 - int(dimension.score / 10))
            output.append(f"{name}: {dimension.score:.1f} [{bar}]")
        
        output.append("")
        output.append("[Radar Data]")
        for name, value in report.radar_data.items():
            output.append(f"  {name}: {value:.1f}")
        
        if report.improvement_suggestions:
            output.append("")
            output.append("[Improvement Suggestions]")
            for suggestion in report.improvement_suggestions:
                output.append(f"\n[{suggestion['priority']} Priority] {suggestion['dimension']} (Current: {suggestion['current_score']:.1f})")
                if suggestion['issues']:
                    output.append("  Issues:")
                    for issue in suggestion['issues'][:2]:
                        output.append(f"    - {issue.get('detail', '')}")
                output.append("  Suggestions:")
                for s in suggestion['suggestions'][:3]:
                    output.append(f"    * {s}")
        
        output.append("")
        output.append("=" * 60)
        
        return "\n".join(output)


def main():
    qa_system = NWACSQualitySystemV4(work_type="novel")
    
    test_text = """
    叶青云站在山巅之上，俯瞰着脚下的云海。夕阳的余晖洒在他的身上，为他镀上了一层金色的光芒。
    他的眼中闪烁着坚定的光芒，内心充满了对未来的期待。这一路走来，他经历了无数的艰难险阻，
    但他从未放弃过自己的梦想。今天，他终于站在了这片大陆的巅峰，成为了真正的强者。
    """
    
    report = qa_system.analyze(test_text)
    report_text = qa_system.generate_report(report)
    print(report_text)
    
    return {
        "report": report,
        "report_text": report_text
    }


if __name__ == "__main__":
    result = main()
