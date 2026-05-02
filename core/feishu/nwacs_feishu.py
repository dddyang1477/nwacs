# NWACS 飞书集成 - 完整实现
# 支持飞书机器人消息推送
import json
import time
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any

# 配置路径
CONFIG_PATH = Path(__file__).parent.parent / "config" / "feishu_config.json"
LOG_PATH = Path(__file__).parent.parent / "logs" / "feishu_integration.log"


class FeishuConfig:
    """飞书配置管理"""

    DEFAULT_CONFIG = {
        "enable": True,
        "webhook_url": "",
        "secret": "",
        "push_events": [
            "task_start",
            "task_progress",
            "task_complete",
            "learning_complete",
            "quality_warning"
        ],
        "feature_flags": {
            "enable_progress_push": True,
            "enable_learning_report": True,
            "enable_markdown": True
        }
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


class FeishuBot:
    """飞书机器人发送器"""

    def __init__(self, config: Dict):
        self.config = config
        self.webhook_url = config.get("webhook_url", "")
        self.enable = config.get("enable", True) and self.webhook_url

    def send_text(self, message: str, title: Optional[str] = None) -> bool:
        """发送文本消息"""
        if not self.enable:
            print(f"[飞书] 未配置Webhook，模拟发送: {title or ''}\n{message}")
            return True

        try:
            import requests
            import json

            data = {
                "msg_type": "text",
                "content": {
                    "text": f"{title or ''}\n{message}"
                }
            }

            # 设置UTF-8编码的header
            headers = {
                'Content-Type': 'application/json; charset=utf-8'
            }
            
            # 手动序列化并编码为UTF-8
            json_data = json.dumps(data, ensure_ascii=False).encode('utf-8')
            response = requests.post(self.webhook_url, headers=headers, data=json_data)
            result = response.json()

            if result.get("code") == 0:
                print(f"[飞书] 消息发送成功")
                return True
            else:
                print(f"[飞书] 消息发送失败: {result}")
                return False

        except Exception as e:
            print(f"[飞书] 发送异常: {e}")
            return False

    def send_markdown(self, title: str, content: str) -> bool:
        """发送Markdown富文本消息"""
        if not self.enable:
            print(f"[飞书] 未配置Webhook，模拟发送Markdown: {title}")
            return True

        try:
            import requests
            import json

            data = {
                "msg_type": "interactive",
                "card": {
                    "config": {
                        "wide_screen_mode": True
                    },
                    "header": {
                        "template": "blue",
                        "title": {
                            "tag": "plain_text",
                            "content": title
                        }
                    },
                    "elements": [
                        {
                            "tag": "markdown",
                            "content": content
                        }
                    ]
                }
            }

            # 设置UTF-8编码的header
            headers = {
                'Content-Type': 'application/json; charset=utf-8'
            }
            
            # 手动序列化并编码为UTF-8
            json_data = json.dumps(data, ensure_ascii=False).encode('utf-8')
            response = requests.post(self.webhook_url, headers=headers, data=json_data)
            result = response.json()

            if result.get("code") == 0:
                print(f"[飞书] Markdown消息发送成功")
                return True
            else:
                print(f"[飞书] Markdown消息发送失败: {result}")
                # 降级到文本消息
                return self.send_text(content, title)

        except Exception as e:
            print(f"[飞书] Markdown发送异常: {e}")
            return self.send_text(content, title)


class NWACSFeishuIntegration:
    """NWACS飞书集成主入口"""

    def __init__(self):
        self.config = FeishuConfig.load()
        self.bot = FeishuBot(self.config)

        if self.bot.enable:
            print("[NWACS-飞书] 集成模块初始化完成，飞书推送已启用")
        else:
            print("[NWACS-飞书] 集成模块初始化完成，飞书推送未启用（请配置webhook_url）")

    def send_learning_complete(self, report_path: str, knowledge_count: int, top_trends: List[str]):
        """发送学习完成报告"""
        trends_text = "\n".join([f"  - {t}" for t in top_trends])

        title = "🎉 NWACS 学习完成报告"
        content = f"""
⏰ **学习时间**: {time.strftime('%Y-%m-%d %H:%M')}
📊 **学习知识库**: {knowledge_count}个
🔥 **发现热点**:
{trends_text}
📄 **完整报告**: {report_path}
"""

        self.bot.send_markdown(title, content)

    def send_progress_update(self, project: str, progress: int, stage: str):
        """发送进度更新"""
        progress_bar = "═" * (progress // 10) + "░" * (10 - progress // 10)

        title = "📊 NWACS 创作进度"
        content = f"""
**项目**: {project}
**进度**: {progress}% {progress_bar}
**当前阶段**: {stage}
"""

        self.bot.send_markdown(title, content)

    def send_status_update(self):
        """发送系统状态"""
        title = "✅ NWACS 系统状态"
        content = """
**运行状态**: 正常运行
**知识库**: 32个知识库就绪
**Skill**: 28个三级Skill已升级到v7.0
**DeepSeek**: 学习引擎待命
"""

        self.bot.send_markdown(title, content)

    def send_custom_message(self, title: str, message: str):
        """发送自定义消息"""
        self.bot.send_markdown(title, message)

    def test_connection(self) -> bool:
        """测试连接"""
        print("\n" + "="*60)
        print("🧪 NWACS 飞书集成 - 连接测试")
        print("="*60)

        if not self.bot.webhook_url:
            print("\n❌ 请先配置飞书webhook_url！")
            print(f"   配置文件: {CONFIG_PATH}")
            return False

        print(f"\n✅ 配置文件已加载")
        print(f"   Webhook: {self.bot.webhook_url[:30]}...")
        print("\n正在发送测试消息...")

        success = self.send_custom_message(
            "🧪 飞书集成测试",
            f"✅ 测试成功！\n\n当前时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n这是NWACS飞书集成的测试消息。"
        )

        if success:
            print("\n🎉 测试成功！请到飞书查看消息！")
        else:
            print("\n❌ 测试失败，请检查配置！")

        return success

    def run_interactive_menu(self):
        """交互式菜单"""
        print("\n" + "="*60)
        print("📱 NWACS 飞书集成 - 完整实现")
        print("="*60)

        while True:
            print("\n请选择功能:")
            print("  1. 测试飞书连接")
            print("  2. 查看系统状态")
            print("  3. 打开配置文件")
            print("  4. 退出")

            choice = input("\n请输入选项 (1-4): ").strip()

            if choice == "1":
                self.test_connection()
            elif choice == "2":
                self.send_status_update()
            elif choice == "3":
                print(f"\n正在打开配置文件: {CONFIG_PATH}")
                os.startfile(str(CONFIG_PATH))
            elif choice == "4":
                print("\n再见！")
                break
            else:
                print("\n无效选项，请重新输入！")


def create_default_config():
    """创建默认配置"""
    if not CONFIG_PATH.exists():
        FeishuConfig.save(FeishuConfig.DEFAULT_CONFIG)
        print(f"✅ 默认配置已创建: {CONFIG_PATH}")


if __name__ == "__main__":
    create_default_config()
    integration = NWACSFeishuIntegration()
    integration.run_interactive_menu()
