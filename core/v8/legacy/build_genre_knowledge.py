#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 题材流派知识库构建器

用 DeepSeek API 对每种题材+流派组合进行深度学习，提取：
1. 写作手法 - 该流派特有的叙事技巧
2. 剧情模板 - 经典剧情结构和变体
3. 写作特点 - 语言风格和节奏特征
4. 风格指纹 - 可量化的风格标识
5. 创作词汇 - 高频词汇、句式、修辞

输出: genre_knowledge_base.json
"""

import json
import os
import sys
import time
import traceback
from datetime import datetime

API_KEY = "sk-f3246fbd1eef446e9a11d78efefd9bba"
BASE_URL = "https://api.deepseek.com"

GENRE_SCHOOLS = {
    "玄幻": [
        ("sign_in", "签到流"),
        ("system", "系统流"),
        ("wisdom", "智取流"),
        ("gou_dao", "苟道流"),
        ("mortal", "凡人流"),
        ("invincible", "无敌流"),
        ("waste_reverse", "废柴逆袭流"),
        ("farming", "种田流"),
        ("behind_scenes", "幕后黑手流"),
    ],
    "都市": [
        ("urban_romance", "都市情感"),
        ("business_war", "商战流"),
        ("rebirth_city", "重生流"),
        ("divine_doctor", "神医流"),
        ("treasure", "鉴宝流"),
        ("entertainment", "娱乐流"),
        ("war_god_return", "战神归来流"),
        ("campus", "校园流"),
        ("workplace", "职场流"),
    ],
    "仙侠": [
        ("traditional_xiuxian", "传统修仙流"),
        ("sword_cultivator", "剑修流"),
        ("alchemy", "丹修流"),
        ("formation", "阵法流"),
        ("sect", "宗门流"),
        ("rogue_cultivator", "散修流"),
        ("demon_cultivator", "魔修流"),
        ("reincarnation_immortal", "转世重修流"),
    ],
    "科幻": [
        ("hard_scifi", "硬科幻流"),
        ("cyberpunk", "赛博朋克流"),
        ("star_war", "星际战争流"),
        ("apocalypse", "末世流"),
        ("mecha", "机甲流"),
        ("gene_evolution", "基因进化流"),
        ("ai_awakening", "AI觉醒流"),
        ("time_travel_scifi", "时空穿梭流"),
    ],
    "悬疑": [
        ("classic_detective", "本格推理流"),
        ("social_suspense", "社会派流"),
        ("psychological", "心理悬疑流"),
        ("criminal_investigation", "刑侦流"),
        ("tomb_raider", "盗墓流"),
        ("spy", "谍战流"),
        ("reversal", "反转流"),
    ],
    "言情": [
        ("ceo_romance", "霸道总裁流"),
        ("sweet_pet", "甜宠流"),
        ("tortured_love", "虐恋流"),
        ("marry_first", "先婚后爱流"),
        ("female_dominance", "女尊流"),
        ("palace_struggle", "宫斗流"),
        ("family_struggle", "宅斗流"),
        ("business_woman", "商业女霸总"),
        ("youth_campus_love", "青春校园流"),
    ],
    "历史": [
        ("time_travel_history", "穿越流"),
        ("farming_history", "种田流"),
        ("conquest", "争霸流"),
        ("scheming", "权谋流"),
        ("imperial_exam", "科举流"),
        ("business_history", "经商流"),
        ("alternate_history", "架空历史流"),
        ("tech_uplift", "科技攀升流"),
    ],
    "游戏": [
        ("full_dive_vr", "全息游戏流"),
        ("esports", "电竞流"),
        ("game_system", "系统流"),
        ("fourth_disaster", "第四天灾流"),
        ("npc_awakening", "NPC觉醒流"),
        ("game_rebirth", "游戏重生流"),
        ("game_world_travel", "游戏异界流"),
    ],
    "恐怖": [
        ("supernatural", "灵异流"),
        ("folk_horror", "民俗恐怖流"),
        ("infinite_loop", "无限流"),
        ("rule_horror", "规则怪谈流"),
        ("cthulhu", "克苏鲁流"),
        ("urban_legend", "都市传说流"),
        ("survival_horror", "生存恐怖流"),
    ],
    "武侠": [
        ("traditional_wuxia", "传统武侠流"),
        ("high_martial", "高武流"),
        ("national_art", "国术流"),
        ("government_martial", "朝廷鹰犬流"),
        ("demon_cult", "魔教流"),
        ("assassin", "刺客流"),
        ("sword_hero", "剑客流"),
    ],
}


def call_deepseek(prompt: str, temperature: float = 0.3, max_tokens: int = 4000) -> str:
    import requests
    try:
        resp = requests.post(
            f"{BASE_URL}/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {API_KEY}",
            },
            json={
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": "你是中国网络文学研究专家，精通各类型小说的写作技法分析。请用中文回答，只输出JSON格式。"},
                    {"role": "user", "content": prompt},
                ],
                "temperature": temperature,
                "max_tokens": max_tokens,
            },
            timeout=120,
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f'{{"error": "{str(e)[:200]}"}}'


def build_school_knowledge(genre: str, school_id: str, school_name: str) -> dict:
    prompt = f"""你是一位深耕中国网络文学20年的资深编辑和写作导师。请对「{genre}」题材下的「{school_name}」流派进行深度分析。

请基于你对海量网络文学作品的理解，从以下6个维度进行专业分析：

## 1. 写作手法（5-8条）
该流派最核心的叙事技巧和写作技法。每条包含：
- technique: 技法名称
- description: 详细说明（50-100字）
- example_usage: 在小说中如何应用
- effectiveness: 为什么有效

