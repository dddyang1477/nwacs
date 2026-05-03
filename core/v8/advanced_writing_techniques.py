#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS V8.6 高级写作技巧增强模块
参考: 笔灵AI文笔润色, Sudowrite感官描写

核心功能:
- 多维度写作技巧增强
- 黄金开头生成
- 钩子技巧
- 节奏把控
- 去AI味处理
"""

import os
import json
import re
import random
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class WritingSkill(Enum):
    OPENING = "opening"
    DIALOGUE = "dialogue"
    DESCRIPTION = "description"
    BATTLE = "battle"
    EMOTION = "emotion"
    TRANSITION = "transition"
    HOOK = "hook"
    PACING = "pacing"
    GROUP_NARRATIVE = "group_narrative"
    WORLD_BUILDING = "world_building"
    PUZZLE = "puzzle"
    GUARD_THEME = "guard_theme"
    SUSPENSE = "suspense"
    TWIST = "twist"


@dataclass
class SkillEnhancement:
    """技巧增强配置"""
    skill_type: WritingSkill
    name: str
    description: str
    templates: List[str]
    examples: List[str]


class AdvancedWritingTechniques:
    """高级写作技巧"""

    def __init__(self):
        self.skills = self._load_skills()

    def _load_skills(self) -> Dict[WritingSkill, SkillEnhancement]:
        """加载写作技巧"""
        return {
            WritingSkill.OPENING: SkillEnhancement(
                skill_type=WritingSkill.OPENING,
                name="黄金开头技巧",
                description="创作吸引读者的开头技巧",
                templates=[
                    """开头公式一：【困境+悬念】
在{time}，{protagonist}正面临{crisis}。
突然，{incident}发生了！
这一切，都要从{backstory}说起。
""",
                    """开头公式二：【冲突+对立】
{protagonist}与{antagonist}的第一次相遇，充满了火药味。
" {dialogue} " {antagonist}冷笑道。
{protagonist}的眼神变得锐利："{response} "
"""
                ],
                examples=[
                    "黎明前的黑暗中，一道剑光划破寂静...",
                    "天玄大陆，以剑为尊。而他，叶尘，却连剑都握不稳..."
                ]
            ),
            WritingSkill.DIALOGUE: SkillEnhancement(
                skill_type=WritingSkill.DIALOGUE,
                name="对话技巧",
                description="让人物对话更生动",
                templates=[
                    """对话公式：【动作+台词+反应】
{character}猛地抬起头，眼中闪过一丝惊诧。
" {dialogue} "他的声音微微颤抖。
对面的人愣了愣，随即哈哈大笑起来。
""",
                    """对话公式：【省略+暗示+张力】
"你确定要..."
话还没说完，{character}已经转身离去。
只留下一个决绝的背影，和{detail}。
"""
                ],
                examples=[
                    "她低声说：我不知道。",
                    "他笑道：\"你以为，我会同意？\""
                ]
            ),
            WritingSkill.DESCRIPTION: SkillEnhancement(
                skill_type=WritingSkill.DESCRIPTION,
                name="描写技巧",
                description="多维度场景描写",
                templates=[
                    """五感描写公式：
视觉：{visual}
听觉：{auditory}
嗅觉：{olfactory}
触觉：{tactile}
心理：{psychological}
""",
                    """环境渲染公式：
此时的天空{sky}，{wind}吹过，带来一阵{smell}。
远处的{sound}若隐若现，让人不由得紧张起来。
"""
                ],
                examples=[
                    "月光如水般倾泻而下，银色的光芒照亮了她的脸庞...",
                    "空气中弥漫着淡淡的血腥味，和着泥土的腥气，让人作呕..."
                ]
            ),
            WritingSkill.BATTLE: SkillEnhancement(
                skill_type=WritingSkill.BATTLE,
                name="战斗描写技巧",
                description="精彩的战斗场景",
                templates=[
                    """战斗公式一：【蓄力+爆发+余波】
{attacker}深吸一口气，体内的灵力如潮水般涌动。
"受死吧！"
{technique}骤然发出，带着毁天灭地的威势，直奔{opponent}而去。
大地崩裂，山河变色。战斗的余波席卷四方，围观者纷纷后退。
""",
                    """战斗公式二：【悬念+反转+碾压】
{opponent}嗤笑一声："{taunt}"
然而，下一秒，他的笑容凝固了。
只见{attacker}缓缓抬手，{power}骤然爆发。
"不可能！" {opponent}瞪大了眼睛，满脸不可置信。
"""
                ],
                examples=[
                    "剑光如虹，凌厉无匹，直取敌人咽喉...",
                    "他嘴角勾起一抹冷笑，指尖灵力凝聚，轻声道：\"结束了。\""
                ]
            ),
            WritingSkill.EMOTION: SkillEnhancement(
                skill_type=WritingSkill.EMOTION,
                name="情感描写技巧",
                description="细腻的情感表达",
                templates=[
                    """情感公式一：【递进+爆发】
