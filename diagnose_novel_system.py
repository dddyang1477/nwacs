#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
诊断小说生成系统问题
检测命名系统和硬编码问题
"""
import sys
from pathlib import Path

# 添加 core 目录到路径
sys.path.insert(0, str(Path(__file__).parent / "core"))

print("="*60)
print("NWACS 小说生成系统诊断")
print("="*60)
print()

# 1. 测试命名系统
print("1️⃣ 测试命名系统...")
try:
    from character_namer import CharacterNamer
    namer = CharacterNamer()
    print("   ✅ 命名系统导入成功")
    
    print("\n   测试生成名字：")
    test_male1 = namer.name_boss_male()
    test_male2 = namer.name_gentle_male()
    test_female1 = namer.name_warm_female()
    test_female2 = namer.name_strong_female()
    test_villain = namer.name_villain()
    
    print(f"      霸道总裁: {test_male1}")
    print(f"      温柔男主: {test_male2}")
    print(f"      温柔女主: {test_female1}")
    print(f"      飒爽女主: {test_female2}")
    print(f"      反派: {test_villain}")
    print("   ✅ 命名系统工作正常！")
except Exception as e:
    print(f"   ❌ 命名系统错误: {e}")

print()

# 2. 检查项目管理器中的硬编码问题
print("2️⃣ 检查项目管理器代码...")
try:
    project_file = Path(__file__).parent / "core" / "novel_project_manager.py"
    content = project_file.read_text(encoding="utf-8")
    
    check_names = ["顾长青", "苏瑶", "姜雪晴", "王天辰", "苍元大陆", "苍云宗"]
    found_issues = []
    
    for name in check_names:
        if name in content:
            count = content.count(name)
            found_issues.append((name, count))
    
    if found_issues:
        print("   ⚠️ 发现硬编码问题：")
        for name, count in found_issues:
            print(f"      - '{name}' 出现了 {count} 次")
    else:
        print("   ✅ 未发现硬编码问题")
    
except Exception as e:
    print(f"   ❌ 检查错误: {e}")

print()
print("="*60)
print("诊断完成！")
print("="*60)
