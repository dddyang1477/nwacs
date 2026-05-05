#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS项目DeepSeek评测工具
使用DeepSeek对项目进行全面评测，分析功能、查找不足、提出优化建议
"""

import os
import json
import time
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

try:
    from openai import OpenAI
except ImportError:
    print("❌ 请先安装 openai 库：pip install openai")
    exit(1)


class NWACSEvaluator:
    """NWACS DeepSeek评测工具"""

    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise ValueError("❌ 请设置 DEEPSEEK_API_KEY")

        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.deepseek.com"
        )

        self.project_root = Path(__file__).parent
        self.report_path = self.project_root / "logs" / "deepseek_evaluation"
        self.report_path.mkdir(parents=True, exist_ok=True)

        print("🚀 NWACS DeepSeek评测工具启动")
        print(f"📍 项目根目录: {self.project_root}")
        print("-"*60)

    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")

    def scan_project_structure(self):
        """扫描项目结构"""
        self.log("🔍 扫描项目结构...")

        structure = {
            "directories": {},
            "python_files": [],
            "markdown_files": [],
            "json_files": [],
            "batch_files": [],
            "skill_files": {
                "level3": [],
                "level2": [],
                "level1": []
            },
            "knowledge_files": []
        }

        for root, dirs, files in os.walk(self.project_root):
            rel_root = Path(root).relative_to(self.project_root)

            if ".git" in str(rel_root) or "__pycache__" in str(rel_root) or "archive" in str(rel_root):
                continue

            structure["directories"][str(rel_root)] = len(files)

            for file in files:
                filepath = Path(root) / file

                if file.endswith('.py'):
                    structure["python_files"].append(str(filepath.relative_to(self.project_root)))
                elif file.endswith('.md'):
                    structure["markdown_files"].append(str(filepath.relative_to(self.project_root)))
                elif file.endswith('.json'):
                    structure["json_files"].append(str(filepath.relative_to(self.project_root)))
                elif file.endswith('.bat'):
                    structure["batch_files"].append(str(filepath.relative_to(self.project_root)))

                if "skills/level3" in str(rel_root):
                    structure["skill_files"]["level3"].append(file)
                elif "skills/level2" in str(rel_root):
                    structure["skill_files"]["level2"].append(file)
                elif "skills/level1" in str(rel_root):
                    structure["skill_files"]["level1"].append(file)

                if "skills/level2/learnings" in str(rel_root):
                    structure["knowledge_files"].append(file)

        self.log(f"✅ 扫描完成：{len(structure['python_files'])} Python文件，{len(structure['markdown_files'])} Markdown文件")
        return structure

    def read_key_files(self, structure):
        """读取关键文件内容"""
        self.log("📖 读取关键文件...")

        key_files_content = {}

        key_file_list = [
            "docs/architecture/01_系统架构框架.md",
            "项目状态报告.md",
            "deepseek_learning_engine.py",
            "skills/level2/learnings/00_知识库共享中心索引.txt"
        ]

        for filepath in key_file_list:
            fp = self.project_root / filepath
            if fp.exists():
                try:
                    with open(fp, 'r', encoding='utf-8') as f:
                        content = f.read(5000)  # 限制大小，避免过长
                    key_files_content[filepath] = content
                except Exception as e:
                    key_files_content[filepath] = f"读取失败: {e}"

        self.log(f"✅ 已读取 {len(key_files_content)} 个关键文件")
        return key_files_content

    def evaluate_with_deepseek(self, structure, key_files_content):
        """使用DeepSeek进行全面评测"""
        self.log("🧠 使用DeepSeek进行项目评测...")

        system_prompt = """你是一个专业的AI项目评测专家。你需要对NWACS（Novel Writing AI Collaborative System）项目进行全面评测。

