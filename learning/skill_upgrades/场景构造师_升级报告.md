# 场景构造师 智能升级报告
============================================================

## 📊 升级概况
- 升级时间：2026-04-30 00:42:54
- 升级系统：Skill智能学习系统 v3.0

## 🎯 升级目标
# 【场景构造师】智能化与人性化升级方案

## 一、总体架构

以“感知—推理—生成—校验—增强”为核心流水线，将场景构造拆解为五个智能模块与五个人性化服务层：

- **智能化模块**：画面感检查、情绪一致性、空间布局验证、场景转换优化、记忆管理
- **人性化服务**：示例库、情绪指南、衔接建议、可视化描述、新手引导

最终以交互式助手形态呈现，支持多模态输出（文本+结构化JSON+简单SVG示意图）。

---

## 二、智能化升级详细方案

### 2.1 画面感检查器（Visual Intensity Checker）

**目标**：量化场景描写的“画面感”，提示缺失的感官细节。

**实现思路**：
- 建立**五感（视觉、听觉、嗅觉、触觉、味觉）与动态元素（光影、运动、色彩、声音源）的评分模型**。
- 检查画面中是否具备“焦点主体-中景衬托-远景氛围”的层次。
- 给出不足项及补写建议。

**伪代码示例**：

```python
class VisualIntensityChecker:
    SENSORY_KEYS = {
        "视觉": ["颜色", "形状", "光影", "尺度", "位置"],
        "听觉": ["声音源", "音量", "音色", "节奏"],
        "嗅觉": ["气味类型", "浓度", "来源"],
        "触觉": ["材质", "温度", "湿度", "压力"],
        "味觉": ["味道", "强度"]
    }
    
    def check(self, scene_text: str) -> dict:
        parsed = self.parse_scene(scene_text)
        sensory_coverage = self.count_sensory_details(parsed)
        depth_score = self.evaluate_depth(parsed)   # 是否有前景/背景层次
        dynamic_score = self.evaluate_dynamics(parsed) # 是否描述运动、变化
        
        suggestions = []
        for sense, elements in self.SENSORY_KEYS.items():
            if sensory_coverage[sense] < 2:
                suggestions.append(f"增加{sense}细节，例如{elements[0]}描述。")
        if depth_score < 0.5:
            suggestions.append("可补充前景主体与远景氛围，增强空间层次。")
        if dynamic_score < 0.3:
            suggestions.append("加入动态元素（飘动、闪烁）打破静态感。")
            
        return {
            "画面感得分": sum(sensory_coverage.values()) + depth_score*10 + dynamic_score*10,
            "感官覆盖": sensory_coverage,
            "增强建议": suggestions
        }
```

### 2.2 情绪一致性维护器（Mood Consistency Guardian）

**目标**：保证氛围营造与目标情绪一致，检测不和谐的元素并调整。

**实现**：
- 使用情绪维度模型（如Valence-Arousal-Dominance，或基础愉悦度/唤醒度）。
- 将场景中的物体、色彩、声音、天气等映射为情绪向量。
- 计算整体向量与目标情绪的余弦相似度，低于阈值则标记冲突元素。

**处理流程**：

```
输入：场景文本 + 目标情绪（如“寂静中的不安”）
 → 提取元素及属性（例如：钟摆声——规律→平静，但音量突兀→不安）
 → 计算各元素情绪得分
 → 合成场景情绪向量
 → 对比目标向量
 → 输出不一致元素及替换方案
```

**伪代码**：

```python
class MoodConsistency:
    ELEMENT_MOOD_DB = {
        "暴雨": {"valence": -0.4, "arousal": 0.9, "dominance": -0.5},
        "壁炉火": {"valence": 0.7, "arousal": -0.2, "dominance": 0.4},
        # ... 预设库
    }
    
    def validate(self, scene_elements: list, target_mood: str) -> dict:
        target_vec = self.mood_to_vector(target_mood)
        total_vec = np.mean([self.ELEMENT_MOOD_DB[e] for e in scene_elements], axis=0)
        similarity = cosine_similarity(total_vec, target_vec)
        
        conflicts = []
        for elem in scene_elements:
            if cosine_similarity(self.ELEMENT_MOOD_DB[elem], target_vec) < 0.2:
                conflicts.append(elem)
        
        return {
            "情绪一致性": similarity,
            "冲突元素": conflicts,
            "调整建议": [f"将{el}替换为更符合‘{target_mood}’的物品" for el in conflicts]
        }
```

