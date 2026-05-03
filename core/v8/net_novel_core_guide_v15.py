#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS V15 - 网文创作核心指南（2026联网学习版）
基于2026年最新爆款小说拆解，包含完整的读者心理学、开局公式、爽点设计等
"""

import sys
import os
import json
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

class NetNovelCoreGuide:
    """NWACS V15 网文创作核心指南"""
    
    def __init__(self):
        print("="*80)
        print("📚 NWACS V15 - 网文创作核心指南（2026联网学习版）")
        print("="*80)
        
        # 读者心理学
        self.reader_psychology = self.load_reader_psychology()
        
        # 黄金三章指南
        self.golden_three_chapters = self.load_golden_chapters()
        
        # 爽点设计
        self.shuang_points = self.load_shuang_points()
        
        # 人设反差设计
        self.character_contrast = self.load_character_contrast()
        
        # 金句钩子设计
        self.golden_hooks = self.load_golden_hooks()
        
        # 书名公式
        self.book_title_formulas = self.load_book_titles()
        
        # 平台差异化
        self.platform_strategy = self.load_platform_strategy()
        
        print(f"✅ 已加载全部核心指南!")
        
        self.save_to_disk()
    
    def load_reader_psychology(self):
        """加载读者心理学"""
        return {
            "four_types": {
                "爽文党": {
                    "ratio": "40%",
                    "description": "网文基本盘，工作累了想看逆袭打脸",
                    "core_needs": ["低门槛", "快节奏", "高密度爽点"],
                    "writing_tips": [
                        "主角憋屈不超过三章，第三章必须翻身",
                        "等级体系要清晰，主角变强要肉眼可见",
                        "打脸要干脆，反派智商不用太高",
                        "金手指要直接，不要铺垫太久"
                    ],
                    "representative_works": ["《斗破苍穹》", "《全职高手》"]
                },
                "情感党": {
                    "ratio": "25%",
                    "description": "以女频为主，看小说为心动、心疼、意难平",
                    "core_needs": ["情绪张力", "代入感", "情感共鸣"],
                    "writing_tips": [
                        "主角情感经历要有波折，不能一帆风顺",
                        "虐点要虐得合理，不能为虐而虐",
                        "甜点要甜得自然，不能工业糖精",
                        "配角情感线也要有看点"
                    ],
                    "representative_works": ["《何以笙箫默》", "《偷偷藏不住》"]
                },
                "设定党": {
                    "ratio": "15%",
                    "description": "网文里的硬核玩家，喜欢研究世界观和等级体系",
                    "core_needs": ["创新", "严谨", "可挖掘的深度"],
                    "writing_tips": [
                        "世界观要新颖，不能老套",
                        "等级体系要自洽，不能前后矛盾",
                        "有隐藏线索、伏笔、值得二刷的细节",
                        "可以'考据'和'讨论'的空间"
                    ],
                    "representative_works": ["《诡秘之主》", "《道诡异仙》"]
                },
                "书荒党": {
                    "ratio": "20%",
                    "description": "流动人口，到处找书看，决策快放弃也快",
                    "core_needs": ["高效找到能看下去的书", "开篇快速判断合不合口味"],
                    "writing_tips": [
                        "书名和简介要清晰传达类型和爽点",
                        "前三章要有留住人的钩子",
                        "如果不好看，他们会立刻换下一本",
                        "降低读者的试错成本"
                    ],
                    "representative_works": ["各种榜单作品"]
                }
            },
            "decision_data": {
                "番茄小说": "读者单本决策周期仅3秒",
                "起点中文网": "读者决策周期约30秒",
                "行业数据": "90%读者在前三章做出是否继续阅读决策"
            }
        }
    
    def load_golden_chapters(self):
        """加载黄金三章指南"""
        return {
            "core_data": {
                "读者决策": "90%读者在前三章做出是否继续阅读决策",
                "番茄算法": "新书前三章完读率≥45%，才能进入首秀推荐池",
                "起点万订": "前三章核心信息(人设+核心冲突+主线目标)覆盖率达100%",
                "2026爆款": "100%在第一章完成主角出场+核心困境/钩子抛出"
            },
            "chapter_standards": {
                "起点中文网(付费)": {
                    "篇幅": "单章2000-3000字，三章合计6000-9000字",
                    "世界观铺垫": "10%-20%，融入剧情与主角行动",
                    "钩子密度": "每章1-2个核心钩子，章末强悬念",
                    "爽点节奏": "第三章完成首次小爽点，核心侧重长期预期铺垫",
                    "文本格式": "段落节奏适中，兼顾叙事与对话"
                },
                "番茄小说网(免费)": {
                    "篇幅": "单章1500-2000字，三章合计4000-6000字",
                    "世界观铺垫": "≤5%，几乎无纯设定讲解",
                    "钩子密度": "每500字1个小钩子，每章结尾必留强反转钩子",
                    "爽点节奏": "第三章必须完成强打脸/反转爽点",
                    "文本格式": "多短句、短段落，手机屏幕单段不超过3行，对话占比≥60%"
                }
            },
            "three_chapter_formula": {
                "chapter_1": {
                    "name": "冲突种子",
                    "task": "抛出不可回避的矛盾",
                    "tips": "不需要铺垫世界观，直接抛出冲突",
                    "example": "血光冲天，古老的封印在他手中裂开"
                },
                "chapter_2": {
                    "name": "人物定位",
                    "task": "让主角的动机、能力和弱点鲜活起来",
                    "tips": "用两三个细节让读者产生代入感",
                    "key": "缺陷+欲望组合能提升读者共情指数近20%"
                },
                "chapter_3": {
                    "name": "悬念钩子",
                    "task": "设置让读者必须继续翻页的未知因素",
                    "tips": "不是标题的噱头，是情节内部的未解之谜",
                    "example": "她的手机里突然出现一个陌生号码，来电显示却是她已故的父亲"
                }
            }
        }
    
    def load_shuang_points(self):
        """加载爽点设计"""
        return {
            "three_core_emotions": {
                "期待感": {
                    "description": "吸引读者的第一步，爽点爆发的基础",
                    "method": "让主角处于被轻视、被羞辱、被背叛的底层处境",
                    "details": "用动作、神态、对话等细节，放大主角的委屈和无力",
                    "goal": "让读者瞬间代入，产生'想看到主角反击'的期待",
                    "bad_example": "他遇到了麻烦",
                    "good_example": "债主把他堵在巷子里，三把刀抵在腰上"
                },
                "爽快感": {
                    "description": "留住读者的核心，男频网文的终极目的",
                    "method": "主角通过激活金手指、暴露身份、提升实力碾压反派",
                    "details": "爽快感要'快、狠、准'，憋屈铺垫足够后立刻爆发",
                    "key": "打脸的同时要升职加薪，确保主角获得实质性收益"
                },
                "宣泄感": {
                    "description": "2026年新兴情绪，释放读者积压的情绪",
                    "method": "发疯文学，让主角不管不顾地宣泄",
                    "example": "癫，都癫，癫点好啊"
                }
            },
            "2026_high_frequency_shuang": {
                "打脸爽点": "主角用实力/智慧，当场打脸嘲讽、陷害自己的反派",
                "破局爽点": "主角破解生死危机，找到核心困境的解决方法",
                "收获爽点": "主角通过金手指，获得第一笔实质性收益(修为突破、第一桶金、核心能力解锁)"
            },
            "shuang_pattern": {
                "formula": "先抑后扬",
                "steps": [
                    "先让反派利用身份或资源打压主角",
                    "主角利用脑洞能力或智慧获取筹码进行反击",
                    "最后公开打脸"
                ],
                "best_effect": "叠加情绪爽点与利益爽点"
            }
        }
    
    def load_character_contrast(self):
        """加载人设反差设计"""
        return {
            "formula": "A身份 + B行为/能力，且A和B形成强烈冲突",
            "examples": {
                "乞丐+精通量子物理": "极端身份与极端学识的反差",
                "小学生+黑帮老大": "年龄与地位的反差",
                "外卖员+国际杀手": "平凡职业与危险身份的反差",
                "保洁阿姨+S级悬赏犯": "底层形象与顶级实力的反差"
            },
            "three_steps": {
                "step_1": {
                    "name": "选一个普通身份",
                    "tip": "主角身份越普通，反差越震撼",
                    "examples": ["学生", "快递员", "保安", "家庭主妇"]
                },
                "step_2": {
                    "name": "赋予超常能力或秘密",
                    "tip": "不是简单的'会武功'，而是独特能力",
                    "examples": ["能在梦里杀人", "说过的每句话都会成真", "被全世界遗忘却记得所有历史"]
                },
                "step_3": {
                    "name": "第一章就让反差暴露",
                    "tip": "2026年读者等不了30章揭秘，第一章就要制造第一个爽点"
                }
            },
            "case_study": {
                "title": "保洁阿姨是S级悬赏犯",
                "setting": "女主角是写字楼的保洁阿姨，50多岁，沉默寡言",
                "conflict": "第一章，一群雇佣兵冲进大楼抓捕'S级罪犯'",
                "golden_line": "保洁阿姨摘下橡胶手套，面无表情地说:'你们是要自己走出去，还是我送你们出去?'",
                "result": "上架首日收藏破2万，读者评论高频词是'这个设定太带感了'"
            }
        }
    
    def load_golden_hooks(self):
        """加载金句钩子设计"""
        return {
            "importance": "有金句钩子的章节，下一章打开率比没有钩子的高出53%",
            "three_types": {
                "反转信息": {
                    "example": "其实，你才是克隆体。",
                    "effect": "打破认知，引发讨论"
                },
                "情绪爆发": {
                    "example": "从今天起，我不做人了。",
                    "effect": "情绪冲击，让人震撼"
                },
                "强力承诺": {
                    "example": "我会让这座城，记住我的名字。",
                    "effect": "引发期待，让读者记住"
                }
            },
            "operation": {
                "step_1": "每章结尾最后一句独立成段",
                "step_2": "不要藏在段落中间，单独一行",
                "step_3": "用'一句话'制造'必须看下一章'的冲动"
            },
            "common_patterns": {
                "揭秘式": "那个救我的人，长着和我一模一样的脸。",
                "威胁式": "他知道，三秒后，自己会死。",
                "选择式": "按下这个按钮，他的人生将彻底改变。"
            },
            "case_study": {
                "title": "我的室友是重生者",
                "opening": "凌晨两点，宿舍熄灯了。下铺的兄弟突然坐起来，用一种不属于二十岁年轻人的声音说:'三天后，这栋楼会着火，我们都会死。'",
                "analysis": {
                    "冲突前置": "一句话抛出致命危机(着火、死亡)",
                    "人设反差": "普通室友突然变成预言者",
                    "金句钩子": "'我们都会死'直接引爆悬念"
                },
                "result": "首秀7日追读率达18%，远超番茄12%的及格线"
            }
        }
    
    def load_book_titles(self):
        """加载书名公式"""
        return {
            "tomato_formulas": {
                "core_logic": "算法推荐+免费阅读+广告变现，追求即时满足",
                "three_iron_rules": [
                    "强冲突前置：前3个字必须抛出一个矛盾或悬念",
                    "信息密度高：让读者一眼知道'谁+什么题材+爽点在哪'",
                    "钩子放在开头"
                ],
                "examples": [
                    "《游戏入侵:抢男女主机缘会上瘾诶》——题材+身份反转+情绪词",
                    "《时停起手，邪神也得给我跪下!》——金手指设定+冲突对象+爽感",
                    "《开局长生万古，苟到天荒地老》——开局金手指+核心玩法+结果预期",
                    "《大一实习，你跑去749收容怪物》——身份反差+高概念场景+猎奇感"
                ]
            },
            "qidian_formulas": {
                "core_logic": "付费订阅+IP孵化+粉丝经济，读者是资深书虫",
                "three_iron_rules": [
                    "精炼大气：短书名(2-4字)自带'经典感'",
                    "立意先行：书名承载故事的气质和格局",
                    "文学性加持：适当化用成语、典故或哲学概念"
                ],
                "examples": [
                    "《诡秘之主》——'诡秘'点明克苏鲁氛围，'之主'暗示主角身份",
                    "《道诡异仙》——'道'与'异'的冲突，修仙体系与克苏鲁的暴力缝合",
                    "《玄鉴仙族》——'玄鉴'有勘验真相之意，'仙族'点明家族修仙群像",
                    "《大奉打更人》——职业+身份，边缘职业自带悬念和烟火气"
                ]
            },
            "four_proven_formulas": {
                "formula_1": {
                    "name": "核心设定+身份/标签",
                    "examples": ["我不是戏神", "我在精神病院学斩神"],
                    "applicable": "通用于番茄和起点"
                },
                "formula_2": {
                    "name": "金手指+冲突对象+爽感预期",
                    "examples": ["时停起手，邪神也得给我跪下!", "开局长生万古，苟到天荒地老"],
                    "applicable": "番茄主战场，适用于系统流、异能文"
                },
                "formula_3": {
                    "name": "反常理/身份错位+悬念",
                    "examples": ["全宗都是舔狗，小师妹是真狗", "大一实习，你跑去749收容怪物"],
                    "applicable": "番茄主战场，通过打破认知惯性制造悬念"
                },
                "formula_4": {
                    "name": "矛盾反差/文学化表达",
                    "examples": ["诡秘之主", "道诡异仙", "玄鉴仙族", "遮天"],
                    "applicable": "起点主战场，适合世界观宏大的作品"
                }
            }
        }
    
    def load_platform_strategy(self):
        """加载平台差异化策略"""
        return {
            "tomato": {
                "platform": "番茄小说",
                "model": "免费阅读+广告变现",
                "user": "18-35岁下沉市场用户，碎片化阅读",
                "core": "追求即时爽感、强情绪冲击、快节奏反转",
                "writing_style": {
                    "书名": "强冲突+直给+钩子前置，偏长，多用'!'、口语化",
                    "开局": "前三章完读率≥45%，钩子密度高，每500字1个小钩子",
                    "格式": "多短句、短段落，对话占比≥60%",
                    "爽点": "第三章必须完成强打脸/反转爽点"
                }
            },
            "qidian": {
                "platform": "起点中文网",
                "model": "付费订阅+IP孵化",
                "user": "20-40岁资深网文读者，付费意愿强",
                "core": "追求故事逻辑、人设深度、世界观完整性",
                "writing_style": {
                    "书名": "世界观+立意+精炼，2-4字，追求文学性",
                    "开局": "前三章核心信息覆盖率100%，钩子密度适中",
                    "格式": "段落节奏适中，兼顾叙事与对话",
                    "爽点": "第三章完成首次小爽点，侧重长期预期铺垫"
                }
            },
            "2026_trends": {
                "from_external_to_internal": "从'莫欺少年穷'的外求型叙事，转向建设和守护为核心的内求型叙事",
                "crazy_literature": "发疯文异军突起，让主角不管不顾地宣泄情绪",
                "examples": ["癫，都癫，癫点好啊"]
            }
        }
    
    def get_guide(self, section):
        """获取指定部分的指南"""
        guides = {
            "读者心理学": self.reader_psychology,
            "黄金三章": self.golden_three_chapters,
            "爽点设计": self.shuang_points,
            "人设反差": self.character_contrast,
            "金句钩子": self.golden_hooks,
            "书名公式": self.book_title_formulas,
            "平台策略": self.platform_strategy
        }
        return guides.get(section, {})
    
    def show_reader_psychology(self):
        """显示读者心理学"""
        print("\n" + "="*80)
        print("🧠 读者心理学 - 四类读者分析")
        print("="*80)
        
        for reader_type, info in self.reader_psychology["four_types"].items():
            print(f"\n📌 {reader_type} ({info['ratio']})")
            print(f"   描述: {info['description']}")
            print(f"   核心需求: {', '.join(info['core_needs'])}")
            print(f"   写作要点:")
            for tip in info['writing_tips']:
                print(f"      • {tip}")
    
    def show_golden_chapters(self):
        """显示黄金三章"""
        print("\n" + "="*80)
        print("📖 黄金三章 - 核心数据")
        print("="*80)
        
        print(f"\n核心数据:")
        for key, value in self.golden_three_chapters['core_data'].items():
            print(f"   • {key}: {value}")
        
        print(f"\n📚 第一章: {self.golden_three_chapters['three_chapter_formula']['chapter_1']['name']}")
        print(f"   任务: {self.golden_three_chapters['three_chapter_formula']['chapter_1']['task']}")
        print(f"   技巧: {self.golden_three_chapters['three_chapter_formula']['chapter_1']['tips']}")
        print(f"   示例: {self.golden_three_chapters['three_chapter_formula']['chapter_1']['example']}")
        
        print(f"\n📚 第二章: {self.golden_three_chapters['three_chapter_formula']['chapter_2']['name']}")
        print(f"   任务: {self.golden_three_chapters['three_chapter_formula']['chapter_2']['task']}")
        print(f"   关键: {self.golden_three_chapters['three_chapter_formula']['chapter_2']['key']}")
        
        print(f"\n📚 第三章: {self.golden_three_chapters['three_chapter_formula']['chapter_3']['name']}")
        print(f"   任务: {self.golden_three_chapters['three_chapter_formula']['chapter_3']['task']}")
        print(f"   示例: {self.golden_three_chapters['three_chapter_formula']['chapter_3']['example']}")
    
    def show_shuang_points(self):
        """显示爽点设计"""
        print("\n" + "="*80)
        print("🔥 爽点设计 - 三种核心情绪")
        print("="*80)
        
        for emotion, info in self.shuang_points['three_core_emotions'].items():
            print(f"\n💫 {emotion}")
            print(f"   描述: {info['description']}")
            print(f"   方法: {info['method']}")
            if 'details' in info:
                print(f"   细节: {info['details']}")
            if 'goal' in info:
                print(f"   目标: {info['goal']}")
            if 'example' in info:
                print(f"   示例: {info['example']}")
    
    def show_character_contrast(self):
        """显示人设反差"""
        print("\n" + "="*80)
        print("🎭 人设反差设计")
        print("="*80)
        
        print(f"\n公式: {self.character_contrast['formula']}")
        
        print(f"\n示例:")
        for contrast, desc in self.character_contrast['examples'].items():
            print(f"   • {contrast}: {desc}")
        
        print(f"\n三步法:")
        for step, info in self.character_contrast['three_steps'].items():
            print(f"   {step}. {info['name']}")
            print(f"       技巧: {info['tip']}")
    
    def show_golden_hooks(self):
        """显示金句钩子"""
        print("\n" + "="*80)
        print("🪝 金句钩子设计")
        print("="*80)
        
        print(f"\n重要性: {self.golden_hooks['importance']}")
        
        print(f"\n三种类型:")
        for hook_type, info in self.golden_hooks['three_types'].items():
            print(f"   • {hook_type}:")
            print(f"       示例: {info['example']}")
            print(f"       效果: {info['effect']}")
        
        print(f"\n常用模式:")
        for pattern, example in self.golden_hooks['common_patterns'].items():
            print(f"   • {pattern}: {example}")
    
    def show_book_titles(self):
        """显示书名公式"""
        print("\n" + "="*80)
        print("📚 爆款书名公式")
        print("="*80)
        
        print(f"\n🍅 番茄小说:")
        print(f"   核心逻辑: {self.book_title_formulas['tomato_formulas']['core_logic']}")
        print(f"   三大铁律:")
        for rule in self.book_title_formulas['tomato_formulas']['three_iron_rules']:
            print(f"      • {rule}")
        
        print(f"\n📖 起点中文网:")
        print(f"   核心逻辑: {self.book_title_formulas['qidian_formulas']['core_logic']}")
        print(f"   三大铁律:")
        for rule in self.book_title_formulas['qidian_formulas']['three_iron_rules']:
            print(f"      • {rule}")
        
        print(f"\n📋 四大验证公式:")
        for i, (name, info) in enumerate(self.book_title_formulas['four_proven_formulas'].items(), 1):
            print(f"   {i}. {info['name']}")
            print(f"      适用: {info['applicable']}")
    
    def demo(self):
        """演示"""
        print("\n" + "="*80)
        print("📚 网文创作核心指南演示")
        print("="*80)
        
        self.show_reader_psychology()
        self.show_golden_chapters()
        self.show_shuang_points()
        self.show_character_contrast()
        self.show_golden_hooks()
        self.show_book_titles()
        
        print("\n" + "="*80)
        print("✅ 演示完成!")
        print("="*80)
    
    def save_to_disk(self):
        """保存"""
        save_data = {
            "reader_psychology": self.reader_psychology,
            "golden_three_chapters": self.golden_three_chapters,
            "shuang_points": self.shuang_points,
            "character_contrast": self.character_contrast,
            "golden_hooks": self.golden_hooks,
            "book_title_formulas": self.book_title_formulas,
            "platform_strategy": self.platform_strategy,
            "version": "V15",
            "saved_at": datetime.now().isoformat(),
            "source": "2026联网学习"
        }
        
        filename = "net_novel_core_guide_v15.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 核心指南已保存到: {filename}")


def main():
    """主程序"""
    guide = NetNovelCoreGuide()
    guide.demo()


if __name__ == "__main__":
    main()
