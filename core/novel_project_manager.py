#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 百万字长篇小说协作创作系统 - 增强版
核心功能：
1. 世界观框架生成
2. 人物框架生成
3. 剧情大纲生成
4. 章节标题生成
5. 伏笔追踪
6. 时间线管理
7. 人物一致性管理
8. 情节连续性跟踪
"""

import os
import sys
import json
from datetime import datetime
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Any, Optional

sys.stdout.reconfigure(encoding='utf-8')

VERSION = "2.0"
NOVEL_DIR = "novel_project/"

@dataclass
class Character:
    """角色数据模型"""
    name: str
    personality: str = ""
    appearance: str = ""
    background: str = ""
    special_abilities: List[str] = field(default_factory=list)
    goals: List[str] = field(default_factory=list)
    character_arc: List[str] = field(default_factory=list)
    first_appearance: int = 1
    last_appearance: int = 1
    relationships: Dict[str, str] = field(default_factory=dict)
    notes: str = ""

@dataclass
class PlotHook:
    """伏笔数据模型"""
    id: int
    name: str
    description: str
    set_in_chapter: int
    expected_resolve_chapter: int = 0
    resolved: bool = False
    resolve_chapter: int = 0
    notes: str = ""

@dataclass
class TimelineEvent:
    """时间线事件"""
    chapter: int
    title: str
    description: str
    event_type: str = "main"  # main, sub, character, world

@dataclass
class ChapterRecord:
    """章节记录"""
    num: int
    title: str
    summary: str = ""
    word_count: int = 0
    status: str = "draft"
    plot_hooks: List[int] = field(default_factory=list)  # 伏笔ID列表
    created_at: str = ""

@dataclass
class WorldFramework:
    """世界观框架"""
    world_type: str = ""  # 玄幻/修仙/都市/科幻等
    world_name: str = ""
    main_continent: str = ""
    power_system: str = ""
    cultivation_realms: List[str] = field(default_factory=list)
    main_factions: List[str] = field(default_factory=list)
    core_conflict: str = ""
    special_rules: List[str] = field(default_factory=list)

@dataclass
class CharacterFramework:
    """人物框架"""
    protagonist: Dict = field(default_factory=dict)
    female_leads: List[Dict] = field(default_factory=list)
    antagonists: List[Dict] = field(default_factory=list)
    supporting_chars: List[Dict] = field(default_factory=list)

@dataclass
class PlotFramework:
    """剧情框架"""
    main_plot: str = ""
    sub_plots: List[str] = field(default_factory=list)
    plot_arcs: List[Dict] = field(default_factory=list)
    total_chapters: int = 200

class NovelProjectManager:
    """小说项目管理器 - 核心协作系统"""

    def __init__(self, project_name="默认小说"):
        self.project_name = project_name
        self.project_dir = f"{NOVEL_DIR}{project_name}/"
        self._ensure_dirs()

        self.world_framework = WorldFramework()
        self.character_framework = CharacterFramework()
        self.plot_framework = PlotFramework()

        self.characters: Dict[str, Character] = {}
        self.plot_hooks: List[PlotHook] = []
        self.timeline: List[TimelineEvent] = []
        self.chapters: List[ChapterRecord] = []

        self._load_data()

    def _ensure_dirs(self):
        os.makedirs(self.project_dir, exist_ok=True)
        os.makedirs(f"{self.project_dir}chapters/", exist_ok=True)
        os.makedirs(f"{self.project_dir}frameworks/", exist_ok=True)

    def _load_data(self):
        """加载已有数据"""
        char_file = self.project_dir + "characters.json"
        if os.path.exists(char_file):
            with open(char_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.characters = {name: Character(**d) for name, d in data.items()}

        hooks_file = self.project_dir + "plot_hooks.json"
        if os.path.exists(hooks_file):
            with open(hooks_file, 'r', encoding='utf-8') as f:
                self.plot_hooks = [PlotHook(**h) for h in json.load(f)]

        timeline_file = self.project_dir + "timeline.json"
        if os.path.exists(timeline_file):
            with open(timeline_file, 'r', encoding='utf-8') as f:
                self.timeline = [TimelineEvent(**t) for t in json.load(f)]

        chapters_file = self.project_dir + "chapters.json"
        if os.path.exists(chapters_file):
            with open(chapters_file, 'r', encoding='utf-8') as f:
                self.chapters = [ChapterRecord(**c) for c in json.load(f)]

        framework_file = self.project_dir + "frameworks.json"
        if os.path.exists(framework_file):
            with open(framework_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if 'world' in data:
                    self.world_framework = WorldFramework(**data['world'])
                if 'character' in data:
                    self.character_framework = CharacterFramework(**data['character'])
                if 'plot' in data:
                    self.plot_framework = PlotFramework(**data['plot'])

    def _save_data(self):
        """保存所有数据"""
        os.makedirs(self.project_dir, exist_ok=True)

        with open(self.project_dir + "characters.json", 'w', encoding='utf-8') as f:
            json.dump({n: asdict(c) for n, c in self.characters.items()}, f, indent=4, ensure_ascii=False)

        with open(self.project_dir + "plot_hooks.json", 'w', encoding='utf-8') as f:
            json.dump([asdict(h) for h in self.plot_hooks], f, indent=4, ensure_ascii=False)

        with open(self.project_dir + "timeline.json", 'w', encoding='utf-8') as f:
            json.dump([asdict(t) for t in self.timeline], f, indent=4, ensure_ascii=False)

        with open(self.project_dir + "chapters.json", 'w', encoding='utf-8') as f:
            json.dump([asdict(c) for c in self.chapters], f, indent=4, ensure_ascii=False)

        with open(self.project_dir + "frameworks.json", 'w', encoding='utf-8') as f:
            json.dump({
                'world': asdict(self.world_framework),
                'character': asdict(self.character_framework),
                'plot': asdict(self.plot_framework)
            }, f, indent=4, ensure_ascii=False)

    # ==============
    # 框架生成功能
    # ==============

    def generate_world_framework(self, novel_type="玄幻修仙", main_theme="复仇与成长"):
        """生成世界观框架"""
        print(f"\n🌍 生成世界观框架...")

        self.world_framework = WorldFramework(
            world_type=novel_type,
            world_name="苍元大陆",
            main_continent="中洲",
            power_system="灵气修炼体系",
            cultivation_realms=[
                "炼气期（寿元150-200年）",
                "筑基期（寿元300-500年）",
                "金丹期（寿元800-1500年）",
                "元婴期（寿元3000-5000年）",
                "化神期（寿元1-3万年）",
                "炼虚期（寿元5-10万年）",
                "合体期（寿元20-50万年）",
                "大乘期（寿元100万年以上）",
                "渡劫期（永生或灰飞）"
            ],
            main_factions=[
                "正道七宗：苍云宗、太清宫、天机阁等",
                "魔道四派：血神教、万鬼宗等",
                "三大古派：太清宫（炼丹）、剑阁（剑道）、万法宗（万法）",
                "劫运教：神秘组织，背后操控修仙界"
            ],
            core_conflict=main_theme,
            special_rules=[
                "末法时代：灵气日益稀薄",
                "天道沉睡：世界规则紊乱",
                "长生会：修仙界隐藏的最大阴谋组织"
            ]
        )

        self._save_data()
        print(f"✅ 世界观框架生成完成！")
        return self.world_framework

    def generate_character_framework(self):
        """生成人物框架"""
        print(f"\n👤 生成人物框架...")

        self.character_framework = CharacterFramework(
            protagonist={
                "name": "顾长青",
                "age": 17,
                "personality": "谨慎、冷静、隐忍、智斗为先，典型的苟道流",
                "appearance": "眉清目秀，气质内敛，看似普通",
                "background": "家族被灭，父亲蒙冤而死",
                "abilities": ["望气之术", "窃运术", "毒术"],
                "goals": ["查清灭门真相", "复仇", "在修仙界存活"]
            },
            female_leads=[
                {
                    "name": "苏瑶",
                    "age": 18,
                    "personality": "温柔但有原则，外柔内刚",
                    "identity": "太清宫圣女",
                    "relationship": "红颜知己"
                },
                {
                    "name": "姜雪晴",
                    "age": 19,
                    "personality": "冷漠聪明，高冷傲娇",
                    "identity": "天机阁少阁主",
                    "relationship": "盟友/合作伙伴"
                },
                {
                    "name": "白骨夫人",
                    "age": "未知",
                    "personality": "妩媚狡猾，亦敌亦友",
                    "identity": "白骨谷主",
                    "relationship": "长辈旧识"
                }
            ],
            antagonists=[
                {
                    "name": "王天辰",
                    "identity": "苍云宗执法长老",
                    "status": "已死（被灭口）",
                    "behind": "劫运教"
                },
                {
                    "name": "劫运教",
                    "identity": "幕后黑手",
                    "goal": "控制修仙界"
                }
            ]
        )

        self._save_data()
        print(f"✅ 人物框架生成完成！")
        return self.character_framework

    def generate_plot_framework(self, total_chapters=200):
        """生成剧情框架"""
        print(f"\n📖 生成剧情框架...")

        volumes = []
        chapters_per_volume = 40

        volume_themes = [
            "凡人之路：觉醒与隐忍",
            "逃亡之路：追杀与成长",
            "纵横修仙：崭露头角",
            "长生之谜：揭开阴谋",
            "长夜将明：最终决战"
        ]

        for i, theme in enumerate(volume_themes):
            volumes.append({
                "name": f"第{i+1}卷：{theme}",
                "start_chapter": i * chapters_per_volume + 1,
                "end_chapter": (i + 1) * chapters_per_volume,
                "theme": theme
            })

        self.plot_framework = PlotFramework(
            main_plot="顾长青复仇，查清灭门案真相",
            sub_plots=[
                "父亲下落之谜",
                "长生会阴谋",
                "天道沉睡真相",
                "与三女的感情发展"
            ],
            plot_arcs=volumes,
            total_chapters=total_chapters
        )

        self._save_data()
        print(f"✅ 剧情框架生成完成！共{total_chapters}章，分为{len(volumes)}卷")
        return self.plot_framework

    # ==============
    # 章节标题生成
    # ==============

    def generate_chapter_titles(self, novel_theme="修仙复仇"):
        """生成所有章节标题"""
        print(f"\n📝 生成章节标题...")

        chapter_titles = []

        if novel_theme == "修仙复仇":
            base_titles = [
                # 第1卷（第1-40章）
                "末法时代", "望气之术", "父亲的遗产", "毒经救人", "十年之约",
                "初入苍云", "棋逢对手", "秘境开启", "劫运教阴谋", "暗夜逃亡",
                "苏瑶解毒", "长老试探", "暗中调查", "天机阁密约", "太清宫邀请",
                "劫运教伏击", "窃运术小成", "宗门大比", "王天成的阴谋", "秘境深处",
                "父亲真相", "幽冥毒龙传承", "姜雪晴的过去", "三方势力", "外门大比",
                "内门考核", "王天成出手", "绝境逢生", "真相大白", "十年之约终局",
                "神秘黑衣人", "苍云宗追杀", "白骨夫人相助", "逃亡路上", "进入西漠",
                "沙漠奇遇", "上古遗迹", "获得传承", "筑基成功", "第二卷开启",

                # 第2卷（第41-80章）
                "劫运教再现", "万鬼宗阴谋", "西漠之主", "白骨谷秘辛", "师父下落",
                "修炼突破", "金丹初期", "重返中洲", "故人重逢", "新的敌人",
                "万宝楼", "拍卖会风云", "势力初成", "建立根基", "招收弟子",
                "宗门大比预选", "技惊四座", "一路横扫", "冠军之争", "丰厚奖励",
                "太清宫之邀", "天机阁考验", "神秘任务", "深入敌后", "发现真相",
                "劫运教总部", "生死一线", "绝地逃生", "重大收获", "闭关突破",
                "金丹中期", "实力大增", "复仇开始", "重回苍云", "清算旧账",

                # 第3卷（第81-120章）
                "真相大白", "王天辰伏法", "新的征程", "踏上旅途", "各路英豪",
                "群雄汇聚", "天才云集", "暗中较量", "技压群雄", "一战成名",
                "扬名立万", "各方拉拢", "选择势力", "加入宗门", "核心弟子",
                "门派秘辛", "上古遗迹", "秘境探险", "获得宝物", "实力飞跃",
                "修为精进", "突破在即", "金丹后期", "大圆满", "元婴之劫",
                "渡劫成功", "元婴初期", "震惊修仙界", "各方反应", "新的挑战",
                "劫运教扩张", "修仙界动荡", "应对之策", "联盟成立", "共抗劫运",
                "大战将起", "首战告捷", "激烈交锋", "生死搏杀", "惨烈代价",

                # 第4卷（第121-160章）
                "战局稳定", "整顿休息", "情报收集", "深入调查", "劫运教秘密",
                "天道沉睡", "惊天真相", "远古秘辛", "上个纪元", "天道复苏",
                "关键线索", "寻访名师", "远古遗迹", "获得传承", "实力暴涨",
                "突破化神", "震惊天下", "劫运教恐慌", "疯狂反扑", "最终决战",
                "生死对决", "击败教主", "劫运教覆灭", "天道觉醒", "世界变化",
                "修仙界和平", "新的秩序", "顾长青的选择", "功成身退", "新的旅程",
                "告别故人", "踏上征途", "星辰大海", "无尽星空", "未知世界",

                # 第5卷（第161-200章）
                "异界降临", "新世界", "适应环境", "修炼体系", "重新开始",
                "结识新友", "卷入纷争", "展现天赋", "引起关注", "招揽势力",
                "建立势力", "发展壮大", "遭遇强敌", "生死危机", "绝地反击",
                "反败为胜", "声名远扬", "登上门派", "成为长老", "传授功法",
                "培养后辈", "发现回归之法", "准备回归", "撕裂虚空", "重返故土",
                "物是人非", "寻找故人", "重逢相聚", "共叙往事", "新的威胁",
                "应对威胁", "提升实力", "最终决战", "击败敌人", "守护家园",
                "和平到来", "修仙界繁荣", "传承延续", "长夜将明", "完美结局"
            ]

            chapter_titles = base_titles

        # 确保有200章
        while len(chapter_titles) < 200:
            chapter_titles.append(f"第{len(chapter_titles)+1}章：待补充")

        # 截取或补充到正好200章
        chapter_titles = chapter_titles[:200]

        # 生成章节记录
        self.chapters = []
        for i, title in enumerate(chapter_titles):
            record = ChapterRecord(
                num=i+1,
                title=title,
                summary="",
                status="outline"  # 大纲状态
            )
            self.chapters.append(record)

        self._save_data()
        print(f"✅ 章节标题生成完成！共{len(chapter_titles)}章")
        return chapter_titles

    # ==============
    # 伏笔管理
    # ==============

    def add_plot_hook(self, name, description, set_in_chapter, expected_resolve=0):
        """添加伏笔"""
        hook = PlotHook(
            id=len(self.plot_hooks) + 1,
            name=name,
            description=description,
            set_in_chapter=set_in_chapter,
            expected_resolve_chapter=expected_resolve
        )
        self.plot_hooks.append(hook)
        self._save_data()
        return hook

    def resolve_plot_hook(self, hook_id, resolve_chapter):
        """解决伏笔"""
        for hook in self.plot_hooks:
            if hook.id == hook_id:
                hook.resolved = True
                hook.resolve_chapter = resolve_chapter
                self._save_data()
                return True
        return False

    def get_unresolved_hooks(self):
        """获取未解决的伏笔"""
        return [h for h in self.plot_hooks if not h.resolved]

    def get_hooks_for_chapter(self, chapter_num):
        """获取某章节需要解决的伏笔"""
        return [h for h in self.plot_hooks if h.expected_resolve_chapter == chapter_num]

    # ==============
    # 时间线管理
    # ==============

    def add_timeline_event(self, chapter, title, description, event_type="main"):
        """添加时间线事件"""
        event = TimelineEvent(
            chapter=chapter,
            title=title,
            description=description,
            event_type=event_type
        )
        self.timeline.append(event)
        self.timeline.sort(key=lambda x: x.chapter)
        self._save_data()
        return event

    def get_timeline_for_chapter(self, chapter_num):
        """获取某章节的时间线"""
        return [t for t in self.timeline if t.chapter == chapter_num]

    # ==============
    # 人物管理
    # ==============

    def add_character(self, character: Character):
        """添加角色"""
        self.characters[character.name] = character
        self._save_data()
        return True

    def get_character_context(self, name) -> str:
        """获取角色上下文"""
        if name not in self.characters:
            return ""

        char = self.characters[name]
        return f"""{name}人物设定：
