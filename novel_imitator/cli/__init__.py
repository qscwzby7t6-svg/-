"""
命令行界面模块 - 提供命令行交互接口
支持文件输入、参数配置、进度显示等功能
"""
import os
import sys
import argparse
import logging
from typing import Optional, List
from pathlib import Path

from ..core.controller import NovelImitatorController
from ..config import load_config, Config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CommandLineInterface:
    """命令行界面"""
    
    def __init__(self):
        self.controller = NovelImitatorController()
        self.config = load_config()
    
    def create_parser(self) -> argparse.ArgumentParser:
        """创建参数解析器"""
        parser = argparse.ArgumentParser(
            description='小说仿写工具 - 1:1风格级复刻原版小说',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
示例:
  # 从TXT文件仿写
  python -m novel_imitator.cli --file novel.txt --output ./output

  # 从内容仿写
  python -m novel_imitator.cli --content "小说内容..." --title "小说标题"

  # 指定主角名
  python -m novel_imitator.cli --file novel.txt --protagonist "李云"

  # 批量仿写多章
  python -m novel_imitator.cli --file novel.txt --chapters 50
            """
        )
        
        parser.add_argument(
            '--file', '-f',
            type=str,
            help='源小说文件路径（支持TXT格式）'
        )
        
        parser.add_argument(
            '--content', '-c',
            type=str,
            help='源小说内容（直接输入内容）'
        )
        
        parser.add_argument(
            '--title', '-t',
            type=str,
            default='',
            help='小说标题'
        )
        
        parser.add_argument(
            '--author', '-a',
            type=str,
            default='',
            help='小说作者'
        )
        
        parser.add_argument(
            '--protagonist', '-p',
            type=str,
            default='主角',
            help='主角名字'
        )
        
        parser.add_argument(
            '--genre', '-g',
            type=str,
            default='xianxia',
            choices=['xianxia', 'wuxia', 'urban', 'xuanhuan', 'other'],
            help='小说类型（默认：xianxia）'
        )
        
        parser.add_argument(
            '--chapters', '-n',
            type=int,
            default=10,
            help='要仿写的章节数（默认：10）'
        )
        
        parser.add_argument(
            '--start-chapter', '-s',
            type=int,
            default=1,
            help='起始章节（默认：1）'
        )
        
        parser.add_argument(
            '--output', '-o',
            type=str,
            default='./output',
            help='输出目录（默认：./output）'
        )
        
        parser.add_argument(
            '--api-key',
            type=str,
            default='',
            help='DeepSeek API密钥（可选）'
        )
        
        parser.add_argument(
            '--verbose', '-v',
            action='store_true',
            help='显示详细日志'
        )
        
        parser.add_argument(
            '--version',
            action='version',
            version='%(prog)s 1.0.0'
        )
        
        return parser
    
    def run(self, args: Optional[List[str]] = None) -> int:
        """运行命令行"""
        parser = self.create_parser()
        parsed_args = parser.parse_args(args)
        
        if parsed_args.verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        
        if not parsed_args.file and not parsed_args.content:
            parser.print_help()
            print("\n错误: 请提供 --file 或 --content 参数")
            return 1
        
        if parsed_args.file and not os.path.exists(parsed_args.file):
            print(f"错误: 文件不存在: {parsed_args.file}")
            return 1
        
        print("=" * 70)
        print("小说仿写工具 v1.0.0")
        print("=" * 70)
        print()
        
        try:
            if parsed_args.api_key:
                os.environ['DEEPSEEK_API_KEY'] = parsed_args.api_key
            
            output_dir = Path(parsed_args.output)
            output_dir.mkdir(parents=True, exist_ok=True)
            
            print(f"源文件: {parsed_args.file or '直接输入内容'}")
            print(f"标题: {parsed_args.title or '未指定'}")
            print(f"作者: {parsed_args.author or '未指定'}")
            print(f"主角: {parsed_args.protagonist}")
            print(f"类型: {parsed_args.genre}")
            print(f"章节数: {parsed_args.chapters}")
            print(f"输出目录: {output_dir.absolute()}")
            print()
            
            print("开始仿写...")
            print()
            
            result = self.controller.run_full_imitation(
                source_file=parsed_args.file,
                source_content=parsed_args.content,
                source_title=parsed_args.title,
                source_author=parsed_args.author,
                protagonist_name=parsed_args.protagonist,
                genre=parsed_args.genre,
                total_chapters=parsed_args.chapters
            )
            
            if result.success:
                print()
                print("=" * 70)
                print("仿写完成！")
                print("=" * 70)
                print()
                
                output_file = output_dir / f"{result.metadata.get('title', '仿写小说')}.txt"
                self.controller.save_result(result, str(output_file))
                
                print(f"输出文件: {output_file.absolute()}")
                print()
                print("字数统计:")
                print(result.word_count_report)
                print()
                print("元数据:")
                for key, value in result.metadata.items():
                    print(f"  {key}: {value}")
                
                return 0
            else:
                print()
                print("=" * 70)
                print(f"仿写失败: {result.error_message}")
                print("=" * 70)
                return 1
                
        except KeyboardInterrupt:
            print("\n\n用户中断操作")
            return 130
        except Exception as e:
            logger.error(f"运行失败: {e}", exc_info=True)
            print()
            print("=" * 70)
            print(f"错误: {e}")
            print("=" * 70)
            return 1
    
    def interactive_mode(self):
        """交互模式"""
        print("=" * 70)
        print("小说仿写工具 - 交互模式")
        print("=" * 70)
        print()
        
        print("请输入源小说文件路径（或直接回车输入内容）：")
        file_path = input("> ").strip()
        
        content = None
        title = ""
        author = ""
        
        if not file_path:
            print("\n请输入小说内容（输入完成后输入 END 结束）：")
            lines = []
            while True:
                line = input()
                if line.strip() == 'END':
                    break
                lines.append(line)
            content = '\n'.join(lines)
            print("\n请输入小说标题：")
            title = input("> ").strip()
            print("\n请输入小说作者：")
            author = input("> ").strip()
        elif not os.path.exists(file_path):
            print(f"\n错误: 文件不存在: {file_path}")
            return 1
        
        print("\n请输入主角名字（默认：主角）：")
        protagonist = input("> ").strip() or "主角"
        
        print("\n请选择小说类型：")
        print("  1. 修仙 (xianxia)")
        print("  2. 武侠 (wuxia)")
        print("  3. 都市 (urban)")
        print("  4. 玄幻 (xuanhuan)")
        print("  5. 其他 (other)")
        genre_choice = input("> ").strip() or "1"
        
        genre_map = {
            '1': 'xianxia',
            '2': 'wuxia',
            '3': 'urban',
            '4': 'xuanhuan',
            '5': 'other'
        }
        genre = genre_map.get(genre_choice, 'xianxia')
        
        print("\n请输入要仿写的章节数（默认：10）：")
        try:
            chapters = int(input("> ").strip() or "10")
        except ValueError:
            chapters = 10
        
        print("\n请输入输出目录（默认：./output）：")
        output_dir = input("> ").strip() or "./output"
        
        return self.run([
            '--file', file_path if file_path else '',
            '--content', content or '',
            '--title', title,
            '--author', author,
            '--protagonist', protagonist,
            '--genre', genre,
            '--chapters', str(chapters),
            '--output', output_dir
        ])


def main():
    """主入口"""
    cli = CommandLineInterface()
    
    if len(sys.argv) == 1:
        cli.interactive_mode()
    else:
        sys.exit(cli.run())


if __name__ == "__main__":
    main()
