#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单版NWACS项目评测
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
    print("🧠 NWACS DeepSeek简单评测")
    print("="*60)
    print()

    # 设置API Key
    api_key = "sk-f3246fbd1eef446e9a11d78efefd9bba"

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com"
    )

    project_root = Path(__file__).parent

    # 读取关键文档
    key_files = []

    for filepath in [
        "docs/architecture/01_系统架构框架.md",
        "项目状态报告.md",
        "skills/level2/learnings/00_知识库共享中心索引.txt"
    ]:
        fp = project_root / filepath
        if fp.exists():
            print(f"📖 读取: {filepath}")
            with open(fp, 'r', encoding='utf-8') as f:
                content = f.read(3000)
                key_files.append(f"---\n{filepath}\n---\n{content}\n")

    # 统计文件数量
    py_files = list(project_root.glob("**/*.py"))
    md_files = list(project_root.glob("**/*.md"))
    print()
    print(f"📊 文件统计:")
    print(f"   - Python文件: {len(py_files)}")
    print(f"   - Markdown文档: {len(md_files)}")
    print()

    # 构建评测提示
    print("🧠 调用DeepSeek进行评测...")
    system_prompt = """你是一个专业的AI项目评测专家。你需要对NWACS（Novel Writing AI Collaborative System）项目进行评测。

请从以下方面评价：
1. 功能完整性
2. 架构合理性
3. 文档完整性
4. 优化建议

请给出详细的评测报告。"""

    user_prompt = f"""请评测NWACS项目。

项目信息：
- Python文件: {len(py_files)}
- Markdown文档: {len(md_files)}

关键文档内容：
{''.join(key_files)}

请给出详细的评测报告。"""

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )

        result = response.choices[0].message.content

        print()
        print("="*60)
        print("✅ DeepSeek评测结果")
        print("="*60)
        print()
        print(result)
        print()

        # 保存评测报告
        report_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_dir = project_root / "logs" / "deepseek_evaluation"
        report_dir.mkdir(parents=True, exist_ok=True)
        report_file = report_dir / f"NWACS评测_{report_time}.md"

        report_content = f"""# NWACS DeepSeek评测报告

**评测时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 评测结果

{result}

---

## 项目统计

| 类型 | 数量 |
|------|------|
| Python文件 | {len(py_files)} |
| Markdown文档 | {len(md_files)} |

*评测工具: NWACS简单评测工具*
"""

        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_content)

        print("="*60)
        print(f"✅ 评测报告已保存到:")
        print(f"   {report_file}")
        print("="*60)

    except Exception as e:
        print(f"❌ 评测失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
