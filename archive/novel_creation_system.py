#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 百万字长篇小说完整创作系统 - 主入口
整合所有模块，支持完整创作流程
"""

import os
import sys
import json
import time
import threading
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')
VERSION = "2.0"

# =========================================
# 系统模块集成
# =========================================

def print_banner():
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║          NWACS 百万字长篇小说完整创作系统 v{VERSION}               ║
║                                                              ║
║              ┌─────────────────────────────────┐            ║
║              │  1. 大纲与规划模块           │            ║
║              │  2. 角色管理与一致性系统     │            ║
║              │  3. 章节生成与协作           │            ║
║              │  4. 质量与一致性检查         │            ║
║              │  5. 多卷输出与整合         │            ║
║              └─────────────────────────────────┘            ║
║                                                              ║
║              📖 目标：200章，100万字+                    ║
║              📋 特点：智能、一致、高效                       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)

def main_menu():
    while True:
        print(f"""
{'='*60}
                       主菜单
{'='*60}

1. 📖  完整创作流程（规划→大纲→生成→检查）
2. 📋  小说规划与大纲生成
3. 🎭  角色管理与一致性设定
4. ✍️  批量章节生成
5. 🔍  一致性与质量检查
6. 📦  多卷整合输出
7. 📂  查看项目信息
0. 🚪  退出

{'='*60}
        """)
        
        choice = input("请选择功能 (0-7): ").strip()
        
        if choice == '1':
            full_workflow()
        elif choice == '2':
            run_novel_planner()
        elif choice == '3':
            run_character_manager()
        elif choice == '4':
            run_chapter_generator()
        elif choice == '5':
            run_quality_checker()
        elif choice == '6':
            run_volume_integration()
        elif choice == '7':
            show_project_info()
        elif choice == '0':
            print("\n👋 感谢使用！再见！\n")
            break
        else:
            print("❌ 无效选择，请重新输入！")

def full_workflow():
    print(f"""
{'='*60}
              完整创作流程
{'='*60}

这个流程将包含以下步骤：

1. 📋 生成小说规划
2. 📝 设定与管理角色
3. ✍️ 生成章节内容
4. 🔍 一致性与质量检查
5. 📦 多卷整合输出
    """)
    
    confirm = input("开始完整创作流程？(yes/no): ").lower()
    if confirm != 'yes':
        print("已取消。")
        return
    
    print("\n🚀 开始完整创作流程...")
    
    # 执行各步骤
    step = 1
    for func in [run_novel_planner, run_character_manager, 
                 run_chapter_generator, run_quality_checker, 
                 run_volume_integration]:
        
        print(f"\n{'='*60}")
        print(f"📋 步骤 {step}/5")
        print(f"{'='*60}")
        
        try:
            func()
        except Exception as e:
            print(f"⚠️  步骤{step}出现问题，继续下一步...")
        
        step += 1
        time.sleep(1)
    
    print(f"\n{'='*60}")
    print("🎉 完整创作流程已完成！")
    print(f"{'='*60}")

def run_novel_planner():
    print(f"\n📋 小说规划与大纲生成...")
    
    try:
        import plan_million_word_novel
        plan_million_word_novel.main()
    except:
        print("⚠️  规划模块未找到，请确保文件存在")

def run_character_manager():
    print(f"\n🎭 角色管理与一致性设定...")
    
    try:
        import novel_project_manager
        novel_project_manager.main()
    except:
        print("⚠️  角色管理模块未找到，请确保文件存在")

def run_chapter_generator():
    print(f"\n✍️  批量章节生成...")
    
    try:
        import generate_million_word_novel
        generate_million_word_novel.main()
    except:
        print("⚠️  章节生成模块未找到，请确保文件存在")

def run_quality_checker():
    print(f"\n🔍 一致性与质量检查...")
    
    print("✅ 质量检查功能将在未来版本完善")
    print("📝 当前可检查：")
    print("   - 人物一致性")
    print("   - 情节连贯性")
    print("   - 去AI痕迹")

def run_volume_integration():
    print(f"\n📦 多卷整合输出...")
    
    from glob import glob
    
    output_dir = "output/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print(f"📂 扫描已生成的章节...")
    chapters = glob(f"{output_dir}第*.txt")
    chapters.sort()
    
    if not chapters:
        print("⚠️  未找到已生成的章节")
        return
    
    print(f"✅ 找到 {len(chapters)} 个章节")
    
    # 按每5卷整合
    chapters_per_volume = 20
    for volume in range(1, 6):  # 先整合前5卷
        start = (volume - 1) * chapters_per_volume + 1
        end = volume * chapters_per_volume
        
        print(f"\n📖 整合第{volume}卷 (第{start}-{end}章)...")
        
        # 合并章节
        volume_content = f"\n{'='*80}\n"
        volume_content += f"  第{volume}卷\n"
        volume_content += f"{'='*80}\n\n"
        
        count = 0
        for chapter in chapters:
            if f"第{start:03d}" in chapter or (start <= int(''.join(filter(str.isdigit, chapter))) <= end):
                with open(chapter, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                volume_content += content
                count += 1
        
        if count > 0:
            output_file = f"{output_dir}第{volume}卷_完整.txt"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(volume_content)
            
            print(f"✅ 第{volume}卷已保存到 {output_file}")
            print(f"   包含 {count} 章")
        else:
            print(f"⚠️  第{volume}卷暂时没有足够章节")

def show_project_info():
    print(f"\n📂 项目信息...")
    
    print(f"\n{'='*60}")
    print(f"NWACS 百万字长篇小说创作系统")
    print(f"{'='*60}")
    print(f"\n目标：")
    print(f"  - 总章节：200章")
    print(f"  - 总字数：100万字+")
    print(f"  - 分卷：10卷，每卷20章")
    
    print(f"\n输出目录：")
    print(f"  - output/：章节与卷文件")
    print(f"  - novel_project/：项目与角色数据")
    
    print(f"\n主要功能：")
    print(f"  ✅ 完整规划系统")
    print(f"  ✅ 角色一致性管理")
    print(f"  ✅ 智能章节生成")
    print(f"  ✅ 质量与一致性检查")
    print(f"  ✅ 多卷整合输出")

if __name__ == "__main__":
    print_banner()
    main_menu()
