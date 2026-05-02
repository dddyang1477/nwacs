#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS V8.0 内容丰富化系统
通过DeepSeek联网学习，为V8系统填充实际可用的内容
"""

import sys
import json
import time
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "sk-f3246fbd1eef446e9a11d78efefd9bba"
BASE_URL = "https://api.deepseek.com"

def call_deepseek(prompt, system_prompt=None, temperature=0.7):
    """调用DeepSeek API"""
    import requests

    url = f"{BASE_URL}/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    data = {
        "model": "deepseek-chat",
        "messages": messages,
        "temperature": temperature,
        "max_tokens": 8000
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=120)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"   ❌ API调用失败: {e}")
        return None

def enrich_creative_engine():
    """丰富创作引擎的内置知识"""
    print("\n" + "="*60)
    print("📚 丰富创作引擎内置知识")
    print("="*60)

    prompt = """请为AI小说创作系统生成丰富的内置知识库，包括：

1. **玄幻修仙设定库**（JSON格式）
```json
{
  "境界体系": [
    {"name": "炼气期", "levels": ["初期", "中期", "后期", "圆满"], "description": "修士入门阶段"},
    {"name": "筑基期", "levels": ["初期", "中期", "后期", "圆满"], "description": "奠定修炼根基"},
    {"name": "金丹期", "levels": ["初期", "中期", "后期", "圆满"], "description": "凝结金丹"},
    {"name": "元婴期", "levels": ["初期", "中期", "后期", "圆满"], "description": "元婴出窍"},
    {"name": "化神期", "levels": ["初期", "中期", "后期", "圆满"], "description": "化神蜕变"},
    {"name": "渡劫期", "levels": ["初期", "中期", "后期", "圆满"], "description": "渡天劫"},
    {"name": "大乘期", "levels": ["初期", "中期", "后期", "圆满"], "description": "大乘境界"},
    {"name": "真仙境", "levels": ["初期", "中期", "后期", "圆满"], "description": "成仙"}
  ],
  "功法分类": [
    {"type": "炼体功法", "examples": ["九转玄功", "神象镇狱功", "不灭金身", "龙象般若功", "金刚不坏体"]},
    {"type": "炼气功法", "examples": ["九天真经", "太上诀", "天皇经", "苍穹诀", "万道归元功"]},
    {"type": "剑法", "examples": ["天剑诀", "万剑归宗", "诛仙剑诀", "九霄剑典", "太极剑意"]},
    {"type": "刀法", "examples": ["斩天刀法", "绝情刀", "修罗刀", "霸刀斩"]},
    {"type": "身法", "examples": ["凌波微步", "缩地成寸", "咫尺天涯", "虚空漫步"]}
  ],
  "法宝等级": ["法器", "灵器", "宝器", "道器", "后天灵宝", "先天灵宝", "混沌至宝", "大道圣器"],
  "材料宝库": ["九天玄铁", "万年玄冰", "凤血石", "龙鳞", "朱果", "七叶灵芝", "天地灵液"],
  "灵药大全": ["九转还魂草", "天元丹", "悟道茶", "筑基丹", "结金丹", "化神丹", "渡劫丹"],
  "妖兽图鉴": [
    {"name": "上古凶兽", "examples": ["饕餮", "穷奇", "梼杌", "混沌"]},
    {"name": "神兽", "examples": ["青龙", "白虎", "朱雀", "玄武", "麒麟", "凤凰"]},
    {"name": "仙兽", "examples": ["九尾狐", "天马", "独角兽", "白泽"]},
    {"name": "灵兽", "examples": ["紫电貂", "烈火狮", "玄冰虎", "金翅鹏"]}
  ]
}
```

