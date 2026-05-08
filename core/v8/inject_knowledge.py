#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""将全网搜索的写作技法精华注入知识库"""
import json
import os
import hashlib
from datetime import datetime

KB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".deep_learning_kb", "knowledge_base.json")

NEW_TECHNIQUES = [
    {
        "name": "减法写作：去形容词用动词",
        "category": "写作风格",
        "description": "删除冗余形容词和副词，用精准动词和名词替代。一个精准动词胜过三个形容词。让文字更干净有力。",
        "rules": [
            "每句最多保留1个形容词",
            "用动作替代情绪描述：不写'他很生气'，写'他把烟掐灭在手心'",
            "删除'非常''极其''十分'等程度副词",
            "用具体名词替代抽象概念",
        ],
        "examples": [
            {"before": "他非常愤怒地大声喊道。", "after": "他吼。"},
            {"before": "房间里非常安静，气氛十分压抑。", "after": "房间静得能听见自己的心跳。墙角的水渍像一张扭曲的脸。"},
        ],
        "source_url": "https://www.zhihu.com/search?type=content&q=写作去AI痕迹",
        "source_topic": "AI痕迹消除核心技法",
        "confidence": 0.95,
    },
    {
        "name": "长短句呼吸法",
        "category": "句式结构",
        "description": "打破AI均匀句长，制造人类写作的呼吸感。短句制造紧张，长句铺陈情绪，交替使用形成节奏。",
        "rules": [
            "每段至少1个超短句(3-8字)和1个中长句(20-40字)",
            "连续3句不能长度相近(差距<5字)",
            "打斗/冲突用短句连击，每句不超过15字",
            "抒情段落用长句铺陈，但结尾必须用短句收住",
        ],
        "examples": [
            {"before": "战斗非常激烈，双方你来我往，打了很久才分出胜负。", "after": "刀光。\n他侧身——慢了半拍。肩头一凉，血飙出来。\n退。再退。后背撞上墙。\n没路了。\n他咧嘴。牙缝里全是血。然后冲出去。"},
        ],
        "source_url": "https://www.zhihu.com/search?type=content&q=写作句式节奏",
        "source_topic": "句式节奏控制",
        "confidence": 0.93,
    },
    {
        "name": "五感矩阵描写法",
        "category": "感官描写",
        "description": "每场景至少使用2种非视觉感官（听觉/嗅觉/触觉/味觉），感官绑定情绪，让读者身临其境。",
        "rules": [
            "每场景至少2种非视觉感官",
            "感官绑定情绪：冷风=紧张，桂花香=安心，铁锈味=危险",
            "声音分层：前景声+环境声+内心声",
            "触觉优先：温度、质地、湿度比颜色更能制造沉浸感",
            "嗅觉是记忆触发器：某种气味可以瞬间拉回回忆",
        ],
        "examples": [
            {"before": "房间里很安静，只有他一个人。", "after": "空调嗡鸣突然变得很响。他闻到自己的汗味——酸的，混着铁锈似的血腥气。指尖碰到桌面，冰凉滑腻，像摸到蛇皮。"},
        ],
        "source_url": "https://www.zhihu.com/search?type=content&q=五感描写写作技巧",
        "source_topic": "多感官描写技法",
        "confidence": 0.94,
    },
    {
        "name": "镜头语言三幕法",
        "category": "场景描写",
        "description": "远景建立空间(1-2句) → 中景推进叙事(人物动作) → 特写引爆情绪(细节)。像电影导演一样运镜。",
        "rules": [
            "远景建立空间：1-2句环境描写",
            "中景推进叙事：人物动作和互动",
            "特写引爆情绪：关键细节放大",
            "关键瞬间使用慢镜头：把一秒掰成十秒写",
            "用'先看到局部，再看到全貌'制造悬念",
        ],
        "examples": [
            {"before": "战场上到处都是尸体和破碎的武器，场面非常惨烈。", "after": "硝烟贴着地面爬。远处，残破的旗帜在风里一抽一抽。近处——一只断手还握着剑，指节发白。"},
        ],
        "source_url": "https://www.zhihu.com/search?type=content&q=小说镜头语言画面感",
        "source_topic": "影视化写作技法",
        "confidence": 0.92,
    },
    {
        "name": "光影情绪映射法",
        "category": "场景描写",
        "description": "用光影暗示情绪而非直白陈述。暖光=安全/温馨，冷光=压抑/孤独，逆光=悲壮/威胁。",
        "rules": [
            "用光影暗示情绪，不直接说",
            "写时间的光：晨曦/斜阳/路灯/月光，每种光有不同情绪",
            "写颜色的层次：别只用单色，写'砖红中泛着灰白'",
            "天气随剧情走：暴雨=冲突，雪=离别，雾=悬念",
            "光影变化=情绪变化：灯灭=绝望，烛燃=希望",
        ],
        "examples": [
            {"before": "黄昏时分，天色渐渐暗了下来。", "after": "落日在西天烧成绛紫色。云层边缘勾着一道金边——像烧红的刀刃。屋瓦上的余温还没散尽，炊烟就升起来了。"},
        ],
        "source_url": "https://www.zhihu.com/search?type=content&q=光影描写情绪渲染",
        "source_topic": "光影情绪技法",
        "confidence": 0.91,
    },
    {
        "name": "对话冲突法则",
        "category": "对话技巧",
        "description": "每句对话必须有目的+冲突。对话不是聊天，是'想得到什么/想掩盖什么/想激怒谁/想说服谁'。",
        "rules": [
            "每句对话必须有目的：想得到/掩盖/激怒/说服",
            "用动作、表情、停顿替代废话",
            "每个人说话方式不同：用词习惯、句子长度、口头禅",
            "关键对话中，说出来的和心里想的要相反(潜台词)",
            "避免'他说''她说'重复，用动作标签替代",
        ],
        "examples": [
            {"before": "'你为什么要这样做？'他问道。'因为我想帮你。'她回答说。", "after": "'为什么？'\n他盯着她——不是质问，是恳求。\n她把茶杯转了半圈。'帮你。'两个字轻得像叹气。\n他笑了一下，比哭还难看。'我不需要。'"},
        ],
        "source_url": "https://www.zhihu.com/search?type=content&q=小说对话写作技巧",
        "source_topic": "对话写作进阶",
        "confidence": 0.93,
    },
    {
        "name": "留白艺术：不说完",
        "category": "叙事技巧",
        "description": "关键节点少写一句，让读者脑补。章末卡在临界点。用沉默传递情绪。结尾不说破。",
        "rules": [
            "关键节点少写一句，让读者脑补",
            "章末卡在临界点：'他推开门，里面的场景让他瞳孔骤缩——'",
            "用沉默传递情绪：不写'他很难过'，写'他张了张嘴，什么都没说'",
            "对话留白：用动作替代台词",
            "结尾不说破：门关了、人走了、水溅裤脚，故事定格",
        ],
        "examples": [
            {"before": "他非常震惊，完全说不出话来。", "after": "他张嘴。\n闭上。\n又张嘴。\n最后只是把手机屏幕转向她。"},
        ],
        "source_url": "https://www.zhihu.com/search?type=content&q=小说留白写作技巧",
        "source_topic": "留白叙事技法",
        "confidence": 0.90,
    },
    {
        "name": "具体细节替代抽象概括",
        "category": "细节描写",
        "description": "用特指替代泛指，用案例替代概括，用物件细节替代千字解释。缺口茶杯、磨损戒指、泛黄照片——比千字解释更有力。",
        "rules": [
            "用特指替代泛指：'老槐树第三根枝杈上的铁铃铛'替代'村口的树'",
            "数字具体化：'缩短30%的时间'替代'大幅提升效率'",
            "品牌/地名/人名具体化",
            "物件细节：缺口茶杯、磨损戒指、泛黄照片",
        ],
        "examples": [
            {"before": "故乡是一个山清水秀的小村庄。", "after": "村口老槐树的第三根枝杈上，挂着一只生锈的铁铃铛。风一吹就哑着嗓子响——这声音，他听了十八年。"},
        ],
        "source_url": "https://www.zhihu.com/search?type=content&q=写作具体细节描写",
        "source_topic": "细节描写技法",
        "confidence": 0.94,
    },
    {
        "name": "批判思维注入法",
        "category": "写作风格",
        "description": "在核心论点后加入让步、自我质疑、对立观点。避免完美结论，保留'未定结论'。人类倾向保留不确定性，AI倾向给出完美结论。",
        "rules": [
            "在核心论点后加入让步：'但这个结论可能不适用于...'",
            "加入自我质疑：'我之前也这么想，直到看到一个反例'",
            "加入对立观点：'有学者提出完全相反的看法...'",
            "结论加限制：'仍需进一步验证''本研究存在...局限'",
            "避免完美结论",
        ],
        "examples": [
            {"before": "实验结果表明，该方法具有显著效果。", "after": "实验数据确实漂亮。但说实话——样本只有三十人，而且全是大学生。换一批人呢？不好说。"},
        ],
        "source_url": "https://www.zhihu.com/search?type=content&q=AI写作去痕迹批判思维",
        "source_topic": "批判思维注入",
        "confidence": 0.92,
    },
    {
        "name": "不完美美学注入",
        "category": "写作风格",
        "description": "保留轻微冗余、口语化词汇、思考停顿。用破折号、省略号体现人类思维的跳跃和不完美。",
        "rules": [
            "保留轻微冗余：'其实说白了''你猜怎么着'",
            "插入口语化词汇：'说实话''有点迷''这里要划重点'",
            "用破折号、省略号体现思考停顿",
            "偶尔的语法不完美：口语化断句、重复强调",
            "加入'我觉得''我发现''有意思的是'等主观引导",
        ],
        "examples": [
            {"before": "数据分析显示，用户偏好发生了显著变化。", "after": "数据跑出来的时候，我愣了一下。用户偏好——变了。变得还挺彻底。说实话，有点意外。"},
        ],
        "source_url": "https://www.zhihu.com/search?type=content&q=AI写作去痕迹口语化",
        "source_topic": "不完美美学技法",
        "confidence": 0.91,
    },
    {
        "name": "动作替代形容词法则",
        "category": "描写技巧",
        "description": "禁止直接陈述情绪和状态。用动作链替代心理描写。每个情绪至少找到3个外化动作。动词优先。",
        "rules": [
            "禁止直接陈述情绪：不写'他很生气'，写'他把烟掐灭在手心'",
            "禁止直接陈述状态：不写'房间很乱'，写'吃剩的外卖盒子堆在桌角'",
            "用动作链替代心理描写",
            "每个情绪至少找到3个外化动作",
            "动词优先：一个精准动词胜过三个形容词",
        ],
        "examples": [
            {"before": "他非常紧张，心跳加速。", "after": "他把烟掐灭又点上。打火机按了三次——没着。第四次，手在抖。"},
            {"before": "她非常开心，笑容满面。", "after": "她把皮凉鞋脱了。赤脚在人行道的方砖上——一格，一格，跳过去。"},
        ],
        "source_url": "https://www.zhihu.com/search?type=content&q=show don't tell 写作技巧",
        "source_topic": "Show Don't Tell 技法",
        "confidence": 0.95,
    },
    {
        "name": "节奏控制：快慢交替",
        "category": "叙事技巧",
        "description": "打斗/冲突用短句连击，心理/回忆用长句铺陈。一章内至少2次节奏变化。用段落长度控制阅读速度。高潮前蓄力。",
        "rules": [
            "打斗/冲突/意外：短句连击，每句不超过15字",
            "心理/回忆/风景：长句铺陈，但结尾短句收住",
            "一章内至少2次节奏变化：快→慢→快",
            "用段落长度控制阅读速度：短段=快读，长段=慢品",
            "高潮前蓄力：放慢节奏堆细节，然后短句爆发",
        ],
        "examples": [
            {"before": "战斗非常激烈，双方你来我往，打了很久才分出胜负。", "after": "刀光。\n他侧身——慢了半拍。肩头一凉，血飙出来。\n退。再退。后背撞上墙。\n没路了。\n他咧嘴。牙缝里全是血。然后冲出去。"},
        ],
        "source_url": "https://www.zhihu.com/search?type=content&q=小说节奏控制技巧",
        "source_topic": "节奏控制技法",
        "confidence": 0.93,
    },
    {
        "name": "AI高频词替换表",
        "category": "AI痕迹消除",
        "description": "系统替换AI生成文本中的高频特征词汇，用更自然的人类表达替代。这是去AI痕迹最直接有效的方法。",
        "rules": [
            "'值得注意的是' → '有意思的是'",
            "'综上所述' → '说到底'",
            "'首先/其次/最后' → '头一件事/再来/末了'",
            "'通过...实现...' → '靠...做到...'",
            "'进行/做出/加以' → '做/给出/再'",
            "'显著/呈现出/具有重要' → '明显/显出/很关键'",
            "'毫无疑问/毋庸置疑' → '没说的/不用怀疑'",
            "'显然/必定/必然' → '明摆着/肯定/一定'",
        ],
        "examples": [
            {"before": "值得注意的是，通过系统性的优化方案，我们实现了显著的效率提升。", "after": "有意思的是，靠这套优化方案，效率确实提上来了——还挺明显。"},
        ],
        "source_url": "https://www.zhihu.com/search?type=content&q=AI写作特征词替换",
        "source_topic": "AI特征词替换策略",
        "confidence": 0.96,
    },
    {
        "name": "主观声音注入法",
        "category": "写作风格",
        "description": "加入第一人称感受和判断。避免上帝视角的客观陈述。用'笔者发现''结合调研来看'替代被动语态。",
        "rules": [
            "加入第一人称感受：'我读到这段的时候，后背发凉'",
            "加入个人判断：'以我的经验来看，这条路走不通'",
            "加入情感反应：'看到这个数据，我差点把咖啡喷屏幕上'",
            "避免上帝视角的客观陈述",
            "用'笔者发现''结合调研来看'替代被动语态",
        ],
        "examples": [
            {"before": "该政策的实施效果需要进一步观察。", "after": "政策落地三个月了。效果？我盯着数据看了半天——说实话，跟预期差得有点远。"},
        ],
        "source_url": "https://www.zhihu.com/search?type=content&q=写作主观声音个人风格",
        "source_topic": "主观声音技法",
        "confidence": 0.90,
    },
    {
        "name": "段落呼吸控制",
        "category": "句式结构",
        "description": "用段落长度控制阅读节奏。短段制造紧迫感，长段营造沉浸感。避免AI均匀段落长度的模板化特征。",
        "rules": [
            "关键情节用单句成段，制造冲击力",
            "描写段落不超过5行",
            "对话段落尽量短，每段不超过3句",
            "段落长度要有明显变化：长→短→长→极短",
            "避免连续3段长度相近",
        ],
        "examples": [
            {"before": "他走进房间，环顾四周。房间里很暗，只有一盏灯。他走到桌前，拿起那封信。信上写着他的名字。他打开信，开始阅读。", "after": "他推门。\n\n房间暗得像口井。唯一的光——桌上那盏灯，昏黄，摇摇欲坠。\n\n他走过去。\n\n信。\n\n上面是他的名字。三个字，像三根钉子。"},
        ],
        "source_url": "https://www.zhihu.com/search?type=content&q=小说段落节奏控制",
        "source_topic": "段落节奏技法",
        "confidence": 0.92,
    },
]


