#!/usr/bin/env python3
import os
import requests
import json
from datetime import datetime

API_KEY = os.getenv("DEEPSEEK_API_KEY")
if not API_KEY:
    API_KEY = "your-api-key-here"

URL = "https://api.deepseek.com/v1/chat/completions"

def call_deepseek(prompt, model="deepseek-chat", max_tokens=4000):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.8
    }
    try:
        response = requests.post(URL, headers=headers, json=data, timeout=120)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"请求错误: {str(e)}"

def generate_chapter(chapter_num, chapter_title, context=""):
    prompt = f"""你是网络小说作家，创作玄幻修仙小说《苟在仙门：从废柴到幕后黑手》。

请创作第{chapter_num}章：{chapter_title}

小说设定：
- 主角：陈墨，青云宗外门弟子，表面废柴实则身负混沌仙体，性格苟道流+智斗流+黑暗流+幕后流
- 四个女主：苏清雪（清冷仙子）、夜玲珑（刁蛮魔女）、柳轻烟（温柔丹师）、紫灵（神秘御姐）
- 世界观：玄黄大千世界，修炼境界：炼气→筑基→金丹→元婴→化神→炼虚→合体→大乘→飞升

要求：
1. 每章不少于4000字
2. 内容充实，情节丰富
3. 主角苟道流风格：善于隐忍、扮猪吃老虎
4. 包含修炼、战斗、智斗元素
5. 语言流畅，符合网络小说风格

{context}

请开始创作第{chapter_num}章内容："""
    return call_deepseek(prompt, max_tokens=4500)

def generate_chapters_batch(start_ch, end_ch, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("《苟在仙门：从废柴到幕后黑手》\n")
        f.write("=" * 80 + "\n\n")
        
        for ch in range(start_ch, end_ch + 1):
            print(f"正在生成第{ch}章...")
            
            if ch == 1:
                title = "废物弟子"
            elif ch == 2:
                title = "混沌觉醒"
            elif ch == 3:
                title = "神秘传承"
            elif ch == 4:
                title = "暗中修炼"
            elif ch == 5:
                title = "宗门任务"
            elif ch == 6:
                title = "圣女苏清雪"
            elif ch == 7:
                title = "冲突爆发"
            elif ch == 8:
                title = "意外发现"
            elif ch == 9:
                title = "铁柱小弟"
            elif ch == 10:
                title = "情报网络"
            else:
                title = f"第{ch}章"
            
            chapter_content = generate_chapter(ch, title)
            f.write(f"\n{'=' * 80}\n")
            f.write(f"第{ch}章 {title}\n")
            f.write(f"{'=' * 80}\n\n")
            f.write(chapter_content)
            f.write("\n\n")
            print(f"第{ch}章完成 ({len(chapter_content)}字)")
    
    print(f"\n批量生成完成！文件已保存至: {output_file}")

if __name__ == "__main__":
    output_dir = r"E:\Program Files (x86)\Trae CN\github\NWACS\novel"
    os.makedirs(output_dir, exist_ok=True)
    
    print("开始生成小说...")
    print("=" * 50)
    
    output_file = os.path.join(output_dir, "第1-5章.txt")
    generate_chapters_batch(1, 5, output_file)