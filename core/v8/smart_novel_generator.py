#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS V8.0 支持剧情连贯的小说生成系统
功能：
1. 记录每一章的剧情信息
2. 在生成后续章节时提供上下文
3. 确保角色、设定、剧情前后一致
4. 支持剧情回顾和调整
"""

import sys
import json
import os
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "sk-f3246fbd1eef446e9a11d78efefd9bba"
BASE_URL = "https://api.deepseek.com"

def call_deepseek(prompt, system_prompt=None, temperature=0.85):
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

class NovelContext:
    """小说上下文管理器"""
    
    def __init__(self, novel_name):
        self.novel_name = novel_name
        self.context = {
            "novel_name": novel_name,
            "chapters": [],
            "characters": {},
            "setting": {},
            "plot_summary": "",
            "unresolved_questions": [],
            "foreshadowing": []
        }
        self.context_file = f"novels/{novel_name}/context.json"
    
    def load_context(self):
        """加载上下文"""
        if os.path.exists(self.context_file):
            try:
                with open(self.context_file, 'r', encoding='utf-8') as f:
                    self.context = json.load(f)
                print(f"   ✅ 已加载上下文: {len(self.context['chapters'])} 章")
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
    
    def add_chapter_context(self, chapter_num, chapter_name, content, summary=None):
        """添加章节上下文"""
        chapter_info = {
            "chapter_num": chapter_num,
            "chapter_name": chapter_name,
            "content": content,
            "summary": summary or self._auto_summary(content),
            "characters_appeared": [],
            "key_events": [],
            "new_plots": [],
            "created_at": datetime.now().isoformat()
        }
        self.context["chapters"].append(chapter_info)
        self._update_plot_summary()
        self.save_context()
    
    def _auto_summary(self, content):
        """自动生成章节摘要"""
        # 简单实现：取前200字
        return content[:200] + "..." if len(content) > 200 else content
    
    def _update_plot_summary(self):
        """更新剧情总结"""
        summaries = [ch["summary"] for ch in self.context["chapters"]]
        self.context["plot_summary"] = "\n\n".join(summaries)
    
    def get_context_for_generation(self, chapter_num):
        """获取用于生成的上下文"""
        # 获取前面3章的摘要
        recent_chapters = self.context["chapters"][-3:] if chapter_num > 3 else self.context["chapters"]
        
        context_parts = []
        
        # 添加小说设定
        if self.context["setting"]:
            context_parts.append("【小说设定】")
            for key, value in self.context["setting"].items():
                context_parts.append(f"{key}: {value}")
        
        # 添加前面章节摘要
        if recent_chapters:
            context_parts.append("\n【前面章节摘要】")
            for ch in recent_chapters:
                context_parts.append(f"- 第{ch['chapter_num']}章 {ch['chapter_name']}: {ch['summary']}")
        
        # 添加剧情总结
        if self.context["plot_summary"]:
            context_parts.append("\n【整体剧情总结】")
            context_parts.append(self.context["plot_summary"])
        
        return "\n".join(context_parts)
    
    def set_initial_setting(self, setting):
        """设置初始设定"""
        self.context["setting"] = setting
        self.save_context()
    
    def get_all_chapters(self):
        """获取所有章节"""
        return self.context["chapters"]

def create_novel_directory(novel_name):
    """创建小说文件夹"""
    novel_dir = f"novels/{novel_name}"
    os.makedirs(novel_dir, exist_ok=True)
    print(f"   ✅ 小说文件夹已创建: {novel_dir}")
    return novel_dir

def save_chapter(novel_dir, chapter_num, chapter_name, content):
    """保存章节内容"""
    # 保存为 .md 格式
    md_file = f"{novel_dir}/chapter_{chapter_num:02d}.md"
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(f"# {chapter_name}\n\n")
        f.write(content)
        f.write("\n")
    print(f"   ✅ 章节已保存 (MD): {md_file}")
    
    # 保存为 .txt 格式
    txt_file = f"{novel_dir}/chapter_{chapter_num:02d}.txt"
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write(f"{chapter_name}\n")
        f.write("="*len(chapter_name) + "\n\n")
        f.write(content)
        f.write("\n")
    print(f"   ✅ 章节已保存 (TXT): {txt_file}")
    
    return md_file, txt_file

def generate_table_of_contents(novel_dir, novel_name, chapters):
    """生成目录"""
    toc_md = f"{novel_dir}/table_of_contents.md"
    toc_txt = f"{novel_dir}/table_of_contents.txt"
    
    toc_content_md = [
        f"# 📖 {novel_name} - 目录\n\n",
        f"*由NWACS V8.0生成 | 更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n",
        "---\n\n",
        "## 目录\n\n"
    ]
    
    toc_content_txt = [
        f"{novel_name} - 目录\n",
        "="*60 + "\n\n",
        f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n",
        "目录\n\n"
    ]
    
    for chapter_num, chapter_name in chapters:
        toc_content_md.append(f"- [{chapter_name}](chapter_{chapter_num:02d}.md)\n")
        toc_content_txt.append(f"{chapter_name} (chapter_{chapter_num:02d}.txt)\n")
    
    with open(toc_md, 'w', encoding='utf-8') as f:
        f.writelines(toc_content_md)
    print(f"   ✅ 目录已生成 (MD): {toc_md}")
    
    with open(toc_txt, 'w', encoding='utf-8') as f:
        f.writelines(toc_content_txt)
    print(f"   ✅ 目录已生成 (TXT): {toc_txt}")
    
    return toc_md, toc_txt

def merge_full_novel(novel_dir, novel_name, chapters, full_content):
    """合并完整小说"""
    full_md = f"{novel_dir}/{novel_name}_full.md"
    full_txt = f"{novel_dir}/{novel_name}_full.txt"
    
    md_content = [
        f"# 📖 {novel_name}\n\n",
        f"*由NWACS V8.0生成 | 更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n",
        "---\n\n"
    ]
    md_content.extend(full_content)
    
    txt_content = [
        f"{novel_name}\n",
        "="*60 + "\n\n",
        f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n",
        "---\n\n"
    ]
    txt_content.extend(full_content)
    
    with open(full_md, 'w', encoding='utf-8') as f:
        f.writelines(md_content)
    print(f"   ✅ 完整小说已保存 (MD): {full_md}")
    
    with open(full_txt, 'w', encoding='utf-8') as f:
        f.writelines(txt_content)
    print(f"   ✅ 完整小说已保存 (TXT): {full_txt}")
    
    return full_md, full_txt

def generate_tianji_daozhu_with_context():
    """生成《天机道主》- 支持剧情连贯"""
    novel_name = "天机道主"
    print("="*60)
    print(f"📖 开始生成小说: {novel_name} (支持剧情连贯)")
    print("="*60)
    
    # 创建小说文件夹
    novel_dir = create_novel_directory(novel_name)
    
    # 初始化上下文管理器
    context = NovelContext(novel_name)
    context.load_context()
    
    # 设置初始设定
    context.set_initial_setting({
        "小说类型": "玄幻",
        "写作风格": "苟道流、智斗流、热血",
        "主角": "叶青云",
        "境界体系": "启灵境→聚气境→凝丹境→化婴境→出窍境→分神境→合体境→渡劫境→大乘境"
    })
    
    # 定义章节
    chapters_info = [
        (1, "废物与棋子"),
        (2, "因果初显"),
        (3, "天机推演"),
        (4, "暗箭难防"),
        (5, "因果初成"),
    ]
    
    chapters_list = []
    full_content = []
    full_content.append(f"# 📖 {novel_name}\n\n")
    full_content.append(f"*由NWACS V8.0生成 | 更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
    full_content.append("---\n\n")
    
    # 生成每个章节
    for chapter_num, chapter_name in chapters_info:
        print(f"\n生成中 {chapter_num}/{len(chapters_info)}: {chapter_name}")
        
        # 检查是否已生成
        existing_chapters = context.get_all_chapters()
        already_generated = any(ch["chapter_num"] == chapter_num for ch in existing_chapters)
        
        if already_generated:
            print(f"   ⏭️ 第{chapter_num}章已存在，跳过")
            continue
        
        # 获取上下文
        context_str = context.get_context_for_generation(chapter_num)
        
        # 生成章节内容
        chapter_content = generate_tianji_chapter(chapter_num, chapter_name, context_str)
        
        if chapter_content:
            # 保存章节
            save_chapter(novel_dir, chapter_num, chapter_name, chapter_content)
            chapters_list.append((chapter_num, chapter_name))
            
            # 添加上下文
            context.add_chapter_context(chapter_num, chapter_name, chapter_content)
            
            # 添加到完整内容
            full_content.append(f"# {chapter_name}\n\n")
            full_content.append(chapter_content)
            full_content.append("\n---\n\n")
            print(f"   ✅ 第{chapter_num}章完成")
        else:
            print(f"   ❌ 第{chapter_num}章失败")
    
    # 生成目录
    generate_table_of_contents(novel_dir, novel_name, chapters_list)
    
    # 合并完整小说
    merge_full_novel(novel_dir, novel_name, chapters_list, full_content)
    
    print("\n" + "="*60)
    print(f"🎉 小说《{novel_name}》生成完成！")
    print("="*60)
    print(f"\n✅ 特点：")
    print(f"  - 支持剧情连贯生成")
    print(f"  - 自动保存章节上下文")
    print(f"  - 角色、设定前后一致")
    
    print(f"\n小说文件夹: {novel_dir}")
    print(f"章节数量: {len(chapters_list)}")
    
    return novel_dir

def generate_tianji_chapter(chapter_num, chapter_name, context_str):
    """生成《天机道主》章节 - 带上下文"""
    prompts = {
        1: """请为长篇玄幻小说《天机道主》撰写第1章。

