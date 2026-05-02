#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 飞书调试服务器 v1.0
超级简单版 - 只打印所有收到的消息
"""
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime

PORT = 8088

print("="*70)
print("NWACS Feishu Debug Server v1.0")
print("="*70)
print(f"Port: {PORT}")
print("This server will PRINT ALL RECEIVED MESSAGES!")
print()
print("Check browser: http://localhost:8088")
print()

class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {format % args}", flush=True)

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        html = """<html><head><meta charset="utf-8"><title>NWACS DEBUG</title></head>
        <body><h1>NWACS DEBUG SERVER RUNNING!</h1>
        <p>Time: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</p>
        <p>This server will print ALL POST requests to console.</p>
        <p>Check your terminal to see messages from Feishu!</p>
        </body></html>"""
        self.wfile.write(html.encode('utf-8'))
        print(f"GET from {self.client_address[0]}")

    def do_POST(self):
        print()
        print("="*60)
        print(f"RECEIVED POST at {datetime.now().strftime('%H:%M:%S')}")
        print("="*60)

        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')

        print(f"RAW BODY: {repr(body)}")
        print(f"LENGTH: {content_length}")

        try:
            data = json.loads(body)
            print(f"PARSED JSON: {json.dumps(data, indent=2, ensure_ascii=False)}")
        except Exception as e:
            print(f"JSON PARSE ERROR: {e}")

        print()

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        response = {"code": 0, "msg": "debug server"}
        self.wfile.write(json.dumps(response).encode())

        print(f"RESPONDED: {json.dumps(response)}")
        print("="*60)

print("DEBUG server starting on port %s..." % PORT)
try:
    server = HTTPServer(('0.0.0.0', PORT), Handler)
    print(f"✅ DEBUG server ready! http://localhost:{PORT}")
    print("All POST requests will be PRINTED to console!")
    print("Press Ctrl+C to stop")
    server.serve_forever()
except KeyboardInterrupt:
    print("\nServer stopped")
except Exception as e:
    print(f"Error: {e}")
