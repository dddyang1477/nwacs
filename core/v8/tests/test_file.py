import urllib.request, json

BASE = 'http://127.0.0.1:8099'

body = json.dumps({
    'genres': ['玄幻', '仙侠'],
    'styles': ['热血爽文'],
    'tones': ['紧张刺激'],
    'length': '中长篇',
    'schools': ['sign_in'],
    'school_names': ['签到流'],
    'theme': '逆境成长'
}).encode('utf-8')

req = urllib.request.Request(BASE + '/api/generate_plots', data=body, method='POST')
req.add_header('Content-Type', 'application/json')

try:
    r = json.loads(urllib.request.urlopen(req, timeout=180).read())
    with open('test_result.txt', 'w', encoding='utf-8') as f:
        f.write('Plots: ' + str(len(r.get('plots', []))) + '\n')
        for p in r.get('plots', []):
            f.write(' - ' + p['name'] + ': ' + p['tagline'][:50] + '\n')
        f.write('MULTI-SELECT API OK!\n')
except Exception as e:
    with open('test_result.txt', 'w', encoding='utf-8') as f:
        f.write('ERROR: ' + str(e) + '\n')