最初的{cold}渐渐消融，取而代之的是{warm}。
当{event}发生时，她的心猛地揪紧了。
那一刻，所有的伪装都土崩瓦解，只剩下{cry}。
""",
                    """情感公式二：【隐忍+细节+触动】
他什么都没说，只是转过身去。
但她看到了——他紧握的拳头，指节泛白。
还有那微微颤抖的肩膀，和{detail}。
"""
                ],
                examples=[
                    "她的眼眶渐渐泛红，却倔强地不让泪水落下...",
                    "那双眼睛里，有太多她读不懂的情绪——悲伤、愧疚，还有深深的爱意..."
                ]
            ),
            WritingSkill.TRANSITION: SkillEnhancement(
                skill_type=WritingSkill.TRANSITION,
                name="转场技巧",
                description="流畅的场景转换",
                templates=[
                    """时间转场：【数年后/时光飞逝】
{cultivation}过去了。
{protagonist}的修为已经突破了{realm}，达到了新的高度。
而那个曾经{cold}的人，如今却变得{change}。
""",
                    """空间转场：【场景+呼应】
{place_pre}的风光依旧，{detail}。
{protagonist}站在原地，心中却已沧海桑田。
{psychological}
"""
                ],
                examples=[
                    "春去秋来，岁月如梭。三年时间，转瞬即逝。",
                    "画面一转，场景来到了天玄宗的山门之前..."
                ]
            ),
            WritingSkill.HOOK: SkillEnhancement(
                skill_type=WritingSkill.HOOK,
                name="钩子技巧",
                description="制造悬念吸引读者",
                templates=[
                    """悬念钩子：【疑问+暗示】
正当{protagonist}要打开{object}时，他突然停住了。
因为，他发现了一件事——
{secret}。
""",
                    """危机钩子：【高潮+中断】
眼看着{victory}在望，{protagonist}却突然感到一阵剧痛。
低头一看，{crisis}。
他的脸色瞬间变得苍白：\"怎么可能...！\"
"""
                ],
                examples=[
                    "然而，就在他即将成功的那一刻，意外发生了...",
                    "他不知道的是，真正的危机，才刚刚开始..."
                ]
            ),
            WritingSkill.PACING: SkillEnhancement(
                skill_type=WritingSkill.PACING,
                name="节奏技巧",
                description="控制叙事节奏",
                templates=[
                    """快节奏公式：【短句+动词+紧凑】
轰！
他出手了。
快如闪电，猛如惊雷。
对方还没反应过来，就已经倒飞出去。
""",
                    """慢节奏公式：【长句+细节+氛围】
月光下，她静静地站在那里。
微风拂过，吹动她的衣袂。
那双眼睛，望着远方，似乎在想着什么。
{psychological}
"""
                ],
                examples=[
                    "一剑霜寒十四州！",
                    "夜深了，万籁俱寂，只有虫鸣声在耳边回响..."
                ]
            ),
            WritingSkill.GROUP_NARRATIVE: SkillEnhancement(
                skill_type=WritingSkill.GROUP_NARRATIVE,
                name="群像叙事技巧",
                description="多视角、多角色叙事（参考十日终焉）",
                templates=[
                    """视角切换公式：【主视角→配角视角→主视角】
{protagonist_a}的视角：
他看着眼前的一切，心中充满了震惊。

镜头一转，{protagonist_b}的视角：
而在另一边，{protagonist_b}正在经历着完全不同的故事。

最终，两条线索汇聚在一起...
""",
                    """多人独白公式：【角色A独白→角色B独白→共同行动】
{character_a}内心独白：
我必须活下去，不管付出什么代价。

