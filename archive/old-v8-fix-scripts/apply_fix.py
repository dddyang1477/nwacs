#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS FINAL - Python修复脚本
将三次质量检验集成到主程序
"""

import os
import sys

def main():
    print("=" * 70)
    print("NWACS FINAL - Three-Time Quality Check Fix Script (Python)")
    print("=" * 70)
    print()

    base_path = os.path.dirname(os.path.abspath(__file__))
    main_file = os.path.join(base_path, "NWACS_FINAL.py")

    print("[1/3] Reading NWACS_FINAL.py...")

    if not os.path.exists(main_file):
        print("[ERROR] NWACS_FINAL.py not found!")
        return

    with open(main_file, 'r', encoding='utf-8') as f:
        content = f.read()

    print("[2/3] Checking and applying fix...")

    # Check if already fixed
    if "call_three_time_quality_check" in content:
        print("  [SKIP] Already has three-time check integrated!")
        print()
        print("Fix already applied. No action needed.")
        return

    # Old code
    old_code = """        # 3. 集成质量检测功能
        try:
            from quality_check_and_save_v2 import QualityChecker
            checker = QualityChecker(processed_opening, 1)
            passed, report = checker.run_all_checks()
            
            if not passed:
                print("⚠️ 质量检测提示：建议后续人工完善内容")
        except Exception as e:
            print(f"⚠️ 质量检测模块加载跳过: {e}")"""

    # New code (three-time check)
    new_code = """        # 3. Integrate three-time quality check process
        print("\\n" + "="*60)
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
                print(f"Quality check module skipped: {e2}")"""

    # Execute replace
    if old_code in content:
        content = content.replace(old_code, new_code)

        # Save file
        with open(main_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print("  [OK] Fix applied successfully!")
    else:
        print("  [ERROR] Cannot find code to replace")
        print("  Code may have been modified already or format is different")
        print()
        print("Please check the file manually.")
        return

    print("[3/3] Verifying fix...")

    # Verify
    with open(main_file, 'r', encoding='utf-8') as f:
        verify = f.read()

    if "call_three_time_quality_check" in verify:
        print("  [OK] Verification passed!")
    else:
        print("  [ERROR] Verification failed")
        return

    print()
    print("=" * 70)
    print("Fix completed successfully!")
    print("Now you can run: python NWACS_FINAL.py")
    print("=" * 70)

if __name__ == "__main__":
    main()
