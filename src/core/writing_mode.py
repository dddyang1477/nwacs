#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
专注写作模式
功能：全屏写作界面、实时字数统计、章节进度追踪
"""

import os
import sys
import time
from datetime import datetime

class WritingMode:
    def __init__(self):
        self.current_file = None
        self.start_time = None
        self.total_words = 0
        self.session_words = 0

    def start_writing(self, filename=None):
        if filename:
            self.current_file = f"manuscripts/{filename}.txt"
            os.makedirs("manuscripts", exist_ok=True)

        self.start_time = time.time()
        self.session_words = 0

        print("\n" + "=" * 60)
        print("              Focus Writing Mode")
        print("=" * 60)
        print("\nPress Ctrl+C to save and exit")
        print("-" * 60)

        try:
            while True:
                line = input()
                if line.strip():
                    self.session_words += len(line.strip())
                    self.total_words += len(line.strip())

                    if self.current_file:
                        with open(self.current_file, 'a', encoding='utf-8') as f:
                            f.write(line + "\n")

                elapsed = int(time.time() - self.start_time)
                mins = elapsed // 60
                secs = elapsed % 60
                print(f"  [{mins:02d}:{secs:02d}] Words: {self.session_words} / Total: {self.total_words}", end="\r")

        except KeyboardInterrupt:
            self.save_and_exit()

    def save_and_exit(self):
        print("\n\n" + "-" * 60)
        print("Saving...")
        print(f"Session: {self.session_words} words")
        print(f"Total: {self.total_words} words")
        print("Saved to:", self.current_file if self.current_file else "Memory")
        print("-" * 60)

def main():
    mode = WritingMode()
    filename = input("Filename (Enter for new): ").strip()
    mode.start_writing(filename if filename else None)

if __name__ == "__main__":
    main()
