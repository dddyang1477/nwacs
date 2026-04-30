#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS Skill 协作模块（优化版）
支持 Skill 间知识共享与大模型协作分析
优化功能：余额检测、限流重试、本地缓存、多模型支持
"""

import json
import os
import time
from datetime import datetime
from logger import logger

# 导入大模型优化器
try:
    from llm_optimizer import get_llm_optimizer
    OPTIMIZER_ENABLED = True
except ImportError:
    OPTIMIZER_ENABLED = False
    logger.warning("大模型优化器未启用")

class SkillCollaboration:
    """Skill 协作管理器（优化版）"""

    def __init__(self):
        self.knowledge_base = {}
        self.collaboration_cache = {}
        self.llm_enabled = False
        self.llm_client = None
        self.optimizer = None

        self._init_knowledge_base()
        self._init_llm_client()

    def _init_knowledge_base(self):
        """初始化知识库"""
        kb_file = "skill_knowledge_base.json"
        if os.path.exists(kb_file):
            try:
                with open(kb_file, 'r', encoding='utf-8') as f:
                    self.knowledge_base = json.load(f)
                logger.info("知识库已加载，包含 %d 个知识点" % len(self.knowledge_base))
            except Exception as e:
                logger.log_exception(e, "加载知识库")
                self.knowledge_base = {}

    def _init_llm_client(self):
        """初始化大模型客户端（优化版）"""
        try:
            import openai
            
            # 初始化优化器
            if OPTIMIZER_ENABLED:
                self.optimizer = get_llm_optimizer()
                logger.info("大模型优化器已初始化")
            
            # 从配置文件读取 API 密钥
            config = self._load_config()
            api_key = config.get('api_key') or os.environ.get('OPENAI_API_KEY') or os.environ.get('DEEPSEEK_API_KEY')
            base_url = config.get('base_url') or os.environ.get('OPENAI_BASE_URL')
            self.model = config.get('model', 'deepseek-chat')
            
            if api_key and config.get('enabled', True):
                if base_url:
                    self.llm_client = openai.OpenAI(api_key=api_key, base_url=base_url)
                else:
                    self.llm_client = openai.OpenAI(api_key=api_key)
                
                # 检查余额
                if self.optimizer:
                    balance = self.optimizer.check_balance(self.llm_client)
                    if balance and balance.get('available'):
                        self.llm_enabled = True
                        logger.info("大模型客户端已初始化，模型：%s，余额：%.2f" % (self.model, balance.get('amount', 0)))
                    else:
                        logger.warning("大模型余额不足，功能受限")
                        self.llm_enabled = False
                else:
                    self.llm_enabled = True
                    logger.info("大模型客户端已初始化，模型：%s" % self.model)
            else:
                logger.info("未配置 API 密钥或未启用，大模型功能未启用")
        except ImportError:
            logger.info("openai 库未安装，大模型功能未启用")
        except Exception as e:
            logger.log_exception(e, "初始化大模型客户端")
    
    def _load_config(self):
        """从配置文件加载设置"""
        config_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config.json')
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def share_learning_to_knowledge_base(self, skill_name, topic, learning_result):
        """将学习内容分享到知识库"""
        try:
            key = "%s_%s" % (skill_name, topic)

            if key not in self.knowledge_base:
                self.knowledge_base[key] = {
                    'skill_name': skill_name,
                    'topic': topic,
                    'learned_at': datetime.now().isoformat(),
                    'content': [],
                    '引用次数': 0
                }

            if isinstance(learning_result, dict):
                content_item = {
                    'learned_at': datetime.now().isoformat(),
                    'key_points': learning_result.get('key_points', []),
                    'trends': learning_result.get('trends', []),
                    'tips': learning_result.get('tips', []),
                    'search_results': [r.get('title', '') for r in learning_result.get('search_results', [])]
                }
            else:
                content_item = {
                    'learned_at': datetime.now().isoformat(),
                    'content': str(learning_result)
                }

            self.knowledge_base[key]['content'].append(content_item)
            self.knowledge_base[key]['last_updated'] = datetime.now().isoformat()

            self._save_knowledge_base()
            logger.debug("%s 学习成果已分享到知识库" % skill_name)
            return True

        except Exception as e:
            logger.log_exception(e, "share_learning_to_knowledge_base")
            return False

    def _save_knowledge_base(self):
        """保存知识库"""
        try:
            with open("skill_knowledge_base.json", 'w', encoding='utf-8') as f:
                json.dump(self.knowledge_base, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.log_exception(e, "_save_knowledge_base")

    def query_knowledge_base(self, skill_name=None, topic_keyword=None, limit=10):
        """查询知识库"""
        results = []

        for key, data in self.knowledge_base.items():
            if skill_name and data.get('skill_name') != skill_name:
                continue

            if topic_keyword and topic_keyword not in key:
                continue

            results.append(data)

        return results[:limit]

    def get_related_knowledge(self, skill_name, topic):
        """获取相关Skill的知识"""
        related = {}

        # 定义Skill关联关系
        skill_relations = {
            '短篇小说爽文大师': ['写作技巧大师', '剧情构造师', '角色塑造师'],
            '写作技巧大师': ['剧情构造师', '角色塑造师', '去AI痕迹监督官'],
            '剧情构造师': ['写作技巧大师', '战斗设计师', '场景构造师'],
            '角色塑造师': ['对话设计师', '写作技巧大师', '世界观构造师'],
            '战斗设计师': ['剧情构造师', '场景构造师', '规则掌控者'],
            '场景构造师': ['世界观构造师', '战斗设计师', '规则掌控者'],
            '对话设计师': ['角色塑造师', '写作技巧大师'],
            '世界观构造师': ['场景构造师', '规则掌控者', '词汇大师'],
            '规则掌控者': ['世界观构造师', '战斗设计师'],
            '去AI痕迹监督官': ['写作技巧大师', '质量审计师'],
            '质量审计师': ['写作技巧大师', '去AI痕迹监督官'],
            '学习大师': ['所有Skill'],
            '词汇大师': ['写作技巧大师', '世界观构造师'],
        }

        related_skills = skill_relations.get(skill_name, [])

        for related_skill in related_skills:
            if related_skill == '所有Skill':
                # 获取所有相关知识
                for k, v in self.knowledge_base.items():
                    if k.startswith(skill_name):
                        continue
                    related[k] = v
            else:
                for k, v in self.knowledge_base.items():
                    if v.get('skill_name') == related_skill:
                        related[k] = v

        return related

    def analyze_with_llm(self, content, analysis_type="summary"):
        """使用大模型分析内容（优化版：带缓存、限流、重试）"""
        if not self.llm_enabled:
            logger.debug("大模型未启用，跳过分析")
            return None

        try:
            prompt = self._build_analysis_prompt(content, analysis_type)
            temperature = 0.7
            
            # 1. 尝试从缓存获取
            if self.optimizer:
                cached_result = self.optimizer.get_from_cache(prompt, self.model, temperature)
                if cached_result:
                    logger.info("命中缓存，直接返回")
                    return {
                        'analysis': cached_result,
                        'model': self.model,
                        'timestamp': datetime.now().isoformat(),
                        'from_cache': True
                    }
            
            # 2. 选择最佳模型
            task_model = self.model
            if self.optimizer:
                task_model = self.optimizer.select_best_model(analysis_type)
                logger.debug("为任务 '%s' 选择模型：%s" % (analysis_type, task_model))
            
            # 3. 带重试的执行
            def make_request():
                return self.llm_client.chat.completions.create(
                    model=task_model,
                    messages=[
                        {"role": "system", "content": "你是一个专业的小说创作分析师，擅长提取关键信息、总结趋势、提供写作建议。"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=temperature,
                    max_tokens=1000
                )
            
            if self.optimizer:
                response = self.optimizer.execute_with_retry(make_request)
            else:
                response = make_request()

            result = response.choices[0].message.content
            logger.info("大模型分析完成，模型：%s" % task_model)
            
            # 4. 保存到缓存
            if self.optimizer:
                self.optimizer.save_to_cache(prompt, task_model, temperature, result)
            
            # 5. 估算成本
            if self.optimizer:
                cost = self.optimizer.estimate_cost(len(result), task_model)
                logger.debug("本次请求估算成本：$%.4f" % cost)

            return {
                'analysis': result,
                'model': task_model,
                'timestamp': datetime.now().isoformat(),
                'from_cache': False
            }

        except Exception as e:
            logger.log_exception(e, "analyze_with_llm")
            return None

    def _build_analysis_prompt(self, content, analysis_type):
        """构建分析提示词"""
        if analysis_type == "summary":
            return """请分析以下小说创作学习内容，提取：
