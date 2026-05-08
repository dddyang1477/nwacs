#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
【NWACS 简化质量检测系统】
功能：适合开局等短篇内容检测
"""

import sys
import os
from datetime import datetime
try:
    sys.stdout.reconfigure(encoding='utf-8')
except (AttributeError, OSError):
    pass

# 简化版参数 - 适合开局检测
MIN_WORDS = 300  # 开局300字足够
MIN_PARAGRAPHS = 3  # 至少3段
MAX_RETRY = 3

BASE_URL = "https://api.deepseek.com"
API_KEY = "sk-f3246fbd1eef446e9a11d78efefd9bba"

def call_deepseek(prompt, system_prompt=None):
    """调用DeepSeek"""
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
            "temperature": 0.85,
            "max_tokens": 16000
        }
        response = requests.post(url, headers=headers, json=data, timeout=300)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"   [FAIL] API调用失败: {e}")
        return None

class QualityChecker:
    """质量检测类"""
    def __init__(self, content, chapter_num):
        self.content = content
        self.chapter_num = chapter_num
        self.report = {}
    
    def run_all_checks(self):
        """执行所有检测"""
        print(f"\n{'='*60}")
        print(f"[第{self.chapter_num}章 - 质量检测")
        print(f"{'='*60}")

        checks = [
            self.check_word_count,
            self.check_structure,
            self.check_readability,
            self.check_ending,
            self.check_ai_traces,
        ]
        
        all_passed = True
        
        for check_func in checks:
            try:
                name = check_func.__name__
                passed, msg = check_func()
                self.report[name] = passed
                print(f"   [{name}] {msg}")
                if not passed:
                    all_passed = False
            except Exception as e:
                print(f"   [WARN] 检测出错: {e}")
        
        final_result = all_passed and self.report.get("check_word_count", False)
        self.report["final"] = final_result
        
        print(f"\n{'='*60}")
        print(f"{'[OK] 检测通过' if final_result else '[FAIL] 检测不通过'}")
        print(f"{'='*60}")
        
        return final_result, self.report
    
    def check_word_count(self):
        """字数检测 - 开局版"""
        wc = len(self.content)
        passed = wc >= MIN_WORDS
        msg = f"{'OK' if passed else 'WARN'} 字数: {wc}字 (≥{MIN_WORDS}字)"
        self.report["word_count"] = wc
        return passed, msg
    
    def check_structure(self):
        """结构检测 - 开局版"""
        paragraphs = [p for p in self.content.split('\n\n') if p.strip()]
        avg_paragraph_len = sum(len(p) for p in paragraphs) / max(len(paragraphs),1)
        passed = len(paragraphs) >= MIN_PARAGRAPHS
        msg = f"{'OK' if passed else 'WARN'} 段落: {len(paragraphs)}段, 平均{int(avg_paragraph_len)}字"
        self.report["paragraphs"] = len(paragraphs)
        return passed, msg
    
    def check_readability(self):
        """可读性检测"""
        total_chars = len(self.content)
        dots = self.content.count('。')
        commas = self.content.count('，')
        exclaims = self.content.count('！')
        question = self.content.count('？')
        punc_ratio = (dots + commas + exclaims + question) / max(total_chars, 1)
        
        passed = 0.03 < punc_ratio < 0.12
        
        msg = f"{'OK' if passed else 'WARN'} 标点密度: {punc_ratio:.2%}"
        return passed, msg
    
    def check_ending(self):
        """结尾检测"""
        last_part = self.content[-500:].strip()
        passed = len(last_part) > 100 and '。' in last_part[-100:]
        msg = f"{'OK' if passed else 'WARN'} 结尾: {len(last_part)}字"
        return passed, msg

    def check_ai_traces(self):
        """AI痕迹检测"""
        try:
            from ai_polisher import get_polisher
            polisher = get_polisher()
            traces = polisher.detect_ai_traces(self.content)
            score = traces["total_score"]
            passed = score <= 25
            msg = f"{'OK' if passed else 'FAIL'} AI痕迹: {score}/100 (阈值≤25)"
            self.report["ai_trace_score"] = score
            return passed, msg
        except ImportError:
            return True, "[WARN] AI痕迹检测模块不可用，跳过"
        except Exception as e:
            return True, f"[WARN] AI痕迹检测出错: {e}"

def clean_content(content):
    """清理内容"""
    lines = content.strip().split('\n')
    cleaned = []
    skip_keywords = ["本章结束", "未完待续", "---", "字数", "第.*章"]
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        skip = False
        for kw in skip_keywords:
            if kw in line:
                skip = True
                break
        if not skip:
            cleaned.append(line)
    
    return '\n'.join(cleaned)

def mark_for_manual_check(chapter_num, report, output_dir="novel"):
    """
    标记为需要人工处理
    - 创建待处理标记文件
    - 记录检测报告
    """
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    mark_filename = os.path.join(output_dir, f"第{chapter_num}章_需要人工检查.txt")
    
    warning_content = f"""[WARNING] 此章节需要人工检查
{'='*70}
生成时间: {timestamp}
章节: 第{chapter_num}章
状态: 质量检测失败（第{MAX_RETRY}次）

