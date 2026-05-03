#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用DeepSeek检测小说剧情一致性
"""

import sys
import os
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "sk-f3246fbd1eef446e9a11d78efefd9bba"
BASE_URL = "https://api.deepseek.com"

def call_deepseek(prompt, system_prompt=None, temperature=0.7):
    """调用DeepSeek API"""
    import requests
    try:
        url = f"{BASE_URL}/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        data = {
            "model": "deepseek-chat",
            "messages": messages,
            "temperature": temperature,
            "max_tokens": 8000
        }
        response = requests.post(url, headers=headers, json=data, timeout=180)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"   ❌ API调用失败: {e}")
        return None

def read_chapters():
    """读取所有已生成的章节内容"""
    chapters = []
    
    # 读取第1-5章
    if os.path.exists("novel/《天机道主》第1-5章.txt"):
        with open("novel/《天机道主》第1-5章.txt", 'r', encoding='utf-8') as f:
            content = f.read()[:5000]  # 限制长度
            chapters.append(("第1-5章", content))
    
    # 读取第6-10章
    if os.path.exists("novel/《天机道主》第6-10章.txt"):
        with open("novel/《天机道主》第6-10章.txt", 'r', encoding='utf-8') as f:
            content = f.read()[:5000]
            chapters.append(("第6-10章", content))
    
    # 读取第11-15章
    if os.path.exists("novel/第11-15章.txt"):
        with open("novel/第11-15章.txt", 'r', encoding='utf-8') as f:
            content = f.read()[:5000]
            chapters.append(("第11-15章", content))
    
    # 读取第16-20章
    if os.path.exists("novel/第16-20章.txt"):
        with open("novel/第16-20章.txt", 'r', encoding='utf-8') as f:
            content = f.read()[:5000]
            chapters.append(("第16-20章", content))
    
    # 读取第21-25章
    if os.path.exists("novel/第21-25章.txt"):
        with open("novel/第21-25章.txt", 'r', encoding='utf-8') as f:
            content = f.read()[:5000]
            chapters.append(("第21-25章", content))
    
    # 读取第26-30章
    if os.path.exists("novel/第26-30章.txt"):
        with open("novel/第26-30章.txt", 'r', encoding='utf-8') as f:
            content = f.read()[:5000]
            chapters.append(("第26-30章", content))
    
    return chapters

def detect_plot_consistency():
    """检测剧情一致性"""
    print("="*60)
    print("🔍 使用DeepSeek检测剧情一致性")
    print("="*60)
    
    chapters = read_chapters()
    
    if not chapters:
        print("   ❌ 未找到章节文件")
        return
    
    # 构建章节摘要
    chapters_summary = ""
    for title, content in chapters:
        chapters_summary += f"【{title}】\n"
        chapters_summary += f"内容摘要：{content[:300]}...\n\n"
    
    prompt = f"""请对长篇玄幻小说《天机道主》已生成的第1-30章进行全面的剧情一致性检测。

## 已生成章节摘要
{chapters_summary}

## 小说核心设定（来自大纲）
- **主角：** 叶青云，前世是天道文明最后一位"天算师"，掌握因果推演能力，穿越到青云宗外门杂役身上
- **世界观：** 天玄大陆，九重天境修炼体系（炼气→筑基→金丹→元婴→化神→合体→大乘→渡劫→真仙）
- **核心设定：** 天机乱象，天道每三千年制造一批"天机之子"让他们互相厮杀，胜者成为天道宿主
- **终极目标：** 主角要反杀天道，让所有被天道操控的命运重获自由

## 检测要求
请从以下六个维度进行详细检测：

### 1. 人物一致性
- 主角叶青云的性格、能力、行为逻辑是否一致？
- 女主角苏沐雪的性格、行为是否一致？
- 其他配角（林逸、林啸天、楚凌霄、王铁柱等）的性格和行为是否一致？

### 2. 剧情连贯性
- 从第1章到第30章，剧情发展是否连贯？
- 是否存在逻辑断层或不合理的跳跃？
- 关键剧情节点之间是否有合理的过渡？

### 3. 设定一致性
- 修炼体系是否前后一致？
- 世界观设定（秘境、宗门、势力等）是否一致？
- 因果推演能力的使用是否合理？是否存在滥用或矛盾？

### 4. 节奏合理性
- 爽点分布是否均匀？
- 剧情节奏是否张弛有度？
- 是否存在过于拖沓或过于仓促的部分？

### 5. 偏离度检测
- 当前剧情是否偏离了大纲设定的主线？
- 如果有偏离，偏离程度如何？是否严重？
- 是否需要调整以回到主线？

### 6. 改进建议
- 针对发现的问题，给出具体的改进建议
- 如何让剧情更紧凑、更连贯、更符合设定？

## 输出格式要求
请使用Markdown格式，分点详细说明，给出具体例子和页码/章节位置。

请开始检测。"""

    system_prompt = """你是一位专业的小说编辑和剧情分析师，擅长检测长篇小说的剧情一致性和连贯性。
你的分析特点：
1. 能够准确识别剧情中的逻辑漏洞和人物矛盾
2. 能够给出具体、可操作的改进建议
3. 分析客观、专业，基于文本内容说话
4. 能够指出具体的章节位置和例子

请给出详细、专业、有深度的分析报告。"""

    print("   🧠 正在调用DeepSeek进行分析...")
    result = call_deepseek(prompt, system_prompt, temperature=0.7)
    
    if result:
        report_file = "novel/deepseek_plot_consistency_report.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write("《天机道主》剧情一致性检测报告\n")
            f.write("="*60 + "\n\n")
            f.write(f"检测时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"检测范围：第1-30章\n\n")
            f.write("分析工具：DeepSeek AI\n\n")
            f.write("="*60 + "\n\n")
            f.write(result)
        print(f"   ✅ 检测报告已保存：{report_file}")
        return result
    else:
        print("   ❌ 检测失败")
        return None

def main():
    result = detect_plot_consistency()
    
    if result:
        print("\n" + "="*60)
        print("📋 检测报告预览")
        print("="*60)
        
        # 提取关键结论
        lines = result.split('\n')
        print("\n【关键结论】")
        for i, line in enumerate(lines):
            if '一致' in line or '连贯' in line or '偏离' in line or '问题' in line or '建议' in line:
                if len(line) > 0 and not line.startswith('#'):
                    print(f"  • {line[:80]}...")
                    if i >= 5:
                        break

if __name__ == "__main__":
    main()