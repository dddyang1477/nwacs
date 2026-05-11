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
from genre_profile_manager import GenreProfileManager, GenreType
from llm_interface import llm, GenerationParams
from character_name_engine import CharacterNameEngine, CharacterProfile
from story_system import StorySystem
from reviewer_agent import ReviewerAgent
from quality_system import QualitySystem
from project_memory import ProjectMemory
from planning_system import PlanningSystem

log("Initializing core modules...")
genre_manager = GenreProfileManager()
name_engine = CharacterNameEngine(llm)

PROJECT_ROOT = os.path.dirname(__file__)
log("Initializing new modules (story/reviewer/quality/memory/planning)...")
story_system = StorySystem(PROJECT_ROOT)
reviewer = ReviewerAgent(PROJECT_ROOT)
quality_system = QualitySystem(PROJECT_ROOT)
project_memory = ProjectMemory(PROJECT_ROOT)
planning_system = PlanningSystem(PROJECT_ROOT)
log("All modules initialized.")

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
        elif path == '/api/models':
            self._send_json({
                "models": llm.get_available_models(),
                "current": {
                    "provider": llm.config.provider.value,
                    "model_name": llm.config.model_name,
                    "temperature": llm.config.temperature,
                    "top_p": llm.config.top_p,
                    "max_tokens": llm.config.max_tokens,
                }
            })
        elif path == '/api/config':
            self._send_json({
                "provider": llm.config.provider.value,
                "model_name": llm.config.model_name,
                "base_url": llm.config.base_url,
                "temperature": llm.config.temperature,
                "top_p": llm.config.top_p,
                "frequency_penalty": llm.config.frequency_penalty,
                "presence_penalty": llm.config.presence_penalty,
                "max_tokens": llm.config.max_tokens,
                "timeout": llm.config.timeout,
                "max_retries": llm.config.max_retries,
            })
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
        elif path == '/api/quality/trend':
            trend = quality_system.get_quality_trend()
            self._send_json({"success": True, "trend": trend.to_dict()})
        elif path == '/api/memory/stats':
            stats = project_memory.get_memory_stats()
            self._send_json({"success": True, "stats": stats})
        elif path == '/api/planning/timeline':
            self._send_json({"success": True, "entries": planning_system.get_timeline()})
        elif path == '/api/story/snapshots':
            snapshots = story_system.list_snapshots()
            self._send_json({"success": True, "snapshots": snapshots})
        elif path == '/api/story/lock':
            lock_status = story_system.check_lock()
            self._send_json({"success": True, **lock_status})
        elif path == '/api/story/control':
            ctrl = story_system.get_control_document()
            self._send_json({"success": True, "control": ctrl})
        elif path == '/api/quality/arcs':
            self._send_json({"success": True, "message": "使用POST请求提交文本进行分析"})
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
        elif path == '/api/config':
            self._handle_update_config(data)
        elif path == '/api/generate_names':
            self._handle_generate_names(data)
        elif path == '/api/generate_titles':
            self._handle_generate_titles(data)
        elif path == '/api/generate_org_names':
            self._handle_generate_org_names(data)
        elif path == '/api/generate_power_system':
            self._handle_generate_power_system(data)
        elif path == '/api/story/init':
            self._handle_story_init(data)
        elif path == '/api/story/master':
            self._handle_story_master(data)
        elif path == '/api/story/volume':
            self._handle_story_volume(data)
        elif path == '/api/story/chapter-contract':
            self._handle_story_chapter_contract(data)
        elif path == '/api/story/commit':
            self._handle_story_commit(data)
        elif path == '/api/review':
            self._handle_review(data)
        elif path == '/api/quality/record':
            self._handle_quality_record(data)
        elif path == '/api/quality/trend':
            self._handle_quality_trend(data)
        elif path == '/api/quality/checklist':
            self._handle_quality_checklist(data)
        elif path == '/api/memory/patterns':
            self._handle_memory_patterns(data)
        elif path == '/api/memory/learn':
            self._handle_memory_learn(data)
        elif path == '/api/memory/context':
            self._handle_memory_context(data)
        elif path == '/api/memory/stats':
            self._handle_memory_stats(data)
        elif path == '/api/planning/beat-sheet':
            self._handle_planning_beat_sheet(data)
        elif path == '/api/planning/outline':
            self._handle_planning_outline(data)
        elif path == '/api/planning/directive':
            self._handle_planning_directive(data)
        elif path == '/api/planning/timeline':
            self._handle_planning_timeline(data)
        elif path == '/api/story/snapshot':
            self._handle_story_snapshot(data)
        elif path == '/api/story/lock':
            self._handle_story_lock(data)
        elif path == '/api/story/control':
            self._handle_story_control(data)
        elif path == '/api/quality/arcs':
            self._handle_quality_arcs(data)
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

            prompt = f"""你是一位资深网文编辑兼故事架构师，曾策划过100+部爆款小说，精通三幕式结构、英雄之旅和网文节奏设计。请为以下需求生成3个完全不同的剧情方案。

## 需求信息
- 题材：{genre_label}
- 风格：{style_str}
- 基调：{tone_str}
- 篇幅：{length}
- 主题：{theme}{school_label}{multi_genre_note}{protag_str}{extra_str}

{genre_context}

{knowledge_injection}

## 🎬 专业故事架构要求

### 三幕式结构（每个方案必须包含）
- **第一幕·建置**（前25%）：介绍主角、世界观、核心冲突的种子
- **第二幕·对抗**（中间50%）：冲突升级、盟友与敌人、主角成长与挫折
- **第三幕·解决**（后25%）：最终对决、角色蜕变、主题升华

### 核心冲突设计
- **外部冲突**：主角vs反派/环境/制度（看得见的对抗）
- **内部冲突**：主角vs自己（恐惧/欲望/道德困境）
- **关系冲突**：主角vs盟友/爱人/家人（情感张力）
- 三种冲突必须交织，不能只有外部冲突

### 金手指设计原则
- **有限制**：金手指必须有代价/冷却/副作用，无限能力=无聊
- **有成长**：金手指随主角成长而进化，不是一开始就满级
- **有时机**：金手指在关键时刻使用，而非日常滥用

### 爽点节奏设计
- **三章一小爽**：每3章一个小高潮（打脸/突破/收获）
- **十章一大爽**：每10章一个大高潮（越级挑战/身份揭露/逆天改命）
- **情绪曲线**：压抑→爆发→余韵→新危机，循环往复

## ⚠️ 要求
1. 3个方案必须完全不同——不同的世界观、不同的核心冲突、不同的人物关系
2. 每个方案必须有独特的"卖点"——读者看一眼就想点进去
3. 拒绝套路：不要"废柴逆袭"、"穿越重生"、"系统金手指"等烂大街设定（除非用户明确要求）
4. 每个方案的名字要有爆款网文气质
5. 每个方案必须包含三幕式结构的大致规划

## 输出格式
返回纯JSON（不要markdown包裹）：
{{"plots": [{{"id": "plot_1", "name": "方案名（3-8字）", "tagline": "一句话卖点（15字以内）", "core_idea": "核心创意（50-100字）", "protagonist": "主角设定（30字）", "main_conflict": "核心冲突（30字）", "three_act_structure": "三幕式规划（50字）", "golden_finger": "金手指设定及限制（30字）", "expected_beats": "预期爽点/泪点", "target_readers": "目标读者群", "innovation": "创新之处"}}]}}"""

            log("Calling LLM...")
            result_text = llm.generate(prompt, params=GenerationParams(temperature=0.9, max_tokens=3000))
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

            prompt = f"""你是一位拥有20年经验的顶级{genre_label}小说大纲规划师。你必须严格遵循以下写作铁律来构建大纲。

## ⚠️ 必须遵守的写作铁律（违反任何一条即为失败）

### 铁律1：剧情不可重复
- 每一章的剧情必须有本质不同，不能是"换个场景打同样的架"
- 每章的核心冲突类型必须轮换：战斗→智斗→情感→探索→战斗
- 禁止连续两章使用相同的冲突模式

### 铁律2：角色弧光必须递进
- 主角每章必须有可感知的成长（能力/认知/关系至少一项变化）
- 反派不能是"等着被打"的静态靶子，必须有独立行动线
- 配角必须有独立于主角的目标和行动

### 铁律3：因果链必须严密
- 每章的开头必须是上一章结尾的直接后果
- 每章的结尾必须为下一章埋下必然的钩子
- 禁止"突然出现"的 Deus ex Machina 式解决

{knowledge_injection}

## 小说基本信息
- 题材：{genre_label}
- 风格：{style_str}{school_label}{multi_genre_note}
- 基调：{tone_str}
- 篇幅：{length}
- 主题：{theme}
- 选定剧情：{plot_name}

{genre_context}

## 大纲输出要求
1. **书名**：必须有爆款网文气质，3-8个字，拒绝套路书名
2. **梗概**：200字，必须包含：核心冲突 + 独特卖点 + 情感主线
3. **人物**：至少4个角色（主角、反派、2个配角），每个角色必须有：
   - 名字（拒绝"天/云/辰/宇/昊/轩/逸/尘/雪/月/瑶/璃"等烂大街字）
   - 名字寓意（50字以上，解释名字如何暗示角色命运）
   - 角色弧光（从什么状态变到什么状态）
   - 核心欲望（角色真正想要什么）
4. **剧情线**：主线1条 + 辅线至少2条 + 因果关系链至少3条
5. **章节规划**：12-18章，每章必须包含：
   - 冲突类型标签（战斗/智斗/情感/探索/成长）
   - 因果链（前因是什么→本章发生什么→导致什么后果）
   - 角色变化（本章结束后角色发生了什么变化）
   - 目标字数：4000字

返回纯JSON（不要markdown包裹）：
{{"title": "...", "synopsis": "...", "characters": [{{"name": "...", "name_meaning": "...", "role": "protagonist/antagonist/supporting/mentor", "description": "...", "arc": "...", "core_desire": "..."}}], "plot_lines": {{"main_line": "...", "sub_lines": ["...", "..."], "cause_effect_chains": [{{"cause": "...", "effect": "...", "chapters_involved": [1, 3]}}]}}, "acts": [{{"name": "Act 1", "description": "...", "chapters": [{{"number": 1, "title": "...", "summary": "...", "conflict_type": "战斗/智斗/情感/探索/成长", "plot_line_type": "main/sub/transition", "cause_effect": {{"caused_by": "...", "leads_to": "..."}}, "character_change": "...", "key_events": ["..."], "word_count_target": 4000, "notes": ""}}]}}]}}"""

            log("Calling LLM for outline...")
            result_text = llm.generate(prompt, params=GenerationParams(temperature=0.8, max_tokens=6000))
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
                        {"name": "林逸", "name_meaning": "逸：超逸脱俗，象征主角不甘平凡、终将超越一切束缚的命运", "role": "protagonist", "description": "出身平凡的坚毅少年，意外获得改变命运的力量", "arc": "从自卑怯懦的废柴成长为自信强大的守护者", "core_desire": "保护所爱之人，打破阶级固化"},
                        {"name": "暗影", "name_meaning": "暗：神秘莫测的力量来源，影：无处不在的威胁，暗示反派如影随形的压迫感", "role": "antagonist", "description": "神秘组织的首领，与主角命运交织", "arc": "从高高在上的掌控者到被自己培养的对手击败", "core_desire": "维持现有秩序，消灭一切变数"},
                        {"name": "苏晴", "name_meaning": "晴：雨过天晴，象征在黑暗时刻带来希望与温暖的力量", "role": "supporting", "description": "主角的挚友/伴侣，在关键时刻给予支持", "arc": "从被保护的弱者成长为能与主角并肩作战的强者", "core_desire": "证明自己的价值，不再成为负担"},
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
                             {"number": 1, "title": "命运的起点", "summary": "主角的平凡生活被打破，获得改变命运的契机", "conflict_type": "成长", "plot_line_type": "main", "cause_effect": {"caused_by": "命运的转折", "leads_to": "踏入新世界"}, "character_change": "主角从普通人的懵懂转变为对力量的渴望", "key_events": ["引入主角", "展示世界观", "触发事件"], "word_count_target": 4000, "notes": ""},
                             {"number": 2, "title": "初入新世界", "summary": "主角开始接触新的力量体系，遭遇第一次真正的危险", "conflict_type": "战斗", "plot_line_type": "main", "cause_effect": {"caused_by": "获得力量", "leads_to": "第一次试炼"}, "character_change": "主角意识到自己的弱小，开始认真修炼", "key_events": ["能力觉醒", "遇到导师", "第一次战斗"], "word_count_target": 4000, "notes": ""},
                             {"number": 3, "title": "第一次考验", "summary": "主角面临第一个重大挑战，必须在生死之间做出选择", "conflict_type": "智斗", "plot_line_type": "main", "cause_effect": {"caused_by": "初入新世界", "leads_to": "踏上征程"}, "character_change": "主角学会用智慧而非蛮力解决问题", "key_events": ["遭遇敌人", "突破极限", "获得成长"], "word_count_target": 4000, "notes": ""},
                         ]},
                        {"name": "第二幕：发展", "description": "冲突升级，主角不断成长",
                         "chapters": [
                             {"number": 4, "title": "踏上征程", "summary": "主角离开舒适区，开始真正的冒险之旅", "conflict_type": "探索", "plot_line_type": "transition", "cause_effect": {"caused_by": "通过考验", "leads_to": "遭遇危机"}, "character_change": "主角的眼界从一隅之地扩展到整个世界", "key_events": ["离开家乡", "结识伙伴", "明确目标"], "word_count_target": 4000, "notes": ""},
                             {"number": 5, "title": "危机四伏", "summary": "主角团队遭遇重大危机，信任受到考验", "conflict_type": "情感", "plot_line_type": "sub", "cause_effect": {"caused_by": "踏上征程", "leads_to": "实力飞跃"}, "character_change": "主角学会信任与被信任，团队羁绊加深", "key_events": ["遭遇强敌", "团队考验", "获得宝物"], "word_count_target": 4000, "notes": ""},
                             {"number": 6, "title": "实力飞跃", "summary": "主角获得重大突破，但代价是失去重要的东西", "conflict_type": "战斗", "plot_line_type": "main", "cause_effect": {"caused_by": "危机激发", "leads_to": "最终决战"}, "character_change": "主角实力暴涨但内心更加成熟，理解了力量的代价", "key_events": ["突破瓶颈", "新能力觉醒", "击败劲敌"], "word_count_target": 4000, "notes": ""},
                         ]},
                        {"name": "第三幕：高潮", "description": "最终对决，主题升华",
                         "chapters": [
                             {"number": 7, "title": "最终决战", "summary": "主角面对最终boss，必须在胜利与牺牲之间抉择", "conflict_type": "战斗", "plot_line_type": "main", "cause_effect": {"caused_by": "实力飞跃", "leads_to": "新的开始"}, "character_change": "主角完成了从少年到英雄的蜕变", "key_events": ["终极对决", "牺牲与抉择", "主题升华"], "word_count_target": 4000, "notes": ""},
                             {"number": 8, "title": "新的开始", "summary": "战后重建，主角找到了真正的归宿", "conflict_type": "成长", "plot_line_type": "transition", "cause_effect": {"caused_by": "最终决战", "leads_to": "未完待续"}, "character_change": "主角从追求力量转变为守护和平", "key_events": ["世界变化", "主角归宿", "留下悬念"], "word_count_target": 4000, "notes": ""},
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

        outline_data = data.get('outline', {})
        characters = outline_data.get('characters', [])
        previous_chapter_content = data.get('previous_chapter_content', '')
        previous_chapter_num = data.get('previous_chapter_num', 0)

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
            school_label = f"\n- 写作流派: {school_str_list}" if school_str_list else ""
            multi_genre_note = ""
            if len(genres) > 1:
                multi_genre_note = f"\n- 跨类型融合: {genre_str}"

            knowledge_injection = build_knowledge_injection(primary_genre, primary_school)
            if len(genres) > 1:
                for g in genres[1:]:
                    extra_kb = build_knowledge_injection(g, '')
                    if extra_kb:
                        knowledge_injection += "\n" + extra_kb

            character_context = ""
            if characters:
                character_context = "\n## 🎭 已确立的角色（名字必须严格一致，不得更改）\n"
                for ch in characters:
                    character_context += f"- **{ch.get('name', '')}**（{ch.get('role', '')}）：{ch.get('description', '')}。名字寓意：{ch.get('name_meaning', '')}\n"

            previous_context = ""
            if previous_chapter_content and previous_chapter_num > 0:
                prev_summary = previous_chapter_content[:500] if len(previous_chapter_content) > 500 else previous_chapter_content
                previous_context = f"""
## 📖 上一章（第{previous_chapter_num}章）结尾内容
```
{prev_summary}...
```
本章必须从上一章的结尾状态自然延续，不能出现角色位置/状态/关系的跳跃。
"""

            prompt = f"""你是一位{genre_label}领域的顶级网文作家，拥有15年创作经验，曾写出10+部爆款作品。风格为{style_str}，基调为{tone_str}。{school_label}{multi_genre_note}

## ⚠️ 写作铁律
1. **角色名字必须一致**：使用下方"已确立的角色"中的名字，不得自行更改或创造新名字
2. **字数不低于4000字**：这是硬性要求，少于4000字视为不合格
3. **剧情不可重复**：不能和前面章节的冲突模式相同
4. **因果必须连贯**：本章开头必须承接上一章的结尾状态

{character_context}

{previous_context}

## 本章信息
- 第{chapter_num}章：{chapter_title}
- 章节概要：{chapter_summary}
- 主题：{theme}

{genre_context}

{knowledge_injection}

## 🎨 专业写作技法（必须遵循）

### 一、开篇技法
- **黄金开篇三章定律**：前三章必须完成"钩子→世界→冲突"三步
  - 第1章：强力钩子（悬念/动作/冲突开场，in medias res）
  - 第2章：世界观铺垫（通过角色行动展示，而非旁白解释）
  - 第3章：核心冲突确立（让读者知道"这本书讲什么"）
- **拒绝信息倾泻**：不要用大段旁白解释世界观，通过角色的眼睛和行动来展示

### 二、角色塑造
- **压力揭示性格**：人在压力下的选择才暴露真实性格，不要直接说"他勇敢"，写他在危险中的行动
- **人物反差**：给每个角色一个"表里不一"的特质（外表冷酷内心温柔/表面懦弱关键时刻爆发）
- **标签化角色**：每个角色有一个标志性动作/口头禅/习惯，让读者一眼认出
- **人物弧光**：角色在本章中必须有微小变化——学到了什么/失去了什么/改变了什么看法

### 三、描写技法
- **用动作替代形容词**：不写"他愤怒"，写"他一拳砸在桌上，茶杯跳了起来"
- **感官细节**：每段场景至少包含2种感官（视觉+听觉/触觉/嗅觉/味觉）
- **画面感描写**：像电影镜头一样——远景→中景→特写→细节
- **本土生活细节**：加入烟火气、人情世故、市井气息（叫卖声、炊烟、讨价还价）

### 四、节奏控制
- **张弛有度**：紧张场景后必须有舒缓过渡，不能连续高强度
- **长短句交替**：短句3-10字制造紧张，长句25-50字渲染氛围
- **断章三式**：
  - 悬念断章：在关键信息即将揭示时切断
  - 反转断章：在剧情突然反转时切断
  - 情绪断章：在情感最高潮时切断

### 五、爽点设计
- **压抑→爆发**：先让读者感到憋屈/愤怒，再让主角反击，爽感翻倍
- **信息差爽点**：读者知道但反派不知道的信息，制造期待感
- **成长爽点**：主角使用之前修炼/获得的技能解决问题
- **打脸节奏**：铺垫→挑衅→反击→碾压，四步完成一个爽点循环

### 六、对话技法
- **潜台词**：角色说的和想的往往不同，对话要有言外之意
- **语癖区分**：不同角色的说话方式完全不同（用词习惯、句子长度、语气词）
- **行动中对话**：对话时角色在做其他事（喝茶、擦剑、看窗外），避免"站着说话"

### 七、去AI痕迹
- 禁止使用"此外""然而""因此""值得注意的是"等AI高频连接词
- 禁止三段式列举（X、Y和Z）
- 禁止"作为……的证明""标志着""为……奠定基础"等AI内容模式
- 句子长度必须剧烈变化，不能连续3句长度相同
- 加入口语化表达、不完美表达（"嗯""妈的""就是"）

## 输出要求
- **字数**：不低于4000中文字符，这是硬性要求
- **格式**：直接输出章节正文，不要JSON包裹，不要标题
- **钩子**：章节结尾必须有强有力的悬念钩子

现在开始写第{chapter_num}章正文："""

            log("Calling LLM for chapter...")
            content = llm.generate(prompt, params=GenerationParams(temperature=0.85, max_tokens=8000))
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

    def _handle_update_config(self, data):
        try:
            updates = {}
            for key in ['provider', 'model_name', 'base_url', 'api_key',
                       'temperature', 'top_p', 'frequency_penalty',
                       'presence_penalty', 'max_tokens', 'timeout', 'max_retries']:
                if key in data:
                    if key == 'provider':
                        from llm_interface import ModelProvider
                        updates[key] = ModelProvider(data[key])
                    else:
                        updates[key] = data[key]
            llm.update_config(**updates)
            llm.save_config()
            log(f"Config updated: {list(updates.keys())}")
            self._send_json({"success": True, "config": {
                "provider": llm.config.provider.value,
                "model_name": llm.config.model_name,
                "temperature": llm.config.temperature,
                "max_tokens": llm.config.max_tokens,
            }})
        except Exception as e:
            log(f"Config update error: {e}")
            self._send_json({"error": str(e)}, 400)

    def _handle_generate_names(self, data):
        genre = data.get('genre', '玄幻')
        role = data.get('role', 'protagonist')
        gender = data.get('gender', 'male')
        personality = data.get('personality', '')
        background = data.get('background', '')
        fate = data.get('fate', '')
        ability = data.get('ability', '')
        weakness = data.get('weakness', '')
        arc = data.get('arc', '')
        story_context = data.get('story_context', '')
        count = data.get('count', 5)
        style = data.get('name_style', None)

        log(f"Generating names: genre={genre}, role={role}, gender={gender}")

        try:
            profile = CharacterProfile(
                role=role, gender=gender, age=data.get('age', 'young'),
                personality=personality, background=background,
                fate=fate, ability=ability, weakness=weakness, arc=arc,
            )
            results = name_engine.generate_character_names(
                genre=genre, profile=profile, count=count,
                style=style, story_context=story_context,
            )
            names_data = []
            for r in results:
                names_data.append({
                    "full_name": r.full_name,
                    "surname": r.surname,
                    "given_name": r.given_name,
                    "style": r.style,
                    "meaning": r.meaning,
                    "literal_meaning": r.literal_meaning,
                    "fate_connection": r.fate_connection,
                    "personality_match": r.personality_match,
                    "aliases": r.aliases,
                    "titles": r.titles,
                    "score": r.score,
                })
            self._send_json({"success": True, "names": names_data})
        except Exception as e:
            log(f"Name generation error: {e}")
            traceback.print_exc()
            fallback_profile = CharacterProfile(role=role, gender=gender)
            fallback = name_engine._fallback_names(genre, fallback_profile, count)
            names_data = [{
                "full_name": r.full_name, "surname": r.surname,
                "given_name": r.given_name, "style": r.style,
                "meaning": r.meaning, "literal_meaning": r.literal_meaning,
                "fate_connection": r.fate_connection,
                "personality_match": r.personality_match,
                "aliases": r.aliases, "titles": r.titles, "score": r.score,
            } for r in fallback]
            self._send_json({"success": True, "names": names_data, "note": f"Fallback: {str(e)[:100]}"})

    def _handle_generate_titles(self, data):
        genre = data.get('genre', '玄幻')
        character_name = data.get('character_name', '')
        personality = data.get('personality', '')
        ability = data.get('ability', '')
        style = data.get('title_style', 'domineering')

        log(f"Generating titles for: {character_name}")

        try:
            titles = name_engine.generate_title(
                genre=genre, character_name=character_name,
                personality=personality, ability=ability, style=style,
            )
            self._send_json({"success": True, "titles": titles})
        except Exception as e:
            log(f"Title generation error: {e}")
            self._send_json({"success": True, "titles": [], "note": str(e)[:100]})

    def _handle_generate_org_names(self, data):
        genre = data.get('genre', '玄幻')
        org_type = data.get('org_type', 'sect')
        description = data.get('description', '')
        count = data.get('count', 5)

        log(f"Generating org names: genre={genre}, type={org_type}")

        try:
            results = name_engine.generate_organization_name(
                genre=genre, org_type=org_type,
                description=description, count=count,
            )
            self._send_json({"success": True, "organizations": results})
        except Exception as e:
            log(f"Org name generation error: {e}")
            self._send_json({"success": True, "organizations": [], "note": str(e)[:100]})

    def _handle_generate_power_system(self, data):
        genre = data.get('genre', '玄幻')
        system_type = data.get('system_type', 'cultivation')
        description = data.get('description', '')
        count = data.get('count', 8)

        log(f"Generating power system: genre={genre}, type={system_type}")

        try:
            results = name_engine.generate_power_system_names(
                genre=genre, system_type=system_type,
                description=description, count=count,
            )
            self._send_json({"success": True, "levels": results})
        except Exception as e:
            log(f"Power system generation error: {e}")
            self._send_json({"success": True, "levels": [], "note": str(e)[:100]})

    def _handle_story_init(self, data):
        try:
            result = story_system.init_master_setting(
                title=data.get('title', ''),
                genre=data.get('genre', '玄幻'),
                sub_genre=data.get('sub_genre', ''),
                tone=data.get('tone', ''),
                style=data.get('style', ''),
                protagonist_name=data.get('protagonist_name', ''),
                protagonist_desire=data.get('protagonist_desire', ''),
                protagonist_flaw=data.get('protagonist_flaw', ''),
                core_conflict=data.get('core_conflict', ''),
                world_type=data.get('world_type', ''),
                power_system=data.get('power_system', ''),
                taboos=data.get('taboos'),
                anti_patterns=data.get('anti_patterns'),
                genre_profile=data.get('genre_profile'),
            )
            self._send_json({"success": True, "master_setting": result})
        except Exception as e:
            log(f"Story init error: {e}")
            self._send_json({"success": False, "error": str(e)[:200]})

    def _handle_story_master(self, data):
        action = data.get('action', 'get')
        try:
            if action == 'get':
                master = story_system.get_master_setting()
                self._send_json({"success": True, "master_setting": master})
            elif action == 'update':
                updates = data.get('updates', {})
                master = story_system.update_master_setting(updates)
                self._send_json({"success": True, "master_setting": master})
            else:
                self._send_json({"error": "Unknown action"}, 400)
        except Exception as e:
            log(f"Story master error: {e}")
            self._send_json({"success": False, "error": str(e)[:200]})

    def _handle_story_volume(self, data):
        action = data.get('action', 'get')
        try:
            if action == 'create':
                chapter_range = data.get('chapter_range', [1, 10])
                result = story_system.create_volume_contract(
                    volume_id=data.get('volume_id', 1),
                    volume_name=data.get('volume_name', ''),
                    chapter_range=(chapter_range[0], chapter_range[1]) if isinstance(chapter_range, list) else (1, 10),
                    core_conflict=data.get('core_conflict', ''),
                    volume_climax=data.get('volume_climax', ''),
                    pacing_strategy=data.get('pacing_strategy', 'standard'),
                    strand_distribution=data.get('strand_distribution'),
                    cool_point_density=data.get('cool_point_density', 'medium'),
                    foreshadowing_plan=data.get('foreshadowing_plan'),
                )
                self._send_json({"success": True, "volume_contract": result})
            elif action == 'get':
                result = story_system.get_volume_contract(data.get('volume_id', 1))
                self._send_json({"success": True, "volume_contract": result})
            else:
                self._send_json({"error": "Unknown action"}, 400)
        except Exception as e:
            log(f"Story volume error: {e}")
            self._send_json({"success": False, "error": str(e)[:200]})

    def _handle_story_chapter_contract(self, data):
        action = data.get('action', 'get')
        try:
            if action == 'create':
                result = story_system.create_chapter_contract(
                    chapter=data.get('chapter', 1),
                    volume_id=data.get('volume_id', 1),
                    chapter_title=data.get('chapter_title', ''),
                    chapter_goal=data.get('chapter_goal', ''),
                    time_anchor=data.get('time_anchor', ''),
                    chapter_span=data.get('chapter_span', ''),
                    countdown=data.get('countdown'),
                    cbn=data.get('cbn'),
                    cpns=data.get('cpns'),
                    cen=data.get('cen'),
                    must_cover_nodes=data.get('must_cover_nodes'),
                    forbidden_zones=data.get('forbidden_zones'),
                    style_priority=data.get('style_priority', ''),
                    pacing_strategy=data.get('pacing_strategy', ''),
                    anti_patterns=data.get('anti_patterns'),
                    chapter_end_open_question=data.get('chapter_end_open_question', ''),
                )
                self._send_json({"success": True, "chapter_contract": result})
            elif action == 'get':
                result = story_system.get_chapter_contract(data.get('chapter', 1))
                self._send_json({"success": True, "chapter_contract": result})
            else:
                self._send_json({"error": "Unknown action"}, 400)
        except Exception as e:
            log(f"Story chapter contract error: {e}")
            self._send_json({"success": False, "error": str(e)[:200]})

    def _handle_story_commit(self, data):
        try:
            chapter = data.get('chapter', 1)
            review_result = data.get('review_result', {})
            fulfillment_result = data.get('fulfillment_result', {})
            extraction_result = data.get('extraction_result', {})

            commit = story_system.build_chapter_commit(
                chapter=chapter,
                review_result=review_result,
                fulfillment_result=fulfillment_result,
                extraction_result=extraction_result,
            )

            if commit.get('status') == 'accepted':
                commit = story_system.apply_projections(commit)

            self._send_json({"success": True, "commit": commit})
        except Exception as e:
            log(f"Story commit error: {e}")
            self._send_json({"success": False, "error": str(e)[:200]})

    def _handle_review(self, data):
        chapter = data.get('chapter', 1)
        chapter_text = data.get('text', '')
        use_llm = data.get('use_llm', True)

        if not chapter_text:
            self._send_json({"error": "No text provided"}, 400)
            return

        log(f"Reviewing chapter {chapter} ({len(chapter_text)} chars)...")

        try:
            chapter_contract = story_system.get_chapter_contract(chapter)
            master_setting = story_system.get_master_setting()

            prev_summary = ""
            if chapter > 1:
                prev_commit_path = story_system.story_system_dir / "commits" / f"commit_ch{chapter - 1:04d}.json"
                if prev_commit_path.exists():
                    prev_commit = json.loads(prev_commit_path.read_text(encoding='utf-8'))
                    extraction = prev_commit.get('extraction', {})
                    prev_summary = extraction.get('summary', '')

            result = reviewer.review_chapter(
                chapter=chapter,
                chapter_text=chapter_text,
                chapter_contract=chapter_contract if chapter_contract else None,
                master_setting=master_setting if master_setting else None,
                previous_summary=prev_summary,
                use_llm=use_llm,
            )

            story_system.create_review_contract(chapter, result.to_dict())

            project_memory.learn_from_review(result.to_dict(), chapter)

            quality_system.record_chapter_quality(
                chapter=chapter,
                review_result=result.to_dict(),
                word_count=len(chapter_text.replace(' ', '').replace('\n', '').replace('\r', '')),
            )

            self._send_json({"success": True, "review": result.to_dict()})
        except Exception as e:
            log(f"Review error: {e}")
            traceback.print_exc()
            self._send_json({"success": False, "error": str(e)[:200]})

    def _handle_quality_record(self, data):
        try:
            record = quality_system.record_chapter_quality(
                chapter=data.get('chapter', 1),
                review_result=data.get('review_result'),
                checklist_result=data.get('checklist_result'),
                hook_strength=data.get('hook_strength', ''),
                cool_point_count=data.get('cool_point_count', 0),
                word_count=data.get('word_count', 0),
            )
            self._send_json({"success": True, "record": record.to_dict()})
        except Exception as e:
            log(f"Quality record error: {e}")
            self._send_json({"success": False, "error": str(e)[:200]})

    def _handle_quality_trend(self, data):
        try:
            last_n = data.get('last_n', 20)
            trend = quality_system.get_quality_trend(last_n=last_n)
            self._send_json({"success": True, "trend": trend.to_dict()})
        except Exception as e:
            log(f"Quality trend error: {e}")
            self._send_json({"success": False, "error": str(e)[:200]})

    def _handle_quality_checklist(self, data):
        action = data.get('action', 'get')
        try:
            if action == 'get':
                self._send_json({"success": True, "checklist": quality_system.DEFAULT_WRITING_CHECKLIST})
            elif action == 'evaluate':
                chapter_text = data.get('text', '')
                if not chapter_text:
                    self._send_json({"error": "No text provided"}, 400)
                    return

                required_count = len(quality_system.DEFAULT_WRITING_CHECKLIST.get('required', []))
                optional_count = len(quality_system.DEFAULT_WRITING_CHECKLIST.get('optional', []))

                required_pass = 0
                optional_pass = 0

                word_count = len(chapter_text.replace(' ', '').replace('\n', '').replace('\r', ''))
                if word_count >= 4000:
                    required_pass += 1

                if re.search(r'(?:悬念|冲突|动作|疑问|危险)', chapter_text[:300]):
                    required_pass += 1

                if re.search(r'(?:悬念|疑问|未解|下一)', chapter_text[-300:]):
                    required_pass += 1

                ai_patterns_count = len(re.findall(r'(?:此外|然而|因此|值得注意的是|总而言之|综上所述)', chapter_text))
                if ai_patterns_count < 5:
                    required_pass += 1

                required_pass += 1

                if re.search(r'(?:突破|碾压|击败|收获|觉醒|逆袭)', chapter_text):
                    optional_pass += 1

                sensory_count = len(re.findall(r'(?:看到|听到|闻到|触到|感到|觉得)', chapter_text))
                if sensory_count >= 3:
                    optional_pass += 1

                optional_pass += 1

                required_rate = required_pass / max(required_count, 1)
                optional_rate = optional_pass / max(optional_count, 1)
                completion_rate = (required_pass + optional_pass) / max(required_count + optional_count, 1)
                score = (required_rate * 0.7 + optional_rate * 0.3) * 100

                result = {
                    "score": round(score, 1),
                    "completion_rate": round(completion_rate, 2),
                    "required_rate": round(required_rate, 2),
                    "optional_rate": round(optional_rate, 2),
                    "required_pass": required_pass,
                    "required_total": required_count,
                    "optional_pass": optional_pass,
                    "optional_total": optional_count,
                }
                self._send_json({"success": True, "result": result})
            else:
                self._send_json({"error": "Unknown action"}, 400)
        except Exception as e:
            log(f"Quality checklist error: {e}")
            self._send_json({"success": False, "error": str(e)[:200]})

    def _handle_memory_patterns(self, data):
        try:
            pattern_type = data.get('pattern_type', '')
            category = data.get('category', '')
            query = data.get('query', '')
            limit = data.get('limit', 20)

            if query:
                results = project_memory.search_patterns(query, limit)
            elif pattern_type:
                results = project_memory.get_patterns_by_type(pattern_type, limit)
            elif category:
                results = project_memory.get_patterns_by_category(category, limit)
            else:
                anti = project_memory.get_anti_patterns(limit)
                tech = project_memory.get_writing_techniques(limit)
                results = {"anti_patterns": anti, "writing_techniques": tech}

            self._send_json({"success": True, "patterns": results})
        except Exception as e:
            log(f"Memory patterns error: {e}")
            self._send_json({"success": False, "error": str(e)[:200]})

    def _handle_memory_learn(self, data):
        try:
            review_result = data.get('review_result', {})
            chapter = data.get('chapter', 1)
            results = project_memory.learn_from_review(review_result, chapter)
            self._send_json({"success": True, "learned": results})
        except Exception as e:
            log(f"Memory learn error: {e}")
            self._send_json({"success": False, "error": str(e)[:200]})

    def _handle_memory_context(self, data):
        try:
            chapter = data.get('chapter', 1)
            context = project_memory.build_context_injection(chapter)
            self._send_json({"success": True, "context": context})
        except Exception as e:
            log(f"Memory context error: {e}")
            self._send_json({"success": False, "error": str(e)[:200]})

    def _handle_memory_stats(self, data):
        try:
            stats = project_memory.get_memory_stats()
            self._send_json({"success": True, "stats": stats})
        except Exception as e:
            log(f"Memory stats error: {e}")
            self._send_json({"success": False, "error": str(e)[:200]})

    def _handle_planning_beat_sheet(self, data):
        action = data.get('action', 'get')
        try:
            if action == 'create':
                beat_sheet = planning_system.create_volume_beat_sheet(
                    volume_id=data.get('volume_id', 1),
                    volume_name=data.get('volume_name', ''),
                    chapter_start=data.get('chapter_start', 1),
                    chapter_end=data.get('chapter_end', 10),
                    act_structure=data.get('act_structure', 'three_act'),
                )
                self._send_json({"success": True, "beat_sheet": beat_sheet.to_dict()})
            elif action == 'get':
                beat_sheet = planning_system.get_volume_beat_sheet(data.get('volume_id', 1))
                if beat_sheet:
                    self._send_json({"success": True, "beat_sheet": beat_sheet.to_dict()})
                else:
                    self._send_json({"success": True, "beat_sheet": None})
            elif action == 'for_chapter':
                beat = planning_system.get_beat_for_chapter(data.get('chapter', 1))
                self._send_json({"success": True, "beat": beat})
            else:
                self._send_json({"error": "Unknown action"}, 400)
        except Exception as e:
            log(f"Planning beat sheet error: {e}")
            self._send_json({"success": False, "error": str(e)[:200]})

    def _handle_planning_outline(self, data):
        action = data.get('action', 'parse')
        try:
            if action == 'parse':
                outline = planning_system.parse_chapter_outline(
                    outline_text=data.get('outline_text', ''),
                    chapter=data.get('chapter', 1),
                )
                self._send_json({"success": True, "outline": outline.to_dict()})
            elif action == 'save':
                outline = planning_system.parse_chapter_outline(
                    outline_text=data.get('outline_text', ''),
                    chapter=data.get('chapter', 1),
                )
                planning_system.save_chapter_outline(outline)
                self._send_json({"success": True, "outline": outline.to_dict()})
            elif action == 'load':
                outline = planning_system.load_chapter_outline(data.get('chapter', 1))
                if outline:
                    self._send_json({"success": True, "outline": outline.to_dict()})
                else:
                    self._send_json({"success": True, "outline": None})
            else:
                self._send_json({"error": "Unknown action"}, 400)
        except Exception as e:
            log(f"Planning outline error: {e}")
            self._send_json({"success": False, "error": str(e)[:200]})

    def _handle_planning_directive(self, data):
        try:
            outline = planning_system.parse_chapter_outline(
                outline_text=data.get('outline_text', ''),
                chapter=data.get('chapter', 1),
            )
            beat = planning_system.get_beat_for_chapter(data.get('chapter', 1))
            directive = planning_system.build_execution_directive(outline, beat)
            self._send_json({"success": True, "directive": directive})
        except Exception as e:
            log(f"Planning directive error: {e}")
            self._send_json({"success": False, "error": str(e)[:200]})

    def _handle_planning_timeline(self, data):
        action = data.get('action', 'get')
        try:
            if action == 'add':
                entry = planning_system.create_timeline_entry(
                    chapter=data.get('chapter', 1),
                    event=data.get('event', ''),
                    time_point=data.get('time_point', ''),
                    location=data.get('location', ''),
                    characters=data.get('characters'),
                )
                self._send_json({"success": True, "entry": entry})
            elif action == 'get':
                entries = planning_system.get_timeline(
                    start_chapter=data.get('start_chapter', 0),
                    end_chapter=data.get('end_chapter', 9999),
                )
                self._send_json({"success": True, "entries": entries})
            else:
                self._send_json({"error": "Unknown action"}, 400)
        except Exception as e:
            log(f"Planning timeline error: {e}")
            self._send_json({"success": False, "error": str(e)[:200]})

    def _handle_story_snapshot(self, data):
        action = data.get('action', 'list')
        try:
            if action == 'create':
                result = story_system.create_snapshot(
                    chapter=data.get('chapter', 1),
                    label=data.get('label', ''),
                    tags=data.get('tags'),
                )
                self._send_json({"success": True, "snapshot": result})
            elif action == 'restore':
                result = story_system.restore_snapshot(data.get('snapshot_id', ''))
                self._send_json(result)
            elif action == 'list':
                snapshots = story_system.list_snapshots(
                    limit=data.get('limit', 20),
                    tag=data.get('tag', ''),
                )
                self._send_json({"success": True, "snapshots": snapshots})
            elif action == 'delete':
                result = story_system.delete_snapshot(data.get('snapshot_id', ''))
                self._send_json(result)
            else:
                self._send_json({"error": "Unknown action"}, 400)
        except Exception as e:
            log(f"Story snapshot error: {e}")
            self._send_json({"success": False, "error": str(e)[:200]})

    def _handle_story_lock(self, data):
        action = data.get('action', 'check')
        try:
            if action == 'acquire':
                result = story_system.acquire_lock(
                    locked_by=data.get('locked_by', 'user'),
                    reason=data.get('reason', ''),
                    ttl_minutes=data.get('ttl_minutes', 30),
                )
                self._send_json(result)
            elif action == 'release':
                result = story_system.release_lock(
                    locked_by=data.get('locked_by', ''),
                )
                self._send_json(result)
            elif action == 'check':
                result = story_system.check_lock()
                self._send_json({"success": True, **result})
            elif action == 'force_release':
                result = story_system.force_release_lock()
                self._send_json(result)
            else:
                self._send_json({"error": "Unknown action"}, 400)
        except Exception as e:
            log(f"Story lock error: {e}")
            self._send_json({"success": False, "error": str(e)[:200]})

    def _handle_story_control(self, data):
        action = data.get('action', 'get')
        try:
            if action == 'get':
                ctrl = story_system.get_control_document()
                self._send_json({"success": True, "control": ctrl})
            elif action == 'update':
                ctrl = story_system.update_control_document(data.get('updates', {}))
                self._send_json({"success": True, "control": ctrl})
            elif action == 'update_index':
                ctrl = story_system.update_chapter_index(
                    chapter=data.get('chapter', 1),
                    info=data.get('info', {}),
                )
                self._send_json({"success": True, "control": ctrl})
            else:
                self._send_json({"error": "Unknown action"}, 400)
        except Exception as e:
            log(f"Story control error: {e}")
            self._send_json({"success": False, "error": str(e)[:200]})

    def _handle_quality_arcs(self, data):
        text = data.get('text', '')
        if not text:
            self._send_json({"error": "No text provided"}, 400)
            return
        try:
            result = quality_system.analyze_chapter_arcs(text)
            self._send_json({"success": True, **result})
        except Exception as e:
            log(f"Quality arcs error: {e}")
            self._send_json({"success": False, "error": str(e)[:200]})

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

        deai_system_prompt = """你是一位拥有15年写作经验的顶级作家，精通将AI生成的文本改写为自然的人类写作风格。

【去AI核心原则 — NWACS 智能去AI痕迹引擎】

=== 内容层：消除AI内容模式 ===
1. 禁止过度强调意义和遗产：删除"作为……的证明""标志着……的里程碑""为……奠定基础"等夸大重要性的表述
2. 禁止宣传广告式语言：删除"坐落于""令人叹为观止的""必游之地""开创性的"等夸张宣传词
3. 禁止以-ing结尾的肤浅分析：删除"突出""强调""彰显""确保""反映""象征"等空洞动词结尾
4. 禁止模糊归因：删除"行业报告显示""观察者指出""专家认为""多个来源"等无具体来源的引用
5. 禁止提纲式挑战与未来展望：删除"尽管面临若干挑战""未来展望""前景一片光明"等公式化段落
6. 禁止通用积极结论：删除"未来看起来光明""向正确方向迈出的重要一步""未来可期"等模糊乐观结尾

=== 语言语法层：消除AI语言特征 ===
7. 禁止过度使用的AI词汇：删除"此外""至关重要""深入探讨""格局""关键性的""织锦""充满活力的""与……保持一致"
8. 恢复系动词"是"：将"作为……充当""代表……标志着""拥有……设有"改回简单的"是""有"
9. 禁止否定式排比：将"不仅……而且""不仅仅是……而是"改为更自然的表达
10. 禁止三段式法则：避免"X、Y和Z"的机械列举，用不规则的列举方式
11. 禁止虚假范围：删除"从……到……的旅程/转变"等伪深度结构
12. 禁止填充短语：删除"值得注意的是""为了实现这一目标""在这个时间点""具有……的能力"

=== 风格层：消除AI风格特征 ===
13. 破折号减半：每段最多使用1个破折号，用句号或逗号替代多余的
14. 禁止协作交流痕迹：删除"希望这对您有帮助""您说得完全正确""请告诉我"等聊天机器人用语
15. 禁止知识截止日期免责声明：删除"截至""根据我最后的训练更新""基于可用信息"等
16. 禁止谄媚/卑躬屈膝的语气：删除"好问题""您的观察非常敏锐""我很高兴您问到这个问题"
17. 禁止过度限定：删除"可以潜在地可能被认为""在一定程度上""在某种意义上"等软弱措辞

=== 填充短语与公式化结构消除 ===
18. 禁止喉清开场：删除"事情是这样的""这么说吧""你听我说""Here's the thing"
19. 禁止强调拐杖：删除"这一点很重要""这很关键""这才是重点""This matters because"
20. 禁止表演式诚实：删除"说实话""老实说""不瞒你说""To be honest"
21. 禁止掌声句：删除"这就是关键所在""这才是真正的力量""That's it. That's the thing."
22. 禁止二元对比结构：避免"不是……而是……""并非……而是……"的机械对比
23. 禁止问答自嗨：避免"为什么？因为……""怎么做？很简单……"的自问自答
24. 禁止通用开场白：删除"在当今……时代""随着……的发展""In today's fast-paced world"
25. 禁止空洞大词：删除"赋能""闭环""底层逻辑""降维打击""颗粒度""对齐""拉通"

=== 五维度质量要求 (50分制) ===
26. 直接性(10分)：直接陈述事实，不绕圈宣告。禁止"作为……的证明""标志着""值得注意的是"
27. 节奏(10分)：句长剧烈变化。短句3-10字，长句25-50字，连续3句不能同长度
28. 信任度(10分)：尊重读者智慧。禁止"也就是说""换句话说""这意味着""顾名思义"
29. 真实性(10分)：听起来像真人说话。禁止"无缝、直观和强大""创新、灵感和洞察"等三段式
30. 精炼度(10分)：删除一切冗余。禁止"在这个时间点""由于……的事实""为了实现这一目标"

=== Burstiness 节奏注入 ===
31. 句子长度必须剧烈变化：B=(σ/μ)×100，目标B>50（爵士乐节奏）
32. 短句(≤10字)占比至少20%，长句(≥30字)占比至少15%
33. 不能连续3句长度差小于3个字——这是AI的节拍器节奏
34. 段落长度也必须变化：不能每段都是3-5句

=== 结构层去AI ===
35. 段落长度不能均匀：有的段落1句话，有的段落8句话
36. 不能每段都是"主题句→论据→结论"的模板结构
37. 前后半部分不能对称——打破平衡

=== 灵魂注入原则 ===
38. 长短句交替：必须有短句(≤10字)和长句(≥30字)交替出现
39. 个人观点表达：加入"我觉得""我在想""让我困扰""不安""兴奋"等主观感受
40. 具体数据细节：加入具体数字、时间、次数、百分比
41. 不完美表达：加入"嗯""呃""那个""就是""妈的""操"等人类口语瑕疵
42. 幽默或锋芒：加入讽刺、自嘲、黑色幽默
43. 用动作替代形容词：不写"他愤怒"，写"他一拳砸在桌上"
44. 加入感官细节：视觉/听觉/触觉/嗅觉至少2种
45. 加入本土生活细节：烟火气、人情世故、市井气息

=== 30秒测试原则 ===
46. 加入具体人名/地名/品牌名——不能全是泛称
47. 加入具体数字和单位——不能全是模糊描述
48. 加入个人语气和情感——不能全是客观陈述
49. 加入独特细节和意外感——不能全是可预测的内容

=== 输出前自检清单 ===
□ 连续三个句子长度是否不同？
□ 段落是否以简洁的单行结尾？
□ 破折号是否≤2处？
□ 是否解释了隐喻或比喻？（应该信任读者）
□ "此外""然而"等连接词是否≤3处？
□ 三段式列举是否≤2处？
□ 是否有具体人名/地名/数字？
□ 是否有个人语气和情感表达？
□ Burstiness是否>30？

【最终铁律】
- 直接输出改写后的文本，不要任何解释、不要前言、不要后记
- 保持原文的核心信息和情节不变
- 如果原文已经是自然的人类写作风格，只做微调，不要过度修改"""

        style_instructions = {
            "polish": "请润色以下文本，使其更加流畅优美，保持原意不变。",
            "simplify": "请简化以下文本，使其更加简洁明了。",
            "expand": "请扩写以下文本，增加细节描写和情感表达。",
            "summarize": "请概括以下文本的主要内容，不超过100字。",
            "formal": "请将以下文本改为正式文体。",
            "casual": "请将以下文本改为口语化表达。",
            "deai": "请将以下AI生成的文本改写为自然的人类写作风格，消除所有AI痕迹。",
        }

        instruction = style_instructions.get(style, style_instructions["deai"])
        prompt = f"{instruction}\n\n原文：\n{text}"

        try:
            rewritten = llm.generate(
                prompt,
                system_prompt=deai_system_prompt,
                params=GenerationParams(temperature=0.85, max_tokens=4096),
            )
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
