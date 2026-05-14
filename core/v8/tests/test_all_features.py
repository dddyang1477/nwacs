"""
NWACS 全功能端到端测试脚本
测试所有 API 端点是否正常调用和返回
结果写入 test_report.txt
"""
import subprocess
import sys
import time
import json
import urllib.request
import urllib.error
import os
import traceback

BASE = os.path.dirname(__file__)
REPORT_FILE = os.path.join(BASE, 'test_report.txt')
SERVER_LOG = os.path.join(BASE, 'server_debug.log')

results = []
passed = 0
failed = 0
errors = []

def report(msg, ok=True):
    global passed, failed
    status = "✅ PASS" if ok else "❌ FAIL"
    if ok:
        passed += 1
    else:
        failed += 1
    line = f"{status} | {msg}"
    results.append(line)
    print(line)

def api_get(path, timeout=10):
    url = f"http://localhost:8099{path}"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode('utf-8'))

def api_post(path, data, timeout=120):
    url = f"http://localhost:8099{path}"
    body = json.dumps(data, ensure_ascii=False).encode('utf-8')
    req = urllib.request.Request(url, data=body, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode('utf-8'))

# ============================================================
# Step 1: Start server
# ============================================================
report("=== 阶段1: 启动服务器 ===", True)

# Kill existing python processes
subprocess.run(['taskkill', '/F', '/IM', 'python.exe'], capture_output=True)
time.sleep(2)

server_proc = subprocess.Popen(
    [sys.executable, 'nwacs_server_v3.py'],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    cwd=BASE,
    text=True,
)
time.sleep(6)

# Check if server is running
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(3)
try:
    s.connect(('localhost', 8099))
    s.close()
    report("服务器启动成功，端口8099已监听")
except Exception as e:
    report(f"服务器启动失败: {e}", False)
    errors.append(f"服务器无法启动: {e}")
    # Try to read server output
    try:
        server_output = server_proc.stdout.read()
        results.append(f"Server output: {server_output[:500]}")
    except:
        pass

# ============================================================
# Step 2: Test GET endpoints
# ============================================================
report("=== 阶段2: GET 端点测试 ===", True)

# 2.1 Health
try:
    data = api_get('/api/health')
    if data.get('status') == 'ok':
        report("GET /api/health - 健康检查正常")
    else:
        report(f"GET /api/health - 返回异常: {data}", False)
except Exception as e:
    report(f"GET /api/health - 失败: {e}", False)
    errors.append(f"health: {e}")

# 2.2 Models
try:
    data = api_get('/api/models')
    models = data.get('models', [])
    current = data.get('current', {})
    if models and current:
        report(f"GET /api/models - 返回{len(models)}个模型, 当前={current.get('model_name','?')}")
    else:
        report(f"GET /api/models - 数据不完整: {data}", False)
except Exception as e:
    report(f"GET /api/models - 失败: {e}", False)
    errors.append(f"models: {e}")

# 2.3 Config
try:
    data = api_get('/api/config')
    if data.get('provider'):
        report(f"GET /api/config - provider={data['provider']}, model={data.get('model_name','?')}")
    else:
        report(f"GET /api/config - 数据不完整: {data}", False)
except Exception as e:
    report(f"GET /api/config - 失败: {e}", False)
    errors.append(f"config: {e}")

# 2.4 Options
try:
    data = api_get('/api/options')
    genres = data.get('genres', {})
    schools = data.get('schools', {})
    styles = data.get('styles', {})
    tones = data.get('tones', {})
    lengths = data.get('lengths', {})
    if genres and schools and styles:
        total_schools = sum(len(v) for v in schools.values())
        report(f"GET /api/options - {len(genres)}类型, {total_schools}流派, {len(styles)}风格, {len(tones)}基调, {len(lengths)}篇幅")
    else:
        report(f"GET /api/options - 数据不完整", False)
except Exception as e:
    report(f"GET /api/options - 失败: {e}", False)
    errors.append(f"options: {e}")

