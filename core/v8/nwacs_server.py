#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 商用级API服务器
为前端UI提供REST API，整合所有核心模块
"""

import sys
import os
import json
import time
import uuid
import traceback
from typing import Dict, List, Any, Optional
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

from plot_brainstorm_engine import PlotBrainstormEngine, PlotArcType
from engine.creative_engine import SmartCreativeEngine
from enhanced_ai_detector import EnhancedAIDetector
from pleasure_beat_analyzer import PleasureBeatAnalyzer
from writing_knowledge_engine import WritingKnowledgeEngine
from genre_profile_manager import GenreProfileManager
from character_voice_injector import CharacterVoiceInjector
from auto_consistency_pipeline import AutoConsistencyPipeline
from novel_memory_manager import NovelMemoryManager
from simple_direct_pipeline import SimpleDirectPipeline
from chinese_traditional_namer import ChineseTraditionalNamer

app = FastAPI(title="NWACS API", version="9.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"\n{'='*60}")
    print(f"ERROR in {request.method} {request.url.path}")
    traceback.print_exc()
    print(f"{'='*60}\n")
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc), "type": type(exc).__name__},
    )

creative_engine = SmartCreativeEngine()
plotter = PlotBrainstormEngine(creative_engine=creative_engine)
detector = EnhancedAIDetector()
beat_analyzer = PleasureBeatAnalyzer()
knowledge_engine = WritingKnowledgeEngine()
genre_manager = GenreProfileManager()
voice_injector = CharacterVoiceInjector()
consistency = AutoConsistencyPipeline()
namer = ChineseTraditionalNamer()

sessions: Dict[str, Dict] = {}


class PlotRequest(BaseModel):
    genre: str = "玄幻"
    style: str = "热血爽文"
    tone: str = "紧张刺激"
    length: str = "中长篇"
    protagonist: str = ""
    theme: str = ""
    extra_requirements: str = ""
    session_id: Optional[str] = None


class OutlineRequest(BaseModel):
    session_id: str
    plot_id: str


class ChapterRequest(BaseModel):
    session_id: str
    chapter_num: int


class AIDetectRequest(BaseModel):
    text: str
    deep: bool = False


GENRE_OPTIONS = {
    "玄幻": {"icon": "🐉", "desc": "东方奇幻世界，修炼体系，逆天改命", "color": "#7c3aed"},
    "都市": {"icon": "🏙️", "desc": "现代都市背景，商战职场，异能隐世", "color": "#2563eb"},
    "仙侠": {"icon": "⚔️", "desc": "修仙问道，法宝灵兽，飞升渡劫", "color": "#059669"},
    "科幻": {"icon": "🚀", "desc": "未来科技，星际文明，AI觉醒", "color": "#0891b2"},
    "悬疑": {"icon": "🔍", "desc": "推理探案，层层反转，真相揭秘", "color": "#d97706"},
    "言情": {"icon": "💕", "desc": "情感纠葛，甜宠虐恋，命中注定", "color": "#db2777"},
    "历史": {"icon": "📜", "desc": "架空历史，权谋争霸，王朝更迭", "color": "#b45309"},
    "游戏": {"icon": "🎮", "desc": "虚拟现实，游戏异界，数据升级", "color": "#4f46e5"},
    "恐怖": {"icon": "👻", "desc": "灵异惊悚，规则怪谈，细思极恐", "color": "#6b21a8"},
    "武侠": {"icon": "🥋", "desc": "江湖恩怨，绝世武功，侠之大者", "color": "#b91c1c"},
}

STYLE_OPTIONS = {
    "热血爽文": {"icon": "🔥", "desc": "节奏明快，打脸不断，爽感拉满"},
    "轻松搞笑": {"icon": "😄", "desc": "幽默诙谐，吐槽不断，轻松愉快"},
    "黑暗深沉": {"icon": "🌑", "desc": "人性探讨，道德困境，沉重深刻"},
    "温馨治愈": {"icon": "🌸", "desc": "温暖人心，日常美好，治愈系"},
    "悬疑烧脑": {"icon": "🧩", "desc": "伏笔重重，反转不断，烧脑体验"},
    "史诗宏大": {"icon": "🏰", "desc": "世界观庞大，多线叙事，史诗感"},
}

TONE_OPTIONS = {
    "紧张刺激": "节奏紧凑，冲突密集，读者停不下来",
    "轻松愉快": "氛围轻松，笑点密集，阅读无压力",
    "虐心催泪": "情感浓烈，虐点精准，催泪效果强",
    "冷静克制": "叙事冷静，留白多，余味悠长",
    "热血燃爆": "情绪高涨，战斗精彩，燃点不断",
}

LENGTH_OPTIONS = {
    "短篇": "3-5万字，精炼有力",
    "中篇": "10-30万字，结构完整",
    "中长篇": "50-100万字，世界观丰富",
    "长篇": "100-300万字，史诗级叙事",
    "超长篇": "300万字+，网文标配",
}


def _get_or_create_session(session_id: Optional[str] = None) -> str:
    if session_id and session_id in sessions:
        return session_id
    new_id = str(uuid.uuid4())[:8]
    sessions[new_id] = {
        "created_at": datetime.now().isoformat(),
        "plots": [],
        "selected_plot": None,
        "outline": None,
        "chapters": {},
        "config": {},
    }
    return new_id


@app.get("/api/options")
async def get_options():
    return {
        "genres": GENRE_OPTIONS,
        "styles": STYLE_OPTIONS,
        "tones": TONE_OPTIONS,
        "lengths": LENGTH_OPTIONS,
    }


@app.post("/api/generate_plots")
async def generate_plots(req: PlotRequest):
    session_id = _get_or_create_session(req.session_id)
    session = sessions[session_id]
    session["config"] = {
        "genre": req.genre,
        "style": req.style,
        "tone": req.tone,
        "length": req.length,
        "protagonist": req.protagonist,
        "theme": req.theme,
        "extra": req.extra_requirements,
    }

    genre_context = ""
    if genre_manager:
        try:
            from genre_profile_manager import GenreType
            genre_map = {gt.label: gt for gt in GenreType}
            genre_enum = genre_map.get(req.genre)
            if genre_enum:
                genre_manager.set_genre(genre_enum)
                genre_context = genre_manager.get_full_generation_context(include_pleasure=True)
        except Exception:
            pass

    extra_str = f"\n额外要求: {req.extra_requirements}" if req.extra_requirements else ""
    protagonist_str = f"\n主角设定: {req.protagonist}" if req.protagonist else ""

    prompt = f"""你是一位资深小说策划编辑，请为以下需求生成3个完全不同方向的剧情方案。

