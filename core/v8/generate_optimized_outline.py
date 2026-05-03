#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
根据2026年趋势报告，重新生成《天机道主》优化大纲
确保：人物一致性、主线副线埋笔一致、记忆点前后一致
"""

import sys
import os
sys.stdout.reconfigure(encoding='utf-8')

def call_deepseek_optimized_outline():
    """调用DeepSeek生成优化大纲"""
    
    import requests
    
    API_KEY = "sk-f3246fbd1eef446e9a11d78efefd9bba"
    BASE_URL = "https://api.deepseek.com"
    
    system_prompt = """你是一位资深的网文编辑和策划人，擅长：
1. 确保人物一致性——人物性格、能力、动机从始至终保持一致
2. 主线副线埋笔一致——伏笔从埋下到回收有明确的时间表
3. 记忆点前后一致——重要事件、物品、对话前后呼应

你熟悉2026年玄幻小说趋势：
- 智者型主角，不是单纯的爽文男主
- 情感线有深度，不是花瓶女配
- 世界观有层层递进的真相
- 升级有代价，能力有边界
- 智斗为主，爽点密集

风格要求：
- 专业、详细、可操作
- 每个设定都有明确的章节位置
- 每个伏笔都有明确的回收计划"""
    
    user_prompt = """请根据2026年玄幻小说趋势报告，为《天机道主》重新生成一个优化完整大纲。

书名：《天机道主》

核心设定：
- 主角：叶青云（前世是"天算师"，被天道追杀穿越，性格：苟道、谨慎、智商高，不轻易暴露底牌）
- 核心能力：因果推演（有消耗、有反噬、有边界，不是万能的）
- 世界观核心："天机乱象"——每三千年一次的天道筛选，选中100位"天机之子"互相厮杀，最后一人成为新的天道宿主
- 核心反派：楚凌霄（天衍圣地圣子，拥有"因果之眼"，是天道的监视器，不是纯粹的坏人，而是立场对立的悲剧人物）
- 女主角：苏沐雪（青云宗第一美女，拥有"冰凤血脉"，可以净化因果，性格：温柔但有主见，不是花瓶，有自己的成长线）
- 重要配角：王铁柱（胖子，拥有"因果免疫"体质，搞笑担当，后期成为关键人物）
- 世界观真相：天道不是正义的，而是一个维持"循环悲剧"的系统，天机之子注定被吃掉

要求：
1. 人物一致性：确保每个角色的性格、能力、动机从第一章到第一百章保持一致
2. 主线副线埋笔一致：每个伏笔在埋下前就规划好回收位置
3. 记忆点前后一致：重要事件、物品、对话要有明确的前后呼应
4. 章节规划：第1-100章详细规划，每10章一个里程碑
5. 情感线：叶青云与苏沐雪的感情发展要有合理的铺垫、转折、高潮
6. 升级线：因果推演能力要有明确的成长曲线和边界
7. 世界观揭示：分阶段揭示真相，不是一次性揭开
8. 结局：开放式结局，为第二卷埋下伏笔

请输出完整优化大纲，格式清晰，可操作性强。"""
    
    try:
        url = f"{BASE_URL}/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        data = {
            "model": "deepseek-chat",
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 8000
        }
        print("正在调用DeepSeek生成优化大纲...")
        response = requests.post(url, headers=headers, json=data, timeout=180)
        response.raise_for_status()
        result = response.json()
        outline = result["choices"][0]["message"]["content"]
        
        # 保存大纲
        output_path = "novel/《天机道主》优化大纲_完整版.txt"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(outline)
        
        print(f"\n✅ 优化大纲已保存到: {output_path}")
        print("\n" + "="*80)
        print(outline[:3000])  # 输出前3000字预览
        if len(outline) > 3000:
            print("\n...（预览内容过长，完整内容请查看文件）")
        
        return outline
        
    except Exception as e:
        print(f"\n❌ 调用失败: {e}")
        return None

if __name__ == "__main__":
    print("="*80)
    print("📚 《天机道主》优化大纲生成器")
    print("="*80)
    call_deepseek_optimized_outline()
