#!/usr/bin/env python3
"""
NWACS 智能编排器 + 章纲注入 - 《黑日藏锋》第1-10章
编排器管理所有NWACS模块(引擎/记忆/检测)，章纲注入引擎生成
不手写API调用，全部由NWACS工具链管理
"""
import os, sys, time, re, glob

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
CORE_V8_DIR = os.path.join(PROJECT_DIR, "core", "v8")
for d in [PROJECT_DIR, CORE_V8_DIR]:
    if d not in sys.path:
        sys.path.insert(0, d)

OUTPUT_DIR = os.path.join(PROJECT_DIR, "黑日藏锋")
os.makedirs(OUTPUT_DIR, exist_ok=True)

CHAPTERS = [
    (1, "黑日之下",
     "林锋穿越醒来，后脑勺疼得像被人砸过。天上挂着一轮黑色太阳，边缘暗红，不发热。铁柱——猎户的儿子，土系下品灵根，骨架大得不像杂役——塞给他半块杂粮饼子，硬得刮嗓子。王虎，凝气三层，三角眼，脸上有道疤，挥着竹鞭催人下矿。草鞋断了绳，大脚趾露在外面。脚踝上扣着锁魂环，刻着'矿奴'两个字。杂役院里全是穿灰布衣的人，瘦骨嶙峋，眼神空洞。这就是黑日世界。",
     ["穿越醒来后脑勺疼", "黑色太阳不发热", "铁柱塞杂粮饼子", "王虎竹鞭催人", "锁魂环刻矿奴", "杂役院灰布衣"]),
    (2, "矿道",
     "矿道入口在半山腰，石头凿出来的口子，两米宽，三米高。光明石嵌在洞壁上，发着冷光，照得人脸发青。老赵是监工，手里攥着铁棍，敲着洞壁警告——岔道多，别乱走，走丢了没人找。林锋和铁柱被分到丙区岔道，废灵石矿脉，岩壁上全是暗红色的纹路。铁柱教他顺着纹砸，省力。手掌磨出水泡，破了，流水。矿道里阴冷潮湿，石粉呛得人咳嗽，硫磺味混着汗臭。",
     ["矿道入口半山腰", "光明石冷光", "老赵铁棍警告", "丙区废灵石矿脉", "铁柱教砸矿", "手掌磨泡流水"]),
    (3, "废灵石",
     "矿难来得突然。轰隆一声，气浪冲过来，碎石堵死了岔道口。铁柱额头被飞石划开一道口子，血顺着眉毛流进眼睛里。外面的人喊了几声，说明天再挖——不管里面的人死活。林锋没慌。他往矿道深处走，发现一处岩壁温度不对——别的岩壁冰凉，这块却是温热的。他抄起铁镐砸下去。岩壁裂开，里面是个天然岩洞，大得看不到顶。",
     ["矿难塌方轰隆", "铁柱额头受伤", "外面放弃救援", "岩壁温度异常", "砸开岩壁", "天然岩洞"]),
    (4, "暗红色的光",
     "岩洞中央嵌着一块人头大的暗红色石头。内部的光芒像心跳一样明灭。林锋伸手去碰——烫。不是皮肤烫，是骨头烫。热流顺着指尖灌进丹田。意识坠入暗红色的漩涡，他看到了幻象——天上的黑日像蛋壳一样裂开，碎片四散飞落。醒来时掌心多了一道疤，像被烙铁烫过。丹田里有什么东西在转——真气种子。",
     ["暗红石头心跳明灭", "触碰烫进骨头", "热流灌入丹田", "黑日碎裂幻象", "掌心留疤", "真气种子转动"]),
    (5, "藏锋诀",
     "碎日残片灌入了一套功法——藏锋诀。真气不走经脉，贴着骨头表面流动，外表看起来和凡人一模一样，谁也看不出来。三天时间，凝气一层。附带金针术——真气凝成针，刺入穴位，可救人也可杀人。他试了一拳，铁镐砸在岩壁上，砸出一个坑。然后仔细抹平痕迹。藏锋诀三层：敛息、藏脉、隐骨。一层比一层深。",
     ["功法传承灌入", "真气贴骨走", "三天凝气一层", "金针术", "一拳一坑", "三层敛息藏脉隐骨"]),
    (6, "小灰",
     "废井边的碎石堆里，林锋捡到一只暗影狼幼崽。左后腿断了，肋骨凹进去一块，快死了。他抱回岩洞，用金针术接骨——真气凝成针，刺入骨缝，一点一点把碎骨拼回去。又从碎日残片里分出一丝真气渡过去。喂泡软的饼子。起名叫小灰。小灰有双暗银色的眼睛，一直盯着他看。三天后，小灰站起来了，舔他的手指。",
     ["废井捡幼崽", "金针术接骨", "真气渡命", "起名小灰", "暗银眼睛", "三天后站起来"]),
    (7, "凝气二层",
     "突破凝气二层失败了两次。第一次真气逆行，一口血吐出来，嗓子眼里全是腥甜味。第二次丹田差点炸了，疼得他蜷在地上像只虾。第三次他悟出来了——不灌，让碎日残片的力量自己渗，像水渗进沙子。这叫引字诀。真气液化，凝气二层成了。一拳砸在岩壁上，三寸深的拳印。小灰也觉醒了——暗影潜行，能融入阴影，肉眼看不见。",
     ["两次突破失败", "真气逆行吐血", "悟出引字诀", "凝气二层成", "三寸拳印", "小灰暗影潜行"]),
    (8, "杂役院的老鼠",
     "林锋找到瘦猴侯三——杂役院里最机灵的人，瘦得像根竹竿。一块饼子换一条信息。他又放出消息：收信息，换食物。三天来了十个人，七天来了三十个。他建了三类信息系统：人物——谁是谁，什么背景；事件——发生了什么，谁参与了；资源——哪里有东西，怎么弄到。然后锁定目标：三个月后的外门考核。杂役进外门，唯一的机会。",
     ["找瘦猴侯三", "饼子换信息", "三天十人七天三十", "三类信息系统", "人物事件资源", "锁定外门考核"]),
    (9, "第一次交易",
     "厨房老李透露了一条消息——赵师兄在找赤阳石。林锋让瘦猴放出风声：矿道深处有赤阳石矿脉。赵师兄找上门来，花两块灵石买了这条消息。林锋分给瘦猴半块，老李半块。三方都得了好处，没人知道消息源头是谁。第一笔情报交易完成。模板建立：信息变成灵石，灵石变成分成。零风险，零暴露。",
     ["老李透露消息", "赤阳石情报", "赵师兄两块灵石", "三方分成", "源头无人知晓", "情报交易模板"]),
    (10, "周老",
     "杂役院最偏僻的角落有间石洞，住着周老。没人知道他在这儿待了多久。林锋注意到一件事——周老的手不像干杂活的手。指节分明，虎口有茧，那是握剑的茧。眼睛偶尔锐利得像刀子。周老让林锋帮忙搬酒坛，坛子上刻着三级聚灵阵。他看了林锋一眼，说：藏得不错。又说：别碰太多。林锋决定搞清楚这个人到底是谁。",
     ["偏僻石洞周老", "握剑的茧", "眼睛锐如刀", "三级聚灵阵酒坛", "藏得不错", "决定调查"]),
]

