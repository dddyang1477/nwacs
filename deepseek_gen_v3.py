"""DeepSeek API 逐章生成 - 精简稳定版"""
import os, requests, json, time

API_KEY = os.getenv("DEEPSEEK_API_KEY") or "sk-f3246fbd1eef446e9a11d78efefd9bba"
URL = "https://api.deepseek.com/v1/chat/completions"
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "黑日藏锋")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "黑日藏锋_第1-10章.txt")
os.makedirs(OUTPUT_DIR, exist_ok=True)

STYLE_RULES = """
写作规则：
- 每句不超过20字，多用句号
- 禁用：然而、因此、显然、总而言之、他意识到、心中涌起
- 用感官代替情绪：不写"害怕"写"手指抠进石缝"
- 对话短，带脏话，直接换行不用"XX说"
- 段落长短穿插，每300字有短段破节奏
- 结尾用动作/细节收尾，不总结不升华
- 保留瑕疵，偶尔不通顺
"""

CHAPTERS = [
    (1, "黑日之下", "林锋穿越醒来，后脑勺疼。天上黑色太阳边缘暗红。铁柱（猎户儿子土系下品灵根）塞饼子。王虎（凝气三层三角眼疤脸）竹鞭催人。杂粮饼硬得刮嗓子。草鞋断绳。脚踝锁魂环。"),
    (2, "矿道", "矿道入口半山腰。光明石冷光。老赵监工警告别乱走。丙区岔道废灵石矿脉暗红纹路。铁柱教顺着纹砸。手掌磨水泡。矿道阴冷石粉呛人。"),
    (3, "废灵石", "矿难塌方气浪冲来。岔道口碎石堵住。铁柱额头飞石划伤。外面人说'明天再挖'。林锋往深处走。发现岩壁温度异常——别的冰凉这块温热。砸开岩壁里面天然岩洞。"),
    (4, "暗红色的光", "岩洞中央人头大暗红石头。内部光芒像心跳明灭。林锋触碰——烫进骨头。热流灌丹田。意识坠暗红漩涡。看到黑日碎裂幻象——黑日像蛋壳裂开碎片四散。醒来掌心多道疤。丹田真气种子转动。"),
    (5, "藏锋诀", "碎日残片灌入功法。藏锋诀——真气贴骨走非经脉。外表如凡人。三天凝气一层。金针术——真气凝针刺穴雕刻。铁镐砸岩壁一拳一坑。抹平痕迹。三层：敛息藏脉隐骨。"),
    (6, "小灰", "废井碎石堆捡暗影狼幼崽。左后腿断肋骨凹快死了。抱回岩洞。金针术接骨真气凝针刺骨缝。真气渡命碎日残片分出一丝。喂泡软饼子。起名小灰。暗银眼睛一直看他。三天后能站。"),
    (7, "凝气二层", "突破失败两次。第一次真气逆行吐血。第二次丹田差点炸。悟出引字诀——不灌让碎日残片力量自己渗。像水渗沙。真气液化凝气二层成。一拳岩壁三寸拳印。小灰觉醒暗影潜行融入阴影。"),
    (8, "杂役院的老鼠", "找瘦猴侯三。饼子换信息。散布收信息换食物消息。三天十人七天三十人。建三类信息系统：人物事件资源。锁定三月后外门考核——杂役进外门唯一机会。"),
    (9, "第一次交易", "厨房老李透露赵师兄找赤阳石。林锋让瘦猴放消息矿道深处有赤阳石矿脉。赵师兄花两块灵石买消息。分瘦猴老李各半块。三方获利源头无人知晓。情报交易模板建立。"),
    (10, "周老", "杂役院角落石洞住周老。没人知待多久。手不像干杂活——指节分明虎口有茧握剑的茧。眼睛偶尔锐如刀。让林锋搬酒坛——坛刻三级聚灵阵。说藏得不错。又说别碰太多。林锋决定搞清楚他是谁。"),
]

def gen_chapter(num, title, outline):
    prompt = f"""你是网文写手。写《黑日藏锋》第{num}章：{title}

剧情：{outline}

{STYLE_RULES}

要求2500-3500字。直接写正文。不要标题。"""
    
    for attempt in range(3):
        try:
            print(f"  第{num}章 尝试{attempt+1}...", end=" ", flush=True)
            r = requests.post(URL, headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {API_KEY}"
            }, json={
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 3000,
                "temperature": 0.95,
                "top_p": 0.92,
                "frequency_penalty": 0.3,
                "presence_penalty": 0.3
            }, timeout=120)
            
            if r.status_code == 429:
                print("限速等30s")
                time.sleep(30)
                continue
            
            r.raise_for_status()
            content = r.json()["choices"][0]["message"]["content"]
            print(f"✅ {len(content)}字")
            return content
            
        except Exception as e:
            print(f"❌ {str(e)[:60]}")
            if attempt < 2:
                time.sleep(10)
    return None

def main():
    header = """╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                    《黑日藏锋》第1-10章                                       ║
║                    第一、二小结：黑日之下 / 矿道深处                            ║
║                    由 DeepSeek API (deepseek-v4-flash) 直接生成                ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

"""
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(header)
    
    for batch_name, start, end in [("第一小结：黑日之下", 1, 5), ("第二小结：矿道深处", 6, 10)]:
        with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
            f.write(f"\n{'━'*80}\n{batch_name}（第{start}-{end}章）\n{'━'*80}\n")
        
        for num, title, outline in CHAPTERS[start-1:end]:
            content = gen_chapter(num, title, outline)
            if content:
                with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
                    f.write(f"\n\n第{num}章 {title}\n\n{content}\n")
                print(f"  💾 第{num}章已保存")
            else:
                print(f"  ⚠️ 第{num}章失败")
            time.sleep(2)
        
        with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
            f.write(f"\n{'━'*80}\n（{batch_name} 完）\n{'━'*80}\n")
    
    print(f"\n🎉 完成！{OUTPUT_FILE}")

if __name__ == "__main__":
    main()