{character_b}内心独白：
这一次，我不会再退缩。

当他们相遇时，命运的齿轮开始转动...
"""
                ],
                examples=[
                    "而在另一边，齐夏并不知道，一场更大的危机正在等待着他...",
                    "林七夜看着眼前的一切，而在城市的另一角，有人正默默地注视着这一切..."
                ]
            ),
            WritingSkill.WORLD_BUILDING: SkillEnhancement(
                skill_type=WritingSkill.WORLD_BUILDING,
                name="世界观构建技巧",
                description="独特世界观设定（参考诡秘之主）",
                templates=[
                    """世界观公式：【核心设定→规则体系→具体表现】
核心设定：{core_concept}

在这个世界里，{rule_system}

具体表现为，{specific_manifestation}
""",
                    """克苏鲁风公式：【未知恐怖→禁忌知识→人性挣扎】
世界的真相，远比想象中更加恐怖。

{forbidden_knowledge}

而人类，在这样的真相面前，显得如此渺小...
"""
                ],
                examples=[
                    "蒸汽与机械的浪潮中，谁能触及非凡？历史和黑暗的迷雾里，又是谁在耳语？",
                    "在永夜笼罩的世界里，人类必须点燃自己，才能照亮前行的道路..."
                ]
            ),
            WritingSkill.PUZZLE: SkillEnhancement(
                skill_type=WritingSkill.PUZZLE,
                name="智斗解谜技巧",
                description="逻辑推理、规则破解（参考十日终焉）",
                templates=[
                    """规则破解公式：【发现规则→分析漏洞→利用漏洞】
{character}仔细观察着周围的一切。

终于，他发现了规则中的破绽：{loophole}

"原来如此..."他的眼中闪过一丝光芒，"我知道该怎么做了。"
""",
                    """时间循环公式：【循环开始→积累信息→找到破局点】
第一次循环：{first_loop}

第二次循环：{second_loop}

第N次循环：{nth_loop}

终于，{character}找到了打破循环的方法...
"""
                ],
                examples=[
                    "齐夏看着眼前的十二生肖，突然明白了什么——原来规则的破绽就在这里...",
                    "如果这一切都是循环，那我只需要记住每一个细节，就能找到破局的方法..."
                ]
            ),
            WritingSkill.GUARD_THEME: SkillEnhancement(
                skill_type=WritingSkill.GUARD_THEME,
                name="守护主题技巧",
                description="守护家人、守护家园（参考斩神）",
                templates=[
                    """守护宣言公式：【危机降临→守护决心→爆发力量】
当{threat}来临时，{character}站了出来。

"我要守护的，是我身后的一切！"

这一刻，{character}爆发出了前所未有的力量...
""",
                    """家国情怀公式：【个人情感→升华为家国→共同守护】
{character}曾经以为，自己只是为了{personal_goal}而战。

但当他看到{scene}时，他明白了——

他要守护的，是整个{home}！
"""
                ],
                examples=[
                    "大夏境内，神明禁行！",
                    "以身为灯，照破长夜！"
                ]
            ),
            WritingSkill.SUSPENSE: SkillEnhancement(
                skill_type=WritingSkill.SUSPENSE,
                name="悬念设置技巧",
                description="制造读者好奇心（参考知乎盐言故事）",
                templates=[
                    """信息差悬念公式：【隐瞒关键信息→逐步透露】
读者知道{secret}，但主角不知道。

每当主角接近真相时，{obstacle}出现。

读者的心被紧紧抓住，期待着主角发现真相的那一刻...
""",
                    """反常悬念公式：【正常场景→异常事件】
{normal_scene}，一切看起来都很正常。

然而，{abnormal_event}发生了。

没有人知道为什么，包括读者——这就是悬念的魅力。
"""
                ],
                examples=[
                    "他总戴着手套，从不碰凶器；指甲缝永远干净...",
                    "她从不问关键问题；别人提某事时她会走神..."
                ]
            ),
            WritingSkill.TWIST: SkillEnhancement(
                skill_type=WritingSkill.TWIST,
                name="反转技巧",
                description="制造意料之外情理之中的反转（参考欧亨利）",
                templates=[
                    """3+1反转公式：【伏笔→误导→点破→揭晓】