2. **都市异能设定库**
```json
{
  "异能分类": [
    {"type": "元素系", "subtypes": [
      {"name": "火", "skills": ["火焰操控", "烈火掌", "炎爆术"]},
      {"name": "水", "skills": ["水流操控", "水盾术", "冰封术"]},
      {"name": "雷", "skills": ["雷电操控", "雷罚", "闪电链"]},
      {"name": "风", "skills": ["风力操控", "风刃", "风暴之翼"]},
      {"name": "土", "skills": ["土石操控", "地裂术", "岩盾"]},
      {"name": "冰", "skills": ["冰雪操控", "绝对零度", "冰封千里"]}
    ]},
    {"type": "强化系", "subtypes": [
      {"name": "身体强化", "skills": ["铜墙铁壁", "金刚之躯", "再生能力"]},
      {"name": "感官强化", "skills": ["千里眼", "顺风耳", "感知强化"]},
      {"name": "再生强化", "skills": ["极速再生", "不死之身", "细胞修复"]}
    ]},
    {"type": "特殊系", "subtypes": [
      {"name": "空间", "skills": ["瞬移", "空间折叠", "空间裂缝"]},
      {"name": "时间", "skills": ["时间暂停", "时间倒流", "时间加速"]},
      {"name": "念力", "skills": ["念力控物", "精神攻击", "心灵感应"]}
    ]}
  ],
  "组织设定": [
    {"name": "龙组", "description": "国家神秘组织", "level": "最高"},
    {"name": "异调局", "description": "异能者管理部门", "level": "高"},
    {"name": "古武协会", "description": "古武修炼者联盟", "level": "高"},
    {"name": "暗影殿", "description": "地下杀手组织", "level": "危险"},
    {"name": "佣兵联盟", "description": "佣兵组织", "level": "中"}
  ],
  "都市势力": [
    {"type": "商界巨头", "examples": ["四大家族", "十大财阀"]},
    {"type": "地下王者", "examples": ["地下皇帝", "黑道教父"]},
    {"type": "医道世家", "examples": ["华家", "叶家"]}
  ]
}
```

3. **女频言情设定库**
```json
{
  "男主类型": [
    {"type": "霸道总裁", "traits": ["冷傲", "霸道", "深情", "能力超强"], "examples": ["陆景琛", "顾霆深", "厉爵铭", "傅司寒"]},
    {"type": "温柔竹马", "traits": ["温柔", "体贴", "青梅竹马"], "examples": ["江辰", "陆子轩", "顾恒"]},
    {"type": "禁欲系", "traits": ["高冷", "禁欲", "深情"], "examples": ["沈知意", "傅司寒", "陆衍"]},
    {"type": "阳光奶狗", "traits": ["阳光", "开朗", "撒娇"], "examples": ["许燃", "江言"]},
    {"type": "腹黑", "traits": ["腹黑", "占有欲强", "宠溺"], "examples": ["霍司爵", "厉爵城"]}
  ],
  "女主类型": [
    {"type": "软萌甜", "traits": ["可爱", "软糯", "善良"], "examples": ["苏软软", "白小阮"]},
    {"type": "独立飒", "traits": ["独立", "坚强", "有能力"], "examples": ["姜鱼", "秦野"]},
    {"type": "病娇", "traits": ["病娇", "执念", "深情"], "examples": ["顾烟", "沈萋萋"]},
    {"type": "清冷", "traits": ["清冷", "疏离", "内心柔软"], "examples": ["云七七", "苏念"]}
  ],
  "甜宠剧情": ["误会重重", "破镜重圆", "先婚后爱", "暗恋成真", "失忆梗", "契约恋人", "错认", "带球跑"],
  "虐恋剧情": ["带球跑", "车祸失忆", "癌症误诊", "家族仇恨", "替身文学", "相爱相杀", "追妻火葬场"]
}
```

请生成完整的、可直接使用的JSON格式数据。"""

    system_prompt = "你是一位专业的网文设定师，擅长创作各种类型小说的完整设定体系。"
    result = call_deepseek(prompt, system_prompt, temperature=0.7)

    if result:
        output_file = "core/v8/engine/builtin_knowledge.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"   ✅ 创作引擎内置知识已保存")
        return True
    return False

def enrich_writing_templates():
    """丰富写作模板库"""
    print("\n" + "="*60)
    print("📝 丰富写作模板库")
    print("="*60)

    prompt = """请为AI小说创作系统生成丰富的写作模板，包括：

