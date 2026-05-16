"""
文风特征提取模块 - 核心去AI化模块
负责提取原文的写作风格特征，确保仿写作品保持原风格
"""
import re
from typing import List, Dict, Tuple, Optional, Any, Set
from dataclasses import dataclass, field
from collections import Counter, defaultdict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class WritingStyle:
    """写作风格"""
    name: str
    value: float
    examples: List[str]

@dataclass
class PhrasePattern:
    """短语模式"""
    pattern: str
    frequency: int
    examples: List[str]

@dataclass
class SentencePattern:
    """句子模式"""
    pattern_type: str
    avg_length: float
    structure: str
    examples: List[str]

@dataclass
class NarrativeVoice:
    """叙事声音"""
    perspective: str
    tone: str
    formality: float
    characteristics: List[str]

@dataclass
class StyleFeatures:
    """完整风格特征"""
    writing_styles: List[WritingStyle]
    phrase_patterns: List[PhrasePattern]
    sentence_patterns: List[SentencePattern]
    narrative_voice: NarrativeVoice
    ai_indicators: List[str]
    unique_expressions: Dict[str, int]
    taboo_phrases: List[str]

class StyleFeatureExtractor:
    """文风特征提取器"""
    
    def __init__(self, config: Optional[Any] = None):
        self.config = config
        self.ai_phrase_library = self._init_ai_phrases()
        self.concrete_action_words = self._init_concrete_actions()
        self.slang_patterns = self._init_slang_patterns()
    
    def _init_ai_phrases(self) -> Set[str]:
        """初始化AI特征短语库"""
        return {
            '首先', '其次', '最后', '综上所述', '值得注意的是',
            '从某种意义上说', '可以说', '在这个时代', '在这个背景下',
            '不得不说', '事实上', '实际上', '客观来说', '主观而言',
            '一般来说', '通常情况下', '往往', '往往会是', '大多数情况下',
            '这就意味着', '因此', '所以', '由此可见', '综上所述',
            '总而言之', '简而言之', '一言以蔽之', '归根结底',
            '值得注意的是', '需要指出的是', '必须承认',
            '毫无疑问', '不言而喻', '毫无疑问地',
            '与此同时', '与此同时的', '在此基础上',
            '随着时代的发展', '在当代社会', '在现代社会中',
            '从历史的角度看', '从全局来看', '从长远来看'
        }
    
    def _init_concrete_actions(self) -> Dict[str, List[str]]:
        """初始化具体动作词库"""
        return {
            'hand_actions': [
                '握紧', '松开', '举起', '放下', '挥动', '拍打', '揉搓',
                '抚摸', '抓紧', '捏住', '攥紧', '扣住', '搭上', '按在'
            ],
            'body_actions': [
                '转身', '后退', '前冲', '跃起', '蹲下', '倒下', '扑倒',
                '踉跄', '踉跄后退', '猛地站起', '一屁股坐在'
            ],
            'facial_actions': [
                '皱起眉头', '瞪大眼睛', '咬紧牙关', '嘴角上扬', '嘴角抽搐',
                '眼神一凝', '目光闪烁', '脸色一变', '面沉如水', '面露喜色'
            ],
            'foot_actions': [
                '跺脚', '踢腿', '后退一步', '上前一步', '踏出一步',
                '脚下一滑', '脚跟一蹬', '脚尖一点', '步履蹒跚'
            ]
        }
    
    def _init_slang_patterns(self) -> Dict[str, List[str]]:
        """初始化俚语模式"""
        return {
            'first_person': ['老子', '爷', '本少爷', '本大爷', '小爷', '洒家', '俺', '咱'],
            'emotions': ['妈的', '他妈的', '操', '靠', '卧槽', '我靠', '他丫的', '娘的'],
            'contempt': ['切', '呸', '嘁', '滚蛋', '王八蛋', '龟儿子', '狗东西'],
            'praise': ['牛逼', '厉害', '牛逼哄哄', '吊炸天', '666', '真他妈强'],
            'casual': ['搞起', '整起来', '搞事情', '搞毛', '啥玩意', '咋回事', '咋整']
        }
    
    def extract_features(self, content: str, chapters: Optional[List[Any]] = None) -> StyleFeatures:
        """提取完整风格特征"""
        logger.info("开始提取文风特征")
        
        writing_styles = self._extract_writing_styles(content)
        phrase_patterns = self._extract_phrase_patterns(content)
        sentence_patterns = self._extract_sentence_patterns(content)
        narrative_voice = self._extract_narrative_voice(content)
        ai_indicators = self._find_ai_indicators(content)
        unique_expressions = self._extract_unique_expressions(content)
        taboo_phrases = self._find_taboos(content)
        
        features = StyleFeatures(
            writing_styles=writing_styles,
            phrase_patterns=phrase_patterns,
            sentence_patterns=sentence_patterns,
            narrative_voice=narrative_voice,
            ai_indicators=ai_indicators,
            unique_expressions=unique_expressions,
            taboo_phrases=taboo_phrases
        )
        
        logger.info(f"风格特征提取完成: {len(writing_styles)}种风格, {len(phrase_patterns)}个短语模式")
        return features
    
    def _extract_writing_styles(self, content: str) -> List[WritingStyle]:
        """提取写作风格"""
        logger.info("提取写作风格")
        
        styles = []
        
        action_density = self._calculate_action_density(content)
        styles.append(WritingStyle(
            name='action_density',
            value=action_density,
            examples=self._find_action_examples(content, 3)
        ))
        
        dialogue_density = self._calculate_dialogue_density(content)
        styles.append(WritingStyle(
            name='dialogue_density',
            value=dialogue_density,
            examples=self._find_dialogue_examples(content, 3)
        ))
        
        description_style = self._analyze_description_style(content)
        styles.append(WritingStyle(
            name='description_style',
            value=description_style,
            examples=[]
        ))
        
        emotional_expression = self._analyze_emotional_expression(content)
        styles.append(WritingStyle(
            name='emotional_expression',
            value=emotional_expression,
            examples=self._find_emotion_examples(content, 3)
        ))
        
        pacing_style = self._analyze_pacing_style(content)
        styles.append(WritingStyle(
            name='pacing_style',
            value=pacing_style,
            examples=[]
        ))
        
        return styles
    
    def _calculate_action_density(self, content: str) -> float:
        """计算动作密度"""
        all_actions = []
        for actions in self.concrete_action_words.values():
            all_actions.extend(actions)
        
        action_count = sum(content.count(action) for action in all_actions)
        
        return action_count / max(len(content) / 1000, 1)
    
    def _calculate_dialogue_density(self, content: str) -> float:
        """计算对话密度"""
        dialogue_marks = ['"', '"', '"', '"', '：', ':', '说道', '说道：', '问道：', '答曰']
        dialogue_count = sum(content.count(mark) for mark in dialogue_marks)
        
        sentences = len(re.findall(r'[。！？]', content))
        
        return dialogue_count / max(sentences, 1) * 100
    
    def _analyze_description_style(self, content: str) -> float:
        """分析描写风格"""
        adjectives = len(re.findall(r'[的]、[的]', content))
        concrete_details = len(re.findall(r'(?:只见|但见|只见那|那|一)', content))
        
        if adjectives == 0:
            return 0.5
        
        return concrete_details / (adjectives + concrete_details)
    
    def _analyze_emotional_expression(self, content: str) -> float:
        """分析情感表达方式"""
        direct_emotions = sum(1 for word in ['高兴', '悲伤', '愤怒', '害怕', '开心', '难过'] if word in content)
        implied_emotions = sum(1 for word in ['脸色', '眼神', '表情', '身体'] if word in content)
        
        total = direct_emotions + implied_emotions
        if total == 0:
            return 0.5
        
        return implied_emotions / total
    
    def _analyze_pacing_style(self, content: str) -> float:
        """分析节奏风格"""
        short_sentences = len(re.findall(r'[^。？！]{1,20}[。？！]', content))
        long_sentences = len(re.findall(r'[^。？！]{100,}[。？！]', content))
        
        total = short_sentences + long_sentences
        if total == 0:
            return 0.5
        
        return short_sentences / total
    
    def _find_action_examples(self, content: str, count: int) -> List[str]:
        """查找动作示例"""
        examples = []
        all_actions = []
        for actions in self.concrete_action_words.values():
            all_actions.extend(actions)
        
        for action in all_actions:
            pattern = rf'.{{0,20}}{action}.{{0,20}}'
            for match in re.finditer(pattern, content):
                if len(match.group(0)) > 10:
                    examples.append(match.group(0))
                    if len(examples) >= count:
                        return examples
        
        return examples[:count]
    
    def _find_dialogue_examples(self, content: str, count: int) -> List[str]:
        """查找对话示例"""
        examples = []
        patterns = [
            r'["""].{5,50}["""]',
            r'(?:说道|问道|答道)[：:]?\s*["""].{5,50}["""]',
            r'(?:说|问|答)[：:]?\s*["""].{5,50}["""]'
        ]
        
        for pattern in patterns:
            for match in re.finditer(pattern, content):
                examples.append(match.group(0))
                if len(examples) >= count:
                    return examples
        
        return examples[:count]
    
    def _find_emotion_examples(self, content: str, count: int) -> List[str]:
        """查找情感表达示例"""
        examples = []
        patterns = [
            r'(?:脸色|表情|眼神|眼神中)[^.。！？]{5,30}[。！？]',
            r'(?:紧张|害怕|高兴|悲伤|愤怒)[^.。！？]{5,30}[。！？]',
            r'(?:手|脚|身体)[^.。！？]{5,30}[。！？]'
        ]
        
        for pattern in patterns:
            for match in re.finditer(pattern, content):
                examples.append(match.group(0))
                if len(examples) >= count:
                    return examples
        
        return examples[:count]
    
    def _extract_phrase_patterns(self, content: str) -> List[PhrasePattern]:
        """提取短语模式"""
        logger.info("提取短语模式")
        
        patterns_data = []
        
        phrase_patterns = [
            (r'(?:只见|但见|但看)[^，。]{10,30}', 'observational'),
            (r'(?:突然|忽然|猛地)[^，。]{5,20}', 'sudden'),
            (r'(?:那|这)[^，。]{5,15}(?:人|物|事|地方)', 'reference'),
            (r'(?:于是|然后|接着)[^，。]{5,20}', 'sequence'),
            (r'(?:只|却|竟|偏|偏要)[^，。]{5,20}', 'emphasis'),
        ]
        
        for pattern, pattern_type in phrase_patterns:
            matches = re.findall(pattern, content)
            if matches:
                phrase = PhrasePattern(
                    pattern=pattern_type,
                    frequency=len(matches),
                    examples=matches[:5]
                )
                patterns_data.append(phrase)
        
        return patterns_data
    
    def _extract_sentence_patterns(self, content: str) -> List[SentencePattern]:
        """提取句子模式"""
        logger.info("提取句子模式")
        
        patterns = []
        
        short_pattern = r'[^。？！]{1,30}[。？！]'
        medium_pattern = r'[^。？！]{31,80}[。？！]'
        long_pattern = r'[^。？！]{81,}[。？！]'
        
        short_sentences = re.findall(short_pattern, content)
        medium_sentences = re.findall(medium_pattern, content)
        long_sentences = re.findall(long_pattern, content)
        
        if short_sentences:
            patterns.append(SentencePattern(
                pattern_type='short',
                avg_length=sum(len(s) for s in short_sentences) / len(short_sentences),
                structure='简洁有力',
                examples=short_sentences[:3]
            ))
        
        if medium_sentences:
            patterns.append(SentencePattern(
                pattern_type='medium',
                avg_length=sum(len(s) for s in medium_sentences) / len(medium_sentences),
                structure='平衡叙事',
                examples=medium_sentences[:3]
            ))
        
        if long_sentences:
            patterns.append(SentencePattern(
                pattern_type='long',
                avg_length=sum(len(s) for s in long_sentences) / len(long_sentences),
                structure='详细描写',
                examples=long_sentences[:3]
            ))
        
        return patterns
    
    def _extract_narrative_voice(self, content: str) -> NarrativeVoice:
        """提取叙事声音"""
        logger.info("提取叙事声音")
        
        first_person_count = sum(content.count(word) for word in self.slang_patterns['first_person'])
        third_person_count = content.count('他') + content.count('她')
        
        if first_person_count > third_person_count * 0.1:
            perspective = 'first_person'
        else:
            perspective = 'third_person'
        
        formal_marks = ['因此', '然而', '但是', '不过', '然而']
        informal_marks = ['老子', '妈的', '操', '靠', '卧槽']
        
        formal_count = sum(content.count(mark) for mark in formal_marks)
        informal_count = sum(content.count(mark) for mark in informal_marks)
        
        formality = formal_count / max(formal_count + informal_count, 1)
        
        if informal_count > formal_count * 2:
            tone = 'casual'
        elif formal_count > informal_count * 2:
            tone = 'formal'
        else:
            tone = 'mixed'
        
        characteristics = []
        if informal_count > 10:
            characteristics.append('大量口语化表达')
        if first_person_count > 5:
            characteristics.append('直接的人物内心独白')
        if content.count('"') > 10:
            characteristics.append('丰富的对话描写')
        
        return NarrativeVoice(
            perspective=perspective,
            tone=tone,
            formality=formality,
            characteristics=characteristics
        )
    
    def _find_ai_indicators(self, content: str) -> List[str]:
        """查找AI指示词"""
        logger.info("查找AI指示词")
        
        found_indicators = []
        
        for phrase in self.ai_phrase_library:
            count = content.count(phrase)
            if count > 0:
                found_indicators.append(f"{phrase} (出现{count}次)")
        
        ai_structure_patterns = [
            r'第一[、，](?:首先|第一)',
            r'第二[、，](?:其次|第二)',
            r'第三[、，](?:最后|第三)',
            r'综上所述[，\.]',
            r'总而言之[，\.]',
            r'总得来说[，\.]'
        ]
        
        for pattern in ai_structure_patterns:
            if re.search(pattern, content):
                found_indicators.append(f"结构化表达: {pattern}")
        
        return found_indicators
    
    def _extract_unique_expressions(self, content: str) -> Dict[str, int]:
        """提取独特表达"""
        logger.info("提取独特表达")
        
        expressions = {}
        
        unique_patterns = [
            r'(?:只见|但见|但看|忽见)[^\n]{5,30}',
            r'(?:那人|那物|那处|那事)[^\n]{5,30}',
            r'(?:猛然|陡然|骤然|猝然|忽然)[^\n]{5,20}',
            r'(?:不由得|不由得|忍不住)[^\n]{5,20}'
        ]
        
        for pattern in unique_patterns:
            matches = re.findall(pattern, content)
            for match in matches[:10]:
                if len(match) > 5:
                    expressions[match] = expressions.get(match, 0) + 1
        
        return dict(sorted(expressions.items(), key=lambda x: x[1], reverse=True)[:20])
    
    def _find_taboos(self, content: str) -> List[str]:
        """查找禁忌语/脏话"""
        logger.info("查找禁忌语")
        
        taboo_found = []
        
        for category, words in self.slang_patterns.items():
            for word in words:
                if word in content:
                    taboo_found.append(word)
        
        return list(set(taboo_found))
    
    def generate_style_guide(self, features: StyleFeatures) -> str:
        """生成风格指南"""
        guide_parts = []
        
        guide_parts.append("=" * 50)
        guide_parts.append("文风特征指南")
        guide_parts.append("=" * 50)
        
        guide_parts.append("\n一、写作风格:")
        for style in features.writing_styles:
            guide_parts.append(f"  - {style.name}: {style.value:.2f}")
        
        guide_parts.append("\n二、短语模式:")
        for pattern in features.phrase_patterns:
            guide_parts.append(f"  - {pattern.pattern}: {pattern.frequency}次")
        
        guide_parts.append("\n三、叙事声音:")
        guide_parts.append(f"  - 人称: {features.narrative_voice.perspective}")
        guide_parts.append(f"  - 语气: {features.narrative_voice.tone}")
        guide_parts.append(f"  - 正式度: {features.narrative_voice.formality:.2f}")
        guide_parts.append(f"  - 特征: {', '.join(features.narrative_voice.characteristics)}")
        
        guide_parts.append("\n四、AI特征词（需避免）:")
        for indicator in features.ai_indicators[:10]:
            guide_parts.append(f"  - {indicator}")
        
        guide_parts.append("\n五、独特表达:")
        for expr, count in list(features.unique_expressions.items())[:10]:
            guide_parts.append(f"  - {expr}: {count}次")
        
        guide_parts.append("\n六、禁忌语:")
        for taboo in features.taboo_phrases[:10]:
            guide_parts.append(f"  - {taboo}")
        
        guide_parts.append("\n" + "=" * 50)
        
        return '\n'.join(guide_parts)
    
    def check_de_ai_score(self, text: str) -> float:
        """检查去AI化程度"""
        score = 100.0
        
        for phrase in self.ai_phrase_library:
            count = text.count(phrase)
            if count > 0:
                score -= count * 5
        
        if re.search(r'第一[、，](?:首先|第一)', text):
            score -= 15
        if re.search(r'第二[、，](?:其次|第二)', text):
            score -= 15
        if re.search(r'第三[、，](?:最后|第三)', text):
            score -= 15
        
        ai_structures = ['综上所述', '总而言之', '总得来说']
        for struct in ai_structures:
            if struct in text:
                score -= 10
        
        score = max(score, 0)
        
        return score


