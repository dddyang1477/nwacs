#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 系统优化器 v1.0
检查智能学习能力、优化配置、提升联通性
"""

import os
import sys
import json
import requests
import time
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

VERSION = "1.0"
CONFIG_FILE = "config.json"
CORE_DIR = "core/"
LEARNING_DIR = "learning/"
SKILLS_DIR = "skills/"

class SystemOptimizer:
    """系统优化器"""
    
    def __init__(self):
        self.config = self._load_config()
        self.optimizations = []
        self.issues = []
        self.verifications = []
    
    def _load_config(self):
        """加载配置文件"""
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _save_config(self):
        """保存配置文件"""
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def test_api_connection(self):
        """测试API连接"""
        if not self.config.get('api_key') or not self.config.get('base_url'):
            self.issues.append("❌ API配置不完整")
            return False
        
        try:
            headers = {
                'Authorization': f"Bearer {self.config['api_key']}",
                'Content-Type': 'application/json'
            }
            data = {
                'model': self.config.get('model', 'deepseek-v4-pro'),
                'messages': [{'role': 'user', 'content': 'test'}],
                'max_tokens': 5
            }
            response = requests.post(
                f"{self.config['base_url']}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            if response.status_code == 200:
                self.verifications.append("✅ API连接正常")
                return True
            else:
                self.issues.append(f"❌ API连接失败: {response.status_code}")
                return False
        except Exception as e:
            self.issues.append(f"❌ API连接异常: {str(e)}")
            return False
    
    def check_core_modules(self):
        """检查核心模块"""
        core_modules = [
            'novel_project_manager.py',
            'novel_quality_checker.py', 
            'nwacs_single.py',
            'auto_idle_learning.py',
            'comprehensive_learning.py',
            'book_learning_system.py',
            'novel_download_and_analyze.py'
        ]
        
        for module in core_modules:
            path = os.path.join(CORE_DIR, module)
            if os.path.exists(path):
                self.verifications.append(f"✅ 核心模块: {module}")
            else:
                self.issues.append(f"❌ 缺失核心模块: {module}")
    
    def check_learning_system(self):
        """检查学习系统"""
        # 检查学习目录
        if os.path.exists(LEARNING_DIR):
            learning_files = os.listdir(LEARNING_DIR)
            if learning_files:
                self.verifications.append(f"✅ 学习目录存在，共 {len(learning_files)} 个文件")
            else:
                self.issues.append("⚠️ 学习目录为空")
        else:
            self.issues.append("❌ 学习目录不存在")
        
        # 检查技能目录
        if os.path.exists(SKILLS_DIR):
            self.verifications.append("✅ 技能目录存在")
        else:
            self.issues.append("❌ 技能目录不存在")
    
    def optimize_config(self):
        """优化配置设置"""
        # 优化连接超时设置
        if 'timeout' not in self.config:
            self.config['timeout'] = 60
            self.optimizations.append("添加连接超时设置: 60秒")
        
        # 添加重试机制
        if 'max_retries' not in self.config:
            self.config['max_retries'] = 3
            self.optimizations.append("添加重试机制: 3次")
        
        # 添加API版本配置
        if 'api_version' not in self.config:
            self.config['api_version'] = 'v1'
            self.optimizations.append("添加API版本配置")
        
        # 优化学习设置
        if 'learning' not in self.config:
            self.config['learning'] = {
                'enabled': True,
                'auto_learn_interval': 3600,
                'max_learning_hours': 2
            }
            self.optimizations.append("优化学习设置")
        
        # 添加日志配置
        if 'logging' not in self.config:
            self.config['logging'] = {
                'level': 'INFO',
                'file': 'logs/NWACS.log',
                'max_size': '10MB'
            }
            self.optimizations.append("添加日志配置")
        
        self._save_config()
    
    def verify_intelligent_features(self):
        """验证智能功能"""
        features = [
            ('auto_idle_learning', '自动空闲学习'),
            ('novel_quality_checker', '质量检查'),
            ('novel_download_and_analyze', '小说下载分析'),
            ('book_learning_system', '书籍学习系统'),
            ('comprehensive_learning', '综合学习')
        ]
        
        for module, desc in features:
            path = os.path.join(CORE_DIR, f"{module}.py")
            if os.path.exists(path):
                # 检查是否有智能相关代码
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    if 'learn' in content.lower() or 'intelligent' in content.lower():
                        self.verifications.append(f"✅ 智能功能: {desc}")
                    else:
                        self.issues.append(f"⚠️ 智能功能待增强: {desc}")
            else:
                self.issues.append(f"❌ 智能功能缺失: {desc}")
    
    def run_full_optimization(self):
        """运行完整优化流程"""
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║         NWACS 系统优化器 v{VERSION}                              ║
║                                                              ║
║         🚀 开始系统检查与优化...                              ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
        """)
        
        print("\n🔍 阶段一：API连接测试")
        self.test_api_connection()
        
        print("\n🔍 阶段二：核心模块检查")
        self.check_core_modules()
        
        print("\n🔍 阶段三：学习系统检查")
        self.check_learning_system()
        
        print("\n🔍 阶段四：智能功能验证")
        self.verify_intelligent_features()
        
        print("\n⚡ 阶段五：配置优化")
        self.optimize_config()
        
        self._generate_report()
    
    def _generate_report(self):
        """生成优化报告"""
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║         📊 NWACS 系统优化报告                                  ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

【系统配置】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

 模型: {self.config.get('model', '未配置')}
 API版本: {self.config.get('api_version', 'v1')}
 连接超时: {self.config.get('timeout', 60)}秒
 最大重试: {self.config.get('max_retries', 3)}次
 学习功能: {'✅ 已启用' if self.config.get('learning_enabled') else '❌ 未启用'}

【优化项】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")
        
        if self.optimizations:
            for opt in self.optimizations:
                print(f"  ✨ {opt}")
        else:
            print("  暂无优化项")
        
        print(f"""
【验证结果】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")
        
        for v in self.verifications:
            print(f"  {v}")
        
        print(f"""
【待处理问题】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")
        
        if self.issues:
            for issue in self.issues:
                print(f"  {issue}")
        else:
            print("  ✅ 无问题")
        
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║         ✅ 系统优化完成！                                      ║
║                                                              ║
║         优化项: {len(self.optimizations)} 项                   ║
║         验证通过: {len(self.verifications)} 项                 ║
║         待处理: {len(self.issues)} 项                         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
        """)

def main():
    optimizer = SystemOptimizer()
    optimizer.run_full_optimization()

if __name__ == "__main__":
    main()