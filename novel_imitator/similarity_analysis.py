#!/usr/bin/env python
"""
仿写相似度综合分析报告
整合所有相似度分析功能，生成完整的对比报告
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_comprehensive_report():
    """创建综合分析报告"""
    
    print("\n" + "="*80)
    print("仿写文字与原文相似度综合分析报告")
    print("="*80)
    
    from modules.similarity_comparator import TextSimilarityComparator
    from modules.style_extractor import StyleFeatureExtractor
    from modules.text_concretizer import TextConcretizer
    
    comparator = TextSimilarityComparator()
    style_extractor = StyleFeatureExtractor()
    concretizer = TextConcretizer()
    
    print("\n【第一部分：核心算法测试】")
    print("-"*80)
    
    original = """
扬州境内，江宁郡，宜城。
宜城境内有一座大山，名为大延山，在大延山山脚有着一座庄子，名为林家庄。

整个庄子家家户户靠的都很近，宛如一个整体。在整个林家庄的外围，还有着一大片的高达九尺的木栅栏。
有这木栅栏保护，山上的狼群也不能轻易的进入庄子吃人了。

林家庄，其中一户人家庭院内，正聚集着十数人。
其中一个年近三十的短衫壮汉正焦急地在屋门外徘徊。

"永林，别在那晃来晃去的。"严肃的声音响起，说话的是一头发花白，却虎背熊腰的老者。

"师傅，我……"那短衫壮汉却不知道该说什么。

他没法不紧张，他的妻子正在里面生孩子。
    """
    
    imitated = """
扬州境内，江宁郡，宜城。
宜城境内有一座大山，名为大延山，在大延山山脚有着一座庄子，名为林家庄。

整个庄子家家户户靠的都很近，宛如一个整体。在整个林家庄的外围，还有着一大片的高达九尺的木栅栏。
有这木栅栏保护，山上的狼群也不能轻易的进入庄子吃人了。

林家庄，其中一户人家庭院内，正聚集着十数人。
其中一个年近三十的短衫壮汉正焦急地在屋门外徘徊。

"永林，别在那晃来晃去的。"严肃的声音响起，说话的是一头发花白，却虎背熊腰的老者。

"师傅，我……"那短衫壮汉却不知道该说什么。

他没法不紧张，他的妻子正在里面生孩子。
    """
    
    print("\n测试文本1: 高度相似（仅标点差异）")
    report1 = comparator.calculate_similarity(original, imitated)
    print(f"  综合相似度: {report1.overall_similarity*100:.2f}%")
    print(f"  各维度:")
    print(f"    - 文本相似度: {report1.text_similarity*100:.2f}%")
    print(f"    - 结构相似度: {report1.structural_similarity*100:.2f}%")
    print(f"    - 词汇相似度: {report1.vocabulary_similarity*100:.2f}%")
    print(f"    - 风格相似度: {report1.style_similarity*100:.2f}%")
    
    modified = """
扬州境内，江宁郡，宜城。
宜城境内有一座高山，名为大延山，在大延山脚下有一座庄子，名为林家村。

整个村子家家户户靠的都很近，宛若一个整体。
    """
    
    print("\n测试文本2: 中等相似（词汇替换）")
    report2 = comparator.calculate_similarity(original[:200], modified)
    print(f"  综合相似度: {report2.overall_similarity*100:.2f}%")
    print(f"  各维度:")
    print(f"    - 文本相似度: {report2.text_similarity*100:.2f}%")
    print(f"    - 结构相似度: {report2.structural_similarity*100:.2f}%")
    print(f"    - 词汇相似度: {report2.vocabulary_similarity*100:.2f}%")
    print(f"    - 风格相似度: {report2.style_similarity*100:.2f}%")
    
    print("\n【第二部分：具体化转换相似度分析】")
    print("-"*80)
    
    abstract = "林凡很紧张，他站在那里不知所措。"
    concrete = concretizer.concretize_text(abstract)
    
    print(f"\n原文: {abstract}")
    print(f"具体化后: {concrete[:60]}...")
    
    report3 = comparator.calculate_similarity(abstract, concrete)
    print(f"\n相似度: {report3.overall_similarity*100:.2f}%")
    print("说明: 具体化增加了大量细节，相似度自然降低，但这正是期望的效果")
    
    print("\n【第三部分：去AI化效果评估】")
    print("-"*80)
    
    ai_text = """
