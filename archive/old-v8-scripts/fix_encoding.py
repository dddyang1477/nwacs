#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 乱码修复工具
修复文件中的乱码问题
"""

import os
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

def fix_encoding(filepath):
    """修复单个文件的编码问题"""
    try:
        # 读取文件内容
        with open(filepath, 'rb') as f:
            raw_content = f.read()
        
        # 尝试多种编码解码
        encodings = ['utf-8', 'gbk', 'gb2312', 'big5']
        content = None
        
        for enc in encodings:
            try:
                content = raw_content.decode(enc)
                break
            except UnicodeDecodeError:
                continue
        
        if content is None:
            print(f"❌ 无法解码: {filepath}")
            return False
        
        # 移除控制字符
        cleaned_content = remove_control_characters(content)
        
        # 修复常见乱码
        cleaned_content = fix_common_mojibake(cleaned_content)
        
        # 保存修复后的文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)
        
        print(f"✅ 修复完成: {filepath}")
        return True
    
    except Exception as e:
        print(f"❌ 修复失败 {filepath}: {e}")
        return False

def remove_control_characters(text):
    """移除控制字符（保留换行、制表符）"""
    # 保留的控制字符
    allowed = {0x09, 0x0A, 0x0D}
    
    result = []
    for char in text:
        code = ord(char)
        if code < 32 and code not in allowed:
            # 替换为空格或删除
            continue
        result.append(char)
    
    return ''.join(result)

def fix_common_mojibake(text):
    """修复常见的乱码问题"""
    # 常见的UTF-8解码错误修复
    fixes = [
        # UTF-8 double encoding
        (r''', "'"),
        (r'"', '"'),
        (r'"', '"'),
        (r''', "'"),
        # GBK/GB2312 错误解码为 UTF-8
        (r'€', '€'),
        (r'-', '-'),
        (r'—', '—'),
        (r'…', '…'),
        # 其他常见乱码
        (r'?', '?'),
    ]
    
    for pattern, replacement in fixes:
        text = text.replace(pattern, replacement)
    
    # 使用正则修复更复杂的乱码模式
    text = re.sub(r'[\x80-\xff]{2,}', lambda m: fix_utf8_sequence(m.group()), text)
    
    return text

def fix_utf8_sequence(seq):
    """尝试修复UTF-8序列"""
    try:
        return seq.encode('latin-1').decode('utf-8', errors='replace')
    except:
        return seq

def fix_all_files_in_directory(directory):
    """修复目录下所有文件"""
    print(f"\n🔍 正在扫描目录: {directory}")
    
    fixed_count = 0
    total_count = 0
    
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith(('.py', '.txt', '.md', '.json')):
                filepath = os.path.join(root, filename)
                total_count += 1
                
                print(f"\n处理: {filepath}")
                if fix_encoding(filepath):
                    fixed_count += 1
    
    print(f"\n{'='*60}")
    print(f"修复完成！")
    print(f"处理文件: {total_count} 个")
    print(f"成功修复: {fixed_count} 个")
    print(f"{'='*60}")

def main():
    print("="*60)
    print("      NWACS 乱码修复工具")
    print("="*60)
    
    # 修复当前目录下所有文件
    fix_all_files_in_directory('.')

if __name__ == "__main__":
    main()