## 小说核心设定
- 主角：叶青云，前世是天道文明最后一位"天算师"，掌握因果推演能力
- 穿越身份：青云宗外门杂役，修为炼气一层，废物中的废物
- 背景：这是一个修炼至上的世界，修炼境界分为：启灵境→聚气境→凝丹境→化婴境→出窍境→分神境→合体境→渡劫境→大乘境
- 核心能力：主角拥有"天机棋子"，可以推演因果、操控因果线
- 风格：苟道流、智斗流、热血、悬疑、治愈、搞笑

## 第1章要求
**核心目标**：开篇即高能，打破读者预期，建立主角人设

**必须包含**：
1. 开场即冲突：主角被当众羞辱（被长老之子林逸踩脸）
2. 主角性格展示：表面废物，实则心智如妖，有前世记忆
3. 金手指暗示：天机棋子濒死激活
4. 第一个爽点：主角用智谋反杀，第一个小胜利
5. 埋笔：暗示林逸背后有人操控，主角的处境危险

**字数**：2000-3000字
**风格**：节奏快、信息密度高、每句话都有用
**结尾钩子**：留下悬念，让读者想看下一章""",

        2: """请为长篇玄幻小说《天机道主》撰写第2章。

## 小说核心设定
- 主角：叶青云，前世天算师，穿越到青云宗外门杂役身上
- 核心能力：天机棋子，因果推演，操控因果线
- 风格：苟道流、智斗流

