#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS - Novel Writing AI Collaborative System
统一入口 - 整合所有功能模块
"""

import sys
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CORE_DIR = os.path.join(ROOT_DIR, "core", "v8")

sys.path.insert(0, ROOT_DIR)
sys.path.insert(0, CORE_DIR)

def main():
    try:
        from NWACS_FINAL import NWACSFinal
        app = NWACSFinal()
    except ImportError as e:
        print(f"❌ 核心模块加载失败: {e}")
        print(f"   请确保 core/v8/ 目录完整")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n👋 NWACS 已退出")
    except Exception as e:
        print(f"❌ 运行错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
