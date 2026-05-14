#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MCP Server for Novel Creation
小说创作MCP服务器实现
"""

import argparse
import json
import os
import sys
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from novel_writer import NovelWriter

class NovelWriterHandler(BaseHTTPRequestHandler):
    """HTTP请求处理器"""
    
    def __init__(self, *args, **kwargs):
        self.writer = NovelWriter()
        super().__init__(*args, **kwargs)
    
    def log_message(self, format, *args):
        """自定义日志"""
        print(f"[MCP] {format % args}")
    
    def send_json_response(self, data):
        """发送JSON响应"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
    
    def send_error_response(self, message):
        """发送错误响应"""
        self.send_response(500)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "error", "message": message}).encode('utf-8'))
    
    def do_POST(self):
        """处理POST请求"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            request = json.loads(body)
            
            action = request.get("action")
            
            if action == "list_functions":
                response = self.list_functions()
            elif action == "execute":
                name = request.get("name")
                arguments = request.get("arguments", {})
                response = self.execute_function(name, arguments)
            else:
                response = {"status": "error", "message": f"Unknown action: {action}"}
            
            self.send_json_response(response)
        
        except json.JSONDecodeError:
            self.send_error_response("Invalid JSON")
        except Exception as e:
            self.send_error_response(str(e))
    
    def do_GET(self):
        """处理GET请求"""
        if self.path == "/health":
            self.send_json_response({"status": "healthy"})
        elif self.path == "/functions":
            self.send_json_response(self.list_functions())
        else:
            self.send_error_response("Not found")
    
    def list_functions(self):
        """列出可用函数"""
        return {
            "functions": [
                {
                    "name": "generate_outline",
                    "description": "生成小说大纲",
                    "parameters": {
                        "genre": {"type": "string", "description": "小说类型", "required": True},
                        "theme": {"type": "string", "description": "小说主题", "required": True},
                        "length": {"type": "string", "description": "篇幅（短篇/中篇/长篇）", "required": False}
                    }
                },
                {
                    "name": "generate_chapter",
                    "description": "生成章节内容",
                    "parameters": {
                        "chapter_info": {"type": "object", "description": "章节信息", "required": True},
                        "outline": {"type": "object", "description": "小说大纲", "required": True}
                    }
                },
                {
                    "name": "polish_text",
                    "description": "润色文本",
                    "parameters": {
                        "text": {"type": "string", "description": "待润色文本", "required": True},
                        "style": {"type": "string", "description": "润色风格（流畅/简洁/华丽/古风）", "required": False}
                    }
                },
                {
                    "name": "save_novel",
                    "description": "保存小说",
                    "parameters": {
                        "novel_data": {"type": "object", "description": "小说数据", "required": True},
                        "filename": {"type": "string", "description": "文件名", "required": False}
                    }
                }
            ]
        }
    
    def execute_function(self, name: str, arguments: dict):
        """执行函数"""
        try:
            if name == "generate_outline":
                genre = arguments.get("genre", "玄幻修仙")
                theme = arguments.get("theme", "逆袭")
                length = arguments.get("length", "长篇")
                result = self.writer.generate_outline(genre, theme, length)
                return {"status": "success", "result": result}
            
            elif name == "generate_chapter":
                chapter_info = arguments.get("chapter_info", {"chapter": 1, "title": "第一章", "content": "开端"})
                outline = arguments.get("outline", {})
                result = self.writer.generate_chapter(chapter_info, outline)
                return {"status": "success", "result": result}
            
            elif name == "polish_text":
                text = arguments.get("text", "")
                style = arguments.get("style", "流畅")
                result = self.writer.polish_text(text, style)
                return {"status": "success", "result": result}
            
            elif name == "save_novel":
                novel_data = arguments.get("novel_data", {})
                filename = arguments.get("filename", None)
                result = self.writer.save_novel(novel_data, filename)
                return {"status": "success" if result.get("success") else "error", "result": result}
            
            else:
                return {"status": "error", "message": f"Unknown function: {name}"}
        
        except Exception as e:
            return {"status": "error", "message": str(e)}

def run_server(host: str = "127.0.0.1", port: int = 8888):
    """启动服务器"""
    server_address = (host, port)
    httpd = HTTPServer(server_address, NovelWriterHandler)
    print(f"[INFO] NovelCreation MCP Server running on http://{host}:{port}")
    print(f"[INFO] Health check: http://{host}:{port}/health")
    print(f"[INFO] Functions list: http://{host}:{port}/functions")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[INFO] Server stopping...")
        httpd.server_close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Novel Creation MCP Server")
    parser.add_argument("--host", default="127.0.0.1", help="Host address")
    parser.add_argument("--port", type=int, default=8888, help="Port number")
    args = parser.parse_args()
    
    run_server(args.host, args.port)