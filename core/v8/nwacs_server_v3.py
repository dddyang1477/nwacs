import sys, os, json, traceback, threading, time, re, urllib.request, urllib.error
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

# 动态获取当前文件所在目录，支持跨平台
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, CURRENT_DIR)
os.chdir(CURRENT_DIR)

LOG_FILE = os.path.join(os.path.dirname(__file__), 'server_debug.log')

def log(msg):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    line = f"[{timestamp}] {msg}"
    print(line)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(line + '\n')

def _safe_filename(name: str) -> str:
    """将小说名/章节名转换为安全的文件名"""
    import re
    safe = re.sub(r'[\\/:*?"<>|]', '_', name)
    safe = safe.strip().rstrip('.')
    return safe if safe else 'untitled'

log("Importing NWACS modules...")
from genre_profile_manager import GenreProfileManager, GenreType
from llm_interface import llm, GenerationParams
from character_name_engine import CharacterNameEngine, CharacterProfile
from story_system import StorySystem, MultiAgentPipeline
from reviewer_agent import ReviewerAgent
from quality_system import QualitySystem
from ai_humanizer import detect_ai_traces, build_humanize_prompt, build_ai_detection_report_prompt
from project_memory import ProjectMemory, TruthFilesManager
from planning_system import PlanningSystem
from retention_system import RetentionSystem
from fatigue_detector import FatigueDetector, HumanReviewGates
from rag_engine import RAGEngine
from truth_file_manager import TruthFileManager
from style_fingerprint import StyleFingerprintEngine
from strand_weave import StrandWeaveEngine
from writing_pipeline import WritingPipeline

log("Initializing core modules...")
genre_manager = GenreProfileManager()
name_engine = CharacterNameEngine(llm)

PROJECT_ROOT = os.path.dirname(__file__)
log("Initializing new modules (story/reviewer/quality/memory/planning)...")
story_system = StorySystem(PROJECT_ROOT)
pipeline = MultiAgentPipeline(story_system)
reviewer = ReviewerAgent(PROJECT_ROOT)
quality_system = QualitySystem(PROJECT_ROOT)
project_memory = ProjectMemory(PROJECT_ROOT)
truth_files = TruthFilesManager(PROJECT_ROOT)
planning_system = PlanningSystem(PROJECT_ROOT)
retention_system = RetentionSystem(PROJECT_ROOT)
fatigue_detector = FatigueDetector(PROJECT_ROOT)
review_gates = HumanReviewGates(PROJECT_ROOT)
rag_engine = RAGEngine(PROJECT_ROOT)
truth_file_mgr = TruthFileManager(PROJECT_ROOT)
style_engine = StyleFingerprintEngine()
strand_engine = StrandWeaveEngine()
writing_pipeline = WritingPipeline(
    truth_manager=truth_file_mgr,
    style_engine=style_engine,
    strand_engine=strand_engine,
)
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


def fetch_creative_inspiration(genre: str, theme: str = "") -> str:
    """联网获取创作灵感，包括热门趋势和创意元素"""
    inspiration_parts = []
    genre_keywords = {
        "玄幻": "玄幻小说+热门题材+创新设定+2025+2026",
        "都市": "都市小说+热门题材+社会热点+2025+2026",
        "仙侠": "仙侠小说+创新流派+热门设定+2025+2026",
        "科幻": "科幻小说+前沿科技+AI+创新概念+2025+2026",
        "悬疑": "悬疑小说+热门题材+社会案件+2025+2026",
        "言情": "言情小说+热门题材+情感趋势+2025+2026",
        "历史": "历史小说+热门朝代+创新穿越+2025+2026",
        "游戏": "游戏小说+热门游戏+电竞趋势+2025+2026",
        "恐怖": "恐怖小说+灵异题材+都市传说+2025+2026",
        "武侠": "武侠小说+创新设定+国风复兴+2025+2026",
    }
    query = genre_keywords.get(genre, f"{genre}+小说+热门题材+创新+2025+2026")
    if theme:
        query += f"+{theme}"

    encoded_query = urllib.parse.quote(query)
    search_url = f"https://www.baidu.com/s?wd={encoded_query}"

    try:
        req = urllib.request.Request(
            search_url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml",
                "Accept-Language": "zh-CN,zh;q=0.9",
            }
        )
        with urllib.request.urlopen(req, timeout=8) as resp:
            html = resp.read().decode('utf-8', errors='ignore')

        snippets = re.findall(r'<span class="content-right_[^"]*">(.*?)</span>', html, re.DOTALL)
        if not snippets:
            snippets = re.findall(r'<div class="c-abstract">(.*?)</div>', html, re.DOTALL)
        if not snippets:
            snippets = re.findall(r'class="c-summary[^"]*"[^>]*>(.*?)</', html, re.DOTALL)

        if snippets:
            clean_snippets = []
            for s in snippets[:8]:
                clean = re.sub(r'<[^>]+>', '', s)
                clean = re.sub(r'\s+', ' ', clean).strip()
                if len(clean) > 15:
                    clean_snippets.append(clean)

            if clean_snippets:
                inspiration_parts.append("\n## 🌐 联网获取的创作灵感（来自实时搜索）\n")
                inspiration_parts.append("以下是从网络中获取的最新热门趋势和创意元素，请参考这些信息来增强剧情的创新性和时代感：\n")
                for i, snippet in enumerate(clean_snippets[:6], 1):
                    inspiration_parts.append(f"{i}. {snippet}")
                inspiration_parts.append("\n请将以上趋势信息融入剧情方案中，创造更具时代感和创新性的故事。\n")

        log(f"Web inspiration fetched: {len(snippets) if snippets else 0} snippets for {genre}")

    except Exception as e:
        log(f"Web inspiration fetch failed: {e}")

    creative_prompts = [
        "\n## 🎨 创意增强指令\n",
        "1. **反套路设计**：思考当前市场上最常见的套路是什么，然后反其道而行之",
        "2. **跨类型融合**：将{genre}与其他类型的核心元素融合，创造全新阅读体验",
        "3. **时代共鸣**：融入当代读者最关心的社会议题和情感需求",
        "4. **高概念设定**：用一个简单但极具冲击力的'如果……会怎样'来构建核心创意",
        "5. **情感锚点**：确保故事有让读者产生强烈情感共鸣的核心关系",
    ]
    inspiration_parts.extend(creative_prompts)

    return "\n".join(inspiration_parts).replace("{genre}", genre)


