#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
print("Python version:", sys.version)
print("Testing NWACS_FINAL import...")

try:
    import importlib.util
    spec = importlib.util.spec_from_file_location("NWACS_FINAL", "NWACS_FINAL.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    print("[OK] Module loaded successfully!")
    print("[OK] Class NWACSFinal found:", hasattr(module, 'NWACSFinal'))
except Exception as e:
    print(f"[ERROR] {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
