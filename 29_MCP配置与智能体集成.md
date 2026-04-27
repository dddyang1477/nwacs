# MCP配置与智能体集成指南
## 让小说写作系统连接外部工具

---

## 一、MCP (Model Context Protocol) 简介

MCP 是 AI 与外部工具通信的标准协议。通过 MCP，你的小说写作 Skill 可以：
- 实时搜索网络获取最新信息
- 分析数据（如小说热度、读者偏好）
- 访问数据库（如世界观设定库、角色档案库）
- 调用外部工具（如绘图、语音合成）
- 读写文件（保存创作进度、记忆文件）

---

## 二、推荐 MCP 工具配置

### 2.1 搜索类 MCP

```json
{
  "mcpServers": {
    "web_search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "env": {
        "BRAVE_API_KEY": "your_api_key"
      }
    }
  }
}
```

**用途**：
- 一级Skill 搜索类型趋势
- 类型专家 搜索专业知识
- 去AI官 搜索人类写作特征

---

### 2.2 文件系统 MCP

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/novel/projects"]
    }
  }
}
```

**用途**：
- 保存世界观文档、角色档案、分章大纲
- 自动保存每章正文
- 读取历史创作记录
- 维护记忆管理模板

---

### 2.3 数据库 MCP (SQLite)

```json
{
  "mcpServers": {
    "sqlite": {
      "command": "uvx",
      "args": ["mcp-server-sqlite", "--db-path", "/path/to/novel_memory.db"]
    }
  }
}
```

**数据库设计**：

```sql
-- 项目表
CREATE TABLE projects (
    id INTEGER PRIMARY KEY,
    name TEXT,
    genre TEXT,
    style TEXT,
    status TEXT,
    created_at TIMESTAMP
);

-- 角色表
CREATE TABLE characters (
    id INTEGER PRIMARY KEY,
    project_id INTEGER,
    name TEXT,
    role_type TEXT,
    desire TEXT,
    fear TEXT,
    secret TEXT,
    arc TEXT,
    FOREIGN KEY (project_id) REFERENCES projects(id)
);

-- 章节表
CREATE TABLE chapters (
    id INTEGER PRIMARY KEY,
    project_id INTEGER,
    volume INTEGER,
    chapter_num INTEGER,
    title TEXT,
    content TEXT,
    ai_score INTEGER,
    quality_score INTEGER,
    status TEXT,
    FOREIGN KEY (project_id) REFERENCES projects(id)
);

-- 记忆表
CREATE TABLE memories (
    id INTEGER PRIMARY KEY,
    skill_name TEXT,
    memory_type TEXT,
    content TEXT,
    project_id INTEGER,
    created_at TIMESTAMP
);

-- 伏笔表
CREATE TABLE foreshadowing (
    id INTEGER PRIMARY KEY,
    project_id INTEGER,
    hint TEXT,
    planted_chapter INTEGER,
    resolved_chapter INTEGER,
    status TEXT
);
```

---

### 2.4 知识图谱 MCP

```json
{
  "mcpServers": {
    "neo4j": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "mcp/neo4j", 
             "--host", "localhost", "--port", "7687",
             "--username", "neo4j", "--password", "password"]
    }
  }
}
```

**知识图谱设计**：

```cypher
// 创建世界观节点
CREATE (world:World {name: "九州大陆", genre: "玄幻仙侠"})

// 创建势力节点
CREATE (sect1:Sect {name: "青云宗", type: "正道", strength: 8})
CREATE (sect2:Sect {name: "万剑阁", type: "中立", strength: 9})

// 创建角色节点
CREATE (char1:Character {name: "林凡", role: "protagonist", level: "炼气"})
CREATE (char2:Character {name: "赵天行", role: "villain", level: "筑基"})

