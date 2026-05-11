import py_compile, os, sys

files_to_check = [
    'nwacs_server_v3.py',
    'story_system.py',
    'reviewer_agent.py',
    'quality_system.py',
    'project_memory.py',
    'planning_system.py',
    'enhanced_ai_detector.py',
    'llm_interface.py',
    'character_name_engine.py',
    'genre_profile_manager.py',
]

errors = []
for f in files_to_check:
    if os.path.exists(f):
        try:
            py_compile.compile(f, doraise=True)
            print(f'  OK: {f}')
        except py_compile.PyCompileError as e:
            errors.append(f)
            print(f'  ERROR: {f} - {e}')
    else:
        print(f'  MISSING: {f}')

print(f'\nTotal: {len(files_to_check)} files checked, {len(errors)} errors')