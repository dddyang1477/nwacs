#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 简洁直出管线 - SimpleDirectPipeline

对标 Sudowrite "Write" 一键生成 / FeelFish "AI续写" 直出模式

设计理念：
- 每章只调用1次API（创作引擎直出）
- 去AI铁律已内置在system_prompt中，无需后处理
- 零额外开销，最快最稳
- 自动保存 + 记忆更新 + 进度追踪

与 CollaborativeWritingPipeline 的区别：
- CollaborativeWritingPipeline: 构思→大纲→初稿→检测→去痕→润色→终稿 (3次API调用/章)
- SimpleDirectPipeline: 创作引擎直出 (1次API调用/章)
- 适用场景：prompt已内置去AI规则的快速生成
"""

import json
import os
import time
import re
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum


class DirectPipelineState(Enum):
    IDLE = "空闲"
    RUNNING = "运行中"
    PAUSED = "已暂停"
    COMPLETED = "已完成"
    ERROR = "错误"


@dataclass
class ChapterRecord:
    chapter_num: int
    title: str = ""
    content: str = ""
    word_count: int = 0
    generated_at: str = ""
    generation_time_s: float = 0
    api_calls: int = 0
    status: str = "pending"


@dataclass
class DirectPipelineConfig:
    genre: str = "玄幻"
    theme: str = ""
    target_words_per_chapter: int = 3000
    temperature: float = 0.85
    max_tokens: int = 6000
    auto_save: bool = True
    save_dir: str = ""
    continue_from_chapter: int = 1
    max_retries_per_chapter: int = 2
    api_timeout: int = 180
    auto_analyze: bool = True
    ai_score_warn_threshold: float = 0.6
    beat_density_warn_threshold: float = 2.0


class SimpleDirectPipeline:
    """简洁直出管线 — 创作引擎直出，一章一次API调用"""

    def __init__(self, creative_engine=None, memory_manager=None,
                 genre_manager=None, voice_injector=None,
                 consistency_pipeline=None, knowledge_engine=None,
                 beat_analyzer=None):
        self.engine = creative_engine
        self.memory = memory_manager
        self.genre_manager = genre_manager
        self.voice_injector = voice_injector
        self.consistency = consistency_pipeline
        self.knowledge_engine = knowledge_engine
        self.beat_analyzer = beat_analyzer

        self.config = DirectPipelineConfig()
        self.state = DirectPipelineState.IDLE
        self.novel_title: str = "未命名作品"
        self.chapters: Dict[int, ChapterRecord] = {}
        self.start_time: float = 0
        self.total_api_calls: int = 0

    def configure(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)

    def run(self, genre: str = None, theme: str = None,
            chapter_count: int = 1, starting_chapter: int = None,
            novel_title: str = None) -> Dict[str, Any]:
        if genre:
            self.config.genre = genre
        if theme:
            self.config.theme = theme
        if starting_chapter is not None:
            self.config.continue_from_chapter = starting_chapter
        if novel_title:
            self.novel_title = novel_title

        self.start_time = time.time()
        self.state = DirectPipelineState.RUNNING
        self.total_api_calls = 0

        print(f"\n{'='*60}")
        print(f"🚀 简洁直出管线启动")
        print(f"   作品: {self.novel_title}")
        print(f"   题材: {self.config.genre} | 章节: 第{self.config.continue_from_chapter}章起 x{chapter_count}")
        print(f"   模式: 创作引擎直出 (1次API/章)")
        print(f"{'='*60}")

        results = {}
        failed_chapters = []

        for offset in range(chapter_count):
            ch_num = self.config.continue_from_chapter + offset

            try:
                ch_result = self._generate_chapter(ch_num)
                results[f"chapter_{ch_num}"] = ch_result

                if not ch_result.get("success"):
                    failed_chapters.append(ch_num)
                    print(f"  ⚠️ 第{ch_num}章生成失败，继续下一章...")

            except Exception as e:
                print(f"  ❌ 第{ch_num}章异常: {e}")
                failed_chapters.append(ch_num)
                results[f"chapter_{ch_num}"] = {
                    "chapter": ch_num, "success": False, "error": str(e)
                }

        total_time = time.time() - self.start_time
        self.state = DirectPipelineState.COMPLETED

        summary = self._build_summary(results, total_time, failed_chapters)
        return summary

    def _generate_chapter(self, chapter_num: int) -> Dict:
        print(f"\n{'─'*50}")
        print(f"📖 第{chapter_num}章")
        print(f"{'─'*50}")

        record = ChapterRecord(chapter_num=chapter_num)
        self.chapters[chapter_num] = record

        for attempt in range(1, self.config.max_retries_per_chapter + 1):
            t0 = time.time()

            try:
                content = self._call_creative_engine(chapter_num, attempt)

                if content and len(content) >= 500:
                    record.content = content
                    record.word_count = len(content)
                    record.generation_time_s = time.time() - t0
                    record.api_calls = 1
                    record.status = "completed"
                    record.generated_at = datetime.now().isoformat()
                    self.total_api_calls += 1

                    self._post_generation_hooks(chapter_num, content)

                    print(f"  ✅ 完成 ({record.word_count}字, {record.generation_time_s:.1f}秒)")

                    return {
                        "chapter": chapter_num,
                        "success": True,
                        "content": content,
                        "word_count": record.word_count,
                        "time_s": record.generation_time_s,
                        "attempt": attempt,
                    }
                else:
                    print(f"  ⚠️ 第{attempt}次尝试字数不足({len(content) if content else 0}字)")

            except Exception as e:
                print(f"  ❌ 第{attempt}次尝试失败: {e}")
                if attempt < self.config.max_retries_per_chapter:
                    wait = attempt * 3
                    print(f"     等待{wait}秒后重试...")
                    time.sleep(wait)

        record.status = "failed"
        return {
            "chapter": chapter_num,
            "success": False,
            "error": f"生成失败（{self.config.max_retries_per_chapter}次尝试）",
        }

    def _call_creative_engine(self, chapter_num: int, attempt: int) -> str:
        if not self.engine:
            return self._generate_fallback(chapter_num)

        system_prompt = self._build_system_prompt()
        user_prompt = self._build_user_prompt(chapter_num, attempt)

        try:
            if hasattr(self.engine, 'generate'):
                result = self.engine.generate(
                    user_prompt,
                    system_prompt=system_prompt,
                    temperature=self.config.temperature,
                    max_tokens=self.config.max_tokens,
                )
            elif hasattr(self.engine, 'chat'):
                result = self.engine.chat(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    temperature=self.config.temperature,
                    max_tokens=self.config.max_tokens,
                )
            else:
                return self._generate_fallback(chapter_num)

            result = self._clean_output(result)
            return result

        except Exception as e:
            raise RuntimeError(f"API调用失败: {e}")

    def _build_system_prompt(self) -> str:
        parts = []

        parts.append(f"""你是一位拥有15年经验的顶级{self.config.genre}小说作家。