1. **黄金开篇模板**（JSON格式，10个以上）
```json
{
  "opening_templates": [
    {
      "template_id": "001",
      "name": "冲突前置法",
      "structure": "危机事件 → 主角处境 → 核心冲突 → 悬念钩子",
      "example": "【宗门大比前夜】\\n\\n\"三天后就是宗门大比，可我的修为还停留在炼气三层...\"\\n林动握紧拳头，指甲深深陷入掌心。\\n堂兄林琅天得意的声音从门外传来：\"废物，识相的就自己退出大比！\"",
      "applicable_genres": ["玄幻", "都市", "武侠"],
      "keywords": ["困境", "压迫", "反击"]
    },
    {
      "template_id": "002",
      "name": "身份反差法",
      "structure": "平凡身份 → 隐藏实力 → 遭遇展示 → 震惊全场",
      "example": "【都市宴会】\\n\\n顾兮兮挽着闺蜜的手走进宴会厅，却被拦在门口：\"不好意思，我们这是VIP宴会。\"\\n正当她尴尬时，一辆限量版跑车停在大门口，一个身影走下来，所有人倒吸一口凉气...",
      "applicable_genres": ["都市", "言情"],
      "keywords": ["身份", "反差", "震惊"]
    }
  ]
}
```

2. **章末钩子模板**（JSON格式，10个以上）
```json
{
  "chapter_hooks": [
    {
      "type": "危机悬念型",
      "example": "就在他以为逃出生天时，身后突然传来一道阴冷的笑声：\"想走？\"",
      "keywords": ["危险", "转折", "悬念"]
    },
    {
      "type": "身份揭秘型",
      "example": "她颤抖着手打开那封信，看完后整个人如坠冰窟——原来他竟是...",
      "keywords": ["揭秘", "震惊", "反转"]
    },
    {
      "type": "情感冲突型",
      "example": "\"你说什么？\"她的声音陡然提高，\"你再说一遍！\"",
      "keywords": ["情感", "冲突", "爆发"]
    }
  ]
}
```

请生成完整的JSON格式数据。"""

    system_prompt = "你是一位专业的小说写作导师，擅长总结各种写作模板。"
    result = call_deepseek(prompt, system_prompt, temperature=0.7)

    if result:
        output_file = "core/v8/engine/writing_templates.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"   ✅ 写作模板库已保存")
        return True
    return False

def enrich_character_profiles():
    """丰富角色画像库"""
    print("\n" + "="*60)
    print("👤 丰富角色画像库")
    print("="*60)

    prompt = """请为AI小说创作系统生成丰富的角色画像库，包括：

1. **主角模板**（JSON格式，每个类型5个以上）
```json
{
  "protagonist_templates": [
    {
      "type": "废柴逆袭型",
      "name_pattern": {
        "surname": ["林", "萧", "叶", "秦", "楚", "苏", "顾"],
        "given_name": ["动", "炎", "尘", "风", "寒", "辰", "轩"]
      },
      "personality_arc": {
        "early": "懦弱、自卑、被欺辱",
        "middle": "获得机缘、艰苦奋斗",
        "late": "坚毅、果敢、重情重义、登临绝顶"
      },
      "signature_traits": ["隐藏实力", "扮猪吃虎", "逆境爆发", "杀伐果断"],
      "example_dialogue": {
        "low": "对不起，我这就离开...",
        "high": "今日之辱，来日必十倍奉还！"
      },
      "growth_stages": [
        "被测出废物体质",
        "被未婚妻退婚羞辱",
        "偶得上古传承",
        "开始修炼展现天赋",
        "家族大比一鸣惊人"
      ]
    },
    {
      "type": "都市兵王型",
      "name_pattern": {
        "surname": ["叶", "陈", "秦", "萧", "顾"],
        "given_name": ["城", "冥", "枫", "寒", "霄"]
      },
      "personality_arc": {
        "early": "冷酷、寡言、杀伐",
        "middle": "回归都市、隐藏身份",
        "late": "守护爱人、承担责任"
      },
      "signature_traits": ["铁血", "忠诚", "霸气", "护短"],
      "example_dialogue": {
        "cold": "挡我路的人，只有死。",
        "warm": "敢动我的女人，我会让你后悔来到这个世界。"
      }
    }
  ]
}
```