开篇：{minor_clue}（无人在意的小细节）
中段：{strong_misdirection}（让读者坚信错误答案）
反转前：{hint}（一句台词暗示真相）
反转时：{revelation}（所有伏笔瞬间闭环）
""",
                    """人设反转公式：【表面形象→隐藏线索→揭露真相】
{character}看起来是{surface_personality}。

但仔细看，{hidden_clues}。

当{trigger_event}发生时，他终于露出了真面目——{true_identity}！
"""
                ],
                examples=[
                    "原来，凶手就是最不可能的那个人...",
                    "她不是受害者，而是整个阴谋的策划者..."
                ]
            )
        }

    def enhance_opening(self, protagonist: str, world_setting: str,
                       conflict: str) -> str:
        """生成黄金开头"""
        templates = self.skills[WritingSkill.OPENING].templates

        opening = f"""
==========================================
【黄金开头】玄幻小说经典开场模式
==========================================

开场模式一：世界观+困境
------------------------------------------
{world_setting}。

在这片大陆上，{protagonist}只是一个微不足道的存在。

然而，一场突如其来的{cn_conflict}，彻底改变了他的命运。

"我不能就这样认输！"他在心中怒吼。

==========================================

开场模式二：对立+悬念
------------------------------------------
{protagonist}从未想过，他会与{conflict}扯上关系。

那一天，当{antagonist}出现在他面前时，命运的齿轮开始转动。

"从今天起，你的命运，将由我来书写。" {antagonist}的话，如同诅咒般萦绕在他心头。

==========================================

开场模式三：倒叙+伏笔
------------------------------------------
多年后，当{protagonist}回首往事，一切都要从那个改变他命运的日子说起。

那一天，天空下着雨，{detail}。

而他，将彻底告别过去，走上一条全新的道路。

==========================================
"""
        return opening

    def enhance_dialogue(self, character: str, emotion: str,
                         subtext: str) -> str:
        """增强对话描写"""
        templates = self.skills[WritingSkill.DIALOGUE].templates

        return f"""
==========================================
【对话技巧】{character}的情感表达
==========================================

内心外化型：
------------------------------------------
{character}张了张嘴，想要说什么，却又咽了回去。

那欲言又止的模样，比任何语言都更能说明他的心情。

——{subtext}

------------------------------------------

动作配合型：
------------------------------------------
{character}冷笑一声，转过身去。

"随你怎么想。"

他的声音听起来漫不经心，但那双紧握的拳头，却出卖了他的真实情绪。

——{emotion}

------------------------------------------

沉默压迫型：
------------------------------------------
{character}没有说话。

他只是静静地看着对方，那眼神，仿佛在看一个死人。

空气仿佛凝固了，压得人喘不过气来。

良久，他才开口：

"{subtext}"

------------------------------------------
"""

    def enhance_battle(self, attacker: str, technique: str,
                      opponent: str) -> str:
        """增强战斗描写"""
        templates = self.skills[WritingSkill.BATTLE].templates

        return f"""
==========================================
【战斗技巧】{attacker} vs {opponent}
==========================================

蓄力阶段：
------------------------------------------
{attacker}深吸一口气，周身灵力开始沸腾。

天地灵气仿佛感受到了召唤，疯狂地向他们汇聚。

风起云涌，天色骤变。

"接招吧！" {attacker}暴喝一声。

------------------------------------------

爆发阶段：
------------------------------------------
{technique}！！

这一剑，仿佛要将天地撕裂，带着毁天灭地的威势，直取{opponent}。

剑光所过之处，虚空碎裂，星辰陨落。

{detail}

------------------------------------------

结果展示：
------------------------------------------
{opponent}的瞳孔骤然收缩。

他想躲，却发现自己已经被锁定了。

"不...不可能！"

轰然巨响中，他被彻底击飞出去。

鲜血喷洒长空，染红了半边天。

------------------------------------------

围观反应：
------------------------------------------
周围所有人都惊呆了。

他们不敢相信，那个不可一世的{opponent}，竟然...

"这...这怎么可能！"有人惊呼出声。

而{attacker}，只是淡淡地收回剑，转身离去。

留给众人的，只有一个孤独而强大的背影。

