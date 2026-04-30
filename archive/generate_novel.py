#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

NOVEL_TYPES = {
    "1": {"name": "穿越古代", "description": "现代人意外穿越到古代"},
    "2": {"name": "穿越星际", "description": "穿越到未来星际时代"},
    "3": {"name": "玄幻修仙", "description": "仙侠世界修仙问道"},
    "4": {"name": "都市异能", "description": "现代都市拥有特殊能力"},
    "5": {"name": "悬疑推理", "description": "烧脑悬疑抽丝剥茧"},
    "6": {"name": "霸道总裁", "description": "都市言情豪门恋曲"},
}

WORLDS = {
    "1": {"name": "大唐盛世", "description": "繁华的长安城万国来朝"},
    "2": {"name": "大宋风华", "description": "文雅宋词山水画境"},
    "3": {"name": "大明王朝", "description": "天子守国门郑和下西洋"},
    "4": {"name": "架空虚构", "description": "完全虚构的幻想世界"},
    "5": {"name": "现代都市", "description": "当代社会都市风云"},
}

MALE_LEADS = {
    "1": {"name": "冷傲王爷", "description": "高冷傲娇权倾天下"},
    "2": {"name": "温柔书生", "description": "温文尔雅才华横溢"},
    "3": {"name": "霸道总裁", "description": "冷酷多金强势宠溺"},
    "4": {"name": "热血少年", "description": "意气风发勇往直前"},
    "5": {"name": "腹黑谋士", "description": "城府深沉智计无双"},
    "6": {"name": "忠犬侍卫", "description": "忠诚守护默默付出"},
}

FEMALE_LEADS = {
    "1": {"name": "活泼医女", "description": "古灵精怪医术高超"},
    "2": {"name": "大家闺秀", "description": "温婉贤淑知书达理"},
    "3": {"name": "倔强庶女", "description": "不甘平庸逆袭人生"},
    "4": {"name": "飒爽女将", "description": "英姿飒爽征战沙场"},
    "5": {"name": "绝美女配", "description": "红颜祸水倾国倾城"},
    "6": {"name": "独立女强", "description": "事业有成坚强独立"},
}

PLOT_TYPES = {
    "1": {"name": "甜宠日常", "description": "轻松甜蜜宠溺无极限"},
    "2": {"name": "虐恋情深", "description": "相爱相杀虐心催泪"},
    "3": {"name": "复仇逆袭", "description": "重生复仇打脸虐渣"},
    "4": {"name": "共同成长", "description": "相互扶持并肩前行"},
    "5": {"name": "欢喜冤家", "description": "冤家路窄日久生情"},
    "6": {"name": "阴谋阳谋", "description": "权谋争斗智计百出"},
}

TAGS = {
    "1": {"name": "重生", "description": "主角带着前世记忆重生"},
    "2": {"name": "系统", "description": "拥有神秘系统辅助"},
    "3": {"name": "空间", "description": "拥有随身空间异能"},
    "4": {"name": "医术", "description": "精通医术救人无数"},
    "5": {"name": "经商", "description": "商业头脑发财致富"},
    "6": {"name": "宫斗", "description": "后宫争宠斗智斗勇"},
    "7": {"name": "江湖", "description": "武侠江湖恩怨情仇"},
    "8": {"name": "星际", "description": "星际探索冒险漂流"},
}

WORD_COUNTS = {
    "1": {"name": "短篇", "min": 10000, "max": 15000, "description": "10000-15000字"},
    "2": {"name": "中篇", "min": 30000, "max": 50000, "description": "30000-50000字"},
    "3": {"name": "长篇", "min": 100000, "max": 200000, "description": "100000-200000字"},
}

CHAPTER_COUNTS = {
    "1": {"name": "5章", "value": 5},
    "2": {"name": "10章", "value": 10},
    "3": {"name": "20章", "value": 20},
    "4": {"name": "30章", "value": 30},
}


def print_header(title):
    print("\n" + "=" * 60)
    print("  " + title)
    print("=" * 60)


