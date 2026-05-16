"""
去AI痕迹引擎 v5.0
==================

顶尖写作工具的核心模块，实现：
1. 文风模仿引擎（金庸/古龙/网文大神）
2. 句式多样化引擎
3. 情感具象化引擎
4. 人性化处理模块
5. 实时AI痕迹检测与改写

作者: NWACS优化团队
版本: v5.0
日期: 2026-05-14
"""

import re
import json
from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum


class StyleType(Enum):
    """文风类型"""
    JIN_YONG = "jin_yong"      # 金庸风格
    GU_LONG = "gu_long"          # 古龙风格
    WANG_WEN = "wang_wen"      # 网文大神风格
    USER = "user"                # 用户自定义风格


@dataclass
class AIDetectionResult:
    """AI痕迹检测结果"""
    sentence_template_score: int    # 句式模板化分数
    emotion_label_score: int       # 情绪标签化分数
    rhetoric_ai_score: int        # 修辞AI味分数
    logic_perfect_score: int      # 逻辑过于完美分数
    vocab_diversity_score: int    # 词汇多样性分数
    total_score: int              # 综合分数
    issues: List[Dict]           # 检测到的问题列表


@dataclass
class StyleFeature:
    """文风特征"""
    name: str
    sentence_structures: List[str]
    emotion_expressions: List[str]
    dialog_styles: List[str]
    example_before: str
    example_after: str


class StyleLibrary:
    """文风库"""
    
    def __init__(self):
        self.styles = {}
        self._load_styles()
    
    def _load_styles(self):
        """加载文风特征库"""
        # 金庸风格
        self.styles[StyleType.JIN_YONG] = StyleFeature(
            name="金庸风格",
            sentence_structures=[
                "多用四字短语：'月光如水，清风徐来'",
                "古风词汇：'当下'、'须知'、'却说'",
                "心理描写细腻：'他心中一凛，暗道：...'"
            ],
            emotion_expressions=[
                "间接表达：'他沉默良久，缓缓点头'",
                "动作暗示：'他拳头紧握，指节发白'"
            ],
            dialog_styles=[
                "古白话：'足下'、'在下'、'阁下'",
                "诗词引用：适时引用古诗词"
            ],
            example_before="他很生气，决定报复。",
            example_after="他心中怒火中烧，暗道：'此仇不报，誓不为人！'"
        )
        
        # 古龙风格
        self.styles[StyleType.GU_LONG] = StyleFeature(
            name="古龙风格",
            sentence_structures=[
                "短句为主：'风吹过。他站在那里。'",
                "意境优先：'夜色如墨，杀意如霜'",
                "留白艺术：'他知道，有些事必须做。'"
            ],
            emotion_expressions=[
                "极简表达：'他笑了。笑容比哭还难看。'",
                "环境烘托：'风很冷，就像他的心。'"
            ],
            dialog_styles=[
                "极简短对话：'你来了。' '我来了。'",
                "哲理化对白：'每个人都有自己的剑。'"
            ],
            example_before="他感到非常悲伤，眼泪流了下来。",
            example_after="他抬起头。夜空很暗。眼泪，不知不觉就流了下来。"
        )
        
        # 网文大神风格（会说话的肘子）
        self.styles[StyleType.WANG_WEN] = StyleFeature(
            name="网文大神风格",
            sentence_structures=[
                "短句为主，节奏快",
                "口语化强，接地气",
                "吐槽式内心独白"
            ],
            emotion_expressions=[
                "幽默化解紧张：'系统您大爷的'",
                "反差萌：强大实力+逗比性格"
            ],
            dialog_styles=[
                "现代口语：'卧槽！'、'牛逼！'",
                "内心吐槽：'这特么也能行？'"
            ],
            example_before="他非常惊讶，不敢相信眼前的事实。",
            example_after="他整个人都傻了。卧槽？这特么也能行？"
        )
    
    def get_style(self, style_type: StyleType) -> StyleFeature:
        """获取指定文风的特征"""
        return self.styles.get(style_type)
    
    def apply_style(self, text: str, style_type: StyleType) -> str:
        """应用文风转换"""
        # 这里是简化实现，实际需要更复杂的NLP处理
        style = self.get_style(style_type)
        if not style:
            return text
        
        # 示例：根据文风特征进行简单替换
        if style_type == StyleType.JIN_YONG:
            # 金庸风格：添加古风词汇
            text = re.sub(r'说道', '道', text)
            text = re.sub(r'非常', '甚是', text)
        elif style_type == StyleType.GU_LONG:
            # 古龙风格：短句化
            text = re.sub(r'，', '。', text)
        elif style_type == StyleType.WANG_WEN:
            # 网文风格：口语化
            text = re.sub(r'感到惊讶', '傻了', text)
        
        return text


