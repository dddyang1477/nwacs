"""
快速测试DeepSeek学习引擎 - 仅学习新增的3个知识库
"""
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from deepseek_learning_engine import DeepSeekLearningEngine

# 使用已知的API key
API_KEY = "sk-f3246fbd1eef446e9a11d78efefd9bba"

print("🚀 开始运行DeepSeek学习引擎（测试版本）...")
print("📚 仅学习新增的3个写作相关知识库")
print("-" * 50)

try:
    # 初始化学习引擎，暂时禁用飞书和微信推送
    engine = DeepSeekLearningEngine(
        api_key=API_KEY,
        enable_feishu=False,
        enable_wechat=False
    )
    
    # 仅测试学习新增的3个知识库
    engine.knowledge_bases = [
        "写作手法与修辞知识库.txt",
        "小说创作灵感库.txt", 
        "写作经典技巧精华库.txt"
    ]
    
    print(f"📖 待学习知识库:")
    for kb in engine.knowledge_bases:
        print(f"   - {kb}")
    print("-" * 50)
    
    # 学习这些知识库
    results = []
    for kb in engine.knowledge_bases:
        print(f"\n📚 开始学习: {kb}")
        result = engine.learn_knowledge_base(kb)
        results.append(result)
        if result['status'] == 'success':
            print(f"✅ 完成学习: {kb}")
        else:
            print(f"⚠️ 跳过: {kb} - {result.get('reason', '未知原因')}")
    
    print("\n" + "-" * 50)
    print("🎉 测试学习完成！")
    
    # 打印学习结果摘要
    print("\n📝 学习结果摘要:")
    for kb, result in zip(engine.knowledge_bases, results):
        if result['status'] == 'success':
            print(f"✅ {kb}")
        else:
            print(f"❌ {kb}: {result.get('reason', '失败')}")
    
except Exception as e:
    print(f"\n❌ 发生错误: {e}")
    import traceback
    traceback.print_exc()