性格：{char.personality}
外貌：{char.appearance}
背景：{char.background}
特殊能力：{', '.join(char.special_abilities)}
目标：{', '.join(char.goals)}
首次出场：第{char.first_appearance}章
最近出场：第{char.last_appearance}章"""

    # ==============
    # 输出框架
    # ==============

    def export_frameworks_to_txt(self):
        """导出框架为可读文本"""
        output = f"""
{'='*80}
《{self.project_name}》完整框架
{'='*80}

生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{'='*80}
一、世界观框架
{'='*80}
类型：{self.world_framework.world_type}
世界名：{self.world_framework.world_name}
主要大陆：{self.world_framework.main_continent}
修炼体系：{self.world_framework.power_system}

修炼境界：
"""
        for realm in self.world_framework.cultivation_realms:
            output += f"  - {realm}\n"

        output += f"""
主要势力：
"""
        for faction in self.world_framework.main_factions:
            output += f"  - {faction}\n"

        output += f"""
核心冲突：{self.world_framework.core_conflict}

特殊规则：
"""
        for rule in self.world_framework.special_rules:
            output += f"  - {rule}\n"

        output += f"""
{'='*80}
二、人物框架
{'='*80}
主角：{self.character_framework.protagonist.get('name', '待定')}
性格：{self.character_framework.protagonist.get('personality', '')}
能力：{', '.join(self.character_framework.protagonist.get('abilities', []))}