# 2.5 Frontend HTML
try:
    url = "http://localhost:8099/"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode('utf-8')
        if '<!DOCTYPE html>' in html and '</html>' in html:
            report(f"GET / - 前端页面加载成功 ({len(html)}字节)")
        else:
            report(f"GET / - HTML不完整 ({len(html)}字节)", False)
except Exception as e:
    report(f"GET / - 失败: {e}", False)
    errors.append(f"frontend: {e}")

# ============================================================
# Step 3: Test POST endpoints (core writing flow)
# ============================================================
report("=== 阶段3: 核心写作流程测试 ===", True)

# 3.1 Generate Plots
plot_data = None
try:
    data = api_post('/api/generate_plots', {
        'genres': ['玄幻'],
        'styles': ['热血爽文'],
        'tones': ['紧张刺激'],
        'length': '中长篇',
        'theme': '逆境成长',
        'schools': ['mortal'],
        'school_names': ['凡人流'],
    }, timeout=120)
    if data.get('success') and data.get('plots'):
        plots = data['plots']
        report(f"POST /api/generate_plots - 生成{len(plots)}个剧情方案")
        for p in plots:
            report(f"  - {p.get('name','?')}: {p.get('tagline','?')[:40]}")
        plot_data = data
    else:
        report(f"POST /api/generate_plots - 失败: {data}", False)
        errors.append(f"generate_plots: {data}")
except Exception as e:
    report(f"POST /api/generate_plots - 异常: {e}", False)
    errors.append(f"generate_plots: {e}")

# 3.2 Generate Outline (select_plot)
outline_data = None
if plot_data and plot_data.get('plots'):
    try:
        first_plot = plot_data['plots'][0]
        data = api_post('/api/select_plot', {
            'plot_id': first_plot['id'],
            'plot_name': first_plot['name'],
            'genres': ['玄幻'],
            'styles': ['热血爽文'],
            'tones': ['紧张刺激'],
            'length': '中长篇',
            'theme': '逆境成长',
            'schools': ['mortal'],
            'school_names': ['凡人流'],
        }, timeout=180)
        if data.get('success') and data.get('outline'):
            outline = data['outline']
            chars = outline.get('characters', [])
            acts = outline.get('acts', [])
            total_chapters = sum(len(act.get('chapters', [])) for act in acts)
            report(f"POST /api/select_plot - 大纲生成成功: {outline.get('title','?')}, {len(chars)}角色, {total_chapters}章")
            for ch in chars:
                report(f"  - {ch.get('name','?')}({ch.get('role','?')}): {ch.get('name_meaning','?')[:30]}...")
            outline_data = data
        else:
            report(f"POST /api/select_plot - 失败: {str(data)[:200]}", False)
            errors.append(f"select_plot: {str(data)[:200]}")
    except Exception as e:
        report(f"POST /api/select_plot - 异常: {e}", False)
        errors.append(f"select_plot: {e}")

# 3.3 Generate Chapter
chapter_content = None
if outline_data and outline_data.get('outline'):
    try:
        outline = outline_data['outline']
        acts = outline.get('acts', [])
        if acts and acts[0].get('chapters'):
            ch1 = acts[0]['chapters'][0]
            data = api_post('/api/generate_chapter', {
                'chapter_number': ch1.get('number', 1),
                'chapter_title': ch1.get('title', '第1章'),
                'chapter_summary': ch1.get('summary', ''),
                'genres': ['玄幻'],
                'styles': ['热血爽文'],
                'tones': ['紧张刺激'],
                'theme': '逆境成长',
                'schools': ['mortal'],
                'school_names': ['凡人流'],
                'outline': outline,
                'previous_chapter_content': '',
                'previous_chapter_num': 0,
            }, timeout=180)
            if data.get('success') and data.get('content'):
                content = data['content']
                char_count = len(content)
                report(f"POST /api/generate_chapter - 第{data.get('chapter_number',1)}章生成成功: {char_count}字")
                if char_count >= 4000:
                    report(f"  ✅ 字数达标 (≥4000)")
                else:
                    report(f"  ⚠️ 字数不足4000: {char_count}字", False)
                chapter_content = content
            else:
                report(f"POST /api/generate_chapter - 失败: {str(data)[:200]}", False)
                errors.append(f"generate_chapter: {str(data)[:200]}")
    except Exception as e:
        report(f"POST /api/generate_chapter - 异常: {e}", False)
        errors.append(f"generate_chapter: {e}")

