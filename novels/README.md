# 📖 NWACS V8.0 小说生成系统使用说明

## 概述

NWACS V8.0的小说生成系统现在支持：
- ✅ 按小说名字创建文件夹
- ✅ 分章节保存为 .md 和 .txt 格式
- ✅ 自动生成目录
- ✅ 合并完整小说为单个文件

## 文件结构

```
novels/
└── 小说名/
    ├── chapter_01.md          # 第1章 (Markdown格式)
    ├── chapter_01.txt         # 第1章 (文本格式)
    ├── chapter_02.md
    ├── chapter_02.txt
    ├── ...
    ├── table_of_contents.md   # 目录 (Markdown格式)
    ├── table_of_contents.txt  # 目录 (文本格式)
    ├── 小说名_full.md         # 完整小说 (Markdown格式)
    ├── 小说名_full.txt        # 完整小说 (文本格式)
    └── novel_info.json        # 小说信息
```

## 使用方法

### 🎯 **推荐：一键智能选择启动器（最简单）
```bash
py smart_start.py
```
**特点：
- ✅ 会根据小说长度自动选择生成模式
- ✅ 推荐：短篇 → 快速生成
- ✅ 中长篇 → 剧情连贯模式
- ✅ 简单易用的界面
- 不需要你不需要你你不需不需
-

### 快速开始（手动选择）

#### 1. 测试文件保存功能

首先测试文件保存功能是否正常：

```bash
py core/v8/test_file_saving.py
```

这会在 `novels/测试小说/` 目录下生成测试文件。

#### 2. 生成《天机道主》

有两种选择：

**方案A：快速生成（适合短篇）
```bash
py core/v8/novel_generator.py
```

**方案B：剧情连贯（推荐，适合长篇）**
```bash
py core/v8/smart_novel_generator.py
```

选择选项 1，开始生成小说。

**请阅读 [剧情连贯说明](./CONTINUITY_GUIDE.md) 了解更多详情！

### 功能说明

#### novel_generator.py 功能

1. **按小说名创建文件夹**
   - 自动在 `novels/` 目录下创建与小说名同名的文件夹

2. **分章节保存**
   - 每个章节同时保存为 `.md` 和 `.txt` 两种格式
   - 文件名格式：`chapter_01.md`, `chapter_01.txt`

3. **自动生成目录**
   - Markdown格式的目录包含可点击链接
   - 文本格式的目录简洁清晰

4. **合并完整小说**
   - 将所有章节合并为单个文件
   - 同时提供 `.md` 和 `.txt` 两种格式

## 示例输出

### 生成的文件列表

```
novels/天机道主/
├── chapter_01.md
├── chapter_01.txt
├── chapter_02.md
├── chapter_02.txt
├── chapter_03.md
├── chapter_03.txt
├── chapter_04.md
├── chapter_04.txt
├── chapter_05.md
├── chapter_05.txt
├── table_of_contents.md
├── table_of_contents.txt
├── 天机道主_full.md
├── 天机道主_full.txt
└── novel_info.json
```

### Markdown格式示例

```markdown
# 第一章：废物与棋子

内容...
```

### 文本格式示例

```
第一章：废物与棋子
==============================

内容...
```

## 自定义小说

要生成自定义小说，请修改 `novel_generator.py`，添加新的小说生成函数。

### 结构说明

每个小说生成函数需要：

1. 定义 `novel_name` - 小说名称
2. 创建小说文件夹
3. 定义章节信息
4. 生成每个章节
5. 保存章节
6. 生成目录
7. 合并完整小说

## 历史说明

### 原来的问题

- ❌ 没有按小说名创建文件夹
- ❌ 只保存为 .md 格式，没有 .txt 格式
- ❌ 文件保存路径硬编码
- ❌ 没有目录和完整小说合并

### 现在的改进

- ✅ 按小说名创建文件夹
- ✅ 同时保存为 .md 和 .txt 格式
- ✅ 自动生成目录
- ✅ 合并完整小说为单个文件
- ✅ 保存小说信息到 JSON

## 下一步计划

- [ ] 添加更多预设小说
- [ ] 支持自定义小说设定
- [ ] 支持批量生成
- [ ] 添加章节预览功能
- [ ] 添加小说导出功能

---

**NWACS V8.0 - 让小说创作更简单！** 📖✨
