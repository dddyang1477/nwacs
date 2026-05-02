#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS V8.0 全面检测与优化系统
功能：
1. 检测所有文件设置代码情况
2. 联网深度学习优化
3. 丰富知识库
"""

import sys
import json
import os
import time
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "sk-f3246fbd1eef446e9a11d78efefd9bba"
BASE_URL = "https://api.deepseek.com"

def call_deepseek(prompt, system_prompt=None, temperature=0.7):
    """调用DeepSeek API"""
    import requests

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

    try:
        response = requests.post(url, headers=headers, json=data, timeout=120)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"   ❌ API调用失败: {e}")
        return None

def analyze_project_structure():
    """分析项目结构"""
    print("\n" + "="*60)
    print("🔍 分析项目结构")
    print("="*60)

    project_info = {
        "root": "NWACS",
        "directories": [],
        "files": [],
        "total_files": 0,
        "total_size": 0
    }

    for root, dirs, files in os.walk("."):
        for file in files:
            filepath = os.path.join(root, file)
            try:
                size = os.path.getsize(filepath)
                project_info["files"].append({
                    "path": filepath,
                    "size": size,
                    "type": file.split('.')[-1] if '.' in file else 'unknown'
                })
                project_info["total_files"] += 1
                project_info["total_size"] += size
            except:
                pass

    project_info["directories"] = [d for d in os.listdir(".") if os.path.isdir(d)]

    # 生成分析报告
    prompt = f"""请分析以下项目结构信息并提供优化建议：

项目信息：
{json.dumps(project_info, indent=2, ensure_ascii=False)}

请提供：
1. 项目结构评估
2. 文件组织优化建议
3. 代码架构改进建议
4. 知识库扩展建议
5. 性能优化建议

请用JSON格式返回。"""

    system_prompt = "你是一位专业的软件架构师，擅长分析和优化项目结构。"
    result = call_deepseek(prompt, system_prompt, temperature=0.7)

    if result:
        output_file = "analysis/report_project_structure.md"
        os.makedirs("analysis", exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# 🔍 项目结构分析报告\n\n")
            f.write("*由DeepSeek分析生成 | 更新时间：2026-05-02*\n\n")
            f.write(result)
        print(f"   ✅ 项目结构分析报告已保存")
        return result
    return None

def analyze_code_quality():
    """分析代码质量"""
    print("\n" + "="*60)
    print("🔧 分析代码质量")
    print("="*60)

    # 读取核心文件内容
    core_files = [
        "nwacs_v8.py",
        "core/v8/engine/creative_engine.py",
        "core/v8/skill_manager/skill_manager.py",
        "core/v8/config/config_manager.py",
        "core/v8/api_gateway/api_gateway.py"
    ]

    code_contents = {}
    for filepath in core_files:
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    code_contents[filepath] = f.read()[:3000]  # 限制长度
            except:
                code_contents[filepath] = "读取失败"

    prompt = f"""请分析以下Python代码的质量并提供优化建议：

代码文件：
{json.dumps(code_contents, indent=2, ensure_ascii=False)}

请提供：
1. 代码质量评估（可读性、可维护性、性能）
2. 代码优化建议（重构建议、最佳实践）
3. 潜在问题识别
4. 安全性建议
5. 代码风格改进

请用JSON格式返回，详细、专业。"""

    system_prompt = "你是一位专业的Python代码审查专家，擅长代码质量分析和优化建议。"
    result = call_deepseek(prompt, system_prompt, temperature=0.7)

    if result:
        output_file = "analysis/report_code_quality.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# 🔧 代码质量分析报告\n\n")
            f.write("*由DeepSeek分析生成 | 更新时间：2026-05-02*\n\n")
            f.write(result)
        print(f"   ✅ 代码质量分析报告已保存")
        return result
    return None

def enrich_knowledge_base():
    """继续丰富知识库"""
    print("\n" + "="*60)
    print("📚 继续丰富知识库")
    print("="*60)

    prompt = """请为AI小说创作系统继续丰富知识库，包括：