### 2.3 空间布局合理性验证器（Spatial Logic Validator）

**目标**：确保场景内物体位置、尺度、光影关系符合物理常识和连贯性。

**实现**：
- 构建简化的3D关系图谱（物体-相对位置-遮挡关系）。
- 规则检查引擎：
  - 物体不能悬空（除非说明漂浮）
  - 光源与阴影方向一致
  - 大小尺度合理（桌子上的茶杯不能比桌子大）
  - 门、窗等开口与朝向逻辑正确
- 可以调用简单物理常识库或常识推理API。

**示例规则**：

```python
class SpatialValidator:
    def validate(self, elements: list[dict]) -> list[str]:
        issues = []
        light_sources = [e for e in elements if e["type"] == "光源"]
        shadows = [e for e in elements if "阴影" in e.get("properties", [])]
        
        # 检查光源方向一致性
        for shadow in shadows:
            if not self.is_shadow_consistent(shadow, light_sources):
                issues.append(f"物体'{shadow['name']}'的阴影与光源方向矛盾。")
                
        # 检查支撑关系
        for obj in elements:
            if "支撑物" not in obj and obj.get("z_level", 0) > 0:
                issues.append(f"'{obj['name']}'处于高处但缺少支撑物。")
                
        # 尺度合理性（简单规则：容器内物体不大于容器）
        for container in elements:
            if container.get("contains"):
                for item in container["contains"]:
                    if item["scale"] > container["scale"]:
                        issues.append(f"'{item['name']}'的尺寸超过容器'{container['name']}'，请检查。")
        return issues
```

### 2.4 场景转换流畅度优化器（Transition Smoother）

**目标**：保证场景切换不突兀，提供衔接建议。

**策略**：
- 利用**感官桥梁**：当前场景的某种感官延续到下一场景（如声音、气味、触感）。
- **物体线索**：携带一个物品贯穿场景。
- **情感线索**：人物内心情绪作为连续体。
- **时空提示**：明确时间/空间过渡短语（“片刻之后”，“穿过走廊”）。

**实现**：

```python
class TransitionOptimizer:
    def suggest_transition(self, scene_from: str, scene_to: str) -> str:
        bridges = []
        # 提取前一场景的感官词
        sense_words = self.extract_senses(scene_from)
        # 提取后一场景可匹配的入口点
        entry_points = self.find_entry_points(scene_to, sense_words)
        
        if entry_points:
            bridge = f"延续着{entry_points[0]}的感觉，{self.generate_link(entry_points[0])}"
        else:
            # 默认使用时间/空间过渡
            bridge = "片刻之后，" if self.is_temporal(scene_to) else "穿过狭长的甬道，"
        
        return f"{scene_from}\n\n{bridge}\n\n{scene_to}"
```

### 2.5 场景信息记忆管理器（Scene Memory Manager）

**目标**：跨对话/跨章节记录已构建场景的关键信息，实现长期一致性。

**结构**：
- 使用**场景知识图谱**存储：地点、时间、天气、重要物品、在场角色、氛围基调。
- 按时间线索引，支持回溯和引用。
- 新场景创建时自动检索相关历史场景，防止矛盾。

**简化的存储接口**：

```python
class SceneMemory:
    def __init__(self):
        self.scene_db = {}  # scene_id -> SceneNode
        self.timeline = []
        
    def store(self, scene_id, metadata: dict):
        # metadata包含：位置、时间、角色、氛围、关键物品等
        node = SceneNode(metadata)
        self.scene_db[scene_id] = node
        self.timeline.append(scene_id)
        
    def query_relevant(self, current_metadata: dict) -> list:
        # 基于位置接近、时间顺序、人物重叠等返回相关历史场景
        pass
        
    def check_conflict(self, current_metadata: dict) -> list:
        # 检查是否与历史设定矛盾（如同一地点不同时间突然改变布局）
        pass
```

