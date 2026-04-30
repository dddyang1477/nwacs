#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 创作模板库与素材库
功能：开篇模板、爽点模板、描写素材、对话模板
"""

import json
import os
import random
from logger import logger

class TemplateLibrary:
    """创作模板库"""
    
    def __init__(self):
        self.templates_file = "writing_templates.json"
        self.templates = {}
        self._load_templates()
    
    def _load_templates(self):
        """加载模板"""
        # 内置模板
        self.templates = {
            '开篇模板': {
                '冲突开篇': {
                    'description': '以激烈冲突开场，立即抓住读者注意力',
                    'structure': [
                        '场景描写（紧张氛围）',
                        '冲突爆发（对话/动作）',
                        '主角登场（展现态度）',
                        '悬念埋设（引出后续）'
                    ],
                    'example': '“你凭什么抢我的名额？”林悦拍案而起，整个教室瞬间安静。她盯着眼前趾高气昂的女生，嘴角勾起一抹冷笑。这个看似柔弱的女孩，没人知道她已不是原来的她...'
                },
                '穿越开篇': {
                    'description': '主角穿越到异世界，身份反差制造爽点',
                    'structure': [
                        '现代场景（铺垫）',
                        '穿越过程（简略）',
                        '异世界登场（身份揭示）',
                        '反差展现（震惊他人）'
                    ],
                    'example': '苏墨醒来时，发现自己躺在雕花大床上，身侧站着七八个丫鬟。“小姐醒了！”丫鬟们惊喜呼喊。她茫然照镜，镜中竟是绝世容颜。等等，这不是她昨晚看的小说里那个被退婚的炮灰女配吗？'
                },
                '重生开篇': {
                    'description': '主角重生回到过去，利用先知优势',
                    'structure': [
                        '前世悲剧（简短回忆）',
                        '重生醒来（时间地点）',
                        '发现机会（先知优势）',
                        '决心改变（立目标）'
                    ],
                    'example': '顾言再次睁开眼，竟然回到了十年前。看着镜子里青涩的自己，他握紧拳头。上一世他被渣男骗得倾家荡产，这一世，他要让那些人付出代价！'
                },
                '系统开篇': {
                    'description': '主角获得系统，开启逆袭之路',
                    'structure': [
                        '困境描写（主角低谷）',
                        '系统激活（金手指）',
                        '新手礼包（初始能力）',
                        '首次任务（开始改变）'
                    ],
                    'example': '“叮！神豪系统已激活！”叶辰看着眼前的虚拟面板，以为自己眼花了。作为月薪三千的社畜，他从未想过这种好事会降临。“恭喜宿主获得新手礼包：现金 100 万！”'
                },
                '退婚开篇': {
                    'description': '经典退婚流，制造屈辱感和期待感',
                    'structure': [
                        '退婚场景（公开羞辱）',
                        '主角反应（隐忍/愤怒）',
                        '立下誓言（三年之约）',
                        '金手指觉醒（希望）'
                    ],
                    'example': '“萧炎，你我婚约就此作废！”纳兰嫣然高傲地站在萧家大厅中央。萧炎紧握拳头，指甲嵌入掌心：“好！三年后，我自会上云岚宗讨回公道！”'
                }
            },
            '爽点模板': {
                '打脸虐渣': {
                    'description': '主角被轻视后展现实力，狠狠打脸',
                    'structure': [
                        '被轻视/嘲讽（铺垫）',
                        '主角隐忍（不解释）',
                        '关键时刻（展现能力）',
                        '众人震惊（爽点爆发）',
                        '反派吃瘪（收尾）'
                    ],
                    'key_points': [
                        '铺垫要足，让读者憋屈',
                        '打脸要狠，让读者爽快',
                        '围观群众反应要夸张'
                    ]
                },
                '扮猪吃虎': {
                    'description': '主角隐藏实力，关键时刻一鸣惊人',
                    'structure': [
                        '伪装弱小（降低期待）',
                        '遭遇挑衅（制造冲突）',
                        '被迫出手（无奈之举）',
                        '实力爆发（震惊全场）'
                    ],
                    'key_points': [
                        '伪装要自然，不能太假',
                        '爆发要突然，反差要大'
                    ]
                },
                '身份揭露': {
                    'description': '主角隐藏身份被揭穿，众人震惊',
                    'structure': [
                        '身份隐藏（日常状态）',
                        '危机出现（需要身份）',
                        '身份揭露（高潮）',
                        '众人反应（爽点）'
                    ],
                    'key_points': [
                        '身份要足够震撼',
                        '揭露时机要巧妙'
                    ]
                },
                '收获成长': {
                    'description': '主角获得机缘，实力/地位提升',
                    'structure': [
                        '进入秘境/获得机会',
                        '经历考验/战斗',
                        '获得宝物/传承',
                        '实力突破/地位提升'
                    ],
                    'key_points': [
                        '收获要配得上付出',
                        '成长要让读者期待后续'
                    ]
                }
            },
            '对话模板': {
                '冲突对话': {
                    'description': '两人针锋相对，火药味十足',
                    'pattern': [
                        'A: 挑衅/质疑',
                        'B: 反击/不屑',
                        'A: 升级冲突',
                        'B: 终极回应'
                    ],
                    'example': 'A: “就凭你？也配挑战我？”\nB: “配不配，打过才知道。”\nA: “找死！”\nB: “谁死还不一定。”'
                },
                '暧昧对话': {
                    'description': '男女主之间暧昧互动',
                    'pattern': [
                        '男主：调戏/靠近',
                        '女主：害羞/嘴硬',
                        '男主：进一步',
                        '女主：心动'
                    ],
                    'example': '“你靠这么近干嘛？”她脸红。\n“看你脸上有没有花。”他笑。\n“无聊！”她扭头，心跳却漏了一拍。'
                },
                '装逼对话': {
                    'description': '主角云淡风轻地装逼',
                    'pattern': [
                        '配角：震惊/询问',
                        '主角：淡然回应',
                        '配角：更震惊',
                        '主角：深藏功与名'
                    ],
                    'example': '“你...你怎么会这么强？”\n“还行吧。”\n“这还是人吗？”\n“只是个普通人。”'
                }
            },
            '描写素材': {
                '外貌描写': {
                    '女主': [
                        '眉如远山含黛，眼似秋水横波',
                        '肤若凝脂，唇若点朱',
                        '一袭白衣胜雪，气质出尘',
                        '明眸皓齿，顾盼生辉'
                    ],
                    '男主': [
                        '剑眉星目，鼻梁高挺',
                        '一身黑衣，气质冷峻',
                        '眸光深邃，仿佛藏着星辰大海',
                        '嘴角微扬，带着几分邪魅'
                    ]
                },
                '动作描写': {
                    '战斗': [
                        '身形如电，转瞬即至',
                        '一拳轰出，空气炸裂',
                        '剑气纵横，所过之处寸草不生',
                        '身影闪烁，如鬼魅般飘忽'
                    ],
                    '日常': [
                        '轻抚下巴，若有所思',
                        '双手抱胸，一脸玩味',
                        '眉头微皱，面露不悦',
                        '嘴角上扬，露出神秘笑容'
                    ]
                },
                '心理描写': {
                    '震惊': [
                        '心中掀起惊涛骇浪',
                        '大脑一片空白',
                        '怀疑自己是不是在做梦',
                        '世界观都被颠覆了'
                    ],
                    '愤怒': [
                        '怒火中烧，几欲爆发',
                        '拳头紧握，指节发白',
                        '眼中杀意闪烁',
                        '牙齿咬得咯咯作响'
                    ],
                    '喜悦': [
                        '心中乐开了花',
                        '嘴角不自觉地上扬',
                        '整个人都轻飘飘的',
                        '仿佛拥有了全世界'
                    ]
                },
                '环境描写': {
                    '紧张氛围': [
                        '空气仿佛凝固，落针可闻',
                        '乌云压顶，山雨欲来',
                        '狂风呼啸，树叶沙沙作响',
                        '四周寂静得可怕，只能听见心跳声'
                    ],
                    '浪漫氛围': [
                        '月光如水，洒在两人身上',
                        '微风轻拂，花香四溢',
                        '星光点点，夜色温柔',
                        '湖面波光粼粼，倒映着两人的身影'
                    ]
                }
            }
        }
        
        # 尝试从文件加载自定义模板
        if os.path.exists(self.templates_file):
            try:
                with open(self.templates_file, 'r', encoding='utf-8') as f:
                    custom_templates = json.load(f)
                
                # 合并自定义模板
                for category, templates in custom_templates.items():
                    if category not in self.templates:
                        self.templates[category] = {}
                    self.templates[category].update(templates)
                
                logger.info("模板库已加载，共 %d 个分类" % len(self.templates))
            except Exception as e:
                logger.log_exception(e, "加载模板库")
    
    def _save_templates(self):
        """保存模板（仅保存自定义部分）"""
        try:
            with open(self.templates_file, 'w', encoding='utf-8') as f:
                json.dump(self.templates, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.log_exception(e, "保存模板库")
    
    def get_template(self, category, template_name=None):
        """获取模板"""
        if category not in self.templates:
            return {'error': '分类不存在'}
        
        if template_name:
            if template_name not in self.templates[category]:
                return {'error': '模板不存在'}
            return self.templates[category][template_name]
        
        # 返回整个分类
        return self.templates[category]
    
    def get_random_template(self, category):
        """随机获取一个模板"""
        if category not in self.templates or not self.templates[category]:
            return {'error': '分类不存在或为空'}
        
        template_name = random.choice(list(self.templates[category].keys()))
        template = self.templates[category][template_name]
        
        return {
            'name': template_name,
            'content': template
        }
    
    def add_custom_template(self, category, template_name, template_data):
        """添加自定义模板"""
        if category not in self.templates:
            self.templates[category] = {}
        
        self.templates[category][template_name] = template_data
        self._save_templates()
        
        logger.info("已添加自定义模板：%s/%s" % (category, template_name))
    
    def remove_template(self, category, template_name):
        """删除模板（仅支持自定义）"""
        if category in self.templates and template_name in self.templates[category]:
            del self.templates[category][template_name]
            self._save_templates()
            logger.info("已删除模板：%s/%s" % (category, template_name))
    
    def search_templates(self, keyword):
        """搜索模板"""
        results = []
        
        for category, templates in self.templates.items():
            for name, content in templates.items():
                # 搜索名称和描述
                if keyword in name or keyword in str(content.get('description', '')):
                    results.append({
                        'category': category,
                        'name': name,
                        'content': content
                    })
        
        return results
    
    def get_all_categories(self):
        """获取所有分类"""
        return list(self.templates.keys())
    
    def export_template(self, category, template_name, format='text'):
        """导出模板"""
        template = self.get_template(category, template_name)
        
        if 'error' in template:
            return template['error']
        
        if format == 'text':
            output = []
            output.append("=" * 60)
            output.append("%s - %s" % (category, template_name))
            output.append("=" * 60)
            
            if 'description' in template:
                output.append("\n【说明】%s" % template['description'])
            
            if 'structure' in template:
                output.append("\n【结构】")
                for i, item in enumerate(template['structure'], 1):
                    output.append("  %d. %s" % (i, item))
            
            if 'example' in template:
                output.append("\n【示例】")
                output.append(template['example'])
            
            if 'key_points' in template:
                output.append("\n【要点】")
                for point in template['key_points']:
                    output.append("  • %s" % point)
            
            output.append("\n" + "=" * 60)
            
            return "\n".join(output)
        
        elif format == 'json':
            return json.dumps(template, ensure_ascii=False, indent=2)


# 全局模板库实例
template_library = TemplateLibrary()


def get_template_library():
    """获取模板库实例"""
    return template_library


# === DeepSeek V4 Optimization Templates ===

## Shuangwen Core Formula

### Male Lead Formula
- Status Contrast + Fake Weakness + Face Slapping + Growth

### Female Lead Formula
- Rebirth/Transfer + Info Advantage + Antagonist Revenge + Career Love Success

## Classic Plot Patterns

### 1. Underdog Type
Start (Low Point) -> Develop (Opportunity) -> Turn (Crisis) -> End (Victory)

### 2. Sweet Romance Type
Meet -> Flirt -> Misunderstanding -> Happy Ending

### 3. Revenge Type
Harmed -> Rebirth -> Revenge -> Success


# === DeepSeek V4 Optimization Templates ===

## Shuangwen Core Formula

### Male Lead Formula
- Status Contrast + Fake Weakness + Face Slapping + Growth

### Female Lead Formula
- Rebirth/Transfer + Info Advantage + Antagonist Revenge + Career Love Success

## Classic Plot Patterns

### 1. Underdog Type
Start (Low Point) -> Develop (Opportunity) -> Turn (Crisis) -> End (Victory)

### 2. Sweet Romance Type
Meet -> Flirt -> Misunderstanding -> Happy Ending

### 3. Revenge Type
Harmed -> Rebirth -> Revenge -> Success


# === DeepSeek V4 Optimization Templates ===

## Shuangwen Core Formula

### Male Lead Formula
- Status Contrast + Fake Weakness + Face Slapping + Growth

### Female Lead Formula
- Rebirth/Transfer + Info Advantage + Antagonist Revenge + Career Love Success

## Classic Plot Patterns

### 1. Underdog Type
Start (Low Point) -> Develop (Opportunity) -> Turn (Crisis) -> End (Victory)

### 2. Sweet Romance Type
Meet -> Flirt -> Misunderstanding -> Happy Ending

### 3. Revenge Type
Harmed -> Rebirth -> Revenge -> Success


# === DeepSeek V4 Optimization Templates ===

## Shuangwen Core Formula

### Male Lead Formula
- Status Contrast + Fake Weakness + Face Slapping + Growth

### Female Lead Formula
- Rebirth/Transfer + Info Advantage + Antagonist Revenge + Career Love Success

## Classic Plot Patterns

### 1. Underdog Type
Start (Low Point) -> Develop (Opportunity) -> Turn (Crisis) -> End (Victory)

### 2. Sweet Romance Type
Meet -> Flirt -> Misunderstanding -> Happy Ending

### 3. Revenge Type
Harmed -> Rebirth -> Revenge -> Success
