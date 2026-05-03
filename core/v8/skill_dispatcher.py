#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS V8.0 智能Skill调度系统
主Skill智能调度次级Skill，确保写作时有序协作
"""

import sys
import json
import os
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "sk-f3246fbd1eef446e9a11d78efefd9bba"
BASE_URL = "https://api.deepseek.com"

def call_deepseek(prompt, system_prompt=None, temperature=0.7):
    """调用DeepSeek API"""
    import requests
    try:
        url = f"{BASE_URL}/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        data = {
            "model": "deepseek-chat",
            "messages": messages,
            "temperature": temperature,
            "max_tokens": 8000
        }
        response = requests.post(url, headers=headers, json=data, timeout=300)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"   ❌ DeepSeek调用失败: {e}")
        return None


class SkillRegistry:
    """Skill注册表 - 定义所有Skill及其功能"""

    def __init__(self):
        self.skills = {
            # ========== 一级Skill（总调度官）==========
            "小说创作总调度": {
                "level": 1,
                "description": "小说创作的总指挥，负责接收任务并调度次级Skill",
                "capabilities": [
                    "任务解析",
                    "Skill匹配",
                    "流程编排",
                    "质量把控"
                ],
                "sub_skills": [
                    "世界观构造师",
                    "角色塑造师",
                    "剧情构造师",
                    "场景构造师",
                    "对话设计师",
                    "高潮设计师",
                    "节奏控制师",
                    "伏笔埋设师",
                    "质量审查师"
                ],
                "trigger_conditions": {
                    "用户输入创作指令": ["任务解析", "Skill匹配", "流程编排"],
                    "需要世界观设定": ["世界观构造师"],
                    "需要角色设计": ["角色塑造师"],
                    "需要剧情设计": ["剧情构造师"],
                    "需要场景描写": ["场景构造师"],
                    "需要对话生成": ["对话设计师"],
                    "需要高潮设计": ["高潮设计师"],
                    "需要节奏控制": ["节奏控制师"],
                    "需要埋设伏笔": ["伏笔埋设师"],
                    "需要质量审查": ["质量审查师"]
                }
            },

            # ========== 二级Skill（专业领域）==========
            "世界观构造师": {
                "level": 2,
                "description": "负责构建小说的世界观、境界体系、势力分布",
                "capabilities": [
                    "境界体系设计",
                    "势力分布规划",
                    "地理环境构建",
                    "历史背景设定",
                    "修炼规则制定"
                ],
                "trigger_keywords": [
                    "世界观", "境界", "势力", "宗门", "大陆",
                    "位面", "法则", "规则", "背景设定"
                ],
                "output": "世界观设定文档"
            },

            "角色塑造师": {
                "level": 2,
                "description": "负责设计小说人物的外貌、性格、背景、能力",
                "capabilities": [
                    "主角设计",
                    "女主设计",
                    "配角设计",
                    "反派设计",
                    "人物关系图谱",
                    "性格一致性维护"
                ],
                "trigger_keywords": [
                    "角色", "人物", "主角", "女主", "配角",
                    "反派", "外貌", "性格", "能力", "设定"
                ],
                "output": "人物设定文档"
            },

            "剧情构造师": {
                "level": 2,
                "description": "负责设计小说的整体剧情走向和章节规划",
                "capabilities": [
                    "三幕结构设计",
                    "章节规划",
                    "爽点设计",
                    "高潮布局",
                    "支线剧情设计"
                ],
                "trigger_keywords": [
                    "剧情", "大纲", "章节", "故事", "主线",
                    "支线", "高潮", "爽点", "发展", "结局"
                ],
                "output": "剧情大纲文档"
            },

            # ========== 三级Skill（具体执行）==========
            "场景构造师": {
                "level": 3,
                "description": "负责描写小说中的场景、环境、氛围",
                "capabilities": [
                    "自然环境描写",
                    "建筑场景描写",
                    "战斗场景描写",
                    "室内场景描写",
                    "氛围营造"
                ],
                "trigger_keywords": [
                    "场景", "环境", "描写", "氛围", "建筑",
                    "战斗", "天空", "大地", "室内", "室外"
                ],
                "required_by": ["剧情构造师", "小说创作总调度"],
                "output": "场景描写文本"
            },

            "对话设计师": {
                "level": 3,
                "description": "负责设计小说中人物的对白",
                "capabilities": [
                    "角色对白生成",
                    "潜台词设计",
                    "冲突对话",
                    "情感对话",
                    "幽默对话"
                ],
                "trigger_keywords": [
                    "对话", "对白", "说话", "台词", "交流",
                    "争论", "争吵", "告白", "聊天"
                ],
                "required_by": ["剧情构造师", "小说创作总调度"],
                "output": "对话文本"
            },

            "高潮设计师": {
                "level": 3,
                "description": "负责设计小说中的高潮场面",
                "capabilities": [
                    "战斗高潮设计",
                    "情感高潮设计",
                    "反转设计",
                    "爽点爆发",
                    "悬念高潮"
                ],
                "trigger_keywords": [
                    "高潮", "爆发", "反转", "震惊", "激动",
                    "燃", "爆", "炸裂", "震撼", "激烈"
                ],
                "required_by": ["剧情构造师"],
                "output": "高潮场面描写"
            },

            "节奏控制师": {
                "level": 3,
                "description": "负责控制小说的整体节奏",
                "capabilities": [
                    "张弛节奏控制",
                    "章节节奏",
                    "整体节奏把控",
                    "悬念节奏",
                    "爽点节奏"
                ],
                "trigger_keywords": [
                    "节奏", "快慢", "紧张", "舒缓", "铺垫",
                    "爆发", "控制", "安排", "分配"
                ],
                "required_by": ["剧情构造师"],
                "output": "节奏调整建议"
            },

            "伏笔埋设师": {
                "level": 3,
                "description": "负责在前文埋设伏笔，为后续剧情做铺垫",
                "capabilities": [
                    "关键伏笔埋设",
                    "伏笔回收设计",
                    "伏笔呼应",
                    "悬念设置",
                    "线索埋设"
                ],
                "trigger_keywords": [
                    "伏笔", "铺垫", "暗示", "线索", "伏脉",
                    "悬念", "预示", "前兆"
                ],
                "required_by": ["剧情构造师"],
                "output": "伏笔埋设计划"
            },

            "质量审查师": {
                "level": 3,
                "description": "负责审查小说的整体质量",
                "capabilities": [
                    "逻辑审查",
                    "一致性检查",
                    "语法检查",
                    "节奏评估",
                    "改进建议"
                ],
                "trigger_keywords": [
                    "审查", "检查", "质量", "审核", "评估",
                    "修改", "改进", "优化", "问题"
                ],
                "required_by": ["小说创作总调度"],
                "output": "质量审查报告"
            }
        }

    def get_skill(self, skill_name):
        """获取Skill信息"""
        return self.skills.get(skill_name)

    def get_sub_skills(self, skill_name):
        """获取次级Skill列表"""
        skill = self.get_skill(skill_name)
        if skill:
            return skill.get("sub_skills", [])
        return []

    def match_skills(self, user_input):
        """根据用户输入匹配需要调用的Skill"""
        matched_skills = []
        user_input_lower = user_input.lower()

        for skill_name, skill_info in self.skills.items():
            if skill_info["level"] == 1:
                continue

            keywords = skill_info.get("trigger_keywords", [])
            for keyword in keywords:
                if keyword in user_input_lower:
                    matched_skills.append(skill_name)
                    break

        return matched_skills if matched_skills else ["剧情构造师"]


class SkillOrchestrator:
    """Skill编排器 - 智能调度次级Skill"""

    def __init__(self, novel_name):
        self.novel_name = novel_name
        self.registry = SkillRegistry()
        self.dispatch_log = []
        self.context_file = f"novels/{novel_name}/skill_context.json"
        self.context = {
            "novel_name": novel_name,
            "dispatch_history": [],
            "current_phase": "初始化",
            "active_skills": []
        }
        self.load_context()

    def load_context(self):
        """加载上下文"""
        if os.path.exists(self.context_file):
            try:
                with open(self.context_file, 'r', encoding='utf-8') as f:
                    self.context = json.load(f)
                print(f"   ✅ 已加载Skill调度上下文")
            except Exception as e:
                print(f"   ⚠️ 加载上下文失败: {e}")

    def save_context(self):
        """保存上下文"""
        os.makedirs(f"novels/{self.novel_name}", exist_ok=True)
        with open(self.context_file, 'w', encoding='utf-8') as f:
            json.dump(self.context, f, indent=2, ensure_ascii=False)

    def dispatch_skill(self, skill_name, task_description, context=None):
        """调度Skill执行任务"""
        skill_info = self.registry.get_skill(skill_name)
        if not skill_info:
            print(f"   ❌ 未找到Skill: {skill_name}")
            return None

        print(f"\n   🎯 调度Skill: {skill_name}")
        print(f"   📝 任务: {task_description}")
        print(f"   🔧 能力: {', '.join(skill_info.get('capabilities', []))}")

        dispatch_record = {
            "skill": skill_name,
            "task": task_description,
            "time": datetime.now().isoformat(),
            "level": skill_info["level"]
        }
        self.dispatch_log.append(dispatch_record)
        self.context["dispatch_history"].append(dispatch_record)

        result = self.execute_skill(skill_name, task_description, context)

        self.save_context()

        return result

    def execute_skill(self, skill_name, task_description, context=None):
        """执行Skill"""
        skill_info = self.registry.get_skill(skill_name)

        skill_prompts = {
            "世界观构造师": f"""请为小说《{self.novel_name}》构建世界观！

