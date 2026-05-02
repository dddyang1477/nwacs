"""
快速运行DeepSeek学习引擎
"""
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from deepseek_learning_engine import DeepSeekLearningEngine

# 使用已知的API key
API_KEY = "sk-f3246fbd1eef446e9a11d78efefd9bba"

print("🚀 开始运行DeepSeek学习引擎...")
print(f"📚 共 {len(DeepSeekLearningEngine(API_KEY, enable_feishu=False, enable_wechat=False).knowledge_bases)} 个知识库待学习")
print("-" * 50)

try:
    # 初始化学习引擎，暂时禁用飞书和微信推送
    engine = DeepSeekLearningEngine(
        api_key=API_KEY,
        enable_feishu=False,
        enable_wechat=False
    )
    
    # 运行学习
    report = engine.run(duration_hours=1)
    
    print("-" * 50)
    print("🎉 学习完成！")
    print(f"📝 报告已保存到: {engine.report_path}")
    
except Exception as e:
    print(f"❌ 发生错误: {e}")
    import traceback
    traceback.print_exc()
