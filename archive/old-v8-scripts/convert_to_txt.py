#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将小说大纲和章节转换为txt格式
"""

import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

def convert_md_to_txt(md_path, txt_path):
    """将markdown文件转换为txt格式"""
    if os.path.exists(md_path):
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 简单清理markdown格式
        content = content.replace('# ', '')
        content = content.replace('## ', '')
        content = content.replace('### ', '')
        content = content.replace('#### ', '')
        content = content.replace('**', '')
        content = content.replace('*', '')
        content = content.replace('---\n', '')
        content = content.replace('|', '')
        content = content.replace('=', '')
        
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✓ 已转换: {txt_path}")
        return True
    else:
        print(f"  ✗ 文件不存在: {md_path}")
        return False

def main():
    print("\n" + "=" * 80)
    print("          将小说转换为TXT格式")
    print("=" * 80)
    
    files_to_convert = [
        ('NOVEL_OUTLINE.md', 'NOVEL_OUTLINE.txt'),
        ('NOVEL_CHAPTERS_1-10.md', 'NOVEL_CHAPTERS_1-10.txt'),
    ]
    
    print("\n正在转换文件...")
    for md_file, txt_file in files_to_convert:
        convert_md_to_txt(md_file, txt_file)
    
    print("\n" + "=" * 80)
    print("                    转换完成！")
    print("=" * 80)
    print("\n📁 转换后的文件：")
    print("  • NOVEL_OUTLINE.txt - 小说大纲")
    print("  • NOVEL_CHAPTERS_1-10.txt - 前10章内容")
    print("\n所有文件已保存为UTF-8编码的TXT格式！")
    print("=" * 80)

if __name__ == "__main__":
    main()