1. 核心要点（3-5条）
2. 写作技巧建议（2-3条）
3. 相关题材趋势（1-2条）

内容：
%s

请用简洁的列表格式输出。""" % str(content)

        elif analysis_type == "skill_update":
            return """作为小说创作Skill优化助手，请根据以下学习内容，更新优化写作技巧建议。

要求：
1. 提取可操作的具体技巧
2. 给出实际写作示例
3. 标注适用题材

内容：
%s

请用Markdown格式输出。""" % str(content)

        elif analysis_type == "trend_analysis":
            return """分析以下内容中的网络小说趋势：

1. 当前热门题材
2. 读者偏好变化
3. 写作趋势预测

内容：
%s

请用结构化格式输出。""" % str(content)

        return str(content)

    def collaborative_learning(self, skill_names, shared_topic):
        """多Skill协作学习"""
        logger.info("启动协作学习: %s -> %s" % (skill_names, shared_topic))

        results = {}

        # 各Skill分别学习
        for skill_name in skill_names:
            results[skill_name] = {
                'status': 'pending',
                'learning_content': None
            }

        # 汇总分析
        all_content = "\n".join([
            "[%s]: %s" % (name, str(data.get('learning_content', '')))
            for name, data in results.items()
        ])

        # 大模型综合分析
        if self.llm_enabled:
            synthesis = self.analyze_with_llm(all_content, "summary")
            if synthesis:
                results['synthesis'] = synthesis

        return results

    def notify_skill_update(self, source_skill, target_skills, update_content):
        """通知相关Skill进行更新"""
        notification = {
            'source': source_skill,
            'targets': target_skills,
            'content': update_content,
            'timestamp': datetime.now().isoformat()
        }

        # 保存通知
        notification_file = "skill_notifications.json"
        notifications = []

        if os.path.exists(notification_file):
            try:
                with open(notification_file, 'r', encoding='utf-8') as f:
                    notifications = json.load(f)
            except:
                notifications = []

        notifications.append(notification)

        with open(notification_file, 'w', encoding='utf-8') as f:
            json.dump(notifications, f, ensure_ascii=False, indent=2)

        logger.info("%s 已通知 %s 更新" % (source_skill, target_skills))
        return True

    def get_skill_insights(self, skill_name):
        """获取特定Skill的所有洞察"""
        insights = {
            'own': [],
            'related': []
        }

        # 获取自己的知识
        for key, data in self.knowledge_base.items():
            if data.get('skill_name') == skill_name:
                insights['own'].append(data)

        # 获取相关Skill的知识
        related_data = self.get_related_knowledge(skill_name, "")
        insights['related'] = list(related_data.values())

        return insights


# 全局单例
_collab_instance = None

def get_skill_collaboration():
    """获取协作管理器单例"""
    global _collab_instance
    if _collab_instance is None:
        _collab_instance = SkillCollaboration()
    return _collab_instance