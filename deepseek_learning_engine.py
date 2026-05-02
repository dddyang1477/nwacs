"""
NWACS v7.0 DeepSeek联网学习脚本
使用DeepSeek API进行自动化学习优化

使用前请先：
1. 安装依赖：pip install openai
2. 配置环境变量：export DEEPSEEK_API_KEY="your-api-key"
   或在代码中直接设置 DEEPSEEK_API_KEY = "your-api-key"

运行方式：
python deepseek_learning_engine.py --duration 4h
"""

import os
import time
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

try:
    from openai import OpenAI
except ImportError:
    print("❌ 请先安装 openai 库：pip install openai")
    exit(1)

class DeepSeekLearningEngine:
    """DeepSeek联网学习引擎"""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise ValueError("❌ 请设置 DEEPSEEK_API_KEY 环境变量或传入api_key参数")

        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.deepseek.com"
        )

        self.knowledge_base_path = Path("skills/level2/learnings")
        self.report_path = Path("skills/level2/learnings/学习进化报告")

        self.learned_content = []
        self.start_time = None
        self.end_time = None

        self.knowledge_bases = [
            "跨媒体开发知识库.txt",
            "学习进化系统知识库.txt",
            "2026年最新网文写作技巧与市场趋势.txt",
            "小说类型解剖式学习手册.txt",
            "玄幻修仙小说知识库.txt",
            "都市小说详细知识库.txt",
            "女频言情小说详细知识库.txt",
            "悬疑推理小说详细知识库.txt",
            "科幻末日小说详细知识库.txt",
            "写作技巧_画面感与人物刻画指南.txt",
            "小说人物起名知识库.txt",
            "网络流行语知识库.txt"
        ]

    def log(self, message: str):
        """带时间戳的日志输出"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")

    def call_deepseek(self, system_prompt: str, user_prompt: str, model: str = "deepseek-chat") -> str:
        """调用DeepSeek API"""
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            return response.choices[0].message.content
        except Exception as e:
            self.log(f"❌ API调用失败: {e}")
            return ""

    def learn_knowledge_base(self, kb_name: str) -> Dict[str, Any]:
        """学习单个知识库"""
        kb_path = self.knowledge_base_path / kb_name

        if not kb_path.exists():
            self.log(f"⚠️ 知识库不存在: {kb_name}")
            return {"status": "skipped", "reason": "file not found"}

        self.log(f"📚 开始学习: {kb_name}")

        with open(kb_path, 'r', encoding='utf-8') as f:
            content = f.read()

        system_prompt = """你是一个专业的网文创作知识学习助手。
你的任务是：
1. 深度理解提供的知识库内容
2. 提取核心要点和关键模式
3. 用简洁的语言总结学习成果
4. 识别可以应用到实际创作的关键技巧"""

        user_prompt = f"""请学习以下知识库内容，并提取核心学习要点：

文件名：{kb_name}

内容：
{content[:8000]}

请用以下格式输出学习摘要：
1. 核心知识点（3-5个）
2. 可应用的创作技巧（3-5个）
3. 需要注意的要点（2-3个）
4. 对其他Skill的优化建议（如有）"""

        result = self.call_deepseek(system_prompt, user_prompt)

        self.learned_content.append({
            "knowledge_base": kb_name,
            "result": result,
            "timestamp": datetime.now().isoformat()
        })

        self.log(f"✅ 完成: {kb_name}")
        return {"status": "success", "result": result}

    def learn_all_knowledge_bases(self):
        """学习所有知识库"""
        self.log("🚀 开始DeepSeek联网学习...")

        for i, kb in enumerate(self.knowledge_bases, 1):
            self.log(f"📖 进度: {i}/{len(self.knowledge_bases)}")
            self.learn_knowledge_base(kb)
            time.sleep(2)

    def analyze_market_trends(self):
        """分析市场趋势"""
        self.log("📊 开始市场趋势分析...")

        system_prompt = """你是一个专业的网文市场分析师。
你的任务是分析当前网文市场趋势，并为创作提供指导。"""

        user_prompt = """请分析2026年5月网文市场趋势，包括：
