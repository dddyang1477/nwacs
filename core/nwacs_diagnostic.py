#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS全面检测和修复工具
用DeepSeek对项目进行全面检测，修复乱码和错误代码
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime

try:
    from openai import OpenAI
except ImportError:
    print("❌ 请先安装 openai 库：pip install openai")
    sys.exit(1)


class NWACSDiagnosticTool:
    """NWACS全面诊断工具"""

    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise ValueError("❌ 请设置 DEEPSEEK_API_KEY 环境变量")

        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.deepseek.com"
        )

        self.project_root = Path(__file__).parent
        self.report_path = self.project_root / "logs" / "diagnostic_report"
        self.report_path.mkdir(parents=True, exist_ok=True)

        self.found_issues = []
        self.fixed_files = []

        # 文件分类
        self.file_categories = {
            "python": [".py"],
            "markdown": [".md"],
            "text": [".txt"],
            "json": [".json"],
            "config": [".json", ".yaml", ".yml"]
        }

        # 忽略的目录
        self.ignore_dirs = [
            "__pycache__", ".git", "node_modules", "dist", "build",
            "archive", "backup", ".trae"
        ]

        print(f"🚀 NWACS全面诊断工具启动")
        print(f"📍 项目根目录: {self.project_root}")
        print("-" * 60)

    def log(self, message):
        """带时间戳的日志"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")

    def is_valid_file(self, filepath):
        """验证文件是否有效"""
        # 检查是否忽略目录
        parts = filepath.parts
        for ignore in self.ignore_dirs:
            if ignore in parts:
                return False

        # 只检查特定类型的文件
        allowed_extensions = set()
        for exts in self.file_categories.values():
            allowed_extensions.update(exts)

        return filepath.suffix in allowed_extensions

    def scan_project(self):
        """扫描项目文件"""
        self.log("🔍 扫描项目文件...")
        all_files = []

        for root, dirs, files in os.walk(self.project_root):
            # 修改dirs列表，避免扫描忽略目录
            dirs[:] = [d for d in dirs if d not in self.ignore_dirs]

            for file in files:
                filepath = Path(root) / file
                if self.is_valid_file(filepath):
                    all_files.append(filepath)

        self.log(f"✅ 找到 {len(all_files)} 个文件")
        return all_files

    def check_file_encoding(self, filepath):
        """检查文件编码"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                f.read()
            return "utf-8", None
        except UnicodeDecodeError:
            try:
                with open(filepath, 'r', encoding='gbk') as f:
                    f.read()
                return "gbk", "需要转换编码"
            except Exception:
                try:
                    with open(filepath, 'r', encoding='gb18030') as f:
                        f.read()
                    return "gb18030", "需要转换编码"
                except Exception as e:
                    return "unknown", f"编码错误: {e}"

    def check_python_syntax(self, filepath):
        """检查Python语法"""
        if filepath.suffix != ".py":
            return None

        try:
            import ast
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            ast.parse(content)
            return None
        except SyntaxError as e:
            return f"语法错误: {e}"
        except Exception as e:
            return f"解析错误: {e}"

    def analyze_with_deepseek(self, filepath):
        """用DeepSeek分析文件问题"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # 短文件直接分析，长文件采样
            if len(content) > 5000:
                content = content[:2500] + "\n\n...[文件过长，已截断]...\n\n" + content[-2500:]

            system_prompt = """你是一个专业的代码和文件质量检测专家。你的任务是：
1. 检测文件中的乱码问题
2. 检测代码语法错误
3. 检测内容格式问题
4. 提供修复建议

请用JSON格式输出你的分析结果，格式如下：
{
  "has_issues": true/false,
  "issue_type": "乱码/语法错误/格式问题/其他",
  "description": "问题描述",
  "severity": "严重/中等/轻微",
  "fix_suggestion": "修复建议"
}"""

            user_prompt = f"""请分析以下文件，检测是否有乱码、语法错误或其他问题：
