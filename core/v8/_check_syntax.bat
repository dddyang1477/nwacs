@echo off
cd /d "d:\Trae CN\github\nwacs\nwacs\core\v8"
python -c "import py_compile; py_compile.compile('nwacs_server_v3.py', doraise=True); print('nwacs_server_v3.py: OK')" 2>&1
python -c "import py_compile; py_compile.compile('story_system.py', doraise=True); print('story_system.py: OK')" 2>&1
python -c "import py_compile; py_compile.compile('reviewer_agent.py', doraise=True); print('reviewer_agent.py: OK')" 2>&1
python -c "import py_compile; py_compile.compile('quality_system.py', doraise=True); print('quality_system.py: OK')" 2>&1
python -c "import py_compile; py_compile.compile('project_memory.py', doraise=True); print('project_memory.py: OK')" 2>&1
python -c "import py_compile; py_compile.compile('planning_system.py', doraise=True); print('planning_system.py: OK')" 2>&1
python -c "import py_compile; py_compile.compile('llm_interface.py', doraise=True); print('llm_interface.py: OK')" 2>&1
python -c "import py_compile; py_compile.compile('character_name_engine.py', doraise=True); print('character_name_engine.py: OK')" 2>&1
python -c "import py_compile; py_compile.compile('genre_profile_manager.py', doraise=True); print('genre_profile_manager.py: OK')" 2>&1
python -c "import py_compile; py_compile.compile('fatigue_detector.py', doraise=True); print('fatigue_detector.py: OK')" 2>&1
python -c "import py_compile; py_compile.compile('rag_engine.py', doraise=True); print('rag_engine.py: OK')" 2>&1
python -c "import py_compile; py_compile.compile('retention_system.py', doraise=True); print('retention_system.py: OK')" 2>&1
python -c "import py_compile; py_compile.compile('truth_file_manager.py', doraise=True); print('truth_file_manager.py: OK')" 2>&1
python -c "import py_compile; py_compile.compile('style_fingerprint.py', doraise=True); print('style_fingerprint.py: OK')" 2>&1
python -c "import py_compile; py_compile.compile('strand_weave.py', doraise=True); print('strand_weave.py: OK')" 2>&1
python -c "import py_compile; py_compile.compile('writing_pipeline.py', doraise=True); print('writing_pipeline.py: OK')" 2>&1
python -c "import py_compile; py_compile.compile('ai_humanizer.py', doraise=True); print('ai_humanizer.py: OK')" 2>&1
echo Done
pause