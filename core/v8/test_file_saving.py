#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试小说生成系统的文件保存功能
"""

import sys
import os
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

def create_novel_directory(novel_name):
    """创建小说文件夹"""
    novel_dir = f"novels/{novel_name}"
    os.makedirs(novel_dir, exist_ok=True)
    print(f"   ✅ 小说文件夹已创建: {novel_dir}")
    return novel_dir

def save_chapter(novel_dir, chapter_num, chapter_name, content):
    """保存章节内容"""
    # 保存为 .md 格式
    md_file = f"{novel_dir}/chapter_{chapter_num:02d}.md"
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(f"# {chapter_name}\n\n")
        f.write(content)
        f.write("\n")
    print(f"   ✅ 章节已保存 (MD): {md_file}")

    # 保存为 .txt 格式
    txt_file = f"{novel_dir}/chapter_{chapter_num:02d}.txt"
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write(f"{chapter_name}\n")
        f.write("="*len(chapter_name) + "\n\n")
        f.write(content)
        f.write("\n")
    print(f"   ✅ 章节已保存 (TXT): {txt_file}")

    return md_file, txt_file

def generate_table_of_contents(novel_dir, novel_name, chapters):
    """生成目录"""
    toc_md = f"{novel_dir}/table_of_contents.md"
    toc_txt = f"{novel_dir}/table_of_contents.txt"

    toc_content_md = [
        f"# 📖 {novel_name} - 目录\n\n",
        f"*由NWACS V8.0生成 | 更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n",
        "---\n\n",
        "## 目录\n\n"
    ]

    toc_content_txt = [
        f"{novel_name} - 目录\n",
        "="*60 + "\n\n",
        f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n",
        "目录\n\n"
    ]

    for chapter_num, chapter_name in chapters:
        toc_content_md.append(f"- [{chapter_name}](chapter_{chapter_num:02d}.md)\n")
        toc_content_txt.append(f"{chapter_name} (chapter_{chapter_num:02d}.txt)\n")

    with open(toc_md, 'w', encoding='utf-8') as f:
        f.writelines(toc_content_md)
    print(f"   ✅ 目录已生成 (MD): {toc_md}")

    with open(toc_txt, 'w', encoding='utf-8') as f:
        f.writelines(toc_content_txt)
    print(f"   ✅ 目录已生成 (TXT): {toc_txt}")

    return toc_md, toc_txt

def merge_full_novel(novel_dir, novel_name, chapters, full_content):
    """合并完整小说"""
    full_md = f"{novel_dir}/{novel_name}_full.md"
    full_txt = f"{novel_dir}/{novel_name}_full.txt"

    md_content = [
        f"# 📖 {novel_name}\n\n",
        f"*由NWACS V8.0生成 | 更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n",
        "---\n\n"
    ]
    md_content.extend(full_content)

    txt_content = [
        f"{novel_name}\n",
        "="*60 + "\n\n",
        f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n",
        "---\n\n"
    ]
    txt_content.extend(full_content)

    with open(full_md, 'w', encoding='utf-8') as f:
        f.writelines(md_content)
    print(f"   ✅ 完整小说已保存 (MD): {full_md}")

    with open(full_txt, 'w', encoding='utf-8') as f:
        f.writelines(txt_content)
    print(f"   ✅ 完整小说已保存 (TXT): {full_txt}")

    return full_md, full_txt

def main():
    print("="*60)
    print("📝 测试小说文件保存系统")
    print("="*60)

    novel_name = "测试小说"
    print(f"\n小说名称: {novel_name}")

    # 创建小说文件夹
    novel_dir = create_novel_directory(novel_name)

    # 模拟章节内容
    test_chapters = [
        (1, "第一章：测试章节", "这是测试章节1的内容...\n\n这是第二段内容..."),
        (2, "第二章：测试章节", "这是测试章节2的内容...\n\n这是第二段内容..."),
        (3, "第三章：测试章节", "这是测试章节3的内容...\n\n这是第二段内容..."),
    ]

    chapters_list = []
    full_content = []

    # 保存测试章节
    for chapter_num, chapter_name, content in test_chapters:
        print(f"\n保存章节 {chapter_num}: {chapter_name}")
        save_chapter(novel_dir, chapter_num, chapter_name, content)
        chapters_list.append((chapter_num, chapter_name))

        full_content.append(f"# {chapter_name}\n\n")
        full_content.append(content)
        full_content.append("\n---\n\n")

    # 生成目录
    generate_table_of_contents(novel_dir, novel_name, chapters_list)

    # 合并完整小说
    merge_full_novel(novel_dir, novel_name, chapters_list, full_content)

    print("\n" + "="*60)
    print("🎉 测试完成！")
    print("="*60)
    print(f"\n生成的文件:")
    print(f"  - 小说文件夹: {novel_dir}")
    print(f"  - 目录 (MD): {novel_dir}/table_of_contents.md")
    print(f"  - 目录 (TXT): {novel_dir}/table_of_contents.txt")
    print(f"  - 完整小说 (MD): {novel_dir}/{novel_name}_full.md")
    print(f"  - 完整小说 (TXT): {novel_dir}/{novel_name}_full.txt")

    for i in range(1, 4):
        print(f"  - 第{i}章 (MD): {novel_dir}/chapter_{i:02d}.md")
        print(f"  - 第{i}章 (TXT): {novel_dir}/chapter_{i:02d}.txt")

    print(f"\n✅ 文件保存功能测试成功！")

if __name__ == "__main__":
    main()
