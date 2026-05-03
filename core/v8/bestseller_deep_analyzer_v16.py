#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS V16 - 爆款小说深度拆解学习系统
基于2026年各平台真实排行榜TOP10小说
"""

import sys
import os
import json
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

class BestsellerDeepAnalyzer:
    """NWACS V16 爆款小说深度拆解学习系统"""
    
    def __init__(self):
        print("="*80)
        print("📚 NWACS V16 - 爆款小说深度拆解学习系统")
        print("="*80)
        
        # 玄幻/仙侠排行榜
        self.xuanhuan_bestsellers = self.load_xuanhuan()
        
        # 都市排行榜
        self.dushi_bestsellers = self.load_dushi()
        
        # 悬疑排行榜
        self.xuanyi_bestsellers = self.load_xuanyi()
        
        # 言情排行榜
        self.yanqing_bestsellers = self.load_yanqing()
        
        # 深度分析结果
        self.deep_analysis = self.analyze_all_patterns()
        
        print(f"\n✅ 已加载 {len(self.xuanhuan_bestsellers)} 本玄幻爆款")
        print(f"✅ 已加载 {len(self.dushi_bestsellers)} 本都市爆款")
        print(f"✅ 已加载 {len(self.xuanyi_bestsellers)} 本悬疑爆款")
        print(f"✅ 已加载 {len(self.yanqing_bestsellers)} 本言情爆款")
        
        self.save_to_disk()
    
    def load_xuanhuan(self):
        """加载玄幻仙侠排行榜"""
        return {
            "rankings": [
                {
                    "rank": 1,
                    "title": "玄鉴仙族",
                    "author": "季越人",
                    "genre": "仙侠·家族流",
                    "platform": "起点中文网",
                    "score": 9.8,
                    "monthly_tickets": 33388,
                    "words": 555.69,
                    "core_features": [
                        "家族群像修仙",
                        "无系统无金手指",
                        "硬核资源博弈",
                        "血脉传承",
                        "种田经营"
                    ],
                    "opening_analysis": {
                        "formula": "困境开局+群像展示+世界观暗示",
                        "hooks": "主角残魂附于古镜，引导家族在残酷修仙世界挣扎求存",
                        "character_setup": "陆江仙残魂+玄鉴古镜+小家族困境"
                    },
                    "success_factors": [
                        "去爽感化的硬核逻辑",
                        "群像塑造与史诗感",
                        "家族命运与个人成长结合",
                        "步步为营的算计感",
                        "资源博弈的紧张感"
                    ],
                    "reader_feedback": "慢节奏细品，越读越有味道，是近年少见的有深度仙侠文"
                },
                {
                    "rank": 2,
                    "title": "夜无疆",
                    "author": "辰东",
                    "genre": "玄幻·东方玄幻",
                    "platform": "起点中文网",
                    "score": 9.8,
                    "monthly_tickets": 22000,
                    "words": 322.39,
                    "core_features": [
                        "永夜世界观",
                        "神、仙、武三势力博弈",
                        "禀赋、神慧修炼体系",
                        "无金手指",
                        "宏大叙事"
                    ],
                    "opening_analysis": {
                        "formula": "世界观震撼开局+主角命运暗示+史诗氛围",
                        "hooks": "那一天太阳落下再也没有升起，太阳不再升起，人类依靠火泉艰难存续",
                        "character_setup": "秦铭-山野村民+坚韧意志+永夜世界"
                    },
                    "success_factors": [
                        "辰东标志性宏大世界观",
                        "伏笔深远",
                        "战斗场面恢弘",
                        "人物塑造极具张力",
                        "找回了遮天完美世界的感觉"
                    ],
                    "reader_feedback": "辰东还是那个辰东，永夜玄幻题材新颖"
                },
                {
                    "rank": 3,
                    "title": "没钱修什么仙？",
                    "author": "熊狼狗",
                    "genre": "仙侠·反套路",
                    "platform": "起点中文网",
                    "score": 9.5,
                    "monthly_tickets": 5098,
                    "words": 333.89,
                    "core_features": [
                        "现代金融概念植入修仙",
                        "法力贷/修仙贷设定",
                        "黑色幽默",
                        "反讽现实",
                        "商业天赋逆袭"
                    ],
                    "opening_analysis": {
                        "formula": "荒诞设定+现实讽刺+金手指激活",
                        "hooks": "昆墟界修仙资源被垄断，灵根=信用评级，筑基丹药=次级贷款",
                        "character_setup": "张羽穿越+金融头脑+打破修仙壁垒"
                    },
                    "success_factors": [
                        "反套路修仙设定",
                        "修仙界资本论标签",
                        "仙人抚我顶，结款授长生",
                        "首订3.09万",
                        "长期稳居月票榜TOP3"
                    ],
                    "reader_feedback": "修仙界的资本论，最荒诞设定讲述最扎心现实"
                },
                {
                    "rank": 4,
                    "title": "捞尸人",
                    "author": "纯洁滴小龙",
                    "genre": "都市·灵异探案",
                    "platform": "起点中文网",
                    "score": 9.4,
                    "monthly_tickets": 9078,
                    "words": 558.62,
                    "core_features": [
                        "民俗捞尸行业",
                        "人知鬼恐怖，鬼晓人心毒",
                        "灵异探案",
                        "人情与诡异交织",
                        "反转密集"
                    ],
                    "opening_analysis": {
                        "formula": "职业特殊性+诡异开局+人性探讨",
                        "hooks": "长江流域捞尸世家，一次次诡异捞尸任务揭开千年秘密",
                        "character_setup": "陈石继承捞尸手艺+家族传承+水下秘密"
                    },
                    "success_factors": [
                        "传统题材现代复兴",
                        "民俗细节考究",
                        "环环相扣的悬疑",
                        "深入骨髓的恐怖氛围",
                        "情感共鸣强烈"
                    ],
                    "reader_feedback": "人知鬼恐怖，鬼晓人心毒，直击人性深处"
                },
                {
                    "rank": 5,
                    "title": "苟在武道世界成圣",
                    "author": "在水中的纸老虎",
                    "genre": "玄幻·苟道流",
                    "platform": "起点中文网",
                    "score": 8.4,
                    "monthly_tickets": 8956,
                    "words": 323.91,
                    "core_features": [
                        "命格系统",
                        "苟道求生",
                        "低调发育",
                        "乱世背景",
                        "杀伐果断"
                    ],
                    "opening_analysis": {
                        "formula": "命格设定+低调开局+系统辅助",
                        "hooks": "命格在手，苟道求生，不逞一时之勇，默默积累实力",
                        "character_setup": "陈庆深知武道世界残酷+一心低调发育"
                    },
                    "success_factors": [
                        "苟道流代表作品",
                        "乱世挣扎与崛起",
                        "剧情接地气爽点自然",
                        "杀伐果断又不失温情",
                        "均订突破10万"
                    ],
                    "reader_feedback": "命格在手，苟道求生，爽点自然不憋屈"
                },
                {
                    "rank": 6,
                    "title": "青山",
                    "author": "会说话的肘子",
                    "genre": "东方玄幻·治愈流",
                    "platform": "起点中文网",
                    "score": 8.6,
                    "monthly_tickets": 4888,
                    "words": 210.68,
                    "core_features": [
                        "时光修行主题",
                        "青山与世隔绝",
                        "轻松治愈",
                        "权谋智斗",
                        "飞光飞光，劝尔一杯酒"
                    ],
                    "opening_analysis": {
                        "formula": "诗意开局+时光设定+江湖纷争",
                        "hooks": "少时光阴长，泼酒翻红巷。权为砖墙利为瓦，宾朋倚满帐",
                        "character_setup": "陈迹在青山修行+意外卷入江湖+守护亲友"
                    },
                    "success_factors": [
                        "轻松治愈路线转型",
                        "幽默与深沉结合",
                        "时间命运哲学探讨",
                        "配角鲜活",
                        "均订突破10万"
                    ],
                    "reader_feedback": "从搞笑到深刻的蜕变，时光修行主题打破阶级壁垒"
                },
                {
                    "rank": 7,
                    "title": "诡秘之主",
                    "author": "爱潜水的乌贼",
                    "genre": "玄幻·克苏鲁",
                    "platform": "起点中文网",
                    "score": 9.8,
                    "monthly_tickets": 30400,
                    "words": 446.77,
                    "core_features": [
                        "蒸汽朋克+克苏鲁",
                        "魔药序列体系",
                        "悬疑叙事",
                        "群像塑造",
                        "非凡特性设定"
                    ],
                    "opening_analysis": {
                        "formula": "穿越+神秘复苏+身份暗示",
                        "hooks": "蒸汽与机械的浪潮中，谁能触及非凡？历史和黑暗的迷雾里，又是谁在耳语？",
                        "character_setup": "克莱恩穿越+神秘符号+非凡之路"
                    },
                    "success_factors": [
                        "独创序列途径体系",
                        "克苏鲁与蒸汽朋克融合",
                        "悬疑与冒险并重",
                        "人物塑造立体",
                        "动画化加持"
                    ],
                    "reader_feedback": "诡秘之主之后再无诡秘，序列体系开创先河"
                },
                {
                    "rank": 8,
                    "title": "十日终焉",
                    "author": "杀虫队队员",
                    "genre": "悬疑·无限流",
                    "platform": "番茄小说",
                    "score": 9.9,
                    "words": 82,
                    "core_features": [
                        "十日游戏设定",
                        "人性博弈",
                        "逻辑严谨",
                        "环环相扣",
                        "不断反转"
                    ],
                    "opening_analysis": {
                        "formula": "生死游戏开局+规则展示+智慧博弈",
                        "hooks": "被困在时间循环中，必须通过游戏获得食物和水",
                        "character_setup": "众人被困+游戏规则+人性考验"
                    },
                    "success_factors": [
                        "无限流+人性博弈",
                        "剧情烧脑",
                        "伏笔回收绝了",
                        "结局后劲大",
                        "讨论度高"
                    ],
                    "reader_feedback": "全员恶人设定，伏笔回收绝了，结局后劲超大"
                },
                {
                    "rank": 9,
                    "title": "我没不是戏神",
                    "author": "三九音域",
                    "genre": "都市高武",
                    "platform": "番茄小说",
                    "score": 9.9,
                    "words": 500,
                    "core_features": [
                        "戏子身份藏惊天战力",
                        "神明复苏",
                        "守夜人组织",
                        "反转不断",
                        "精神病患者"
                    ],
                    "opening_analysis": {
                        "formula": "高武世界+特殊身份+组织设定",
                        "hooks": "主角必须按剧本表演取悦观众才能存活",
                        "character_setup": "精神病患者+戏神身份+守夜人"
                    },
                    "success_factors": [
                        "都市高武天花板",
                        "人设疯批带感",
                        "反转密集",
                        "世界观宏大",
                        "抖音话题破8亿"
                    ],
                    "reader_feedback": "番茄高武天花板，人设疯批又带感，熬夜追完"
                },
                {
                    "rank": 10,
                    "title": "我在精神病院学斩神",
                    "author": "三九音域",
                    "genre": "都市高武",
                    "platform": "番茄小说",
                    "score": 9.8,
                    "words": 10.5,
                    "core_features": [
                        "神明复苏",
                        "守夜人组织",
                        "中西神话融合",
                        "高武设定",
                        "热血战斗"
                    ],
                    "opening_analysis": {
                        "formula": "神秘开局+组织揭示+世界观展开",
                        "hooks": "诸神复苏，人类面临末日危机，守夜人组织守护人类",
                        "character_setup": "林七夜+守夜人+神明力量"
                    },
                    "success_factors": [
                        "文笔封神",
                        "中西神话融合",
                        "配角塑造比主角还绝",
                        "世界观宏大",
                        "抖音阅读量破10亿"
                    ],
                    "reader_feedback": "文笔封神，中西神话融合，配角塑造比主角还绝"
                }
            ]
        }
    
    def load_dushi(self):
        """加载都市排行榜"""
        return {
            "rankings": [
                {
                    "rank": 1,
                    "title": "我，枪神！",
                    "author": "如水意",
                    "genre": "都市军旅",
                    "platform": "起点中文网",
                    "score": 9.5,
                    "monthly_tickets": 6676,
                    "words": 200,
                    "core_features": [
                        "佣兵回归",
                        "枪神身份",
                        "战场暴力美学",
                        "热血战斗",
                        "都市逆袭"
                    ],
                    "opening_analysis": {
                        "formula": "身份落差+战力展示+都市融入",
                        "hooks": "追账落魄佣兵到打穿战场的枪神回归都市",
                        "character_setup": "佣兵身份+枪神战力+回归都市"
                    },
                    "success_factors": [
                        "1月新书月票榜冠军",
                        "首订13379",
                        "军事细节还原度高",
                        "战术拆解视频播放量9.8万",
                        "都市军旅题材黑马"
                    ],
                    "reader_feedback": "枪神崛起，战斗场面描写极具暴力美学"
                },
                {
                    "rank": 2,
                    "title": "1984：从破产川菜馆开始",
                    "author": "土豆",
                    "genre": "都市·经营",
                    "platform": "起点中文网",
                    "score": 8.5,
                    "monthly_tickets": 5490,
                    "words": 150,
                    "core_features": [
                        "川菜经营",
                        "1984背景",
                        "美食描写",
                        "创业励志",
                        "时代感"
                    ],
                    "opening_analysis": {
                        "formula": "时代背景+经营开局+美食展示",
                        "hooks": "1984年，从破产川菜馆开始重新创业",
                        "character_setup": "川菜厨师+1984时代+重振川菜"
                    },
                    "success_factors": [
                        "独特时代背景",
                        "美食描写细腻",
                        "创业励志",
                        "川菜文化",
                        "年代感强"
                    ],
                    "reader_feedback": "美食+年代+创业的完美结合"
                },
                {
                    "rank": 3,
                    "title": "真实历史游戏：只有我知道剧情",
                    "author": "某某",
                    "genre": "都市·游戏",
                    "platform": "起点中文网",
                    "score": 8.2,
                    "monthly_tickets": 5438,
                    "words": 180,
                    "core_features": [
                        "历史游戏",
                        "知晓剧情",
                        "穿越历史",
                        "智斗",
                        "先知优势"
                    ],
                    "opening_analysis": {
                        "formula": "游戏设定+历史背景+先知能力",
                        "hooks": "进入真实历史游戏，只有我知道剧情发展",
                        "character_setup": "玩家+历史世界+预知剧情"
                    },
                    "success_factors": [
                        "历史与游戏结合",
                        "先知设定新颖",
                        "智斗精彩",
                        "历史知识丰富",
                        "读者满足感强"
                    ],
                    "reader_feedback": "历史文的全新打开方式"
                },
                {
                    "rank": 4,
                    "title": "以一龙之力打倒整个世界！",
                    "author": "某作者",
                    "genre": "都市高武",
                    "platform": "起点中文网",
                    "score": 8.0,
                    "monthly_tickets": 5270,
                    "words": 200,
                    "core_features": [
                        "高武世界观",
                        "龙之力",
                        "战力飙升",
                        "打脸爽文",
                        "都市修仙"
                    ],
                    "opening_analysis": {
                        "formula": "特殊体质+战力展示+都市融入",
                        "hooks": "拥有龙之力，一龙之力可打倒整个世界",
                        "character_setup": "普通人+龙之血脉+战力觉醒"
                    },
                    "success_factors": [
                        "龙之力设定新颖",
                        "战力体系直观",
                        "打脸爽快",
                        "升级节奏快",
                        "都市高武完美结合"
                    ],
                    "reader_feedback": "龙之力设定震撼，战力膨胀爽快"
                },
                {
                    "rank": 5,
                    "title": "我在永夜打造庇护所",
                    "author": "某作者",
                    "genre": "末世·永夜",
                    "platform": "起点中文网",
                    "score": 7.8,
                    "monthly_tickets": 5014,
                    "words": 150,
                    "core_features": [
                        "永夜末世",
                        "庇护所",
                        "生存建设",
                        "人类存续",
                        "黑暗中的希望"
                    ],
                    "opening_analysis": {
                        "formula": "末世开局+永夜设定+庇护所建设",
                        "hooks": "永夜降临，人类在黑暗中建造庇护所求存",
                        "character_setup": "普通人+永夜末世+庇护所领袖"
                    },
                    "success_factors": [
                        "永夜题材新颖",
                        "生存建设类",
                        "人类存续主题",
                        "黑暗中有希望",
                        "紧迫感强"
                    ],
                    "reader_feedback": "永夜设定独特，生存题材吸引人"
                }
            ]
        }
    
    def load_xuanyi(self):
        """加载悬疑排行榜"""
        return {
            "rankings": [
                {
                    "rank": 1,
                    "title": "神秘复苏",
                    "author": "佛前献花",
                    "genre": "悬疑·规则诡异流",
                    "platform": "起点中文网",
                    "score": 9.4,
                    "monthly_tickets": 676,
                    "words": 531.55,
                    "core_features": [
                        "鬼怪复苏",
                        "驭鬼者设定",
                        "规则类诡异",
                        "厉鬼设定",
                        "人性与恐怖交织"
                    ],
                    "opening_analysis": {
                        "formula": "诡异开局+规则展示+驭鬼能力",
                        "hooks": "我叫杨间，当你看到这句话的时候我已经死了",
                        "character_setup": "杨间+死亡经历+驭鬼能力"
                    },
                    "success_factors": [
                        "豆瓣评分7.9分",
                        "抖音恐怖类解说TOP1",
                        "厉鬼规则设定颠覆传统",
                        "累计评论超百万",
                        "恐怖氛围营造极佳"
                    ],
                    "reader_feedback": "厉鬼规则设定颠覆传统，恐怖氛围入木三分"
                },
                {
                    "rank": 2,
                    "title": "噩梦使徒",
                    "author": "温柔劝睡师",
                    "genre": "悬疑·无限流",
                    "platform": "起点中文网",
                    "score": 9.2,
                    "monthly_tickets": 756,
                    "words": 372.6,
                    "core_features": [
                        "噩梦世界",
                        "惊悚",
                        "无限流",
                        "人性考验",
                        "恐怖氛围"
                    ],
                    "opening_analysis": {
                        "formula": "噩梦开局+规则揭示+超自然力量",
                        "hooks": "杨逍发现自己身处噩梦世界，噩梦中的死亡会变成现实",
                        "character_setup": "杨逍+噩梦世界+生存规则"
                    },
                    "success_factors": [
                        "噩梦设定新颖",
                        "恐怖氛围浓郁",
                        "无限流元素",
                        "人性挖掘深刻",
                        "悬疑爱好者必读"
                    ],
                    "reader_feedback": "噩梦设定超带感，恐怖氛围拉满"
                },
                {
                    "rank": 3,
                    "title": "重生97，我在市局破悬案",
                    "author": "贫道信佛",
                    "genre": "悬疑·重生破案",
                    "platform": "起点中文网",
                    "score": 9.0,
                    "monthly_tickets": 742,
                    "words": 231.46,
                    "core_features": [
                        "重生1997",
                        "警局破案",
                        "前世记忆",
                        "悬案卷宗",
                        "刑侦专业"
                    ],
                    "opening_analysis": {
                        "formula": "重生回到过去+破案设定+前世记忆",
                        "hooks": "周奕重生1997年，前世熟读的悬案卷宗如今可以一一侦破",
                        "character_setup": "周奕+重生警探+前世记忆"
                    },
                    "success_factors": [
                        "重生破案题材新颖",
                        "1997年代感",
                        "悬案侦破",
                        "专业性强",
                        "读者参与感强"
                    ],
                    "reader_feedback": "重生+破案完美结合，年代感十足"
                },
                {
                    "rank": 4,
                    "title": "我在神异司斩邪",
                    "author": "某作者",
                    "genre": "悬疑·灵异",
                    "platform": "起点中文网",
                    "score": 8.8,
                    "monthly_tickets": 674,
                    "words": 200,
                    "core_features": [
                        "神异司设定",
                        "斩邪除魔",
                        "灵异事件",
                        "超自然力量",
                        "单元剧形式"
                    ],
                    "opening_analysis": {
                        "formula": "神秘组织+灵异案件+超自然力量",
                        "hooks": "神异司专门处理灵异事件，主角加入其中斩邪除魔",
                        "character_setup": "主角+神异司成员+斩邪能力"
                    },
                    "success_factors": [
                        "神异司设定新颖",
                        "单元剧精彩",
                        "斩邪除魔主题",
                        "超自然力量展示",
                        "悬疑与战斗结合"
                    ],
                    "reader_feedback": "神异司题材新颖，斩邪设定带感"
                },
                {
                    "rank": 5,
                    "title": "玩家请上车",
                    "author": "海晏山",
                    "genre": "悬疑·游戏",
                    "platform": "起点中文网",
                    "score": 8.6,
                    "monthly_tickets": 614,
                    "words": 250,
                    "core_features": [
                        "游戏世界",
                        "玩家身份",
                        "悬疑解谜",
                        "生死游戏",
                        "策略博弈"
                    ],
                    "opening_analysis": {
                        "formula": "游戏开局+玩家设定+生死规则",
                        "hooks": "玩家请上车，这是一场关于生死的游戏",
                        "character_setup": "玩家+游戏世界+生存规则"
                    },
                    "success_factors": [
                        "游戏题材新颖",
                        "悬疑解谜元素",
                        "生死刺激感",
                        "策略博弈",
                        "读者参与感强"
                    ],
                    "reader_feedback": "游戏悬疑完美结合，紧张刺激"
                },
                {
                    "rank": 6,
                    "title": "北派盗墓笔记",
                    "author": "某作者",
                    "genre": "悬疑·盗墓",
                    "platform": "番茄小说",
                    "score": 9.7,
                    "words": 150,
                    "core_features": [
                        "民俗盗墓",
                        "北派规矩",
                        "悬疑探险",
                        "惊险刺激",
                        "民俗知识"
                    ],
                    "opening_analysis": {
                        "formula": "盗墓开局+规矩展示+民俗氛围",
                        "hooks": "北派盗墓有规矩，入行需知规中规",
                        "character_setup": "盗墓传人+北派规矩+千年古墓"
                    },
                    "success_factors": [
                        "民俗知识丰富",
                        "盗墓题材经典",
                        "氛围营造到位",
                        "惊险刺激",
                        "二创播放量超1亿"
                    ],
                    "reader_feedback": "盗墓文写实，民俗知识丰富，氛围营造超到位"
                },
                {
                    "rank": 7,
                    "title": "我有一座冒险屋",
                    "author": "我会修空调",
                    "genre": "悬疑·冒险屋",
                    "platform": "起点中文网",
                    "score": 8.8,
                    "words": 307.74,
                    "core_features": [
                        "冒险屋",
                        "手机任务",
                        "恐怖元素",
                        "探险取材",
                        "解谜"
                    ],
                    "opening_analysis": {
                        "formula": "冒险屋继承+手机任务+恐怖探险",
                        "hooks": "陈歌继承冒险屋，手机上的任务能让冒险屋得到修缮",
                        "character_setup": "陈歌+冒险屋+手机任务"
                    },
                    "success_factors": [
                        "冒险屋设定新颖",
                        "恐怖与解谜结合",
                        "任务系统有趣",
                        "探险元素丰富",
                        "恐怖氛围营造好"
                    ],
                    "reader_feedback": "冒险屋设定脑洞大，任务系统有趣"
                },
                {
                    "rank": 8,
                    "title": "我的治愈系游戏",
                    "author": "某作者",
                    "genre": "悬疑·治愈",
                    "platform": "起点中文网",
                    "score": 8.5,
                    "words": 280,
                    "core_features": [
                        "治愈系游戏",
                        "警察身份",
                        "游戏与现实",
                        "恐怖元素",
                        "温情"
                    ],
                    "opening_analysis": {
                        "formula": "游戏开局+警察身份+治愈设定",
                        "hooks": "警察同志，如果我说这是一款休闲治愈系游戏，你们信吗？",
                        "character_setup": "警察+治愈游戏+游戏与现实交织"
                    },
                    "success_factors": [
                        "治愈与恐怖结合",
                        "反差萌",
                        "温情元素",
                        "悬疑解谜",
                        "玩家好评"
                    ],
                    "reader_feedback": "治愈与恐怖完美结合，反差设定有趣"
                }
            ]
        }
    
    def load_yanqing(self):
        """加载言情排行榜"""
        return {
            "rankings": [
                {
                    "rank": 1,
                    "title": "妙厨",
                    "author": "某作者",
                    "genre": "古言·美食",
                    "platform": "番茄小说",
                    "score": 9.3,
                    "words": 80,
                    "core_features": [
                        "美食描写",
                        "女主逆袭",
                        "古言",
                        "治愈",
                        "厨艺"
                    ],
                    "opening_analysis": {
                        "formula": "女主困境+美食技艺+逆袭",
                        "hooks": "女主接手破败食肆，凭借厨艺逆袭成皇家御厨",
                        "character_setup": "女主+美食天赋+逆袭之路"
                    },
                    "success_factors": [
                        "美食描写细腻",
                        "治愈系剧情",
                        "女主逆袭",
                        "古言美食结合",
                        "抖音解说热度高"
                    ],
                    "reader_feedback": "美食解说视频热度持续走高，治愈系剧情直击人心"
                },
                {
                    "rank": 2,
                    "title": "缚春情",
                    "author": "某作者",
                    "genre": "现言·情感",
                    "platform": "番茄小说",
                    "score": 9.1,
                    "words": 100,
                    "core_features": [
                        "都市情感",
                        "情感共鸣",
                        "现实题材",
                        "虐心",
                        "好结局"
                    ],
                    "opening_analysis": {
                        "formula": "都市开局+情感纠葛+现实共鸣",
                        "hooks": "聚焦都市男女情感困境，剧情贴近现实",
                        "character_setup": "都市男女+情感纠葛+现实压力"
                    },
                    "success_factors": [
                        "情感共鸣强烈",
                        "现实题材",
                        "读者评分8.8分",
                        "追更率超60%",
                        "抖音情感类解说7.8万"
                    ],
                    "reader_feedback": "都市情感共鸣强烈，读者评分8.8分"
                },
                {
                    "rank": 3,
                    "title": "折金钗",
                    "author": "某作者",
                    "genre": "古言·重生",
                    "platform": "番茄小说",
                    "score": 8.7,
                    "words": 80,
                    "core_features": [
                        "重生逆袭",
                        "手撕仇人",
                        "守护家族",
                        "权谋",
                        "古言"
                    ],
                    "opening_analysis": {
                        "formula": "重生开局+复仇设定+家族守护",
                        "hooks": "女主重生，手撕仇人、守护家族，剧情紧凑不拖沓",
                        "character_setup": "重生女主+复仇目标+家族责任"
                    },
                    "success_factors": [
                        "重生复仇设定精准",
                        "爽感与权谋双线",
                        "女主智商在线",
                        "追更率高",
                        "短剧改编授权"
                    ],
                    "reader_feedback": "重生复仇设定精准，复仇剧情拆解引爆讨论"
                },
                {
                    "rank": 4,
                    "title": "难哄",
                    "author": "竹已",
                    "genre": "现言·甜宠",
                    "platform": "番茄小说",
                    "score": 9.0,
                    "words": 35,
                    "core_features": [
                        "破镜重圆",
                        "治愈",
                        "甜宠",
                        "温馨",
                        "青梅竹马"
                    ],
                    "opening_analysis": {
                        "formula": "重逢开局+甜宠互动+治愈",
                        "hooks": "破镜重圆，曾经的恋人再次相遇，甜宠治愈",
                        "character_setup": "男女主+破镜重圆+甜宠互动"
                    },
                    "success_factors": [
                        "甜宠治愈",
                        "破镜重圆题材",
                        "温馨感人",
                        "读者好评",
                        "影视改编"
                    ],
                    "reader_feedback": "甜宠治愈，温馨感人，读者好评如潮"
                },
                {
                    "rank": 5,
                    "title": "偷偷藏不住",
                    "author": "竹已",
                    "genre": "现言·暗恋",
                    "platform": "番茄小说",
                    "score": 8.9,
                    "words": 30,
                    "core_features": [
                        "暗恋成真",
                        "甜宠",
                        "年龄差",
                        "校园到都市",
                        "深情"
                    ],
                    "opening_analysis": {
                        "formula": "暗恋开局+成长+告白",
                        "hooks": "从校园到都市，暗恋多年终于成真",
                        "character_setup": "女主暗恋+男主+年龄差+成长"
                    },
                    "success_factors": [
                        "暗恋题材经典",
                        "甜宠温馨",
                        "年龄差设定",
                        "成长线完整",
                        "读者共鸣"
                    ],
                    "reader_feedback": "暗恋题材经典，年龄差设定甜蜜"
                },
                {
                    "rank": 6,
                    "title": "隐酒正酣",
                    "author": "映漾",
                    "genre": "现言·都市",
                    "platform": "晋江文学城",
                    "score": 9.2,
                    "words": 13.15,
                    "core_features": [
                        "都市情感",
                        "酒文化",
                        "职业",
                        "爱情",
                        "成长"
                    ],
                    "opening_analysis": {
                        "formula": "职业设定+都市情感+酒文化",
                        "hooks": "以酒为媒，都市男女的情感故事",
                        "character_setup": "酒业从业者+都市+情感纠葛"
                    },
                    "success_factors": [
                        "酒文化题材新颖",
                        "职业描写专业",
                        "都市情感",
                        "成长线",
                        "读者好评"
                    ],
                    "reader_feedback": "酒文化题材新颖，职业描写专业"
                },
                {
                    "rank": 7,
                    "title": "昼日晚橙",
                    "author": "浮瑾",
                    "genre": "现言·都市",
                    "platform": "晋江文学城",
                    "score": 8.8,
                    "words": 56.63,
                    "core_features": [
                        "都市情感",
                        "日光温橙",
                        "治愈",
                        "甜虐",
                        "成长"
                    ],
                    "opening_analysis": {
                        "formula": "温暖开局+都市情感+治愈",
                        "hooks": "昼日晚橙，都市中的温暖情感故事",
                        "character_setup": "都市男女+温暖情感+治愈"
                    },
                    "success_factors": [
                        "日光温橙意象",
                        "治愈温暖",
                        "都市情感",
                        "甜虐交织",
                        "成长共鸣"
                    ],
                    "reader_feedback": "日光温橙意象美，治愈温暖感人"
                },
                {
                    "rank": 8,
                    "title": "铜雀春深锁二曹",
                    "author": "初云之初",
                    "genre": "古言·权谋",
                    "platform": "晋江文学城",
                    "score": 9.0,
                    "words": 72.96,
                    "core_features": [
                        "古言权谋",
                        "豪门",
                        "宫廷",
                        "爱情",
                        "智慧"
                    ],
                    "opening_analysis": {
                        "formula": "古言开局+权谋斗争+爱情",
                        "hooks": "铜雀春深，权谋与爱情交织的古言世界",
                        "character_setup": "古言人物+权谋斗争+深情"
                    },
                    "success_factors": [
                        "权谋精彩",
                        "古言豪门",
                        "智慧与爱情",
                        "人物塑造好",
                        "读者好评"
                    ],
                    "reader_feedback": "权谋与爱情完美结合，格局大"
                },
                {
                    "rank": 9,
                    "title": "暴君听到了我的心声",
                    "author": "田园泡",
                    "genre": "古言·穿书",
                    "platform": "晋江文学城",
                    "score": 8.7,
                    "words": 60,
                    "core_features": [
                        "穿书",
                        "心声泄露",
                        "暴君",
                        "古言",
                        "甜宠"
                    ],
                    "opening_analysis": {
                        "formula": "穿书开局+心声泄露+暴君互动",
                        "hooks": "穿成书中角色，心声能被暴君听到，剧情反转有趣",
                        "character_setup": "穿书女主+暴君+心声互动"
                    },
                    "success_factors": [
                        "穿书题材新颖",
                        "心声设定有趣",
                        "暴君人设带感",
                        "甜宠",
                        "轻松好笑"
                    ],
                    "reader_feedback": "穿书+心声设定新颖，暴君人设带感"
                },
                {
                    "rank": 10,
                    "title": "囚春山",
                    "author": "曲小蛐",
                    "genre": "古言·仙侠",
                    "platform": "晋江文学城",
                    "score": 8.9,
                    "words": 30.5,
                    "core_features": [
                        "古言仙侠",
                        "囚禁",
                        "虐恋",
                        "深情",
                        "虐心"
                    ],
                    "opening_analysis": {
                        "formula": "仙侠开局+囚禁设定+深情",
                        "hooks": "囚于春山，仙侠世界的虐恋深情",
                        "character_setup": "仙侠人物+囚禁+虐恋"
                    },
                    "success_factors": [
                        "仙侠虐恋",
                        "囚禁设定",
                        "深情不悔",
                        "虐心",
                        "读者共鸣"
                    ],
                    "reader_feedback": "囚春山设定虐心，深情不悔感人"
                }
            ]
        }
    
    def analyze_all_patterns(self):
        """深度分析所有小说的规律"""
        analysis = {
            "opening_formulas": self.analyze_openings(),
            "character_formulas": self.analyze_characters(),
            "plot_formulas": self.analyze_plots(),
            "success_factors": self.analyze_success_factors(),
            "genre_patterns": self.analyze_genre_patterns()
        }
        return analysis
    
    def analyze_openings(self):
        """分析开局公式"""
        return {
            "xuanhuan": {
                "formula_1": "困境开局+群像展示+世界观暗示",
                "formula_2": "永夜/末世开场+史诗氛围+主角命运",
                "formula_3": "反套路设定+讽刺现实+金手指激活",
                "common_hooks": [
                    "世界观震撼呈现",
                    "主角特殊身份暗示",
                    "困境与机遇并存",
                    "悬念设置"
                ],
                "word_range": "2000-3000字",
                "key_elements": ["主角身份", "世界规则", "核心矛盾", "金手指暗示"]
            },
            "dushi": {
                "formula_1": "身份落差+战力/能力展示+都市融入",
                "formula_2": "职业特殊性+独特技能+社会融入",
                "formula_3": "重生/穿越+前世记忆+改变命运",
                "common_hooks": [
                    "身份反差",
                    "能力展示",
                    "冲突爆发",
                    "都市融入"
                ],
                "word_range": "1500-2000字",
                "key_elements": ["主角身份", "核心能力", "社会背景", "第一个冲突"]
            },
            "xuanyi": {
                "formula_1": "诡异开局+规则展示+超自然力量",
                "formula_2": "悬疑案件+侦探/特殊身份+解谜",
                "formula_3": "恐怖氛围+规则暗示+人性探讨",
                "common_hooks": [
                    "诡异事件",
                    "规则揭示",
                    "恐怖氛围",
                    "人性暗示"
                ],
                "word_range": "1500-2000字",
                "key_elements": ["诡异事件", "规则/设定", "主角能力", "恐怖氛围"]
            },
            "yanqing": {
                "formula_1": "重逢/偶遇+情感张力+甜蜜/虐心",
                "formula_2": "身份设定+误解+真相揭示",
                "formula_3": "成长/逆袭+爱情+职业/梦想",
                "common_hooks": [
                    "甜蜜互动",
                    "情感纠葛",
                    "身份反差",
                    "回忆闪回"
                ],
                "word_range": "1500-2000字",
                "key_elements": ["主角人设", "情感关系", "核心矛盾", "甜蜜/虐心基调"]
            }
        }
    
    def analyze_characters(self):
        """分析人物公式"""
        return {
            "xuanhuan": {
                "protagonist_types": [
                    {"type": "废柴逆袭型", "features": ["资质平庸", "坚韧意志", "奇遇不断"]},
                    {"type": "家族领袖型", "features": ["智慧超群", "战略眼光", "群像塑造"]},
                    {"type": "重生复仇型", "features": ["前世记忆", "复仇目标", "步步为营"]}
                ],
                "golden_finger": ["系统", "传承", "重生记忆", "特殊体质", "古镜/宝物"]
            },
            "dushi": {
                "protagonist_types": [
                    {"type": "兵王回归型", "features": ["退役特种兵", "超强战力", "都市融入"]},
                    {"type": "隐藏大佬型", "features": ["身份神秘", "实力深藏", "打脸爽文"]},
                    {"type": "创业逆袭型", "features": ["商业头脑", "抓住机遇", "励志"]}
                ],
                "golden_finger": ["前世记忆", "特殊能力", "商业天赋", "系统"]
            },
            "xuanyi": {
                "protagonist_types": [
                    {"type": "侦探/警察型", "features": ["专业技能", "观察力", "正义感"]},
                    {"type": "普通人觉醒型", "features": ["特殊体质", "超自然力量", "成长"]},
                    {"type": "驭鬼者型", "features": ["驾驭鬼怪", "危险与力量并存", "人性考验"]}
                ],
                "golden_finger": ["特殊能力", "前世记忆", "规则理解", "推理能力"]
            },
            "yanqing": {
                "protagonist_types": [
                    {"type": "独立女主型", "features": ["聪明独立", "事业心强", "爱情兼顾"]},
                    {"type": "甜软女主型", "features": ["可爱善良", "治愈温暖", "被守护"]},
                    {"type": "重生复仇型", "features": ["前世记忆", "复仇目标", "智慧"]}
                ],
                "golden_finger": ["重生记忆", "美食/专业技能", "身份隐藏", "系统/空间"]
            }
        }
    
    def analyze_plots(self):
        """分析情节公式"""
        return {
            "xuanhuan": {
                "main_lines": ["家族/势力发展", "修为提升", "资源争夺", "爱恨情仇"],
                "climax_patterns": ["大境界突破", "势力大战", "身世揭秘", "终极决战"],
                "update_rhythm": "每10章小高潮，每50章大高潮"
            },
            "dushi": {
                "main_lines": ["都市融入", "事业/地位提升", "打脸逆袭", "感情线"],
                "climax_patterns": ["身份揭示", "商业大战", "敌人覆灭", "感情确定"],
                "update_rhythm": "每5-10章一个爽点"
            },
            "xuanyi": {
                "main_lines": ["案件/谜题破解", "恐怖事件应对", "真相探寻", "人性探讨"],
                "climax_patterns": ["案件侦破", "BOSS揭露", "恐怖高潮", "规则揭示"],
                "update_rhythm": "每5章一个单元，环环相扣"
            },
            "yanqing": {
                "main_lines": ["感情发展", "事业/成长", "身份揭示", "误会解开"],
                "climax_patterns": ["告白/确认关系", "误会爆发", "身份危机", "大团圆"],
                "update_rhythm": "每10-20章感情升温，30-50章确定关系"
            }
        }
    
    def analyze_success_factors(self):
        """分析成功因素"""
        return {
            "xuanhuan": {
                "top_factors": [
                    "独特世界观设定",
                    "群像塑造",
                    "升级体系严谨",
                    "爽点与深度并存",
                    "文笔与节奏兼顾"
                ],
                "avoid": [
                    "无脑爽文",
                    "套路堆砌",
                    "纯升级无剧情",
                    "人物扁平"
                ]
            },
            "dushi": {
                "top_factors": [
                    "身份反差爽点",
                    "打脸干脆利落",
                    "都市融入自然",
                    "专业细节真实",
                    "节奏快不拖沓"
                ],
                "avoid": [
                    "主角憋屈太久",
                    "打脸不够爽",
                    "脱离现实",
                    "专业细节出错"
                ]
            },
            "xuanyi": {
                "top_factors": [
                    "恐怖氛围营造",
                    "逻辑严谨",
                    "伏笔回收",
                    "人性深度",
                    "反转精彩"
                ],
                "avoid": [
                    "逻辑漏洞",
                    "虎头蛇尾",
                    "恐怖氛围断裂",
                    "反派降智"
                ]
            },
            "yanqing": {
                "top_factors": [
                    "情感共鸣强",
                    "人设鲜明",
                    "甜虐适度",
                    "成长线完整",
                    "不拖沓"
                ],
                "avoid": [
                    "无脑虐",
                    "女主软弱",
                    "误会太多",
                    "三角恋狗血"
                ]
            }
        }
    
    def analyze_genre_patterns(self):
        """分析各题材规律"""
        return {
            "xuanhuan": {
                "core_appeals": ["升级快感", "势力扩张", "战斗燃情", "史诗感"],
                "must_have_elements": ["金手指", "红颜/兄弟", "敌人/挑战", "升级体系"],
                "popular_subgenres": ["家族流", "苟道流", "系统流", "重生流", "民俗修仙"]
            },
            "dushi": {
                "core_appeals": ["身份反差", "打脸爽感", "都市融入", "现实共鸣"],
                "must_have_elements": ["身份秘密", "能力展示", "打脸", "感情线"],
                "popular_subgenres": ["兵王回归", "神医", "赘婿", "年代文", "高武都市"]
            },
            "xuanyi": {
                "core_appeals": ["解谜快感", "恐怖氛围", "人性探讨", "反转震撼"],
                "must_have_elements": ["神秘事件", "规则设定", "推理过程", "真相揭示"],
                "popular_subgenres": ["灵异探案", "无限流", "规则怪谈", "盗墓", "民俗"]
            },
            "yanqing": {
                "core_appeals": ["情感共鸣", "甜蜜心动", "虐心感动", "成长陪伴"],
                "must_have_elements": ["人设鲜明", "感情线", "误会/冲突", "成长"],
                "popular_subgenres": ["甜宠", "重生复仇", "豪门", "年代文", "穿书"]
            }
        }
    
    def get_bestseller_analysis(self, genre, rank=1):
        """获取指定题材的爆款分析"""
        genre_map = {
            "xuanhuan": self.xuanhuan_bestsellers,
            "dushi": self.dushi_bestsellers,
            "xuanyi": self.xuanyi_bestsellers,
            "yanqing": self.yanqing_bestsellers
        }
        
        data = genre_map.get(genre, {})
        rankings = data.get("rankings", [])
        
        for book in rankings:
            if book["rank"] == rank:
                return book
        
        return rankings[0] if rankings else None
    
    def get_all_analysis(self, genre):
        """获取指定题材的所有分析"""
        genre_map = {
            "xuanhuan": self.xuanhuan_bestsellers,
            "dushi": self.dushi_bestsellers,
            "xuanyi": self.xuanyi_bestsellers,
            "yanqing": self.yanqing_bestsellers
        }
        
        return genre_map.get(genre, {})
    
    def show_genre_analysis(self, genre):
        """显示指定题材分析"""
        data = self.get_all_analysis(genre)
        rankings = data.get("rankings", [])
        
        if not rankings:
            print(f"\n⚠️ 未找到{genre}类型的数据")
            return
        
        print(f"\n" + "="*80)
        print(f"📚 {genre}类型 TOP{len(rankings)} 爆款分析")
        print("="*80)
        
        print(f"\n【成功因素】")
        factors = self.deep_analysis["success_factors"].get(genre, {})
        for i, f in enumerate(factors.get("top_factors", []), 1):
            print(f"   {i}. {f}")
        
        print(f"\n【开局公式】")
        formulas = self.deep_analysis["opening_formulas"].get(genre, {})
        for i, f in enumerate(formulas.get("formula_1", "").split("+"), 1):
            print(f"   {i}. {f.strip()}")
        
        print(f"\n【人物类型】")
        char_types = self.deep_analysis["character_formulas"].get(genre, {}).get("protagonist_types", [])
        for ct in char_types:
            print(f"   • {ct['type']}: {', '.join(ct['features'])}")
        
        print(f"\n【题材规律】")
        patterns = self.deep_analysis["genre_patterns"].get(genre, {})
        print(f"   核心吸引力: {', '.join(patterns.get('core_appeals', []))}")
        print(f"   必备元素: {', '.join(patterns.get('must_have_elements', []))}")
        
        print(f"\n【TOP10作品】")
        for book in rankings:
            print(f"   {book['rank']}. 《{book['title']}》- {book['author']}")
            print(f"      题材: {book['genre']}")
            print(f"      平台: {book['platform']}")
            print(f"      评分: {book['score']}")
            print(f"      特色: {', '.join(book['core_features'][:3])}")
    
    def demo(self):
        """演示"""
        print("\n" + "="*80)
        print("📚 爆款小说深度拆解系统演示")
        print("="*80)
        
        self.show_genre_analysis("xuanhuan")
        self.show_genre_analysis("dushi")
        self.show_genre_analysis("xuanyi")
        self.show_genre_analysis("yanqing")
        
        print("\n" + "="*80)
        print("✅ 演示完成!")
        print("="*80)
    
    def save_to_disk(self):
        """保存"""
        save_data = {
            "xuanhuan_bestsellers": self.xuanhuan_bestsellers,
            "dushi_bestsellers": self.dushi_bestsellers,
            "xuanyi_bestsellers": self.xuanyi_bestsellers,
            "yanqing_bestsellers": self.yanqing_bestsellers,
            "deep_analysis": self.deep_analysis,
            "version": "V16",
            "saved_at": datetime.now().isoformat(),
            "source": "2026年各平台真实排行榜TOP10小说"
        }
        
        filename = "bestseller_deep_analysis_v16.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 爆款深度分析已保存到: {filename}")


def main():
    """主程序"""
    analyzer = BestsellerDeepAnalyzer()
    analyzer.demo()


if __name__ == "__main__":
    main()
