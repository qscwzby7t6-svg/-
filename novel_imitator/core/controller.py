"""
主控制器模块 - 协调所有模块，完成仿写任务
负责管理整个仿写流程，包括解析、分析、生成、后处理等
"""
import os
import sys
import time
import logging
from typing import List, Dict, Optional, Any, Tuple
from dataclasses import dataclass, field
from pathlib import Path
import json

try:
    from ..modules.parser import NovelParser, Chapter, NovelMetadata
    from ..modules.macro_architecture import MacroArchitectureAnalyzer, WorldArchitecture
    from ..modules.character_analyzer import CharacterAnalyzer, Character
    from ..modules.chapter_structure import ChapterStructureAnalyzer, ChapterStructure
    from ..modules.style_extractor import StyleFeatureExtractor, StyleFeatures
    from ..modules.deepseek_client import DeepSeekClient, GenerationRequest
    from ..modules.text_concretizer import TextConcretizer
    from ..modules.fight_generator import FightSceneGenerator, Combatant
    from ..modules.swear_handler import SwearWordHandler
    from ..modules.climax_generator import ClimaxGenerator, Climax
    from ..modules.word_count_controller import WordCountController, WordCountTarget
except ImportError:
    from modules.parser import NovelParser, Chapter, NovelMetadata
    from modules.macro_architecture import MacroArchitectureAnalyzer, WorldArchitecture
    from modules.character_analyzer import CharacterAnalyzer, Character
    from modules.chapter_structure import ChapterStructureAnalyzer, ChapterStructure
    from modules.style_extractor import StyleFeatureExtractor, StyleFeatures
    from modules.deepseek_client import DeepSeekClient, GenerationRequest
    from modules.text_concretizer import TextConcretizer
    from modules.fight_generator import FightSceneGenerator, Combatant
    from modules.swear_handler import SwearWordHandler
    from modules.climax_generator import ClimaxGenerator, Climax
    from modules.word_count_controller import WordCountController, WordCountTarget

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ImitationTask:
    """仿写任务"""
    task_id: str
    source_file: Optional[str] = None
    source_content: Optional[str] = None
    source_title: str = ""
    source_author: str = ""
    protagonist_name: str = "主角"
    genre: str = "xianxia"
    total_chapters: int = 10
    target_chapters: List[int] = field(default_factory=list)
    status: str = "pending"
    progress: float = 0.0
    created_at: str = ""
    completed_at: str = ""

@dataclass
class ImitationResult:
    """仿写结果"""
    task_id: str
    success: bool
    chapters: List[str]
    word_count_report: str
    metadata: Dict[str, Any]
    error_message: Optional[str] = None

