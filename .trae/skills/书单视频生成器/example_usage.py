#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
书单视频生成器 - 使用示例
"""

from video_script_generator import VideoScriptGenerator, RecommendationCopywriter


def example_1_generate_video_script():
    """示例1：生成视频脚本"""
    print("=" * 50)
    print("示例1：生成视频脚本")
    print("=" * 50)
    
    # 准备书单数据
    books = [
        {
            "title": "活着",
            "author": "余华",
            "description": "讲述了一个普通人苦难而坚韧的一生，让我们读懂生命的意义",
            "quote": "人是为活着本身而活着的",
            "theme": "生命的意义",
            "characters": "福贵、家珍、凤霞",
            "plot": "从富家少爷到贫苦农民的坎坷一生"
        },
        {
            "title": "被讨厌的勇气",
            "author": "岸见一郎",
            "description": "阿德勒心理学的通俗解读，教你如何获得真正的自由",
            "quote": "决定我们自身的不是过去的经历",
            "theme": "自我成长",
            "problem": "人际关系的困扰",
            "method": "阿德勒心理学",
            "goal": "获得心灵自由"
        },
        {
            "title": "小王子",
            "author": "安托万·德·圣-埃克苏佩里",
            "description": "一个关于爱与责任的童话，献给所有曾经是孩子的大人",
            "quote": "真正重要的东西，用眼睛是看不见的",
            "theme": "爱与责任"
        }
    ]
    
    # 创建生成器
    generator = VideoScriptGenerator()
    
    # 生成1分钟文艺风格的脚本
    print("\n生成1分钟文艺风格的视频脚本...")
    script = generator.generate_script(
        books=books[:2],  # 用前两本书
        template="1min",
        style="literary"
    )
    
    # 打印脚本
    print_script(script)
    
    # 导出脚本
    generator.export_script(script, "output_script_1min.json")
    print("\n脚本已导出到: output_script_1min.json")


def example_2_generate_recommendation_copy():
    """示例2：生成推荐文案"""
    print("\n" + "=" * 50)
    print("示例2：生成推荐文案")
    print("=" * 50)
    
    books = [
        {
            "title": "活着",
            "author": "余华",
            "description": "讲述了一个普通人苦难而坚韧的一生",
            "quote": "人是为活着本身而活着的",
            "theme": "生命的意义",
            "characters": "福贵、家珍、凤霞",
            "plot": "从富家少爷到贫苦农民的坎坷一生"
        },
        {
            "title": "被讨厌的勇气",
            "author": "岸见一郎",
            "description": "阿德勒心理学的通俗解读",
            "quote": "决定我们自身的不是过去的经历",
            "theme": "自我成长",
            "problem": "人际关系的困扰",
            "method": "阿德勒心理学",
            "goal": "获得心灵自由",
            "content": "目的论、课题分离、共同体感觉",
            "skills": "处理人际关系的能力",
            "outcome": "获得真正的自由"
        }
    ]
    
    copywriter = RecommendationCopywriter()
    
    for book in books:
        print(f"\n--- 《{book['title']}》 ---")
        
        # 生成不同长度的文艺风格文案
        print("\n【文艺清新风 - 短文案】")
        print(copywriter.generate_recommendation(book, "literary", "short"))
        
        print("\n【文艺清新风 - 中文案】")
        print(copywriter.generate_recommendation(book, "literary", "medium"))
        
        print("\n【文艺清新风 - 长文案】")
        print(copywriter.generate_recommendation(book, "literary", "long"))
        
        # 如果是实用类书籍，也可以生成干货风格
        if "problem" in book:
            print("\n【干货讲书风 - 中文案】")
            print(copywriter.generate_recommendation(book, "practical", "medium"))


def example_3_different_templates():
    """示例3：使用不同的模板"""
    print("\n" + "=" * 50)
    print("示例3：使用不同的模板")
    print("=" * 50)
    
    books = [
        {
            "title": "活着",
            "author": "余华",
            "description": "讲述了一个普通人苦难而坚韧的一生",
            "quote": "人是为活着本身而活着的"
        },
        {
            "title": "被讨厌的勇气",
            "author": "岸见一郎",
            "description": "阿德勒心理学的通俗解读",
            "quote": "决定我们自身的不是过去的经历"
        },
        {
            "title": "小王子",
            "author": "安托万·德·圣-埃克苏佩里",
            "description": "一个关于爱与责任的童话",
            "quote": "真正重要的东西，用眼睛是看不见的"
        }
    ]
    
    generator = VideoScriptGenerator()
    
    # 30秒短视频模板
    print("\n--- 30秒短视频脚本 ---")
    script_30s = generator.generate_script(books[:2], "30s", "humorous")
    print_script_summary(script_30s)
    
    # 1分钟视频模板
    print("\n--- 1分钟视频脚本 ---")
    script_1min = generator.generate_script(books[:2], "1min", "literary")
    print_script_summary(script_1min)
    
    # 3分钟深度视频模板
    print("\n--- 3分钟深度视频脚本 ---")
    script_3min = generator.generate_script(books, "3min", "emotional")
    print_script_summary(script_3min)


def print_script(script: dict):
    """打印完整脚本"""
    print("\n【脚本元数据】")
    print(f"模板: {script['metadata']['template']}")
    print(f"风格: {script['metadata']['style']}")
    print(f"时长: {script['metadata']['duration']}秒")
    print(f"书籍数量: {script['metadata']['book_count']}")
    
    print("\n【脚本片段】")
    for segment in script['segments']:
        print(f"\n[{segment['time']}] {segment['type']}")
        print(f"描述: {segment['description']}")
        print(f"口播: {segment['narration']}")
        print(f"画面: {segment['visual']}")
        print(f"字幕: {segment['subtitle']}")
    
    print("\n【BGM推荐】")
    for bgm in script['materials']['bgm']:
        print(f"- {bgm}")


def print_script_summary(script: dict):
    """打印脚本摘要"""
    print(f"模板: {script['metadata']['template']}")
    print(f"风格: {script['metadata']['style']}")
    print(f"时长: {script['metadata']['duration']}秒")
    print(f"片段数: {len(script['segments'])}")
    print(f"BGM推荐: {', '.join(script['materials']['bgm'])}")


def main():
    """主函数"""
    print("\n🎬 书单视频生成器 - 使用示例 📚")
    print("=" * 50)
    
    try:
        example_1_generate_video_script()
        example_2_generate_recommendation_copy()
        example_3_different_templates()
        
        print("\n" + "=" * 50)
        print("🎉 所有示例运行完成！")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n❌ 运行出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
