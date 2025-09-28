#!/usr/bin/env python3
"""
ETH HMA 分析器主程序
这是整个项目的入口点，提供简单的命令行界面
"""
import sys
import argparse
from pathlib import Path
import logging

# Ensure project root is on PYTHONPATH so we can import the src package
PROJECT_ROOT = Path(__file__).parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.managers.project_manager import ProjectManager
from src.utils.config import *

def setup_logging(verbose: bool = False):
    """设置日志配置"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('assets/logs/eth_hma_analysis.log'),
            logging.StreamHandler()
        ]
    )

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='ETH HMA 分析器 - 自动下载ETH历史数据并计算HMA指标',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python scripts/main.py                    # 运行完整分析
  python scripts/main.py --interval 1h     # 仅分析1小时数据
  python scripts/main.py --interval 4h     # 仅分析4小时数据
  python scripts/main.py --years 2         # 获取过去2年数据
  python scripts/main.py --hma-period 30   # 使用30周期HMA
  python scripts/main.py --verbose         # 显示详细日志
        """
    )
    
    parser.add_argument(
        '--interval', 
        choices=['1h', '4h', 'both'],
        default='both',
        help='要分析的时间间隔 (默认: both)'
    )
    
    parser.add_argument(
        '--years',
        type=int,
        default=YEARS_BACK,
        help=f'获取多少年的历史数据 (默认: {YEARS_BACK})'
    )
    
    parser.add_argument(
        '--hma-period',
        type=int,
        default=HMA_PERIOD,
        help=f'HMA周期参数 (默认: {HMA_PERIOD})'
    )
    
    parser.add_argument(
        '--symbol',
        default=SYMBOL,
        help=f'交易对符号 (默认: {SYMBOL})'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='显示详细日志'
    )
    
    parser.add_argument(
        '--overview',
        action='store_true',
        help='仅显示数据概览，不运行分析'
    )
    
    args = parser.parse_args()
    
    # 设置日志
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)
    
    # 显示启动信息
    print("🚀 ETH HMA 分析器启动")
    print("=" * 50)
    print(f"📊 交易对: {args.symbol}")
    print(f"⏰ 时间间隔: {args.interval}")
    print(f"📅 历史数据: {args.years} 年")
    print(f"🔢 HMA周期: {args.hma_period}")
    print("=" * 50)
    
    try:
        # 创建项目管理器
        manager = ProjectManager()
        
        # 如果只是查看概览
        if args.overview:
            print("\n📋 数据概览:")
            overview = manager.get_data_overview()
            if overview['total_files'] == 0:
                print("   📁 暂无数据文件")
            else:
                for file_info in overview['files']:
                    info = file_info['info']
                    print(f"   📄 {file_info['filename']}")
                    print(f"      💾 大小: {info.get('file_size_mb', 0):.2f} MB")
                    print(f"      📊 记录: {info.get('rows', 0):,} 条")
                    print(f"      🏷️  类型: {info.get('data_type', 'unknown')}")
                    print(f"      ⏰ 创建: {info.get('created_at', 'unknown')}")
                    print()
            return
        
        # 运行分析
        if args.interval == 'both':
            # 运行完整分析
            result = manager.run_full_analysis()
        else:
            # 运行单个间隔分析
            result = manager.process_single_interval(
                args.symbol, 
                args.interval, 
                args.years
            )
        
        # 检查结果
        if result.get('success', False):
            print("\n✅ 分析完成！")
        else:
            print(f"\n❌ 分析失败: {result.get('error', '未知错误')}")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⏹️  用户中断操作")
        sys.exit(0)
    except Exception as e:
        logger.error(f"程序执行出错: {e}")
        print(f"\n💥 程序执行出错: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()