#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 质量检测师 - QualityDetector

基于 DeepSeek API 实现：
1. AI痕迹检测 - 分析文本是否由AI生成
2. 文章质量评估 - 结构、可读性、文学性、连贯性
3. AI去痕重写 - 调用DeepSeek重写去除AI痕迹
4. 三轮检测流水线 - 检测→修改→再检测→输出/人工干预
"""

import json
import os
import re
import time
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


API_KEY = "sk-f3246fbd1eef446e9a11d78efefd9bba"
BASE_URL = "https://api.deepseek.com"
AI_TRACE_THRESHOLD = 40
QUALITY_THRESHOLD = 60
MAX_RETRY_ROUNDS = 3


class DetectionStatus(Enum):
    PASS = "pass"
    FAIL_AI_TRACE = "fail_ai_trace"
    FAIL_QUALITY = "fail_quality"
    FAIL_BOTH = "fail_both"
    MANUAL_REQUIRED = "manual_required"


@dataclass
class AITraceReport:
    score: float
    level: str
    indicators: List[str]
    confidence: float
    summary: str


@dataclass
class QualityReport:
    score: float
    structure_score: float
    readability_score: float
    literary_score: float
    coherence_score: float
    issues: List[str]
    suggestions: List[str]
    summary: str


@dataclass
class RoundResult:
    round_num: int
    ai_trace_report: AITraceReport
    quality_report: QualityReport
    passed: bool
    status: DetectionStatus
    rewritten_text: str = ""
    duration_seconds: float = 0.0


@dataclass
class PipelineResult:
    passed: bool
    final_text: str
    rounds: List[RoundResult]
    total_duration_seconds: float
    needs_manual: bool
    manual_reason: str = ""
    final_status: DetectionStatus = DetectionStatus.PASS


def _call_deepseek(prompt: str, system_prompt: str = "",
                   temperature: float = 0.3, max_tokens: int = 8000,
                   timeout: int = 120) -> Optional[str]:
    import requests
    try:
        url = f"{BASE_URL}/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        data = {
            "model": "deepseek-chat",
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        response = requests.post(url, headers=headers, json=data, timeout=timeout)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"   ❌ DeepSeek API调用失败: {e}")
        return None


def _parse_json_response(text: str) -> Dict[str, Any]:
    try:
        json_match = re.search(r'\{[\s\S]*\}', text)
        if json_match:
            return json.loads(json_match.group())
    except (json.JSONDecodeError, AttributeError):
        pass
    return {}


class QualityDetector:
    """质量检测师 - AI痕迹检测 + 文章质量评估 + AI去痕重写"""

    def __init__(self):
        self.detection_history: List[RoundResult] = []

    def detect_ai_traces(self, text: str) -> AITraceReport:
        local_result = None
        try:
            from ai_polisher import get_polisher
            polisher = get_polisher()
            local_result = polisher.detect_ai_traces(text)
        except ImportError:
            pass

        system_prompt = """你是一个专业的AI文本检测专家。你的任务是分析给定文本是否由AI生成。

请从以下维度分析：
1. 句式重复度 - AI倾向于使用相似的句式结构
2. 词汇多样性 - AI词汇使用较为单一、套路化
3. 情感自然度 - AI情感表达较为机械、缺乏真实感
4. 细节丰富度 - AI细节描写较为笼统、缺乏个性化
5. 逻辑连贯性 - AI逻辑过于完美、缺乏人类思维的跳跃
6. AI模板句式 - "值得注意的是""综上所述""通过...实现..."等
7. 虚化动词 - "进行""做出""加以"等万能动词
8. 情感直述 - "他感到""他觉得""他心想"等

请严格按以下JSON格式返回结果（不要包含其他内容）：
{
    "score": 数字(0-100,越高越像AI),
    "level": "low/medium/high",
    "indicators": ["具体AI特征1", "具体AI特征2", ...],
    "confidence": 数字(0-1),
    "summary": "简短总结"
}"""

        local_hint = ""
        if local_result and local_result["patterns_found"]:
            local_hint = f"\n【本地预检测结果】\n已发现{len(local_result['patterns_found'])}个AI特征模式:\n"
            for p in local_result["patterns_found"][:5]:
                local_hint += f"- {p['name']}: {p['count']}处 ({p['severity']})\n"

        prompt = f"""请分析以下文本的AI生成痕迹：
{local_hint}
【待检测文本】
{text[:8000]}

