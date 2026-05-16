"""
章节结构分析模块 - 负责分析章节的结构、节奏、叙事模式
"""
import re
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass, field
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SceneBlock:
    """场景块"""
    scene_type: str
    content: str
    start_pos: int
    end_pos: int
    length: int
    purpose: str

@dataclass
class ChapterStructure:
    """章节结构"""
    chapter_number: int
    title: str
    length: int
    scenes: List[SceneBlock]
    dialogue_ratio: float
    action_ratio: float
    description_ratio: float
    pacing: str
    tension_level: int
    opening_style: str
    closing_style: str

class ChapterStructureAnalyzer:
    """章节结构分析器"""
    
    def __init__(self, config: Optional[Any] = None):
        self.config = config
        self.scene_types = self._init_scene_types()
        self.opening_patterns = self._init_opening_patterns()
        self.closing_patterns = self._init_closing_patterns()
    
    def _init_scene_types(self) -> Dict[str, List[str]]:
        """初始化场景类型"""
        return {
            'combat': ['战斗', '打斗', '交手', '厮杀', '搏斗', '对决', '比试', '过招'],
            'dialogue': ['说道', '问道', '答道', '说道：', '问道：', '说道"', '问道"'],
            'narration': ['于是', '然后', '接着', '只见', '但见', '只见'],
            'description': ['的', '地', '得', '像', '如', '似'],
            'reflection': ['心想', '想到', '寻思', '暗自', '暗暗', '心中想'],
            'travel': ['来到', '走向', '前往', '穿过', '踏入', '进入'],
            'training': ['修炼', '打坐', '运功', '吸收', '炼化', '突破']
        }
    
    def _init_opening_patterns(self) -> List[str]:
        """初始化开头模式"""
        return [
            r'^清晨',
            r'^早晨',
            r'^夜晚',
            r'^夜色',
            r'^突然',
            r'^话说',
            r'^却说',
            r'^却说',
            r'^这一日',
            r'^某一天',
            r'^这一夜',
            r'^第二日',
            r'^天一亮'
        ]
    
    def _init_closing_patterns(self) -> List[str]:
        """初始化结尾模式"""
        return [
            r'未完待续',
            r'敬请期待',
            r'欲知后事如何',
            r'且听下回分解',
            r'本章完',
            r'字数不够',
            r'（完）',
            r'END',
            r'——',
            r'……'
        ]
    
    def analyze_chapter(self, chapter_content: str, chapter_number: int = 1, title: str = "") -> ChapterStructure:
        """分析单个章节结构"""
        logger.info(f"分析第{chapter_number}章结构")
        
        scenes = self._extract_scenes(chapter_content)
        dialogue_ratio = self._calculate_dialogue_ratio(chapter_content)
        action_ratio = self._calculate_action_ratio(chapter_content)
        description_ratio = self._calculate_description_ratio(chapter_content)
        pacing = self._analyze_pacing(chapter_content, scenes)
        tension_level = self._analyze_tension(chapter_content)
        opening_style = self._identify_opening(chapter_content)
        closing_style = self._identify_closing(chapter_content)
        
        return ChapterStructure(
            chapter_number=chapter_number,
            title=title or f"第{chapter_number}章",
            length=len(chapter_content),
            scenes=scenes,
            dialogue_ratio=dialogue_ratio,
            action_ratio=action_ratio,
            description_ratio=description_ratio,
            pacing=pacing,
            tension_level=tension_level,
            opening_style=opening_style,
            closing_style=closing_style
        )
    
    def analyze_chapters(self, chapters: List[Any]) -> List[ChapterStructure]:
        """分析多个章节结构"""
        logger.info(f"分析{len(chapters)}个章节结构")
        
        structures = []
        for i, chapter in enumerate(chapters):
            content = chapter.content if hasattr(chapter, 'content') else str(chapter)
            structure = self.analyze_chapter(
                content,
                chapter.number if hasattr(chapter, 'number') else i+1,
                chapter.title if hasattr(chapter, 'title') else ""
            )
            structures.append(structure)
        
        return structures
    
    def _extract_scenes(self, content: str) -> List[SceneBlock]:
        """提取场景"""
        scenes = []
        
        separators = ['\n\n', '\n', '。']
        
        for sep in separators:
            if len(content) > 500:
                break
            parts = content.split(sep)
            if len(parts) > 5:
                break
        
        current_pos = 0
        for part in parts:
            if len(part.strip()) < 50:
                current_pos += len(part) + len(sep)
                continue
            
            scene_type = self._classify_scene(part)
            scene = SceneBlock(
                scene_type=scene_type,
                content=part.strip(),
                start_pos=current_pos,
                end_pos=current_pos + len(part),
                length=len(part),
                purpose=self._infer_scene_purpose(part, scene_type)
            )
            scenes.append(scene)
            current_pos += len(part) + len(sep)
        
        return scenes
    
    def _classify_scene(self, text: str) -> str:
        """分类场景"""
        scores = {}
        
        for scene_type, keywords in self.scene_types.items():
            score = sum(1 for keyword in keywords if keyword in text)
            scores[scene_type] = score
        
        if not scores or max(scores.values()) == 0:
            return 'narration'
        
        return max(scores.items(), key=lambda x: x[1])[0]
    
    def _infer_scene_purpose(self, text: str, scene_type: str) -> str:
        """推断场景目的"""
        purposes = {
            'combat': '推进情节，展示实力',
            'dialogue': '传递信息，揭示关系',
            'narration': '交代背景，连接情节',
            'description': '营造氛围，烘托情绪',
            'reflection': '展示心理，塑造人物',
            'travel': '推动剧情，转换场景',
            'training': '展现成长，推进力量体系'
        }
        
        return purposes.get(scene_type, '推进情节')
    
    def _calculate_dialogue_ratio(self, content: str) -> float:
        """计算对话比例"""
        dialogue_marks = ['"', '"', '"', '"', '"', '"', '"', '"', '："', '"：', '说：', '道：', '问：', '答：']
        dialogue_count = 0
        
        for mark in dialogue_marks:
            dialogue_count += content.count(mark)
        
        total_sentences = max(len(re.findall(r'[。！？]', content)), 1)
        
        return (dialogue_count / total_sentences) * 100
    
    def _calculate_action_ratio(self, content: str) -> float:
        """计算动作比例"""
        action_words = [
            '站', '走', '跑', '跳', '冲', '飞', '挥', '砍', '刺', '挡', '闪', '退',
            '躲', '扑', '抓', '推', '拉', '抬', '举', '甩', '踢', '踩', '踏',
            '看', '盯', '望', '瞧', '瞅', '扫', '瞥', '瞪', '眨',
            '笑', '哭', '喊', '叫', '吼', '啸', '吟', '唱', '说', '问', '答',
            '手', '脚', '身', '头', '眼', '嘴', '拳', '掌', '指'
        ]
        
        action_count = sum(content.count(word) for word in action_words)
        
        return (action_count / max(len(content), 1)) * 100
    
    def _calculate_description_ratio(self, content: str) -> float:
        """计算描写比例"""
        descriptive_marks = ['的', '地', '得', '像', '如', '似', '仿佛']
        
        descriptive_count = sum(content.count(mark) for mark in descriptive_marks)
        
        return (descriptive_count / max(len(content), 1)) * 100
    
    def _analyze_pacing(self, content: str, scenes: List[SceneBlock]) -> str:
        """分析节奏"""
        action_scenes = [s for s in scenes if s.scene_type == 'combat']
        
        if len(action_scenes) > len(scenes) * 0.3:
            return 'fast'
        elif len(action_scenes) < len(scenes) * 0.1:
            return 'slow'
        else:
            return 'moderate'
    
    def _analyze_tension(self, content: str) -> int:
        """分析紧张度"""
        tension_keywords = {
            5: ['战斗', '危机', '生死', '危险', '死亡', '威胁'],
            4: ['紧张', '担心', '害怕', '焦急', '不安'],
            3: ['疑惑', '犹豫', '矛盾', '冲突'],
            2: ['平静', '安宁', '和谐'],
            1: ['轻松', '愉快', '欢笑']
        }
        
        score = 1
        for level, keywords in tension_keywords.items():
            if any(keyword in content for keyword in keywords):
                score = max(score, level)
        
        return score
    
    def _identify_opening(self, content: str) -> str:
        """识别开头风格"""
        first_sentence = content.split('\n')[0] if content else ""
        
        for pattern in self.opening_patterns:
            if re.search(pattern, first_sentence):
                return pattern.replace(r'^', '')
        
        if any(word in first_sentence for word in ['突然', '忽然', '猛地']):
            return 'sudden'
        elif any(word in first_sentence for word in ['只见', '但见', '但看']):
            return 'observational'
        elif any(word in first_sentence for word in ['却说', '话说', '且说']):
            return 'narrative'
        else:
            return 'direct'
    
    def _identify_closing(self, content: str) -> str:
        """识别结尾风格"""
        last_sentences = re.split(r'[。！？]', content)[-5:]
        
        for pattern in self.closing_patterns:
            if any(re.search(pattern, s) for s in last_sentences):
                return pattern.replace(r'\\', '')
        
        if any(word in ' '.join(last_sentences) for word in ['突然', '就在这时']):
            return 'cliffhanger'
        elif any(word in ' '.join(last_sentences) for word in ['未完', '待续']):
            return 'to_be_continued'
        else:
            return 'conclusive'
    
    def compare_structures(self, structure1: ChapterStructure, structure2: ChapterStructure) -> Dict[str, Any]:
        """比较两个章节结构"""
        return {
            'length_diff': abs(structure1.length - structure2.length),
            'length_diff_ratio': abs(structure1.length - structure2.length) / max(structure1.length, structure2.length, 1),
            'dialogue_diff': abs(structure1.dialogue_ratio - structure2.dialogue_ratio),
            'action_diff': abs(structure1.action_ratio - structure2.action_ratio),
            'pacing_match': structure1.pacing == structure2.pacing,
            'tension_diff': abs(structure1.tension_level - structure2.tension_level)
        }
    
    def generate_structure_template(self, structures: List[ChapterStructure]) -> Dict[str, Any]:
        """生成结构模板"""
        if not structures:
            return {}
        
        avg_length = sum(s.length for s in structures) / len(structures)
        avg_dialogue = sum(s.dialogue_ratio for s in structures) / len(structures)
        avg_action = sum(s.action_ratio for s in structures) / len(structures)
        
        pacing_counts = {}
        for s in structures:
            pacing_counts[s.pacing] = pacing_counts.get(s.pacing, 0) + 1
        
        opening_counts = {}
        for s in structures:
            opening_counts[s.opening_style] = opening_counts.get(s.opening_style, 0) + 1
        
        closing_counts = {}
        for s in structures:
            closing_counts[s.closing_style] = closing_counts.get(s.closing_style, 0) + 1
        
        return {
            'target_length': int(avg_length),
            'target_dialogue_ratio': avg_dialogue,
            'target_action_ratio': avg_action,
            'common_pacing': max(pacing_counts.items(), key=lambda x: x[1])[0] if pacing_counts else 'moderate',
            'common_opening': max(opening_counts.items(), key=lambda x: x[1])[0] if opening_counts else 'direct',
            'common_closing': max(closing_counts.items(), key=lambda x: x[1])[0] if closing_counts else 'conclusive'
        }


