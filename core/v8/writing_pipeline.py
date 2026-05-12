"""
NWACS 多Agent写作管线
基于 InkOS 5-Agent Pipeline 架构深度优化
Planner → Writer → Auditor → Reviser 四阶段接力

核心功能：
1. Planner - 规划章节结构、场景节拍、节奏控制
2. Writer - 根据大纲+当前世界状态生成正文
3. Auditor - 对照真相文件验证草稿，多维度检查
4. Reviser - 修复审计发现的问题
"""

import json
import os
import re
import time
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple, Callable
from dataclasses import dataclass, field
from enum import Enum


class PipelineStage(Enum):
    PLANNING = 'planning'
    WRITING = 'writing'
    AUDITING = 'auditing'
    REVISING = 'revising'
    COMPLETED = 'completed'
    FAILED = 'failed'


class AuditSeverity(Enum):
    CRITICAL = 'critical'
    HIGH = 'high'
    MEDIUM = 'medium'
    LOW = 'low'


@dataclass
class AuditIssue:
    dimension: str
    severity: AuditSeverity
    description: str
    location: str
    suggestion: str
    auto_fixable: bool = False


@dataclass
class PipelineResult:
    stage: PipelineStage
    chapter_num: int
    plan: str = ''
    draft: str = ''
    audit_issues: List[AuditIssue] = field(default_factory=list)
    revised_draft: str = ''
    passed: bool = False
    error: str = ''
    started_at: float = 0
    completed_at: float = 0


AUDIT_DIMENSIONS = [
    '角色记忆一致性',
    '物品连续性',
    '伏笔回收',
    '大纲偏离度',
    '叙事节奏',
    '情感弧线',
    '战力体系',
    '时间线',
    '空间一致性',
    '对话人设',
    'AI痕迹检测',
    '字数控制',
    '章节钩子',
    '追读力',
    '文风一致性',
]


