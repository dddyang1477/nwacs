#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
精确检查Skill文件中的真实乱码问题
"""

import os
import re

def check_files():
    skills_dir = 'skills/level2'
    files_to_check = [
        '11_二级Skill_短篇小说爽文大师.md',
        '04_二级Skill_剧情构造师.md',
        '07_二级Skill_角色塑造师.md'
    ]
    
    for filename in files_to_check:
        filepath = os.path.join(skills_dir, filename)
        if os.path.exists(filepath):
            print(f'=== {filename} ===')
            
            # 读取文件
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 查找真正的异常字符（排除正常的换行、制表符等）
            # 只匹配控制字符（除了换行\n 0x0A、制表符\t 0x09、回车\r 0x0D）
            weird_chars = []
            for i, char in enumerate(content):
                # 检查是否是不可打印的控制字符（排除正常的空白字符）
                if char < '\x20' and char not in '\t\n\r':
                    weird_chars.append((i, repr(char)))
                # 检查是否是扩展ASCII字符（可能是乱码）
                elif '\x7F' <= char <= '\xFF':
                    weird_chars.append((i, repr(char)))
            
            if weird_chars:
                print(f'发现 {len(weird_chars)} 个异常字符:')
                for idx, char_repr in weird_chars[:10]:
                    start = max(0, idx-20)
                    end = min(len(content), idx+20)
                    context = content[start:end]
                    # 清理上下文以便显示
                    context = context.replace('\n', '\\n').replace('\t', '\\t')
                    print(f'  位置 {idx}: {char_repr}')
                    print(f'  上下文: "{context}"')
                    print()
                
                # 修复：移除真正的控制字符
                fixed_content = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F-\xFF]', '', content)
                
                # 保存修复后的内容
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                
                print(f'✓ 已修复并保存')
            else:
                print('✓ 无乱码')
            
            print()

if __name__ == "__main__":
    check_files()