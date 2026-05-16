"""
模块初始化文件
导出所有模块的主要类
"""
from .parser import NovelParser, Chapter, NovelMetadata
from .macro_architecture import MacroArchitectureAnalyzer, WorldArchitecture
from .character_analyzer import CharacterAnalyzer, Character
from .chapter_structure import ChapterStructureAnalyzer, ChapterStructure
from .style_extractor import StyleFeatureExtractor, StyleFeatures
from .deepseek_client import DeepSeekClient, GenerationRequest
from .text_concretizer import TextConcretizer
from .fight_generator import FightSceneGenerator, Combatant
from .swear_handler import SwearWordHandler
from .climax_generator import ClimaxGenerator, Climax
from .word_count_controller import WordCountController, WordCountTarget
from .similarity_comparator import TextSimilarityComparator, ComparisonReport

__all__ = [
    'NovelParser',
    'Chapter',
    'NovelMetadata',
    'MacroArchitectureAnalyzer',
    'WorldArchitecture',
    'CharacterAnalyzer',
    'Character',
    'ChapterStructureAnalyzer',
    'ChapterStructure',
    'StyleFeatureExtractor',
    'StyleFeatures',
    'DeepSeekClient',
    'GenerationRequest',
    'TextConcretizer',
    'FightSceneGenerator',
    'Combatant',
    'SwearWordHandler',
    'ClimaxGenerator',
    'Climax',
    'WordCountController',
    'WordCountTarget',
    'TextSimilarityComparator',
    'ComparisonReport'
]
