#!/usr/bin/env python3
import sys
import time

# 输出到文件
with open('test_output.log', 'w', encoding='utf-8') as f:
    f.write(f"Python version: {sys.version}\n")
    f.write(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write("Script started\n")

print("Test script running...", flush=True)
print("Check test_output.log for details", flush=True)

# 简单延迟
for i in range(3):
    print(f"Count: {i+1}", flush=True)
    time.sleep(1)

print("Done!", flush=True)
