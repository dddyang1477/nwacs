# NWACS v3.0 项目规则 (Project Rules)

## 系统身份
本项目使用 NWACS (Novel Writing AI Collaborative System) v3.0 架构。
所有 Agent 必须遵守以下全局规则。

## 1. 文件规范
- 所有共享事实写入 `nwacs-data/` 目录
- 章节正文写入 `chapters/chapter_XXX.md`
- 角色档案写入 `nwacs-data/characters/{name}.json`
- 伏笔索引写入 `nwacs-data/foreshadow_index.json`
- 世界观写入 `nwacs-data/world_setting.md`

## 2. 上下文隔离协议
- Agent 间不共享思维链、草稿、修改历史
- 创作 Agent 只能读取规则文件和上游 Agent 的最终输出
- 监督 Agent 只能读取成品文本和档案文件，禁止读取创作过程
- 调度官是唯一拥有全局视角的 Agent，但本身不参与创作与审核

## 3. 版本控制
- 每章完成后必须更新 `nwacs-data/version_log.md`
- 格式：`[YYYY-MM-DD HH:MM] 第X章 状态 操作者`

## 4. 安全红线
- 禁止生成违反法律法规的内容
- 禁止生成侵犯他人版权的实质性相似内容
- 涉及敏感历史/宗教/政治内容时，自动降级为架空设定
