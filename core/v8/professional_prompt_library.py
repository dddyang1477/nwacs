#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS V8.6 专业写作提示词模板系统
参考: 蛙蛙写作5000+工作流, 笔灵AI 300+生成器

核心功能:
- 专业写作提示词模板库
- 多场景写作工作流
- 爆款拆解提示词
- 黄金开头生成器
- 剧情发展提示词库
"""

import os
import json
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import random


class WritingGenre(Enum):
    XUANHUAN = "xuanhuan"
    YANQING = "yanqing"
    DUSHI = "dushi"
    LINGYI = "lingyi"
    XIANxia = "xianxia"
    KEHUN = "kehuan"
    ZHENTAN = "zhentan"
    TONGSU = "tongsu"


class WritingScene(Enum):
    OPENING = "opening"
    BATTLE = "battle"
    ROMANCE = "romance"
    DAILY = "daily"
    HORROR = "horror"
    REVELATION = "revelation"
    CLIMAX = "climax"
    ENDING = "ending"


@dataclass
class PromptTemplate:
    """提示词模板"""
    template_id: str
    name: str
    genre: WritingGenre
    scene: WritingScene
    description: str
    prompt_template: str
    keywords: List[str]
    effectiveness: float = 0.8


class ProfessionalPromptLibrary:
    """专业写作提示词库"""

    def __init__(self):
        self.templates: Dict[str, PromptTemplate] = {}
        self.genres = {}
        self._load_builtin_templates()

    def _load_builtin_templates(self):
        """加载内置模板"""
        self.templates = {
            "xuanhuan_opening_golden": PromptTemplate(
                template_id="xuanhuan_opening_golden",
                name="玄幻黄金开头",
                genre=WritingGenre.XUANHUAN,
                scene=WritingScene.OPENING,
                description="生成玄幻小说黄金开头，包含悬念和世界观",
                prompt_template="""你是顶级玄幻小说作家。请根据以下设定创作一个{word_count}字的黄金开头。

设定：
- 世界观：{world_setting}
- 主角：{protagonist}，性格：{personality}
- 核心冲突：{core_conflict}
- 金手指：{cheat}

要求：
1. 开头300字必须出现核心悬念
2. 世界观要新颖独特
3. 主角性格要鲜明
4. 埋下至少一个伏笔
5. 结尾要有钩子，吸引读者继续阅读
6. 文笔要精彩，节奏要快

请开始创作：""",
                keywords=["黄金开头", "玄幻", "悬念", "世界观", "伏笔"],
                effectiveness=0.95
            ),
            "xuanhuan_battle_enhance": PromptTemplate(
                template_id="xuanhuan_battle_enhance",
                name="玄幻战斗增强",
                genre=WritingGenre.XUANHUAN,
                scene=WritingScene.BATTLE,
                description="增强玄幻战斗场景的描写",
                prompt_template="""你是资深玄幻作家，精通战斗场景描写。请增强以下战斗段落：

原文：
{original_text}

场景设定：
- 战斗双方：{combatants}
- 境界等级：{realm}
- 功法技能：{technique}
- 战斗目的：{purpose}

增强要求：
1. 从视觉、听觉、触觉多维度描写
2. 战斗节奏要紧凑
3. 体现境界压制感
4. 招式名称要有新意
5. 战斗心理要到位
6. 战斗结果要合理

请输出增强后的版本：""",
                keywords=["战斗", "打斗", "功法", "境界", "对决"],
                effectiveness=0.92
            ),
            "yanqing_romance_emotion": PromptTemplate(
                template_id="yanqing_romance_emotion",
                name="言情情感互动",
                genre=WritingGenre.YANQING,
                scene=WritingScene.ROMANCE,
                description="增强言情小说的情感互动",
                prompt_template="""你是资深言情作家，擅长情感描写。请创作一段{word_count}字的情感互动场景。

人物设定：
- 男主：{male_lead}，性格：{male_personality}
- 女主：{female_lead}，性格：{female_personality}
- 当前关系：{relationship}

场景设定：
{scene_setting}

情感基调：{emotion_tone}

要求：
1. 情感细腻动人
2. 肢体语言描写到位
3. 心理活动丰富
4. 对话符合人物性格
5. 暧昧氛围营造
6. 留下情感钩子

