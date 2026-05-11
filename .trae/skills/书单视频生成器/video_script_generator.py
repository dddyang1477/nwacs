#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
书单视频生成器 - 核心脚本生成模块
"""

import json
from typing import Dict, List, Optional


class VideoScriptGenerator:
    """视频脚本生成器"""
    
    def __init__(self):
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict:
        """加载视频模板"""
        return {
            "30s": {
                "duration": 30,
                "structure": [
                    {"time": "0-5", "type": "opening", "description": "开场悬念/问题"},
                    {"time": "5-15", "type": "book1", "description": "第一本书推荐"},
                    {"time": "15-25", "type": "book2", "description": "第二本书推荐"},
                    {"time": "25-30", "type": "cta", "description": "互动引导"}
                ]
            },
            "1min": {
                "duration": 60,
                "structure": [
                    {"time": "0-10", "type": "opening", "description": "开场引入"},
                    {"time": "10-25", "type": "book1", "description": "第一本书深度推荐"},
                    {"time": "25-40", "type": "book2", "description": "第二本书深度推荐"},
                    {"time": "40-55", "type": "summary", "description": "总结升华"},
                    {"time": "55-60", "type": "cta", "description": "关注引导"}
                ]
            },
            "3min": {
                "duration": 180,
                "structure": [
                    {"time": "0-20", "type": "opening", "description": "主题介绍+开场"},
                    {"time": "20-60", "type": "book1", "description": "第一本书（内容+金句+感悟）"},
                    {"time": "60-100", "type": "book2", "description": "第二本书（内容+金句+感悟）"},
                    {"time": "100-140", "type": "book3", "description": "第三本书（内容+金句+感悟）"},
                    {"time": "140-160", "type": "summary", "description": "书单总结+行动建议"},
                    {"time": "160-180", "type": "cta", "description": "互动引导+关注"}
                ]
            }
        }
    
    def generate_script(
        self,
        books: List[Dict],
        template: str = "1min",
        style: str = "literary"
    ) -> Dict:
        """
        生成视频脚本
        
        Args:
            books: 书籍列表，每本书包含 title, author, description, quote
            template: 模板类型 "30s", "1min", "3min"
            style: 文案风格
        
        Returns:
            完整的视频脚本
        """
        if template not in self.templates:
            template = "1min"
        
        template_data = self.templates[template]
        book_count = len(books)
        
        script = {
            "metadata": {
                "template": template,
                "style": style,
                "duration": template_data["duration"],
                "book_count": book_count
            },
            "segments": [],
            "materials": {
                "images": [],
                "bgm": self._suggest_bgm(style),
                "subtitles": []
            }
        }
        
        for segment in template_data["structure"]:
            segment_content = self._generate_segment_content(
                segment, books, style, book_count
            )
            # 过滤掉空的书籍片段
            if not (segment["type"].startswith("book") and segment_content["narration"] == ""):
                script["segments"].append(segment_content)
        
        return script
    
    def _generate_segment_content(
        self,
        segment: Dict,
        books: List[Dict],
        style: str,
        book_count: int = 1
    ) -> Dict:
        """生成单个片段的内容"""
        content = {
            "time": segment["time"],
            "type": segment["type"],
            "description": segment["description"],
            "narration": "",
            "visual": "",
            "subtitle": ""
        }
        
        if segment["type"] == "opening":
            content.update(self._generate_opening(books, style, book_count))
        elif segment["type"].startswith("book"):
            book_index = int(segment["type"].replace("book", "")) - 1
            if book_index < len(books):
                # 如果只有一本书，为3分钟模板生成更详细的内容
                if book_count == 1 and book_index == 0:
                    content.update(self._generate_single_book_deep_dive(books[book_index], style, segment["time"]))
                else:
                    content.update(self._generate_book_segment(books[book_index], style))
        elif segment["type"] == "summary":
            content.update(self._generate_summary(books, style))
        elif segment["type"] == "cta":
            content.update(self._generate_cta(style))
        
        return content
    
    def _generate_opening(self, books: List[Dict], style: str, book_count: int) -> Dict:
        """生成开场内容"""
        # 根据书籍数量选择合适的开场文案
        if book_count == 1:
            book_title = books[0].get("title", "这本书")
            openings = {
                "literary": {
                    "narration": f"今天想和大家分享一本让我深受触动的书——《{book_title}》。",
                    "visual": f"展示《{book_title}》的封面，搭配温馨的阅读场景",
                    "subtitle": f"今日荐书：《{book_title}》"
                },
                "practical": {
                    "narration": f"今天给大家推荐一本非常值得一读的书——《{book_title}》。",
                    "visual": f"展示《{book_title}》的封面，搭配简洁的背景",
                    "subtitle": f"好书推荐：《{book_title}》"
                },
                "humorous": {
                    "narration": f"书荒的小伙伴看过来！今天推荐的《{book_title}》绝对让你欲罢不能！",
                    "visual": f"展示《{book_title}》的封面，搭配有趣的动画效果",
                    "subtitle": f"这本好书你不能错过！"
                },
                "emotional": {
                    "narration": f"有一本书，让无数人泪流满面，也让无数人重新思考生命的意义——它就是《{book_title}》。",
                    "visual": f"展示《{book_title}》的封面，搭配温暖的光影效果",
                    "subtitle": f"感动千万人的书：《{book_title}》"
                }
            }
        else:
            openings = {
                "literary": {
                    "narration": "你是否也在寻找一本能触动心灵的书？今天为你推荐几本值得一读的好书。",
                    "visual": "展示温馨的阅读场景，搭配柔和的光影效果",
                    "subtitle": "今天推荐的好书"
                },
                "practical": {
                    "narration": "想提升自己却不知道读什么？今天这份书单帮你快速成长。",
                    "visual": "展示办公或学习场景，突出书籍的实用性",
                    "subtitle": "成长必读书单"
                },
                "humorous": {
                    "narration": "书荒了？别慌！今天这几本书保证让你看得停不下来！",
                    "visual": "展示有趣的书籍封面或搞笑的读书场景",
                    "subtitle": "告别书荒"
                },
                "emotional": {
                    "narration": "有些书，读过之后会改变你的人生轨迹。今天就为大家推荐这样的好书。",
                    "visual": "展示书架或阅读场景，搭配温暖的色调",
                    "subtitle": "改变人生的好书"
                }
            }
        return openings.get(style, openings["literary"])
    
    def _generate_book_segment(self, book: Dict, style: str) -> Dict:
        """生成书籍推荐片段"""
        return {
            "narration": f"《{book['title']}》 by {book['author']}。{book['description']}",
            "visual": f"展示《{book['title']}》的封面，搭配书中精彩片段",
            "subtitle": f"《{book['title']}》- {book.get('quote', '')}"
        }
    
    def _generate_single_book_deep_dive(self, book: Dict, style: str, time_range: str) -> Dict:
        """为单本书生成深度解析内容"""
        time_parts = time_range.split("-")
        duration = int(time_parts[1]) - int(time_parts[0])
        
        if duration >= 100:
            # 长片段：详细解析
            return {
                "narration": f"《{book['title']}》是{book['author']}最具代表性的作品之一。这本书讲述了{book['characters']}等人物的故事，通过{book['plot']}的情节，深刻探讨了{book['theme']}这一主题。书中最经典的一句话是：{book.get('quote', '')}",
                "visual": f"依次展示《{book['title']}》的封面、作者照片、书中精彩段落截图，可以加入一些象征性的画面",
                "subtitle": f"《{book['title']}》深度解析"
            }
        elif duration >= 40:
            # 中等片段：详细推荐
            return {
                "narration": f"《{book['title']}》by {book['author']}。这本书用朴实无华的语言，讲述了一个关于{book['theme']}的深刻故事。{book.get('description', '')}",
                "visual": f"展示《{book['title']}》的封面，搭配书中经典场景的画面",
                "subtitle": f"《{book['title']}》- {book.get('quote', '')[:30]}..."
            }
        else:
            # 短片段：简洁推荐
            return self._generate_book_segment(book, style)
    
    def _generate_summary(self, books: List[Dict], style: str) -> Dict:
        """生成总结内容"""
        book_count = len(books)
        if book_count == 1:
            book = books[0]
            return {
                "narration": f"《{book['title']}》是一本值得反复阅读的书，它让我们重新思考生命的意义。希望今天的分享能让你有所收获，也欢迎在评论区分享你的读后感。",
                "visual": f"再次展示《{book['title']}》的封面，搭配温馨的阅读场景",
                "subtitle": f"《{book['title']}》推荐完毕"
            }
        else:
            book_titles = "、".join([f"《{b['title']}》" for b in books])
            return {
                "narration": f"以上就是今天推荐的{book_titles}，希望对你有所帮助。",
                "visual": "展示所有推荐书籍的封面合集",
                "subtitle": "感谢观看"
            }
    
    def _generate_cta(self, style: str) -> Dict:
        """生成互动引导内容"""
        ctas = {
            "literary": {
                "narration": "如果你喜欢这期视频，别忘了点赞关注，我们下期再见。",
                "visual": "显示点赞、关注的图标",
                "subtitle": "点赞+关注"
            },
            "practical": {
                "narration": "觉得有用的话，点赞收藏，把这份书单分享给更多需要的人。",
                "visual": "显示收藏、分享的图标",
                "subtitle": "收藏+分享"
            },
            "emotional": {
                "narration": "如果你也被这本书感动，别忘了点赞关注，让更多人读到这本好书。",
                "visual": "显示点赞、关注、分享的图标",
                "subtitle": "点赞+关注+分享"
            }
        }
        return ctas.get(style, ctas["literary"])
    
    def _suggest_bgm(self, style: str) -> List[str]:
        """推荐背景音乐"""
        bgm_map = {
            "literary": ["舒缓钢琴曲", "轻音乐", "古典吉他"],
            "practical": ["轻快电子乐", "励志背景音乐", "节奏明快的纯音乐"],
            "humorous": ["欢快的卡通音乐", "俏皮的背景音乐"],
            "professional": ["专业的新闻配乐", "商务背景音乐"],
            "emotional": ["情感丰富的配乐", "感人的背景音乐"]
        }
        return bgm_map.get(style, bgm_map["literary"])
    
    def export_script(self, script: Dict, output_path: str):
        """导出脚本为JSON文件"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(script, f, ensure_ascii=False, indent=2)


