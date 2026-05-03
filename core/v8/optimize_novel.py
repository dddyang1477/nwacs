#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
根据DeepSeek检测报告优化NWACS工具设置并润色小说章节
"""

import sys
import os
import json
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "sk-f3246fbd1eef446e9a11d78efefd9bba"
BASE_URL = "https://api.deepseek.com"

def call_deepseek(prompt, system_prompt=None, temperature=0.8):
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

def optimize_nwacs_settings():
    """优化NWACS工具设置"""
    print("\n" + "="*60)
    print("⚙️  优化NWACS工具设置")
    print("="*60)
    
    prompt = """请根据以下检测报告，优化NWACS玄幻小说创作工具的设置：

## 检测报告问题摘要
1. **人物塑造问题：**
   - 主角情感表达生硬，信任建立过快
   - 女主角功能性过强，缺乏独立性
   - 配角工具人倾向

2. **设定平衡问题：**
   - 因果推演能力边界模糊，存在滥用风险
   - 修炼体系提及较少
   - 需要为推演能力设置限制（消耗、干扰因素、因果反噬）

3. **剧情节奏问题：**
   - 时间线跳跃感
   - 部分章节节奏偏快

## 需要优化的设置
请提供以下优化后的工具配置：

1. **人物生成规则**（确保人物有深度、独立性）
2. **能力限制规则**（因果推演能力的消耗、干扰因素、反噬机制）
3. **剧情节奏控制规则**（过渡章节要求、爽点密度、高潮间隔）
4. **设定一致性规则**（修炼体系、世界观设定的检查规则）

请以JSON格式输出详细的优化配置。"""

    system_prompt = """你是一位专业的AI写作工具配置专家，擅长根据检测报告优化创作工具设置。
优化原则：
1. 确保人物有深度、动机复杂
2. 能力要有代价和限制
3. 剧情节奏要有张弛
4. 设定要前后一致"""

    result = call_deepseek(prompt, system_prompt, temperature=0.7)
    
    if result:
        # 保存优化配置
        output_file = "core/v8/engine/optimized_settings.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"   ✅ 优化配置已保存：{output_file}")
        return result
    return None

def rewrite_chapter_1():
    """重写第1章，优化主角性格展示"""
    print("\n" + "="*60)
    print("📝 重写第1章")
    print("="*60)
    
    # 读取原章节
    if os.path.exists("novel/《天机道主》第1-5章.txt"):
        with open("novel/《天机道主》第1-5章.txt", 'r', encoding='utf-8') as f:
            content = f.read()
            # 提取第1章内容
            start = content.find("第一章")
            end = content.find("第二章")
            if end == -1:
                end = len(content)
            chapter1 = content[start:end]
    else:
        chapter1 = ""
    
    prompt = f"""请根据以下检测建议重写《天机道主》第1章：

## 原章节内容
{chapter1[:3000]}

## 优化要求
1. **主角性格深化：** 叶青云作为前世天算师，应该更加深沉、谨慎，情感不外露
2. **能力展示收敛：** 不要让推演能力过于无敌，第一次推演应该有消耗感和风险
3. **悬念设置：** 增加更多关于父亲失踪的线索和悬念
4. **节奏放缓：** 不要太快解决冲突，增加一些心理活动描写

## 具体修改点
1. 叶青云的冷静应该是"经历过生死的平静"，而不是简单的"镇定"
2. 第一次使用推演能力应该有代价（如头痛、消耗精神力）
3. 增加对父亲失踪的回忆和疑惑
4. 对林逸的反击应该更有层次感，不是一次到位

请重写第1章，保持原有剧情框架，但优化细节。"""

    system_prompt = """你是一位顶尖的玄幻小说作家，擅长写有深度的角色和紧凑的剧情。
写作要点：
1. 人物心理活动要细腻
2. 能力使用要有代价
3. 悬念要到位
4. 节奏要适中"""

    result = call_deepseek(prompt, system_prompt, temperature=0.85)
    return result

def rewrite_chapter_5():
    """重写第5章，优化主角与苏沐雪的关系发展"""
    print("\n" + "="*60)
    print("📝 重写第5章")
    print("="*60)
    
    prompt = """请根据以下检测建议重写《天机道主》第5章：

## 原章节核心内容
叶青云帮助苏沐雪，两人关系快速升温，叶青云向苏沐雪展示推演能力

## 优化要求
1. **情感发展合理化：** 叶青云对苏沐雪的信任需要建立在推演基础上，而不是单纯的情感冲动
2. **苏沐雪形象深化：** 赋予她更多独立思考和主动性，不是单纯的"跟随者"
3. **能力展示谨慎：** 叶青云不会轻易展示推演能力，需要有合理的理由
4. **增加试探：** 叶青云应该先试探苏沐雪，确认她值得信任

## 具体修改点
1. 叶青云通过推演发现苏沐雪是"因果锚点"，对他的计划至关重要
2. 叶青云先暗中观察苏沐雪一段时间，确认她的品性
3. 苏沐雪应该对叶青云的能力产生怀疑和思考，而不是盲目信任
4. 两人的关系建立在"互相需要"的基础上，而不是单纯的好感