请返回JSON格式的检测结果。"""

        response = _call_deepseek(prompt, system_prompt, temperature=0.1, max_tokens=2000)
        if not response:
            if local_result:
                return AITraceReport(
                    score=float(local_result["total_score"]),
                    level=local_result["level"],
                    indicators=[p["name"] for p in local_result["patterns_found"]],
                    confidence=0.6,
                    summary=f"API不可用，使用本地检测: {local_result['level']}级别AI痕迹"
                )
            return AITraceReport(
                score=50.0, level="medium",
                indicators=["API调用失败，使用默认评分"],
                confidence=0.0,
                summary="检测服务不可用"
            )

        data = _parse_json_response(response)
        api_score = float(data.get("score", 50))

        if local_result:
            blended_score = api_score * 0.6 + local_result["total_score"] * 0.4
            blended_indicators = list(set(
                data.get("indicators", []) +
                [p["name"] for p in local_result["patterns_found"][:5]]
            ))
            return AITraceReport(
                score=round(blended_score, 1),
                level=str(data.get("level", local_result["level"])),
                indicators=blended_indicators,
                confidence=float(data.get("confidence", 0.7)),
                summary=str(data.get("summary", "")),
            )

        return AITraceReport(
            score=api_score,
            level=str(data.get("level", "medium")),
            indicators=data.get("indicators", []),
            confidence=float(data.get("confidence", 0.5)),
            summary=str(data.get("summary", "")),
        )

    def evaluate_quality(self, text: str) -> QualityReport:
        system_prompt = """你是一个资深网文编辑，擅长评估小说章节质量。

请从以下维度评分（每项0-100）：
1. 结构完整性 - 是否有清晰的开头、发展、高潮、结尾
2. 可读性 - 语言是否流畅、段落是否合理、标点是否恰当
3. 文学性 - 文笔是否优美、描写是否生动、修辞是否恰当
4. 连贯性 - 情节是否连贯、逻辑是否自洽、前后是否呼应

请严格按以下JSON格式返回结果：
{
    "structure_score": 数字,
    "readability_score": 数字,
    "literary_score": 数字,
    "coherence_score": 数字,
    "issues": ["问题1", "问题2", ...],
    "suggestions": ["建议1", "建议2", ...],
    "summary": "简短总结"
}"""

        prompt = f"""请评估以下小说章节的质量：

【章节内容】
{text[:8000]}

请返回JSON格式的评估结果。"""

        response = _call_deepseek(prompt, system_prompt, temperature=0.2, max_tokens=2000)
        if not response:
            return QualityReport(
                score=50.0, structure_score=50, readability_score=50,
                literary_score=50, coherence_score=50,
                issues=["API调用失败，使用默认评分"],
                suggestions=["请检查API配置"],
                summary="评估服务不可用"
            )

        data = _parse_json_response(response)
        scores = [
            float(data.get("structure_score", 50)),
            float(data.get("readability_score", 50)),
            float(data.get("literary_score", 50)),
            float(data.get("coherence_score", 50)),
        ]
        avg_score = sum(scores) / len(scores)

        return QualityReport(
            score=round(avg_score, 1),
            structure_score=float(data.get("structure_score", 50)),
            readability_score=float(data.get("readability_score", 50)),
            literary_score=float(data.get("literary_score", 50)),
            coherence_score=float(data.get("coherence_score", 50)),
            issues=data.get("issues", []),
            suggestions=data.get("suggestions", []),
            summary=str(data.get("summary", "")),
        )

    def remove_ai_traces(self, text: str, ai_report: AITraceReport,
                         quality_report: QualityReport) -> str:
        try:
            from ai_polisher import get_polisher, PolishLevel, WritingStyle
            polisher = get_polisher()

            if ai_report.score >= 60:
                level = PolishLevel.DEEP
            elif ai_report.score >= 30:
                level = PolishLevel.MEDIUM
            else:
                level = PolishLevel.LIGHT

            result = polisher.polish(text, level, WritingStyle.WEB_NOVEL)
            print(f"   ✅ AI润色器完成: AI痕迹 {result.ai_trace_before:.0f} → {result.ai_trace_after:.0f}")
            return result.polished

        except ImportError:
            pass

        issues_text = ""
        if ai_report.indicators:
            issues_text += "【AI痕迹问题】\n" + "\n".join(
                f"- {ind}" for ind in ai_report.indicators[:5]
            ) + "\n\n"
        if quality_report.issues:
            issues_text += "【质量问题】\n" + "\n".join(
                f"- {iss}" for iss in quality_report.issues[:5]
            )

        system_prompt = """你是一个顶级网文作家，擅长将AI生成的文本改写为具有人类作家风格的文字。

