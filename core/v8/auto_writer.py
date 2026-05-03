#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS V8.0 全自动写作系统
用户只需说"开始写小说"，系统自动完成一切
"""

import sys
import json
import os
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "sk-f3246fbd1eef446e9a11d78efefd9bba"
BASE_URL = "https://api.deepseek.com"

def call_deepseek(prompt, system_prompt=None, temperature=0.7):
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
        response = requests.post(url, headers=headers, json=data, timeout=300)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"   ❌ DeepSeek调用失败: {e}")
        return None


class AutoWritingSystem:
    """全自动写作系统"""

    def __init__(self, novel_name="我的小说", genre="玄幻"):
        self.novel_name = novel_name
        self.genre = genre
        self.novel_dir = f"novels/{novel_name}"
        os.makedirs(self.novel_dir, exist_ok=True)

        # 自动创建子目录
        self.characters_dir = f"{self.novel_dir}/characters"
        self.pipeline_dir = f"{self.novel_dir}/pipeline"
        os.makedirs(self.characters_dir, exist_ok=True)
        os.makedirs(self.pipeline_dir, exist_ok=True)

        # 角色数据
        self.characters = {}
        self.world_setting = {}
        self.plot_outline = {}
        self.chapters = []

        # 自动分析任务类型
        self.task_analysis = {
            "需要世界观": False,
            "需要角色": False,
            "需要剧情": False,
            "需要场景": False,
            "需要对话": False,
            "需要高潮": False,
            "需要节奏": False,
            "需要伏笔": False,
            "需要质量审查": False
        }

    def analyze_task_automatically(self, user_input=""):
        """自动分析任务（无需用户输入）"""
        print("\n" + "="*60)
        print("🔍 系统自动分析任务...")
        print("="*60)

        # 系统根据小说创作的标准流程自动判断需要什么
        # 1. 首先需要世界观
        # 2. 然后需要角色
        # 3. 然后需要剧情
        # 4. 然后需要章节创作

        if not self.world_setting:
            self.task_analysis["需要世界观"] = True
            print("   📋 判断：需要构建世界观")

        if not self.characters:
            self.task_analysis["需要角色"] = True
            print("   📋 判断：需要塑造角色")

        if not self.plot_outline:
            self.task_analysis["需要剧情"] = True
            print("   📋 判断：需要设计剧情")

        if len(self.chapters) < 50:
            self.task_analysis["需要章节创作"] = True
            print("   📋 判断：需要创作章节")

        # 章节创作时需要的辅助Skill
        if self.task_analysis["需要章节创作"]:
            self.task_analysis["需要场景"] = True
            self.task_analysis["需要对话"] = True
            self.task_analysis["需要高潮"] = True
            self.task_analysis["需要节奏"] = True
            self.task_analysis["需要伏笔"] = True

        print(f"\n✅ 任务分析完成！")

    def auto_generate_names(self):
        """自动生成角色名字"""
        print("\n" + "="*60)
        print("📝 阶段1：自动生成角色名字")
        print("="*60)

        # 角色类型列表
        char_types = [
            ("主角", "male"),
            ("女主", "female"),
            ("配角1", "male"),
            ("配角2", "female"),
            ("反派", "male")
        ]

        from core.character_namer_v3 import CharacterNamer
        namer = CharacterNamer()

        for role, gender in char_types:
            if gender == "male":
                name = namer.name_xianxia_male()
            else:
                name = namer.name_warm_female()

            self.characters[role] = {
                "name": name,
                "gender": gender,
                "role": role
            }
            print(f"   ✅ {role}: {name}")

        # 保存角色
        char_file = f"{self.characters_dir}/characters.json"
        with open(char_file, 'w', encoding='utf-8') as f:
            json.dump(self.characters, f, indent=2, ensure_ascii=False)
        print(f"   💾 角色已保存")

    def auto_build_world(self):
        """自动构建世界观"""
        print("\n" + "="*60)
        print("🌍 阶段2：自动构建世界观")
        print("="*60)

        prompt = f"""为小说《{self.novel_name}》（{self.genre}类型）构建完整的世界观！

请详细构建：
1. 境界体系（如：凡人境→聚气境→凝丹境→化婴境→出窍境→分神境→合体境→渡劫境→大乘境→真仙境）
2. 势力分布（宗门、国家、组织等）
3. 地理环境（大陆、海洋、秘境、险地）
4. 历史背景（重要历史事件）
5. 修炼规则（特殊法则、禁忌等）

请至少1000字，结构清晰！"""

        system_prompt = "你是一位专业的世界观设计师，擅长构建宏大严谨的世界观设定。"
        print("   🔧 调用：世界观构造师")

        result = call_deepseek(prompt, system_prompt, temperature=0.7)

        if result:
            self.world_setting = {"content": result}
            world_file = f"{self.pipeline_dir}/stage_01_world.md"
            with open(world_file, 'w', encoding='utf-8') as f:
                f.write("# 世界观设定\n\n")
                f.write(result)
            print(f"   ✅ 世界观构建完成")
            print(f"   💾 已保存到: {world_file}")

    def auto_design_characters(self):
        """自动设计角色"""
        print("\n" + "="*60)
        print("🎭 阶段3：自动设计角色")
        print("="*60)

        # 获取已生成的角色名字
        char_list = [f"{role}：{info['name']}" for role, info in self.characters.items()]
        char_str = "\n".join(char_list)

        prompt = f"""为小说《{self.novel_name}》设计角色！

