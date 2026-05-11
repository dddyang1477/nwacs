#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quality System — NWACS 质量追踪与趋势分析模块

核心功能:
1. 审查指标记录 — 每章审查结果的结构化存储
2. 写作清单管理 — 必做/可选项追踪与完成率
3. 质量趋势分析 — 多维度评分趋势与风险预警
4. 追读力评估 — 钩子强度/爽点密度/微回报率
5. 维度评分 — 设定/角色/情节/文笔/节奏 五维评分
6. 风险标记 — 自动识别质量下滑与阻断风险
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _to_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _to_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


@dataclass
class ChapterQualityRecord:
    chapter: int
    overall_score: float = 0.0
    dimension_scores: Dict[str, float] = field(default_factory=dict)
    severity_counts: Dict[str, int] = field(default_factory=dict)
    checklist_score: float = 0.0
    checklist_completion: float = 0.0
    checklist_required_completion: float = 0.0
    hook_strength: str = ""
    cool_point_count: int = 0
    word_count: int = 0
    created_at: str = field(default_factory=_utc_now_iso)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "chapter": self.chapter,
            "overall_score": self.overall_score,
            "dimension_scores": self.dimension_scores,
            "severity_counts": self.severity_counts,
            "checklist_score": self.checklist_score,
            "checklist_completion": self.checklist_completion,
            "checklist_required_completion": self.checklist_required_completion,
            "hook_strength": self.hook_strength,
            "cool_point_count": self.cool_point_count,
            "word_count": self.word_count,
            "created_at": self.created_at,
        }


@dataclass
class QualityTrend:
    overall_avg: float = 0.0
    overall_min: float = 0.0
    overall_max: float = 0.0
    overall_std: float = 0.0
    dimension_avg: Dict[str, float] = field(default_factory=dict)
    severity_totals: Dict[str, int] = field(default_factory=dict)
    checklist_score_avg: float = 0.0
    checklist_completion_avg: float = 0.0
    count: int = 0
    trend_direction: str = "stable"
    risk_flags: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "overall_avg": round(self.overall_avg, 1),
            "overall_min": round(self.overall_min, 1),
            "overall_max": round(self.overall_max, 1),
            "overall_std": round(self.overall_std, 1),
            "dimension_avg": {k: round(v, 1) for k, v in self.dimension_avg.items()},
            "severity_totals": self.severity_totals,
            "checklist_score_avg": round(self.checklist_score_avg, 1),
            "checklist_completion_avg": round(self.checklist_completion_avg, 2),
            "count": self.count,
            "trend_direction": self.trend_direction,
            "risk_flags": self.risk_flags,
        }