class NovelImitatorController:
    """小说仿写主控制器"""
    
    def __init__(self, config: Optional[Any] = None):
        self.config = config
        self.parser = NovelParser(config)
        self.architecture_analyzer = MacroArchitectureAnalyzer(config)
        self.character_analyzer = CharacterAnalyzer(config)
        self.chapter_analyzer = ChapterStructureAnalyzer(config)
        self.style_extractor = StyleFeatureExtractor(config)
        self.deepseek_client = DeepSeekClient(config=config)
        self.text_concretizer = TextConcretizer(config)
        self.fight_generator = FightSceneGenerator(config)
        self.swear_handler = SwearWordHandler(config)
        self.climax_generator = ClimaxGenerator(config)
        self.word_count_controller = WordCountController(config)
        
        self.current_task: Optional[ImitationTask] = None
        self.metadata: Optional[NovelMetadata] = None
        self.architecture: Optional[WorldArchitecture] = None
        self.characters: List[Character] = []
        self.styles: Optional[StyleFeatures] = None
        self.chapter_structures: List[ChapterStructure] = []
        
        self.tasks: Dict[str, ImitationTask] = {}
    
    def create_task(self, **kwargs) -> ImitationTask:
        """创建仿写任务"""
        import uuid
        from datetime import datetime
        
        task_id = str(uuid.uuid4())[:8]
        
        task = ImitationTask(
            task_id=task_id,
            source_file=kwargs.get('source_file'),
            source_content=kwargs.get('source_content'),
            source_title=kwargs.get('source_title', ''),
            source_author=kwargs.get('source_author', ''),
            protagonist_name=kwargs.get('protagonist_name', '主角'),
            genre=kwargs.get('genre', 'xianxia'),
            total_chapters=kwargs.get('total_chapters', 10),
            status='created',
            created_at=datetime.now().isoformat()
        )
        
        self.tasks[task_id] = task
        self.current_task = task
        
        logger.info(f"创建仿写任务: {task_id}")
        
        return task
    
    def run_analysis_phase(self) -> bool:
        """运行分析阶段"""
        logger.info("=" * 60)
        logger.info("开始分析阶段")
        logger.info("=" * 60)
        
        try:
            if not self.current_task:
                raise ValueError("没有当前任务")
            
            task = self.current_task
            
            logger.info("步骤1: 解析小说")
            if task.source_file:
                self.metadata = self.parser.parse_file(task.source_file)
            elif task.source_content:
                self.metadata = self.parser.parse_content(
                    task.source_content, 
                    task.source_title, 
                    task.source_author
                )
            else:
                raise ValueError("没有提供源文件或源内容")
            
            logger.info(f"  解析完成: {self.metadata.total_chapters}章节, {self.metadata.total_words}字")
            
            task.progress = 0.1
            logger.info("步骤2: 分析宏观架构")
            full_content = '\n'.join([ch.content for ch in self.metadata.chapters])
            self.architecture = self.architecture_analyzer.analyze(full_content, self.metadata.chapters)
            logger.info(f"  分析完成: {len(self.architecture.power_levels)}个境界, {len(self.architecture.factions)}个势力")
            
            task.progress = 0.2
            logger.info("步骤3: 分析人物")
            self.characters = self.character_analyzer.analyze(full_content, self.metadata.chapters)
            logger.info(f"  分析完成: {len(self.characters)}个人物")
            
            task.progress = 0.3
            logger.info("步骤4: 分析章节结构")
            self.chapter_structures = self.chapter_analyzer.analyze_chapters(self.metadata.chapters)
            logger.info(f"  分析完成: {len(self.chapter_structures)}个章节结构")
            
            task.progress = 0.4
            logger.info("步骤5: 提取文风特征")
            self.styles = self.style_extractor.extract_features(full_content, self.metadata.chapters)
            logger.info(f"  提取完成: {len(self.styles.writing_styles)}种风格")
            
            task.progress = 0.5
            task.status = 'analysis_completed'
            logger.info("分析阶段完成")
            
            return True
            
        except Exception as e:
            logger.error(f"分析阶段失败: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def generate_chapter(self, chapter_number: int, source_chapter: Optional[Chapter] = None) -> str:
        """生成单个章节"""
        logger.info(f"生成第{chapter_number}章")
        
        try:
            target_length = self._calculate_target_length(chapter_number)
            
            outline = self._generate_chapter_outline(chapter_number, target_length)
            
            context = self._prepare_chapter_context(chapter_number)
            
            content = self._call_deepseek_for_generation(outline, target_length, context)
            
            content = self.text_concretizer.concretize_text(content)
            
            content = self._apply_style_guidelines(content)
            
            content = self._ensure_word_count_compliance(content, target_length)
            
            if self.climax_generator.should_insert_climax(chapter_number):
                content = self._insert_climax(content, chapter_number)
            
            content = self._add_opening_and_closing(content, chapter_number)
            
            logger.info(f"第{chapter_number}章生成完成: {len(content)}字")
            
            return content
            
        except Exception as e:
            logger.error(f"生成第{chapter_number}章失败: {e}")
            import traceback
            traceback.print_exc()
            return f"第{chapter_number}章生成失败: {str(e)}"
    
    def _calculate_target_length(self, chapter_number: int) -> int:
        """计算目标长度"""
        if self.chapter_structures:
            for structure in self.chapter_structures:
                if structure.chapter_number == chapter_number:
                    return max(structure.length, 3000)
        
        if self.metadata and self.metadata.total_chapters > 0:
            avg_length = self.metadata.total_words // self.metadata.total_chapters
            return max(avg_length, 3000)
        
        return 3000
    
    def _generate_chapter_outline(self, chapter_number: int, target_length: int) -> str:
        """生成章节大纲"""
        outline_parts = []
        
        outline_parts.append(f"第{chapter_number}章")
        
        if self.architecture:
            if self.architecture.power_levels:
                outline_parts.append(f"涉及境界: {[p.name for p in self.architecture.power_levels[:3]]}")
            
            if self.architecture.factions and chapter_number <= len(self.architecture.factions):
                faction = self.architecture.factions[chapter_number - 1]
                outline_parts.append(f"涉及势力: {faction.name}")
        
        outline_parts.append(f"目标字数: 约{target_length}字")
        
        outline_parts.append("情节要求:")
        
        if self.characters:
            protagonist = next((c for c in self.characters if c.importance == 'protagonist'), self.characters[0])
            outline_parts.append(f"- 主角: {protagonist.name}")
            
            if protagonist.goals:
                outline_parts.append(f"- 主角目标: {protagonist.goals[0]}")
        
        if chapter_number % 5 == 0:
            outline_parts.append("- 需要有小高潮")
        
        outline_parts.append("- 保持原文章风格")
        
        return '\n'.join(outline_parts)
    
    def _prepare_chapter_context(self, chapter_number: int) -> Dict[str, Any]:
        """准备章节上下文"""
        context = {
            'chapter_number': chapter_number,
            'protagonist': self.current_task.protagonist_name if self.current_task else '主角'
        }
        
        if self.architecture:
            context['cultivation_system'] = self.architecture.cultivation_system
            context['time_system'] = self.architecture.time_system
            
            if self.architecture.locations:
                context['current_location'] = self.architecture.locations[min(chapter_number - 1, len(self.architecture.locations) - 1)]
        
        if self.characters:
            protagonist = next((c for c in self.characters if c.importance == 'protagonist'), self.characters[0])
            context['protagonist_info'] = {
                'name': protagonist.name,
                'power_level': protagonist.power_level,
                'personality': [t.name for t in protagonist.personality_traits[:3]]
            }
        
        return context
    
    def _call_deepseek_for_generation(self, outline: str, target_length: int, context: Dict[str, Any]) -> str:
        """调用DeepSeek生成内容"""
        logger.info("调用DeepSeek API生成内容")
        
        style_guide = ""
        if self.styles:
            style_guide = self.style_extractor.generate_style_guide(self.styles)
        
        content = self.deepseek_client.generate_chapter(
            outline=outline,
            style_guide=style_guide,
            target_length=target_length,
            context=context
        )
        
        if not content or len(content) < 100:
            logger.warning("DeepSeek API返回内容过短，使用本地生成")
            content = self._generate_local_fallback(outline, target_length, context)
        
        return content
    
    def _generate_local_fallback(self, outline: str, target_length: int, context: Dict[str, Any]) -> str:
        """本地备用生成"""
        logger.info("使用本地模板生成")
        
        content_parts = []
        
        content_parts.append(f"第{context['chapter_number']}章\n\n")
        
        protagonist = context.get('protagonist', '主角')
        location = context.get('current_location', '某处')
        
        content_parts.append(f"清晨的阳光洒落在{location}上。\n\n")
        
        content_parts.append(f"{protagonist}独自站在山巅，望着远方的云海，心中思绪万千。\n\n")
        
        content_parts.append(f"就在这时，一阵脚步声从身后传来。\n\n")
        
        content_parts.append(f'"{self._get_random_dialogue()}"{protagonist}转过身来。\n\n')
        
        while len('\n'.join(content_parts)) < target_length:
            content_parts.append(f"战斗瞬间爆发！\n\n")
            content_parts.append(f"{protagonist}身形暴起，拳风呼啸。\n\n")
            content_parts.append(f"双方你来我往，招招凶狠。\n\n")
        
        content = '\n'.join(content_parts)
        
        return content
    
    def _get_random_dialogue(self) -> str:
        """获取随机对话"""
        dialogues = [
            "站住！",
            "来者何人？",
            "受死吧！",
            "你的死期到了！",
            "哼，就凭你？"
        ]
        import random
        return random.choice(dialogues)
    
    def _apply_style_guidelines(self, content: str) -> str:
        """应用风格指南"""
        content = self.text_concretizer.remove_ai_patterns(content)
        
        if self.styles and self.styles.ai_indicators:
            for indicator in self.styles.ai_indicators[:10]:
                phrase = indicator.split(' (')[0]
                if phrase in content:
                    content = content.replace(phrase, '')
        
        return content
    
    def _ensure_word_count_compliance(self, content: str, target_length: int) -> str:
        """确保字数合规"""
        return self.word_count_controller.ensure_word_count_compliance(
            content, 
            target_length, 
            tolerance=0.1
        )
    
    def _insert_climax(self, content: str, chapter_number: int) -> str:
        """插入高潮"""
        protagonist = self.current_task.protagonist_name if self.current_task else '主角'
        
        climax_type = self._infer_climax_type_for_chapter(chapter_number)
        
        climax = self.climax_generator.generate_climax(
            climax_type=climax_type,
            chapter=chapter_number,
            context={'protagonist': protagonist},
            protagonist=protagonist
        )
        
        content = self.climax_generator.integrate_climax_into_chapter(content, climax, position='end')
        
        return content
    
    def _infer_climax_type_for_chapter(self, chapter_number: int) -> str:
        """推断章节高潮类型"""
        climax_types = ['battle', 'revelation', 'breakthrough', 'confrontation']
        import random
        return random.choice(climax_types)
    
    def _add_opening_and_closing(self, content: str, chapter_number: int) -> str:
        """添加开头和结尾"""
        openings = [
            f"第{chapter_number}章\n\n",
            f"却说第{chapter_number}章\n\n"
        ]
        
        import random
        
        if not content.startswith('第'):
            content = random.choice(openings) + content
        
        closings = [
            '\n\n欲知后事如何，且听下回分解。',
            '\n\n（本章完）',
            ''
        ]
        
        if not content.endswith(('完', '分解')):
            content += random.choice(closings)
        
        return content
    
    def run_generation_phase(self, start_chapter: int = 1, end_chapter: Optional[int] = None) -> List[str]:
        """运行生成阶段"""
        logger.info("=" * 60)
        logger.info("开始生成阶段")
        logger.info("=" * 60)
        
        if not self.current_task:
            raise ValueError("没有当前任务")
        
        task = self.current_task
        
        if end_chapter is None:
            end_chapter = task.total_chapters
        
        generated_chapters = []
        
        for chapter_num in range(start_chapter, end_chapter + 1):
            logger.info(f"正在生成第{chapter_num}/{end_chapter}章...")
            
            source_chapter = None
            if self.metadata and chapter_num <= len(self.metadata.chapters):
                source_chapter = self.metadata.chapters[chapter_num - 1]
            
            chapter_content = self.generate_chapter(chapter_num, source_chapter)
            generated_chapters.append(chapter_content)
            
            progress = 0.5 + (chapter_num - start_chapter + 1) / (end_chapter - start_chapter + 1) * 0.4
            task.progress = progress
            
            time.sleep(0.1)
        
        task.progress = 0.9
        task.status = 'generation_completed'
        
        logger.info(f"生成阶段完成: {len(generated_chapters)}章节")
        
        return generated_chapters
    
    def run_full_imitation(self, **kwargs) -> ImitationResult:
        """运行完整仿写"""
        logger.info("=" * 60)
        logger.info("开始完整仿写流程")
        logger.info("=" * 60)
        
        task = self.create_task(**kwargs)
        
        try:
            if not self.run_analysis_phase():
                return ImitationResult(
                    task_id=task.task_id,
                    success=False,
                    chapters=[],
                    word_count_report="",
                    metadata={},
                    error_message="分析阶段失败"
                )
            
            chapters = self.run_generation_phase()
            
            task.status = 'completed'
            task.progress = 1.0
            from datetime import datetime
            task.completed_at = datetime.now().isoformat()
            
            target = self.word_count_controller.calculate_target(3000)
            report = self.word_count_controller.generate_word_count_report(
                chapters,
                [self._calculate_target_length(i+1) for i in range(len(chapters))],
                target
            )
            
            metadata = {
                'title': self.metadata.title if self.metadata else task.source_title,
                'author': self.metadata.author if self.metadata else task.source_author,
                'total_chapters': len(chapters),
                'total_words': sum(len(ch) for ch in chapters)
            }
            
            return ImitationResult(
                task_id=task.task_id,
                success=True,
                chapters=chapters,
                word_count_report=report,
                metadata=metadata
            )
            
        except Exception as e:
            logger.error(f"仿写流程失败: {e}")
            import traceback
            traceback.print_exc()
            return ImitationResult(
                task_id=task.task_id,
                success=False,
                chapters=[],
                word_count_report="",
                metadata={},
                error_message=str(e)
            )
    
    def save_result(self, result: ImitationResult, output_path: str) -> bool:
        """保存结果"""
        try:
            output_dir = Path(output_path).parent
            output_dir.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                for i, chapter in enumerate(result.chapters):
                    f.write(f"{'='*60}\n")
                    f.write(f"第{i+1}章\n")
                    f.write(f"{'='*60}\n\n")
                    f.write(chapter)
                    f.write("\n\n")
            
            logger.info(f"结果已保存到: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"保存失败: {e}")
            return False
    
    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """获取任务状态"""
        task = self.tasks.get(task_id)
        if not task:
            return None
        
        return {
            'task_id': task.task_id,
            'status': task.status,
            'progress': task.progress,
            'created_at': task.created_at,
            'completed_at': task.completed_at
        }


def test_controller():
    """测试主控制器"""
    print("=" * 60)
    print("小说仿写主控制器测试")
    print("=" * 60)
    
    controller = NovelImitatorController()
    
    test_content = """
    书名：测试小说
    作者：测试作者
    
    第一章 初始
    
    清晨的阳光洒落在青云山上。
    
    李云站在山巅，望着远方的云海。
    
    "师父，今天的修炼要做什么？"李云问道。
    
    清风真人捋了捋胡须，笑道："今日你便随为师前往天元城历练。"
    
    第二章 修炼
    
    李云来到天元城中。
    
    突然，一道黑影从林中窜出！
    
    "小心！"李云大喝一声，拔剑而起。
    
    两人交手数十招，不分胜负。
    """
    
    print("\n测试1: 创建任务")
    try:
        task = controller.create_task(
            source_content=test_content,
            source_title="测试小说",
            source_author="测试作者",
            protagonist_name="李云",
            genre="xianxia",
            total_chapters=3
        )
        print(f"✓ 任务创建成功: {task.task_id}")
    except Exception as e:
        print(f"✗ 任务创建失败: {e}")
    
    print("\n测试2: 运行分析阶段")
    try:
        success = controller.run_analysis_phase()
        print(f"✓ 分析阶段: {'成功' if success else '失败'}")
    except Exception as e:
        print(f"✗ 分析阶段失败: {e}")
    
    print("\n测试3: 生成单个章节")
    try:
        chapter = controller.generate_chapter(1)
        print(f"✓ 章节生成成功: {len(chapter)}字")
        print(f"  预览: {chapter[:200]}...")
    except Exception as e:
        print(f"✗ 章节生成失败: {e}")
    
    print("\n测试4: 运行完整仿写")
    try:
        result = controller.run_full_imitation(
            source_content=test_content,
            source_title="测试小说",
            source_author="测试作者",
            protagonist_name="李云",
            total_chapters=2
        )
        print(f"✓ 仿写完成: {'成功' if result.success else '失败'}")
        if result.success:
            print(f"  生成章节数: {len(result.chapters)}")
            print(f"  总字数: {result.metadata.get('total_words', 0)}")
    except Exception as e:
        print(f"✗ 仿写失败: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("主控制器测试完成")
    print("=" * 60)


if __name__ == "__main__":
    test_controller()
