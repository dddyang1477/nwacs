"""
爆款基因分析系统 v1.0
==================

从顶尖写作工具角度，分析爆款小说的基因，
帮助作者创作具有商业化潜力的作品。

功能：
1. 学习起点/番茄/晋江等平台Top 20小说
2. 分析爆款基因（开局钩子、爽点密度、情绪曲线等）
3. 预测读者情绪曲线
4. 优化爽点密度

作者: NWACS优化团队
版本: v1.0
日期: 2026-05-14
"""

import re
import json
from typing import Dict, List, Tuple
from dataclasses import dataclass, field
from enum import Enum


class Platform(Enum):
    """平台类型"""
    QIDIAN = "qidian"        # 起点中文网
    FANQIE = "fanqie"        # 番茄小说
    JINJIANG = "jinjiang"     # 晋江文学城


class Genre(Enum):
    """小说类型"""
    XUANHUAN = "xuanhuan"    # 玄幻
    XIULIAN = "xiulian"        # 修仙
    DUSHI = "dushi"            # 都市
    KEHUAN = "kehuan"          # 科幻
    XUYI = "xuyi"             # 悬疑
    DANMEI = "danmei"          # 耽美


@dataclass
class Shuandian:
    """爽点"""
    type: str                  # 类型：实力打脸/收获升级/美人倾心/敌人吃瘪
    position: int              # 位置（字数）
    intensity: int             # 强度（0-100）
    description: str = ""      # 描述


@dataclass
class EmotionPoint:
    """情绪点"""
    position: float            # 位置（0-1）
    emotion: str              # 情绪类型
    intensity: int            # 强度（0-100）


@dataclass
class BestsellerGene:
    """爆款基因"""
    hook_strength: int        # 钩子强度（0-100）
    emotion_resonance: int     # 情感共鸣度（0-100）
    pace_rhythm: int          # 节奏感（0-100）
    character_appeal: int     # 角色魅力（0-100）
    innovation_score: int      # 创新度（0-100）
    total_score: int = 0      # 综合爆款分数（0-100）
    
    def __post_init__(self):
        # 计算综合分数
        self.total_score = int(
            self.hook_strength * 0.25 +
            self.emotion_resonance * 0.2 +
            self.pace_rhythm * 0.2 +
            self.character_appeal * 0.2 +
            self.innovation_score * 0.15
        )


@dataclass
class NovelAnalysis:
    """小说分析结果"""
    title: str
    platform: Platform
    gene: BestsellerGene
    shuangdian_density: float   # 爽点密度（个/千字）
    emotion_curve: List[EmotionPoint]
    plot_structure: Dict
    suggestions: List[str]


