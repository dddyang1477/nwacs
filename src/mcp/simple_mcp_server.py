#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple Novel Creation MCP Server
独立的小说创作MCP服务器
不依赖任何外部模块
"""

import json
import sys
import os
import random

def generate_title(genre, theme):
    """生成小说标题"""
    titles = {
        '玄幻修仙': ['逆鳞', '天渊', '剑墟', '道骨', '龙血', '玄黄', '尘缘', '仙路'],
        '都市异能': ['觉醒', '超凡', '禁区', '神级', '都市', '巅峰', '无敌', '至尊'],
        '历史架空': ['天下', '山河', '王朝', '帝国', '霸业', '征途', '龙图', '锦绣'],
        '科幻未来': ['星际', '银河', '纪元', '奇点', '跃迁', '星舰', '深空', '重生'],
        '悬疑推理': ['迷局', '真相', '追凶', '暗影', '谜案', '解密', '深渊', '救赎'],
        '言情纯爱': ['心动', '余生', '遇见', '情深', '挚爱', '暖婚', '蜜恋', '星辰'],
        '武侠江湖': ['侠影', '剑心', '江湖', '风云', '铁血', '柔情', '武魂', '传奇'],
        '恐怖惊悚': ['惊魂', '鬼域', '噩梦', '咒怨', '诡影', '禁地', '午夜', '惊悚'],
        '游戏异界': ['重生', '系统', '攻略', '巅峰', '神级', '无敌', '穿越', '争霸']
    }
    
    genre_titles = titles.get(genre, ['传奇', '故事', '风云', '史诗'])
    title_parts = random.sample(genre_titles, 2)
    
    return f"{title_parts[0]}{title_parts[1]}"

def generate_outline(genre, theme, length="长篇"):
    """生成小说大纲"""
    outline = {
        'genre': genre,
        'theme': theme,
        'length': length,
        'title': generate_title(genre, theme),
        'logline': f"一个{theme}的少年，意外获得奇遇，从此踏上逆袭之路",
        'protagonist': {
            'name': f"林{random.choice(['风', '云', '雨', '雷', '雪', '霜', '冰', '炎'])}",
            'background': '小宗门弟子',
            'personality': '隐忍坚韧/智计百出',
            'goal': '复仇/追求大道'
        },
        'three_act_structure': {
            'act1': '开端：主角身处困境，意外获得机缘',
            'act2': '发展：主角历练成长，遭遇挑战',
            'act3': '高潮：主角对决强敌，成就传奇'
        },
        'chapters': [f"第{i}章" for i in range(1, 11)]
    }
    return outline

def generate_chapter(chapter_info, outline):
    """生成章节内容"""
    chapter_num = chapter_info.get('chapter', 1)
    title = chapter_info.get('title', f"第{chapter_num}章")
    
    content = f"【{title}】\n\n"
    content += f"这是第{chapter_num}章的内容。\n\n"
    content += "主角开始了新的冒险...\n\n"
    content += "（章节内容待扩展）"
    
    return {"title": title, "content": content, "chapter": chapter_num}

def polish_text(text, style="流畅"):
    """润色文本"""
    style_effects = {
        '流畅': text.replace('。', '。\n'),
        '简洁': text.replace('非常', '十分').replace('的话', ''),
        '华丽': text + '（华丽润色效果）',
        '古风': text.replace('很', '甚').replace('说', '道')
    }
    return style_effects.get(style, text)

def save_novel(novel_data, filename=None):
    """保存小说"""
    if not filename:
        filename = f"{novel_data.get('title', 'novel')}.txt"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"【{novel_data.get('title', '无题')}】\n\n")
            f.write(f"类型：{novel_data.get('genre', '')}\n")
            f.write(f"主题：{novel_data.get('theme', '')}\n")
            f.write(f"一句话梗概：{novel_data.get('logline', '')}\n\n")
            f.write("【小说内容】\n")
            f.write("（小说内容待填充）")
        
        return {"success": True, "filename": filename, "message": "保存成功"}
    except Exception as e:
        return {"success": False, "message": str(e)}

def list_functions():
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

def describe():
    """描述服务"""
    return {
        "status": "success",
        "name": "novel_creation",
        "description": "小说创作工具 - 支持大纲生成、章节创作、文本润色、小说保存",
        "version": "1.0.0"
    }

def main():
    """主函数"""
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
                    response = list_functions()
                
                elif action == "execute":
                    name = request.get("name")
                    arguments = request.get("arguments", {})
                    
                    if name == "generate_outline":
                        genre = arguments.get("genre", "玄幻修仙")
                        theme = arguments.get("theme", "逆袭")
                        length = arguments.get("length", "长篇")
                        result = generate_outline(genre, theme, length)
                        response = {"status": "success", "result": result}
                    
                    elif name == "generate_chapter":
                        chapter_info = arguments.get("chapter_info", {"chapter": 1, "title": "第一章"})
                        outline = arguments.get("outline", {})
                        result = generate_chapter(chapter_info, outline)
                        response = {"status": "success", "result": result}
                    
                    elif name == "polish_text":
                        text = arguments.get("text", "")
                        style = arguments.get("style", "流畅")
                        result = polish_text(text, style)
                        response = {"status": "success", "result": result}
                    
                    elif name == "save_novel":
                        novel_data = arguments.get("novel_data", {})
                        filename = arguments.get("filename", None)
                        result = save_novel(novel_data, filename)
                        response = {"status": "success" if result.get("success") else "error", "result": result}
                    
                    else:
                        response = {"status": "error", "message": f"Unknown function: {name}"}
                
                elif action == "describe":
                    response = describe()
                
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