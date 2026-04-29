#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 文件清理优化模块
检测和清理无用文件，优化文件结构
"""

import os
import json
import time
import shutil
from datetime import datetime, timedelta
from logger import logger

class FileCleanup:
    """文件清理优化器"""

    def __init__(self):
        self.base_dir = r"e:\Program Files (x86)\Trae CN\github\NWACS"
        self.cleanup_log = []
        self.dry_run = False  # 试运行模式

    def scan_project(self):
        """扫描项目文件"""
        results = {
            'total_files': 0,
            'total_size': 0,
            'file_types': {},
            'old_files': [],
            'duplicate_files': [],
            'empty_files': [],
            'backup_files': [],
            'log_files': []
        }

        for root, dirs, files in os.walk(self.base_dir):
            # 排除某些目录
            dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', 'node_modules', 'backup']]

            for filename in files:
                filepath = os.path.join(root, filename)
                results['total_files'] += 1

                try:
                    file_size = os.path.getsize(filepath)
                    results['total_size'] += file_size

                    # 按文件类型统计
                    ext = os.path.splitext(filename)[1].lower() or 'no_ext'
                    results['file_types'][ext] = results['file_types'].get(ext, 0) + 1

                    # 检查空文件
                    if file_size == 0:
                        results['empty_files'].append(filepath)

                    # 检查旧文件（超过30天）
                    mtime = os.path.getmtime(filepath)
                    if datetime.now() - datetime.fromtimestamp(mtime) > timedelta(days=30):
                        results['old_files'].append({
                            'path': filepath,
                            'age_days': (datetime.now() - datetime.fromtimestamp(mtime)).days,
                            'size': file_size
                        })

                    # 检查备份文件
                    if 'backup' in filename.lower() or filename.endswith('.bak'):
                        results['backup_files'].append(filepath)

                    # 检查日志文件
                    if filename.endswith('.log') or filename.endswith('.txt'):
                        results['log_files'].append(filepath)

                except Exception as e:
                    logger.log_exception(e, f"扫描文件 {filepath}")

        # 检查重复文件
        results['duplicate_files'] = self._find_duplicates()

        return results

    def _find_duplicates(self):
        """查找重复文件（基于文件名）"""
        duplicates = {}

        for root, dirs, files in os.walk(self.base_dir):
            dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__']]

            for filename in files:
                # 忽略临时文件
                if filename.startswith('~') or filename.startswith('.'):
                    continue

                key = filename.lower()
                if key not in duplicates:
                    duplicates[key] = []
                duplicates[key].append(os.path.join(root, filename))

        # 只返回有重复的文件
        return {k: v for k, v in duplicates.items() if len(v) > 1}

    def analyze_skill_files(self):
        """分析Skill文件"""
        skill_dir = os.path.join(self.base_dir, 'skills', 'level2')
        results = {
            'skill_count': 0,
            'total_size': 0,
            'issues': []
        }

        if not os.path.exists(skill_dir):
            results['issues'].append({'error': 'Skill目录不存在'})
            return results

        md_files = [f for f in os.listdir(skill_dir) if f.endswith('.md')]
        results['skill_count'] = len(md_files)

        for filename in md_files:
            filepath = os.path.join(skill_dir, filename)

            try:
                file_size = os.path.getsize(filepath)
                results['total_size'] += file_size

                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 检查必要内容
                if '---' not in content[:50]:
                    results['issues'].append({
                        'file': filename,
                        'issue': '缺少YAML元数据标记',
                        'severity': 'warning'
                    })

                if 'Skill名称' not in content:
                    results['issues'].append({
                        'file': filename,
                        'issue': '缺少Skill名称',
                        'severity': 'warning'
                    })

                # 检查学习标记
                if '学习成果自动插入' not in content:
                    results['issues'].append({
                        'file': filename,
                        'issue': '缺少学习标记',
                        'severity': 'info'
                    })

            except Exception as e:
                results['issues'].append({
                    'file': filename,
                    'issue': f'读取失败: {e}',
                    'severity': 'error'
                })

        return results

    def clean_up(self, options=None):
        """执行清理操作"""
        if options is None:
            options = {
                'remove_empty_files': True,
                'remove_old_backups': True,
                'remove_old_logs': True,
                'remove_duplicates': False,  # 默认不删除重复文件
                'backup_before_clean': True
            }

        self.cleanup_log = []
        cleaned_count = 0
        freed_space = 0

        # 备份
        if options['backup_before_clean']:
            backup_path = self._create_backup()
            if backup_path:
                self.cleanup_log.append(f"已创建备份: {backup_path}")

        # 删除空文件
        if options['remove_empty_files']:
            scan_result = self.scan_project()
            for filepath in scan_result['empty_files']:
                if self._delete_file(filepath):
                    cleaned_count += 1
                    freed_space += os.path.getsize(filepath)

        # 删除旧备份文件（超过7天）
        if options['remove_old_backups']:
            backup_dir = os.path.join(self.base_dir, 'backup')
            if os.path.exists(backup_dir):
                for filename in os.listdir(backup_dir):
                    filepath = os.path.join(backup_dir, filename)
                    mtime = os.path.getmtime(filepath)
                    if datetime.now() - datetime.fromtimestamp(mtime) > timedelta(days=7):
                        if self._delete_file(filepath):
                            cleaned_count += 1
                            freed_space += os.path.getsize(filepath)

        # 删除旧日志文件（超过7天）
        if options['remove_old_logs']:
            scan_result = self.scan_project()
            for filepath in scan_result['log_files']:
                try:
                    mtime = os.path.getmtime(filepath)
                    if datetime.now() - datetime.fromtimestamp(mtime) > timedelta(days=7):
                        if self._delete_file(filepath):
                            cleaned_count += 1
                            freed_space += os.path.getsize(filepath)
                except:
                    pass

        return {
            'cleaned_count': cleaned_count,
            'freed_space_bytes': freed_space,
            'freed_space_human': self._format_size(freed_space),
            'log': self.cleanup_log
        }

    def _delete_file(self, filepath):
        """删除文件"""
        try:
            if self.dry_run:
                self.cleanup_log.append(f"[模拟删除] {filepath}")
                return True

            os.remove(filepath)
            self.cleanup_log.append(f"已删除: {filepath}")
            return True
        except Exception as e:
            self.cleanup_log.append(f"删除失败 {filepath}: {e}")
            return False

    def _create_backup(self):
        """创建备份"""
        backup_dir = os.path.join(self.base_dir, 'backup')
        os.makedirs(backup_dir, exist_ok=True)

        backup_name = f"cleanup_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        backup_path = os.path.join(backup_dir, backup_name)

        try:
            import zipfile
            ignore_list = ['backup', '.git', '__pycache__', 'node_modules']

            with zipfile.ZipFile(f"{backup_path}.zip", 'w', zipfile.ZIP_DEFLATED) as zf:
                for root, dirs, files in os.walk(self.base_dir):
                    dirs[:] = [d for d in dirs if d not in ignore_list]
                    for file in files:
                        if file.endswith(('.pyc', '.pyo')):
                            continue
                        filepath = os.path.join(root, file)
                        arcname = os.path.relpath(filepath, self.base_dir)
                        zf.write(filepath, arcname)

            return f"{backup_path}.zip"
        except Exception as e:
            logger.log_exception(e, "创建备份")
            return None

    def _format_size(self, bytes_size):
        """格式化文件大小"""
        if bytes_size < 1024:
            return f"{bytes_size} B"
        elif bytes_size < 1024 * 1024:
            return f"{bytes_size / 1024:.2f} KB"
        else:
            return f"{bytes_size / (1024 * 1024):.2f} MB"

    def generate_report(self):
        """生成完整报告"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'project_scan': self.scan_project(),
            'skill_analysis': self.analyze_skill_files()
        }
        return report

    def print_report(self, report):
        """打印报告"""
        print("=" * 60)
        print("          NWACS 文件清理优化报告")
        print("=" * 60)
        print(f"生成时间: {report['timestamp']}")
        print()

        # 项目扫描摘要
        scan = report['project_scan']
        print("【项目概览】")
        print(f"  文件总数: {scan['total_files']}")
        print(f"  总大小: {self._format_size(scan['total_size'])}")
        print()

        # 文件类型分布
        print("【文件类型分布】")
        for ext, count in sorted(scan['file_types'].items(), key=lambda x: -x[1]):
            print(f"  {ext}: {count} 个")
        print()

        # 问题文件
        print("【问题文件】")

        if scan['empty_files']:
            print(f"  空文件 ({len(scan['empty_files'])}个):")
            for f in scan['empty_files'][:5]:
                print(f"    - {os.path.basename(f)}")

        if scan['old_files']:
            print(f"\n  旧文件 (>30天, {len(scan['old_files'])}个):")
            for f in scan['old_files'][:5]:
                print(f"    - {os.path.basename(f['path'])} ({f['age_days']}天)")

        if scan['duplicate_files']:
            print(f"\n  重复文件 ({len(scan['duplicate_files'])}组):")
            for name, paths in list(scan['duplicate_files'].items())[:3]:
                print(f"    - {name}: {len(paths)}个副本")

        # Skill分析
        skill = report['skill_analysis']
        print("\n【Skill分析】")
        print(f"  Skill数量: {skill['skill_count']}")
        print(f"  总大小: {self._format_size(skill['total_size'])}")

        if skill['issues']:
            print(f"\n  发现问题 ({len(skill['issues'])}个):")
            for issue in skill['issues'][:5]:
                severity = issue.get('severity', 'info').upper()
                print(f"    [{severity}] {issue.get('file', '')}: {issue.get('issue', '')}")

        print("\n" + "=" * 60)


# 独立运行测试
if __name__ == "__main__":
    print("=====================================")
    print("    NWACS 文件清理优化工具")
    print("=====================================")

    cleaner = FileCleanup()

    # 生成报告
    print("\n[1/2] 正在扫描项目...")
    report = cleaner.generate_report()
    cleaner.print_report(report)

    # 询问是否清理
    confirm = input("\n是否执行清理操作? (y/n): ").lower()
    if confirm == 'y':
        print("\n[2/2] 正在执行清理...")
        result = cleaner.clean_up()

        print("\n清理结果:")
        print(f"  删除文件数: {result['cleaned_count']}")
        print(f"  释放空间: {result['freed_space_human']}")
        print("\n清理日志:")
        for log in result['log']:
            print(f"  - {log}")
    else:
        print("已取消清理")