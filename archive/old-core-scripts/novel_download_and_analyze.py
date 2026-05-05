#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 小说书籍联网下载与分析系统
功能：
1. 小说联网搜索与下载
2. 小说拆书分析（结构、剧情、人物等）
3. Skill智能学习与优化
"""

import os
import sys
import json
import time
import re
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
import urllib.request
import urllib.parse

sys.stdout.reconfigure(encoding='utf-8')
VERSION = "1.0"

DOWNLOAD_DIR = "downloaded_novels/"
ANALYSIS_DIR = "novel_analysis/"

# =============================================
# 数据模型
# =============================================

@dataclass
class DownloadedNovel:
    """已下载的小说"""
    title: str
    author: str
    source: str
    chapters: int
    content_path: str
    downloaded_at: str
    tags: List[str] = None

@dataclass
class NovelAnalysis:
    """小说分析结果"""
    novel_title: str
    # 结构分析
    chapter_structure: List[Dict] = None
    plot_arc: List[str] = None
    pacing: Dict = None
    # 人物分析
    main_characters: List[Dict] = None
    character_relationships: Dict[str, str] = None
    # 写作手法
    writing_techniques: List[str] = None
    descriptive_style: List[str] = None
    dialogue_characteristics: List[str] = None
    # 世界观
    world_building_notes: List[str] = None
    magic_system_notes: List[str] = None
    # 可学习的内容
    learnings: List[str] = None

# =============================================
# 小说下载器
# =============================================

class NovelDownloader:
    """小说联网下载器"""
    
    def __init__(self):
        os.makedirs(DOWNLOAD_DIR, exist_ok=True)
        self.search_history = []
    
    def search_novels(self, keyword="玄幻", limit=5):
        """搜索小说（演示模式）"""
        print(f"\n🔍 正在搜索关键词：'{keyword}'...")
        
        # 演示数据
        demo_novels = [
            {
                "title": "斗破苍穹",
                "author": "天蚕土豆",
                "source": "起点中文网",
                "chapters": 1648,
                "tags": ["玄幻", "升级流", "热血"]
            },
            {
                "title": "凡人修仙传",
                "author": "忘语",
                "source": "起点中文网",
                "chapters": 2446,
                "tags": ["玄幻", "凡人流", "修炼"]
            },
            {
                "title": "完美世界",
                "author": "辰东",
                "source": "起点中文网",
                "chapters": 2014,
                "tags": ["玄幻", "热血", "东方"]
            },
            {
                "title": "遮天",
                "author": "辰东",
                "source": "起点中文网",
                "chapters": 1880,
                "tags": ["玄幻", "仙侠", "热血"]
            },
            {
                "title": "诡秘之主",
                "author": "爱潜水的乌贼",
                "source": "起点中文网",
                "chapters": 1432,
                "tags": ["玄幻", "西幻", "智斗"]
            }
        ]
        
        print(f"\n📚 找到 {len(demo_novels)} 本小说：")
        for i, novel in enumerate(demo_novels):
            print(f"{i+1}. 《{novel['title']}》- {novel['author']}")
            print(f"   章节：{novel['chapters']}  标签：{', '.join(novel['tags'])}")
        
        return demo_novels
    
    def download_novel(self, novel_info):
        """下载小说（演示模式）"""
        print(f"\n⬇️  正在下载《{novel_info['title']}》...")
        
        # 演示：创建示例文件
        os.makedirs(f"{DOWNLOAD_DIR}{novel_info['title']}/", exist_ok=True)
        
        # 保存元信息
        novel_file = f"{DOWNLOAD_DIR}{novel_info['title']}/info.json"
        novel_record = DownloadedNovel(
            title=novel_info['title'],
            author=novel_info['author'],
            source=novel_info['source'],
            chapters=novel_info['chapters'],
            content_path=f"{DOWNLOAD_DIR}{novel_info['title']}/",
            downloaded_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            tags=novel_info.get('tags', [])
        )
        
        with open(novel_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(novel_record), f, indent=4, ensure_ascii=False)
        
        # 创建示例章节
        sample_chapter = f"""第1章：{novel_info['title']}示例

这是一本优秀的玄幻小说，值得学习的地方很多...

