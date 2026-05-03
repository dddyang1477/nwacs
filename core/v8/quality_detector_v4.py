#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS V8.0 质量检测器 V4
由DeepSeek联网深度优化升级
升级时间：2026-05-03 13:49:16
"""

我来为您生成NWACS V8.0系统的V4版本质量检测系统完整代码：

```python
import json
import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum
import math
from collections import defaultdict

class QualityLevel(Enum):
    S = "S级(卓越)"
    A = "A级(优秀)"
    B = "B级(良好)"
    C = "C级(合格)"
    D = "D级(不合格)"

@dataclass
class QualityDimension:
    """质量维度定义"""
    name: str
    weight: float
    score: float = 0.0
    sub_items: List[str] = field(default_factory=list)
    issues: List[Dict] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)

@dataclass
class QualityReport:
    """质量报告"""
    total_score: float = 0.0
    level: QualityLevel = QualityLevel.D
    dimensions: Dict[str, QualityDimension] = field(default_factory=dict)
    radar_data: Dict[str, float] = field(default_factory=dict)
    critical_issues: List[Dict] = field(default_factory=list)
    improvement_suggestions: List[Dict] = field(default_factory=list)
    passed_gate: bool = False

class NWACSQualitySystemV4:
    """NWACS V8.0 质量检测系统 V4版本"""
    
    def __init__(self, work_type: str = "novel"):
        self.work_type = work_type
        self.quality_gate = {
            "min_total_score": 60,
            "min_dimension_score": 40,
            "auto_block": True
        }
        self._init_default_weights()
        
    def _init_default_weights(self):
        """初始化默认权重"""
        self.weights = {
            "novel": {
                "逻辑性": 0.20,
                "一致性": 0.20,
                "文学性": 0.20,
                "可读性": 0.20,
                "创新性": 0.10,
                "市场性": 0.10
            },
            "essay": {
                "逻辑性": 0.25,
                "一致性": 0.15,
                "文学性": 0.25,
                "可读性": 0.20,
                "创新性": 0.10,
                "市场性": 0.05
            },
            "poetry": {
                "逻辑性": 0.10,
                "一致性": 0.10,
                "文学性": 0.35,
                "可读性": 0.20,
                "创新性": 0.15,
                "市场性": 0.10
            }
        }
        
    def analyze(self, text: str) -> QualityReport:
        """执行完整质量分析"""
        report = QualityReport()
        
        # 1. 六维度分析
        self._analyze_logic(report, text)
        self._analyze_consistency(report, text)
        self._analyze_literariness(report, text)
        self._analyze_readability(report, text)
        self._analyze_innovation(report, text)
        self._analyze_marketability(report, text)
        
        # 2. 计算总分
        report.total_score = self._calculate_total_score(report)
        
        # 3. 等级判定
        report.level = self._determine_level(report.total_score)
        
        # 4. 生成雷达图数据
        report.radar_data = self._generate_radar_data(report)
        
        # 5. 生成改进建议
        report.improvement_suggestions = self._generate_improvement_suggestions(report)
        
        # 6. 质量门禁检查
        report.passed_gate = self._check_quality_gate(report)
        
        return report
    
    def _analyze_logic(self, report: QualityReport, text: str):
        """逻辑性分析"""
        dimension = QualityDimension(
            name="逻辑性",
            weight=self.weights.get(self.work_type, self.weights["novel"])["逻辑性"],
            sub_items=["因果关系", "时间线", "空间逻辑", "动机合理"]
        )
        
        issues = []
        score = 100
        
        # 检查因果关系
        cause_effect_patterns = [
            (r'因为.*所以', 5),
            (r'由于.*因此', 5),
            (r'导致', 3),
            (r'结果', 3)
        ]
        cause_effect_score = self._check_patterns(text, cause_effect_patterns)
        
        # 检查时间线
        time_patterns = [
            (r'\d{4}年', 3),
            (r'[上中下]午', 2),
            (r'[昨今明]天', 2),
            (r'[前后]来', 2)
        ]
        time_score = self._check_patterns(text, time_patterns)
        
        # 检查空间逻辑
        space_patterns = [
            (r'[东南西北]边', 2),
            (r'[上下左右]方', 2),
            (r'[内外前后]', 2)
        ]
        space_score = self._check_patterns(text, space_patterns)
        
        # 检查动机合理
        motive_patterns = [
            (r'为了', 3),
            (r'想要', 2),
            (r'打算', 2),
            (r'希望', 2)
        ]
        motive_score = self._check_patterns(text, motive_patterns)
        
        # 计算总得分
        dimension.score = min(100, (cause_effect_score + time_score + space_score + motive_score) * 5)
        
        # 检查逻辑矛盾
        contradictions = self._find_contradictions(text)
        if contradictions:
            dimension.score -= len(contradictions) * 10
            issues.extend(contradictions)
        
        dimension.issues = issues
        report.dimensions["逻辑性"] = dimension
    
    def _analyze_consistency(self, report: QualityReport, text: str):
        """一致性分析"""
        dimension = QualityDimension(
            name="一致性",
            weight=self.weights.get(self.work_type, self.weights["novel"])["一致性"],
            sub_items=["角色性格", "世界观规则", "剧情前后", "细节一致"]
        )
        
        issues = []
        score = 100
        
        # 检查角色一致性
        character_consistency = self._check_character_consistency(text)
        if character_consistency["issues"]:
            score -= len(character_consistency["issues"]) * 15
            issues.extend(character_consistency["issues"])
        
        # 检查世界观规则
        world_rules = self._check_world_rules(text)
        if world_rules["issues"]:
            score -= len(world_rules["issues"]) * 10
            issues.extend(world_rules["issues"])
        
        # 检查剧情前后一致
        plot_consistency = self._check_plot_consistency(text)
        if plot_consistency["issues"]:
            score -= len(plot_consistency["issues"]) * 12
            issues.extend(plot_consistency["issues"])
        
        # 检查细节一致
        detail_consistency = self._check_detail_consistency(text)
        if detail_consistency["issues"]:
            score -= len(detail_consistency["issues"]) * 8
            issues.extend(detail_consistency["issues"])
        
        dimension.score = max(0, score)
        dimension.issues = issues
        report.dimensions["一致性"] = dimension
    
    def _analyze_literariness(self, report: QualityReport, text: str):
        """文学性分析"""
        dimension = QualityDimension(
            name="文学性",
            weight=self.weights.get(self.work_type, self.weights["novel"])["文学性"],
            sub_items=["语言优美", "描写生动", "情感真挚", "意境营造"]
        )
        
        score = 100
        issues = []
        
        # 语言优美度检查
        beautiful_language = self._check_beautiful_language(text)
        score += beautiful_language["score"]
        if beautiful_language["issues"]:
            issues.extend(beautiful_language["issues"])
        
        # 描写生动度检查
        vivid_description = self._check_vivid_description(text)
        score += vivid_description["score"]
        if vivid_description["issues"]:
            issues.extend(vivid_description["issues"])
        
        # 情感真挚度检查
        emotional_authenticity = self._check_emotional_authenticity(text)
        score += emotional_authenticity["score"]
        if emotional_authenticity["issues"]:
            issues.extend(emotional_authenticity["issues"])
        
        # 意境营造检查
        artistic_conception = self._check_artistic_conception(text)
        score += artistic_conception["score"]
        if artistic_conception["issues"]:
            issues.extend(artistic_conception["issues"])
        
        dimension.score = max(0, min(100, score))
        dimension.issues = issues
        report.dimensions["文学性"] = dimension
    
    def _analyze_readability(self, report: QualityReport, text: str):
        """可读性分析"""
        dimension = QualityDimension(
            name="可读性",
            weight=self.weights.get(self.work_type, self.weights["novel"])["可读性"],
            sub_items=["节奏把控", "钩子设置", "爽点安排", "阅读体验"]
        )
        
        score = 100
        issues = []
        
        # 节奏把控检查
        rhythm_control = self._check_rhythm_control(text)
        score += rhythm_control["score"]
        if rhythm_control["issues"]:
            issues.extend(rhythm_control["issues"])
        
        # 钩子设置检查
        hook_setting = self._check_hook_setting(text)
        score += hook_setting["score"]
        if hook_setting["issues"]:
            issues.extend(hook_setting["issues"])
        
        # 爽点安排检查
        pleasure_points = self._check_pleasure_points(text)
        score += pleasure_points["score"]
        if pleasure_points["issues"]:
            issues.extend(pleasure_points["issues"])
        
        # 阅读体验检查
        reading_experience = self._check_reading_experience(text)
        score += reading_experience["score"]
        if reading_experience["issues"]:
            issues.extend(reading_experience["issues"])
        
        dimension.score = max(0, min(100, score))
        dimension.issues = issues
        report.dimensions["可读性"] = dimension
    
    def _analyze_innovation(self, report: QualityReport, text: str):
        """创新性分析"""
        dimension = QualityDimension(
            name="创新性",
            weight=self.weights.get(self.work_type, self.weights["novel"])["创新性"],
            sub_items=["情节创新", "人物创新", "设定创新", "表达创新"]
        )
        
        score = 50  # 基础分
        issues = []
        
        # 检查创新元素
        innovation_elements = self._check_innovation_elements(text)
        score += innovation_elements["score"]
        if innovation_elements["issues"]:
            issues.extend(innovation_elements["issues"])
        
        # 检查独特表达
        unique_expression = self._check_unique_expression(text)
        score += unique_expression["score"]
        if unique_expression["issues"]:
            issues.extend(unique_expression["issues"])
        
        dimension.score = max(0, min(100, score))
        dimension.issues = issues
        report.dimensions["创新性"] = dimension
    
    def _analyze_marketability(self, report: QualityReport, text: str):
        """市场性分析"""
        dimension = QualityDimension(
            name="市场性",
            weight=self.weights.get(self.work_type, self.weights["novel"])["市场性"],
            sub_items=["读者接受度", "平台适配", "商业价值", "传播潜力"]
        )
        
        score = 50  # 基础分
        issues = []
        
        # 检查市场元素
        market_elements = self._check_market_elements(text)
        score += market_elements["score"]
        if market_elements["issues"]:
            issues.extend(market_elements["issues"])
        
        # 检查平台适配性
        platform_adaptation = self._check_platform_adaptation(text)
        score += platform_adaptation["score"]
        if platform_adaptation["issues"]:
            issues.extend(platform_adaptation["issues"])
        
        dimension.score = max(0, min(100, score))
        dimension.issues = issues
        report.dimensions["市场性"] = dimension
    
    def _calculate_total_score(self, report: QualityReport) -> float:
        """计算总分"""
        total = 0.0
        for name, dimension in report.dimensions.items():
            total += dimension.score * dimension.weight
        return round(total, 2)
    
    def _determine_level(self, score: float) -> QualityLevel:
        """等级判定"""
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
        """生成雷达图数据"""
        return {
            name: dimension.score
            for name, dimension in report.dimensions.items()
        }
    
    def _generate_improvement_suggestions(self, report: QualityReport) -> List[Dict]:
        """生成改进建议"""
        suggestions = []
        
        for name, dimension in report.dimensions.items():
            if dimension.score < 60:
                suggestion = {
                    "dimension": name,
                    "current_score": dimension.score,
                    "priority": "高" if dimension.score < 40 else "中",
                    "issues": dimension.issues[:3],  # 最多显示3个问题
                    "suggestions": self._get_improvement_suggestions(name, dimension)
                }
                suggestions.append(suggestion)
        
        # 按优先级排序
        suggestions.sort(key=lambda x: x["current_score"])
        
        return suggestions
    
    def _get_improvement_suggestions(self, dimension_name: str, dimension: QualityDimension) -> List[str]:
        """获取具体改进建议"""
        suggestions_map = {
            "逻辑性": [
                "加强因果关系的交代",
                "注意时间线的连贯性",
                "确保空间逻辑一致",
                "完善角色行为动机"
            ],
            "一致性": [
                "保持角色性格统一",
                "遵守世界观设定规则",
                "检查剧情前后矛盾",
                "注意细节描写一致"
            ],
            "文学性": [
                "丰富修辞手法运用",
                "增强场景描写生动性",
                "深化情感表达",
                "营造独特意境"
            ],
            "可读性": [
                "调整章节节奏",
                "设置更多悬念钩子",
                "合理安排爽点",
                "优化阅读流畅度"
            ],
            "创新性": [
                "尝试新颖的情节设计",
                "塑造独特的人物形象",
                "创新世界观设定",
                "探索新的表达方式"
            ],
            "市场性": [
                "关注读者喜好趋势",
                "适配目标平台要求",
                "提升商业价值",
                "增强传播性"
            ]
        }
        
        return suggestions_map.get(dimension_name, ["关注该维度的提升"])
    
    def _check_quality_gate(self, report: QualityReport) -> bool:
        """质量门禁检查"""
        # 检查总分
        if report.total_score < self.quality_gate["min_total_score"]:
            return False
        
        # 检查单项分数
        for dimension in report.dimensions.values():
            if dimension.score < self.quality_gate["min_dimension_score"]:
                return False
        
        return True
    
    def _check_patterns(self, text: str, patterns: List[Tuple[str, int]]) -> int:
        """检查文本中的模式"""
        score = 0
        for pattern, weight in patterns:
            matches = re.findall(pattern, text)
            score += len(matches) * weight
        return score
    
    def _find_contradictions(self, text: str) -> List[Dict]:
        """查找逻辑矛盾"""
        contradictions = []
        
        # 检查时间矛盾
        time_pattern = r'(\d{4})年'
        years = re.findall(time_pattern, text)
        if len(years) >= 2:
            if int(years[-1]) < int(years[0]):
                contradictions.append({
                    "type": "时间矛盾",
                    "detail": f"时间线混乱：{years[0]}年 -> {years[-1]}年",
                    "severity": "高"
                })
        
        # 检查空间矛盾
        space_pattern = r'[东南西北]边'
        spaces = re.findall(space_pattern, text)
        if len(spaces) >= 4:
            # 简单检查是否有矛盾的方向描述
            if '东边' in spaces and '西边' in spaces:
                contradictions.append({
                    "type": "空间矛盾",
                    "detail": "同时出现东边和西边的描述",
                    "severity": "中"
                })
        
        return contradictions
    
    def _check_character_consistency(self, text: str) -> Dict:
        """检查角色一致性"""
        result = {"issues": [], "score": 0}
        
        # 提取角色名
        character_pattern = r'[他她它]'
        characters = re.findall(character_pattern, text)
        
        # 检查角色代词使用
        if len(set(characters)) > 3:
            result["issues"].append({
                "type": "角色代词混乱",
                "detail": "多个角色代词混用，可能导致读者混淆",
                "severity": "中"
            })
        
        return result
    
    def _check_world_rules(self, text: str) -> Dict:
        """检查世界观规则"""
        result = {"issues": [], "score": 0}
        
        # 检查规则一致性
        rule_patterns = [
            (r'不能.*却', "规则矛盾"),
            (r'可以.*但.*不能', "规则冲突"),
            (r'必须.*却.*没有', "规则违反")
        ]
        
        for pattern, issue_type in rule_patterns:
            if re.search(pattern, text):
                result["issues"].append({
                    "type": issue_type,
                    "detail": f"发现规则不一致：{pattern}",
                    "severity": "高"
                })
        
        return result
    
    def _check_plot_consistency(self, text: str) -> Dict:
        """检查剧情一致性"""
        result = {"issues": [], "score": 0}
        
        # 检查剧情转折
        plot_turns = re.findall(r'突然|意外|转折', text)
        if len(plot_turns) > 5:
            result["issues"].append({
                "type": "剧情转折过多",
                "detail": "剧情转折过于频繁，可能影响故事连贯性",
                "severity": "中"
            })
        
        return result
    
    def _check_detail_consistency(self, text: str) -> Dict:
        """检查细节一致性"""
        result = {"issues": [], "score": 0}
        
        # 检查数字一致性
        numbers = re.findall(r'\d+', text)
        if len(numbers) > 10:
            # 检查是否有明显的数字矛盾
            for i in range(len(numbers) - 1):
                if abs(int(numbers[i]) - int(numbers[i+1])) > 1000:
                    result["issues"].append({
                        "type": "数字矛盾",
                        "detail": f"数字{numbers[i]}和{numbers[i+1]}相差过大",
                        "severity": "低"
                    })
        
        return result
    
    def _check_beautiful_language(self, text: str) -> Dict:
        """检查语言优美度"""
        result = {"issues": [], "score": 0}
        
        # 检查修辞手法
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
                "type": "修辞手法不足",
                "detail": "建议增加修辞手法的使用，提升语言表现力",
                "severity": "低"
            })
        
        return result
    
    def _check_vivid_description(self, text: str) -> Dict:
        """检查描写生动度"""
        result = {"issues": [], "score": 0}
        
        # 检查感官描写
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
                "type": "感官描写不足",
                "detail": "建议增加多感官描写，增强场景沉浸感",
                "severity": "中"
            })
        
        return result
    
    def _check_emotional_authenticity(self, text: str) -> Dict:
        """检查情感真挚度"""
        result = {"issues": [], "score": 0}
        
        # 检查情感词汇
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
                "type": "情感表达不足",
                "detail": "建议增加情感描写，增强读者共鸣",
                "severity": "中"
            })
        
        return result
    
    def _check_artistic_conception(self, text: str) -> Dict:
        """检查意境营造"""
        result = {"issues": [], "score": 0}
        
        # 检查意境词汇
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
                "type": "意境营造不足",
                "detail": "建议增加意境描写，提升文学美感",
                "severity": "低"
            })
        
        return result
    
    def _check_rhythm_control(self, text: str) -> Dict:
        """检查节奏把控"""
        result = {"issues": [], "score": 0}
        
        # 检查段落长度
        paragraphs = text.split('\n')
        avg_paragraph_length = sum(len(p) for p in paragraphs) / max(len(paragraphs), 1)
        
        if avg_paragraph_length > 500:
            result["issues"].append({
                "type": "段落过长",
                "detail": "平均段落过长，建议适当分段提升可读性",
                "severity": "中"
            })
            result["score"] = -10
        elif avg_paragraph_length < 50:
            result["issues"].append({
                "type": "段落过短",
                "detail": "段落过于零碎，建议适当合并",
                "severity": "低"
            })
            result["score"] = -5
        else:
            result["score"] = 10
        
        return result
    
    def _check_hook_setting(self, text: str) -> Dict:
        """检查钩子设置"""
        result = {"issues": [], "score": 0}
        
        # 检查悬念设置
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
                "type": "悬念设置不足",
                "detail": "建议增加悬念和钩子，提升读者阅读欲望",
                "severity": "高"
            })
        
        return result
    
    def _check_pleasure_points(self, text: str) -> Dict:
        """检查爽点安排"""
        result = {"issues": [], "score": 0}
        
        # 检查爽点元素
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
                "type": "爽点不足",
                "detail": "建议增加爽点安排，提升阅读快感",
                "severity": "中"
            })
        
        return result
    
    def _check_reading_experience(self, text: str) -> Dict:
        """检查阅读体验"""
        result = {"issues": [], "score": 0}
        
        # 检查句子长度
        sentences = re.split(r'[。！？]', text)
        avg_sentence_length = sum(len(s) for s in sentences) / max(len(sentences), 1)
        
        if avg_sentence_length > 100:
            result["issues"].append({
                "type": "句子过长",
                "detail": "平均句子过长，建议适当拆分",
                "severity": "中"
            })
            result["score"] = -10
        elif avg_sentence_length < 10:
            result["issues"].append({
                "type": "句子过短",
                "detail": "句子过于简短，建议适当丰富",
                "severity": "低"
            })
            result["score"] = -5
        else:
            result["score"] = 10
        
        return result
    
    def _check_innovation_elements(self, text: str) -> Dict:
        """检查创新元素"""
        result = {"issues": [], "score": 0}
        
        # 检查创新词汇
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
        """检查独特表达"""
        result = {"issues": [], "score": 0}
        
        # 检查独特表达方式
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
        """检查市场元素"""
        result = {"issues": [], "score": 0}
        
        # 检查热门元素
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
                "type": "市场元素不足",
                "detail": "建议增加热门元素，提升市场吸引力",
                "severity": "中"
            })
        
        return result
    
    def _check_platform_adaptation(self, text: str) -> Dict:
        """检查平台适配性"""
        result = {"issues": [], "score": 0}
        
        # 检查字数
        word_count = len(text)
        if word_count < 1000:
            result["issues"].append({
                "type": "字数不足",
                "detail": f"当前字数{word_count}，建议达到1000字以上",
                "severity": "高"
            })
            result["score"] = -20
        elif word_count > 10000:
            result["issues"].append({
                "type": "字数过多",
                "detail": f"当前字数{word_count}，建议适当精简",
                "severity": "低"
            })
            result["score"] = -5
        else:
            result["score"] = 10
        
        return result
    
    def generate_report(self, report: QualityReport) -> str:
        """生成可读的报告"""
        output = []
        output.append("=" * 60)
        output.append(f"NWACS V8.0 质量检测报告 (V4版本)")
        output.append("=" * 60)
        output.append(f"作品类型: {self.work_type}")
        output.append(f"总分: {report.total_score:.2f}分")
        output.append(f"等级: {report.level.value}")
        output.append(f"门禁状态: {'通过' if report.passed_gate else '未通过'}")
        output.append("")
        
        # 各维度得分
        output.append("【六维度得分】")
        for name, dimension in report.dimensions.items():
            bar = "█" * int(dimension.score / 10) + "░" * (10 - int(dimension.score / 10))
            output.append(f"{name}: {dimension.score:.1f}分 {bar}")
        
        output.append("")
        output.append("【雷达图数据】")
        for name, value in report.radar_data.items():
            output.append(f"  {name}: {value:.1f}")
        
        # 改进建议
        if report.improvement_suggestions:
            output.append("")
            output.append("【改进建议】")
            for suggestion in report.improvement_suggestions:
                output.append(f"\n[{suggestion['priority']}优先级] {suggestion['dimension']} (当前: {suggestion['current_score']:.1f}分)")
                if suggestion['issues']:
                    output.append("  问题:")
                    for issue in suggestion['issues'][:2]:
                        output.append(f"    - {issue.get('detail', '')}")
                output.append("  建议:")
                for s in suggestion['suggestions'][:3]:
                    output.append(f"    ✓ {s}")
        
        output.append("")
        output.append("=" * 60)
        
        return "\n".join(output)

# 使用示例
def main():
    # 创建质量检测系统
    qa_system = NWACSQualitySystemV4(work_type="novel")
    
    # 测试文本
    test_text = """
    在一个遥远的王国里，有一个年轻的王子名叫艾伦。他从小就被教导要成为一位伟大的统治者。
    然而，就在他十八岁生日那天，一个神秘的预言改变了一切。
    
    预言说，王国将在三年后陷入黑暗，只有找到传说中的光明之石才能拯救王国。
    艾伦决定踏上寻找光明之石的旅程。他带着忠诚的骑士和聪明的法师，一起出发了。
    
    在旅途中，他们遇到了各种困难和挑战。他们穿越了黑暗森林，翻越了雪山，渡过了急流。
    每次遇到危险，艾伦都能凭借智慧和勇气化险为夷。
    
    终于，在经历了无数考验后，他们找到了光明之石。但让他们惊讶的是，
    光明之石竟然是一个普通的石头，只有内心纯净的人才能让它发光。
    
    艾伦明白了，真正的光明来自于内心的善良和勇气。他带着这个领悟回到了王国，
    用自己的行动照亮了整个王国。
    """
    
    # 执行分析
    report = qa_system.analyze(test_text)
    
    # 生成报告
    report_text = qa_system.generate_report(report)
    print(report_text)
    
    # 返回完整数据
    return {
        "report": report,
        "report_text": report_text
    }

if __name__ == "__main__":
    result = main()
```

这个V4版本的质量检测系统实现了以下核心功能：

## 主要特性

### 1. 六维度质量模型
- **逻辑性(20分)**：检查因果关系、时间线、空间逻辑、动机合理
- **一致性(20分)**：检查角色性格、世界观规则、剧情前后、细节一致
- **文学性(20分)**：检查语言优美、描写生动、情感真挚、意境营造
- **可读性(20分)**：检查节奏把控、钩子设置、爽点安排、阅读体验
- **创新性(10分)**：检查情节创新、人物创新、设定创新、表达创新
- **市场性(10分)**：检查读者接受度、平台适配、商业价值、传播潜力

### 2. 智能评分引擎
- 自动评分：根据各维度自动打分
- 权重调整：可根据作品类型调整权重(小说/散文/诗歌)
- 等级判定：S/A/B/C/D五级
- 雷达图：多维度可视化数据

### 3. 改进建议系统
- 问题定位：具体指出问题所在
- 原因分析：分析问题原因
- 优化方向：指出优化方向
- 优先级：按重要性排序

### 4. 质量门禁
- 最低标准：总分>=60
- 单项标准：无维度<40
- 自动拦截：不达标不保存
- 人工授权：可强制通过

系统会自动生成详细的质量报告，包括各维度得分、雷达图数据、改进建议等，帮助作者全面提升作品质量。