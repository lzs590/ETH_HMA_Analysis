#!/usr/bin/env python3
"""
快速可视化分析
生成关键图表进行HMA分析
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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

def create_comprehensive_analysis(data):
    """创建综合分析图表"""
    fig = plt.figure(figsize=(20, 15))
    
    # 创建子图布局
    gs = fig.add_gridspec(4, 3, hspace=0.3, wspace=0.3)
    
    # 1. 价格与HMA对比 (1小时)
    ax1 = fig.add_subplot(gs[0, :2])
    df_1h = data['1h']
    ax1.plot(df_1h.index, df_1h['close'], label='ETH价格', linewidth=0.8, alpha=0.8, color='blue')
    ax1.plot(df_1h.index, df_1h['HMA_45'], label='HMA_45', linewidth=1.2, alpha=0.9, color='red')
    ax1.fill_between(df_1h.index, df_1h['close'], df_1h['HMA_45'], 
                    where=(df_1h['close'] >= df_1h['HMA_45']), 
                    color='green', alpha=0.2)
    ax1.fill_between(df_1h.index, df_1h['close'], df_1h['HMA_45'], 
                    where=(df_1h['close'] < df_1h['HMA_45']), 
                    color='red', alpha=0.2)
    ax1.set_title('ETH价格与HMA对比 (1小时)', fontsize=14, fontweight='bold')
    ax1.set_ylabel('价格 (USDT)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 2. HMA偏离度 (1小时)
    ax2 = fig.add_subplot(gs[0, 2])
    deviation_1h = df_1h['hma_deviation'].dropna()
    ax2.hist(deviation_1h, bins=50, alpha=0.7, color='purple', edgecolor='black')
    ax2.axvline(x=0, color='red', linestyle='--', alpha=0.7)
    ax2.axvline(x=deviation_1h.mean(), color='green', linestyle='-', alpha=0.7)
    ax2.set_title('HMA偏离度分布 (1小时)')
    ax2.set_xlabel('偏离度 (%)')
    ax2.set_ylabel('频次')
    ax2.grid(True, alpha=0.3)
    
    # 3. 价格与HMA对比 (4小时)
    ax3 = fig.add_subplot(gs[1, :2])
    df_4h = data['4h']
    ax3.plot(df_4h.index, df_4h['close'], label='ETH价格', linewidth=0.8, alpha=0.8, color='blue')
    ax3.plot(df_4h.index, df_4h['HMA_45'], label='HMA_45', linewidth=1.2, alpha=0.9, color='red')
    ax3.fill_between(df_4h.index, df_4h['close'], df_4h['HMA_45'], 
                    where=(df_4h['close'] >= df_4h['HMA_45']), 
                    color='green', alpha=0.2)
    ax3.fill_between(df_4h.index, df_4h['close'], df_4h['HMA_45'], 
                    where=(df_4h['close'] < df_4h['HMA_45']), 
                    color='red', alpha=0.2)
    ax3.set_title('ETH价格与HMA对比 (4小时)', fontsize=14, fontweight='bold')
    ax3.set_ylabel('价格 (USDT)')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # 4. HMA偏离度 (4小时)
    ax4 = fig.add_subplot(gs[1, 2])
    deviation_4h = df_4h['hma_deviation'].dropna()
    ax4.hist(deviation_4h, bins=50, alpha=0.7, color='purple', edgecolor='black')
    ax4.axvline(x=0, color='red', linestyle='--', alpha=0.7)
    ax4.axvline(x=deviation_4h.mean(), color='green', linestyle='-', alpha=0.7)
    ax4.set_title('HMA偏离度分布 (4小时)')
    ax4.set_xlabel('偏离度 (%)')
    ax4.set_ylabel('频次')
    ax4.grid(True, alpha=0.3)
    
    # 5. 交易信号分析 (1小时)
    ax5 = fig.add_subplot(gs[2, :])
    df_signal = df_1h.copy()
    df_signal['hma_signal'] = np.where(df_signal['close'] > df_signal['HMA_45'], 1, -1)
    df_signal['signal_change'] = df_signal['hma_signal'].diff()
    
    ax5.plot(df_signal.index, df_signal['close'], label='ETH价格', linewidth=0.8, alpha=0.8)
    ax5.plot(df_signal.index, df_signal['HMA_45'], label='HMA_45', linewidth=1.2, alpha=0.9)
    
    # 标记交易信号
    buy_signals = df_signal[df_signal['signal_change'] == 2]
    sell_signals = df_signal[df_signal['signal_change'] == -2]
    
    ax5.scatter(buy_signals.index, buy_signals['close'], 
               color='green', alpha=0.7, s=15, label=f'买入信号 ({len(buy_signals)})', marker='^')
    ax5.scatter(sell_signals.index, sell_signals['close'], 
               color='red', alpha=0.7, s=15, label=f'卖出信号 ({len(sell_signals)})', marker='v')
    
    ax5.set_title('HMA交易信号分析 (1小时)', fontsize=14, fontweight='bold')
    ax5.set_ylabel('价格 (USDT)')
    ax5.legend()
    ax5.grid(True, alpha=0.3)
    
    # 6. 相关性分析
    ax6 = fig.add_subplot(gs[3, 0])
    corr_data = df_1h[['close', 'HMA_45', 'price_change', 'hma_deviation']].corr()
    im = ax6.imshow(corr_data, cmap='coolwarm', aspect='auto', vmin=-1, vmax=1)
    ax6.set_xticks(range(len(corr_data.columns)))
    ax6.set_yticks(range(len(corr_data.columns)))
    ax6.set_xticklabels(corr_data.columns, rotation=45)
    ax6.set_yticklabels(corr_data.columns)
    ax6.set_title('变量相关性矩阵')
    
    # 添加数值标注
    for i in range(len(corr_data.columns)):
        for j in range(len(corr_data.columns)):
            text = ax6.text(j, i, f'{corr_data.iloc[i, j]:.3f}',
                           ha="center", va="center", color="black", fontsize=8)
    
    # 7. 价格变化分布
    ax7 = fig.add_subplot(gs[3, 1])
    price_changes = df_1h['price_change'].dropna() * 100
    ax7.hist(price_changes, bins=100, alpha=0.7, color='skyblue', edgecolor='black')
    ax7.axvline(x=0, color='red', linestyle='--', alpha=0.7)
    ax7.axvline(x=price_changes.mean(), color='green', linestyle='-', alpha=0.7)
    ax7.set_title('价格变化分布')
    ax7.set_xlabel('价格变化 (%)')
    ax7.set_ylabel('频次')
    ax7.grid(True, alpha=0.3)
    
    # 8. 统计信息
    ax8 = fig.add_subplot(gs[3, 2])
    ax8.axis('off')
    
    # 计算统计信息
    stats_text = f"""
    📊 HMA分析统计
    
    1小时数据:
    • 记录数: {len(df_1h):,}
    • 价格范围: ${df_1h['close'].min():.2f} - ${df_1h['close'].max():.2f}
    • 平均价格: ${df_1h['close'].mean():.2f}
    • HMA相关性: {df_1h['close'].corr(df_1h['HMA_45']):.4f}
    • 平均偏离度: {deviation_1h.mean():.3f}%
    • 偏离度标准差: {deviation_1h.std():.3f}%
    
    4小时数据:
    • 记录数: {len(df_4h):,}
    • 价格范围: ${df_4h['close'].min():.2f} - ${df_4h['close'].max():.2f}
    • 平均价格: ${df_4h['close'].mean():.2f}
    • HMA相关性: {df_4h['close'].corr(df_4h['HMA_45']):.4f}
    • 平均偏离度: {deviation_4h.mean():.3f}%
    • 偏离度标准差: {deviation_4h.std():.3f}%
    
    交易信号:
    • 买入信号: {len(buy_signals):,} 次
    • 卖出信号: {len(sell_signals):,} 次
    • 信号频率: {(len(buy_signals) + len(sell_signals)) / len(df_1h) * 100:.1f}%
    """
    
    ax8.text(0.05, 0.95, stats_text, transform=ax8.transAxes, fontsize=10,
             verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.8))
    
    plt.suptitle('ETH HMA 综合分析报告', fontsize=18, fontweight='bold', y=0.98)
    plt.savefig('ETH_HMA_Comprehensive_Analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

def main():
    """主函数"""
    print("🎨 ETH HMA 快速可视化分析")
    print("=" * 50)
    
    # 加载数据
    data = load_data()
    if not data:
        print("❌ 没有找到可分析的数据文件")
        return
    
    print(f"✅ 加载数据完成: {len(data)} 个时间间隔")
    print("📊 生成综合分析图表...")
    
    # 创建综合分析图表
    create_comprehensive_analysis(data)
    
    print("✅ 可视化分析完成！")
    print("📁 图表已保存为: ETH_HMA_Comprehensive_Analysis.png")
    print("\n💡 您也可以启动Jupyter Notebook进行交互式分析:")
    print("   python3 start_jupyter.py")

if __name__ == "__main__":
    main()
