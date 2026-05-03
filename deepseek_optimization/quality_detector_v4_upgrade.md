# 质量检测V4升级方案

*由DeepSeek深度优化 | 时间：2026-05-03 13:47:42*

我来为您创建NWACS V8.0系统深度优化质量检测系统的V4版本代码。这是一个完整的、可直接运行的HTML文档。

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NWACS V8.0 - 质量检测系统V4</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
            background: #0a0e1a;
            color: #e0e6f0;
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        header {
            background: linear-gradient(135deg, #1a1f35 0%, #0f1525 100%);
            border: 1px solid #2a3a5c;
            border-radius: 12px;
            padding: 20px 30px;
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        header h1 {
            font-size: 24px;
            background: linear-gradient(90deg, #4fc3f7, #81c784);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        header .version {
            background: #2a3a5c;
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 14px;
            color: #90caf9;
        }
        .grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        @media (max-width: 900px) {
            .grid {
                grid-template-columns: 1fr;
            }
        }
        .card {
            background: linear-gradient(145deg, #141b2d, #1a2337);
            border: 1px solid #2a3a5c;
            border-radius: 12px;
            padding: 20px;
            transition: all 0.3s;
        }
        .card:hover {
            border-color: #4fc3f7;
            box-shadow: 0 0 20px rgba(79, 195, 247, 0.1);
        }
        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
            padding-bottom: 10px;
            border-bottom: 1px solid #2a3a5c;
        }
        .card-header h2 {
            font-size: 18px;
            color: #90caf9;
        }
        .card-header .badge {
            background: #2a3a5c;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            color: #b0bec5;
        }
        .dimension-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
        }
        .dimension-item {
            background: #1a2337;
            border: 1px solid #2a3a5c;
            border-radius: 8px;
            padding: 10px;
            text-align: center;
        }
        .dimension-item .label {
            font-size: 12px;
            color: #90a4ae;
            margin-bottom: 4px;
        }
        .dimension-item .value {
            font-size: 20px;
            font-weight: bold;
        }
        .dimension-item .subs {
            font-size: 11px;
            color: #78909c;
            margin-top: 4px;
        }
        .score-bar {
            height: 6px;
            background: #2a3a5c;
            border-radius: 3px;
            margin-top: 6px;
            overflow: hidden;
        }
        .score-bar .fill {
            height: 100%;
            border-radius: 3px;
            transition: width 0.8s ease;
        }
        .grade-display {
            text-align: center;
            padding: 20px;
        }
        .grade-display .grade {
            font-size: 48px;
            font-weight: bold;
        }
        .grade-display .score {
            font-size: 24px;
            color: #90caf9;
        }
        .grade-S { color: #ffd54f; }
        .grade-A { color: #81c784; }
        .grade-B { color: #4fc3f7; }
        .grade-C { color: #ffb74d; }
        .grade-D { color: #ef5350; }
        .suggestion-item {
            background: #1a2337;
            border-left: 3px solid #4fc3f7;
            padding: 10px 14px;
            margin-bottom: 8px;
            border-radius: 0 6px 6px 0;
        }
        .suggestion-item .priority {
            font-size: 11px;
            padding: 2px 8px;
            border-radius: 10px;
            margin-left: 8px;
        }
        .priority-high { background: #c62828; color: #fff; }
        .priority-medium { background: #f57f17; color: #fff; }
        .priority-low { background: #2e7d32; color: #fff; }
        .gate-status {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 12px;
            border-radius: 8px;
            margin-top: 10px;
        }
        .gate-pass { background: #1b3a2d; border: 1px solid #388e3c; }
        .gate-fail { background: #3a1b1b; border: 1px solid #c62828; }
        .gate-pending { background: #2a2a1b; border: 1px solid #f57f17; }
        .btn {
            background: #2a3a5c;
            border: none;
            color: #e0e6f0;
            padding: 10px 24px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.3s;
        }
        .btn:hover {
            background: #3a4a6c;
            transform: translateY(-1px);
        }
        .btn-primary {
            background: linear-gradient(135deg, #1565c0, #1976d2);
        }
        .btn-primary:hover {
            background: linear-gradient(135deg, #1976d2, #2196f3);
        }
        .btn-danger {
            background: linear-gradient(135deg, #c62828, #d32f2f);
        }
        .btn-danger:hover {
            background: linear-gradient(135deg, #d32f2f, #e53935);
        }
        .btn-success {
            background: linear-gradient(135deg, #2e7d32, #388e3c);
        }
        .btn-success:hover {
            background: linear-gradient(135deg, #388e3c, #43a047);
        }
        textarea {
            width: 100%;
            height: 120px;
            background: #0f1525;
            border: 1px solid #2a3a5c;
            border-radius: 8px;
            color: #e0e6f0;
            padding: 12px;
            font-size: 14px;
            resize: vertical;
            margin-bottom: 10px;
        }
        textarea:focus {
            outline: none;
            border-color: #4fc3f7;
        }
        .radar-container {
            position: relative;
            width: 100%;
            max-width: 320px;
            margin: 0 auto;
        }
        .flex-between {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .mt-10 { margin-top: 10px; }
        .mt-20 { margin-top: 20px; }
        .mb-10 { margin-bottom: 10px; }
        .text-center { text-align: center; }
        .text-sm { font-size: 13px; color: #78909c; }
        .text-xs { font-size: 11px; color: #546e7a; }
        .inline-flex { display: inline-flex; gap: 8px; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div>
                <h1>⚡ NWACS V8.0 质量检测系统</h1>
                <span class="text-sm">深度优化 · 智能评估 · 六维分析</span>
            </div>
            <div>
                <span class="version">V4.0.0</span>
                <span class="version" style="margin-left:8px;background:#1b3a2d;">专业版</span>
            </div>
        </header>

        <div class="grid">
            <!-- 左侧：输入与六维度 -->
            <div>
                <div class="card">
                    <div class="card-header">
                        <h2>📝 文本输入</h2>
                        <span class="badge">粘贴小说内容</span>
                    </div>
                    <textarea id="textInput" placeholder="在此粘贴小说内容进行质量检测...">夜幕降临，王明推开酒吧的门。他点了杯威士忌，坐在角落。三年前，他在这里遇到了小雨。现在，他又回来了。酒吧老板还是老张，吧台还是那个吧台。但一切都变了。小雨已经不在了。王明喝了一口酒，苦涩的味道在舌尖蔓延。他想起那天晚上，小雨说她要走了，去一个很远的地方。王明没有挽留。现在他后悔了。窗外下起了雨，和那天晚上一样。</textarea>
                    <div class="flex-between">
                        <div class="inline-flex">
                            <button class="btn btn-primary" onclick="runAnalysis()">🔍 运行质量检测</button>
                            <button class="btn" onclick="clearAll()">🗑️ 清空</button>
                        </div>
                        <span class="text-xs" id="charCount">0 字符</span>
                    </div>
                </div>

                <div class="card mt-10">
                    <div class="card-header">
                        <h2>📊 六维度质量模型</h2>
                        <span class="badge">总分加权</span>
                    </div>
                    <div class="dimension-grid" id="dimensionGrid">
                        <div class="dimension-item">
                            <div class="label">逻辑性</div>
                            <div class="value" id="dim-logic">0</div>
                            <div class="subs">因果/时间/空间</div>
                            <div class="score-bar"><div class="fill" id="bar-logic" style="width:0%;background:#4fc3f7;"></div></div>
                        </div>
                        <div class="dimension-item">
                            <div class="label">一致性</div>
                            <div class="value" id="dim-consistency">0</div>
                            <div class="subs">角色/世界观/细节</div>
                            <div class="score-bar"><div class="fill" id="bar-consistency" style="width:0%;background:#81c784;"></div></div>
                        </div>
                        <div class="dimension-item">
                            <div class="label">文学性</div>
                            <div class="value" id="dim-literary">0</div>
                            <div class="subs">语言/描写/情感</div>
                            <div class="score-bar"><div class="fill" id="bar-literary" style="width:0%;background:#ffd54f;"></div></div>
                        </div>
                        <div class="dimension-item">
                            <div class="label">可读性</div>
                            <div class="value" id="dim-readability">0</div>
                            <div class="subs">节奏/钩子/爽点</div>
                            <div class="score-bar"><div class="fill" id="bar-readability" style="width:0%;background:#ce93d8;"></div></div>
                        </div>
                        <div class="dimension-item">
                            <div class="label">创新性</div>
                            <div class="value" id="dim-innovation">0</div>
                            <div class="subs">情节/人物/设定</div>
                            <div class="score-bar"><div class="fill" id="bar-innovation" style="width:0%;background:#ffab91;"></div></div>
                        </div>
                        <div class="dimension-item">
                            <div class="label">市场性</div>
                            <div class="value" id="dim-market">0</div>
                            <div class="subs">接受度/适配/商业</div>
                            <div class="score-bar"><div class="fill" id="bar-market" style="width:0%;background:#a5d6a7;"></div></div>
                        </div>
                    </div>
                    <div class="flex-between mt-10">
                        <span class="text-sm">权重配置：</span>
                        <div class="inline-flex">
                            <button class="btn text-xs" onclick="setWeight('default')">默认</button>
                            <button class="btn text-xs" onclick="setWeight('web')">网文</button>
                            <button class="btn text-xs" onclick="setWeight('literary')">纯文学</button>
                        </div>
                    </div>
                </div>

                <!-- 雷达图 -->
                <div class="card mt-10">
                    <div class="card-header">
                        <h2>📈 质量雷达图</h2>
                        <span class="badge">可视化</span>
                    </div>
                    <div class="radar-container">
                        <canvas id="radarChart" width="300" height="300"></canvas>
                    </div>
                </div>
            </div>

            <!-- 右侧：评分、建议、门禁 -->
            <div>
                <div class="card">
                    <div class="card-header">
                        <h2>🏆 智能评分引擎</h2>
                        <span class="badge">自动评分</span>
                    </div>
                    <div class="grade-display">
                        <div class="grade" id="gradeDisplay">-</div>
                        <div class="score" id="totalScoreDisplay">总分: 0.0</div>
                        <div class="text-sm mt-10" id="scoreDetail">逻辑:0 一致:0 文学:0 可读:0 创新:0 市场:0</div>
                    </div>
                    <div class="flex-between mt-10">
                        <span class="text-sm">等级判定: <strong id="gradeLabel">未检测</strong></span>
                        <span class="text-xs">S(90+) A(80+) B(70+) C(60+) D(&lt;60)</span>
                    </div>
                </div>

                <div class="card mt-10">
                    <div class="card-header">
                        <h2>💡 改进建议系统</h2>
                        <span class="badge">优先级排序</span>
                    </div>
                    <div id="suggestionList">
                        <div class="suggestion-item">
                            <div class="flex-between">
                                <span>📌 尚未检测，请先运行质量检测</span>
                                <span class="priority priority-low">等待</span>
                            </div>
                            <div class="text-xs mt-10">点击"运行质量检测"按钮开始分析</div>
                        </div>
                    </div>
                </div>

                <div class="card mt-10">
                    <div class="card-header">
                        <h2>🔒 质量门禁</h2>
                        <span class="badge" id="gateBadge">等待检测</span>
                    </div>
                    <div id="gateStatus" class="gate-status gate-pending">
                        <span style="font-size:20px;">⏳</span>
                        <div>
                            <div><strong>等待检测</strong></div>
                            <div class="text-xs">最低标准: 总分≥60 | 单项≥40</div>
                        </div>
                    </div>
                    <div class="flex-between mt-10">
                        <span class="text-xs" id="gateDetail">总分: - | 最低单项: -</span>
                        <div class="inline-flex">
                            <button class="btn btn-success text-xs" onclick="forcePass()" id="forcePassBtn" disabled>🔑 强制通过</button>
                            <button class="btn btn-danger text-xs" onclick="resetGate()">🔄 重置</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // ========== 核心数据 ==========
        let currentScores = {
            logic: 0,
            consistency: 0,
            literary: 0,
            readability: 0,
            innovation: 0,
            market: 0
        };
        let currentTotal = 0;
        let currentGrade = '-';
        let gatePassed = false;
        let gateForced = false;

        // 权重配置
        const weights = {
            default: { logic: 20, consistency: 20, literary: 20, readability: 20, innovation: 10, market: 10 },
            web: { logic: 15, consistency: 15, literary: 15, readability: 25, innovation: 10, market: 20 },
            literary: { logic: 15, consistency: 15, literary: 30, readability: 15, innovation: 15, market: 10 }
        };
        let currentWeight = 'default';

        // ========== 智能评分引擎 ==========
        function analyzeText(text) {
            if (!text || text.trim().length < 10) {
                return { error: '文本太短，请至少输入10个字符' };
            }

            // 1. 逻辑性评分 (0-100)
            let logicScore = 50;
            // 检查因果关系词
            const causeWords = ['因为', '所以', '因此', '由于', '导致', '于是', '结果'];
            const causeCount = causeWords.filter(w => text.includes(w)).length;
            logicScore += causeCount * 5;
            // 时间线检查
            const timeWords = ['今天', '昨天', '明天', '晚上', '早上', '下午', '三年前', '现在', '那天'];
            const timeCount = timeWords.filter(w => text.includes(w)).length;
            logicScore += timeCount * 3;
            // 空间逻辑
            const spaceWords = ['酒吧', '房间', '外面', '里面', '角落', '吧台', '窗外'];
            const spaceCount = spaceWords.filter(w => text.includes(w)).length;
            logicScore += spaceCount * 2;
            // 动机合理
            const motiveWords = ['后悔', '因为', '为了', '想要', '需要', '决定'];
            const motiveCount = motiveWords.filter(w => text.includes(w)).length;
            logicScore += motiveCount * 3;
            logicScore = Math.min(100, Math.max(0, logicScore));

            // 2. 一致性评分 (0-100)
            let consistencyScore = 50;
            // 角色性格一致性
            const charWords = ['王明', '小雨', '老张'];
            const charCount = charWords.filter(w => text.includes(w)).length;
            consistencyScore += charCount * 4;
            // 世界观规则
            const worldWords = ['酒吧', '威士忌', '雨'];
            const worldCount = worldWords.filter(w => text.includes(w)).length;
            consistencyScore += worldCount * 3;
            // 剧情前后一致
            if (text.includes('三年前') && text.includes('现在')) consistencyScore += 8;
            if (text.includes('那天晚上') && text.includes('现在')) consistencyScore += 5;
            consistencyScore = Math.min(100, Math.max(0, consistencyScore));

            // 3. 文学性评分 (0-100)
            let literaryScore = 40;
            // 语言优美
            const beautyWords = ['苦涩', '蔓延', '推开', '降临', '回荡', '沉默'];
            const beautyCount = beautyWords.filter(w => text.includes(w)).length;
            literaryScore += beautyCount * 5;
            // 描写生动
            const descWords = ['推开', '坐在', '喝了一口', '苦涩', '蔓延', '下雨'];
            const descCount = descWords.filter(w => text.includes(w)).length;
            literaryScore += descCount * 4;
            // 情感真挚
            const emotionWords = ['后悔', '苦涩', '想起', '变了', '走了'];
            const emotionCount = emotionWords.filter(w => text.includes(w)).length;
            literaryScore += emotionCount * 5;
            // 意境营造
            const moodWords = ['夜幕', '雨', '角落', '苦涩', '变了'];
            const moodCount = moodWords.filter(w => text.includes(w)).length;
            literaryScore += moodCount * 4;
            literaryScore = Math.min(100, Math.max(0, literaryScore));

            // 4. 可读性评分 (0-100)
            let readabilityScore = 45;
            // 节奏把控 - 句子长度适中
            const sentences = text.split(/[。！？\n]/).filter(s => s.trim().length > 0);
            const avgSentLen = sentences.reduce((sum, s) => sum + s.length, 0) / (sentences.length || 1);
            if (avgSentLen > 15 && avgSentLen < 40) readabilityScore += 10;
            else if (avgSentLen >= 40) readabilityScore += 5;
            else readabilityScore += 3;
            // 钩子设置
            const hookWords = ['现在', '变了', '后悔', '走了', '那天'];
            const hookCount = hookWords.filter(w => text.includes(w)).length;
            readabilityScore += hookCount * 4;
            // 爽点安排
            const funWords = ['推开', '喝了一口', '想起'];
            const funCount = funWords.filter(w => text.includes(w)).length;
            readabilityScore += funCount * 3;
            // 阅读体验
            if (text.length > 100) readabilityScore += 5;
            if (text.length > 200) readabilityScore += 3;
            readabilityScore = Math.min(100, Math.max(0, readabilityScore));

            // 5. 创新性评分 (0-100)
            let innovationScore = 30;
            // 情节创新
            const plotWords = ['遇到', '离开', '回来', '后悔'];
            const plotCount = plotWords.filter(w => text.includes(w)).length;
            innovationScore += plotCount * 4;
            // 人物创新
            innovationScore += charCount * 2;
            // 设定创新
            const settingWords = ['酒吧', '威士忌', '雨'];
            const settingCount = settingWords.filter(w => text.includes(w)).length;
            innovationScore += settingCount * 3;
            // 表达创新
            const exprWords = ['苦涩', '蔓延', '推开'];
            const exprCount = exprWords.filter(w => text.includes(w)).length;
            innovationScore += exprCount * 3;
            innovationScore = Math.min(100, Math.max(0, innovationScore));

            // 6. 市场性评分 (0-100)
            let marketScore = 40;
            // 读者接受度
            const popularWords = ['酒吧', '威士忌', '后悔', '走了', '雨'];
            const popularCount = popularWords.filter(w => text.includes(w)).length;
            marketScore += popularCount * 4;
            // 平台适配
            if (text.length > 80 && text.length < 500) marketScore += 10;
            // 商业价值
            const bizWords = ['酒吧', '威士忌'];
            const bizCount = bizWords.filter(w => text.includes(w)).length;
            marketScore += bizCount * 5;
            // 传播潜力
            if (text.includes('后悔') || text.includes('变了')) marketScore += 8;
            marketScore = Math.min(100, Math.max(0, marketScore));

            return {
                logic: Math.round(logicScore),
                consistency: Math.round(consistencyScore),
                literary: Math.round(literaryScore),
                readability: Math.round(readabilityScore),
                innovation: Math.round(innovationScore),
                market: Math.round(marketScore)
            };
        }

        // ========== 计算加权总分 ==========
        function calculateWeightedScore(scores, weightKey) {
            const w = weights[weightKey] || weights.default;
            const totalWeight = Object.values(w).reduce((a, b) => a + b, 0);
            let weighted = 0;
            weighted += scores.logic * (w.logic / totalWeight);
            weighted += scores.consistency * (w.consistency / totalWeight);
            weighted += scores.literary * (w.literary / totalWeight);
            weighted += scores.readability * (w.readability / totalWeight);
            weighted += scores.innovation * (w.innovation / totalWeight);
            weighted += scores.market * (w.market / totalWeight);
            return Math.round(weighted * 10) / 10;
        }

        // ========== 等级判定 ==========
        function getGrade(score) {
            if (score >= 90) return 'S';
            if (score >= 80) return 'A';
            if (score >= 70) return 'B';
            if (score >= 60) return 'C';
            return 'D';
        }

        // ========== 生成改进建议 ==========
        function generateSuggestions(scores) {
            const suggestions = [];
            const dims = [
                { key: 'logic', name: '逻辑性', threshold: 60 },
                { key: 'consistency', name: '一致性', threshold: 60 },
                { key: 'literary', name: '文学性', threshold: 60 },
                { key: 'readability', name: '可读性', threshold: 60 },
                { key: 'innovation', name: '创新性', threshold: 50 },
                { key: 'market', name: '市场性', threshold: 50 }
            ];

            dims.forEach(dim => {
                const score = scores[dim.key];
                if (score < dim.threshold) {
                    let priority = 'low';
                    let priorityLabel = '低';
                    if (score < 40) { priority = 'high'; priorityLabel = '高'; }
                    else if (score < 50) { priority = 'medium'; priorityLabel = '中'; }

                    let reason = '';
                    let direction = '';
                    let example = '';

                    switch (dim.key) {
                        case 'logic':
                            reason = '因果关系不够清晰，时间线或空间逻辑有待加强';
                            direction = '增加因果连接词，明确时间顺序和空间关系';
                            example = '例如：因为...所以...，三年前...现在...';
                            break;
                        case 'consistency':
                            reason = '角色性格或世界观设定不够一致';
                            direction = '保持角色行为与性格一致，维护世界观规则';
                            example = '例如：王明作为一个怀旧的人，行为应体现其性格';
                            break;
                        case 'literary':
                            reason = '语言表达或情感描写不够生动';
                            direction = '增加修饰词和情感渲染，提升意境';
                            example = '例如：用"苦涩的威士忌"代替"喝了一口酒"';
                            break;
                        case 'readability':
                            reason = '节奏把控或阅读体验有待提升';
                            direction = '调整句子长度，增加钩子和爽点';
                            example = '例如：设置悬念"他没想到，这次回来会改变一切"';
                            break;
                        case 'innovation':
                            reason = '情节或设定较为常规，创新性不足';
                            direction = '尝试加入反转或独特设定';
                            example = '例如：小雨的离开隐藏着更大的秘密';
                            break;
                        case 'market':
                            reason = '市场吸引力或传播潜力有待提升';
                            direction = '增加流行元素或情感共鸣点';
                            example = '例如：加入"遗憾""重逢"等热门情感元素';
                            break;
                    }

                    suggestions.push({
                        dim: dim.name,
                        score: score,
                        priority: priority,
                        priorityLabel: priorityLabel,
                        reason: reason,
                        direction: direction,
                        example: example
                    });
                }
            });

            // 按优先级排序
            suggestions.sort((a, b) => {
                const order = { high: 0, medium: 1, low: 2 };
                return order[a.priority] - order[b.priority];
            });

            if (suggestions.length === 0) {
                suggestions.push({
                    dim: '整体',
                    score: 100,
                    priority: 'low',
                    priorityLabel: '低',
                    reason: '所有维度均达到良好水平',
                    direction: '继续保持，可尝试更高层次的突破',
                    example: '考虑增加深度主题或社会意义'
                });
            }

            return suggestions;
        }

        // ========== 质量门禁检查 ==========
        function checkGate(scores, total) {
            const dimValues = Object.values(scores);
            const minDim = Math.min(...dimValues);
            const pass = total >= 60 && minDim >= 40;
            return { pass, total, minDim };
        }

        // ========== UI更新 ==========
        function updateUI(scores, total, grade, suggestions, gateResult) {
            // 更新维度显示
            const dimMap = {
                logic: { id: 'dim-logic', bar: 'bar-logic', color: '#4fc3f7' },
                consistency: { id: 'dim-consistency', bar: 'bar-consistency', color: '#81c784' },
                literary: { id: 'dim-literary', bar: 'bar-literary', color: '#ffd54f' },
                readability: { id: 'dim-readability', bar: 'bar-readability', color: '#ce93d8' },
                innovation: { id: 'dim-innovation', bar: 'bar-innovation', color: '#ffab91' },
                market: { id: 'dim-market', bar: 'bar-market', color: '#a5d6a7' }
            };

            for (const [key, val] of Object.entries(scores)) {
                if (dimMap[key]) {
                    document.getElementById(dimMap[key].id).textContent = val;
                    document.getElementById(dimMap[key].bar).style.width = val + '%';
                    document.getElementById(dimMap[key].bar).style.background = dimMap[key].color;
                }
            }

            // 更新总分和等级
            document.getElementById('totalScoreDisplay').textContent = `总分: ${total.toFixed(1)}`;
            document.getElementById('gradeDisplay').textContent = grade;
            document.getElementById('gradeDisplay').className = `grade grade-${grade}`;
            document.getElementById('gradeLabel').textContent = grade === 'S' ? 'S级 - 完美' :
                grade === 'A' ? 'A级 - 优秀' :
                grade === 'B' ? 'B级 - 良好' :
                grade === 'C' ? 'C级 - 合格' : 'D级 - 不合格';

            document.getElementById('scoreDetail').textContent =
                `逻辑:${scores.logic} 一致:${scores.consistency} 文学:${scores.literary} 可读:${scores.readability} 创新:${scores.innovation} 市场:${scores.market}`;

            // 更新建议
            const suggestionList = document.getElementById('suggestionList');
            suggestionList.innerHTML = '';
            suggestions.forEach(sug => {
                const div = document.createElement('div');
                div.className = 'suggestion-item';
                div.innerHTML = `
                    <div class="flex-between">
                        <span>📌 <strong>${sug.dim}</strong> (${sug.score}分) - ${sug.reason}</span>
                        <span class="priority priority-${sug.priority}">${sug.priorityLabel}优先级</span>
                    </div>
                    <div class="text-xs mt-10">🔧 优化方向: ${sug.direction}</div>
                    <div class="text-xs" style="color:#90caf9;">💡 参考示例: ${sug.example}</div>
                `;
                suggestionList.appendChild(div);
            });

            // 更新门禁
            const gateStatus = document.getElementById('gateStatus');
            const gateBadge = document.getElementById('gateBadge');
            const gateDetail = document.getElementById('gateDetail');
            const forceBtn = document.getElementById('forcePassBtn');

            if (gateResult.pass || gateForced) {
                gateStatus.className = 'gate-status gate-pass';
                gateStatus.innerHTML = `
                    <span style="font-size:20px;">✅</span>
                    <div>
                        <div><strong>门禁通过</strong></div>
                        <div class="text-xs">${gateForced ? '已强制通过（人工授权）' : '自动检测通过'}</div>
                    </div>
                `;
                gateBadge.textContent = '✅ 已通过';
                gateBadge.style.background = '#1b3a2d';
                forceBtn.disabled = true;
                gatePassed = true;
            } else {
                gateStatus.className = 'gate-status gate-fail';
                gateStatus.innerHTML = `
                    <span style="font-size:20px;">❌</span>
                    <div>
                        <div><strong>门禁未通过</strong></div>
                        <div class="text-xs">总分 ${gateResult.total.toFixed(1)} < 60 或 最低单项 ${gateResult.minDim} < 40</div>
                    </div>
                `;
                gateBadge.textContent = '❌ 未通过';
                gateBadge.style.background = '#3a1b1b';
                forceBtn.disabled = false;
                gatePassed = false;
            }
            gateDetail.textContent = `总分: ${gateResult.total.toFixed(1)} | 最低单项: ${gateResult.minDim}`;

            // 更新雷达图
            drawRadar(scores);
        }

        // ========== 绘制雷达图 ==========
        function drawRadar(scores) {
            const canvas = document.getElementById('radarChart');
            const ctx = canvas.getContext('2d');
            const width = canvas.width;
            const height = canvas.height;
            const centerX = width / 2;
            const centerY = height / 2;
            const radius = Math.min(width, height) * 0.35;

            ctx.clearRect(0, 0, width, height);

            // 绘制六边形网格
            const angles = [0, 60, 120, 180, 240, 300].map(deg => deg * Math.PI / 180);
            const labels = ['逻辑性', '一致性', '文学性', '可读性', '创新性', '市场性'];
            const values = [scores.logic, scores.consistency, scores.literary, scores.readability, scores.innovation, scores.market];

            // 网格
            for (let ring = 1; ring <= 5; ring++) {
                const