==========================================
"""

    def enhance_emotion(self, character: str, emotion_type: str,
                       trigger: str) -> str:
        """增强情感描写"""
        templates = self.skills[WritingSkill.EMOTION].templates

        emotion_map = {
            "sadness": {"word": "悲伤", "detail": "泪水无声滑落", "psychological": "心如刀绞"},
            "joy": {"word": "喜悦", "detail": "笑容灿烂如阳", "psychological": "心花怒放"},
            "anger": {"word": "愤怒", "detail": "眼中怒火燃烧", "psychological": "怒发冲冠"},
            "fear": {"word": "恐惧", "detail": "脸色苍白如纸", "psychological": "心惊肉跳"}
        }

        emotion = emotion_map.get(emotion_type, emotion_map["sadness"])

        return f"""
==========================================
【情感技巧】{character}的{emotion['word']}
==========================================

触动时刻：
------------------------------------------
当{trigger}时，{character}的心猛地揪紧了。

那是一种难以言喻的感觉，仿佛有什么东西在心底深处被触动。

他想起了{trigger}，想起了那些{related_memory}。

------------------------------------------

情感爆发：
------------------------------------------
终于，他再也忍不住了。

{emotion['detail']}。

那泪水，如同断了线的珠子，怎么也止不住。

这一刻，所有的坚强都崩塌了。

------------------------------------------

心理描写：
------------------------------------------
{character}的内心正在经历{emotion['psychological']}的煎熬。

他不明白，为什么{reason}。

他只知道，此刻的这种感觉，让他几乎窒息。

------------------------------------------

情感余韵：
------------------------------------------
良久，{character}才渐渐平复下来。

他抬起头，望向远方。

眼神中，多了一丝坚定：

"从今往后，我再也不会..."

==========================================
"""

    def enhance_hook(self, hook_type: str, context: str) -> str:
        """增强悬念钩子"""
        templates = self.skills[WritingSkill.HOOK].templates

        return f"""
==========================================
【钩子技巧】{hook_type}类型悬念
==========================================

悬念设置：
------------------------------------------
正当所有人都以为事情已经结束时，
突然，{unexpected_event}发生了！

原来，真正的真相竟然是...
{truth}

------------------------------------------

危机降临：
------------------------------------------
然而，真正的危机，才刚刚开始。

当{character}意识到这一点时，已经太晚了。

{crisis}，正在一步步逼近。

而他，似乎已经无路可逃...

------------------------------------------

命运抉择：
------------------------------------------
摆在{character}面前的，只有两条路。

要么，{choice_a}。
要么，{choice_b}。

无论选择哪一条，都将改变他的命运。

"我..." {character}的声音，在黑暗中回荡。

==========================================
"""

    def remove_ai_taste(self, text: str) -> str:
        """去除AI写作痕迹"""
        ai_patterns = {
            r"\b因此\b": "所以",
            r"\b然而\b": "但",
            r"\b所以\b": "于是",
            r"\b并且\b": "还",
            r"\b首先\b": "",
            r"\b其次\b": "",
            r"\b最后\b": "",
            r"\b综上所述\b": "",
            r"\b可以看出\b": "能看到",
            r"\b值得注意的是\b": "",
            r"\b一般来说\b": "",
            r"\b通常情况下\b": ""
        }

        result = text
        for pattern, replacement in ai_patterns.items():
            result = re.sub(pattern, replacement, result)

        return result

    def create_shooting_hook(self, chapter_content: str) -> str:
        """创建追更钩子"""
        hooks = []

        if "战斗" in chapter_content or "对决" in chapter_content:
            hooks.append("然而，就在这千钧一发之际，意外发生了...")

        if "成功" in chapter_content or "突破" in chapter_content:
            hooks.append("但他不知道的是，真正的危险正在逼近...")

        if "感情" in chapter_content or "告白" in chapter_content:
            hooks.append("就在两人即将表白的关键时刻，有人突然出现...")

        hooks.append("欲知后事如何，请看下章分解...")
        hooks.append("他的命运，将在下一次相见时，彻底改变...")
        hooks.append("而这一切，都只是开始...")

        return random.choice(hooks)
    
    def enhance_group_narrative(self, characters: List[str], scenes: List[str]) -> str:
        """增强群像叙事"""
        result = []
        result.append("="*60)
        result.append("👥 群像叙事技巧 - 参考十日终焉")
        result.append("="*60)
        
        for i, char in enumerate(characters):
            result.append(f"\n📖 {char}的视角:")
            result.append("-"*60)
            if i < len(scenes):
                result.append(f"{scenes[i]}")
            else:
                result.append(f"{char}正在经历着自己的故事...")
        
        result.append("\n🔗 视角汇聚:")
        result.append("-"*60)
        result.append("最终，所有的线索汇聚在一起...")
        result.append("命运的齿轮开始转动，没有人能够逃脱...")
        
        result.append("\n" + "="*60)
        return "\n".join(result)
    
    def enhance_world_building(self, core_concept: str, rule_system: str, specific_manifestation: str) -> str:
        """增强世界观构建"""
        return f"""
{"="*60}
🌍 世界观构建技巧 - 参考诡秘之主
{"="*60}

