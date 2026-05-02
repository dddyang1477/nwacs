# NWACS 微信集成模块 - 概念验证实现
# 支持企业微信机器人 + 个人微信itchat双方案
import json
import time
import os
from pathlib import Path
from typing import Dict, List, Optional

# 配置路径
CONFIG_PATH = Path(__file__).parent.parent / "config" / "wechat_config.json"
LOG_PATH = Path(__file__).parent.parent / "logs" / "wechat_integration.log"


class WechatConfig:
    """微信配置管理"""

    DEFAULT_CONFIG = {
        "enable": True,
        "mode": "qiyewechat",  # qiyewechat 或 personal
        "qiyewechat": {
            "webhook_url": "",
            "secret": "",
            "chat_id": ""
        },
        "personal": {
            "auto_login": True
        },
        "push_events": [
            "task_start",
            "task_progress",
            "task_complete",
            "learning_complete",
            "quality_warning"
        ]
    }

    @classmethod
    def load(cls) -> Dict:
        """加载配置"""
        if not CONFIG_PATH.exists():
            cls.save(cls.DEFAULT_CONFIG)
            return cls.DEFAULT_CONFIG
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)

    @classmethod
    def save(cls, config: Dict):
        """保存配置"""
        os.makedirs(CONFIG_PATH.parent, exist_ok=True)
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)


class WechatSender:
    """微信消息发送器"""

    def __init__(self, config: Dict):
        self.config = config
        self.mode = config.get("mode", "qiyewechat")

    def send(self, message: str, title: Optional[str] = None) -> bool:
        """发送消息"""
        try:
            if self.mode == "qiyewechat":
                return self._send_qiyewechat(message, title)
            elif self.mode == "personal":
                return self._send_personal(message, title)
            else:
                print(f"[Wechat] 未知模式: {self.mode}")
                return False
        except Exception as e:
            print(f"[Wechat] 发送失败: {e}")
            return False

    def _send_qiyewechat(self, message: str, title: Optional[str] = None) -> bool:
        """企业微信机器人发送"""
        webhook_url = self.config.get("qiyewechat", {}).get("webhook_url", "")
        if not webhook_url:
            print("[Wechat] 企业微信未配置webhook_url，请在config/wechat_config.json中配置")
            print(f"[Wechat] 模拟发送消息: {title or ''}\n{message}")
            return True

        import requests
        data = {
            "msgtype": "markdown",
            "markdown": {
                "content": f"# {title or 'NWACS通知'}\n\n{message}"
            }
        }
        response = requests.post(webhook_url, json=data)
        return response.status_code == 200

    def _send_personal(self, message: str, title: Optional[str] = None) -> bool:
        """个人微信发送（itchat）"""
        print(f"[Wechat] 个人微信模式: {title or ''}\n{message}")
        # 实际使用时需要集成itchat
        return True


class WechatReceiver:
    """微信消息接收器"""

    def __init__(self, config: Dict):
        self.config = config
        self.message_queue = []
        self.running = False

    def start(self):
        """启动接收服务"""
        self.running = True
        print("[Wechat] 消息接收器启动")

    def stop(self):
        """停止接收服务"""
        self.running = False

    def get_next_message(self) -> Optional[Dict]:
        """获取下一条消息"""
        if self.message_queue:
            return self.message_queue.pop(0)
        return None


