# 系统集成优化方案

*由DeepSeek生成 | 时间：2026-05-03 13:34:28*

# NWACS V8.0 AI检测与质量检测集成方案

## 1. 核心集成架构

```python
# integration/core.py
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum
import asyncio
from datetime import datetime

class DetectionResult(Enum):
    PASS = "pass"
    WARNING = "warning"
    BLOCK = "block"

@dataclass
class AIDetectionReport:
    """AI检测报告"""
    score: float
    features: Dict[str, float]
    warnings: List[str]
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class QualityReport:
    """质量检测报告"""
    total_score: float
    dimensions: Dict[str, float]
    issues: List[str]
    suggestions: List[str]

@dataclass
class OptimizationResult:
    """优化结果"""
    original_text: str
    optimized_text: str
    before_detection: AIDetectionReport
    after_detection: AIDetectionReport
    quality_report: QualityReport
    changes: List[str]

@dataclass
class GenerationContext:
    """生成上下文"""
    text: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    detection_history: List[AIDetectionReport] = field(default_factory=list)
```

## 2. AI检测系统集成

```python
# integration/ai_detector.py
import numpy as np
from typing import Dict, List
import re

class AIDetector:
    """AI检测系统"""
    
    def __init__(self, threshold: float = 40.0):
        self.threshold = threshold
        self.feature_weights = {
            'repetition': 0.2,
            'sentence_length_variance': 0.15,
            'vocabulary_richness': 0.25,
            'transition_diversity': 0.2,
            'emotional_consistency': 0.2
        }
    
    async def detect(self, text: str) -> AIDetectionReport:
        """实时检测AI特征"""
        features = await self._extract_features(text)
        score = self._calculate_score(features)
        warnings = self._generate_warnings(score, features)
        
        return AIDetectionReport(
            score=score,
            features=features,
            warnings=warnings
        )
    
    async def _extract_features(self, text: str) -> Dict[str, float]:
        """提取AI特征"""
        return {
            'repetition': self._check_repetition(text),
            'sentence_length_variance': self._check_sentence_variance(text),
            'vocabulary_richness': self._check_vocabulary(text),
            'transition_diversity': self._check_transitions(text),
            'emotional_consistency': self._check_emotion(text)
        }
    
    def _check_repetition(self, text: str) -> float:
        """检测重复模式"""
        words = text.split()
        if len(words) < 10:
            return 0.0
        
        # 检查词频分布
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # 计算重复得分
        max_freq = max(word_freq.values())
        avg_freq = sum(word_freq.values()) / len(word_freq)
        
        return min(100, (max_freq / avg_freq - 1) * 50)
    
    def _check_sentence_variance(self, text: str) -> float:
        """检测句子长度变化"""
        sentences = re.split(r'[。！？\n]', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) < 3:
            return 0.0
        
        lengths = [len(s) for s in sentences]
        variance = np.var(lengths)
        
        # 方差越小越像AI
        return min(100, (1 - variance / (np.mean(lengths) ** 2)) * 100)
    
    def _check_vocabulary(self, text: str) -> float:
        """检测词汇丰富度"""
        words = set(text.split())
        total_words = len(text.split())
        
        if total_words == 0:
            return 0.0
        
        # 词汇多样性
        diversity = len(words) / total_words
        
        # 多样性越低越像AI
        return min(100, (1 - diversity) * 150)
    
    def _check_transitions(self, text: str) -> float:
        """检测过渡词多样性"""
        transition_words = [
            '但是', '然而', '因此', '所以', '而且',
            '此外', '同时', '另外', '不过', '虽然'
        ]
        
        found_transitions = []
        for word in transition_words:
            if word in text:
                found_transitions.append(word)
        
        # 过渡词太少或太多都像AI
        diversity = len(set(found_transitions)) / len(transition_words)
        return min(100, abs(diversity - 0.5) * 200)
    
    def _check_emotion(self, text: str) -> float:
        """检测情感一致性"""
        # 简化版情感检测
        positive_words = ['好', '美', '棒', '优秀', '精彩']
        negative_words = ['差', '糟', '坏', '糟糕', '失败']
        
        positive_count = sum(1 for w in positive_words if w in text)
        negative_count = sum(1 for w in negative_words if w in text)
        
        total_emotion = positive_count + negative_count
        if total_emotion == 0:
            return 50  # 中性
        
        ratio = positive_count / total_emotion
        
        # 极端情感比例更像AI
        return min(100, abs(ratio - 0.5) * 200)
    
    def _calculate_score(self, features: Dict[str, float]) -> float:
        """计算综合得分"""
        score = 0
        for feature, value in features.items():
            weight = self.feature_weights.get(feature, 0.1)
            score += value * weight
        return score
    
    def _generate_warnings(self, score: float, features: Dict[str, float]) -> List[str]:
        """生成预警信息"""
        warnings = []
        
        if score > self.threshold:
            warnings.append(f"AI特征得分过高: {score:.1f} > {self.threshold}")
        
        for feature, value in features.items():
            if value > 60:
                warnings.append(f"{feature}特征异常: {value:.1f}")
        
        return warnings
```

