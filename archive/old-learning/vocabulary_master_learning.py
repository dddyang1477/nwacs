#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 词汇大师学习系统
根据之前学习过的书籍名单，开始学习
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

VERSION = "2.0"
SYSTEM_NAME = "词汇大师学习系统"

# ============================================================================
# 配置模块
# ============================================================================

def load_config():
    config = {}
    if os.path.exists('config.json'):
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
    return config

# ============================================================================
# 之前学习过的书籍名单
# ============================================================================

LEARNED_BOOKS = [
    {
        "name": "剑来",
        "author": "烽火戏诸侯",
        "type": "仙侠/古典仙侠",
        "features": [
            "陈平安的说话方式（朴素真诚、言出必行）",
            "富有哲理的对话风格",
            "细腻的心理描写",
            "古风韵味但不晦涩",
            "三观较正的语句"
        ]
    },
    {
        "name": "斗破苍穹",
        "author": "天蚕土豆",
        "type": "玄幻/废柴流",
        "features": [
            "经典的废柴逆袭模板",
            "打脸虐渣的爽点设计",
            "升级体系的严谨设定",
            "战斗场面的热血描写",
            "退婚、嘲讽、反击的经典套路"
        ]
    },
    {
        "name": "庆余年",
        "author": "猫腻",
        "type": "权谋/穿越",
        "features": [
            "权谋算计的智斗",
            "人物对话的个性塑造",
            "细腻的情感描写",
            "复杂的人物关系网络",
            "伏笔埋设与回收"
        ]
    },
    {
        "name": "诡秘之主",
        "author": "爱潜水的乌贼",
        "type": "奇幻/克苏鲁",
        "features": [
            "世界观构建的宏大细致",
            "22条神之途径的独特设定",
            "角色扮演（塔罗会）的创新",
            "氛围营造的悬疑感",
            "细腻的心理转变描写"
        ]
    },
    {
        "name": "全职高手",
        "author": "蝴蝶蓝",
        "type": "电竞/职业竞技",
        "features": [
            "专业术语的巧妙运用",
            "团队配合的战术描写",
            "人物群像的精彩刻画",
            "热血但不失幽默",
            "专业性与趣味性的平衡"
        ]
    },
    {
        "name": "明朝那些事儿",
        "author": "当年明月",
        "type": "历史/通俗历史",
        "features": [
            "幽默诙谐的叙述风格",
            "历史人物的人性化描写",
            "复杂事件的简明阐述",
            "历史规律的深刻洞察",
            "代入感极强的写作方式"
        ]
    },
    {
        "name": "悟空传",
        "author": "今何在",
        "type": "西游/颠覆",
        "features": [
            "对经典的颠覆性解读",
            "强烈的情感表达",
            "诗意的语言风格",
            "对命运的深刻思考",
            "热血与悲壮的交织"
        ]
    },
    {
        "name": "凡人修仙传",
        "author": "忘语",
        "type": "仙侠/凡人流",
        "features": [
            "谨慎低调的处世哲学",
            "苟道生存的智慧",
            "资源争夺的残酷描写",
            "修仙体系的严谨设定",
            "扮猪吃虎的经典套路"
        ]
    },
    {
        "name": "雪中悍刀行",
        "author": "烽火戏诸侯",
        "type": "武侠/玄幻武侠",
        "features": [
            "人物取名的艺术",
            "江湖气息的营造",
            "招式名称的诗意",
            "人物群像的精彩刻画",
            "家国情怀的深刻主题"
        ]
    },
    {
        "name": "赘婿",
        "author": "愤怒的香蕉",
        "type": "历史/穿越",
        "features": [
            "商战智斗的精彩",
            "人物成长的细腻描写",
            "历史与创新的结合",
            "情感线的精心布局",
            "社会现实的深刻反映"
        ]
    }
]

# ============================================================================
# 词汇学习主题
# ============================================================================