任务：{task_description}

请构建：
1. 境界体系（详细说明每个境界）
2. 势力分布（宗门、国家、组织）
3. 地理环境（大陆、海洋、秘境）
4. 历史背景
5. 修炼规则

请详细、结构化地回答！""",

            "角色塑造师": f"""请为小说《{self.novel_name}》设计人物！

任务：{task_description}

请设计：
1. 主角（姓名、外貌、性格、背景、能力）
2. 女主
3. 配角
4. 反派
5. 人物关系

请详细、结构化地回答！""",

            "剧情构造师": f"""请为小说《{self.novel_name}》设计剧情！

任务：{task_description}

请设计：
1. 三幕结构
2. 章节规划（20-50章）
3. 爽点设计
4. 高潮布局

请详细、结构化地回答！""",

            "场景构造师": f"""请为小说《{self.novel_name}》描写场景！

任务：{task_description}

请进行生动的场景描写，包括：
1. 环境细节
2. 氛围营造
3. 感官描写（视觉、听觉、嗅觉等）

请详细、生动地描写！""",

            "对话设计师": f"""请为小说《{self.novel_name}》设计对话！

任务：{task_description}

请设计：
1. 角色对白
2. 潜台词
3. 情感表达

请让对话自然、有个性！""",

            "高潮设计师": f"""请为小说《{self.novel_name}》设计高潮！

