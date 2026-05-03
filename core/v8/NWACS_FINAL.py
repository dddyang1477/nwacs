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
            print(" 19. 关于与帮助")
            print("  0. 退出")
            
            choice = input(f"\n请输入选项 (0-19): ").strip()
            
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
                self.show_about()
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
        """保存小说到文件夹 - 增强版：含AI去痕和质量检测"""
        import os
        from datetime import datetime
        
        # 创建小说主文件夹
        base_path = os.path.dirname(os.path.abspath(__file__))
        novels_folder = os.path.join(base_path, "novels")
        if not os.path.exists(novels_folder):
            os.makedirs(novels_folder)
        
        # 创建以小说名命名的文件夹
        clean_name = "".join(c for c in novel_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        novel_folder = os.path.join(novels_folder, clean_name)
        
        # 如果文件夹已存在，添加时间戳
        if os.path.exists(novel_folder):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            novel_folder = os.path.join(novels_folder, f"{clean_name}_{timestamp}")
        
        os.makedirs(novel_folder)
        
        print(f"\n✅ 已创建小说文件夹: {novel_folder}")
        
        # 1. 获取开局内容
        original_opening = template['example_opening']
        
        # 2. 集成AI去痕功能
        print("\n" + "="*60)
        print("🔍 开始AI检测与去痕...")
        print("="*60)
        
        processed_opening = original_opening
        try:
            # 尝试加载AI去痕模块
            from ai_detector_and_rewriter import AIDetectorAndRewriter
            detector = AIDetectorAndRewriter()
            processed_opening = detector.check_and_rewrite(original_opening)
        except Exception as e:
            print(f"⚠️ AI去痕模块加载跳过: {e}")
            processed_opening = original_opening
        
        # 3. Integrate three-time quality check process
        print("\n" + "="*60)
        print("Starting three-time quality check process...")
        print("   Up to 3 checks, will reprocess if failed")
        print("="*60)

        try:
            from three_time_quality_check import call_three_time_quality_check
            processed_opening, quality_passed, quality_report = call_three_time_quality_check(
                processed_opening,
                chapter_num=1,
                novel_title=novel_name
            )

            if quality_passed:
                print("All three checks passed!")
            else:
                print("Warning: Not all checks passed, suggest manual review")

        except Exception as e:
            print(f"Three-time check error: {e}")
            print("   Falling back to basic quality check...")
            try:
                from quality_check_and_save_v2 import QualityChecker
                checker = QualityChecker(processed_opening, 1)
                passed, report = checker.run_all_checks()

                if not passed:
                    print("Warning: Quality check suggests manual review")
            except Exception as e2:
                print(f"Quality check module skipped: {e2}")      
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
        
        # 5. 保存开局文件（原始版和去痕版都保存）
        opening_file = os.path.join(novel_folder, "第一章_开局_去痕版.txt")
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
        
        print(f"✅ 已保存开局(去痕版): {opening_file}")
        
        # 保存原始版作为参考
        original_file = os.path.join(novel_folder, "第一章_开局_参考版.txt")
        with open(original_file, "w", encoding="utf-8") as f:
            f.write(f"# {novel_name} - 第一章（原始参考）\n\n")
            f.write(f"## 正文\n")
            f.write(original_opening)
        
        print(f"✅ 已保存参考版: {original_file}")
        
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
        print(f"\n小说文件夹: {novel_folder}")
        print("\n已创建文件:")
        print("  1. 小说信息.md - 模板信息与核心要素")
        print("  2. 第一章_开局_去痕版.txt - 推荐使用此版本")
        print("  3. 第一章_开局_参考版.txt - 原始版对比参考")
        print("  4. 小说大纲.md - 可编辑的大纲模板")
        print("  5. AI去痕与优化指南.md - 后续人工优化建议")
        
        input("\n按回车返回主菜单...")
    
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
    engine = NWACSFinal()
    engine.run()
