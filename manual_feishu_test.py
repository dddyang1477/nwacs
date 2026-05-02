# -*- coding: utf-8 -*-
"""
NWACS 飞书推送测试 - 手动触发
"""
import sys
from pathlib import Path
from datetime import datetime

print("="*60)
print("🚀 NWACS 飞书推送测试")
print("="*60)

# 添加项目路径
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

# 导入飞书集成
try:
    from core.feishu.nwacs_feishu import NWACSFeishuIntegration
    print("✅ 飞书集成模块加载成功")
except Exception as e:
    print(f"❌ 导入失败: {e}")
    sys.exit(1)

def test_feishu_push():
    """测试飞书推送"""
    print("\n" + "="*60)
    print("📱 测试飞书推送功能")
    print("="*60)

    try:
        # 初始化集成
        integration = NWACSFeishuIntegration()

        print("\n[1/4] 测试 - 发送系统状态...")
        integration.send_status_update()

        print("\n[2/4] 测试 - 发送进度更新...")
        integration.send_progress_update(
            project="测试项目",
            progress=50,
            stage="测试阶段"
        )

        print("\n[3/4] 测试 - 发送自定义消息...")
        integration.send_custom_message(
            "🧪 手动测试消息",
            f"✅ NWACS飞书推送测试\n\n测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n如果看到这条消息，说明飞书推送功能正常！"
        )

        print("\n[4/4] 测试 - 发送学习完成报告...")
        integration.send_learning_complete(
            report_path="测试报告.md",
            knowledge_count=35,
            top_trends=[
                "情绪流·虐恋追妻火葬场",
                "赛博修仙",
                "无限流·规则怪谈"
            ]
        )

        print("\n" + "="*60)
        print("✅ 所有测试完成！")
        print("请检查飞书群，是否收到了4条消息？")
        print("="*60)

    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_feishu_push()
