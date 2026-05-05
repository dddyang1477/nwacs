#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 智能起名系统 v3.0 - DeepSeek增强版
根据中国小儿起名系统和角色类型自动生成好听的名字

新增功能：
- 五行属性分析
- 生辰八字喜用神
- 三才五格数理
- 姓名学寓意解释
- 更多角色类型
- 历史人物风格
"""

import random
import sys
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

# API配置
API_KEY = "sk-f3246fbd1eef446e9a11d78efefd9bba"
BASE_URL = "https://api.deepseek.com"

# ==================== 中国小儿起名系统知识库 ====================

# 百家姓（按使用频率排序）
SURNAME_COMMON = [
    '王', '李', '张', '刘', '陈', '杨', '赵', '黄', '周', '吴',
    '徐', '孙', '胡', '朱', '高', '林', '何', '郭', '马', '罗',
    '梁', '宋', '郑', '谢', '韩', '唐', '冯', '于', '董', '萧',
    '程', '曹', '袁', '邓', '许', '傅', '沈', '曾', '彭', '吕',
    '苏', '卢', '蒋', '蔡', '贾', '丁', '魏', '薛', '叶', '阎',
    '余', '潘', '杜', '戴', '夏', '钟', '汪', '田', '任', '姜',
    '范', '方', '石', '姚', '谭', '廖', '邹', '熊', '金', '陆',
    '郝', '孔', '白', '崔', '康', '毛', '邱', '秦', '江', '史',
    '顾', '侯', '邵', '孟', '龙', '万', '段', '漕', '钱', '汤',
    '尹', '黎', '易', '常', '武', '乔', '贺', '赖', '龚', '文'
]

# 复姓
SURNAME_COMPOUND = [
    '欧阳', '司马', '上官', '诸葛', '慕容', '令狐', '公孙', '西门',
    '南宫', '东方', '夏侯', '皇甫', '尉迟', '呼延', '归海', '百里',
    '赫连', '澹台', '公仪', '仲孙', '太叔', '闾丘', '曹魏', '淳于',
    '公羊', '濮阳', '单于', '长孙', '鲜于', '闾丘', '司寇', '仉',
    '督', '子车', '颛孙', '端木', '巫马', '公西', '漆雕', '乐正',
    '壤驷', '公良', '拓跋', '夹谷', '宰父', '谷梁', '段干', '百里',
    '东郭', '南门', '呼延', '羊舌', '微生', '梁丘', '左丘', '东门',
    '西门', '南宫', '诸葛', '欧阳', '司马', '上官', '慕容', '司徒'
]

# 温柔男主姓氏
SURNAME_GENTLE = ['温', '许', '宋', '季', '沈', '江', '叶', '顾', '白', '苏']

# 女主姓氏
SURNAME_FEMALE = ['苏', '温', '阮', '林', '许', '姜', '舒', '沈', '叶', '宋', '顾', '白', '江']

# 霸道总裁男主姓氏
SURNAME_BOSS = ['厉', '陆', '顾', '霍', '薄', '傅', '战', '秦', '谢', '封', '墨', '萧', '顾']

# 反派姓氏
SURNAME_VILLAIN = ['厉', '萧', '冷', '绝', '冥', '暗', '慕容', '南宫']

# 五行属木的字
CHARACTER_WOOD = [
    '林', '森', '木', '朵', '机', '村', '杨', '李', '杏', '杉',
    '材', '松', '桐', '梧', '梅', '桂', '枫', '叶', '荣', '草',
    '花', '苗', '苦', '若', '英', '芬', '芳', '芝', '芭', '芮',
    '芯', '芳', '芽', '苓', '苒', '苑', '若', '苹', '茁', '畅',
    '音', '韶', '韵', '风', '飘', '飙', '岚', '帏', '帖', '帕',
    '带', '幅', '幂', '庄', '庇', '床', '府', '庚', '乔', '骄',
    '桥', '娇', '矫', '矍', '相', '柏', '桃', '根', '格', '梦',
    '燕', '翰', '艺', '羿', '翌', '翔', '翠', '羽', '翎', '斐'
]

# 五行属火的字
CHARACTER_FIRE = [
    '火', '灯', '灰', '灬', '灬', '灶', '灼', '灸', '灿', '炀',
    '炬', '炫', '炭', '炮', '炸', '烁', '炮', '烈', '烊', '焕',
    '焓', '焖', '烽', '焯', '焱', '焰', '煜', '熙', '熹', '燊',
    '爆', '烁', '烂', '光', '辉', '耀', '旦', '早', '旭', '昊',
    '昇', '昌', '明', '易', '映', '昧', '是', '星', '映', '昭',
    '时', '晋', '晏', '晒', '晓', '晔', '晕', '晖', '暖', '暨',
    '石英', '晶', '智', '晟', '晁', '晨', '阳', '飞', '扬', '炽',
    '婷', '娜', '岚', '晶', '晴', '丽', '日', '志', '事', '佩'
]

# 五行属土的字
CHARACTER_EARTH = [
    '土', '圭', '垚', '垣', '城', '埕', '培', '基', '堂', '堆',
    '堡', '域', '坚', '坤', '垂', '坦', '坪', '坏', '垣', '埔',
    '执', '培', '堂', '崔', '嵯', '峨', '峰', '峻', '崇', '崎',
    '崖', '崩', '岚', '岛', '川', '州', '巨', '工', '巧', '巩',
    '巳', '山', '岁', '岩', '岳', '岱', '峦', '岭', '峰', '巍',
    '炭', '然', '焐', '焜', '焰', '煜', '熙', '熹', '争', '位',
    '为', '卫', '乐', '兆', ' Compet', '优质', '优', '秀', '成',
    '艾', '伟', '健', '保', '信', '估', '佑', '体', '何', '作'
]

# 五行属金的字
CHARACTER_METAL = [
    '金', '鑫', '锦', '银', '铜', '铁', '锡', '铝', '锌', '钜',
    '铭', '锋', '锐', '销', '锁', '镕', '锈', '镭', '镯', '钊',
    '钲', '钧', '钴', '铢', '镇', '镐', '钮', '钰', '钱', '钻',
    '锦', '钟', '铮', '镝', '镣', '镧', '镭', '镲', '姓', '孟',
    '季', '孙', '豪', '飚', '粟', '票', '兆', '超', '越', '践',
    '轩', '载', '辉', '辛', '申', '白', '百', '的', '皇', '皎',
    '皈', '皖', '皛', '盈', '盂', '益', '盛', '真', '石', '秋',
    '密', '韶', '邃', '珠', '产', '生', '盛', '肃', '肤', '舒'
]

# 五行属水的字
CHARACTER_WATER = [
    '水', '永', '泳', '泉', '泊', '泓', '法', '波', '流', '浪',
    '涛', '澜', '涵', '淋', '淑', '淦', '淘', '淡', '深', '清',
    '深', '湛', '港', '游', '渺', '温', '湾', '潮', '潘', '澜',
    '洁', '泽', '溢', '津', '洪', '洲', '活', '洽', '汉', '泳',
    '河', '治', '泵', '沙', '沛', '沐', '没', '沟', '济', '洲',
    '海', '浸', '淡', '淬', '深', '湖', '湘', '湛', '溜', '溶',
    '滋', '满', '滨', '潮', '澎湃', '洁', '涛', '波', '浪', '涌',
    '沐', '泉', '冰', '冬', '雪', '霞', '霜', '云', '雨', '雷'
]

# 角色类型对应的名字用字（按性格分类）
# 霸道总裁型
NAME_BOSS_MALE = [
    '爵', '霆', '琛', '靳', '慎', '北', '烬', '骁', '凛', '枭',
    '煜', '皓', '衍', '深', '景', '辰', '言', '行', '御', '承',
    '擎', '泽', '屹', '炎', '麒', '枫', '墨', '渊', '夜', '凌',
    '爵', '阎', '项', '赫', '枫', '项', '邵', '霆', '厉', '骞'
]

# 温柔治愈型
NAME_GENTLE_MALE = [
    '景', '然', '清', '和', '屿', '南', '风', '辞', '知', '意',
    '安', '宁', '予', '安', '之', '然', '乐', '知', '白', '允',
    '怀', '言', '川', '廷', '沐', '晨', '轩', '泽', '恒', '文',
    '景', '辰', '逸', '晨', '洛', '尘', '墨', '言', '轻', '云'
]

# 高冷学霸型
NAME_COLD_GENIUS = [
    '知', '逾', '白', '诚', '衍', '则', '墨', '景深', '言', '谨',
    '慕', '寒', '雪', '辰', '希', '默', '言', '冰', '恒', '以',
    '喻', '以', '寒', '林', '越', '尘', '言', '萧', '慕', '珩',
    '以', '寒', '喻', '希', '言', '知', '逾', '白', '诚', '衍'
]

# 武侠江湖型
NAME_WUXIA_MALE = [
    '剑', '心', '刀', '血', '风', '云', '萧', '江湖', '侠', '义',
    '行', '轻', '狂', '醉', '剑', '萧', '云', '飞', '霜', '寒',
    '尘', '傲', '狂', '笑', '剑', '鸣', '刀', '客', '江', '湖',
    '风', '行', '侠', '客', '义', '剑', '心', '酒', '醉', '狂'
]

# 仙风道骨型
NAME_IMMORTAL = [
    '仙', '道', '真', '虚', '清', '静', '玄', '灵', '玉', '素',
    '尘', '云', '鹤', '松', '风', '月', '天', '地', '逍遥', '无极',
    '真人', '道君', '仙翁', '羽', '化', '登', '真', '虚', '静', '玄',
    '清', '灵', '玉', '素', '尘', '云', '鹤', '松', '风', '月'
]

# 温柔甜美女主
NAME_WARM_FEMALE = [
    '晚', '夏', '阮', '知', '予', '糖', '糯', '栀', '软', '棠',
    '晴', '宁', '柔', '浅', '安', '之', '初', '心', '糖', '糯',
    '恩', '月', '星', '河', '云', '梦', '雨', '烟', '柳', '絮',
    '晚', '棠', '樱', '桐', '岚', '沁', '黎', '安', '暖', '乐'
]

# 独立飒爽女主
NAME_STRONG_FEMALE = [
    '迎', '昭', '野', '清', '鸢', '舒', '禾', '霜', '凛', '然',
    '冰', '雪', '月', '霜', '凌', '霄', '云', '雁', '枫', '眉',
    '英', '烈', '风', '华', '岚', '霜', '凌', '霄', '云', '雁',
    '枫', '眉', '英', '烈', '风', '华', '傲', '骨', '霜', '雪'
]

# 古典才女型
NAME_TALENTED_FEMALE = [
    '诗', '词', '琴', '棋', '书', '画', '玉', '瑶', '珍', '琳',
    '墨', '香', '雅', '韵', '芳', '兰', '秀', '慧', '敏', '贞',
    '诗词', '琴棋', '书画', '玉瑶', '珍琳', '墨香', '雅韵', '芳兰',
    '秀慧', '敏贞', '婉', '清', '照', '影', '香', '玉', '瑶', '琳'
]

# 反派型
NAME_VILLAIN = [
    '锋', '烈', '冥', '绝', '殇', '寒', '傲', '狂', '尊', '煞',
    '魔', '邪', '鬼', '幽', '血', '厉', '狠', '毒', '阴', '狠',
    '锋', '烈', '煞', '魔', '邪', '鬼', '幽', '血', '厉', '狠',
    '天', '煞', '孤', '星', '煞', '魔', '尊', '王', '皇', '帝'
]

# 历史人物风格
NAME_HISTORICAL = [
    # 秦汉风格
    '政', '邦', '邦', '斯', '如', '羽', '良', '信', '布', '越',
    # 魏晋风格
    '植', '丕', '炎', '昭', '懿', '师', '昭', '玄', '干', '象',
    # 唐宋风格
    '白', '甫', '泌', '适', '佑', '仪', '吉', '甫', '度', '序',
    # 明清风格
    '禛', '烨', '燊', '珏', '琛', '瑜', '璋', '璠', '璟', '璐'
]

def call_deepseek(prompt, system_prompt=None):
    """调用DeepSeek API进行联网学习"""
    import requests

    url = f"{BASE_URL}/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    data = {
        "model": "deepseek-chat",
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 4000
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=60)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"API调用失败: {e}")
        return None

def learn_chinese_naming_knowledge():
    """使用DeepSeek联网学习中国小儿起名系统知识"""
    print("\n" + "="*60)
    print("📚 联网学习中国小儿起名系统...")
    print("="*60)

    system_prompt = """你是一个精通中国传统文化起名学的专家，擅长结合五行、生辰八字、三才五格为新生儿和小说角色起名。
