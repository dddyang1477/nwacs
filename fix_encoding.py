#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查并修复Skill文件中的乱码问题
"""

import os
import re

def check_and_fix_files():
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
            
            # 查找异常字符
            weird_chars = []
            for i, char in enumerate(content):
                if char < '\x20' or (char >= '\x7F' and char <= '\xFF'):
                    weird_chars.append((i, repr(char)))
            
            if weird_chars:
                print(f'发现 {len(weird_chars)} 个异常字符:')
                for idx, char_repr in weird_chars[:5]:  # 只显示前5个
                    context = content[max(0, idx-20):idx+20]
                    print(f'  位置 {idx}: {char_repr}')
                    print(f'  上下文: "{context}"')
                    print()
                
                # 修复：移除控制字符
                fixed_content = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F]', '', content)
                
                # 保存修复后的内容
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                
                print(f'✓ 已修复并保存')
            else:
                print('✓ 无乱码')
            
            print()

if __name__ == "__main__":
    check_and_fix_files()