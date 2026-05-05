#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 多平台格式化导出系统 - PlatformExporter

对标百度作家平台，核心能力：
1. 起点中文网 / 番茄小说 / 纵横中文网 / 七猫小说 / 飞卢小说 / 掌阅 / 豆瓣阅读
2. 通用TXT / Markdown / HTML / EPUB / DOCX / LaTeX 导出
3. 章节自动分卷 + 多级目录生成
4. 封面信息嵌入 + 封面HTML生成
5. 导出预设系统 + 批量导出 + 导出历史
6. 字数统计 + 导出质量验证
"""

import json
import os
import re
import zipfile
import shutil
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Callable
from dataclasses import dataclass, field
from enum import Enum
from collections import Counter


class ExportPlatform(Enum):
    QIDIAN = ("起点中文网", "qidian", "utf-8", "txt")
    FANQIE = ("番茄小说", "fanqie", "utf-8", "md")
    ZONGHENG = ("纵横中文网", "zongheng", "utf-8", "txt")
    QIMAO = ("七猫小说", "qimao", "utf-8", "txt")
    FEILU = ("飞卢小说", "feilu", "utf-8", "txt")
    ZHANGYUE = ("掌阅", "zhangyue", "utf-8", "html")
    DOUBAN = ("豆瓣阅读", "douban", "utf-8", "md")
    TXT = ("通用TXT", "txt", "utf-8", "txt")
    MARKDOWN = ("Markdown", "md", "utf-8", "md")
    HTML = ("HTML网页", "html", "utf-8", "html")
    EPUB = ("EPUB电子书", "epub", "utf-8", "epub")
    DOCX = ("Word文档", "docx", "utf-8", "docx")
    LATEX = ("LaTeX排版", "latex", "utf-8", "tex")

    def __init__(self, label: str, ext: str, encoding: str, format_type: str):
        self.label = label
        self.ext = ext
        self.encoding = encoding
        self.format_type = format_type


@dataclass
class ChapterData:
    chapter_num: int
    title: str
    content: str
    word_count: int
    volume: int = 1
    volume_title: str = ""
    summary: str = ""
    created_at: str = ""


@dataclass
class NovelMeta:
    title: str
    author: str
    genre: str
    sub_genre: str = ""
    synopsis: str = ""
    tags: List[str] = field(default_factory=list)
    cover_path: str = ""
    total_words: int = 0
    status: str = "连载中"
    pen_name: str = ""
    contact: str = ""
    copyright_info: str = ""


@dataclass
class ExportPreset:
    preset_id: str
    name: str
    platforms: List[ExportPlatform]
    output_dir: str = ""
    include_cover: bool = True
    include_toc: bool = True
    split_by_volume: bool = False
    encoding: str = "utf-8"
    custom_css: str = ""
    created_at: str = ""
    last_used_at: str = ""


@dataclass
class ExportRecord:
    record_id: str
    preset_name: str
    platform: str
    output_path: str
    chapter_count: int
    total_words: int
    file_size_bytes: int
    duration_seconds: float
    success: bool
    error_message: str = ""
    exported_at: str = ""


@dataclass
class WordCountStats:
    total_chapters: int
    total_words: int
    total_characters: int
    avg_words_per_chapter: float
    min_words_chapter: Tuple[int, int]
    max_words_chapter: Tuple[int, int]
    words_by_volume: Dict[int, int] = field(default_factory=dict)
    daily_output: Dict[str, int] = field(default_factory=dict)


class PlatformExporter:
    """多平台格式化导出"""

    def __init__(self, output_dir: str = None):
        if output_dir is None:
            output_dir = os.path.join(os.path.dirname(__file__), "..", "..", "exports")
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

        self.presets: Dict[str, ExportPreset] = {}
        self.export_history: List[ExportRecord] = []
        self._record_counter = 0
        self._preset_counter = 0

        self._init_builtin_presets()
        self._load_data()

    def _init_builtin_presets(self):
        builtins = [
            ("default_all", "全平台导出", list(ExportPlatform), True, True, False),
            ("novel_sites", "小说网站三件套",
             [ExportPlatform.QIDIAN, ExportPlatform.FANQIE, ExportPlatform.ZONGHENG],
             True, True, False),
            ("mobile_reading", "移动阅读",
             [ExportPlatform.TXT, ExportPlatform.EPUB, ExportPlatform.HTML],
             True, True, False),
            ("backup_only", "纯文本备份",
             [ExportPlatform.TXT, ExportPlatform.MARKDOWN],
             False, False, True),
            ("publishing", "出版级导出",
             [ExportPlatform.DOCX, ExportPlatform.LATEX, ExportPlatform.EPUB],
             True, True, True),
        ]

        for pid, name, platforms, cover, toc, split_vol in builtins:
            self._preset_counter += 1
            preset_id = f"PRESET_{self._preset_counter:04d}"
            self.presets[preset_id] = ExportPreset(
                preset_id=preset_id,
                name=name,
                platforms=platforms,
                include_cover=cover,
                include_toc=toc,
                split_by_volume=split_vol,
                created_at=datetime.now().isoformat(),
            )

    def export(self, meta: NovelMeta, chapters: List[ChapterData],
               platform: ExportPlatform) -> str:
        method_map = {
            ExportPlatform.QIDIAN: self._export_qidian,
            ExportPlatform.FANQIE: self._export_fanqie,
            ExportPlatform.ZONGHENG: self._export_zongheng,
            ExportPlatform.QIMAO: self._export_qimao,
            ExportPlatform.FEILU: self._export_feilu,
            ExportPlatform.ZHANGYUE: self._export_zhangyue,
            ExportPlatform.DOUBAN: self._export_douban,
            ExportPlatform.TXT: self._export_txt,
            ExportPlatform.MARKDOWN: self._export_markdown,
            ExportPlatform.HTML: self._export_html,
            ExportPlatform.EPUB: self._export_epub,
            ExportPlatform.DOCX: self._export_docx,
            ExportPlatform.LATEX: self._export_latex,
        }
        exporter = method_map.get(platform, self._export_txt)
        return exporter(meta, chapters)

    def export_all(self, meta: NovelMeta, chapters: List[ChapterData]) -> Dict[str, str]:
        results = {}
        for platform in ExportPlatform:
            try:
                path = self.export(meta, chapters, platform)
                results[platform.label] = path
            except Exception as e:
                results[platform.label] = f"导出失败: {e}"
        return results

    def export_with_preset(self, preset_id: str, meta: NovelMeta,
                           chapters: List[ChapterData]) -> Dict[str, str]:
        preset = self.presets.get(preset_id)
        if not preset:
            return {"error": f"预设不存在: {preset_id}"}

        results = {}
        for platform in preset.platforms:
            try:
                path = self.export(meta, chapters, platform)
                results[platform.label] = path
                self._record_export(preset.name, platform.label, path,
                                    chapters, True)
            except Exception as e:
                results[platform.label] = f"导出失败: {e}"
                self._record_export(preset.name, platform.label, "",
                                    chapters, False, str(e))

        preset.last_used_at = datetime.now().isoformat()
        return results

    def _record_export(self, preset_name: str, platform: str,
                       path: str, chapters: List[ChapterData],
                       success: bool, error: str = ""):
        self._record_counter += 1
        file_size = os.path.getsize(path) if success and os.path.exists(path) else 0
        total_words = sum(ch.word_count for ch in chapters)

        self.export_history.append(ExportRecord(
            record_id=f"REC_{self._record_counter:06d}",
            preset_name=preset_name,
            platform=platform,
            output_path=path,
            chapter_count=len(chapters),
            total_words=total_words,
            file_size_bytes=file_size,
            duration_seconds=0,
            success=success,
            error_message=error,
            exported_at=datetime.now().isoformat(),
        ))

    def create_preset(self, name: str, platforms: List[ExportPlatform],
                      **kwargs) -> str:
        self._preset_counter += 1
        preset_id = f"PRESET_{self._preset_counter:04d}"
        self.presets[preset_id] = ExportPreset(
            preset_id=preset_id,
            name=name,
            platforms=platforms,
            output_dir=kwargs.get("output_dir", ""),
            include_cover=kwargs.get("include_cover", True),
            include_toc=kwargs.get("include_toc", True),
            split_by_volume=kwargs.get("split_by_volume", False),
            encoding=kwargs.get("encoding", "utf-8"),
            custom_css=kwargs.get("custom_css", ""),
            created_at=datetime.now().isoformat(),
        )
        self._save_data()
        return preset_id

    def delete_preset(self, preset_id: str) -> bool:
        if preset_id in self.presets:
            del self.presets[preset_id]
            self._save_data()
            return True
        return False

    def get_export_history(self, limit: int = 20) -> List[ExportRecord]:
        return sorted(self.export_history,
                      key=lambda r: r.exported_at, reverse=True)[:limit]

    def compute_word_stats(self, chapters: List[ChapterData]) -> WordCountStats:
        if not chapters:
            return WordCountStats(0, 0, 0, 0, (0, 0), (0, 0))

        sorted_ch = sorted(chapters, key=lambda c: c.chapter_num)
        total_words = sum(ch.word_count for ch in sorted_ch)
        total_chars = sum(len(ch.content) for ch in sorted_ch)
        avg_words = total_words / len(sorted_ch)

        min_ch = min(sorted_ch, key=lambda c: c.word_count)
        max_ch = max(sorted_ch, key=lambda c: c.word_count)

        words_by_volume: Dict[int, int] = {}
        for ch in sorted_ch:
            words_by_volume[ch.volume] = words_by_volume.get(ch.volume, 0) + ch.word_count

        daily_output: Dict[str, int] = {}
        for ch in sorted_ch:
            if ch.created_at:
                day = ch.created_at[:10]
                daily_output[day] = daily_output.get(day, 0) + ch.word_count

        return WordCountStats(
            total_chapters=len(sorted_ch),
            total_words=total_words,
            total_characters=total_chars,
            avg_words_per_chapter=round(avg_words, 1),
            min_words_chapter=(min_ch.chapter_num, min_ch.word_count),
            max_words_chapter=(max_ch.chapter_num, max_ch.word_count),
            words_by_volume=words_by_volume,
            daily_output=daily_output,
        )

    def generate_cover_html(self, meta: NovelMeta,
                            chapters: List[ChapterData]) -> str:
        stats = self.compute_word_stats(chapters)
        output_path = os.path.join(self.output_dir, "cover",
                                   f"{self._safe_filename(meta.title)}_封面.html")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        tag_html = " ".join(
            f'<span class="tag">{t}</span>' for t in meta.tags
        )

        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>{meta.title} - 封面</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
    display: flex; justify-content: center; align-items: center;
    min-height: 100vh; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    font-family: 'Microsoft YaHei', 'Noto Serif SC', serif;
}}
.cover {{
    width: 600px; padding: 60px 50px;
    background: linear-gradient(180deg, #faf3e0 0%, #f5e6ca 50%, #e8d5b7 100%);
    border: 3px solid #8b7355; border-radius: 4px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.5), inset 0 0 30px rgba(139,115,85,0.1);
    text-align: center; position: relative;
}}
.cover::before {{
    content: ''; position: absolute; top: 15px; left: 15px; right: 15px; bottom: 15px;
    border: 1px solid #c4a97d; pointer-events: none;
}}
.title {{
    font-size: 36px; font-weight: bold; color: #3e2723;
    margin: 30px 0 15px; letter-spacing: 8px;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
}}
.subtitle {{
    font-size: 16px; color: #6d4c41; margin-bottom: 40px;
    letter-spacing: 4px;
}}
.author-line {{
    font-size: 18px; color: #5d4037; margin: 20px 0;
    letter-spacing: 3px;
}}
.divider {{
    width: 100px; height: 2px; background: #8b7355;
    margin: 25px auto; opacity: 0.6;
}}
.info-grid {{
    display: grid; grid-template-columns: 1fr 1fr;
    gap: 12px 30px; margin: 30px 0; text-align: left;
    font-size: 14px; color: #5d4037;
}}
.info-item {{ display: flex; justify-content: space-between; }}
.info-label {{ color: #8b7355; }}
.info-value {{ font-weight: bold; }}
.synopsis {{
    font-size: 14px; color: #4e342e; line-height: 1.8;
    margin: 25px 0; padding: 20px; text-align: left;
    background: rgba(139,115,85,0.08); border-radius: 4px;
    font-style: italic;
}}
.tags {{ margin: 20px 0; }}
.tag {{
    display: inline-block; padding: 3px 12px; margin: 3px;
    background: #8b7355; color: #faf3e0; border-radius: 12px;
    font-size: 12px; letter-spacing: 1px;
}}
.stats {{
    margin-top: 30px; padding-top: 20px;
    border-top: 1px dashed #c4a97d;
    font-size: 13px; color: #8b7355;
}}
.footer {{
    margin-top: 40px; font-size: 12px; color: #a1887f;
    letter-spacing: 2px;
}}
</style>
</head>
<body>
<div class="cover">
    <div class="title">{meta.title}</div>
    <div class="subtitle">{meta.genre}{' · ' + meta.sub_genre if meta.sub_genre else ''}</div>
    <div class="divider"></div>
    <div class="author-line">作者：{meta.author}</div>
    <div class="info-grid">
        <div class="info-item"><span class="info-label">总字数</span><span class="info-value">{stats.total_words:,}</span></div>
        <div class="info-item"><span class="info-label">总章节</span><span class="info-value">{stats.total_chapters}</span></div>
        <div class="info-item"><span class="info-label">状态</span><span class="info-value">{meta.status}</span></div>
        <div class="info-item"><span class="info-label">均章字数</span><span class="info-value">{stats.avg_words_per_chapter:,.0f}</span></div>
    </div>
    <div class="synopsis">{meta.synopsis}</div>
    <div class="tags">{tag_html}</div>
    <div class="stats">
        首章 {stats.min_words_chapter[1]:,} 字 · 最长章 {stats.max_words_chapter[1]:,} 字
    </div>
    <div class="footer">{meta.copyright_info or '© ' + datetime.now().strftime('%Y') + ' ' + meta.author + ' 版权所有'}</div>
</div>
</body>
</html>"""

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)
        return output_path

    def generate_toc_html(self, meta: NovelMeta,
                          chapters: List[ChapterData]) -> str:
        output_path = os.path.join(self.output_dir, "toc",
                                   f"{self._safe_filename(meta.title)}_目录.html")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        sorted_ch = sorted(chapters, key=lambda c: (c.volume, c.chapter_num))
        volumes: Dict[int, List[ChapterData]] = {}
        for ch in sorted_ch:
            if ch.volume not in volumes:
                volumes[ch.volume] = []
            volumes[ch.volume].append(ch)

        toc_items = []
        for vol_num in sorted(volumes):
            vol_chapters = volumes[vol_num]
            vol_title = vol_chapters[0].volume_title or f"第{vol_num}卷"
            vol_words = sum(ch.word_count for ch in vol_chapters)

            toc_items.append(f"""
            <li class="volume">
                <span class="vol-title">{vol_title}</span>
                <span class="vol-stats">({len(vol_chapters)}章 · {vol_words:,}字)</span>
                <ul class="chapter-list">""")

            for ch in vol_chapters:
                toc_items.append(f"""
                    <li class="chapter-item">
                        <span class="ch-num">第{ch.chapter_num}章</span>
                        <span class="ch-title">{ch.title}</span>
                        <span class="ch-words">{ch.word_count:,}字</span>
                    </li>""")

            toc_items.append("</ul></li>")

        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>{meta.title} - 目录</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
    max-width: 700px; margin: 0 auto; padding: 40px 20px;
    font-family: 'Microsoft YaHei', sans-serif;
    background: #fdf6ec; color: #3e2723;
}}
h1 {{ text-align: center; font-size: 28px; margin-bottom: 10px; letter-spacing: 4px; }}
.meta {{ text-align: center; color: #8b7355; margin-bottom: 30px; font-size: 14px; }}
.volume {{ list-style: none; margin-bottom: 25px; }}
.vol-title {{
    font-size: 20px; font-weight: bold; color: #5d4037;
    display: block; padding: 8px 0; border-bottom: 2px solid #c4a97d;
}}
.vol-stats {{ font-size: 13px; color: #a1887f; margin-left: 10px; }}
.chapter-list {{ list-style: none; margin-top: 8px; }}
.chapter-item {{
    display: flex; align-items: baseline; padding: 6px 12px;
    border-bottom: 1px dotted #e8d5b7; font-size: 15px;
}}
.chapter-item:hover {{ background: rgba(139,115,85,0.08); }}
.ch-num {{ color: #8b7355; min-width: 80px; font-size: 13px; }}
.ch-title {{ flex: 1; }}
.ch-words {{ color: #a1887f; font-size: 12px; min-width: 60px; text-align: right; }}
</style>
</head>
<body>
<h1>《{meta.title}》</h1>
<div class="meta">作者：{meta.author} · 共{len(chapters)}章 · {sum(ch.word_count for ch in chapters):,}字</div>
<ul>{"".join(toc_items)}</ul>
</body>
</html>"""

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)
        return output_path

    def validate_export(self, filepath: str,
                        platform: ExportPlatform) -> Dict[str, Any]:
        result = {
            "filepath": filepath,
            "platform": platform.label,
            "exists": os.path.exists(filepath),
            "size_bytes": 0,
            "encoding_valid": True,
            "structure_valid": True,
            "warnings": [],
            "errors": [],
        }

        if not result["exists"]:
            result["errors"].append("文件不存在")
            return result

        result["size_bytes"] = os.path.getsize(filepath)
        if result["size_bytes"] == 0:
            result["errors"].append("文件为空")

        try:
            with open(filepath, "r", encoding=platform.encoding) as f:
                content = f.read(10000)
        except UnicodeDecodeError:
            result["encoding_valid"] = False
            result["errors"].append(f"编码不匹配，期望{platform.encoding}")

        if platform == ExportPlatform.EPUB:
            if not zipfile.is_zipfile(filepath):
                result["structure_valid"] = False
                result["errors"].append("EPUB文件结构无效")
            else:
                with zipfile.ZipFile(filepath, "r") as zf:
                    required = ["mimetype", "META-INF/container.xml"]
                    for req in required:
                        if req not in zf.namelist():
                            result["warnings"].append(f"缺少必要文件: {req}")

        if platform == ExportPlatform.HTML:
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    html_content = f.read(5000)
                if "<!DOCTYPE html>" not in html_content:
                    result["warnings"].append("缺少DOCTYPE声明")
                if "</html>" not in html_content:
                    result["warnings"].append("HTML结构不完整")
            except Exception:
                pass

        return result

    def _safe_filename(self, name: str) -> str:
        return re.sub(r'[<>:"/\\|?*]', '_', name)

    def _get_output_path(self, meta: NovelMeta, platform: ExportPlatform,
                         subdir: str = "") -> str:
        safe_title = self._safe_filename(meta.title)
        dir_path = self.output_dir
        if subdir:
            dir_path = os.path.join(dir_path, subdir)
        os.makedirs(dir_path, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.join(
            dir_path, f"{safe_title}_{timestamp}.{platform.ext}"
        )

    def _format_chapter_content(self, chapter: ChapterData,
                                platform: ExportPlatform) -> str:
        lines = []
        lines.append(f"第{chapter.chapter_num}章 {chapter.title}")
        lines.append("")
        lines.append(chapter.content.strip())
        lines.append("")
        return "\n".join(lines)

    def _group_by_volume(self, chapters: List[ChapterData]
                         ) -> Dict[int, List[ChapterData]]:
        volumes: Dict[int, List[ChapterData]] = {}
        for ch in sorted(chapters, key=lambda c: c.chapter_num):
            if ch.volume not in volumes:
                volumes[ch.volume] = []
            volumes[ch.volume].append(ch)
        return volumes

    def _export_qidian(self, meta: NovelMeta, chapters: List[ChapterData]) -> str:
        output_path = self._get_output_path(meta, ExportPlatform.QIDIAN, "qidian")
        lines = []

        lines.append(f"书名：{meta.title}")
        lines.append(f"作者：{meta.author}")
        lines.append(f"类型：{meta.genre}")
        if meta.sub_genre:
            lines.append(f"子类型：{meta.sub_genre}")
        lines.append(f"简介：{meta.synopsis}")
        lines.append(f"标签：{'/'.join(meta.tags)}")
        lines.append("=" * 50)
        lines.append("")

        current_volume = 0
        for ch in sorted(chapters, key=lambda c: c.chapter_num):
            if ch.volume != current_volume:
                current_volume = ch.volume
                vol_title = ch.volume_title or f"第{current_volume}卷"
                lines.append(f"\n{'=' * 20} {vol_title} {'=' * 20}\n")
            lines.append(self._format_chapter_content(ch, ExportPlatform.QIDIAN))
            lines.append("-" * 30)

        content = "\n".join(lines)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        return output_path

    def _export_fanqie(self, meta: NovelMeta, chapters: List[ChapterData]) -> str:
        output_path = self._get_output_path(meta, ExportPlatform.FANQIE, "fanqie")
        lines = []

        lines.append(f"# {meta.title}")
        lines.append(f"作者: {meta.author}")
        lines.append(f"分类: {meta.genre}")
        lines.append(f"简介: {meta.synopsis}")
        lines.append("")

        for ch in sorted(chapters, key=lambda c: c.chapter_num):
            lines.append(f"## 第{ch.chapter_num}章 {ch.title}")
            lines.append("")
            lines.append(ch.content.strip())
            lines.append("")
            lines.append("---")
            lines.append("")

        content = "\n".join(lines)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        return output_path

    def _export_zongheng(self, meta: NovelMeta, chapters: List[ChapterData]) -> str:
        output_path = self._get_output_path(meta, ExportPlatform.ZONGHENG, "zongheng")
        lines = []

        lines.append(f"《{meta.title}》")
        lines.append(f"作者：{meta.author}")
        lines.append(f"类别：{meta.genre} | 状态：{meta.status}")
        lines.append(f"简介：{meta.synopsis}")
        lines.append("=" * 60)
        lines.append("")

        for ch in sorted(chapters, key=lambda c: c.chapter_num):
            lines.append(f"正文 第{ch.chapter_num}章 {ch.title}")
            lines.append("")
            lines.append("　　" + ch.content.strip().replace("\n", "\n　　"))
            lines.append("")

        content = "\n".join(lines)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        return output_path

    def _export_qimao(self, meta: NovelMeta, chapters: List[ChapterData]) -> str:
        output_path = self._get_output_path(meta, ExportPlatform.QIMAO, "qimao")
        lines = []

        lines.append(f"《{meta.title}》")
        lines.append(f"作者：{meta.author}")
        lines.append(f"类型：{meta.genre}")
        lines.append(f"简介：{meta.synopsis}")
        lines.append("=" * 40)
        lines.append("")

        for ch in sorted(chapters, key=lambda c: c.chapter_num):
            lines.append(f"第{ch.chapter_num}章 {ch.title}")
            lines.append("")
            for paragraph in ch.content.strip().split("\n"):
                if paragraph.strip():
                    lines.append("    " + paragraph.strip())
            lines.append("")
            lines.append("—" * 30)
            lines.append("")

        content = "\n".join(lines)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        return output_path

    def _export_feilu(self, meta: NovelMeta, chapters: List[ChapterData]) -> str:
        output_path = self._get_output_path(meta, ExportPlatform.FEILU, "feilu")
        lines = []

        lines.append(f"书名：《{meta.title}》")
        lines.append(f"笔名：{meta.pen_name or meta.author}")
        lines.append(f"分类：{meta.genre}")
        lines.append(f"简介：{meta.synopsis}")
        lines.append("=" * 50)
        lines.append("")

        for ch in sorted(chapters, key=lambda c: c.chapter_num):
            lines.append(f"第{ch.chapter_num}章 {ch.title}")
            lines.append("")
            lines.append(ch.content.strip())
            lines.append("")
            lines.append("——")
            lines.append("")

        content = "\n".join(lines)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        return output_path

    def _export_zhangyue(self, meta: NovelMeta, chapters: List[ChapterData]) -> str:
        output_path = self._get_output_path(meta, ExportPlatform.ZHANGYUE, "zhangyue")
        sorted_ch = sorted(chapters, key=lambda c: c.chapter_num)

        toc_items = []
        content_items = []
        for ch in sorted_ch:
            ch_id = f"ch{ch.chapter_num}"
            toc_items.append(
                f'<li><a href="#{ch_id}">第{ch.chapter_num}章 {ch.title}</a></li>'
            )
            paras = "".join(
                f"<p>{p.strip()}</p>"
                for p in ch.content.strip().split("\n") if p.strip()
            )
            content_items.append(f"""
            <div class="chapter" id="{ch_id}">
                <h2>第{ch.chapter_num}章 {ch.title}</h2>
                <div class="content">{paras}</div>
            </div>""")

        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{meta.title}</title>
<style>
body {{ font-family: 'PingFang SC', 'Hiragino Sans GB', sans-serif;
       max-width: 750px; margin: 0 auto; padding: 15px;
       background: #f8f4ed; color: #333; line-height: 1.9; }}
h1 {{ text-align: center; font-size: 24px; margin: 20px 0; }}
.meta {{ text-align: center; color: #888; font-size: 13px; margin-bottom: 20px; }}
.toc {{ background: #fff; padding: 15px 20px; border-radius: 8px; margin-bottom: 25px; }}
.toc h3 {{ margin: 0 0 10px; font-size: 16px; }}
.toc ul {{ list-style: none; padding: 0; }}
.toc li {{ padding: 4px 0; border-bottom: 1px dotted #eee; font-size: 14px; }}
.toc a {{ color: #b8860b; text-decoration: none; }}
.chapter {{ margin-bottom: 30px; }}
.chapter h2 {{ font-size: 18px; border-left: 4px solid #b8860b; padding-left: 10px; }}
.content p {{ text-indent: 2em; margin: 8px 0; }}
</style>
</head>
<body>
<h1>{meta.title}</h1>
<div class="meta">作者：{meta.author} · {meta.genre} · {meta.status}</div>
<div class="toc"><h3>目录</h3><ul>{"".join(toc_items)}</ul></div>
{"".join(content_items)}
</body>
</html>"""

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)
        return output_path

    def _export_douban(self, meta: NovelMeta, chapters: List[ChapterData]) -> str:
        output_path = self._get_output_path(meta, ExportPlatform.DOUBAN, "douban")
        lines = []

        lines.append(f"# 《{meta.title}》")
        lines.append("")
        lines.append(f"**作者**：{meta.author}")
        lines.append(f"**分类**：{meta.genre}")
        lines.append(f"**状态**：{meta.status}")
        lines.append("")
        lines.append(f"> {meta.synopsis}")
        lines.append("")
        lines.append("---")
        lines.append("")

        volumes = self._group_by_volume(chapters)
        for vol_num in sorted(volumes):
            vol_chapters = volumes[vol_num]
            vol_title = vol_chapters[0].volume_title or f"第{vol_num}卷"
            lines.append(f"## {vol_title}")
            lines.append("")

            for ch in vol_chapters:
                lines.append(f"### 第{ch.chapter_num}章 {ch.title}")
                lines.append("")
                lines.append(ch.content.strip())
                lines.append("")
                lines.append("* * *")
                lines.append("")

        content = "\n".join(lines)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        return output_path

    def _export_txt(self, meta: NovelMeta, chapters: List[ChapterData]) -> str:
        output_path = self._get_output_path(meta, ExportPlatform.TXT, "txt")
        lines = []

        lines.append(f"《{meta.title}》")
        lines.append(f"作者：{meta.author}")
        lines.append(f"类型：{meta.genre}")
        lines.append(f"简介：{meta.synopsis}")
        lines.append("=" * 50)
        lines.append("")

        for ch in sorted(chapters, key=lambda c: c.chapter_num):
            lines.append(f"第{ch.chapter_num}章 {ch.title}")
            lines.append("")
            lines.append(ch.content.strip())
            lines.append("")
            lines.append("")

        content = "\n".join(lines)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        return output_path

    def _export_markdown(self, meta: NovelMeta, chapters: List[ChapterData]) -> str:
        output_path = self._get_output_path(meta, ExportPlatform.MARKDOWN, "md")
        lines = []

        lines.append(f"# {meta.title}")
        lines.append("")
        lines.append(f"**作者**: {meta.author}")
        lines.append(f"**类型**: {meta.genre}")
        lines.append(f"**状态**: {meta.status}")
        lines.append("")
        lines.append(f"> {meta.synopsis}")
        lines.append("")
        lines.append("---")
        lines.append("")

        lines.append("## 目录")
        lines.append("")
        for ch in sorted(chapters, key=lambda c: c.chapter_num):
            lines.append(f"- [第{ch.chapter_num}章 {ch.title}](#chapter-{ch.chapter_num})")
        lines.append("")
        lines.append("---")
        lines.append("")

        for ch in sorted(chapters, key=lambda c: c.chapter_num):
            lines.append(f"## 第{ch.chapter_num}章 {ch.title} {{#chapter-{ch.chapter_num}}}")
            lines.append("")
            lines.append(ch.content.strip())
            lines.append("")
            lines.append("---")
            lines.append("")

        content = "\n".join(lines)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        return output_path

    def _export_html(self, meta: NovelMeta, chapters: List[ChapterData]) -> str:
        output_path = self._get_output_path(meta, ExportPlatform.HTML, "html")
        lines = []

        lines.append("<!DOCTYPE html>")
        lines.append('<html lang="zh-CN">')
        lines.append("<head>")
        lines.append('<meta charset="UTF-8">')
        lines.append('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
        lines.append(f"<title>{meta.title} - {meta.author}</title>")
        lines.append("<style>")
        lines.append("""
            :root { --primary: #1f77b4; --bg: #fdfdfd; --text: #333; }
            body { max-width: 800px; margin: 0 auto; padding: 20px;
                   font-family: 'Microsoft YaHei', 'Noto Serif SC', sans-serif;
                   line-height: 1.8; background: var(--bg); color: var(--text); }
            h1 { text-align: center; color: #222; font-size: 28px; letter-spacing: 4px; }
            .meta { text-align: center; color: #888; margin-bottom: 30px; font-size: 14px; }
            .synopsis { background: #f8f8f8; padding: 18px 22px; border-radius: 8px;
                        margin-bottom: 30px; font-style: italic; border-left: 4px solid var(--primary); }
            .toc { background: #fafafa; padding: 18px 22px; border-radius: 8px; margin-bottom: 30px; }
            .toc h3 { margin-top: 0; }
            .toc ol { padding-left: 20px; }
            .toc a { color: var(--primary); text-decoration: none; }
            .toc a:hover { text-decoration: underline; }
            .chapter { margin-bottom: 40px; }
            .chapter h2 { border-bottom: 2px solid var(--primary); padding-bottom: 10px; font-size: 20px; }
            .chapter-content p { text-indent: 2em; margin: 10px 0; }
            .back-to-top { position: fixed; bottom: 30px; right: 30px;
                          background: var(--primary); color: #fff; border: none;
                          padding: 10px 15px; border-radius: 50%; cursor: pointer;
                          font-size: 18px; opacity: 0.7; }
            .back-to-top:hover { opacity: 1; }
        """)
        lines.append("</style>")
        lines.append("</head>")
        lines.append("<body>")
        lines.append(f"<h1>{meta.title}</h1>")
        lines.append(f'<div class="meta">作者：{meta.author} | 类型：{meta.genre} | {meta.status}</div>')
        lines.append(f'<div class="synopsis">{meta.synopsis}</div>')

        lines.append('<div class="toc"><h3>📑 目录</h3><ol>')
        for ch in sorted(chapters, key=lambda c: c.chapter_num):
            lines.append(f'<li><a href="#ch{ch.chapter_num}">第{ch.chapter_num}章 {ch.title}</a></li>')
        lines.append("</ol></div>")

        for ch in sorted(chapters, key=lambda c: c.chapter_num):
            lines.append(f'<div class="chapter" id="ch{ch.chapter_num}">')
            lines.append(f"<h2>第{ch.chapter_num}章 {ch.title}</h2>")
            lines.append('<div class="chapter-content">')
            for paragraph in ch.content.strip().split("\n"):
                if paragraph.strip():
                    lines.append(f"<p>{paragraph.strip()}</p>")
            lines.append("</div></div>")

        lines.append('<button class="back-to-top" onclick="window.scrollTo({top:0,behavior:\'smooth\'})">↑</button>')
        lines.append("</body></html>")

        content = "\n".join(lines)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        return output_path

    def _export_epub(self, meta: NovelMeta, chapters: List[ChapterData]) -> str:
        output_path = self._get_output_path(meta, ExportPlatform.EPUB, "epub")

        container_xml = """<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>"""

        sorted_chapters = sorted(chapters, key=lambda c: c.chapter_num)

        manifest_items = ['<item id="cover" href="cover.xhtml" media-type="application/xhtml+xml"/>']
        spine_items = ['<itemref idref="cover"/>']

        for ch in sorted_chapters:
            ch_id = f"ch{ch.chapter_num}"
            ch_file = f"chapter{ch.chapter_num}.xhtml"
            manifest_items.append(
                f'<item id="{ch_id}" href="{ch_file}" media-type="application/xhtml+xml"/>'
            )
            spine_items.append(f'<itemref idref="{ch_id}"/>')

        content_opf = f"""<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="2.0" unique-identifier="bookid">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:title>{meta.title}</dc:title>
    <dc:creator>{meta.author}</dc:creator>
    <dc:language>zh-CN</dc:language>
    <dc:identifier id="bookid">urn:uuid:{meta.title}</dc:identifier>
    <dc:subject>{meta.genre}</dc:subject>
    <dc:description>{meta.synopsis[:200]}</dc:description>
  </metadata>
  <manifest>
    <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
    {"".join(manifest_items)}
  </manifest>
  <spine toc="ncx">
    {"".join(spine_items)}
  </spine>
</package>"""

        nav_points = []
        for ch in sorted_chapters:
            nav_points.append(f"""<navPoint id="nav{ch.chapter_num}" playOrder="{ch.chapter_num}">
      <navLabel><text>第{ch.chapter_num}章 {ch.title}</text></navLabel>
      <content src="chapter{ch.chapter_num}.xhtml"/>
    </navPoint>""")

        toc_ncx = f"""<?xml version="1.0" encoding="UTF-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
  <head><meta name="dtb:uid" content="urn:uuid:{meta.title}"/></head>
  <docTitle><text>{meta.title}</text></docTitle>
  <navMap>
    {"".join(nav_points)}
  </navMap>
</ncx>"""

        cover_html = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head><title>封面</title></head>
<body style="text-align:center;padding:40px;">
<h1 style="font-size:28px;">{meta.title}</h1>
<p style="font-size:16px;color:#666;">{meta.author} 著</p>
<p style="font-size:14px;color:#888;">{meta.genre} · {meta.status}</p>
<p style="font-size:13px;color:#999;margin-top:30px;">{meta.synopsis[:300]}</p>
</body>
</html>"""

        with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("mimetype", "application/epub+zip")
            zf.writestr("META-INF/container.xml", container_xml)
            zf.writestr("content.opf", content_opf)
            zf.writestr("toc.ncx", toc_ncx)
            zf.writestr("cover.xhtml", cover_html)

            for ch in sorted_chapters:
                ch_html = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head><title>第{ch.chapter_num}章 {ch.title}</title></head>
<body>
<h2>第{ch.chapter_num}章 {ch.title}</h2>
{"".join(f"<p>{p.strip()}</p>" for p in ch.content.strip().split("\\n") if p.strip())}
</body>
</html>"""
                zf.writestr(f"chapter{ch.chapter_num}.xhtml", ch_html)

        return output_path

    def _export_docx(self, meta: NovelMeta, chapters: List[ChapterData]) -> str:
        output_path = self._get_output_path(meta, ExportPlatform.DOCX, "docx")
        lines = []

        lines.append(f"《{meta.title}》")
        lines.append(f"作者：{meta.author}")
        lines.append(f"类型：{meta.genre} | 状态：{meta.status}")
        lines.append(f"简介：{meta.synopsis}")
        lines.append("=" * 60)
        lines.append("")

        lines.append("【目录】")
        lines.append("")
        for ch in sorted(chapters, key=lambda c: c.chapter_num):
            lines.append(f"  第{ch.chapter_num}章  {ch.title}")
        lines.append("")
        lines.append("=" * 60)
        lines.append("")

        for ch in sorted(chapters, key=lambda c: c.chapter_num):
            lines.append(f"第{ch.chapter_num}章  {ch.title}")
            lines.append("")
            for paragraph in ch.content.strip().split("\n"):
                if paragraph.strip():
                    lines.append("    " + paragraph.strip())
            lines.append("")
            lines.append("—" * 40)
            lines.append("")

        content = "\n".join(lines)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        return output_path

    def _export_latex(self, meta: NovelMeta, chapters: List[ChapterData]) -> str:
        output_path = self._get_output_path(meta, ExportPlatform.LATEX, "latex")
        lines = []

        lines.append(r"\documentclass[12pt,a4paper]{book}")
        lines.append(r"\usepackage[UTF8]{ctex}")
        lines.append(r"\usepackage{geometry}")
        lines.append(r"\geometry{left=2.5cm,right=2.5cm,top=3cm,bottom=3cm}")
        lines.append(r"\usepackage{fancyhdr}")
        lines.append(r"\pagestyle{fancy}")
        lines.append(r"\fancyhf{}")
        lines.append(r"\fancyhead[LE,RO]{\thepage}")
        lines.append(r"\fancyhead[RE]{\leftmark}")
        lines.append(r"\fancyhead[LO]{\rightmark}")
        lines.append("")
        lines.append(r"\title{" + meta.title + r"}")
        lines.append(r"\author{" + meta.author + r"}")
        lines.append(r"\date{\today}")
        lines.append("")
        lines.append(r"\begin{document}")
        lines.append(r"\maketitle")
        lines.append(r"\tableofcontents")
        lines.append(r"\newpage")
        lines.append("")

        for ch in sorted(chapters, key=lambda c: c.chapter_num):
            safe_title = ch.title.replace("&", r"\&").replace("%", r"\%")
            lines.append(r"\chapter{" + safe_title + r"}")
            lines.append("")
            for paragraph in ch.content.strip().split("\n"):
                if paragraph.strip():
                    safe_para = (paragraph.strip()
                                 .replace("&", r"\&")
                                 .replace("%", r"\%")
                                 .replace("$", r"\$")
                                 .replace("#", r"\#")
                                 .replace("_", r"\_")
                                 .replace("{", r"\{")
                                 .replace("}", r"\}"))
                    lines.append(safe_para)
                    lines.append("")
            lines.append(r"\newpage")
            lines.append("")

        lines.append(r"\end{document}")

        content = "\n".join(lines)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        return output_path

    def batch_export_from_memory(self, memory_manager,
                                 meta: NovelMeta) -> Dict[str, str]:
        chapters = []
        for ch_num in range(1, getattr(memory_manager, 'current_chapter', 0) + 1):
            ch_data = getattr(memory_manager, 'get_chapter', lambda x: None)(ch_num)
            if ch_data:
                chapters.append(ChapterData(
                    chapter_num=ch_num,
                    title=ch_data.get("title", f"第{ch_num}章"),
                    content=ch_data.get("content", ""),
                    word_count=ch_data.get("word_count", 0),
                ))

        meta.total_words = sum(ch.word_count for ch in chapters)
        return self.export_all(meta, chapters)

    def _save_data(self):
        data = {
            "presets": {
                pid: {
                    "preset_id": p.preset_id,
                    "name": p.name,
                    "platforms": [pl.label for pl in p.platforms],
                    "output_dir": p.output_dir,
                    "include_cover": p.include_cover,
                    "include_toc": p.include_toc,
                    "split_by_volume": p.split_by_volume,
                    "encoding": p.encoding,
                    "custom_css": p.custom_css,
                    "created_at": p.created_at,
                    "last_used_at": p.last_used_at,
                }
                for pid, p in self.presets.items()
            },
            "export_history": [
                {
                    "record_id": r.record_id,
                    "preset_name": r.preset_name,
                    "platform": r.platform,
                    "output_path": r.output_path,
                    "chapter_count": r.chapter_count,
                    "total_words": r.total_words,
                    "file_size_bytes": r.file_size_bytes,
                    "duration_seconds": r.duration_seconds,
                    "success": r.success,
                    "error_message": r.error_message,
                    "exported_at": r.exported_at,
                }
                for r in self.export_history[-100:]
            ],
            "record_counter": self._record_counter,
            "preset_counter": self._preset_counter,
        }

        filepath = os.path.join(self.output_dir, "exporter_data.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _load_data(self):
        filepath = os.path.join(self.output_dir, "exporter_data.json")
        if not os.path.exists(filepath):
            return

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

            self._record_counter = data.get("record_counter", 0)
            self._preset_counter = data.get("preset_counter", 0)

            for pid, pd in data.get("presets", {}).items():
                platforms = []
                for pl_label in pd.get("platforms", []):
                    for ep in ExportPlatform:
                        if ep.label == pl_label:
                            platforms.append(ep)
                            break
                self.presets[pid] = ExportPreset(
                    preset_id=pd.get("preset_id", pid),
                    name=pd.get("name", ""),
                    platforms=platforms,
                    output_dir=pd.get("output_dir", ""),
                    include_cover=pd.get("include_cover", True),
                    include_toc=pd.get("include_toc", True),
                    split_by_volume=pd.get("split_by_volume", False),
                    encoding=pd.get("encoding", "utf-8"),
                    custom_css=pd.get("custom_css", ""),
                    created_at=pd.get("created_at", ""),
                    last_used_at=pd.get("last_used_at", ""),
                )

            for rd in data.get("export_history", []):
                self.export_history.append(ExportRecord(**rd))

        except (json.JSONDecodeError, KeyError, TypeError) as e:
            print(f"  ⚠️ 导出数据加载失败: {e}")


if __name__ == "__main__":
    print("=" * 60)
    print("📦 多平台格式化导出系统测试")
    print("=" * 60)

    exporter = PlatformExporter()

    meta = NovelMeta(
        title="星辰大帝",
        author="叶青云",
        genre="玄幻",
        sub_genre="东方玄幻",
        synopsis="一个被家族抛弃的废柴少年，意外获得星辰传承，从此踏上逆天改命的修炼之路。"
                 "在这个弱肉强食的世界，他誓要成为那至高无上的星辰大帝！",
        tags=["废柴逆袭", "热血", "升级流", "扮猪吃虎"],
        status="连载中",
        pen_name="云中客",
        copyright_info="© 2026 叶青云 版权所有",
    )

    chapters = [
        ChapterData(1, "星辰坠落", "叶青云站在悬崖边，望着远方渐渐西沉的落日。\n"
                   "他的手中握着一枚暗淡无光的玉佩，那是母亲留给他的唯一遗物。\n"
                   "三年前，他还是叶家的天才少年，如今却沦为了人人嘲笑的废物。",
                   156, 1, "废柴开局"),
        ChapterData(2, "意外传承", "就在叶青云准备放弃的那一刻，玉佩突然绽放出璀璨的星光。\n"
                   "一股磅礴的信息流涌入他的脑海——星辰大帝的传承！\n"
                   "原来，这枚玉佩中封印着上古星辰大帝的全部记忆和功法。",
                   203, 1, "废柴开局"),
        ChapterData(3, "初次打脸", "叶家演武场上，曾经嘲笑他的堂兄叶天龙正得意洋洋。\n"
                   "叶青云缓步走上擂台，嘴角勾起一抹冷笑。\n"
                   "三招之内，叶天龙被轰下擂台，全场哗然！",
                   312, 1, "废柴开局"),
        ChapterData(4, "踏上征程", "离开叶家后，叶青云踏上了前往青云宗的修炼之路。\n"
                   "一路上，他遇到了形形色色的人物，也经历了第一次真正的生死搏杀。\n"
                   "这个世界远比他想象的要残酷得多。",
                   278, 2, "初入宗门"),
        ChapterData(5, "宗门考核", "青云宗的入门考核异常严苛，千人报名，最终只收十人。\n"
                   "叶青云凭借星辰传承中的秘法，在考核中脱颖而出。\n"
                   "但他不知道的是，一场针对他的阴谋正在暗中酝酿。",
                   345, 2, "初入宗门"),
    ]

    print("\n【内置预设】")
    for pid, preset in exporter.presets.items():
        platforms_str = ", ".join(p.label for p in preset.platforms[:3])
        print(f"  {preset.name}: {platforms_str}...")

    print("\n【字数统计】")
    stats = exporter.compute_word_stats(chapters)
    print(f"  总章节: {stats.total_chapters}")
    print(f"  总字数: {stats.total_words:,}")
    print(f"  均章字数: {stats.avg_words_per_chapter:,.0f}")
    print(f"  最短章: 第{stats.min_words_chapter[0]}章 ({stats.min_words_chapter[1]:,}字)")
    print(f"  最长章: 第{stats.max_words_chapter[0]}章 ({stats.max_words_chapter[1]:,}字)")
    print(f"  分卷字数: {stats.words_by_volume}")

    print("\n【导出测试】")
    for platform in [ExportPlatform.QIDIAN, ExportPlatform.FANQIE, ExportPlatform.HTML]:
        path = exporter.export(meta, chapters, platform)
        print(f"  {platform.label}: {path}")

    print("\n【封面生成】")
    cover_path = exporter.generate_cover_html(meta, chapters)
    print(f"  封面: {cover_path}")

    print("\n【目录生成】")
    toc_path = exporter.generate_toc_html(meta, chapters)
    print(f"  目录: {toc_path}")

    print("\n【导出验证】")
    for platform in [ExportPlatform.QIDIAN, ExportPlatform.HTML]:
        path = exporter.export(meta, chapters, platform)
        validation = exporter.validate_export(path, platform)
        status = "✅" if not validation["errors"] else "❌"
        print(f"  {status} {platform.label}: {len(validation['errors'])}个错误, {len(validation['warnings'])}个警告")

    print("\n【预设导出】")
    result = exporter.export_with_preset("PRESET_0002", meta, chapters)
    for platform, path in result.items():
        print(f"  {platform}: {path}")

    print("\n【导出历史】")
    for record in exporter.get_export_history(5):
        status = "✅" if record.success else "❌"
        print(f"  {status} {record.platform}: {record.chapter_count}章 {record.total_words:,}字")

    print("\n✅ 导出系统测试完成")