def inject_techniques():
    with open(KB_PATH, 'r', encoding='utf-8') as f:
        kb = json.load(f)

    added = 0
    for tech in NEW_TECHNIQUES:
        key = hashlib.md5(
            (tech["source_url"] + tech["name"]).encode()
        ).hexdigest()[:16]

        tech_id = f"manual_inject_{key}"
        if tech_id in kb:
            kb[tech_id]["times_reinforced"] += 1
            continue

        kb[tech_id] = {
            "technique_id": tech_id,
            "name": tech["name"],
            "category": tech["category"],
            "description": tech["description"],
            "rules": tech["rules"],
            "examples": tech["examples"],
            "source_url": tech["source_url"],
            "source_topic": tech["source_topic"],
            "confidence": tech["confidence"],
            "learned_at": datetime.now().isoformat(),
            "times_reinforced": 1,
        }
        added += 1

    with open(KB_PATH, 'w', encoding='utf-8') as f:
        json.dump(kb, f, ensure_ascii=False, indent=2)

    print(f"✅ 知识库更新完成")
    print(f"   新增技法: {added}条")
    print(f"   总技法数: {len(kb)}条")
    cats = set(t["category"] for t in kb.values())
    print(f"   覆盖类别: {len(cats)}个 - {cats}")


if __name__ == "__main__":
    inject_techniques()