def test_style_feature_extraction():
    """测试风格特征提取"""
    print("=" * 60)
    print("文风特征提取模块测试")
    print("=" * 60)
    
    extractor = StyleFeatureExtractor()
    
    test_content = """
    清晨的阳光洒落在青云山上，只见云雾缭绕，宛如仙境。
    
    李云站在山巅，老子心中豪情万丈。
    
    "师父，今天的修炼要做什么？"李云问道。
    
    清风真人捋了捋胡须，笑道："今日你便随为师前往天元城历练。"
    
    突然，一道黑影从林中窜出！
    
    "小心！"李云大喝一声，拔剑而起。
    
    只见那黑影手中持着一把弯刀，直取李云要害。
    
    李云不由得心中一紧，但他没有退缩。
    
    两人交手数十招，不分胜负。
    
    "你是谁？妈的，为何在此埋伏？"李云怒道。
    
    那人不答，只是招招狠辣，刀刀致命。
    
    战斗越来越激烈，李云渐渐感到吃力。
    
    就在这时，清风真人出手了！
    
    一道剑光闪过，那黑衣人应声倒地。
    
    首先，我们要明白修炼的重要性。
    
    其次，修炼需要坚持不懈。
    
    最后，修炼必须要有坚定的信念。
    
    综上所述，修炼是人生最重要的事情。
    
    李云擦了擦额头的汗水："多谢师父相救。"
    
    两人继续向天元城进发。
    """
    
    print("\n测试1: 完整风格特征提取")
    try:
        features = extractor.extract_features(test_content)
        print(f"✓ 提取成功")
        print(extractor.generate_style_guide(features))
    except Exception as e:
        print(f"✗ 提取失败: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n测试2: AI特征词检测")
    try:
        ai_indicators = extractor._find_ai_indicators(test_content)
        print(f"✓ 检测成功，找到 {len(ai_indicators)} 个AI特征词")
        for indicator in ai_indicators:
            print(f"  - {indicator}")
    except Exception as e:
        print(f"✗ 检测失败: {e}")
    
    print("\n测试3: 去AI化评分")
    try:
        score = extractor.check_de_ai_score(test_content)
        print(f"✓ 评分成功: {score:.2f}/100")
        
        clean_content = test_content.replace('首先，我们要明白修炼的重要性。', '').replace('其次，修炼需要坚持不懈。', '').replace('最后，修炼必须要有坚定的信念。', '').replace('综上所述，修炼是人生最重要的事情。', '')
        clean_score = extractor.check_de_ai_score(clean_content)
        print(f"✓ 清理后评分: {clean_score:.2f}/100")
    except Exception as e:
        print(f"✗ 评分失败: {e}")
    
    print("\n测试4: 独特表达提取")
    try:
        expressions = extractor._extract_unique_expressions(test_content)
        print(f"✓ 提取成功，找到 {len(expressions)} 个独特表达")
        for expr, count in list(expressions.items())[:5]:
            print(f"  - {expr}: {count}次")
    except Exception as e:
        print(f"✗ 提取失败: {e}")
    
    print("\n" + "=" * 60)
    print("文风特征提取模块测试完成")
    print("=" * 60)


if __name__ == "__main__":
    test_style_feature_extraction()
