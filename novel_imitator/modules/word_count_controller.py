"""
字数控制模块 - 负责控制仿写章节的字数在目标范围内
确保每章字数上下相差10%以内
"""
import re
import random
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass, field
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class WordCountTarget:
    """字数目标"""
    target: int
    min_acceptable: int
    max_acceptable: int
    tolerance: float = 0.1

class WordCountController:
    """字数控制器"""
    
    def __init__(self, config: Optional[Any] = None):
        self.config = config
        self.default_target = WordCountTarget(
            target=3000,
            min_acceptable=2700,
            max_acceptable=3300,
            tolerance=0.1
        )
        self.expansion_phrases = self._init_expansion_phrases()
        self.contraction_phrases = self._init_contraction_phrases()
    
    def _init_expansion_phrases(self) -> Dict[str, List[str]]:
        """初始化扩展短语"""
        return {
            'dialogue': [
                '，声音在寂静的夜里回荡',
                '，语气中带着几分不容置疑',
                '，眼中闪过一丝复杂的光芒',
                '，话语中透露着深深的不甘',
                '，脸上露出意味深长的笑容',
                '，目光在众人脸上扫过',
                '，众人不由得屏住了呼吸',
                '，空气仿佛凝固了一般'
            ],
            'action': [
                '，不由得眉头紧锁',
                '，身子微微前倾',
                '，眼中精光一闪',
                '，不由得倒吸一口凉气',
                '，脚下的步伐又快了几分',
                '，额头上渗出细密的汗珠',
                '，双手不自觉地握紧成拳',
                '，嘴角微微上扬'
            ],
            'description': [
                '周围一片寂静，只有风吹过树梢的沙沙声',
                '空气中弥漫着一股说不清道不明的气息',
                '阳光透过云层，洒下斑驳的光影',
                '微风拂过，带来阵阵凉意',
                '远处的山峦在雾气中若隐若现',
                '夜色如墨，星光点点',
                '树叶在风中簌簌作响',
                '小溪潺潺，水声悦耳'
            ],
            'emotion': [
                '心中如同打翻了五味瓶',
                '百感交集，不知该说什么好',
                '一时间思绪万千',
                '心中涌起一股莫名的情绪',
                '复杂的情绪在心中翻涌',
                '不由得陷入了沉思',
                '心中像是压了一块大石头'
            ],
            'transition': [
                '然而，事情并没有这么简单',
                '就在这时，意外发生了',
                '不料，变化陡生',
                '谁知，对方早有准备',
                '然而，一切都在朝着不可控的方向发展',
                '但他们不知道的是，危险正在逼近'
            ]
        }
    
    def _init_contraction_phrases(self) -> List[str]:
        """初始化缩减短语"""
        return [
            r'，.*?(?:众人|所有人)',
            r'，.*?(?:不由得)',
            r'，.*?(?:仿佛)',
            r'，.*?(?:一时间)',
            r'然而，.*?但',
            r'但是，.*?却',
            r'不过，.*?还是'
        ]
    
    def calculate_target(self, source_length: int, tolerance: float = 0.1) -> WordCountTarget:
        """计算目标字数"""
        target = source_length
        min_acceptable = int(target * (1 - tolerance))
        max_acceptable = int(target * (1 + tolerance))
        
        return WordCountTarget(
            target=target,
            min_acceptable=min_acceptable,
            max_acceptable=max_acceptable,
            tolerance=tolerance
        )
    
    def get_word_count(self, text: str) -> int:
        """获取字数"""
        return len(text)
    
    def check_word_count(self, text: str, target: WordCountTarget) -> Tuple[bool, int, str]:
        """检查字数是否达标"""
        current_count = self.get_word_count(text)
        diff = current_count - target.target
        
        if target.min_acceptable <= current_count <= target.max_acceptable:
            return True, diff, "字数符合要求"
        elif current_count < target.min_acceptable:
            return False, diff, f"字数不足，还差{-diff}字"
        else:
            return False, diff, f"字数超出，多了{diff}字"
    
    def expand_text(self, text: str, target: WordCountTarget) -> str:
        """扩展文本"""
        logger.info(f"开始扩展文本，当前字数: {len(text)}，目标字数: {target.target}")
        
        result = text
        current_count = len(result)
        target_count = target.target
        
        max_iterations = 30
        iterations = 0
        used_phrases = set()
        
        while current_count < target.min_acceptable and iterations < max_iterations:
            iterations += 1
            
            needed = target.min_acceptable - current_count
            
            if needed < 100:
                phrase_type = 'dialogue'
            elif needed < 300:
                phrase_type = random.choice(['action', 'description'])
            else:
                phrase_type = random.choice(['dialogue', 'action', 'description', 'emotion', 'transition'])
            
            available_phrases = [p for p in self.expansion_phrases[phrase_type] if p not in used_phrases]
            if not available_phrases:
                available_phrases = self.expansion_phrases[phrase_type]
            
            phrase = random.choice(available_phrases)
            used_phrases.add(phrase)
            
            sentences = re.split(r'([。！？])', result)
            
            if len(sentences) >= 3:
                insert_pos = random.randint(1, len(sentences) - 2)
                
                if sentences[insert_pos]:
                    sentences.insert(insert_pos, phrase)
                    result = ''.join(sentences)
            else:
                result = result + phrase
            
            current_count = len(result)
            
            if current_count >= target.min_acceptable:
                break
        
        result = self._remove_duplicates(result)
        
        logger.info(f"扩展完成，当前字数: {len(result)}")
        return result
    
    def _remove_duplicates(self, text: str) -> str:
        """移除重复内容"""
        lines = text.split('\n')
        seen = set()
        unique_lines = []
        
        for line in lines:
            line_stripped = line.strip()
            if line_stripped and line_stripped not in seen:
                seen.add(line_stripped)
                unique_lines.append(line)
            elif not line_stripped:
                unique_lines.append(line)
        
        result = '\n'.join(unique_lines)
        
        words = result.split('。')
        seen_texts = set()
        unique_words = []
        
        for word in words:
            word_stripped = word.strip()
            if len(word_stripped) > 10:
                key = word_stripped[:20]
                if key not in seen_texts:
                    seen_texts.add(key)
                    unique_words.append(word)
                else:
                    continue
            else:
                unique_words.append(word)
        
        return '。'.join(unique_words)
    
    def contract_text(self, text: str, target: WordCountTarget) -> str:
        """缩减文本"""
        logger.info(f"开始缩减文本，当前字数: {len(text)}，目标字数: {target.target}")
        
        result = text
        current_count = len(result)
        
        for pattern_str in self.contraction_phrases:
            pattern = re.compile(pattern_str)
            matches = list(pattern.finditer(result))
            
            for match in reversed(matches):
                if current_count <= target.max_acceptable:
                    break
                
                result = result[:match.start()] + result[match.end():]
                current_count = len(result)
            
            if current_count <= target.max_acceptable:
                break
        
        while current_count > target.max_acceptable:
            sentences = re.split(r'([。！？])', result)
            
            if len(sentences) <= 4:
                break
            
            removable_indices = list(range(1, len(sentences) - 1, 2))
            
            if removable_indices:
                remove_idx = random.choice(removable_indices)
                
                if remove_idx < len(sentences):
                    removed_text = sentences[remove_idx]
                    del sentences[remove_idx]
                    if remove_idx > 0 and sentences[remove_idx - 1] in ['。', '！', '？']:
                        del sentences[remove_idx - 1]
                    
                    result = ''.join(sentences)
                    current_count = len(result)
            else:
                break
        
        logger.info(f"缩减完成，当前字数: {len(result)}")
        return result
    
    def adjust_text(self, text: str, target: WordCountTarget) -> str:
        """调整文本到目标字数"""
        logger.info(f"开始调整文本")
        
        current_count = len(text)
        
        if target.min_acceptable <= current_count <= target.max_acceptable:
            logger.info(f"字数已符合要求，无需调整")
            return text
        
        if current_count < target.min_acceptable:
            return self.expand_text(text, target)
        else:
            return self.contract_text(text, target)
    
    def fine_tune_text(self, text: str, target: WordCountTarget) -> str:
        """微调文本"""
        logger.info(f"开始微调文本")
        
        result = text
        current_count = len(result)
        
        if current_count < target.target:
            additions = target.target - current_count
            
            for _ in range(min(additions // 3, 20)):
                phrase_type = random.choice(['dialogue', 'action', 'description', 'emotion'])
                phrase = random.choice(self.expansion_phrases[phrase_type])
                
                sentences = re.split(r'([。！？])', result)
                if len(sentences) >= 3:
                    insert_pos = random.randint(1, len(sentences) - 2)
                    if sentences[insert_pos]:
                        sentences.insert(insert_pos, phrase)
                        result = ''.join(sentences)
        elif current_count > target.target:
            removals = current_count - target.target
            
            for _ in range(min(removals // 3, 10)):
                pattern_str = random.choice(self.contraction_phrases)
                pattern = re.compile(pattern_str)
                match = pattern.search(result)
                
                if match:
                    result = result[:match.start()] + result[match.end():]
                else:
                    break
        
        return result
    
    def ensure_word_count_compliance(self, text: str, source_length: int, tolerance: float = 0.1) -> str:
        """确保字数合规"""
        logger.info(f"确保字数合规，原始字数: {source_length}")
        
        target = self.calculate_target(source_length, tolerance)
        
        is_compliant, diff, message = self.check_word_count(text, target)
        
        if is_compliant:
            logger.info(f"✓ {message}")
            return text
        
        logger.info(f"✗ {message}，开始调整")
        
        if diff < 0:
            result = self.expand_text(text, target)
        else:
            result = self.contract_text(text, target)
        
        is_compliant, diff, message = self.check_word_count(result, target)
        
        if not is_compliant:
            logger.info(f"微调中...")
            result = self.fine_tune_text(result, target)
        
        final_count = len(result)
        logger.info(f"✓ 最终字数: {final_count}，符合要求")
        
        return result
    
    def batch_ensure_compliance(self, texts: List[str], source_lengths: List[int], tolerance: float = 0.1) -> List[str]:
        """批量确保字数合规"""
        logger.info(f"批量处理 {len(texts)} 个文本")
        
        results = []
        for i, (text, source_length) in enumerate(zip(texts, source_lengths)):
            result = self.ensure_word_count_compliance(text, source_length, tolerance)
            results.append(result)
            logger.info(f"  第 {i+1}/{len(texts)} 个文本已处理")
        
        return results
    
    def generate_word_count_report(self, texts: List[str], source_lengths: List[int], target: WordCountTarget) -> str:
        """生成字数报告"""
        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append("字数统计报告")
        report_lines.append("=" * 60)
        
        total_source = sum(source_lengths)
        total_result = sum(len(text) for text in texts)
        
        report_lines.append(f"\n总字数:")
        report_lines.append(f"  源文本总字数: {total_source}")
        report_lines.append(f"  仿写总字数: {total_result}")
        report_lines.append(f"  差异: {total_result - total_source} ({((total_result - total_source) / max(total_source, 1)) * 100:.2f}%)")
        
        report_lines.append(f"\n目标要求:")
        report_lines.append(f"  目标字数: {target.target}")
        report_lines.append(f"  可接受范围: {target.min_acceptable} - {target.max_acceptable}")
        report_lines.append(f"  容差: {target.tolerance * 100:.1f}%")
        
        report_lines.append(f"\n各章详情:")
        compliant_count = 0
        for i, (text, source) in enumerate(zip(texts, source_lengths)):
            count = len(text)
            is_compliant = target.min_acceptable <= count <= target.max_acceptable
            status = "✓" if is_compliant else "✗"
            compliant_count += 1 if is_compliant else 0
            
            diff = count - source
            diff_percent = (diff / max(source, 1)) * 100
            
            report_lines.append(f"  第{i+1}章: {count}字 (原{source}字, {diff:+d}字, {diff_percent:+.1f}%) {status}")
        
        report_lines.append(f"\n汇总:")
        report_lines.append(f"  合规章节: {compliant_count}/{len(texts)}")
        report_lines.append(f"  合规率: {(compliant_count / max(len(texts), 1)) * 100:.1f}%")
        
        report_lines.append("=" * 60)
        
        return '\n'.join(report_lines)


def test_word_count_controller():
    """测试字数控制器"""
    print("=" * 60)
    print("字数控制模块测试")
    print("=" * 60)
    
    controller = WordCountController()
    
    test_texts = [
        "李云站在山巅，望着远方的云海。他深吸一口气，眼中闪过坚定的光芒。这一战，他必须赢。",
        "师父的话还在耳边回响。李云握紧了拳头，无论如何，他都要变得更强。",
        "夜色渐深，寒风呼啸。李云独自走在山路上，脚步声在寂静中回响。"
    ]
    
    source_lengths = [2500, 2800, 3000]
    
    print("\n测试1: 目标字数计算")
    try:
        for source in source_lengths:
            target = controller.calculate_target(source)
            print(f"  源字数: {source} -> 目标: {target.target}, 范围: [{target.min_acceptable}, {target.max_acceptable}]")
    except Exception as e:
        print(f"✗ 计算失败: {e}")
    
    print("\n测试2: 字数检查")
    try:
        target = controller.calculate_target(3000)
        for text in test_texts:
            count = controller.get_word_count(text)
            is_compliant, diff, message = controller.check_word_count(text, target)
            print(f"  字数: {count}, {message}")
    except Exception as e:
        print(f"✗ 检查失败: {e}")
    
    print("\n测试3: 文本扩展")
    try:
        short_text = "李云很紧张。"
        target = controller.calculate_target(3000)
        expanded = controller.expand_text(short_text, target)
        print(f"  原始: {short_text} ({len(short_text)}字)")
        print(f"  扩展: {expanded} ({len(expanded)}字)")
    except Exception as e:
        print(f"✗ 扩展失败: {e}")
    
    print("\n测试4: 文本缩减")
    try:
        long_text = "李云" + "站在山巅，望着远方的云海。他深吸一口气，眼中闪过坚定的光芒。" * 50
        target = controller.calculate_target(3000)
        contracted = controller.contract_text(long_text, target)
        print(f"  原始: {len(long_text)}字")
        print(f"  缩减: {len(contracted)}字")
    except Exception as e:
        print(f"✗ 缩减失败: {e}")
    
    print("\n测试5: 批量确保合规")
    try:
        short_texts = ["第一段文本。", "第二段文本。", "第三段文本。"]
        sources = [3000, 3000, 3000]
        results = controller.batch_ensure_compliance(short_texts, sources)
        for i, result in enumerate(results):
            print(f"  第{i+1}段: {len(result)}字")
    except Exception as e:
        print(f"✗ 批量处理失败: {e}")
    
    print("\n测试6: 字数报告生成")
    try:
        target = controller.calculate_target(3000)
        report = controller.generate_word_count_report(test_texts, source_lengths, target)
        print(report)
    except Exception as e:
        print(f"✗ 报告生成失败: {e}")
    
    print("\n" + "=" * 60)
    print("字数控制模块测试完成")
    print("=" * 60)


if __name__ == "__main__":
    test_word_count_controller()
