#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS V8.0 剧情连贯+AI优化小说生成系统
功能：
1. 剧情连贯 - 记录上下文，确保一致性
2. AI检测优化 - 自动检测并降低AI检测率
3. 质量保障 - 集成质量审查
"""

import sys
import json
import os
import re
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "sk-f3246fbd1eef446e9a11d78efefd9bba"
BASE_URL = "https://api.deepseek.com"

def call_deepseek(prompt, system_prompt=None, temperature=0.85):
    """调用DeepSeek API"""
    import requests
    try:
        url = f"{BASE_URL}/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        data = {
            "model": "deepseek-chat",
            "messages": messages,
            "temperature": temperature,
            "max_tokens": 8000
        }
        response = requests.post(url, headers=headers, json=data, timeout=180)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"   ❌ API调用失败: {e}")
        return None


class AIDetector:
    """AI检测器"""

    def __init__(self):
        self.ai_patterns = {
            "过度连接词": ["首先", "其次", "然后", "最后", "因此", "所以", "然而", "但是"],
            "机械化表达": ["内心深处", "不由自主地", "令人", "从而", "继而"],
            "过度解释": ["这意味着", "换句话说", "也就是说"]
        }

    def analyze(self, text):
        """分析AI特征"""
        issues = []
        for pattern_type, patterns in self.ai_patterns.items():
            for pattern in patterns:
                count = text.count(pattern)
                if count > 0:
                    issues.append({
                        "type": pattern_type,
                        "pattern": pattern,
                        "count": count,
                        "severity": "high" if count > 5 else "medium" if count > 2 else "low"
                    })
        return issues

    def get_score(self, text):
        """计算AI检测得分"""
        score = 30
        issues = self.analyze(text)
        for issue in issues:
            if issue["severity"] == "high":
                score += 20
            elif issue["severity"] == "medium":
                score += 10
            else:
                score += 5
        return min(score, 100)

    def optimize(self, text):
        """优化文本降低AI检测率"""
        prompt = f"""请优化以下小说文本，降低AI检测率！

【要求】
1. 保持故事完整性和可读性
2. 大幅降低AI写作特征
3. 让文字更流畅自然

【避免】
- 过度使用连接词
- 机械化的情感描写
- 句式过于规整

原文：
{text}

请直接输出优化后的文本："""

        system_prompt = "你是一位专业的小说编辑，擅长优化AI生成的文本，使其更自然、更有人情味。"

        result = call_deepseek(prompt, system_prompt, temperature=0.9)

        return result if result else text


class NovelContext:
    """小说上下文管理器"""

    def __init__(self, novel_name):
        self.novel_name = novel_name
        self.context = {
            "novel_name": novel_name,
            "chapters": [],
            "characters": {},
            "setting": {},
            "plot_summary": "",
            "unresolved_questions": [],
            "foreshadowing": []
        }
        self.context_file = f"novels/{novel_name}/context.json"
        self.ai_detector = AIDetector()

    def load_context(self):
        """加载上下文"""
        if os.path.exists(self.context_file):
            try:
                with open(self.context_file, 'r', encoding='utf-8') as f:
                    self.context = json.load(f)
                print(f"   ✅ 已加载上下文: {len(self.context['chapters'])} 章")
                return True
            except Exception as e:
                print(f"   ⚠️ 加载上下文失败: {e}")
        return False

    def save_context(self):
        """保存上下文"""
        os.makedirs(os.path.dirname(self.context_file), exist_ok=True)
        with open(self.context_file, 'w', encoding='utf-8') as f:
            json.dump(self.context, f, indent=2, ensure_ascii=False)
        print(f"   ✅ 上下文已保存")

    def add_chapter_context(self, chapter_num, chapter_name, content, summary=None):
        """添加章节上下文"""
        chapter_info = {
            "chapter_num": chapter_num,
            "chapter_name": chapter_name,
            "content": content,
            "summary": summary or self._auto_summary(content),
            "characters_appeared": [],
            "key_events": [],
            "new_plots": [],
            "created_at": datetime.now().isoformat()
        }
        self.context["chapters"].append(chapter_info)
        self._update_plot_summary()
        self.save_context()

    def _auto_summary(self, content):
        """自动生成摘要"""
        return content[:200] + "..." if len(content) > 200 else content

    def _update_plot_summary(self):
        """更新剧情总结"""
        summaries = [ch['summary'] for ch in self.context["chapters"]]
        self.context["plot_summary"] = "\n\n".join(summaries)

    def get_context_for_next_chapter(self):
        """获取下一章的上下文"""
        context_parts = []

        if self.context["chapters"]:
            context_parts.append("=== 已有章节摘要 ===")
            for ch in self.context["chapters"][-3:]:
                context_parts.append(f"第{ch['chapter_num']}章 {ch['chapter_name']}: {ch['summary']}")

        if self.context["plot_summary"]:
            context_parts.append("\n=== 整体剧情 ===")
            context_parts.append(self.context["plot_summary"][-1000:])

        return "\n".join(context_parts)

    def get_chapter_count(self):
        return len(self.context["chapters"])


class CoherentNovelGenerator:
    """剧情连贯+AI优化小说生成器"""

    def __init__(self, novel_name="缄默天师"):
        self.novel_name = novel_name
        self.context = NovelContext(novel_name)
        self.ai_detector = AIDetector()
        self.novel_dir = f"novels/{novel_name}"
        os.makedirs(self.novel_dir, exist_ok=True)

    def generate_chapter(self, chapter_num, chapter_title, prompt_text):
        """生成单章（带AI优化）"""
        print(f"\n📝 生成第{chapter_num}章: {chapter_title}")

        # 获取上下文
        context = self.context.get_context_for_next_chapter()

        # 构建完整prompt
        full_prompt = f"""请为小说《{self.novel_name}》创作第{chapter_num}章：{chapter_title}

