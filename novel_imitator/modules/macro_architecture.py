"""
宏观架构分析模块 - 负责分析小说的世界观、力量体系、伏笔等宏观元素
"""
import re
from typing import List, Dict, Tuple, Optional, Any, Set
from dataclasses import dataclass, field
from collections import defaultdict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class PowerLevel:
    """力量等级"""
    name: str
    description: str
    characteristics: List[str]
    appeared_in: List[str]

@dataclass
class Faction:
    """势力门派"""
    name: str
    type: str
    members: List[str]
    location: str
    traits: List[str]
    relationship: Dict[str, str]

@dataclass
class WorldRule:
    """世界规则"""
    name: str
    description: str
    examples: List[str]
    importance: str

@dataclass
class Foreshadow:
    """伏笔"""
    text: str
    hint_type: str
    chapter: int
    related_elements: List[str]
    resolved_later: bool = False

@dataclass
class WorldArchitecture:
    """世界架构"""
    power_levels: List[PowerLevel]
    factions: List[Faction]
    world_rules: List[WorldRule]
    foreshadows: List[Foreshadow]
    locations: List[str]
    time_system: str
    cultivation_system: str

class MacroArchitectureAnalyzer:
    """宏观架构分析器"""
    
    def __init__(self, config: Optional[Any] = None):
        self.config = config
        self.cultivation_realms = self._init_cultivation_realms()
        self.common_keywords = self._init_common_keywords()
    
    def _init_cultivation_realms(self) -> Dict[str, List[str]]:
        """初始化修炼境界关键词"""
        return {
            'mortal': ['凡人', '普通人', '常人', '世俗'],
            'qi_refining': ['炼气', '聚气', '凝气', '引气'],
            'foundation': ['筑基', '固本', '培元'],
            'core_formation': ['金丹', '结丹', '凝丹'],
            'nascent': ['元婴', '化神', '出窍'],
            'spirit': ['化虚', '合体', '大乘'],
            'transcendent': ['渡劫', '飞升', '真仙', '天仙'],
            'immortal': ['金仙', '太乙', '大罗', '混元']
        }
    
    def _init_common_keywords(self) -> Dict[str, List[str]]:
        """初始化常见关键词"""
        return {
            'material': ['灵草', '灵药', '灵石', '灵矿', '灵兽', '妖兽', '魔兽'],
            'technique': ['功法', '秘术', '神通', '绝技', '秘法', '心法', '口诀'],
            'item': ['法器', '灵器', '法宝', '灵宝', '仙器', '丹药', '阵图'],
            'location': ['秘境', '遗迹', '洞府', '禁地', '险境', '绝地']
        }
    
    def analyze(self, content: str, chapters: Optional[List[Any]] = None) -> WorldArchitecture:
        """分析宏观架构"""
        logger.info("开始分析宏观架构")
        
        power_levels = self.extract_power_system(content)
        factions = self.extract_factions(content)
        world_rules = self.extract_world_rules(content)
        foreshadows = self.extract_foreshadows(content, chapters)
        locations = self.extract_locations(content)
        time_system = self.analyze_time_system(content)
        cultivation_system = self.analyze_cultivation_system(content)
        
        architecture = WorldArchitecture(
            power_levels=power_levels,
            factions=factions,
            world_rules=world_rules,
            foreshadows=foreshadows,
            locations=locations,
            time_system=time_system,
            cultivation_system=cultivation_system
        )
        
        logger.info(f"宏观架构分析完成: {len(power_levels)}个境界, {len(factions)}个势力, {len(foreshadows)}个伏笔")
        return architecture
    
    def extract_power_system(self, content: str) -> List[PowerLevel]:
        """提取力量体系"""
        logger.info("提取力量体系")
        
        power_levels = []
        found_realms = defaultdict(list)
        
        for realm, keywords in self.cultivation_realms.items():
            for keyword in keywords:
                if keyword in content:
                    found_realms[realm].append(keyword)
        
        realm_order = ['mortal', 'qi_refining', 'foundation', 'core_formation', 
                      'nascent', 'spirit', 'transcendent', 'immortal']
        realm_names = {
            'mortal': '凡人境',
            'qi_refining': '炼气境',
            'foundation': '筑基境',
            'core_formation': '金丹境',
            'nascent': '元婴境',
            'spirit': '化神境',
            'transcendent': '渡劫境',
            'immortal': '真仙境'
        }
        
        for realm in realm_order:
            if realm in found_realms:
                characteristics = self._extract_realm_characteristics(content, found_realms[realm])
                power_level = PowerLevel(
                    name=realm_names[realm],
                    description=self._generate_realm_description(realm),
                    characteristics=characteristics,
                    appeared_in=found_realms[realm]
                )
                power_levels.append(power_level)
        
        return power_levels
    
    def _extract_realm_characteristics(self, content: str, keywords: List[str]) -> List[str]:
        """提取境界特征"""
        characteristics = []
        
        for keyword in keywords[:2]:
            patterns = [
                rf'{keyword}.{{0,50}}(?:可以|能够|拥有|具有|掌握)',
                rf'{keyword}.{{0,50}}(?:灵力|法力|真元|元气)',
                rf'{keyword}.{{0,50}}(?:寿元|寿命|年)'
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, content)
                if matches:
                    characteristics.append(matches[0][:50])
        
        return characteristics[:5]
    
    def _generate_realm_description(self, realm: str) -> str:
        """生成境界描述"""
        descriptions = {
            'mortal': '普通人的境界，没有修炼基础',
            'qi_refining': '初入修炼之门，能够感应灵气',
            'foundation': '奠定修炼根基，可使用法术',
            'core_formation': '丹成之后，实力大增',
            'nascent': '元婴出窍，精神力大幅提升',
            'spirit': '神识化虚，与天地共鸣',
            'transcendent': '渡劫飞升，超凡入圣',
            'immortal': '长生不死，与日月同辉'
        }
        return descriptions.get(realm, '')
    
    def extract_factions(self, content: str) -> List[Faction]:
        """提取势力门派"""
        logger.info("提取势力门派")
        
        faction_patterns = [
            r'([^\s]{2,8})(?:门|派|教|宗|会|盟|帮)\s*(?:是|位于|建立|创建)',
            r'([^\s]{2,8})(?:家族|世家)\s*(?:是|位于|传承)',
            r'([^\s]{2,8})(?:殿|宫|阁|堂|楼)\s*(?:是|位于)',
        ]
        
        factions_dict = {}
        
        for pattern in faction_patterns:
            for match in re.finditer(pattern, content):
                name = match.group(1)
                if len(name) >= 2:
                    faction_type = self._infer_faction_type(name, pattern)
                    factions_dict[name] = {
                        'name': name,
                        'type': faction_type,
                        'members': self._extract_faction_members(content, name),
                        'location': self._extract_faction_location(content, name),
                        'traits': [],
                        'relationship': {}
                    }
        
        factions = []
        for name, data in factions_dict.items():
            faction = Faction(
                name=data['name'],
                type=data['type'],
                members=data['members'],
                location=data['location'],
                traits=data['traits'],
                relationship=data['relationship']
            )
            factions.append(faction)
        
        return factions
    
    def _infer_faction_type(self, name: str, pattern: str) -> str:
        """推断势力类型"""
        if '门' in name:
            return '门派'
        elif '派' in name:
            return '流派'
        elif '教' in name:
            return '教派'
        elif '宗' in name:
            return '宗门'
        elif '会' in name or '盟' in name:
            return '联盟'
        elif '帮' in name:
            return '帮派'
        elif '家族' in name or '世家' in name:
            return '家族'
        elif '殿' in name or '宫' in name:
            return '宫殿'
        else:
            return '其他'
    
    def _extract_faction_members(self, content: str, faction_name: str) -> List[str]:
        """提取势力成员"""
        members = []
        member_patterns = [
            rf'{faction_name}(?:的|所属)([^\s，,]{2,4})',
            rf'([^\s，,]{2,4})(?:是|为)(?:{faction_name}(?:的|所属|之人)|{faction_name}弟子)',
        ]
        
        for pattern in member_patterns:
            matches = re.findall(pattern, content)
            members.extend([m for m in matches if len(m) >= 2])
        
        return list(set(members))[:10]
    
    def _extract_faction_location(self, content: str, faction_name: str) -> str:
        """提取势力位置"""
        patterns = [
            rf'{faction_name}(?:位于|坐落于|建立在)([^\s，。,]{2,10})',
            rf'([^\s，。,]{2,10})(?:的|位于){faction_name}',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content)
            if match:
                return match.group(1)
        
        return "未知"
    
    def extract_world_rules(self, content: str) -> List[WorldRule]:
        """提取世界规则"""
        logger.info("提取世界规则")
        
        rules = []
        
        spirit_patterns = [
            r'天地灵气(?:是|存在于|弥漫于)',
            r'灵气复苏(?:导致|使得)',
            r'修炼(?:需要|依靠|消耗)灵气',
        ]
        
        for pattern in spirit_patterns:
            if re.search(pattern, content):
                rules.append(WorldRule(
                    name='灵气法则',
                    description='世界由灵气构成，修炼者吸收灵气提升实力',
                    examples=self._find_rule_examples(content, pattern),
                    importance='核心'
                ))
                break
        
        karma_patterns = [
            r'(?:因果|业力|报应)',
            r'(?:善有善报|恶有恶报)',
            r'(?:天道轮回)',
        ]
        
        for pattern in karma_patterns:
            if re.search(pattern, content):
                rules.append(WorldRule(
                    name='因果法则',
                    description='世间存在因果报应，善恶终有回报',
                    examples=self._find_rule_examples(content, pattern),
                    importance='重要'
                ))
                break
        
        fate_patterns = [
            r'(?:命运|天命|定数)',
            r'(?:打破命运|逆天改命)',
            r'(?:天意|注定)',
        ]
        
        for pattern in fate_patterns:
            if re.search(pattern, content):
                rules.append(WorldRule(
                    name='命运法则',
                    description='命运既定，但可被打破或改变',
                    examples=self._find_rule_examples(content, pattern),
                    importance='重要'
                ))
                break
        
        return rules
    
    def _find_rule_examples(self, content: str, pattern: str) -> List[str]:
        """查找规则示例"""
        examples = []
        for match in re.finditer(pattern, content):
            start = max(0, match.start() - 50)
            end = min(len(content), match.end() + 50)
            examples.append(content[start:end].strip())
        return examples[:3]
    
    def extract_foreshadows(self, content: str, chapters: Optional[List[Any]] = None) -> List[Foreshadow]:
        """提取伏笔"""
        logger.info("提取伏笔")
        
        foreshadows = []
        hint_patterns = {
            'mystery': [r'(?:似乎|好像|隐隐)(?:预示|暗示|预示着)', r'但不知为何', r'总觉得'],
            'prophecy': [r'(?:预言|预言说|据说)', r'(?:命运|注定|天赋)', r'(?:命定之人|天选之子)'],
            'secret': [r'(?:隐藏着|埋藏着|封印着)', r'(?:不为人知|秘密)', r'(?:古老的|久远的)'],
            'future_event': [r'(?:将来|日后|未来)', r'(?:某一天|终有一天)', r'(?:迟早|早晚)']
        }
        
        chapter_content = content
        if chapters:
            for i, chapter in enumerate(chapters[:5]):
                chapter_text = chapter.content if hasattr(chapter, 'content') else str(chapter)
                
                for hint_type, patterns in hint_patterns.items():
                    for pattern in patterns:
                        for match in re.finditer(pattern, chapter_text):
                            start = max(0, match.start() - 30)
                            end = min(len(chapter_text), match.end() + 30)
                            text = chapter_text[start:end]
                            
                            if len(text) > 10:
                                foreshadows.append(Foreshadow(
                                    text=text,
                                    hint_type=hint_type,
                                    chapter=i + 1,
                                    related_elements=self._find_related_elements(content, text)
                                ))
        
        for hint_type, patterns in hint_patterns.items():
            for pattern in patterns:
                for match in re.finditer(pattern, content):
                    start = max(0, match.start() - 30)
                    end = min(len(content), match.end() + 30)
                    text = content[start:end]
                    
                    if len(text) > 10 and not any(abs(f.start_pos - match.start()) < 20 for f in foreshadows if hasattr(f, 'start_pos')):
                        foreshadows.append(Foreshadow(
                            text=text,
                            hint_type=hint_type,
                            chapter=0,
                            related_elements=self._find_related_elements(content, text)
                        ))
        
        return foreshadows[:20]
    
    def _find_related_elements(self, content: str, hint_text: str) -> List[str]:
        """查找相关元素"""
        related = []
        keywords = re.findall(r'[^\s]{2,4}', hint_text)
        
        for keyword in keywords[:5]:
            if keyword in content and content.count(keyword) > 1:
                related.append(keyword)
        
        return related[:5]
    
    def extract_locations(self, content: str) -> List[str]:
        """提取地点"""
        logger.info("提取地点")
        
        location_patterns = [
            r'([^\s]{2,6})(?:城|镇|村|县|府|州|省|国)',
            r'([^\s]{2,6})(?:山|峰|崖|谷|洞|渊|海|湖|河|江|岛)',
            r'([^\s]{2,6})(?:秘境|遗迹|禁地|险境|洞府)',
            r'在([^\s]{2,6})(?:之|的)中(?:修炼|修行|生活|居住)',
        ]
        
        locations = set()
        
        for pattern in location_patterns:
            for match in re.finditer(pattern, content):
                location = match.group(1)
                if len(location) >= 2 and location not in ['一个', '这个', '那个']:
                    locations.add(location)
        
        return sorted(list(locations))[:30]
    
    def analyze_time_system(self, content: str) -> str:
        """分析时间体系"""
        time_markers = {
            'modern': ['现代', '都市', '科技', '互联网', '手机'],
            'ancient': ['古代', '王朝', '皇朝', '帝国', '武林'],
            'cultivation': ['修仙', '修真', '灵气', '修士', '修仙界'],
            'fantasy': ['异界', '异大陆', '魔法', '斗气', '神界']
        }
        
        for system, markers in time_markers.items():
            count = sum(content.count(marker) for marker in markers)
            if count > 5:
                return system
        
        return 'unknown'
    
    def analyze_cultivation_system(self, content: str) -> str:
        """分析修炼体系"""
        cultivation_types = {
            'xianxia': ['金丹', '元婴', '渡劫', '飞升', '仙界'],
            'wuxia': ['内力', '真气', '经脉', '穴位', '武功'],
            'xuanhuan': ['斗气', '魔法', '魔兽', '斗师', '大魔导师'],
            'urban': ['异能', '觉醒', '超能力', '异能者']
        }
        
        max_count = 0
        best_type = 'unknown'
        
        for system, markers in cultivation_types.items():
            count = sum(content.count(marker) for marker in markers)
            if count > max_count:
                max_count = count
                best_type = system
        
        return best_type
    
    def get_architecture_summary(self, architecture: WorldArchitecture) -> str:
        """获取架构摘要"""
        summary_parts = []
        
        if architecture.power_levels:
            summary_parts.append(f"力量境界: {' > '.join([p.name for p in architecture.power_levels])}")
        
        if architecture.factions:
            summary_parts.append(f"势力门派: {', '.join([f.name for f in architecture.factions[:5]])}")
        
        if architecture.locations:
            summary_parts.append(f"重要地点: {', '.join(architecture.locations[:5])}")
        
        summary_parts.append(f"修炼体系: {architecture.cultivation_system}")
        summary_parts.append(f"时间设定: {architecture.time_system}")
        
        return '\n'.join(summary_parts)


