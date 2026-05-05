#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS最终清理脚本
仅清理 __pycache__ 缓存目录
"""

import os
import shutil


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))

    safe_dirs = [
        '__pycache__',
    ]

    print("=" * 80)
    print("NWACS最终清理脚本")
    print("=" * 80)

    for dir_name in safe_dirs:
        dir_path = os.path.join(current_dir, dir_name)
        if os.path.exists(dir_path):
            try:
                shutil.rmtree(dir_path)
                print(f"已删除: {dir_name}")
            except Exception as e:
                print(f"删除失败: {dir_name} - {e}")
        else:
            print(f"不存在: {dir_name}")

    print("\n" + "=" * 80)
    print("清理完成！")
    print("=" * 80)


if __name__ == "__main__":
    main()
