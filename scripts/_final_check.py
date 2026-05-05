import os
import json
import glob

base = os.path.dirname(os.path.abspath(__file__))

print("=" * 60)
print("NWACS 最终验证测试")
print("=" * 60)

# 1. Python syntax check
print("\n[1] Python Syntax Check")
py_errors = 0
for f in glob.glob(os.path.join(base, '**', '*.py'), recursive=True):
    if '__pycache__' in f:
        continue
    try:
        with open(f, 'r', encoding='utf-8') as fh:
            source = fh.read()
        compile(source, f, 'exec')
    except SyntaxError as e:
        rel = os.path.relpath(f, base)
        print(f'  SYNTAX ERROR: {rel}: {e}')
        py_errors += 1

if py_errors == 0:
    print(f'  All Python files pass!')
else:
    print(f'  {py_errors} syntax error(s) found')

# 2. JSON check (runtime files only)
print("\n[2] Runtime JSON Validity Check")
json_paths = [
    'core/v8/engine/builtin_knowledge.json',
    'core/v8/engine/character_profiles.json',
    'core/v8/engine/extended_knowledge.json',
    'core/v8/engine/optimized_settings.json',
    'core/v8/engine/plot_outlines.json',
    'core/v8/engine/world_settings.json',
    'core/v8/engine/writing_phrases.json',
    'core/v8/engine/writing_templates.json',
    'core/v8/engine/xuanhuan_trend_data.json',
    'core/v8/skill_manager/skill_descriptions.json',
]
json_errors = 0
for jp in json_paths:
    fp = os.path.join(base, jp)
    if not os.path.exists(fp):
        print(f'  MISSING: {jp}')
        json_errors += 1
        continue
    try:
        with open(fp, 'r', encoding='utf-8') as f:
            json.load(f)
        print(f'  OK: {jp}')
    except json.JSONDecodeError as e:
        print(f'  JSON ERROR: {jp}: {e}')
        json_errors += 1

if json_errors == 0:
    print(f'  All runtime JSON files valid!')

# 3. Core module import check
print("\n[3] Core Module Import Check")
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

import importlib
import_errors = 0
for modname in core_modules:
    try:
        importlib.import_module(modname)
        print(f'  OK: {modname}')
    except SyntaxError as e:
        print(f'  SYNTAX ERROR: {modname}: {e}')
        import_errors += 1
    except ModuleNotFoundError as e:
        print(f'  MISSING: {modname}: {e}')
        import_errors += 1
    except Exception as e:
        print(f'  ERROR: {modname}: {type(e).__name__}: {e}')
        import_errors += 1

if import_errors == 0:
    print(f'  All core modules import successfully!')

# Summary
print("\n" + "=" * 60)
total = py_errors + json_errors + import_errors
if total == 0:
    print("ALL CHECKS PASSED!")
else:
    print(f"TOTAL ISSUES: {total} (Python: {py_errors}, JSON: {json_errors}, Import: {import_errors})")
print("=" * 60)
