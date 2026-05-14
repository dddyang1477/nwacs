#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MCP Server for Novel Creation - STDIN/STDOUT Protocol
小说创作MCP服务器 - 基于标准输入输出协议
"""

import json
import os
import sys

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from novel_writer import NovelWriter

class NovelCreationMCP:
    """小说创作MCP服务"""
    
    def __init__(self):
        self.writer = NovelWriter()
        # 发送初始化完成信号
        self.send_response({"status": "ready", "message": "NovelCreation MCP Server ready"})
    
    def send_response(self, data):
        """发送响应"""
        response = json.dumps(data, ensure_ascii=False)
        print(response)
        sys.stdout.flush()
    
    def handle_request(self, request):
        """处理请求"""
        try:
            action = request.get("action")
            
            if action == "list_functions":
                return self.list_functions()
            
            elif action == "execute":
                name = request.get("name")
                arguments = request.get("arguments", {})
                return self.execute_function(name, arguments)
            
            elif action == "describe":
                return self.describe()
            
            else:
                return {"status": "error", "message": f"Unknown action: {action}"}
        
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def list_functions(self):
        """列出可用函数"""
        return {
            "status": "success",
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
    
    def describe(self):
        """描述服务"""
        return {
            "status": "success",
            "name": "novel_creation",
            "description": "小说创作工具 - 支持大纲生成、章节创作、文本润色、小说保存",
            "version": "1.0.0"
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
    
    def run(self):
        """运行服务主循环"""
        try:
            for line in sys.stdin:
                line = line.strip()
                if not line:
                    continue
                
                try:
                    request = json.loads(line)
                    response = self.handle_request(request)
                    self.send_response(response)
                except json.JSONDecodeError:
                    self.send_response({"status": "error", "message": "Invalid JSON"})
        
        except KeyboardInterrupt:
            pass
        except Exception as e:
            self.send_response({"status": "error", "message": str(e)})

if __name__ == "__main__":
    mcp = NovelCreationMCP()
    mcp.run()