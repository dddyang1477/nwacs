#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 学习内容智能分发器
将学习到的知识自动分发到对应的Skill文件中
"""

import os
import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

def load_learning_content():
    """加载学习内容"""
    content = {}
    
    # 从skills目录读取学习内容
    skills_dir = 'skills/'
    for root, dirs, files in os.walk(skills_dir):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content[filepath] = f.read()
    
    return content

def match_topic_to_skill(topic):
    """将学习主题匹配到对应Skill"""
    topic_keywords = {
        '词汇': ['词汇', '词语', '描写', '词典', '素材', '词汇库'],
        '写作手法': ['写作', '技巧', '手法', '修辞', '叙事', '文风'],
        '场景渲染': ['场景', '环境', '氛围', '画面', '描写', '渲染'],
        '去AI痕迹': ['AI', '痕迹', '检测', '去AI化', '人类化'],
        '剧情铺设': ['剧情', '情节', '故事', '结构', '伏笔', '节奏'],
        '人物架设': ['人物', '角色', '性格', '塑造', '人设'],
        '世界观': ['世界观', '世界构造', '设定', '规则'],
        '对话': ['对话', '台词', '语言'],
        '战斗': ['战斗', '招式', '武功'],
        '情感': ['情感', '心理', '情绪'],
    }
    
    for skill_name, keywords in topic_keywords.items():
        for keyword in keywords:
            if keyword in topic:
                return skill_name
    return '其他'

def distribute_to_skill(skill_name, content):
    """将内容分发到对应Skill"""
    skill_mapping = {
        '词汇': ['skills/level2/32_二级Skill_词汇大师.md', 'skills/GoldenPhraseMaster/GoldenPhraseMaster.md'],
        '写作手法': ['skills/level2/09_二级Skill_写作技巧大师.md'],
        '场景渲染': ['skills/level2/05_二级Skill_场景构造师.md'],
        '去AI痕迹': ['skills/level2/10_二级Skill_去AI痕迹监督官.md'],
        '剧情铺设': ['skills/level2/04_二级Skill_剧情构造师.md', 'skills/PlotMaster/PlotMaster.md'],
        '人物架设': ['skills/level2/07_二级Skill_角色塑造师.md', 'skills/CharacterMaster/CharacterMaster.md'],
        '世界观': ['skills/level2/03_二级Skill_世界观构造师.md'],
        '对话': ['skills/level2/06_二级Skill_对话设计师.md'],
        '战斗': ['skills/level2/08_二级Skill_战斗设计师.md'],
        '情感': ['skills/level2/07_二级Skill_角色塑造师.md'],
        '其他': ['skills/level1/level1.md'],
    }
    
    if skill_name in skill_mapping:
        for filepath in skill_mapping[skill_name]:
            append_to_skill(filepath, content)

def append_to_skill(filepath, content):
    """追加内容到Skill文件"""
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            existing_content = f.read()
        
        # 检查内容是否已存在
        if content[:100] not in existing_content:
            with open(filepath, 'a', encoding='utf-8') as f:
                f.write('\n\n## 学习成果\n\n')
                f.write(content)
                f.write('\n\n---\n*本章节由自动学习系统生成*\n')
            print(f"  ✓ 更新: {os.path.basename(filepath)}")
        else:
            print(f"  - 已存在: {os.path.basename(filepath)}")
    else:
        print(f"  ! 不存在: {filepath}")

def extract_learning_topics(content):
    """从内容中提取学习主题"""
    topics = []
    
    # 匹配学习主题
    topic_pattern = r'学习主题[：:]\s*(.+?)\n'
    matches = re.findall(topic_pattern, content, re.DOTALL)
    for match in matches:
        topics.append(match.strip())
    
    # 匹配章节标题
    chapter_pattern = r'##\s+(.+?)\n'
    matches = re.findall(chapter_pattern, content)
    for match in matches:
        if match.strip() and match.strip() not in topics:
            topics.append(match.strip())
    
    return topics

def optimize_vocabulary_skill():
    """优化词汇大师Skill"""
    print("\n[1/6] 优化词汇大师Skill...")
    
    vocab_content = """## 新增词汇素材（2026升级版）