【用户需求】
- 题材: {req.genre}
- 风格: {req.style}
- 基调: {req.tone}
- 篇幅: {req.length}
- 主题: {req.theme}{protagonist_str}{extra_str}

{genre_context}

【要求】
1. 生成3个完全不同的剧情方案，每个方案要有独特的核心创意
2. 每个方案包含：方案名称、一句话梗概、核心创意、主角设定、主要冲突、预期爽点、适合读者群
3. 方案之间要有明显差异化（不同世界观/不同主角类型/不同冲突模式）
4. 每个方案都要有商业价值，符合当前网文市场趋势

请严格按照以下JSON格式输出（不要输出其他内容）：
```json
{{
  "plots": [
    {{
      "id": "plot_1",
      "name": "方案名称",
      "tagline": "一句话梗概（20字以内）",
      "core_idea": "核心创意（100字）",
      "protagonist": "主角设定（50字）",
      "main_conflict": "主要冲突（50字）",
      "expected_beats": "预期爽点（50字）",
      "target_readers": "适合读者群（30字）",
      "innovation": "创新亮点（50字）"
    }}
  ]
}}
```"""

    try:
        result_text = creative_engine.models["deepseek"].generate(
            prompt, temperature=0.9, max_tokens=3000
        )

        json_match = result_text
        if "```json" in result_text:
            json_match = result_text.split("```json")[1].split("```")[0]
        elif "```" in result_text:
            json_match = result_text.split("```")[1].split("```")[0]

        data = json.loads(json_match.strip())
        plots = data.get("plots", [])

        for i, plot in enumerate(plots):
            plot["id"] = f"plot_{i+1}"
            plot["color"] = ["#7c3aed", "#2563eb", "#059669", "#d97706", "#db2777"][i % 5]

        session["plots"] = plots
        return {"success": True, "session_id": session_id, "plots": plots}

    except Exception as e:
        fallback_plots = _generate_fallback_plots(req)
        session["plots"] = fallback_plots
        return {
            "success": True,
            "session_id": session_id,
            "plots": fallback_plots,
            "note": f"使用本地模板生成 (API: {str(e)[:100]})",
        }


def _generate_fallback_plots(req: PlotRequest) -> List[Dict]:
    ideas = plotter.brainstorm_ideas(req.genre, req.theme, count=3)
    plots = []
    for i, idea in enumerate(ideas):
        plots.append({
            "id": f"plot_{i+1}",
            "name": idea.get("template", f"方案{i+1}"),
            "tagline": idea.get("core_concept", "")[:20],
            "core_idea": idea.get("opening_scene", ""),
            "protagonist": f"{req.genre}世界中的{'普通' if i == 0 else '天才' if i == 1 else '神秘'}主角",
            "main_conflict": idea.get("key_conflict", ""),
            "expected_beats": idea.get("emotional_core", ""),
            "target_readers": f"喜欢{req.style}的读者",
            "innovation": idea.get("suggested_twist", ""),
            "color": ["#7c3aed", "#2563eb", "#059669"][i],
        })
    return plots


@app.post("/api/select_plot")
async def select_plot(req: OutlineRequest):
    if req.session_id not in sessions:
        raise HTTPException(404, "会话不存在")

    session = sessions[req.session_id]
    selected = None
    for p in session.get("plots", []):
        if p["id"] == req.plot_id:
            selected = p
            break

    if not selected:
        raise HTTPException(404, "方案不存在")

    session["selected_plot"] = selected

    config = session.get("config", {})
    prompt = f"""你是一位资深小说大纲策划，请为以下选定的剧情方案生成详细大纲。

