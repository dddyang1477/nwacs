#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 人工写作特征注入引擎 - HumanWritingInjector

核心目标：将AI生成文本的人工特征占比提升至85%以上

基于全网深度搜索的写作技法精华：
- 减法写作：去形容词、用动词名词、show don't tell
- 五感矩阵：每场景至少2种非视觉感官
- 镜头语言：远景→中景→特写的运镜逻辑
- 长短句呼吸：打破AI均匀句长，制造节奏感
- 光影情绪：用光与色替代直白情绪陈述
- 对话冲突：每句对话必有目的+冲突
- 留白艺术：不解释一切，让读者脑补
- 具体细节：用特指替代泛指，用案例替代概括
- 批判思维：让步、反驳、自我质疑
- 不完美美学：保留轻微冗余、口语化、思考停顿
"""

import json
import os
import re
import random
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


API_KEY = "sk-f3246fbd1eef446e9a11d78efefd9bba"
BASE_URL = "https://api.deepseek.com"


class HumanFeature(Enum):
    SENTENCE_RHYTHM = "句式节奏"       # 长短句交替，打破均匀
    SENSORY_MATRIX = "感官矩阵"       # 多感官描写
    CAMERA_LANGUAGE = "镜头语言"      # 远景中景特写运镜
    LIGHT_EMOTION = "光影情绪"        # 用光色替代直白情绪
    DIALOGUE_CONFLICT = "对话冲突"    # 每句对话有目的+冲突
    WHITE_SPACE = "留白艺术"          # 不解释一切
    SPECIFIC_DETAIL = "具体细节"      # 特指替代泛指
    CRITICAL_THINKING = "批判思维"    # 让步反驳自我质疑
    IMPERFECTION = "不完美美学"       # 轻微冗余口语化停顿
    SUBJECTIVE_VOICE = "主观声音"     # 第一人称感受和判断
    ACTION_OVER_ADJECTIVE = "动作替代形容词"  # show don't tell
    PACING_CONTROL = "节奏控制"       # 快慢交替


@dataclass
class HumanFeatureInjection:
    feature_type: str
    rules: List[str]
    examples: List[Dict[str, str]]
    weight: float  # 0-1, 该特征在改写中的权重


HUMAN_FEATURES = {
    HumanFeature.SENTENCE_RHYTHM.value: HumanFeatureInjection(
        feature_type="句式节奏",
        rules=[
            "每段至少包含1个超短句(3-8字)和1个中长句(20-40字)",
            "连续3句不能长度相近(差距<5字即为相近)",
            "关键情节用短句连击制造紧张感",
            "抒情段落用长句铺陈，但结尾必须用短句收住",
            "避免'首先其次最后''一二三'等AI列举结构",
            "用'不过''话说''有意思的是'替代'此外''另外'",
        ],
        examples=[
            {
                "before": "他走进房间，看到桌上放着一封信，信上写着他的名字，他拿起信打开阅读。",
                "after": "他推门。桌上躺着一封信。是他的名字。手指碰到信封边缘——停了一秒。然后撕开。",
            },
            {
                "before": "首先，他检查了武器。其次，他确认了路线。最后，他出发了。",
                "after": "武器，检查完毕。路线？早就刻在脑子里了。他深吸一口气，出发。",
            },
        ],
        weight=0.15,
    ),
    HumanFeature.SENSORY_MATRIX.value: HumanFeatureInjection(
        feature_type="感官矩阵",
        rules=[
            "每个场景至少包含2种非视觉感官(听觉/嗅觉/触觉/味觉)",
            "感官必须绑定情绪：冷风=紧张，桂花香=安心，铁锈味=危险",
            "声音分层：前景声(对话/动作)+环境声(风声/雨声)+内心声",
            "触觉优先：温度、质地、湿度比颜色更能制造沉浸感",
            "嗅觉是记忆触发器：某种气味可以瞬间拉回回忆",
        ],
        examples=[
            {
                "before": "房间里很安静，只有他一个人。",
                "after": "空调嗡鸣突然变得很响。他闻到自己的汗味——酸的，混着铁锈似的血腥气。指尖碰到桌面，冰凉滑腻，像摸到蛇皮。",
            },
            {
                "before": "她走进厨房，母亲正在做饭。",
                "after": "推门，油花在锅里滋滋跳。葱花下锅——'哗'一声，白烟腾地窜起。空气里炸开的香味让她鼻子一酸。",
            },
        ],
        weight=0.12,
    ),
    HumanFeature.CAMERA_LANGUAGE.value: HumanFeatureInjection(
        feature_type="镜头语言",
        rules=[
            "远景建立空间(1-2句环境) → 中景推进叙事(人物动作) → 特写引爆情绪(细节)",
            "关键瞬间使用慢镜头：把一秒掰成十秒写",
            "镜头要有变化：推拉摇移跟升降",
            "用'先看到局部，再看到全貌'制造悬念",
            "空镜定调：用环境暗示情绪，不直接说",
        ],
        examples=[
            {
                "before": "战场上到处都是尸体和破碎的武器，场面非常惨烈。",
                "after": "硝烟贴着地面爬。远处，残破的旗帜在风里一抽一抽。近处——一只断手还握着剑，指节发白。",
            },
            {
                "before": "她站在窗前看着外面的雨，心情很悲伤。",
                "after": "窗玻璃上的雨痕把街灯切成碎片。她的影子投在墙上，一动不动。手指按在冰冷的玻璃上——慢慢滑下，留下一道水汽。",
            },
        ],
        weight=0.10,
    ),
    HumanFeature.LIGHT_EMOTION.value: HumanFeatureInjection(
        feature_type="光影情绪",
        rules=[
            "用光影暗示情绪：暖光=安全/温馨，冷光=压抑/孤独，逆光=悲壮/威胁",
            "写时间的光：晨曦/斜阳/路灯/月光，每种光有不同情绪",
            "写颜色的层次：别只用单色，写'砖红中泛着灰白，墙根爬满墨绿的苔'",
            "天气随剧情走：暴雨=冲突，雪=离别，雾=悬念",
            "光影变化=情绪变化：灯灭=绝望，烛燃=希望",
        ],
        examples=[
            {
                "before": "黄昏时分，天色渐渐暗了下来。",
                "after": "落日在西天烧成绛紫色。云层边缘勾着一道金边——像烧红的刀刃。屋瓦上的余温还没散尽，炊烟就升起来了。",
            },
            {
                "before": "房间里光线很暗，气氛压抑。",
                "after": "昏黄的灯透过积灰的玻璃窗，在墙上投下一道狭长的影。影子里浮着细小的尘埃——像困在琥珀里的碎屑。",
            },
        ],
        weight=0.08,
    ),
    HumanFeature.DIALOGUE_CONFLICT.value: HumanFeatureInjection(
        feature_type="对话冲突",
        rules=[
            "每句对话必须有目的：想得到什么/想掩盖什么/想激怒谁/想说服谁",
            "对话不是聊天，是'目的+冲突'",
            "用动作、表情、停顿替代废话",
            "每个人说话方式不同：用词习惯、句子长度、口头禅",
            "关键对话中，说出来的和心里想的要相反(潜台词)",
            "避免'他说''她说'重复，用动作标签替代",
        ],
        examples=[
            {
                "before": '"你为什么要这样做？"他问道。"因为我想帮你。"她回答说。',
                "after": '"为什么？"\n他盯着她——不是质问，是恳求。\n她把茶杯转了半圈。\'帮你。\'两个字轻得像叹气。\n他笑了一下，比哭还难看。\'我不需要。\'',
            },
            {
                "before": '"我很生气！"他大声说。',
                "after": '他没说话。只是把烟掐灭在手心——火星一闪，熄了。然后抬头，笑："没事。"',
            },
        ],
        weight=0.10,
    ),
    HumanFeature.WHITE_SPACE.value: HumanFeatureInjection(
        feature_type="留白艺术",
        rules=[
            "关键节点少写一句，让读者脑补",
            "章末卡在临界点：'他推开门，里面的场景让他瞳孔骤缩——'",
            "用沉默传递情绪：不写'他很难过'，写'他张了张嘴，什么都没说'",
            "对话留白：用动作替代台词",
            "结尾不说破：门关了、人走了、水溅裤脚，故事定格",
        ],
        examples=[
            {
                "before": "他非常震惊，完全说不出话来。",
                "after": "他张嘴。\n闭上。\n又张嘴。\n最后只是把手机屏幕转向她。",
            },
            {
                "before": "故事到这里就结束了，他最终选择了离开。",
                "after": "门在他身后关上。锁舌弹进槽里——咔哒。走廊的声控灯亮了，又灭了。脚步声越来越远。",
            },
        ],
        weight=0.08,
    ),
    HumanFeature.SPECIFIC_DETAIL.value: HumanFeatureInjection(
        feature_type="具体细节",
        rules=[
            "用特指替代泛指：'老槐树第三根枝杈上的铁铃铛'替代'村口的树'",
            "用案例替代概括：'我身边有个朋友，坚持跑步三个月后...'替代'研究表明...'",
            "数字具体化：'缩短30%的时间'替代'大幅提升效率'",
            "品牌/地名/人名具体化：'知网收录的张教授团队研究'替代'有研究显示'",
            "物件细节：缺口茶杯、磨损戒指、泛黄照片——比千字解释更有力",
        ],
        examples=[
            {
                "before": "故乡是一个山清水秀的小村庄。",
                "after": "村口老槐树的第三根枝杈上，挂着一只生锈的铁铃铛。风一吹就哑着嗓子响——这声音，他听了十八年。",
            },
            {
                "before": "厨房里很温馨，充满了家的味道。",
                "after": "灶台上的搪瓷锅缺了个口——是七岁那年他摔的。母亲从没换过。锅里的排骨汤咕嘟咕嘟冒着泡，蒸汽模糊了窗玻璃上的剪纸。",
            },
        ],
        weight=0.10,
    ),
    HumanFeature.CRITICAL_THINKING.value: HumanFeatureInjection(
        feature_type="批判思维",
        rules=[
            "在核心论点后加入让步：'但这个结论可能不适用于...'",
            "加入自我质疑：'我之前也这么想，直到看到一个反例'",
            "加入对立观点：'有学者提出完全相反的看法...'",
            "结论加限制：'仍需进一步验证''本研究存在...局限'",
            "避免完美结论：人类倾向保留'未定结论'，AI倾向给出'完美结论'",
        ],
        examples=[
            {
                "before": "实验结果表明，该方法具有显著效果。",
                "after": "实验数据确实漂亮。但说实话——样本只有三十人，而且全是大学生。换一批人呢？不好说。",
            },
            {
                "before": "综上所述，这个方案是最优选择。",
                "after": "所以，选这个方案？\n大概率没错。但有个前提——市场别出幺蛾子。万一出了呢？那就是另一个故事了。",
            },
        ],
        weight=0.07,
    ),
    HumanFeature.IMPERFECTION.value: HumanFeatureInjection(
        feature_type="不完美美学",
        rules=[
            "保留轻微冗余：'其实说白了''你猜怎么着'",
            "插入口语化词汇：'说实话''有点迷''这里要划重点'",
            "用破折号、省略号体现思考停顿",
            "偶尔的语法不完美：口语化断句、重复强调",
            "加入'我觉得''我发现''有意思的是'等主观引导",
        ],
        examples=[
            {
                "before": "数据分析显示，用户偏好发生了显著变化。",
                "after": "数据跑出来的时候，我愣了一下。用户偏好——变了。变得还挺彻底。说实话，有点意外。",
            },
            {
                "before": "该理论具有重要的学术价值。",
                "after": "这个理论...怎么说呢。有用，确实有用。但你要说它完美？差得远。至少有三个坑，踩进去就出不来。",
            },
        ],
        weight=0.08,
    ),
    HumanFeature.SUBJECTIVE_VOICE.value: HumanFeatureInjection(
        feature_type="主观声音",
        rules=[
            "加入第一人称感受：'我读到这段的时候，后背发凉'",
            "加入个人判断：'以我的经验来看，这条路走不通'",
            "加入情感反应：'看到这个数据，我差点把咖啡喷屏幕上'",
            "避免上帝视角的客观陈述",
            "用'笔者发现''结合调研来看'替代被动语态",
        ],
        examples=[
            {
                "before": "该政策的实施效果需要进一步观察。",
                "after": "政策落地三个月了。效果？我盯着数据看了半天——说实话，跟预期差得有点远。",
            },
            {
                "before": "实验结果表明假设成立。",
                "after": "结果出来那一刻，实验室安静了三秒。然后我听见自己说了句脏话。假设成立——妈的，真的成立了。",
            },
        ],
        weight=0.06,
    ),
    HumanFeature.ACTION_OVER_ADJECTIVE.value: HumanFeatureInjection(
        feature_type="动作替代形容词",
        rules=[
            "禁止直接陈述情绪：不写'他很生气'，写'他把烟掐灭在手心'",
            "禁止直接陈述状态：不写'房间很乱'，写'吃剩的外卖盒子堆在桌角'",
            "用动作链替代心理描写：'他拿起刀→放下→又拿起→手指在刀刃上抹了一下'",
            "每个情绪至少找到3个外化动作",
            "动词优先：一个精准动词胜过三个形容词",
        ],
        examples=[
            {
                "before": "他非常紧张，心跳加速。",
                "after": "他把烟掐灭又点上。打火机按了三次——没着。第四次，手在抖。",
            },
            {
                "before": "她非常开心，笑容满面。",
                "after": "她把皮凉鞋脱了。赤脚在人行道的方砖上——一格，一格，跳过去。",
            },
        ],
        weight=0.10,
    ),
    HumanFeature.PACING_CONTROL.value: HumanFeatureInjection(
        feature_type="节奏控制",
        rules=[
            "打斗/冲突/意外：短句连击，每句不超过15字",
            "心理/回忆/风景：长句铺陈，但结尾短句收住",
            "一章内至少2次节奏变化：快→慢→快",
            "用段落长度控制阅读速度：短段=快读，长段=慢品",
            "高潮前蓄力：放慢节奏堆细节，然后短句爆发",
        ],
        examples=[
            {
                "before": "战斗非常激烈，双方你来我往，打了很久才分出胜负。",
                "after": "刀光。\n他侧身——慢了半拍。肩头一凉，血飙出来。\n退。再退。后背撞上墙。\n没路了。\n他咧嘴。牙缝里全是血。然后冲出去。",
            },
            {
                "before": "他回忆起童年的美好时光，心中充满了温暖。",
                "after": "那年夏天的蝉鸣特别响。他和阿姊蹲在井边，把西瓜浸在冰凉的井水里——等半个时辰，捞上来，一刀切下去，咔嚓。红色的汁水顺着手指往下淌。阿姊笑得露出豁了的门牙。\n后来那口井填了。阿姊嫁了。西瓜还是那个西瓜，但咔嚓声不对了。",
            },
        ],
        weight=0.08,
    ),
}


class HumanWritingInjector:
    """人工写作特征注入引擎"""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or API_KEY
        self.base_url = BASE_URL
        self.features = HUMAN_FEATURES

    def build_human_features_prompt(self, intensity: str = "maximum") -> str:
        """构建完整的人工写作特征注入提示词"""
        parts = ["\n【🎯 人工写作特征注入 — 目标：AI痕迹降至15%以下】\n"]
        parts.append("（以下技法来自全网深度搜索的写作社区精华，持续更新）\n")

        for feature_name, injection in self.features.items():
            parts.append(f"## {feature_name}（权重{injection.weight*100:.0f}%）")
            for i, rule in enumerate(injection.rules, 1):
                parts.append(f"  {i}. {rule}")
            parts.append("")

        if intensity == "maximum":
            parts.append("\n【⚠️ 强制执行】")
            parts.append("1. 以上12类人工特征，每1000字至少体现8类")
            parts.append("2. 禁止使用任何AI模板句式（详见AI痕迹模式库）")
            parts.append("3. 每段必须有至少1处'不完美'表达")
            parts.append("4. 对话占比不低于全文的15%")
            parts.append("5. 每场景至少2种感官描写")

        return "\n".join(parts)

    def build_rewrite_system_prompt(self, genre: str = "玄幻") -> str:
        """构建去AI痕迹重写的系统提示词"""
        return f"""你是一位拥有15年写作经验的顶级{genre}小说作家。你的任务是将AI生成的文本彻底改写为人类作家的原创作品。