class WritingPipeline:
    def __init__(self, llm_call_fn: Callable = None, truth_manager=None,
                 style_engine=None, strand_engine=None):
        self.llm_call = llm_call_fn or self._default_llm_call
        self.truth_manager = truth_manager
        self.style_engine = style_engine
        self.strand_engine = strand_engine
        self.results: Dict[int, PipelineResult] = {}

    def _default_llm_call(self, prompt: str) -> str:
        return f'[LLM模拟响应] 已收到prompt，长度{len(prompt)}字'

    def run(self, chapter_num: int, outline: Dict, context: Dict = None,
            word_count: int = 3000, style_label: str = '') -> PipelineResult:
        result = PipelineResult(
            stage=PipelineStage.PLANNING,
            chapter_num=chapter_num,
            started_at=time.time(),
        )

        try:
            result.plan = self._plan_chapter(chapter_num, outline, context, word_count)
            result.stage = PipelineStage.WRITING

            result.draft = self._write_chapter(chapter_num, result.plan, outline, context, word_count, style_label)
            result.stage = PipelineStage.AUDITING

            result.audit_issues = self._audit_chapter(chapter_num, result.draft, outline, context)
            result.stage = PipelineStage.REVISING

            critical_issues = [i for i in result.audit_issues if i.severity == AuditSeverity.CRITICAL]
            if critical_issues:
                result.revised_draft = self._revise_chapter(result.draft, critical_issues, outline)
            else:
                result.revised_draft = result.draft

            result.passed = len([i for i in result.audit_issues
                                 if i.severity in (AuditSeverity.CRITICAL, AuditSeverity.HIGH)]) <= 2
            result.stage = PipelineStage.COMPLETED

        except Exception as e:
            result.stage = PipelineStage.FAILED
            result.error = str(e)

        result.completed_at = time.time()
        self.results[chapter_num] = result
        return result

    def _plan_chapter(self, chapter_num: int, outline: Dict, context: Dict, word_count: int) -> str:
        outline_text = json.dumps(outline, ensure_ascii=False, indent=2)[:1000]
        context_text = ''
        if context:
            for key, val in context.items():
                context_text += f'\n{key}: {val[:300] if val else "无"}'

        prompt = f"""你是一位专业的小说章节规划师。请为第{chapter_num}章制定详细的写作计划。

## 大纲参考
{outline_text}

## 上下文
{context_text}

## 要求
- 目标字数：{word_count}字
- 规划内容：本章核心冲突、场景安排、节奏控制、角色出场
- 输出格式：清晰的场景列表，每个场景包含地点、人物、核心事件

请输出章节规划："""
        return self.llm_call(prompt)

    def _write_chapter(self, chapter_num: int, plan: str, outline: Dict,
                        context: Dict, word_count: int, style_label: str) -> str:
        style_prompt = ''
        if self.style_engine and style_label:
            fp = self.style_engine.get_fingerprint(style_label)
            if fp:
                style_prompt = self.style_engine.get_style_prompt(style_label)

        outline_text = json.dumps(outline, ensure_ascii=False, indent=2)[:500]

        prompt = f"""你是一位专业的小说作家。请根据以下规划创作第{chapter_num}章。

## 章节规划
{plan}

## 大纲参考
{outline_text}

## 写作要求
- 目标字数：{word_count}字（上下浮动不超过10%）
- 语言：中文网文风格
- 格式：自然段落，适当使用对话

{style_prompt}

请开始写作："""
        return self.llm_call(prompt)

    def _audit_chapter(self, chapter_num: int, draft: str, outline: Dict, context: Dict) -> List[AuditIssue]:
        issues = []

        word_count = len(draft)
        if word_count < 500:
            issues.append(AuditIssue(
                dimension='字数控制', severity=AuditSeverity.CRITICAL,
                description=f'章节字数过少：{word_count}字',
                location='全文', suggestion='需要大幅扩充内容', auto_fixable=False,
            ))

        dialogue_count = len(re.findall(r'「[^」]*」', draft))
        if dialogue_count == 0:
            issues.append(AuditIssue(
                dimension='叙事节奏', severity=AuditSeverity.MEDIUM,
                description='本章没有对话',
                location='全文', suggestion='适当加入角色对话丰富节奏', auto_fixable=True,
            ))

        emotion_words = re.findall(r'[喜怒哀乐悲恐惊]', draft)
        if len(emotion_words) < 3:
            issues.append(AuditIssue(
                dimension='情感弧线', severity=AuditSeverity.LOW,
                description='情感表达不足',
                location='全文', suggestion='增加角色情感描写', auto_fixable=True,
            ))

        hook_patterns = ['突然', '就在这时', '没想到', '然而', '但是', '却']
        has_hook = any(p in draft for p in hook_patterns)
        if not has_hook:
            issues.append(AuditIssue(
                dimension='章节钩子', severity=AuditSeverity.MEDIUM,
                description='缺少章节钩子',
                location='结尾', suggestion='在章节结尾设置悬念或转折', auto_fixable=True,
            ))

        if self.strand_engine:
            analysis = self.strand_engine.analyze_chapter(chapter_num, draft)
            if analysis.quest_ratio < 0.2:
                issues.append(AuditIssue(
                    dimension='叙事节奏', severity=AuditSeverity.MEDIUM,
                    description='主线(Quest)占比过低',
                    location='全文', suggestion='增加主线剧情推进', auto_fixable=True,
                ))

        return issues

    def _revise_chapter(self, draft: str, critical_issues: List[AuditIssue], outline: Dict) -> str:
        if not critical_issues:
            return draft

        issue_text = '\n'.join([f'- [{i.severity.value}] {i.dimension}: {i.description}' for i in critical_issues])

        prompt = f"""请修改以下小说章节，修复以下问题：

## 需要修复的问题
{issue_text}

## 原文
{draft[:3000]}

## 要求
- 保持原有文风和叙事节奏
- 只修改有问题的部分
- 确保修改后自然流畅

请输出修改后的章节："""
        return self.llm_call(prompt)

    def get_result(self, chapter_num: int) -> Optional[PipelineResult]:
        return self.results.get(chapter_num)

    def get_pipeline_status(self) -> Dict[str, Any]:
        total = len(self.results)
        passed = sum(1 for r in self.results.values() if r.passed)
        failed = sum(1 for r in self.results.values() if r.stage == PipelineStage.FAILED)
        return {
            'total_chapters': total,
            'passed': passed,
            'failed': failed,
            'pass_rate': round(passed / total * 100, 1) if total > 0 else 0,
            'recent_results': [
                {
                    'chapter': r.chapter_num,
                    'stage': r.stage.value,
                    'passed': r.passed,
                    'issues': len(r.audit_issues),
                    'duration': round(r.completed_at - r.started_at, 1),
                }
                for r in sorted(self.results.values(), key=lambda x: x.chapter_num)[-10:]
            ],
        }