def print_options(options, multi_select=False):
    for key, val in options.items():
        if multi_select:
            print("  [" + key + "] " + val["name"])
        else:
            print("  [" + key + "] " + val["name"] + " - " + val["description"])
    print("-" * 60)


def get_single_selection(title, options):
    print_header(title)
    print_options(options)
    while True:
        selection = input("请输入选项编号: ").strip()
        if selection in options:
            return selection
        print("选项无效，请重新输入!")


def get_multi_selection(title, options, min_select=1):
    print_header(title + "（可多选，如：1,3,5）")
    print_options(options, multi_select=True)
    print("提示：输入多个选项用逗号分隔")
    while True:
        selection = input("请输入选项编号: ").strip()
        if not selection:
            print("选项不能为空!")
            continue
        selected = []
        for s in selection.split(','):
            s = s.strip()
            if s in options:
                selected.append(s)
        if len(selected) >= min_select:
            return selected
        print("至少需要选择 %d 个选项!" % min_select)


def generate_outline(info):
    male = info["male_lead"]["name"]
    female = info["female_lead"]["name"]
    world = info["world"]["name"]
    plot_type = info["plot_type"]["name"]
    tags = [info["tags"][i]["name"] for i in info["tags"]]
    chapter_count = info["chapter_count"]
    word_target = info["word_count"]["min"]

    outline = []
    outline.append("=" * 60)
    outline.append("                    小说大纲")
    outline.append("=" * 60)
    outline.append("")
    outline.append("【基本信息】")
    outline.append("小说类型: " + info["novel_type"]["name"])
    outline.append("世界设定: " + world)
    outline.append("男主设定: " + male)
    outline.append("女主设定: " + female)
    outline.append("情节类型: " + plot_type)
    outline.append("特殊标签: " + "、".join(tags))
    outline.append("章节数量: " + str(chapter_count) + " 章")
    outline.append("目标字数: " + str(word_target) + " 字")
    outline.append("")

    outline.append("【故事背景】")
    if world == "大唐盛世":
        outline.append(world + "，经济繁荣，文化昌盛，万国来朝。")
        outline.append("但朝堂之上暗流涌动，各方势力蠢蠢欲动。")
    elif world == "大宋风华":
        outline.append(world + "，文风鼎盛，市井繁华。")
        outline.append("然而边关战事频仍，国家命运悬于一线。")
    elif world == "大明王朝":
        outline.append(world + "，天子守国门，郑和下西洋。")
        outline.append("宦官当道，东林党争，朝局动荡不安。")
    elif world == "架空虚构":
        outline.append("一个完全虚构的世界，玄幻莫测。")
        outline.append("存在着各种神秘的力量和未知的危险。")
    else:
        outline.append(world + "，当代都市，繁华与平凡交织。")

    outline.append("")

    outline.append("【主角设定】")
    outline.append("男主角: " + male)
    outline.append("- 身份：权贵之后/普通青年/神秘强者")
    outline.append("- 性格：高冷/温柔/腹黑/热血")
    outline.append("- 能力：智计无双/实力强横/商业头脑")
    outline.append("")
    outline.append("女主角: " + female)
    outline.append("- 身份：名门贵女/平凡女子/女强人")
    outline.append("- 性格：活泼/温婉/倔强/飒爽")
    outline.append("- 能力：医术/经商/武艺/智慧")
    outline.append("")

    outline.append("【情节主线】")
    if plot_type == "甜宠日常":
        outline.append("两人从相识到相知，经历各种甜蜜日常，最终修成正果。")
    elif plot_type == "虐恋情深":
        outline.append("两人相爱却受尽磨难，历经波折终于相守。")
    elif plot_type == "复仇逆袭":
        outline.append("主角被人陷害，重生后复仇，最终收获爱情。")
    elif plot_type == "共同成长":
        outline.append("两人相互扶持，共同面对困难，一起成长。")
    elif plot_type == "欢喜冤家":
        outline.append("两人从互相看不顺眼，到日久生情。")
    else:
        outline.append("两人在权谋斗争中相知相爱。")

    outline.append("")

    outline.append("【章节大纲】")
    if chapter_count == 5:
        chapters = [
            ("第一章", "命运的相遇", "两人意外相遇，命运从此交织"),
            ("第二章", "暗生情愫", "相处中渐生情愫，感情萌芽"),
            ("第三章", "风波骤起", "遭遇危机或阻碍，感情受考验"),
            ("第四章", "真情告白", "突破障碍表白心意，确认关系"),
            ("第五章", "携手余生", "经历考验，最终走到一起"),
        ]
    elif chapter_count == 10:
        chapters = [
            ("第一章", "意外相遇", "命运的安排，两人相遇"),
            ("第二章", "初步了解", "开始认识，留下印象"),
            ("第三章", "渐生情愫", "相处中产生好感"),
            ("第四章", "明确心意", "意识到喜欢对方"),
            ("第五章", "遭遇危机", "外部困难出现"),
            ("第六章", "感情受挫", "误会或阻碍，感情受挫"),
            ("第七章", "努力挽回", "积极解决问题"),
            ("第八章", "重新在一起", "解除误会，感情升温"),
            ("第九章", "危机再现", "更大的考验来临"),
            ("第十章", "圆满结局", "克服困难，携手余生"),
        ]
    elif chapter_count == 20:
        chapters = [
            ("第一章", "穿越/重生", "主角来到异世界/获得新生"),
            ("第二章", "初识世界", "了解环境，适应新身份"),
            ("第三章", "意外发现", "发现金手指/特殊能力"),
            ("第四章", "小试牛刀", "初次使用能力"),
            ("第五章", "引起注意", "被某人注意到"),
            ("第六章", "结识女主", "与女主相遇"),
            ("第七章", "产生好感", "相处中渐生情愫"),
            ("第八章", "第一个副本", "经历第一个事件/冲突"),
            ("第九章", "感情升温", "关系更进一步"),
            ("第十章", "危机降临", "遭遇重大危机"),
            ("第十一章", "艰难抉择", "面临艰难选择"),
            ("第十二章", "真相大白", "揭开某个秘密"),
            ("第十三章", "感情危机", "误会或外部阻挠"),
            ("第十四章", "努力挽回", "积极解决问题"),
            ("第十五章", "突破自我", "能力/心境提升"),
            ("第十六章", "重新在一起", "感情回归正轨"),
            ("第十七章", "最终boss", "面对最大敌人"),
            ("第十八章", "生死决战", "激烈的最终对决"),
            ("第十九章", "胜利归来", "战胜敌人，获得胜利"),
            ("第二十章", "圆满结局", "大婚/圆满的结局"),
        ]
    else:
        chapters = [
            ("第一章", "开篇", "故事开始"),
            ("第二章", "相遇", "主角相遇"),
            ("第三章", "发展", "感情发展"),
            ("第四章", "高潮", "矛盾冲突"),
            ("第五章", "结局", "圆满结局"),
        ]

    for num, title, desc in chapters:
        outline.append("  " + num + "：" + title)
        outline.append("    - " + desc)

    outline.append("")
    outline.append("=" * 60)

    return "\n".join(outline)