class RecommendationCopywriter:
    """推荐文案生成器"""
    
    def __init__(self):
        self.styles = {
            "literary": "文艺清新风",
            "practical": "干货讲书风",
            "humorous": "幽默风趣风",
            "professional": "专业深度风",
            "emotional": "情感共鸣风"
        }
    
    def generate_recommendation(
        self,
        book: Dict,
        style: str = "literary",
        length: str = "medium"
    ) -> str:
        """生成推荐文案"""
        templates = self._get_templates(style, length)
        return self._fill_template(templates, book)
    
    def _get_templates(self, style: str, length: str) -> Dict:
        """获取文案模板"""
        templates = {
            "literary": {
                "short": "在《{title}》中，{author}用细腻的笔触，勾勒出一个触动心灵的世界。",
                "medium": "《{title}》是{author}的代表作。这本书用诗意的语言，讲述了一个关于{theme}的故事，每一页都能让你感受到文字的魅力。",
                "long": "翻开《{title}》，就像走进了{author}精心构建的世界。在这里，你会遇见{characters}，经历{plot}。这本书不仅是一个故事，更是一次心灵的旅行，让你在阅读中找到共鸣与感动。"
            },
            "practical": {
                "short": "《{title}》by {author}，一本能帮你解决{problem}的实用好书。",
                "medium": "想解决{problem}？《{title}》给出了答案。{author}通过{method}，教你如何{goal}，干货满满，值得一读。",
                "long": "在这个快速变化的时代，我们需要实用的知识来指导生活。《{title}》正是这样一本书，{author}用多年的经验总结，系统地讲解了{content}。读完这本书，你将掌握{skills}，能够{outcome}。"
            }
        }
        return templates.get(style, templates["literary"])[length]
    
    def _fill_template(self, template: str, book: Dict) -> str:
        """填充模板"""
        return template.format(
            title=book.get("title", ""),
            author=book.get("author", ""),
            theme=book.get("theme", "成长与爱"),
            characters=book.get("characters", "一个个鲜活的人物"),
            plot=book.get("plot", "一段段难忘的经历"),
            problem=book.get("problem", "生活中的困惑"),
            method=book.get("method", "科学的方法"),
            goal=book.get("goal", "实现目标"),
            content=book.get("content", "核心知识"),
            skills=book.get("skills", "实用技能"),
            outcome=book.get("outcome", "更好地应对挑战")
        )


def main():
    """示例使用"""
    # 示例书籍
    sample_books = [
        {
            "title": "活着",
            "author": "余华",
            "description": "讲述了一个普通人苦难而坚韧的一生",
            "quote": "人是为活着本身而活着的",
            "theme": "生命的意义"
        },
        {
            "title": "被讨厌的勇气",
            "author": "岸见一郎",
            "description": "阿德勒心理学的通俗解读，帮你获得自由",
            "quote": "决定我们自身的不是过去的经历",
            "theme": "自我成长"
        }
    ]
    
    # 生成脚本
    generator = VideoScriptGenerator()
    script = generator.generate_script(
        sample_books,
        template="1min",
        style="literary"
    )
    
    print("生成的视频脚本：")
    print(json.dumps(script, ensure_ascii=False, indent=2))
    
    # 生成推荐文案
    copywriter = RecommendationCopywriter()
    for book in sample_books:
        copy = copywriter.generate_recommendation(book, "literary", "medium")
        print(f"\n《{book['title']}》推荐文案：")
        print(copy)


if __name__ == "__main__":
    main()
