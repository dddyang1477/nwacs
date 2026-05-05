#!/usr/bin/env python3
"""
NWACS 批量流水线：连续创作多章
运行: python batch_pipeline.py
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from orchestrator import ConfigManager, AgentExecutor, Pipeline

def create_chapter(chapter_no: int, theme: str, genre: str):
    """创作单章"""
    config = ConfigManager("config")
    executor = AgentExecutor(config)
    pipeline = Pipeline(executor)

    pipeline.add_step(
        "剧情构造师",
        f"创作第{chapter_no}章大纲。主题：{theme}。类型：{genre}。要求：埋设或回收伏笔"
    )
    pipeline.add_step("场景构造师", "生成核心场景描写")
    pipeline.add_step("对话设计师", "设计关键对话")
    pipeline.add_step("去AI监督官", "审核去AI化程度")

    results = pipeline.run()

    # 保存
    if results and results[-1].get("success"):
        os.makedirs("output/chapters", exist_ok=True)
        path = f"output/chapters/chapter_{chapter_no:03d}.md"
        with open(path, "w", encoding="utf-8") as f:
            f.write(results[-1]["content"])
        print(f"第{chapter_no}章已保存: {path}")
        return True
    return False

# 批量创作3章
chapters = [
    (3, "主角发现神秘组织的线索", "悬疑推理"),
    (4, "主角与导师的决裂", "玄幻仙侠"),
    (5, "最终决战前的宁静", "科幻未来")
]

for no, theme, genre in chapters:
    print(f"\n{'='*40}")
    print(f"开始创作第{no}章")
    print(f"{'='*40}")
    success = create_chapter(no, theme, genre)
    if not success:
        print(f"第{no}章创作失败，停止批量")
        break

print("\n批量创作完成")