任务：{task_description}

请设计：
1. 高潮点
2. 情绪爆发
3. 爽点安排

请让高潮有冲击力！""",

            "节奏控制师": f"""请为小说《{self.novel_name}》控制节奏！

任务：{task_description}

请分析并建议：
1. 当前节奏是否合适
2. 如何调整张弛
3. 节奏优化建议

请给出专业建议！""",

            "伏笔埋设师": f"""请为小说《{self.novel_name}》埋设伏笔！

任务：{task_description}

请设计：
1. 关键伏笔
2. 伏笔回收时机
3. 伏笔呼应

请让伏笔自然巧妙！""",

            "质量审查师": f"""请审查小说《{self.novel_name}》的质量！

任务：{task_description}

请检查：
1. 逻辑一致性
2. 角色行为合理性
3. 剧情发展
4. 语言质量

请给出改进建议！"""
        }

        prompt = skill_prompts.get(skill_name, f"请完成以下任务：{task_description}")

        if context:
            prompt += f"\n\n【上下文】\n{context}"

        system_prompt = f"你是一位专业的{skill_name}，擅长执行相关任务。"

        return call_deepseek(prompt, system_prompt, temperature=0.7)

    def auto_dispatch(self, user_input, context=None):
        """根据用户输入自动调度Skill"""
        print("\n" + "="*60)
        print("🎯 智能Skill调度")
        print("="*60)

        matched_skills = self.registry.match_skills(user_input)

        print(f"\n📝 用户输入: {user_input}")
        print(f"🎯 匹配到的Skill: {', '.join(matched_skills)}")

        if not matched_skills:
            print("   ⚠️ 未匹配到特定Skill，使用默认剧情构造师")
            matched_skills = ["剧情构造师"]

        results = {}
        for skill in matched_skills:
            result = self.dispatch_skill(skill, user_input, context)
            results[skill] = result

        return results

    def get_dispatch_plan(self, phase):
        """获取指定阶段的Skill调度计划"""
        phase_plans = {
            "世界观设定": ["世界观构造师"],
            "人物塑造": ["角色塑造师"],
            "剧情大纲": ["剧情构造师"],
            "伏笔埋设": ["伏笔埋设师", "剧情构造师"],
            "章节创作": ["场景构造师", "对话设计师", "高潮设计师", "节奏控制师"],
            "高潮设计": ["高潮设计师", "节奏控制师"],
            "质量审查": ["质量审查师"]
        }

        return phase_plans.get(phase, ["剧情构造师"])

    def execute_phase(self, phase, context=None):
        """执行指定阶段的Skill调度"""
        print("\n" + "="*60)
        print(f"🚀 执行阶段: {phase}")
        print("="*60)

        plan = self.get_dispatch_plan(phase)
        print(f"📋 Skill调度计划: {', '.join(plan)}")

        self.context["current_phase"] = phase

        results = {}
        for skill in plan:
            result = self.dispatch_skill(skill, f"执行{phase}任务", context)
            results[skill] = result

        self.save_context()

        return results

    def display_dispatch_log(self):
        """显示Skill调度日志"""
        print("\n" + "="*60)
        print("📋 Skill调度日志")
        print("="*60)

        if not self.dispatch_log:
            print("   暂无调度记录")
            return

        for i, record in enumerate(self.dispatch_log, 1):
            print(f"\n{i}. [{record['level']}级] {record['skill']}")
            print(f"   任务: {record['task']}")
            print(f"   时间: {record['time']}")


def main():
    print("="*60)
    print("🎯 NWACS V8.0 智能Skill调度系统")
    print("="*60)
    print("\n【核心功能】")
    print("  ✅ Skill注册表 - 明确定义每个Skill的功能")
    print("  ✅ 智能匹配 - 根据输入自动匹配需要的Skill")
    print("  ✅ 调度编排 - 主Skill有序调度次级Skill")
    print("  ✅ 触发条件 - 明确什么情况下调用什么Skill")
    print("  ✅ 调度日志 - 记录所有Skill调度历史")
    print("="*60)

    novel_name = input("\n请输入小说名称: ").strip()
    if not novel_name:
        novel_name = "测试小说"

    orchestrator = SkillOrchestrator(novel_name)

    print("\n请选择操作:")
    print("   1. 📝 根据输入自动调度")
    print("   2. 🚀 执行完整写作流程（7阶段）")
    print("   3. 📋 查看调度日志")
    print("   4. 🔍 查看Skill注册表")

    choice = input("\n请选择 (1/2/3/4): ").strip()

    if choice == "1":
        user_input = input("\n请输入创作需求: ").strip()
        if user_input:
            orchestrator.auto_dispatch(user_input)

    elif choice == "2":
        phases = [
            "世界观设定",
            "人物塑造",
            "剧情大纲",
            "伏笔埋设",
            "章节创作",
            "高潮设计",
            "质量审查"
        ]

        for phase in phases:
            results = orchestrator.execute_phase(phase)
            if len(phases) > 1:
                choice = input("\n是否继续下一阶段？(Y/n): ").strip().lower()
                if choice == "n":
                    break

    elif choice == "3":
        orchestrator.display_dispatch_log()

    elif choice == "4":
        registry = SkillRegistry()
        print("\n📋 Skill注册表:")
        for skill_name, skill_info in registry.skills.items():
            print(f"\n【{skill_name}】(等级: {skill_info['level']})")
            print(f"   描述: {skill_info['description']}")
            print(f"   能力: {', '.join(skill_info.get('capabilities', []))}")
            if skill_info.get('trigger_keywords'):
                print(f"   触发词: {', '.join(skill_info['trigger_keywords'][:10])}...")

    print("\n✅ Skill调度系统演示完成！")


if __name__ == "__main__":
    main()
