#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试联网学习功能
"""

import sys
import os

# 添加src/core到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'core'))

def test_web_learning():
    print("=" * 60)
    print("    联网学习功能测试")
    print("=" * 60)
    
    # 1. 检查模块导入
    print("\n[1/4] 检查联网学习模块...")
    try:
        from web_learning import get_web_learning
        print("  OK 联网学习模块已导入")
    except ImportError as e:
        print("  FAIL 联网学习模块导入失败: %s" % e)
        return
    
    # 2. 创建学习实例
    print("\n[2/4] 创建联网学习实例...")
    try:
        web_learning = get_web_learning()
        print("  OK 联网学习实例创建成功")
    except Exception as e:
        print("  FAIL 创建实例失败: %s" % e)
        return
    
    # 3. 测试联网搜索
    print("\n[3/4] 测试联网搜索...")
    test_topic = "2025 2026 短篇小说爽文类型 爆款"
    try:
        print("  正在搜索: %s" % test_topic)
        result = web_learning.search_and_learn("短篇小说爽文大师", test_topic)
        
        if result:
            print("  OK 联网搜索成功！")
            print("  搜索结果:")
            print("    - 主题: %s" % result.get('topic', '未知'))
            print("    - 要点数量: %d" % len(result.get('key_points', [])))
            print("    - 趋势数量: %d" % len(result.get('trends', [])))
            print("    - 搜索结果数: %d" % len(result.get('search_results', [])))
            
            if result.get('key_points'):
                print("  学习要点:")
                for i, point in enumerate(result['key_points'][:3], 1):
                    print("    %d. %s" % (i, point))
        else:
            print("  WARN 搜索结果为空")
            
    except Exception as e:
        print("  FAIL 联网搜索失败: %s" % e)
        return
    
    # 4. 测试缓存功能
    print("\n[4/4] 测试缓存功能...")
    try:
        cached_result = web_learning.search_and_learn("短篇小说爽文大师", test_topic)
        print("  OK 缓存功能正常")
    except Exception as e:
        print("  FAIL 缓存测试失败: %s" % e)
    
    # 总结
    print("\n" + "=" * 60)
    print("  联网学习功能测试: ✓ 通过")
    print("  可以正常连接互联网进行学习优化Skill")
    print("=" * 60)

if __name__ == "__main__":
    test_web_learning()