#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""创建批处理文件"""

import os

# 批处理文件内容
bat_content = '''@echo off
chcp 65001 >nul
title NWACS - 小说创作辅助系统

cd /d "%~dp0"

python main.py

pause
'''

# 配置工具批处理内容
config_bat_content = '''@echo off
chcp 65001 >nul
title NWACS - 配置工具

cd /d "%~dp0"

python config_tool.py

pause
'''

# 创建启动批处理
with open('启动NWACS.bat', 'w', encoding='utf-8') as f:
    f.write(bat_content)

# 创建配置批处理
with open('配置NWACS.bat', 'w', encoding='utf-8') as f:
    f.write(config_bat_content)

print("批处理文件创建成功！")