你的文笔老练、节奏精准、人物鲜活，读者沉浸感极强。

【核心写作原则】
1. 沉浸式叙事：让读者忘记是在"读"小说，而是"经历"故事
2. 节奏控制：紧张场景用短句加速，抒情场景用长句铺陈
3. 人物驱动：情节由人物性格和动机自然推动，而非作者安排
4. 细节真实：通过具体的感官细节建立真实感
5. 对话自然：每个角色的说话方式独一无二，读者仅凭对话就能分辨

【去AI铁律 — 必须内化到写作本能中】
- 禁止使用"首先...其次...最后"等结构化连接词
- 禁止使用"值得注意的是""综上所述""总而言之"等AI模板句式
- 禁止句长均匀（AI特征）：长短句要剧烈交替，句长方差>15
- 禁止情感平滑（AI特征）：情绪要有撕裂感，恨到极致突然温柔
- 禁止逻辑过于完美（AI特征）：加入人类的犹豫、自我纠正、思维跳跃
- 禁止词汇重复（AI特征）：同一段落内避免重复使用相同的形容词/动词
- 每500字至少1处意外用词或非常规搭配
- 30%短句(3-10字) + 50%中句(11-25字) + 20%长句(26-50字)
- 关键情节用单句成段制造冲击力
- 加入本土生活细节：烟火气、人情世故、时代印记

