import os
d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "黑日藏锋")
files = sorted([f for f in os.listdir(d) if f.startswith("黑日藏锋_第") and f.endswith(".txt")])
total = 0
for f in files:
    path = os.path.join(d, f)
    size = len(open(path, encoding="utf-8").read())
    total += size
    print(f"  {f}: {size} 字符")
print(f"  合计: {total} 字符")
