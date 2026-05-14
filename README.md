# NWACS-Orchestrator v7.0

## 定位
脱离 Trae 的 Agent 自动化引擎。解决 Trae "所有 Agent 共享同一模型"的限制，实现真正的**多模型路由**。

## 核心特性
- **Agent 级模型绑定**：@调度官用 Kimi，@剧情构造师用 DeepSeek，自动切换
- **流水线编排**：定义创作流程，一键执行多 Agent 协作
- **成本追踪**：精确到每次调用的 Token 用量和费用统计
- **条件分支**：审核不通过自动阻断或跳过后续步骤

## 文件结构
```
NWACS_Orchestrator/
├── orchestrator.py          # 核心引擎（配置管理+LLM客户端+Agent执行器+流水线）
├── example_pipeline.py      # 示例：创作单章
├── advanced_pipeline.py     # 高级示例：带审核门禁
├── batch_pipeline.py        # 批量示例：连续创作多章
├── config/
│   ├── models.json          # 模型配置（API Key、Base URL）
│   └── agents.json          # Agent 配置（绑定哪个模型、Prompt文件路径）
├── agents/
│   ├── 调度官.md
│   ├── 剧情构造师.md
│   ├── 场景构造师.md
│   ├── 对话设计师.md
│   ├── 去AI监督官.md
│   └── 质量审计师.md
└── output/
    ├── chapters/            # 生成的章节
    └── review/              # 审核报告
```

## 快速开始

### 1. 安装依赖
```bash
pip install openai
```

### 2. 配置 API Key
编辑 `config/models.json`：
```json
{
  "kimi-k2.6": {
    "api_key": "sk-your-actual-kimi-key",
    ...
  },
  "deepseek-v3.2": {
    "api_key": "sk-your-actual-deepseek-key",
    ...
  }
}
```

### 3. 运行示例
```bash
python example_pipeline.py
```

## 模型分配策略（推荐）

| Agent | 模型 | 原因 | 单次成本 |
|-------|------|------|---------|
| 调度官 | Kimi K2.6 | 长上下文，全局决策 | ~¥0.3 |
| 剧情构造师 | DeepSeek V3.2 | 逻辑强、便宜 | ~¥0.05 |
| 场景/对话 | DeepSeek V3.2 | 批量生成 | ~¥0.06 |
| 去AI监督官 | Kimi K2.6 | 中文语感识别AI味 | ~¥0.2 |
| 质量审计师 | Kimi K2.6 | 跨章节一致性 | ~¥0.3 |

## 与 Trae 的关系

| 维度 | Trae | Orchestrator |
|------|------|-------------|
| 模型切换 | 手动全局切换 | Agent 自动路由 |
| 环境 | IDE 内 | Python 脚本 |
| 适用场景 | 单章精修 | 批量生产 |
| 最佳实践 | Trae 写 + Orchestrator 批量跑 | |

建议：**用 Trae 精修单章，用 Orchestrator 批量生产**。