def generate_chapter_content(chapter_info, info, chapter_num):
    male = info["male_lead"]["name"]
    female = info["female_lead"]["name"]
    world = info["world"]["name"]

    templates = {
        1: {
            "opening": "命运有时候就是如此奇妙。",
            "content": "在" + world + "的某个角落，一场意外的相遇改变了一切。\n\n",
            "ending": "从这一刻起，两人的命运开始交织。"
        },
        2: {
            "opening": "日子一天天过去。",
            "content": "相处的时间越长，" + male + "发现自己越来越离不开" + female + "。\n\n",
            "ending": "不知不觉中，心已经沉沦。"
        },
        3: {
            "opening": "然而，平静之下暗流涌动。",
            "content": male + "的身份注定了他无法过普通人的生活。朝廷的明争暗斗，家族的尔虞我诈，很快就将矛头指向了她。\n\n",
            "ending": "一场风暴即将来临。"
        },
        4: {
            "opening": "那是一个月色皎洁的夜晚。",
            "content": "他终于鼓起勇气，说出了藏在心底的话。\n\n",
            "ending": "月光下，两人紧紧相拥。"
        },
        5: {
            "opening": "经历了重重困难，他们终于走到了一起。",
            "content": male + "为她举办了一场盛大的婚礼，整个" + world + "都为之瞩目。\n\n",
            "ending": "从此，他们携手余生，再不分离。"
        },
    }

    if chapter_num in templates:
        template = templates[chapter_num]
    else:
        template = templates.get(chapter_num % 5 + 1, templates[1])

    content = template["opening"] + "\n\n" + template["content"] + template["ending"]
    return content


