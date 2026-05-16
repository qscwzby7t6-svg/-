"""
星辰变仿写测试 - 基于《星辰变》第一章进行仿写测试
"""
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

def test_imitator_with_novel():
    """使用小说内容进行仿写测试"""
    print("\n" + "#"*70)
    print("#"*15 + " 星辰变 第一章 仿写测试 " + "#"*15)
    print("#"*70)

    from core.controller import NovelImitatorController
    from modules.parser import NovelParser
    from modules.macro_architecture import MacroArchitectureAnalyzer
    from modules.character_analyzer import CharacterAnalyzer
    from modules.style_extractor import StyleFeatureExtractor
    from modules.text_concretizer import TextConcretizer
    from modules.fight_generator import FightSceneGenerator, Combatant
    from modules.climax_generator import ClimaxGenerator
    from modules.word_count_controller import WordCountController

    star_novel_content = """星辰变 第一章 秦羽

时则深冬，大雪过后，整个炎京城都披上了一层银装。炎京城极大，可容纳人口数百万，而掌控东域三郡的'镇东王'秦德的府邸便是在这炎京城。

镇东王府邸占地极广，正门日间夜间都是大大敞开，府邸正门宽广无比，足够六七人并行入内。

而在大门两侧站着两名身高两米左右的赤裸着上半身的勇猛大汉，这两名大汉犹如岩石雕刻一般，冷漠双眼扫视着过往人群，那宽厚的虎背之上正挂巨型血红色战刀。那血红色的战刀一眼看去足有一米五长。

深冬之时，雪花满地，温度低得吓人，河中都已经结冰了，可这两个大汉却赤裸着上半身。

然而这并不是最骇人的，更加骇人的是在这两个大汉旁边竟然分别有一只凶猛的老虎。

老虎全身为火焰般赤红色，体长约有两米多，那犹如铁鞭一样的尾巴猛然一扫都让空气一阵振动，虎目之中发出森冷的寒芒，这老虎正是所谓的'烈虎'。

忽然，镇东王的府邸之中走出另外两名大汉，这两名大汉同样赤裸着上半身，分别牵引着一只凶猛的烈虎，他们是来换班的。

府邸之外，炎京城的豪族贵族亦或是平民游民都自觉地绕着镇东王的府邸走开。

镇东王府邸内一幽静的小院中。

一青衣中年人正坐在石凳之上，他的腿上坐着一个可爱的小男孩。而在中年人身前正是站着十二人，这十二人或是老者，或是美妇，或是青年……但是有一点是一样的，这十二人都是一身紫衣。

"父王，你让这么多老师都来干什么呢？"才刚刚六岁的秦羽坐在自己父亲的腿上，手中乱捏着一雪球，疑惑看着自己的父亲秦德。

秦德关爱地抚摸了秦羽的脑袋，而后抬头看向十二人，淡然道："你们教导羽儿也有一段时间了，好了，别顾及什么，有什么判断就说出来吧。"

这十二人彼此相视，而后一名白须飘飘的老者上前一步，恭敬地道："禀报王爷，我们从各个方面观察，三殿下只是对奇门巧技略微有些兴趣，然而，对上位者御下之道等等，却是根本没有丝毫兴趣。根据我们的判断，三殿下不可能成为一个完美的上位者。"

仅仅凭一段日子和男孩的接触，就下了如此断言，似乎略显武断。然而秦德却是毫不怀疑。

秦德长长叹了一口气，看了看懵懂不知的秦羽，苦笑道："我能够看出来，羽儿像他娘，对于俗世权势丝毫没有兴趣，可是他在修炼一途上却是……"

秦德说到这嘎然而止，而后挥了挥手，道："这段时间麻烦你们了，你们现在可以离开王府了。"

"王爷，我等告辞！"

紫衣十二人同时躬身，而后依次出了小小幽静庄院。

此刻，庄院中只有秦德和儿子秦羽，秦德沉默不言一语，时而还看看腿上的秦羽，眼中的含义，至少六岁的秦羽还是无法明白的。

"父王他怎么了，怎么不说话了呢？"秦羽心中暗想，但是秦羽却很是乖巧地没有打搅他父亲，从小没有母亲，在秦羽心中，最重要的就是父亲，还有另外两个哥哥。

许久许久，秦德一直坐着，秦羽就一直静静坐在自己爹的腿上。

忽然，一声鹤鸣响起。

只见空中一白色仙鹤飞来，在仙鹤之上正坐着一仙风道骨的俊雅中年人，片刻仙鹤便落到院落之中。

"风兄，羽儿丹田的问题，你是否可以想办法……"秦德一看到这中年人，当即急切地站了起来询问道。

风玉子看到秦德如此，他自然知道自己的好友秦德的事情，只能叹了一口气道："王爷，我早就说过了，羽儿他在修炼一途中根本没有任何希望，他的丹田十分怪异，无法积蓄内力，自然无法修炼。如此丹田根本就是天生的，亿万人中根本无法找到一例，我风玉子也是无丝毫办法。"

听到这个结果，秦德徐徐坐下，沉思许久。

"父王？内力是什么啊，我的丹田无法积蓄内力又怎么了？刚才那些老师又说什么上位者，那是什么意思啊？"六岁的秦羽睁大了眼睛，疑惑地询问道。
"""

    print("\n" + "="*70)
    print("第一步：解析小说")
    print("="*70)

    parser = NovelParser()
    metadata = parser.parse_content(star_novel_content, "星辰变", "我吃西红柿")

    print(f"✓ 解析完成")
    print(f"  标题: {metadata.title}")
    print(f"  作者: {metadata.author}")
    print(f"  章节数: {metadata.total_chapters}")
    print(f"  总字数: {metadata.total_words}")

    print("\n" + "="*70)
    print("第二步：分析宏观架构")
    print("="*70)

    analyzer = MacroArchitectureAnalyzer()
    architecture = analyzer.analyze(star_novel_content, metadata.chapters)

    print(f"✓ 分析完成")
    print(f"\n力量体系:")
    for power in architecture.power_levels[:5]:
        print(f"  - {power.name}: {power.description}")

    print(f"\n势力门派:")
    for faction in architecture.factions[:3]:
        print(f"  - {faction.name} ({faction.type})")

    print(f"\n世界设定:")
    print(f"  - 修炼体系: {architecture.cultivation_system}")
    print(f"  - 时间设定: {architecture.time_system}")

    print(f"\n重要地点:")
    for loc in architecture.locations[:5]:
        print(f"  - {loc}")

    print("\n" + "="*70)
    print("第三步：分析人物")
    print("="*70)

    char_analyzer = CharacterAnalyzer()
    characters = char_analyzer.analyze(star_novel_content, metadata.chapters)

    print(f"✓ 分析完成，共发现 {len(characters)} 个人物")
    for char in characters[:5]:
        print(f"\n  {char.name} ({char.importance})")
        print(f"    性别: {char.gender}")
        print(f"    势力: {char.faction}")
        print(f"    性格: {[t.name for t in char.personality_traits[:3]]}")
        if char.goals:
            print(f"    目标: {char.goals[0]}")

    print("\n" + "="*70)
    print("第四步：提取文风特征")
    print("="*70)

    style_extractor = StyleFeatureExtractor()
    styles = style_extractor.extract_features(star_novel_content, metadata.chapters)

    print(f"✓ 提取完成")
    print(f"\n写作风格:")
    for style in styles.writing_styles:
        print(f"  - {style.name}: {style.value:.2f}")

    print(f"\nAI特征词 (需要避免):")
    for indicator in styles.ai_indicators[:5]:
        print(f"  - {indicator}")

    print(f"\n去AI化评分: {style_extractor.check_de_ai_score(star_novel_content):.0f}/100")

    print(f"\n独特表达:")
    for expr, count in list(styles.unique_expressions.items())[:5]:
        print(f"  - {expr}: {count}次")

    print("\n" + "="*70)
    print("第五步：文本具体化测试")
    print("="*70)

    concretizer = TextConcretizer()

    test_cases = [
        ("秦羽很紧张", "情感具体化"),
        ("一个勇猛的大汉", "人物具体化"),
        ("他很快地跑过来", "速度具体化")
    ]

    for text, desc in test_cases:
        result = concretizer.concretize_text(text)
        print(f"\n  {desc}:")
        print(f"    原文: {text}")
        print(f"    结果: {result}")

    print("\n" + "="*70)
    print("第六步：打斗场景生成测试")
    print("="*70)

    fight_gen = FightSceneGenerator()

    protagonist = Combatant(
        name="林凡",
        power_level="外功修炼者",
        weapon="战刀",
        fighting_style="外功硬功",
        special_abilities=["力量"]
    )

    antagonist = Combatant(
        name="黑衣人",
        power_level="外功巅峰",
        weapon="长枪",
        fighting_style="枪法凌厉",
        special_abilities=["暗器"]
    )

    scene = fight_gen.generate_fight_scene(
        [protagonist, antagonist],
        context={"location": "镇东王府", "time": "深夜"},
        intensity="medium",
        min_length=500
    )

    print(f"✓ 打斗场景生成完成 ({len(scene)}字)")
    print(f"\n生成内容预览:")
    print(scene[:300] + "...")

    print("\n" + "="*70)
    print("第七步：高潮生成测试")
    print("="*70)

    climax_gen = ClimaxGenerator()

    climax_types = ["battle", "revelation", "breakthrough"]
    for ctype in climax_types:
        climax = climax_gen.generate_climax(
            climax_type=ctype,
            chapter=10,
            context={"protagonist": "林凡"},
            protagonist="林凡",
            antagonist="风玉子"
        )
        print(f"\n{ctype.upper()} 高潮:")
        print(f"  标题: {climax.title}")
        print(f"  强度: {'⭐' * climax.intensity}")
        print(f"  预览: {climax.content[:100]}...")

    print("\n" + "="*70)
    print("第八步：字数控制测试")
    print("="*70)

    word_controller = WordCountController()

    target = word_controller.calculate_target(len(star_novel_content))
    print(f"目标字数: {target.target}")
    print(f"可接受范围: [{target.min_acceptable}, {target.max_acceptable}]")

    test_text = "林凡站在山巅。"
    expanded = word_controller.expand_text(test_text, target)
    print(f"\n扩展测试: {len(test_text)}字 -> {len(expanded)}字")

    print("\n" + "="*70)
    print("第九步：生成仿写内容")
    print("="*70)

    controller = NovelImitatorController()

    print("\n生成仿写章节...")

    try:
        chapter_content = controller.generate_chapter(
            chapter_number=1,
            source_chapter=metadata.chapters[0] if metadata.chapters else None
        )

        print(f"✓ 章节生成完成 ({len(chapter_content)}字)")
        print(f"\n生成内容预览:")
        print("-" * 70)
        print(chapter_content[:500])
        print("...")
        print("-" * 70)

    except Exception as e:
        print(f"✗ 生成失败: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "="*70)
    print("测试完成")
    print("="*70)

    return {
        "metadata": metadata,
        "architecture": architecture,
        "characters": characters,
        "styles": styles
    }

def generate_analysis_report(results):
    """生成分析报告"""
    print("\n" + "#"*70)
    print("#"*15 + " 分析报告 " + "#"*15)
    print("#"*70)

    metadata = results["metadata"]
    architecture = results["architecture"]
    characters = results["characters"]
    styles = results["styles"]

    print(f"""
📊 数据统计

小说标题: {metadata.title}
作者: {metadata.author}
总章节数: {metadata.total_chapters}
总字数: {metadata.total_words}
平均章节字数: {metadata.total_words // max(metadata.total_chapters, 1)}

🏗️ 宏观架构

力量体系: {len(architecture.power_levels)}个境界
势力门派: {len(architecture.factions)}个势力
重要地点: {len(architecture.locations)}个地点
修炼体系: {architecture.cultivation_system}
世界设定: {architecture.time_system}

👥 人物分析

主要人物: {len([c for c in characters if c.importance in ['protagonist', 'major']])}人
次要人物: {len([c for c in characters if c.importance == 'secondary']])}人
总人物数: {len(characters)}人

🎨 文风特征

写作风格数: {len(styles.writing_styles)}种
独特表达数: {len(styles.unique_expressions)}个
AI特征词: {len(styles.ai_indicators)}个
去AI化评分: {styles.narrative_voice.formality:.0%} (0=口语化, 1=书面化)

📝 建议

1. 保持场景描写的具体性，参考原文的细节描写方式
2. 注意人物对话的自然流畅，避免过于书面化
3. 保持修炼体系的层次分明
4. 适当使用具体化的动作描写
5. 控制章节字数在 {metadata.total_words // max(metadata.total_chapters, 1)} 字左右
""")

if __name__ == "__main__":
    results = test_imitator_with_novel()
    generate_analysis_report(results)
