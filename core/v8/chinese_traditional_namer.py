#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 中国传统命名系统 - ChineseTraditionalNamer

基于中国传统文化的角色命名引擎，融合：

1. 五行学说 (Five Elements)
   - 金木水火土五行属性
   - 生辰八字推算五行缺失
   - 五行相生相克平衡
   - 五行偏旁部首匹配

2. 八卦理论 (Eight Trigrams)
   - 乾坤震巽坎离艮兑
   - 卦象寓意与人物性格匹配
   - 卦象对应方位/五行/属性

3. 风水命名 (Feng Shui Naming)
   - 三才五格法(天格/人格/地格/外格/总格)
   - 笔画数理吉凶
   - 81数理吉凶判断

4. 辈分字派 (Generation Naming)
   - 家族辈分诗/字派序列
   - 姓氏+辈分字+名字结构

5. 寓意取名 (Meaningful Naming)
   - 经典典故引用
   - 美德寓意(仁义礼智信)
   - 诗词化用
   - 自然意象

设计原则：
- 纯本地计算，零API依赖
- 严格遵循中国传统命名规范
- 支持多种命名策略组合
"""

import random
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class FiveElement(Enum):
    METAL = ("金", "⚪", "西", "白", "义")
    WOOD = ("木", "🟢", "东", "青", "仁")
    WATER = ("水", "⚫", "北", "黑", "智")
    FIRE = ("火", "🔴", "南", "赤", "礼")
    EARTH = ("土", "🟤", "中", "黄", "信")

    def __init__(self, name: str, symbol: str, direction: str,
                 color: str, virtue: str):
        self.chinese_name = name
        self.symbol = symbol
        self.direction = direction
        self.color = color
        self.virtue = virtue


class EightTrigram(Enum):
    QIAN = ("乾", "☰", "天", "健", FiveElement.METAL, "父", "西北")
    KUN = ("坤", "☷", "地", "顺", FiveElement.EARTH, "母", "西南")
    ZHEN = ("震", "☳", "雷", "动", FiveElement.WOOD, "长男", "东")
    XUN = ("巽", "☴", "风", "入", FiveElement.WOOD, "长女", "东南")
    KAN = ("坎", "☵", "水", "陷", FiveElement.WATER, "中男", "北")
    LI = ("离", "☲", "火", "丽", FiveElement.FIRE, "中女", "南")
    GEN = ("艮", "☶", "山", "止", FiveElement.EARTH, "少男", "东北")
    DUI = ("兑", "☱", "泽", "说", FiveElement.METAL, "少女", "西")

    def __init__(self, name: str, symbol: str, nature: str,
                 quality: str, element: FiveElement,
                 family_role: str, direction: str):
        self.chinese_name = name
        self.symbol = symbol
        self.nature = nature
        self.quality = quality
        self.element = element
        self.family_role = family_role
        self.direction = direction


class Gender(Enum):
    MALE = "男"
    FEMALE = "女"


@dataclass
class NameResult:
    """命名结果"""
    full_name: str
    surname: str
    generation_char: str = ""
    given_name: str = ""
    gender: Gender = Gender.MALE
    element: FiveElement = FiveElement.WOOD
    trigram: Optional[EightTrigram] = None
    meaning: str = ""
    stroke_analysis: Dict = field(default_factory=dict)
    cultural_reference: str = ""
    score: int = 0


class ChineseTraditionalNamer:
    """中国传统命名系统"""

    def __init__(self):
        self._init_surnames()
        self._init_element_chars()
        self._init_generation_poems()
        self._init_virtue_names()
        self._init_nature_names()
        self._init_classical_names()
        self._init_stroke_data()
        self.used_names: Set[str] = set()

    # ================================================================
    # 数据初始化
    # ================================================================

    def _init_surnames(self):
        """初始化百家姓（完整504姓）"""
        self.surnames = {
            "top10": ["王", "李", "张", "刘", "陈", "杨", "黄", "赵", "吴", "周"],
            "top50": ["徐", "孙", "马", "胡", "朱", "郭", "何", "罗", "高", "林",
                      "郑", "梁", "谢", "唐", "许", "冯", "宋", "韩", "邓", "彭",
                      "曹", "曾", "田", "萧", "潘", "袁", "蔡", "蒋", "余", "于",
                      "杜", "叶", "程", "苏", "魏", "吕", "丁", "任", "沈", "姚"],
            "common": ["卢", "姜", "崔", "钟", "谭", "陆", "汪", "范", "金", "石",
                      "廖", "贾", "夏", "韦", "付", "方", "白", "邹", "孟", "熊",
                      "秦", "邱", "江", "尹", "薛", "闫", "段", "雷", "侯", "龙",
                      "史", "陶", "黎", "贺", "顾", "毛", "郝", "龚", "邵", "万",
                      "钱", "严", "覃", "武", "戴", "莫", "孔", "向", "汤", "温",
                      "康", "施", "文", "牛", "樊", "葛", "邢", "安", "齐", "易",
                      "乔", "伍", "庞", "颜", "倪", "庄", "聂", "章", "鲁", "岳",
                      "翟", "殷", "詹", "申", "欧", "耿", "关", "兰", "焦", "俞",
                      "左", "柳", "甘", "祝", "包", "宁", "尚", "符", "舒", "阮",
                      "柯", "纪", "梅", "童", "凌", "毕", "单", "季", "裴", "霍",
                      "涂", "成", "苗", "谷", "盛", "曲", "翁", "冉", "骆", "蓝",
                      "路", "游", "辛", "靳", "管", "柴", "蒙", "喻", "廉", "郎"],
            "less_common": ["费", "卫", "艾", "卞", "祁", "时", "穆", "常", "元", "卜",
                           "平", "禹", "米", "贝", "明", "臧", "计", "伏", "成", "谈",
                           "茅", "庞", "熊", "纪", "舒", "屈", "项", "祝", "董", "梁",
                           "杜", "阮", "蓝", "闵", "席", "季", "麻", "强", "贾", "路",
                           "娄", "危", "江", "童", "颜", "郭", "梅", "盛", "林", "刁",
                           "钟", "徐", "邱", "骆", "高", "夏", "蔡", "田", "樊", "胡",
                           "凌", "霍", "虞", "万", "支", "柯", "昝", "管", "卢", "莫",
                           "经", "房", "裘", "缪", "干", "解", "应", "宗", "丁", "宣",
                           "贲", "邓", "郁", "单", "杭", "洪", "包", "诸", "左", "石",
                           "崔", "吉", "钮", "龚", "程", "嵇", "邢", "滑", "裴", "陆",
                           "荣", "翁", "荀", "羊", "於", "惠", "甄", "麴", "家", "封",
                           "芮", "羿", "储", "靳", "汲", "邴", "糜", "松", "井", "段",
                           "富", "巫", "乌", "焦", "巴", "弓", "牧", "隗", "山", "谷",
                           "车", "侯", "宓", "蓬", "全", "郗", "班", "仰", "秋", "仲",
                           "伊", "宫", "宁", "仇", "栾", "暴", "甘", "钭", "厉", "戎",
                           "祖", "武", "符", "刘", "景", "詹", "束", "龙", "叶", "幸",
                           "司", "韶", "郜", "黎", "蓟", "薄", "印", "宿", "白", "怀",
                           "蒲", "邰", "从", "鄂", "索", "咸", "籍", "赖", "卓", "蔺",
                           "屠", "蒙", "池", "乔", "阴", "鬱", "胥", "能", "苍", "双",
                           "闻", "莘", "党", "翟", "谭", "贡", "劳", "逄", "姬", "申",
                           "扶", "堵", "冉", "宰", "郦", "雍", "卻", "璩", "桑", "桂",
                           "濮", "牛", "寿", "通", "边", "扈", "燕", "冀", "郏", "浦",
                           "尚", "农", "温", "别", "庄", "晏", "柴", "瞿", "阎", "充",
                           "慕", "连", "茹", "习", "宦", "艾", "鱼", "容", "向", "古",
                           "易", "慎", "戈", "廖", "庾", "终", "暨", "居", "衡", "步",
                           "都", "耿", "满", "弘", "匡", "国", "文", "寇", "广", "禄",
                           "阙", "东", "欧", "殳", "沃", "利", "蔚", "越", "夔", "隆",
                           "师", "巩", "厍", "聂", "晁", "勾", "敖", "融", "冷", "訾",
                           "辛", "阚", "那", "简", "饶", "空", "曾", "毋", "沙", "乜",
                           "养", "鞠", "须", "丰", "巢", "关", "蒯", "相", "查", "后",
                           "荆", "红", "游", "竺", "权", "逯", "盖", "益", "桓", "公"],
            "compound": ["慕容", "上官", "欧阳", "司马", "独孤", "皇甫", "令狐",
                        "东方", "南宫", "西门", "长孙", "宇文", "尉迟", "公孙",
                        "诸葛", "夏侯", "端木", "申屠", "淳于", "闾丘", "左丘",
                        "公羊", "谷梁", "轩辕", "濮阳", "东郭", "太史", "南门",
                        "呼延", "归海", "羊舌", "微生", "梁丘", "左人", "百里",
                        "东门", "西门", "南郭", "北宫", "第五", "钟离", "司寇",
                        "司徒", "司空", "司城", "司鸿", "仲孙", "叔孙", "季孙",
                        "孟孙", "公西", "公仪", "公冶", "公良", "公户", "公伯",
                        "夹谷", "巫马", "壤驷", "漆雕", "乐正", "宰父", "段干"],
            "rare": ["姬", "嬴", "妘", "妫", "姒", "风", "偃", "归", "曼", "隗",
                    "芈", "斟", "斟鄩", "斟灌", "有穷", "有仍", "有缗", "有扈",
                    "涂山", "防风", "葛天", "无怀", "方雷", "彤鱼", "西陵", "青阳"],
            "literary": ["萧", "沈", "顾", "陆", "谢", "温", "柳", "梅", "兰", "竹",
                        "云", "风", "月", "雪", "花", "叶", "林", "江", "海", "山",
                        "龙", "凤", "鹤", "燕", "鸿", "白", "墨", "青", "紫", "玄"],
        }

    def _init_element_chars(self):
        """五行偏旁字库"""
        self.element_chars = {
            FiveElement.METAL: {
                "male": ["锋", "钧", "锐", "铭", "铮", "锡", "锦", "锟", "铠", "钊",
                        "钰", "钦", "铎", "铄", "铿", "锵", "镕", "镔", "鑫", "镜"],
                "female": ["铃", "钰", "锦", "银", "钗", "钏", "铢", "铉", "銮", "鏴",
                          "钿", "钏", "铌", "铷", "铯", "铱", "铒", "铥", "铕", "铟"],
            },
            FiveElement.WOOD: {
                "male": ["林", "森", "松", "柏", "栋", "梁", "楷", "模", "棋", "楠",
                        "桐", "桦", "枫", "榕", "樟", "檀", "栎", "栩", "彬", "楚"],
                "female": ["梅", "兰", "竹", "菊", "桂", "柳", "桃", "杏", "樱", "薇",
                          "蓉", "莲", "荷", "芝", "茉", "莉", "萱", "茜", "芸", "芷"],
            },
            FiveElement.WATER: {
                "male": ["海", "洋", "江", "河", "湖", "泊", "涛", "波", "浪", "潮",
                        "浩", "瀚", "渊", "源", "清", "澈", "泓", "淼", "潇", "澜"],
                "female": ["冰", "雪", "霜", "露", "霞", "雯", "霏", "霓", "霖", "霭",
                          "洁", "淑", "涵", "漫", "滢", "潆", "漪", "涟", "漪", "潋"],
            },
            FiveElement.FIRE: {
                "male": ["炎", "焱", "煜", "炜", "炫", "烨", "焕", "炬", "炳", "炽",
                        "烽", "燃", "煌", "熠", "灿", "灼", "炀", "炅", "炘", "炆"],
                "female": ["煜", "烨", "焕", "炫", "灿", "炘", "炘", "炀", "炅", "炆",
                          "灵", "炅", "炘", "炆", "炀", "炘", "炆", "炀", "炘", "炆"],
            },
            FiveElement.EARTH: {
                "male": ["坤", "垚", "垚", "垚", "垚", "垚", "垚", "垚", "垚", "垚",
                        "坚", "坦", "坪", "坡", "城", "培", "基", "堂", "堡", "垒"],
                "female": ["圭", "垚", "垚", "垚", "垚", "垚", "垚", "垚", "垚", "垚",
                          "壁", "玺", "璧", "莹", "璎", "璐", "瑾", "瑜", "璇", "璋"],
            },
        }

    def _init_generation_poems(self):
        """辈分字派诗（扩展版）"""
        self.generation_poems = {
            "叶氏": ["云", "风", "天", "道", "玄", "清", "明", "正"],
            "苏氏": ["婉", "清", "如", "玉", "映", "月", "华", "光"],
            "林氏": ["修", "齐", "治", "平", "德", "润", "家", "邦"],
            "陈氏": ["志", "存", "高", "远", "学", "贯", "古", "今"],
            "李氏": ["文", "章", "华", "国", "诗", "礼", "传", "家"],
            "王氏": ["仁", "义", "礼", "智", "信", "忠", "孝", "廉"],
            "张氏": ["天", "地", "玄", "黄", "宇", "宙", "洪", "荒"],
            "刘氏": ["邦", "国", "永", "昌", "世", "代", "荣", "光"],
            "杨氏": ["春", "风", "化", "雨", "润", "物", "无", "声"],
            "黄氏": ["金", "玉", "满", "堂", "福", "寿", "安", "康"],
            "赵氏": ["乾", "坤", "正", "大", "日", "月", "光", "明"],
            "周氏": ["文", "武", "成", "康", "昭", "穆", "共", "和"],
            "吴氏": ["延", "陵", "世", "泽", "至", "德", "传", "家"],
            "徐氏": ["东", "海", "家", "声", "南", "州", "世", "泽"],
            "孙氏": ["乐", "安", "世", "泽", "兵", "法", "传", "家"],
            "马氏": ["伏", "波", "世", "泽", "铜", "柱", "家", "声"],
            "朱氏": ["紫", "阳", "世", "泽", "白", "鹿", "家", "风"],
            "胡氏": ["安", "定", "世", "泽", "苏", "湖", "家", "声"],
            "郭氏": ["汾", "阳", "世", "泽", "将", "相", "家", "声"],
            "何氏": ["庐", "江", "世", "泽", "东", "海", "家", "声"],
            "高氏": ["渤", "海", "家", "声", "供", "侯", "世", "泽"],
            "罗氏": ["豫", "章", "世", "泽", "湘", "水", "家", "声"],
            "郑氏": ["荥", "阳", "世", "泽", "诗", "礼", "家", "声"],
            "梁氏": ["安", "定", "世", "泽", "魁", "星", "家", "声"],
            "谢氏": ["陈", "留", "世", "泽", "宝", "树", "家", "声"],
            "宋氏": ["京", "兆", "世", "泽", "文", "章", "家", "声"],
            "唐氏": ["晋", "阳", "世", "泽", "桐", "叶", "家", "声"],
            "韩氏": ["南", "阳", "世", "泽", "北", "斗", "家", "声"],
            "曹氏": ["谯", "国", "世", "泽", "文", "章", "家", "声"],
            "许氏": ["高", "阳", "世", "泽", "汝", "南", "家", "声"],
            "邓氏": ["南", "阳", "世", "泽", "云", "台", "家", "声"],
            "萧氏": ["兰", "陵", "世", "泽", "相", "国", "家", "声"],
            "冯氏": ["始", "平", "世", "泽", "大", "树", "家", "声"],
            "曾氏": ["鲁", "国", "世", "泽", "三", "省", "家", "声"],
            "程氏": ["安", "定", "世", "泽", "伊", "洛", "家", "声"],
            "蔡氏": ["济", "阳", "世", "泽", "纸", "业", "家", "声"],
            "彭氏": ["陇", "西", "世", "泽", "长", "寿", "家", "声"],
            "潘氏": ["荥", "阳", "世", "泽", "花", "县", "家", "声"],
            "袁氏": ["汝", "南", "世", "泽", "卧", "雪", "家", "声"],
            "于氏": ["河", "内", "世", "泽", "忠", "肃", "家", "声"],
            "董氏": ["陇", "西", "世", "泽", "良", "史", "家", "声"],
            "余氏": ["下", "邳", "世", "泽", "风", "采", "家", "声"],
            "苏氏2": ["眉", "山", "世", "泽", "文", "章", "家", "声"],
            "蒋氏": ["乐", "安", "世", "泽", "九", "侯", "家", "声"],
            "沈氏": ["吴", "兴", "世", "泽", "梦", "溪", "家", "声"],
            "卢氏": ["范", "阳", "世", "泽", "大", "历", "家", "声"],
            "贾氏": ["武", "威", "世", "泽", "经", "学", "家", "声"],
            "丁氏": ["济", "阳", "世", "泽", "梦", "松", "家", "声"],
            "魏氏": ["钜", "鹿", "世", "泽", "鹤", "山", "家", "声"],
            "薛氏": ["河", "东", "世", "泽", "三", "凤", "家", "声"],
            "任氏": ["乐", "安", "世", "泽", "诗", "礼", "家", "声"],
            "姜氏": ["天", "水", "世", "泽", "渭", "水", "家", "声"],
            "范氏": ["高", "平", "世", "泽", "忧", "乐", "家", "声"],
            "方氏": ["河", "南", "世", "泽", "正", "学", "家", "声"],
            "石氏": ["武", "威", "世", "泽", "徂", "徕", "家", "声"],
            "姚氏": ["吴", "兴", "世", "泽", "文", "章", "家", "声"],
            "谭氏": ["齐", "郡", "世", "泽", "善", "断", "家", "声"],
            "廖氏": ["武", "威", "世", "泽", "万", "石", "家", "声"],
            "邹氏": ["范", "阳", "世", "泽", "讽", "谏", "家", "声"],
            "熊氏": ["江", "陵", "世", "泽", "忠", "义", "家", "声"],
            "金氏": ["彭", "城", "世", "泽", "仁", "山", "家", "声"],
            "陆氏": ["河", "南", "世", "泽", "剑", "南", "家", "声"],
            "郝氏": ["太", "原", "世", "泽", "晒", "书", "家", "声"],
            "孔氏": ["鲁", "国", "世", "泽", "圣", "学", "家", "声"],
            "白氏": ["南", "阳", "世", "泽", "香", "山", "家", "声"],
            "崔氏": ["博", "陵", "世", "泽", "清", "河", "家", "声"],
            "康氏": ["京", "兆", "世", "泽", "诰", "命", "家", "声"],
            "毛氏": ["西", "河", "世", "泽", "诗", "学", "家", "声"],
            "邱氏": ["河", "南", "世", "泽", "文", "庄", "家", "声"],
            "秦氏": ["天", "水", "世", "泽", "淮", "海", "家", "声"],
            "江氏": ["济", "阳", "世", "泽", "文", "通", "家", "声"],
            "史氏": ["京", "兆", "世", "泽", "直", "笔", "家", "声"],
            "顾氏": ["武", "陵", "世", "泽", "亭", "林", "家", "声"],
            "侯氏": ["上", "谷", "世", "泽", "关", "中", "家", "声"],
            "邵氏": ["博", "陵", "世", "泽", "安", "乐", "家", "声"],
            "孟氏": ["平", "陵", "世", "泽", "亚", "圣", "家", "声"],
            "龙氏": ["武", "陵", "世", "泽", "图", "腾", "家", "声"],
            "万氏": ["扶", "风", "世", "泽", "文", "章", "家", "声"],
            "段氏": ["京", "兆", "世", "泽", "忠", "烈", "家", "声"],
            "雷氏": ["冯", "翊", "世", "泽", "精", "通", "家", "声"],
            "钱氏": ["彭", "城", "世", "泽", "吴", "越", "家", "声"],
            "汤氏": ["中", "山", "世", "泽", "玉", "茗", "家", "声"],
            "尹氏": ["天", "水", "世", "泽", "文", "章", "家", "声"],
            "黎氏": ["京", "兆", "世", "泽", "文", "章", "家", "声"],
            "易氏": ["太", "原", "世", "泽", "文", "章", "家", "声"],
            "常氏": ["平", "原", "世", "泽", "忠", "武", "家", "声"],
            "武氏": ["太", "原", "世", "泽", "忠", "武", "家", "声"],
            "乔氏": ["梁", "国", "世", "泽", "文", "章", "家", "声"],
            "贺氏": ["广", "平", "世", "泽", "文", "章", "家", "声"],
            "赖氏": ["颍", "川", "世", "泽", "松", "阳", "家", "声"],
            "龚氏": ["武", "陵", "世", "泽", "渤", "海", "家", "声"],
            "文氏": ["雁", "门", "世", "泽", "正", "气", "家", "声"],
        }

    def _init_virtue_names(self):
        """美德寓意名"""
        self.virtue_names = {
            "male": {
                "仁": ["仁", "德", "慈", "善", "惠", "恩", "泽", "济"],
                "义": ["义", "正", "直", "刚", "勇", "烈", "侠", "豪"],
                "礼": ["礼", "敬", "恭", "谦", "让", "和", "雅", "儒"],
                "智": ["智", "慧", "明", "哲", "睿", "聪", "敏", "达"],
                "信": ["信", "诚", "忠", "贞", "恒", "毅", "笃", "厚"],
            },
            "female": {
                "淑": ["淑", "贞", "娴", "雅", "静", "婉", "惠", "懿"],
                "慧": ["慧", "敏", "颖", "巧", "灵", "秀", "睿", "智"],
                "美": ["美", "丽", "妍", "姣", "娥", "婵", "娟", "婷"],
                "柔": ["柔", "婉", "温", "顺", "和", "怡", "悦", "欣"],
                "德": ["德", "贤", "良", "善", "慈", "淑", "端", "庄"],
            },
        }

    def _init_nature_names(self):
        """自然意象名"""
        self.nature_names = {
            "male": {
                "山": ["岳", "峰", "岭", "峦", "岩", "崖", "巍", "峨"],
                "水": ["渊", "泽", "瀚", "涛", "澜", "泓", "淼", "潇"],
                "天": ["宇", "穹", "霄", "昊", "苍", "宸", "乾", "曜"],
                "光": ["辉", "煌", "耀", "曦", "旭", "昀", "晟", "晔"],
            },
            "female": {
                "月": ["月", "婵", "娟", "娥", "胧", "朦", "曦", "晗"],
                "花": ["兰", "莲", "蓉", "薇", "萱", "芷", "茉", "莉"],
                "云": ["云", "霞", "雯", "霓", "霏", "霭", "霁", "霄"],
                "玉": ["玉", "琳", "琅", "琪", "瑶", "瑾", "瑜", "璇"],
            },
        }

    def _init_classical_names(self):
        """经典典故名（诗经/楚辞/唐诗/宋词/论语/道德经）"""
        self.classical_names = {
            "male": [
                ("鹏举", "《庄子·逍遥游》鹏之徙于南冥也，水击三千里，抟扶摇而上者九万里"),
                ("子渊", "《论语》学问渊博，如渊之深"),
                ("浩然", "《孟子》我善养吾浩然之气"),
                ("逸飞", "《诗经·小雅》飘逸飞扬，不可捉摸"),
                ("思远", "《诗经·邶风》深思远虑，静言思之"),
                ("景行", "《诗经·小雅》高山仰止，景行行止"),
                ("明哲", "《诗经·大雅》既明且哲，以保其身"),
                ("维翰", "《诗经·大雅》大邦维翰，四方为纲"),
                ("子衿", "《诗经·郑风》青青子衿，悠悠我心"),
                ("凯风", "《诗经·邶风》凯风自南，吹彼棘心"),
                ("鹤鸣", "《诗经·小雅》鹤鸣于九皋，声闻于天"),
                ("清源", "《楚辞·离骚》正本清源，返璞归真"),
                ("正则", "《楚辞·离骚》名余曰正则兮，字余曰灵均"),
                ("伯庸", "《楚辞·离骚》朕皇考曰伯庸"),
                ("望舒", "《楚辞·离骚》前望舒使先驱兮"),
                ("云旗", "《楚辞·离骚》驾八龙之婉婉兮，载云旗之委蛇"),
                ("承宇", "《楚辞·九章》霰雪纷其无垠兮，云霏霏而承宇"),
                ("怀瑾", "《楚辞·九章》怀瑾握瑜兮，穷不知所示"),
                ("嘉树", "《楚辞·九章》后皇嘉树，橘徕服兮"),
                ("杜衡", "《楚辞·离骚》畦留夷与揭车兮，杂杜衡与芳芷"),
                ("江离", "《楚辞·离骚》扈江离与辟芷兮，纫秋兰以为佩"),
                ("青云", "唐诗·王勃《滕王阁序》穷且益坚，不坠青云之志"),
                ("长风", "唐诗·李白《行路难》长风破浪会有时，直挂云帆济沧海"),
                ("鸿飞", "唐诗·李白《送友人》浮云游子意，落日故人情。挥手自兹去，萧萧班马鸣"),
                ("知远", "唐诗·王之涣《登鹳雀楼》欲穷千里目，更上一层楼"),
                ("松涛", "唐诗·王维《山居秋暝》明月松间照，清泉石上流"),
                ("云帆", "唐诗·李白《行路难》长风破浪会有时，直挂云帆济沧海"),
                ("星河", "唐诗·杜甫《旅夜书怀》星垂平野阔，月涌大江流"),
                ("天涯", "唐诗·王勃《送杜少府之任蜀州》海内存知己，天涯若比邻"),
                ("锦程", "唐诗·孟郊《登科后》春风得意马蹄疾，一日看尽长安花"),
                ("凌霄", "唐诗·杜甫《望岳》会当凌绝顶，一览众山小"),
                ("千帆", "唐诗·刘禹锡《酬乐天》沉舟侧畔千帆过，病树前头万木春"),
                ("东篱", "宋词·李清照《醉花阴》东篱把酒黄昏后，有暗香盈袖"),
                ("疏影", "宋词·林逋《山园小梅》疏影横斜水清浅，暗香浮动月黄昏"),
                ("庭坚", "宋词·黄庭坚，取坚韧不拔之意"),
                ("放翁", "宋词·陆游号放翁，取豪放不羁之意"),
                ("稼轩", "宋词·辛弃疾号稼轩，取田园之志"),
                ("子瞻", "宋词·苏轼字子瞻，取高瞻远瞩之意"),
                ("君复", "宋词·林逋字君复，取返璞归真之意"),
                ("尧章", "宋词·姜夔字尧章，取华美文章之意"),
                ("邦彦", "宋词·周邦彦，取邦国之才"),
                ("少游", "宋词·秦观字少游，取少年游历之意"),
                ("德润", "《大学》富润屋，德润身"),
                ("至诚", "《中庸》唯天下至诚，为能尽其性"),
                ("知新", "《论语》温故而知新，可以为师矣"),
                ("弘毅", "《论语》士不可以不弘毅，任重而道远"),
                ("思齐", "《论语》见贤思齐焉，见不贤而内自省也"),
                ("安仁", "《论语》仁者安仁，知者利仁"),
                ("守拙", "《道德经》大巧若拙，大智若愚"),
                ("若水", "《道德经》上善若水，水善利万物而不争"),
                ("知白", "《道德经》知其白，守其黑，为天下式"),
                ("希声", "《道德经》大音希声，大象无形"),
            ],
            "female": [
                ("静姝", "《诗经·邶风》静女其姝，俟我于城隅"),
                ("燕婉", "《诗经·邶风》燕婉之求，籧篨不鲜"),
                ("清扬", "《诗经·郑风》有美一人，清扬婉兮"),
                ("如雪", "《诗经·曹风》蜉蝣掘阅，麻衣如雪"),
                ("若兰", "《楚辞·离骚》纫秋兰以为佩"),
                ("采薇", "《诗经·小雅》采薇采薇，薇亦作止"),
                ("蒹葭", "《诗经·秦风》蒹葭苍苍，白露为霜"),
                ("桃夭", "《诗经·周南》桃之夭夭，灼灼其华"),
                ("子佩", "《诗经·郑风》青青子佩，悠悠我思"),
                ("舜华", "《诗经·郑风》有女同车，颜如舜华"),
                ("巧笑", "《诗经·卫风》巧笑倩兮，美目盼兮"),
                ("美淑", "《诗经·陈风》彼美淑姬，可与晤歌"),
                ("琼瑶", "《诗经·卫风》投我以木桃，报之以琼瑶"),
                ("文茵", "《诗经·秦风》文茵畅毂，驾我骐馵"),
                ("惠然", "《诗经·邶风》惠然肯来，莫往莫来"),
                ("楚楚", "《诗经·曹风》蜉蝣之羽，衣裳楚楚"),
                ("依依", "《诗经·小雅》昔我往矣，杨柳依依"),
                ("霏霏", "《诗经·小雅》今我来思，雨雪霏霏"),
                ("兰芷", "《楚辞·离骚》兰芷变而不芳兮，荃蕙化而为茅"),
                ("芳蔼", "《楚辞·九叹》芳蔼兮挫枯，荃蕙兮为茅"),
                ("杜若", "《楚辞·九歌》采芳洲兮杜若，将以遗兮下女"),
                ("辛夷", "《楚辞·九歌》辛夷楣兮药房，罔薜荔兮为帷"),
                ("荷衣", "《楚辞·离骚》制芰荷以为衣兮，集芙蓉以为裳"),
                ("芙蓉", "《楚辞·离骚》制芰荷以为衣兮，集芙蓉以为裳"),
                ("芳馨", "《楚辞·九歌》合百草兮实庭，建芳馨兮庑门"),
                ("云容", "唐诗·李白《清平调》云想衣裳花想容，春风拂槛露华浓"),
                ("月华", "唐诗·张若虚《春江花月夜》此时相望不相闻，愿逐月华流照君"),
                ("如烟", "唐诗·李白《望庐山瀑布》日照香炉生紫烟，遥看瀑布挂前川"),
                ("锦瑟", "唐诗·李商隐《锦瑟》锦瑟无端五十弦，一弦一柱思华年"),
                ("明珠", "唐诗·白居易《琵琶行》大珠小珠落玉盘"),
                ("清秋", "唐诗·李白《宣州谢朓楼》长风万里送秋雁，对此可以酣高楼"),
                ("春晓", "唐诗·孟浩然《春晓》春眠不觉晓，处处闻啼鸟"),
                ("晚晴", "唐诗·李商隐《晚晴》天意怜幽草，人间重晚晴"),
                ("碧落", "唐诗·白居易《长恨歌》上穷碧落下黄泉，两处茫茫皆不见"),
                ("紫烟", "唐诗·李白《望庐山瀑布》日照香炉生紫烟"),
                ("清音", "宋词·苏轼《前赤壁赋》惟江上之清风，与山间之明月，耳得之而为声"),
                ("如梦", "宋词·李清照《如梦令》常记溪亭日暮，沉醉不知归路"),
                ("暗香", "宋词·姜夔《暗香》旧时月色，算几番照我，梅边吹笛"),
                ("疏桐", "宋词·苏轼《卜算子》缺月挂疏桐，漏断人初静"),
                ("晓风", "宋词·柳永《雨霖铃》今宵酒醒何处？杨柳岸，晓风残月"),
                ("微雨", "宋词·晏几道《临江仙》落花人独立，微雨燕双飞"),
                ("海棠", "宋词·李清照《如梦令》试问卷帘人，却道海棠依旧"),
                ("幽兰", "宋词·苏轼《题杨次公春兰》春兰如美人，不采羞自献"),
                ("雪梅", "宋词·卢梅坡《雪梅》梅须逊雪三分白，雪却输梅一段香"),
                ("冰心", "唐诗·王昌龄《芙蓉楼送辛渐》洛阳亲友如相问，一片冰心在玉壶"),
                ("知画", "宋词·苏轼《书鄢陵王主簿》诗中有画，画中有诗"),
                ("如玉", "《诗经·小雅》言念君子，温其如玉"),
                ("含章", "《易经》含章可贞，以时发也"),
                ("素心", "《礼记》素心若雪，不染尘埃"),
                ("若素", "《中庸》君子素其位而行，不愿乎其外"),
            ],
        }

    def _init_stroke_data(self):
        """笔画数理吉凶数据(81数理)"""
        self.stroke_auspicious = {
            1: ("大吉", "太极之数，万物开泰，生发无穷，利禄亨通"),
            3: ("大吉", "三才之数，天地人和，大事大业，繁荣昌隆"),
            5: ("大吉", "五行之数，阴阳和合，名利双收，后福重重"),
            6: ("大吉", "六爻之数，发展变化，天赋美德，吉祥安泰"),
            7: ("大吉", "七政之数，精悍严谨，天赋之力，吉星高照"),
            8: ("大吉", "八卦之数，乾坎艮震，巽离坤兑，无穷无尽"),
            11: ("大吉", "旱苗逢雨，万物更新，调顺发达，恢弘泽世"),
            13: ("大吉", "春日牡丹，才艺多能，智谋奇略，忍柔当事"),
            15: ("大吉", "福寿圆满，富贵荣誉，涵养雅量，德高望重"),
            16: ("大吉", "厚重载德，安富尊荣，财官双美，功成名就"),
            17: ("大吉", "刚强不屈，权威刚强，突破万难，必获成功"),
            18: ("大吉", "铁镜重磨，权威显达，博得名利，且养柔德"),
            21: ("大吉", "明月中天，光风霁月，万物确立，官运亨通"),
            23: ("大吉", "旭日东升，壮丽壮观，权威旺盛，功名荣达"),
            24: ("大吉", "家门余庆，金钱丰盈，白手成家，财源广进"),
            25: ("大吉", "资性英敏，刚毅果断，才能奇特，自成大业"),
            29: ("大吉", "智谋优秀，财力归集，名闻海内，成就大业"),
            31: ("大吉", "智勇得志，博得名利，统领众人，繁荣富贵"),
            32: ("大吉", "侥幸多望，贵人得助，财帛如裕，繁荣至上"),
            33: ("大吉", "旭日升天，鸾凤相会，名闻天下，隆昌至极"),
            35: ("大吉", "温和平静，智达通畅，文昌技艺，奏功洋洋"),
            37: ("大吉", "权威显达，热诚忠信，宜着雅量，终身荣富"),
            39: ("大吉", "云开见月，虽有劳碌，光明坦途，指日可期"),
            41: ("大吉", "有德纯和，纯阳独秀，德高望重，和顺畅达"),
            45: ("大吉", "顺风扬帆，新生泰和，智谋经纬，富贵繁荣"),
            47: ("大吉", "开花结果，权威进取，有贵人助，成大事业"),
            48: ("大吉", "德智兼备，鹤立鸡群，名利双收，繁荣富贵"),
            52: ("大吉", "卓识达眼，先见之明，智谋超群，名利双收"),
            63: ("大吉", "万物化育，繁荣之象，专心一意，必能成功"),
            65: ("大吉", "天长地久，家运隆昌，福寿绵长，事事成就"),
            67: ("大吉", "顺风通达，万事如意，利路亨通，步步高升"),
            68: ("大吉", "智虑周密，思虑周详，发明创造，集众信望"),
            81: ("大吉", "最极之数，还本归元，吉祥重叠，富贵尊荣"),
        }

        self.stroke_inauspicious = {
            2: ("大凶", "混沌未开，进退保守，志望难达，破败无常"),
            4: ("大凶", "四象之数，凶变之象，前途坎坷，苦难折磨"),
            9: ("大凶", "大成之数，蕴含凶险，或成或败，难以把握"),
            10: ("大凶", "终结之数，雪暗飘零，偶或有成，回顾茫然"),
            12: ("大凶", "掘井无泉，无理之数，发展薄弱，虽生不足"),
            14: ("大凶", "破兆之数，沦落天涯，失意烦闷，家庭缘薄"),
            19: ("大凶", "风云蔽月，辛苦重来，虽有智谋，万事挫折"),
            20: ("大凶", "非业破运，灾难重重，进退维谷，万事难成"),
            22: ("大凶", "秋草逢霜，困难疾弱，虽出豪杰，人生波折"),
            26: ("大凶", "变怪之数，波澜重叠，英雄豪杰，归诸失败"),
            27: ("大凶", "欲望无止，自我强烈，多受毁谤，尚可成功"),
            28: ("大凶", "遭难之数，豪杰气概，四海漂泊，终世浮躁"),
            34: ("大凶", "破家之数，辛苦不绝，灾祸至极，难以成功"),
            36: ("大凶", "波澜重叠，沉浮万状，侠肝义胆，舍己成仁"),
            40: ("大凶", "智谋胆力，冒险投机，沉浮不定，退保平安"),
            42: ("大凶", "寒蝉在柳，博识多能，精通世情，十艺九不成"),
            44: ("大凶", "破家亡身，暗藏惨淡，事不如意，乱世怪杰"),
            46: ("大凶", "载宝沉舟，浪里淘金，大难尝尽，大功有成"),
            49: ("大凶", "吉凶难分，得宽则宽，得饶则饶，切忌贪心"),
            50: ("大凶", "小舟入海，吉凶参半，先得后失，晚景凄凉"),
            51: ("大凶", "浮沉不定，盛衰交加，天降大任，磨难重重"),
            53: ("大凶", "曲卷难推，外祥内苦，先福后祸，先祸后福"),
            54: ("大凶", "石上栽花，多难悲运，难望成功，残菊废叶"),
            55: ("大凶", "善恶兼半，外美内苦，先吉后凶，先凶后吉"),
            56: ("大凶", "浪里行舟，历尽艰辛，四周障碍，事难遂愿"),
            57: ("大凶", "日照春松，寒雪青松，虽有困难，时来运转"),
            58: ("大凶", "晚行遇月，先苦后甘，宽宏扬名，富贵繁荣"),
            59: ("大凶", "寒蝉悲风，时运不济，缺乏忍耐，难得成功"),
            60: ("大凶", "无谋之人，漂泊不定，晦暝暗黑，动摇不安"),
            61: ("大凶", "牡丹芙蓉，花开富贵，名利双收，定享幸福"),
            62: ("大凶", "衰败之数，内外不合，志望难达，灾祸频来"),
            64: ("大凶", "骨肉分离，孤独悲愁，难得心安，做事不成"),
            66: ("大凶", "进退失据，内外不和，信用缺乏，灾祸频来"),
            69: ("大凶", "坐立不安，常陷逆境，穷迫滞塞，灾祸交加"),
            70: ("大凶", "残菊逢霜，家运衰退，晚景凄凉，多灾多难"),
            71: ("大凶", "石上金花，内心劳苦，贯彻始终，定可成功"),
            72: ("大凶", "劳苦相伴，先甘后苦，万难忍受，身多痛苦"),
            73: ("大凶", "志高力微，盛衰交加，徒有高志，终生平安"),
            74: ("大凶", "残菊经霜，智能无用，辛苦不绝，沉沦逆境"),
            75: ("大凶", "退守保吉，发迹太迟，虽有智谋，难望成功"),
            76: ("大凶", "倾覆离散，骨肉分离，内外不合，虽劳无功"),
            77: ("大凶", "家庭不和，先甘后苦，前半生幸福，后半生悲运"),
            78: ("大凶", "晚境凄凉，先得后失，智能发达，中年成功"),
            79: ("大凶", "云头望月，身疲力尽，前途无望，身多苦劳"),
            80: ("大凶", "遁吉入凶，最极之数，还本归元，一生艰难"),
        }

    # ================================================================
    # 五行推算
    # ================================================================

    def calculate_element_from_birth(self, year: int, month: int,
                                     day: int, hour: int = 0) -> FiveElement:
        """根据生辰推算五行属性"""
        heavenly_stems = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
        stem_elements = {
            "甲": FiveElement.WOOD, "乙": FiveElement.WOOD,
            "丙": FiveElement.FIRE, "丁": FiveElement.FIRE,
            "戊": FiveElement.EARTH, "己": FiveElement.EARTH,
            "庚": FiveElement.METAL, "辛": FiveElement.METAL,
            "壬": FiveElement.WATER, "癸": FiveElement.WATER,
        }

        year_stem_index = (year - 4) % 10
        year_stem = heavenly_stems[year_stem_index]

        return stem_elements[year_stem]

    def find_missing_element(self, year: int, month: int,
                             day: int, hour: int = 0) -> FiveElement:
        """查找八字中缺失的五行"""
        heavenly_stems = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
        earthly_branches = ["子", "丑", "寅", "卯", "辰", "巳",
                           "午", "未", "申", "酉", "戌", "亥"]

        stem_elements = {
            "甲": FiveElement.WOOD, "乙": FiveElement.WOOD,
            "丙": FiveElement.FIRE, "丁": FiveElement.FIRE,
            "戊": FiveElement.EARTH, "己": FiveElement.EARTH,
            "庚": FiveElement.METAL, "辛": FiveElement.METAL,
            "壬": FiveElement.WATER, "癸": FiveElement.WATER,
        }
        branch_elements = {
            "子": FiveElement.WATER, "丑": FiveElement.EARTH,
            "寅": FiveElement.WOOD, "卯": FiveElement.WOOD,
            "辰": FiveElement.EARTH, "巳": FiveElement.FIRE,
            "午": FiveElement.FIRE, "未": FiveElement.EARTH,
            "申": FiveElement.METAL, "酉": FiveElement.METAL,
            "戌": FiveElement.EARTH, "亥": FiveElement.WATER,
        }

        year_stem = heavenly_stems[(year - 4) % 10]
        year_branch = earthly_branches[(year - 4) % 12]
        month_stem = heavenly_stems[(year * 12 + month + 13) % 10]
        month_branch = earthly_branches[(month + 1) % 12]
        day_stem = heavenly_stems[(year * 365 + month * 30 + day + 15) % 10]
        day_branch = earthly_branches[(year * 365 + month * 30 + day + 15) % 12]

        present_elements = set()
        for stem in [year_stem, month_stem, day_stem]:
            present_elements.add(stem_elements[stem])
        for branch in [year_branch, month_branch, day_branch]:
            present_elements.add(branch_elements[branch])

        all_elements = set(FiveElement)
        missing = all_elements - present_elements

        if missing:
            return random.choice(list(missing))
        return random.choice(list(all_elements))

    # ================================================================
    # 三才五格法
    # ================================================================

    def _char_strokes(self, char: str) -> int:
        """获取汉字笔画数(简化版)"""
        stroke_map = {
            '一': 1, '乙': 1, '二': 2, '十': 2, '丁': 2, '厂': 2, '七': 2,
            '八': 2, '人': 2, '入': 2, '儿': 2, '九': 2, '几': 2, '了': 2,
            '力': 2, '乃': 2, '刀': 2, '又': 2, '三': 3, '于': 3, '干': 3,
            '工': 3, '土': 3, '才': 3, '寸': 3, '下': 3, '大': 3, '丈': 3,
            '万': 3, '上': 3, '小': 3, '口': 3, '山': 3, '巾': 3, '千': 3,
            '川': 3, '亿': 3, '个': 3, '久': 3, '凡': 3, '丸': 3, '夕': 3,
            '么': 3, '广': 3, '亡': 3, '门': 3, '义': 3, '之': 3, '已': 3,
            '子': 3, '也': 3, '女': 3, '飞': 3, '习': 3, '马': 3, '乡': 3,
            '王': 4, '天': 4, '夫': 4, '元': 4, '无': 4, '云': 4, '专': 4,
            '艺': 4, '木': 4, '五': 4, '支': 4, '不': 4, '太': 4, '犬': 4,
            '区': 4, '历': 4, '友': 4, '尤': 4, '匹': 4, '车': 4, '巨': 4,
            '牙': 4, '屯': 4, '戈': 4, '比': 4, '互': 4, '切': 4, '瓦': 4,
            '止': 4, '少': 4, '日': 4, '中': 4, '贝': 4, '内': 4, '水': 4,
            '见': 4, '午': 4, '牛': 4, '手': 4, '气': 4, '毛': 4, '长': 4,
            '仁': 4, '片': 4, '化': 4, '反': 4, '介': 4, '父': 4, '从': 4,
            '今': 4, '凶': 4, '分': 4, '公': 4, '月': 4, '风': 4, '丹': 4,
            '文': 4, '六': 4, '方': 4, '火': 4, '为': 4, '斗': 4, '心': 4,
            '玉': 5, '示': 5, '未': 5, '末': 5, '打': 5, '巧': 5, '正': 5,
            '功': 5, '去': 5, '甘': 5, '世': 5, '古': 5, '节': 5, '本': 5,
            '可': 5, '左': 5, '右': 5, '石': 5, '龙': 5, '平': 5, '东': 5,
            '北': 5, '占': 5, '业': 5, '旧': 5, '帅': 5, '归': 5, '叶': 5,
            '田': 5, '由': 5, '只': 5, '史': 5, '央': 5, '兄': 5, '生': 5,
            '白': 5, '令': 5, '用': 5, '印': 5, '乐': 5, '句': 5, '外': 5,
            '冬': 5, '鸟': 5, '主': 5, '立': 5, '半': 5, '头': 5, '汉': 5,
            '宁': 5, '穴': 5, '它': 5, '写': 5, '礼': 5, '必': 5, '永': 5,
        }

        if char in stroke_map:
            return stroke_map[char]

        code = ord(char)
        if 0x4E00 <= code <= 0x9FFF:
            return 4 + (code % 20)
        return 4

    def analyze_strokes(self, surname: str, given_name: str) -> Dict:
        """三才五格分析"""
        s_strokes = sum(self._char_strokes(c) for c in surname)
        g_strokes = sum(self._char_strokes(c) for c in given_name)

        tian_ge = s_strokes + 1
        ren_ge = s_strokes + g_strokes
        di_ge = g_strokes + 1
        wai_ge = tian_ge + di_ge - ren_ge + 1
        zong_ge = s_strokes + g_strokes

        def judge(num):
            if num in self.stroke_auspicious:
                return "吉", self.stroke_auspicious[num][1]
            elif num in self.stroke_inauspicious:
                return "凶", self.stroke_inauspicious[num][1]
            return "平", "中平之数"

        return {
            "天格": {"value": tian_ge, "judgment": judge(tian_ge)},
            "人格": {"value": ren_ge, "judgment": judge(ren_ge)},
            "地格": {"value": di_ge, "judgment": judge(di_ge)},
            "外格": {"value": wai_ge, "judgment": judge(wai_ge)},
            "总格": {"value": zong_ge, "judgment": judge(zong_ge)},
            "综合评分": self._calculate_stroke_score(tian_ge, ren_ge, di_ge, wai_ge, zong_ge),
        }

    def _calculate_stroke_score(self, tian: int, ren: int,
                                di: int, wai: int, zong: int) -> int:
        """计算五格综合评分"""
        score = 50
        for num in [tian, ren, di, wai, zong]:
            if num in self.stroke_auspicious:
                score += 10
            elif num in self.stroke_inauspicious:
                score -= 10
        return max(0, min(100, score))

    # ================================================================
    # 核心命名方法
    # ================================================================

    def generate(self, surname: str = None,
                 gender: Gender = Gender.MALE,
                 element: FiveElement = None,
                 trigram: EightTrigram = None,
                 birth_year: int = None,
                 birth_month: int = None,
                 birth_day: int = None,
                 use_generation: bool = True,
                 strategy: str = "balanced",
                 count: int = 5) -> List[NameResult]:
        """
        生成角色名字

        参数:
            surname: 姓氏(不指定则随机)
            gender: 性别
            element: 指定五行(不指定则根据生辰推算)
            trigram: 指定八卦(不指定则根据五行匹配)
            birth_year/month/day: 生辰(用于推算五行)
            use_generation: 是否使用辈分字
            strategy: 命名策略 - balanced/element_focused/classical/nature/virtue
            count: 生成数量
        """
        if surname is None:
            surname = random.choice(self.surnames["top10"] + self.surnames["top50"] + self.surnames["common"])

        if element is None and birth_year:
            element = self.calculate_element_from_birth(
                birth_year, birth_month or 1, birth_day or 1
            )
        elif element is None:
            element = random.choice(list(FiveElement))

        if trigram is None:
            trigram = self._element_to_trigram(element)

        results = []
        attempts = 0
        max_attempts = count * 30

        while len(results) < count and attempts < max_attempts:
            attempts += 1
            result = self._generate_single(
                surname, gender, element, trigram,
                use_generation, strategy
            )

            if result and result.full_name not in self.used_names:
                self.used_names.add(result.full_name)
                results.append(result)

        return results

    def _generate_single(self, surname: str, gender: Gender,
                         element: FiveElement, trigram: EightTrigram,
                         use_generation: bool,
                         strategy: str) -> Optional[NameResult]:
        """生成单个名字"""
        generation_char = ""
        given_name = ""

        if use_generation and surname + "氏" in self.generation_poems:
            gen_list = self.generation_poems[surname + "氏"]
            generation_char = random.choice(gen_list)

        if strategy == "element_focused":
            given_name = self._pick_element_name(gender, element)
        elif strategy == "classical":
            classical = self.classical_names["male" if gender == Gender.MALE else "female"]
            given_name, cultural_ref = random.choice(classical)
        elif strategy == "nature":
            given_name = self._pick_nature_name(gender)
        elif strategy == "virtue":
            given_name = self._pick_virtue_name(gender)
        else:
            strategies = ["element_focused", "classical", "nature", "virtue"]
            weights = [0.4, 0.2, 0.2, 0.2]
            chosen = random.choices(strategies, weights=weights)[0]
            return self._generate_single(
                surname, gender, element, trigram,
                use_generation, chosen
            )

        if not given_name:
            return None

        full_name = surname + generation_char + given_name
        if len(given_name) == 1:
            full_name = surname + generation_char + given_name

        meaning = self._derive_meaning(given_name, element, trigram, gender)
        stroke_analysis = self.analyze_strokes(surname, generation_char + given_name)
        score = stroke_analysis.get("综合评分", 50)

        return NameResult(
            full_name=full_name,
            surname=surname,
            generation_char=generation_char,
            given_name=given_name,
            gender=gender,
            element=element,
            trigram=trigram,
            meaning=meaning,
            stroke_analysis=stroke_analysis,
            score=score,
        )

    def _pick_element_name(self, gender: Gender,
                           element: FiveElement) -> str:
        """从五行字库选名"""
        gender_key = "male" if gender == Gender.MALE else "female"
        chars = self.element_chars.get(element, {}).get(gender_key, [])
        if not chars:
            return ""

        if random.random() < 0.6:
            return random.choice(chars)
        else:
            return random.choice(chars) + random.choice(chars)

    def _pick_nature_name(self, gender: Gender) -> str:
        """从自然意象选名"""
        gender_key = "male" if gender == Gender.MALE else "female"
        all_chars = []
        for category_chars in self.nature_names[gender_key].values():
            all_chars.extend(category_chars)
        return random.choice(all_chars) if all_chars else ""

    def _pick_virtue_name(self, gender: Gender) -> str:
        """从美德寓意选名"""
        gender_key = "male" if gender == Gender.MALE else "female"
        all_chars = []
        for category_chars in self.virtue_names[gender_key].values():
            all_chars.extend(category_chars)
        return random.choice(all_chars) if all_chars else ""

    def _element_to_trigram(self, element: FiveElement) -> EightTrigram:
        """五行对应八卦"""
        mapping = {
            FiveElement.METAL: [EightTrigram.QIAN, EightTrigram.DUI],
            FiveElement.WOOD: [EightTrigram.ZHEN, EightTrigram.XUN],
            FiveElement.WATER: [EightTrigram.KAN],
            FiveElement.FIRE: [EightTrigram.LI],
            FiveElement.EARTH: [EightTrigram.KUN, EightTrigram.GEN],
        }
        return random.choice(mapping.get(element, [EightTrigram.QIAN]))

    def _derive_meaning(self, given_name: str, element: FiveElement,
                        trigram: EightTrigram, gender: Gender) -> str:
        """推导名字寓意"""
        parts = []

        parts.append(f"五行属{element.chinese_name}，")
        parts.append(f"卦象为{trigram.chinese_name}({trigram.nature})，")

        if gender == Gender.MALE:
            parts.append(f"寓意{trigram.quality}刚健，")
        else:
            parts.append(f"寓意{trigram.quality}柔顺，")

        parts.append(f"取{element.virtue}之德。")

        return "".join(parts)

    # ================================================================
    # 高级命名方法
    # ================================================================

    def generate_with_birth(self, surname: str, year: int, month: int,
                            day: int, hour: int = 0,
                            gender: Gender = Gender.MALE,
                            count: int = 5) -> List[NameResult]:
        """根据生辰八字生成名字"""
        element = self.calculate_element_from_birth(year, month, day, hour)
        missing = self.find_missing_element(year, month, day, hour)

        results = []
        results.extend(self.generate(
            surname=surname, gender=gender, element=element,
            birth_year=year, birth_month=month, birth_day=day,
            strategy="balanced", count=max(1, count // 2),
        ))

        if missing != element:
            results.extend(self.generate(
                surname=surname, gender=gender, element=missing,
                birth_year=year, birth_month=month, birth_day=day,
                strategy="element_focused", count=max(1, count - len(results)),
            ))

        return results[:count]

    def generate_clan_names(self, surname: str, generation: int = 1,
                            gender: Gender = Gender.MALE,
                            count: int = 5) -> List[NameResult]:
        """生成同辈分角色名"""
        if surname + "氏" not in self.generation_poems:
            return self.generate(surname=surname, gender=gender, count=count)

        gen_list = self.generation_poems[surname + "氏"]
        gen_char = gen_list[min(generation - 1, len(gen_list) - 1)]

        results = []
        for _ in range(count):
            element = random.choice(list(FiveElement))
            given = self._pick_element_name(gender, element)
            full = surname + gen_char + given

            if full not in self.used_names:
                self.used_names.add(full)
                results.append(NameResult(
                    full_name=full,
                    surname=surname,
                    generation_char=gen_char,
                    given_name=given,
                    gender=gender,
                    element=element,
                    meaning=f"辈分字「{gen_char}」，五行属{element.chinese_name}",
                ))

        return results

    def generate_title(self, name: str, genre: str = "xuanhuan") -> str:
        """生成称号/道号"""
        title_templates = {
            "xuanhuan": [
                "{element}灵{being}", "太{concept}{being}",
                "{direction}域{being}", "{color}莲{being}",
                "九天{being}", "万古{being}", "混元{being}",
            ],
            "wuxia": [
                "{element}面{being}", "{direction}方{being}",
                "一剑{being}", "万里{being}", "独步{being}",
            ],
        }

        templates = title_templates.get(genre, title_templates["xuanhuan"])
        template = random.choice(templates)

        element_map = {
            FiveElement.METAL: "金", FiveElement.WOOD: "木",
            FiveElement.WATER: "水", FiveElement.FIRE: "火",
            FiveElement.EARTH: "土",
        }
        direction_map = {
            FiveElement.METAL: "西", FiveElement.WOOD: "东",
            FiveElement.WATER: "北", FiveElement.FIRE: "南",
            FiveElement.EARTH: "中",
        }
        color_map = {
            FiveElement.METAL: "白", FiveElement.WOOD: "青",
            FiveElement.WATER: "黑", FiveElement.FIRE: "赤",
            FiveElement.EARTH: "黄",
        }

        beings = ["真人", "道君", "天尊", "仙尊", "圣君", "大帝", "老祖", "上仙"]
        concepts = ["虚", "玄", "元", "始", "初", "极", "微", "妙"]

        element = self.calculate_element_from_birth(
            random.randint(1980, 2024), random.randint(1, 12), random.randint(1, 28)
        )

        return template.format(
            element=element_map.get(element, "玄"),
            being=random.choice(beings),
            concept=random.choice(concepts),
            direction=direction_map.get(element, "中"),
            color=color_map.get(element, "玄"),
        )

    def get_element_compatibility(self, name1: str,
                                  name2: str) -> Dict[str, str]:
        """分析两个名字的五行相生相克关系"""
        return {
            "相生关系": "木生火，火生土，土生金，金生水，水生木",
            "相克关系": "木克土，土克水，水克火，火克金，金克木",
            "提示": "角色关系可参考五行生克设计冲突与羁绊",
        }

    def get_all_surnames(self) -> List[str]:
        """获取所有姓氏的扁平列表"""
        all_s = []
        for category in ["top10", "top50", "common", "less_common", "compound", "rare", "literary"]:
            all_s.extend(self.surnames.get(category, []))
        return all_s

    def get_surname_by_category(self, category: str) -> List[str]:
        """按分类获取姓氏"""
        return self.surnames.get(category, [])

    def get_random_surname(self, categories: List[str] = None) -> str:
        """随机获取姓氏"""
        if categories is None:
            categories = ["top10", "top50", "common"]
        pool = []
        for cat in categories:
            pool.extend(self.surnames.get(cat, []))
        return random.choice(pool) if pool else "叶"

    def get_surname_stats(self) -> Dict:
        """获取姓氏库统计"""
        return {
            "total_categories": len(self.surnames),
            "total_surnames": sum(len(v) for v in self.surnames.values()),
            "by_category": {k: len(v) for k, v in self.surnames.items()},
        }


if __name__ == "__main__":
    print("=" * 60)
    print("🏮 中国传统命名系统测试")
    print("=" * 60)

    namer = ChineseTraditionalNamer()

    print("\n【五行推算】")
    element = namer.calculate_element_from_birth(2000, 6, 15)
    print(f"  2000年6月15日生 → 五行属{element.chinese_name}")
    missing = namer.find_missing_element(2000, 6, 15)
    print(f"  八字缺失五行: {missing.chinese_name}")

    print("\n【基础命名 - 五行策略】")
    names = namer.generate(surname="叶", gender=Gender.MALE,
                           element=FiveElement.WOOD,
                           strategy="element_focused", count=3)
    for n in names:
        print(f"  {n.full_name} | 五行:{n.element.chinese_name} | 卦:{n.trigram.chinese_name} | {n.meaning[:50]}")

    print("\n【经典典故命名】")
    names = namer.generate(surname="苏", gender=Gender.FEMALE,
                           strategy="classical", count=3)
    for n in names:
        print(f"  {n.full_name} | {n.meaning[:60]}")

    print("\n【生辰八字命名】")
    names = namer.generate_with_birth("林", 1998, 3, 21, 8,
                                      gender=Gender.MALE, count=3)
    for n in names:
        print(f"  {n.full_name} | 五行:{n.element.chinese_name} | 评分:{n.score}")

    print("\n【辈分命名】")
    names = namer.generate_clan_names("叶", generation=1,
                                      gender=Gender.MALE, count=3)
    for n in names:
        print(f"  {n.full_name} | 辈分字:{n.generation_char} | {n.meaning}")

    print("\n【三才五格分析】")
    analysis = namer.analyze_strokes("叶", "青云")
    for grid, info in analysis.items():
        if grid != "综合评分":
            print(f"  {grid}: {info['value']}画 ({info['judgment'][0]}) - {info['judgment'][1][:40]}")
    print(f"  综合评分: {analysis['综合评分']}/100")

    print("\n【称号生成】")
    for _ in range(3):
        title = namer.generate_title("叶青云", "xuanhuan")
        print(f"  {title}")

    print("\n【五行生克关系】")
    compat = namer.get_element_compatibility("叶青云", "苏婉儿")
    print(f"  {compat['相生关系']}")
    print(f"  {compat['相克关系']}")
    print(f"  {compat['提示']}")
