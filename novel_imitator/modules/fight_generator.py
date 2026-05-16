"""
打斗场景生成模块 - 负责生成具体化的打斗场景
将抽象的打斗描写转换为具体的动作细节
"""
import re
import random
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass, field
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class CombatMove:
    """战斗动作"""
    name: str
    type: str
    description: str
    speed: str
    damage: str
    animation: List[str]

@dataclass
class Combatant:
    """战斗者"""
    name: str
    power_level: str
    weapon: str
    fighting_style: str
    special_abilities: List[str]

@dataclass
class CombatPhase:
    """战斗阶段"""
    phase_type: str
    moves: List[CombatMove]
    duration: str
    intensity: int
    description: str

class FightSceneGenerator:
    """打斗场景生成器"""
    
    def __init__(self, config: Optional[Any] = None):
        self.config = config
        self.basic_moves = self._init_basic_moves()
        self.weapon_techniques = self._init_weapon_techniques()
        self.bodypart_actions = self._init_bodypart_actions()
        self.combat_sounds = self._init_combat_sounds()
        self.combat_transitions = self._init_combat_transitions()
    
    def _init_basic_moves(self) -> Dict[str, List[str]]:
        """初始化基础动作"""
        return {
            'punch': [
                '猛地一拳砸出，带着呼啸的风声直奔对方面门',
                '右拳如同毒蛇出洞，闪电般击向对手胸口',
                '一拳挥出，拳风猎猎作响，直取对方要害',
                '勾拳上挑，拳头带着凌厉的劲风',
                '冲拳直击，拳头发出一声闷响',
                '摆拳横扫，势大力沉，寻常人挨上就得骨断筋折'
            ],
            'kick': [
                '飞起一脚，直踢对方下颌，腿风凌厉',
                '横扫一腿，如铁棍横扫，带着呼呼风声',
                '垫步上前，膝盖如毒蝎般顶向对方小腹',
                '脚尖点地，身形暴起，一脚踢向对方胸口',
                '下劈一腿，如巨斧劈下，带着千钧之力',
                '回旋踢，腿影重重，让人防不胜防'
            ],
            'block': [
                '双臂交叉，硬生生挡下对方攻击',
                '侧身一闪，顺势用手臂格挡开来',
                '以掌代刀，精准地拍开来拳',
                '脚步一错，避开要害，顺手挡开攻击',
                '后仰闪避，但还是被拳风扫中',
                '硬接一掌，震得虎口发麻'
            ],
            'dodge': [
                '身形一晃，如鬼魅般闪到一旁',
                '侧身避过，堪堪躲过这致命一击',
                '脚尖一点，身形暴退三尺',
                '后仰避开来拳，额头冷汗直冒',
                '侧头一闪，拳风擦着耳根掠过',
                '猛地低头，躲过横扫的腿影'
            ],
            'counter': [
                '趁对方收招不及，一掌拍向对方胸口',
                '借力打力，将对方攻势完全卸去',
                '反手一肘，正中对方软肋',
                '抓住破绽，一记膝顶撞向对方腹部',
                '脚下一绊，将对方摔了个四脚朝天',
                '扣住对方手腕，猛地一拉一送'
            ],
            'special': [
                '指尖凝聚灵力，一道光芒激射而出',
                '真气运转，双掌推出，一道气浪席卷而去',
                '掐诀念咒，周身灵气涌动',
                '祭出法宝，灵光万道',
                '催动秘术，战力陡然暴涨',
                '燃烧生命精华，实力瞬间翻倍'
            ]
        }
    
    def _init_weapon_techniques(self) -> Dict[str, List[str]]:
        """初始化武器技巧"""
        return {
            'sword': [
                '剑光如练，一道寒芒划破长空',
                '剑身一抖，化作漫天剑影',
                '剑尖直刺，带着尖锐的破空声',
                '横剑一挡，堪堪挡住对方攻击',
                '挽了个剑花，剑气纵横',
                '剑走偏锋，招招狠辣'
            ],
            'blade': [
                '刀光闪烁，寒芒逼人',
                '大刀阔斧，一刀劈下，山崩地裂般的气势',
                '刀锋一转，横扫千军',
                '刀背拍击，震得对方五脏六腑都在翻涌',
                '刀光霍霍，每一刀都带着必杀的决心',
                '刀势如虹，势不可挡'
            ],
            'spear': [
                '长枪如龙，直刺而出，带着尖锐的破空声',
                '枪尖一抖，点点寒芒笼罩对方周身',
                '横扫一枪，将对方逼退数步',
                '枪身一挡，架住对方的攻击',
                '刺、挑、扫、拨，枪法如神',
                '长枪所向，无人能挡'
            ],
            'staff': [
                '棍影重重，如狂风暴雨般袭来',
                '当头一棒，带着呼啸的风声',
                '横扫千军，棍风呼啸',
                '一挡一拨，将攻击尽数卸开',
                '棍法刚猛，每一击都势大力沉',
                '连环三棍，让人眼花缭乱'
            ],
            'fist': [
                '拳拳到肉，每一击都带着千钧之力',
                '拳风呼啸，招招直奔要害',
                '连环拳打，快如闪电',
                '以拳化掌，拍向对方胸口',
                '双拳如锤，狠狠砸下',
                '拳法凌厉，让人难以招架'
            ],
            'palm': [
                '掌风猎猎，一掌拍出，空气都被压缩',
                '掌心凝聚灵力，光芒闪烁',
                '掌影重重，虚实难辨',
                '一掌推出，带着排山倒海般的气势',
                '掌法精妙，每一掌都恰到好处',
                '凌空一掌，隔空伤人'
            ]
        }
    
    def _init_bodypart_actions(self) -> Dict[str, List[str]]:
        """初始化身体部位动作"""
        return {
            'eye': [
                '眼睛眯起，死死盯着对方的动作',
                '眼神一凝，不敢有丝毫大意',
                '眼中精光闪烁，寻找对方破绽',
                '瞳孔收缩，看清了对方的攻击轨迹',
                '瞪大眼睛，满脸不可思议',
                '眼皮直跳，暗道不好'
            ],
            'mouth': [
                '牙关紧咬，使出全力',
                '嘴角勾起一抹冷笑',
                '张开大嘴，发出一声怒吼',
                '嘴唇颤抖，说不出话来',
                '嘴角溢出一丝鲜血',
                '咬牙切齿，眼中满是怒火'
            ],
            'hand': [
                '手掌紧握成拳，指关节泛白',
                '手指微微颤抖，不知是紧张还是兴奋',
                '十指张开，摆出进攻架势',
                '五指如钩，抓向对方咽喉',
                '手掌拍出，带着呼啸的风声',
                '手指连点，封住对方穴道'
            ],
            'foot': [
                '脚步一错，避开对方的攻击',
                '脚尖一点，身形暴起',
                '双脚踏地，扎稳马步',
                '脚下一滑，险些摔倒',
                '脚跟一蹬，踢向对方小腿',
                '脚步如风，身形飘忽不定'
            ],
            'body': [
                '身形一晃，出现在对方身后',
                '身子一矮，躲过横劈的一刀',
                '身躯一震，硬接下这一击',
                '身体前倾，攻向对方下盘',
                '身形暴退，拉开距离',
                '腰身一拧，躲过致命一击'
            ]
        }
    
    def _init_combat_sounds(self) -> Dict[str, List[str]]:
        """初始化战斗音效"""
        return {
            'impact': [
                '砰的一声，两股力量狠狠撞在一起',
                '轰隆巨响，气浪向四周扩散',
                '闷响传来，双方各退数步',
                '啪的一下，骨头断裂的声音清晰可闻',
                '轰然炸响，尘土飞扬',
                '咔嚓一声，武器相交，火花四溅'
            ],
            'whoosh': [
                '呼呼的风声在耳边呼啸而过',
                '尖锐的破空声响彻耳际',
                '风声大作，树叶簌簌落下',
                '空气被撕裂，发出嘶嘶声',
                '劲风扑面，刮得人脸颊生疼',
                '气流涌动，让人呼吸一窒'
            ],
            'scream': [
                '发出一声凄厉的惨叫',
                '仰天怒吼，声音震得山林都在颤抖',
                '闷哼一声，脸色瞬间惨白',
                '痛得大声呼叫，声音都变了调',
                '一声暴喝，气势陡然暴涨',
                '发出野兽般的嘶吼'
            ],
            'metal': [
                '叮叮当当，金铁交鸣声不绝于耳',
                '刀剑相击，火星四溅',
                '金属碰撞，发出刺耳的声响',
                '枪棍相交，震得手臂发麻',
                '法宝相撞，灵光乱闪',
                '铛的一声，其中一人武器脱手'
            ]
        }
    
    def _init_combat_transitions(self) -> List[str]:
        """初始化战斗过渡"""
        return [
            '电光火石间',
            '说时迟那时快',
            '眨眼之间',
            '就在这千钧一发之际',
            '就在对方愣神的功夫',
            '趁着对方收招不及',
            '就在刀锋即将落下的瞬间',
            '就在双方僵持不下时',
            '就在对方露出破绽的一刹那',
            '然而就在这时',
            '却见对方突然变招',
            '谁知对方早有准备',
            '不料对方另有杀招'
        ]
    
    def generate_fight_scene(
        self, 
        combatants: List[Combatant],
        context: Dict[str, Any],
        intensity: str = 'medium',
        min_length: int = 300,
        max_length: int = 2000
    ) -> str:
        """生成打斗场景"""
        logger.info(f"生成打斗场景，参与者: {[c.name for c in combatants]}")
        
        if len(combatants) < 2:
            raise ValueError("战斗需要至少两个参与者")
        
        protagonist = combatants[0]
        antagonist = combatants[1] if len(combatants) > 1 else None
        
        phases = self._generate_combat_phases(protagonist, antagonist, intensity)
        
        scene_parts = []
        scene_parts.append(self._generate_opening(protagonist, antagonist, context))
        
        for phase in phases:
            phase_text = self._generate_phase_text(phase, protagonist, antagonist)
            scene_parts.append(phase_text)
        
        scene_parts.append(self._generate_ending(protagonist, antagonist, phases))
        
        scene = '\n\n'.join(scene_parts)
        
        while len(scene) < min_length and len(phases) < 10:
            phases.append(self._add_extra_phase(protagonist, antagonist, intensity))
            scene_parts.append(self._generate_phase_text(phases[-1], protagonist, antagonist))
            scene = '\n\n'.join(scene_parts)
        
        while len(scene) > max_length and len(scene_parts) > 3:
            scene_parts.pop()
            scene = '\n\n'.join(scene_parts)
        
        logger.info(f"打斗场景生成完成，长度: {len(scene)}字")
        return scene
    
    def _generate_opening(self, protagonist: Combatant, antagonist: Optional[Combatant], context: Dict[str, Any]) -> str:
        """生成开场"""
        openings = [
            f"只见{protagonist.name}眼神一凝，周身气势陡然攀升。",
            f"双方对峙，空气中弥漫着火药味。",
            f"{protagonist.name}深吸一口气，体内真气疯狂运转。",
            f"一场激战，一触即发！",
            f"{antagonist.name}冷笑一声，率先发动攻击！"
        ]
        
        opening = random.choice(openings)
        
        if antagonist:
            opening += f"\n\n{antagonist.name}手持{antagonist.weapon}，眼中满是杀意。"
        
        opening += f"\n\n{protagonist.name}也不甘示弱，{protagonist.fighting_style}，迎了上去。"
        
        return opening
    
    def _generate_combat_phases(self, protagonist: Combatant, antagonist: Optional[Combatant], intensity: str) -> List[CombatPhase]:
        """生成战斗阶段"""
        phases = []
        
        phase_count = {'low': 3, 'medium': 5, 'high': 8}[intensity]
        
        for i in range(phase_count):
            phase_intensity = min(i + 1, 5)
            
            if i < phase_count * 0.3:
                phase_type = 'opening'
            elif i < phase_count * 0.7:
                phase_type = 'climax'
            else:
                phase_type = 'finale'
            
            moves = self._generate_phase_moves(phase_type, protagonist, antagonist)
            
            phase = CombatPhase(
                phase_type=phase_type,
                moves=moves,
                duration=self._estimate_phase_duration(phase_type),
                intensity=phase_intensity,
                description=""
            )
            
            phases.append(phase)
        
        return phases
    
    def _generate_phase_moves(self, phase_type: str, protagonist: Combatant, antagonist: Optional[Combatant]) -> List[CombatMove]:
        """生成阶段动作"""
        moves = []
        move_count = {'opening': 3, 'climax': 5, 'finale': 4}[phase_type]
        
        attack_types = ['punch', 'kick', 'special']
        defense_types = ['block', 'dodge', 'counter']
        
        if protagonist.weapon and protagonist.weapon != '徒手':
            attack_types.extend(['sword', 'blade', 'spear', 'staff'])
        
        for i in range(move_count):
            if i % 2 == 0:
                move_type = random.choice(attack_types)
                actor = protagonist
            else:
                move_type = random.choice(defense_types)
                actor = antagonist or protagonist
            
            move = CombatMove(
                name=f"{actor.name}的{move_type}",
                type=move_type,
                description=self._generate_move_description(move_type, actor),
                speed=self._generate_speed_description(i, phase_type),
                damage=self._generate_damage_description(i, phase_type),
                animation=self._generate_move_animation(move_type, actor)
            )
            
            moves.append(move)
        
        return moves
    
    def _generate_move_description(self, move_type: str, actor: Combatant) -> str:
        """生成动作描述"""
        if move_type in self.basic_moves:
            descriptions = self.basic_moves[move_type]
            desc = random.choice(descriptions)
            
            if '{name}' not in desc:
                desc = f"{actor.name}" + desc
            else:
                desc = desc.replace('{name}', actor.name)
            
            return desc
        elif move_type in self.weapon_techniques:
            descriptions = self.weapon_techniques[move_type]
            return random.choice(descriptions)
        
        return f"{actor.name}使出了一招"
    
    def _generate_speed_description(self, move_index: int, phase_type: str) -> str:
        """生成速度描述"""
        speed_words = [
            '快如闪电',
            '势若奔雷',
            '电光火石般',
            '快得看不清',
            '迅猛无比',
            '凌厉无匹',
            '快到了极致'
        ]
        
        if phase_type in ['climax', 'finale']:
            return random.choice(speed_words[:4])
        else:
            return random.choice(speed_words[3:])
    
    def _generate_damage_description(self, move_index: int, phase_type: str) -> str:
        """生成伤害描述"""
        damage_phrases = [
            '直打得骨断筋折',
            '震得五脏六腑都在翻涌',
            '打得口吐鲜血',
            '震得连连后退',
            '身上多处受伤',
            '鲜血飞溅'
        ]
        
        if phase_type == 'finale':
            return random.choice(damage_phrases[:2])
        else:
            return random.choice(damage_phrases[2:])
    
    def _generate_move_animation(self, move_type: str, actor: Combatant) -> List[str]:
        """生成动作动画"""
        animations = []
        
        if 'eye' in actor.fighting_style.lower() or random.random() > 0.5:
            animations.append(random.choice(self.bodypart_actions['eye']))
        
        if 'hand' in move_type.lower() or random.random() > 0.5:
            animations.append(random.choice(self.bodypart_actions['hand']))
        
        if random.random() > 0.6:
            animations.append(random.choice(self.combat_sounds['whoosh']))
        
        return animations
    
    def _generate_phase_text(self, phase: CombatPhase, protagonist: Combatant, antagonist: Optional[Combatant]) -> str:
        """生成阶段文本"""
        phase_text_parts = []
        
        if phase.phase_type == 'climax':
            transition = random.choice(self.combat_transitions)
            phase_text_parts.append(transition)
        
        for i, move in enumerate(phase.moves):
            move_text = move.description
            
            for anim in move.animation[:2]:
                move_text += f"，{anim}"
            
            if i > 0 and random.random() > 0.7:
                sound = random.choice(list(self.combat_sounds.values())[0])
                move_text += f"，{random.choice(sound)}"
            
            phase_text_parts.append(move_text)
            
            if i < len(phase.moves) - 1 and phase.phase_type == 'climax':
                impact = random.choice(self.combat_sounds['impact'])
                phase_text_parts.append(impact)
        
        return '。\n\n'.join(phase_text_parts) + '。'
    
    def _estimate_phase_duration(self, phase_type: str) -> str:
        """估算阶段时长"""
        durations = {
            'opening': '数息之间',
            'climax': '电光火石间',
            'finale': '最后一击'
        }
        return durations.get(phase_type, '')
    
    def _add_extra_phase(self, protagonist: Combatant, antagonist: Optional[Combatant], intensity: str) -> CombatPhase:
        """添加额外阶段"""
        return CombatPhase(
            phase_type='extension',
            moves=self._generate_phase_moves('climax', protagonist, antagonist)[:3],
            duration='激战中',
            intensity=3,
            description=""
        )
    
    def _generate_ending(self, protagonist: Combatant, antagonist: Optional[Combatant], phases: List[CombatPhase]) -> str:
        """生成结尾"""
        endings = [
            f"一番激战下来，{protagonist.name}终于将{antagonist.name if antagonist else '对手'}击败。",
            f"最终，{protagonist.name}凭借{protagonist.fighting_style}，险胜对手。",
            f"战斗结束，{protagonist.name}大口喘着粗气，身上伤痕累累。",
            f"胜负已分，{protagonist.name}傲然而立，俯视着倒在地上的{antagonist.name if antagonist else '对手'}。"
        ]
        
        ending = random.choice(endings)
        
        if phases[-1].phase_type == 'finale':
            impact = random.choice(self.combat_sounds['impact'])
            ending = f"{impact}，" + ending
        
        return ending
    
    def concretize_fight_phrase(self, abstract_phrase: str) -> str:
        """具体化抽象战斗短语"""
        conversions = {
            '激烈战斗': '刀光剑影，血雨腥风，招招凶险，式式致命',
            '一招': '身形暴起，掌风呼啸，直取要害',
            '很快': '快若闪电，疾如风雷，让人根本来不及反应',
            '很重': '势大力沉，如同山岳压顶，寻常人挨上就得粉身碎骨',
            '打斗': '你来我往，互不相让，每一招都带着滔天杀意',
            '受伤': '鲜血飞溅，染红了衣襟，伤口触目惊心'
        }
        
        for abstract, concrete in conversions.items():
            if abstract in abstract_phrase:
                return abstract_phrase.replace(abstract, concrete)
        
        return abstract_phrase