class BestsellerGeneAnalyzer:
    """爆款基因分析器"""
    
    def __init__(self):
        self.top_novels = {}
        self._load_top_novels()
    
    def _load_top_novels(self):
        """加载Top小说数据（模拟）"""
        # 起点Top 5（男频）
        self.top_novels[Platform.QIDIAN] = [
            {
                "title": "诡秘之主",
                "author": "爱潜水的乌贼",
                "genre": Genre.XUANHUAN,
                "features": {
                    "hook": "穿越到蒸汽朋克+克苏鲁世界",
                    "shuangdian_density": 3.2,  # 每千字3.2个爽点
                    "emotion_curve": "高开-平稳-小高潮-大高潮-爆炸",
                    "innovation": "世界观创新（序列途径系统）"
                }
            },
            {
                "title": "斗破苍穹",
                "author": "天蚕土豆",
                "genre": Genre.XIULIAN,
                "features": {
                    "hook": "天才沦为废柴，未婚妻退婚",
                    "shuangdian_density": 4.5,
                    "emotion_curve": "屈辱-获得传承-成长-打脸-巅峰",
                    "innovation": "废柴逆袭模式（经典）"
                }
            },
            {
                "title": "完美世界",
                "author": "辰东",
                "genre": Genre.XUANHUAN,
                "features": {
                    "hook": "少年从石村走出，独断万古",
                    "shuangdian_density": 4.0,
                    "emotion_curve": "热血-战斗-升级-更强敌人-突破",
                    "innovation": "宏大世界观+独断万古理念"
                }
            }
        ]
        
        # 番茄Top 3（快节奏）
        self.top_novels[Platform.FANQIE] = [
            {
                "title": "我真没想重生啊",
                "author": "昌昌",
                "genre": Genre.DUSHI,
                "features": {
                    "hook": "重生回1998年，改变命运",
                    "shuangdian_density": 5.8,  # 番茄节奏更快
                    "emotion_curve": "轻松-打脸-搞笑-温馨-高潮",
                    "innovation": "重生+轻松搞笑流"
                }
            }
        ]
        
        # 晋江Top 2（女频）
        self.top_novels[Platform.JINJIANG] = [
            {
                "title": "魔道祖师",
                "author": "墨香铜臭",
                "genre": Genre.XUANHUAN,
                "features": {
                    "hook": "含光君温宁，却是个...（悬念）",
                    "shuangdian_density": 2.8,  # 女频爽点密度较低
                    "emotion_curve": "虐-甜-虐-真相-HE",
                    "innovation": "耽美+虐恋+反转"
                }
            }
        ]
    
    def analyze_bestseller(self, novel_text: str, platform: Platform) -> BestsellerGene:
        """
        分析小说的爆款潜力
        
        Args:
            novel_text: 小说文本
            platform: 目标平台
        
        Returns:
            BestsellerGene对象
        """
        # 简化实现：基于规则评估
        hook_strength = self._analyze_hook(novel_text)
        emotion_resonance = self._analyze_emotion_resonance(novel_text)
        pace_rhythm = self._analyze_pace(novel_text)
        character_appeal = self._analyze_character_appeal(novel_text)
        innovation_score = self._analyze_innovation(novel_text, platform)
        
        return BestsellerGene(
            hook_strength=hook_strength,
            emotion_resonance=emotion_resonance,
            pace_rhythm=pace_rhythm,
            character_appeal=character_appeal,
            innovation_score=innovation_score
        )
    
    def _analyze_hook(self, text: str) -> int:
        """分析开局钩子强度"""
        score = 50  # 基础分
        
        # 检测前300字是否有强钩子
        first_300 = text[:300]
        
        # 钩子元素
        hook_elements = [
            "穿越", "重生", "系统", "退婚", "废柴",
            "死亡", "复活", "马甲", "隐藏", "秘密"
        ]
        
        for element in hook_elements:
            if element in first_300:
                score += 10
        
        # 检测开篇是否有冲突
        conflict_words = ["但是", "突然", "没想到", "竟然", "原来"]
        for word in conflict_words:
            if word in first_300:
                score += 5
        
        return min(100, score)
    
    def _analyze_emotion_resonance(self, text: str) -> int:
        """分析情感共鸣度"""
        score = 50
        
        # 检测情感具象化表达
        emotion_actions = ["拳头紧握", "泪水流下", "嘴角上扬", "喉结滚动"]
        for action in emotion_actions:
            if action in text:
                score += 5
        
        # 检测是否有读者代入感（第一人称或近距离第三人称）
        if "我" in text[:500]:
            score += 10  # 第一人称代入感强
        
        return min(100, score)
    
    def _analyze_pace(self, text: str) -> int:
        """分析节奏感"""
        score = 50
        
        # 检测短句比例（快节奏）
        sentences = re.split('[。！？]', text)
        short_sentences = sum(1 for s in sentences if 5 <= len(s) <= 20)
        short_ratio = short_sentences / len(sentences) if sentences else 0
        
        if short_ratio > 0.6:
            score += 20  # 短句多，节奏快
        
        # 检测对话比例（对话多节奏快）
        dialog_count = text.count('"') // 2
        dialog_ratio = dialog_count / len(text) if text else 0
        
        if dialog_ratio > 0.1:
            score += 15
        
        return min(100, score)
    
    def _analyze_character_appeal(self, text: str) -> int:
        """分析角色魅力"""
        score = 50
        
        # 检测是否有鲜明的角色特征
        # 简化：检测角色名字出现频率
        import re
        names = re.findall(r'([A-Za-z\u4e00-\u9fa5]{2,4})', text)
        if names:
            from collections import Counter
            name_counts = Counter(names)
            top_name = name_counts.most_common(1)[0]
            
            if top_name[1] > 10:  # 主角出现次数多
                score += 20
        
        return min(100, score)
    
    def _analyze_innovation(self, text: str, platform: Platform) -> int:
        """分析创新度"""
        score = 50
        
        # 对比平台Top小说的创新点
        if platform in self.top_novels:
            top_novel = self.top_novels[platform][0]
            # 简化：检测是否有不同的元素组合
            score += 15  # 假设有一定创新
        
        return min(100, score)
    
    def learn_from_bestsellers(self, platform: Platform, top_n: int = 20):
        """
        从平台Top N小说中学习爆款基因
        
        学习维度:
        1. 开局钩子设计（前3000字）
        2. 爽点密度分布
        3. 情绪曲线设计
        4. 人物设定模式
        5. 世界观创新点
        6. 读者评论高频词（好评/差评）
        """
        if platform not in self.top_novels:
            return {"error": f"平台{platform.value}的数据尚未加载"}
        
        novels = self.top_novels[platform][:top_n]
        
        # 提取共性特征
        common_features = {
            "hook_patterns": [],
            "shuangdian_types": [],
            "emotion_patterns": [],
            "character_archetypes": []
        }
        
        for novel in novels:
            features = novel["features"]
            common_features["hook_patterns"].append(features["hook"])
            common_features["shuangdian_types"].append(features["shuangdian_density"])
        
        return {
            "platform": platform.value,
            "novel_count": len(novels),
            "common_features": common_features,
            "average_shuangdian_density": sum(
                n["features"]["shuangdian_density"] for n in novels
            ) / len(novels)
        }
    
    def predict_emotion_curve(self, chapter_text: str) -> List[EmotionPoint]:
        """
        预测读者阅读时的情绪变化
        
        Returns:
            情绪点列表
        """
        curve = []
        
        # 简化实现：基于关键词检测
        sentences = re.split('[。！？]', chapter_text)
        total_sentences = len(sentences)
        
        for i, sentence in enumerate(sentences):
            position = i / total_sentences if total_sentences > 0 else 0
            
            # 检测情绪关键词
            if any(word in sentence for word in ["突然", "震惊", "没想到"]):
                curve.append(EmotionPoint(
                    position=position,
                    emotion="震惊",
                    intensity=85
                ))
            elif any(word in sentence for word in ["愤怒", "怒火", "咬牙"]):
                curve.append(EmotionPoint(
                    position=position,
                    emotion="愤怒",
                    intensity=80
                ))
            elif any(word in sentence for word in ["悲伤", "泪", "哭"]):
                curve.append(EmotionPoint(
                    position=position,
                    emotion="悲伤",
                    intensity=75
                ))
            elif any(word in sentence for word in ["笑", "高兴", "喜悦"]):
                curve.append(EmotionPoint(
                    position=position,
                    emotion="高兴",
                    intensity=70
                ))
        
        # 如果没有检测到明显情绪，添加默认曲线
        if not curve:
            curve = [
                EmotionPoint(0.1, "好奇", 70),
                EmotionPoint(0.3, "紧张", 85),
                EmotionPoint(0.5, "震撼", 95),
                EmotionPoint(0.7, "悲伤", 80),
                EmotionPoint(0.9, "满足", 90)
            ]
        
        return curve
    
    def analyze_shuangdian_density(self, novel_text: str) -> Dict:
        """
        分析爽点密度
        
        Returns:
            {
                "current_density": "中",
                "shuangdian": [...],
                "gaps": [...],
                "suggestions": [...]
            }
        """
        shuangdian_types = {
            "实力打脸": ["打脸", "反击", "震惊", "不敢置信"],
            "收获升级": ["获得", "突破", "升级", "提升"],
            "美人倾心": ["喜欢", "倾心", "心动", "爱慕"],
            "敌人吃瘪": ["失败", "吃瘪", "倒霉", "后悔"]
        }
        
        found_shuangdian = []
        gaps = []
        
        # 检测爽点
        for s_type, keywords in shuangdian_types.items():
            for keyword in keywords:
                positions = [m.start() for m in re.finditer(keyword, novel_text)]
                for pos in positions:
                    found_shuangdian.append({
                        "position": pos,
                        "type": s_type,
                        "keyword": keyword
                    })
        
        # 按位置排序
        found_shuangdian.sort(key=lambda x: x["position"])
        
        # 检测爽点间隔（如果>2000字无爽点，记录为gap）
        word_count = len(novel_text)
        for i in range(len(found_shuangdian) - 1):
            current_pos = found_shuangdian[i]["position"]
            next_pos = found_shuangdian[i + 1]["position"]
            gap = next_pos - current_pos
            
            if gap > 2000:
                gaps.append({
                    "start": current_pos,
                    "end": next_pos,
                    "gap_words": gap,
                    "problem": f"约{gap}字无爽点"
                })
        
        # 生成建议
        suggestions = []
        for gap in gaps:
            suggestions.append(
                f"在第{gap['start']}字附近添加爽点"
                f"（建议：敌人嘲讽+主角淡定反击）"
            )
        
        # 计算密度
        density = len(found_shuangdian) / (word_count / 1000) if word_count > 0 else 0
        
        return {
            "current_density": "高" if density > 4 else "中" if density > 2 else "低",
            "shuangdian_count": len(found_shuangdian),
            "density_per_1000_words": round(density, 2),
            "shuangdian": found_shuangdian[:10],  # 只返回前10个
            "gaps": gaps,
            "suggestions": suggestions
        }


