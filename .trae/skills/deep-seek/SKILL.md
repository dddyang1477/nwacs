---
name: "deep-seek"
description: "调用DeepSeek API进行AI对话和任务处理。Invoke when user wants to use DeepSeek AI for conversations, Q&A, writing assistance, or code generation."
---

# DeepSeek AI 调用助手

本技能用于通过DeepSeek API进行AI对话和任务处理。

## 配置

### 获取API密钥
1. 访问 [DeepSeek Platform](https://platform.deepseek.com/)
2. 注册账号并获取API密钥
3. 将API密钥设置为环境变量 `DEEPSEEK_API_KEY`

## 使用方法

### 基本对话调用

```python
import os
import requests

def chat_with_deepseek(prompt, model="deepseek-chat"):
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        return "错误：请设置DEEPSEEK_API_KEY环境变量"

    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"请求错误: {str(e)}"

# 示例对话
result = chat_with_deepseek("你好，请介绍一下你自己")
print(result)
```

### 使用DeepSeek-Coder进行代码生成

```python
def code_with_deepseek(prompt, model="deepseek-coder"):
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        return "错误：请设置DEEPSEEK_API_KEY环境变量"

    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=60)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"请求错误: {str(e)}"

# 代码生成示例
code = code_with_deepseek("用Python写一个快速排序算法")
print(code)
```

### 多轮对话

```python
def multi_turn_chat(messages, model="deepseek-chat"):
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        return "错误：请设置DEEPSEEK_API_KEY环境变量"

    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": model,
        "messages": messages
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"请求错误: {str(e)}"

# 多轮对话示例
messages = [
    {"role": "system", "content": "你是一个乐于助人的助手"},
    {"role": "user", "content": "什么是Python？"},
    {"role": "assistant", "content": "Python是一种高级编程语言..."},
    {"role": "user", "content": "它适合做什么开发？"}
]
response = multi_turn_chat(messages)
print(response)
```

## 可用模型

| 模型名称 | 说明 |
|---------|------|
| `deepseek-chat` | 通用对话模型 |
| `deepseek-coder` | 代码生成模型 |

## 注意事项

1. **API安全性**: 不要在代码中硬编码API密钥，使用环境变量
2. **成本控制**: DeepSeek API按token计费，注意监控使用量
3. **错误处理**: 实现适当的错误处理以应对网络问题或API限制
4. **超时设置**: 建议设置合理的超时时间避免长时间等待

## 环境变量配置

在Windows系统中设置环境变量：
```cmd
setx DEEPSEEK_API_KEY "your-api-key-here"
```

或使用Python的dotenv库：
```python
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")
```
