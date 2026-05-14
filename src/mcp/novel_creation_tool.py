#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Novel Creation Tool for Trae CN
小说创作工具 - 直接函数调用方式
"""

import json
import os
import sys

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from novel_writer import NovelWriter

class NovelCreationTool:
    """小说创作工具类"""
    
    def __init__(self):
        self.writer = NovelWriter()
        print("[INFO] NovelCreation Tool initialized")
    
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
    
    def execute(self, function_name, **kwargs):
        """执行函数"""
        try:
            if function_name == "generate_outline":
                genre = kwargs.get("genre", "玄幻修仙")
                theme = kwargs.get("theme", "逆袭")
                length = kwargs.get("length", "长篇")
                result = self.writer.generate_outline(genre, theme, length)
                return {"status": "success", "result": result}
            
            elif function_name == "generate_chapter":
                chapter_info = kwargs.get("chapter_info", {"chapter": 1, "title": "第一章", "content": "开端"})
                outline = kwargs.get("outline", {})
                result = self.writer.generate_chapter(chapter_info, outline)
                return {"status": "success", "result": result}
            
            elif function_name == "polish_text":
                text = kwargs.get("text", "")
                style = kwargs.get("style", "流畅")
                result = self.writer.polish_text(text, style)
                return {"status": "success", "result": result}
            
            elif function_name == "save_novel":
                novel_data = kwargs.get("novel_data", {})
                filename = kwargs.get("filename", None)
                result = self.writer.save_novel(novel_data, filename)
                return {"status": "success" if result.get("success") else "error", "result": result}
            
            else:
                return {"status": "error", "message": f"Unknown function: {function_name}"}
        
        except Exception as e:
            return {"status": "error", "message": str(e)}

# MCP协议兼容接口
def handle_request(input_data):
    """处理MCP请求"""
    tool = NovelCreationTool()
    
    if isinstance(input_data, str):
        try:
            request = json.loads(input_data)
        except json.JSONDecodeError:
            return json.dumps({"status": "error", "message": "Invalid JSON"})
    else:
        request = input_data
    
    action = request.get("action")
    
    if action == "list_functions":
        return json.dumps(tool.list_functions())
    elif action == "execute":
        name = request.get("name")
        arguments = request.get("arguments", {})
        return json.dumps(tool.execute(name, **arguments))
    else:
        return json.dumps({"status": "error", "message": f"Unknown action: {action}"})

# 命令行接口
if __name__ == "__main__":
    tool = NovelCreationTool()
    
    if len(sys.argv) > 1:
        # 命令行模式
        function_name = sys.argv[1]
        kwargs = {}
        
        # 解析参数
        for arg in sys.argv[2:]:
            if "=" in arg:
                key, value = arg.split("=", 1)
                # 尝试解析JSON值
                try:
                    kwargs[key] = json.loads(value)
                except json.JSONDecodeError:
                    kwargs[key] = value
        
        result = tool.execute(function_name, **kwargs)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        # 交互式模式
        print("Novel Creation Tool - Interactive Mode")
        print("Available functions: generate_outline, generate_chapter, polish_text, save_novel")
        
        while True:
            print("\nEnter function name (or 'quit' to exit):")
            func_name = input("> ").strip()
            
            if func_name.lower() == 'quit':
                break
            
            if func_name == 'generate_outline':
                genre = input("Enter genre: ") or "玄幻修仙"
                theme = input("Enter theme: ") or "逆袭"
                length = input("Enter length (短篇/中篇/长篇): ") or "长篇"
                result = tool.execute('generate_outline', genre=genre, theme=theme, length=length)
                print(json.dumps(result, ensure_ascii=False, indent=2))
            
            elif func_name == 'generate_chapter':
                chapter_num = int(input("Enter chapter number: ") or 1)
                title = input("Enter chapter title: ") or "第一章"
                content_type = input("Enter content type: ") or "开端"
                chapter_info = {"chapter": chapter_num, "title": title, "content": content_type}
                outline = {"title": "测试小说", "protagonist": {"name": "测试主角"}}
                result = tool.execute('generate_chapter', chapter_info=chapter_info, outline=outline)
                print(json.dumps(result, ensure_ascii=False, indent=2))
            
            elif func_name == 'polish_text':
                text = input("Enter text to polish: ")
                style = input("Enter style (流畅/简洁/华丽/古风): ") or "流畅"
                result = tool.execute('polish_text', text=text, style=style)
                print(json.dumps(result, ensure_ascii=False, indent=2))
            
            elif func_name == 'save_novel':
                novel_data = {
                    "title": "测试小说",
                    "logline": "测试梗概",
                    "genre": "玄幻修仙",
                    "theme": "逆袭",
                    "length": "短篇",
                    "tone": "测试",
                    "protagonist": {"name": "测试主角"},
                    "antagonist": {"name": "测试反派"},
                    "three_act_structure": {},
                    "chapters": []
                }
                result = tool.execute('save_novel', novel_data=novel_data)
                print(json.dumps(result, ensure_ascii=False, indent=2))
            
            else:
                print(f"Unknown function: {func_name}")