#!/usr/bin/env python3
"""DeepSeek API 小说章节生成器 - 低AI痕迹版"""
import os
import sys
import requests
import json
import time

API_KEY = os.getenv("DEEPSEEK_API_KEY")
if not API_KEY:
    API_KEY = "sk-f3246fbd1eef446e9a11d78efefd9bba"

URL = "https://api.deepseek.com/v1/chat/completions"

OUTLINE = """
《黑日藏锋》小说设定：
- 主角林锋，穿越到黑日世界，青云宗杂役弟子，废灵根
- 黑日世界：天上挂着黑色太阳，边缘暗红，世界永远暗红色调
- 在矿道矿难中发现碎日残片（黑日碎片），获得藏锋诀功法
- 藏锋诀核心：隐藏修为、隐藏气息，真气贴骨走，外表如凡人
- 捡到暗影狼幼崽"小灰"，会暗影潜行（隐身）
- 收编瘦猴（侯三）建立情报网，铁柱走体修路线
- 杂役头目王虎（凝气三层）欺压杂役，与外门弟子刘元勾结
- 神秘老杂役周老，疑似隐藏高手，识破林锋伪装
- 修炼体系：凝气→筑基→金丹→元婴→化神
- 风格：苟道流（隐忍藏锋）+ 黑暗流（矿道生存）+ 智斗流（情报博弈）

章节大纲：
第1章 黑日之下：林锋穿越醒来，黑日世界初体验，杂役身份，铁柱出场，王虎压迫
第2章 矿道：第一次下矿，废灵石矿脉，矿道阴冷环境，老赵监工
第3章 废灵石：矿难塌方被困，发现岩壁后空洞，碎日残片的召唤
第4章 暗红色的光：接触碎日残片，黑日碎裂的记忆幻象，丹田种下真气种子
第5章 藏锋诀：获得功法传承，三天凝气一层，学会隐藏修为，金针术
第6章 小灰：捡到濒死暗影狼幼崽，用真气救活，小灰认主
第7章 凝气二层：突破失败两次，悟出"引"字诀，成功突破，小灰觉醒暗影潜行
第8章 杂役院的老鼠：收编瘦猴，用饼子换信息，建立30人情报网，锁定外门考核目标
第9章 第一次交易：赤阳石情报变现，三方获利，零暴露，情报交易模板建立
第10章 周老：神秘老杂役，酒坛刻三级聚灵阵，识破伪装，"别碰太多"警告
"""

SYSTEM_PROMPT = """你是一个有十年经验的网络小说写手。你的文字有强烈的个人风格。

【核心写作规则 - 必须严格遵守】

1. 句子控制：每句话不超过20个字。多用句号。少用逗号连接长句。像人在说话。有停顿。有呼吸。

2. 禁用词汇（绝对不能出现）：
- 然而、因此、显然、总而言之、由此可见、毋庸置疑、不可否认
- 不仅……而且……、既……又……、一方面……另一方面……
- 他意识到、他明白、他知道（太AI了，删掉）
- 心中涌起、内心充满、感到一阵（空洞的情绪描写，删掉）

3. 感官描写（每段至少一个）：
- 不要写"他很害怕" → 写"手指抠进石缝。指甲缝里全是泥。"
- 不要写"矿道很冷" → 写"石头缝里往外渗寒气。水滴在脖子上。冰得人一激灵。"
- 不要写"饼子很难吃" → 写"咬了一口。硬。像啃砖头。咽下去刮嗓子。"

4. 对话规则：
- 每句对话不超过15个字
- 带脏话、带语气词、带口癖
- 不要写"他愤怒地说" → 写"他骂了一声。"
- 对话和叙述之间不要用"XX说："来连接，直接换行

5. 段落节奏：
- 长短穿插。长段不超过4行。短段可以只有1个字。
- 像呼吸。紧。松。紧。松。
- 每300字必须有一个短段（1-2句）打破节奏

6. 结尾规则：
- 绝对不要总结、升华、点题
- 用动作收尾。用细节收尾。用沉默收尾。
- 不要写"他知道，新的挑战即将开始"这种AI屁话

7. 思维呈现：
- 主角的思考不要写成"他想：……"
- 写成短句碎片。像真的在想事情。跳跃的。不完整的。
- 偶尔加入自我怀疑。"不对。""也许。""算了。"

8. 瑕疵保留：
- 偶尔有不通顺的句子
- 偶尔有重复的词
- 不要每段都完美工整

记住：你的目标不是写一篇"好文章"。你的目标是写一段"人写的东西"。人写的东西有毛边。有呼吸。有不完美。"""

def call_deepseek(chapter_num, chapter_title, chapter_outline):
    """调用DeepSeek API生成单章"""
    user_prompt = f"""写《黑日藏锋》第{chapter_num}章：{chapter_title}

剧情要点：{chapter_outline}

要求：
- 2500-3500字
- 用短句。用口语。用脏话。
- 多写动作和感官。少写心理活动。
- 不要总结。不要升华。
- 像人在讲故事。不像AI在写作文。

直接开始写正文。不要写"第X章：XXX"这种标题。"""
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        "max_tokens": 4096,
        "temperature": 0.95,
        "top_p": 0.92,
        "frequency_penalty": 0.3,
        "presence_penalty": 0.3
    }
    
    try:
        print(f"  正在调用DeepSeek API生成第{chapter_num}章...")
        response = requests.post(URL, headers=headers, json=data, timeout=180)
        response.raise_for_status()
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        print(f"  第{chapter_num}章生成完成 ({len(content)}字)")
        return content
    except requests.exceptions.RequestException as e:
        print(f"  第{chapter_num}章生成失败: {e}")
        return None