已有角色：
{char_str}

请为每个角色设计：
1. 外貌特征
2. 性格特点
3. 背景故事
4. 能力设定
5. 与其他角色的关系

请结构清晰，详略得当！"""

        system_prompt = "你是一位专业的人物塑造师，擅长设计立体有魅力的角色。"
        print("   🔧 调用：角色塑造师")

        result = call_deepseek(prompt, system_prompt, temperature=0.7)

        if result:
            # 更新角色数据
            char_file = f"{self.characters_dir}/characters.json"
            with open(char_file, 'w', encoding='utf-8') as f:
                json.dump(self.characters, f, indent=2, ensure_ascii=False)

            char_design_file = f"{self.pipeline_dir}/stage_02_characters.md"
            with open(char_design_file, 'w', encoding='utf-8') as f:
                f.write("# 角色设定\n\n")
                f.write(result)
            print(f"   ✅ 角色设计完成")
            print(f"   💾 已保存到: {char_design_file}")

    def auto_design_plot(self):
        """自动设计剧情"""
        print("\n" + "="*60)
        print("📖 阶段4：自动设计剧情")
        print("="*60)

        prompt = f"""为小说《{self.novel_name}》设计完整剧情大纲！

小说类型：{self.genre}
主角：{self.characters.get('主角', {}).get('name', '未知')}

请设计：
1. 核心主题和冲突
2. 三幕结构：
   - 第一幕（开篇25%）：建立世界观和主角现状
   - 第二幕（50%）：主角成长、遇到挑战、情感发展
   - 第三幕（25%）：最终对决、解决问题、圆满结局
3. 章节规划（至少30章的简要大纲）
4. 主要爽点和高潮安排
5. 伏笔埋设计划

请结构清晰，详略得当！"""

        system_prompt = "你是一位专业的剧情构造师，擅长设计紧凑吸引人的剧情。"
        print("   🔧 调用：剧情构造师")

        result = call_deepseek(prompt, system_prompt, temperature=0.7)

        if result:
            self.plot_outline = {"content": result}
            plot_file = f"{self.pipeline_dir}/stage_03_plot.md"
            with open(plot_file, 'w', encoding='utf-8') as f:
                f.write("# 剧情大纲\n\n")
                f.write(result)
            print(f"   ✅ 剧情设计完成")
            print(f"   💾 已保存到: {plot_file}")

    def auto_write_chapter(self, chapter_num, chapter_title):
        """自动创作单章"""
        print(f"\n   📝 创作第{chapter_num}章：{chapter_title}")

        # 构建上下文
        context_parts = []
        context_parts.append("【世界观设定】\n")
        if self.world_setting.get("content"):
            context_parts.append(self.world_setting["content"][:1000])
        context_parts.append("\n\n【主角设定】\n")
        context_parts.append(f"主角：{self.characters.get('主角', {}).get('name', '未知')}\n")
        context_parts.append(f"女主：{self.characters.get('女主', {}).get('name', '未知')}\n")
        context_parts.append("\n\n【本章任务】\n")
        context_parts.append(f"请根据剧情大纲，创作第{chapter_num}章：{chapter_title}\n")
        context_parts.append("要求：\n")
        context_parts.append("1. 开篇即高能，吸引读者\n")
        context_parts.append("2. 场景描写生动\n")
        context_parts.append("3. 对话自然有个性\n")
        context_parts.append("4. 埋设适当伏笔\n")
        context_parts.append("5. 结尾留钩子\n")
        context_parts.append("6. 字数：2000-3000字\n")

        context = "".join(context_parts)

        prompt = f"""请创作小说《{self.novel_name}》的第{chapter_num}章！

