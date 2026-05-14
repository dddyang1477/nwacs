#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 全面联通性检查脚本 v3
"""

import os
import sys
import json
import py_compile
import importlib.util
import io

if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'core'))
sys.path.insert(0, os.path.join(BASE_DIR, 'core', 'v8'))

SKIP_DIRS = {'__pycache__', '.git', 'node_modules', 'backup', 'archive',
             'temp_backup', 'temp_tests', 'novel-mcp-server-v2',
             'novel_project', 'output', 'learning', '.trae'}
SKIP_FILES = {'_check.py', '_check_all.py', '_fix_json.py', '_fix_quotes.py',
              '_fix_quotes2.py', '_fix_all_quotes.py'}

results = []
def log(msg):
    results.append(msg)
    try:
        print(msg)
    except UnicodeEncodeError:
        print(msg.encode('ascii', errors='replace').decode('ascii'))

log("=" * 80)
log("NWACS Full Connectivity Check v3")
log("=" * 80)

# ============================================================
# 1. Python Syntax Check
# ============================================================
log("\n[1/5] Python Syntax Check")

py_files = []
for root, dirs, files in os.walk(BASE_DIR):
    dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
    for f in files:
        if f.endswith('.py') and f not in SKIP_FILES:
            py_files.append(os.path.join(root, f))

log(f"  Total: {len(py_files)} Python files")

syntax_errors = []
for fp in py_files:
    rel = os.path.relpath(fp, BASE_DIR)
    try:
        py_compile.compile(fp, doraise=True)
    except py_compile.PyCompileError as e:
        syntax_errors.append((rel, str(e)))

if syntax_errors:
    log(f"  [FAIL] Syntax errors: {len(syntax_errors)}")
    for rel, err in syntax_errors:
        log(f"    - {rel}")
        log(f"      {err[:300]}")
else:
    log(f"  [OK] All passed ({len(py_files)} files)")

# ============================================================
# 2. JSON Validity Check
# ============================================================
log("\n[2/5] JSON Validity Check")

json_files = []
for root, dirs, files in os.walk(BASE_DIR):
    dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
    for f in files:
        if f.endswith('.json'):
            json_files.append(os.path.join(root, f))

log(f"  Total: {len(json_files)} JSON files")

json_errors = []
json_empty = []
for fp in json_files:
    rel = os.path.relpath(fp, BASE_DIR)
    try:
        with open(fp, 'r', encoding='utf-8') as f:
            content = f.read()
        if not content.strip():
            json_empty.append(rel)
            continue
        json.loads(content)
    except json.JSONDecodeError as e:
        json_errors.append((rel, str(e)))
    except Exception as e:
        json_errors.append((rel, f"Read error: {e}"))

if json_errors:
    log(f"  [FAIL] JSON errors: {len(json_errors)}")
    for rel, err in json_errors:
        log(f"    - {rel}: {err[:200]}")
else:
    log(f"  [OK] All JSON valid")

if json_empty:
    log(f"  [WARN] Empty JSON files: {len(json_empty)}")
    for rel in json_empty:
        log(f"    - {rel}")

# ============================================================
# 3. Core Module Import Check
# ============================================================
log("\n[3/5] Core Module Import Check")

core_modules = [
    "core.v8.config.config_manager",
    "core.v8.engine.creative_engine",
    "core.v8.skill_manager.skill_manager",
    "core.v8.knowledge_base.knowledge_manager",
    "core.v8.api_gateway.api_gateway",
    "core.v8.bestseller_deep_analyzer_v16",
    "core.v8.bestseller_opening_templates_v16",
    "core.v8.opening_examples_library_v15",
    "core.v8.net_novel_core_guide_v15",
    "core.v8.writing_templates_library",
    "core.v8.quality_check_and_save_v2",
    "core.v8.three_time_quality_check",
    "core.v8.ai_detector_and_rewriter",
    "core.v8.system_diagnosis",
]

import_errors = []
import_ok = []

old_stdout = sys.stdout
sys.stdout = io.StringIO()

for modname in core_modules:
    try:
        importlib.import_module(modname)
        import_ok.append(modname)
    except SyntaxError as e:
        import_errors.append((modname, f"SyntaxError: {e}"))
    except Exception as e:
        import_errors.append((modname, f"{type(e).__name__}: {e}"))

sys.stdout = old_stdout

if import_errors:
    log(f"  [FAIL] Import failures: {len(import_errors)}")
    for mod, err in import_errors:
        log(f"    - {mod}: {err[:200]}")
else:
    log(f"  [OK] All imports successful ({len(import_ok)} modules)")

for m in import_ok:
    log(f"    OK {m}")

# ============================================================
# 4. Skill System Call Chain
# ============================================================
log("\n[4/5] Skill System Call Chain Check")

skill_desc_path = os.path.join(BASE_DIR, 'core', 'v8', 'skill_manager', 'skill_descriptions.json')
if os.path.exists(skill_desc_path):
    try:
        with open(skill_desc_path, 'r', encoding='utf-8') as f:
            skill_data = json.load(f)
        skills = skill_data.get('skills', {})
        log(f"  [OK] Skill descriptions valid, {len(skills)} skills:")
        for sid, sinfo in skills.items():
            name = sinfo.get('name', sid)
            features = sinfo.get('features', [])
            log(f"    - {name} ({sid}): {len(features)} features")
    except Exception as e:
        log(f"  [FAIL] Skill descriptions error: {e}")
else:
    log(f"  [FAIL] Skill descriptions file missing")

engine_dir = os.path.join(BASE_DIR, 'core', 'v8', 'engine')
engine_jsons = ['builtin_knowledge.json', 'character_profiles.json',
                'extended_knowledge.json', 'optimized_settings.json',
                'plot_outlines.json', 'world_settings.json',
                'writing_phrases.json', 'writing_templates.json',
                'xuanhuan_trend_data.json']
log(f"\n  Engine knowledge base files:")
for jf in engine_jsons:
    jp = os.path.join(engine_dir, jf)
    if os.path.exists(jp):
        try:
            with open(jp, 'r', encoding='utf-8') as f:
                data = json.load(f)
            size = len(json.dumps(data, ensure_ascii=False))
            if isinstance(data, dict):
                log(f"    OK {jf}: {len(data)} entries, {size} bytes")
            elif isinstance(data, list):
                log(f"    OK {jf}: {len(data)} elements, {size} bytes")
            else:
                log(f"    OK {jf}: valid ({size} bytes)")
        except Exception as e:
            log(f"    FAIL {jf}: {e}")
    else:
        log(f"    FAIL {jf}: file not found")

# ============================================================
# 5. Entry Point Files Check
# ============================================================
log("\n[5/5] Entry Point Files Check")

entry_files = [
    "core/v8/NWACS_FINAL.py",
    "core/v8/启动NWACS.bat",
    "core/v8/启动NWACS.ps1",
    "core/v8/智能启动NWACS.ps1",
    "core/v8/简单启动NWACS.ps1",
    "core/main.py",
    "core/nwacs_main.py",
    "core/nwacs_console.py",
    "core/nwacs_launcher.py",
    "core/nwacs_super_launcher.py",
    "core/nwacs_single.py",
    "nwacs_v8.py",
    "smart_start.py",
    "orchestrator.py",
]

for ef in entry_files:
    ep = os.path.join(BASE_DIR, ef)
    if os.path.exists(ep):
        size = os.path.getsize(ep)
        log(f"  OK {ef} ({size} bytes)")
    else:
        log(f"  MISS {ef}")

# ============================================================
# Summary
# ============================================================
log("\n" + "=" * 80)
log("Check Summary")
log("=" * 80)

total = len(syntax_errors) + len(json_errors) + len(json_empty) + len(import_errors)
log(f"\n  Python syntax errors: {len(syntax_errors)}")
log(f"  JSON errors:          {len(json_errors)}")
log(f"  Empty JSON files:     {len(json_empty)}")
log(f"  Import failures:      {len(import_errors)}")
log(f"  Total issues:         {total}")

if total == 0:
    log("\n  [OK] All checks passed! System connectivity is normal!")
else:
    log(f"\n  [WARN] Found {total} issues to fix")

log("\n" + "=" * 80)

with open(os.path.join(BASE_DIR, '_check_result.txt'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(results))
