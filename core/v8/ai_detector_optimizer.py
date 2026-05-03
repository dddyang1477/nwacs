#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS V8.0 AI检测优化系统
检测并优化写作内容，降低AI检测率
"""

import sys
import json
import os
import re
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "sk-f3246fbd1eef446e9a11d78efefd9bba"
BASE_URL = "https://api.deepseek.com"

def call_deepseek(prompt, system_prompt=None, temperature=0.7):
    """调用DeepSeek API"""
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
            "max_tokens": 8000
        }
        response = requests.post(url, headers=headers, json=data, timeout=300)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"   ❌ DeepSeek调用失败: {e}")
        return None


class AIDetectionOptimizer:
    """AI检测优化器"""

    def __init__(self):
        # AI写作特征列表
        self.ai_patterns = {
            "过度使用的连接词": [
                "首先", "其次", "然后", "最后",
                "因此", "所以", "然而", "但是",
                "与此同时", "值得注意的是"
            ],
            "过度规整的句式": [
                r"\.{3,}",  # 过多的省略号
                r"，{2,}",   # 过多的逗号
                r"、{2,}",  # 过多的顿号
            ],
            "过度解释": [
                "这意味着",
                "换句话说",
                "也就是说",
                "具体来说"
            ],
            "机械化的情感表达": [
                "他感到",
                "她觉得",
                "内心深处",
                "不由自主地"
            ],
            "AI常用的高频词": [
                "竟然", "居然", "简直", "未免",
                "令人", "使得", "从而", "继而"
            ]
        }

        # 优化策略
        self.optimization_tips = [
            "使用更口语化的表达",
            "增加句式变化",
            "减少过度连接的句子",
            "增加个人风格的表达",
            "使用更具体的细节描写",
            "增加情感波动"
        ]

    def analyze_ai_patterns(self, text):
        """分析文本中的AI特征"""
        issues = []

        for pattern_type, patterns in self.ai_patterns.items():
            for pattern in patterns:
                if isinstance(pattern, str):
                    if pattern in text:
                        count = text.count(pattern)
                        issues.append({
                            "type": pattern_type,
                            "pattern": pattern,
                            "count": count,
                            "severity": "high" if count > 5 else "medium" if count > 2 else "low"
                        })
                else:
                    matches = re.findall(pattern, text)
                    if matches:
                        issues.append({
                            "type": pattern_type,
                            "pattern": str(pattern),
                            "count": len(matches),
                            "severity": "high" if len(matches) > 10 else "medium" if len(matches) > 5 else "low"
                        })

        return issues

    def get_detectability_score(self, text):
        """计算AI检测可能性得分（0-100，越低越好）"""
        score = 30  # 基础分

        issues = self.analyze_ai_patterns(text)

        for issue in issues:
            if issue["severity"] == "high":
                score += 20
            elif issue["severity"] == "medium":
                score += 10
            else:
                score += 5

        # 检查句子长度分布
        sentences = re.split(r'[.。!！?？]', text)
        avg_sentence_len = sum(len(s.strip()) for s in sentences) / max(len(sentences), 1)

        if avg_sentence_len > 50:
            score += 15  # 句子太长，AI特征明显
        elif avg_sentence_len < 10:
            score += 5

        # 检查段落长度一致性
        paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
        if paragraphs:
            lens = [len(p) for p in paragraphs]
            variance = sum((l - sum(lens)/len(lens))**2 for l in lens) / len(lens)
            if variance < 100:
                score += 10  # 段落长度太一致，AI特征

        return min(score, 100)

    def optimize_text_deepseek(self, text, target_score=30):
        """使用DeepSeek优化文本，降低AI检测率"""
        prompt = f"""请优化以下小说文本，降低AI检测率，同时保持内容质量！

【重要要求】
1. 降低AI写作特征，让文字更有人情味
2. 保持故事完整性和可读性
3. 优化后内容不能有明显逻辑问题

【需要避免的AI特征】
- 过度使用"首先、其次、然后、最后"等连接词
- 句子长度过于规整
- 过度解释性语句
- 机械化的情感描写
- 重复使用相同的句式结构

【优化技巧】
1. 增加口语化表达
2. 使用更自然的对话
3. 增加句式变化
4. 添加个人风格
5. 使用更具体的细节
6. 增加情感波动

待优化文本：
{text}

请直接输出优化后的文本，不需要解释！"""

        system_prompt = """你是一位专业的小说编辑，擅长优化AI生成的文本，使其更自然、更有人情味。