class AIPhraseDetector:
    """AI短语检测器"""
    
    # AI常用短语库
    AI_PHRASSES = [
        "首先", "其次", "最后",
        "总的来说", "综上所述",
        "值得注意的是", "需要指出的是",
        "毫无疑问", "显然",
        "确实如此", "毋庸置疑"
    ]
    
    def __init__(self):
        self.ai_phrase_pattern = re.compile('|'.join(self.AI_PHRASSES))
    
    def detect(self, text: str) -> List[Dict]:
        """检测AI常用短语"""
        issues = []
        for phrase in self.AI_PHRASES:
            positions = [m.start() for m in re.finditer(phrase, text)]
            for pos in positions:
                issues.append({
                    "type": "ai_phrase",
                    "phrase": phrase,
                    "position": pos,
                    "suggestion": f"删除或替换AI常用短语'{phrase}'"
                })
        return issues


class EmotionConcretizer:
    """情感具象化器"""
    
    # 情感标签到具象化表达的映射
    EMOTION_MAP = {
        "愤怒": [
            "他拳头紧握，指节发白",
            "他眼中闪过一丝寒芒",
            "他咬了咬牙，脸色阴沉"
        ],
        "悲伤": [
            "她低下头，久久不语",
            "她的声音有些哽咽",
            "她转过身，不想让他看到脸上的泪"
        ],
        "紧张": [
            "他的喉结上下滚动了一下",
            "他下意识地握紧了拳头",
            "他的后背渗出了一层细密的汗"
        ],
        "高兴": [
            "他嘴角忍不住上扬",
            "他眼中闪过一丝喜色",
            "他忍不住哈哈大笑起来"
        ],
        "害怕": [
            "他不由自主地后退了一步",
            "他的声音有些发颤",
            "他的瞳孔猛地收缩"
        ]
    }
    
    def concretize(self, text: str) -> Tuple[str, List[Dict]]:
        """
        将情感标签转换为具象化表达
        
        Returns:
            修改后的文本，修改记录
        """
        issues = []
        
        for emotion, expressions in self.EMOTION_MAP.items():
            # 检测"他很XX"模式
            pattern = f"他很{emotion}|她很{emotion}"
            matches = list(re.finditer(pattern, text))
            
            for match in reversed(matches):  # 反向遍历，避免位置偏移
                start = match.start()
                end = match.end()
                
                # 随机选择一个具象化表达
                import random
                replacement = random.choice(expressions)
                
                text = text[:start] + replacement + text[end:]
                issues.append({
                    "type": "emotion_abstraction",
                    "original": match.group(),
                    "replacement": replacement,
                    "position": start
                })
        
        return text, issues


class SentenceDiversifier:
    """句式多样化器"""
    
    def __init__(self):
        self.sentence_endings = ["。", "！", "？"]
    
    def diversify(self, text: str) -> Tuple[str, List[Dict]]:
        """
        使句式多样化
        
        策略：
        1. 长短句交替
        2. 主动被动交替
        3. 疑问句/感叹句/陈述句混合
        """
        issues = []
        sentences = re.split('([。！？])', text)
        
        # 分析句子长度
        for i in range(0, len(sentences) - 1, 2):
            if i + 1 < len(sentences):
                sentence = sentences[i]
                punctuation = sentences[i + 1]
                
                # 检测过长的句子（>50字）
                if len(sentence) > 50:
                    # 建议拆分
                    issues.append({
                        "type": "sentence_too_long",
                        "sentence": sentence,
                        "position": text.find(sentence),
                        "suggestion": "句子过长，建议拆分为2-3个短句"
                    })
        
        return text, issues


