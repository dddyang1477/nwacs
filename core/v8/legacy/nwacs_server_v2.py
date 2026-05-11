import sys, os
sys.path.insert(0, r'd:\Trae CN\github\nwacs\nwacs\core\v8')
os.chdir(r'd:\Trae CN\github\nwacs\nwacs\core\v8')

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn, json, traceback, asyncio
from concurrent.futures import ThreadPoolExecutor

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

executor = ThreadPoolExecutor(max_workers=4)

class PlotRequest(BaseModel):
    genre: str = "玄幻"
    style: str = "热血爽文"
    tone: str = "紧张刺激"
    length: str = "中长篇"
    theme: str = "逆境成长"
    protagonist: str = ""
    extra_requirements: str = ""
    session_id: str = ""

@app.get("/api/health")
async def health():
    return {"status": "ok"}

@app.post("/api/test_post")
async def test_post(req: PlotRequest):
    return {"received": req.genre, "style": req.style}

@app.post("/api/generate_plots")
async def generate_plots(req: PlotRequest):
    print(f"Received plot request: genre={req.genre}, style={req.style}")
    try:
        from engine.creative_engine import SmartCreativeEngine
        from genre_profile_manager import GenreProfileManager, GenreType

        genre_manager = GenreProfileManager()
        genre_map = {gt.label: gt for gt in GenreType}
        genre_enum = genre_map.get(req.genre)
        genre_context = ""
        if genre_enum:
            genre_manager.set_genre(genre_enum)
            genre_context = genre_manager.get_full_generation_context(include_pleasure=True)

        prompt = f"""You are a senior novel editor. Generate 3 completely different plot ideas for:
Genre: {req.genre}
Style: {req.style}
Tone: {req.tone}
Length: {req.length}
Theme: {req.theme}

{genre_context}

Return ONLY valid JSON:
{{"plots": [{{"id": "plot_1", "name": "...", "tagline": "...", "core_idea": "...", "protagonist": "...", "main_conflict": "...", "expected_beats": "...", "target_readers": "...", "innovation": "..."}}]}}"""

        print("Calling DeepSeek API...")
        engine = SmartCreativeEngine()
        result_text = engine.models["deepseek"].generate(prompt, temperature=0.9, max_tokens=3000)
        print(f"DeepSeek response length: {len(result_text)}")

        json_match = result_text
        if "```json" in result_text:
            json_match = result_text.split("```json")[1].split("```")[0]
        elif "```" in result_text:
            json_match = result_text.split("```")[1].split("```")[0]

        data = json.loads(json_match.strip())
        plots = data.get("plots", [])
        colors = ["#7c3aed", "#2563eb", "#059669", "#d97706", "#db2777"]
        for i, plot in enumerate(plots):
            plot["id"] = f"plot_{i+1}"
            plot["color"] = colors[i % 5]

        return {"success": True, "session_id": req.session_id or "test", "plots": plots}

    except Exception as e:
        print(f"Error in generate_plots: {e}")
        traceback.print_exc()
        return {
            "success": True,
            "session_id": req.session_id or "test",
            "plots": [
                {"id": "plot_1", "name": "逆天改命", "tagline": "平凡少年获得神秘传承，一路逆袭", "core_idea": "废柴主角意外获得上古传承", "protagonist": "出身平凡的坚毅少年", "main_conflict": "与天命抗争，打破阶级固化", "expected_beats": "打脸升级，逆天改命", "target_readers": "喜欢热血升级的读者", "innovation": "传统升级流加入现代元素", "color": "#7c3aed"},
                {"id": "plot_2", "name": "暗流涌动", "tagline": "都市阴影中的异能者战争", "core_idea": "现代都市隐藏着异能者世界", "protagonist": "意外觉醒异能的普通上班族", "main_conflict": "异能者组织间的明争暗斗", "expected_beats": "能力觉醒，组织对抗", "target_readers": "喜欢都市异能的读者", "innovation": "都市+异能+悬疑三合一", "color": "#2563eb"},
                {"id": "plot_3", "name": "星辰大海", "tagline": "星际流浪者的传奇冒险", "core_idea": "在星际文明中寻找失落的地球文明", "protagonist": "星际探险家", "main_conflict": "不同星际文明间的冲突", "expected_beats": "探索未知，文明碰撞", "target_readers": "喜欢科幻冒险的读者", "innovation": "东方哲学+西方科幻", "color": "#059669"},
            ],
            "note": f"Fallback: {str(e)[:100]}"
        }

if __name__ == "__main__":
    print("Starting test server on port 8098...")
    uvicorn.run(app, host="0.0.0.0", port=8098, log_level="info")
