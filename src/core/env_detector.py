#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 环境检测与修复工具 v1.0
检测并自动修复Python环境配置问题
"""

import os
import sys
import subprocess
import platform
from datetime import datetime

class EnvironmentDetector:
    """环境检测与修复器"""
    
    def __init__(self):
        self.issues = []
        self.fixes = []
        self.python_paths = []
    
    def detect_python_environment(self):
        """检测Python环境"""
        print("="*60)
        print("Python环境检测")
        print("="*60)
        
        # 检测Python版本
        self._detect_python_version()
        
        # 检测Python路径
        self._detect_python_paths()
        
        # 检测pip
        self._detect_pip()
        
        # 检测必要依赖
        self._detect_dependencies()
        
        # 检测环境变量
        self._detect_env_variables()
        
        # 检测脚本目录权限
        self._detect_permissions()
    
    def _detect_python_version(self):
        """检测Python版本"""
        version = sys.version_info
        print(f"Python版本: {version.major}.{version.minor}.{version.micro}")
        
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            self.issues.append(f"Python版本过低: {version.major}.{version.minor}.{version.micro}，建议使用Python 3.8+")
        else:
            print("✓ Python版本符合要求")
    
    def _detect_python_paths(self):
        """检测Python路径"""
        print(f"\nPython可执行文件路径: {sys.executable}")
        print(f"Python安装目录: {os.path.dirname(sys.executable)}")
        
        # 查找其他Python安装
        try:
            if platform.system() == "Windows":
                # 在Windows上查找Python
                paths_to_check = [
                    r"C:\Python39\python.exe",
                    r"C:\Python38\python.exe",
                    r"C:\Program Files\Python39\python.exe",
                    r"C:\Program Files\Python38\python.exe",
                    r"C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python39\python.exe",
                    r"C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python38\python.exe",
                ]
                for path in paths_to_check:
                    expanded_path = os.path.expandvars(path)
                    if os.path.exists(expanded_path):
                        self.python_paths.append(expanded_path)
                        print(f"发现Python安装: {expanded_path}")
            else:
                # 在Linux/macOS上查找Python
                result = subprocess.run(['which', '-a', 'python3'], capture_output=True, text=True)
                if result.returncode == 0:
                    paths = result.stdout.strip().split('\n')
                    for path in paths:
                        if path:
                            self.python_paths.append(path)
                            print(f"发现Python安装: {path}")
        except Exception as e:
            print(f"检测Python路径时出错: {e}")
    
    def _detect_pip(self):
        """检测pip"""
        print("\npip检测:")
        try:
            result = subprocess.run([sys.executable, '-m', 'pip', '--version'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✓ pip版本: {result.stdout.strip()}")
            else:
                self.issues.append("pip未安装或配置不正确")
                print("✗ pip检测失败")
        except Exception as e:
            self.issues.append(f"检测pip时出错: {e}")
            print(f"✗ 检测pip时出错: {e}")
    
    def _detect_dependencies(self):
        """检测必要依赖"""
        print("\n必要依赖检测:")
        required_packages = ['json', 'os', 'sys', 'time', 'threading', 'datetime', 
                            'logging', 'subprocess', 'platform']
        
        missing_packages = []
        for package in required_packages:
            try:
                __import__(package)
                print(f"✓ {package}")
            except ImportError:
                missing_packages.append(package)
                print(f"✗ {package}")
        
        if missing_packages:
            self.issues.append(f"缺少必要依赖: {', '.join(missing_packages)}")
    
    def _detect_env_variables(self):
        """检测环境变量"""
        print("\n环境变量检测:")
        path_var = os.environ.get('PATH', '')
        
        # 检查Python是否在PATH中
        python_dir = os.path.dirname(sys.executable)
        if python_dir in path_var:
            print("✓ Python目录在PATH环境变量中")
        else:
            self.issues.append(f"Python目录不在PATH中: {python_dir}")
            self.fixes.append(f"将Python目录添加到PATH: {python_dir}")
            print(f"✗ Python目录不在PATH中: {python_dir}")
    
    def _detect_permissions(self):
        """检测脚本目录权限"""
        print("\n目录权限检测:")
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 检查读写权限
        if os.access(script_dir, os.R_OK):
            print("✓ 脚本目录可读")
        else:
            self.issues.append(f"脚本目录不可读: {script_dir}")
            print(f"✗ 脚本目录不可读: {script_dir}")
        
        if os.access(script_dir, os.W_OK):
            print("✓ 脚本目录可写")
        else:
            self.issues.append(f"脚本目录不可写: {script_dir}")
            print(f"✗ 脚本目录不可写: {script_dir}")
        
        # 检查logs目录
        logs_dir = os.path.join(script_dir, 'logs')
        if not os.path.exists(logs_dir):
            try:
                os.makedirs(logs_dir)
                print(f"✓ 自动创建logs目录: {logs_dir}")
            except Exception as e:
                self.issues.append(f"无法创建logs目录: {e}")
                print(f"✗ 无法创建logs目录: {e}")
        else:
            print(f"✓ logs目录已存在")
    
    def generate_report(self):
        """生成检测报告"""
        print("\n" + "="*60)
        print("环境检测报告")
        print("="*60)
        
        if self.issues:
            print("\n发现的问题:")
            for i, issue in enumerate(self.issues, 1):
                print(f"  {i}. {issue}")
        else:
            print("\n✓ 未发现问题")
        
        if self.fixes:
            print("\n建议的修复方案:")
            for i, fix in enumerate(self.fixes, 1):
                print(f"  {i}. {fix}")
        
        # 保存报告
        report_content = self._generate_report_content()
        report_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                  '环境检测报告.txt')
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        print(f"\n报告已保存到: {report_path}")
        
        return self.issues, self.fixes
    
    def _generate_report_content(self):
        """生成报告内容"""
        content = []
        content.append("="*60)
        content.append("NWACS 环境检测报告")
        content.append("="*60)
        content.append(f"检测时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        content.append(f"操作系统: {platform.system()} {platform.release()}")
        content.append(f"Python版本: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
        content.append(f"Python路径: {sys.executable}")
        content.append("")
        content.append("="*60)
        content.append("发现的问题:")
        content.append("="*60)
        
        if self.issues:
            for i, issue in enumerate(self.issues, 1):
                content.append(f"{i}. {issue}")
        else:
            content.append("无")
        
        content.append("")
        content.append("="*60)
        content.append("建议的修复方案:")
        content.append("="*60)
        
        if self.fixes:
            for i, fix in enumerate(self.fixes, 1):
                content.append(f"{i}. {fix}")
        else:
            content.append("无")
        
        content.append("")
        content.append("="*60)
        content.append("检测完成")
        content.append("="*60)
        
        return '\n'.join(content)
    
    def auto_fix(self):
        """自动修复问题"""
        print("\n" + "="*60)
        print("自动修复")
        print("="*60)
        
        # 尝试修复PATH问题
        if self.fixes:
            for fix in self.fixes:
                if "添加到PATH" in fix:
                    print(f"尝试修复: {fix}")
                    # 在Windows上尝试添加到PATH
                    if platform.system() == "Windows":
                        try:
                            # 获取Python目录
                            python_dir = os.path.dirname(sys.executable)
                            # 添加到当前会话的PATH
                            os.environ['PATH'] = python_dir + os.pathsep + os.environ['PATH']
                            print(f"✓ 已将Python目录添加到当前会话的PATH")
                        except Exception as e:
                            print(f"✗ 修复失败: {e}")
        
        # 创建logs目录
        script_dir = os.path.dirname(os.path.abspath(__file__))
        logs_dir = os.path.join(script_dir, 'logs')
        if not os.path.exists(logs_dir):
            try:
                os.makedirs(logs_dir)
                print(f"✓ 创建logs目录成功")
            except Exception as e:
                print(f"✗ 创建logs目录失败: {e}")

def main():
    """主函数"""
    detector = EnvironmentDetector()
    detector.detect_python_environment()
    detector.auto_fix()
    detector.generate_report()

if __name__ == "__main__":
    main()