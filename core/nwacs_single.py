#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 单次执行模式
每次只执行一个功能，不进入循环，避免卡住
用法：
py nwacs_single.py 1 新小说名称  # 生成框架（可指定小说名）
py nwacs_single.py 2  # 生成章节标题
py nwacs_single.py 3  # 添加伏笔
py nwacs_single.py 0  # 查看帮助
"""

import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

VERSION = "3.0"

def print_help():
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     NWACS 单次执行模式 v{VERSION}                                 ║
║                                                              ║
║  用法：py nwacs_single.py [功能编号] [参数]                    ║
║                                                              ║
║  功能列表：                                                  ║
║    1 [小说名] - 生成完整框架（可指定小说名）                    ║
║    2 - 生成章节标题（200章）                                 ║
║    3 - 添加伏笔                                             ║
║    4 - 添加时间线事件                                       ║
║    5 - 导出框架为TXT                                       ║
║    6 - 打印项目状态                                        ║
║    0 - 显示帮助                                            ║
║                                                              ║
║  示例：                                                      ║
║    py nwacs_single.py 1 我的新小说  # 生成新小说框架          ║
║    py nwacs_single.py 1             # 生成默认框架           ║
║    py nwacs_single.py 2             # 生成章节标题           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)

def run_function(choice, args=None):
    from novel_project_manager import NovelProjectManager

    novel_name = args[0] if args else "默认小说"
    manager = NovelProjectManager(novel_name)

    if choice == '1':
        print(f"\n🌍 生成小说《{novel_name}》完整框架...")
        novel_type = input("小说类型（默认玄幻修仙）: ").strip() or "玄幻修仙"
        main_theme = input("核心主题（默认复仇与成长）: ").strip() or "复仇与成长"

        print("\n正在生成世界观...")
        manager.generate_world_framework(novel_type, main_theme)

        print("\n正在生成人物...")
        manager.generate_character_framework()

        print("\n正在生成剧情...")
        manager.generate_plot_framework()

        print("\n正在导出框架...")
        manager.export_frameworks_to_txt()
        print(f"\n✅ 小说《{novel_name}》框架生成完成！")
        print(f"📁 保存位置：novel_project/{novel_name}/")

    elif choice == '2':
        print("\n📝 生成章节标题...")
        titles = manager.generate_chapter_titles()
        print(f"✅ 生成了 {len(titles)} 章标题")

    elif choice == '3':
        name = args[0] if args else input("伏笔名称: ")
        desc = args[1] if len(args) > 1 else input("伏笔描述: ")
        chapter = int(args[2]) if len(args) > 2 else int(input("埋下章节: "))
        resolve = int(args[3]) if len(args) > 3 else 0
        manager.add_plot_hook(name, desc, chapter, resolve)
        print(f"✅ 伏笔 '{name}' 已添加！")

    elif choice == '4':
        chapter = int(args[0]) if args else int(input("章节: "))
        title = args[1] if len(args) > 1 else input("事件标题: ")
        desc = args[2] if len(args) > 2 else input("事件描述: ")
        etype = args[3] if len(args) > 3 else "main"
        manager.add_timeline_event(chapter, title, desc, etype)
        print(f"✅ 时间线事件已添加！")

    elif choice == '5':
        print("\n📤 导出框架...")
        manager.export_frameworks_to_txt()
        print("✅ 框架已导出！")

    elif choice == '6':
        manager.print_status()

    else:
        print_help()

def main():
    if len(sys.argv) < 2:
        print_help()
        return

    choice = sys.argv[1]
    args = sys.argv[2:] if len(sys.argv) > 2 else []

    if choice == '0':
        print_help()
    else:
        try:
            run_function(choice, args)
        except Exception as e:
            print(f"\n❌ 错误：{e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()
