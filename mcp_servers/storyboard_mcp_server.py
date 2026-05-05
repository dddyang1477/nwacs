#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS-v7 Storyboard MCP Server
分镜构造师 — 将小说段落转化为漫剧分镜表
"""

import json
import re
import os
from typing import List, Dict
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

app = Server("nwacs-storyboard-mcp")

def parse_dramatic_marks(text: str) -> List[Dict]:
    """解析小说中的漫剧标记"""
    marks = []
    # 匹配 [[TYPE:content,param]]
    pattern = r"\[\[(\w+):(.*?)(?:,(.*?))?\]\]"
    for m in re.finditer(pattern, text):
        marks.append({
            "type": m.group(1),
            "content": m.group(2).strip(),
            "param": m.group(3).strip() if m.group(3) else "",
            "pos": m.start()
        })
    return marks

def text_to_panels(text: str, episode_no: int) -> List[Dict]:
    """将小说正文自动切分为分镜"""
    panels = []
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    panel_id = 1

    for para in paragraphs:
        marks = parse_dramatic_marks(para)
        clean_text = re.sub(r"\[\[.*?\]\]", "", para).strip()

        # 自动判断景别
        if len(clean_text) < 20:
            shot = "特写(CU)"
            duration = 2.0
        elif len(clean_text) < 80:
            shot = "近景(MCU)"
            duration = 3.5
        elif "全景" in clean_text or "整个" in clean_text:
            shot = "全景(WS)"
            duration = 4.0
        else:
            shot = "中景(MS)"
            duration = 3.0

        # 提取对话
        dialogues = re.findall(r'["""](.*?)["""]', clean_text)

        # 提取动作
        actions = []
        action_keywords = ["转身", "抬头", "握拳", "拔剑", "跪下", "后退", "冲", "跑", "跳", "挥"]
        for kw in action_keywords:
            if kw in clean_text:
                actions.append(kw)

        panel = {
            "episode": episode_no,
            "panel_id": f"EP{episode_no:03d}_P{panel_id:03d}",
            "shot_type": shot,
            "duration": duration,
            "narration": clean_text if not dialogues else "",
            "dialogues": dialogues,
            "actions": actions,
            "dramatic_marks": marks,
            "camera_move": "",
            "transition": "硬切",
            "visual_notes": "",
            "audio_notes": ""
        }

        # 处理显式标记
        for m in marks:
            if m["type"] == "CAM":
                panel["camera_move"] = m["content"]
            elif m["type"] == "SFX":
                panel["audio_notes"] += f"音效:{m['content']}({m['param']});"
            elif m["type"] == "BGM":
                panel["audio_notes"] += f"BGM:{m['content']}({m['param']});"
            elif m["type"] == "PANEL":
                panel["shot_type"] = m["content"]
                if m["param"]:
                    try:
                        panel["duration"] = float(m["param"].replace("s",""))
                    except:
                        pass
            elif m["type"] == "TRANS":
                panel["transition"] = m["content"]

        panels.append(panel)
        panel_id += 1

    return panels

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="generate_storyboard",
            description="将小说正文转换为漫剧分镜表(JSON)",
            inputSchema={
                "type": "object",
                "properties": {
                    "episode_no": {"type": "integer"},
                    "novel_text": {"type": "string", "description": "带漫剧标记的小说正文"},
                    "style": {"type": "string", "enum": ["条漫","页漫","动态漫","短剧"], "default": "动态漫"}
                },
                "required": ["episode_no", "novel_text"]
            }
        ),
        Tool(
            name="export_storyboard_json",
            description="导出标准分镜JSON文件",
            inputSchema={
                "type": "object",
                "properties": {
                    "panels": {"type": "array"},
                    "output_path": {"type": "string"}
                },
                "required": ["panels", "output_path"]
            }
        ),
        Tool(
            name="analyze_pacing",
            description="分析分镜节奏，输出情绪曲线与时长建议",
            inputSchema={
                "type": "object",
                "properties": {
                    "panels": {"type": "array"}
                },
                "required": ["panels"]
            }
        ),
        Tool(
            name="auto_dramatic_marks",
            description="为纯文本小说自动插入漫剧标记建议",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string"},
                    "intensity": {"type": "string", "enum": ["低","中","高"], "default": "中"}
                },
                "required": ["text"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "generate_storyboard":
        panels = text_to_panels(arguments["novel_text"], arguments["episode_no"])
        style = arguments.get("style", "动态漫")
        # 根据风格调整
        if style == "条漫":
            for p in panels:
                p["layout"] = "竖屏"
                p["duration"] = min(p["duration"], 2.5)
        elif style == "短剧":
            for p in panels:
                p["duration"] = max(p["duration"], 3.0)
        return [TextContent(type="text", text=json.dumps({"style": style, "panel_count": len(panels), "panels": panels}, ensure_ascii=False, indent=2))]

    elif name == "export_storyboard_json":
        path = arguments["output_path"]
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(arguments["panels"], f, ensure_ascii=False, indent=2)
        return [TextContent(type="text", text=f"✅ 分镜表已导出: {path}")]

    elif name == "analyze_pacing":
        panels = arguments["panels"]
        total_duration = sum(p["duration"] for p in panels)
        dialog_density = sum(len(p["dialogues"]) for p in panels) / max(len(panels), 1)
        action_density = sum(len(p["actions"]) for p in panels) / max(len(panels), 1)

        # 简单情绪曲线
        curve = []
        for i, p in enumerate(panels):
            score = 50
            if p["actions"]: score += 20
            if p["dialogues"]: score += 10
            if "特写" in p["shot_type"]: score += 15
            if p["camera_move"]: score += 10
            curve.append({"panel": i+1, "intensity": min(score, 100)})

        report = {
            "total_duration_sec": round(total_duration, 1),
            "total_duration_min": round(total_duration/60, 2),
            "panel_count": len(panels),
            "avg_dialog_per_panel": round(dialog_density, 2),
            "avg_action_per_panel": round(action_density, 2),
            "pacing_suggestion": "节奏偏快" if total_duration < 120 else "节奏适中" if total_duration < 300 else "节奏偏慢，建议删减",
            "intensity_curve": curve
        }
        return [TextContent(type="text", text=json.dumps(report, ensure_ascii=False, indent=2))]

    elif name == "auto_dramatic_marks":
        text = arguments["text"]
        intensity = arguments.get("intensity", "中")

        # 自动标记规则
        markers = []
        lines = text.split("\n")
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            # 对话自动标记
            if '"' in line or '"' in line:
                if "说" in line or "道" in line:
                    markers.append(f"第{i+1}行: 建议插入 [[PANEL:近景,2.5s]] 对话特写")
            # 动作自动标记
            action_words = ["突然", "猛地", "瞬间", "轰", "砰", "拔剑", "转身", "冲"]
            if any(w in line for w in action_words):
                markers.append(f"第{i+1}行: 建议插入 [[CAM:快速推拉]] + [[SFX:强音效,瞬时]]")
            # 情绪高潮
            emotion_words = ["死", "杀", "爱", "恨", "泪", "血", "绝望", "希望"]
            if any(w in line for w in emotion_words) and intensity == "高":
                markers.append(f"第{i+1}行: 建议插入 [[PANEL:特写,3s]] + [[BGM:情绪高潮,弦乐]]")

        return [TextContent(type="text", text="\n".join(markers) if markers else "未检测到强烈戏剧点，建议保持当前叙事节奏")]

    return [TextContent(type="text", text="未知工具")]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
