"""
项目总指挥 (The Project Manager)
负责指挥各个部门按顺序工作，协调整个ETH HMA分析流程
"""
import logging
from pathlib import Path
from typing import List, Dict, Any
import time
from datetime import datetime

from ..collectors.data_collector import DataCollector
from ..analyzers.math_brain import MathBrain
from .librarian import Librarian
from ..utils.config import *

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('eth_hma_analysis.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class ProjectManager:
    """项目总指挥 - 协调各个部门完成ETH HMA分析任务"""
    
    def __init__(self):
        """初始化项目总指挥"""
        self.data_collector = DataCollector()
        self.math_brain = MathBrain(hma_period=HMA_PERIOD)
        self.librarian = Librarian(DATA_DIR)
        
        logger.info("项目总指挥初始化完成")
        logger.info(f"配置信息: 符号={SYMBOL}, 间隔={INTERVALS}, HMA周期={HMA_PERIOD}")
    
    def process_single_interval(self, symbol: str, interval: str, years_back: int = 3) -> Dict[str, Any]:
        """
        处理单个时间间隔的数据
        
        Args:
            symbol: 交易对符号
            interval: 时间间隔
            years_back: 获取多少年的历史数据
            
        Returns:
            处理结果字典
        """
        logger.info(f"开始处理 {symbol} {interval} 数据")
        start_time = time.time()
        
        result = {
            'symbol': symbol,
            'interval': interval,
            'years_back': years_back,
            'start_time': datetime.now().isoformat(),
            'success': False,
            'error': None,
            'files_created': [],
            'data_stats': {}
        }
        
        try:
            # 第一步：数据采集部工作
            logger.info("📥 命令数据采集部：获取原始数据")
            raw_data = self.data_collector.collect_historical_data(symbol, interval, years_back)
            
            if raw_data.empty:
                raise ValueError("数据采集部未获取到任何数据")
            
            result['data_stats']['raw_records'] = len(raw_data)
            result['data_stats']['date_range'] = {
                'start': raw_data.index.min().isoformat(),
                'end': raw_data.index.max().isoformat()
            }
            
            # 保存原始数据
            raw_file = self.librarian.save_raw_data(raw_data, symbol, interval)
            result['files_created'].append(str(raw_file))
            logger.info(f"✅ 原始数据已保存: {raw_file.name}")
            
            # 第二步：分析计算部工作
            logger.info("🧮 命令分析计算部：计算HMA指标")
            
            # 验证数据质量
            if not self.math_brain.validate_data(raw_data):
                raise ValueError("数据质量验证失败")
            
            # 计算HMA指标
            processed_data = self.math_brain.add_hma_to_dataframe(raw_data)
            
            # 计算额外指标（可选）
            processed_data = self.math_brain.calculate_additional_indicators(processed_data)
            
            result['data_stats']['processed_records'] = len(processed_data)
            result['data_stats']['hma_valid_count'] = processed_data[f'HMA_{HMA_PERIOD}'].notna().sum()
            
            # 第三步：档案管理部工作
            logger.info("📚 命令档案管理部：保存处理后的数据")
            processed_file = self.librarian.save_processed_data(
                processed_data, symbol, interval, HMA_PERIOD
            )
            result['files_created'].append(str(processed_file))
            logger.info(f"✅ 处理后数据已保存: {processed_file.name}")
            
            # 任务完成
            result['success'] = True
            result['end_time'] = datetime.now().isoformat()
            result['duration_seconds'] = time.time() - start_time
            
            logger.info(f"🎉 {symbol} {interval} 数据处理完成！耗时: {result['duration_seconds']:.2f}秒")
            
        except Exception as e:
            result['error'] = str(e)
            result['end_time'] = datetime.now().isoformat()
            result['duration_seconds'] = time.time() - start_time
            
            logger.error(f"❌ {symbol} {interval} 数据处理失败: {e}")
        
        return result
    
    def run_full_analysis(self) -> Dict[str, Any]:
        """
        运行完整的ETH HMA分析流程
        
        Returns:
            完整的分析结果
        """
        logger.info("🚀 开始执行ETH HMA完整分析流程")
        overall_start_time = time.time()
        
        analysis_result = {
            'project_name': 'ETH HMA Analysis',
            'start_time': datetime.now().isoformat(),
            'config': {
                'symbol': SYMBOL,
                'intervals': INTERVALS,
                'hma_period': HMA_PERIOD,
                'years_back': YEARS_BACK
            },
            'results': [],
            'summary': {},
            'success': False
        }
        
        try:
            # 处理每个时间间隔
            for interval in INTERVALS:
                logger.info(f"📋 开始处理时间间隔: {interval}")
                
                result = self.process_single_interval(SYMBOL, interval, YEARS_BACK)
                analysis_result['results'].append(result)
                
                if not result['success']:
                    logger.error(f"❌ {interval} 处理失败，继续处理下一个间隔")
                    continue
                
                # 间隔处理之间的短暂休息
                time.sleep(1)
            
            # 生成总结报告
            analysis_result = self._generate_summary(analysis_result)
            
            # 任务完成
            analysis_result['end_time'] = datetime.now().isoformat()
            analysis_result['total_duration_seconds'] = time.time() - overall_start_time
            analysis_result['success'] = True
            
            logger.info("🎊 ETH HMA完整分析流程执行完毕！")
            self._print_summary(analysis_result)
            
        except Exception as e:
            analysis_result['error'] = str(e)
            analysis_result['end_time'] = datetime.now().isoformat()
            analysis_result['total_duration_seconds'] = time.time() - overall_start_time
            
            logger.error(f"💥 完整分析流程执行失败: {e}")
        
        return analysis_result
    
    def _generate_summary(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """生成分析总结"""
        results = analysis_result['results']
        
        # 统计成功和失败的任务
        successful_tasks = [r for r in results if r['success']]
        failed_tasks = [r for r in results if not r['success']]
        
        # 统计总数据量
        total_raw_records = sum(r['data_stats'].get('raw_records', 0) for r in successful_tasks)
        total_processed_records = sum(r['data_stats'].get('processed_records', 0) for r in successful_tasks)
        
        # 统计文件
        all_files = []
        for r in successful_tasks:
            all_files.extend(r['files_created'])
        
        analysis_result['summary'] = {
            'total_tasks': len(results),
            'successful_tasks': len(successful_tasks),
            'failed_tasks': len(failed_tasks),
            'total_raw_records': total_raw_records,
            'total_processed_records': total_processed_records,
            'files_created': len(all_files),
            'file_list': all_files,
            'success_rate': len(successful_tasks) / len(results) * 100 if results else 0
        }
        
        return analysis_result
    
    def _print_summary(self, analysis_result: Dict[str, Any]):
        """打印分析总结"""
        summary = analysis_result['summary']
        
        print("\n" + "="*60)
        print("📊 ETH HMA 分析结果总结")
        print("="*60)
        print(f"⏱️  总耗时: {analysis_result['total_duration_seconds']:.2f} 秒")
        print(f"📈 处理任务: {summary['successful_tasks']}/{summary['total_tasks']} 成功")
        print(f"📊 原始数据记录: {summary['total_raw_records']:,} 条")
        print(f"🔢 处理后记录: {summary['total_processed_records']:,} 条")
        print(f"📁 生成文件: {summary['files_created']} 个")
        print(f"✅ 成功率: {summary['success_rate']:.1f}%")
        
        if summary['file_list']:
            print("\n📂 生成的文件:")
            for file_path in summary['file_list']:
                print(f"   • {Path(file_path).name}")
        
        print("="*60)
    
    def get_data_overview(self) -> Dict[str, Any]:
        """获取数据概览"""
        files = self.librarian.list_files()
        overview = {
            'total_files': len(files),
            'files': []
        }
        
        for file_path in files:
            file_info = self.librarian.get_file_info(file_path)
            overview['files'].append({
                'filename': file_path.name,
                'info': file_info
            })
        
        return overview


if __name__ == "__main__":
    # 运行ETH HMA分析
    manager = ProjectManager()
    
    # 可以选择运行单个间隔或完整分析
    print("选择运行模式:")
    print("1. 完整分析 (1h + 4h)")
    print("2. 仅1小时数据")
    print("3. 仅4小时数据")
    
    choice = input("请输入选择 (1-3): ").strip()
    
    if choice == "1":
        result = manager.run_full_analysis()
    elif choice == "2":
        result = manager.process_single_interval("ETHUSDT", "1h", 3)
    elif choice == "3":
        result = manager.process_single_interval("ETHUSDT", "4h", 3)
    else:
        print("无效选择，运行完整分析")
        result = manager.run_full_analysis()
    
    # 显示数据概览
    print("\n📋 数据概览:")
    overview = manager.get_data_overview()
    for file_info in overview['files']:
        print(f"文件: {file_info['filename']}")
        print(f"  大小: {file_info['info'].get('file_size_mb', 0):.2f} MB")
        print(f"  记录数: {file_info['info'].get('rows', 0):,}")
        print(f"  类型: {file_info['info'].get('data_type', 'unknown')}")
        print()