【选定方案】
- 方案名称: {selected['name']}
- 核心创意: {selected['core_idea']}
- 主角设定: {selected['protagonist']}
- 主要冲突: {selected['main_conflict']}

【创作配置】
- 题材: {config.get('genre', '玄幻')}
- 风格: {config.get('style', '热血爽文')}
- 基调: {config.get('tone', '紧张刺激')}
- 篇幅: {config.get('length', '中长篇')}

【要求】
1. 生成完整的三幕式大纲结构
2. 每幕包含3-5个关键情节点
3. 标注高潮章节和反转点
4. 包含主要人物关系网
5. 标注伏笔埋设和回收点

请严格按照以下JSON格式输出：
```json
{{
  "outline": {{
    "title": "作品暂定名",
    "summary": "200字故事梗概",
    "total_chapters_estimate": 100,
    "acts": [
      {{
        "act_num": 1,
        "name": "第一幕：开端",
        "chapter_range": "1-30章",
        "description": "本幕概述",
        "key_events": [
          {{"chapter": 1, "event": "事件描述", "type": "开场/冲突/转折/高潮", "foreshadowing": "伏笔内容"}}
        ]
      }}
    ],
    "character_web": [
      {{"name": "角色名", "role": "主角/反派/盟友/导师", "relation": "关系描述", "arc": "角色弧光"}}
    ],
    "foreshadowing_map": [
      {{"plant_chapter": 5, "payoff_chapter": 45, "content": "伏笔内容", "impact": "影响程度"}}
    ]
  }}
}}
```"""

    try:
        result_text = creative_engine.models["deepseek"].generate(
            prompt, temperature=0.8, max_tokens=4000
        )

        json_match = result_text
        if "```json" in result_text:
            json_match = result_text.split("```json")[1].split("```")[0]
        elif "```" in result_text:
            json_match = result_text.split("```")[1].split("```")[0]

        data = json.loads(json_match.strip())
        outline = data.get("outline", {})

        session["outline"] = outline
        return {"success": True, "outline": outline}

    except Exception as e:
        fallback_outline = _generate_fallback_outline(selected, config)
        session["outline"] = fallback_outline
        return {
            "success": True,
            "outline": fallback_outline,
            "note": f"使用本地模板生成",
        }


def _generate_fallback_outline(selected: Dict, config: Dict) -> Dict:
    genre = config.get("genre", "玄幻")
    return {
        "title": f"《{selected['name']}》",
        "summary": selected.get("core_idea", ""),
        "total_chapters_estimate": 100,
        "acts": [
            {
                "act_num": 1,
                "name": "第一幕：开端",
                "chapter_range": "1-30章",
                "description": "主角登场，世界观展开，核心冲突建立",
                "key_events": [
                    {"chapter": 1, "event": "主角登场，展示日常与困境", "type": "开场", "foreshadowing": "主角的特殊之处"},
                    {"chapter": 5, "event": "触发事件，主角被迫踏上征程", "type": "转折", "foreshadowing": ""},
                    {"chapter": 15, "event": "第一次重大挑战，主角初露锋芒", "type": "冲突", "foreshadowing": "更大阴谋的线索"},
                    {"chapter": 25, "event": "第一幕高潮，主角做出关键选择", "type": "高潮", "foreshadowing": "第二幕的伏笔"},
                ],
            },
            {
                "act_num": 2,
                "name": "第二幕：发展",
                "chapter_range": "31-70章",
                "description": "冲突升级，主角成长，各方势力登场",
                "key_events": [
                    {"chapter": 35, "event": "新势力登场，局势复杂化", "type": "冲突", "foreshadowing": ""},
                    {"chapter": 50, "event": "重大挫折，主角陷入低谷", "type": "转折", "foreshadowing": "转机线索"},
                    {"chapter": 60, "event": "主角突破，实力大幅提升", "type": "高潮", "foreshadowing": ""},
                    {"chapter": 70, "event": "第二幕高潮，真相开始浮出水面", "type": "高潮", "foreshadowing": "最终对决的铺垫"},
                ],
            },
            {
                "act_num": 3,
                "name": "第三幕：结局",
                "chapter_range": "71-100章",
                "description": "最终对决，伏笔回收，主题升华",
                "key_events": [
                    {"chapter": 80, "event": "最终对决开始，各方势力汇聚", "type": "冲突", "foreshadowing": ""},
                    {"chapter": 90, "event": "最大反转，真相揭露", "type": "转折", "foreshadowing": "回收前期伏笔"},
                    {"chapter": 95, "event": "最终决战，主角面临终极选择", "type": "高潮", "foreshadowing": ""},
                    {"chapter": 100, "event": "结局，主题升华，留下余韵", "type": "结局", "foreshadowing": ""},
                ],
            },
        ],
        "character_web": [
            {"name": "主角", "role": "主角", "relation": "—", "arc": "从平凡到伟大的成长弧光"},
            {"name": "导师角色", "role": "导师", "relation": "引导主角", "arc": "牺牲或退场，完成使命"},
            {"name": "主要反派", "role": "反派", "relation": "与主角对立", "arc": "揭示动机，或洗白或毁灭"},
            {"name": "盟友角色", "role": "盟友", "relation": "并肩作战", "arc": "从怀疑到信任"},
        ],
        "foreshadowing_map": [
            {"plant_chapter": 1, "payoff_chapter": 90, "content": "主角的身世之谜", "impact": "核心"},
            {"plant_chapter": 5, "payoff_chapter": 50, "content": "神秘物品的真正用途", "impact": "重要"},
            {"plant_chapter": 15, "payoff_chapter": 80, "content": "反派的真实目的", "impact": "核心"},
        ],
    }


@app.post("/api/generate_chapter")
async def generate_chapter(req: ChapterRequest):
    if req.session_id not in sessions:
        raise HTTPException(404, "会话不存在")

    session = sessions[req.session_id]
    config = session.get("config", {})
    outline = session.get("outline", {})
    selected = session.get("selected_plot", {})

    chapter_events = []
    for act in outline.get("acts", []):
        for event in act.get("key_events", []):
            if event.get("chapter") == req.chapter_num:
                chapter_events.append(event)

    prev_content = ""
    if req.chapter_num > 1:
        prev_chapter = session["chapters"].get(str(req.chapter_num - 1), {})
        prev_content = prev_chapter.get("content", "")[-500:]

    events_str = ""
    if chapter_events:
        events_str = "\n".join(
            f"- [{e.get('type', '事件')}] {e.get('event', '')}"
            for e in chapter_events
        )

    knowledge_prompt = ""
    if knowledge_engine:
        try:
            knowledge_prompt = knowledge_engine.inject_knowledge_to_prompt(
                base_prompt="",
                genre=config.get("genre", "玄幻"),
                chapter_num=req.chapter_num,
            )
        except Exception:
            pass

    prompt = f"""你是一位拥有15年经验的顶级{config.get('genre', '玄幻')}小说作家。