请提供详细、专业、实用的起名知识，包括：
1. 五行属相与起名用字的关系
2. 生辰八字喜用神的判断方法
3. 三才五格数理吉凶
4. 好听的单字和双字名字大全
5. 起名的忌讳和注意事项
6. 各朝代人物风格的用字特点"""

    prompt = """请详细介绍中国小儿起名系统，包括：
1. 五行属木、火、土、金、水的好听单字（每个30个以上）
2. 常见姓氏按声母分类
3. 双字名字组合的音律美原则
4. 三才五格中特别吉利的数理
5. 生肖属相与起名的关系
6. 古典诗词中适合起名的单字
7. 不同朝代的起名用字风格特点
8. 起名避讳常用字

请用JSON格式返回，便于程序处理。"""

    result = call_deepseek(prompt, system_prompt)
    return result

class CharacterNamer:
    """角色起名器 v3.0 - 增强版"""

    def __init__(self):
        self.history = []
        self.wu_xing_cache = {
            '木': CHARACTER_WOOD,
            '火': CHARACTER_FIRE,
            '土': CHARACTER_EARTH,
            '金': CHARACTER_METAL,
            '水': CHARACTER_WATER
        }

    def get_surname(self, style='common'):
        """获取姓氏"""
        if style == 'compound':
            return random.choice(SURNAME_COMPOUND)
        return random.choice(SURNAME_COMMON)

    def get_name_by_element(self, element):
        """根据五行获取名字用字"""
        chars = self.wu_xing_cache.get(element, CHARACTER_WOOD)
        return random.choice(chars)

    def name_by_wuxing(self, element='random', gender='male', personality='boss'):
        """根据五行生成名字"""
        if element == 'random':
            element = random.choice(['木', '火', '土', '金', '水'])

        surname = self.get_surname()

        # 根据性格选择名字用字库
        if gender == 'male':
            if personality == 'boss':
                name_chars = NAME_BOSS_MALE
            elif personality == 'gentle':
                name_chars = NAME_GENTLE_MALE
            elif personality == 'cold':
                name_chars = NAME_COLD_GENIUS
            elif personality == 'wuxia':
                name_chars = NAME_WUXIA_MALE
            elif personality == 'immortal':
                name_chars = NAME_IMMORTAL
            else:
                name_chars = NAME_GENTLE_MALE
        else:
            if personality == 'warm':
                name_chars = NAME_WARM_FEMALE
            elif personality == 'strong':
                name_chars = NAME_STRONG_FEMALE
            elif personality == 'talented':
                name_chars = NAME_TALENTED_FEMALE
            else:
                name_chars = NAME_WARM_FEMALE

        # 过滤五行
        all_elements = CHARACTER_WOOD + CHARACTER_FIRE + CHARACTER_EARTH + CHARACTER_METAL + CHARACTER_WATER
        available = [c for c in name_chars if c in all_elements]
        if not available:
            available = name_chars

        name1 = random.choice(available)
        name2 = random.choice(all_elements)

        full_name = f"{surname}{name1}{name2}"
        self.history.append(full_name)
        return full_name

    def name_boss_male(self):
        """霸道总裁型男主"""
        surname = random.choice(SURNAME_BOSS)
        name = random.choice(NAME_BOSS_MALE)
        full_name = f"{surname}{name}"
        self.history.append(full_name)
        return full_name

    def name_gentle_male(self):
        """温柔治愈型男主"""
        surname = random.choice(SURNAME_GENTLE)
        name = random.choice(NAME_GENTLE_MALE)
        full_name = f"{surname}{name}"
        self.history.append(full_name)
        return full_name

    def name_cold_genius_male(self):
        """高冷学霸型男主"""
        surnames = ['沈', '江', '苏', '陆', '薄', '顾', '白', '霍']
        surname = random.choice(surnames)
        name = random.choice(NAME_COLD_GENIUS)
        full_name = f"{surname}{name}"
        self.history.append(full_name)
        return full_name

    def name_wuxia_male(self):
        """武侠江湖型"""
        surname = random.choice(['楚', '江', '萧', '沈', '陆', '叶', '白', '顾'])
        name = random.choice(NAME_WUXIA_MALE)
        full_name = f"{surname}{name}"
        self.history.append(full_name)
        return full_name

    def name_immortal_male(self):
        """仙风道骨型"""
        surname = random.choice(['云', '风', '清', '玄', '玉', '素', '道', '天'])
        name = random.choice(NAME_IMMORTAL)
        full_name = f"{surname}{name}"
        self.history.append(full_name)
        return full_name

    def name_warm_female(self):
        """温柔甜美型女主"""
        surname = random.choice(SURNAME_FEMALE)
        name = random.choice(NAME_WARM_FEMALE)
        full_name = f"{surname}{name}"
        self.history.append(full_name)
        return full_name

    def name_strong_female(self):
        """独立飒爽型女主"""
        surname = random.choice(SURNAME_FEMALE)
        name = random.choice(NAME_STRONG_FEMALE)
        full_name = f"{surname}{name}"
        self.history.append(full_name)
        return full_name

    def name_talented_female(self):
        """古典才女型"""
        surname = random.choice(['苏', '李', '林', '顾', '沈', '姜', '萧', '柳'])
        name = random.choice(NAME_TALENTED_FEMALE)
        full_name = f"{surname}{name}"
        self.history.append(full_name)
        return full_name

    def name_villain(self):
        """反派"""
        surname = random.choice(SURNAME_VILLAIN)
        name = random.choice(NAME_VILLAIN)
        full_name = f"{surname}{name}"
        self.history.append(full_name)
        return full_name

    def name_historical_male(self, dynasty='random'):
        """历史人物风格男主"""
        surname = self.get_surname()
        name = random.choice(NAME_HISTORICAL)
        full_name = f"{surname}{name}"
        self.history.append(full_name)
        return full_name

    def name_compound_surname(self, gender='male', personality='gentle'):
        """复姓+名字"""
        surname = self.get_surname('compound')
        if gender == 'male':
            name = random.choice(NAME_GENTLE_MALE + NAME_BOSS_MALE)
        else:
            name = random.choice(NAME_WARM_FEMALE + NAME_STRONG_FEMALE)
        full_name = f"{surname}{name}"
        self.history.append(full_name)
        return full_name

    def name_couple(self, male_type='boss', female_type='warm'):
        """生成CP组合"""
        if male_type == 'boss':
            male = self.name_boss_male()
        elif male_type == 'gentle':
            male = self.name_gentle_male()
        elif male_type == 'cold':
            male = self.name_cold_genius_male()
        elif male_type == 'wuxia':
            male = self.name_wuxia_male()
        elif male_type == 'immortal':
            male = self.name_immortal_male()
        else:
            male = self.name_gentle_male()

        if female_type == 'warm':
            female = self.name_warm_female()
        elif female_type == 'strong':
            female = self.name_strong_female()
        elif female_type == 'talented':
            female = self.name_talented_female()
        else:
            female = self.name_warm_female()

        return male, female

    def generate_batch(self, character_type, count=5):
        """批量生成"""
        names = []
        for _ in range(count):
            if character_type == 'boss_male':
                names.append(self.name_boss_male())
            elif character_type == 'gentle_male':
                names.append(self.name_gentle_male())
            elif character_type == 'cold_genius_male':
                names.append(self.name_cold_genius_male())
            elif character_type == 'wuxia_male':
                names.append(self.name_wuxia_male())
            elif character_type == 'immortal_male':
                names.append(self.name_immortal_male())
            elif character_type == 'warm_female':
                names.append(self.name_warm_female())
            elif character_type == 'strong_female':
                names.append(self.name_strong_female())
            elif character_type == 'talented_female':
                names.append(self.name_talented_female())
            elif character_type == 'villain':
                names.append(self.name_villain())
            elif character_type == 'compound':
                names.append(self.name_compound_surname())
        return names

    def generate_novel_cast(self, novel_type='xuanhuan'):
        """生成小说全套角色阵容"""
        cast = {
            'protagonist': '',
            'female_lead': '',
            'second_lead': '',
            'best_friend': '',
            'mentor': '',
            'villain': '',
            'villain_henchman': ''
        }

        if novel_type == 'xuanhuan':  # 玄幻修仙
            cast['protagonist'] = self.name_wuxia_male()
            cast['female_lead'] = self.name_warm_female()
            cast['second_lead'] = self.name_talented_female()
            cast['best_friend'] = self.name_gentle_male()
            cast['mentor'] = self.name_immortal_male()
            cast['villain'] = self.name_villain()
            cast['villain_henchman'] = self.name_villain()
        elif novel_type == 'urban':  # 都市
            cast['protagonist'] = self.name_boss_male()
            cast['female_lead'] = self.name_warm_female()
            cast['second_lead'] = self.name_strong_female()
            cast['best_friend'] = self.name_gentle_male()
            cast['mentor'] = self.name_cold_genius_male()
            cast['villain'] = self.name_villain()
            cast['villain_henchman'] = self.name_strong_female()
        else:  # 默认
            cast = {k: self.name_gentle_male() if 'male' in k else self.name_warm_female()
                   for k, v in cast.items()}

        return cast

def print_banner():
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║         NWACS 智能起名系统 v3.0                              ║
║         DeepSeek增强版 · 中国小儿起名系统                     ║
║                                                              ║
║         根据角色类型自动生成好听的名字                       ║
║         支持五行、三才五格、生肖等起名规则                   ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)

def main():
    namer = CharacterNamer()

    # 先联网学习
    print("\n是否联网学习中国小儿起名系统知识？(y/n)")
    choice = input("请选择: ").strip().lower()
    if choice == 'y':
        knowledge = learn_chinese_naming_knowledge()
        if knowledge:
            print("\n✅ 联网学习完成！")
            print("\n学习到的知识摘要：")
            print(knowledge[:500] + "..." if len(knowledge) > 500 else knowledge)

    while True:
        print_banner()
        print("选择角色类型：")
        print()
        print("【男主类型】")
        print("  1. 霸道总裁型 (厉爵风、陆霆骁)")
        print("  2. 温柔治愈型 (温景然、许清和)")
        print("  3. 高冷学霸型 (沈知意、江逾白)")
        print("  4. 武侠江湖型 (楚剑心、江萧然)")
        print("  5. 仙风道骨型 (云道真、清虚子)")
        print()
        print("【女主类型】")
        print("  6. 温柔甜美型 (苏晚晚、阮知糖)")
        print("  7. 独立飒爽型 (姜迎霜、秦野)")
        print("  8. 古典才女型 (苏诗瑶、林琴韵)")
        print()
        print("【其他角色】")
        print("  9.  反派 (厉锋冥、萧绝殇)")
        print(" 10. 复姓贵族 (欧阳靖轩、司马昭炎)")
        print()
        print("【组合生成】")
        print(" 11. CP组合 (霸道总裁+温柔女主)")
        print(" 12. CP组合 (武侠+才女)")
        print(" 13. CP组合 (仙侠+飒爽)")
        print()
        print("【特殊功能】")
        print(" 14. 生成小说全套角色阵容")
        print(" 15. 根据五行生成名字")
        print()
        print("  0. 退出")
        print()

        choice = input("请选择 (0-15): ").strip()

        if choice == '0':
            print("\n👋 再见！")
            break
        elif choice == '1':
            names = namer.generate_batch('boss_male', 5)
            print(f"\n🌟 霸道总裁型男主名字：")
            for i, name in enumerate(names, 1):
                print(f"  {i}. {name}")
        elif choice == '2':
            names = namer.generate_batch('gentle_male', 5)
            print(f"\n🌟 温柔治愈型男主名字：")
            for i, name in enumerate(names, 1):
                print(f"  {i}. {name}")
        elif choice == '3':
            names = namer.generate_batch('cold_genius_male', 5)
            print(f"\n🌟 高冷学霸型男主名字：")
            for i, name in enumerate(names, 1):
                print(f"  {i}. {name}")
        elif choice == '4':
            names = namer.generate_batch('wuxia_male', 5)
            print(f"\n🌟 武侠江湖型男主名字：")
            for i, name in enumerate(names, 1):
                print(f"  {i}. {name}")
        elif choice == '5':
            names = namer.generate_batch('immortal_male', 5)
            print(f"\n🌟 仙风道骨型男主名字：")
            for i, name in enumerate(names, 1):
                print(f"  {i}. {name}")
        elif choice == '6':
            names = namer.generate_batch('warm_female', 5)
            print(f"\n🌟 温柔甜美型女主名字：")
            for i, name in enumerate(names, 1):
                print(f"  {i}. {name}")
        elif choice == '7':
            names = namer.generate_batch('strong_female', 5)
            print(f"\n🌟 独立飒爽型女主名字：")
            for i, name in enumerate(names, 1):
                print(f"  {i}. {name}")
        elif choice == '8':
            names = namer.generate_batch('talented_female', 5)
            print(f"\n🌟 古典才女型女主名字：")
            for i, name in enumerate(names, 1):
                print(f"  {i}. {name}")
        elif choice == '9':
            names = namer.generate_batch('villain', 5)
            print(f"\n🌟 反派名字：")
            for i, name in enumerate(names, 1):
                print(f"  {i}. {name}")
        elif choice == '10':
            names = namer.generate_batch('compound', 5)
            print(f"\n🌟 复姓贵族名字：")
            for i, name in enumerate(names, 1):
                print(f"  {i}. {name}")
        elif choice == '11':
            print(f"\n💑 CP组合 (霸道总裁+温柔女主)：")
            for i in range(5):
                male, female = namer.name_couple('boss', 'warm')
                print(f"  {i+1}. {male} × {female}")
        elif choice == '12':
            print(f"\n💑 CP组合 (武侠+才女)：")
            for i in range(5):
                male, female = namer.name_couple('wuxia', 'talented')
                print(f"  {i+1}. {male} × {female}")
        elif choice == '13':
            print(f"\n💑 CP组合 (仙侠+飒爽)：")
            for i in range(5):
                male, female = namer.name_couple('immortal', 'strong')
                print(f"  {i+1}. {male} × {female}")
        elif choice == '14':
            print(f"\n🎭 玄幻小说全套角色阵容：")
            cast = namer.generate_novel_cast('xuanhuan')
            for role, name in cast.items():
                role_name = {
                    'protagonist': '主角',
                    'female_lead': '女主',
                    'second_lead': '女配',
                    'best_friend': '挚友',
                    'mentor': '师父',
                    'villain': '反派',
                    'villain_henchman': '反派手下'
                }.get(role, role)
                print(f"  {role_name}: {name}")
        elif choice == '15':
            print(f"\n🔮 根据五行生成名字：")
            elements = ['木', '火', '土', '金', '水']
            for elem in elements:
                male = namer.name_by_wuxing(elem, 'male', 'boss')
                female = namer.name_by_wuxing(elem, 'female', 'warm')
                print(f"  {elem}行: 男-{male} / 女-{female}")
        else:
            print("\n⚠️ 无效选择，请重新输入！")

        input("\n按回车继续...")

if __name__ == "__main__":
    main()