# ============================================================
# Step 4: Test AI detection and rewrite
# ============================================================
report("=== 阶段4: AI检测与重写测试 ===", True)

test_text = chapter_content if chapter_content else "这是一段测试文本，用于验证AI检测功能是否正常工作。主角林逸站在山巅，望着远方的云海，心中涌起无限感慨。"

# 4.1 AI Detection
try:
    data = api_post('/api/detect_ai', {
        'text': test_text[:2000],
        'deep': True,
    }, timeout=60)
    if data.get('success') and data.get('result'):
        result = data['result']
        report(f"POST /api/detect_ai - AI评分={result.get('ai_score','?')}, 置信度={result.get('confidence','?')}")
    else:
        report(f"POST /api/detect_ai - 失败: {str(data)[:200]}", False)
        errors.append(f"detect_ai: {str(data)[:200]}")
except Exception as e:
    report(f"POST /api/detect_ai - 异常: {e}", False)
    errors.append(f"detect_ai: {e}")

# 4.2 Rewrite
try:
    data = api_post('/api/rewrite', {
        'text': test_text[:1000],
        'style': 'deai',
    }, timeout=60)
    if data.get('success') and data.get('content'):
        report(f"POST /api/rewrite - 重写成功 ({len(data['content'])}字)")
    else:
        report(f"POST /api/rewrite - 失败: {str(data)[:200]}", False)
        errors.append(f"rewrite: {str(data)[:200]}")
except Exception as e:
    report(f"POST /api/rewrite - 异常: {e}", False)
    errors.append(f"rewrite: {e}")

# ============================================================
# Step 5: Test name generation endpoints
# ============================================================
report("=== 阶段5: 名字生成系统测试 ===", True)

# 5.1 Character Names
try:
    data = api_post('/api/generate_names', {
        'genre': '玄幻',
        'role': 'protagonist',
        'gender': 'male',
        'personality': '坚毅果敢，外冷内热',
        'background': '出身平凡的猎户之子',
        'fate': '注定成为拯救世界的英雄',
        'ability': '剑道天赋',
        'weakness': '过于重情义',
        'arc': '从自卑少年成长为自信强者',
        'story_context': '在一个灵气复苏的世界中',
        'count': 3,
    }, timeout=60)
    if data.get('success') and data.get('names'):
        names = data['names']
        report(f"POST /api/generate_names - 生成{len(names)}个角色名")
        for n in names:
            report(f"  - {n.get('full_name','?')}: {n.get('meaning','?')[:40]}... (评分:{n.get('score','?')})")
    else:
        report(f"POST /api/generate_names - 失败: {str(data)[:200]}", False)
        errors.append(f"generate_names: {str(data)[:200]}")
except Exception as e:
    report(f"POST /api/generate_names - 异常: {e}", False)
    errors.append(f"generate_names: {e}")

# 5.2 Titles
try:
    data = api_post('/api/generate_titles', {
        'genre': '玄幻',
        'character_name': '林逸',
        'personality': '坚毅果敢',
        'ability': '剑道通神',
        'title_style': 'domineering',
    }, timeout=60)
    if data.get('success'):
        titles = data.get('titles', [])
        report(f"POST /api/generate_titles - 生成{len(titles)}个称号")
    else:
        report(f"POST /api/generate_titles - 失败: {str(data)[:200]}", False)
        errors.append(f"generate_titles: {str(data)[:200]}")
except Exception as e:
    report(f"POST /api/generate_titles - 异常: {e}", False)
    errors.append(f"generate_titles: {e}")