请创作：""",
                keywords=["言情", "情感", "暧昧", "心动", "互动"],
                effectiveness=0.93
            ),
            "plot_branch_generation": PromptTemplate(
                template_id="plot_branch_generation",
                name="剧情分支生成",
                genre=WritingGenre.XUANHUAN,
                scene=WritingScene.REVELATION,
                description="参考彩云小梦三条剧情分支",
                prompt_template="""你是专业剧情设计师。请根据当前剧情生成3条不同走向的剧情分支。

当前剧情：
{current_plot}

主角状态：
{protagonist_status}

已铺垫的伏笔：
{foreshadows}

请生成3条剧情分支：

分支1：【意外转折】
- 走向描述：{branch1_desc}
- 冲突设计：{branch1_conflict}
- 预期字数：{branch1_words}

分支2：【高潮推进】
- 走向描述：{branch2_desc}
- 冲突设计：{branch2_conflict}
- 预期字数：{branch2_words}

分支3：【情感深化】
- 走向描述：{branch3_desc}
- 冲突设计：{branch3_conflict}
- 预期字数：{branch3_words}

每条分支需要：
1. 与前文逻辑连贯
2. 能回收伏笔
3. 留下新的悬念
4. 符合人物性格发展""",
                keywords=["剧情分支", "三条路线", "走向", "分支"],
                effectiveness=0.90
            ),
            "character_ooc_check": PromptTemplate(
                template_id="character_ooc_check",
                name="角色OOC检测",
                genre=WritingGenre.XUANHUAN,
                scene=WritingScene.DAILY,
                description="检测角色是否偏离设定(笔灵432特征值参考)",
                prompt_template="""你是严谨的角色一致性审核员。请检测以下内容是否存在OOC(角色脱离设定)问题。

角色设定档案：
{character_profile}

待检测内容：
{content_to_check}

请从以下432个特征维度检测：
1. 性格特质 (外放/内敛/双重等)
2. 行为模式 (果断/犹豫/冲动等)
3. 语言风格 (文雅/粗犷/幽默等)
4. 思维逻辑 (理性/感性/跳跃等)
5. 情感表达 (直接/含蓄/压抑等)
6. 价值观念 (正义/中立/邪恶等)

输出格式：
{{
    "ooc_detected": true/false,
    "violations": [
        {{
            "aspect": "维度",
            "expected": "应有表现",
            "actual": "实际表现",
            "severity": "严重程度"
        }}
    ],
    "suggestions": ["修改建议"]
}}""",
                keywords=["OOC检测", "角色一致性", "人设检测"],
                effectiveness=0.88
            ),
            "shooting_hook_ending": PromptTemplate(
                template_id="shooting_hook_ending",
                name="悬念钩子结尾",
                genre=WritingGenre.XUANHUAN,
                scene=WritingScene.ENDING,
                description="生成强悬念结尾吸引读者",
                prompt_template="""你是悬念大师，擅长制造追更钩子。请为当前章节创作一个{hook_type}结尾。

章节内容摘要：
{chapter_summary}

章节主题：{theme}
当前情绪：{emotion}

钩子类型可选：
1. 【突发事件】- 突然的危机或变故
2. 【身份谜团】- 揭示或新增悬念
3. 【情感冲击】- 强烈的情感转折
4. 【命运抉择】- 重大选择关头
5. 【伏笔回收】- 前文伏笔揭晓
6. 【戛然而止】- 最高潮时中断

要求：
1. 钩子要与章节主题呼应
2. 不能突兀，要水到渠成
3. 留下足够的想象空间
4. 让读者欲罢不能

请选择最佳钩子类型并创作：""",
                keywords=["钩子", "悬念", "结尾", "追更"],
                effectiveness=0.94
            ),
            "worldbuilding_complete": PromptTemplate(
                template_id="worldbuilding_complete",
                name="完整世界观构建",
                genre=WritingGenre.XUANHUAN,
                scene=WritingScene.OPENING,
                description="参考彩云小梦世界设定系统",
                prompt_template="""你是顶级世界观架构师。请构建一个完整的{genre}世界观。

作品名称：{novel_name}
题材风格：{genre}
核心主题：{theme}

请从以下维度构建：

