# -*- coding: utf-8 -*-
"""
NWACS 飞书指令服务器启动器
自动检测并解决依赖问题
"""
import os
import sys
import subprocess
import webbrowser
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent

print("="*70)
print("🚀 NWACS 飞书指令服务器启动器")
print("="*70)
print()

# 检查Python
print("[1/4] 检查Python环境...")
try:
    result = subprocess.run([sys.executable, "--version"], capture_output=True, text=True)
    print(f"   ✅ Python: {result.stdout.strip()}")
except Exception as e:
    print(f"   ❌ Python检查失败: {e}")
    input("按回车键退出...")
    sys.exit(1)

# 检查依赖
print()
print("[2/4] 检查依赖...")
required_modules = ["openai", "requests"]
missing = []

for module in required_modules:
    try:
        __import__(module)
        print(f"   ✅ {module}")
    except ImportError:
        print(f"   ⚠️ {module} 未安装")
        missing.append(module)

if missing:
    print()
    print(f"   安装缺失模块: {', '.join(missing)}")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install"] + missing)
        print("   ✅ 依赖安装完成")
    except Exception as e:
        print(f"   ❌ 安装失败: {e}")

# 启动服务器
print()
print("[3/4] 启动飞书指令服务器...")
print("   按 Ctrl+C 停止服务器")
print("="*70)
print()

try:
    # 直接运行服务器脚本
    server_script = PROJECT_ROOT / "feishu_command_server.py"
    subprocess.run([sys.executable, str(server_script)])

except KeyboardInterrupt:
    print("\n\n👋 服务器已停止")
except Exception as e:
    print(f"\n❌ 启动失败: {e}")

print()
print("="*70)
input("按回车键退出...")
