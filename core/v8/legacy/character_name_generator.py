#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 角色命名生成器 - CharacterNameGenerator
核心功能：
1. 多题材命名 - 玄幻/都市/古风/武侠/现代
2. 性别区分 - 男名/女名/中性名
3. 含义命名 - 基于性格/命运/能力生成有含义的名字
4. 称号生成 - 道号/绰号/尊称/笔名
5. 批量生成 - 一次性生成多个角色名
6. 去重检查 - 避免与已有角色重名

设计原则：
- 纯本地规则引擎，零API调用
- 基于大量名字语料库的模板组合
- 支持自定义规则扩展
"""

import random
import json
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field


@dataclass
class GeneratedName:
    """生成的名字"""
    full_name: str
    surname: str
    given_name: str
    gender: str
    style: str
    meaning: str
    pinyin: str = ""
    alias: str = ""


class NameElementPool:
    """名字元素池"""

    # 玄幻/仙侠 姓氏
    XUANHUAN_SURNAMES = [
        "叶", "林", "萧", "苏", "云", "秦", "楚", "慕容", "上官",
        "独孤", "南宫", "东方", "西门", "北冥", "皇甫", "欧阳",
        "龙", "凤", "白", "墨", "凌", "沈", "陆", "顾", "裴",
        "轩辕", "令狐", "端木", "公孙", "尉迟", "司马", "诸葛",
    ]

    # 都市/现代 姓氏
    URBAN_SURNAMES = [
        "王", "李", "张", "刘", "陈", "杨", "赵", "黄", "周", "吴",
        "徐", "孙", "胡", "朱", "高", "林", "何", "郭", "马", "罗",
        "梁", "宋", "郑", "谢", "韩", "唐", "冯", "于", "董", "萧",
        "程", "曹", "袁", "邓", "许", "傅", "沈", "曾", "彭", "吕",
    ]

    # 玄幻男名用字
    XUANHUAN_MALE_GIVEN = [
        "天", "云", "辰", "宇", "昊", "轩", "逸", "尘", "渊", "玄",
        "霄", "凌", "风", "霆", "曜", "曦", "澜", "泽", "瀚", "宸",
        "瑾", "瑜", "珩", "琰", "琮", "珩", "璟", "璨", "皓", "晔",
        "青云", "无极", "长生", "破天", "问道", "逍遥", "无痕",
        "子轩", "子墨", "子涵", "子昂", "子衿", "子渊", "子期",
    ]

    # 玄幻女名用字
    XUANHUAN_FEMALE_GIVEN = [
        "雪", "月", "瑶", "璃", "璇", "琳", "玥", "琪", "婉", "清",
        "灵", "若", "诗", "画", "琴", "韵", "芷", "兰", "萱", "薇",
        "凝", "霜", "冰", "烟", "雨", "晴", "柔", "静", "雅", "娴",
        "婉儿", "灵儿", "雪儿", "月儿", "瑶儿", "璃儿", "璇儿",
        "若兰", "如烟", "似水", "倾城", "倾国", "无双", "天音",
    ]

    # 都市男名用字
    URBAN_MALE_GIVEN = [
        "伟", "强", "磊", "军", "勇", "杰", "涛", "明", "辉", "鹏",
        "浩", "宇", "轩", "然", "博", "文", "哲", "翰", "霖", "毅",
        "子豪", "志远", "思远", "博文", "浩然", "宇轩", "子涵",
        "一鸣", "天宇", "俊杰", "嘉诚", "铭泽", "睿渊", "煜城",
    ]

    # 都市女名用字
    URBAN_FEMALE_GIVEN = [
        "芳", "敏", "静", "丽", "婷", "雪", "玲", "萍", "红", "霞",
        "欣", "怡", "悦", "瑶", "琳", "琪", "颖", "萱", "宁", "彤",
        "雨桐", "梓涵", "一诺", "欣怡", "诗涵", "梦瑶", "语嫣",
        "思雨", "晓彤", "雅静", "若曦", "紫萱", "沐晴", "安琪",
    ]

    # 古风/武侠 名字用字
    WUXIA_SURNAMES = [
        "燕", "谢", "殷", "任", "向", "霍", "段", "乔", "韦", "岳",
        "花", "柳", "铁", "石", "风", "雷", "冷", "温", "江", "水",
    ]

    WUXIA_GIVEN = [
        "无忌", "孤城", "寻欢", "留香", "吹雪", "寻梦", "问天",
        "飞鸿", "惊鸿", "踏雪", "追风", "逐月", "听雨", "观潮",
        "断水", "残阳", "落雁", "沉鱼", "闭月", "羞花",
        "一剑", "无剑", "有剑", "忘剑", "藏剑", "出剑",
    ]

    # 含义词库 - 用于生成有含义的名字
    MEANING_WORDS = {
        "智慧": ["明", "哲", "睿", "慧", "智", "聪", "颖", "悟", "思", "谋"],
        "勇敢": ["勇", "毅", "刚", "烈", "猛", "豪", "雄", "武", "威", "霸"],
        "美丽": ["美", "丽", "秀", "艳", "娇", "媚", "婷", "娜", "媛", "姝"],
        "高贵": ["尊", "贵", "雅", "华", "荣", "耀", "辉", "煌", "圣", "皇"],
        "神秘": ["幽", "冥", "玄", "秘", "隐", "暗", "影", "幻", "虚", "空"],
        "温柔": ["柔", "婉", "娴", "淑", "静", "雅", "温", "和", "善", "良"],
        "强大": ["天", "帝", "皇", "尊", "圣", "神", "王", "霸", "龙", "凤"],
        "自由": ["逍", "遥", "逸", "游", "翔", "飞", "飘", "流", "放", "纵"],
    }

    # 称号/道号前缀
    TITLE_PREFIXES = [
        "太虚", "紫霄", "青云", "碧落", "黄泉", "九天", "万古",
        "混元", "无极", "太上", "玄天", "灵虚", "真武", "天机",
        "血手", "铁剑", "金刀", "银枪", "铜锤", "玉笛", "冰心",
        "毒手", "鬼影", "神行", "飞天", "遁地", "翻江", "倒海",
    ]

    TITLE_SUFFIXES = [
        "真人", "道君", "天尊", "仙尊", "帝君", "圣君", "神君",
        "上人", "散人", "居士", "先生", "大师", "老祖", "老魔",
        "剑仙", "刀皇", "枪神", "拳圣", "腿王", "掌尊", "指帝",
    ]


class CharacterNameGenerator:
    """角色命名生成器"""

    def __init__(self, memory_manager=None):
        self.pool = NameElementPool()
        self.memory = memory_manager
        self.used_names: set = set()
        self.generation_count = 0

    def generate(self, genre: str = "xuanhuan", gender: str = "male",
                 count: int = 1, style: str = None,
                 meaning_keywords: List[str] = None) -> List[GeneratedName]:
        """
        生成角色名字

        参数:
            genre: 题材 - xuanhuan/urban/wuxia/historical
            gender: 性别 - male/female/neutral
            count: 生成数量
            style: 风格 - elegant/powerful/mysterious/gentle
            meaning_keywords: 含义关键词列表
        """
        results = []
        attempts = 0
        max_attempts = count * 20

        while len(results) < count and attempts < max_attempts:
            attempts += 1
            name = self._generate_single(genre, gender, style, meaning_keywords)

            if name.full_name not in self.used_names:
                self.used_names.add(name.full_name)
                results.append(name)
                self.generation_count += 1

        return results

    def _generate_single(self, genre: str, gender: str,
                         style: str = None,
                         meaning_keywords: List[str] = None) -> GeneratedName:
        """生成单个名字"""
        if genre == "xuanhuan":
            surname = random.choice(self.pool.XUANHUAN_SURNAMES)
            if gender == "male":
                given = random.choice(self.pool.XUANHUAN_MALE_GIVEN)
            else:
                given = random.choice(self.pool.XUANHUAN_FEMALE_GIVEN)

        elif genre == "urban":
            surname = random.choice(self.pool.URBAN_SURNAMES)
            if gender == "male":
                given = random.choice(self.pool.URBAN_MALE_GIVEN)
            else:
                given = random.choice(self.pool.URBAN_FEMALE_GIVEN)

        elif genre == "wuxia":
            surname = random.choice(self.pool.WUXIA_SURNAMES)
            given = random.choice(self.pool.WUXIA_GIVEN)

        else:
            surname = random.choice(self.pool.XUANHUAN_SURNAMES)
            given = random.choice(self.pool.XUANHUAN_MALE_GIVEN)

        if meaning_keywords:
            given = self._apply_meaning(given, meaning_keywords, gender)

        if style:
            given = self._apply_style(given, style)

        meaning = self._derive_meaning(surname, given, genre)

        return GeneratedName(
            full_name=f"{surname}{given}",
            surname=surname,
            given_name=given,
            gender=gender,
            style=style or "default",
            meaning=meaning,
        )

    def _apply_meaning(self, given: str, keywords: List[str], gender: str) -> str:
        """根据含义关键词调整名字"""
        available_chars = []
        for kw in keywords:
            if kw in self.pool.MEANING_WORDS:
                available_chars.extend(self.pool.MEANING_WORDS[kw])

        if available_chars and len(given) <= 2:
            meaning_char = random.choice(available_chars)
            if len(given) == 1:
                given = meaning_char + given
            else:
                given = given[0] + meaning_char

        return given

    def _apply_style(self, given: str, style: str) -> str:
        """根据风格调整名字"""
        style_chars = {
            "elegant": ["雅", "清", "逸", "韵", "瑾", "瑶", "诗", "琴"],
            "powerful": ["天", "霸", "龙", "帝", "皇", "尊", "圣", "神"],
            "mysterious": ["幽", "冥", "玄", "隐", "暗", "影", "幻", "虚"],
            "gentle": ["柔", "婉", "静", "和", "温", "善", "淑", "娴"],
        }

        chars = style_chars.get(style, [])
        if chars and len(given) <= 2:
            style_char = random.choice(chars)
            if len(given) == 1:
                given = given + style_char
            else:
                given = given[0] + style_char

        return given

    def _derive_meaning(self, surname: str, given: str, genre: str) -> str:
        """推导名字含义"""
        meanings = []

        char_meanings = {
            "天": "天空/天道", "云": "云彩/高远", "辰": "星辰/时光",
            "宇": "宇宙/气度", "昊": "广阔天空", "轩": "高大/气宇轩昂",
            "雪": "纯洁/高洁", "月": "明月/清冷", "瑶": "美玉/珍贵",
            "璃": "琉璃/璀璨", "璇": "美玉/星辰", "琳": "美玉/琳琅",
            "龙": "神龙/尊贵", "凤": "凤凰/祥瑞", "剑": "剑道/锋芒",
            "叶": "生机/平凡中见不凡", "林": "森林/包容",
            "萧": "萧瑟/深沉", "苏": "复苏/希望",
        }

        for char in given:
            if char in char_meanings:
                meanings.append(char_meanings[char])

        if meanings:
            return "、".join(meanings[:3])
        return f"{genre}风格名字"

    def generate_title(self, genre: str = "xuanhuan",
                       personality: str = "neutral") -> str:
        """生成称号/道号"""
        prefix = random.choice(self.pool.TITLE_PREFIXES)
        suffix = random.choice(self.pool.TITLE_SUFFIXES)
        return f"{prefix}{suffix}"

    def generate_alias(self, name: str, genre: str = "xuanhuan") -> str:
        """为已有名字生成别名/绰号"""
        alias_patterns = [
            lambda n: f"小{n[-1]}" if len(n) >= 2 else f"小{n}",
            lambda n: f"老{n[0]}" if n else "老某",
            lambda n: f"阿{n[-1]}" if len(n) >= 2 else f"阿{n}",
            lambda n: f"{n}子",
            lambda n: f"{n}儿",
        ]
        pattern = random.choice(alias_patterns)
        return pattern(name)

    def generate_clan_name(self, genre: str = "xuanhuan") -> str:
        """生成宗门/家族名称"""
        clan_prefixes = [
            "青云", "紫霄", "太虚", "天剑", "万剑", "星辰", "日月",
            "碧落", "黄泉", "九天", "灵虚", "玄天", "真武", "天机",
            "血煞", "幽冥", "天魔", "万毒", "噬魂", "炼狱", "修罗",
        ]
        clan_suffixes = [
            "宗", "派", "门", "阁", "殿", "宫", "谷", "山", "峰",
            "堡", "城", "府", "庄", "楼", "堂", "盟", "教",
        ]
        return f"{random.choice(clan_prefixes)}{random.choice(clan_suffixes)}"

    def generate_full_character_name(self, genre: str = "xuanhuan",
                                     gender: str = "male",
                                     include_title: bool = True,
                                     include_alias: bool = True) -> Dict:
        """生成完整角色命名包"""
        names = self.generate(genre, gender, count=1)
        if not names:
            return {}

        name = names[0]
        result = {
            "full_name": name.full_name,
            "surname": name.surname,
            "given_name": name.given_name,
            "gender": name.gender,
            "meaning": name.meaning,
        }

        if include_title:
            result["title"] = self.generate_title(genre)

        if include_alias:
            result["alias"] = self.generate_alias(name.given_name, genre)

        return result

    def batch_generate(self, genre: str = "xuanhuan",
                       specs: List[Dict] = None) -> List[Dict]:
        """
        批量生成角色名

        specs = [
            {"gender": "male", "role": "主角", "style": "powerful"},
            {"gender": "female", "role": "女主", "style": "elegant"},
            {"gender": "male", "role": "反派", "style": "mysterious"},
        ]
        """
        if specs is None:
            specs = [
                {"gender": "male", "role": "主角"},
                {"gender": "female", "role": "女主"},
                {"gender": "male", "role": "反派"},
            ]

        results = []
        for spec in specs:
            name_data = self.generate_full_character_name(
                genre=genre,
                gender=spec.get("gender", "male"),
                include_title=True,
                include_alias=True,
            )
            name_data["role"] = spec.get("role", "未知")
            name_data["style"] = spec.get("style", "default")
            results.append(name_data)

        return results

    def check_name_quality(self, name: str) -> Dict[str, Any]:
        """检查名字质量"""
        issues = []
        score = 100

        if len(name) < 2:
            issues.append("名字过短")
            score -= 30
        elif len(name) > 4:
            issues.append("名字过长")
            score -= 10

        awkward_combos = ["死死", "鬼鬼", "贱贱", "臭臭", "屎屎"]
        for combo in awkward_combos:
            if combo in name:
                issues.append(f"包含不当组合: {combo}")
                score -= 40

        rare_chars = ["龘", "靐", "齉", "龘", "爨", "癵"]
        for char in rare_chars:
            if char in name:
                issues.append(f"包含生僻字: {char}")
                score -= 15

        return {
            "name": name,
            "score": max(score, 0),
            "issues": issues,
            "is_good": score >= 70 and len(issues) == 0,
        }

    def reset_used_names(self):
        """重置已用名字集合"""
        self.used_names.clear()


if __name__ == "__main__":
    print("=" * 60)
    print("📛 NWACS 角色命名生成器测试")
    print("=" * 60)

    gen = CharacterNameGenerator()

    print("\n【玄幻男名 x5】")
    for name in gen.generate("xuanhuan", "male", 5):
        print(f"  {name.full_name} — {name.meaning}")

    print("\n【玄幻女名 x5】")
    for name in gen.generate("xuanhuan", "female", 5):
        print(f"  {name.full_name} — {name.meaning}")

    print("\n【都市男名 x5】")
    for name in gen.generate("urban", "male", 5):
        print(f"  {name.full_name} — {name.meaning}")

    print("\n【武侠名字 x5】")
    for name in gen.generate("wuxia", "male", 5):
        print(f"  {name.full_name} — {name.meaning}")

    print("\n【含义命名 - 智慧+勇敢】")
    for name in gen.generate("xuanhuan", "male", 3, meaning_keywords=["智慧", "勇敢"]):
        print(f"  {name.full_name} — {name.meaning}")

    print("\n【称号生成 x5】")
    for _ in range(5):
        print(f"  {gen.generate_title('xuanhuan')}")

    print("\n【宗门名称 x5】")
    for _ in range(5):
        print(f"  {gen.generate_clan_name()}")

    print("\n【完整角色命名包】")
    char = gen.generate_full_character_name("xuanhuan", "male")
    print(f"  {json.dumps(char, ensure_ascii=False, indent=2)}")

    print("\n【批量生成】")
    batch = gen.batch_generate("xuanhuan")
    for c in batch:
        print(f"  {c['role']}: {c['full_name']} ({c['title']})")

    print("\n【名字质量检查】")
    for test_name in ["叶青云", "狗蛋", "龘靐", "死死死"]:
        quality = gen.check_name_quality(test_name)
        status = "✅" if quality["is_good"] else "❌"
        print(f"  {status} {test_name}: {quality['score']}分 {quality['issues']}")