## 第2章要求
**核心目标**：展示主角的智斗能力，埋下重要伏笔

**必须包含**：
1. 主角利用天机棋子的能力，第一次推演成功
2. 发现《因果真经》残卷的线索
3. 与女主苏沐雪的初遇（她是唯一没有嘲笑主角的人）
4. 展示主角的苟道策略：表面废物，暗中布局
5. 林逸的威胁：林逸是长老之子，不会善罢甘休

**字数**：2000-3000字
**风格**：信息量大、智斗精彩、感情线铺垫
**结尾钩子**：暗示更大的阴谋""",

        3: """请为长篇玄幻小说《天机道主》撰写第3章。

## 小说核心设定
- 主角：叶青云，前世天算师，拥有因果推演能力
- 核心设定：等价交换——修炼有代价，力量不是免费
- 风格：苟道流、悬疑

## 第3章要求
**核心目标**：深入展示天机棋子的能力，揭示世界观一角

**必须包含**：
1. 主角第一次完整使用天机推演能力
2. 推演结果：发现林逸背后有人指使，是宗门内部斗争
3. 主角开始布局：用因果线在暗处布局
4. 发现宗门藏经阁的秘密（第七层有上古遗迹）
5. 搞笑元素：主角自言自语吐槽自己的处境

**字数**：2000-3000字
**风格**：智斗为主，搞笑为辅
**结尾钩子**：发现林逸背后的人身份不简单""",

        4: """请为长篇玄幻小说《天机道主》撰写第4章。

