"""
仿写文字与原文相似度对比模块
实现多种相似度算法，提供详细的对比分析
"""
import re
import math
from typing import List, Dict, Tuple, Set, Optional, Any
from dataclasses import dataclass, field
from collections import Counter
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SimilarityScore:
    """相似度评分"""
    algorithm: str
    score: float
    description: str
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ComparisonReport:
    """对比报告"""
    overall_similarity: float
    text_similarity: float
    structural_similarity: float
    vocabulary_similarity: float
    style_similarity: float
    detailed_scores: List[SimilarityScore]
    similarities: Dict[str, float]
    differences: List[str]
    recommendations: List[str]

class TextSimilarityComparator:
    """文本相似度对比器"""
    
    def __init__(self, config: Optional[Any] = None):
        self.config = config
        self.stopwords = self._init_stopwords()
    
    def _init_stopwords(self) -> Set[str]:
        """初始化停用词"""
        return {
            '的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个',
            '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好',
            '自己', '这', '那', '之', '为', '与', '而', '或', '但', '等', '以', '及',
            '于', '中', '从', '对', '所', '能', '把', '被', '让', '给', '向', '往'
        }
    
    def preprocess_text(self, text: str) -> str:
        """文本预处理"""
        text = re.sub(r'[^\w\s\u4e00-\u9fff]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def tokenize(self, text: str) -> List[str]:
        """分词"""
        text = self.preprocess_text(text)
        words = []
        current_word = ""
        
        for char in text:
            if '\u4e00' <= char <= '\u9fff':
                if current_word:
                    words.append(current_word)
                    current_word = ""
                words.append(char)
            elif char == ' ':
                if current_word:
                    words.append(current_word)
                    current_word = ""
            else:
                current_word += char
        
        if current_word:
            words.append(current_word)
        
        return [w for w in words if w.strip()]
    
    def jaccard_similarity(self, text1: str, text2: str) -> SimilarityScore:
        """Jaccard相似度"""
        tokens1 = set(self.tokenize(text1))
        tokens2 = set(self.tokenize(text2))
        
        intersection = tokens1 & tokens2
        union = tokens1 | tokens2
        
        if not union:
            return SimilarityScore("Jaccard", 0.0, "无交集")
        
        score = len(intersection) / len(union)
        
        return SimilarityScore(
            algorithm="Jaccard相似度",
            score=score,
            description=f"词汇交集比例: {len(intersection)}/{len(union)}",
            details={
                'tokens1_count': len(tokens1),
                'tokens2_count': len(tokens2),
                'intersection_count': len(intersection),
                'union_count': len(union)
            }
        )
    
    def cosine_similarity(self, text1: str, text2: str) -> SimilarityScore:
        """余弦相似度"""
        tokens1 = self.tokenize(text1)
        tokens2 = self.tokenize(text2)
        
        counter1 = Counter(tokens1)
        counter2 = Counter(tokens2)
        
        all_tokens = set(counter1.keys()) | set(counter2.keys())
        
        dot_product = sum(counter1.get(t, 0) * counter2.get(t, 0) for t in all_tokens)
        
        norm1 = math.sqrt(sum(counter1.get(t, 0) ** 2 for t in all_tokens))
        norm2 = math.sqrt(sum(counter2.get(t, 0) ** 2 for t in all_tokens))
        
        if norm1 == 0 or norm2 == 0:
            return SimilarityScore("Cosine", 0.0, "向量为空")
        
        score = dot_product / (norm1 * norm2)
        
        return SimilarityScore(
            algorithm="余弦相似度",
            score=score,
            description=f"词向量夹角余弦值",
            details={
                'dot_product': dot_product,
                'norm1': norm1,
                'norm2': norm2
            }
        )
    
    def levenshtein_similarity(self, text1: str, text2: str) -> SimilarityScore:
        """Levenshtein相似度（编辑距离）"""
        len1, len2 = len(text1), len(text2)
        
        if len1 == 0 and len2 == 0:
            return SimilarityScore("Levenshtein", 1.0, "完全相同")
        
        dp = [[0] * (len2 + 1) for _ in range(len1 + 1)]
        
        for i in range(len1 + 1):
            dp[i][0] = i
        for j in range(len2 + 1):
            dp[0][j] = j
        
        for i in range(1, len1 + 1):
            for j in range(1, len2 + 1):
                cost = 0 if text1[i-1] == text2[j-1] else 1
                dp[i][j] = min(
                    dp[i-1][j] + 1,
                    dp[i][j-1] + 1,
                    dp[i-1][j-1] + cost
                )
        
        distance = dp[len1][len2]
        max_len = max(len1, len2)
        score = 1 - (distance / max_len) if max_len > 0 else 0
        
        return SimilarityScore(
            algorithm="Levenshtein相似度",
            score=score,
            description=f"编辑距离: {distance}",
            details={
                'edit_distance': distance,
                'length1': len1,
                'length2': len2
            }
        )
    
    def ngram_similarity(self, text1: str, text2: str, n: int = 2) -> SimilarityScore:
        """N-gram相似度"""
        def get_ngrams(text: str, n: int) -> Set[str]:
            words = self.tokenize(text)
            ngrams = set()
            for i in range(len(words) - n + 1):
                ngram = tuple(words[i:i+n])
                ngrams.add(ngram)
            return ngrams
        
        ngrams1 = get_ngrams(text1, n)
        ngrams2 = get_ngrams(text2, n)
        
        if not ngrams1 and not ngrams2:
            return SimilarityScore(f"{n}-gram", 1.0, "无n-gram")
        
        intersection = ngrams1 & ngrams2
        union = ngrams1 | ngrams2
        
        score = len(intersection) / len(union) if union else 0
        
        return SimilarityScore(
            algorithm=f"{n}-gram相似度",
            score=score,
            description=f"{n}元组匹配比例",
            details={
                f'ngrams1_count': len(ngrams1),
                f'ngrams2_count': len(ngrams2),
                'intersection_count': len(intersection)
            }
        )
    
    def structural_similarity(self, text1: str, text2: str) -> SimilarityScore:
        """结构相似度"""
        stats1 = self._analyze_structure(text1)
        stats2 = self._analyze_structure(text2)
        
        scores = []
        
        char_len_ratio = min(stats1['char_length'], stats2['char_length']) / max(stats1['char_length'], stats2['char_length'])
        scores.append(char_len_ratio)
        
        word_count_ratio = min(stats1['word_count'], stats2['word_count']) / max(stats1['word_count'], stats2['word_count'])
        scores.append(word_count_ratio)
        
        sentence_count_ratio = min(stats1['sentence_count'], stats2['sentence_count']) / max(stats1['sentence_count'], stats2['sentence_count'])
        scores.append(sentence_count_ratio)
        
        avg_sentence_ratio = min(stats1['avg_sentence_len'], stats2['avg_sentence_len']) / max(stats1['avg_sentence_len'], stats2['avg_sentence_len'])
        scores.append(avg_sentence_ratio)
        
        score = sum(scores) / len(scores) if scores else 0
        
        return SimilarityScore(
            algorithm="结构相似度",
            score=score,
            description="段落、句子、长度结构对比",
            details={
                'text1_stats': stats1,
                'text2_stats': stats2,
                'component_scores': scores
            }
        )
    
    def _analyze_structure(self, text: str) -> Dict[str, Any]:
        """分析文本结构"""
        sentences = re.split(r'[。！？]', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        words = self.tokenize(text)
        
        char_length = len(text)
        word_count = len(words)
        sentence_count = len(sentences)
        avg_sentence_len = sum(len(s) for s in sentences) / sentence_count if sentence_count else 0
        
        dialogue_count = len(re.findall(r'["""\'""\']', text))
        
        return {
            'char_length': char_length,
            'word_count': word_count,
            'sentence_count': sentence_count,
            'avg_sentence_len': avg_sentence_len,
            'dialogue_count': dialogue_count
        }
    
    def vocabulary_similarity(self, text1: str, text2: str) -> SimilarityScore:
        """词汇相似度"""
        tokens1 = set(self.tokenize(text1)) - self.stopwords
        tokens2 = set(self.tokenize(text2)) - self.stopwords
        
        intersection = tokens1 & tokens2
        only_in_1 = tokens1 - tokens2
        only_in_2 = tokens2 - tokens1
        
        common_ratio = len(intersection) / max(len(tokens1), len(tokens2)) if max(len(tokens1), len(tokens2)) > 0 else 0
        
        score = common_ratio
        
        return SimilarityScore(
            algorithm="词汇相似度",
            score=score,
            description=f"核心词汇重合度",
            details={
                'common_words': list(intersection)[:20],
                'only_in_text1': list(only_in_1)[:10],
                'only_in_text2': list(only_in_2)[:10],
                'common_count': len(intersection)
            }
        )
    
    def style_similarity(self, text1: str, text2: str) -> SimilarityScore:
        """风格相似度"""
        style1 = self._analyze_style(text1)
        style2 = self._analyze_style(text2)
        
        scores = []
        
        dialogue_ratio_diff = abs(style1['dialogue_ratio'] - style2['dialogue_ratio'])
        dialogue_score = max(0, 1 - dialogue_ratio_diff)
        scores.append(dialogue_score)
        
        punctuation_diff = abs(style1['punctuation_density'] - style2['punctuation_density'])
        punctuation_score = max(0, 1 - punctuation_diff)
        scores.append(punctuation_score)
        
        sentence_len_diff = abs(style1['avg_sentence_length'] - style2['avg_sentence_length'])
        sentence_score = max(0, 1 - sentence_len_diff / max(style1['avg_sentence_length'], style2['avg_sentence_length'], 1))
        scores.append(sentence_score)
        
        verb_ratio_diff = abs(style1['verb_ratio'] - style2['verb_ratio'])
        verb_score = max(0, 1 - verb_ratio_diff)
        scores.append(verb_score)
        
        score = sum(scores) / len(scores) if scores else 0
        
        return SimilarityScore(
            algorithm="风格相似度",
            score=score,
            description="对话比例、标点、句长等写作风格对比",
            details={
                'text1_style': style1,
                'text2_style': style2
            }
        )
    
    def _analyze_style(self, text: str) -> Dict[str, float]:
        """分析写作风格"""
        words = self.tokenize(text)
        word_count = len(words)
        
        dialogue_count = len(re.findall(r'["""\'""\']', text))
        dialogue_ratio = dialogue_count / word_count if word_count > 0 else 0
        
        punctuation_count = sum(1 for c in text if c in '，。！？、；：""''（）')
        punctuation_density = punctuation_count / word_count if word_count > 0 else 0
        
        sentences = re.split(r'[。！？]', text)
        sentences = [s for s in sentences if s.strip()]
        avg_sentence_length = sum(len(s) for s in sentences) / len(sentences) if sentences else 0
        
        verbs = ['的', '地', '得', '了', '着', '过', '是', '有', '在', '来', '去', '说', '看', '想', '做']
        verb_count = sum(1 for w in words if w in verbs)
        verb_ratio = verb_count / word_count if word_count > 0 else 0
        
        adjectives = ['大', '小', '高', '低', '好', '坏', '新', '老', '美', '丑', '长', '短', '快', '慢', '强', '弱']
        adj_count = sum(1 for w in words if w in adjectives)
        adj_ratio = adj_count / word_count if word_count > 0 else 0
        
        return {
            'dialogue_ratio': dialogue_ratio,
            'punctuation_density': punctuation_density,
            'avg_sentence_length': avg_sentence_length,
            'verb_ratio': verb_ratio,
            'adjective_ratio': adj_ratio
        }
    
    def calculate_similarity(self, original_text: str, imitated_text: str) -> ComparisonReport:
        """计算完整相似度"""
        logger.info("开始计算相似度")
        
        jaccard = self.jaccard_similarity(original_text, imitated_text)
        cosine = self.cosine_similarity(original_text, imitated_text)
        levenshtein = self.levenshtein_similarity(original_text, imitated_text)
        ngram_2 = self.ngram_similarity(original_text, imitated_text, 2)
        ngram_3 = self.ngram_similarity(original_text, imitated_text, 3)
        structural = self.structural_similarity(original_text, imitated_text)
        vocabulary = self.vocabulary_similarity(original_text, imitated_text)
        style = self.style_similarity(original_text, imitated_text)
        
        all_scores = [jaccard, cosine, levenshtein, ngram_2, ngram_3, structural, vocabulary, style]
        
        text_algorithms = ['Jaccard相似度', '余弦相似度', 'Levenshtein相似度', '2-gram相似度', '3-gram相似度']
        text_scores = [s for s in all_scores if s.algorithm in text_algorithms]
        text_similarity = sum(s.score for s in text_scores) / len(text_scores) if text_scores else 0
        
        structural_similarity = structural.score
        vocabulary_similarity = vocabulary.score
        style_similarity = style.score
        
        overall_similarity = (
            text_similarity * 0.3 +
            structural_similarity * 0.2 +
            vocabulary_similarity * 0.2 +
            style_similarity * 0.3
        )
        
        differences = self._identify_differences(original_text, imitated_text)
        recommendations = self._generate_recommendations(all_scores)
        
        similarities = {
            'jaccard': jaccard.score,
            'cosine': cosine.score,
            'levenshtein': levenshtein.score,
            'ngram_2': ngram_2.score,
            'ngram_3': ngram_3.score,
            'structural': structural_similarity,
            'vocabulary': vocabulary_similarity,
            'style': style_similarity
        }
        
        return ComparisonReport(
            overall_similarity=overall_similarity,
            text_similarity=text_similarity,
            structural_similarity=structural_similarity,
            vocabulary_similarity=vocabulary_similarity,
            style_similarity=style_similarity,
            detailed_scores=all_scores,
            similarities=similarities,
            differences=differences,
            recommendations=recommendations
        )
    
    def _identify_differences(self, text1: str, text2: str) -> List[str]:
        """识别差异"""
        differences = []
        
        tokens1 = set(self.tokenize(text1))
        tokens2 = set(self.tokenize(text2))
        
        only_in_1 = tokens1 - tokens2
        only_in_2 = tokens2 - tokens1
        
        if len(only_in_1) > len(tokens1) * 0.5:
            differences.append(f"原文包含{len(only_in_1)}个独有词汇，仿写文本替换了大量词汇")
        
        if len(only_in_2) > len(tokens2) * 0.3:
            differences.append(f"仿写文本引入了{len(only_in_2)}个新词汇，增加了新的表达")
        
        len_diff = abs(len(text1) - len(text2)) / max(len(text1), len(text2))
        if len_diff > 0.5:
            differences.append(f"文本长度差异较大（{len_diff*100:.1f}%）")
        
        style1 = self._analyze_style(text1)
        style2 = self._analyze_style(text2)
        
        if abs(style1['dialogue_ratio'] - style2['dialogue_ratio']) > 0.2:
            differences.append("对话比例差异明显")
        
        if abs(style1['avg_sentence_length'] - style2['avg_sentence_length']) > 10:
            differences.append("平均句长差异较大")
        
        return differences
    
    def _generate_recommendations(self, scores: List[SimilarityScore]) -> List[str]:
        """生成建议"""
        recommendations = []
        
        avg_score = sum(s.score for s in scores) / len(scores) if scores else 0
        
        if avg_score > 0.8:
            recommendations.append("相似度过高，建议增加更多原创内容")
        elif avg_score < 0.3:
            recommendations.append("相似度过低，可能偏离原风格太远")
        
        for score in scores:
            if score.algorithm == "词汇相似度" and score.score < 0.2:
                recommendations.append("词汇变化较大，建议保留更多核心词汇")
            
            if score.algorithm == "结构相似度" and score.score < 0.5:
                recommendations.append("结构差异较大，建议参考原文段落结构")
            
            if score.algorithm == "风格相似度" and score.score < 0.5:
                recommendations.append("风格差异明显，建议调整对话和描写比例")
        
        return recommendations
    
    def generate_report(self, report: ComparisonReport, original_name: str = "原文", 
                       imitated_name: str = "仿写文本") -> str:
        """生成详细报告"""
        report_lines = []
        
        report_lines.append("=" * 80)
        report_lines.append("文本相似度对比报告")
        report_lines.append("=" * 80)
        report_lines.append(f"\n对比文本: {original_name} vs {imitated_name}")
        
        report_lines.append("\n" + "-" * 80)
        report_lines.append("一、总体相似度")
        report_lines.append("-" * 80)
        report_lines.append(f"  综合相似度: {report.overall_similarity*100:.2f}%")
        report_lines.append(f"  文本相似度: {report.text_similarity*100:.2f}%")
        report_lines.append(f"  结构相似度: {report.structural_similarity*100:.2f}%")
        report_lines.append(f"  词汇相似度: {report.vocabulary_similarity*100:.2f}%")
        report_lines.append(f"  风格相似度: {report.style_similarity*100:.2f}%")
        
        report_lines.append("\n" + "-" * 80)
        report_lines.append("二、各算法评分")
        report_lines.append("-" * 80)
        for score in report.detailed_scores:
            bar = "█" * int(score.score * 20) + "░" * (20 - int(score.score * 20))
            report_lines.append(f"  {score.algorithm:20s} [{bar}] {score.score*100:5.2f}%")
            report_lines.append(f"    {score.description}")
        
        report_lines.append("\n" + "-" * 80)
        report_lines.append("三、主要差异")
        report_lines.append("-" * 80)
        if report.differences:
            for i, diff in enumerate(report.differences, 1):
                report_lines.append(f"  {i}. {diff}")
        else:
            report_lines.append("  未发现显著差异")
        
        report_lines.append("\n" + "-" * 80)
        report_lines.append("四、优化建议")
        report_lines.append("-" * 80)
        if report.recommendations:
            for i, rec in enumerate(report.recommendations, 1):
                report_lines.append(f"  {i}. {rec}")
        else:
            report_lines.append("  当前仿写质量良好")
        
        report_lines.append("\n" + "-" * 80)
        report_lines.append("五、相似度评分解读")
        report_lines.append("-" * 80)
        report_lines.append(f"  综合相似度: {report.overall_similarity*100:.1f}%")
        if report.overall_similarity > 0.7:
            report_lines.append("  → 相似度较高，仿写内容与原文风格接近")
            report_lines.append("  → 建议：适当增加原创内容，避免侵权风险")
        elif report.overall_similarity > 0.4:
            report_lines.append("  → 相似度适中，保持了原风格的同时有所创新")
            report_lines.append("  → 建议：当前状态良好，可继续优化细节")
        else:
            report_lines.append("  → 相似度较低，仿写内容更具原创性")
            report_lines.append("  → 建议：可适当借鉴原文风格特色")
        
        report_lines.append("\n" + "=" * 80)
        
        return '\n'.join(report_lines)
    
    def visualize_comparison(self, original_text: str, imitated_text: str) -> str:
        """可视化对比"""
        lines = []
        
        lines.append("\n" + "=" * 80)
        lines.append("文本可视化对比")
        lines.append("=" * 80)
        
        orig_stats = self._analyze_structure(original_text)
        imit_stats = self._analyze_structure(imitated_text)
        
        lines.append("\n【长度对比】")
        max_len = max(orig_stats['char_length'], imit_stats['char_length'], 1)
        orig_bar = "█" * int(orig_stats['char_length'] / max_len * 40)
        imit_bar = "█" * int(imit_stats['char_length'] / max_len * 40)
        lines.append(f"  原文: {orig_bar} {orig_stats['char_length']}字")
        lines.append(f"  仿写: {imit_bar} {imit_stats['char_length']}字")
        
        lines.append("\n【句子数对比】")
        max_sent = max(orig_stats['sentence_count'], imit_stats['sentence_count'], 1)
        orig_bar = "█" * int(orig_stats['sentence_count'] / max_sent * 40)
        imit_bar = "█" * int(imit_stats['sentence_count'] / max_sent * 40)
        lines.append(f"  原文: {orig_bar} {orig_stats['sentence_count']}句")
        lines.append(f"  仿写: {imit_bar} {imit_stats['sentence_count']}句")
        
        lines.append("\n【词数对比】")
        max_word = max(orig_stats['word_count'], imit_stats['word_count'], 1)
        orig_bar = "█" * int(orig_stats['word_count'] / max_word * 40)
        imit_bar = "█" * int(imit_stats['word_count'] / max_word * 40)
        lines.append(f"  原文: {orig_bar} {orig_stats['word_count']}词")
        lines.append(f"  仿写: {imit_bar} {imit_stats['word_count']}词")
        
        style_orig = self._analyze_style(original_text)
        style_imit = self._analyze_style(imitated_text)
        
        lines.append("\n【风格特征对比】")
        
        lines.append("  对话比例:")
        max_dial = max(style_orig['dialogue_ratio'], style_imit['dialogue_ratio'], 0.01)
        orig_bar = "█" * int(style_orig['dialogue_ratio'] / max_dial * 40)
        imit_bar = "█" * int(style_imit['dialogue_ratio'] / max_dial * 40)
        lines.append(f"    原文: {orig_bar} {style_orig['dialogue_ratio']*100:.1f}%")
        lines.append(f"    仿写: {imit_bar} {style_imit['dialogue_ratio']*100:.1f}%")
        
        lines.append("  平均句长:")
        max_sent_len = max(style_orig['avg_sentence_length'], style_imit['avg_sentence_length'], 1)
        orig_bar = "█" * int(style_orig['avg_sentence_length'] / max_sent_len * 40)
        imit_bar = "█" * int(style_imit['avg_sentence_length'] / max_sent_len * 40)
        lines.append(f"    原文: {orig_bar} {style_orig['avg_sentence_length']:.1f}字")
        lines.append(f"    仿写: {imit_bar} {style_imit['avg_sentence_length']:.1f}字")
        
        lines.append("\n" + "=" * 80)
        
        return '\n'.join(lines)


def test_similarity_comparator():
    """测试相似度对比器"""
    print("\n" + "=" * 80)
    print("文本相似度对比模块测试")
    print("=" * 80)
    
    comparator = TextSimilarityComparator()
    
    original = """
扬州境内，江宁郡，宜城。
宜城境内有一座大山，名为大延山，在大延山山脚有着一座庄子，名为林家庄。

整个庄子家家户户靠的都很近，宛如一个整体。在整个林家庄的外围，还有着一大片的高达九尺的木栅栏。
有这木栅栏保护，山上的狼群也不能轻易的进入庄子吃人了。

林家庄，其中一户人家庭院内，正聚集着十数人。
其中一个年近三十的短衫壮汉正焦急地在屋门外徘徊。

"永林，别在那晃来晃去的。"严肃的声音响起，说话的是一头发花白，却虎背熊腰的老者。

"师傅，我……"那短衫壮汉却不知道该说什么。
    """
    
    imitated = """
扬州境内，江宁郡，宜城。
宜城境内有一座大山，名为大延山，在大延山山脚有着一座庄子，名为林家村。

整个村子家家户户靠的都很近，宛如一个整体。在整个林家村的外围，还有着一大片的高达九尺的木栅栏。
有这木栅栏保护，山上的狼群也不能轻易的进入村子吃人了。

林家村，其中一户人家庭院内，正聚集着十数人。
其中一个年近三十的短衫壮汉正焦急地在屋门外徘徊。

"永林，别在那晃来晃去的。"严肃的声音响起，说话的是一头发花白，却虎背熊腰的老者。

"师傅，我……"那短衫壮汉却不知道该说什么。
    """
    
    very_different = """
在一个遥远的王国里，有一位年轻的勇士。
他名叫林凡，是村子里最出色的猎人。
有一天，他离开了家乡，踏上了冒险的旅程。
在旅途中，他遇到了许多挑战和困难。
但是他从未放弃，一直勇往直前。
    """
    
    print("\n【测试1: 高度相似文本对比】")
    report = comparator.calculate_similarity(original, imitated)
    print(f"  综合相似度: {report.overall_similarity*100:.2f}%")
    print(f"  文本相似度: {report.text_similarity*100:.2f}%")
    print(f"  结构相似度: {report.structural_similarity*100:.2f}%")
    print(f"  词汇相似度: {report.vocabulary_similarity*100:.2f}%")
    print(f"  风格相似度: {report.style_similarity*100:.2f}%")
    
    print("\n【测试2: 差异较大文本对比】")
    report2 = comparator.calculate_similarity(original, very_different)
    print(f"  综合相似度: {report2.overall_similarity*100:.2f}%")
    print(f"  文本相似度: {report2.text_similarity*100:.2f}%")
    print(f"  结构相似度: {report2.structural_similarity*100:.2f}%")
    print(f"  词汇相似度: {report2.vocabulary_similarity*100:.2f}%")
    print(f"  风格相似度: {report2.style_similarity*100:.2f}%")
    
    print("\n【测试3: 生成详细报告】")
    report_text = comparator.generate_report(report, "原文", "仿写文本（高度相似）")
    print(report_text)
    
    print("\n【测试4: 可视化对比】")
    viz = comparator.visualize_comparison(original, imitated)
    print(viz)
    
    print("\n" + "=" * 80)
    print("测试完成")
    print("=" * 80)


if __name__ == "__main__":
    test_similarity_comparator()