请从以下方面进行评测：
1. 功能完整性 - 所有功能是否正常，是否有缺失
2. 架构合理性 - 项目结构是否合理，是否需要优化
3. 文档完整性 - 文档是否齐全，是否足够清晰
4. 代码质量 - 代码是否规范，是否有潜在问题
5. 可扩展性 - 项目是否容易扩展和维护
6. 用户体验 - 上手难度如何，是否需要改进
7. 优化建议 - 具体的改进建议和优化方案

请给出详细、专业、可执行的评测报告。"""

        user_prompt = f"""请对NWACS项目进行全面评测。以下是项目信息：

---
项目结构统计：
- Python文件：{len(structure['python_files'])} 个
- Markdown文档：{len(structure['markdown_files'])} 个
- JSON配置：{len(structure['json_files'])} 个
- 启动脚本：{len(structure['batch_files'])} 个
- 三级Skill：{len(structure['skill_files']['level3'])} 个
- 二级Skill：{len(structure['skill_files']['level2'])} 个
- 知识库文件：{len(structure['knowledge_files'])} 个

---
关键文件内容：
"""

        for filepath, content in key_files_content.items():
            user_prompt += f"\n{'='*60}\n📄 {filepath}\n{'='*60}\n{content}\n"

        user_prompt += """
---
请进行全面评测，输出格式：
{
  "evaluation_summary": "总体评价",
  "score": {
    "functionality": 0-10,
    "architecture": 0-10,
    "documentation": 0-10,
    "code_quality": 0-10,
    "extendability": 0-10,
    "user_experience": 0-10,
    "overall": 0-10
  },
  "strengths": ["优点1", "优点2"],
  "weaknesses": ["缺点1", "缺点2"],
  "optimization_suggestions": [
    {"priority": "high/medium/low", "suggestion": "建议内容", "expected_benefit": "预期收益"}
  ],
  "feature_recommendations": ["推荐的新功能1", "推荐的新功能2"]
}
"""

        try:
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=3000
            )

            result = response.choices[0].message.content

            # 尝试解析JSON，如果不能，就保留原文
            try:
                result_json = json.loads(result)
                return result_json
            except:
                return {"raw_text": result}

        except Exception as e:
            self.log(f"❌ DeepSeek评测失败: {e}")
            return {"error": str(e)}

    def generate_report(self, structure, key_files_content, evaluation):
        """生成评测报告"""
        report_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.report_path / f"NWACS深度评测_{report_time}.md"

        report = f"""# NWACS项目深度评测报告

**评测时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**评测工具**: DeepSeek API
**工具版本**: NWACSEvaluator v1.0

---

## 一、项目概况

### 文件统计
| 类型 | 数量 |
|------|------|
| Python文件 | {len(structure['python_files'])} |
| Markdown文档 | {len(structure['markdown_files'])} |
| JSON配置 | {len(structure['json_files'])} |
| 启动脚本 | {len(structure['batch_files'])} |
| 三级Skill | {len(structure['skill_files']['level3'])} |
| 二级Skill | {len(structure['skill_files']['level2'])} |
| 知识库文件 | {len(structure['knowledge_files'])} |

---

## 二、DeepSeek深度评测

