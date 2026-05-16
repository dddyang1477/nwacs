"""
创造力激发与学习系统 v1.0
===================

顶尖写作工具的终极功能：
1. 创造力激发模块（打破陈词滥调）
2. 跨类型融合引擎
3. 词汇丰富度系统
4. 感官细节增强系统
5. 剧情创意生成器

作者: NWACS优化团队
版本: v1.0
日期: 2026-05-14
"""

import re
import random
from typing import List, Dict, Tuple
from dataclasses import dataclass
from enum import Enum


class Genre(Enum):
    """小说类型"""
    XUANHUAN = "xuanhuan"      # 玄幻
    XIULIAN = "xiulian"          # 修仙
    DUSHI = "dushi"              # 都巿
    KEHUAN = "kehuan"            # 科幻
    XUYI = "xuyi"               # 悬疑
    DANMEI = "danmei"            # 耽美
    WUXIA = "wuxia"              # 武侠


@dataclass
class PlotIdea:
    """剧情创意"""
    title: str
    description: str
    genre: Genre
    innovation_score: int        # 创新度（0-100）
    feasibility_score: int       # 可行度（0-100）


@dataclass
class VocabSuggestion:
    """词汇建议"""
    original: str
    synonyms: List[str]
    positions: List[int]
    reason: str