核心设定：
{core_concept}

规则体系：
{rule_system}

具体表现：
{specific_manifestation}

读者融入指南：
1. 从小处着手，通过细节展现世界观
2. 让世界观影响主角的决策和行动
3. 逐步揭示，不要一次性灌输
4. 让世界观成为推动剧情的力量

{"="*60}
"""
    
    def enhance_puzzle(self, character: str, puzzle_type: str) -> str:
        """增强智斗解谜"""
        puzzle_templates = {
            "time_loop": f"""
{"="*60}
⏰ 时间循环解谜 - 参考十日终焉
{"="*60}

{character}发现自己陷入了时间循环...

第一次循环：慌乱、迷茫
第二次循环：开始观察、记录
第三次循环：发现规律、寻找破绽
...
第N次循环：找到破局的关键！

解谜要点：
1. 每一次循环都要获取新信息
2. 找出规则中的漏洞
3. 利用已知改变未知
4. 在循环中不断成长

{"="*60}
""",
            "rule_breaking": f"""
{"="*60}
🎯 规则破解技巧
{"="*60}

{character}仔细观察着眼前的一切...

步骤1：理解规则
步骤2：找出漏洞
步骤3：利用漏洞
步骤4：打破规则！

关键思维：
- 规则是人定的，就一定有破绽
- 换个角度看问题
- 把限制变成优势

{"="*60}
"""
        }
        return puzzle_templates.get(puzzle_type, puzzle_templates["time_loop"])
    
    def enhance_guard_theme(self, character: str, what_to_guard: str, threat: str) -> str:
        """增强守护主题"""
        return f"""
{"="*60}
🛡️ 守护主题技巧 - 参考斩神
{"="*60}

当{threat}来临时...

{character}站了出来。

"我要守护的，是我身后的{what_to_guard}！"

守护宣言的层次：
1. 守护个人（家人、爱人）
2. 守护集体（同伴、组织）
3. 守护家园（城市、国家）
4. 守护文明（整个人类）

经典台词模板：
- "{what_to_guard}境内，{threat}禁行！"
- "以身为灯，照破长夜！"
- "这一次，换我来守护你！"

{"="*60}
"""
    
    def enhance_suspense(self, setup: str, mystery: str, stakes: str) -> str:
        """增强悬念设置"""
        return f"""
{"="*60}
🔍 悬念设置技巧 - 参考知乎盐言故事
{"="*60}

核心口诀：明线误导，暗线藏真；细节说话，台词留缝

设置步骤：
1. 反常开场：{setup}
2. 抛出疑问：{mystery}
3. 建立 stakes：{stakes}

四种伏笔类型：
1. 细节伏笔：用物品、动作、习惯藏真相，不解释、不强调
2. 台词伏笔：说半句真话，半句假话，台词能同时解释假身份和真身份
3. 视角偏差伏笔：利用主角视角盲区，只写主角看到的
4. 因果倒置伏笔：先给结果，再露原因，巧合多到不正常

信息差技巧：
- 读者知道 + 主角不知道 = 戏剧性 irony
- 角色知道 + 读者不知道 = 期待感

{"="*60}
"""
    
    def enhance_twist(self, setup: str, misdirection: str, revelation: str) -> str:
        """增强反转设计"""
        return f"""
{"="*60}
💥 反转设计技巧 - 参考欧亨利、盐言故事
{"="*60}

3+1反转结构：
【第一步】开篇轻伏笔
{setup}（无人在意的小细节）

【第二步】中段强误导
{misdirection}（让读者坚信错误答案）

【第三步】反转前点破
一句台词/一个动作，暗示真相

