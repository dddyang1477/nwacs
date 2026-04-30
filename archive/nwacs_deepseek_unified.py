#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS × DeepSeek V4 统一小说创作系统
整合所有功能，一站式服务
"""

import os
import sys
import json
import urllib.request
import urllib.error
import time
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

VERSION = "2.0"
SYSTEM_NAME = "NWACS × DeepSeek V4"

# ============================================================================
# 配置模块
# ============================================================================

def load_config():
    """加载配置"""
    config = {}
    if os.path.exists('config.json'):
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
    return config

def save_config(config):
    """保存配置"""
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

# ============================================================================
# DeepSeek API 调用模块
# ============================================================================

def call_deepseek_v4(prompt, system_prompt=None, max_tokens=6000):
    """调用DeepSeek V4 API"""
    config = load_config()
    if not config.get('api_key'):
        print("❌ 错误: API Key未配置！")
        return None

    if not system_prompt:
        system_prompt = """你是一位顶尖玄幻网文大神，擅长苟道流、黑暗流、智斗流。
创作的小说节奏紧凑、爽点密集、画面感强、悬念钩子、不水文。"""

    url = config.get('base_url', 'https://api.deepseek.com/v1') + '/chat/completions'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {config.get("api_key")}'
    }

    data = {
        'model': config.get('model', 'deepseek-v4-pro'),
        'messages': [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': prompt}
        ],
        'temperature': 0.8,
        'max_tokens': max_tokens
    }

    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method='POST')

    try:
        with urllib.request.urlopen(req, timeout=180) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result['choices'][0]['message']['content']
    except Exception as e:
        print(f"❌ API错误: {e}")
        return None

# ============================================================================
# 文件保存模块
# ============================================================================

def save_to_txt(novel_name, content, chapter_range=""):
    """保存为TXT格式"""
    safe_name = ''.join(c for c in novel_name if c not in '\\/:*?"<>|')
    
    if chapter_range:
        filename = f"{safe_name}_{chapter_range}.txt"
    else:
        filename = f"{safe_name}.txt"
    
    os.makedirs('output', exist_ok=True)
    filepath = os.path.join('output', filename)
    
    header = f"""{novel_name}
{'=' * 60}
修仙玄幻·苟道流·黑暗流·智斗流
生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'=' * 60}

"""
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(header)
        f.write(content)
        f.write(f"\n\n{'=' * 60}\n")
        f.write("本小说由 NWACS × DeepSeek V4 联合创作\n")
    
    print(f"✅ 已保存: {filepath}")
    return filepath

# ============================================================================
# 清理模块
# ============================================================================

def clean_old_files():
    """清理旧文件"""
    import glob
    
    temp_files = [
        'test_*.py',
        'temp_*.py',
        '__pycache__',
    ]
    
    print("\n🧹 清理临时文件...")
    for pattern in temp_files:
        for filepath in glob.glob(pattern):
            try:
                if os.path.isdir(filepath):
                    import shutil
                    shutil.rmtree(filepath)
                else:
                    os.remove(filepath)
                print(f"  ✓ 已清理: {filepath}")
            except Exception:
                pass
    
    print("✅ 清理完成！")

# ============================================================================
# 功能模块
# ============================================================================

def show_menu():
    """显示主菜单"""
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║            {SYSTEM_NAME} 统一创作系统 v{VERSION}              ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  【小说创作】                                                 ║
║                                                              ║
║    1. 生成玄幻小说大纲（100万字）                              ║
║    2. 生成前10章内容                                          ║
║    3. 生成自定义章节                                          ║
║    4. 生成创新设定小说                                        ║
║                                                              ║
║  【系统工具】                                                 ║
║                                                              ║
║    5. 清理旧文件                                              ║
║    6. 检查API配置                                             ║
║    7. 配置DeepSeek                                            ║
║                                                              ║
║  【其他】                                                     ║
║                                                              ║
║    0. 退出                                                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)

def check_api_config():
    """检查API配置"""
    config = load_config()
    
    print("\n📋 API配置检查")
    print("=" * 60)
    
    if config.get('api_key'):
        print(f"✅ API Key: 已配置")
        print(f"   模型: {config.get('model', 'deepseek-v4-pro')}")
        print(f"   状态: {config.get('enabled', True)}")
    else:
        print("❌ API Key: 未配置")
        print("   请先运行选项7进行配置")

def config_deepseek():
    """配置DeepSeek"""
    print("\n⚙️ DeepSeek配置")
    print("=" * 60)
    
    config = load_config()
    
    api_key = input("请输入API Key (直接回车跳过): ").strip()
    if api_key:
        config['api_key'] = api_key
    
    model = input("请输入模型名称 [deepseek-v4-pro] (直接回车使用默认): ").strip()
    if model:
        config['model'] = model
    else:
        config['model'] = 'deepseek-v4-pro'
    
    save_config(config)
    print("✅ 配置已保存！")

def generate_outline():
    """生成小说大纲"""
    print("\n📝 正在生成玄幻小说大纲...")
    print("   (100万字完整大纲，包含世界观、修炼体系、人物设定等)")
    
    prompt = """请为修仙玄幻小说生成完整大纲，要求：
