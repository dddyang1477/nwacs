#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS-Feishu MCP Server
飞书/微信 消息推送 — MCP 工具层
依赖: pip install mcp requests
环境变量: FEISHU_WEBHOOK_URL
"""

import os
import json
import requests
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

FEISHU_WEBHOOK = os.environ.get("FEISHU_WEBHOOK_URL", "")
WECHAT_WEBHOOK = os.environ.get("WECHAT_WEBHOOK_URL", "")

app = Server("nwacs-feishu-mcp")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="push_feishu_text",
            description="推送纯文本消息到飞书群机器人",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "消息标题"},
                    "content": {"type": "string", "description": "正文内容"},
                    "at_all": {"type": "boolean", "default": False}
                },
                "required": ["title", "content"]
            }
        ),
        Tool(
            name="push_feishu_rich",
            description="推送富文本卡片到飞书（含章节完成进度、伏笔状态等）",
            inputSchema={
                "type": "object",
                "properties": {
                    "chapter_no": {"type": "integer"},
                    "chapter_title": {"type": "string"},
                    "word_count": {"type": "integer"},
                    "status": {"type": "string", "enum": ["生成中", "审核中", "已完成", "已发布"]},
                    "foreshadow_count": {"type": "integer"},
                    "quality_score": {"type": "number", "description": "质量评分 0-100"},
                    "ai_score": {"type": "number", "description": "去AI化评分 0-100"},
                    "notes": {"type": "string"}
                },
                "required": ["chapter_no", "chapter_title", "status"]
            }
        ),
        Tool(
            name="push_wechat_text",
            description="推送文本到企业微信机器人（如配置了 WECHAT_WEBHOOK_URL）",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {"type": "string"}
                },
                "required": ["content"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "push_feishu_text":
        if not FEISHU_WEBHOOK:
            return [TextContent(type="text", text="❌ FEISHU_WEBHOOK_URL 未配置")]
        payload = {
            "msg_type": "text",
            "content": {"text": f"【{arguments['title']}】\n{arguments['content']}"}
        }
        if arguments.get("at_all"):
            payload["content"]["text"] += "\n<at user_id=\"all\">所有人</at>"
        try:
            r = requests.post(FEISHU_WEBHOOK, json=payload, timeout=10)
            return [TextContent(type="text", text=f"✅ 飞书推送成功: {r.status_code}")]
        except Exception as e:
            return [TextContent(type="text", text=f"❌ 推送失败: {e}")]

    elif name == "push_feishu_rich":
        if not FEISHU_WEBHOOK:
            return [TextContent(type="text", text="❌ FEISHU_WEBHOOK_URL 未配置")]
        elements = [
            [{"tag": "div", "text": {"tag": "lark_md", "content": f"**章节:** 第{arguments['chapter_no']}章 {arguments['chapter_title']}"}}],
            [{"tag": "div", "text": {"tag": "lark_md", "content": f"**状态:** {arguments['status']}"}}]
        ]
        if "word_count" in arguments:
            elements.append([{"tag": "div", "text": {"tag": "lark_md", "content": f"**字数:** {arguments['word_count']}"}}])
        if "quality_score" in arguments:
            elements.append([{"tag": "div", "text": {"tag": "lark_md", "content": f"**质量分:** {arguments['quality_score']}/100 | **去AI分:** {arguments.get('ai_score', 'N/A')}/100"}}])
        if "notes" in arguments:
            elements.append([{"tag": "div", "text": {"tag": "lark_md", "content": f"**备注:** {arguments['notes']}"}}])

        payload = {
            "msg_type": "interactive",
            "card": {
                "header": {"title": {"tag": "plain_text", "content": "📚 NWACS 创作进度"}, "template": "blue"},
                "elements": [item for sublist in elements for item in sublist]
            }
        }
        try:
            r = requests.post(FEISHU_WEBHOOK, json=payload, timeout=10)
            return [TextContent(type="text", text=f"✅ 飞书卡片推送成功: {r.status_code}")]
        except Exception as e:
            return [TextContent(type="text", text=f"❌ 推送失败: {e}")]

    elif name == "push_wechat_text":
        if not WECHAT_WEBHOOK:
            return [TextContent(type="text", text="❌ WECHAT_WEBHOOK_URL 未配置")]
        payload = {"msgtype": "text", "text": {"content": arguments["content"]}}
        try:
            r = requests.post(WECHAT_WEBHOOK, json=payload, timeout=10)
            return [TextContent(type="text", text=f"✅ 微信推送成功: {r.status_code}")]
        except Exception as e:
            return [TextContent(type="text", text=f"❌ 推送失败: {e}")]

    return [TextContent(type="text", text="未知工具")]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
