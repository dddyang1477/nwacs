#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
搜索短篇小说改编短剧趋势
"""

import sys
import os

# 添加src/core到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'core'))

def search_drama_trends():
    print("=" * 60)
    print("    搜索：短篇小说改编短剧趋势")
    print("=" * 60)
    
    # 导入模块
    from web_learning import get_web_learning
    
    # 创建学习实例
    web_learning = get_web_learning()
    
    # 搜索主题
    topics = [
        "2025 2026 短篇小说改编短剧 趋势分析",
        "短剧热门类型 爆款特征",
        "短篇小说改编短剧 写作技巧",
        "短剧剧本创作方法"
    ]
    
    all_results = []
    
    for topic in topics:
        print("\n[搜索主题]: %s" % topic)
        print("-" * 50)
        
        try:
            result = web_learning.search_and_learn("短篇小说爽文大师", topic)
            
            if result:
                # 提取要点
                key_points = result.get('key_points', [])
                trends = result.get('trends', [])
                search_results = result.get('search_results', [])
                
                print("【学习要点】:")
                for i, point in enumerate(key_points, 1):
                    print("  %d. %s" % (i, point))
                
                if trends:
                    print("\n【趋势分析】:")
                    for i, trend in enumerate(trends, 1):
                        print("  %d. %s" % (i, trend))
                
                all_results.append(result)
                
        except Exception as e:
            print("  搜索失败: %s" % e)
    
    # 总结
    print("\n" + "=" * 60)
    print("    搜索完成！")
    print("=" * 60)
    print("已搜索 %d 个主题，获取了丰富的学习内容" % len(all_results))
    print("这些内容将用于优化短篇小说创作Skill")

if __name__ == "__main__":
    search_drama_trends()