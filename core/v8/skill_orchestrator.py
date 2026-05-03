#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS V8.0 Skill协作编排系统
实现小说写作流水线，让多个Skill有序高效地协作
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
        response = requests.post(url, headers=headers, json=data, timeout=180)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"   ❌ DeepSeek调用失败: {e}")
        return None


class NovelWritingPipeline:
    """小说写作流水线 - Skill协作编排系统"""

    def __init__(self, novel_name, genre="玄幻"):
        self.novel_name = novel_name
        self.genre = genre
        self.pipeline_dir = f"novels/{novel_name}/pipeline"
        os.makedirs(self.pipeline_dir, exist_ok=True)

        # 写作阶段定义
        self.pipeline_stages = [
            {
                "stage_id": 1,
                "name": "世界观设定",
                "skills": ["世界观构造师"],
                "description": "构建小说的世界观、境界体系、势力分布",
                "input": "小说主题、类型、基本背景",
                "output": "完整的世界观设定文档"
            },
            {
                "stage_id": 2,
                "name": "人物塑造",
                "skills": ["角色塑造师"],
                "description": "设计主角、配角、反派的完整设定",
                "input": "世界观设定",
                "output": "人物设定文档、人物关系图谱"
            },
            {
                "stage_id": 3,
                "name": "剧情大纲",
                "skills": ["剧情构造师"],
                "description": "设计完整的三幕结构、章节规划、高潮布局",
                "input": "世界观、人物设定",
                "output": "剧情大纲文档、章节规划表"
            },
            {
                "stage_id": 4,
                "name": "伏笔埋设",
                "skills": ["伏笔埋设师"],
                "description": "在前文埋设关键伏笔，为后续剧情做准备",
                "input": "剧情大纲、人物设定",
                "output": "伏笔埋设计划、关键伏笔清单"
            },
            {
                "stage_id": 5,
                "name": "章节创作",
                "skills": ["场景构造师", "对话设计师"],
                "description": "逐章创作，每个章节进行场景描写和对话设计",
                "input": "剧情大纲、伏笔计划、当前章节设定",
                "output": "章节内容"
            },
            {
                "stage_id": 6,
                "name": "高潮设计",
                "skills": ["高潮设计师", "节奏控制师"],
                "description": "优化每章的高潮场面，控制整体节奏",
                "input": "章节内容",
                "output": "优化后的高潮章节"
            },
            {
                "stage_id": 7,
                "name": "质量审查",
                "skills": ["质量审查师"],
                "description": "审查整体质量，逻辑检查，细节补充",
                "input": "完整小说",
                "output": "修改建议、优化版本"
            }
        ]

        # 当前进度
        self.current_stage = 0
        self.pipeline_state = {
            "novel_name": novel_name,
            "genre": genre,
            "start_time": datetime.now().isoformat(),
            "stages_completed": [],
            "current_stage": 0,
            "stage_outputs": {}
        }

    def load_pipeline(self):
        """加载流水线状态"""
        state_file = f"{self.pipeline_dir}/pipeline_state.json"
        if os.path.exists(state_file):
            try:
                with open(state_file, 'r', encoding='utf-8') as f:
                    self.pipeline_state = json.load(f)
                print(f"   ✅ 已加载流水线状态")
                return True
            except Exception as e:
                print(f"   ⚠️ 加载流水线失败: {e}")
        return False

    def save_pipeline(self):
        """保存流水线状态"""
        state_file = f"{self.pipeline_dir}/pipeline_state.json"
        with open(state_file, 'w', encoding='utf-8') as f:
            json.dump(self.pipeline_state, f, indent=2, ensure_ascii=False)
        print(f"   ✅ 流水线状态已保存")

    def display_pipeline(self):
        """显示整个写作流水线"""
        print("\n" + "="*60)
        print("📋 NWACS V8.0 小说写作流水线")
        print("="*60)

        print("\n写作流程:")
        for stage in self.pipeline_stages:
            status = "✅" if stage["stage_id"] in self.pipeline_state["stages_completed"] else "⏳"
            current = "👈 当前" if stage["stage_id"] == self.pipeline_state["current_stage"] else ""
            print(f"\n{status} 阶段{stage['stage_id']}: {stage['name']} {current}")
            print(f"   Skill: {', '.join(stage['skills'])}")
            print(f"   {stage['description']}")

        print("\n" + "="*60)

    def execute_stage(self, stage_id):
        """执行单个阶段"""
        stage = self.pipeline_stages[stage_id - 1]
        print(f"\n" + "="*60)
        print(f"🚀 执行阶段{stage['stage_id']}: {stage['name']}")
        print("="*60)

        # 根据阶段类型执行不同的逻辑
        if stage["name"] == "世界观设定":
            output = self._world_building_stage()
        elif stage["name"] == "人物塑造":
            output = self._character_design_stage()
        elif stage["name"] == "剧情大纲":
            output = self._plot_outline_stage()
        elif stage["name"] == "伏笔埋设":
            output = self._foreshadowing_stage()
        elif stage["name"] == "章节创作":
            output = self._chapter_writing_stage()
        elif stage["name"] == "高潮设计":
            output = self._climax_design_stage()
        elif stage["name"] == "质量审查":
            output = self._quality_review_stage()
        else:
            output = "未知阶段"

        if output:
            # 保存阶段输出
            output_file = f"{self.pipeline_dir}/stage_{stage_id:02d}_output.md"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"# {stage['name']}\n\n")
                f.write(output)

            # 更新流水线状态
            self.pipeline_state["stages_completed"].append(stage_id)
            self.pipeline_state["stage_outputs"][str(stage_id)] = {
                "stage_name": stage['name'],
                "output_file": output_file,
                "completed_time": datetime.now().isoformat()
            }

            if stage_id < len(self.pipeline_stages):
                self.pipeline_state["current_stage"] = stage_id + 1
            else:
                self.pipeline_state["current_stage"] = "all_completed"

            self.save_pipeline()
            return True

        return False

    def _world_building_stage(self):
        """阶段1: 世界观设定"""
        prompt = f"""请为小说《{self.novel_name}》（{self.genre}类型）构建完整的世界观设定：

请包括：
1. 境界体系（详细说明每个境界）
2. 势力分布（主要势力、宗门、国家）
3. 地理环境（大陆、海洋、秘境、险地）
4. 历史背景（重要历史事件）
5. 修炼法则（特殊规则、禁忌）

请详细、结构化地回答，至少1000字以上。"""

        system_prompt = "你是一位专业的玄幻小说世界观设计师，擅长构建宏大而严谨的世界观设定。"
        print(f"   🔧 调用技能: 世界观构造师")
        output = call_deepseek(prompt, system_prompt, temperature=0.7)

        if output:
            print(f"   ✅ 世界观设定完成")
        return output

    def _character_design_stage(self):
        """阶段2: 人物塑造"""
        prompt = f"""请为小说《{self.novel_name}》设计完整的人物设定：

请包括：
1. 主角（姓名、外貌、性格、背景、成长弧光、金手指）
2. 女主角（姓名、外貌、性格、背景、与主角关系）
3. 配角（至少3-5个重要配角）
4. 反派（至少1-2个反派，要有动机）
5. 人物关系图谱（主要人物之间的关系）

请详细、结构化地回答。"""

        system_prompt = "你是一位专业的人物塑造师，擅长设计立体而有魅力的小说人物。"
        print(f"   🔧 调用技能: 角色塑造师")
        output = call_deepseek(prompt, system_prompt, temperature=0.7)

        if output:
            print(f"   ✅ 人物塑造完成")
        return output

    def _plot_outline_stage(self):
        """阶段3: 剧情大纲"""
        prompt = f"""请为小说《{self.novel_name}》设计完整的剧情大纲：

请包括：
1. 核心主题和核心冲突
2. 三幕结构设计：
   - 第一幕（开篇铺垫）
   - 第二幕（发展和冲突）
   - 第三幕（高潮和结局）
3. 章节规划（至少20-50章的规划）
4. 主要爽点设计
5. 高潮布局

请详细、结构化地回答。"""

        system_prompt = "你是一位专业的剧情构造师，擅长设计紧凑而有吸引力的小说剧情大纲。"
        print(f"   🔧 调用技能: 剧情构造师")
        output = call_deepseek(prompt, system_prompt, temperature=0.7)

        if output:
            print(f"   ✅ 剧情大纲完成")
        return output

    def _foreshadowing_stage(self):
        """阶段4: 伏笔埋设"""
        prompt = f"""请为小说《{self.novel_name}》设计伏笔埋设计划：

请包括：
1. 开篇需要埋设的关键伏笔
2. 中期需要埋设的伏笔
3. 各伏笔的回收时机
4. 伏笔埋设技巧和要点
5. 避免伏笔冲突或遗忘的注意事项

请详细、结构化地回答。"""

        system_prompt = "你是一位专业的伏笔埋设师，擅长在前文埋设自然而巧妙的伏笔。"
        print(f"   🔧 调用技能: 伏笔埋设师")
        output = call_deepseek(prompt, system_prompt, temperature=0.7)

        if output:
            print(f"   ✅ 伏笔埋设完成")
        return output

    def _chapter_writing_stage(self):
        """阶段5: 章节创作（示例）"""
        prompt = f"""请为小说《{self.novel_name}》创作第1章：

要求：
1. 开篇即高能，吸引读者
2. 展现主角现状
3. 埋设关键伏笔
4. 结尾留钩子，让读者想看下一章
5. 场景描写要生动
6. 对话要自然
7. 字数：2000-3000字

请完整创作。"""

        system_prompt = "你是一位顶尖的小说作家，擅长写精彩的开篇章节。"
        print(f"   🔧 调用技能: 场景构造师 + 对话设计师")
        output = call_deepseek(prompt, system_prompt, temperature=0.7)

        if output:
            print(f"   ✅ 第1章创作完成")
        return output

    def _climax_design_stage(self):
        """阶段6: 高潮设计"""
        prompt = f"""请为小说《{self.novel_name}》优化章节，设计高潮场面：

要求：
1. 分析章节中的高潮点是否足够突出
2. 优化情绪节奏，让高潮更有冲击力
3. 控制整体节奏，张弛有度
4. 增强爽点
5. 优化场景描写和对话

请给出优化建议和优化后的章节内容。"""

        system_prompt = "你是一位专业的高潮设计师和节奏控制师，擅长营造有冲击力的小说高潮。"
        print(f"   🔧 调用技能: 高潮设计师 + 节奏控制师")
        output = call_deepseek(prompt, system_prompt, temperature=0.7)

        if output:
            print(f"   ✅ 高潮设计完成")
        return output

    def _quality_review_stage(self):
        """阶段7: 质量审查"""
        prompt = f"""请对小说《{self.novel_name}》进行质量审查：

请检查：
1. 逻辑是否自洽
2. 人物行为是否符合设定
3. 情节发展是否合理
4. 伏笔是否合理埋设和回收
5. 语言质量
6. 节奏是否得当
7. 有哪些可以改进的地方

请给出详细的审查意见和修改建议。"""

        system_prompt = "你是一位专业的小说编辑，擅长审查小说质量并提出改进建议。"
        print(f"   🔧 调用技能: 质量审查师")
        output = call_deepseek(prompt, system_prompt, temperature=0.7)

        if output:
            print(f"   ✅ 质量审查完成")
        return output

    def run_entire_pipeline(self):
        """运行整个写作流水线"""
        self.display_pipeline()

        print(f"\n🎯 开始执行小说写作流水线")
        print(f"小说: {self.novel_name}")
        print(f"类型: {self.genre}")

        for stage in self.pipeline_stages:
            if stage["stage_id"] in self.pipeline_state["stages_completed"]:
                print(f"\n⏭️ 阶段{stage['stage_id']}已完成，跳过")
                continue

            success = self.execute_stage(stage["stage_id"])

            if not success:
                print(f"\n❌ 阶段{stage['stage_id']}执行失败，流水线暂停")
                break

            if stage["stage_id"] < len(self.pipeline_stages):
                choice = input(f"\n是否继续下一阶段？(Y/n): ").strip().lower()
                if choice == "n":
                    print(f"\n⏸️ 流水线暂停，下次运行可继续")
                    break

        print(f"\n" + "="*60)
        print("🎉 小说写作流水线执行完成！")
        print("="*60)
        print(f"完成的阶段: {len(self.pipeline_state['stages_completed'])}/{len(self.pipeline_stages)}")
        print(f"输出目录: {self.pipeline_dir}")

    def continue_from_stage(self, stage_id):
        """从指定阶段继续"""
        self.pipeline_state["current_stage"] = stage_id

        for i in range(len(self.pipeline_state["stages_completed"]) - 1, -1, -1):
            if self.pipeline_state["stages_completed"][i] >= stage_id:
                self.pipeline_state["stages_completed"].pop(i)

        self.save_pipeline()
        print(f"   ✅ 已重置到阶段{stage_id}")


