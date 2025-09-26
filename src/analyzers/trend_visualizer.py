"""
趋势分析可视化器

提供丰富的图表来展示趋势分析结果：
1. 拐点识别图
2. 趋势区间分析图
3. 事件分析图
4. 统计分布图
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Optional
import logging
from pathlib import Path
from .trend_analyzer import TrendInterval, EventAnalysis

logger = logging.getLogger(__name__)

# 字体设置将在TrendVisualizer类中根据语言选择进行

class TrendVisualizer:
    """趋势分析可视化器"""
    
    def __init__(self, figsize: tuple = (15, 10), style: str = 'whitegrid', use_chinese: bool = True):
        """
        初始化可视化器
        
        Args:
            figsize: 图表尺寸
            style: 图表样式
            use_chinese: 是否使用中文标签
        """
        self.figsize = figsize
        self.use_chinese = use_chinese
        sns.set_style(style)
        
        # 根据语言设置字体
        self._setup_fonts()
        
        # 设置标签
        if self.use_chinese:
            self.labels = {
                'title_turning_points': 'HMA拐点识别分析',
                'title_price_trend': '价格走势与HMA拐点',
                'title_slope_change': 'HMA斜率变化',
                'title_volume': '成交量',
                'title_volume_no_data': '成交量 (无数据)',
                'price_label': 'ETH价格',
                'hma_label': 'HMA45',
                'slope_label': 'HMA斜率',
                'volume_label': '成交量',
                'up_turn': '上拐点',
                'down_turn': '下拐点',
                'time_label': '时间',
                'price_usdt': '价格 (USDT)',
                'slope_value': '斜率',
                'volume_value': '成交量',
                'title_trend_intervals': '趋势区间分析',
                'title_price_trend_intervals': '价格走势与趋势区间',
                'title_price_change_dist': '区间价格变化分布',
                'title_pfe_vs_mae': 'PFE vs MAE 分析',
                'title_duration_dist': '区间持续时间分布',
                'up_trend': '上升趋势',
                'down_trend': '下降趋势',
                'price_change_pct': '价格变化 (%)',
                'frequency': '频次',
                'duration_cycles': '持续时间 (周期)',
                'title_event_analysis': '事件分析 - 斜率改变时的价格行为',
                'title_price_change_trend': '事件后价格变化趋势',
                'title_volatility_dist': '事件窗口波动率分布',
                'title_consistency_dist': '事件预测一致性分布',
                'title_event_time_dist': '事件时间分布',
                'avg_price_change_pct': '平均价格变化 (%)',
                'periods_after_event': '事件后周期数',
                'annualized_volatility': '年化波动率',
                'consistency_pct': '一致性 (%)',
                'event_type': '事件类型',
                'up': '上升',
                'down': '下降',
                'title_comprehensive': 'ETH HMA趋势分析 - 综合分析报告',
                'title_price_trend_comprehensive': 'ETH价格走势与HMA拐点分析',
                'title_interval_count': '趋势区间数量',
                'title_avg_returns': '平均价格变化',
                'title_max_capture': '最大有利偏移 (PFE)',
                'title_event_consistency': '事件预测一致性分析',
                'count': '数量',
                'change_pct': '变化 (%)',
                'max_pfe_up': '上升最大PFE',
                'max_pfe_down': '下降最大PFE',
                'consistency_up': '上升拐点一致性',
                'consistency_down': '下降拐点一致性',
                'baseline_50': '50%基准线'
            }
        else:
            self.labels = {
                'title_turning_points': 'HMA Turning Points Analysis',
                'title_price_trend': 'Price Trend with HMA Turning Points',
                'title_slope_change': 'HMA Slope Changes',
                'title_volume': 'Volume',
                'title_volume_no_data': 'Volume (No Data)',
                'price_label': 'ETH Price',
                'hma_label': 'HMA45',
                'slope_label': 'HMA Slope',
                'volume_label': 'Volume',
                'up_turn': 'Up Turn',
                'down_turn': 'Down Turn',
                'time_label': 'Time',
                'price_usdt': 'Price (USDT)',
                'slope_value': 'Slope',
                'volume_value': 'Volume',
                'title_trend_intervals': 'Trend Intervals Analysis',
                'title_price_trend_intervals': 'Price Trend with Trend Intervals',
                'title_price_change_dist': 'Price Change Distribution',
                'title_pfe_vs_mae': 'PFE vs MAE Analysis',
                'title_duration_dist': 'Duration Distribution',
                'up_trend': 'Up Trend',
                'down_trend': 'Down Trend',
                'price_change_pct': 'Price Change (%)',
                'frequency': 'Frequency',
                'duration_cycles': 'Duration (Cycles)',
                'title_event_analysis': 'Event Analysis - Price Behavior at Slope Changes',
                'title_price_change_trend': 'Price Change Trend After Events',
                'title_volatility_dist': 'Volatility Distribution',
                'title_consistency_dist': 'Consistency Distribution',
                'title_event_time_dist': 'Event Time Distribution',
                'avg_price_change_pct': 'Average Price Change (%)',
                'periods_after_event': 'Periods After Event',
                'annualized_volatility': 'Annualized Volatility',
                'consistency_pct': 'Consistency (%)',
                'event_type': 'Event Type',
                'up': 'Up',
                'down': 'Down',
                'title_comprehensive': 'ETH HMA Trend Analysis - Comprehensive Report',
                'title_price_trend_comprehensive': 'ETH Price Trend with HMA Turning Points',
                'title_interval_count': 'Trend Interval Count',
                'title_avg_returns': 'Average Price Change',
                'title_max_capture': 'Maximum Favorable Excursion (PFE)',
                'title_event_consistency': 'Event Prediction Consistency Analysis',
                'count': 'Count',
                'change_pct': 'Change (%)',
                'max_pfe_up': 'Max PFE Up',
                'max_pfe_down': 'Max PFE Down',
                'consistency_up': 'Up Turn Consistency',
                'consistency_down': 'Down Turn Consistency',
                'baseline_50': '50% Baseline'
            }
        
        logger.info("趋势可视化器初始化完成")
    
    def _setup_fonts(self):
        """设置字体"""
        import matplotlib
        matplotlib.rcParams['axes.unicode_minus'] = False
        
        if self.use_chinese:
            # 尝试设置中文字体
            try:
                import matplotlib.font_manager as fm
                available_fonts = [f.name for f in fm.fontManager.ttflist]
                
                # 按优先级尝试中文字体
                chinese_fonts = [
                    'Arial Unicode MS',
                    'PingFang SC',
                    'Hiragino Sans GB',
                    'STHeiti',
                    'SimHei',
                    'Microsoft YaHei',
                    'WenQuanYi Micro Hei'
                ]
                
                for font in chinese_fonts:
                    if font in available_fonts:
                        matplotlib.rcParams['font.sans-serif'] = [font] + matplotlib.rcParams['font.sans-serif']
                        logger.info(f"✅ 已设置中文字体: {font}")
                        break
                else:
                    logger.warning("⚠️ 未找到中文字体，图表可能显示为方框")
                    
            except Exception as e:
                logger.warning(f"⚠️ 字体设置失败: {e}")
        else:
            # 使用英文字体，明确避免中文字体
            matplotlib.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Liberation Sans', 'sans-serif']
            matplotlib.rcParams['font.family'] = 'sans-serif'
            # 清除可能的中文字体设置
            if 'font.serif' in matplotlib.rcParams:
                matplotlib.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif', 'serif']
            logger.info("✅ 已设置英文字体")
    
    def plot_turning_points(self, df: pd.DataFrame, save_path: Optional[str] = None) -> None:
        """
        绘制拐点识别图
        
        Args:
            df: 包含拐点数据的DataFrame
            save_path: 保存路径
        """
        logger.info("绘制拐点识别图")
        
        fig, axes = plt.subplots(3, 1, figsize=self.figsize, sharex=True)
        fig.suptitle(self.labels['title_turning_points'], fontsize=16, fontweight='bold')
        
        # 1. 价格和HMA
        ax1 = axes[0]
        ax1.plot(df.index, df['close'], label=self.labels['price_label'], linewidth=1, alpha=0.8)
        ax1.plot(df.index, df[f'HMA_45'], label=self.labels['hma_label'], linewidth=2, color='orange')
        
        # 标记拐点
        up_turns = df[df['turning_point'] == 1]
        down_turns = df[df['turning_point'] == -1]
        
        ax1.scatter(up_turns.index, up_turns['close'], color='green', s=50, marker='^', 
                   label=f"{self.labels['up_turn']} ({len(up_turns)})", zorder=5)
        ax1.scatter(down_turns.index, down_turns['close'], color='red', s=50, marker='v', 
                   label=f"{self.labels['down_turn']} ({len(down_turns)})", zorder=5)
        
        ax1.set_title(self.labels['title_price_trend'])
        ax1.set_ylabel(self.labels['price_usdt'])
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. HMA斜率
        ax2 = axes[1]
        ax2.plot(df.index, df['HMA_slope'], label=self.labels['slope_label'], linewidth=1, alpha=0.8)
        ax2.axhline(y=0, color='black', linestyle='--', alpha=0.5)
        
        # 标记斜率变化
        ax2.scatter(up_turns.index, up_turns['HMA_slope'], color='green', s=30, marker='^', zorder=5)
        ax2.scatter(down_turns.index, down_turns['HMA_slope'], color='red', s=30, marker='v', zorder=5)
        
        ax2.set_title(self.labels['title_slope_change'])
        ax2.set_ylabel(self.labels['slope_value'])
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 3. 成交量（如果有）
        ax3 = axes[2]
        if 'volume' in df.columns:
            ax3.bar(df.index, df['volume'], alpha=0.6, width=0.8)
            ax3.set_title(self.labels['title_volume'])
            ax3.set_ylabel(self.labels['volume_value'])
        else:
            ax3.text(0.5, 0.5, self.labels['title_volume_no_data'], ha='center', va='center', transform=ax3.transAxes)
            ax3.set_title(self.labels['title_volume_no_data'])
        
        ax3.grid(True, alpha=0.3)
        ax3.set_xlabel(self.labels['time_label'])
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"拐点识别图已保存到: {save_path}")
        
        plt.show()
    
    def plot_trend_intervals(self, df: pd.DataFrame, intervals: List[TrendInterval], 
                           save_path: Optional[str] = None) -> None:
        """
        绘制趋势区间分析图
        
        Args:
            df: 原始数据
            intervals: 趋势区间列表
            save_path: 保存路径
        """
        logger.info("绘制趋势区间分析图")
        
        fig, axes = plt.subplots(2, 2, figsize=self.figsize)
        fig.suptitle(self.labels['title_trend_intervals'], fontsize=16, fontweight='bold')
        
        # 1. 价格走势与趋势区间
        ax1 = axes[0, 0]
        ax1.plot(df.index, df['close'], label=self.labels['price_label'], linewidth=1, alpha=0.7, color='blue')
        ax1.plot(df.index, df['HMA_45'], label='HMA45', linewidth=2, color='orange')
        
        # 绘制趋势区间
        colors = ['green' if i.trend_direction == 'up' else 'red' for i in intervals]
        for i, interval in enumerate(intervals):
            start_time = interval.start_time
            end_time = interval.end_time
            ax1.axvspan(start_time, end_time, alpha=0.2, color=colors[i])
            
            # 标记区间开始和结束
            ax1.scatter(start_time, interval.start_price, color=colors[i], s=30, marker='o', zorder=5)
            ax1.scatter(end_time, interval.end_price, color=colors[i], s=30, marker='s', zorder=5)
        
        ax1.set_title(self.labels['title_price_trend_intervals'])
        ax1.set_ylabel(self.labels['price_usdt'])
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. 区间价格变化分布
        ax2 = axes[0, 1]
        up_changes = [i.price_change_pct for i in intervals if i.trend_direction == 'up']
        down_changes = [i.price_change_pct for i in intervals if i.trend_direction == 'down']
        
        if up_changes:
            ax2.hist(up_changes, bins=20, alpha=0.7, label=f'{self.labels["up_trend"]} ({len(up_changes)})', color='green')
        if down_changes:
            ax2.hist(down_changes, bins=20, alpha=0.7, label=f'{self.labels["down_trend"]} ({len(down_changes)})', color='red')
        
        ax2.axvline(x=0, color='black', linestyle='--', alpha=0.5)
        ax2.set_title(self.labels['title_price_change_dist'])
        ax2.set_xlabel(self.labels['price_change_pct'])
        ax2.set_ylabel(self.labels['frequency'])
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 3. PFE vs MAE 散点图
        ax3 = axes[1, 0]
        up_pfe = [i.pfe_pct for i in intervals if i.trend_direction == 'up']
        up_mae = [i.mae_pct for i in intervals if i.trend_direction == 'up']
        down_pfe = [i.pfe_pct for i in intervals if i.trend_direction == 'down']
        down_mae = [i.mae_pct for i in intervals if i.trend_direction == 'down']
        
        if up_pfe and up_mae:
            ax3.scatter(up_mae, up_pfe, alpha=0.7, label='上升趋势', color='green', s=50)
        if down_pfe and down_mae:
            ax3.scatter(down_mae, down_pfe, alpha=0.7, label='下降趋势', color='red', s=50)
        
        ax3.plot([0, max(up_mae + down_mae) if up_mae or down_mae else 0], 
                [0, max(up_pfe + down_pfe) if up_pfe or down_pfe else 0], 
                'k--', alpha=0.5, label='1:1线')
        
        ax3.set_title('PFE vs MAE 分析')
        ax3.set_xlabel('MAE (%)')
        ax3.set_ylabel('PFE (%)')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # 4. 区间持续时间分布
        ax4 = axes[1, 1]
        up_durations = [i.duration for i in intervals if i.trend_direction == 'up']
        down_durations = [i.duration for i in intervals if i.trend_direction == 'down']
        
        if up_durations:
            ax4.hist(up_durations, bins=15, alpha=0.7, label=f'上升趋势 ({len(up_durations)})', color='green')
        if down_durations:
            ax4.hist(down_durations, bins=15, alpha=0.7, label=f'下降趋势 ({len(down_durations)})', color='red')
        
        ax4.set_title('区间持续时间分布')
        ax4.set_xlabel('持续时间 (周期)')
        ax4.set_ylabel('频次')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"趋势区间分析图已保存到: {save_path}")
        
        plt.show()
    
    def plot_event_analysis(self, events: List[EventAnalysis], save_path: Optional[str] = None) -> None:
        """
        绘制事件分析图
        
        Args:
            events: 事件分析列表
            save_path: 保存路径
        """
        logger.info("绘制事件分析图")
        
        if not events:
            logger.warning("没有事件数据可分析")
            return
        
        fig, axes = plt.subplots(2, 2, figsize=self.figsize)
        fig.suptitle(self.labels['title_event_analysis'], fontsize=16, fontweight='bold')
        
        # 分离上升和下降事件
        up_events = [e for e in events if e.event_type == 'up_turn']
        down_events = [e for e in events if e.event_type == 'down_turn']
        
        # 1. 事件后价格变化趋势
        ax1 = axes[0, 0]
        
        if up_events:
            up_changes = np.array([e.price_changes for e in up_events if len(e.price_changes) > 0])
            if len(up_changes) > 0:
                up_mean = np.mean(up_changes, axis=0)
                up_std = np.std(up_changes, axis=0)
                periods = range(1, len(up_mean) + 1)
                ax1.plot(periods, up_mean, 'g-', label=self.labels['up_turn'], linewidth=2)
                ax1.fill_between(periods, up_mean - up_std, up_mean + up_std, alpha=0.3, color='green')
        
        if down_events:
            down_changes = np.array([e.price_changes for e in down_events if len(e.price_changes) > 0])
            if len(down_changes) > 0:
                down_mean = np.mean(down_changes, axis=0)
                down_std = np.std(down_changes, axis=0)
                periods = range(1, len(down_mean) + 1)
                ax1.plot(periods, down_mean, 'r-', label=self.labels['down_turn'], linewidth=2)
                ax1.fill_between(periods, down_mean - down_std, down_mean + down_std, alpha=0.3, color='red')
        
        ax1.axhline(y=0, color='black', linestyle='--', alpha=0.5)
        ax1.set_title(self.labels['title_price_change_trend'])
        ax1.set_xlabel(self.labels['periods_after_event'])
        ax1.set_ylabel(self.labels['avg_price_change_pct'])
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. 波动率分析
        ax2 = axes[0, 1]
        up_volatilities = [e.volatility for e in up_events]
        down_volatilities = [e.volatility for e in down_events]
        
        if up_volatilities:
            ax2.hist(up_volatilities, bins=15, alpha=0.7, label=f'{self.labels["up_turn"]} ({len(up_volatilities)})', color='green')
        if down_volatilities:
            ax2.hist(down_volatilities, bins=15, alpha=0.7, label=f'{self.labels["down_turn"]} ({len(down_volatilities)})', color='red')
        
        ax2.set_title(self.labels['title_volatility_dist'])
        ax2.set_xlabel(self.labels['annualized_volatility'])
        ax2.set_ylabel(self.labels['frequency'])
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 3. 一致性分析
        ax3 = axes[1, 0]
        up_consistencies = [e.consistency for e in up_events]
        down_consistencies = [e.consistency for e in down_events]
        
        if up_consistencies:
            ax3.hist(up_consistencies, bins=15, alpha=0.7, label=f'{self.labels["up_turn"]} ({len(up_consistencies)})', color='green')
        if down_consistencies:
            ax3.hist(down_consistencies, bins=15, alpha=0.7, label=f'{self.labels["down_turn"]} ({len(down_consistencies)})', color='red')
        
        ax3.axvline(x=0.5, color='black', linestyle='--', alpha=0.5, label=self.labels['baseline_50'])
        ax3.set_title(self.labels['title_consistency_dist'])
        ax3.set_xlabel(self.labels['consistency_pct'])
        ax3.set_ylabel(self.labels['frequency'])
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # 4. 事件时间分布
        ax4 = axes[1, 1]
        up_times = [e.event_time for e in up_events]
        down_times = [e.event_time for e in down_events]
        
        if up_times:
            ax4.scatter(up_times, [1] * len(up_times), alpha=0.7, label=f'{self.labels["up_turn"]} ({len(up_times)})', color='green', s=50)
        if down_times:
            ax4.scatter(down_times, [0] * len(down_times), alpha=0.7, label=f'{self.labels["down_turn"]} ({len(down_times)})', color='red', s=50)
        
        ax4.set_title(self.labels['title_event_time_dist'])
        ax4.set_xlabel(self.labels['time_label'])
        ax4.set_ylabel(self.labels['event_type'])
        ax4.set_yticks([0, 1])
        ax4.set_yticklabels([self.labels['down'], self.labels['up']])
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"事件分析图已保存到: {save_path}")
        
        plt.show()
    
    def plot_comprehensive_analysis(self, df: pd.DataFrame, intervals: List[TrendInterval], 
                                  events: List[EventAnalysis], save_path: Optional[str] = None) -> None:
        """
        绘制综合分析图
        
        Args:
            df: 原始数据
            intervals: 趋势区间列表
            events: 事件分析列表
            save_path: 保存路径
        """
        logger.info("绘制综合分析图")
        
        fig = plt.figure(figsize=(20, 12))
        gs = fig.add_gridspec(4, 3, hspace=0.3, wspace=0.3)
        
        fig.suptitle(self.labels['title_comprehensive'], fontsize=18, fontweight='bold')
        
        # 1. 主要价格走势图 (占据上方2行)
        ax_main = fig.add_subplot(gs[0:2, :])
        ax_main.plot(df.index, df['close'], label=self.labels['price_label'], linewidth=1, alpha=0.8, color='blue')
        ax_main.plot(df.index, df['HMA_45'], label='HMA45', linewidth=2, color='orange')
        
        # 标记拐点
        up_turns = df[df['turning_point'] == 1]
        down_turns = df[df['turning_point'] == -1]
        
        ax_main.scatter(up_turns.index, up_turns['close'], color='green', s=30, marker='^', 
                       label=f'上拐点 ({len(up_turns)})', zorder=5)
        ax_main.scatter(down_turns.index, down_turns['close'], color='red', s=30, marker='v', 
                       label=f'下拐点 ({len(down_turns)})', zorder=5)
        
        # 绘制趋势区间
        for interval in intervals:
            color = 'green' if interval.trend_direction == 'up' else 'red'
            ax_main.axvspan(interval.start_time, interval.end_time, alpha=0.1, color=color)
        
        ax_main.set_title(self.labels['title_price_trend_comprehensive'], fontsize=14, fontweight='bold')
        ax_main.set_ylabel(self.labels['price_usdt'])
        ax_main.legend()
        ax_main.grid(True, alpha=0.3)
        
        # 2. 区间统计 (左下)
        ax_stats = fig.add_subplot(gs[2, 0])
        up_intervals = [i for i in intervals if i.trend_direction == 'up']
        down_intervals = [i for i in intervals if i.trend_direction == 'down']
        
        categories = [self.labels['up_trend'], self.labels['down_trend']]
        counts = [len(up_intervals), len(down_intervals)]
        colors = ['green', 'red']
        
        bars = ax_stats.bar(categories, counts, color=colors, alpha=0.7)
        ax_stats.set_title(self.labels['title_interval_count'])
        ax_stats.set_ylabel(self.labels['count'])
        
        # 添加数值标签
        for bar, count in zip(bars, counts):
            ax_stats.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                         str(count), ha='center', va='bottom')
        
        # 3. 平均收益 (中下)
        ax_returns = fig.add_subplot(gs[2, 1])
        up_returns = [i.price_change_pct for i in up_intervals] if up_intervals else [0]
        down_returns = [i.price_change_pct for i in down_intervals] if down_intervals else [0]
        
        avg_up = np.mean(up_returns) if up_returns else 0
        avg_down = np.mean(down_returns) if down_returns else 0
        
        categories = [self.labels['up_trend'], self.labels['down_trend']]
        returns = [avg_up, avg_down]
        colors = ['green' if r > 0 else 'red' for r in returns]
        
        bars = ax_returns.bar(categories, returns, color=colors, alpha=0.7)
        ax_returns.set_title(self.labels['title_avg_returns'])
        ax_returns.set_ylabel(self.labels['change_pct'])
        ax_returns.axhline(y=0, color='black', linestyle='--', alpha=0.5)
        
        # 添加数值标签
        for bar, ret in zip(bars, returns):
            ax_returns.text(bar.get_x() + bar.get_width()/2, bar.get_height() + (0.1 if ret > 0 else -0.1), 
                           f'{ret:.2f}%', ha='center', va='bottom' if ret > 0 else 'top')
        
        # 4. 最大捕获分析 (右下)
        ax_capture = fig.add_subplot(gs[2, 2])
        up_pfe = [i.pfe_pct for i in up_intervals] if up_intervals else [0]
        down_pfe = [i.pfe_pct for i in down_intervals] if down_intervals else [0]
        
        max_up_pfe = np.max(up_pfe) if up_pfe else 0
        max_down_pfe = np.max(down_pfe) if down_pfe else 0
        
        categories = [self.labels['max_pfe_up'], self.labels['max_pfe_down']]
        max_pfes = [max_up_pfe, max_down_pfe]
        colors = ['green', 'red']
        
        bars = ax_capture.bar(categories, max_pfes, color=colors, alpha=0.7)
        ax_capture.set_title(self.labels['title_max_capture'])
        ax_capture.set_ylabel('PFE (%)')
        
        # 添加数值标签
        for bar, pfe in zip(bars, max_pfes):
            ax_capture.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                           f'{pfe:.2f}%', ha='center', va='bottom')
        
        # 5. 事件分析 (底部)
        ax_events = fig.add_subplot(gs[3, :])
        
        up_events = [e for e in events if e.event_type == 'up_turn']
        down_events = [e for e in events if e.event_type == 'down_turn']
        
        up_consistencies = [e.consistency for e in up_events] if up_events else [0]
        down_consistencies = [e.consistency for e in down_events] if down_events else [0]
        
        avg_up_consistency = np.mean(up_consistencies) if up_consistencies else 0
        avg_down_consistency = np.mean(down_consistencies) if down_consistencies else 0
        
        categories = [self.labels['consistency_up'], self.labels['consistency_down']]
        consistencies = [avg_up_consistency * 100, avg_down_consistency * 100]
        colors = ['green', 'red']
        
        bars = ax_events.bar(categories, consistencies, color=colors, alpha=0.7)
        ax_events.set_title(self.labels['title_event_consistency'])
        ax_events.set_ylabel(self.labels['consistency_pct'])
        ax_events.set_ylim(0, 100)
        ax_events.axhline(y=50, color='black', linestyle='--', alpha=0.5, label=self.labels['baseline_50'])
        
        # 添加数值标签
        for bar, cons in zip(bars, consistencies):
            ax_events.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                          f'{cons:.1f}%', ha='center', va='bottom')
        
        ax_events.legend()
        ax_events.grid(True, alpha=0.3)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"综合分析图已保存到: {save_path}")
        
        plt.show()
