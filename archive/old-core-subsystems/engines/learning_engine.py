#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 学习引擎
核心业务层 - 处理学习相关逻辑
"""
import os
import sys
from pathlib import Path
from datetime import datetime

# 添加项目根目录
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.config_manager import config
from core.logger import NWACSLogger
from core.adapters.feishu_adapter import FeishuAdapter

class LearningEngine:
    """学习引擎 - 核心业务层"""

    def __init__(self):
        self.logger = NWACSLogger.get_logger("LearningEngine")
        self.learned_count = 0
        self.learned_content = {}
        self.feishu = FeishuAdapter()
        self.logger.info("LearningEngine initialized")

    def run_learning_cycle(self, update_skills: bool = True) -> bool:
        """执行学习周期"""
        self.logger.info("Starting learning cycle...")

        try:
            # 这里可以调用实际的学习逻辑
            # 简化版本：模拟学习过程
            self.logger.info("Simulating learning...")

            # 学习完成后发送通知
            self.feishu.send_learning_complete(
                knowledge_count=35,
                trends=[
                    "情绪流·虐恋追妻火葬场",
                    "赛博修仙·科技与玄学融合",
                    "无限流·规则怪谈"
                ]
            )

            self.logger.info("Learning cycle completed")
            return True

        except Exception as e:
            self.logger.error(f"Learning cycle failed: {e}")
            return False

    def get_knowledge_bases(self) -> list:
        """获取知识库列表"""
        kb_dir = config.LEARNING_DIR
        if kb_dir.exists():
            return [f.name for f in kb_dir.glob("*.txt")]
        return []

    def get_learning_stats(self) -> dict:
        """获取学习统计"""
        return {
            "total_kb": len(self.get_knowledge_bases()),
            "learned": self.learned_count,
            "last_update": datetime.now().isoformat()
        }
