#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS V8.0 主入口
整合所有核心组件，启动系统
"""

import sys
import os
import json
import time
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

class NWACS_V8:
    """NWACS V8.0主类"""
    
    def __init__(self):
        self.config = None
        self.engine = None
        self.skill_manager = None
        self.knowledge_manager = None
        self.api_gateway = None
        self.is_running = False
    
    def initialize(self):
        """初始化所有组件"""
        print("="*60)
        print("🚀 NWACS V8.0 初始化")
        print("="*60)
        
        # 1. 初始化配置管理
        print("\n[1/5] 初始化配置管理...")
        from core.v8.config.config_manager import ConfigBuilder
        self.config = ConfigBuilder.create_default_config()
        print("   ✅ 配置管理初始化完成")
        
        # 2. 初始化创作引擎
        print("\n[2/5] 初始化创作引擎...")
        from core.v8.engine.creative_engine import SmartCreativeEngine
        self.engine = SmartCreativeEngine()
        print("   ✅ 创作引擎初始化完成")
        
        # 3. 初始化Skill管理器
        print("\n[3/5] 初始化Skill管理器...")
        from core.v8.skill_manager.skill_manager import SkillManagerBuilder
        self.skill_manager = SkillManagerBuilder.create_default_manager()
        self.skill_manager.set_engine(self.engine)
        print("   ✅ Skill管理器初始化完成")
        
        # 4. 初始化知识库管理
        print("\n[4/5] 初始化知识库管理...")
        from core.v8.knowledge_base.knowledge_manager import KnowledgeBaseManager
        self.knowledge_manager = KnowledgeBaseManager()
        self.knowledge_manager.load_knowledge_base("学习知识库", "skills/level2/learnings")
        print("   ✅ 知识库管理初始化完成")
        
        # 5. 初始化API网关
        print("\n[5/5] 初始化API网关...")
        from core.v8.api_gateway.api_gateway import APIGateway
        self.api_gateway = APIGateway(
            host=self.config.get("server.host", "127.0.0.1"),
            port=self.config.get("server.port", 8000)
        )
        self.api_gateway.set_engine(self.engine)
        self.api_gateway.set_skill_manager(self.skill_manager)
        self.api_gateway.set_knowledge_manager(self.knowledge_manager)
        print("   ✅ API网关初始化完成")
        
        print("\n" + "="*60)
        print("🎉 NWACS V8.0 初始化完成！")
        print("="*60)
    
    def start(self):
        """启动系统"""
        if not self.is_running:
            self.is_running = True
            print(f"\n启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("系统已准备就绪，可以开始创作！")
    
    def stop(self):
        """停止系统"""
        if self.is_running:
            self.is_running = False
            if self.api_gateway:
                self.api_gateway.stop()
            print(f"\n停止时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("系统已停止")
    
    def run_command(self, command: str):
        """执行命令"""
        commands = {
            'help': self._show_help,
            'start': self.start,
            'stop': self.stop,
            'generate': self._generate_content,
            'outline': self._generate_outline,
            'character': self._generate_character,
            'scene': self._generate_scene,
            'dialogue': self._generate_dialogue,
            'skills': self._list_skills,
            'execute': self._execute_skill,
            'knowledge': self._search_knowledge,
            'stats': self._show_stats
        }
        
        cmd_parts = command.strip().lower().split(' ', 1)
        cmd = cmd_parts[0]
        args = cmd_parts[1] if len(cmd_parts) > 1 else ""
        
        if cmd in commands:
            return commands[cmd](args)
        else:
            return f"未知命令: {command}\n输入 'help' 查看可用命令"
    
    def _show_help(self, args):
        """显示帮助"""
        help_text = """
📋 NWACS V8.0 命令列表

基础命令:
  help          - 显示此帮助信息
  start         - 启动系统
  stop          - 停止系统
  stats         - 显示系统状态

创作命令:
  generate <提示词>      - 生成内容
  outline <主题>         - 生成小说大纲
  character <类型>       - 生成角色设定
  scene <地点> <时间>    - 生成场景描写
  dialogue <人物> <话题> - 生成对话

Skill命令:
  skills       - 列出所有Skill
  execute <skill_id> - 执行指定Skill

知识库命令:
  knowledge <关键词> - 搜索知识库

示例:
  generate 写一段玄幻小说的战斗场景
  outline 废柴少年逆袭
  character protagonist
  scene 青云宗 清晨
  dialogue 林动 林琅天 比武挑战
  knowledge 写作技巧
