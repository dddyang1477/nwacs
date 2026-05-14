#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS Novel Writer Tool
小说创作核心工具，支持大纲生成、章节创作、内容润色等功能
"""

import os
import json
import random
from datetime import datetime
from logger import logger

class NovelWriter:
    """小说创作工具"""
    
    def __init__(self):
        self.logger = logger
        self.logger.info("NovelWriter 工具初始化完成")
        
    def generate_outline(self, genre, theme, length="长篇"):
        """生成小说大纲"""
        outline = {
            'genre': genre,
            'theme': theme,
            'length': length,
            'title': self._generate_title(genre, theme),
            'logline': self._generate_logline(genre, theme),
            'protagonist': self._generate_protagonist(genre),
            'antagonist': self._generate_antagonist(genre),
            'three_act_structure': self._generate_three_act_structure(genre, theme),
            'chapters': self._generate_chapter_list(genre, length),
            'themes': self._generate_themes(theme),
            'tone': self._generate_tone(genre)
        }
        
        self.logger.info(f"已生成{genre}小说大纲: {outline['title']}")
        return outline
    
    def _generate_title(self, genre, theme):
        """生成小说标题"""
        titles = {
            '玄幻修仙': ['逆鳞', '天渊', '剑墟', '道骨', '龙血', '玄黄', '尘缘', '仙路'],
            '都市异能': ['觉醒', '超凡', '禁区', '神级', '都市', '巅峰', '无敌', '至尊'],
            '历史架空': ['天下', '山河', '王朝', '帝国', '霸业', '征途', '龙图', '锦绣'],
            '科幻未来': ['星际', '银河', '纪元', '奇点', '跃迁', '星舰', '深空', '重生'],
            '悬疑推理': ['迷局', '真相', '追凶', '暗影', '谜案', '解密', '深渊', '救赎'],
            '言情纯爱': ['心动', '余生', '遇见', '情深', '挚爱', '暖婚', '蜜恋', '星辰'],
            '武侠江湖': ['侠影', '剑心', '江湖', '风云', '铁血', '柔情', '武魂', '传奇'],
            '恐怖惊悚': ['惊魂', '鬼域', '噩梦', '咒怨', '诡影', '禁地', '午夜', '惊悚'],
            '游戏异界': ['重生', '系统', '攻略', '巅峰', '神级', '无敌', '穿越', '争霸']
        }
        
        genre_titles = titles.get(genre, ['传奇', '故事', '风云', '史诗'])
        title_parts = random.sample(genre_titles, 2)
        
        return f"{title_parts[0]}{title_parts[1]}"
    
    def _generate_logline(self, genre, theme):
        """生成一句话梗概"""
        loglines = {
            '玄幻修仙': f"一个{theme}的少年，意外获得{self._get_random_treasure()}，从此踏上{self._get_random_path()}的逆袭之路",
            '都市异能': f"{theme}的普通青年，在一次意外中觉醒{self._get_random_power()}，开启都市{self._get_random_journey()}传奇",
            '历史架空': f"{theme}的少年，凭借{self._get_random_ability()}，在{self._get_random_era()}书写{self._get_random_destiny()}",
            '科幻未来': f"{theme}的{self._get_random_role()}，在{self._get_random_crisis()}中，{self._get_random_action()}拯救{self._get_random_target()}",
            '悬疑推理': f"一桩{theme}的{self._get_random_case()}，{self._get_random_detective()}如何{self._get_random_investigate()}揭开{self._get_random_truth()}",
            '言情纯爱': f"{theme}的{self._get_random_meet()}，让{self._get_random_character()}与{self._get_random_character()}相遇，演绎{self._get_random_love()}",
            '武侠江湖': f"{theme}的{self._get_random_wuxia()}，背负{self._get_random_secret()}，在{self._get_random_world()}中{self._get_random_fight()}",
            '恐怖惊悚': f"{theme}的{self._get_random_setting()}，{self._get_random_event()}引发{self._get_random_horror()}，{self._get_random_survivor()}如何{self._get_random_survive()}",
            '游戏异界': f"{theme}的{self._get_random_gamer()}，穿越到{self._get_random_game()}，凭借{self._get_random_skill()}成为{self._get_random_legend()}"
        }
        
        return loglines.get(genre, f"{theme}的故事")
    
    def _generate_protagonist(self, genre):
        """生成主角设定"""
        protagonists = {
            '玄幻修仙': {
                'name': self._get_random_name('male'),
                'background': '小宗门弟子/废柴少爷/普通少年',
                'personality': '隐忍坚韧/智计百出/重情重义',
                'goal': '复仇/守护/追求大道',
                'flaw': '过于执着/轻信他人/情感牵绊'
            },
            '都市异能': {
                'name': self._get_random_name('male'),
                'background': '普通上班族/大学生/草根青年',
                'personality': '低调务实/热血正义/机智幽默',
                'goal': '保护身边的人/探索真相/追求更强',
                'flaw': '责任感过强/不善表达/冲动'
            },
            '历史架空': {
                'name': self._get_random_name('male'),
                'background': '寒门子弟/没落贵族/边疆小兵',
                'personality': '深谋远虑/杀伐果断/知人善任',
                'goal': '争霸天下/兴复家国/守护百姓',
                'flaw': '疑心太重/杀伐过重/执念太深'
            },
            '言情纯爱': {
                'name': self._get_random_name('female'),
                'background': '都市白领/豪门千金/普通少女',
                'personality': '温柔善良/独立自主/坚强勇敢',
                'goal': '寻找真爱/实现自我/守护幸福',
                'flaw': '过于善良/缺乏安全感/犹豫不决'
            }
        }
        
        return protagonists.get(genre, {
            'name': self._get_random_name('male'),
            'background': '普通人',
            'personality': '勇敢善良',
            'goal': '追求梦想',
            'flaw': '经验不足'
        })
    
    def _generate_antagonist(self, genre):
        """生成反派设定"""
        antagonists = {
            '玄幻修仙': {
                'name': self._get_random_name('male'),
                'role': '大宗门少主/魔道巨擘/上古邪魔',
                'motivation': '追求力量/复仇/统治天下',
                'strength': '修为高深/势力庞大/智谋过人',
                'weakness': '骄傲自大/有执念/被利用'
            },
            '都市异能': {
                'name': self._get_random_name('male'),
                'role': '神秘组织首领/黑暗势力头目/变异怪物',
                'motivation': '夺取资源/控制他人/毁灭世界',
                'strength': '实力强大/资源丰富/手段狠辣',
                'weakness': '野心太大/内部矛盾/有软肋'
            },
            '历史架空': {
                'name': self._get_random_name('male'),
                'role': '敌国皇帝/权臣奸臣/野心诸侯',
                'motivation': '称霸天下/权力欲望/家族恩怨',
                'strength': '权倾朝野/兵力雄厚/谋略深远',
                'weakness': '不得民心/众叛亲离/年老力衰'
            }
        }
        
        return antagonists.get(genre, {
            'name': self._get_random_name('male'),
            'role': '反派角色',
            'motivation': '邪恶目的',
            'strength': '强大',
            'weakness': '有弱点'
        })
    
    def _generate_three_act_structure(self, genre, theme):
        """生成三幕式结构"""
        return {
            'act1': {
                'title': '启程',
                'plot_points': [
                    f"介绍主角的{theme}生活",
                    '主角面临困境/挑战',
                    '获得机遇/奇遇',
                    '下定决心踏上旅程'
                ]
            },
            'act2': {
                'title': '考验',
                'plot_points': [
                    '主角在历练中成长',
                    '结识伙伴/遭遇敌人',
                    '揭露重大秘密/阴谋',
                    '面临重大挫折/背叛',
                    '主角陷入低谷'
                ]
            },
            'act3': {
                'title': '决战',
                'plot_points': [
                    '主角领悟/突破',
                    '集结力量准备决战',
                    '最终对决',
                    '结局/新的开始'
                ]
            }
        }
    
    def _generate_chapter_list(self, genre, length):
        """生成章节列表"""
        chapter_counts = {
            '短篇': 10,
            '中篇': 30,
            '长篇': 100
        }
        
        count = chapter_counts.get(length, 30)
        chapters = []
        
        for i in range(1, count + 1):
            if i == 1:
                chapters.append({'chapter': i, 'title': '序章/第一章', 'content': '引子/开端'})
            elif i <= count * 0.2:
                chapters.append({'chapter': i, 'title': f'第{i}章', 'content': '第一幕内容'})
            elif i <= count * 0.6:
                chapters.append({'chapter': i, 'title': f'第{i}章', 'content': '第二幕内容'})
            elif i < count:
                chapters.append({'chapter': i, 'title': f'第{i}章', 'content': '第三幕内容'})
            else:
                chapters.append({'chapter': i, 'title': f'第{i}章 终章', 'content': '结局'})
        
        return chapters
    
    def _generate_themes(self, theme):
        """生成主题列表"""
        theme_map = {
            '逆袭': ['成长', '奋斗', '坚持', '逆袭', '梦想'],
            '复仇': ['仇恨', '正义', '救赎', '放下', '因果'],
            '爱情': ['真爱', '守护', '成长', '包容', '牺牲'],
            '争霸': ['权力', '野心', '谋略', '人心', '取舍'],
            '探险': ['探索', '勇气', '发现', '成长', '敬畏'],
            '悬疑': ['真相', '谎言', '正义', '救赎', '人性']
        }
        
        return theme_map.get(theme, ['成长', '友情', '勇气'])
    
    def _generate_tone(self, genre):
        """生成风格调性"""
        tones = {
            '玄幻修仙': '热血激昂/沉稳大气/略带诙谐',
            '都市异能': '轻松爽快/略带悬疑/情感真挚',
            '历史架空': '厚重深沉/权谋博弈/史诗感',
            '科幻未来': '硬核严谨/充满想象/略带惊悚',
            '悬疑推理': '紧张刺激/逻辑严密/层层递进',
            '言情纯爱': '温馨甜蜜/略带虐心/情感细腻',
            '武侠江湖': '快意恩仇/热血豪情/侠骨柔情',
            '恐怖惊悚': '阴森恐怖/心理压迫/反转不断',
            '游戏异界': '轻松爽文/策略博弈/成长升级'
        }
        
        return tones.get(genre, '适中')
    
    def _get_random_name(self, gender):
        """生成随机名字"""
        male_names = ['林云', '叶辰', '秦风', '苏铭', '陈凡', '楚枫', '叶凡', '石昊', '王林', '孟浩']
        female_names = ['苏雪', '林雨', '柳月', '陈瑶', '云汐', '风晚', '紫烟', '婉清', '雨柔', '梦瑶']
        
        if gender == 'female':
            return random.choice(female_names)
        return random.choice(male_names)
    
    def _get_random_treasure(self):
        """获取随机宝物"""
        return random.choice(['神秘传承', '上古神器', '逆天功法', '变异灵根', '奇遇机缘'])
    
    def _get_random_path(self):
        """获取随机道路"""
        return random.choice(['逆天', '传奇', '无敌', '至尊'])
    
    def _get_random_power(self):
        """获取随机能力"""
        return random.choice(['超强异能', '神秘系统', '古老传承', '未来科技'])
    
    def _get_random_journey(self):
        """获取随机旅程"""
        return random.choice(['强者', '传奇', '无敌', '巅峰'])
    
    def _get_random_ability(self):
        """获取随机能力"""
        return random.choice(['超凡智慧', '无双武艺', '治国之才', '经商天赋'])
    
    def _get_random_era(self):
        """获取随机时代"""
        return random.choice(['乱世', '盛世', '王朝末年', '新朝初立'])
    
    def _get_random_destiny(self):
        """获取随机命运"""
        return random.choice(['传奇', '霸业', '传奇人生', '不朽传说'])
    
    def _get_random_role(self):
        """获取随机角色"""
        return random.choice(['科学家', '宇航员', '战士', '探险家'])
    
    def _get_random_crisis(self):
        """获取随机危机"""
        return random.choice(['外星入侵', 'AI反叛', '时空危机', '资源枯竭'])
    
    def _get_random_action(self):
        """获取随机行动"""
        return random.choice(['带领人类', '孤身一人', '联合盟友'])
    
    def _get_random_target(self):
        """获取随机目标"""
        return random.choice(['地球', '文明', '宇宙', '未来'])
    
    def _get_random_case(self):
        """获取随机案件"""
        return random.choice(['离奇命案', '失踪案', '连环杀人', '密室谋杀'])
    
    def _get_random_detective(self):
        """获取随机侦探"""
        return random.choice(['天才侦探', '普通警察', '私家侦探', '法医'])
    
    def _get_random_investigate(self):
        """获取随机调查方式"""
        return random.choice(['抽丝剥茧', '层层深入', '险象环生'])
    
    def _get_random_truth(self):
        """获取随机真相"""
        return random.choice(['惊人真相', '隐藏秘密', '惊天阴谋'])
    
    def _get_random_meet(self):
        """获取随机相遇"""
        return random.choice(['意外', '命中注定', '戏剧性'])
    
    def _get_random_character(self):
        """获取随机角色"""
        return random.choice(['高冷总裁', '阳光少年', '温柔医生', '神秘男神'])
    
    def _get_random_love(self):
        """获取随机爱情"""
        return random.choice(['甜蜜爱情', '虐心之恋', '暖心故事'])
    
    def _get_random_wuxia(self):
        """获取随机武侠元素"""
        return random.choice(['少年侠客', '隐世高手', '江湖浪子'])
    
    def _get_random_secret(self):
        """获取随机秘密"""
        return random.choice(['血海深仇', '家族秘密', '身世之谜'])
    
    def _get_random_world(self):
        """获取随机世界"""
        return random.choice(['江湖', '武林', '乱世'])
    
    def _get_random_fight(self):
        """获取随机战斗"""
        return random.choice(['快意恩仇', '行侠仗义', '争霸武林'])
    
    def _get_random_setting(self):
        """获取随机场景"""
        return random.choice(['古老宅院', '荒村', '废弃医院', '孤岛'])
    
    def _get_random_event(self):
        """获取随机事件"""
        return random.choice(['怪事频发', '噩梦成真', '诅咒降临'])
    
    def _get_random_horror(self):
        """获取随机恐怖"""
        return random.choice(['恐怖事件', '灵异现象', '血腥杀戮'])
    
    def _get_random_survivor(self):
        """获取随机幸存者"""
        return random.choice(['一群年轻人', '探险队', '一家人'])
    
    def _get_random_survive(self):
        """获取随机生存方式"""
        return random.choice(['挣扎求生', '揭开真相', '破除诅咒'])
    
    def _get_random_gamer(self):
        """获取随机玩家"""
        return random.choice(['职业玩家', '普通少年', '游戏废宅'])
    
    def _get_random_game(self):
        """获取随机游戏"""
        return random.choice(['虚拟游戏', '异界大陆', '末世游戏'])
    
    def _get_random_skill(self):
        """获取随机技能"""
        return random.choice(['游戏知识', '战略头脑', '特殊天赋'])
    
    def _get_random_legend(self):
        """获取随机传奇"""
        return random.choice(['游戏传奇', '异界霸主', '无敌玩家'])
    
    def generate_chapter(self, chapter_info, outline):
        """生成章节内容"""
        chapter_num = chapter_info['chapter']
        chapter_title = chapter_info['title']
        content_type = chapter_info['content']
        
        content = f"## {chapter_title}\n\n"
        
        if chapter_num == 1:
            content += self._generate_opening(outline)
        elif content_type == '第一幕内容':
            content += self._generate_act1_content(outline, chapter_num)
        elif content_type == '第二幕内容':
            content += self._generate_act2_content(outline, chapter_num)
        elif content_type == '第三幕内容':
            content += self._generate_act3_content(outline, chapter_num)
        elif '终章' in chapter_title:
            content += self._generate_climax(outline)
        
        return content
    
    def _generate_opening(self, outline):
        """生成开场"""
        protag = outline['protagonist']
        return f"【{outline['title']}】\n\n{outline['logline']}\n\n{protag['name']}，一个出身{protag['background']}的少年，性格{protag['personality']}。他的梦想是{protag['goal']}，但命运似乎对他并不眷顾...\n\n第一章的故事，从{self._get_random_starting_point()}开始..."
    
    def _generate_act1_content(self, outline, chapter_num):
        """生成第一幕内容"""
        events = [
            f"{outline['protagonist']['name']}遭遇了人生的第一个重大挫折",
            "机缘巧合之下，他获得了改变命运的契机",
            "踏上了一条未知的道路",
            "初入江湖/宗门/都市，见识到了新世界的广阔",
            "结识了第一位重要的伙伴/导师",
            "遭遇了第一个小BOSS/挑战"
        ]
        
        return events[(chapter_num - 1) % len(events)] + "\n\n" + self._generate_descriptive_text()
    
    def _generate_act2_content(self, outline, chapter_num):
        """生成第二幕内容"""
        events = [
            f"{outline['protagonist']['name']}在历练中不断成长",
            "结识更多伙伴，建立深厚情谊",
            "遭遇{outline['antagonist']['name']}的初次打压",
            "发现惊天秘密/阴谋",
            "经历重大背叛/挫折",
            "陷入人生低谷，开始反思"
        ]
        
        return events[(chapter_num - 1) % len(events)] + "\n\n" + self._generate_descriptive_text()
    
    def _generate_act3_content(self, outline, chapter_num):
        """生成第三幕内容"""
        events = [
            f"{outline['protagonist']['name']}领悟真谛，实力突破",
            "集结伙伴，准备最终决战",
            "与{outline['antagonist']['name']}的终极对决",
            "揭露最终真相",
            "尘埃落定，迎来结局"
        ]
        
        return events[(chapter_num - 1) % len(events)] + "\n\n" + self._generate_descriptive_text()
    
    def _generate_climax(self, outline):
        """生成高潮结局"""
        return f"最终决战爆发！\n\n{outline['protagonist']['name']}与{outline['antagonist']['name']}展开惊天对决，天地变色，风云激荡！\n\n经过惊心动魄的激战，{outline['protagonist']['name']}最终{self._get_random_outcome()}！\n\n【全书完】"
    
    def _generate_descriptive_text(self):
        """生成描写性文字"""
        descriptions = [
            "夕阳的余晖洒落在连绵的山脉上，将整个世界染成一片金红。",
            "夜色渐浓，星辰点点，微风拂过树梢，带来阵阵清凉。",
            "繁华的都市灯火辉煌，车水马龙，喧嚣中透着一丝孤独。",
            "古老的宗门矗立在云雾缭绕的山峰之巅，神秘而威严。",
            "剑鸣声声，剑气纵横，一场惊心动魄的对决正在上演！",
            "月光如水，洒落庭院，映照出他孤寂的身影。",
            "血雨腥风过后，残阳如血，满地狼藉诉说着刚刚的惨烈。",
            "春风拂面，花香四溢，一切都显得那么宁静美好。"
        ]
        
        return random.choice(descriptions)
    
    def _get_random_starting_point(self):
        """获取随机起点"""
        return random.choice([
            "一个平凡的午后",
            "一场突如其来的变故",
            "一次意外的发现",
            "一段尘封的记忆"
        ])
    
    def _get_random_outcome(self):
        """获取随机结局"""
        return random.choice([
            "战胜了邪恶，守护了心中珍视的一切",
            "功成身退，归隐山林",
            "成为一代传奇，受万人敬仰",
            "找到了真正的自我，踏上新的征程"
        ])
    
    def polish_text(self, text, style="流畅"):
        """润色文本"""
        polished = text
        
        if style == "简洁":
            polished = self._simplify_text(text)
        elif style == "华丽":
            polished = self._embellish_text(text)
        elif style == "古风":
            polished = self._ancient_style(text)
        
        return polished
    
    def _simplify_text(self, text):
        """简化文本"""
        return text.replace("非常", "").replace("十分", "").replace("特别", "")
    
    def _embellish_text(self, text):
        """美化文本"""
        embellishments = ["璀璨的", "绚丽的", "神秘的", "悠远的", "苍茫的"]
        words = text.split()
        result = []
        for i, word in enumerate(words):
            if i % 3 == 0 and word.isalpha():
                result.append(random.choice(embellishments) + word)
            else:
                result.append(word)
        return ' '.join(result)
    
    def _ancient_style(self, text):
        """转换古风"""
        replacements = {
            "的": "之",
            "了": "矣",
            "是": "乃",
            "在": "于",
            "和": "与",
            "有": "有",
            "我": "吾",
            "你": "汝",
            "他": "其"
        }
        
        for old, new in replacements.items():
            text = text.replace(old, new)
        
        return text
    
    def save_novel(self, novel_data, filename=None):
        """保存小说"""
        if not filename:
            filename = f"{novel_data['title']}_{datetime.now().strftime('%Y%m%d')}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"【小说标题】{novel_data['title']}\n\n")
                f.write(f"【一句话梗概】{novel_data['logline']}\n\n")
                f.write(f"【类型】{novel_data['genre']}\n")
                f.write(f"【主题】{novel_data['theme']}\n")
                f.write(f"【篇幅】{novel_data['length']}\n")
                f.write(f"【风格】{novel_data['tone']}\n\n")
                
                f.write("【主角设定】\n")
                for key, value in novel_data['protagonist'].items():
                    f.write(f"  - {key}: {value}\n")
                
                f.write("\n【反派设定】\n")
                for key, value in novel_data['antagonist'].items():
                    f.write(f"  - {key}: {value}\n")
                
                f.write("\n【三幕式结构】\n")
                for act, content in novel_data['three_act_structure'].items():
                    f.write(f"【{content['title']}】\n")
                    for i, point in enumerate(content['plot_points'], 1):
                        f.write(f"  {i}. {point}\n")
                
                f.write("\n【章节列表】\n")
                for chapter in novel_data['chapters'][:20]:
                    f.write(f"  第{chapter['chapter']}章 {chapter['title']}\n")
                
                if len(novel_data['chapters']) > 20:
                    f.write(f"  ...（共{len(novel_data['chapters'])}章）\n")
            
            self.logger.info(f"小说已保存: {filename}")
            return {'success': True, 'filename': filename}
        
        except Exception as e:
            self.logger.log_exception(e, "save_novel")
            return {'success': False, 'error': str(e)}

# 测试
if __name__ == "__main__":
    writer = NovelWriter()
    
    # 测试生成大纲
    outline = writer.generate_outline('玄幻修仙', '逆袭')
    print(f"小说标题: {outline['title']}")
    print(f"一句话梗概: {outline['logline']}")
    print(f"主角: {outline['protagonist']['name']}")
    print(f"章节数: {len(outline['chapters'])}")
    
    # 测试保存
    result = writer.save_novel(outline)
    print(f"保存结果: {result}")