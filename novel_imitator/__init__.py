"""
仿写小说软件 - 包初始化文件
"""
from .config import Config, get_default_config, load_config

__version__ = "1.0.0"
__author__ = "Novel Imitator Team"

__all__ = [
    'Config',
    'get_default_config', 
    'load_config'
]
