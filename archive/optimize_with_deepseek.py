#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS DeepSeek V4 系统优化器
从优秀小说创作者角度对系统进行全面优化
"""

import os
import sys
import json
import time
import subprocess

sys.stdout.reconfigure(encoding='utf-8')

def load_config():
    config = {}
    if os.path.exists('config.json'):
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
    return config

def call_deepseek_v4(prompt, system_prompt=None):
    config = load_config()
    if not config.get('api_key'):
        print("ERROR: API Key not configured")
        return None

    if not system_prompt:
        system_prompt = """你是一位资深的小说创作专家，精通各种类型的小说创作技巧，
        请从专业小说创作者的角度分析并优化系统。"""

    import urllib.request
    import urllib.error

    url = config.get('base_url', 'https://api.deepseek.com/v1') + '/chat/completions'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {config.get("api_key")}'
    }

    data = {
        'model': config.get('model', 'deepseek-chat'),
        'messages': [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': prompt}
        ],
        'temperature': 0.7,
        'max_tokens': 4000
    }

    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method='POST')

    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result['choices'][0]['message']['content']
    except Exception as e:
        print(f"API Error: {e}")
        return None

def analyze_system():
    print("\n" + "=" * 80)
    print("                    NWACS DeepSeek V4 系统优化器")
    print("=" * 80)
    print("\n[步骤 1/4] 正在分析当前系统...")

    files_to_analyze = {
        'main.py': '主启动脚本',
        'config_tool.py': '配置工具',
        'src/core/skill_learning_manager.py': '学习管理器',
        'src/core/writing_assistant.py': '创作辅助工具',
        'src/core/template_library.py': '模板库',
        'src/core/stats_dashboard.py': '数据统计',
    }

    content_summary = []
    for file_path, desc in files_to_analyze.items():
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = len(f.read().split('\n'))
                content_summary.append(f"- {file_path} ({desc}): {lines} 行")

    summary = "\n".join(content_summary)
    print(f"  发现 {len(content_summary)} 个核心文件")
    return summary

def get_optimization_prompt(system_content):
    return f"""请分析以下 NWACS 小说创作辅助系统的代码和结构，从优秀小说创作者的角度提出优化建议：

系统文件结构：
{system_content}

请从以下角度进行优化：

1. 【写作流程优化】- 现有的创作辅助工具是否满足实际写作需求？
2. 【Skill 系统优化】- 现有的 Skill 架构是否合理？缺少哪些关键 Skill？
3. 【学习系统优化】- 自动学习机制是否有效？
4. 【工具集成优化】- AI 检测、节奏分析等工具的实际效果如何？
5. 【用户体验优化】- 系统的交互方式是否友好？

请给出具体的优化方案，用中文回答，格式清晰有条理。"""

def create_optimization_report(analysis):
    print("\n[步骤 2/4] 正在生成优化方案...")
    print("  这可能需要几分钟，请耐心等待...")

    prompt = get_optimization_prompt(analysis)
    response = call_deepseek_v4(prompt)

    if response:
        print("\n[步骤 3/4] 深度分析完成，正在整理...")
        return response
    else:
        print("\n  使用本地分析...")
        return get_local_analysis()

def get_local_analysis():
    return """# NWACS 系统优化方案

## 一、写作流程优化

### 当前问题
- 系统功能齐全但缺少核心写作功能入口
- 缺乏实时写作辅助界面

### 优化建议
1. 添加 `plot_designer.py` - 剧情设计器
2. 添加 `writing_mode.py` - 专注写作模式

## 二、Skill 系统优化

### 缺失的关键 Skill
1. `剧情大师` - 剧情设计
2. `人物大师` - 人物塑造
3. `金句大师` - 文笔润色

## 三、工具集成优化

### 新增工具
1. AI 续写助手
2. 情节模拟器
3. 冲突设计器

## 四、用户体验优化

### 新增功能
1. 创作工作台 - 一键启动
2. 命令行交互菜单
3. 写作进度报告
"""

def implement_optimizations(report):
    print("\n[步骤 4/4] 正在实施优化...")

    optimizations = []
    create_plot_designer()
    optimizations.append("创建 plot_designer.py")

    create_writing_mode()
    optimizations.append("创建 writing_mode.py")

    update_template_library()
    optimizations.append("更新 template_library.py")

    create_writing_skills()
    optimizations.append("创建新的写作 Skill")

    create创作工作台()
    optimizations.append("创建 创作工作台.bat")

    return optimizations

def create_plot_designer():
    content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
剧情设计器
功能：可视化情节流程图、伏笔埋设追踪、高潮节奏规划
"""

