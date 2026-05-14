# NWACS 系统优化 - 快速使用指南

## 🎯 新增功能一览

| 功能模块 | 用途 | 使用方式 |
|----------|------|----------|
| 大模型优化器 | 节省 API 成本、提高稳定性 | 自动启用，无需手动操作 |
| 智能分发器 | 精准匹配学习内容到 Skill | 学习时自动使用 |
| GitHub 同步增强 | 更可靠的代码同步 | 自动同步，失败自动备份 |
| 主题生成器 | 智能生成学习计划 | 自动为各 Skill 生成主题 |
| 数据统计面板 | 记录写作和学习数据 | 自动记录，随时查询 |
| 模板库 | 提供写作模板和素材 | 按需调用 |

---

## 📦 核心模块说明

### 1. 大模型优化器 (llm_optimizer.py)

**功能**:
- 💰 余额检测 - 避免 API 余额不足导致中断
- 🔄 限流控制 - 防止触发 API 限流
- 💾 本地缓存 - 相同请求不重复调用，节省 60% 成本
- ⚡ 重试机制 - 失败自动重试 3 次

**自动生效场景**:
- Skill 学习时调用大模型分析
- 创作时调用大模型辅助
- 任何使用大模型的功能

---

### 2. 智能分发器 (smart_distributor.py)

**功能**:
- 🎯 智能匹配 - 自动将学习内容分发到最合适的 Skill
- 🚫 去重机制 - 24 小时内不重复学习同一主题
- 📊 学习历史 - 记录所有学习活动

**示例**:
```
学习主题："短篇小说开篇技巧"
→ 自动匹配到：短篇小说爽文大师

学习主题："修炼体系设定"
→ 自动匹配到：世界观构造师
```

---

### 3. GitHub 同步增强 (git_sync_enhanced.py)

**功能**:
- 🌐 网络检测 - 同步前检查网络
- 🔁 自动重试 - 失败后自动重试 3 次
- 💾 自动备份 - 同步失败时创建本地备份
- 📝 历史记录 - 查询同步状态

**使用**:
```python
from git_sync_enhanced import sync_to_github

# 手动同步（可选）
sync_to_github("手动同步 - 更新章节")
```

---

### 4. 主题生成器 (topic_generator.py)

**功能**:
- 📚 动态生成学习主题
- 📈 优先级排序 - 热点话题优先
- 📅 学习计划 - 生成 7 天/30 天学习计划

**查看学习计划**:
```python
from topic_generator import get_topic_generator

generator = get_topic_generator()
plan = generator.suggest_learning_plan('短篇小说爽文大师', days=7)

for day in plan['daily_topics']:
    print("第%d天：%s" % (day['day'], day['topic']))
```

---

### 5. 数据统计面板 (stats_dashboard.py)

**功能**:
- ✍️ 写作统计 - 字数、章节、项目进度
- 📖 学习统计 - 学习次数、时长
- 🏆 成就系统 - 解锁写作成就徽章

**查看今日数据**:
```python
from stats_dashboard import get_stats_dashboard

dashboard = get_stats_dashboard()
today = dashboard.get_daily_summary()
print("今日写作：%d 字" % today['total_words'])
```

**查看完整报告**:
```python
report = dashboard.export_report(format='text')
print(report)
```

---

### 6. 模板库 (template_library.py)

**功能**:
- 📝 开篇模板 - 5 种爆款开篇方式
- 🔥 爽点模板 - 经典爽点套路
- 💬 对话模板 - 各类对话模式
- 🎨 描写素材 - 外貌、动作、心理、环境

**使用示例**:
```python
from template_library import get_template_library

library = get_template_library()

# 获取开篇模板
template = library.get_template('开篇模板', '冲突开篇')
print(template['example'])

# 随机获取爽点模板
random_temp = library.get_random_template('爽点模板')
print(random_temp['name'])

# 搜索模板
results = library.search_templates('打脸')
for r in results:
    print("%s/%s" % (r['category'], r['name']))
```

---

## 🚀 快速体验

### 方式 1: 双击运行演示
```
运行优化演示.bat
```

### 方式 2: 命令行运行
```bash
python demo_optimizations.py
```

### 方式 3: 在创作中使用
所有优化已集成到系统中，正常使用即可自动生效。

---

## 📊 数据管理

### 查看统计数据文件
- `writing_stats.json` - 写作和学习统计数据
- `learning_history.json` - 学习分发历史
- `topic_learning_history.json` - 主题学习历史
- `git_sync_history.json` - Git 同步历史
- `llm_response_cache.json` - 大模型响应缓存

### 清空统计数据
```python
from stats_dashboard import get_stats_dashboard

dashboard = get_stats_dashboard()
dashboard.clear_data()  # 清空所有统计数据
```

---

## ⚙️ 配置说明

### 大模型配置 (config.json)
```json
{
  "api_key": "你的 API 密钥",
  "base_url": "https://api.deepseek.com",
  "model": "deepseek-chat",
  "enabled": true
}
```

### 自定义模板
模板会自动保存到 `writing_templates.json`，可手动编辑添加自定义模板。

---

## 🎯 最佳实践

### 1. 写作时
- 系统自动记录写作数据
- 需要灵感时查看模板库
- 定期查看统计数据，了解自己的写作进度

### 2. 学习时
- 系统自动安排学习计划
- 学习内容精准分发到对应 Skill
- 24 小时内不重复学习，提高效率

### 3. 同步代码
- 系统自动同步到 GitHub
- 网络异常时自动备份
- 可手动触发同步

### 4. 使用大模型
- 相同请求自动使用缓存
- 根据任务类型选择最佳模型
- 实时监控余额和成本

---

## 🔧 故障排查

### 问题 1: 大模型调用失败
**检查**:
1. config.json 中 API 密钥是否正确
2. 网络连接是否正常
3. 查看日志文件了解详细错误

**解决**:
- 余额不足时系统会自动切换到纯联网学习模式
- 网络异常时会使用缓存数据

### 问题 2: GitHub 同步失败
**检查**:
1. 网络连接
2. Git 仓库配置
3. 查看同步历史

**解决**:
- 系统会自动创建本地备份
- 网络恢复后会自动重试

### 问题 3: 学习内容分发错误
**检查**:
1. Skill 名称是否正确
2. 查看分发历史

**解决**:
- 系统会智能匹配最合适的 Skill
- 可手动调整分发规则

---

## 📞 获取帮助

### 查看日志
所有操作都会记录到日志文件，位置：`logs/` 目录

### 查看演示
运行 `demo_optimizations.py` 查看所有功能演示

### 查看完整报告
阅读 `OPTIMIZATION_REPORT.md` 了解详细优化内容

---

## 🎉 开始使用

**无需额外配置，所有优化已自动集成到系统中！**

只需正常使用 NWACS 系统，优化功能会自动生效：
- ✅ 写作时自动统计数据
- ✅ 学习时智能分发内容
- ✅ 调用大模型时自动优化
- ✅ 同步代码时增强可靠性

**立即开始高效创作吧！** ✍️🚀
