# NWACS 创作辅助工具使用指南

## 📦 工具概览

NWACS 已成功集成 `novel-mcp-server-v2` 中的所有创作辅助工具，提供从写作到审核的完整工具链。

### 可用工具列表

| 工具名称 | 功能说明 | 内置实现 | Node.js 实现 |
|----------|----------|----------|--------------|
| **AI 痕迹检测** | 检测文本中的 AI 生成痕迹 | ✅ 可用 | ✅ 可用 |
| **节奏分析** | 分析章节节奏是否符合预期 | ✅ 可用 | ✅ 可用 |
| **连贯性检查** | 检查前后情节的逻辑一致性 | ❌ | ✅ 需服务 |
| **对话优化** | 优化对话的自然度和角色特征 | ❌ | ✅ 需服务 |
| **敏感词过滤** | 检测暴力、色情、政治敏感内容 | ❌ | ✅ 需服务 |
| **读者模拟** | 预测读者反馈和弃书点 | ❌ | ✅ 需服务 |
| **风格指纹** | 提取并分析写作风格特征 | ❌ | ✅ 需服务 |
| **场景可视化** | 增强场景描写的感染力 | ❌ | ✅ 需服务 |

---

## 🚀 快速开始

### 方式 1: 双击运行测试
```
测试创作辅助工具.bat
```

### 方式 2: 命令行运行
```bash
python test_writing_assistant.py
```

---

## 💻 Python 代码调用

### 1. 导入工具

```python
from writing_assistant import get_writing_assistant

assistant = get_writing_assistant()
```

### 2. AI 痕迹检测

```python
# 基础检测
result = assistant.detect_ai(text)

# 深度检测
result = assistant.detect_ai(text, detection_mode='deep')

# 返回结果
if result['success']:
    ai_prob = result['ai_probability']  # 0-100 的概率值
    flagged = result['flagged_sections']  # 可疑段落列表
    suggestions = result['suggestions']   # 优化建议
```

**示例**:
```python
text = """
经过慎重考虑，我认为在这种情况下，
我们需要首先明确目标，其次制定计划。

值得注意的是，这种方法有其局限性。
"""

result = assistant.detect_ai(text)
print(f"AI 概率: {result['ai_probability']}%")
# 输出: AI 概率: 65%
```

---

### 3. 节奏分析

```python
# 基础分析
result = assistant.analyze_pacing(text)

# 指定章节位置和目标节奏
result = assistant.analyze_pacing(
    text,
    chapter_position='climax',  # opening/rising/climax/falling/ending
    target_pacing='fast'       # fast/moderate/slow
)

# 返回结果
if result['success']:
    score = result['score']           # 0-100 的评分
    issues = result['issues']         # 发现的问题
    suggestions = result['suggestions']  # 优化建议
```

**示例**:
```python
# 高潮战斗场景 - 需要快节奏
battle_text = """
他猛然转身。刀光一闪。血溅三尺。

"去死！"他低吼，身形暴起。
"""

result = assistant.analyze_pacing(battle_text, 'climax', 'fast')
print(f"节奏评分: {result['score']}/100")
# 输出: 节奏评分: 85/100
```

---

### 4. 连贯性检查

```python
# 检查小说连贯性
result = assistant.check_continuity(
    novel_id='my_novel_001',
    check_scope='chapter',   # chapter/arc/full
    strictness='normal'      # loose/normal/strict
)

# 返回结果
if result['success']:
    issues = result['issues']       # 发现的问题列表
    severity = result['severity']   # low/medium/high
    suggestions = result['suggestions']  # 修复建议
```

**注意**: 此功能需要完整的项目上下文，建议使用 Node.js 服务。

---

### 5. 对话优化

```python
# 优化对话
result = assistant.tune_dialogue(
    dialogue='"你好。"他说。"你好。"她说。',
    characters=['张三', '李四'],
    scene_context='办公室场景',
    tune_mode='natural'  # natural/characteristic/dramatic
)

# 返回结果
if result['success']:
    naturalness = result['naturalness_score']  # 自然度评分
    consistency = result['character_consistency']  # 角色一致性
    suggestions = result['suggestions']  # 优化建议
```

**注意**: 此功能需要 Node.js 服务支持。

---

### 6. 敏感词过滤