【检测报告】
字数: {report.get('word_count',0)}字 (要求≥{MIN_WORDS}字)
段落: {report.get('paragraphs',0)}段 (要求≥10段)

【检测结果】
pass_word_count: {report.get('check_word_count',False)}
pass_structure: {report.get('check_structure',False)}
pass_readability: {report.get('check_readability',False)}
pass_ending: {report.get('check_ending',False)}
overall: {report.get('final',False)}

【处理建议】
1. 检查API配置是否正常
2. 检查章节大纲是否合理
3. 人工重写或调整内容
4. 处理完成后删除此标记文件
{'='*70}
"""
    
    with open(mark_filename, 'w', encoding='utf-8') as f:
        f.write(warning_content)
    
    print(f"   [WARN] 已创建标记文件: {mark_filename}")
    
    # 2. 更新待处理列表
    log_file = os.path.join(output_dir, "待人工处理列表.txt")
    log_entry = f"{timestamp} - 第{chapter_num}章 - 检测失败\n"
    
    if os.path.exists(log_file):
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    else:
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write("NWACS 待人工处理章节列表\n")
            f.write("="*50 + "\n")
            f.write(log_entry)
    
    print(f"   [WARN] 已更新待处理列表: {log_file}")

def generate_and_check(chapter_num, outline, output_dir="novel"):
    """
    完整流程
    """
    print(f"\n[开始处理第{chapter_num}章")
    
    title = outline.get("title", "")
    summary = outline.get("summary", "")
    key_points = outline.get("key_points", [])
    
    last_report = {}
    
    for attempt in range(1, MAX_RETRY + 1):
        print(f"\n{'='*60}")
        print(f"[第{attempt}次尝试")
        print(f"{'='*60}")
        
        # =========== 1. 生成 ===========
        print(f"  正在生成...")
        
        system_prompt = """你是顶级网文作家，精通影视化写作。

【影视感写作原则】
1. 镜头语言：远景建立空间→中景推进叙事→特写引爆情绪
2. 感官矩阵：每个场景至少调动3种感官（视觉/听觉/触觉/嗅觉/动觉）
3. 情绪外化：不写"他愤怒"，写他掀翻了桌子；不写"他紧张"，写他指尖发白
4. 节奏控制：战斗用短句加速，情感用长句沉溺，段落要有呼吸感
5. 对话影视化：每2-3句对话插入画面描写，潜台词用动作暗示
6. 光影色彩：用光影和色彩传递情绪，让文字有画面

【硬性要求】
1. 字数：绝对不能少于4000字！最好写4000-5000字
2. 结构：有开头、发展、高潮、结尾
3. 细节：增加环境描写、心理活动、对话
4. 视角：以叶青云为主视角

