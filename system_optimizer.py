#!/usr/bin/env python3
"""
NWACS项目系统化优化脚本
功能：清理无用数据、整合文件、优化结构、减少臃肿
"""

import os
import shutil
import json
import time
from pathlib import Path

# 项目根目录
PROJECT_ROOT = r"C:\Users\111\WorkBuddy\2026-05-13-task-3\NWACS"
BACKUP_DIR = os.path.join(PROJECT_ROOT, "optimized_backup")

def log(msg):
    """日志记录"""
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] {msg}")

def create_backup_dir():
    """创建备份目录"""
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
        log(f"创建备份目录: {BACKUP_DIR}")

def clean_pycache():
    """清理所有__pycache__目录"""
    log("开始清理Python缓存...")
    count = 0
    for root, dirs, files in os.walk(PROJECT_ROOT):
        for dir_name in dirs:
            if dir_name == "__pycache__":
                cache_path = os.path.join(root, dir_name)
                try:
                    shutil.rmtree(cache_path)
                    count += 1
                except Exception as e:
                    log(f"清理失败 {cache_path}: {e}")
    
    log(f"清理了 {count} 个__pycache__目录")

def clean_temp_files():
    """清理临时文件和日志"""
    log("开始清理临时文件...")
    temp_extensions = ['.tmp', '.log', '.bak', '.backup', '.old', '.orig']
    count = 0
    
    for root, dirs, files in os.walk(PROJECT_ROOT):
        for file_name in files:
            if any(file_name.endswith(ext) for ext in temp_extensions):
                file_path = os.path.join(root, file_name)
                try:
                    os.remove(file_path)
                    count += 1
                except Exception as e:
                    log(f"删除失败 {file_path}: {e}")
    
    log(f"清理了 {count} 个临时文件")

def analyze_project_structure():
    """分析项目结构"""
    log("分析项目结构...")
    
    # 计算各目录大小
    dir_sizes = {}
    for item in os.listdir(PROJECT_ROOT):
        item_path = os.path.join(PROJECT_ROOT, item)
        if os.path.isdir(item_path):
            total_size = 0
            for root, dirs, files in os.walk(item_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        total_size += os.path.getsize(file_path)
                    except:
                        pass
            dir_sizes[item] = total_size / (1024 * 1024)  # MB
    
    # 按大小排序
    sorted_dirs = sorted(dir_sizes.items(), key=lambda x: x[1], reverse=True)
    
    log("项目目录大小分析:")
    for dir_name, size in sorted_dirs:
        log(f"  {dir_name}: {size:.2f} MB")

def optimize_core_files():
    """优化核心文件"""
    log("优化核心文件...")
    
    # 检查核心文件语法
    core_dir = os.path.join(PROJECT_ROOT, "core", "v8")
    if os.path.exists(core_dir):
        server_file = os.path.join(core_dir, "nwacs_server_v3.py")
        if os.path.exists(server_file):
            log(f"检查 {server_file} 语法...")
            try:
                import py_compile
                py_compile.compile(server_file, doraise=True)
                log("✓ 后端服务器语法检查通过")
            except py_compile.PyCompileError as e:
                log(f"✗ 语法错误: {e}")
        
        frontend_file = os.path.join(core_dir, "frontend", "index.html")
        if os.path.exists(frontend_file):
            log(f"检查 {frontend_file} ...")
            with open(frontend_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if content.count('<script>') == content.count('</script>'):
                    log("✓ 前端HTML标签匹配")
                else:
                    log("✗ 前端HTML标签不匹配")

def create_optimization_report():
    """创建优化报告"""
    log("创建优化报告...")
    
    report = {
        "optimization_time": time.strftime('%Y-%m-%d %H:%M:%S'),
        "actions_taken": [
            "清理Python缓存目录",
            "清理临时文件和日志",
            "分析项目结构",
            "检查核心文件语法"
        ],
        "recommendations": [
            "定期清理__pycache__目录",
            "将archive文件夹移出项目或压缩",
            "删除不必要的.log和.tmp文件",
            "考虑将大文件移出项目"
        ]
    }
    
    report_file = os.path.join(PROJECT_ROOT, "optimization_report.json")
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    log(f"优化报告已保存: {report_file}")

def main():
    """主函数"""
    log("=" * 60)
    log("NWACS项目系统化优化开始")
    log("=" * 60)
    
    # 1. 创建备份目录
    create_backup_dir()
    
    # 2. 清理Python缓存
    clean_pycache()
    
    # 3. 清理临时文件
    clean_temp_files()
    
    # 4. 分析项目结构
    analyze_project_structure()
    
    # 5. 优化核心文件
    optimize_core_files()
    
    # 6. 创建优化报告
    create_optimization_report()
    
    log("=" * 60)
    log("NWACS项目系统化优化完成")
    log("=" * 60)

if __name__ == "__main__":
    main()