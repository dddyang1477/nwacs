from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

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
    print(f"ENDPOINT CALLED: genre={req.genre}")
    return {"success": True, "genre": req.genre, "style": req.style}

@app.get("/api/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    print("Starting pure FastAPI server on 8095...")
    uvicorn.run(app, host="127.0.0.1", port=8095, log_level="info")