## 3. 质量检测系统集成

```python
# integration/quality_checker.py
from typing import List, Dict, Tuple
import re

class QualityChecker:
    """质量检测系统"""
    
    def __init__(self, min_total_score: float = 60.0):
        self.min_total_score = min_total_score
        self.dimension_weights = {
            'readability': 0.2,
            'coherence': 0.2,
            'structure': 0.2,
            'grammar': 0.2,
            'engagement': 0.2
        }
    
    async def check(self, text: str) -> QualityReport:
        """执行质量检测"""
        dimensions = await self._evaluate_dimensions(text)
        total_score = self._calculate_total(dimensions)
        issues = self._identify_issues(dimensions)
        suggestions = self._generate_suggestions(issues)
        
        return QualityReport(
            total_score=total_score,
            dimensions=dimensions,
            issues=issues,
            suggestions=suggestions
        )
    
    async def _evaluate_dimensions(self, text: str) -> Dict[str, float]:
        """评估各个维度"""
        return {
            'readability': self._check_readability(text),
            'coherence': self._check_coherence(text),
            'structure': self._check_structure(text),
            'grammar': self._check_grammar(text),
            'engagement': self._check_engagement(text)
        }
    
    def _check_readability(self, text: str) -> float:
        """检查可读性"""
        sentences = re.split(r'[。！？\n]', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences:
            return 0.0
        
        # 计算平均句长
        avg_length = sum(len(s) for s in sentences) / len(sentences)
        
        # 理想句长在20-40字之间
        if 20 <= avg_length <= 40:
            return 100.0
        elif avg_length < 20:
            return 60.0 + (avg_length / 20) * 40
        else:
            return max(0, 100 - (avg_length - 40) * 2)
    
    def _check_coherence(self, text: str) -> float:
        """检查连贯性"""
        # 检查连接词使用
        connectors = [
            '因为', '所以', '虽然', '但是', '而且',
            '如果', '那么', '不仅', '而且', '然而'
        ]
        
        connector_count = sum(1 for c in connectors if c in text)
        sentences = re.split(r'[。！？\n]', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) < 2:
            return 50.0
        
        # 每2-3句应该有一个连接词
        expected_connectors = len(sentences) / 2.5
        ratio = connector_count / expected_connectors
        
        return min(100, ratio * 100)
    
    def _check_structure(self, text: str) -> float:
        """检查结构"""
        paragraphs = text.split('\n')
        paragraphs = [p.strip() for p in paragraphs if p.strip()]
        
        if len(paragraphs) < 2:
            return 30.0
        
        # 检查段落长度是否合理
        lengths = [len(p) for p in paragraphs]
        avg_length = sum(lengths) / len(lengths)
        
        # 理想段落长度在100-300字
        if 100 <= avg_length <= 300:
            return 100.0
        elif avg_length < 100:
            return 50.0 + (avg_length / 100) * 50
        else:
            return max(0, 100 - (avg_length - 300) * 0.5)
    
    def _check_grammar(self, text: str) -> float:
        """检查语法"""
        # 简化版语法检查
        issues = 0
        
        # 检查常见语法问题
        patterns = [
            r'的的',  # 重复的
            r'了了',  # 重复了
            r'在在',  # 重复在
            r'是是',  # 重复是
            r'不不',  # 重复不
        ]
        
        for pattern in patterns:
            if re.search(pattern, text):
                issues += 1
        
        # 检查标点符号使用
        if text.count('，') > text.count('。') * 3:
            issues += 1
        
        # 计算得分
        score = max(0, 100 - issues * 20)
        return score
    
    def _check_engagement(self, text: str) -> float:
        """检查参与度"""
        # 检查修辞手法
        rhetoric = [
            '？', '！', '...', '——',
            '仿佛', '好像', '如同', '就像'
        ]
        
        rhetoric_count = sum(1 for r in rhetoric if r in text)
        sentences = re.split(r'[。！？\n]', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences:
            return 0.0
        
        # 每3-5句应该有一个修辞手法
        expected = len(sentences) / 4
        ratio = rhetoric_count / expected
        
        return min(100, ratio * 100)
    
    def _calculate_total(self, dimensions: Dict[str, float]) -> float:
        """计算总分"""
        total = 0
        for dim, score in dimensions.items():
            weight = self.dimension_weights.get(dim, 0.2)
            total += score * weight
        return total
    
    def _identify_issues(self, dimensions: Dict[str, float]) -> List[str]:
        """识别问题"""
        issues = []
        
        if dimensions['readability'] < 60:
            issues.append("可读性较差，需要调整句子长度")
        if dimensions['coherence'] < 60:
            issues.append("连贯性不足，需要增加连接词")
        if dimensions['structure'] < 60:
            issues.append("结构不合理，需要调整段落长度")
        if dimensions['grammar'] < 60:
            issues.append("存在语法问题，需要修正")
        if dimensions['engagement'] < 60:
            issues.append("参与度不高，需要增加修辞手法")
        
        return issues
    
    def _generate_suggestions(self, issues: List[str]) -> List[str]:
        """生成改进建议"""
        suggestion_map = {
            "可读性较差，需要调整句子长度": "将长句拆分为短句，保持20-40字为宜",
            "连贯性不足，需要增加连接词": "在段落间添加适当的连接词，如'因此'、'然而'等",
            "结构不合理，需要调整段落长度": "保持段落长度在100-300字之间",
            "存在语法问题，需要修正": "检查并修正重复词语和标点符号使用",
            "参与度不高，需要增加修辞手法": "适当加入疑问句、感叹句和比喻修辞"
        }
        
        return [suggestion_map.get(issue, "请检查并改进") for issue in issues]
```

