import urllib.request, json, time

BASE = 'http://127.0.0.1:8099'

def api(path, method='GET', body=None):
    data = json.dumps(body).encode('utf-8') if body else None
    req = urllib.request.Request(BASE + path, data=data, method=method)
    req.add_header('Content-Type', 'application/json')
    return json.loads(urllib.request.urlopen(req, timeout=300).read())

results = []

print('=' * 60)
print('  NWACS v9.0 端到端测试 - 多选功能')
print('=' * 60)

print('\n[1/4] 健康检查...')
r = api('/api/health')
print(f'  Status: {r["status"]}')
results.append(r['status'] == 'ok')

print('\n[2/4] 多选剧情生成 (玄幻+仙侠, 签到流+剑修流)...')
r = api('/api/generate_plots', 'POST', {
    'genres': ['玄幻', '仙侠'],
    'styles': ['热血爽文', '史诗宏大'],
    'tones': ['紧张刺激', '悲壮感人'],
    'length': '中长篇',
    'schools': ['sign_in', 'sword_cultivator'],
    'school_names': ['签到流', '剑修流'],
    'theme': '逆境成长',
    'protagonist': '穿越者',
    'extra_requirements': '融合签到流和剑修流的特点'
})
plots = r.get('plots', [])
print(f'  Plots: {len(plots)}')
for p in plots:
    print(f'    - {p["name"]}: {p["tagline"][:60]}')
results.append(len(plots) >= 3)

print('\n[3/4] 大纲生成...')
if plots:
    plot = plots[0]
    r = api('/api/select_plot', 'POST', {
        'plot_id': plot['id'],
        'plot_name': plot['name'],
        'genres': ['玄幻', '仙侠'],
        'styles': ['热血爽文', '史诗宏大'],
        'tones': ['紧张刺激', '悲壮感人'],
        'length': '中长篇',
        'schools': ['sign_in', 'sword_cultivator'],
        'school_names': ['签到流', '剑修流'],
        'theme': '逆境成长',
    })
    o = r.get('outline', {})
    print(f'  Title: {o.get("title", "N/A")}')
    chars = o.get('characters', [])
    print(f'  Characters: {len(chars)}')
    for c in chars:
        print(f'    - {c["name"]} ({c["role"]}): {c.get("name_meaning", "")[:40]}')
    acts = o.get('acts', [])
    total_ch = sum(len(act.get('chapters', [])) for act in acts)
    print(f'  Acts: {len(acts)}, Chapters: {total_ch}')
    results.append(len(chars) >= 3 and total_ch >= 8)

print('\n[4/4] 单类型测试 (悬疑, 本格推理流)...')
r = api('/api/generate_plots', 'POST', {
    'genres': ['悬疑'],
    'styles': ['黑暗深沉'],
    'tones': ['紧张刺激'],
    'length': '中长篇',
    'schools': ['classic_detective'],
    'school_names': ['本格推理流'],
    'theme': '真相追寻',
})
plots2 = r.get('plots', [])
print(f'  Plots: {len(plots2)}')
for p in plots2:
    print(f'    - {p["name"]}: {p["tagline"][:60]}')
results.append(len(plots2) >= 3)

print('\n' + '=' * 60)
passed = sum(results)
total = len(results)
print(f'  结果: {passed}/{total} 通过')
if passed == total:
    print('  ALL TESTS PASSED!')
else:
    print('  SOME TESTS FAILED!')
print('=' * 60)
