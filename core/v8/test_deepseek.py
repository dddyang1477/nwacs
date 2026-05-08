import sys, traceback
sys.path.insert(0, r'd:\Trae CN\github\nwacs\nwacs\core\v8')

try:
    from engine.creative_engine import SmartCreativeEngine
    engine = SmartCreativeEngine()
    result = engine.models['deepseek'].generate(
        'Say hello in JSON: {"message": "hello"}',
        temperature=0.7,
        max_tokens=100
    )
    print(f"Result: {result[:200]}")
    print("DeepSeek API OK")
except Exception as e:
    traceback.print_exc()