1. 【天地规则】
   - 修炼体系：{cultivation_system}
   - 等级设定：{realm_levels}
   - 力量来源：{power_source}

2. 【地理构造】
   - 主要势力分布：{forces}
   - 禁地险境：{forbidden_areas}
   - 资源产出：{resources}

3. 【社会结构】
   - 王朝宗门：{sects}
   - 阶层划分：{hierarchy}
   - 生存法则：{survival_rules}

4. 【特殊设定】
   - 金手指系统：{cheat_system}
   - 特殊职业：{special_occupations}
   - 禁忌知识：{forbidden_knowledge}

5. 【伏笔埋线】
   - 终极悬念：{ultimate_mystery}
   - 长期伏笔：{long_term_foreshadow}
   - 草蛇灰线：{subtle_foreshadow}

要求：
1. 世界观要自洽完整
2. 要有独特亮点
3. 要服务于剧情
4. 要有扩展空间

请详细构建：""",
                keywords=["世界观", "架构", "设定", "体系"],
                effectiveness=0.91
            ),
            "peak_cramping": PromptTemplate(
                template_id="peak_cramping",
                name="爽点密集设计",
                genre=WritingGenre.XUANHUAN,
                scene=WritingScene.CLIMAX,
                description="设计高密度爽点场景",
                prompt_template="""你是爽文写作大师，精通读者爽点设计。请设计一个高密度爽点场景。

场景背景：
{scene_background}

主角当前状态：
{protagonist_status}

反派/对手设定：
{antagonist_info}

爽点类型（可多选）：
1. 【打脸反杀】- 强势反击
2. 【天赋碾压】- 越级挑战
3. 【秘宝出世】- 获得机缘
4. 【势力扩张】- 收服强者
5. 【真相揭示】- 揭露阴谋
6. 【情感收获】- 美人倾心

设计要求：
1. 爽点要层层递进
2. 压抑要足够充分
3. 爆发要酣畅淋漓
4. 反派要足够可恨
5. 主角要足够帅气
6. 观众要能代入

请详细设计这个场景：""",
                keywords=["爽点", "打脸", "碾压", "爆发"],
                effectiveness=0.96
            ),
            "ai_style_removal": PromptTemplate(
                template_id="ai_style_removal",
                name="AI味去除",
                genre=WritingGenre.XUANHUAN,
                scene=WritingScene.DAILY,
                description="去除AI写作痕迹(去AI化)",
                prompt_template="""你是资深编辑，精通识别和去除AI写作痕迹。请修改以下文本，使其更像人类写作。

原文：
{original_text}

AI写作常见特征（需要去除）：
1. 过度使用"然而"、"因此"、"所以"等连接词
2. 句子结构过于规整
3. 情感表达过于直白或夸张
4. 细节描写过于面面俱到
5. 缺乏个人语言风格
6. 过渡段落过于平滑

修改要求：
1. 增加语言的个性化和变化
2. 增加适当的省略和跳跃
3. 增加生活化和口语化表达
4. 保留核心剧情和关键描写
5. 让文章更有"人气"

请输出修改后的版本：""",
                keywords=["去AI味", "AI痕迹", "人工味", "自然"],
                effectiveness=0.89
            ),
            "plot_tree_generation": PromptTemplate(
                template_id="plot_tree_generation",
                name="剧情树生成",
                genre=WritingGenre.XUANHUAN,
                scene=WritingScene.REVELATION,
                description="参考墨狐AI剧情树功能",
                prompt_template="""你是剧情架构师。请根据已有情节生成一个可视化的剧情树。

当前情节：
{current_plot}

已知角色：
{characters}

已埋设伏笔：
{foreshadows}

请生成剧情树结构：

主枝干（核心剧情）：
1. 第一关键节点：{node1}
   - 分支A：{branch_a}
   - 分支B：{branch_b}

2. 第二关键节点：{node2}
   - 分支A：{branch_c}
   - 分支B：{branch_d}

3. 第三关键节点：{node3}
   - 分支A：{branch_e}
   - 分支B：{branch_f}

每个节点需要标注：
- 预计章节位置
- 核心事件
- 情感变化
- 伏笔回收点

