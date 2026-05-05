#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS v7.0 API服务
让Web UI能调用NWACS核心引擎
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from functools import wraps

try:
    from flask import Flask, request, jsonify, render_template
    import openai
except ImportError:
    print("❌ 请先安装依赖库：pip install flask openai")
    sys.exit(1)


# 初始化Flask应用
app = Flask(__name__,
            template_folder='../web_ui',
            static_folder='../web_ui',
            static_url_path='')

app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# API配置
API_CONFIG = {
    'api_key': os.environ.get('DEEPSEEK_API_KEY') or 'sk-f3246fbd1eef446e9a11d78efefd9bba',
    'base_url': 'https://api.deepseek.com',
    'model': 'deepseek-chat'
}


def init_openai():
    """初始化OpenAI客户端"""
    try:
        client = openai.OpenAI(
            api_key=API_CONFIG['api_key'],
            base_url=API_CONFIG['base_url']
        )
        return client
    except Exception as e:
        print(f"❌ OpenAI初始化失败: {e}")
        return None


# 全局OpenAI客户端
openai_client = init_openai()


def error_response(message, status_code=400):
    """错误响应"""
    return jsonify({
        'success': False,
        'error': message,
        'timestamp': datetime.now().isoformat()
    }), status_code


def success_response(data, message='Success'):
    """成功响应"""
    return jsonify({
        'success': True,
        'message': message,
        'data': data,
        'timestamp': datetime.now().isoformat()
    })


def load_skill_content(skill_path: str) -> str:
    """加载Skill内容"""
    project_root = Path(__file__).parent.parent
    full_path = project_root / skill_path

    if full_path.exists():
        with open(full_path, 'r', encoding='utf-8') as f:
            return f.read(3000)
    return f"未找到Skill: {skill_path}"


def get_novel_type_skill(novel_type: str) -> str:
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


def generate_chapter(novel_type: str, prompt: str, chapter_title: str, word_count: int = 3000) -> dict:
    """生成小说章节"""
    if not openai_client:
        return {"success": False, "error": "OpenAI客户端未初始化"}

    skill_file = get_novel_type_skill(novel_type)
    skill_content = load_skill_content(skill_file)

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
        response = openai_client.chat.completions.create(
            model=API_CONFIG['model'],
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=4000
        )

        content = response.choices[0].message.content

        return {
            "success": True,
            "title": chapter_title,
            "content": content,
            "novel_type": novel_type,
            "word_count": len(content.replace(' ', ''))
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


# ============================================
# API路由
# ============================================

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')


@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查"""
    return success_response({
        'status': 'healthy',
        'version': 'v7.0',
        'api_configured': bool(API_CONFIG['api_key'])
    })


@app.route('/api/novel-types', methods=['GET'])
def get_novel_types():
    """获取支持的小说类型"""
    types = [
        {"id": "xuanhuan", "name": "玄幻仙侠", "icon": "🐉", "description": "修仙、玄幻、仙侠"},
        {"id": "dushi", "name": "都市言情", "icon": "🏙️", "description": "都市、言情、职场"},
        {"id": "xuanyi", "name": "悬疑推理", "icon": "🔍", "description": "悬疑、推理、侦探"},
        {"id": "kehuan", "name": "科幻未来", "icon": "🚀", "description": "科幻、未来、末世"},
        {"id": "lishi", "name": "历史穿越", "icon": "📜", "description": "历史、穿越、架空"},
        {"id": "kongbu", "name": "恐怖惊悚", "icon": "👻", "description": "恐怖、惊悚、灵异"},
        {"id": "youxi", "name": "游戏竞技", "icon": "🎮", "description": "游戏、竞技、电竞"},
        {"id": "nvpin", "name": "女频系列", "icon": "💖", "description": "总裁、年代、马甲、萌宝"}
    ]
    return success_response(types)


@app.route('/api/create', methods=['POST'])
def create_chapter():
    """创建小说章节"""
    data = request.get_json()

    if not data:
        return error_response("请提供JSON数据")

    novel_type = data.get('novel_type')
    chapter_title = data.get('chapter_title', '第一章')
    prompt = data.get('prompt')
    word_count = data.get('word_count', 3000)

    if not novel_type:
        return error_response("请选择小说类型")
    if not prompt:
        return error_response("请输入创作需求")

    result = generate_chapter(novel_type, prompt, chapter_title, word_count)

    if result['success']:
        return success_response(result, "创作成功")
    else:
        return error_response(result.get('error', '创作失败'), 500)


@app.route('/api/quality-check', methods=['POST'])
def quality_check():
    """质量检查"""
    data = request.get_json()

    if not data:
        return error_response("请提供JSON数据")

    text = data.get('text', '')

    if not text:
        return error_response("请输入要检查的文本")

    # 简单的质量检查
    words = len(text.replace(' ', ''))
    sentences = len([s for s in text.split('。') if s.strip()])
    avg_sentence_length = words / max(sentences, 1)

    # 可读性评分
    if avg_sentence_length < 15:
        readability = 90
        level = "极易阅读"
    elif avg_sentence_length < 25:
        readability = 75
        level = "易读"
    elif avg_sentence_length < 35:
        readability = 60
        level = "一般"
    elif avg_sentence_length < 50:
        readability = 45
        level = "稍难"
    else:
        readability = 30
        level = "难读"

    return success_response({
        'word_count': words,
        'sentence_count': sentences,
        'avg_sentence_length': round(avg_sentence_length, 1),
        'readability_score': readability,
        'readability_level': level
    })


@app.route('/api/knowledge-bases', methods=['GET'])
def get_knowledge_bases():
    """获取知识库列表"""
    project_root = Path(__file__).parent.parent
    knowledge_dir = project_root / "skills" / "level2" / "learnings"

    if not knowledge_dir.exists():
        return success_response([])

    files = []
    for f in knowledge_dir.glob("*.txt"):
        if "索引" not in f.name and "配置" not in f.name:
            files.append({
                "name": f.name,
                "path": str(f.relative_to(project_root))
            })

    return success_response(files)


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """获取系统统计"""
    project_root = Path(__file__).parent.parent

    # 统计文件
    py_files = list(project_root.glob("**/*.py"))
    md_files = list(project_root.glob("**/*.md"))
    skills_level3 = list((project_root / "skills/level3").glob("*.md"))
    skills_level2 = list((project_root / "skills/level2").glob("*.md"))

    return success_response({
        'python_files': len(py_files),
        'markdown_files': len(md_files),
        'level3_skills': len(skills_level3),
        'level2_skills': len(skills_level2),
        'knowledge_bases': 32,
        'version': 'v7.0',
        'architecture': 'v2.2'
    })


# ============================================
# 启动服务
# ============================================

def main():
    """主函数"""
    print("="*60)
    print("🚀 NWACS v7.0 API服务启动")
    print("="*60)
    print()
    print(f"📍 服务地址: http://localhost:5000")
    print(f"🌐 Web界面: http://localhost:5000/")
    print(f"📚 API文档: http://localhost:5000/api/health")
    print()
    print("按 Ctrl+C 停止服务")
    print("="*60)

    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == '__main__':
    main()