## 2. 剧情模板（3-5个）
该流派最经典的剧情结构和变体。每个包含：
- template_name: 模板名称
- structure: 结构描述（起承转合）
- key_nodes: 关键情节点（3-5个）
- variations: 常见变体（2-3个）
- reader_appeal: 为什么吸引读者

## 3. 写作特点（5-8条）
该流派的语言风格、节奏特征、叙事视角等。每条包含：
- feature: 特点名称
- description: 详细描述
- contrast: 与其他流派的区别

## 4. 风格指纹（量化指标）
可量化的风格标识：
- sentence_length_preference: 句子长度偏好（短句/中句/长句/混合）
- paragraph_density: 段落密度（密集/适中/稀疏）
- dialogue_ratio: 对话占比（低30%/中30-50%/高50%+）
- description_ratio: 描写占比
- action_ratio: 动作占比
- pov_preference: 视角偏好（第一人称/第三人称限知/第三人称全知/多视角）
- pacing: 节奏特征（快/中/慢/变速）
- emotional_curve: 情绪曲线特征
- hook_frequency: 钩子频率（每章结尾悬念密度）

## 5. 创作词汇（分类词汇表）
该流派高频使用的词汇和表达：
- power_system_terms: 力量体系术语（5-10个）
- action_verbs: 动作动词（10-15个）
- emotional_vocabulary: 情感词汇（10-15个）
- environment_descriptors: 环境描写词汇（10-15个）
- character_descriptors: 人物描写词汇（10-15个）
- transition_phrases: 过渡句式（5-10个）
- climax_phrases: 高潮句式（5-10个）
- signature_expressions: 标志性表达（5-10个）

## 6. 大师技法（3-5条）
该流派顶尖作品的独门技法：
- master: 代表作品或作者风格
- technique: 独门技法
- learnable_point: 可学习的要点

请输出完整JSON，不要省略任何字段。格式如下：
```json
{{
  "genre": "{genre}",
  "school_id": "{school_id}",
  "school_name": "{school_name}",
  "analyzed_at": "",
  "writing_techniques": [...],
  "plot_templates": [...],
  "writing_characteristics": [...],
  "style_fingerprint": {{...}},
  "vocabulary": {{...}},
  "master_techniques": [...]
}}
```"""

    print(f"  📡 正在向DeepSeek查询 {genre}/{school_name}...")
    result_text = call_deepseek(prompt, temperature=0.3, max_tokens=6000)

    import re
    json_match = re.search(r'```json\s*(.*?)\s*```', result_text, re.DOTALL)
    if json_match:
        result_text = json_match.group(1)
    else:
        result_text = result_text.strip()

    try:
        data = json.loads(result_text)
        data["analyzed_at"] = datetime.now().isoformat()
        return data
    except json.JSONDecodeError as e:
        print(f"  ⚠️ JSON解析失败: {e}")
        result_text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', result_text)
        last_brace = result_text.rfind('}')
        if last_brace > 0:
            result_text = result_text[:last_brace + 1]
            bracket_count = result_text.count('{') - result_text.count('}')
            result_text += '}' * bracket_count
        try:
            data = json.loads(result_text)
            data["analyzed_at"] = datetime.now().isoformat()
            return data
        except json.JSONDecodeError:
            return {
                "genre": genre,
                "school_id": school_id,
                "school_name": school_name,
                "analyzed_at": datetime.now().isoformat(),
                "error": str(e)[:200],
                "raw_response": result_text[:500],
            }


def main():
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(output_dir, "genre_knowledge_base.json")

    knowledge_base = {}

    if os.path.exists(output_file):
        try:
            with open(output_file, "r", encoding="utf-8") as f:
                knowledge_base = json.load(f)
            print(f"📂 加载已有知识库: {len(knowledge_base)} 个题材")
        except Exception:
            knowledge_base = {}

    total_schools = sum(len(schools) for schools in GENRE_SCHOOLS.values())
    processed = 0
    skipped = 0

    print("=" * 60)
    print("  NWACS 题材流派知识库构建器")
    print(f"  共 {len(GENRE_SCHOOLS)} 个题材, {total_schools} 个流派")
    print("=" * 60)

    for genre, schools in GENRE_SCHOOLS.items():
        if genre not in knowledge_base:
            knowledge_base[genre] = {}

        print(f"\n📚 {genre} ({len(schools)}个流派)")

        for school_id, school_name in schools:
            if school_id in knowledge_base[genre]:
                existing = knowledge_base[genre][school_id]
                if "error" not in existing and existing.get("writing_techniques"):
                    print(f"  ⏭️ {school_name} - 已有数据，跳过")
                    skipped += 1
                    continue

            try:
                data = build_school_knowledge(genre, school_id, school_name)
                knowledge_base[genre][school_id] = data

                if "error" in data:
                    print(f"  ❌ {school_name} - 失败: {data['error'][:80]}")
                else:
                    techs = len(data.get("writing_techniques", []))
                    templates = len(data.get("plot_templates", []))
                    print(f"  ✅ {school_name} - 技法:{techs} 模板:{templates}")

                processed += 1

                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(knowledge_base, f, ensure_ascii=False, indent=2)

                time.sleep(1)

            except Exception as e:
                print(f"  ❌ {school_name} - 异常: {e}")
                traceback.print_exc()
                knowledge_base[genre][school_id] = {
                    "genre": genre,
                    "school_id": school_id,
                    "school_name": school_name,
                    "error": str(e)[:200],
                }
                processed += 1

    print("\n" + "=" * 60)
    print(f"  完成! 处理: {processed}, 跳过: {skipped}")
    print(f"  知识库: {output_file}")
    print(f"  大小: {os.path.getsize(output_file) / 1024:.1f} KB")
    print("=" * 60)


if __name__ == "__main__":
    main()
