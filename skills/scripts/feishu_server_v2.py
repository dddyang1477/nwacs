#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 飞书指令服务器 v2.0
修复版 - 支持飞书实际消息格式
"""
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
import sys

sys.stdout.reconfigure(encoding='utf-8')

PORT = 8088

print("="*70)
print("NWACS Feishu Command Server v2.0")
print("="*70)
print(f"Port: {PORT}")
print("Ready!")
print()

class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {format % args}", flush=True)

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        html = """<html><head><meta charset="utf-8"><title>NWACS</title></head>
        <body><h1>NWACS Server Running</h1>
        <p>Time: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</p>
        <p>Status: Ready for Feishu commands</p>
        <h3>Available:</h3>
        <ul>
            <li>status - System status</li>
            <li>learn - Start learning</li>
            <li>report - Send report</li>
            <li>help - Help</li>
        </ul>
        </body></html>"""
        self.wfile.write(html.encode('utf-8'))
        self.log_message("GET from %s", self.client_address[0])

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        self.log_message("POST: %s", body[:200])

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        response = {"code": 0, "msg": "ok"}
        self.wfile.write(json.dumps(response).encode())

        # Process message
        try:
            data = json.loads(body)
            self.process_feishu_message(data)
        except Exception as e:
            self.log_message("Error: %s", str(e))

    def process_feishu_message(self, data):
        """处理飞书消息"""
        # 飞书消息格式
        event = data.get('event', {})
        message = event.get('text', '') or data.get('text', '')
        sender = event.get('sender', {}).get('sender_id', {}).get('open_id', 'unknown')

        self.log_message("User: %s", sender)
        self.log_message("Message: %s", message)

        # 提取命令
        cmd = message.strip().lower()

        if cmd in ['status', '状态']:
            self.send_status()
        elif cmd in ['learn', '学习']:
            self.start_learning()
        elif cmd in ['report', '报告']:
            self.send_report()
        elif cmd in ['help', '帮助']:
            self.send_help()
        elif cmd in ['stats', '统计']:
            self.send_stats()
        else:
            self.send_unknown(cmd)

    def send_status(self):
        """发送状态"""
        self.log_message("Sending status...")
        # 这里会调用飞书发送响应
        try:
            from core.feishu.nwacs_feishu import NWACSFeishuIntegration
            integration = NWACSFeishuIntegration()
            integration.send_custom_message("📊 NWACS Status",
                "System: Running\nVersion: v7.0\nKnowledge: 35 bases\nStatus: OK")
        except Exception as e:
            self.log_message("Send failed: %s", e)

    def start_learning(self):
        """开始学习"""
        self.log_message("Starting learning...")
        try:
            from core.comprehensive_learning import AutoLearningSystem
            learning = AutoLearningSystem()
            learning.run_learning_cycle(update_skills=True)
            self.send_to_feishu("✅ Learning completed!")
        except Exception as e:
            self.log_message("Learning error: %s", e)
            self.send_to_feishu(f"❌ Error: {e}")

    def send_report(self):
        """发送报告"""
        self.log_message("Sending report...")
        self.send_to_feishu("📄 Report feature coming soon")

    def send_help(self):
        """发送帮助"""
        help_text = """📖 NWACS Commands:
1. status - System status
2. learn - Start learning
3. report - Send report
4. stats - Learning stats
5. help - This help"""
        self.send_to_feishu(help_text)

    def send_stats(self):
        """发送统计"""
        stats = """📈 NWACS Stats:
Knowledge: 35 bases
Skills: 28 (v7.0/v8.0)
Status: Running"""
        self.send_to_feishu(stats)

    def send_unknown(self, cmd):
        """未知命令"""
        self.send_to_feishu(f"Unknown: {cmd}\nSend 'help' for commands")

    def send_to_feishu(self, message):
        """发送消息到飞书"""
        try:
            from core.feishu.nwacs_feishu import NWACSFeishuIntegration
            integration = NWACSFeishuIntegration()
            integration.send_custom_message("📨 NWACS Response", message)
            self.log_message("Sent to Feishu: %s", message[:50])
        except Exception as e:
            self.log_message("Send to Feishu failed: %s", e)

print("Server starting on port %s..." % PORT)
try:
    server = HTTPServer(('0.0.0.0', PORT), Handler)
    print(f"✅ Server ready! http://localhost:{PORT}")
    print("Press Ctrl+C to stop")
    server.serve_forever()
except KeyboardInterrupt:
    print("\nServer stopped")
except Exception as e:
    print(f"Error: {e}")
