"""
趋势分析器 - 基于HMA斜率变化的趋势区间分析

实现完整的趋势分析框架：
1. HMA斜率计算和拐点识别
2. 事件研究 - 斜率改变时的价格行为
3. 区间研究 - 趋势区间的最大涨幅/跌幅捕获
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

logger = logging.getLogger(__name__)

@dataclass
class TrendInterval:
    """趋势区间数据类"""
    start_idx: int
    end_idx: int
    start_time: pd.Timestamp
    end_time: pd.Timestamp
    trend_direction: str  # 'up' or 'down'
    start_price: float
    end_price: float
    high_price: float
    low_price: float
    duration: int  # 周期数
    price_change: float  # 绝对价格变化
    price_change_pct: float  # 百分比变化
    pfe: float  # Potential Favorable Excursion (最大有利偏移)
    mae: float  # Maximum Adverse Excursion (最大不利偏移)
    pfe_pct: float  # PFE百分比
    mae_pct: float  # MAE百分比

@dataclass
class EventAnalysis:
    """事件分析结果"""
    event_type: str  # 'up_turn' or 'down_turn'
    event_time: pd.Timestamp
    price_at_event: float
    price_changes: List[float]  # 事件后N个周期的价格变化
    volatility: float  # 事件窗口内的波动率
    consistency: float  # 后续走势一致性

class TrendAnalyzer:
    """趋势分析器"""
    
    def __init__(self, hma_period: int = 45, slope_threshold: float = 0.001):
        """
        初始化趋势分析器
        
        Args:
            hma_period: HMA周期
            slope_threshold: 斜率阈值，用于过滤噪音
        """
        self.hma_period = hma_period
        self.slope_threshold = slope_threshold
        logger.info(f"趋势分析器初始化 - HMA周期: {hma_period}, 斜率阈值: {slope_threshold}")
    
    def calculate_hma_slope(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        计算HMA斜率并识别拐点
        
        Args:
            df: 包含HMA数据的DataFrame
            
        Returns:
            添加了斜率分析列的DataFrame
        """
        logger.info("开始计算HMA斜率分析")
        
        # 确保HMA列存在
        hma_col = f'HMA_{self.hma_period}'
        if hma_col not in df.columns:
            raise ValueError(f"HMA列 {hma_col} 不存在")
        
        # 计算HMA斜率（一阶差分）
        df['HMA_slope'] = df[hma_col].diff()
        
        # 计算斜率符号
        df['HMA_slope_sign'] = np.sign(df['HMA_slope'])
        
        # 识别斜率变化点
        df['slope_change'] = df['HMA_slope_sign'].diff().fillna(0)
        
        # 识别拐点（斜率符号改变）
        df['turning_point'] = 0
        df.loc[df['slope_change'] == 2.0, 'turning_point'] = 1  # 上拐点
        df.loc[df['slope_change'] == -2.0, 'turning_point'] = -1  # 下拐点
        
        # 过滤噪音：只保留斜率变化幅度足够大的拐点
        if self.slope_threshold > 0:
            slope_magnitude = df['HMA_slope'].abs()
            valid_turns = (df['turning_point'] != 0) & (slope_magnitude >= self.slope_threshold)
            df.loc[~valid_turns, 'turning_point'] = 0
        
        # 统计拐点数量
        up_turns = (df['turning_point'] == 1).sum()
        down_turns = (df['turning_point'] == -1).sum()
        
        logger.info(f"识别到 {up_turns} 个上拐点, {down_turns} 个下拐点")
        
        return df
    
    def analyze_events(self, df: pd.DataFrame, window_before: int = 5, window_after: int = 5) -> List[EventAnalysis]:
        """
        分析斜率改变事件的价格行为
        
        Args:
            df: 包含拐点数据的DataFrame
            window_before: 事件前分析窗口
            window_after: 事件后分析窗口
            
        Returns:
            事件分析结果列表
        """
        logger.info(f"开始事件分析 - 窗口: {window_before}前, {window_after}后")
        
        events = []
        turning_points = df[df['turning_point'] != 0].copy()
        
        for idx, row in turning_points.iterrows():
            event_type = 'up_turn' if row['turning_point'] == 1 else 'down_turn'
            
            # 获取数值索引
            numeric_idx = df.index.get_loc(idx)
            
            # 定义分析窗口
            start_idx = max(0, numeric_idx - window_before)
            end_idx = min(len(df), numeric_idx + window_after + 1)
            
            window_data = df.iloc[start_idx:end_idx].copy()
            
            # 计算价格变化
            price_at_event = row['close']
            price_changes = []
            
            for i in range(1, window_after + 1):
                if numeric_idx + i < len(df):
                    future_price = df.iloc[numeric_idx + i]['close']
                    change_pct = (future_price / price_at_event - 1) * 100
                    price_changes.append(change_pct)
            
            # 计算波动率
            returns = window_data['close'].pct_change().dropna()
            volatility = returns.std() * np.sqrt(252 * 24)  # 年化波动率
            
            # 计算一致性
            if event_type == 'up_turn':
                consistency = sum(1 for change in price_changes if change > 0) / len(price_changes) if price_changes else 0
            else:
                consistency = sum(1 for change in price_changes if change < 0) / len(price_changes) if price_changes else 0
            
            event = EventAnalysis(
                event_type=event_type,
                event_time=row.name,
                price_at_event=price_at_event,
                price_changes=price_changes,
                volatility=volatility,
                consistency=consistency
            )
            events.append(event)
        
        logger.info(f"完成事件分析 - 共分析 {len(events)} 个事件")
        return events
    
    def analyze_trend_intervals(self, df: pd.DataFrame) -> List[TrendInterval]:
        """
        分析趋势区间，计算最大涨幅/跌幅捕获
        
        Args:
            df: 包含拐点数据的DataFrame
            
        Returns:
            趋势区间分析结果列表
        """
        logger.info("开始趋势区间分析")
        
        # 获取所有拐点
        turning_points = df[df['turning_point'] != 0].copy()
        
        if len(turning_points) < 2:
            logger.warning("拐点数量不足，无法进行区间分析")
            return []
        
        intervals = []
        
        # 遍历连续的拐点对
        for i in range(len(turning_points) - 1):
            start_point = turning_points.iloc[i]
            end_point = turning_points.iloc[i + 1]
            
            start_time = start_point.name
            end_time = end_point.name
            
            # 获取数值索引
            start_idx = df.index.get_loc(start_time)
            end_idx = df.index.get_loc(end_time)
            
            # 确定趋势方向
            trend_direction = 'up' if start_point['turning_point'] == 1 else 'down'
            
            # 获取区间数据
            interval_data = df.iloc[start_idx:end_idx + 1]
            
            start_price = start_point['close']
            end_price = end_point['close']
            high_price = interval_data['high'].max()
            low_price = interval_data['low'].min()
            
            # 计算基本指标
            duration = end_idx - start_idx
            price_change = end_price - start_price
            price_change_pct = (end_price / start_price - 1) * 100
            
            # 计算PFE和MAE
            if trend_direction == 'up':
                pfe = (high_price / start_price - 1) * 100
                mae = (start_price / low_price - 1) * 100
            else:
                pfe = (start_price / low_price - 1) * 100
                mae = (high_price / start_price - 1) * 100
            
            interval = TrendInterval(
                start_idx=start_idx,
                end_idx=end_idx,
                start_time=start_time,
                end_time=end_time,
                trend_direction=trend_direction,
                start_price=start_price,
                end_price=end_price,
                high_price=high_price,
                low_price=low_price,
                duration=duration,
                price_change=price_change,
                price_change_pct=price_change_pct,
                pfe=pfe,
                mae=mae,
                pfe_pct=pfe,
                mae_pct=mae
            )
            intervals.append(interval)
        
        logger.info(f"完成趋势区间分析 - 共分析 {len(intervals)} 个区间")
        return intervals
    
    def generate_trend_report(self, intervals: List[TrendInterval], events: List[EventAnalysis]) -> Dict:
        """
        生成趋势分析报告
        
        Args:
            intervals: 趋势区间列表
            events: 事件分析列表
            
        Returns:
            分析报告字典
        """
        logger.info("生成趋势分析报告")
        
        if not intervals:
            return {"error": "没有可分析的区间数据"}
        
        # 分离上升和下降趋势
        up_intervals = [i for i in intervals if i.trend_direction == 'up']
        down_intervals = [i for i in intervals if i.trend_direction == 'down']
        
        # 分离上升和下降事件
        up_events = [e for e in events if e.event_type == 'up_turn']
        down_events = [e for e in events if e.event_type == 'down_turn']
        
        report = {
            "summary": {
                "total_intervals": len(intervals),
                "up_intervals": len(up_intervals),
                "down_intervals": len(down_intervals),
                "total_events": len(events),
                "up_events": len(up_events),
                "down_events": len(down_events)
            },
            "interval_analysis": {
                "up_trends": {
                    "count": len(up_intervals),
                    "avg_duration": np.mean([i.duration for i in up_intervals]) if up_intervals else 0,
                    "avg_price_change_pct": np.mean([i.price_change_pct for i in up_intervals]) if up_intervals else 0,
                    "max_price_change_pct": np.max([i.price_change_pct for i in up_intervals]) if up_intervals else 0,
                    "min_price_change_pct": np.min([i.price_change_pct for i in up_intervals]) if up_intervals else 0,
                    "avg_pfe_pct": np.mean([i.pfe_pct for i in up_intervals]) if up_intervals else 0,
                    "max_pfe_pct": np.max([i.pfe_pct for i in up_intervals]) if up_intervals else 0,
                    "avg_mae_pct": np.mean([i.mae_pct for i in up_intervals]) if up_intervals else 0,
                    "max_mae_pct": np.max([i.mae_pct for i in up_intervals]) if up_intervals else 0,
                    "win_rate": sum(1 for i in up_intervals if i.price_change_pct > 0) / len(up_intervals) if up_intervals else 0
                },
                "down_trends": {
                    "count": len(down_intervals),
                    "avg_duration": np.mean([i.duration for i in down_intervals]) if down_intervals else 0,
                    "avg_price_change_pct": np.mean([i.price_change_pct for i in down_intervals]) if down_intervals else 0,
                    "max_price_change_pct": np.max([i.price_change_pct for i in down_intervals]) if down_intervals else 0,
                    "min_price_change_pct": np.min([i.price_change_pct for i in down_intervals]) if down_intervals else 0,
                    "avg_pfe_pct": np.mean([i.pfe_pct for i in down_intervals]) if down_intervals else 0,
                    "max_pfe_pct": np.max([i.pfe_pct for i in down_intervals]) if down_intervals else 0,
                    "avg_mae_pct": np.mean([i.mae_pct for i in down_intervals]) if down_intervals else 0,
                    "max_mae_pct": np.max([i.mae_pct for i in down_intervals]) if down_intervals else 0,
                    "win_rate": sum(1 for i in down_intervals if i.price_change_pct < 0) / len(down_intervals) if down_intervals else 0
                }
            },
            "event_analysis": {
                "up_turns": {
                    "count": len(up_events),
                    "avg_volatility": np.mean([e.volatility for e in up_events]) if up_events else 0,
                    "avg_consistency": np.mean([e.consistency for e in up_events]) if up_events else 0,
                    "avg_price_change_1h": np.mean([e.price_changes[0] for e in up_events if len(e.price_changes) > 0]) if up_events else 0,
                    "avg_price_change_5h": np.mean([e.price_changes[4] for e in up_events if len(e.price_changes) > 4]) if up_events else 0
                },
                "down_turns": {
                    "count": len(down_events),
                    "avg_volatility": np.mean([e.volatility for e in down_events]) if down_events else 0,
                    "avg_consistency": np.mean([e.consistency for e in down_events]) if down_events else 0,
                    "avg_price_change_1h": np.mean([e.price_changes[0] for e in down_events if len(e.price_changes) > 0]) if down_events else 0,
                    "avg_price_change_5h": np.mean([e.price_changes[4] for e in down_events if len(e.price_changes) > 4]) if down_events else 0
                }
            }
        }
        
        # 计算盈亏比
        if up_intervals and down_intervals:
            avg_up_profit = np.mean([i.price_change_pct for i in up_intervals if i.price_change_pct > 0])
            avg_down_loss = abs(np.mean([i.price_change_pct for i in down_intervals if i.price_change_pct < 0]))
            report["interval_analysis"]["profit_loss_ratio"] = avg_up_profit / avg_down_loss if avg_down_loss > 0 else float('inf')
        
        logger.info("趋势分析报告生成完成")
        return report