请生成完整的JSON格式数据，包含至少5种不同类型的主角模板。"""

    system_prompt = "你是一位专业的角色设计师，擅长创作各种类型的角色画像。"
    result = call_deepseek(prompt, system_prompt, temperature=0.7)

    if result:
        output_file = "core/v8/engine/character_profiles.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"   ✅ 角色画像库已保存")
        return True
    return False

def enrich_world_settings():
    """丰富世界观设定库"""
    print("\n" + "="*60)
    print("🌍 丰富世界观设定库")
    print("="*60)

    prompt = """请为AI小说创作系统生成丰富的世界观设定库，包括：

1. **完整世界观模板**（JSON格式，3个以上）
```json
{
  "world_settings": [
    {
      "world_id": "xianxia_001",
      "world_name": "九霄仙域",
      "geography": {
        "continents": ["中州", "南域", "北荒", "东洲", "西域"],
        "famous_mountains": ["青云峰", "天剑山", "万兽山脉", "幽冥深渊", "蓬莱仙岛"],
        "seas": ["东海龙宫", "西海归墟", "南海秘境", "北海冰原"]
      },
      "powers": {
        "supreme_forces": [
          {"name": "天机阁", "specialty": "情报与占卜"},
          {"name": "万佛寺", "specialty": "佛法与炼体"},
          {"name": "剑冢", "specialty": "剑道传承"},
          {"name": "丹殿", "specialty": "炼丹之术"},
          {"name": "器宗", "specialty": "炼器之道"}
        ],
        "major_families": ["林家", "萧家", "叶家", "秦家", "楚家"]
      },
      "rules": {
        "cultivation_system": "炼气 → 筑基 → 金丹 → 元婴 → 化神 → 渡劫 → 大乘 → 真仙",
        "spiritual_energy": "灵气浓度决定修炼速度，中州灵气最浓",
        "formation_system": "一级至九级阵法，威力递增"
      },
      "cultures": {
        "sects": "以宗门为尊，等级森严",
        "events": "每百年举办一次天骄大会",
        "taboos": "渡劫期不可轻易出手，否则天道反噬"
      },
      "unique_locations": [
        {"name": "禁地·坠仙崖", "description": "传闻有真仙陨落于此，禁制重重"},
        {"name": "秘境的规则", "description": "上古遗迹，蕴含大机缘"}
      ]
    },
    {
      "world_id": "urban_001",
      "world_name": "现代都市",
      "modern_powers": {
        "official": [
          {"name": "龙组", "description": "国家神秘组织"},
          {"name": "异调局", "description": "异能者管理部门"},
          {"name": "古武协会", "description": "古武修炼者联盟"}
        ],
        "underground": [
          {"name": "暗网", "description": "地下信息交易"},
          {"name": "黑市", "description": "非法交易场所"}
        ]
      },
      "social_structure": {
        "upper_class": "隐世家族掌权者",
        "middle_class": "古武世家、异能者",
        "lower_class": "普通人"
      },
      "special_places": {
        "training_grounds": ["昆仑秘境", "神农架禁区"],
        "underground_arenas": ["黑拳场", "异能者角斗场"]
      }
    }
  ]
}
```

请生成完整的JSON格式数据，包含至少3个完整的玄幻世界观和2个都市世界观。"""

    system_prompt = "你是一位专业的世界观构建师，擅长创作完整的小说世界观设定。"
    result = call_deepseek(prompt, system_prompt, temperature=0.7)

    if result:
        output_file = "core/v8/engine/world_settings.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"   ✅ 世界观设定库已保存")
        return True
    return False

def enrich_plot_outlines():
    """丰富剧情大纲库"""
    print("\n" + "="*60)
    print("📖 丰富剧情大纲库")
    print("="*60)

    prompt = """请为AI小说创作系统生成丰富的剧情大纲库，包括：

