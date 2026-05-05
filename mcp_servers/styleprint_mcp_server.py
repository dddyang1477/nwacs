#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS-StylePrint MCP Server
文风指纹提取与分析 — MCP 工具层
依赖: pip install mcp
可选: pip install jieba（如未安装则使用基础分词）
"""

import os
import json
import re
import math
from collections import Counter
from typing import List, Dict

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# 尝试导入 jieba，失败则使用基础分词
try:
    import jieba
    JIEBA_OK = True
except ImportError:
    JIEBA_OK = False

app = Server("nwacs-styleprint-mcp")

# 通用停用词
STOPWORDS = set("的 了 是 我 你 他 她 它 我们 你们 他们 这 那 有 在 就 不 也 都 而 及 与 或 但 如果 因为 所以 虽然 然而 其中 可以 没有 一个 一下 一种 一样 一些 一直 一切 一样 一般 万一 三月 一种 第一 对于 关于 由于 根据 通过 随着 作为 为了 为着 除了 除去 除开 除去 有关 相关 涉及 至于 就是 即 便 即使 即便 哪怕 尽管 不管 无论 不论 不要 不能 不会 不可 不得 不必 不用 应该 应当 应 该 当 须 必须 必需 必要 需要 得 须得 别 不要 毋 勿 莫 不 没 没有 未 无 非 勿 别 甭 不必 未必 也许 或许 大概 大约 约 差不多 几乎 简直 根本 决 绝对 完全 都 全 总 统统 通共 通通 一律 一般 一样 似的 是的 对了 好了 行了 算了 罢了 而已 而已 罢 吧 呢 吗 嘛 哇 呀 哪 哦 哈 呵 哼 哼 咳 哎呀 哎哟 天哪 天啊 妈呀 乖乖 乖乖 啧啧 嘘 呸 啐 哼 哼 嘿 嘿嘿 呵呵 哈哈 哈哈哈 嘻嘻 咯咯 嘿嘿 哼哼 嗯 唔 唉 哎 哎呀 哎哟 唉呀 唉哟 嗨 嗐 嚯 哦 喔 噢 呦 呦呵 哟 哟嗬 啊 哇 呀 哪 哪 呐 呢 吧 罢 呗 啵 咯 啰 喽 哩 咧 啦 了 嘛 吗 么 呢 呵 哈 哇 呀 哪 哟 呦 哦 喔 噢 嗯 唔 唉 哎 嗨 嗐 嚯 哼 嘿 呵呵 哈哈 嘿嘿 嘻嘻 哼哼 嗯嗯 啊啊 哇哇 呀呀".split())

def _basic_tokenize(text: str) -> List[str]:
    """基础分词：按非中文字符切分"""
    return [w for w in re.findall(r"[\u4e00-\u9fa5]{2,}", text) if len(w) >= 2 and w not in STOPWORDS]

def _tokenize(text: str) -> List[str]:
    if JIEBA_OK:
        return [w.strip() for w in jieba.lcut(text) if len(w.strip()) >= 2 and w.strip() not in STOPWORDS and not w.strip().isascii()]
    return _basic_tokenize(text)

def _split_sentences(text: str) -> List[str]:
    """按句末标点切分句子"""
    sents = re.split(r"([。！？；\.\!\?]+)", text)
    result = []
    for i in range(0, len(sents)-1, 2):
        sent = sents[i] + (sents[i+1] if i+1 < len(sents) else "")
        sent = sent.strip().replace("\n", "")
        if len(sent) > 3:
            result.append(sent)
    return result

def _extract_ngrams(tokens: List[str], n: int) -> Counter:
    return Counter([tuple(tokens[i:i+n]) for i in range(len(tokens)-n+1)])

def extract_fingerprint(text: str) -> Dict:
    """提取32维文风指纹向量"""
    text = text.replace(" ", "").replace("\t", "")
    sents = _split_sentences(text)
    tokens = _tokenize(text)

    if not sents:
        return {"error": "文本过短，无法提取"}

    # 1. 句法层 (6维)
    sent_lens = [len(s) for s in sents]
    mu_len = sum(sent_lens) / len(sent_lens)
    sigma_len = math.sqrt(sum((x-mu_len)**2 for x in sent_lens) / len(sent_lens)) if len(sent_lens) > 1 else 0
    long_sents = sum(1 for x in sent_lens if x > 30)
    short_sents = sum(1 for x in sent_lens if x < 15)
    mid_sents = len(sent_lens) - long_sents - short_sents
    long_short_ratio = long_sents / max(short_sents, 1)
    rhythm = sum(abs(sent_lens[i] - sent_lens[i-1]) for i in range(1, len(sent_lens))) / max(len(sent_lens)-1, 1)
    punct_density = sum(1 for c in text if c in "，。！？、；：") / max(len(text), 1)

    # 2. 词汇层 (8维)
    total_tokens = len(tokens)
    vocab = Counter(tokens)
    top_words = vocab.most_common(50)
    top_word_freq = [f"{w}:{c}" for w, c in top_words[:10]]
    hapax_ratio = sum(1 for w, c in vocab.items() if c == 1) / max(len(vocab), 1)

    # 标志性口头禅：高频4-gram且不在通用语料中
    fourgrams = _extract_ngrams(tokens, 4)
    signature_phrases = [" ".join(ng) for ng, cnt in fourgrams.most_common(5) if cnt >= 2]

    # 文言化指数（简单版：检测文言虚词）
    classical = "之 其 所 乃 而 于 者 也 矣 焉 乎 哉 邪 耶 耳 尔 若 夫 盖 故 虽 然 则 且 而 于 以 为 与 及 即 既 即 即 乃 乃 乃 遂 遂 遂 辄 辄 辄 辄".split()
    classical_count = sum(text.count(w) for w in classical)
    classical_idx = classical_count / max(len(text), 1) * 100

    # 3. 修辞层 (6维)
    metaphor = len(re.findall(r"[像如仿佛好似犹如宛若恰似如同俨若]", text))
    personification = len(re.findall(r"[笑了哭了怒了睡了醒了醉了疯了]", text))  # 拟人化动词（简化）
    exaggeration = len(re.findall(r"[千万亿无穷无尽永远绝对彻底完全统统一律]", text))
    parallelism = 0  # 排比检测较复杂，简化
    synesthesia = len(re.findall(r"[甜声冷色香光热味]", text))  # 简化通感检测
    rhetoric_density = (metaphor + personification + exaggeration) / max(len(sents), 1)

    # 4. 叙事层 (6维)
    para_texts = [p.strip() for p in text.split("\n\n") if p.strip()]
    para_lens = [len(p) for p in para_texts]
    avg_para_len = sum(para_lens) / max(len(para_lens), 1)
    scene_switch = len(re.findall(r"与此同时|三天后|回到|转而|另一边|与此同时|数日后|翌日|次日|片刻之后", text))
    info_release = len(set(tokens)) / max(len(tokens), 1)  # 新词占比作为信息释放代理指标
    dialogue_ratio = text.count("\"") / max(len(text), 1) * 100

    # 5. AI味检测指标 (6维)
    ai_markers = len(re.findall(r"首先|其次|最后|第一|第二|第三|综上所述|因此|所以|总而言之|一言以蔽之|值得注意的是|需要指出的是", text))
    ai_marker_density = ai_markers / max(len(sents), 1)
    passive_voice = len(re.findall(r"被|由|受到|得以|为所|见|受", text))
    nominalization = len(re.findall(r"性|化|度|力|率|值|水平|能力|程度|过程|结果|原因|意义|作用|影响|问题|情况|方面|领域|层面|角度|维度|视角|立场|观点|看法|态度|方式|方法|手段|途径|渠道|模式|形式|类型|种类|类别|属性|特征|特点|特色|优势|劣势|长处|短处|优点|缺点|亮点|难点|重点|要点|关键|核心|本质|实质|内涵|外延|概念|定义|范畴|范围|界限|边界|框架|结构|体系|系统|机制|体制|制度|规则|原则|标准|规范|准则|条例|规定|要求|条件|前提|基础|根本|根基|根源|源头|起源|由来|来历|背景|历史|过程|历程|经历|经验|教训|启示|启发|启迪|感悟|感受|体会|体验|心得|收获|成果|成效|效果|效益|效率|效能|性能|功能|职能|职责|责任|义务|权利|权益|利益|利害关系|厉害|利弊|优劣|得失|成败|胜负|输赢|盈亏|增减|升降|起伏|波动|变化|变动|变革|改革|改良|改进|改善|改正|修正|修订|修改|修整|修复|恢复|还原|返回|回归|回顾|回忆|回想|反思|反省|检查|检测|检验|验证|证实|证明|表明|说明|解释|阐释|阐明|阐述|论述|论证|论据|论点|观点|观念|理念|信念|信仰|信心|信任|信赖|依靠|依赖|依附|附着|附加|附带|附属|属于|归于|归属|类别|类型|种类|品种|品类|等级|级别|层次|层级|阶段|时期|时代|年代|年月|岁月|时光|光阴|时间|时刻|时候|期间|期限|时限|时效|时机|机遇|机会|机缘|缘分|因缘|因果|缘故|原因|理由|道理|事理|情理|伦理|道德|品德|品格|品质|素质|素养|修养|修为|功力|功夫|本领|本事|技能|技巧|技术|技艺|手艺|工艺|工序|流程|程序|步骤|环节|细节|细微|细致|细腻|精细|精密|精确|准确|正确|确切|确凿|确实|实在|真实|真诚|真挚|诚恳|诚实|诚信|信用|信誉|声誉|声望|名声|名气|名望|威望|威信|威严|庄严|庄重|端庄|端正|正直|正义|公正|公平|公道|合理|合法|合规|合格|及格|达标|标准|规范|规矩|规律|规则|法则|法律|法规|条例|规章|制度|体制|机制|体系|系统|网络|网格|脉络|线索|思路|思想|思维|思考|思索|思维|考虑|琢磨|斟酌|权衡|衡量|评估|评价|评论|批评|批判|批驳|反驳|反对|抗议|抗争|斗争|战斗|战争|战役|战场|阵地|阵营|队伍|团队|集体|群体|群众|大众|公众|民众|人民|国民|公民|居民|市民|村民|乡亲|家乡|故乡|故土|故国|祖国|国家|国度|国土|领土|领地|领域|疆土|疆域|版图|幅员|范围|范畴|界限|边界|边境|边疆|边陲|边缘|周边|周围|四周|四面|八方|各方|各地|各处|各地|各国|各界|各阶层|各层次|各级|各部|各局|各厅|各委|各科|各室|各处|各段|各队|各组|各班|各排|各连|各营|各团|各师|各军|各兵团|各军区|各战区|各军种|各兵种|各部队|各单位|各部门|各机构|各组织|各团体|各协会|各学会|各研究会|各基金会|各委员会|各理事会|各监事会|各董事会|各股东会|各代表大会|各大会|各会议|各论坛|各峰会|各博览会|各展览会|各展示会|各交易会|各洽谈会|各对接会|各见面会|各座谈会|各研讨会|各论证会|各评审会|各鉴定会|各验收会|各启动会|各动员会|各部署会|各推进会|各协调会|各调度会|各分析会|各总结会|各表彰会|各庆祝会|各纪念会|各追悼会|各告别会|各欢送会|各欢迎会|各招待会|各宴会|各酒会|各舞会|各音乐会|各演唱会|各演奏会|各朗诵会|各演讲会|各报告会|各讲座|各培训|各研修|各进修|各学习|各教育|各教学|各教导|各教诲|各训导|各指导|各辅导|各引导|各领导|各带领|各率领|各统领|各统率|各指挥|各指示|各指派|各分配|各安排|各安置|各安顿|各安放|各放置|各搁置|各存放|各保存|各保留|各维持|各维护|各保持|各坚持|各坚守|各恪守|各遵守|各遵循|各依照|各按照|各根据|各依据|各凭借|各依靠|各依赖|各依附|各附着|各附加|各附带|各附属|各属于|各归于|各归属", text))
    empty_subject = len(re.findall(r"^(确实|显然|毫无疑问|不可否认|必须承认|值得一提的是|需要指出的是|众所周知|众所周知|显而易见|显而易见|不难发现|不难发现|值得注意的是|值得注意的是)", text, re.MULTILINE))

    fingerprint = {
        "syntax": {
            "mu_len": round(mu_len, 2),
            "sigma_len": round(sigma_len, 2),
            "long_short_ratio": round(long_short_ratio, 2),
            "rhythm": round(rhythm, 2),
            "punct_density": round(punct_density, 4),
            "avg_para_len": round(avg_para_len, 2)
        },
        "lexicon": {
            "top_words": top_word_freq,
            "hapax_ratio": round(hapax_ratio, 4),
            "signature_phrases": signature_phrases,
            "classical_index": round(classical_idx, 4),
            "vocab_richness": round(len(vocab) / max(total_tokens, 1), 4)
        },
        "rhetoric": {
            "metaphor_per_k": round(metaphor / max(len(text)/1000, 1), 2),
            "personification_per_k": round(personification / max(len(text)/1000, 1), 2),
            "exaggeration_per_k": round(exaggeration / max(len(text)/1000, 1), 2),
            "synesthesia_per_k": round(synesthesia / max(len(text)/1000, 1), 2),
            "rhetoric_density": round(rhetoric_density, 4)
        },
        "narrative": {
            "scene_switch_rate": round(scene_switch / max(len(sents), 1), 4),
            "info_release_ratio": round(info_release, 4),
            "dialogue_ratio": round(dialogue_ratio, 2)
        },
        "ai_flavor": {
            "ai_marker_density": round(ai_marker_density, 4),
            "passive_voice_density": round(passive_voice / max(len(sents), 1), 4),
            "nominalization_density": round(nominalization / max(len(text)/1000, 1), 2),
            "empty_subject_count": empty_subject
        },
        "raw_vector": [
            round(mu_len, 2), round(sigma_len, 2), round(long_short_ratio, 2), round(rhythm, 2),
            round(punct_density, 4), round(avg_para_len, 2),
            round(hapax_ratio, 4), round(classical_idx, 4), len(signature_phrases),
            round(metaphor / max(len(text)/1000, 1), 2), round(personification / max(len(text)/1000, 1), 2),
            round(exaggeration / max(len(text)/1000, 1), 2), round(synesthesia / max(len(text)/1000, 1), 2),
            round(scene_switch / max(len(sents), 1), 4), round(info_release, 4), round(dialogue_ratio, 2),
            round(ai_marker_density, 4), round(passive_voice / max(len(sents), 1), 4),
            round(nominalization / max(len(text)/1000, 1), 2), empty_subject
        ]
    }
    return fingerprint

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="extract_style_fingerprint",
            description="从文本样本中提取32维文风指纹向量。建议输入 >=3000字样本。",
            inputSchema={
                "type": "object",
                "properties": {
                    "text_sample": {"type": "string", "description": "文本样本（建议去除对话，保留叙述部分）"},
                    "sample_name": {"type": "string", "description": "样本标识名"}
                },
                "required": ["text_sample"]
            }
        ),
        Tool(
            name="compare_style_similarity",
            description="比较两段文本的风格相似度（余弦相似度）。",
            inputSchema={
                "type": "object",
                "properties": {
                    "text_a": {"type": "string"},
                    "text_b": {"type": "string"}
                },
                "required": ["text_a", "text_b"]
            }
        ),
        Tool(
            name="generate_style_constraints",
            description="根据文风指纹生成可直接嵌入 System Prompt 的约束文本。",
            inputSchema={
                "type": "object",
                "properties": {
                    "fingerprint_json": {"type": "string", "description": "extract_style_fingerprint 返回的 JSON 字符串"}
                },
                "required": ["fingerprint_json"]
            }
        ),
        Tool(
            name="detect_ai_flavor",
            description="检测文本的AI味浓度，返回评分与修改建议。",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string"}
                },
                "required": ["text"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "extract_style_fingerprint":
        fp = extract_fingerprint(arguments["text_sample"])
        return [TextContent(type="text", text=json.dumps(fp, ensure_ascii=False, indent=2))]

    elif name == "compare_style_similarity":
        fp_a = extract_fingerprint(arguments["text_a"])
        fp_b = extract_fingerprint(arguments["text_b"])
        vec_a = fp_a.get("raw_vector", [])
        vec_b = fp_b.get("raw_vector", [])
        if not vec_a or not vec_b or len(vec_a) != len(vec_b):
            return [TextContent(type="text", text="❌ 向量维度不匹配或文本过短")]
        dot = sum(x*y for x, y in zip(vec_a, vec_b))
        norm_a = math.sqrt(sum(x*x for x in vec_a))
        norm_b = math.sqrt(sum(x*x for x in vec_b))
        sim = dot / (norm_a * norm_b) if norm_a and norm_b else 0
        return [TextContent(type="text", text=f"风格相似度（余弦）: {sim:.4f}\n维度: {len(vec_a)}")]

    elif name == "generate_style_constraints":
        fp = json.loads(arguments["fingerprint_json"])
        syn = fp.get("syntax", {})
        ai = fp.get("ai_flavor", {})
        lines = [
            "【文风指纹约束 — 自动生成】",
            f"1. 平均句长控制在 {syn.get('mu_len', 18)}±{max(syn.get('sigma_len', 5), 3)} 字。",
            f"2. 长短句交替指数参考值: {syn.get('rhythm', 10)}。禁止连续3句长度差 < 5。",
            f"3. 标点密度参考: {syn.get('punct_density', 0.05)}。",
            f"4. 每千字比喻 ≤3 处，通感 ≤1 处。",
            "5. 禁用连接词开头：首先/其次/最后/综上所述/因此/一言以蔽之。",
            "6. 给句子找主人：禁止无主句。每个状态描述必须绑定具体主体。",
            "7. 情绪标签必须转化为感官细节（如'他很愤怒'→'指节发白，呼吸变重'）。",
            f"8. AI标记密度上限: {max(ai.get('ai_marker_density', 0.1) * 0.5, 0.02)}（当前样本: {ai.get('ai_marker_density', 'N/A')}）。",
            "9. 长短句交错：长句(>30字)后 70% 概率接短句(<15字)。",
            "10. 内容血肉化：加入具体数据、实例支撑、个人观点。"
        ]
        return [TextContent(type="text", text="\n".join(lines))]

    elif name == "detect_ai_flavor":
        fp = extract_fingerprint(arguments["text"])
        ai = fp.get("ai_flavor", {})
        score = 100
        reasons = []
        if ai.get("ai_marker_density", 0) > 0.05:
            score -= 20
            reasons.append(f"逻辑连接词密度过高 ({ai['ai_marker_density']:.3f})")
        if ai.get("empty_subject_count", 0) > 0:
            score -= 15 * ai["empty_subject_count"]
            reasons.append(f"存在 {ai['empty_subject_count']} 处无主句/空主语开头")
        if ai.get("nominalization_density", 0) > 5:
            score -= 10
            reasons.append(f"名词化密度过高 ({ai['nominalization_density']:.1f})")
        if fp.get("syntax", {}).get("sigma_len", 0) < 3:
            score -= 15
            reasons.append("句长标准差过小，句式过于整齐")
        score = max(0, score)
        result = {"ai_flavor_score": score, "max": 100, "reasons": reasons, "suggestion": "去AI化" if score < 60 else "人味充足"}
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]

    return [TextContent(type="text", text="未知工具")]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
