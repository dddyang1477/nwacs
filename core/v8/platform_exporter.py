#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 多平台格式化导出系统 - PlatformExporter

对标百度作家平台，核心能力：
1. 起点中文网格式导出
2. 番茄小说格式导出
3. 纵横中文网格式导出
4. 通用TXT/Markdown/HTML/EPUB导出
5. 章节自动分卷
6. 封面信息嵌入
"""

import json
import os
import re
import zipfile
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class ExportPlatform(Enum):
    QIDIAN = ("起点中文网", "qidian", "utf-8")
    FANQIE = ("番茄小说", "fanqie", "utf-8")
    ZONGHENG = ("纵横中文网", "zongheng", "utf-8")
    TXT = ("通用TXT", "txt", "utf-8")
    MARKDOWN = ("Markdown", "md", "utf-8")
    HTML = ("HTML网页", "html", "utf-8")
    EPUB = ("EPUB电子书", "epub", "utf-8")

    def __init__(self, label: str, ext: str, encoding: str):
        self.label = label
        self.ext = ext
        self.encoding = encoding


@dataclass
class ChapterData:
    chapter_num: int
    title: str
    content: str
    word_count: int
    volume: int = 1


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


class PlatformExporter:
    """多平台格式化导出"""

    def __init__(self, output_dir: str = None):
        if output_dir is None:
            output_dir = os.path.join(os.path.dirname(__file__), "..", "exports")
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def export(self, meta: NovelMeta, chapters: List[ChapterData],
               platform: ExportPlatform) -> str:
        """导出到指定平台格式"""
        method_map = {
            ExportPlatform.QIDIAN: self._export_qidian,
            ExportPlatform.FANQIE: self._export_fanqie,
            ExportPlatform.ZONGHENG: self._export_zongheng,
            ExportPlatform.TXT: self._export_txt,
            ExportPlatform.MARKDOWN: self._export_markdown,
            ExportPlatform.HTML: self._export_html,
            ExportPlatform.EPUB: self._export_epub,
        }
        exporter = method_map.get(platform, self._export_txt)
        return exporter(meta, chapters)

    def export_all(self, meta: NovelMeta, chapters: List[ChapterData]) -> Dict[str, str]:
        """导出所有格式"""
        results = {}
        for platform in ExportPlatform:
            try:
                path = self.export(meta, chapters, platform)
                results[platform.label] = path
            except Exception as e:
                results[platform.label] = f"导出失败: {e}"
        return results

    def _safe_filename(self, name: str) -> str:
        return re.sub(r'[<>:"/\\|?*]', '_', name)

    def _get_output_path(self, meta: NovelMeta, platform: ExportPlatform,
                         subdir: str = "") -> str:
        safe_title = self._safe_filename(meta.title)
        dir_path = self.output_dir
        if subdir:
            dir_path = os.path.join(dir_path, subdir)
        os.makedirs(dir_path, exist_ok=True)
        return os.path.join(dir_path, f"{safe_title}.{platform.ext}")

    def _format_chapter_content(self, chapter: ChapterData,
                                platform: ExportPlatform) -> str:
        """格式化章节内容"""
        lines = []
        lines.append(f"第{chapter.chapter_num}章 {chapter.title}")
        lines.append("")
        lines.append(chapter.content.strip())
        lines.append("")
        return "\n".join(lines)

    def _export_qidian(self, meta: NovelMeta, chapters: List[ChapterData]) -> str:
        """起点中文网格式"""
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
                lines.append(f"\n第{current_volume}卷\n")
            lines.append(self._format_chapter_content(ch, ExportPlatform.QIDIAN))
            lines.append("-" * 30)

        content = "\n".join(lines)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        return output_path

    def _export_fanqie(self, meta: NovelMeta, chapters: List[ChapterData]) -> str:
        """番茄小说格式"""
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
        """纵横中文网格式"""
        output_path = self._get_output_path(meta, ExportPlatform.ZONGHENG, "zongheng")
        lines = []

        lines.append(f"《{meta.title}》")
        lines.append(f"作者：{meta.author}")
        lines.append(f"类别：{meta.genre} | 状态：连载中")
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

    def _export_txt(self, meta: NovelMeta, chapters: List[ChapterData]) -> str:
        """通用TXT格式"""
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
        """Markdown格式"""
        output_path = self._get_output_path(meta, ExportPlatform.MARKDOWN, "md")
        lines = []

        lines.append(f"# {meta.title}")
        lines.append("")
        lines.append(f"**作者**: {meta.author}")
        lines.append(f"**类型**: {meta.genre}")
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
        """HTML网页格式"""
        output_path = self._get_output_path(meta, ExportPlatform.HTML, "html")
        lines = []

        lines.append("<!DOCTYPE html>")
        lines.append('<html lang="zh-CN">')
        lines.append("<head>")
        lines.append('<meta charset="UTF-8">')
        lines.append(f"<title>{meta.title} - {meta.author}</title>")
        lines.append("<style>")
        lines.append("""
            body { max-width: 800px; margin: 0 auto; padding: 20px;
                   font-family: 'Microsoft YaHei', sans-serif; line-height: 1.8; }
            h1 { text-align: center; color: #333; }
            .meta { text-align: center; color: #666; margin-bottom: 30px; }
            .synopsis { background: #f5f5f5; padding: 15px; border-radius: 8px;
                        margin-bottom: 30px; font-style: italic; }
            .toc { background: #fafafa; padding: 15px; border-radius: 8px; margin-bottom: 30px; }
            .toc a { color: #1f77b4; text-decoration: none; }
            .chapter { margin-bottom: 40px; }
            .chapter h2 { border-bottom: 2px solid #1f77b4; padding-bottom: 10px; }
            .chapter-content { text-indent: 2em; }
        """)
        lines.append("</style>")
        lines.append("</head>")
        lines.append("<body>")
        lines.append(f"<h1>{meta.title}</h1>")
        lines.append(f'<div class="meta">作者：{meta.author} | 类型：{meta.genre}</div>')
        lines.append(f'<div class="synopsis">{meta.synopsis}</div>')

        lines.append('<div class="toc"><h3>目录</h3><ul>')
        for ch in sorted(chapters, key=lambda c: c.chapter_num):
            lines.append(f'<li><a href="#ch{ch.chapter_num}">第{ch.chapter_num}章 {ch.title}</a></li>')
        lines.append("</ul></div>")

        for ch in sorted(chapters, key=lambda c: c.chapter_num):
            lines.append(f'<div class="chapter" id="ch{ch.chapter_num}">')
            lines.append(f"<h2>第{ch.chapter_num}章 {ch.title}</h2>")
            lines.append(f'<div class="chapter-content">')
            for paragraph in ch.content.strip().split("\n"):
                if paragraph.strip():
                    lines.append(f"<p>{paragraph.strip()}</p>")
            lines.append("</div></div>")

        lines.append("</body></html>")

        content = "\n".join(lines)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        return output_path

    def _export_epub(self, meta: NovelMeta, chapters: List[ChapterData]) -> str:
        """EPUB电子书格式（简化版）"""
        output_path = self._get_output_path(meta, ExportPlatform.EPUB, "epub")

        container_xml = """<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>"""

        sorted_chapters = sorted(chapters, key=lambda c: c.chapter_num)

        manifest_items = []
        spine_items = []
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

        with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("mimetype", "application/epub+zip")
            zf.writestr("META-INF/container.xml", container_xml)
            zf.writestr("content.opf", content_opf)
            zf.writestr("toc.ncx", toc_ncx)

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

    def batch_export_from_memory(self, memory_manager, meta: NovelMeta) -> Dict[str, str]:
        """从NovelMemoryManager批量导出"""
        chapters = []
        for ch_num in range(1, memory_manager.current_chapter + 1):
            ch_data = memory_manager.get_chapter(ch_num)
            if ch_data:
                chapters.append(ChapterData(
                    chapter_num=ch_num,
                    title=ch_data.get("title", f"第{ch_num}章"),
                    content=ch_data.get("content", ""),
                    word_count=ch_data.get("word_count", 0),
                ))

        meta.total_words = sum(ch.word_count for ch in chapters)
        return self.export_all(meta, chapters)
