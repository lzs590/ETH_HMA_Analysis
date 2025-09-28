"""
策略可视化模块
专门为HMA趋势策略创建专业的可视化图表
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# 设置英文字体 - 使用英文标签
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 设置英文字体
matplotlib.rcdefaults()  # 重置所有设置

# 设置英文字体
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Liberation Sans', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 10

# 确保matplotlib全局设置也生效
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Liberation Sans', 'sans-serif']
matplotlib.rcParams['axes.unicode_minus'] = False
matplotlib.rcParams['font.size'] = 10

class StrategyVisualizer:
    """策略可视化器"""
    
    def __init__(self, output_dir: str = "assets/charts"):
        """
        初始化策略可视化器
        
        Args:
            output_dir: 图表输出目录
        """
        self.output_dir = output_dir
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 设置图表样式
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
    def create_strategy_overview(self, df: pd.DataFrame, intervals: list, 
                               uptrend_analysis: dict, downtrend_analysis: dict, 
                               interval: str) -> str:
        """
        创建策略总览图表
        
        Args:
            df: 包含HMA数据的DataFrame
            intervals: 趋势区间列表
            uptrend_analysis: 上涨趋势分析结果
            downtrend_analysis: 下跌趋势分析结果
            interval: 时间间隔
            
        Returns:
            图表文件路径
        """
        fig, axes = plt.subplots(2, 2, figsize=(20, 16))
        fig.suptitle(f'ETH HMA{interval}策略总览分析', fontsize=20, fontweight='bold')
        
        # 1. 价格走势和HMA曲线
        ax1 = axes[0, 0]
        ax1.plot(df.index, df['close'], label='ETH价格', alpha=0.7, linewidth=1)
        ax1.plot(df.index, df[f'HMA_45'], label='HMA45', linewidth=2, color='red')
        
        # 标记拐点
        turning_points = df[df['turning_point'] != 0]
        up_points = turning_points[turning_points['turning_point'] == 1]
        down_points = turning_points[turning_points['turning_point'] == -1]
        
        ax1.scatter(up_points.index, up_points['close'], 
                   color='green', marker='^', s=100, label='上涨拐点', zorder=5)
        ax1.scatter(down_points.index, down_points['close'], 
                   color='red', marker='v', s=100, label='下跌拐点', zorder=5)
        
        ax1.set_title('价格走势与HMA趋势识别', fontsize=14, fontweight='bold')
        ax1.set_ylabel('价格 (USDT)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. 策略收益分布
        ax2 = axes[0, 1]
        
        # 做多策略收益
        long_profits = [interval['long_actual_profit'] for interval in uptrend_analysis.get('intervals', [])]
        # 做空策略收益
        short_profits = [interval['short_actual_profit'] for interval in downtrend_analysis.get('intervals', [])]
        
        if long_profits:
            ax2.hist(long_profits, bins=20, alpha=0.7, label='做多策略收益', color='green')
        if short_profits:
            ax2.hist(short_profits, bins=20, alpha=0.7, label='做空策略收益', color='red')
        
        ax2.axvline(0, color='black', linestyle='--', alpha=0.5)
        ax2.set_title('策略收益分布', fontsize=14, fontweight='bold')
        ax2.set_xlabel('收益率 (%)')
        ax2.set_ylabel('频次')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 3. 风险收益散点图
        ax3 = axes[1, 0]
        
        # 做多策略风险收益
        long_risks = [interval['long_risk_loss'] for interval in uptrend_analysis.get('intervals', [])]
        long_rewards = [interval['long_ideal_profit'] for interval in uptrend_analysis.get('intervals', [])]
        
        if long_risks and long_rewards:
            ax3.scatter(long_risks, long_rewards, alpha=0.6, label='做多策略', color='green', s=50)
        
        # 做空策略风险收益
        short_risks = [interval['short_risk_loss'] for interval in downtrend_analysis.get('intervals', [])]
        short_rewards = [interval['short_ideal_profit'] for interval in downtrend_analysis.get('intervals', [])]
        
        if short_risks and short_rewards:
            ax3.scatter(short_risks, short_rewards, alpha=0.6, label='做空策略', color='red', s=50)
        
        ax3.set_title('风险收益散点图', fontsize=14, fontweight='bold')
        ax3.set_xlabel('风险损失 (%)')
        ax3.set_ylabel('理想收益 (%)')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # 4. 策略统计摘要
        ax4 = axes[1, 1]
        ax4.axis('off')
        
        # 创建统计摘要文本
        stats_text = f"""
策略统计摘要

📈 做多策略:
• 总交易次数: {uptrend_analysis.get('total_uptrends', 0)}
• 平均理想收益: {uptrend_analysis.get('avg_long_ideal_profit', 0):.2f}%
• 最大理想收益: {uptrend_analysis.get('max_long_ideal_profit', 0):.2f}%
• 平均实际收益: {uptrend_analysis.get('avg_long_actual_profit', 0):.2f}%
• 平均风险损失: {uptrend_analysis.get('avg_long_risk_loss', 0):.2f}%
• 风险收益比: {uptrend_analysis.get('avg_risk_reward_ratio', 0):.2f}

