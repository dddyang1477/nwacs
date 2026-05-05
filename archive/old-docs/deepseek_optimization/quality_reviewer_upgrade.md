# 质量检测系统升级方案

*由DeepSeek生成 | 时间：2026-05-03 13:31:41*

# NWACS V8.0 质量检测系统升级方案

## 一、完整升级代码实现

```python
import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json

# ==================== 基础数据结构 ====================

@dataclass
class QualityDimension:
    """质量维度类"""
    name: str
    weight: float
    score: float = 0.0
    details: Dict[str, float] = field(default_factory=dict)
    issues: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)

@dataclass
class DetectionResult:
    """检测结果类"""
    dimension: str
    score: float
    issues: List[str]
    suggestions: List[str]
    confidence: float  # 置信度

@dataclass
class ChapterAnalysis:
    """章节分析结果"""
    chapter_number: int
    word_count: int
    hook_density: float  # 钩子密度
    pacing_score: float
    emotional_curve: List[float]
    key_points: List[str]

# ==================== 核心检测引擎 ====================

class AdvancedQualityDetector:
    """高级质量检测引擎"""
    
    def __init__(self):
        self.semantic_analyzer = SemanticAnalyzer()
        self.emotion_analyzer = EmotionAnalyzer()
        self.structure_analyzer = StructureAnalyzer()
        self.style_analyzer = StyleAnalyzer()
        
    def analyze_text(self, text: str) -> Dict[str, DetectionResult]:
        """综合分析文本"""
        results = {}
        
        # 语义分析
        semantic_result = self.semantic_analyzer.analyze(text)
        results['semantic'] = semantic_result
        
        # 情感分析
        emotion_result = self.emotion_analyzer.analyze(text)
        results['emotion'] = emotion_result
        
        # 结构分析
        structure_result = self.structure_analyzer.analyze(text)
        results['structure'] = structure_result
        
        # 风格分析
        style_result = self.style_analyzer.analyze(text)
        results['style'] = style_result
        
        return results

class SemanticAnalyzer:
    """语义分析器"""
    
    def __init__(self):
        self.contradiction_patterns = [
            (r'但是.*却.*相反', '转折矛盾'),
            (r'虽然.*但是.*然而', '逻辑混乱'),
        ]
        self.causality_markers = ['因为', '所以', '因此', '由于', '导致']
        
    def analyze(self, text: str) -> DetectionResult:
        """分析语义逻辑"""
        issues = []
        suggestions = []
        score = 100.0
        
        # 检查语义矛盾
        for pattern, issue_type in self.contradiction_patterns:
            if re.search(pattern, text):
                issues.append(f"发现{issue_type}")
                score -= 10
        
        # 检查因果关系
        causality_count = sum(1 for marker in self.causality_markers if marker in text)
        if causality_count == 0:
            suggestions.append("建议增加因果关系连接词，增强逻辑性")
            score -= 5
            
        return DetectionResult(
            dimension="语义分析",
            score=max(0, score),
            issues=issues,
            suggestions=suggestions,
            confidence=0.85
        )

class EmotionAnalyzer:
    """情感分析器"""
    
    def __init__(self):
        self.positive_words = ['喜悦', '感动', '温暖', '希望', '幸福']
        self.negative_words = ['悲伤', '愤怒', '恐惧', '绝望', '痛苦']
        self.emotion_intensity = {
            '强烈': 0.9, '中等': 0.6, '轻微': 0.3
        }
        
    def analyze(self, text: str) -> DetectionResult:
        """分析情感表达效果"""
        issues = []
        suggestions = []
        score = 100.0
        
        # 检测情感词汇密度
        total_words = len(text)
        emotion_words = sum(1 for word in self.positive_words + self.negative_words if word in text)
        emotion_density = emotion_words / max(total_words, 1) * 100
        
        if emotion_density < 1:
            suggestions.append("情感词汇密度较低，建议增加情感表达")
            score -= 15
        elif emotion_density > 20:
            suggestions.append("情感词汇过多，建议适度控制")
            score -= 5
            
        # 检测情感平衡
        pos_count = sum(1 for word in self.positive_words if word in text)
        neg_count = sum(1 for word in self.negative_words if word in text)
        
        if pos_count == 0 and neg_count == 0:
            suggestions.append("缺乏情感词汇，建议增加情感描写")
            score -= 10
        elif abs(pos_count - neg_count) > 5:
            suggestions.append("情感倾向过于单一，建议平衡正负面情感")
            score -= 5
            
        return DetectionResult(
            dimension="情感分析",
            score=max(0, score),
            issues=issues,
            suggestions=suggestions,
            confidence=0.80
        )

class StructureAnalyzer:
    """结构分析器"""
    
    def __init__(self):
        self.chapter_markers = ['第一章', '第1章', 'Chapter', '章节']
        self.transition_words = ['与此同时', '另一方面', '然而', '突然']
        
    def analyze(self, text: str) -> DetectionResult:
        """分析章节结构"""
        issues = []
        suggestions = []
        score = 100.0
        
        # 检测章节划分
        chapters = [m.start() for m in re.finditer(r'(第[一二三四五六七八九十百千]+章|第\d+章|Chapter\s+\d+)', text)]
        
        if len(chapters) < 2:
            suggestions.append("建议增加章节划分，提高可读性")
            score -= 20
        elif len(chapters) > 50:
            suggestions.append("章节过多，建议合并部分章节")
            score -= 10
            
        # 检测过渡使用
        transition_count = sum(1 for word in self.transition_words if word in text)
        if transition_count < 3:
            suggestions.append("过渡词汇较少，建议增加场景切换的过渡")
            score -= 10
            
        # 计算章节长度均匀性
        if len(chapters) > 1:
            chapter_lengths = []
            for i in range(len(chapters) - 1):
                chapter_lengths.append(chapters[i+1] - chapters[i])
            
            if chapter_lengths:
                avg_length = sum(chapter_lengths) / len(chapter_lengths)
                variance = sum((l - avg_length)**2 for l in chapter_lengths) / len(chapter_lengths)
                
                if variance > avg_length * 2:
                    issues.append("章节长度差异过大")
                    score -= 10
                    
        return DetectionResult(
            dimension="结构分析",
            score=max(0, score),
            issues=issues,
            suggestions=suggestions,
            confidence=0.75
        )

class StyleAnalyzer:
    """风格分析器"""
    
    def __init__(self):
        self.formal_markers = ['因此', '然而', '此外', '鉴于']
        self.informal_markers = ['然后', '但是', '而且', '因为']
        self.dialogue_markers = ['说', '道', '问', '答']
        
    def analyze(self, text: str) -> DetectionResult:
        """分析写作风格"""
        issues = []
        suggestions = []
        score = 100.0
        
        # 检测风格一致性
        formal_count = sum(1 for word in self.formal_markers if word in text)
        informal_count = sum(1 for word in self.informal_markers if word in text)
        
        if formal_count > 0 and informal_count > 0:
            ratio = formal_count / (informal_count + 1)
            if ratio < 0.5 or ratio > 2.0:
                issues.append("写作风格不统一，正式与非正式词汇混用")
                score -= 15
                
        # 检测对话密度
        dialogue_count = sum(1 for word in self.dialogue_markers if word in text)
        total_sentences = len(re.findall(r'[。！？]', text))
        
        if total_sentences > 0:
            dialogue_density = dialogue_count / total_sentences
            if dialogue_density < 0.1:
                suggestions.append("对话比例较低，建议增加对话交互")
                score -= 5
            elif dialogue_density > 0.8:
                suggestions.append("对话比例过高，建议增加叙述描写")
                score -= 5
                
        return DetectionResult(
            dimension="风格分析",
            score=max(0, score),
            issues=issues,
            suggestions=suggestions,
            confidence=0.70
        )

# ==================== 质量评分系统 ====================

class QualityScoringSystem:
    """质量评分系统"""
    
    def __init__(self):
        self.dimensions = {
            '逻辑性': QualityDimension('逻辑性', 0.20),
            '一致性': QualityDimension('一致性', 0.20),
            '文学性': QualityDimension('文学性', 0.20),
            '可读性': QualityDimension('可读性', 0.20),
            '创新性': QualityDimension('创新性', 0.10),
            '市场性': QualityDimension('市场性', 0.10)
        }
        
    def calculate_scores(self, detection_results: Dict[str, DetectionResult]) -> Dict[str, float]:
        """计算各维度得分"""
        scores = {}
        
        # 从检测结果映射到质量维度
        for dimension in self.dimensions:
            dim_score = 100.0
            
            # 根据检测结果调整分数
            for result_key, result in detection_results.items():
                if result_key == 'semantic' and dimension == '逻辑性':
                    dim_score = result.score
                elif result_key == 'emotion' and dimension == '文学性':
                    dim_score = (dim_score + result.score) / 2
                elif result_key == 'structure' and dimension == '可读性':
                    dim_score = result.score
                elif result_key == 'style' and dimension == '文学性':
                    dim_score = (dim_score + result.score) / 2
                    
            scores[dimension] = dim_score
            
        return scores
    
    def calculate_total_score(self, dimension_scores: Dict[str, float]) -> float:
        """计算总分"""
        total = 0.0
        for dimension, score in dimension_scores.items():
            weight = self.dimensions[dimension].weight
            total += score * weight
        return total
    
    def get_grade(self, total_score: float) -> str:
        """获取等级评定"""
        if total_score >= 90:
            return 'S级'
        elif total_score >= 80:
            return 'A级'
        elif total_score >= 70:
            return 'B级'
        elif total_score >= 60:
            return 'C级'
        else:
            return 'D级'

# ==================== 改进建议系统 ====================

class ImprovementSuggestionSystem:
    """改进建议系统"""
    
    def __init__(self):
        self.suggestion_templates = {
            '逻辑性': {
                'high': ["逻辑链条清晰，建议保持"],
                'medium': ["部分逻辑需要加强，建议："],
                'low': ["逻辑问题较多，建议重点优化："]
            },
            '一致性': {
                'high': ["角色和设定一致性好"],
                'medium': ["建议检查角色行为的一致性"],
                'low': ["存在多处一致性冲突，建议重新梳理"]
            },
            '文学性': {
                'high': ["文笔优美，建议保持"],
                'medium': ["部分描写可以更生动，建议："],
                'low': ["文学性有待提高，建议："]
            },
            '可读性': {
                'high': ["阅读体验流畅"],
                'medium': ["节奏可以进一步优化，建议："],
                'low': ["可读性需要改进，建议："]
            },
            '创新性': {
                'high': ["创新性强，建议保持"],
                'medium": ["可以在某些方面增加创新，建议："],
                'low': ["建议增加创新元素"]
            },
            '市场性': {
                'high': ["市场潜力大"],
                'medium': ["可以进一步优化市场定位"],
                'low': ["需要调整市场策略"]
            }
        }
        
    def generate_suggestions(self, dimension_scores: Dict[str, float]) -> Dict[str, List[str]]:
        """生成改进建议"""
        suggestions = {}
        
        for dimension, score in dimension_scores.items():
            if score >= 85:
                level = 'high'
            elif score >= 70:
                level = 'medium'
            else:
                level = 'low'
                
            dim_suggestions = self.suggestion_templates[dimension][level].copy()
            
            # 添加具体建议
            if level != 'high':
                specific_suggestions = self._get_specific_suggestions(dimension, score)
                dim_suggestions.extend(specific_suggestions)
                
            suggestions[dimension] = dim_suggestions
            
        return suggestions
    
    def _get_specific_suggestions(self, dimension: str, score: float) -> List[str]:
        """获取具体改进建议"""
        suggestions = []
        
        if dimension == '逻辑性':
            if score < 70:
                suggestions.extend([
                    "检查故事的时间线是否连贯",
                    "验证因果关系是否合理",
                    "确保没有逻辑漏洞"
                ])
            else:
                suggestions.extend([
                    "优化次要情节的逻辑",
                    "增加伏笔和呼应的设计"
                ])
                
        elif dimension == '一致性':
            if score < 70:
                suggestions.extend([
                    "建立角色性格特征表",
                    "检查世界观规则的一致性",
                    "避免前后矛盾"
                ])
            else:
                suggestions.extend([
                    "深化角色性格刻画",
                    "细化世界观设定"
                ])
                
        elif dimension == '文学性':
            if score < 70:
                suggestions.extend([
                    "增加感官描写（视觉、听觉、触觉）",
                    "运用修辞手法（比喻、拟人）",
                    "优化句式结构，避免单调"
                ])
            else:
                suggestions.extend([
                    "提炼金句和精彩段落",
                    "增强情感表达的层次感"
                ])
                
        elif dimension == '可读性':
            if score < 70:
                suggestions.extend([
                    "增加章节钩子",
                    "优化节奏控制",
                    "设置悬念和爽点"
                ])
            else:
                suggestions.extend([
                    "调整高潮和低谷的节奏",
                    "优化信息释放的节奏"
                ])
                
        return suggestions[:3]  # 最多返回3条具体建议
    
    def prioritize_suggestions(self, suggestions: Dict[str, List[str]], 
                              dimension_scores: Dict[str, float]) -> List[Tuple[str, str, int]]:
        """对建议进行优先级排序"""
        prioritized = []
        
        for dimension, dim_suggestions in suggestions.items():
            score = dimension_scores[dimension]
            priority = 1 if score < 70 else (2 if score < 85 else 3)
            
            for suggestion in dim_suggestions:
                prioritized.append((dimension, suggestion, priority))
                
        # 按优先级排序
        prioritized.sort(key=lambda x: x[2])
        
        return prioritized

# ==================== 主检测系统 ====================

class NWACSQualityDetectionSystem:
    """NWACS V8.0 质量检测系统"""
    
    def __init__(self):
        self.detector = AdvancedQualityDetector()
        self.scoring_system = QualityScoringSystem()
        self.suggestion_system = ImprovementSuggestionSystem()
        
    def analyze_text(self, text: str) -> Dict:
        """分析文本质量"""
        # 1. 执行高级检测
        detection_results = self.detector.analyze_text(text)
        
        # 2. 计算各维度得分
        dimension_scores = self.scoring_system.calculate_scores(detection_results)
        
        # 3. 计算总分
        total_score = self.scoring_system.calculate_total_score(dimension_scores)
        
        # 4. 获取等级
        grade = self.scoring_system.get_grade(total_score)
        
        # 5. 生成改进建议
        suggestions = self.suggestion_system.generate_suggestions(dimension_scores)
        prioritized_suggestions = self.suggestion_system.prioritize_suggestions(
            suggestions, dimension_scores
        )
        
        # 6. 生成报告
        report = self._generate_report(
            detection_results,
            dimension_scores,
            total_score,
            grade,
            prioritized_suggestions
        )
        
        return report
    
    def _generate_report(self, detection_results, dimension_scores, 
                        total_score, grade, prioritized_suggestions):
        """生成检测报告"""
        report = {
            '检测时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            '系统版本': 'NWACS V8.0',
            '总体评分': {
                '总分': round(total_score, 2),
                '等级': grade
            },
            '分项评分': {},
            '改进建议': [],
            '详细检测结果': {}
        }
        
        # 添加分项评分
        for dimension, score in dimension_scores.items():
            report['分项评分'][dimension] = round(score, 2)
            
        # 添加改进建议
        for dimension, suggestion, priority in prioritized_suggestions:
            report['改进建议'].append({
                '维度': dimension,
                '建议': suggestion,
                '优先级': '高' if priority == 1 else ('中' if priority == 2 else '低')
            })
            
        # 添加详细检测结果
        for key, result in detection_results.items():
            report['详细检测结果'][key] = {
                '得分': result.score,
                '问题': result.issues,
                '建议': result.suggestions,
                '置信度': result.confidence
            }
            
        return report

# ==================== 使用示例 ====================

def main():
    """使用示例"""
    # 创建检测系统
    system = NWACSQualityDetectionSystem()
    
    # 示例文本
    sample_text = """
    第一章 相遇
    
    那是一个阳光明媚的下午，李明走在回家的路上。突然，他看到一个女孩晕倒在路边。
    
    他急忙跑过去，发现女孩脸色苍白，呼吸微弱。李明立刻拨打了急救电话。
    
    在等待救护车的时候，他想起自己学过一些急救知识，于是开始给女孩做心肺复苏。
    
    救护车很快赶到，医生们迅速将女孩送往医院。李明也跟了上去。
    
    在医院里，他得知女孩叫小红，是因为低血糖晕倒的。小红醒来后，对李明表示了感谢。
    
    这就是他们第一次相遇的故事。
    """
    
    # 执行检测
    report = system.analyze_text(sample_text)
    
    # 输出报告
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
```

