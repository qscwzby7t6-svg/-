"""
人物分析模块 - 负责分析小说中的人物性格、成长线、关系网络
"""
import re
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass, field
from collections import defaultdict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class CharacterTrait:
    """人物特征"""
    name: str
    trait_type: str
    description: str
    evidence: List[str]
    chapter: int

@dataclass
class CharacterGrowth:
    """人物成长"""
    stage: str
    chapter: int
    description: str
    power_change: str
    mental_change: str

@dataclass
class CharacterRelationship:
    """人物关系"""
    from_char: str
    to_char: str
    relationship_type: str
    description: str
    evidence: str
    is_key: bool = False

@dataclass
class Character:
    """人物"""
    name: str
    alias: List[str]
    gender: str
    age: str
    occupation: str
    faction: str
    power_level: str
    personality_traits: List[CharacterTrait]
    growth_stages: List[CharacterGrowth]
    goals: List[str]
    fears: List[str]
    first_appearance: int
    importance: str

class CharacterAnalyzer:
    """人物分析器"""
    
    def __init__(self, config: Optional[Any] = None):
        self.config = config
        self.personality_keywords = self._init_personality_keywords()
        self.relationship_keywords = self._init_relationship_keywords()
    
    def _init_personality_keywords(self) -> Dict[str, List[str]]:
        """初始化性格关键词"""
        return {
            'brave': ['勇敢', '无畏', '胆大', '豪胆', '敢于', '勇猛'],
            'cunning': ['狡猾', '奸诈', '阴险', '诡计多端', '心机深沉'],
            'kind': ['善良', '仁慈', '好心', '心善', '温柔', '温和'],
            'cold': ['冷漠', '冷酷', '冰冷', '冷淡', '冷血', '无情'],
            'proud': ['骄傲', '自负', '傲慢', '高傲', '自傲', '狂妄'],
            'humble': ['谦虚', '谦逊', '低调', '谦和', '不骄不躁'],
            'loyal': ['忠诚', '忠心', '忠义', '可靠', '可信', '值得信赖'],
            'treacherous': ['背叛', '叛徒', '叛变', '出卖', '背信弃义'],
            'wise': ['聪明', '睿智', '智慧', '精明', '机智', '狡黠'],
            'foolish': ['愚蠢', '傻', '笨蛋', '无知', '天真', '单纯'],
            'violent': ['暴躁', '易怒', '冲动', '鲁莽', '粗暴', '凶残'],
            'patient': ['耐心', '沉稳', '冷静', '镇定', '稳重', '冷静沉着'],
            'ambitious': ['野心', '雄心', '志向', '抱负', '不甘平凡'],
            'caring': ['关心', '关怀', '体贴', '在乎', '关爱', '呵护']
        }
    
    def _init_relationship_keywords(self) -> Dict[str, List[str]]:
        """初始化关系关键词"""
        return {
            'master_disciple': ['师徒', '师父', '师傅', '弟子', '徒弟', '师门'],
            'parent_child': ['父亲', '母亲', '父亲', '爹', '娘', '父亲', '子女', '儿子', '女儿', '爹娘'],
            'sibling': ['兄弟', '兄妹', '姐妹', '兄长', '弟弟', '姐姐', '妹妹'],
            'friend': ['朋友', '好友', '挚友', '兄弟', '闺蜜'],
            'enemy': ['敌人', '仇人', '仇敌', '死敌', '宿敌'],
            'lover': ['爱人', '恋人', '情侣', '道侣', '伴侣', '配偶'],
            'senior': ['前辈', '长老', '师兄', '师姐', '学长'],
            'junior': ['后辈', '晚辈', '师弟', '师妹', '学弟'],
            'master_servant': ['主仆', '主人', '仆人', '随从', '侍从'],
            'rival': ['对手', '竞争者', '竞争', '较量'],
            'alliance': ['盟友', '同盟', '联盟', '盟友', '伙伴'],
            'family': ['家族', '族人', '宗族', '血亲']
        }
    
    def analyze(self, content: str, chapters: Optional[List[Any]] = None) -> List[Character]:
        """分析所有人物"""
        logger.info("开始分析人物")
        
        character_data = self.extract_character_base_info(content, chapters)
        characters = []
        
        for name, data in character_data.items():
            personality = self.analyze_personality(content, name, data.get('alias', []))
            growth = self.analyze_growth(content, name, chapters)
            goals, fears = self.analyze_motivation(content, name)
            
            character = Character(
                name=name,
                alias=data.get('alias', []),
                gender=data.get('gender', 'unknown'),
                age=data.get('age', 'unknown'),
                occupation=data.get('occupation', 'unknown'),
                faction=data.get('faction', 'unknown'),
                power_level=data.get('power_level', 'unknown'),
                personality_traits=personality,
                growth_stages=growth,
                goals=goals,
                fears=fears,
                first_appearance=data.get('first_chapter', 0),
                importance=data.get('importance', 'secondary')
            )
            characters.append(character)
        
        characters.sort(key=lambda x: (
            {'protagonist': 0, 'major': 1, 'secondary': 2, 'minor': 3}.get(x.importance, 4),
            x.first_appearance
        ))
        
        logger.info(f"人物分析完成，找到 {len(characters)} 个人物")
        return characters
    
    def extract_character_base_info(self, content: str, chapters: Optional[List[Any]] = None) -> Dict[str, Dict]:
        """提取人物基础信息"""
        logger.info("提取人物基础信息")
        
        character_data = {}
        
        name_patterns = [
            r'([^\s，。,]{2,4})\s*（([^）]+)）',
            r'([^\s，。,]{2,4})\s*[,，]\s*(?:一个|名叫|叫|是)(?:个?|位|名)',
            r'主角(?:叫|名|叫做|是)([^\s，。,]{2,4})',
            r'主角([^\s，。,]{2,4})(?:是|叫|名)',
        ]
        
        for pattern in name_patterns:
            for match in re.finditer(pattern, content):
                name = match.group(1)
                if len(name) >= 2 and name not in ['一个', '这个', '那个人', '主角']:
                    alias = [match.group(2)] if match.lastindex >= 2 and match.group(2) else []
                    
                    if name not in character_data:
                        character_data[name] = {
                            'alias': alias,
                            'first_chapter': 0,
                            'importance': 'minor',
                            'appearance_count': 0
                        }
                    
                    character_data[name]['appearance_count'] += 1
                    
                    if chapters:
                        for i, chapter in enumerate(chapters[:20]):
                            chapter_text = chapter.content if hasattr(chapter, 'content') else str(chapter)
                            if name in chapter_text and character_data[name]['first_chapter'] == 0:
                                character_data[name]['first_chapter'] = i + 1
                                break
        
        protagonist_keywords = ['主角', '主人公', '男主', '女主', '李云', '张小凡', '萧炎', '唐三']
        for name, data in character_data.items():
            if any(keyword in name for keyword in protagonist_keywords) or data['appearance_count'] > 50:
                data['importance'] = 'protagonist'
            elif data['appearance_count'] > 20:
                data['importance'] = 'major'
            elif data['appearance_count'] > 5:
                data['importance'] = 'secondary'
            else:
                data['importance'] = 'minor'
        
        gender_patterns = {
            'male': ['他', '他的', '他是一个', '他是', '男子', '男人', '少男', '少年', '青年'],
            'female': ['她', '她的', '她是一个', '她是', '女子', '女人', '少女', '姑娘', '美女']
        }
        
        for name, data in character_data.items():
            gender_counts = {'male': 0, 'female': 0}
            for gender, patterns in gender_patterns.items():
                for pattern in patterns:
                    gender_counts[gender] += content.count(f'{name}{pattern}')
            
            if gender_counts['male'] > gender_counts['female']:
                data['gender'] = 'male'
            elif gender_counts['female'] > gender_counts['male']:
                data['gender'] = 'female'
            else:
                data['gender'] = 'unknown'
        
        return character_data
    
    def analyze_personality(self, content: str, name: str, alias: List[str]) -> List[CharacterTrait]:
        """分析人物性格"""
        logger.info(f"分析人物性格: {name}")
        
        traits = []
        all_names = [name] + alias
        
        for trait_type, keywords in self.personality_keywords.items():
            evidence = []
            
            for n in all_names:
                for keyword in keywords:
                    pattern = rf'{n}.{{0,20}}{keyword}|{keyword}.{{0,20}}{n}'
                    matches = re.findall(pattern, content)
                    evidence.extend(matches[:3])
            
            if evidence:
                trait = CharacterTrait(
                    name=trait_type,
                    trait_type=self._get_trait_category(trait_type),
                    description=self._get_trait_description(trait_type),
                    evidence=evidence[:5],
                    chapter=0
                )
                traits.append(trait)
        
        return traits
    
    def _get_trait_category(self, trait: str) -> str:
        """获取特征类别"""
        categories = {
            'brave': '行为特征', 'cunning': '行为特征', 'kind': '行为特征',
            'cold': '性格特征', 'proud': '性格特征', 'humble': '性格特征',
            'loyal': '品质特征', 'treacherous': '品质特征',
            'wise': '智慧特征', 'foolish': '智慧特征',
            'violent': '情绪特征', 'patient': '情绪特征',
            'ambitious': '志向特征', 'caring': '情感特征'
        }
        return categories.get(trait, '其他特征')
    
    def _get_trait_description(self, trait: str) -> str:
        """获取特征描述"""
        descriptions = {
            'brave': '勇敢无畏，敢于面对困难和危险',
            'cunning': '狡猾奸诈，善于使用计谋',
            'kind': '善良仁慈，待人温和友好',
            'cold': '冷漠无情，对人冷淡疏离',
            'proud': '骄傲自大，瞧不起他人',
            'humble': '谦虚低调，不骄不躁',
            'loyal': '忠诚可靠，值得信赖',
            'treacherous': '背信弃义，可能会背叛',
            'wise': '聪明睿智，能够看清局势',
            'foolish': '天真单纯，容易被骗',
            'violent': '暴躁冲动，容易动怒',
            'patient': '沉稳冷静，遇事不慌',
            'ambitious': '雄心勃勃，有远大志向',
            'caring': '关心他人，在乎身边的人'
        }
        return descriptions.get(trait, '')
    
    def analyze_growth(self, content: str, name: str, chapters: Optional[List[Any]] = None) -> List[CharacterGrowth]:
        """分析人物成长"""
        logger.info(f"分析人物成长: {name}")
        
        growths = []
        
        if not chapters:
            return growths
        
        all_names = [name]
        
        for i, chapter in enumerate(chapters[:30]):
            chapter_text = chapter.content if hasattr(chapter, 'content') else str(chapter)
            
            for n in all_names:
                power_change = self._detect_power_change(chapter_text, n)
                mental_change = self._detect_mental_change(chapter_text, n)
                
                if power_change or mental_change:
                    growth = CharacterGrowth(
                        stage=f"第{i+1}章",
                        chapter=i+1,
                        description=self._summarize_growth(chapter_text, n),
                        power_change=power_change,
                        mental_change=mental_change
                    )
                    growths.append(growth)
        
        return growths
    
    def _detect_power_change(self, text: str, name: str) -> str:
        """检测力量变化"""
        patterns = [
            (r'突破(?:到|至)?(.{2,8})境界', '突破境界'),
            (r'晋升(?:为|到)(.{2,8})', '晋升'),
            (r'实力(?:大进|提升|增强)', '实力提升'),
            (r'领悟(?:了)?(.{2,8})', '获得领悟'),
            (r'修炼(?:成功|完成)', '修炼成功'),
        ]
        
        for pattern, change_type in patterns:
            if re.search(pattern, text):
                match = re.search(pattern, text)
                return f"{change_type}: {match.group(1) if match.lastindex else '新层次'}"
        
        return ""
    
    def _detect_mental_change(self, text: str, name: str) -> str:
        """检测心理变化"""
        patterns = [
            (r'明白了(.{2,20})道理', '明白道理'),
            (r'学会了(.{2,10})', '学会技能/态度'),
            (r'不再(.{2,10})', '改变习惯'),
            (r'变得(.{2,10})', '性格变化'),
        ]
        
        for pattern, change_type in patterns:
            if re.search(pattern, text):
                match = re.search(pattern, text)
                return f"{change_type}: {match.group(1)}"
        
        return ""
    
    def _summarize_growth(self, text: str, name: str) -> str:
        """总结成长"""
        sentences = re.split(r'[。！？]', text)
        relevant = [s for s in sentences if name in s and any(k in s for k in ['成长', '变化', '领悟', '提升', '突破'])]
        
        return relevant[0].strip() if relevant else text[:100]
    
    def analyze_motivation(self, content: str, name: str) -> Tuple[List[str], List[str]]:
        """分析人物动机"""
        logger.info(f"分析人物动机: {name}")
        
        goals = []
        fears = []
        
        goal_patterns = [
            r'(?:想要|希望|渴望|追求|立志)(.{2,20})',
            r'(?:目标是|志向是|梦想是)(.{2,20})',
            r'(?:要|必须|一定)(?:要|会)(.{2,10})',
        ]
        
        for pattern in goal_patterns:
            for match in re.finditer(pattern, content):
                if name in content[max(0, match.start()-50):match.end()+50]:
                    goals.append(match.group(1).strip())
        
        fear_patterns = [
            r'(?:害怕|恐惧|担忧|担心)(.{2,20})',
            r'(?:不想|不愿|不敢)(?:要|做|看到)(.{2,20})',
            r'(?:唯恐|生怕|恐怕)(.{2,20})',
        ]
        
        for pattern in fear_patterns:
            for match in re.finditer(pattern, content):
                if name in content[max(0, match.start()-50):match.end()+50]:
                    fears.append(match.group(1).strip())
        
        return list(set(goals))[:5], list(set(fears))[:5]
    
    def extract_relationships(self, content: str, characters: List[Character]) -> List[CharacterRelationship]:
        """提取人物关系"""
        logger.info("提取人物关系")
        
        relationships = []
        char_names = [c.name for c in characters]
        
        for i, char1 in enumerate(char_names):
            for char2 in char_names[i+1:]:
                rel_type, evidence = self._find_relationship(content, char1, char2)
                
                if rel_type:
                    relationship = CharacterRelationship(
                        from_char=char1,
                        to_char=char2,
                        relationship_type=rel_type,
                        description=self._get_relationship_description(rel_type),
                        evidence=evidence,
                        is_key=True
                    )
                    relationships.append(relationship)
        
        relationships.sort(key=lambda x: x.is_key, reverse=True)
        
        return relationships[:50]
    
    def _find_relationship(self, content: str, name1: str, name2: str) -> Tuple[str, str]:
        """查找两人关系"""
        for rel_type, keywords in self.relationship_keywords.items():
            for keyword in keywords:
                pattern = rf'{name1}.{{0,30}}{keyword}.{{0,30}}{name2}|{name2}.{{0,30}}{keyword}.{{0,30}}{name1}'
                match = re.search(pattern, content)
                if match:
                    return rel_type, match.group(0)[:100]
        
        return "", ""
    
    def _get_relationship_description(self, rel_type: str) -> str:
        """获取关系描述"""
        descriptions = {
            'master_disciple': '师徒关系，师傅传授徒弟功法',
            'parent_child': '父子/母女关系，血缘至亲',
            'sibling': '兄弟姐妹关系，同辈血亲',
            'friend': '朋友关系，互相帮助',
            'enemy': '敌对关系，互相仇视',
            'lover': '恋人关系，感情深厚',
            'senior': '前辈后辈关系，资历高低',
            'junior': '后辈关系，资历较低',
            'master_servant': '主仆关系，服从与服务',
            'rival': '竞争对手，互相较量',
            'alliance': '同盟关系，共同目标',
            'family': '家族关系，同族之人'
        }
        return descriptions.get(rel_type, '未知关系')
    
    def get_character_summary(self, character: Character) -> str:
        """获取人物摘要"""
        summary_parts = []
        
        summary_parts.append(f"姓名: {character.name}")
        if character.alias:
            summary_parts.append(f"别名: {', '.join(character.alias)}")
        
        summary_parts.append(f"性别: {character.gender}")
        summary_parts.append(f"势力: {character.faction}")
        summary_parts.append(f"实力: {character.power_level}")
        
        if character.personality_traits:
            traits = [t.name for t in character.personality_traits[:3]]
            summary_parts.append(f"性格: {', '.join(traits)}")
        
        if character.goals:
            summary_parts.append(f"目标: {', '.join(character.goals[:2])}")
        
        return '\n'.join(summary_parts)


