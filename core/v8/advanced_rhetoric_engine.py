#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 高级修辞与文体引擎 - AdvancedRhetoricEngine

全网深度学习精华蒸馏：
- 国内：知乎/龙空/豆瓣/今日头条/CSDN/中国作家网
- 国际：Writer's Digest/Reddit/Medium/ResearchGate/Fiveable
- AI检测对抗：GPTZero 7组件检测原理/Perplexity/Burstiness/HIL Perturbations

核心目标：将AI检测率压制到5%以下，人工特征占比95%+
"""

import json
import os
import re
import random
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


API_KEY = "sk-f3246fbd1eef446e9a11d78efefd9bba"
BASE_URL = "https://api.deepseek.com"


class RhetoricCategory(Enum):
    SENTENCE_CRAFT = "句式工艺"        # 长短句/排比/对偶/回文
    SENSORY_DEPTH = "感官深度"        # 五感/通感/感官轰炸
    FIGURE_SPEECH = "修辞格"          # 比喻/拟人/夸张/借代
    NARRATIVE_VOICE = "叙事声音"      # 视角/语气/主观性
    EMOTION_MAPPING = "情绪映射"      # 外化/光影/环境折射
    DIALOGUE_CRAFT = "对话工艺"       # 潜台词/钩子/动作标签
    PACING_RHYTHM = "节奏韵律"        # 快慢/张弛/段落呼吸
    WHITE_SPACE_ART = "留白艺术"      # 暗示/省略/临界点
    DETAIL_ANCHOR = "细节锚定"        # 特指/物件/品牌/数字
    IMPERFECTION = "不完美美学"       # 口语/停顿/冗余/语法瑕疵
    AI_EVASION = "AI检测规避"         # Perplexity/Burstiness对抗
    CULTURAL_TEXTURE = "文化肌理"     # 方言/俚语/时代感/烟火气


@dataclass
class RhetoricTechnique:
    name: str
    category: str
    description: str
    rules: List[str]
    examples: List[Dict[str, str]]
    source: str
    confidence: float
    ai_evasion_power: int  # 1-10, 对AI检测的规避能力


RHETORIC_TECHNIQUES: Dict[str, RhetoricTechnique] = {}

def _register(tech: RhetoricTechnique):
    RHETORIC_TECHNIQUES[tech.name] = tech
    return tech


# ============================================================
# 句式工艺 (Sentence Craft)
# ============================================================

_register(RhetoricTechnique(
    name="匕首句法",
    category=RhetoricCategory.SENTENCE_CRAFT.value,
    description="文字是匕首不是棉被。舍弃一切'看起来很美但没用'的描写，只保留推动情节或刻画人性的文字。血淋淋的真实感 > 朦胧的诗意。",
    rules=[
        "每句问自己：删掉这句，故事还成立吗？不成立才保留",
        "用动词替代形容词：'她害怕地后退'→'她撞上墙根'",
        "砍掉'的''了''然后'：原句精简30%以上",
        "一个精准动词胜过三个形容词",
        "短篇小说尤其：用最少的字，捅最深的刀",
    ],
    examples=[
        {
            "before": "月光如水般倾泻在她苍白的脸上，她望着那扇紧闭的门，仿佛听见了命运的回声。",
            "after": "月光刺在她脸上，她盯着那扇门——里面藏着她偷走的十万块钱。",
        },
        {
            "before": "她拿着钥匙，打开了那扇生了锈的门，走了进去，发现里面一片漆黑。",
            "after": "钥匙插进锁孔，铁门吱呀洞开。黑暗吞没她时，她听见身后传来锁舌咬合的脆响。",
        },
    ],
    source="今日头条·短篇小说文笔指南",
    confidence=0.95,
    ai_evasion_power=9,
))

_register(RhetoricTechnique(
    name="长短句呼吸法·进阶",
    category=RhetoricCategory.SENTENCE_CRAFT.value,
    description="人类写作的自然'爆发性'(Burstiness)：长句铺陈后紧跟短句爆发。AI文本句长均匀如节拍器，人类文本句长起伏如呼吸。GPTZero核心检测指标之一。",
    rules=[
        "30%短句(3-10字) + 50%中句(11-25字) + 20%长句(26-50字)",
        "连续3句不能长度相近(差距<5字即为相近)",
        "关键情节用单句成段：'刀光。' 独立成段制造冲击",
        "抒情段落用长句铺陈，但结尾必须用短句收住",
        "GPTZero检测burstiness：句长方差越大越像人类",
    ],
    examples=[
        {
            "before": "战斗非常激烈，双方你来我往，打了很久才分出胜负。",
            "after": "刀光。\n他侧身——慢了半拍。肩头一凉，血飙出来。\n退。再退。后背撞上墙。\n没路了。\n他咧嘴。牙缝里全是血。然后冲出去。",
        },
    ],
    source="GPTZero Burstiness对抗研究 + 知乎写作社区",
    confidence=0.96,
    ai_evasion_power=10,
))

_register(RhetoricTechnique(
    name="排比爆破法",
    category=RhetoricCategory.SENTENCE_CRAFT.value,
    description="用短句+排比制造朗朗上口的节奏感，同时打破AI均匀句式。三句排比后跟一个反转型短句。",
    rules=[
        "排比三句，每句不超过12字",
        "排比后紧跟一个反转型短句(5-8字)",
        "排比内容要有递进：动作→情绪→反转",
        "避免AI式'一方面...另一方面...'的假排比",
    ],
    examples=[
        {
            "before": "在面对困难、挫折和挑战时，我们要保持积极心态。",
            "after": "遇到坎儿，别怂。遇到事儿，别慌。遇到人，别装。\n但遇到她——全白搭。",
        },
    ],
    source="今日头条·去AI味实操指南",
    confidence=0.92,
    ai_evasion_power=8,
))

_register(RhetoricTechnique(
    name="回文钩子法",
    category=RhetoricCategory.SENTENCE_CRAFT.value,
    description="Chiasmus(回文/交错配列)：'Ask not what your country can do for you, ask what you can do for your country.' 中文版：前后句结构颠倒，制造思维回环。AI几乎不会使用此结构。",
    rules=[
        "前句A→B，后句B→A",
        "中文示例：'不是你选择了命运，是命运选择了你'",
        "每3000字至少1处回文结构",
        "回文后紧跟留白，让读者回味",
    ],
    examples=[
        {
            "before": "他为了力量放弃了人性，最终发现力量毫无意义。",
            "after": "他以为力量能换回人性。后来才懂——人性，才能换回力量。",
        },
    ],
    source="Writer's Digest + Fiveable Literary Devices",
    confidence=0.90,
    ai_evasion_power=9,
))


# ============================================================
# 感官深度 (Sensory Depth)
# ============================================================

_register(RhetoricTechnique(
    name="感官轰炸法",
    category=RhetoricCategory.SENSORY_DEPTH.value,
    description="用环境细节折射心理，比直白抒情高级100倍。不写'她很慌'，写'冷汗浸透睡衣后背，楼下保安巡楼的脚步声突然停在楼梯间'。",
    rules=[
        "禁止直接陈述情绪，用感官细节替代",
        "每场景至少3种感官(视觉+听觉+触觉/嗅觉)",
        "感官细节必须绑定情节推进",
        "声音分层：前景声(对话/动作)+环境声(风声/雨声)+内心声",
        "嗅觉是记忆触发器：某种气味瞬间拉回回忆",
    ],
    examples=[
        {
            "before": "她心里很慌。",
            "after": "冷汗浸透睡衣后背。楼下保安巡楼的脚步声——突然停在楼梯间。她屏住呼吸。三秒。五秒。脚步声又响了，往上去。她瘫在门板上，腿软得像两团泥。",
        },
    ],
    source="今日头条·短篇小说文笔指南 + Fiveable Sensory Writing",
    confidence=0.94,
    ai_evasion_power=9,
))

_register(RhetoricTechnique(
    name="通感联觉法",
    category=RhetoricCategory.SENSORY_DEPTH.value,
    description="将五感相互转化，产生新奇效果。'她的笑声像一串风铃在阳光下闪烁'(听觉→视觉)。张爱玲、朱自清经典技法。AI几乎不会使用通感。",
    rules=[
        "每章至少1处通感修辞",
        "通感方向：听觉→视觉、嗅觉→触觉、视觉→听觉",
        "通感需与情绪绑定：悲伤时用冷色调通感",
        "避免生硬：'声音像光线'比'声音像颜色'更自然",
    ],
    examples=[
        {
            "before": "她发出了银铃般的笑声。",
            "after": "她的笑声清脆，像一串风铃在阳光下闪烁。",
        },
        {
            "before": "微风送来清香。",
            "after": "微风过处，送来缕缕清香，仿佛远处高楼上渺茫的歌似的。",
        },
    ],
    source="朱自清《荷塘月色》+ 张爱玲研究 + 网易写作计划",
    confidence=0.93,
    ai_evasion_power=10,
))


# ============================================================
# 修辞格 (Figures of Speech)
# ============================================================

_register(RhetoricTechnique(
    name="化虚为实比喻法",
    category=RhetoricCategory.FIGURE_SPEECH.value,
    description="钱钟书：'比喻是文学语言的根本。'将抽象概念(愁/时光/命运)比作具体可感之物。化虚为实是基础，化实为虚是进阶。",
    rules=[
        "抽象情绪→具体物象：'愁'→'一川烟草，满城风絮，梅子黄时雨'",
        "具体物象→抽象意境：'飞花'→'梦'，'丝雨'→'愁'",
        "比喻要有新鲜感，避免'像花朵一样美丽'等陈词",
        "每个比喻服务于当前场景的情绪基调",
    ],
    examples=[
        {
            "before": "他非常忧愁。",
            "after": "他的愁像梅雨季的墙——湿漉漉的，一层层剥落，露出里面灰黑的砖。",
        },
        {
            "before": "普通人的一生很平凡。",
            "after": "普通人的一生，再好些也是'桃花扇'，撞破了头，血溅到扇子上，就这上面略加点染成为一枝桃花。",
        },
    ],
    source="张爱玲《红玫瑰与白玫瑰》+ 钱钟书 + 大众新闻",
    confidence=0.95,
    ai_evasion_power=9,
))

_register(RhetoricTechnique(
    name="拟人活化法",
    category=RhetoricCategory.FIGURE_SPEECH.value,
    description="为没有生命的物体赋予生命，把静止状态转为正在进行的动作。'开水壶在发警报''尘埃在光柱中浮动'。让画面跃然纸上。",
    rules=[
        "每场景至少1处拟人",
        "拟人需有叙事功能，不是纯装饰",
        "用动词驱动拟人：'风灌进来''黑暗吞没她'",
        "拟人方向与情绪一致：悲伤场景用压抑拟人",
    ],
    examples=[
        {
            "before": "水壶里的水烧开了，冒出了热气。",
            "after": "耳边忽然传来咕咚咕咚翻滚的响声，原来是开水壶在发警报。",
        },
        {
            "before": "房间里很暗。",
            "after": "黑暗蹲在墙角，像一只耐心的猫——等着她迈出第一步。",
        },
    ],
    source="网易·写作计划 + 番茄小说创作方法",
    confidence=0.91,
    ai_evasion_power=7,
))


# ============================================================
# 叙事声音 (Narrative Voice)
# ============================================================

_register(RhetoricTechnique(
    name="主观声音注入法·进阶",
    category=RhetoricCategory.NARRATIVE_VOICE.value,
    description="Voice = Personality。Writer's Digest定义：叙事声音由视角、词汇、标点、句法、节奏、描写技巧共同构成。AI缺乏真正的'声音'，只有模板。注入强烈主观性是去AI痕迹的王牌。",
    rules=[
        "加入第一人称判断：'以我的经验来看''我读到这段时后背发凉'",
        "加入情感反应：'看到这个数据，我差点把咖啡喷屏幕上'",
        "加入个人轶事：'我认识一个人，他...''有一次我遇到...'",
        "避免上帝视角的客观陈述",
        "用'笔者发现''结合调研来看'替代被动语态",
    ],
    examples=[
        {
            "before": "该政策的实施效果需要进一步观察。",
            "after": "政策落地三个月了。效果？我盯着数据看了半天——说实话，跟预期差得有点远。",
        },
    ],
    source="Writer's Digest Voice Guide + NaturalWrite + Soundcy",
    confidence=0.93,
    ai_evasion_power=9,
))

_register(RhetoricTechnique(
    name="角色灵魂档案法",
    category=RhetoricCategory.NARRATIVE_VOICE.value,
    description="AI写角色容易'千人一面'。必须在动笔前给角色注入：核心创伤、语言指纹(口头禅/用词习惯)、反差萌。每个角色说话方式完全不同。",
    rules=[
        "每个角色建立'语言指纹'：用词习惯、句子长度、口头禅",
        "核心创伤驱动行为：童年哪件事让他变成现在的性格？",
        "反差萌：外表凶狠的黑帮老大私下喜欢织毛衣",
        "对话中体现角色身份：老匠人说'这榫头得拿刨子咬一下'",
    ],
    examples=[
        {
            "before": "'你为什么要这样做？'他问道。'因为我想帮你。'她回答说。",
            "after": "'为什么？'\n他盯着她——不是质问，是恳求。刑警二十年，第一次用这种语气跟嫌疑人说话。\n她把茶杯转了半圈。'帮你。'两个字轻得像叹气。'就当还当年那颗糖。'",
        },
    ],
    source="今日头条·豆包去AI味7大技巧 + Writer's Digest Character Voice",
    confidence=0.94,
    ai_evasion_power=8,
))


# ============================================================
# 情绪映射 (Emotion Mapping)
# ============================================================

_register(RhetoricTechnique(
    name="情绪外化五步法",
    category=RhetoricCategory.EMOTION_MAPPING.value,
    description="禁止直接陈述情绪。每个情绪至少找到3个外化动作+2个环境折射+1个感官细节。'他很难过'→'他攥着信纸的手微微发抖，喉结滚动了几下，却什么也没说出来'。",
    rules=[
        "禁止：'他很生气/难过/开心/紧张'",
        "每个情绪=3个外化动作+2个环境折射+1个感官细节",
        "动作链替代心理描写：'拿起刀→放下→又拿起→手指在刀刃上抹了一下'",
        "环境折射：'暴雨冲垮了他们初遇时的木桥'(暗示关系破裂)",
        "感官细节：'他衬衫上的雪松香水味，混着她的眼泪'",
    ],
    examples=[
        {
            "before": "他非常紧张，心跳加速。",
            "after": "他把烟掐灭又点上。打火机按了三次——没着。第四次，手在抖。窗外救护车的鸣笛由远及近，他的瞳孔跟着那声音一缩一缩。",
        },
    ],
    source="CSDN·AI辅助创作指南 + Show Don't Tell研究",
    confidence=0.96,
    ai_evasion_power=10,
))

_register(RhetoricTechnique(
    name="光影情绪映射法·进阶",
    category=RhetoricCategory.EMOTION_MAPPING.value,
    description="张爱玲是色彩大师。用光影和色彩暗示情绪：暖光=安全/温馨，冷光=压抑/孤独，逆光=悲壮/威胁。写颜色的层次而非单一颜色。",
    rules=[
        "用光影暗示情绪，不直接说",
        "写颜色的层次：'砖红中泛着灰白，墙根爬满墨绿的苔'",
        "天气随剧情走：暴雨=冲突，雪=离别，雾=悬念",
        "光影变化=情绪变化：灯灭=绝望，烛燃=希望",
        "服装颜色=人物性格：'蓝布罩袍洗得泛灰白→温雅、质朴、人淡如菊'",
    ],
    examples=[
        {
            "before": "黄昏时分，天色渐渐暗了下来。",
            "after": "落日在西天烧成绛紫色。云层边缘勾着一道金边——像烧红的刀刃。屋瓦上的余温还没散尽，炊烟就升起来了，灰白的，懒懒的，像一声叹息。",
        },
    ],
    source="张爱玲研究 + 大众新闻·提升文笔 + 知乎镜头语言",
    confidence=0.94,
    ai_evasion_power=9,
))


# ============================================================
# 对话工艺 (Dialogue Craft)
# ============================================================

_register(RhetoricTechnique(
    name="潜台词对话法",
    category=RhetoricCategory.DIALOGUE_CRAFT.value,
    description="好对话永远是'话里有话'。表面谈论天气或晚饭，实际在试探忠诚度或掩饰慌张。每句话都要撕开人物关系的一道口子。AI对话太直白，像交换信息。",
    rules=[
        "每句对话必须有潜台词：说A，意思是B",
        "表面+实际双层设计：'饭在锅里，菜热了三次'(=你又晚归，我等你很久了)",
        "吵架用短句甚至半句，体现急促和攻击性",
        "暧昧用长句+动作描写，体现拉扯感",
        "用动作标签替代'他说''她说'",
    ],
    examples=[
        {
            "before": "'听说你男人出轨了？''关你屁事！''他包养的那个网红，好像是你高中同学。'",
            "after": "'听说你男人...'\n她没等对方说完。'关你屁事。'\n对方把手机推过来。屏幕上——一张合照。她盯着看了三秒。然后笑了一下。比哭还难看。'这人...是我同桌。高三，坐我左边。'",
        },
    ],
    source="今日头条·豆包去AI味7大技巧 + 短篇小说文笔指南",
    confidence=0.95,
    ai_evasion_power=9,
))

_register(RhetoricTechnique(
    name="对话钩子法",
    category=RhetoricCategory.DIALOGUE_CRAFT.value,
    description="每句对话必须带钩子——撕开人物关系的一道口子。不是交换信息，是制造冲突。废话对话是AI的典型特征。",
    rules=[
        "禁止废话对话：'你好吗''还不错''我也还行'",
        "每句对话推动：揭示信息/制造冲突/深化关系/反转认知",
        "对话节奏：冲突时短句连击，试探时长句迂回",
        "关键对话中，说出来的和心里想的要相反",
    ],
    examples=[
        {
            "before": "'你最近好吗？''还不错，你呢？''我也还行。'",
            "after": "'听说你男人出轨了？'\n'关你屁事！'\n'他包养的那个网红，好像是你高中同学。'\n她手里的杯子——没碎。但水洒了一桌。",
        },
    ],
    source="今日头条·短篇小说文笔指南",
    confidence=0.93,
    ai_evasion_power=8,
))


# ============================================================
# 节奏韵律 (Pacing & Rhythm)
# ============================================================

_register(RhetoricTechnique(
    name="三幕节奏控制法",
    category=RhetoricCategory.PACING_RHYTHM.value,
    description="用经典三幕式结构强行拉升剧情张力，打破AI流水账。第一幕(铺垫)打破平静，第二幕(对抗)困难升级，第三幕(高潮)绝地反击。每幕内也有小节奏循环。",
    rules=[
        "第一幕(20%)：打破平静，主角被迫卷入麻烦",
        "第二幕(50%)：困难升级，主角屡战屡败，情绪压抑",
        "第三幕(30%)：绝地反击，解决核心冲突",
        "每幕内至少2次节奏变化：快→慢→快",
        "高潮前蓄力：放慢节奏堆细节，然后短句爆发",
    ],
    examples=[
        {
            "before": "故事进行到一半，主角发现了重要线索。",
            "after": "线索就在眼前。\n他伸手——指尖碰到纸面的一瞬，突然缩回来。不对。太顺利了。他重新审视那条线索——每一个字，每一个标点。然后冷汗下来了。\n这是陷阱。反派故意留给他的。",
        },
    ],
    source="今日头条·豆包去AI味7大技巧 + Writer's Digest",
    confidence=0.92,
    ai_evasion_power=8,
))

_register(RhetoricTechnique(
    name="段落呼吸控制法",
    category=RhetoricCategory.PACING_RHYTHM.value,
    description="用段落长度控制阅读速度。短段=快读(紧张)，长段=慢品(沉浸)。避免AI均匀段落长度的模板化特征。段落长度要有明显变化：长→短→长→极短。",
    rules=[
        "关键情节用单句成段，制造冲击力",
        "描写段落不超过5行",
        "对话段落尽量短，每段不超过3句",
        "段落长度要有明显变化：长→短→长→极短",
        "避免连续3段长度相近(差距<2行)",
    ],
    examples=[
        {
            "before": "他走进房间，环顾四周。房间里很暗，只有一盏灯。他走到桌前，拿起那封信。信上写着他的名字。他打开信，开始阅读。",
            "after": "他推门。\n\n房间暗得像口井。唯一的光——桌上那盏灯，昏黄，摇摇欲坠。灯罩上积了厚厚的灰，把光滤成旧照片的颜色。\n\n他走过去。\n\n信。\n\n上面是他的名字。三个字，像三根钉子。",
        },
    ],
    source="番茄小说·创作方法 + 知乎写作社区",
    confidence=0.91,
    ai_evasion_power=8,
))


# ============================================================
# 留白艺术 (White Space Art)
# ============================================================

_register(RhetoricTechnique(
    name="临界点留白法",
    category=RhetoricCategory.WHITE_SPACE_ART.value,
    description="章末卡在临界点——不说完，让读者脑补。'他推开门，里面的场景让他瞳孔骤缩——' 用沉默传递情绪，结尾不说破。这是对抗AI'完美收尾'特征的王牌技法。",
    rules=[
        "章末卡在临界点：动作即将发生但未发生",
        "用沉默传递情绪：不写'他很难过'，写'他张了张嘴，什么都没说'",
        "对话留白：用动作替代台词",
        "结尾不说破：门关了、人走了、水溅裤脚，故事定格",
        "关键节点少写一句，让读者脑补",
    ],
    examples=[
        {
            "before": "故事到这里就结束了，他最终选择了离开。",
            "after": "门在他身后关上。锁舌弹进槽里——咔哒。\n走廊的声控灯亮了。\n又灭了。\n脚步声越来越远。越来越远。\n然后——\n没了。",
        },
    ],
    source="今日头条·短篇小说文笔指南 + 汪曾祺研究",
    confidence=0.93,
    ai_evasion_power=9,
))


# ============================================================
# 细节锚定 (Detail Anchor)
# ============================================================

_register(RhetoricTechnique(
    name="特指锚定法",
    category=RhetoricCategory.DETAIL_ANCHOR.value,
    description="用特指替代泛指。'老槐树第三根枝杈上的铁铃铛'替代'村口的树'。品牌/地名/人名具体化。数字具体化。物件细节：缺口茶杯、磨损戒指、泛黄照片——比千字解释更有力。",
    rules=[
        "用特指替代泛指：具体到'哪一个''哪一根''哪一次'",
        "数字具体化：'缩短30%的时间'替代'大幅提升效率'",
        "品牌/地名/人名具体化：'知网收录的张教授团队研究'替代'有研究显示'",
        "物件细节：缺口茶杯、磨损戒指、泛黄照片",
        "每1000字至少3处特指锚定",
    ],
    examples=[
        {
            "before": "故乡是一个山清水秀的小村庄。",
            "after": "村口老槐树的第三根枝杈上，挂着一只生锈的铁铃铛。风一吹就哑着嗓子响——这声音，他听了十八年。铃铛是阿姊用自行车链条做的，链条上还刻着'永久'两个字。",
        },
    ],
    source="大众新闻·提升文笔 + 知乎写作社区",
    confidence=0.94,
    ai_evasion_power=9,
))


# ============================================================
# 不完美美学 (Imperfection)
# ============================================================

_register(RhetoricTechnique(
    name="不完美美学·进阶",
    category=RhetoricCategory.IMPERFECTION.value,
    description="Human-in-the-Loop Perturbations研究证实：人工注入的文体特征（句长变化、故意语法错误、独特措辞）对AI检测器来说计算成本极高。保留轻微冗余、口语化词汇、思考停顿、语法不完美——这些'人味'是AI检测器的盲区。",
    rules=[
        "保留轻微冗余：'其实说白了''你猜怎么着'",
        "插入口语化词汇：'说实话''有点迷''这里要划重点'",
        "用破折号、省略号体现思考停顿",
        "偶尔的语法不完美：口语化断句、重复强调",
        "加入'我觉得''我发现''有意思的是'等主观引导",
        "每1000字至少2处'不完美'表达",
    ],
    examples=[
        {
            "before": "数据分析显示，用户偏好发生了显著变化。",
            "after": "数据跑出来的时候，我愣了一下。用户偏好——变了。变得还挺彻底。说实话，有点意外。我本来以为...算了，不说了。",
        },
    ],
    source="ResearchGate HIL Perturbations论文 + Soundcy + NaturalWrite",
    confidence=0.95,
    ai_evasion_power=10,
))


# ============================================================
# AI检测规避 (AI Evasion)
# ============================================================

_register(RhetoricTechnique(
    name="Perplexity爆破法",
    category=RhetoricCategory.AI_EVASION.value,
    description="GPTZero核心检测指标：Perplexity(困惑度)。AI文本过于流畅可预测→低困惑度。人类写作跳跃性强→高困惑度。通过注入意外词汇、非常规搭配、思维跳跃来提高困惑度。",
    rules=[
        "每500字至少1处意外用词：打破读者预期但合情合理",
        "非常规搭配：'月光刺在脸上'(不用'洒')，'黑暗吞没她'(不用'笼罩')",
        "思维跳跃：突然从A话题跳到B话题，但B与A有深层关联",
        "避免过于流畅的过渡：偶尔用'话说回来''突然想到'打断流畅度",
        "GPTZero检测perplexity：文本越难被语言模型预测，越像人类",
    ],
    examples=[
        {
            "before": "月光洒在她脸上，她感到非常悲伤。",
            "after": "月光——不是洒，是刺。一根一根扎进她的瞳孔。她没哭。眼泪早就被那个男人榨干了。话说回来，榨汁机的工作原理，跟婚姻差不多。",
        },
    ],
    source="GPTZero技术白皮书 + CSDN + 搜狐技术分析",
    confidence=0.97,
    ai_evasion_power=10,
))

_register(RhetoricTechnique(
    name="三步精修法",
    category=RhetoricCategory.AI_EVASION.value,
    description="初稿出来后必须走三步流程去AI味：①查逻辑(宏观)：剧情符合常理吗？②磨对话(中观)：所有对话读出声，拗口就改。③删废话(微观)：删掉'首先其次总之'等AI连接词。",
    rules=[
        "第一步查逻辑：把剧情读一遍，问自己'这事儿符合常理吗？'",
        "第二步磨对话：把所有对话读出声，拗口就改，像新闻联播就重写",
        "第三步删废话：删掉'首先其次总之值得注意的是'等AI连接词",
        "额外第四步：随机删除3-5个'的'字",
    ],
    examples=[
        {
            "before": "首先，他对现场进行了仔细的勘查。其次，他询问了目击者。最后，他得出了一个初步的结论。",
            "after": "现场——他蹲下来。指尖抹过地板上的灰痕。抬头。'谁第一个到的？'\n没人吭声。\n他又问了一遍。这次声音很轻。但所有人都听出了刀锋。",
        },
    ],
    source="今日头条·豆包去AI味7大技巧 + CSDN",
    confidence=0.95,
    ai_evasion_power=9,
))


# ============================================================
# 文化肌理 (Cultural Texture)
# ============================================================

_register(RhetoricTechnique(
    name="烟火气注入法",
    category=RhetoricCategory.CULTURAL_TEXTURE.value,
    description="写出中国老百姓的真实生活，而不是像在看译制片。把'喝咖啡'改成'喝豆浆、撸串'。把'上帝'改成'老天爷'。场景从'酒吧'切换到'大排档'或'麻将馆'。加入人情世故：办事靠'找熟人''递烟''给面子'。",
    rules=[
        "本土化细节：'喝咖啡'→'喝豆浆、撸串'，'上帝'→'老天爷'",
        "场景本土化：'酒吧'→'大排档/麻将馆/茶馆'",
        "人情世故：办事靠'找熟人''递烟''给面子'",
        "方言适度点缀：每章1-2处方言词汇(需加注释或上下文可理解)",
        "时代感细节：BB机、IC卡、绿皮火车、小灵通",
    ],
    examples=[
        {
            "before": "他在咖啡馆里思考着人生的意义。",
            "after": "他在大排档里撸着串。啤酒瓶碰了三次——对面那哥们儿还没开口。他知道，这是在'给面子'。等对方递烟过来，事儿才算开始谈。",
        },
    ],
    source="今日头条·豆包去AI味7大技巧 + 汪曾祺研究",
    confidence=0.92,
    ai_evasion_power=8,
))

_register(RhetoricTechnique(
    name="平淡近自然法",
    category=RhetoricCategory.CULTURAL_TEXTURE.value,
    description="汪曾祺文风核心：素笔留白，以小见大。摒弃浮华，偏爱质朴直白的语言、简洁利落的短句。只写一花一草、一饭一蔬，用极简白描，不修饰不渲染，在寻常点滴里藏尽生活温柔。张爱玲晚年也追求'平淡而近自然'。这是最高级的写作——也是最不像AI的写作。",
    rules=[
        "用最朴素的语言写最深的感情",
        "不修饰不渲染：白描优先",
        "以小见大：从一碗面、一场雨写出人生",
        "短句为主，节奏舒缓",
        "细节藏情：不写'他很孤独'，写'他一个人吃了三碗面'",
    ],
    examples=[
        {
            "before": "他感到非常孤独，在这个城市里没有朋友。",
            "after": "他一个人吃了三碗面。\n老板看了他一眼。\n他笑笑：'饿了。'\n其实不饿。就是不想回去。回去也是一个人。",
        },
    ],
    source="汪曾祺研究 + 张爱玲晚年风格 + 中国作家网",
    confidence=0.93,
    ai_evasion_power=9,
))


class AdvancedRhetoricEngine:
    """高级修辞与文体引擎"""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or API_KEY
        self.base_url = BASE_URL
        self.techniques = RHETORIC_TECHNIQUES

    def get_techniques_by_category(self, category: str) -> List[RhetoricTechnique]:
        return [t for t in self.techniques.values() if t.category == category]

    def get_top_evasion_techniques(self, top_n: int = 10) -> List[RhetoricTechnique]:
        return sorted(
            self.techniques.values(),
            key=lambda t: t.ai_evasion_power,
            reverse=True,
        )[:top_n]

    def build_master_prompt(self, genre: str = "玄幻") -> str:
        """构建大师级写作系统提示词"""
        parts = [
            f"你是一位拥有20年写作经验的{genre}小说大师，精通以下所有高级修辞与文体技法。",
            "",
            "【核心目标】AI检测率压制到5%以下，人工特征占比95%+",
            "",
        ]

        for cat in RhetoricCategory:
            techs = self.get_techniques_by_category(cat.value)
            if not techs:
                continue
            parts.append(f"## {cat.value}")
            for tech in techs[:2]:
                parts.append(f"### {tech.name}（规避力{tech.ai_evasion_power}/10）")
                parts.append(f"{tech.description}")
                for i, rule in enumerate(tech.rules[:3], 1):
                    parts.append(f"  {i}. {rule}")
                parts.append("")

        parts.append("【GPTZero 7组件检测对抗策略】")
        parts.append("1. Perplexity(困惑度)：注入意外词汇和非常规搭配，提高文本不可预测性")
        parts.append("2. Burstiness(爆发度)：句长方差>15，30%短句+50%中句+20%长句")
        parts.append("3. 段落呼吸：段落长度有明显变化，避免连续3段长度相近")
        parts.append("4. 主观声音：每500字至少1处第一人称判断或情感反应")
        parts.append("5. 不完美注入：每1000字至少2处口语词/思考停顿/语法瑕疵")
        parts.append("6. 通感修辞：每章至少1处感官交叉描写")
        parts.append("7. 留白收尾：章末不说完，卡在临界点")

        return "\n".join(parts)

    def build_rewrite_prompt(self, text: str, genre: str = "玄幻",
                              detected_traces: List[str] = None) -> str:
        """构建重写提示词"""
        trace_hint = ""
        if detected_traces:
            trace_hint = "\n【已检测到的AI痕迹（必须全部消除）】\n"
            trace_hint += "\n".join(f"- {t}" for t in detected_traces[:15])

        return f"""请将以下AI生成的{genre}小说章节彻底改写为人类大师级作品。