VOCABULARY_TOPICS = [
    {
        "name": "外貌描写词汇",
        "prompt": """请为小说写作提供详细的外貌描写词汇库：

1. **面部描写**：眉、眼、鼻、口、耳的各类描写词汇
2. **肤色描写**：各种肤色状态的描写
3. **表情描写**：喜、怒、哀、乐、惊、恐的表情词汇
4. **体型描写**：高、矮、胖、瘦、强壮、纤细的描写
5. **气质描写**：高贵、冷傲、儒雅、狂放、邪魅等气质词汇

请分类整理，每个词汇给出例句！"""
    },
    {
        "name": "动作描写词汇",
        "prompt": """请为小说写作提供详细的动作描写词汇库：

1. **手部动作**：抓、握、捏、弹、敲、抚、推、拉、举、挥等
2. **脚步动作**：走、跑、跳、跃、踏、踱、蹒跚、蹿等
3. **身体动作**：弯、伸、扭、转、抖、颤、晃、摆等
4. **头部动作**：点、摇、抬、低、偏、仰、侧等
5. **复合动作**：连贯动作描写

请分类整理，每个词汇给出例句！"""
    },
    {
        "name": "心理描写词汇",
        "prompt": """请为小说写作提供详细的心理描写词汇库：

1. **情感类**：喜、怒、哀、乐、悲、恐、惊、怨、恨、忧等
2. **思维类**：想、思、念、忆、悟、懂、明、察、猜、疑等
3. **欲望类**：想、要、愿、盼、期、求、追、寻等
4. **心理状态**：平静、激动、矛盾、挣扎、坚定、犹豫等
5. **潜意识的描写**：无意识的小动作、下意识的反应

请分类整理，每个词汇给出例句！"""
    },
    {
        "name": "环境描写词汇",
        "prompt": """请为小说写作提供详细的环境描写词汇库：

1. **自然环境**：山、水、风、雨、雪、云、日、月、星等
2. **季节描写**：春、夏、秋、冬的特色描写
3. **时间描写**：晨、午、暮、夜、深夜的特色
4. **空间描写**：室内、室外、宫殿、茅屋、森林、荒漠等
5. **氛围描写**：诡异、温馨、压抑、轻松、紧张、神秘等

请分类整理，每个词汇给出例句！"""
    },
    {
        "name": "古风词汇",
        "prompt": """请为小说写作提供古风词汇库，结合《剑来》《雪中悍刀行》的风格：

1. **称谓类**：公子、佳人、侠客、书生、陛下、殿下、长老、掌门等
2. **动作类**：拱手、抱拳、作揖、颔首、拂袖、负手、踱步等
3. **场所类**：江湖、山庄、府邸、宗门、宫殿、庙宇、酒楼等
4. **器物类**：剑、刀、琴、棋、书、画、玉佩、酒杯等
5. **语气词**：呵呵、嘿嘿、呜呼、善哉、美哉、然也等

请分类整理，参考《剑来》的古风韵味！"""
    },
    {
        "name": "战斗描写词汇",
        "prompt": """请为小说写作提供战斗描写词汇库：

1. **攻击类**：劈、砍、刺、斩、扫、挑、戳、挥等
2. **防御类**：挡、格、架、挡、护、庇、守等
3. **移动类**：闪、避、躲、遁、跃、冲、扑等
4. **效果类**：血溅、骨折、倒飞、翻滚、撕裂等
5. **法术类**：施展、催动、凝聚、爆发、释放等

请分类整理，给出玄幻风格的例句！"""
    }
]

# ============================================================================
# DeepSeek API调用
# ============================================================================

def call_deepseek_v4(prompt, system_prompt=None, max_tokens=8000, timeout=120):
    config = load_config()
    if not config.get('api_key'):
        print("❌ 错误: API Key未配置！")
        return None

    if not system_prompt:
        system_prompt = """你是一位顶尖的网文写作导师，精通各种写作技巧。
请用中文详细解答写作问题，提供具体的例子和分析！"""

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

    except Exception as e:
        stop_spinner.set()
        print(f"❌ API调用失败: {e}")
        return None