def main():
    print("=" * 60)
    print("  NWACS 智能编排器 + 章纲注入")
    print("  调度: IntelligentOrchestrator")
    print("  引擎: SmartCreativeEngine (DeepSeek)")
    print("  记忆: NovelMemoryManager")
    print("=" * 60)

    from core.v8.intelligent_orchestrator import IntelligentOrchestrator
    orch = IntelligentOrchestrator()
    print("✅ IntelligentOrchestrator 已初始化")

    orch.load_module("engine")
    orch.load_module("novel_memory")
    print("✅ 核心模块已加载 (engine + memory)\n")

    engine = orch._get_instance("engine")
    memory = orch._get_instance("novel_memory")

    NOVEL_CONTEXT = """【小说设定 - 必须严格遵守】
书名：《黑日藏锋》
主角：林锋（穿越者，前世工地搬砖，穿越到黑日世界成为黑曜矿场矿奴）
世界：黑日世界，天上挂黑色太阳，边缘暗红，不发热。修真世界，等级森严。
地点：黑曜矿场杂役院，矿奴穿灰布衣，脚踝扣锁魂环刻"矿奴"二字。
核心设定：林锋获得碎日残片，习得藏锋诀（真气贴骨走，外表如凡人），金针术（真气凝针刺穴）。
伙伴：铁柱（猎户儿子，土系下品灵根，骨架大，憨厚）、小灰（暗影狼幼崽，暗银眼睛，会暗影潜行）。
信息网：瘦猴侯三（杂役院情报头子），厨房老李（消息源）。
神秘人物：周老（杂役院角落石洞，握剑的茧，三级聚灵阵酒坛，深不可测）。
目标：三个月后外门考核，杂役进外门唯一机会。"""

    total_chars = 0
    for ch_num, ch_title, ch_summary, ch_points in CHAPTERS:
        print(f"[第{ch_num}章] {ch_title} ", end="", flush=True)
        t0 = time.time()

        points_text = "\n".join(f"  - {p}" for p in ch_points)

        system_prompt = f"""你是一位拥有15年经验的顶级玄幻小说作家。
文笔老练、节奏精准、人物鲜活，读者沉浸感极强。

{NOVEL_CONTEXT}

【核心写作原则】
1. 沉浸式叙事：让读者忘记是在"读"小说，而是"经历"故事
2. 节奏控制：紧张场景用短句加速，抒情场景用长句铺陈
3. 人物驱动：情节由人物性格和动机自然推动
4. 细节真实：通过具体的感官细节建立真实感
5. 对话自然：每个角色的说话方式独一无二

【去AI铁律】
- 禁止"首先其次最后""值得注意的是""综上所述"等AI模板句式
- 句长剧烈交替：30%短句(3-10字)+50%中句(11-25字)+20%长句(26-50字)
- 情绪要有撕裂感：恨到极致突然温柔，笑到一半突然哭
- 加入人类的犹豫、自我纠正、思维跳跃
- 每500字至少1处意外用词或非常规搭配
- 关键情节用单句成段制造冲击力
- 加入本土生活细节：烟火气、人情世故
- 口语化叙述：说实话、妈的、操、谁懂啊

【输出格式】
- 直接输出小说正文，不要任何解释标记前缀
- 段落间用空行分隔
- 对话使用中文引号「」"""

        user_prompt = f"""请写《黑日藏锋》第{ch_num}章：{ch_title}。

剧情概要：
{ch_summary}

必须包含的情节点：
{points_text}

目标字数3000字左右。包含对话、动作描写、心理活动、环境描写。章末留悬念。"""

        try:
            content = engine.generate(
                user_prompt,
                system_prompt=system_prompt,
                temperature=0.9,
                max_tokens=6000,
            )
            t1 = time.time()

            if not content or len(content) < 300:
                print(f"❌ 字数不足", flush=True)
                continue

            content = re.sub(r'```.*?\n|```', '', content).strip()

            outfile = os.path.join(OUTPUT_DIR, f"黑日藏锋_第{ch_num}章.txt")
            with open(outfile, "w", encoding="utf-8") as f:
                f.write(f"第{ch_num}章 {ch_title}\n\n{content}")

            if memory and hasattr(memory, 'save_conversation'):
                try:
                    memory.save_conversation("system", f"第{ch_num}章 {ch_title} 生成完成 ({len(content)}字)")
                except Exception:
                    pass

            total_chars += len(content)
            print(f"✅ {len(content)}字 ({t1-t0:.0f}s)", flush=True)

        except Exception as e:
            print(f"❌ {e}", flush=True)

        time.sleep(1)

    print(f"\n{'='*60}")
    print("  合并打包...")
    print(f"{'='*60}")

    files = glob.glob(os.path.join(OUTPUT_DIR, "黑日藏锋_第*.txt"))
    files = [f for f in files if "第1-10章" not in f and "大纲" not in f]
    files.sort(key=lambda f: int(re.search(r"第(\d+)章", f).group(1)))

    merged_path = os.path.join(OUTPUT_DIR, "黑日藏锋_第1-10章.txt")
    merged_chars = 0
    with open(merged_path, "w", encoding="utf-8") as out:
        out.write("《黑日藏锋》\n")
        out.write("=" * 40 + "\n\n")
        for f in files:
            content = open(f, encoding="utf-8").read()
            out.write(content)
            out.write("\n\n" + "─" * 30 + "\n\n")
            merged_chars += len(content)

    print(f"✅ 合并完成: {len(files)}章, {merged_chars}字符")
    print(f"📁 {merged_path}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
