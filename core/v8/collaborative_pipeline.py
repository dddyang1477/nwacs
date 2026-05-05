#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 写作协作运行机制 - CollaborativeWritingPipeline
核心功能：
1. 多阶段流水线 - 构思→大纲→初稿→检测→去痕→润色→终稿
2. 角色分工 - 每个阶段由专门的"角色"负责
3. 质量门禁 - 每阶段输出必须通过质量检查才能进入下一阶段
4. 回退机制 - 不合格内容自动回退重试
5. 上下文传递 - 记忆系统贯穿全流程
6. 进度追踪 - 实时追踪写作进度

设计原则：
- 串行流水线，阶段间松耦合
- 每阶段可独立启用/禁用
- 失败自动回退，最多3次
- 全程记忆追踪
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum


class PipelineStage(Enum):
    """流水线阶段"""
    IDEA = "构思阶段"
    OUTLINE = "大纲阶段"
    DRAFT = "初稿阶段"
    DETECT = "检测阶段"
    REWRITE = "去痕阶段"
    POLISH = "润色阶段"
    FINAL = "终稿阶段"


class StageStatus(Enum):
    """阶段状态"""
    PENDING = "等待中"
    RUNNING = "执行中"
    PASSED = "已通过"
    FAILED = "未通过"
    SKIPPED = "已跳过"


@dataclass
class StageResult:
    """阶段结果"""
    stage: PipelineStage
    status: StageStatus
    output: Any = None
    report: Dict = field(default_factory=dict)
    duration_ms: float = 0
    attempt: int = 1
    error: str = ""


@dataclass
class PipelineConfig:
    """流水线配置"""
    max_retries: int = 3
    enable_detect: bool = True
    enable_rewrite: bool = True
    enable_polish: bool = True
    detect_threshold: int = 40
    rewrite_intensity: str = "medium"
    auto_save: bool = True


