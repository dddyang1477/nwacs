#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 文件整理与检测工具
"""

import os
import json
import shutil
from datetime import datetime

def analyze_directory(base_dir):
    """分析目录结构"""
    result = {
        'total_files': 0,
        'total_dirs': 0,
        'by_type': {},
        'size_bytes': 0,
        'problems': []
    }

    for root, dirs, files in os.walk(base_dir):
        result['total_dirs'] += len(dirs)
        
        for f in files:
            filepath = os.path.join(root, f)
            result['total_files'] += 1
            
            # 文件大小
            try:
                result['size_bytes'] += os.path.getsize(filepath)
            except:
                pass
            
            # 文件类型统计
            ext = os.path.splitext(f)[1].lower()
            if ext not in result['by_type']:
                result['by_type'][ext] = 0
            result['by_type'][ext] += 1
            
            # 问题检测
            if f.startswith('._'):
                result['problems'].append(f"隐藏文件: {filepath}")
            if '.pyc' in f and '__pycache__' not in filepath:
                result['problems'].append(f"孤立pyc文件: {filepath}")

    return result

def cleanup_directory(base_dir):
    """清理目录"""
    cleaned = {
        'removed_files': 0,
        'removed_dirs': 0,
        'freed_bytes': 0
    }

    # 删除旧备份（超过7天）
    backup_dir = os.path.join(base_dir, 'backup')
    if os.path.exists(backup_dir):
        now = datetime.now()
        for f in os.listdir(backup_dir):
            filepath = os.path.join(backup_dir, f)
            if os.path.isfile(filepath):
                mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
                if (now - mtime).days > 7:
                    size = os.path.getsize(filepath)
                    os.remove(filepath)
                    cleaned['removed_files'] += 1
                    cleaned['freed_bytes'] += size

    # 删除pycache目录
    for root, dirs, files in os.walk(base_dir):
        for d in dirs:
            if d == '__pycache__':
                dirpath = os.path.join(root, d)
                try:
                    shutil.rmtree(dirpath)
                    cleaned['removed_dirs'] += 1
                except:
                    pass

    # 删除孤立的.pyc文件
    for root, dirs, files in os.walk(base_dir):
        for f in files:
            if f.endswith('.pyc') and '__pycache__' not in root:
                filepath = os.path.join(root, f)
                try:
                    os.remove(filepath)
                    cleaned['removed_files'] += 1
                    cleaned['freed_bytes'] += os.path.getsize(filepath)
                except:
                    pass

    return cleaned

def verify_scripts(base_dir):
    """验证脚本文件"""
    scripts = [
        'start.bat',
        '系统自检.bat',
        '开始学习.bat',
        '空闲学习.bat'
    ]
    
    results = []
    for script in scripts:
        path = os.path.join(base_dir, script)
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if 'python' in content.lower() or 'py.exe' in content.lower():
                        results.append({'name': script, 'status': 'ok', 'reason': '包含Python调用'})
                    else:
                        results.append({'name': script, 'status': 'warning', 'reason': '未找到Python调用'})
            except Exception as e:
                results.append({'name': script, 'status': 'error', 'reason': str(e)})
        else:
            results.append({'name': script, 'status': 'missing', 'reason': '文件不存在'})
    
    return results

def verify_python_files(base_dir):
    """验证Python文件"""
    core_dir = os.path.join(base_dir, 'src', 'core')
    results = []
    
    if os.path.exists(core_dir):
        for f in os.listdir(core_dir):
            if f.endswith('.py'):
                filepath = os.path.join(core_dir, f)
                try:
                    with open(filepath, 'r', encoding='utf-8') as file:
                        content = file.read()
                        if len(content) < 10:
                            results.append({'name': f, 'status': 'warning', 'reason': '文件内容过短'})
                        else:
                            results.append({'name': f, 'status': 'ok', 'reason': '正常'})
                except Exception as e:
                    results.append({'name': f, 'status': 'error', 'reason': str(e)})
    
    return results

def generate_report(base_dir):
    """生成完整报告"""
    print("=" * 60)
    print("      NWACS 文件整理与检测报告")
    print("=" * 60)
    print(f"分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"分析目录: {base_dir}")
    print()

    # 1. 目录分析
    print("[1/4] 目录结构分析...")
    analysis = analyze_directory(base_dir)
    
    print(f"  总目录数: {analysis['total_dirs']}")
    print(f"  总文件数: {analysis['total_files']}")
    print(f"  总大小: {format_size(analysis['size_bytes'])}")
    print()
    print("  文件类型分布:")
    for ext, count in sorted(analysis['by_type'].items(), key=lambda x: -x[1]):
        print(f"    {ext or '无扩展名'}: {count}个")
    
    if analysis['problems']:
        print()
        print("  发现问题:")
        for p in analysis['problems'][:5]:
            print(f"    ! {p}")

    # 2. 脚本验证
    print("\n[2/4] 启动脚本验证...")
    scripts = verify_scripts(base_dir)
    for s in scripts:
        status_icon = {'ok': '✓', 'warning': '!', 'error': '✗', 'missing': '?'}[s['status']]
        print(f"  {status_icon} {s['name']}: {s['reason']}")

    # 3. Python文件验证
    print("\n[3/4] Python核心文件验证...")
    py_files = verify_python_files(base_dir)
    ok_count = sum(1 for f in py_files if f['status'] == 'ok')
    print(f"  正常: {ok_count}/{len(py_files)}")
    errors = [f for f in py_files if f['status'] != 'ok']
    if errors:
        print("  问题文件:")
        for e in errors[:3]:
            print(f"    ! {e['name']}: {e['reason']}")

    # 4. 清理操作
    print("\n[4/4] 执行清理...")
    cleaned = cleanup_directory(base_dir)
    print(f"  删除文件: {cleaned['removed_files']}个")
    print(f"  删除目录: {cleaned['removed_dirs']}个")
    print(f"  释放空间: {format_size(cleaned['freed_bytes'])}")

    print("\n" + "=" * 60)
    print("      整理完成！")
    print("=" * 60)

    # 生成目录结构文档
    generate_structure_doc(base_dir)

def format_size(bytes_size):
    """格式化文件大小"""
    if bytes_size < 1024:
        return f"{bytes_size} B"
    elif bytes_size < 1024 * 1024:
        return f"{bytes_size / 1024:.1f} KB"
    elif bytes_size < 1024 * 1024 * 1024:
        return f"{bytes_size / (1024 * 1024):.1f} MB"
    else:
        return f"{bytes_size / (1024 * 1024 * 1024):.1f} GB"

def generate_structure_doc(base_dir):
    """生成目录结构文档"""
    doc = f"""# NWACS 目录结构

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 目录结构

