#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS Skill自主学习管理器
为所有Skill添加独立的自主学习能力
支持真正的联网学习功能
"""

import time
import threading
import json
import os
from datetime import datetime
from logger import logger

# 尝试导入联网学习模块
try:
    from web_learning import get_web_learning
    WEB_LEARNING_ENABLED = True
except ImportError:
    WEB_LEARNING_ENABLED = False
    logger.warning("联网学习模块未启用，使用模拟学习")

# 尝试导入协作模块
try:
    from skill_collaboration import get_skill_collaboration
    COLLABORATION_ENABLED = True
except ImportError:
    COLLABORATION_ENABLED = False
    logger.warning("协作模块未启用")

# 大模型分析开关
LLM_ANALYSIS_ENABLED = True

class SkillLearner:
    """单个Skill的学习器"""

    # Skill文件路径映射
    SKILL_FILE_MAP = {
        '世界观构造师': 'skills/level2/03_二级Skill_世界观构造师.md',
        '剧情构造师': 'skills/level2/04_二级Skill_剧情构造师.md',
        '角色塑造师': 'skills/level2/07_二级Skill_角色塑造师.md',
        '战斗设计师': 'skills/level2/08_二级Skill_战斗设计师.md',
        '场景构造师': 'skills/level2/05_二级Skill_场景构造师.md',
        '对话设计师': 'skills/level2/06_二级Skill_对话设计师.md',
        '写作技巧大师': 'skills/level2/09_二级Skill_写作技巧大师.md',
        '去AI痕迹监督官': 'skills/level2/10_二级Skill_去AI痕迹监督官.md',
        '质量审计师': 'skills/level2/11_二级Skill_质量审计师.md',
        '学习大师': 'skills/level2/30_二级Skill_学习大师.md',
        '规则掌控者': 'skills/level2/31_二级Skill_规则掌控者.md',
        '词汇大师': 'skills/level2/32_二级Skill_词汇大师.md',
        '短篇小说爽文大师': 'skills/level2/11_二级Skill_短篇小说爽文大师.md',
        '小说总调度官': 'skills/level2/01_二级Skill_小说总调度官.md',
    }

    def __init__(self, skill_name, skill_type, learning_topics):
        self.skill_name = skill_name
        self.skill_type = skill_type
        self.learning_topics = learning_topics
        self.is_learning = False
        self.learning_count = 0
        self.error_count = 0
        self.last_learning_time = 0
        self.learning_interval = 1800  # 每30分钟学习一次
        self._topic_index = 0
        
        logger.info("初始化Skill学习器: %s" % skill_name)
    
    def start_learning_loop(self):
        """启动学习循环"""
        thread = threading.Thread(target=self.learning_loop)
        thread.daemon = False
        thread.start()
    
    def learning_loop(self):
        """学习循环"""
        logger.debug("%s 学习循环启动" % self.skill_name)
        
        while True:
            try:
                current_time = time.time()
                
                # 检查是否需要学习
                if current_time - self.last_learning_time >= self.learning_interval:
                    if not self.is_learning:
                        self.execute_learning()
                
                time.sleep(60)  # 每分钟检查一次
            except Exception as e:
                logger.log_exception(e, "%s learning_loop" % self.skill_name)
                self.error_count += 1
    
    def execute_learning(self):
        """执行学习"""
        self.is_learning = True
        self.last_learning_time = time.time()

        try:
            # 选择学习主题
            topic = self.select_topic()
            logger.info("%s 正在学习: %s" % (self.skill_name, topic))

            # 执行学习（联网或模拟）
            learning_result = self.simulate_learning(topic)

            # 更新学习记录
            self.update_learning_record(topic)

            # 分发学习内容到对应的Skill文件
            if learning_result:
                self.distribute_learning_content(topic, learning_result)

                # 分享到知识库（协作功能）
                if COLLABORATION_ENABLED:
                    try:
                        collab = get_skill_collaboration()
                        collab.share_learning_to_knowledge_base(self.skill_name, topic, learning_result)

                        # 大模型分析（如果启用）
                        if LLM_ANALYSIS_ENABLED and collab.llm_enabled:
                            llm_result = collab.analyze_with_llm(learning_result, "skill_update")
                            if llm_result:
                                logger.info("%s 大模型分析完成" % self.skill_name)
                                # 可以将分析结果也加入知识库
                                collab.share_learning_to_knowledge_base(
                                    self.skill_name,
                                    topic + "_LLM分析",
                                    llm_result
                                )
                    except Exception as e:
                        logger.log_exception(e, "%s 协作功能" % self.skill_name)

            self.learning_count += 1
            logger.info("%s 学习完成" % self.skill_name)

        except Exception as e:
            logger.log_exception(e, "%s execute_learning" % self.skill_name)
            self.error_count += 1
        finally:
            self.is_learning = False
    
    def select_topic(self):
        """选择下一个学习主题"""
        if not self.learning_topics:
            return "通用写作技巧"
        
        topic = self.learning_topics[self._topic_index]
        self._topic_index = (self._topic_index + 1) % len(self.learning_topics)
        return topic
    
    def simulate_learning(self, topic):
        """学习过程（联网版）"""
        logger.debug("%s 正在深入学习: %s" % (self.skill_name, topic))

        if WEB_LEARNING_ENABLED:
            # 真正的联网学习
            try:
                web_learning = get_web_learning()
                learning_result = web_learning.search_and_learn(self.skill_name, topic)

                if learning_result:
                    logger.info("%s 联网学习完成，获得 %d 条要点" % (
                        self.skill_name,
                        len(learning_result.get('key_points', []))
                    ))
                    return learning_result
            except Exception as e:
                logger.log_exception(e, "%s 联网学习" % self.skill_name)
                # 如果联网失败，使用模拟学习
                time.sleep(2)
        else:
            # 模拟学习时间
            time.sleep(2)

        # 模拟学习成果（备用）
        learning_outcome = {
            'topic': topic,
            'skill_name': self.skill_name,
            'learned_points': self.generate_learning_points(topic),
            'timestamp': datetime.now().isoformat()
        }

        return learning_outcome
    
    def generate_learning_points(self, topic):
        """生成学习要点（模拟）"""
        points = []
        
        if '情感' in topic:
            points = ["微表情描写技巧", "情感递进表达", "心理活动刻画"]
        elif '人物' in topic:
            points = ["角色弧光设计", "性格一致性", "动机合理性"]
        elif '剧情' in topic:
            points = ["节奏控制", "冲突设计", "伏笔埋设"]
        elif '世界观' in topic:
            points = ["规则一致性", "细节丰富度", "独特性"]
        elif '战斗' in topic:
            points = ["招式设计", "节奏控制", "场面描写"]
        else:
            points = ["写作技巧提升", "语言表达优化", "风格统一"]
        
        return points
    
    def update_learning_record(self, topic):
        """更新学习记录"""
        record = {
            'skill_name': self.skill_name,
            'skill_type': self.skill_type,
            'topic': topic,
            'timestamp': datetime.now().isoformat(),
            'learning_count': self.learning_count
        }
        
        # 保存到学习记录文件
        self._save_to_record(record)
    
    def _save_to_record(self, record):
        """保存记录到文件"""
        record_file = "skill_learning_records.json"
        
        try:
            if os.path.exists(record_file):
                # 检查文件是否为空
                file_size = os.path.getsize(record_file)
                if file_size == 0:
                    records = []
                else:
                    with open(record_file, 'r', encoding='utf-8') as f:
                        try:
                            records = json.load(f)
                        except json.JSONDecodeError:
                            # 文件内容不是有效JSON，重新初始化
                            records = []
            else:
                records = []
            
            records.append(record)
            
            with open(record_file, 'w', encoding='utf-8') as f:
                json.dump(records, f, ensure_ascii=False, indent=2)
            
        except Exception as e:
            logger.log_exception(e, "%s _save_to_record" % self.skill_name)

    def distribute_learning_content(self, topic, learning_result):
        """将学习内容分发到对应的Skill文件"""
        skill_file = self.SKILL_FILE_MAP.get(self.skill_name)
        if not skill_file:
            logger.debug("%s 未配置Skill文件路径" % self.skill_name)
            return False

        # 确保路径是相对于工作目录
        if not os.path.isabs(skill_file):
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            skill_file = os.path.join(base_dir, skill_file)

        if not os.path.exists(skill_file):
            logger.warning("%s Skill文件不存在: %s" % (self.skill_name, skill_file))
            return False

        try:
            # 读取现有内容
            with open(skill_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # 生成学习内容章节
            chapter_title = "## 学习成果 - %s\n\n" % datetime.now().strftime('%Y-%m-%d')
            chapter_content = chapter_title

            if isinstance(learning_result, dict):
                # 添加学习主题
                chapter_content += "**学习主题：** %s\n\n" % topic

                # 添加关键数据
                if 'key_points' in learning_result and learning_result['key_points']:
                    chapter_content += "**关键数据：**\n"
                    for point in learning_result['key_points'][:5]:
                        chapter_content += "- %s\n" % point
                    chapter_content += "\n"

                # 添加趋势分析
                if 'trends' in learning_result and learning_result['trends']:
                    chapter_content += "**趋势分析：**\n"
                    for trend in learning_result['trends'][:3]:
                        chapter_content += "- %s\n" % trend
                    chapter_content += "\n"

                # 添加写作技巧
                if 'tips' in learning_result and learning_result['tips']:
                    chapter_content += "**写作技巧：**\n"
                    for tip in learning_result['tips'][:3]:
                        if len(tip) < 200:
                            chapter_content += "- %s\n" % tip
                    chapter_content += "\n"

                # 添加搜索结果摘要
                if 'search_results' in learning_result and learning_result['search_results']:
                    chapter_content += "**参考资料：**\n"
                    for i, result in enumerate(learning_result['search_results'][:2], 1):
                        title = result.get('title', '未知')
                        chapter_content += "- %s\n" % title
                    chapter_content += "\n"
            else:
                # 简单文本
                chapter_content += "%s\n\n" % str(learning_result)

            chapter_content += "---\n*本章节由自动学习系统于 %s 生成*\n\n" % datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # 查找插入位置（在文件末尾或特定标记处）
            marker = "<!-- 学习成果自动插入位置 -->"
            if marker in content:
                # 在标记处插入
                content = content.replace(marker, chapter_content + marker)
            else:
                # 在文件末尾添加
                content += "\n\n" + chapter_content

            # 保存更新
            with open(skill_file, 'w', encoding='utf-8') as f:
                f.write(content)

            logger.info("%s 学习内容已分发到: %s" % (self.skill_name, skill_file))
            return True

        except Exception as e:
            logger.log_exception(e, "%s distribute_learning_content" % self.skill_name)
            return False

    def get_stats(self):
        """获取统计信息"""
        return {
            'skill_name': self.skill_name,
            'skill_type': self.skill_type,
            'learning_count': self.learning_count,
            'error_count': self.error_count,
            'is_learning': self.is_learning,
            'last_learning_time': self.last_learning_time,
            'learning_topics': self.learning_topics
        }

class SkillLearningManager:
    """Skill学习管理器"""
    
    def __init__(self):
        self.skill_learners = {}
        self.running = False
        
        # 定义各Skill的学习主题
        self.skill_topics = {
            '世界观构造师': [
                '玄幻世界构建技巧',
                '都市异能设定方法',
                '科幻世界规则设计',
                '历史架空背景构建',
                '世界规则一致性维护'
            ],
            '剧情构造师': [
                '三幕式结构设计',
                '英雄之旅模板应用',
                '悬疑反转设计技巧',
                '伏笔埋设与回收',
                '剧情节奏控制'
            ],
            '角色塑造师': [
                '角色性格刻画方法',
                '人物动机设定',
                '角色成长弧光设计',
                '人物关系网络构建',
                '反派角色塑造技巧'
            ],
            '战斗设计师': [
                '战斗场景描写技巧',
                '招式命名艺术',
                '战斗节奏控制',
                '不同境界战斗差异',
                '特殊能力对决设计'
            ],
            '场景构造师': [
                '环境氛围营造',
                '感官细节描写',
                '空间布局设计',
                '场景转换技巧',
                '地域特色体现'
            ],
            '对话设计师': [
                '对话个性塑造',
                '潜台词设计',
                '对话节奏控制',
                '情感对话描写',
                '冲突对话设计'
            ],
            '写作技巧大师': [
                '风格定位与统一',
                '修辞手法运用',
                '叙事视角选择',
                '节奏控制技巧',
                '去AI化写作方法'
            ],
            '去AI痕迹监督官': [
                'AI痕迹识别技巧',
                '自然语言优化',
                '人类风格模拟',
                '文本质量评估',
                '写作风格多样性'
            ],
            '质量审计师': [
                '小说质量评估标准',
                '结构完整性检查',
                '人物一致性检查',
                '逻辑合理性验证',
                '读者体验优化'
            ],
            '学习大师': [
                '网络小说趋势分析',
                '经典文学研究',
                '写作技巧创新',
                '跨领域知识融合',
                '学习方法优化'
            ],
            '规则掌控者': [
                '自然规则设定',
                '社会规则构建',
                '特殊规则设计',
                '规则一致性维护',
                '规则冲突解决'
            ],
            '词汇大师': [
                '词汇收集与整理',
                '描写素材积累',
                '语言风格优化',
                '专业术语应用',
                '修辞丰富度提升'
            ],
            '短篇小说爽文大师': [
                '2025 2026 短篇小说爽文类型 爆款',
                '2025 2026 短剧改编热门题材',
                '男频爽文最新趋势 套路创新',
                '女频爽文最新趋势 套路创新',
                '短篇小说爆款开篇技巧',
                '爽文写作技巧 节奏控制',
                '恶毒女配逆袭文写作技巧',
                '重生年代文创作方法',
                '都市脑洞文设定技巧'
            ]
        }
    
    def initialize_learners(self):
        """初始化所有Skill学习器"""
        logger.info("初始化所有Skill学习器")
        
        for skill_name, topics in self.skill_topics.items():
            learner = SkillLearner(skill_name, 'secondary', topics)
            self.skill_learners[skill_name] = learner
        
        logger.info("已初始化 %d 个Skill学习器" % len(self.skill_learners))
    
    def start_all_learners(self):
        """启动所有学习器"""
        self.running = True
        
        for skill_name, learner in self.skill_learners.items():
            learner.start_learning_loop()
            logger.info("启动Skill学习器: %s" % skill_name)
        
        logger.info("所有Skill学习器已启动")
    
    def stop_all_learners(self):
        """停止所有学习器"""
        self.running = False
        logger.info("所有Skill学习器已停止")
    
    def get_all_stats(self):
        """获取所有学习器统计"""
        stats = {}
        for skill_name, learner in self.skill_learners.items():
            stats[skill_name] = learner.get_stats()
        return stats
    
    def print_status(self):
        """打印状态"""
        print("=" * 60)
        print("            Skill自主学习状态")
        print("=" * 60)
        
        for skill_name, stats in self.get_all_stats().items():
            print(f"\n【{skill_name}】")
            print(f"  学习次数: {stats['learning_count']}")
            print(f"  错误次数: {stats['error_count']}")
            print(f"  学习中: {'是' if stats['is_learning'] else '否'}")
            print(f"  当前学习主题: {stats['learning_topics'][stats['_topic_index']] if hasattr(stats, '_topic_index') else '未知'}")
        
        print("\n" + "=" * 60)

    def collaborative_learn(self, skill_names, shared_topic):
        """协作学习：多个Skill共同学习一个主题"""
        if not COLLABORATION_ENABLED:
            logger.warning("协作功能未启用")
            return None

        try:
            collab = get_skill_collaboration()
            logger.info("启动协作学习: %s" % skill_names)

            # 多Skill协作学习
            results = collab.collaborative_learning(skill_names, shared_topic)

            # 通知相关Skill更新
            for skill_name in skill_names:
                if skill_name in self.skill_learners:
                    learner = self.skill_learners[skill_name]
                    # 获取相关Skill的知识
                    related = collab.get_related_knowledge(skill_name, shared_topic)
                    if related:
                        logger.info("%s 获得 %d 条相关知识" % (skill_name, len(related)))

            return results

        except Exception as e:
            logger.log_exception(e, "collaborative_learn")
            return None

    def query_cross_skill_knowledge(self, skill_name):
        """查询跨Skill知识"""
        if not COLLABORATION_ENABLED:
            return {}

        try:
            collab = get_skill_collaboration()
            return collab.get_skill_insights(skill_name)
        except Exception as e:
            logger.log_exception(e, "query_cross_skill_knowledge")
            return {}

# 独立运行测试
if __name__ == "__main__":
    print("=====================================")
    print("    NWACS Skill自主学习管理器")
    print("=====================================")
    
    # 创建管理器
    manager = SkillLearningManager()
    manager.initialize_learners()
    
    # 启动所有学习器
    print("\n启动所有Skill学习器...")
    manager.start_all_learners()
    
    # 显示状态
    print("\n当前状态:")
    manager.print_status()
    
    # 保持运行
    try:
        while True:
            time.sleep(60)
            # 每分钟更新一次状态
            print("\n更新状态:")
            manager.print_status()
    except KeyboardInterrupt:
        manager.stop_all_learners()
        print("\nSkill学习管理器已停止")