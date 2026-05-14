#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS Daily Checker
功能：每日自动自检 Skill 状态、文件清理、GitHub 同步
"""

import os
import sys
import time
import json
import shutil
from datetime import datetime, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from logger import logger

class DailyChecker:
    """每日检查器"""

    def __init__(self):
        self.last_check = None
        self.check_interval = 24 * 60 * 60  # 24小时
        self.running = False

        # 加载配置
        self.config = self._load_config()

    def _load_config(self):
        """加载配置"""
        config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config.json')
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            'auto_sync': True,
            'file_cleanup': True,
            'skill_check': True
        }

    def start(self):
        """启动检查器"""
        if self.running:
            logger.info("Daily Checker already running")
            return

        self.running = True
        logger.info("Daily Checker started")

        # 检查是否需要立即执行
        self._check_and_execute()

        # 启动后台检查循环
        self._run_loop()

    def _run_loop(self):
        """运行检查循环"""
        while self.running:
            try:
                time.sleep(3600)  # 每小时检查一次
                self._check_and_execute()
            except Exception as e:
                logger.error(f"Daily Checker error: {e}")
                logger.log_exception(e, "Daily Checker")

    def _check_and_execute(self):
        """检查并执行"""
        now = datetime.now()

        # 检查是否到了执行时间
        if self.last_check is None:
            # 首次运行，执行检查
            self._execute_daily_check()
            self.last_check = now
        else:
            # 检查是否超过24小时
            elapsed = (now - self.last_check).total_seconds()
            if elapsed >= self.check_interval:
                self._execute_daily_check()
                self.last_check = now

    def _execute_daily_check(self):
        """执行每日检查"""
        logger.info("=" * 60)
        logger.info("开始每日自检...")
        print("\n" + "=" * 60)
        print("       NWACS 每日自检")
        print("=" * 60)

        # 1. Skill 体检
        if self.config.get('skill_check', True):
            self._check_skills()

        # 2. 文件清理
        if self.config.get('file_cleanup', True):
            self._cleanup_files()

        # 3. GitHub 同步
        if self.config.get('auto_sync', True):
            self._sync_github()

        logger.info("每日自检完成")
        print("\n" + "-" * 60)
        print("自检完成！按 Ctrl+C 停止系统")
        print("-" * 60)

    def _check_skills(self):
        """检查所有 Skill"""
        print("\n[1/3] Skill 体检")
        print("-" * 40)

        skills_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'skills')
        if not os.path.exists(skills_dir):
            print("  SKILLS 目录不存在，跳过")
            logger.warning("SKILLS directory not found")
            return

        skill_count = 0
        healthy_count = 0

        for item in os.listdir(skills_dir):
            item_path = os.path.join(skills_dir, item)
            if os.path.isdir(item_path):
                skill_count += 1
                # 检查必要文件
                skill_file = os.path.join(item_path, f"{item}.md")
                if os.path.exists(skill_file):
                    healthy_count += 1
                    print(f"  OK - {item}")
                else:
                    print(f"  WARN - {item} (缺少主文件)")

        print(f"  总结: {healthy_count}/{skill_count} 个 Skill 正常")

    def _cleanup_files(self):
        """清理文件"""
        print("\n[2/3] 文件清理")
        print("-" * 40)

        cleaned = 0
        cleaned_size = 0

        # 清理空文件
        cleaned += self._clean_empty_files()
        # 清理旧日志
        cleaned += self._clean_old_logs()
        # 清理临时文件
        cleaned += self._clean_temp_files()

        print(f"  清理完成: {cleaned} 个文件")

    def _clean_empty_files(self):
        """清理空文件"""
        count = 0
        base_dir = os.path.dirname(__file__)
        for root, dirs, files in os.walk(base_dir):
            # 跳过必要目录
            if 'skills' in root or '.git' in root:
                continue
            for file in files:
                if file.endswith(('.log', '.tmp', '.bak')):
                    file_path = os.path.join(root, file)
                    if os.path.getsize(file_path) == 0:
                        os.remove(file_path)
                        count += 1
        return count

    def _clean_old_logs(self):
        """清理旧日志"""
        count = 0
        log_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'logs')
        if not os.path.exists(log_dir):
            return 0

        cutoff = datetime.now() - timedelta(days=30)
        for file in os.listdir(log_dir):
            if file.endswith('.log'):
                file_path = os.path.join(log_dir, file)
                mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                if mtime < cutoff:
                    os.remove(file_path)
                    count += 1
        return count

    def _clean_temp_files(self):
        """清理临时文件"""
        count = 0
        base_dir = os.path.dirname(__file__)
        for root, dirs, files in os.walk(base_dir):
            for file in files:
                if file.endswith('.tmp') or file.startswith('.'):
                    try:
                        os.remove(os.path.join(root, file))
                        count += 1
                    except:
                        pass
        return count

    def _sync_github(self):
        """同步到 GitHub"""
        print("\n[3/3] GitHub 同步")
        print("-" * 40)

        try:
            # 检查 git 是否可用
            import subprocess
            result = subprocess.run(['git', 'status'], capture_output=True, text=True)

            if result.returncode == 0:
                print("  OK - Git 仓库正常")
                print("  INFO - 自动同步已禁用，请手动执行 git push")
                logger.info("GitHub sync check completed")
            else:
                print("  WARN - Git 仓库不可用")

        except FileNotFoundError:
            print("  WARN - Git 未安装")
        except Exception as e:
            print(f"  ERROR - 同步失败: {e}")
            logger.log_exception(e, "GitHub sync")

    def stop(self):
        """停止检查器"""
        self.running = False
        logger.info("Daily Checker stopped")


if __name__ == "__main__":
    checker = DailyChecker()
    try:
        checker.start()
    except KeyboardInterrupt:
        print("\n\n正在停止 Daily Checker...")
        checker.stop()
        print("已停止")