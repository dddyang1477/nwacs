#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS FINAL - 最终统一版本
一个版本整合所有功能
"""

import sys
import os
import json
import time
from datetime import datetime

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 显示启动界面
print("="*80)
print("""
███╗   ██╗██╗    ██╗ █████╗  ██████╗ ███████╗
████╗  ██║██║    ██║██╔══██╗██╔════╝ ██╔════╝
██╔██╗ ██║██║ █╗ ██║███████║██║  ███╗█████╗  
██║╚██╗██║██║███╗██║██╔══██║██║   ██║██╔══╝  
██║ ╚████║╚███╔███╔╝██║  ██║╚██████╔╝███████╗
╚═╝  ╚═══╝ ╚══╝╚══╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝
 
         F I N A L   V E R S I O N
    一个版本整合所有功能
""")
print("="*80)

class NWACSFinal:
    """NWACS最终统一版本"""
    
    def __init__(self):
        self.config = {
            "author": "默认作者",
            "default_genre": "xuanhuan",
            "auto_save": True,
            "version": "FINAL"
        }
        
        print(f"\n🚀 NWACS FINAL 最终版启动!")
        print(f"📅 当前时间: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}")
        
        self.show_main_menu()
    
    def show_main_menu(self):
        """显示主菜单"""
        while True:
            print("\n" + "="*80)
            print("🎮 NWACS FINAL - 最终统一版本 - 主菜单")
            print("="*80)
            
            print("\n【🔥 爆款学习】")
            print("  1. 40本真实爆款深度分析")
            print("  2. 40个基于真实爆款的开局模板")
            print("  3. 爆款成功因素与避坑指南")
            print("  4. 爆款开局公式总结")
            
            print("\n【🌟 2026年新趋势】")
            print("  5. 冲突前置vs黄金三章：新网文范式")
            print("  6. 番茄小说顶流题材分析（都市脑洞/恶毒女配）")
            print("  7. 短剧IP改编创作指南（微短篇/视觉化）")
            print("  8. 新网文特质：反套路+人性博弈")
            
            print("\n【📚 创作指南】")
            print("  9. 读者心理学（四类读者分析）")
            print(" 10. 爽点设计（三种核心情绪）")
            print(" 11. 人设反差设计")
            print(" 12. 金句钩子设计")
            print(" 13. 爆款书名公式")
            
            print("\n【📖 示例学习】")
            print(" 14. 玄幻开局示例")
            print(" 15. 都市开局示例")
            print(" 16. 言情开局示例")
            print(" 17. 悬疑开局示例")
            
            print("\n【🛠️ 工具】")
            print(" 18. 快速生成开局")
            print(" 19. 🎬 影视感写作引擎（镜头语言+感官矩阵）")
            print(" 20. 关于与帮助")
            print("\n【🖊️ 品质提升】")
            print(" 21. 🧹 去AI痕迹写作技巧（自然文风+人性化表达）")
            print("  0. 退出")
            
            choice = input(f"\n请输入选项 (0-21): ").strip()
            
            if choice == "0":
                self.quit()
            elif choice == "1":
                self.show_bestseller_analysis()
            elif choice == "2":
                self.show_bestseller_templates()
            elif choice == "3":
                self.show_success_factors()
            elif choice == "4":
                self.show_opening_formulas()
            elif choice == "5":
                self.show_new_paradigm()
            elif choice == "6":
                self.show_tomato_topics()
            elif choice == "7":
                self.show_drama_adaptation()
            elif choice == "8":
                self.show_new_wangwen_traits()
            elif choice == "9":
                self.show_reader_psychology()
            elif choice == "10":
                self.show_shuang_points()
            elif choice == "11":
                self.show_character_contrast()
            elif choice == "12":
                self.show_golden_hooks()
            elif choice == "13":
                self.show_book_titles()
            elif choice == "14":
                self.show_opening_examples("xuanhuan")
            elif choice == "15":
                self.show_opening_examples("dushi")
            elif choice == "16":
                self.show_opening_examples("yanqing")
            elif choice == "17":
                self.show_opening_examples("xuanyi")
            elif choice == "18":
                self.quick_generate()
            elif choice == "19":
                self.show_cinematic_engine()
            elif choice == "20":
                self.show_about()
            elif choice == "21":
                self.show_deai_techniques()
            else:
                print("⚠️ 无效选项，请重新选择")
    
    def show_bestseller_analysis(self):
        """显示爆款深度分析"""
        print("\n" + "="*80)
        print("📚 40本真实爆款深度分析")
        print("="*80)
        
        try:
            from bestseller_deep_analyzer_v16 import BestsellerDeepAnalyzer
            analyzer = BestsellerDeepAnalyzer()
        except Exception as e:
            print("⚠️ 爆款分析模块未加载，显示概要信息")
            self.show_analysis_summary()
            input("\n按回车返回主菜单...")
            return
        
        print("\n请选择类型：")
        print("1. 玄幻/仙侠 TOP10 分析")
        print("2. 都市 TOP10 分析")
        print("3. 悬疑 TOP10 分析")
        print("4. 言情 TOP10 分析")
        print("5. 查看全部")
        print("0. 返回主菜单")
        
        choice = input("\n请输入选项 (0-5): ").strip()
        
        if choice == "0":
            return
        
        genre_map = {
            "1": "xuanhuan",
            "2": "dushi",
            "3": "xuanyi",
            "4": "yanqing"
        }
        
        if choice in genre_map:
            analyzer.show_genre_analysis(genre_map[choice])
        elif choice == "5":
            for genre in ["xuanhuan", "dushi", "xuanyi", "yanqing"]:
                analyzer.show_genre_analysis(genre)
        
        input("\n按回车返回主菜单...")
    
    def show_analysis_summary(self):
        """显示分析概要"""
        print("\n" + "="*60)
        print("📊 爆款分析概要")
        print("="*60)
        
        print("\n【玄幻/仙侠 TOP10】")
        print("  《玄鉴仙族》、《夜无疆》、《没钱修什么仙？》")
        print("  《捞尸人》、《苟在武道世界成圣》")
        print("  重点: 独特世界观、群像塑造、升级体系")
        
        print("\n【都市 TOP10】")
        print("  《我，枪神！》、《1984：从破产川菜馆开始》")
        print("  重点: 身份反差爽点、打脸干脆、专业细节")
        
        print("\n【悬疑 TOP10】")
        print("  《神秘复苏》、《噩梦使徒》、《重生97破悬案》")
        print("  重点: 恐怖氛围、逻辑严谨、伏笔回收")
        
        print("\n【言情 TOP10】")
        print("  《难哄》、《偷偷藏不住》、《缚春情》")
        print("  重点: 情感共鸣、人设鲜明、成长线")
    
    def show_bestseller_templates(self):
        """显示爆款开局模板"""
        print("\n" + "="*80)
        print("📖 40个基于真实爆款的开局模板")
        print("="*80)
        
        try:
            from bestseller_opening_templates_v16 import BestsellerOpeningTemplates
            templates = BestsellerOpeningTemplates()
        except Exception as e:
            print("⚠️ 爆款模板模块未加载，显示概要信息")
            self.show_template_summary()
            input("\n按回车返回主菜单...")
            return
        
        print("\n请选择类型：")
        print("1. 玄幻/仙侠 10个开局模板")
        print("2. 都市 10个开局模板")
        print("3. 悬疑 10个开局模板")
        print("4. 言情 10个开局模板")
        print("5. 查看全部模板列表")
        print("0. 返回主菜单")
        
        choice = input("\n请输入选项 (0-5): ").strip()
        
        if choice == "0":
            return
        
        genre_map = {
            "1": "xuanhuan",
            "2": "dushi",
            "3": "xuanyi",
            "4": "yanqing"
        }
        
        if choice in genre_map:
            templates.show_all_templates(genre_map[choice])
        elif choice == "5":
            self.show_template_list_summary(templates)
        
        input("\n按回车返回主菜单...")
    
    def show_template_summary(self):
        """显示模板概要"""
        print("\n" + "="*60)
        print("📝 爆款模板概要")
        print("="*60)
        
        print("\n【玄幻/仙侠 10个模板】")
        print("  1. 家族流开局（基于《玄鉴仙族》）")
        print("  2. 永夜世界观开局（基于《夜无疆》）")
        print("  3. 反套路修仙开局（基于《没钱修什么仙？》）")
        print("  4. 苟道流开局（基于《苟在武道世界成圣》）")
        print("  5-10. 更多玄幻开局模板...")
        
        print("\n【都市 10个模板】")
        print("  1. 兵王回归开局（基于《我，枪神！》）")
        print("  2. 年代文开局（基于《1984》）")
        print("  3-10. 更多都市开局模板...")
        
        print("\n【悬疑 10个模板】")
        print("  1. 灵异复苏开局（基于《神秘复苏》）")
        print("  2. 捞尸人开局（基于《捞尸人》）")
        print("  3-10. 更多悬疑开局模板...")
        
        print("\n【言情 10个模板】")
        print("  1. 甜宠开局（基于《难哄》）")
        print("  2. 暗恋成真开局（基于《偷偷藏不住》）")
        print("  3-10. 更多言情开局模板...")
    
    def show_template_list_summary(self, templates):
        """显示模板列表"""
        print("\n" + "="*80)
        print("📖 全部模板列表")
        print("="*80)
        
        genre_name_map = {
            "xuanhuan": "玄幻/仙侠",
            "dushi": "都市",
            "xuanyi": "悬疑",
            "yanqing": "言情"
        }
        
        for genre in ["xuanhuan", "dushi", "xuanyi", "yanqing"]:
            if genre in templates.templates:
                print(f"\n{genre_name_map[genre]} 10个模板：")
                for i, t in enumerate(templates.templates[genre]):
                    print(f"  {i+1}. {t['name']} (基于: {t.get('based_on', '爆款')})")
    
    def show_success_factors(self):
        """显示成功因素与避坑指南"""
        print("\n" + "="*80)
        print("🎯 各类型爆款成功因素与避坑指南")
        print("="*80)
        
        print("\n" + "="*60)
        print("玄幻/仙侠 TOP成功因素:")
        print("- 独特世界观")
        print("- 群像塑造")
        print("- 升级体系严谨")
        print("- 伏笔回收")
        print("\n避坑:")
        print("- 不要写无脑爽文")
        print("- 不要套路堆砌")
        print("- 不要人物扁平")
        
        print("\n" + "="*60)
        print("都市 TOP成功因素:")
        print("- 身份反差爽点")
        print("- 打脸干脆")
        print("- 专业细节真实")
        print("\n避坑:")
        print("- 不要让主角憋屈太久")
        print("- 不要打脸不够爽")
        print("- 不要脱离现实")
        
        print("\n" + "="*60)
        print("悬疑 TOP成功因素:")
        print("- 恐怖氛围营造")
        print("- 逻辑严谨")
        print("- 伏笔回收")
        print("\n避坑:")
        print("- 不要有逻辑漏洞")
        print("- 不要虎头蛇尾")
        print("- 不要恐怖氛围断裂")
        
        print("\n" + "="*60)
        print("言情 TOP成功因素:")
        print("- 情感共鸣强")
        print("- 人设鲜明")
        print("- 成长线完整")
        print("\n避坑:")
        print("- 不要写无脑虐")
        print("- 不要女主太软弱")
        print("- 不要误会太多")
        
        input("\n按回车返回主菜单...")
    
    def show_opening_formulas(self):
        """显示爆款开局公式总结"""
        print("\n" + "="*80)
        print("📝 爆款开局公式总结")
        print("="*80)
        
        print("\n" + "="*60)
        print("玄幻开局公式:")
        print("  公式: 困境开局 + 群像展示 + 世界观暗示")
        print("  关键要素: 主角身份、世界规则、核心矛盾、金手指暗示")
        
        print("\n" + "="*60)
        print("都市开局公式:")
        print("  公式: 身份落差 + 战力/能力展示 + 都市融入")
        print("  关键要素: 主角身份、核心能力、社会背景、第一个冲突")
        
        print("\n" + "="*60)
        print("悬疑开局公式:")
        print("  公式: 诡异开局 + 规则展示 + 超自然力量")
        print("  关键要素: 诡异事件、规则/设定、主角能力、恐怖氛围")
        
        print("\n" + "="*60)
        print("言情开局公式:")
        print("  公式: 重逢/偶遇 + 情感张力 + 甜蜜/虐心")
        print("  关键要素: 主角人设、情感关系、核心矛盾、甜蜜/虐心基调")
        
        print("\n" + "="*60)
        print("人物公式:")
        print("\n玄幻主角类型:")
        print("  - 废柴逆袭型、家族领袖型、重生复仇型")
        print("玄幻金手指:")
        print("  - 系统、传承、重生记忆、特殊体质")
        print("\n都市主角类型:")
        print("  - 兵王回归型、隐藏大佬型、创业逆袭型")
        print("都市金手指:")
        print("  - 前世记忆、特殊能力、商业天赋、系统")
        print("\n悬疑主角类型:")
        print("  - 侦探/警察型、普通人觉醒型、驭鬼者型")
        print("悬疑金手指:")
        print("  - 特殊能力、前世记忆、规则理解、推理能力")
        print("\n言情主角类型:")
        print("  - 独立女主型、甜软女主型、重生复仇型")
        print("言情金手指:")
        print("  - 重生记忆、美食/专业技能、身份隐藏、系统/空间")
        
        input("\n按回车返回主菜单...")
    
    def show_reader_psychology(self):
        """显示读者心理学"""
        try:
            from net_novel_core_guide_v15 import NetNovelCoreGuide
            guides = NetNovelCoreGuide()
            guides.show_reader_psychology()
        except Exception as e:
            print("\n⚠️ 读者心理学模块未加载")
        
        input("\n按回车返回主菜单...")
    
    def show_golden_chapters(self):
        """显示黄金三章"""
        try:
            from net_novel_core_guide_v15 import NetNovelCoreGuide
            guides = NetNovelCoreGuide()
            guides.show_golden_chapters()
        except Exception as e:
            print("\n⚠️ 黄金三章模块未加载")
        
        input("\n按回车返回主菜单...")
    
    def show_shuang_points(self):
        """显示爽点设计"""
        try:
            from net_novel_core_guide_v15 import NetNovelCoreGuide
            guides = NetNovelCoreGuide()
            guides.show_shuang_points()
        except Exception as e:
            print("\n⚠️ 爽点设计模块未加载")
        
        input("\n按回车返回主菜单...")
    
    def show_character_contrast(self):
        """显示人设反差"""
        try:
            from net_novel_core_guide_v15 import NetNovelCoreGuide
            guides = NetNovelCoreGuide()
            guides.show_character_contrast()
        except Exception as e:
            print("\n⚠️ 人设反差模块未加载")
        
        input("\n按回车返回主菜单...")
    
    def show_golden_hooks(self):
        """显示金句钩子"""
        try:
            from net_novel_core_guide_v15 import NetNovelCoreGuide
            guides = NetNovelCoreGuide()
            guides.show_golden_hooks()
        except Exception as e:
            print("\n⚠️ 金句钩子模块未加载")
        
        input("\n按回车返回主菜单...")
    
    def show_book_titles(self):
        """显示爆款书名公式"""
        try:
            from net_novel_core_guide_v15 import NetNovelCoreGuide
            guides = NetNovelCoreGuide()
            guides.show_book_titles()
        except Exception as e:
            print("\n⚠️ 爆款书名公式模块未加载")
        
        input("\n按回车返回主菜单...")
    
    def show_opening_examples(self, genre):
        """显示开局示例"""
        try:
            from opening_examples_library_v15 import OpeningExamplesLibrary
            examples = OpeningExamplesLibrary()
            examples.show_opening(genre)
        except Exception as e:
            print("\n⚠️ 开局示例库模块未加载")
        
        input("\n按回车返回主菜单...")
    
    def quick_generate(self):
        """快速生成开局 - 自动保存功能"""
        print("\n" + "="*80)
        print("🚀 快速生成开局 - 自动保存功能")
        print("="*80)
        
        # 1. 让用户输入小说名
        print("\n请输入小说名称：")
        novel_name = input("小说名: ").strip()
        
        if not novel_name:
            print("\n⚠️ 小说名不能为空！")
            input("按回车返回...")
            return
        
        # 2. 让用户选择类型
        print("\n请选择小说类型：")
        print("1. 玄幻/仙侠")
        print("2. 都市")
        print("3. 悬疑")
        print("4. 言情")
        print("0. 返回")
        
        choice = input("\n请输入选项 (0-4): ").strip()
        
        if choice == "0":
            return
        
        genre_map = {
            "1": "xuanhuan",
            "2": "dushi",
            "3": "xuanyi",
            "4": "yanqing"
        }
        
        genre_name_map = {
            "xuanhuan": "玄幻/仙侠",
            "dushi": "都市",
            "xuanyi": "悬疑",
            "yanqing": "言情"
        }
        
        if choice not in genre_map:
            print("\n⚠️ 无效选项！")
            input("按回车返回...")
            return
        
        genre = genre_map[choice]
        
        # 3. 选择模板
        try:
            from bestseller_opening_templates_v16 import BestsellerOpeningTemplates
            templates = BestsellerOpeningTemplates()
        except Exception as e:
            print(f"⚠️ 模板模块加载失败: {e}")
            input("按回车返回...")
            return
        
        if genre not in templates.templates:
            print("\n⚠️ 没有找到该类型模板！")
            input("按回车返回...")
            return
        
        print(f"\n【{genre_name_map[genre]} 10个模板】")
        for i, t in enumerate(templates.templates[genre]):
            print(f"  {i+1}. {t['name']} (基于: {t.get('based_on', '爆款')})")
        
        print("\n请选择模板编号 (1-10)：")
        template_choice = input("模板编号: ").strip()
        
        if not template_choice.isdigit():
            print("\n⚠️ 请输入有效数字！")
            input("按回车返回...")
            return
        
        template_idx = int(template_choice) - 1
        
        if template_idx < 0 or template_idx >= len(templates.templates[genre]):
            print("\n⚠️ 模板编号无效！")
            input("按回车返回...")
            return
        
        selected_template = templates.templates[genre][template_idx]
        
        # 4. 创建文件夹并保存
        self.save_novel_to_folder(novel_name, selected_template, genre_name_map[genre])
    
    def save_novel_to_folder(self, novel_name, template, genre_name):
        """保存小说到文件夹 - 每部小说独立文件夹，每批章节独立txt文件"""
        import os
        from datetime import datetime
        
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        clean_name = "".join(c for c in novel_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        novel_folder = os.path.join(base_path, clean_name)
        
        if os.path.exists(novel_folder):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            novel_folder = os.path.join(base_path, f"{clean_name}_{timestamp}")
        
        os.makedirs(novel_folder)
        
        print(f"\n✅ 已创建小说文件夹: {novel_folder}")
        
        original_opening = template['example_opening']

        print("\n" + "=" * 60)
        print("[三级Skill智能编排] 一级检测 → 按需二级润色 → 按需三级兜底")
        print("=" * 60)

        try:
            from three_time_quality_check import call_three_time_quality_check
            processed_opening, quality_passed, quality_report = call_three_time_quality_check(
                original_opening,
                chapter_num=1,
                novel_title=novel_name,
                output_dir=novel_folder
            )

            if quality_passed:
                print("\n[OK] 质量检验全部通过")
            else:
                print("\n[WARN] 部分检验未通过，建议人工复核")

        except Exception as e:
            print(f"[WARN] 三级编排异常: {e}")
            print("  回退到基础质量检测...")
            processed_opening = original_opening
            try:
                from quality_check_and_save_v2 import QualityChecker
                checker = QualityChecker(processed_opening, 1)
                passed, report = checker.run_all_checks()
                if not passed:
                    print("[WARN] 基础检测建议人工复核")
            except Exception as e2:
                print(f"[WARN] 基础检测跳过: {e2}")
        # 4. 保存小说信息文件
        info_file = os.path.join(novel_folder, "小说信息.md")
        with open(info_file, "w", encoding="utf-8") as f:
            f.write(f"# {novel_name}\n\n")
            f.write(f"**类型**: {genre_name}\n")
            f.write(f"**模板**: {template['name']}\n")
            f.write(f"**基于**: {template.get('based_on', '爆款')}\n")
            f.write(f"**创建时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**AI处理**: 已通过AI检测与去痕处理\n\n")
            f.write(f"## 爆款公式\n{template['formula']}\n\n")
            f.write(f"## 核心要素\n")
            for elem in template['core_elements']:
                f.write(f"- {elem}\n")
        
        print(f"✅ 已保存小说信息: {info_file}")
        
        # 5. 保存开局文件（规范命名：小说名_第X-Y章.txt）
        opening_file = os.path.join(novel_folder, f"{clean_name}_第1章.txt")
        with open(opening_file, "w", encoding="utf-8") as f:
            f.write(f"# {novel_name} - 第一章\n\n")
            f.write(f"## 版本说明\n")
            f.write(f"- 此版本经过AI去痕处理，降低AI特征\n\n")
            f.write(f"## 模板结构\n")
            for chap in template.get('structure', []):
                f.write(f"第{chap['chapter']}章: {chap['title']}\n")
                f.write(f"  {chap['content']}\n\n")
            f.write(f"\n## 正文\n")
            f.write(processed_opening)
        
        print(f"✅ 已保存开局: {opening_file}")
        
        # 6. 保存大纲模板文件
        outline_file = os.path.join(novel_folder, "小说大纲.md")
        with open(outline_file, "w", encoding="utf-8") as f:
            f.write(f"# {novel_name} - 小说大纲\n\n")
            f.write(f"## 基本信息\n")
            f.write(f"- 作品名: {novel_name}\n")
            f.write(f"- 作品类型: {genre_name}\n")
            f.write(f"- 预计字数: (建议3-5万字短剧版 / 30-100万字长篇)\n")
            f.write(f"- 核心卖点: (一句话概括)\n\n")
            f.write(f"## AI去痕提示\n")
            f.write(f"- 已自动处理，但建议后续人工润色\n")
            f.write(f"- 可在基础上调整句式，增加个人风格\n")
            f.write(f"- 参考原始版进行对比，找到最佳平衡点\n\n")
            f.write(f"## 主角设定\n")
            f.write(f"- 主角名: (填写)\n")
            f.write(f"- 主角身份: (填写)\n")
            f.write(f"- 金手指: (填写)\n")
            f.write(f"- 核心目标: (填写)\n\n")
            f.write(f"## 开篇设定\n")
            f.write(f"- 开篇场景: (填写)\n")
            f.write(f"- 第一个冲突: (填写)\n")
            f.write(f"- 主角困境: (填写)\n\n")
            f.write(f"## 章节大纲\n")
            f.write(f"第1章: (填写)\n")
            f.write(f"第2章: (填写)\n")
            f.write(f"第3章: (填写)\n")
        
        print(f"✅ 已保存大纲模板: {outline_file}")
        
        # 7. 保存AI去痕指南
        guide_file = os.path.join(novel_folder, "AI去痕与优化指南.md")
        with open(guide_file, "w", encoding="utf-8") as f:
            f.write(f"# {novel_name} - AI去痕与优化指南\n\n")
            f.write(f"## 检测结果\n")
            f.write(f"- 已进行AI特征检测与初步去痕\n\n")
            f.write(f"## 进一步人工优化建议\n\n")
            f.write(f"### 1. 词句方面\n")
            f.write(f"- 减少成语/排比过度使用\n")
            f.write(f"- 增加口语化表达，增强真实感\n")
            f.write(f"- 适当使用语气词（嗯、哦、呢）\n\n")
            f.write(f"### 2. 结构方面\n")
            f.write(f"- 避免完美的段落长度整齐\n")
            f.write(f"- 偶尔有小的逻辑跳跃或不完整表达\n")
            f.write(f"- 增加一些'题外话'或细节描写\n\n")
            f.write(f"### 3. 内容方面\n")
            f.write(f"- 加入个人化的设定与观察\n")
            f.write(f"- 增加一些'无关紧要'的细节描写\n")
            f.write(f"- 对话更自然，不要太书面化\n\n")
            f.write(f"### 4. 错误与瑕疵\n")
            f.write(f"- 适当保留一些无伤大雅的小错误或不完美\n")
            f.write(f"- 不要修改得过于完美\n")
            f.write(f"- 保留一些个人风格的痕迹\n\n")
        
        print(f"✅ 已保存去痕指南: {guide_file}")
        
        print("\n" + "="*60)
        print(f"🎉 小说《{novel_name}》创建成功！")
        print("="*60)
        print(f"\n📁 小说文件夹: {novel_folder}")
        print("\n📝 文件命名规范: [小说名]_第X-Y章.txt")
        print("\n已创建文件:")
        print(f"  1. {clean_name}_第1章.txt - 开局章节")
        print("  2. 小说信息.md - 模板信息与核心要素")
        print("  3. 小说大纲.md - 可编辑的大纲模板")
        print("  4. AI去痕与优化指南.md - 后续人工优化建议")
        print("\n💡 后续章节命名示例:")
        print(f"  {clean_name}_第2-6章.txt")
        print(f"  {clean_name}_第7-11章.txt")
        print(f"  ...以此类推")
        
        input("\n按回车返回主菜单...")

    def save_chapter_batch(self, novel_name, start_chapter, end_chapter, content):
        """保存章节批次 - 规范命名：[小说名]_第X-Y章.txt"""
        import os
        
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        clean_name = "".join(c for c in novel_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        novel_folder = os.path.join(base_path, clean_name)
        
        if not os.path.exists(novel_folder):
            os.makedirs(novel_folder)
            print(f"✅ 已创建小说文件夹: {novel_folder}")
        
        filename = f"{clean_name}_第{start_chapter}-{end_chapter}章.txt"
        filepath = os.path.join(novel_folder, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        
        print(f"✅ 已保存: {filepath}")
        return filepath

    def show_cinematic_engine(self):
        """影视感写作引擎"""
        print("\n" + "=" * 80)
        print("🎬 影视感写作引擎 - 用镜头语言写小说")
        print("=" * 80)

        try:
            from cinematic_writing_engine import (
                CinematicWritingEngine, get_cinematic_engine,
                analyze_text_cinematic, enhance_text_cinematic,
            )
            engine = get_cinematic_engine()
        except ImportError as e:
            print(f"❌ 影视感引擎加载失败: {e}")
            input("\n按回车返回主菜单...")
            return

        while True:
            print("\n" + "=" * 60)
            print("🎬 影视感写作引擎")
            print("=" * 60)
            print("\n  1. 📋 查看全部影视感技法")
            print("  2. 🔍 分析文本影视感程度")
            print("  3. ✨ 增强文本影视感（AI改写）")
            print("  4. 📖 生成影视感章节")
            print("  5. 🌐 联网学习真实写作技巧")
            print("  6. 📝 查看技法速查表")
            print("  0. 返回主菜单")

            choice = input("\n请选择 (0-6): ").strip()

            if choice == "0":
                break
            elif choice == "1":
                self._show_all_techniques(engine)
            elif choice == "2":
                self._analyze_text_cinematic(engine)
            elif choice == "3":
                self._enhance_text_cinematic(engine)
            elif choice == "4":
                self._generate_cinematic_chapter(engine)
            elif choice == "5":
                self._web_learn(engine)
            elif choice == "6":
                print(engine.get_technique_cheatsheet())
                input("\n按回车继续...")
            else:
                print("⚠️ 无效选项")

    def _show_all_techniques(self, engine):
        """展示全部技法"""
        print("\n" + "=" * 60)
        print("📋 影视感写作技法大全")
        print("=" * 60)

        for category in engine.get_categories():
            techniques = engine.get_techniques_by_category(category)
            print(f"\n{'='*50}")
            print(f"【{category}】({len(techniques)}个技法)")
            print(f"{'='*50}")

            for i, t in enumerate(techniques, 1):
                print(f"\n  {i}. {t.name} [{t.difficulty}]")
                print(f"     {t.description}")
                print(f"     ❌ 改写前: {t.example_before[:60]}...")
                print(f"     ✅ 改写后: {t.example_after[:80]}...")
                print(f"     适用: {', '.join(t.applicable_scenes[:3])}")

        input("\n按回车返回...")

    def _analyze_text_cinematic(self, engine):
        """分析文本影视感"""
        print("\n" + "=" * 60)
        print("🔍 文本影视感分析")
        print("=" * 60)
        print("\n请输入要分析的文本（输入END结束）:")
        lines = []
        while True:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)
        text = "\n".join(lines)

        if not text.strip():
            print("⚠️ 文本为空")
            return

        analysis = engine.analyze_scene(text)
        print(f"\n{'='*50}")
        print(f"📊 分析结果")
        print(f"{'='*50}")
        print(f"  影视感评分: {analysis.cinematic_score}/100")
        print(f"  镜头类型: {', '.join(analysis.shot_types_used) if analysis.shot_types_used else '无'}")
        print(f"  感官类型: {', '.join(analysis.sense_types_used) if analysis.sense_types_used else '无'}")
        print(f"  节奏: {analysis.pace}")
        if analysis.highlight_lines:
            print(f"\n  ✨ 亮点句子:")
            for hl in analysis.highlight_lines:
                print(f"    > {hl}")
        if analysis.suggestions:
            print(f"\n  💡 改进建议:")
            for s in analysis.suggestions:
                print(f"    - {s}")

        input("\n按回车返回...")

    def _enhance_text_cinematic(self, engine):
        """AI增强影视感"""
        print("\n" + "=" * 60)
        print("✨ AI影视感增强")
        print("=" * 60)
        print("\n请输入要增强的文本（输入END结束）:")
        lines = []
        while True:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)
        text = "\n".join(lines)

        if not text.strip():
            print("⚠️ 文本为空")
            return

        genre = input("\n小说类型 (玄幻/都市/言情/悬疑, 默认玄幻): ").strip() or "玄幻"

        print("\n🔄 正在调用AI增强影视感...")
        enhanced = engine.enhance_cinematic_quality(text, genre)

        print(f"\n{'='*50}")
        print(f"✅ 增强完成")
        print(f"{'='*50}")
        print(f"\n原文 ({len(text)}字):")
        print(text[:300] + ("..." if len(text) > 300 else ""))
        print(f"\n增强版 ({len(enhanced)}字):")
        print(enhanced[:500] + ("..." if len(enhanced) > 500 else ""))

        save = input("\n是否保存增强版? (y/n): ").strip().lower()
        if save == "y":
            filename = input("文件名 (默认: enhanced_cinematic.txt): ").strip() or "enhanced_cinematic.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(enhanced)
            print(f"✅ 已保存: {filename}")

        input("\n按回车返回...")

    def _generate_cinematic_chapter(self, engine):
        """生成影视感章节"""
        print("\n" + "=" * 60)
        print("📖 生成影视感章节")
        print("=" * 60)

        try:
            chapter_num = int(input("章节号: ").strip())
        except ValueError:
            print("⚠️ 无效章节号")
            return

        title = input("章节标题: ").strip()
        summary = input("章节概要: ").strip()
        genre = input("小说类型 (默认玄幻): ").strip() or "玄幻"

        print("关键情节点 (每行一个，输入END结束):")
        key_points = []
        while True:
            line = input()
            if line.strip().upper() == "END":
                break
            if line.strip():
                key_points.append(line.strip())

        try:
            target_words = int(input("目标字数 (默认4000): ").strip() or "4000")
        except ValueError:
            target_words = 4000

        print(f"\n🔄 正在生成第{chapter_num}章《{title}》(影视感)...")
        content = engine.generate_cinematic_chapter(
            chapter_num, title, summary, key_points, genre, target_words
        )

        if content:
            print(f"\n✅ 生成完成 ({len(content)}字)")
            print(f"\n{'='*50}")
            print(content[:500] + ("..." if len(content) > 500 else ""))

            save = input("\n是否保存? (y/n): ").strip().lower()
            if save == "y":
                filename = input(f"文件名 (默认: 第{chapter_num}章_{title}.txt): ").strip()
                if not filename:
                    filename = f"第{chapter_num}章_{title}.txt"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"✅ 已保存: {filename}")
        else:
            print("❌ 生成失败")

        input("\n按回车返回...")

    def _web_learn(self, engine):
        """联网学习"""
        print("\n" + "=" * 60)
        print("🌐 联网学习真实写作技巧")
        print("=" * 60)
        print("\n正在从以下来源学习...")
        for src in engine.web_learner.LEARNING_SOURCES:
            print(f"  - {src['topic']}")

        force = input("\n是否强制刷新缓存? (y/n, 默认n): ").strip().lower() == "y"

        print("\n🔄 正在联网学习...")
        results = engine.web_learner.learn(force_refresh=force)

        if results:
            for r in results:
                print(f"\n{'='*50}")
                print(f"📚 {r.topic}")
                print(f"   来源: {r.source_url}")
                print(f"   获取时间: {r.fetched_at}")
                print(f"\n   关键技法:")
                for i, tech in enumerate(r.key_techniques[:5], 1):
                    print(f"     {i}. {tech}")
                if r.examples:
                    print(f"\n   示例:")
                    for ex in r.examples[:3]:
                        print(f"     > {ex['text'][:80]}...")
        else:
            print("⚠️ 联网学习未获取到有效内容")

        input("\n按回车返回...")

    def show_deai_techniques(self):
        """去AI痕迹写作技巧 - 让文字更自然、更有人味"""
        while True:
            print("\n" + "=" * 80)
            print("🧹 去AI痕迹写作技巧 — 自然文风 + 人性化表达")
            print("=" * 80)

            print("\n【核心原则】")
            print("  AI文本特征：逻辑太规整、情绪太平、视角太空洞、缺乏现场感")
            print("  目标：让文字像人在说话，有停顿、有节奏、有思考、有瑕疵")

            print("\n" + "-" * 60)
            print("  1. 📝 短句拆分 — 打破AI长句习惯")
            print("  2. 🎭 身份锚定 — 给文字一个\"人设\"")
            print("  3. 🔀 结构多样化 — 拒绝\"总-分-总\"模板")
            print("  4. 🌊 自然过渡 — 用\"思考式衔接\"代替逻辑词")
            print("  5. 🎯 精准术语 — 摆脱\"泛化表达\"")
            print("  6. 🔗 补全推理链 — 结论不能\"直接抛\"")
            print("  7. ⚡ 加入对立观点 — 让表达更像真实思考")
            print("  8. 👁️ 感官锚点 — 引入视听嗅味触")
            print("  9. 💬 对话自然化 — 不完美才是真人")
            print(" 10. 🧩 注入具象细节 — 只有你能写出的内容")
            print(" 11. 🎵 语感节奏 — 长短句穿插")
            print(" 12. 📋 删除模板连接词 — 去掉AI高频词")
            print(" 13. 🎬 风格切换 — 根据场景调整文风")
            print(" 14. 📖 小说专用降AI技巧")
            print(" 15. 🔍 自检清单")
            print("  0. 返回主菜单")

            choice = input("\n请选择查看 (0-15): ").strip()

            if choice == "0":
                break
            elif choice == "1":
                self._deai_short_sentences()
            elif choice == "2":
                self._deai_identity_anchor()
            elif choice == "3":
                self._deai_structure_variety()
            elif choice == "4":
                self._deai_natural_transition()
            elif choice == "5":
                self._deai_precise_terms()
            elif choice == "6":
                self._deai_reasoning_chain()
            elif choice == "7":
                self._deai_opposing_views()
            elif choice == "8":
                self._deai_sensory_anchors()
            elif choice == "9":
                self._deai_natural_dialogue()
            elif choice == "10":
                self._deai_concrete_details()
            elif choice == "11":
                self._deai_rhythm()
            elif choice == "12":
                self._deai_delete_connectors()
            elif choice == "13":
                self._deai_style_switch()
            elif choice == "14":
                self._deai_fiction_specific()
            elif choice == "15":
                self._deai_checklist()
            else:
                print("⚠️ 无效选项")

    def _deai_short_sentences(self):
        """技巧1：短句拆分"""
        print("\n" + "=" * 60)
        print("📝 技巧1：短句拆分 — 把30字长句拆成25字以内的自然表达")
        print("=" * 60)

        print("\n【原理】")
        print("  AI喜欢堆长句，但人类写作更倾向于短句。")
        print("  25字以内的短句阅读流畅度比长句高42%，更贴近口语逻辑。")

        print("\n【对比示例】")
        print("  ❌ AI原句：")
        print("    \"基于对当前行业发展现状的分析以及相关数据的支撑可以得出以下结论。\"")
        print()
        print("  ✅ 人类写法：")
        print("    \"看完行业现状和相关数据，我们大概能得出这样一个结论。\"")

        print("\n【玄幻小说示例】")
        print("  ❌ AI写法：")
        print("    \"林锋运转藏锋诀将自身的灵力波动压制到最低限度然后小心翼翼地沿着矿道的阴影边缘向前移动。\"")
        print()
        print("  ✅ 人类写法：")
        print("    \"林锋运转藏锋诀。灵力波动压到最低。他贴着矿道的阴影边缘，一步一步往前挪。\"")

        print("\n【操作要点】")
        print("  1. 每句控制在25字以内")
        print("  2. 用句号代替逗号，大胆断句")
        print("  3. 一段不超过3-4行")
        print("  4. 动作描写一句一个动作，不要堆叠")

        input("\n按回车返回...")

    def _deai_identity_anchor(self):
        """技巧2：身份锚定"""
        print("\n" + "=" * 60)
        print("🎭 技巧2：身份锚定 — 给文字一个\"人设\"")
        print("=" * 60)

        print("\n【原理】")
        print("  AI的句子让人有种\"谁都能说，但谁也不像谁\"的感觉。")
        print("  因为它没有视角、没有身份、没有个人经验。")
        print("  带有个人视角表达的内容，推荐量比模板式内容高37%。")

        print("\n【对比示例】")
        print("  ❌ AI写法：\"很多人在沟通中会遇到问题。\"")
        print("  ✅ 人类写法：\"我之前在做运营策划时，有一次和产品同事沟通，就遇到过类似状况。\"")

        print("\n【玄幻小说示例】")
        print("  ❌ AI写法：\"修炼一途充满艰险，需要持之以恒。\"")
        print("  ✅ 人类写法：\"林锋在矿道里待了三年。三年，够他把这句话嚼烂了——修炼不是比谁天赋高，是比谁活得久。\"")

        print("\n【操作要点】")
        print("  1. 用角色视角叙述，不要上帝视角")
        print("  2. 加入角色的主观判断和偏见")
        print("  3. 让角色有自己的口头禅和思维习惯")
        print("  4. 不同角色看到同一件事，反应完全不同")

        input("\n按回车返回...")

    def _deai_structure_variety(self):
        """技巧3：结构多样化"""
        print("\n" + "=" * 60)
        print("🔀 技巧3：结构多样化 — 拒绝\"总-分-总\"模板")
        print("=" * 60)

        print("\n【原理】")
        print("  AI的默认逻辑是整齐的\"总—分—总\"，看似规范，读起来却很僵硬。")
        print("  真实的人类写作结构多变，有时先抛结论，有时先讲细节。")

        print("\n【可替换的结构模式】")
        print("  1. \"细节→观点\" 替代 \"观点→细节\"")
        print("  2. \"案例→结论→原理\" 替代 \"原理→分析→结论\"")
        print("  3. \"方法→问题→原因\" 替代 \"问题→原因→方法\"")
        print("  4. 冷启动问题开场 + 举例 + 归因")
        print("  5. 故事 → 误解 → 真相反转式")
        print("  6. 三个场景串联式叙述")

        print("\n【玄幻小说示例】")
        print("  ❌ AI模板结构：")
        print("    背景介绍→主角困境→金手指出现→开始逆袭")
        print()
        print("  ✅ 人类写法结构：")
        print("    冲突画面→倒叙原因→主角抉择→意外转折")

        print("\n【操作要点】")
        print("  1. 每章开头不要用\"话说\"、\"且说\"等套路词")
        print("  2. 偶尔从中间切入，再回溯前因")
        print("  3. 章节结尾不一定是悬念，可以是情绪余韵")
        print("  4. 段落长度刻意不整齐，制造节奏变化")

        input("\n按回车返回...")

    def _deai_natural_transition(self):
        """技巧4：自然过渡"""
        print("\n" + "=" * 60)
        print("🌊 技巧4：自然过渡 — 用\"思考式衔接\"代替模板化逻辑词")
        print("=" * 60)

        print("\n【原理】")
        print("  AI过渡常用\"因此\"\"此外\"\"首先\"\"其次\"，像公式。")
        print("  加入\"思路推进式过渡\"后，文本被判定为人类写作的概率上升58%。")

        print("\n【AI高频连接词 → 替换方案】")
        print("  ❌ \"首先…其次…最后…\" → ✅ 直接列举，不加序号")
        print("  ❌ \"综上所述\" → ✅ \"说到底\"、\"一句话\"")
        print("  ❌ \"因此\"、\"所以\" → ✅ \"这么一来\"、\"结果就是\"")
        print("  ❌ \"此外\"、\"另外\" → ✅ \"还有个事\"、\"对了\"")
        print("  ❌ \"然而\"、\"但是\" → ✅ \"可问题是\"、\"不过\"")

        print("\n【思考式衔接示例】")
        print("  \"说到这，有个细节不得不提……\"")
        print("  \"这里其实还有一个更关键的点……\"")
        print("  \"但回过头来看，就能理解为什么……\"")
        print("  \"扯远了，说回来……\"")

        print("\n【玄幻小说示例】")
        print("  ❌ AI写法：\"此外，林锋还发现矿道深处有异常灵力波动。\"")
        print("  ✅ 人类写法：\"不对。林锋停住脚步。刚才那股灵力波动……不是错觉。\"")

        input("\n按回车返回...")

    def _deai_precise_terms(self):
        """技巧5：精准术语"""
        print("\n" + "=" * 60)
        print("🎯 技巧5：精准术语 — 摆脱\"泛化表达\"")
        print("=" * 60)

        print("\n【原理】")
        print("  AI为了保险，常用非常宽泛的词：\"影响效率\"\"有一定作用\"\"存在一些问题\"。")
        print("  精准的术语和具体的描述能大幅提升专业感和真实感。")

        print("\n【泛化词 → 精准词替换表】")
        print("  ❌ \"很厉害\" → ✅ \"凝气三层巅峰\"、\"剑意入微\"")
        print("  ❌ \"一种丹药\" → ✅ \"三纹聚灵丹\"、\"碧落回春散\"")
        print("  ❌ \"某个地方\" → ✅ \"青云宗外门矿道第三岔口\"")
        print("  ❌ \"过了一段时间\" → ✅ \"三个时辰后\"、\"第七天傍晚\"")
        print("  ❌ \"有人来了\" → ✅ \"脚步声。三个。练气二层以上。\"")

        print("\n【玄幻小说示例】")
        print("  ❌ AI写法：\"他服用了一种提升修为的丹药。\"")
        print("  ✅ 人类写法：\"他吞下那颗三纹聚灵丹。药力化开，丹田里的真气像被点着了一样，烫得他额头冒汗。\"")

        print("\n【操作要点】")
        print("  1. 给物品起具体的名字，不要用\"一种XX\"")
        print("  2. 时间用具体数字，不要用\"不久\"\"一会儿\"")
        print("  3. 地点用具体方位，建立空间感")
        print("  4. 功法、丹药、法宝都要有专属名称")

        input("\n按回车返回...")

    def _deai_reasoning_chain(self):
        """技巧6：补全推理链"""
        print("\n" + "=" * 60)
        print("🔗 技巧6：补全推理链 — 结论不能\"直接抛\"")
        print("=" * 60)

        print("\n【原理】")
        print("  AI喜欢直接说结论，但没有\"为什么\"。")
        print("  真实的人类写作会给出：观察现象 → 数据支撑 → 原因解释。")

        print("\n【三段式论证模板】")
        print("  现象：\"连续三晚睡眠不足6小时……\"")
        print("  原理：\"海马体信息整合能力会下降约30%……\"")
        print("  结论：\"因此熬夜后记忆能力明显减弱，也就不难理解了。\"")

        print("\n【玄幻小说示例】")
        print("  ❌ AI写法：\"林锋决定不暴露实力。\"")
        print()
        print("  ✅ 人类写法：")
        print("    \"林锋攥紧拳头，又松开。王虎身后站着外门执事——凝气五层。自己这点底牌，不够人家一只手捏的。忍。现在不是时候。\"")

        print("\n【操作要点】")
        print("  1. 角色的每个决定都要有内心推理过程")
        print("  2. 不要直接说\"因为他很谨慎\"，要展示谨慎的思考过程")
        print("  3. 重大决策前，让角色权衡利弊")
        print("  4. 偶尔让角色推理错误，增加真实感")

        input("\n按回车返回...")

    def _deai_opposing_views(self):
        """技巧7：加入对立观点"""
        print("\n" + "=" * 60)
        print("⚡ 技巧7：加入对立观点 — 让表达更像真实思考")
        print("=" * 60)

        print("\n【原理】")
        print("  AI习惯\"一刀切式赞美\"或\"单向否定\"。")
        print("  真实的人会犹豫、会矛盾、会自我反驳。")

        print("\n【对比示例】")
        print("  ❌ AI写法：\"这个方案是最优解。\"")
        print("  ✅ 人类写法：\"这个方案看起来不错，但有个问题——成本太高。不过话说回来，短期投入换长期收益，也不是不能考虑。\"")

        print("\n【玄幻小说示例】")
        print("  ❌ AI写法：\"林锋决定冒险进入矿道深处。\"")
        print()
        print("  ✅ 人类写法：")
        print("    \"去，还是不去？林锋在岔道口站了半盏茶的功夫。去了可能死。不去……一辈子待在杂役院，跟死了有什么区别？他咬了咬牙，抬脚迈了进去。\"")

        print("\n【操作要点】")
        print("  1. 让角色内心有矛盾、有挣扎")
        print("  2. 重大选择前展示两难处境")
        print("  3. 不要让角色永远正确，允许他们犯错后悔")
        print("  4. 不同角色对同一件事有不同解读")

        input("\n按回车返回...")

    def _deai_sensory_anchors(self):
        """技巧8：感官锚点"""
        print("\n" + "=" * 60)
        print("👁️ 技巧8：感官锚点 — 引入视觉、听觉、嗅觉、触觉、味觉")
        print("=" * 60)

        print("\n【原理】")
        print("  AI写的场景通常很空泛（比如\"他很生气\"）。")
        print("  人类写作会自然带入感官细节，让画面立起来。")

        print("\n【五感写作对照】")
        print("  ❌ AI写法：\"他很愤怒。\"")
        print("  ✅ 人类写法：\"他攥紧的拳头指节发白，牙关咬得咯吱响，太阳穴上的青筋突突直跳。\"")
        print()
        print("  ❌ AI写法：\"房间里很安静。\"")
        print("  ✅ 人类写法：\"房间里只剩键盘声在响，空气里飘着咖啡的苦味，窗外偶尔传来一声远处的狗叫。\"")

        print("\n【玄幻小说示例】")
        print("  ❌ AI写法：\"矿道深处很危险。\"")
        print()
        print("  ✅ 人类写法：")
        print("    \"矿道深处黑得像墨汁。光明石的光只能照出三步远。空气里一股铁锈味，混着某种腐烂的甜腥。脚下踩到什么黏糊糊的东西——林锋没敢低头看。\"")

        print("\n【五感速查表】")
        print("  视觉：颜色、光影、形状、动态")
        print("  听觉：音量、音色、节奏、远近")
        print("  嗅觉：香/臭/酸/甜/焦/腥/霉")
        print("  触觉：温度/湿度/硬度/粗糙度/痛感")
        print("  味觉：酸甜苦辣咸涩麻")

        input("\n按回车返回...")

    def _deai_natural_dialogue(self):
        """技巧9：对话自然化"""
        print("\n" + "=" * 60)
        print("💬 技巧9：对话自然化 — 不完美才是真人")
        print("=" * 60)

        print("\n【原理】")
        print("  AI写的对话永远逻辑闭环、情绪平稳。")
        print("  可现实里的人说话会有停顿、口误、情绪上头的口不择言。")
        print("  会说半截话，会口是心非，会词不达意。")

        print("\n【对比示例】")
        print("  ❌ AI写法：\"她非常愤怒地对他说：你的行为太过分了，我无法接受。\"")
        print("  ✅ 人类写法：\"她攥着手机的手指都泛白了，张了张嘴，半天只憋出一句：'你是不是有病？'\"")

        print("\n【玄幻小说示例】")
        print("  ❌ AI写法：")
        print("    王虎：\"林锋，你最近的行为很可疑，我怀疑你隐藏了实力。\"")
        print("    林锋：\"王师兄说笑了，我只是一个普通的杂役弟子。\"")
        print()
        print("  ✅ 人类写法：")
        print("    王虎眯着眼：\"林锋，你最近……不太对劲。\"")
        print("    林锋抬起头，一脸茫然：\"啊？王师兄说什么？\"")
        print("    王虎盯着他看了三息。林锋的眼神里只有困惑——恰到好处的困惑。")
        print("    王虎哼了一声，转身走了。")
        print("    林锋低下头，嘴角动了动。没出声。")

        print("\n【操作要点】")
        print("  1. 对话要有潜台词，角色说的和想的不一样")
        print("  2. 加入动作描写打断对话节奏")
        print("  3. 不同身份的人说话方式完全不同")
        print("  4. 偶尔让角色说错话、被误解、欲言又止")
        print("  5. 对话中穿插环境描写，不要让对话\"漂浮\"在空中")

        input("\n按回车返回...")

    def _deai_concrete_details(self):
        """技巧10：注入具象细节"""
        print("\n" + "=" * 60)
        print("🧩 技巧10：注入具象细节 — 只有你能写出的内容")
        print("=" * 60)

        print("\n【原理】")
        print("  AI写内容永远用的是全网通用的素材。")
        print("  没有具体的细节，自然没有灵魂，一眼就是AI拼凑的。")
        print("  加入专属的、有生活感的小细节，是去AI感的核心。")

        print("\n【对比示例】")
        print("  ❌ AI写法：\"她很爱自己的孩子。\"")
        print("  ✅ 人类写法：\"她外套口袋里永远装着孩子的湿巾和哄娃的糖果，手机相册里90%都是孩子的照片，自己的自拍还是半年前拍的。\"")

        print("\n【玄幻小说示例】")
        print("  ❌ AI写法：\"林锋在矿道里修炼了三年。\"")
        print()
        print("  ✅ 人类写法：")
        print("    \"林锋在矿道里待了三年。他的手掌磨出了老茧——不是握剑磨的，是搬矿石搬的。右肩比左肩低半寸，也是常年扛矿篓压的。但他最得意的不是这些。是他能在矿镐砸在石头上的噪音里，分辨出三丈外监工走近的脚步声。\"")

        print("\n【细节注入模板】")
        print("  \"我记得哪年哪月，刚好遇上……\"")
        print("  \"有个细节一直没提……\"")
        print("  \"说个不起眼的事……\"")
        print("  \"他身上有个小习惯……\"")

        input("\n按回车返回...")

    def _deai_rhythm(self):
        """技巧11：语感节奏"""
        print("\n" + "=" * 60)
        print("🎵 技巧11：语感节奏 — 长短句穿插，拒绝整齐划一")
        print("=" * 60)

        print("\n【原理】")
        print("  AI句子句式整齐划一，缺少节奏破碎感。")
        print("  人类写作会自然变换句式：长句铺陈，短句爆发。")

        print("\n【节奏模式示例】")
        print("  长句铺垫 + 短句爆发：")
        print("  \"他在黑暗中摸索了不知道多久，手指划过粗糙的岩壁，脚下踩着不知名的碎骨，耳边只有自己越来越重的呼吸声。\"")
        print("  \"然后他看到了光。\"")
        print()
        print("  三短句连击：")
        print("  \"林锋没动。没出声。甚至没呼吸。\"")

        print("\n【玄幻小说节奏示例】")
        print("  ❌ AI写法（全是中等长度句）：")
        print("  \"林锋运转藏锋诀将灵力波动压制到最低，然后小心翼翼地沿着矿道边缘前进，同时留意着周围的动静和灵力变化。\"")
        print()
        print("  ✅ 人类写法（长短交替）：")
        print("  \"藏锋诀运转。灵力压到最低。林锋贴着矿道边缘，一步一步往前挪。走了大约半个时辰——不对。他停住。前方有光。不是光明石的光。是暗红色的、有节奏的、像心跳一样的光。\"")

        print("\n【操作要点】")
        print("  1. 紧张场景用短句，一句一段")
        print("  2. 抒情场景用长句，娓娓道来")
        print("  3. 关键信息用极短句单独成段")
        print("  4. 偶尔用单字成句：\"死。\" \"跑。\" \"杀。\"")

        input("\n按回车返回...")

    def _deai_delete_connectors(self):
        """技巧12：删除模板连接词"""
        print("\n" + "=" * 60)
        print("📋 技巧12：删除模板连接词 — 去掉AI高频词")
        print("=" * 60)

        print("\n【原理】")
        print("  AI生成内容常有公式感，大量使用万能连接词。")
        print("  这些词是AI检测系统的重要识别特征。")

        print("\n【AI高频词黑名单 — 能删就删】")
        print("  ▸ 综上所述、总而言之、总的说来")
        print("  ▸ 首先…其次…再次…最后")
        print("  ▸ 在当今社会、随着…的发展")
        print("  ▸ 不可否认、毋庸置疑、显而易见")
        print("  ▸ 众所周知、大家知道")
        print("  ▸ 从某种角度来说、在一定程度上")
        print("  ▸ 不仅…而且…、既…又…")
        print("  ▸ 与此同时、另一方面")

        print("\n【玄幻小说AI高频词】")
        print("  ▸ \"只见\"、\"只听得\"、\"忽然间\"")
        print("  ▸ \"心中暗道\"、\"暗想\"、\"不由得\"")
        print("  ▸ \"一股…的气息\"、\"散发出…的波动\"")
        print("  ▸ \"眼中闪过…\"、\"嘴角泛起…\"")
        print("  ▸ \"身形一动\"、\"心念一转\"")

        print("\n【操作要点】")
        print("  1. 写完一章后，搜索这些词，逐个删除或替换")
        print("  2. \"只见\"删掉，直接写看到的画面")
        print("  3. \"心中暗道\"改成直接引语或动作暗示")
        print("  4. 每删一个模板词，文风就自然一分")

        input("\n按回车返回...")

    def _deai_style_switch(self):
        """技巧13：风格切换"""
        print("\n" + "=" * 60)
        print("🎬 技巧13：风格切换 — 根据场景调整文风")
        print("=" * 60)

        print("\n【原理】")
        print("  AI通篇一个语调，但人类写作会根据场景自然切换文风。")
        print("  战斗场景、日常场景、情感场景的文风应该完全不同。")

        print("\n【场景-文风对照表】")
        print("  战斗场景 → 短句、快节奏、动词密集、少修饰")
        print("  日常场景 → 口语化、轻松、可有废话、节奏舒缓")
        print("  情感场景 → 细腻、长句、内心独白、节奏缓慢")
        print("  悬疑场景 → 短句+长句交替、信息克制、氛围渲染")
        print("  装逼打脸 → 节奏明快、对话犀利、爽感直接")

        print("\n【玄幻小说示例】")
        print("  战斗场景：")
        print("    \"剑光。三道。林锋侧身，第一道擦着鼻尖过去。第二道——他抬手，金针撞偏了剑锋。第三道来不及躲。他硬扛。肩头一凉，血飙了出来。\"")

        print("\n  日常场景：")
        print("    \"老周蹲在矿道口啃馒头，看见林锋出来，含糊不清地招呼：'小子，今天挖了多少？'林锋把矿篓往地上一撂，瘫坐下来：'别提了，东边那条道全是硬岩，镐头都崩了两个口子。'\"")

        input("\n按回车返回...")

    def _deai_fiction_specific(self):
        """技巧14：小说专用降AI技巧"""
        print("\n" + "=" * 60)
        print("📖 技巧14：小说专用降AI技巧")
        print("=" * 60)

        print("\n【网文AI检测的特殊难点】")
        print("  1. 篇幅超长 → 全文检测困难，抽检为主 → 需要整体风格一致")
        print("  2. 风格多样 → 不同类型语言差异大 → 需要适配类型特点")
        print("  3. 更新频繁 → 日更压力大 → 需要高效处理流程")
        print("  4. 人物对话多 → 对话是原创性体现 → 对话降重需特别小心")
        print("  5. 情节连贯 → 前后文关联紧密 → 降重需保持连贯性")

        print("\n【核心原则：风格一致性高于一切】")
        print("  网文读者追更的核心动力是对作者风格的认可。")
        print("  降重后如果风格突变，读者会立刻察觉。")

        print("\n【风格一致性的三个维度】")
        print("  1. 叙事节奏 — 长短句搭配、段落长度、场景切换频率")
        print("  2. 语言习惯 — 用词偏好、修辞风格、口头禅")
        print("  3. 情感基调 — 幽默/严肃、轻快/沉重、温馨/虐心")

        print("\n【对比示例：轻松吐槽流】")
        print("  原文风格：")
        print("    \"林夜看着面前这位自称'修仙界第一美男'的家伙，内心毫无波动，甚至想给他一拳。\"")
        print("    \"拜托，你那张脸，说是第一美男，那整个修仙界的审美是不是集体下线了？\"")
        print()
        print("  ❌ AI改写后（风格断裂）：")
        print("    \"林夜注视着眼前这位自诩为修仙界第一美男的修士，心中波澜不惊，甚至产生了攻击冲动。\"")
        print()
        print("  ✅ 正确改写（保持风格）：")
        print("    \"林夜盯着那张自称'第一美男'的脸看了三秒。就这？他默默把拳头攥紧了。\"")

        print("\n【各平台AI检测严格程度】")
        print("  起点中文网 → 算法识别+编辑审核 → 警告/限流/下架/解约 → ★★★★★")
        print("  晋江文学城 → 系统检测+读者举报 → 锁章/扣分/封禁 → ★★★★★")
        print("  番茄小说   → AI识别系统       → 限制推荐/下架     → ★★★")
        print("  七猫小说   → 抽检机制         → 警告/限流         → ★★")
        print("  刺猬猫     → 编辑人工审核     → 拒稿/解约         → ★★★★")

        input("\n按回车返回...")

    def _deai_checklist(self):
        """技巧15：自检清单"""
        print("\n" + "=" * 60)
        print("🔍 技巧15：自检清单 — 一章写完后的10个检查点")
        print("=" * 60)

        print("\n【逐项检查】")
        checks = [
            ("1. 长句检查", "有没有超过30字的句子？拆掉。"),
            ("2. 连接词检查", "有没有\"首先/其次/综上所述/此外\"？删掉。"),
            ("3. 感官检查", "这一章用了几个感官？至少3个（视听嗅触味）。"),
            ("4. 对话检查", "对话像不像真人在说话？有没有潜台词和动作打断？"),
            ("5. 细节检查", "有没有只有你能写出的具象细节？至少1处。"),
            ("6. 节奏检查", "长短句是否交替？有没有单独成段的短句？"),
            ("7. 视角检查", "是否始终在角色视角内？有没有上帝视角跳脱？"),
            ("8. 推理检查", "角色的决定有没有内心推理过程？"),
            ("9. 模板检查", "有没有\"只见/心中暗道/不由得\"等网文AI高频词？"),
            ("10. 风格检查", "这一章的风格和前后章是否一致？"),
        ]

        for title, detail in checks:
            print(f"  ✅ {title}")
            print(f"     {detail}")
            print()

        print("【快速自检命令】")
        print("  写完一章后，用搜索功能查找以下关键词：")
        print("  \"只见\" \"心中\" \"不由得\" \"一股\" \"眼中闪过\" \"嘴角\"")
        print("  \"首先\" \"其次\" \"最后\" \"综上所述\" \"总而言之\"")
        print("  \"不仅…而且\" \"既…又\" \"与此同时\"")
        print()
        print("  每找到一个，就问自己：删掉它，句子会变差吗？")
        print("  如果不会——删。")

        input("\n按回车返回...")

    def show_about(self):
        """显示关于"""
        print("\n" + "="*80)
        print("ℹ️ 关于 NWACS FINAL - 最终统一版本")
        print("="*80)
        
        print("\n📋 版本说明:")
        print("  NWACS FINAL - 最终统一版本")
        print("  一个版本整合所有功能！")
        
        print("\n📦 包含内容:")
        print("  ✅ 40本真实爆款分析")
        print("  ✅ 40个基于真实爆款的开局模板")
        print("  ✅ 16个开局示例")
        print("  ✅ 完整的网文创作指南")
        
        print("\n📊 内容统计:")
        print("  - 真实爆款分析: 40本")
        print("  - 基于真实爆款的开局模板: 40个")
        print("  - 开局示例: 16个")
        
        print("\n📁 数据来源:")
        print("  - 起点中文网 TOP10 排行榜 2026")
        print("  - 番茄小说 TOP10 排行榜 2026")
        print("  - 晋江文学城 TOP10 排行榜 2026")
        
        print("\n💡 使用建议:")
        print("  1. 先看爆款分析，了解市场趋势")
        print("  2. 选择对应类型的爆款模板")
        print("  3. 结合核心写作指南学习")
        print("  4. 参考示例，开始创作")
        
        print("\n🎯 这是最终的统一版本，不再有版本混乱的问题！")
        
        input("\n按回车返回主菜单...")
    
    def show_new_paradigm(self):
        """显示2026年新网文范式：冲突前置vs黄金三章"""
        print("\n" + "="*80)
        print("🌟 2026年新网文范式：冲突前置 vs 黄金三章")
        print("="*80)
        
        print("\n📊 新旧对比：")
        print("\n" + "="*60)
        print("【旧范式：黄金三章】")
        print("  第一章：介绍背景、主角身份")
        print("  第二章：铺垫设定、引出冲突")
        print("  第三章：展示金手指、开始主线")
        print("\n问题：")
        print("  - 读者在第一段就可能划走！")
        print("  - 节奏太慢，不适应短视频时代")
        
        print("\n" + "="*60)
        print("【新范式：冲突前置 + 人设反差 + 金句钩子】")
        print("  ✅ 第一段：直接出事！")
        print("  ✅ 开头500字内：制造强烈人设反差")
        print("  ✅ 每章结尾：金句钩子，让人欲罢不能")
        
        print("\n📝 核心公式：")
        print("   冲突前置 + 人设反差 + 金句钩子 = 留住读者的开头")
        
        print("\n🎯 具体操作方法：")
        print("\n步骤1：砍掉所有背景介绍！")
        print("  - 把\"林晨是个普通大学生\"改为\"林晨被一脚踹翻在地时，嘴里还咬着半块馒头\"")
        
        print("\n步骤2：用动作和对话呈现冲突！")
        print("  - 不要写\"他很生气\"")
        print("  - 要写\"他抓起烟灰缸砸了过去\"")
        print("  - 不要写\"他们吵架了\"")
        print("  - 要写\"'离婚!'妻子把结婚证撕成两半\"")
        
        print("\n步骤3：冲突要具体、可感知！")
        print("  - 错误：他遇到了麻烦")
        print("  - 正确：债主把他堵在巷子里，三把刀抵在腰上")
        
        print("\n📖 爆款案例拆解：")
        print("\n【案例1：《我的室友是重生者》番茄新晋榜第7】")
        print("   开头第一段：")
        print("   \"凌晨两点，宿舍熄灯了。下铺的兄弟突然坐起来，用一种不属于二十岁年轻人的声音说：'三天后，这栋楼会着火，我们都会死。'\"")
        print("\n分析：")
        print("   ✅ 冲突前置：一句话抛出致命危机")
        print("   ✅ 人设反差：普通室友突然变成预言者")
        print("   ✅ 金句钩子：\"我们都会死\"直接引爆悬念")
        print("\n结果：首秀7日追读率达18%，远超番茄12%的及格线")
        
        print("\n【案例2：《保洁阿姨是S级悬赏犯》起点新书榜第12】")
        print("   人设反差公式：")
        print("   - 表面身份：卑微的保洁阿姨（极度普通）")
        print("   - 实际身份：令国际雇佣兵闻风丧胆的顶级罪犯")
        print("   - 反差爆发点：第一章就让反差制造第一个爽点！")
        print("\n结果：上架首日收藏破2万，读者评论高频词是\"这个设定太带感了\"")
        
        print("\n⚠️ 2026年避坑指南：")
        print("   ❌ 不要再用\"我叫XXX\"开头！")
        print("   ❌ 不要铺垫超过300字！")
        print("   ❌ 不要让读者等太久才看到冲突！")
        
        input("\n按回车返回主菜单...")
    
    def show_tomato_topics(self):
        """显示番茄小说顶流题材分析（2026年Q1-Q2）"""
        print("\n" + "="*80)
        print("🍅 番茄小说顶流题材深度分析（2026年Q1-Q2）")
        print("="*80)
        
        print("\n📊 番茄小说核心趋势：")
        print("  - 短篇为王、短剧适配、脑洞破圈、情绪拉满")
        print("  - 推出\"新引力计划\"等十亿级激励")
        print("  - 优先扶持节奏快、冲突强、易改编、情绪稳的作品")
        
        print("\n🔥 男频顶流赛道（必冲！流量天花板）：")
        
        print("\n" + "="*60)
        print("1. 都市脑洞/异能（S级，完读率76%）")
        print("  核心逻辑：现代背景 + 反套路金手指")
        print("  节奏要求：每3章1个小爽点、10章1个大高潮")
        print("  短剧潜力：改编率超60%！")
        print("\n  爆款玩法：")
        print("    - 反套路金手指：摸鱼变强、冷门职业异能（遗物整理师看前世、法医读心）")
        print("    - 跨界融合：灵气复苏+校园/职场、民俗玄学+都市日常")
        print("\n  代表作品：")
        print("    - 《摸鱼就能变强》：月均新增同类305本，留存率89%")
        print("    - 《遗物整理师的阴阳眼》：上线30天在读破50万，抖音解说播放量超2亿")
        print("    - 《我在精神病院学斩神》：都市高武标杆，抖音话题阅读量超8亿，评分9.8")
        
        print("\n" + "="*60)
        print("2. 赘婿逆袭/战神归来（A级，霸榜基本盘）")
        print("  核心逻辑：身份反差 + 强爽点")
        print("  精准群体：30-45岁蓝领/个体户")
        print("\n  爆款玩法：")
        print("    - 战神赘婿：隐退大佬回归，先受辱再打脸，兼顾家庭与事业")
        print("    - 战神归来：退伍军人/隐世高手回乡，解决邻里矛盾、守护家人")
        print("\n  代表作品：")
        print("    - 《战神赘婿》：连续霸榜12周，单书日活超500万，累计在读破2000万")
        print("    - 《我，赘婿，摊牌了》：上线60天全网热度破圈，抖音推书视频播放量超5亿")
        
        print("\n" + "="*60)
        print("3. 都市修真/种田（A级，完读率TOP3）")
        print("  核心逻辑：拒绝传统修仙，走\"都市+修仙/种田\"融合路线")
        print("\n  爆款玩法：")
        print("    - 都市修真：神医下山被师姐团宠、高武都市扮猪吃虎，用医术/武功解决现实问题")
        print("    - 乡村种田：把留守村打造成首富村，结合乡村振兴、邻里矛盾，正能量拉满")
        print("\n  修仙2.0新趋势（热门！）：")
        print("    - 《我在东北种仙参》：修仙者不打架不夺宝，一门心思种人参，催生法术三个月出货")
        print("    - 《修真程序员》：码农得上古传承，把阵法刻进代码里，开发健康管理APP颠覆行业")
        print("    - 《灶王爷在现代》：灶神不开宗立派，从街边烧烤摊做起，三昧真火烤串火遍全国")
        print("\n  新趋势底层原因：")
        print("    - 读者要的不是飘渺天道，是实实在在的财富增长和乡村变迁")
        print("    - 从个人爽走向共同富有升级！")
        
        print("\n💄 女频顶流赛道（稳冲！情绪价值拉满）：")
        
        print("\n" + "="*60)
        print("1. 恶毒女配/全家反派（S级，3月榜单第一！）")
        print("  核心逻辑：穿书+洗白/逆袭，反转剧情吸睛")
        print("  精准群体：18-28岁年轻女性，日新增评论破10万！")
        print("\n  爆款玩法：")
        print("    - 恶女洗白：穿成恶毒女配，不按原剧情走，靠智商/实力逆袭，手撕渣男极品")
        print("    - 全家反派：主角与反派家族结盟，反杀其他豪门，爽感更强烈")
        print("\n  代表作品：")
        print("    - 《穿成恶毒女配后我洗白了》：3月女频榜首，在读超150万")
        
        print("\n" + "="*60)
        print("2. 重生年代文（常青树，新增在读130万+）")
        print("  核心逻辑：含恨重生→手撕渣男→抓时代红利搞钱")
        print("\n  爆款玩法：")
        print("    - 经典细分：囤货军婚、赶山赶海娇妻文、八零当后妈，结合空间/美食元素")
        print("\n  代表作品：")
        print("    - 《重生八零：从小山村走出个大富翁》：年代文爆款，在读超200万")
        
        print("\n" + "="*60)
        print("3. 无CP大女主（2026年新风口！）")
        print("  核心特征：主线清晰（就是升级、变强、征服世界），没有感情戏注水")
        print("  平台数据：免费平台算法核心指标是完读率和互动率，无CP文更容易触发推荐")
        print("\n  爆款案例：")
        print("    - 《游戏入侵》：女主全程搞事业、抢机缘、虐渣复仇，感情线为0，长期霸占巅峰榜")
        print("    - 《听懂动物语言：我成警局常客》：女主靠独一无二专业能力立足，观众追职业成长")
        
        print("\n🌊 全品类蓝海赛道（避卷！完读率高）：")
        
        print("\n" + "="*60)
        print("1. 悬疑脑洞/灵异（增速最快！）")
        print("  核心逻辑：民俗风水+刑侦反转，短篇更易出成绩")
        print("\n  爆款玩法：")
        print("    - 民俗风水：天命神算、狐仙镇百鬼、邪物典当铺")
        print("    - 刑侦反转：交警抢刑侦、碰触尸体锁定凶手")
        print("\n  代表作品：")
        print("    - 《十日终焉》：悬疑无限流天花板，评分9.9，在读超82万，抖音话题播放量破5亿")
        
        print("\n📝 番茄爆款创作指南：")
        print("\n  黄金三章定生死（番茄版）：")
        print("    - 第一章：立人设 + 拉仇恨（主角困境）")
        print("    - 第二章：亮金手指")
        print("    - 第三章：兑现爽点")
        
        print("\n  钩子结尾公式：")
        print("    - 每章结尾 = 悬念 + 情绪")
        
        print("\n  精准用词规则：")
        print("    - 情绪触发词：爽感词（震惊、打脸、逆袭）、压抑词（羞辱、嘲讽、看不起）")
        print("    - 身份反差词：赘婿→战神、废物→大佬、穷小子→首富")
        
        print("\n  避坑红线（2026番茄严打）：")
        print("    ❌ 慢热铺垫：300字内必须出现冲突！")
        print("    ❌ 圣母主角：主角要有底线但不圣母，面对羞辱必须反击！")
        print("    ❌ 反派弱智：反派要有智商和动机！")
        
        input("\n按回车返回主菜单...")
    
    def show_drama_adaptation(self):
        """显示短剧IP改编创作指南（微短篇/视觉化）"""
        print("\n" + "="*80)
        print("🎬 短剧IP改编创作指南：从网文到微短剧的变现密码")
        print("="*80)
        
        print("\n📊 2026年短剧行业现状：")
        print("  - 网文IP改编：微短剧市场主流，番茄6700部作品进入改编链路")
        print("  - 爆款案例：14部改编短剧播放量突破30亿！")
        print("  - 收入模式：版权费 + 后端分成（番茄一般抽10%）")
        
        print("\n🔄 思维转换：从写小说到写短剧的底层变化")
        
        print("\n" + "="*60)
        print("【核心转换公式：压缩+提速+视觉化】")
        print("  - 删除：所有不能产生即时冲突的文字")
        print("  - 转换：把爽点从脑补变为视听刺激")
        
        print("\n  叙事视角转换：")
        print("    - 小说：阅读视角，可以有大段心理独白、环境描写")
        print("    - 短剧：镜头视角，内心戏必须外化！")
        
        print("\n  写作示例对比：")
        print("    ❌ 小说写法：\"她看着手中的支票，心中充满了被羞辱的痛苦，回想起这些年来的委屈……\"")
        print("    ✅ 短剧写法：\"△ 她死死攥着支票，由于用力过猛，指尖发白。猛地抬头，将支票撕成碎片摔在渣男脸上：'拿着你的臭钱，滚！'\"")
        
        print("\n  核心单位转换：")
        print("    - 小说：章 → 情节推动")
        print("    - 短剧：集 → 情绪钩子")
        
        print("\n🎯 什么样的网文适合短剧改编？（筛选阶段）")
        
        print("\n" + "="*60)
        print("【筛选3问】")
        print("\n  1️⃣ 故事核够硬吗？")
        print("     - 好的短剧内核一句话就能概括")
        print("     - 例如：战神回归发现女儿住狗窝、真千金马甲掉落后全球震动")
        
        print("\n  2️⃣ 人设够极致吗？")
        print("     - 主角必须自带\"美强惨\"属性或极致金手指")
        print("     - 性格不能中庸，要有极强的目标感（复仇、夺回遗产、登顶巅峰）")
        
        print("\n  3️⃣ 节奏自带爆点吗？")
        print("     - 评估原著是否具备\"三章一打脸\"的密度")
        
        print("\n📝 短剧创作实操指南：")
        
        print("\n" + "="*60)
        print("【阶段1：提纯】")
        print("  - 毫不留情砍掉：次要感情线、冗余配角、所有慢节奏铺垫")
        
        print("\n" + "="*60)
        print("【阶段2：重构】")
        print("  - 情节节点表格化：建议用Excel，把原著浓缩为20-30个情节节点")
        print("  - 每集公式：第N集 = 解决上一集悬念 + 爆发本集冲突 + 埋下下一集钩子")
        
        print("\n" + "="*60)
        print("【阶段3：黄金结构】")
        print("  - 黄金开篇（1-8集）：生死时速！前10秒必须有核心冲突！")
        print("    - 把主角推向绝境，亮出反击手段（金手指），确立全剧总基调")
        print("  - 中段拉锯（8-20集）：闯关模式！遇险→反击→小胜→更强对手循环")
        print("  - 终极对决（21-30集）：所有前期压抑情绪彻底释放！")
        
        print("\n" + "="*60)
        print("【阶段4：剧本写作】")
        print("  - 开场10秒夺命钩子：")
        print("    - 冲突式：哪怕是扇巴掌，也要扇出清脆感")
        print("    - 悬念式：\"我是谁？我为什么会在反派床上？\"")
        
        print("\n  - 台词情绪化改装：")
        print("    ❌ 错误：\"我觉得我们之间可能存在一些误会，你听我解释\"")
        print("    ✅ 正确：\"住口！你竟然为了他，要我的命？！\"")
        
        print("\n  - 动作描写可视化：")
        print("    ❌ 不要写\"她感到极度愤怒\"")
        print("    ✅ 要写\"她一把掀翻了铺满昂贵瓷器的餐桌\"")
        
        print("\n  - 结尾钩子精密设计：")
        print("    - 这是断章艺术的巅峰！")
        
        print("\n💡 2026年短剧适配创作策略（直接写短剧向网文）：")
        print("  - 字数：3-5万字微短篇！")
        print("  - 节奏：开篇高能，把最炸裂的冲突直接甩在读者脸上！")
        print("  - 写法：视觉化写作，让导演一看就觉得这段不用改直接能拍！")
        
        print("\n📖 爆款短剧改编案例拆解：")
        print("  - 《一品布衣》：历史穿越文提质升级，家国情怀+群像成长，女性用户占比39%，播放破20亿")
        print("  - 《我在冷宫忙种田》：甜宠IP轻量化，种田技巧作为钩子，每集解锁新技能")
        
        input("\n按回车返回主菜单...")
    
    def show_new_wangwen_traits(self):
        """显示新网文特质：反套路+人性博弈"""
        print("\n" + "="*80)
        print("✨ 新网文特质：从套路爽文到反套路+人性博弈")
        print("="*80)
        
        print("\n📊 新网文崛起背景：")
        print("  - 传统爽文退潮：废柴逆袭、无脑打脸已经过时")
        print("  - 读者审美升级：追求更深层次内容")
        
        print("\n🔥 新网文代表作（2026年霸榜作品）：")
        
        print("\n" + "="*60)
        print("【《诸神愚戏》——连续16个月番茄榜前列，评分9.8，评论近400万】")
        print("  核心设定：谎言成真")
        print("  故事内核：主角从命运弃子到带领人类打破神明桎梏")
        print("  深度价值：文明存续、命运抉择、自由意志的深刻思辨")
        
        print("\n" + "="*60)
        print("【《十日终焉》——悬疑无限流天花板，评分9.9】")
        print("  核心特色：多线叙事、象征体系、人性博弈放大")
        print("  现实映射：把当代人精神层面困境，用生死游戏形式呈现")
        
        print("\n" + "="*60)
        print("【《我不是戏神》——都市高武爆款，抖音话题阅读量超8亿】")
        print("  主角成长：以\"戏子\"身份在宿命枷锁中癫狂表演反抗")
        print("  主题升华：从求生到燃灯的蜕变")
        
        print("\n💎 新网文四大核心特质（2026年总结）：")
        
        print("\n" + "="*60)
        print("【特质1：反套路设计】")
        print("  - 跳出升级打怪寻宝的线性模式")
        print("  - 用错位感制造戏剧张力")
        print("  - 让期待的故事充满反转")
        print("  - 要求读者调动逻辑推理，理解主角布局或谎言")
        
        print("\n" + "="*60)
        print("【特质2：类型桎梏打破】")
        print("  - 传统类型边界不再重要")
        print("  - 多题材多元素深度融合：玄幻+科幻、历史+悬疑、都市+修仙")
        print("  - 进入规则重构与范式迭代新阶段")
        print("  - 题材深度化合+读者圈层突破，为网文创作开辟新路")
        
        print("\n" + "="*60)
        print("【特质3：隐喻化价值表达】")
        print("  - 深度嵌入现实关怀：不再是单纯娱乐消遣")
        print("  - 从直白浅露到深度隐喻：承载思想传递功能")
        print("  - 幻想外壳下的现实映射：")
        print("    - 《诸神愚戏》：职场、算法等现实议题，游戏化转译")
        print("    - 《十日终焉》：精神困境→生死游戏形式")
        
        print("\n" + "="*60)
        print("【特质4：立体人设】")
        print("  - 从扁平符号到真实共情")
        print("  - 反差性人设，赋予角色复杂性格")
        print("  - 人物不再伟光正或脸谱化，更接近真实人性")
        
        print("\n🚀 给创作者的启示：")
        print("  - 不要只追求爽感！要追求深度价值！")
        print("  - 不要只写个人逆袭！可以写共同成长、家国情怀！")
        print("  - 不要只用老套路！可以类型融合、设定创新！")
        print("  - 不要只写简单情节！可以加入人性博弈、逻辑推理！")
        
        print("\n📈 新网文的价值升级：")
        print("  - 从：情绪消费")
        print("  - 到：品质驱动、思想承载、文化传承")
        
        input("\n按回车返回主菜单...")
    
    def quit(self):
        """退出"""
        print("\n" + "="*80)
        print("👋 感谢使用 NWACS FINAL 最终统一版本!")
        print("="*80)
        print("\n祝您创作顺利！🎉")
        print("💡 包含2026年5月最新联网趋势数据！")
        time.sleep(1.5)
        sys.exit(0)

if __name__ == "__main__":
    NWACSFinal()
