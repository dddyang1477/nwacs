#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os, json, py_compile

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
sys.path.insert(0, os.path.join(BASE, "core", "v8"))

errors = []
ok_count = 0

def check_py_syntax(filepath):
    try:
        py_compile.compile(filepath, doraise=True)
        return True, None
    except py_compile.PyCompileError as e:
        return False, str(e)
    except Exception as e:
        return False, str(e)

def check_json(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            json.load(f)
        return True, None
    except Exception as e:
        return False, str(e)

print("=" * 70)
print("  NWACS Final Verification")
print("=" * 70)

# 1. Directory structure
print("\n[1] Directory Structure")
required_dirs = [
    "core", "core/v8", "core/v8/engine", "core/v8/config",
    "core/v8/api_gateway", "core/v8/knowledge_base", "core/v8/skill_manager",
    "config", "docs", "archive", "scripts", "agents"
]
for d in required_dirs:
    path = os.path.join(BASE, d)
    if os.path.isdir(path):
        ok_count += 1
    else:
        errors.append(f"Missing dir: {d}")

required_files = [
    "main.py", "core/__init__.py", "core/v8/__init__.py",
    "core/v8/NWACS_FINAL.py", "core/v8/ai_detector_and_rewriter.py",
    "core/v8/quality_check_and_save_v2.py", "core/v8/three_time_quality_check.py",
    "core/v8/bestseller_deep_analyzer_v16.py", "core/v8/bestseller_opening_templates_v16.py",
    "core/v8/opening_examples_library_v15.py", "core/v8/net_novel_core_guide_v15.py",
    "core/v8/writing_templates_library.py", "core/v8/system_diagnosis.py",
    "core/v8/engine/__init__.py", "core/v8/engine/creative_engine.py",
    "core/v8/config/__init__.py", "core/v8/config/config_manager.py",
    "core/v8/api_gateway/__init__.py", "core/v8/api_gateway/api_gateway.py",
    "core/v8/knowledge_base/__init__.py", "core/v8/knowledge_base/knowledge_manager.py",
    "core/v8/skill_manager/__init__.py", "core/v8/skill_manager/skill_manager.py",
    "config/config.json", "config/models.json", "config/agents.json",
    "core/config.json", "core/logger.py",
]
for f in required_files:
    path = os.path.join(BASE, f)
    if os.path.isfile(path):
        ok_count += 1
    else:
        errors.append(f"Missing file: {f}")

print(f"  Checked: {len(required_dirs) + len(required_files)} items")

# 2. Python syntax
print("\n[2] Python Syntax")
core_py_files = []
for root, dirs, files in os.walk(os.path.join(BASE, "core")):
    for f in files:
        if f.endswith('.py'):
            core_py_files.append(os.path.join(root, f))

for fpath in core_py_files:
    rel = os.path.relpath(fpath, BASE)
    ok, err = check_py_syntax(fpath)
    if ok:
        ok_count += 1
    else:
        errors.append(f"Syntax: {rel} - {err}")

print(f"  Checked: {len(core_py_files)} .py files")

# 3. JSON
print("\n[3] JSON Files")
json_files = []
for root, dirs, files in os.walk(os.path.join(BASE, "core")):
    for f in files:
        if f.endswith('.json'):
            json_files.append(os.path.join(root, f))
for root, dirs, files in os.walk(os.path.join(BASE, "config")):
    for f in files:
        if f.endswith('.json'):
            json_files.append(os.path.join(root, f))

for fpath in json_files:
    rel = os.path.relpath(fpath, BASE)
    ok, err = check_json(fpath)
    if ok:
        ok_count += 1
    else:
        errors.append(f"JSON: {rel} - {err}")

print(f"  Checked: {len(json_files)} .json files")

# 4. Core imports
print("\n[4] Core Module Imports")
modules = [
    ("NWACS_FINAL", "NWACSFinal"),
    ("ai_detector_and_rewriter", None),
    ("quality_check_and_save_v2", "QualityChecker"),
    ("three_time_quality_check", "call_three_time_quality_check"),
    ("bestseller_deep_analyzer_v16", "BestsellerDeepAnalyzer"),
    ("bestseller_opening_templates_v16", "BestsellerOpeningTemplates"),
    ("opening_examples_library_v15", None),
    ("net_novel_core_guide_v15", None),
    ("writing_templates_library", None),
    ("system_diagnosis", None),
]

for mod_name, attr in modules:
    try:
        mod = __import__(mod_name)
        if attr:
            getattr(mod, attr)
        ok_count += 1
    except Exception as e:
        errors.append(f"Import: {mod_name} - {e}")

# 5. Sub-package imports
print("\n[5] Sub-package Imports")
sub_modules = [
    ("engine.creative_engine", "SmartCreativeEngine"),
    ("config.config_manager", "ConfigManager"),
    ("api_gateway.api_gateway", "APIGateway"),
    ("knowledge_base.knowledge_manager", "KnowledgeBaseManager"),
    ("skill_manager.skill_manager", "SkillManager"),
]

for mod_name, attr in sub_modules:
    try:
        mod = __import__(mod_name, fromlist=[attr])
        if attr:
            getattr(mod, attr)
        ok_count += 1
    except Exception as e:
        errors.append(f"Sub-import: {mod_name} - {e}")

# 6. Entry point
print("\n[6] Entry Point (main.py)")
main_path = os.path.join(BASE, "main.py")
if os.path.isfile(main_path):
    ok, err = check_py_syntax(main_path)
    if ok:
        ok_count += 1
    else:
        errors.append(f"main.py syntax: {err}")
else:
    errors.append("main.py not found")

# Summary
print("\n" + "=" * 70)
print("  Results")
print("=" * 70)
print(f"  PASS: {ok_count}")
print(f"  FAIL: {len(errors)}")

if errors:
    print(f"\n  Errors:")
    for e in errors:
        print(f"    - {e}")

if not errors:
    print("\n  ALL CHECKS PASSED! NWACS optimization complete!")
else:
    print(f"\n  {len(errors)} issues to fix")

print("=" * 70)