## 二、升级说明文档

### 1. 系统架构升级

```
NWACS V8.0 质量检测系统
├── 数据层
│   ├── QualityDimension (质量维度类)
│   ├── DetectionResult (检测结果类)
│   └── ChapterAnalysis (章节分析类)
├── 检测层
│   ├── AdvancedQualityDetector (高级检测引擎)
│   ├── SemanticAnalyzer (语义分析器)
│   ├── EmotionAnalyzer (情感分析器)
│   ├── StructureAnalyzer (结构分析器)
│   └── StyleAnalyzer (风格分析器)
├── 评分层
│   └── QualityScoringSystem (评分系统)
└── 建议层
    └── ImprovementSuggestionSystem (建议系统)
```

### 2. 新增功能详解

#### 2.1 语义分析增强
- **因果关系检测**：自动识别逻辑连接词，评估推理链条完整性
- **矛盾检测**：使用正则表达式识别语义矛盾
- **置信度评估**：为每个检测结果提供置信度指标

#### 2.2 情感分析增强
- **情感词汇库**：包含正面和负面情感词汇
- **情感密度计算**：评估情感表达充分性
- **情感平衡检测**：确保正负面情感适当平衡

#### 2.3 结构分析增强
- **章节划分检测**：自动识别章节标记
- **过渡词汇评估**：检测场景切换的流畅性
- **章节长度均匀性**：评估章节结构合理性