## 小说核心设定
- 主角：叶青云，苟道流主角，表面废物实则智慧超群
- 敌人：林逸（长老之子，炼气七层，嚣张跋扈）
- 世界观：青云宗是个下等宗门，但内部斗争激烈

## 第4章要求
**核心目标**：林逸的第二次威胁，主角被动应战

**必须包含**：
1. 林逸设下毒计：让主角在宗门任务中"意外"死亡
2. 主角用天机推演提前预知陷阱
3. 反杀开始：主角将计就计，让林逸的阴谋暴露
4. 苏沐雪的担忧：她发现了主角的异常
5. 感情线推进：苏沐雪给主角送药，主角内心触动

**字数**：2000-3000字
**风格**：危机感强，智斗精彩，感情温暖
**结尾钩子**：林逸的阴谋暴露，但更大的危机即将到来""",

        5: """请为长篇玄幻小说《天机道主》撰写第5章。

## 小说核心设定
- 主角：叶青云，智斗流主角，擅长因果推演和布局
- 本章重点：主角的第一次小高潮——林逸当众出丑

## 第5章要求
**核心目标**：第一个爽点高潮，主角初露锋芒

**必须包含**：
1. 宗门任务开始：林逸等着看主角的笑话
2. 主角早已布下因果线，等待收割
3. 第一个反转：林逸自己踩进了陷阱
4. 打脸时刻：林逸当众暴露勾结魔教的证据
5. 震惊众人：废物杂役竟然让林逸吃瘪
6. 苏沐雪的震惊和好奇：她开始注意到主角

**字数**：2000-3000字
**风格**：爽点密集、打脸痛快、节奏燃爆
**结尾钩子**：长老会介入，主角获得宗门资源倾斜，但危险也在逼近"""
    }
    
    system_prompt_base = """你是一位顶尖的玄幻小说作家，擅长写让人欲罢不能的开篇。
你的写作特点：
1. 开篇第一句话就抓住读者
2. 节奏快，不水字数
3. 每章结尾留钩子
4. 人物对话符合性格
5. 爽点自然流露，不生硬
6. 前后剧情要连贯一致，注意角色设定和情节延续"""
    
    # 添加上下文提示
    if context_str:
        full_prompt = prompts.get(chapter_num, "") + "\n\n" + context_str + "\n\n【重要提醒】请注意前面章节的剧情，保持角色、设定、剧情前后一致！"
    else:
        full_prompt = prompts.get(chapter_num, "")
    
    return call_deepseek(full_prompt, system_prompt_base, temperature=0.85)

def main():
    print("="*60)
    print("📖 NWACS V8.0 小说生成系统（支持剧情连贯）")
    print("="*60)
    
    print("\n请选择要生成的小说：")
    print("  1. 《天机道主》- 玄幻小说（推荐，支持剧情连贯）")
    print("  2. 自定义小说（需提供设定）")
    
    choice = input("\n请输入选项 (1/2): ").strip()
    
    if choice == "1":
        generate_tianji_daozhu_with_context()
    elif choice == "2":
        print("自定义小说功能开发中...")
    else:
        print("无效选项")

if __name__ == "__main__":
    main()
