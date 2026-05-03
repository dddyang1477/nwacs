#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS V15 - 丰富的写作模板库
完整的开局、人设、情节、高潮、结尾等模板
"""

import sys
import os
import json
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

class WritingTemplateLibrary:
    """NWACS V15 写作模板库"""
    
    def __init__(self):
        print("="*80)
        print("📚 NWACS V15 - 写作模板库")
        print("="*80)
        
        # 开局模板
        self.opening_templates = {
            "xuanhuan": self.xuanhuan_openings(),
            "dushi": self.dushi_openings(),
            "yanqing": self.yanqing_openings(),
            "xuanyi": self.xuanyi_openings()
        }
        
        # 人设模板
        self.character_templates = {
            "male": self.male_characters(),
            "female": self.female_characters(),
            "villain": self.villain_characters()
        }
        
        # 情节模板
        self.plot_templates = {
            "face_slaps": self.face_slaps(),
            "reveals": self.reveals(),
            "battles": self.battles()
        }
        
        # 节奏模板
        self.rhythm_templates = self.rhythm_patterns()
        
        print(f"✅ 已加载 {len(self.opening_templates)} 种开局模板")
        print(f"✅ 已加载 {len(self.character_templates)} 种人设模板")
        print(f"✅ 已加载 {len(self.plot_templates)} 种情节模板")
        
        self.save_to_disk()
    
    def xuanhuan_openings(self):
        """玄幻开局模板"""
        return [
            {
                "name": "穿越觉醒",
                "structure": "穿越→苏醒→了解现状→发现金手指",
                "example": """林风猛地睁开眼睛，发现自己躺在一张破旧的木床上。
记忆如潮水般涌来——这里是青云大陆，一个修仙者的世界。
而他，是林家那个资质平庸的废柴三少爷！
突然，林风发现脑海里多了一个神秘的金色光团...""",
                "hooks": ["穿越重生", "废柴逆袭", "神秘金手指"],
                "scene_setting": "破屋/小院/柴房"
            },
            {
                "name": "退婚流",
                "structure": "家族大会→被退婚→受辱→发誓→发现金手指",
                "example": """"林辰，这婚，我们取消了。"
萧战拿着婚书，一脸轻蔑地看着林辰。
整个大厅的人都在嘲笑他，包括他曾经的未婚妻。
林辰攥紧拳头，指甲掐进掌心。
"三十年河东，三十年河西！"
就在这时，他胸口的玉佩突然发热...""",
                "hooks": ["退婚羞辱", "莫欺少年穷", "玉佩金手指"],
                "scene_setting": "家族大厅/正殿"
            },
            {
                "name": "系统流",
                "structure": "开篇介绍→系统激活→新手大礼包→第一次任务",
                "example": """苏阳坐在公园长椅上，吐槽着刚才看的小说。
"要是我有系统就好了..."他喃喃自语。
突然——
【叮！最强修仙系统已激活！】
【新手大礼包已发放：洗髓丹x1，筑基功法x1！】
苏阳愣住了，看着只有自己能看到的虚拟面板，疯狂大笑！""",
                "hooks": ["系统激活", "新手礼包", "从零开始"],
                "scene_setting": "公园/校园/家中"
            },
            {
                "name": "重生复仇",
                "structure": "死亡场景→重生回到过去→复仇目标→金手指/先知",
                "example": """火焰焚烧着夜轻羽的身体，敌人在狞笑。
"若有来生，我定要你们血债血偿！"
她带着无尽的怨恨，闭上了眼睛。
然后——
夜轻羽猛地睁开眼，回到了十年前！
一切都还来得及！""",
                "hooks": ["前世惨死", "重生归来", "复仇目标"],
                "scene_setting": "悬崖/火场/临死场景→重生到闺房/校园"
            }
        ]
    
    def dushi_openings(self):
        """都市开局模板"""
        return [
            {
                "name": "神医下山",
                "structure": "下山→遇麻烦→救人→展现实力",
                "example": """叶城走下火车，看着繁华的都市，有些茫然。
五年前他被师父带上山学医，现在终于出师了。
"小兄弟，你能救救我女儿吗？"
一个中年男人抱着一个浑身抽搐的女孩冲过来...""",
                "hooks": ["神医下山", "救人打脸", "深藏不露"],
                "scene_setting": "火车站/医院"
            },
            {
                "name": "赘婿逆袭",
                "structure": "在家受辱→出门办事→被人看不起→打脸",
                "example": """废物！"
