import urllib.request, json

BASE = 'http://127.0.0.1:8099'

def api(path, method='GET', body=None):
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(BASE+path, data=data, method=method)
    req.add_header('Content-Type', 'application/json')
    return json.loads(urllib.request.urlopen(req, timeout=120))

print('Testing plot generation with流派...')
result = api('/api/generate_plots', 'POST', {
    'genre': '玄幻', 'style': '热血爽文', 'tone': '紧张刺激',
    'length': '中长篇', 'theme': '逆境成长',
    'school': 'sign_in', 'school_name': '签到流'
})
print(f'Plots: {len(result["plots"])}')
for p in result['plots']:
    print(f'  - {p["name"]}: {p["tagline"][:50]}')

print()
print('Testing outline generation with流派...')
plot = result['plots'][0]
result2 = api('/api/select_plot', 'POST', {
    'plot_id': plot['id'], 'plot_name': plot['name'],
    'genre': '玄幻', 'style': '热血爽文', 'tone': '紧张刺激',
    'length': '中长篇', 'theme': '逆境成长',
    'school': 'sign_in', 'school_name': '签到流'
})
o = result2['outline']
print(f'Title: {o.get("title")}')
print(f'Characters: {len(o.get("characters", []))}')
for c in o.get('characters', []):
    print(f'  - {c["name"]} ({c["role"]}): {c.get("name_meaning", "")[:40]}')
print(f'Plot lines: main={o.get("plot_lines",{}).get("main_line","")[:50]}')
print(f'Sub lines: {len(o.get("plot_lines",{}).get("sub_lines",[]))}')
print(f'CE chains: {len(o.get("plot_lines",{}).get("cause_effect_chains",[]))}')
print(f'Acts: {len(o.get("acts",[]))}')
for act in o.get('acts', []):
    for ch in act.get('chapters', []):
        notes = ch.get('notes', '')
        plt = ch.get('plot_line_type', '?')
        ce = ch.get('cause_effect', {})
        print(f'  Ch{ch["number"]} [{plt}] {ch["title"]} | cause={ce.get("caused_by","?")[:20]} -> effect={ce.get("leads_to","?")[:20]} | notes="{notes}"')
print()
print('ALL TESTS PASSED!')
