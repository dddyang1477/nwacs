"""
NWACS 真相文件管理系统
基于 InkOS 7 真相文件架构深度优化
维护小说的唯一事实来源，防止AI幻觉和前后矛盾

7 个真相文件：
1. current_state.md    - 世界状态：角色位置、关系网络、已知信息
2. particle_ledger.md  - 资源账本：物品、金钱、物资数量及衰减
3. pending_hooks.md    - 未闭合伏笔：铺垫、对读者的承诺、未解决冲突
4. chapter_summaries.md - 各章摘要：出场人物、关键事件、状态变化
5. subplot_board.md    - 支线进度板：A/B/C 线状态、停滞检测
6. emotional_arcs.md   - 情感弧线：按角色追踪情绪变化和成长
7. character_matrix.md - 角色交互矩阵：相遇记录、信息边界
"""

import json
import os
import re
import time
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path


TRUTH_FILES = {
    'current_state': 'current_state.md',
    'particle_ledger': 'particle_ledger.md',
    'pending_hooks': 'pending_hooks.md',
    'chapter_summaries': 'chapter_summaries.md',
    'subplot_board': 'subplot_board.md',
    'emotional_arcs': 'emotional_arcs.md',
    'character_matrix': 'character_matrix.md',
}


class TruthFileManager:
    def __init__(self, project_root: str = None):
        self.project_root = project_root or os.getcwd()
        self.truth_dir = os.path.join(self.project_root, 'truth_files')
        os.makedirs(self.truth_dir, exist_ok=True)

    def _path(self, name: str) -> str:
        return os.path.join(self.truth_dir, TRUTH_FILES.get(name, f'{name}.md'))

    def get_all_status(self) -> Dict[str, Any]:
        status = {}
        for key, filename in TRUTH_FILES.items():
            path = self._path(key)
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                status[key] = {
                    'exists': True,
                    'size': len(content),
                    'lines': content.count('\n'),
                    'updated': datetime.fromtimestamp(os.path.getmtime(path)).strftime('%Y-%m-%d %H:%M:%S'),
                    'preview': content[:200] + '...' if len(content) > 200 else content,
                }
            else:
                status[key] = {'exists': False, 'size': 0, 'lines': 0, 'updated': '', 'preview': ''}
        return status

    def get_file(self, name: str) -> str:
        path = self._path(name)
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        return ''

    def update_file(self, name: str, content: str):
        path = self._path(name)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

    def initialize_from_outline(self, outline: Dict, protagonist: str = ''):
        world_state = self._build_initial_world_state(outline, protagonist)
        self.update_file('current_state', world_state)

        ledger = self._build_initial_ledger(outline)
        self.update_file('particle_ledger', ledger)

        hooks = self._build_initial_hooks(outline)
        self.update_file('pending_hooks', hooks)

        summaries = '# 章节摘要\n\n暂无已写章节\n'
        self.update_file('chapter_summaries', summaries)

        subplot = self._build_initial_subplots(outline)
        self.update_file('subplot_board', subplot)

        emotional = self._build_initial_emotional_arcs(outline, protagonist)
        self.update_file('emotional_arcs', emotional)

        matrix = self._build_initial_character_matrix(outline)
        self.update_file('character_matrix', matrix)

    def _build_initial_world_state(self, outline: Dict, protagonist: str) -> str:
        title = outline.get('title', outline.get('novel_name', '未命名'))
        world = outline.get('world_setting', outline.get('world', '待设定'))
        lines = [
            f'# 世界状态：{title}',
            f'',
            f'## 基本信息',
            f'- 创建时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
            f'- 主角：{protagonist or "待定"}',
            f'',
            f'## 世界观',
            f'{world}',
            f'',
            f'## 当前角色位置',
            f'- {protagonist or "主角"}：初始地点',
            f'',
            f'## 已知信息',
            f'- 暂无',
            f'',
            f'## 情感状态',
            f'- {protagonist or "主角"}：平静',
            f'',
        ]
        return '\n'.join(lines)

    def _build_initial_ledger(self, outline: Dict) -> str:
        lines = [
            f'# 资源账本',
            f'',
            f'## 主角持有',
            f'- 暂无',
            f'',
            f'## 重要物品',
            f'- 暂无',
            f'',
            f'## 金钱/资源',
            f'- 暂无',
            f'',
            f'## 衰减追踪',
            f'- 暂无',
            f'',
        ]
        return '\n'.join(lines)

    def _build_initial_hooks(self, outline: Dict) -> str:
        lines = [
            f'# 未闭合伏笔',
            f'',
            f'## 活跃伏笔',
            f'- 暂无',
            f'',
            f'## 已回收伏笔',
            f'- 暂无',
            f'',
            f'## 对读者的承诺',
            f'- 暂无',
            f'',
        ]
        return '\n'.join(lines)

    def _build_initial_subplots(self, outline: Dict) -> str:
        lines = [
            f'# 支线进度板',
            f'',
            f'## A线（主线）',
            f'- 状态：未开始',
            f'- 进度：0%',
            f'',
            f'## B线（感情线）',
            f'- 状态：未开始',
            f'- 进度：0%',
            f'',
            f'## C线（世界观线）',
            f'- 状态：未开始',
            f'- 进度：0%',
            f'',
            f'## 停滞检测',
            f'- 无',
            f'',
        ]
        return '\n'.join(lines)

    def _build_initial_emotional_arcs(self, outline: Dict, protagonist: str) -> str:
        lines = [
            f'# 情感弧线',
            f'',
            f'## {protagonist or "主角"}',
            f'- 初始状态：平静',
            f'- 当前状态：平静',
            f'- 成长轨迹：待记录',
            f'',
            f'## 其他角色',
            f'- 暂无',
            f'',
        ]
        return '\n'.join(lines)

    def _build_initial_character_matrix(self, outline: Dict) -> str:
        lines = [
            f'# 角色交互矩阵',
            f'',
            f'## 角色列表',
            f'- 暂无',
            f'',
            f'## 相遇记录',
            f'- 暂无',
            f'',
            f'## 信息边界',
            f'- 暂无',
            f'',
        ]
        return '\n'.join(lines)

    def update_after_chapter(self, chapter_num: int, chapter_content: str, chapter_title: str = '',
                              characters: List[str] = None, events: List[str] = None,
                              new_items: List[str] = None, hooks_planted: List[str] = None,
                              hooks_resolved: List[str] = None):
        self._update_chapter_summary(chapter_num, chapter_content, chapter_title, characters, events)
        if hooks_planted or hooks_resolved:
            self._update_hooks(hooks_planted, hooks_resolved)
        if new_items:
            self._update_ledger(new_items)
        self._update_character_matrix_from_content(chapter_content, chapter_num)

    def _update_chapter_summary(self, chapter_num: int, content: str, title: str,
                                 characters: List[str] = None, events: List[str] = None):
        summary = self.get_file('chapter_summaries')
        word_count = len(content)
        char_line = f'出场人物：{", ".join(characters) if characters else "待提取"}'
        event_line = f'关键事件：{"; ".join(events[:3]) if events else "待提取"}'
        new_entry = (
            f'\n## 第{chapter_num}章：{title or f"第{chapter_num}章"}'
            f'\n- 字数：{word_count}'
            f'\n- {char_line}'
            f'\n- {event_line}'
            f'\n- 状态变化：待分析'
            f'\n- 伏笔动态：待分析'
            f'\n'
        )
        if '# 章节摘要' in summary:
            summary += new_entry
        else:
            summary = f'# 章节摘要\n\n{new_entry}'
        self.update_file('chapter_summaries', summary)

    def _update_hooks(self, planted: List[str], resolved: List[str]):
        content = self.get_file('pending_hooks')
        for h in planted:
            content += f'\n- [ ] {h}（埋设于第X章）'
        for h in resolved:
            content = content.replace(f'- [ ] {h}', f'- [x] {h}（已回收）')
        self.update_file('pending_hooks', content)

    def _update_ledger(self, new_items: List[str]):
        content = self.get_file('particle_ledger')
        for item in new_items:
            content += f'\n- {item}'
        self.update_file('particle_ledger', content)

    def _update_character_matrix_from_content(self, content: str, chapter_num: int):
        names = self._extract_names(content)
        if not names:
            return
        matrix = self.get_file('character_matrix')
        matrix += f'\n## 第{chapter_num}章交互'
        for name in names[:10]:
            matrix += f'\n- {name} 出场'
        self.update_file('character_matrix', matrix)

    def _extract_names(self, text: str) -> List[str]:
        names = re.findall(r'[「『【]([^」』】]{2,4})[」』】】', text)
        return list(set(names))

    def get_context_for_writing(self, chapter_num: int) -> Dict[str, str]:
        context = {}
        for key in ['current_state', 'pending_hooks', 'chapter_summaries', 'subplot_board', 'character_matrix']:
            context[key] = self.get_file(key)
        return context

    def get_hooks_summary(self) -> Dict[str, Any]:
        content = self.get_file('pending_hooks')
        active = re.findall(r'- \[ \] (.+)', content)
        resolved = re.findall(r'- \[x\] (.+)', content)
        return {
            'active_count': len(active),
            'resolved_count': len(resolved),
            'active_hooks': active,
            'resolved_hooks': resolved,
        }

    def get_character_matrix_summary(self) -> Dict[str, Any]:
        content = self.get_file('character_matrix')
        chars = re.findall(r'- (.+) 出场', content)
        unique_chars = list(set(chars))
        return {
            'total_characters': len(unique_chars),
            'characters': unique_chars,
            'interaction_count': len(chars),
        }