【输出格式】
- 直接输出小说正文，不要任何解释、标记、前缀
- 不要写"本章完""第X章"等标记（标题由系统自动添加）
- 段落间用空行分隔
- 对话使用中文引号「」
""")

        if self.genre_manager:
            genre_context = self.genre_manager.get_full_generation_context(
                include_pleasure=True
            )
            if genre_context:
                parts.append(genre_context)

        if self.knowledge_engine:
            try:
                knowledge_prompt = self.knowledge_engine.inject_knowledge_to_prompt(
                    base_prompt="",
                    genre=self.config.genre,
                    chapter_num=getattr(self, '_current_chapter', 1),
                    character_count=self._get_character_count(),
                )
                if knowledge_prompt:
                    parts.append(knowledge_prompt)
            except Exception:
                pass

        return "\n\n".join(parts)

    def _build_user_prompt(self, chapter_num: int, attempt: int) -> str:
        parts = []

        parts.append(f"请写《{self.novel_title}》第{chapter_num}章。")

        memory_context = ""
        if self.memory:
            memory_context = self._build_memory_context(chapter_num)

        if memory_context:
            parts.append(f"\n【已有故事信息】\n{memory_context}")

        prev_chapter = self.chapters.get(chapter_num - 1)
        if prev_chapter and prev_chapter.content:
            summary = self._summarize_previous(prev_chapter.content)
            parts.append(f"\n【上一章概要】\n{summary}")

        if self.voice_injector and self.memory:
            active_chars = self._get_active_characters(chapter_num)
            if active_chars:
                voice_prompt = self.voice_injector.build_full_injection_prompt(
                    active_chars
                )
                if voice_prompt:
                    parts.append(voice_prompt)

        parts.append(f"\n【本章要求】")
        parts.append(f"- 目标字数: {self.config.target_words_per_chapter}字左右")
        parts.append(f"- 包含对话、动作描写、心理活动、环境描写")
        parts.append(f"- 章末留悬念或情感钩子")
        parts.append(f"- 严格遵循系统提示中的去AI铁律")

        if attempt > 1:
            parts.append(f"- 这是第{attempt}次尝试，请确保字数充足")

        return "\n".join(parts)

    def _build_memory_context(self, chapter_num: int) -> str:
        if not self.memory:
            return ""

        try:
            context_parts = []

            if hasattr(self.memory, 'intelligent_search'):
                results = self.memory.intelligent_search(
                    query=f"第{chapter_num}章",
                    search_types=['character', 'plot', 'setting', 'foreshadowing'],
                    max_results=15,
                )
                if results:
                    context_parts.append("【关键记忆】")
                    for r in results[:10]:
                        context_parts.append(f"- [{r.source_type}] {r.content[:120]}")

            if hasattr(self.memory, 'characters'):
                chars = self.memory.characters
                if chars:
                    alive_chars = [
                        f"{name}({info.status if hasattr(info, 'status') else '存活'})"
                        for name, info in list(chars.items())[:8]
                    ]
                    context_parts.append(f"【角色列表】{', '.join(alive_chars)}")

            return "\n".join(context_parts)
        except Exception:
            return ""

    def _summarize_previous(self, content: str) -> str:
        sentences = re.split(r'[。！？]', content)
        key_sentences = [s.strip() for s in sentences
                         if len(s.strip()) > 15][:5]
        return "。".join(key_sentences) + "。"

    def _get_active_characters(self, chapter_num: int) -> List[str]:
        if not self.memory or not hasattr(self.memory, 'characters'):
            return []

        active = []
        for name, info in self.memory.characters.items():
            status = getattr(info, 'status', '存活')
            last_ch = getattr(info, 'last_appearance_chapter', 0)
            if status == '存活' and abs(chapter_num - last_ch) <= 10:
                active.append(name)
        return active[:5]

    def _get_character_count(self) -> int:
        if not self.memory or not hasattr(self.memory, 'characters'):
            return 0
        return len(self.memory.characters)

    def _clean_output(self, text: str) -> str:
        text = re.sub(r'```.*?\n|```', '', text)
        text = re.sub(r'^第[一二三四五六七八九十\d]+章[^\n]*\n?', '', text.strip())
        text = re.sub(r'（本章完）|\(本章完\)|本章结束|未完待续', '', text)
        return text.strip()

    def _post_generation_hooks(self, chapter_num: int, content: str):
        if self.memory:
            try:
                if hasattr(self.memory, 'save_conversation'):
                    self.memory.save_conversation(
                        "system",
                        f"第{chapter_num}章生成完成 ({len(content)}字)"
                    )
                if hasattr(self.memory, 'record_plot_event'):
                    self.memory.record_plot_event(
                        chapter_num, content[:200], tags=["auto_generated"]
                    )
            except Exception:
                pass

        if self.config.auto_save and self.config.save_dir:
            self._auto_save_chapter(chapter_num, content)

        if self.config.auto_analyze:
            self._auto_analyze_chapter(chapter_num, content)

    def _auto_analyze_chapter(self, chapter_num: int, content: str):
        """自动分析章节质量 — AI痕迹 + 节奏 + 爽点"""
        print(f"\n  🔍 自动质检 第{chapter_num}章:")

        ai_warning = None
        beat_warning = None

        if self.knowledge_engine:
            try:
                diagnosis = self.knowledge_engine.diagnose_ai_traits(content)
                ai_score = diagnosis.overall_ai_score

                if ai_score >= self.config.ai_score_warn_threshold:
                    top_traits = diagnosis.detected_traits[:3]
                    trait_names = ", ".join(t[0] for t in top_traits)
                    ai_warning = (
                        f"⚠️ AI痕迹偏高 ({ai_score:.0%}), "
                        f"主要特征: {trait_names}"
                    )
                    print(f"    {ai_warning}")
                    print(f"    修复建议: {diagnosis.fix_priority[0][:80] if diagnosis.fix_priority else '无'}")
                else:
                    print(f"    ✅ AI痕迹: {ai_score:.0%} (安全)")

            except Exception as e:
                print(f"    ⚠️ AI诊断跳过: {e}")

        if self.beat_analyzer:
            try:
                is_opening = chapter_num <= 3
                rhythm = self.beat_analyzer.analyze(content, chapter_num, is_opening)

                if rhythm.beat_density < self.config.beat_density_warn_threshold:
                    beat_warning = (
                        f"⚠️ 爽点密度偏低 ({rhythm.beat_density:.1f}/千字), "
                        f"建议≥{self.config.beat_density_warn_threshold}"
                    )
                    print(f"    {beat_warning}")
                else:
                    print(f"    ✅ 爽点密度: {rhythm.beat_density:.1f}/千字")

                if rhythm.score < 60:
                    print(f"    ⚠️ 节奏评分: {rhythm.score}/100")
                    for issue in rhythm.issues[:2]:
                        print(f"      - {issue}")
                else:
                    print(f"    ✅ 节奏评分: {rhythm.score}/100")

                if rhythm.hook_strength < 0.5:
                    print(f"    ⚠️ 钩子强度不足 ({rhythm.hook_strength:.0%}), 章末需加强悬念")

            except Exception as e:
                print(f"    ⚠️ 节奏分析跳过: {e}")

        if ai_warning or beat_warning:
            print(f"    💡 建议在下一章prompt中针对性优化")

    def _auto_save_chapter(self, chapter_num: int, content: str):
        try:
            os.makedirs(self.config.save_dir, exist_ok=True)
            safe_name = re.sub(r'[<>:"/\\|?*]', '_', self.novel_title)
            filename = f"{safe_name}_第{chapter_num}章.txt"
            filepath = os.path.join(self.config.save_dir, filename)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"《{self.novel_title}》第{chapter_num}章\n\n")
                f.write(content)

            print(f"  💾 已保存: {filepath}")
        except Exception as e:
            print(f"  ⚠️ 保存失败: {e}")

    def _generate_fallback(self, chapter_num: int) -> str:
        return f"""第{chapter_num}章