def generate_full_content(info):
    male = info["male_lead"]["name"]
    female = info["female_lead"]["name"]
    world = info["world"]["name"]
    plot_type = info["plot_type"]["name"]
    tags = [info["tags"][i]["name"] for i in info["tags"]]
    chapter_count = info["chapter_count"]
    word_target = info["word_count"]["min"]

    chapters = []
    for i in range(chapter_count):
        chapter_num = i + 1
        title = "第" + str(chapter_num) + "章"

        if chapter_count == 5:
            titles = ["命运的相遇", "暗生情愫", "风波骤起", "真情告白", "携手余生"]
            title = titles[i] if i < len(titles) else "第" + str(chapter_num) + "章"
        elif chapter_count == 10:
            titles = ["意外相遇", "初步了解", "渐生情愫", "明确心意", "遭遇危机",
                     "感情受挫", "努力挽回", "重新在一起", "危机再现", "圆满结局"]
            title = titles[i] if i < len(titles) else "第" + str(chapter_num) + "章"
        elif chapter_count >= 20:
            titles = ["穿越/重生", "初识世界", "意外发现", "小试牛刀", "引起注意",
                     "结识女主", "产生好感", "第一个副本", "感情升温", "危机降临",
                     "艰难抉择", "真相大白", "感情危机", "努力挽回", "突破自我",
                     "重新在一起", "最终boss", "生死决战", "胜利归来", "圆满结局"]
            title = titles[i] if i < len(titles) else "第" + str(chapter_num) + "章"

        content = generate_chapter_content({"title": title}, info, chapter_num)

        chapters.append({
            "title": title,
            "content": content
        })

    total_content = "\n\n".join([ch["content"] for ch in chapters])
    current_words = len(total_content)

    if word_target > current_words and chapter_count > 0:
        expansion_needed = word_target - current_words
        extra_per_chapter = expansion_needed // chapter_count

        expanded_chapters = []
        for chapter in chapters:
            base_content = chapter["content"]
            base_len = len(base_content)

            expanded = base_content
            target_len = base_len + extra_per_chapter

            while len(expanded) < target_len:
                expanded = expanded + base_content[len(base_content) // 3:]

            expanded = expanded[:target_len]
            expanded_chapters.append({
                "title": chapter["title"],
                "content": expanded
            })
        chapters = expanded_chapters

    return {
        "title": world + " " + male + "与" + female,
        "chapters": chapters,
        "theme": "、".join([world, male, female, plot_type] + tags),
        "word_count": sum(len(ch["content"]) for ch in chapters),
        "chapters_count": len(chapters),
        "info": info,
    }


def save_novel(novel, include_outline=None):
    filename = novel["title"] + ".txt"
    save_path = "manuscripts/" + filename
    os.makedirs("manuscripts", exist_ok=True)

    with open(save_path, "w", encoding="utf-8") as f:
        f.write("《" + novel["title"] + "》\n\n")
        f.write("类型: " + novel["info"]["novel_type"]["name"] + "\n")
        f.write("世界: " + novel["info"]["world"]["name"] + "\n")
        f.write("男主: " + novel["info"]["male_lead"]["name"] + "\n")
        f.write("女主: " + novel["info"]["female_lead"]["name"] + "\n")
        f.write("情节: " + novel["info"]["plot_type"]["name"] + "\n")
        tags = [novel["info"]["tags"][i]["name"] for i in novel["info"]["tags"]]
        f.write("标签: " + "、".join(tags) + "\n")
        f.write("章节: " + str(novel["chapters_count"]) + " 章\n")
        f.write("字数: " + str(novel["word_count"]) + " 字\n\n")

        if include_outline:
            f.write("=" * 60 + "\n\n")
            f.write("【小说大纲】\n\n")
            f.write(include_outline)
            f.write("\n\n")

        f.write("=" * 60 + "\n\n")
        f.write("【正文】\n\n")

        for i, chapter in enumerate(novel["chapters"]):
            f.write("【第" + str(i + 1) + "章：" + chapter["title"] + "】\n\n")
            f.write(chapter["content"])
            f.write("\n\n" + "-" * 60 + "\n\n")

    return save_path


def main():
    print("\n" + "=" * 60)
    print("           智能小说生成器")
    print("           Novel Writing Assistant")
    print("=" * 60)

    print("\n欢迎使用智能小说生成器！")
    print("请按照提示选择小说各项设定（支持多选）")
    print("确认后我将先生成大纲，您满意后再生成完整内容")

    print("\n" + "-" * 60)
    print("【第一步】选择小说类型")
    novel_type_key = get_single_selection("小说类型", NOVEL_TYPES)
    novel_type = NOVEL_TYPES[novel_type_key]

    print("\n【第二步】选择世界环境")
    world_key = get_single_selection("世界环境", WORLDS)
    world = WORLDS[world_key]

    print("\n【第三步】选择男主设定")
    male_key = get_single_selection("男主设定", MALE_LEADS)
    male_lead = MALE_LEADS[male_key]

    print("\n【第四步】选择女主设定")
    female_key = get_single_selection("女主设定", FEMALE_LEADS)
    female_lead = FEMALE_LEADS[female_key]

    print("\n【第五步】选择情节类型")
    plot_key = get_single_selection("情节类型", PLOT_TYPES)
    plot_type = PLOT_TYPES[plot_key]

    print("\n【第六步】选择特殊标签（可多选）")
    tag_keys = get_multi_selection("特殊标签", TAGS, min_select=0)
    tags = [TAGS[k] for k in tag_keys]

    print("\n【第七步】选择章节数量")
    chapter_key = get_single_selection("章节数量", CHAPTER_COUNTS)
    chapter_count = CHAPTER_COUNTS[chapter_key]["value"]

    print("\n【第八步】选择小说长度")
    word_key = get_single_selection("小说长度", WORD_COUNTS)
    word_count = WORD_COUNTS[word_key]

    info = {
        "novel_type": novel_type,
        "world": world,
        "male_lead": male_lead,
        "female_lead": female_lead,
        "plot_type": plot_type,
        "tags": tag_keys,
        "chapter_count": chapter_count,
        "word_count": word_count,
    }

    print_header("您的选择汇总")
    print("  小说类型: " + novel_type["name"])
    print("  世界环境: " + world["name"])
    print("  男主设定: " + male_lead["name"])
    print("  女主设定: " + female_lead["name"])
    print("  情节类型: " + plot_type["name"])
    if tags:
        print("  特殊标签: " + "、".join([t["name"] for t in tags]))
    else:
        print("  特殊标签: 无")
    print("  章节数量: " + str(chapter_count) + " 章")
    print("  小说长度: " + word_count["description"])
    print("-" * 60)

    print("\n正在生成大纲...")
    outline = generate_outline(info)

    print_header("小说大纲预览")
    print(outline)

    confirm = input("\n大纲满意吗？确认生成完整小说？(y/n/q退出): ").strip().lower()
    if confirm == "q":
        print("已退出。")
        return
    if confirm != "y":
        print("已取消生成。")
        return

    print("\n正在生成小说内容（约 " + str(word_count["min"]) + " 字）...")

    novel = generate_full_content(info)
    save_path = save_novel(novel, outline)

    print_header("小说生成完成!")
    print("  标题: 《" + novel["title"] + "》")
    print("  章节: " + str(novel["chapters_count"]) + " 章")
    print("  字数: " + str(novel["word_count"]) + " 字")
    print("  保存: " + save_path)
    print("=" * 60)


if __name__ == "__main__":
    main()
