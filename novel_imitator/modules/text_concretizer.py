"""
文本具体化转换模块 - 将抽象描述转换为具体画面
这是去AI化的核心模块之一
"""
import re
from typing import List, Dict, Tuple, Optional, Any, Set
from dataclasses import dataclass, field
import random
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ConcreteMapping:
    """具体化映射"""
    abstract_word: str
    concrete_expressions: List[str]
    context_type: str
    examples: List[str] = field(default_factory=list)

class TextConcretizer:
    """文本具体化转换器"""
    
    def __init__(self, config: Optional[Any] = None):
        self.config = config
        self.emotion_conversions = self._init_emotion_conversions()
        self.action_conversions = self._init_action_conversions()
        self.description_conversions = self._init_description_conversions()
        self.adjective_equivalent = self._init_adjective_equivalent()
    
    def _init_emotion_conversions(self) -> Dict[str, List[str]]:
        """初始化情感转换"""
        return {
            '紧张': [
                '手足无措地站在那里，双手紧紧地拧着衣角，指关节因用力而泛白',
                '额头渗出细密的汗珠，眼神飘忽不定，喉结上下滚动',
                '声音微微发颤，嘴唇不自觉地抿紧，呼吸变得急促',
                '双腿微微打颤，手指不停地在袖口搓动',
                '脸色苍白，额头上豆大的汗珠一颗颗滚落'
            ],
            '愤怒': [
                '脸色铁青，双拳紧握，指关节咔咔作响，眼中几乎要喷出火来',
                '胸膛剧烈起伏，鼻息粗重如牛，嘴角不停地抽搐',
                '猛地一拍桌子，茶杯震得叮当作响，怒目圆睁',
                '牙关紧咬，腮帮子的肌肉鼓起老高',
                '眼中闪过一丝狠厉，一字一顿地说道'
            ],
            '高兴': [
                '眉开眼笑，嘴角都快咧到耳根，眼角的皱纹都舒展开来',
                '脸上洋溢着藏不住的喜悦，整个人像是年轻了十岁',
                '一蹦三尺高，兴奋得手舞足蹈，嘴里不停地傻笑',
                '乐得合不拢嘴，眼睛眯成了一条缝',
                '心中像是吃了蜜一样甜，脚步都轻快了几分'
            ],
            '悲伤': [
                '眼眶泛红，泪水在眼眶里打转，却倔强地不肯落下',
                '身体微微颤抖，肩膀不停地耸动，终于忍不住放声痛哭',
                '声音哽咽，半天说不出话来，眼泪像断了线的珠子往下掉',
                '心像是被什么东西狠狠揪住，痛得喘不过气来',
                '整个人像是被抽干了力气，一屁股瘫坐在地上'
            ],
            '惊讶': [
                '瞪大了眼睛，嘴巴张成了O形，整个人像是被定住了一样',
                '倒吸一口凉气，背脊发凉，一股寒意从脚底蹿到头顶',
                '脸色瞬间变得煞白，连退三步，差点摔倒在地',
                '瞳孔骤然收缩，瞳孔中倒映出不可思议的画面',
                '脑袋嗡的一声，一片空白，呆呆地站在原地'
            ],
            '害怕': [
                '浑身起满了鸡皮疙瘩，后背凉飕飕的，冷汗湿透了衣衫',
                '双腿发软，像是被灌了铅一样，每一步都迈不动',
                '心跳得像要从嗓子眼里蹦出来，眼睛不敢往那边看',
                '牙齿咯咯作响，整个人抖得像筛糠一样',
                '瞳孔放大，眼睛里满是恐惧，像是被什么吓傻了'
            ],
            '着急': [
                '急得团团转，额头上的青筋都暴了起来',
                '像是热锅上的蚂蚁，急得不知道该往哪走',
                '双手不停地搓着衣角，眉头皱成了川字',
                '急得直跺脚，恨不得长翅膀飞过去',
                '焦躁不安，一刻也停不下来，嘴上起了一圈燎泡'
            ],
            '无奈': [
                '长叹一声，无奈地摇了摇头，眼里满是苦涩',
                '双手一摊，苦笑一声，像是认命了一般',
                '深深地叹了口气，整个人像是被抽空了力气',
                '仰天长叹，眼眶中闪烁着晶莹的泪光',
                '苦笑着摇头，那笑容比哭还难看'
            ],
            '兴奋': [
                '激动得浑身发抖，攥紧拳头，眼中闪烁着狂热的光芒',
                '血液像是沸腾了一样，整个人都亢奋起来',
                '一跃而起，兴奋得不知道说什么好',
                '心中像是有一团火在烧，烧得他坐立不安',
                '激动得手心全是汗，连说话都结巴了'
            ],
            '认真': [
                '两眼紧盯着某处，眉头微皱，一丝不苟',
                '神情专注，仿佛周围的一切都与他无关',
                '全神贯注，连呼吸都放轻了，生怕打扰了什么',
                '一本正经，目不转睛，生怕漏掉任何一个细节',
                '聚精会神，恨不得把眼睛贴上去看'
            ]
        }
    
    def _init_action_conversions(self) -> Dict[str, List[str]]:
        """初始化动作转换"""
        return {
            '看': [
                '目光落在...上，久久不曾移开',
                '眼睛眯成一条缝，上下打量着...',
                '瞪大眼睛，使劲往...处瞧',
                '侧过头，斜着眼睛瞄了一眼...',
                '目不转睛地盯着...，生怕错过什么',
                '定睛一看，这才发现...'
            ],
            '走': [
                '迈开步子，一步一步向...走去',
                '脚尖轻点地面，身形飘向...',
                '大摇大摆地走向...，一副趾高气扬的模样',
                '低着头，深一脚浅一脚地往...挪',
                '三步并作两步，飞快地冲向...',
                '故意放慢脚步，不紧不慢地踱向...'
            ],
            '说': [
                '嘴唇翕动，从牙缝里挤出几个字',
                '清了清嗓子，一字一顿地说道',
                '声音低沉，像是从胸腔里挤出来的',
                '话音刚落，便又噼里啪啦地讲了起来',
                '支支吾吾了半天，终于说出...',
                '深吸一口气，鼓足勇气说道'
            ],
            '想': [
                '心里盘算着...',
                '不由得想起...',
                '在心中反复掂量着...',
                '暗暗思忖道...',
                '脑海中不断浮现出...',
                '不由得陷入沉思...'
            ],
            '站': [
                '稳稳地站在原地，双腿像是在地上扎了根',
                '身体微微前倾，一副随时准备冲出去的架势',
                '靠在墙边，双手抱在胸前',
                '一屁股坐在了地上，再也不想站起来',
                '身子晃了晃，差点没站稳',
                '双腿并拢，挺直腰板，规规矩矩地立在那儿'
            ],
            '坐': [
                '一屁股坐在椅子上，整个人陷了进去',
                '规规矩矩地坐在桌前，腰背挺得笔直',
                '盘腿坐在地上，双手放在膝盖上',
                '歪歪斜斜地靠在椅背上，一副懒散模样',
                '双手撑在桌上，身体微微前倾',
                '侧身坐在床沿，双腿悬空晃悠着'
            ],
            '笑': [
                '嘴角勾起一抹笑意，眼底却透着冷意',
                '笑得合不拢嘴，露出两排白牙',
                '皮笑肉不笑，那笑容让人发毛',
                '忍不住扑哧一声笑了出来',
                '仰头大笑，笑声回荡在屋子里',
                '嘴角微微上扬，露出若有若无的笑意'
            ],
            '哭': [
                '眼泪像断了线的珠子，噼里啪啦往下掉',
                '抽抽噎噎的，肩膀一耸一耸的',
                '咬着嘴唇，硬是没让眼泪掉下来',
                '捂着脸，无声地哭泣',
                '嚎啕大哭，哭得撕心裂肺',
                '眼眶泛红，泪水在眼眶里直打转'
            ]
        }
    
    def _init_description_conversions(self) -> Dict[str, List[str]]:
        """初始化描写转换"""
        return {
            '快': [
                '电光火石间',
                '说时迟那时快',
                '眨眼之间',
                '快得让人看不清',
                '几乎是在一瞬间',
                '比闪电还快'
            ],
            '慢': [
                '慢吞吞地',
                '像蜗牛一样',
                '一步一步地',
                '慢得让人着急',
                '不紧不慢地',
                '慢悠悠地'
            ],
            '强': [
                '实力强得可怕',
                '厉害得离谱',
                '强到没朋友',
                '恐怖如斯',
                '强得令人发指',
                '牛逼哄哄的'
            ],
            '弱': [
                '弱得像只蚂蚁',
                '不堪一击',
                '弱得可怜',
                '弱不禁风',
                '没什么本事',
                '三脚猫功夫'
            ],
            '很热': [
                '热得人直冒汗',
                '像是置身于火炉之中',
                '汗水湿透了衣衫',
                '热得喘不过气来',
                '滚滚热浪扑面而来',
                '连风都是烫的'
            ],
            '很冷': [
                '冷得人直打哆嗦',
                '寒意直往骨头里钻',
                '呼出的气都凝成了白雾',
                '冻得人缩成一团',
                '冷风像刀子一样刮在脸上',
                '浑身起满了鸡皮疙瘩'
            ]
        }
    
    def _init_adjective_equivalent(self) -> Dict[str, List[str]]:
        """初始化形容词替代"""
        return {
            '美丽': ['好看', '漂亮', '俊俏', '清秀', '秀丽', '标致'],
            '高大': ['高挑', '高大', '魁梧', '挺拔', '伟岸', '壮实'],
            '矮小': ['瘦小', '矮小', '单薄', '瘦弱', '矮墩墩', '短小精悍'],
            '快速': ['飞快', '迅速', '快速', '高速', '疾速', '迅猛'],
            '缓慢': ['慢慢', '迟缓', '慢腾腾', '慢悠悠', '磨蹭', '拖沓'],
            '安静': ['寂静', '宁静', '静悄悄', '鸦雀无声', '沉默', '平静'],
            '热闹': ['喧闹', '嘈杂', '喧嚣', '熙熙攘攘', '人声鼎沸', '热闘'],
            '非常好': ['贼好', '倍儿棒', '超赞', '牛逼', '厉害', '绝了'],
            '非常坏': ['贼坏', '坏透了', '缺德', '王八蛋', '不是东西', '坏到骨子里']
        }
    
    def concretize_text(self, text: str, intensity: str = 'medium') -> str:
        """具体化文本"""
        logger.info(f"开始具体化文本，长度: {len(text)}")
        
        result = text
        
        result = self._concretize_emotions(result)
        result = self._concretize_actions(result)
        result = self._concretize_descriptions(result)
        result = self._replace_vague_adjectives(result)
        
        logger.info(f"具体化完成")
        return result
    
    def _concretize_emotions(self, text: str) -> str:
        """具体化情感"""
        result = text
        
        for emotion, expressions in self.emotion_conversions.items():
            pattern = rf'{emotion}'
            
            if re.search(pattern, result):
                concrete = random.choice(expressions)
                result = re.sub(pattern, concrete, result, count=1)
        
        emotion_patterns = [
            (r'很?紧张', self.emotion_conversions['紧张']),
            (r'很?愤怒', self.emotion_conversions['愤怒']),
            (r'很?高兴', self.emotion_conversions['高兴']),
            (r'很?悲伤', self.emotion_conversions['悲伤']),
            (r'很?惊讶', self.emotion_conversions['惊讶']),
            (r'很?害怕', self.emotion_conversions['害怕']),
            (r'很?着急', self.emotion_conversions['着急']),
            (r'很?无奈', self.emotion_conversions['无奈']),
            (r'很?兴奋', self.emotion_conversions['兴奋']),
            (r'很?认真', self.emotion_conversions['认真'])
        ]
        
        for pattern, expressions in emotion_patterns:
            if re.search(pattern, result):
                concrete = random.choice(expressions)
                result = re.sub(pattern, concrete, result, count=1)
        
        return result
    
    def _concretize_actions(self, text: str) -> str:
        """具体化动作"""
        result = text
        
        for action, expressions in self.action_conversions.items():
            pattern = rf'([^\s]{1,4}?)把?(?:眼睛|目光|眼)?{action}([^\s，,。！？]{0,10})'
            
            for match in re.finditer(pattern, result):
                before = match.group(1)
                after = match.group(2)
                
                if len(before) >= 2 and len(before) <= 4:
                    concrete = random.choice(expressions)
                    concrete = concrete.replace('...', after) if '...' in concrete else concrete + after
                    
                    original = match.group(0)
                    if concrete and concrete not in result:
                        result = result.replace(original, concrete, 1)
                        break
        
        return result
    
    def _concretize_descriptions(self, text: str) -> str:
        """具体化描写"""
        result = text
        
        for desc, expressions in self.description_conversions.items():
            if desc in result:
                concrete = random.choice(expressions)
                result = result.replace(desc, concrete, 1)
        
        vague_patterns = [
            (r'很快', ['电光火石间', '眨眼之间', '说时迟那时快']),
            (r'很慢', ['慢吞吞地', '像蜗牛一样', '一步一挪']),
            (r'非常快', ['快得像道闪电', '快得只看见残影', '快到无法想象']),
            (r'非常慢', ['慢得让人急死', '慢得像在爬', '慢得离谱'])
        ]
        
        for pattern, replacements in vague_patterns:
            if re.search(pattern, result):
                concrete = random.choice(replacements)
                result = re.sub(pattern, concrete, result, count=1)
        
        return result
    
    def _replace_vague_adjectives(self, text: str) -> str:
        """替换模糊形容词"""
        result = text
        
        for adj, alternatives in self.adjective_equivalent.items():
            if adj in result:
                replacement = random.choice(alternatives)
                result = result.replace(adj, replacement, 1)
        
        return result
    
    def add_specific_details(self, text: str, detail_type: str = 'all') -> str:
        """添加具体细节"""
        result = text
        
        if detail_type in ['all', 'sight']:
            result = self._add_sight_details(result)
        
        if detail_type in ['all', 'sound']:
            result = self._add_sound_details(result)
        
        if detail_type in ['all', 'touch']:
            result = self._add_touch_details(result)
        
        if detail_type in ['all', 'smell']:
            result = self._add_smell_details(result)
        
        return result
    
    def _add_sight_details(self, text: str) -> str:
        """添加视觉细节"""
        sight_additions = [
            '只见',
            '但见',
            '只见那',
            '定睛一看',
            '映入眼帘的是'
        ]
        
        if len(text) > 50 and not any(word in text[:100] for word in ['只见', '但见', '但看']):
            addition = random.choice(sight_additions)
            sentences = re.split(r'([。！？])', text)
            if len(sentences) > 2:
                insert_pos = len(sentences[0]) + 1
                return text[:insert_pos] + addition + text[insert_pos:]
        
        return text
    
    def _add_sound_details(self, text: str) -> str:
        """添加声音细节"""
        if '砰' in text or '响' in text or '声' in text:
            return text
        
        sound_words = ['哗啦', '噼啪', '嗖', '噗', '嘎吱', '叮当']
        
        if random.random() > 0.7:
            sound = random.choice(sound_words)
            text = text + f'，只听"{sound}"一声，'
        
        return text
    
    def _add_touch_details(self, text: str) -> str:
        """添加触觉细节"""
        touch_phrases = [
            '手上传来一阵刺痛',
            '冰凉的触感从指尖传来',
            '一股暖流涌遍全身',
            '身子不由得打了个寒颤'
        ]
        
        if random.random() > 0.8:
            phrase = random.choice(touch_phrases)
            text = text + phrase
        
        return text
    
    def _add_smell_details(self, text: str) -> str:
        """添加嗅觉细节"""
        smell_phrases = [
            '一股血腥味扑面而来',
            '空气中弥漫着淡淡的清香',
            '刺鼻的臭味让人作呕',
            '焦糊味充斥鼻腔'
        ]
        
        if random.random() > 0.85:
            phrase = random.choice(smell_phrases)
            text = text + phrase
        
        return text
    
    def remove_ai_patterns(self, text: str) -> str:
        """移除AI模式"""
        ai_patterns = [
            (r'首先[，,]', ''),
            (r'其次[，,]', ''),
            (r'最后[，,]', ''),
            (r'综上所述[，\.]', ''),
            (r'总而言之[，\.]', ''),
            (r'值得注意的是[，\.]', ''),
            (r'从某种意义上说[，\.]', ''),
            (r'可以说[，\.]', ''),
            (r'在这个时代[，\.]', ''),
            (r'在这个背景下[，\.]', ''),
            (r'不得不说[，\.]', ''),
            (r'事实上[，\.]', ''),
            (r'实际上[，\.]', ''),
            (r'客观来说[，\.]', ''),
            (r'主观而言[，\.]', ''),
            (r'一般来说[，\.]', ''),
            (r'通常情况下[，\.]', ''),
            (r'往往[是|会]', ''),
            (r'这就意味着[，\.]', ''),
            (r'因此[，\.]', ''),
            (r'所以[，\.]', ''),
            (r'由此可见[，\.]', ''),
            (r'总而言之[，\.]', ''),
            (r'简而言之[，\.]', ''),
            (r'一言以蔽之[，\.]', ''),
            (r'归根结底[，\.]', '')
        ]
        
        result = text
        for pattern, replacement in ai_patterns:
            result = re.sub(pattern, replacement, result)
        
        result = re.sub(r'\s+', ' ', result)
        result = re.sub(r'[，,]+[,，]', ',', result)
        result = re.sub(r'。+', '。', result)
        
        return result.strip()
    
    def batch_concretize(self, texts: List[str], intensity: str = 'medium') -> List[str]:
        """批量具体化"""
        return [self.concretize_text(text, intensity) for text in texts]