def test_macro_architecture():
    """测试宏观架构分析"""
    print("=" * 60)
    print("宏观架构分析模块测试")
    print("=" * 60)
    
    analyzer = MacroArchitectureAnalyzer()
    
    test_content = """
    在这个修仙世界中，共分为八大境界：凡人、炼气、筑基、金丹、元婴、化神、渡劫、真仙。
    
    青云门是北域最大的修仙门派，位于青云山脉之中。掌门人清风真人已达到元婴境界。
    
    据说千年前，天地灵气充沛，修士可以轻易飞升仙界。但后来灵气衰竭，飞升变得困难。
    
    据说每一个修士都有属于自己的命格，或贵或贱，或是天选之子。
    
    李云是青云门外门弟子，刚刚踏入炼气境界。他住在青云山脚下的青云镇。
    
    天元城中有一个神秘的黑风教，据说他们修炼的是禁忌功法。
    
    李云总觉得自己的命运与众不同，仿佛有什么在等待着他。
    
    据说在极北之地的北海深渊中，封印着一头上古凶兽。
    
    未来某一天，李云将面对命运的重大抉择。
    """
    
    print("\n测试1: 完整架构分析")
    try:
        architecture = analyzer.analyze(test_content)
        print(f"✓ 分析成功")
        print(f"\n架构摘要:")
        print(analyzer.get_architecture_summary(architecture))
    except Exception as e:
        print(f"✗ 分析失败: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n测试2: 力量体系提取")
    try:
        power_levels = analyzer.extract_power_system(test_content)
        print(f"✓ 提取成功，找到 {len(power_levels)} 个境界")
        for level in power_levels:
            print(f"  - {level.name}: {level.description}")
    except Exception as e:
        print(f"✗ 提取失败: {e}")
    
    print("\n测试3: 势力门派提取")
    try:
        factions = analyzer.extract_factions(test_content)
        print(f"✓ 提取成功，找到 {len(factions)} 个势力")
        for faction in factions:
            print(f"  - {faction.name} ({faction.type}): {faction.location}")
    except Exception as e:
        print(f"✗ 提取失败: {e}")
    
    print("\n测试4: 伏笔提取")
    try:
        foreshadows = analyzer.extract_foreshadows(test_content)
        print(f"✓ 提取成功，找到 {len(foreshadows)} 个伏笔")
        for fs in foreshadows[:3]:
            print(f"  - [{fs.hint_type}] {fs.text[:50]}...")
    except Exception as e:
        print(f"✗ 提取失败: {e}")
    
    print("\n测试5: 地点提取")
    try:
        locations = analyzer.extract_locations(test_content)
        print(f"✓ 提取成功，找到 {len(locations)} 个地点")
        print(f"  {', '.join(locations[:10])}")
    except Exception as e:
        print(f"✗ 提取失败: {e}")
    
    print("\n" + "=" * 60)
    print("宏观架构分析模块测试完成")
    print("=" * 60)


if __name__ == "__main__":
    test_macro_architecture()
