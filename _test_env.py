#!/usr/bin/env python3
"""Test script to verify Python and git availability"""
import subprocess
import os

log_path = r"d:\Trae CN\github\nwacs\nwacs\_test_py.txt"

with open(log_path, "w", encoding="utf-8") as f:
    f.write("Python test script started\n")
    
    # Test Python version
    import sys
    f.write(f"Python version: {sys.version}\n")
    
    # Test git availability
    try:
        result = subprocess.run(["git", "--version"], capture_output=True, text=True, timeout=10)
        f.write(f"git --version: {result.stdout}\n")
        if result.stderr:
            f.write(f"git stderr: {result.stderr}\n")
    except FileNotFoundError:
        f.write("git NOT FOUND in PATH\n")
    except Exception as e:
        f.write(f"git error: {e}\n")
    
    f.write("Test complete\n")

print(f"Log written to {log_path}")