"""
Jupyter可视化模块
专门为Jupyter Notebook环境设计的交互式可视化工具
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 12

# 设置Jupyter内联显示
try:
    from IPython.display import display, HTML
    # %matplotlib inline  # 这个魔法命令只能在Jupyter notebook中使用
except ImportError:
    pass

class JupyterVisualizer:
    """Jupyter可视化器 - 专为交互式分析设计"""
    
    def __init__(self, figsize=(15, 10), style='seaborn-v0_8'):
        """
        初始化Jupyter可视化器
        
        Args:
            figsize: 默认图表大小
            style: matplotlib样式
        """
        self.figsize = figsize
        self.style = style
        plt.style.use(style)
        sns.set_palette("husl")
        
    def plot_price_and_hma(self, df, hma_col='HMA_45', title="ETH价格与HMA走势", 
                          start_date=None, end_date=None, show_turning_points=True):
        """
        绘制价格和HMA曲线图（Jupyter版本）
        
        Args:
            df: 包含价格和HMA数据的DataFrame
            hma_col: HMA列名
            title: 图表标题
            start_date: 开始日期
            end_date: 结束日期
            show_turning_points: 是否显示拐点
        """
        # 数据筛选
        if start_date:
            df = df[df.index >= start_date]
        if end_date:
            df = df[df.index <= end_date]
            
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # 绘制价格曲线
        ax.plot(df.index, df['close'], label='ETH价格', color='lightgray', alpha=0.7, linewidth=1)
        
        # 绘制HMA曲线
        if hma_col in df.columns:
            ax.plot(df.index, df[hma_col], label=f'{hma_col}曲线', color='blue', linewidth=2)
        
        # 显示拐点
        if show_turning_points and 'turning_point' in df.columns:
            up_turns = df[df['turning_point'] == 1]
            down_turns = df[df['turning_point'] == -1]
            
            ax.scatter(up_turns.index, up_turns['close'], 
                      marker='^', color='green', s=100, label='上涨拐点', zorder=5)
            ax.scatter(down_turns.index, down_turns['close'], 
                      marker='v', color='red', s=100, label='下跌拐点', zorder=5)
        
        # 设置图表
        ax.set_title(title, fontsize=16, fontweight='bold')
        ax.set_xlabel('时间', fontsize=12)
        ax.set_ylabel('价格 (USDT)', fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # 格式化x轴日期
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        plt.show()
        
        return fig, ax
    
    def plot_strategy_performance(self, uptrend_analysis, downtrend_analysis, 
                                title="策略表现分析"):
        """
        绘制策略表现分析图（Jupyter版本）
        
        Args:
            uptrend_analysis: 上涨趋势分析结果
            downtrend_analysis: 下跌趋势分析结果
            title: 图表标题
        """
        fig, axes = plt.subplots(2, 2, figsize=(18, 12))
        
        # 1. 做多策略表现
        long_ideal = uptrend_analysis.get('avg_long_ideal_profit', 0)
        long_actual = uptrend_analysis.get('avg_long_actual_profit', 0)
        long_risk = uptrend_analysis.get('avg_long_risk_loss', 0)
        
        axes[0, 0].bar(['理想收益', '实际收益', '风险损失'], 
                     [long_ideal, long_actual, long_risk], 
                     color=['green', 'lightgreen', 'red'])
        axes[0, 0].set_title('做多策略表现', fontsize=14, fontweight='bold')
        axes[0, 0].set_ylabel('百分比 (%)', fontsize=12)
        axes[0, 0].grid(axis='y', alpha=0.3)
        
        # 2. 做空策略表现
        short_ideal = downtrend_analysis.get('avg_short_ideal_profit', 0)
        short_actual = downtrend_analysis.get('avg_short_actual_profit', 0)
        short_risk = downtrend_analysis.get('avg_short_risk_loss', 0)
        
        axes[0, 1].bar(['理想收益', '实际收益', '风险损失'], 
                     [short_ideal, short_actual, short_risk], 
                     color=['red', 'salmon', 'green'])
        axes[0, 1].set_title('做空策略表现', fontsize=14, fontweight='bold')
        axes[0, 1].set_ylabel('百分比 (%)', fontsize=12)
        axes[0, 1].grid(axis='y', alpha=0.3)
        
        # 3. 风险收益比对比
        long_rr = uptrend_analysis.get('avg_risk_reward_ratio', 0)
        short_rr = downtrend_analysis.get('avg_risk_reward_ratio', 0)
        
        axes[1, 0].bar(['做多风险收益比', '做空风险收益比'], 
                     [long_rr, short_rr], 
                     color=['green', 'red'])
        axes[1, 0].set_title('风险收益比对比', fontsize=14, fontweight='bold')
        axes[1, 0].set_ylabel('风险收益比', fontsize=12)
        axes[1, 0].grid(axis='y', alpha=0.3)
        
        # 4. 胜率对比
        long_win_rate = uptrend_analysis.get('win_rate', 0) * 100
        short_win_rate = downtrend_analysis.get('win_rate', 0) * 100
        
        axes[1, 1].bar(['做多胜率', '做空胜率'], 
                     [long_win_rate, short_win_rate], 
                     color=['green', 'red'])
        axes[1, 1].set_title('策略胜率对比', fontsize=14, fontweight='bold')
        axes[1, 1].set_ylabel('胜率 (%)', fontsize=12)
        axes[1, 1].set_ylim(0, 100)
        axes[1, 1].grid(axis='y', alpha=0.3)
        
        plt.suptitle(title, fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.show()
        
        return fig, axes
    
    def plot_risk_analysis(self, uptrend_analysis, downtrend_analysis, 
                         title="风险分析"):
        """
        绘制风险分析图（Jupyter版本）
        
        Args:
            uptrend_analysis: 上涨趋势分析结果
            downtrend_analysis: 下跌趋势分析结果
            title: 图表标题
        """
        fig, axes = plt.subplots(2, 2, figsize=(18, 12))
        
        # 1. 做多策略风险损失分布
        long_risk_losses = [i['long_risk_loss'] for i in uptrend_analysis.get('intervals', [])]
        if long_risk_losses:
            sns.histplot(long_risk_losses, bins=20, color='red', kde=True, ax=axes[0, 0])
            axes[0, 0].set_title('做多策略风险损失分布', fontsize=14, fontweight='bold')
            axes[0, 0].set_xlabel('风险损失 (%)', fontsize=12)
            axes[0, 0].set_ylabel('频率', fontsize=12)
            axes[0, 0].grid(True, alpha=0.3)
        
        # 2. 做空策略风险损失分布
        short_risk_losses = [i['short_risk_loss'] for i in downtrend_analysis.get('intervals', [])]
        if short_risk_losses:
            sns.histplot(short_risk_losses, bins=20, color='red', kde=True, ax=axes[0, 1])
            axes[0, 1].set_title('做空策略风险损失分布', fontsize=14, fontweight='bold')
            axes[0, 1].set_xlabel('风险损失 (%)', fontsize=12)
            axes[0, 1].set_ylabel('频率', fontsize=12)
            axes[0, 1].grid(True, alpha=0.3)
        
        # 3. 收益分布对比
        long_ideal_profits = [i['long_ideal_profit'] for i in uptrend_analysis.get('intervals', [])]
        short_ideal_profits = [i['short_ideal_profit'] for i in downtrend_analysis.get('intervals', [])]
        
        if long_ideal_profits or short_ideal_profits:
            if long_ideal_profits:
                sns.histplot(long_ideal_profits, bins=20, color='green', alpha=0.6, 
                           label='做多理想收益', ax=axes[1, 0])
            if short_ideal_profits:
                sns.histplot(short_ideal_profits, bins=20, color='red', alpha=0.6, 
                           label='做空理想收益', ax=axes[1, 0])
            axes[1, 0].set_title('理想收益分布对比', fontsize=14, fontweight='bold')
            axes[1, 0].set_xlabel('收益 (%)', fontsize=12)
            axes[1, 0].set_ylabel('频率', fontsize=12)
            axes[1, 0].legend()
            axes[1, 0].grid(True, alpha=0.3)
        
        # 4. 风险收益散点图
        long_risks = [i['long_risk_loss'] for i in uptrend_analysis.get('intervals', [])]
        long_rewards = [i['long_ideal_profit'] for i in uptrend_analysis.get('intervals', [])]
        short_risks = [i['short_risk_loss'] for i in downtrend_analysis.get('intervals', [])]
        short_rewards = [i['short_ideal_profit'] for i in downtrend_analysis.get('intervals', [])]
        
        if long_risks or short_risks:
            if long_risks:
                axes[1, 1].scatter(long_risks, long_rewards, color='green', alpha=0.6, 
                                 label='做多策略', s=50)
            if short_risks:
                axes[1, 1].scatter(short_risks, short_rewards, color='red', alpha=0.6, 
                                 label='做空策略', s=50)
            axes[1, 1].set_title('风险 vs 收益散点图', fontsize=14, fontweight='bold')
            axes[1, 1].set_xlabel('最大风险损失 (%)', fontsize=12)
            axes[1, 1].set_ylabel('最大理想收益 (%)', fontsize=12)
            axes[1, 1].legend()
            axes[1, 1].grid(True, alpha=0.3)
            # 添加1:1线
            max_val = max(max(long_risks + [0]), max(short_risks + [0]), 
                         max(long_rewards + [0]), max(short_rewards + [0]))
            axes[1, 1].plot([0, max_val], [0, max_val], 'k--', alpha=0.5, label='1:1线')
        
        plt.suptitle(title, fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.show()
        
        return fig, axes
    
    def plot_trend_intervals(self, df, intervals, title="趋势区间分析"):
        """
        绘制趋势区间分析图（Jupyter版本）
        
        Args:
            df: 包含价格数据的DataFrame
            intervals: 趋势区间列表
            title: 图表标题
        """
        fig, ax = plt.subplots(figsize=(18, 10))
        
        # 绘制价格曲线
        ax.plot(df.index, df['close'], label='ETH价格', color='lightgray', alpha=0.7)
        
        # 绘制趋势区间
        colors = ['green', 'red']
        for i, interval in enumerate(intervals):
            start_idx = interval['start_idx']
            end_idx = interval['end_idx']
            direction = interval['direction']
            
            color = colors[0] if direction == 'up' else colors[1]
            ax.axvspan(df.index[start_idx], df.index[end_idx], 
                      alpha=0.3, color=color, 
                      label=f'{direction}趋势' if i < 2 else "")
        
        # 设置图表
        ax.set_title(title, fontsize=16, fontweight='bold')
        ax.set_xlabel('时间', fontsize=12)
        ax.set_ylabel('价格 (USDT)', fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # 格式化x轴日期
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        plt.show()
        
        return fig, ax
    
    def display_strategy_summary(self, uptrend_analysis, downtrend_analysis):
        """
        显示策略分析摘要（Jupyter版本）
        
        Args:
            uptrend_analysis: 上涨趋势分析结果
            downtrend_analysis: 下跌趋势分析结果
        """
        print("📊 策略分析摘要")
        print("=" * 50)
        
        # 做多策略摘要
        print("\n🟢 做多策略 (上涨趋势):")
        print(f"  总趋势数: {uptrend_analysis.get('total_uptrends', 0)}")
        print(f"  平均理想收益: {uptrend_analysis.get('avg_long_ideal_profit', 0):.2f}%")
        print(f"  平均实际收益: {uptrend_analysis.get('avg_long_actual_profit', 0):.2f}%")
        print(f"  平均风险损失: {uptrend_analysis.get('avg_long_risk_loss', 0):.2f}%")
        print(f"  平均风险收益比: {uptrend_analysis.get('avg_risk_reward_ratio', 0):.2f}")
        print(f"  胜率: {uptrend_analysis.get('win_rate', 0):.2%}")
        
        # 做空策略摘要
        print("\n🔴 做空策略 (下跌趋势):")
        print(f"  总趋势数: {downtrend_analysis.get('total_downtrends', 0)}")
        print(f"  平均理想收益: {downtrend_analysis.get('avg_short_ideal_profit', 0):.2f}%")
        print(f"  平均实际收益: {downtrend_analysis.get('avg_short_actual_profit', 0):.2f}%")
        print(f"  平均风险损失: {downtrend_analysis.get('avg_short_risk_loss', 0):.2f}%")
        print(f"  平均风险收益比: {downtrend_analysis.get('avg_risk_reward_ratio', 0):.2f}")
        print(f"  胜率: {downtrend_analysis.get('win_rate', 0):.2%}")
        
        print("\n" + "=" * 50)
    
    def create_interactive_dashboard(self, df, uptrend_analysis, downtrend_analysis):
        """
        创建交互式仪表板（Jupyter版本）
        
        Args:
            df: 包含价格数据的DataFrame
            uptrend_analysis: 上涨趋势分析结果
            downtrend_analysis: 下跌趋势分析结果
        """
        # 显示摘要
        self.display_strategy_summary(uptrend_analysis, downtrend_analysis)
        
        # 创建综合图表
        fig, axes = plt.subplots(3, 2, figsize=(20, 15))
        
        # 1. 价格和HMA走势
        ax1 = axes[0, 0]
        ax1.plot(df.index, df['close'], label='ETH价格', color='lightgray', alpha=0.7)
        if 'HMA_45' in df.columns:
            ax1.plot(df.index, df['HMA_45'], label='HMA_45', color='blue')
        ax1.set_title('ETH价格与HMA走势', fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. 策略表现对比
        ax2 = axes[0, 1]
        categories = ['做多理想收益', '做多实际收益', '做空理想收益', '做空实际收益']
        values = [
            uptrend_analysis.get('avg_long_ideal_profit', 0),
            uptrend_analysis.get('avg_long_actual_profit', 0),
            downtrend_analysis.get('avg_short_ideal_profit', 0),
            downtrend_analysis.get('avg_short_actual_profit', 0)
        ]
        colors = ['green', 'lightgreen', 'red', 'salmon']
        ax2.bar(categories, values, color=colors)
        ax2.set_title('策略表现对比', fontweight='bold')
        ax2.set_ylabel('收益 (%)')
        ax2.tick_params(axis='x', rotation=45)
        
        # 3. 风险分析
        ax3 = axes[1, 0]
        risk_categories = ['做多风险损失', '做空风险损失']
        risk_values = [
            uptrend_analysis.get('avg_long_risk_loss', 0),
            downtrend_analysis.get('avg_short_risk_loss', 0)
        ]
        ax3.bar(risk_categories, risk_values, color=['red', 'red'])
        ax3.set_title('风险损失分析', fontweight='bold')
        ax3.set_ylabel('风险损失 (%)')
        
        # 4. 风险收益比
        ax4 = axes[1, 1]
        rr_categories = ['做多风险收益比', '做空风险收益比']
        rr_values = [
            uptrend_analysis.get('avg_risk_reward_ratio', 0),
            downtrend_analysis.get('avg_risk_reward_ratio', 0)
        ]
        ax4.bar(rr_categories, rr_values, color=['green', 'red'])
        ax4.set_title('风险收益比分析', fontweight='bold')
        ax4.set_ylabel('风险收益比')
        
        # 5. 胜率对比
        ax5 = axes[2, 0]
        win_categories = ['做多胜率', '做空胜率']
        win_values = [
            uptrend_analysis.get('win_rate', 0) * 100,
            downtrend_analysis.get('win_rate', 0) * 100
        ]
        ax5.bar(win_categories, win_values, color=['green', 'red'])
        ax5.set_title('策略胜率对比', fontweight='bold')
        ax5.set_ylabel('胜率 (%)')
        ax5.set_ylim(0, 100)
        
        # 6. 趋势数量统计
        ax6 = axes[2, 1]
        trend_categories = ['上涨趋势数', '下跌趋势数']
        trend_values = [
            uptrend_analysis.get('total_uptrends', 0),
            downtrend_analysis.get('total_downtrends', 0)
        ]
        ax6.bar(trend_categories, trend_values, color=['green', 'red'])
        ax6.set_title('趋势数量统计', fontweight='bold')
        ax6.set_ylabel('趋势数量')
        
        plt.suptitle('ETH HMA策略分析仪表板', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.show()
        
        return fig, axes