```
NWACS/
├── .trae/                    # Trae配置目录
│   └── skills/               # Skill配置
├── backup/                   # 备份文件（自动清理）
├── config/                   # 配置文件
│   └── *.json                # 各类配置
├── docs/                     # 文档目录
│   ├── architecture/         # 系统架构文档
│   ├── guides/               # 使用指南
│   ├── overview/             # 概览文档
│   └── protocols/            # 协议文档
├── examples/                 # 示例项目
│   └── xuanhuan/             # 玄幻小说示例
├── logs/                     # 日志文件
├── novel-mcp-server-v2/      # MCP服务器（TypeScript）
│   ├── src/                  # 源代码
│   └── dist/                 # 编译输出
├── novel_creation/           # 小说创作模块
├── output/                   # 输出文件
├── records/                  # 学习记录
├── skills/                   # Skill文件
│   ├── level1/               # 一级Skill
│   ├── level2/               # 二级Skill
│   └── level3/               # 三级Skill
├── src/                      # 核心源代码
│   ├── core/                 # 核心模块
│   └── mcp/                  # MCP相关代码
├── tests/                    # 测试文件
└── *.bat                     # 快捷启动脚本
```

## 快捷启动脚本

| 文件 | 功能 |
|------|------|
| `start.bat` | 启动完整系统 |
| `系统自检.bat` | 执行系统自检 |
| `开始学习.bat` | 启动学习系统 |
| `空闲学习.bat` | 启动空闲检测学习 |

## 核心模块

| 文件 | 功能 |
|------|------|
| `main_system.py` | 主系统入口 |
| `skill_learning_manager.py` | Skill学习管理器 |
| `llm_writer.py` | 大模型创作接口 |
| `file_cleanup.py` | 文件清理优化 |
| `skill_checkup.py` | Skill体检 |
| `idle_learning.py` | 空闲检测学习 |
| `web_learning.py` | 联网学习 |

## 配置文件

| 文件 | 说明 |
|------|------|
| `config.json` | 主配置文件（API密钥、阈值等） |
| `config/*.json` | 各模块配置 |
| `skill_knowledge_base.json` | Skill知识库 |
"""

    doc_path = os.path.join(base_dir, '目录结构.md')
    with open(doc_path, 'w', encoding='utf-8') as f:
        f.write(doc)
    print(f"  目录结构文档已生成: 目录结构.md")

if __name__ == "__main__":
    # 获取NWACS根目录
    script_path = os.path.abspath(__file__)
    core_dir = os.path.dirname(script_path)
    src_dir = os.path.dirname(core_dir)
    base_dir = os.path.dirname(src_dir)
    
    print(f"脚本路径: {script_path}")
    print(f"核心目录: {core_dir}")
    print(f"源目录: {src_dir}")
    print(f"NWACS目录: {base_dir}")
    print()
    
    generate_report(base_dir)