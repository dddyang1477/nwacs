import urllib.request, json, sys

BASE = 'http://localhost:8099'

def test(path, method='GET', data=None):
    url = BASE + path
    if data:
        req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type':'application/json'}, method=method)
    else:
        req = urllib.request.Request(url, method=method)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read().decode('utf-8'))
            print(f'  OK {method} {path}')
            return result
    except Exception as e:
        print(f'  FAIL {method} {path} -> {e}')
        return None

passed = 0
failed = 0

def check(name, result):
    global passed, failed
    if result is not None:
        passed += 1
    else:
        failed += 1

print('=== 1. 基础API测试 ===')
check('models', test('/api/models'))
check('config', test('/api/config'))
check('options', test('/api/options'))

print('\n=== 2. 名字生成测试 ===')
check('generate_names', test('/api/generate_names', 'POST', {'genre': '玄幻', 'count': 6, 'type': 'protagonist'}))
check('generate_names_batch', test('/api/generate_names_batch', 'POST', {'genre': '玄幻', 'count': 5, 'type': 'protagonist'}))

print('\n=== 3. 剧情生成测试 ===')
check('generate_plots', test('/api/generate_plots', 'POST', {'genre': '玄幻', 'school': 'xianxia', 'prompt': '测试剧情'}))

print('\n=== 4. 质量系统测试 ===')
check('quality_trend', test('/api/quality/trend', 'POST', {'last_n': 5}))
check('quality_checklist', test('/api/quality/checklist', 'POST', {'action': 'evaluate', 'text': '测试文本', 'use_llm': False}))

print('\n=== 5. 记忆系统测试 ===')
check('memory_stats', test('/api/memory/stats'))

print('\n=== 6. 规划系统测试 ===')
check('planning_timeline', test('/api/planning/timeline'))

print('\n=== 7. 追读力系统测试 ===')
check('retention_report', test('/api/retention/report', 'GET'))

print('\n=== 8. 词汇疲劳检测测试 ===')
check('fatigue_analyze', test('/api/fatigue/analyze', 'POST', {'chapter': 1, 'content': '测试内容'}))

print('\n=== 9. 审查关卡测试 ===')
check('gates_evaluate', test('/api/gates/evaluate', 'POST', {'chapter': 1, 'content': '测试内容', 'target_word_count': 3000}))

print('\n=== 10. RAG引擎测试 ===')
check('rag_search', test('/api/rag/search', 'POST', {'query': '测试', 'top_k': 5}))
check('rag_stats', test('/api/rag/stats', 'GET'))

print('\n=== 11. 新系统测试 ===')
check('style_list', test('/api/style/list', 'GET'))
check('strand_report', test('/api/strand/report', 'GET'))
check('truth_new_status', test('/api/truth/new/status', 'GET'))
check('pipeline_new_status', test('/api/pipeline/new/status', 'GET'))

print('\n=== 12. 片段管理测试 ===')
check('fragment_save', test('/api/fragment/save', 'POST', {'chapter': 1, 'content': '测试内容', 'label': 'v1'}))
check('fragment_list', test('/api/fragment/list', 'POST', {'chapter': 1}))

print('\n=== 13. 角色状态测试 ===')
check('char_states', test('/api/characters/states', 'POST', {}))

print('\n=== 14. 文风指纹测试 ===')
check('style_analyze', test('/api/style/analyze', 'POST', {'text': '测试文本内容', 'label': 'test'}))

print('\n=== 15. 节奏编织测试 ===')
check('strand_analyze', test('/api/strand/analyze', 'POST', {'chapter': 1, 'content': '测试内容'}))

print(f'\n{"="*40}')
print(f'测试结果: {passed} 通过, {failed} 失败')
if failed > 0:
    sys.exit(1)
else:
    print('所有API测试通过!')