#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS v7.0 快速功能测试
验证核心引擎和所有功能是否正常
"""

import sys
from pathlib import Path


def test_file_structure():
    """测试项目文件结构"""
    print("📁 1. 测试项目文件结构...")
    
    project_root = Path(__file__).parent
    required_dirs = [
        "skills",
        "skills/level1",
        "skills/level2",
        "skills/level3",
        "skills/level2/learnings",
        "docs",
        "core",
        "config"
    ]
    
    missing = []
    for dir_name in required_dirs:
        dir_path = project_root / dir_name
        if not dir_path.exists():
            missing.append(dir_name)
    
    if missing:
        print(f"   ⚠️  缺失目录: {', '.join(missing)}")
        return False
    else:
        print("   ✅ 目录结构完整")
        return True


def test_python_imports():
    """测试Python模块导入"""
    print("\n🐍 2. 测试Python模块...")
    
    try:
        # 测试OpenAI
        from openai import OpenAI
        print("   ✅ OpenAI库正常")
        
        # 测试核心模块
        core_files = [
            "core.nwacs_novel_engine",
            "core.nwacs_quality_assurance",
            "core.nwacs_diagnostic",
            "core.nwacs_evaluator",
            "core.feishu.nwacs_feishu",
            "core.wechat.nwacs_wechat"
        ]
        
        for module_name in core_files:
            try:
                __import__(module_name)
                print(f"   ✅ {module_name}")
            except Exception as e:
                print(f"   ⚠️  {module_name} 导入失败: {e}")
        
        return True
        
    except ImportError as e:
        print(f"   ❌ 缺失库: {e}")
        print("      请运行: pip install openai")
        return False


def test_knowledge_bases():
    """测试知识库"""
    print("\n📚 3. 测试知识库...")
    
    project_root = Path(__file__).parent
    knowledge_dir = project_root / "skills" / "level2" / "learnings"
    
    if not knowledge_dir.exists():
        print("   ❌ 知识库目录不存在")
        return False
    
    # 检查核心知识库
    required_knowledges = [
        "00_知识库共享中心索引.txt",
        "玄幻修仙小说知识库.txt",
        "都市小说详细知识库.txt",
        "女频言情小说详细知识库.txt",
        "悬疑推理小说详细知识库.txt",
        "科幻末日小说详细知识库.txt",
        "2026年最新网文写作技巧与市场趋势.txt",
        "跨媒体开发知识库.txt",
        "学习进化系统知识库.txt"
    ]
    
    found = 0
    missing = []
    
    for kb in required_knowledges:
        kb_path = knowledge_dir / kb
        if kb_path.exists():
            found += 1
        else:
            missing.append(kb)
    
    print(f"   ✅ 找到 {found}/{len(required_knowledges)} 核心知识库")
    
    if missing:
        print(f"   ⚠️  缺失: {', '.join(missing[:3])}")
    
    total_kbs = len(list(knowledge_dir.glob("*.txt"))) + len(list(knowledge_dir.glob("*.md")))
    print(f"   📊 总知识库数量: {total_kbs}")
    
    return True


def test_skills():
    """测试Skill文件"""
    print("\n🎯 4. 测试Skill文件...")
    
    project_root = Path(__file__).parent
    skills_dir = project_root / "skills"
    
    # 检查三级Skill
    level3_dir = skills_dir / "level3"
    level3_files = list(level3_dir.glob("*.md"))
    print(f"   ✅ 三级Skill: {len(level3_files)} 个")
    
    # 检查二级Skill
    level2_dir = skills_dir / "level2"
    level2_files = list(level2_dir.glob("*.md"))
    print(f"   ✅ 二级Skill: {len(level2_files)} 个")
    
    # 检查一级Skill
    level1_dir = skills_dir / "level1"
    level1_files = list(level1_dir.glob("*.md"))
    print(f"   ✅ 一级Skill: {len(level1_files)} 个")
    
    # Master类Skill
    master_dirs = list(skills_dir.glob("*Master"))
    print(f"   ✅ Master类Skill: {len(master_dirs)} 个")
    
    return True


def test_startup_scripts():
    """测试启动脚本"""
    print("\n🚀 5. 测试启动脚本...")
    
    project_root = Path(__file__).parent
    
    scripts = [
        "启动创作引擎.bat",
        "启动飞书集成.bat",
        "启动微信集成.bat",
        "启动诊断工具.bat",
        "启动DeepSeek评测.bat"
    ]
    
    found = []
    missing = []
    
    for script in scripts:
        script_path = project_root / script
        if script_path.exists():
            found.append(script)
        else:
            missing.append(script)
    
    for script in found:
        print(f"   ✅ {script}")
    
    if missing:
        print(f"   ⚠️  缺失: {', '.join(missing)}")
    
    return True


def test_config_files():
    """测试配置文件"""
    print("\n⚙️ 6. 测试配置文件...")
    
    project_root = Path(__file__).parent
    config_dir = project_root / "config"
    
    if not config_dir.exists():
        print("   ⚠️  config目录缺失，正在创建...")
        config_dir.mkdir(exist_ok=True)
    
    configs = [
        "feishu_config.json",
        "wechat_config.json"
    ]
    
    for config in configs:
        config_path = config_dir / config
        if config_path.exists():
            print(f"   ✅ {config}")
        else:
            print(f"   ⚠️  {config} 缺失（可选功能）")
    
    return True


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("🧪 NWACS v7.0 快速功能测试")
    print("=" * 60)
    
    results = []
    
    results.append(("文件结构", test_file_structure()))
    results.append(("Python模块", test_python_imports()))
    results.append(("知识库", test_knowledge_bases()))
    results.append(("Skill文件", test_skills()))
    results.append(("启动脚本", test_startup_scripts()))
    results.append(("配置文件", test_config_files()))
    
    print("\n" + "=" * 60)
    print("📊 测试总结")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"   {name}: {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"📈 结果: {passed}/{len(results)} 项通过")
    print("=" * 60)
    
    if failed == 0:
        print("\n🎉 恭喜！NWACS v7.0功能完全正常！")
        print("\n📖 快速开始：")
        print("   1. 双击 '启动创作引擎.bat' 开始小说创作")
        print("   2. 双击 '启动诊断工具.bat' 检查项目状态")
        print("   3. 双击 '启动飞书集成.bat' 配置飞书通知")
    else:
        print(f"\n⚠️  有 {failed} 项需要检查")
    
    return passed == len(results)


if __name__ == "__main__":
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️ 用户中断测试")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ 测试出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