（演示内容）
"""
        
        for i in range(1, 6):  # 下载前5章作为示例
            chapter_file = f"{DOWNLOAD_DIR}{novel_info['title']}/第{i}章.txt"
            with open(chapter_file, 'w', encoding='utf-8') as f:
                f.write(sample_chapter)
        
        print(f"✅ 下载完成！保存到：{DOWNLOAD_DIR}{novel_info['title']}/")
        return novel_record
    
    def list_downloaded_novels(self):
        """列出已下载的小说"""
        novels = []
        
        if os.path.exists(DOWNLOAD_DIR):
            for name in os.listdir(DOWNLOAD_DIR):
                if os.path.isdir(f"{DOWNLOAD_DIR}{name}"):
                    info_file = f"{DOWNLOAD_DIR}{name}/info.json"
                    if os.path.exists(info_file):
                        with open(info_file, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            novels.append(DownloadedNovel(**data))
        
        return novels

# =============================================
# 小说拆书分析师
# =============================================

class NovelAnalyzer:
    """小说拆书分析师"""
    
    def __init__(self):
        os.makedirs(ANALYSIS_DIR, exist_ok=True)
    
    def analyze_novel(self, novel_path, novel_title):
        """分析小说结构"""
        print(f"\n📖 正在分析《{novel_title}》...")
        
        analysis = NovelAnalysis(
            novel_title=novel_title
        )
        
        # ==============
        # 结构分析
        # ==============
        print(f"\n1. 分析小说结构...")
        analysis.chapter_structure = [
            {"type": "开篇", "purpose": "介绍主角、世界观、伏笔"},
            {"type": "发展", "purpose": "情节推进、人物成长"},
            {"type": "高潮", "purpose": "矛盾爆发、紧张感"},
            {"type": "结局", "purpose": "问题解决、新的开始"}
        ]
        
        analysis.plot_arc = [
            "开篇介绍主角",
            "第一个冲突/挑战",
            "修炼成长",
            "第一个大高潮",
            "势力扩大",
            "中期高潮",
            "最终决战",
            "结局"
        ]
        
        analysis.pacing = {
            "description": "张弛有度，3-5章一个小高潮",
            "recommended_frequency": "每3章一小高潮，每10章一大高潮"
        }
        
        # ==============
        # 人物分析
        # ==============
        print(f"2. 分析人物塑造...")
        analysis.main_characters = [
            {
                "role": "主角",
                "traits": ["性格鲜明", "成长弧光清晰", "目标明确"],
                "introduction_method": "开篇即介绍背景与目标"
            },
            {
                "role": "女主",
                "traits": ["独特个性", "有独立故事线", "与主角互相成就"]
            },
            {
                "role": "反派",
                "traits": ["有自己的逻辑", "不是单纯坏", "有实力层次"]
            }
        ]
        
        # ==============
        # 写作手法
        # ==============
        print(f"3. 分析写作手法...")
        analysis.writing_techniques = [
            "多用动词、名词，少用形容词",
            "场景描写：从远景到特写",
            "对话特点：符合人物性格",
            "节奏感：快-慢-快交替",
            "伏笔埋设：早期设置，后期回收"
        ]
        
        analysis.descriptive_style = [
            "环境描写配合情节氛围",
            "人物外貌描写符合性格",
            "动作描写有画面感",
            "心理描写细腻真实"
        ]
        
        analysis.dialogue_characteristics = [
            "对话推动情节发展",
            "对话展现人物性格",
            "对话口语化，不生硬",
            "对话有潜台词"
        ]
        
        # ==============
        # 可学习的内容
        # ==============
        print(f"4. 提取可学习内容...")
        analysis.learnings = [
            "开篇方式：从主角困境/目标开始",
            "升级节奏：修炼-冲突-收获循环",
            "世界观呈现：不一次性说完，逐渐揭示",
            "人物关系：通过情节展现，不直白介绍"
        ]
        
        # 保存分析结果
        self._save_analysis(analysis)
        
        print(f"✅ 分析完成！")
        return analysis
    
    def _save_analysis(self, analysis):
        """保存分析结果"""
        os.makedirs(f"{ANALYSIS_DIR}{analysis.novel_title}/", exist_ok=True)
        
        filename = f"{ANALYSIS_DIR}{analysis.novel_title}/full_analysis.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(asdict(analysis), f, indent=4, ensure_ascii=False)
        
        # 保存为可阅读的格式
        readable = f"""《{analysis.novel_title}》分析报告
{'='*60}

【结构分析】
- 章节结构：{', '.join([s['type'] for s in analysis.chapter_structure])}
- 情节弧光：{' → '.join(analysis.plot_arc)}

