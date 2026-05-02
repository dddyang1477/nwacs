#!/usr/bin/env python3
import sys
import time

print("="*60, flush=True)
print("SERVER TEST", flush=True)
print("="*60, flush=True)
print(f"Python: {sys.version}", flush=True)
print(f"Port: 8088", flush=True)
print("", flush=True)

# Test server
try:
    from http.server import HTTPServer, BaseHTTPRequestHandler
    
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, fmt, *args):
            print(f"REQUEST: {args[0]}", flush=True)
        
        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'OK')
    
    server = HTTPServer(('0.0.0.0', 8088), Handler)
    print("✅ Server started!", flush=True)
    print("Visit: http://localhost:8088", flush=True)
    print("Press Ctrl+C to stop", flush=True)
    print("", flush=True)
    server.serve_forever()
    
except KeyboardInterrupt:
    print("\nServer stopped", flush=True)
except Exception as e:
    print(f"❌ Error: {e}", flush=True)
