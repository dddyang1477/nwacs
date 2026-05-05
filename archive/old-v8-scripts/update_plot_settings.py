#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
剧情设定更新工具 - 交互式选择创新设定
"""

import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

def print_header(title):
    print("\n" + "=" * 60)
    print("  " + title)
    print("=" * 60)

def get_selection(title, options):
    print_header(title)
    for key, val in options.items():
        print(f"  [{key}] {val['name']} - {val['description']}")
    print("-" * 60)
    while True:
        selection = input("请输入选项编号: ").strip()
        if selection in options:
            return options[selection]
        print("选项无效，请重新输入!")

def get_multi_selection(title, options):
    print_header(title + "（可多选，用逗号分隔）")
    for key, val in options.items():
        print(f"  [{key}] {val['name']}")
    print("-" * 60)
    while True:
        selection = input("请输入选项编号: ").strip()
        selected = []
        for s in selection.split(','):
            s = s.strip()
            if s in options:
                selected.append(options[s])
        if selected:
            return selected
        print("请至少选择一个选项!")

def main():
    print("\n" + "=" * 80)
    print("          剧情设定更新工具")
    print("          反套路创新设定")
    print("=" * 80)

    # 主角身份选择
    protagonist_types = {
        "1": {"name": "平民出身", "description": "普通市井少年，乐观开朗，运气特别好"},
        "2": {"name": "家中中落", "description": "曾经的天才，但家族衰败，选择低调生活"},
        "3": {"name": "穿越者", "description": "带着现代知识来到修仙世界，智计无双"},
        "4": {"name": "走狗屎运", "description": "普通少年，却总能遇到各种奇遇"},
        "5": {"name": "转世重生", "description": "带着前世记忆，目标明确"},
        "6": {"name": "宗门弃徒", "description": "被逐出师门，却因祸得福"},
    }

    protagonist = get_selection("请选择主角身份", protagonist_types)
    print(f"\n✓ 选择主角身份: {protagonist['name']}")

    # 金手指类型选择
    golden_fingers = {
        "1": {"name": "锦鲤体质", "description": "运气爆棚，逢凶化吉，捡漏之王"},
        "2": {"name": "招财猫", "description": "会说话的招财猫，能感知宝物位置"},
        "3": {"name": "谎言成真", "description": "说的谎言有一定概率变成现实"},
        "4": {"name": "梦境修炼", "description": "在梦中修炼，时间加速10倍"},
        "5": {"name": "情绪收集器", "description": "能吸收他人情绪转化为修为"},
        "6": {"name": "因果线", "description": "能看到并轻微改变因果关系"},
        "7": {"name": "美食悟道", "description": "通过烹饪美食领悟大道"},
        "8": {"name": "记忆当铺", "description": "可以典当记忆换取修炼资源"},
    }

    golden_finger = get_selection("请选择金手指类型", golden_fingers)
    print(f"\n✓ 选择金手指: {golden_finger['name']}")

    # 修炼体系选择
    cultivation_systems = {
        "1": {"name": "气运修炼", "description": "收集天地气运，气运越高实力越强"},
        "2": {"name": "因果修炼", "description": "操控因果线，影响事物发展"},
        "3": {"name": "情绪修炼", "description": "吸收他人情绪转化为修为"},
        "4": {"name": "梦境修炼", "description": "在梦中修炼，时间流速不同"},
        "5": {"name": "美食修炼", "description": "通过烹饪悟道，美食越强修为越高"},
        "6": {"name": "契约修炼", "description": "与各种生灵签订契约获得力量"},
        "7": {"name": "卡牌修炼", "description": "将功法、法术封印在卡牌中"},
        "8": {"name": "音乐修炼", "description": "以音入道，音律攻击"},
    }

    cultivation = get_selection("请选择修炼体系", cultivation_systems)
    print(f"\n✓ 选择修炼体系: {cultivation['name']}")

    # 女主类型选择（多选）
    female_types = {
        "1": {"name": "吃货少女", "description": "顶级美食家，能品尝出食材的灵气"},
        "2": {"name": "算卦少女", "description": "精通卜卦，能预知未来"},
        "3": {"name": "妖族公主", "description": "妖族公主，傲娇但护短"},
        "4": {"name": "失忆圣女", "description": "失去记忆的圣女，呆萌可爱"},
        "5": {"name": "机关大师", "description": "擅长制作各种机关法宝"},
        "6": {"name": "毒医双绝", "description": "既是毒师又是神医"},
        "7": {"name": "书呆子", "description": "博学多才，过目不忘"},
        "8": {"name": "女土匪", "description": "性格豪爽，武功高强"},
    }

    females = get_multi_selection("请选择女主类型（可多选）", female_types)
    print(f"\n✓ 选择女主: {', '.join([f['name'] for f in females])}")

    # 输出设定摘要
    print_header("剧情设定摘要")
    print(f"主角身份: {protagonist['name']}")
    print(f"金手指: {golden_finger['name']}")
    print(f"修炼体系: {cultivation['name']}")
    print(f"女主: {', '.join([f['name'] for f in females])}")

    # 保存设定
    save_path = 'output/剧情设定.txt'
    os.makedirs('output', exist_ok=True)
    
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write("剧情设定\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"主角身份: {protagonist['name']}\n")
        f.write(f"  描述: {protagonist['description']}\n\n")
        f.write(f"金手指: {golden_finger['name']}\n")
        f.write(f"  描述: {golden_finger['description']}\n\n")
        f.write(f"修炼体系: {cultivation['name']}\n")
        f.write(f"  描述: {cultivation['description']}\n\n")
        f.write("女主设定:\n")
        for i, f in enumerate(females, 1):
            f.write(f"  {i}. {f['name']} - {f['description']}\n")

    print(f"\n✓ 设定已保存到: {save_path}")

    print("\n" + "=" * 80)
    print("                    设定完成！")
    print("=" * 80)
    print("\n接下来可以使用这些设定生成小说大纲和章节！")

if __name__ == "__main__":
    main()