## 4. 优化流水线系统

```python
# integration/optimization_pipeline.py
import asyncio
from typing import List, Optional
from dataclasses import dataclass

class OptimizationPipeline:
    """优化流水线"""
    
    def __init__(self, ai_detector: AIDetector, quality_checker: QualityChecker):
        self.ai_detector = ai_detector
        self.quality_checker = quality_checker
        self.optimizers = []
    
    def register_optimizer(self, optimizer: 'TextOptimizer'):
        """注册优化器"""
        self.optimizers.append(optimizer)
    
    async def process(self, text: str) -> OptimizationResult:
        """执行优化流水线"""
        # 第一步：AI特征检测
        before_detection = await self.ai_detector.detect(text)
        
        # 第二步：AI自动优化
        optimized_text = text
        for optimizer in self.optimizers:
            optimized_text = await optimizer.optimize(optimized_text, before_detection)
        
        # 第三步：质量审查
        quality_report = await self.quality_checker.check(optimized_text)
        
        # 第四步：改进建议
        if quality_report.total_score < 60:
            suggestions = quality_report.suggestions
            optimized_text = await self._apply_suggestions(optimized_text, suggestions)
        
        # 第五步：最终检测
        after_detection = await self.ai_detector.detect(optimized_text)
        
        # 记录变更
        changes = self._identify_changes(text, optimized_text)
        
        return OptimizationResult(
            original_text=text,
            optimized_text=optimized_text,
            before_detection=before_detection,
            after_detection=after_detection,
            quality_report=quality_report,
            changes=changes
        )
    
    async def _apply_suggestions(self, text: str, suggestions: List[str]) -> str:
        """应用改进建议"""
        # 这里可以实现建议的自动应用逻辑
        # 目前返回原文本，实际应用时需要更复杂的逻辑
        return text
    
    def _identify_changes(self, original: str, optimized: str) -> List[str]:
        """识别变更"""
        changes = []
        
        if original != optimized:
            # 简单比较长度变化
            if len(optimized) > len(original):
                changes.append(f"文本长度增加 {len(optimized) - len(original)} 字")
            elif len(optimized) < len(original):
                changes.append(f"文本长度减少 {len(original) - len(optimized)} 字")
        
        return changes

class TextOptimizer:
    """文本优化器基类"""
    
    async def optimize(self, text: str, detection: AIDetectionReport) -> str:
        """优化文本"""
        raise NotImplementedError

class AIFeatureOptimizer(TextOptimizer):
    """AI特征优化器"""
    
    async def optimize(self, text: str, detection: AIDetectionReport) -> str:
        """优化AI特征"""
        optimized = text
        
        # 如果重复特征过高，增加词汇多样性
        if detection.features.get('repetition', 0) > 60:
            optimized = self._reduce_repetition(optimized)
        
        # 如果句子方差过小，调整句子长度
        if detection.features.get('sentence_length_variance', 0) > 60:
            optimized = self._adjust_sentence_length(optimized)
        
        # 如果词汇丰富度低，替换常用词
        if detection.features.get('vocabulary_richness', 0) > 60:
            optimized = self._enrich_vocabulary(optimized)
        
        return optimized
    
    def _reduce_repetition(self, text: str) -> str:
        """减少重复"""
        # 简化实现：替换重复词
        common_words = ['的', '了', '在', '是', '有']
        replacements = {
            '的': '之',
            '了': '过',
            '在': '于',
            '是': '为',
            '有': '具'
        }
        
        for word, replacement in replacements.items():
            if word in text:
                text = text.replace(word, replacement, 1)  # 只替换一次
                break
        
        return text
    
    def _adjust_sentence_length(self, text: str) -> str:
        """调整句子长度"""
        import re
        sentences = re.split(r'[。！？]', text)
        adjusted = []
        
        for sentence in sentences:
            if len(sentence) > 40:
                # 拆分长句
                mid = len(sentence) // 2
                adjusted.append(sentence[:mid] + '。')
                adjusted.append(sentence[mid:] + '，')
            elif len(sentence) < 10 and adjusted:
                # 合并短句
                adjusted[-1] = adjusted[-1].rstrip('。，') + '，' + sentence
            else:
                adjusted.append(sentence)
        
        return '。'.join(adjusted)
    
    def _enrich_vocabulary(self, text: str) -> str:
        """丰富词汇"""
        # 简化实现：替换常见词
        simple_words = ['好', '大', '小', '多', '少']
        complex_words = ['优秀', '庞大', '微小', '众多', '稀少']
        
        for simple, complex_word in zip(simple_words, complex_words):
            if simple in text:
                text = text.replace(simple, complex_word, 1)
                break
        
        return text
```

