#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS Skills文件夹重组脚本
按等级/功能重新排序，消除编号混乱
"""

import os
import shutil

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(BASE, "skills")

def safe_makedirs(path):
    os.makedirs(path, exist_ok=True)

def safe_move(src, dst):
    if os.path.exists(src):
        if os.path.exists(dst):
            print(f"  ⚠️ 目标已存在，跳过: {dst}")
            return False
        shutil.move(src, dst)
        print(f"  ✅ {os.path.basename(src)} -> {os.path.basename(dst)}")
        return True
    else:
        print(f"  ❌ 源文件不存在: {src}")
        return False

def main():
    print("=" * 70)
    print("NWACS Skills 文件夹重组")
    print("=" * 70)

    # ============================================================
    # 1. 创建新目录结构
    # ============================================================
    print("\n[1] 创建新目录结构...")
    
    dirs = [
        "skills/level1",
        "skills/level2/learnings",
        "skills/level3",
        "skills/masters",
        "skills/scripts",
        "skills/references",
        "skills/archive/backups",
        "skills/archive/upgrades",
    ]
    for d in dirs:
        safe_makedirs(os.path.join(BASE, d))
        print(f"  📁 {d}")

    # ============================================================
    # 2. 整理 level1 (一级Skill)
    # ============================================================
    print("\n[2] 整理 level1...")
    
    level1_src = os.path.join(SKILLS, "level1")
    level1_dst = os.path.join(BASE, "skills", "level1")
    
    # 重命名 02_一级Skill_小说总调度官.md -> 01_小说总调度官.md
    old_name = os.path.join(level1_src, "02_一级Skill_小说总调度官.md")
    new_name = os.path.join(level1_dst, "01_小说总调度官.md")
    if os.path.exists(old_name):
        shutil.copy2(old_name, new_name)
        print(f"  ✅ 02_一级Skill_小说总调度官.md -> 01_小说总调度官.md")
    
    # 复制 level1.md
    old_readme = os.path.join(level1_src, "level1.md")
    new_readme = os.path.join(level1_dst, "README.md")
    if os.path.exists(old_readme):
        shutil.copy2(old_readme, new_readme)
        print(f"  ✅ level1.md -> README.md")

    # ============================================================
    # 3. 整理 level2 (二级Skill) - 消除编号重复
    # ============================================================
    print("\n[3] 整理 level2...")
    
    level2_src = os.path.join(SKILLS, "level2")
    level2_dst = os.path.join(BASE, "skills", "level2")
    
    # 映射: 旧文件名 -> 新编号+新文件名
    # 按功能分组，消除重复编号
    level2_map = [
        ("03_二级Skill_世界观构造师.md", "01_世界观构造师.md"),
        ("04_二级Skill_剧情构造师.md", "02_剧情构造师.md"),
        ("05_二级Skill_场景构造师.md", "03_场景构造师.md"),
        ("06_二级Skill_对话设计师.md", "04_对话设计师.md"),
        ("07_二级Skill_角色塑造师.md", "05_角色塑造师.md"),
        ("08_二级Skill_战斗设计师.md", "06_战斗设计师.md"),
        ("09_二级Skill_写作技巧大师.md", "07_写作技巧大师.md"),
        ("10_二级Skill_去AI痕迹监督官.md", "08_去AI痕迹监督官.md"),
        ("11_二级Skill_质量审计师.md", "09_质量审计师.md"),
        ("12_二级Skill_选题策划大师.md", "10_选题策划大师.md"),
        ("13_二级Skill_大纲架构师.md", "11_大纲架构师.md"),
        ("14_二级Skill_节奏控制大师.md", "12_节奏控制大师.md"),
        ("15_二级Skill_情感共鸣师.md", "13_情感共鸣师.md"),
        ("16_二级Skill_一键AI消痕师.md", "14_一键AI消痕师.md"),
        ("16_二级Skill_市场分析师.md", "15_市场分析师.md"),
        ("17_二级Skill_AI工作流大师.md", "16_AI工作流大师.md"),
        ("17_二级Skill_IP运营师.md", "17_IP运营师.md"),
        ("18_二级Skill_小说拆书师.md", "18_小说拆书师.md"),
        ("18_二级Skill_数据分析师.md", "19_数据分析师.md"),
        ("19_二级Skill_描写增强师.md", "20_描写增强师.md"),
        ("20_二级Skill_版权保护师.md", "21_版权保护师.md"),
        ("21_二级Skill_市场分析师.md", "22_市场分析师_扩展.md"),
        ("22_二级Skill_创新灵感生成器.md", "23_创新灵感生成器.md"),
        ("23_二级Skill_读者心理分析师.md", "24_读者心理分析师.md"),
        ("24_二级Skill_发布规划师.md", "25_发布规划师.md"),
        ("30_二级Skill_学习大师.md", "26_学习大师.md"),
        ("31_二级Skill_规则掌控者.md", "27_规则掌控者.md"),
        ("32_二级Skill_词汇大师.md", "28_词汇大师.md"),
        ("40_二级Skill_题材选择大师.md", "29_题材选择大师.md"),
        ("11_二级Skill_短篇小说爽文大师.md", "30_短篇小说爽文大师.md"),
    ]
    
    for old, new in level2_map:
        src = os.path.join(level2_src, old)
        dst = os.path.join(level2_dst, new)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"  ✅ {old} -> {new}")
        else:
            print(f"  ⚠️ 未找到: {old}")
    
    # 复制协作总览
    src_overview = os.path.join(level2_src, "00_Skill协作总览.md")
    dst_overview = os.path.join(level2_dst, "00_Skill协作总览.md")
    if os.path.exists(src_overview):
        shutil.copy2(src_overview, dst_overview)
        print(f"  ✅ 00_Skill协作总览.md")
    
    # 复制 README
    src_readme = os.path.join(level2_src, "level2.md")
    dst_readme = os.path.join(level2_dst, "README.md")
    if os.path.exists(src_readme):
        shutil.copy2(src_readme, dst_readme)
        print(f"  ✅ level2.md -> README.md")
    
    # 复制 learnings 知识库
    src_learnings = os.path.join(level2_src, "learnings")
    dst_learnings = os.path.join(level2_dst, "learnings")
    if os.path.exists(src_learnings):
        for item in os.listdir(src_learnings):
            s = os.path.join(src_learnings, item)
            d = os.path.join(dst_learnings, item)
            if os.path.isdir(s):
                if not os.path.exists(d):
                    shutil.copytree(s, d)
            else:
                shutil.copy2(s, d)
        print(f"  ✅ learnings/ 知识库已复制")

    # ============================================================
    # 4. 整理 level3 (三级Skill) - 重新编号
    # ============================================================
    print("\n[4] 整理 level3...")
    
    level3_src = os.path.join(SKILLS, "level3")
    level3_dst = os.path.join(BASE, "skills", "level3")
    
    level3_map = [
        ("12_三级Skill_小说类型基类.md", "01_小说类型基类.md"),
        ("13_三级Skill_玄幻仙侠.md", "02_玄幻仙侠.md"),
        ("14_三级Skill_都市言情.md", "03_都市言情.md"),
        ("15_三级Skill_悬疑推理.md", "04_悬疑推理.md"),
        ("16_三级Skill_科幻未来.md", "05_科幻未来.md"),
        ("17_三级Skill_历史穿越.md", "06_历史穿越.md"),
        ("18_三级Skill_恐怖惊悚.md", "07_恐怖惊悚.md"),
        ("19_三级Skill_游戏竞技.md", "08_游戏竞技.md"),
        ("19_三级Skill_地理环境设计师.md", "09_地理环境设计师.md"),
        ("20_三级Skill_种族文明设计师.md", "10_种族文明设计师.md"),
        ("21_三级Skill_规则体系设计师.md", "11_规则体系设计师.md"),
        ("22_三级Skill_主线剧情设计师.md", "12_主线剧情设计师.md"),
        ("23_三级Skill_支线剧情设计师.md", "13_支线剧情设计师.md"),
        ("24_三级Skill_伏笔埋设师.md", "14_伏笔埋设师.md"),
        ("25_三级Skill_角色背景设计师.md", "15_角色背景设计师.md"),
        ("26_三级Skill_角色性格塑造师.md", "16_角色性格塑造师.md"),
        ("27_三级Skill_角色关系网络设计师.md", "17_角色关系网络设计师.md"),
        ("28_三级Skill_战斗场景设计师.md", "18_战斗场景设计师.md"),
        ("29_三级Skill_战斗招式设计师.md", "19_战斗招式设计师.md"),
        ("30_三级Skill_战斗节奏控制师.md", "20_战斗节奏控制师.md"),
        ("31_三级Skill_环境氛围营造师.md", "21_环境氛围营造师.md"),
        ("32_三级Skill_空间布局设计师.md", "22_空间布局设计师.md"),
        ("32_三级Skill_词汇大师.md", "23_词汇大师.md"),
        ("33_三级Skill_感官细节设计师.md", "24_感官细节设计师.md"),
        ("37_三级Skill_女频总裁文设计师.md", "25_女频总裁文设计师.md"),
        ("38_三级Skill_女频年代文设计师.md", "26_女频年代文设计师.md"),
        ("39_三级Skill_女频马甲文设计师.md", "27_女频马甲文设计师.md"),
        ("40_三级Skill_女频萌宝文设计师.md", "28_女频萌宝文设计师.md"),
    ]
    
    for old, new in level3_map:
        src = os.path.join(level3_src, old)
        dst = os.path.join(level3_dst, new)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"  ✅ {old} -> {new}")
        else:
            print(f"  ⚠️ 未找到: {old}")
    
    # 处理子目录类型的skill
    subdir_skills = [
        ("41_三级Skill_风水玄学小说", "41_三级Skill_风水玄学小说设计师.md", "29_风水玄学小说设计师.md"),
        ("42_三级Skill_军事小说", "42_三级Skill_军事小说设计师.md", "30_军事小说设计师.md"),
    ]
    
    for subdir, inner_file, new_name in subdir_skills:
        src = os.path.join(level3_src, subdir, inner_file)
        dst = os.path.join(level3_dst, new_name)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"  ✅ {subdir}/{inner_file} -> {new_name}")
        else:
            print(f"  ⚠️ 未找到: {subdir}/{inner_file}")
    
    # 复制词汇大师_new
    src_vocab_new = os.path.join(level3_src, "32_三级Skill_词汇大师_new.md")
    dst_vocab_new = os.path.join(level3_dst, "23_词汇大师_v2.md")
    if os.path.exists(src_vocab_new):
        shutil.copy2(src_vocab_new, dst_vocab_new)
        print(f"  ✅ 32_三级Skill_词汇大师_new.md -> 23_词汇大师_v2.md")
    
    # 复制 README
    src_readme3 = os.path.join(level3_src, "level3.md")
    dst_readme3 = os.path.join(level3_dst, "README.md")
    if os.path.exists(src_readme3):
        shutil.copy2(src_readme3, dst_readme3)
        print(f"  ✅ level3.md -> README.md")

    # ============================================================
    # 5. 整理 masters (大师级Skill)
    # ============================================================
    print("\n[5] 整理 masters...")
    
    masters_src = [
        ("CharacterMaster", "CharacterMaster.md"),
        ("GoldenPhraseMaster", "GoldenPhraseMaster.md"),
        ("PlotMaster", "PlotMaster.md"),
        ("SceneMaster", "SceneMaster.md"),
        ("WorldBuildingMaster", "WorldBuildingMaster.md"),
    ]
    
    masters_dst = os.path.join(BASE, "skills", "masters")
    for folder, filename in masters_src:
        src = os.path.join(SKILLS, folder, filename)
        dst = os.path.join(masters_dst, filename)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"  ✅ {folder}/{filename} -> masters/{filename}")
        else:
            print(f"  ⚠️ 未找到: {folder}/{filename}")

    # ============================================================
    # 6. 整理 scripts (Python脚本)
    # ============================================================
    print("\n[6] 整理 scripts...")
    
    py_files = [
        "deepseek_advanced_learning.py",
        "deepseek_competitor_analysis.py",
        "deepseek_learning_engine.py",
        "deepseek_online_optimize.py",
        "deepseek_v8_planning.py",
        "feishu_deepseek_diagnosis.py",
        "feishu_server_v2.py",
        "simple_learning.py",
        "specialized_learning.py",
        "start_feishu_server.py",
    ]
    
    scripts_dst = os.path.join(BASE, "skills", "scripts")
    for f in py_files:
        src = os.path.join(SKILLS, f)
        dst = os.path.join(scripts_dst, f)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"  ✅ {f} -> scripts/{f}")
        else:
            print(f"  ⚠️ 未找到: {f}")

    # ============================================================
    # 7. 整理 references (参考文本)
    # ============================================================
    print("\n[7] 整理 references...")
    
    txt_files = [
        "anti_ai_detection.txt",
        "character_building.txt",
        "plot_design.txt",
        "scene_rendering.txt",
        "vocabulary_master.txt",
        "writing_techniques.txt",
    ]
    
    refs_dst = os.path.join(BASE, "skills", "references")
    for f in txt_files:
        src = os.path.join(SKILLS, f)
        dst = os.path.join(refs_dst, f)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"  ✅ {f} -> references/{f}")
        else:
            print(f"  ⚠️ 未找到: {f}")

    # ============================================================
    # 8. 归档旧文件 (.bak, 智能升级)
    # ============================================================
    print("\n[8] 归档旧文件...")
    
    backups_dst = os.path.join(BASE, "skills", "archive", "backups")
    upgrades_dst = os.path.join(BASE, "skills", "archive", "upgrades")
    
    # .bak 文件
    bak_files = [
        "05_二级Skill_场景构造师.md.bak",
        "09_二级Skill_写作技巧大师.md.bak",
    ]
    for f in bak_files:
        src = os.path.join(level2_src, f)
        dst = os.path.join(backups_dst, f)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"  ✅ {f} -> archive/backups/")
    
    # 智能升级文件
    upgrade_files = [f for f in os.listdir(level2_src) if f.startswith("skill_") and f.endswith("_智能升级.md")]
    for f in upgrade_files:
        src = os.path.join(level2_src, f)
        dst = os.path.join(upgrades_dst, f)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"  ✅ {f} -> archive/upgrades/")

    # ============================================================
    # 9. 复制 system 目录
    # ============================================================
    print("\n[9] 整理 system...")
    
    system_src = os.path.join(SKILLS, "system")
    system_dst = os.path.join(BASE, "skills", "system")
    if os.path.exists(system_src) and not os.path.exists(system_dst):
        shutil.copytree(system_src, system_dst)
        print(f"  ✅ system/ 已复制")
    else:
        print(f"  ⚠️ system/ 已存在或源不存在")

    # ============================================================
    # 10. 生成新的 Skill索引文件
    # ============================================================
    print("\n[10] 生成 Skill索引...")
    
    index_content = """# NWACS Skill 完整索引 (重组版)

