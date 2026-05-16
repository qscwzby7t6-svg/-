"""
脏话处理模块 - 负责在适当场景下添加合适的口语化表达
根据情绪和情境自动选择合适的表达
"""
import re
import random
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SwearWord:
    """脏话词汇"""
    word: str
    intensity: int
    category: str
    context: List[str]

class SwearWordHandler:
    """脏话处理模块"""
    
    def __init__(self, config: Optional[Any] = None):
        self.config = config
        self.swear_library = self._init_swear_library()
        self.context_triggers = self._init_context_triggers()
    
    def _init_swear_library(self) -> Dict[str, List[SwearWord]]:
        """初始化脏话库"""
        return {
            '愤怒': [
                SwearWord('妈的', 2, '口头禅', ['通用']),
                SwearWord('他妈的', 3, '强烈', ['被背叛', '极度愤怒']),
                SwearWord('混账', 3, '斥责', ['骂人']),
                SwearWord('王八蛋', 3, '辱骂', ['敌人']),
                SwearWord('狗东西', 2, '轻蔑', ['敌人']),
                SwearWord('龟儿子', 2, '辱骂', ['骂人']),
                SwearWord('他丫的', 2, '口头禅', ['通用']),
                SwearWord('操', 2, '感叹', ['惊讶']),
                SwearWord('滚蛋', 2, '驱赶', ['愤怒']),
                SwearWord('什么东西', 1, '轻蔑', ['轻蔑']),
                SwearWord('该死', 2, '咒骂', ['愤怒']),
                SwearWord('混蛋', 2, '斥责', ['骂人']),
                SwearWord('杂碎', 3, '极度侮辱', ['敌人']),
                SwearWord('贼子', 2, '古风骂人', ['武侠']),
                SwearWord('竖子', 2, '古风骂人', ['武侠']),
                SwearWord('匹夫', 2, '古风骂人', ['武侠'])
            ],
            '蔑视': [
                SwearWord('切', 1, '不屑', ['轻蔑']),
                SwearWord('呸', 1, '吐口水', ['轻蔑']),
                SwearWord('嘁', 1, '不屑', ['轻蔑']),
                SwearWord('切，有什么了不起', 2, '不服', ['挑衅']),
                SwearWord('就这？', 1, '极度不屑', ['挑衅']),
                SwearWord('小样', 1, '轻视', ['熟悉的人']),
                SwearWord('爷', 1, '自称傲慢', ['傲慢']),
                SwearWord('老子', 1, '自称傲慢', ['傲慢']),
                SwearWord('老子我', 2, '强调傲慢', ['傲慢'])
            ],
            '疼痛': [
                SwearWord('操', 2, '感叹', ['疼痛']),
                SwearWord('妈的', 2, '口头禅', ['疼痛']),
                SwearWord('该死', 2, '咒骂', ['受伤']),
                SwearWord('疼死老子了', 3, '强烈', ['极度疼痛']),
                SwearWord('嘶', 1, '倒吸凉气', ['疼痛']),
                SwearWord('啊', 2, '惨叫', ['剧烈疼痛'])
            ],
            '惊讶': [
                SwearWord('靠', 2, '感叹', ['惊讶']),
                SwearWord('我靠', 2, '感叹', ['惊讶']),
                SwearWord('卧槽', 2, '感叹', ['极度惊讶']),
                SwearWord('卧槽，这也行', 3, '极度惊讶', ['难以置信']),
                SwearWord('我去', 1, '感叹', ['惊讶']),
                SwearWord('真的假的', 1, '疑问', ['质疑']),
                SwearWord('不会吧', 1, '疑问', ['质疑'])
            ],
            '无奈': [
                SwearWord('妈的', 2, '口头禅', ['无奈']),
                SwearWord('真是见了鬼', 2, '无奈', ['无奈']),
                SwearWord('我太难了', 2, '感叹', ['绝望']),
                SwearWord('没办法', 1, '陈述', ['放弃']),
                SwearWord('认命了', 1, '接受', ['放弃']),
                SwearWord('操蛋', 2, '抱怨', ['不满'])
            ],
            '兴奋': [
                SwearWord('牛逼', 3, '赞美', ['兴奋']),
                SwearWord('太他妈爽了', 3, '极度兴奋', ['极度兴奋']),
                SwearWord('干得漂亮', 2, '赞美', ['赞美']),
                SwearWord('厉害了我的哥', 3, '极度赞美', ['极度兴奋']),
                SwearWord('666', 2, '网络用语', ['赞美']),
                SwearWord('碉堡了', 2, '网络用语', ['赞美']),
                SwearWord('吊炸天', 3, '极度赞美', ['极度兴奋'])
            ],
            '疼痛_强烈': [
                SwearWord('妈的，疼死老子了', 4, '极度疼痛', ['剧痛']),
                SwearWord('操，疼死爷了', 4, '极度疼痛', ['剧痛']),
                SwearWord('他妈的，怎么这么疼', 3, '抱怨疼痛', ['受伤']),
                SwearWord('痛死老子了', 3, '强烈', ['受伤'])
            ],
            '得意': [
                SwearWord('那是当然', 1, '自信', ['自信']),
                SwearWord('老子就是牛逼', 3, '极度自信', ['傲慢']),
                SwearWord('洒家', 1, '自称', ['自信']),
                SwearWord('本少爷', 1, '自称', ['傲慢']),
                SwearWord('本大爷', 2, '自称', ['傲慢']),
                SwearWord('爷就是强', 2, '自信', ['自信'])
            ],
            '紧张': [
                SwearWord('妈的，紧张死了', 2, '口头禅', ['紧张']),
                SwearWord('稳住，别慌', 1, '自我安慰', ['紧张']),
                SwearWord('我靠，怎么办', 2, '焦虑', ['紧张']),
                SwearWord('完蛋了', 2, '绝望', ['极度紧张'])
            ],
            '恐惧': [
                SwearWord('我靠，不会吧', 3, '恐惧', ['恐惧']),
                SwearWord('完了完了', 3, '绝望', ['极度恐惧']),
                SwearWord('妈呀', 2, '惊呼', ['害怕']),
                SwearWord('我的妈呀', 2, '惊呼', ['极度害怕']),
                SwearWord('我的天', 1, '感叹', ['惊讶害怕'])
            ]
        }
    
    def _init_context_triggers(self) -> Dict[str, List[str]]:
        """初始化上下文触发器"""
        return {
            '愤怒': ['怒', '气', '火', '恨', '不满', '怨'],
            '蔑视': ['不屑', '轻视', '瞧不起', '看不上'],
            '疼痛': ['疼', '痛', '伤', '流血', '伤口'],
            '惊讶': ['惊', '讶', '没想到', '竟然', '居然'],
            '无奈': ['无能为力', '没办法', '无解', '绝望'],
            '兴奋': ['爽', '高兴', '开心', '痛快', '爽'],
            '疼痛_强烈': ['剧痛', '钻心', '撕裂', '剧痛难忍'],
            '得意': ['得意', '骄傲', '自信', '自豪'],
            '紧张': ['紧张', '心慌', '忐忑', '不安'],
            '恐惧': ['怕', '惧', '恐怖', '可怕', '吓人']
        }
    
    def select_swear_words(self, emotion: str, context: str = "", intensity: int = 2) -> List[str]:
        """根据情绪和上下文选择脏话"""
        logger.info(f"选择脏话: 情绪={emotion}, 上下文={context}")
        
        if emotion not in self.swear_library:
            emotion = self._find_similar_emotion(emotion)
        
        candidates = self.swear_library.get(emotion, [])
        
        if context:
            candidates = [sw for sw in candidates if any(ctx in sw.context for ctx in [context, '通用'])]
        
        selected = [sw for sw in candidates if sw.intensity <= intensity]
        
        if not selected:
            selected = candidates[:2]
        
        return [sw.word for sw in selected[:2]]
    
    def _find_similar_emotion(self, emotion: str) -> str:
        """查找相似情绪"""
        emotion_map = {
            '生气': '愤怒',
            '恼火': '愤怒',
            '气愤': '愤怒',
            '不爽': '愤怒',
            '蔑视': '蔑视',
            '看不起': '蔑视',
            '疼痛': '疼痛',
            '痛': '疼痛',
            '惊讶': '惊讶',
            '吃惊': '惊讶',
            '震惊': '惊讶',
            '无奈': '无奈',
            '无助': '无奈',
            '兴奋': '兴奋',
            '激动': '兴奋',
            '得意': '得意',
            '嘚瑟': '得意',
            '紧张': '紧张',
            '焦急': '紧张',
            '害怕': '恐惧',
            '恐惧': '恐惧',
            '惊恐': '恐惧'
        }
        
        return emotion_map.get(emotion, '愤怒')
    
    def insert_swear_into_dialogue(self, dialogue: str, emotion: str, context: str = "") -> str:
        """在对话中插入脏话"""
        logger.info(f"插入脏话到对话: {dialogue[:30]}...")
        
        swear_words = self.select_swear_words(emotion, context)
        
        if not swear_words:
            return dialogue
        
        swear = random.choice(swear_words)
        
        insert_positions = [
            ('开头', 0),
            ('中间', len(dialogue) // 2),
            ('结尾', len(dialogue))
        ]
        
        position_type, pos = random.choice(insert_positions)
        
        punctuation = ['，', '，', '，', '。', '！']
        punct = random.choice(punctuation)
        
        if position_type == '开头':
            return f"{swear}{punct}{dialogue}"
        elif position_type == '中间':
            return f"{dialogue[:pos]}{swear}{punct}{dialogue[pos:]}"
        else:
            return f"{dialogue}{punct}{swear}"
    
    def replace_emotion_with_swear(self, emotion_text: str) -> str:
        """将情感词替换为脏话"""
        logger.info(f"替换情感词为脏话: {emotion_text[:30]}...")
        
        replacements = {
            '非常生气': '气得直哆嗦',
            '特别愤怒': '怒火中烧',
            '很生气': '气得发抖',
            '非常惊讶': '惊得下巴都快掉了',
            '很惊讶': '惊得一愣一愣的',
            '非常高兴': '高兴得直蹦跶',
            '很高兴': '乐得找不着北'
        }
        
        for emotion, expression in replacements.items():
            if emotion in emotion_text:
                emotion_text = emotion_text.replace(emotion, expression)
        
        return emotion_text
    
    def add_swear_context(self, text: str, emotion: str) -> str:
        """添加脏话上下文"""
        logger.info(f"添加脏话上下文: {text[:30]}...")
        
        swear_words = self.select_swear_words(emotion)
        
        if not swear_words:
            return text
        
        context_patterns = {
            '愤怒': ['不由得{}骂了一句', '气得{}低吼一声', '{}，{}咬牙切齿'],
            '蔑视': ['{}冷笑一声', '{}瞥了一眼', '{}不屑地{}说'],
            '疼痛': ['{}闷哼一声', '{}疼得{}直咧嘴', '{}不由得{}叫出声'],
            '惊讶': ['{}惊呼一声', '{}不由得{}愣住', '{}差点{}没叫出声'],
            '无奈': ['{}无奈地{}叹气', '{}不由得{}苦笑', '{}只能{}摇头']
        }
        
        pattern = context_patterns.get(emotion, ['{}'])
        
        if isinstance(pattern, list):
            pattern = pattern[0]
        
        swear = random.choice(swear_words)
        
        placeholders = pattern.count('{}')
        
        if placeholders == 1:
            context = pattern.format(swear)
        elif placeholders == 2:
            context = pattern.format(swear, random.choice(['不由得', '忍不住', '']))
        else:
            context = pattern.format(swear, random.choice(['不由得', '忍不住', '']), swear)
        
        sentences = re.split(r'[。！？]', text)
        
        if len(sentences) > 1:
            insert_idx = random.randint(0, len(sentences) - 2)
            sentences.insert(insert_idx, context)
            return '。\n'.join(sentences) + '。'
        else:
            return f"{context}，{text}"
    
    def adapt_swear_to_genre(self, text: str, genre: str) -> str:
        """根据类型调整脏话"""
        logger.info(f"根据类型调整脏话: genre={genre}")
        
        genre_specific = {
            'xianxia': {
                '替换': [('妈的', '混账'), ('他妈的', '竖子'), ('老子', '本座'), ('我靠', '这厮')],
                '增加': ['孽障', '竖子', '匹夫', '贼子', '你这小辈']
            },
            'wuxia': {
                '替换': [('妈的', '他妈的'), ('我靠', '这家伙')],
                '增加': ['奶奶的', '直娘贼', '贼厮', '腌臜泼才']
            },
            'urban': {
                '替换': [],
                '增加': ['卧槽', '牛逼', '厉害了我的哥', '666']
            }
        }
        
        genre_rules = genre_specific.get(genre, genre_specific['urban'])
        
        for old, new in genre_rules['替换']:
            text = text.replace(old, new)
        
        if random.random() > 0.7:
            addition = random.choice(genre_rules['增加'])
            text = text + f"，直娘贼"
        
        return text
    
    def batch_process(self, dialogues: List[str], emotions: List[str]) -> List[str]:
        """批量处理对话"""
        logger.info(f"批量处理 {len(dialogues)} 条对话")
        
        results = []
        for dialogue, emotion in zip(dialogues, emotions):
            processed = self.insert_swear_into_dialogue(dialogue, emotion)
            results.append(processed)
        
        return results
    
    def should_add_swear(self, text: str, context: str) -> bool:
        """判断是否应该添加脏话"""
        emotion_keywords = {
            '愤怒': 0.8,
            '蔑视': 0.6,
            '疼痛': 0.7,
            '惊讶': 0.4,
            '无奈': 0.5,
            '兴奋': 0.3,
            '紧张': 0.4,
            '恐惧': 0.5
        }
        
        for emotion, probability in emotion_keywords.items():
            if emotion in context:
                return random.random() < probability
        
        return random.random() < 0.1


def test_swear_word_handler():
    """测试脏话处理"""
    print("=" * 60)
    print("脏话处理模块测试")
    print("=" * 60)
    
    handler = SwearWordHandler()
    
    print("\n测试1: 根据情绪选择脏话")
    try:
        emotions = ['愤怒', '蔑视', '惊讶', '疼痛', '兴奋']
        for emotion in emotions:
            swears = handler.select_swear_words(emotion)
            print(f"  {emotion}: {swears}")
    except Exception as e:
        print(f"✗ 选择失败: {e}")
    
    print("\n测试2: 在对话中插入脏话")
    try:
        dialogues = [
            "你给我等着！",
            "这不可能！",
            "太厉害了！"
        ]
        emotions = ['愤怒', '惊讶', '兴奋']
        
        for dialogue, emotion in zip(dialogues, emotions):
            result = handler.insert_swear_into_dialogue(dialogue, emotion)
            print(f"  {emotion}: \"{dialogue}\" -> \"{result}\"")
    except Exception as e:
        print(f"✗ 插入失败: {e}")
    
    print("\n测试3: 添加脏话上下文")
    try:
        text = "李云冲了上去。"
        emotion = "愤怒"
        result = handler.add_swear_context(text, emotion)
        print(f"  原文: {text}")
        print(f"  结果: {result}")
    except Exception as e:
        print(f"✗ 添加上下文失败: {e}")
    
    print("\n测试4: 根据类型调整脏话")
    try:
        text = "妈的，这家伙真牛逼！"
        genres = ['xianxia', 'wuxia', 'urban']
        for genre in genres:
            result = handler.adapt_swear_to_genre(text, genre)
            print(f"  {genre}: {result}")
    except Exception as e:
        print(f"✗ 调整失败: {e}")
    
    print("\n测试5: 批量处理")
    try:
        dialogues = ["你好啊", "打得好", "疼死我了"]
        emotions = ["友好", "兴奋", "疼痛"]
        results = handler.batch_process(dialogues, emotions)
        for i, result in enumerate(results):
            print(f"  {i+1}. {result}")
    except Exception as e:
        print(f"✗ 批量处理失败: {e}")
    
    print("\n" + "=" * 60)
    print("脏话处理模块测试完成")
    print("=" * 60)


if __name__ == "__main__":
    test_swear_word_handler()
