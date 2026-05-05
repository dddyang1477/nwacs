#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS-v7 Drama Export MCP Server
出版衍生师 — 导出剪映/PR/漫画工程文件
"""

import json
import os
import csv
from typing import List, Dict
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

EXPORT_DIR = os.environ.get("NWACS_EXPORT_DIR", "nwacs-data/drama/export")

def _ensure_dir():
    os.makedirs(EXPORT_DIR, exist_ok=True)

app = Server("nwacs-drama-export-mcp")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="export_jianying_json",
            description="导出剪映专业版可导入的 JSON 草稿",
            inputSchema={
                "type": "object",
                "properties": {
                    "episode_no": {"type": "integer"},
                    "panels": {"type": "array", "description": "分镜表数据"},
                    "output_name": {"type": "string"}
                },
                "required": ["episode_no", "panels"]
            }
        ),
        Tool(
            name="export_voice_script",
            description="导出配音台本（按角色分组，含情绪标注）",
            inputSchema={
                "type": "object",
                "properties": {
                    "episode_no": {"type": "integer"},
                    "panels": {"type": "array"},
                    "output_name": {"type": "string"}
                },
                "required": ["episode_no", "panels"]
            }
        ),
        Tool(
            name="export_comic_script",
            description="导出漫画脚本（页码/格子/台词/效果线）",
            inputSchema={
                "type": "object",
                "properties": {
                    "episode_no": {"type": "integer"},
                    "panels": {"type": "array"},
                    "page_layout": {"type": "string", "enum": ["条漫","页漫(4格)","页漫(6格)","自由"], "default": "条漫"}
                },
                "required": ["episode_no", "panels"]
            }
        ),
        Tool(
            name="export_epub_meta",
            description="导出 EPUB 元数据与目录结构",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "author": {"type": "string"},
                    "chapters": {"type": "array", "items": {"type": "string"}},
                    "cover_prompt": {"type": "string", "description": "封面图SD提示词"}
                },
                "required": ["title", "author", "chapters"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    _ensure_dir()

    if name == "export_jianying_json":
        panels = arguments["panels"]
        ep = arguments["episode_no"]
        out = arguments.get("output_name", f"jianying_ep{ep:03d}")

        # 剪映 JSON 简化结构（实际需按剪映 schema 调整）
        tracks = []
        for i, p in enumerate(panels):
            tracks.append({
                "id": p["panel_id"],
                "type": "video",
                "text": p.get("narration", "") or " ".join(p.get("dialogues", [])),
                "duration": int(p["duration"] * 1000000),  # 微秒
                "shot": p["shot_type"],
                "camera": p.get("camera_move", ""),
                "transition": p.get("transition", "硬切")
            })

        jianying_data = {
            "version": "v7.0",
            "project": {"name": out, "duration": sum(t["duration"] for t in tracks)},
            "tracks": [{"type": "video", "segments": tracks}]
        }

        path = os.path.join(EXPORT_DIR, f"{out}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(jianying_data, f, ensure_ascii=False, indent=2)
        return [TextContent(type="text", text=f"✅ 剪映工程已导出: {path}\n总时长: {sum(t['duration'] for t in tracks)/1000000:.1f}秒")]

    elif name == "export_voice_script":
        panels = arguments["panels"]
        ep = arguments["episode_no"]
        out = arguments.get("output_name", f"voice_ep{ep:03d}")

        lines = [f"# 配音台本 — 第{ep}集", "="*50, ""]
        for p in panels:
            lines.append(f"【{p['panel_id']}】{p['shot_type']} | 时长:{p['duration']}s")
            for d in p.get("dialogues", []):
                # 简单角色推断
                role = "旁白"
                if "：" in d:
                    role, d = d.split("：", 1)
                lines.append(f"  [{role}] {d}")
            if p.get("narration"):
                lines.append(f"  [旁白] {p['narration']}")
            if p.get("audio_notes"):
                lines.append(f"  [音效/BGM] {p['audio_notes']}")
            lines.append("")

        path = os.path.join(EXPORT_DIR, f"{out}.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        return [TextContent(type="text", text=f"✅ 配音台本已导出: {path}")]

    elif name == "export_comic_script":
        panels = arguments["panels"]
        ep = arguments["episode_no"]
        layout = arguments.get("page_layout", "条漫")

        pages = []
        if layout == "条漫":
            panels_per_page = 4
        elif layout == "页漫(4格)":
            panels_per_page = 4
        elif layout == "页漫(6格)":
            panels_per_page = 6
        else:
            panels_per_page = 4

        for i in range(0, len(panels), panels_per_page):
            page_panels = panels[i:i+panels_per_page]
            page = {
                "page_no": i//panels_per_page + 1,
                "layout": layout,
                "panels": []
            }
            for j, p in enumerate(page_panels):
                page["panels"].append({
                    "panel_no": j+1,
                    "shot": p["shot_type"],
                    "content": p.get("narration", "") or " ".join(p.get("dialogues", [])),
                    "dialogues": p.get("dialogues", []),
                    "sfx": p.get("audio_notes", ""),
                    "effect_lines": [a for a in p.get("actions", [])],  # 效果线提示
                    "camera": p.get("camera_move", "")
                })
            pages.append(page)

        path = os.path.join(EXPORT_DIR, f"comic_script_ep{ep:03d}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"episode": ep, "layout": layout, "pages": pages}, f, ensure_ascii=False, indent=2)
        return [TextContent(type="text", text=f"✅ 漫画脚本已导出: {path} | 共{len(pages)}页")]

    elif name == "export_epub_meta":
        meta = {
            "title": arguments["title"],
            "author": arguments["author"],
            "chapters": [{"id": f"ch{i+1:03d}", "title": t} for i, t in enumerate(arguments["chapters"])],
            "cover_prompt": arguments.get("cover_prompt", ""),
            "generated_at": __import__("datetime").datetime.utcnow().isoformat()
        }
        path = os.path.join(EXPORT_DIR, "epub_meta.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)
        return [TextContent(type="text", text=f"✅ EPUB 元数据已导出: {path}")]

    return [TextContent(type="text", text="未知工具")]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
