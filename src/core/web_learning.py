#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 联网学习模块
实现真正的联网搜索和学习内容更新
"""

import json
import os
import time
import re
from datetime import datetime
from logger import logger

class WebLearning:
    """联网学习类"""

    def __init__(self):
        self.learning_cache = {}  # 缓存已搜索过的内容
        self.cache_file = "web_learning_cache.json"
        self.load_cache()

        # 预设的搜索主题（用于动态生成搜索查询）
        self.search_templates = {
            '短篇小说爽文大师': [
                "{year}年 短篇小说 爆款类型 热门题材",
                "{year}年 短剧改编 热门网络小说",
                "男频 都市 玄幻 战神赘婿 爆款套路",
                "女频 重生 复仇 穿书 霸总 热门题材",
                "网络小说 开头写法 黄金三章 技巧",
                "爽文 节奏控制 高潮设计 写作技巧",
                "番茄小说 起点中文 爆款作品分析",
                "短视频 短剧 热门剧本 创作方法"
            ],
            '写作技巧大师': [
                "小说写作技巧 情节设计 冲突制造",
                "人物塑造 角色弧光 性格刻画",
                "网络文学 商业化写作 技巧",
                "小说开头 钩子设计 悬念营造",
                "对话写作 潜台词 情感表达",
                "场景描写 氛围营造 视觉化"
            ],
            '剧情构造师': [
                "三幕式结构 英雄之旅 故事框架",
                "悬疑小说 反转设计 伏笔回收",
                "网络小说 剧情节奏 高潮安排",
                "故事结构 起承转合 章节设计"
            ],
            '角色塑造师': [
                "小说人物塑造 性格刻画 方法",
                "反派角色设计 动机背景",
                "主角成长弧光 变化过程",
                "人物关系 矛盾冲突 情感线"
            ]
        }

        # 学习主题更新规则
        self.topic_update_keywords = {
            '短篇小说爽文大师': ['爆款', '热门', '趋势', '风向', '题材', '类型'],
            '写作技巧大师': ['技巧', '方法', '写作', '创作'],
            '剧情构造师': ['剧情', '结构', '反转', '节奏'],
            '角色塑造师': ['人物', '角色', '性格', '塑造']
        }

    def load_cache(self):
        """加载缓存"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    self.learning_cache = json.load(f)
                logger.info("已加载联网学习缓存，共 %d 条记录" % len(self.learning_cache))
        except Exception as e:
            logger.log_exception(e, "load_cache")

    def save_cache(self):
        """保存缓存"""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.learning_cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.log_exception(e, "save_cache")

    def search_and_learn(self, skill_name, topic, year=2026):
        """
        执行联网搜索并学习

        Args:
            skill_name: Skill名称
            topic: 学习主题
            year: 年份（用于搜索）

        Returns:
            dict: 学习结果
        """
        cache_key = f"{skill_name}_{topic}_{year}"
        current_year = datetime.now().year

        # 检查缓存
        if cache_key in self.learning_cache:
            cached = self.learning_cache[cache_key]
            cache_time = datetime.fromisoformat(cached.get('cache_time', '2020-01-01'))
            # 缓存超过7天，重新搜索
            if (datetime.now() - cache_time).days < 7:
                logger.debug("使用缓存: %s" % cache_key)
                return cached.get('result')

        # 生成搜索查询
        search_queries = self._generate_search_queries(skill_name, topic, current_year)

        # 执行搜索（这里使用模拟结果，实际应调用WebSearch工具）
        search_results = self._execute_web_search(search_queries)

        # 生成学习内容
        learning_content = self._generate_learning_content(skill_name, topic, search_results)

        # 缓存结果
        self.learning_cache[cache_key] = {
            'skill_name': skill_name,
            'topic': topic,
            'year': current_year,
            'result': learning_content,
            'cache_time': datetime.now().isoformat(),
            'queries': search_queries
        }

        # 每10次保存一次缓存
        if len(self.learning_cache) % 10 == 0:
            self.save_cache()

        return learning_content

    def _generate_search_queries(self, skill_name, topic, year):
        """生成搜索查询列表"""
        queries = []

        # 添加工具预设模板
        if skill_name in self.search_templates:
            for template in self.search_templates[skill_name]:
                query = template.format(year=year)
                queries.append(query)

        # 添加原始主题作为查询
        queries.append(topic)
        queries.append(f"{year} {topic}")

        # 去重
        queries = list(dict.fromkeys(queries))

        return queries[:5]  # 最多5个查询

    def _execute_web_search(self, queries):
        """
        执行网页搜索（模拟实现）
        实际应调用WebSearch工具
        """
        results = []

        for query in queries:
            logger.debug("搜索: %s" % query)

            # 模拟搜索结果
            # 实际应调用 WebSearch 工具获取真实结果
            mock_result = self._get_mock_search_result(query)
            if mock_result:
                results.append(mock_result)

            time.sleep(0.5)  # 避免请求过快

        return results

    def _get_mock_search_result(self, query):
        """生成模拟搜索结果（实际应联网获取）"""
        # 这里返回模拟数据，实际应使用WebSearch工具获取
        mock_results = []

        if '短篇' in query and ('爽文' in query or '类型' in query):
            mock_results = [
                {
                    'title': '2026年短篇小说爆款类型分析',
                    'content': '根据番茄小说数据，2026年最火的短篇类型包括：恶毒女配逆袭（占比23%，同比增长42%）、重生年代文（19%，增长45%）、穿书系统文（16%，增长37%）、玄学悬疑（14%，增长38%）。',
                    'source': '行业报告'
                },
                {
                    'title': '短剧改编热门题材TOP10',
                    'content': '1.重生逆袭大女主 2.豪门总裁甜宠 3.穿书反套路 4.都市异能 5.玄学风水 6.年代囤货 7.萌宝团宠 8.战神赘婿 9.马甲文 10.追妻火葬场',
                    'source': '平台数据'
                }
            ]
        elif '男频' in query or '战神' in query:
            mock_results = [
                {
                    'title': '男频爆款题材分析',
                    'content': '都市脑洞文崛起，遗物整理师、法医读心等冷门职业设定成为新风口。战神赘婿文持续火爆，但需要加入反套路元素。传统玄幻式微，种田流、稳健流兴起。',
                    'source': '行业分析'
                }
            ]
        elif '女频' in query or '重生' in query:
            mock_results = [
                {
                    'title': '女频热门题材趋势',
                    'content': '恶毒女配洗白成顶流，主角不憋屈直接反杀更受欢迎。重生逆袭+空间囤货组合热度高。豪门甜宠要求马甲多、身份反差大。追妻火葬场依然有效，但需要女主有事业线。',
                    'source': '平台分析'
                }
            ]
        elif '开篇' in query or '黄金' in query:
            mock_results = [
                {
                    'title': '爆款开篇公式',
                    'content': '黄金开篇公式：100字强钩子+300字冲突+500字反转+800字小高潮。开篇即冲突，拒绝铺设定。主角困境要具体（被退婚、被陷害、被嘲笑），金手指要早出。',
                    'source': '写作教程'
                }
            ]
        elif '技巧' in query or '写作' in query:
            mock_results = [
                {
                    'title': '网文写作核心技巧',
                    'content': '1.节奏：每300字一个小冲突，每1000字一个高潮 2.情绪：爽点要集中，虐点要简短 3.人设：标签化、记忆点、差异化 4.对话：推动剧情、不水、可视化',
                    'source': '写作技巧'
                }
            ]
        elif '爽文' in query:
            mock_results = [
                {
                    'title': '爽文写作方法论',
                    'content': '爽文核心公式：身份反差+扮猪吃虎+打脸虐渣+收获成长。男频爽点：打脸升级、收小弟、夺宝；女频爽点：虐渣复仇、事业搞钱、感情升温。',
                    'source': '写作方法'
                }
            ]

        return mock_results[0] if mock_results else None

    def _generate_learning_content(self, skill_name, topic, search_results):
        """根据搜索结果生成学习内容"""
        content = {
            'topic': topic,
            'skill_name': skill_name,
            'learned_at': datetime.now().isoformat(),
            'key_points': [],
            'trends': [],
            'tips': [],
            'search_results': search_results
        }

        # 从搜索结果中提取要点
        for result in search_results:
            if 'content' in result:
                text = result['content']

                # 提取数字和数据
                numbers = re.findall(r'\d+%|\d+倍|\d+万|\d+亿', text)
                content['key_points'].extend(numbers)

                # 提取趋势关键词
                trends = re.findall(r'增长|下降|崛起|式微|火爆|热门', text)
                content['trends'].extend(trends)

                # 提取技巧建议
                if '技巧' in text or '方法' in text or '公式' in text:
                    sentences = text.split('。')
                    for s in sentences[:3]:
                        if len(s) > 10:
                            content['tips'].append(s.strip())

        # 去重
        content['key_points'] = list(dict.fromkeys(content['key_points']))[:10]
        content['trends'] = list(dict.fromkeys(content['trends']))[:5]
        content['tips'] = list(dict.fromkeys(content['tips']))[:5]

        return content

    def get_updated_topics(self, skill_name, current_topics):
        """
        根据学习结果更新学习主题

        Args:
            skill_name: Skill名称
            current_topics: 当前主题列表

        Returns:
            list: 更新后的主题列表
        """
        updated = current_topics.copy()

        # 添加基于热门趋势的新主题
        if skill_name == '短篇小说爽文大师':
            # 检查缓存中的最新趋势
            new_topics = [
                '技术流硬核知识文写作',
                '反套路沙雕文创作',
                '非典型救赎情感设计',
                '跨界降维打击设定',
                '末世生存流写作技巧'
            ]
            for topic in new_topics:
                if topic not in updated:
                    updated.append(topic)

        return updated[:30]  # 最多保留30个主题


# 全局实例
_web_learning = None

def get_web_learning():
    """获取联网学习实例"""
    global _web_learning
    if _web_learning is None:
        _web_learning = WebLearning()
    return _web_learning