【核心原则：85%人工特征占比】

你的改写必须让AI检测率降至15%以下。这意味着：
- 每1000字至少体现8类人工写作特征
- 零AI模板句式
- 充满'人味'的表达

{self.build_human_features_prompt('maximum')}

【改写铁律】
1. 保留原有人物性格和核心情节走向
2. 不添加新的关键情节
3. 不删除重要内容
4. 只输出改写后的正文，不要任何解释

现在，请用人类作家的方式重写。让每一个字都有温度。"""

    def build_rewrite_user_prompt(self, text: str, ai_traces: List[str] = None) -> str:
        """构建重写的用户提示词"""
        trace_hint = ""
        if ai_traces:
            trace_hint = "\n【已检测到的AI痕迹】\n" + "\n".join(f"- {t}" for t in ai_traces[:10])
            trace_hint += "\n\n请重点消除以上痕迹。"

        return f"""请将以下AI生成的网文章节彻底改写为人类作家风格。

{trace_hint}

【改写要求】
1. 打破所有AI模板句式（值得注意的是/综上所述/首先其次/通过...实现...等）
2. 注入12类人工写作特征（句式节奏/感官矩阵/镜头语言/光影情绪/对话冲突/留白/具体细节/批判思维/不完美/主观声音/动作替代形容词/节奏控制）
3. 长短句交替，制造呼吸感
4. 每场景至少2种感官描写
5. 对话占比不低于15%，每句对话有目的+冲突
6. 用动作替代形容词，show don't tell
7. 保留轻微不完美：口语词、思考停顿、省略号
8. 章末留白，不说完

