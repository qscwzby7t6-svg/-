#!/usr/bin/env python
"""
仿写文字与原文相似度对比测试
使用多种算法对比仿写文本与原文的相似度
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """主函数"""
    print("\n" + "="*80)
    print("仿写文字与原文相似度对比测试")
    print("="*80)
    
    from modules.similarity_comparator import TextSimilarityComparator
    
    comparator = TextSimilarityComparator()
    
    print("\n【第一组测试：高度相似文本】")
    print("-" * 80)
    
    original1 = """
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
    
    imitated1 = """
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
    
    report1 = comparator.calculate_similarity(original1, imitated1)
    print(f"综合相似度: {report1.overall_similarity*100:.2f}%")
    print(f"文本相似度: {report1.text_similarity*100:.2f}%")
    print(f"结构相似度: {report1.structural_similarity*100:.2f}%")
    print(f"词汇相似度: {report1.vocabulary_similarity*100:.2f}%")
    print(f"风格相似度: {report1.style_similarity*100:.2f}%")
    
    print("\n【第二组测试：中等相似文本（仅修改少量词汇）】")
    print("-" * 80)
    
    original2 = """
扬州境内，江宁郡，宜城。
宜城境内有一座大山，名为大延山，在大延山山脚有着一座庄子，名为林家庄。

整个庄子家家户户靠的都很近，宛如一个整体。
    """
    
    imitated2 = """
扬州境内，江宁郡，宜城。
宜城境内有一座高山，名为大延山，在大延山脚下有一座庄子，名为林家村。

整个村子家家户户靠的都很近，宛若一个整体。
    """
    
    report2 = comparator.calculate_similarity(original2, imitated2)
    print(f"综合相似度: {report2.overall_similarity*100:.2f}%")
    print(f"文本相似度: {report2.text_similarity*100:.2f}%")
    print(f"结构相似度: {report2.structural_similarity*100:.2f}%")
    print(f"词汇相似度: {report2.vocabulary_similarity*100:.2f}%")
    print(f"风格相似度: {report2.style_similarity*100:.2f}%")
    
    print("\n【第三组测试：完全不同的文本】")
    print("-" * 80)
    
    original3 = """
扬州境内，江宁郡，宜城。
宜城境内有一座大山，名为大延山。
    """
    
    imitated3 = """
在一个遥远的王国里，有一位年轻的勇士。
他名叫林凡，是村子里最出色的猎人。
有一天，他离开了家乡，踏上了冒险的旅程。
    """
    
    report3 = comparator.calculate_similarity(original3, imitated3)
    print(f"综合相似度: {report3.overall_similarity*100:.2f}%")
    print(f"文本相似度: {report3.text_similarity*100:.2f}%")
    print(f"结构相似度: {report3.structural_similarity*100:.2f}%")
    print(f"词汇相似度: {report3.vocabulary_similarity*100:.2f}%")
    print(f"风格相似度: {report3.style_similarity*100:.2f}%")
    
    print("\n【详细对比报告生成】")
    print("-" * 80)
    
    report_text = comparator.generate_report(report2, "原文", "仿写文本（中等相似）")
    print(report_text)
    
    print("\n【可视化对比】")
    print("-" * 80)
    
    viz = comparator.visualize_comparison(original2, imitated2)
    print(viz)
    
    print("\n【测试4：实际仿写场景模拟】")
    print("-" * 80)
    
    print("\n场景：原文 -> 抽象化 -> 具体化 的相似度变化")
    
    original_text = """
林凡很紧张，他站在那里不知所措。
李云很愤怒，脸色涨得通红。
他很快地跑了过来。
    """
    
    abstracted_text = """
林凡感到紧张的情绪，站在那里显得局促不安。
李云表现出愤怒的情感，脸部呈现红色的状态。
他以较快的速度完成了跑的动作。
    """
    
    concretized_text = """
林凡手足无措地站在那里，双手紧紧地拧着衣角，指关节因用力而泛白。
李云脸色铁青，双拳紧握，指关节咔咔作响，眼中几乎要喷出火来。
他脚尖一点，身形暴起，快如闪电般冲了过来。
    """
    
    print("\n原文 -> 抽象化:")
    report_a = comparator.calculate_similarity(original_text, abstracted_text)
    print(f"  相似度: {report_a.overall_similarity*100:.2f}%")
    print(f"  说明: 改变了表达方式，保留核心含义")
    
    print("\n原文 -> 具体化:")
    report_b = comparator.calculate_similarity(original_text, concretized_text)
    print(f"  相似度: {report_b.overall_similarity*100:.2f}%")
    print(f"  说明: 丰富了细节描写，增加了新元素")
    
    print("\n抽象化 -> 具体化:")
    report_c = comparator.calculate_similarity(abstracted_text, concretized_text)
    print(f"  相似度: {report_c.overall_similarity*100:.2f}%")
    print(f"  说明: 都是对原文的转换，但方向不同")
    
    print("\n【相似度评分标准说明】")
    print("-" * 80)
    print("90-100%: 高度相似，几乎逐字对应")
    print("70-89%:  较高相似，保持了核心内容和结构")
    print("50-69%:  中等相似，部分内容和风格相似")
    print("30-49%:  较低相似，仅保留少量共同元素")
    print("0-29%:   极低相似，内容和风格差异显著")
    
    print("\n【防侵权建议】")
    print("-" * 80)
    print("1. 相似度>80%: 建议增加原创内容，降低侵权风险")
    print("2. 相似度60-80%: 可接受，但应确保核心情节的独特性")
    print("3. 相似度<60%: 原创性较好，但仍需注意核心设定的独特性")
    
    print("\n" + "="*80)
    print("相似度对比测试完成！")
    print("="*80)
    
    return report1, report2, report3


if __name__ == "__main__":
    results = main()
