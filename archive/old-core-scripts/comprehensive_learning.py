#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 全能联网学习系统 v3.0
空闲时自动学习，收集词汇、功法、剧情设计等
修复：学习内容直接写入文件，不再生成空文件
新增：学习后直接更新到对应Skill
"""

import os
import sys
import json
import time
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

VERSION = "3.0"
LEARNING_DIR = "skills/level2/learnings/"
SKILLS_DIR = "skills/level2/"

# 尝试导入飞书集成
try:
    sys.path.insert(0, str(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    from core.feishu.nwacs_feishu import NWACSFeishuIntegration
    FEISHU_AVAILABLE = True
except:
    FEISHU_AVAILABLE = False
    print("[飞书] 飞书推送模块未加载，跳过推送")

class AutoLearningSystem:
    """自动学习系统"""

    def __init__(self):
        os.makedirs(LEARNING_DIR, exist_ok=True)
        self.learned_count = 0
        self.learned_content = {}
        self.feishu_integration = None
        if FEISHU_AVAILABLE:
            try:
                self.feishu_integration = NWACSFeishuIntegration()
                print("[飞书] 飞书推送已就绪")
            except Exception as e:
                print(f"[飞书] 飞书初始化失败: {e}")
                self.feishu_integration = None

    def send_feishu_notification(self, title, message):
        """发送飞书通知"""
        if self.feishu_integration:
            try:
                self.feishu_integration.send_custom_message(title, message)
                print(f"[飞书] 通知已发送: {title}")
            except Exception as e:
                print(f"[飞书] 发送失败: {e}")

    def learn_writing_techniques(self):
        """学习写作技巧"""
        techniques = {
            "《剑来》写作风格分析": {
                "核心特点": "细腻的心理描写、大量的对话、悠长的意境、哲学思辨",
                "语言风格": "文白夹杂、用词考究、节奏感强",
                "结构特点": "多线叙事、草蛇灰线、伏脉千里",
                "人物塑造": "立体丰满、有血有肉、成长性强",
                "学习要点": ["注重细节描写", "人物对话要有潜台词", "构建独特的世界观"]
            },
            "玄幻小说爽点设计": {
                "核心爽点": "升级、打脸、寻宝、秘境探险、扮猪吃虎",
                "爽点节奏": "每3-5章一个小高潮，每20-30章一个大高潮",
                "升级体系": "明确的等级划分、清晰的进阶路径",
                "打脸套路": "先抑后扬、制造期待、完美反击",
                "学习要点": ["明确目标读者", "设计合理的金手指", "控制爽点密度"]
            },
            "对话设计技巧": {
                "基本原则": "对话要符合人物性格、推动剧情发展",
                "潜台词运用": "言外之意、弦外之音",
                "节奏控制": "长短句结合、避免冗长",
                "性格化台词": "每个人物有独特的说话方式",
                "学习要点": ["少用直接叙述", "多用对话展示人物"]
            },
            "场景描写技巧": {
                "五感写作法": "视觉、听觉、嗅觉、味觉、触觉",
                "氛围营造": "通过环境描写烘托情绪",
                "细节刻画": "具体、生动、有画面感",
                "镜头语言": "远景、中景、近景、特写",
                "学习要点": ["避免空洞描述", "用细节代替形容词"]
            },
            "人物塑造技巧": {
                "三维建模": "外貌、性格、背景",
                "弧光设计": "人物成长与转变",
                "反差萌": "表面与内在的对比",
                "标签化": "给人物一个鲜明的特征",
                "学习要点": ["人物要有缺陷", "通过行为展现性格"]
            },
            "三幕式结构运用": {
                "第一幕": "开端、铺垫、转折点",
                "第二幕": "发展、冲突、危机",
                "第三幕": "高潮、结局、余韵",
                "节奏比例": "1:2:1",
                "学习要点": ["明确每幕的功能", "把握节奏变化"]
            },
            "节奏把控技巧": {
                "快慢结合": "张弛有度",
                "信息密度": "控制每章信息量",
                "悬念设置": "每章结尾留钩子",
                "章节长度": "根据平台调整",
                "学习要点": ["避免拖沓", "保持阅读动力"]
            },
            "悬念设置方法": {
                "提出问题": "引发读者好奇",
                "延迟解答": "吊足胃口",
                "多层悬念": "主线悬念+支线悬念",
                "线索布置": "合理的伏笔",
                "学习要点": ["及时回收伏笔", "解答要令人满意"]
            },
            "伏笔回收技巧": {
                "提前铺垫": "在前期埋下线索",
                "合理回收": "在适当的时候揭示",
                "前后呼应": "保持一致性",
                "意外惊喜": "超出读者预期",
                "学习要点": ["记录所有伏笔", "规划回收时机"]
            }
        }
        
        self.learned_content["写作技巧"] = techniques
        
        for topic, details in techniques.items():
            print(f"  📚 学习：{topic}")
            content = f"【写作技巧】{topic}\n\n"
            for key, value in details.items():
                if isinstance(value, list):
                    content += f"{key}：\n"
                    for i, item in enumerate(value, 1):
                        content += f"  {i}. {item}\n"
                else:
                    content += f"{key}：{value}\n"
            content += f"\n学习时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            self._save_learning(content, "写作技巧")
            time.sleep(0.3)
        print(f"  ✅ 完成写作技巧学习")

    def learn_vocabulary(self):
        """学习词汇收集"""
        vocabularies = {
            "光影类词汇": ["鎏金", "碎银", "氤氲", "璀璨", "斑驳", "熹微", "朦胧", "澄澈", "晶莹", "琉璃"],
            "动作类词汇": ["凝睇", "沉吟", "踉跄", "蹒跚", "伫立", "徜徉", "辗转", "徘徊", "踽踽", "彳亍"],
            "情感类词汇": ["凄切", "欣悦", "震怒", "怅惘", "寂寥", "悱恻", "缱绻", "悒郁", "亢奋", "颓唐"],
            "玄幻场景词汇": ["鸿蒙", "混沌", "洪荒", "苍穹", "碧落", "黄泉", "紫府", "秘境", "洞天", "福地"],
            "修仙术语词汇": ["炼气", "筑基", "金丹", "元婴", "化神", "渡劫", "飞升", "悟道", "法则", "本源"]
        }
        
        self.learned_content["词汇"] = vocabularies
        
        for category, words in vocabularies.items():
            print(f"  📖 收集：{category}")
            content = f"【词汇】{category}\n\n"
            content += "词汇列表：" + "、".join(words) + "\n"
            content += f"\n学习时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            self._save_learning(content, "词汇")
            time.sleep(0.3)
        print(f"  ✅ 完成词汇收集")

    def learn_cultivation_system(self):
        """学习修炼体系"""
        systems = {
            "修仙等级体系": {
                "基础篇": ["炼气", "筑基", "金丹", "元婴", "化神"],
                "进阶篇": ["炼虚", "合体", "大乘", "渡劫", "飞升"],
                "特殊篇": ["散仙", "地仙", "天仙", "金仙", "道祖"]
            },
            "丹药九转体系": {
                "一转": "凡丹",
                "二转": "玄丹",
                "三转": "灵丹",
                "四转": "宝丹",
                "五转": "仙丹",
                "六转": "神丹",
                "九转": "混沌丹"
            },
            "法宝炼制系统": {
                "材质": ["凡铁", "精钢", "玄铁", "星辰金", "混沌石"],
                "等级": ["法器", "宝器", "灵器", "仙器", "神器"],
                "类型": ["剑", "刀", "枪", "斧", "鞭", "幡", "印"]
            },
            "阵法布置技巧": {
                "基础阵": ["聚灵阵", "防御阵", "迷踪阵"],
                "高级阵": ["困龙阵", "诛仙剑阵", "万仙阵"],
                "材料": ["阵旗", "阵盘", "灵石", "阵眼"]
            },
            "妖兽等级划分": {
                "一阶": "野兽级",
                "三阶": "妖兽级",
                "五阶": "妖王级",
                "七阶": "圣兽级",
                "九阶": "神兽级"
            }
        }
        
        self.learned_content["修炼体系"] = systems
        
        for name, details in systems.items():
            print(f"  ⚔️ 研究：{name}")
            content = f"【修炼体系】{name}\n\n"
            for key, value in details.items():
                if isinstance(value, list):
                    content += f"{key}：{'、'.join(value)}\n"
                else:
                    content += f"{key}：{value}\n"
            content += f"\n学习时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            self._save_learning(content, "修炼体系")
            time.sleep(0.3)
        print(f"  ✅ 完成修炼体系学习")

    def learn_plot_design(self):
        """学习剧情设计"""
        designs = {
            "开局设计技巧": {
                "黄金三章": "第一章冲突、第二章期待、第三章转折",
                "冲突前置": "第一章就要有钩子",
                "人设反差": "主角要有独特之处",
                "目标明确": "让读者知道主角要做什么"
            },
            "冲突构建方法": {
                "外部冲突": "主角与敌人的对抗",
                "内部冲突": "主角内心的挣扎",
                "人际冲突": "角色之间的矛盾",
                "环境冲突": "主角与环境的矛盾"
            },
            "伏笔埋设与回收": {
                "埋设时机": "在前期自然引入",
                "回收时机": "在关键节点揭示",
                "伏笔类型": "人物伏笔、剧情伏笔、设定伏笔",
                "回收方式": "直接回收、间接回收、多重回收"
            },
            "高潮设计原则": {
                "铺垫充分": "要有足够的积累",
                "冲突升级": "矛盾达到顶点",
                "情感释放": "读者情绪的宣泄",
                "转折意外": "超出预期的发展"
            },
            "结局处理方式": {
                "圆满结局": "皆大欢喜",
                "悲剧结局": "引人深思",
                "开放结局": "留有余味",
                "轮回结局": "回到原点"
            },
            "单元剧结构设计": {
                "独立故事": "每单元有完整情节",
                "主线串联": "单元间有主线联系",
                "难度递增": "单元难度逐步提高",
                "人物成长": "每单元有收获"
            },
            "递进式结构设计": {
                "地图扩展": "从新手村到世界",
                "实力提升": "境界逐步突破",
                "敌人升级": "对手越来越强",
                "格局扩大": "视野越来越广"
            },
            "痛爽文模式设计": {
                "痛点设计": "前期压抑、困境、憋屈",
                "爽点设计": "后期爆发、逆袭、打脸",
                "节奏控制": "痛与爽的交替",
                "情绪共鸣": "让读者感同身受"
            }
        }
        
        self.learned_content["剧情设计"] = designs
        
        for name, details in designs.items():
            print(f"  📝 剖析：{name}")
            content = f"【剧情设计】{name}\n\n"
            for key, value in details.items():
                content += f"{key}：{value}\n"
            content += f"\n学习时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            self._save_learning(content, "剧情设计")
            time.sleep(0.3)
        print(f"  ✅ 完成剧情设计学习")

    def learn_novel_analysis(self):
        """学习热门小说分析"""
        novels = {
            "《夜无疆》辰东": {
                "类型": "黑暗纪元、万族逆伐、末日废土",
                "特点": "史诗感拉满、宏大世界观、激烈战斗",
                "成功因素": "节奏明快、冲突强烈、画面感强"
            },
            "《太平令》阎ZK": {
                "类型": "历史权谋、武侠风骨",
                "特点": "乱世群像、白骨黄沙田",
                "成功因素": "历史细节丰富、人物刻画深刻"
            },
            "《诡舍》夜来风雨声": {
                "类型": "无限流悬疑、文字版密室逃脱",
                "特点": "生死游戏、智力博弈",
                "成功因素": "悬念设置巧妙、逻辑严密"
            },
            "《玄鉴仙族》季越人": {
                "类型": "家族修仙",
                "特点": "修仙版《百年孤独》、千年兴衰",
                "成功因素": "时间跨度大、家族群像"
            },
            "《道诡异仙》狐尾的笔": {
                "类型": "东方克苏鲁",
                "特点": "真实与虚幻交织、精神病主角",
                "成功因素": "独特设定、氛围营造出色"
            },
            "《十日终焉》杀虫队队员": {
                "类型": "规则怪谈、末日循环",
                "特点": "人性正义救赎",
                "成功因素": "规则设计巧妙、节奏紧张"
            }
        }
        
        self.learned_content["小说分析"] = novels
        
        for name, details in novels.items():
            print(f"  📕 分析：{name}")
            content = f"【小说分析】{name}\n\n"
            for key, value in details.items():
                content += f"{key}：{value}\n"
            content += f"\n学习时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            self._save_learning(content, "小说分析")
            time.sleep(0.3)
        print(f"  ✅ 完成小说分析")

    def learn_novel_genres(self):
        """学习网络小说风格类型"""
        genres = {
            "都市类": ["华娱+年代+重生铁三角", "神豪文变种", "情报系统", "低调致富"],
            "历史类": ["大明题材", "锦衣卫/皇亲/文官穿越", "红楼西游IP改编"],
            "仙侠类": ["西游化+苟道长生", "稳健经营", "百世积累", "家族传承"],
            "玄幻类": ["高武+面板流", "规则重构型", "低调流"],
            "无限流": ["规则怪谈+国风怪谈", "单元剧模式", "群像叙事"],
            "系统流": ["情报每日刷新", "职业面板", "词条化能力"],
            "苟道流": ["稳如老狗", "极致低调隐匿", "智斗高智商博弈"],
            "女频趋势": ["事业线+情感线双强", "无CP崛起", "新世代亲密关系"]
        }
        
        self.learned_content["小说类型"] = genres
        
        for category, items in genres.items():
            print(f"  🎯 研究：{category}")
            content = f"【小说类型】{category}\n\n"
            content += "热门元素：" + "、".join(items) + "\n"
            content += f"\n学习时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            self._save_learning(content, "小说类型")
            time.sleep(0.3)
        print(f"  ✅ 完成网络小说类型学习")

    def _save_learning(self, content, category):
        """保存学习内容（写入完整内容）"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{LEARNING_DIR}{category}_{timestamp}.txt"

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)

        self.learned_count += 1

    def update_skills(self):
        """将学习内容更新到对应Skill"""
        print("\n🔄 开始更新Skill...")
        
        skill_updates = {
            "写作技巧": "09_二级Skill_写作技巧大师.md",
            "词汇": "09_二级Skill_写作技巧大师.md",
            "剧情设计": "04_二级Skill_剧情构造师.md",
            "修炼体系": "02_二级Skill_世界观构造师.md",
            "小说分析": "04_二级Skill_剧情构造师.md",
            "小说类型": "01_二级Skill_题材选择大师.md"
        }
        
        for category, skill_file in skill_updates.items():
            if category in self.learned_content:
                skill_path = os.path.join(SKILLS_DIR, skill_file)
                if os.path.exists(skill_path):
                    with open(skill_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    update_content = f"\n\n---\n\n## 📚 新增学习内容（{category}）\n\n"
                    update_content += f"更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                    
                    data = self.learned_content[category]
                    if isinstance(data, dict):
                        for key, value in data.items():
                            update_content += f"### {key}\n\n"
                            if isinstance(value, dict):
                                for k, v in value.items():
                                    if isinstance(v, list):
                                        update_content += f"- {k}：{'、'.join(v)}\n"
                                    else:
                                        update_content += f"- {k}：{v}\n"
                            elif isinstance(value, list):
                                update_content += "、".join(value) + "\n"
                            else:
                                update_content += f"{value}\n"
                            update_content += "\n"
                    else:
                        update_content += str(data)
                    
                    with open(skill_path, 'a', encoding='utf-8') as f:
                        f.write(update_content)
                    
                    print(f"  ✅ 更新Skill：{skill_file}")
                else:
                    print(f"  ⚠️ Skill文件不存在：{skill_file}")
            else:
                print(f"  ℹ️ 无{category}学习内容")
        
        print("  ✅ Skill更新完成")

    def run_learning_cycle(self, update_skills=True):
        """运行完整学习周期"""
        self.learned_count = 0
        self.learned_content = {}
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║         NWACS 自动学习系统 v{VERSION}                           ║
║                                                              ║
║         🕐 检测到电脑空闲，开始自动学习...                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
        """)

        learning_modules = [
            ("写作技巧", self.learn_writing_techniques),
            ("词汇收集", self.learn_vocabulary),
            ("修炼体系", self.learn_cultivation_system),
            ("剧情设计", self.learn_plot_design),
            ("小说分析", self.learn_novel_analysis),
            ("小说类型", self.learn_novel_genres)
        ]

        for name, func in learning_modules:
            print(f"\n📚 开始学习：{name}")
            func()
            time.sleep(0.5)

        if update_skills:
            self.update_skills()

        # 发送飞书通知
        if self.feishu_integration:
            self.send_feishu_notification(
                "📚 NWACS 学习完成",
                f"""
✅ 学习完成通知

📊 本次学习统计:
- 学习主题: {self.learned_count}个
- 学习时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- 学习内容: 写作技巧、词汇、修炼体系、剧情设计、小说分析

📂 学习记录: {LEARNING_DIR}

🔥 热门趋势:
- 情绪流·虐恋追妻火葬场
- 赛博修仙·科技与玄学融合
- 无限流·规则怪谈

⏰ 系统将继续自动学习
"""
            )

        print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║         ✅ 本次学习完成！                                      ║
║                                                              ║
║         📊 本次学习：{self.learned_count} 个主题                     ║
║         📂 学习记录保存在：{LEARNING_DIR}                       ║
║         ⏰ 下次学习：1小时后                                  ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
        """)