1. 当前最火爆的题材类型
2. 读者偏好变化
3. 平台算法特点
4. 爆款作品的共同特征
5. 创作者应该注意的要点

请给出详细的分析报告。"""

        result = self.call_deepseek(system_prompt, user_prompt)

        self.learned_content.append({
            "type": "market_analysis",
            "result": result,
            "timestamp": datetime.now().isoformat()
        })

        self.log("✅ 市场趋势分析完成")
        return result

    def optimize_skills(self):
        """优化所有Skill"""
        self.log("⚙️ 开始Skill优化...")

        system_prompt = """你是一个专业的Skill优化专家。
你的任务是分析现有Skill的不足，并提出优化建议。"""

        user_prompt = """请分析以下v7.0 Skill系统的优化方向：

已学习的知识库要点：
{self._format_learned_content()}

请给出：
1. 各Skill的优化建议
2. Skill协作效率提升方案
3. 跨媒体适配优化方向
4. 学习进化系统改进建议"""

        result = self.call_deepseek(system_prompt, user_prompt)

        self.learned_content.append({
            "type": "skill_optimization",
            "result": result,
            "timestamp": datetime.now().isoformat()
        })

        self.log("✅ Skill优化完成")
        return result

    def _format_learned_content(self) -> str:
        """格式化已学习内容"""
        formatted = []
        for item in self.learned_content[-5:]:
            formatted.append(f"### {item.get('knowledge_base', item.get('type'))}\n{item.get('result', '')[:500]}")
        return "\n\n".join(formatted)

    def generate_report(self) -> str:
        """生成学习报告"""
        self.log("📝 生成学习报告...")

        report = f"""# NWACS v7.0 DeepSeek联网学习报告

## 学习概况
- **开始时间**: {self.start_time}
- **结束时间**: {self.end_time}
- **学习知识库数**: {len(self.knowledge_bases)}
- **API调用次数**: {len(self.learned_content)}

## 已学习知识库

"""

        for item in self.learned_content:
            kb_name = item.get('knowledge_base', item.get('type', 'unknown'))
            report += f"""### {kb_name}

{item.get('result', '')[:1000]}

---

"""

        report += f"""
## 市场趋势分析

{self.learned_content[-2].get('result', '') if len(self.learned_content) >= 2 else 'N/A'}

## Skill优化建议

{self.learned_content[-1].get('result', '') if self.learned_content else 'N/A'}

## 下一步建议

1. 持续学习：建议每天学习2小时
2. 知识更新：每周更新一次市场趋势
3. Skill迭代：根据学习成果持续优化

---
*报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
*由DeepSeek Learning Engine v1.0生成*
"""

        self.report_path.mkdir(parents=True, exist_ok=True)
        report_file = self.report_path / f"学习报告_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)

        self.log(f"✅ 报告已保存: {report_file}")
        return report

    def run(self, duration_hours: float = 4):
        """运行学习引擎"""
        self.start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log(f"🎯 开始{duration_hours}小时深度学习...")

        self.learn_all_knowledge_bases()
        self.analyze_market_trends()
        self.optimize_skills()

        self.end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        report = self.generate_report()

        self.log("🎉 学习完成！")
        return report


def main():
    import argparse

    parser = argparse.ArgumentParser(description='NWACS v7.0 DeepSeek联网学习引擎')
    parser.add_argument('--duration', type=str, default='4h', help='学习时长，如 4h, 2h, 30m')
    parser.add_argument('--api-key', type=str, default=None, help='DeepSeek API密钥')

    args = parser.parse_args()

    duration_map = {'4h': 4, '2h': 2, '1h': 1, '30m': 0.5}
    duration = duration_map.get(args.duration, 4)

    try:
        engine = DeepSeekLearningEngine(api_key=args.api_key)
        engine.run(duration_hours=duration)
    except ValueError as e:
        print(e)
        print("\n📌 使用方法：")
        print("1. 设置环境变量：export DEEPSEEK_API_KEY='your-key'")
        print("2. 运行脚本：python deepseek_learning_engine.py --duration 4h")


if __name__ == "__main__":
    main()
