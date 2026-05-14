#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS GitHub 同步增强模块
功能：重试机制、网络检测、异步同步、失败备份
"""

import os
import time
import subprocess
import threading
import socket
from datetime import datetime
from logger import logger

class GitHubSyncEnhancer:
    """GitHub 同步增强器"""
    
    def __init__(self):
        self.max_retries = 3
        self.retry_delay = 5  # 秒
        self.timeout = 30  # 超时时间（秒）
        self.backup_dir = "git_backup"
        self.sync_history = []
        self.history_file = "git_sync_history.json"
        
        # 网络检测配置
        self.test_hosts = [
            ('github.com', 443),
            ('gitee.com', 443),
            ('8.8.8.8', 53)
        ]
        
        self._load_history()
    
    def _load_history(self):
        """加载同步历史"""
        import json
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.sync_history = json.load(f)
            except Exception:
                self.sync_history = []
    
    def _save_history(self):
        """保存同步历史"""
        import json
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.sync_history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.log_exception(e, "保存同步历史")
    
    def check_network(self):
        """检查网络连接"""
        logger.info("正在检查网络连接...")
        
        for host, port in self.test_hosts:
            try:
                socket.setdefaulttimeout(3)
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                result = sock.connect_ex((host, port))
                sock.close()
                
                if result == 0:
                    logger.info("网络正常：可访问 %s:%d" % (host, port))
                    return True
            except Exception:
                continue
        
        logger.warning("网络连接失败，无法访问 GitHub")
        return False
    
    def create_backup(self):
        """创建本地备份"""
        try:
            import zipfile
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = "nwacs_backup_%s.zip" % timestamp
            
            if not os.path.exists(self.backup_dir):
                os.makedirs(self.backup_dir)
            
            backup_path = os.path.join(self.backup_dir, backup_name)
            
            # 创建压缩文件
            with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # 添加重要文件
                important_files = [
                    'src/',
                    'skills/',
                    'config.json',
                    'main.py'
                ]
                
                for file_path in important_files:
                    if os.path.exists(file_path):
                        if os.path.isdir(file_path):
                            for root, dirs, files in os.walk(file_path):
                                for file in files:
                                    full_path = os.path.join(root, file)
                                    arcname = os.path.relpath(full_path, '.')
                                    zipf.write(full_path, arcname)
                        else:
                            zipf.write(file_path, os.path.basename(file_path))
            
            logger.info("已创建备份：%s" % backup_path)
            return backup_path
            
        except Exception as e:
            logger.log_exception(e, "创建备份")
            return None
    
    def execute_git_command(self, command, cwd='.'):
        """执行 Git 命令（带重试）"""
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                # 检查网络
                if attempt > 0 and not self.check_network():
                    logger.warning("网络不可用，等待重试...")
                    time.sleep(self.retry_delay * (attempt + 1))
                    continue
                
                logger.info("执行 Git 命令（第 %d 次尝试）: %s" % (attempt + 1, command))
                
                # 执行命令
                result = subprocess.run(
                    command,
                    shell=True,
                    cwd=cwd,
                    capture_output=True,
                    text=True,
                    timeout=self.timeout
                )
                
                if result.returncode == 0:
                    logger.info("Git 命令执行成功")
                    if result.stdout:
                        logger.debug("输出：%s" % result.stdout)
                    return True
                else:
                    logger.warning("Git 命令失败：%s" % result.stderr)
                    last_error = result.stderr
                    
            except subprocess.TimeoutExpired:
                logger.warning("Git 命令超时（%d 秒）" % self.timeout)
                last_error = "Timeout"
                
            except Exception as e:
                logger.log_exception(e, "执行 Git 命令")
                last_error = str(e)
            
            # 等待后重试
            if attempt < self.max_retries - 1:
                wait_time = self.retry_delay * (2 ** attempt)  # 指数退避
                logger.info("等待 %d 秒后重试..." % wait_time)
                time.sleep(wait_time)
        
        logger.error("所有重试失败：%s" % last_error)
        return False
    
    def sync_to_github(self, commit_message="Auto sync"):
        """同步到 GitHub（增强版）"""
        logger.info("=" * 60)
        logger.info("开始同步到 GitHub")
        logger.info("=" * 60)
        
        # 1. 检查网络
        if not self.check_network():
            logger.error("网络不可用，无法同步到 GitHub")
            # 创建备份
            backup_path = self.create_backup()
            self._record_sync('failed', 'network_error', backup_path)
            return False
        
        # 2. 检查 Git 仓库
        if not os.path.exists('.git'):
            logger.error("当前目录不是 Git 仓库")
            return False
        
        # 3. 添加文件
        if not self.execute_git_command("git add -A"):
            logger.error("添加文件失败")
            self._record_sync('failed', 'add_failed')
            return False
        
        # 4. 提交更改
        commit_cmd = 'git commit -m "%s"' % commit_message
        if not self.execute_git_command(commit_cmd):
            logger.info("没有需要提交的更改")
        
        # 5. 推送远程
        if not self.execute_git_command("git push origin main"):
            # 尝试备用分支名
            if not self.execute_git_command("git push origin master"):
                logger.error("推送到远程仓库失败")
                self._record_sync('failed', 'push_failed')
                # 创建备份
                backup_path = self.create_backup()
                logger.info("已创建本地备份：%s" % backup_path)
                return False
        
        # 6. 记录成功
        self._record_sync('success', 'completed')
        logger.info("GitHub 同步完成！")
        return True
    
    def _record_sync(self, status, message, backup_path=None):
        """记录同步历史"""
        record = {
            'timestamp': datetime.now().isoformat(),
            'status': status,
            'message': message,
            'backup_path': backup_path
        }
        
        self.sync_history.append(record)
        
        # 保持历史记录数量
        if len(self.sync_history) > 100:
            self.sync_history = self.sync_history[-100:]
        
        self._save_history()
    
    def async_sync(self, commit_message="Auto sync"):
        """异步同步（不阻塞主流程）"""
        def sync_thread():
            try:
                result = self.sync_to_github(commit_message)
                if result:
                    logger.info("异步同步成功")
                else:
                    logger.warning("异步同步失败")
            except Exception as e:
                logger.log_exception(e, "异步同步")
        
        thread = threading.Thread(target=sync_thread)
        thread.daemon = True
        thread.start()
        
        logger.info("已启动异步同步线程")
        return thread
    
    def get_sync_status(self):
        """获取同步状态"""
        if not self.sync_history:
            return {'message': '暂无同步记录'}
        
        last_sync = self.sync_history[-1]
        
        return {
            'last_sync': last_sync['timestamp'],
            'status': last_sync['status'],
            'message': last_sync['message'],
            'total_syncs': len(self.sync_history),
            'success_count': len([r for r in self.sync_history if r['status'] == 'success']),
            'failed_count': len([r for r in self.sync_history if r['status'] == 'failed'])
        }
    
    def cleanup_old_backups(self, keep_days=7):
        """清理旧备份"""
        try:
            import os
            import time
            
            if not os.path.exists(self.backup_dir):
                return
            
            current_time = time.time()
            keep_seconds = keep_days * 86400
            
            for filename in os.listdir(self.backup_dir):
                filepath = os.path.join(self.backup_dir, filename)
                
                # 获取文件修改时间
                file_time = os.path.getmtime(filepath)
                
                # 删除超过保留期限的文件
                if current_time - file_time > keep_seconds:
                    os.remove(filepath)
                    logger.info("已删除旧备份：%s" % filename)
            
            logger.info("备份清理完成")
            
        except Exception as e:
            logger.log_exception(e, "清理旧备份")


# 全局同步增强器实例
sync_enhancer = GitHubSyncEnhancer()


def get_sync_enhancer():
    """获取同步增强器实例"""
    return sync_enhancer


def sync_to_github(commit_message="Auto sync"):
    """便捷同步函数"""
    enhancer = get_sync_enhancer()
    return enhancer.sync_to_github(commit_message)
