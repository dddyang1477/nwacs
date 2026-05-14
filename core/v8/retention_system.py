"""
NWACS 追读力系统 — 读者留存要素追踪引擎
基于网文行业最佳实践，追踪Hook/Cool-point/微兑现/债务四大维度
确保每章都有让读者欲罢不能的要素
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict
from datetime import datetime


@dataclass
class Hook:
    hook_type: str
    description: str
    chapter: int
    position: str = "opening"
    strength: int = 5
    resolved: bool = False
    resolution_chapter: Optional[int] = None
    created_at: str = ""

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class CoolPoint:
    point_type: str
    description: str
    chapter: int
    intensity: int = 5
    buildup_chapters: int = 0
    payoff_quality: str = "good"
    created_at: str = ""

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class MicroPayoff:
    description: str
    chapter: int
    debt_type: str
    related_debt_id: Optional[str] = None
    satisfaction: int = 5
    created_at: str = ""

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class ReaderDebt:
    debt_id: str
    debt_type: str
    description: str
    created_chapter: int
    expected_resolution_chapter: Optional[int] = None
    resolved: bool = False
    resolution_chapter: Optional[int] = None
    urgency: int = 5
    related_characters: List[str] = field(default_factory=list)
    created_at: str = ""

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()

    def to_dict(self) -> Dict:
        return asdict(self)


class RetentionSystem:
    """追读力系统 — 管理读者留存四要素

    Hook:     每章开头的钩子，抓住读者注意力
    CoolPoint: 爽点/高光时刻，让读者兴奋
    MicroPayoff: 微兑现，章内小回报让读者满足
    ReaderDebt: 读者债务，追踪对读者的承诺和伏笔
    """

    HOOK_TYPES = {
        "question": "疑问钩子 — 抛出悬念问题让读者好奇",
        "action": "动作钩子 — 开场即高潮，直接进入冲突",
        "emotional": "情感钩子 — 强烈情感冲击抓住读者",
        "mystery": "神秘钩子 — 引入未知元素制造好奇",
        "conflict": "冲突钩子 — 直接展示矛盾对立",
        "reversal": "反转钩子 — 颠覆读者预期",
        "stakes": "赌注钩子 — 展示高风险让读者紧张",
        "character": "角色钩子 — 引入魅力角色吸引读者",
    }

    COOL_POINT_TYPES = {
        "power_up": "升级突破 — 角色实力/地位提升",
        "face_slap": "打脸逆袭 — 反击看不起自己的人",
        "reveal": "身份揭露 — 隐藏身份/真相曝光",
        "treasure": "机缘获得 — 获得宝物/功法/机遇",
        "relationship": "关系突破 — 感情线进展",
        "revenge": "复仇成功 — 大仇得报",
        "recognition": "获得认可 — 被重要人物/群体认可",
        "domination": "碾压全场 — 展示绝对实力",
        "wisdom": "智谋取胜 — 以智慧化解危机",
        "save": "英雄救美/美救英雄 — 关键时刻救援",
    }

    DEBT_TYPES = {
        "foreshadowing": "伏笔 — 为后续情节埋下的线索",
        "question": "悬疑 — 提出的未解之谜",
        "conflict": "冲突 — 未解决的矛盾对立",
        "promise": "承诺 — 对读者做出的情节承诺",
        "mystery": "身世之谜 — 角色背景未解之谜",
        "goal": "目标 — 角色尚未达成的目标",
        "threat": "威胁 — 尚未解除的危险",
    }

    def __init__(self, project_dir: Path):
        self.project_dir = Path(project_dir)
        self.data_dir = self.project_dir / "retention_data"
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.hooks: List[Hook] = []
        self.cool_points: List[CoolPoint] = []
        self.micro_payoffs: List[MicroPayoff] = []
        self.reader_debts: List[ReaderDebt] = []

        self._load()

    def _get_file_path(self, name: str) -> Path:
        return self.data_dir / f"{name}.json"

    def _load(self) -> None:
        for attr, cls in [
            ("hooks", Hook), ("cool_points", CoolPoint),
            ("micro_payoffs", MicroPayoff), ("reader_debts", ReaderDebt),
        ]:
            fp = self._get_file_path(attr)
            if fp.exists():
                try:
                    with open(fp, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    getattr(self, attr).clear()
                    for item in data:
                        getattr(self, attr).append(cls(**item))
                except Exception as e:
                    print(f"[RetentionSystem] Load error for {attr}: {e}")

    def _save(self) -> None:
        for attr in ["hooks", "cool_points", "micro_payoffs", "reader_debts"]:
            fp = self._get_file_path(attr)
            items = [item.to_dict() for item in getattr(self, attr)]
            with open(fp, 'w', encoding='utf-8') as f:
                json.dump(items, f, ensure_ascii=False, indent=2)

    def add_hook(self, hook_type: str, description: str, chapter: int,
                 position: str = "opening", strength: int = 5) -> Hook:
        if hook_type not in self.HOOK_TYPES:
            hook_type = "question"
        hook = Hook(
            hook_type=hook_type,
            description=description,
            chapter=chapter,
            position=position,
            strength=min(10, max(1, strength)),
        )
        self.hooks.append(hook)
        self._save()
        return hook

    def add_cool_point(self, point_type: str, description: str, chapter: int,
                       intensity: int = 5, buildup_chapters: int = 0) -> CoolPoint:
        if point_type not in self.COOL_POINT_TYPES:
            point_type = "power_up"
        cp = CoolPoint(
            point_type=point_type,
            description=description,
            chapter=chapter,
            intensity=min(10, max(1, intensity)),
            buildup_chapters=buildup_chapters,
        )
        self.cool_points.append(cp)
        self._save()
        return cp

    def add_micro_payoff(self, description: str, chapter: int, debt_type: str,
                         related_debt_id: Optional[str] = None, satisfaction: int = 5) -> MicroPayoff:
        if debt_type not in self.DEBT_TYPES:
            debt_type = "foreshadowing"
        mp = MicroPayoff(
            description=description,
            chapter=chapter,
            debt_type=debt_type,
            related_debt_id=related_debt_id,
            satisfaction=min(10, max(1, satisfaction)),
        )
        self.micro_payoffs.append(mp)
        self._save()
        return mp

    def add_reader_debt(self, debt_type: str, description: str, created_chapter: int,
                        expected_resolution_chapter: Optional[int] = None,
                        urgency: int = 5,
                        related_characters: Optional[List[str]] = None) -> ReaderDebt:
        if debt_type not in self.DEBT_TYPES:
            debt_type = "foreshadowing"
        debt_id = f"debt_{created_chapter}_{len(self.reader_debts) + 1}"
        debt = ReaderDebt(
            debt_id=debt_id,
            debt_type=debt_type,
            description=description,
            created_chapter=created_chapter,
            expected_resolution_chapter=expected_resolution_chapter,
            urgency=min(10, max(1, urgency)),
            related_characters=related_characters or [],
        )
        self.reader_debts.append(debt)
        self._save()
        return debt

    def resolve_debt(self, debt_id: str, resolution_chapter: int) -> Optional[ReaderDebt]:
        for debt in self.reader_debts:
            if debt.debt_id == debt_id and not debt.resolved:
                debt.resolved = True
                debt.resolution_chapter = resolution_chapter
                self._save()
                return debt
        return None

    def get_chapter_retention_score(self, chapter: int) -> Dict[str, Any]:
        """计算章节追读力分数"""
        ch_hooks = [h for h in self.hooks if h.chapter == chapter]
        ch_cool_points = [cp for cp in self.cool_points if cp.chapter == chapter]
        ch_payoffs = [mp for mp in self.micro_payoffs if mp.chapter == chapter]

        hook_score = sum(h.strength for h in ch_hooks) * 3
        cool_score = sum(cp.intensity for cp in ch_cool_points) * 4
        payoff_score = sum(mp.satisfaction for mp in ch_payoffs) * 2

        unresolved_debts = [d for d in self.reader_debts if not d.resolved]
        resolved_this_chapter = [d for d in self.reader_debts if d.resolution_chapter == chapter]
        debt_score = len(resolved_this_chapter) * 5 - len(unresolved_debts) * 0.5

        total = hook_score + cool_score + payoff_score + debt_score
        max_possible = 100

        return {
            "chapter": chapter,
            "total_score": min(100, max(0, int(total))),
            "max_score": max_possible,
            "hook_count": len(ch_hooks),
            "hook_score": hook_score,
            "cool_point_count": len(ch_cool_points),
            "cool_score": cool_score,
            "micro_payoff_count": len(ch_payoffs),
            "payoff_score": payoff_score,
            "debts_resolved": len(resolved_this_chapter),
            "debts_unresolved": len(unresolved_debts),
            "debt_score": max(0, debt_score),
            "level": self._score_level(total),
            "suggestions": self._generate_retention_suggestions(
                ch_hooks, ch_cool_points, ch_payoffs, unresolved_debts, chapter
            ),
        }

    def _score_level(self, score: float) -> str:
        if score >= 80:
            return "极佳 — 读者欲罢不能"
        elif score >= 60:
            return "良好 — 读者会继续追读"
        elif score >= 40:
            return "一般 — 需要加强钩子和爽点"
        elif score >= 20:
            return "较差 — 读者可能弃书"
        else:
            return "危险 — 急需注入追读要素"

    def _generate_retention_suggestions(
        self, hooks: List[Hook], cool_points: List[CoolPoint],
        payoffs: List[MicroPayoff], unresolved_debts: List[ReaderDebt],
        chapter: int,
    ) -> List[str]:
        suggestions = []

        if not hooks:
            suggestions.append("🔗 本章缺少开篇钩子！建议在开头300字内设置悬念、冲突或情感冲击")
        elif len(hooks) == 1:
            suggestions.append("🔗 建议增加钩子类型多样性，尝试组合疑问+动作+情感钩子")

        if not cool_points:
            suggestions.append("⚡ 本章缺少爽点！建议加入升级突破、打脸逆袭或身份揭露等高光时刻")
        elif len(cool_points) < 2 and chapter > 3:
            suggestions.append("⚡ 爽点密度偏低，建议每章至少2个爽点保持读者兴奋度")

        if not payoffs and unresolved_debts:
            suggestions.append("🎁 本章缺少微兑现！有未解决的读者债务，建议在本章给予部分回报")

        urgent_debts = [d for d in unresolved_debts if d.urgency >= 7]
        if urgent_debts:
            suggestions.append(f"⚠️ 有{len(urgent_debts)}个高紧急度债务未解决，建议尽快兑现")

        old_debts = [d for d in unresolved_debts if chapter - d.created_chapter > 10]
        if old_debts:
            suggestions.append(f"⏰ 有{len(old_debts)}个债务超过10章未解决，读者可能已经遗忘或不满")

        if len(unresolved_debts) > 15:
            suggestions.append(f"📊 未解决债务总数({len(unresolved_debts)})过高，建议集中回收一批")

        if not suggestions:
            suggestions.append("✅ 本章追读力要素齐全，继续保持！")

        return suggestions

    def get_overall_retention_report(self) -> Dict[str, Any]:
        """生成整体追读力报告"""
        all_chapters = set()
        for h in self.hooks:
            all_chapters.add(h.chapter)
        for cp in self.cool_points:
            all_chapters.add(cp.chapter)
        for mp in self.micro_payoffs:
            all_chapters.add(mp.chapter)
        for d in self.reader_debts:
            all_chapters.add(d.created_chapter)

        chapter_scores = []
        for ch in sorted(all_chapters):
            chapter_scores.append(self.get_chapter_retention_score(ch))

        total_hooks = len(self.hooks)
        total_cool_points = len(self.cool_points)
        total_payoffs = len(self.micro_payoffs)
        total_debts = len(self.reader_debts)
        resolved_debts = len([d for d in self.reader_debts if d.resolved])
        unresolved_debts = total_debts - resolved_debts

        avg_score = sum(s["total_score"] for s in chapter_scores) / len(chapter_scores) if chapter_scores else 0

        hook_type_dist = {}
        for h in self.hooks:
            hook_type_dist[h.hook_type] = hook_type_dist.get(h.hook_type, 0) + 1

        cool_type_dist = {}
        for cp in self.cool_points:
            cool_type_dist[cp.point_type] = cool_type_dist.get(cp.point_type, 0) + 1

        return {
            "total_chapters_analyzed": len(all_chapters),
            "average_retention_score": round(avg_score, 1),
            "overall_level": self._score_level(avg_score),
            "total_hooks": total_hooks,
            "total_cool_points": total_cool_points,
            "total_micro_payoffs": total_payoffs,
            "total_debts": total_debts,
            "resolved_debts": resolved_debts,
            "unresolved_debts": unresolved_debts,
            "debt_resolution_rate": round(resolved_debts / total_debts * 100, 1) if total_debts > 0 else 100,
            "hook_type_distribution": hook_type_dist,
            "cool_point_distribution": cool_type_dist,
            "chapter_scores": chapter_scores,
            "unresolved_debt_details": [
                {
                    "debt_id": d.debt_id,
                    "type": d.debt_type,
                    "description": d.description,
                    "created_chapter": d.created_chapter,
                    "urgency": d.urgency,
                    "chapters_ago": (max(all_chapters) - d.created_chapter) if all_chapters else 0,
                }
                for d in self.reader_debts if not d.resolved
            ],
        }

    def analyze_chapter_for_retention(self, chapter: int, content: str,
                                      chapter_summary: str = "") -> Dict[str, Any]:
        """分析章节内容中的追读力要素（基于规则的快速分析）"""
        result = {
            "chapter": chapter,
            "detected_hooks": [],
            "detected_cool_points": [],
            "detected_payoffs": [],
            "detected_debts": [],
        }

        first_300 = content[:300] if len(content) > 300 else content

        hook_patterns = [
            ("question", ["？", "难道", "为什么", "怎么回事", "究竟"]),
            ("action", ["突然", "猛地", "瞬间", "轰", "砰", "杀"]),
            ("emotional", ["泪", "哭", "笑", "怒", "惊", "怕", "恨", "爱"]),
            ("mystery", ["神秘", "诡异", "奇怪", "未知", "秘密"]),
            ("conflict", ["对峙", "对抗", "冲突", "矛盾", "不服"]),
            ("reversal", ["竟然", "没想到", "反转", "原来", "其实"]),
            ("stakes", ["生死", "危机", "危险", "赌", "命"]),
        ]

        for htype, keywords in hook_patterns:
            for kw in keywords:
                if kw in first_300:
                    result["detected_hooks"].append({
                        "type": htype,
                        "keyword": kw,
                        "auto_added": False,
                    })
                    break

        cool_patterns = [
            ("power_up", ["突破", "升级", "晋升", "进阶", "觉醒", "领悟"]),
            ("face_slap", ["打脸", "震惊", "不敢相信", "目瞪口呆", "哑口无言"]),
            ("reveal", ["身份", "真相", "揭露", "曝光", "原来是你"]),
            ("treasure", ["宝物", "机缘", "奇遇", "秘籍", "神器"]),
            ("domination", ["碾压", "秒杀", "横扫", "无敌", "完胜"]),
        ]

        for ctype, keywords in cool_patterns:
            for kw in keywords:
                if kw in content:
                    result["detected_cool_points"].append({
                        "type": ctype,
                        "keyword": kw,
                        "auto_added": False,
                    })
                    break

        debt_patterns = [
            ("foreshadowing", ["伏笔", "暗示", "线索", "端倪", "苗头"]),
            ("question", ["？"]),
            ("mystery", ["身世", "来历", "秘密", "谜", "隐藏"]),
            ("threat", ["威胁", "危险", "敌人", "对手", "危机"]),
        ]

        for dtype, keywords in debt_patterns:
            for kw in keywords:
                if kw in content:
                    result["detected_debts"].append({
                        "type": dtype,
                        "keyword": kw,
                        "auto_added": False,
                    })
                    break

        return result

    def build_retention_prompt(self, chapter: int, chapter_summary: str = "") -> str:
        """构建追读力增强提示词，注入到章节生成prompt中"""
        unresolved = [d for d in self.reader_debts if not d.resolved]
        recent_hooks = [h for h in self.hooks if chapter - h.chapter <= 3 and not h.resolved]
        recent_cool = [cp for cp in self.cool_points if chapter - cp.chapter <= 3]

        parts = ["\n## 📈 追读力增强指令\n"]

        parts.append("### 本章必须包含的追读要素")
        parts.append("1. **开篇钩子**（前300字）：用悬念、冲突或情感冲击抓住读者")
        parts.append("2. **至少2个爽点**：升级突破/打脸逆袭/身份揭露/机缘获得")
        parts.append("3. **至少1个微兑现**：对之前伏笔或承诺的小回报")
        parts.append("4. **设置1-2个新债务**：为后续章节埋下伏笔或悬念")

        if unresolved:
            parts.append(f"\n### 待解决的读者债务（共{len(unresolved)}个）")
            urgent = [d for d in unresolved if d.urgency >= 7][:3]
            for d in urgent:
                parts.append(f"- ⚠️ [{d.debt_type}] {d.description}（第{d.created_chapter}章创建，紧急度{d.urgency}/10）")
            if len(unresolved) > 3:
                parts.append(f"- ... 还有{len(unresolved) - 3}个待解决债务")

        if recent_hooks:
            parts.append(f"\n### 近期未回收的钩子（共{len(recent_hooks)}个）")
            for h in recent_hooks[:3]:
                parts.append(f"- [{h.hook_type}] {h.description}（第{h.chapter}章）")

        parts.append("\n### 追读力写作原则")
        parts.append("- 每3000字至少1个爽点，每章至少2个")
        parts.append("- 钩子要具体，不要模糊的「他看到了不可思议的一幕」")
        parts.append("- 微兑现要让读者感到「作者没忘」，增强信任感")
        parts.append("- 新债务要有明确的回收计划，不要挖坑不填")

        return "\n".join(parts)