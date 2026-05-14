#!/usr/bin/env python3
"""
NWACS 高级流水线：带审核门禁和自动重试
运行: python advanced_pipeline.py
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from orchestrator import ConfigManager, AgentExecutor, Pipeline

def audit_passed(results):
    """检查审核是否通过"""
    if not results:
        return False
    last = results[-1]
    if not last.get("success"):
        return False
    content = last.get("content", "")
    # 如果审核报告包含"通过"或分数>80，视为通过
    return "通过" in content or ("综合去AI分" in content and 
           any(int(x) > 80 for x in re.findall(r'\d+', content)))

# 初始化
config = ConfigManager("config")
executor = AgentExecutor(config)
pipeline = Pipeline(executor)

# 阶段1: 创作
pipeline.add_step("剧情构造师", "创作第2章大纲，都市言情题材，主角在咖啡厅偶遇前任")
pipeline.add_step("场景构造师", "生成咖啡厅场景，要求：温馨但尴尬的氛围")
pipeline.add_step("对话设计师", "设计对话，要求：表面客气，实则刀光剑影")

# 阶段2: 审核（去AI）
pipeline.add_step("去AI监督官", "审核成品，输出评分和修改清单")

# 阶段3: 如审核通过，继续质量审计；如未通过，跳过
pipeline.add_step(
    "质量审计师", 
    "进行质量审计：检查人设一致性、逻辑矛盾",
    condition=audit_passed  # 只有去AI审核通过才执行
)

# 执行
results = pipeline.run()

# 保存
if results:
    os.makedirs("output/chapters", exist_ok=True)
    with open("output/chapters/chapter_002.md", "w", encoding="utf-8") as f:
        f.write(results[-1]["content"])
    print("\n第2章已保存")