1. **完整小说大纲模板**（JSON格式，3个以上）
```json
{
  "plot_outlines": [
    {
      "outline_id": "xuanhuan_001",
      "genre": "玄幻",
      "theme": "废柴少年逆袭成仙帝",
      "target_length": "300万字+",
      "three_act_structure": {
        "act1_setup": {
          "chapters": "第1-100章",
          "main_events": [
            "被测出废物体质",
            "被未婚妻退婚当众羞辱",
            "偶得上古传承/老爷爷/系统",
            "开始修炼展现天赋",
            "家族大比一鸣惊人"
          ],
          "ending_hook": "主角得罪了大门派少主"
        },
        "act2_confrontation": {
          "chapters": "第101-800章",
          "main_events": [
            "加入宗门从外门弟子做起",
            "结识红颜知己1号",
            "宗门大比夺冠震惊全宗",
            "发现灭门仇人",
            "历练大陆获得机缘",
            "结识红颜知己2号",
            "建立自己的势力",
            "与大门派正式开战",
            "红颜知己被害",
            "主角暴走强势复仇"
          ],
          "midpoint_climax": "与大门派正式开战",
          "ending_hook": "发现幕后还有更大的黑手"
        },
        "act3_resolution": {
          "chapters": "第801-1000章+",
          "main_events": [
            "揭露幕后黑手身份",
            "与仙界势力对抗",
            "最终决战",
            "成就仙帝之位"
          ]
        }
      },
      "boilerplate_chapters": [
        {"chapter": 30, "event": "金手指首次显威"},
        {"chapter": 50, "event": "打脸退婚未婚妻"},
        {"chapter": 100, "event": "宗门拜师"}
      ]
    },
    {
      "outline_id": "urban_001",
      "genre": "都市",
      "theme": "兵王回归都市纵横花都",
      "target_length": "200万字+",
      "three_act_structure": {
        "act1": {
          "chapters": "第1-100章",
          "main_events": [
            "世界最强兵王回归",
            "与绝美总裁的第一次相遇",
            "成为贴身保镖",
            "暗榜高手来袭被震慑",
            "宣示主权震惊全场"
          ]
        },
        "act2": {
          "chapters": "第101-500章",
          "main_events": [
            "商界大佬挑衅",
            "地下势力觊觎",
            "异能者出现",
            "各国强者来袭",
            "守护城市安全",
            "发现惊天阴谋",
            "与各国兵王对战",
            "最终决战"
          ]
        }
      }
    }
  ]
}
```

请生成完整的JSON格式数据，包含至少3个玄幻大纲和2个都市大纲。"""

    system_prompt = "你是一位专业的大纲设计师，擅长创作各种类型小说的完整大纲。"
    result = call_deepseek(prompt, system_prompt, temperature=0.7)

    if result:
        output_file = "core/v8/engine/plot_outlines.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"   ✅ 剧情大纲库已保存")
        return True
    return False

def enrich_writing_phrases():
    """丰富写作词库"""
    print("\n" + "="*60)
    print("✨ 丰富写作词库")
    print("="*60)

    prompt = """请为AI小说创作系统生成丰富的写作词库，包括：

1. **动作描写词库**（JSON格式）
```json
{
  "combat_actions": {
    "attack": ["挥拳", "出剑", "劈砍", "刺杀", "突刺", "横扫", "下劈", "上挑", "虚晃", "连击", "重击", "速攻", "暗算", "偷袭"],
    "defense": ["格挡", "闪避", "后撤", "侧身", "下蹲", "招架", "卸力", "偏转", "闪躲", "规避"],
    "movement": ["冲刺", "飞跃", "瞬移", "滑步", "横移", "腾空", "落地", "翻滚", "跃起", "突进"]
  },
  "emotion_actions": {
    "happy": ["眉开眼笑", "喜上眉梢", "笑逐颜开", "欣喜若狂", "欢呼雀跃", "精神焕发", "神采奕奕"],
    "angry": ["怒目圆睁", "咬牙切齿", "握拳", "青筋暴起", "怒火中烧", "气急败坏", "勃然大怒"],
    "sad": ["黯然神伤", "泪流满面", "捶胸顿足", "抱头痛哭", "心如刀割", "泣不成声", "悲痛欲绝"],
    "scared": ["瑟瑟发抖", "脸色苍白", "冷汗直流", "双腿发软", "魂飞魄散", "惊恐万状", "面如土色"]
  }
}
```