## 一级Skill - 总调度层
| 编号 | Skill名称 | 文件 |
|------|-----------|------|
| 01 | 小说总调度官 | level1/01_小说总调度官.md |

## 二级Skill - 核心创作能力层
| 编号 | Skill名称 | 文件 |
|------|-----------|------|
| 01 | 世界观构造师 | level2/01_世界观构造师.md |
| 02 | 剧情构造师 | level2/02_剧情构造师.md |
| 03 | 场景构造师 | level2/03_场景构造师.md |
| 04 | 对话设计师 | level2/04_对话设计师.md |
| 05 | 角色塑造师 | level2/05_角色塑造师.md |
| 06 | 战斗设计师 | level2/06_战斗设计师.md |
| 07 | 写作技巧大师 | level2/07_写作技巧大师.md |
| 08 | 去AI痕迹监督官 | level2/08_去AI痕迹监督官.md |
| 09 | 质量审计师 | level2/09_质量审计师.md |
| 10 | 选题策划大师 | level2/10_选题策划大师.md |
| 11 | 大纲架构师 | level2/11_大纲架构师.md |
| 12 | 节奏控制大师 | level2/12_节奏控制大师.md |
| 13 | 情感共鸣师 | level2/13_情感共鸣师.md |
| 14 | 一键AI消痕师 | level2/14_一键AI消痕师.md |
| 15 | 市场分析师 | level2/15_市场分析师.md |
| 16 | AI工作流大师 | level2/16_AI工作流大师.md |
| 17 | IP运营师 | level2/17_IP运营师.md |
| 18 | 小说拆书师 | level2/18_小说拆书师.md |
| 19 | 数据分析师 | level2/19_数据分析师.md |
| 20 | 描写增强师 | level2/20_描写增强师.md |
| 21 | 版权保护师 | level2/21_版权保护师.md |
| 22 | 市场分析师(扩展) | level2/22_市场分析师_扩展.md |
| 23 | 创新灵感生成器 | level2/23_创新灵感生成器.md |
| 24 | 读者心理分析师 | level2/24_读者心理分析师.md |
| 25 | 发布规划师 | level2/25_发布规划师.md |
| 26 | 学习大师 | level2/26_学习大师.md |
| 27 | 规则掌控者 | level2/27_规则掌控者.md |
| 28 | 词汇大师 | level2/28_词汇大师.md |
| 29 | 题材选择大师 | level2/29_题材选择大师.md |
| 30 | 短篇小说爽文大师 | level2/30_短篇小说爽文大师.md |