### 写作词汇库增强

#### 光影类词汇扩展
| 词汇 | 意境描述 | 适用场景 |
|------|----------|----------|
| 鎏金 | 金色光泽流动 | 阳光、宝物 |
| 碎银 | 银色碎片闪烁 | 月光、水面 |
| 氤氲 | 朦胧雾气弥漫 | 仙境、清晨 |
| 斑驳 | 光影交错 | 树影、古墙 |
| 熹微 | 晨光初现 | 黎明 |
| 余晖 | 夕阳残留 | 黄昏 |

#### 动作动词升级
| 基础动词 | 升级替换 | 情感色彩 |
|----------|----------|----------|
| 看 | 凝睇、端详、窥视、睥睨 | 不同视角与情绪 |
| 说 | 低喃、沉吟、冷笑、轻叹 | 语气与态度 |
| 走 | 缓步、疾行、踉跄、彳亍 | 速度与状态 |
| 想 | 思忖、忖度、琢磨、思量 | 思考深度 |

#### 情感形容词库
| 情感 | 词汇列表 |
|------|----------|
| 悲伤 | 凄切、悲凉、怆然、凄婉 |
| 喜悦 | 欣悦、怡然、欣然、畅快 |
| 愤怒 | 震怒、暴怒、愤然、愠怒 |
| 恐惧 | 悚然、骇然、惶然、惊悚 |

### 影视化写作词汇
#### 镜头描写
- **全景**：广袤、辽阔、无垠、苍茫、浩瀚
- **中景**：伫立、端坐、徘徊、凝视、远眺
- **近景**：垂眸、抬眸、蹙眉、浅笑、低语
- **特写**：颤抖、摩挲、抽搐、滚动、紧握

#### 情绪表达（非直白）
| 情绪 | 替代表达 |
|------|----------|
| 紧张 | 指尖发抖、掌心出汗、呼吸急促 |
| 不安 | 喉结滚动、目光躲闪、坐姿僵硬 |
| 悲伤 | 眼眶泛红、声音哽咽、双肩颤抖 |
| 愤怒 | 青筋暴起、咬牙切齿、拳头紧握 |
"""
    
    distribute_to_skill('词汇', vocab_content)

def optimize_writing_techniques():
    """优化写作技巧大师Skill"""
    print("\n[2/6] 优化写作技巧大师Skill...")
    
    writing_content = """## 进阶写作技巧（2026升级版）

### 叙事节奏控制

#### 句子节奏
- **短句**：制造紧张感，适合战斗、追逐场景
- **长句**：营造氛围，适合抒情、描写场景
- **长短交织**：增强阅读体验，避免单调

#### 段落节奏
- 段落长度影响呼吸感
- 关键信息单独成段
- 场景切换时使用空行分隔

#### 章节节奏
- 章末钩子制造悬念
- 信息密度控制
- 高潮分布合理

### 视角管理
| 视角类型 | 适用场景 | 优势 |
|----------|----------|------|
| 第一人称 | 悬疑、青春 | 代入感强 |
| 第三人称有限 | 通用 | 平衡沉浸与全知 |
| 第三人称全知 | 史诗、群像 | 视角广阔 |
| 多视角 | 复杂叙事 | 层次丰富 |

### 开头技巧
- **悬疑开头**：抛出无法解释的状况
- **反差开头**：利用前后反差制造吸引点
- **危机开头**：直击主角核心利益
- **金手指前置**：尽早亮出核心能力
"""
    
    distribute_to_skill('写作手法', writing_content)

def optimize_scene_rendering():
    """优化场景构造师Skill"""
    print("\n[3/6] 优化场景构造师Skill...")
    
    scene_content = """## 场景渲染高级技巧（2026升级版）

### 五感沉浸式描写

