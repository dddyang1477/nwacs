#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试角色起名系统 v3.0
"""
import sys
sys.path.insert(0, 'core')

from character_namer_v3 import CharacterNamer

print("="*60)
print("NWACS 智能起名系统 v3.0 测试")
print("="*60)
print()

namer = CharacterNamer()

print("1️⃣ 测试霸道总裁男主:")
for i in range(5):
    print(f"   {i+1}. {namer.name_boss_male()}")

print("\n2️⃣ 测试温柔治愈型:")
for i in range(5):
    print(f"   {i+1}. {namer.name_gentle_male()}")

print("\n3️⃣ 测试武侠江湖型:")
for i in range(5):
    print(f"   {i+1}. {namer.name_wuxia_male()}")

print("\n4️⃣ 测试仙风道骨型:")
for i in range(5):
    print(f"   {i+1}. {namer.name_immortal_male()}")

print("\n5️⃣ 测试温柔甜美女主:")
for i in range(5):
    print(f"   {i+1}. {namer.name_warm_female()}")

print("\n6️⃣ 测试古典才女型:")
for i in range(5):
    print(f"   {i+1}. {namer.name_talented_female()}")

print("\n7️⃣ 测试复姓贵族:")
for i in range(5):
    print(f"   {i+1}. {namer.name_compound_surname()}")

print("\n8️⃣ 测试CP组合:")
for i in range(3):
    male, female = namer.name_couple('boss', 'warm')
    print(f"   {i+1}. {male} × {female}")

print("\n9️⃣ 测试玄幻小说全套角色阵容:")
cast = namer.generate_novel_cast('xuanhuan')
role_names = {
    'protagonist': '主角',
    'female_lead': '女主',
    'second_lead': '女配',
    'best_friend': '挚友',
    'mentor': '师父',
    'villain': '反派',
    'villain_henchman': '反派手下'
}
for role, name in cast.items():
    print(f"   {role_names.get(role, role)}: {name}")

print("\n🔟 测试五行名字:")
elements = ['木', '火', '土', '金', '水']
for elem in elements:
    male = namer.name_by_wuxing(elem, 'male', 'boss')
    female = namer.name_by_wuxing(elem, 'female', 'warm')
    print(f"   {elem}行: 男-{male} / 女-{female}")

print()
print("="*60)
print("测试完成！")
print("="*60)