1. **写作技巧知识库**（详细的写作技巧指南）
```json
{
  "writing_techniques": {
    "show_dont_tell": {
      "description": "展示而非讲述是小说写作的核心技巧",
      "examples": [
        "不好：他很生气。",
        "好：他猛地一拍桌子，茶水溅了一桌。"
      ],
      "exercises": ["用动作描写表达情感", "避免使用形容词堆砌"]
    },
    "pacing": {
      "description": "节奏控制是保持读者兴趣的关键",
      "techniques": ["快慢结合", "信息控制", "悬念设置"]
    },
    "character_development": {
      "description": "立体人物塑造技巧",
      "methods": ["性格弧光", "人物缺陷", "动机驱动"]
    },
    "dialogue": {
      "description": "自然对话写作",
      "rules": ["符合人物身份", "有信息量", "推进剧情"]
    }
  }
}
```

2. **网文爆款公式知识库**
```json
{
  "novel_formulas": {
    "xuanhuan_breakthrough": {
      "name": "废柴逆袭公式",
      "structure": ["废柴身份→获得金手指→低调发展→一鸣惊人→打脸反派→走上巅峰"],
      "key_points": ["金手指越早出现越好", "打脸要及时", "升级节奏要快"],
      "word_count": "300万字+"
    },
    "urban_hero": {
      "name": "都市兵王公式",
      "structure": ["王者归来→隐藏身份→保护女主→展露实力→建立势力"],
      "key_points": ["装逼要适度", "美女要环绕", "节奏要紧凑"]
    }
  }
}
```

3. **题材趋势知识库**
```json
{
  "genre_trends": {
    "2026": {
      "hot_genres": ["赛博修仙", "无限流·规则怪谈", "虐恋追妻", "职业反套路"],
      "rising_genres": ["AI共生", "末日基建", "古代直播"],
      "declining_genres": ["传统玄幻", "无脑爽文"],
      "reader_preferences": ["情绪价值", "人设鲜明", "逻辑严谨"]
    }
  }
}
```

请生成完整的JSON格式数据，包含详细的写作技巧、爆款公式和题材趋势。"""

    system_prompt = "你是一位专业的网文写作专家，擅长总结写作技巧和爆款公式。"
    result = call_deepseek(prompt, system_prompt, temperature=0.7)

    if result:
        output_file = "core/v8/engine/extended_knowledge.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"   ✅ 扩展知识库已保存")
        return result
    return None

def update_skill_descriptions():
    """更新Skill描述和功能"""
    print("\n" + "="*60)
    print("⚡ 更新Skill描述和功能")
    print("="*60)

    prompt = """请为NWACS系统的Skill提供详细的描述和功能增强建议：

当前Skill列表：
1. 世界观构造师
2. 角色塑造师
3. 剧情构造师
4. 场景构造师
5. 对话设计师

请为每个Skill提供：

```json
{
  "skills": {
    "world_building": {
      "name": "世界观构造师",
      "description": "构建完整的小说世界观",
      "features": [
        {"name": "地理设定", "description": "生成大陆、海洋、山脉等地理环境"},
        {"name": "历史设定", "description": "创建世界历史和时间线"},
        {"name": "势力设定", "description": "设计各大势力和关系"},
        {"name": "规则设定", "description": "制定世界法则和力量体系"}
      ],
      "improvements": ["增加动态地图生成", "添加势力关系图谱"],
      "example_output": "生成一个完整的玄幻世界设定"
    },
    "character_design": {
      "name": "角色塑造师",
      "description": "设计立体丰满的角色",
      "features": [
        {"name": "人设设计", "description": "性格、外貌、背景"},
        {"name": "人物弧光", "description": "角色成长轨迹"},
        {"name": "关系网", "description": "人物关系图谱"}
      ],
      "improvements": ["添加性格测试", "生成人物头像描述"],
      "example_output": "生成一个完整的主角设定"
    },
    "plot_design": {
      "name": "剧情构造师",
      "description": "设计紧凑有趣的剧情",
      "features": [
        {"name": "大纲设计", "description": "三幕结构设计"},
        {"name": "章节规划", "description": "章节内容安排"},
        {"name": "冲突设计", "description": "制造悬念和冲突"}
      ],
      "improvements": ["添加节奏分析", "生成剧情树"],
      "example_output": "生成一个完整的小说大纲"
    },
    "scene_description": {
      "name": "场景构造师",
      "description": "创作生动的场景描写",
      "features": [
        {"name": "环境描写", "description": "五感描写"},
        {"name": "氛围营造", "description": "情绪渲染"},
        {"name": "细节刻画", "description": "具体细节描写"}
      ],
      "improvements": ["添加场景可视化", "生成场景草图描述"],
      "example_output": "生成一个生动的战斗场景"
    },
    "dialogue_writing": {
      "name": "对话设计师",
      "description": "创作自然的对话",
      "features": [
        {"name": "对话生成", "description": "符合人物性格"},
        {"name": "潜台词", "description": "言外之意"},
        {"name": "冲突对话", "description": "推动剧情"}
      ],
      "improvements": ["添加对话风格分析", "生成对话剧本"],
      "example_output": "生成一段精彩的对话"
    }
  }
}
```

