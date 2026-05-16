"""
高潮生成模块 - 负责在适当位置生成小高潮和小爆发
每十章必须有一个高潮，增强故事吸引力
"""
import re
import random
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass, field
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class Climax:
    """高潮"""
    climax_type: str
    chapter: int
    intensity: int
    title: str
    content: str
    trigger: str
    consequences: str

@dataclass
class ClimaxElement:
    """高潮元素"""
    element_type: str
    description: str
    participants: List[str]

class ClimaxGenerator:
    """高潮生成器"""
    
    def __init__(self, config: Optional[Any] = None):
        self.config = config
        self.climax_types = self._init_climax_types()
        self.climax_patterns = self._init_climax_patterns()
        self.climax_buildups = self._init_climax_buildups()
        self.climax_releases = self._init_climax_releases()
    
    def _init_climax_types(self) -> Dict[str, Dict[str, Any]]:
        """初始化高潮类型"""
        return {
            'battle': {
                'name': '战斗高潮',
                'description': '生死对决，激烈战斗',
                'intensity_range': (4, 5),
                'elements': ['fight_generator', 'swear_handler'],
                'key_moments': [
                    '最强一击',
                    '绝地反击',
                    '逆转胜负',
                    '同归于尽',
                    '最后一击'
                ]
            },
            'revelation': {
                'name': '揭示高潮',
                'description': '真相大白，震撼揭示',
                'intensity_range': (3, 5),
                'elements': ['emotion_handler'],
                'key_moments': [
                    '身世之谜',
                    '隐藏势力',
                    '惊天秘密',
                    '背叛真相',
                    '幕后黑手'
                ]
            },
            'betrayal': {
                'name': '背叛高潮',
                'description': '亲友背叛，情感冲击',
                'intensity_range': (4, 5),
                'elements': ['emotion_handler', 'swear_handler'],
                'key_moments': [
                    '师父背叛',
                    '兄弟反目',
                    '爱人背叛',
                    '盟友出卖',
                    '身陷绝境'
                ]
            },
            'breakthrough': {
                'name': '突破高潮',
                'description': '实力突破，境界提升',
                'intensity_range': (3, 4),
                'elements': ['fight_generator'],
                'key_moments': [
                    '顿悟',
                    '突破境界',
                    '领悟功法',
                    '觉醒血脉',
                    '获得传承'
                ]
            },
            'confrontation': {
                'name': '对峙高潮',
                'description': '紧张对峙，一触即发',
                'intensity_range': (3, 5),
                'elements': ['swear_handler', 'emotion_handler'],
                'key_moments': [
                    '势力对决',
                    '强者威压',
                    '舌战群儒',
                    '极限对峙',
                    '生死抉择'
                ]
            },
            'escape': {
                'name': '逃亡高潮',
                'description': '绝境求生，惊险逃亡',
                'intensity_range': (4, 5),
                'elements': ['fight_generator'],
                'key_moments': [
                    '围追堵截',
                    '绝地逃生',
                    '九死一生',
                    '千钧一发',
                    '死里逃生'
                ]
            },
            'sacrifice': {
                'name': '牺牲高潮',
                'description': '为救他人，壮烈牺牲',
                'intensity_range': (5, 5),
                'elements': ['emotion_handler'],
                'key_moments': [
                    '自我牺牲',
                    '舍己救人',
                    '以命换命',
                    '壮烈牺牲',
                    '永恒离别'
                ]
            },
            'victory': {
                'name': '胜利高潮',
                'description': '大获全胜，荣耀时刻',
                'intensity_range': (3, 4),
                'elements': ['swear_handler'],
                'key_moments': [
                    '击败强敌',
                    '夺回宝物',
                    '拯救苍生',
                    '登顶称雄',
                    '功成名就'
                ]
            }
        }
    
    def _init_climax_patterns(self) -> Dict[str, List[str]]:
        """初始化高潮模式"""
        return {
            'buildup': [
                '然而就在这时，',
                '谁也没有想到，',
                '突然，',
                '就在众人以为尘埃落定之时，',
                '变故陡生！',
                '事情并没有那么简单，',
                '真正的危机才刚刚开始……',
                '然而，命运却跟他开了个天大的玩笑……',
                '就在这千钧一发之际，',
                '谁知对方突然暴起！'
            ],
            'intensification': [
                '局势急转直下！',
                '事情的发展超出了所有人的预料！',
                '所有人都惊呆了！',
                '这一幕，让在场所有人都倒吸一口凉气！',
                '空气仿佛凝固了一般！',
                '所有人都屏住了呼吸！',
                '时间仿佛静止了！',
                '这一刻，世界都安静了！',
                '所有人的心都提到了嗓子眼！',
                '危险正在一步步逼近……'
            ],
            'climax_action': [
                '电光火石间，',
                '说时迟那时快，',
                '就在这生死存亡的关头，',
                '就在对方露出破绽的一瞬间，',
                '然而，',
                '不料，',
                '却见对方',
                '只见',
                '但见',
                '却不知'
            ],
            'resolution': [
                '尘埃落定，',
                '最终，',
                '良久，',
                '半晌，',
                '许久之后，',
                '风波暂时平息，',
                '危机总算解除，',
                '战斗终于结束，',
                '真相大白，',
                '一切终于水落石出……'
            ]
        }
    
    def _init_climax_buildups(self) -> Dict[str, List[str]]:
        """初始化高潮铺垫"""
        return {
            'battle': [
                '双方已经大战了三百回合，仍未分出胜负。',
                '战斗进入白热化阶段，双方都已筋疲力尽。',
                '对方的攻势如狂风暴雨，让他渐渐难以招架。',
                '每一次交手都是生死较量，双方都拼尽了全力。'
            ],
            'revelation': [
                '然而，当真相揭晓的那一刻，所有人都震惊了。',
                '直到这一刻，他才明白一切都只是阴谋。',
                '原来如此，一切都说得通了！',
                '这个秘密一旦曝光，必将引起轩然大波。'
            ],
            'betrayal': [
                '他怎么也没有想到，背叛他的竟是他最信任的人。',
                '看着那张熟悉的脸，他的心瞬间坠入冰窟。',
                '曾经并肩作战的兄弟，如今却刀剑相向。',
                '当那柄剑刺入他身体的那一刻，一切都结束了。'
            ],
            'breakthrough': [
                '就在生死存亡之际，他体内突然涌起一股强大的力量。',
                '多年的积累终于在这一刻爆发！',
                '仿佛有什么东西在体内炸开，他的实力瞬间暴涨！',
                '就在这一瞬间，他感觉自己触摸到了那道门槛。'
            ],
            'confrontation': [
                '两大高手对峙，气势如山岳般沉重。',
                '空气中弥漫着火药味，大战一触即发。',
                '双方剑拔弩张，谁也不肯退让半步。',
                '强者威压如实质般压来，让人喘不过气。'
            ],
            'escape': [
                '前有堵截，后有追兵，他陷入了绝境。',
                '敌人的包围圈越收越小，他能活动的空间越来越有限。',
                '每走一步都是陷阱，每停一秒都是死亡。',
                '时间一分一秒地流逝，他的生机也在一点点消失。'
            ],
            'sacrifice': [
                '为了保护身后的人，他选择了牺牲自己。',
                '明知必死无疑，他却依然义无反顾。',
                '在生命的最后一刻，他露出了释然的笑容。',
                '用自己的生命，换取他人的一线生机。'
            ],
            'victory': [
                '随着最后一击落下，胜负终于揭晓。',
                '当对方倒下的那一刻，他长长地舒了口气。',
                '终于结束了，他做到了！',
                '这一刻，所有的付出都得到了回报。'
            ]
        }
    
    def _init_climax_releases(self) -> Dict[str, List[str]]:
        """初始化高潮释放"""
        return {
            'battle': [
                '轰然巨响，气浪翻涌，双方都被震退了数丈！',
                '一道剑光划破夜空，直取对方要害！',
                '两人同时出招，胜负就在这一瞬间！',
                '只听砰的一声，其中一人倒飞出去！'
            ],
            'revelation': [
                '原来，竟然是他！所有人都惊呆了！',
                '真相大白，所有人都难以置信！',
                '这个秘密一旦曝光，必将改变整个格局！',
                '直到此刻他才明白，一切都只是一场骗局！'
            ],
            'betrayal': [
                '他怎么也没有想到，最亲近的人会背叛他。',
                '心像是被什么东西狠狠刺穿，疼得他几乎无法呼吸。',
                '曾经的信任在这一刻化为乌有。',
                '他感觉自己的世界在这一刻崩塌了。'
            ],
            'breakthrough': [
                '轰的一声，他周身金光大盛，实力暴涨！',
                '突破了！他终于突破了！',
                '这一刻，他感觉自己前所未有的强大！',
                '多年来的积累在这一刻全部转化为力量！'
            ],
            'confrontation': [
                '双方的气势同时爆发，碰撞出激烈的火花！',
                '只听轰的一声，双方同时倒退三步！',
                '气浪翻涌，尘土飞扬，两人的身影在烟尘中若隐若现。',
                '强者的对决，每一招都是生死较量！'
            ],
            'escape': [
                '就在刀锋即将落下的瞬间，他猛地侧身躲过！',
                '他拼尽全力，终于冲出了包围圈！',
                '生死一线间，他做出了最正确的选择！',
                '就在这千钧一发之际，援兵终于到了！'
            ],
            'sacrifice': [
                '鲜血飞溅，他用身体挡下了那致命的一击。',
                '在倒下的最后一刻，他依然保持着微笑。',
                '他的牺牲，换来了所有人的平安。',
                '英雄陨落，天地同悲。'
            ],
            'victory': [
                '当对方倒下的那一刻，欢呼声响彻云霄！',
                '胜利了！他终于胜利了！',
                '这一刻，所有的艰辛都化为了喜悦的泪水。',
                '荣耀加身，他终于站在了巅峰！'
            ]
        }
    
    def generate_climax(
        self,
        climax_type: str,
        chapter: int,
        context: Dict[str, Any],
        protagonist: str,
        antagonist: Optional[str] = None
    ) -> Climax:
        """生成高潮"""
        logger.info(f"生成{chapter}章高潮，类型: {climax_type}")
        
        if climax_type not in self.climax_types:
            climax_type = self._infer_climax_type(context)
        
        climax_info = self.climax_types[climax_type]
        intensity = random.randint(*climax_info['intensity_range'])
        
        key_moment = random.choice(climax_info['key_moments'])
        title = f"第{chapter}章 · {key_moment}"
        
        buildup = self._generate_buildup(climax_type, protagonist, antagonist, context)
        action = self._generate_climax_action(climax_type, protagonist, antagonist, context)
        release = self._generate_release(climax_type, protagonist, antagonist, context)
        consequence = self._generate_consequence(climax_type, context)
        
        content = buildup + "\n\n" + action + "\n\n" + release + "\n\n" + consequence
        
        climax = Climax(
            climax_type=climax_type,
            chapter=chapter,
            intensity=intensity,
            title=title,
            content=content,
            trigger=self._generate_trigger(climax_type, context),
            consequences=self._summarize_consequences(climax_type, consequence)
        )
        
        logger.info(f"高潮生成完成: {title}, 强度: {intensity}/5")
        return climax
    
    def _infer_climax_type(self, context: Dict[str, Any]) -> str:
        """推断高潮类型"""
        context_str = str(context).lower()
        
        if any(word in context_str for word in ['战斗', '对决', '搏斗', '厮杀']):
            return 'battle'
        elif any(word in context_str for word in ['背叛', '出卖', '反目']):
            return 'betrayal'
        elif any(word in context_str for word in ['揭示', '真相', '秘密']):
            return 'revelation'
        elif any(word in context_str for word in ['突破', '顿悟', '觉醒']):
            return 'breakthrough'
        elif any(word in context_str for word in ['对峙', '威胁', '压迫']):
            return 'confrontation'
        elif any(word in context_str for word in ['逃亡', '逃跑', '追杀']):
            return 'escape'
        elif any(word in context_str for word in ['牺牲', '死亡', '离别']):
            return 'sacrifice'
        else:
            return 'victory'
    
    def _generate_buildup(self, climax_type: str, protagonist: str, antagonist: Optional[str], context: Dict[str, Any]) -> str:
        """生成高潮铺垫"""
        buildup_patterns = self.climax_patterns['buildup']
        buildup_templates = self.climax_buildups.get(climax_type, self.climax_buildups['battle'])
        
        parts = []
        parts.append(random.choice(buildup_patterns))
        
        template = random.choice(buildup_templates)
        template = template.replace('{protagonist}', protagonist)
        template = template.replace('{antagonist}', antagonist or '对手')
        parts.append(template)
        
        intensification = random.choice(self.climax_patterns['intensification'])
        parts.append(intensification)
        
        return ''.join(parts)
    
    def _generate_climax_action(self, climax_type: str, protagonist: str, antagonist: Optional[str], context: Dict[str, Any]) -> str:
        """生成高潮动作"""
        action_patterns = self.climax_patterns['climax_action']
        
        parts = []
        parts.append(random.choice(action_patterns))
        
        if climax_type == 'battle':
            action = self._generate_battle_action(protagonist, antagonist)
        elif climax_type == 'breakthrough':
            action = self._generate_breakthrough_action(protagonist)
        elif climax_type == 'revelation':
            action = self._generate_revelation_action(protagonist)
        elif climax_type == 'betrayal':
            action = self._generate_betrayal_action(protagonist, antagonist)
        else:
            action = self._generate_generic_action(protagonist, antagonist)
        
        parts.append(action)
        
        return ''.join(parts)
    
    def _generate_battle_action(self, protagonist: str, antagonist: Optional[str]) -> str:
        """生成战斗动作"""
        actions = [
            f'{protagonist}凝聚全身灵力，一道璀璨的剑芒直冲云霄！',
            f'{protagonist}双掌推出，一股排山倒海般的掌力呼啸而出！',
            f'只见{protagonist}身形暴起，化作一道流光，直取对方要害！',
            f'{protagonist}张口喷出一道精纯的真元，化作漫天剑影！',
            f'双方同时暴喝一声，两股力量轰然相撞！',
            f'就在这千钧一发之际，{protagonist}使出了自己的最强一击！'
        ]
        return random.choice(actions)
    
    def _generate_breakthrough_action(self, protagonist: str) -> str:
        """生成突破动作"""
        actions = [
            f'轰的一声，{protagonist}体内仿佛有什么东西被打破！',
            f'{protagonist}感觉自己的经脉在疯狂扩张，灵力如潮水般涌入！',
            f'就在这一刻，{protagonist}多年的积累终于迎来了质变！',
            f'{protagonist}仰天长啸，周身金光大盛，气势节节攀升！',
            f'一道璀璨的光柱从{protagonist}体内冲霄而起！',
            f'天地灵气疯狂涌动，尽数涌入{protagonist}体内！'
        ]
        return random.choice(actions)
    
    def _generate_revelation_action(self, protagonist: str) -> str:
        """生成揭示动作"""
        actions = [
            f'当真相揭晓的那一刻，{protagonist}整个人都僵住了。',
            f'这个秘密如同惊雷，在{protagonist}脑海中炸响！',
            f'一切都说得通了！{protagonist}终于明白了前因后果！',
            f'原来如此！{protagonist}感觉自己的世界观都被颠覆了！',
            f'当那个名字被说出，{protagonist}如遭雷击！'
        ]
        return random.choice(actions)
    
    def _generate_betrayal_action(self, protagonist: str, antagonist: Optional[str]) -> str:
        """生成背叛动作"""
        actions = [
            f'当那柄剑刺入{protagonist}身体的那一刻，一切都结束了。',
            f'{protagonist}瞪大眼睛，不敢置信地看着面前的人。',
            f'曾经最信任的人，此刻却露出了狰狞的笑容。',
            f'心像是被什么东西狠狠撕裂，疼得{protagonist}几乎无法呼吸。',
            f'鲜血从伤口涌出，{protagonist}踉跄后退，不敢相信眼前的一切。'
        ]
        return random.choice(actions)
    
    def _generate_generic_action(self, protagonist: str, antagonist: Optional[str]) -> str:
        """生成通用动作"""
        actions = [
            f'{protagonist}做出了决定，义无反顾地冲了上去！',
            f'就在这生死存亡的关头，{protagonist}展现出了惊人的潜力！',
            f'局势瞬间逆转，所有人都惊呆了！',
            f'命运在这一刻做出了选择。',
            f'当一切尘埃落定，{protagonist}终于松了一口气。'
        ]
        return random.choice(actions)
    
    def _generate_release(self, climax_type: str, protagonist: str, antagonist: Optional[str], context: Dict[str, Any]) -> str:
        """生成高潮释放"""
        release_patterns = self.climax_patterns['resolution']
        release_templates = self.climax_releases.get(climax_type, self.climax_releases['victory'])
        
        parts = []
        
        template = random.choice(release_templates)
        template = template.replace('{protagonist}', protagonist)
        template = template.replace('{antagonist}', antagonist or '对手')
        parts.append(template)
        
        parts.append(random.choice(release_patterns))
        
        return ''.join(parts)
    
    def _generate_consequence(self, climax_type: str, context: Dict[str, Any]) -> str:
        """生成后果"""
        consequences = {
            'battle': '双方都付出了惨重的代价，战斗终于落下帷幕。',
            'revelation': '这个秘密将改变所有人的命运。',
            'betrayal': '信任一旦崩塌，就再也无法回到从前。',
            'breakthrough': '实力暴涨的他，前路将一片光明。',
            'confrontation': '这场对峙将决定未来的格局。',
            'escape': '虽然逃出生天，但他也身负重伤。',
            'sacrifice': '英雄的牺牲不会白费。',
            'victory': '胜利的喜悦冲淡了所有的疲惫。'
        }
        
        return consequences.get(climax_type, '一切终于结束了。')
    
    def _generate_trigger(self, climax_type: str, context: Dict[str, Any]) -> str:
        """生成触发点"""
        triggers = [
            '命运的安排',
            '敌人的阴谋',
            '实力的差距',
            '内心的执念',
            '时机的把握',
            '运气的眷顾',
            '盟友的支援',
            '敌人的大意'
        ]
        return random.choice(triggers)
    
    def _summarize_consequences(self, climax_type: str, consequence: str) -> str:
        """总结后果"""
        return consequence[:50] if len(consequence) > 50 else consequence
    
    def should_insert_climax(self, chapter_number: int, climax_interval: int = 10) -> bool:
        """判断是否应该插入高潮"""
        return chapter_number % climax_interval == 0 or chapter_number % climax_interval == climax_interval - 1
    
    def generate_climax_plan(self, total_chapters: int, climax_interval: int = 10) -> List[int]:
        """生成高潮计划"""
        climax_chapters = []
        
        for i in range(1, total_chapters + 1):
            if self.should_insert_climax(i, climax_interval):
                climax_chapters.append(i)
        
        if total_chapters > 10 and total_chapters % climax_interval != 0:
            climax_chapters.append(total_chapters)
        
        climax_chapters = sorted(list(set(climax_chapters)))
        
        return climax_chapters
    
    def integrate_climax_into_chapter(
        self,
        chapter_content: str,
        climax: Climax,
        position: str = 'end'
    ) -> str:
        """将高潮整合到章节中"""
        logger.info(f"整合高潮到章节，位置: {position}")
        
        climax_section = f"\n\n{'='*20}\n{climax.title}\n{'='*20}\n\n{climax.content}\n"
        
        if position == 'end':
            return chapter_content + climax_section
        elif position == 'middle':
            midpoint = len(chapter_content) // 2
            return chapter_content[:midpoint] + climax_section + chapter_content[midpoint:]
        else:
            return climax_section + chapter_content
    
    def enhance_chapter_with_micro_climax(
        self,
        chapter_content: str,
        chapter_number: int
    ) -> str:
        """增强章节小高潮"""
        logger.info(f"增强第{chapter_number}章小高潮")
        
        if chapter_number % 5 == 0:
            buildup = random.choice(self.climax_patterns['buildup'][:5])
            intensification = random.choice(self.climax_patterns['intensification'][:5])
            
            micro_climax = f"\n\n{buildup}{intensification}"
            
            sentences = re.split(r'[。！？]', chapter_content)
            if len(sentences) > 10:
                insert_pos = len(sentences) // 2
                sentences.insert(insert_pos, micro_climax)
                return ''.join(sentences)
        
        return chapter_content