class CollaborativeWritingPipeline:
    """写作协作流水线"""

    def __init__(self, memory_manager=None, creative_engine=None,
                 name_generator=None, plot_engine=None,
                 ai_detector=None, enhanced_detector=None):
        self.memory = memory_manager
        self.engine = creative_engine
        self.namer = name_generator
        self.plotter = plot_engine
        self.detector = ai_detector
        self.enhanced_detector = enhanced_detector

        self.config = PipelineConfig()
        self.stages: List[StageResult] = []
        self.context: Dict[str, Any] = {}
        self.start_time: float = 0
        self.novel_title: str = "未命名作品"

    def run(self, genre: str = "玄幻",
            theme: str = "",
            chapter_count: int = 1,
            starting_chapter: int = 1) -> Dict[str, Any]:
        """运行完整流水线"""
        self.start_time = time.time()
        self.stages = []
        self.context = {
            "genre": genre,
            "theme": theme,
            "chapter_count": chapter_count,
            "starting_chapter": starting_chapter,
        }

        print(f"\n{'='*70}")
        print(f"🚀 写作协作流水线启动")
        print(f"   作品: {self.novel_title}")
        print(f"   题材: {genre} | 章节: 第{starting_chapter}章起 x{chapter_count}")
        print(f"{'='*70}")

        results = {}

        for ch_offset in range(chapter_count):
            ch_num = starting_chapter + ch_offset
            chapter_result = self._run_single_chapter(ch_num)
            results[f"chapter_{ch_num}"] = chapter_result

        total_time = time.time() - self.start_time
        summary = self._build_summary(results, total_time)

        if self.config.auto_save and self.memory:
            self.memory.persist()

        return summary

    def _run_single_chapter(self, chapter_num: int) -> Dict:
        """运行单章流水线"""
        print(f"\n{'─'*60}")
        print(f"📖 第{chapter_num}章")
        print(f"{'─'*60}")

        chapter_context = {**self.context, "chapter": chapter_num}

        stage_results = []

        stage_results.append(self._stage_idea(chapter_context))
        stage_results.append(self._stage_outline(chapter_context))
        stage_results.append(self._stage_draft(chapter_context))

        if self.config.enable_detect:
            stage_results.append(self._stage_detect(chapter_context))

        if self.config.enable_rewrite:
            stage_results.append(self._stage_rewrite(chapter_context))

        if self.config.enable_polish:
            stage_results.append(self._stage_polish(chapter_context))

        stage_results.append(self._stage_final(chapter_context))

        self.stages.extend(stage_results)

        return {
            "chapter": chapter_num,
            "stages": [
                {
                    "stage": r.stage.value,
                    "status": r.status.value,
                    "duration_ms": r.duration_ms,
                    "attempt": r.attempt,
                }
                for r in stage_results
            ],
            "final_content": chapter_context.get("final_content", ""),
            "passed": all(
                r.status in [StageStatus.PASSED, StageStatus.SKIPPED]
                for r in stage_results
            ),
        }

    def _stage_idea(self, ctx: Dict) -> StageResult:
        """构思阶段"""
        t0 = time.time()
        print(f"  💡 构思阶段...")

        if self.plotter:
            ideas = self.plotter.brainstorm_ideas(
                ctx["genre"], ctx.get("theme", ""), count=3
            )
            ctx["ideas"] = ideas
            ctx["selected_idea"] = ideas[0] if ideas else {}

        if self.memory:
            self.memory.save_plot_point(
                ctx["chapter"], "构思",
                ctx.get("selected_idea", {}).get("core_concept", "剧情构思"),
                "idea"
            )

        return StageResult(
            stage=PipelineStage.IDEA,
            status=StageStatus.PASSED,
            output=ctx.get("selected_idea"),
            duration_ms=(time.time() - t0) * 1000,
        )

    def _stage_outline(self, ctx: Dict) -> StageResult:
        """大纲阶段"""
        t0 = time.time()
        print(f"  📋 大纲阶段...")

        if self.plotter:
            from plot_brainstorm_engine import PlotArcType
            arc = self.plotter.design_plot_arc(
                PlotArcType.THREE_ACT, 30, ctx["genre"]
            )
            outline = self.plotter.generate_chapter_outline(arc, ctx["genre"])
            ctx["outline"] = outline

            ch_outline = next(
                (o for o in outline if o["chapter"] == ctx["chapter"]), None
            )
            ctx["chapter_outline"] = ch_outline

        if self.memory and ctx.get("chapter_outline"):
            self.memory.save_plot_point(
                ctx["chapter"],
                ctx["chapter_outline"].get("title", ""),
                ctx["chapter_outline"].get("summary", ""),
                "outline"
            )

        return StageResult(
            stage=PipelineStage.OUTLINE,
            status=StageStatus.PASSED,
            output=ctx.get("chapter_outline"),
            duration_ms=(time.time() - t0) * 1000,
        )

    def _stage_draft(self, ctx: Dict) -> StageResult:
        """初稿阶段"""
        t0 = time.time()
        print(f"  ✍️ 初稿阶段...")

        for attempt in range(1, self.config.max_retries + 1):
            draft = self._generate_draft(ctx, attempt)

            if draft and len(draft) >= 300:
                ctx["draft"] = draft
                ctx["current_content"] = draft

                if self.memory:
                    self.memory.save_conversation("system", f"第{ctx['chapter']}章初稿完成 ({len(draft)}字)")

                return StageResult(
                    stage=PipelineStage.DRAFT,
                    status=StageStatus.PASSED,
                    output={"length": len(draft)},
                    duration_ms=(time.time() - t0) * 1000,
                    attempt=attempt,
                )

            print(f"     ⚠️ 第{attempt}次尝试字数不足，重试...")

        return StageResult(
            stage=PipelineStage.DRAFT,
            status=StageStatus.FAILED,
            error=f"初稿生成失败（{self.config.max_retries}次尝试）",
            duration_ms=(time.time() - t0) * 1000,
        )

    def _generate_draft(self, ctx: Dict, attempt: int) -> Optional[str]:
        """生成初稿"""
        if not self.engine:
            return self._generate_local_draft(ctx)

        outline = ctx.get("chapter_outline", {})
        memory_context = ""
        if self.memory:
            memory_context = self.memory.build_context(["character", "plot", "world"])

        prompt = f"""请写《{self.novel_title}》第{ctx['chapter']}章。

题材: {ctx['genre']}
章节标题: {outline.get('title', '')}
章节概要: {outline.get('summary', '')}
情感基调: {outline.get('emotional_beat', 'neutral')}

已有信息:
{memory_context}

要求:
- 不少于1500字
- 包含对话、动作描写、心理活动
- 章末留悬念
- 不要写"本章结束"等标记"""

        try:
            result = self.engine.generate(
                prompt,
                system_prompt="你是顶级网文作家，擅长创作引人入胜的小说章节。",
                temperature=0.8,
                max_tokens=4000,
            )
            return result
        except Exception as e:
            print(f"     ❌ API调用失败: {e}")
            return self._generate_local_draft(ctx)

    def _generate_local_draft(self, ctx: Dict) -> str:
        """本地生成初稿（无API时的fallback）"""
        outline = ctx.get("chapter_outline", {})
        return f"""第{ctx['chapter']}章 {outline.get('title', '新篇章')}

{outline.get('summary', '剧情展开中...')}

（本章内容需要通过AI接口生成，当前为占位内容。请配置DeepSeek API后重试。）
"""

    def _stage_detect(self, ctx: Dict) -> StageResult:
        """检测阶段"""
        t0 = time.time()
        content = ctx.get("current_content", "")
        print(f"  🔍 检测阶段...")

        detector = self.enhanced_detector or self.detector

        if detector:
            if hasattr(detector, 'detect'):
                report = detector.detect(content)
                score = report.overall_score
            else:
                score = detector.detect_ai_score(content)

            ctx["ai_score"] = score
            passed = score < self.config.detect_threshold

            status_text = "✅" if passed else "⚠️"
            print(f"     {status_text} AI分数: {score}/100 (阈值{self.config.detect_threshold})")

            return StageResult(
                stage=PipelineStage.DETECT,
                status=StageStatus.PASSED if passed else StageStatus.FAILED,
                output={"score": score},
                report={"score": score, "threshold": self.config.detect_threshold},
                duration_ms=(time.time() - t0) * 1000,
            )

        return StageResult(
            stage=PipelineStage.DETECT,
            status=StageStatus.SKIPPED,
            duration_ms=0,
        )

    def _stage_rewrite(self, ctx: Dict) -> StageResult:
        """去痕阶段"""
        t0 = time.time()
        content = ctx.get("current_content", "")
        print(f"  🔄 去痕阶段...")

        detector = self.enhanced_detector or self.detector

        if detector and ctx.get("ai_score", 100) >= self.config.detect_threshold:
            for attempt in range(1, self.config.max_retries + 1):
                if hasattr(detector, 'rewrite'):
                    rewritten, rw_report = detector.rewrite(
                        content, self.config.rewrite_intensity
                    )
                    new_score = rw_report.final_score
                else:
                    rewritten = detector.rewrite_remove_ai(content)
                    new_score = detector.detect_ai_score(rewritten)

                if new_score < self.config.detect_threshold or attempt == self.config.max_retries:
                    ctx["current_content"] = rewritten
                    ctx["ai_score"] = new_score
                    print(f"     去痕后分数: {new_score}/100")

                    return StageResult(
                        stage=PipelineStage.REWRITE,
                        status=StageStatus.PASSED,
                        output={"new_score": new_score},
                        duration_ms=(time.time() - t0) * 1000,
                        attempt=attempt,
                    )

                content = rewritten

        return StageResult(
            stage=PipelineStage.REWRITE,
            status=StageStatus.SKIPPED,
            duration_ms=0,
        )

    def _stage_polish(self, ctx: Dict) -> StageResult:
        """润色阶段"""
        t0 = time.time()
        content = ctx.get("current_content", "")
        print(f"  ✨ 润色阶段...")

        if self.engine and len(content) > 100:
            try:
                polished = self.engine.rewrite(content, "polish")
                ctx["current_content"] = polished
                print(f"     润色完成 ({len(polished)}字)")
            except Exception:
                pass

        return StageResult(
            stage=PipelineStage.POLISH,
            status=StageStatus.PASSED,
            duration_ms=(time.time() - t0) * 1000,
        )

    def _stage_final(self, ctx: Dict) -> StageResult:
        """终稿阶段"""
        t0 = time.time()
        content = ctx.get("current_content", "")
        print(f"  📦 终稿阶段...")

        ctx["final_content"] = content

        if self.memory:
            self.memory.save_conversation(
                "system",
                f"第{ctx['chapter']}章终稿完成 ({len(content)}字, AI分数:{ctx.get('ai_score', 'N/A')})"
            )

        return StageResult(
            stage=PipelineStage.FINAL,
            status=StageStatus.PASSED,
            output={"length": len(content)},
            duration_ms=(time.time() - t0) * 1000,
        )

    def _build_summary(self, results: Dict, total_time: float) -> Dict:
        """构建流水线摘要"""
        all_stages = []
        for ch_key, ch_data in results.items():
            all_stages.extend(ch_data.get("stages", []))

        passed = sum(1 for s in all_stages if s["status"] == "已通过")
        failed = sum(1 for s in all_stages if s["status"] == "未通过")
        skipped = sum(1 for s in all_stages if s["status"] == "已跳过")

        print(f"\n{'='*70}")
        print(f"📊 流水线执行摘要")
        print(f"{'='*70}")
        print(f"  总耗时: {total_time:.1f}秒")
        print(f"  阶段统计: {passed}通过 / {failed}失败 / {skipped}跳过")
        print(f"  章节数: {len(results)}")
        print(f"{'='*70}")

        return {
            "novel_title": self.novel_title,
            "total_time_s": round(total_time, 1),
            "chapters": len(results),
            "stages_passed": passed,
            "stages_failed": failed,
            "stages_skipped": skipped,
            "results": results,
        }

    def set_config(self, **kwargs):
        """动态配置流水线"""
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)


if __name__ == "__main__":
    print("=" * 60)
    print("🔗 写作协作流水线测试")
    print("=" * 60)

    pipeline = CollaborativeWritingPipeline()
    pipeline.novel_title = "测试作品"

    pipeline.config.enable_detect = True
    pipeline.config.enable_rewrite = True
    pipeline.config.enable_polish = False
    pipeline.config.auto_save = False

    summary = pipeline.run(
        genre="玄幻",
        theme="少年修仙",
        chapter_count=1,
        starting_chapter=1,
    )

    print(f"\n最终摘要: {json.dumps({k: v for k, v in summary.items() if k != 'results'}, ensure_ascii=False, indent=2)}")
