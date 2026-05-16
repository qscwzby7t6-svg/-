"""
小说解析模块 - 负责解析和分割小说文本
支持TXT格式，提取章节、人物、世界观等信息
"""
import re
import os
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass, field
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class Chapter:
    """章节数据类"""
    number: int
    title: str
    content: str
    word_count: int
    start_pos: int
    end_pos: int
    
    def __post_init__(self):
        if self.word_count == 0:
            self.word_count = len(self.content)

@dataclass
class NovelMetadata:
    """小说元数据"""
    title: str
    author: str
    total_chapters: int
    total_words: int
    genre: str = ""
    chapters: List[Chapter] = field(default_factory=list)

class NovelParser:
    """小说解析器"""
    
    CHAPTER_PATTERNS = [
        r'^第[一二三四五六七八九十百千零\d]+章[章节部]\s*[:：]?\s*(.+)$',
        r'^第[一二三四五六七八九十百千零\d]+节\s*[:：]?\s*(.+)$',
        r'^Chapter\s+\d+[:\.]?\s*(.+)$',
        r'^第[一二三四五六七八九十百千零\d]+部\s*[:：]?\s*(.+)$',
        r'^第\d+章\s+(.+)$',
        r'^第\s*\d+\s*章\s*[:：]?\s*(.*)$',
    ]
    
    def __init__(self, config: Optional[Any] = None):
        self.config = config
        self.chapter_patterns = [re.compile(p, re.MULTILINE) for p in self.CHAPTER_PATTERNS]
    
    def parse_file(self, file_path: str) -> NovelMetadata:
        """解析小说文件"""
        logger.info(f"开始解析小说文件: {file_path}")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        metadata = self._extract_metadata(content)
        metadata.chapters = self._split_chapters(content)
        metadata.total_chapters = len(metadata.chapters)
        metadata.total_words = sum(ch.word_count for ch in metadata.chapters)
        
        logger.info(f"解析完成: {metadata.total_chapters}章节, {metadata.total_words}字")
        return metadata
    
    def parse_content(self, content: str, title: str = "", author: str = "") -> NovelMetadata:
        """解析小说内容"""
        logger.info("开始解析小说内容")
        
        metadata = self._extract_metadata(content)
        if title:
            metadata.title = title
        if author:
            metadata.author = author
            
        metadata.chapters = self._split_chapters(content)
        metadata.total_chapters = len(metadata.chapters)
        metadata.total_words = sum(ch.word_count for ch in metadata.chapters)
        
        logger.info(f"解析完成: {metadata.total_chapters}章节, {metadata.total_words}字")
        return metadata
    
    def _extract_metadata(self, content: str) -> NovelMetadata:
        """提取元数据"""
        lines = content.split('\n')
        title = ""
        author = ""
        genre = ""
        
        for line in lines[:20]:
            line = line.strip()
            if not line:
                continue
                
            title_match = re.search(r'书名[：:]\s*(.+)', line)
            if title_match:
                title = title_match.group(1).strip()
                continue
                
            author_match = re.search(r'作者[：:]\s*(.+)', line)
            if author_match:
                author = author_match.group(1).strip()
                continue
                
            genre_match = re.search(r'类型[：:]\s*(.+)', line)
            if genre_match:
                genre = genre_match.group(1).strip()
                continue
        
        first_line = lines[0].strip() if lines else ""
        if not title and first_line and len(first_line) < 50:
            title = first_line
            
        return NovelMetadata(
            title=title or "未知标题",
            author=author or "未知作者",
            total_chapters=0,
            total_words=0,
            genre=genre
        )
    
    def _split_chapters(self, content: str) -> List[Chapter]:
        """分割章节"""
        chapters = []
        chapter_starts = []
        chapter_info = []
        
        for i, pattern in enumerate(self.chapter_patterns):
            for match in pattern.finditer(content):
                chapter_starts.append(match.start())
                chapter_info.append({
                    'pattern_id': i,
                    'title': match.group(1) if match.lastindex else match.group(0),
                    'match': match
                })
        
        chapter_starts = sorted(set(chapter_starts))
        
        if not chapter_starts:
            chapters = self._split_by_length(content)
        else:
            for idx, start in enumerate(chapter_starts):
                end = chapter_starts[idx + 1] if idx + 1 < len(chapter_starts) else len(content)
                chapter_text = content[start:end]
                
                info = chapter_info[idx]
                chapter = Chapter(
                    number=idx + 1,
                    title=info['title'],
                    content=chapter_text,
                    word_count=len(chapter_text),
                    start_pos=start,
                    end_pos=end
                )
                chapters.append(chapter)
        
        if len(chapters) == 1:
            chapters = self._split_by_length(content)
        
        for idx, chapter in enumerate(chapters):
            chapter.number = idx + 1
            
        return chapters
    
    def _split_by_length(self, content: str, min_length: int = 2000) -> List[Chapter]:
        """按长度分割章节"""
        chapters = []
        separators = ['\n\n', '\n', '。', '！', '？']
        
        parts = []
        current_pos = 0
        current_len = 0
        
        for sep in separators:
            if sep == '\n':
                lines = content.split('\n')
                parts = []
                for line in lines:
                    parts.append(line + '\n')
                    current_len += len(line)
                    if current_len >= min_length:
                        break
                if parts:
                    break
            else:
                sentences = content.split(sep)
                parts = []
                for sent in sentences:
                    parts.append(sent + sep)
                    current_len += len(sent)
                    if current_len >= min_length:
                        break
                if parts:
                    break
        
        if not parts:
            parts = [content[i:i+min_length] for i in range(0, len(content), min_length)]
        
        current_content = ""
        for idx, part in enumerate(parts):
            current_content += part
            if len(current_content) >= min_length or idx == len(parts) - 1:
                chapter = Chapter(
                    number=len(chapters) + 1,
                    title=f"第{self._int_to_chinese(len(chapters) + 1)}章",
                    content=current_content.strip(),
                    word_count=len(current_content),
                    start_pos=0,
                    end_pos=len(current_content)
                )
                chapters.append(chapter)
                current_content = ""
        
        return chapters
    
    def _int_to_chinese(self, num: int) -> str:
        """数字转中文"""
        chinese_nums = '零一二三四五六七八九十百千'
        if num <= 0:
            return '零'
        if num <= 10:
            return chinese_nums[num]
        if num < 20:
            return '十' + chinese_nums[num - 10] if num > 10 else '十'
        if num < 100:
            q, r = divmod(num, 10)
            return chinese_nums[q] + '十' + (chinese_nums[r] if r else '')
        return str(num)
    
    def extract_characters(self, content: str, top_n: int = 50) -> List[Dict[str, Any]]:
        """提取人物信息"""
        logger.info("提取人物信息")
        
        character_patterns = [
            r'["""]([^"""]+)["""]\s*[,，]\s*["""]([^"""]+)["""]',
            r'([^\s]{2,4})\s*（[^）]+）',
            r'([^\s]{2,4})\s*说道\s*[:：]',
            r'([^\s]{2,4})\s*说\s*[:：]',
            r'([^\s]{2,4})\s*问道\s*[:：]',
            r'([^\s]{2,4})\s*怒道\s*[:：]',
            r'([^\s]{2,4})\s*冷笑道\s*[:：]',
        ]
        
        character_counts = {}
        
        for pattern in character_patterns:
            for match in re.finditer(pattern, content):
                name = match.group(1).strip()
                if len(name) >= 2 and len(name) <= 4:
                    character_counts[name] = character_counts.get(name, 0) + 1
        
        sorted_chars = sorted(character_counts.items(), key=lambda x: x[1], reverse=True)
        
        return [
            {'name': name, 'count': count, 'frequency': count / len(content) * 10000}
            for name, count in sorted_chars[:top_n]
        ]
    
    def extract_world_info(self, content: str) -> Dict[str, Any]:
        """提取世界观信息"""
        logger.info("提取世界观信息")
        
        location_patterns = [
            r'([^\s]{2,6})(?:城|镇|村|国|域|界|州|府|省|山|峰|谷|洞|林|海|湖|河|岛))',
            r'在([^\s]{2,6})(?:中|里|内|外|上|下|前|后)',
        ]
        
        locations = []
        for pattern in location_patterns:
            locations.extend(re.findall(pattern, content))
        
        location_counts = {}
        for loc in locations:
            if len(loc) >= 2:
                location_counts[loc] = location_counts.get(loc, 0) + 1
        
        faction_patterns = [
            r'([^\s]{2,6})(?:门|派|教|宗|会|盟|帮|殿|宫|阁|堂|楼)',
            r'([^\s]{2,6})(?:家族|势力)',
        ]
        
        factions = []
        for pattern in faction_patterns:
            factions.extend(re.findall(pattern, content))
        
        return {
            'locations': sorted(location_counts.items(), key=lambda x: x[1], reverse=True)[:20],
            'factions': list(set(factions))[:20]
        }
    
    def calculate_chapter_stats(self, chapter: Chapter) -> Dict[str, Any]:
        """计算章节统计信息"""
        content = chapter.content
        
        dialogue_count = len(re.findall(r'["""\'].*?["""]', content))
        action_count = len(re.findall(r'(?:站|走|跑|跳|冲|飞|挥|砍|刺|挡|闪|退)', content))
        descriptive_count = len(re.findall(r'(?:的|地|得|像|如|似)', content))
        
        avg_sentence_length = len(content) / max(len(re.findall(r'[。！？]', content)), 1)
        
        return {
            'word_count': chapter.word_count,
            'dialogue_ratio': dialogue_count / max(chapter.word_count, 1) * 100,
            'action_ratio': action_count / max(chapter.word_count, 1) * 100,
            'descriptive_density': descriptive_count / max(chapter.word_count, 1) * 100,
            'avg_sentence_length': avg_sentence_length
        }