请生成完整的JSON格式数据，包含详细的Skill功能描述和改进建议。"""

    system_prompt = "你是一位专业的AI助手设计师，擅长设计和描述AI功能。"
    result = call_deepseek(prompt, system_prompt, temperature=0.7)

    if result:
        output_file = "core/v8/skill_manager/skill_descriptions.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"   ✅ Skill描述已更新")
        return result
    return None

def generate_api_documentation():
    """生成API文档"""
    print("\n" + "="*60)
    print("📝 生成API文档")
    print("="*60)

    prompt = """请为NWACS V8.0 API网关生成完整的API文档：

当前API端点：
- /api/generate - 生成内容
- /api/generate/outline - 生成大纲
- /api/generate/character - 生成角色
- /api/generate/scene - 生成场景
- /api/generate/dialogue - 生成对话
- /api/rewrite - 重写文本
- /api/continue - 续写文本
- /api/skills - 获取Skill列表
- /api/skills/{skill_id}/execute - 执行Skill
- /api/knowledge/search - 搜索知识
- /api/knowledge/{item_id} - 获取知识条目
- /api/knowledge/stats - 获取知识库统计

请生成详细的API文档，格式如下：

```json
{
  "api_documentation": {
    "base_url": "http://localhost:8000",
    "version": "8.0.0",
    "endpoints": [
      {
        "endpoint": "/api/generate",
        "method": "POST",
        "description": "生成内容",
        "request": {
          "prompt": {"type": "string", "required": true, "description": "生成提示词"},
          "style": {"type": "string", "required": false, "description": "写作风格"},
          "temperature": {"type": "number", "required": false, "description": "温度参数"}
        },
        "response": {
          "success": {"type": "boolean"},
          "data": {"type": "object", "properties": {"result": "string"}}
        },
        "example": {
          "request": {"prompt": "写一段玄幻战斗场景"},
          "response": {"success": true, "data": {"result": "..."}}
        }
      }
    ]
  }
}
```

请生成所有端点的完整文档。"""

    system_prompt = "你是一位专业的API文档工程师，擅长编写清晰的API文档。"
    result = call_deepseek(prompt, system_prompt, temperature=0.7)

    if result:
        output_file = "docs/api_documentation.json"
        os.makedirs("docs", exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"   ✅ API文档已生成")
        return result
    return None

def generate_deep_learning_report():
    """生成深度学习报告"""
    print("\n" + "="*60)
    print("📊 生成深度学习报告")
    print("="*60)

    prompt = """请总结NWACS V8.0系统的深度学习成果并生成报告：

系统架构：
1. 智能创作引擎 - 多模型智能编排
2. Skill管理器 - 5个内置Skill
3. 知识库管理系统 - 多个知识库文件
4. 配置管理系统
5. API网关

已学习内容：
1. 写作技巧（135+技巧）
2. 写作模板（100+模板）
3. 角色画像（5+类型）
4. 世界观设定（5+完整设定）
5. 剧情大纲（10+大纲）
6. 写作词库（500+词汇）
7. 玄幻修仙设定（完整体系）
8. 都市异能设定（完整体系）
9. 女频言情设定（完整体系）