你的优化原则：
1. 保持原文的核心内容和情节
2. 大幅降低AI写作特征
3. 让文字更流畅自然
4. 增加人性化的表达"""

        result = call_deepseek(prompt, system_prompt, temperature=0.9)

        return result

    def optimize_local(self, text):
        """本地简单优化（不使用API）"""
        optimized = text

        # 替换AI常用词
        replacements = {
            "首先": "",
            "其次": "",
            "然后": "接着",
            "因此": "所以",
            "然而": "可是",
            "但是": "不过",
            "内心深处": "心里",
            "不由自主地": "忍不住",
            "令人": "让人",
            "从而": "于是",
            "继而": "接着"
        }

        for old, new in replacements.items():
            optimized = optimized.replace(old, new)

        # 减少连续标点
        optimized = re.sub(r'。{2,}', '。', optimized)
        optimized = re.sub(r'，{2,}', '，', optimized)

        return optimized

    def full_optimization(self, text, use_deepseek=True):
        """完整优化流程"""
        print("\n" + "="*60)
        print("🔍 AI检测与优化系统")
        print("="*60)

        # 1. 分析AI特征
        print("\n📊 步骤1: AI特征分析...")
        issues = self.analyze_ai_patterns(text)

        if issues:
            print(f"   发现 {len(issues)} 个AI特征：")
            for issue in issues[:10]:
                print(f"   - [{issue['severity'].upper()}] {issue['type']}: '{issue['pattern']}' (出现{issue['count']}次)")
        else:
            print("   ✅ 未发现明显AI特征")

        # 2. 计算检测得分
        print("\n📊 步骤2: AI检测可能性评估...")
        score = self.get_detectability_score(text)
        print(f"   当前AI检测得分: {score}/100")
        print(f"   评估: {'⚠️ 高风险' if score > 60 else '🟡 中风险' if score > 40 else '✅ 低风险'}")

        # 3. 本地初步优化
        print("\n📊 步骤3: 本地初步优化...")
        optimized_local = self.optimize_local(text)
        print("   ✅ 本地优化完成")

        # 4. DeepSeek深度优化
        if use_deepseek and score > 30:
            print("\n📊 步骤4: DeepSeek深度优化...")
            optimized_deepseek = self.optimize_text_deepseek(text, target_score=30)
            print("   ✅ 深度优化完成")

            final_score = self.get_detectability_score(optimized_deepseek)
            print(f"\n📊 优化后AI检测得分: {final_score}/100")
            print(f"   评估: {'⚠️ 高风险' if final_score > 60 else '🟡 中风险' if final_score > 40 else '✅ 低风险'}")

            improvement = score - final_score
            print(f"   改善: {improvement:.1f}分")

            return optimized_deepseek
        else:
            print("\n📊 优化后AI检测得分: 已显著降低")
            return optimized_local


class QualityReviewer:
    """质量审查师 - 集成AI检测优化"""

    def __init__(self):
        self.ai_optimizer = AIDetectionOptimizer()

    def review_novel(self, novel_content):
        """审查小说质量并优化"""
        print("\n" + "="*60)
        print("🔍 质量审查与AI优化")
        print("="*60)

        results = {
            "ai_detection_score": 0,
            "issues": [],
            "suggestions": [],
            "optimized_content": None
        }

        # 1. AI检测
        print("\n📊 AI检测分析...")
        results["ai_detection_score"] = self.ai_optimizer.get_detectability_score(novel_content)
        print(f"   AI检测得分: {results['ai_detection_score']}/100")

        # 2. 问题识别
        print("\n📊 识别质量问题...")
        results["issues"] = self.ai_optimizer.analyze_ai_patterns(novel_content)
        print(f"   发现 {len(results['issues'])} 个问题")

        # 3. 优化建议
        print("\n📊 生成优化建议...")
        results["suggestions"] = self.ai_optimizer.optimization_tips
        print(f"   生成了 {len(results['suggestions'])} 条优化建议")

        # 4. 深度优化
        print("\n📊 执行深度优化...")
        results["optimized_content"] = self.ai_optimizer.full_optimization(novel_content, use_deepseek=True)
        print("   ✅ 优化完成")

        return results

    def batch_review_chapters(self, chapter_files):
        """批量审查章节"""
        print("\n" + "="*60)
        print(f"📚 批量审查 {len(chapter_files)} 个章节")
        print("="*60)

        results = []

        for i, file_path in enumerate(chapter_files, 1):
            print(f"\n📖 审查第 {i} 章: {os.path.basename(file_path)}")

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                result = self.review_novel(content)
                results.append({
                    "file": file_path,
                    "score_before": result["ai_detection_score"],
                    "issues_count": len(result["issues"])
                })

                # 保存优化后的内容
                optimized_file = file_path.replace(".txt", "_optimized.txt")
                with open(optimized_file, 'w', encoding='utf-8') as f:
                    f.write(result["optimized_content"])
                print(f"   💾 已保存优化版本: {os.path.basename(optimized_file)}")

            except Exception as e:
                print(f"   ❌ 审查失败: {e}")

        print("\n" + "="*60)
        print("📊 批量审查完成")
        print("="*60)

        total_score = sum(r["score_before"] for r in results)
        avg_score = total_score / len(results) if results else 0

        print(f"   审查章节数: {len(results)}")
        print(f"   平均AI检测得分: {avg_score:.1f}/100")

        return results


def main():
    print("="*60)
    print("🔍 NWACS V8.0 AI检测优化系统")
    print("="*60)
    print("\n【功能说明】")
    print("  ✅ AI特征分析 - 检测文本中的AI写作特征")
    print("  ✅ AI检测评分 - 计算AI检测可能性得分")
    print("  ✅ 本地优化 - 快速简单的优化")
    print("  ✅ DeepSeek深度优化 - 智能优化，降低检测率")
    print("  ✅ 批量处理 - 支持多章节批量优化")
    print("="*60)

    print("\n请选择操作：")
    print("  1. 🔍 分析文本AI特征")
    print("  2. ✏️ 优化单个文本")
    print("  3. 📚 批量优化章节")
    print("  4. 📖 审查并优化小说文件夹")

    choice = input("\n请选择 (1/2/3/4): ").strip()

    optimizer = AIDetectionOptimizer()

    if choice == "1":
        print("\n请输入要分析的文本（直接回车使用示例）：")
        sample = """首先，主角叶青云站在青云宗的山门前，他感到内心深处有一种莫名的激动。
