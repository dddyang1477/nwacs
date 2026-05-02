#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS核心创作引擎
集成所有三级Skill，支持各种小说类型创作
"""

import os
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

try:
    from openai import OpenAI
except ImportError:
    print("❌ 请先安装 openai 库：pip install openai")
    exit(1)


class NWACSNovelEngine:
    """NWACS小说创作核心引擎"""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise ValueError("❌ 请设置 DEEPSEEK_API_KEY")

        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.deepseek.com"
        )

        self.project_root = Path(__file__).parent
        self.skills_dir = self.project_root / "skills"
        self.knowledge_dir = self.skills_dir / "level2" / "learnings"

        print("🚀 NWACS v7.0 核心创作引擎启动")
        print("-" * 60)

        # 加载系统信息
        self.skill_index = self._load_skill_index()
        self.knowledge_index = self._load_knowledge_index()

    def _load_skill_index(self) -> Dict:
        """加载Skill索引"""
        index_file = self.skills_dir / "system" / "Skill完整索引.md"
        if index_file.exists():
            return {"loaded": True, "path": str(index_file)}
        return {"loaded": False}

    def _load_knowledge_index(self) -> Dict:
        """加载知识库索引"""
        index_file = self.knowledge_dir / "00_知识库共享中心索引.txt"
        if index_file.exists():
            return {"loaded": True, "path": str(index_file)}
        return {"loaded": False}

    def get_supported_novel_types(self) -> List[Dict]:
        """获取支持的小说类型"""
        return [
            {"id": "xuanhuan", "name": "玄幻仙侠", "icon": "🐉", "description": "修仙、玄幻、仙侠"},
            {"id": "dushi", "name": "都市言情", "icon": "🏙️", "description": "都市、言情、职场"},
            {"id": "xuanyi", "name": "悬疑推理", "icon": "🔍", "description": "悬疑、推理、侦探"},
            {"id": "kehuan", "name": "科幻未来", "icon": "🚀", "description": "科幻、未来、末世"},
            {"id": "lishi", "name": "历史穿越", "icon": "📜", "description": "历史、穿越、架空"},
            {"id": "kongbu", "name": "恐怖惊悚", "icon": "👻", "description": "恐怖、惊悚、灵异"},
            {"id": "youxi", "name": "游戏竞技", "icon": "🎮", "description": "游戏、竞技、电竞"},
            {"id": "nvpin", "name": "女频系列", "icon": "💖", "description": "总裁、年代、马甲、萌宝"}
        ]

    def get_novel_type_skill(self, novel_type: str) -> str:
        """获取小说类型对应的Skill文件"""
        skill_files = {
            "xuanhuan": "skills/level3/13_三级Skill_玄幻仙侠.md",
            "dushi": "skills/level3/14_三级Skill_都市言情.md",
            "xuanyi": "skills/level3/15_三级Skill_悬疑推理.md",
            "kehuan": "skills/level3/16_三级Skill_科幻未来.md",
            "lishi": "skills/level3/17_三级Skill_历史穿越.md",
            "kongbu": "skills/level3/18_三级Skill_恐怖惊悚.md",
            "youxi": "skills/level3/19_三级Skill_游戏竞技.md",
            "nvpin": "skills/level3/37_三级Skill_女频总裁文设计师.md"
        }
        return skill_files.get(novel_type, "skills/level3/12_三级Skill_小说类型基类.md")

    def load_skill_content(self, skill_path: str) -> str:
        """加载Skill内容"""
        full_path = self.project_root / skill_path
        if full_path.exists():
            with open(full_path, 'r', encoding='utf-8') as f:
                return f.read(5000)  # 限制长度
        return f"⚠️ 未找到Skill: {skill_path}"

    def generate_chapter(self, 
                        novel_type: str,
                        prompt: str,
                        chapter_title: str = "第一章",
                        word_count: int = 3000) -> Dict:
        """生成小说章节"""
        print(f"📝 开始生成 [{chapter_title}]")
        print(f"   类型: {novel_type}")
        print(f"   目标字数: {word_count}")

        # 加载类型Skill
        skill_file = self.get_novel_type_skill(novel_type)
        skill_content = self.load_skill_content(skill_file)

        # 构建完整提示
        system_prompt = f"""你是NWACS v7.0专业小说创作助手。
请以流畅、生动、富有画面感的文笔创作小说。