"""

        if "error" in evaluation:
            report += f"### ⚠️ 评测异常\n\n```\n{evaluation['error']}\n```\n"
        elif "raw_text" in evaluation:
            report += f"### 评测结果\n\n```\n{evaluation['raw_text']}\n```\n"
        else:
            # 格式化显示JSON结构的评测结果
            if "evaluation_summary" in evaluation:
                report += f"### 📝 总体评价\n\n{evaluation['evaluation_summary']}\n\n"

            if "score" in evaluation:
                report += "### 📊 评分\n\n"
                score = evaluation["score"]
                for key, value in score.items():
                    label = {
                        "functionality": "功能完整性",
                        "architecture": "架构合理性",
                        "documentation": "文档完整性",
                        "code_quality": "代码质量",
                        "extendability": "可扩展性",
                        "user_experience": "用户体验",
                        "overall": "总体评分"
                    }.get(key, key)
                    report += f"- **{label}**: {value}/10\n"
                report += "\n"

            if "strengths" in evaluation:
                report += "### ✅ 优点\n\n"
                for strength in evaluation["strengths"]:
                    report += f"- {strength}\n"
                report += "\n"

            if "weaknesses" in evaluation:
                report += "### ⚠️ 不足\n\n"
                for weakness in evaluation["weaknesses"]:
                    report += f"- {weakness}\n"
                report += "\n"

            if "optimization_suggestions" in evaluation:
                report += "### 🔧 优化建议\n\n"
                for suggestion in evaluation["optimization_suggestions"]:
                    priority = suggestion.get("priority", "medium")
                    priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(priority, "⚪")
                    report += f"{priority_emoji} **优先级**: {priority}\n"
                    report += f"   - 建议: {suggestion.get('suggestion', '')}\n"
                    report += f"   - 预期收益: {suggestion.get('expected_benefit', '')}\n\n"

            if "feature_recommendations" in evaluation:
                report += "### 🎯 功能推荐\n\n"
                for feature in evaluation["feature_recommendations"]:
                    report += f"- {feature}\n"
                report += "\n"

        report += """
---

## 三、项目文件清单（部分）

### Python文件
"""

        for pyfile in structure["python_files"][:20]:
            report += f"- {pyfile}\n"
        if len(structure["python_files"]) > 20:
            report += f"- ... 还有 {len(structure['python_files'])-20} 个\n"

        report += """
### Skill文件
"""

        report += f"\n**三级Skill** ({len(structure['skill_files']['level3'])} 个)\n"
        for skill in structure["skill_files"]["level3"][:10]:
            report += f"- {skill}\n"
        if len(structure["skill_files"]["level3"]) > 10:
            report += f"- ... 还有 {len(structure['skill_files']['level3'])-10} 个\n"

        report += f"\n**二级Skill** ({len(structure['skill_files']['level2'])} 个)\n"
        for skill in structure["skill_files"]["level2"][:10]:
            report += f"- {skill}\n"
        if len(structure["skill_files"]["level2"]) > 10:
            report += f"- ... 还有 {len(structure['skill_files']['level2'])-10} 个\n"

        report += """
---

## 四、使用建议

1. 配置飞书机器人，享受学习完成自动推送
2. 运行DeepSeek学习，持续优化知识库
3. 定期使用诊断工具，检查项目健康状态
4. 根据评测报告，持续优化项目

---

*评测时间: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """*
*评测工具: NWACSEvaluator v1.0*
*NWACS版本: v7.0*
*架构版本: v2.2*
"""

        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)

        self.log(f"📄 评测报告已生成: {report_file}")
        return report_file

    def run_evaluation(self):
        """运行完整评测流程"""
        self.log("="*60)
        self.log("🧪 NWACS DeepSeek全面评测")
        self.log("="*60)

        # 1. 扫描项目结构
        structure = self.scan_project_structure()

        # 2. 读取关键文件
        key_files_content = self.read_key_files(structure)

        # 3. DeepSeek评测
        evaluation = self.evaluate_with_deepseek(structure, key_files_content)

        # 4. 生成报告
        report_file = self.generate_report(structure, key_files_content, evaluation)

        self.log("="*60)
        self.log("✅ 评测完成！")
        self.log("="*60)

        return report_file


def main():
    import argparse

    parser = argparse.ArgumentParser(description="NWACS DeepSeek评测工具")
    parser.add_argument("--api-key", type=str, default=None, help="DeepSeek API密钥")

    args = parser.parse_args()

    try:
        evaluator = NWACSEvaluator(api_key=args.api_key)
        report_file = evaluator.run_evaluation()
        print(f"\n🎉 评测完成！报告已保存到:\n{report_file}")
    except Exception as e:
        print(f"❌ 评测失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
