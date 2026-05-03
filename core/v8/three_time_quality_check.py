#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS - 三次质量检验调用器
让快速生成功能使用完整的三次检验流程
"""

import sys
import os

def call_three_time_quality_check(content, chapter_num=1, novel_title="未命名"):
    """
    使用三次质量检验流程处理内容
    
    参数:
        content: 初始内容（可以是模板或去痕版）
        chapter_num: 章节号
        novel_title: 小说名
    
    返回:
        (处理后的内容, 是否通过检验, 检验报告)
    """
    from quality_check_and_save_v2 import QualityChecker, MAX_RETRY
    
    print("\n" + "="*70)
    print(f"🔍 三次质量检验流程启动（第1-3次）")
    print("="*70)
    
    processed_content = content
    last_report = {}
    
    for attempt in range(1, MAX_RETRY + 1):
        print(f"\n{'='*60}")
        print(f"📋 第{attempt}次检验")
        print(f"{'='*60}")
        
        # 执行质量检测
        checker = QualityChecker(processed_content, chapter_num)
        passed, report = checker.run_all_checks()
        last_report = report
        
        # 打印检测结果
        print(f"\n检测结果:")
        for key, value in report.items():
            if key != 'final':
                print(f"   - {key}: {value}")
        
        if passed:
            print(f"\n✅ 第{attempt}次检验通过！")
            return processed_content, True, report
        
        # 如果不是最后一次，继续处理
        if attempt < MAX_RETRY:
            print(f"\n⚠️ 第{attempt}次检验未通过")
            print("🔄 正在进行去痕优化...")
            
            # 进行额外的去痕处理
            processed_content = apply_additional_de_ai(processed_content)
            print(f"✅ 去痕优化完成，新长度: {len(processed_content)}字")
        else:
            # 最后一次也失败
            print(f"\n{'='*70}")
            print(f"⚠️ ⚠️ ⚠️  WARNING: 第{MAX_RETRY}次检验全部失败！")
            print(f"{'='*70}")
            print(f"📋 最终检测报告:")
            print(f"   - 字数: {last_report.get('word_count', 0)}字")
            print(f"   - 段落: {last_report.get('paragraphs', 0)}段")
            print(f"   - 结果: 未通过")
            print(f"\n💡 建议: 人工检查并优化内容")
            print(f"{'='*70}")
            
            return processed_content, False, report
    
    return processed_content, False, last_report


def apply_additional_de_ai(content):
    """
    额外的去痕处理（第二次优化）
    """
    import random
    
    result = content
    
    # 1. 进一步替换AI特征词
    replacements = {
        "慢慢地": "一点一点",
        "缓缓地": "慢慢",
        "轻轻地": "轻轻",
        "悄悄地": "悄悄",
        "渐渐地": "逐步",
        "微微一笑": "咧嘴笑了笑",
        "淡淡一笑": "不以为意地笑了笑",
        "似乎": "好像",
        "仿佛": "好像",
        "非常": "特别",
        "极其": "相当",
        "十分": "特别"
    }
    
    for old, new in replacements.items():
        result = result.replace(old, new)
    
    # 2. 随机增加口语化元素
    if random.random() < 0.3:
        # 在句子中插入语气词
        sentences = result.split('。')
        new_sentences = []
        for sent in sentences:
            if len(sent) > 20 and random.random() < 0.2:
                # 在中间插入"然后"或"接着"
                words = list(sent)
                if len(words) > 15:
                    insert_pos = len(words) // 2
                    words.insert(insert_pos, "，" + random.choice(["然后", "接着", "之后"]))
                sent = ''.join(words)
            new_sentences.append(sent)
        result = '。'.join(new_sentences)
    
    # 3. 增加标点变化
    if random.random() < 0.2:
        # 把某些句号改成感叹号或问号
        result = result.replace("。", random.choice(["。", "！", "？"]), 1)
    
    return result


def create_quality_check_wrapper():
    """
    创建一个包装函数，用于NWACS_FINAL的save_novel_to_folder方法调用
    """
    print("\n" + "="*70)
    print("🎯 NWACS - 三次质量检验系统")
    print("="*70)
    print("\n功能说明:")
    print("  1. 对内容进行AI特征检测")
    print("  2. 如果不合格，进行去痕优化")
    print("  3. 最多检验3次")
    print("  4. 第3次仍失败会标记人工处理")
    print("\n检测标准:")
    print(f"  - 字数 ≥ 300字")
    print(f"  - 段落 ≥ 3段")
    print("  - 可读性正常")
    print("  - 结尾完整")
    print("="*70)
    
    return call_three_time_quality_check


if __name__ == "__main__":
    # 测试
    test_content = """
    林晨缓缓地站起身，宛如一只刚刚破茧而出的蝴蝶。
    心中不禁激动万分，仿佛天地都在为他欢呼。
    眼前的景象十分壮观，格外震撼人心。
    这一切似乎都像是一场梦境，渐渐地，林晨才相信这是真的。
    他微微一笑，心中暗想，自己的努力终究没有白费。
    极其艰难的旅程，非常辛苦的奋斗，终于换来了此刻的成功。
   宛如重生一般，他慢慢地向前走去，轻轻地踏上了前方的道路。
    """
    
    wrapper = create_quality_check_wrapper()
    result, success, report = wrapper(test_content, 1, "测试小说")
    
    print("\n最终结果:")
    print(f"  是否通过: {'✅' if success else '❌'}")
    print(f"  最终字数: {len(result)}字")
    print("\n处理后内容:")
    print(result)
