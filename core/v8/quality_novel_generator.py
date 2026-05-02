#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS V8.0 高质量逐章小说生成系统
核心原则：
1. 质量优先，不追求速度
2. 逐章写作，不批量生成
3. 每章生成前回顾前面剧情
4. 确保角色、设定、剧情前后绝对一致
5. 每章生成后可检查和调整
"""

import sys
import json
import os
import time
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
            "max_tokens": 12000
        }
        print("   ⏳ 正在生成中...")
        response = requests.post(url, headers=headers, json=data, timeout=300)
        response.raise_for_status()
        result = response.json()
        print("   ✅ 生成完成")
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"   ❌ API调用失败: {e}")
        return None

class QualityNovelContext:
    """高质量小说上下文管理器"""
    
    def __init__(self, novel_name):
        self.novel_name = novel_name
        self.context_file = f"novels/{novel_name}/quality_context.json"
        self.context = {
            "novel_name": novel_name,
            "chapters": [],
            "current_chapter": 0,
            "characters": {},
            "setting": {},
            "plot_summary": "",
            "writing_style": "",
            "character_consistency": {
                "main_characters": {},
                "supporting_characters": {},
                "rules": []
            },
            "check_history": []
        }
    
    def load_context(self):
        """加载上下文"""
        if os.path.exists(self.context_file):
            try:
                with open(self.context_file, 'r', encoding='utf-8') as f:
                    self.context = json.load(f)
                print(f"   ✅ 已加载上下文（已生成{len(self.context['chapters'])}章）")
                return True
            except Exception as e:
                print(f"   ⚠️ 加载上下文失败: {e}")
        return False
    
    def save_context(self):
        """保存上下文"""
        os.makedirs(os.path.dirname(self.context_file), exist_ok=True)
        with open(self.context_file, 'w', encoding='utf-8') as f:
            json.dump(self.context, f, indent=2, ensure_ascii=False)
        print(f"   ✅ 上下文已保存")
    
    def set_initial_setting(self, setting_dict):
        """设置初始小说设定"""
        self.context["setting"] = setting_dict
        self.save_context()
    
    def get_comprehensive_context(self):
        """获取完整的上下文（用于生成）"""
        parts = []
        
        if self.context["setting"]:
            parts.append("=== 小说设定 ===")
            for key, value in self.context["setting"].items():
                parts.append(f"{key}: {value}")
            parts.append("")
        
        if self.context["chapters"]:
            parts.append("=== 已生成章节摘要 ===")
            for i, ch in enumerate(self.context["chapters"], 1):
                parts.append(f"第{ch['chapter_num']}章 {ch['chapter_name']}:")
                parts.append(ch['summary'])
                parts.append("")
            
            parts.append("=== 整体剧情总结 ===")
            parts.append(self.context["plot_summary"])
            parts.append("")
        
        if self.context["character_consistency"]:
            parts.append("=== 角色一致性规则 ===")
            if self.context["character_consistency"]["main_characters"]:
                for name, info in self.context["character_consistency"]["main_characters"].items():
                    parts.append(f"主角 {name}:")
                    parts.append(f"  性格: {info.get('personality', '')}")
                    parts.append(f"  特点: {info.get('traits', '')}")
                    parts.append("")
        
        return "\n".join(parts)
    
    def add_complete_chapter(self, chapter_num, chapter_name, content, summary, character_updates=None):
        """添加完整的章节信息"""
        chapter_info = {
            "chapter_num": chapter_num,
            "chapter_name": chapter_name,
            "content": content,
            "summary": summary,
            "character_updates": character_updates or {},
            "generated_at": datetime.now().isoformat()
        }
        self.context["chapters"].append(chapter_info)
        
        # 更新剧情总结
        all_summaries = [ch['summary'] for ch in self.context["chapters"]]
        self.context["plot_summary"] = "\n\n".join(all_summaries)
        
        self.save_context()
    
    def get_chapter_count(self):
        return len(self.context["chapters"])

def create_novel_dir(novel_name):
    novel_dir = f"novels/{novel_name}"
    os.makedirs(novel_dir, exist_ok=True)
    print(f"   ✅ 小说文件夹: {novel_dir}")
    return novel_dir

def save_chapter_file(novel_dir, chapter_num, chapter_name, content):
    """保存章节文件（同时保存md和txt）"""
    md_file = f"{novel_dir}/chapter_{chapter_num:02d}.md"
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(f"# {chapter_name}\n\n")
        f.write(content)
        f.write("\n")
    print(f"   ✅ 已保存 (Markdown): {md_file}")
    
    txt_file = f"{novel_dir}/chapter_{chapter_num:02d}.txt"
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write(f"{chapter_name}\n")
        f.write("=" * len(chapter_name) + "\n\n")
        f.write(content)
        f.write("\n")
    print(f"   ✅ 已保存 (文本): {txt_file}")
    
    return md_file, txt_file

def generate_chapter_summary(content):
    """生成章节摘要"""
    prompt = f"""请为下面的小说章节生成一个简洁的摘要（200字以内），包含：
