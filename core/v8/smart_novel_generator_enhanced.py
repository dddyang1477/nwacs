#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS V8.x 智能小说生成器（增强版）
整合一体化引擎，写作时自动调用技能支持
"""

import sys
import os
import json
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class SmartNovelGenerator:
    """智能小说生成器 - 写作时自动调用技能支持"""

    def __init__(self):
        self.version = "8.9"
        self.engine = None
        self.session = {
            "current_chapter": 1,
            "total_chapters": 100,
            "novel_name": "天机道主",
            "genre": "玄幻"
        }

        print("="*70)
        print(f"📖 NWACS V{self.version} 智能小说生成器")
        print("="*70)

        self._initialize_engine()

    def _initialize_engine(self):
        """初始化一体化引擎"""
        try:
            from nwacs_unified_engine import NWACSUnifiedEngine
            self.engine = NWACSUnifiedEngine()
            print("\n✅ 一体化引擎加载成功")
        except Exception as e:
            print(f"\n⚠️ 一体化引擎加载失败: {e}")
            print("💡 将使用基础模式")
            self.engine = None

    def generate_chapter_with_skills(self, chapter_num, outline=None):
        """
        生成章节 - 写作时自动调用技能增强

        Args:
            chapter_num: 章节号
            outline: 章节大纲

        Returns:
            生成的章节内容
        """
        print(f"\n{'='*70}")
        print(f"📝 开始创作第 {chapter_num} 章")
        print(f"{'='*70}")

        chapter_content = []

        # Step 1: 分析爆款
        if self.engine:
            print("\n📊 [技能1] 爆款分析 - 参考同类型爆款...")
            self.engine.execute_skill("爆款分析", genre=self.session["genre"])

        # Step 2: 设计悬念
        if self.engine:
            print("\n🔍 [技能2] 悬念设置 - 为章节设置钩子...")
            self.engine.execute_skill("悬念设置", setup=f"第{chapter_num}章开场")

        # Step 3: 设计反转（可选）
        if chapter_num % 5 == 0:
            if self.engine:
                print("\n💥 [技能3] 反转设计 - 这章有重要反转！")
                self.engine.execute_skill("反转设计", setup="看似正常发展")

        # Step 4: 构建场景
        if self.engine:
            print("\n🎨 [技能4] 感官增强 - 增强场景描写...")
            # 生成基础内容
            base_scene = f"第{chapter_num}章，场景开始..."
            self.engine.execute_skill("感官增强", text=base_scene)

        # Step 5: 生成实际内容
        print("\n✍️  开始创作章节内容...")
        chapter_content = self._generate_actual_chapter(chapter_num, outline)

        print(f"\n✅ 第 {chapter_num} 章创作完成！")
        return chapter_content

    def _generate_actual_chapter(self, chapter_num, outline):
        """生成实际的章节内容（简化版）"""

        # 章节模板
        chapter_templates = {
            1: """
第1章 废柴与废物

天元大陆，大炎王朝，林家。

林默睁开眼睛，发现自己躺在冰冷的地上，头痛欲裂。

"我...还活着？"

记忆如潮水般涌来——原主是林家的旁系子弟，天生灵根残缺，无法修炼，被称为林家的废物，昨天因为与人争执，被人失手打死...

突然，脑海中传来一道声音：
【叮！检测到合适宿主，神级选择系统绑定中...】
""",

            31: """
第31章 天衍圣地的阴影

落凤城，叶青云的住处。

"奇怪，最近总感觉有人在监视我..."

叶青云站在窗边，望着远处的天际，眉头微蹙。作为一名天机师，他对因果变化有着超乎常人的直觉——最近几天，他隐约感觉到，有一双眼睛正在注视着他。

"楚凌霄...你果然还是发现了吗？"

叶青云轻语一声，随手拿出一枚古朴的铜钱，开始推演。然而当他的灵力注入铜钱时，铜钱却突然剧烈颤抖起来，然后"啪"地一声碎成了两半。

