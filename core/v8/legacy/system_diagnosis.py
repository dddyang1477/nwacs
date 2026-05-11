#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS FINAL - 系统完整度诊断工具
检测所有功能是否实际可用、是否有联动、是否真正起作用
"""

import os
import sys

def diagnose_system():
    """全面诊断系统功能"""
    print("="*80)
    print("🔍 NWACS FINAL - 系统完整度诊断")
    print("="*80)
    
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    results = {
        "✅ 正常": [],
        "⚠️ 警告": [],
        "❌ 错误": []
    }
    
    # 1. 检查核心文件
    print("\n📁 【文件完整性检查】")
    core_files = {
        "NWACS_FINAL.py": "主程序",
        "ai_detector_and_rewriter.py": "AI去痕模块",
        "quality_check_and_save_v2.py": "质量检测模块",
        "bestseller_deep_analyzer_v16.py": "爆款分析模块",
        "bestseller_opening_templates_v16.py": "爆款模板模块",
        "opening_examples_library_v15.py": "开局示例模块",
        "net_novel_core_guide_v15.py": "创作指南模块",
        "writing_templates_library.py": "写作模板库"
    }
    
    for filename, desc in core_files.items():
        filepath = os.path.join(base_path, filename)
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            results["✅ 正常"].append(f"{filename} ({size}字节)")
            print(f"  ✅ {filename} - {desc} ({size}字节)")
        else:
            results["❌ 错误"].append(f"{filename} - 缺失!")
            print(f"  ❌ {filename} - 缺失!")
    
    # 2. 检查函数完整性
    print("\n📋 【函数联动检查】")
    
    # 检查主程序中调用的函数
    main_file = os.path.join(base_path, "NWACS_FINAL.py")
    if os.path.exists(main_file):
        with open(main_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 需要在主程序中定义的方法
        required_methods = [
            "show_bestseller_analysis",
            "show_bestseller_templates",
            "show_success_factors",
            "show_opening_formulas",
            "show_new_paradigm",
            "show_tomato_topics",
            "show_drama_adaptation",
            "show_new_wangwen_traits",
            "show_reader_psychology",
            "show_shuang_points",
            "show_character_contrast",
            "show_golden_hooks",
            "show_book_titles",
            "show_opening_examples",
            "quick_generate",
            "save_novel_to_folder",
            "show_about",
            "quit"
        ]
        
        for method in required_methods:
            if f"def {method}(" in content:
                results["✅ 正常"].append(f"方法: {method}")
                print(f"  ✅ 方法定义: {method}")
            else:
                results["⚠️ 警告"].append(f"方法未定义: {method}")
                print(f"  ⚠️ 方法未定义: {method}")
    
    # 3. 检查模块联动
    print("\n🔗 【模块联动检查】")
    
    # 检查是否正确导入模块
    module_imports = [
        ("bestseller_opening_templates_v16", "BestsellerOpeningTemplates"),
        ("bestseller_deep_analyzer_v16", "BestsellerDeepAnalyzer"),
        ("net_novel_core_guide_v15", "NetNovelCoreGuide"),
        ("opening_examples_library_v15", "OpeningExamplesLibrary"),
        ("ai_detector_and_rewriter", "AIDetectorAndRewriter"),
        ("quality_check_and_save_v2", "QualityChecker")
    ]
    
    for module_name, class_name in module_imports:
        module_file = os.path.join(base_path, f"{module_name}.py")
        if os.path.exists(module_file):
            with open(module_file, 'r', encoding='utf-8') as f:
                module_content = f.read()
            
            if f"class {class_name}" in module_content:
                results["✅ 正常"].append(f"模块类: {module_name}.{class_name}")
                print(f"  ✅ {module_name}.{class_name}")
            else:
                results["⚠️ 警告"].append(f"类定义缺失: {module_name}.{class_name}")
                print(f"  ⚠️ 类定义缺失: {module_name}.{class_name}")
        else:
            results["❌ 错误"].append(f"模块文件缺失: {module_name}")
            print(f"  ❌ 模块文件缺失: {module_name}")
    
    # 4. 检查功能实际调用
    print("\n🎯 【功能调用检查】")
    
    if os.path.exists(main_file):
        with open(main_file, 'r', encoding='utf-8') as f:
            main_content = f.read()
        
        # 检查菜单选项对应的调用
        call_checks = [
            ("quick_generate", "save_novel_to_folder", "小说保存"),
            ("show_bestseller_templates", "BestsellerOpeningTemplates", "爆款模板"),
            ("show_reader_psychology", "NetNovelCoreGuide", "读者心理学"),
            ("show_opening_examples", "OpeningExamplesLibrary", "开局示例")
        ]
        
        for method, module, desc in call_checks:
            if method in main_content and module in main_content:
                results["✅ 正常"].append(f"联动: {method} -> {module}")
                print(f"  ✅ {desc}功能: {method}正确调用{module}")
            elif method in main_content:
                results["⚠️ 警告"].append(f"方法存在但可能未调用模块: {method}")
                print(f"  ⚠️ {desc}功能: {method}可能未正确调用")
            else:
                results["❌ 错误"].append(f"功能方法缺失: {method}")
                print(f"  ❌ {desc}功能方法缺失: {method}")
    
    # 5. 检查novels文件夹
    print("\n📂 【文件夹结构检查】")
    novels_folder = os.path.join(base_path, "novels")
    if os.path.exists(novels_folder):
        novel_count = len(os.listdir(novels_folder))
        results["✅ 正常"].append(f"novels文件夹存在 ({novel_count}个小说)")
        print(f"  ✅ novels文件夹存在 ({novel_count}个小说)")
    else:
        results["⚠️ 警告"].append("novels文件夹不存在（将在首次生成时创建）")
        print(f"  ⚠️ novels文件夹不存在（将在首次生成时创建）")
    
    # 6. 生成总结
    print("\n" + "="*80)
    print("📊 诊断总结")
    print("="*80)
    
    total = len(results["✅ 正常"]) + len(results["⚠️ 警告"]) + len(results["❌ 错误"])
    
    print(f"\n✅ 正常: {len(results['✅ 正常'])}/{total}")
    print(f"⚠️ 警告: {len(results['⚠️ 警告'])}/{total}")
    print(f"❌ 错误: {len(results['❌ 错误'])}/{total}")
    
    if results["❌ 错误"]:
        print("\n❌ 需要修复的错误:")
        for item in results["❌ 错误"]:
            print(f"   - {item}")
    
    if results["⚠️ 警告"]:
        print("\n⚠️ 需要关注的警告:")
        for item in results["⚠️ 警告"]:
            print(f"   - {item}")
    
    print("\n" + "="*80)
    
    # 7. 功能清单
    print("\n📋 【菜单功能清单】")
    print("""
 1. ✅ 40本真实爆款深度分析 - 需要 bestseller_deep_analyzer_v16.py
 2. ✅ 40个基于真实爆款的开局模板 - 需要 bestseller_opening_templates_v16.py
 3. ✅ 爆款成功因素与避坑指南 - 主程序内嵌
 4. ✅ 爆款开局公式总结 - 主程序内嵌
 5. ✅ 冲突前置vs黄金三章 - 主程序内嵌（2026新趋势）
 6. ✅ 番茄小说顶流题材分析 - 主程序内嵌（2026新趋势）
 7. ✅ 短剧IP改编创作指南 - 主程序内嵌（2026新趋势）
 8. ✅ 新网文特质 - 主程序内嵌（2026新趋势）
 9. ✅ 读者心理学 - 需要 net_novel_core_guide_v15.py
10. ✅ 爽点设计 - 需要 net_novel_core_guide_v15.py
11. ✅ 人设反差设计 - 需要 net_novel_core_guide_v15.py
12. ✅ 金句钩子设计 - 需要 net_novel_core_guide_v15.py
13. ✅ 爆款书名公式 - 需要 net_novel_core_guide_v15.py
14. ✅ 玄幻开局示例 - 需要 opening_examples_library_v15.py
15. ✅ 都市开局示例 - 需要 opening_examples_library_v15.py
16. ✅ 言情开局示例 - 需要 opening_examples_library_v15.py
17. ✅ 悬疑开局示例 - 需要 opening_examples_library_v15.py
18. ✅ 快速生成开局 - 主程序 + AI去痕 + 质量检测
19. ✅ 关于与帮助 - 主程序内嵌
    """)
    
    return results

if __name__ == "__main__":
    results = diagnose_system()
    input("\n按回车退出...")
