#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 飞书接入适配器
负责与飞书平台交互
"""
import json
import requests
from typing import Optional
from datetime import datetime

from core.config_manager import config
from core.logger import NWACSLogger

class FeishuAdapter:
    """飞书平台接入适配器"""

    def __init__(self):
        self.logger = NWACSLogger.get_logger("FeishuAdapter")
        self.webhook_url = config.feishu_webhook_url
        self.enabled = config.feishu_enabled
        self.logger.info(f"FeishuAdapter initialized (enabled={self.enabled})")

    def send_message(self, message: str, title: str = None) -> bool:
        """发送消息到飞书"""
        if not self.enabled:
            self.logger.warning("Feishu is disabled")
            return False

        if not self.webhook_url:
            self.logger.error("Webhook URL not configured")
            return False

        try:
            data = {
                "msg_type": "text",
                "content": {
                    "text": f"{title or ''}\n{message}" if title else message
                }
            }

            headers = {
                'Content-Type': 'application/json; charset=utf-8'
            }

            json_data = json.dumps(data, ensure_ascii=False).encode('utf-8')
            response = requests.post(
                self.webhook_url,
                headers=headers,
                data=json_data,
                timeout=10
            )

            result = response.json()

            if result.get("code") == 0:
                self.logger.info(f"Message sent successfully: {message[:50]}...")
                return True
            else:
                self.logger.error(f"Failed to send: {result}")
                return False

        except Exception as e:
            self.logger.error(f"Exception sending message: {e}")
            return False

    def send_custom_message(self, title: str, message: str) -> bool:
        """发送自定义消息（别名）"""
        return self.send_message(message, title)

    def send_learning_complete(self, knowledge_count: int, trends: list) -> bool:
        """发送学习完成通知"""
        trends_text = "\n".join([f"  • {t}" for t in trends])

        message = f"""
✅ 学习完成！

📊 统计:
- 知识库数量: {knowledge_count}
- 学习时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🔥 热门趋势:
{trends_text}

⏰ 持续学习中...
"""

        return self.send_message(message, "📚 NWACS 学习完成")

    def send_status_update(self, status: str = "running") -> bool:
        """发送状态更新"""
        message = f"""
📊 系统状态: {status}
时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        return self.send_message(message, "📊 NWACS 状态更新")

    def test_connection(self) -> bool:
        """测试连接"""
        self.logger.info("Testing Feishu connection...")
        return self.send_message("🧪 NWACS连接测试成功！", "✅ 测试消息")