class WechatRouter:
    """指令路由器 - 把微信消息路由到NWACS"""

    COMMAND_PREFIX = "/"
    COMMANDS = {
        "start": "开始新创作项目",
        "status": "查看当前状态",
        "progress": "查看创作进度",
        "learn": "启动DeepSeek学习",
        "report": "获取最新学习报告",
        "help": "显示帮助"
    }

    def __init__(self, config: Dict):
        self.config = config
        self.sender = WechatSender(config)
        self.receiver = WechatReceiver(config)

    def process_message(self, message: str) -> str:
        """处理微信消息"""
        message = message.strip()

        # 快捷命令处理
        if message.startswith(self.COMMAND_PREFIX):
            return self._process_command(message[1:])

        # 自然语言处理
        return self._process_natural_language(message)

    def _process_command(self, command: str) -> str:
        """处理快捷命令"""
        command = command.lower()

        if command == "help":
            return self._generate_help_message()
        elif command == "status":
            return self._get_status()
        elif command == "learn":
            return self._start_learning()
        elif command == "start":
            return "好的，请告诉我您要创作什么类型的小说？"
        else:
            return f"未知命令: {command}\n输入 /help 查看帮助"

    def _process_natural_language(self, message: str) -> str:
        """处理自然语言"""
        # 这里可以对接DeepSeek做NLP处理
        return f"收到您的需求: '{message}'\n正在启动NWACS处理..."

    def _generate_help_message(self) -> str:
        """生成帮助信息"""
        help_text = "【NWACS 微信助手 帮助】\n\n"
        for cmd, desc in self.COMMANDS.items():
            help_text += f"/{cmd} - {desc}\n"
        help_text += "\n也可以直接说您的需求，如：'帮我写个玄幻大纲'"
        return help_text

    def _get_status(self) -> str:
        """获取系统状态"""
        return "【NWACS 系统状态】\n\n✅ 运行正常\n📚 32个知识库就绪\n🔧 DeepSeek学习引擎待命\n🎯 28个三级Skill已升级到v7.0"

    def _start_learning(self) -> str:
        """启动学习"""
        return "好的！正在启动DeepSeek联网学习...\n完成后会给您发报告"


class NWACSWechatIntegration:
    """NWACS微信集成主入口"""

    def __init__(self):
        self.config = WechatConfig.load()
        self.router = WechatRouter(self.config)
        print("[NWACS-微信] 集成模块初始化完成")

    def send_status_update(self, project: str, progress: int, stage: str):
        """发送状态更新"""
        progress_bar = "═" * (progress // 10) + "░" * (10 - progress // 10)
        message = (
            f"**项目**: {project}\n"
            f"**进度**: {progress}% {progress_bar}\n"
            f"**当前阶段**: {stage}"
        )
        self.router.sender.send(message, title="NWACS 创作进度")

    def send_learning_complete(self, report_path: str, knowledge_count: int, top_trends: List[str]):
        """发送学习完成报告"""
        trends_text = "\n".join([f"  - {t}" for t in top_trends])
        message = (
            f"**学习时间**: {time.strftime('%Y-%m-%d %H:%M')}\n"
            f"**学习知识库**: {knowledge_count}个\n"
            f"**发现热点**:\n{trends_text}\n\n"
            f"📄 完整报告: {report_path}"
        )
        self.router.sender.send(message, title="NWACS 学习完成报告")

    def run_interactive_demo(self):
        """交互式演示"""
        print("\n=" * 50)
        print("📱 NWACS 微信集成 - 概念验证演示")
        print("=" * 50)
        print("\n💡 说明：")
        print("   这是一个概念验证，模拟微信交互")
        print("   真实使用时需要配置企业微信webhook_url")
        print("=" * 50)

        while True:
            print("\n请输入指令（输入 'quit' 退出）:")
            user_input = input("> ").strip()

            if user_input.lower() in ["quit", "exit", "q"]:
                print("再见！")
                break

            response = self.router.process_message(user_input)
            print(f"\n[NWACS回复]: {response}")


def create_default_config():
    """创建默认配置文件"""
    config = WechatConfig.DEFAULT_CONFIG
    WechatConfig.save(config)
    print(f"[Wechat] 默认配置已创建: {CONFIG_PATH}")


if __name__ == "__main__":
    print("=" * 60)
    print("📱 NWACS 微信集成 - 概念验证")
    print("=" * 60)
    integration = NWACSWechatIntegration()
    integration.run_interactive_demo()
