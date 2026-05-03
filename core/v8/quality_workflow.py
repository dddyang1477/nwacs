#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS V8.0 质量检测工作流系统
- 检测结果反馈给谁
- 谁来负责整改
- 整改完谁再次检测
- 三次循环触发人工处理
- 三次以内合格输出文本
"""

import sys
import json
import os
from datetime import datetime
from enum import Enum

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


class QualityLevel(Enum):
    """质量等级"""
    S_LEVEL = "S级（优秀）"
    A_LEVEL = "A级（良好）"
    B_LEVEL = "B级（合格）"
    C_LEVEL = "C级（需改进）"
    D_LEVEL = "D级（不合格）"


class DetectionResult:
    """检测结果"""

    def __init__(self):
        self.ai_score = 0
        self.quality_score = 0
        self.total_score = 0
        self.level = None
        self.issues = []
        self.suggestions = []
        self.detection_time = None

    def to_dict(self):
        return {
            "ai_score": self.ai_score,
            "quality_score": self.quality_score,
            "total_score": self.total_score,
            "level": self.level.value if self.level else None,
            "issues": self.issues,
            "suggestions": self.suggestions,
            "detection_time": self.detection_time
        }


class QualityWorkflowManager:
    """质量检测工作流管理器"""

    def __init__(self, novel_name="测试小说"):
        self.novel_name = novel_name
        self.workflow_dir = f"novels/{novel_name}/quality_workflow"
        os.makedirs(self.workflow_dir, exist_ok=True)

        # 工作流状态
        self.workflow_state = {
            "novel_name": novel_name,
            "current_phase": "初始化",
            "detection_count": 0,
            "max_detection": 3,
            "status": "pending",
            "detections": [],
            "final_result": None,
            "need_human_intervention": False,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }

        # 责任人定义
        self.responsibility_map = {
            "ai_pattern": {
                "responsible": "AI优化专员",
                "description": "负责优化AI写作特征",
                "action": "调用AI优化器"
            },
            "logic_issue": {
                "responsible": "逻辑审查员",
                "description": "负责修复逻辑问题",
                "action": "重构相关段落"
            },
            "consistency_issue": {
                "responsible": "一致性审查员",
                "description": "负责保持角色/设定一致",
                "action": "修正不一致内容"
            },
            "quality_issue": {
                "responsible": "质量优化员",
                "description": "负责提升整体质量",
                "action": "全面优化文本"
            }
        }

        self.load_state()

    def load_state(self):
        """加载工作流状态"""
        state_file = f"{self.workflow_dir}/workflow_state.json"
        if os.path.exists(state_file):
            try:
                with open(state_file, 'r', encoding='utf-8') as f:
                    self.workflow_state = json.load(f)
                print(f"   ✅ 已加载工作流状态")
            except Exception as e:
                print(f"   ⚠️ 加载失败: {e}")

    def save_state(self):
        """保存工作流状态"""
        self.workflow_state["updated_at"] = datetime.now().isoformat()
        state_file = f"{self.workflow_dir}/workflow_state.json"
        with open(state_file, 'w', encoding='utf-8') as f:
            json.dump(self.workflow_state, f, indent=2, ensure_ascii=False)
        print(f"   ✅ 工作流状态已保存")

    def check_ai_pattern(self, text):
        """检查AI特征"""
        issues = []

        ai_patterns = [
            "首先", "其次", "然后", "最后",
            "因此", "所以", "然而", "但是",
            "内心深处", "不由自主地"
        ]

        for pattern in ai_patterns:
            count = text.count(pattern)
            if count > 3:
                issues.append({
                    "type": "ai_pattern",
                    "pattern": pattern,
                    "count": count,
                    "severity": "high" if count > 5 else "medium"
                })

        return issues

    def check_quality(self, text):
        """检查质量"""
        issues = []

        # 句子长度检查
        sentences = text.split(/[.。!！?？]/)
        avg_len = sum(len(s) for s in sentences) / max(len(sentences), 1)

        if avg_len > 50:
            issues.append({
                "type": "quality_issue",
                "issue": "句子过长",
                "detail": f"平均句子长度：{avg_len:.1f}字符"
            })

        # 段落一致性检查
        paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
        if paragraphs:
            lens = [len(p) for p in paragraphs]
            variance = sum((l - sum(lens)/len(lens))**2 for l in lens) / len(lens)
            if variance < 50:
                issues.append({
                    "type": "quality_issue",
                    "issue": "段落结构过于规整",
                    "detail": f"段落长度方差：{variance:.1f}"
                })

        return issues

    def calculate_scores(self, text):
        """计算综合得分"""
        result = DetectionResult()
        result.detection_time = datetime.now().isoformat()

        # AI检测得分
        ai_issues = self.check_ai_pattern(text)
        ai_penalty = len(ai_issues) * 15
        result.ai_score = max(0, 100 - ai_penalty)

        # 质量得分
        quality_issues = self.check_quality(text)
        quality_penalty = len(quality_issues) * 20
        result.quality_score = max(0, 100 - quality_penalty)

        # 综合得分
        result.total_score = (result.ai_score * 0.6 + result.quality_score * 0.4)

        # 确定等级
        if result.total_score >= 90:
            result.level = QualityLevel.S_LEVEL
        elif result.total_score >= 80:
            result.level = QualityLevel.A_LEVEL
        elif result.total_score >= 70:
            result.level = QualityLevel.B_LEVEL
        elif result.total_score >= 60:
            result.level = QualityLevel.C_LEVEL
        else:
            result.level = QualityLevel.D_LEVEL

        # 收集所有问题
        result.issues = ai_issues + quality_issues

        # 生成改进建议
        for issue in result.issues:
            if issue["type"] == "ai_pattern":
                result.suggestions.append({
                    "issue": f"AI特征过多：'{issue['pattern']}'出现{issue['count']}次",
                    "responsible": "AI优化专员",
                    "action": "替换为更自然的表达"
                })
            else:
                result.suggestions.append({
                    "issue": issue.get("issue", "质量问题"),
                    "responsible": "质量优化员",
                    "action": "优化文本结构"
                })

        return result

    def get_responsible_person(self, issue_type):
        """获取责任人"""
        return self.responsibility_map.get(issue_type, {
            "responsible": "质量优化员",
            "description": "负责通用优化",
            "action": "全面优化"
        })

    def report_result(self, result):
        """反馈检测结果"""
        print("\n" + "="*60)
        print("📊 质量检测报告")
        print("="*60)

        print(f"\n【综合得分】{result.total_score}/100 ({result.level.value})")

        print(f"\n【AI检测】{result.ai_score}/100")
        print(f"【质量评估】{result.quality_score}/100")

        if result.issues:
            print(f"\n【发现问题】共{len(result.issues)}个：")
            for i, issue in enumerate(result.issues, 1):
                resp = self.get_responsible_person(issue["type"])
                print(f"\n{i}. [{issue['type']}] {issue.get('pattern') or issue.get('issue')}")
                print(f"   严重程度: {issue.get('severity', 'medium')}")
                print(f"   责任人: {resp['responsible']}")
                print(f"   职责: {resp['description']}")
                print(f"   应采取行动: {resp['action']}")

        if result.suggestions:
            print(f"\n【改进建议】")
            for i, suggestion in enumerate(result.suggestions, 1):
                print(f"{i}. {suggestion['issue']}")
                print(f"   → 负责人: {suggestion['responsible']}")
                print(f"   → 行动: {suggestion['action']}")

        return result

    def optimize_text(self, text, result):
        """优化文本"""
        print("\n" + "="*60)
        print("🔧 执行整改")
        print("="*60)

        print("\n【责任人认领任务】")
        responsible_tasks = {}
        for suggestion in result.suggestions:
            resp = suggestion["responsible"]
            if resp not in responsible_tasks:
                responsible_tasks[resp] = []
            responsible_tasks[resp].append(suggestion)

        for resp, tasks in responsible_tasks.items():
            print(f"\n📋 {resp}:")
            for task in tasks:
                print(f"   - {task['issue']}")
                print(f"     → {task['action']}")

        print("\n⏳ 调用DeepSeek进行智能优化...")
        prompt = f"""请优化以下小说文本，降低AI检测率，提升质量！

