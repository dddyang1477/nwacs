#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 书籍学习提炼系统 v2.0
支持内存模式学习、临时文件管理、小说项目独立文件夹
"""

import os
import sys
import json
import time
import tempfile
import shutil
from datetime import datetime, timedelta

sys.stdout.reconfigure(encoding='utf-8')

VERSION = "2.0"
LEARNING_DIR = "skills/level2/learnings/"
TEMP_DIR = "temp/"
NOVELS_DIR = "novels/"

class BookLearningSystem:
    """书籍学习提炼系统"""

    def __init__(self, memory_only=False, temp_expire_days=7):
        self.memory_only = memory_only
        self.temp_expire_days = temp_expire_days
        self.learned_count = 0
        self.learned_content = []
        
        if not memory_only:
            os.makedirs(LEARNING_DIR, exist_ok=True)
            os.makedirs(TEMP_DIR, exist_ok=True)
            self._clean_expired_temp_files()

    def _clean_expired_temp_files(self):
        """清理过期的临时文件"""
        now = datetime.now()
        for filename in os.listdir(TEMP_DIR):
            filepath = os.path.join(TEMP_DIR, filename)
            if os.path.isfile(filepath):
                mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
                if (now - mtime).days >= self.temp_expire_days:
                    os.remove(filepath)
                    print(f"  🗑️ 清理过期临时文件: {filename}")

    def _save_learning(self, content, category):
        """保存学习内容（根据模式决定是否写入文件）"""
        self.learned_content.append({"category": category, "content": content})
        
        if self.memory_only:
            self.learned_count += 1
            return
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{LEARNING_DIR}{category}_{timestamp}.txt"

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"学习时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*50 + "\n")
            f.write(content)

        self.learned_count += 1

    def _create_temp_file(self, content, prefix="learning_"):
        """创建临时文件，会自动过期删除"""
        fd, path = tempfile.mkstemp(suffix='.txt', prefix=prefix, dir=TEMP_DIR)
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(content)
        return path

    def learn_writing_textbooks(self):
        """学习写作教材"""
        books = [
            {"title": "故事-罗伯特麦基", "category": "写作教材",
             "core_points": ["故事的本质是冲突", "三幕式结构：开端-对抗-结局", 
                            "人物弧光的重要性", "主题必须通过故事来表达", "场景必须有转折点"],
             "key_concepts": ["结构", "人物", "主题", "冲突", "节奏"]},
            {"title": "故事写作大师班-约翰克卢碧", "category": "写作教材",
             "core_points": ["从想法到故事的转化技巧", "人物动机与欲望的设计",
                            "场景构建的层次", "对话的潜台词运用", "修改与编辑的艺术"],
             "key_concepts": ["创意转化", "人物动机", "场景层次", "潜台词"]},
            {"title": "九宫格写作法", "category": "写作方法",
             "core_points": ["9宫格创意发散法", "中心主题与8个关联点",
                            "快速构建故事框架", "激发创意联想", "角色与情节的多维展开"],
             "key_concepts": ["创意发散", "框架构建", "多维展开"]},
            {"title": "卡片笔记写作法", "category": "写作方法",
             "core_points": ["卢曼卡片盒系统", "知识的网络化连接",
                            "原子化写作单元", "非线性创作流程", "积累式写作策略"],
             "key_concepts": ["知识网络", "原子化", "非线性"]},
            {"title": "模板写作法", "category": "写作方法",
             "core_points": ["模块化写作结构", "场景模板库建设",
                            "高效产出技巧", "类型小说套路拆解", "快速启动写作"],
             "key_concepts": ["模块化", "高效产出", "套路拆解"]},
            {"title": "写出我心-娜塔莉戈德堡", "category": "写作心灵",
             "core_points": ["自由书写练习", "写作是一种修行",
                            "找到自己的声音", "克服写作障碍", "倾听内心的声音"],
             "key_concepts": ["自由书写", "写作修行", "个人声音"]},
            {"title": "学会写作-粥佐罗", "category": "写作教材",
             "core_points": ["写作的底层逻辑", "选题与标题技巧",
                            "结构化表达方法", "用户思维写作", "持续输出策略"],
             "key_concepts": ["底层逻辑", "用户思维", "持续输出"]},
            {"title": "小说的骨架-凯蒂维兰德", "category": "写作教材",
             "core_points": ["提纲的重要性", "故事结构设计",
                            "人物弧线规划", "情节衔接技巧", "节奏把控方法"],
             "key_concepts": ["提纲", "结构设计", "节奏把控"]},
            {"title": "小说课-毕飞宇", "category": "文学评论",
             "core_points": ["小说的细节之美", "语言的分寸感",
                            "视角的选择", "留白的艺术", "节奏的把控"],
             "key_concepts": ["细节", "语言分寸", "留白"]},
            {"title": "这样写出好故事-詹姆斯贝尔", "category": "写作教材",
             "core_points": ["场景的功能", "人物塑造技巧",
                            "悬念设置方法", "情感共鸣营造", "故事逻辑构建"],
             "key_concepts": ["场景功能", "悬念", "情感共鸣"]}
        ]

        for book in books:
            print(f"  📚 学习：{book['title']}")
            content = f"【{book['category']}】{book['title']}\n\n核心要点：\n"
            for i, point in enumerate(book['core_points'], 1):
                content += f"{i}. {point}\n"
            content += f"\n关键词：{'、'.join(book['key_concepts'])}\n"
            self._save_learning(content, book['category'])
            time.sleep(0.2)
        print(f"  ✅ 完成写作教材学习")

    def learn_classic_literature(self):
        """学习经典文学作品"""
        classics = [
            {"title": "红楼梦", "category": "经典文学",
             "core_points": ["家族兴衰的史诗叙事", "人物群像的精细刻画",
                            "意象与象征的运用", "悲剧美学的极致展现", "诗词与叙事的融合"],
             "writing_value": ["人物塑造", "场景描写", "隐喻运用"]},
            {"title": "平凡的世界", "category": "当代文学",
             "core_points": ["普通人的奋斗史诗", "时代变迁的记录",
                            "现实主义创作方法", "苦难中的人性光辉", "朴实真挚的语言风格"],
             "writing_value": ["时代叙事", "人物成长", "情感共鸣"]},
            {"title": "活着", "category": "当代文学",
             "core_points": ["苦难中的生存意志", "极简叙事的力量",
                            "命运的无常与坚韧", "以小见大的叙事手法", "悲剧中的温情"],
             "writing_value": ["叙事节奏", "情感克制", "人物命运"]},
            {"title": "白鹿原", "category": "当代文学",
             "core_points": ["民族秘史的宏大叙事", "传统文化的深度挖掘",
                            "人物命运与时代交织", "史诗性结构", "方言与民俗的运用"],
             "writing_value": ["宏大叙事", "文化底蕴", "史诗结构"]},
            {"title": "围城", "category": "经典文学",
             "core_points": ["知识分子生活的讽刺", "精妙的比喻与讽刺",
                            "婚姻与人生的困境", "幽默与悲剧的融合", "语言的智慧与犀利"],
             "writing_value": ["讽刺手法", "语言艺术", "心理描写"]},
            {"title": "金锁记", "category": "经典文学",
             "core_points": ["人性扭曲的深刻描写", "封建礼教的批判",
                            "心理分析的深度", "意象的系统性运用", "苍凉的悲剧基调"],
             "writing_value": ["心理刻画", "悲剧美学", "意象构建"]},
            {"title": "边城", "category": "经典文学",
             "core_points": ["田园牧歌式的抒情", "人性美的赞歌",
                            "诗意的语言风格", "留白艺术的运用", "淡淡的忧愁基调"],
             "writing_value": ["抒情叙事", "诗意语言", "留白"]},
            {"title": "四世同堂", "category": "经典文学",
             "core_points": ["战争中的民族精神", "家庭与民族命运的联结",
                            "市井生活的细致描绘", "人物性格的复杂性", "文化传统的坚守"],
             "writing_value": ["家国叙事", "群像塑造", "时代记录"]},
            {"title": "蛙", "category": "当代文学",
             "core_points": ["计划生育政策的反思", "生命伦理的探讨",
                            "多重视角的叙事", "魔幻现实主义手法", "历史与个人命运"],
             "writing_value": ["主题深度", "叙事视角", "现实批判"]},
            {"title": "嫌疑人X的献身", "category": "推理小说",
             "core_points": ["极致的逻辑推理", "人性与理性的冲突",
                            "完美犯罪的设计", "情感与逻辑的交织", "出人意料的结局"],
             "writing_value": ["悬念设计", "逻辑构建", "反转技巧"]},
            {"title": "一句顶一万句", "category": "当代文学",
             "core_points": ["中国式孤独的描绘", "普通人的精神世界",
                            "口语化叙事风格", "寻找与救赎的主题", "生活细节的真实感"],
             "writing_value": ["口语叙事", "心理深度", "主题挖掘"]},
            {"title": "撒哈拉的故事", "category": "散文",
             "core_points": ["异域生活的诗意描写", "浪漫与苦难的交织",
                            "独特的生命体验", "细腻的情感表达", "自由精神的歌颂"],
             "writing_value": ["散文写作", "情感表达", "细节描写"]},
            {"title": "长恨歌", "category": "当代文学",
             "core_points": ["上海女性的命运书写", "都市文化的描绘",
                            "细腻的心理描写", "时间与记忆的主题", "精致的语言风格"],
             "writing_value": ["都市叙事", "心理描写", "语言风格"]},
            {"title": "在细雨中呼喊", "category": "当代文学",
             "core_points": ["童年记忆的诗意重构", "死亡与生存的思考",
                            "非线性叙事结构", "情感记忆的唤醒", "独特的叙事视角"],
             "writing_value": ["记忆叙事", "非线性结构", "情感表达"]},
            {"title": "半生缘", "category": "经典文学",
             "core_points": ["爱情与命运的悲剧", "女性命运的书写",
                            "细腻的心理刻画", "苍凉的叙事基调", "时代背景的烘托"],
             "writing_value": ["爱情叙事", "心理刻画", "悲剧感"]},
            {"title": "呼兰河传", "category": "经典文学",
             "core_points": ["童年视角的故乡回忆", "民俗风情的描绘",
                            "散文诗般的语言", "人性的愚昧与善良", "淡淡的乡愁与忧伤"],
             "writing_value": ["童年叙事", "民俗描写", "诗意语言"]},
            {"title": "海边的房间", "category": "当代文学",
             "core_points": ["都市孤独的书写", "细腻的感官描写",
                            "现代性的焦虑", "碎片化的叙事", "隐喻与象征"],
             "writing_value": ["都市书写", "感官描写", "隐喻"]},
            {"title": "望江南", "category": "当代文学",
             "core_points": ["茶文化的诗意表达", "家族故事的书写",
                            "传统文化的传承", "江南风情的描绘", "细腻的情感表达"],
             "writing_value": ["文化书写", "情感表达", "地域特色"]},
            {"title": "父亲", "category": "散文",
             "core_points": ["父子关系的深刻描写", "父爱的含蓄表达",
                            "代际冲突与和解", "记忆与时间的主题", "情感的真挚流露"],
             "writing_value": ["亲情书写", "情感真挚", "细节刻画"]},
            {"title": "焦虑的人", "category": "当代文学",
             "core_points": ["现代社会的焦虑症候", "多人物视角叙事",
                            "黑色幽默的运用", "人性的温暖与救赎", "都市生活的困境"],
             "writing_value": ["社会批判", "多视角", "黑色幽默"]},
            {"title": "青蛇", "category": "当代文学",
             "core_points": ["传统神话的现代解构", "女性视角的重构",
                            "爱情与欲望的探讨", "华丽的语言风格", "人性与妖性的边界"],
             "writing_value": ["神话重构", "女性叙事", "语言风格"]}
        ]

        for book in classics:
            print(f"  📖 研读：{book['title']}")
            content = f"【{book['category']}】{book['title']}\n\n核心要点：\n"
            for i, point in enumerate(book['core_points'], 1):
                content += f"{i}. {point}\n"
            content += f"\n写作借鉴：{'、'.join(book['writing_value'])}\n"
            self._save_learning(content, book['category'])
            time.sleep(0.2)
        print(f"  ✅ 完成经典文学学习")

    def learn_additional_books(self):
        """学习补充书籍"""
        books = [
            {"title": "存在主义的咖啡馆", "category": "哲学", "core_points": ["存在主义思想", "自由与选择", "生命意义"]},
            {"title": "人间词话", "category": "文论", "core_points": ["境界说", "诗词鉴赏", "意境营造"]},
            {"title": "人类群星闪耀时", "category": "历史", "core_points": ["关键时刻", "人物决定性瞬间", "历史叙事"]},
            {"title": "苏东坡传", "category": "传记", "core_points": ["人生态度", "旷达精神", "文人风骨"]},
            {"title": "陶庵梦忆", "category": "小品文", "core_points": ["晚明风情", "小品文风格", "故国之思"]},
            {"title": "万古江河", "category": "历史", "core_points": ["中华文明历程", "文化传承", "历史视野"]},
            {"title": "乡土中国", "category": "社会学", "core_points": ["中国社会结构", "乡土文化", "差序格局"]},
            {"title": "雅舍小品", "category": "散文", "core_points": ["闲适风格", "幽默讽刺", "生活情趣"]},
            {"title": "浮生六记", "category": "自传", "core_points": ["生活美学", "夫妻情深", "闲情逸致"]},
            {"title": "文化苦旅", "category": "散文", "core_points": ["文化反思", "历史沧桑", "人文关怀"]},
            {"title": "雪国", "category": "外国文学", "core_points": ["物哀美学", "虚无感", "美的幻灭"]},
            {"title": "世说新语", "category": "志人小说", "core_points": ["魏晋风度", "人物品鉴", "简洁传神"]},
            {"title": "病隙碎笔", "category": "散文", "core_points": ["生命思考", "苦难与信仰", "精神救赎"]},
            {"title": "水问", "category": "散文", "core_points": ["女性意识", "生命感悟", "细腻文风"]},
            {"title": "武则天", "category": "历史", "core_points": ["权力斗争", "女性执政", "历史评价"]},
            {"title": "汪曾祺纪念文集", "category": "散文", "core_points": ["市井风情", "生活美学", "平淡见真"]},
            {"title": "人间草木", "category": "散文", "core_points": ["草木情怀", "生活细节", "诗意栖居"]},
            {"title": "人间有至味", "category": "散文", "core_points": ["饮食文化", "生活情趣", "人间烟火"]},
            {"title": "巨鲸歌唱", "category": "散文", "core_points": ["海洋意象", "生命感悟", "诗意表达"]},
            {"title": "将饮茶", "category": "散文", "core_points": ["知识分子生活", "文化记忆", "优雅文风"]},
            {"title": "有如候鸟", "category": "散文", "core_points": ["迁徙主题", "生命漂泊", "故乡情结"]},
            {"title": "张枣的诗", "category": "诗歌", "core_points": ["语言实验", "意象创新", "抒情深度"]},
            {"title": "如何写砸一本小说", "category": "写作教材", "core_points": ["常见误区", "避免套路", "反面教材"]},
            {"title": "小说写作叙事技巧指南", "category": "写作教材", "core_points": ["叙事视角", "时间结构", "节奏控制"]}
        ]

        for book in books:
            print(f"  📕 学习：{book['title']}")
            content = f"【{book['category']}】{book['title']}\n\n核心要点：\n"
            for i, point in enumerate(book['core_points'], 1):
                content += f"{i}. {point}\n"
            self._save_learning(content, book['category'])
            time.sleep(0.1)
        print(f"  ✅ 完成补充书籍学习")

    def learn_writing_dictionaries(self):
        """学习写作词典类书籍"""
        dicts = [
            {"title": "写作成语词典", "category": "写作工具", "value": "丰富表达"},
            {"title": "文学描写词典", "category": "写作工具", "value": "描写素材"},
            {"title": "写作借鉴词典", "category": "写作工具", "value": "写作参考"},
            {"title": "中国神话人物词典", "category": "写作工具", "value": "神话素材"},
            {"title": "读书词典", "category": "写作工具", "value": "阅读指导"},
            {"title": "写作辞林", "category": "写作工具", "value": "词汇宝库"},
            {"title": "最佳景色描写词典", "category": "写作工具", "value": "场景描写"},
            {"title": "最佳女性外貌描写词典", "category": "写作工具", "value": "人物描写"},
            {"title": "最佳外貌描写词典", "category": "写作工具", "value": "外貌描写"},
            {"title": "最佳心理描写词典", "category": "写作工具", "value": "心理刻画"},
            {"title": "最佳男性描写词典", "category": "写作工具", "value": "男性塑造"},
            {"title": "最佳女性描写词典", "category": "写作工具", "value": "女性塑造"},
            {"title": "唐代衣食住行研究", "category": "写作工具", "value": "历史细节"},
            {"title": "小说创造基本技巧", "category": "写作教材", "value": "基础技能"},
            {"title": "小说写作进阶技巧", "category": "写作教材", "value": "进阶提升"}
        ]

        for d in dicts:
            print(f"  📗 参考：{d['title']}")
            content = f"【{d['category']}】{d['title']}\n\n价值：{d['value']}\n"
            self._save_learning(content, d['category'])
            time.sleep(0.05)
        print(f"  ✅ 完成写作词典学习")

    def run_full_learning(self):
        """运行完整学习流程"""
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║         NWACS 书籍学习提炼系统 v{VERSION}                       ║
║                                                              ║
║         📚 学习模式：{'内存模式（不保存文件）' if self.memory_only else '文件模式（保存学习记录）'}              ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
        """)

        modules = [
            ("写作教材", self.learn_writing_textbooks),
            ("经典文学", self.learn_classic_literature),
            ("补充书籍", self.learn_additional_books),
            ("写作词典", self.learn_writing_dictionaries)
        ]

        for name, func in modules:
            print(f"\n📚 开始学习：{name}")
            func()
            time.sleep(0.5)

        print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║         ✅ 书籍学习提炼完成！                                  ║
