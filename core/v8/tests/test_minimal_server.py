import sys, os, traceback
sys.path.insert(0, r'd:\Trae CN\github\nwacs\nwacs\core\v8')
os.chdir(r'd:\Trae CN\github\nwacs\nwacs\core\v8')

print("Step 1: Importing FastAPI...")
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

print("Step 2: Creating app...")
app = FastAPI()

print("Step 3: Importing NWACS modules...")
from engine.creative_engine import SmartCreativeEngine
from genre_profile_manager import GenreProfileManager, GenreType

print("Step 4: Initializing modules...")
engine = SmartCreativeEngine()
genre_manager = GenreProfileManager()

print("Step 5: Testing DeepSeek...")
result = engine.models["deepseek"].generate("Say hello", temperature=0.7, max_tokens=50)
print(f"DeepSeek result: {result[:100]}")

print("Step 6: Defining endpoint...")
class PlotRequest(BaseModel):
    genre: str = "玄幻"
    style: str = "热血爽文"
    tone: str = "紧张刺激"
    length: str = "中长篇"
    theme: str = "逆境成长"
    protagonist: str = ""
    extra_requirements: str = ""
    session_id: str = ""

@app.post("/api/generate_plots")
def generate_plots(req: PlotRequest):
    print(f"!!! ENDPOINT CALLED: genre={req.genre}")
    try:
        genre_map = {gt.label: gt for gt in GenreType}
        genre_enum = genre_map.get(req.genre)
        genre_context = ""
        if genre_enum:
            genre_manager.set_genre(genre_enum)
            genre_context = genre_manager.get_full_generation_context(include_pleasure=True)

        prompt = f"Generate 3 plot ideas for {req.genre} novel. Return JSON."
        print("Calling DeepSeek from endpoint...")
        result_text = engine.models["deepseek"].generate(prompt, temperature=0.9, max_tokens=500)
        print(f"Got response: {len(result_text)} chars")
        
        import json
        return {"success": True, "plots": [{"id": "p1", "name": "Test", "tagline": result_text[:50]}]}
    except Exception as e:
        print(f"ERROR: {e}")
        traceback.print_exc()
        return {"success": True, "plots": [{"id": "p1", "name": "Fallback", "tagline": str(e)[:50]}]}

@app.get("/api/health")
def health():
    return {"status": "ok"}

print("Step 7: Starting server...")
print("All setup complete, starting uvicorn...")
uvicorn.run(app, host="127.0.0.1", port=8096, log_level="info")
