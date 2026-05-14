import sys, os, traceback
sys.path.insert(0, r'd:\Trae CN\github\nwacs\nwacs\core\v8')
os.chdir(r'd:\Trae CN\github\nwacs\nwacs\core\v8')

print("Testing DeepSeek generate in isolation...")
try:
    from engine.creative_engine import SmartCreativeEngine
    engine = SmartCreativeEngine()
    print("Engine created, testing generate...")
    result = engine.models['deepseek'].generate(
        'Reply with JSON only: {"status":"ok"}',
        temperature=0.7,
        max_tokens=50
    )
    print(f"Result: {result}")
    print("DeepSeek generate OK")
except Exception as e:
    print(f"Error: {e}")
    traceback.print_exc()
