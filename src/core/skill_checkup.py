#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS Skill体检模块
检查Skill状态、协作流畅度和优化建议
"""

import os
import json
import time
from datetime import datetime
from logger import logger

class SkillCheckup:
    """Skill体检器"""

    def __init__(self):
        # 使用相对路径，兼容不同机器
        self.skills_dir = os.path.abspath(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'skills', 'level2')
        )
        self.check_results = {}

    def check_all_skills(self):
        """检查所有Skill"""
        logger.info("开始Skill体检...")
        self.check_results = {}

        # 检查文件完整性
        file_check = self._check_file_integrity()

        # 检查学习标记
        marker_check = self._check_learning_markers()

        # 检查协作关系
        collaboration_check = self._check_collaboration()

        # 检查知识库状态
        kb_check = self._check_knowledge_base()

        # 生成综合报告
        report = self._generate_report([
            file_check,
            marker_check,
            collaboration_check,
            kb_check
        ])

        return report

    def _check_file_integrity(self):
        """检查文件完整性"""
        results = {
            'name': '文件完整性检查',
            'status': 'pass',
            'items': []
        }

        try:
            md_files = [f for f in os.listdir(self.skills_dir) if f.endswith('.md')]

            for filename in md_files:
                filepath = os.path.join(self.skills_dir, filename)
                file_size = os.path.getsize(filepath)

                # 检查文件大小
                if file_size < 100:
                    results['items'].append({
                        'skill': filename.replace('.md', ''),
                        'issue': '文件内容过少',
                        'severity': 'warning',
                        'suggestion': '请补充Skill内容'
                    })
                    if results['status'] != 'error':
                        results['status'] = 'warning'
                elif file_size > 1000000:
                    results['items'].append({
                        'skill': filename.replace('.md', ''),
                        'issue': '文件过大',
                        'severity': 'info',
                        'suggestion': '建议拆分或优化内容结构'
                    })

            if not results['items']:
                results['items'].append({'message': '所有文件完整性检查通过'})

        except Exception as e:
            results['status'] = 'error'
            results['items'].append({'error': str(e)})

        return results

    def _check_learning_markers(self):
        """检查学习标记"""
        results = {
            'name': '学习标记检查',
            'status': 'pass',
            'items': []
        }

        try:
            md_files = [f for f in os.listdir(self.skills_dir) if f.endswith('.md')]
            missing_count = 0

            for filename in md_files:
                filepath = os.path.join(self.skills_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                if '学习成果自动插入' not in content:
                    results['items'].append({
                        'skill': filename.replace('.md', ''),
                        'issue': '缺少学习标记',
                        'severity': 'warning',
                        'suggestion': '运行"添加学习标记.bat"添加标记'
                    })
                    missing_count += 1

            if missing_count > 0:
                results['status'] = 'warning'
            else:
                results['items'].append({'message': '所有学习标记检查通过'})

        except Exception as e:
            results['status'] = 'error'
            results['items'].append({'error': str(e)})

        return results

    def _check_collaboration(self):
        """检查协作关系"""
        results = {
            'name': '协作关系检查',
            'status': 'pass',
            'items': []
        }

        # 定义期望的协作关系
        expected_relations = {
            '短篇小说爽文大师': ['写作技巧大师', '剧情构造师', '角色塑造师'],
            '写作技巧大师': ['剧情构造师', '角色塑造师', '去AI痕迹监督官'],
            '剧情构造师': ['写作技巧大师', '战斗设计师', '场景构造师'],
            '角色塑造师': ['对话设计师', '写作技巧大师', '世界观构造师'],
            '战斗设计师': ['剧情构造师', '场景构造师', '规则掌控者'],
        }

        try:
            # 检查协作模块
            collab_file = os.path.join(os.path.dirname(__file__), 'skill_collaboration.py')
            if not os.path.exists(collab_file):
                results['items'].append({
                    'issue': '协作模块不存在',
                    'severity': 'error',
                    'suggestion': '请创建skill_collaboration.py'
                })
                results['status'] = 'error'
            else:
                results['items'].append({'message': '协作模块已就绪'})

            # 检查学习管理器集成
            manager_file = os.path.join(os.path.dirname(__file__), 'skill_learning_manager.py')
            if os.path.exists(manager_file):
                with open(manager_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                if 'collaborative_learn' in content:
                    results['items'].append({'message': '协作学习方法已集成'})
                else:
                    results['items'].append({
                        'issue': '缺少协作学习方法',
                        'severity': 'warning',
                        'suggestion': '更新skill_learning_manager.py'
                    })

        except Exception as e:
            results['status'] = 'error'
            results['items'].append({'error': str(e)})

        return results

    def _check_knowledge_base(self):
        """检查知识库状态"""
        results = {
            'name': '知识库检查',
            'status': 'pass',
            'items': []
        }

        kb_file = 'skill_knowledge_base.json'

        try:
            if os.path.exists(kb_file):
                file_size = os.path.getsize(kb_file)

                with open(kb_file, 'r', encoding='utf-8') as f:
                    try:
                        kb_data = json.load(f)
                        item_count = len(kb_data)

                        if item_count == 0:
                            results['items'].append({
                                'issue': '知识库为空',
                                'severity': 'info',
                                'suggestion': '运行学习系统填充知识库'
                            })
                        else:
                            results['items'].append({
                                'message': f'知识库包含 {item_count} 条知识'
                            })

                    except json.JSONDecodeError:
                        results['items'].append({
                            'issue': '知识库格式错误',
                            'severity': 'error',
                            'suggestion': '修复或重建知识库文件'
                        })
                        results['status'] = 'error'
            else:
                results['items'].append({
                    'issue': '知识库文件不存在',
                    'severity': 'info',
                    'suggestion': '运行学习系统将自动创建'
                })

        except Exception as e:
            results['status'] = 'error'
            results['items'].append({'error': str(e)})

        return results

    def _generate_report(self, checks):
        """生成综合报告"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'overall_status': 'pass',
            'checks': checks,
            'summary': {
                'passed': 0,
                'warning': 0,
                'error': 0,
                'total': len(checks)
            },
            'suggestions': []
        }

        for check in checks:
            status = check['status']
            if status == 'pass':
                report['summary']['passed'] += 1
            elif status == 'warning':
                report['summary']['warning'] += 1
            elif status == 'error':
                report['summary']['error'] += 1

            # 收集建议
            for item in check.get('items', []):
                if 'suggestion' in item:
                    report['suggestions'].append(item['suggestion'])

        # 确定总体状态
        if report['summary']['error'] > 0:
            report['overall_status'] = 'error'
        elif report['summary']['warning'] > 0:
            report['overall_status'] = 'warning'

        return report

    def print_report(self, report):
        """打印报告"""
        print("=" * 60)
        print("          NWACS Skill体检报告")
        print("=" * 60)
        print(f"检查时间: {report['timestamp']}")
        print(f"总体状态: {report['overall_status'].upper()}")
        print()

        for check in report['checks']:
            print(f"【{check['name']}】")
            print(f"  状态: {check['status']}")

            for item in check.get('items', []):
                if 'message' in item:
                    print(f"    ✓ {item['message']}")
                elif 'issue' in item:
                    severity = item.get('severity', 'info').upper()
                    print(f"    ✗ [{severity}] {item['issue']}")
                    if 'suggestion' in item:
                        print(f"      建议: {item['suggestion']}")
                elif 'error' in item:
                    print(f"    ✗ 错误: {item['error']}")
            print()

        print("【优化建议】")
        for i, suggestion in enumerate(report['suggestions'], 1):
            print(f"  {i}. {suggestion}")

        print("\n" + "=" * 60)

    def export_report(self, report, filename=None):
        """导出报告到文件"""
        if not filename:
            filename = f"skill_checkup_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        logger.info(f"体检报告已导出: {filename}")
        return filename


# 独立运行测试
if __name__ == "__main__":
    print("=====================================")
    print("    NWACS Skill体检工具")
    print("=====================================")

    checkup = SkillCheckup()
    report = checkup.check_all_skills()
    checkup.print_report(report)
    checkup.export_report(report)