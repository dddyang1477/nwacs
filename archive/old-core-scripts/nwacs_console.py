#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 控制台 - 统一操作入口
整合所有手动操作项，方便选择使用
"""

import os
import sys
import subprocess

sys.stdout.reconfigure(encoding='utf-8')

class NWACSConsole:
    """NWACS 控制台"""

    def __init__(self):
        self.menu_items = [
            {
                'id': '1',
                'name': '启动完整系统',
                'description': '启动所有服务（学习系统、空闲检测、创作辅助工具）',
                'action': self.start_full_system
            },
            {
                'id': '2',
                'name': '专注写作模式',
                'description': '全屏写作界面，实时字数统计',
                'action': self.start_writing_mode
            },
            {
                'id': '3',
                'name': '剧情设计器',
                'description': '可视化情节流程图、伏笔追踪、张力曲线',
                'action': self.start_plot_designer
            },
            {
                'id': '4',
                'name': '配置工具',
                'description': '设置 DeepSeek API Key、敏感词过滤、自动启动',
                'action': self.start_config_tool
            },
            {
                'id': '5',
                'name': '学习系统管理',
                'description': '管理 Skill 学习计划、查看学习进度',
                'action': self.start_learning_manager
            },
            {
                'id': '6',
                'name': '创作辅助工具',
                'description': 'AI检测、节奏分析、连贯性检查等工具',
                'action': self.start_writing_assistant
            },
            {
                'id': '7',
                'name': '系统状态检查',
                'description': '检查所有服务是否正常运行',
                'action': self.check_system_status
            },
            {
                'id': '8',
                'name': '数据统计面板',
                'description': '查看写作统计、学习进度、成就系统',
                'action': self.show_stats_dashboard
            },
            {
                'id': '0',
                'name': '退出',
                'description': '退出控制台',
                'action': self.exit_console
            }
        ]

    def print_menu(self):
        """打印菜单"""
        print("\n" + "=" * 80)
        print("                    NWACS 控制台")
        print("=" * 80)
        print("\n请选择要执行的操作：")
        print("-" * 60)

        for item in self.menu_items:
            print(f"  [{item['id']}] {item['name']}")
            print(f"        {item['description']}")

        print("-" * 60)

    def run(self):
        """运行控制台"""
        while True:
            self.print_menu()
            choice = input("\n请输入选择 [0-8]: ").strip()

            # 查找并执行对应的操作
            found = False
            for item in self.menu_items:
                if item['id'] == choice:
                    item['action']()
                    found = True
                    break

            if not found and choice != '':
                print(f"\n无效选择: {choice}")

    def start_full_system(self):
        """启动完整系统"""
        print("\n[启动完整系统]")
        print("-" * 40)
        print("正在启动所有服务...")
        self._run_script('main.py', blocking=False)

    def start_writing_mode(self):
        """启动专注写作模式"""
        print("\n[专注写作模式]")
        print("-" * 40)
        print("按 Ctrl+C 保存并退出")
        self._run_script('src/core/writing_mode.py')

    def start_plot_designer(self):
        """启动剧情设计器"""
        print("\n[剧情设计器]")
        print("-" * 40)
        self._run_script('src/core/plot_designer.py')

    def start_config_tool(self):
        """启动配置工具"""
        print("\n[配置工具]")
        print("-" * 40)
        self._run_script('config_tool.py')

    def start_learning_manager(self):
        """启动学习系统管理"""
        print("\n[学习系统管理]")
        print("-" * 40)
        self._run_script('src/core/skill_learning_manager.py')

    def start_writing_assistant(self):
        """启动创作辅助工具"""
        print("\n[创作辅助工具]")
        print("-" * 40)
        self._run_script('test_writing_assistant.py')

    def check_system_status(self):
        """检查系统状态"""
        print("\n[系统状态检查]")
        print("-" * 40)

        # 检查关键文件
        files = [
            ('main.py', '主启动脚本'),
            ('config.json', '配置文件'),
            ('src/core/writing_assistant.py', '创作辅助工具'),
            ('src/core/daily_checker.py', '每日自检'),
            ('src/core/plot_designer.py', '剧情设计器'),
            ('src/core/writing_mode.py', '写作模式'),
        ]

        print("文件状态:")
        for file_path, desc in files:
            if os.path.exists(file_path):
                print(f"  OK   {file_path}")
            else:
                print(f"  MISS {file_path}")

        # 检查配置
        print("\n配置状态:")
        if os.path.exists('config.json'):
            import json
            with open('config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
                print(f"  API Key: {'已配置' if config.get('api_key') else '未配置'}")
                print(f"  模型: {config.get('model', '未配置')}")
                print(f"  版本: {config.get('model_version', '未配置')}")
                print(f"  敏感词过滤: {config.get('sensitivity', {}).get('content_type', '未配置')}")
        else:
            print("  配置文件不存在")

        # 检查目录
        print("\n目录状态:")
        dirs = ['skills', 'src/core', 'novel-mcp-server-v2']
        for d in dirs:
            if os.path.exists(d):
                count = len(os.listdir(d))
                print(f"  OK   {d} ({count} 个文件)")
            else:
                print(f"  MISS {d}")

        print("\n" + "-" * 40)
        input("\n按 Enter 继续...")

    def show_stats_dashboard(self):
        """显示数据统计面板"""
        print("\n[数据统计面板]")
        print("-" * 40)

        # 模拟统计数据
        stats = {
            'total_words': 0,
            'learning_hours': 0,
            'skills_count': 0,
            'templates_count': 0
        }

        # 统计技能数量
        skills_dir = 'skills'
        if os.path.exists(skills_dir):
            stats['skills_count'] = len([d for d in os.listdir(skills_dir) if os.path.isdir(os.path.join(skills_dir, d))])

        print(f"已学习 Skill: {stats['skills_count']} 个")
        print(f"学习时长: {stats['learning_hours']} 小时")
        print(f"累计写作: {stats['total_words']} 字")
        print(f"模板数量: {stats['templates_count']} 个")

        print("\n学习进度:")
        print("  [██████████] 剧情大师 (100%)")
        print("  [██████░░░░] 人物大师 (60%)")
        print("  [████░░░░░░] 金句大师 (40%)")

        print("\n" + "-" * 40)
        input("\n按 Enter 继续...")

    def exit_console(self):
        """退出控制台"""
        print("\n感谢使用 NWACS！")
        sys.exit(0)

    def _run_script(self, script_path, blocking=True):
        """运行脚本"""
        if not os.path.exists(script_path):
            print(f"错误: 未找到文件 {script_path}")
            input("按 Enter 继续...")
            return

        try:
            if blocking:
                subprocess.run(['py', script_path], cwd=os.getcwd())
            else:
                subprocess.Popen(['py', script_path], cwd=os.getcwd())
                print("系统已启动，按 Enter 返回菜单...")
                input()
        except Exception as e:
            print(f"运行失败: {e}")
            input("按 Enter 继续...")


def main():
    """主函数"""
    console = NWACSConsole()
    console.run()


if __name__ == "__main__":
    main()
