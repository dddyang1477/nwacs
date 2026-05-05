#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 服务编排层
连接接入层和核心业务层
"""
import sys
from pathlib import Path

# 添加项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.config_manager import config
from core.logger import NWACSLogger

class ServiceOrchestrator:
    """服务编排器 - 协调各层工作"""

    def __init__(self):
        self.logger = NWACSLogger.get_logger("ServiceOrchestrator")
        self.feishu_adapter = None
        self.learning_engine = None
        self.logger.info("ServiceOrchestrator initialized")

    def initialize_feishu(self):
        """初始化飞书接入"""
        try:
            from core.adapters.feishu_adapter import FeishuAdapter
            self.feishu_adapter = FeishuAdapter()
            self.logger.info("Feishu adapter initialized")
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize Feishu: {e}")
            return False

    def initialize_learning(self):
        """初始化学习引擎"""
        try:
            from core.engines.learning_engine import LearningEngine
            self.learning_engine = LearningEngine()
            self.logger.info("Learning engine initialized")
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize Learning: {e}")
            return False

    def process_command(self, command: str, user_id: str = None) -> str:
        """处理用户命令"""
        self.logger.info(f"Processing command: {command} from user: {user_id}")

        command_lower = command.lower().strip()

        # 命令路由
        if command_lower in ['status', '状态']:
            return self.get_status()
        elif command_lower in ['learn', '学习']:
            return self.start_learning()
        elif command_lower in ['report', '报告']:
            return self.get_report()
        elif command_lower in ['help', '帮助']:
            return self.get_help()
        elif command_lower in ['setup', '配置']:
            return self.run_setup()
        elif command_lower in ['stats', '统计']:
            return self.get_stats()
        else:
            return self.unknown_command(command)

    def get_status(self) -> str:
        """获取系统状态"""
        status = f"""
📊 **NWACS 系统状态**

🕐 时间: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

✅ 状态: 运行中
📦 版本: v7.0
🧠 学习引擎: {'就绪' if self.learning_engine else '未初始化'}
📱 飞书集成: {'就绪' if self.feishu_adapter else '未初始化'}

📚 知识库: 35个
🎯 Skill: 28个（v7.0/v8.0）

⏰ 服务器运行正常
"""
        self.logger.info("Status requested")
        return status

    def start_learning(self) -> str:
        """启动学习"""
        if not self.learning_engine:
            return "❌ 学习引擎未初始化"

        self.logger.info("Starting learning...")
        try:
            self.learning_engine.run_learning_cycle(update_skills=True)
            return "✅ 学习任务完成！\n请查看日志获取详情。"
        except Exception as e:
            self.logger.error(f"Learning failed: {e}")
            return f"❌ 学习失败: {str(e)}"

    def get_report(self) -> str:
        """获取报告"""
        self.logger.info("Report requested")
        return "📄 学习报告功能开发中..."

    def get_help(self) -> str:
        """获取帮助"""
        help_text = """
📖 **NWACS 可用命令**

1. **status** - 查看系统状态
2. **learn** - 开始学习
3. **report** - 获取学习报告
4. **stats** - 查看统计
5. **setup** - 配置向导
6. **help** - 显示帮助

💡 发送命令即可执行对应功能
"""
        self.logger.info("Help requested")
        return help_text

    def run_setup(self) -> str:
        """运行配置向导"""
        self.logger.info("Setup requested")
        setup_guide = """
🔧 **NWACS 配置向导**

步骤1: 检查飞书配置
- Webhook: {webhook}
- 状态: {status}

步骤2: 测试连接
- 运行: `py feishu_simple_test.py`

步骤3: 配置ngrok（可选）
- 需要双向通信时配置

📖 查看完整指南: 飞书指令服务器配置指南.md
"""
        webhook = config.feishu_webhook_url
        webhook_short = webhook[:50] + "..." if len(webhook) > 50 else webhook
        status = "✅ 已配置" if webhook else "❌ 未配置"

        return setup_guide.format(webhook=webhook_short, status=status)

    def get_stats(self) -> str:
        """获取统计"""
        stats = """
📈 **NWACS 学习统计**

📚 知识库总数: 35个
- 题材知识库: 12个
- 专业技能库: 13个
- 素材资源库: 6个
- v7.0新增: 2个
- 市场动态: 2个

🎯 Skill总数: 28个
- Level 2 Skill: 24个（v7.0/v8.0）
- Level 3 Skill: 28个

🔥 热门题材: 情绪流、赛博修仙、无限流

⏰ 持续学习中...
"""
        self.logger.info("Stats requested")
        return stats

    def unknown_command(self, command: str) -> str:
        """未知命令"""
        self.logger.warning(f"Unknown command: {command}")
        return f"⚠️ 未知命令: {command}\n\n发送 **help** 查看可用命令"


# 全局服务实例
orchestrator = ServiceOrchestrator()