女主：
"""
        for fl in self.character_framework.female_leads:
            output += f"  - {fl.get('name', '')}：{fl.get('identity', '')}，{fl.get('personality', '')}\n"

        output += f"""
{'='*80}
三、剧情框架
{'='*80}
主线：{self.plot_framework.main_plot}

辅线：
"""
        for sp in self.plot_framework.sub_plots:
            output += f"  - {sp}\n"

        output += f"""
分卷结构：
"""
        for arc in self.plot_framework.plot_arcs:
            output += f"  {arc['name']}（第{arc['start_chapter']}-{arc['end_chapter']}章）\n"
            output += f"    主题：{arc['theme']}\n"

        output += f"""
{'='*80}
四、章节标题（共{len(self.chapters)}章）
{'='*80}
"""
        for ch in self.chapters:
            output += f"第{ch.num:03d}章：{ch.title}\n"

        output += f"""
{'='*80}
五、伏笔追踪
{'='*80}
总伏笔数：{len(self.plot_hooks)}
已解决：{len([h for h in self.plot_hooks if h.resolved])}
未解决：{len([h for h in self.plot_hooks if not h.resolved])}

未解决伏笔：
"""
        for h in self.get_unresolved_hooks():
            output += f"  [{h.id}] {h.name}（第{h.set_in_chapter}章埋下，预计第{h.expected_resolve_chapter}章解决）\n"
            output += f"      {h.description}\n"

        # 保存
        os.makedirs(f"{self.project_dir}frameworks/", exist_ok=True)
        with open(f"{self.project_dir}frameworks/完整框架.txt", 'w', encoding='utf-8') as f:
            f.write(output)

        print(f"✅ 框架已导出到：{self.project_dir}frameworks/完整框架.txt")
        return output

    def print_status(self):
        """打印状态"""
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║                  《{self.project_name}》项目状态                    ║
╚══════════════════════════════════════════════════════════════╝

📊 数据统计：
   角色数：{len(self.characters)}
   章节数：{len(self.chapters)}
   伏笔数：{len(self.plot_hooks)}（已解决：{len([h for h in self.plot_hooks if h.resolved])}）
   时间线事件：{len(self.timeline)}

📋 框架状态：
   世界观：{'✅ 已生成' if self.world_framework.world_name else '❌ 未生成'}
   人物：{'✅ 已生成' if self.character_framework.protagonist else '❌ 未生成'}
   剧情：{'✅ 已生成' if self.plot_framework.main_plot else '❌ 未生成'}

📁 项目目录：{self.project_dir}
""")


