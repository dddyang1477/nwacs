#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 主系统入口
整合所有功能模块，支持每日自动自检
"""

import os
import sys
import time
import threading
from datetime import datetime, timedelta

# 添加src/core到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logger import logger

class DailyChecker:
    """每日自检器"""

    def __init__(self):
        self.last_check_time = None
        self.check_interval = timedelta(hours=24)  # 每日检查
        self.check_thread = None
        self.running = False

    def needs_check(self):
        """检查是否需要执行每日自检"""
        if self.last_check_time is None:
            return True
        return datetime.now() - self.last_check_time >= self.check_interval

    def run_daily_check(self):
        """执行每日自检"""
        if not self.needs_check():
            return

        logger.info("开始每日自检...")
        self.last_check_time = datetime.now()

        # 1. Skill体检
        try:
            from skill_checkup import SkillCheckup
            checkup = SkillCheckup()
            report = checkup.check_all_skills()
            checkup.export_report(report)
            logger.info("Skill体检完成")
        except Exception as e:
            logger.log_exception(e, "每日Skill体检")

        # 2. 文件清理优化
        try:
            from file_cleanup import FileCleanup
            cleaner = FileCleanup()
            cleaner.dry_run = False  # 设为True可只扫描不删除
            result = cleaner.clean_up()
            logger.info(f"文件清理完成: 删除 {result['cleaned_count']} 个文件，释放 {result['freed_space_human']}")
        except Exception as e:
            logger.log_exception(e, "每日文件清理")

        logger.info("每日自检完成")

    def check_loop(self):
        """检查循环"""
        while self.running:
            if self.needs_check():
                self.run_daily_check()
            time.sleep(3600)  # 每小时检查一次是否需要执行每日自检

    def start(self):
        """启动每日检查"""
        self.running = True
        self.check_thread = threading.Thread(target=self.check_loop)
        self.check_thread.daemon = True
        self.check_thread.start()
        logger.info("每日自检器已启动")

    def stop(self):
        """停止每日检查"""
        self.running = False
        if self.check_thread:
            self.check_thread.join()


def main():
    print("=" * 60)
    print("          NWACS 小说创作系统 v2.1")
    print("=" * 60)
    print(f"启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # 初始化每日自检器
    daily_checker = DailyChecker()
    daily_checker.start()

    # 1. 执行启动时自检
    print("[1/5] 执行启动自检...")
    try:
        daily_checker.run_daily_check()
        print("     ✓ 启动自检完成")
    except Exception as e:
        print(f"     ✗ 启动自检失败: {e}")

    # 2. 初始化空闲检测学习
    print("\n[2/5] 初始化空闲检测学习系统...")
    scheduler = None
    try:
        from idle_learning import get_auto_scheduler
        scheduler = get_auto_scheduler()
        scheduler.start()
        print("     ✓ 空闲检测学习系统已启动")
        print("     ✓ 空闲阈值: 10分钟")
    except Exception as e:
        print(f"     ✗ 空闲检测学习系统初始化失败: {e}")

    # 3. 初始化大模型创作接口
    print("\n[3/5] 初始化大模型创作接口...")
    try:
        from llm_writer import get_llm_writer
        
        # 检查API密钥（配置文件和环境变量）
        import json
        config_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config.json')
        config = {}
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
        
        config_key = config.get('api_key', '').strip()
        env_key = os.environ.get('OPENAI_API_KEY') or os.environ.get('DEEPSEEK_API_KEY')
        api_key_set = bool(config_key or env_key)
        
        if api_key_set:
            choice = input("     检测到API密钥，是否启用大模型? (y/n): ").lower()
            enable_llm = choice == 'y' or choice == ''
        else:
            choice = input("     未检测到API密钥，是否尝试启用大模型? (y/n): ").lower()
            enable_llm = choice == 'y'
        
        if enable_llm:
            llm_writer = get_llm_writer()
            llm_writer.load_skill_knowledge()
            if llm_writer.enabled:
                print("     ✓ 大模型创作接口已启动")
                print("     ✓ 知识库已加载")
            else:
                print("     ! 大模型启动失败（API密钥可能无效）")
        else:
            print("     ✓ 已跳过大模型（可后续手动启用）")
    except Exception as e:
        print(f"     ✗ 大模型创作接口初始化失败: {e}")

    # 4. 初始化协作模块
    print("\n[4/5] 初始化Skill协作模块...")
    try:
        from skill_collaboration import get_skill_collaboration
        collab = get_skill_collaboration()
        print("     ✓ Skill协作模块已启动")
        print(f"     ✓ 大模型分析: {'已启用' if collab.llm_enabled else '未启用'}")
    except Exception as e:
        print(f"     ✗ 协作模块初始化失败: {e}")

    # 5. 文件清理优化
    print("\n[5/5] 检查文件清理优化...")
    try:
        from file_cleanup import FileCleanup
        cleaner = FileCleanup()
        report = cleaner.generate_report()
        print(f"     ✓ 项目文件: {report['project_scan']['total_files']} 个")
        print(f"     ✓ 项目大小: {cleaner._format_size(report['project_scan']['total_size'])}")
        print(f"     ✓ Skill数量: {report['skill_analysis']['skill_count']} 个")
    except Exception as e:
        print(f"     ✗ 文件检查失败: {e}")

    print("\n" + "=" * 60)
    print("    系统启动完成！")
    print("    空闲10分钟后自动开始学习")
    print("    每日自动执行系统自检")
    print("    按 Ctrl+C 退出")
    print("=" * 60)
    print()

    # 保持运行
    try:
        while True:
            time.sleep(60)
            # 每分钟检查一次状态
            if scheduler:
                idle_time = scheduler.idle_monitor.get_idle_time()
                status = "空闲" if scheduler.idle_monitor.is_idle else "活跃"
                print(f"\r[{datetime.now().strftime('%H:%M:%S')}] 系统运行中 | 空闲时间: {int(idle_time)}秒 | 状态: {status}", end="")
    except KeyboardInterrupt:
        print("\n\n正在关闭系统...")
        if scheduler:
            scheduler.stop()
        daily_checker.stop()
        print("系统已停止")


if __name__ == "__main__":
    main()