#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS AI漫剧创作模块
将小说创作与AI漫剧制作无缝衔接
"""

import sys
import os
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class AIComicDramaModule:
    """AI漫剧创作模块"""

    def __init__(self):
        self.version = "1.0"
        print("="*70)
        print(f"🎬 NWACS AI漫剧创作模块 v{self.version}")
        print("="*70)

        # 导入依赖模块
        self._import_dependencies()

    def _import_dependencies(self):
        """导入依赖模块"""
        print("\n📦 加载依赖模块...")
        try:
            from nwacs_unified_engine import NWACSUnifiedEngine
            self.unified_engine = NWACSUnifiedEngine()
            print("   ✅ 一体化引擎已加载")
        except Exception as e:
            print(f"   ⚠️ 一体化引擎加载失败: {e}")
            self.unified_engine = None

    def novel_to_comic_script(self, novel_text: str, episode_count: int = 10) -> Dict[str, Any]:
        """
        将小说文本转换为漫剧剧本
        
        Args:
            novel_text: 小说文本
            episode_count: 期望的集数
            
        Returns:
            结构化的漫剧剧本数据
        """
        print(f"\n🔄 将小说转换为 {episode_count} 集漫剧剧本...")

        # 1. 分析小说结构
        print("   1. 分析小说结构...")
        plot_points = self._analyze_novel_structure(novel_text)

        # 2. 分割为集数
        print("   2. 分割为集数...")
        episodes = self._split_into_episodes(plot_points, episode_count)

        # 3. 转换为漫剧脚本格式
        print("   3. 转换为漫剧脚本格式...")
        comic_script = self._convert_to_comic_format(episodes)

        return comic_script

    def _analyze_novel_structure(self, text: str) -> List[Dict]:
        """分析小说结构，提取关键情节点"""
        # 简化版分析：提取段落作为情节点
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        plot_points = []

        for i, paragraph in enumerate(paragraphs[:20], 1):
            plot_points.append({
                "id": i,
                "content": paragraph[:200] + "..." if len(paragraph) > 200 else paragraph,
                "type": self._detect_scene_type(paragraph)
            })

        return plot_points

    def _detect_scene_type(self, text: str) -> str:
        """检测场景类型"""
        text_lower = text.lower()
        if any(word in text_lower for word in ['战斗', '攻击', '对决', '打']):
            return "action"
        elif any(word in text_lower for word in ['说', '问', '答', '对话']):
            return "dialogue"
        elif any(word in text_lower for word in ['想', '回忆', '内心']):
            return "internal"
        else:
            return "narrative"

    def _split_into_episodes(self, plot_points: List[Dict], episode_count: int) -> List[Dict]:
        """将情节点分割为集数"""
        episodes = []
        points_per_episode = max(1, len(plot_points) // episode_count)

        for i in range(episode_count):
            start_idx = i * points_per_episode
            end_idx = min((i + 1) * points_per_episode, len(plot_points))
            
            if start_idx >= len(plot_points):
                break

            episodes.append({
                "episode": i + 1,
                "title": f"第{i+1}章",
                "plot_points": plot_points[start_idx:end_idx]
            })

        return episodes

    def _convert_to_comic_format(self, episodes: List[Dict]) -> Dict[str, Any]:
        """转换为结构化漫剧脚本格式"""
        comic_script = {
            "version": "1.0",
            "title": "AI漫剧剧本",
            "total_episodes": len(episodes),
            "created_at": datetime.now().isoformat(),
            "episodes": []
        }

        for episode in episodes:
            scenes = []
            for point in episode["plot_points"]:
                scene = self._create_scene(point, episode["episode"])
                scenes.append(scene)

            comic_script["episodes"].append({
                "episode": episode["episode"],
                "title": episode["title"],
                "scenes": scenes,
                "duration": len(scenes) * 4  # 每场景约4秒
            })

        return comic_script

    def _create_scene(self, plot_point: Dict, episode_num: int) -> Dict[str, Any]:
        """创建单个场景"""
        content = plot_point["content"]
        
        # 根据场景类型选择镜头
        if plot_point["type"] == "action":
            camera = "中景"
            mood = "紧张"
        elif plot_point["type"] == "dialogue":
            camera = "近景"
            mood = "对话"
        elif plot_point["type"] == "internal":
            camera = "特写"
            mood = "沉思"
        else:
            camera = "全景"
            mood = "叙事"

        return {
            "scene_id": f"EP{episode_num}-{plot_point['id']}",
            "location": self._extract_location(content),
            "characters": self._extract_characters(content),
            "action": content[:100],
            "dialogue": "",
            "camera": camera,
            "mood": mood,
            "duration": 4,
            "shot_type": self._get_shot_type(plot_point["type"])
        }

    def _extract_location(self, text: str) -> str:
        """从文本中提取地点"""
        locations = ['房间', '大厅', '街道', '森林', '山洞', '宫殿', '战场', '屋顶']
        for loc in locations:
            if loc in text:
                return loc
        return "未知地点"

    def _extract_characters(self, text: str) -> List[str]:
        """从文本中提取角色（简化版）"""
        # 实际应用中需要NLP分析
        return ["主角"]

    def _get_shot_type(self, scene_type: str) -> str:
        """获取镜头类型"""
        shot_types = {
            "action": "动作镜头",
            "dialogue": "对话镜头",
            "internal": "内心独白",
            "narrative": "场景交代"
        }
        return shot_types.get(scene_type, "场景交代")

    def generate_prompts_for_ai_tools(self, scene: Dict) -> Dict[str, str]:
        """
        生成AI绘图工具的提示词
        
        Args:
            scene: 场景数据
            
        Returns:
            包含各种格式提示词的字典
        """
        base_prompt = f"""