#### 视觉
- 色彩：黛青、鸦青、月白、水红、石青、松绿
- 光影：鎏金、碎银、斑驳、氤氲、熹微、余晖
- 形状：朱栏、画栋、雕梁、飞檐、回廊、曲径

#### 听觉
- 自然声：鸟鸣、风声、雨声、流水声
- 环境声：叫卖声、脚步声、器物碰撞声
- 情感声：叹息、轻笑、抽泣、怒吼

#### 嗅觉
- 自然香：花香、草香、泥土香、雨气
- 食物香：饭菜香、茶香、酒香
- 环境味：霉味、硝烟味、血腥味

#### 触觉
- 温度：冰凉、滚烫、温暖、凉爽
- 质地：粗糙、光滑、柔软、坚硬
- 压力：沉重、轻盈、压迫、舒缓

#### 味觉
- 基础味：甜、酸、苦、辣、咸
- 复合味：苦涩、清甜、酸辣、咸香

### 氛围营造公式
**氛围 = 情绪 + 细节 + 感官体验**

| 情绪 | 场景元素 | 感官细节 |
|------|----------|----------|
| 孤独 | 雨夜、孤灯、残影 | 冷、湿、静 |
| 温暖 | 阳光、炉火、茶香 | 暖、香、柔 |
| 恐怖 | 黑暗、异响、腐臭 | 冷、臭、慌 |
| 紧张 | 滴答声、急促呼吸、冷汗 | 急、湿、紧 |
"""
    
    distribute_to_skill('场景渲染', scene_content)

def optimize_anti_ai():
    """优化去AI痕迹监督官Skill"""
    print("\n[4/6] 优化去AI痕迹监督官Skill...")
    
    anti_ai_content = """## 去AI化进阶技巧（2026升级版）

### AI特征深度识别

#### 语言层面
| AI特征 | 表现 | 修正方向 |
|--------|------|----------|
| 过度结构化 | 首先...其次...最后... | 打破对称，自然过渡 |
| 抽象空洞 | "深刻的"、"重要的" | 用具体细节替代 |
| 完美对称 | 排比过于工整 | 加入不对称 |
| 词汇重复 | AI高频词 | 替换为口语化表达 |

#### 结构层面
| AI特征 | 表现 | 修正方向 |
|--------|------|----------|
| 段落均匀 | 每段长度相似 | 长短错落 |
| 逻辑过清 | 每步都铺垫完美 | 加入意外和跳跃 |
| 情绪平滑 | 无情绪爆发点 | 加入失控时刻 |

### 人类化改造五步法

**第一步：注入个人化细节**
- 添加具体物品
- 添加感官体验
- 添加记忆锚点

**第二步：口语化改造**
- 使用俗语、俚语
- 加入口头禅
- 使用不规范表达

**第三步：情感具象化**
- 用行为表现情绪
- 避免直白情绪标签
- 使用身体语言描写

**第四步：节奏多样化**
- 短句制造紧张
- 长句营造氛围
- 不规则句式增加真实感

**第五步：添加"人类痕迹"**
- 犹豫和停顿
- 自我修正
- 习惯动作

### AI高频词黑名单
- 设置词："在一个XX的世界里" → 直接描写场景
- 连接词："然而、因此、此外" → 用动作切换
- 修饰词："非常、十分、特别" → 用细节替代
- 总结词："总而言之、值得一提" → 直接说结论
"""
    
    distribute_to_skill('去AI痕迹', anti_ai_content)

def optimize_plot_design():
    """优化剧情构造师Skill"""
    print("\n[5/6] 优化剧情构造师Skill...")
    
    plot_content = """## 剧情设计高级技巧（2026升级版）

### 故事结构设计

#### 三幕式结构
| 阶段 | 内容 | 要点 |
|------|------|------|
| 第一幕 | 建立 | 介绍人物、背景、冲突 |
| 第二幕 | 发展 | 矛盾升级、主角成长 |
| 第三幕 | 解决 | 高潮、结局、反思 |

