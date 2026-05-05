#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS V15 - 完整开局示例库
基于2026年最新爆款公式：冲突前置+人设反差+金句钩子
每个题材多案例完整示例
"""

import sys
import os
import json
from datetime import datetime

try:
    sys.stdout.reconfigure(encoding='utf-8')
except (AttributeError, OSError):
    pass

class OpeningExamplesLibrary:
    """NWACS V15 完整开局示例库"""
    
    def __init__(self):
        print("="*80)
        print("📖 NWACS V15 - 完整开局示例库")
        print("="*80)
        
        # 玄幻开局示例
        self.xuanhuan_openings = self.load_xuanhuan_openings()
        
        # 都市开局示例
        self.dushi_openings = self.load_dushi_openings()
        
        # 言情开局示例
        self.yanqing_openings = self.load_yanqing_openings()
        
        # 悬疑开局示例
        self.xuanyi_openings = self.load_xuanyi_openings()
        
        print(f"✅ 已加载 {len(self.xuanhuan_openings)} 个玄幻开局")
        print(f"✅ 已加载 {len(self.dushi_openings)} 个都市开局")
        print(f"✅ 已加载 {len(self.yanqing_openings)} 个言情开局")
        print(f"✅ 已加载 {len(self.xuanyi_openings)} 个悬疑开局")
        
        self.save_to_disk()
    
    def load_xuanhuan_openings(self):
        """加载玄幻开局示例"""
        return [
            {
                "title": "第1章：废物新生",
                "formula": "退婚流+冲突前置",
                "content": """"这婚，退定了。"
