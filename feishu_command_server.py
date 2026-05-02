#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 飞书指令服务器
飞书发送指令到NWACS，NWACS执行并返回结果

功能：
- 接收飞书消息
- 解析指令
- 执行相应操作
- 返回结果到飞书
"""

import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

# 配置
PROJECT_ROOT = Path(__file__).parent
CONFIG_PATH = PROJECT_ROOT / "config" / "feishu_config.json"
sys.path.insert(0, str(PROJECT_ROOT))

VERSION = "1.0"
SERVER_PORT = 8088

print("="*70)
print("🚀 NWACS 飞书指令服务器 v" + VERSION)
print("="*70)
print()

# 尝试导入飞书集成
try:
    from core.feishu.nwacs_feishu import NWACSFeishuIntegration
    FEISHU_AVAILABLE = True
    print("✅ 飞书集成模块加载成功")
except Exception as e:
    FEISHU_AVAILABLE = False
    print(f"⚠️ 飞书集成模块加载失败: {e}")

# 尝试导入学习系统
try:
    from core.comprehensive_learning import AutoLearningSystem
    LEARNING_AVAILABLE = True
    print("✅ 学习模块加载成功")
except Exception as e:
    LEARNING_AVAILABLE = False
    print(f"⚠️ 学习模块加载失败: {e}")

print()
print("📡 服务器配置:")
print(f"   端口: {SERVER_PORT}")
print(f"   飞书集成: {'启用' if FEISHU_AVAILABLE else '禁用'}")
print(f"   学习系统: {'启用' if LEARNING_AVAILABLE else '禁用'}")
print()

class FeishuCommandHandler(BaseHTTPRequestHandler):
    """处理飞书指令"""

    def log_message(self, format, *args):
        """自定义日志格式"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {format % args}")

    def send_feishu_response(self, message):
        """发送响应到飞书"""
        if not FEISHU_AVAILABLE:
            return

        try:
            integration = NWACSFeishuIntegration()
            integration.send_custom_message("📨 NWACS 指令响应", message)
            self.log_message("响应已发送到飞书")
        except Exception as e:
            self.log_message(f"发送响应失败: {e}")

    def do_GET(self):
        """处理GET请求"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        html = """
        <html>
        <head><meta charset="utf-8"><title>NWACS 飞书指令服务器</title></head>
        <body>
        <h1>🚀 NWACS 飞书指令服务器</h1>
        <h2>状态: 运行中 ✅</h2>
        <p>时间: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</p>
        <h3>可用指令:</h3>
        <ul>
            <li><b>status</b> - 查看系统状态</li>
            <li><b>learn</b> - 立即开始学习</li>
            <li><b>report</b> - 发送学习报告</li>
            <li><b>help</b> - 显示帮助</li>
        </ul>
        <h3>使用方法:</h3>
        <p>在飞书群中 @机器人 发送指令即可</p>
        </body>
        </html>
        """
        self.wfile.write(html.encode('utf-8'))

    def do_POST(self):
        """处理POST请求（飞书回调）"""
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        body = post_data.decode('utf-8')

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        response = {"code": 0, "msg": "success"}
        self.wfile.write(json.dumps(response).encode('utf-8'))

        # 解析飞书消息
        try:
            data = json.loads(body)
            self.log_message("收到飞书消息: %s", json.dumps(data, ensure_ascii=False))

            # 提取消息内容
            event = data.get('event', {})
            message = event.get('text', '')
            sender = event.get('sender', {}).get('sender_id', {}).get('open_id', 'unknown')

            self.log_message(f"来自用户: {sender}")
            self.log_message(f"消息内容: {message}")

            # 处理指令
            self.handle_command(message.strip(), sender)

        except Exception as e:
            self.log_message(f"处理消息失败: {e}")

    def handle_command(self, message, sender):
        """处理指令"""
        self.log_message(f"处理指令: {message}")

        message_lower = message.lower()

        # 帮助指令
        if 'help' in message_lower or '帮助' in message:
            response = """
📖 **NWACS 指令帮助**

可用指令：
1. **status** - 查看系统状态
2. **learn** - 立即开始学习
3. **report** - 发送学习报告
4. **stats** - 查看学习统计

