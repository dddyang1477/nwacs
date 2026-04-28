#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MCP Server Entry Point for Novel Creation
小说创作MCP服务器入口
"""

import json
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from novel_writer import NovelWriter

def main():
    """主函数"""
    writer = NovelWriter()
    
    # 发送初始化完成信号
    print(json.dumps({"status": "ready", "message": "NovelCreation MCP Server ready"}, ensure_ascii=False))
    sys.stdout.flush()
    
    try:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            
            try:
                request = json.loads(line)
                action = request.get("action")
                
                if action == "list_functions":
                    response = {
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
                
                elif action == "execute":
                    name = request.get("name")
                    arguments = request.get("arguments", {})
                    
                    if name == "generate_outline":
                        genre = arguments.get("genre", "玄幻修仙")
                        theme = arguments.get("theme", "逆袭")
                        length = arguments.get("length", "长篇")
                        result = writer.generate_outline(genre, theme, length)
                        response = {"status": "success", "result": result}
                    
                    elif name == "generate_chapter":
                        chapter_info = arguments.get("chapter_info", {"chapter": 1, "title": "第一章", "content": "开端"})
                        outline = arguments.get("outline", {})
                        result = writer.generate_chapter(chapter_info, outline)
                        response = {"status": "success", "result": result}
                    
                    elif name == "polish_text":
                        text = arguments.get("text", "")
                        style = arguments.get("style", "流畅")
                        result = writer.polish_text(text, style)
                        response = {"status": "success", "result": result}
                    
                    elif name == "save_novel":
                        novel_data = arguments.get("novel_data", {})
                        filename = arguments.get("filename", None)
                        result = writer.save_novel(novel_data, filename)
                        response = {"status": "success" if result.get("success") else "error", "result": result}
                    
                    else:
                        response = {"status": "error", "message": f"Unknown function: {name}"}
                
                elif action == "describe":
                    response = {
                        "status": "success",
                        "name": "novel_creation",
                        "description": "小说创作工具 - 支持大纲生成、章节创作、文本润色、小说保存",
                        "version": "1.0.0"
                    }
                
                else:
                    response = {"status": "error", "message": f"Unknown action: {action}"}
                
                print(json.dumps(response, ensure_ascii=False))
                sys.stdout.flush()
            
            except json.JSONDecodeError:
                print(json.dumps({"status": "error", "message": "Invalid JSON"}, ensure_ascii=False))
                sys.stdout.flush()
    
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}, ensure_ascii=False))
        sys.stdout.flush()

if __name__ == "__main__":
    main()