def test_fight_scene_generator():
    """测试打斗场景生成"""
    print("=" * 60)
    print("打斗场景生成模块测试")
    print("=" * 60)
    
    generator = FightSceneGenerator()
    
    protagonist = Combatant(
        name='李云',
        power_level='筑基境',
        weapon='长剑',
        fighting_style='剑术精湛，招招狠辣',
        special_abilities=['剑气', '御剑术']
    )
    
    antagonist = Combatant(
        name='黑衣人',
        power_level='筑基境',
        weapon='弯刀',
        fighting_style='刀法诡异，出招狠辣',
        special_abilities=['暗器']
    )
    
    context = {
        'location': '荒野',
        'time': '深夜',
        'cause': '争夺宝物'
    }
    
    print("\n测试1: 生成中等强度打斗场景")
    try:
        scene = generator.generate_fight_scene(
            [protagonist, antagonist],
            context,
            intensity='medium',
            min_length=500
        )
        print(f"✓ 生成成功")
        print(f"  长度: {len(scene)}字")
        print(f"\n生成内容预览:\n{scene[:500]}...")
    except Exception as e:
        print(f"✗ 生成失败: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n测试2: 生成高强度打斗场景")
    try:
        scene = generator.generate_fight_scene(
            [protagonist, antagonist],
            context,
            intensity='high',
            min_length=800
        )
        print(f"✓ 生成成功")
        print(f"  长度: {len(scene)}字")
    except Exception as e:
        print(f"✗ 生成失败: {e}")
    
    print("\n测试3: 动作描述生成")
    try:
        for move_type in ['punch', 'kick', 'block']:
            desc = generator._generate_move_description(move_type, protagonist)
            print(f"  {move_type}: {desc}")
    except Exception as e:
        print(f"✗ 生成失败: {e}")
    
    print("\n测试4: 战斗音效")
    try:
        sounds = generator.combat_sounds
        print(f"  撞击声: {random.choice(sounds['impact'])}")
        print(f"  风声: {random.choice(sounds['whoosh'])}")
        print(f"  金属声: {random.choice(sounds['metal'])}")
    except Exception as e:
        print(f"✗ 生成失败: {e}")
    
    print("\n测试5: 具体化抽象短语")
    try:
        phrases = ['激烈战斗', '对方出一招', '打得很快', '很重的攻击']
        for phrase in phrases:
            concrete = generator.concretize_fight_phrase(phrase)
            print(f"  {phrase} -> {concrete}")
    except Exception as e:
        print(f"✗ 具体化失败: {e}")
    
    print("\n" + "=" * 60)
    print("打斗场景生成模块测试完成")
    print("=" * 60)


if __name__ == "__main__":
    test_fight_scene_generator()
