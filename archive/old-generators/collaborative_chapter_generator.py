#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 协作式百万字章节生成系统
整合：
- 一致性检查
- 角色管理
- 世界观参考
- 多Skill协作
"""

import os
import sys
import json
import time
import threading
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

VERSION = "2.0"

# 导入我们的模块
try:
    from novel_project_manager import NovelProjectManager, Character
    from novel_quality_checker import ConsistencyChecker
except:
    pass

# =============================================
# 百万字小说章节规划（完整）
# =============================================

NOVEL_PLAN = {
    "title": "长生仙逆",
    "total_chapters": 200,
    "volumes": [
        {
            "id": 1,
            "name": "第一卷：凡人之路",
            "chapters": 20,
            "theme": "顾长青觉醒，踏上修仙路，初步接触修仙界",
            "chapter_titles": [
                "末法时代", "望气之术", "父亲的遗产", "毒经救人", "十年之约",
                "初入苍云", "棋逢对手", "秘境开启", "劫运教阴谋", "暗夜逃亡",
                "苏瑶解毒", "长老试探", "暗中调查", "天机阁密约", "太清宫邀请",
                "劫运教伏击", "窃运术小成", "宗门大比", "王天成的阴谋", "秘境深处"
            ]
        },
        {
            "id": 2,
            "name": "第二卷：初入仙门",
            "chapters": 20,
            "theme": "外门生活，积蓄实力，第一次与王天辰正式交锋",
            "chapter_titles": [
                "父亲真相", "幽冥毒龙传承", "姜雪晴的过去", "三方势力", "外门大比",
                "内门考核", "王天成出手", "绝境逢生", "真相大白", "十年之约",
                "第一个师父", "修炼路上", "洞府生活", "外门历练", "第一次杀人",
                "血色试炼", "秘境寻宝", "丹炉崩溃", "宗门追杀", "逃出生天"
            ]
        },
        {
            "id": 3,
            "name": "第三卷：外门风云",
            "chapters": 20,
            "theme": "在外门崛起，名声渐显，智斗不断",
            "chapter_titles": [
                "再次相见", "小露一手", "反杀", "第一次交锋", "声名鹊起",
                "丹会", "技惊四座", "炼丹天才", "王动的心思", "招揽",
                "打脸", "我拒绝", "冲突", "执法队", "谁给你的勇气",
                "墨岩真人", "外门大比开始", "第一战", "震惊", "黑马"
            ]
        },
        # 继续添加更多卷...
    ]
}

# =============================================
# 生成系统
# =============================================

class CollaborativeNovelGenerator:
    """协作式百万字小说生成器"""
    
    def __init__(self):
        self.project = None
        self.checker = None
        self._init_project()
    
    def _init_project(self):
        """初始化项目"""
        try:
            self.project = NovelProjectManager("长生仙逆")
            self.checker = ConsistencyChecker("长生仙逆")
        except:
            print("⚠️  项目管理器初始化失败，继续运行")
    
    def build_context(self, chapter_num, title, summary, prev_chapters_content):
        """构建完整上下文提示"""
        
        context = f"""你是一位优秀的玄幻小说作家，请创作《长生仙逆》第{chapter_num}章。

标题：{title}

摘要：{summary}

要求：
1. 每章至少4000字，细节丰富，有画面感
2. 保持《剑来》风格：注重对话，三观正，有哲理
3. 苟道流：主角顾长青谨慎、隐忍，不鲁莽
4. 智斗为主：不靠金手指，靠智慧取胜
5. 去AI痕迹：避免模板化，语言自然
6. 情节连贯：与前面章节保持一致
7. 画面感：远景→中景→特写，有镜头感

人物设定：
- 顾长青：谨慎、隐忍、擅长毒术
- 苏瑶：太清宫圣女，温柔但有原则
- 姜雪晴：天机阁少阁主，冷漠聪明
- 王天辰：苍云宗长老，表面正义，实则虚伪

前情回顾：
{prev_chapters_content[:3000]}

