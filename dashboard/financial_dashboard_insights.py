#!/usr/bin/env python3
"""
深度数据分析Dashboard - 挖掘数据背后的隐藏信息
专注于数据洞察发现和深度分析
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import json
import os
import glob
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# 页面配置
st.set_page_config(
    page_title="ETH HMA 深度数据分析终端",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 专业级CSS样式
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .insight-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .critical-insight {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        border-left: 5px solid #ff4757;
    }
    .opportunity-insight {
        background: linear-gradient(135deg, #2ed573 0%, #1e90ff 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        border-left: 5px solid #2ed573;
    }
    .warning-insight {
        background: linear-gradient(135deg, #ffa502 0%, #ff6348 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        border-left: 5px solid #ffa502;
    }
    .metric-highlight {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_analysis_data():
    """加载分析数据"""
    current_dir = Path(__file__).parent
    project_root = current_dir.parent
    reports_dir = project_root / "assets" / "reports"
    
    json_files = list(reports_dir.glob("trend_analysis_4h_*.json"))
    
    if not json_files:
        return None, "未找到4h分析结果文件"
    
    latest_file = max(json_files, key=lambda x: x.stat().st_mtime)
    
    try:
        with open(latest_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data, f"✅ 已加载最新分析结果: {latest_file.name}"
    except Exception as e:
        return None, f"❌ 加载分析结果失败: {str(e)}"

@st.cache_data
def create_enhanced_dataframe(analysis_data):
    """创建增强版DataFrame，包含更多分析维度"""
    trends_data = []
    
    # 处理上涨趋势
    if 'uptrend_analysis' in analysis_data and 'intervals' in analysis_data['uptrend_analysis']:
        for interval in analysis_data['uptrend_analysis']['intervals']:
            start_price = interval.get('start_price', 0)
            end_price = interval.get('end_price', 0)
            high_price = interval.get('high_price', 0)
            low_price = interval.get('low_price', 0)
            
            # 基础计算
            price_change = end_price - start_price if start_price > 0 else 0
            price_change_pct = (price_change / start_price * 100) if start_price > 0 else 0
            volatility = ((high_price - low_price) / start_price * 100) if start_price > 0 else 0
            trend_strength = abs(price_change_pct)
            
            # 策略指标
            ideal_profit = interval.get('long_ideal_profit', 0)
            actual_profit = interval.get('long_actual_profit', 0)
            risk_loss = interval.get('long_risk_loss', 0)
            risk_reward_ratio = ideal_profit / risk_loss if risk_loss > 0 else 0
            
            # 时间指标
            duration_hours = interval.get('duration_hours', 0)
            start_time = pd.to_datetime(interval.get('start_time', ''))
            
            # 增强分析指标
            profit_efficiency = (actual_profit / ideal_profit * 100) if ideal_profit > 0 else 0
            risk_level = '低风险' if risk_reward_ratio > 2 else '中风险' if risk_reward_ratio > 1 else '高风险'
            trend_quality = '优质' if profit_efficiency > 50 and risk_reward_ratio > 1 else '一般' if profit_efficiency > 20 else '较差'
            
            # 市场环境分析
            hour_of_day = start_time.hour
            day_of_week = start_time.dayofweek
            market_session = '亚洲' if 0 <= hour_of_day < 8 else '欧洲' if 8 <= hour_of_day < 16 else '美洲'
            
            trend_data = {
                'trend_id': f"UPTREND_{interval.get('interval_id', '')}",
                'trend_type': 'uptrend',
                'start_time': start_time,
                'end_time': pd.to_datetime(interval.get('end_time', '')),
                'start_price': start_price,
                'end_price': end_price,
                'high_price': high_price,
                'low_price': low_price,
                'price_change': price_change,
                'price_change_pct': price_change_pct,
                'volatility': volatility,
                'trend_strength': trend_strength,
                'duration_hours': duration_hours,
                'duration_days': duration_hours / 24,
                'ideal_profit': ideal_profit,
                'actual_profit': actual_profit,
                'risk_loss': risk_loss,
                'risk_reward_ratio': risk_reward_ratio,
                'profit_efficiency': profit_efficiency,
                'risk_level': risk_level,
                'trend_quality': trend_quality,
                'market_session': market_session,
                'hour_of_day': hour_of_day,
                'day_of_week': day_of_week,
                'max_rally': interval.get('max_rally', 0),
                'max_decline': interval.get('max_decline', 0),
                'pfe': interval.get('pfe', 0),
                'mae': interval.get('mae', 0)
            }
            trends_data.append(trend_data)
    
    # 处理下跌趋势
    if 'downtrend_analysis' in analysis_data and 'intervals' in analysis_data['downtrend_analysis']:
        for interval in analysis_data['downtrend_analysis']['intervals']:
            start_price = interval.get('start_price', 0)
            end_price = interval.get('end_price', 0)
            high_price = interval.get('high_price', 0)
            low_price = interval.get('low_price', 0)
            
            # 基础计算
            price_change = end_price - start_price if start_price > 0 else 0
            price_change_pct = (price_change / start_price * 100) if start_price > 0 else 0
            volatility = ((high_price - low_price) / start_price * 100) if start_price > 0 else 0
            trend_strength = abs(price_change_pct)
            
            # 策略指标
            ideal_profit = interval.get('short_ideal_profit', 0)
            actual_profit = interval.get('short_actual_profit', 0)
            risk_loss = interval.get('short_risk_loss', 0)
            risk_reward_ratio = ideal_profit / risk_loss if risk_loss > 0 else 0
            
            # 时间指标
            duration_hours = interval.get('duration_hours', 0)
            start_time = pd.to_datetime(interval.get('start_time', ''))
            
            # 增强分析指标
            profit_efficiency = (actual_profit / ideal_profit * 100) if ideal_profit > 0 else 0
            risk_level = '低风险' if risk_reward_ratio > 2 else '中风险' if risk_reward_ratio > 1 else '高风险'
            trend_quality = '优质' if profit_efficiency > 50 and risk_reward_ratio > 1 else '一般' if profit_efficiency > 20 else '较差'
            
            # 市场环境分析
            hour_of_day = start_time.hour
            day_of_week = start_time.dayofweek
            market_session = '亚洲' if 0 <= hour_of_day < 8 else '欧洲' if 8 <= hour_of_day < 16 else '美洲'
            
            trend_data = {
                'trend_id': f"DOWNTREND_{interval.get('interval_id', '')}",
                'trend_type': 'downtrend',
                'start_time': start_time,
                'end_time': pd.to_datetime(interval.get('end_time', '')),
                'start_price': start_price,
                'end_price': end_price,
                'high_price': high_price,
                'low_price': low_price,
                'price_change': price_change,
                'price_change_pct': price_change_pct,
                'volatility': volatility,
                'trend_strength': trend_strength,
                'duration_hours': duration_hours,
                'duration_days': duration_hours / 24,
                'ideal_profit': ideal_profit,
                'actual_profit': actual_profit,
                'risk_loss': risk_loss,
                'risk_reward_ratio': risk_reward_ratio,
                'profit_efficiency': profit_efficiency,
                'risk_level': risk_level,
                'trend_quality': trend_quality,
                'market_session': market_session,
                'hour_of_day': hour_of_day,
                'day_of_week': day_of_week,
                'max_rally': interval.get('max_rally', 0),
                'max_decline': interval.get('max_decline', 0),
                'pfe': interval.get('pfe', 0),
                'mae': interval.get('mae', 0)
            }
            trends_data.append(trend_data)
    
    if not trends_data:
        return None
    
    df = pd.DataFrame(trends_data)
    df = df.sort_values('start_time')
    
    return df

def analyze_strategy_efficiency(df):
    """分析策略效率"""
    st.markdown("### 🎯 策略效率深度分析")
    
    # 计算效率指标
    total_trends = len(df)
    profitable_trends = len(df[df['actual_profit'] > 0])
    high_efficiency_trends = len(df[df['profit_efficiency'] > 50])
    low_risk_trends = len(df[df['risk_level'] == '低风险'])
    high_quality_trends = len(df[df['trend_quality'] == '优质'])
    
    # 效率分析表格
    efficiency_data = {
        '效率指标': [
            '总趋势数', '盈利趋势数', '高效率趋势数', '低风险趋势数', '优质趋势数',
            '盈利比例', '高效率比例', '低风险比例', '优质比例'
        ],
        '数值': [
            f"{total_trends}",
            f"{profitable_trends}",
            f"{high_efficiency_trends}",
            f"{low_risk_trends}",
            f"{high_quality_trends}",
            f"{profitable_trends/total_trends*100:.1f}%",
            f"{high_efficiency_trends/total_trends*100:.1f}%",
            f"{low_risk_trends/total_trends*100:.1f}%",
            f"{high_quality_trends/total_trends*100:.1f}%"
        ]
    }
    
    efficiency_df = pd.DataFrame(efficiency_data)
    st.dataframe(efficiency_df, use_container_width=True)
    
    # 效率洞察
    st.markdown("#### 🔍 效率洞察")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("策略胜率", f"{profitable_trends/total_trends*100:.1f}%", 
                 delta="盈利趋势比例")
    with col2:
        st.metric("执行效率", f"{high_efficiency_trends/total_trends*100:.1f}%", 
                 delta="高效率趋势比例")
    with col3:
        st.metric("风险控制", f"{low_risk_trends/total_trends*100:.1f}%", 
                 delta="低风险趋势比例")
    with col4:
        st.metric("趋势质量", f"{high_quality_trends/total_trends*100:.1f}%", 
                 delta="优质趋势比例")

def analyze_market_patterns(df):
    """分析市场模式"""
    st.markdown("### 📊 市场模式深度分析")
    
    # 按市场时段分析
    session_analysis = df.groupby('market_session').agg({
        'ideal_profit': ['mean', 'std', 'count'],
        'actual_profit': ['mean', 'std'],
        'risk_reward_ratio': ['mean', 'std'],
        'profit_efficiency': ['mean', 'std']
    }).round(2)
    
    st.markdown("#### 🌍 市场时段表现分析")
    st.dataframe(session_analysis, use_container_width=True)
    
    # 按小时分析
    hourly_analysis = df.groupby('hour_of_day').agg({
        'ideal_profit': 'mean',
        'actual_profit': 'mean',
        'risk_reward_ratio': 'mean',
        'profit_efficiency': 'mean'
    }).round(2)
    
    st.markdown("#### ⏰ 小时级别表现分析")
    st.dataframe(hourly_analysis, use_container_width=True)
    
    # 按星期分析
    weekly_analysis = df.groupby('day_of_week').agg({
        'ideal_profit': 'mean',
        'actual_profit': 'mean',
        'risk_reward_ratio': 'mean',
        'profit_efficiency': 'mean'
    }).round(2)
    
    st.markdown("#### 📅 星期级别表现分析")
    st.dataframe(weekly_analysis, use_container_width=True)

def analyze_risk_patterns(df):
    """分析风险模式"""
    st.markdown("### ⚠️ 风险模式深度分析")
    
    # 风险等级分析
    risk_analysis = df.groupby('risk_level').agg({
        'ideal_profit': ['mean', 'std', 'count'],
        'actual_profit': ['mean', 'std'],
        'profit_efficiency': ['mean', 'std'],
        'duration_hours': ['mean', 'std']
    }).round(2)
    
    st.markdown("#### 🎯 风险等级表现分析")
    st.dataframe(risk_analysis, use_container_width=True)
    
    # 风险收益比分析
    risk_reward_analysis = df.groupby(pd.cut(df['risk_reward_ratio'], 
                                            bins=[0, 0.5, 1, 2, float('inf')], 
                                            labels=['极高风险', '高风险', '中风险', '低风险'])).agg({
        'ideal_profit': 'mean',
        'actual_profit': 'mean',
        'profit_efficiency': 'mean',
        'duration_hours': 'mean'
    }).round(2)
    
    st.markdown("#### 📈 风险收益比表现分析")
    st.dataframe(risk_reward_analysis, use_container_width=True)

def analyze_trend_characteristics(df):
    """分析趋势特征"""
    st.markdown("### 📈 趋势特征深度分析")
    
    # 趋势质量分析
    quality_analysis = df.groupby('trend_quality').agg({
        'ideal_profit': ['mean', 'std', 'count'],
        'actual_profit': ['mean', 'std'],
        'risk_reward_ratio': ['mean', 'std'],
        'duration_hours': ['mean', 'std'],
        'volatility': ['mean', 'std']
    }).round(2)
    
    st.markdown("#### 🏆 趋势质量表现分析")
    st.dataframe(quality_analysis, use_container_width=True)
    
    # 趋势强度分析
    strength_analysis = df.groupby(pd.cut(df['trend_strength'], 
                                        bins=[0, 1, 3, 5, float('inf')], 
                                        labels=['弱趋势', '中趋势', '强趋势', '极强趋势'])).agg({
        'ideal_profit': 'mean',
        'actual_profit': 'mean',
        'profit_efficiency': 'mean',
        'risk_reward_ratio': 'mean',
        'duration_hours': 'mean'
    }).round(2)
    
    st.markdown("#### 💪 趋势强度表现分析")
    st.dataframe(strength_analysis, use_container_width=True)

def generate_insights(df):
    """生成深度洞察"""
    st.markdown("### 🔍 深度数据洞察")
    
    # 关键洞察
    insights = []
    
    # 1. 策略效率洞察
    avg_efficiency = df['profit_efficiency'].mean()
    if avg_efficiency < 30:
        insights.append({
            'type': 'critical',
            'title': '🚨 策略执行效率严重不足',
            'content': f'平均执行效率仅为{avg_efficiency:.1f}%，远低于理想水平。建议优化交易执行策略，提高信号捕捉能力。'
        })
    elif avg_efficiency < 50:
        insights.append({
            'type': 'warning',
            'title': '⚠️ 策略执行效率有待提升',
            'content': f'平均执行效率为{avg_efficiency:.1f}%，仍有较大提升空间。建议分析执行瓶颈，优化交易时机。'
        })
    else:
        insights.append({
            'type': 'opportunity',
            'title': '✅ 策略执行效率良好',
            'content': f'平均执行效率为{avg_efficiency:.1f}%，表现良好。可考虑适当增加仓位或优化风险控制。'
        })
    
    # 2. 风险控制洞察
    high_risk_ratio = len(df[df['risk_level'] == '高风险']) / len(df) * 100
    if high_risk_ratio > 40:
        insights.append({
            'type': 'critical',
            'title': '🚨 高风险趋势比例过高',
            'content': f'高风险趋势占比{high_risk_ratio:.1f}%，存在较大风险。建议加强风险控制，优化入场条件。'
        })
    elif high_risk_ratio > 25:
        insights.append({
            'type': 'warning',
            'title': '⚠️ 风险控制需要关注',
            'content': f'高风险趋势占比{high_risk_ratio:.1f}%，需要加强风险控制。建议优化止损策略。'
        })
    else:
        insights.append({
            'type': 'opportunity',
            'title': '✅ 风险控制良好',
            'content': f'高风险趋势占比{high_risk_ratio:.1f}%，风险控制良好。可考虑适当提高仓位。'
        })
    
    # 3. 市场时段洞察
    best_session = df.groupby('market_session')['profit_efficiency'].mean().idxmax()
    best_session_efficiency = df.groupby('market_session')['profit_efficiency'].mean().max()
    insights.append({
        'type': 'insight',
        'title': '🌍 最佳交易时段发现',
        'content': f'{best_session}时段表现最佳，平均执行效率为{best_session_efficiency:.1f}%。建议重点关注该时段的交易机会。'
    })
    
    # 4. 趋势质量洞察
    quality_ratio = len(df[df['trend_quality'] == '优质']) / len(df) * 100
    if quality_ratio < 20:
        insights.append({
            'type': 'warning',
            'title': '⚠️ 优质趋势比例偏低',
            'content': f'优质趋势占比{quality_ratio:.1f}%，建议优化趋势识别算法，提高信号质量。'
        })
    else:
        insights.append({
            'type': 'opportunity',
            'title': '✅ 趋势质量良好',
            'content': f'优质趋势占比{quality_ratio:.1f}%，趋势识别效果良好。可考虑增加交易频率。'
        })
    
    # 5. 时间模式洞察
    best_hour = df.groupby('hour_of_day')['profit_efficiency'].mean().idxmax()
    best_hour_efficiency = df.groupby('hour_of_day')['profit_efficiency'].mean().max()
    insights.append({
        'type': 'insight',
        'title': '⏰ 最佳交易时间发现',
        'content': f'{best_hour}点表现最佳，平均执行效率为{best_hour_efficiency:.1f}%。建议在该时间段重点关注交易机会。'
    })
    
    # 显示洞察
    for insight in insights:
        if insight['type'] == 'critical':
            st.markdown(f'<div class="critical-insight"><h4>{insight["title"]}</h4><p>{insight["content"]}</p></div>', unsafe_allow_html=True)
        elif insight['type'] == 'warning':
            st.markdown(f'<div class="warning-insight"><h4>{insight["title"]}</h4><p>{insight["content"]}</p></div>', unsafe_allow_html=True)
        elif insight['type'] == 'opportunity':
            st.markdown(f'<div class="opportunity-insight"><h4>{insight["title"]}</h4><p>{insight["content"]}</p></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="insight-card"><h4>{insight["title"]}</h4><p>{insight["content"]}</p></div>', unsafe_allow_html=True)

def create_advanced_charts(df):
    """创建高级分析图表"""
    st.markdown("### 📊 高级分析图表")
    
    # 1. 策略效率分布图
    fig1 = px.histogram(df, x='profit_efficiency', color='trend_type', 
                       title='策略执行效率分布',
                       labels={'profit_efficiency': '执行效率 (%)', 'count': '频次'})
    st.plotly_chart(fig1, use_container_width=True)
    
    # 2. 风险收益关系图
    fig2 = px.scatter(df, x='risk_loss', y='ideal_profit', 
                      color='risk_level', size='profit_efficiency',
                      title='风险收益关系分析',
                      labels={'risk_loss': '风险损失 (%)', 'ideal_profit': '理想收益 (%)'})
    st.plotly_chart(fig2, use_container_width=True)
    
    # 3. 市场时段表现图
    session_performance = df.groupby('market_session').agg({
        'profit_efficiency': 'mean',
        'risk_reward_ratio': 'mean',
        'ideal_profit': 'mean'
    }).reset_index()
    
    fig3 = px.bar(session_performance, x='market_session', y='profit_efficiency',
                  title='市场时段表现分析',
                  labels={'market_session': '市场时段', 'profit_efficiency': '平均执行效率 (%)'})
    st.plotly_chart(fig3, use_container_width=True)
    
    # 4. 时间模式分析图
    hourly_performance = df.groupby('hour_of_day').agg({
        'profit_efficiency': 'mean',
        'risk_reward_ratio': 'mean'
    }).reset_index()
    
    fig4 = px.line(hourly_performance, x='hour_of_day', y='profit_efficiency',
                   title='小时级别表现分析',
                   labels={'hour_of_day': '小时', 'profit_efficiency': '平均执行效率 (%)'})
    st.plotly_chart(fig4, use_container_width=True)

def main():
    """主函数"""
    # 页面标题
    st.markdown('<h1 class="main-header">🔍 ETH HMA 深度数据分析终端</h1>', unsafe_allow_html=True)
    
    # 数据状态显示
    st.markdown('<div class="insight-card">🔍 正在加载最新分析数据...</div>', unsafe_allow_html=True)
    
    # 加载数据
    analysis_data, status_message = load_analysis_data()
    
    if analysis_data is None:
        st.error(f"❌ {status_message}")
        st.stop()
    else:
        st.success(f"✅ {status_message}")
    
    # 转换数据
    df = create_enhanced_dataframe(analysis_data)
    
    if df is None or df.empty:
        st.error("❌ 无法转换分析数据")
        st.stop()
    
    # 侧边栏筛选器
    st.sidebar.markdown("### 🔍 数据筛选")
    
    # 时间范围筛选
    min_date = df['start_time'].min().date()
    max_date = df['start_time'].max().date()
    
    date_range = st.sidebar.date_input(
        "📅 时间范围",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # 趋势类型筛选
    trend_types = st.sidebar.multiselect(
        "📊 趋势类型",
        options=['uptrend', 'downtrend'],
        default=['uptrend', 'downtrend']
    )
    
    # 风险等级筛选
    risk_levels = st.sidebar.multiselect(
        "⚠️ 风险等级",
        options=['低风险', '中风险', '高风险'],
        default=['低风险', '中风险', '高风险']
    )
    
    # 趋势质量筛选
    quality_levels = st.sidebar.multiselect(
        "🏆 趋势质量",
        options=['优质', '一般', '较差'],
        default=['优质', '一般', '较差']
    )
    
    # 市场时段筛选
    market_sessions = st.sidebar.multiselect(
        "🌍 市场时段",
        options=['亚洲', '欧洲', '美洲'],
        default=['亚洲', '欧洲', '美洲']
    )
    
    # 应用筛选
    filtered_df = df[
        (df['start_time'].dt.date >= date_range[0]) &
        (df['start_time'].dt.date <= date_range[1]) &
        (df['trend_type'].isin(trend_types)) &
        (df['risk_level'].isin(risk_levels)) &
        (df['trend_quality'].isin(quality_levels)) &
        (df['market_session'].isin(market_sessions))
    ]
    
    if filtered_df.empty:
        st.warning("⚠️ 筛选后没有数据")
        st.stop()
    
    # 主要分析内容
    st.markdown("### 📊 深度数据分析")
    
    # 策略效率分析
    analyze_strategy_efficiency(filtered_df)
    
    # 市场模式分析
    analyze_market_patterns(filtered_df)
    
    # 风险模式分析
    analyze_risk_patterns(filtered_df)
    
    # 趋势特征分析
    analyze_trend_characteristics(filtered_df)
    
    # 生成洞察
    generate_insights(filtered_df)
    
    # 高级图表
    create_advanced_charts(filtered_df)

if __name__ == "__main__":
    main()