首先，我们要明白修炼的重要性。
其次，修炼需要坚持不懈的努力。
第三，还需要正确的方法。
最后，也是最关键的，必须要有坚定的信念。
综上所述，这四点缺一不可。
    """
    
    de_ai_score = style_extractor.check_de_ai_score(ai_text)
    print(f"\nAI特征文本评分: {de_ai_score:.1f}/100")
    print("说明: 分数越低表示AI特征越明显")
    
    cleaned = concretizer.remove_ai_patterns(ai_text)
    cleaned_score = style_extractor.check_de_ai_score(cleaned)
    print(f"\n清理后评分: {cleaned_score:.1f}/100")
    print(f"清理后内容: {cleaned}")
    
    print("\n【第四部分：综合对比报告】")
    print("-"*80)
    
    comprehensive_report = comparator.generate_report(
        report2, 
        "原文（《九鼎记》风格）", 
        "仿写文本"
    )
    print(comprehensive_report)
    
    print("\n【第五部分：可视化对比】")
    print("-"*80)
    
    viz = comparator.visualize_comparison(original[:200], modified)
    print(viz)
    
    print("\n【第六部分：仿写质量评估矩阵】")
    print("-"*80)
    
    print("\n┌─────────────────────┬───────────┬───────────┬───────────┐")
    print("│ 评估维度             │ 原文      │ 仿写      │ 差异      │")
    print("├─────────────────────┼───────────┼───────────┼───────────┤")
    
    from modules.similarity_comparator import TextSimilarityComparator
    comp = TextSimilarityComparator()
    
    orig_stats = comp._analyze_structure(original[:200])
    imit_stats = comp._analyze_structure(modified)
    
    orig_style = comp._analyze_style(original[:200])
    imit_style = comp._analyze_style(modified)
    
    print(f"│ 字数                 │ {orig_stats['char_length']:8d} │ {imit_stats['char_length']:8d} │ {abs(orig_stats['char_length']-imit_stats['char_length']):8d} │")
    print(f"│ 词数                 │ {orig_stats['word_count']:8d} │ {imit_stats['word_count']:8d} │ {abs(orig_stats['word_count']-imit_stats['word_count']):8d} │")
    print(f"│ 句子数               │ {orig_stats['sentence_count']:8d} │ {imit_stats['sentence_count']:8d} │ {abs(orig_stats['sentence_count']-imit_stats['sentence_count']):8d} │")
    print(f"│ 平均句长             │ {orig_stats['avg_sentence_len']:8.1f} │ {imit_stats['avg_sentence_len']:8.1f} │ {abs(orig_stats['avg_sentence_len']-imit_stats['avg_sentence_len']):8.1f} │")
    print(f"│ 对话比例             │ {orig_style['dialogue_ratio']*100:8.2f}% │ {imit_style['dialogue_ratio']*100:8.2f}% │ {abs(orig_style['dialogue_ratio']-imit_style['dialogue_ratio'])*100:8.2f}% │")
    print("└─────────────────────┴───────────┴───────────┴───────────┘")
    
    print("\n【第七部分：侵权风险评估】")
    print("-"*80)
    
    risk_level = "低"
    if report2.overall_similarity > 0.9:
        risk_level = "极高"
    elif report2.overall_similarity > 0.8:
        risk_level = "高"
    elif report2.overall_similarity > 0.6:
        risk_level = "中"
    elif report2.overall_similarity > 0.4:
        risk_level = "低"
    else:
        risk_level = "极低"
    
    print(f"\n侵权风险等级: {risk_level}")
    print(f"综合相似度: {report2.overall_similarity*100:.1f}%")
    
    if risk_level == "极高":
        print("建议: 大量增加原创内容，重新构思情节")
    elif risk_level == "高":
        print("建议: 增加原创情节，修改人物名称和背景")
    elif risk_level == "中":
        print("建议: 适度调整，保持核心风格的同时增加变化")
    else:
        print("建议: 当前状态良好，保持原创性")
    
    print("\n【第八部分：优化建议汇总】")
    print("-"*80)
    
    suggestions = []
    
    if report2.text_similarity > 0.8:
        suggestions.append("文本相似度过高，建议替换更多词汇和表达方式")
    
    if report2.vocabulary_similarity > 0.8:
        suggestions.append("词汇重复较多，建议使用更多同义词和近义词")
    
    if report2.structural_similarity < 0.7:
        suggestions.append("结构差异较大，建议参考原文的段落安排")
    
    if orig_style['dialogue_ratio'] != imit_style['dialogue_ratio']:
        suggestions.append("对话比例有差异，建议调整对话描写频率")
    
    if de_ai_score < 50:
        suggestions.append("检测到AI特征词，建议移除结构化表达")
    
    if suggestions:
        print("\n发现以下需要优化的方面:")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"  {i}. {suggestion}")
    else:
        print("\n✓ 仿写质量良好，未发现明显问题")
    
    print("\n" + "="*80)
    print("综合分析报告生成完成")
    print("="*80)
    
    return {
        'report1': report1,
        'report2': report2,
        'report3': report3,
        'de_ai_score': de_ai_score,
        'cleaned_score': cleaned_score
    }


def main():
    """主函数"""
    try:
        results = create_comprehensive_report()
        
        print("\n" + "="*80)
        print("✓ 相似度对比分析完成！")
        print("="*80)
        
        print("\n主要发现:")
        print(f"  1. 高度相似文本相似度: {results['report1'].overall_similarity*100:.1f}%")
        print(f"  2. 中等相似文本相似度: {results['report2'].overall_similarity*100:.1f}%")
        print(f"  3. 具体化转换相似度: {results['report3'].overall_similarity*100:.1f}%")
        print(f"  4. AI特征检测评分: {results['de_ai_score']:.1f}/100")
        print(f"  5. 去AI化后评分: {results['cleaned_score']:.1f}/100")
        
        print("\n使用建议:")
        print("  - 仿写相似度控制在50-70%较为理想")
        print("  - 保留原风格的同时增加原创元素")
        print("  - 定期使用本工具检测侵权风险")
        
        return 0
        
    except Exception as e:
        print(f"\n✗ 分析失败: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
