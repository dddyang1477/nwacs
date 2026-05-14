#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reviewer Agent — NWACS 统一审查模块 v3.0

核心功能:
1. 设定一致性检查 — 角色能力/地点/物品/货币
2. 时间线检查 — 时间衔接/倒计时/同时出现
3. 叙事连贯性检查 — 钩子回应/场景过渡/情绪弧
4. 角色一致性检查 — 对话风格/行为/知识边界
5. 逻辑检查 — 因果关系/决策动机/力量对比
6. AI味检查 — 词汇层/句式层/叙事层/情感层/对话层
7. POV感知检查 — 视角一致性/信息边界/感知过滤
8. 钩子债务追踪 — 伏笔回收/开放循环/债务升级
9. 情绪弧分析 — 情绪曲线/转折点/情绪过渡
10. 节奏一致性 — 场景节奏/张力曲线/信息密度
11. 37维连续性检查 — 角色/世界/情节/叙事/风格全维度

设计原则:
- 只找问题、给证据、给修复方向
- 不评分、不给建议、不写摘要性评价
- 每个 issue 必须有 evidence
- severity 分级: critical > high > medium > low
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from llm_interface import llm, GenerationParams


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


@dataclass
class ReviewIssue:
    severity: str
    category: str
    location: str
    description: str
    evidence: str
    fix_hint: str
    blocking: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "severity": self.severity,
            "category": self.category,
            "location": self.location,
            "description": self.description,
            "evidence": self.evidence,
            "fix_hint": self.fix_hint,
            "blocking": self.blocking,
        }


@dataclass
class ReviewResult:
    chapter: int
    issues: List[ReviewIssue] = field(default_factory=list)
    summary: str = ""
    created_at: str = field(default_factory=_utc_now_iso)

    @property
    def blocking_count(self) -> int:
        return sum(1 for i in self.issues if i.blocking)

    @property
    def critical_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == "critical")

    @property
    def high_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == "high")

    @property
    def overall_status(self) -> str:
        if self.blocking_count > 0:
            return "rejected"
        if self.critical_count > 0:
            return "needs_fix"
        if self.high_count > 3:
            return "needs_review"
        return "accepted"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "chapter": self.chapter,
            "issues": [i.to_dict() for i in self.issues],
            "summary": self.summary,
            "blocking_count": self.blocking_count,
            "critical_count": self.critical_count,
            "high_count": self.high_count,
            "overall_status": self.overall_status,
            "created_at": self.created_at,
        }