def test_climax_generator():
    """测试高潮生成"""
    print("=" * 60)
    print("高潮生成模块测试")
    print("=" * 60)
    
    generator = ClimaxGenerator()
    
    context = {
        'location': '青云山顶',
        'situation': '生死对决',
        'protagonist': '李云',
        'antagonist': '清风真人'
    }
    
    print("\n测试1: 生成战斗高潮")
    try:
        climax = generator.generate_climax(
            climax_type='battle',
            chapter=10,
            context=context,
            protagonist='李云',
            antagonist='清风真人'
        )
        print(f"✓ 生成成功")
        print(f"  类型: {climax.climax_type}")
        print(f"  标题: {climax.title}")
        print(f"  强度: {climax.intensity}/5")
        print(f"\n内容预览:\n{climax.content[:300]}...")
    except Exception as e:
        print(f"✗ 生成失败: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n测试2: 生成突破高潮")
    try:
        climax = generator.generate_climax(
            climax_type='breakthrough',
            chapter=20,
            context={'protagonist': '李云'},
            protagonist='李云'
        )
        print(f"✓ 生成成功")
        print(f"  类型: {climax.climax_type}")
        print(f"  标题: {climax.title}")
    except Exception as e:
        print(f"✗ 生成失败: {e}")
    
    print("\n测试3: 高潮计划生成")
    try:
        plan = generator.generate_climax_plan(50, 10)
        print(f"✓ 生成成功")
        print(f"  计划章节: {plan}")
        print(f"  总共 {len(plan)} 个高潮点")
    except Exception as e:
        print(f"✗ 生成失败: {e}")
    
    print("\n测试4: 章节高潮增强")
    try:
        chapter = "李云走在山路上，突然遇到敌人袭击。双方展开激烈战斗，最终李云获胜。"
        enhanced = generator.enhance_chapter_with_micro_climax(chapter, 5)
        print(f"✓ 增强成功")
        print(f"  原文: {chapter}")
        print(f"  增强后: {enhanced[:100]}...")
    except Exception as e:
        print(f"✗ 增强失败: {e}")
    
    print("\n测试5: 高潮类型推断")
    try:
        contexts = [
            {'situation': '生死战斗'},
            {'situation': '真相揭示'},
            {'situation': '被背叛'}
        ]
        for ctx in contexts:
            climax_type = generator._infer_climax_type(ctx)
            print(f"  {ctx} -> {climax_type}")
    except Exception as e:
        print(f"✗ 推断失败: {e}")
    
    print("\n" + "=" * 60)
    print("高潮生成模块测试完成")
    print("=" * 60)


if __name__ == "__main__":
    test_climax_generator()
