import sys, os, json, traceback, threading, time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

sys.path.insert(0, r'd:\Trae CN\github\nwacs\nwacs\core\v8')
os.chdir(r'd:\Trae CN\github\nwacs\nwacs\core\v8')

LOG_FILE = os.path.join(os.path.dirname(__file__), 'server_debug.log')

def log(msg):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    line = f"[{timestamp}] {msg}"
    print(line)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(line + '\n')

log("Importing NWACS modules...")
from engine.creative_engine import SmartCreativeEngine
from genre_profile_manager import GenreProfileManager, GenreType

log("Initializing...")
engine = SmartCreativeEngine()
genre_manager = GenreProfileManager()

GENRE_KB_FILE = os.path.join(os.path.dirname(__file__), 'genre_knowledge_base.json')
genre_knowledge_base = {}
if os.path.exists(GENRE_KB_FILE):
    try:
        with open(GENRE_KB_FILE, 'r', encoding='utf-8') as f:
            genre_knowledge_base = json.load(f)
        total_schools = sum(len(schools) for schools in genre_knowledge_base.values())
        log(f"Knowledge base loaded: {len(genre_knowledge_base)} genres, {total_schools} schools")
    except Exception as e:
        log(f"Knowledge base load failed: {e}")
else:
    log("No knowledge base file found, will use built-in defaults")

log("Ready.")

def build_knowledge_injection(genre: str, school_id: str = "") -> str:
    """从知识库构建可注入prompt的专业知识文本"""
    if not genre_knowledge_base or genre not in genre_knowledge_base:
        return ""

    kb = genre_knowledge_base[genre]
    school_data = kb.get(school_id) if school_id else None

    parts = []

    if school_data and "error" not in school_data:
        parts.append(f"\n## {school_data.get('school_name', '')}流派专业知识\n")

        techniques = school_data.get("writing_techniques", [])
        if techniques:
            parts.append("### 核心写作手法")
            for t in techniques[:5]:
                parts.append(f"- **{t.get('technique', '')}**: {t.get('description', '')}")
                if t.get("example_usage"):
                    parts.append(f"  应用: {t['example_usage']}")
            parts.append("")

        templates = school_data.get("plot_templates", [])
        if templates:
            parts.append("### 经典剧情模板")
            for t in templates[:3]:
                parts.append(f"- **{t.get('template_name', '')}**: {t.get('structure', '')}")
                nodes = t.get("key_nodes", [])
                if nodes:
                    parts.append(f"  关键节点: {' → '.join(nodes)}")
            parts.append("")

        chars = school_data.get("writing_characteristics", [])
        if chars:
            parts.append("### 写作特点")
            for c in chars[:5]:
                parts.append(f"- {c.get('feature', '')}: {c.get('description', '')}")
            parts.append("")

        fp = school_data.get("style_fingerprint", {})
        if fp:
            parts.append("### 风格指纹")
            parts.append(f"- 句子偏好: {fp.get('sentence_length_preference', '混合')}")
            parts.append(f"- 对话占比: {fp.get('dialogue_ratio', '中')}")
            parts.append(f"- 节奏: {fp.get('pacing', '中')}")
            parts.append(f"- 视角: {fp.get('pov_preference', '第三人称')}")
            parts.append(f"- 情绪曲线: {fp.get('emotional_curve', '起伏')}")
            parts.append("")

        vocab = school_data.get("vocabulary", {})
        if vocab:
            parts.append("### 创作词汇库")
            for key, words in vocab.items():
                if isinstance(words, list) and words:
                    label = key.replace('_', ' ').title()
                    parts.append(f"- {label}: {', '.join(words[:8])}")
            parts.append("")

        masters = school_data.get("master_techniques", [])
        if masters:
            parts.append("### 大师技法参考")
            for m in masters[:3]:
                parts.append(f"- {m.get('master', '')}: {m.get('technique', '')} — {m.get('learnable_point', '')}")
            parts.append("")

    if not school_data:
        for sid, sdata in kb.items():
            if isinstance(sdata, dict) and "error" not in sdata:
                chars = sdata.get("writing_characteristics", [])
                if chars:
                    parts.append(f"\n## {genre}通用写作特点\n")
                    for c in chars[:8]:
                        parts.append(f"- {c.get('feature', '')}: {c.get('description', '')}")
                    parts.append("")
                    break

    return "\n".join(parts)


class NWACSHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        log(f"HTTP: {args[0]}")

    def _send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        path = urlparse(self.path).path
        if path == '/api/health':
            self._send_json({"status": "ok"})
        elif path == '/api/options':
            self._send_json({
                "genres": {
                    "玄幻": {"icon": "🐉", "desc": "东方奇幻世界", "color": "#7c3aed"},
                    "都市": {"icon": "🏙️", "desc": "现代都市背景", "color": "#2563eb"},
                    "仙侠": {"icon": "⚔️", "desc": "修仙问道", "color": "#059669"},
                    "科幻": {"icon": "🚀", "desc": "未来科技", "color": "#0891b2"},
                    "悬疑": {"icon": "🔍", "desc": "推理探案", "color": "#d97706"},
                    "言情": {"icon": "💕", "desc": "情感纠葛", "color": "#db2777"},
                    "历史": {"icon": "📜", "desc": "架空历史", "color": "#b45309"},
                    "游戏": {"icon": "🎮", "desc": "虚拟现实", "color": "#4f46e5"},
                    "恐怖": {"icon": "👻", "desc": "灵异惊悚", "color": "#6b21a8"},
                    "武侠": {"icon": "🥋", "desc": "江湖恩怨", "color": "#b91c1c"},
                },
                "schools": {
                    "玄幻": [
                        {"id": "sign_in", "name": "签到流", "desc": "每日签到获得奖励，躺平变强"},
                        {"id": "system", "name": "系统流", "desc": "绑定系统，完成任务获得能力"},
                        {"id": "wisdom", "name": "智取流", "desc": "以智取胜，运筹帷幄"},
                        {"id": "gou_dao", "name": "苟道流", "desc": "低调发育，苟到无敌"},
                        {"id": "mortal", "name": "凡人流", "desc": "资质平凡，靠毅力逆袭"},
                        {"id": "invincible", "name": "无敌流", "desc": "开局满级，一路碾压"},
                        {"id": "waste_reverse", "name": "废柴逆袭流", "desc": "从废物到巅峰的热血之路"},
                        {"id": "farming", "name": "种田流", "desc": "经营发展，种田修仙"},
                        {"id": "behind_scenes", "name": "幕后黑手流", "desc": "暗中操控一切，做幕后大佬"},
                    ],
                    "都市": [
                        {"id": "urban_romance", "name": "都市情感", "desc": "现代都市中的爱恨情仇"},
                        {"id": "business_war", "name": "商战流", "desc": "商场如战场，资本博弈"},
                        {"id": "rebirth_city", "name": "重生流", "desc": "重生回到过去，改写人生"},
                        {"id": "divine_doctor", "name": "神医流", "desc": "医术通天，妙手回春"},
                        {"id": "treasure", "name": "鉴宝流", "desc": "慧眼识珠，捡漏暴富"},
                        {"id": "entertainment", "name": "娱乐流", "desc": "娱乐圈打拼，成为顶流"},
                        {"id": "war_god_return", "name": "战神归来流", "desc": "退役兵王回归都市"},
                        {"id": "campus", "name": "校园流", "desc": "校园青春，热血成长"},
                        {"id": "workplace", "name": "职场流", "desc": "职场晋升，步步为营"},
                    ],
                    "仙侠": [
                        {"id": "traditional_xiuxian", "name": "传统修仙流", "desc": "炼气筑基，步步登仙"},
                        {"id": "sword_cultivator", "name": "剑修流", "desc": "一剑破万法，剑道独尊"},
                        {"id": "alchemy", "name": "丹修流", "desc": "炼丹成道，以药入仙"},
                        {"id": "formation", "name": "阵法流", "desc": "布阵杀敌，阵法通神"},
                        {"id": "sect", "name": "宗门流", "desc": "宗门经营，壮大势力"},
                        {"id": "rogue_cultivator", "name": "散修流", "desc": "无门无派，独自闯荡"},
                        {"id": "demon_cultivator", "name": "魔修流", "desc": "以魔入道，亦正亦邪"},
                        {"id": "reincarnation_immortal", "name": "转世重修流", "desc": "大能转世，重走仙路"},
                    ],
                    "科幻": [
                        {"id": "hard_scifi", "name": "硬科幻流", "desc": "基于真实科学理论的推演"},
                        {"id": "cyberpunk", "name": "赛博朋克流", "desc": "高科技低生活，反乌托邦"},
                        {"id": "star_war", "name": "星际战争流", "desc": "宇宙大战，文明碰撞"},
                        {"id": "apocalypse", "name": "末世流", "desc": "末日降临，挣扎求生"},
                        {"id": "mecha", "name": "机甲流", "desc": "驾驶机甲，驰骋星海"},
                        {"id": "gene_evolution", "name": "基因进化流", "desc": "基因改造，人类进化"},
                        {"id": "ai_awakening", "name": "AI觉醒流", "desc": "人工智能产生自我意识"},
                        {"id": "time_travel_scifi", "name": "时空穿梭流", "desc": "穿越时空，改变命运"},
                    ],
                    "悬疑": [
                        {"id": "classic_detective", "name": "本格推理流", "desc": "逻辑严密，公平解谜"},
                        {"id": "social_suspense", "name": "社会派流", "desc": "关注社会问题，人性探讨"},
                        {"id": "psychological", "name": "心理悬疑流", "desc": "心理博弈，精神对抗"},
                        {"id": "criminal_investigation", "name": "刑侦流", "desc": "警察破案，追查真凶"},
                        {"id": "tomb_raider", "name": "盗墓流", "desc": "古墓探险，解密寻宝"},
                        {"id": "spy", "name": "谍战流", "desc": "间谍暗战，情报交锋"},
                        {"id": "reversal", "name": "反转流", "desc": "层层反转，不到最后不知真相"},
                    ],
                    "言情": [
                        {"id": "ceo_romance", "name": "霸道总裁流", "desc": "强势总裁爱上我"},
                        {"id": "sweet_pet", "name": "甜宠流", "desc": "全程高甜，宠溺无边"},
                        {"id": "tortured_love", "name": "虐恋流", "desc": "虐心虐身，痛彻心扉"},
                        {"id": "marry_first", "name": "先婚后爱流", "desc": "先结婚后恋爱，日久生情"},
                        {"id": "female_dominance", "name": "女尊流", "desc": "女性主导，女强男弱"},
                        {"id": "palace_struggle", "name": "宫斗流", "desc": "后宫争斗，步步惊心"},
                        {"id": "family_struggle", "name": "宅斗流", "desc": "家族内斗，嫡庶之争"},
                        {"id": "business_woman", "name": "商业女霸总", "desc": "女强人叱咤商界"},
                        {"id": "youth_campus_love", "name": "青春校园流", "desc": "校园纯爱，青春悸动"},
                    ],
                    "历史": [
                        {"id": "time_travel_history", "name": "穿越流", "desc": "现代人穿越古代，用知识改变世界"},
                        {"id": "farming_history", "name": "种田流", "desc": "古代种田发家致富"},
                        {"id": "conquest", "name": "争霸流", "desc": "逐鹿天下，一统江山"},
                        {"id": "scheming", "name": "权谋流", "desc": "朝堂权谋，智斗天下"},
                        {"id": "imperial_exam", "name": "科举流", "desc": "科举入仕，步步高升"},
                        {"id": "business_history", "name": "经商流", "desc": "古代经商，富甲天下"},
                        {"id": "alternate_history", "name": "架空历史流", "desc": "虚构朝代，自由发挥"},
                        {"id": "tech_uplift", "name": "科技攀升流", "desc": "用现代科技改造古代"},
                    ],
                    "游戏": [
                        {"id": "full_dive_vr", "name": "全息游戏流", "desc": "沉浸式虚拟现实游戏"},
                        {"id": "esports", "name": "电竞流", "desc": "电子竞技，巅峰对决"},
                        {"id": "game_system", "name": "系统流", "desc": "现实世界获得游戏系统"},
                        {"id": "fourth_disaster", "name": "第四天灾流", "desc": "玩家降临异界，掀起波澜"},
                        {"id": "npc_awakening", "name": "NPC觉醒流", "desc": "游戏NPC产生自我意识"},
                        {"id": "game_rebirth", "name": "游戏重生流", "desc": "重生回游戏开服前"},
                        {"id": "game_world_travel", "name": "游戏异界流", "desc": "穿越到游戏世界"},
                    ],
                    "恐怖": [
                        {"id": "supernatural", "name": "灵异流", "desc": "鬼怪灵异，阴阳两界"},
                        {"id": "folk_horror", "name": "民俗恐怖流", "desc": "民间传说，禁忌仪式"},
                        {"id": "infinite_loop", "name": "无限流", "desc": "无限循环的恐怖副本"},
                        {"id": "rule_horror", "name": "规则怪谈流", "desc": "遵守规则才能存活"},
                        {"id": "cthulhu", "name": "克苏鲁流", "desc": "不可名状的宇宙恐怖"},
                        {"id": "urban_legend", "name": "都市传说流", "desc": "都市中的诡异传说"},
                        {"id": "survival_horror", "name": "生存恐怖流", "desc": "绝境求生，恐怖降临"},
                    ],
                    "武侠": [
                        {"id": "traditional_wuxia", "name": "传统武侠流", "desc": "侠之大者，为国为民"},
                        {"id": "high_martial", "name": "高武流", "desc": "武力值爆表，破碎虚空"},
                        {"id": "national_art", "name": "国术流", "desc": "国术传承，明劲暗劲"},
                        {"id": "government_martial", "name": "朝廷鹰犬流", "desc": "为朝廷效力，六扇门风云"},
                        {"id": "demon_cult", "name": "魔教流", "desc": "魔教中人，亦正亦邪"},
                        {"id": "assassin", "name": "刺客流", "desc": "暗杀组织，一击必杀"},
                        {"id": "sword_hero", "name": "剑客流", "desc": "仗剑天涯，快意恩仇"},
                    ],
                },
                "styles": {
                    "热血爽文": {"icon": "🔥", "desc": "节奏明快"},
                    "轻松搞笑": {"icon": "😄", "desc": "幽默诙谐"},
                    "黑暗深沉": {"icon": "🌑", "desc": "人性探讨"},
                    "温馨治愈": {"icon": "🌸", "desc": "温暖人心"},
                    "悬疑烧脑": {"icon": "🧩", "desc": "伏笔重重"},
                    "史诗宏大": {"icon": "🏰", "desc": "世界观庞大"},
                },
                "tones": {
                    "紧张刺激": "节奏紧凑",
                    "轻松愉快": "氛围轻松",
                    "虐心催泪": "情感浓烈",
                    "冷静克制": "叙事冷静",
                    "热血燃爆": "情绪高涨",
                },
                "lengths": {
                    "短篇": "3-5万字",
                    "中篇": "10-30万字",
                    "中长篇": "50-100万字",
                    "长篇": "100-300万字",
                    "超长篇": "300万字+",
                }
            })
        elif path == '/' or path == '/index.html':
            frontend_path = os.path.join(os.path.dirname(__file__), 'frontend', 'index.html')
            if os.path.exists(frontend_path):
                with open(frontend_path, 'r', encoding='utf-8') as f:
                    html = f.read()
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(html.encode('utf-8'))
            else:
                self._send_json({"error": "Frontend not found"}, 404)
        else:
            self._send_json({"error": "Not found"}, 404)

    def do_POST(self):
        path = urlparse(self.path).path
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self._send_json({"error": "Invalid JSON"}, 400)
            return

        if path == '/api/generate_plots':
            self._handle_generate_plots(data)
        elif path == '/api/select_plot':
            self._handle_select_plot(data)
        elif path == '/api/generate_chapter':
            self._handle_generate_chapter(data)
        elif path == '/api/detect_ai':
            self._handle_detect_ai(data)
        elif path == '/api/rewrite':
            self._handle_rewrite(data)
        else:
            self._send_json({"error": "Not found"}, 404)

    def _handle_generate_plots(self, data):
        genres = data.get('genres', [data.get('genre', '玄幻')])
        if isinstance(genres, str):
            genres = [genres]
        styles = data.get('styles', [data.get('style', '热血爽文')])
        if isinstance(styles, str):
            styles = [styles]
        tones = data.get('tones', [data.get('tone', '紧张刺激')])
        if isinstance(tones, str):
            tones = [tones]
        length = data.get('length', '中长篇')
        theme = data.get('theme', '逆境成长')
        protagonist = data.get('protagonist', '')
        extra = data.get('extra_requirements', '')
        schools = data.get('schools', [data.get('school', '')])
        if isinstance(schools, str):
            schools = [schools] if schools else []
        school_names = data.get('school_names', [data.get('school_name', '')])
        if isinstance(school_names, str):
            school_names = [school_names] if school_names else []

        primary_genre = genres[0] if genres else '玄幻'
        primary_school = schools[0] if schools else ''
        primary_school_name = school_names[0] if school_names else ''

        genre_str = '、'.join(genres) if len(genres) > 1 else genres[0]
        style_str = '、'.join(styles)
        tone_str = '、'.join(tones)
        school_str_list = '、'.join(school_names) if school_names else ''

        log(f"Generating plots: genres={genre_str}, styles={style_str}, schools={school_str_list}, theme={theme}")

        try:
            genre_map = {gt.label: gt for gt in GenreType}
            genre_enum = genre_map.get(primary_genre)
            genre_context = ""
            if genre_enum:
                genre_manager.set_genre(genre_enum)
                genre_context = genre_manager.get_full_generation_context(include_pleasure=True)

            extra_str = f"\nExtra: {extra}" if extra else ""
            protag_str = f"\nProtagonist: {protagonist}" if protagonist else ""

            genre_label = f"{genre_str}（融合）" if len(genres) > 1 else genres[0]
            school_label = f"\nWriting Schools: {school_str_list}" if school_str_list else ""
            multi_genre_note = ""
            if len(genres) > 1:
                multi_genre_note = f"\nThis is a cross-genre novel blending: {genre_str}. Blend elements from all these genres naturally."

            knowledge_injection = build_knowledge_injection(primary_genre, primary_school)
            if len(genres) > 1:
                for g in genres[1:]:
                    extra_kb = build_knowledge_injection(g, '')
                    if extra_kb:
                        knowledge_injection += "\n" + extra_kb

            prompt = f"""You are a senior novel editor. Generate 3 completely different plot ideas.

Requirements:
- Genre: {genre_label}
- Style: {style_str}
- Tone: {tone_str}
- Length: {length}
- Theme: {theme}{school_label}{multi_genre_note}{protag_str}{extra_str}

{genre_context}

{knowledge_injection}

For each plot, provide: name, tagline (one sentence), core_idea, protagonist, main_conflict, expected_beats, target_readers, innovation.

Return ONLY valid JSON in this exact format:
{{"plots": [{{"id": "plot_1", "name": "...", "tagline": "...", "core_idea": "...", "protagonist": "...", "main_conflict": "...", "expected_beats": "...", "target_readers": "...", "innovation": "..."}}]}}"""

            log("Calling DeepSeek...")
            result_text = engine.models["deepseek"].generate(prompt, temperature=0.9, max_tokens=3000)
            log(f"Response: {len(result_text)} chars")

            json_match = result_text
            if "```json" in result_text:
                json_match = result_text.split("```json")[1].split("```")[0]
            elif "```" in result_text:
                json_match = result_text.split("```")[1].split("```")[0]

            json_str = json_match.strip()
            try:
                result_data = json.loads(json_str)
            except json.JSONDecodeError as je:
                log(f"JSON parse error: {je}, attempting recovery...")
                import re
                json_str = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', json_str)
                json_str = json_str.replace('\t', ' ').replace('\r', '')
                last_brace = json_str.rfind('}')
                last_bracket = json_str.rfind(']')
                cut_point = max(last_brace, last_bracket)
                if cut_point > 0:
                    json_str = json_str[:cut_point + 1]
                    bracket_count = json_str.count('{') - json_str.count('}')
                    json_str += '}' * bracket_count
                try:
                    result_data = json.loads(json_str)
                except json.JSONDecodeError:
                    log("Recovery failed, trying regex extraction...")
                    plots = []
                    plot_blocks = re.findall(r'\{\s*"name"\s*:\s*"([^"]*)"\s*,\s*"tagline"\s*:\s*"([^"]*)"', json_str)
                    for i, (name, tagline) in enumerate(plot_blocks[:3]):
                        plots.append({
                            "id": f"plot_{i+1}", "name": name, "tagline": tagline,
                            "core_idea": tagline, "protagonist": "", "main_conflict": "",
                            "expected_beats": "", "target_readers": "", "innovation": "",
                            "color": ["#7c3aed", "#2563eb", "#059669"][i]
                        })
                    if plots:
                        result_data = {"plots": plots}
                    else:
                        raise

            plots = result_data.get("plots", [])
            colors = ["#7c3aed", "#2563eb", "#059669", "#d97706", "#db2777"]
            for i, plot in enumerate(plots):
                plot["id"] = f"plot_{i+1}"
                plot["color"] = colors[i % 5]

            self._send_json({"success": True, "plots": plots})

        except Exception as e:
            log(f"Error: {e}")
            traceback.print_exc()
            self._send_json({
                "success": True,
                "plots": [
                    {"id": "plot_1", "name": "逆天改命", "tagline": "平凡少年获得神秘传承，一路逆袭", "core_idea": "废柴主角意外获得上古传承，从此踏上逆天之路", "protagonist": "出身平凡的坚毅少年", "main_conflict": "与天命抗争，打破阶级固化", "expected_beats": "打脸升级，逆天改命", "target_readers": "喜欢热血升级的读者", "innovation": "传统升级流加入现代元素", "color": "#7c3aed"},
                    {"id": "plot_2", "name": "暗流涌动", "tagline": "都市阴影中的异能者战争", "core_idea": "现代都市隐藏着异能者世界，主角意外觉醒", "protagonist": "意外觉醒异能的普通上班族", "main_conflict": "异能者组织间的明争暗斗", "expected_beats": "能力觉醒，组织对抗", "target_readers": "喜欢都市异能的读者", "innovation": "都市+异能+悬疑三合一", "color": "#2563eb"},
                    {"id": "plot_3", "name": "星辰大海", "tagline": "星际流浪者的传奇冒险", "core_idea": "在星际文明中寻找失落的地球文明", "protagonist": "星际探险家", "main_conflict": "不同星际文明间的冲突", "expected_beats": "探索未知，文明碰撞", "target_readers": "喜欢科幻冒险的读者", "innovation": "东方哲学+西方科幻", "color": "#059669"},
                ],
                "note": f"Fallback: {str(e)[:100]}"
            })

    def _handle_select_plot(self, data):
        plot_id = data.get('plot_id', '')
        plot_name = data.get('plot_name', '')
        genres = data.get('genres', [data.get('genre', '玄幻')])
        if isinstance(genres, str):
            genres = [genres]
        styles = data.get('styles', [data.get('style', '热血爽文')])
        if isinstance(styles, str):
            styles = [styles]
        tones = data.get('tones', [data.get('tone', '紧张刺激')])
        if isinstance(tones, str):
            tones = [tones]
        length = data.get('length', '中长篇')
        theme = data.get('theme', '逆境成长')
        schools = data.get('schools', [data.get('school', '')])
        if isinstance(schools, str):
            schools = [schools] if schools else []
        school_names = data.get('school_names', [data.get('school_name', '')])
        if isinstance(school_names, str):
            school_names = [school_names] if school_names else []

        primary_genre = genres[0] if genres else '玄幻'
        primary_school = schools[0] if schools else ''

        genre_str = '、'.join(genres) if len(genres) > 1 else genres[0]
        style_str = '、'.join(styles)
        tone_str = '、'.join(tones)
        school_str_list = '、'.join(school_names) if school_names else ''

        log(f"Generating outline for: {plot_name}, schools={school_str_list}")

        try:
            genre_map = {gt.label: gt for gt in GenreType}
            genre_enum = genre_map.get(primary_genre)
            genre_context = ""
            if genre_enum:
                genre_manager.set_genre(genre_enum)
                genre_context = genre_manager.get_full_generation_context(include_pleasure=True)

            genre_label = f"{genre_str}（融合）" if len(genres) > 1 else genres[0]
            school_label = f"\n- Writing Schools: {school_str_list}" if school_str_list else ""
            multi_genre_note = ""
            if len(genres) > 1:
                multi_genre_note = f"\n- Cross-genre blend: {genre_str}. Naturally integrate elements from all these genres."

            knowledge_injection = build_knowledge_injection(primary_genre, primary_school)
            if len(genres) > 1:
                for g in genres[1:]:
                    extra_kb = build_knowledge_injection(g, '')
                    if extra_kb:
                        knowledge_injection += "\n" + extra_kb

            prompt = f"""You are a senior novel outline planner. Create a detailed chapter-by-chapter outline.

Novel Info:
- Genre: {genre_label}
- Style: {style_str}{school_label}{multi_genre_note}
- Tone: {tone_str}
- Length: {length}
- Theme: {theme}
- Selected Plot: {plot_name}

{genre_context}

{knowledge_injection}

Create an outline with:
1. A compelling title
2. A 200-word synopsis
3. Main characters with name suggestions and name meanings (at least 3 characters: protagonist, antagonist, key supporting)
4. Plot lines breakdown: main_line (主线), sub_lines (辅线, at least 2), cause_effect_chains (因果关系链, at least 2)
5. Three-act structure breakdown
6. 10-15 chapter summaries with key events, each chapter must include: plot_line_type (main/sub/transition), cause_effect (what causes this chapter and what it leads to), notes (empty string for user annotations)

Return ONLY valid JSON:
{{"title": "...", "synopsis": "...", "characters": [{{"name": "...", "name_meaning": "...", "role": "protagonist/antagonist/supporting", "description": "..."}}], "plot_lines": {{"main_line": "...", "sub_lines": ["...", "..."], "cause_effect_chains": [{{"cause": "...", "effect": "...", "chapters_involved": [1, 3]}}]}}, "acts": [{{"name": "Act 1", "description": "...", "chapters": [{{"number": 1, "title": "...", "summary": "...", "plot_line_type": "main/sub/transition", "cause_effect": {{"caused_by": "...", "leads_to": "..."}}, "key_events": ["..."], "word_count_target": 3000, "notes": ""}}]}}]}}"""

            log("Calling DeepSeek for outline...")
            result_text = engine.models["deepseek"].generate(prompt, temperature=0.8, max_tokens=6000)
            log(f"Outline response: {len(result_text)} chars")

            json_match = result_text
            if "```json" in result_text:
                json_match = result_text.split("```json")[1].split("```")[0]
            elif "```" in result_text:
                json_match = result_text.split("```")[1].split("```")[0]

            json_str = json_match.strip()
            try:
                outline = json.loads(json_str)
            except json.JSONDecodeError as je:
                log(f"Outline JSON parse error: {je}, attempting recovery...")
                import re
                json_str = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', json_str)
                json_str = json_str.replace('\t', ' ').replace('\r', '')
                last_brace = json_str.rfind('}')
                last_bracket = json_str.rfind(']')
                cut_point = max(last_brace, last_bracket)
                if cut_point > 0:
                    json_str = json_str[:cut_point + 1]
                    bracket_count = json_str.count('{') - json_str.count('}')
                    json_str += '}' * bracket_count
                try:
                    outline = json.loads(json_str)
                except json.JSONDecodeError:
                    log("Outline recovery failed, using regex extraction...")
                    title_match = re.search(r'"title"\s*:\s*"([^"]*)"', json_str)
                    synopsis_match = re.search(r'"synopsis"\s*:\s*"([^"]*)"', json_str)
                    outline = {
                        "title": title_match.group(1) if title_match else plot_name,
                        "synopsis": synopsis_match.group(1) if synopsis_match else "",
                        "characters": [],
                        "plot_lines": {"main_line": "", "sub_lines": [], "cause_effect_chains": []},
                        "acts": []
                    }
                    char_blocks = re.findall(r'\{\s*"name"\s*:\s*"([^"]*)"\s*,\s*"name_meaning"\s*:\s*"([^"]*)"\s*,\s*"role"\s*:\s*"([^"]*)"', json_str)
                    for name, meaning, role in char_blocks:
                        outline["characters"].append({"name": name, "name_meaning": meaning, "role": role, "description": ""})
                    ch_blocks = re.findall(r'"number"\s*:\s*(\d+)\s*,\s*"title"\s*:\s*"([^"]*)"\s*,\s*"summary"\s*:\s*"([^"]*)"', json_str)
                    if ch_blocks:
                        act = {"name": "Act 1", "description": "", "chapters": []}
                        for num, title, summary in ch_blocks:
                            act["chapters"].append({
                                "number": int(num), "title": title, "summary": summary,
                                "plot_line_type": "main", "cause_effect": {"caused_by": "", "leads_to": ""},
                                "key_events": [], "word_count_target": 3000, "notes": ""
                            })
                        outline["acts"] = [act]

            self._send_json({"success": True, "outline": outline})

        except Exception as e:
            log(f"Outline error: {e}")
            traceback.print_exc()
            self._send_json({
                "success": True,
                "outline": {
                    "title": f"{plot_name}",
                    "synopsis": f"一部{style}风格的{genre}小说，围绕{theme}展开...",
                    "characters": [
                        {"name": "林逸", "name_meaning": "逸：超逸脱俗，象征主角不凡的命运", "role": "protagonist", "description": "出身平凡的坚毅少年，意外获得改变命运的力量"},
                        {"name": "暗影", "name_meaning": "暗：神秘莫测，影：无处不在", "role": "antagonist", "description": "神秘组织的首领，与主角命运交织"},
                        {"name": "苏晴", "name_meaning": "晴：阳光明媚，象征希望与温暖", "role": "supporting", "description": "主角的挚友/伴侣，在关键时刻给予支持"},
                    ],
                    "plot_lines": {
                        "main_line": "主角从平凡到巅峰的成长之路",
                        "sub_lines": ["友情与背叛的情感纠葛", "世界背后的真相探索"],
                        "cause_effect_chains": [
                            {"cause": "主角获得神秘力量", "effect": "被各方势力盯上", "chapters_involved": [1, 2, 3]},
                            {"cause": "主角突破瓶颈", "effect": "揭开世界真相的一角", "chapters_involved": [4, 5, 6]},
                        ]
                    },
                    "acts": [
                        {"name": "第一幕：开端", "description": "建立世界观，引入主角和核心冲突",
                         "chapters": [
                             {"number": 1, "title": "命运的起点", "summary": "主角的平凡生活被打破，获得改变命运的契机", "plot_line_type": "main", "cause_effect": {"caused_by": "命运的转折", "leads_to": "踏入新世界"}, "key_events": ["引入主角", "展示世界观", "触发事件"], "word_count_target": 3000, "notes": ""},
                             {"number": 2, "title": "初入新世界", "summary": "主角开始接触新的力量体系", "plot_line_type": "main", "cause_effect": {"caused_by": "获得力量", "leads_to": "第一次试炼"}, "key_events": ["能力觉醒", "遇到导师", "第一次试炼"], "word_count_target": 3000, "notes": ""},
                             {"number": 3, "title": "第一次考验", "summary": "主角面临第一个重大挑战", "plot_line_type": "main", "cause_effect": {"caused_by": "初入新世界", "leads_to": "踏上征程"}, "key_events": ["遭遇敌人", "突破极限", "获得成长"], "word_count_target": 3500, "notes": ""},
                         ]},
                        {"name": "第二幕：发展", "description": "冲突升级，主角不断成长",
                         "chapters": [
                             {"number": 4, "title": "踏上征程", "summary": "主角离开舒适区，开始真正的冒险", "plot_line_type": "transition", "cause_effect": {"caused_by": "通过考验", "leads_to": "遭遇危机"}, "key_events": ["离开家乡", "结识伙伴", "明确目标"], "word_count_target": 3000, "notes": ""},
                             {"number": 5, "title": "危机四伏", "summary": "主角团队遭遇重大危机", "plot_line_type": "sub", "cause_effect": {"caused_by": "踏上征程", "leads_to": "实力飞跃"}, "key_events": ["遭遇强敌", "团队考验", "获得宝物"], "word_count_target": 3500, "notes": ""},
                             {"number": 6, "title": "实力飞跃", "summary": "主角获得重大突破", "plot_line_type": "main", "cause_effect": {"caused_by": "危机激发", "leads_to": "最终决战"}, "key_events": ["突破瓶颈", "新能力觉醒", "击败劲敌"], "word_count_target": 3000, "notes": ""},
                         ]},
                        {"name": "第三幕：高潮", "description": "最终对决，主题升华",
                         "chapters": [
                             {"number": 7, "title": "最终决战", "summary": "主角面对最终boss", "plot_line_type": "main", "cause_effect": {"caused_by": "实力飞跃", "leads_to": "新的开始"}, "key_events": ["终极对决", "牺牲与抉择", "主题升华"], "word_count_target": 4000, "notes": ""},
                             {"number": 8, "title": "新的开始", "summary": "战后重建，开启新篇章", "plot_line_type": "transition", "cause_effect": {"caused_by": "最终决战", "leads_to": "未完待续"}, "key_events": ["世界变化", "主角归宿", "留下悬念"], "word_count_target": 3000, "notes": ""},
                         ]}
                    ]
                },
                "note": f"Fallback outline: {str(e)[:100]}"
            })

    def _handle_generate_chapter(self, data):
        chapter_num = data.get('chapter_number', 1)
        chapter_title = data.get('chapter_title', '')
        chapter_summary = data.get('chapter_summary', '')
        genres = data.get('genres', [data.get('genre', '玄幻')])
        if isinstance(genres, str):
            genres = [genres]
        styles = data.get('styles', [data.get('style', '热血爽文')])
        if isinstance(styles, str):
            styles = [styles]
        tones = data.get('tones', [data.get('tone', '紧张刺激')])
        if isinstance(tones, str):
            tones = [tones]
        theme = data.get('theme', '逆境成长')
        schools = data.get('schools', [data.get('school', '')])
        if isinstance(schools, str):
            schools = [schools] if schools else []
        school_names = data.get('school_names', [data.get('school_name', '')])
        if isinstance(school_names, str):
            school_names = [school_names] if school_names else []

        primary_genre = genres[0] if genres else '玄幻'
        primary_school = schools[0] if schools else ''

        genre_str = '、'.join(genres) if len(genres) > 1 else genres[0]
        style_str = '、'.join(styles)
        tone_str = '、'.join(tones)
        school_str_list = '、'.join(school_names) if school_names else ''

        log(f"Generating chapter {chapter_num}: {chapter_title}")

        try:
            genre_map = {gt.label: gt for gt in GenreType}
            genre_enum = genre_map.get(primary_genre)
            genre_context = ""
            if genre_enum:
                genre_manager.set_genre(genre_enum)
                genre_context = genre_manager.get_full_generation_context(include_pleasure=True)

            genre_label = f"{genre_str}（融合）" if len(genres) > 1 else genres[0]
            school_label = f"\n- Writing Schools: {school_str_list}" if school_str_list else ""
            multi_genre_note = ""
            if len(genres) > 1:
                multi_genre_note = f"\n- Cross-genre blend: {genre_str}"

            knowledge_injection = build_knowledge_injection(primary_genre, primary_school)
            if len(genres) > 1:
                for g in genres[1:]:
                    extra_kb = build_knowledge_injection(g, '')
                    if extra_kb:
                        knowledge_injection += "\n" + extra_kb

            prompt = f"""You are a professional {genre_label} novelist writing in {style_str} style with {tone_str} tone.{school_label}{multi_genre_note}

Write Chapter {chapter_num}: {chapter_title}
Summary: {chapter_summary}
Theme: {theme}

{genre_context}

{knowledge_injection}

Requirements:
- Write 2000-3000 Chinese characters
- Include vivid descriptions and natural dialogue
- Maintain consistent pacing
- End with a hook

Write the chapter content directly, no JSON wrapper."""

            log("Calling DeepSeek for chapter...")
            content = engine.models["deepseek"].generate(prompt, temperature=0.85, max_tokens=4000)
            log(f"Chapter response: {len(content)} chars")

            self._send_json({"success": True, "content": content, "chapter_number": chapter_num, "chapter_title": chapter_title})

        except Exception as e:
            log(f"Chapter error: {e}")
            traceback.print_exc()
            self._send_json({
                "success": True,
                "content": f"第{chapter_num}章 {chapter_title}\n\n{chapter_summary}\n\n（AI生成暂时不可用，请稍后重试）",
                "chapter_number": chapter_num,
                "chapter_title": chapter_title,
                "note": f"Fallback: {str(e)[:100]}"
            })

    def _handle_detect_ai(self, data):
        text = data.get('text', '')
        deep = data.get('deep', False)

        if not text:
            self._send_json({"error": "No text provided"}, 400)
            return

        log(f"Detecting AI traces in {len(text)} chars...")

        try:
            from enhanced_ai_detector import EnhancedAIDetector
            from dataclasses import asdict
            detector = EnhancedAIDetector()
            result = detector.detect(text, detail_level="full" if deep else "basic")
            self._send_json({"success": True, "result": asdict(result)})
        except Exception as e:
            log(f"AI detection error: {e}")
            traceback.print_exc()
            self._send_json({
                "success": True,
                "result": {
                    "ai_score": 0.5,
                    "confidence": 0.5,
                    "traits": [],
                    "suggestions": ["无法完成AI检测，请稍后重试"],
                    "note": f"Fallback: {str(e)[:100]}"
                }
            })

    def _handle_rewrite(self, data):
        text = data.get('text', '')
        style = data.get('style', 'deai')

        if not text:
            self._send_json({"error": "No text provided"}, 400)
            return

        log(f"Rewriting {len(text)} chars with style={style}...")

        try:
            rewritten = engine.rewrite(text, style=style)
            self._send_json({"success": True, "content": rewritten})
        except Exception as e:
            log(f"Rewrite error: {e}")
            traceback.print_exc()
            self._send_json({"success": True, "content": text, "note": f"Fallback: {str(e)[:100]}"})


class ThreadedHTTPServer(HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

    def process_request(self, request, client_address):
        t = threading.Thread(target=self.process_request_thread, args=(request, client_address))
        t.daemon = True
        t.start()

    def process_request_thread(self, request, client_address):
        try:
            self.finish_request(request, client_address)
        except Exception:
            traceback.print_exc()
        finally:
            self.shutdown_request(request)


def main():
    port = 8099
    server = ThreadedHTTPServer(('0.0.0.0', port), NWACSHandler)
    print(f"=" * 60)
    print(f"  NWACS 商用级写作工具 v9.0")
    print(f"  http://localhost:{port}")
    print(f"=" * 60)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.shutdown()


if __name__ == '__main__':
    main()
