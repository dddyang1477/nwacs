#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 系统优化使用示例
演示所有新增优化功能的使用方式
"""

import sys
import os

# 添加 src/core 到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'core'))

from logger import logger

def demo_llm_optimizer():
    """演示大模型优化器"""
    print("=" * 60)
    print("    演示 1：大模型优化器")
    print("=" * 60)
    
    from llm_optimizer import get_llm_optimizer
    
    optimizer = get_llm_optimizer()
    
    # 查看统计
    stats = optimizer.get_statistics()
    print("\n大模型状态统计:")
    print("  - 启用状态：%s" % stats['enabled'])
    print("  - 当前模型：%s" % stats['current_model'])
    print("  - 缓存大小：%d 条" % stats['cache_size'])
    print("  - 请求计数：%d" % stats['request_count'])
    
    # 模型选择
    best_model = optimizer.select_best_model('创作')
    print("\n为'创作'任务推荐模型：%s" % best_model)
    
    # 成本估算
    cost = optimizer.estimate_cost(1000)
    print("\n1000 字估算成本：$%.4f" % cost)
    
    print("\n✓ 大模型优化器演示完成\n")


def demo_smart_distributor():
    """演示智能分发器"""
    print("=" * 60)
    print("    演示 2：学习内容智能分发")
    print("=" * 60)
    
    from smart_distributor import get_learning_distributor
    
    distributor = get_learning_distributor()
    
    # 测试主题匹配
    test_topics = [
        "短篇小说开篇技巧",
        "世界观修炼体系设定",
        "角色性格塑造方法",
        "战斗场面描写"
    ]
    
    print("\n主题匹配测试:")
    for topic in test_topics:
        matched_skill = distributor.match_skill(topic)
        print("  '%s' -> %s" % (topic, matched_skill))
    
    # 学习建议
    suggestion = distributor.get_learning_suggestions('短篇小说爽文大师')
    print("\n学习建议:")
    print("  %s" % suggestion.get('suggestion'))
    if 'recommended_topics' in suggestion:
        print("  推荐主题:")
        for t in suggestion['recommended_topics'][:3]:
            print("    - %s" % t)
    
    print("\n✓ 智能分发器演示完成\n")


def demo_topic_generator():
    """演示智能主题生成器"""
    print("=" * 60)
    print("    演示 3：智能学习主题生成")
    print("=" * 60)
    
    from topic_generator import get_topic_generator
    
    generator = get_topic_generator()
    
    # 生成学习主题
    print("\n为'短篇小说爽文大师'生成学习主题:")
    topics = generator.generate_topics('短篇小说爽文大师', count=5)
    
    for i, topic in enumerate(topics, 1):
        print("  %d. %s (优先级：%.1f, 类别：%s)" % (
            i, topic['topic'], topic['score'], topic.get('category', '未知')
        ))
    
    # 选择下一个主题
    next_topic = generator.select_next_topic('短篇小说爽文大师')
    print("\n下一个推荐主题：%s" % next_topic)
    
    # 学习计划
    plan = generator.suggest_learning_plan('短篇小说爽文大师', days=7)
    print("\n7 天学习计划:")
    for day in plan['daily_topics']:
        print("  第%d天：%s (%s)" % (
            day['day'], day['topic'], day['category']
        ))
    
    print("\n✓ 主题生成器演示完成\n")


def demo_stats_dashboard():
    """演示数据统计面板"""
    print("=" * 60)
    print("    演示 4：创作数据统计面板")
    print("=" * 60)
    
    from stats_dashboard import get_stats_dashboard
    
    dashboard = get_stats_dashboard()
    
    # 模拟记录写作
    dashboard.record_writing('我的小说', 3000, chapter_count=1)
    dashboard.record_learning('短篇小说爽文大师', '开篇技巧', duration_minutes=30)
    
    # 获取今日摘要
    today = dashboard.get_daily_summary()
    print("\n今日写作统计:")
    print("  - 日期：%s" % today['date'])
    print("  - 总字数：%d" % today['total_words'])
    print("  - 章节数：%d" % today['total_chapters'])
    
    # 获取成就
    badges = dashboard.get_achievement_badges()
    if badges:
        print("\n已获得成就:")
        for badge in badges:
            print("  %s %s" % (badge['icon'], badge['name']))
    else:
        print("\n继续加油，解锁更多成就！")
    
    # 导出报告
    report = dashboard.export_report(format='text')
    print("\n" + report)
    
    print("\n✓ 统计面板演示完成\n")


def demo_template_library():
    """演示模板库"""
    print("=" * 60)
    print("    演示 5：创作模板库")
    print("=" * 60)
    
    from template_library import get_template_library
    
    library = get_template_library()
    
    # 获取所有分类
    categories = library.get_all_categories()
    print("\n模板分类:")
    for cat in categories:
        print("  - %s" % cat)
    
    # 获取具体模板
    template = library.get_template('开篇模板', '冲突开篇')
    print("\n【冲突开篇】模板:")
    print("  说明：%s" % template.get('description', ''))
    print("  结构:")
    for i, step in enumerate(template.get('structure', []), 1):
        print("    %d. %s" % (i, step))
    print("  示例：%s" % template.get('example', '')[:100] + "...")
    
    # 随机模板
    random_temp = library.get_random_template('爽点模板')
    print("\n随机爽点模板：%s" % random_temp.get('name', '未知'))
    
    # 搜索模板
    results = library.search_templates('打脸')
    print("\n搜索'打脸'相关模板:")
    for result in results:
        print("  - %s/%s" % (result['category'], result['name']))
    
    print("\n✓ 模板库演示完成\n")


def demo_git_sync():
    """演示 Git 同步增强"""
    print("=" * 60)
    print("    演示 6：GitHub 同步增强")
    print("=" * 60)
    
    from git_sync_enhanced import get_sync_enhancer
    
    enhancer = get_sync_enhancer()
    
    # 检查网络
    print("\n检查网络连接...")
    network_ok = enhancer.check_network()
    print("  网络状态：%s" % ("正常" if network_ok else "异常"))
    
    # 获取同步状态
    status = enhancer.get_sync_status()
    print("\n同步状态:")
    if 'message' in status:
        print("  %s" % status['message'])
    else:
        print("  最后同步：%s" % status['last_sync'])
        print("  状态：%s" % status['status'])
        print("  总次数：%d" % status['total_syncs'])
        print("  成功：%d 次" % status['success_count'])
        print("  失败：%d 次" % status['failed_count'])
    
    print("\n✓ Git 同步演示完成\n")


def main():
    """主函数"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 15 + "NWACS 系统优化功能演示" + " " * 15 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    try:
        # 依次演示各个模块
        demo_llm_optimizer()
        demo_smart_distributor()
        demo_topic_generator()
        demo_stats_dashboard()
        demo_template_library()
        demo_git_sync()
        
        print("\n")
        print("=" * 60)
        print("    所有演示完成！")
        print("=" * 60)
        print("\n优化功能列表:")
        print("  ✓ 大模型连接优化（余额检测、限流重试、本地缓存）")
        print("  ✓ 学习内容智能分发（精准匹配、避免重复）")
        print("  ✓ GitHub 同步增强（重试机制、网络检测、备份）")
        print("  ✓ 智能主题生成（动态生成、热点分析、优先级）")
        print("  ✓ 创作数据统计（字数统计、学习记录、成就系统）")
        print("  ✓ 模板素材库（开篇模板、爽点模板、描写素材）")
        print("\n提示：这些功能已集成到系统中，会自动运行")
        print("=" * 60)
        print("\n")
        
    except Exception as e:
        logger.log_exception(e, "演示运行")
        print("\n演示过程中出现异常，请查看日志")


if __name__ == "__main__":
    main()
