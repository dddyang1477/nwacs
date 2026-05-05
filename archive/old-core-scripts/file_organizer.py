#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 文件结构优化器
整合整理文件，创建清晰的目录结构
"""

import os
import sys
import shutil
import json
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

VERSION = "1.0"

class FileOrganizer:
    """文件整理器"""
    
    def __init__(self):
        self.root_dir = os.getcwd()
        self.archive_dir = os.path.join(self.root_dir, 'archive')
        os.makedirs(self.archive_dir, exist_ok=True)
        
        # 定义目标目录结构
        self.target_structure = {
            'core/': [
                '*.py',
                '__pycache__/'
            ],
            'novels/': [
                # 每部小说一个文件夹
            ],
            'output/': [
                'chapters/',
                'outlines/',
                'drafts/'
            ],
            'learning/': [
                'materials/',      # 学习素材
                'records/',        # 学习记录
                'skills/'          # 技能文件
            ],
            'config/': [
                '*.json',
                'settings/'
            ],
            'docs/': [
                'guides/',
                'api/',
                'changelog/'
            ],
            'tools/': [
                '*.py',
                'scripts/'
            ],
            'logs/': []
        }
        
        # 需要归档的文件类型
        self.archive_patterns = [
            '*.bat',
            '*.ps1',
            '*.vbs',
            '*_old.*',
            '*_backup.*'
        ]
        
        # 根目录保留的核心文件
        self.root_keep = [
            'config.json',
            'main.py',
            'nwacs_main.py',
            'QUICK_START.md',
            'WRITING_TOOLS_GUIDE.md'
        ]
    
    def organize_files(self):
        """执行文件整理"""
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║         NWACS 文件结构优化器 v{VERSION}                          ║
║                                                              ║
║         📁 开始整理文件...                                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
        """)
        
        # 1. 创建目标目录结构
        print("\n📂 创建目标目录结构...")
        self._create_structure()
        
        # 2. 归档旧文件
        print("\n📦 归档旧文件...")
        self._archive_old_files()
        
        # 3. 整理根目录
        print("\n🧹 整理根目录...")
        self._clean_root()
        
        # 4. 整理学习目录
        print("\n📚 整理学习目录...")
        self._organize_learning()
        
        # 5. 创建统一入口
        print("\n🚪 创建统一入口...")
        self._create_main_entry()
        
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║         ✅ 文件整理完成！                                      ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
        """)
        
        self._show_final_structure()
    
    def _create_structure(self):
        """创建目录结构"""
        for dir_name, subdirs in self.target_structure.items():
            dir_path = os.path.join(self.root_dir, dir_name)
            os.makedirs(dir_path, exist_ok=True)
            
            for subdir in subdirs:
                if subdir.endswith('/'):
                    subdir_path = os.path.join(dir_path, subdir)
                    os.makedirs(subdir_path, exist_ok=True)
    
    def _archive_old_files(self):
        """归档旧文件"""
        import fnmatch
        
        for pattern in self.archive_patterns:
            for filename in os.listdir(self.root_dir):
                if fnmatch.fnmatch(filename, pattern):
                    src = os.path.join(self.root_dir, filename)
                    dst = os.path.join(self.archive_dir, filename)
                    if os.path.isfile(src) and not os.path.exists(dst):
                        shutil.move(src, dst)
                        print(f"   归档: {filename}")
    
    def _clean_root(self):
        """清理根目录"""
        for filename in os.listdir(self.root_dir):
            filepath = os.path.join(self.root_dir, filename)
            
            # 跳过保留的文件
            if filename in self.root_keep:
                continue
            
            # 跳过目录
            if os.path.isdir(filepath):
                continue
            
            # 移动到工具目录或归档
            if filename.endswith('.py'):
                dst = os.path.join(self.root_dir, 'tools', filename)
            else:
                dst = os.path.join(self.archive_dir, filename)
            
            if not os.path.exists(dst):
                shutil.move(filepath, dst)
                print(f"   移动: {filename} -> {os.path.basename(os.path.dirname(dst))}/")
    
    def _organize_learning(self):
        """整理学习目录"""
        learning_dir = os.path.join(self.root_dir, 'learning')
        
        # 移动学习相关文件
        files_to_move = [
            ('skill_knowledge_base.json', 'skills'),
            ('skill_learning_records.json', 'records'),
            ('web_learning_cache.json', 'records'),
        ]
        
        for filename, subdir in files_to_move:
            src = os.path.join(self.root_dir, filename)
            dst = os.path.join(learning_dir, subdir, filename)
            if os.path.exists(src) and not os.path.exists(dst):
                shutil.move(src, dst)
                print(f"   移动: {filename} -> learning/{subdir}/")
    
    def _create_main_entry(self):
        """创建统一入口脚本"""
        main_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 主入口
统一启动所有功能
"""

import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

def main():
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║         NWACS 小说创作系统                                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    while True:
        print("\\n请选择功能:")
        print("1. 开始创作小说")
        print("2. 管理小说项目")
        print("3. 质量检查")
        print("4. 系统学习")
        print("5. 查看帮助")
        print("0. 退出")
        
        choice = input("\\n请输入选择: ").strip()
        
        if choice == '1':
            from core import nwacs_single
            nwacs_single.main()
        elif choice == '2':
            from core import novel_project_manager
            # 简单启动项目管理器
            print("项目管理器功能开发中...")
        elif choice == '3':
            from core import novel_quality_checker
            novel_quality_checker.main()
        elif choice == '4':
            from core import book_learning_system
            book_learning_system.main()
        elif choice == '5':
            print("\\n📖 NWACS 使用指南")
            print("-" * 40)
            print("1. 创作小说: 生成大纲和章节")
            print("2. 项目管理: 管理小说项目")
            print("3. 质量检查: 检查一致性和AI痕迹")
            print("4. 系统学习: 学习写作技巧")
        elif choice == '0':
            print("\\n👋 再见!")
            break
        else:
            print("\\n❌ 无效选择")

if __name__ == "__main__":
    main()
'''
        
        with open(os.path.join(self.root_dir, 'main.py'), 'w', encoding='utf-8') as f:
            f.write(main_content)
        print("   创建: main.py (统一入口)")
    
    def _show_final_structure(self):
        """显示最终目录结构"""
        print(f"""

📁 优化后目录结构:
══════════════════════════════════════════════════════════════

NWACS/
├── core/              # 核心模块
│   ├── *.py
│   └── __pycache__/
├── novels/            # 小说项目 (每部小说独立文件夹)
│   └── [小说名]/
│       ├── chapters/
│       ├── characters/
│       ├── outline/
│       └── worldview/
├── output/            # 输出目录
│   ├── chapters/
│   ├── outlines/
│   └── drafts/
├── learning/          # 学习系统
│   ├── materials/     # 学习素材
│   ├── records/       # 学习记录
│   └── skills/        # 技能文件
├── config/            # 配置文件
│   └── settings/
├── docs/              # 文档
│   ├── guides/
│   ├── api/
│   └── changelog/
├── tools/             # 工具脚本
├── logs/              # 日志
├── archive/           # 归档文件
├── config.json        # 主配置
├── main.py            # 统一入口
├── nwacs_main.py      # 备用入口
├── QUICK_START.md     # 快速入门
└── WRITING_TOOLS_GUIDE.md  # 使用指南

══════════════════════════════════════════════════════════════
""")

def main():
    organizer = FileOrganizer()
    organizer.organize_files()

if __name__ == "__main__":
    main()