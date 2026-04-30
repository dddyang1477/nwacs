#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 系统维护工具
检测修复错码、删除无用代码、保持Skill连通性、优化配置
"""

import os
import sys
import json
import re
import shutil
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

VERSION = "1.0"

# ============================================================================
# 乱码检测和修复
# ============================================================================

def detect_encoding(filepath):
    """检测文件编码"""
    encodings = ['utf-8', 'gbk', 'gb2312', 'big5', 'latin-1']
    
    for enc in encodings:
        try:
            with open(filepath, 'r', encoding=enc) as f:
                f.read()
            return enc
        except UnicodeDecodeError:
            continue
    
    return None

def fix_file_encoding(filepath):
    """修复文件编码"""
    try:
        # 读取原始内容
        raw_content = None
        for enc in ['utf-8', 'gbk', 'gb2312', 'big5']:
            try:
                with open(filepath, 'rb') as f:
                    raw_content = f.read()
                content = raw_content.decode(enc)
                target_encoding = 'utf-8'
                break
            except (UnicodeDecodeError, LookupError):
                continue
        
        if content is None:
            return False, "无法识别编码"
        
        # 移除控制字符
        cleaned_content = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', content)
        
        # 修复常见乱码
        replacements = [
            (r'\xe2\x80\x93', '—'),
            (r'\xe2\x80\x94', '—'),
            (r'\xe2\x80\x98', "'"),
            (r'\xe2\x80\x99', "'"),
            (r'\xe2\x80\x9c', '"'),
            (r'\xe2\x80\x9d', '"'),
            (r'\xe2\x80\xa6', '…'),
            (r'\xc3\xa2\xc2\x80\xc2\x99', "'"),
            (r'\ufffd', '?'),
        ]
        
        for pattern, replacement in replacements:
            cleaned_content = cleaned_content.replace(pattern, replacement)
        
        # 保存修复后的文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)
        
        return True, f"已修复，编码: {target_encoding}"
    
    except Exception as e:
        return False, f"修复失败: {str(e)}"

# ============================================================================
# 无用代码检测
# ============================================================================

def detect_unused_code(filepath):
    """检测无用代码"""
    unused = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检测空函数
        empty_functions = re.findall(r'def (\w+)\([^)]*\):\s*(?:"""[\s\S]*?""")?\s*(?:pass|...)', content)
        for func in empty_functions:
            unused.append(f"空函数: {func}")
        
        # 检测空类
        empty_classes = re.findall(r'class (\w+)[^:]*:\s*(?:"""[\s\S]*?""")?\s*(?:pass|...)', content)
        for cls in empty_classes:
            unused.append(f"空类: {cls}")
        
        # 检测注释掉的代码
        commented_code = re.findall(r'#\s*(import|from|class|def|if|for|while)\s+', content)
        if commented_code:
            unused.append(f"注释掉的代码: {len(commented_code)}处")
        
    except Exception as e:
        return [f"检测失败: {str(e)}"]
    
    return unused

# ============================================================================
# Skill连通性检测
# ============================================================================

def check_skill_connectivity():
    """检查Skill之间的连通性"""
    print("\n" + "="*60)
    print("🔍 检查Skill连通性...")
    print("="*60)
    
    skills_dir = 'skills/level2'
    if not os.path.exists(skills_dir):
        return {"status": "error", "message": "skills/level2 目录不存在"}
    
    # 读取所有Skill文件
    skill_files = [f for f in os.listdir(skills_dir) if f.endswith('.md')]
    skills = {}
    
    for sf in skill_files:
        filepath = os.path.join(skills_dir, sf)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                skills[sf] = content
        except Exception as e:
            print(f"❌ 读取失败: {sf} - {e}")
    
    # 检查Skill之间的引用
    references = {}
    for skill_name, content in skills.items():
        refs = re.findall(r'\[\[([^\]]+)\]\]', content)
        refs += re.findall(r'【([^】]+)】', content)
        references[skill_name] = refs
    
    # 检查孤立Skill
    all_refs = set()
    for refs in references.values():
        all_refs.update(refs)
    
    isolated = []
    for skill_name in skills.keys():
        skill_short = skill_name.replace('二级Skill_', '').replace('.md', '')
        if not any(skill_short in str(refs) for refs in references.values()):
            if skill_name not in all_refs:
                isolated.append(skill_name)
    
    result = {
        "total_skills": len(skill_files),
        "isolated_skills": isolated,
        "references": references
    }
    
    print(f"\n📊 Skill总数: {len(skill_files)}")
    print(f"🔗 孤立Skill: {len(isolated)}")
    
    if isolated:
        print("\n⚠️ 孤立Skill列表:")
        for skill in isolated:
            print(f"   - {skill}")
    
    return result

# ============================================================================
# 配置文件优化
# ============================================================================

def optimize_config():
    """优化配置文件"""
    print("\n" + "="*60)
    print("⚙️ 优化配置文件...")
    print("="*60)
    
    config_file = 'config.json'
    
    # 默认配置
    default_config = {
        "api_key": "",
        "base_url": "https://api.deepseek.com/v1",
        "model": "deepseek-v4-pro",
        "enabled": True,
        "idle_threshold": 600,
        "sensitivity": {
            "content_type": "political",
            "check_level": "normal"
        },
        "learning_enabled": True,
        "auto_sync": False,
        "cache_expiry": 3600,
        "writing": {
            "min_chapter_words": 3000,
            "max_chapter_words": 5500,
            "short_novel_words": 10000,
            "medium_novel_words": 30000,
            "long_novel_words": 500000
        }
    }
    
    try:
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                current_config = json.load(f)
            
            # 检查并添加缺失的配置
            updated = False
            for key, value in default_config.items():
                if key not in current_config:
                    current_config[key] = value
                    updated = True
                    print(f"➕ 添加配置: {key}")
            
            if updated:
                with open(config_file, 'w', encoding='utf-8') as f:
                    json.dump(current_config, f, indent=4, ensure_ascii=False)
                print(f"✅ 配置文件已更新")
            else:
                print(f"✅ 配置文件已是最新")
            
            return True, "配置优化完成"
        else:
            # 创建默认配置
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=4, ensure_ascii=False)
            print(f"✅ 默认配置文件已创建")
            return True, "配置创建完成"
    
    except Exception as e:
        return False, f"配置优化失败: {str(e)}"

# ============================================================================
# 清理无用文件
# ============================================================================

def cleanup_useless_files():
    """清理无用文件"""
    print("\n" + "="*60)
    print("🧹 清理无用文件...")
    print("="*60)
    
    # 无用文件模式
    useless_patterns = [
        r'^test_.*\.py$',
        r'^temp_.*\.py$',
        r'^debug_.*\.py$',
        r'^old_.*\.py$',
        r'^backup_.*\.py$',
        r'^\..*\.tmp$',
        r'^__pycache__$',
        r'\.pyc$',
        r'\.pyo$'
    ]
    
    # 保留的重要文件
    important_files = [
        'nwacs_console.py',
        'auto_learning.py',
        'idle_learning.py',
        'main_system.py',
        'skill_learning_manager.py',
        'config.json'
    ]
    
    cleaned_files = []
    errors = []
    
    for root, dirs, files in os.walk('.'):
        # 跳过output和learning目录
        if 'output' in root or 'learning' in root or '.git' in root:
            continue
        
        for filename in files:
            filepath = os.path.join(root, filename)
            
            # 检查是否应该清理
            should_clean = False
            
            # 检查模式
            for pattern in useless_patterns:
                if re.match(pattern, filename):
                    should_clean = True
                    break
            
            # 检查是否重要文件
            if filename in important_files:
                should_clean = False
            
            # 检查文件大小（空文件）
            try:
                if os.path.getsize(filepath) == 0:
                    should_clean = True
            except:
                pass
            
            if should_clean:
                try:
                    # 备份到临时目录
                    backup_dir = 'temp_backup'
                    os.makedirs(backup_dir, exist_ok=True)
                    backup_path = os.path.join(backup_dir, filename)
                    shutil.copy2(filepath, backup_path)
                    
                    # 删除原文件
                    os.remove(filepath)
                    cleaned_files.append(filepath)
                    print(f"🗑️ 已清理: {filepath}")
                except Exception as e:
                    errors.append(f"{filepath}: {str(e)}")
    
    result = {
        "cleaned": len(cleaned_files),
        "errors": errors
    }
    
    print(f"\n📊 清理完成: {len(cleaned_files)} 个文件")
    if errors:
        print(f"❌ 错误: {len(errors)} 个")
    
    return result

# ============================================================================
# 主流程
# ============================================================================

def main():
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║           NWACS 系统维护工具 v{VERSION}                          ║
║                                                              ║
║           🔍 检测修复错码                                     ║
║           🗑️  删除无用代码                                     ║
║           🔗 保持Skill连通性                                  ║
║           ⚙️  优化配置文件                                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    results = {}
    
    # 1. 检测和修复乱码
    print("\n" + "="*60)
    print("🔍 第一步：检测和修复乱码...")
    print("="*60)
    
    encoding_fixes = []
    file_types = ['*.py', '*.md', '*.txt', '*.json']
    
    for file_type in file_types:
        for root, dirs, files in os.walk('.'):
            # 跳过特定目录
            if any(skip in root for skip in ['output', 'learning', '.git', '__pycache__']):
                continue
            
            for filename in files:
                if filename.endswith(tuple(file_type.replace('*', ''))):
                    filepath = os.path.join(root, filename)
                    
                    # 检测编码
                    encoding = detect_encoding(filepath)
                    
                    if encoding != 'utf-8':
                        print(f"⚠️  {filepath} - 编码: {encoding}")
                        success, message = fix_file_encoding(filepath)
                        encoding_fixes.append({
                            "file": filepath,
                            "success": success,
                            "message": message
                        })
    
    results['encoding_fixes'] = encoding_fixes
    print(f"\n📊 编码修复: {sum(1 for f in encoding_fixes if f['success'])}/{len(encoding_fixes)}")
    
    # 2. 检测无用代码
    print("\n" + "="*60)
    print("🔍 第二步：检测无用代码...")
    print("="*60)
    
    unused_code = []
    py_files = []
    
    for root, dirs, files in os.walk('.'):
        if any(skip in root for skip in ['output', 'learning', '.git', '__pycache__']):
            continue
        for filename in files:
            if filename.endswith('.py'):
                py_files.append(os.path.join(root, filename))
    
    for filepath in py_files:
        unused = detect_unused_code(filepath)
        if unused:
            print(f"\n⚠️  {filepath}:")
            for u in unused:
                print(f"   - {u}")
            unused_code.append({"file": filepath, "issues": unused})
    
    results['unused_code'] = unused_code
    print(f"\n📊 检测到无用代码: {len(unused_code)} 个文件")
    
    # 3. 检查Skill连通性
    results['skill_connectivity'] = check_skill_connectivity()
    
    # 4. 优化配置文件
    success, message = optimize_config()
    results['config_optimize'] = {"success": success, "message": message}
    
    # 5. 清理无用文件
    results['cleanup'] = cleanup_useless_files()
    
    # 生成报告
    generate_report(results)

def generate_report(results):
    """生成维护报告"""
    print("\n" + "="*60)
    print("📋 生成维护报告...")
    print("="*60)
    
    report = f"""# NWACS 系统维护报告
{'='*60}
维护时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 1. 乱码修复