#### 2.4 风格分析增强
- **正式/非正式词汇检测**：评估风格一致性
- **对话密度计算**：确保适当的对话比例
- **写作风格统一性**：检测风格变化

### 3. 评分体系说明

| 等级 | 分数范围 | 含义 | 建议行动 |
|------|---------|------|---------|
| S级 | 90-100 | 优秀 | 可投稿发表 |
| A级 | 80-89 | 良好 | 小幅修改 |
| B级 | 70-79 | 中等 | 中等修改 |
| C级 | 60-69 | 及格 | 大幅修改 |
| D级 | <60 | 不合格 | 重新创作 |

### 4. 改进建议优先级

```
优先级1 (高)：影响核心质量的严重问题
- 逻辑漏洞
- 角色行为不一致
- 严重语法错误

优先级2 (中)：影响阅读体验的问题
- 节奏控制不佳
- 描写不够生动
- 情感表达不足

优先级3 (低)：锦上添花的改进
- 优化句式
- 增加修辞手法
- 细化细节描写
```

### 5. 使用建议

1. **定期检测**：建议每完成一个章节或情节段落后进行检测
2. **重点关注**：优先处理高优先级问题
3. **迭代优化**：根据建议逐步改进，每次修改后重新检测
4. **结合人工**：系统建议作为参考，最终判断需结合人工经验

### 6. 扩展接口

系统预留了扩展接口，可以：
- 添加新的检测维度
- 自定义评分权重
- 扩展情感词汇库
- 添加新的分析器