## 三级Skill - 细分领域层
| 编号 | Skill名称 | 文件 |
|------|-----------|------|
| 01 | 小说类型基类 | level3/01_小说类型基类.md |
| 02 | 玄幻仙侠 | level3/02_玄幻仙侠.md |
| 03 | 都市言情 | level3/03_都市言情.md |
| 04 | 悬疑推理 | level3/04_悬疑推理.md |
| 05 | 科幻未来 | level3/05_科幻未来.md |
| 06 | 历史穿越 | level3/06_历史穿越.md |
| 07 | 恐怖惊悚 | level3/07_恐怖惊悚.md |
| 08 | 游戏竞技 | level3/08_游戏竞技.md |
| 09 | 地理环境设计师 | level3/09_地理环境设计师.md |
| 10 | 种族文明设计师 | level3/10_种族文明设计师.md |
| 11 | 规则体系设计师 | level3/11_规则体系设计师.md |
| 12 | 主线剧情设计师 | level3/12_主线剧情设计师.md |
| 13 | 支线剧情设计师 | level3/13_支线剧情设计师.md |
| 14 | 伏笔埋设师 | level3/14_伏笔埋设师.md |
| 15 | 角色背景设计师 | level3/15_角色背景设计师.md |
| 16 | 角色性格塑造师 | level3/16_角色性格塑造师.md |
| 17 | 角色关系网络设计师 | level3/17_角色关系网络设计师.md |
| 18 | 战斗场景设计师 | level3/18_战斗场景设计师.md |
| 19 | 战斗招式设计师 | level3/19_战斗招式设计师.md |
| 20 | 战斗节奏控制师 | level3/20_战斗节奏控制师.md |
| 21 | 环境氛围营造师 | level3/21_环境氛围营造师.md |
| 22 | 空间布局设计师 | level3/22_空间布局设计师.md |
| 23 | 词汇大师 | level3/23_词汇大师.md |
| 24 | 感官细节设计师 | level3/24_感官细节设计师.md |
| 25 | 女频总裁文设计师 | level3/25_女频总裁文设计师.md |
| 26 | 女频年代文设计师 | level3/26_女频年代文设计师.md |
| 27 | 女频马甲文设计师 | level3/27_女频马甲文设计师.md |
| 28 | 女频萌宝文设计师 | level3/28_女频萌宝文设计师.md |
| 29 | 风水玄学小说设计师 | level3/29_风水玄学小说设计师.md |
| 30 | 军事小说设计师 | level3/30_军事小说设计师.md |

