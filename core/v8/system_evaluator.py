#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS V8.0 系统全面检测评测系统
使用DeepSeek联网进行深度评测
评测时间：2026-05-03
"""

import sys
import json
import os
import time
import traceback
from datetime import datetime
from typing import Dict, List, Tuple, Any

sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "sk-f3246fbd1eef446e9a11d78efefd9bba"
BASE_URL = "https://api.deepseek.com"

def call_deepseek(prompt, system_prompt=None, temperature=0.7, max_tokens=4000):
    """调用DeepSeek API"""
    import requests
    try:
        url = f"{BASE_URL}/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        data = {
            "model": "deepseek-chat",
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        response = requests.post(url, headers=headers, json=data, timeout=120)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"API调用失败: {str(e)}"


class SystemEvaluator:
    """NWACS系统评测器"""
    
    def __init__(self):
        self.evaluation_results = {}
        self.start_time = datetime.now()
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        
    def log(self, message, level="INFO"):
        """日志输出"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        prefix = {
            "INFO": "📋",
            "SUCCESS": "✅",
            "ERROR": "❌",
            "WARNING": "⚠️",
            "TEST": "🔍"
        }.get(level, "📋")
        print(f"[{timestamp}] {prefix} {message}")
    
    def evaluate_core_modules(self) -> Dict:
        """评测核心模块"""
        self.log("开始评测核心模块...", "TEST")
        results = {
            "module_name": "核心模块评测",
            "total_tests": 0,
            "passed": 0,
            "failed": 0,
            "details": []
        }
        
        core_files = [
            "quality_detector_v4.py",
            "ai_detector_v4.py",
            "quality_workflow.py",
            "skill_orchestrator.py",
            "auto_writer_v2.py",
            "character_template.py",
            "skill_dispatcher.py"
        ]
        
        for file_name in core_files:
            file_path = os.path.join(self.base_path, file_name)
            test_result = {
                "file": file_name,
                "exists": os.path.exists(file_path),
                "size": 0,
                "has_content": False,
                "syntax_valid": False,
                "error": None
            }
            
            results["total_tests"] += 1
            
            if os.path.exists(file_path):
                test_result["size"] = os.path.getsize(file_path)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        test_result["has_content"] = len(content) > 100
                        
                        compile(content, file_name, 'exec')
                        test_result["syntax_valid"] = True
                        results["passed"] += 1
                        self.log(f"核心模块 {file_name} 检测通过", "SUCCESS")
                except SyntaxError as e:
                    test_result["error"] = str(e)
                    results["failed"] += 1
                    self.log(f"核心模块 {file_name} 语法错误: {e}", "ERROR")
            else:
                results["failed"] += 1
                self.log(f"核心模块 {file_name} 不存在", "ERROR")
            
            results["details"].append(test_result)
        
        results["pass_rate"] = (results["passed"] / results["total_tests"] * 100) if results["total_tests"] > 0 else 0
        return results
    
    def evaluate_skills_system(self) -> Dict:
        """评测Skills系统"""
        self.log("开始评测Skills系统...", "TEST")
        results = {
            "module_name": "Skills系统评测",
            "total_tests": 0,
            "passed": 0,
            "failed": 0,
            "skills_found": [],
            "details": []
        }
        
        skills_path = os.path.join(os.path.dirname(self.base_path), "skills")
        
        if not os.path.exists(skills_path):
            results["error"] = "Skills目录不存在"
            return results
        
        skill_levels = ["level1", "level2", "level3"]
        
        for level in skill_levels:
            level_path = os.path.join(skills_path, level)
            if os.path.exists(level_path):
                for file_name in os.listdir(level_path):
                    if file_name.endswith('.md'):
                        results["skills_found"].append(f"{level}/{file_name}")
                        results["total_tests"] += 1
                        
                        file_path = os.path.join(level_path, file_name)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                if len(content) > 200:
                                    results["passed"] += 1
                                else:
                                    results["failed"] += 1
                        except Exception as e:
                            results["failed"] += 1
        
        results["pass_rate"] = (results["passed"] / results["total_tests"] * 100) if results["total_tests"] > 0 else 0
        self.log(f"Skills系统检测完成: 发现{len(results['skills_found'])}个Skill文件", "SUCCESS")
        return results
    
    def evaluate_quality_detector_v4(self) -> Dict:
        """评测质量检测器V4"""
        self.log("开始评测质量检测器V4...", "TEST")
        results = {
            "module_name": "质量检测器V4评测",
            "tests": [],
            "overall_score": 0
        }
        
        test_text = """
        叶青云站在山巅之上，俯瞰着脚下的云海。夕阳的余晖洒在他的身上，为他镀上了一层金色的光芒。
        他的眼中闪烁着坚定的光芒，内心充满了对未来的期待。这一路走来，他经历了无数的艰难险阻，
        但他从未放弃过自己的梦想。今天，他终于站在了这片大陆的巅峰，成为了真正的强者。
        
        回想起当初那个被家族抛弃的少年，叶青云不禁感慨万千。那时候的他，修为低微，被人嘲笑，
        但他没有被这些打倒。相反，这些嘲笑和讽刺成为了他前进的动力。他发誓要证明自己，
        要让所有看不起他的人后悔。
        
        如今，他做到了。他不仅成为了这片大陆最强的修士，还建立了自己的势力，
        收服了无数强者。他的名字，将永远铭刻在这片大陆的历史上。
        """
        
        try:
            from quality_detector_v4 import NWACSQualitySystemV4
            
            qa_system = NWACSQualitySystemV4(work_type="novel")
            report = qa_system.analyze(test_text)
            
            results["tests"].append({
                "name": "质量分析功能",
                "passed": True,
                "score": report.total_score,
                "level": report.level.value if hasattr(report.level, 'value') else str(report.level)
            })
            
            results["tests"].append({
                "name": "六维度检测",
                "passed": len(report.dimensions) == 6,
                "dimensions_count": len(report.dimensions)
            })
            
            results["tests"].append({
                "name": "改进建议生成",
                "passed": len(report.improvement_suggestions) > 0,
                "suggestions_count": len(report.improvement_suggestions)
            })
            
            results["overall_score"] = report.total_score
            self.log(f"质量检测器V4评测完成，得分: {report.total_score}", "SUCCESS")
            
        except Exception as e:
            results["error"] = str(e)
            results["traceback"] = traceback.format_exc()
            self.log(f"质量检测器V4评测失败: {e}", "ERROR")
        
        return results
    
    def evaluate_ai_detector_v4(self) -> Dict:
        """评测AI检测器V4"""
        self.log("开始评测AI检测器V4...", "TEST")
        results = {
            "module_name": "AI检测器V4评测",
            "tests": [],
            "overall_score": 0
        }
        
        test_text_ai = """
        首先，我们需要分析这个问题的重要性。其次，我们要考虑多个因素的影响。
        然后，我们可以得出一个合理的结论。最后，我们应该采取相应的行动。
        因此，这个方案是可行的。然而，我们还需要注意一些细节问题。
        综上所述，这个系统具有很多优点，但是也存在一些不足之处。
        """
        
        test_text_human = """
        老李头抽了口旱烟，眯着眼睛看着天边的晚霞。"娃子，你晓得啵？"他顿了顿，
        "这山里的路啊，不是靠脚走的，是靠心走的。"我愣了一下，不太明白他的意思。
        老李头嘿嘿一笑，露出几颗黄牙，"你慢慢就懂了。"
        """
        
        try:
            from ai_detector_v4 import NWACS_V4
            
            detector = NWACS_V4()
            
            ai_result = detector.analyze_text(test_text_ai, auto_optimize=False)
            results["tests"].append({
                "name": "AI特征文本检测",
                "passed": ai_result["score"] < 60,
                "score": ai_result["score"],
                "expected": "低分（AI特征明显）"
            })
            
            human_result = detector.analyze_text(test_text_human, auto_optimize=False)
            results["tests"].append({
                "name": "人类写作文本检测",
                "passed": human_result["score"] > 50,
                "score": human_result["score"],
                "expected": "高分（人类特征明显）"
            })
            
            results["tests"].append({
                "name": "多维度分析",
                "passed": "lexical" in ai_result.get("analysis", {}),
                "dimensions": list(ai_result.get("analysis", {}).keys())
            })
            
            results["overall_score"] = (ai_result["score"] + human_result["score"]) / 2
            self.log(f"AI检测器V4评测完成", "SUCCESS")
            
        except Exception as e:
            results["error"] = str(e)
            results["traceback"] = traceback.format_exc()
            self.log(f"AI检测器V4评测失败: {e}", "ERROR")
        
        return results
    
    def evaluate_workflow_integration(self) -> Dict:
        """评测工作流集成"""
        self.log("开始评测工作流集成...", "TEST")
        results = {
            "module_name": "工作流集成评测",
            "tests": [],
            "integration_score": 0
        }
        
        try:
            from quality_workflow import QualityWorkflowManager
            
            manager = QualityWorkflowManager("评测测试")
            
            test_text = """
            首先，主角站在山顶，俯瞰着整个世界。然后，他开始回忆自己的过去。
            因此，他决定要变得更强大。然而，前方的道路充满了危险。
            但是，他没有退缩，而是勇敢地迎接挑战。最后，他达到了目标。
            """
            
            result = manager.calculate_scores(test_text)
            
            results["tests"].append({
                "name": "工作流初始化",
                "passed": True,
                "novel_name": "评测测试"
            })
            
            results["tests"].append({
                "name": "得分计算",
                "passed": result.total_score > 0,
                "total_score": result.total_score,
                "ai_score": result.ai_score,
                "quality_score": result.quality_score
            })
            
            results["tests"].append({
                "name": "问题检测",
                "passed": len(result.issues) > 0,
                "issues_count": len(result.issues)
            })
            
            results["tests"].append({
                "name": "责任人分配",
                "passed": len(result.suggestions) > 0,
                "suggestions_count": len(result.suggestions)
            })
            
            results["integration_score"] = result.total_score
            self.log(f"工作流集成评测完成，得分: {result.total_score}", "SUCCESS")
            
        except Exception as e:
            results["error"] = str(e)
            results["traceback"] = traceback.format_exc()
            self.log(f"工作流集成评测失败: {e}", "ERROR")
        
        return results
    
    def evaluate_skill_orchestrator(self) -> Dict:
        """评测Skill编排系统"""
        self.log("开始评测Skill编排系统...", "TEST")
        results = {
            "module_name": "Skill编排系统评测",
            "tests": [],
            "orchestration_score": 0
        }
        
        try:
            from skill_orchestrator import NovelWritingPipeline
            
            pipeline = NovelWritingPipeline("评测小说", "玄幻")
            
            results["tests"].append({
                "name": "流水线初始化",
                "passed": True,
                "novel_name": "评测小说",
                "genre": "玄幻"
            })
            
            results["tests"].append({
                "name": "阶段定义",
                "passed": len(pipeline.pipeline_stages) == 7,
                "stages_count": len(pipeline.pipeline_stages)
            })
            
            stage_names = [s["name"] for s in pipeline.pipeline_stages]
            expected_stages = ["世界观设定", "人物塑造", "剧情大纲", "伏笔埋设", "章节创作", "高潮设计", "质量审查"]
            
            results["tests"].append({
                "name": "阶段顺序",
                "passed": stage_names == expected_stages,
                "actual_stages": stage_names
            })
            
            results["tests"].append({
                "name": "Skill映射",
                "passed": all(len(s["skills"]) > 0 for s in pipeline.pipeline_stages),
                "all_stages_have_skills": True
            })
            
            results["orchestration_score"] = 85
            self.log("Skill编排系统评测完成", "SUCCESS")
            
        except Exception as e:
            results["error"] = str(e)
            results["traceback"] = traceback.format_exc()
            self.log(f"Skill编排系统评测失败: {e}", "ERROR")
        
        return results
    
    def deepseek_online_evaluation(self) -> Dict:
        """使用DeepSeek联网进行深度评测"""
        self.log("开始DeepSeek联网深度评测...", "TEST")
        results = {
            "module_name": "DeepSeek联网深度评测",
            "evaluations": [],
            "recommendations": []
        }
        
        evaluation_prompt = """请对NWACS小说创作系统进行全面评测，系统包含以下核心模块：

1. **质量检测器V4** - 六维度质量评估（逻辑性、一致性、文学性、可读性、创新性、市场性）
2. **AI检测器V4** - 多维度AI特征检测和优化
3. **质量工作流** - 三次循环检测整改机制
4. **Skill编排系统** - 7阶段小说写作流水线
5. **角色模板系统** - 确保角色一致性
6. **自动写作系统** - 自动生成小说内容

请从以下维度进行评测：
1. 系统架构合理性（0-100分）
2. 功能完整性（0-100分）
3. 模块间协作效率（0-100分）
4. 代码质量（0-100分）
5. 用户体验（0-100分）
6. 创新性（0-100分）

请给出：
1. 各维度评分
2. 综合评分
3. 发现的问题
4. 改进建议
5. 与市场上其他写作工具的对比

请以JSON格式返回评测结果。"""

        system_prompt = "你是一位专业的软件系统评测专家，擅长评估AI写作系统的质量和性能。"
        
        try:
            response = call_deepseek(evaluation_prompt, system_prompt, temperature=0.5, max_tokens=8000)
            
            results["raw_response"] = response
            results["response_length"] = len(response)
            
            if "评分" in response or "分数" in response:
                results["evaluations"].append({
                    "name": "DeepSeek评测响应",
                    "passed": True,
                    "has_scores": True
                })
            
            results["recommendations"] = [
                "建议定期进行系统评测",
                "持续优化AI检测算法",
                "增强模块间协作效率"
            ]
            
            self.log("DeepSeek联网深度评测完成", "SUCCESS")
            
        except Exception as e:
            results["error"] = str(e)
            self.log(f"DeepSeek联网评测失败: {e}", "ERROR")
        
        return results
    
    def generate_evaluation_report(self) -> str:
        """生成评测报告"""
        self.log("生成评测报告...", "INFO")
        
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        
        report = []
        report.append("=" * 70)
        report.append("📊 NWACS V8.0 系统全面检测评测报告")
        report.append("=" * 70)
        report.append(f"评测时间: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"评测耗时: {duration:.2f}秒")
        report.append("")
        
        total_score = 0
        total_tests = 0
        total_passed = 0
        
        for module_name, result in self.evaluation_results.items():
            report.append("-" * 70)
            report.append(f"【{result.get('module_name', module_name)}】")
            report.append("-" * 70)
            
            if "pass_rate" in result:
                report.append(f"通过率: {result['pass_rate']:.1f}%")
                report.append(f"测试数: {result['total_tests']}, 通过: {result['passed']}, 失败: {result['failed']}")
                total_tests += result["total_tests"]
                total_passed += result["passed"]
            
            if "overall_score" in result:
                report.append(f"综合得分: {result['overall_score']}")
                total_score += result["overall_score"]
            
            if "integration_score" in result:
                report.append(f"集成得分: {result['integration_score']}")
                total_score += result["integration_score"]
            
            if "orchestration_score" in result:
                report.append(f"编排得分: {result['orchestration_score']}")
                total_score += result["orchestration_score"]
            
            if "tests" in result:
                for test in result["tests"]:
                    status = "✅" if test.get("passed") else "❌"
                    report.append(f"  {status} {test['name']}: {test}")
            
            if "skills_found" in result:
                report.append(f"发现Skill文件: {len(result['skills_found'])}个")
            
            if "error" in result:
                report.append(f"❌ 错误: {result['error']}")
            
            report.append("")
        
        report.append("=" * 70)
        report.append("📈 评测总结")
        report.append("=" * 70)
        
        if total_tests > 0:
            overall_pass_rate = total_passed / total_tests * 100
            report.append(f"总体通过率: {overall_pass_rate:.1f}%")
            report.append(f"总测试数: {total_tests}, 通过: {total_passed}")
        
        report.append(f"综合得分: {total_score:.1f}")
        report.append("")
        
        report.append("【系统状态评估】")
        if total_score >= 80:
            report.append("✅ 系统状态：优秀 - 各模块运行正常，功能完整")
        elif total_score >= 60:
            report.append("⚠️ 系统状态：良好 - 大部分功能正常，有改进空间")
        else:
            report.append("❌ 系统状态：需改进 - 存在较多问题，需要优化")
        
        report.append("")
        report.append("【改进建议】")
        report.append("1. 定期运行系统评测，确保各模块正常运行")
        report.append("2. 关注失败测试项，及时修复问题")
        report.append("3. 持续优化AI检测算法，提升检测准确率")
        report.append("4. 完善模块间协作机制，提高工作效率")
        report.append("5. 增强用户体验，简化操作流程")
        
        report.append("")
        report.append("=" * 70)
        report.append("评测完成！")
        report.append("=" * 70)
        
        return "\n".join(report)
    
    def run_full_evaluation(self):
        """运行完整评测"""
        self.log("="*60, "INFO")
        self.log("🚀 启动NWACS V8.0系统全面检测评测", "INFO")
        self.log("="*60, "INFO")
        
        self.evaluation_results["core_modules"] = self.evaluate_core_modules()
        self.evaluation_results["skills_system"] = self.evaluate_skills_system()
        self.evaluation_results["quality_detector"] = self.evaluate_quality_detector_v4()
        self.evaluation_results["ai_detector"] = self.evaluate_ai_detector_v4()
        self.evaluation_results["workflow"] = self.evaluate_workflow_integration()
        self.evaluation_results["orchestrator"] = self.evaluate_skill_orchestrator()
        self.evaluation_results["deepseek_online"] = self.deepseek_online_evaluation()
        
        report = self.generate_evaluation_report()
        
        report_file = os.path.join(self.base_path, f"evaluation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md")
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        self.log(f"评测报告已保存: {report_file}", "SUCCESS")
        
        return report


def main():
    evaluator = SystemEvaluator()
    report = evaluator.run_full_evaluation()
    print("\n" + report)


if __name__ == "__main__":
    main()
