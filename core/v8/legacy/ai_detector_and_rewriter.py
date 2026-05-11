#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
【NWACS AI检测与预处理模块 v2.0】
设计原则：
- 只检测，不破坏 — 不对原文做机械替换（那会制造更多AI痕迹）
- 真正的去痕交给DeepSeek API（ai_polisher）
- 本模块只做安全的、非破坏性的预处理
"""

import re
import random


class AIDetectorAndRewriter:

    def __init__(self):
        self.ai_indicators = [
            "宛如", "仿佛", "似乎", "犹如", "宛若", "恰似",
            "不禁", "不由得", "忍不住",
            "非常", "极其", "极为", "十分", "特别", "格外",
            "缓缓地", "慢慢地", "渐渐地", "轻轻地", "悄悄地",
            "微微一笑", "轻轻一笑", "淡淡一笑",
            "心中暗想", "心中思索", "心中暗忖",
            "值得注意的是", "综上所述", "总而言之",
            "首先", "其次", "最后", "此外", "另外",
            "通过", "实现", "促进", "推动", "提升",
            "具有重要意义", "发挥着重要作用",
        ]

        self.ai_patterns = [
            (r"^(虽然|尽管|即使).*(，|。)", 0.3),
            (r"[！？]{2,}", 0.4),
            (r"\.{4,}", 0.3),
            (r"，.*，.*，.*，", 0.2),
            (r"(?:他|她|它)(?:感到|觉得|认为|心想|暗想)", 0.5),
            (r"(?:进行|做出|加以|予以)(?:了)?(?:的)?", 0.4),
            (r"(?:显著|明显|突出|卓越)(?:的)?(?:提升|改善|增强|提高)", 0.5),
            (r"(?:这意味着|这表明|这体现|这反映)", 0.4),
            (r"(?:一定|必然|绝对|毫无疑问)(?:地|的)?", 0.3),
            (r"(?:性|化|度|率|力){2,}", 0.3),
        ]

    def detect_ai_score(self, text):
        score = 0
        text_len = max(len(text), 1)

        word_hits = 0
        for word in self.ai_indicators:
            word_hits += text.count(word)
        density = word_hits / (text_len / 100)
        score += min(density * 8, 40)

        pattern_hits = 0
        for pattern, weight in self.ai_patterns:
            matches = re.findall(pattern, text)
            pattern_hits += len(matches) * weight * 10
        score += min(int(pattern_hits), 30)

        lines = text.split('\n')
        if len(lines) > 5:
            similar_starts = 0
            for i in range(1, min(len(lines), 15)):
                if (lines[i].startswith(('他', '她', '它', '这', '那'))
                        and lines[i - 1].startswith(('他', '她', '它', '这', '那'))):
                    similar_starts += 1
            score += min(similar_starts * 5, 30)

        return min(score, 100)

    def _safe_humanize(self, text):
        """
        安全的、非破坏性的人类化预处理
        只做不会引入新AI痕迹的操作：
        - 段落呼吸：确保段落长度有变化
        - 标点自然化：减少连续重复标点
        """
        result = text

        result = re.sub(r'([！？]){3,}', r'\1\1', result)
        result = re.sub(r'\.{5,}', '……', result)

        paras = result.split('\n\n')
        if len(paras) >= 4:
            lengths = [len(p) for p in paras]
            avg_len = sum(lengths) / len(lengths)
            new_paras = []
            for i, para in enumerate(paras):
                if len(para) > avg_len * 2.5 and random.random() < 0.4:
                    mid = len(para) // 2
                    split_point = para.rfind('。', mid - 50, mid + 50)
                    if split_point == -1:
                        split_point = mid
                    else:
                        split_point += 1
                    new_paras.append(para[:split_point])
                    new_paras.append(para[split_point:])
                else:
                    new_paras.append(para)
            result = '\n\n'.join(new_paras)

        return result

    def check_and_rewrite(self, text):
        """
        检测 + 安全预处理
        不做破坏性机械替换，真正的去痕交给ai_polisher
        """
        print("\n" + "=" * 60)
        print("[AI检测与预处理 v2.0 非破坏模式]")
        print("=" * 60)

        original_score = self.detect_ai_score(text)
        print(f"  初始AI痕迹评分: {original_score}/100")

        if original_score < 15:
            print("  [OK] AI痕迹极少，直接通过")
            return text

        print("  执行安全预处理（段落呼吸 + 标点自然化）...")
        processed = self._safe_humanize(text)

        final_score = self.detect_ai_score(processed)
        print(f"  预处理后评分: {final_score}/100")

        if final_score < original_score:
            print(f"  降低: {original_score - final_score}分")
        else:
            print("  评分未显著变化，交由AI润色器深度处理")

        print("  预处理完成，移交AI润色器进行深度去痕...")
        return processed


if __name__ == "__main__":
    test_text = """
    林晨缓缓地站起身，宛如一只刚刚破茧而出的蝴蝶，心中不禁激动万分。
    仿佛天地都在为他欢呼，眼前的景象十分壮观，格外震撼人心。
    这一切似乎都像是一场梦境，渐渐地，林晨才相信这是真的。
    他微微一笑，心中暗想，自己的努力终究没有白费。
    极其艰难的旅程，非常辛苦的奋斗，终于换来了此刻的成功。
    宛如重生一般，他慢慢地向前走去，轻轻地踏上了前方的道路。
    """

    detector = AIDetectorAndRewriter()
    result = detector.check_and_rewrite(test_text)
    print("\n处理后:")
    print("-" * 40)
    print(result)