def main():
    print("="*60)
    print("📋 NWACS V8.0 Skill协作编排系统")
    print("="*60)
    print("\n本系统实现小说写作流水线，让多个Skill有序协作！")
    print("="*60)

    novel_name = input("\n请输入小说名称: ").strip()
    if not novel_name:
        novel_name = "测试小说"

    print("\n请选择小说类型:")
    print("   1. 玄幻（默认）")
    print("   2. 都市")
    print("   3. 言情")
    print("   4. 科幻")
    choice = input("\n请选择 (1/2/3/4): ").strip()

    genre_map = {"1": "玄幻", "2": "都市", "3": "言情", "4": "科幻"}
    genre = genre_map.get(choice, "玄幻")

    pipeline = NovelWritingPipeline(novel_name, genre)

    # 检查是否有已存在的流水线
    if pipeline.load_pipeline():
        print("\n检测到已存在的写作进度！")
        print(f"当前阶段: {pipeline.pipeline_state['current_stage']}")
        print(f"已完成: {len(pipeline.pipeline_state['stages_completed'])} 阶段")

        choice = input("\n要继续之前的进度吗？(Y/n): ").strip().lower()
        if choice == "n":
            print("\n⚠️ 将重新开始！")
            pipeline = NovelWritingPipeline(novel_name, genre)

    pipeline.display_pipeline()

    print("\n请选择:")
    print("   1. 运行完整写作流水线（推荐）")
    print("   2. 从指定阶段继续")
    print("   3. 查看已有阶段输出")
    choice = input("\n请选择 (1/2/3): ").strip()

    if choice == "1":
        pipeline.run_entire_pipeline()
    elif choice == "2":
        stage_id = int(input("\n请输入要从第几阶段开始: ").strip())
        pipeline.continue_from_stage(stage_id)
        pipeline.run_entire_pipeline()
    elif choice == "3":
        print("\n📁 阶段输出文件:")
        for stage_id in pipeline.pipeline_state["stages_completed"]:
            output_file = pipeline.pipeline_state["stage_outputs"][str(stage_id)]["output_file"]
            print(f"   阶段{stage_id}: {output_file}")
    else:
        print("\n无效选项")


if __name__ == "__main__":
    main()
