#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS GitHub同步模块
自动同步代码到GitHub仓库
"""

import os
import subprocess
import time
from datetime import datetime
from logger import logger

class GitHubSync:
    """GitHub同步器"""

    def __init__(self, repo_path=None):
        self.repo_path = repo_path or r"e:\Program Files (x86)\Trae CN\github\NWACS"
        self.git_path = self._find_git_path()

    def _find_git_path(self):
        """查找git可执行文件路径"""
        # 常见的git路径
        paths = [
            r"C:\Program Files\Git\bin\git.exe",
            r"C:\Program Files (x86)\Git\bin\git.exe",
            r"C:\Program Files\Git\cmd\git.exe",
            r"C:\Program Files (x86)\Git\cmd\git.exe"
        ]

        for path in paths:
            if os.path.exists(path):
                return path

        # 尝试从PATH中查找
        try:
            result = subprocess.run(['where', 'git'], capture_output=True, text=True)
            if result.returncode == 0 and result.stdout:
                return result.stdout.strip().split('\n')[0]
        except:
            pass

        return 'git'  # 希望系统能找到

    def run_git_command(self, command, cwd=None):
        """运行git命令"""
        if cwd is None:
            cwd = self.repo_path

        full_command = f'"{self.git_path}" {command}'
        
        try:
            result = subprocess.run(
                full_command,
                cwd=cwd,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace'
            )

            return {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'command': command
            }

        except Exception as e:
            return {
                'success': False,
                'stdout': '',
                'stderr': str(e),
                'command': command
            }

    def check_repo_status(self):
        """检查仓库状态"""
        logger.info("检查仓库状态...")
        
        # 检查是否在git仓库中
        result = self.run_git_command('rev-parse --is-inside-work-tree')
        if not result['success']:
            return {'error': '不在git仓库中'}

        # 获取状态
        status = self.run_git_command('status --porcelain')
        branch = self.run_git_command('rev-parse --abbrev-ref HEAD')
        remote = self.run_git_command('remote -v')

        return {
            'is_repo': True,
            'branch': branch['stdout'].strip(),
            'remote': remote['stdout'],
            'has_changes': len(status['stdout']) > 0,
            'changes': status['stdout']
        }

    def sync(self, commit_message=None):
        """执行同步"""
        logger.info("开始同步到GitHub...")

        results = []

        # 检查状态
        status = self.check_repo_status()
        if 'error' in status:
            return {'success': False, 'error': status['error']}

        if not status['has_changes']:
            return {'success': True, 'message': '没有需要同步的变更'}

        # 自动生成提交信息
        if not commit_message:
            commit_message = f"自动同步 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

        # 添加所有文件
        result = self.run_git_command('add .')
        results.append(result)
        if not result['success']:
            return {'success': False, 'error': f'add失败: {result["stderr"]}'}

        # 提交
        result = self.run_git_command(f'commit -m "{commit_message}"')
        results.append(result)
        if not result['success']:
            return {'success': False, 'error': f'commit失败: {result["stderr"]}'}

        # 拉取最新代码
        result = self.run_git_command('pull origin main --rebase')
        results.append(result)
        if not result['success']:
            logger.warning(f'pull失败: {result["stderr"]}')

        # 推送
        result = self.run_git_command('push origin main')
        results.append(result)
        if not result['success']:
            return {'success': False, 'error': f'push失败: {result["stderr"]}'}

        return {
            'success': True,
            'message': '同步完成',
            'commit_message': commit_message,
            'results': results
        }

    def backup_before_sync(self):
        """同步前备份"""
        backup_dir = os.path.join(self.repo_path, 'backup')
        os.makedirs(backup_dir, exist_ok=True)

        backup_file = os.path.join(backup_dir, f'backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.zip')

        try:
            import zipfile
            with zipfile.ZipFile(backup_file, 'w', zipfile.ZIP_DEFLATED) as zf:
                for root, dirs, files in os.walk(self.repo_path):
                    # 排除不必要的目录
                    dirs[:] = [d for d in dirs if d not in ['backup', '.git', '__pycache__']]
                    
                    for file in files:
                        if file.endswith('.pyc') or file.endswith('.pyo'):
                            continue
                        
                        filepath = os.path.join(root, file)
                        arcname = os.path.relpath(filepath, self.repo_path)
                        zf.write(filepath, arcname)

            logger.info(f"备份完成: {backup_file}")
            return backup_file

        except Exception as e:
            logger.log_exception(e, "备份")
            return None

    def setup_git_config(self, username=None, email=None):
        """设置git配置"""
        results = []

        if username:
            result = self.run_git_command(f'config user.name "{username}"')
            results.append(result)

        if email:
            result = self.run_git_command(f'config user.email "{email}"')
            results.append(result)

        return results


# 独立运行测试
if __name__ == "__main__":
    print("=====================================")
    print("    NWACS GitHub同步工具")
    print("=====================================")

    sync = GitHubSync()

    # 检查状态
    print("\n[1/4] 检查仓库状态...")
    status = sync.check_repo_status()
    
    if 'error' in status:
        print(f"错误: {status['error']}")
        exit(1)

    print(f"分支: {status['branch']}")
    print(f"有变更: {'是' if status['has_changes'] else '否'}")
    
    if status['has_changes']:
        print("\n变更内容:")
        print(status['changes'])

    # 询问是否同步
    if status['has_changes']:
        confirm = input("\n是否继续同步? (y/n): ").lower()
        if confirm != 'y':
            print("已取消同步")
            exit(0)

        # 备份
        print("\n[2/4] 创建备份...")
        backup = sync.backup_before_sync()
        if backup:
            print(f"备份文件: {backup}")

        # 同步
        print("\n[3/4] 执行同步...")
        result = sync.sync()

        print("\n[4/4] 同步结果:")
        if result['success']:
            print(f"✓ {result['message']}")
            print(f"提交信息: {result['commit_message']}")
        else:
            print(f"✗ 失败: {result.get('error', '未知错误')}")
    else:
        print("\n没有需要同步的变更")