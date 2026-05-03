#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix duplicate code in NWACS_FINAL.py
"""

import os

def fix_duplicate():
    base_path = os.path.dirname(os.path.abspath(__file__))
    main_file = os.path.join(base_path, "NWACS_FINAL.py")

    print("Reading file...")
    with open(main_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    print("Fixing duplicate code...")

    # Find and remove duplicate lines
    new_lines = []
    skip = False
    i = 0

    while i < len(lines):
        line = lines[i]

        # Skip duplicate block (lines with just variable assignments)
        if '                processed_opening,' in line and i > 600:
            # Check if this is part of duplicate block
            if i + 2 < len(lines) and '                chapter_num=1,' in lines[i+1]:
                skip = True
                i += 4  # Skip 4 lines of duplicate
                continue

        if skip:
            if ')' in line and 'novel_title' not in line:
                skip = False
            i += 1
            continue

        new_lines.append(line)
        i += 1

    print(f"Original lines: {len(lines)}")
    print(f"New lines: {len(new_lines)}")
    print(f"Removed: {len(lines) - len(new_lines)} duplicate lines")

    print("Saving file...")
    with open(main_file, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    print("Done!")

if __name__ == "__main__":
    fix_duplicate()
