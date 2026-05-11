#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一键视频生成器 - 整合搜索、文案、视频生成能力
"""

import os
import json
import requests
import shutil
from typing import Dict, List, Optional
from video_script_generator import VideoScriptGenerator, RecommendationCopywriter

# 素材保存目录
ASSETS_DIR = "video_assets"


class VideoAssetsDownloader:
    """视频素材下载器 - 自动搜索和下载书籍封面、相关图片"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.ensure_assets_dir()
    
    def ensure_assets_dir(self):
        """确保素材目录存在"""
        if not os.path.exists(ASSETS_DIR):
            os.makedirs(ASSETS_DIR)
        if not os.path.exists(os.path.join(ASSETS_DIR, "images")):
            os.makedirs(os.path.join(ASSETS_DIR, "images"))
    
    def search_book_cover(self, book_title: str, author: str = "") -> str:
        """搜索并下载书籍封面"""
        search_query = f"{book_title} {author} 书籍封面 高清"
        print(f"🔍 正在搜索封面: {search_query}")
        
        # 使用网络搜索获取图片（模拟搜索结果）
        cover_urls = self._mock_search_images(search_query)
        
        if cover_urls:
            return self.download_image(cover_urls[0], f"{book_title}_cover")
        return ""
    
    def search_related_images(self, book_title: str, keywords: List[str]) -> List[str]:
        """搜索相关主题图片"""
        downloaded_images = []
        for keyword in keywords:
            search_query = f"{book_title} {keyword}"
            print(f"🔍 正在搜索图片: {search_query}")
            
            image_urls = self._mock_search_images(search_query)
            if image_urls:
                filename = self.download_image(image_urls[0], f"{book_title}_{keyword}")
                downloaded_images.append(filename)
        
        return downloaded_images
    
    def _mock_search_images(self, query: str) -> List[str]:
        """模拟图片搜索结果（实际应用中应接入真实图片搜索API）"""
        # 模拟搜索结果，返回一些示例图片URL
        mock_results = {
            "活着 余华 书籍封面": [
                "https://neeko-copilot.bytedance.net/api/text_to_image?prompt=book%20cover%20design%20Chinese%20novel%20living%20life%20story&image_size=portrait_4_3",
                "https://neeko-copilot.bytedance.net/api/text_to_image?prompt=Chinese%20book%20cover%20minimalist%20style&image_size=portrait_4_3"
            ],
            "活着 阅读场景": [
                "https://neeko-copilot.bytedance.net/api/text_to_image?prompt=peaceful%20reading%20scene%20cozy%20room%20warm%20lighting&image_size=landscape_16_9",
                "https://neeko-copilot.bytedance.net/api/text_to_image?prompt=person%20reading%20book%20by%20window%20sunlight&image_size=landscape_16_9"
            ],
            "活着 生命": [
                "https://neeko-copilot.bytedance.net/api/text_to_image?prompt=life%20journey%20emotional%20landscape%20sunset&image_size=landscape_16_9",
                "https://neeko-copilot.bytedance.net/api/text_to_image?prompt=hope%20resilience%20nature%20mountains%20sunrise&image_size=landscape_16_9"
            ],
            "活着 苦难": [
                "https://neeko-copilot.bytedance.net/api/text_to_image?prompt=hardship%20struggle%20emotional%20drama%20cinematic&image_size=landscape_16_9",
                "https://neeko-copilot.bytedance.net/api/text_to_image?prompt=rural%20China%20village%20nostalgic%20atmosphere&image_size=landscape_16_9"
            ]
        }
        
        for key, urls in mock_results.items():
            if query.lower() in key.lower() or key.lower() in query.lower():
                return urls
        # 默认返回风景图
        return [
            "https://neeko-copilot.bytedance.net/api/text_to_image?prompt=beautiful%20landscape%20peaceful%20nature&image_size=landscape_16_9"
        ]
    
    def download_image(self, url: str, filename: str) -> str:
        """下载图片到本地"""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # 提取文件扩展名
            ext = ".jpg"
            if "content-type" in response.headers:
                content_type = response.headers["content-type"]
                if "png" in content_type:
                    ext = ".png"
                elif "gif" in content_type:
                    ext = ".gif"
            
            filepath = os.path.join(ASSETS_DIR, "images", f"{filename}{ext}")
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ 图片已下载: {filepath}")
            return filepath
        except Exception as e:
            print(f"❌ 下载图片失败: {e}")
            return ""


