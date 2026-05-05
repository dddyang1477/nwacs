#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS v7.0 API服务 v2
增强版API，支持用户知识库和更多功能
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

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
    'version': 'v2.0',
    'api_key': os.environ.get('DEEPSEEK_API_KEY') or 'sk-f3246fbd1eef446e9a11d78efefd9bba',
    'base_url': 'https://api.deepseek.com',
    'model': 'deepseek-chat'
}

# 初始化OpenAI
openai_client = None
try:
    openai_client = openai.OpenAI(
        api_key=API_CONFIG['api_key'],
        base_url=API_CONFIG['base_url']
    )
except Exception as e:
    print(f"⚠️ OpenAI初始化失败: {e}")


def error_response(message, status_code=400, error_code=None):
    """错误响应"""
    response = {
        'success': False,
        'error': message,
        'timestamp': datetime.now().isoformat()
    }
    if error_code:
        response['error_code'] = error_code
    return jsonify(response), status_code


def success_response(data, message='Success', meta=None):
    """成功响应"""
    response = {
        'success': True,
        'message': message,
        'data': data,
        'timestamp': datetime.now().isoformat()
    }
    if meta:
        response['meta'] = meta
    return jsonify(response)


# ============================================
# 辅助函数
# ============================================

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


# ============================================
# 用户知识库管理
# ============================================

def init_user_kb():
    """初始化用户知识库"""
    from core.knowledge_base_manager import KnowledgeBaseManager
    return KnowledgeBaseManager()

user_kb_manager = init_user_kb()


# ============================================
# API路由
# ============================================

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')


@app.route('/api/v2/health', methods=['GET'])
def health_check_v2():
    """健康检查 v2"""
    return success_response({
        'status': 'healthy',
        'version': API_CONFIG['version'],
        'api_key_configured': bool(API_CONFIG['api_key']),
        'openai_ready': openai_client is not None
    })


# ============================================
# 小说类型接口
# ============================================

@app.route('/api/v2/novel-types', methods=['GET'])
def get_novel_types_v2():
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
    return success_response(types, meta={'total': len(types)})


# ============================================
# 创作接口
# ============================================

