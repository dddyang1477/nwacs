# NWACS 系统结构梳理与功能分类报告

> 生成时间：2026-05-16  
> 基于代码库全量扫描分析（Agent Explore + 人工验证）

---

## 一、项目总览

**NWACS** (Novel Writing AI Collaborative System) 智能小说写作AI协作系统，当前处于 v7/v8/v9 多版本代码并存状态。

- **根目录**：`NWACS/`
- **技术栈**：Python 3.13 + 原生HTML/CSS/JS + HTTP Server + MCP协议
- **核心文件规模**：约 80+ Python模块 + 10+ HTML前端 + 100+ Skill知识库文档

---

## 二、调度中心 — 谁在控制一切？

### 唯一核心调度器：`core/v8/nwacs_server_v3.py`

这是整个NWACS的**中枢神经**，承担三大职责：

1. **模块初始化**：启动时一次性初始化全部核心模块（约20+个）
2. **HTTP API服务**：基于 `http.server.HTTPServer` 提供REST API，所有前端请求通过 `do_GET()` / `do_POST()` 路由
3. **数据路由**：LLM请求 -> `llm_interface.py` -> DeepSeek/OpenAI API

### 辅助调度器

| 文件 | 角色 | 独立性 |
|------|------|--------|
| `smart_start.py` | 交互式启动菜单，调用各子模式脚本 | 低 |
| `orchestrator.py` | 外部编排器 v4.0，独立Agent流水线 | **高（可脱离主系统运行）** |
| `main.py` | 设计的统一入口 | **损坏**（引用的 `NWACS_FINAL` 类不存在） |

---

## 三、后端模块分层结构

### 第一层：数据与配置管理

| 模块 | 功能 | 联动状态 |
|------|------|----------|
| `genre_profile_manager.py` | 题材画像管理 | 被调度器初始化，前端未调用 |
| `project_memory.py` | 项目记忆 | 被调度器初始化，前端未调用 |
| `truth_file_manager.py` | 真相文件一致性 | 被调度器初始化，前端未调用 |
| `llm_interface.py` | 统一大模型接口（多模型支持） | 被调度器初始化，前端未调用 |

### 第二层：核心创作引擎

| 模块 | 功能 | 联动状态 |
|------|------|----------|
| `story_system.py` | 故事合同/章节提交/快照 | 被调度器初始化，前端未调用 |
| `writing_pipeline.py` | 多Agent写作管线（Planner-Writer-Auditor-Reviser） | 被调度器初始化，前端未调用 |
| `planning_system.py` | 卷级/章级合同规划 | 被调度器初始化，前端未调用 |
| `strand_weave.py` | 暗线编织引擎 | 被调度器初始化，前端未调用 |
| `rag_engine.py` | RAG检索增强 | 被调度器初始化，前端未调用 |

### 第三层：质量与优化

| 模块 | 功能 | 联动状态 |
|------|------|----------|
| `quality_system.py` | 多维质量评估 | 被调度器初始化，前端未调用 |
| `reviewer_agent.py` | 章节审查Agent | 被调度器初始化，前端未调用 |
| `ai_humanizer.py` | 去AI痕迹引擎 v5 | 被调度器初始化，前端未调用 |
| `fatigue_detector.py` | 疲劳检测/重复用词 | 被调度器初始化，前端未调用 |
| `style_fingerprint.py` | 文风一致性分析 | 被调度器初始化，前端未调用 |

---

## 四、前端分析 — `index_v9_final.html`

### 4.1 基本定位

- **文件大小**：3650行
- **性质**：纯前端单页应用（SPA）
- **关键特征**：**无任何网络请求代码**（无 fetch / XMLHttpRequest / WebSocket）
- **数据持久化**：仅通过浏览器存储（localStorage）

### 4.2 JS函数分类（9大模块）

| 分类 | 函数数量 | 核心函数 |
|------|----------|----------|
| A. 初始化与系统 | 6+ | `init()`, `loadTheme()`, `loadApiSettings()`, `testApiConnection()` |
| B. Step导航与UI | 6+ | `switchStep()`, `goToStep()`, `autoFillDefaults()` |
| C. 角色管理 | 8+ | `initCharacters()`, `smartNameChar()`, `generateTraditionalName()`（含五行/八卦/阴阳/风水） |
| D. 剧情生成 | 3+ | `generatePlots()`, `getStyleExpansionPool()`, `getToneAtmosphere()` |
| E. 大纲与细纲 | 3+ | `generateOutline()`, `generateChapterTitles()`, `generateDetailOutline()` |
| F. 写作编辑器 | 6+ | `startWriting()`, `saveWriting()`, `continueWriting()` |
| G. AI辅助工具 | 8+ | `aiPolish()`（15阶段）, `checkAIDetect()`（24种模式）, `detectSynonymCycles()`, `checkSentenceRhythm()` |
| H. 内容生成 | 1+ | `generateChapterContent()`（6种题材场景库模板拼接） |
| I. 导出与留言 | 4+ | `exportNovel()`, `loadComments()`, `addComment()` |

