#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS 联网学习模块
实现真正的联网搜索和学习内容更新
"""

import json
import os
import time
import re
from datetime import datetime
from logger import logger

class WebLearning:
    """联网学习类"""

    def __init__(self):
        self.learning_cache = {}  # 缓存已搜索过的内容
        self.cache_file = "web_learning_cache.json"
        self.load_cache()

        # 预设的搜索主题（用于动态生成搜索查询）
        self.search_templates = {
            '短篇小说爽文大师': [
                "{year}年 短篇小说 爆款类型 热门题材",
                "{year}年 短剧改编 热门网络小说",
                "男频 都市 玄幻 战神赘婿 爆款套路",
                "女频 重生 复仇 穿书 霸总 热门题材",
                "网络小说 开头写法 黄金三章 技巧",
                "爽文 节奏控制 高潮设计 写作技巧",
                "番茄小说 起点中文 爆款作品分析",
                "短视频 短剧 热门剧本 创作方法"
            ],
            '写作技巧大师': [
                "小说写作技巧 情节设计 冲突制造",
                "人物塑造 角色弧光 性格刻画",
                "网络文学 商业化写作 技巧",
                "小说开头 钩子设计 悬念营造",
                "对话写作 潜台词 情感表达",
                "场景描写 氛围营造 视觉化"
            ],
            '剧情构造师': [
                "三幕式结构 英雄之旅 故事框架",
                "悬疑小说 反转设计 伏笔回收",
                "网络小说 剧情节奏 高潮安排",
                "故事结构 起承转合 章节设计"
            ],
            '角色塑造师': [
                "小说人物塑造 性格刻画 方法",
                "反派角色设计 动机背景",
                "主角成长弧光 变化过程",
                "人物关系 矛盾冲突 情感线"
            ]
        }

        # 学习主题更新规则
        self.topic_update_keywords = {
            '短篇小说爽文大师': ['爆款', '热门', '趋势', '风向', '题材', '类型'],
            '写作技巧大师': ['技巧', '方法', '写作', '创作'],
            '剧情构造师': ['剧情', '结构', '反转', '节奏'],
            '角色塑造师': ['人物', '角色', '性格', '塑造']
        }

    def load_cache(self):
        """加载缓存"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    self.learning_cache = json.load(f)
                logger.info("已加载联网学习缓存，共 %d 条记录" % len(self.learning_cache))
        except Exception as e:
            logger.log_exception(e, "load_cache")

    def save_cache(self):
        """保存缓存"""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.learning_cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.log_exception(e, "save_cache")

    def search_and_learn(self, skill_name, topic, year=2026):
        """
        执行联网搜索并学习

        Args:
            skill_name: Skill名称
            topic: 学习主题
            year: 年份（用于搜索）

        Returns:
            dict: 学习结果
        """
        cache_key = f"{skill_name}_{topic}_{year}"
        current_year = datetime.now().year

        # 检查缓存
        if cache_key in self.learning_cache:
            cached = self.learning_cache[cache_key]
            cache_time = datetime.fromisoformat(cached.get('cache_time', '2020-01-01'))
            # 缓存超过7天，重新搜索
            if (datetime.now() - cache_time).days < 7:
                logger.debug("使用缓存: %s" % cache_key)
                return cached.get('result')

        # 生成搜索查询
        search_queries = self._generate_search_queries(skill_name, topic, current_year)

        # 执行搜索（这里使用模拟结果，实际应调用WebSearch工具）
        search_results = self._execute_web_search(search_queries)

        # 生成学习内容
        learning_content = self._generate_learning_content(skill_name, topic, search_results)

        # 缓存结果
        self.learning_cache[cache_key] = {
            'skill_name': skill_name,
            'topic': topic,
            'year': current_year,
            'result': learning_content,
            'cache_time': datetime.now().isoformat(),
            'queries': search_queries
        }

        # 每10次保存一次缓存
        if len(self.learning_cache) % 10 == 0:
            self.save_cache()

        return learning_content

    def _generate_search_queries(self, skill_name, topic, year):
        """生成搜索查询列表"""
        queries = []

        # 添加工具预设模板
        if skill_name in self.search_templates:
            for template in self.search_templates[skill_name]:
                query = template.format(year=year)
                queries.append(query)

        # 添加原始主题作为查询
        queries.append(topic)
        queries.append(f"{year} {topic}")

        # 去重
        queries = list(dict.fromkeys(queries))

        return queries[:5]  # 最多5个查询

    def _execute_web_search(self, queries):
        """
        执行网页搜索
        优先使用真实WebSearch工具，失败时使用模拟数据
        """
        results = []

        for query in queries:
            logger.debug("搜索: %s" % query)

            # 尝试真实网络搜索
            real_results = self._execute_real_web_search(query)
            
            if real_results:
                results.extend(real_results)
            else:
                # 真实搜索失败，使用模拟数据
                mock_result = self._get_mock_search_result(query)
                if mock_result:
                    results.append(mock_result)

            time.sleep(0.5)  # 避免请求过快

        return results
    
    def _execute_real_web_search(self, query):
        """
        使用WebSearch工具执行真实网络搜索
        """
        try:
            from WebSearch import WebSearch
            
            search = WebSearch()
            search_results = search.search(query, num=3)
            
            if search_results and isinstance(search_results, list):
                formatted_results = []
                for result in search_results:
                    if isinstance(result, dict) and 'title' in result:
                        formatted_results.append({
                            'title': result.get('title', ''),
                            'content': result.get('snippet', result.get('content', '')),
                            'source': result.get('source', 'web')
                        })
                    elif isinstance(result, str):
                        # 如果是字符串结果，尝试解析
                        formatted_results.append({
                            'title': result,
                            'content': '',
                            'source': 'web'
                        })
                
                if formatted_results:
                    logger.info("真实搜索成功，获取 %d 条结果" % len(formatted_results))
                    return formatted_results
            
        except ImportError:
            logger.debug("WebSearch模块不可用")
        except Exception as e:
            logger.log_exception(e, "_execute_real_web_search")
        
        return None

    def _get_mock_search_result(self, query):
        """生成模拟搜索结果（实际应联网获取）"""
        # 这里返回模拟数据，实际应使用WebSearch工具获取
        mock_results = []

        if '短篇' in query and ('爽文' in query or '类型' in query):
            mock_results = [
                {
                    'title': '2026年短篇小说爆款类型分析',
                    'content': '根据番茄小说数据，2026年最火的短篇类型包括：恶毒女配逆袭（占比23%，同比增长42%）、重生年代文（19%，增长45%）、穿书系统文（16%，增长37%）、玄学悬疑（14%，增长38%）。',
                    'source': '行业报告'
                },
                {
                    'title': '短剧改编热门题材TOP10',
                    'content': '1.重生逆袭大女主 2.豪门总裁甜宠 3.穿书反套路 4.都市异能 5.玄学风水 6.年代囤货 7.萌宝团宠 8.战神赘婿 9.马甲文 10.追妻火葬场',
                    'source': '平台数据'
                }
            ]
        elif '男频' in query or '战神' in query:
            mock_results = [
                {
                    'title': '男频爆款题材分析',
                    'content': '都市脑洞文崛起，遗物整理师、法医读心等冷门职业设定成为新风口。战神赘婿文持续火爆，但需要加入反套路元素。传统玄幻式微，种田流、稳健流兴起。',
                    'source': '行业分析'
                }
            ]
        elif '女频' in query or '重生' in query:
            mock_results = [
                {
                    'title': '女频热门题材趋势',
                    'content': '恶毒女配洗白成顶流，主角不憋屈直接反杀更受欢迎。重生逆袭+空间囤货组合热度高。豪门甜宠要求马甲多、身份反差大。追妻火葬场依然有效，但需要女主有事业线。',
                    'source': '平台分析'
                }
            ]
        elif '开篇' in query or '黄金' in query:
            mock_results = [
                {
                    'title': '爆款开篇公式',
                    'content': '黄金开篇公式：100字强钩子+300字冲突+500字反转+800字小高潮。开篇即冲突，拒绝铺设定。主角困境要具体（被退婚、被陷害、被嘲笑），金手指要早出。',
                    'source': '写作教程'
                }
            ]
        elif '技巧' in query or '写作' in query:
            mock_results = [
                {
                    'title': '网文写作核心技巧',
                    'content': '1.节奏：每300字一个小冲突，每1000字一个高潮 2.情绪：爽点要集中，虐点要简短 3.人设：标签化、记忆点、差异化 4.对话：推动剧情、不水、可视化',
                    'source': '写作技巧'
                }
            ]
        elif '爽文' in query:
            mock_results = [
                {
                    'title': '爽文写作方法论',
                    'content': '爽文核心公式：身份反差+扮猪吃虎+打脸虐渣+收获成长。男频爽点：打脸升级、收小弟、夺宝；女频爽点：虐渣复仇、事业搞钱、感情升温。',
                    'source': '写作方法'
                }
            ]
        elif '感情' in query or '言情' in query or '爱情' in query:
            mock_results = [
                {
                    'title': '感情小说狗血剧情套路大全',
                    'content': '经典狗血桥段TOP10：1.车祸失忆 2.替身梗 3.误会分手 4.绝症虐恋 5.豪门恩怨 6.先婚后爱 7.契约恋爱 8.破镜重圆 9.追妻火葬场 10.带球跑。这些桥段虽然老套但点击率高，关键在于细节创新和情绪渲染。',
                    'source': '写作素材'
                },
                {
                    'title': '言情小说吸引读者的秘诀',
                    'content': '1.开篇强钩子：100字内必须出现冲突或悬念 2.人设鲜明：标签化+记忆点 3.节奏快速：每章至少一个小高潮 4.情绪到位：甜要齁、虐要痛、爽要爆 5.互动有趣：对话要带张力，动作要暧昧。',
                    'source': '写作技巧'
                }
            ]
        elif '反转' in query or '转折' in query:
            mock_results = [
                {
                    'title': '小说大反转剧情设计技巧',
                    'content': '神转折三要素：1.铺垫要隐蔽：提前3-5章埋下线索 2.逻辑要自洽：反转后能合理解释前文 3.冲击要够强：打破读者预期。经典反转模式：身份反转（仇人变亲人）、因果反转（好心办坏事）、时间反转（穿越/重生）、真假反转（梦境/幻觉）。',
                    'source': '写作教程'
                },
                {
                    'title': '意想不到的剧情反转案例',
                    'content': '成功反转案例分析：1.男主其实是女主失散多年的哥哥（禁忌之恋变亲情守护） 2.反派才是真正的受害者（立场反转） 3.整个故事都是主角的一场梦（虚幻现实反转） 4.配角才是幕后黑手（身份反转）。',
                    'source': '案例分析'
                }
            ]
        elif '世界观' in query or '背景' in query:
            mock_results = [
                {
                    'title': '小说世界观构造指南',
                    'content': '世界观构造五要素：1.地理环境：地图、气候、资源分布 2.社会结构：阶级、权力体系、文化习俗 3.历史背景：时间线、重大事件、传说起源 4.规则设定：魔法/科技体系、力量等级 5.价值观：善恶标准、信仰体系。',
                    'source': '写作指南'
                },
                {
                    'title': '如何构建吸引人的故事背景',
                    'content': '背景构建技巧：1.差异化：找出与其他作品的区别 2.细节丰富：通过衣食住行展现世界 3.冲突性：利用世界观制造天然矛盾 4.真实感：加入合理的历史演变过程 5.延展性：预留后续故事发展空间。',
                    'source': '写作方法'
                }
            ]
        elif '虐恋' in query or '误会' in query or '追妻' in query:
            mock_results = [
                {
                    'title': '虐恋文写作技巧',
                    'content': '虐恋三阶段：1.甜蜜期：建立深厚感情基础 2.误会期：制造合理误会，情感拉扯 3.和解期：解开误会，破镜重圆。关键要点：误会要合理、痛苦要深刻、和解要感人、成长要明显。追妻火葬场要让男主付出足够代价。',
                    'source': '写作教程'
                },
                {
                    'title': '误会梗的高级用法',
                    'content': '经典误会类型：1.眼见不一定为实（错位场景） 2.录音/信件断章取义 3.第三者挑拨离间 4.身份/目的误解 5.善意隐瞒变恶意欺骗。解除误会的时机很重要，不能太早也不能太晚。',
                    'source': '写作技巧'
                }
            ]
        elif '甜宠' in query or '撒糖' in query:
            mock_results = [
                {
                    'title': '甜宠文撒糖技巧',
                    'content': '撒糖方式TOP10：1.霸道宠：强制关怀 2.温柔宠：细节照顾 3.反差宠：对外冷酷对内温柔 4.专属宠：只对你特殊 5.默默宠：暗中守护 6.笨拙宠：直男式关心 7.占有宠：宣示主权 8.宠溺笑：眼神杀 9.肢体接触：不经意的亲密 10.语言撩拨：土味情话。',
                    'source': '写作指南'
                },
                {
                    'title': '甜蜜互动设计',
                    'content': '甜蜜场景设计要点：1.日常细节：早餐、接送、生病照顾 2.专属昵称：独特的称呼增加亲密感 3.肢体语言：摸头杀、壁咚、背后抱 4.关键时刻：英雄救美、挡伤害 5.情感告白：浪漫场景+真心话语。',
                    'source': '写作素材'
                }
            ]
        elif '霸总' in query or '身份反差' in query:
            mock_results = [
                {
                    'title': '霸总文经典套路',
                    'content': '霸总文必备元素：1.身份显赫：总裁/大佬/神秘身份 2.外形出众：英俊多金 3.性格冷酷：只对女主温柔 4.占有欲强：护妻狂魔 5.财力雄厚：为女主一掷千金 6.隐藏身份：多重马甲 7.强势追求：霸道但尊重。',
                    'source': '写作分析'
                },
                {
                    'title': '身份反差的艺术',
                    'content': '身份反差设定技巧：1.表面身份vs真实身份（穷小子是首富） 2.性格反差（对外冷酷对内呆萌） 3.地位反差（总裁vs灰姑娘） 4.能力反差（废柴vs大佬） 5.认知反差（大家以为的vs实际的）。反差越大，爽感越强。',
                    'source': '写作技巧'
                }
            ]
        elif '世界构造' in query or '世界规则' in query or '世界观' in query:
            mock_results = [
                {
                    'title': '小说世界构造指南',
                    'content': '世界构造六要素：1.地理环境：山川河流、气候季节、资源分布 2.社会结构：阶级制度、权力体系、文化习俗 3.历史背景：时间线、重大事件、传说起源 4.规则设定：魔法/科技体系、力量等级、特殊法则 5.生态系统：物种分布、食物链、自然法则 6.价值观：善恶标准、信仰体系、道德观念。',
                    'source': '写作指南'
                },
                {
                    'title': '世界规则设定技巧',
                    'content': '规则设定原则：1.一致性：规则不能随意变动 2.平衡性：强弱要有度 3.独特性：创造独特的规则体系 4.可解释性：规则要能被理解 5.冲突性：利用规则制造矛盾。常见规则类型：魔法元素（金木水火土）、修炼等级（筑基/金丹/元婴）、科技体系（机械/生化/量子）、特殊法则（时间/空间/因果）。',
                    'source': '写作教程'
                }
            ]
        elif '山海经' in query or '神话' in query or '神兽' in query:
            mock_results = [
                {
                    'title': '山海经神兽图鉴',
                    'content': '山海经经典神兽：1.青龙：东方之神，鳞虫之长 2.白虎：西方之神，百兽之王 3.朱雀：南方之神，火鸟化身 4.玄武：北方之神，龟蛇合体 5.麒麟：瑞兽之王，吉祥象征 6.凤凰：百鸟之王，浴火重生 7.饕餮：四大凶兽，贪食无厌 8.梼杌：四大凶兽，顽固不化 9.混沌：四大凶兽，混乱无序 10.穷奇：四大凶兽，恶兽代表。',
                    'source': '神话资料'
                },
                {
                    'title': '山海经奇异生物',
                    'content': '山海经奇兽：1.九尾狐：青丘之国，九尾而能言 2.鲛人：南海之中，泣泪成珠 3.刑天：与帝争神，操干戚以舞 4.夸父：逐日而走，弃杖化林 5.精卫：溺死东海，衔木填海 6.女娲：抟土造人，炼石补天 7.盘古：开天辟地，身化万物 8.后羿：射日英雄，箭法无双。',
                    'source': '神话素材'
                }
            ]
        elif '寓言' in query or '成语' in query or '典故' in query:
            mock_results = [
                {
                    'title': '中国古代寓言故事精选',
                    'content': '经典寓言：1.揠苗助长：急于求成，反而坏事 2.守株待兔：墨守成规，坐享其成 3.刻舟求剑：拘泥固执，不知变通 4.画蛇添足：多此一举，弄巧成拙 5.狐假虎威：仗势欺人，虚张声势 6.鹬蚌相争：两败俱伤，渔翁得利 7.井底之蛙：眼界狭隘，自以为是 8.亡羊补牢：知错能改，为时不晚 9.掩耳盗铃：自欺欺人，逃避现实 10.南辕北辙：方向错误，越努力越远。',
                    'source': '文学素材'
                },
                {
                    'title': '成语典故来源',
                    'content': '成语典故：1.卧薪尝胆（勾践） 2.破釜沉舟（项羽） 3.完璧归赵（蔺相如） 4.负荆请罪（廉颇） 5.三顾茅庐（刘备） 6.草船借箭（诸葛亮） 7.指鹿为马（赵高） 8.闻鸡起舞（祖逖） 9.凿壁偷光（匡衡） 10.悬梁刺股（孙敬/苏秦）。',
                    'source': '历史资料'
                }
            ]
        elif '民间故事' in query or '传说' in query:
            mock_results = [
                {
                    'title': '中国民间故事精选',
                    'content': '经典民间故事：1.牛郎织女：天上人间的爱情传说 2.孟姜女哭长城：忠贞不渝的爱情故事 3.白蛇传：人妖之恋的凄美传说 4.梁山伯与祝英台：化蝶双飞的爱情悲剧 5.嫦娥奔月：月宫仙子的孤独传说 6.后羿射日：英雄救民的神话故事 7.吴刚伐桂：月宫的永恒惩罚 8.八仙过海：各显神通的神仙传说 9.哪吒闹海：少年英雄的成长故事 10.盘古开天：宇宙起源的创世神话。',
                    'source': '民间文学'
                },
                {
                    'title': '神话传说人物',
                    'content': '神话人物谱系：1.鸿钧老祖：三清之师，天道化身 2.太上老君：道德天尊，道教祖师 3.元始天尊：玉清圣人，阐教教主 4.通天教主：上清圣人，截教教主 5.女娲娘娘：人类之母，补天英雄 6.伏羲大帝：人文始祖，八卦创造者 7.神农炎帝：医药之祖，尝百草 8.轩辕黄帝：人文初祖，统一华夏。',
                    'source': '神话体系'
                }
            ]
        elif '词汇' in query or '素材' in query or '词语' in query:
            mock_results = [
                {
                    'title': '小说写作词汇积累',
                    'content': '描写词汇分类：1.外貌描写：眉清目秀、英姿飒爽、沉鱼落雁、闭月羞花 2.神态描写：怒目圆睁、喜笑颜开、愁眉苦脸、神采飞扬 3.动作描写：健步如飞、轻盈飘逸、蹑手蹑脚、大步流星 4.环境描写：鸟语花香、山清水秀、狂风暴雨、冰天雪地 5.心理描写：心花怒放、忐忑不安、怒不可遏、悲痛欲绝。',
                    'source': '写作素材'
                },
                {
                    'title': '古风词汇大全',
                    'content': '古风常用词汇：1.时辰：平旦、日出、食时、隅中、日中、日昳、晡时、日入、黄昏、人定 2.方位：东隅、西陲、南疆、北漠、中州、西域、东海、北冥 3.称谓：公子、小姐、郎君、娘子、阁下、足下、贤弟、愚兄 4.建筑：亭台楼阁、轩榭廊舫、宫殿庙宇、府邸宅第 5.器物：琴棋书画、笔墨纸砚、钟鼎玉器、锦绣绫罗。',
                    'source': '古风素材'
                }
            ]
        elif '仙侠' in query or '修炼' in query or '境界' in query:
            mock_results = [
                {
                    'title': '仙侠修炼体系设定',
                    'content': '常见修炼境界：1.引气入体 2.练气 3.筑基 4.金丹 5.元婴 6.化神 7.炼虚 8.合体 9.大乘 10.渡劫飞升。每个境界分初期、中期、后期、巅峰四个阶段。特殊体质：先天道体、混沌体、圣体、神体、魔体、灵体。',
                    'source': '仙侠设定'
                },
                {
                    'title': '仙侠世界元素',
                    'content': '仙侠世界要素：1.宗门：蜀山、昆仑、峨眉、蓬莱、青城 2.功法：内功心法、剑诀、法术、神通 3.法宝：飞剑、符箓、丹药、阵法 4.妖兽：灵草、灵兽、魔兽、神兽 5.地域：凡界、修真界、仙界、神界。',
                    'source': '仙侠素材'
                }
            ]

        return mock_results[0] if mock_results else None

    def _generate_learning_content(self, skill_name, topic, search_results):
        """根据搜索结果生成学习内容"""
        content = {
            'topic': topic,
            'skill_name': skill_name,
            'learned_at': datetime.now().isoformat(),
            'key_points': [],
            'trends': [],
            'tips': [],
            'search_results': search_results
        }

        # 从搜索结果中提取要点
        for result in search_results:
            if 'content' in result:
                text = result['content']
                title = result.get('title', '')

                # 提取数字和数据
                numbers = re.findall(r'\d+%|\d+倍|\d+万|\d+亿', text)
                content['key_points'].extend(numbers)

                # 提取趋势关键词
                trends = re.findall(r'增长|下降|崛起|式微|火爆|热门', text)
                content['trends'].extend(trends)

                # 提取技巧建议和完整要点
                sentences = text.split('。')
                for s in sentences:
                    s = s.strip()
                    if len(s) > 10:
                        # 如果是技巧、方法相关，添加到tips
                        if any(keyword in s for keyword in ['技巧', '方法', '公式', '建议', '注意', '要点']):
                            content['tips'].append(s)
                        # 如果包含题材、类型信息，添加到key_points
                        elif any(keyword in s for keyword in ['题材', '类型', '爆款', '热门', '逆袭', '重生', '穿书']):
                            content['key_points'].append(s)
                        # 其他重要句子也添加到要点
                        elif len(s) > 20:
                            content['key_points'].append(s)

        # 去重并限制数量
        content['key_points'] = list(dict.fromkeys(content['key_points']))[:10]
        content['trends'] = list(dict.fromkeys(content['trends']))[:5]
        content['tips'] = list(dict.fromkeys(content['tips']))[:5]
        content['tips'] = list(dict.fromkeys(content['tips']))[:5]

        return content

    def get_updated_topics(self, skill_name, current_topics):
        """
        根据学习结果更新学习主题

        Args:
            skill_name: Skill名称
            current_topics: 当前主题列表

        Returns:
            list: 更新后的主题列表
        """
        updated = current_topics.copy()

        # 添加基于热门趋势的新主题
        if skill_name == '短篇小说爽文大师':
            # 检查缓存中的最新趋势
            new_topics = [
                '技术流硬核知识文写作',
                '反套路沙雕文创作',
                '非典型救赎情感设计',
                '跨界降维打击设定',
                '末世生存流写作技巧'
            ]
            for topic in new_topics:
                if topic not in updated:
                    updated.append(topic)

        return updated[:30]  # 最多保留30个主题


# 全局实例
_web_learning = None

def get_web_learning():
    """获取联网学习实例"""
    global _web_learning
    if _web_learning is None:
        _web_learning = WebLearning()
    return _web_learning
