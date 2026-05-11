import urllib.request, json, sys, time

data = json.dumps({
    "genre": "玄幻",
    "style": "热血爽文",
    "tone": "紧张刺激",
    "length": "中长篇",
    "theme": "逆境成长"
}).encode('utf-8')

print("Testing plot generation API...")
start = time.time()
req = urllib.request.Request(
    'http://localhost:8099/api/generate_plots',
    data=data,
    headers={'Content-Type': 'application/json'}
)

try:
    resp = urllib.request.urlopen(req, timeout=120)
    result = json.loads(resp.read())
    elapsed = time.time() - start
    print(f"Success: {result['success']} (took {elapsed:.1f}s)")
    print(f"Session: {result['session_id']}")
    print(f"Plots: {len(result['plots'])}")
    for p in result['plots']:
        print(f"  - {p['name']}: {p['tagline'][:50]}")
    if result.get('note'):
        print(f"Note: {result['note']}")
except urllib.error.HTTPError as e:
    elapsed = time.time() - start
    body = e.read().decode()
    print(f"HTTP {e.code} (took {elapsed:.1f}s): {body[:500]}")
except Exception as e:
    elapsed = time.time() - start
    print(f"Error (took {elapsed:.1f}s): {e}")
    sys.exit(1)