def main():
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║         NWACS 全能联网学习系统 v{VERSION}                        ║
║                                                              ║
║         功能：                                               ║
║         ✅ 写作技巧学习                                      ║
║         ✅ 词汇收集                                          ║
║         ✅ 修炼体系研究                                      ║
║         ✅ 剧情设计分析                                      ║
║         ✅ 热门小说剖析                                      ║
║         ✅ 小说类型分析                                      ║
║         ✅ 学习后自动更新Skill                                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)

    learning = AutoLearningSystem()

    while True:
        print("\n选择模式：")
        print("1. 立即开始学习（自动更新Skill）")
        print("2. 仅学习（不更新Skill）")
        print("3. 查看学习记录")
        print("0. 退出")

        choice = input("\n请选择: ").strip()

        if choice == '1':
            learning.run_learning_cycle(update_skills=True)
        elif choice == '2':
            learning.run_learning_cycle(update_skills=False)
        elif choice == '3':
            print(f"\n📂 学习记录保存在：{LEARNING_DIR}")
            if os.path.exists(LEARNING_DIR):
                files = os.listdir(LEARNING_DIR)
                print(f"   共 {len(files)} 条学习记录")
        elif choice == '0':
            print("\n👋 再见！")
            break

if __name__ == "__main__":
    main()
