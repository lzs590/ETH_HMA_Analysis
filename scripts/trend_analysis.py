#!/usr/bin/env python3
"""
趋势分析主脚本

基于HMA斜率变化的完整趋势分析系统：
1. 识别HMA拐点
2. 分析事件行为
3. 计算趋势区间捕获的最大涨幅/跌幅
4. 生成详细报告和可视化
"""

import sys
import argparse
import logging
import json
from pathlib import Path
from datetime import datetime

# 添加src到Python路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pandas as pd
import numpy as np
# 直接导入核心模块
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src', 'eth_hma_analysis', 'core'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from trend_analyzer import TrendAnalyzer
from analyzers.trend_visualizer import TrendVisualizer
from visualizers.strategy_visualizer import StrategyVisualizer
from reporters.strategy_reporter import StrategyReporter
from utils.config import *

def setup_logging(verbose: bool = False):
    """设置日志"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('assets/logs/trend_analysis.log'),
            logging.StreamHandler()
        ]
    )

def load_data(data_dir: str = "assets/data") -> dict:
    """加载数据"""
    data_dir = Path(data_dir)
    data = {}
    
    # 查找最新的处理文件
    processed_files = list(data_dir.glob("ETHUSDT_*_processed_*.parquet"))
    
    for file_path in processed_files:
        if '1h' in file_path.name:
            df = pd.read_parquet(file_path)
            df.set_index('open_time', inplace=True)
            data['1h'] = df
            print(f"✅ 加载1小时数据: {len(df):,} 条记录")
        elif '4h' in file_path.name:
            df = pd.read_parquet(file_path)
            df.set_index('open_time', inplace=True)
            data['4h'] = df
            print(f"✅ 加载4小时数据: {len(df):,} 条记录")
    
    if not data:
        raise FileNotFoundError("没有找到可分析的数据文件")
    
    return data

def run_trend_analysis(data: dict, hma_period: int = 45, slope_threshold: float = 0.001) -> dict:
    """运行趋势分析"""
    logger = logging.getLogger(__name__)
    results = {}
    
    for interval, df in data.items():
        logger.info(f"开始分析 {interval} 数据")
        
        # 初始化分析器
        analyzer = TrendAnalyzer(hma_period=hma_period, slope_threshold=slope_threshold)
        
        # 运行完整趋势分析（包括改进算法和下跌趋势专项分析）
        complete_report = analyzer.run_complete_analysis(df.copy())
        
        # 提取基础数据用于可视化
        df_with_slope = analyzer.calculate_hma_slope(df.copy())
        events = analyzer.analyze_events(df_with_slope)
        intervals = analyzer.analyze_trend_intervals(df_with_slope)
        
        # 使用完整报告
        report = complete_report
        
        results[interval] = {
            'data': df_with_slope,
            'events': events,
            'intervals': intervals,
            'report': report
        }
        
        logger.info(f"{interval} 数据分析完成")
    
    return results

def save_results(results: dict, output_dir: str = "assets/reports"):
    """保存分析结果"""
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 保存报告为JSON
    for interval, result in results.items():
        report_file = output_dir / f"trend_analysis_{interval}_{timestamp}.json"
        
        # 转换numpy类型为Python原生类型
        def convert_numpy(obj):
            if isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            return obj
        
        # 递归转换
        def recursive_convert(d):
            if isinstance(d, dict):
                return {k: recursive_convert(v) for k, v in d.items()}
            elif isinstance(d, list):
                return [recursive_convert(item) for item in d]
            else:
                return convert_numpy(d)
        
        report_data = recursive_convert(result['report'])
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        print(f"📊 {interval} 分析报告已保存: {report_file}")

def generate_visualizations(results: dict, output_dir: str = "assets/charts", use_chinese: bool = True):
    """生成可视化图表"""
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    visualizer = TrendVisualizer(use_chinese=use_chinese)
    strategy_visualizer = StrategyVisualizer(str(output_dir))
    
    for interval, result in results.items():
        print(f"🎨 生成 {interval} 可视化图表...")
        
        # 1. 拐点识别图
        turning_points_path = output_dir / f"turning_points_{interval}_{timestamp}.png"
        visualizer.plot_turning_points(
            result['data'], 
            save_path=str(turning_points_path)
        )
        
        # 2. 趋势区间分析图
        intervals_path = output_dir / f"trend_intervals_{interval}_{timestamp}.png"
        visualizer.plot_trend_intervals(
            result['data'], 
            result['intervals'], 
            save_path=str(intervals_path)
        )
        
        # 3. 事件分析图
        events_path = output_dir / f"event_analysis_{interval}_{timestamp}.png"
        visualizer.plot_event_analysis(
            result['events'], 
            save_path=str(events_path)
        )
        
        # 4. 综合分析图
        comprehensive_path = output_dir / f"comprehensive_analysis_{interval}_{timestamp}.png"
        visualizer.plot_comprehensive_analysis(
            result['data'], 
            result['intervals'], 
            result['events'], 
            save_path=str(comprehensive_path)
        )
        
        # 5. 策略总览图
        strategy_overview_path = strategy_visualizer.create_strategy_overview(
            result['data'],
            result['intervals'],
            result['report'].get('uptrend_analysis', {}),
            result['report'].get('downtrend_analysis', {}),
            interval
        )
        
        # 6. 策略表现分析图
        strategy_performance_path = strategy_visualizer.create_strategy_performance(
            result['report'].get('uptrend_analysis', {}),
            result['report'].get('downtrend_analysis', {}),
            interval
        )
        
        # 7. 风险分析图
        risk_analysis_path = strategy_visualizer.create_risk_analysis(
            result['report'].get('uptrend_analysis', {}),
            result['report'].get('downtrend_analysis', {}),
            interval
        )

def print_summary(results: dict):
    """打印分析摘要"""
    print("\n" + "="*80)
    print("🎯 ETH HMA趋势分析摘要")
    print("="*80)
    
    for interval, result in results.items():
        report = result['report']
        intervals = result['intervals']
        events = result['events']
        
        print(f"\n📈 {interval.upper()} 数据分析结果:")
        print("-" * 50)
        
        # 基本统计
        summary = report['summary']
        print(f"📊 总趋势区间: {summary['total_intervals']}")
        print(f"   ├─ 上升趋势: {summary['up_intervals']}")
        print(f"   └─ 下降趋势: {summary['down_intervals']}")
        print(f"🎯 总拐点事件: {summary['total_events']}")
        print(f"   ├─ 上升拐点: {summary['up_events']}")
        print(f"   └─ 下降拐点: {summary['down_events']}")
        
        # 趋势区间分析
        up_analysis = report['interval_analysis']['up_trends']
        down_analysis = report['interval_analysis']['down_trends']
        
        print(f"\n📈 上升趋势区间分析:")
        print(f"   ├─ 平均持续时间: {up_analysis['avg_duration']:.1f} 周期")
        print(f"   ├─ 平均价格变化: {up_analysis['avg_price_change_pct']:.2f}%")
        print(f"   ├─ 最大价格变化: {up_analysis['max_price_change_pct']:.2f}%")
        print(f"   ├─ 平均PFE: {up_analysis['avg_pfe_pct']:.2f}%")
        print(f"   ├─ 最大PFE: {up_analysis['max_pfe_pct']:.2f}%")
        print(f"   └─ 胜率: {up_analysis['win_rate']:.1%}")
        
        print(f"\n📉 下降趋势区间分析:")
        print(f"   ├─ 平均持续时间: {down_analysis['avg_duration']:.1f} 周期")
        print(f"   ├─ 平均价格变化: {down_analysis['avg_price_change_pct']:.2f}%")
        print(f"   ├─ 最大价格变化: {down_analysis['max_price_change_pct']:.2f}%")
        print(f"   ├─ 平均PFE: {down_analysis['avg_pfe_pct']:.2f}%")
        print(f"   ├─ 最大PFE: {down_analysis['max_pfe_pct']:.2f}%")
        print(f"   └─ 胜率: {down_analysis['win_rate']:.1%}")
        
        # 事件分析
        up_events = report['event_analysis']['up_turns']
        down_events = report['event_analysis']['down_turns']
        
        print(f"\n🎯 事件分析:")
        print(f"   上升拐点:")
        print(f"   ├─ 平均波动率: {up_events['avg_volatility']:.3f}")
        print(f"   ├─ 平均一致性: {up_events['avg_consistency']:.1%}")
        print(f"   ├─ 1小时后平均变化: {up_events['avg_price_change_1h']:.2f}%")
        print(f"   └─ 5小时后平均变化: {up_events['avg_price_change_5h']:.2f}%")
        
        print(f"   下降拐点:")
        print(f"   ├─ 平均波动率: {down_events['avg_volatility']:.3f}")
        print(f"   ├─ 平均一致性: {down_events['avg_consistency']:.1%}")
        print(f"   ├─ 1小时后平均变化: {down_events['avg_price_change_1h']:.2f}%")
        print(f"   └─ 5小时后平均变化: {down_events['avg_price_change_5h']:.2f}%")
        
        # 盈亏比
        if 'profit_loss_ratio' in report['interval_analysis']:
            pl_ratio = report['interval_analysis']['profit_loss_ratio']
            print(f"\n💰 盈亏比: {pl_ratio:.2f}")
        
        # 上涨趋势专项分析（做多策略）
        if 'uptrend_analysis' in report and report['uptrend_analysis']['total_uptrends'] > 0:
            uptrend = report['uptrend_analysis']
            print(f"\n📈 上涨趋势专项分析（做多策略）:")
            print(f"   ├─ 总上涨趋势数: {uptrend['total_uptrends']}")
            print(f"   ├─ 平均做多理想收益: {uptrend['avg_long_ideal_profit']:.2f}%")
            print(f"   ├─ 最大做多理想收益: {uptrend['max_long_ideal_profit']:.2f}%")
            print(f"   ├─ 平均做多实际收益: {uptrend['avg_long_actual_profit']:.2f}%")
            print(f"   ├─ 最大做多实际收益: {uptrend['max_long_actual_profit']:.2f}%")
            print(f"   ├─ 平均做多风险损失: {uptrend['avg_long_risk_loss']:.2f}%")
            print(f"   ├─ 最大做多风险损失: {uptrend['max_long_risk_loss']:.2f}%")
            print(f"   └─ 平均风险收益比: {uptrend['avg_risk_reward_ratio']:.2f}")
        
        # 下跌趋势专项分析（做空策略）
        if 'downtrend_analysis' in report and report['downtrend_analysis']['total_downtrends'] > 0:
            downtrend = report['downtrend_analysis']
            print(f"\n📉 下跌趋势专项分析（做空策略）:")
            print(f"   ├─ 总下跌趋势数: {downtrend['total_downtrends']}")
            print(f"   ├─ 平均做空理想收益: {downtrend['avg_short_ideal_profit']:.2f}%")
            print(f"   ├─ 最大做空理想收益: {downtrend['max_short_ideal_profit']:.2f}%")
            print(f"   ├─ 平均做空实际收益: {downtrend['avg_short_actual_profit']:.2f}%")
            print(f"   ├─ 最大做空实际收益: {downtrend['max_short_actual_profit']:.2f}%")
            print(f"   ├─ 平均做空风险损失: {downtrend['avg_short_risk_loss']:.2f}%")
            print(f"   ├─ 最大做空风险损失: {downtrend['max_short_risk_loss']:.2f}%")
            print(f"   └─ 平均风险收益比: {downtrend['avg_risk_reward_ratio']:.2f}")
        
        print("-" * 50)

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='ETH HMA趋势分析工具')
    parser.add_argument('--data-dir', default='assets/data', help='数据目录')
    parser.add_argument('--output-dir', default='assets/reports', help='输出目录')
    parser.add_argument('--charts-dir', default='assets/charts', help='图表目录')
    parser.add_argument('--hma-period', type=int, default=45, help='HMA周期')
    parser.add_argument('--slope-threshold', type=float, default=0.001, help='斜率阈值')
    parser.add_argument('--no-viz', action='store_true', help='跳过可视化')
    parser.add_argument('--english', action='store_true', help='使用英文标签')
    parser.add_argument('--verbose', '-v', action='store_true', help='详细输出')
    
    args = parser.parse_args()
    
    # 设置日志
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)
    
    try:
        print("🚀 开始ETH HMA趋势分析...")
        
        # 1. 加载数据
        print("\n📁 加载数据...")
        data = load_data(args.data_dir)
        
        # 2. 运行分析
        print("\n🔍 运行趋势分析...")
        results = run_trend_analysis(
            data, 
            hma_period=args.hma_period, 
            slope_threshold=args.slope_threshold
        )
        
        # 3. 保存结果
        print("\n💾 保存分析结果...")
        save_results(results, args.output_dir)
        
        # 4. 生成可视化
        if not args.no_viz:
            print("\n🎨 生成可视化图表...")
            generate_visualizations(results, args.charts_dir, use_chinese=not args.english)
        
        # 5. 生成Markdown报告
        print("\n📝 生成策略分析报告...")
        reporter = StrategyReporter(args.output_dir)
        report_file = reporter.generate_strategy_report(results)
        print(f"📄 策略报告已生成: {report_file}")
        
        # 6. 打印摘要
        print_summary(results)
        
        print("\n✅ 趋势分析完成！")
        print(f"📊 报告保存在: {args.output_dir}")
        if not args.no_viz:
            print(f"🎨 图表保存在: {args.charts_dir}")
        
    except Exception as e:
        logger.error(f"分析过程中出现错误: {e}")
        print(f"❌ 错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