class DeAIEngineV5:
    """去AI痕迹引擎 v5.0"""
    
    def __init__(self):
        self.style_library = StyleLibrary()
        self.ai_phrase_detector = AIPhraseDetector()
        self.emotion_concretizer = EmotionConcretizer()
        self.sentence_diversifier = SentenceDiversifier()
    
    def process(self, text: str, target_style: StyleType = StyleType.USER) -> Dict:
        """
        处理文本，去除AI痕迹
        
        Args:
            text: 待处理文本
            target_style: 目标文风
        
        Returns:
            {
                "optimized_text": "优化后文本",
                "ai_score_before": 45,
                "ai_score_after": 88,
                "changes": [...],  # 具体修改点
                "emotion_resonance_score": 92  # 情感共鸣度
            }
        """
        changes = []
        
        # Step 1: 检测AI痕迹（优化前）
        ai_report_before = self.detect_ai_traces(text)
        
        # Step 2: 文风转换
        styled_text = self.style_library.apply_style(text, target_style)
        if styled_text != text:
            changes.append({
                "type": "style_conversion",
                "description": f"应用{self.style_library.get_style(target_style).name}转换"
            })
        
        # Step 3: 情感具象化
        emotional_text, emotion_issues = self.emotion_concretizer.concretize(styled_text)
        changes.extend(emotion_issues)
        
        # Step 4: 句式多样化
        diversified_text, sentence_issues = self.sentence_diversifier.diversify(emotional_text)
        changes.extend(sentence_issues)
        
        # Step 5: 后验AI分数（优化后）
        ai_report_after = self.detect_ai_traces(diversified_text)
        
        # Step 6: 计算情感共鸣度
        emotion_resonance_score = self._calculate_emotion_resonance(diversified_text)
        
        return {
            "optimized_text": diversified_text,
            "ai_score_before": ai_report_before.total_score,
            "ai_score_after": ai_report_after.total_score,
            "changes": changes,
            "emotion_resonance_score": emotion_resonance_score
        }
    
    def detect_ai_traces(self, text: str) -> AIDetectionResult:
        """检测AI痕迹"""
        issues = []
        
        # 1. 句式模板化检测
        sentence_template_score = self._detect_sentence_templates(text)
        
        # 2. 情绪标签化检测
        emotion_label_score = self._detect_emotion_labels(text)
        
        # 3. 修辞AI味检测
        rhetoric_ai_score = self._detect_ai_rhetoric(text)
        
        # 4. 逻辑过于完美检测
        logic_perfect_score = self._detect_too_perfect_logic(text)
        
        # 5. 词汇多样性检测
        vocab_diversity_score = self._detect_vocab_repetition(text)
        
        # 综合分数计算（分数越高，AI痕迹越少）
        total_score = int(
            (sentence_template_score + emotion_label_score + 
             rhetoric_ai_score + logic_perfect_score + 
             vocab_diversity_score) / 5
        )
        
        # 收集所有问题
        issues.extend(self.ai_phrase_detector.detect(text))
        
        return AIDetectionResult(
            sentence_template_score=sentence_template_score,
            emotion_label_score=emotion_label_score,
            rhetoric_ai_score= rhetoric_ai_score,
            logic_perfect_score=logic_perfect_score,
            vocab_diversity_score=vocab_diversity_score,
            total_score=total_score,
            issues=issues
        )
    
    def _detect_sentence_templates(self, text: str) -> int:
        """检测句式模板化（返回分数0-100，越高越好）"""
        score = 100
        
        # 检测"首先...其次...最后"结构
        if "首先" in text and "其次" in text:
            score -= 30
        
        # 检测连续3句以上结构相似
        sentences = re.split('[。！？]', text)
        if len(sentences) >= 3:
            # 简化：检测句子长度相似度
            lengths = [len(s) for s in sentences[:10] if s.strip()]
            if len(lengths) >= 3:
                avg_len = sum(lengths) / len(lengths)
                similar_count = sum(1 for l in lengths if abs(l - avg_len) < 5)
                if similar_count >= 3:
                    score -= 25
        
        return max(0, score)
    
    def _detect_emotion_labels(self, text: str) -> int:
        """检测情绪标签化（返回分数0-100）"""
        score = 100
        
        # 检测直接情绪标签
        emotion_labels = ["愤怒", "悲伤", "高兴", "紧张", "害怕", "惊讶"]
        for label in emotion_labels:
            if f"他很{label}" in text or f"她很{label}" in text:
                score -= 20
        
        return max(0, score)
    
    def _detect_ai_rhetoric(self, text: str) -> int:
        """检测修辞AI味（返回分数0-100）"""
        score = 100
        
        # 检测过多比喻（每千字>5处）
        metaphor_count = len(re.findall(r'如同|好像|仿佛|就像', text))
        word_count = len(text)
        if word_count > 0:
            metaphor_density = (metaphor_count / word_count) * 1000
            if metaphor_density > 5:
                score -= 30
        
        return max(0, score)
    
    def _detect_too_perfect_logic(self, text: str) -> int:
        """检测逻辑过于完美（返回分数0-100）"""
        score = 100
        
        # 人类写作会有小瑕疵，AI写作过于完美
        # 简化检测：缺少口语化表达、省略、语气词等
        oral_markers = ["吧", "呢", "啊", "嗯", "呃"]
        has_oral = any(marker in text for marker in oral_markers)
        if not has_oral:
            score -= 15
        
        return max(0, score)
    
    def _detect_vocab_repetition(self, text: str) -> int:
        """检测词汇重复（返回分数0-100）"""
        score = 100
        
        # 检测高频词
        words = re.findall(r'[\w]+', text)
        if len(words) > 0:
            from collections import Counter
            word_counts = Counter(words)
            most_common = word_counts.most_common(5)
            
            for word, count in most_common:
                if len(word) > 1 and count > len(words) * 0.05:  # 某个词占比>5%
                    score -= 10
        
        return max(0, score)
    
    def _calculate_emotion_resonance(self, text: str) -> int:
        """计算情感共鸣度（返回分数0-100）"""
        score = 50  # 基础分
        
        # 检测感官细节
        sensory_words = ["看到", "听到", "闻到", "摸到", "感到"]
        for word in sensory_words:
            if word in text:
                score += 5
        
        # 检测具象化情感表达
        for emotion, _ in self.emotion_concretizer.EMOTION_MAP.items():
            if emotion in text:
                score -= 5  # 抽象情感标签
            else:
                # 检测是否有具象化表达（简化）
                if any(char in text for char in ["拳", "泪", "笑", "牙"]):
                    score += 10
        
        return min(100, max(0, score))