二次元漫剧风格，{scene['location']}，{scene['action']}，
{scene['camera']}，{scene['mood']}氛围，高清画质，4K，
角色一致性，无AI畸形，动漫风格
"""

        return {
            "midjourney": base_prompt.strip(),
            "stable_diffusion": base_prompt.strip(),
            "jimeng": f"角色参考图@, {base_prompt.strip()}",
            "description": scene['action']
        }

    def export_to_json(self, script: Dict, filename: str) -> bool:
        """导出剧本为JSON格式"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(script, f, ensure_ascii=False, indent=2)
            print(f"✅ 剧本已导出到 {filename}")
            return True
        except Exception as e:
            print(f"❌ 导出失败: {e}")
            return False

    def export_to_script_format(self, script: Dict, filename: str) -> bool:
        """导出为可读脚本格式"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"# AI漫剧剧本 - {script['title']}\n")
                f.write(f"# 总集数: {script['total_episodes']}\n")
                f.write(f"# 创建时间: {script['created_at']}\n")
                f.write("="*60 + "\n\n")

                for episode in script['episodes']:
                    f.write(f"## 第{episode['episode']}集: {episode['title']}\n")
                    f.write(f"### 时长: {episode['duration']}秒\n\n")

                    for scene in episode['scenes']:
                        f.write(f"【{scene['scene_id']}】\n")
                        f.write(f"  景别: {scene['camera']}\n")
                        f.write(f"  地点: {scene['location']}\n")
                        f.write(f"  情绪: {scene['mood']}\n")
                        f.write(f"  时长: {scene['duration']}秒\n")
                        f.write(f"  动作: {scene['action']}\n")
                        f.write(f"  镜头: {scene['shot_type']}\n")
                        if scene['dialogue']:
                            f.write(f"  台词: {scene['dialogue']}\n")
                        f.write("\n")

            print(f"✅ 剧本已导出到 {filename}")
            return True
        except Exception as e:
            print(f"❌ 导出失败: {e}")
            return False

    def generate_full_workflow(self, novel_text: str, output_dir: str = "comic_drama") -> Dict[str, Any]:
        """
        生成完整的漫剧制作工作流
        
        Args:
            novel_text: 小说文本
            output_dir: 输出目录
            
        Returns:
            工作流配置
        """
        os.makedirs(output_dir, exist_ok=True)

        # 1. 生成剧本
        script = self.novel_to_comic_script(novel_text, episode_count=5)

        # 2. 导出剧本
        self.export_to_json(script, os.path.join(output_dir, "comic_script.json"))
        self.export_to_script_format(script, os.path.join(output_dir, "comic_script.txt"))

        # 3. 生成提示词文件
        prompts = self._generate_all_prompts(script)
        self.export_to_json(prompts, os.path.join(output_dir, "prompts.json"))

        # 4. 生成制作指南
        guide = self._generate_production_guide(script)
        with open(os.path.join(output_dir, "production_guide.md"), 'w', encoding='utf-8') as f:
            f.write(guide)

        print(f"\n🎉 漫剧制作工作流已生成！输出目录: {output_dir}")

        return {
            "status": "success",
            "script": script,
            "output_dir": output_dir,
            "files": [
                "comic_script.json",
                "comic_script.txt",
                "prompts.json",
                "production_guide.md"
            ]
        }

    def _generate_all_prompts(self, script: Dict) -> Dict[str, Any]:
        """生成所有场景的提示词"""
        prompts = {}
        for episode in script['episodes']:
            for scene in episode['scenes']:
                prompts[scene['scene_id']] = self.generate_prompts_for_ai_tools(scene)
        return prompts

    def _generate_production_guide(self, script: Dict) -> str:
        """生成制作指南"""
        guide = f"""