请生成完整的剧情树：""",
                keywords=["剧情树", "分支", "走向", "结构"],
                effectiveness=0.87
            )
        }

    def get_template(self, template_id: str) -> Optional[PromptTemplate]:
        """获取模板"""
        return self.templates.get(template_id)

    def render_template(self, template_id: str, **kwargs) -> str:
        """渲染模板"""
        template = self.get_template(template_id)
        if not template:
            return ""

        try:
            return template.prompt_template.format(**kwargs)
        except KeyError as e:
            return f"模板渲染错误：缺少参数 {e}"

    def search_templates(self, query: str, genre: WritingGenre = None,
                        scene: WritingScene = None) -> List[PromptTemplate]:
        """搜索模板"""
        results = []
        query_lower = query.lower()

        for template in self.templates.values():
            if genre and template.genre != genre:
                continue
            if scene and template.scene != scene:
                continue

            score = 0
            if query_lower in template.name.lower():
                score += 2
            if query_lower in template.description.lower():
                score += 1
            if any(query_lower in kw.lower() for kw in template.keywords):
                score += 1

            if score > 0:
                results.append((template, score))

        results.sort(key=lambda x: x[1], reverse=True)
        return [t for t, _ in results]

    def get_genre_templates(self, genre: WritingGenre) -> List[PromptTemplate]:
        """获取指定题材的所有模板"""
        return [t for t in self.templates.values() if t.genre == genre]

    def get_scene_templates(self, scene: WritingScene) -> List[PromptTemplate]:
        """获取指定场景的所有模板"""
        return [t for t in self.templates.values() if t.scene == scene]

    def get_all_template_ids(self) -> List[str]:
        """获取所有模板ID"""
        return list(self.templates.keys())

    def generate_random_prompt(self, genre: WritingGenre = None,
                               scene: WritingScene = None) -> str:
        """生成随机提示词"""
        templates = self.templates.values()

        if genre:
            templates = [t for t in templates if t.genre == genre]
        if scene:
            templates = [t for t in templates if t.scene == scene]

        if not templates:
            return ""

        template = random.choice(list(templates))

        prompts = {
            "xuanhuan_opening_golden": {
                "word_count": "2000-3000",
                "world_setting": "一个以剑道为尊的修仙世界，百家宗门林立",
                "protagonist": "叶尘",
                "personality": "冷静沉稳，心思缜密",
                "core_conflict": "家族被灭，仇人追杀",
                "cheat": "能感知敌人弱点"
            },
            "xuanhuan_battle_enhance": {
                "original_text": "叶尘大喝一声，剑光闪烁，敌人应声倒下。",
                "combatants": "叶尘 vs 王浩",
                "realm": "筑基期 vs 筑基中期",
                "technique": "青云剑法 vs 烈火拳",
                "purpose": "争夺秘境机缘"
            },
            "yanqing_romance_emotion": {
                "word_count": "1500",
                "male_lead": "顾霆渊",
                "male_personality": "外冷内热，霸道总裁",
                "female_lead": "苏念",
                "female_personality": "独立坚强，聪慧可爱",
                "relationship": "欢喜冤家",
                "scene_setting": "深夜的办公室，她加班到很晚",
                "emotion_tone": "甜蜜中带点虐"
            }
        }

        params = prompts.get(template.template_id, {})
        return self.render_template(template.template_id, **params)


class WritingWorkflowEngine:
    """写作工作流引擎 - 参考蛙蛙写作5000+工作流"""

    def __init__(self):
        self.workflows: Dict[str, Dict] = {}
        self.prompt_library = ProfessionalPromptLibrary()
        self._load_builtin_workflows()

    def _load_builtin_workflows(self):
        """加载内置工作流"""
        self.workflows = {
            "xuanhuan_full_flow": {
                "name": "玄幻小说全流程",
                "description": "从灵感到完稿的完整流程",
                "steps": [
                    {"name": "灵感输入", "template": None, "output": "灵感描述"},
                    {"name": "世界观构建", "template": "worldbuilding_complete", "output": "完整世界观"},
                    {"name": "大纲生成", "template": None, "output": "小说大纲"},
                    {"name": "黄金开头", "template": "xuanhuan_opening_golden", "output": "开头章节"},
                    {"name": "章节续写", "template": "plot_branch_generation", "output": "章节内容"},
                    {"name": "战斗增强", "template": "xuanhuan_battle_enhance", "output": "增强内容"},
                    {"name": "OOC检测", "template": "character_ooc_check", "output": "检测报告"},
                    {"name": "结尾钩子", "template": "shooting_hook_ending", "output": "悬念结尾"}
                ]
            },
            "yanqing_full_flow": {
                "name": "言情小说全流程",
                "description": "言情小说创作完整流程",
                "steps": [
                    {"name": "人物设定", "template": None, "output": "角色档案"},
                    {"name": "关系设计", "template": None, "output": "关系图谱"},
                    {"name": "情感铺垫", "template": "yanqing_romance_emotion", "output": "情感场景"},
                    {"name": "冲突设计", "template": "plot_branch_generation", "output": "冲突分支"},
                    {"name": "误会设计", "template": None, "output": "误会场景"},
                    {"name": "和好设计", "template": None, "output": "和好场景"},
                    {"name": "结局设计", "template": "shooting_hook_ending", "output": "完美结局"}
                ]
            },
            "professional_edit_flow": {
                "name": "专业编辑审稿流程",
                "description": "参考笔灵AI编辑审稿标准",
                "steps": [
                    {"name": "节奏检测", "template": None, "output": "节奏分析"},
                    {"name": "爽点检测", "template": "peak_cramping", "output": "爽点报告"},
                    {"name": "OOC检测", "template": "character_ooc_check", "output": "一致性报告"},
                    {"name": "AI味去除", "template": "ai_style_removal", "output": "自然文本"},
                    {"name": "钩子检测", "template": "shooting_hook_ending", "output": "钩子评分"},
                    {"name": "综合评分", "template": None, "output": "审稿报告"}
                ]
            },
            "branch_story_flow": {
                "name": "分支剧情工作流",
                "description": "参考彩云小梦三条分支",
                "steps": [
                    {"name": "当前剧情分析", "template": None, "output": "剧情摘要"},
                    {"name": "分支1生成", "template": "plot_branch_generation", "output": "转折分支"},
                    {"name": "分支2生成", "template": "plot_branch_generation", "output": "高潮分支"},
                    {"name": "分支3生成", "template": "plot_branch_generation", "output": "情感分支"},
                    {"name": "剧情树生成", "template": "plot_tree_generation", "output": "可视化树"},
                    {"name": "分支选择", "template": None, "output": "选定分支"}
                ]
            }
        }

    def get_workflow(self, workflow_id: str) -> Optional[Dict]:
        """获取工作流"""
        return self.workflows.get(workflow_id)

    def list_workflows(self) -> List[Dict]:
        """列出所有工作流"""
        return [
            {"id": k, "name": v["name"], "description": v["description"]}
            for k, v in self.workflows.items()
        ]

    def execute_workflow(self, workflow_id: str,
                        context: Dict = None) -> List[Dict]:
        """执行工作流"""
        workflow = self.get_workflow(workflow_id)
        if not workflow:
            return []

        context = context or {}
        results = []

        for step in workflow["steps"]:
            result = {
                "step_name": step["name"],
                "output_key": step["output"],
                "status": "pending"
            }

            if step["template"]:
                rendered = self.prompt_library.render_template(
                    step["template"],
                    **context
                )
                result["prompt"] = rendered
                result["status"] = "ready_to_generate"
            else:
                result["status"] = "manual_input_needed"

            results.append(result)

        return results


def main():
    print("="*60)
    print("📚 NWACS V8.6 专业写作提示词系统")
    print("="*60)

    prompt_lib = ProfessionalPromptLibrary()
    workflow_engine = WritingWorkflowEngine()

    print(f"\n📊 提示词模板数量: {len(prompt_lib.get_all_template_ids())}")

    print("\n📋 可用模板:")
    for template_id in prompt_lib.get_all_template_ids()[:5]:
        template = prompt_lib.get_template(template_id)
        print(f"  • {template.name} [{template.genre.value}]")

    print("\n📋 可用工作流:")
    for wf in workflow_engine.list_workflows():
        print(f"  • {wf['name']}: {wf['description']}")

    print("\n" + "="*60)
    print("✅ 专业写作提示词系统就绪")
    print("="*60)


if __name__ == "__main__":
    main()