def test_character_analysis():
    """测试人物分析"""
    print("=" * 60)
    print("人物分析模块测试")
    print("=" * 60)
    
    analyzer = CharacterAnalyzer()
    
    test_content = """
    李云（主角），是一个年轻的修仙者，他勇敢无畏，但也有些冲动。
    
    李云的父亲李天是一个强大的修士，已经达到了金丹境界。
    
    李云和他的师父清风真人是师徒关系，清风真人对他悉心教导。
    
    李云有一个好朋友叫张小凡，两人一起在青云门修炼。
    
    李云渴望变得强大，他想要成为最强的修士，打破自己的命运。
    
    李云害怕失去身边的人，尤其是他的师父。
    
    第三章，李云成功突破到筑基境界，实力大进。
    
    第五章，李云的性格变得更加沉稳，不再像以前那样冲动了。
    
    小红是青云门的师姐，她聪明伶俐，待人温柔。
    
    小红和李云是同门师兄妹的关系，经常一起执行任务。
    
    黑风教的长老是一个阴险狡诈的敌人，他多次设计陷害李云。
    """
    
    print("\n测试1: 完整人物分析")
    try:
        characters = analyzer.analyze(test_content)
        print(f"✓ 分析成功，找到 {len(characters)} 个人物")
        
        for char in characters[:3]:
            print(f"\n{char.name} ({char.importance}):")
            print(analyzer.get_character_summary(char))
    except Exception as e:
        print(f"✗ 分析失败: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n测试2: 性格分析")
    try:
        traits = analyzer.analyze_personality(test_content, '李云', ['主角'])
        print(f"✓ 分析成功，找到 {len(traits)} 个性格特征")
        for trait in traits:
            print(f"  - {trait.name}: {trait.description}")
    except Exception as e:
        print(f"✗ 分析失败: {e}")
    
    print("\n测试3: 人物关系提取")
    try:
        from modules.parser import Chapter
        chapters = [Chapter(1, '第一章', test_content, len(test_content), 0, len(test_content))]
        characters = analyzer.analyze(test_content, chapters)
        relationships = analyzer.extract_relationships(test_content, characters)
        print(f"✓ 提取成功，找到 {len(relationships)} 个关系")
        for rel in relationships[:3]:
            print(f"  - {rel.from_char} <-> {rel.to_char}: {rel.relationship_type}")
    except Exception as e:
        print(f"✗ 提取失败: {e}")
    
    print("\n" + "=" * 60)
    print("人物分析模块测试完成")
    print("=" * 60)


if __name__ == "__main__":
    test_character_analysis()
