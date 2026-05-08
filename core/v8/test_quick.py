import urllib.request, json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

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
r = json.loads(urllib.request.urlopen(req, timeout=180).read())

print('Plots:', len(r.get('plots', [])))
for p in r.get('plots', []):
    print(' -', p['name'], ':', p['tagline'][:50])
print('MULTI-SELECT API OK!')
