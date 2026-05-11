#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 自动后生成一致性检查管线 - AutoConsistencyPipeline

对标 AI_NovelGenerator 自动审校机制 / 炼字工坊 RAG向量防崩盘

核心能力：
1. 生成后自动触发 - 每章生成完成后自动运行全套一致性检查
2. 多维度检查 - 人物/剧情/设定/伏笔/风格 五维检查
3. 智能修复建议 - 发现问题后自动生成修复提示词
4. 检查报告 - 生成结构化的一致性报告
5. 与RAG向量记忆联动 - 利用语义搜索发现深层矛盾

设计原则：
- 纯本地计算，零API调用（检查阶段）
- 修复阶段可选调用API
- 可配置检查严格度
"""

import json
import os
import time
import re
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class CheckSeverity(Enum):
    PASS = "通过"
    INFO = "提示"
    WARN = "警告"
    ERROR = "错误"
    CRITICAL = "严重"


class CheckCategory(Enum):
    CHARACTER = "人物一致性"
    PLOT = "剧情一致性"
    SETTING = "设定一致性"
    FORESHADOWING = "伏笔管理"
    STYLE = "风格一致性"
    STRUCTURE = "结构完整性"
    LOGIC = "逻辑自洽"


@dataclass
class CheckResult:
    category: CheckCategory
    severity: CheckSeverity
    description: str
    detail: str = ""
    suggestion: str = ""
    chapter: int = 0
    related_chapters: List[int] = field(default_factory=list)
    auto_fixable: bool = False


@dataclass
class ConsistencyReport:
    chapter: int
    timestamp: str
    total_checks: int = 0
    passed: int = 0
    warnings: int = 0
    errors: int = 0
    results: List[CheckResult] = field(default_factory=list)
    overall_score: float = 1.0
    is_clean: bool = True


class AutoConsistencyPipeline:
    """自动后生成一致性检查管线"""

    def __init__(self, memory_manager=None, voice_injector=None, rag_memory=None):
        self.memory_manager = memory_manager
        self.voice_injector = voice_injector
        self.rag_memory = rag_memory
        self.check_history: List[ConsistencyReport] = []

    def run_full_check(self, chapter: int, content: str,
                        novel_title: str = "",
                        strictness: str = "normal") -> ConsistencyReport:
        t0 = time.time()

        report = ConsistencyReport(
            chapter=chapter,
            timestamp=datetime.now().isoformat(),
        )

        results = []

        results.extend(self._check_character_consistency(chapter, content))
        results.extend(self._check_plot_consistency(chapter, content))
        results.extend(self._check_setting_consistency(chapter, content))
        results.extend(self._check_foreshadowing(chapter, content))
        results.extend(self._check_style_consistency(chapter, content))
        results.extend(self._check_structure(chapter, content))
        results.extend(self._check_logic(chapter, content))

        if self.rag_memory:
            results.extend(self._check_semantic_consistency(chapter, content))

        report.results = results
        report.total_checks = len(results)

        for r in results:
            if r.severity == CheckSeverity.PASS:
                report.passed += 1
            elif r.severity in (CheckSeverity.WARN, CheckSeverity.INFO):
                report.warnings += 1
            elif r.severity in (CheckSeverity.ERROR, CheckSeverity.CRITICAL):
                report.errors += 1

        severity_weights = {
            CheckSeverity.PASS: 0,
            CheckSeverity.INFO: -1,
            CheckSeverity.WARN: -3,
            CheckSeverity.ERROR: -8,
            CheckSeverity.CRITICAL: -15,
        }
        total_penalty = sum(severity_weights.get(r.severity, 0) for r in results)
        report.overall_score = max(0.0, 100 + total_penalty) / 100
        report.is_clean = report.errors == 0

        elapsed = time.time() - t0
        report.results.insert(0, CheckResult(
            category=CheckCategory.STRUCTURE,
            severity=CheckSeverity.INFO,
            description=f"一致性检查完成，耗时{elapsed:.1f}秒",
            detail=f"共{report.total_checks}项检查，{report.passed}通过/{report.warnings}警告/{report.errors}错误",
        ))

        self.check_history.append(report)
        return report

    def _check_character_consistency(self, chapter: int, content: str) -> List[CheckResult]:
        results = []

        if not self.memory_manager:
            return results

        char_names = self._extract_character_names(content)

        for name in char_names:
            profile = self.memory_manager.characters.get(name)
            if not profile:
                continue

            if profile.first_appearance_chapter > 0 and chapter < profile.first_appearance_chapter:
                results.append(CheckResult(
                    category=CheckCategory.CHARACTER,
                    severity=CheckSeverity.ERROR,
                    description=f"角色「{name}」在第{chapter}章出现，但首次出场记录为第{profile.first_appearance_chapter}章",
                    suggestion=f"更新「{name}」的首次出场章节",
                    chapter=chapter,
                ))

            if profile.status == "已死亡" and self._is_character_alive_in_text(name, content):
                results.append(CheckResult(
                    category=CheckCategory.CHARACTER,
                    severity=CheckSeverity.CRITICAL,
                    description=f"角色「{name}」已标记为死亡，但在第{chapter}章中仍然活跃",
                    suggestion=f"检查「{name}」的状态或修改本章内容",
                    chapter=chapter,
                ))

            if profile.status == "存活":
                gap = chapter - profile.last_appearance_chapter
                if gap > 50 and profile.last_appearance_chapter > 0:
                    results.append(CheckResult(
                        category=CheckCategory.CHARACTER,
                        severity=CheckSeverity.INFO,
                        description=f"角色「{name}」时隔{gap}章重新出场",
                        suggestion=f"在文中简要回顾该角色的近况",
                        chapter=chapter,
                    ))

        if self.voice_injector and char_names:
            for name in char_names:
                dialogues = self._extract_dialogues(name, content)
                for dialogue in dialogues[:3]:
                    voice_check = self.voice_injector.check_dialogue_consistency(name, dialogue)
                    if not voice_check["consistent"]:
                        results.append(CheckResult(
                            category=CheckCategory.CHARACTER,
                            severity=CheckSeverity.WARN,
                            description=f"「{name}」的对话偏离其语音风格",
                            detail=f"问题: {'; '.join(voice_check['issues'])}",
                            suggestion=f"调整「{name}」的对话以符合其说话风格",
                            chapter=chapter,
                            auto_fixable=True,
                        ))

        return results

    def _check_plot_consistency(self, chapter: int, content: str) -> List[CheckResult]:
        results = []

        if not self.memory_manager:
            return results

        events = self.memory_manager.plot_events
        recent_events = [e for e in events
                         if abs(e['chapter'] - chapter) <= 5 and e['chapter'] < chapter]

        for event in recent_events:
            event_keywords = set(event['event'])
            content_keywords = set(content)
            overlap = event_keywords & content_keywords
            if len(overlap) < 3 and event.get('type') == 'cliffhanger':
                results.append(CheckResult(
                    category=CheckCategory.PLOT,
                    severity=CheckSeverity.WARN,
                    description=f"第{event['chapter']}章的悬念「{event['event'][:50]}」在本章未得到回应",
                    suggestion="考虑在本章提及或推进该悬念",
                    chapter=chapter,
                    related_chapters=[event['chapter']],
                ))

        return results

    def _check_setting_consistency(self, chapter: int, content: str) -> List[CheckResult]:
        results = []

        if not self.memory_manager:
            return results

        locations = self._extract_locations(content)
        for loc in locations:
            if loc in self.memory_manager.world_settings:
                setting = self.memory_manager.world_settings[loc]
                if isinstance(setting, dict) and setting.get("destroyed"):
                    results.append(CheckResult(
                        category=CheckCategory.SETTING,
                        severity=CheckSeverity.ERROR,
                        description=f"地点「{loc}」已被摧毁，但在第{chapter}章中仍然出现",
                        suggestion=f"检查「{loc}」的状态或修改本章内容",
                        chapter=chapter,
                    ))

        return results

    def _check_foreshadowing(self, chapter: int, content: str) -> List[CheckResult]:
        results = []

        if not self.memory_manager:
            return results

        for fs in self.memory_manager.foreshadowings.values():
            if fs.expected_payoff_chapter == chapter:
                if fs.status.value in ("已埋设", "已暗示"):
                    fs_terms = set(fs.description)
                    content_terms = set(content)
                    if len(fs_terms & content_terms) < 3:
                        results.append(CheckResult(
                            category=CheckCategory.FORESHADOWING,
                            severity=CheckSeverity.WARN,
                            description=f"伏笔「{fs.description[:50]}」预期在第{chapter}章回收，但未发现相关内容",
                            suggestion="检查是否遗漏了该伏笔的回收",
                            chapter=chapter,
                        ))

            if fs.expected_payoff_chapter < chapter and fs.status.value in ("已埋设", "已暗示"):
                results.append(CheckResult(
                    category=CheckCategory.FORESHADOWING,
                    severity=CheckSeverity.INFO,
                    description=f"伏笔「{fs.description[:50]}」已超期未回收(预期第{fs.expected_payoff_chapter}章)",
                    suggestion="尽快安排该伏笔的回收，或调整预期回收章节",
                    chapter=chapter,
                ))

        return results

    def _check_style_consistency(self, chapter: int, content: str) -> List[CheckResult]:
        results = []

        if not self.memory_manager:
            return results

        fingerprint = self.memory_manager.style_fingerprint
        if not fingerprint or not fingerprint.get("avg_sentence_length"):
            return results

        sentences = re.split(r'[。！？\n]', content)
        sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 2]

        if sentences:
            avg_len = sum(len(s) for s in sentences) / len(sentences)
            expected_len = fingerprint["avg_sentence_length"]

            if expected_len > 0:
                deviation = abs(avg_len - expected_len) / expected_len
                if deviation > 0.5:
                    results.append(CheckResult(
                        category=CheckCategory.STYLE,
                        severity=CheckSeverity.WARN,
                        description=f"句长偏离风格指纹: 当前{avg_len:.1f}字/句 vs 预期{expected_len:.1f}字/句",
                        suggestion="调整句子长度以匹配整体风格",
                        chapter=chapter,
                        auto_fixable=True,
                    ))

        return results

    def _check_structure(self, chapter: int, content: str) -> List[CheckResult]:
        results = []

        word_count = len(content)
        if word_count < 500:
            results.append(CheckResult(
                category=CheckCategory.STRUCTURE,
                severity=CheckSeverity.ERROR,
                description=f"章节字数过少: {word_count}字 (建议≥2000字)",
                suggestion="扩充章节内容",
                chapter=chapter,
            ))
        elif word_count < 1500:
            results.append(CheckResult(
                category=CheckCategory.STRUCTURE,
                severity=CheckSeverity.WARN,
                description=f"章节字数偏少: {word_count}字 (建议≥2000字)",
                suggestion="适当扩充章节内容",
                chapter=chapter,
            ))

        paragraphs = [p.strip() for p in content.split('\n') if p.strip()]
        if len(paragraphs) < 3:
            results.append(CheckResult(
                category=CheckCategory.STRUCTURE,
                severity=CheckSeverity.WARN,
                description=f"段落数过少: {len(paragraphs)}段",
                suggestion="合理分段，增强可读性",
                chapter=chapter,
            ))

        if not content.strip().endswith(('。', '！', '？', '…', '"', '」')):
            results.append(CheckResult(
                category=CheckCategory.STRUCTURE,
                severity=CheckSeverity.INFO,
                description="章节结尾不完整",
                suggestion="确保章节有完整的结尾",
                chapter=chapter,
            ))

        return results

    def _check_logic(self, chapter: int, content: str) -> List[CheckResult]:
        results = []

        contradictions = [
            (r'(刚刚|刚才).*(已经|早就)', "时间矛盾"),
            (r'(死了|被杀|陨落).*(说话|笑道|走来)', "生死矛盾"),
            (r'(昏迷|晕倒|失去意识).*(看到|听到|感觉到)', "感知矛盾"),
            (r'(废了|被废|修为尽失).*(运转|爆发|施展)', "能力矛盾"),
        ]

        for pattern, desc in contradictions:
            matches = re.findall(pattern, content)
            if matches:
                results.append(CheckResult(
                    category=CheckCategory.LOGIC,
                    severity=CheckSeverity.WARN,
                    description=f"疑似{desc}: 发现{len(matches)}处",
                    detail=f"匹配模式: {pattern}",
                    suggestion=f"检查{desc}是否合理",
                    chapter=chapter,
                ))

        return results

    def _check_semantic_consistency(self, chapter: int, content: str) -> List[CheckResult]:
        results = []

        if not self.rag_memory:
            return results

        key_sentences = []
        for sentence in re.split(r'[。！？]', content):
            sentence = sentence.strip()
            if len(sentence) > 15 and len(sentence) < 100:
                key_sentences.append(sentence)
            if len(key_sentences) >= 5:
                break

        for sentence in key_sentences[:3]:
            search_results = self.rag_memory.search(
                query=sentence,
                top_k=3,
                min_score=0.7,
            )

            for sr in search_results:
                if sr.chunk.chapter > 0 and sr.chunk.chapter < chapter:
                    prev_content = sr.chunk.content
                    if self._detect_contradiction(sentence, prev_content):
                        results.append(CheckResult(
                            category=CheckCategory.LOGIC,
                            severity=CheckSeverity.WARN,
                            description=f"语义矛盾: 本章内容与第{sr.chunk.chapter}章存在潜在冲突",
                            detail=f"本章: {sentence[:80]}...\n前文: {prev_content[:80]}...",
                            suggestion="检查两处内容是否逻辑一致",
                            chapter=chapter,
                            related_chapters=[sr.chunk.chapter],
                        ))

        return results

    def _detect_contradiction(self, text1: str, text2: str) -> bool:
        contradiction_pairs = [
            (["活", "生", "存活"], ["死", "陨落", "陨", "去世"]),
            (["有", "拥有", "持有"], ["没有", "失去", "丢失"]),
            (["强", "厉害", "无敌"], ["弱", "废", "不堪一击"]),
            (["男", "他"], ["女", "她"]),
        ]

        for pos_set, neg_set in contradiction_pairs:
            t1_has_pos = any(w in text1 for w in pos_set)
            t1_has_neg = any(w in text1 for w in neg_set)
            t2_has_pos = any(w in text2 for w in pos_set)
            t2_has_neg = any(w in text2 for w in neg_set)

            if (t1_has_pos and t2_has_neg) or (t1_has_neg and t2_has_pos):
                return True

        return False

    def _extract_character_names(self, content: str) -> List[str]:
        if not self.memory_manager:
            return []
        known_names = set(self.memory_manager.characters.keys())
        found = []
        for name in known_names:
            if name in content:
                found.append(name)
        return found

    def _extract_dialogues(self, name: str, content: str) -> List[str]:
        dialogues = []
        pattern = rf'{name}[^"]*"[^"]+"'
        matches = re.findall(pattern, content)
        for m in matches:
            quote_match = re.search(r'"([^"]+)"', m)
            if quote_match:
                dialogues.append(quote_match.group(1))

        pattern2 = rf'{name}[^「]*「([^」]+)」'
        matches2 = re.findall(pattern2, content)
        dialogues.extend(matches2)

        return dialogues

    def _extract_locations(self, content: str) -> List[str]:
        if not self.memory_manager:
            return []
        known_locations = set()
        for key in self.memory_manager.world_settings:
            if isinstance(self.memory_manager.world_settings[key], dict):
                if self.memory_manager.world_settings[key].get("type") == "location":
                    known_locations.add(key)

        found = []
        for loc in known_locations:
            if loc in content:
                found.append(loc)
        return found

    def _is_character_alive_in_text(self, name: str, content: str) -> bool:
        context_window = 50
        for match in re.finditer(name, content):
            start = max(0, match.start() - context_window)
            end = min(len(content), match.end() + context_window)
            context = content[start:end]
            action_verbs = ["说", "走", "看", "站", "坐", "笑", "拿", "打", "飞", "跑"]
            if any(v in context for v in action_verbs):
                return True
        return False

    def generate_fix_prompt(self, report: ConsistencyReport) -> str:
        if report.is_clean:
            return ""

        parts = ["\n【一致性检查发现问题，请根据以下建议修改本章内容】\n"]

        errors = [r for r in report.results
                  if r.severity in (CheckSeverity.ERROR, CheckSeverity.CRITICAL)]
        warnings = [r for r in report.results
                    if r.severity == CheckSeverity.WARN]

        if errors:
            parts.append("## 必须修复的问题:")
            for i, e in enumerate(errors, 1):
                parts.append(f"{i}. [{e.category.value}] {e.description}")
                if e.suggestion:
                    parts.append(f"   修复建议: {e.suggestion}")

        if warnings:
            parts.append("\n## 建议优化的问题:")
            for i, w in enumerate(warnings, 1):
                parts.append(f"{i}. [{w.category.value}] {w.description}")
                if w.suggestion:
                    parts.append(f"   优化建议: {w.suggestion}")

        parts.append(f"\n整体一致性评分: {report.overall_score:.0%}")
        parts.append("请修改本章内容以解决以上问题，保持故事的连贯性和一致性。")

        return "\n".join(parts)

    def format_report(self, report: ConsistencyReport) -> str:
        lines = []
        lines.append("=" * 60)
        lines.append(f"第{report.chapter}章 一致性检查报告")
        lines.append("=" * 60)
        lines.append(f"时间: {report.timestamp}")
        lines.append(f"评分: {report.overall_score:.0%} | "
                      f"通过:{report.passed} 警告:{report.warnings} 错误:{report.errors}")
        lines.append(f"状态: {'✅ 通过' if report.is_clean else '❌ 存在问题'}")
        lines.append("-" * 60)

        by_category = {}
        for r in report.results:
            cat = r.category.value
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(r)

        for cat, cat_results in by_category.items():
            lines.append(f"\n【{cat}】")
            for r in cat_results:
                icon = {CheckSeverity.PASS: "✅", CheckSeverity.INFO: "ℹ️",
                        CheckSeverity.WARN: "⚠️", CheckSeverity.ERROR: "❌",
                        CheckSeverity.CRITICAL: "🚨"}.get(r.severity, "•")
                lines.append(f"  {icon} {r.description}")
                if r.detail:
                    lines.append(f"     详情: {r.detail}")
                if r.suggestion:
                    lines.append(f"     建议: {r.suggestion}")

        lines.append("\n" + "=" * 60)
        return "\n".join(lines)


if __name__ == "__main__":
    print("=" * 60)
    print("自动后生成一致性检查管线 - 功能验证")
    print("=" * 60)

    from novel_memory_manager import NovelMemoryManager

    memory = NovelMemoryManager(novel_title="测试小说")

    memory.register_character("叶青云", gender="男", age=18,
                               personality="坚毅果敢", role="主角",
                               first_appearance_chapter=1,
                               last_appearance_chapter=5)
    memory.register_character("冷月", gender="女", age=20,
                               personality="冷酷寡言", role="女主",
                               first_appearance_chapter=3,
                               last_appearance_chapter=5)

    memory.add_plot_event(3, "冷月首次出场，救下被追杀的叶青云",
                          event_type="character_intro",
                          characters=["冷月", "叶青云"])

    memory.add_foreshadowing(
        description="冷月身上有一块神秘玉佩，似乎与叶青云的上古传承有关",
        planted_chapter=3,
        expected_payoff_chapter=10,
        fs_type="物品",
    )

    memory.style_fingerprint = {"avg_sentence_length": 25.0}

    pipeline = AutoConsistencyPipeline(memory_manager=memory)

    print("\n[1] 正常章节检查...")
    good_content = """叶青云站在山巅，望着远方的云海翻涌。

    自从获得上古传承以来，他的修为一日千里。短短两个月，便从炼气期突破到了筑基期。

    "在想什么？"冷月的声音从身后传来，依旧清冷如霜。

    叶青云没有回头，只是轻声道："在想，这条路还要走多久。"

    冷月走到他身旁，沉默了片刻，才说："走到你不想走为止。"

    她的语气依旧简短，但叶青云听出了一丝不同以往的温柔。"""

    report = pipeline.run_full_check(6, good_content)
    print(pipeline.format_report(report))

    print("\n[2] 有问题章节检查...")
    bad_content = """叶青云死了。冷月看着他倒下的身影，泪流满面。

    "你为什么要这样做？"叶青云问道。

    冷月擦了擦眼泪，温柔地说："因为我爱你啊，你这个傻瓜。"

    叶青云哈哈大笑："太好了，那我们一起去吃火锅吧！"

    两人手牵手走向远方。"""

    report2 = pipeline.run_full_check(6, bad_content)
    print(pipeline.format_report(report2))

    print("\n[3] 修复提示词生成...")
    if not report2.is_clean:
        fix_prompt = pipeline.generate_fix_prompt(report2)
        print(fix_prompt[:500])

    print("\n✅ 自动后生成一致性检查管线验证完成")
