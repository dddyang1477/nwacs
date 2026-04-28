#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 学习系统测试脚本
验证自动学习功能是否正常工作
"""

import time
import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from logger import logger
from auto_learning import AutoLearningSystem

def test_learning_system():
    """测试自动学习系统"""
    print("=====================================")
    print("    NWACS 学习系统测试")
    print("=====================================")
    
    # 创建学习系统（独立模式）
    print("\n初始化自动学习系统...")
    system = AutoLearningSystem(standalone=True)
    print("✓ 自动学习系统初始化完成")
    
    # 测试学习触发
    print("\n测试手动触发学习...")
    system.trigger_learning("测试触发")
    print("✓ 学习触发成功")
    
    # 获取统计信息
    stats = system.get_stats()
    print("\n学习系统统计:")
    print(f"  学习次数: {stats['learning_count']}")
    print(f"  错误次数: {stats['error_count']}")
    print(f"  是否正在学习: {'是' if stats['is_learning'] else '否'}")
    
    # 模拟空闲状态触发学习
    print("\n模拟空闲状态（30秒后触发学习）...")
    time.sleep(30)
    
    # 再次获取统计
    stats = system.get_stats()
    print("\n学习系统统计（空闲触发后）:")
    print(f"  学习次数: {stats['learning_count']}")
    print(f"  错误次数: {stats['error_count']}")
    
    print("\n✓ 测试完成！")

if __name__ == "__main__":
    try:
        test_learning_system()
    except Exception as e:
        logger.log_exception(e, "test_learning_system")
        print(f"测试失败: {str(e)}")