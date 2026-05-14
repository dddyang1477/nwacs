#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""验证P0级新模块"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

print("=" * 60)
print("P0级新模块验证")
print("=" * 60)

print("\n[1] ModelRouter — 多模型协同路由...")
from model_router import ModelRouter, TaskType, ModelProvider, ModelConfig
router = ModelRouter()
router.register_model(ModelConfig(
    provider=ModelProvider.DEEPSEEK,
    model_name="deepseek-chat",
    api_key=os.environ.get("DEEPSEEK_API_KEY", "test-key"),
    api_base="https://api.deepseek.com/v1",
))
stats = router.get_stats()
health = router.health_check()
print(f"  已注册模型: {len(router.models)}")
print(f"  健康状态: {health}")
rec = router.get_recommendation(TaskType.CREATIVE_WRITING)
print(f"  创意写作推荐: {rec.get('recommended_model', 'N/A')}")
print("  ✅ 通过")

print("\n[2] PleasureBeatAnalyzer — 爽点节奏分析...")
from pleasure_beat_analyzer import PleasureBeatAnalyzer
analyzer = PleasureBeatAnalyzer()

test_chapter = """
李明站在擂台中央，环顾四周。台下数千观众的目光如刀锋般刺来。

"就凭你，也配挑战我？"对手冷笑一声，手中长剑泛起寒光。

李明没有回答。他闭上眼睛，体内那股沉寂多年的力量突然涌动起来。瓶颈——松动了！

轰！

一股磅礴的气势从他体内爆发，擂台地面寸寸龟裂。对手脸上的冷笑凝固了，取而代之的是难以置信的惊恐。

"这...这怎么可能！"

全场鸦雀无声。

李明睁开眼，嘴角勾起一抹弧度："现在，轮到我了。"
"""

profile = analyzer.analyze(test_chapter, chapter_num=1, is_opening=True)
print(f"  节奏评分: {profile.score}/100")
print(f"  爽点密度: {profile.beat_density}/千字")
print(f"  章末钩子: {profile.hook_strength}")
print(f"  问题数: {len(profile.issues)}")
print(f"  建议数: {len(profile.suggestions)}")
print("  ✅ 通过")

print("\n[3] DeconstructionEngine — AI拆书引擎...")
from deconstruction_engine import DeconstructionEngine, SnowflakeStage
engine = DeconstructionEngine()

templates = engine.get_genre_templates()
print(f"  可用模板: {list(templates.keys())}")

guide = engine.get_snowflake_guide(SnowflakeStage.IDEA)
print(f"  雪花写作法引导(阶段1): {guide[:80]}...")

chapters = {1: test_chapter, 2: test_chapter.replace("李明", "李凡")}
result = engine.deconstruct("测试作品", chapters, "玄幻")
print(f"  拆解结果: {result.total_chapters}章, {result.total_words}字")
print(f"  结构评分: {result.structure_score}/100")
print(f"  可复用模式: {result.reusable_patterns}")
print("  ✅ 通过")

print("\n[4] StyleParameterTuner — 风格参数调节...")
from style_parameter_tuner import StyleParameterTuner
tuner = StyleParameterTuner()

presets = tuner.list_presets()
print(f"  预设风格数: {len(presets)}")

tuner.activate_preset("热血爽文")
instructions = tuner.to_prompt_instructions()
print(f"  热血爽文指令(前100字): {instructions[:100]}...")

blended = tuner.blend("古风仙侠", "悬疑推理", 0.4)
print(f"  混合风格: {blended.name}")

comparison = tuner.compare_profiles("热血爽文", "文学性写作")
print(f"  风格对比差异维度: {comparison['total_dimensions_changed']}")
print("  ✅ 通过")

print("\n[5] IntelligentOrchestrator — 新模块注册...")
from intelligent_orchestrator import IntelligentOrchestrator
orch = IntelligentOrchestrator()

new_modules = ["model_router", "beat_analyzer", "deconstruction_engine", "style_tuner"]
for m in new_modules:
    assert m in orch.modules, f"模块 {m} 应已注册"
print(f"  总模块数: {len(orch.modules)}")
print(f"  新模块: {new_modules}")
print("  ✅ 通过")

print("\n" + "=" * 60)
print("✅ 全部P0级模块验证通过！")
print("=" * 60)
