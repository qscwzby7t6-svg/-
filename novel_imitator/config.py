"""
仿写小说软件 - 配置模块
提供全局配置和参数管理
"""
import os
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, field
import json

@dataclass
class ModelConfig:
    """模型配置"""
    deepseek_api_key: str = ""
    deepseek_base_url: str = "https://api.deepseek.com/v4"
    deepseek_model: str = "deepseek-v4-pro"
    temperature: float = 0.7
    max_tokens: int = 4000
    request_timeout: int = 120

@dataclass
class ParseConfig:
    """解析配置"""
    min_chapter_length: int = 500
    max_chapter_length: int = 50000
    min_word_count_for_analysis: int = 10000
    encoding: str = "utf-8"
    supported_formats: list = field(default_factory=lambda: [".txt"])

@dataclass
class StyleConfig:
    """文风配置"""
    avoid_ai_phrases: list = field(default_factory=lambda: [
        "首先", "其次", "最后", "综上所述", "值得注意的是",
        "从某种意义上说", "可以说", "值得注意的是",
        "在这个时代", "在这个背景下", "不得不说",
        "事实上", "实际上", "客观来说", "主观而言"
    ])
    concrete_indicators: list = field(default_factory=lambda: [
        "突然", "猛然", "陡然", "猝然", "骤然"
    ])
    bad_words_library: dict = field(default_factory=lambda: {
        "愤怒": ["妈的", "他妈的", "混账", "王八蛋"],
        "蔑视": ["切", "呸", "嘁", "滚蛋"],
        "疼痛": ["操", "该死", "妈的"],
        "惊讶": ["靠", "我靠", "卧槽"],
        "无奈": ["妈的", "真是见了鬼"],
        "兴奋": ["牛逼", "太他妈爽了", "干得漂亮"]
    })
    slang_expressions: list = field(default_factory=lambda: [
        "老子", "老子我", "爷", "本大爷", "本少爷",
        "小爷", "奶奶", "姑奶奶"
    ])

@dataclass
class FightConfig:
    """打斗场景配置"""
    min_fight_duration: int = 300
    max_fight_duration: int = 2000
    fight_intensity_levels: dict = field(default_factory=lambda: {
        "low": {"strikes_per_minute": 5, "descriptions": 3},
        "medium": {"strikes_per_minute": 10, "descriptions": 5},
        "high": {"strikes_per_minute": 20, "descriptions": 10}
    })

@dataclass
class ClimaxConfig:
    """高潮场景配置"""
    climax_interval: int = 10
    min_climax_length: int = 500
    max_climax_length: int = 2000
    climax_types: list = field(default_factory=lambda: [
        "battle", "revelation", "betrayal", "breakthrough", "confrontation"
    ])

@dataclass
class WordCountConfig:
    """字数控制配置"""
    target_word_count: int = 3000
    tolerance: float = 0.1
    min_words: int = 2700
    max_words: int = 3300

class Config:
    """全局配置类"""
    def __init__(self, config_path: Optional[str] = None):
        self.model = ModelConfig()
        self.parse = ParseConfig()
        self.style = StyleConfig()
        self.fight = FightConfig()
        self.climax = ClimaxConfig()
        self.word_count = WordCountConfig()
        
        if config_path:
            self.load_from_file(config_path)
    
    def load_from_file(self, config_path: str):
        """从JSON文件加载配置"""
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for section in ['model', 'parse', 'style', 'fight', 'climax', 'word_count']:
                    if section in data:
                        getattr(self, section).__dict__.update(data[section])
    
    def save_to_file(self, config_path: str):
        """保存配置到JSON文件"""
        data = {
            'model': self.model.__dict__,
            'parse': self.parse.__dict__,
            'style': self.style.__dict__,
            'fight': self.fight.__dict__,
            'climax': self.climax.__dict__,
            'word_count': self.word_count.__dict__
        }
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

def get_default_config() -> Config:
    """获取默认配置"""
    return Config()

def get_config_path() -> Path:
    """获取配置文件路径"""
    return Path.home() / ".novel_imitator" / "config.json"

def load_config() -> Config:
    """加载配置，优先从默认路径"""
    config_path = get_config_path()
    if config_path.exists():
        return Config(str(config_path))
    return get_default_config()