### 4.3 "智能生成"的真相

所有标为"生成"的功能，实际上都是**前端模板拼接模拟**：

- `generatePlots()`：从 `PLOT_TEMPLATES` 常量中按题材取模板
- `generateChapterContent()`：使用内置6种题材场景库（xuanhuan/xianxia/wuxia/dushi/kehuan/yanqing），每个2组场景模板，拼接生成
- `aiPolish()`：基于正则替换规则库，非LLM调用
- `testApiConnection()`：仅读取输入框值，**无实际网络请求**

---

## 五、前后端断联 — 最大问题

### 断联证据

| 前端 | 后端 | 状态 |
|------|------|------|
| `index_v9_final.html` | `nwacs_server_v3.py` | **完全断联** — 前端无任何API调用 |
| `web_ui/index.html` (v7) | `localhost:5000` | **端口不匹配** — 后端实际端口未知 |
| `main.py` | `NWACS_FINAL` 类 | **引用不存在** — 入口文件损坏 |

### 后端API能力（未被前端利用）

`nwacs_server_v3.py` 提供了完整的REST API：

- `GET /api/health` — 健康检查
- `GET /api/models` — 模型列表
- `POST /api/generate_plots` — LLM生成剧情
- `POST /api/generate_chapter` — LLM生成章节 + 质量检查
- `POST /api/generate_names` — 生成角色名
- `POST /api/story_init` — 初始化故事
- `POST /api/review` — 审查章节
- 等数十个端点，已配置CORS支持跨域

**结论**：后端引擎全副武装，前端却在前端"假装"工作。这是系统最大的结构性问题。

---

## 六、孤立模块分析

### 6.1 真正孤立（无被导入/引用）

| 文件 | 说明 |
|------|------|
| `core/v8/refactored_do_get.py` | HTTP处理重构碎片 |
| `frontend/fix2.js`, `fix_template.js` | 临时修复脚本 |
| `core/v8/tests/*.py` | 测试文件 |
| `tools/organize_directory.py` | 目录整理工具 |
| `fix_kb.py`, `check_chapters.py` | 独立修复脚本 |
| `_git_push.bat` / `.ps1` | Git推送辅助 |

### 6.2 半独立（低耦合，可独立运行）

| 文件 | 说明 |
|------|------|
| `orchestrator.py` | 独立Agent流水线，不依赖core/v8 |
| `mcp_servers/*.py` | 通过stdio外部通信，不调用主系统 |
| `skills/scripts/*.py` | Skill专用脚本 |
| `.trae/skills/*/SKILL.md` | Trae IDE扩展定义 |
| `docs/`, `learning/`, `examples/` | 纯文档知识库 |

### 6.3 版本并存垃圾文件（需清理）

`frontend/` 目录下有 **6个废弃的index_v9中间版本**：

- `index_v9.html`
- `index_v9_complete.html`
- `index_v9_fixed.html`
- `index_v9_merged.html`
- `index_v9_refactored.html`
- `__temp_check.js` (1-4), `fix2.js`, `fix_template.js`

---

## 七、协作联动通畅性评估

### 通畅的链路

```
nwacs_server_v3.py  ->  llm_interface.py  ->  DeepSeek/OpenAI API
       |
       v
  story_system.py <-> writing_pipeline.py <-> planning_system.py
       |
       v
  quality_system.py + reviewer_agent.py + ai_humanizer.py
```

后端内部模块高度耦合，通过调度器统一管理，**内部联动通畅**。

### 断裂的链路

```
index_v9_final.html  --X-->  nwacs_server_v3.py API
       ^
       |
   所有"生成"功能都是前端模板拼接，从未调用LLM
```

---

## 八、建议

1. **紧急：前端对接后端API** — 为 `index_v9_final.html` 添加 `fetch()` 调用，将前端模板生成替换为真实的 `nwacs_server_v3.py` API调用
2. **清理废弃文件** — 删除6个废弃的index_v9中间版本和临时JS文件
3. **修复main.py** — 补全或移除对 `NWACS_FINAL` 的引用
4. **明确半独立模块** — 将 `orchestrator.py` 和 `mcp_servers/` 标注为"可选插件"
5. **版本管理** — 使用Git分支管理版本迭代，避免多版本文件并存