// 创建关系
CREATE (char1)-[:BELONGS_TO {status: "expelled"}]->(sect1)
CREATE (char2)-[:BELONGS_TO {status: "heir"}]->(sect1)
CREATE (char1)-[:ENEMY {reason: "驱逐与背叛"}]->(char2)
CREATE (sect1)-[:ALLIANCE {type: "竞争"}]->(sect2)
```

---

## 三、Trae CN 中的 MCP 配置

### 3.1 配置步骤

1. 打开 Trae CN → 设置 → MCP
2. 添加 MCP 服务器配置（JSON格式）
3. 测试连接
4. 在 Skill 提示词中声明可用工具

### 3.2 Skill 提示词中的 MCP 声明

在 `02_一级Skill_小说总调度官.md` 中添加：

```markdown
## 可用工具（MCP）

### web_search
- 用途：搜索网络获取最新信息
- 触发时机：项目启动、创作卡壳、趋势跟踪
- 示例查询：
  - "玄幻仙侠 2026 热门趋势"
  - "修炼体系 创新设计"
  - "读者评价 玄幻小说 常见槽点"

### filesystem
- 用途：读写项目文件
- 触发时机：保存创作成果、读取历史记录
- 文件路径：
  - `/projects/{project_name}/worldview.md`
  - `/projects/{project_name}/characters/`
  - `/projects/{project_name}/chapters/`

### sqlite
- 用途：查询和更新项目数据库
- 触发时机：记忆检索、进度跟踪、伏笔管理

### neo4j
- 用途：管理角色关系和世界关联
- 触发时机：关系分析、势力格局可视化
```

---

## 四、智能体 (Agent) 配置

### 4.1 什么是智能体

智能体是具备以下能力的 AI：
- 目标导向：自主分解任务并执行
- 循环执行：观察→思考→行动→反思
- 工具调用：使用 MCP 工具完成复杂任务
- 状态维护：维护长期记忆和上下文

### 4.2 小说写作智能体设计

```
智能体：NovelWritingAgent
├── 技能层
│   ├── 调度官：解析需求、拆解任务
│   ├── 世界观师：构建世界
│   ├── 角色师：塑造角色
│   ├── 剧情师：设计剧情
│   ├── 场景师：设计场景
│   ├── 对话师：设计对话
│   ├── 战斗师：设计战斗
│   ├── 写作大师：统一风格
│   ├── 去AI官：消除AI痕迹
│   ├── 审计师：质量评估
│   └── 类型专家：专业指导
├── 工具层（MCP）
│   ├── web_search：网络搜索
│   ├── filesystem：文件读写
│   ├── sqlite：数据库
│   └── neo4j：知识图谱
└── 记忆层
    ├── 项目记忆：当前项目状态
    ├── 用户记忆：用户偏好
    ├── Skill记忆：各Skill经验
    └── 类型记忆：类型知识库
```

### 4.3 智能体工作流

```
用户输入需求
    |
    v
[调度官] 解析需求 → 搜索类型趋势
    |
    v
[并行执行]
├── [世界观师] → 保存到 filesystem
├── [角色师] → 保存到 sqlite
└── [类型专家] → 提供专业指导
    |
    v
[剧情师] → 读取世界+角色 → 设计剧情
    |
    v
[循环：每章]
├── [场景师+对话师+战斗师] → 创作正文
├── [写作大师] → 统一风格
├── [去AI官] → 检查AI痕迹
├── [审计师] → 质量评分
└── 不达标 → 返回修改
    |
    v
[调度官] → 汇总交付
    |
    v
[进化] → 分析数据 → 优化Skill
```

---

## 五、Trae CN 智能体配置实操

### 5.1 创建主智能体

**系统提示词**（基于 `20_整合版_主入口提示词.md` 扩展）：

```markdown
# 小说创作智能体 (NovelAgent)

你是一个具备自主决策能力的小说创作智能体。

## 核心能力
1. 自主规划：根据用户需求自动拆解任务
2. 工具调用：使用 MCP 工具获取信息和保存数据
3. 循环优化：创作→审查→修改，直到达标
4. 记忆维护：维护项目记忆，确保连续性

## 可用工具
- web_search：搜索网络信息
- filesystem：读写文件
- sqlite：数据库操作
- neo4j：知识图谱查询