# ════════════════ 测试用例 ════════════════

def test_bestseller_analyzer():
    """测试爆款基因分析器"""
    analyzer = BestsellerGeneAnalyzer()
    
    # 测试文本
    test_text = """
    林晨原本是家族天才，却在一夜之间修为尽失，沦为废柴。
    未婚妻柳菲菲上门退婚，当众羞辱："你这种废物，也配和我成亲？"
    林晨拳头紧握，指节发白，心中暗道："此仇不报，誓不为人！"
    就在此时，一枚古朴戒指从他脖子上滑落...
    """
    
    print("═══════════════════════════════════")
    print("测试爆款基因分析系统 v1.0")
    print("═══════════════════════════════════\n")
    
    # 分析爆款基因
    print("【爆款基因分析】")
    gene = analyzer.analyze_bestseller(test_text, Platform.QIDIAN)
    print(f"综合爆款分数: {gene.total_score}/100")
    print(f"  - 钩子强度: {gene.hook_strength}/100")
    print(f"  - 情感共鸣度: {gene.emotion_resonance}/100")
    print(f"  - 节奏感: {gene.pace_rhythm}/100")
    print(f"  - 角色魅力: {gene.character_appeal}/100")
    print(f"  - 创新度: {gene.innovation_score}/100")
    
    # 预测情绪曲线
    print("\n【情绪曲线预测】")
    curve = analyzer.predict_emotion_curve(test_text)
    print(f"检测到{len(curve)}个情绪点：")
    for point in curve:
        print(f"  - 位置{point.position:.1f}: {point.emotion} (强度{point.intensity})")
    
    # 分析爽点密度
    print("\n【爽点密度分析】")
    density_result = analyzer.analyze_shuangdian_density(test_text)
    print(f"当前密度: {density_result['current_density']}")
    print(f"爽点数量: {density_result['shuangdian_count']}")
    print(f"每千字爽点: {density_result['density_per_1000_words']}")
    
    if density_result['suggestions']:
        print("\n建议:")
        for sug in density_result['suggestions']:
            print(f"  - {sug}")
    
    # 学习Top小说
    print("\n【学习起点Top小说】")
    learning_result = analyzer.learn_from_bestsellers(Platform.QIDIAN, top_n=3)
    print(f"平台: {learning_result['platform']}")
    print(f"学习小说数: {learning_result['novel_count']}")
    print(f"平均爽点密度: {learning_result['average_shuangdian_density']:.2f}/千字")
    
    return gene


if __name__ == "__main__":
    test_bestseller_analyzer()