- 修复文件数: {len(results['encoding_fixes'])}
- 成功修复: {sum(1 for f in results['encoding_fixes'] if f['success'])}
- 修复失败: {sum(1 for f in results['encoding_fixes'] if not f['success'])}

## 2. 无用代码检测

- 检测到无用代码文件: {len(results['unused_code'])}
"""
    
    for item in results['unused_code']:
        report += f"\n### {item['file']}\n"
        for issue in item['issues']:
            report += f"- {issue}\n"
    
    report += f"""

## 3. Skill连通性

- Skill总数: {results['skill_connectivity'].get('total_skills', 0)}
- 孤立Skill: {len(results['skill_connectivity'].get('isolated_skills', []))}
"""
    
    if results['skill_connectivity'].get('isolated_skills'):
        report += "\n孤立Skill列表:\n"
        for skill in results['skill_connectivity']['isolated_skills']:
            report += f"- {skill}\n"
    
    report += f"""

## 4. 配置优化

- 状态: {'成功' if results['config_optimize']['success'] else '失败'}
- 消息: {results['config_optimize']['message']}

## 5. 文件清理

- 清理文件数: {results['cleanup']['cleaned']}
- 错误数: {len(results['cleanup']['errors'])}
"""
    
    if results['cleanup']['errors']:
        report += "\n清理错误:\n"
        for error in results['cleanup']['errors']:
            report += f"- {error}\n"
    
    report += f"""

{'='*60}
报告结束
"""
    
    # 保存报告
    os.makedirs('maintenance', exist_ok=True)
    report_path = f'maintenance/系统维护报告_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✅ 报告已保存: {report_path}")
    
    # 打印总结
    print("\n" + "="*60)
    print("🎉 系统维护完成！")
    print("="*60)
    print(f"\n📊 维护总结:")
    print(f"   🔍 乱码修复: {len(results['encoding_fixes'])} 个文件")
    print(f"   ⚠️  无用代码: {len(results['unused_code'])} 个文件")
    print(f"   🔗 Skill连通性: {results['skill_connectivity'].get('total_skills', 0)} 个Skill")
    print(f"   ⚙️  配置优化: {'成功' if results['config_optimize']['success'] else '失败'}")
    print(f"   🗑️  文件清理: {results['cleanup']['cleaned']} 个文件")
    print(f"\n📂 报告位置: {report_path}")

if __name__ == "__main__":
    main()