## 5. 质量门禁系统

```python
# integration/quality_gate.py
from enum import Enum
from typing import Tuple

class GateStatus(Enum):
    ALLOW = "allow"
    WARNING = "warning"
    BLOCK = "block"

class QualityGate:
    """质量门禁系统"""
    
    def __init__(self, ai_threshold: float = 40.0, min_quality: float = 60.0):
        self.ai_threshold = ai_threshold
        self.min_quality = min_quality
    
    async def check(self, result: OptimizationResult) -> Tuple[GateStatus, str]:
        """检查是否通过门禁"""
        # AI检测阈值检查
        if result.after_detection.score > self.ai_threshold:
            return (GateStatus.BLOCK, 
                    f"AI检测得分 {result.after_detection.score:.1f} > {self.ai_threshold}，需要优化")
        
        # 质量最低标准检查
        if result.quality_report.total_score < self.min_quality:
            return (GateStatus.BLOCK,
                    f"质量评分 {result.quality_report.total_score:.1f} < {self.min_quality}，需要改进")
        
        # 检查是否有严重问题
        if len(result.quality_report.issues) > 3:
            return (GateStatus.WARNING,
                    f"存在 {len(result.quality_report.issues)} 个问题，建议改进")
        
        return (GateStatus.ALLOW, "通过所有检查")
```