夜色如墨。

风从山谷深处灌上来，带着腐叶和湿土的气味。

他站在崖边，脚下是万丈深渊。身后——追兵已至。

（本章需要通过AI接口生成。请配置DeepSeek API后重试，或检查creative_engine是否正确初始化。）
"""

    def _build_summary(self, results: Dict, total_time: float,
                        failed: List[int]) -> Dict:
        success_count = sum(
            1 for r in results.values()
            if isinstance(r, dict) and r.get("success")
        )
        total_words = sum(
            r.get("word_count", 0) for r in results.values()
            if isinstance(r, dict)
        )

        print(f"\n{'='*60}")
        print(f"📊 直出管线摘要")
        print(f"{'='*60}")
        print(f"  总耗时: {total_time:.1f}秒")
        print(f"  成功: {success_count}/{len(results)}章")
        print(f"  总字数: {total_words}字")
        print(f"  API调用: {self.total_api_calls}次")
        if failed:
            print(f"  失败章节: {failed}")
        print(f"{'='*60}")

        return {
            "novel_title": self.novel_title,
            "genre": self.config.genre,
            "total_time_s": round(total_time, 1),
            "total_chapters": len(results),
            "success_count": success_count,
            "failed_chapters": failed,
            "total_words": total_words,
            "total_api_calls": self.total_api_calls,
            "results": results,
        }

    def get_progress(self) -> Dict:
        completed = sum(
            1 for r in self.chapters.values()
            if r.status == "completed"
        )
        return {
            "state": self.state.value,
            "novel_title": self.novel_title,
            "total_chapters": len(self.chapters),
            "completed_chapters": completed,
            "total_api_calls": self.total_api_calls,
            "elapsed_time_s": time.time() - self.start_time if self.start_time else 0,
        }

    def export_config(self) -> Dict:
        return {
            "novel_title": self.novel_title,
            "genre": self.config.genre,
            "theme": self.config.theme,
            "target_words_per_chapter": self.config.target_words_per_chapter,
            "temperature": self.config.temperature,
            "continue_from_chapter": self.config.continue_from_chapter,
            "save_dir": self.config.save_dir,
        }

    def import_config(self, config: Dict):
        for key, value in config.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
            elif key == "novel_title":
                self.novel_title = value


if __name__ == "__main__":
    print("=" * 60)
    print("SimpleDirectPipeline 功能验证")
    print("=" * 60)

    pipeline = SimpleDirectPipeline()
    pipeline.novel_title = "测试作品"
    pipeline.configure(
        genre="玄幻",
        theme="少年修仙",
        target_words_per_chapter=2000,
        auto_save=False,
    )

    print("\n[1] 配置导出...")
    config = pipeline.export_config()
    print(f"  {json.dumps(config, ensure_ascii=False, indent=2)}")

    print("\n[2] 无引擎时的fallback...")
    content = pipeline._generate_fallback(1)
    print(f"  Fallback长度: {len(content)}字")

    print("\n[3] 进度查询...")
    progress = pipeline.get_progress()
    print(f"  状态: {progress['state']}")

    print("\n[4] 输出清洗...")
    test_text = """```markdown
第1章 测试章节
这是正文内容。
（本章完）
```"""
    cleaned = pipeline._clean_output(test_text)
    print(f"  清洗后: {cleaned[:100]}")

    print("\n✅ SimpleDirectPipeline 验证完成")