岳母将一张纸扔在赵旭脸上："离婚协议书，签了吧！"
赵旭默默拿起笔。
三年了，他受够了。
就在这时，手机响起一个陌生号码："少爷，家族终于找到你了！"
从今天起，他赵旭，将不再是赘婿！""",
                "hooks": ["上门女婿", "离婚羞辱", "身份反转"],
                "scene_setting": "岳家/客厅"
            },
            {
                "name": "重生致富",
                "structure": "回到过去→利用先知→抓住机遇→赚钱",
                "example": """2008年8月8日。
张远看着墙上的日历，浑身颤抖。
他回来了！
回到了股市崩盘的一年前，回到了比特币一文不值的时候，回到了房价还没飞涨的时候！
这一世，他要成为世界首富！""",
                "hooks": ["时光倒流", "先知先觉", "致富密码"],
                "scene_setting": "卧室/教室/出租屋"
            },
            {
                "name": "规则怪谈",
                "structure": "发现规则→诡异开始→利用规则求生",
                "example": """林七夜站在精神病院的门前，手里握着一张纸条。
【规则一：不要回头！】
【规则二：如果看到护士的脸，请立即闭眼！】
【规则三：不要相信任何人的话！】
他深吸一口气，推开了那扇门...""",
                "hooks": ["诡异规则", "求生游戏", "心理惊悚"],
                "scene_setting": "医院/学校/公寓"
            }
        ]
    
    def yanqing_openings(self):
        """言情开局模板"""
        return [
            {
                "name": "久别重逢",
                "structure": "偶遇→对视→回忆→尴尬/心动",
                "example": """温以凡没想到会在这种地方遇到桑延。
咖啡厅的音乐突然变得暧昧，周围人的声音都远去了。
"好久不见。"他先开口，声音还是那么好听。
温以凡的心跳，漏了一拍。""",
                "hooks": ["久别重逢", "旧情复燃", "悸动"],
                "scene_setting": "咖啡厅/同学聚会/机场"
            },
            {
                "name": "先婚后爱",
                "structure": "领证→同房/同居→初遇尴尬→慢慢了解",
                "example": """顾小姐，从今天开始，我们就是合法夫妻了。"
顾兮兮看着结婚证上的照片，觉得像梦一样。
旁边的男人是她闪婚的对象，有钱，帅，但...冷得像块冰。
"住在一起，可以，但分房睡。"
他说。""",
                "hooks": ["闪婚协议", "先婚后爱", "同居生活"],
                "scene_setting": "民政局/婚房/酒店"
            },
            {
                "name": "萌宝助攻",
                "structure": "萌宝出场→遇到男主→神助攻",
                "example": """苏晚晚拖着行李箱走出机场，却撞上一个和儿子长得一模一样的小团子！
