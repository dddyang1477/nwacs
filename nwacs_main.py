#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 主入口
"""

import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

def main():
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║              NWACS 小说创作系统 v2.0                        ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

核心工具位于 core/ 目录：

  py core/nwacs_console.py       # 控制台模式
  py core/nwacs_single.py 1      # 生成框架
  py core/nwacs_single.py 6      # 查看状态
    """)

if __name__ == "__main__":
    main()
