#!/usr/bin/env python3
"""
HMA可视化分析脚本
生成各种图表来分析HMA指标的表现
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def load_data():
    """加载数据"""
    data_dir = Path('data')
    processed_files = list(data_dir.glob("ETHUSDT_*_processed_*.parquet"))
    
    data = {}
    for file_path in processed_files:
        if '1h' in file_path.name:
            df = pd.read_parquet(file_path)
            df.set_index('open_time', inplace=True)
            data['1h'] = df
        elif '4h' in file_path.name:
            df = pd.read_parquet(file_path)
            df.set_index('open_time', inplace=True)
            data['4h'] = df
    
    return data

def plot_price_and_hma(data):
    """绘制价格与HMA对比图"""
    fig, axes = plt.subplots(2, 1, figsize=(15, 12))
    fig.suptitle('ETH 价格与HMA对比分析', fontsize=16, fontweight='bold')
    
    for i, (interval, df) in enumerate(data.items()):
        ax = axes[i]
        
        # 绘制价格和HMA
        ax.plot(df.index, df['close'], label='ETH价格', linewidth=0.8, alpha=0.8, color='blue')
        ax.plot(df.index, df['HMA_45'], label='HMA_45', linewidth=1.2, alpha=0.9, color='red')
        
        # 填充价格与HMA之间的区域
        ax.fill_between(df.index, df['close'], df['HMA_45'], 
                       where=(df['close'] >= df['HMA_45']), 
                       color='green', alpha=0.3, label='价格>HMA')
        ax.fill_between(df.index, df['close'], df['HMA_45'], 
                       where=(df['close'] < df['HMA_45']), 
                       color='red', alpha=0.3, label='价格<HMA')
        
        ax.set_title(f'{interval} 数据 - 价格与HMA对比')
        ax.set_ylabel('价格 (USDT)')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('hma_price_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_hma_deviation(data):
    """绘制HMA偏离度分析"""
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('HMA偏离度分析', fontsize=16, fontweight='bold')
    
    for i, (interval, df) in enumerate(data.items()):
        # 偏离度时间序列
        ax1 = axes[i, 0]
        deviation = df['hma_deviation'].dropna()
        ax1.plot(deviation.index, deviation, linewidth=0.8, alpha=0.8, color='purple')
        ax1.axhline(y=0, color='black', linestyle='--', alpha=0.5)
        ax1.axhline(y=5, color='red', linestyle='--', alpha=0.5, label='+5%')
        ax1.axhline(y=-5, color='red', linestyle='--', alpha=0.5, label='-5%')
        ax1.set_title(f'{interval} - HMA偏离度时间序列')
        ax1.set_ylabel('偏离度 (%)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 偏离度分布直方图
        ax2 = axes[i, 1]
        ax2.hist(deviation, bins=50, alpha=0.7, color='skyblue', edgecolor='black')
        ax2.axvline(x=0, color='red', linestyle='--', alpha=0.7)
        ax2.axvline(x=deviation.mean(), color='green', linestyle='-', alpha=0.7, 
                   label=f'平均值: {deviation.mean():.3f}%')
        ax2.set_title(f'{interval} - 偏离度分布')
        ax2.set_xlabel('偏离度 (%)')
        ax2.set_ylabel('频次')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('hma_deviation_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_trading_signals(data):
    """绘制交易信号分析"""
    fig, axes = plt.subplots(2, 1, figsize=(15, 10))
    fig.suptitle('HMA交易信号分析', fontsize=16, fontweight='bold')
    
    for i, (interval, df) in enumerate(data.items()):
        ax = axes[i]
        
        # 创建交易信号
        df_signal = df.copy()
        df_signal['hma_signal'] = np.where(df_signal['close'] > df_signal['HMA_45'], 1, -1)
        df_signal['signal_change'] = df_signal['hma_signal'].diff()
        
        # 绘制价格和HMA
        ax.plot(df_signal.index, df_signal['close'], label='ETH价格', linewidth=0.8, alpha=0.8)
        ax.plot(df_signal.index, df_signal['HMA_45'], label='HMA_45', linewidth=1.2, alpha=0.9)
        
        # 标记买入信号
        buy_signals = df_signal[df_signal['signal_change'] == 2]
        ax.scatter(buy_signals.index, buy_signals['close'], 
                  color='green', alpha=0.7, s=20, label='买入信号', marker='^')
        
        # 标记卖出信号
        sell_signals = df_signal[df_signal['signal_change'] == -2]
        ax.scatter(sell_signals.index, sell_signals['close'], 
                  color='red', alpha=0.7, s=20, label='卖出信号', marker='v')
        
        ax.set_title(f'{interval} - HMA交易信号')
        ax.set_ylabel('价格 (USDT)')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('hma_trading_signals.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_volume_analysis(data):
    """绘制成交量分析"""
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('成交量与HMA关系分析', fontsize=16, fontweight='bold')
    
    for i, (interval, df) in enumerate(data.items()):
        # 成交量时间序列
        ax1 = axes[i, 0]
        ax1.plot(df.index, df['volume'], linewidth=0.8, alpha=0.8, color='orange')
        ax1.set_title(f'{interval} - 成交量走势')
        ax1.set_ylabel('成交量 (ETH)')
        ax1.grid(True, alpha=0.3)
        
        # 成交量与价格变化关系
        ax2 = axes[i, 1]
        price_changes = df['price_change'].dropna() * 100
        volumes = df['volume'].loc[price_changes.index]
        
        scatter = ax2.scatter(price_changes, volumes, alpha=0.5, s=10, c=price_changes, cmap='RdYlGn')
        ax2.set_title(f'{interval} - 成交量与价格变化关系')
        ax2.set_xlabel('价格变化 (%)')
        ax2.set_ylabel('成交量 (ETH)')
        ax2.grid(True, alpha=0.3)
        plt.colorbar(scatter, ax=ax2, label='价格变化 (%)')
    
    plt.tight_layout()
    plt.savefig('volume_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_correlation_analysis(data):
    """绘制相关性分析"""
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    fig.suptitle('HMA相关性分析', fontsize=16, fontweight='bold')
    
    for i, (interval, df) in enumerate(data.items()):
        ax = axes[i]
        
        # 选择相关列
        corr_cols = ['close', 'HMA_45', 'price_change', 'hma_deviation', 'volume']
        corr_data = df[corr_cols].corr()
        
        # 绘制热力图
        sns.heatmap(corr_data, annot=True, cmap='coolwarm', center=0, 
                   square=True, linewidths=0.5, ax=ax, cbar_kws={"shrink": 0.8})
        ax.set_title(f'{interval} - 变量相关性')
    
    plt.tight_layout()
    plt.savefig('correlation_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_hma_performance(data):
    """绘制HMA性能分析"""
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('HMA性能分析', fontsize=16, fontweight='bold')
    
    for i, (interval, df) in enumerate(data.items()):
        # HMA跟踪误差
        ax1 = axes[i, 0]
        hma = df['HMA_45'].dropna()
        price = df['close'].loc[hma.index]
        error = price - hma
        
        ax1.plot(price.index, error, linewidth=0.8, alpha=0.8, color='purple')
        ax1.axhline(y=0, color='black', linestyle='--', alpha=0.5)
        ax1.axhline(y=error.std(), color='red', linestyle='--', alpha=0.5, label=f'+1σ: {error.std():.2f}')
        ax1.axhline(y=-error.std(), color='red', linestyle='--', alpha=0.5, label=f'-1σ: {-error.std():.2f}')
        ax1.set_title(f'{interval} - HMA跟踪误差')
        ax1.set_ylabel('误差 (USDT)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 误差分布
        ax2 = axes[i, 1]
        ax2.hist(error, bins=50, alpha=0.7, color='lightblue', edgecolor='black')
        ax2.axvline(x=0, color='red', linestyle='--', alpha=0.7)
        ax2.axvline(x=error.mean(), color='green', linestyle='-', alpha=0.7, 
                   label=f'平均值: {error.mean():.2f}')
        ax2.set_title(f'{interval} - 跟踪误差分布')
        ax2.set_xlabel('误差 (USDT)')
        ax2.set_ylabel('频次')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('hma_performance.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_market_conditions(data):
    """绘制不同市场条件下的HMA表现"""
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('不同市场条件下的HMA表现', fontsize=16, fontweight='bold')
    
    for i, (interval, df) in enumerate(data.items()):
        # 上涨市场
        ax1 = axes[i, 0]
        up_market = df[df['price_change'] > 0.01]  # 涨幅>1%
        if len(up_market) > 0:
            up_deviation = up_market['hma_deviation'].dropna()
            ax1.hist(up_deviation, bins=30, alpha=0.7, color='green', edgecolor='black')
            ax1.axvline(x=up_deviation.mean(), color='darkgreen', linestyle='-', alpha=0.7,
                       label=f'平均值: {up_deviation.mean():.3f}%')
            ax1.set_title(f'{interval} - 上涨市场HMA偏离度')
            ax1.set_xlabel('偏离度 (%)')
            ax1.set_ylabel('频次')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
        
        # 下跌市场
        ax2 = axes[i, 1]
        down_market = df[df['price_change'] < -0.01]  # 跌幅>1%
        if len(down_market) > 0:
            down_deviation = down_market['hma_deviation'].dropna()
            ax2.hist(down_deviation, bins=30, alpha=0.7, color='red', edgecolor='black')
            ax2.axvline(x=down_deviation.mean(), color='darkred', linestyle='-', alpha=0.7,
                       label=f'平均值: {down_deviation.mean():.3f}%')
            ax2.set_title(f'{interval} - 下跌市场HMA偏离度')
            ax2.set_xlabel('偏离度 (%)')
            ax2.set_ylabel('频次')
            ax2.legend()
            ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('market_conditions_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

def main():
    """主函数"""
    print("🎨 ETH HMA 可视化分析")
    print("=" * 50)
    
    # 加载数据
    data = load_data()
    if not data:
        print("❌ 没有找到可分析的数据文件")
        return
    
    print(f"✅ 加载数据完成: {len(data)} 个时间间隔")
    
    # 创建图表目录
    Path('charts').mkdir(exist_ok=True)
    
    # 生成各种图表
    print("\n📊 生成价格与HMA对比图...")
    plot_price_and_hma(data)
    
    print("📈 生成HMA偏离度分析图...")
    plot_hma_deviation(data)
    
    print("🎯 生成交易信号分析图...")
    plot_trading_signals(data)
    
    print("📊 生成成交量分析图...")
    plot_volume_analysis(data)
    
    print("🔗 生成相关性分析图...")
    plot_correlation_analysis(data)
    
    print("⚡ 生成HMA性能分析图...")
    plot_hma_performance(data)
    
    print("📈 生成市场条件分析图...")
    plot_market_conditions(data)
    
    print("\n✅ 所有图表生成完成！")
    print("📁 图表已保存到当前目录")
    print("\n💡 您也可以启动Jupyter Notebook进行交互式分析:")
    print("   python3 start_jupyter.py")

if __name__ == "__main__":
    main()
