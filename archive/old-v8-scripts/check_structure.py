#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 工具结构检查器
"""

import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

def print_tree(path, indent=0):
    if indent == 0:
        print('='*80)
        print('              NWACS 工具结构总览')
        print('='*80)
    
    items = sorted(os.listdir(path))
    for item in items:
        if item.startswith('.') or item == '__pycache__':
            continue
        full_path = os.path.join(path, item)
        prefix = '|   ' * (indent // 2)
        
        if os.path.isdir(full_path):
            print(f'{prefix}{"├─" if indent > 0 else ""}[DIR] {item}/')
            print_tree(full_path, indent + 2)
        elif item.endswith('.py'):
            print(f'{prefix}{"├─" if indent > 0 else ""}[PY] {item}')
        elif item.endswith('.json'):
            print(f'{prefix}{"├─" if indent > 0 else ""}[CFG] {item}')

def show_function_summary():
    print('\n' + '='*80)
    print('              NWACS 功能模块汇总')
    print('='*80)
    
    modules = [
        ('nwacs_console.py', '统一控制台入口', '启动系统、写作模式、配置工具'),
        ('generate_novel.py', '智能小说生成器', '交互式选择、大纲生成、内容创作'),
        ('quick_novel.py', '快速小说生成', '一键生成预设短篇小说'),
        ('optimize_with_deepseek.py', '大模型优化器', '系统分析、优化报告、实施优化'),
        ('full_optimization.py', '全网学习优化器', '词汇、写作、场景、去AI化学习'),
        ('smart_distribute.py', '智能分发器', '学习内容分发到对应Skill'),
    ]
    
    print('\n[主程序模块]')
    print('-'*60)
    for file, desc, features in modules:
        print(f'  • {file}')
        print(f'    描述: {desc}')
        print(f'    功能: {features}')
        print()
    
    print('\n[核心子系统]')
    print('-'*60)
    subsystems = [
        ('src/core/main_system.py', '主系统管理', '启动所有服务'),
        ('src/core/learning_service.py', '学习服务', '联网学习、知识更新'),
        ('src/core/idle_learning.py', '空闲学习', '电脑空闲时自动学习'),
        ('src/core/daily_checker.py', '每日自检', 'Skill体检、文件清理'),
        ('src/core/llm_optimizer.py', '大模型优化', '连接优化、限流控制'),
        ('src/core/git_sync_enhanced.py', 'Git同步', '代码同步、网络重试'),
    ]
    
    for file, desc, features in subsystems:
        print(f'  • {file}')
        print(f'    描述: {desc}')
        print(f'    功能: {features}')
        print()
    
    print('\n[Skill模块]')
    print('-'*60)
    skills = [
        ('level1', '小说总调度官', '一级Skill，统筹管理'),
        ('level2', '二级Skill', '世界观、剧情、场景、对话、角色、战斗、写作技巧等'),
        ('level3', '三级Skill', '小说类型、玄幻仙侠、都市言情、悬疑推理等'),
        ('CharacterMaster', '角色大师', '人物设定、关系网络'),
        ('PlotMaster', '剧情大师', '情节设计、伏笔埋设'),
        ('GoldenPhraseMaster', '词汇大师', '词汇储备、描写素材'),
    ]
    
    for folder, desc, features in skills:
        print(f'  • skills/{folder}/')
        print(f'    描述: {desc}')
        print(f'    功能: {features}')
        print()

def main():
    print_tree('.')
    show_function_summary()
    
    print('='*80)
    print('                    检查完成！')
    print('='*80)

if __name__ == "__main__":
    import sys
    main()
