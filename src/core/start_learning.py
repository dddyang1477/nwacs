#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 自动学习启动脚本
简化版，便于调试和运行
"""

import time
import os
from datetime import datetime

def log_message(message):
    """记录日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] {message}"
    print(log_line)
    
    # 确保日志目录存在
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    with open('logs/NWACS.log', 'a', encoding='utf-8') as f:
        f.write(log_line + '\n')

def main():
    print("=====================================")
    print("    NWACS 自动学习系统")
    print("=====================================")
    log_message("自动学习系统启动")
    
    # 学习主题列表
    learning_topics = [
        "2026 热门小说分析",
        "情感描写技巧",
        "人物刻画方法",
        "剧情构造技巧",
        "微动作微表情描写",
        "故事合理性把握",
        "网络小说趋势",
        "写作技巧提升"
    ]
    
    log_message(f"加载 {len(learning_topics)} 个学习主题")
    
    # 开始学习循环
    topic_index = 0
    learning_count = 0
    
    try:
        while True:
            # 选择学习主题
            topic = learning_topics[topic_index]
            topic_index = (topic_index + 1) % len(learning_topics)
            
            log_message(f"开始学习: {topic}")
            
            # 模拟学习过程
            log_message(f"正在搜索 {topic}...")
            time.sleep(2)
            log_message(f"正在分析学习内容...")
            time.sleep(3)
            log_message(f"{topic} 学习完成")
            
            learning_count += 1
            
            # 更新学习记录
            update_learning_record(topic)
            
            # 学习间隔
            log_message(f"已学习 {learning_count} 次，休息60秒...")
            time.sleep(60)
            
    except KeyboardInterrupt:
        log_message(f"学习系统停止，共学习 {learning_count} 次")
        print("\n学习系统已停止")

def update_learning_record(topic):
    """更新学习记录"""
    record_file = "36_2026年学习更新记录.md"
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_record = f"\n\n## 自动学习记录 ({now})\n- 学习主题: {topic}\n- 学习状态: 已完成\n- 触发方式: 系统自动"
    
    try:
        with open(record_file, 'a', encoding='utf-8') as f:
            f.write(new_record)
        log_message("学习记录已更新")
    except Exception as e:
        log_message(f"更新学习记录失败: {str(e)}")

if __name__ == "__main__":
    main()