#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
剧情设计器
功能：可视化情节流程图、伏笔埋设追踪、高潮节奏规划
"""

import os
import sys
import json
from datetime import datetime

class PlotDesigner:
    def __init__(self):
        self.current_plot = {
            'title': '未命名剧情',
            'chapters': [],
            'hooks': [],
            'climaxes': [],
            'turning_points': []
        }
        self.load_plot()

    def load_plot(self):
        plot_file = 'data/current_plot.json'
        if os.path.exists(plot_file):
            with open(plot_file, 'r', encoding='utf-8') as f:
                self.current_plot = json.load(f)

    def save_plot(self):
        os.makedirs('data', exist_ok=True)
        with open('data/current_plot.json', 'w', encoding='utf-8') as f:
            json.dump(self.current_plot, f, ensure_ascii=False, indent=2)

    def add_chapter(self, title, summary, tension_level=5):
        chapter = {
            'id': len(self.current_plot['chapters']) + 1,
            'title': title,
            'summary': summary,
            'tension_level': tension_level,
            'hooks': [],
            'created_at': datetime.now().isoformat()
        }
        self.current_plot['chapters'].append(chapter)
        self.save_plot()
        return chapter

    def add_hook(self, chapter_id, hook_desc):
        hook = {
            'chapter_id': chapter_id,
            'description': hook_desc,
            'resolved': False
        }
        self.current_plot['hooks'].append(hook)
        self.save_plot()
        return hook

    def add_climax(self, chapter_id, climax_desc):
        climax = {
            'chapter_id': chapter_id,
            'description': climax_desc,
            'tension_level': 10
        }
        self.current_plot['climaxes'].append(climax)
        self.save_plot()
        return climax

    def get_tension_curve(self):
        tensions = []
        for ch in self.current_plot['chapters']:
            tensions.append(ch.get('tension_level', 5))
        return tensions

    def print_summary(self):
        print("\n" + "=" * 60)
        print("              剧情设计器 - 剧情摘要")
        print("=" * 60)
        print(f"\n标题: {self.current_plot['title']}")
        print(f"章节数: {len(self.current_plot['chapters'])}")
        print(f"伏笔数: {len(self.current_plot['hooks'])}")
        print(f"高潮数: {len(self.current_plot['climaxes'])}")

        print("\n张力曲线:")
        tensions = self.get_tension_curve()
        if tensions:
            for i, t in enumerate(tensions):
                bar = "█" * t + "░" * (10 - t)
                print(f"  第{i+1}章: [{bar}] {t}/10")
        else:
            print("  暂无章节数据")

        print("\n伏笔追踪:")
        for hook in self.current_plot['hooks']:
            status = "OK" if hook.get('resolved') else "PENDING"
            print(f"  [{status}] Chapter {hook['chapter_id']}: {hook['description']}")

def main():
    designer = PlotDesigner()
    designer.print_summary()
    print("\n[Plot Designer Ready]")

if __name__ == "__main__":
    main()