【改写原则】
1. 保持原意和情节不变
2. 打破AI的套路化句式，增加句式变化
3. 增加感官细节描写（视觉、听觉、嗅觉、触觉）
4. 加入人物内心独白和心理活动
5. 适当使用口语化表达和不完美表达
6. 增加环境氛围渲染
7. 对话要自然，符合人物性格
8. 段落长短交错，避免整齐划一
9. 适当使用修辞但不堆砌
10. 保持网文特有的节奏感和爽感

【禁止事项】
- 不要改变原有人物性格和情节走向
- 不要添加新的关键情节
- 不要删除重要内容
- 不要输出任何解释，只输出改写后的正文"""

        prompt = f"""请将以下AI生成的网文章节改写为人类作家风格：

{issues_text}

【原文】
{text[:12000]}

请直接输出改写后的完整章节内容，不要加任何说明。"""

        response = _call_deepseek(
            prompt, system_prompt,
            temperature=0.85, max_tokens=16000, timeout=180
        )
        if not response:
            print("   ⚠️ AI去痕重写失败，返回原文")
            return text

        cleaned = response.strip()
        for prefix in ["改写后的章节内容：", "改写后：", "以下是改写后的内容：", "```", "---"]:
            if cleaned.startswith(prefix):
                cleaned = cleaned[len(prefix):].strip()
        for suffix in ["```", "---"]:
            if cleaned.endswith(suffix):
                cleaned = cleaned[:-len(suffix)].strip()

        return cleaned

    def run_single_round(self, text: str, round_num: int) -> RoundResult:
        start_time = time.time()

        print(f"\n  {'='*50}")
        print(f"  🔍 第{round_num}轮检测")
        print(f"  {'='*50}")

        print(f"  📊 AI痕迹检测中...")
        ai_report = self.detect_ai_traces(text)
        print(f"     AI痕迹分数: {ai_report.score}/100 ({ai_report.level})")
        if ai_report.indicators:
            for ind in ai_report.indicators[:3]:
                print(f"       - {ind}")

        print(f"  📊 文章质量评估中...")
        quality_report = self.evaluate_quality(text)
        print(f"     综合质量: {quality_report.score}/100")
        print(f"     结构:{quality_report.structure_score} 可读:{quality_report.readability_score} "
              f"文学:{quality_report.literary_score} 连贯:{quality_report.coherence_score}")

        ai_passed = ai_report.score <= AI_TRACE_THRESHOLD
        quality_passed = quality_report.score >= QUALITY_THRESHOLD

        if ai_passed and quality_passed:
            status = DetectionStatus.PASS
            passed = True
        elif not ai_passed and not quality_passed:
            status = DetectionStatus.FAIL_BOTH
            passed = False
        elif not ai_passed:
            status = DetectionStatus.FAIL_AI_TRACE
            passed = False
        else:
            status = DetectionStatus.FAIL_QUALITY
            passed = False

        duration = time.time() - start_time

        result = RoundResult(
            round_num=round_num,
            ai_trace_report=ai_report,
            quality_report=quality_report,
            passed=passed,
            status=status,
            duration_seconds=round(duration, 1),
        )

        if passed:
            print(f"  ✅ 第{round_num}轮检测通过！")
        else:
            print(f"  ❌ 第{round_num}轮检测未通过 ({status.value})")

        return result

    def run_full_pipeline(self, text: str, title: str = "",
                          chapter_num: int = 0) -> PipelineResult:
        print(f"\n{'='*60}")
        print(f"🎯 质量检测流水线启动")
        if title:
            print(f"   作品: {title}")
        if chapter_num:
            print(f"   章节: 第{chapter_num}章")
        print(f"   AI阈值: ≤{AI_TRACE_THRESHOLD}分 | 质量阈值: ≥{QUALITY_THRESHOLD}分")
        print(f"   最大轮次: {MAX_RETRY_ROUNDS}")
        print(f"{'='*60}")

        pipeline_start = time.time()
        rounds: List[RoundResult] = []
        current_text = text

        for round_num in range(1, MAX_RETRY_ROUNDS + 1):
            result = self.run_single_round(current_text, round_num)
            rounds.append(result)

            if result.passed:
                total_duration = time.time() - pipeline_start
                print(f"\n  🎉 流水线完成！第{round_num}轮通过")
                return PipelineResult(
                    passed=True,
                    final_text=current_text,
                    rounds=rounds,
                    total_duration_seconds=round(total_duration, 1),
                    needs_manual=False,
                    final_status=DetectionStatus.PASS,
                )

            if round_num < MAX_RETRY_ROUNDS:
                print(f"\n  ⚙️ 第{round_num}轮未通过，开始AI去痕重写...")
                current_text = self.remove_ai_traces(
                    current_text, result.ai_trace_report, result.quality_report
                )
                if current_text == text:
                    print(f"  ⚠️ 重写失败，跳过后续轮次")
                    break
                print(f"  ✅ 重写完成，进入第{round_num + 1}轮检测")

        total_duration = time.time() - pipeline_start
        last_result = rounds[-1] if rounds else None

        manual_reason_parts = []
        if last_result:
            if last_result.status in (DetectionStatus.FAIL_AI_TRACE, DetectionStatus.FAIL_BOTH):
                manual_reason_parts.append(
                    f"AI痕迹分数{last_result.ai_trace_report.score}分(阈值≤{AI_TRACE_THRESHOLD})"
                )
            if last_result.status in (DetectionStatus.FAIL_QUALITY, DetectionStatus.FAIL_BOTH):
                manual_reason_parts.append(
                    f"质量分数{last_result.quality_report.score}分(阈值≥{QUALITY_THRESHOLD})"
                )

        print(f"\n  {'='*50}")
        print(f"  ⚠️ 三轮检测均未通过，需要人工干预")
        print(f"     原因: {'; '.join(manual_reason_parts)}")
        print(f"  {'='*50}")

        return PipelineResult(
            passed=False,
            final_text=current_text,
            rounds=rounds,
            total_duration_seconds=round(total_duration, 1),
            needs_manual=True,
            manual_reason="; ".join(manual_reason_parts),
            final_status=DetectionStatus.MANUAL_REQUIRED,
        )

    def format_pipeline_report(self, result: PipelineResult) -> str:
        lines = []
        lines.append("=" * 60)
        lines.append("📋 质量检测流水线报告")
        lines.append("=" * 60)
        lines.append(f"最终状态: {'✅ 通过' if result.passed else '⚠️ 需人工干预'}")
        lines.append(f"总耗时: {result.total_duration_seconds}秒")
        lines.append(f"检测轮次: {len(result.rounds)}")
        lines.append("")

        for r in result.rounds:
            lines.append(f"--- 第{r.round_num}轮 ---")
            lines.append(f"  AI痕迹: {r.ai_trace_report.score}分 ({r.ai_trace_report.level})")
            lines.append(f"  质量评分: {r.quality_report.score}分")
            lines.append(f"  结构:{r.quality_report.structure_score} "
                         f"可读:{r.quality_report.readability_score} "
                         f"文学:{r.quality_report.literary_score} "
                         f"连贯:{r.quality_report.coherence_score}")
            lines.append(f"  结果: {'✅ 通过' if r.passed else '❌ 未通过'} "
                         f"({r.status.value})")
            lines.append(f"  耗时: {r.duration_seconds}秒")
            if r.ai_trace_report.indicators:
                lines.append(f"  AI特征: {', '.join(r.ai_trace_report.indicators[:3])}")
            if r.quality_report.issues:
                lines.append(f"  问题: {', '.join(r.quality_report.issues[:3])}")
            lines.append("")

        if result.needs_manual:
            lines.append(f"⚠️ 人工干预原因: {result.manual_reason}")
            lines.append("建议: 人工润色后重新提交检测")

        return "\n".join(lines)


def mark_for_manual_review(title: str, chapter_num: int,
                           pipeline_result: PipelineResult,
                           output_dir: str = "novel") -> str:
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    safe_title = re.sub(r'[<>:"/\\|?*]', '_', title)

    mark_filename = os.path.join(
        output_dir,
        f"{safe_title}_第{chapter_num}章_需人工检查.txt"
    )

    last_round = pipeline_result.rounds[-1] if pipeline_result.rounds else None

    content = f"""⚠️  WARNING: 此章节需要人工检查 ⚠️
{'='*70}
生成时间: {timestamp}
作品: {title}
章节: 第{chapter_num}章
状态: 三轮质量检测均未通过