以下是该类型的专业Skill知识：
{skill_content}

创作要求：
1. 遵循"黄金三秒"法则，开篇立即抓住读者
2. 每1000字左右设置一个小爽点或悬念
3. 人物对话自然，符合性格设定
4. 环境描写细腻，烘托氛围
5. 避免AI腔，语言风格自然
6. 字数控制在{word_count}左右"""

        user_prompt = f"""请创作小说的 {chapter_title}

用户需求：
{prompt}

请直接生成小说正文，格式清晰，段落分明。"""

        try:
            start_time = time.time()
            
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=4000
            )

            content = response.choices[0].message.content
            elapsed = round(time.time() - start_time, 2)

            print(f"✅ 章节生成完成，耗时 {elapsed} 秒")
            
            # 估算字数
            estimated_words = len(content.replace(" ", ""))
            
            return {
                "success": True,
                "title": chapter_title,
                "content": content,
                "word_count": estimated_words,
                "novel_type": novel_type,
                "elapsed_seconds": elapsed
            }

        except Exception as e:
            print(f"❌ 生成失败: {e}")
            return {"success": False, "error": str(e)}

    def interactive_creator(self):
        """交互式创作界面"""
        print("=" * 60)
        print("📚 NWACS v7.0 小说创作引擎")
        print("=" * 60)
        print()

        # 选择小说类型
        print("请选择小说类型：")
        novel_types = self.get_supported_novel_types()
        
        for i, nt in enumerate(novel_types, 1):
            print(f"{i}. {nt['icon']} {nt['name']} - {nt['description']}")
        
        choice = input("\n请输入选项编号 (1-8): ").strip()
        
        try:
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(novel_types):
                selected_type = novel_types[choice_idx]
                novel_type_id = selected_type['id']
            else:
                novel_type_id = "xuanhuan"
        except:
            novel_type_id = "xuanhuan"
        
        # 输入创作要求
        print("\n" + "=" * 60)
        print("📝 请输入创作要求")
        print("=" * 60)
        print("（例如：写一个关于废柴逆袭的玄幻开篇，主角从悬崖掉落获得奇遇）")
        
        prompt = input("\n请输入创作需求: ").strip()
        chapter_title = input("请输入章节标题（默认：第一章）: ").strip() or "第一章"
        
        try:
            word_count_str = input("请输入目标字数（默认：3000）: ").strip() or "3000"
            word_count = int(word_count_str)
        except:
            word_count = 3000

        # 生成章节
        print("\n" + "=" * 60)
        print("🎨 正在生成章节...")
        print("=" * 60)
        
        result = self.generate_chapter(
            novel_type=novel_type_id,
            prompt=prompt,
            chapter_title=chapter_title,
            word_count=word_count
        )

        if result['success']:
            # 显示结果
            print("\n" + "=" * 60)
            print(f"📖 {result['title']}")
            print("=" * 60)
            print()
            print(result['content'])
            print()
            print("=" * 60)
            print(f"📊 字数: {result['word_count']} 字")
            print(f"⏱️ 耗时: {result['elapsed_seconds']} 秒")
            print("=" * 60)

            # 保存文件
            save = input("\n是否保存到文件？(y/n): ").lower().strip()
            if save == 'y':
                self.save_to_file(result)
        else:
            print(f"\n❌ 生成失败: {result['error']}")

    def save_to_file(self, result: Dict):
        """保存到文件"""
        output_dir = self.project_root / "output"
        output_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{result['title']}_{timestamp}.md"
        filepath = output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# {result['title']}\n\n")
            f.write(f"**类型**: {result['novel_type']}\n")
            f.write(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**字数**: {result['word_count']} 字\n\n")
            f.write("---\n\n")
            f.write(result['content'])
        
        print(f"✅ 已保存到: {filepath}")


def main():
    parser = argparse.ArgumentParser(description="NWACS v7.0 核心创作引擎")
    parser.add_argument("--api-key", type=str, default=None, help="DeepSeek API密钥")
    parser.add_argument("--interactive", action="store_true", help="交互式创作模式")
    
    args = parser.parse_args()

    try:
        engine = NWACSNovelEngine(api_key=args.api_key)
        
        if args.interactive:
            engine.interactive_creator()
        else:
            print("提示：使用 --interactive 参数启动交互式创作")
            engine.interactive_creator()

    except Exception as e:
        print(f"❌ 启动失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    import argparse
    main()
