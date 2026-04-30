#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试novel-writer工具
"""

from novel_writer import NovelWriter

def test_novel_writer():
    """测试NovelWriter工具"""
    print("=" * 60)
    print("    测试 NovelWriter 工具")
    print("=" * 60)
    
    try:
        # 创建实例
        writer = NovelWriter()
        print("[OK] NovelWriter初始化成功")
        
        # 测试生成大纲
        print("\n【测试1】生成小说大纲")
        outline = writer.generate_outline('玄幻修仙', '逆袭')
        print("  小说标题:", outline['title'])
        print("  一句话梗概:", outline['logline'])
        print("  主角:", outline['protagonist']['name'])
        print("  反派:", outline['antagonist']['name'])
        print("  章节数:", len(outline['chapters']))
        print("[OK] 大纲生成成功")
        
        # 测试生成章节
        print("\n【测试2】生成章节内容")
        chapter_info = {'chapter': 1, 'title': '第一章 初入江湖', 'content': '第一幕内容'}
        chapter_content = writer.generate_chapter(chapter_info, outline)
        print("  章节内容预览:", chapter_content[:100], "...")
        print("[OK] 章节生成成功")
        
        # 测试润色
        print("\n【测试3】文本润色")
        text = "他很开心，跑了起来"
        polished = writer.polish_text(text, style="华丽")
        print("  原文:", text)
        print("  润色后:", polished)
        print("[OK] 润色成功")
        
        # 测试保存
        print("\n【测试4】保存小说")
        result = writer.save_novel(outline)
        if result['success']:
            print("  保存成功:", result['filename'])
        else:
            print("  保存失败:", result['error'])
        
        print("\n" + "=" * 60)
        print("    NovelWriter 工具测试完成")
        print("=" * 60)
        
    except Exception as e:
        print("[ERROR] 测试失败:", str(e))
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_novel_writer()