#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小说生成器配置 - 默认TXT格式 + 自动清理
"""

import os
import sys
import glob
import shutil
from datetime import datetime, timedelta

sys.stdout.reconfigure(encoding='utf-8')

# 默认配置
DEFAULT_FORMAT = 'txt'
DEFAULT_ENCODING = 'utf-8'
OUTPUT_DIR = 'output'
GENERATOR_DIR = '.'

# 清理设置
AUTO_CLEAN_GENERATORS = True  # 自动清理生成脚本
KEEP_GENERATORS_DAYS = 7     # 保留天数

def get_file_age_days(filepath):
    """获取文件年龄（天）"""
    try:
        mtime = os.path.getmtime(filepath)
        file_date = datetime.fromtimestamp(mtime)
        age = (datetime.now() - file_date).days
        return age
    except Exception:
        return 0

def clean_old_generators():
    """清理旧的生成脚本"""
    if not AUTO_CLEAN_GENERATORS:
        return 0
    
    # 要清理的文件模式
    patterns = [
        'generate_*.py',
        '*_novel_*.py',
    ]
    
    # 不清理这些
    keep_files = [
        'generate_novel.py',
        'quick_novel.py',
        'nwacs_console.py',
        'novel_writer_config.py',
        'auto_learning.py',
    ]
    
    cleaned_count = 0
    
    for pattern in patterns:
        for filepath in glob.glob(pattern):
            if os.path.basename(filepath) in keep_files:
                continue
            
            age = get_file_age_days(filepath)
            if age >= KEEP_GENERATORS_DAYS:
                try:
                    os.remove(filepath)
                    print(f"  ✓ 已清理: {filepath} ({age}天前)")
                    cleaned_count += 1
                except Exception as e:
                    print(f"  ✗ 清理失败: {filepath} - {e}")
    
    return cleaned_count

def clean_temp_files():
    """清理临时文件"""
    temp_patterns = [
        'test_*.py',
        'temp_*.py',
        'debug_*.py',
        '__pycache__',
        '*.pyc',
    ]
    
    cleaned_count = 0
    
    for pattern in temp_patterns:
        if '*' in pattern:
            for filepath in glob.glob(pattern):
                try:
                    os.remove(filepath)
                    print(f"  ✓ 已清理: {filepath}")
                    cleaned_count += 1
                except Exception:
                    pass
        elif os.path.isdir(pattern):
            try:
                shutil.rmtree(pattern)
                print(f"  ✓ 已清理目录: {pattern}")
                cleaned_count += 1
            except Exception:
                pass
    
    return cleaned_count

def save_novel_to_txt(novel_name, content, chapter_range=""):
    """
    保存小说到TXT格式

    参数：
        novel_name: 小说名称
        content: 小说内容
        chapter_range: 章节范围，如 "1-10章"
    """
    # 清理小说名中的非法字符
    safe_name = ''.join(c for c in novel_name if c not in '\\/:*?"<>|')
    
    # 生成文件名
    if chapter_range:
        filename = f"{safe_name}_{chapter_range}.txt"
    else:
        filename = f"{safe_name}.txt"
    
    # 确保输出目录存在
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    full_path = os.path.join(OUTPUT_DIR, filename)
    
    # 添加头部信息
    header = f"""{novel_name}
{'=' * 60}
修仙玄幻·苟道流·黑暗流·智斗流
生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'=' * 60}

"""
    
    # 写入文件
    with open(full_path, 'w', encoding=DEFAULT_ENCODING) as f:
        f.write(header)
        f.write(content)
        f.write(f"\n\n{'=' * 60}\n")
        f.write("本小说由 NWACS × DeepSeek V4 联合创作\n")
        f.write("NWACS提供框架与大纲\n")
        f.write("DeepSeek弥补内容创作缺陷\n")
    
    print(f"  ✓ 已保存: {full_path}")
    return full_path

def cleanup_all():
    """执行所有清理"""
    print("\n" + "=" * 60)
    print("          开始清理旧文件")
    print("=" * 60)
    
    total_cleaned = 0
    
    print("\n[1/2] 清理旧生成脚本...")
    total_cleaned += clean_old_generators()
    
    print("\n[2/2] 清理临时文件...")
    total_cleaned += clean_temp_files()
    
    print("\n" + "=" * 60)
    print(f"          清理完成！共清理 {total_cleaned} 个文件")
    print("=" * 60)

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='小说生成器配置工具')
    parser.add_argument('--clean', action='store_true', help='清理旧文件')
    parser.add_argument('--save', nargs=2, metavar=('NAME', 'CONTENT'), help='保存小说')
    parser.add_argument('--check', action='store_true', help='检查配置')
    
    args = parser.parse_args()
    
    if args.clean:
        cleanup_all()
    elif args.save:
        novel_name, content = args.save
        save_novel_to_txt(novel_name, content)
    elif args.check:
        print(f"\n默认格式: {DEFAULT_FORMAT}")
        print(f"默认编码: {DEFAULT_ENCODING}")
        print(f"输出目录: {OUTPUT_DIR}")
        print(f"自动清理: {AUTO_CLEAN_GENERATORS}")
        print(f"保留天数: {KEEP_GENERATORS_DAYS}天")
    else:
        # 默认执行清理
        cleanup_all()

if __name__ == "__main__":
    main()
