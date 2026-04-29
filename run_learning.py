#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 学习系统启动脚本
运行此脚本启动所有Skill的自主学习功能
"""

import sys
import os

# 添加src/core到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'core'))

from skill_learning_manager import SkillLearningManager
import time

def main():
    print("=" * 60)
    print("    NWACS 自主学习系统")
    print("=" * 60)
    print("\n正在初始化学习管理器...")
    
    # 创建管理器
    manager = SkillLearningManager()
    manager.initialize_learners()
    
    # 启动所有学习器
    print(f"\n已初始化 {len(manager.skill_learners)} 个Skill学习器")
    print("\n启动所有Skill学习器...")
    manager.start_all_learners()
    
    # 显示状态
    print("\n当前学习状态:")
    manager.print_status()
    
    # 保持运行
    print("\n学习系统已启动！按 Ctrl+C 停止")
    print("学习器将每30分钟自动学习一次")
    print("=" * 60)
    
    try:
        while True:
            time.sleep(60)
            # 每分钟更新一次状态
            os.system('cls' if os.name == 'nt' else 'clear')
            print("=" * 60)
            print("    NWACS 自主学习系统 - 运行中")
            print("=" * 60)
            manager.print_status()
            print("\n按 Ctrl+C 停止学习系统")
    except KeyboardInterrupt:
        manager.stop_all_learners()
        print("\n\n学习系统已停止")

if __name__ == "__main__":
    main()