def main():
    chapters = [
        (1, "黑日之下", "林锋穿越醒来，后脑勺疼，天上黑色太阳。铁柱出场叫他去矿道。王虎拿竹鞭催人。杂粮饼子硬得刮嗓子。"),
        (2, "矿道", "矿道入口在半山腰，光明石冷光。老赵监工警告别乱走。丙区岔道，废灵石矿脉暗红纹路。铁柱教他顺着纹砸。手掌磨出水泡。"),
        (3, "废灵石", "矿难塌方，气浪冲来，岔道口被碎石堵住。铁柱额头被飞石划伤。外面人说'明天再挖'。林锋往矿道深处走，发现岩壁温度异常。砸开岩壁，里面是天然岩洞。"),
        (4, "暗红色的光", "岩洞中央嵌着人头大的暗红石头，内部光芒像心跳。林锋伸手触碰，烫进骨头，热流灌入丹田。意识坠入暗红漩涡，看到黑日碎裂的幻象。醒来掌心多了一道疤。"),
        (5, "藏锋诀", "丹田里真气种子旋转。碎日残片灌入功法——真气贴骨走，外表如凡人。三天凝气一层。金针术可刺穴雕刻。铁镐砸岩壁一拳一个坑。抹平痕迹。"),
        (6, "小灰", "废井碎石堆里捡到暗影狼幼崽，左后腿断了，快死了。抱回岩洞，金针术接骨，真气渡命。喂泡软的饼子。起名小灰。暗银色眼睛一直看着他。"),
        (7, "凝气二层", "突破失败两次，吐血。悟出'引'字诀——不灌，让碎日残片力量自己渗。真气液化，凝气二层成。一拳在岩壁上打出拳印。小灰觉醒暗影潜行。"),
        (8, "杂役院的老鼠", "找到瘦猴侯三，用饼子换信息。散布'收信息换食物'消息。三天十人，七天三十人。建立人物/事件/资源三类信息系统。锁定三个月后外门考核。"),
        (9, "第一次交易", "厨房老李透露赵师兄找赤阳石。林锋让瘦猴放消息'矿道深处有赤阳石矿脉'。赵师兄花两块灵石买消息。分给瘦猴老李各半块。三方获利，源头无人知晓。"),
        (10, "周老", "杂役院角落石洞里住着周老，没人知道待了多久。手不像干杂活的，眼睛偶尔锐如刀。让林锋搬酒坛——坛上刻三级聚灵阵。说'藏得不错''别碰太多'。林锋决定搞清楚他是谁。"),
    ]
    
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "黑日藏锋")
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, "黑日藏锋_第1-10章.txt")
    
    header = """╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                    《黑日藏锋》第1-10章                                       ║
║                    第一、二小结：黑日之下 / 矿道深处                            ║
║                    由 DeepSeek API 直接生成                                    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

"""
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(header)
        f.write("━" * 80 + "\n")
        f.write("第一小结：黑日之下（第1-5章）\n")
        f.write("━" * 80 + "\n\n")
    
    for ch_num, ch_title, ch_outline in chapters[:5]:
        content = call_deepseek(ch_num, ch_title, ch_outline)
        if content:
            with open(output_file, "a", encoding="utf-8") as f:
                f.write(f"\n\n第{ch_num}章 {ch_title}\n\n")
                f.write(content)
                f.write("\n\n")
        time.sleep(2)
    
    with open(output_file, "a", encoding="utf-8") as f:
        f.write("\n" + "━" * 80 + "\n")
        f.write("（第一小结 完）\n")
        f.write("━" * 80 + "\n\n")
        f.write("━" * 80 + "\n")
        f.write("第二小结：矿道深处（第6-10章）\n")
        f.write("━" * 80 + "\n\n")
    
    for ch_num, ch_title, ch_outline in chapters[5:]:
        content = call_deepseek(ch_num, ch_title, ch_outline)
        if content:
            with open(output_file, "a", encoding="utf-8") as f:
                f.write(f"\n\n第{ch_num}章 {ch_title}\n\n")
                f.write(content)
                f.write("\n\n")
        time.sleep(2)
    
    with open(output_file, "a", encoding="utf-8") as f:
        f.write("\n" + "━" * 80 + "\n")
        f.write("（第二小结 完）\n")
        f.write("下一小结预告（第11-15章）：\n")
        f.write("凝气三层、王虎的怀疑、第一次用毒、借刀杀人、矿道中的秘密基地升级……\n")
        f.write("━" * 80 + "\n")
    
    print(f"\n✅ 全部完成！文件保存在: {output_file}")

if __name__ == "__main__":
    main()
