#!/usr/bin/env python3
"""
NWACS系统全方位体检和诊断工具
功能：全面检查、诊断问题、优化升级系统
"""

import os
import sys
import json
import time
import ast
import re
from pathlib import Path
from collections import defaultdict

# 项目根目录
PROJECT_ROOT = r"C:\Users\111\WorkBuddy\2026-05-13-task-3\NWACS"
CORE_DIR = os.path.join(PROJECT_ROOT, "core", "v8")

class SystemDiagnostic:
    def __init__(self):
        self.issues = []
        self.warnings = []
        self.stats = {
            "total_files": 0,
            "python_files": 0,
            "html_files": 0,
            "js_files": 0,
            "json_files": 0,
            "total_lines": 0,
            "syntax_errors": 0,
            "warnings": 0
        }
        self.start_time = time.time()
    
    def log(self, msg, level="INFO"):
        """日志记录"""
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        prefix = {
            "INFO": "ℹ️",
            "WARNING": "⚠️",
            "ERROR": "❌",
            "SUCCESS": "✅",
            "OPTIMIZE": "🔧"
        }.get(level, "ℹ️")
        
        line = f"[{timestamp}] {prefix} {msg}"
        print(line)
        
        # 保存到日志文件
        log_file = os.path.join(PROJECT_ROOT, "system_diagnostic.log")
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(line + '\n')
    
    def check_python_syntax(self, file_path):
        """检查Python文件语法"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            ast.parse(code)
            return True, None
        except SyntaxError as e:
            return False, f"行{e.lineno}: {e.msg}"
        except Exception as e:
            return False, str(e)
    
    def check_html_structure(self, file_path):
        """检查HTML文件结构"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查基本结构
            issues = []
            
            # 检查DOCTYPE
            if not content.strip().startswith('<!DOCTYPE html'):
                issues.append("缺少DOCTYPE声明")
            
            # 检查标签匹配
            open_tags = re.findall(r'<(\w+)[^>]*>', content)
            close_tags = re.findall(r'</(\w+)>', content)
            
            # 简单检查（实际应该用HTML解析器）
            for tag in ['html', 'head', 'body']:
                if content.count(f'<{tag}') != content.count(f'</{tag}>'):
                    issues.append(f"<{tag}>标签不匹配")
            
            # 检查script标签
            script_count = content.count('<script')
            script_close_count = content.count('</script>')
            if script_count != script_close_count:
                issues.append(f"script标签不匹配: {script_count} open vs {script_close_count} close")
            
            return len(issues) == 0, issues
        except Exception as e:
            return False, [str(e)]
    
    def scan_project_files(self):
        """扫描项目文件"""
        self.log("开始扫描项目文件...", "INFO")
        
        for root, dirs, files in os.walk(PROJECT_ROOT):
            # 跳过某些目录
            dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', 'node_modules']]
            
            for file in files:
                file_path = os.path.join(root, file)
                self.stats["total_files"] += 1
                
                # 统计文件类型
                if file.endswith('.py'):
                    self.stats["python_files"] += 1
                    self.check_file_syntax(file_path, 'python')
                elif file.endswith('.html'):
                    self.stats["html_files"] += 1
                    self.check_file_syntax(file_path, 'html')
                elif file.endswith('.js'):
                    self.stats["js_files"] += 1
                elif file.endswith('.json'):
                    self.stats["json_files"] += 1
                    self.check_json_syntax(file_path)
    
    def check_file_syntax(self, file_path, file_type):
        """检查文件语法"""
        if file_type == 'python':
            success, error = self.check_python_syntax(file_path)
            if not success:
                self.stats["syntax_errors"] += 1
                self.issues.append({
                    "file": file_path,
                    "type": "syntax_error",
                    "message": error
                })
                self.log(f"语法错误: {file_path} - {error}", "ERROR")
        
        elif file_type == 'html':
            success, errors = self.check_html_structure(file_path)
            if not success:
                for error in errors:
                    self.issues.append({
                        "file": file_path,
                        "type": "html_structure",
                        "message": error
                    })
                self.log(f"HTML结构问题: {file_path} - {', '.join(errors)}", "WARNING")
    
    def check_json_syntax(self, file_path):
        """检查JSON文件语法"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                json.load(f)
        except json.JSONDecodeError as e:
            self.issues.append({
                "file": file_path,
                "type": "json_error",
                "message": str(e)
            })
            self.log(f"JSON语法错误: {file_path} - {e}", "ERROR")
    
    def analyze_code_quality(self):
        """分析代码质量"""
        self.log("分析代码质量...", "INFO")
        
        # 检查核心文件
        core_files = [
            os.path.join(CORE_DIR, "nwacs_server_v3.py"),
            os.path.join(CORE_DIR, "frontend", "index.html")
        ]
        
        for file_path in core_files:
            if os.path.exists(file_path):
                self.analyze_single_file(file_path)
    
    def analyze_single_file(self, file_path):
        """分析单个文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                self.stats["total_lines"] += len(lines)
            
            # 检查代码质量问题
            issues = []
            
            # 检查过长的函数
            if file_path.endswith('.py'):
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        func_lines = node.end_lineno - node.lineno
                        if func_lines > 50:
                            issues.append(f"函数 {node.name} 过长: {func_lines} 行")
            
            # 检查TODO和FIXME
            todo_count = content.count('TODO')
            fixme_count = content.count('FIXME')
            if todo_count > 0:
                issues.append(f"发现 {todo_count} 个TODO")
            if fixme_count > 0:
                issues.append(f"发现 {fixme_count} 个FIXME")
            
            if issues:
                for issue in issues:
                    self.warnings.append({
                        "file": file_path,
                        "message": issue
                    })
                self.stats["warnings"] += len(issues)
        
        except Exception as e:
            self.log(f"分析失败 {file_path}: {e}", "ERROR")
    
    def check_variable_associations(self):
        """检查变量关联"""
        self.log("检查变量关联...", "INFO")
        
        # 检查核心Python文件中的变量使用
        server_file = os.path.join(CORE_DIR, "nwacs_server_v3.py")
        if os.path.exists(server_file):
            try:
                with open(server_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 检查未使用的导入
                tree = ast.parse(content)
                imports = set()
                used_names = set()
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            imports.add(alias.asname or alias.name)
                    elif isinstance(node, ast.ImportFrom):
                        for alias in node.names:
                            imports.add(alias.asname or alias.name)
                    elif isinstance(node, ast.Name):
                        used_names.add(node.id)
                
                unused = imports - used_names
                if unused:
                    self.warnings.append({
                        "file": server_file,
                        "message": f"可能未使用的导入: {', '.join(list(unused)[:5])}"
                    })
                
                self.log(f"发现 {len(unused)} 个可能未使用的导入", "WARNING")
                
            except Exception as e:
                self.log(f"变量关联检查失败: {e}", "ERROR")
    
    def generate_optimization_plan(self):
        """生成优化方案"""
        self.log("生成优化方案...", "INFO")
        
        plan = {
            "immediate_actions": [],
            "short_term_improvements": [],
            "long_term_restructuring": []
        }
        
        # 立即行动
        if self.stats["syntax_errors"] > 0:
            plan["immediate_actions"].append("修复所有语法错误")
        
        if len(self.issues) > 10:
            plan["immediate_actions"].append("清理代码问题")
        
        # 短期改进
        plan["short_term_improvements"].append("添加单元测试")
        plan["short_term_improvements"].append("完善错误处理")
        plan["short_term_improvements"].append("优化API响应格式")
        
        # 长期重构
        plan["long_term_restructuring"].append("模块化重构后端代码")
        plan["long_term_restructuring"].append("前后端分离架构")
        plan["long_term_restructuring"].append("引入类型提示")
        
        return plan
    
    def run_diagnostic(self):
        """运行诊断"""
        self.log("=" * 60, "INFO")
        self.log("NWACS系统全方位体检和诊断开始", "INFO")
        self.log("=" * 60, "INFO")
        
        # 1. 扫描项目文件
        self.scan_project_files()
        
        # 2. 分析代码质量
        self.analyze_code_quality()
        
        # 3. 检查变量关联
        self.check_variable_associations()
        
        # 4. 生成优化方案
        plan = self.generate_optimization_plan()
        
        # 5. 生成报告
        self.generate_report(plan)
        
        self.log("=" * 60, "INFO")
        self.log("NWACS系统全方位体检和诊断完成", "INFO")
        self.log("=" * 60, "INFO")
    
    def generate_report(self, plan):
        """生成诊断报告"""
        self.log("生成诊断报告...", "INFO")
        
        elapsed_time = time.time() - self.start_time
        
        report = {
            "diagnostic_time": time.strftime('%Y-%m-%d %H:%M:%S'),
            "elapsed_seconds": round(elapsed_time, 2),
            "statistics": self.stats,
            "issues_found": len(self.issues),
            "warnings_found": len(self.warnings),
            "issues": self.issues[:10],  # 只显示前10个
            "warnings": self.warnings[:10],
            "optimization_plan": plan
        }
        
        # 保存JSON报告
        report_file = os.path.join(PROJECT_ROOT, "system_diagnostic_report.json")
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        # 生成可读报告
        readable_report = f"""
# NWACS系统体检诊断报告
生成时间: {report['diagnostic_time']}
耗时: {report['elapsed_seconds']} 秒

## 📊 统计信息
- 总文件数: {self.stats['total_files']}
- Python文件: {self.stats['python_files']}
- HTML文件: {self.stats['html_files']}
- JavaScript文件: {self.stats['js_files']}
- JSON文件: {self.stats['json_files']}
- 总代码行数: {self.stats['total_lines']}
- 语法错误: {self.stats['syntax_errors']}
- 警告数: {self.stats['warnings']}

## ❌ 发现的问题 ({len(self.issues)} 个)
"""
        
        for i, issue in enumerate(self.issues[:10], 1):
            readable_report += f"{i}. [{issue['type']}] {issue['file']}: {issue['message']}\n"
        
        readable_report += f"\n## ⚠️ 警告 ({len(self.warnings)} 个)\n"
        for i, warning in enumerate(self.warnings[:10], 1):
            readable_report += f"{i}. {warning['file']}: {warning['message']}\n"
        
        readable_report += "\n## 🔧 优化方案\n"
        readable_report += "### 立即行动\n"
        for action in plan["immediate_actions"]:
            readable_report += f"- {action}\n"
        
        readable_report += "\n### 短期改进\n"
        for improvement in plan["short_term_improvements"]:
            readable_report += f"- {improvement}\n"
        
        readable_report += "\n### 长期重构\n"
        for restructuring in plan["long_term_restructuring"]:
            readable_report += f"- {restructuring}\n"
        
        # 保存可读报告
        readable_file = os.path.join(PROJECT_ROOT, "system_diagnostic_report.md")
        with open(readable_file, 'w', encoding='utf-8') as f:
            f.write(readable_report)
        
        self.log(f"诊断报告已保存: {report_file}", "SUCCESS")
        self.log(f"可读报告已保存: {readable_file}", "SUCCESS")

def main():
    diagnostic = SystemDiagnostic()
    diagnostic.run_diagnostic()

if __name__ == "__main__":
    main()