```python
# 敏感词检查
result = assistant.filter_sensitivity(
    text='他拿起刀砍向敌人。',
    check_level='normal',  # strict/normal/loose
    content_type='all'    # violence/sexual/political/superstitious/all
)

# 返回结果
if result['success']:
    sensitive = result['sensitive_content']  # 敏感内容列表
    risk = result['risk_level']  # low/medium/high
    suggestions = result['suggestions']  # 处理建议
```

**注意**: 此功能需要 Node.js 服务支持。

---

### 7. 读者反馈模拟

```python
# 模拟读者反馈
result = assistant.simulate_reader(
    text='他走到门口，深吸一口气，推开了那扇门...',
    reader_group='young_male',  # teen_male/young_male/young_female/mature_male/mature_female
    simulation_depth='surface'   # surface/deep
)

# 返回结果
if result['success']:
    engagement = result['engagement_score']  # 吸引力评分
    drop_points = result['predicted_drop_points']  # 预测弃书点
    suggestions = result['suggestions']  # 改进建议
```

**注意**: 此功能需要 Node.js 服务支持。

---

### 8. 综合分析

一次性执行多个检测：

```python
# 综合分析
result = assistant.comprehensive_analysis(text)

# 返回结果包含:
# - ai_detection: AI 痕迹检测结果
# - pacing_analysis: 节奏分析结果
# - word_count: 字数
# - char_count: 字符数
# - sentence_count: 句子数

print(f"AI 概率: {result['ai_detection']['ai_probability']}%")
print(f"节奏评分: {result['pacing_analysis']['score']}/100")
print(f"字数: {result['word_count']}")
```

---

## 🎯 实际应用场景

### 场景 1: 写完章节后自检

```python
from writing_assistant import get_writing_assistant

assistant = get_writing_assistant()

# 假设这是你刚写的章节
chapter_text = """
夜幕降临，华灯初上。

李明站在写字楼的落地窗前，俯瞰着整个城市。
...

他深吸一口气，推开了那扇门。
"""

# 1. AI 痕迹检测
ai_result = assistant.detect_ai(chapter_text)
if ai_result['ai_probability'] > 50:
    print("警告：文本可能存在 AI 痕迹，建议优化")
    for suggestion in ai_result['suggestions']:
        print(f"  • {suggestion}")

# 2. 节奏分析
pacing_result = assistant.analyze_pacing(chapter_text, 'climax', 'moderate')
if pacing_result['score'] < 60:
    print("警告：节奏可能需要调整")
    for issue in pacing_result['issues']:
        print(f"  • {issue}")

# 3. 敏感词检查
sensitivity_result = assistant.filter_sensitivity(chapter_text)
if sensitivity_result.get('risk_level') == 'high':
    print("警告：存在敏感内容，请检查")
```

### 场景 2: 发布前综合审核

```python
def pre_publish_check(chapter_text):
    """发布前综合审核"""
    assistant = get_writing_assistant()

    print("=" * 60)
    print("发布前综合审核")
    print("=" * 60)

    # 执行所有检查
    checks = {
        'AI 痕迹': assistant.detect_ai(chapter_text),
        '节奏分析': assistant.analyze_pacing(chapter_text),
        '敏感词': assistant.filter_sensitivity(chapter_text),
        '读者模拟': assistant.simulate_reader(chapter_text)
    }

    # 汇总结果
    all_passed = True

    for check_name, result in checks.items():
        print(f"\n【{check_name}】")
        if result.get('success'):
            if check_name == 'AI 痕迹':
                prob = result['ai_probability']
                print(f"  AI 概率: {prob}%")
                if prob > 60:
                    print("  ⚠️ 可能需要优化")
                    all_passed = False
                else:
                    print("  ✓ 通过")
            elif check_name == '节奏分析':
                score = result['score']
                print(f"  评分: {score}/100")
                if score < 60:
                    print("  ⚠️ 可能需要调整")
                    all_passed = False
                else:
                    print("  ✓ 通过")
            elif check_name == '敏感词':
                risk = result.get('risk_level', 'low')
                print(f"  风险等级: {risk}")
                if risk == 'high':
                    print("  ⚠️ 存在敏感内容")
                    all_passed = False
                else:
                    print("  ✓ 通过")
            elif check_name == '读者模拟':
                engagement = result.get('engagement_score', 0)
                print(f"  吸引力: {engagement}")
                if engagement < 60:
                    print("  ⚠️ 吸引力可能不足")
                    all_passed = False
                else:
                    print("  ✓ 通过")
        else:
            print(f"  ⚠️ 检查跳过: {result.get('error', '未知')}")

    print("\n" + "=" * 60)
    if all_passed:
        print("✓ 所有检查通过，可以发布！")
    else:
        print("⚠️ 建议根据以上提示优化后发布")
    print("=" * 60)

# 使用
pre_publish_check(chapter_text)
```

