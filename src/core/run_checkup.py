#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 系统自检脚本
单独运行的自检工具
"""

import os
import sys
from datetime import datetime

# 添加路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def main():
    print("=" * 60)
    print("          NWACS 系统自检工具")
    print("=" * 60)
    print(f"自检时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # 1. Skill体检
    print("[1/2] 执行Skill体检...")
    try:
        from skill_checkup import SkillCheckup
        checkup = SkillCheckup()
        report = checkup.check_all_skills()
        checkup.print_report(report)
        report_file = checkup.export_report(report)
        print(f"     ✓ 体检报告已导出: {report_file}")
    except Exception as e:
        print(f"     ✗ Skill体检失败: {e}")

    # 2. 文件清理优化
    print("\n[2/2] 执行文件清理优化...")
    try:
        from file_cleanup import FileCleanup
        cleaner = FileCleanup()

        # 先扫描
        print("     扫描项目中...")
        report = cleaner.generate_report()

        # 显示扫描结果
        print(f"     文件总数: {report['project_scan']['total_files']}")
        print(f"     项目大小: {cleaner._format_size(report['project_scan']['total_size'])}")
        
        if report['project_scan']['empty_files']:
            print(f"     空文件: {len(report['project_scan']['empty_files'])} 个")
        if report['project_scan']['old_files']:
            print(f"     旧文件: {len(report['project_scan']['old_files'])} 个")

        # 询问是否清理
        confirm = input("\n是否执行清理操作? (y/n): ").lower()
        if confirm == 'y':
            print("\n     正在清理...")
            cleaner.dry_run = False
            result = cleaner.clean_up()
            print(f"     ✓ 清理完成: 删除 {result['cleaned_count']} 个文件")
            print(f"     ✓ 释放空间: {result['freed_space_human']}")
        else:
            print("     已跳过清理")

    except Exception as e:
        print(f"     ✗ 文件清理失败: {e}")

    print("\n" + "=" * 60)
    print("    系统自检完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()