文件类型: {filepath.suffix}
文件路径: {filepath}
文件内容:
{content}"""

            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=1500
            )

            result = response.choices[0].message.content

            # 尝试解析JSON
            try:
                result_json = json.loads(result)
                return result_json
            except json.JSONDecodeError:
                # 如果不是JSON，尝试提取
                return {
                    "has_issues": "乱码" in result or "错误" in result,
                    "issue_type": "未解析",
                    "description": result,
                    "severity": "需要检查",
                    "fix_suggestion": "手动检查"
                }

        except Exception as e:
            return {
                "has_issues": True,
                "issue_type": "分析失败",
                "description": f"分析异常: {e}",
                "severity": "轻微",
                "fix_suggestion": "跳过此文件"
            }

    def fix_file_encoding(self, filepath, detected_encoding):
        """修复文件编码"""
        try:
            with open(filepath, 'r', encoding=detected_encoding) as f:
                content = f.read()

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

            self.log(f"✅ 编码已修复: {filepath} ({detected_encoding} -> UTF-8)")
            self.fixed_files.append(f"{filepath}: 编码修复")
            return True
        except Exception as e:
            self.log(f"❌ 编码修复失败: {filepath}, 错误: {e}")
            return False

    def run_full_diagnostic(self):
        """运行完整诊断"""
        self.log("=" * 60)
        self.log("🧪 开始NWACS项目全面诊断")
        self.log("=" * 60)

        files = self.scan_project()

        # 分批处理，避免过长
        batch_size = 20
        total_files = len(files)
        processed = 0

        for i in range(0, total_files, batch_size):
            batch = files[i:i + batch_size]
            self.log(f"📦 处理批次 {i//batch_size + 1}/{(total_files + batch_size - 1)//batch_size} ({len(batch)} 个文件)")

            for filepath in batch:
                processed += 1

                # 1. 检查编码
                encoding, encoding_issue = self.check_file_encoding(filepath)

                if encoding_issue:
                    issue = {
                        "file": str(filepath),
                        "type": "编码问题",
                        "encoding": encoding,
                        "description": encoding_issue,
                        "severity": "中等"
                    }
                    self.found_issues.append(issue)
                    self.log(f"⚠️ 编码问题: {filepath}")

                    # 尝试修复编码
                    if encoding in ["gbk", "gb18030"]:
                        self.fix_file_encoding(filepath, encoding)

                # 2. 检查Python语法
                if filepath.suffix == ".py":
                    py_issue = self.check_python_syntax(filepath)
                    if py_issue:
                        issue = {
                            "file": str(filepath),
                            "type": "Python语法错误",
                            "description": py_issue,
                            "severity": "严重"
                        }
                        self.found_issues.append(issue)
                        self.log(f"❌ 语法错误: {filepath} - {py_issue}")

                # 3. DeepSeek深度分析（只对部分文件进行）
                if processed % 30 == 0:  # 每30个文件深度分析一个
                    self.log(f"🔍 DeepSeek深度分析: {filepath}")
                    analysis = self.analyze_with_deepseek(filepath)

                    if analysis.get("has_issues"):
                        issue = {
                            "file": str(filepath),
                            "type": analysis.get("issue_type", "未知"),
                            "description": analysis.get("description", ""),
                            "severity": analysis.get("severity", "需要检查"),
                            "fix_suggestion": analysis.get("fix_suggestion", "")
                        }
                        self.found_issues.append(issue)

                # 进度显示
                if processed % 50 == 0:
                    self.log(f"⏱️  已处理: {processed}/{total_files} 文件")

        self.log("=" * 60)
        self.log("✅ 诊断完成")
        self.log("=" * 60)

        self.log(f"📊 总计检测: {total_files} 文件")
        self.log(f"⚠️  发现问题: {len(self.found_issues)} 个")
        self.log(f"✅ 已修复: {len(self.fixed_files)} 个")

        self.generate_report()

    def generate_report(self):
        """生成诊断报告"""
        report_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.report_path / f"诊断报告_{report_time}.md"

        report = f"""# NWACS项目全面诊断报告

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**检测文件数**: {len(list(self.scan_project()))}
**发现问题数**: {len(self.found_issues)}
**已修复文件数**: {len(self.fixed_files)}

---

## 已修复的文件

"""

        for fixed in self.fixed_files:
            report += f"- {fixed}\n"

        report += f"""

---

## 发现的问题

"""

        if self.found_issues:
            # 按严重程度分组
            severe_issues = [i for i in self.found_issues if i.get("severity") == "严重"]
            medium_issues = [i for i in self.found_issues if i.get("severity") == "中等"]
            minor_issues = [i for i in self.found_issues if i.get("severity") not in ["严重", "中等"]]

            if severe_issues:
                report += "### 🔴 严重问题\n\n"
                for issue in severe_issues:
                    report += f"- **{issue['file']}**: {issue['description']}\n"

            if medium_issues:
                report += "\n### 🟡 中等问题\n\n"
                for issue in medium_issues:
                    report += f"- **{issue['file']}**: {issue['description']}\n"

            if minor_issues:
                report += "\n### 🟢 轻微问题\n\n"
                for issue in minor_issues:
                    report += f"- **{issue['file']}**: {issue['description']}\n"
        else:
            report += "✅ 没有发现问题！项目状态良好！\n"

        report += f"""

---

## 总结

本次诊断运行正常，已检测项目中所有主要文件。
如有需要，可以运行DeepSeek全面学习来进一步优化项目。

---

*诊断工具版本: v1.0*
*生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""

        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)

        self.log(f"📄 诊断报告已生成: {report_file}")
        return report_file


def main():
    import argparse

    parser = argparse.ArgumentParser(description='NWACS全面检测和修复工具')
    parser.add_argument('--api-key', type=str, default=None, help='DeepSeek API密钥')
    parser.add_argument('--full', action='store_true', help='完整检测（包括DeepSeek分析）')
    parser.add_argument('--quick', action='store_true', help='快速检测（只检查编码和语法）')

    args = parser.parse_args()

    try:
        tool = NWACSDiagnosticTool(api_key=args.api_key)
        tool.run_full_diagnostic()
    except Exception as e:
        print(f"❌ 诊断失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