请重写第5章，保持原有剧情框架，但优化情感发展。"""

    system_prompt = """你是一位顶尖的玄幻小说作家，擅长写细腻的情感和智斗。
写作要点：
1. 情感发展要有逻辑
2. 人物要有独立思考
3. 信任建立要有过程
4. 对话要符合人物性格"""

    result = call_deepseek(prompt, system_prompt, temperature=0.85)
    return result

def rewrite_chapters_11_15():
    """重写第11-15章，优化秘境探险情节"""
    print("\n" + "="*60)
    print("📝 重写第11-15章")
    print("="*60)
    
    prompt = """请根据以下检测建议重写《天机道主》第11-15章（秘境探险部分）：

## 原章节核心内容
叶青云进入秘境，轻松破解幻阵，发现父亲的玉佩，获得机缘

## 优化要求
1. **增加危机感：** 秘境应该更危险，推演能力不能解决所有问题
2. **能力限制：** 增加推演的消耗和干扰因素（如上古禁制干扰推演）
3. **团队互动：** 增加苏沐雪的主动性，她应该能独立解决一些问题
4. **悬念加深：** 父亲玉佩的线索应该更神秘，留下更多疑问

## 具体修改点
1. 幻阵不仅考验智力，还要考验意志力
2. 叶青云的推演在秘境中受到干扰，出现模糊和错误
3. 苏沐雪利用自己的冰凤血脉帮助破除部分幻境
4. 玉佩上的线索不完整，需要后续解密
5. 增加一个中等强度的战斗，展现两人的配合

请重写第11-15章，保持原有剧情框架，但增加危险感和团队互动。"""

    system_prompt = """你是一位顶尖的玄幻小说作家，擅长写探险和智斗。
写作要点：
1. 危险要真实可信
2. 能力使用要有代价和限制
3. 团队互动要自然
4. 悬念要到位"""

    result = call_deepseek(prompt, system_prompt, temperature=0.85)
    return result

def rewrite_chapters_21_30():
    """重写第21-30章，优化离开宗门和建立天机阁的情节"""
    print("\n" + "="*60)
    print("📝 重写第21-30章")
    print("="*60)
    
    prompt = """请根据以下检测建议重写《天机道主》第21-30章（离开宗门和建立天机阁部分）：

## 原章节核心内容
叶青云离开青云宗，在落凤城建立天机阁

## 优化要求
1. **离开动机强化：** 增加"压死骆驼的最后一根稻草"式的事件
2. **建立过程细化：** 天机阁的建立应该有更多细节和挑战
3. **配角深化：** 增加王铁柱等配角的独立性和动机
4. **节奏放缓：** 不要太快完成建立过程

## 具体修改点
1. 增加宗门高层对叶青云的迫害或利用，迫使他离开
2. 描写叶青云如何解决初始资金、收服追随者、应对当地势力
3. 王铁柱应该有自己的梦想和挣扎，不是单纯的跟班
4. 天机阁初期应该更像一个"情报组织"而非"战斗门派"

请重写第21-30章，保持原有剧情框架，但增加细节和合理性。"""

    system_prompt = """你是一位顶尖的玄幻小说作家，擅长写势力建立和智斗。
写作要点：
1. 建立势力要有过程和挑战
2. 人物要有独立动机
3. 细节要丰富
4. 节奏要适中"""

    result = call_deepseek(prompt, system_prompt, temperature=0.85)
    return result

def main():
    print("="*60)
    print("🔧 根据DeepSeek检测报告优化NWACS与润色小说")
    print("="*60)
    
    # 1. 优化NWACS工具设置
    optimize_nwacs_settings()
    
    # 2. 重写关键章节
    chapters_to_rewrite = [
        ("第1章", rewrite_chapter_1),
        ("第5章", rewrite_chapter_5),
        ("第11-15章", rewrite_chapters_11_15),
        ("第21-30章", rewrite_chapters_21_30),
    ]
    
    rewritten_chapters = {}
    
    for name, func in chapters_to_rewrite:
        result = func()
        if result:
            rewritten_chapters[name] = result
            print(f"   ✅ {name}重写完成")
    
    # 3. 保存重写的章节
    if rewritten_chapters:
        output_file = "novel/《天机道主》优化版第1-30章.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write("《天机道主》优化版第1-30章\n")
            f.write("="*60 + "\n\n")
            f.write(f"优化时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("优化依据：DeepSeek剧情一致性检测报告\n\n")
            f.write("="*60 + "\n\n")
            
            for name, content in rewritten_chapters.items():
                f.write(f"【{name}】\n")
                f.write("-"*60 + "\n")
                f.write(content)
                f.write("\n\n")
        
        print(f"\n   ✅ 优化版章节已保存：{output_file}")
    
    print("\n" + "="*60)
    print("🎉 优化完成！")
    print("="*60)
    print("\n优化内容：")
    print("  1. NWACS工具设置优化（core/v8/engine/optimized_settings.json）")
    print("  2. 第1章重写（深化主角性格，增加能力代价）")
    print("  3. 第5章重写（优化情感发展，增加合理性）")
    print("  4. 第11-15章重写（增加危机感，强化团队互动）")
    print("  5. 第21-30章重写（细化建立过程，增加细节）")

if __name__ == "__main__":
    main()