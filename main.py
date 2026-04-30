#!/usr/bin/env python3
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
        print("\n请选择功能:")
        print("1. 开始创作小说")
        print("2. 管理小说项目")
        print("3. 质量检查")
        print("4. 系统学习")
        print("5. 查看帮助")
        print("0. 退出")
        
        choice = input("\n请输入选择: ").strip()
        
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
            print("\n📖 NWACS 使用指南")
            print("-" * 40)
            print("1. 创作小说: 生成大纲和章节")
            print("2. 项目管理: 管理小说项目")
            print("3. 质量检查: 检查一致性和AI痕迹")
            print("4. 系统学习: 学习写作技巧")
        elif choice == '0':
            print("\n👋 再见!")
            break
        else:
            print("\n❌ 无效选择")

if __name__ == "__main__":
    main()