"什么？！因果线被干扰了？！"
""",

            40: """
第40章 因果的代价

"苏沐雪！"

叶青云目眦欲裂，看着远处被黑衣修士团团围住的少女，心脏像是被一只无形的手攥紧。

"叶青云，出来受死！否则你的小情人就要香消玉殒了！"

楚凌霄的声音从远处传来，带着胜利者的得意。叶青云握紧了拳头，指甲深嵌掌心。他知道，楚凌霄是在用苏沐雪逼他现身。

"天机道主，难道真的只能眼睁睁看着自己在意的人陷入危险吗？"

叶青云闭上眼，深吸一口气。当他再次睁开眼时，眼中已经没有了犹豫——只有坚定的决心。
""",
        }

        # 返回模板内容或生成内容
        if chapter_num in chapter_templates:
            return chapter_templates[chapter_num]

        # 通用内容生成
        return f"""
第{chapter_num}章 未知的章节

[这是第{chapter_num}章的内容]

本章要点：
- 悬念设置完成
- 人物发展推进
- 为后续章节埋下伏笔

（实际使用时会调用DeepSeek API生成完整内容）
"""

    def run_workflow(self, workflow_name="玄幻小说创作"):
        """运行完整的创作工作流"""
        if not self.engine:
            print("⚠️ 一体化引擎未加载，无法运行工作流")
            return

        print(f"\n🚀 启动创作工作流: {workflow_name}")
        result = self.engine.run_workflow(workflow_name, genre=self.session["genre"])

        if result.get('status') == 'success':
            print(f"\n✅ 工作流完成！")
            print(f"⏱️  总耗时: {result.get('total_time')}s")
            print(f"📌 总步骤: {result.get('total_steps')}")

    def interactive_writing_mode(self):
        """交互式写作模式"""
        print(f"\n{'='*70}")
        print("🎮 交互式写作模式")
        print(f"{'='*70}")

        while True:
            print(f"\n当前进度: 第 {self.session['current_chapter']}/{self.session['total_chapters']} 章")
            print(f"\n请选择:")
            print(f"  1. 生成下一章")
            print(f"  2. 查看可用技能")
            print(f"  3. 运行创作工作流")
            print(f"  4. 设置小说信息")
            print(f"  0. 退出")

            choice = input("\n请输入选择 (0-4): ").strip()

            if choice == '1':
                chapter_content = self.generate_chapter_with_skills(
                    self.session['current_chapter']
                )
                print(chapter_content)
                self.session['current_chapter'] += 1

            elif choice == '2':
                if self.engine:
                    print("\n📋 可用技能:")
                    for skill in self.engine.list_skills():
                        print(f"  {skill['icon']} {skill['name']}")

            elif choice == '3':
                if self.engine:
                    print("\n📁 可用工作流:")
                    workflows = self.engine.list_workflows()
                    for i, wf in enumerate(workflows, 1):
                        print(f"  {i}. {wf['name']}")
                    wf_choice = input("\n选择工作流 (1-3): ").strip()
                    if wf_choice in ['1', '2', '3']:
                        self.run_workflow(workflows[int(wf_choice)-1]['name'])

            elif choice == '4':
                self.session['novel_name'] = input("小说名称: ").strip()
                self.session['genre'] = input("小说类型 (玄幻/都市/言情/等): ").strip()
                self.session['total_chapters'] = int(input("总章节数: ").strip() or 100)
                print(f"✅ 已设置: {self.session['novel_name']} ({self.session['genre']})")

            elif choice == '0':
                print("\n👋 再见！")
                break

            else:
                print("⚠️ 无效选择，请重试")


def main():
    """主函数"""
    generator = SmartNovelGenerator()

    # 启动交互式模式
    generator.interactive_writing_mode()


if __name__ == "__main__":
    main()