def main():
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     NWACS 百万字长篇小说协作创作系统 v{VERSION}                      ║
║                                                              ║
║     功能：                                                   ║
║       ✅ 世界观框架生成                                      ║
║       ✅ 人物框架生成                                        ║
║       ✅ 剧情大纲生成                                        ║
║       ✅ 章节标题生成                                        ║
║       ✅ 伏笔追踪                                           ║
║       ✅ 时间线管理                                          ║
║       ✅ 人物一致性管理                                      ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)

    manager = NovelProjectManager("长夜将明")

    while True:
        print(f"""
{'='*60}
主菜单
{'='*60}
1. 生成完整框架（世界观+人物+剧情）
2. 生成章节标题（200章）
3. 添加伏笔
4. 添加时间线事件
5. 导出框架为TXT
6. 打印项目状态
0. 退出
""")
        choice = input("请选择: ").strip()

        if choice == '1':
            manager.generate_world_framework()
            manager.generate_character_framework()
            manager.generate_plot_framework()
            print("✅ 完整框架生成完成！")

        elif choice == '2':
            titles = manager.generate_chapter_titles()
            print(f"✅ 生成了{len(titles)}章标题")

        elif choice == '3':
            name = input("伏笔名称: ")
            desc = input("伏笔描述: ")
            chapter = int(input("埋下章节: "))
            resolve = int(input("预计解决章节(0=未知): ") or "0")
            manager.add_plot_hook(name, desc, chapter, resolve)
            print("✅ 伏笔已添加！")

        elif choice == '4':
            chapter = int(input("章节: "))
            title = input("事件标题: ")
            desc = input("事件描述: ")
            etype = input("事件类型(main/sub/character/world): ") or "main"
            manager.add_timeline_event(chapter, title, desc, etype)
            print("✅ 时间线事件已添加！")

        elif choice == '5':
            manager.export_frameworks_to_txt()
            print("✅ 框架已导出！")

        elif choice == '6':
            manager.print_status()

        elif choice == '0':
            print("\n👋 再见！")
            break


if __name__ == "__main__":
    main()
