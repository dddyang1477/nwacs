#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS × DeepSeek V4 统一小说创作系统 - 优化版
✨ 加入画面影视感、读者带入感优化，解决卡住问题
"""

import os
import sys
import json
import urllib.request
import urllib.error
import time
import threading
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

VERSION = "3.0"
SYSTEM_NAME = "NWACS × DeepSeek V4"

# ============================================================================
# 配置模块
# ============================================================================

def load_config():
    config = {}
    if os.path.exists('config.json'):
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
    return config

def save_config(config):
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

# ============================================================================
# DeepSeek V4 写作手法优化模块
# ============================================================================

WRITING_TIPS = """【写作手法优化】
1. 画面影视感：
   - 运用镜头语言：远景（环境描写）、中景（人物动作）、特写（细节放大）
   - 多感官描写：视觉、听觉、嗅觉、触觉、味觉
   - 动态描写：不要静态画面，要写出流动感
   - 色彩运用：红、黑、金等色彩营造氛围

2. 读者带入感：
   -  POV视角切换：主角视角+关键配角视角
   - 内心描写：主角的心理活动要细腻
   - 对话风格：人物说话要有自己的特点
   - 情感共鸣：让读者感同身受

3. 节奏控制：
   - 300字小爽点，1000字大爽点
   - 每章结尾留悬念钩子
   - 张弛有度，战斗和日常交替

4. 细节刻画：
   - 微表情描写：眼神变化、嘴角弧度
   - 动作细节：手指动作、脚步移动
   - 环境烘托：天气、场景变化
"""

def get_enhanced_system_prompt():
    """获取增强的系统提示词"""
    return f"""你是一位顶尖玄幻网文大神，创作过《凡人修仙传》《仙逆》《遮天》等名著。

【核心写作原则】
1. 画面影视感：
   - 用镜头语言：远景（天地）→中景（人物）→特写（细节）
   - 多感官描写：视觉、听觉、嗅觉、触觉、味觉
   - 动态画面：写出流动感，不要静态描写
   - 色彩运用：用红、黑、金、紫等色营造氛围

2. 读者带入感：
   - POV视角：深入主角内心，细腻的心理活动
   - 对话风格：每个角色说话要有自己的特点
   - 情感共鸣：让读者感同身受，喜怒哀乐都能传递
   - 细节真实：微表情、小动作、场景变化都要写

3. 节奏控制：
   - 300字小爽点，1000字大爽点
   - 每章结尾必须留悬念钩子
   - 张弛有度：战斗场面和日常场景交替

4. 创新设定：
   - 不要用老套路（废柴流、戒指老爷爷等）
   - 苟道流：谨慎小心，不暴露底牌
   - 黑暗流：世界残酷，主角心狠
   - 智斗流：以弱胜强，靠智慧布局

【写作要求】
每章约3000字，不水文，每句话都要有信息量。
{WRITING_TIPS}
"""

# ============================================================================
# DeepSeek API 调用模块（优化版）
# ============================================================================

def call_deepseek_v4(prompt, system_prompt=None, max_tokens=6000, timeout=120):
    """调用DeepSeek V4 API（优化版，解决卡住问题）"""
    config = load_config()
    if not config.get('api_key'):
        print("❌ 错误: API Key未配置！")
        return None

    if not system_prompt:
        system_prompt = get_enhanced_system_prompt()

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

    print(f"\n⏳ 正在调用DeepSeek V4...")
    print(f"   预计等待时间: {timeout/60:.1f}分钟")
    print(f"   正在生成内容，请稍候...")

    # 显示进度动画的线程
    stop_spinner = threading.Event()
    spinner_thread = threading.Thread(target=spinner_animation, args=(stop_spinner,))
    spinner_thread.daemon = True
    spinner_thread.start()

    try:
        req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method='POST')

        with urllib.request.urlopen(req, timeout=timeout) as response:
            stop_spinner.set()
            result = json.loads(response.read().decode('utf-8'))
            print(f"✅ API调用成功！")
            return result['choices'][0]['message']['content']

    except urllib.error.HTTPError as e:
        stop_spinner.set()
        print(f"❌ HTTP错误: {e.code} - {e.reason}")
        if e.code == 429:
            print("   ⚠️  请求过于频繁，请稍后重试")
        elif e.code == 402:
            print("   ⚠️  API余额不足，请充值")
        return None
    except urllib.error.URLError as e:
        stop_spinner.set()
        print(f"❌ URL错误: {e.reason}")
        print("   ⚠️  网络连接问题，请检查网络")
        return None
    except Exception as e:
        stop_spinner.set()
        print(f"❌ API调用失败: {e}")
        return None

def spinner_animation(stop_event):
    """显示旋转动画"""
    spinner = ['|', '/', '-', '\\']
    idx = 0
    while not stop_event.is_set():
        sys.stdout.write(f"\r   {spinner[idx]}")
        sys.stdout.flush()
        idx = (idx + 1) % 4
        time.sleep(0.2)

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
        f.write("NWACS提供框架与大纲\n")
        f.write("DeepSeek弥补内容创作缺陷\n")
    
    print(f"\n✅ 已保存: {filepath}")
    return filepath

# ============================================================================
# 清理模块
# ============================================================================

def clean_old_files():
    """清理旧文件"""
    import glob
    
    print("\n🧹 清理临时文件...")
    
    temp_files = [
        'test_*.py',
        'temp_*.py',
        'debug_*.py',
        '__pycache__',
        '*.pyc',
    ]
    
    cleaned_count = 0
    for pattern in temp_files:
        if '*' in pattern:
            for filepath in glob.glob(pattern):
                try:
                    if os.path.isdir(filepath):
                        import shutil
                        shutil.rmtree(filepath)
                    else:
                        os.remove(filepath)
                    print(f"  ✓ 已清理: {filepath}")
                    cleaned_count += 1
                except Exception:
                    pass
        elif os.path.isdir(pattern):
            try:
                import shutil
                shutil.rmtree(pattern)
                print(f"  ✓ 已清理目录: {pattern}")
                cleaned_count += 1
            except Exception:
                pass
    
    print(f"✅ 清理完成！共清理 {cleaned_count} 个文件")

# ============================================================================
# 功能模块
# ============================================================================

def show_menu():
    """显示主菜单"""
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║            {SYSTEM_NAME} 统一创作系统 v{VERSION}              ║
║              ✨ 画面影视感 + 读者带入感                      ║
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
        print(f"\n✨ 写作优化:")
        print(f"   ✓ 画面影视感: 镜头语言 + 多感官描写")
        print(f"   ✓ 读者带入感: POV视角 + 内心描写")
        print(f"   ✓ 节奏控制: 300字小爽点 + 每章悬念")
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

【画面影视感】
- 大陆描写：用远景镜头展示宏大世界
- 城市描写：用中景+特写展示繁华城市
- 战斗描写：用慢镜头+特写展示战斗细节

【读者带入感】
- 主角设定：让读者能代入，引起共鸣
- 感情描写：细腻的情感描写
- 配角塑造：每个配角都有自己的故事

请详细生成：
1. 书名（5个候选）
2. 世界观（4块大陆体系）
3. 修炼体系（炼气→渡劫→飞升，6种辅助修炼）
4. 门派势力（三大古派、七大宗、三十六门派）
5. 主角设定（性格、金手指、外貌）
6. 女主设定（4位女主详细设定）
7. 主线剧情（100万字分4卷）
8. 前30章详细大纲

请详细输出！"""
    
    content = call_deepseek_v4(prompt, max_tokens=8000)
    if content:
        novel_name = "长生仙逆从苟道毒修开始"
        save_to_txt(novel_name, content, "大纲")
        print("✅ 大纲生成完成！")

