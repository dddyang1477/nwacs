#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""快速验证命名系统扩展"""
from chinese_traditional_namer import ChineseTraditionalNamer, FiveElement, Gender

n = ChineseTraditionalNamer()

stats = n.get_surname_stats()
print(f"姓氏总数: {stats['total_surnames']}")
print(f"分类数: {stats['total_categories']}")
print(f"分类详情: {stats['by_category']}")

print("\n【复姓+典故命名】")
names = n.generate(surname="南宫", gender=Gender.MALE, strategy="classical", count=3)
for x in names:
    print(f"  {x.full_name} | {x.meaning[:60]}")

print("\n【女性典故命名】")
names2 = n.generate(surname="叶", gender=Gender.FEMALE, strategy="classical", count=3)
for x in names2:
    print(f"  {x.full_name} | {x.meaning[:60]}")

print("\n【随机姓氏命名】")
for _ in range(5):
    surname = n.get_random_surname(["compound"])
    name = n.generate(surname=surname, gender=Gender.MALE, count=1)[0]
    print(f"  {name.full_name} ({surname})")

print("\n【全部姓氏扁平列表】")
all_s = n.get_all_surnames()
print(f"  共 {len(all_s)} 个姓氏")
print(f"  前20: {all_s[:20]}")
print(f"  后20: {all_s[-20:]}")

print("\n✅ 命名系统扩展验证完成")