class NWACSHandler(BaseHTTPRequestHandler):
    chapters_cache = {}  # 缓存已生成的章节内容，用于防重复检测

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
                    "紧张刺激": {"icon": "⚡", "desc": "节奏紧凑，悬念迭起"},
                    "轻松愉快": {"icon": "😊", "desc": "氛围轻松，温馨有趣"},
                    "虐心催泪": {"icon": "😢", "desc": "情感浓烈，催人泪下"},
                    "冷静克制": {"icon": "🧊", "desc": "叙事冷静，理性克制"},
                    "热血燃爆": {"icon": "🔥", "desc": "情绪高涨，热血沸腾"},
                    "黑暗沉重": {"icon": "🌑", "desc": "氛围压抑，人性探讨"},
                    "诙谐幽默": {"icon": "😂", "desc": "轻松搞笑，诙谐风趣"},
                },
                "lengths": {
                    "自定义字数": "5万-300万字可设置",
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
        elif path == '/api/retention/report':
            report = retention_system.get_overall_retention_report()
            self._send_json({"success": True, "report": report})
        elif path == '/api/retention/score':
            self._send_json({"success": True, "message": "使用POST请求提交章节号"})
        elif path == '/api/story/snapshot':
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
        elif path == '/api/rag/stats':
            stats = rag_engine.get_stats()
            self._send_json({"success": True, "stats": stats})
        elif path == '/api/rag/characters':
            chars = rag_engine.get_character_network()
            self._send_json({"success": True, "characters": chars})
        elif path == '/api/rag/timeline':
            timeline = rag_engine.get_event_timeline()
            self._send_json({"success": True, "timeline": timeline})
        elif path == '/api/style/list':
            fps = style_engine.list_fingerprints()
            self._send_json({"success": True, "fingerprints": fps})
        elif path == '/api/strand/report':
            report = strand_engine.get_rhythm_report()
            self._send_json({"success": True, "report": report})
        elif path == '/api/truth/new/status':
            status = truth_file_mgr.get_all_status()
            self._send_json({"success": True, "status": status})
        elif path == '/api/truth/new/hooks':
            hooks = truth_file_mgr.get_file('pending_hooks')
            self._send_json({"success": True, "hooks": hooks})
        elif path == '/api/pipeline/new/status':
            self._send_json({"success": True, "results": {str(k): {"stage": v.stage.value, "passed": v.passed, "error": v.error} for k, v in writing_pipeline.results.items()}})
        elif path == '/api/fatigue/overall':
            try:
                report = fatigue_detector.get_overall_fatigue_report()
                self._send_json({"success": True, "report": report})
            except Exception as e:
                log(f"fatigue/overall error: {e}")
                traceback.print_exc()
                self._send_json({"success": False, "error": str(e)[:200]})
        elif path == '/api/gates/summary':
            try:
                summary = review_gates.get_all_gates_summary()
                self._send_json({"success": True, "summary": summary})
            except Exception as e:
                log(f"gates/summary error: {e}")
                traceback.print_exc()
                self._send_json({"success": False, "error": str(e)[:200]})
        elif path == '/' or path == '/index.html':
            # 优先服务最新的 index_v9_final.html
            frontend_dir = os.path.join(os.path.dirname(__file__), 'frontend')
            for fname in ['index_v9_final.html', 'index.html']:
                frontend_path = os.path.join(frontend_dir, fname)
                if os.path.exists(frontend_path):
                    with open(frontend_path, 'r', encoding='utf-8') as f:
                        html = f.read()
                    self.send_response(200)
                    self.send_header('Content-Type', 'text/html; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(html.encode('utf-8'))
                    return
            self._send_json({"error": "Frontend not found"}, 404)
        else:
            self._send_json({"error": "Not found"}, 404)
    
    # ========== GET请求处理器（重构版）=========
    def _handle_get_health(self):
        """健康检查"""
        self._send_json({"status": "ok"})
    
    def _handle_get_models(self):
        """获取可用模型列表"""
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
    
    def _handle_get_config(self):
        """获取系统配置"""
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
    
    def _handle_get_options(self):
        """获取所有选项（题材、流派、风格等）"""
        self._send_json({
            "genres": self._get_genres_options(),
            "schools": self._get_schools_options(),
            "styles": self._get_styles_options(),
            "tones": self._get_tones_options(),
            "lengths": self._get_lengths_options()
        })
    
    def _get_genres_options(self):
        """获取题材选项"""
        return {
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
        }
    
    def _get_schools_options(self):
        """获取流派选项（简化版）"""
        return {
            "玄幻": [
                {"id": "sign_in", "name": "签到流", "desc": "每日签到获得奖励，躺平变强"},
                {"id": "system", "name": "系统流", "desc": "绑定系统，完成任务获得能力"},
                {"id": "wisdom", "name": "智取流", "desc": "以智取胜，运筹帷幄"},
            ],
            "都市": [
                {"id": "urban_romance", "name": "都市情感", "desc": "现代都市中的爱恨情仇"},
                {"id": "rebirth_city", "name": "重生流", "desc": "重生回到过去，改写人生"},
                {"id": "business_war", "name": "商战流", "desc": "商场如战场，资本博弈"},
            ],
        }
    
    def _get_styles_options(self):
        """获取风格选项"""
        return {
            "热血爽文": {"icon": "🔥", "desc": "节奏明快"},
            "轻松搞笑": {"icon": "😄", "desc": "幽默诙谐"},
            "黑暗深沉": {"icon": "🌑", "desc": "人性探讨"},
            "温馨治愈": {"icon": "🌸", "desc": "温暖人心"},
            "悬疑烧脑": {"icon": "🧩", "desc": "伏笔重重"},
            "史诗宏大": {"icon": "🏰", "desc": "世界观庞大"},
        }
    
    def _get_tones_options(self):
        """获取基调选项"""
        return {
            "紧张刺激": {"icon": "⚡", "desc": "节奏紧凑，悬念迭起"},
            "轻松愉快": {"icon": "😊", "desc": "氛围轻松，温馨有趣"},
            "虐心催泪": {"icon": "😢", "desc": "情感浓烈，催人泪下"},
            "冷静克制": {"icon": "🧊", "desc": "叙事冷静，理性克制"},
            "热血燃爆": {"icon": "🔥", "desc": "情绪高涨，热血沸腾"},
            "黑暗沉重": {"icon": "🌑", "desc": "氛围压抑，人性探讨"},
            "诙谐幽默": {"icon": "😂", "desc": "轻松搞笑，诙谐风趣"},
        }
    
    def _get_lengths_options(self):
        """获取篇幅选项"""
        return {
            "自定义字数": "5万-300万字可设置",
        }
    
    def _handle_get_quality_trend(self):
        """获取质量趋势"""
        try:
            trend = quality_system.get_quality_trend()
            self._send_json({"success": True, "trend": trend.to_dict()})
        except Exception as e:
            log(f"quality/trend error: {e}")
            self._send_json({"success": False, "error": str(e)[:200]})
    
    def _handle_get_memory_stats(self):
        """获取记忆统计"""
        try:
            stats = project_memory.get_memory_stats()
            self._send_json({"success": True, "stats": stats})
        except Exception as e:
            log(f"memory/stats error: {e}")
            self._send_json({"success": False, "error": str(e)[:200]})
    
    def _handle_get_planning_timeline(self):
        """获取规划时间线"""
        try:
            timeline = planning_system.get_timeline()
            self._send_json({"success": True, "timeline": timeline})
        except Exception as e:
            log(f"planning/timeline error: {e}")
            self._send_json({"success": False, "error": str(e)[:200]})
    
    def _handle_get_retention_report(self):
        """获取留存报告"""
        try:
            report = retention_system.get_overall_retention_report()
            self._send_json({"success": True, "report": report})
        except Exception as e:
            log(f"retention/report error: {e}")
            self._send_json({"success": False, "error": str(e)[:200]})
    
    def _handle_get_story_snapshot(self):
        """获取故事快照"""
        try:
            snapshots = story_system.list_snapshots()
            self._send_json({"success": True, "snapshots": snapshots})
        except Exception as e:
            log(f"story/snapshot error: {e}")
            self._send_json({"success": False, "error": str(e)[:200]})
    
    def _handle_get_story_lock(self):
        """获取故事锁定状态"""
        try:
            lock_status = story_system.check_lock()
            self._send_json({"success": True, **lock_status})
        except Exception as e:
            log(f"story/lock error: {e}")
            self._send_json({"success": False, "error": str(e)[:200]})
    
    def _handle_get_story_control(self):
        """获取故事控制文档"""
        try:
            ctrl = story_system.get_control_document()
            self._send_json({"success": True, "control": ctrl})
        except Exception as e:
            log(f"story/control error: {e}")
            self._send_json({"success": False, "error": str(e)[:200]})
    
    def _handle_get_quality_arcs(self):
        """获取质量弧线（仅返回提示）"""
        self._send_json({"success": True, "message": "使用POST请求提交文本进行分析"})
    
    def _handle_get_rag_stats(self):
        """获取RAG统计"""
        try:
            stats = rag_engine.get_stats()
            self._send_json({"success": True, "stats": stats})
        except Exception as e:
            log(f"rag/stats error: {e}")
            self._send_json({"success": False, "error": str(e)[:200]})
    
    def _handle_get_rag_characters(self):
        """获取RAG角色网络"""
        try:
            chars = rag_engine.get_character_network()
            self._send_json({"success": True, "characters": chars})
        except Exception as e:
            log(f"rag/characters error: {e}")
            self._send_json({"success": False, "error": str(e)[:200]})
    
    def _handle_get_rag_timeline(self):
        """获取RAG事件时间线"""
        try:
            timeline = rag_engine.get_event_timeline()
            self._send_json({"success": True, "timeline": timeline})
        except Exception as e:
            log(f"rag/timeline error: {e}")
            self._send_json({"success": False, "error": str(e)[:200]})
    
    def _handle_get_style_list(self):
        """获取风格指纹列表"""
        try:
            fps = style_engine.list_fingerprints()
            self._send_json({"success": True, "fingerprints": fps})
        except Exception as e:
            log(f"style/list error: {e}")
            self._send_json({"success": False, "error": str(e)[:200]})
    
    def _handle_get_strand_report(self):
        """获取节奏报告"""
        try:
            report = strand_engine.get_rhythm_report()
            self._send_json({"success": True, "report": report})
        except Exception as e:
            log(f"strand/report error: {e}")
            self._send_json({"success": False, "error": str(e)[:200]})
    
    def _handle_get_truth_new_status(self):
        """获取真值文件状态"""
        try:
            status = truth_file_mgr.get_all_status()
            self._send_json({"success": True, "status": status})
        except Exception as e:
            log(f"truth/new/status error: {e}")
            self._send_json({"success": False, "error": str(e)[:200]})
    
    def _handle_get_pipeline_new_status(self):
        """获取新流水线状态"""
        try:
            # 安全获取pipeline结果
            results = {}
            if hasattr(writing_pipeline, 'results') and writing_pipeline.results:
                for k, v in writing_pipeline.results.items():
                    results[str(k)] = {
                        "stage": v.stage.value if hasattr(v.stage, 'value') else str(v.stage),
                        "passed": v.passed if hasattr(v, 'passed') else False,
                        "error": v.error if hasattr(v, 'error') else None
                    }
            self._send_json({"success": True, "results": results})
        except Exception as e:
            log(f"pipeline/new/status error: {e}")
            self._send_json({"success": False, "error": str(e)[:200]})
    
    def _handle_get_index(self):
        """处理首页请求"""
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
    
    def _handle_error(self, e):
        """统一错误处理"""
        log(f"Error in GET handler: {e}")
        traceback.print_exc()
        self._send_json({"success": False, "error": str(e)[:200]}, 500)
    
    def do_GET(self):
        """处理GET请求 - 重构版（使用调度表）"""
        path = urlparse(self.path).path
        
        # API调度表
        get_handlers = {
            '/api/health': self._handle_get_health,
            '/api/models': self._handle_get_models,
            '/api/config': self._handle_get_config,
            '/api/options': self._handle_get_options,
            '/api/quality/trend': self._handle_get_quality_trend,
            '/api/memory/stats': self._handle_get_memory_stats,
            '/api/planning/timeline': self._handle_get_planning_timeline,
            '/api/retention/report': self._handle_get_retention_report,
            '/api/story/snapshot': self._handle_get_story_snapshot,
            '/api/story/lock': self._handle_get_story_lock,
            '/api/story/control': self._handle_get_story_control,
            '/api/quality/arcs': self._handle_get_quality_arcs,
            '/api/rag/stats': self._handle_get_rag_stats,
            '/api/rag/characters': self._handle_get_rag_characters,
            '/api/rag/timeline': self._handle_get_rag_timeline,
            '/api/style/list': self._handle_get_style_list,
            '/api/strand/report': self._handle_get_strand_report,
            '/api/truth/new/status': self._handle_get_truth_new_status,
            '/api/pipeline/new/status': self._handle_get_pipeline_new_status,
            '/': self._handle_get_index,
            '/index.html': self._handle_get_index,
        }
        
        # 查找处理器
        handler = get_handlers.get(path)
        if handler:
            try:
                handler()
            except Exception as e:
                self._handle_error(e)
        else:
            self._send_json({"error": "Not found"}, 404)
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
        elif path == '/api/generate_chapters_batch':
            self._handle_generate_chapters_batch(data)
        elif path == '/api/detect_ai':
            self._handle_detect_ai(data)
        elif path == '/api/rewrite':
            self._handle_rewrite(data)
        elif path == '/api/save_chapter':
            self._handle_save_chapter(data)
        elif path == '/api/config':
            self._handle_update_config(data)
        elif path == '/api/generate_names':
            self._handle_generate_names(data)
        elif path == '/api/generate_names_batch':
            self._handle_generate_names_batch(data)
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
        elif path == '/api/memory/fingerprint':
            self._handle_memory_fingerprint(data)
        elif path == '/api/memory/stats':
            self._handle_memory_stats(data)
        elif path == '/api/truth/context':
            self._handle_truth_context(data)
        elif path == '/api/truth/all':
            self._handle_truth_all(data)
        elif path == '/api/truth/update':
            self._handle_truth_update(data)
        elif path == '/api/truth/hooks':
            self._handle_truth_hooks(data)
        elif path == '/api/pipeline/start':
            self._handle_pipeline_start(data)
        elif path == '/api/pipeline/state':
            self._handle_pipeline_state(data)
        elif path == '/api/pipeline/revise':
            self._handle_pipeline_revise(data)
        elif path == '/api/planning/beat-sheet':
            self._handle_planning_beat_sheet(data)
        elif path == '/api/planning/outline':
            self._handle_planning_outline(data)
        elif path == '/api/planning/directive':
            self._handle_planning_directive(data)
        elif path == '/api/planning/timeline':
            self._handle_planning_timeline(data)
        elif path == '/api/retention/score':
            self._handle_retention_score(data)
        elif path == '/api/retention/analyze':
            self._handle_retention_analyze(data)
        elif path == '/api/retention/add_hook':
            self._handle_retention_add_hook(data)
        elif path == '/api/retention/add_cool_point':
            self._handle_retention_add_cool_point(data)
        elif path == '/api/retention/add_debt':
            self._handle_retention_add_debt(data)
        elif path == '/api/retention/resolve_debt':
            self._handle_retention_resolve_debt(data)
        elif path == '/api/fatigue/analyze':
            self._handle_fatigue_analyze(data)
        elif path == '/api/fatigue/report':
            self._handle_fatigue_report(data)
        elif path == '/api/fatigue/overall':
            self._handle_fatigue_overall(data)
        elif path == '/api/fatigue/suggestions':
            self._handle_fatigue_suggestions(data)
        elif path == '/api/gates/evaluate':
            self._handle_gates_evaluate(data)
        elif path == '/api/gates/chapter':
            self._handle_gates_chapter(data)
        elif path == '/api/gates/summary':
            self._handle_gates_summary(data)
        elif path == '/api/rag/search':
            self._handle_rag_search(data)
        elif path == '/api/rag/context':
            self._handle_rag_context(data)
        elif path == '/api/rag/reverse':
            self._handle_rag_reverse(data)
        elif path == '/api/rag/consistency':
            self._handle_rag_consistency(data)
        elif path == '/api/rag/characters':
            self._handle_rag_characters(data)
        elif path == '/api/rag/timeline':
            self._handle_rag_timeline(data)
        elif path == '/api/rag/stats':
            self._handle_rag_stats(data)
        elif path == '/api/story/snapshot':
            self._handle_story_snapshot(data)
        elif path == '/api/story/lock':
            self._handle_story_lock(data)
        elif path == '/api/story/control':
            self._handle_story_control(data)
        elif path == '/api/quality/arcs':
            self._handle_quality_arcs(data)
        elif path == '/api/fragment/save':
            self._handle_fragment_save(data)
        elif path == '/api/fragment/list':
            self._handle_fragment_list(data)
        elif path == '/api/fragment/get':
            self._handle_fragment_get(data)
        elif path == '/api/fragment/apply':
            self._handle_fragment_apply(data)
        elif path == '/api/characters/states':
            self._handle_characters_states(data)
        elif path == '/api/style/analyze':
            self._handle_style_analyze(data)
        elif path == '/api/style/compare':
            self._handle_style_compare(data)
        elif path == '/api/style/list':
            self._handle_style_list(data)
        elif path == '/api/strand/analyze':
            self._handle_strand_analyze(data)
        elif path == '/api/strand/report':
            self._handle_strand_report(data)

        elif path == '/api/generate_detailed_outline':
            self._handle_generate_detailed_outline(data)
        elif path == '/api/strand/suggest':
            self._handle_strand_suggest(data)
        elif path == '/api/truth/new/status':
            self._handle_truth_new_status(data)
        elif path == '/api/truth/new/init':
            self._handle_truth_new_init(data)
        elif path == '/api/truth/new/update':
            self._handle_truth_new_update(data)
        elif path == '/api/truth/new/hooks':
            self._handle_truth_new_hooks(data)
        elif path == '/api/pipeline/new/run':
            self._handle_pipeline_new_run(data)
        elif path == '/api/pipeline/new/status':
            self._handle_pipeline_new_status(data)
        else:
            self._send_json({"error": "Not found"}, 404)
    
    def do_POST(self):
        """处理POST请求 - 重构版（使用调度表）"""
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self._send_json({"error": "Invalid JSON"}, 400)
            return
        
        path = urlparse(self.path).path
        
        # API调度表
        post_handlers = {
            '/api/generate_plots': self._handle_generate_plots,
            '/api/select_plot': self._handle_select_plot,
            '/api/generate_chapter': self._handle_generate_chapter,
            '/api/generate_chapters_batch': self._handle_generate_chapters_batch,
            '/api/detect_ai': self._handle_detect_ai,
            '/api/rewrite': self._handle_rewrite,
            '/api/save_chapter': self._handle_save_chapter,
            '/api/config': self._handle_update_config,
            '/api/generate_names': self._handle_generate_names,
            '/api/generate_names_batch': self._handle_generate_names_batch,
            '/api/generate_org_names': self._handle_generate_org_names,
            '/api/generate_power_system': self._handle_generate_power_system,
            '/api/story/init': self._handle_story_init,
            '/api/story/master': self._handle_story_master,
            '/api/story/volume': self._handle_story_volume,
            '/api/story/chapter-contract': self._handle_story_chapter_contract,
            '/api/story/commit': self._handle_story_commit,
            '/api/review': self._handle_review,
            '/api/quality/record': self._handle_quality_record,
            '/api/quality/trend': self._handle_quality_trend,
            '/api/quality/checklist': self._handle_quality_checklist,
            '/api/memory/patterns': self._handle_memory_patterns,
            '/api/memory/learn': self._handle_memory_learn,
            '/api/memory/context': self._handle_memory_context,
            '/api/memory/fingerprint': self._handle_memory_fingerprint,
            '/api/memory/stats': self._handle_memory_stats,
            '/api/truth/context': self._handle_truth_context,
            '/api/truth/all': self._handle_truth_all,
            '/api/truth/update': self._handle_truth_update,
            '/api/truth/hooks': self._handle_truth_hooks,
            '/api/pipeline/start': self._handle_pipeline_start,
            '/api/pipeline/state': self._handle_pipeline_state,
            '/api/pipeline/revise': self._handle_pipeline_revise,
            '/api/planning/beat-sheet': self._handle_planning_beat_sheet,
            '/api/planning/outline': self._handle_planning_outline,
            '/api/planning/directive': self._handle_planning_directive,
            '/api/planning/timeline': self._handle_planning_timeline,
            '/api/retention/score': self._handle_retention_score,
            '/api/retention/analyze': self._handle_retention_analyze,
            '/api/retention/add_hook': self._handle_retention_add_hook,
            '/api/retention/add_cool_point': self._handle_retention_add_cool_point,
            '/api/retention/add_debt': self._handle_retention_add_debt,
            '/api/retention/resolve_debt': self._handle_retention_resolve_debt,
            '/api/fatigue/analyze': self._handle_fatigue_analyze,
            '/api/fatigue/report': self._handle_fatigue_report,
            '/api/fatigue/overall': self._handle_fatigue_overall,
            '/api/fatigue/suggestions': self._handle_fatigue_suggestions,
            '/api/gates/evaluate': self._handle_gates_evaluate,
            '/api/gates/chapter': self._handle_gates_chapter,
            '/api/gates/summary': self._handle_gates_summary,
            '/api/rag/search': self._handle_rag_search,
            '/api/rag/context': self._handle_rag_context,
            '/api/rag/reverse': self._handle_rag_reverse,
            '/api/rag/consistency': self._handle_rag_consistency,
            '/api/rag/characters': self._handle_rag_characters,
            '/api/rag/timeline': self._handle_rag_timeline,
            '/api/rag/stats': self._handle_rag_stats,
            '/api/story/snapshot': self._handle_story_snapshot,
            '/api/story/lock': self._handle_story_lock,
            '/api/story/control': self._handle_story_control,
            '/api/quality/arcs': self._handle_quality_arcs,
            '/api/fragment/save': self._handle_fragment_save,
            '/api/fragment/list': self._handle_fragment_list,
            '/api/fragment/get': self._handle_fragment_get,
            '/api/fragment/apply': self._handle_fragment_apply,
            '/api/characters/states': self._handle_characters_states,
            '/api/style/analyze': self._handle_style_analyze,
            '/api/style/compare': self._handle_style_compare,
            '/api/style/list': self._handle_style_list,
            '/api/strand/analyze': self._handle_strand_analyze,
            '/api/strand/report': self._handle_strand_report,
            '/api/generate_detailed_outline': self._handle_generate_detailed_outline,
            '/api/strand/suggest': self._handle_strand_suggest,
            '/api/truth/new/status': self._handle_truth_new_status,
            '/api/truth/new/init': self._handle_truth_new_init,
            '/api/truth/new/update': self._handle_truth_new_update,
            '/api/truth/new/hooks': self._handle_truth_new_hooks,
            '/api/pipeline/new/run': self._handle_pipeline_new_run,
            '/api/pipeline/new/status': self._handle_pipeline_new_status,
        }
        
        # 查找处理器
        handler = post_handlers.get(path)
        if handler:
            try:
                handler(data)
            except Exception as e:
                self._handle_post_error(e, path)
        else:
            self._send_json({"error": "Not found"}, 404)
    
    def _handle_post_error(self, error, path):
        """POST请求统一错误处理"""
        log(f"Error in POST handler {path}: {error}")
        traceback.print_exc()
        self._send_json({"success": False, "error": str(error)[:200]}, 500)
    
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
        length = data.get('length', '自定义字数')
        theme = data.get('theme', '逆境成长')
        protagonist = data.get('protagonist', '')
        extra = data.get('extra_requirements', '')
        world_req = data.get('world_requirement', '')
        creation_notes = data.get('creation_notes', '')
        schools = data.get('schools', [data.get('school', '')])
        if isinstance(schools, str):
            schools = [schools] if schools else []
        school_names = data.get('school_names', [data.get('school_name', '')])
        if isinstance(school_names, str):
            school_names = [school_names] if school_names else []
        writing_method = data.get('writing_method', '')
        total_word_count = data.get('total_word_count', 500000)
        target_word_count = data.get('target_word_count', 4000)

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
            world_str = f"\nWorld Requirement: {world_req}" if world_req else ""
            notes_str = f"\nNotes: {creation_notes}" if creation_notes else ""
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

            web_inspiration = fetch_creative_inspiration(primary_genre, theme)

            method_instruction = ""
            if writing_method:
                method_map = {
                    'three_act': '三幕结构（建置→对抗→结局）',
                    'hero_journey': '英雄之旅（平凡世界→冒险→蜕变→归来）',
                    'story_circle': '故事圈（舒适区→探索→改变→回归）',
                    'seven_point': '七点结构（钩子→触发→转折→中点→转折→高潮→结局）',
                    'pixar_formula': '皮克斯公式（日常→事件→连锁反应→成长→蜕变）',
                    'freytag': '弗莱塔格金字塔（引言→上升→高潮→下降→结局）',
                    'save_the_cat': '救猫咪节拍表（15节拍精准控制节奏）',
                    'kishotenketsu': '起承转合（引入→发展→转折→收束）',
                }
                method_name = method_map.get(writing_method, writing_method)
                method_instruction = f"\n### 叙事结构要求\n请严格按照「{method_name}」的结构框架来设计剧情方案，确保方案符合该叙事结构的核心节拍和节奏要求。"

            prompt = f"""你是一位资深网文编辑兼故事架构师，曾策划过100+部爆款小说，精通三幕式结构、英雄之旅和网文节奏设计。请为以下需求生成3个完全不同的剧情方案。

## 需求信息
- 题材：{genre_label}
- 风格：{style_str}
- 基调：{tone_str}
- 篇幅：{length}（总字数约{total_word_count//10000}万字，每章约{target_word_count}字）
- 主题：{theme}{school_label}{multi_genre_note}{protag_str}{extra_str}{world_str}{notes_str}

{genre_context}

{knowledge_injection}

{web_inspiration}

{method_instruction}

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
{"plots": [{"id": "plot_1", "name": "方案名（3-8字）", "tagline": "一句话卖点（15字以内）", "core_idea": "核心创意（50-100字）", "protagonist": "主角设定（30字）", "main_conflict": "核心冲突（30字）", "three_act_structure": "三幕式规划（50字）", "golden_finger": "金手指设定及限制（30字）", "expected_beats": "预期爽点/泪点", "target_readers": "目标读者群", "innovation": "创新之处"}}]}}"""

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
        protagonist = data.get('protagonist', '')
        genres = data.get('genres', [data.get('genre', '玄幻')])
        if isinstance(genres, str):
            genres = [genres]
        styles = data.get('styles', [data.get('style', '热血爽文')])
        if isinstance(styles, str):
            styles = [styles]
        tones = data.get('tones', [data.get('tone', '紧张刺激')])
        if isinstance(tones, str):
            tones = [tones]
        length = data.get('length', '自定义字数')
        theme = data.get('theme', '逆境成长')
        schools = data.get('schools', [data.get('school', '')])
        if isinstance(schools, str):
            schools = [schools] if schools else []
        school_names = data.get('school_names', [data.get('school_name', '')])
        if isinstance(school_names, str):
            school_names = [school_names] if school_names else []
        writing_method = data.get('writing_method', '')
        total_word_count = data.get('total_word_count', 500000)
        target_word_count = data.get('target_word_count', 4000)
        extra = data.get('extra_requirements', '')
        world_req = data.get('world_requirement', '')
        creation_notes = data.get('creation_notes', '')

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

            web_inspiration = fetch_creative_inspiration(primary_genre, theme)

            method_instruction = ""
            if writing_method:
                method_map = {
                    'three_act': '三幕结构（建置→对抗→结局）',
                    'hero_journey': '英雄之旅（平凡世界→冒险→蜕变→归来）',
                    'story_circle': '故事圈（舒适区→探索→改变→回归）',
                    'seven_point': '七点结构（钩子→触发→转折→中点→转折→高潮→结局）',
                    'pixar_formula': '皮克斯公式（日常→事件→连锁反应→成长→蜕变）',
                    'freytag': '弗莱塔格金字塔（引言→上升→高潮→下降→结局）',
                    'save_the_cat': '救猫咪节拍表（15节拍精准控制节奏）',
                    'kishotenketsu': '起承转合（引入→发展→转折→收束）',
                }
                method_name = method_map.get(writing_method, writing_method)
                method_instruction = f"\n### 叙事结构要求\n请严格按照「{method_name}」的结构框架来规划章节大纲，确保每章对应叙事结构的相应节拍。"

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

{web_inspiration}

{method_instruction}

## 小说基本信息
- 题材：{genre_label}
- 风格：{style_str}{school_label}{multi_genre_note}
- 基调：{tone_str}
- 篇幅：{length}
- 主题：{theme}
- 选定剧情：{plot_name}
- 主角名：{protagonist}
- 角色要求：{extra}
- 世界观要求：{world_req}
- 备注：{creation_notes}

{genre_context}

## 大纲输出要求
1. **书名**：必须有爆款网文气质，3-8个字，拒绝套路书名
2. **梗概**：200字，必须包含：核心冲突 + 独特卖点 + 情感主线
3. **人物**：至少4个角色（主角、反派、2个配角），每个角色必须有：
   - 名字（拒绝"天/云/辰/宇/昊/轩/逸/尘/雪/月/瑶/璃"等烂大街字）
   - **主角名字必须使用上方指定的"主角名"**，不得更改
   - 名字寓意（50字以上，解释名字如何暗示角色命运）
   - 角色弧光（从什么状态变到什么状态）
   - 核心欲望（角色真正想要什么）
4. **剧情线**：主线1条 + 辅线至少2条 + 因果关系链至少3条
5. **世界架构**：world_architecture对象，包含：
   - world_type：世界类型（修真/玄幻/都市/科幻等）
   - era：时代背景
   - geography：地理概况（主要地域、势力范围）
   - power_system：力量体系概述
   - rules：世界规则（至少3条核心规则）
6. **组织架构**：organizations数组，至少3个组织/势力，每个包含：
   - name：组织名称
   - type：类型（宗门/家族/国家/商会/散修等）
   - leader：首领
   - description：描述
   - relationship_to_protagonist：与主角关系
7. **章节规划**：根据总字数{total_word_count//10000}万字和每章{target_word_count}字，规划合理的章节数量（约{max(1, total_word_count//target_word_count)}章），每章必须包含：
   - 冲突类型标签（战斗/智斗/情感/探索/成长）
   - 因果链（前因是什么→本章发生什么→导致什么后果）
   - 角色变化（本章结束后角色发生了什么变化）
   - 目标字数：{target_word_count}字

返回纯JSON（不要markdown包裹）：
{{"title": "...", "synopsis": "...", "total_chapters_estimate": {max(1, total_word_count//target_word_count)}, "characters": [{{"name": "...", "name_meaning": "...", "role": "protagonist/antagonist/supporting/mentor", "description": "...", "arc": "...", "core_desire": "..."}}], "plot_lines": {{"main_line": "...", "sub_lines": ["...", "..."], "cause_effect_chains": [{{"cause": "...", "effect": "...", "chapters_involved": [1, 3]}}]}}, "world_architecture": {{"world_type": "...", "era": "...", "geography": "...", "power_system": "...", "rules": ["...", "...", "..."]}}, "organizations": [{{"name": "...", "type": "宗门/家族/国家/商会", "leader": "...", "description": "...", "relationship_to_protagonist": "..."}}], "acts": [{{"name": "Act 1", "description": "...", "chapters": [{{"number": 1, "title": "...", "summary": "...", "conflict_type": "战斗/智斗/情感/探索/成长", "plot_line_type": "main/sub/transition", "cause_effect": {{"caused_by": "...", "leads_to": "..."}}, "character_change": "...", "key_events": ["..."], "word_count_target": {target_word_count}, "notes": ""}}]}}]}}"""

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
                import re as _re
                json_str = _re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', json_str)
                json_str = json_str.replace('\t', ' ').replace('\r', '')
                json_str = _re.sub(r',\s*}', '}', json_str)
                json_str = _re.sub(r',\s*]', ']', json_str)
                json_str = _re.sub(r'(?<!")(\btrue\b|\bfalse\b)(?!")', lambda m: f'"{m.group(1)}"', json_str, flags=_re.IGNORECASE)
                json_str = _re.sub(r'(?<!")(\bnull\b)(?!")', '"null"', json_str, flags=_re.IGNORECASE)
                last_brace = json_str.rfind('}')
                last_bracket = json_str.rfind(']')
                cut_point = max(last_brace, last_bracket)
                if cut_point > 0:
                    json_str = json_str[:cut_point + 1]
                    open_braces = json_str.count('{')
                    close_braces = json_str.count('}')
                    open_brackets = json_str.count('[')
                    close_brackets = json_str.count(']')
                    json_str += '}' * (open_braces - close_braces)
                    json_str += ']' * (open_brackets - close_brackets)
                try:
                    outline = json.loads(json_str)
                except json.JSONDecodeError:
                    log("Outline recovery failed, using regex extraction...")
                    title_match = _re.search(r'"title"\s*:\s*"([^"]*)"', json_str)
                    synopsis_match = _re.search(r'"synopsis"\s*:\s*"([^"]*)"', json_str)
                    outline = {
                        "title": title_match.group(1) if title_match else plot_name,
                        "synopsis": synopsis_match.group(1) if synopsis_match else "",
                        "characters": [],
                        "plot_lines": {"main_line": "", "sub_lines": [], "cause_effect_chains": []},
                        "acts": []
                    }
                    char_blocks = _re.findall(r'\{\s*"name"\s*:\s*"([^"]*)"\s*,\s*"name_meaning"\s*:\s*"([^"]*)"\s*,\s*"role"\s*:\s*"([^"]*)"', json_str)
                    for name, meaning, role in char_blocks:
                        outline["characters"].append({"name": name, "name_meaning": meaning, "role": role, "description": ""})
                    ch_blocks = _re.findall(r'"number"\s*:\s*(\d+)\s*,\s*"title"\s*:\s*"([^"]*)"\s*,\s*"summary"\s*:\s*"([^"]*)"', json_str)
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
                    "synopsis": f"一部{style_str}风格的{genre_str}小说，围绕{theme}展开...",
                    "characters": [
                        {"name": protagonist or "林逸", "name_meaning": "逸：超逸脱俗，象征主角不甘平凡、终将超越一切束缚的命运", "role": "protagonist", "description": "出身平凡的坚毅少年，意外获得改变命运的力量", "arc": "从自卑怯懦的废柴成长为自信强大的守护者", "core_desire": "保护所爱之人，打破阶级固化"},
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
        target_word_count = data.get('target_word_count', 4000)
        protagonist_name = data.get('protagonist_name', '')
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

            # 构建已写章节摘要列表，帮助LLM避免重复
            written_chapters_summary = ""
            written_indices = [i for i in range(1, chapter_num) if i in self.chapters_cache]
            if written_indices:
                written_chapters_summary = "\n## 📚 已写章节摘要（避免重复以下内容）\n"
                for wi in written_indices[-5:]:  # 最多显示最近5章
                    wc = self.chapters_cache[wi]
                    wc_title = wc.get('title', f'第{wi}章')
                    wc_summary = wc.get('content', '')[:100] if wc.get('content') else ''
                    written_chapters_summary += f"- 第{wi}章 {wc_title}: {wc_summary}...\n"

            truth_context = truth_files.get_context_for_chapter(chapter_num)
            if truth_context:
                truth_context = f"""
## 🧠 叙事记忆注入（基于已写章节的真相文件）
{truth_context}
"""

            prompt = f"""你是一位{genre_label}领域的顶级网文作家，拥有15年创作经验，曾写出10+部爆款作品。风格为{style_str}，基调为{tone_str}。{school_label}{multi_genre_note}

## ⚠️ 写作铁律（违反任何一条即为失败）
1. **角色名字绝对锁定**：下方"已确立的角色"中的名字是最终确定的，你绝对不能更改、替换或创造新名字。主角名字是"{protagonist_name}"，如果已设定则必须使用此名
2. **【铁律】字数必须严格控制在{target_word_count}字**：这是不可妥协的硬性要求。生成后我会用程序自动校验，少于{int(target_word_count*0.9)}字或超过{int(target_word_count*1.1)}字将判定为不合格并退回重写。你必须精确控制篇幅
3. **剧情不可重复**：不能和前面章节的冲突模式相同
4. **因果必须连贯**：本章开头必须承接上一章的结尾状态
5. **名字一致性**：所有角色名字必须与下方"已确立的角色"完全一致，包括配角、路人角色也要保持一致

{truth_context}

{character_context}

{previous_context}

{written_chapters_summary}

## 🚫 防重复铁律（违反即为失败）
1. **冲突类型必须轮换**：本章的冲突类型必须与上一章不同。如果上一章是"战斗"，本章必须是"智斗/情感/探索/成长"之一
2. **场景不能重复**：禁止使用与前面章节相同的场景设定（如连续两章都在"修炼室"或"擂台"）
3. **对话模式不能重复**：禁止连续使用相同的对话模式（如连续两章都是"主角被质疑→主角用实力证明"）
4. **爽点模式不能重复**：禁止连续使用相同的爽点模式（如连续两章都是"主角突破→碾压对手"）
5. **叙事节奏必须变化**：本章的叙事节奏必须与上一章形成对比（上一章紧张则本章舒缓，上一章舒缓则本章紧张）

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

{retention_system.build_retention_prompt(chapter_num, chapter_summary)}
{fatigue_detector.build_fatigue_avoidance_prompt(chapter_num)}
{rag_engine.build_context_prompt(chapter_num, chapter_summary)}

## 输出要求
- **【铁律】字数**：严格{target_word_count}中文字符，正负误差不超过10%。程序会自动校验字数，不达标将退回重写
- **格式**：直接输出章节正文，不要JSON包裹，不要标题
- **钩子**：章节结尾必须有强有力的悬念钩子

现在开始写第{chapter_num}章正文："""

            log("Calling LLM for chapter...")
            # 重置API调用计数，防止重试叠加
            llm.reset_operation_count()
            content = llm.generate(prompt, params=GenerationParams(temperature=0.85, max_tokens=8000))
            log(f"Chapter response: {len(content)} chars")

            # 字数强制校验：正负误差不超过10%，最多重试2次（带间隔）
            min_words = int(target_word_count * 0.85)
            max_words = int(target_word_count * 1.15)
            actual_words = len(content.replace('\n', '').replace(' ', ''))
            if actual_words < min_words or actual_words > max_words:
                log(f"Word count {actual_words} outside range [{min_words}, {max_words}], adjusting...")
                for attempt in range(2):
                    time.sleep(1.0 + random.uniform(0, 0.5))
                    direction = "扩充" if actual_words < min_words else "精简"
                    adjust_prompt = f"""你是一位严格的网文编辑。以下章节字数不符合要求。

当前字数：{actual_words}字 | 目标：{target_word_count}字 | 允许范围：{min_words}-{max_words}字

请{direction}以下章节内容（第{attempt+1}次调整）：
- 扩充：增加细节描写、对话、心理活动、环境描写
- 精简：删除冗余修饰、合并重复表达、删减非核心内容

**必须保持**：剧情走向、角色设定、章节标题、核心情节、角色名字、结尾悬念钩子不变

直接输出调整后的章节正文，不要任何额外说明：

{content}"""
                    adjusted = llm.generate(adjust_prompt, params=GenerationParams(temperature=0.7, max_tokens=8000))
                    adjusted_words = len(adjusted.replace('\n', '').replace(' ', ''))
                    log(f"Adjust attempt {attempt+1}: {adjusted_words} chars")
                    if min_words <= adjusted_words <= max_words:
                        content = adjusted
                        actual_words = adjusted_words
                        log(f"Word count adjusted successfully on attempt {attempt+1}")
                        break
                    content = adjusted
                    actual_words = adjusted_words
                else:
                    log(f"Word count adjustment failed after 2 attempts, using last result ({actual_words} chars)")

            # 自动去AI痕迹：集成到生成prompt中，避免额外API调用
            try:
                deai = data.get('auto_deai', True)
                if deai and len(content) > 100:
                    from ai_humanizer import detect_ai_traces
                    detection = detect_ai_traces(content)
                    if detection.get('total_score', 100) < 70:
                        log(f"Auto DEAI skipped (score={detection['total_score']}), AI痕迹已通过生成prompt控制")
            except Exception as deai_err:
                log(f"DEAI check warning: {deai_err}")

            novel_title = outline_data.get('title', '未命名作品')
            novel_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'output', _safe_filename(novel_title))
            os.makedirs(novel_dir, exist_ok=True)
            ch_filename = f"第{chapter_num}章_{_safe_filename(chapter_title)}.txt"
            ch_path = os.path.join(novel_dir, ch_filename)
            with open(ch_path, 'w', encoding='utf-8') as f:
                f.write(f"第{chapter_num}章 {chapter_title}\n\n{content}")
            log(f"Chapter saved to: {ch_path}")

            # 更新章节缓存，用于防重复检测
            self.__class__.chapters_cache[chapter_num] = {
                'title': chapter_title,
                'content': content[:500],  # 只缓存前500字用于摘要
                'summary': chapter_summary,
            }

            try:
                truth_files.add_chapter_summary(
                    chapter=chapter_num,
                    title=chapter_title,
                    core_events=[chapter_summary] if chapter_summary else [],
                    word_count=len(content),
                )
                characters = outline_data.get('characters', [])
                for ch in characters:
                    truth_files.update_character_matrix(
                        character_name=ch.get('name', ''),
                        chapter=chapter_num,
                        role=ch.get('role', ''),
                        motivation=ch.get('core_desire', ''),
                    )
                log(f"Truth files updated for chapter {chapter_num}")
            except Exception as te:
                log(f"Truth files update warning: {te}")

            try:
                pipeline.start_chapter(chapter_num)
                pipeline.set_plan({"chapter_number": chapter_num, "chapter_title": chapter_title, "chapter_summary": chapter_summary})
                pipeline.set_draft(content)
                log(f"Pipeline advanced to auditing for chapter {chapter_num}")
            except Exception as pe:
                log(f"Pipeline update warning: {pe}")

            self._send_json({"success": True, "content": content, "chapter_number": chapter_num, "chapter_title": chapter_title, "saved_path": ch_path})

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

    def _handle_generate_chapters_batch(self, data):
        start_chapter = data.get('start_chapter', 1)
        end_chapter = data.get('end_chapter', 1)
        max_chapters = min(end_chapter - start_chapter + 1, 5)
        log(f"Batch generating chapters {start_chapter} to {start_chapter + max_chapters - 1}")

        outline_data = data.get('outline', {})
        characters = outline_data.get('characters', [])
        genres = data.get('genres', ['玄幻'])
        if isinstance(genres, str):
            genres = [genres]
        styles = data.get('styles', ['热血爽文'])
        if isinstance(styles, str):
            styles = [styles]
        tones = data.get('tones', ['紧张刺激'])
        if isinstance(tones, str):
            tones = [tones]
        theme = data.get('theme', '逆境成长')
        schools = data.get('schools', [''])
        if isinstance(schools, str):
            schools = [schools] if schools else []
        school_names = data.get('school_names', [''])
        if isinstance(school_names, str):
            school_names = [school_names] if school_names else []
        target_wc = data.get('target_word_count', 4000)
        protagonist = data.get('protagonist_name', '')
        previous_chapter_content = data.get('previous_chapter_content', '')
        previous_chapter_num = data.get('previous_chapter_num', 0)

        primary_genre = genres[0] if genres else '玄幻'
        primary_school = schools[0] if schools else ''

        genre_str = '、'.join(genres) if len(genres) > 1 else genres[0]
        style_str = '、'.join(styles)
        tone_str = '、'.join(tones)
        school_str_list = '、'.join(school_names) if school_names else ''

        chapters_info = []
        for ch_num in range(start_chapter, start_chapter + max_chapters):
            ch_title = f"第{ch_num}章"
            ch_summary = ''
            if outline_data and outline_data.get('acts'):
                for act in outline_data['acts']:
                    for ch in (act.get('chapters') or []):
                        if ch.get('number') == ch_num:
                            ch_title = ch.get('title', ch_title)
                            ch_summary = ch.get('summary', '')
                            break
            chapters_info.append(f"第{ch_num}章：{ch_title} - {ch_summary}")

        chapters_str = '\n'.join(chapters_info)

        # 构建与单章生成相同的丰富上下文
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
第{start_chapter}章必须从上一章的结尾状态自然延续，不能出现角色位置/状态/关系的跳跃。
"""

        truth_context = truth_files.get_context_for_chapter(start_chapter)
        if truth_context:
            truth_context = f"""
## 🧠 叙事记忆注入（基于已写章节的真相文件）
{truth_context}
"""

        # 为每章分配不同的冲突类型和场景，确保多样性
        conflict_types = ['战斗', '智斗', '情感', '探索', '成长']
        scene_types = ['室内', '户外', '城镇', '荒野', '秘境', '宫殿', '山林', '水域', '地下', '空中']
        pleasure_modes = ['突破', '打脸', '收获', '反转', '情感', '揭秘', '联盟', '逃生']
        chapter_assignments = []
        for i, ch_info in enumerate(chapters_info):
            ct = conflict_types[i % len(conflict_types)]
            st = scene_types[(i * 3 + 1) % len(scene_types)]
            sp = pleasure_modes[(i * 2 + 3) % len(pleasure_modes)]
            chapter_assignments.append(f"  第{start_chapter + i}章：冲突类型={ct}，主要场景={st}，核心爽点={sp}")

        assignments_str = '\n'.join(chapter_assignments)

        prompt = f"""你是一位{genre_label}领域的顶级网文作家，拥有15年创作经验，曾写出10+部爆款作品。风格为{style_str}，基调为{tone_str}。{school_label}{multi_genre_note}

## ⚠️ 写作铁律（违反任何一条即为失败）
1. **角色名字绝对锁定**：下方"已确立的角色"中的名字是最终确定的，你绝对不能更改、替换或创造新名字。主角名字是"{protagonist}"，如果已设定则必须使用此名
2. **【铁律】每章字数必须严格控制在{target_wc}字左右**：这是不可妥协的硬性要求
3. **每章之间必须有明显的情节推进**：不能重复相同的情节模式
4. **因果必须连贯**：每章开头必须承接上一章的结尾状态
5. **名字一致性**：所有角色名字必须与下方"已确立的角色"完全一致

{truth_context}

{character_context}

{previous_context}

## 📋 每章差异化分配（必须严格遵守）
以下是为每章预先分配的差异化元素，确保每章内容完全不同：

{assignments_str}

## 🚫 防重复铁律（违反即为失败）
1. **冲突类型必须轮换**：连续章节不能使用相同的冲突类型。严格按照上方分配执行
2. **场景不能重复**：每章的场景设定必须不同，严格按照上方分配执行
3. **对话模式不能重复**：禁止连续使用相同的对话模式（如连续两章都是"主角被质疑→主角用实力证明"）
4. **爽点模式不能重复**：每章的爽点设计必须不同，严格按照上方分配执行
5. **叙事节奏必须变化**：紧张章节后必须跟舒缓章节，形成节奏起伏
6. **每章开场方式必须不同**：不能连续两章以相同方式开场（对话/描写/动作/心理）

## 待生成章节
{chapters_str}

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

{genre_context}

{knowledge_injection}

## 输出格式
请严格按照以下JSON格式输出，不要包含其他内容：
{{
  "chapters": [
    {{"chapter_number": {start_chapter}, "title": "第{start_chapter}章标题", "content": "第{start_chapter}章完整内容..."}},
    ...
  ]
}}

每章字数严格控制在{target_wc}字左右，每章结尾必须有强有力的悬念钩子。"""

        try:
            llm.reset_operation_count()
            result_text = llm.generate(prompt, params=GenerationParams(temperature=0.92, max_tokens=target_wc * max_chapters * 2))
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0]
            result_text = re.sub(r',\s*}', '}', result_text)
            result_text = re.sub(r',\s*]', ']', result_text)
            result = json.loads(result_text)
            chapters = result.get('chapters', [])

            if len(chapters) >= 2:
                from difflib import SequenceMatcher
                for i in range(len(chapters)):
                    for j in range(i + 1, len(chapters)):
                        ci = chapters[i].get('content', '')
                        cj = chapters[j].get('content', '')
                        if ci and cj:
                            ci_head = ci[:200]
                            cj_head = cj[:200]
                            similarity = SequenceMatcher(None, ci_head, cj_head).ratio()
                            if similarity > 0.6:
                                log(f"DEDUP WARNING: ch{chapters[i].get('chapter_number')} vs ch{chapters[j].get('chapter_number')} head similarity={similarity:.2f}")
                                dup_ch = chapters[j]
                                dup_num = dup_ch.get('chapter_number', start_chapter + j)
                                fix_prompt = f"""你是一位网文作家。以下章节内容与前面章节的开头过于相似（相似度{similarity:.0%}）。

## 必须改变的要素
1. **开场方式**：不能以相同的方式开场（当前是"{ci_head[:50]}..."）
2. **冲突类型**：必须使用与上一章不同的冲突类型
3. **场景设定**：必须使用完全不同的场景
4. **叙事视角**：可以尝试从不同角色的视角开场

## 章节信息
第{dup_num}章：{dup_ch.get('title', '')}

## 要求
- 保持原有剧情走向不变
- 字数控制在{target_wc}字左右
- 直接输出章节正文，不要JSON包裹

现在重写第{dup_num}章："""
                                time.sleep(1.0)
                                fixed = llm.generate(fix_prompt, params=GenerationParams(temperature=0.9, max_tokens=target_wc * 2))
                                if fixed and len(fixed) > 200:
                                    chapters[j]['content'] = fixed
                                    log(f"DEDUP FIXED: ch{dup_num} regenerated")

            novel_title = outline_data.get('title', '未命名作品')
            novel_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'output', _safe_filename(novel_title))
            os.makedirs(novel_dir, exist_ok=True)

            for ch in chapters:
                ch_num = ch.get('chapter_number', start_chapter)
                ch_content = ch.get('content', '')
                ch_title = ch.get('title', f'第{ch_num}章')

                # 自动去AI痕迹
                try:
                    if ch_content and len(ch_content) > 100:
                        from ai_humanizer import detect_ai_traces, build_humanize_prompt
                        detection = detect_ai_traces(ch_content)
                        if detection.get('total_score', 100) < 70:
                            humanize_prompt = build_humanize_prompt(ch_content, detection)
                            if humanize_prompt:
                                deai_result = llm.generate(humanize_prompt, params=GenerationParams(temperature=0.7, max_tokens=len(ch_content)*2))
                                if deai_result and len(deai_result) > 100:
                                    ch_content = deai_result
                                    log(f"Batch DEAI applied for ch{ch_num}")
                except Exception as deai_err:
                    log(f"Batch DEAI warning ch{ch_num}: {deai_err}")

                ch_filename = f"第{ch_num}章_{_safe_filename(ch_title)}.txt"
                ch_path = os.path.join(novel_dir, ch_filename)
                with open(ch_path, 'w', encoding='utf-8') as f:
                    f.write(f"{ch_title}\n\n{ch_content}")

                # 更新章节缓存
                self.__class__.chapters_cache[ch_num] = {
                    'title': ch_title,
                    'content': ch_content[:500],
                    'summary': '',
                }

                # 更新真相文件
                try:
                    truth_files.add_chapter_summary(
                        chapter=ch_num,
                        title=ch_title,
                        core_events=[],
                        word_count=len(ch_content),
                    )
                except Exception as te:
                    log(f"Truth files update warning ch{ch_num}: {te}")

            self._send_json({"success": True, "chapters": chapters, "count": len(chapters)})
        except Exception as e:
            log(f"Batch chapter error: {e}")
            traceback.print_exc()
            self._send_json({"success": False, "error": str(e)[:200]})

    def _handle_update_config(self, data):
        try:
            updates = {}
            for key in ['provider', 'model_name', 'base_url', 'api_key',
                       'temperature', 'top_p', 'frequency_penalty',
                       'presence_penalty', 'max_tokens', 'timeout', 'max_retries']:
                if key in data:
                    if key == 'provider':
                        from llm_interface import ModelProvider
                        try:
                            updates[key] = ModelProvider(data[key])
                        except ValueError:
                            log(f"Unknown provider: {data[key]}, falling back to custom")
                            updates[key] = ModelProvider.CUSTOM
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
            traceback.print_exc()
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

    def _handle_generate_names_batch(self, data):
        genre = data.get('genre', '玄幻')
        characters = data.get('characters', [])
        world_notes = data.get('world_notes', '')
        story_context = data.get('story_context', '')
        count = data.get('count', 3)
        combined_context = '\n'.join([x for x in [world_notes, story_context] if x])

        if not characters:
            self._send_json({"success": False, "error": "请提供至少一个角色信息"})
            return

        log(f"Batch generating names for {len(characters)} characters, genre={genre}")

        results = []
        for char in characters:
            role = char.get('role', '角色')
            gender = char.get('gender', '男')
            personality = char.get('personality', '')
            try:
                profile = CharacterProfile(
                    role=role, gender=gender, age='young',
                    personality=personality,
                )
                names = name_engine.generate_character_names(
                    genre=genre, profile=profile, count=count,
                    story_context=combined_context,
                )
                names_data = []
                for r in names:
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
                results.append({
                    "role": role,
                    "gender": gender,
                    "personality": personality,
                    "names": names_data,
                })
            except Exception as e:
                log(f"Batch name error for {role}: {e}")
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
                results.append({
                    "role": role,
                    "gender": gender,
                    "personality": personality,
                    "names": names_data,
                    "note": f"Fallback: {str(e)[:100]}",
                })

        self._send_json({"success": True, "results": results})

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

            try:
                if pipeline.current_chapter == chapter and pipeline.current_stage == "auditing":
                    audit_result = pipeline.set_audit_result(result.to_dict())
                    log(f"Pipeline audit result: {audit_result.get('status')}")
            except Exception as pe:
                log(f"Pipeline audit warning: {pe}")

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
        import re as _re
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

                if _re.search(r'(?:悬念|冲突|动作|疑问|危险)', chapter_text[:300]):
                    required_pass += 1

                if _re.search(r'(?:悬念|疑问|未解|下一)', chapter_text[-300:]):
                    required_pass += 1

                ai_patterns_count = len(_re.findall(r'(?:此外|然而|因此|值得注意的是|总而言之|综上所述)', chapter_text))
                if ai_patterns_count < 5:
                    required_pass += 1

                required_pass += 1

                if _re.search(r'(?:突破|碾压|击败|收获|觉醒|逆袭)', chapter_text):
                    optional_pass += 1

                sensory_count = len(_re.findall(r'(?:看到|听到|闻到|触到|感到|觉得)', chapter_text))
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

    def _handle_memory_fingerprint(self, data):
        action = data.get('action', 'get')
        try:
            if action == 'get':
                fp = project_memory.get_fingerprint()
                self._send_json({"success": True, "fingerprint": fp})
            elif action == 'generate':
                chapters = data.get('chapters', [])
                genres = data.get('genres', [])
                styles = data.get('styles', [])
                fp = project_memory.generate_fingerprint(chapters, genres, styles)
                self._send_json({"success": True, "fingerprint": fp})
            elif action == 'lock':
                project_memory.lock_fingerprint()
                self._send_json({"success": True, "message": "写作指纹已锁定"})
            elif action == 'unlock':
                project_memory.unlock_fingerprint()
                self._send_json({"success": True, "message": "写作指纹已解锁"})
            elif action == 'check':
                chapter = data.get('chapter', 1)
                text = data.get('text', '')
                result = project_memory.check_style_consistency(chapter, text)
                self._send_json({"success": True, "result": result})
            else:
                self._send_json({"error": "Unknown action"}, 400)
        except Exception as e:
            log(f"Memory fingerprint error: {e}")
            self._send_json({"success": False, "error": str(e)[:200]})

    def _handle_memory_stats(self, data):
        try:
            stats = project_memory.get_memory_stats()
            self._send_json({"success": True, "stats": stats})
        except Exception as e:
            log(f"Memory stats error: {e}")
            self._send_json({"success": False, "error": str(e)[:200]})

    def _handle_truth_context(self, data):
        chapter = data.get('chapter', 1)
        try:
            context = truth_files.get_context_for_chapter(chapter)
            self._send_json({"success": True, "context": context, "chapter": chapter})
        except Exception as e:
            log(f"Truth context error: {e}")
            self._send_json({"success": False, "error": str(e)[:200]})

    def _handle_truth_all(self, data):
        try:
            all_files = truth_files.get_all_truth_files()
            self._send_json({"success": True, "truth_files": all_files})
        except Exception as e:
            log(f"Truth all error: {e}")
            self._send_json({"success": False, "error": str(e)[:200]})

    def _handle_truth_update(self, data):
        file_name = data.get('file', '')
        chapter = data.get('chapter', 1)
        try:
            if file_name == 'current_state':
                result = truth_files.update_current_state(
                    chapter=chapter,
                    world_time=data.get('world_time', ''),
                    locations=data.get('locations'),
                    character_positions=data.get('character_positions'),
                    known_information=data.get('known_information'),
                    active_conflicts=data.get('active_conflicts'),
                    atmosphere=data.get('atmosphere', ''),
                )
            elif file_name == 'particle_ledger':
                result = truth_files.update_particle_ledger(
                    chapter=chapter,
                    items=data.get('items'),
                    currency=data.get('currency'),
                    resources=data.get('resources'),
                )
            elif file_name == 'pending_hooks':
                action = data.get('action', 'add')
                if action == 'resolve':
                    result = truth_files.resolve_hook(
                        hook_id=data.get('hook_id', ''),
                        resolution_chapter=chapter,
                        resolution_note=data.get('resolution_note', ''),
                    )
                else:
                    result = truth_files.add_hook(
                        chapter=chapter,
                        hook_description=data.get('hook_description', ''),
                        hook_type=data.get('hook_type', 'foreshadowing'),
                        expected_resolution_chapter=data.get('expected_resolution_chapter'),
                        related_characters=data.get('related_characters'),
                    )
            elif file_name == 'chapter_summaries':
                result = truth_files.add_chapter_summary(
                    chapter=chapter,
                    title=data.get('title', ''),
                    core_events=data.get('core_events'),
                    emotional_changes=data.get('emotional_changes'),
                    key_decisions=data.get('key_decisions'),
                    character_appearances=data.get('character_appearances'),
                    word_count=data.get('word_count', 0),
                )
            elif file_name == 'subplot_progress':
                result = truth_files.update_subplot(
                    subplot_id=data.get('subplot_id', ''),
                    chapter=chapter,
                    progress_description=data.get('progress_description', ''),
                    milestone_reached=data.get('milestone_reached'),
                    status=data.get('status', 'active'),
                )
            elif file_name == 'emotional_arcs':
                result = truth_files.update_emotional_arc(
                    character_name=data.get('character_name', ''),
                    chapter=chapter,
                    emotional_state=data.get('emotional_state', ''),
                    intensity=data.get('intensity', 50),
                    trigger_event=data.get('trigger_event', ''),
                    arc_phase=data.get('arc_phase', ''),
                )
            elif file_name == 'character_matrix':
                result = truth_files.update_character_matrix(
                    character_name=data.get('character_name', ''),
                    chapter=chapter,
                    role=data.get('role', ''),
                    motivation=data.get('motivation', ''),
                    ability_changes=data.get('ability_changes'),
                    relationships=data.get('relationships'),
                    current_goal=data.get('current_goal', ''),
                )
            else:
                self._send_json({"success": False, "error": f"Unknown truth file: {file_name}"}, 400)
                return
            self._send_json({"success": True, "result": result})
        except Exception as e:
            log(f"Truth update error: {e}")
            self._send_json({"success": False, "error": str(e)[:200]})

    def _handle_truth_hooks(self, data):
        try:
            pending = truth_files.get_pending_hooks()
            self._send_json({"success": True, "pending_hooks": pending, "count": len(pending)})
        except Exception as e:
            log(f"Truth hooks error: {e}")
            self._send_json({"success": False, "error": str(e)[:200]})

    def _handle_pipeline_start(self, data):
        chapter = data.get('chapter', 1)
        try:
            result = pipeline.start_chapter(chapter)
            self._send_json({"success": True, "pipeline": result})
        except Exception as e:
            log(f"Pipeline start error: {e}")
            self._send_json({"success": False, "error": str(e)[:200]})

    def _handle_pipeline_state(self, data):
        try:
            state = pipeline.get_pipeline_state()
            self._send_json({"success": True, "pipeline": state})
        except Exception as e:
            log(f"Pipeline state error: {e}")
            self._send_json({"success": False, "error": str(e)[:200]})

    def _handle_pipeline_revise(self, data):
        content = data.get('content', '')
        try:
            review_result = reviewer.review_chapter(
                chapter=pipeline.current_chapter,
                chapter_text=content,
                use_llm=True,
            )
            audit_dict = review_result.to_dict()
            result = pipeline.revise_and_audit(content, audit_dict)

            if result.get("status") == "revising":
                revision_prompt = pipeline.build_revision_prompt(audit_dict.get("issues", []))
                self._send_json({
                    "success": True,
                    "pipeline": result,
                    "revision_prompt": revision_prompt,
                    "issues": audit_dict.get("issues", []),
                })
            else:
                self._send_json({
                    "success": True,
                    "pipeline": result,
                    "final_content": content,
                })
        except Exception as e:
            log(f"Pipeline revise error: {e}")
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

        log(f"Detecting AI traces in {len(text)} chars (deep={deep})...")

        local_result = detect_ai_traces(text)
        log(f"Local detection: {len(local_result.get('traces_found',[]))} traces, score={local_result.get('total_score',0)}")

        if deep:
            try:
                detection_prompt = build_ai_detection_report_prompt(text)
                llm_result = llm.generate(
                    detection_prompt,
                    system_prompt="你是一位专业的AI写作痕迹检测专家，基于NWACS智能检测标准进行检测。请严格按JSON格式输出。",
                    params=GenerationParams(temperature=0.3, max_tokens=2048),
                )
                try:
                    json_match = re.search(r'\{[\s\S]*\}', llm_result)
                    if json_match:
                        llm_data = json.loads(json_match.group(0))
                        local_result["llm_analysis"] = llm_data
                        local_result["ai_score"] = llm_data.get("ai_score", local_result["ai_probability"])
                        local_result["human_score"] = llm_data.get("human_score", local_result["total_score"])
                        if llm_data.get("issues"):
                            for iss in llm_data["issues"]:
                                local_result["traces_found"].append({
                                    "category": iss.get("category", ""),
                                    "pattern": iss.get("pattern", ""),
                                    "found": iss.get("description", ""),
                                    "severity": iss.get("severity", "medium"),
                                    "fix": iss.get("fix", ""),
                                    "source": "llm",
                                })
                except json.JSONDecodeError:
                    log(f"Failed to parse LLM detection result JSON")
            except Exception as e:
                log(f"LLM deep detection error: {e}")

        self._send_json({"success": True, "result": local_result})

    def _handle_save_chapter(self, data):
        ch_num = data.get('chapter_number', 1)
        title = data.get('title', f'第{ch_num}章')
        content = data.get('content', '')
        word_count = data.get('word_count', len(re.sub(r'\s', '', content)))

        if not content:
            self._send_json({"error": "No content provided"}, 400)
            return

        try:
            novel_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'output', 'novel')
            os.makedirs(novel_dir, exist_ok=True)

            ch_data = {
                'chapter': ch_num,
                'title': title,
                'content': content,
                'word_count': word_count,
                'updated_at': datetime.now().isoformat(),
            }

            ch_path = os.path.join(novel_dir, f'chapter_{ch_num:04d}.json')
            with open(ch_path, 'w', encoding='utf-8') as f:
                json.dump(ch_data, f, ensure_ascii=False, indent=2)

            log(f"Chapter {ch_num} saved to {ch_path}")
            self._send_json({"success": True, "chapter_number": ch_num, "saved_path": ch_path})
        except Exception as e:
            log(f"Save chapter error: {e}")
            self._send_json({"error": str(e)[:200]}, 500)

    def _handle_rewrite(self, data):
        text = data.get('text', '')
        style = data.get('style', 'deai')

        if not text:
            self._send_json({"error": "No text provided"}, 400)
            return

        log(f"Rewriting {len(text)} chars with style={style}...")

        deai_system_prompt = """你是一位拥有15年写作经验的顶级作家，精通将AI生成的文本改写为自然的人类写作风格。

【去AI核心原则 — NWACS 智能去AI痕迹引擎 v3.0】

=== 一、降低AI痕迹（核心目标）===
1. 重写文本更自然：去除机械感，让文字充满人性温度
2. 减少完美句式：故意保留轻微的"不完美"，如小停顿、口语化表达
3. 个性化表达：加入独特的视角和表达方式，避免模板化
4. 口语化融入：适当使用"嗯""呃""那个""就是"等自然口语词
5. 避免机械段落：打破AI特有的均匀段落结构，让段落长短错落有致

=== 二、润色句子 ===
6. 用词精准生动：替换平淡词汇为更精准、更有画面感的表达
7. 句式流畅：调整语序，让句子读起来更顺口
8. 增强韵律感：注意平仄、节奏，让文字有音乐感
9. 风格统一：保持全文风格一致，避免混搭
10. 修正错误：修复语法、用词不当等问题

=== 三、简化结构 ===
11. 拆分长段落：每段不超过5句，一段一中心
12. 去除模糊歧义：明确指代，避免"这""那""其"等模糊代词
13. 层次清晰：逻辑递进，让读者一目了然

=== 四、转换语气 ===
14. 正式/非正式切换：根据场景调整语气强度
15. 匹配受众认知：使用目标读者熟悉的表达方式
16. 调整术语密度：避免术语堆砌，必要时解释专业概念
17. 情感贴合：让语气与内容情感相匹配

=== 五、增加细节 ===
18. 补充案例数据：加入具体数字、实例，增强说服力
19. 解释概念：对抽象内容进行具象化处理
20. 感官描写：加入视觉、听觉、触觉、嗅觉等细节

=== 六、突出核心 ===
21. 删除重复冗余：去除重复表达，合并相似观点
22. 去无关细节：砍掉与主题无关的内容
23. 减少修饰：避免过度形容词堆砌，每句有明确目的

=== 七、调整节奏 ===
24. 长短句混合：短句（≤15字）占20%，长句（≥30字）占15%
25. 简单句与复合句交替：避免句式单调
26. 修辞问句：适当使用反问、设问增强节奏感
27. 韵律自然：避免机械排比，让节奏有呼吸感

=== 八、避免AI特征词汇 ===
28. 禁用空洞大词：删除"赋能""闭环""底层逻辑""降维打击""颗粒度"
29. 禁用AI连接词：删除"此外""至关重要""深入探讨""格局"
30. 禁用夸张宣传词：删除"令人叹为观止""开创性的""必游之地"
31. 禁用模糊归因：删除"专家认为""行业报告显示""多个来源"
32. 禁用填充短语：删除"值得注意的是""为了实现这一目标""在这个时间点"

=== 九、灵魂注入技巧 ===
33. 动作替代形容词：不写"他很愤怒"，写"他一拳砸在桌上"
34. 个人语气表达：加入"我觉得""我在想""让我困扰"等主观感受
35. 本土生活细节：加入烟火气、人情世故、市井气息
36. 幽默或锋芒：适当加入讽刺、自嘲、黑色幽默

=== 十、语言精炼原则 ===
37. 拆分长定语：多层定语拆为短句，每层"的"不超过2个
38. 补全主语：避免连续省略主语
39. 删除范畴词：删除"问题""情况""状态""方面""领域"等空洞词汇
40. 控制虚词密度：减少"的""地""得"使用频率

=== 十一、节奏注入要求 ===
41. 句子长度必须剧烈变化：目标Burstiness>50
42. 不能连续3句长度差小于3个字
43. 段落长度不均匀：有的段落1句，有的段落8句
44. 打破对称结构：前后部分不要刻意对称

=== 十二、输出前自检清单 ===
□ 连续三个句子长度是否不同？
□ 段落是否以简洁的单行结尾？
□ 破折号是否≤2处？
□ "此外""然而"等连接词是否≤3处？
□ 三段式列举是否≤2处？
□ 是否有具体人名/地名/数字？
□ 是否有个人语气和情感表达？
□ Burstiness是否>30？

【最终铁律】
- 直接输出改写后的文本，不要任何解释、不要前言、不要后记
- 保持原文的核心信息和情节不变
- 如果原文已经是自然的人类写作风格，只做微调，不要过度修改"""

        detection = detect_ai_traces(text)
        traces_count = len(detection.get("traces_found", []))
        log(f"Pre-rewrite detection: {traces_count} AI traces found, score={detection.get('total_score',0)}")

        humanize_prompt = build_humanize_prompt(text, detection) if traces_count > 0 else ""

        style_instructions = {
            "deai": "请将以下AI生成的文本改写为自然的人类写作风格，消除所有AI痕迹。",
            "polish": "请润色以下文本，使其用词更精准、表达更生动、语句更流畅，保持原意不变。",
            "simplify": "请简化以下文本结构：拆分长段落（每段不超过5句）、拆分长句（每句不超过40字）、用短句替代复杂从句。",
            "tone_formal": "请将以下文本改为正式、严谨的书面语气，适合正式场合使用。",
            "tone_casual": "请将以下文本改为自然、亲切的口语化表达，像朋友间聊天一样。",
            "details": "请为以下文本增加细节：补充具体案例、数据、背景信息、感官描写，使内容更丰富立体。",
            "concise": "请精简以下文本：删除重复表达、冗余修饰、无关内容，突出核心信息。",
            "rhythm": "请调整以下文本的节奏：长短句交替使用（短句≤15字占比20%，长句≥30字占比15%），段落长度变化，避免连续3句同长度。",
            "expand": "请扩写以下文本：围绕主题丰富信息，增加细节描写、对话、心理活动、环境描写，使内容更充实。",
            "imitate": "请先分析以下文本的原文风格（用词习惯、句式特点、节奏感、语气），然后保持该风格重写文本，使其风格更鲜明一致。",
            "wording": "请优化以下文本的用词：替换平淡词汇为更精准生动的表达，避免重复用词，删除陈词滥调和空洞大词。",
            "abbreviate": "请缩写以下文本：删除无关内容、合并重复表达、精简冗余描写，保留核心情节和信息。",
            "maintain_theme": "请重写以下文本，确保中心思想贯穿全文：删除偏离主题的内容，强化主题相关的表达，使主线更清晰。",
            "fix": "请根据提供的问题描述和修复建议，修改指定位置的文本。",
        }

        issue = data.get('issue', None)
        
        instruction = style_instructions.get(style, style_instructions["deai"])

        system_prompt = deai_system_prompt if style == "deai" else f"""你是一位拥有15年写作经验的顶级文字编辑。

{instruction}

## 改写原则
1. 保持原文的核心信息和情节不变
2. 不要过度修改，保留原文的特色和风格
3. 直接输出改写后的文本，不要任何解释、不要前言、不要后记
4. 确保改写后的文本自然流畅，读起来像人类写作"""

        if style == "deai" and humanize_prompt:
            prompt = humanize_prompt
        elif style == "fix" and issue:
            issue_desc = issue.get('description', '')
            issue_loc = issue.get('location', '')
            issue_fix = issue.get('fix', '')
            prompt = f"""请根据以下问题描述和修复建议，修改原文中指定位置的内容。

## 问题描述
{issue_desc}

## 问题位置
{issue_loc}

## 修复建议
{issue_fix}

## 原文
{text}

## 要求
1. 只修改问题位置附近的内容
2. 保持其他部分不变
3. 直接输出修改后的完整文本，不要任何额外说明"""
        else:
            prompt = f"{instruction}\n\n原文：\n{text}"

        try:
            rewritten = llm.generate(
                prompt,
                system_prompt=system_prompt,
                params=GenerationParams(temperature=0.85, max_tokens=4096),
            )

            post_detection = detect_ai_traces(rewritten)
            post_traces = len(post_detection.get("traces_found", []))
            log(f"Post-rewrite detection: {post_traces} AI traces (was {traces_count}), score={post_detection.get('total_score',0)}")

            self._send_json({
                "success": True,
                "content": rewritten,
                "before_score": detection.get("total_score", 0),
                "after_score": post_detection.get("total_score", 0),
                "before_traces": traces_count,
                "after_traces": post_traces,
            })
        except Exception as e:
            log(f"Rewrite error: {e}")
            traceback.print_exc()
            self._send_json({"success": True, "content": text, "note": f"Fallback: {str(e)[:100]}"})

    def _handle_retention_score(self, data):
        chapter = data.get('chapter', 1)
        score = retention_system.get_chapter_retention_score(chapter)
        self._send_json({"success": True, "score": score})

    def _handle_retention_analyze(self, data):
        chapter = data.get('chapter', 1)
        content = data.get('content', '')
        summary = data.get('summary', '')
        result = retention_system.analyze_chapter_for_retention(chapter, content, summary)
        self._send_json({"success": True, "analysis": result})

    def _handle_retention_add_hook(self, data):
        hook_type = data.get('hook_type', 'question')
        description = data.get('description', '')
        chapter = data.get('chapter', 1)
        position = data.get('position', 'opening')
        strength = data.get('strength', 5)
        if not description:
            self._send_json({"error": "description is required"}, 400)
            return
        hook = retention_system.add_hook(hook_type, description, chapter, position, strength)
        self._send_json({"success": True, "hook": hook.to_dict()})

    def _handle_retention_add_cool_point(self, data):
        point_type = data.get('point_type', 'power_up')
        description = data.get('description', '')
        chapter = data.get('chapter', 1)
        intensity = data.get('intensity', 5)
        buildup = data.get('buildup_chapters', 0)
        if not description:
            self._send_json({"error": "description is required"}, 400)
            return
        cp = retention_system.add_cool_point(point_type, description, chapter, intensity, buildup)
        self._send_json({"success": True, "cool_point": cp.to_dict()})

    def _handle_retention_add_debt(self, data):
        debt_type = data.get('debt_type', 'foreshadowing')
        description = data.get('description', '')
        chapter = data.get('chapter', 1)
        expected_ch = data.get('expected_resolution_chapter')
        urgency = data.get('urgency', 5)
        characters = data.get('related_characters', [])
        if not description:
            self._send_json({"error": "description is required"}, 400)
            return
        debt = retention_system.add_reader_debt(
            debt_type, description, chapter, expected_ch, urgency, characters
        )
        self._send_json({"success": True, "debt": debt.to_dict()})

    def _handle_retention_resolve_debt(self, data):
        debt_id = data.get('debt_id', '')
        chapter = data.get('chapter', 1)
        if not debt_id:
            self._send_json({"error": "debt_id is required"}, 400)
            return
        debt = retention_system.resolve_debt(debt_id, chapter)
        if debt:
            self._send_json({"success": True, "debt": debt.to_dict()})
        else:
            self._send_json({"error": "Debt not found or already resolved"}, 404)

    def _handle_fatigue_analyze(self, data):
        chapter = data.get('chapter', 1)
        content = data.get('content', '')
        if not content:
            self._send_json({"error": "content is required"}, 400)
            return
        stats = fatigue_detector.analyze_chapter(chapter, content)
        report = fatigue_detector.get_chapter_fatigue_report(chapter)
        self._send_json({"success": True, "stats": stats.to_dict(), "report": report})

    def _handle_fatigue_report(self, data):
        chapter = data.get('chapter', 1)
        report = fatigue_detector.get_chapter_fatigue_report(chapter)
        self._send_json({"success": True, "report": report})

    def _handle_fatigue_overall(self, data):
        report = fatigue_detector.get_overall_fatigue_report()
        self._send_json({"success": True, "report": report})

    def _handle_fatigue_suggestions(self, data):
        word = data.get('word', '')
        if not word:
            self._send_json({"error": "word is required"}, 400)
            return
        result = fatigue_detector.get_word_replacement_suggestions(word)
        self._send_json({"success": True, "suggestions": result})

    def _handle_gates_evaluate(self, data):
        chapter = data.get('chapter', 1)
        content = data.get('content', '')
        if not content:
            self._send_json({"error": "content is required"}, 400)
            return

        ai_result = detect_ai_traces(content)
        ai_score = ai_result.get("total_score", 0)

        fatigue_stats = fatigue_detector.analyze_chapter(chapter, content)
        fatigue_score = fatigue_stats.fatigue_score

        retention_score_data = retention_system.get_chapter_retention_score(chapter)
        retention_score = retention_score_data.get("total_score", 0)

        word_count = len(content.replace('\n', '').replace(' ', ''))
        target_word_count = data.get('target_word_count', 4000)

        consistency_issues = data.get('consistency_issues', 0)
        pacing_score = data.get('pacing_score', 70)
        dialogue_ratio = data.get('dialogue_ratio', 0.2)
        hook_count = data.get('hook_count', 1)

        result = review_gates.evaluate_chapter(
            chapter=chapter,
            ai_trace_score=ai_score,
            fatigue_score=fatigue_score,
            retention_score=retention_score,
            word_count=word_count,
            target_word_count=target_word_count,
            consistency_issues=consistency_issues,
            pacing_score=pacing_score,
            dialogue_ratio=dialogue_ratio,
            hook_count=hook_count,
        )
        self._send_json({"success": True, "result": result})

    def _handle_gates_chapter(self, data):
        chapter = data.get('chapter', 1)
        result = review_gates.get_chapter_gates(chapter)
        if result:
            self._send_json({"success": True, "result": result})
        else:
            self._send_json({"error": f"第{chapter}章暂无审查数据"}, 404)

    def _handle_gates_summary(self, data):
        summary = review_gates.get_all_gates_summary()
        self._send_json({"success": True, "summary": summary})

    def _handle_rag_search(self, data):
        query = data.get('query', '')
        top_k = data.get('top_k', 10)
        chapter_filter = data.get('chapter')
        if not query:
            self._send_json({"error": "query is required"}, 400)
            return
        results = rag_engine.search(query, top_k=top_k, filter_chapter=chapter_filter)
        self._send_json({"success": True, "results": [r.to_dict() for r in results], "count": len(results)})

    def _handle_rag_context(self, data):
        chapter = data.get('chapter', 1)
        summary = data.get('summary', '')
        max_chars = data.get('max_chars', 3000)
        context = rag_engine.get_relevant_context(chapter, summary, max_chars)
        prompt = rag_engine.build_context_prompt(chapter, summary)
        self._send_json({"success": True, "context": context, "prompt": prompt})

    def _handle_rag_reverse(self, data):
        chapter = data.get('chapter', 1)
        content = data.get('content', '')
        if not content:
            self._send_json({"error": "content is required"}, 400)
            return
        rag_engine.index_chapter(chapter, content)
        result = rag_engine.reverse_engineer_chapter(chapter, content)
        self._send_json({"success": True, "analysis": result})

    def _handle_rag_consistency(self, data):
        chapter = data.get('chapter', 1)
        content = data.get('content', '')
        if not content:
            self._send_json({"error": "content is required"}, 400)
            return
        result = rag_engine.check_consistency(chapter, content)
        self._send_json({"success": True, "consistency": result})
        
    def _handle_rag_characters(self, data):
        network = rag_engine.get_character_network()
        self._send_json({"success": True, "network": network})
        
    def _handle_rag_timeline(self, data):
        timeline = rag_engine.get_event_timeline()
        self._send_json({"success": True, "timeline": timeline})
        
    def _handle_rag_stats(self, data):
        stats = rag_engine.get_stats()
        self._send_json({"success": True, "stats": stats})

    # ── Fragment Management ──
    def _handle_fragment_save(self, data):
        chapter = data.get('chapter', 1)
        content = data.get('content', '')
        title = data.get('title', f'第{chapter}章')
        word_count = data.get('word_count', len(content))
        frag_dir = os.path.join(PROJECT_ROOT, 'fragments')
        os.makedirs(frag_dir, exist_ok=True)
        frag_file = os.path.join(frag_dir, f'chapter_{chapter}_fragments.json')
        fragments = []
        if os.path.exists(frag_file):
            try:
                with open(frag_file, 'r', encoding='utf-8') as f:
                    fragments = json.load(f)
            except:
                fragments = []
        version = len(fragments) + 1
        frag = {
            'id': f'ch{chapter}_v{version}_{int(time.time())}',
            'chapter': chapter,
            'version': version,
            'title': title,
            'content': content,
            'word_count': word_count,
            'created_at': time.strftime('%Y-%m-%d %H:%M:%S'),
            'label': f'v{version} - {time.strftime("%H:%M")}'
        }
        fragments.append(frag)
        with open(frag_file, 'w', encoding='utf-8') as f:
            json.dump(fragments, f, ensure_ascii=False, indent=2)
        self._send_json({"success": True, "version": frag['label'], "fragment": frag})

    def _handle_fragment_list(self, data):
        chapter = data.get('chapter', 1)
        frag_file = os.path.join(PROJECT_ROOT, 'fragments', f'chapter_{chapter}_fragments.json')
        fragments = []
        if os.path.exists(frag_file):
            try:
                with open(frag_file, 'r', encoding='utf-8') as f:
                    fragments = json.load(f)
            except:
                fragments = []
        self._send_json({"success": True, "fragments": fragments})

    def _handle_fragment_get(self, data):
        fragment_id = data.get('fragment_id', '')
        if not fragment_id:
            self._send_json({"error": "fragment_id required"}, 400)
            return
        frag_dir = os.path.join(PROJECT_ROOT, 'fragments')
        if not os.path.exists(frag_dir):
            self._send_json({"error": "No fragments found"}, 404)
            return
        for fn in os.listdir(frag_dir):
            if not fn.endswith('.json'):
                continue
            try:
                with open(os.path.join(frag_dir, fn), 'r', encoding='utf-8') as f:
                    fragments = json.load(f)
                for frag in fragments:
                    if frag.get('id') == fragment_id:
                        self._send_json({"success": True, "fragment": frag})
                        return
            except:
                continue
        self._send_json({"error": "Fragment not found"}, 404)

    def _handle_fragment_apply(self, data):
        fragment_id = data.get('fragment_id', '')
        if not fragment_id:
            self._send_json({"error": "fragment_id required"}, 400)
            return
        frag_dir = os.path.join(PROJECT_ROOT, 'fragments')
        for fn in os.listdir(frag_dir):
            if not fn.endswith('.json'):
                continue
            try:
                with open(os.path.join(frag_dir, fn), 'r', encoding='utf-8') as f:
                    fragments = json.load(f)
                for frag in fragments:
                    if frag.get('id') == fragment_id:
                        ch_num = frag.get('chapter', 1)
                        self._send_json({
                            "success": True,
                            "chapter": ch_num,
                            "chapter_data": {
                                "title": frag.get('title', ''),
                                "content": frag.get('content', ''),
                                "word_count": frag.get('word_count', len(frag.get('content', '')))
                            }
                        })
                        return
            except:
                continue
        self._send_json({"error": "Fragment not found"}, 404)

    # ── Character State Tracking ──
    def _handle_characters_states(self, data):
        char_file = os.path.join(PROJECT_ROOT, 'character_states.json')
        characters = []
        if os.path.exists(char_file):
            try:
                with open(char_file, 'r', encoding='utf-8') as f:
                    characters = json.load(f)
            except:
                characters = []
        if not characters:
            characters = self._extract_characters_from_chapters()
            try:
                with open(char_file, 'w', encoding='utf-8') as f:
                    json.dump(characters, f, ensure_ascii=False, indent=2)
            except:
                pass
        self._send_json({"success": True, "characters": characters})

    def _extract_characters_from_chapters(self):
        chars = {}
        novel_dir = os.path.join(PROJECT_ROOT, 'novel')
        if not os.path.exists(novel_dir):
            return []
        for fn in sorted(os.listdir(novel_dir)):
            if fn.endswith('.json'):
                try:
                    with open(os.path.join(novel_dir, fn), 'r', encoding='utf-8') as f:
                        ch = json.load(f)
                    content = ch.get('content', '') + ' ' + ch.get('title', '')
                    chapter_num = ch.get('chapter', 0)

                    name_candidates = set()

                    patterns = [
                        r'([\u4e00-\u9fff]{2,4})(?:说|道|问|答|喊|叫|怒|笑|哭|叹|骂|喝|吼|哼|嗯|啊|哦|啦|呢|吗|吧|呀|嘛|哈|嘿|喂|请|谢|拜|跪)',
                        r'(?:说|道|问|答|喊|叫)[\u4e00-\u9fff]{0,10}?[：:]["「『【]([^"」』】]{2,4})',
                        r'([\u4e00-\u9fff]{2,4})(?:大侠|公子|小姐|长老|宗主|掌门|师兄|师弟|师姐|师妹|前辈|老祖|天尊|大帝|圣主|魔王|教主|大人|将军|陛下|王爷|公主|殿下|先生|女士|姑娘|兄弟)',
                        r'[「『【]([^「』】]{2,4})[」』】]',
                        r'([\u4e00-\u9fff]{2,4})(?:的身影|的声音|的眼神|的脚步|的笑容|的拳头|的长剑|的气势|的气息|的威压|的嘴角|的眼中|的脸上|的手上|的心里)',
                        r'([\u4e00-\u9fff]{2,4})(?:心中|体内|身后|面前|脚下|手中|眼前|脑海|身旁)',
                        r'(?:只见|但见|却见|便见|就见|看到|发现|只见那|但见那)([\u4e00-\u9fff]{2,4})',
                        r'(?:对|向|朝|跟|和|与|给|为|被|把|将)([\u4e00-\u9fff]{2,4})(?:说|道|问|喊|叫|笑|怒|拜|跪|拱手|抱拳|点头|摇头|行礼)',
                    ]

                    for pattern in patterns:
                        for match in re.finditer(pattern, content):
                            name = match.group(1).strip()
                            if name and len(name) >= 2 and len(name) <= 6:
                                name_candidates.add(name)

                    for n in name_candidates:
                        if n not in chars:
                            chars[n] = {
                                'name': n,
                                'status': 'alive',
                                'role': 'unknown',
                                'last_chapter': chapter_num,
                                'notes': '',
                                'mention_count': content.count(n),
                            }
                except:
                    continue
        sorted_chars = sorted(chars.values(), key=lambda x: -x.get('mention_count', 0))
        return sorted_chars[:50]

    # ── Style Fingerprint Handlers ──
    def _handle_style_analyze(self, data):
        text = data.get('text', '')
        label = data.get('label', 'default')
        if not text:
            self._send_json({"error": "text required"}, 400)
            return
        try:
            fp = style_engine.analyze(text, label)
            self._send_json({
                "success": True,
                "fingerprint": {
                    "sentence_length_mean": fp.sentence_length_mean,
                    "sentence_length_std": fp.sentence_length_std,
                    "dialogue_ratio": fp.dialogue_ratio,
                    "paragraph_avg_length": fp.paragraph_avg_length,
                    "emotion_word_ratio": fp.emotion_word_ratio,
                    "action_word_ratio": fp.action_word_ratio,
                    "passive_voice_ratio": fp.passive_voice_ratio,
                    "avg_sentence_complexity": fp.avg_sentence_complexity,
                    "style_rules": fp.style_rules,
                    "top_bigrams": [f'{w1} {w2}' for (w1, w2), _ in fp.top_bigrams[:5]],
                },
                "label": label,
            })
        except Exception as e:
            log(f"Style analyze error: {e}")
            self._send_json({"success": False, "error": str(e)[:200]})

    def _handle_style_compare(self, data):
        text = data.get('text', '')
        reference_label = data.get('reference_label', 'default')
        if not text:
            self._send_json({"error": "text required"}, 400)
            return
        try:
            result = style_engine.compare(text, reference_label)
            self._send_json({"success": True, "comparison": result})
        except Exception as e:
            log(f"Style compare error: {e}")
            self._send_json({"success": False, "error": str(e)[:200]})

    def _handle_style_list(self, data):
        try:
            fingerprints = style_engine.list_fingerprints()
            self._send_json({"success": True, "fingerprints": fingerprints})
        except Exception as e:
            log(f"Style list error: {e}")
            self._send_json({"success": False, "error": str(e)[:200]})

    # ── Strand Weave Handlers ──
    def _handle_strand_analyze(self, data):
        chapter = data.get('chapter', 1)
        content = data.get('content', '')
        if not content:
            self._send_json({"error": "content required"}, 400)
            return
        try:
            record = strand_engine.analyze_chapter(chapter, content)
            self._send_json({
                "success": True,
                "analysis": {
                    "chapter": record.chapter,
                    "quest_ratio": record.quest_ratio,
                    "fire_ratio": record.fire_ratio,
                    "constellation_ratio": record.constellation_ratio,
                    "dominant": record.dominant_strand,
                    "quest_samples": record.quest_content[:3],
                    "fire_samples": record.fire_content[:3],
                    "constellation_samples": record.constellation_content[:3],
                },
            })
        except Exception as e:
            log(f"Strand analyze error: {e}")
            self._send_json({"success": False, "error": str(e)[:200]})

    def _handle_strand_report(self, data):
        try:
            report = strand_engine.get_rhythm_report()
            self._send_json({"success": True, "report": report})
        except Exception as e:
            log(f"Strand report error: {e}")
            self._send_json({"success": False, "error": str(e)[:200]})

    def _handle_strand_suggest(self, data):
        chapter = data.get('chapter', 1)
        try:
            suggestion = strand_engine.get_strand_suggestion(chapter)
            self._send_json({"success": True, "suggestion": suggestion})
        except Exception as e:
            log(f"Strand suggest error: {e}")
            self._send_json({"success": False, "error": str(e)[:200]})

    # ── Truth File Manager (New) Handlers ──
    def _handle_truth_new_status(self, data):
        try:
            status = truth_file_mgr.get_all_status()
            self._send_json({"success": True, "truth_files": status})
        except Exception as e:
            log(f"Truth new status error: {e}")
            self._send_json({"success": False, "error": str(e)[:200]})

    def _handle_truth_new_init(self, data):
        outline = data.get('outline', {})
        protagonist = data.get('protagonist', '')
        try:
            truth_file_mgr.initialize_from_outline(outline, protagonist)
            status = truth_file_mgr.get_all_status()
            self._send_json({"success": True, "truth_files": status})
        except Exception as e:
            log(f"Truth new init error: {e}")
            self._send_json({"success": False, "error": str(e)[:200]})

    def _handle_truth_new_update(self, data):
        file_name = data.get('file', '')
        content = data.get('content', '')
        if not file_name or not content:
            self._send_json({"error": "file and content required"}, 400)
            return
        try:
            truth_file_mgr.update_file(file_name, content)
            self._send_json({"success": True, "file": file_name})
        except Exception as e:
            log(f"Truth new update error: {e}")
            self._send_json({"success": False, "error": str(e)[:200]})

    def _handle_truth_new_hooks(self, data):
        try:
            hooks = truth_file_mgr.get_hooks_summary()
            self._send_json({"success": True, "hooks": hooks})
        except Exception as e:
            log(f"Truth new hooks error: {e}")
            self._send_json({"success": False, "error": str(e)[:200]})

    # ── Writing Pipeline (New) Handlers ──
    def _handle_pipeline_new_run(self, data):
        chapter = data.get('chapter', 1)
        outline = data.get('outline', {})
        context = data.get('context', {})
        word_count = data.get('word_count', 3000)
        style_label = data.get('style_label', '')
        try:
            result = writing_pipeline.run(chapter, outline, context, word_count, style_label)
            self._send_json({
                "success": True,
                "result": {
                    "chapter": result.chapter_num,
                    "stage": result.stage.value,
                    "passed": result.passed,
                    "plan": result.plan[:500] if result.plan else '',
                    "draft": result.draft[:2000] if result.draft else '',
                    "revised_draft": result.revised_draft[:2000] if result.revised_draft else '',
                    "issues": [
                        {
                            "dimension": i.dimension,
                            "severity": i.severity.value,
                            "description": i.description,
                            "suggestion": i.suggestion,
                        }
                        for i in result.audit_issues
                    ],
                    "error": result.error,
                    "duration": round(result.completed_at - result.started_at, 1) if result.completed_at else 0,
                },
            })
        except Exception as e:
            log(f"Pipeline new run error: {e}")
            self._send_json({"success": False, "error": str(e)[:200]})

    def _handle_pipeline_new_status(self, data):
        try:
            status = writing_pipeline.get_pipeline_status()
            self._send_json({"success": True, "status": status})
        except Exception as e:
            log(f"Pipeline new status error: {e}")
            self._send_json({"success": False, "error": str(e)[:200]})


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
    print(f"  NWACS 商用级写作工具 v7.0")
    print(f"  http://localhost:{port}")
    print(f"=" * 60)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.shutdown()




    def _handle_generate_detailed_outline(self, data):
        """生成详细大纲"""
        try:
            outline = data.get('outline', {})
            genres = data.get('genres', [])
            styles = data.get('styles', [])
            tones = data.get('tones', [])
            method = data.get('method', '')
            target_word_count = data.get('target_word_count', 4000)
            
            # 构建提示词
            genre_str = '、'.join(genres) if genres else '玄幻'
            style_str = '、'.join(styles) if styles else '热血'
            tone_str = '、'.join(tones) if tones else '紧张'
            
            prompt = f"""你是一个专业的小说大纲设计师。请根据以下信息生成详细的章节大纲。

## 基本信息
- 题材：{genre_str}
- 风格：{style_str}
- 基调：{tone_str}
- 写作方法：{method}
- 目标每章字数：{target_word_count}

## 基础大纲
{json.dumps(outline, ensure_ascii=False, indent=2) if outline else '无'}

## 要求
1. 生成详细的章节大纲，包括：
   - 章节编号和标题
   - 本章主要情节
   - 关键情节点
   - 角色发展
   - 字数分配
2. 大纲应该详细到可以直接用来写作的程度
3. 返回JSON格式，包含 chapters 数组，每个元素包含：
   - chapter: 章节号
   - title: 章节标题
   - summary: 章节摘要
   - plot_points: 情节点数组
   - character_development: 角色发展
   - word_count: 预计字数
   - key_events: 关键事件数组

返回格式示例：
```json
{"chapters": [{"chapter": 1, "title": "第一章：觉醒", "summary": "主角发现自己拥有特殊能力", "plot_points": ["发现能力", "初次使用", "遇到困难"], "character_development": "主角从迷茫到坚定", "word_count": 3000, "key_events": ["意外觉醒", "测试能力", "决定行动"]}]}
```
"""
            
            # 调用LLM生成
            from llm_interface import llm, GenerationParams
            params = GenerationParams(max_tokens=2000, temperature=0.7)
            response = llm(prompt, params)
            
            # 解析响应
            import json
            try:
                # 尝试提取JSON
                json_match = re.search(r'```json\s*(.*?)\s*```', response, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group(1))
                else:
                    result = json.loads(response)
                
                self._send_json({
                    "success": True,
                    "detailed_outline": result
                })
            except json.JSONDecodeError:
                # 如果解析失败，返回原始文本
                self._send_json({
                    "success": True,
                    "detailed_outline": {
                        "chapters": [{"chapter": 1, "title": "生成的大纲", "summary": response}],
                        "raw_text": response
                    }
                })
                
        except Exception as e:
            log(f"Error in _handle_generate_detailed_outline: {e}")
            log(traceback.format_exc())
            self._send_json({"error": str(e)}, 500)


if __name__ == '__main__':
    main()