"""
        return help_text
    
    def _generate_content(self, args):
        """生成内容"""
        if not args:
            return "请提供生成内容的提示词"
        
        try:
            result = self.engine.generate(args)
            return f"✅ 生成完成:\n\n{result}"
        except Exception as e:
            return f"❌ 生成失败: {e}"
    
    def _generate_outline(self, args):
        """生成大纲"""
        if not args:
            return "请提供小说主题"
        
        try:
            result = self.engine.generate_outline(args, length=10)
            return f"✅ 大纲生成完成:\n\n{result}"
        except Exception as e:
            return f"❌ 大纲生成失败: {e}"
    
    def _generate_character(self, args):
        """生成角色"""
        char_type = args if args else "protagonist"
        
        try:
            result = self.engine.generate_character(char_type)
            return f"✅ 角色生成完成:\n\n{result}"
        except Exception as e:
            return f"❌ 角色生成失败: {e}"
    
    def _generate_scene(self, args):
        """生成场景"""
        parts = args.split(' ')
        location = parts[0] if parts else "未知地点"
        time = parts[1] if len(parts) > 1 else "某个时刻"
        
        try:
            result = self.engine.generate_scene(location, time, [], "")
            return f"✅ 场景生成完成:\n\n{result}"
        except Exception as e:
            return f"❌ 场景生成失败: {e}"
    
    def _generate_dialogue(self, args):
        """生成对话"""
        parts = args.split(' ', 2)
        if len(parts) >= 2:
            characters = parts[:2]
            topic = parts[2] if len(parts) > 2 else "日常对话"
        else:
            characters = ["人物A", "人物B"]
            topic = args if args else "日常对话"
        
        try:
            result = self.engine.generate_dialogue(characters, topic)
            return f"✅ 对话生成完成:\n\n{result}"
        except Exception as e:
            return f"❌ 对话生成失败: {e}"
    
    def _list_skills(self, args):
        """列出所有Skill"""
        skills = self.skill_manager.get_skill_list()
        result = "📚 可用Skill列表:\n\n"
        for i, skill in enumerate(skills, 1):
            result += f"{i}. {skill['name']} ({skill['skill_id']})\n"
            result += f"   类型: {skill['skill_type']}\n"
            result += f"   描述: {skill['description']}\n\n"
        return result
    
    def _execute_skill(self, args):
        """执行Skill"""
        if not args:
            return "请指定要执行的Skill ID"
        
        parts = args.split(' ', 1)
        skill_id = parts[0]
        params = {}
        
        if len(parts) > 1:
            try:
                params = json.loads(parts[1])
            except:
                pass
        
        try:
            result = self.skill_manager.execute_skill(skill_id, **params)
            return f"✅ Skill执行完成:\n\n{result}"
        except Exception as e:
            return f"❌ Skill执行失败: {e}"
    
    def _search_knowledge(self, args):
        """搜索知识库"""
        if not args:
            return "请提供搜索关键词"
        
        try:
            results = self.knowledge_manager.search(args)
            if results:
                result = f"🔍 搜索 '{args}' 找到 {len(results)} 条结果:\n\n"
                for item_id, score in results[:5]:
                    item = self.knowledge_manager.get_item(item_id)
                    if item:
                        result += f"- {item.title} (相关性: {score})\n"
                return result
            else:
                return f"🔍 搜索 '{args}' 未找到结果"
        except Exception as e:
            return f"❌ 搜索失败: {e}"
    
    def _show_stats(self, args):
        """显示系统状态"""
        stats = {
            "version": "8.0.0",
            "status": "running" if self.is_running else "stopped",
            "engine": "SmartCreativeEngine",
            "skills_count": len(self.skill_manager.get_skill_list()),
            "knowledge_bases": self.knowledge_manager.get_all_kb_names(),
            "api_port": self.config.get("server.port", 8000)
        }
        
        result = "📊 NWACS V8.0 系统状态:\n\n"
        for key, value in stats.items():
            result += f"   {key}: {value}\n"
        
        return result

def main():
    """主函数"""
    print("="*60)
    print("🎯 NWACS V8.0 - 小说创作AI协同系统")
    print("="*60)
    
    try:
        # 初始化系统
        nwacs = NWACS_V8()
        nwacs.initialize()
        
        # 启动系统
        nwacs.start()
        
        # 命令行交互
        print("\n📝 输入命令开始创作 (输入 'help' 查看命令列表)")
        print("="*60)
        
        while True:
            try:
                command = input("\n> ").strip()
                if not command:
                    continue
                
                if command.lower() in ['exit', 'quit', 'bye']:
                    nwacs.stop()
                    print("👋 再见！")
                    break
                
                result = nwacs.run_command(command)
                print(result)
                
            except KeyboardInterrupt:
                nwacs.stop()
                print("\n👋 再见！")
                break
            except Exception as e:
                print(f"❌ 执行命令时出错: {e}")
    
    except Exception as e:
        print(f"❌ 系统初始化失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