萧战将婚书拍在桌上，眼神冰冷。
林辰攥紧拳头，指甲嵌进掌心。
整个大厅的人都在嘲笑他——林家那个修炼三年还在淬体一重的废物，居然敢肖想萧家千金？
"三日后，我会让你亲自来求我收回这句话。"
林辰的声音很轻，却让所有人都愣住了。
萧战冷笑："就凭你？"
林辰没有回答，只是在心里默念：三天后，我会让你们知道，什么叫莫欺少年穷。
当晚，他的脑海里突然亮起一道金光——""",
                "analysis": {
                    "conflict": "退婚羞辱，冲突前置",
                    "golden_hook": "三日后，我会让你亲自来求我收回这句话",
                    "golden_finger": "脑海金光（系统/传承）",
                    "reader_expectation": "期待打脸"""
                }
            },
            {
                "title": "第1章：系统激活",
                "formula": "系统流+冲突前置",
                "content": """【叮！最强修仙系统已激活！】
【检测到宿主被未婚妻当众退婚，激活条件已满足！】
【新手大礼包已发放：洗髓丹x1，筑基功法x1，神秘老爷爷x1！】
林辰愣愣地看着脑海中突然出现的金色面板。
三分钟前，他还在被整个萧家嘲笑。
三分钟后，他的人生彻底改变了。
"从今天起，我不再是废物。"
林辰攥紧拳头，眼里闪过一丝凌厉的光。
萧家，你们等着！""",
                "analysis": {
                    "conflict": "被退婚+系统激活",
                    "golden_hook": "新手大礼包已发放！",
                    "golden_finger": "最强修仙系统",
                    "reader_expectation": "期待逆袭打脸"""
                }
            },
            {
                "title": "第1章：重生复仇",
                "formula": "重生流+人设反差",
                "content": """火焰焚烧着夜轻羽的身体。
她看着曾经深爱的男人搂着另一个女人狞笑，看着自己一手创立的势力被瓜分殆尽。
"若有来生，我定要你们血债血偿！"
十年后。
夜轻羽猛地睁开眼睛，发现自己躺在熟悉的闺房里。
窗外，丫鬟正在敲门："小姐，萧家来退婚了！"
她愣住了——这是，十六岁那年？
她没有像上一世那样哭闹，而是站起身，嘴角微微上扬：
"退婚？好啊。让他们在客厅等着。"
这一世，她要让那些人知道，什么叫真正的王者归来。""",
                "analysis": {
                    "conflict": "前世惨死+重生回到过去",
                    "golden_hook": "若有来生，我定要你们血债血偿",
                    "golden_finger": "前世记忆+复仇目标明确",
                    "reader_expectation": "期待复仇打脸"""
                }
            },
            {
                "title": "第1章：禁地奇遇",
                "formula": "禁地流+冲突前置",
                "content": """"那个废物居然敢进禁地？"
"找死吧他！禁地里有上古凶兽，进去就别想出来！"
林尘没有理会身后的嘲笑，径直踏入了禁地。
他知道自己只有三天时间——三天后，家族大比，如果他还是垫底，就会被逐出家门。
禁地里危机四伏，但他不怕。
因为他的脑海里，有一卷神秘功法。
那是他十年前在一处古迹中得到的东西。
"既然你们觉得我废物，那我就废物给你们看。"
林尘低吼一声，踏入了禁地深处。""",
                "analysis": {
                    "conflict": "被嘲笑+禁地冒险",
                    "golden_hook": "进去就别想出来",
                    "golden_finger": "神秘功法",
                    "reader_expectation": "期待禁地逆袭"""
                }
            }
        ]
    
    def load_dushi_openings(self):
        """加载都市开局示例"""
        return [
            {
                "title": "第1章：神医下山",
                "formula": "身份反差+冲突前置",
                "content": """"让开！都让开！病人快不行了！"
医院走廊里，一个中年男人抱着浑身抽搐的小女孩冲进来。
所有人都在摇头——这病，没救了。
叶城站在角落里，看着这一幕，嘴角微微上扬。
五年前，他被师父带上山学医。
五年后的今天，他终于可以出手了。
"让我看看。"
他走上前，手指轻轻搭在小女孩的脉搏上。
"不过是中了寒毒，我三针就能解决。"
整个走廊鸦雀无声。
然后，叶城从怀里掏出银针——""",
                "analysis": {
                    "conflict": "绝症+神医出手",
                    "golden_hook": "不过寒毒，我三针就能解决",
                    "golden_finger": "神秘医术",
                    "reader_expectation": "期待打脸震惊"""
                }
            },
            {
                "title": "第1章：赘婿觉醒",
                "formula": "身份反转+情绪张力",
                "content": """"离婚协议书签了，滚吧。"
岳母将一张纸扔在赵旭脸上。
三年了。
他在苏家当了三年上门女婿，受尽屈辱，换来的就是这样一句话。
赵旭默默捡起笔。
就在这时，他的手机响了。
"少爷，家族终于找到您了！老爷说，您是赵家唯一的继承人..."
赵旭愣住了。
他看着手里的离婚协议书，又看了看手机。
然后，他笑了。
"离婚？"
他将协议书撕成碎片，站起身来。
"现在，该轮到我不要你们了。'""",
                "analysis": {
                    "conflict": "被离婚+身份曝光",
                    "golden_hook": "现在，该轮到我不要你们了",
                    "golden_finger": "豪门继承人身份",
                    "reader_expectation": "期待强势打脸"""
                }
            },
            {
                "title": "第1章：规则怪谈",
                "formula": "规则流+悬念前置",
                "content": """【规则一：不要回头】
【规则二：如果看到护士的脸，请立即闭眼】
【规则三：不要相信任何人的话】
【规则四：每晚12点必须熄灯】
林七夜盯着手机里的这条消息，头皮发麻。
他是一名精神科医生，三天前被调来这家疗养院工作。
但他很快发现，这里的病人不太对劲。
他们总是用奇怪的眼神看着他。
他们总是说一些莫名其妙的话。
而墙上贴的那些规则...好像，每一条都在保护什么东西。
"新来的医生？"
一个护士突然出现在他身后。
林七夜的心猛地一紧——""",
                "analysis": {
                    "conflict": "规则怪谈+诡异疗养院",
                    "golden_hook": "不要相信任何人的话",
                    "golden_finger": "规则背后的真相",
                    "reader_expectation": "期待恐怖揭秘"""
                }
            },
            {
                "title": "第1章：捞尸人",
                "formula": "职业流+悬念前置",
                "content": """河面上，一个身影漂浮着。
"又捞上来一个。"
陈九蹲在岸边，看着打捞上来的尸体，面无表情。
他是一个捞尸人，在这个行业干了十年。
但今天这具尸体...不太对劲。
尸体保持着微笑，嘴角上扬，像是睡着了一样。
但陈九知道，这个人不是溺水死的。
他是被吓死的。
就在陈九准备收工的时候，尸体的眼睛突然睁开了——
"终于...有人来了..."
陈九愣住了。
因为他认识这个人。
这是他失踪三年的弟弟。""",
                "analysis": {
                    "conflict": "捞尸遇到弟弟+恐怖悬疑",
                    "golden_hook": "终于有人来了",
                    "golden_finger": "弟弟的死因真相",
                    "reader_expectation": "期待恐怖揭秘"""
                }
            }
        ]
    
    def load_yanqing_openings(self):
        """加载言情开局示例"""
        return [
            {
                "title": "第1章：破镜重逢",
                "formula": "久别重逢+情绪张力",
                "content": """七年了。
温以凡没想到会在这种地方遇到桑延。
咖啡厅的音乐很轻，灯光昏暗，一切都像极了七年前那个夜晚。
"好久不见。"他先开口，声音还是那么好听。
温以凡端着咖啡杯的手微微一颤。
"好久不见。"
七年前，他们因为一场误会分手。
七年后，她以为早就忘了他。
但此刻看着他的眼睛，她才发现，有些东西从来没变。
"这些年，你过得好吗？"他问。
温以凡笑了笑，眼眶却有些湿润："挺好的，你呢？"
他没有回答，只是看着她，目光深沉。
"以凡，我...'""",
                "analysis": {
                    "conflict": "七年重逢+旧情难忘",
                    "golden_hook": "我...",
                    "golden_finger": "七年前的误会真相",
                    "reader_expectation": "期待复合"""
                }
            },
            {
                "title": "第1章：先婚后爱",
                "formula": "协议婚姻+冲突前置",
                "content": """"从今天起，我们就是合法夫妻了。"
顾兮兮看着手里的结婚证，有些恍惚。
三天前，她还是顾家不受待见的大小姐。
三天后，她成了陆家少奶奶。
当然，这只是名义上的。
"形婚，各过各的，不要干涉对方。"陆霆琛冷冷地说。
顾兮兮点头："没问题。"
她知道他为什么娶她——为了她手里的股份。
她也知道自己为什么嫁他——为了报复继母。
两个各怀心思的人，就这样成了夫妻。
但他们都不知道，命运的齿轮，已经开始转动。""",
                "analysis": {
                    "conflict": "形婚+各怀心思",
                    "golden_hook": "命运的齿轮已经开始转动",
                    "golden_finger": "两人隐藏的秘密",
                    "reader_expectation": "期待假戏真做"""
                }
            },
            {
                "title": "第1章：萌宝助攻",
                "formula": "萌宝+身份错位",
                "content": """"妈咪！"
一个奶声奶气的声音从身后传来。
苏晚晚愣住了——她还没结婚，哪来的孩子？
然后，她看到了一个长得和某人几乎一模一样的小团子朝她扑过来。
"找到了！爹地说了，找到妈咪就给我们一百万！"
苏晚晚："？？？"
她蹲下身，看着这张熟悉的小脸，心跳加速。
这孩子...怎么跟她前男友长得一模一样？
就在这时，一辆黑色宾利停在路边。
车门打开，一个高大的男人走下来——
苏晚晚愣住了。
那是...她五年前分手的初恋？""",
                "analysis": {
                    "conflict": "萌宝找妈咪+前男友出现",
                    "golden_hook": "找到妈咪就给我们一百万",
                    "golden_finger": "孩子是谁的？",
                    "reader_expectation": "期待甜蜜纠葛"""
                }
            },
            {
                "title": "第1章：暗恋成真",
                "formula": "暗恋+甜宠",
                "content": """整个图书馆安静得只能听见翻书声。
苏念念偷偷抬起眼，看向对面那个专注看书的男生。
他叫陆星河，是学校出了名的学神。
而她，只是一个普普通通的女生。
她暗恋他三年，从没敢表白。
但今天，她决定做一件疯狂的事。
她拿出一张纸条，写了几个字，然后鼓起勇气走过去，将纸条放在他面前。
然后，她转身就跑。
陆星河抬起头，看着那个逃跑的背影，嘴角微微上扬。
他拿起纸条，上面写着：
"我喜欢你，可以认识你吗？"
他站起身，朝门口走去——""",
                "analysis": {
                    "conflict": "暗恋表白+逃跑",
                    "golden_hook": "他站起身，朝门口走去",
                    "golden_finger": "他会接受吗？",
                    "reader_expectation": "期待甜蜜恋爱"""
                }
            }
        ]
    
    def load_xuanyi_openings(self):
        """加载悬疑开局示例"""
        return [
            {
                "title": "第1章：死亡预告",
                "formula": "倒计时+悬念前置",
                "content": """【今晚9点，你将会死。】
苏默盯着手机屏幕上的这条消息，冷汗直流。
他以为是恶作剧，但很快发现不对——
发消息的号码，是他自己三个月后的手机号。
"神经病。"他骂了一句，关掉手机。
但那天晚上8点59分，他鬼使神差地看向窗外。
然后，他看到了一个人影站在对面楼顶。
下一秒，那个人跳了下去——
正好砸在他家的阳台上。
血溅了一地。
苏默看清了那张脸。
那是...他自己。""",
                "analysis": {
                    "conflict": "死亡预告+亲眼看到自己死亡",
                    "golden_hook": "那是...他自己",
                    "golden_finger": "如何改变命运？",
                    "reader_expectation": "期待悬疑揭秘"""
                }
            },
            {
                "title": "第1章：双重人格",
                "formula": "人格分裂+悬念",
                "content": """"不是我杀的！真的不是我！"
审讯室里，林夏歇斯底里地喊着。
但所有证据都指向她——她的指纹，她的动机，她是最后一个见到死者的人。
问题是，她根本不记得那晚发生了什么。
她只记得自己8点就睡了，第二天醒来时满身是血。
"林小姐，"警官递过来一张照片，"认识这个人吗？"
林夏愣住了。
照片上的人...和她长得一模一样。
"但这个人，在三年前就已经死了。"
林夏感觉脑子里有什么东西"嗡"地一声炸开了。""",
                "analysis": {
                    "conflict": "被诬陷+双重人格嫌疑",
                    "golden_hook": "这个人，在三年前就已经死了",
                    "golden_finger": "另一个人格的真相",
                    "reader_expectation": "期待悬疑反转"""
                }
            },
            {
                "title": "第1章：不在场证明",
                "formula": "推理+时间线",
                "content": """"张总死了，死在自己的办公室里。"
王警官看着现场，眉头紧锁。
死者的电脑屏幕上，还停留在一份未发送的邮件上。
"死亡时间是晚上9点到10点之间。"
"不可能！"死者的秘书坚定地说，"9点的时候，我还接到张总的电话！"
但王警官注意到一个细节——
秘书的手腕上，有一道新鲜的抓痕。
"这道伤是怎么来的？"他问。
秘书的脸色瞬间变了。
就在这时，法医走过来低声说：
"王警官，死者的胃里发现了大量安眠药。'""",
                "analysis": {
                    "conflict": "不可能的犯罪+证据矛盾",
                    "golden_hook": "死者胃里发现了大量安眠药",
                    "golden_finger": "真相是什么？",
                    "reader_expectation": "期待推理揭秘"""
                }
            },
            {
                "title": "第1章：精神分裂",
                "formula": "现实扭曲+心理悬疑",
                "content": """我总觉得有人在跟踪我。
但每次回头，都什么都没有。
医生说这是精神分裂的早期症状。
但我知道不是。
因为今天，我在家里发现了一本日记。
那本日记的字迹，和我的一模一样。
但我从来没见过这本日记。
"不要相信任何人。"
日记的第一页这样写道。
我颤抖着翻开第二页——
上面写着我的名字，还有我的住址。
以及一行字：
"她已经开始怀疑了。'""",
                "analysis": {
                    "conflict": "日记证明有人冒充自己",
                    "golden_hook": "她已经开始怀疑了",
                    "golden_finger": "谁是幕后黑手？",
                    "reader_expectation": "期待恐怖揭秘"""
                }
            }
        ]
    
    def get_opening(self, genre, index=0):
        """获取指定开局"""
        openings_map = {
            "xuanhuan": self.xuanhuan_openings,
            "dushi": self.dushi_openings,
            "yanqing": self.yanqing_openings,
            "xuanyi": self.xuanyi_openings
        }
        
        openings = openings_map.get(genre, [])
        
        if 0 <= index < len(openings):
            return openings[index]
        
        return None
    
    def show_opening(self, genre, index=0):
        """显示开局示例"""
        opening = self.get_opening(genre, index)
        
        if not opening:
            print(f"\n⚠️ 未找到{genre}类型的第{index+1}个开局")
            return
        
        print(f"\n" + "="*80)
        print(f"📖 {opening['title']}")
        print(f"📝 公式: {opening['formula']}")
        print("="*80)
        
        print(f"\n【正文】\n")
        print(opening['content'])
        
        print(f"\n【分析】")
        analysis = opening['analysis']
        print(f"   冲突: {analysis['conflict']}")
        print(f"   金句钩子: {analysis['golden_hook']}")
        print(f"   金手指: {analysis['golden_finger']}")
        print(f"   读者期待: {analysis['reader_expectation']}")
    
    def show_all_openings(self, genre):
        """显示所有开局"""
        openings_map = {
            "xuanhuan": self.xuanhuan_openings,
            "dushi": self.dushi_openings,
            "yanqing": self.yanqing_openings,
            "xuanyi": self.xuanyi_openings
        }
        
        openings = openings_map.get(genre, [])
        
        if not openings:
            print(f"\n⚠️ 未找到{genre}类型的开局")
            return
        
        print(f"\n" + "="*80)
        print(f"📚 {genre}类型开局示例（共{len(openings)}个）")
        print("="*80)
        
        for i, opening in enumerate(openings):
            print(f"\n{i+1}. 【{opening['title']}】")
            print(f"   公式: {opening['formula']}")
            print(f"   钩子: {opening['analysis']['golden_hook']}")
    
    def demo(self):
        """演示"""
        print("\n" + "="*80)
        print("📖 开局示例库演示")
        print("="*80)
        
        genres = ["xuanhuan", "dushi", "yanqing", "xuanyi"]
        
        for genre in genres:
            self.show_all_openings(genre)
        
        print("\n" + "="*80)
        print("📖 详细内容示例")
        print("="*80)
        
        self.show_opening("xuanhuan", 0)
        self.show_opening("dushi", 0)
        self.show_opening("yanqing", 0)
        self.show_opening("xuanyi", 0)
        
        print("\n" + "="*80)
        print("✅ 演示完成!")
        print("="*80)
    
    def save_to_disk(self):
        """保存"""
        save_data = {
            "xuanhuan_openings": self.xuanhuan_openings,
            "dushi_openings": self.dushi_openings,
            "yanqing_openings": self.yanqing_openings,
            "xuanyi_openings": self.xuanyi_openings,
            "version": "V15",
            "saved_at": datetime.now().isoformat(),
            "source": "2026联网学习爆款开局"
        }
        
        filename = "opening_examples_library_v15.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 开局示例库已保存到: {filename}")


def main():
    """主程序"""
    library = OpeningExamplesLibrary()
    library.demo()


if __name__ == "__main__":
    main()
