#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证写作知识引擎集成效果
测试: 知识引擎 → 检测器 → 管线 → 编排器 全链路
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("NWACS 写作知识引擎集成验证")
print("=" * 60)

# ============================================================
# 1. WritingKnowledgeEngine 自检
# ============================================================
print("\n[1/5] WritingKnowledgeEngine 自检")
from writing_knowledge_engine import WritingKnowledgeEngine

engine = WritingKnowledgeEngine()

test_text = """他感到非常愤怒，因为敌人又一次逃脱了。首先，他检查了周围的痕迹。
其次，他开始分析敌人的逃跑路线。最后，他制定了一个新的追捕计划。
总而言之，这次失败让他意识到了自己的不足，也为后续的成长体系赋能。"""

diagnosis = engine.diagnose_ai_traits(test_text)
print(f"  综合评分: {diagnosis.overall_ai_score:.1%}")
print(f"  风险等级: {diagnosis.risk_level}")
print(f"  检测特征: {len(diagnosis.detected_traits)}个")
assert diagnosis.overall_ai_score > 0.5, "AI评分应>50%"
assert len(diagnosis.detected_traits) >= 3, "应检测到至少3个特征"
print("  ✅ 诊断功能正常")

pipeline = engine.generate_deai_pipeline(test_text, "voice")
print(f"  去痕阶段: {len(pipeline.stages)}个")
print(f"  预估效果: {pipeline.estimated_effectiveness:.0%}")
assert len(pipeline.stages) >= 4, "应有至少4个去痕阶段"
print("  ✅ 去痕流水线正常")

techniques = engine.recommend_techniques(context={"genre": "玄幻", "chapter_num": 1})
print(f"  推荐技法: {len(techniques)}个")
assert len(techniques) > 0, "应有技法推荐"
print("  ✅ 技法推荐正常")

enhanced = engine.inject_knowledge_to_prompt("写一章小说", "玄幻", 1, 3)
print(f"  提示词增强: {len('写一章小说')} → {len(enhanced)} 字符")
assert len(enhanced) > len("写一章小说") * 3, "增强后应显著更长"
print("  ✅ 提示词增强正常")

# ============================================================
# 2. EnhancedAIDetector 深度诊断
# ============================================================
print("\n[2/5] EnhancedAIDetector 深度诊断")
from enhanced_ai_detector import EnhancedAIDetector

detector = EnhancedAIDetector()

basic = detector.detect(test_text)
print(f"  基础检测: {basic.overall_score}/100 ({basic.level})")

deep = detector.diagnose_deep(test_text)
print(f"  深度诊断: {deep['overall_ai_score']:.1%} ({deep['risk_level']})")
print(f"  检测特征: {len(deep['detected_traits'])}个")
print(f"  去痕阶段: {len(deep['deai_pipeline']['stages'])}个")
print(f"  推荐技法: {len(deep['recommended_techniques'])}个")
assert deep['overall_ai_score'] > 0.5, "深度诊断应检测到AI特征"
assert len(deep['fix_priority']) > 0, "应有修复优先级"
print("  ✅ 深度诊断正常")

# ============================================================
# 3. SimpleDirectPipeline 知识注入
# ============================================================
print("\n[3/5] SimpleDirectPipeline 知识注入")
from simple_direct_pipeline import SimpleDirectPipeline

pipeline = SimpleDirectPipeline(knowledge_engine=engine)
pipeline.config.genre = "玄幻"
pipeline.novel_title = "测试作品"

char_count = pipeline._get_character_count()
print(f"  人物数量: {char_count}")
assert char_count == 0, "无memory时应为0"
print("  ✅ _get_character_count正常")

system_prompt = pipeline._build_system_prompt()
print(f"  系统提示词长度: {len(system_prompt)} 字符")
assert len(system_prompt) > 500, "系统提示词应足够长"
print("  ✅ 系统提示词构建正常(含知识注入)")

# ============================================================
# 4. IntelligentOrchestrator 模块注册
# ============================================================
print("\n[4/5] IntelligentOrchestrator 模块注册")
from intelligent_orchestrator import IntelligentOrchestrator

orch = IntelligentOrchestrator()

assert "knowledge_engine" in orch.modules, "knowledge_engine应已注册"
print(f"  已注册模块: {len(orch.modules)}个")
print(f"  knowledge_engine: {orch.modules['knowledge_engine'].description}")

loaded = orch.load_module("knowledge_engine")
assert loaded, "knowledge_engine应加载成功"
print("  ✅ 模块注册和加载正常")

# ============================================================
# 5. 编排器命令测试
# ============================================================
print("\n[5/5] 编排器命令测试")

r1 = orch.execute("diagnose_ai_traits", text=test_text)
assert r1["success"], f"diagnose_ai_traits失败: {r1.get('error')}"
print(f"  diagnose_ai_traits: {r1['data']['overall_ai_score']:.1%} ({r1['data']['risk_level']})")
print("  ✅ diagnose_ai_traits命令正常")

r2 = orch.execute("recommend_techniques", context={"genre": "玄幻", "chapter_num": 1})
assert r2["success"], f"recommend_techniques失败: {r2.get('error')}"
print(f"  recommend_techniques: {len(r2['data'])}个推荐")
print("  ✅ recommend_techniques命令正常")

r3 = orch.execute("generate_deai_pipeline", text=test_text, target_level="voice")
assert r3["success"], f"generate_deai_pipeline失败: {r3.get('error')}"
print(f"  generate_deai_pipeline: {len(r3['data']['stages'])}阶段, 效果{r3['data']['estimated_effectiveness']:.0%}")
print("  ✅ generate_deai_pipeline命令正常")

r4 = orch.execute("inject_knowledge", base_prompt="写一章", genre="玄幻", chapter_num=1)
assert r4["success"], f"inject_knowledge失败: {r4.get('error')}"
print(f"  inject_knowledge: {r4['data']['original_length']} → {r4['data']['enhanced_length']} 字符")
print("  ✅ inject_knowledge命令正常")

r5 = orch.execute("detect_ai", text=test_text, deep=True)
assert r5["success"], f"detect_ai deep失败: {r5.get('error')}"
print(f"  detect_ai(deep): {r5['data']['overall_ai_score']:.1%}, mode={r5.get('mode')}")
print("  ✅ detect_ai深度模式正常")

# ============================================================
# 总结
# ============================================================
print("\n" + "=" * 60)
print("✅ 所有验证通过 — 写作知识引擎集成成功")
print("=" * 60)
print("""
集成内容:
  - WritingKnowledgeEngine: 26个AI特征 + 21个技法 + 8个读者策略 + 6个去痕策略
  - EnhancedAIDetector.diagnose_deep(): 6层深度诊断
  - SimpleDirectPipeline: 自动知识注入到系统提示词
  - IntelligentOrchestrator: 4个新命令 + 深度检测模式
""")