1. 主要情节
2. 重要事件
3. 角色发展
4. 埋下的伏笔

章节内容：
{content[:4000]}...

请用简洁的语言，分点概括："""
    
    system_prompt = "你是一位专业的小说编辑，擅长总结章节内容。"
    
    result = call_deepseek(prompt, system_prompt, temperature=0.5)
    return result or "摘要生成失败"

def chapter_review_ui(chapter_num, chapter_name, content):
    """章节审查界面"""
    print("\n" + "="*60)
    print(f"📖 第{chapter_num}章: {chapter_name}")
    print("="*60)
    print("\n【内容预览】")
    preview = content[:1000]
    print(preview)
    if len(content) > 1000:
        print("\n...（预览到前1000字）")
    
    print("\n请选择：")
    print("  1. ✅ 接受这一章，继续")
    print("  2. 🔄 重新生成这一章")
    print("  3. ✏️  手动修改内容后保存")
    print("  4. ⏸️  暂停，稍后继续")
    
    choice = input("\n请输入选项 (1/2/3/4): ").strip()
    return choice

def generate_single_chapter_quality(context, chapter_num, chapter_name, prompt_text):
    """生成单章（高质量模式）"""
    novel_dir = create_novel_dir(context.novel_name)
    
    print(f"\n📖 准备生成第{chapter_num}章: {chapter_name}")
    
    comprehensive_context = context.get_comprehensive_context()
    
    system_prompt = """你是一位顶尖的小说作家，特别擅长写高质量的长篇小说。

你的写作原则：
1. 质量优先，不追求速度
2. 剧情连贯，角色设定前后一致
3. 细节丰富，描写生动
4. 节奏有张有弛，有高潮有铺垫
5. 每章结尾都有钩子，吸引读者继续看
6. 语言优美，不水字数
7. 注意前文中的伏笔和设定，前后保持一致"""
    
    full_prompt = f"""请为小说《{context.novel_name}》撰写第{chapter_num}章：{chapter_name}

{prompt_text}

---
【重要】前面章节的剧情回顾（请保持设定和剧情一致）：
{comprehensive_context}

---
【要求】
1. 请确保角色性格、设定和前面一致
2. 注意前面埋下的伏笔
3. 语言质量要高，不水字数
4. 字数：2000-4000字
5. 这一章的结尾要留钩子，吸引读者继续看"""
    
    content = call_deepseek(full_prompt, system_prompt, temperature=0.7)
    
    if content:
        summary = generate_chapter_summary(content)
        
        while True:
            choice = chapter_review_ui(chapter_num, chapter_name, content)
            
            if choice == "1":
                save_chapter_file(novel_dir, chapter_num, chapter_name, content)
                context.add_complete_chapter(chapter_num, chapter_name, content, summary)
                print(f"\n✅ 第{chapter_num}章已保存！")
                return True
            elif choice == "2":
                print(f"\n🔄 重新生成第{chapter_num}章...")
                return generate_single_chapter_quality(context, chapter_num, chapter_name, prompt_text)
            elif choice == "3":
                print(f"\n✏️ 请手动修改后保存")
                print("提示：你可以直接修改小说文件夹里的章节文件")
                print("修改完成后，请按回车继续...")
                input()
                return True
            elif choice == "4":
                print(f"\n⏸️ 暂停中")
                print("下次运行本程序时，可以从第{chapter_num}章继续！")
                return False
            else:
                print("无效选项")
    
    return False

def tianji_chapter_prompt(chapter_num, chapter_name):
    prompts = {
        1: """## 第1章：废物与棋子

**核心目标**：开篇即高能，打破读者预期，建立主角人设

**必须包含**：
1. 开场即冲突：主角被当众羞辱（被长老之子林逸踩脸）
2. 主角性格展示：表面废物，实则心智如妖，有前世记忆
3. 金手指暗示：天机棋子濒死激活
4. 第一个爽点：主角用智谋反杀，第一个小胜利
5. 埋笔：暗示林逸背后有人操控，主角的处境危险

**人物**：
- 主角：叶青云，前世是天道文明最后一位"天算师"
- 反派：林逸，长老之子，嚣张跋扈
- 女主：苏沐雪（本章先不出现，第2章再出场）

**风格**：苟道流、智斗流、节奏快、张力强""",
        
        2: """## 第2章：因果初显

**核心目标**：展示主角的智斗能力，埋下重要伏笔，初遇女主

**必须包含**：
1. 主角利用天机棋子的能力，第一次推演成功
2. 发现《因果真经》残卷的线索
3. 与女主苏沐雪的初遇（她是唯一没有嘲笑主角的人）
4. 展示主角的苟道策略：表面废物，暗中布局
5. 林逸的威胁：林逸是长老之子，不会善罢甘休

**新角色介绍**：
- 苏沐雪：青云宗外门弟子，第一美女，冰肌玉骨，素裙飘飘，眼神清冷但内心善良，拥有"冰凤血脉"（被误认为废血脉）