class ReviewerAgent:
    """统一审查 Agent — 结构化审查章节正文"""

    AI_VOCAB_HIGH_FREQ = [
        "此外", "然而", "因此", "值得注意的是", "总而言之", "综上所述",
        "不可否认", "显而易见", "毋庸置疑", "与此同时", "不仅如此",
        "作为……的证明", "标志着", "为……奠定基础", "在……的过程中",
        "缓缓", "淡淡", "微微", "轻轻", "默默", "静静",
        "眸中闪过", "瞳孔微缩", "心中一凛", "嘴角微扬", "眉头微皱",
        "眼中闪过一丝", "脸上浮现", "心中涌起", "心底升起",
    ]

    AI_SENTENCE_PATTERNS = [
        (r"(?:他|她|它)不知道的是", "戏剧性反讽提示"),
        (r"殊不知", "戏剧性反讽提示"),
        (r"他终于明白[了]?", "总结句收尾"),
        (r"由此可见", "总结句收尾"),
        (r"这(?:一切|些|件事).{0,10}(?:意味|说明|表明|证明)", "解释性叙述"),
        (r"他这么说是因为", "对话后解释"),
        (r"她这么做是因为", "对话后解释"),
    ]

    AI_EMOTION_LABELS = [
        r"他感到\w+",
        r"她感到\w+",
        r"他非常\w+",
        r"她非常\w+",
        r"他十分\w+",
        r"她十分\w+",
        r"他内心\w+",
        r"她内心\w+",
    ]

    def __init__(self, project_root: str = ""):
        self.project_root = Path(project_root) if project_root else Path(".")
        self._story_system = None

    def _get_story_system(self):
        if self._story_system is None:
            from story_system import StorySystem
            self._story_system = StorySystem(str(self.project_root))
        return self._story_system

    def review_chapter(
        self,
        chapter: int,
        chapter_text: str,
        chapter_contract: Optional[Dict[str, Any]] = None,
        master_setting: Optional[Dict[str, Any]] = None,
        previous_summary: str = "",
        use_llm: bool = True,
    ) -> ReviewResult:
        result = ReviewResult(chapter=chapter)

        if not chapter_text or not chapter_text.strip():
            result.issues.append(ReviewIssue(
                severity="critical",
                category="other",
                location="全文",
                description="正文为空",
                evidence="chapter_text 为空或仅含空白字符",
                fix_hint="请提供有效的章节正文",
                blocking=True,
            ))
            result.summary = "1个问题：1个阻断"
            return result

        self._check_ai_vocab_layer(chapter_text, result)
        self._check_ai_sentence_layer(chapter_text, result)
        self._check_ai_narrative_layer(chapter_text, result)
        self._check_ai_emotion_layer(chapter_text, result)
        self._check_ai_dialogue_layer(chapter_text, result)

        self._check_basic_structure(chapter_text, result)

        self._check_pov_consistency(chapter_text, result)
        self._check_hook_debt(chapter_text, result, chapter_contract)
        self._check_emotional_arc(chapter_text, result)
        self._check_pacing_consistency(chapter_text, result)
        self._check_continuity_37d(chapter_text, result, chapter_contract, master_setting)

        if use_llm and llm:
            try:
                llm_issues = self._llm_deep_review(
                    chapter, chapter_text, chapter_contract, master_setting, previous_summary
                )
                for issue_data in llm_issues:
                    result.issues.append(ReviewIssue(**issue_data))
            except Exception as e:
                result.issues.append(ReviewIssue(
                    severity="low",
                    category="other",
                    location="系统",
                    description=f"LLM深度审查失败: {e}",
                    evidence=str(e),
                    fix_hint="检查LLM连接后重试",
                    blocking=False,
                ))

        total = len(result.issues)
        blocking = result.blocking_count
        critical = result.critical_count
        high = result.high_count
        result.summary = f"{total}个问题：{blocking}个阻断，{critical}个严重，{high}个高优"

        return result

    def _check_ai_vocab_layer(self, text: str, result: ReviewResult) -> None:
        found_patterns: Dict[str, List[str]] = {}
        for pattern in self.AI_VOCAB_HIGH_FREQ:
            matches = re.findall(re.escape(pattern), text)
            if matches:
                found_patterns[pattern] = matches

        total_hits = sum(len(v) for v in found_patterns.values())
        if total_hits == 0:
            return

        if total_hits >= 10:
            severity = "high"
        elif total_hits >= 5:
            severity = "medium"
        else:
            severity = "low"

        sample_patterns = list(found_patterns.keys())[:5]
        result.issues.append(ReviewIssue(
            severity=severity,
            category="ai_flavor",
            location="全文",
            description=f"高频AI词汇密集出现（共{total_hits}处）",
            evidence=f"检测到: {', '.join(sample_patterns)} 等词汇",
            fix_hint="替换为更自然的表达，删除不必要的连接词，用动作和对话替代抽象描述",
            blocking=severity == "high",
        ))

        text_500 = text[:500]
        faint_verbs = re.findall(r"(?:缓缓|淡淡|微微|轻轻|默默|静静)(?:地)?\w{1,4}", text_500)
        if len(faint_verbs) >= 3:
            result.issues.append(ReviewIssue(
                severity="medium",
                category="ai_flavor",
                location=f"前500字",
                description=f"「缓缓/淡淡/微微」+动词 结构在500字内出现{len(faint_verbs)}次",
                evidence=f"示例: {faint_verbs[:3]}",
                fix_hint="用具体动作替代模糊副词，如「缓缓走来」→「拖着步子挪过来」",
                blocking=False,
            ))

        expression_templates = re.findall(r"(?:眸中闪过|瞳孔微缩|心中一凛|嘴角微扬|眉头微皱|眼中闪过一丝|脸上浮现|心中涌起|心底升起)", text)
        if len(expression_templates) >= 5:
            result.issues.append(ReviewIssue(
                severity="medium",
                category="ai_flavor",
                location="全文",
                description=f"神态模板密集使用（共{len(expression_templates)}处）",
                evidence=f"示例: {expression_templates[:3]}",
                fix_hint="用独特的行为描写替代模板化神态，每个角色的反应方式应不同",
                blocking=False,
            ))

    def _check_ai_sentence_layer(self, text: str, result: ReviewResult) -> None:
        sentences = re.split(r'[。！？\n]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        if len(sentences) < 10:
            return

        lengths = [len(s) for s in sentences]
        consecutive_same = 0
        max_consecutive = 0
        for i in range(1, len(lengths)):
            diff = abs(lengths[i] - lengths[i - 1])
            if diff <= 3:
                consecutive_same += 1
                max_consecutive = max(max_consecutive, consecutive_same)
            else:
                consecutive_same = 0

        if max_consecutive >= 5:
            result.issues.append(ReviewIssue(
                severity="high",
                category="ai_flavor",
                location="全文",
                description=f"连续{max_consecutive + 1}句长度几乎相同（节拍器节奏）",
                evidence=f"句子长度变化极小，最大连续同构句数: {max_consecutive + 1}",
                fix_hint="刻意变化句子长度：短句3-10字制造紧张，长句25-50字渲染氛围",
                blocking=False,
            ))

        paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
        summary_endings = 0
        for para in paragraphs:
            if re.search(r"(?:终于|最终|从此|于是|就这样).{0,10}(?:明白|懂得|知道|学会|成长|改变|蜕变)", para):
                summary_endings += 1

        if summary_endings >= 3:
            result.issues.append(ReviewIssue(
                severity="medium",
                category="ai_flavor",
                location="全文",
                description=f"段落总结句收尾过多（{summary_endings}处）",
                evidence="多段以「他终于明白」「从此他懂得」等句式收尾",
                fix_hint="删除总结句，让读者自己体会。用行动或新悬念替代感悟式收尾",
                blocking=False,
            ))

        for pattern, label in self.AI_SENTENCE_PATTERNS:
            matches = re.findall(pattern, text)
            if len(matches) >= 2:
                result.issues.append(ReviewIssue(
                    severity="medium",
                    category="ai_flavor",
                    location="全文",
                    description=f"{label}模式出现{len(matches)}次",
                    evidence=f"匹配: {matches[:3]}",
                    fix_hint="删除此类提示性语句，让读者自行发现",
                    blocking=False,
                ))

    def _check_ai_narrative_layer(self, text: str, result: ReviewResult) -> None:
        paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
        if len(paragraphs) < 5:
            return

        para_lengths = [len(p) for p in paragraphs]
        if para_lengths:
            mean_len = sum(para_lengths) / len(para_lengths)
            if mean_len > 0:
                variance = sum((x - mean_len) ** 2 for x in para_lengths) / len(para_lengths)
                std_dev = (variance ** 0.5)
                cv = (std_dev / mean_len) * 100

                if cv < 25:
                    result.issues.append(ReviewIssue(
                        severity="medium",
                        category="ai_flavor",
                        location="全文",
                        description=f"段落信息密度过于均匀（变异系数{cv:.1f}%）",
                        evidence=f"段落长度均值{mean_len:.0f}字，标准差{std_dev:.0f}",
                        fix_hint="刻意制造段落长短对比：紧张场景用短段落，渲染场景用长段落",
                        blocking=False,
                    ))

        last_paragraph = paragraphs[-1] if paragraphs else ""
        safe_landing_patterns = [
            r"一切.{0,5}(?:恢复|归于|回到).{0,5}(?:平静|正常|原样)",
            r"问题.{0,5}(?:解决|化解|处理)",
            r"危机.{0,5}(?:解除|过去|消散)",
            r"(?:终于|最终).{0,5}(?:安全|平安|放心)",
        ]
        for pattern in safe_landing_patterns:
            if re.search(pattern, last_paragraph):
                result.issues.append(ReviewIssue(
                    severity="medium",
                    category="ai_flavor",
                    location="章末",
                    description="章末「安全着陆」——冲突完美解决，无遗留不安感",
                    evidence=f"章末段落: {last_paragraph[:100]}...",
                    fix_hint="章末保留一个未闭合的问题或不安因素，制造追读欲望",
                    blocking=False,
                ))
                break

        show_then_explain = re.findall(
            r"([^。！？]{10,40})(?:这|那)(?:是|意味着|说明|表明)[^。！？]{5,30}[。]",
            text
        )
        if len(show_then_explain) >= 3:
            result.issues.append(ReviewIssue(
                severity="medium",
                category="ai_flavor",
                location="全文",
                description=f"展示后紧跟解释模式出现{len(show_then_explain)}次",
                evidence=f"示例: {show_then_explain[:2]}",
                fix_hint="展示后不要解释，信任读者的理解力。删除「这意味着」「这说明」等解释性语句",
                blocking=False,
            ))

    def _check_ai_emotion_layer(self, text: str, result: ReviewResult) -> None:
        label_hits = 0
        for pattern in self.AI_EMOTION_LABELS:
            matches = re.findall(pattern, text)
            label_hits += len(matches)

        if label_hits >= 5:
            result.issues.append(ReviewIssue(
                severity="high",
                category="ai_flavor",
                location="全文",
                description=f"情绪标签化严重（共{label_hits}处「他感到/她非常」等）",
                evidence=f"检测到{label_hits}处情绪标签",
                fix_hint="用行为暗示情绪：不写「他愤怒」，写「他一拳砸在桌上，茶杯跳了起来」",
                blocking=False,
            ))

        emotion_words = ["愤怒", "悲伤", "恐惧", "紧张", "兴奋", "平静", "焦虑", "绝望", "喜悦", "痛苦"]
        emotion_sequence: List[Tuple[str, int]] = []
        for i, para in enumerate(text.split('\n')):
            for word in emotion_words:
                if word in para:
                    emotion_sequence.append((word, i))
                    break

        if len(emotion_sequence) >= 3:
            rapid_switches = 0
            for i in range(1, len(emotion_sequence)):
                if emotion_sequence[i][1] == emotion_sequence[i - 1][1]:
                    if emotion_sequence[i][0] != emotion_sequence[i - 1][0]:
                        rapid_switches += 1
            if rapid_switches >= 2:
                result.issues.append(ReviewIssue(
                    severity="medium",
                    category="ai_flavor",
                    location="全文",
                    description=f"情绪即时切换（无过渡）出现{rapid_switches}次",
                    evidence=f"情绪序列: {[e[0] for e in emotion_sequence[:5]]}",
                    fix_hint="情绪变化需要过渡——用身体反应、环境描写、内心独白作为情绪转换的桥梁",
                    blocking=False,
                ))

    def _check_ai_dialogue_layer(self, text: str, result: ReviewResult) -> None:
        dialogue_lines = re.findall(r'[「「"]([^「」"]+)[」」"]', text)
        if not dialogue_lines:
            return

        info_dump_count = 0
        for line in dialogue_lines:
            if len(line) > 80 and any(kw in line for kw in ["因为", "所以", "实际上", "其实", "要知道"]):
                info_dump_count += 1

        if info_dump_count >= 3:
            result.issues.append(ReviewIssue(
                severity="high",
                category="ai_flavor",
                location="对话",
                description=f"对话信息宣讲过多（{info_dump_count}处长对话含解释性内容）",
                evidence=f"示例: {[l[:50] for l in dialogue_lines if len(l) > 80][:3]}",
                fix_hint="对话应推进冲突而非解释背景。将背景信息融入动作和场景中",
                blocking=False,
            ))

        formal_count = 0
        for line in dialogue_lines:
            if re.search(r"(?:因此|然而|此外|不过|虽然|但是|所以|于是|总之)", line) and len(line) > 30:
                formal_count += 1

        if formal_count >= 3:
            result.issues.append(ReviewIssue(
                severity="medium",
                category="ai_flavor",
                location="对话",
                description=f"对话书面语化严重（{formal_count}处使用书面连接词）",
                evidence=f"示例: {[l[:50] for l in dialogue_lines if '因此' in l or '然而' in l][:3]}",
                fix_hint="口语化对话：删除书面连接词，加入语气词、省略、打断、重复",
                blocking=False,
            ))

        dialogue_explain = re.findall(r'[」」"][^。！？]{0,30}(?:这么说|这样说是|这句话|这话)(?:是因为|意思是|表明)', text)
        if len(dialogue_explain) >= 2:
            result.issues.append(ReviewIssue(
                severity="medium",
                category="ai_flavor",
                location="对话",
                description=f"对话后跟解释性叙述（{len(dialogue_explain)}处）",
                evidence=f"示例: {dialogue_explain[:2]}",
                fix_hint="删除对话后的解释，让对话本身传达含义",
                blocking=False,
            ))

    def _check_basic_structure(self, text: str, result: ReviewResult) -> None:
        char_count = len(text.replace('\n', '').replace(' ', ''))
        if char_count < 2000:
            result.issues.append(ReviewIssue(
                severity="high",
                category="other",
                location="全文",
                description=f"字数不足（{char_count}字），网文章节建议4000字以上",
                evidence=f"当前正文字数: {char_count}",
                fix_hint="扩充场景描写、对话细节、内心独白，确保每章有足够的信息量",
                blocking=False,
            ))

        paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
        if len(paragraphs) < 5:
            result.issues.append(ReviewIssue(
                severity="medium",
                category="other",
                location="全文",
                description=f"段落数过少（{len(paragraphs)}段），可能缺乏节奏变化",
                evidence=f"当前段落数: {len(paragraphs)}",
                fix_hint="适当分段，每段聚焦一个动作/一个想法/一个场景元素",
                blocking=False,
            ))

    def _check_pov_consistency(self, text: str, result: ReviewResult) -> None:
        """POV感知检查 — 视角一致性/信息边界/感知过滤"""
        paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
        if len(paragraphs) < 5:
            return

        pov_violations = 0
        pov_evidence: List[str] = []

        for i, para in enumerate(paragraphs):
            char_mentions = re.findall(r'(?:他|她|它)(?:心中|心想|暗想|默默|暗自|心道)', para)
            if len(char_mentions) >= 2:
                unique_chars = set()
                for m in char_mentions:
                    unique_chars.add(m[0])
                if len(unique_chars) >= 2:
                    pov_violations += 1
                    pov_evidence.append(f"第{i+1}段: 同时进入{len(unique_chars)}个角色的内心")

            omniscient_patterns = re.findall(
                r'(?:谁也不知道|没有人知道|所有人都|每个人都在|谁都没注意|无人察觉)',
                para
            )
            if omniscient_patterns:
                pov_violations += 1
                pov_evidence.append(f"第{i+1}段: 上帝视角叙述「{omniscient_patterns[0]}」")

        if pov_violations >= 3:
            result.issues.append(ReviewIssue(
                severity="high",
                category="character",
                location="全文",
                description=f"POV视角混乱（{pov_violations}处视角跳跃/上帝视角）",
                evidence="; ".join(pov_evidence[:3]),
                fix_hint="固定一个POV角色，只描述该角色能感知到的信息。如需切换POV，用场景分隔符明确标记",
                blocking=False,
            ))
        elif pov_violations >= 1:
            result.issues.append(ReviewIssue(
                severity="medium",
                category="character",
                location="全文",
                description=f"POV视角存在{pov_violations}处不一致",
                evidence="; ".join(pov_evidence[:2]),
                fix_hint="检查是否无意中切换了视角，确保信息只来自当前POV角色的感知范围",
                blocking=False,
            ))

        info_boundary_violations = 0
        for para in paragraphs:
            if re.search(r'(?:他知道|她明白|他清楚|她了解).{0,20}(?:对方|别人|那人|对手)', para):
                info_boundary_violations += 1

        if info_boundary_violations >= 2:
            result.issues.append(ReviewIssue(
                severity="medium",
                category="character",
                location="全文",
                description=f"角色信息边界越界（{info_boundary_violations}处角色知道了不应知道的信息）",
                evidence=f"角色似乎能读取他人想法或知道不在场的信息",
                fix_hint="角色只能通过观察（看/听/闻）获取信息，不能直接知道他人的内心想法",
                blocking=False,
            ))

    def _check_hook_debt(
        self,
        text: str,
        result: ReviewResult,
        chapter_contract: Optional[Dict[str, Any]] = None,
    ) -> None:
        """钩子债务追踪 — 伏笔回收/开放循环/债务升级"""
        paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
        if len(paragraphs) < 3:
            return

        open_loops_created = 0
        open_loops_resolved = 0
        loop_evidence: List[str] = []

        for i, para in enumerate(paragraphs):
            if re.search(r'(?:难道|究竟|到底|为什么|怎么会|莫非|该不会|莫非是)', para):
                open_loops_created += 1
                loop_evidence.append(f"新循环#{open_loops_created}: 第{i+1}段「{para[:50]}...」")

            if re.search(r'(?:原来|终于|总算|果然|怪不得|难怪|原来如此)', para):
                open_loops_resolved += 1

        net_loops = open_loops_created - open_loops_resolved

        if net_loops > 5:
            result.issues.append(ReviewIssue(
                severity="high",
                category="continuity",
                location="全文",
                description=f"钩子债务过高（净增{net_loops}个开放循环，创建{open_loops_created}个/回收{open_loops_resolved}个）",
                evidence="; ".join(loop_evidence[:3]),
                fix_hint="控制每章新增悬念不超过3个，优先回收旧悬念再开新悬念。未回收悬念超过10个时暂停开新悬念",
                blocking=False,
            ))
        elif net_loops > 3:
            result.issues.append(ReviewIssue(
                severity="medium",
                category="continuity",
                location="全文",
                description=f"钩子债务偏高（净增{net_loops}个开放循环）",
                evidence=f"创建{open_loops_created}个新悬念，回收{open_loops_resolved}个",
                fix_hint="考虑在本章回收1-2个旧悬念，避免读者遗忘",
                blocking=False,
            ))

        if open_loops_created == 0 and open_loops_resolved == 0:
            result.issues.append(ReviewIssue(
                severity="low",
                category="continuity",
                location="全文",
                description="本章无悬念创建也无悬念回收，可能缺乏追读动力",
                evidence="未检测到悬念创建或回收标记",
                fix_hint="章末至少保留一个未闭合问题，制造追读欲望",
                blocking=False,
            ))

        if chapter_contract:
            directive = chapter_contract.get("chapter_directive", {})
            expected_question = directive.get("chapter_end_open_question", "")
            if expected_question:
                last_para = paragraphs[-1] if paragraphs else ""
                if expected_question not in last_para:
                    result.issues.append(ReviewIssue(
                        severity="medium",
                        category="continuity",
                        location="章末",
                        description=f"章末未体现预期的开放问题「{expected_question}」",
                        evidence=f"章末段落: {last_para[:100]}...",
                        fix_hint="在章末明确暗示或直接提出该问题，制造追读钩子",
                        blocking=False,
                    ))

    def _check_emotional_arc(self, text: str, result: ReviewResult) -> None:
        """情绪弧分析 — 情绪曲线/转折点/情绪过渡"""
        paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
        if len(paragraphs) < 5:
            return

        emotion_keywords = {
            "positive": ["笑", "喜", "乐", "兴奋", "激动", "满足", "幸福", "温暖", "安心", "得意", "骄傲", "感动"],
            "negative": ["怒", "悲", "恐", "焦虑", "绝望", "痛苦", "愤怒", "悲伤", "恐惧", "紧张", "压抑", "失落"],
            "neutral": ["平静", "冷静", "沉默", "思考", "观察", "等待", "回忆", "沉思"],
        }

        segment_size = max(1, len(paragraphs) // 5)
        emotion_curve: List[Dict[str, Any]] = []

        for seg_idx in range(5):
            start = seg_idx * segment_size
            end = start + segment_size if seg_idx < 4 else len(paragraphs)
            seg_text = " ".join(paragraphs[start:end])

            pos_count = sum(1 for kw in emotion_keywords["positive"] if kw in seg_text)
            neg_count = sum(1 for kw in emotion_keywords["negative"] if kw in seg_text)
            neu_count = sum(1 for kw in emotion_keywords["neutral"] if kw in seg_text)

            if pos_count > neg_count and pos_count > neu_count:
                tone = "positive"
            elif neg_count > pos_count and neg_count > neu_count:
                tone = "negative"
            else:
                tone = "neutral"

            emotion_curve.append({
                "segment": seg_idx + 1,
                "tone": tone,
                "positive": pos_count,
                "negative": neg_count,
                "neutral": neu_count,
            })

        tones = [e["tone"] for e in emotion_curve]
        unique_tones = len(set(tones))

        if unique_tones == 1:
            result.issues.append(ReviewIssue(
                severity="medium",
                category="continuity",
                location="全文",
                description=f"情绪弧过于平坦（全章情绪基调为{tones[0]}，无变化）",
                evidence=f"5段情绪分析: {' → '.join(tones)}",
                fix_hint="设计情绪起伏：紧张→舒缓→再紧张→爆发→余韵，制造情绪过山车效果",
                blocking=False,
            ))

        rapid_shifts = 0
        for i in range(1, len(tones)):
            if tones[i] != tones[i-1]:
                rapid_shifts += 1

        if rapid_shifts >= 4:
            result.issues.append(ReviewIssue(
                severity="medium",
                category="continuity",
                location="全文",
                description=f"情绪切换过于频繁（5段中切换{rapid_shifts}次）",
                evidence=f"情绪序列: {' → '.join(tones)}",
                fix_hint="情绪变化需要过渡段落，避免在相邻段落中情绪剧烈跳变",
                blocking=False,
            ))

        neg_segments = [e for e in emotion_curve if e["tone"] == "negative"]
        if len(neg_segments) >= 4:
            result.issues.append(ReviewIssue(
                severity="medium",
                category="continuity",
                location="全文",
                description=f"负面情绪占比过高（{len(neg_segments)}/5段为负面）",
                evidence=f"情绪分布: pos={sum(1 for e in emotion_curve if e['tone']=='positive')}, neg={len(neg_segments)}, neu={sum(1 for e in emotion_curve if e['tone']=='neutral')}",
                fix_hint="网文读者需要正向反馈，每章至少安排一个正向情绪段落（收获/突破/温暖）",
                blocking=False,
            ))

    def _check_pacing_consistency(self, text: str, result: ReviewResult) -> None:
        """节奏一致性检查 — 场景节奏/张力曲线/信息密度"""
        paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
        if len(paragraphs) < 5:
            return

        para_lengths = [len(p) for p in paragraphs]
        if not para_lengths:
            return

        action_indicators = [
            "打", "击", "冲", "闪", "躲", "刺", "砍", "劈", "轰", "爆",
            "飞", "跳", "跃", "跑", "追", "逃", "杀", "战", "斗", "攻",
        ]
        description_indicators = [
            "景色", "风景", "建筑", "天空", "阳光", "月光", "风", "云",
            "山", "水", "树", "花", "草", "街道", "房间", "宫殿",
        ]
        dialogue_indicators = ["「", "」", '"', '"', "：", "说", "道", "问", "答"]

        segments = []
        seg_size = max(1, len(paragraphs) // 4)
        for seg_idx in range(4):
            start = seg_idx * seg_size
            end = start + seg_size if seg_idx < 3 else len(paragraphs)
            seg_text = " ".join(paragraphs[start:end])

            action_count = sum(1 for kw in action_indicators if kw in seg_text)
            desc_count = sum(1 for kw in description_indicators if kw in seg_text)
            dialogue_count = sum(1 for kw in dialogue_indicators if kw in seg_text)

            total = action_count + desc_count + dialogue_count
            if total > 0:
                action_ratio = action_count / total
                desc_ratio = desc_count / total
                dialogue_ratio = dialogue_count / total
            else:
                action_ratio = desc_ratio = dialogue_ratio = 0

            if action_ratio > 0.5:
                pace = "fast"
            elif desc_ratio > 0.5:
                pace = "slow"
            elif dialogue_ratio > 0.5:
                pace = "dialogue"
            else:
                pace = "mixed"

            segments.append({
                "segment": seg_idx + 1,
                "pace": pace,
                "action_ratio": round(action_ratio, 2),
                "desc_ratio": round(desc_ratio, 2),
                "dialogue_ratio": round(dialogue_ratio, 2),
            })

        paces = [s["pace"] for s in segments]
        unique_paces = len(set(paces))

        if unique_paces == 1:
            result.issues.append(ReviewIssue(
                severity="medium",
                category="pacing",
                location="全文",
                description=f"节奏单一（全章节奏类型为{paces[0]}，无变化）",
                evidence=f"4段节奏分析: {' → '.join(paces)}",
                fix_hint="设计节奏变化：快节奏战斗→对话过渡→慢节奏描写→快节奏高潮，制造节奏对比",
                blocking=False,
            ))

        fast_segments = sum(1 for p in paces if p == "fast")
        slow_segments = sum(1 for p in paces if p == "slow")

        if fast_segments >= 3:
            result.issues.append(ReviewIssue(
                severity="medium",
                category="pacing",
                location="全文",
                description=f"快节奏占比过高（{fast_segments}/4段），读者可能疲劳",
                evidence=f"节奏分布: fast={fast_segments}, slow={slow_segments}, dialogue={sum(1 for p in paces if p=='dialogue')}, mixed={sum(1 for p in paces if p=='mixed')}",
                fix_hint="在快节奏段落之间插入慢节奏过渡，给读者喘息空间",
                blocking=False,
            ))

        if slow_segments >= 3:
            result.issues.append(ReviewIssue(
                severity="medium",
                category="pacing",
                location="全文",
                description=f"慢节奏占比过高（{slow_segments}/4段），可能导致读者流失",
                evidence=f"节奏分布: fast={fast_segments}, slow={slow_segments}",
                fix_hint="压缩描写段落，增加冲突或对话推进情节",
                blocking=False,
            ))

        if para_lengths:
            mean_len = sum(para_lengths) / len(para_lengths)
            if mean_len > 0:
                variance = sum((x - mean_len) ** 2 for x in para_lengths) / len(para_lengths)
                std_dev = variance ** 0.5
                cv = (std_dev / mean_len) * 100

                if cv < 20:
                    result.issues.append(ReviewIssue(
                        severity="medium",
                        category="pacing",
                        location="全文",
                        description=f"信息密度过于均匀（变异系数{cv:.1f}%），缺乏节奏张力",
                        evidence=f"段落长度均值{mean_len:.0f}字，标准差{std_dev:.0f}",
                        fix_hint="刻意制造信息密度对比：关键情节用短段落加速，渲染场景用长段落减速",
                        blocking=False,
                    ))

    def _check_continuity_37d(
        self,
        text: str,
        result: ReviewResult,
        chapter_contract: Optional[Dict[str, Any]] = None,
        master_setting: Optional[Dict[str, Any]] = None,
    ) -> None:
        """37维连续性检查 — 角色/世界/情节/叙事/风格全维度"""
        paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
        if len(paragraphs) < 3:
            return

        checks_passed = 0
        checks_total = 0

        # === 角色维度 (8项) ===
        checks_total += 1
        if master_setting:
            protagonist = master_setting.get("protagonist", {})
            protag_name = protagonist.get("name", "")
            if protag_name and protag_name in text:
                checks_passed += 1
            elif not protag_name:
                checks_passed += 1
        else:
            checks_passed += 1

        checks_total += 1
        char_names = set(re.findall(r'[\u4e00-\u9fff]{2,4}(?=说|道|问|答|喊|叫|吼|笑|哭|叹)', text))
        if len(char_names) <= 8:
            checks_passed += 1
        else:
            result.issues.append(ReviewIssue(
                severity="low",
                category="character",
                location="全文",
                description=f"单章出场角色过多（{len(char_names)}个有对话的角色）",
                evidence=f"对话角色: {', '.join(list(char_names)[:8])}",
                fix_hint="控制单章有台词角色不超过5-6个，避免读者混淆",
                blocking=False,
            ))

        checks_total += 1
        if master_setting:
            taboos = master_setting.get("constraints", {}).get("taboos", [])
            violated = [t for t in taboos if t in text]
            if not violated:
                checks_passed += 1
            else:
                result.issues.append(ReviewIssue(
                    severity="critical",
                    category="setting",
                    location="全文",
                    description=f"违反故事禁忌（{len(violated)}处）",
                    evidence=f"禁忌内容: {', '.join(violated[:3])}",
                    fix_hint="立即删除违反禁忌的内容，这些是故事设定的红线",
                    blocking=True,
                ))
        else:
            checks_passed += 1

        checks_total += 1
        if master_setting:
            anti_patterns = master_setting.get("constraints", {}).get("anti_patterns", [])
            found_anti = [p for p in anti_patterns if p in text]
            if not found_anti:
                checks_passed += 1
            else:
                result.issues.append(ReviewIssue(
                    severity="high",
                    category="setting",
                    location="全文",
                    description=f"使用了反模式内容（{len(found_anti)}处）",
                    evidence=f"反模式: {', '.join(found_anti[:3])}",
                    fix_hint="替换或删除反模式内容，这些是明确要避免的写作模式",
                    blocking=False,
                ))
        else:
            checks_passed += 1

        checks_total += 1
        dialogue_lines = re.findall(r'[「「"]([^「」"]+)[」」"]', text)
        if dialogue_lines:
            avg_dialogue_len = sum(len(d) for d in dialogue_lines) / len(dialogue_lines)
            if avg_dialogue_len > 60:
                result.issues.append(ReviewIssue(
                    severity="medium",
                    category="character",
                    location="对话",
                    description=f"对话平均长度过长（{avg_dialogue_len:.0f}字/句），可能变成演讲",
                    evidence=f"共{len(dialogue_lines)}句对话",
                    fix_hint="拆分长对话，加入动作打断和对方反应，让对话更像真实交流",
                    blocking=False,
                ))
            else:
                checks_passed += 1
        else:
            checks_passed += 1

        checks_total += 1
        if dialogue_lines:
            unique_speakers = len(char_names)
            if unique_speakers >= 2:
                checks_passed += 1
            else:
                result.issues.append(ReviewIssue(
                    severity="low",
                    category="character",
                    location="对话",
                    description="对话角色单一，缺乏多角色互动",
                    evidence=f"仅有{unique_speakers}个角色有对话",
                    fix_hint="增加角色间对话互动，丰富人物关系展示",
                    blocking=False,
                ))
        else:
            checks_passed += 1

        checks_total += 1
        action_verbs = len(re.findall(r'(?:打|击|冲|闪|躲|刺|砍|劈|轰|爆|飞|跳|跃|跑|追|逃|杀|战)', text))
        inner_thoughts = len(re.findall(r'(?:心想|暗想|心道|暗道|思忖|琢磨|寻思)', text))
        if action_verbs > inner_thoughts * 2:
            checks_passed += 1
        elif inner_thoughts > action_verbs * 2:
            result.issues.append(ReviewIssue(
                severity="medium",
                category="character",
                location="全文",
                description="内心独白过多，行动描写不足",
                evidence=f"动作词{action_verbs}个 vs 内心词{inner_thoughts}个",
                fix_hint="用行动展示角色性格，减少直接的心理描述",
                blocking=False,
            ))
        else:
            checks_passed += 1

        checks_total += 1
        if master_setting:
            char_registry = master_setting.get("character_registry", [])
            if char_registry:
                mentioned_chars = 0
                for char in char_registry:
                    if char.get("name", "") in text:
                        mentioned_chars += 1
                if mentioned_chars > 0:
                    checks_passed += 1
                else:
                    result.issues.append(ReviewIssue(
                        severity="low",
                        category="character",
                        location="全文",
                        description="已注册角色均未在本章出现",
                        evidence=f"注册角色数: {len(char_registry)}",
                        fix_hint="确保至少一个已注册角色在本章有戏份",
                        blocking=False,
                    ))
            else:
                checks_passed += 1
        else:
            checks_passed += 1

        # === 世界维度 (6项) ===
        checks_total += 1
        location_changes = len(re.findall(r'(?:来到|走到|进入|离开|回到|前往|到达|抵达)', text))
        if location_changes <= 5:
            checks_passed += 1
        else:
            result.issues.append(ReviewIssue(
                severity="low",
                category="setting",
                location="全文",
                description=f"场景切换过于频繁（{location_changes}次）",
                evidence=f"检测到{location_changes}次地点转换",
                fix_hint="减少场景切换，每个场景至少写500字再切换",
                blocking=False,
            ))

        checks_total += 1
        if master_setting:
            world_rules = master_setting.get("world_rules", [])
            if world_rules:
                rules_violated = 0
                for rule in world_rules:
                    rule_content = rule.get("content", "")
                    if rule_content and rule.get("scope") == "global":
                        pass
                checks_passed += 1
            else:
                checks_passed += 1
        else:
            checks_passed += 1

        checks_total += 1
        sensory_words = len(re.findall(r'(?:看到|听到|闻到|触到|感到|觉得|感觉|发现|注意)', text))
        if sensory_words >= 3:
            checks_passed += 1
        else:
            result.issues.append(ReviewIssue(
                severity="low",
                category="setting",
                location="全文",
                description="感官描写不足，场景缺乏沉浸感",
                evidence=f"感官词仅{sensory_words}个",
                fix_hint="每段场景至少包含2种感官细节（视觉+听觉/嗅觉/触觉）",
                blocking=False,
            ))

        checks_total += 1
        time_markers = len(re.findall(r'(?:早晨|中午|下午|傍晚|夜晚|深夜|黎明|黄昏|第二天|次日|几天后|数日后)', text))
        if time_markers >= 1:
            checks_passed += 1
        else:
            result.issues.append(ReviewIssue(
                severity="low",
                category="timeline",
                location="全文",
                description="缺少时间标记，读者可能不清楚故事发生的时间",
                evidence="未检测到时间标记词",
                fix_hint="在章节开头或场景转换时加入时间标记",
                blocking=False,
            ))

        checks_total += 1
        power_terms = len(re.findall(r'(?:境界|修为|灵力|真气|斗气|魔力|法力|等级|段位|层)', text))
        if power_terms > 0:
            power_consistency = True
            levels_found = set(re.findall(r'(?:筑基|金丹|元婴|化神|炼气|先天|后天|武者|武师|武王|武皇|武帝|斗者|斗师|斗灵|斗王|斗皇|斗宗|斗尊|斗圣|斗帝)', text))
            if len(levels_found) > 3:
                result.issues.append(ReviewIssue(
                    severity="medium",
                    category="setting",
                    location="全文",
                    description=f"力量体系术语过多（{len(levels_found)}个不同等级），可能造成混淆",
                    evidence=f"出现的等级: {', '.join(sorted(levels_found))}",
                    fix_hint="控制单章涉及的力量等级不超过3个",
                    blocking=False,
                ))
            else:
                checks_passed += 1
        else:
            checks_passed += 1

        checks_total += 1
        if master_setting:
            world_type = master_setting.get("story_engine", {}).get("world_type", "")
            if world_type:
                checks_passed += 1
            else:
                checks_passed += 1
        else:
            checks_passed += 1

        # === 情节维度 (8项) ===
        checks_total += 1
        conflict_markers = len(re.findall(r'(?:但是|然而|可是|不过|却|竟然|居然|反而|偏偏)', text))
        if conflict_markers >= 3:
            checks_passed += 1
        else:
            result.issues.append(ReviewIssue(
                severity="medium",
                category="plot",
                location="全文",
                description="冲突/转折不足，情节可能过于平铺直叙",
                evidence=f"转折词仅{conflict_markers}个",
                fix_hint="增加情节转折或冲突点，每章至少3个「但是」时刻",
                blocking=False,
            ))

        checks_total += 1
        cause_effect_pairs = len(re.findall(r'(?:因为|由于|所以|因此|于是|结果|导致|引发|造成)', text))
        if cause_effect_pairs >= 2:
            checks_passed += 1
        else:
            result.issues.append(ReviewIssue(
                severity="low",
                category="logic",
                location="全文",
                description="因果链不清晰，事件之间缺乏逻辑连接",
                evidence=f"因果连接词仅{cause_effect_pairs}个",
                fix_hint="确保每个事件都有前因后果，用行动-反应链条串联情节",
                blocking=False,
            ))

        checks_total += 1
        if chapter_contract:
            plot_structure = chapter_contract.get("plot_structure", {})
            must_cover = plot_structure.get("must_cover_nodes", [])
            if must_cover:
                covered = [n for n in must_cover if n in text]
                if len(covered) == len(must_cover):
                    checks_passed += 1
                else:
                    missed = [n for n in must_cover if n not in text]
                    result.issues.append(ReviewIssue(
                        severity="high",
                        category="plot",
                        location="全文",
                        description=f"未覆盖章纲必须节点（{len(missed)}/{len(must_cover)}个缺失）",
                        evidence=f"缺失节点: {', '.join(missed)}",
                        fix_hint="回看章纲，确保所有必须节点都在正文中体现",
                        blocking=False,
                    ))
            else:
                checks_passed += 1
        else:
            checks_passed += 1

        checks_total += 1
        cool_points = len(re.findall(r'(?:突破|碾压|击败|震惊|反转|觉醒|逆袭|打脸|装逼|扮猪吃虎)', text))
        if cool_points >= 1:
            checks_passed += 1
        else:
            result.issues.append(ReviewIssue(
                severity="medium",
                category="plot",
                location="全文",
                description="缺少爽点，读者可能缺乏满足感",
                evidence="未检测到爽点标记",
                fix_hint="每章至少安排一个爽点：突破/打脸/收获/反转",
                blocking=False,
            ))

        checks_total += 1
        first_300 = text[:300] if len(text) >= 300 else text
        hook_in_opening = any(kw in first_300 for kw in ["突然", "竟然", "难道", "为什么", "秘密", "危机", "危险", "死亡", "消失", "诡异", "奇怪"])
        if hook_in_opening:
            checks_passed += 1
        else:
            result.issues.append(ReviewIssue(
                severity="high",
                category="plot",
                location="开篇",
                description="开篇300字缺少钩子，读者可能流失",
                evidence=f"开篇: {first_300[:100]}...",
                fix_hint="开篇300字内必须有悬念/冲突/动作/疑问，抓住读者注意力",
                blocking=False,
            ))

        checks_total += 1
        last_200 = text[-200:] if len(text) >= 200 else text
        cliffhanger = any(kw in last_200 for kw in ["?", "难道", "究竟", "到底", "未知", "谜", "疑", "危险", "危机", "下一", "待续"])
        if cliffhanger:
            checks_passed += 1
        else:
            result.issues.append(ReviewIssue(
                severity="high",
                category="plot",
                location="章末",
                description="章末缺少悬念钩子，追读力不足",
                evidence=f"章末: {last_200[:100]}...",
                fix_hint="章末必须留一个未闭合问题或悬念，让读者想点下一章",
                blocking=False,
            ))

        checks_total += 1
        if chapter_contract:
            forbidden = chapter_contract.get("plot_structure", {}).get("forbidden_zones", [])
            violated_zones = [z for z in forbidden if z in text]
            if not violated_zones:
                checks_passed += 1
            else:
                result.issues.append(ReviewIssue(
                    severity="critical",
                    category="plot",
                    location="全文",
                    description=f"触及章纲禁区（{len(violated_zones)}处）",
                    evidence=f"禁区内容: {', '.join(violated_zones[:3])}",
                    fix_hint="立即删除触及禁区的内容",
                    blocking=True,
                ))
        else:
            checks_passed += 1

        checks_total += 1
        paragraphs_count = len(paragraphs)
        if paragraphs_count >= 10:
            checks_passed += 1
        else:
            result.issues.append(ReviewIssue(
                severity="low",
                category="plot",
                location="全文",
                description=f"段落数偏少（{paragraphs_count}段），情节展开可能不充分",
                evidence=f"共{paragraphs_count}段",
                fix_hint="适当分段并扩充情节细节",
                blocking=False,
            ))

        # === 叙事维度 (8项) ===
        checks_total += 1
        scene_transitions = len(re.findall(r'(?:与此同时|另一方面|画面一转|镜头切换|场景转换|另一边)', text))
        if scene_transitions <= len(paragraphs) // 5:
            checks_passed += 1
        else:
            result.issues.append(ReviewIssue(
                severity="low",
                category="continuity",
                location="全文",
                description=f"场景切换标记过多（{scene_transitions}处），叙事碎片化",
                evidence=f"共{len(paragraphs)}段，{scene_transitions}次切换",
                fix_hint="减少场景跳跃，用更自然的过渡连接场景",
                blocking=False,
            ))

        checks_total += 1
        flashback_markers = len(re.findall(r'(?:回想|回忆|记得|曾经|以前|过去|那时|当年|从前)', text))
        if flashback_markers <= 3:
            checks_passed += 1
        else:
            result.issues.append(ReviewIssue(
                severity="medium",
                category="continuity",
                location="全文",
                description=f"回忆/闪回过多（{flashback_markers}处），打断叙事节奏",
                evidence=f"检测到{flashback_markers}处回忆标记",
                fix_hint="将必要背景信息融入当前场景，减少独立闪回段落",
                blocking=False,
            ))

        checks_total += 1
        show_vs_tell = len(re.findall(r'(?:他是|她是|他很|她很|他非常|她非常|他是一个|她是一个)', text))
        if show_vs_tell <= 5:
            checks_passed += 1
        else:
            result.issues.append(ReviewIssue(
                severity="medium",
                category="continuity",
                location="全文",
                description=f"直接告诉(tell)过多（{show_vs_tell}处），缺少展示(show)",
                evidence=f"检测到{show_vs_tell}处「他是/她很」等直接描述",
                fix_hint="用行动和对话展示角色特质，而非直接告诉读者",
                blocking=False,
            ))

        checks_total += 1
        if len(text) >= 500:
            first_half = text[:len(text)//2]
            second_half = text[len(text)//2:]
            first_entities = set(re.findall(r'[\u4e00-\u9fff]{2,4}', first_half))
            second_entities = set(re.findall(r'[\u4e00-\u9fff]{2,4}', second_half))
            if first_entities and second_entities:
                overlap = len(first_entities & second_entities) / max(len(first_entities | second_entities), 1)
                if overlap > 0.3:
                    checks_passed += 1
                else:
                    result.issues.append(ReviewIssue(
                        severity="low",
                        category="continuity",
                        location="全文",
                        description="前后半章关键词重叠度低，叙事可能不连贯",
                        evidence=f"关键词重叠率: {overlap:.1%}",
                        fix_hint="确保前后半章有主题或人物上的连贯性",
                        blocking=False,
                    ))
            else:
                checks_passed += 1
        else:
            checks_passed += 1

        checks_total += 1
        foreshadowing_planted = len(re.findall(r'(?:似乎|好像|隐约|仿佛|莫名|不知为何|说不清|道不明)', text))
        if foreshadowing_planted <= 5:
            checks_passed += 1
        else:
            result.issues.append(ReviewIssue(
                severity="low",
                category="continuity",
                location="全文",
                description=f"模糊暗示过多（{foreshadowing_planted}处），伏笔不够明确",
                evidence=f"检测到{foreshadowing_planted}处模糊表述",
                fix_hint="伏笔应具体而非模糊，减少「似乎」「好像」等不确定表述",
                blocking=False,
            ))

        checks_total += 1
        chapter_goal_mentioned = False
        if chapter_contract:
            goal = chapter_contract.get("chapter_directive", {}).get("goal", "")
            if goal and goal in text:
                chapter_goal_mentioned = True
                checks_passed += 1
            elif goal:
                result.issues.append(ReviewIssue(
                    severity="medium",
                    category="plot",
                    location="全文",
                    description=f"本章目标「{goal}」未在正文中体现",
                    evidence=f"目标: {goal}",
                    fix_hint="确保正文围绕章纲目标展开",
                    blocking=False,
                ))
            else:
                checks_passed += 1
        else:
            checks_passed += 1

        checks_total += 1
        word_count = len(text.replace(' ', '').replace('\n', '').replace('\r', ''))
        if word_count >= 4000:
            checks_passed += 1
        elif word_count >= 2000:
            result.issues.append(ReviewIssue(
                severity="medium",
                category="other",
                location="全文",
                description=f"字数偏少（{word_count}字），网文章节建议4000字以上",
                evidence=f"当前字数: {word_count}",
                fix_hint="扩充场景描写、对话细节、内心独白",
                blocking=False,
            ))
        else:
            result.issues.append(ReviewIssue(
                severity="high",
                category="other",
                location="全文",
                description=f"字数严重不足（{word_count}字）",
                evidence=f"当前字数: {word_count}",
                fix_hint="大幅扩充内容，确保每章有足够的信息量",
                blocking=False,
            ))

        checks_total += 1
        if dialogue_lines:
            dialogue_ratio = sum(len(d) for d in dialogue_lines) / max(word_count, 1)
            if 0.2 <= dialogue_ratio <= 0.6:
                checks_passed += 1
            elif dialogue_ratio < 0.1:
                result.issues.append(ReviewIssue(
                    severity="low",
                    category="character",
                    location="全文",
                    description="对话占比过低，可能缺乏人物互动",
                    evidence=f"对话占比: {dialogue_ratio:.1%}",
                    fix_hint="增加角色间对话，用对话推进冲突和展示关系",
                    blocking=False,
                ))
            else:
                checks_passed += 1
        else:
            checks_passed += 1

        # === 风格维度 (7项) ===
        checks_total += 1
        unique_chars = len(set(re.findall(r'[\u4e00-\u9fff]', text)))
        if unique_chars >= 500:
            checks_passed += 1
        else:
            result.issues.append(ReviewIssue(
                severity="low",
                category="style",
                location="全文",
                description=f"词汇丰富度偏低（{unique_chars}个不重复汉字）",
                evidence=f"不重复汉字: {unique_chars}",
                fix_hint="丰富词汇量，避免重复使用相同词语",
                blocking=False,
            ))

        checks_total += 1
        sentence_enders = len(re.findall(r'[。！？]', text))
        if sentence_enders > 0:
            avg_sentence_len = word_count / sentence_enders
            if 15 <= avg_sentence_len <= 50:
                checks_passed += 1
            elif avg_sentence_len < 10:
                result.issues.append(ReviewIssue(
                    severity="low",
                    category="style",
                    location="全文",
                    description=f"平均句长过短（{avg_sentence_len:.0f}字），可能显得破碎",
                    evidence=f"总字数{word_count}，{sentence_enders}个句子",
                    fix_hint="适当合并短句，增加中等长度句子",
                    blocking=False,
                ))
            elif avg_sentence_len > 60:
                result.issues.append(ReviewIssue(
                    severity="medium",
                    category="style",
                    location="全文",
                    description=f"平均句长过长（{avg_sentence_len:.0f}字），阅读负担重",
                    evidence=f"总字数{word_count}，{sentence_enders}个句子",
                    fix_hint="拆分长句，控制平均句长在20-40字",
                    blocking=False,
                ))
            else:
                checks_passed += 1
        else:
            checks_passed += 1

        checks_total += 1
        adj_adv_count = len(re.findall(r'(?:的|地|得)(?:\w{1,2})', text))
        adj_ratio = adj_adv_count / max(word_count, 1)
        if adj_ratio < 0.08:
            checks_passed += 1
        else:
            result.issues.append(ReviewIssue(
                severity="low",
                category="style",
                location="全文",
                description=f"修饰词密度偏高（{adj_ratio:.1%}），文风可能过于华丽",
                evidence=f"修饰词占比: {adj_ratio:.1%}",
                fix_hint="精简形容词和副词，用名词和动词驱动叙事",
                blocking=False,
            ))

        checks_total += 1
        passive_voice = len(re.findall(r'(?:被|给|让|叫|受|遭|挨)', text))
        passive_ratio = passive_voice / max(word_count, 1)
        if passive_ratio < 0.02:
            checks_passed += 1
        else:
            result.issues.append(ReviewIssue(
                severity="low",
                category="style",
                location="全文",
                description=f"被动语态偏多（{passive_ratio:.1%}），削弱了动作的力量感",
                evidence=f"被动标记: {passive_voice}处",
                fix_hint="将被动句改为主动句，增强动作的冲击力",
                blocking=False,
            ))

        checks_total += 1
        repetition_pattern = re.findall(r'(\w{2,3})\1{2,}', text)
        if len(repetition_pattern) <= 3:
            checks_passed += 1
        else:
            result.issues.append(ReviewIssue(
                severity="low",
                category="style",
                location="全文",
                description=f"词语重复过多（{len(repetition_pattern)}处连续重复）",
                evidence=f"重复模式: {repetition_pattern[:3]}",
                fix_hint="检查并替换重复使用的词语",
                blocking=False,
            ))

        checks_total += 1
        if chapter_contract:
            style_priority = chapter_contract.get("reasoning", {}).get("style_priority", "")
            if style_priority:
                checks_passed += 1
            else:
                checks_passed += 1
        else:
            checks_passed += 1

        checks_total += 1
        paragraph_variety = len(set(len(p) for p in paragraphs)) / max(len(paragraphs), 1)
        if paragraph_variety > 0.3:
            checks_passed += 1
        else:
            result.issues.append(ReviewIssue(
                severity="low",
                category="style",
                location="全文",
                description="段落长度过于统一，缺乏视觉节奏",
                evidence=f"段落长度变化率: {paragraph_variety:.1%}",
                fix_hint="刻意变化段落长度，制造视觉节奏感",
                blocking=False,
            ))

        if checks_total > 0:
            pass_rate = checks_passed / checks_total
            if pass_rate < 0.6:
                result.issues.append(ReviewIssue(
                    severity="high",
                    category="other",
                    location="全文",
                    description=f"37维连续性检查通过率偏低（{checks_passed}/{checks_total}，{pass_rate:.0%}）",
                    evidence=f"通过{checks_passed}项/共{checks_total}项",
                    fix_hint="优先修复高严重性问题，逐步提升通过率至80%以上",
                    blocking=False,
                ))

    def _llm_deep_review(
        self,
        chapter: int,
        chapter_text: str,
        chapter_contract: Optional[Dict[str, Any]],
        master_setting: Optional[Dict[str, Any]],
        previous_summary: str,
    ) -> List[Dict[str, Any]]:
        text_preview = chapter_text[:3000] if len(chapter_text) > 3000 else chapter_text

        contract_info = ""
        if chapter_contract:
            directive = chapter_contract.get("chapter_directive", {})
            plot_structure = chapter_contract.get("plot_structure", {})
            contract_info = f"""
## 章纲合同
- 本章目标: {directive.get('goal', '未指定')}
- 必须覆盖节点: {', '.join(plot_structure.get('must_cover_nodes', [])) or '无'}
- 本章禁区: {', '.join(plot_structure.get('forbidden_zones', [])) or '无'}
- CBN: {plot_structure.get('CBN', '未指定')}
- CEN: {plot_structure.get('CEN', '未指定')}
"""

        setting_info = ""
        if master_setting:
            constraints = master_setting.get("constraints", {})
            protagonist = master_setting.get("protagonist", {})
            setting_info = f"""
## 主设定
- 主角: {protagonist.get('name', '未知')}
- 核心欲望: {protagonist.get('core_desire', '未知')}
- 致命缺陷: {protagonist.get('fatal_flaw', '未知')}
- 禁忌: {', '.join(constraints.get('taboos', [])) or '无'}
- 反模式: {', '.join(constraints.get('anti_patterns', [])) or '无'}
"""

        prev_info = f"\n## 上一章摘要\n{previous_summary}" if previous_summary else ""

        prompt = f"""你是章节审查员。你的职责是读完正文后，找出所有可验证的问题，输出结构化问题清单。
你不评分、不给建议、不写摘要性评价。你只找问题、给证据、给修复方向。

{contract_info}
{setting_info}
{prev_info}

## 第{chapter}章正文（前3000字预览）
{text_preview}
{"...(正文过长已截断)" if len(chapter_text) > 3000 else ""}

## 检查维度（按顺序执行）

### 1. 设定一致性 (category: setting)
- 角色能力是否与当前境界匹配
- 地点描述是否与世界观一致
- 物品/货币使用是否符合已建立规则

### 2. 时间线 (category: timeline)
- 本章时间是否与上章衔接
- 倒计时/截止日期是否正确推进
- 角色是否同时出现在两个地点

### 3. 叙事连贯 (category: continuity)
- 上章钩子是否有回应
- 场景转换是否有过渡
- 情绪弧是否连续

### 4. 角色一致性 (category: character)
- 对话风格是否符合角色特征
- 行为是否与已建立的性格/动机一致
- 角色是否使用了不应知道的信息

### 5. 逻辑 (category: logic)
- 因果关系是否成立
- 角色决策是否有合理动机
- 战斗/冲突结果是否符合力量对比

## 边界与禁区
- 不评分、不输出 overall_score、不输出 pass/fail
- 不评价文笔质量
- 不建议情节改动
- 只报可验证的问题——必须有 evidence

## 输出格式
严格按以下 JSON 格式输出（无其他文本）：
{{"issues": [{{"severity": "critical|high|medium|low", "category": "continuity|setting|character|timeline|logic|pacing|other", "location": "第N段 或 具体引用", "description": "问题描述", "evidence": "原文引用 vs 数据记录", "fix_hint": "修复方向", "blocking": true|false}}], "summary": "N个问题：X个阻断，Y个高优"}}"""

        result_text = llm.generate(prompt, params=GenerationParams(temperature=0.3, max_tokens=2000))

        try:
            json_str = result_text
            if "```json" in json_str:
                json_str = json_str.split("```json")[1].split("```")[0]
            elif "```" in json_str:
                json_str = json_str.split("```")[1].split("```")[0]
            data = json.loads(json_str.strip())
            return data.get("issues", [])
        except (json.JSONDecodeError, KeyError, IndexError):
            return []

    def review_with_contract(
        self,
        chapter: int,
        chapter_text: str,
        project_root: str = "",
    ) -> ReviewResult:
        if project_root:
            self.project_root = Path(project_root)

        ss = self._get_story_system()
        master = ss.get_master_setting()
        chapter_contract = ss.get_chapter_contract(chapter)

        prev_summary = ""
        if chapter > 1:
            prev_summary_path = self.project_root / ".webnovel" / "summaries" / f"ch{chapter - 1:04d}.md"
            if prev_summary_path.exists():
                prev_summary = prev_summary_path.read_text(encoding="utf-8")[:500]

        return self.review_chapter(
            chapter=chapter,
            chapter_text=chapter_text,
            chapter_contract=chapter_contract,
            master_setting=master,
            previous_summary=prev_summary,
            use_llm=True,
        )

    def quick_check(self, chapter_text: str) -> ReviewResult:
        return self.review_chapter(
            chapter=0,
            chapter_text=chapter_text,
            use_llm=False,
        )

    def build_fulfillment_check(
        self,
        chapter: int,
        chapter_text: str,
        chapter_contract: Dict[str, Any],
    ) -> Dict[str, Any]:
        plot_structure = chapter_contract.get("plot_structure", {})
        must_cover = plot_structure.get("must_cover_nodes", [])
        forbidden = plot_structure.get("forbidden_zones", [])

        covered = []
        missed = []
        for node in must_cover:
            if node in chapter_text:
                covered.append(node)
            else:
                missed.append(node)

        violated = []
        for zone in forbidden:
            if zone in chapter_text:
                violated.append(zone)

        directive = chapter_contract.get("chapter_directive", {})
        goal = directive.get("goal", "")
        goal_met = goal and goal in chapter_text

        return {
            "chapter": chapter,
            "must_cover_total": len(must_cover),
            "must_cover_covered": len(covered),
            "must_cover_missed": missed,
            "forbidden_total": len(forbidden),
            "forbidden_violated": violated,
            "goal_met": goal_met,
            "covered_nodes": covered,
            "missed_nodes": missed,
            "pending": [],
            "status": "passed" if not missed and not violated else "failed",
        }