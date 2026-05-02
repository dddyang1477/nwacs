#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS质量保障模块
提供语法检查、可读性评分、去AI痕迹等功能
"""

import re
from typing import Dict, List, Tuple


class QualityAssurance:
    """质量保障工具"""

    def __init__(self):
        print("🛡️ NWACS质量保障模块启动")

    def check_readability(self, text: str) -> Dict:
        """计算可读性评分"""
        # 简单的可读性评分算法
        sentences = text.split('。')
        total_sentences = len([s for s in sentences if s.strip()])
        total_words = len(text.replace(' ', ''))
        avg_sentence_length = total_words / max(total_sentences, 1)

        # 估算Flesch-Kincaid可读性（中文适配版）
        # 中文一般：句长20-30字较好
        if avg_sentence_length < 15:
            score = 90
            level = "极易阅读"
        elif avg_sentence_length < 25:
            score = 75
            level = "易读"
        elif avg_sentence_length < 35:
            score = 60
            level = "一般"
        elif avg_sentence_length < 50:
            score = 45
            level = "稍难"
        else:
            score = 30
            level = "难读"

        return {
            "score": score,
            "level": level,
            "avg_sentence_length": round(avg_sentence_length, 1),
            "total_words": total_words,
            "total_sentences": total_sentences
        }

    def remove_ai_traits(self, text: str) -> Tuple[str, List[str]]:
        """尝试减少AI痕迹"""
        changes = []
        modified = text

        # 常见AI模式修正
        ai_patterns = [
            (r"在这个[^\n]+中，", ""),
            (r"这是一个[^\n]+的故事", ""),
            (r"让我们[^\n]+", ""),
            (r"接下来[^\n]+", ""),
        ]

        for pattern, replacement in ai_patterns:
            if re.search(pattern, modified):
                changes.append(f"移除AI模式: {pattern[:30]}...")
            modified = re.sub(pattern, replacement, modified)

        return modified, changes

    def check_common_errors(self, text: str) -> List[Dict]:
        """检查常见问题"""
        issues = []

        # 检查连续标点
        if "，，" in text or "。。" in text:
            issues.append({
                "type": "标点错误",
                "severity": "低",
                "description": "发现连续标点符号"
            })

        # 检查段落长度
        paragraphs = text.split('\n\n')
        long_paragraphs = [p for p in paragraphs if len(p.replace(' ', '')) > 500]
        if long_paragraphs:
            issues.append({
                "type": "段落过长",
                "severity": "中",
                "description": f"发现 {len(long_paragraphs)} 个超长段落，建议拆分"
            })

        # 检查对话格式
        dialogue_markers = ['"', '“', '”', '「', '」']
        has_dialogue = any(m in text for m in dialogue_markers)
        if has_dialogue and len(paragraphs) < 5:
            issues.append({
                "type": "格式建议",
                "severity": "低",
                "description": "对话较多，建议每个对话单独分段"
            })

        return issues

    def full_quality_check(self, text: str) -> Dict:
        """完整质量检查"""
        print("\n" + "="*60)
        print("🛡️ NWACS质量检查")
        print("="*60)

        readability = self.check_readability(text)
        cleaned_text, ai_changes = self.remove_ai_traits(text)
        issues = self.check_common_errors(text)

        print(f"\n📖 可读性评分: {readability['score']}/100 - {readability['level']}")
        print(f"   平均句长: {readability['avg_sentence_length']} 字")
        print(f"   总字数: {readability['total_words']}")
        print(f"   段落数: {readability['total_sentences']}")

        if issues:
            print(f"\n⚠️ 发现 {len(issues)} 个问题:")
            for i, issue in enumerate(issues, 1):
                print(f"{i}. [{issue['severity']}] {issue['type']}: {issue['description']}")
        else:
            print("\n✅ 未发现明显问题")

        if ai_changes:
            print(f"\n🔧 AI痕迹优化: {len(ai_changes)} 处")

        return {
            "readability": readability,
            "issues": issues,
            "ai_optimizations": ai_changes,
            "cleaned_text": cleaned_text
        }


def main():
    print("="*60)
    print("🛡️ NWACS质量保障工具")
    print("="*60)

    qa = QualityAssurance()

    # 测试文本
    test_text = """这是一个测试文本。在这个测试中，我们检查一些常见的问题。让我们看看效果如何。接下来进行下一步分析。这是一个非常非常非常非常非常非常非常非常非常非常非常非常长的段落，用来测试段落长度检查。希望这个工具能帮助提升文章质量。"""

    qa.full_quality_check(test_text)


if __name__ == "__main__":
    main()