发送方式：@机器人 + 指令
            """
            self.send_feishu_response(response)
            return

        # 状态指令
        if 'status' in message_lower or '状态' in message:
            response = self.get_system_status()
            self.send_feishu_response(response)
            return

        # 学习指令
        if 'learn' in message_lower or '学习' in message:
            self.log_message("开始执行学习...")
            self.start_learning()
            return

        # 报告指令
        if 'report' in message_lower or '报告' in message:
            self.send_learning_report()
            return

        # 统计指令
        if 'stats' in message_lower or '统计' in message:
            response = self.get_learning_stats()
            self.send_feishu_response(response)
            return

        # 未知指令
        response = f"""
⚠️ 未知指令: {message}

发送 **help** 查看可用指令
        """
        self.send_feishu_response(response)

    def get_system_status(self):
        """获取系统状态"""
        status = f"""
📊 **NWACS 系统状态**

🕐 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

✅ 状态: 运行中
📦 版本: v7.0
🧠 学习引擎: {'就绪' if LEARNING_AVAILABLE else '未就绪'}
📱 飞书集成: {'就绪' if FEISHU_AVAILABLE else '未就绪'}

📚 知识库: 35个
🎯 Skill: 28个（v7.0/v8.0）

⏰ 服务器运行正常
        """
        return status

    def start_learning(self):
        """开始学习"""
        if not LEARNING_AVAILABLE:
            self.send_feishu_response("⚠️ 学习模块未就绪")
            return

        try:
            self.send_feishu_response("📚 开始执行学习任务...")

            # 导入并运行学习
            from core.comprehensive_learning import AutoLearningSystem
            learning = AutoLearningSystem()
            learning.run_learning_cycle(update_skills=True)

            self.send_feishu_response("✅ 学习任务完成！\n请查看上方日志获取详情。")

        except Exception as e:
            error_msg = f"❌ 学习失败: {str(e)}"
            self.log_message(error_msg)
            self.send_feishu_response(error_msg)

    def send_learning_report(self):
        """发送学习报告"""
        if not FEISHU_AVAILABLE:
            return

        try:
            integration = NWACSFeishuIntegration()
            integration.send_learning_complete(
                report_path="skills/level2/learnings/学习进化报告/",
                knowledge_count=35,
                top_trends=[
                    "情绪流·虐恋追妻火葬场",
                    "赛博修仙·科技与玄学融合",
                    "无限流·规则怪谈"
                ]
            )
            self.send_feishu_response("📄 学习报告已发送！")

        except Exception as e:
            self.send_feishu_response(f"❌ 发送失败: {str(e)}")

    def get_learning_stats(self):
        """获取学习统计"""
        stats = """
📈 **学习统计**

📚 知识库总数: 35个
- 题材知识库: 12个
- 专业技能库: 13个
- 素材资源库: 6个
- v7.0新增: 2个
- 市场动态: 2个

🎯 Skill总数: 28个
- Level 2 Skill: 24个（v7.0/v8.0）
- Level 3 Skill: 28个

📊 DeepSeek学习: 已完成
🔥 热门题材: 情绪流、赛博修仙、无限流

⏰ 持续学习中...
        """
        return stats


def main():
    """主函数"""
    print("="*70)
    print("🌐 启动飞书指令服务器...")
    print(f"📡 监听端口: {SERVER_PORT}")
    print("="*70)
    print()

    try:
        server = HTTPServer(('0.0.0.0', SERVER_PORT), FeishuCommandHandler)
        print(f"✅ 服务器启动成功！")
        print(f"📡 访问地址: http://localhost:{SERVER_PORT}")
        print()
        print("📋 可用指令:")
        print("   - status : 查看系统状态")
        print("   - learn  : 开始学习")
        print("   - report : 发送学习报告")
        print("   - help   : 显示帮助")
        print()
        print("按 Ctrl+C 停止服务器")
        print("="*70)

        server.serve_forever()

    except KeyboardInterrupt:
        print("\n\n👋 服务器已停止")
    except Exception as e:
        print(f"\n❌ 服务器启动失败: {e}")


if __name__ == "__main__":
    main()
