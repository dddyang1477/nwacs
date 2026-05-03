#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 2026各平台爆款深度剖析报告展示工具
基于2026年5月最新联网数据
"""

import os

def show_report():
    """展示完整报告"""
    report_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "2026各平台爆款深度剖析报告.md")
    
    print("\n" + "="*80)
    print("📊 NWACS 2026各平台爆款深度剖析报告")
    print("="*80)
    print("\n数据来源：起点中文网、番茄小说、晋江文学城、抖音精选APP")
    print("整理时间：2026年5月3日")
    print("\n" + "="*80)
    
    if os.path.exists(report_file):
        with open(report_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if '==' in line or ('--' in line and len(line) < 10):
                continue
            if line.strip():
                print(line)
            
            if i % 100 == 0 and i > 0:
                input("\n按回车继续显示...")
        
        print("\n" + "="*80)
        print(f"📁 完整报告已保存至: {report_file}")
        print("="*80)
    else:
        print(f"\n❌ 报告文件不存在: {report_file}")
        print("请确保 '2026各平台爆款深度剖析报告.md' 文件存在")

if __name__ == "__main__":
    show_report()
    input("\n按回车退出...")
