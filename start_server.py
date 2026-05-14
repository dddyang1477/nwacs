import subprocess
import sys
import os

os.chdir(os.path.join(os.path.dirname(__file__), 'core', 'v8'))
proc = subprocess.Popen(
    [sys.executable, 'nwacs_server_v3.py'],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True
)

import time
time.sleep(8)

for _ in range(5):
    line = proc.stdout.readline()
    if line:
        print(line.strip())
    else:
        break

print(f"SERVER_PID={proc.pid}")
print("Server started in background. Press Ctrl+C to stop.")