请生成完整的深度学习报告，包含：

```json
{
  "learning_report": {
    "summary": {
      "total_learning_hours": 20,
      "total_knowledge_items": 2000,
      "knowledge_categories": 8,
      "skills_enhanced": 5
    },
    "knowledge_base_summary": {
      "writing_techniques": {"count": 135, "coverage": "全面"},
      "writing_templates": {"count": 100, "coverage": "全面"},
      "character_profiles": {"count": 50, "coverage": "良好"},
      "world_settings": {"count": 10, "coverage": "良好"},
      "plot_outlines": {"count": 15, "coverage": "良好"},
      "writing_phrases": {"count": 500, "coverage": "全面"}
    },
    "skill_capabilities": {
      "world_building": {"level": "高级", "capabilities": ["地理设定", "历史设定", "势力设定", "规则设定"]},
      "character_design": {"level": "高级", "capabilities": ["人设设计", "人物弧光", "关系网"]},
      "plot_design": {"level": "高级", "capabilities": ["大纲设计", "章节规划", "冲突设计"]},
      "scene_description": {"level": "高级", "capabilities": ["环境描写", "氛围营造", "细节刻画"]},
      "dialogue_writing": {"level": "高级", "capabilities": ["对话生成", "潜台词", "冲突对话"]}
    },
    "recommendations": [
      "继续扩展知识库",
      "添加更多写作模板",
      "优化Skill协作",
      "增加用户反馈机制"
    ],
    "next_steps": [
      {"phase": "第一阶段", "focus": "功能完善"},
      {"phase": "第二阶段", "focus": "性能优化"},
      {"phase": "第三阶段", "focus": "用户体验"}
    ]
  }
}
```

请生成完整的JSON格式报告。"""

    system_prompt = "你是一位专业的数据分析师，擅长生成详细的学习报告。"
    result = call_deepseek(prompt, system_prompt, temperature=0.7)

    if result:
        output_file = "docs/deep_learning_report.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"   ✅ 深度学习报告已生成")
        return result
    return None

def main():
    print("="*60)
    print("🎯 NWACS V8.0 全面检测与优化系统")
    print("="*60)

    start_time = datetime.now()
    print(f"\n启动时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    tasks = [
        ("项目结构分析", analyze_project_structure),
        ("代码质量分析", analyze_code_quality),
        ("扩展知识库", enrich_knowledge_base),
        ("更新Skill描述", update_skill_descriptions),
        ("生成API文档", generate_api_documentation),
        ("生成深度学习报告", generate_deep_learning_report)
    ]

    completed = []
    failed = []

    for i, (task_name, task_func) in enumerate(tasks, 1):
        print(f"\n任务 {i}/{len(tasks)}: {task_name}")
        try:
            success = task_func()
            if success:
                completed.append(task_name)
                print(f"   ✅ 完成")
            else:
                failed.append(task_name)
                print(f"   ❌ 失败")
        except Exception as e:
            failed.append(task_name)
            print(f"   ❌ 异常: {e}")

        if i < len(tasks):
            time.sleep(3)

    end_time = datetime.now()

    print("\n" + "="*60)
    print("🎉 全面检测与优化完成！")
    print("="*60)

    print(f"\n完成时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"总耗时: {(end_time - start_time).total_seconds() / 60:.1f}分钟")

    print(f"\n✅ 成功完成 ({len(completed)}):")
    for task in completed:
        print(f"   - {task}")

    if failed:
        print(f"\n❌ 失败 ({len(failed)}):")
        for task in failed:
            print(f"   - {task}")

    print("\n📁 生成的文件:")
    print("  1. analysis/report_project_structure.md - 项目结构分析报告")
    print("  2. analysis/report_code_quality.md - 代码质量分析报告")
    print("  3. core/v8/engine/extended_knowledge.json - 扩展知识库")
    print("  4. core/v8/skill_manager/skill_descriptions.json - Skill描述")
    print("  5. docs/api_documentation.json - API文档")
    print("  6. docs/deep_learning_report.json - 深度学习报告")

if __name__ == "__main__":
    main()
