#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
联网学习：世界构造、世界规则、词汇素材（山海经、寓言故事、民间故事）
"""

import sys
import os

# 添加src/core到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'core'))

def search_worldbuilding_topics():
    print("=" * 60)
    print("    搜索：世界构造与词汇素材")
    print("=" * 60)
    
    from web_learning import get_web_learning
    
    # 创建学习实例
    web_learning = get_web_learning()
    
    # 搜索主题列表
    topics = [
        "小说世界观构造 世界规则设定 元素体系",
        "山海经 神话生物 神兽名称 词汇",
        "中国古代寓言故事 成语典故 素材",
        "民间故事 传说 神话 素材收集",
        "仙侠世界设定 修炼体系 境界划分",
        "奇幻世界构造 魔法体系 种族设定",
        "历史朝代背景 文化习俗 设定素材",
        "东方神话体系 神仙谱系 词汇"
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
                    if len(point) > 5:
                        print("  %d. %s" % (i, point))
                
                if trends:
                    print("\n【相关标签】: %s" % ", ".join(trends))
                
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
    search_worldbuilding_topics()