def test_text_concretizer():
    """测试文本具体化"""
    print("=" * 60)
    print("文本具体化转换模块测试")
    print("=" * 60)
    
    concretizer = TextConcretizer()
    
    test_texts = [
        "小红很紧张，她站在那里不知所措。",
        "李云很愤怒，他的脸涨得通红。",
        "他很快地跑了过来。",
        "看到这一幕，他很惊讶。",
        "首先，我们要明白这个道理。其次，要付诸行动。最后，才能成功。",
        "美丽的花朵在风中摇曳，她很漂亮。",
        "张三大步走向门口，他的脚步很重。",
        "李四坐在椅子上，眼睛看着远方。",
        "他笑了笑，说出了自己的心里话。",
        "总的来说，这是一件好事。"
    ]
    
    print("\n测试1: 情感具体化")
    try:
        result = concretizer.concretize_emotions("小红很紧张")
        print(f"✓ 情感具体化成功")
        print(f"  原文: 小红很紧张")
        print(f"  结果: {result}")
    except Exception as e:
        print(f"✗ 情感具体化失败: {e}")
    
    print("\n测试2: 完整具体化")
    try:
        for original in test_texts[:5]:
            result = concretizer.concretize_text(original)
            print(f"\n  原文: {original}")
            print(f"  结果: {result}")
    except Exception as e:
        print(f"✗ 具体化失败: {e}")
    
    print("\n测试3: 移除AI模式")
    try:
        ai_text = "首先，我们要明白这个道理。其次，要付诸行动。最后，才能成功。综上所述，这很重要。"
        result = concretizer.remove_ai_patterns(ai_text)
        print(f"✓ 移除AI模式成功")
        print(f"  原文: {ai_text}")
        print(f"  结果: {result}")
    except Exception as e:
        print(f"✗ 移除AI模式失败: {e}")
    
    print("\n测试4: 添加感官细节")
    try:
        text = "战斗结束了。"
        result = concretizer.add_specific_details(text, 'all')
        print(f"✓ 添加感官细节成功")
        print(f"  原文: {text}")
        print(f"  结果: {result}")
    except Exception as e:
        print(f"✗ 添加感官细节失败: {e}")
    
    print("\n测试5: 批量具体化")
    try:
        results = concretizer.batch_concretize(test_texts[:3])
        print(f"✓ 批量具体化成功，处理 {len(results)} 段文本")
        for i, result in enumerate(results):
            print(f"  {i+1}. {result[:50]}...")
    except Exception as e:
        print(f"✗ 批量具体化失败: {e}")
    
    print("\n" + "=" * 60)
    print("文本具体化转换模块测试完成")
    print("=" * 60)


if __name__ == "__main__":
    test_text_concretizer()
