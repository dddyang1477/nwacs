#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS最终清理脚本
删除所有旧版目录和缓存
"""
import os
import shutil

current_dir = os.path.dirname(os.path.abspath(__file__))

old_dirs = [
    '__pycache__',
    'api_gateway',
    'config',
    'engine',
    'knowledge_base',
    'skill_manager'
]

print("=" * 80)
print("NWACS最终清理脚本")
print("=" * 80)

for dir_name in old_dirs:
    dir_path = os.path.join(current_dir, dir_name)
    if os.path.exists(dir_path):
        try:
            shutil.rmtree(dir_path)
            print(f"✅ 已删除: {dir_name}")
        except Exception as e:
            print(f"❌ 删除失败: {dir_name} - {e}")
    else:
        print(f"ℹ️  不存在: {dir_name}")

print("\n" + "=" * 80)
print("清理完成！")
print("=" * 80)

# 删除自己
try:
    os.unlink(__file__)
    print(f"\n✅ 已删除清理脚本")
except Exception as e:
    print(f"\n⚠️  无法删除清理脚本")

print("\n")