请开始创作！"""
        
        return context
    
    def generate_chapter(self, chapter_num, title, summary, prev_chapters):
        """生成单章"""
        print(f"\n{'='*60}")
        print(f"✍️ 正在生成第{chapter_num}章：{title}")
        print(f"{'='*60}")
        
        # 构建上下文
        context = self.build_context(chapter_num, title, summary, prev_chapters)
        
        # 调用API生成
        content = self._call_deepseek(context)
        
        if content:
            # 一致性检查
            print(f"\n🔍 正在检查一致性...")
            issues, score = self.checker.run_full_check(chapter_num, title, content, prev_chapters)
            
            # 保存章节
            filename = self._save_chapter(chapter_num, title, content)
            print(f"✅ 第{chapter_num}章已保存：{filename}")
            print(f"⭐ 质量评分：{score}/100")
            
            return content, score
        
        return None, 0
    
    def _call_deepseek(self, prompt):
        """调用DeepSeek API"""
        config = self._load_config()
        
        if not config or not config.get('api_key'):
            print("❌ API Key未配置！")
            return None
        
        url = config.get('base_url', 'https://api.deepseek.com/v1') + '/chat/completions'
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {config.get("api_key")}'
        }
        
        data = {
            'model': config.get('model', 'deepseek-v4-pro'),
            'messages': [
                {'role': 'system', 'content': '你是一位优秀的玄幻小说作家，擅长创作长篇小说'},
                {'role': 'user', 'content': prompt}
            ],
            'temperature': 0.85,
            'max_tokens': 12000
        }
        
        try:
            import urllib.request
            
            print(f"\r⏳ 正在生成...", end='', flush=True)
            
            req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)
            with urllib.request.urlopen(req, timeout=180) as response:
                result = json.loads(response.read().decode('utf-8'))
                print(f"\r✅ 生成成功！", end='', flush=True)
                return result['choices'][0]['message']['content']
        
        except Exception as e:
            print(f"\r❌ 生成失败：{e}", end='', flush=True)
            return None
    
    def _save_chapter(self, num, title, content):
        """保存章节"""
        os.makedirs('output/', exist_ok=True)
        filename = f'output/第{num:03d}章_{title}.txt'
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"第{num}章：{title}\n\n")
            f.write(content)
        
        return filename
    
    def _load_config(self):
        """加载配置"""
        config = {}
        if os.path.exists('config.json'):
            with open('config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
        return config
    
    def generate_volume(self, volume_id, start_from_chapter=1):
        """生成整卷"""
        volume = NOVEL_PLAN['volumes'][volume_id - 1]
        
        print(f"\n{'='*60}")
        print(f"📖 开始生成{volume['name']}")
        print(f"{'='*60}")
        
        all_chapters = []
        total_score = 0
        
        # 获取前面章节内容
        prev_chapters = ""
        for i in range(1, volume_id):
            prev_chapters += f"\n第{i}卷\n"
        
        start_idx = start_from_chapter - 1
        
        for idx in range(start_idx, min(volume['chapters'], len(volume['chapter_titles']))):
            actual_chapter_num = (volume_id - 1) * 20 + (idx + 1)
            title = volume['chapter_titles'][idx]
            
            content, score = self.generate_chapter(
                actual_chapter_num, title, f"{volume['theme']} - {title}", prev_chapters
            )
            
            if content:
                all_chapters.append(content)
                total_score += score
                
                # 更新前情
                prev_chapters += f"\n第{actual_chapter_num}章摘要：{title}\n"
                
                # 每5章暂停一次，检查进度
                if (idx + 1) % 5 == 0 and (idx + 1) < len(volume['chapter_titles']):
                    print(f"\n{'='*60}")
                    print(f"✅ 第{idx + 1}章/20章完成")
                    print(f"⏳ 即将开始第{idx + 2}章")
                    print(f"{'='*60}")
                    
                    choice = input("\n继续下一章？(yes/no): ").strip().lower()
                    if choice != 'yes' and choice != 'y':
                        print("已暂停。")
                        break
        
        # 整合该卷
        if all_chapters:
            avg_score = total_score / len(all_chapters)
            print(f"\n{'='*60}")
            print(f"🎉 {volume['name']}完成！")
            print(f"⭐ 平均质量：{avg_score:.1f}/100")
            print(f"{'='*60}")
            
            self._integrate_volume(volume_id, all_chapters)
    
    def _integrate_volume(self, volume_id, chapters):
        """整合成卷"""
        volume = NOVEL_PLAN['volumes'][volume_id - 1]
        
        print(f"\n💾 整合{volume['name']}...")
        
        volume_content = f"\n{'='*80}\n"
        volume_content += f"{volume['name']}\n"
        volume_content += f"{'='*80}\n\n"
        
        for idx, chapter_content in enumerate(chapters):
            volume_content += chapter_content
            volume_content += f"\n\n{'='*80}\n\n"
        
        os.makedirs('output/volumes/', exist_ok=True)
        filename = f'output/volumes/第{volume_id}卷_完整.txt'
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(volume_content)
        
        print(f"✅ 第{volume_id}卷已保存：{filename}")

def main():
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║       NWACS 协作式百万字长篇小说生成系统 v{VERSION}                  ║
║                                                              ║
║     功能：                                                  ║
║        ✅ 规划式章节生成                                      ║
║        ✅ 人物一致性保证                                      ║
║        ✅ 情节连贯性检查                                      ║
║        ✅ 质量自动评分                                        ║
║        ✅ 每5卷自动整合                                        ║
║                                                              ║
║     目标：200章，100万字+                                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    generator = CollaborativeNovelGenerator()
    
    while True:
        print(f"\n{'='*60}")
        print(f"生成菜单")
        print(f"{'='*60}")
        print(f"1. 生成单章")
        print(f"2. 生成整卷（20章）")
        print(f"3. 从指定章节继续")
        print(f"4. 整合已生成的章节为卷")
        print(f"0. 返回")
        
        choice = input("\n请选择: ").strip()
        
        if choice == '1':
            chapter_num = int(input("请输入章节号: "))
            title = input("请输入标题: ")
            summary = input("请输入摘要: ")
            generator.generate_chapter(chapter_num, title, summary, "")
        
        elif choice == '2':
            volume_id = int(input("请输入卷号 (1-10): "))
            generator.generate_volume(volume_id)
        
        elif choice == '3':
            volume_id = int(input("请输入卷号: "))
            start_from = int(input("从第章开始: "))
            generator.generate_volume(volume_id, start_from)
        
        elif choice == '4':
            print("⚠️  功能开发中...")
        
        elif choice == '0':
            break

if __name__ == "__main__":
    main()
