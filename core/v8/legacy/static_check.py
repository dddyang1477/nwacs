"""
NWACS 全功能静态检查 - 不启动服务器，直接检查代码完整性
"""
import sys
import os
import json
import traceback

BASE = r'd:\Trae CN\github\nwacs\nwacs\core\v8'
sys.path.insert(0, BASE)
os.chdir(BASE)

REPORT_FILE = os.path.join(BASE, 'static_check_report.txt')
results = []
passed = 0
failed = 0

def check(msg, ok):
    global passed, failed
    status = "PASS" if ok else "FAIL"
    if ok:
        passed += 1
    else:
        failed += 1
    results.append(f"[{status}] {msg}")

# ============================================================
# 1. Check file existence
# ============================================================
results.append("=" * 60)
results.append("1. 文件完整性检查")
results.append("=" * 60)

required_files = [
    'nwacs_server_v3.py',
    'llm_interface.py',
    'character_name_engine.py',
    'enhanced_ai_detector.py',
    'genre_knowledge_base.json',
    'genre_profile_manager.py',
    'frontend/index.html',
    'engine/creative_engine.py',
    'engine/__init__.py',
]

for f in required_files:
    full = os.path.join(BASE, f)
    check(f"文件存在: {f}", os.path.exists(full))

# ============================================================
# 2. Check imports
# ============================================================
results.append("")
results.append("=" * 60)
results.append("2. 模块导入检查")
results.append("=" * 60)

# 2.1 llm_interface
try:
    from llm_interface import llm, GenerationParams, ModelProvider, ModelConfig
    check("导入 llm_interface (llm, GenerationParams, ModelProvider, ModelConfig)", True)
    check(f"  LLM provider={llm.config.provider.value}, model={llm.config.model_name}", True)
except Exception as e:
    check(f"导入 llm_interface 失败: {e}", False)

# 2.2 character_name_engine
try:
    from character_name_engine import CharacterNameEngine, CharacterProfile, NameResult, NameStyle, CharacterRole
    check("导入 character_name_engine (CharacterNameEngine, CharacterProfile, NameResult, NameStyle, CharacterRole)", True)
except Exception as e:
    check(f"导入 character_name_engine 失败: {e}", False)

# 2.3 enhanced_ai_detector
try:
    from enhanced_ai_detector import EnhancedAIDetector
    check("导入 enhanced_ai_detector (EnhancedAIDetector)", True)
except Exception as e:
    check(f"导入 enhanced_ai_detector 失败: {e}", False)

# 2.4 genre_profile_manager
try:
    from genre_profile_manager import GenreProfileManager, GenreType
    check("导入 genre_profile_manager (GenreProfileManager, GenreType)", True)
    check(f"  GenreType枚举: {[gt.label for gt in GenreType]}", True)
except Exception as e:
    check(f"导入 genre_profile_manager 失败: {e}", False)

# 2.5 creative_engine
try:
    from engine.creative_engine import SmartCreativeEngine
    check("导入 engine.creative_engine (SmartCreativeEngine)", True)
except Exception as e:
    check(f"导入 engine.creative_engine 失败: {e}", False)

# ============================================================
# 3. Check class methods
# ============================================================
results.append("")
results.append("=" * 60)
results.append("3. 类方法完整性检查")
results.append("=" * 60)

# 3.1 CharacterNameEngine methods
try:
    name_engine = CharacterNameEngine(llm)
    required_methods = [
        'generate_character_names',
        'generate_cast',
        'generate_title',
        'generate_organization_name',
        'generate_location_name',
        'generate_power_system_names',
        '_fallback_names',
    ]
    for m in required_methods:
        check(f"  CharacterNameEngine.{m}()", hasattr(name_engine, m) and callable(getattr(name_engine, m)))
except Exception as e:
    check(f"CharacterNameEngine 初始化失败: {e}", False)

# 3.2 EnhancedAIDetector methods
try:
    detector = EnhancedAIDetector()
    check(f"  EnhancedAIDetector.detect()", hasattr(detector, 'detect') and callable(detector.detect))
except Exception as e:
    check(f"EnhancedAIDetector 初始化失败: {e}", False)

# 3.3 SmartCreativeEngine methods
try:
    engine = SmartCreativeEngine()
    check(f"  SmartCreativeEngine.rewrite()", hasattr(engine, 'rewrite') and callable(engine.rewrite))
except Exception as e:
    check(f"SmartCreativeEngine 初始化失败: {e}", False)

# 3.4 GenreProfileManager methods
try:
    gpm = GenreProfileManager()
    check(f"  GenreProfileManager.set_genre()", hasattr(gpm, 'set_genre') and callable(gpm.set_genre))
    check(f"  GenreProfileManager.get_full_generation_context()", hasattr(gpm, 'get_full_generation_context') and callable(gpm.get_full_generation_context))
except Exception as e:
    check(f"GenreProfileManager 初始化失败: {e}", False)

# 3.5 LLM Interface methods
try:
    llm_methods = ['generate', 'generate_stream', 'update_config', 'save_config', 'get_available_models']
    for m in llm_methods:
        check(f"  LLMInterface.{m}()", hasattr(llm, m) and callable(getattr(llm, m)))
except Exception as e:
    check(f"LLM方法检查失败: {e}", False)

