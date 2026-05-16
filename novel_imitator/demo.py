#!/usr/bin/env python
"""
仿写小说软件 - 快速演示
展示核心功能的实际效果
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def demo_text_concretization():
    """演示文本具体化"""
    print("\n" + "="*70)
    print("演示1: 文本具体化 - 将抽象描述转为具体画面")
    print("="*70)
    
    from modules.text_concretizer import TextConcretizer
    
    concretizer = TextConcretizer()
    
    examples = [
        ("小红很紧张", "情感具体化"),
        ("李云很愤怒", "情感具体化"),
        ("他很快地跑了过来", "速度具体化"),
        ("看到这一幕，他很惊讶", "惊讶具体化")
    ]
    
    for text, desc in examples:
        result = concretizer.concretize_text(text)
        print(f"\n{desc}:")
        print(f"  原文: {text}")
        print(f"  结果: {result}")

def demo_de_ai():
    """演示去AI化"""
    print("\n" + "="*70)
    print("演示2: 去AI化 - 移除AI特征词和结构化表达")
    print("="*70)
    
    from modules.style_extractor import StyleFeatureExtractor
    
    extractor = StyleFeatureExtractor()
    
    ai_text = """
    首先，我们要明白修炼的重要性。
    
    其次，修炼需要坚持不懈的努力。
    
    第三，还需要正确的方法。
    
    最后，也是最关键的，必须要有坚定的信念。
    
    综上所述，这四点缺一不可。
    
    值得注意的是，每个人的情况都不同。
    """
    
    print("\n原文（包含AI特征）:")
    print(ai_text)
    
    de_ai_score = extractor.check_de_ai_score(ai_text)
    print(f"\n去AI评分: {de_ai_score:.0f}/100")
    
    cleaned = extractor.remove_ai_patterns(ai_text)
    print(f"\n清理后:")
    print(cleaned)

def demo_fight_scene():
    """演示打斗场景生成"""
    print("\n" + "="*70)
    print("演示3: 打斗场景生成 - 具体化的战斗描写")
    print("="*70)
    
    from modules.fight_generator import FightSceneGenerator, Combatant
    
    generator = FightSceneGenerator()
    
    protagonist = Combatant(
        name='李云',
        power_level='筑基境',
        weapon='长剑',
        fighting_style='剑法凌厉',
        special_abilities=['剑气']
    )
    
    antagonist = Combatant(
        name='黑衣人',
        power_level='筑基境',
        weapon='弯刀',
        fighting_style='刀法诡异',
        special_abilities=['暗器']
    )
    
    scene = generator.generate_fight_scene(
        [protagonist, antagonist],
        context={'location': '荒野', 'time': '深夜'},
        intensity='high',
        min_length=800
    )
    
    print(f"\n生成的打斗场景 ({len(scene)}字):")
    print("-" * 70)
    print(scene[:500])
    print("...")
    print("-" * 70)

def demo_climax():
    """演示高潮生成"""
    print("\n" + "="*70)
    print("演示4: 高潮生成 - 每10章的小高潮/小爆发")
    print("="*70)
    
    from modules.climax_generator import ClimaxGenerator
    
    generator = ClimaxGenerator()
    
    climax_types = ['battle', 'revelation', 'breakthrough', 'betrayal']
    
    for climax_type in climax_types:
        climax = generator.generate_climax(
            climax_type=climax_type,
            chapter=10,
            context={'protagonist': '李云'},
            protagonist='李云',
            antagonist='清风真人'
        )
        
        print(f"\n【{climax.title}】 - {climax_type.upper()}")
        print(f"强度: {'⭐' * climax.intensity}")
        print(climax.content[:200] + "...")

def demo_word_count():
    """演示字数控制"""
    print("\n" + "="*70)
    print("演示5: 字数控制 - 确保章节字数±10%")
    print("="*70)
    
    from modules.word_count_controller import WordCountController
    
    controller = WordCountController()
    
    target = controller.calculate_target(3000)
    print(f"\n目标字数: {target.target}")
    print(f"可接受范围: [{target.min_acceptable}, {target.max_acceptable}]")
    
    short_text = "李云很紧张。"
    expanded = controller.expand_text(short_text, target)
    
    print(f"\n测试文本: {short_text} ({len(short_text)}字)")
    print(f"扩展后: {expanded[:100]}... ({len(expanded)}字)")

def demo_swear():
    """演示脏话处理"""
    print("\n" + "="*70)
    print("演示6: 脏话处理 - 适当场景添加口语化表达")
    print("="*70)
    
    from modules.swear_handler import SwearWordHandler
    
    handler = SwearWordHandler()
    
    dialogues = [
        ("你给我等着！", "愤怒"),
        ("这不可能！", "惊讶"),
        ("太厉害了！", "兴奋"),
        ("就这？", "蔑视")
    ]
    
    for dialogue, emotion in dialogues:
        result = handler.insert_swear_into_dialogue(dialogue, emotion)
        print(f"\n{emotion}: \"{dialogue}\"")
        print(f"  -> \"{result}\"")

def main():
    """主函数"""
    print("\n" + "#"*70)
    print("#"*15 + " 仿写小说软件 - 功能演示 " + "#"*15)
    print("#"*70)
    
    demos = [
        ("文本具体化", demo_text_concretization),
        ("去AI化", demo_de_ai),
        ("打斗场景生成", demo_fight_scene),
        ("高潮生成", demo_climax),
        ("字数控制", demo_word_count),
        ("脏话处理", demo_swear)
    ]
    
    for name, demo_func in demos:
        try:
            demo_func()
        except Exception as e:
            print(f"\n演示失败: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*70)
    print("演示完成！")
    print("="*70)
    print("\n使用方法:")
    print("  python integration_test.py  # 运行集成测试")
    print("  python -m novel_imitator --file novel.txt  # 仿写小说")
    print("\n查看文档: cat README.md")

if __name__ == "__main__":
    main()
