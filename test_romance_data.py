#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直接测试感情小说学习内容（跳过缓存）
"""

import sys
import os

# 添加src/core到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'core'))

def test_romance_topics():
    print("=" * 60)
    print("    感情小说创作技巧 - 学习内容")
    print("=" * 60)
    
    from web_learning import WebLearning
    
    # 创建新实例（不加载缓存）
    web_learning = WebLearning()
    
    # 清空缓存
    web_learning.learning_cache = {}
    
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
    
    for topic in topics:
        print("\n" + "=" * 50)
        print("[主题]: %s" % topic)
        print("-" * 50)
        
        # 直接调用内部方法获取模拟数据
        mock_result = web_learning._get_mock_search_result(topic)
        
        if mock_result:
            print("【标题】: %s" % mock_result.get('title', ''))
            print("【来源】: %s" % mock_result.get('source', ''))
            print("【内容】:")
            content = mock_result.get('content', '')
            # 分段显示
            sentences = content.split('。')
            for i, sentence in enumerate(sentences[:5], 1):
                if sentence.strip():
                    print("  %d. %s。" % (i, sentence.strip()))
            
            # 显示完整内容
            print("\n【完整内容】:")
            print(content)
        
        else:
            print("  暂无数据")
    
    # 总结
    print("\n" + "=" * 60)
    print("    学习内容已准备完成！")
    print("=" * 60)

if __name__ == "__main__":
    test_romance_topics()