2. **环境描写词库**
```json
{
  "ancient_architecture": {
    "palace": ["金碧辉煌", "雕梁画栋", "气势恢宏", "富丽堂皇", "宏伟壮观"],
    "temple": ["古朴庄严", "香烟缭绕", "钟声悠扬", "青灯古佛", "梵音阵阵"],
    "pavilion": ["飞檐翘角", "清雅别致", "临水而建", "曲径通幽", "小巧玲珑"]
  },
  "natural_landscape": {
    "mountain": ["巍峨耸立", "云雾缭绕", "层峦叠嶂", "奇峰罗列", "悬崖峭壁"],
    "water": ["波光粼粼", "清澈见底", "汹涌澎湃", "潺潺流水", "水平如镜"],
    "forest": ["古木参天", "遮天蔽日", "郁郁葱葱", "落叶纷飞", "茂密幽深"]
  }
}
```

3. **人物描写词库**
```json
{
  "male_beauty": {
    "general": ["俊朗", "英挺", "潇洒", "冷峻", "儒雅", "清秀", "阳刚"],
    "eyes": ["深邃", "锐利", "温柔", "邪魅", "清冷", "深邃", "明亮"],
    "features": ["剑眉星目", "面如冠玉", "轮廓分明", "器宇不凡", "棱角分明"]
  },
  "female_beauty": {
    "general": ["绝美", "清丽", "妩媚", "冷艳", "温婉", "清秀", "甜美"],
    "eyes": ["清澈", "灵动", "魅惑", "幽怨", "明媚", "水灵", "传神"],
    "features": ["倾国倾城", "闭月羞花", "沉鱼落雁", "冰肌玉骨", "明艳动人"]
  }
}
```

请生成完整的JSON格式数据，包含丰富的词汇。"""

    system_prompt = "你是一位专业的写作词汇分析师，擅长收集和整理各类写作词汇。"
    result = call_deepseek(prompt, system_prompt, temperature=0.7)

    if result:
        output_file = "core/v8/engine/writing_phrases.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"   ✅ 写作词库已保存")
        return True
    return False

def main():
    print("="*60)
    print("🎯 NWACS V8.0 内容丰富化系统")
    print("="*60)

    start_time = datetime.now()
    print(f"\n启动时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    tasks = [
        ("创作引擎内置知识", enrich_creative_engine),
        ("写作模板库", enrich_writing_templates),
        ("角色画像库", enrich_character_profiles),
        ("世界观设定库", enrich_world_settings),
        ("剧情大纲库", enrich_plot_outlines),
        ("写作词库", enrich_writing_phrases)
    ]

    completed = []
    failed = []

    for i, (task_name, task_func) in enumerate(tasks, 1):
        print(f"\n任务 {i}/{len(tasks)}: {task_name}")
        try:
            success = task_func()
            if success:
                completed.append(task_name)
                print(f"   ✅ 完成")
            else:
                failed.append(task_name)
                print(f"   ❌ 失败")
        except Exception as e:
            failed.append(task_name)
            print(f"   ❌ 异常: {e}")

        if i < len(tasks):
            time.sleep(3)

    end_time = datetime.now()

    print("\n" + "="*60)
    print("🎉 内容丰富化完成！")
    print("="*60)

    print(f"\n完成时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"总耗时: {(end_time - start_time).total_seconds() / 60:.1f}分钟")

    print(f"\n✅ 成功完成 ({len(completed)}):")
    for task in completed:
        print(f"   - {task}")

    if failed:
        print(f"\n❌ 失败 ({len(failed)}):")
        for task in failed:
            print(f"   - {task}")

    print("\n📁 生成的文件:")
    print("  1. core/v8/engine/builtin_knowledge.json - 内置设定知识")
    print("  2. core/v8/engine/writing_templates.json - 写作模板库")
    print("  3. core/v8/engine/character_profiles.json - 角色画像库")
    print("  4. core/v8/engine/world_settings.json - 世界观设定库")
    print("  5. core/v8/engine/plot_outlines.json - 剧情大纲库")
    print("  6. core/v8/engine/writing_phrases.json - 写作词库")

if __name__ == "__main__":
    main()
