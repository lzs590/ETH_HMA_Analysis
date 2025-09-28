"""
Jupyter工具模块
为Jupyter Notebook环境提供便捷的数据处理和工具函数
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 12

class JupyterDataLoader:
    """Jupyter数据加载器"""
    
    def __init__(self, data_dir="src/utils/data"):
        """
        初始化数据加载器
        
        Args:
            data_dir: 数据目录路径
        """
        self.data_dir = Path(data_dir)
        
    def load_4h_data(self, filename=None):
        """
        加载4h级别数据
        
        Args:
            filename: 指定文件名，如果为None则自动查找最新的4h数据
            
        Returns:
            pd.DataFrame: 4h数据
        """
        if filename:
            data_file = self.data_dir / filename
        else:
            # 自动查找最新的4h数据
            data_files = list(self.data_dir.glob("*4h*processed*.parquet"))
            if not data_files:
                raise FileNotFoundError("未找到4h数据文件")
            data_file = max(data_files, key=lambda x: x.stat().st_mtime)
            
        if not data_file.exists():
            raise FileNotFoundError(f"数据文件不存在: {data_file}")
            
        df = pd.read_parquet(data_file)
        df = df.sort_index()  # 确保按时间排序
        
        print(f"✅ 4h数据加载成功: {len(df)} 条记录")
        print(f"📅 时间范围: {df.index[0]} 到 {df.index[-1]}")
        print(f"📈 价格范围: ${df['close'].min():.2f} - ${df['close'].max():.2f}")
        
        return df
    
    def load_1h_data(self, filename=None):
        """
        加载1h级别数据
        
        Args:
            filename: 指定文件名，如果为None则自动查找最新的1h数据
            
        Returns:
            pd.DataFrame: 1h数据
        """
        if filename:
            data_file = self.data_dir / filename
        else:
            # 自动查找最新的1h数据
            data_files = list(self.data_dir.glob("*1h*processed*.parquet"))
            if not data_files:
                raise FileNotFoundError("未找到1h数据文件")
            data_file = max(data_files, key=lambda x: x.stat().st_mtime)
            
        if not data_file.exists():
            raise FileNotFoundError(f"数据文件不存在: {data_file}")
            
        df = pd.read_parquet(data_file)
        df = df.sort_index()  # 确保按时间排序
        
        print(f"✅ 1h数据加载成功: {len(df)} 条记录")
        print(f"📅 时间范围: {df.index[0]} 到 {df.index[-1]}")
        print(f"📈 价格范围: ${df['close'].min():.2f} - ${df['close'].max():.2f}")
        
        return df
    
    def get_data_info(self, df):
        """
        获取数据基本信息
        
        Args:
            df: 数据DataFrame
            
        Returns:
            dict: 数据信息
        """
        info = {
            'shape': df.shape,
            'columns': list(df.columns),
            'dtypes': df.dtypes.to_dict(),
            'missing_values': df.isnull().sum().to_dict(),
            'time_range': (df.index[0], df.index[-1]),
            'price_range': (df['close'].min(), df['close'].max())
        }
        
        return info
    
    def display_data_summary(self, df):
        """
        显示数据摘要
        
        Args:
            df: 数据DataFrame
        """
        print("📊 数据摘要")
        print("=" * 50)
        print(f"数据形状: {df.shape}")
        print(f"时间范围: {df.index[0]} 到 {df.index[-1]}")
        print(f"价格范围: ${df['close'].min():.2f} - ${df['close'].max():.2f}")
        
        # 检查HMA指标
        hma_cols = [col for col in df.columns if 'HMA' in col]
        if hma_cols:
            print(f"HMA指标: {hma_cols}")
        else:
            print("❌ 未找到HMA指标")
            
        # 检查缺失值
        missing_data = df.isnull().sum()
        if missing_data.sum() > 0:
            print(f"缺失值: {missing_data[missing_data > 0].to_dict()}")
        else:
            print("✅ 无缺失值")
            
        print("=" * 50)

class JupyterAnalyzer:
    """Jupyter分析器"""
    
    def __init__(self):
        """初始化分析器"""
        pass
    
    def quick_price_analysis(self, df, title="价格分析"):
        """
        快速价格分析
        
        Args:
            df: 价格数据
            title: 图表标题
        """
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # 1. 价格走势
        axes[0, 0].plot(df.index, df['close'], color='blue', linewidth=1)
        axes[0, 0].set_title('价格走势')
        axes[0, 0].set_ylabel('价格 (USDT)')
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. 价格分布
        axes[0, 1].hist(df['close'], bins=50, color='green', alpha=0.7)
        axes[0, 1].set_title('价格分布')
        axes[0, 1].set_xlabel('价格 (USDT)')
        axes[0, 1].set_ylabel('频率')
        axes[0, 1].grid(True, alpha=0.3)
        
        # 3. 成交量分析
        if 'volume' in df.columns:
            axes[1, 0].plot(df.index, df['volume'], color='orange', linewidth=1)
            axes[1, 0].set_title('成交量走势')
            axes[1, 0].set_ylabel('成交量')
            axes[1, 0].grid(True, alpha=0.3)
        
        # 4. 价格变化率
        price_change = df['close'].pct_change() * 100
        axes[1, 1].hist(price_change.dropna(), bins=50, color='red', alpha=0.7)
        axes[1, 1].set_title('价格变化率分布')
        axes[1, 1].set_xlabel('变化率 (%)')
        axes[1, 1].set_ylabel('频率')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.suptitle(title, fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.show()
        
        return fig, axes
    
    def hma_analysis(self, df, hma_col='HMA_45', title="HMA分析"):
        """
        HMA指标分析
        
        Args:
            df: 数据
            hma_col: HMA列名
            title: 图表标题
        """
        if hma_col not in df.columns:
            print(f"❌ 未找到HMA列: {hma_col}")
            return None, None
            
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # 1. 价格和HMA对比
        axes[0, 0].plot(df.index, df['close'], label='价格', color='blue', alpha=0.7)
        axes[0, 0].plot(df.index, df[hma_col], label=hma_col, color='red', linewidth=2)
        axes[0, 0].set_title('价格与HMA对比')
        axes[0, 0].set_ylabel('价格 (USDT)')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. HMA斜率分析
        hma_slope = df[hma_col].diff()
        axes[0, 1].plot(df.index, hma_slope, color='green', linewidth=1)
        axes[0, 1].axhline(y=0, color='red', linestyle='--', alpha=0.7)
        axes[0, 1].set_title('HMA斜率变化')
        axes[0, 1].set_ylabel('斜率')
        axes[0, 1].grid(True, alpha=0.3)
        
        # 3. HMA分布
        axes[1, 0].hist(df[hma_col].dropna(), bins=50, color='purple', alpha=0.7)
        axes[1, 0].set_title('HMA值分布')
        axes[1, 0].set_xlabel('HMA值')
        axes[1, 0].set_ylabel('频率')
        axes[1, 0].grid(True, alpha=0.3)
        
        # 4. 价格与HMA相关性
        axes[1, 1].scatter(df[hma_col], df['close'], alpha=0.5, color='orange')
        axes[1, 1].set_title('价格与HMA相关性')
        axes[1, 1].set_xlabel('HMA值')
        axes[1, 1].set_ylabel('价格 (USDT)')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.suptitle(title, fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.show()
        
        return fig, axes
    
    def trend_summary(self, intervals, events):
        """
        趋势分析摘要
        
        Args:
            intervals: 趋势区间列表
            events: 事件列表
        """
        print("📊 趋势分析摘要")
        print("=" * 50)
        
        if intervals:
            up_trends = [i for i in intervals if i['direction'] == 'up']
            down_trends = [i for i in intervals if i['direction'] == 'down']
            
            print(f"总趋势数: {len(intervals)}")
            print(f"上涨趋势: {len(up_trends)}")
            print(f"下跌趋势: {len(down_trends)}")
            
            if up_trends:
                avg_up_duration = np.mean([i['duration'] for i in up_trends])
                avg_up_pfe = np.mean([i['pfe_pct'] for i in up_trends])
                print(f"平均上涨持续时间: {avg_up_duration:.1f}周期")
                print(f"平均上涨PFE: {avg_up_pfe:.2f}%")
            
            if down_trends:
                avg_down_duration = np.mean([i['duration'] for i in down_trends])
                avg_down_pfe = np.mean([i['pfe_pct'] for i in down_trends])
                print(f"平均下跌持续时间: {avg_down_duration:.1f}周期")
                print(f"平均下跌PFE: {avg_down_pfe:.2f}%")
        else:
            print("❌ 无趋势数据")
            
        if events:
            print(f"\n事件总数: {len(events)}")
            event_types = {}
            for event in events:
                event_type = event['event_type']
                event_types[event_type] = event_types.get(event_type, 0) + 1
            print("事件类型分布:")
            for event_type, count in event_types.items():
                print(f"  {event_type}: {count}")
        else:
            print("❌ 无事件数据")
            
        print("=" * 50)

class JupyterConfig:
    """Jupyter配置类"""
    
    @staticmethod
    def setup_matplotlib():
        """设置matplotlib中文字体"""
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
        plt.rcParams['axes.unicode_minus'] = False
        plt.rcParams['font.size'] = 12
        
    @staticmethod
    def setup_pandas():
        """设置pandas显示选项"""
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', None)
        
    @staticmethod
    def setup_seaborn():
        """设置seaborn样式"""
        sns.set_style("whitegrid")
        sns.set_palette("husl")
        
    @staticmethod
    def setup_all():
        """设置所有配置"""
        JupyterConfig.setup_matplotlib()
        JupyterConfig.setup_pandas()
        JupyterConfig.setup_seaborn()
        print("✅ Jupyter环境配置完成")

# 便捷函数
def quick_setup():
    """快速设置Jupyter环境"""
    JupyterConfig.setup_all()
    
def load_4h_data(filename=None):
    """快速加载4h数据"""
    loader = JupyterDataLoader()
    return loader.load_4h_data(filename)

def load_1h_data(filename=None):
    """快速加载1h数据"""
    loader = JupyterDataLoader()
    return loader.load_1h_data(filename)

def quick_analysis(df, hma_col='HMA_45'):
    """快速分析"""
    analyzer = JupyterAnalyzer()
    fig1, _ = analyzer.quick_price_analysis(df)
    fig2, _ = analyzer.hma_analysis(df, hma_col)
    return fig1, fig2
