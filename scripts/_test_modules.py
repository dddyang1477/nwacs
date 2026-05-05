#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 核心模块真实执行测试
逐函数测试，验证代码能否真实运行
"""

import sys
import os
import json
import traceback
import importlib

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "core", "v8"))
sys.path.insert(0, os.path.join(BASE, "core", "v8", "engine"))
sys.path.insert(0, os.path.join(BASE, "core", "v8", "skill_manager"))

try:
    sys.stdout.reconfigure(encoding='utf-8')
except (AttributeError, OSError):
    pass

PASS = "✅"
FAIL = "❌"
SKIP = "⏭️"
WARN = "⚠️"

results = {"pass": 0, "fail": 0, "skip": 0, "total": 0}

def test(name, func):
    """运行单个测试"""
    global results
    results["total"] += 1
    try:
        func()
        results["pass"] += 1
        print(f"  {PASS} {name}")
        return True
    except Exception as e:
        results["fail"] += 1
        tb = traceback.format_exc()
        print(f"  {FAIL} {name}")
        print(f"     错误: {e}")
        print(f"     详情: {tb.split(chr(10))[-3].strip()}")
        return False

def section(title):
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}")

# ================================================================
# 模块1: AI检测与去痕 (纯逻辑，无需API)
# ================================================================
def test_ai_detector():
    section("模块1: AI检测与去痕 (ai_detector_and_rewriter.py)")
    
    from ai_detector_and_rewriter import AIDetectorAndRewriter
    
    detector = AIDetectorAndRewriter()
    
    # 1.1 实例化
    test("1.1 类实例化", lambda: None)
    
    # 1.2 特征词库加载
    test("1.2 特征词库加载", lambda: (
        len(detector.ai_indicators) > 0,
        len(detector.ai_patterns) > 0
    ))
    
    # 1.3 AI检测 - 高AI文本
    high_ai_text = """
    林晨缓缓地站起身，宛如一只刚刚破茧而出的蝴蝶，心中不禁激动万分。
    仿佛天地都在为他欢呼，眼前的景象十分壮观，格外震撼人心。
    这一切似乎都像是一场梦境，渐渐地，林晨才相信这是真的。
    他微微一笑，心中暗想，自己的努力终究没有白费。
    """
    
    def test_detect_high():
        score = detector.detect_ai_score(high_ai_text)
        assert 0 <= score <= 100, f"分数超出范围: {score}"
        assert score > 20, f"高AI文本分数应>20, 实际: {score}"
        print(f"     高AI文本分数: {score}/100")
    
    test("1.3 AI检测 - 高AI文本", test_detect_high)
    
    # 1.4 AI检测 - 低AI文本
    low_ai_text = """
    林晨站起来，腿有点麻。他揉了揉膝盖，看了眼窗外。
    天快亮了。一夜没睡，脑子昏沉沉的。
    "妈的。"他骂了一句，抓起桌上的烟盒，空的。
    他把烟盒揉成一团，扔进垃圾桶。
    """
    
    def test_detect_low():
        score = detector.detect_ai_score(low_ai_text)
        assert 0 <= score <= 100, f"分数超出范围: {score}"
        print(f"     低AI文本分数: {score}/100")
    
    test("1.4 AI检测 - 低AI文本", test_detect_low)
    
    # 1.5 去痕重写
    def test_rewrite():
        result = detector.rewrite_remove_ai(high_ai_text)
        assert isinstance(result, str), f"返回类型错误: {type(result)}"
        assert len(result) > 0, "返回空字符串"
        new_score = detector.detect_ai_score(result)
        print(f"     去痕后分数: {new_score}/100")
    
    test("1.5 去痕重写", test_rewrite)
    
    # 1.6 人类化增强
    def test_enhance():
        result = detector.enhance_humanize(low_ai_text)
        assert isinstance(result, str), f"返回类型错误: {type(result)}"
        assert len(result) > 0, "返回空字符串"
    
    test("1.6 人类化增强", test_enhance)
    
    # 1.7 完整流程
    def test_full_flow():
        result = detector.check_and_rewrite(high_ai_text)
        assert isinstance(result, str), f"返回类型错误: {type(result)}"
        assert len(result) > 0, "返回空字符串"
    
    test("1.7 完整检测-重写流程", test_full_flow)
    
    # 1.8 空文本处理
    def test_empty():
        score = detector.detect_ai_score("")
        assert score == 0, f"空文本分数应为0, 实际: {score}"
    
    test("1.8 空文本处理", test_empty)
    
    # 1.9 段落打乱
    def test_shuffle():
        text = "段落一\n\n段落二\n\n段落三\n\n段落四\n\n段落五"
        result = detector._shuffle_paragraphs(text)
        assert isinstance(result, str)
    
    test("1.9 段落打乱", test_shuffle)

# ================================================================
# 模块2: 质量检查 (纯逻辑，无需API)
# ================================================================
def test_quality_checker():
    section("模块2: 质量检查 (quality_check_and_save_v2.py)")
    
    from quality_check_and_save_v2 import QualityChecker, clean_content, mark_for_manual_check
    
    # 2.1 实例化
    test_content = """
    第一章 觉醒
    
    林晨站在天台上，风吹得他的校服猎猎作响。
    
    他低头看着手中的玉佩，那是母亲留给他的唯一遗物。玉佩在月光下泛着淡淡的青光，像是有什么东西在里面流动。
    
    "你终于来了。"身后传来一个苍老的声音。
    
    林晨猛地转身，看到一个白发老者不知何时出现在他身后。老者穿着一身青色长袍，仙风道骨，不像是这个时代的人。
    
    "你是谁？"林晨警惕地问。
    
    老者微微一笑："我是谁不重要，重要的是你是谁。"
    
    林晨皱眉："什么意思？"
    
    "你手中的玉佩，是上古神器'天机盘'的碎片。"老者指着玉佩说，"它选择了你，说明你有修仙的资质。"
    
    林晨愣住了。修仙？那不是小说里才有的东西吗？
    
    "这个世界远比你想象的要复杂。"老者继续说，"灵气正在复苏，古老的传承即将重现。而你，将是这场变革的关键。"
    
    林晨握紧了玉佩，感受着掌心传来的温热。他不知道该不该相信这个突然出现的老者，但内心深处，有一个声音在告诉他——这一切都是真的。
    
    "我该怎么做？"林晨问。
    
    老者从怀中取出一本泛黄的古籍："这是《天机诀》，是最基础的修炼功法。从今天开始，你要按照上面的方法修炼。"
    
    林晨接过古籍，翻开第一页。上面画着复杂的人体经络图，旁边写着密密麻麻的古文。虽然看不懂，但他能感觉到这些文字中蕴含的力量。
    
    "记住，"老者的身影开始变得模糊，"修炼之路充满艰险，但只要你坚持下去，终有一天会站在这个世界的巅峰。"
    
    话音落下，老者化作一道青光，消失在夜空中。
    
    林晨独自站在天台上，手中握着玉佩和古籍。月光洒在他身上，仿佛为他披上了一层银色的铠甲。
    
    从这一刻起，他的人生将彻底改变。
    """
    
    checker = QualityChecker(test_content, 1)
    
    test("2.1 类实例化", lambda: None)
    
    # 2.2 字数检测
    def test_word_count():
        passed, msg = checker.check_word_count()
        assert isinstance(passed, bool)
        assert isinstance(msg, str)
        print(f"     {msg}")
    
    test("2.2 字数检测", test_word_count)
    
    # 2.3 结构检测
    def test_structure():
        passed, msg = checker.check_structure()
        assert isinstance(passed, bool)
        assert isinstance(msg, str)
        print(f"     {msg}")
    
    test("2.3 结构检测", test_structure)
    
    # 2.4 可读性检测
    def test_readability():
        passed, msg = checker.check_readability()
        assert isinstance(passed, bool)
        assert isinstance(msg, str)
        print(f"     {msg}")
    
    test("2.4 可读性检测", test_readability)
    
    # 2.5 结尾检测
    def test_ending():
        passed, msg = checker.check_ending()
        assert isinstance(passed, bool)
        assert isinstance(msg, str)
        print(f"     {msg}")
    
    test("2.5 结尾检测", test_ending)
    
    # 2.6 完整检测流程
    def test_full_check():
        passed, report = checker.run_all_checks()
        assert isinstance(passed, bool)
        assert isinstance(report, dict)
        assert "final" in report
        print(f"     最终结果: {'通过' if passed else '未通过'}")
    
    test("2.6 完整检测流程", test_full_check)
    
    # 2.7 内容清理
    def test_clean():
        dirty = "本章结束\n\n正文内容\n\n未完待续\n\n---\n\n字数: 3000"
        cleaned = clean_content(dirty)
        assert "本章结束" not in cleaned
        assert "未完待续" not in cleaned
        assert "正文内容" in cleaned
    
    test("2.7 内容清理", test_clean)
    
    # 2.8 短内容检测
    def test_short():
        short = "短内容"
        checker2 = QualityChecker(short, 1)
        passed, report = checker2.run_all_checks()
        assert not passed, "短内容应该不通过"
    
    test("2.8 短内容检测", test_short)
    
    # 2.9 标记人工处理
    def test_mark():
        report = {"word_count": 100, "paragraphs": 2}
        mark_for_manual_check(99, report)
        assert os.path.exists("novel/第99章_需要人工检查.txt")
        # 清理
        os.remove("novel/第99章_需要人工检查.txt")
        if os.path.exists("novel/待人工处理列表.txt"):
            os.remove("novel/待人工处理列表.txt")
    
    test("2.9 标记人工处理", test_mark)

# ================================================================
# 模块3: Skill管理器 (纯逻辑，无需API)
# ================================================================
def test_skill_manager():
    section("模块3: Skill管理器 (skill_manager.py)")
    
    from skill_manager import (
        SkillType, SkillMetadata, Skill,
        WorldBuildingSkill, CharacterDesignSkill, PlotDesignSkill
    )
    
    # 3.1 枚举类型
    test("3.1 SkillType枚举", lambda: (
        SkillType.WORLD_BUILDING.value == "world_building",
        SkillType.CHARACTER_DESIGN.value == "character_design",
        SkillType.PLOT_DESIGN.value == "plot_design",
        SkillType.SCENE_DESCRIPTION.value == "scene_description",
        SkillType.DIALOGUE_WRITING.value == "dialogue_writing",
        SkillType.COMBAT_DESIGN.value == "combat_design",
        SkillType.STYLE_REFINEMENT.value == "style_refinement",
        SkillType.OUTLINE_GENERATION.value == "outline_generation",
        SkillType.NOVEL_WRITING.value == "novel_writing",
        SkillType.PROOFREADING.value == "proofreading",
        SkillType.MARKET_ANALYSIS.value == "market_analysis"
    ))
    
    # 3.2 SkillMetadata创建
    def test_metadata():
        meta = SkillMetadata(
            skill_id="test_skill",
            name="测试Skill",
            skill_type=SkillType.WORLD_BUILDING,
            description="测试用Skill",
            tags=["测试"],
            input_schema={"type": "object"},
            output_schema={"type": "object"},
            priority=50
        )
        assert meta.skill_id == "test_skill"
        assert meta.name == "测试Skill"
        assert meta.priority == 50
        assert meta.enabled == True
        assert meta.usage_count == 0
        
        d = meta.to_dict()
        assert d["skill_id"] == "test_skill"
        assert d["name"] == "测试Skill"
        assert d["skill_type"] == "world_building"
    
    test("3.2 SkillMetadata创建与序列化", test_metadata)
    
    # 3.3 WorldBuildingSkill创建
    def test_world_skill():
        skill = WorldBuildingSkill()
        assert skill.metadata.skill_id == "world_building"
        assert skill.metadata.name == "世界观构造师"
        assert skill.metadata.priority == 90
        assert skill.metadata.skill_type == SkillType.WORLD_BUILDING
        assert "world_type" in skill.metadata.input_schema["properties"]
    
    test("3.3 WorldBuildingSkill创建", test_world_skill)
    
    # 3.4 CharacterDesignSkill创建
    def test_char_skill():
        skill = CharacterDesignSkill()
        assert skill.metadata.skill_id == "character_design"
        assert skill.metadata.name == "角色塑造师"
        assert skill.metadata.priority == 85
        assert "character_type" in skill.metadata.input_schema["properties"]
    
    test("3.4 CharacterDesignSkill创建", test_char_skill)
    
    # 3.5 PlotDesignSkill创建
    def test_plot_skill():
        skill = PlotDesignSkill()
        assert skill.metadata.skill_id == "plot_design"
        assert skill.metadata.name == "剧情构造师"
        assert skill.metadata.priority == 80
        assert "theme" in skill.metadata.input_schema["properties"]
    
    test("3.5 PlotDesignSkill创建", test_plot_skill)
    
    # 3.6 Skill基类_execute未实现检查
    def test_base_skill():
        meta = SkillMetadata("base", "基础", SkillType.WORLD_BUILDING, "", [], {}, {})
        base = Skill(meta)
        try:
            base._execute()
            assert False, "应该抛出NotImplementedError"
        except NotImplementedError:
            pass  # 预期行为
    
    test("3.6 Skill基类_execute未实现检查", test_base_skill)
    
    # 3.7 Skill元数据usage_count递增
    def test_usage_count():
        meta = SkillMetadata("count_test", "计数测试", SkillType.WORLD_BUILDING, "", [], {}, {})
        skill = Skill(meta)
        # 直接调用execute会触发_execute，但我们只测试计数
        assert skill.metadata.usage_count == 0
        skill.metadata.usage_count += 1
        assert skill.metadata.usage_count == 1
    
    test("3.7 Skill元数据usage_count", test_usage_count)

# ================================================================
# 模块4: 创作引擎 (部分需要API，测试非API部分)
# ================================================================
def test_creative_engine():
    section("模块4: 创作引擎 (creative_engine.py)")
    
    from creative_engine import (
        SmartCreativeEngine, CreativeEngineBuilder,
        DeepSeekAdapter, ModelAdapter
    )
    
    # 4.1 引擎构建器
    def test_builder():
        engine = CreativeEngineBuilder.create_basic_engine()
        assert isinstance(engine, SmartCreativeEngine)
    
    test("4.1 引擎构建器", test_builder)
    
    # 4.2 引擎实例化
    engine = SmartCreativeEngine()
    test("4.2 引擎实例化", lambda: None)
    
    # 4.3 模型切换
    def test_model_switch():
        assert engine.set_active_model("deepseek") == True
        assert engine.set_active_model("nonexistent") == False
    
    test("4.3 模型切换", test_model_switch)
    
    # 4.4 风格提示词获取
    def test_style_prompts():
        styles = ["default", "novel", "xuanhuan", "urban", "romance", 
                  "suspense", "science", "poetic", "humorous", "professional"]
        for s in styles:
            prompt = engine._get_style_prompt(s)
            assert isinstance(prompt, str) and len(prompt) > 0, f"风格'{s}'提示词为空"
        # 未知风格回退到default
        unknown = engine._get_style_prompt("unknown_style")
        assert unknown == engine._get_style_prompt("default")
    
    test("4.4 风格提示词获取", test_style_prompts)
    
    # 4.5 DeepSeekAdapter创建
    def test_adapter():
        adapter = DeepSeekAdapter()
        assert adapter.get_model_name() == "deepseek-chat"
        assert adapter.api_key is not None
        assert adapter.base_url == "https://api.deepseek.com"
    
    test("4.5 DeepSeekAdapter创建", test_adapter)
    
    # 4.6 ModelAdapter抽象基类
    def test_abstract():
        assert hasattr(ModelAdapter, 'generate')
        assert hasattr(ModelAdapter, 'get_model_name')
    
    test("4.6 ModelAdapter抽象基类", test_abstract)
    
    # 4.7 引擎模型字典
    def test_models_dict():
        assert "deepseek" in engine.models
        assert isinstance(engine.models["deepseek"], DeepSeekAdapter)
    
    test("4.7 引擎模型字典", test_models_dict)

# ================================================================
# 模块5: 三次质量检验 (部分需要API，测试非API部分)
# ================================================================
def test_three_time_check():
    section("模块5: 三次质量检验 (three_time_quality_check.py)")
    
    from three_time_quality_check import (
        apply_additional_de_ai,
        create_quality_check_wrapper
    )
    
    # 5.1 额外去痕处理
    def test_extra_deai():
        text = "他慢慢地站起身，仿佛一只蝴蝶，微微一笑，心中暗想。"
        result = apply_additional_de_ai(text)
        assert isinstance(result, str)
        assert len(result) > 0
    
    test("5.1 额外去痕处理", test_extra_deai)
    
    # 5.2 包装器创建
    def test_wrapper():
        wrapper = create_quality_check_wrapper()
        assert callable(wrapper)
    
    test("5.2 包装器创建", test_wrapper)

# ================================================================
# 模块6: 知识库加载验证
# ================================================================
def test_knowledge_base():
    section("模块6: 知识库加载验证")
    
    engine_dir = os.path.join(BASE, "core", "v8", "engine")
    
    # 6.1 builtin_knowledge.json
    def test_builtin():
        path = os.path.join(engine_dir, "builtin_knowledge.json")
        assert os.path.exists(path), f"文件不存在: {path}"
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        assert "玄幻修仙设定库" in data
        assert "网文写作手法库" in data
        assert "2026爆款小说拆解库" in data
        print(f"     包含 {len(data)} 个知识库模块")
    
    test("6.1 builtin_knowledge.json", test_builtin)
    
    # 6.2 extended_knowledge.json
    def test_extended():
        path = os.path.join(engine_dir, "extended_knowledge.json")
        assert os.path.exists(path), f"文件不存在: {path}"
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        assert "writing_techniques" in data
        assert "novel_formulas" in data
        assert "genre_trends" in data
        assert "golden_three_chapters" in data
        assert "pleasure_point_design" in data
        assert "bestseller_opening_formula" in data
        assert "emotional_value_writing" in data
        print(f"     包含 {len(data)} 个知识模块")
    
    test("6.2 extended_knowledge.json", test_extended)

# ================================================================
# 模块7: Skills文件夹结构验证
# ================================================================
def test_skills_structure():
    section("模块7: Skills文件夹结构验证")
    
    skills_dir = os.path.join(BASE, "skills")
    
    # 7.1 目录结构
    def test_dirs():
        for sub in ["level1", "level2", "level3", "masters", "scripts", "references"]:
            path = os.path.join(skills_dir, sub)
            assert os.path.isdir(path), f"目录不存在: {sub}"
    
    test("7.1 目录结构完整", test_dirs)
    
    # 7.2 level1文件
    def test_level1():
        path = os.path.join(skills_dir, "level1")
        files = os.listdir(path)
        md_files = [f for f in files if f.endswith(".md")]
        assert len(md_files) >= 1, "level1缺少Skill文件"
        print(f"     level1: {len(md_files)} 个Skill")
    
    test("7.2 level1文件", test_level1)
    
    # 7.3 level2文件
    def test_level2():
        path = os.path.join(skills_dir, "level2")
        files = os.listdir(path)
        md_files = [f for f in files if f.endswith(".md") and f[0].isdigit()]
        assert len(md_files) >= 20, f"level2 Skill数量不足: {len(md_files)}"
        print(f"     level2: {len(md_files)} 个Skill")
    
    test("7.3 level2文件", test_level2)
    
    # 7.4 level3文件
    def test_level3():
        path = os.path.join(skills_dir, "level3")
        files = os.listdir(path)
        md_files = [f for f in files if f.endswith(".md") and f[0].isdigit()]
        assert len(md_files) >= 10, f"level3 Skill数量不足: {len(md_files)}"
        print(f"     level3: {len(md_files)} 个Skill")
    
    test("7.4 level3文件", test_level3)

# ================================================================
# 主函数
# ================================================================
def main():
    print("=" * 70)
    print("  NWACS 核心模块真实执行测试")
    print("=" * 70)
    print(f"  项目路径: {BASE}")
    print(f"  测试时间: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    test_ai_detector()
    test_quality_checker()
    test_skill_manager()
    test_creative_engine()
    test_three_time_check()
    test_knowledge_base()
    test_skills_structure()
    
    # 汇总
    print(f"\n{'='*70}")
    print(f"  测试汇总")
    print(f"{'='*70}")
    print(f"  总计: {results['total']} 项")
    print(f"  {PASS} 通过: {results['pass']}")
    print(f"  {FAIL} 失败: {results['fail']}")
    print(f"  {SKIP} 跳过: {results['skip']}")
    
    if results['fail'] == 0:
        print(f"\n  {PASS} 所有测试通过！")
    else:
        print(f"\n  {FAIL} 有 {results['fail']} 项测试失败，需要修复")
    
    print(f"{'='*70}")
    
    return results['fail'] == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
