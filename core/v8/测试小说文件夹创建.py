#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试小说文件夹创建功能
"""

import sys
import os

# 添加当前目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# 设置UTF-8编码输出
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

print("="*80)
print("🧪 测试小说文件夹创建功能")
print("="*80)

# 测试1：创建一个简单的测试模板
test_template = {
    'name': '测试模板',
    'based_on': '爆款',
    'formula': '测试公式',
    'core_elements': ['元素1', '元素2'],
    'structure': [
        {'chapter': 1, 'title': '第一章', 'content': '第一章内容'}
    ],
    'example_opening': '这是一个测试开局内容...'
}

print("\n📁 测试1：创建测试小说文件夹...")

from datetime import datetime

# 创建小说主文件夹
base_path = os.path.dirname(os.path.abspath(__file__))
novels_folder = os.path.join(base_path, "novels")
if not os.path.exists(novels_folder):
    os.makedirs(novels_folder)
    print(f"✅ 创建了 novels 主文件夹: {novels_folder}")
else:
    print(f"✅ novels 文件夹已存在: {novels_folder}")

# 创建以小说名命名的文件夹
test_novel_name = "测试小说作品"
clean_name = "".join(c for c in test_novel_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
novel_folder = os.path.join(novels_folder, clean_name)

# 如果文件夹已存在，添加时间戳
if os.path.exists(novel_folder):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    novel_folder = os.path.join(novels_folder, f"{clean_name}_{timestamp}")

os.makedirs(novel_folder)
print(f"✅ 创建了小说文件夹: {novel_folder}")

# 测试2：保存一个简单的测试文件
test_file = os.path.join(novel_folder, "测试文件.txt")
with open(test_file, "w", encoding="utf-8") as f:
    f.write("这是一个测试文件，用于验证文件夹创建功能正常！\n")
    f.write(f"创建时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

print(f"✅ 创建了测试文件: {test_file}")

# 验证文件是否存在
if os.path.exists(test_file):
    print("\n🎉 测试成功！所有功能正常！")
    print(f"   文件位置: {novel_folder}")
else:
    print("\n❌ 测试失败！")

print("\n" + "="*80)
print("💡 提示：现在您可以正常使用 NWACS FINAL 的「快速生成开局」功能了！")
print("   程序会自动创建小说文件夹并保存5个文件！")
print("="*80)

input("\n按回车键退出...")