║                                                              ║
║         📊 本次学习：{self.learned_count} 本书籍/资源              ║
║         {'📂 学习记录保存在：' + LEARNING_DIR if not self.memory_only else '💭 学习内容已存入内存'}              ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
        """)

        return self.learned_content

class NovelProjectManager:
    """小说项目管理器 - 每部小说独立文件夹"""

    def __init__(self):
        os.makedirs(NOVELS_DIR, exist_ok=True)

    def create_novel_folder(self, novel_name):
        """为小说创建独立文件夹"""
        novel_folder = os.path.join(NOVELS_DIR, novel_name)
        os.makedirs(novel_folder, exist_ok=True)
        
        subfolders = ['chapters', 'characters', 'outline', 'worldview', 'drafts']
        for sub in subfolders:
            os.makedirs(os.path.join(novel_folder, sub), exist_ok=True)
        
        return novel_folder

    def save_novel_content(self, novel_name, content_type, content, filename=None):
        """保存小说内容到对应目录"""
        novel_folder = self.create_novel_folder(novel_name)
        
        type_map = {
            'chapter': 'chapters',
            'character': 'characters',
            'outline': 'outline',
            'worldview': 'worldview',
            'draft': 'drafts'
        }
        
        subfolder = type_map.get(content_type, 'drafts')
        if not filename:
            filename = f"{content_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        filepath = os.path.join(novel_folder, subfolder, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return filepath

    def list_novels(self):
        """列出所有小说项目"""
        novels = []
        for item in os.listdir(NOVELS_DIR):
            path = os.path.join(NOVELS_DIR, item)
            if os.path.isdir(path):
                novels.append(item)
        return novels

    def get_novel_structure(self, novel_name):
        """获取小说项目结构"""
        novel_folder = os.path.join(NOVELS_DIR, novel_name)
        if not os.path.exists(novel_folder):
            return None
        
        structure = {}
        for subfolder in ['chapters', 'characters', 'outline', 'worldview', 'drafts']:
            path = os.path.join(novel_folder, subfolder)
            if os.path.exists(path):
                structure[subfolder] = os.listdir(path)
        
        return structure

def main():
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║         NWACS 书籍学习提炼系统 v{VERSION}                       ║
║                                                              ║
║         请选择操作模式：                                       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)

    while True:
        print("\n1. 内存模式学习（不创建文件）")
        print("2. 文件模式学习（保存学习记录）")
        print("3. 创建小说项目文件夹")
        print("4. 查看现有小说项目")
        print("0. 退出")
        
        choice = input("\n请选择: ").strip()
        
        if choice == '1':
            learner = BookLearningSystem(memory_only=True)
            learner.run_full_learning()
        elif choice == '2':
            learner = BookLearningSystem(memory_only=False)
            learner.run_full_learning()
        elif choice == '3':
            novel_name = input("请输入小说名称: ").strip()
            if novel_name:
                manager = NovelProjectManager()
                folder = manager.create_novel_folder(novel_name)
                print(f"\n✅ 已为《{novel_name}》创建项目文件夹: {folder}")
                print("📁 目录结构:")
                print("  - chapters/     # 章节内容")
                print("  - characters/   # 人物设定")
                print("  - outline/      # 大纲")
                print("  - worldview/    # 世界观")
                print("  - drafts/       # 草稿")
            else:
                print("❌ 小说名称不能为空")
        elif choice == '4':
            manager = NovelProjectManager()
            novels = manager.list_novels()
            if novels:
                print("\n📚 现有小说项目:")
                for i, novel in enumerate(novels, 1):
                    print(f"  {i}. {novel}")
            else:
                print("\n暂无小说项目")
        elif choice == '0':
            print("\n👋 再见！")
            break
        else:
            print("\n❌ 无效选择，请重新输入")

if __name__ == "__main__":
    main()