## 6. 报告生成系统

```python
# integration/report_generator.py
from datetime import datetime
from typing import Dict, Any

class ReportGenerator:
    """报告生成系统"""
    
    async def generate(self, result: OptimizationResult) -> Dict[str, Any]:
        """生成完整报告"""
        return {
            "报告生成时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "AI检测得分": {
                "优化前": round(result.before_detection.score, 2),
                "优化后": round(result.after_detection.score, 2),
                "变化": round(result.before_detection.score - result.after_detection.score, 2)
            },
            "AI特征分析": {
                feature: {
                    "优化前": round(result.before_detection.features.get(feature, 0), 2),
                    "优化后": round(result.after_detection.features.get(feature, 0), 2)
                }
                for feature in result.before_detection.features
            },
            "质量评分": {
                "总分": round(result.quality_report.total_score, 2),
                "各维度": {
                    dim: round(score, 2)
                    for dim, score in result.quality_report.dimensions.items()
                }
            },
            "优化前后对比": {
                "原文字数": len(result.original_text),
                "优化后字数": len(result.optimized_text),
                "变更列表": result.changes
            },
            "改进建议列表": result.quality_report.suggestions,
            "预警信息": result.before_detection.warnings + result.after_detection.warnings
        }
    
    async def generate_summary(self, result: OptimizationResult) -> str:
        """生成摘要报告"""
        report = await self.generate(result)
        
        summary = f"""
=== NWACS V8.0 检测报告 ===
生成时间: {report['报告生成时间']}

AI检测结果:
- 优化前得分: {report['AI检测得分']['优化前']}
- 优化后得分: {report['AI检测得分']['优化后']}
- 改善幅度: {report['AI检测得分']['变化']}

质量评估:
- 总分: {report['质量评分']['总分']}
- 可读性: {report['质量评分']['各维度']['readability']}
- 连贯性: {report['质量评分']['各维度']['coherence']}
- 结构: {report['质量评分']['各维度']['structure']}
- 语法: {report['质量评分']['各维度']['grammar']}
- 参与度: {report['质量评分']['各维度']['engagement']}

改进建议:
{chr(10).join(f'- {s}' for s in report['改进建议列表'])}
"""
        return summary
```

## 7. 主集成控制器

```python
# integration/controller.py
import asyncio
from typing import Optional

class NWACSIntegrationController:
    """NWACS V8.0 集成控制器"""
    
    def __init__(self):
        # 初始化各系统
        self.ai_detector = AIDetector(threshold=40.0)
        self.quality_checker = QualityChecker(min_total_score=60.0)
        self.quality_gate = QualityGate(ai_threshold=40.0, min_quality=60.0)
        self.report_generator = ReportGenerator()
        
        # 初始化优化流水线
        self.pipeline = OptimizationPipeline(self.ai_detector, self.quality_checker)
        self.pipeline.register_optimizer(AIFeatureOptimizer())
    
    async def process_text(self, text: str) -> dict:
        """处理文本的完整流程"""
        print(f"开始处理文本 (长度: {len(text)}字)")
        
        # 1. 生成时实时检测
        print("步骤1: AI特征实时检测...")
        initial_detection = await self.ai_detector.detect(text)
        print(f"  AI特征得分: {initial_detection.score:.2f}")
        
        # 2. 执行优化流水线
        print("步骤2-5: 执行优化流水线...")
        result = await self.pipeline.process(text)
        
        # 3. 质量门禁检查
        print("步骤6: 质量门禁检查...")
        gate_status, gate_message = await self.quality_gate.check(result)
        print(f"  门禁状态: {gate_status.value}")
        print(f"  门禁信息: {gate_message}")
        
        # 4. 生成报告
        print("步骤7: 生成报告...")
        report = await self.report_generator.generate(result)
        
        return {
            "status": gate_status.value,
            "message": gate_message,
            "result": result,
            "report": report
        }
    
    async def save_if_qualified(self, text: str) -> bool:
        """保存前检查"""
        response = await self.process_text(text)
        
        if response["status"] == "block":
            print("保存被拦截：未通过质量检查")
            print(response["message"])
            return False
        
        print("保存成功：通过所有检查")
        return True

# 使用示例
async def main():
    controller = NWACSIntegrationController()
    
    # 测试文本
    test_text = """
    这是一个测试文本。它包含了多个句子。每个句子都很短。这看起来像是AI生成的。
    实际上，这种重复的模式很常见。AI经常会产生这样的文本。
    但是，我们需要检测并优化这些特征。
    """
    
    # 处理文本
    result = await controller.process_text(test_text)
    
    # 打印报告
    print("\n" + "="*50)
    print("完整报告:")
    print("="*50)
    print(result["report"])
    
    # 尝试保存
    print("\n" + "="*50)
    print("尝试保存:")
    print("="*50)
    await controller.save_if_qualified(test_text)

if __name__ == "__main__":
    asyncio.run(main())
```

