# 🚀 NWACS v7.0 API服务使用说明

**版本**: v1.0
**更新时间**: 2026-05-02

---

## 📖 概述

NWACS API服务是连接Web UI和核心引擎的桥梁，让用户可以通过浏览器使用NWACS的全部功能。

### 功能

- ✅ RESTful API接口
- ✅ Web UI后端支持
- ✅ 小说创作接口
- ✅ 质量检查接口
- ✅ 知识库查询接口
- ✅ 系统状态接口

---

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install flask openai
```

### 2. 启动服务

双击 `启动API服务.bat`

或命令行运行：
```bash
python core/api_server.py
```

### 3. 访问Web UI

浏览器打开：`http://localhost:5000`

---

## 🌐 API接口列表

### 健康检查

**GET** `/api/health`

检查服务是否正常运行。

```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "version": "v7.0",
    "api_configured": true
  }
}
```

### 获取小说类型

**GET** `/api/novel-types`

获取支持的小说类型列表。

```json
{
  "success": true,
  "data": [
    {"id": "xuanhuan", "name": "玄幻仙侠", "icon": "🐉", "description": "修仙、玄幻、仙侠"},
    {"id": "dushi", "name": "都市言情", "icon": "🏙️", "description": "都市、言情、职场"},
    ...
  ]
}
```

### 创建小说章节

**POST** `/api/create`

创作小说章节。

**请求体**:
```json
{
  "novel_type": "xuanhuan",
  "chapter_title": "第一章 废物崛起",
  "prompt": "写一个废柴逆袭的玄幻开篇，主角被未婚妻退婚",
  "word_count": 3000
}
```

**响应**:
```json
{
  "success": true,
  "message": "创作成功",
  "data": {
    "title": "第一章 废物崛起",
    "content": "青云宗大殿...",
    "novel_type": "xuanhuan",
    "word_count": 3200
  }
}
```

### 质量检查

**POST** `/api/quality-check`

检查文本质量。

**请求体**:
```json
{
  "text": "要检查的文本内容..."
}
```

**响应**:
```json
{
  "success": true,
  "data": {
    "word_count": 1500,
    "sentence_count": 50,
    "avg_sentence_length": 30.0,
    "readability_score": 75,
    "readability_level": "易读"
  }
}
```

### 获取知识库

**GET** `/api/knowledge-bases`

获取知识库列表。

```json
{
  "success": true,
  "data": [
    {"name": "玄幻修仙小说知识库.txt", "path": "skills/level2/learnings/玄幻修仙小说知识库.txt"},
    ...
  ]
}
```

### 获取系统统计

**GET** `/api/stats`

获取系统统计信息。

```json
{
  "success": true,
  "data": {
    "python_files": 135,
    "markdown_files": 435,
    "level3_skills": 28,
    "level2_skills": 30,
    "knowledge_bases": 32,
    "version": "v7.0",
    "architecture": "v2.2"
  }
}
```

---

## 💻 代码调用示例

### Python调用

```python
import requests

# 创建章节
response = requests.post('http://localhost:5000/api/create', json={
    'novel_type': 'xuanhuan',
    'chapter_title': '第一章',
    'prompt': '写一个废柴逆袭的开篇',
    'word_count': 3000
})

result = response.json()
if result['success']:
    print(result['data']['content'])
```

### JavaScript调用

```javascript
// 创建章节
fetch('http://localhost:5000/api/create', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        novel_type: 'xuanhuan',
        chapter_title: '第一章',
        prompt: '写一个废柴逆袭的开篇',
        word_count: 3000
    })
})
.then(res => res.json())
.then(data => {
    if (data.success) {
        console.log(data.data.content);
    }
});
```

---

## ⚙️ 配置说明

API使用环境变量或默认配置：

- `DEEPSEEK_API_KEY` - DeepSeek API密钥
- 默认密钥已配置：`sk-f3246fbd1eef446e9a11d78efefd9bba`

---

## 🔧 故障排除

### 问题1：端口被占用

```
Error: Port 5000 is already in use
```

解决方法：
1. 关闭占用5000端口的程序
2. 或修改端口：编辑 `api_server.py`，将 `port=5000` 改为其他端口

### 问题2：API Key无效

```
Error: Invalid API key
```

解决方法：
1. 检查 `core/api_server.py` 中的API_KEY
2. 或设置环境变量：`set DEEPSEEK_API_KEY=your-key`

### 问题3：Web UI无法连接

```
Failed to fetch
```

解决方法：
1. 确认API服务正在运行
2. 确认浏览器访问地址正确
3. 检查防火墙设置

---

## 📁 相关文件

| 文件 | 说明 |
|------|------|
| `core/api_server.py` | API服务主程序 |
| `启动API服务.bat` | 启动脚本 |
| `web_ui/index.html` | Web UI界面 |
| `docs/guides/API使用说明.md` | 本文档 |

---

## 🎯 下一步

1. 启动API服务：`双击 启动API服务.bat`
2. 访问Web UI：`浏览器打开 http://localhost:5000`
3. 开始创作：选择类型，输入需求，生成章节！

---

*API服务版本: v1.0 | 更新时间: 2026-05-02*
