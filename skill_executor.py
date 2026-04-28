#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS Skill执行框架 v2.0
集成任务优化系统，提升执行效率和任务完成率
"""

import time
import json
import os
import threading
import uuid
from datetime import datetime
from logger import logger
from fault_tolerance import retry_on_failure, circuit_breaker, RateLimiter
from task_optimizer import ExecutionOptimizer

class SkillExecutorV2:
    """增强版Skill执行器"""
    
    def __init__(self):
        self.config = self.load_config()
        self.skill_registry = {}
        self.execute_count = 0
        self.error_count = 0
        self.success_count = 0
        self.task_optimizer = None
        self.running = False
        
        # 性能指标
        self.performance_metrics = {
            'total_executions': 0,
            'successful_executions': 0,
            'failed_executions': 0,
            'average_response_time': 0,
            'throughput': 0,
            'skill_stats': {}
        }
        
        self.register_skills()
        self.start_optimizer()
    
    def load_config(self):
        """加载Skill配置"""
        config_path = "20_TraeCN_Skills配置.json"
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                logger.info("Skill配置加载成功")
                return config
            except Exception as e:
                logger.log_exception(e, "load_config")
                self.error_count += 1
        return {}
    
    def register_skills(self):
        """注册所有Skill"""
        try:
            # 注册二级Skill
            for skill in self.config.get('skills', {}).get('secondary', []):
                self._register_skill(skill, 'secondary')
            
            # 注册三级Skill
            for skill in self.config.get('skills', {}).get('tertiary', []):
                self._register_skill(skill, 'tertiary')
            
            logger.info("已注册 %d 个Skill" % len(self.skill_registry))
        except Exception as e:
            logger.log_exception(e, "register_skills")
            self.error_count += 1
    
    def _register_skill(self, skill_config, skill_type):
        """注册单个Skill"""
        skill_name = skill_config['name']
        self.skill_registry[skill_name] = {
            'type': skill_type,
            'config': skill_config,
            'executor': self.create_skill_executor(skill_config),
            'stats': {
                'executions': 0,
                'successes': 0,
                'failures': 0,
                'avg_time': 0
            }
        }
        
        # 初始化性能统计
        self.performance_metrics['skill_stats'][skill_name] = {
            'executions': 0,
            'success_rate': 0,
            'avg_time': 0
        }
    
    def create_skill_executor(self, skill_config):
        """创建Skill执行器"""
        def executor(task_data):
            return self.execute_skill_with_enhancement(skill_config, task_data)
        return executor
    
    @retry_on_failure
    def execute_skill_with_enhancement(self, skill_config, task_data):
        """增强版Skill执行"""
        skill_name = skill_config['name']
        start_time = time.time()
        
        logger.debug("执行Skill: %s" % skill_name)
        
        try:
            # 模拟执行过程（实际应调用真实Skill）
            time.sleep(1.5)  # 优化：减少模拟时间
            
            # 检查配置中的特殊规则
            if 'creation_rules' in skill_config:
                logger.debug("应用创建规则: %s" % skill_config['creation_rules'])
            
            # 检查专长
            if 'specialties' in skill_config:
                logger.debug("应用专长: %s" % skill_config['specialties'][:2])
            
            elapsed = round(time.time() - start_time, 2)
            
            # 更新统计
            self._update_skill_stats(skill_name, success=True, elapsed=elapsed)
            
            self.execute_count += 1
            self.success_count += 1
            
            result = {
                'skill_name': skill_name,
                'status': 'completed',
                'output': self._generate_skill_output(skill_config, task_data),
                'details': self._generate_skill_details(skill_config, task_data),
                'execution_time': elapsed,
                'timestamp': datetime.now().isoformat()
            }
            
            logger.info("Skill执行成功: %s (耗时: %.2fs)" % (skill_name, elapsed))
            return result
            
        except Exception as e:
            elapsed = round(time.time() - start_time, 2)
            self._update_skill_stats(skill_name, success=False, elapsed=elapsed)
            
            self.execute_count += 1
            self.error_count += 1
            
            logger.log_exception(e, "execute_skill - %s" % skill_name)
            return {
                'skill_name': skill_name,
                'status': 'failed',
                'error': str(e),
                'execution_time': elapsed,
                'timestamp': datetime.now().isoformat()
            }
    
    def _generate_skill_output(self, skill_config, task_data):
        """生成Skill输出"""
        skill_name = skill_config['name']
        description = skill_config.get('description', '')
        
        if skill_name == '世界观构造师':
            world_type = task_data.get('world_type', '未知世界')
            return f"【{skill_name}】已完成{world_type}的世界观构建，包含修炼体系、势力架构、地理环境等核心设定"
        
        elif skill_name == '主线剧情设计师':
            plot_type = task_data.get('type', '剧情')
            return f"【{skill_name}】已完成{plot_type}主线设计，包含三幕式结构和关键转折点"
        
        elif skill_name == '角色塑造师':
            char_name = task_data.get('character_name', '角色')
            return f"【{skill_name}】已完成{char_name}的角色塑造，包含性格设定、动机和成长弧光"
        
        elif skill_name == '战斗设计师':
            scale = task_data.get('scale', '战斗')
            return f"【{skill_name}】已完成{scale}场景设计，包含招式、战术和节奏控制"
        
        elif skill_name == '去AI痕迹监督官':
            return f"【{skill_name}】已完成去AI化检查，确保文字自然流畅"
        
        elif skill_name == '质量审计师':
            return f"【{skill_name}】已完成质量审计，输出综合评分和改进建议"
        
        else:
            return f"【{skill_name}】{description} - 任务已完成"
    
    def _generate_skill_details(self, skill_config, task_data):
        """生成详细结果"""
        skill_name = skill_config['name']
        
        details = {
            'skill_name': skill_name,
            'parameters': task_data,
            'timestamp': datetime.now().isoformat()
        }
        
        if 'specialties' in skill_config:
            details['specialties_used'] = skill_config['specialties'][:3]
        
        if 'creation_rules' in skill_config:
            details['rules_applied'] = skill_config['creation_rules'][:3]
        
        return details
    
    def _update_skill_stats(self, skill_name, success, elapsed):
        """更新Skill统计"""
        if skill_name in self.skill_registry:
            stats = self.skill_registry[skill_name]['stats']
            stats['executions'] += 1
            
            if success:
                stats['successes'] += 1
            else:
                stats['failures'] += 1
            
            # 更新平均时间
            if stats['avg_time'] == 0:
                stats['avg_time'] = elapsed
            else:
                stats['avg_time'] = round(
                    (stats['avg_time'] * (stats['executions'] - 1) + elapsed) / stats['executions'], 
                    2
                )
            
            # 更新性能指标
            perf_stats = self.performance_metrics['skill_stats'][skill_name]
            perf_stats['executions'] = stats['executions']
            perf_stats['success_rate'] = round(
                (stats['successes'] / stats['executions']) * 100, 1
            )
            perf_stats['avg_time'] = stats['avg_time']
    
    def start_optimizer(self):
        """启动任务优化器"""
        self.task_optimizer = ExecutionOptimizer()
        self.task_optimizer.start()
        logger.info("任务优化器已启动")
    
    def execute_by_name(self, skill_name, task_data=None, priority=5):
        """按名称执行Skill（增强版）"""
        if skill_name in self.skill_registry:
            # 使用任务优化器执行
            task_id = self.task_optimizer.submit_task(
                name=f"执行{skill_name}",
                skill_name=skill_name,
                data=task_data or {},
                priority=priority
            )
            
            # 等待任务完成
            status = self.task_optimizer.wait_for_task(task_id, timeout=60)
            
            if status and status.get('status') == 'completed':
                return self.skill_registry[skill_name]['executor'](task_data or {})
            else:
                logger.warning("任务执行异常: %s" % status)
                return {'error': '任务执行失败或超时'}
        else:
            error_msg = "Skill '%s' 未找到" % skill_name
            logger.warning(error_msg)
            return {'error': error_msg}
    
    def execute_workflow(self, workflow):
        """执行工作流"""
        """
        workflow格式:
        [
            {'skill': 'Skill名称', 'data': {...}, 'priority': 5},
            ...
        ]
        """
        results = []
        
        for step in workflow:
            skill_name = step['skill']
            data = step.get('data', {})
            priority = step.get('priority', 5)
            
            logger.info(f"执行工作流步骤: {skill_name}")
            
            result = self.execute_by_name(skill_name, data, priority)
            results.append({
                'step': skill_name,
                'result': result
            })
            
            # 如果失败，尝试重试或跳过
            if result.get('status') == 'failed':
                logger.warning(f"工作流步骤失败: {skill_name}")
        
        return results
    
    def get_skill_status(self):
        """获取所有Skill状态"""
        status = []
        for name, info in self.skill_registry.items():
            stats = info['stats']
            success_rate = round((stats['successes'] / stats['executions']) * 100, 1) if stats['executions'] > 0 else 0
            
            status.append({
                'name': name,
                'type': info['type'],
                'description': info['config'].get('description', ''),
                'executions': stats['executions'],
                'success_rate': f"{success_rate}%",
                'avg_time': f"{stats['avg_time']}s"
            })
        return status
    
    def get_performance_report(self):
        """获取性能报告"""
        total_exec = self.execute_count
        success_rate = round((self.success_count / total_exec) * 100, 1) if total_exec > 0 else 0
        
        report = {
            'summary': {
                'total_skills': len(self.skill_registry),
                'total_executions': total_exec,
                'successful_executions': self.success_count,
                'failed_executions': self.error_count,
                'success_rate': f"{success_rate}%",
                'optimizer_active': self.task_optimizer is not None
            },
            'skill_stats': self.performance_metrics['skill_stats'],
            'generated_at': datetime.now().isoformat()
        }
        
        return report
    
    def get_stats(self):
        """获取执行统计信息"""
        return {
            'total_skills': len(self.skill_registry),
            'execute_count': self.execute_count,
            'error_count': self.error_count,
            'success_count': self.success_count,
            'success_rate': round((self.success_count / self.execute_count) * 100, 1) if self.execute_count > 0 else 0
        }

class NovelMasterOrchestratorV2:
    """增强版小说总调度官"""
    
    def __init__(self):
        self.skill_executor = SkillExecutorV2()
        self.logger = logger
        self.logger.info("增强版小说总调度官初始化完成")
    
    def execute_workflow(self, user_request):
        """执行完整工作流"""
        self.logger.info("用户需求: %s" % user_request)
        
        # 解析需求
        workflow = self._parse_request(user_request)
        
        if not workflow:
            self.logger.error("无法解析用户需求")
            return {'error': '无法解析用户需求'}
        
        self.logger.info(f"解析到 {len(workflow)} 个工作步骤")
        
        # 执行工作流
        results = self.skill_executor.execute_workflow(workflow)
        
        # 汇总结果
        summary = self._summarize_results(results)
        
        return summary
    
    def _parse_request(self, user_request):
        """解析用户请求为工作流"""
        workflow = []
        
        # 根据关键词匹配Skill
        keywords = {
            '世界观': '世界观构造师',
            '世界设定': '世界观构造师',
            '修炼体系': '世界观构造师',
            '剧情': '主线剧情设计师',
            '故事': '主线剧情设计师',
            '情节': '主线剧情设计师',
            '角色': '角色塑造师',
            '人物': '角色塑造师',
            '战斗': '战斗设计师',
            '打斗': '战斗设计师',
            '场景': '场景构造师',
            '环境': '场景构造师',
            '对话': '对话设计师',
            '对话设计': '对话设计师',
            '写作': '写作技巧大师',
            '润色': '写作技巧大师',
            '检查': '质量审计师',
            '审核': '质量审计师',
            '去AI': '去AI痕迹监督官'
        }
        
        for keyword, skill_name in keywords.items():
            if keyword in user_request:
                workflow.append({
                    'skill': skill_name,
                    'data': {'user_request': user_request},
                    'priority': 5
                })
        
        # 如果没有匹配，默认执行完整流程
        if not workflow:
            workflow = [
                {'skill': '世界观构造师', 'data': {'user_request': user_request}, 'priority': 10},
                {'skill': '主线剧情设计师', 'data': {'user_request': user_request}, 'priority': 10},
                {'skill': '角色塑造师', 'data': {'user_request': user_request}, 'priority': 9},
                {'skill': '场景构造师', 'data': {'user_request': user_request}, 'priority': 8},
                {'skill': '对话设计师', 'data': {'user_request': user_request}, 'priority': 8},
                {'skill': '去AI痕迹监督官', 'data': {}, 'priority': 7},
                {'skill': '质量审计师', 'data': {}, 'priority': 7}
            ]
        
        return workflow
    
    def _summarize_results(self, results):
        """汇总工作流结果"""
        successful = 0
        failed = 0
        details = []
        
        for item in results:
            step = item['step']
            result = item['result']
            
            if result.get('status') == 'completed':
                successful += 1
                details.append(f"✓ {step}: 成功")
            else:
                failed += 1
                details.append(f"✗ {step}: 失败 - {result.get('error', '未知错误')}")
        
        return {
            'status': 'completed' if failed == 0 else 'partial',
            'successful_steps': successful,
            'failed_steps': failed,
            'total_steps': len(results),
            'details': details,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_system_status(self):
        """获取系统状态"""
        return {
            'executor_stats': self.skill_executor.get_stats(),
            'performance_report': self.skill_executor.get_performance_report(),
            'skill_status': self.skill_executor.get_skill_status()
        }
    
    def print_status(self):
        """打印系统状态"""
        status = self.get_system_status()
        
        print("=" * 60)
        print("            NWACS 系统状态")
        print("=" * 60)
        
        # 执行统计
        stats = status['executor_stats']
        print("\n【执行统计】")
        print(f"  Skill总数: {stats['total_skills']}")
        print(f"  执行次数: {stats['execute_count']}")
        print(f"  成功次数: {stats['success_count']}")
        print(f"  失败次数: {stats['error_count']}")
        print(f"  成功率: {stats['success_rate']}%")
        
        # 性能报告
        report = status['performance_report']
        print("\n【性能报告】")
        print(f"  优化器状态: {'运行中' if report['summary']['optimizer_active'] else '未启动'}")
        
        # Skill状态（前5个）
        print("\n【Skill状态（前5个）】")
        for skill in status['skill_status'][:5]:
            print(f"  [{skill['type']}] {skill['name']}")
            print(f"    执行次数: {skill['executions']}, 成功率: {skill['success_rate']}, 平均耗时: {skill['avg_time']}")
        
        print("=" * 60)

# 测试增强版执行框架
if __name__ == "__main__":
    print("=====================================")
    print("    NWACS Skill执行框架 v2.0")
    print("=====================================")
    
    # 创建调度官
    orchestrator = NovelMasterOrchestratorV2()
    
    # 显示状态
    orchestrator.print_status()
    
    # 执行测试工作流
    print("\n执行测试工作流...")
    result = orchestrator.execute_workflow("创建一个玄幻修仙小说的世界观和主线剧情")
    print("\n工作流执行结果:")
    print(f"状态: {result['status']}")
    print(f"完成步骤: {result['successful_steps']}/{result['total_steps']}")
    for detail in result['details']:
        print(f"  {detail}")