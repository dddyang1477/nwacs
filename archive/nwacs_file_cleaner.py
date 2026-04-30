#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 文件整理与优化工具
分批次清理重复、临时文件，优化目录结构
"""

import os
import sys
import shutil
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')
VERSION = "1.0"

# 定义需要保留的核心文件
CORE_FILES = [
    # 主启动文件
    "nwacs_main.py",
    "启动NWACS.bat",
    "启动小说创作系统.bat",
    # 配置文件
    "config.json",
    # 核心工具（保留几个最完整的）
    "nwacs_console.py",
    "novel_writer_config.py",
    # Skill 目录
    "skills/",
    # output 目录（保留已生成的内容）
    "output/",
    # README
    "README.md"
]

# 定义可以删除的临时/重复/旧文件
TEMP_FILES = [
    "generate_*.py",
    "demo_*.py",
    "check_*.py",
    "test_*.py",
    "setup_*.py",
    "update_*.py",
    "search_*.py",
    "verify_*.py",
    "fix_*.py",
    "make_*.py",
    "create_*.py",
    "convert_*.py",
    "optimize_*.py",
    "full_optimization.py",
    "regenerate_chapters_v3.py",
    "quick_novel.py",
    "changye_continuation_plan.py",
    "novel_creation_system.py",
    "plan_million_word_novel.py",
    "collaborative_chapter_generator.py",
    "generate_million_word_novel.py",
    "nwacs_deepseek_v3.py",
    "nwacs_deepseek_unified.py",
    "nwacs_new_skills.py",
    "nwacs_skill_learning.py",
    "nwacs_learning_system.py",
    "nwacs_comprehensive_learning.py",
    "nwacs_skill_intelligent_learning.py",
    "auto_idle_learning.py",
    "run_learning.py",
    "smart_distribute.py",
    "system_maintenance.py"
]

def organize_files():
    """第一阶段：整理目录结构"""
    print(f"""
{'='*60}
第一阶段：整理目录结构
{'='*60}
    """)
    
    # 创建归档目录
    os.makedirs('archive/', exist_ok=True)
    os.makedirs('tools/', exist_ok=True)
    os.makedirs('tools/archive/', exist_ok=True)
    
    print("✅ 目录创建完成")

def cleanup_temp_files():
    """第二阶段：清理临时/重复文件"""
    print(f"""
{'='*60}
第二阶段：清理临时/重复文件
{'='*60}
    """)
    
    deleted_count = 0
    files = os.listdir('.')
    
    for file in files:
        # 检查是否是需要删除的模式
        should_delete = False
        for pattern in TEMP_FILES:
            if file.startswith(tuple(pattern.replace('*.py',''))) and file.endswith('.py'):
                should_delete = True
                break
        
        # 或者检查文件名包含某些关键词
        if not should_delete:
            keywords = ['demo', 'test', 'check', 'update', 'setup', 'search', 'verify', 'fix', 'make', 'create', 'convert']
            for keyword in keywords:
                if keyword in file and file.endswith('.py'):
                    should_delete = True
                    break
        
        if should_delete and file not in CORE_FILES and os.path.isfile(file):
            # 移动到归档，而不是直接删除
            shutil.move(file, 'tools/archive/' + file)
            print(f"  📦 已归档: {file}")
            deleted_count += 1
    
    print(f"\n✅ 第二阶段完成，共归档 {deleted_count} 个临时文件")
    return deleted_count

def create_unified_tool():
    """第三阶段：创建统一工具"""
    print(f"""
{'='*60}
第三阶段：创建统一工具
{'='*60}
    """)
    
    print("✅ 统一工具将在下一个脚本中创建")
    return True

def create_framework_system():
    """第四阶段：创建框架生成系统"""
    print(f"""
{'='*60}
第四阶段：创建小说框架生成系统
{'='*60}
    """)
    
    print("✅ 框架系统将在下一个脚本中创建")
    return True

def main():
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║        NWACS 文件整理与优化工具 v{VERSION}                        ║
║                                                              ║
║  功能：                                                    ║
║  1. 整理目录结构                                           ║
║  2. 清理临时/重复/旧文件（归档而非删除）                  ║
║  3. 整合核心功能                                           ║
║  4. 创建统一的框架生成系统                                  ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # 确认是否继续
    confirm = input("\n⚠️ 开始文件整理？(yes/no): ").lower()
    if confirm != 'yes':
        print("已取消。")
        return
    
    # 执行四个阶段
    organize_files()
    cleanup_temp_files()
    create_unified_tool()
    create_framework_system()
    
    print(f"""
{'='*60}
🎉 文件整理完成！
{'='*60}

下一步建议：
1. 查看归档目录：tools/archive/
2. 使用统一工具创作小说
3. 使用框架系统先构思，再生成内容

所有旧文件都已安全归档，不会丢失！
    """)

if __name__ == "__main__":
    main()