def test_chapter_structure():
    """测试章节结构分析"""
    print("=" * 60)
    print("章节结构分析模块测试")
    print("=" * 60)
    
    analyzer = ChapterStructureAnalyzer()
    
    test_content = """
    清晨的阳光洒落在青云山上。
    
    李云站在山巅，望着远方的云海。
    
    "师父，今天的修炼要做什么？"李云问道。
    
    清风真人捋了捋胡须，笑道："今日你便随为师前往天元城历练。"
    
    突然，一道黑影从林中窜出！
    
    "小心！"李云大喝一声，拔剑而起。
    
    只见那黑影手中持着一把弯刀，直取李云要害。
    
    李云挥剑挡开对方的攻击，顺势反击。
    
    两人交手数十招，不分胜负。
    
    "你是谁？为何在此埋伏？"李云喝问道。
    
    那人不答，只是招招狠辣，刀刀致命。
    
    战斗越来越激烈，李云渐渐感到吃力。
    
    就在危急关头，清风真人出手了！
    
    一道剑光闪过，那黑衣人应声倒地。
    
    "没事吧？"清风真人问道。
    
    李云擦了擦额头的汗水："多谢师父相救。"
    
    两人继续向天元城进发。
    """
    
    print("\n测试1: 章节结构分析")
    try:
        structure = analyzer.analyze_chapter(test_content, 1, "测试章节")
        print(f"✓ 分析成功")
        print(f"  章节长度: {structure.length}字")
        print(f"  对话比例: {structure.dialogue_ratio:.2f}%")
        print(f"  动作比例: {structure.action_ratio:.2f}%")
        print(f"  节奏: {structure.pacing}")
        print(f"  紧张度: {structure.tension_level}/5")
        print(f"  开头风格: {structure.opening_style}")
        print(f"  结尾风格: {structure.closing_style}")
        print(f"  场景数: {len(structure.scenes)}")
    except Exception as e:
        print(f"✗ 分析失败: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n测试2: 场景提取")
    try:
        scenes = analyzer._extract_scenes(test_content)
        print(f"✓ 提取成功，找到 {len(scenes)} 个场景")
        for scene in scenes[:5]:
            print(f"  - [{scene.scene_type}] {scene.content[:30]}... ({scene.length}字)")
    except Exception as e:
        print(f"✗ 提取失败: {e}")
    
    print("\n测试3: 结构模板生成")
    try:
        from modules.parser import Chapter
        chapters = [
            Chapter(1, "第一章", test_content, len(test_content), 0, len(test_content)),
            Chapter(2, "第二章", test_content * 1.2, int(len(test_content) * 1.2), 0, int(len(test_content) * 1.2))
        ]
        structures = analyzer.analyze_chapters(chapters)
        template = analyzer.generate_structure_template(structures)
        print(f"✓ 生成成功")
        print(f"  目标字数: {template['target_length']}")
        print(f"  目标对话比例: {template['target_dialogue_ratio']:.2f}%")
        print(f"  常见节奏: {template['common_pacing']}")
        print(f"  常见开头: {template['common_opening']}")
        print(f"  常见结尾: {template['common_closing']}")
    except Exception as e:
        print(f"✗ 生成失败: {e}")
    
    print("\n" + "=" * 60)
    print("章节结构分析模块测试完成")
    print("=" * 60)


if __name__ == "__main__":
    test_chapter_structure()