【检测历史】
"""
    for r in pipeline_result.rounds:
        content += f"""
第{r.round_num}轮:
  AI痕迹分数: {r.ai_trace_report.score}/100 ({r.ai_trace_report.level})
  质量评分: {r.quality_report.score}/100
  结构:{r.quality_report.structure_score} 可读:{r.quality_report.readability_score}
  文学:{r.quality_report.literary_score} 连贯:{r.quality_report.coherence_score}
  状态: {'通过' if r.passed else '未通过'}
"""

    content += f"""
【未通过原因】
{pipeline_result.manual_reason}

【处理建议】
1. 人工润色章节内容，降低AI痕迹
2. 检查情节逻辑和人物对话是否自然
3. 增加细节描写和感官体验
4. 处理完成后重新提交检测
{'='*70}
"""

    with open(mark_filename, 'w', encoding='utf-8') as f:
        f.write(content)

    log_file = os.path.join(output_dir, "待人工处理列表.txt")
    log_entry = f"{timestamp} - {title} 第{chapter_num}章 - 三轮检测失败\n"

    if os.path.exists(log_file):
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    else:
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write("NWACS 待人工处理章节列表\n")
            f.write("=" * 50 + "\n")
            f.write(log_entry)

    print(f"   ⚠️ 已创建标记文件: {mark_filename}")
    return mark_filename


if __name__ == "__main__":
    test_text = """
    林晨缓缓地站起身，宛如一只刚刚破茧而出的蝴蝶，心中不禁激动万分。
    仿佛天地都在为他欢呼，眼前的景象十分壮观，格外震撼人心。
    这一切似乎都像是一场梦境，渐渐地，林晨才相信这是真的。
    他微微一笑，心中暗想，自己的努力终究没有白费。
    极其艰难的旅程，非常辛苦的奋斗，终于换来了此刻的成功。
    宛如重生一般，他慢慢地向前走去，轻轻地踏上了前方的道路。

    周围的景色美不胜收，青山绿水，鸟语花香。林晨深深地吸了一口气，
    感受着大自然的美好。他不禁想起了自己一路走来的艰辛历程，
    心中感慨万千。这一切都是值得的，他对自己说。

    突然，一阵微风吹过，带来了远处的声音。林晨警觉地抬起头，
    目光如炬地望向远方。他的直觉告诉他，有什么事情即将发生。
    作为一名经验丰富的修行者，他从不忽视自己的直觉。
    """

    detector = QualityDetector()
    result = detector.run_full_pipeline(test_text, title="测试小说", chapter_num=1)

    print("\n")
    print(detector.format_pipeline_report(result))

    if result.needs_manual:
        mark_for_manual_review("测试小说", 1, result)
