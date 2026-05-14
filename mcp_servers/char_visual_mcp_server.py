#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS-v7 Character Visual MCP Server
角色造型师 — 管理角色视觉设定，确保跨媒介一致性
"""

import json
import os
from typing import Dict, List
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

DB_DIR = os.environ.get("NWACS_VISUAL_DIR", "nwacs-data/visual/characters")

def _ensure_dir():
    os.makedirs(DB_DIR, exist_ok=True)

def _char_path(char_id: str) -> str:
    return os.path.join(DB_DIR, f"{char_id}.json")

app = Server("nwacs-char-visual-mcp")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="create_character_visual",
            description="创建角色视觉设定档案",
            inputSchema={
                "type": "object",
                "properties": {
                    "char_id": {"type": "string", "description": "角色唯一标识"},
                    "char_name": {"type": "string"},
                    "age_appearance": {"type": "string", "description": "外观年龄"},
                    "gender": {"type": "string", "enum": ["男","女","无","其他"]},
                    "height": {"type": "string"},
                    "body_type": {"type": "string", "enum": ["纤瘦","标准","健壮","魁梧","娇小"]},
                    "hair_color": {"type": "string"},
                    "hair_style": {"type": "string"},
                    "eye_color": {"type": "string"},
                    "skin_tone": {"type": "string"},
                    "facial_features": {"type": "array", "items": {"type": "string"}, "description": "面部特征标签"},
                    "outfit_default": {"type": "string", "description": "默认服装描述"},
                    "outfit_variants": {"type": "array", "items": {"type": "string"}, "description": "变装（战斗/礼服/伪装等）"},
                    "prop_signature": {"type": "string", "description": "标志性道具"},
                    "color_theme": {"type": "string", "description": "角色主题色（HEX或描述）"},
                    "expression_keywords": {"type": "array", "items": {"type": "string"}, "description": "常用表情关键词"},
                    "silhouette_feature": {"type": "string", "description": "剪影识别特征（如：长马尾、独臂、高帽）"},
                    "sd_prompt_template": {"type": "string", "description": "Stable Diffusion 提示词模板"},
                    "reference_images": {"type": "array", "items": {"type": "string"}, "description": "参考图URL或路径"}
                },
                "required": ["char_id", "char_name", "gender", "hair_color", "eye_color", "outfit_default"]
            }
        ),
        Tool(
            name="get_character_visual",
            description="获取角色视觉设定",
            inputSchema={
                "type": "object",
                "properties": {
                    "char_id": {"type": "string"}
                },
                "required": ["char_id"]
            }
        ),
        Tool(
            name="check_visual_consistency",
            description="检查文本描述是否与视觉设定冲突",
            inputSchema={
                "type": "object",
                "properties": {
                    "char_id": {"type": "string"},
                    "text_description": {"type": "string", "description": "小说中的角色外貌描写段落"}
                },
                "required": ["char_id", "text_description"]
            }
        ),
        Tool(
            name="list_all_characters",
            description="列出所有角色视觉档案",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="generate_sd_prompt",
            description="为指定角色+场景生成 Stable Diffusion 提示词",
            inputSchema={
                "type": "object",
                "properties": {
                    "char_id": {"type": "string"},
                    "scene_desc": {"type": "string", "description": "场景描述"},
                    "emotion": {"type": "string", "description": "当前情绪"},
                    "shot_type": {"type": "string", "enum": ["特写","近景","中景","全景"], "default": "中景"}
                },
                "required": ["char_id", "scene_desc"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    _ensure_dir()

    if name == "create_character_visual":
        data = {k: v for k, v in arguments.items()}
        data["updated_at"] = __import__("datetime").datetime.utcnow().isoformat()
        path = _char_path(arguments["char_id"])
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return [TextContent(type="text", text=f"✅ 角色视觉档案已创建: {arguments['char_name']} ({arguments['char_id']})")]

    elif name == "get_character_visual":
        path = _char_path(arguments["char_id"])
        if not os.path.exists(path):
            return [TextContent(type="text", text=f"❌ 角色 {arguments['char_id']} 视觉档案不存在")]
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [TextContent(type="text", text=json.dumps(data, ensure_ascii=False, indent=2))]

    elif name == "check_visual_consistency":
        path = _char_path(arguments["char_id"])
        if not os.path.exists(path):
            return [TextContent(type="text", text=f"❌ 角色档案不存在")]
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        text = arguments["text_description"]
        conflicts = []
        checks = [
            (data.get("hair_color", ""), ["黑发","白发","红发","金发","蓝发","紫发","绿发","棕发","银发"]),
            (data.get("eye_color", ""), ["黑瞳","红瞳","蓝瞳","金瞳","绿瞳","紫瞳"]),
            (data.get("outfit_default", ""), ["西装","古装","校服","铠甲","道袍","和服","皮衣"]),
        ]
        for attr_val, keywords in checks:
            for kw in keywords:
                if kw in text and kw not in attr_val and attr_val:
                    conflicts.append(f"冲突: 文本提到'{kw}'，但档案设定为'{attr_val}'")

        if conflicts:
            return [TextContent(type="text", text="⚠️ 发现视觉冲突:\n" + "\n".join(conflicts))]
        return [TextContent(type="text", text="✅ 视觉一致性检查通过")]

    elif name == "list_all_characters":
        chars = []
        for f in os.listdir(DB_DIR):
            if f.endswith(".json"):
                with open(os.path.join(DB_DIR, f), "r", encoding="utf-8") as fp:
                    d = json.load(fp)
                    chars.append(f"{d['char_id']}: {d['char_name']} ({d.get('gender','?')}, {d.get('hair_color','?')})")
        return [TextContent(type="text", text="\n".join(chars) if chars else "暂无角色")]

    elif name == "generate_sd_prompt":
        path = _char_path(arguments["char_id"])
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        template = data.get("sd_prompt_template", "")
        if not template:
            template = f"1boy, {data['hair_color']} hair, {data['eye_color']} eyes, {data['outfit_default']}, best quality"

        scene = arguments["scene_desc"]
        emotion = arguments.get("emotion", "neutral")
        shot = arguments.get("shot_type", "中景")

        shot_prompt = {"特写": "close-up portrait", "近景": "upper body", "中景": "medium shot", "全景": "full body"}.get(shot, "medium shot")

        prompt = f"{template}, {shot_prompt}, {scene}, {emotion} expression, cinematic lighting, highly detailed"
        negative = "lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality"

        return [TextContent(type="text", text=f"【正向提示词】\n{prompt}\n\n【反向提示词】\n{negative}")]

    return [TextContent(type="text", text="未知工具")]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
