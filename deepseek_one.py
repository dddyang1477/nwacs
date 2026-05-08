"""DeepSeek 单章生成 - 极简稳定版，逐章执行"""
import os, requests, sys, time

API_KEY = os.getenv("DEEPSEEK_API_KEY") or "sk-f3246fbd1eef446e9a11d78efefd9bba"
URL = "https://api.deepseek.com/v1/chat/completions"

DATA = {
    1: ("黑日之下", "林锋穿越醒来后脑勺疼。天上黑色太阳边缘暗红不发热。铁柱（猎户儿子土系下品灵根骨架大）塞半块杂粮饼子硬得刮嗓子。王虎（凝气三层三角眼疤脸）竹鞭催人下矿。草鞋断绳大脚趾露外面。脚踝锁魂环刻矿奴。杂役院灰布衣全是瘦骨嶙峋的人。"),
    2: ("矿道", "矿道入口半山腰石头凿的口子两米宽三米高。光明石冷光照脸发青。老赵监工铁棍敲洞壁警告岔道多别乱走走丢没人找。丙区岔道废灵石矿脉暗红纹路。铁柱教顺着纹砸省力。手掌磨水泡破了流水。矿道阴冷石粉呛人硫磺味混汗臭。"),
    3: ("废灵石", "矿难塌方轰隆一声气浪冲来碎石堵岔道口。铁柱额头飞石划伤血流进眼睛。外面人喊明天再挖。林锋往矿道深处走发现岩壁温度异常——别的冰凉这块温热。砸开岩壁里面天然岩洞很大看不到顶。"),
    4: ("暗红色的光", "岩洞中央嵌人头大暗红石头内部光芒像心跳明灭。林锋伸手触碰烫进骨头不是皮肤烫是骨头烫。热流灌入丹田。意识坠暗红漩涡看到黑日碎裂幻象——黑日像蛋壳裂开碎片四散。醒来掌心多道疤。丹田真气种子转动。"),
    5: ("藏锋诀", "碎日残片灌入功法传承。藏锋诀——真气贴骨走非经脉贴着骨头表面流动外表如凡人谁也看不出来。三天凝气一层。金针术真气凝针刺穴雕刻杀人。铁镐砸岩壁一拳一坑。抹平痕迹。三层：敛息藏脉隐骨。"),
    6: ("小灰", "废井碎石堆捡暗影狼幼崽左后腿断肋骨凹进去快死了。抱回岩洞金针术接骨真气凝针刺骨缝。真气渡命碎日残片分出一丝。喂泡软饼子。起名小灰暗银眼睛一直看他。三天后能站起来舔他手指。"),
    7: ("凝气二层", "突破失败两次。第一次真气逆行吐血嗓子腥甜。第二次丹田差点炸了疼得蜷成虾。悟出引字诀——不灌让碎日残片力量自己渗像水渗沙子。真气液化凝气二层成。一拳岩壁三寸拳印。小灰觉醒暗影潜行融入阴影肉眼看不见。"),
    8: ("杂役院的老鼠", "找瘦猴侯三饼子换信息。散布收信息换食物消息。三天十人七天三十人。建三类信息系统：人物谁是谁、事件发生什么、资源哪里有东西。锁定三月后外门考核——杂役进外门唯一机会。"),
    9: ("第一次交易", "厨房老李透露赵师兄找赤阳石。林锋让瘦猴放消息矿道深处有赤阳石矿脉。赵师兄花两块灵石买消息。分瘦猴老李各半块。三方获利源头无人知晓。情报交易模板建立：信息变灵石变分成。"),
    10: ("周老", "杂役院角落石洞住周老没人知待多久。手不像干杂活——指节分明虎口有茧握剑的茧。眼睛偶尔锐如刀。让林锋搬酒坛——坛刻三级聚灵阵。说藏得不错。又说别碰太多。林锋决定搞清楚他是谁。"),
}

STYLE = """写作铁律：
1. 每句不超20字。句号多逗号少。
2. 禁用：然而因此显然总而言之他意识到心中涌起感到一阵
3. 用感官替情绪。不写害怕写手指抠进石缝指甲缝全是泥
4. 对话短带脏话。直接换行不用XX说
5. 段落长短穿插。长段不超4行。短段可1字
6. 结尾用动作细节收。不总结不升华
7. 保留瑕疵偶尔不通顺偶尔重复"""

def gen(chapter_num):
    title, outline = DATA[chapter_num]
    prompt = f"你是网文写手。写《黑日藏锋》第{chapter_num}章：{title}\n\n剧情：{outline}\n\n{STYLE}\n\n写2000-3000字。直接写正文不要标题。"
    
    print(f"[第{chapter_num}章] 开始调用API...", flush=True)
    t0 = time.time()
    
    try:
        r = requests.post(URL,
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"},
            json={"model": "deepseek-chat", "messages": [{"role": "user", "content": prompt}], "max_tokens": 2500, "temperature": 0.95},
            timeout=300)
        t1 = time.time()
        print(f"[第{chapter_num}章] HTTP {r.status_code} (耗时{t1-t0:.1f}s)", flush=True)
        
        if r.status_code == 200:
            content = r.json()["choices"][0]["message"]["content"]
            print(f"[第{chapter_num}章] 生成 {len(content)} 字符", flush=True)
            
            outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "黑日藏锋")
            os.makedirs(outdir, exist_ok=True)
            outfile = os.path.join(outdir, f"黑日藏锋_第{chapter_num}章.txt")
            with open(outfile, "w", encoding="utf-8") as f:
                f.write(f"第{chapter_num}章 {title}\n\n{content}")
            print(f"[第{chapter_num}章] 已保存: {outfile}", flush=True)
            return True
        else:
            print(f"[第{chapter_num}章] 错误: {r.text[:300]}", flush=True)
            return False
    except Exception as e:
        print(f"[第{chapter_num}章] 异常: {type(e).__name__}: {e}", flush=True)
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python deepseek_one.py <章节号 1-10>")
        sys.exit(1)
    ok = gen(int(sys.argv[1]))
    sys.exit(0 if ok else 1)