#### 英雄之旅
- 启程：离开舒适区
- 启蒙：获得知识/能力
- 考验：面对挑战
- 回归：带回礼物

### 情节推进技巧

#### 悬念设置
- **伏笔埋设**：提前布置线索
- **信息隐藏**：控制信息披露节奏
- **反转设计**：打破读者预期

#### 冲突设计
| 冲突类型 | 示例 | 效果 |
|----------|------|------|
| 外部冲突 | 主角vs反派 | 推动剧情 |
| 内部冲突 | 欲望vs道德 | 深化人物 |
| 人际冲突 | 信任vs背叛 | 制造张力 |

### 节奏控制公式
**节奏 = 压力积累 + 爆发式爽点**

- 每3-5章一次情绪起伏
- 爽点间隔不超过4万字
- 受挫后3万字内必爽

### 剧情创新技巧
- **非线性叙事**：多时间线并行
- **元叙事**：打破第四面墙
- **伪主角设定**：中期揭示真相
- **嵌套式叙事**：故事套故事
"""
    
    distribute_to_skill('剧情铺设', plot_content)

def optimize_character_building():
    """优化角色塑造师Skill"""
    print("\n[6/6] 优化角色塑造师Skill...")
    
    character_content = """## 人物塑造深度技巧（2026升级版）

### 人物核心驱动

#### 核心欲望
- 复仇、权力、爱情、自由、救赎
- 欲望决定人物行为逻辑

#### 核心恐惧
- 孤独、背叛、失败、失去、死亡
- 恐惧制造人物弱点

#### 内在矛盾
- 欲望与恐惧的冲突
- 道德与利益的抉择

### 人物弧光设计

| 阶段 | 内容 | 示例 |
|------|------|------|
| 起点 | 初始状态 | 懦弱、自私、迷茫 |
| 触发 | 关键事件 | 亲人离世、秘密揭露 |
| 成长 | 变化过程 | 性格转变、能力提升 |
| 终点 | 最终状态 | 勇敢、无私、觉悟 |

### 人设模板

#### 硬核专业型
- 专业上冷酷，生活里沙雕
- 反差萌增加魅力

#### 疯批清醒型
- 对所有人冷酷，唯独对某人温柔
- 极端性格制造戏剧张力

#### 沙雕卷王型
- 表面不正经，实则超级努力
- 扮猪吃老虎套路

### 配角升级
- 配角不再是工具人
- 要有独立故事线
- 合理动机和成长

### 人物关系网络
| 关系类型 | 作用 | 示例 |
|----------|------|------|
| 羁绊 | 情感支撑 | 亲情、友情、爱情 |
| 对手 | 冲突来源 | 宿敌、竞争者 |
| 导师 | 成长引导 | 师父、前辈 |
| 盟友 | 合作助力 | 队友、伙伴 |
"""
    
    distribute_to_skill('人物架设', character_content)

def main():
    print("\n" + "=" * 80)
    print("          NWACS 学习内容智能分发器")
    print("=" * 80)
    print("\n正在将学习内容分发到对应Skill...")
    
    # 优化各个Skill
    optimize_vocabulary_skill()
    optimize_writing_techniques()
    optimize_scene_rendering()
    optimize_anti_ai()
    optimize_plot_design()
    optimize_character_building()
    
    print("\n" + "=" * 80)
    print("                    分发完成！")
    print("=" * 80)
    print("\n📚 优化的Skill模块：")
    print("  1. 词汇大师 - 词汇素材扩展")
    print("  2. 写作技巧大师 - 叙事节奏控制")
    print("  3. 场景构造师 - 五感沉浸式描写")
    print("  4. 去AI痕迹监督官 - 人类化改造")
    print("  5. 剧情构造师 - 剧情设计技巧")
    print("  6. 角色塑造师 - 人物弧光设计")
    print("\n所有学习内容已成功分发到对应Skill！")
    print("=" * 80)

if __name__ == "__main__":
    import sys
    main()