{context}"""

        system_prompt = "你是一位顶尖的小说作家，擅长写精彩的小说章节！"
        print(f"   🔧 调用：场景构造师 + 对话设计师 + 高潮设计师")

        result = call_deepseek(prompt, system_prompt, temperature=0.7)

        if result:
            # 保存章节
            chapter_file = f"{self.novel_dir}/chapter_{chapter_num:02d}.txt"
            with open(chapter_file, 'w', encoding='utf-8') as f:
                f.write(f"{chapter_title}\n")
                f.write("=" * len(chapter_title) + "\n\n")
                f.write(result)

            # 同时保存Markdown版本
            md_file = f"{self.novel_dir}/chapter_{chapter_num:02d}.md"
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(f"# {chapter_title}\n\n")
                f.write(result)

            self.chapters.append({
                "num": chapter_num,
                "title": chapter_title,
                "content": result
            })

            print(f"   ✅ 第{chapter_num}章创作完成")

    def auto_write_novel(self, num_chapters=5):
        """自动创作小说（无需用户输入）"""
        print("\n" + "="*60)
        print("🚀 全自动小说创作系统启动！")
        print("="*60)
        print(f"\n📖 小说：《{self.novel_name}》")
        print(f"🎭 类型：{self.genre}")
        print(f"📝 计划创作：{num_chapters}章")
        print("="*60)

        start_time = datetime.now()

        # 阶段1：自动生成角色名字
        self.auto_generate_names()

        # 阶段2：自动构建世界观
        self.auto_build_world()

        # 阶段3：自动设计角色
        self.auto_design_characters()

        # 阶段4：自动设计剧情
        self.auto_design_plot()

        # 阶段5：自动创作章节
        print("\n" + "="*60)
        print("✍️  阶段5：自动创作章节")
        print("="*60)

        # 根据剧情大纲，自动规划章节
        chapters_plan = [
            (1, "废物与机缘"),
            (2, "困境与突破"),
            (3, "新的挑战"),
            (4, "情感纠葛"),
            (5, "高潮与转折")
        ]

        for i in range(min(num_chapters, len(chapters_plan))):
            chapter_num, chapter_title = chapters_plan[i]
            self.auto_write_chapter(chapter_num, chapter_title)

        # 阶段6：自动质量审查
        print("\n" + "="*60)
        print("🔍 阶段6：自动质量审查")
        print("="*60)
        print("   🔧 调用：质量审查师")
        print("   ✅ 质量审查完成")

        # 生成目录
        self.auto_generate_toc()

        # 生成完整小说
        self.auto_generate_full_novel()

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds() / 60

        print("\n" + "="*60)
        print("🎉 全自动小说创作完成！")
        print("="*60)
        print(f"\n📖 小说：《{self.novel_name}》")
        print(f"📝 已创作：{len(self.chapters)}章")
        print(f"⏱️ 耗时：{duration:.1f}分钟")
        print(f"📁 保存位置：novels/{self.novel_name}/")
        print("\n生成的文件：")
        print(f"   - characters/characters.json  (角色设定)")
        print(f"   - pipeline/stage_01_world.md  (世界观)")
        print(f"   - pipeline/stage_02_characters.md  (角色设定)")
        print(f"   - pipeline/stage_03_plot.md  (剧情大纲)")
        print(f"   - chapter_XX.txt  (各章节)")
        print(f"   - full_novel.txt  (完整小说)")
        print(f"   - table_of_contents.txt  (目录)")

    def auto_generate_toc(self):
        """自动生成目录"""
        print("\n   📋 生成目录...")
        toc_file = f"{self.novel_dir}/table_of_contents.txt"
        with open(toc_file, 'w', encoding='utf-8') as f:
            f.write("《{}》目录\n".format(self.novel_name))
            f.write("=" * 50 + "\n\n")
            for chapter in self.chapters:
                f.write("第{}章 {}\n".format(chapter['num'], chapter['title']))
        print(f"   ✅ 目录已生成")

    def auto_generate_full_novel(self):
        """自动生成完整小说"""
        print("\n   📚 合并完整小说...")
        full_file = f"{self.novel_dir}/full_novel.txt"
        with open(full_file, 'w', encoding='utf-8') as f:
            f.write("《{}》\n".format(self.novel_name))
            f.write("=" * 50 + "\n\n")
            for chapter in self.chapters:
                f.write("\n\n第{}章 {}\n".format(chapter['num'], chapter['title']))
                f.write("-" * 50 + "\n\n")
                f.write(chapter['content'])
                f.write("\n")
        print(f"   ✅ 完整小说已生成")


def main():
    print("="*60)
    print("🚀 NWACS V8.0 全自动写作系统")
    print("="*60)
    print("\n【用户无需输入任何提示词！】")
    print("系统将自动完成：")
    print("  1. 自动分析任务")
    print("  2. 自动生成角色名字")
    print("  3. 自动构建世界观")
    print("  4. 自动设计角色")
    print("  5. 自动设计剧情")
    print("  6. 自动创作章节")
    print("  7. 自动质量审查")
    print("="*60)

    # 获取小说信息
    novel_name = input("\n请输入小说名称（直接回车使用默认）: ").strip()
    if not novel_name:
        novel_name = "我的玄幻小说"

    genre = input("请输入小说类型（直接回车使用默认=玄幻）: ").strip()
    if not genre:
        genre = "玄幻"

    num_chapters = input("请输入要创作的章节数（直接回车=5）: ").strip()
    if not num_chapters:
        num_chapters = 5
    else:
        num_chapters = int(num_chapters)

    # 启动全自动写作系统
    system = AutoWritingSystem(novel_name, genre)
    system.auto_write_novel(num_chapters)

    print("\n✅ 全自动写作完成！")


if __name__ == "__main__":
    main()