## 工作流（自动执行）
当用户提出需求时，自动执行：
1. 解析需求 → 使用 web_search 搜索类型趋势
2. 构建世界观 → 保存到 filesystem
3. 设计角色 → 保存到 sqlite
4. 架构剧情 → 保存到 filesystem
5. 创作正文 → 每章保存，更新 sqlite
6. 审查优化 → 使用去AI化 + 质量审计
7. 交付成果 → 汇总所有文件

## 记忆管理
每次交互后自动更新：
- 当前项目状态
- 用户偏好
- 创作进度
- 质量数据

## 进化机制
每完成5章自动执行：
- 分析质量趋势
- 优化创作策略
- 更新类型知识
```

### 5.2 配置 Trae 智能体

1. 打开 Trae CN → 智能体 → 创建智能体
2. 粘贴上述系统提示词
3. 配置 MCP 工具（搜索、文件系统、数据库）
4. 设置自动执行模式
5. 测试运行

---

## 六、高级功能

### 6.1 自动伏笔追踪

使用 neo4j 追踪伏笔：
```cypher
MATCH (f:Foreshadowing {status: 'planted'})
WHERE f.project_id = $project_id
RETURN f.hint, f.planted_chapter, 
       CASE WHEN f.resolved_chapter IS NULL 
            THEN '未回收' 
            ELSE '已回收' END as status
```

### 6.2 角色一致性检查

使用 sqlite 检查角色行为：
```sql
SELECT name, action, chapter 
FROM character_actions 
WHERE character_id = $char_id
ORDER BY chapter;
```

### 6.3 质量趋势分析

```sql
SELECT 
    chapter_num,
    ai_score,
    quality_score,
    LAG(quality_score) OVER (ORDER BY chapter_num) as prev_score,
    quality_score - LAG(quality_score) OVER (ORDER BY chapter_num) as trend
FROM chapters
WHERE project_id = $project_id
ORDER BY chapter_num;
```

### 6.4 自动联网学习

定时任务：每周更新类型知识
```
foreach genre in [玄幻仙侠, 都市言情, 悬疑推理, 科幻未来]:
    trends = web_search.search(f"{genre} 2026 热门趋势")
    sqlite.insert("memories", skill_name=f"{genre}专家", 
                  memory_type="trend", content=trends)
```

---

## 七、配置文件汇总

### 7.1 完整 MCP 配置

```json
{
  "mcpServers": {
    "web_search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "env": {"BRAVE_API_KEY": "your_key"}
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/novel_projects"]
    },
    "sqlite": {
      "command": "uvx",
      "args": ["mcp-server-sqlite", "--db-path", "/novel_projects/memory.db"]
    },
    "neo4j": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "mcp/neo4j", 
             "--host", "localhost", "--port", "7687",
             "--username", "neo4j", "--password", "password"]
    }
  }
}
```

### 7.2 环境变量

```bash
# .env 文件
BRAVE_API_KEY=your_brave_api_key
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
PROJECT_ROOT=/novel_projects
```

---

## 八、常见问题

**Q：Trae CN 支持 MCP 吗？**
A：Trae CN 正在逐步支持 MCP。如果暂不支持，可以：
- 使用外部 MCP 服务器 + API 调用
- 手动复制搜索结果到对话中
- 使用文件系统手动管理项目文件

**Q：没有 API Key 怎么办？**
A：可以使用免费的搜索 MCP（如 DuckDuckGo），或使用本地数据库替代云端服务。

**Q：智能体模式太复杂，能简化吗？**
A：可以先使用 `28_最小启动包.md`，手动执行各阶段，逐步过渡到智能体模式。

---

## 九、下一步行动

1. 复制 MCP 配置到 Trae CN
2. 创建 NovelAgent 智能体
3. 配置数据库和知识图谱
4. 使用 `28_最小启动包.md` 测试基础功能
5. 逐步启用 MCP 工具
6. 开始自动化创作！

---

> 下一步：配置 MCP → 创建智能体 → 开始自动化创作！
