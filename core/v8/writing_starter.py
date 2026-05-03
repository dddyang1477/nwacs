#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS V8.0 写作启动器
自动运行：命名工具 → 角色模板 → 写作流水线
"""

import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

def print_header():
    print("="*60)
    print("📖 NWACS V8.0 小说创作启动器")
    print("="*60)
    print("\n【创作流程】")
    print("  1️⃣ 自动生成角色名字")
    print("  2️⃣ 创建角色模板")
    print("  3️⃣ 启动写作流水线")
    print("="*60)

def step1_generate_names():
    """步骤1: 生成角色名字"""
    print("\n" + "="*60)
    print("📝 步骤1: 生成角色名字")
    print("="*60)

    try:
        from core.character_namer_v3 import CharacterNamer
        namer = CharacterNamer()

        print("\n🎲 随机生成角色阵容:")
        print("\n【主角】")
        protagonist = namer.name_xianxia_male()
        print(f"   姓名: {protagonist}")

        print("\n【女主】")
        heroine = namer.name_warm_female()
        print(f"   姓名: {heroine}")

        print("\n【配角】")
        supporting = namer.name_xianxia_male()
        print(f"   姓名: {supporting}")

        print("\n【反派】")
        antagonist = namer.name_evil_male()
        print(f"   姓名: {antagonist}")

        print("\n【复姓贵族】")
        noble = namer.generate_compound_surname()
        print(f"   姓名: {noble}")

        return {
            "protagonist": protagonist,
            "heroine": heroine,
            "supporting": supporting,
            "antagonist": antagonist,
            "noble": noble
        }

    except Exception as e:
        print(f"   ⚠️ 命名工具加载失败: {e}")
        return None

def step2_create_templates(names):
    """步骤2: 创建角色模板"""
    print("\n" + "="*60)
    print("🎭 步骤2: 创建角色模板")
    print("="*60)

    if not names:
        print("   ⚠️ 没有角色名字，跳过")
        return None

    try:
        from core.v8.character_template import CharacterTemplateManager

        novel_name = input("\n请输入小说名称: ").strip()
        if not novel_name:
            novel_name = "我的小说"

        manager = CharacterTemplateManager(novel_name)

        from core.v8.character_template import CharacterTemplate

        print("\n📝 正在创建角色模板...")

        char_configs = [
            ("主角", names.get("protagonist", "叶青云"), "protagonist"),
            ("女主", names.get("heroine", "苏沐雪"), "heroine"),
            ("配角", names.get("supporting", "萧寒"), "supporting"),
            ("反派", names.get("antagonist", "林逸"), "antagonist"),
        ]

        for role, name, role_type in char_configs:
            if name:
                char = manager.create_character(name, role_type)
                print(f"   ✅ 创建{role}: {name}")

        manager.save_templates()

        print(f"\n   ✅ 已创建 {len(char_configs)} 个角色模板")
        print(f"   📁 保存位置: novels/{novel_name}/characters/")

        return manager

    except Exception as e:
        print(f"   ⚠️ 角色模板创建失败: {e}")
        return None

def step3_start_pipeline():
    """步骤3: 启动写作流水线"""
    print("\n" + "="*60)
    print("🚀 步骤3: 启动写作流水线")
    print("="*60)

    print("\n即将启动Skill协作编排系统...")
    print("系统将自动按顺序执行7个阶段！")

    choice = input("\n是否启动写作流水线？(Y/n): ").strip().lower()
    if choice != "n":
        print("\n启动中...")
        os.system("py core/v8/skill_orchestrator.py")
    else:
        print("\n好的，可以稍后手动启动:")
        print("   py core/v8/skill_orchestrator.py")

def main():
    print_header()

    print("\n🎯 开始小说创作流程")
    print("本流程将自动完成：命名 → 模板 → 写作")

    # 步骤1: 生成名字
    names = step1_generate_names()

    # 步骤2: 创建模板
    manager = step2_create_templates(names)

    # 步骤3: 启动流水线
    step3_start_pipeline()

    print("\n" + "="*60)
    print("🎉 创作流程已完成！")
    print("="*60)
    print("\n接下来你可以:")
    print("   1. 使用 py core/v8/skill_orchestrator.py 继续写作")
    print("   2. 查看角色模板: novels/{小说名}/characters/")
    print("   3. 使用 py smart_start.py 启动其他模式")

if __name__ == "__main__":
    main()