📉 做空策略:
• 总交易次数: {downtrend_analysis.get('total_downtrends', 0)}
• 平均理想收益: {downtrend_analysis.get('avg_short_ideal_profit', 0):.2f}%
• 最大理想收益: {downtrend_analysis.get('max_short_ideal_profit', 0):.2f}%
• 平均实际收益: {downtrend_analysis.get('avg_short_actual_profit', 0):.2f}%
• 平均风险损失: {downtrend_analysis.get('avg_short_risk_loss', 0):.2f}%
• 风险收益比: {downtrend_analysis.get('avg_risk_reward_ratio', 0):.2f}
        """
        
        ax4.text(0.05, 0.95, stats_text, transform=ax4.transAxes, fontsize=11,
                verticalalignment='top', fontfamily='monospace',
                bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgray", alpha=0.8))
        
        plt.tight_layout()
        
        # 保存图表
        filename = f"strategy_overview_{interval}_{self.timestamp}.png"
        filepath = f"{self.output_dir}/{filename}"
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filepath
    
    def create_strategy_performance(self, uptrend_analysis: dict, downtrend_analysis: dict, 
                                   interval: str) -> str:
        """
        创建策略表现分析图表
        
        Args:
            uptrend_analysis: 上涨趋势分析结果
            downtrend_analysis: 下跌趋势分析结果
            interval: 时间间隔
            
        Returns:
            图表文件路径
        """
        fig, axes = plt.subplots(2, 2, figsize=(18, 14))
        fig.suptitle(f'ETH HMA{interval}策略表现分析', fontsize=18, fontweight='bold')
        
        # 1. 理想收益 vs 实际收益对比
        ax1 = axes[0, 0]
        
        strategies = ['做多策略', '做空策略']
        ideal_profits = [
            uptrend_analysis.get('avg_long_ideal_profit', 0),
            downtrend_analysis.get('avg_short_ideal_profit', 0)
        ]
        actual_profits = [
            uptrend_analysis.get('avg_long_actual_profit', 0),
            downtrend_analysis.get('avg_short_actual_profit', 0)
        ]
        
        x = np.arange(len(strategies))
        width = 0.35
        
        bars1 = ax1.bar(x - width/2, ideal_profits, width, label='理想收益', alpha=0.8, color='lightblue')
        bars2 = ax1.bar(x + width/2, actual_profits, width, label='实际收益', alpha=0.8, color='orange')
        
        ax1.set_title('理想收益 vs 实际收益对比', fontsize=14, fontweight='bold')
        ax1.set_ylabel('收益率 (%)')
        ax1.set_xticks(x)
        ax1.set_xticklabels(strategies)
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 添加数值标签
        for bar in bars1:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{height:.2f}%', ha='center', va='bottom')
        for bar in bars2:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{height:.2f}%', ha='center', va='bottom')
        
        # 2. 风险收益比分析
        ax2 = axes[0, 1]
        
        risk_reward_ratios = [
            uptrend_analysis.get('avg_risk_reward_ratio', 0),
            downtrend_analysis.get('avg_risk_reward_ratio', 0)
        ]
        
        colors = ['green', 'red']
        bars = ax2.bar(strategies, risk_reward_ratios, color=colors, alpha=0.7)
        
        ax2.set_title('风险收益比分析', fontsize=14, fontweight='bold')
        ax2.set_ylabel('风险收益比')
        ax2.grid(True, alpha=0.3)
        
        # 添加数值标签
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                    f'{height:.2f}', ha='center', va='bottom')
        
        # 3. 最大收益分析
        ax3 = axes[1, 0]
        
        max_ideal_profits = [
            uptrend_analysis.get('max_long_ideal_profit', 0),
            downtrend_analysis.get('max_short_ideal_profit', 0)
        ]
        max_actual_profits = [
            uptrend_analysis.get('max_long_actual_profit', 0),
            downtrend_analysis.get('max_short_actual_profit', 0)
        ]
        
        bars1 = ax3.bar(x - width/2, max_ideal_profits, width, label='最大理想收益', alpha=0.8, color='lightgreen')
        bars2 = ax3.bar(x + width/2, max_actual_profits, width, label='最大实际收益', alpha=0.8, color='lightcoral')
        
        ax3.set_title('最大收益分析', fontsize=14, fontweight='bold')
        ax3.set_ylabel('收益率 (%)')
        ax3.set_xticks(x)
        ax3.set_xticklabels(strategies)
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # 4. 风险损失分析
        ax4 = axes[1, 1]
        
        avg_risks = [
            uptrend_analysis.get('avg_long_risk_loss', 0),
            downtrend_analysis.get('avg_short_risk_loss', 0)
        ]
        max_risks = [
            uptrend_analysis.get('max_long_risk_loss', 0),
            downtrend_analysis.get('max_short_risk_loss', 0)
        ]
        
        bars1 = ax4.bar(x - width/2, avg_risks, width, label='平均风险损失', alpha=0.8, color='lightcoral')
        bars2 = ax4.bar(x + width/2, max_risks, width, label='最大风险损失', alpha=0.8, color='darkred')
        
        ax4.set_title('风险损失分析', fontsize=14, fontweight='bold')
        ax4.set_ylabel('损失率 (%)')
        ax4.set_xticks(x)
        ax4.set_xticklabels(strategies)
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # 保存图表
        filename = f"strategy_performance_{interval}_{self.timestamp}.png"
        filepath = f"{self.output_dir}/{filename}"
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filepath
    
    def create_risk_analysis(self, uptrend_analysis: dict, downtrend_analysis: dict, 
                           interval: str) -> str:
        """
        创建风险分析图表
        
        Args:
            uptrend_analysis: 上涨趋势分析结果
            downtrend_analysis: 下跌趋势分析结果
            interval: 时间间隔
            
        Returns:
            图表文件路径
        """
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle(f'ETH HMA{interval}策略风险分析', fontsize=18, fontweight='bold')
        
        # 1. 风险损失分布
        ax1 = axes[0, 0]
        
        long_risks = [interval['long_risk_loss'] for interval in uptrend_analysis.get('intervals', [])]
        short_risks = [interval['short_risk_loss'] for interval in downtrend_analysis.get('intervals', [])]
        
        if long_risks:
            ax1.hist(long_risks, bins=15, alpha=0.7, label='做多策略风险', color='green', density=True)
        if short_risks:
            ax1.hist(short_risks, bins=15, alpha=0.7, label='做空策略风险', color='red', density=True)
        
        ax1.set_title('风险损失分布', fontsize=14, fontweight='bold')
        ax1.set_xlabel('风险损失 (%)')
        ax1.set_ylabel('密度')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. 收益风险散点图
        ax2 = axes[0, 1]
        
        # 做多策略
        if long_risks and uptrend_analysis.get('intervals'):
            long_rewards = [interval['long_ideal_profit'] for interval in uptrend_analysis['intervals']]
            ax2.scatter(long_risks, long_rewards, alpha=0.6, label='做多策略', color='green', s=50)
        
        # 做空策略
        if short_risks and downtrend_analysis.get('intervals'):
            short_rewards = [interval['short_ideal_profit'] for interval in downtrend_analysis['intervals']]
            ax2.scatter(short_risks, short_rewards, alpha=0.6, label='做空策略', color='red', s=50)
        
        ax2.set_title('收益风险散点图', fontsize=14, fontweight='bold')
        ax2.set_xlabel('风险损失 (%)')
        ax2.set_ylabel('理想收益 (%)')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 3. 风险收益比分布
        ax3 = axes[1, 0]
        
        long_ratios = [interval['risk_reward_ratio'] for interval in uptrend_analysis.get('intervals', []) 
                      if interval['risk_reward_ratio'] != float('inf')]
        short_ratios = [interval['risk_reward_ratio'] for interval in downtrend_analysis.get('intervals', []) 
                       if interval['risk_reward_ratio'] != float('inf')]
        
        if long_ratios:
            ax3.hist(long_ratios, bins=15, alpha=0.7, label='做多策略', color='green', density=True)
        if short_ratios:
            ax3.hist(short_ratios, bins=15, alpha=0.7, label='做空策略', color='red', density=True)
        
        ax3.set_title('风险收益比分布', fontsize=14, fontweight='bold')
        ax3.set_xlabel('风险收益比')
        ax3.set_ylabel('密度')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # 4. 策略胜率分析
        ax4 = axes[1, 1]
        
        # 计算胜率
        long_wins = sum(1 for interval in uptrend_analysis.get('intervals', []) 
                       if interval['long_actual_profit'] > 0)
        long_total = len(uptrend_analysis.get('intervals', []))
        long_win_rate = long_wins / long_total if long_total > 0 else 0
        
        short_wins = sum(1 for interval in downtrend_analysis.get('intervals', []) 
                        if interval['short_actual_profit'] > 0)
        short_total = len(downtrend_analysis.get('intervals', []))
        short_win_rate = short_wins / short_total if short_total > 0 else 0
        
        strategies = ['做多策略', '做空策略']
        win_rates = [long_win_rate * 100, short_win_rate * 100]
        
        colors = ['green', 'red']
        bars = ax4.bar(strategies, win_rates, color=colors, alpha=0.7)
        
        ax4.set_title('策略胜率分析', fontsize=14, fontweight='bold')
        ax4.set_ylabel('胜率 (%)')
        ax4.set_ylim(0, 100)
        ax4.grid(True, alpha=0.3)
        
        # 添加数值标签
        for bar in bars:
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{height:.1f}%', ha='center', va='bottom')
        
        plt.tight_layout()
        
        # 保存图表
        filename = f"strategy_risk_analysis_{interval}_{self.timestamp}.png"
        filepath = f"{self.output_dir}/{filename}"
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filepath