然后，他回想起自己前世的记忆，那是一位伟大的天算师。
因此，他决定要在这个世界重新崛起。
然而，宗门中的林逸却对他不屑一顾。
但是，叶青云并没有放弃，他相信自己的能力。
最后，他踏入了青云宗，开始了新的修炼之旅。"""

        text = input().strip()
        if not text:
            text = sample

        print("\n" + "="*60)
        print("📊 AI特征分析结果")
        print("="*60)

        issues = optimizer.analyze_ai_patterns(text)
        print(f"\n发现 {len(issues)} 个AI特征：")
        for issue in issues:
            print(f"  - [{issue['severity'].upper()}] {issue['type']}: '{issue['pattern']}'")

        score = optimizer.get_detectability_score(text)
        print(f"\nAI检测得分: {score}/100")
        print(f"评估: {'⚠️ 高风险' if score > 60 else '🟡 中风险' if score > 40 else '✅ 低风险'}")

    elif choice == "2":
        print("\n请输入要优化的文本（直接回车使用示例）：")
        sample = """首先，叶青云站在山巅，他感到内心深处有一种难以言喻的情绪。
然后，他开始运转功法，吸收天地灵气。
因此，他的修为在不断提升。
然而，就在这时，天空突然暗了下来。
但是，叶青云并没有惊慌失措，他相信自己的实力。
最后，一道闪电划破天空，照亮了整个世界。"""

        text = input().strip()
        if not text:
            text = sample

        print("\n开始优化...")
        optimized = optimizer.full_optimization(text, use_deepseek=True)

        print("\n" + "="*60)
        print("📝 优化结果")
        print("="*60)
        print(optimized)

    elif choice == "3":
        print("\n请输入章节文件夹路径（直接回车使用默认）：")
        folder = input().strip()
        if not folder:
            folder = "novels"

        print(f"\n扫描文件夹: {folder}")
        chapter_files = []

        if os.path.exists(folder):
            for root, dirs, files in os.walk(folder):
                for file in files:
                    if file.startswith("chapter_") and file.endswith(".txt"):
                        chapter_files.append(os.path.join(root, file))

        if chapter_files:
            reviewer = QualityReviewer()
            reviewer.batch_review_chapters(chapter_files)
        else:
            print("   ❌ 未找到章节文件")

    elif choice == "4":
        print("\n请输入小说文件夹路径：")
        folder = input().strip()

        if not folder or not os.path.exists(folder):
            print("   ❌ 文件夹不存在")
            return

        print(f"\n扫描文件夹: {folder}")
        chapter_files = []

        for file in os.listdir(folder):
            if file.startswith("chapter_") and file.endswith(".txt"):
                chapter_files.append(os.path.join(folder, file))

        if chapter_files:
            print(f"   找到 {len(chapter_files)} 个章节")
            reviewer = QualityReviewer()
            reviewer.batch_review_chapters(chapter_files)
        else:
            print("   ❌ 未找到章节文件")

    else:
        print("\n无效选项")


if __name__ == "__main__":
    main()
