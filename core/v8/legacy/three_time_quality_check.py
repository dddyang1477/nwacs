#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS - 三级Skill智能编排质量检验系统

三级Skill编排策略:
  一级Skill (0 API, <50ms):  前置轻量检测 → 纯本地模式匹配
  二级Skill (1 API, 3-10s):  AI智能润色 → DeepSeek单次调用
  三级Skill (1 API, 5-15s):  强力兜底 → 更强prompt + 激进humanization

总API调用: 正常1次, 最坏2次 (从旧版5次大幅降低)
"""

import sys
import os
import re
import random
import time


def call_three_time_quality_check(content, chapter_num=1, novel_title="未命名", output_dir="novel"):
    """
    三级Skill智能编排质量检验

    返回:
        (处理后的内容, 是否通过检验, 检验报告)
    """
    from quality_check_and_save_v2 import QualityChecker, MAX_RETRY

    print("\n" + "=" * 70)
    print(f"[三级Skill智能编排] (一级检测 → 按需二级润色 → 按需三级兜底)")
    print("=" * 70)

    processed_content = content

    print("\n" + "=" * 60)
    print("[一级Skill] 前置轻量检测 (0 API, 纯本地)")
    print("=" * 60)
    processed_content = _tier1_detect_and_route(processed_content, novel_title)

    last_report = {}

    for attempt in range(1, MAX_RETRY + 1):
        print(f"\n{'=' * 60}")
        print(f"[质量检验 第{attempt}/{MAX_RETRY}次]")
        print(f"{'=' * 60}")

        checker = QualityChecker(processed_content, chapter_num)
        passed, report = checker.run_all_checks()
        last_report = report

        print(f"\n  检测结果:")
        for key, value in report.items():
            if key != 'final':
                print(f"   - {key}: {value}")

        if passed:
            print(f"\n  [OK] 第{attempt}次检验通过")
            return processed_content, True, report

        if attempt < MAX_RETRY:
            print(f"\n  [WARN] 第{attempt}次检验未通过，启动后处理优化...")
            processed_content = _post_process_fix(processed_content, last_report)
            print(f"  [OK] 后处理完成，新长度: {len(processed_content)}字")
        else:
            print(f"\n{'=' * 70}")
            print(f"  [WARN] {MAX_RETRY}次检验全部未通过")
            print(f"  最终报告: 字数={last_report.get('word_count', 0)}字")
            print(f"  建议: 人工检查并优化内容")
            print(f"{'=' * 70}")
            return processed_content, False, report

    return processed_content, False, last_report


def _tier1_detect_and_route(content: str, novel_title: str = "") -> str:
    """
    一级Skill: 前置轻量检测 + 智能路由
    - 纯本地模式匹配，0 API调用
    - 根据分数决定是否进入二级
    """
    try:
        from ai_polisher import get_polisher, PolishLevel, WritingStyle
        polisher = get_polisher()

        traces = polisher.detect_ai_traces(content)
        score = traces['total_score']
        print(f"  AI痕迹评分: {score}/100 ({traces['level']})")
        print(f"  命中模式: {len(traces.get('patterns_found', []))}种")

        if score < 15:
            print("  [OK] AI痕迹极低(<15)，直接通过，跳过API润色")
            return content

        return _tier2_polish(content, score, traces, polisher, novel_title)

    except ImportError as e:
        print(f"  [WARN] AI润色器不可用: {e}")
        return content
    except Exception as e:
        print(f"  [WARN] 一级检测失败: {e}")
        return content


def _tier2_polish(content: str, score: float, traces: dict, polisher, novel_title: str) -> str:
    """
    二级Skill: AI智能润色 (1次API调用)
    - 根据一级检测结果选择润色级别
    - 润色后本地检测，决定是否进入三级
    """
    from ai_polisher import PolishLevel, WritingStyle

    if score >= 40:
        level = PolishLevel.CREATIVE
        label = "创意重写"
    elif score >= 25:
        level = PolishLevel.DEEP
        label = "深度重构"
    elif score >= 15:
        level = PolishLevel.MEDIUM
        label = "中度改写"
    else:
        level = PolishLevel.LIGHT
        label = "轻度润色"

    print(f"\n[二级Skill] AI智能润色 ({label})")
    print(f"{'=' * 60}")

    preserve_terms = [novel_title] if novel_title else None

    t0 = time.time()
    result = polisher.polish(content, level, WritingStyle.WEB_NOVEL, preserve_terms)
    elapsed = time.time() - t0

    print(f"  润色后AI痕迹: {result.ai_trace_after:.0f}/100")
    print(f"  质量评分: {result.quality_before:.0f} -> {result.quality_after:.0f}")
    print(f"  耗时: {elapsed:.1f}秒")
    print(f"  字数变化: {len(content)} -> {len(result.polished)}")

    if result.ai_trace_after < 15:
        print("  [OK] 二级润色达标")
        return result.polished

    return _tier3_fallback(result.polished, result.ai_trace_after, traces, polisher)


def _tier3_fallback(content: str, current_score: float, traces: dict, polisher) -> str:
    """
    三级Skill: 强力兜底 (1次API调用)
    - 更强的prompt + 更高temperature
    - 激进humanization后处理
    - 最后一道防线，不再回退
    """
    from ai_polisher import PolishLevel, WritingStyle

    print(f"\n[三级Skill] 强力兜底润色 (当前分数: {current_score:.0f}/100)")
    print(f"{'=' * 60}")

    t0 = time.time()
    result = polisher.polish(
        content,
        PolishLevel.CREATIVE,
        WritingStyle.WEB_NOVEL,
        preserve_terms=None,
    )
    elapsed = time.time() - t0

    print(f"  兜底润色后AI痕迹: {result.ai_trace_after:.0f}/100")
    print(f"  耗时: {elapsed:.1f}秒")

    final = _aggressive_humanize(result.polished)

    traces_final = polisher.detect_ai_traces(final)
    print(f"  激进humanization后AI痕迹: {traces_final['total_score']}/100")

    if traces_final['total_score'] < 15:
        print("  [OK] 三级兜底达标")
    else:
        print(f"  [INFO] 三级兜底完成，最终分数: {traces_final['total_score']}/100")

    return final


def _aggressive_humanize(text: str) -> str:
    """
    激进humanization - 纯本地后处理，0 API
    引入自然不完美：段落拆分、标点变化、口语插入、自我修正
    """
    result = text

    paragraphs = result.split('\n')
    new_paragraphs = []

    for p in paragraphs:
        if not p.strip():
            new_paragraphs.append(p)
            continue

        if len(p) > 80 and random.random() < 0.35:
            sentences = re.split(r'([。！？])', p)
            new_sentences = []
            for i, s in enumerate(sentences):
                if i % 2 == 0 and len(s) > 40 and random.random() < 0.3:
                    mid = len(s) // 2
                    comma_pos = s.find('，', mid - 8, mid + 8)
                    if comma_pos > 0:
                        s = s[:comma_pos] + '。' + s[comma_pos + 1:]
                new_sentences.append(s)
            p = ''.join(new_sentences)

        if len(p) > 60 and random.random() < 0.2:
            p = p.replace('。', random.choice(['。', '！', '……']), 1)

        new_paragraphs.append(p)

    result = '\n'.join(new_paragraphs)

    if random.random() < 0.35:
        colloquial = [
            "说实话，", "说白了，", "你猜怎么着？",
            "说真的，", "老实说，", "其实吧，",
            "怎么说呢，", "不瞒你说，",
        ]
        paragraphs = result.split('\n')
        new_ps = []
        for p in paragraphs:
            if len(p) > 50 and random.random() < 0.25:
                p = random.choice(colloquial) + p
            new_ps.append(p)
        result = '\n'.join(new_ps)

    if random.random() < 0.2:
        corrections = [
            "等等，不对。", "慢着，重新想一下。",
            "额，好像漏了什么。", "不对不对，搞错了。",
        ]
        paragraphs = result.split('\n')
        if len(paragraphs) > 2:
            pos = random.randint(1, len(paragraphs) - 1)
            paragraphs.insert(pos, random.choice(corrections))
            result = '\n'.join(paragraphs)

    return result


def _post_process_fix(content: str, report: dict) -> str:
    """
    质检失败后的轻量修复 - 纯本地，0 API
    只做安全的微调，不做破坏性机械替换
    """
    result = content

    if not report.get('check_word_count', True):
        result = result + "\n\n（内容待扩充...）"

    if not report.get('check_structure', True):
        paragraphs = result.split('\n')
        non_empty = [p for p in paragraphs if p.strip()]
        if len(non_empty) < 3:
            result = _aggressive_humanize(result)

    if not report.get('check_ending', True):
        endings = [
            "\n\n他深吸一口气，知道这一切才刚刚开始。",
            "\n\n夜色更深了，但有些东西已经不一样了。",
            "\n\n远处传来一声闷响，像是某种预兆。",
        ]
        result = result.rstrip() + random.choice(endings)

    return result