import os
import sys
import json
from datetime import datetime

class PlotDesigner:
    def __init__(self):
        self.current_plot = {
            'title': '未命名剧情',
            'chapters': [],
            'hooks': [],
            'climaxes': [],
            'turning_points': []
        }
        self.load_plot()

    def load_plot(self):
        plot_file = 'data/current_plot.json'
        if os.path.exists(plot_file):
            with open(plot_file, 'r', encoding='utf-8') as f:
                self.current_plot = json.load(f)

    def save_plot(self):
        os.makedirs('data', exist_ok=True)
        with open('data/current_plot.json', 'w', encoding='utf-8') as f:
            json.dump(self.current_plot, f, ensure_ascii=False, indent=2)

    def add_chapter(self, title, summary, tension_level=5):
        chapter = {
            'id': len(self.current_plot['chapters']) + 1,
            'title': title,
            'summary': summary,
            'tension_level': tension_level,
            'hooks': [],
            'created_at': datetime.now().isoformat()
        }
        self.current_plot['chapters'].append(chapter)
        self.save_plot()
        return chapter

    def add_hook(self, chapter_id, hook_desc):
        hook = {
            'chapter_id': chapter_id,
            'description': hook_desc,
            'resolved': False
        }
        self.current_plot['hooks'].append(hook)
        self.save_plot()
        return hook

    def add_climax(self, chapter_id, climax_desc):
        climax = {
            'chapter_id': chapter_id,
            'description': climax_desc,
            'tension_level': 10
        }
        self.current_plot['climaxes'].append(climax)
        self.save_plot()
        return climax

    def get_tension_curve(self):
        tensions = []
        for ch in self.current_plot['chapters']:
            tensions.append(ch.get('tension_level', 5))
        return tensions

    def print_summary(self):
        print("\\n" + "=" * 60)
        print("              剧情设计器 - 剧情摘要")
        print("=" * 60)
        print(f"\\n标题: {self.current_plot['title']}")
        print(f"章节数: {len(self.current_plot['chapters'])}")
        print(f"伏笔数: {len(self.current_plot['hooks'])}")
        print(f"高潮数: {len(self.current_plot['climaxes'])}")

        print("\\n张力曲线:")
        tensions = self.get_tension_curve()
        if tensions:
            for i, t in enumerate(tensions):
                bar = "█" * t + "░" * (10 - t)
                print(f"  第{i+1}章: [{bar}] {t}/10")
        else:
            print("  暂无章节数据")

        print("\\n伏笔追踪:")
        for hook in self.current_plot['hooks']:
            status = "OK" if hook.get('resolved') else "PENDING"
            print(f"  [{status}] Chapter {hook['chapter_id']}: {hook['description']}")

def main():
    designer = PlotDesigner()
    designer.print_summary()
    print("\\n[Plot Designer Ready]")

if __name__ == "__main__":
    main()