class SubtitleGenerator:
    """字幕生成器 - 自动生成和格式化字幕"""
    
    def __init__(self):
        pass
    
    def generate_srt_subtitles(self, script: Dict) -> str:
        """生成SRT格式字幕"""
        subtitles = []
        index = 1
        
        for segment in script['segments']:
            start_time, end_time = self._parse_time(segment['time'])
            text = segment.get('subtitle', '')
            
            if text:
                subtitle_entry = self._format_srt_entry(index, start_time, end_time, text)
                subtitles.append(subtitle_entry)
                index += 1
        
        return "\n\n".join(subtitles)
    
    def generate_ass_subtitles(self, script: Dict) -> str:
        """生成ASS格式字幕（更丰富的样式）"""
        ass_content = [
            "[Script Info]",
            "; Script generated by Booklist Video Generator",
            "Title: Booklist Video Subtitles",
            "ScriptType: v4.00+",
            "Collisions: Normal",
            "PlayResX: 1920",
            "PlayResY: 1080",
            "",
            "[V4+ Styles]",
            "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
            "Style: Default,Microsoft YaHei,48,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,2,2,2,10,10,50,134",
            "",
            "[Events]",
            "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"
        ]
        
        for segment in script['segments']:
            start_time, end_time = self._parse_time(segment['time'])
            text = segment.get('subtitle', '')
            
            if text:
                start = self._format_ass_time(start_time)
                end = self._format_ass_time(end_time)
                ass_content.append(f"Dialogue: 0,{start},{end},Default,,0,0,0,,{text}")
        
        return "\n".join(ass_content)
    
    def _parse_time(self, time_str: str) -> tuple:
        """解析时间字符串 '0-20' -> (0, 20)"""
        parts = time_str.split("-")
        return int(parts[0]), int(parts[1])
    
    def _format_srt_entry(self, index: int, start_sec: int, end_sec: int, text: str) -> str:
        """格式化SRT字幕条目"""
        start = self._format_srt_time(start_sec)
        end = self._format_srt_time(end_sec)
        return f"{index}\n{start} --> {end}\n{text}"
    
    def _format_srt_time(self, seconds: int) -> str:
        """将秒转换为SRT时间格式 00:00:00,000"""
        hrs = seconds // 3600
        mins = (seconds % 3600) // 60
        secs = seconds % 60
        return f"{hrs:02d}:{mins:02d}:{secs:02d},000"
    
    def _format_ass_time(self, seconds: int) -> str:
        """将秒转换为ASS时间格式 0:00:00.00"""
        mins = seconds // 60
        secs = seconds % 60
        return f"0:{mins:02d}:{secs:02d}.00"
    
    def save_subtitles(self, script: Dict, output_path: str, format_type: str = "srt"):
        """保存字幕文件"""
        if format_type == "ass":
            content = self.generate_ass_subtitles(script)
            ext = ".ass"
        else:
            content = self.generate_srt_subtitles(script)
            ext = ".srt"
        
        with open(output_path + ext, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 字幕已保存: {output_path}{ext}")


class VideoComposer:
    """视频合成器 - 使用MoviePy合成最终视频"""
    
    def __init__(self):
        self.has_moviepy = self._check_moviepy()
    
    def _check_moviepy(self) -> bool:
        """检查是否安装了moviepy"""
        try:
            import moviepy
            return True
        except ImportError:
            print("⚠️ 未安装moviepy，将跳过视频合成步骤")
            return False
    
    def compose_video(self, script: Dict, assets: Dict, output_path: str = "output_video"):
        """合成视频"""
        if not self.has_moviepy:
            print("❌ 需要先安装moviepy: pip install moviepy")
            return False
        
        from moviepy.editor import VideoClip, ImageClip, concatenate_videoclips, CompositeVideoClip, TextClip
        from moviepy.video.fx.resize import resize
        
        clips = []
        
        for segment in script['segments']:
            start_sec, end_sec = self._parse_time(segment['time'])
            duration = end_sec - start_sec
            
            # 获取对应的图片
            image_path = assets.get('cover', "")
            if not image_path or not os.path.exists(image_path):
                # 创建纯色背景
                clip = VideoClip(lambda t: (100, 100, 150), duration=duration)
            else:
                clip = ImageClip(image_path).set_duration(duration)
            
            # 添加字幕
            subtitle = segment.get('subtitle', '')
            if subtitle:
                txt_clip = TextClip(
                    subtitle,
                    fontsize=40,
                    color='white',
                    font='SimHei',
                    stroke_color='black',
                    stroke_width=2
                ).set_position(('center', 'bottom')).set_duration(duration)
                clip = CompositeVideoClip([clip, txt_clip])
            
            clips.append(clip)
        
        # 合并所有片段
        final_video = concatenate_videoclips(clips)
        
        # 添加背景音乐（如果有）
        # bgm_path = assets.get('bgm', "")
        # if bgm_path and os.path.exists(bgm_path):
        #     audio = AudioFileClip(bgm_path).subclip(0, final_video.duration)
        #     final_video = final_video.set_audio(audio)
        
        # 导出视频
        final_video.write_videofile(f"{output_path}.mp4", fps=24)
        print(f"✅ 视频已导出: {output_path}.mp4")
        return True
    
    def _parse_time(self, time_str: str) -> tuple:
        """解析时间字符串"""
        parts = time_str.split("-")
        return int(parts[0]), int(parts[1])


class OneClickVideoGenerator:
    """一键视频生成器 - 整合所有模块"""
    
    def __init__(self):
        self.script_generator = VideoScriptGenerator()
        self.copywriter = RecommendationCopywriter()
        self.assets_downloader = VideoAssetsDownloader()
        self.subtitle_generator = SubtitleGenerator()
        self.video_composer = VideoComposer()
    
    def generate_video(
        self,
        book_title: str,
        author: str = "",
        description: str = "",
        quote: str = "",
        theme: str = "",
        template: str = "1min",
        style: str = "emotional",
        output_name: str = "book_video"
    ) -> Dict:
        """
        一键生成视频
        
        Args:
            book_title: 书名
            author: 作者
            description: 书籍描述
            quote: 金句
            theme: 主题
            template: 视频模板 (30s/1min/3min)
            style: 文案风格
            output_name: 输出文件名
        
        Returns:
            生成结果信息
        """
        print("🎬 开始一键生成视频...")
        print("=" * 60)
        
        # 1. 准备书籍数据
        print("\n📚 步骤1: 准备书籍数据")
        books = [{
            'title': book_title,
            'author': author,
            'description': description,
            'quote': quote,
            'theme': theme,
            'characters': "",
            'plot': ""
        }]
        
        # 2. 生成脚本
        print("\n📝 步骤2: 生成视频脚本")
        script = self.script_generator.generate_script(books, template, style)
        
        # 3. 搜索并下载素材
        print("\n🖼️ 步骤3: 搜索并下载素材")
        cover_path = self.assets_downloader.search_book_cover(book_title, author)
        related_images = self.assets_downloader.search_related_images(book_title, ["阅读场景", "生命", "苦难"])
        
        assets = {
            'cover': cover_path,
            'related_images': related_images
        }
        
        # 4. 生成字幕
        print("\n📄 步骤4: 生成字幕")
        self.subtitle_generator.save_subtitles(script, output_name, "srt")
        self.subtitle_generator.save_subtitles(script, output_name, "ass")
        
        # 5. 合成视频
        print("\n🎥 步骤5: 合成视频")
        success = self.video_composer.compose_video(script, assets, output_name)
        
        # 6. 导出脚本
        print("\n💾 步骤6: 导出脚本文件")
        self.script_generator.export_script(script, f"{output_name}_script.json")
        
        print("\n" + "=" * 60)
        print("🎉 视频生成完成！")
        
        return {
            'success': success,
            'script': script,
            'assets': assets,
            'output_files': [
                f"{output_name}_script.json",
                f"{output_name}.srt",
                f"{output_name}.ass",
                f"{output_name}.mp4" if success else ""
            ]
        }


def main():
    """示例：一键生成《活着》的视频"""
    generator = OneClickVideoGenerator()
    
    result = generator.generate_video(
        book_title="活着",
        author="余华",
        description="讲述了一个普通人从富家少爷到贫苦农民的坎坷一生，展现了生命的坚韧与苦难中的希望",
        quote="人是为活着本身而活着的，而不是为活着之外的任何事物所活着",
        theme="生命的意义与坚韧",
        template="1min",
        style="emotional",
        output_name="huozhe_video"
    )
    
    print("\n📋 生成结果:")
    print(f"成功: {result['success']}")
    print(f"输出文件: {[f for f in result['output_files'] if f]}")


if __name__ == "__main__":
    main()
