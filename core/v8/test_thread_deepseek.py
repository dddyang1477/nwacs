import sys, os, traceback, threading, time
sys.path.insert(0, r'd:\Trae CN\github\nwacs\nwacs\core\v8')
os.chdir(r'd:\Trae CN\github\nwacs\nwacs\core\v8')

print("Importing...")
from engine.creative_engine import SmartCreativeEngine

print("Creating engine...")
engine = SmartCreativeEngine()

def test_in_thread():
    print(f"[Thread {threading.current_thread().name}] Starting DeepSeek call...")
    try:
        result = engine.models["deepseek"].generate("Say hello in one word", temperature=0.7, max_tokens=20)
        print(f"[Thread {threading.current_thread().name}] Result: {result}")
    except Exception as e:
        print(f"[Thread {threading.current_thread().name}] ERROR: {e}")
        traceback.print_exc()

print("Testing in main thread...")
test_in_thread()

print("\nTesting in separate thread...")
t = threading.Thread(target=test_in_thread, name="TestThread")
t.start()
t.join(timeout=30)
print("Thread test complete")

print("\nTesting concurrent threads...")
threads = []
for i in range(3):
    t = threading.Thread(target=test_in_thread, name=f"Worker-{i}")
    threads.append(t)
    t.start()

for t in threads:
    t.join(timeout=30)

print("All tests complete")
