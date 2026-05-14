#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""验证去AI痕迹修复效果"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

print("=" * 60)
print("去AI痕迹修复验证")
print("=" * 60)

print("\n[1] EnhancedAIDetector.rewrite() — 不再做破坏性机械替换...")
from enhanced_ai_detector import EnhancedAIDetector
detector = EnhancedAIDetector()

test_text = "他宛如天神下凡，仿佛一切都在掌控之中。非常厉害，极其强大。微微一笑，心中暗想：这次赢定了。"
original = detector.detect(test_text)
print(f"  原始AI分数: {original.overall_score}")

rewritten, report = detector.rewrite(test_text, "medium")
print(f"  改写后AI分数: {report.final_score}")
print(f"  改写后文本(前200字): {rewritten[:200]}")

assert "宛如" in rewritten, "文本不应被破坏性修改"
print("  ✅ 通过 — 不再做破坏性机械替换")

print("\n[2] SmartCreativeEngine.rewrite() — 内置去AI系统提示词...")
from engine.creative_engine import SmartCreativeEngine
engine = SmartCreativeEngine()

assert hasattr(engine, 'rewrite'), "engine应有rewrite方法"
print("  ✅ 通过 — rewrite方法存在")

print("\n[3] CollaborativeWritingPipeline — 默认跳过rewrite/polish...")
from collaborative_pipeline import CollaborativeWritingPipeline, PipelineConfig
config = PipelineConfig()
assert config.enable_rewrite == False, "rewrite应默认关闭"
assert config.enable_polish == False, "polish应默认关闭"
print(f"  enable_rewrite: {config.enable_rewrite}")
print(f"  enable_polish: {config.enable_polish}")
print("  ✅ 通过 — rewrite/polish默认关闭")

print("\n[4] SimpleDirectPipeline — 直出管线...")
from simple_direct_pipeline import SimpleDirectPipeline
sp = SimpleDirectPipeline()
sp.novel_title = "测试"
sp.configure(genre="玄幻", auto_save=False)

config = sp.export_config()
assert config["genre"] == "玄幻"
assert config["novel_title"] == "测试"
print(f"  配置: {config}")
print("  ✅ 通过 — 直出管线配置正常")

print("\n[5] IntelligentOrchestrator — 新命令...")
from intelligent_orchestrator import IntelligentOrchestrator
orch = IntelligentOrchestrator()

assert "simple_pipeline" in orch.modules, "应注册simple_pipeline"
assert "genre_manager" in orch.modules, "应注册genre_manager"
assert "voice_injector" in orch.modules, "应注册voice_injector"
print(f"  已注册模块数: {len(orch.modules)}")
print("  ✅ 通过 — 新模块已注册")

print("\n" + "=" * 60)
print("✅ 全部验证通过！")
print("=" * 60)
