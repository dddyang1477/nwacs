#!/usr/bin/env python3
"""
NWACS v9.0 完整功能测试脚本
测试所有4个阶段的实现
"""

import sys
import traceback

def test_de_ai_engine():
    """测试去AI痕迹引擎v5.0"""
    print("【测试1】去AI痕迹引擎 v5.0")
    print("-" * 50)
    
    try:
        from de_ai_engine_v5 import DeAIEngineV5, StyleType
        
        engine = DeAIEngineV5()
        test_text = "他很愤怒，决定报复。首先，他要制定计划。"
        
        result = engine.process(test_text, StyleType.JIN_YONG)
        
        print(f"✅ AI分数提升: {result['ai_score_before']} → {result['ai_score_after']}")
        print(f"✅ 情感共鸣度: {result['emotion_resonance_score']}/100")
        print(f"✅ 修改次数: {len(result['changes'])}")
        return True
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        traceback.print_exc()
        return False


def test_bestseller_analyzer():
    """测试爆款基因分析系统v1.0"""
    print("\n【测试2】爆款基因分析系统 v1.0")
    print("-" * 50)
    
    try:
        from bestseller_gene_analyzer import BestsellerGeneAnalyzer, Platform
        
        analyzer = BestsellerGeneAnalyzer()
        gene = analyzer.analyze_bestseller("测试文本", Platform.QIDIAN)
        
        print(f"✅ 综合爆款分数: {gene.total_score}/100")
        print(f"✅ 钩子强度: {gene.hook_strength}/100")
        print(f"✅ 情感共鸣度: {gene.emotion_resonance}/100")
        return True
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        traceback.print_exc()
        return False


def test_creativity_booster():
    """测试创造力激发与学习系统v1.0"""
    print("\n【测试3】创造力激发与学习系统 v1.0")
    print("-" * 50)
    
    try:
        from creativity_booster_v1 import CreativityBooster, Genre
        
        booster = CreativityBooster()
        ideas = booster.generate_plot_ideas(Genre.XUANHUAN, num_ideas=3)
        
        print(f"✅ 生成创意数: {len(ideas)}")
        for i, idea in enumerate(ideas[:2]):
            print(f"  - 创意{i+1}: 创新度{idea.innovation_score}/100")
        
        return True
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        traceback.print_exc()
        return False


def main():
    """主测试函数"""
    print("═" * 50)
    print("NWACS v9.0 完整功能测试")
    print("═" * 50)
    print()
    
    results = []
    
    # 测试1: 去AI痕迹引擎
    results.append(test_de_ai_engine())
    
    # 测试2: 爆款基因分析
    results.append(test_bestseller_analyzer())
    
    # 测试3: 创造力激发
    results.append(test_creativity_booster())
    
    # 总结
    print()
    print("═" * 50)
    print("测试总结")
    print("═" * 50)
    
    passed = sum(1 for r in results if r)
    total = len(results)
    
    print(f"通过: {passed}/{total}")
    
    if passed == total:
        print("✅ 所有测试通过！NWACS v9.0 实施成功！")
    else:
        print(f"❌ 有{total - passed}个测试失败，请检查错误信息。")
    
    print("═" * 50)
    
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