【作品信息】
- 书名: {outline.get('title', '未命名')}
- 题材: {config.get('genre', '玄幻')}
- 风格: {config.get('style', '热血爽文')}
- 基调: {config.get('tone', '紧张刺激')}

【故事梗概】
{outline.get('summary', selected.get('core_idea', ''))}

【本章大纲】
{events_str if events_str else '自由发挥，推进主线剧情'}

【前文回顾】
{prev_content if prev_content else '（第一章，无前文）'}

{knowledge_prompt}

【去AI铁律 — 必须内化到写作本能中】
- 禁止使用"首先...其次...最后"等结构化连接词
- 禁止使用"值得注意的是""综上所述""总而言之"等AI模板句式
- 禁止句长均匀：长短句要剧烈交替
- 禁止情感平滑：情绪要有撕裂感
- 禁止逻辑过于完美：加入人类的犹豫、自我纠正
- 30%短句(3-10字) + 50%中句(11-25字) + 20%长句(26-50字)
- 关键情节用单句成段制造冲击力
- 加入本土生活细节：烟火气、人情世故

【输出格式】
- 直接输出小说正文，不要任何解释、标记、前缀
- 不要写"本章完""第X章"等标记
- 段落间用空行分隔
- 对话使用中文引号「」
- 目标字数: 2500-3500字"""

    try:
        content = creative_engine.models["deepseek"].generate(
            prompt, temperature=0.85, max_tokens=4000
        )

        content = content.strip()
        for prefix in ["第", "Chapter", "##"]:
            if content.startswith(prefix):
                lines = content.split("\n", 1)
                if len(lines) > 1:
                    content = lines[1].strip()

        ai_diagnosis = None
        beat_analysis = None

        if knowledge_engine:
            try:
                diagnosis = knowledge_engine.diagnose_ai_traits(content)
                ai_diagnosis = {
                    "score": diagnosis.overall_ai_score,
                    "risk_level": diagnosis.risk_level,
                    "top_traits": [t[0] for t in diagnosis.detected_traits[:3]],
                }
            except Exception:
                pass

        if beat_analyzer:
            try:
                rhythm = beat_analyzer.analyze(content, req.chapter_num, req.chapter_num <= 3)
                beat_analysis = {
                    "beat_density": rhythm.beat_density,
                    "score": rhythm.score,
                    "hook_strength": rhythm.hook_strength,
                }
            except Exception:
                pass

        chapter_data = {
            "chapter_num": req.chapter_num,
            "content": content,
            "word_count": len(content),
            "ai_diagnosis": ai_diagnosis,
            "beat_analysis": beat_analysis,
            "generated_at": datetime.now().isoformat(),
        }
        session["chapters"][str(req.chapter_num)] = chapter_data

        return {"success": True, "chapter": chapter_data}

    except Exception as e:
        raise HTTPException(500, f"生成失败: {str(e)}")


@app.post("/api/detect_ai")
async def detect_ai(req: AIDetectRequest):
    if req.deep and knowledge_engine:
        diagnosis = knowledge_engine.diagnose_ai_traits(req.text)
        pipeline = knowledge_engine.generate_deai_pipeline(req.text, "voice")
        return {
            "success": True,
            "mode": "deep",
            "score": diagnosis.overall_ai_score,
            "risk_level": diagnosis.risk_level,
            "traits": [{"name": t[0], "severity": round(t[1], 3)} for t in diagnosis.detected_traits[:5]],
            "fix_priority": diagnosis.fix_priority[:3],
            "deai_stages": len(pipeline.stages),
        }

    report = detector.detect(req.text)
    return {
        "success": True,
        "mode": "basic",
        "score": report.overall_score,
        "level": report.level,
        "suggestions": report.suggestions[:3],
    }


@app.get("/api/session/{session_id}")
async def get_session(session_id: str):
    if session_id not in sessions:
        raise HTTPException(404, "会话不存在")
    session = sessions[session_id]
    return {
        "session_id": session_id,
        "config": session.get("config", {}),
        "plots": session.get("plots", []),
        "selected_plot": session.get("selected_plot"),
        "outline": session.get("outline"),
        "chapter_count": len(session.get("chapters", {})),
    }


@app.get("/api/health")
async def health():
    return {
        "status": "ok",
        "version": "9.0",
        "modules": {
            "creative_engine": creative_engine is not None,
            "plotter": plotter is not None,
            "detector": detector is not None,
            "beat_analyzer": beat_analyzer is not None,
            "knowledge_engine": knowledge_engine is not None,
            "genre_manager": genre_manager is not None,
        },
    }


FRONTEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend")
os.makedirs(FRONTEND_DIR, exist_ok=True)

if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


@app.get("/")
async def root():
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "NWACS API Server v9.0", "docs": "/docs"}


if __name__ == "__main__":
    import uvicorn
    print("=" * 60)
    print("  NWACS 商用级API服务器 v9.0")
    print("  http://localhost:8099")
    print("  API文档: http://localhost:8099/docs")
    print("=" * 60)
    uvicorn.run(app, host="0.0.0.0", port=8099, log_level="info")