- 书名：苟道流风格
- 世界观：4块大陆体系
- 修炼体系：炼气→渡劫→飞升，6种辅助修炼
- 门派：三大古派、七大宗、三十六门派
- 主角设定：金手指、性格特点
- 女主设定：4位女主详细设定
- 主线剧情：100万字分4卷
- 前30章大纲

请详细输出完整大纲！"""
    
    content = call_deepseek_v4(prompt)
    if content:
        novel_name = "长生仙逆从苟道毒修开始"
        save_to_txt(novel_name, content, "大纲")
        print("✅ 大纲生成完成！")

def generate_first_10_chapters():
    """生成前10章"""
    print("\n📖 正在生成前10章内容...")
    print("   (约30000字，每章3000字)")
    
    prompt = """请为小说《长生仙逆：从苟道毒修开始》创作前10章完整内容。

主角：林玄，炼气期修士，在废丹窑监守，融合天道碎片成为"命运之外的人"

第1章：毒窟少年，天道碎片
- 林玄在废丹窑监守三年，发现天道碎片
- 成为"命运之外的人"，制定苟道十戒
- 发现宗门与魔道勾结贩卖凡人

第2章：苟道十戒，毒丹初炼
- 炼制隐气丹隐藏修为
- 暗中布局收集情报

第3章：杂毒丹成，鱼目混珠
- 用毒丹对付敌人
- 发现上任长老被灭口的真相

第4-10章：
- 继续林玄的苟道成长之路
- 获得毒龙传承
- 遇到神秘女子苏清
- 情节要紧凑，每章留悬念

每章约3000字，300字一小爽点，1000字一大爽点！"""
    
    content = call_deepseek_v4(prompt, max_tokens=8000)
    if content:
        novel_name = "长生仙逆从苟道毒修开始"
        save_to_txt(novel_name, content, "1-10章")
        print("✅ 前10章生成完成！")

def generate_custom_chapters():
    """生成自定义章节"""
    print("\n🎯 生成自定义章节")
    print("=" * 60)
    
    novel_name = input("请输入小说名称: ").strip() or "自定义小说"
    start = input("请输入起始章节: ").strip() or "1"
    end = input("请输入结束章节: ").strip() or "5"
    
    chapter_range = f"第{start}-{end}章"
    print(f"\n📖 正在生成 {chapter_range}...")
    
    prompt = f"""请为小说《{novel_name}》创作第{start}-{end}章内容。

要求：
- 每章约3000字
- 300字一小爽点，1000字一大爽点
- 每章结尾留悬念
- 情节紧凑，不水文

请开始创作！"""
    
    content = call_deepseek_v4(prompt, max_tokens=8000)
    if content:
        save_to_txt(novel_name, content, chapter_range)
        print(f"✅ {chapter_range}生成完成！")

def generate_innovative_novel():
    """生成创新设定小说"""
    print("\n✨ 正在生成创新设定小说...")
    print("   (反套路，不走废柴流老爷爷戒指的套路)")
    
    prompt = """请为修仙玄幻小说生成创新设定的大纲和前5章内容。

要求：
1. 主角不是废柴，不走老套路
2. 金手指要创新（不是戒指老爷爷）
3. 修炼体系要创新
4. 世界观要有趣
5. 生成完整大纲+前5章内容

可选创新方向：
- 美食修仙：吃遍天下提升修为
- 卡牌修仙：收集卡牌战斗
- 梦境修仙：在梦中修炼时间加速
- 契约修仙：与灵兽签订契约
- 反派修仙：穿越成反派知道剧情

请详细创作！"""
    
    content = call_deepseek_v4(prompt, max_tokens=8000)
    if content:
        novel_name = "创新修仙设定"
        save_to_txt(novel_name, content, "完整版")
        print("✅ 创新小说生成完成！")

# ============================================================================
# 主程序
# ============================================================================

def main():
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║           {SYSTEM_NAME}                                      ║
║           统一小说创作系统                                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    while True:
        show_menu()
        choice = input("请输入选项编号: ").strip()
        
        if choice == '1':
            generate_outline()
        elif choice == '2':
            generate_first_10_chapters()
        elif choice == '3':
            generate_custom_chapters()
        elif choice == '4':
            generate_innovative_novel()
        elif choice == '5':
            clean_old_files()
        elif choice == '6':
            check_api_config()
        elif choice == '7':
            config_deepseek()
        elif choice == '0':
            print("\n感谢使用！再见！👋\n")
            break
        else:
            print("\n❌ 无效选项，请重新输入！")
        
        input("\n按回车继续...")

if __name__ == "__main__":
    main()
