#!/usr/bin/env python
"""
仿写小说软件 - 集成测试脚本
测试所有核心模块的功能
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_parser_module():
    """测试小说解析模块"""
    print("\n" + "="*60)
    print("测试1: 小说解析模块")
    print("="*60)
    
    from modules.parser import NovelParser, Chapter, NovelMetadata
    
    parser = NovelParser()
    
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
    """
    
    try:
        metadata = parser.parse_content(test_content, "测试小说", "测试作者")
        print(f"✓ 解析成功")
        print(f"  标题: {metadata.title}")
        print(f"  作者: {metadata.author}")
        print(f"  章节数: {metadata.total_chapters}")
        print(f"  总字数: {metadata.total_words}")
        return True
    except Exception as e:
        print(f"✗ 解析失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_macro_architecture_module():
    """测试宏观架构分析模块"""
    print("\n" + "="*60)
    print("测试2: 宏观架构分析模块")
    print("="*60)
    
    from modules.macro_architecture import MacroArchitectureAnalyzer
    
    analyzer = MacroArchitectureAnalyzer()
    
    test_content = """
    在这个修仙世界中，共分为八大境界：凡人、炼气、筑基、金丹、元婴、化神、渡劫、真仙。
    
    青云门是北域最大的修仙门派，位于青云山脉之中。掌门人清风真人已达到元婴境界。
    
    据说千年前，天地灵气充沛，修士可以轻易飞升仙界。
    
    李云是青云门外门弟子，刚刚踏入炼气境界。他住在青云山脚下的青云镇。
    
    天元城中有一个神秘的黑风教，据说他们修炼的是禁忌功法。
    """
    
    try:
        architecture = analyzer.analyze(test_content)
        print(f"✓ 分析成功")
        print(f"  境界数: {len(architecture.power_levels)}")
        print(f"  势力数: {len(architecture.factions)}")
        print(f"  地点数: {len(architecture.locations)}")
        return True
    except Exception as e:
        print(f"✗ 分析失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_character_analyzer_module():
    """测试人物分析模块"""
    print("\n" + "="*60)
    print("测试3: 人物分析模块")
    print("="*60)
    
    from modules.character_analyzer import CharacterAnalyzer
    
    analyzer = CharacterAnalyzer()
    
    test_content = """
    李云（主角），是一个年轻的修仙者，他勇敢无畏，但也有些冲动。
    
    李云和他的师父清风真人是师徒关系，清风真人对他悉心教导。
    
    李云有一个好朋友叫张小凡，两人一起在青云门修炼。
    
    李云渴望变得强大，他想要成为最强的修士，打破自己的命运。
    
    小红是青云门的师姐，她聪明伶俐，待人温柔。
    """
    
    try:
        characters = analyzer.analyze(test_content)
        print(f"✓ 分析成功")
        print(f"  人物数: {len(characters)}")
        for char in characters[:3]:
            print(f"    - {char.name}: {char.importance}")
        return True
    except Exception as e:
        print(f"✗ 分析失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_style_extractor_module():
    """测试文风特征提取模块"""
    print("\n" + "="*60)
    print("测试4: 文风特征提取模块")
    print("="*60)
    
    from modules.style_extractor import StyleFeatureExtractor
    
    extractor = StyleFeatureExtractor()
    
    test_content = """
    清晨的阳光洒落在青云山上，只见云雾缭绕，宛如仙境。
    
    李云站在山巅，老子心中豪情万丈。
    
    "师父，今天的修炼要做什么？"李云问道。
    
    清风真人捋了捋胡须，笑道："今日你便随为师前往天元城历练。"
    
    突然，一道黑影从林中窜出！
    
    李云不由得心中一紧，但他没有退缩。
    
    首先，我们要明白修炼的重要性。
    
    其次，修炼需要坚持不懈。
    
    最后，修炼必须要有坚定的信念。
    
    综上所述，修炼是人生最重要的事情。
    """
    
    try:
        features = extractor.extract_features(test_content)
        print(f"✓ 提取成功")
        print(f"  风格数: {len(features.writing_styles)}")
        print(f"  AI指示词: {len(features.ai_indicators)}个")
        
        de_ai_score = extractor.check_de_ai_score(test_content)
        print(f"  去AI评分: {de_ai_score:.2f}/100")
        return True
    except Exception as e:
        print(f"✗ 提取失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_text_concretizer_module():
    """测试文本具体化转换模块"""
    print("\n" + "="*60)
    print("测试5: 文本具体化转换模块")
    print("="*60)
    
    from modules.text_concretizer import TextConcretizer
    
    concretizer = TextConcretizer()
    
    test_texts = [
        "小红很紧张，她站在那里不知所措。",
        "李云很愤怒，他的脸涨得通红。",
        "他很快地跑了过来。",
        "首先，我们要明白这个道理。其次，要付诸行动。最后，才能成功。"
    ]
    
    try:
        for i, text in enumerate(test_texts):
            result = concretizer.concretize_text(text)
            print(f"  测试{i+1}:")
            print(f"    原文: {text[:30]}...")
            print(f"    结果: {result[:50]}...")
        print(f"✓ 具体化成功")
        return True
    except Exception as e:
        print(f"✗ 具体化失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_fight_generator_module():
    """测试打斗场景生成模块"""
    print("\n" + "="*60)
    print("测试6: 打斗场景生成模块")
    print("="*60)
    
    from modules.fight_generator import FightSceneGenerator, Combatant
    
    generator = FightSceneGenerator()
    
    protagonist = Combatant(
        name='李云',
        power_level='筑基境',
        weapon='长剑',
        fighting_style='剑术精湛，招招狠辣',
        special_abilities=['剑气', '御剑术']
    )
    
    antagonist = Combatant(
        name='黑衣人',
        power_level='筑基境',
        weapon='弯刀',
        fighting_style='刀法诡异，出招狠辣',
        special_abilities=['暗器']
    )
    
    context = {
        'location': '荒野',
        'time': '深夜',
        'cause': '争夺宝物'
    }
    
    try:
        scene = generator.generate_fight_scene(
            [protagonist, antagonist],
            context,
            intensity='medium',
            min_length=500
        )
        print(f"✓ 生成成功")
        print(f"  长度: {len(scene)}字")
        print(f"  预览: {scene[:100]}...")
        return True
    except Exception as e:
        print(f"✗ 生成失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_climax_generator_module():
    """测试高潮生成模块"""
    print("\n" + "="*60)
    print("测试7: 高潮生成模块")
    print("="*60)
    
    from modules.climax_generator import ClimaxGenerator
    
    generator = ClimaxGenerator()
    
    try:
        climax = generator.generate_climax(
            climax_type='battle',
            chapter=10,
            context={'protagonist': '李云', 'antagonist': '清风真人'},
            protagonist='李云',
            antagonist='清风真人'
        )
        print(f"✓ 生成成功")
        print(f"  类型: {climax.climax_type}")
        print(f"  标题: {climax.title}")
        print(f"  强度: {climax.intensity}/5")
        return True
    except Exception as e:
        print(f"✗ 生成失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_word_count_controller_module():
    """测试字数控制模块"""
    print("\n" + "="*60)
    print("测试8: 字数控制模块")
    print("="*60)
    
    from modules.word_count_controller import WordCountController
    
    controller = WordCountController()
    
    try:
        target = controller.calculate_target(3000)
        print(f"✓ 计算成功")
        print(f"  目标字数: {target.target}")
        print(f"  可接受范围: [{target.min_acceptable}, {target.max_acceptable}]")
        
        short_text = "李云很紧张。"
        expanded = controller.expand_text(short_text, target)
        print(f"  扩展测试: {len(short_text)}字 -> {len(expanded)}字")
        
        return True
    except Exception as e:
        print(f"✗ 控制失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_swear_handler_module():
    """测试脏话处理模块"""
    print("\n" + "="*60)
    print("测试9: 脏话处理模块")
    print("="*60)
    
    from modules.swear_handler import SwearWordHandler
    
    handler = SwearWordHandler()
    
    try:
        emotions = ['愤怒', '蔑视', '惊讶', '疼痛', '兴奋']
        for emotion in emotions:
            swears = handler.select_swear_words(emotion)
            print(f"  {emotion}: {swears}")
        
        dialogue = "你给我等着！"
        result = handler.insert_swear_into_dialogue(dialogue, "愤怒")
        print(f"  对话插入: \"{dialogue}\" -> \"{result}\"")
        
        print(f"✓ 处理成功")
        return True
    except Exception as e:
        print(f"✗ 处理失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """运行所有测试"""
    print("\n" + "#"*70)
    print("#"*10 + " 仿写小说软件 - 集成测试 " + "#"*10)
    print("#"*70)
    
    tests = [
        ("小说解析模块", test_parser_module),
        ("宏观架构分析模块", test_macro_architecture_module),
        ("人物分析模块", test_character_analyzer_module),
        ("文风特征提取模块", test_style_extractor_module),
        ("文本具体化转换模块", test_text_concretizer_module),
        ("打斗场景生成模块", test_fight_generator_module),
        ("高潮生成模块", test_climax_generator_module),
        ("字数控制模块", test_word_count_controller_module),
        ("脏话处理模块", test_swear_handler_module),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"\n✗ {name}测试异常: {e}")
            results.append((name, False))
    
    print("\n" + "="*70)
    print("测试汇总")
    print("="*70)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for name, success in results:
        status = "✓ 通过" if success else "✗ 失败"
        print(f"  {name}: {status}")
    
    print()
    print(f"总计: {passed}/{total} 通过 ({(passed/total*100):.1f}%)")
    
    if passed == total:
        print("\n🎉 所有测试通过！仿写小说软件已准备就绪。")
        return 0
    else:
        print(f"\n⚠️  有 {total-passed} 个测试失败，请检查。")
        return 1

if __name__ == "__main__":
    sys.exit(main())
