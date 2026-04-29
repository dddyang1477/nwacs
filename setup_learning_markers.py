#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量为所有Skill文件添加学习成果插入标记
"""

import os
import re

SKILLS_DIR = r"e:\Program Files (x86)\Trae CN\github\NWACS\skills\level2"

MARKER = "\n\n<!-- 学习成果自动插入位置 -->\n"

def find_best_insert_position(content):
    """找到最佳插入位置（在文件末尾的标记行之前）"""
    lines = content.split('\n')

    # 查找最后一个 ## 标题（通常是协作接口或总结部分）
    last_h2_idx = -1
    for i in range(len(lines) - 1, -1, -1):
        line = lines[i].strip()
        if line.startswith('## ') and any(keyword in line for keyword in ['协作', '接口', '总结', '概述', '核心']):
            last_h2_idx = i
            break

    # 如果找到，在该部分之前插入
    if last_h2_idx > 0:
        return last_h2_idx

    # 否则在文件末尾（倒数5行内）查找合适位置
    for i in range(len(lines) - 1, len(lines) - 10, -1):
        if i < 0:
            break
        line = lines[i].strip()
        # 如果是分隔线或空行较多的地方
        if line == '---' or line.startswith('**') or line == '':
            continue
        else:
            return i + 1

    return len(lines) - 3

def add_marker_to_file(filepath):
    """为单个文件添加标记"""
    if not os.path.exists(filepath):
        print(f"[跳过] 文件不存在: {filepath}")
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 检查是否已有标记
    if '学习成果自动插入' in content:
        print(f"[已有] {os.path.basename(filepath)}")
        return False

    # 查找插入位置
    insert_pos = find_best_insert_position(content)

    # 插入标记
    lines = content.split('\n')
    lines.insert(insert_pos, MARKER.strip())
    new_content = '\n'.join(lines)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"[添加] {os.path.basename(filepath)}")
    return True

def main():
    print("=" * 60)
    print("批量为Skill文件添加学习成果插入标记")
    print("=" * 60)
    print()

    if not os.path.exists(SKILLS_DIR):
        print(f"[错误] 目录不存在: {SKILLS_DIR}")
        return

    # 获取所有markdown文件
    md_files = [f for f in os.listdir(SKILLS_DIR) if f.endswith('.md')]

    print(f"找到 {len(md_files)} 个Skill文件")
    print()

    added_count = 0
    for filename in sorted(md_files):
        filepath = os.path.join(SKILLS_DIR, filename)
        if add_marker_to_file(filepath):
            added_count += 1

    print()
    print("=" * 60)
    print(f"完成！已为 {added_count} 个文件添加标记")
    print("=" * 60)

if __name__ == "__main__":
    main()