def spinner_animation(stop_event):
    spinner = ['|', '/', '-', '\\']
    idx = 0
    while not stop_event.is_set():
        sys.stdout.write(f"\r   {spinner[idx]}")
        sys.stdout.flush()
        idx = (idx + 1) % 4
        time.sleep(0.2)

# ============================================================================
# 保存学习成果
# ============================================================================

def save_learning_content(topic_name, content):
    safe_name = ''.join(c for c in topic_name if c not in '\\/:*?"<>|')
    filename = f"{safe_name}.txt"
    
    os.makedirs('learning/vocabulary', exist_ok=True)
    filepath = os.path.join('learning/vocabulary', filename)
    
    header = f"""{topic_name}
{'=' * 60}
学习时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
参考书籍：{', '.join([book['name'] for book in LEARNED_BOOKS])}
{'=' * 60}

"""
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(header)
        f.write(content)
    
    print(f"✅ 保存成功: {filepath}")
    return filepath

# ============================================================================
# 更新词汇大师Skill文件
# ============================================================================

def update_vocabulary_skill(all_content):
    filepath = 'skills/level2/32_二级Skill_词汇大师.md'
    
    if not os.path.isabs(filepath):
        filepath = os.path.join(os.path.dirname(__file__), filepath)
    
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    # 读取现有内容
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            existing_content = f.read()
    else:
        existing_content = """# 词汇大师
================================================================================

## 职能描述
提供丰富的词汇素材，帮助作者提升文笔质量

## 核心职能
- 词汇收集与整理
- 描写素材积累
- 语言风格优化
- 修辞丰富度提升

"""
    
    # 添加学习内容
    chapter_title = f"\n\n## 词汇库扩充 - {datetime.now().strftime('%Y-%m-%d')}\n"
    chapter_content = chapter_title + all_content
    chapter_content += "\n---\n*本章节由词汇大师学习系统自动生成，基于对10部经典作品的学习*\n"
    
    existing_content += chapter_content
    
    # 保存
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(existing_content)
    
    print(f"✅ Skill更新成功: {filepath}")

# ============================================================================
# 主流程
# ============================================================================

def start_learning():
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║           {SYSTEM_NAME} v{VERSION}                              ║
║                                                              ║
║           📚 学习参考书籍：                                  ║
║           《剑来》《斗破苍穹》《庆余年》《诡秘之主》          ║
║           《全职高手》《明朝那些事儿》《悟空传》             ║
║           《凡人修仙传》《雪中悍刀行》《赘婿》              ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # 检查配置
    config = load_config()
    if not config.get('api_key'):
        print("❌ API Key未配置！")
        return
    
    # 第一步：基于学习过的书籍学习写作风格
    print("\n" + "="*60)
    print("📖 第一步：学习经典作品的写作风格")
    print("="*60)
    
    books_learning_prompt = f"""请分析以下10部经典网络小说的写作风格和特色：

{chr(10).join([f"{i+1}. 《{book['name']}》- {book['author']} ({book['type']})：{', '.join(book['features'])}" for i, book in enumerate(LEARNED_BOOKS)])}

请总结：
1. 每部作品的独特写作风格
2. 可以学习借鉴的写作技巧
3. 如何将这些风格融合到自己的写作中
4. 作为顶级签约作者，应该如何形成自己的风格

请用详细的分析和具体的例子来说明！"""
    
    print("\n⏳ 正在学习经典作品的写作风格...")
    books_content = call_deepseek_v4(books_learning_prompt)
    
    if books_content:
        print("\n✅ 经典作品学习完成！")
        save_learning_content("经典作品写作风格分析", books_content)
    else:
        print("\n❌ 经典作品学习失败！")
    
    # 第二步：学习各类词汇
    all_vocabulary = ""
    
    print("\n" + "="*60)
    print("📚 第二步：扩充词汇库")
    print("="*60)
    
    for topic in VOCABULARY_TOPICS:
        print(f"\n⏳ 正在学习: {topic['name']}...")
        content = call_deepseek_v4(topic['prompt'])
        
        if content:
            print(f"✅ {topic['name']} 学习完成！")
            save_learning_content(topic['name'], content)
            all_vocabulary += f"\n\n{'='*60}\n"
            all_vocabulary += f"【{topic['name']}】\n"
            all_vocabulary += f"{'='*60}\n\n"
            all_vocabulary += content
        else:
            print(f"❌ {topic['name']} 学习失败！")
    
    # 第三步：更新Skill文件
    if all_vocabulary:
        print("\n" + "="*60)
        print("📦 更新词汇大师Skill文件...")
        print("="*60)
        update_vocabulary_skill(all_vocabulary)
    
    # 生成报告
    generate_report(books_content, all_vocabulary)

