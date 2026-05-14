import sys, os
sys.path.insert(0, r'd:\Trae CN\github\nwacs\nwacs\core\v8')
os.chdir(r'd:\Trae CN\github\nwacs\nwacs\core\v8')

from nwacs_server import app
import uvicorn
import threading, time, urllib.request, json

def test_request():
    time.sleep(2)
    try:
        data = json.dumps({
            'genre': '玄幻',
            'style': '热血爽文',
            'tone': '紧张刺激',
            'length': '中长篇',
            'theme': '逆境成长'
        }).encode('utf-8')
        req = urllib.request.Request(
            'http://127.0.0.1:8003/api/generate_plots',
            data=data,
            headers={'Content-Type': 'application/json'}
        )
        resp = urllib.request.urlopen(req, timeout=60)
        result = json.loads(resp.read())
        print(f'Response success: {result.get("success")}')
        print(f'Plots count: {len(result.get("plots", []))}')
    except Exception as e:
        import traceback
        print(f'Test error: {e}')
        traceback.print_exc()

t = threading.Thread(target=test_request, daemon=True)
t.start()

uvicorn.run(app, host='127.0.0.1', port=8003, log_level='info')