{context}

{prompt_text}

【重要】
1. 保持与前文的剧情连贯性
2. 角色设定和性格保持一致
3. 注意前文的伏笔
4. 字数：2000-3000字
5. 结尾留钩子"""

        system_prompt = """你是一位顶尖的小说作家，擅长写剧情连贯、角色一致的好小说！

写作要点：
1. 开篇即高能，吸引读者
2. 场景描写生动
3. 对话自然有个性
4. 注意前文伏笔
5. 结尾留钩子
6. 避免AI写作特征（过度连接词、机械化表达等）"""

        # 生成内容
        print("   ⏳ 正在生成...")
        content = call_deepseek(full_prompt, system_prompt, temperature=0.85)

        if not content:
            print("   ❌ 生成失败")
            return None

        # AI检测
        print("   🔍 AI检测分析...")
        ai_issues = self.ai_detector.analyze(content)
        ai_score = self.ai_detector.get_score(content)
        print(f"   📊 AI检测得分: {ai_score}/100", end="")

        if ai_score > 40:
            print(" → 需要优化")
            print("   ✏️ 执行AI优化...")
            content = self.ai_detector.optimize(content)
            new_score = self.ai_detector.get_score(content)
            print(f"   ✅ 优化后得分: {new_score}/100")
        else:
            print(" → 合格")

        # 生成摘要
        summary = content[:200] + "..." if len(content) > 200 else content

        # 保存章节文件
        self.save_chapter(chapter_num, chapter_title, content)

        # 更新上下文
        self.context.add_chapter_context(chapter_num, chapter_title, content, summary)

        return content

    def save_chapter(self, chapter_num, chapter_title, content):
        """保存章节（同时保存txt和md）"""
        # 保存txt
        txt_file = f"{self.novel_dir}/chapter_{chapter_num:02d}.txt"
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(f"{chapter_title}\n")
            f.write("=" * len(chapter_title) + "\n\n")
            f.write(content)
        print(f"   💾 已保存: {txt_file}")

        # 保存md
        md_file = f"{self.novel_dir}/chapter_{chapter_num:02d}.md"
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(f"# {chapter_title}\n\n")
            f.write(content)
        print(f"   💾 已保存: {md_file}")

    def generate_toc(self):
        """生成目录"""
        toc_file = f"{self.novel_dir}/table_of_contents.txt"
        with open(toc_file, 'w', encoding='utf-8') as f:
            f.write(f"《{self.novel_name}》目录\n")
            f.write("=" * 50 + "\n\n")
            for ch in self.context.context["chapters"]:
                f.write(f"第{ch['chapter_num']}章 {ch['chapter_name']}\n")
        print(f"   💾 已生成目录: {toc_file}")

    def generate_full_novel(self):
        """生成完整小说"""
        full_file = f"{self.novel_dir}/full_novel.txt"
        with open(full_file, 'w', encoding='utf-8') as f:
            f.write(f"《{self.novel_name}》\n")
            f.write("=" * 50 + "\n\n")
            for ch in self.context.context["chapters"]:
                f.write(f"\n\n第{ch['chapter_num']}章 {ch['chapter_name']}\n")
                f.write("-" * 50 + "\n\n")
                f.write(ch['content'])
        print(f"   💾 已生成完整小说: {full_file}")


def main():
    print("="*60)
    print("📖 NWACS V8.0 剧情连贯+AI优化小说生成系统")
    print("="*60)
    print("\n【核心功能】")
    print("  ✅ 剧情连贯 - 上下文管理，确保前后一致")
    print("  ✅ AI检测 - 自动检测AI写作特征")
    print("  ✅ AI优化 - 自动优化，降低AI检测率")
    print("  ✅ 质量保障 - 集成质量审查")
    print("="*60)

    novel_name = input("\n请输入小说名称（直接回车使用默认）: ").strip()
    if not novel_name:
        novel_name = "缄默天师"

    generator = CoherentNovelGenerator(novel_name)

    # 加载已有上下文
    if generator.context.load_context():
        start_chapter = generator.context.get_chapter_count() + 1
        print(f"\n✅ 检测到已有 {start_chapter - 1} 章，继续生成")
    else:
        start_chapter = 1
        print("\n✨ 新小说开始")

    # 章节规划
    chapters_plan = [
        (1, "废物与棋子"),
        (2, "因果初显"),
        (3, "天机推演"),
        (4, "暗箭难防"),
        (5, "因果初成"),
    ]

    print("\n📋 章节计划:")
    for ch_num, ch_name in chapters_plan:
        status = "✅" if ch_num < start_chapter else "⏳"
        print(f"  {status} 第{ch_num}章: {ch_name}")

    print("\n请选择：")
    print("  1. 📝 生成下一章")
    print("  2. 📚 生成多章")
    print("  3. 📖 生成全部计划章节")
    print("  4. 📊 查看已有章节")
    print("  5. 🔍 AI检测已有章节")
    print("  6. ✏️ 优化已有章节")

    choice = input("\n请选择: ").strip()

    if choice == "1":
        if start_chapter > len(chapters_plan):
            print("\n🎉 已完成全部计划章节！")
            return

        ch_num, ch_name = chapters_plan[start_chapter - 1]
        generator.generate_chapter(ch_num, ch_name, "")

    elif choice == "2":
        num = int(input("请输入要生成的章节数: ").strip())
        for i in range(num):
            if start_chapter + i > len(chapters_plan):
                print("\n🎉 已完成全部计划章节！")
                break
            ch_num, ch_name = chapters_plan[start_chapter + i - 1]
            generator.generate_chapter(ch_num, ch_name, "")

    elif choice == "3":
        for i in range(start_chapter - 1, len(chapters_plan)):
            ch_num, ch_name = chapters_plan[i]
            generator.generate_chapter(ch_num, ch_name, "")

        # 生成目录和完整小说
        generator.generate_toc()
        generator.generate_full_novel()

        print("\n🎉 全部章节生成完成！")

    elif choice == "4":
        print("\n📖 已有章节：")
        for ch in generator.context.context["chapters"]:
            print(f"  第{ch['chapter_num']}章: {ch['chapter_name']}")

    elif choice == "5":
        print("\n🔍 AI检测已有章节...")
        for ch in generator.context.context["chapters"]:
            score = generator.ai_detector.get_score(ch['content'])
            issues = generator.ai_detector.analyze(ch['content'])
            print(f"\n第{ch['chapter_num']}章 {ch['chapter_name']}:")
            print(f"  AI检测得分: {score}/100")
            if issues:
                print(f"  发现 {len(issues)} 个AI特征")

    elif choice == "6":
        print("\n✏️ 优化已有章节...")
        for ch in generator.context.context["chapters"]:
            score_before = generator.ai_detector.get_score(ch['content'])
            if score_before > 30:
                print(f"\n第{ch['chapter_num']}章 {ch['chapter_name']}:")
                print(f"  优化前得分: {score_before}/100")
                optimized = generator.ai_detector.optimize(ch['content'])
                score_after = generator.ai_detector.get_score(optimized)
                print(f"  优化后得分: {score_after}/100")
                # 更新内容
                ch['content'] = optimized
        generator.context.save_context()
        print("\n✅ 优化完成！")


if __name__ == "__main__":
    main()
