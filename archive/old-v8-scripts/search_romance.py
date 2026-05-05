#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
搜索感情小说相关学习内容：狗血剧情、反转剧情、世界观构造
"""

import sys
import os

# 添加src/core到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'core'))

def search_romance_novels():
    print("=" * 60)
    print("    搜索：感情小说创作技巧")
    print("=" * 60)
    
    from web_learning import get_web_learning
    
    # 创建学习实例
    web_learning = get_web_learning()
    
    # 搜索主题列表
    topics = [
        "感情小说 狗血剧情 套路 桥段",
        "言情小说 吸引读者 剧情设计",
        "小说 大反转剧情 神转折 写法",
        "爱情小说 故事背景 世界观构造",
        "言情小说 虐恋 误会 追妻火葬场",
        "甜宠文 撒糖技巧 甜蜜互动",
        "霸总文 经典套路 身份反差",
        "重生文 复仇爽点 因果报应"
    ]
    
    all_results = []
    
    for topic in topics:
        print("\n" + "=" * 50)
        print("[搜索主题]: %s" % topic)
        print("-" * 50)
        
        try:
            result = web_learning.search_and_learn("短篇小说爽文大师", topic)
            
            if result:
                key_points = result.get('key_points', [])
                trends = result.get('trends', [])
                tips = result.get('tips', [])
                
                print("【核心要点】:")
                for i, point in enumerate(key_points, 1):
                    if len(point) > 5:  # 过滤纯数字
                        print("  %d. %s" % (i, point))
                
                if trends:
                    print("\n【趋势标签】: %s" % ", ".join(trends))
                
                if tips:
                    print("\n【写作技巧】:")
                    for i, tip in enumerate(tips, 1):
                        print("  %d. %s" % (i, tip))
                
                all_results.append(result)
                
        except Exception as e:
            print("  搜索失败: %s" % e)
    
    # 总结
    print("\n" + "=" * 60)
    print("    搜索完成！")
    print("=" * 60)
    print("已搜索 %d 个主题" % len(all_results))
    print("学习内容已自动分发到对应的Skill文件")

if __name__ == "__main__":
    search_romance_novels()