【当前问题】
{chr(10).join([f"- {s['issue']} → {s['action']}" for s in result.suggestions])}

【待优化文本】
{text}

【要求】
1. 解决所有AI特征问题
2. 改善文本结构
3. 保持故事完整性
4. 让文字更自然流畅

请直接输出优化后的文本："""

        system_prompt = "你是一位专业的小说优化师，擅长优化AI生成的文本，使其更自然、更高质量。"

        optimized = call_deepseek(prompt, system_prompt, temperature=0.9)

        if optimized:
            print("   ✅ 优化完成！")
            return optimized

        return text

    def should_generate(self, result):
        """判断是否应该生成"""
        return result.total_score >= 70

    def run_workflow(self, text, chapter_num=1):
        """运行质量检测工作流"""
        print("\n" + "="*60)
        print(f"🚀 启动质量检测工作流 - 第{chapter_num}章")
        print("="*60)

        self.workflow_state["current_phase"] = "检测"
        self.workflow_state["detection_count"] += 1
        self.save_state()

        # 第一次检测
        print(f"\n【第{self.workflow_state['detection_count']}次检测】")
        result = self.calculate_scores(text)
        self.report_result(result)

        # 记录检测结果
        detection_record = {
            "count": self.workflow_state["detection_count"],
            "time": result.detection_time,
            "scores": {
                "ai_score": result.ai_score,
                "quality_score": result.quality_score,
                "total_score": result.total_score
            },
            "level": result.level.value,
            "issues_count": len(result.issues)
        }
        self.workflow_state["detections"].append(detection_record)

        # 判断是否合格
        if result.total_score >= 70:
            print(f"\n✅ 检测合格！得分：{result.total_score}/100 ({result.level.value})")
            self.workflow_state["status"] = "passed"
            self.workflow_state["final_result"] = result.to_dict()
            self.save_state()
            return text, True, result

        # 检查是否超过最大检测次数
        if self.workflow_state["detection_count"] >= self.workflow_state["max_detection"]:
            print(f"\n🚨 已达到最大检测次数（{self.workflow_state['max_detection']}次）！")
            print("⚠️ 触发人工介入警报！")

            self.workflow_state["status"] = "human_intervention_required"
            self.workflow_state["need_human_intervention"] = True
            self.save_state()

            # 生成人工介入报告
            self.generate_alert_report(result)

            return text, False, result

        # 继续优化
        print(f"\n🔄 检测未通过，开始第{self.workflow_state['detection_count']}次整改...")

        optimized_text = self.optimize_text(text, result)

        self.workflow_state["current_phase"] = "整改"
        self.save_state()

        # 递归继续检测（最多3次）
        return self.run_workflow(optimized_text, chapter_num)

    def generate_alert_report(self, result):
        """生成人工介入警报报告"""
        print("\n" + "="*60)
        print("🚨🚨🚨 人工介入警报 🚨🚨🚨")
        print("="*60)

        report = {
            "alert_type": "HUMAN_INTERVENTION_REQUIRED",
            "time": datetime.now().isoformat(),
            "chapter": "待定",
            "detection_count": self.workflow_state["detection_count"],
            "final_score": result.total_score,
            "final_level": result.level.value,
            "remaining_issues": result.issues,
            "priority": "HIGH",
            "action_required": "人工审核并决定是否生成"
        }

        alert_file = f"{self.workflow_dir}/alert_human_intervention.json"
        with open(alert_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        print(f"\n【警报详情】")
        print(f"  类型: 人工介入请求")
        print(f"  时间: {report['time']}")
        print(f"  检测次数: {report['detection_count']}次")
        print(f"  最终得分: {report['final_score']}/100")
        print(f"  等级: {report['final_level']}")
        print(f"  剩余问题: {len(report['remaining_issues'])}个")

        print(f"\n【需要人工处理】")
        print(f"  1. 审核文本内容")
        print(f"  2. 决定是否强制生成")
        print(f"  3. 或进行手动修改")

        print(f"\n【警报文件】")
        print(f"  {alert_file}")

        return report

    def display_workflow_status(self):
        """显示工作流状态"""
        print("\n" + "="*60)
        print("📋 质量检测工作流状态")
        print("="*60)

        state = self.workflow_state

        print(f"\n【基本信息】")
        print(f"  小说: {state['novel_name']}")
        print(f"  当前阶段: {state['current_phase']}")
        print(f"  状态: {state['status']}")
        print(f"  检测次数: {state['detection_count']}/{state['max_detection']}")

        if state["detections"]:
            print(f"\n【检测历史】")
            for det in state["detections"]:
                print(f"  第{det['count']}次: {det['scores']['total_score']}/100 ({det['level']})")

        if state["need_human_intervention"]:
            print(f"\n🚨 需要人工介入！")

        if state["final_result"]:
            print(f"\n【最终结果】")
            fr = state["final_result"]
            print(f"  得分: {fr['total_score']}/100")
            print(f"  等级: {fr['level']}")

    def force_generate(self, text, reason):
        """强制生成（需要人工授权）"""
        print("\n" + "="*60)
        print("⚠️ 强制生成请求")
        print("="*60)

        print(f"\n强制原因: {reason}")
        print(f"当前得分: {self.workflow_state['final_result']['total_score'] if self.workflow_state['final_result'] else 'N/A'}")

        confirm = input("\n确认强制生成？(yes/no): ").strip().lower()
        if confirm == "yes":
            self.workflow_state["status"] = "force_generated"
            self.workflow_state["force_reason"] = reason
            self.save_state()
            print("   ✅ 已强制生成")
            return True

        print("   ❌ 取消强制生成")
        return False


def main():
    print("="*60)
    print("🔍 NWACS V8.0 质量检测工作流系统")
    print("="*60)
    print("\n【工作流程】")
    print("  1. 检测 → 反馈结果")
    print("  2. 不合格 → 分配责任人整改")
    print("  3. 整改 → 再次检测")
    print("  4. 循环3次 → 触发人工介入")
    print("  5. 3次内合格 → 输出文本")
    print("="*60)

    print("\n请选择操作：")
    print("  1. 🔍 运行质量检测工作流")
    print("  2. 📊 查看工作流状态")
    print("  3. 📋 测试示例")

    choice = input("\n请选择: ").strip()

    if choice == "1":
        novel_name = input("请输入小说名称: ").strip() or "测试小说"
        manager = QualityWorkflowManager(novel_name)

        print("\n请输入要检测的文本（直接回车使用示例）：")
        sample = """首先，叶青云站在山巅之上，他感到内心深处有一种难以言喻的情绪在涌动。
