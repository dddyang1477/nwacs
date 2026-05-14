"""深度功能调用审计 - 检查API端点、导入、方法一致性"""
import os, sys, re, ast

os.chdir(r'd:\Trae CN\github\nwacs\nwacs\core\v8')
sys.path.insert(0, os.getcwd())

print("=" * 60)
print("NWACS 深度功能调用审计")
print("=" * 60)

# 1. 检查服务器API端点与handler方法一致性
print("\n[1] API端点与Handler一致性检查...")
with open('nwacs_server_v3.py', 'r', encoding='utf-8') as f:
    server_code = f.read()

# 提取所有路由
get_routes = re.findall(r"path\s*==\s*'([^']+)'", server_code)
post_routes = re.findall(r"path\s*==\s*'([^']+)'", server_code)

# 提取所有handler方法
handler_methods = re.findall(r'def\s+(_handle_\w+)', server_code)

print(f"  GET路由: {len(get_routes)}")
for r in get_routes:
    print(f"    {r}")
print(f"  Handler方法: {len(handler_methods)}")
for m in handler_methods:
    print(f"    {m}")

# 检查每个POST路由是否有对应handler
post_only = [r for r in post_routes if r not in get_routes]
for route in post_only:
    expected_handler = '_handle_' + route.split('/')[-1].replace('-', '_')
    if expected_handler not in handler_methods:
        print(f"  ⚠ 缺少Handler: {route} -> {expected_handler}")

# 2. 检查模块导入一致性
print("\n[2] 模块导入一致性检查...")
modules_to_check = {
    'story_system.py': ['StorySystem'],
    'reviewer_agent.py': ['ReviewerAgent'],
    'quality_system.py': ['QualitySystem'],
    'project_memory.py': ['ProjectMemory'],
    'planning_system.py': ['PlanningSystem'],
    'enhanced_ai_detector.py': ['EnhancedAIDetector'],
    'llm_interface.py': ['llm', 'GenerationParams'],
    'character_name_engine.py': ['CharacterNameEngine', 'CharacterProfile'],
    'genre_profile_manager.py': ['GenreProfileManager', 'GenreType'],
}

for module_file, expected_classes in modules_to_check.items():
    if not os.path.exists(module_file):
        print(f"  ❌ 文件不存在: {module_file}")
        continue
    with open(module_file, 'r', encoding='utf-8') as f:
        content = f.read()
    for cls in expected_classes:
        if f'class {cls}' in content or f'{cls} =' in content:
            print(f"  ✅ {module_file} 导出 {cls}")
        else:
            print(f"  ⚠ {module_file} 可能未导出 {cls}")

# 3. 检查服务器中使用的模块是否都正确导入
print("\n[3] 服务器模块使用检查...")
server_imports = re.findall(r'from\s+(\w+)\s+import', server_code)
for imp in server_imports:
    module_file = imp + '.py'
    if os.path.exists(module_file):
        print(f"  ✅ from {imp} import ... -> {module_file} 存在")
    else:
        print(f"  ⚠ from {imp} import ... -> {module_file} 不存在")

# 4. 检查to_dict方法一致性
print("\n[4] to_dict/asdict方法检查...")
for module_file in ['story_system.py', 'reviewer_agent.py', 'quality_system.py', 'project_memory.py', 'planning_system.py']:
    if not os.path.exists(module_file):
        continue
    with open(module_file, 'r', encoding='utf-8') as f:
        content = f.read()
    # 检查dataclass是否有to_dict
    dataclasses = re.findall(r'class\s+(\w+)\s*[:\(]', content)
    has_to_dict = 'def to_dict' in content
    has_asdict = 'from dataclasses import' in content and 'asdict' in content
    print(f"  {module_file}: dataclasses={dataclasses}, to_dict={'✅' if has_to_dict else '⚠'}")

# 5. 检查前端API调用与后端端点匹配
print("\n[5] 前端API调用检查...")
frontend_path = os.path.join('frontend', 'index.html')
if os.path.exists(frontend_path):
    with open(frontend_path, 'r', encoding='utf-8') as f:
        frontend_code = f.read()
    frontend_apis = re.findall(r"api\('([^']+)'", frontend_code)
    frontend_apis += re.findall(r'api\("([^"]+)"', frontend_code)
    frontend_apis = list(set(frontend_apis))
    
    all_server_routes = list(set(get_routes + post_routes))
    for api_path in frontend_apis:
        if api_path in all_server_routes:
            print(f"  ✅ 前端 {api_path} -> 后端匹配")
        else:
            print(f"  ⚠ 前端 {api_path} -> 后端无匹配路由")

print("\n" + "=" * 60)
print("审计完成")
print("=" * 60)