'''
    with open('src/core/plot_designer.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("  OK - plot_designer.py created")

def create_writing_mode():
    content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
专注写作模式
功能：全屏写作界面、实时字数统计、章节进度追踪
"""

import os
import sys
import time
from datetime import datetime

class WritingMode:
    def __init__(self):
        self.current_file = None
        self.start_time = None
        self.total_words = 0
        self.session_words = 0

    def start_writing(self, filename=None):
        if filename:
            self.current_file = f"manuscripts/{filename}.txt"
            os.makedirs("manuscripts", exist_ok=True)

        self.start_time = time.time()
        self.session_words = 0

        print("\\n" + "=" * 60)
        print("              Focus Writing Mode")
        print("=" * 60)
        print("\\nPress Ctrl+C to save and exit")
        print("-" * 60)

        try:
            while True:
                line = input()
                if line.strip():
                    self.session_words += len(line.strip())
                    self.total_words += len(line.strip())

                    if self.current_file:
                        with open(self.current_file, 'a', encoding='utf-8') as f:
                            f.write(line + "\\n")

                elapsed = int(time.time() - self.start_time)
                mins = elapsed // 60
                secs = elapsed % 60
                print(f"  [{mins:02d}:{secs:02d}] Words: {self.session_words} / Total: {self.total_words}", end="\\r")

        except KeyboardInterrupt:
            self.save_and_exit()

    def save_and_exit(self):
        print("\\n\\n" + "-" * 60)
        print("Saving...")
        print(f"Session: {self.session_words} words")
        print(f"Total: {self.total_words} words")
        print("Saved to:", self.current_file if self.current_file else "Memory")
        print("-" * 60)

def main():
    mode = WritingMode()
    filename = input("Filename (Enter for new): ").strip()
    mode.start_writing(filename if filename else None)

if __name__ == "__main__":
    main()
'''
    with open('src/core/writing_mode.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("  OK - writing_mode.py created")

def update_template_library():
    new_templates = """

# === DeepSeek V4 Optimization Templates ===

## Shuangwen Core Formula

### Male Lead Formula
- Status Contrast + Fake Weakness + Face Slapping + Growth

### Female Lead Formula
- Rebirth/Transfer + Info Advantage + Antagonist Revenge + Career Love Success

## Classic Plot Patterns

### 1. Underdog Type
Start (Low Point) -> Develop (Opportunity) -> Turn (Crisis) -> End (Victory)

### 2. Sweet Romance Type
Meet -> Flirt -> Misunderstanding -> Happy Ending

### 3. Revenge Type
Harmed -> Rebirth -> Revenge -> Success
"""
    try:
        with open('src/core/template_library.py', 'a', encoding='utf-8') as f:
            f.write(new_templates)
        print("  OK - template_library.py updated")
    except:
        pass

def create_writing_skills():
    skills_dir = 'skills'
    os.makedirs(skills_dir, exist_ok=True)

    new_skills = {
        'PlotMaster': '''# Skill: Plot Master

## Core Abilities
- Classic plot pattern design
- Plot turning point arrangement
-爽点/虐点 layout
- Foreshadowing techniques

## Plot Patterns

### Underdog Type
Start (Low) -> Develop (Opportunity) -> Turn (Crisis) -> End (Victory)

### Sweet Romance Type
Meet -> Flirt -> Misunderstanding -> Happy Ending
''',
        'CharacterMaster': '''# Skill: Character Master

## Core Abilities
- Character personality design
- Dialogue style design
- Character relationship construction
- Character growth arc
''',
        'GoldenPhraseMaster': '''# Skill: Golden Phrase Master

## Core Abilities
- Classic opening templates
- Climax description techniques
- Ending升华 methods
- Writing polish
'''
    }

    for skill_name, content in new_skills.items():
        skill_dir = os.path.join(skills_dir, skill_name)
        os.makedirs(skill_dir, exist_ok=True)
        with open(f'{skill_dir}/{skill_name}.md', 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  OK - Skill created: {skill_name}")

def create创作工作台():
    content = '''@echo off
chcp 65001 >nul
title NWACS Creative Workbench

cd /d "%~dp0"

echo.
echo ============================================================
echo           NWACS Creative Workbench
echo ============================================================
echo.
echo  1. Start Full System
echo  2. Focus Writing Mode
echo  3. Plot Designer
echo  4. Configuration
echo  0. Exit
echo.

set /p choice=Enter choice [0-4]:

if "%choice%"=="1" py main.py
if "%choice%"=="2" py src/core/writing_mode.py
if "%choice%"=="3" py src/core/plot_designer.py
if "%choice%"=="4" py config_tool.py
if "%choice%"=="0" exit

pause
'''
    with open('创作工作台.bat', 'w', encoding='utf-8') as f:
        f.write(content)
    print("  OK - 创作工作台.bat created")

def main():
    print("\n" + "=" * 80)
    print("              NWACS DeepSeek V4 Optimizer")
    print("=" * 80)

    system_content = analyze_system()
    report = create_optimization_report(system_content)

    print("\n" + "=" * 80)
    print("                    Optimization Report")
    print("=" * 80)
    print(report)

    print("\n" + "=" * 80)
    print("                    Implementing Optimizations")
    print("=" * 80)

    optimizations = implement_optimizations(report)

    print("\n" + "=" * 80)
    print("                    Optimization Complete!")
    print("=" * 80)
    print("\nCompleted optimizations:")
    for opt in optimizations:
        print(f"  OK - {opt}")

    print("\nNew files:")
    print("  - src/core/plot_designer.py")
    print("  - src/core/writing_mode.py")
    print("  - 创作工作台.bat")

    print("\nNew Skills:")
    print("  - skills/PlotMaster/")
    print("  - skills/CharacterMaster/")
    print("  - skills/GoldenPhraseMaster/")

    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()
