#!/usr/bin/env python3
"""
NWACS 流水线示例：创作第1章
运行: python example_pipeline.py
"""
import os
import sys

# 确保 orchestrator.py 在同目录
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from orchestrator import ConfigManager, AgentExecutor, Pipeline

# 初始化
config = ConfigManager("config")
executor = AgentExecutor(config)
pipeline = Pipeline(executor)

# 定义流水线：创作一章小说
pipeline.add_step(
    "剧情构造师",
    "创作第1章大纲：主角在雨夜古庙遇到神秘人。要求：3000字，玄幻题材，埋设1个伏笔",
    context_files=["nwacs-data/world_setting.md"] if os.path.exists("nwacs-data/world_setting.md") else []
)

pipeline.add_step(
    "场景构造师",
    "根据大纲生成场景描写。要求：暴雨、古庙、神秘氛围，至少调动3种感官",
)

pipeline.add_step(
    "对话设计师",
    "为场景设计对话。要求：潜台词丰富，主角倔强，神秘人深不可测",
)

pipeline.add_step(
    "去AI监督官",
    "审核以上成品。检查：无主句、情绪标签、AI连接词、句式模板化。如发现问题列出清单",
)

# 执行
results = pipeline.run()

# 保存结果
if results and results[-1].get("success"):
    final_content = results[-1]["content"]

    # 保存章节
    os.makedirs("output/chapters", exist_ok=True)
    with open("output/chapters/chapter_001.md", "w", encoding="utf-8") as f:
        f.write(final_content)
    print("\n第1章已保存到 output/chapters/chapter_001.md")

    # 保存审核报告（倒数第二步）
    if len(results) >= 2 and results[-2].get("success"):
        with open("output/review/chapter_001_review.md", "w", encoding="utf-8") as f:
            f.write(results[-2]["content"])
        print("审核报告已保存到 output/review/chapter_001_review.md")
