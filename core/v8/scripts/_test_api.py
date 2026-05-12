import urllib.request, json

BASE = 'http://localhost:8099'

def test(path, method='GET', data=None, timeout=15):
    url = BASE + path
    if data:
        req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type':'application/json'}, method=method)
    else:
        req = urllib.request.Request(url, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            result = json.loads(resp.read().decode('utf-8'))
            print(f'  OK {method} {path}')
            return result
    except Exception as e:
        print(f'  FAIL {method} {path} -> {e}')
        return None

print('=== 基础API测试 ===')
r1 = test('/api/health')
r2 = test('/api/models')
r3 = test('/api/config')
r4 = test('/api/options')

print()
print('=== 新增系统API测试 ===')
r5 = test('/api/rag/stats')
r6 = test('/api/style/list')
r7 = test('/api/strand/report')
r8 = test('/api/truth/new/status')
r9 = test('/api/pipeline/new/status')
r10 = test('/api/retention/report')
r11 = test('/api/fatigue/overall')
r12 = test('/api/gates/summary')

print()
print('=== POST API测试 ===')
r13 = test('/api/characters/states', 'POST', {}, 10)
r14 = test('/api/fragment/list', 'POST', {}, 10)
r15 = test('/api/quality/trend', 'POST', {}, 10)

passed = sum(1 for r in [r1,r2,r3,r4,r5,r6,r7,r8,r9,r10,r11,r12,r13,r14,r15] if r is not None)
failed = 15 - passed
print(f'\n=== 结果: {passed} 通过, {failed} 失败 ===')