---

## 三、人性化升级详细方案

### 3.1 场景描写示例库（Inspiration Gallery）

**功能**：按类型、情绪、风格分类的例句库，支持搜索和“随机灵感”。

**结构设计**：
- 分类标签：中世纪城堡、赛博朋克城市、田园午后、暴雨夜等
- 每条示例包含：场景短文、五感标注、情绪标签、可复用句式
- 用户可收藏、自定义标签

**实现**：一个JSON文件或轻量数据库，通过简易前端/聊天界面调用。

**示例条目**：

```json
{
  "id": "medieval_tavern",
  "tags": ["中世纪","酒馆","热闹","木质"],
  "mood": "温暖喧闹",
  "text": "旧橡木吧台上烛油堆积如小山，琥珀色的麦酒在陶杯里漾出光晕。吟游诗人指间的鲁特琴散落跳跃音符，混着烤肉油脂的烟气与粗野笑声一起冲上熏黑的房梁。",
  "sensory_breakdown": {
    "视觉": ["橡木吧台","琥珀色酒液","烟熏房梁"],
    "听觉": ["琴声","笑声"],
    "嗅觉": ["烤肉","油脂"],
    "触觉": ["陶杯粗糙感","温暖壁炉"]
  }
}
```

### 3.2 情绪场景指南（Mood Palette）

**功能**：提供情绪-场景元素的映射关系，以**调色盘**形式可视化，帮助用户选择。

**实现方式**：交互式表格或卡片，例如：

| 欲表达情绪 | 推荐色彩 | 环境声 | 天气 | 典型物件 |
|------------|----------|--------|------|----------|
| 孤独 | 蓝灰、褪色黄 | 钟表滴答、风声 | 小雨或阴天 | 空椅、半杯冷茶 |
| 温馨 | 暖橙、柔黄 | 木柴噼啪、轻柔音乐 | 晴天或傍晚 | 毛毯、热饮 |

并提供“情绪混搭”检查，防止互相矛盾的元素组合。

### 3.3 场景转换衔接向导（Transition Wizard）

**功能**：当用户输入两个场景片段，自动生成3种以上衔接方式，并说明各自的叙事效果。

**交互示例**：
> 用户：“从激烈的战斗场景转换到宁静的回忆片段，该怎么接？”

助手回答提供：
1. **感官延续**：“刀剑碰撞声渐弱，取代它的是记忆里母亲轻哼的摇篮曲……”
2. **人物状态过渡**：“他跌坐在地，视野模糊，意识沉入多年前那个同样寒冷的午后……”
3. **物件线索**：“染血的挂坠从撕裂的甲胄中滑出，光泽引出一段尘封往事……”
并附带简要分析。

### 3.4 空间布局可视化描述（Spatial Visualizer）

**功能**：将文字布局转为简单ASCII示意图或生成SVG平面图。

**实现方案**：
- 解析空间描述中的方位词（左、右、前、后、中间、角落等）。
- 用2D网格坐标系统表示物体。
- 生成文本示意图或SVG。

**示例：输出房间布局的ASCII**：

```
[窗]────────────────────[窗]
  │ 书桌 台灯               │
  │    ↓                    │
  │   椅子                  │
  │        茶几──沙发       │
  │                        │
[门]────────────────────[书架]
```

对于更复杂的场景，可以调用绘图库输出简单图形。

### 3.5 新手友好的场景设计引导（Step-by-Step Scene Builder）

**引导流程**（对话式或表单式）：

