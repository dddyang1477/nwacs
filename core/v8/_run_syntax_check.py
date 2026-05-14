import py_compile, os, sys

files = [
    'nwacs_server_v3.py', 'story_system.py', 'reviewer_agent.py',
    'quality_system.py', 'project_memory.py', 'planning_system.py',
    'llm_interface.py', 'character_name_engine.py', 'genre_profile_manager.py',
    'fatigue_detector.py', 'rag_engine.py', 'retention_system.py',
    'truth_file_manager.py', 'style_fingerprint.py', 'strand_weave.py',
    'writing_pipeline.py', 'ai_humanizer.py'
]

os.chdir(r'd:\Trae CN\github\nwacs\nwacs\core\v8')
results = []
for f in files:
    if os.path.exists(f):
        try:
            py_compile.compile(f, doraise=True)
            results.append(f'OK: {f}')
        except py_compile.PyCompileError as e:
            results.append(f'ERROR: {f} - {e}')
    else:
        results.append(f'MISSING: {f}')

with open('_syntax_result.txt', 'w', encoding='utf-8') as out:
    out.write('\n'.join(results))
print('\n'.join(results))