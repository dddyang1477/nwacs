#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速生成书单视频 - 输入书名即可生成
"""

from one_click_video_generator import OneClickVideoGenerator

# 书籍数据库
BOOK_DATABASE = {
    "活着": {
        "title": "活着",
        "author": "余华",
        "description": "讲述了一个普通人从富家少爷到贫苦农民的坎坷一生，展现了生命的坚韧与苦难中的希望",
        "quote": "人是为活着本身而活着的，而不是为活着之外的任何事物所活着",
        "theme": "生命的意义与坚韧"
    },
    "围城": {
        "title": "围城",
        "author": "钱钟书",
        "description": "以诙谐幽默的笔调描绘了民国知识分子的生活百态，探讨了人生的困境与选择",
        "quote": "婚姻是一座围城，城外的人想进去，城里的人想出来",
        "theme": "人生困境与选择"
    },
    "三体": {
        "title": "三体",
        "author": "刘慈欣",
        "description": "一部宏大的科幻史诗，讲述了人类文明与三体文明的首次接触",
        "quote": "弱小和无知不是生存的障碍，傲慢才是",
        "theme": "宇宙文明与生存法则"
    },
    "百年孤独": {
        "title": "百年孤独",
        "author": "加西亚·马尔克斯",
        "description": "魔幻现实主义文学的巅峰之作，讲述了布恩迪亚家族七代人的传奇故事",
        "quote": "生命中所有的灿烂，终要用寂寞来偿还",
        "theme": "孤独与命运"
    },
    "红楼梦": {
        "title": "红楼梦",
        "author": "曹雪芹",
        "description": "中国古典四大名著之一，描绘了一个封建大家族的兴衰历程",
        "quote": "满纸荒唐言，一把辛酸泪",
        "theme": "家族兴衰与爱情悲剧"
    }
}


def generate_video_by_book_name(book_name: str):
    """根据书名生成视频"""
    if book_name not in BOOK_DATABASE:
        print(f"❌ 未找到书籍: {book_name}")
        print("📚 支持的书籍：活着、围城、三体、百年孤独、红楼梦")
        return
    
    book_info = BOOK_DATABASE[book_name]
    print(f"🎬 正在为《{book_name}》生成视频...")
    
    generator = OneClickVideoGenerator()
    result = generator.generate_video(
        book_title=book_info["title"],
        author=book_info["author"],
        description=book_info["description"],
        quote=book_info["quote"],
        theme=book_info["theme"],
        template="1min",
        style="emotional",
        output_name=f"{book_name}_video"
    )
    
    if result['success']:
        print(f"🎉 《{book_name}》视频生成成功！")
    else:
        print(f"⚠️ 《{book_name}》脚本和字幕已生成，视频合成需要安装moviepy")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        book_name = sys.argv[1]
    else:
        book_name = input("请输入书名: ")
    
    generate_video_by_book_name(book_name)