def generate_first_10_chapters():
    """生成前10章"""
    print("\n📖 正在生成前10章内容...")
    print("   (约30000字，每章3000字，画面影视感 + 读者带入感)")
    
    prompt = """请为小说《长生仙逆：从苟道毒修开始》创作前10章完整内容。

【主角设定】
- 林玄：炼气期修士，在废丹窑监守
- 金手指：融合天道碎片，成为"命运之外的人"
- 性格：谨慎小心，苟道流，不暴露底牌

【写作要求】
【画面影视感】
- 镜头语言：远景（天地）→中景（人物）→特写（细节）
- 多感官描写：视觉、听觉、嗅觉、触觉、味觉都要有
- 动态描写：不要静态画面，要写出流动感
- 色彩运用：用红、黑、金、紫等色彩营造氛围

【读者带入感】
- POV视角：深入林玄内心，细腻的心理活动
- 对话风格：每个角色说话要有自己的特点
- 情感共鸣：让读者感同身受

【节奏控制】
- 每章约3000字
- 300字一小爽点，1000字一大爽点
- 每章结尾必须留悬念钩子

请创作前10章：
第1章：毒窟少年，天道碎片
第2章：苟道十戒，毒丹初炼
第3章：杂毒丹成，鱼目混珠
第4-10章：继续林玄的成长之路"""
    
    content = call_deepseek_v4(prompt, max_tokens=8000, timeout=180)
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

【写作要求】
【画面影视感】
- 镜头语言：远景（天地）→中景（人物）→特写（细节）
- 多感官描写：视觉、听觉、嗅觉、触觉、味觉
- 动态描写：不要静态画面，要写出流动感

【读者带入感】
- POV视角：深入主角内心
- 对话风格：每个角色说话要有自己的特点
- 情感共鸣：让读者感同身受

【节奏控制】
- 每章约3000字
- 300字小爽点，1000字大爽点
- 每章结尾留悬念

请开始创作！"""
    
    content = call_deepseek_v4(prompt, max_tokens=8000, timeout=180)
    if content:
        save_to_txt(novel_name, content, chapter_range)
        print(f"✅ {chapter_range}生成完成！")

def generate_innovative_novel():
    """生成创新设定小说"""
    print("\n✨ 正在生成创新设定小说...")
    print("   (反套路，不走废柴流老爷爷戒指的套路)")
    
    prompt = """请为修仙玄幻小说生成创新设定的大纲和前5章内容。

【核心要求】
- 不走老套路：不要废柴流、不要戒指老爷爷
- 创新设定：要有新意，让人眼前一亮
- 画面影视感：镜头语言、多感官描写
- 读者带入感：POV视角、情感共鸣

【可选创新方向】
1. 美食修仙：吃遍天下美食，提升修为
2. 卡牌修仙：收集卡牌，进行卡牌对战
3. 梦境修仙：在梦中修炼，时间加速
4. 契约修仙：与各种灵兽签订契约
5. 反派修仙：穿越成反派，知道剧情走向

请详细创作完整大纲+前5章内容！"""
    
    content = call_deepseek_v4(prompt, max_tokens=8000, timeout=180)
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
║           统一小说创作系统 v{VERSION}                           ║
║           ✨ 画面影视感 + 读者带入感优化                    ║
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
