#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS V8.0 API网关
核心功能：
1. REST API服务
2. 请求路由与分发
3. 身份验证
4. 响应格式化
"""

import sys
import json
import asyncio
from datetime import datetime
from typing import Dict, Any, Optional
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

try:
    sys.stdout.reconfigure(encoding='utf-8')
except (AttributeError, OSError):
    pass

class APIResponse:
    """API响应"""
    
    def __init__(self, data: Any = None, error: str = None, status_code: int = 200):
        self.data = data
        self.error = error
        self.status_code = status_code
    
    def to_dict(self):
        result = {
            "success": self.error is None,
            "timestamp": datetime.now().isoformat()
        }
        
        if self.data is not None:
            result["data"] = self.data
        
        if self.error is not None:
            result["error"] = self.error
        
        return result

class APIRequest:
    """API请求"""
    
    def __init__(self, path: str, method: str, params: Dict[str, Any], body: Dict[str, Any] = None):
        self.path = path
        self.method = method
        self.params = params
        self.body = body or {}

class APIRouter:
    """API路由器"""
    
    def __init__(self):
        self.routes = {
            'GET': {},
            'POST': {},
            'PUT': {},
            'DELETE': {}
        }
    
    def add_route(self, method: str, path: str, handler):
        """添加路由"""
        self.routes[method.upper()][path] = handler
    
    def get_handler(self, method: str, path: str):
        """获取处理器"""
        return self.routes.get(method.upper(), {}).get(path)

class APIHandler(BaseHTTPRequestHandler):
    """API请求处理器"""
    
    router = None
    engine = None
    skill_manager = None
    knowledge_manager = None
    
    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)
    
    def send_json_response(self, response: APIResponse):
        """发送JSON响应"""
        self.send_response(response.status_code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        response_body = json.dumps(response.to_dict(), ensure_ascii=False)
        self.wfile.write(response_body.encode('utf-8'))
    
    def do_GET(self):
        """处理GET请求"""
        self._handle_request('GET')
    
    def do_POST(self):
        """处理POST请求"""
        self._handle_request('POST')
    
    def do_PUT(self):
        """处理PUT请求"""
        self._handle_request('PUT')
    
    def do_DELETE(self):
        """处理DELETE请求"""
        self._handle_request('DELETE')
    
    def _handle_request(self, method: str):
        """处理请求"""
        try:
            parsed = urlparse(self.path)
            path = parsed.path
            params = parse_qs(parsed.query)
            
            # 解析请求体
            body = {}
            if self.headers.get('Content-Type') == 'application/json':
                content_length = int(self.headers.get('Content-Length', 0))
                if content_length > 0:
                    body = json.loads(self.rfile.read(content_length).decode('utf-8'))
            
            request = APIRequest(path, method, params, body)
            
            # 查找处理器
            handler = self.router.get_handler(method, path)
            
            if handler:
                try:
                    response = handler(request)
                except Exception as e:
                    response = APIResponse(error=str(e), status_code=500)
            else:
                response = APIResponse(error=f"Route not found: {method} {path}", status_code=404)
            
            self.send_json_response(response)
        
        except Exception as e:
            self.send_json_response(APIResponse(error=f"Request error: {str(e)}", status_code=500))

class APIGateway:
    """API网关"""
    
    def __init__(self, host: str = '127.0.0.1', port: int = 8000):
        self.host = host
        self.port = port
        self.router = APIRouter()
        self.engine = None
        self.skill_manager = None
        self.knowledge_manager = None
        self.server = None
    
    def set_engine(self, engine):
        """设置创作引擎"""
        self.engine = engine
    
    def set_skill_manager(self, skill_manager):
        """设置Skill管理器"""
        self.skill_manager = skill_manager
    
    def set_knowledge_manager(self, knowledge_manager):
        """设置知识库管理器"""
        self.knowledge_manager = knowledge_manager
    
    def _register_routes(self):
        """注册路由"""
        # 健康检查
        self.router.add_route('GET', '/health', self._handle_health)
        
        # 创作引擎API
        self.router.add_route('POST', '/api/generate', self._handle_generate)
        self.router.add_route('POST', '/api/generate/outline', self._handle_generate_outline)
        self.router.add_route('POST', '/api/generate/character', self._handle_generate_character)
        self.router.add_route('POST', '/api/generate/scene', self._handle_generate_scene)
        self.router.add_route('POST', '/api/generate/dialogue', self._handle_generate_dialogue)
        self.router.add_route('POST', '/api/rewrite', self._handle_rewrite)
        self.router.add_route('POST', '/api/continue', self._handle_continue)
        
        # Skill管理器API
        self.router.add_route('GET', '/api/skills', self._handle_get_skills)
        self.router.add_route('GET', '/api/skills/{skill_id}', self._handle_get_skill)
        self.router.add_route('POST', '/api/skills/{skill_id}/execute', self._handle_execute_skill)
        
        # 知识库API
        self.router.add_route('GET', '/api/knowledge/search', self._handle_knowledge_search)
        self.router.add_route('GET', '/api/knowledge/{item_id}', self._handle_get_knowledge_item)
        self.router.add_route('GET', '/api/knowledge/stats', self._handle_knowledge_stats)
    
    def _handle_health(self, request: APIRequest) -> APIResponse:
        """健康检查"""
        return APIResponse(data={"status": "healthy", "version": "8.0.0"})
    
    def _handle_generate(self, request: APIRequest) -> APIResponse:
        """生成内容"""
        if not self.engine:
            return APIResponse(error="Engine not initialized", status_code=500)
        
        prompt = request.body.get('prompt', '')
        style = request.body.get('style', 'default')
        temperature = request.body.get('temperature', 0.7)
        
        if not prompt:
            return APIResponse(error="Prompt is required", status_code=400)
        
        try:
            result = self.engine.generate_with_style(prompt, style, temperature=temperature)
            return APIResponse(data={"result": result})
        except Exception as e:
            return APIResponse(error=str(e), status_code=500)
    
    def _handle_generate_outline(self, request: APIRequest) -> APIResponse:
        """生成大纲"""
        if not self.engine:
            return APIResponse(error="Engine not initialized", status_code=500)
        
        theme = request.body.get('theme', '')
        length = request.body.get('length', 10)
        
        if not theme:
            return APIResponse(error="Theme is required", status_code=400)
        
        try:
            result = self.engine.generate_outline(theme, length)
            return APIResponse(data={"result": result})
        except Exception as e:
            return APIResponse(error=str(e), status_code=500)
    
    def _handle_generate_character(self, request: APIRequest) -> APIResponse:
        """生成角色"""
        if not self.engine:
            return APIResponse(error="Engine not initialized", status_code=500)
        
        character_type = request.body.get('character_type', 'protagonist')
        
        try:
            result = self.engine.generate_character(character_type)
            return APIResponse(data={"result": result})
        except Exception as e:
            return APIResponse(error=str(e), status_code=500)
    
    def _handle_generate_scene(self, request: APIRequest) -> APIResponse:
        """生成场景"""
        if not self.engine:
            return APIResponse(error="Engine not initialized", status_code=500)
        
        location = request.body.get('location', '')
        time = request.body.get('time', '')
        characters = request.body.get('characters', [])
        purpose = request.body.get('purpose', '')
        
        if not location or not time:
            return APIResponse(error="Location and time are required", status_code=400)
        
        try:
            result = self.engine.generate_scene(location, time, characters, purpose)
            return APIResponse(data={"result": result})
        except Exception as e:
            return APIResponse(error=str(e), status_code=500)
    
    def _handle_generate_dialogue(self, request: APIRequest) -> APIResponse:
        """生成对话"""
        if not self.engine:
            return APIResponse(error="Engine not initialized", status_code=500)
        
        characters = request.body.get('characters', [])
        topic = request.body.get('topic', '')
        emotion = request.body.get('emotion', 'neutral')
        
        if not characters or not topic:
            return APIResponse(error="Characters and topic are required", status_code=400)
        
        try:
            result = self.engine.generate_dialogue(characters, topic, emotion)
            return APIResponse(data={"result": result})
        except Exception as e:
            return APIResponse(error=str(e), status_code=500)
    
    def _handle_rewrite(self, request: APIRequest) -> APIResponse:
        """重写文本"""
        if not self.engine:
            return APIResponse(error="Engine not initialized", status_code=500)
        
        text = request.body.get('text', '')
        style = request.body.get('style', 'polish')
        
        if not text:
            return APIResponse(error="Text is required", status_code=400)
        
        try:
            result = self.engine.rewrite(text, style)
            return APIResponse(data={"result": result})
        except Exception as e:
            return APIResponse(error=str(e), status_code=500)
    
    def _handle_continue(self, request: APIRequest) -> APIResponse:
        """续写文本"""
        if not self.engine:
            return APIResponse(error="Engine not initialized", status_code=500)
        
        text = request.body.get('text', '')
        length = request.body.get('length', 500)
        
        if not text:
            return APIResponse(error="Text is required", status_code=400)
        
        try:
            result = self.engine.continue_writing(text, length)
            return APIResponse(data={"result": result})
        except Exception as e:
            return APIResponse(error=str(e), status_code=500)
    
    def _handle_get_skills(self, request: APIRequest) -> APIResponse:
        """获取Skill列表"""
        if not self.skill_manager:
            return APIResponse(error="Skill manager not initialized", status_code=500)
        
        try:
            skills = self.skill_manager.get_skill_list()
            return APIResponse(data={"skills": skills})
        except Exception as e:
            return APIResponse(error=str(e), status_code=500)
    
    def _handle_get_skill(self, request: APIRequest) -> APIResponse:
        """获取单个Skill"""
        if not self.skill_manager:
            return APIResponse(error="Skill manager not initialized", status_code=500)
        
        skill_id = request.path.split('/')[-1]
        
        try:
            skill = self.skill_manager.get_skill(skill_id)
            if skill:
                return APIResponse(data={"skill": skill.metadata.to_dict()})
            else:
                return APIResponse(error="Skill not found", status_code=404)
        except Exception as e:
            return APIResponse(error=str(e), status_code=500)
    
    def _handle_execute_skill(self, request: APIRequest) -> APIResponse:
        """执行Skill"""
        if not self.skill_manager:
            return APIResponse(error="Skill manager not initialized", status_code=500)
        
        skill_id = request.path.split('/')[3]
        
        try:
            result = self.skill_manager.execute_skill(skill_id, **request.body)
            return APIResponse(data={"result": result})
        except Exception as e:
            return APIResponse(error=str(e), status_code=500)
    
    def _handle_knowledge_search(self, request: APIRequest) -> APIResponse:
        """搜索知识"""
        if not self.knowledge_manager:
            return APIResponse(error="Knowledge manager not initialized", status_code=500)
        
        query = request.params.get('q', [''])[0]
        
        if not query:
            return APIResponse(error="Query is required", status_code=400)
        
        try:
            results = self.knowledge_manager.search(query)
            return APIResponse(data={"results": results})
        except Exception as e:
            return APIResponse(error=str(e), status_code=500)
    
    def _handle_get_knowledge_item(self, request: APIRequest) -> APIResponse:
        """获取知识条目"""
        if not self.knowledge_manager:
            return APIResponse(error="Knowledge manager not initialized", status_code=500)
        
        item_id = request.path.split('/')[-1]
        
        try:
            item = self.knowledge_manager.get_item(item_id)
            if item:
                return APIResponse(data={"item": item.to_dict()})
            else:
                return APIResponse(error="Item not found", status_code=404)
        except Exception as e:
            return APIResponse(error=str(e), status_code=500)
    
    def _handle_knowledge_stats(self, request: APIRequest) -> APIResponse:
        """获取知识库统计"""
        if not self.knowledge_manager:
            return APIResponse(error="Knowledge manager not initialized", status_code=500)
        
        try:
            stats = self.knowledge_manager.get_statistics()
            return APIResponse(data={"stats": stats})
        except Exception as e:
            return APIResponse(error=str(e), status_code=500)
    
    def start(self):
        """启动API服务器"""
        self._register_routes()
        
        # 设置处理器的静态属性
        APIHandler.router = self.router
        APIHandler.engine = self.engine
        APIHandler.skill_manager = self.skill_manager
        APIHandler.knowledge_manager = self.knowledge_manager
        
        self.server = HTTPServer((self.host, self.port), APIHandler)
        print(f"🚀 NWACS V8.0 API Gateway starting on {self.host}:{self.port}")
        
        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 API Gateway stopped")
            self.server.server_close()
    
    def stop(self):
        """停止API服务器"""
        if self.server:
            self.server.server_close()

if __name__ == "__main__":
    print("="*60)
    print("🚀 NWACS V8.0 API Gateway")
    print("="*60)
    
    gateway = APIGateway(host='127.0.0.1', port=8000)
    gateway.start()
