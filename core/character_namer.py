#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 智能起名系统 v2.0
根据角色类型自动生成好听的名字
"""

import random
import sys

sys.stdout.reconfigure(encoding='utf-8')

# 霸道总裁男主姓氏
SURNAME_BOSS = ['厉', '陆', '顾', '霍', '薄', '傅', '战', '秦', '谢', '封', '墨', '萧', '顾']

# 霸道总裁名字用字（霸气）
NAME_BOSS = ['爵', '霆', '琛', '靳', '慎', '北', '烬', '骁', '凛', '枭', '煜', '皓', '衍', '深', '景', '辰', '言', '行', '御', '承']

# 温柔男主姓氏
SURNAME_GENTLE = ['温', '许', '宋', '季', '沈', '江', '叶']

# 温柔男主名字用字
NAME_GENTLE = ['景', '然', '清', '和', '屿', '南', '风', '辞', '知', '意']

# 女主姓氏
SURNAME_FEMALE = ['苏', '温', '阮', '林', '许', '姜', '舒', '沈', '叶', '宋', '顾', '白', '江']

# 女主名字用字（温柔甜美）
NAME_FEMALE_WARM = ['晚', '夏', '阮', '知', '予', '糖', '糯', '栀', '软', '棠', '晴', '宁', '柔', '浅']

# 女主名字用字（独立飒爽）
NAME_FEMALE_STRONG = ['迎', '昭', '野', '清', '鸢', '舒', '禾', '霜', '凛']

# 反派姓氏
SURNAME_VILLAIN = ['厉', '萧', '冷', '绝', '冥', '暗', '慕容', '南宫']

# 反派名字用字
NAME_VILLAIN = ['锋', '烈', '冥', '绝', '殇', '寒', '傲', '狂', '尊']

# 闺蜜/女配姓氏
SURNAME_FRIEND = ['张', '王', '李', '陈', '刘', '赵', '周', '吴']

# 闺蜜名字
NAME_FRIEND = ['玲', '娜', '芳', '洋', '丽', '静', '小雨', '诗语']

class CharacterNamer:
    """角色起名器"""

    def __init__(self):
        self.history = []

    def name_boss_male(self):
        """霸道总裁型男主"""
        surname = random.choice(SURNAME_BOSS)
        name = random.choice(NAME_BOSS)
        full_name = f"{surname}{name}"
        self.history.append(full_name)
        return full_name

    def name_gentle_male(self):
        """温柔治愈型男主"""
        surname = random.choice(SURNAME_GENTLE)
        name = random.choice(NAME_GENTLE)
        full_name = f"{surname}{name}"
        self.history.append(full_name)
        return full_name

    def name_cold_genius_male(self):
        """高冷学霸型男主"""
        surnames = ['沈', '江', '苏', '陆', '薄']
        names = ['知', '逾', '白', '诚', '衍', '则', '墨', '景深']
        surname = random.choice(surnames)
        name = random.choice(names)
        full_name = f"{surname}{name}"
        self.history.append(full_name)
        return full_name

    def name_warm_female(self):
        """温柔甜美型女主"""
        surname = random.choice(SURNAME_FEMALE)
        name = random.choice(NAME_FEMALE_WARM)
        full_name = f"{surname}{name}"
        self.history.append(full_name)
        return full_name

    def name_strong_female(self):
        """独立飒爽型女主"""
        surname = random.choice(SURNAME_FEMALE)
        name = random.choice(NAME_FEMALE_STRONG)
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

    def name_friend(self):
        """闺蜜/女配"""
        surname = random.choice(SURNAME_FRIEND)
        name = random.choice(NAME_FRIEND)
        full_name = f"{surname}{name}"
        self.history.append(full_name)
        return full_name

    def name_couple(self, male_type='boss', female_type='warm'):
        """生成CP组合"""
        if male_type == 'boss':
            male = self.name_boss_male()
        else:
            male = self.name_gentle_male()

        if female_type == 'warm':
            female = self.name_warm_female()
        else:
            female = self.name_strong_female()

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
            elif character_type == 'warm_female':
                names.append(self.name_warm_female())
            elif character_type == 'strong_female':
                names.append(self.name_strong_female())
            elif character_type == 'villain':
                names.append(self.name_villain())
            elif character_type == 'friend':
                names.append(self.name_friend())
        return names

def print_banner():
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║         NWACS 智能起名系统 v2.0                              ║
║                                                              ║
║         根据角色类型自动生成好听的名字                         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)

def main():
    namer = CharacterNamer()

    while True:
        print_banner()
        print("选择角色类型：")
        print()
        print("【男主类型】")
        print("  1. 霸道总裁型 (厉爵风、陆霆骁、霍景深)")
        print("  2. 温柔治愈型 (温景然、许清和、宋屿)")
        print("  3. 高冷学霸型 (沈知意、江逾白、苏亦诚)")
        print()
        print("【女主类型】")
        print("  4. 温柔甜美型 (苏晚、阮糖、夏栀)")
        print("  5. 独立飒爽型 (姜迎、舒晚、秦野)")
        print()
        print("【其他角色】")
        print("  6. 反派 (厉锋、萧冥烈)")
        print("  7. 闺蜜/女配 (张玲、王娜)")
        print()
        print("【组合生成】")
        print("  8. CP组合 (霸道总裁+温柔女主)")
        print("  9. CP组合 (温柔男主+飒爽女主)")
        print()
        print("  0. 退出")
        print()

        choice = input("请选择 (1-9, 0退出): ").strip()

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
            names = namer.generate_batch('warm_female', 5)
            print(f"\n🌟 温柔甜美型女主名字：")
            for i, name in enumerate(names, 1):
                print(f"  {i}. {name}")
        elif choice == '5':
            names = namer.generate_batch('strong_female', 5)
            print(f"\n🌟 独立飒爽型女主名字：")
            for i, name in enumerate(names, 1):
                print(f"  {i}. {name}")
        elif choice == '6':
            names = namer.generate_batch('villain', 5)
            print(f"\n🌟 反派名字：")
            for i, name in enumerate(names, 1):
                print(f"  {i}. {name}")
        elif choice == '7':
            names = namer.generate_batch('friend', 5)
            print(f"\n🌟 闺蜜/女配名字：")
            for i, name in enumerate(names, 1):
                print(f"  {i}. {name}")
        elif choice == '8':
            print(f"\n💑 CP组合 (霸道总裁+温柔女主)：")
            for i in range(5):
                male, female = namer.name_couple('boss', 'warm')
                print(f"  {i+1}. {male} × {female}")
        elif choice == '9':
            print(f"\n💑 CP组合 (温柔男主+飒爽女主)：")
            for i in range(5):
                male, female = namer.name_couple('gentle', 'strong')
                print(f"  {i+1}. {male} × {female}")
        else:
            print("\n⚠️ 无效选择，请重新输入！")

        input("\n按回车继续...")

if __name__ == "__main__":
    main()