class QualitySystem:
    """质量追踪系统 — 记录、分析、预警"""

    DEFAULT_WRITING_CHECKLIST = {
        "required": [
            {"id": "r1", "name": "开篇钩子", "desc": "前300字有强力钩子（悬念/冲突/动作开场）"},
            {"id": "r2", "name": "章末悬念", "desc": "章末有未闭合问题或悬念钩子"},
            {"id": "r3", "name": "角色一致性", "desc": "角色名字、性格、能力与设定一致"},
            {"id": "r4", "name": "因果连贯", "desc": "本章事件因果链完整，无逻辑跳跃"},
            {"id": "r5", "name": "去AI痕迹", "desc": "无明显AI写作特征（连接词/模板句式/匀速节奏）"},
            {"id": "r6", "name": "字数达标", "desc": "正文字数不低于4000字"},
        ],
        "optional": [
            {"id": "o1", "name": "爽点设计", "desc": "本章至少有一个爽点（打脸/突破/收获）"},
            {"id": "o2", "name": "感官描写", "desc": "每段场景至少包含2种感官细节"},
            {"id": "o3", "name": "人物弧光", "desc": "角色在本章中有微小变化或成长"},
            {"id": "o4", "name": "伏笔埋设", "desc": "本章埋设了新的伏笔或线索"},
            {"id": "o5", "name": "对话推进", "desc": "对话推进了冲突或揭示了角色关系"},
            {"id": "o6", "name": "节奏变化", "desc": "本章有明显的节奏变化（紧张/舒缓交替）"},
        ],
    }

    DIMENSION_WEIGHTS = {
        "setting": 0.15,
        "character": 0.20,
        "plot": 0.25,
        "style": 0.20,
        "pacing": 0.10,
        "ai_flavor": 0.10,
    }

    def __init__(self, project_root: str = ""):
        self.project_root = Path(project_root) if project_root else Path(".")
        self.quality_dir = self.project_root / ".webnovel" / "quality"
        self.quality_dir.mkdir(parents=True, exist_ok=True)
        self._records_cache: Optional[List[ChapterQualityRecord]] = None

    def _records_path(self) -> Path:
        return self.quality_dir / "quality_records.json"

    def _load_records(self) -> List[ChapterQualityRecord]:
        path = self._records_path()
        if not path.exists():
            return []
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(data, list):
                return []
            return [
                ChapterQualityRecord(
                    chapter=r.get("chapter", 0),
                    overall_score=r.get("overall_score", 0.0),
                    dimension_scores=r.get("dimension_scores", {}),
                    severity_counts=r.get("severity_counts", {}),
                    checklist_score=r.get("checklist_score", 0.0),
                    checklist_completion=r.get("checklist_completion", 0.0),
                    checklist_required_completion=r.get("checklist_required_completion", 0.0),
                    hook_strength=r.get("hook_strength", ""),
                    cool_point_count=r.get("cool_point_count", 0),
                    word_count=r.get("word_count", 0),
                    created_at=r.get("created_at", ""),
                )
                for r in data
            ]
        except (json.JSONDecodeError, KeyError):
            return []

    def _save_records(self, records: List[ChapterQualityRecord]) -> None:
        path = self._records_path()
        data = [r.to_dict() for r in records]
        tmp_path = path.with_suffix(path.suffix + ".tmp")
        tmp_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        tmp_path.replace(path)
        self._records_cache = None

    def _get_records(self) -> List[ChapterQualityRecord]:
        if self._records_cache is None:
            self._records_cache = self._load_records()
        return self._records_cache

    def record_chapter_quality(
        self,
        chapter: int,
        review_result: Optional[Dict[str, Any]] = None,
        checklist_result: Optional[Dict[str, Any]] = None,
        hook_strength: str = "",
        cool_point_count: int = 0,
        word_count: int = 0,
    ) -> ChapterQualityRecord:
        records = self._get_records()

        existing = None
        for i, r in enumerate(records):
            if r.chapter == chapter:
                existing = i
                break

        dimension_scores = self._calculate_dimension_scores(review_result)
        severity_counts = self._extract_severity_counts(review_result)
        overall_score = self._calculate_overall_score(dimension_scores, severity_counts)

        checklist_score = 0.0
        checklist_completion = 0.0
        checklist_required_completion = 0.0
        if checklist_result:
            checklist_score = _to_float(checklist_result.get("score", 0))
            checklist_completion = _to_float(checklist_result.get("completion_rate", 0))
            checklist_required_completion = _to_float(checklist_result.get("required_rate", 0))

        record = ChapterQualityRecord(
            chapter=chapter,
            overall_score=overall_score,
            dimension_scores=dimension_scores,
            severity_counts=severity_counts,
            checklist_score=checklist_score,
            checklist_completion=checklist_completion,
            checklist_required_completion=checklist_required_completion,
            hook_strength=hook_strength,
            cool_point_count=cool_point_count,
            word_count=word_count,
        )

        if existing is not None:
            records[existing] = record
        else:
            records.append(record)

        records.sort(key=lambda r: r.chapter)
        self._save_records(records)
        return record

    def _calculate_dimension_scores(
        self,
        review_result: Optional[Dict[str, Any]],
    ) -> Dict[str, float]:
        if not review_result:
            return {dim: 100.0 for dim in self.DIMENSION_WEIGHTS}

        issues = review_result.get("issues", [])
        if not issues:
            return {dim: 100.0 for dim in self.DIMENSION_WEIGHTS}

        category_penalties: Dict[str, float] = {dim: 0.0 for dim in self.DIMENSION_WEIGHTS}
        severity_weights = {"critical": 25, "high": 15, "medium": 8, "low": 3}

        for issue in issues:
            category = issue.get("category", "other")
            severity = issue.get("severity", "low")
            penalty = severity_weights.get(severity, 3)

            mapped = self._map_category_to_dimension(category)
            category_penalties[mapped] = category_penalties.get(mapped, 0) + penalty

        scores = {}
        for dim, weight in self.DIMENSION_WEIGHTS.items():
            penalty = category_penalties.get(dim, 0)
            scores[dim] = max(0, min(100, 100 - penalty))

        return scores

    def _map_category_to_dimension(self, category: str) -> str:
        mapping = {
            "setting": "setting",
            "timeline": "setting",
            "character": "character",
            "continuity": "plot",
            "logic": "plot",
            "ai_flavor": "ai_flavor",
            "pacing": "pacing",
        }
        return mapping.get(category, "style")

    def _extract_severity_counts(
        self,
        review_result: Optional[Dict[str, Any]],
    ) -> Dict[str, int]:
        if not review_result:
            return {"critical": 0, "high": 0, "medium": 0, "low": 0}

        issues = review_result.get("issues", [])
        counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
        for issue in issues:
            severity = issue.get("severity", "low")
            if severity in counts:
                counts[severity] += 1
        return counts

    def _calculate_overall_score(
        self,
        dimension_scores: Dict[str, float],
        severity_counts: Dict[str, int],
    ) -> float:
        weighted_sum = sum(
            score * self.DIMENSION_WEIGHTS.get(dim, 0.1)
            for dim, score in dimension_scores.items()
        )

        critical_penalty = severity_counts.get("critical", 0) * 10
        high_penalty = severity_counts.get("high", 0) * 3

        return max(0, min(100, weighted_sum - critical_penalty - high_penalty))

    def get_chapter_quality(self, chapter: int) -> Optional[ChapterQualityRecord]:
        records = self._get_records()
        for r in records:
            if r.chapter == chapter:
                return r
        return None

    def get_quality_trend(self, last_n: int = 20) -> QualityTrend:
        records = self._get_records()
        if not records:
            return QualityTrend()

        recent = records[-last_n:] if len(records) > last_n else records
        trend = QualityTrend()
        trend.count = len(recent)

        scores = [r.overall_score for r in recent]
        trend.overall_avg = sum(scores) / len(scores)
        trend.overall_min = min(scores)
        trend.overall_max = max(scores)

        if len(scores) > 1:
            variance = sum((s - trend.overall_avg) ** 2 for s in scores) / len(scores)
            trend.overall_std = math.sqrt(variance)

        all_dims: Dict[str, List[float]] = {}
        for r in recent:
            for dim, score in r.dimension_scores.items():
                all_dims.setdefault(dim, []).append(score)
        for dim, values in all_dims.items():
            trend.dimension_avg[dim] = sum(values) / len(values)

        for r in recent:
            for severity, count in r.severity_counts.items():
                trend.severity_totals[severity] = trend.severity_totals.get(severity, 0) + count

        checklist_scores = [r.checklist_score for r in recent if r.checklist_score > 0]
        if checklist_scores:
            trend.checklist_score_avg = sum(checklist_scores) / len(checklist_scores)

        checklist_completions = [r.checklist_completion for r in recent if r.checklist_completion > 0]
        if checklist_completions:
            trend.checklist_completion_avg = sum(checklist_completions) / len(checklist_completions)

        if len(scores) >= 3:
            first_half = scores[:len(scores) // 2]
            second_half = scores[len(scores) // 2:]
            first_avg = sum(first_half) / len(first_half)
            second_avg = sum(second_half) / len(second_half)
            diff = second_avg - first_avg
            if diff > 3:
                trend.trend_direction = "improving"
            elif diff < -3:
                trend.trend_direction = "declining"
            else:
                trend.trend_direction = "stable"

        trend.risk_flags = self._detect_risk_flags(trend, recent)

        return trend

    def _detect_risk_flags(
        self,
        trend: QualityTrend,
        records: List[ChapterQualityRecord],
    ) -> List[str]:
        flags: List[str] = []

        if trend.overall_avg < 75 and trend.count > 0:
            flags.append(f"审查均分偏低（{trend.overall_avg:.1f}），建议优先回看低分章节")

        critical_total = trend.severity_totals.get("critical", 0)
        high_total = trend.severity_totals.get("high", 0)
        if critical_total > 0:
            flags.append(f"存在 {critical_total} 个 critical 问题，建议设为最高修复优先级")
        elif high_total >= 5:
            flags.append(f"high 问题累计 {high_total} 个，建议做批量修复专项")

        if trend.checklist_score_avg > 0 and trend.checklist_score_avg < 80:
            flags.append(f"写作清单平均分偏低（{trend.checklist_score_avg:.1f}），建议加强执行清单落地")

        if trend.checklist_completion_avg > 0 and trend.checklist_completion_avg < 0.7:
            flags.append(f"写作清单完成率仅 {trend.checklist_completion_avg * 100:.1f}%，建议减少每章可选项数量")

        if trend.trend_direction == "declining":
            flags.append("质量趋势持续下滑，建议暂停新章节写作，优先修复累积问题")

        ai_flavor_avg = trend.dimension_avg.get("ai_flavor", 100)
        if ai_flavor_avg < 70:
            flags.append(f"AI味维度评分偏低（{ai_flavor_avg:.1f}），建议加强去AI痕迹处理")

        pacing_avg = trend.dimension_avg.get("pacing", 100)
        if pacing_avg < 70:
            flags.append(f"节奏维度评分偏低（{pacing_avg:.1f}），建议检查章节节奏变化")

        if not flags:
            flags.append("近期质量指标整体稳定，暂无高优先级风险")

        return flags

    def generate_quality_report(self, last_n: int = 20) -> str:
        trend = self.get_quality_trend(last_n)
        records = self._get_records()
        recent = records[-last_n:] if len(records) > last_n else records

        now_text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lines: List[str] = []

        lines.append("# 质量趋势报告")
        lines.append("")
        lines.append(f"- 生成时间: {now_text}")
        lines.append(f"- 统计窗口: 最近 {trend.count} 章")
        lines.append(f"- 趋势方向: {trend.trend_direction}")
        lines.append("")

        lines.append("## 总览")
        lines.append("")
        lines.append(f"- 审查均分: {trend.overall_avg:.1f}")
        lines.append(f"- 分数区间: {trend.overall_min:.1f} ~ {trend.overall_max:.1f}")
        lines.append(f"- 标准差: {trend.overall_std:.1f}")
        lines.append(f"- 清单平均分: {trend.checklist_score_avg:.1f}")
        lines.append(f"- 清单平均完成率: {trend.checklist_completion_avg * 100:.1f}%")
        lines.append("")

        lines.append("## 维度均分")
        lines.append("")
        lines.append("| 维度 | 平均分 | 权重 |")
        lines.append("|---|---:|---:|")
        for dim in sorted(trend.dimension_avg.keys()):
            weight = self.DIMENSION_WEIGHTS.get(dim, 0) * 100
            lines.append(f"| {dim} | {trend.dimension_avg[dim]:.1f} | {weight:.0f}% |")
        lines.append("")

        lines.append("## 严重级别汇总")
        lines.append("")
        lines.append("| 等级 | 数量 |")
        lines.append("|---|---:|")
        for level in ("critical", "high", "medium", "low"):
            lines.append(f"| {level} | {trend.severity_totals.get(level, 0)} |")
        lines.append("")

        lines.append("## 章节质量明细")
        lines.append("")
        lines.append("| 章节 | 总分 | 清单分 | 完成率 | Critical | High | Medium | Low |")
        lines.append("|---:|---:|---:|---:|---:|---:|---:|---:|")
        for r in recent:
            lines.append(
                f"| {r.chapter} | {r.overall_score:.1f} | {r.checklist_score:.1f} | "
                f"{r.checklist_completion * 100:.0f}% | "
                f"{r.severity_counts.get('critical', 0)} | "
                f"{r.severity_counts.get('high', 0)} | "
                f"{r.severity_counts.get('medium', 0)} | "
                f"{r.severity_counts.get('low', 0)} |"
            )
        lines.append("")

        lines.append("## 风险提示")
        lines.append("")
        for item in trend.risk_flags:
            lines.append(f"- {item}")
        lines.append("")

        return "\n".join(lines)

    def evaluate_checklist(
        self,
        chapter_text: str,
        completed_required: Optional[List[str]] = None,
        completed_optional: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        required_items = self.DEFAULT_WRITING_CHECKLIST["required"]
        optional_items = self.DEFAULT_WRITING_CHECKLIST["optional"]

        completed_required = completed_required or []
        completed_optional = completed_optional or []

        required_total = len(required_items)
        required_done = len([r for r in required_items if r["id"] in completed_required])
        optional_total = len(optional_items)
        optional_done = len([o for o in optional_items if o["id"] in completed_optional])

        total_items = required_total + optional_total
        total_done = required_done + optional_done

        completion_rate = total_done / total_items if total_items > 0 else 0
        required_rate = required_done / required_total if required_total > 0 else 0

        score = (required_rate * 70 + (optional_done / optional_total if optional_total > 0 else 0) * 30)

        return {
            "score": round(score, 1),
            "completion_rate": round(completion_rate, 2),
            "required_rate": round(required_rate, 2),
            "required_items": required_total,
            "completed_required": required_done,
            "optional_items": optional_total,
            "completed_optional": optional_done,
            "total_items": total_items,
            "total_done": total_done,
            "checklist": {
                "required": [
                    {**item, "completed": item["id"] in completed_required}
                    for item in required_items
                ],
                "optional": [
                    {**item, "completed": item["id"] in completed_optional}
                    for item in optional_items
                ],
            },
        }

    def evaluate_retention_power(
        self,
        chapter_text: str,
        chapter: int,
    ) -> Dict[str, Any]:
        char_count = len(chapter_text.replace('\n', '').replace(' ', ''))

        paragraphs = [p.strip() for p in chapter_text.split('\n') if p.strip()]
        first_300 = chapter_text[:300] if len(chapter_text) >= 300 else chapter_text
        last_200 = chapter_text[-200:] if len(chapter_text) >= 200 else chapter_text

        hook_keywords = ["突然", "竟然", "难道", "为什么", "秘密", "真相", "危机", "危险", "死亡", "消失"]
        hook_score = sum(1 for kw in hook_keywords if kw in first_300)

        suspense_keywords = ["?", "难道", "究竟", "到底", "未知", "谜", "疑"]
        suspense_score = sum(1 for kw in suspense_keywords if kw in last_200)

        cool_keywords = ["突破", "碾压", "击败", "震惊", "不可思议", "恐怖如斯", "竟然", "反转"]
        cool_count = sum(1 for kw in cool_keywords if kw in chapter_text)

        if hook_score >= 3:
            hook_level = "strong"
        elif hook_score >= 1:
            hook_level = "medium"
        else:
            hook_level = "weak"

        if suspense_score >= 2:
            suspense_level = "strong"
        elif suspense_score >= 1:
            suspense_level = "medium"
        else:
            suspense_level = "weak"

        micro_payoff_rate = cool_count / max(1, len(paragraphs)) * 10

        return {
            "chapter": chapter,
            "word_count": char_count,
            "hook_strength": hook_level,
            "hook_score": hook_score,
            "suspense_strength": suspense_level,
            "suspense_score": suspense_score,
            "cool_point_count": cool_count,
            "micro_payoff_rate": round(micro_payoff_rate, 2),
            "retention_score": round(
                (hook_score * 3 + suspense_score * 3 + cool_count * 2) / max(1, char_count / 1000) * 10,
                1,
            ),
        }

    def get_dimension_breakdown(self, chapter: int) -> Dict[str, Any]:
        record = self.get_chapter_quality(chapter)
        if not record:
            return {"error": f"第{chapter}章无质量记录"}

        return {
            "chapter": chapter,
            "overall_score": record.overall_score,
            "dimensions": [
                {
                    "name": dim,
                    "score": score,
                    "weight": self.DIMENSION_WEIGHTS.get(dim, 0),
                    "status": "good" if score >= 80 else ("warning" if score >= 60 else "critical"),
                }
                for dim, score in record.dimension_scores.items()
            ],
            "severity_breakdown": record.severity_counts,
            "checklist": {
                "score": record.checklist_score,
                "completion": record.checklist_completion,
                "required_completion": record.checklist_required_completion,
            },
        }

    # ============================================================
    # 节奏弧分析
    # ============================================================

    def analyze_pacing_arc(self, chapter_text: str) -> Dict[str, Any]:
        """节奏弧分析 — 段落级节奏变化检测"""
        paragraphs = [p.strip() for p in chapter_text.split('\n') if p.strip()]
        if len(paragraphs) < 5:
            return {"error": "段落数不足，无法分析节奏弧", "paragraph_count": len(paragraphs)}

        pacing_data: List[Dict[str, Any]] = []
        action_keywords = ["冲", "打", "杀", "飞", "跳", "跑", "击", "斩", "爆", "轰", "闪", "刺"]
        dialogue_indicators = ["「", "」", "\"", "\"", "：", "道", "说", "问", "答"]
        description_indicators = ["的", "地", "得", "着", "了", "过", "在", "有", "是"]
        inner_thought_indicators = ["心想", "暗想", "心道", "默默", "暗自", "心中"]

        for i, para in enumerate(paragraphs):
            para_len = len(para)
            if para_len < 10:
                continue

            action_count = sum(1 for kw in action_keywords if kw in para)
            dialogue_count = sum(1 for kw in dialogue_indicators if kw in para)
            desc_density = sum(1 for kw in description_indicators if kw in para) / max(1, para_len)
            thought_count = sum(1 for kw in inner_thought_indicators if kw in para)

            if action_count >= 3:
                para_type = "action"
                intensity = min(10, action_count * 3)
            elif dialogue_count >= 3:
                para_type = "dialogue"
                intensity = min(8, dialogue_count * 2)
            elif thought_count >= 1:
                para_type = "inner_thought"
                intensity = 3
            elif desc_density > 0.15:
                para_type = "description"
                intensity = 2
            else:
                para_type = "narration"
                intensity = 4

            pacing_data.append({
                "paragraph_index": i,
                "type": para_type,
                "intensity": intensity,
                "length": para_len,
            })

        if not pacing_data:
            return {"error": "无有效段落数据", "paragraph_count": len(paragraphs)}

        intensities = [p["intensity"] for p in pacing_data]
        avg_intensity = sum(intensities) / len(intensities)
        max_intensity = max(intensities)
        min_intensity = min(intensities)

        type_counts: Dict[str, int] = {}
        for p in pacing_data:
            t = p["type"]
            type_counts[t] = type_counts.get(t, 0) + 1

        transitions = 0
        for i in range(1, len(pacing_data)):
            if pacing_data[i]["type"] != pacing_data[i - 1]["type"]:
                transitions += 1

        intensity_changes = 0
        for i in range(1, len(intensities)):
            if abs(intensities[i] - intensities[i - 1]) >= 3:
                intensity_changes += 1

        issues: List[str] = []
        if transitions < len(pacing_data) * 0.1:
            issues.append("节奏过于单调，段落类型几乎无变化")
        if max_intensity - min_intensity < 3:
            issues.append("强度变化不足，缺乏张弛对比")
        if type_counts.get("action", 0) > len(pacing_data) * 0.6:
            issues.append("动作段落占比过高，可能导致读者疲劳")
        if type_counts.get("description", 0) > len(pacing_data) * 0.5:
            issues.append("描写段落占比过高，节奏可能拖沓")

        pacing_score = 100.0
        if issues:
            pacing_score = max(30, 100 - len(issues) * 15)

        return {
            "paragraph_count": len(paragraphs),
            "analyzed_segments": len(pacing_data),
            "avg_intensity": round(avg_intensity, 1),
            "max_intensity": max_intensity,
            "min_intensity": min_intensity,
            "intensity_range": max_intensity - min_intensity,
            "type_distribution": type_counts,
            "transitions": transitions,
            "intensity_changes": intensity_changes,
            "pacing_score": round(pacing_score, 1),
            "issues": issues,
            "pacing_data": pacing_data[:30],
        }

    # ============================================================
    # 情绪弧分析
    # ============================================================

    def analyze_emotional_arc(self, chapter_text: str) -> Dict[str, Any]:
        """情绪弧分析 — 情绪强度变化与角色情感轨迹"""
        paragraphs = [p.strip() for p in chapter_text.split('\n') if p.strip()]
        if len(paragraphs) < 5:
            return {"error": "段落数不足，无法分析情绪弧", "paragraph_count": len(paragraphs)}

        positive_words = [
            "笑", "喜", "乐", "欢", "悦", "欣", "慰", "安", "暖", "甜",
            "幸福", "开心", "快乐", "满足", "得意", "骄傲", "自豪", "感动",
            "胜利", "成功", "突破", "收获", "希望", "光明", "美好",
        ]
        negative_words = [
            "怒", "悲", "哀", "愁", "恨", "怨", "惧", "恐", "慌", "痛",
            "愤怒", "悲伤", "绝望", "恐惧", "痛苦", "焦虑", "不安", "压抑",
            "失败", "失去", "死亡", "黑暗", "孤独", "无助", "悔恨",
        ]
        neutral_words = [
            "想", "思", "虑", "疑", "惑", "迷", "茫", "静", "淡", "默",
            "思考", "沉思", "犹豫", "迟疑", "平静", "冷静", "淡然",
        ]

        emotional_data: List[Dict[str, Any]] = []
        for i, para in enumerate(paragraphs):
            para_len = len(para)
            if para_len < 10:
                continue

            pos_count = sum(1 for kw in positive_words if kw in para)
            neg_count = sum(1 for kw in negative_words if kw in para)
            neu_count = sum(1 for kw in neutral_words if kw in para)

            total = pos_count + neg_count + neu_count
            if total == 0:
                valence = 0
                intensity = 1
            else:
                valence = (pos_count - neg_count) / total
                intensity = min(10, total * 2)

            emotional_data.append({
                "paragraph_index": i,
                "valence": round(valence, 2),
                "intensity": intensity,
                "positive_count": pos_count,
                "negative_count": neg_count,
                "neutral_count": neu_count,
            })

        if not emotional_data:
            return {"error": "无有效情绪数据", "paragraph_count": len(paragraphs)}

        valences = [e["valence"] for e in emotional_data]
        intensities = [e["intensity"] for e in emotional_data]

        avg_valence = sum(valences) / len(valences)
        avg_intensity = sum(intensities) / len(intensities)

        valence_changes = 0
        for i in range(1, len(valences)):
            if abs(valences[i] - valences[i - 1]) > 0.3:
                valence_changes += 1

        positive_segments = sum(1 for v in valences if v > 0.2)
        negative_segments = sum(1 for v in valences if v < -0.2)
        neutral_segments = len(valences) - positive_segments - negative_segments

        arc_type = "flat"
        if valence_changes >= len(valences) * 0.3:
            if valences[0] < 0 and valences[-1] > 0:
                arc_type = "rising"
            elif valences[0] > 0 and valences[-1] < 0:
                arc_type = "falling"
            else:
                arc_type = "oscillating"
        elif avg_valence > 0.2:
            arc_type = "positive_flat"
        elif avg_valence < -0.2:
            arc_type = "negative_flat"

        issues: List[str] = []
        if arc_type == "flat" or arc_type == "positive_flat" or arc_type == "negative_flat":
            if valence_changes < 3:
                issues.append("情绪弧过于平直，缺乏情感起伏")
        if negative_segments > len(valences) * 0.7:
            issues.append("负面情绪占比过高，可能导致读者压抑")
        if avg_intensity < 2:
            issues.append("情绪强度偏低，情感描写可能不够深入")

        emotional_score = 100.0
        if issues:
            emotional_score = max(30, 100 - len(issues) * 15)

        return {
            "paragraph_count": len(paragraphs),
            "analyzed_segments": len(emotional_data),
            "avg_valence": round(avg_valence, 2),
            "avg_intensity": round(avg_intensity, 1),
            "valence_changes": valence_changes,
            "positive_segments": positive_segments,
            "negative_segments": negative_segments,
            "neutral_segments": neutral_segments,
            "arc_type": arc_type,
            "emotional_score": round(emotional_score, 1),
            "issues": issues,
            "emotional_data": emotional_data[:30],
        }

    def analyze_chapter_arcs(self, chapter_text: str) -> Dict[str, Any]:
        """综合分析 — 同时分析节奏弧和情绪弧"""
        pacing = self.analyze_pacing_arc(chapter_text)
        emotional = self.analyze_emotional_arc(chapter_text)

        pacing_score = pacing.get("pacing_score", 0)
        emotional_score = emotional.get("emotional_score", 0)
        combined_score = round((pacing_score + emotional_score) / 2, 1)

        all_issues = pacing.get("issues", []) + emotional.get("issues", [])

        return {
            "pacing_arc": pacing,
            "emotional_arc": emotional,
            "combined_score": combined_score,
            "all_issues": all_issues,
            "recommendation": self._generate_arc_recommendation(
                pacing, emotional, combined_score
            ),
        }

    def _generate_arc_recommendation(
        self,
        pacing: Dict[str, Any],
        emotional: Dict[str, Any],
        combined_score: float,
    ) -> str:
        if combined_score >= 85:
            return "节奏和情绪弧表现优秀，继续保持当前的写作节奏"
        elif combined_score >= 70:
            pacing_issues = pacing.get("issues", [])
            emotional_issues = emotional.get("issues", [])
            tips = []
            if pacing_issues:
                tips.append(f"节奏: {pacing_issues[0]}")
            if emotional_issues:
                tips.append(f"情绪: {emotional_issues[0]}")
            return "整体表现良好，" + "；".join(tips) if tips else "可小幅优化节奏变化"
        elif combined_score >= 50:
            return "节奏和情绪弧需要优化。建议：增加段落类型变化（动作/对话/描写交替），确保情绪有起伏而非平直"
        else:
            return "节奏和情绪弧存在明显问题。建议：重新规划章节的情绪曲线，确保有起承转合；增加节奏变化点，避免单调"