# ══════════════════ 测试函数 ══════════════════

def test_de_ai_engine():
    """测试去AI痕迹引擎"""
    engine = DeAIEngineV5()
    
    # 测试用例
    test_text = """
    首先，他很愤怒，决定要报复。其次，他开始制定计划。
    这个房间很暗，他走进去。他感到非常紧张，手心出汗。
    他的动作如同行云流水一般。毫无疑问，他是一个高手。
    """
    
    print("══════════════════════════════════════")
    print("测试去AI痕迹引擎 v5.0")
    print("══════════════════════════════════════\n")
    
    # 检测AI痕迹
    print("【检测前】")
    result_before = engine.detect_ai_traces(test_text)
    print(f"综合AI分数: {result_before.total_score}/100")
    print(f"  - 句式模板化: {result_before.sentence_template_score}")
    print(f"  - 情绪标签化: {result_before.emotion_label_score}")
    print(f"  - 修辞AI味: {result_before.rhetoric_ai_score}")
    print(f"  - 逻辑完美度: {result_before.logic_perfect_score}")
    print(f"  - 词汇多样性: {result_before.vocab_diversity_score}")
    print(f"检测到的问题数: {len(result_before.issues)}")
    
    # 处理文本
    print("\n【处理中...】")
    result = engine.process(test_text, target_style=StyleType.JIN_YONG)
    
    print("\n【处理完成】")
    print(f"AI分数提升: {result['ai_score_before']} → {result['ai_score_after']}")
    print(f"情感共鸣度: {result['emotion_resonance_score']}/100")
    print(f"修改次数: {len(result['changes'])}")
    print(f"\n优化前文本:\n{test_text}")
    print(f"\n优化后文本:\n{result['optimized_text']}")
    
    return result


if __name__ == "__main__":
    test_de_ai_engine()