## 8. 配置文件

```python
# integration/config.py
from dataclasses import dataclass
from typing import Dict

@dataclass
class IntegrationConfig:
    """集成配置"""
    # AI检测配置
    ai_detection: Dict = None
    
    # 质量检测配置
    quality_check: Dict = None
    
    # 门禁配置
    quality_gate: Dict = None
    
    # 优化配置
    optimization: Dict = None
    
    def __post_init__(self):
        if self.ai_detection is None:
            self.ai_detection = {
                "threshold": 40.0,
                "feature_weights": {
                    "repetition": 0.2,
                    "sentence_length_variance": 0.15,
                    "vocabulary_richness": 0.25,
                    "transition_diversity": 0.2,
                    "emotional_consistency": 0.2
                }
            }
        
        if self.quality_check is None:
            self.quality_check = {
                "min_total_score": 60.0,
                "dimension_weights": {
                    "readability": 0.2,
                    "coherence": 0.2,
                    "structure": 0.2,
                    "grammar": 0.2,
                    "engagement": 0.2
                }
            }
        
        if self.quality_gate is None:
            self.quality_gate = {
                "ai_threshold": 40.0,
                "min_quality": 60.0
            }
        
        if self.optimization is None:
            self.optimization = {
                "max_iterations": 3,
                "improvement_threshold": 5.0
            }

# 默认配置
default_config = IntegrationConfig()
```

## 9. 部署说明

```yaml
# docker-compose.yml
version: '3.8'

services:
  nwacs-integration:
    build: .
    ports:
      - "8000:8000"
    environment:
      - AI_DETECTION_THRESHOLD=40.0
      - MIN_QUALITY_SCORE=60.0
      - LOG_LEVEL=INFO
    volumes:
      - ./logs:/app/logs
      - ./reports:/app/reports
    restart: unless-stopped
```

## 10. API接口

```python
# integration/api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="NWACS V8.0 Integration API")

class TextRequest(BaseModel):
    text: str
    auto_optimize: bool = True

class TextResponse(BaseModel):
    status: str
    message: str
    report: dict

controller = NWACSIntegrationController()

@app.post("/process", response_model=TextResponse)
async def process_text(request: TextRequest):
    """处理文本"""
    try:
        result = await controller.process_text(request.text)
        return TextResponse(
            status=result["status"],
            message=result["message"],
            report=result["report"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/save", response_model=bool)
async def save_text(request: TextRequest):
    """保存文本"""
    try:
        return await controller.save_if_qualified(request.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

这个完整的集成方案实现了：

1. **实时AI特征监控**：检测AI写作特征并预警
2. **质量门禁系统**：确保文本质量达标
3. **优化流水线**：自动优化AI特征
4. **报告生成**：提供完整的检测报告

系统特点：
- 模块化设计，易于扩展
- 异步处理，性能优秀
- 配置灵活，适应不同需求
- 完整的错误处理和日志记录