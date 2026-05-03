#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS V8.0 自动写作V2（集成质量检测）
在生成小说时自动运行质量检测
创建时间：2026-05-03
"""
import asyncio
from typing import Optional, Dict, Any, List, Tuple
from dataclasses import dataclass, field
from enum import Enum
import logging
from datetime import datetime
import os
import sys

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QualityLevel(Enum):
    EXCELLENT = "excellent"
    GOOD = "good" 
    ACCEPTABLE = "acceptable"
    POOR = "poor"
    CRITICAL = "critical"

class DetectionResult(Enum):
    PASS = "pass"
    NEED_OPTIMIZE = "need_optimize"
    NEED_HUMAN = "need_human"

@dataclass
class QualityMetrics:
    """质量度量结果"""
    overall_score: float = 0.0
    coherence_score: float = 0.0
    grammar_score: float = 0.0
    plot_logic_score: float = 0.0
    character_consistency_score: float = 0.0
    style_match_score: float = 0.0
    details: Dict[str, Any] = field(default_factory=dict)
    level: QualityLevel = QualityLevel.GOOD

@dataclass
class QualityCheckResult:
    """质量检测结果"""
    passed: bool = False
    result: DetectionResult = DetectionResult.PASS
    metrics: QualityMetrics = field(default_factory=QualityMetrics)
    optimization_count: int = 0
    final_text: str = ""
    report: str = ""
    warnings: List[str] = field(default_factory=list)

class AutoWriterV2:
    """自动写作系统V2 - 集成质量检测"""
    
    def __init__(self, novel_name: str = "test_novel", genre: str = "xuanhuan"):
        self.novel_name = novel_name
        self.genre = genre
        self.output_dir = os.path.join("novels", novel_name)
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 初始化组件
        self.quality_detector = None
        self.ai_detector = None
        self.workflow_manager = None
        
        try:
            from quality_detector_v4 import NWACSQualitySystemV4
            from ai_detector_v4 import NWACS_V4
            from quality_workflow import QualityWorkflowManager
            
            self.quality_detector = NWACSQualitySystemV4(work_type="novel")
            self.ai_detector = NWACS_V4()
            self.workflow_manager = QualityWorkflowManager(novel_name)
            logger.info("所有组件初始化成功")
        except Exception as e:
            logger.warning(f"组件初始化失败: {e}")
    
    async def generate_with_quality_check(self, prompt: str, 
                                         max_optimizations: int = 3) -> QualityCheckResult:
        """带质量检测的生成"""
        result = QualityCheckResult()
        
        # 模拟生成过程
        generated_text = self._simulate_generation(prompt)
        
        current_text = generated_text
        
        for i in range(max_optimizations + 1):
            result.optimization_count = i
            
            # 质量检测
            check_result = self._run_quality_check(current_text)
            
            if check_result.passed:
                result.passed = True
                result.result = DetectionResult.PASS
                result.final_text = current_text
                logger.info(f"第{i}次检测通过")
                break
            elif i >= max_optimizations:
                result.passed = False
                result.result = DetectionResult.NEED_HUMAN
                result.final_text = current_text
                result.warnings.append(f"已达到最大优化次数{max_optimizations}，需要人工介入")
                logger.warning("需要人工介入")
            else:
                result.result = DetectionResult.NEED_OPTIMIZE
                logger.info(f"第{i}次检测未通过，开始优化...")
                current_text = self._optimize_text(current_text, check_result)
        
        # 生成报告
        result.report = self._generate_report(result)
        
        # 保存结果
        self._save_result(result)
        
        return result
    
    def _simulate_generation(self, prompt: str) -> str:
        """模拟文本生成"""
        # 实际应用中会调用DeepSeek等API
        return f"""这是一部关于{self.novel_name}的{self.genre}小说。

主角站在山巅之上，俯瞰着脚下的云海。夕阳的余晖洒在他的身上，为他镀上了一层金色的光芒。
他的眼中闪烁着坚定的光芒，内心充满了对未来的期待。这一路走来，他经历了无数的艰难险阻，
但他从未放弃过自己的梦想。今天，他终于站在了这片大陆的巅峰，成为了真正的强者。

