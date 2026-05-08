#!/usr/bin/env python3
"""DeepSeek API 续写章节 - 第4-10章，带重试"""
import os
import requests
import json
import time

API_KEY = os.getenv("DEEPSEEK_API_KEY")
if not API_KEY:
    API_KEY = "sk-f3246fbd1eef446e9a11d78efefd9bba"

URL = "https://api.deepseek.com/v1/chat/completions"

SYSTEM_PROMPT = """你是一个有十年经验的网络小说写手。你的文字有强烈的个人风格。

【核心写作规则 - 必须严格遵守】

1. 句子控制：每句话不超过20个字。多用句号。少用逗号连接长句。像人在说话。有停顿。有呼吸。

2. 禁用词汇（绝对不能出现）：
- 然而、因此、显然、总而言之、由此可见、毋庸置疑、不可否认
- 不仅……而且……、既……又……、一方面……另一方面……
- 他意识到、他明白、他知道
- 心中涌起、内心充满、感到一阵

3. 感官描写（每段至少一个）：
- 不要写"他很害怕" → 写"手指抠进石缝。指甲缝里全是泥。"
- 不要写"矿道很冷" → 写"石头缝里往外渗寒气。水滴在脖子上。冰得人一激灵。"

4. 对话规则：
- 每句对话不超过15个字
- 带脏话、带语气词
- 对话和叙述之间直接换行，不用"XX说："连接

5. 段落节奏：
- 长短穿插。长段不超过4行。短段可以只有1个字。
- 每300字必须有一个短段打破节奏

6. 结尾规则：
- 绝对不要总结、升华、点题
- 用动作收尾。用细节收尾。用沉默收尾。

7. 瑕疵保留：
- 偶尔有不通顺的句子
- 偶尔有重复的词
- 不要每段都完美工整"""

chapters = [
    (4, "暗红色的光", """接上一章：林锋掉进岩洞深处，发现碎日残片。

岩洞中央嵌着人头大的暗红石头。内部光芒像心跳一样明灭。林锋伸手触碰——烫。不是皮肤烫。是骨头烫。热流顺着手指灌进丹田。意识坠入暗红漩涡。看到黑日碎裂的幻象——巨大的黑日像蛋壳一样裂开，碎片四散。醒来掌心多了一道疤。丹田里有什么东西在转。"""),
    
    (5, "藏锋诀", """碎日残片灌入功法传承。真气贴骨走——不是走经脉，是贴着骨头表面流动。外表如凡人，谁也看不出来。三天凝气一层。金针术——真气凝成细针，可刺穴、可雕刻、可杀人。铁镐砸岩壁，一拳一个坑。抹平痕迹。藏锋诀第一层：敛息。第二层：藏脉。第三层：隐骨。"""),
    
    (6, "小灰", """废井碎石堆里捡到暗影狼幼崽。左后腿断了，肋骨凹进去，快死了。抱回岩洞。金针术接骨——真气凝针，刺入骨缝。真气渡命——碎日残片的力量分出一丝。喂泡软的饼子。起名小灰。暗银色眼睛一直看着他。三天后小灰能站起来了。"""),
    
    (7, "凝气二层", """突破失败两次。第一次真气逆行，吐血。第二次丹田差点炸了。悟出"引"字诀——不灌，让碎日残片力量自己渗。像水渗进沙子。真气液化，凝气二层成。一拳在岩壁上打出拳印，三寸深。小灰觉醒暗影潜行——身体融入阴影，肉眼看不见。"""),
    
    (8, "杂役院的老鼠", """找到瘦猴侯三。用饼子换信息。散布"收信息换食物"消息。三天十人，七天三十人。建立三类信息系统：人物（谁是谁）、事件（发生了什么）、资源（哪里有东西）。锁定三个月后外门考核——杂役进外门的唯一机会。"""),
    
    (9, "第一次交易", """厨房老李透露赵师兄找赤阳石。林锋让瘦猴放消息"矿道深处有赤阳石矿脉"。赵师兄花两块灵石买消息。分给瘦猴老李各半块。三方获利。源头无人知晓。情报交易模板建立：信息→灵石→分成。"""),
    
    (10, "周老", """杂役院角落石洞里住着周老。没人知道待了多久。手不像干杂活的——指节分明，虎口有茧，是握剑的茧。眼睛偶尔锐如刀。让林锋搬酒坛——坛上刻三级聚灵阵。说"藏得不错"。又说"别碰太多"。林锋决定搞清楚他是谁。"""),
]