【第四步】反转揭晓
{revelation}（所有伏笔瞬间闭环）

反转类型：
1. 人设反转：白切黑、打破刻板印象、身份互换
2. 情节反转：真相反转、选择反转、绝境反转
3. 结局反转：欧亨利式结尾、意料之外情理之中

避雷指南：
- 伏笔太明显：读者早猜到，没惊喜
- 伏笔太隐晦：读者看不懂，觉得强行
- 只埋一处：证据不足，说服力弱
- 反转后不回收伏笔：前面白写

{"="*60}
"""
    
    def enhance_wechat_article(self, content_type: str = "emotion") -> str:
        """增强公众号爆款文章"""
        templates = {
            "emotion": f"""
{"="*60}
📱 公众号爆款文章 - 情感类
{"="*60}

核心公式：爆款=强情绪+真细节+短节奏+好标题+强结构+高互动

【标题公式】
• 颠覆认知型：别再【错误做法】了，99%的人都被误导了
• 痛点焦虑型：成年人的心酸，都藏在【细节】里
• 人间清醒型：放下执念，才是人生最好的解药
• 对比反差型：以前拼命追求【xx】，现在只想安稳度日

【开头公式 - 5秒留住人】
• 场景代入式：不知道从什么时候开始，我们慢慢变成了【现状】
• 反问扎心式：你有没有发现，越长大，越喜欢沉默
• 共情共鸣式：我们都在普通的生活里，一边崩溃，一边自愈

【正文结构 - 黄金三段式】
开头：戳中情绪 + 现状共鸣
中段：分3点讲道理/讲现实/讲感悟
过渡：其实人生从来都不完美……
结尾：治愈金句 + 升华三观

【结尾公式 - 引导互动】
• 治愈升华款：愿往后余生，看淡得失，从容度日，温柔且坚定
• 互动提问款：你认同这种说法吗？评论区聊聊
• 短句余味款：生活万般不易，自愈才是顶配

【万能金句】
• 万般皆是命，半点不由人
• 接受普通，然后拼尽全力与众不同
• 风雨里做个大人，阳光下做个小孩
• 减少期待，戒掉敏感，好好生活

{"="*60}
""",
            "knowledge": f"""
{"="*60}
📱 公众号爆款文章 - 干货类
{"="*60}

【标题公式】
• 数字干货型：5个【方法】，普通人立刻逆袭
• 痛点+方案：《写作没逻辑？用这招彻底解决》
• 人群精准型：月薪3千和月薪3万，差的从来不是努力

【开头公式】
• 结果前置：用这套方法，我30天写出5篇10W+
• 痛点提问：你有没有过写了3小时，却没人看的崩溃？

【正文结构 - SCQA结构】
S（场景）：具体生活/工作场景
C（冲突）：理想vs现实反差
Q（问题）：读者内心疑问
A（答案）：可落地解决方案

【结尾公式】
• 总结+建议收藏
• 引导转发：内容干货满满，建议收藏，慢慢品读

{"="*60}
""",
            "story": f"""
{"="*60}
📱 公众号爆款文章 - 故事类
{"="*60}

【标题公式】
• 悬念好奇型：为什么越勤快的人，越赚不到钱？
• 反差式：我以为他是"摆烂"的95后，直到看见他的副业收入
• 热点结合式：最近爆火的"村BA"，其实藏了一个秘密

【开头公式】
• 故事引入式：昨天遇到一件小事，瞬间读懂了成年人的无奈
• 悬念式：上周和客户谈判，我用了一个"反常规"技巧……

【正文结构 - 冲突-反转-升华】
冲突：制造矛盾/困境
反转：打破预期
升华：提炼观点/金句

【结尾公式】
• 反转留白：我笑着挂电话，却哭了一小时
• 首尾呼应：回到开头场景，闭环更完整

{"="*60}
"""
        }
        return templates.get(content_type, templates["emotion"])


def main():
    print("="*60)
    print("✨ NWACS V8.6 高级写作技巧增强模块")
    print("="*60)

    techniques = AdvancedWritingTechniques()

    print("\n📚 写作技巧库:")
    for skill in WritingSkill:
        print(f"  • {skill.value}: {techniques.skills[skill].name}")

    print("\n" + "="*60)
    print("✅ 高级写作技巧系统就绪")
    print("="*60)


if __name__ == "__main__":
    main()