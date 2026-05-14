
    def do_GET(self):
        """处理GET请求 - 优化版（使用调度表）"""
        path = urlparse(self.path).path
        
        # API调度表
        get_handlers = {
            '/api/health': self._handle_get_health,
            '/api/models': self._handle_get_models,
            '/api/config': self._handle_get_config,
            '/api/options': self._handle_get_options,
            '/api/quality/trend': self._handle_get_quality_trend,
            '/api/memory/stats': self._handle_get_memory_stats,
            '/api/planning/timeline': self._handle_get_planning_timeline,
            '/api/retention/report': self._handle_get_retention_report,
            '/api/story/snapshot': self._handle_get_story_snapshot,
            '/api/story/lock': self._handle_get_story_lock,
            '/api/story/control': self._handle_get_story_control,
            '/api/quality/arcs': self._handle_get_quality_arcs,
            '/api/rag/stats': self._handle_get_rag_stats,
            '/api/rag/characters': self._handle_get_rag_characters,
            '/api/rag/timeline': self._handle_get_rag_timeline,
            '/api/style/list': self._handle_get_style_list,
            '/api/strand/report': self._handle_get_strand_report,
            '/api/truth/new/status': self._handle_get_truth_new_status,
            '/api/pipeline/new/status': self._handle_get_pipeline_new_status,
            '/': self._handle_get_index,
            '/index.html': self._handle_get_index,
        }
        
        # 查找处理器
        handler = get_handlers.get(path)
        if handler:
            try:
                handler()
            except Exception as e:
                self._handle_error(e)
        else:
            self._send_json({"error": "Not found"}, 404)
    
    # GET请求处理器
    def _handle_get_health(self):
        """健康检查"""
        self._send_json({"status": "ok"})
    
    def _handle_get_models(self):
        """获取可用模型"""
        self._send_json({
            "models": llm.get_available_models(),
            "current": {
                "provider": llm.config.provider.value,
                "model_name": llm.config.model_name,
                "temperature": llm.config.temperature,
                "top_p": llm.config.top_p,
                "max_tokens": llm.config.max_tokens,
            }
        })
    
    def _handle_get_config(self):
        """获取配置"""
        self._send_json({
            "provider": llm.config.provider.value,
            "model_name": llm.config.model_name,
            "base_url": llm.config.base_url,
            "temperature": llm.config.temperature,
            "top_p": llm.config.top_p,
            "frequency_penalty": llm.config.frequency_penalty,
            "presence_penalty": llm.config.presence_penalty,
            "max_tokens": llm.config.max_tokens,
            "timeout": llm.config.timeout,
            "max_retries": llm.config.max_retries,
        })
    
    def _handle_get_options(self):
        """获取选项（题材、流派、风格等）"""
        self._send_json({
            "genres": self._get_genres_options(),
            "schools": self._get_schools_options(),
            "styles": self._get_styles_options(),
            "tones": self._get_tones_options(),
            "lengths": self._get_lengths_options()
        })
    
    def _get_genres_options(self):
        """获取题材选项"""
        return {
            "玄幻": {"icon": "🐉", "desc": "东方奇幻世界", "color": "#7c3aed"},
            "都市": {"icon": "🏙️", "desc": "现代都市背景", "color": "#2563eb"},
            "仙侠": {"icon": "⚔️", "desc": "修仙问道", "color": "#059669"},
            "科幻": {"icon": "🚀", "desc": "未来科技", "color": "#0891b2"},
            "悬疑": {"icon": "🔍", "desc": "推理探案", "color": "#d97706"},
            "言情": {"icon": "💕", "desc": "情感纠葛", "color": "#db2777"},
            "历史": {"icon": "📜", "desc": "架空历史", "color": "#b45309"},
            "游戏": {"icon": "🎮", "desc": "虚拟现实", "color": "#4f46e5"},
            "恐怖": {"icon": "👻", "desc": "灵异惊悚", "color": "#6b21a8"},
            "武侠": {"icon": "🥋", "desc": "江湖恩怨", "color": "#b91c1c"},
        }
    
    def _handle_error(self, error):
        """统一错误处理"""
        log(f"Error in GET handler: {error}")
        traceback.print_exc()
        self._send_json({"success": False, "error": str(error)[:200]}, 500)