def call_deepseek(chapter_num, chapter_title, chapter_outline, retry=3):
    user_prompt = f"""写《黑日藏锋》第{chapter_num}章：{chapter_title}

剧情要点：{chapter_outline}

要求：
- 2500-3500字
- 用短句。用口语。用脏话。
- 多写动作和感官。少写心理活动。
- 不要总结。不要升华。
- 像人在讲故事。不像AI在写作文。

直接开始写正文。不要写"第X章：XXX"这种标题。"""
    
    for attempt in range(retry):
        try:
            print(f"  正在调用DeepSeek API生成第{chapter_num}章 (尝试 {attempt+1}/{retry})...")
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
            response = requests.post(URL, headers=headers, json=data, timeout=180)
            
            if response.status_code == 429:
                print(f"  速率限制，等待30秒...")
                time.sleep(30)
                continue
                
            response.raise_for_status()
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            print(f"  ✅ 第{chapter_num}章生成完成 ({len(content)}字)")
            return content
            
        except requests.exceptions.Timeout:
            print(f"  超时，重试...")
            time.sleep(5)
        except Exception as e:
            print(f"  错误: {e}")
            if attempt < retry - 1:
                time.sleep(10)
    
    print(f"  ❌ 第{chapter_num}章生成失败（已重试{retry}次）")
    return None

def main():
    output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "黑日藏锋", "黑日藏锋_第1-10章.txt")
    
    # 先补完第3章（文件在第3章中途断了）
    # 检查第3章是否完整
    with open(output_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    if "第4章" not in content:
        # 第3章不完整，需要补完
        print("检测到第3章不完整，正在补完...")
        ch3_outline = """接上一章：林锋掉进岩洞深处，发现碎日残片。岩洞中央嵌着人头大的暗红石头。内部光芒像心跳一样明灭。林锋伸手触碰——烫。不是皮肤烫。是骨头烫。热流顺着手指灌进丹田。意识坠入暗红漩涡。看到黑日碎裂的幻象——巨大的黑日像蛋壳一样裂开，碎片四散。醒来掌心多了一道疤。丹田里有什么东西在转。"""
        ch3_content = call_deepseek(3, "废灵石", ch3_outline)
        if ch3_content:
            # 替换掉不完整的第3章内容
            ch3_start = content.find("第3章 废灵石")
            if ch3_start >= 0:
                content = content[:ch3_start]
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(content)
                    f.write(f"\n\n第3章 废灵石\n\n")
                    f.write(ch3_content)
                    f.write("\n\n")
                print("✅ 第3章已补完")
        time.sleep(3)
    
    # 生成第4-10章
    for ch_num, ch_title, ch_outline in chapters:
        chapter_content = call_deepseek(ch_num, ch_title, ch_outline)
        if chapter_content:
            with open(output_file, "a", encoding="utf-8") as f:
                f.write(f"\n\n第{ch_num}章 {ch_title}\n\n")
                f.write(chapter_content)
                f.write("\n\n")
            print(f"  💾 第{ch_num}章已保存")
        else:
            print(f"  ⚠️ 第{ch_num}章跳过")
        time.sleep(3)
    
    # 写入结尾
    with open(output_file, "a", encoding="utf-8") as f:
        f.write("\n" + "━" * 80 + "\n")
        f.write("（第二小结 完）\n")
        f.write("━" * 80 + "\n")
    
    print(f"\n🎉 全部完成！文件: {output_file}")

if __name__ == "__main__":
    main()