【原文】
{text[:12000]}

请直接输出改写后的完整章节，不要加任何说明。"""

    def rewrite_with_human_features(self, text: str, genre: str = "玄幻",
                                     ai_traces: List[str] = None) -> str:
        """使用人工特征注入进行重写"""
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
                        {"role": "system", "content": self.build_rewrite_system_prompt(genre)},
                        {"role": "user", "content": self.build_rewrite_user_prompt(text, ai_traces)},
                    ],
                    "temperature": 0.9,
                    "max_tokens": 16000,
                },
                timeout=300,
            )
            resp.raise_for_status()
            content = resp.json()["choices"][0]["message"]["content"]
            content = re.sub(r'```.*?\n|```', '', content).strip()
            return content
        except Exception as e:
            print(f"   ❌ 人工特征注入重写失败: {e}")
            return text

    def get_feature_summary(self) -> str:
        """获取所有人工特征的摘要"""
        lines = ["=" * 60, "🎯 人工写作特征库（12类）", "=" * 60]
        total_weight = 0
        for name, inj in self.features.items():
            lines.append(f"\n📌 {name} (权重{inj.weight*100:.0f}%)")
            lines.append(f"   规则数: {len(inj.rules)}条")
            lines.append(f"   示例数: {len(inj.examples)}组")
            total_weight += inj.weight
        lines.append(f"\n{'='*60}")
        lines.append(f"📊 总权重: {total_weight*100:.0f}% (12类特征全覆盖)")
        lines.append(f"🎯 目标: AI痕迹降至15%以下，人工特征占比85%+")
        return "\n".join(lines)


def get_injector() -> HumanWritingInjector:
    """获取注入器单例"""
    if not hasattr(get_injector, "_instance"):
        get_injector._instance = HumanWritingInjector()
    return get_injector._instance


if __name__ == "__main__":
    print("=" * 60)
    print("HumanWritingInjector 独立测试")
    print("=" * 60)

    injector = HumanWritingInjector()
    print(injector.get_feature_summary())

    print("\n\n=== 系统提示词(前500字) ===")
    prompt = injector.build_rewrite_system_prompt("玄幻")
    print(prompt[:500])