def test_parser():
    """测试解析器"""
    print("=" * 60)
    print("小说解析模块测试")
    print("=" * 60)
    
    parser = NovelParser()
    
    test_content = """
书名：测试小说
作者：测试作者
类型：玄幻

第一章 初始

清晨的阳光洒落在小镇的街道上。

"小明，你今天要去哪里？"小红问道。

小明说道："我要去山上修炼。"

主角名叫李云，是一个年轻的修士。他生活在一个叫做青云镇的地方。

第二章 修炼

李云站在山巅，望着远方的云海。他的心中充满了对力量的渴望。

"总有一天，我会成为最强的修士！"他暗暗发誓。
    """
    
    print("\n测试1: 解析小说内容")
    try:
        metadata = parser.parse_content(test_content, "测试小说", "测试作者")
        print(f"✓ 解析成功")
        print(f"  标题: {metadata.title}")
        print(f"  作者: {metadata.author}")
        print(f"  章节数: {metadata.total_chapters}")
        print(f"  总字数: {metadata.total_words}")
        print(f"  章节列表:")
        for ch in metadata.chapters:
            print(f"    - {ch.title}: {ch.word_count}字")
    except Exception as e:
        print(f"✗ 解析失败: {e}")
    
    print("\n测试2: 提取人物")
    try:
        characters = parser.extract_characters(test_content)
        print(f"✓ 提取成功，找到 {len(characters)} 个人物")
        for char in characters[:5]:
            print(f"  - {char['name']}: {char['count']}次")
    except Exception as e:
        print(f"✗ 提取失败: {e}")
    
    print("\n测试3: 提取世界观")
    try:
        world_info = parser.extract_world_info(test_content)
        print(f"✓ 提取成功")
        print(f"  地点: {world_info['locations'][:5]}")
        print(f"  势力: {world_info['factions'][:5]}")
    except Exception as e:
        print(f"✗ 提取失败: {e}")
    
    print("\n测试4: 章节统计")
    try:
        if metadata.chapters:
            stats = parser.calculate_chapter_stats(metadata.chapters[0])
            print(f"✓ 统计成功")
            print(f"  字数: {stats['word_count']}")
            print(f"  对话比例: {stats['dialogue_ratio']:.2f}%")
            print(f"  动作比例: {stats['action_ratio']:.2f}%")
    except Exception as e:
        print(f"✗ 统计失败: {e}")
    
    print("\n" + "=" * 60)
    print("解析模块测试完成")
    print("=" * 60)


if __name__ == "__main__":
    test_parser()
