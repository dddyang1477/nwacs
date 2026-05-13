#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 统一大模型接口层 - LLMInterface
核心功能：
1. 多模型支持 - DeepSeek / OpenAI兼容 / 本地模型
2. 流式输出 - SSE (Server-Sent Events) 实时返回
3. 智能重试 - 指数退避 + 抖动
4. 速率限制 - 令牌桶算法
5. 参数调优 - temperature/top_p/frequency_penalty/presence_penalty
6. 模型配置 - 环境变量 + 配置文件双重支持
7. 会话管理 - 多轮对话上下文
"""

import os
import json
import time
import random
import threading
import logging
from typing import Dict, List, Optional, Any, Generator, Callable
from dataclasses import dataclass, field
from enum import Enum
from collections import deque

logger = logging.getLogger("LLMInterface")

DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'llm_config.json')


class ModelProvider(Enum):
    DEEPSEEK = "deepseek"
    OPENAI = "openai"
    ZHIPU = "zhipu"
    MOONSHOT = "moonshot"
    QWEN = "qwen"
    CUSTOM = "custom"


@dataclass
class ModelConfig:
    provider: ModelProvider = ModelProvider.DEEPSEEK
    model_name: str = "deepseek-chat"
    api_key: str = ""
    base_url: str = "https://api.deepseek.com"
    temperature: float = 0.7
    top_p: float = 0.9
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    max_tokens: int = 4096
    timeout: int = 120
    max_retries: int = 3
    retry_delay_base: float = 1.0
    retry_delay_max: float = 30.0


@dataclass
class GenerationParams:
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    frequency_penalty: Optional[float] = None
    presence_penalty: Optional[float] = None
    max_tokens: Optional[int] = None
    stop: Optional[List[str]] = None
    system_prompt: Optional[str] = None


class CircuitBreaker:
    """熔断器 — 防止连续失败导致无限重试"""

    def __init__(self, failure_threshold: int = 5, recovery_timeout: float = 30.0):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self._failure_count = 0
        self._last_failure_time = 0.0
        self._state = "closed"  # closed / open / half-open
        self._lock = threading.Lock()

    def record_failure(self):
        with self._lock:
            self._failure_count += 1
            self._last_failure_time = time.monotonic()
            if self._failure_count >= self.failure_threshold:
                self._state = "open"
                logger.warning(f"Circuit breaker OPEN after {self._failure_count} failures")

    def record_success(self):
        with self._lock:
            self._failure_count = 0
            self._state = "closed"

    def is_allowed(self) -> bool:
        with self._lock:
            if self._state == "closed":
                return True
            if self._state == "open":
                if time.monotonic() - self._last_failure_time > self.recovery_timeout:
                    self._state = "half-open"
                    logger.info("Circuit breaker half-open, allowing test request")
                    return True
                return False
            return True  # half-open: allow one test request

    @property
    def state(self):
        return self._state


class TokenBucket:
    """令牌桶速率限制器"""

    def __init__(self, rate: float, burst: int):
        self.rate = rate
        self.burst = burst
        self.tokens = float(burst)
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

    def acquire(self, tokens: int = 1) -> bool:
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill
            self.tokens = min(self.burst, self.tokens + elapsed * self.rate)
            self.last_refill = now

            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False

    def wait_and_acquire(self, tokens: int = 1, timeout: float = 60.0) -> bool:
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if self.acquire(tokens):
                return True
            time.sleep(0.5)
        return False


class LLMInterface:
    """统一大模型接口"""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config: ModelConfig = None, config_path: str = None):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True

        self.config = config or self._load_config(config_path)
        self._session_store: Dict[str, List[Dict]] = {}
        self._rate_limiters: Dict[str, TokenBucket] = {}
        self._init_rate_limiters()
        self._callbacks: Dict[str, List[Callable]] = {
            'on_generate_start': [],
            'on_generate_chunk': [],
            'on_generate_end': [],
            'on_error': [],
        }
        self._circuit_breaker = CircuitBreaker(failure_threshold=5, recovery_timeout=30.0)
        self._total_api_calls = 0
        self._max_api_calls_per_operation = 20
        self._operation_api_calls = 0

    def _load_config(self, config_path: str = None) -> ModelConfig:
        path = config_path or DEFAULT_CONFIG_PATH
        config = ModelConfig()

        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                config.provider = ModelProvider(data.get('provider', 'deepseek'))
                config.model_name = data.get('model_name', 'deepseek-chat')
                config.api_key = data.get('api_key', '')
                config.base_url = data.get('base_url', 'https://api.deepseek.com')
                config.temperature = data.get('temperature', 0.7)
                config.top_p = data.get('top_p', 0.9)
                config.max_tokens = data.get('max_tokens', 4096)
                config.timeout = data.get('timeout', 120)
                config.max_retries = data.get('max_retries', 3)
            except Exception as e:
                logger.warning(f"Config load failed: {e}, using defaults")

        if not config.api_key:
            config.api_key = os.environ.get(
                'DEEPSEEK_API_KEY',
                os.environ.get('OPENAI_API_KEY', 'sk-f3246fbd1eef446e9a11d78efefd9bba')
            )

        return config

    def _init_rate_limiters(self):
        self._rate_limiters['deepseek'] = TokenBucket(rate=5.0, burst=10)
        self._rate_limiters['openai'] = TokenBucket(rate=3.0, burst=5)

    def on(self, event: str, callback: Callable):
        if event in self._callbacks:
            self._callbacks[event].append(callback)

    def _emit(self, event: str, *args, **kwargs):
        for cb in self._callbacks.get(event, []):
            try:
                cb(*args, **kwargs)
            except Exception as e:
                logger.warning(f"Callback error for event '{event}': {e}")

    def update_config(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)

    def save_config(self, path: str = None):
        path = path or DEFAULT_CONFIG_PATH
        data = {
            'provider': self.config.provider.value,
            'model_name': self.config.model_name,
            'api_key': self.config.api_key,
            'base_url': self.config.base_url,
            'temperature': self.config.temperature,
            'top_p': self.config.top_p,
            'max_tokens': self.config.max_tokens,
            'timeout': self.config.timeout,
            'max_retries': self.config.max_retries,
        }
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def get_available_models(self) -> List[Dict]:
        return [
            {
                "provider": "deepseek",
                "models": [
                    {"id": "deepseek-v4-flash", "name": "DeepSeek V4 Flash", "desc": "最新快速模型，推荐", "max_tokens": 8192},
                    {"id": "deepseek-v4-pro", "name": "DeepSeek V4 Pro", "desc": "最强推理能力", "max_tokens": 8192},
                    {"id": "deepseek-chat", "name": "DeepSeek Chat", "desc": "通用对话，兼容旧版", "max_tokens": 8192},
                    {"id": "deepseek-reasoner", "name": "DeepSeek Reasoner", "desc": "深度推理，适合复杂大纲", "max_tokens": 8192},
                ]
            },
            {
                "provider": "openai",
                "models": [
                    {"id": "gpt-4o", "name": "GPT-4o", "desc": "最强综合能力", "max_tokens": 16384},
                    {"id": "gpt-4o-mini", "name": "GPT-4o Mini", "desc": "轻量快速", "max_tokens": 16384},
                ]
            },
        ]

    def _build_url(self) -> str:
        base = self.config.base_url.rstrip('/')
        return f"{base}/v1/chat/completions"

    def _build_headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.api_key}"
        }

    def _build_payload(self, messages: List[Dict], params: GenerationParams = None,
                       stream: bool = False) -> Dict:
        p = params or GenerationParams()
        payload = {
            "model": self.config.model_name,
            "messages": messages,
            "temperature": p.temperature if p.temperature is not None else self.config.temperature,
            "top_p": p.top_p if p.top_p is not None else self.config.top_p,
            "frequency_penalty": p.frequency_penalty if p.frequency_penalty is not None else self.config.frequency_penalty,
            "presence_penalty": p.presence_penalty if p.presence_penalty is not None else self.config.presence_penalty,
            "max_tokens": p.max_tokens if p.max_tokens is not None else self.config.max_tokens,
            "stream": stream,
        }
        if p.stop:
            payload["stop"] = p.stop
        return payload

    def reset_operation_count(self):
        self._operation_api_calls = 0

    def _check_operation_limit(self):
        if self._operation_api_calls >= self._max_api_calls_per_operation:
            raise RuntimeError(
                f"Operation API call limit reached ({self._max_api_calls_per_operation}). "
                "Too many retries detected. Please try again later."
            )

    def _retry_with_backoff(self, func, *args, **kwargs):
        if not self._circuit_breaker.is_allowed():
            raise RuntimeError("Circuit breaker is OPEN. Too many consecutive failures. Please wait and try again.")

        last_error = None
        for attempt in range(self.config.max_retries + 1):
            try:
                self._check_operation_limit()
                result = func(*args, **kwargs)
                self._operation_api_calls += 1
                self._total_api_calls += 1
                self._circuit_breaker.record_success()
                return result
            except Exception as e:
                last_error = e
                self._circuit_breaker.record_failure()
                if attempt < self.config.max_retries:
                    delay = min(
                        self.config.retry_delay_base * (2 ** attempt) + random.uniform(0, 1),
                        self.config.retry_delay_max
                    )
                    logger.warning(f"Attempt {attempt + 1} failed: {e}, retrying in {delay:.1f}s")
                    self._emit('on_error', e, attempt)
                    time.sleep(delay)
                else:
                    logger.error(f"All {self.config.max_retries + 1} attempts failed")
        raise last_error

    def _call_api(self, messages: List[Dict], params: GenerationParams = None) -> str:
        import urllib.request
        import urllib.error
        import socket

        payload = self._build_payload(messages, params, stream=False)
        data = json.dumps(payload, ensure_ascii=False).encode('utf-8')

        req = urllib.request.Request(
            self._build_url(),
            data=data,
            headers=self._build_headers(),
            method='POST'
        )

        try:
            with urllib.request.urlopen(req, timeout=self.config.timeout) as resp:
                result = json.loads(resp.read().decode('utf-8'))
                return result["choices"][0]["message"]["content"]
        except urllib.error.HTTPError as e:
            body = e.read().decode('utf-8', errors='replace')
            raise RuntimeError(f"HTTP {e.code}: {body[:500]}")
        except socket.timeout:
            raise RuntimeError(f"API call timed out after {self.config.timeout}s")
        except urllib.error.URLError as e:
            raise RuntimeError(f"Connection failed: {e.reason}")
        except Exception as e:
            err_str = str(e)
            if "10053" in err_str or "10054" in err_str or "10060" in err_str:
                raise RuntimeError(f"Connection aborted (WinError {err_str}), retrying...")
            raise RuntimeError(f"API call failed: {err_str}")

    def _call_api_stream(self, messages: List[Dict], params: GenerationParams = None) -> Generator[str, None, None]:
        import urllib.request
        import urllib.error

        payload = self._build_payload(messages, params, stream=True)
        data = json.dumps(payload, ensure_ascii=False).encode('utf-8')

        req = urllib.request.Request(
            self._build_url(),
            data=data,
            headers=self._build_headers(),
            method='POST'
        )

        try:
            with urllib.request.urlopen(req, timeout=self.config.timeout) as resp:
                buffer = b""
                while True:
                    chunk = resp.read(4096)
                    if not chunk:
                        break
                    buffer += chunk
                    while b'\n' in buffer:
                        line, buffer = buffer.split(b'\n', 1)
                        line = line.strip()
                        if not line or line == b'data: [DONE]':
                            continue
                        if line.startswith(b'data: '):
                            line = line[6:]
                        try:
                            event = json.loads(line.decode('utf-8'))
                            delta = event.get('choices', [{}])[0].get('delta', {})
                            content = delta.get('content', '')
                            if content:
                                yield content
                        except json.JSONDecodeError:
                            continue
        except urllib.error.HTTPError as e:
            body = e.read().decode('utf-8', errors='replace')
            raise RuntimeError(f"HTTP {e.code}: {body[:500]}")
        except Exception as e:
            raise RuntimeError(f"Stream API call failed: {str(e)}")

    def generate(self, prompt: str, system_prompt: str = None,
                 params: GenerationParams = None,
                 session_id: str = None) -> str:
        """
        同步生成文本

        参数:
            prompt: 用户提示词
            system_prompt: 系统提示词
            params: 生成参数
            session_id: 会话ID（用于多轮对话）
        """
        messages = self._build_messages(prompt, system_prompt, session_id)

        limiter_key = self.config.provider.value
        limiter = self._rate_limiters.get(limiter_key)
        if limiter and not limiter.wait_and_acquire(timeout=30.0):
            raise RuntimeError("Rate limit exceeded")

        self._emit('on_generate_start', prompt, params)

        def _do_call():
            return self._call_api(messages, params)

        result = self._retry_with_backoff(_do_call)

        if session_id:
            self._append_to_session(session_id, "assistant", result)

        self._emit('on_generate_end', result)
        return result

    def generate_stream(self, prompt: str, system_prompt: str = None,
                        params: GenerationParams = None,
                        session_id: str = None) -> Generator[str, None, None]:
        """
        流式生成文本

        参数:
            prompt: 用户提示词
            system_prompt: 系统提示词
            params: 生成参数
            session_id: 会话ID
        """
        messages = self._build_messages(prompt, system_prompt, session_id)

        limiter_key = self.config.provider.value
        limiter = self._rate_limiters.get(limiter_key)
        if limiter and not limiter.wait_and_acquire(timeout=30.0):
            raise RuntimeError("Rate limit exceeded")

        self._emit('on_generate_start', prompt, params)

        full_response = []

        def _do_stream():
            return self._call_api_stream(messages, params)

        try:
            for attempt in range(self.config.max_retries + 1):
                try:
                    for chunk in _do_stream():
                        full_response.append(chunk)
                        self._emit('on_generate_chunk', chunk)
                        yield chunk
                    break
                except Exception as e:
                    if attempt < self.config.max_retries:
                        delay = min(
                            self.config.retry_delay_base * (2 ** attempt) + random.uniform(0, 1),
                            self.config.retry_delay_max
                        )
                        logger.warning(f"Stream attempt {attempt + 1} failed: {e}, retrying in {delay:.1f}s")
                        time.sleep(delay)
                    else:
                        raise
        finally:
            full_text = ''.join(full_response)
            if session_id and full_text:
                self._append_to_session(session_id, "assistant", full_text)
            self._emit('on_generate_end', full_text)

    def _build_messages(self, prompt: str, system_prompt: str = None,
                        session_id: str = None) -> List[Dict]:
        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        if session_id and session_id in self._session_store:
            messages.extend(self._session_store[session_id])

        messages.append({"role": "user", "content": prompt})

        if session_id:
            if session_id not in self._session_store:
                self._session_store[session_id] = []
            self._session_store[session_id].append({"role": "user", "content": prompt})

        return messages

    def _append_to_session(self, session_id: str, role: str, content: str):
        if session_id not in self._session_store:
            self._session_store[session_id] = []
        self._session_store[session_id].append({"role": role, "content": content})

        max_history = 20
        if len(self._session_store[session_id]) > max_history:
            self._session_store[session_id] = self._session_store[session_id][-max_history:]

    def clear_session(self, session_id: str):
        if session_id in self._session_store:
            del self._session_store[session_id]

    def get_session(self, session_id: str) -> List[Dict]:
        return self._session_store.get(session_id, [])

    def generate_json(self, prompt: str, system_prompt: str = None,
                      params: GenerationParams = None,
                      session_id: str = None,
                      fallback: Any = None) -> Any:
        """
        生成并解析JSON响应

        内置三层JSON解析回退：
        1. 标准JSON解析
        2. 括号修复 + 截断
        3. 正则提取关键字段
        """
        import re

        json_system = (system_prompt or '') + '\nYou MUST return ONLY valid JSON. No markdown, no explanation.'
        result_text = self.generate(prompt, json_system, params, session_id)

        json_str = result_text
        if "```json" in json_str:
            json_str = json_str.split("```json")[1].split("```")[0]
        elif "```" in json_str:
            json_str = json_str.split("```")[1].split("```")[0]
        json_str = json_str.strip()

        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e1:
            logger.warning(f"JSON parse error: {e1}, attempting recovery...")
            json_str = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', json_str)
            json_str = json_str.replace('\t', ' ').replace('\r', '')

            last_brace = json_str.rfind('}')
            last_bracket = json_str.rfind(']')
            cut_point = max(last_brace, last_bracket)
            if cut_point > 0:
                json_str = json_str[:cut_point + 1]
                bracket_count = json_str.count('{') - json_str.count('}')
                json_str += '}' * max(0, bracket_count)

            try:
                return json.loads(json_str)
            except json.JSONDecodeError as e2:
                logger.warning(f"Recovery failed: {e2}, trying regex extraction...")
                if fallback is not None:
                    return fallback

                result = {}
                str_fields = re.findall(r'"(\w+)"\s*:\s*"([^"]*)"', json_str)
                for key, value in str_fields:
                    result[key] = value

                int_fields = re.findall(r'"(\w+)"\s*:\s*(\d+)', json_str)
                for key, value in int_fields:
                    if key not in result:
                        result[key] = int(value)

                list_fields = re.findall(r'"(\w+)"\s*:\s*\[(.*?)\]', json_str, re.DOTALL)
                for key, content in list_fields:
                    if key not in result:
                        items = re.findall(r'"([^"]*)"', content)
                        result[key] = items

                return result if result else fallback


llm = LLMInterface()