@app.route('/api/v2/create', methods=['POST'])
def create_chapter_v2():
    """创建小说章节"""
    data = request.get_json()

    if not data:
        return error_response("请提供JSON数据", error_code="INVALID_REQUEST")

    novel_type = data.get('novel_type')
    chapter_title = data.get('chapter_title', '第一章')
    prompt = data.get('prompt')
    word_count = data.get('word_count', 3000)
    user_kb_id = data.get('user_knowledge_base_id')  # 可选：用户知识库

    if not novel_type:
        return error_response("请选择小说类型", error_code="MISSING_TYPE")
    if not prompt:
        return error_response("请输入创作需求", error_code="MISSING_PROMPT")

    if not openai_client:
        return error_response("OpenAI服务未配置", error_code="SERVICE_UNAVAILABLE", status_code=503)

    skill_file = get_novel_type_skill(novel_type)
    skill_content = load_skill_content(skill_file)

    # 如果指定了用户知识库，加载其内容
    user_kb_context = ""
    if user_kb_id:
        kb_result = user_kb_manager.get_knowledge_base(user_kb_id)
        if kb_result['success']:
            entries = kb_result['content']['entries']
            if entries:
                user_kb_context = "\n\n## 用户自定义知识库内容：\n"
                for entry in entries[:10]:  # 最多使用10条
                    user_kb_context += f"问：{entry['question']}\n答：{entry['answer']}\n\n"

    system_prompt = f"""你是NWACS v7.0专业小说创作助手。
请以流畅、生动、富有画面感的文笔创作小说。

以下是该类型的专业Skill知识：
{skill_content}
{user_kb_context}

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

        return success_response({
            "title": chapter_title,
            "content": content,
            "novel_type": novel_type,
            "word_count": len(content.replace(' ', '')),
            "user_knowledge_base_used": bool(user_kb_id)
        }, message="创作成功")

    except Exception as e:
        return error_response(f"创作失败: {str(e)}", error_code="CREATION_FAILED", status_code=500)


# ============================================
# 质量检查接口
# ============================================

@app.route('/api/v2/quality-check', methods=['POST'])
def quality_check_v2():
    """质量检查"""
    data = request.get_json()

    if not data:
        return error_response("请提供JSON数据", error_code="INVALID_REQUEST")

    text = data.get('text', '')

    if not text:
        return error_response("请输入要检查的文本", error_code="MISSING_TEXT")

    words = len(text.replace(' ', ''))
    sentences = len([s for s in text.split('。') if s.strip()])
    avg_sentence_length = words / max(sentences, 1)

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
        'readability_level': level,
        'suggestions': [
            "保持段落简洁，每段不超过200字" if avg_sentence_length > 30 else None,
            "适当增加对话，使人物更鲜活" if '"' not in text and '"' not in text else None,
            "注意开篇吸引力，前300字至关重要" if words > 500 else None
        ]
    })


# ============================================
# 用户知识库接口
# ============================================

@app.route('/api/v2/knowledge-bases', methods=['GET'])
def list_knowledge_bases_v2():
    """获取知识库列表"""
    result = user_kb_manager.list_knowledge_bases()
    return success_response(result['user_knowledge_bases'], meta={'total': result['total']})


@app.route('/api/v2/knowledge-bases', methods=['POST'])
def create_knowledge_base_v2():
    """创建知识库"""
    data = request.get_json()

    if not data:
        return error_response("请提供JSON数据", error_code="INVALID_REQUEST")

    name = data.get('name')
    description = data.get('description', '')
    kb_type = data.get('type', 'custom')

    if not name:
        return error_response("请提供知识库名称", error_code="MISSING_NAME")

    result = user_kb_manager.create_knowledge_base(name, description, kb_type)
    return success_response(result['knowledge_base'], message="知识库创建成功", status_code=201)


@app.route('/api/v2/knowledge-bases/<kb_id>', methods=['GET'])
def get_knowledge_base_v2(kb_id):
    """获取知识库详情"""
    result = user_kb_manager.get_knowledge_base(kb_id)
    if result['success']:
        return success_response(result)
    return error_response("知识库不存在", error_code="NOT_FOUND", status_code=404)


@app.route('/api/v2/knowledge-bases/<kb_id>/entries', methods=['POST'])
def add_knowledge_entry_v2(kb_id):
    """添加知识条目"""
    data = request.get_json()

    if not data:
        return error_response("请提供JSON数据", error_code="INVALID_REQUEST")

    question = data.get('question')
    answer = data.get('answer')
    tags = data.get('tags', [])

    if not question or not answer:
        return error_response("请提供问题和答案", error_code="MISSING_FIELDS")

    result = user_kb_manager.add_knowledge_entry(kb_id, question, answer, tags)
    if result['success']:
        return success_response(None, message="知识条目添加成功")
    return error_response("知识库不存在", error_code="NOT_FOUND", status_code=404)


@app.route('/api/v2/knowledge-bases/<kb_id>/search', methods=['GET'])
def search_knowledge_base_v2(kb_id):
    """搜索知识库"""
    query = request.args.get('q', '')
    limit = int(request.args.get('limit', 5))

    if not query:
        return error_response("请提供搜索关键词", error_code="MISSING_QUERY")

    result = user_kb_manager.search_knowledge(kb_id, query, limit)
    return success_response(result['results'], meta={
        'query': query,
        'count': result['count']
    })


@app.route('/api/v2/knowledge-bases/<kb_id>', methods=['DELETE'])
def delete_knowledge_base_v2(kb_id):
    """删除知识库"""
    result = user_kb_manager.delete_knowledge_base(kb_id)
    if result['success']:
        return success_response(None, message="知识库删除成功")
    return error_response("知识库不存在", error_code="NOT_FOUND", status_code=404)


# ============================================
# 系统统计接口
# ============================================

@app.route('/api/v2/stats', methods=['GET'])
def get_stats_v2():
    """获取系统统计"""
    project_root = Path(__file__).parent.parent

    py_files = list(project_root.glob("**/*.py"))
    md_files = list(project_root.glob("**/*.md"))
    skills_level3 = list((project_root / "skills/level3").glob("*.md"))
    skills_level2 = list((project_root / "skills/level2").glob("*.md"))

    kb_result = user_kb_manager.list_knowledge_bases()

    return success_response({
        'system': {
            'version': 'v7.0',
            'architecture': 'v2.2',
            'python_files': len(py_files),
            'markdown_files': len(md_files)
        },
        'skills': {
            'level3': len(skills_level3),
            'level2': len(skills_level2)
        },
        'knowledge_bases': {
            'built_in': 32,
            'user_created': kb_result['total']
        }
    })


# ============================================
# 启动服务
# ============================================

def main():
    """主函数"""
    print("="*60)
    print("🚀 NWACS v7.0 API服务 v2")
    print("="*60)
    print()
    print(f"📍 服务地址: http://localhost:5000")
    print(f"🌐 Web界面: http://localhost:5000/")
    print(f"📚 API版本: {API_CONFIG['version']}")
    print()
    print("按 Ctrl+C 停止服务")
    print("="*60)

    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == '__main__':
    main()
