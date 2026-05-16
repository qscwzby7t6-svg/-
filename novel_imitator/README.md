# 仿写小说软件

## 概述

这是一个功能全面的**小说仿写工具**，能够1:1风格级复刻原版小说的：
- 宏观架构和章节架构
- 世界观和力量系统
- 伏笔和人物性格
- 成长线和叙事风格

## 核心特性

### ✅ 去AI化
- 自动识别并移除AI特征词（首先、其次、最后、综上所述等）
- 提取原文独特表达方式
- 保持人类写作的自然流畅

### ✅ 抽象描述具体化
**示例：**
- 原文：`小红很紧张`
- 转换：`小红手足无措地站在那里，双手紧紧地拧着衣角，指关节因用力而泛白`

### ✅ 适当口语化
根据情绪和场景自动添加合适的口语表达：
- 愤怒：妈的、他妈的、混账
- 蔑视：切、呸、小样
- 兴奋：牛逼、干得漂亮

### ✅ 字数控制
- 章节字数上下相差10%以内
- 智能扩展和缩减算法
- 字数统计报告

### ✅ 高潮设置
- 每10章包含小高潮/小爆发
- 多种高潮类型：战斗、揭示、背叛、突破等
- 自动情节增强

### ✅ 动作场景具体化
- 详细的打斗动作描写
- 身体部位动作分解
- 战斗音效和过渡

## 安装

```bash
pip install -r requirements.txt
```

## 使用方法

### 命令行使用

```bash
# 基本用法
python -m novel_imitator --file novel.txt --output ./output

# 指定主角名和章节数
python -m novel_imitator --file novel.txt --protagonist "李云" --chapters 50

# 使用API密钥（推荐）
python -m novel_imitator --file novel.txt --api-key YOUR_API_KEY

# 交互模式
python -m novel_imitator
```

### Python API使用

```python
from novel_imitator.core.controller import NovelImitatorController

# 初始化控制器
controller = NovelImitatorController()

# 运行完整仿写
result = controller.run_full_imitation(
    source_file='novel.txt',
    source_title='小说标题',
    source_author='作者名',
    protagonist_name='主角名',
    genre='xianxia',
    total_chapters=10
)

if result.success:
    # 保存结果
    controller.save_result(result, 'output.txt')
    
    # 查看统计
    print(result.word_count_report)
```

## 项目结构

```
novel_imitator/
├── config.py                 # 配置模块
├── core/
│   └── controller.py        # 主控制器
├── modules/
│   ├── parser.py            # 小说解析
│   ├── macro_architecture.py # 宏观架构分析
│   ├── character_analyzer.py # 人物分析
│   ├── chapter_structure.py  # 章节结构分析
│   ├── style_extractor.py   # 文风特征提取
│   ├── deepseek_client.py   # DeepSeek API集成
│   ├── text_concretizer.py  # 文本具体化
│   ├── fight_generator.py   # 打斗场景生成
│   ├── swear_handler.py     # 脏话处理
│   ├── climax_generator.py  # 高潮生成
│   └── word_count_controller.py # 字数控制
├── cli/
│   └── __init__.py          # 命令行界面
└── integration_test.py       # 集成测试
```

## 配置说明

配置文件位于 `~/.novel_imitator/config.json`

```json
{
  "model": {
    "deepseek_api_key": "your-api-key",
    "temperature": 0.7,
    "max_tokens": 4000
  },
  "style": {
    "avoid_ai_phrases": [
      "首先", "其次", "最后", "综上所述"
    ]
  },
  "word_count": {
    "target": 3000,
    "tolerance": 0.1
  }
}
```

## 模块说明

### 1. 小说解析模块 (parser)
- 解析TXT格式小说
- 章节分割
- 人物和地点提取
- 章节统计

### 2. 宏观架构分析 (macro_architecture)
- 力量体系识别
- 势力门派分析
- 世界规则提取
- 伏笔识别

### 3. 人物分析 (character_analyzer)
- 人物性格分析
- 成长线追踪
- 关系网络构建
- 目标动机分析

### 4. 文风特征提取 (style_extractor)
- 写作风格识别
- AI特征词检测
- 独特表达提取
- 去AI化评分

### 5. 文本具体化 (text_concretizer)
- 情感词具体化
- 动作细节化
- 感官描写增强
- AI模式移除

### 6. 打斗场景生成 (fight_generator)
- 战斗动作编排
- 招式细节描写
- 战斗节奏控制
- 伤害效果描述

### 7. 脏话处理 (swear_handler)
- 情绪识别
- 词汇选择
- 上下文适配
- 类型调整

### 8. 高潮生成 (climax_generator)
- 高潮类型选择
- 铺垫生成
- 爆发点设置
- 后果描述

### 9. 字数控制 (word_count_controller)
- 目标计算
- 智能扩展
- 精准缩减
- 合规检查

## 测试

```bash
# 运行集成测试
python integration_test.py

# 测试特定模块
python modules/parser.py
python modules/fight_generator.py
```

## 注意事项

1. **版权问题**：仿写作品仅供学习研究使用，切勿用于商业目的或侵权行为
2. **API密钥**：建议使用DeepSeek API以获得更好的生成效果
3. **本地模式**：无API密钥时使用本地模板生成，效果可能有限
4. **字数控制**：系统会尽量保持字数在目标范围内（±10%）

## 许可证

MIT License
