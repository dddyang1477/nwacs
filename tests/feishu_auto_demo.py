# NWACS 飞书自动推送演示脚本
# 模拟学习引擎完成后自动发送飞书通知
"""
此脚本演示NWACS飞书集成的自动推送机制

实际使用时，当DeepSeek学习引擎完成学习后，会自动调用：
- send_learning_complete() 发送学习完成报告
- send_progress_update() 发送进度更新
- send_status_update() 发送系统状态

现在让我们演示一下这个流程
"""

import sys
from pathlib import Path
from datetime import datetime

# 添加项目根目录
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

print("="*70)
print("🚀 NWACS 飞书自动推送演示")
print("="*70)
print()

# 尝试导入飞书集成
print("[1/5] 检查飞书集成状态...")
try:
    from core.feishu.nwacs_feishu import NWACSFeishuIntegration, FeishuConfig

    config = FeishuConfig.load()
    print(f"   ✅ 配置加载成功")
    print(f"   - enable: {config.get('enable')}")
    print(f"   - webhook_url: {config.get('webhook_url', '')[:50]}...")

    integration = NWACSFeishuIntegration()
    print(f"   ✅ 集成初始化成功")

except Exception as e:
    print(f"   ❌ 初始化失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 模拟学习完成场景
print()
print("[2/5] 模拟学习引擎完成学习...")
learning_results = {
    "knowledge_count": 35,
    "duration": "2小时",
    "completed_kbs": [
        "跨媒体开发知识库.txt",
        "学习进化系统知识库.txt",
        "写作手法与修辞知识库.txt",
        "小说创作灵感库.txt",
        "写作经典技巧精华库.txt"
    ],
    "top_trends": [
        "情绪流·虐恋追妻火葬场",
        "赛博修仙·科技与玄学融合",
        "无限流·规则怪谈"
    ]
}

print(f"   ✅ 学习完成")
print(f"   - 学习知识库数: {learning_results['knowledge_count']}")
print(f"   - 学习时长: {learning_results['duration']}")

# 自动发送飞书通知
print()
print("[3/5] 自动发送飞书通知...")

try:
    # 发送学习完成报告
    print("   📤 发送学习完成报告...")
    integration.send_learning_complete(
        report_path="skills/level2/learnings/学习进化报告/学习报告.md",
        knowledge_count=learning_results['knowledge_count'],
        top_trends=learning_results['top_trends']
    )
    print("   ✅ 学习报告已发送")

except Exception as e:
    print(f"   ❌ 发送失败: {e}")

# 发送系统状态
print()
print("[4/5] 发送系统状态...")
try:
    integration.send_status_update()
    print("   ✅ 系统状态已发送")
except Exception as e:
    print(f"   ❌ 发送失败: {e}")

# 发送自定义消息
print()
print("[5/5] 发送完成通知...")
try:
    integration.send_custom_message(
        "🎉 NWACS 学习演示完成",
        f"""
✅ 学习任务演示完成！

📊 学习统计:
- 知识库数量: {learning_results['knowledge_count']}
- 学习时长: {learning_results['duration']}
- 完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🔥 热门趋势:
{chr(10).join(['  ' + t for t in learning_results['top_trends']])}

💡 提示: 这是演示消息，实际使用时会在学习引擎完成后自动发送
"""
    )
    print("   ✅ 完成通知已发送")
except Exception as e:
    print(f"   ❌ 发送失败: {e}")

print()
print("="*70)
print("✅ 飞书自动推送演示完成！")
print("请检查飞书群，应该收到4条消息：")
print("   1. 学习完成报告")
print("   2. 系统状态")
print("   3. 自定义完成通知")
print("="*70)