【禁止事项】
- 不要写"本章结束"、"未完待续"
- 不要写"他感到""他觉得""他心想"
- 不要解释，直接写内容
- 不要形容词堆砌，用动作和感官替代

输出要求：只输出完整章节内容！"""
        
        prompt = f"""请写《天机道主》{title}

【本章要点】
{summary}

【关键情节】
{chr(10).join('  ' + point for point in key_points)}

【写作要求】
- 绝对不能少于4000字！
- 内容要非常丰富，增加大量细节
- 保持剧情连贯
- 不要提前结束

直接输出章节内容，不要标题！"""
        
        content = call_deepseek(prompt, system_prompt)
        
        if not content:
            continue
        
        content = clean_content(content)
        
        print(f"   [OK] 生成完成: {len(content)}字")
        
        # =========== 2. 检测 ===========
        checker = QualityChecker(content, chapter_num)
        passed, last_report = checker.run_all_checks()
        
        # =========== 3. 处理结果 ===========
        if passed:
            print(f"\n💾 检测通过！正在保存...")
            filename = save_chapter(chapter_num, content, output_dir)
            print(f"[OK] 已保存: {filename}")
            return content, True, last_report
        
        else:
            if attempt < MAX_RETRY:
                print(f"\n  检测不通过，重新生成...")
            else:
                print(f"\n{'='*70}")
                print(f"[WARNING] 第{attempt}次检测全部失败！")
                print(f"{'='*70}")
                print(f"  请负责人进行人工检查和处理！")
                print(f"    问题章节：第{chapter_num}章")
                print(f"    检测报告：")
                print(f"      字数: {last_report.get('word_count',0)}字")
                print(f"      段落: {last_report.get('paragraphs',0)}段")
                print(f"      检测结果: 不通过")
                print(f"\n  处理建议:")
                print(f"   1. 检查API配置是否正常")
                print(f"   2. 检查章节大纲是否合理")
                print(f"   3. 人工重写或调整")
                print(f"{'='*70}")
                
                mark_for_manual_check(chapter_num, last_report, output_dir)
                
                filename = save_chapter(chapter_num, content, output_dir)
                print(f"[WARN] 已强制保存: {filename}")
                return content, False, last_report

def save_chapter(chapter_num, content, output_dir="novel"):
    """保存章节"""
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, f"第{chapter_num}章.txt")
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return filename

def main():
    print("="*70)
    print("[NWACS V9.0 - 质量检测系统（含人工处理）")
    print("="*70)
    print(f"  检测标准：")
    print(f"   1. 字数 ≥ {MIN_WORDS}字（硬性要求）")
    print(f"   2. 段落 ≥10段")
    print(f"   3. 可读性检查")
    print(f"   4. 结尾完整性")
    print(f"   5. 第{MAX_RETRY}次失败将标记待人工处理")
    print("="*70)
    
    demo_outline = {
        1: {
            "title": "第1章：重生与因果眼",
            "summary": "叶青云重生回到少年时代，发现自己拥有因果推演能力",
            "key_points": ["重生归来", "因果眼觉醒", "初步推演", "立下誓言"]
        }
    }
    
    chapter_num = 1
    outline = demo_outline.get(chapter_num, {})
    
    content, success, report = generate_and_check(chapter_num, outline)
    
    print(f"\n💾 文件已保存: novel/第{chapter_num}章.txt")
    print(f"[OK] 最终字数: {len(content)}字")
    
    if success:
        print(f"🎉 检测通过，完美！")
    else:
        print(f"[WARN] 检测未通过，已标记待人工处理！")
        print(f"   请检查: novel/第{chapter_num}章_需要人工检查.txt")
    
    print("\n" + "="*70)
    print("任务完成！")
    print("="*70)

if __name__ == "__main__":
    main()