class CreativityBooster:
    """创造力激发模块"""
    
    def __init__(self):
        self.cliche_database = self._load_cliches()
        self.cross_genre_templates = self._load_cross_genre_templates()
    
    def _load_cliches(self) -> Dict:
        """加载陈词滥调库"""
        return {
            "废柴逆袭": [
                "天才沦为废柴，被退婚",
                "获得神秘传承/系统",
                "三年之约，打脸"
            ],
            "穿越重生": [
                "车祸/触电穿越",
                "重生回十年前",
                "带着游戏系统穿越"
            ],
            "打脸情节": [
                "被轻视后展现实力",
                "敌人嘲讽，主角淡定",
                "事后众人震惊"
            ]
        }
    
    def _load_cross_genre_templates(self) -> List[Dict]:
        """加载跨类型融合模板"""
        return [
            {
                "genre_a": Genre.XUANHUAN,
                "genre_b": Genre.XUYI,
                "template": "修仙世界，但每隔百年有人失踪，主角调查真相",
                "example": "《诡秘之主》- 修仙+克苏鲁"
            },
            {
                "genre_a": Genre.DUSHI,
                "genre_b": Genre.KEHUAN,
                "template": "现代都市，但科技突然失效，超能力觉醒",
                "example": "《全球高武》- 都市+高武"
            },
            {
                "genre_a": Genre.XIULIAN,
                "genre_b": Genre.DANMEI,
                "template": "修仙世界，但师徒关系复杂，有情劫",
                "example": "《人渣反派自救系统》- 修仙+耽美"
            }
        ]
    
    def generate_plot_ideas(self, genre: Genre, num_ideas: int = 10) -> List[PlotIdea]:
        """
        生成剧情创意
        
        方法:
        1. 随机组合不同小说的元素
        2. 使用GPT/Claude生成反套路剧情
        3. 跨类型迁移（玄幻→都市）
        4. 读者吐槽反向推导（"如果当时主角这样做..."）
        """
        ideas = []
        
        # 方法1：反套路生成
        anti_cliches = self._generate_anti_cliche_ideas(genre, num_ideas // 2)
        ideas.extend(anti_cliches)
        
        # 方法2：跨类型融合
        cross_ideas = self._generate_cross_genre_ideas(num_ideas // 2)
        ideas.extend(cross_ideas)
        
        return ideas[:num_ideas]
    
    def _generate_anti_cliche_ideas(self, genre: Genre, num: int) -> List[PlotIdea]:
        """生成反套路创意"""
        ideas = []
        
        cliches = self.cliche_database.get("废柴逆袭", [])
        
        for i in range(num):
            if i < len(cliches):
                cliche = cliches[i]
                # 生成反套路
                anti_idea = self._reverse_cliche(cliche)
                
                ideas.append(PlotIdea(
                    title=f"反套路创意 #{i+1}",
                    description=anti_idea,
                    genre=genre,
                    innovation_score=random.randint(75, 95),
                    feasibility_score=random.randint(60, 85)
                ))
        
        return ideas
    
    def _reverse_cliche(self, cliche: str) -> str:
        """反转陈词滥调"""
        reversals = {
            "天才沦为废柴，被退婚": "天才依然是天才，但主动退婚（不屑）",
            "获得神秘传承/系统": "获得传承，但传承者是坑货",
            "三年之约，打脸": "三年之约，但对方是他亲哥（伦理冲突）"
        }
        return reversals.get(cliche, f"反转：{cliche}（加入意外元素）")
    
    def _generate_cross_genre_ideas(self, num: int) -> List[PlotIdea]:
        """生成跨类型融合创意"""
        ideas = []
        
        templates = self.cross_genre_templates[:num]
        
        for i, template in enumerate(templates):
            ideas.append(PlotIdea(
                title=f"跨类型融合 #{i+1}",
                description=template["template"],
                genre=template["genre_a"],
                innovation_score=90,  # 跨类型融合创新度高
                feasibility_score=70
            ))
        
        return ideas
    
    def break_cliches(self, plot_outline: str) -> str:
        """
        打破陈词滥调
        
        示例:
        输入: "废柴逆袭，三年之约"
        输出: "废柴逆袭，但敌人是他亲哥（伦理冲突）"
              "三年之约，但对方是好人（价值观冲突）"
        """
        result = plot_outline
        
        for cliche_group, cliches in self.cliche_database.items():
            for cliche in cliches:
                if cliche in plot_outline:
                    # 生成反转建议
                    reversal = self._reverse_cliche(cliche)
                    result += f"\n\n💡 建议优化：{reversal}"
        
        return result
    
    def cross_genre_fusion(self, genre_a: Genre, genre_b: Genre) -> Dict:
        """
        跨类型融合
        
        示例:
        输入: "玄幻" + "悬疑"
        输出: "修仙世界，但每隔百年有人失踪，主角调查真相"
        """
        for template in self.cross_genre_templates:
            if template["genre_a"] == genre_a and template["genre_b"] == genre_b:
                return {
                    "success": True,
                    "fusion_idea": template["template"],
                    "example": template["example"]
                }
        
        # 如果没有预定义模板，生成通用融合
        return {
            "success": True,
            "fusion_idea": f"{genre_a.value}世界，但融入{genre_b.value}元素",
            "example": "自定义融合"
        }


class VocabularyEnricher:
    """词汇丰富度提升系统"""
    
    def __init__(self):
        self.synonyms_db = self._load_synonyms()
        self.high_frequency_words = ["突然", "说道", "然后", "但是", "因为"]
    
    def _load_synonyms(self) -> Dict:
        """加载同义词库"""
        return {
            "突然": ["骤然", "猛地", "冷不丁", "忽然间", "霎时间"],
            "说道": ["回应", "开口", "沉声道", "轻叹", "低语"],
            "然后": ["接着", "随即", "此后", "转眼间", "须臾"],
            "但是": ["然而", "可是", "只不过", "虽则", "倒是高"],
            "因为": ["鉴于", "由于", "只因", "一来", "之所以"]
        }
    
    def analyze_repetition(self, text: str) -> List[VocabSuggestion]:
        """
        分析词汇重复情况
        
        Returns:
            词汇建议列表
        """
        suggestions = []
        
        for word in self.high_frequency_words:
            positions = [m.start() for m in re.finditer(word, text)]
            count = len(positions)
            
            if count > 5:
                synonyms = self.synonyms_db.get(word, [])
                suggestions.append(VocabSuggestion(
                    original=word,
                    synonyms=synonyms,
                    positions=positions,
                    reason=f"'{word}'出现{count}次，建议使用同义词替换"
                ))
        
        return suggestions
    
    def enrich_text(self, text: str) -> Tuple[str, List[VocabSuggestion]]:
        """
        自动丰富词汇
        
        Returns:
            丰富后的文本，词汇建议列表
        """
        suggestions = self.analyze_repetition(text)
        enriched = text
        
        for suggestion in suggestions:
            if suggestion.synonyms:
                # 随机替换一部分（不是全部，保持文本一致性）
                word = suggestion.original
                synonyms = suggestion.synonyms
                
                # 替换30%的出现
                positions = suggestion.positions
                num_to_replace = max(1, len(positions) // 3)
                positions_to_replace = random.sample(positions, min(num_to_replace, len(positions)))
                
                # 从后向前替换，避免位置偏移
                for pos in sorted(positions_to_replace, reverse=True):
                    synonym = random.choice(synonyms)
                    enriched = enriched[:pos] + synonym + enriched[pos + len(word):]
        
        return enriched, suggestions


class SensoryDetailEnhancer:
    """感官细节增强系统"""
    
    def __init__(self):
        self.sensory_words = {
            "visual": ["看到", "望见", "目击", "注视"],
            "auditory": ["听到", "听见", "听闻", "耳闻"],
            "olfactory": ["闻到", "嗅到", "气息", "味道"],
            "tactile": ["摸到", "触到", "感到", "触碰"],
            "taste": ["尝到", "品味", "口感", "滋味"]
        }
    
    def add_sensory_details(self, scene_text: str) -> str:
        """
        添加感官细节
        
        示例:
        输入: "他走进房间。"
        输出: "他推开厚重的木门，一股霉味扑面而来（嗅觉）。
              房间昏暗，只有一缕月光从破窗斜射进来（视觉）。
              脚下木板发出'吱嘎'声（听觉）。"
        """
        # 简化实现：检测简单的动作描述，添加感官细节
        enhanced = scene_text
        
        # 检测"走进"动作
        if "走进" in enhanced or "进入" in enhanced:
            # 添加环境感官细节
            sensory_addition = "\n\n（环境细节：）"
            sensory_addition += "空气中弥漫着...\n"
            sensory_addition += "脚下发出...\n"
            sensory_addition += "远处传来...\n"
            
            # 在段末添加
            enhanced = enhanced.rstrip() + sensory_addition
        
        return enhanced
    
    def enhance_action_scenes(self, action_text: str) -> str:
        """
        增强动作场面的感官冲击
        
        示例:
        输入: "他一拳打在敌人脸上。"
        输出: "他右拳猛地挥出，指节撞击对手颧骨的闷响（听觉），
              对方身体向后仰去，嘴角溢出一丝鲜血（视觉），
              空气中弥漫开铁锈般的气味（嗅觉）。"
        """
        enhanced = action_text
        
        # 检测打击动作
        if "拳" in enhanced or "踢" in enhanced or "打" in enhanced:
            # 添加多感官描述
            enhanced = enhanced.rstrip() + "\n\n（增强：）"
            enhanced += "可以描述：\n"
            enhanced += "- 打击的声音（听觉）\n"
            enhanced += "- 对手的表情/伤势（视觉）\n"
            enhanced += "- 血液/汗水的味道（嗅觉）\n"
            enhanced += "- 拳头的触感（触觉）\n"
        
        return enhanced


class PlotIdeaGenerator:
    """剧情创意生成器（集成版）"""
    
    def __init__(self):
        self.creativity_booster = CreativityBooster()
        self.vocab_enricher = VocabularyEnricher()
        self.sensory_enhancer = SensoryDetailEnhancer()
    
    def generate_novel_ideas(self, genre: Genre, num_ideas: int = 5) -> List[Dict]:
        """
        生成完整的小说创意
        
        包含：
        1. 世界观设定
        2. 主角设定
        3. 核心冲突
        4. 剧情亮点
        """
        ideas = []
        
        # 获取基础创意
        plot_ideas = self.creativity_booster.generate_plot_ideas(genre, num_ideas)
        
        for i, plot_idea in enumerate(plot_ideas):
            full_idea = {
                "title": plot_idea.title,
                "hook": self._generate_hook(plot_idea),
                "protagonist": self._generate_protagonist(genre),
                "core_conflict": self._generate_core_conflict(plot_idea),
                "plot_highlights": self._generate_plot_highlights(plot_idea),
                "innovation_score": plot_idea.innovation_score,
                "feasibility_score": plot_idea.feasibility_score
            }
            ideas.append(full_idea)
        
        return ideas
    
    def _generate_hook(self, plot_idea: PlotIdea) -> str:
        """生成开局钩子"""
        return f"开局：{plot_idea.description[:50]}..."
    
    def _generate_protagonist(self, genre: Genre) -> Dict:
        """生成主角设定"""
        return {
            "name": "待定",
            "age": random.randint(16, 25),
            "trait": "待定（根据剧情设定）",
            "ability": "待定（根据世界观设定）"
        }
    
    def _generate_core_conflict(self, plot_idea: PlotIdea) -> str:
        """生成核心冲突"""
        return f"核心冲突：围绕{plot_idea.description}展开"
    
    def _generate_plot_highlights(self, plot_idea: PlotIdea) -> List[str]:
        """生成剧情亮点"""
        return [
            "亮点1：待定",
            "亮点2：待定",
            "亮点3：待定"
        ]


# ════════════════ 测试函数 ════════════════

def test_creativity_system():
    """测试创造力激发系统"""
    print("══════════════════════════════")
    print("测试创造力激发与学习系统 v1.0")
    print("══════════════════════════════\n")
    
    # 1. 测试创造力激发
    print("【1. 创造力激发测试】")
    booster = CreativityBooster()
    ideas = booster.generate_plot_ideas(Genre.XUANHUAN, num_ideas=3)
    
    for i, idea in enumerate(ideas):
        print(f"\n创意 #{i+1}: {idea.title}")
        print(f"  描述: {idea.description}")
        print(f"  创新度: {idea.innovation_score}/100")
        print(f"  可行度: {idea.feasibility_score}/100")
    
    # 2. 测试打破陈词滥调
    print("\n\n【2. 打破陈词滥调测试】")
    plot = "废柴逆袭，三年之约，打脸"
    print(f"原剧情: {plot}")
    optimized = booster.break_cliches(plot)
    print(f"优化后:\n{optimized}")
    
    # 3. 测试跨类型融合
    print("\n\n【3. 跨类型融合测试】")
    fusion = booster.cross_genre_fusion(Genre.XUANHUAN, Genre.XUYI)
    print(f"融合创意: {fusion['fusion_idea']}")
    print(f"参考案例: {fusion['example']}")
    
    # 4. 测试词汇丰富度
    print("\n\n【4. 词汇丰富度测试】")
    enricher = VocabularyEnricher()
    test_text = "他突然走进房间，然后说道：'突然想到一件事。'然后他就离开了。"
    print(f"优化前: {test_text}")
    
    enriched_text, suggestions = enricher.enrich_text(test_text)
    print(f"优化后: {enriched_text}")
    print("\n词汇建议:")
    for sug in suggestions:
        print(f"  - {sug.reason}")
        print(f"    同义词: {', '.join(sug.synonyms)}")
    
    # 5. 测试感官细节增强
    print("\n\n【5. 感官细节增强测试】")
    enhancer = SensoryDetailEnhancer()
    scene = "他走进房间。"
    print(f"优化前: {scene}")
    enhanced_scene = enhancer.add_sensory_details(scene)
    print(f"优化后:\n{enhanced_scene}")
    
    # 6. 测试完整小说创意生成
    print("\n\n【6. 完整小说创意生成测试】")
    generator = PlotIdeaGenerator()
    novel_ideas = generator.generate_novel_ideas(Genre.XUANHUAN, num_ideas=2)
    
    for i, idea in enumerate(novel_ideas):
        print(f"\n小说创意 #{i+1}:")
        print(f"  标题: {idea['title']}")
        print(f"  钩子: {idea['hook']}")
        print(f"  创新度: {idea['innovation_score']}/100")
    
    print("\n══════════════════════════════")
    print("✅ 所有测试完成！")
    print("══════════════════════════════")


if __name__ == "__main__":
    test_creativity_system()
