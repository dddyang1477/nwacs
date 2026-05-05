#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS-Foreshadow MCP Server
伏笔与档案管理师 — MCP 工具层
依赖: pip install mcp
"""

import json
import sqlite3
import os
from datetime import datetime
from typing import Optional

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

DB_PATH = os.environ.get("NWACS_DB_PATH", "nwacs-data/foreshadow_db.sqlite3")

def _ensure_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS foreshadows (
            foreshadow_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            type TEXT CHECK(type IN ('主线','支线','人物','世界观','情感')),
            priority INTEGER CHECK(priority BETWEEN 1 AND 5),
            chapter_created INTEGER,
            scene_created TEXT,
            content_snippet TEXT,
            clue_vector TEXT,
            status TEXT CHECK(status IN ('埋设','发展中','待回收','已回收','废弃')),
            chapter_expected INTEGER,
            chapter_actual INTEGER,
            development_log TEXT,
            dependencies TEXT,
            related_chars TEXT,
            related_plots TEXT,
            subtlety_score REAL,
            payoff_strength REAL,
            author_note TEXT,
            created_at TEXT,
            updated_at TEXT
        )
    """)
    conn.commit()
    conn.close()

app = Server("nwacs-foreshadow-mcp")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="create_foreshadow",
            description="创建新伏笔。返回 foreshadow_id。",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "伏笔标题"},
                    "type": {"type": "string", "enum": ["主线","支线","人物","世界观","情感"]},
                    "priority": {"type": "integer", "minimum": 1, "maximum": 5},
                    "chapter_created": {"type": "integer"},
                    "scene_created": {"type": "string"},
                    "content_snippet": {"type": "string", "description": "原文片段"},
                    "clue_vector": {"type": "array", "items": {"type": "string"}, "description": "语义关键词列表"},
                    "chapter_expected": {"type": "integer", "description": "预计回收章节"},
                    "related_chars": {"type": "array", "items": {"type": "string"}},
                    "related_plots": {"type": "array", "items": {"type": "string"}},
                    "subtlety_score": {"type": "number", "minimum": 1, "maximum": 10},
                    "payoff_strength": {"type": "number", "minimum": 1, "maximum": 10},
                    "author_note": {"type": "string"}
                },
                "required": ["title", "type", "priority", "chapter_created", "content_snippet", "chapter_expected"]
            }
        ),
        Tool(
            name="get_active_foreshadows",
            description="查询当前活跃伏笔（待回收/发展中）。",
            inputSchema={
                "type": "object",
                "properties": {
                    "chapter": {"type": "integer", "description": "当前章节号"},
                    "status_filter": {"type": "array", "items": {"type": "string"}, "description": "状态过滤，默认['发展中','待回收']"}
                },
                "required": ["chapter"]
            }
        ),
        Tool(
            name="update_foreshadow_status",
            description="更新伏笔状态（状态机转换）。",
            inputSchema={
                "type": "object",
                "properties": {
                    "foreshadow_id": {"type": "string"},
                    "status": {"type": "string", "enum": ["埋设","发展中","待回收","已回收","废弃"]},
                    "chapter_actual": {"type": "integer"},
                    "event_note": {"type": "string", "description": "发展日志备注"}
                },
                "required": ["foreshadow_id", "status"]
            }
        ),
        Tool(
            name="get_foreshadow_detail",
            description="获取单个伏笔详情。",
            inputSchema={
                "type": "object",
                "properties": {
                    "foreshadow_id": {"type": "string"}
                },
                "required": ["foreshadow_id"]
            }
        ),
        Tool(
            name="check_health_report",
            description="生成伏笔健康报告（烂尾风险/回收不彻底）。",
            inputSchema={
                "type": "object",
                "properties": {
                    "current_chapter": {"type": "integer"}
                },
                "required": ["current_chapter"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    _ensure_db()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    now = datetime.utcnow().isoformat()

    if name == "create_foreshadow":
        vol = arguments.get("chapter_created", 0)
        seq = conn.execute("SELECT COUNT(*) FROM foreshadows WHERE chapter_created=?", (vol,)).fetchone()[0] + 1
        fs_id = f"FS_{vol:03d}_{seq:03d}"
        clue_vec = json.dumps(arguments.get("clue_vector", []), ensure_ascii=False)
        deps = json.dumps({"blocks": [], "blocked_by": []}, ensure_ascii=False)
        rel_chars = json.dumps(arguments.get("related_chars", []), ensure_ascii=False)
        rel_plots = json.dumps(arguments.get("related_plots", []), ensure_ascii=False)
        dev_log = json.dumps([{"chapter": vol, "event": "埋设", "note": "首次创建"}], ensure_ascii=False)
        conn.execute("""
            INSERT INTO foreshadows VALUES (
                :id, :title, :type, :priority, :chapter_created, :scene_created,
                :content_snippet, :clue_vector, '埋设', :chapter_expected, NULL,
                :development_log, :dependencies, :related_chars, :related_plots,
                :subtlety_score, :payoff_strength, :author_note, :created_at, :updated_at
            )
        """, {
            "id": fs_id, "title": arguments["title"], "type": arguments["type"],
            "priority": arguments["priority"], "chapter_created": vol,
            "scene_created": arguments.get("scene_created", ""),
            "content_snippet": arguments["content_snippet"],
            "clue_vector": clue_vec, "chapter_expected": arguments["chapter_expected"],
            "development_log": dev_log, "dependencies": deps,
            "related_chars": rel_chars, "related_plots": rel_plots,
            "subtlety_score": arguments.get("subtlety_score", 5.0),
            "payoff_strength": arguments.get("payoff_strength", 5.0),
            "author_note": arguments.get("author_note", ""),
            "created_at": now, "updated_at": now
        })
        conn.commit()
        return [TextContent(type="text", text=f"✅ 伏笔已创建: {fs_id} | {arguments['title']}")]

    elif name == "get_active_foreshadows":
        chapter = arguments["chapter"]
        filters = arguments.get("status_filter", ["发展中", "待回收"])
        placeholders = ",".join(["?"]*len(filters))
        rows = conn.execute(
            f"SELECT foreshadow_id, title, status, priority, chapter_expected, content_snippet FROM foreshadows WHERE status IN ({placeholders}) ORDER BY priority, chapter_expected",
            tuple(filters)
        ).fetchall()
        alerts = []
        for r in rows:
            alert_level = "🔴" if r["status"] == "待回收" and r["chapter_expected"] <= chapter else "🟡"
            alerts.append(f"{alert_level} {r['foreshadow_id']} [{r['status']}] 《{r['title']}》 预计{r['chapter_expected']}章回收 | 优先级:{r['priority']}")
        return [TextContent(type="text", text="\n".join(alerts) if alerts else "✅ 当前无活跃伏笔")]

    elif name == "update_foreshadow_status":
        fs_id = arguments["foreshadow_id"]
        new_status = arguments["status"]
        row = conn.execute("SELECT development_log, status FROM foreshadows WHERE foreshadow_id=?", (fs_id,)).fetchone()
        if not row:
            return [TextContent(type="text", text=f"❌ 伏笔 {fs_id} 不存在")]
        dev_log = json.loads(row["development_log"])
        dev_log.append({"chapter": arguments.get("chapter_actual"), "event": new_status, "note": arguments.get("event_note", ""), "time": now})
        conn.execute("UPDATE foreshadows SET status=?, chapter_actual=?, development_log=?, updated_at=? WHERE foreshadow_id=?",
                     (new_status, arguments.get("chapter_actual"), json.dumps(dev_log, ensure_ascii=False), now, fs_id))
        conn.commit()
        return [TextContent(type="text", text=f"✅ {fs_id} 状态已更新为: {new_status}")]

    elif name == "get_foreshadow_detail":
        fs_id = arguments["foreshadow_id"]
        row = conn.execute("SELECT * FROM foreshadows WHERE foreshadow_id=?", (fs_id,)).fetchone()
        if not row:
            return [TextContent(type="text", text=f"❌ 伏笔 {fs_id} 不存在")]
        data = dict(row)
        for k in ["clue_vector", "development_log", "dependencies", "related_chars", "related_plots"]:
            try:
                data[k] = json.loads(data[k])
            except:
                pass
        return [TextContent(type="text", text=json.dumps(data, ensure_ascii=False, indent=2))]

    elif name == "check_health_report":
        cur = arguments["current_chapter"]
        risks = conn.execute("SELECT foreshadow_id, title, chapter_expected FROM foreshadows WHERE status='待回收' AND chapter_expected < ?", (cur,)).fetchall()
        abandoned = conn.execute("SELECT foreshadow_id, title FROM foreshadows WHERE status='废弃'").fetchall()
        lines = [f"📊 伏笔健康报告 (当前第{cur}章)", "="*40]
        if risks:
            lines.append(f"⚠️ 烂尾风险 ({len(risks)}个):")
            for r in risks:
                lines.append(f"   - {r['foreshadow_id']} 《{r['title']}》 已超期{cur - r['chapter_expected']}章")
        else:
            lines.append("✅ 无烂尾风险")
        if abandoned:
            lines.append(f"🗑️ 废弃伏笔 ({len(abandoned)}个):")
            for r in abandoned:
                lines.append(f"   - {r['foreshadow_id']} 《{r['title']}》")
        return [TextContent(type="text", text="\n".join(lines))]

    conn.close()
    return [TextContent(type="text", text="未知工具")]

async def main():
    _ensure_db()
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