## 大师级Skill
| Skill名称 | 文件 |
|-----------|------|
| CharacterMaster | masters/CharacterMaster.md |
| GoldenPhraseMaster | masters/GoldenPhraseMaster.md |
| PlotMaster | masters/PlotMaster.md |
| SceneMaster | masters/SceneMaster.md |
| WorldBuildingMaster | masters/WorldBuildingMaster.md |

## 目录结构
```
skills/
├── level1/          # 一级Skill - 总调度
├── level2/          # 二级Skill - 核心创作能力 (30个)
│   └── learnings/   # 知识库
├── level3/          # 三级Skill - 细分领域 (30个)
├── masters/         # 大师级Skill (5个)
├── system/          # 系统文档
├── scripts/         # Python脚本
├── references/      # 参考文本
└── archive/         # 归档
    ├── backups/     # .bak备份
    └── upgrades/    # 智能升级记录
```
"""
    
    index_path = os.path.join(BASE, "skills", "Skill完整索引.md")
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_content)
    print(f"  ✅ Skill完整索引.md 已生成")

    # ============================================================
    # 完成
    # ============================================================
    print("\n" + "=" * 70)
    print("✅ Skills 文件夹重组完成！")
    print("=" * 70)
    print("\n新结构:")
    print("  skills/")
    print("  ├── level1/          # 一级Skill (1个)")
    print("  ├── level2/          # 二级Skill (30个)")
    print("  │   └── learnings/   # 知识库")
    print("  ├── level3/          # 三级Skill (30个)")
    print("  ├── masters/         # 大师级Skill (5个)")
    print("  ├── system/          # 系统文档")
    print("  ├── scripts/         # Python脚本 (10个)")
    print("  ├── references/      # 参考文本 (6个)")
    print("  └── archive/         # 归档")
    print("      ├── backups/     # .bak备份")
    print("      └── upgrades/    # 智能升级记录")
    print("\n⚠️ 旧文件保留在原位置，请确认新结构无误后手动删除旧目录。")

if __name__ == "__main__":
    main()