"妈咪！"小团子扑过来抱住她。
等一下，这是谁家的孩子？
就在这时，一个高大帅气的男人走过来，冷冷地盯着她："你是谁？为什么抱着我儿子？""",
                "hooks": ["萌宝神助攻", "父子神似", "带着娃跑"],
                "scene_setting": "机场/超市/公园"
            },
            {
                "name": "破镜重圆",
                "structure": "分手场景→多年后重逢→物是人非",
                "example": """七年后，苏念再次见到陆霆琛，是在他的订婚宴上。
他西装革履，身边站着美丽的未婚妻。
而她，是被请来的设计师。
"苏小姐，好久不见。"他开口，语气没有任何波澜。
苏念也笑："陆先生，好久不见。"
他们的故事，还没结束...""",
                "hooks": ["时隔多年", "订婚宴重逢", "旧情难忘"],
                "scene_setting": "订婚宴/公司/酒店"
            }
        ]
    
    def xuanyi_openings(self):
        """悬疑开局模板"""
        return [
            {
                "name": "凶案现场",
                "structure": "发现尸体→警察/侦探登场→发现第一个疑点",
                "example": """清晨的别墅区格外安静，直到一声尖叫打破了平静。
王警官赶到现场时，年轻的报案人还在发抖。
"死...死...死了..."
他看到了客厅中央的景象，瞳孔骤然收缩。
"保护现场！"
这不是普通的凶杀案...""",
                "hooks": ["密室杀人", "诡异现场", "悬念重重"],
                "scene_setting": "别墅/公寓/凶案现场"
            },
            {
                "name": "死亡预告",
                "structure": "收到预告→警告没人信→预言成真",
                "example": """收到那封信时，沈默以为是谁的恶作剧。
【今晚9点，你会死。】
荒谬！
然而，当晚上8点59分，沈默看着时间一分一秒逼近，心跳开始加速。
9点整——
窗外闪过一个黑影...""",
                "hooks": ["死亡预告", "倒计时", "恐慌"],
                "scene_setting": "家中/房间/独处环境"
            },
            {
                "name": "精神病人",
                "structure": "主角发现自己在精神病院→病友奇怪→规则浮现",
                "example": """林七夜醒来，发现自己在精神病院。
"欢迎来到青云疗养院，请记住以下规则..."
病友们举止诡异，医生态度可疑，墙上的规则一条条浮现。
必须遵守规则，否则...
会死！""",
                "hooks": ["规则怪谈", "精神病人", "生存游戏"],
                "scene_setting": "精神病院/疗养院"
            },
            {
                "name": "被冤枉入狱",
                "structure": "被冤枉入狱→在监狱中→真相线索浮现",
                "example": """谋杀！无期徒刑！
铁窗外是灰色的天空，铁窗内是令人窒息的冰冷。
林凡攥紧拳头："我没有杀人！"
一定有人陷害他！
而真相，就藏在这监狱的某处...""",
                "hooks": ["蒙冤入狱", "狱中求生", "寻找真相"],
                "scene_setting": "监狱/法庭"
            }
        ]
    
    def male_characters(self):
        """男性人设模板"""
        return [
            {
                "name": "冷酷大佬",
                "description": "背景强大，冷酷少言，但只对女主温柔",
                "tags": ["总裁", "大佬", "腹黑", "醋王"],
                "appearance": "身高188，长腿宽肩，面容俊美，眼神冰冷",
                "motivation": "占有欲，保护欲",
                "quote": "我的人，谁敢碰？"
            },
            {
                "name": "温润如玉",
                "description": "温柔体贴，家境好，对女主百般呵护",
                "tags": ["温柔", "体贴", "儒雅", "治愈"],
                "appearance": "清俊干净，气质温润，戴眼镜",
                "motivation": "守护女主",
                "quote": "有我在。"
            },
            {
                "name": "邪魅狂狷",
                "description": "霸道张扬，气势逼人，又撩又苏",
                "tags": ["霸道", "张扬", "邪魅", "撩"],
                "appearance": "俊美非凡，眼神带笑，气场强大",
                "motivation": "征服女主",
                "quote": "女人，你逃不掉的。"
            },
            {
                "name": "禁欲系",
                "description": "清冷克制，禁欲老干部风",
                "tags": ["禁欲", "克制", "老干部", "清冷"],
                "appearance": "清冷禁欲，正装革履",
                "motivation": "被女主打破原则",
                "quote": "..."
            }
        ]
    
    def female_characters(self):
        """女性人设模板"""
        return [
            {
                "name": "飒爽大女主",
                "description": "独立坚强，能力强，不恋爱脑",
                "tags": ["飒", "独立", "强大", "事业批"],
                "appearance": "高挑，气质冷艳，短发/高马尾",
                "motivation": "搞事业",
                "quote": "爱情算什么，搞钱最重要！"
            },
            {
                "name": "软萌治愈",
                "description": "可爱甜美，温暖治愈，容易激起保护欲",
                "tags": ["软萌", "治愈", "可爱", "甜美"],
                "appearance": "圆圆脸，大眼睛，笑起来有酒窝",
                "motivation": "过简单的生活",
                "quote": "你要吃糖吗？"
            },
            {
                "name": "腹黑心机",
                "description": "外表清纯，内心腹黑，有仇必报",
                "tags": ["腹黑", "心机", "复仇", "白切黑"],
                "appearance": "清纯无害，眼神清冷",
                "motivation": "复仇",
                "quote": "欠了我的，总要还的。"
            },
            {
                "name": "温柔坚韧",
                "description": "外柔内刚，温柔但不软弱",
                "tags": ["温柔", "坚韧", "外柔内刚"],
                "appearance": "柔和漂亮，气质温和",
                "motivation": "保护家人/事业",
                "quote": "我很好，谢谢你关心。"
            }
        ]
    
    def villain_characters(self):
        """反派人设模板"""
        return [
            {
                "name": "白莲花女配",
                "description": "外表清纯无辜，内心恶毒，喜欢挑拨离间",
                "trigger": "嫉妒女主",
                "tactics": ["挑拨离间", "装可怜", "陷害女主"]
            },
            {
                "name": "纨绔反派",
                "description": "嚣张跋扈，欺软怕硬，被打脸后变本加厉",
                "trigger": "挑衅失败",
                "tactics": ["找麻烦", "动用关系", "阴谋诡计"]
            },
            {
                "name": "伪善反派",
                "description": "表面和善，内心阴暗",
                "trigger": "被揭穿",
                "tactics": ["利用他人", "借刀杀人", "伪装"]
            }
        ]
    
    def face_slaps(self):
        """打脸情节模板"""
        return [
            {
                "name": "身份暴露",
                "pattern": "被看不起→身份曝光→对方震惊后悔",
                "example": """这个穷酸小子是谁带来的？"
"就是，衣服都是地摊货吧？"
没人知道，眼前这个被嘲笑的年轻人，就是他们刚才讨论的神秘大佬...""",
                "tips": ["先抑后扬", "层层递进", "众人反应"]
            },
            {
                "name": "实力打脸",
                "pattern": "被挑衅→答应比试→展露实力→震惊",
                "example": """你敢跟我比吗？"
"可以。"
然后，所有人都震惊地看着那个刚才还被轻视的身影，爆发出恐怖的实力...""",
                "tips": ["先铺垫对手", "反差要大", "旁观者反应"]
            },
            {
                "name": "打脸白莲花",
                "pattern": "白莲花装可怜→女主拆穿→白莲花真面目暴露",
                "example": """姐姐，我不是故意的...""
"装什么装？"
女主当众拆穿白莲花的伪装，让所有人看清她的真面目...""",
                "tips": ["证据确凿", "逻辑清晰", "白莲花表情变化"]
            }
        ]
    
    def reveals(self):
        """揭秘情节模板"""
        return [
            {
                "name": "身份揭秘",
                "pattern": "隐藏身份→慢慢铺垫→最终揭示",
                "timing": "前期铺垫，中期暗示，后期揭晓"
            },
            {
                "name": "真相大白",
                "pattern": "疑点→调查→反转→真相",
                "timing": "每一个节点都要有新发现"
            }
        ]
    
    def battles(self):
        """战斗情节模板"""
        return [
            {
                "name": "小高潮战斗",
                "pattern": "冲突升级→主角遇险→爆发金手指→胜利",
                "timing": "每10章一个"
            },
            {
                "name": "大高潮战斗",
                "pattern": "前期铺垫→双方准备→激烈对决→结局",
                "timing": "每50章一个"
            }
        ]
    
    def rhythm_patterns(self):
        """节奏模板"""
        return {
            "xuanhuan": {
                "pattern": "开篇→升级→秘境→复仇→再升级→终极决战",
                "key_points": ["第1章钩子", "第5-10章第一个小高潮", "第30-50章大高潮"]
            },
            "dushi": {
                "pattern": "开篇打脸→发展事业→感情升温→危机→解决危机→圆满",
                "key_points": ["第1章打脸", "第10-20章事业起步", "第50-100章感情确定"]
            },
            "yanqing": {
                "pattern": "相遇→试探→误会→解开→表白→考验→圆满",
                "key_points": ["第1章相遇", "第10-30章感情升温", "第50-100章误会与解开"]
            },
            "xuanyi": {
                "pattern": "案发→调查→疑点→反转→真相",
                "key_points": ["第1章案发", "每5-10章一个新线索", "每30-50章一个重大反转"]
            }
        }
    
    def show_templates(self, category):
        """显示模板"""
        print(f"\n📋 {category} 模板:")
        if category in self.opening_templates:
            for i, template in enumerate(self.opening_templates[category]):
                print(f"\n  {i+1}. {template['name']}")
                print(f"     钩子: {', '.join(template['hooks'])}")
                print(f"     场景: {template['scene_setting']}")
    
    def demo(self):
        """演示"""
        print("\n" + "="*80)
        print("📚 模板库演示")
        print("="*80)
        
        categories = ["xuanhuan", "dushi", "yanqing", "xuanyi"]
        for cat in categories:
            self.show_templates(cat)
        
        print("\n" + "="*80)
        print("✅ 模板库演示完成！")
        print("="*80)
    
    def save_to_disk(self):
        """保存"""
        save_data = {
            "opening_templates": self.opening_templates,
            "character_templates": self.character_templates,
            "plot_templates": self.plot_templates,
            "rhythm_templates": self.rhythm_templates,
            "version": "V15",
            "saved_at": datetime.now().isoformat()
        }
        
        filename = "writing_templates_v15.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 模板库已保存到: {filename}")


def main():
    """主程序"""
    library = WritingTemplateLibrary()
    library.demo()


if __name__ == "__main__":
    main()