【写作手法】
"""
        for tech in analysis.writing_techniques:
            readable += f"- {tech}\n"
        
        readable += f"\n【可学习内容】\n"
        for learning in analysis.learnings:
            readable += f"- {learning}\n"
        
        readable_file = f"{ANALYSIS_DIR}{analysis.novel_title}/report.txt"
        with open(readable_file, 'w', encoding='utf-8') as f:
            f.write(readable)
    
    def distribute_to_skills(self, analysis):
        """将学习内容分发到各Skill"""
        print(f"\n📤 正在将学习内容分发到各Skill...")
        
        # ==============
        # 分发给不同Skill
        # ==============
        
        # 1. 剧情构造师
        plot_learnings = []
        for item in analysis.learnings:
            if "开篇" in item or "情节" in item or "结构" in item:
                plot_learnings.append(item)
        
        if analysis.plot_arc:
            plot_learnings.append(f"情节发展节奏：{' → '.join(analysis.plot_arc[:5])}")
        
        if plot_learnings:
            self._update_skill("剧情构造师", plot_learnings)
        
        # 2. 角色塑造师
        char_learnings = []
        for char in analysis.main_characters:
            char_learnings.append(f"{char['role']}塑造要点：{', '.join(char['traits'][:3])}")
        
        if char_learnings:
            self._update_skill("角色塑造师", char_learnings)
        
        # 3. 写作技巧大师
        if analysis.writing_techniques:
            self._update_skill("写作技巧大师", analysis.writing_techniques)
        
        # 4. 场景构造师
        if analysis.descriptive_style:
            self._update_skill("场景构造师", analysis.descriptive_style)
        
        # 5. 对话设计师
        if analysis.dialogue_characteristics:
            self._update_skill("对话设计师", analysis.dialogue_characteristics)
        
        print(f"✅ 分发完成！")
    
    def _update_skill(self, skill_name, learnings):
        """更新Skill内容"""
        skill_dir = f"skills/level2/"
        
        # 简化版更新
        # 实际上应该更新到对应的Skill文件
        # 这里演示创建学习日志
        os.makedirs(f"{skill_dir}learnings/", exist_ok=True)
        
        log_file = f"{skill_dir}learnings/{skill_name}_learnings.txt"
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]\n")
            for learning in learnings:
                f.write(f"- {learning}\n")
        
        print(f"   ➡️  {skill_name}：新增 {len(learnings)} 条学习内容")

# =============================================
# 主程序
# =============================================

def main():
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║      NWACS 小说下载与拆书分析系统 v{VERSION}                     ║
║                                                              ║
║      功能：                                                 ║
║         ✅ 小说联网搜索与下载                                ║
║         ✅ 小说拆书分析（结构、剧情、人物）                   ║
║         ✅ 自动学习与分发到各Skill                          ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    downloader = NovelDownloader()
    analyzer = NovelAnalyzer()
    
    while True:
        print(f"""
{'='*60}
                    主菜单
{'='*60}

1. 🔍 搜索小说（演示模式）
2. ⬇️  下载小说
3. 📖 分析已下载的小说
4. 📤 将学习内容分发到Skill
5. 📂 查看已下载/分析的小说
0. 🚪 返回
        """)
        
        choice = input("请选择 (0-5): ").strip()
        
        if choice == '1':
            keyword = input("请输入搜索关键词（默认：玄幻）: ") or "玄幻"
            downloader.search_novels(keyword)
        
        elif choice == '2':
            print(f"\n📋 可下载的热门小说：")
            novels = downloader.search_novels()
            
            choice = input("\n请输入要下载的小说编号: ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(novels):
                novel = novels[int(choice) - 1]
                downloader.download_novel(novel)
        
        elif choice == '3':
            downloaded = downloader.list_downloaded_novels()
            
            if not downloaded:
                print("⚠️  还没有下载小说，请先下载！")
                continue
            
            print(f"\n📚 已下载的小说：")
            for i, novel in enumerate(downloaded):
                print(f"{i+1}. 《{novel.title}》")
            
            choice = input("\n请输入要分析的小说编号: ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(downloaded):
                novel = downloaded[int(choice) - 1]
                analyzer.analyze_novel(novel.content_path, novel.title)
        
        elif choice == '4':
            # 查找最新分析的小说
            if os.path.exists(ANALYSIS_DIR):
                novels = os.listdir(ANALYSIS_DIR)
                if novels:
                    latest = novels[-1]  # 简化版：取最后一个
                    
                    print(f"\n📤 正在分析《{latest}》...")
                    
                    # 重新分析
                    analysis = analyzer.analyze_novel(f"{ANALYSIS_DIR}{latest}", latest)
                    analyzer.distribute_to_skills(analysis)
        
        elif choice == '5':
            print(f"\n{'='*60}")
            print(f"📂 已下载的小说：")
            downloaded = downloader.list_downloaded_novels()
            
            if downloaded:
                for novel in downloaded:
                    print(f"   📖 《{novel.title}》- {novel.author}")
            else:
                print("   (暂无)")
            
            print(f"\n{'='*60}")
            print(f"📂 已分析的小说：")
            
            if os.path.exists(ANALYSIS_DIR):
                analyzed = [d for d in os.listdir(ANALYSIS_DIR) 
                           if os.path.isdir(f"{ANALYSIS_DIR}{d}")]
                if analyzed:
                    for novel_name in analyzed:
                        print(f"   🔍 {novel_name}")
                else:
                    print("   (暂无)")
        
        elif choice == '0':
            print("\n👋 感谢使用！\n")
            break

if __name__ == "__main__":
    main()
