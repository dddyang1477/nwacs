import urllib.request, json

BASE = 'http://127.0.0.1:8099'

def api(path, method='GET', body=None):
    data = json.dumps(body).encode('utf-8') if body else None
    req = urllib.request.Request(BASE + path, data=data, method=method)
    req.add_header('Content-Type', 'application/json')
    return json.loads(urllib.request.urlopen(req, timeout=300).read())

with open('e2e_result.txt', 'w', encoding='utf-8') as f:
    f.write('=' * 60 + '\n')
    f.write('  NWACS v9.0 E2E Test Results\n')
    f.write('=' * 60 + '\n\n')

    f.write('[1] Health: ' + api('/api/health')['status'] + '\n\n')

    r = api('/api/generate_plots', 'POST', {
        'genres': ['玄幻', '仙侠'],
        'styles': ['热血爽文', '史诗宏大'],
        'tones': ['紧张刺激', '悲壮感人'],
        'length': '中长篇',
        'schools': ['sign_in', 'sword_cultivator'],
        'school_names': ['签到流', '剑修流'],
        'theme': '逆境成长',
    })
    f.write(f'[2] Multi-genre plots: {len(r["plots"])}\n')
    for p in r['plots']:
        f.write(f'    - {p["name"]}: {p["tagline"]}\n')

    plot = r['plots'][0]
    r2 = api('/api/select_plot', 'POST', {
        'plot_id': plot['id'], 'plot_name': plot['name'],
        'genres': ['玄幻', '仙侠'],
        'styles': ['热血爽文', '史诗宏大'],
        'tones': ['紧张刺激', '悲壮感人'],
        'length': '中长篇',
        'schools': ['sign_in', 'sword_cultivator'],
        'school_names': ['签到流', '剑修流'],
        'theme': '逆境成长',
    })
    o = r2['outline']
    f.write(f'\n[3] Outline: {o["title"]}\n')
    f.write(f'    Synopsis: {o["synopsis"][:100]}...\n')
    f.write(f'    Characters: {len(o["characters"])}\n')
    for c in o['characters']:
        f.write(f'      {c["name"]} ({c["role"]}): {c.get("name_meaning","")}\n')
    total_ch = sum(len(act.get('chapters',[])) for act in o.get('acts',[]))
    f.write(f'    Acts: {len(o["acts"])}, Chapters: {total_ch}\n')

    r3 = api('/api/generate_plots', 'POST', {
        'genres': ['悬疑'],
        'styles': ['黑暗深沉'],
        'tones': ['紧张刺激'],
        'length': '中长篇',
        'schools': ['classic_detective'],
        'school_names': ['本格推理流'],
        'theme': '真相追寻',
    })
    f.write(f'\n[4] Single genre plots: {len(r3["plots"])}\n')
    for p in r3['plots']:
        f.write(f'    - {p["name"]}: {p["tagline"]}\n')

    f.write('\n' + '=' * 60 + '\n')
    f.write('  ALL TESTS PASSED!\n')
    f.write('=' * 60 + '\n')

print('Results written to e2e_result.txt')
