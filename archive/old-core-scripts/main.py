#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 主入口
统一启动所有功能
"""

import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

def load_knowledge():
    """加载知识库"""
    try:
        from core import integrated_knowledge_base
        kb = integrated_knowledge_base.IntegratedKnowledgeBase()
        return kb
    except Exception as e:
        print(f"⚠️  知识库加载失败: {e}")
        return None

def show_knowledge_summary(kb):
    """显示知识库摘要"""
    if kb:
        print("\n" + "="*60)
        print("📚 已加载综合知识库")
        print(kb.get_summary())

def knowledge_menu(kb):
    """知识库菜单"""
    while True:
        print("\n📚 知识库功能")
        print("-"*40)
        print("1. 推荐热门题材")
        print("2. 写作技巧查询")
        print("3. 剧情结构查询")
        print("4. 主角类型模板")
        print("5. 世界观类型")
        print("0. 返回主菜单")
        
        choice = input("\n请输入选择: ").strip()
        
        if choice == '1':
            print("\n🔥 必爆题材推荐:")
            topics = kb.suggest_topic('必爆')
            for i, topic in enumerate(topics, 1):
                print(f"{i}. {topic}")
            print("\n📊 稳定输出题材:")
            topics = kb.suggest_topic('稳定')
            for i, topic in enumerate(topics, 1):
                print(f"{i}. {topic}")
        
        elif choice == '2':
            print("\n✍️  写作技巧查询")
            print("1. 镜头语言")
            print("2. 五感全息")
            print("3. 情感共鸣")
            print("4. 节奏把控")
            c = input("\n请输入选择: ").strip()
            type_map = {'1':'镜头语言','2':'五感全息','3':'情感共鸣','4':'节奏把控'}
            if c in type_map:
                tips = kb.get_writing_tip(type_map[c])
                print(f"\n【{type_map[c]}】")
                for tip in tips:
                    print(f"- {tip}")
        
        elif choice == '3':
            print("\n📊 剧情结构查询")
            print("1. 经典结构")
            print("2. 创新模式")
            print("3. 情节元素")
            c = input("\n请输入选择: ").strip()
            type_map = {'1':'经典结构','2':'创新模式','3':'情节元素'}
            if c in type_map:
                struct = kb.get_plot_structure(type_map[c])
                print(f"\n【{type_map[c]}】")
                for s in struct:
                    print(f"- {s}")
        
        elif choice == '4':
            print("\n👤 主角类型模板")
            for name, desc in kb.knowledge['protagonist_types'].items():
                print(f"\n【{name}】")
                for k, v in desc.items():
                    print(f"  {k}: {v}")
        
        elif choice == '5':
            print("\n🌍 世界观类型")
            for name, desc in kb.knowledge['worldview_types'].items():
                print(f"\n【{name}】")
                for k, v in desc.items():
                    print(f"  {k}: {v}")
        
        elif choice == '0':
            break

def main():
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║         NWACS 小说创作系统                                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # 加载知识库
    kb = load_knowledge()
    show_knowledge_summary(kb)
    
    while True:
        print("\n请选择功能:")
        print("1. 开始创作小说")
        print("2. 管理小说项目")
        print("3. 质量检查")
        print("4. 系统学习")
        print("5. 知识库查询")
        print("6. 查看帮助")
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
            from core import comprehensive_learning
            learning = comprehensive_learning.AutoLearningSystem()
            learning.run_learning_cycle()
        elif choice == '5' and kb:
            knowledge_menu(kb)
        elif choice == '6':
            print("\n📖 NWACS 使用指南")
            print("-" * 40)
            print("1. 创作小说: 生成大纲和章节")
            print("2. 项目管理: 管理小说项目")
            print("3. 质量检查: 检查一致性和AI痕迹")
            print("4. 系统学习: 学习写作技巧")
            print("5. 知识库查询: 查询学习到的写作知识")
        elif choice == '0':
            print("\n👋 再见!")
            break
        else:
            print("\n❌ 无效选择")

if __name__ == "__main__":
    main()