---

## ⚙️ 高级配置

### 自定义 Node.js 服务地址

如果需要连接远程 Node.js 服务，修改 `writing_assistant.py` 中的工具目录配置：

```python
class WritingAssistant:
    def __init__(self):
        # 修改为你的服务地址
        self.tools_dir = 'http://your-server.com/tools'
        # ...
```

### 内置实现说明

为确保在没有 Node.js 服务的环境下也能使用，核心功能（AI 检测、节奏分析）提供了纯 Python 内置实现：

- **AI 痕迹检测**: 通过检测模板化表达、句子长度、词汇多样性等特征判断
- **节奏分析**: 通过句子长度、对话比例、动作词密度等判断节奏

内置实现精度略低于 Node.js 实现，但足以满足日常使用需求。

---

## 📊 工具性能对比

| 工具 | 内置实现 | Node.js 实现 | 推荐场景 |
|------|----------|--------------|----------|
| AI 痕迹检测 | ✅ 完整 | ✅ 更准确 | 日常写作/专业审核 |
| 节奏分析 | ✅ 完整 | ✅ 更细致 | 日常写作/专业审核 |
| 连贯性检查 | ❌ | ✅ 完整 | 完整项目审核 |
| 对话优化 | ❌ | ✅ 完整 | 对话多的作品 |
| 敏感词过滤 | ❌ | ✅ 完整 | 发布前必检 |
| 读者模拟 | ❌ | ✅ 完整 | 商业化写作 |

---

## 🔧 故障排查

### 问题 1: Node.js 工具全部不可用

**症状**: 所有需要 Node.js 的工具都返回 "需要 Node.js 服务"

**解决方案**:
1. 确保已安装 Node.js: `node --version`
2. 确保 novel-mcp-server-v2 已正确编译
3. 检查 `writing_assistant.py` 中的工具目录路径是否正确

### 问题 2: 工具执行超时

**症状**: 工具返回 "执行超时"

**解决方案**:
1. 检查文本是否过长（建议单次不超过 10 万字）
2. 检查网络连接
3. 重试操作

### 问题 3: AI 概率误判

**症状**: 正常写作被判定为高 AI 概率

**解决方案**:
1. 使用 `detection_mode='deep'` 进行深度检测
2. 检查 flagged_sections 中的具体原因
3. 根据建议进行针对性优化

---

## 🎓 最佳实践

### 1. 写作阶段
- 专注于内容创作，不必过度在意 AI 检测
- 保持自己的写作风格和节奏

### 2. 初稿完成后
- 使用 AI 痕迹检测，检查是否有模板化表达
- 根据建议适当增加个人风格

### 3. 修改阶段
- 使用节奏分析，确保章节节奏符合预期
- 根据目标读者群体调整节奏

### 4. 发布前
- 运行敏感词过滤，确保内容合规
- 使用读者模拟，预测读者反馈
- 进行综合审核

---

## 📝 总结

NWACS 的创作辅助工具覆盖了小说创作的全流程：

- ✅ **AI 检测**: 确保作品原创性
- ✅ **节奏分析**: 确保阅读体验
- ✅ **连贯性检查**: 确保逻辑严密
- ✅ **敏感词过滤**: 确保内容合规
- ✅ **读者模拟**: 预测市场反馈

**内置实现确保随时可用，Node.js 实现提供更专业的服务。**

---

## 📞 获取帮助

- 查看完整测试: `test_writing_assistant.py`
- 查看集成源码: `src/core/writing_assistant.py`
- 查看 Node.js 工具源码: `novel-mcp-server-v2/src/tools/`

---

**🎯 建议：将这些工具整合到您的写作工作流中，形成「写作 → 自检 → 修改 → 审核 → 发布」的完整闭环！**
