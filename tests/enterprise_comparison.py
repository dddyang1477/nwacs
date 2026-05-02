#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS企业级优化对比工具
使用DeepSeek对比NWACS与企业级写作工具，找出优化方向
"""

import os
import json
from pathlib import Path
from datetime import datetime

try:
    from openai import OpenAI
except ImportError:
    print("❌ 请先安装 openai 库：pip install openai")
    exit(1)


def main():
    print("="*60)
    print("🏢 NWACS企业级对比与优化")
    print("使用DeepSeek对比企业级写作工具")
    print("="*60)
    print()

    # 设置API Key
    api_key = "sk-f3246fbd1eef446e9a11d78efefd9bba"

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com"
    )

    project_root = Path(__file__).parent

    # 读取NWACS信息
    print("📖 读取NWACS项目信息...")
    nwacs_info = ""

    for filepath in [
        "docs/architecture/01_系统架构框架.md",
        "项目状态报告.md",
        "skills/level2/learnings/00_知识库共享中心索引.txt"
    ]:
        fp = project_root / filepath
        if fp.exists():
            with open(fp, 'r', encoding='utf-8') as f:
                content = f.read(2000)
                nwacs_info += f"\n---\n{filepath}\n---\n{content}\n"

    # 统计文件数量
    py_files = list(project_root.glob("**/*.py"))
    md_files = list(project_root.glob("**/*.md"))

    print(f"📊 NWACS项目统计：")
    print(f"   - Python文件: {len(py_files)}")
    print(f"   - Markdown文档: {len(md_files)}")
    print()

    # 构建DeepSeek查询
    print("🧠 调用DeepSeek进行企业级对比...")
    print()

    system_prompt = """你是一个企业级AI写作工具专家。你需要对比NWACS（Novel Writing AI Collaborative System）与目前业界领先的企业级写作工具（如Jasper、Copy.ai、Writesonic、GrammarlyGO、Notion AI等），分析NWACS的差距，并提出企业级优化建议。

请从以下维度进行分析：
1. 功能完整性对比 - 企业级工具具备但NWACS缺少的功能
2. 性能与可靠性 - 企业级的稳定性要求
3. 用户体验 - 企业级的UI/UX要求
4. 团队协作 - 企业级的多人协作功能
5. 部署与集成 - 企业级的部署方案和API集成
6. 安全与合规 - 企业级的数据安全要求
7. 商业模式与可扩展性 - 从工具到企业服务的转变

请给出详细、专业、可执行的分析报告。"""

    user_prompt = f"""请对比NWACS与企业级写作工具，分析差距并提出优化建议。

---
NWACS项目信息：
- 版本: v7.0
- 架构: v2.2
- 三级Skill: 28个
- 知识库: 32个
- Python文件: {len(py_files)}
- Markdown文档: {len(md_files)}
- 集成: 飞书机器人（可用）、微信机器人（概念验证）
- 学习引擎: DeepSeek联网学习

---
NWACS架构文档：
{nwacs_info}

---
请进行详细对比分析，输出：
1. NWACS的优势
2. 企业级工具具备但NWACS缺少的核心功能
3. 具体的企业级优化建议（分优先级）
4. 分阶段升级路线图
"""

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=3000
        )

        result = response.choices[0].message.content

        print("="*60)
        print("🏢 NWACS企业级对比分析")
        print("="*60)
        print()
        print(result)
        print()

        # 保存报告
        report_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_dir = project_root / "logs" / "enterprise_comparison"
        report_dir.mkdir(parents=True, exist_ok=True)
        report_file = report_dir / f"NWACS企业级分析_{report_time}.md"

        report_content = f"""# NWACS企业级对比分析报告

**分析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**NWACS版本**: v7.0
**架构版本**: v2.2
**分析工具**: DeepSeek

---

## 分析结果

{result}

---

## NWACS项目统计

| 指标 | 数量 |
|------|------|
| Python文件 | {len(py_files)} |
| Markdown文档 | {len(md_files)} |
| 三级Skill | 28个 |
| 知识库 | 32个 |
| 集成模块 | 飞书、微信 |

*分析工具: NWACS企业级对比工具*
"""

        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_content)

        print("="*60)
        print(f"✅ 企业级分析报告已保存到:")
        print(f"   {report_file}")
        print("="*60)

    except Exception as e:
        print(f"❌ 分析失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
