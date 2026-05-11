import sys, os, traceback
sys.path.insert(0, r'd:\Trae CN\github\nwacs\nwacs\core\v8')
os.chdir(r'd:\Trae CN\github\nwacs\nwacs\core\v8')

print("Testing Pydantic model with Chinese characters...")
from pydantic import BaseModel

class PlotRequest(BaseModel):
    genre: str = "玄幻"
    style: str = "热血爽文"
    tone: str = "紧张刺激"
    length: str = "中长篇"
    theme: str = "逆境成长"
    protagonist: str = ""
    extra_requirements: str = ""
    session_id: str = ""

try:
    req = PlotRequest(genre="玄幻", style="热血爽文", tone="紧张刺激", length="中长篇", theme="逆境成长")
    print(f"Model created: genre={req.genre}")
    print("Pydantic model OK")
except Exception as e:
    traceback.print_exc()

print("\nTesting with JSON...")
import json
data = '{"genre": "玄幻", "style": "热血爽文", "tone": "紧张刺激", "length": "中长篇", "theme": "逆境成长"}'
try:
    req = PlotRequest.model_validate_json(data)
    print(f"JSON parsed: genre={req.genre}")
    print("JSON parsing OK")
except Exception as e:
    traceback.print_exc()
