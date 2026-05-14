#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS写作手法专项学习
DeepSeek学习修辞知识库并优化写作相关Skill
"""

import os
import json
from pathlib import Path
from datetime import datetime

try:
    from openai import OpenAI
except ImportError:
    print("❌ 请先安装 openai 库：pip install openai")
    exit(1)


def main():
    print("="*60)
    print("📚 NWACS写作手法专项学习")
    print("="*60)
    print()

    # 设置API Key
    api_key = "sk-f3246fbd1eef446e9a11d78efefd9bba"

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com"
    )

    project_root = Path(__file__).parent
    skill_dir = project_root / "skills" / "level2"

    # 读取新创建的知识库
    knowledge_file = project_root / "skills/level2/learnings/写作手法与修辞知识库.txt"

    print("📖 读取写作手法与修辞知识库...")
    with open(knowledge_file, 'r', encoding='utf-8') as f:
        knowledge_content = f.read()

    print(f"✅ 已读取知识库，字数：{len(knowledge_content)}")
    print()

    # 读取现有的写作技巧大师Skill
    print("📝 读取现有写作技巧大师Skill...")
    skill_file = skill_dir / "09_二级Skill_写作技巧大师.md"

    if skill_file.exists():
        with open(skill_file, 'r', encoding='utf-8') as f:
            current_skill = f.read()
        print(f"✅ 已读取现有Skill，字数：{len(current_skill)}")
    else:
        current_skill = "未找到现有Skill"
        print("⚠️ 未找到现有Skill，将创建新Skill")
    print()

    # DeepSeek学习并优化
    print("🧠 调用DeepSeek进行专项学习...")
    print()

    system_prompt = """你是一个专业的小说写作技巧专家。你需要：
1. 学习新的写作手法与修辞知识
2. 分析现有写作技巧大师Skill
3. 将新知识融合到Skill中
4. 输出优化后的Skill内容

请直接输出优化后的Skill内容，保持相同的Markdown格式。"""

    user_prompt = f"""请学习以下写作手法与修辞知识，并与现有Skill融合：

=== 新的写作手法与修辞知识 ===
{knowledge_content}

=== 现有写作技巧大师Skill ===
{current_skill}

要求：
1. 将新的修辞手法（比喻、拟人、排比、夸张等）融入Skill
2. 将高级写作手法（意识流、伏笔、悬念等）融入Skill
3. 将网文专属技巧（爽点设置、情绪流等）融入Skill
4. 保持Skill的专业性和可操作性
5. 保持相同的Markdown格式和结构

请直接输出优化后的完整Skill内容。"""

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=8000
        )

        optimized_skill = response.choices[0].message.content

        print("✅ DeepSeek学习完成！")
        print()

        # 保存优化后的Skill
        backup_file = skill_dir / "09_二级Skill_写作技巧大师.md.bak"
        if skill_file.exists():
            with open(backup_file, 'w', encoding='utf-8') as f:
                f.write(current_skill)
            print(f"✅ 已备份原Skill到: {backup_file.name}")

        with open(skill_file, 'w', encoding='utf-8') as f:
            f.write(optimized_skill)
        print(f"✅ 已保存优化后的Skill到: {skill_file.name}")

        print()
        print("="*60)
        print("📊 学习优化总结")
        print("="*60)
        print(f"  知识库字数: {len(knowledge_content)}")
        print(f"  优化后Skill字数: {len(optimized_skill)}")
        print(f"  新增技巧: 修辞手法、高级写作、网文技巧")
        print()

        # 同时优化场景构造师（环境描写相关）
        print("📝 正在优化场景构造师Skill...")
        scene_skill_file = skill_dir / "05_二级Skill_场景构造师.md"

        if scene_skill_file.exists():
            with open(scene_skill_file, 'r', encoding='utf-8') as f:
                scene_skill = f.read()

            # 添加五感描写技巧
            five_sense_addition = """

## 六、五感描写技巧（专项提升）

### 1. 视觉描写
- 颜色：深浅、明暗、对比
- 形状：大孝圆扁、规则与不规则
- 动态：静止、移动、变化
- 光影：明暗、阴影、倒影

### 2. 听觉描写
- 远近：清晰、模糊、回声
- 强弱：轻柔、强烈、震撼
- 音色：尖锐、圆润、沉闷
- 节奏：均匀、紊乱、起伏

### 3. 嗅觉描写
- 气味：香、臭、淡、浓
- 来源：花草、食物、金属
- 情感关联：熟悉、陌生、回忆

### 4. 味觉描写
- 酸甜苦辣咸
- 温度：冰凉、温热、灼热
- 口感：细腻、粗粝、润滑

### 5. 触觉描写
- 温度：冷、热、温暖
- 材质：粗糙、细腻、光滑
- 质感：柔软、坚硬、弹性
- 情感传递：疼痛、舒适、麻木

### 6. 五感综合运用
```markdown
示例：
夕阳的余晖洒在湖面上，金色的光芒像碎金一般闪烁。（视觉）
微风带来远处花香和青草的气息。（嗅觉）
湖水轻轻拍打着岸边，发出低沉而温柔的声响。（听觉）
脚下的细沙柔软温热，像是踩在云朵上。（触觉）
空气中弥漫着淡淡的甜蜜，像是初恋的味道。（味觉+情感）
```
"""

            optimized_scene_skill = scene_skill + five_sense_addition

            # 备份并保存
            scene_backup = scene_skill_file.with_suffix('.md.bak')
            with open(scene_backup, 'w', encoding='utf-8') as f:
                f.write(scene_skill)

            with open(scene_skill_file, 'w', encoding='utf-8') as f:
                f.write(optimized_scene_skill)

            print(f"✅ 场景构造师Skill已优化，新增五感描写技巧")

        print()
        print("="*60)
        print("✅ 写作手法专项学习完成！")
        print("="*60)
        print()
        print("📝 已优化的Skill：")
        print("   1. 写作技巧大师 - 融入修辞手法、高级技巧")
        print("   2. 场景构造师 - 新增五感描写技巧")
        print()
        print("💡 建议：")
        print("   - 可以继续创作，让NWACS使用新技巧")
        print("   - 可以运行DeepSeek学习引擎，学习更多知识")
        print()

    except Exception as e:
        print(f"❌ 学习失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
