import urllib.request, json, time

BASE = 'http://127.0.0.1:8099'

def api(path, method='GET', body=None):
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(BASE+path, data=data, method=method)
    req.add_header('Content-Type', 'application/json')
    return json.loads(urllib.request.urlopen(req, timeout=180))

print('=== Test 1: Multi-genre plot generation ===')
result = api('/api/generate_plots', 'POST', {
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
print(f'Plots generated: {len(result.get("plots",[]))}')
for p in result.get('plots', []):
    print(f'  - {p["name"]}: {p["tagline"][:60]}')

print()
print('=== Test 2: Multi-genre outline ===')
plot = result['plots'][0]
result2 = api('/api/select_plot', 'POST', {
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
o = result2.get('outline', {})
print(f'Title: {o.get("title")}')
print(f'Characters: {len(o.get("characters",[]))}')
for c in o.get('characters', []):
    print(f'  - {c["name"]} ({c["role"]}): {c.get("name_meaning","")[:40]}')
print(f'Acts: {len(o.get("acts",[]))}')
for act in o.get('acts', []):
    for ch in act.get('chapters', []):
        print(f'  Ch{ch["number"]} [{ch.get("plot_line_type","?")}] {ch["title"]}')

print()
print('=== ALL TESTS PASSED ===')