# 5.3 Organization Names
try:
    data = api_post('/api/generate_org_names', {
        'genre': '玄幻',
        'org_type': 'sect',
        'description': '一个隐世多年的古老剑修宗门',
        'count': 3,
    }, timeout=60)
    if data.get('success'):
        orgs = data.get('organizations', [])
        report(f"POST /api/generate_org_names - 生成{len(orgs)}个组织名")
    else:
        report(f"POST /api/generate_org_names - 失败: {str(data)[:200]}", False)
        errors.append(f"generate_org_names: {str(data)[:200]}")
except Exception as e:
    report(f"POST /api/generate_org_names - 异常: {e}", False)
    errors.append(f"generate_org_names: {e}")

# 5.4 Power System
try:
    data = api_post('/api/generate_power_system', {
        'genre': '玄幻',
        'system_type': 'cultivation',
        'description': '以剑道为核心的修炼体系',
        'count': 5,
    }, timeout=60)
    if data.get('success'):
        levels = data.get('levels', [])
        report(f"POST /api/generate_power_system - 生成{len(levels)}个等级")
    else:
        report(f"POST /api/generate_power_system - 失败: {str(data)[:200]}", False)
        errors.append(f"generate_power_system: {str(data)[:200]}")
except Exception as e:
    report(f"POST /api/generate_power_system - 异常: {e}", False)
    errors.append(f"generate_power_system: {e}")

# ============================================================
# Step 6: Test config update
# ============================================================
report("=== 阶段6: 配置更新测试 ===", True)

try:
    data = api_post('/api/config', {
        'temperature': 0.8,
        'max_tokens': 6000,
    }, timeout=10)
    if data.get('success'):
        report(f"POST /api/config - 配置更新成功")
    else:
        report(f"POST /api/config - 失败: {data}", False)
except Exception as e:
    report(f"POST /api/config - 异常: {e}", False)
    errors.append(f"config_update: {e}")

# ============================================================
# Step 7: Check knowledge base
# ============================================================
report("=== 阶段7: 知识库检查 ===", True)

kb_file = os.path.join(BASE, 'genre_knowledge_base.json')
if os.path.exists(kb_file):
    try:
        with open(kb_file, 'r', encoding='utf-8') as f:
            kb = json.load(f)
        total_schools = sum(len(v) for v in kb.values() if isinstance(v, dict))
        report(f"知识库文件存在: {len(kb)}类型, {total_schools}流派")
        for genre, schools in kb.items():
            if isinstance(schools, dict):
                school_list = [s for s in schools.keys() if isinstance(schools[s], dict) and 'error' not in schools[s]]
                report(f"  - {genre}: {len(school_list)}个流派数据完整")
    except Exception as e:
        report(f"知识库读取失败: {e}", False)
else:
    report("知识库文件不存在!", False)
    errors.append("knowledge_base missing")

# ============================================================
# Step 8: Check server log for errors
# ============================================================
report("=== 阶段8: 服务器日志检查 ===", True)

if os.path.exists(SERVER_LOG):
    try:
        with open(SERVER_LOG, 'r', encoding='utf-8') as f:
            log_lines = f.readlines()
        error_lines = [l for l in log_lines if 'Error' in l or 'error' in l or 'Traceback' in l or 'Exception' in l]
        if error_lines:
            report(f"服务器日志中发现{len(error_lines)}条错误/异常记录:", False)
            for l in error_lines[-10:]:
                report(f"  ⚠️ {l.strip()[:120]}", False)
        else:
            report("服务器日志无错误记录")
    except Exception as e:
        report(f"读取服务器日志失败: {e}", False)
else:
    report("服务器日志文件不存在", False)

# ============================================================
# Summary
# ============================================================
report("=" * 60, True)
report(f"测试完成: {passed}通过, {failed}失败, {len(errors)}个错误", failed == 0)

if errors:
    report("--- 错误详情 ---", False)
    for e in errors:
        report(f"  ❌ {e}", False)

# Write report
with open(REPORT_FILE, 'w', encoding='utf-8') as f:
    f.write('\n'.join(results))

# Cleanup
server_proc.terminate()
server_proc.wait(timeout=5)
print(f"\n报告已保存到: {REPORT_FILE}")