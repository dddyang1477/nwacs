#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS写作经典深度学习
对经典写作书籍进行深度剖析学习
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
    print("="*70)
    print("📚 NWACS写作经典深度学习")
    print("="*70)
    print()

    # 设置API Key
    api_key = "sk-f3246fbd1eef446e9a11d78efefd9bba"

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com"
    )

    project_root = Path(__file__).parent

    # 写作经典书籍列表
    classics = [
        # 写作方法论
        "写好前五十页",
        "写作的诞生",
        "故事-罗伯特麦基",
        "故事写作大师班-约翰克卢碧",
        "九宫格写作法",
        "卡片笔记写作法",
        "模板写作法",
        "写出我心-娜塔莉戈德堡",
        "学会写作-粥佐罗",
        "小说的骨架-凯蒂维兰德",
        "小说课-毕飞宇",
        "这样写出好故事-詹姆斯贝尔",
        "小说创造基本技巧",
        "小说写作进阶技巧",
        "小说写作叙事技巧指南",
        "如何写砸一本小说",

        # 文学作品
        "海边的房间",
        "望江南",
        "父亲",
        "红楼梦",
        "金锁记",
        "平凡的世界",
        "青蛇",
        "撒哈拉的故事",
        "长恨歌",
        "在细雨中呼喊",
        "白鹿原",
        "半生缘",
        "呼兰河传",
        "活着",
        "四世同堂",
        "蛙",
        "嫌疑人X的献身",
        "一句顶一万句",
        "浮生六记",
        "雪国",
        "围城",
        "将饮茶",
        "人间草木",
        "人间有至味",
        "文化苦旅",
        "病隙碎笔",
        "世说新语",
        "水问",

        # 非虚构/散文
        "存在主义的咖啡馆",
        "人类群星闪耀时",
        "苏东坡传",
        "陶庵梦忆",
        "万古江河",
        "乡土中国",
        "拥抱逝水年华",
        "雅舍小品",

        # 工具书
        "写作辞林",
        "写作成语词典",
        "文学描写词典",
        "写作借鉴词典",
        "最佳景色描写词典",
        "最佳女性外貌描写词典",
        "最佳外貌描写词典",
        "最佳心理描写词典",
        "最佳男性描写词典",
        "唐代衣食住行研究",
        "如何写砸一本小说",
        "读书词典",

        # 其他
        "边城",
        "武则天",
        "焦虑的人",
        "巨鲸歌唱",
        "张枣的诗",
    ]

    print(f"📚 共收录 {len(classics)} 本经典著作")
    print()

    # DeepSeek分析请求
    system_prompt = """你是一个专业的写作理论专家。你需要对给定的写作经典书籍进行深度剖析，提炼出对小说写作最有价值的技巧和方法。

请从以下维度进行分析：
1. **核心写作理念**: 这本书最核心的写作思想是什么？
2. **具体写作技巧**: 有哪些可以直接应用的写作技巧？
3. **描写方法**: 人物描写、环境描写、心理描写的技巧
4. **情节构建**: 如何构建引人入胜的情节
5. **语言风格**: 这本书/这位作者的语言特点
6. **经典语句**: 摘录最经典的描写片段
7. **实战应用**: 给小说创作者的具体建议

请用简洁、专业的方式输出分析结果，便于整合到写作知识库中。"""

    user_prompt_base = """请深度分析以下这本写作经典，提炼对小说创作最有价值的技巧：

书籍：《{book_name}》

请从以下方面进行分析：
1. 核心写作理念
2. 具体写作技巧（至少5条）
3. 人物描写方法
4. 环境/场景描写方法
5. 心理描写方法
6. 情节构建技巧
7. 语言风格特点
8. 经典语句摘录（2-3句）
9. 对网文创作者的建议（3条）

请用Markdown格式输出。"""

    print("🧠 开始深度学习...")
    print()

    # 创建输出目录
    output_dir = project_root / "skills" / "level2" / "learnings" / "写作经典深度分析"
    output_dir.mkdir(parents=True, exist_ok=True)

    # 学习摘要
    summary = []
    summary_file = output_dir / "00_写作经典学习摘要.md"

    for i, book in enumerate(classics, 1):
        print(f"📖 [{i}/{len(classics)}] 深度分析: {book}")

        try:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt_base.format(book_name=book)}
                ],
                temperature=0.7,
                max_tokens=3000
            )

            result = response.choices[0].message.content

            # 保存到文件
            safe_filename = book.replace("/", "-").replace("\\", "-").replace(":", "-")
            book_file = output_dir / f"{safe_filename}.md"

            with open(book_file, 'w', encoding='utf-8') as f:
                f.write(f"# {book}\n\n")
                f.write(f"**分析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
                f.write("---\n\n")
                f.write(result)

            summary.append({
                "book": book,
                "file": str(book_file.relative_to(project_root))
            })

            print(f"   ✅ 已保存: {book_file.name}")

        except Exception as e:
            print(f"   ⚠️ 分析失败: {e}")
            continue

        # 每本之间稍作延迟
        import time
        time.sleep(0.5)

    # 生成学习摘要
    print()
    print("📝 生成学习摘要...")

    summary_content = f"""# 写作经典深度学习摘要

**学习时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**学习书籍**: {len(classics)} 本
**成功分析**: {len(summary)} 本

---

## 学习书籍列表

"""

    for i, item in enumerate(summary, 1):
        summary_content += f"{i}. {item['book']}\n"

    summary_content += """

---

## 核心学习要点

"""

    # 调用DeepSeek生成总结
    try:
        summary_prompt = f"""请根据以下已分析的写作经典书籍，生成一份综合性的写作技巧总结：

{chr(10).join([s['book'] for s in summary])}

请总结出：
1. 最重要的10个写作技巧
2. 人物描写的核心要点
3. 场景描写的核心要点
4. 情节构建的核心要点
5. 语言风格的核心要点
6. 给初学者的建议（5条）

请用简洁专业的语言输出。"""

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一个专业的写作理论专家。"},
                {"role": "user", "content": summary_prompt}
            ],
            temperature=0.7,
            max_tokens=4000
        )

        summary_content += response.choices[0].message.content

    except Exception as e:
        summary_content += f"\n\n*摘要生成失败: {e}*\n"

    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(summary_content)

    print()
    print("="*70)
    print("✅ 写作经典深度学习完成！")
    print("="*70)
    print()
    print(f"📊 学习统计:")
    print(f"   书籍总数: {len(classics)}")
    print(f"   成功分析: {len(summary)}")
    print(f"   输出目录: {output_dir}")
    print()
    print(f"📄 学习摘要: {summary_file.name}")
    print()
    print("💡 建议:")
    print("   - 查看学习摘要，掌握核心要点")
    print("   - 查看各书籍的详细分析")
    print("   - 将学到的技巧应用到创作中")


if __name__ == "__main__":
    main()