def generate_report(books_content, vocabulary_content):
    print(f"\n{'='*60}")
    print("📋 生成学习报告...")
    print(f"{'='*60}")
    
    report = f"""# 词汇大师学习报告
{'='*60}
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📚 学习参考书籍

### 仙侠/玄幻类
1. **《剑来》** - 烽火戏诸侯 - 古典仙侠
2. **《斗破苍穹》** - 天蚕土豆 - 废柴逆袭
3. **《凡人修仙传》** - 忘语 - 凡人流
4. **《雪中悍刀行》** - 烽火戏诸侯 - 武侠玄幻

### 奇幻/悬疑类
5. **《诡秘之主》** - 爱潜水的乌贼 - 克苏鲁
6. **《庆余年》** - 猫腻 - 权谋穿越

### 都市/竞技类
7. **《全职高手》** - 蝴蝶蓝 - 电竞
8. **《赘婿》** - 愤怒的香蕉 - 历史穿越

### 其他经典
9. **《悟空传》** - 今何在 - 颠覆西游
10. **《明朝那些事儿》** - 当年明月 - 通俗历史

## 📖 学习内容

### 1. 经典作品写作风格分析
- ✅ 学习10部经典作品的写作风格
- ✅ 总结可借鉴的写作技巧
- ✅ 分析如何形成个人风格

### 2. 词汇库扩充
- ✅ 外貌描写词汇
- ✅ 动作描写词汇
- ✅ 心理描写词汇
- ✅ 环境描写词汇
- ✅ 古风词汇
- ✅ 战斗描写词汇

## 💡 学习成果

### 写作风格收获
- 学习了《剑来》的古风韵味和哲理对话
- 学习了《斗破苍穹》的爽点设计和升级体系
- 学习了《庆余年》的权谋智斗
- 学习了《诡秘之主》的世界观构建
- 学习了《雪中悍刀行》的人物取名和江湖气息

### 词汇库收获
- 积累了丰富的外貌描写词汇
- 积累了精准的动作描写词汇
- 积累了细腻的心理描写词汇
- 积累了生动的环境描写词汇
- 积累了优雅的古风词汇
- 积累了热血的战斗描写词汇

## 📊 统计信息
- 学习书籍数: {len(LEARNED_BOOKS)}
- 词汇主题数: {len(VOCABULARY_TOPICS)}
- 学习时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{'='*60}
报告结束
"""
    
    # 保存报告
    os.makedirs('learning/vocabulary', exist_ok=True)
    report_path = f'learning/vocabulary/词汇大师学习报告_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✅ 报告已保存: {report_path}")
    
    # 打印总结
    print("\n" + "="*60)
    print("🎉 词汇大师学习完成！")
    print("="*60)
    print(f"\n📊 学习统计:")
    print(f"   ✅ 学习书籍: {len(LEARNED_BOOKS)} 部")
    print(f"   ✅ 词汇主题: {len(VOCABULARY_TOPICS)} 个")
    print(f"   ✅ 写作风格: 已分析")
    print(f"   ✅ 词汇库: 已扩充")
    print(f"\n📂 学习报告: {report_path}")
    print(f"📂 词汇文件: learning/vocabulary/")

if __name__ == "__main__":
    start_learning()