# AI漫剧制作指南

## 项目信息
- 标题: {script['title']}
- 总集数: {script['total_episodes']}
- 创建时间: {script['created_at']}

## 制作流程

### 第一步: 角色设计
1. 使用 prompts.json 中的提示词生成角色参考图
2. 训练专属LoRA模型（可选）
3. 保存角色基准图用于后续生成

### 第二步: 分镜画面生成
1. 使用 prompts.json 中各场景的提示词
2. 推荐工具: 即梦AI / Midjourney / Stable Diffusion
3. 确保角色一致性

### 第三步: 图生视频
1. 使用即梦AI / 可灵AI / Runway
2. 每段控制在3-10秒
3. 添加运镜效果

### 第四步: 配音剪辑
1. 使用剪映AI配音
2. 添加字幕和BGM
3. 调整节奏

## 每集概览

"""
        for episode in script['episodes']:
            guide += f"""### 第{episode['episode']}集: {episode['title']}
- 时长: {episode['duration']}秒
- 场景数: {len(episode['scenes'])}
\n"""

        guide += """
## 工具推荐

| 环节 | 推荐工具 |
|------|---------|
| 剧本生成 | NWACS + DeepSeek |
| 角色设计 | 即梦AI / Midjourney |
| 分镜生成 | 即梦AI / ComfyUI |
| 图生视频 | 即梦AI / 可灵AI |
| 配音剪辑 | 剪映 / CapCut |

## 注意事项
1. 保持角色一致性（使用参考图锁定）
2. 控制每集时长在1-3分钟
3. 注意版权问题
"""
        return guide


def main():
    """演示AI漫剧创作模块"""
    print("="*70)
    print("🎬 NWACS AI漫剧创作模块演示")
    print("="*70)

    # 创建模块
    comic_module = AIComicDramaModule()

    # 示例小说文本
    sample_novel = """
夜色降临，林川站在屋顶，看着远处的城市灯火。

他是一名普通的大学生，但最近总做奇怪的梦。梦中，他站在一片废墟之中，手里握着一把发光的剑。

"你终于来了。"一个神秘的声音在耳边响起。

林川猛地惊醒，额头上满是冷汗。窗外，月光如水，洒在他的脸上。

他不知道，命运的齿轮已经开始转动。在这个看似平凡的世界背后，隐藏着一个不为人知的秘密。

第二天，林川像往常一样去上学。但他发现，周围的一切似乎都变了。同学的眼神变得奇怪，老师的讲课内容也变得晦涩难懂。

就在他感到困惑的时候，一个女孩走到他面前。

"你能看见那些东西，对吗？"女孩问道。

林川愣住了。他不知道该如何回答。

"跟我来，"女孩说，"我带你去见一个人。"
"""

    print("\n📝 示例小说文本已准备好")
    print(f"   字数: {len(sample_novel)}")

    # 生成漫剧工作流
    result = comic_module.generate_full_workflow(sample_novel)

    if result['status'] == 'success':
        print("\n✅ 漫剧工作流生成成功！")
        print(f"📁 输出目录: {result['output_dir']}")
        print(f"📄 生成文件: {', '.join(result['files'])}")

    print("\n" + "="*70)
    print("🎬 演示完成！")
    print("="*70)


if __name__ == "__main__":
    main()