# ============================================================
# 4. Check knowledge base
# ============================================================
results.append("")
results.append("=" * 60)
results.append("4. 知识库完整性检查")
results.append("=" * 60)

kb_file = os.path.join(BASE, 'genre_knowledge_base.json')
if os.path.exists(kb_file):
    try:
        with open(kb_file, 'r', encoding='utf-8') as f:
            kb = json.load(f)
        check(f"知识库JSON解析成功", True)
        
        expected_genres = ['玄幻', '都市', '仙侠', '科幻', '悬疑', '言情', '历史', '游戏', '恐怖', '武侠']
        for g in expected_genres:
            if g in kb:
                schools = kb[g]
                if isinstance(schools, dict):
                    valid = {k:v for k,v in schools.items() if isinstance(v, dict) and 'error' not in v}
                    check(f"  {g}: {len(valid)}个流派数据完整", len(valid) > 0)
                else:
                    check(f"  {g}: 数据格式异常", False)
            else:
                check(f"  {g}: 缺失!", False)
    except Exception as e:
        check(f"知识库读取失败: {e}", False)
else:
    check("知识库文件不存在!", False)

# ============================================================
# 5. Check server API route mapping
# ============================================================
results.append("")
results.append("=" * 60)
results.append("5. API路由完整性检查")
results.append("=" * 60)

expected_get_routes = ['/api/health', '/api/models', '/api/config', '/api/options']
expected_post_routes = [
    '/api/generate_plots', '/api/select_plot', '/api/generate_chapter',
    '/api/detect_ai', '/api/rewrite', '/api/config',
    '/api/generate_names', '/api/generate_titles',
    '/api/generate_org_names', '/api/generate_power_system',
]

server_file = os.path.join(BASE, 'nwacs_server_v3.py')
if os.path.exists(server_file):
    with open(server_file, 'r', encoding='utf-8') as f:
        server_code = f.read()
    
    for route in expected_get_routes:
        check(f"  GET {route}", route in server_code)
    
    for route in expected_post_routes:
        check(f"  POST {route}", route in server_code)
    
    # Check handler methods exist
    handler_methods = [
        '_handle_generate_plots', '_handle_select_plot', '_handle_generate_chapter',
        '_handle_detect_ai', '_handle_rewrite', '_handle_update_config',
        '_handle_generate_names', '_handle_generate_titles',
        '_handle_generate_org_names', '_handle_generate_power_system',
    ]
    for m in handler_methods:
        check(f"  Handler {m}()", f'def {m}' in server_code)

# ============================================================
# 6. Check frontend API calls
# ============================================================
results.append("")
results.append("=" * 60)
results.append("6. 前端API调用检查")
results.append("=" * 60)

frontend_file = os.path.join(BASE, 'frontend', 'index.html')
if os.path.exists(frontend_file):
    with open(frontend_file, 'r', encoding='utf-8') as f:
        fe_code = f.read()
    
    fe_api_calls = [
        '/api/options', '/api/generate_plots', '/api/select_plot',
        '/api/generate_chapter', '/api/detect_ai', '/api/rewrite',
        '/api/config', '/api/generate_names',
    ]
    for api in fe_api_calls:
        check(f"  前端调用 {api}", api in fe_code)
    
    # Check frontend features
    fe_features = [
        ('多选类型', 'selectedGenres'),
        ('多选风格', 'selectedStyles'),
        ('多选基调', 'selectedTones'),
        ('多选流派', 'selectedSchools'),
        ('角色名字展示', 'name_meaning'),
        ('冲突类型展示', 'conflict_type'),
        ('角色弧光展示', 'character_change'),
        ('因果标记', 'marker-cause'),
        ('备注栏', 'notes-cell'),
        ('大纲渲染', 'renderOutline'),
        ('章节生成', 'generateChapter'),
        ('AI检测', 'detectAI'),
        ('导出功能', 'exportNovel'),
    ]
    for name, keyword in fe_features:
        check(f"  前端功能: {name}", keyword in fe_code)

# ============================================================
# 7. Check data flow consistency
# ============================================================
results.append("")
results.append("=" * 60)
results.append("7. 数据流一致性检查")
results.append("=" * 60)

# Check that generate_chapter receives outline data
check("章节生成传递outline数据", 'outline' in fe_code and 'generate_chapter' in fe_code)
check("章节生成传递previous_chapter_content", 'previous_chapter_content' in fe_code)
check("服务器接收outline参数", "'outline'" in server_code or '"outline"' in server_code)
check("服务器接收previous_chapter_content参数", 'previous_chapter_content' in server_code)

# Check character context injection
check("服务器注入角色上下文到章节prompt", 'character_context' in server_code)
check("服务器注入上一章内容到章节prompt", 'previous_context' in server_code)

# Check word count requirement
check("章节prompt包含4000字要求", '4000' in server_code)

# ============================================================
# Summary
# ============================================================
results.append("")
results.append("=" * 60)
results.append(f"静态检查完成: {passed}通过, {failed}失败")
results.append("=" * 60)

with open(REPORT_FILE, 'w', encoding='utf-8') as f:
    f.write('\n'.join(results))

print(f"报告已保存: {REPORT_FILE}")
print(f"通过: {passed}, 失败: {failed}")