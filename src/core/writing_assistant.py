#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 创作辅助工具集成模块
集成 novel-mcp-server-v2 中的所有工具
功能：AI检测、节奏检测、连贯性检查、对话优化、读者模拟等
"""

import os
import sys
import json
import subprocess
import tempfile
from typing import Dict, List, Any, Optional
from logger import logger

class WritingAssistant:
    """创作辅助工具管理器"""

    def __init__(self):
        self.tools_dir = os.path.abspath(
            os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                'novel-mcp-server-v2',
                'dist',
                'tools'
            )
        )
        self.node_path = self._find_node()
        self.available = self.node_path is not None

        if not self.available:
            logger.warning("Node.js 未找到，部分创作辅助工具不可用")

        logger.info("创作辅助工具初始化完成，工具目录：%s" % self.tools_dir)

    def _find_node(self):
        """查找 Node.js 可执行文件"""
        try:
            result = subprocess.run(
                ['node', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                logger.info("Node.js 版本：%s" % result.stdout.strip())
                return 'node'
        except Exception:
            pass

        # 尝试常见路径
        common_paths = [
            'C:\\Program Files\\nodejs\\node.exe',
            'C:\\Program Files (x86)\\nodejs\\node.exe',
            os.path.expanduser('~\\AppData\\Roaming\\npm\\node.exe')
        ]

        for path in common_paths:
            if os.path.exists(path):
                return path

        return None

    def _execute_node_tool(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """执行 Node.js 工具"""
        if not self.available:
            return {'success': False, 'error': 'Node.js 不可用'}

        tool_path = os.path.join(self.tools_dir, '%s.js' % tool_name)

        if not os.path.exists(tool_path):
            return {'success': False, 'error': '工具文件不存在：%s' % tool_name}

        try:
            # 创建临时输入文件
            with tempfile.NamedTemporaryFile(
                mode='w',
                suffix='.json',
                delete=False,
                encoding='utf-8'
            ) as f:
                json.dump(params, f, ensure_ascii=False)
                input_file = f.name

            try:
                # 执行 Node.js 工具
                cmd = [self.node_path, tool_path, input_file]

                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=30,
                    cwd=os.path.dirname(tool_path)
                )

                if result.returncode == 0 and result.stdout:
                    try:
                        return json.loads(result.stdout)
                    except json.JSONDecodeError:
                        return {'success': False, 'error': '无法解析工具输出'}
                else:
                    error_msg = result.stderr or '未知错误'
                    logger.warning("工具执行失败：%s" % error_msg)
                    return {'success': False, 'error': error_msg}

            finally:
                # 清理临时文件
                if os.path.exists(input_file):
                    os.remove(input_file)

        except subprocess.TimeoutExpired:
            logger.warning("工具执行超时：%s" % tool_name)
            return {'success': False, 'error': '执行超时'}
        except Exception as e:
            logger.log_exception(e, "执行工具 %s" % tool_name)
            return {'success': False, 'error': str(e)}

    def detect_ai(self, text: str, detection_mode: str = 'standard') -> Dict[str, Any]:
        """
        AI 痕迹检测
        参数:
            text: 待检测文本
            detection_mode: 检测模式 ('standard' 或 'deep')
        返回:
            ai_probability: AI 概率 (0-100)
            flagged_sections: 标记的可疑段落
            suggestions: 优化建议
        """
        params = {
            'text': text,
            'detection_mode': detection_mode
        }

        result = self._execute_node_tool('ai_detector', params)

        if result.get('success'):
            logger.info("AI 痕迹检测完成，概率：%s%%" % result.get('ai_probability', 0))
        else:
            # 如果 Node.js 工具不可用，使用内置实现
            logger.warning("使用内置 AI 检测实现")
            result = self._builtin_ai_detector(text, detection_mode)

        return result

    def _builtin_ai_detector(self, text: str, detection_mode: str = 'standard') -> Dict[str, Any]:
        """内置 AI 痕迹检测（当 Node.js 不可用时使用）"""
        flagged_sections = []
        ai_probability = 0

        ai_patterns = [
            '经过慎重考虑', '综上所述', '需要注意的是',
            '首先', '其次', '最后', '在这种情况下',
            '从某种意义上说', '值得注意的是', '不言而喻'
        ]

        for pattern in ai_patterns:
            if pattern in text:
                ai_probability += 10
                flagged_sections.append('检测到模板化表达: "%s"' % pattern)

        sentences = [s for s in text.replace('?', '?').replace('！', '！').replace('。', '。').split() if s]
        if sentences:
            avg_length = sum(len(s) for s in sentences) / len(sentences)
            if avg_length > 50:
                ai_probability += 10
                flagged_sections.append('句子过长，可能为AI生成')

        unique_chars = len(set(text))
        if unique_chars / max(len(text), 1) < 0.15:
            ai_probability += 15
            flagged_sections.append('词汇多样性较低')

        ai_probability = min(95, max(5, ai_probability))

        if detection_mode == 'deep':
            ai_probability = int(ai_probability * 0.9)

        suggestions = []
        if ai_probability > 60:
            suggestions.append('建议增加个人风格表达')
            suggestions.append('使用更口语化的表达')
            suggestions.append('增加细节描写和情感表达')
        elif ai_probability > 30:
            suggestions.append('整体质量良好，可适当增加个性化表达')
        else:
            suggestions.append('AI痕迹较低，保持创作风格')

        return {
            'success': True,
            'ai_probability': ai_probability,
            'flagged_sections': flagged_sections[:5],
            'suggestions': suggestions
        }

    def analyze_pacing(
        self,
        text: str,
        chapter_position: str = 'rising',
        target_pacing: str = 'moderate'
    ) -> Dict[str, Any]:
        """
        节奏分析
        参数:
            text: 待分析文本
            chapter_position: 章节位置 ('opening', 'rising', 'climax', 'falling', 'ending')
            target_pacing: 目标节奏 ('fast', 'moderate', 'slow')
        返回:
            score: 节奏评分 (0-100)
            issues: 发现的问题
            suggestions: 优化建议
        """
        params = {
            'text': text,
            'chapter_position': chapter_position,
            'target_pacing': target_pacing
        }

        result = self._execute_node_tool('pacing_meter', params)

        if result.get('success'):
            logger.info("节奏分析完成，得分：%s" % result.get('score', 0))
        else:
            logger.warning("使用内置节奏分析实现")
            result = self._builtin_pacing_analyzer(text, chapter_position, target_pacing)

        return result

    def _builtin_pacing_analyzer(
        self,
        text: str,
        chapter_position: str,
        target_pacing: str
    ) -> Dict[str, Any]:
        """内置节奏分析"""
        sentences = [s for s in text.split('。') if s.strip()]
        avg_sentence_length = sum(len(s) for s in sentences) / max(len(sentences), 1)

        dialogue_matches = text.count('"') // 2
        dialogue_ratio = dialogue_matches * 20 / max(len(text), 1)

        action_words = sum(1 for c in text if c in '打杀跑跳飞冲砍刺')
        description_words = text.count('的')

        score = 50

        if target_pacing == 'fast':
            if avg_sentence_length < 30 and action_words > description_words:
                score = 85
            elif avg_sentence_length < 40:
                score = 65
            else:
                score = 40
        elif target_pacing == 'moderate':
            if 30 <= avg_sentence_length <= 50:
                score = 80
            else:
                score = 60
        else:
            if avg_sentence_length > 50 and description_words > action_words:
                score = 80
            else:
                score = 55

        issues = []
        if dialogue_ratio > 0.5:
            issues.append('对话占比过高，可能影响节奏')
        if action_words == 0 and chapter_position == 'climax':
            issues.append('高潮章节动作描写不足')

        suggestions = []
        if score < 60:
            suggestions.append('建议调整句子长度')
            suggestions.append('根据章节位置调整节奏')
        elif score < 80:
            suggestions.append('节奏基本符合预期，可适当优化')
        else:
            suggestions.append('节奏把控良好')

        return {
            'success': True,
            'score': score,
            'issues': issues,
            'suggestions': suggestions
        }

    def check_continuity(
        self,
        novel_id: str,
        check_scope: str = 'chapter',
        strictness: str = 'normal'
    ) -> Dict[str, Any]:
        """
        连贯性检查
        参数:
            novel_id: 小说标识符
            check_scope: 检查范围 ('chapter', 'arc', 'full')
            strictness: 严格程度 ('loose', 'normal', 'strict')
        返回:
            issues: 发现的问题
            severity: 严重程度
            suggestions: 修复建议
        """
        params = {
            'novel_id': novel_id,
            'check_scope': check_scope,
            'strictness': strictness
        }

        result = self._execute_node_tool('continuity_guard', params)

        if result.get('success'):
            logger.info("连贯性检查完成，发现 %d 个问题" % len(result.get('issues', [])))
        else:
            result = {
                'success': False,
                'error': '连贯性检查需要完整的项目上下文，请使用 Node.js 服务'
            }

        return result

    def tune_dialogue(
        self,
        dialogue: str,
        characters: List[str] = None,
        scene_context: str = '',
        tune_mode: str = 'natural'
    ) -> Dict[str, Any]:
        """
        对话优化
        参数:
            dialogue: 待优化对话
            characters: 涉及的角色列表
            scene_context: 场景上下文
            tune_mode: 优化模式 ('natural', 'characteristic', 'dramatic')
        返回:
            naturalness_score: 自然度评分
            character_consistency: 角色一致性
            suggestions: 优化建议
        """
        params = {
            'dialogue': dialogue,
            'characters': characters or [],
            'scene_context': scene_context,
            'tune_mode': tune_mode
        }

        result = self._execute_node_tool('dialogue_tuner', params)

        if result.get('success'):
            logger.info("对话优化完成，自然度：%s" % result.get('naturalness_score', 0))
        else:
            result = {
                'success': False,
                'error': '对话优化需要 Node.js 服务支持'
            }

        return result

    def simulate_reader(
        self,
        text: str,
        reader_group: str = 'young_male',
        simulation_depth: str = 'surface'
    ) -> Dict[str, Any]:
        """
        读者反馈模拟
        参数:
            text: 待模拟文本
            reader_group: 目标读者群体
            simulation_depth: 模拟深度 ('surface', 'deep')
        返回:
            engagement_score: 吸引力评分
            predicted_drop_points: 预测弃书点
            suggestions: 改进建议
        """
        params = {
            'text': text,
            'reader_group': reader_group,
            'simulation_depth': simulation_depth
        }

        result = self._execute_node_tool('reader_simulator', params)

        if result.get('success'):
            logger.info(
                "读者模拟完成，吸引力：%s，弃书点：%d 处" % (
                    result.get('engagement_score', 0),
                    len(result.get('predicted_drop_points', []))
                )
            )
        else:
            result = {
                'success': False,
                'error': '读者模拟需要 Node.js 服务支持'
            }

        return result

    def filter_sensitivity(
        self,
        text: str,
        check_level: str = 'normal',
        content_type: str = 'all'
    ) -> Dict[str, Any]:
        """
        敏感词过滤
        参数:
            text: 待检查文本
            check_level: 检查级别 ('strict', 'normal', 'loose')
            content_type: 内容类型 ('violence', 'sexual', 'political', 'superstitious', 'all')
        返回:
            sensitive_content: 敏感内容列表
            risk_level: 风险等级
            suggestions: 处理建议
        """
        params = {
            'text': text,
            'check_level': check_level,
            'content_type': content_type
        }

        result = self._execute_node_tool('sensitivity_filter', params)

        if result.get('success'):
            logger.info(
                "敏感词检查完成，风险：%s，发现 %d 处敏感内容" % (
                    result.get('risk_level', 'low'),
                    len(result.get('sensitive_content', []))
                )
            )
        else:
            logger.warning("使用内置敏感词过滤实现")
            result = self._builtin_sensitivity_filter(text, check_level, content_type)

        return result

    def _builtin_sensitivity_filter(
        self,
        text: str,
        check_level: str,
        content_type: str
    ) -> Dict[str, Any]:
        """内置敏感词过滤 - 支持仅政治敏感词过滤"""
        
        # 政治敏感词列表
        political_keywords = [
            '中南海', '人民大会堂', '天安门', '钓鱼岛', '台湾',
            '藏独', '台独', '港独', '新疆', '西藏',
            '法轮功', '邪教'
        ]

        sensitive_content = []
        
        for keyword in political_keywords:
            if keyword in text:
                sensitive_content.append({
                    'word': keyword,
                    'category': 'political',
                    'position': text.index(keyword)
                })

        risk_level = 'low'
        if len(sensitive_content) > 3:
            risk_level = 'high'
        elif len(sensitive_content) > 0:
            risk_level = 'medium'

        return {
            'success': True,
            'sensitive_content': sensitive_content,
            'risk_level': risk_level,
            'suggestions': [
                '建议修改或替换敏感内容',
                '避免直接提及敏感人物或事件',
                '使用隐喻或间接表达方式'
            ]
        }

    def extract_style_fingerprint(self, text: str) -> Dict[str, Any]:
        """
        风格指纹提取
        参数:
            text: 待分析文本
        返回:
            features: 风格特征
            style_type: 风格类型
            suggestions: 风格建议
        """
        params = {
            'text': text,
            'action': 'extract'
        }

        result = self._execute_node_tool('style_fingerprint', params)

        if result.get('success'):
            logger.info("风格指纹提取完成，类型：%s" % result.get('style_type', '未知'))
        else:
            result = {
                'success': False,
                'error': '风格指纹提取需要 Node.js 服务支持'
            }

        return result

    def visualize_scene(
        self,
        text: str,
        genre: str = 'urban',
        enhancement_level: str = 'standard'
    ) -> Dict[str, Any]:
        """
        场景可视化增强
        参数:
            text: 待增强文本
            genre: 题材类型
            enhancement_level: 增强级别 ('light', 'standard', 'deep')
        返回:
            enhanced_text: 增强后的文本
            shot_list: 分镜列表
            suggestions: 增强建议
        """
        params = {
            'text': text,
            'genre': genre,
            'enhancement_level': enhancement_level
        }

        result = self._execute_node_tool('scene_visualizer', params)

        if result.get('success'):
            logger.info("场景可视化增强完成")
        else:
            result = {
                'success': False,
                'error': '场景可视化需要 Node.js 服务支持'
            }

        return result

    def comprehensive_analysis(self, text: str) -> Dict[str, Any]:
        """
        综合分析（一次性执行多个检测）
        """
        results = {
            'ai_detection': self.detect_ai(text),
            'pacing_analysis': self.analyze_pacing(text),
            'word_count': len(text),
            'char_count': len(text.replace(' ', '')),
            'sentence_count': len([s for s in text.split('。') if s.strip()])
        }

        logger.info("综合分析完成")
        return results


# 全局实例
writing_assistant = WritingAssistant()


def get_writing_assistant():
    """获取创作辅助工具实例"""
    return writing_assistant
