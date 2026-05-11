#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成《活着》视频脚本
"""

from video_script_generator import VideoScriptGenerator, RecommendationCopywriter
import json


def main():
    # 准备《活着》的详细数据
    books = [
        {
            'title': '活着',
            'author': '余华',
            'description': '讲述了一个普通人从富家少爷到贫苦农民的坎坷一生，展现了生命的坚韧与苦难中的希望',
            'quote': '人是为活着本身而活着的，而不是为活着之外的任何事物所活着',
            'theme': '生命的意义与坚韧',
            'characters': '福贵、家珍、凤霞、有庆',
            'plot': '从富裕到贫穷，经历亲人相继离世的人生悲剧',
            'problem': '如何在苦难中找到活下去的勇气',
            'method': '通过福贵的一生展现生命的韧性',
            'goal': '理解生命的本质和活着的意义'
        }
    ]

    # 生成3分钟深度视频脚本
    generator = VideoScriptGenerator()
    script = generator.generate_script(
        books=books,
        template='3min',
        style='emotional'
    )

    # 打印脚本
    print('=' * 60)
    print('《活着》书单视频脚本')
    print('=' * 60)
    print('\n【视频信息】')
    print(f'时长: {script["metadata"]["duration"]}秒')
    print(f'风格: {script["metadata"]["style"]}')
    print(f'推荐BGM: {"、".join(script["materials"]["bgm"])}')

    print('\n' + '=' * 60)
    print('【脚本内容】')
    print('=' * 60)

    for i, segment in enumerate(script['segments']):
        print(f'\n片段{i+1}: [{segment["time"]}秒] {segment["description"]}')
        print(f'口播: {segment["narration"]}')
        print(f'画面: {segment["visual"]}')
        print(f'字幕: {segment["subtitle"]}')

    # 生成推荐文案
    copywriter = RecommendationCopywriter()
    print('\n' + '=' * 60)
    print('【推荐文案】')
    print('=' * 60)
    print('\n文艺清新风：')
    print(copywriter.generate_recommendation(books[0], 'literary', 'long'))
    print('\n干货讲书风：')
    print(copywriter.generate_recommendation(books[0], 'practical', 'medium'))

    # 导出脚本
    with open('huozhe_video_script.json', 'w', encoding='utf-8') as f:
        json.dump(script, f, ensure_ascii=False, indent=2)
    print('\n脚本已导出到: huozhe_video_script.json')


if __name__ == '__main__':
    main()