然后，他开始运转功法，吸收天地之间的灵气。
因此，他的修为在不断提升，境界也在逐步突破。
然而，就在这时，天空突然暗了下来，乌云密布。
但是，叶青云并没有惊慌失措，他相信自己的实力。
最后，一道闪电划破天空，照亮了整个世界。"""

        text = input().strip()
        if not text:
            text = sample

        optimized_text, success, result = manager.run_workflow(text)

        if success:
            print("\n" + "="*60)
            print("✅ 文本已通过质量检测！")
            print("="*60)
            print("\n【最终得分】")
            print(f"  AI检测: {result.ai_score}/100")
            print(f"  质量评估: {result.quality_score}/100")
            print(f"  综合得分: {result.total_score}/100")
            print(f"  等级: {result.level.value}")

            print("\n【优化后的文本】")
            print(optimized_text[:500] + "..." if len(optimized_text) > 500 else optimized_text)
        else:
            print("\n" + "="*60)
            print("⚠️ 需要人工介入！")
            print("="*60)
            print("\n请人工审核文本，决定是否强制生成。")

    elif choice == "2":
        novel_name = input("请输入小说名称: ").strip() or "测试小说"
        manager = QualityWorkflowManager(novel_name)
        manager.display_workflow_status()

    elif choice == "3":
        print("\n【测试示例】")
        sample = """首先，主角站在山巅，俯瞰着整个世界。
然后，他开始回忆自己的过去，内心充满了复杂的情感。
因此，他决定要变得更强大，保护自己在意的人。
然而，前方的道路充满了未知和危险。
但是，他并没有退缩，而是勇敢地迎接挑战。
最后，他终于达到了自己的目标，成为了真正的强者。"""

        print("\n原文本：")
        print(sample)

        manager = QualityWorkflowManager("测试")
        result = manager.calculate_scores(sample)
        manager.report_result(result)

        print("\n" + "="*60)
        print("是否继续运行工作流进行优化？(y/n)")
        choice = input().strip().lower()
        if choice == "y":
            optimized, success, final_result = manager.run_workflow(sample)
            if success:
                print("\n✅ 优化后的文本：")
                print(optimized[:500] + "..." if len(optimized) > 500 else optimized)


if __name__ == "__main__":
    main()