1. **选择设定**：时代/风格/地点类型（下拉菜单+示例图片）
2. **确定情绪**：滑动条选择情绪维度，实时预览对应氛围短语
3. **添加核心元素**：向导分步提示：“现在请添加一个光源”、“描述地面材质”、“有一种特殊气味吗？”
4. **空间布局**：简易网格拖拽（Web端），或回复数字位置。
5. **预览与调整**：组合所有输入，生成初稿，并高亮可优化部分。
6. **提供一键复制、保存到记忆库**

**错误处理与容错**：若用户跳过某步或输入非常规内容，系统会使用合理默认值并提示“已添加默认黄昏光线，您可随时修改”。

---

## 四、实现框架整合（伪总控）

```python
class SceneBuilderSkill:
    def __init__(self):
        self.visual_checker = VisualIntensityChecker()
        self.mood_guardian = MoodConsistency()
        self.spatial_validator = SpatialValidator()
        self.transition_optimizer = TransitionOptimizer()
        self.memory = SceneMemory()
        self.example_lib = ExampleLibrary()
        self.guide = NewbieGuide()
        
    def generate_scene(self, requirements: dict, use_memory=True):
        # 1. 新手引导或快速模式
        if requirements.get("mode") == "guided":
            scene_basis = self.guide.interactive_build()
        else:
            scene_basis = self.assemble_from_requirements(requirements)
            
        # 2. 查询记忆，检查冲突
        if use_memory:
            conflicts = self.memory.check_conflict(scene_basis)
            if conflicts:
                scene_basis = self.resolve_conflicts(scene_basis, conflicts)
                
        # 3. 生成场景初稿
        draft = self.compose_text(scene_basis)
        
        # 4. 智能化检查与增强
        visual_feedback = self.visual_checker.check(draft)
        mood_feedback = self.mood_guardian.validate(scene_basis['mood_goal'])
        spatial_issues = self.spatial_validator.validate(scene_basis['elements'])
        
        # 5. 根据反馈优化
        final_scene = self.apply_enhancements(draft, visual_feedback, mood_feedback, spatial_issues)
        
        # 6. 存储到记忆
        self.memory.store(final_scene.id, final_scene.metadata)
        
        # 7. 生成可视化示意图（可选）
        layout_svg = None
        if requirements.get("visualize_layout"):
            layout_svg = self.generate_layout_svg(scene_basis['elements'])
            
        return {
            "text": final_scene,
            "suggestions": visual_feedback["增强建议"] + mood_feedback["调整建议"],
            "spatial_warnings": spatial_issues,
            "layout_svg": layout_svg,
            "related_examples": self.example_lib.search_similar(final_scene.mood)
        }
```

---

## 五、用户使用说明

### 5.1 快速开始
1. 直接输入场景需求，如：“一个雨夜中的维多利亚式咖啡馆，略带忧伤。”
2. 系统分析后生成描写，并附带优化建议。
3. 使用`/visual`命令查看画面感评分；`/layout`生成布局图；`/mood 目标情绪`调整氛围。

### 5.2 高级功能
- **衔接辅助**：输入`/transition 场景A文本 >> 场景B文本`获得衔接方案。
- **记忆库**：`/remember`存储当前场景，`/recall 地点/角色`调出相关历史。
- **示例浏览**：`/examples 赛博朋克`获取灵感。

### 5.3 新手学习路径
1. 完成引导式创建（选择“新手向导模式”）
2. 阅读内置的“场景创作小贴士”：五感描写技巧、情绪色彩搭配
3. 分析经典样例（库内带标注）
4. 尝试用`/check`分析自己的习作
5. 参与每日挑战（如：用三个限定词写场景）提高能力

### 5.4 错误处理与容错
- 输入模糊时：系统主动追问关键信息（时间/地点/氛围），而非直接生成不合理内容。
- 发现矛盾时：例如“明亮的月光下伸手不见五指”，系统提醒并给出修改建议，不会强行输出。
- 布局不合理：以⚠️标记并解释问题（如“根据描述，蜡烛在桌上，但桌子在人物背后，光源方向可疑”）。

---

通过上述升级，【场景构造师】将从单纯的文字生成工具蜕变为具备感知、记忆、辅导能力的智能场景设计伙伴，兼顾专业性和友好性。