{trace_hint}

【改写铁律 — 目标AI检测率<5%】
1. 消除所有AI模板句式（值得注意的是/综上所述/首先其次/通过...实现...等50+种）
2. 注入全部12类高级修辞技法
3. 长短句交替：30%短句(3-10字)+50%中句(11-25字)+20%长句(26-50字)
4. 每场景至少3种感官描写（视觉+听觉+触觉/嗅觉）
5. 对话占比≥15%，每句对话有潜台词+钩子
6. 用动作替代形容词：每个情绪找到3个外化动作
7. 章末留白：不说完，卡在临界点
8. 每1000字至少2处'不完美'表达（口语词/停顿/省略号）
9. 每500字至少1处意外用词（提高Perplexity）
10. 注入烟火气：本土化细节、人情世故

【原文】
{text[:12000]}

请直接输出改写后的完整章节，不要加任何说明。"""

    def rewrite_master_level(self, text: str, genre: str = "玄幻",
                              detected_traces: List[str] = None) -> str:
        """大师级重写"""
        try:
            import requests
            resp = requests.post(
                f"{self.base_url}/v1/chat/completions",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.api_key}",
                },
                json={
                    "model": "deepseek-chat",
                    "messages": [
                        {"role": "system", "content": self.build_master_prompt(genre)},
                        {"role": "user", "content": self.build_rewrite_prompt(
                            text, genre, detected_traces
                        )},
                    ],
                    "temperature": 0.92,
                    "max_tokens": 16000,
                },
                timeout=300,
            )
            resp.raise_for_status()
            content = resp.json()["choices"][0]["message"]["content"]
            content = re.sub(r'```.*?\n|```', '', content).strip()
            return content
        except Exception as e:
            print(f"   ❌ 大师级重写失败: {e}")
            return text

    def get_statistics(self) -> Dict:
        """获取统计信息"""
        cats = {}
        total_evasion = 0
        for tech in self.techniques.values():
            cats[tech.category] = cats.get(tech.category, 0) + 1
            total_evasion += tech.ai_evasion_power

        return {
            "total_techniques": len(self.techniques),
            "categories": len(cats),
            "category_breakdown": cats,
            "avg_evasion_power": total_evasion / len(self.techniques) if self.techniques else 0,
            "top_evasion": [
                (t.name, t.ai_evasion_power)
                for t in self.get_top_evasion_techniques(5)
            ],
        }


def get_rhetoric_engine() -> AdvancedRhetoricEngine:
    if not hasattr(get_rhetoric_engine, "_instance"):
        get_rhetoric_engine._instance = AdvancedRhetoricEngine()
    return get_rhetoric_engine._instance


if __name__ == "__main__":
    print("=" * 60)
    print("AdvancedRhetoricEngine 独立测试")
    print("=" * 60)

    engine = AdvancedRhetoricEngine()
    stats = engine.get_statistics()

    print(f"\n📊 修辞技法统计:")
    print(f"   总技法数: {stats['total_techniques']}种")
    print(f"   覆盖类别: {stats['categories']}个")
    print(f"   平均规避力: {stats['avg_evasion_power']:.1f}/10")
    print(f"\n📊 类别分布:")
    for cat, count in stats['category_breakdown'].items():
        print(f"   - {cat}: {count}种")
    print(f"\n🏆 最强规避力TOP5:")
    for name, power in stats['top_evasion']:
        print(f"   - {name}: {power}/10")

    print(f"\n📝 大师级系统提示词(前500字):")
    prompt = engine.build_master_prompt("玄幻")
    print(prompt[:500])