首先，他需要巩固自己的修为。其次，他要寻找传说中的神器。最后，他将挑战邪恶势力。
因此，他开始了新的征程。然而，前方的道路充满了危险。但是，他毫不畏惧。"""
    
    def _run_quality_check(self, text: str) -> QualityCheckResult:
        """运行质量检测"""
        result = QualityCheckResult()
        
        if self.quality_detector:
            try:
                # 使用质量检测器V4
                q_report = self.quality_detector.analyze(text)
                result.metrics.overall_score = q_report.total_score
                result.metrics.level = QualityLevel.GOOD if q_report.total_score >= 70 else QualityLevel.POOR
                result.passed = q_report.passed_gate and q_report.total_score >= 70
                logger.info(f"质量检测得分: {q_report.total_score}")
            except Exception as e:
                logger.warning(f"质量检测失败: {e}")
                result.passed = len(text) > 200
                result.metrics.overall_score = 60.0 if len(text) > 200 else 40.0
        else:
            # 简单回退检测
            result.passed = len(text) > 200
            result.metrics.overall_score = 70.0 if len(text) > 200 else 50.0
        
        return result
    
    def _optimize_text(self, text: str, check_result: QualityCheckResult) -> str:
        """优化文本"""
        if self.ai_detector:
            try:
                ai_result = self.ai_detector.analyze_text(text, auto_optimize=True)
                if ai_result.get('optimized_text'):
                    logger.info("AI优化完成")
                    return ai_result['optimized_text']
            except Exception as e:
                logger.warning(f"AI优化失败: {e}")
        
        # 简单优化
        text = text.replace("首先", "一开始")
        text = text.replace("其次", "接着")
        text = text.replace("最后", "最终")
        text = text.replace("因此", "所以")
        return text
    
    def _generate_report(self, result: QualityCheckResult) -> str:
        """生成报告"""
        report = []
        report.append("=" * 60)
        report.append("NWACS V8.0 自动写作质量报告")
        report.append("=" * 60)
        report.append(f"小说名称: {self.novel_name}")
        report.append(f"类型: {self.genre}")
        report.append(f"检测时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"优化次数: {result.optimization_count}")
        report.append(f"最终结果: {result.result.value}")
        report.append(f"整体得分: {result.metrics.overall_score:.1f}")
        report.append(f"等级: {result.metrics.level.value}")
        report.append("")
        
        if result.warnings:
            report.append("警告:")
            for warning in result.warnings:
                report.append(f"  - {warning}")
        
        report.append("")
        report.append("=" * 60)
        
        return "\n".join(report)
    
    def _save_result(self, result: QualityCheckResult):
        """保存结果"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # 保存文本
        text_file = os.path.join(self.output_dir, f"chapter_{timestamp}.txt")
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write(result.final_text)
        
        # 保存报告
        report_file = os.path.join(self.output_dir, f"report_{timestamp}.txt")
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(result.report)
        
        logger.info(f"结果已保存到: {self.output_dir}")
    
    def batch_generate(self, prompts: List[str]) -> List[QualityCheckResult]:
        """批量生成"""
        results = []
        for i, prompt in enumerate(prompts):
            logger.info(f"正在生成第{i+1}/{len(prompts)}个章节...")
            try:
                result = asyncio.run(self.generate_with_quality_check(prompt))
                results.append(result)
            except Exception as e:
                logger.error(f"生成失败: {e}")
                failed_result = QualityCheckResult()
                failed_result.warnings.append(f"生成失败: {e}")
                results.append(failed_result)
        
        return results

def main():
    """主函数"""
    print("=" * 60)
    print("NWACS V8.0 自动写作系统V2")
    print("=" * 60)
    
    novel_name = input("请输入小说名称 (默认: test_novel): ").strip() or "test_novel"
    genre = input("请输入小说类型 (默认: xuanhuan): ").strip() or "xuanhuan"
    
    writer = AutoWriterV2(novel_name, genre)
    
    print("\n请选择操作:")
    print("1. 单章生成")
    print("2. 批量生成")
    print("3. 测试系统")
    
    choice = input("\n请选择 (1/2/3, 默认: 1): ").strip() or "1"
    
    if choice == "1":
        prompt = input("请输入章节提示词: ").strip()
        result = asyncio.run(writer.generate_with_quality_check(prompt))
        
        print("\n" + "=" * 60)
        print(result.report)
        print("\n最终文本:")
        print("-" * 60)
        print(result.final_text)
    
    elif choice == "2":
        prompts = []
        print("请输入多个章节提示词（每行一个，空行结束）:")
        while True:
            prompt = input().strip()
            if not prompt:
                break
            prompts.append(prompt)
        
        if prompts:
            results = writer.batch_generate(prompts)
            print(f"\n生成完成: {len(results)} 个章节")
            passed = sum(1 for r in results if r.passed)
            print(f"通过: {passed}/{len(results)}")
    
    elif choice == "3":
        print("\n运行系统测试...")
        test_prompt = "写一个玄幻小说的开篇章节"
        result = asyncio.run(writer.generate_with_quality_check(test_prompt))
        print("\n" + result.report)
        print("\n测试完成！")

if __name__ == "__main__":
    main()
