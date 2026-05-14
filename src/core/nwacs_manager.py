#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 系统启动管理器
支持：自动启动、服务管理、配置设置
"""

import os
import sys
import json
import time
import subprocess
import ctypes
from datetime import datetime
from logger import logger

class NWACSManager:
    """NWACS 系统管理器"""

    def __init__(self):
        self.config_file = 'config.json'
        self.auto_start_reg_path = r'Software\Microsoft\Windows\CurrentVersion\Run'
        self.auto_start_name = 'NWACS_AutoStart'
        self._load_config()

    def _load_config(self):
        """加载配置"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            except Exception:
                self.config = {}
        else:
            self.config = {}

    def _save_config(self):
        """保存配置"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.log_exception(e, "保存配置")

    def set_deepseek_v4(self):
        """配置 DeepSeek V4 模型"""
        config = {
            'api_key': '',
            'base_url': 'https://api.deepseek.com/v1',
            'model': 'deepseek-chat',
            'enabled': True,
            'model_version': 'v4'
        }

        print("\n配置 DeepSeek V4 模型")
        print("-" * 40)
        
        api_key = input("请输入 DeepSeek API Key（留空使用环境变量）: ").strip()
        if api_key:
            config['api_key'] = api_key

        self.config.update(config)
        self._save_config()

        print("✓ DeepSeek V4 配置已保存")
        print(f"  API 地址: {config['base_url']}")
        print(f"  模型: {config['model']}")
        print(f"  是否启用: {config['enabled']}")

    def set_sensitivity_filter(self, content_type='political'):
        """配置敏感词过滤类型"""
        if 'sensitivity' not in self.config:
            self.config['sensitivity'] = {}

        self.config['sensitivity']['content_type'] = content_type
        self.config['sensitivity']['check_level'] = 'normal'

        self._save_config()

        print(f"\n✓ 敏感词过滤已配置为: {content_type}")

    def enable_auto_start(self):
        """启用开机自动启动"""
        try:
            import winreg

            # 获取当前脚本路径
            script_path = os.path.abspath(sys.argv[0])
            
            # 如果是 Python 脚本，创建批处理文件
            if script_path.endswith('.py'):
                bat_path = script_path.replace('.py', '_auto.bat')
                with open(bat_path, 'w', encoding='utf-8') as f:
                    f.write(f'''@echo off
chcp 65001 >nul
cd /d "{os.path.dirname(script_path)}"
python "{script_path}"
''')
                script_path = bat_path

            # 添加到注册表
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                self.auto_start_reg_path,
                0,
                winreg.KEY_SET_VALUE
            ) as key:
                winreg.SetValueEx(
                    key,
                    self.auto_start_name,
                    0,
                    winreg.REG_SZ,
                    script_path
                )

            print("\n✓ 已启用开机自动启动")
            print(f"  启动项: {script_path}")
            return True

        except Exception as e:
            print(f"\n✗ 启用自动启动失败: {e}")
            return False

    def disable_auto_start(self):
        """禁用开机自动启动"""
        try:
            import winreg

            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                self.auto_start_reg_path,
                0,
                winreg.KEY_SET_VALUE
            ) as key:
                try:
                    winreg.DeleteValue(key, self.auto_start_name)
                    print("\n✓ 已禁用开机自动启动")
                except FileNotFoundError:
                    print("\n✓ 未找到自动启动项")

            return True

        except Exception as e:
            print(f"\n✗ 禁用自动启动失败: {e}")
            return False

    def check_auto_start(self):
        """检查自动启动状态"""
        try:
            import winreg

            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                self.auto_start_reg_path,
                0,
                winreg.KEY_READ
            ) as key:
                try:
                    value, _ = winreg.QueryValueEx(key, self.auto_start_name)
                    return {'enabled': True, 'path': value}
                except FileNotFoundError:
                    return {'enabled': False}

        except Exception as e:
            logger.log_exception(e, "检查自动启动")
            return {'enabled': False, 'error': str(e)}

    def start_services(self):
        """启动所有服务"""
        print("\n启动 NWACS 服务...")
        print("-" * 40)

        # 启动学习系统
        print("1. 启动学习系统...")
        try:
            from skill_learning_manager import SkillLearningManager
            manager = SkillLearningManager()
            manager.start_all_learning()
            print("   ✓ 学习系统已启动")
        except Exception as e:
            print(f"   ✗ 学习系统启动失败: {e}")

        # 启动空闲检测
        print("2. 启动空闲检测...")
        try:
            from idle_learning import start_idle_detection
            start_idle_detection()
            print("   ✓ 空闲检测已启动")
        except Exception as e:
            print(f"   ✗ 空闲检测启动失败: {e}")

        # 启动每日检查
        print("3. 启动每日检查...")
        try:
            from daily_checker import DailyChecker
            checker = DailyChecker()
            checker.start()
            print("   ✓ 每日检查已启动")
        except Exception as e:
            print(f"   ✗ 每日检查启动失败: {e}")

        print("\n✓ 所有服务启动完成！")

    def show_config(self):
        """显示当前配置"""
        print("\n当前配置")
        print("-" * 40)

        # 模型配置
        print("\n【大模型配置】")
        print(f"  API 地址: {self.config.get('base_url', '未设置')}")
        print(f"  模型: {self.config.get('model', '未设置')}")
        print(f"  版本: {self.config.get('model_version', '未设置')}")
        print(f"  是否启用: {self.config.get('enabled', False)}")

        # 敏感词配置
        print("\n【敏感词过滤配置】")
        sensitivity = self.config.get('sensitivity', {})
        print(f"  过滤类型: {sensitivity.get('content_type', '未设置')}")
        print(f"  检查级别: {sensitivity.get('check_level', '未设置')}")

        # 自动启动配置
        print("\n【自动启动配置】")
        auto_start = self.check_auto_start()
        print(f"  状态: {'已启用' if auto_start.get('enabled') else '已禁用'}")
        if auto_start.get('path'):
            print(f"  路径: {auto_start['path']}")

    def run_wizard(self):
        """配置向导"""
        print("\n" + "=" * 60)
        print("    NWACS 配置向导")
        print("=" * 60)

        while True:
            print("\n请选择配置项:")
            print("1. 配置 DeepSeek V4")
            print("2. 设置敏感词过滤（仅政治敏感词）")
            print("3. 启用开机自动启动")
            print("4. 禁用开机自动启动")
            print("5. 启动所有服务")
            print("6. 查看当前配置")
            print("0. 退出")

            choice = input("\n请输入选择 [0-6]: ").strip()

            if choice == '1':
                self.set_deepseek_v4()
            elif choice == '2':
                self.set_sensitivity_filter('political')
            elif choice == '3':
                self.enable_auto_start()
            elif choice == '4':
                self.disable_auto_start()
            elif choice == '5':
                self.start_services()
            elif choice == '6':
                self.show_config()
            elif choice == '0':
                print("\n✓ 配置完成！")
                break
            else:
                print("✗ 无效选择，请重新输入")


def main():
    """主函数"""
    manager = NWACSManager()

    if len(sys.argv) > 1:
        # 命令行模式
        command = sys.argv[1]

        if command == 'set-deepseek':
            manager.set_deepseek_v4()
        elif command == 'set-sensitivity':
            manager.set_sensitivity_filter('political')
        elif command == 'enable-auto':
            manager.enable_auto_start()
        elif command == 'disable-auto':
            manager.disable_auto_start()
        elif command == 'start':
            manager.start_services()
        elif command == 'config':
            manager.show_config()
        else:
            print(f"未知命令: {command}")
    else:
        # 交互模式
        manager.run_wizard()


if __name__ == "__main__":
    main()