**风格**：信息量大、智斗精彩、感情线细腻铺垫""",
        
        3: """## 第3章：天机推演

**核心目标**：深入展示天机棋子的能力，揭示世界观一角

**必须包含**：
1. 主角第一次完整使用天机推演能力
2. 推演结果：发现林逸背后有人指使，是宗门内部斗争
3. 主角开始布局：用因果线在暗处布局
4. 发现宗门藏经阁的秘密（第七层有上古遗迹）
5. 搞笑元素：主角自言自语吐槽自己的处境

**世界观揭示**：
- 青云宗：下等宗门，但水很深
- 三大古派：天墟阁、冰魄宫、星宿门
- 天机之子：每隔三千年出现一批""",
        
        4: """## 第4章：暗箭难防

**核心目标**：林逸的第二次威胁，主角被动应战，感情线进展

**必须包含**：
1. 林逸设下毒计：让主角在宗门任务中"意外"死亡
2. 主角用天机推演提前预知陷阱
3. 反杀开始：主角将计就计，让林逸的阴谋暴露
4. 苏沐雪的担忧：她发现了主角的异常
5. 感情线推进：苏沐雪给主角送药，主角内心触动

**风格**：危机感强、智斗精彩、感情温暖""",
        
        5: """## 第5章：因果初成

**核心目标**：第一个爽点高潮，主角初露锋芒

**必须包含**：
1. 宗门任务开始：林逸等着看主角的笑话
2. 主角早已布下因果线，等待收割
3. 第一个反转：林逸自己踩进了陷阱
4. 打脸时刻：林逸当众暴露勾结魔教的证据
5. 震惊众人：废物杂役竟然让林逸吃瘪
6. 苏沐雪的震惊和好奇：她开始注意到主角
7. 结尾：长老会介入，主角获得宗门资源倾斜，但危险也在逼近

**风格**：爽点密集、打脸痛快、节奏燃爆""",
    }
    return prompts.get(chapter_num, "")

def main():
    print("="*60)
    print("📖 NWACS V8.0 高质量逐章小说生成系统")
    print("="*60)
    print("\n【核心原则】")
    print("  1. ✅ 质量优先，不追求速度")
    print("  2. ✅ 逐章写作，不批量生成")
    print("  3. ✅ 每章回顾，确保剧情一致")
    print("  4. ✅ 每章可审查，不满意可重写")
    print("="*60)
    
    novel_name = input("\n请输入小说名称（默认：天机道主）: ").strip()
    if not novel_name:
        novel_name = "天机道主"
    
    context = QualityNovelContext(novel_name)
    
    # 加载或初始化
    if context.load_context():
        start_chapter = context.get_chapter_count() + 1
        print(f"\n✅ 检测到已生成{context.get_chapter_count()}章")
    else:
        print("\n✨ 新小说初始化...")
        
        initial_setting = {
            "小说类型": "玄幻",
            "写作风格": "苟道流、智斗流、热血、悬疑",
            "主角": "叶青云",
            "境界体系": "启灵境→聚气境→凝丹境→化婴境→出窍境→分神境→合体境→渡劫境→大乘境",
            "世界背景": "青云宗（下等宗门）→三大古派→辽阔的修真世界"
        }
        context.set_initial_setting(initial_setting)
        start_chapter = 1
        print("   ✅ 初始设定已保存")
    
    chapters_info = [
        (1, "废物与棋子"),
        (2, "因果初显"),
        (3, "天机推演"),
        (4, "暗箭难防"),
        (5, "因果初成"),
    ]
    
    print(f"\n📋 小说计划（共{len(chapters_info)}章）：")
    for ch_num, ch_name in chapters_info:
        status = "✅" if ch_num <= context.get_chapter_count() else "⏳"
        print(f"  {status} 第{ch_num}章: {ch_name}")
    
    while True:
        print("\n请选择：")
        print("  1. 📝 继续生成下一章")
        print("  2. 🔍 查看已生成的章节")
        print("  3. 📊 查看剧情回顾")
        print("  4. 🚪 退出")
        
        choice = input("\n请输入选项 (1/2/3/4): ").strip()
        
        if choice == "1":
            next_chapter = context.get_chapter_count() + 1
            if next_chapter > len(chapters_info):
                print("\n🎉 恭喜！小说已全部完成！")
                break
            
            ch_num, ch_name = chapters_info[next_chapter - 1]
            prompt = tianji_chapter_prompt(ch_num, ch_name)
            
            success = generate_single_chapter_quality(context, ch_num, ch_name, prompt)
            
            if not success:
                print("\n👋 好的，下次继续！")
                break
        
        elif choice == "2":
            print("\n📖 已生成章节：")
            for ch in context.context["chapters"]:
                print(f"  第{ch['chapter_num']}章: {ch['chapter_name']}")
        
        elif choice == "3":
            print("\n📊 剧情回顾：")
            print(context.context["plot_summary"])
        
        elif choice == "4":
            print("\n👋 再见！")
            break

if __name__ == "__main__":
    main()
