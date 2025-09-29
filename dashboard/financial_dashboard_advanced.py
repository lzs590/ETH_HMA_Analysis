#!/usr/bin/env python3
"""
高级专业金融分析Dashboard
包含原始数据展示、交互图表、置信指数算法等专业功能
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
    page_title="ETH HMA 高级专业分析终端",
    page_icon="📊",
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
    .confidence-high {
        background: linear-gradient(135deg, #2ed573 0%, #1e90ff 100%);
        color: white;
        padding: 0.5rem;
        border-radius: 0.25rem;
        text-align: center;
        font-weight: bold;
    }
    .confidence-medium {
        background: linear-gradient(135deg, #ffa502 0%, #ff6348 100%);
        color: white;
        padding: 0.5rem;
        border-radius: 0.25rem;
        text-align: center;
        font-weight: bold;
    }
    .confidence-low {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        color: white;
        padding: 0.5rem;
        border-radius: 0.25rem;
        text-align: center;
        font-weight: bold;
    }
    .metric-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .data-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
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
    """创建增强版DataFrame，包含置信指数计算"""
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
            
            # 置信指数计算
            confidence_score = calculate_confidence_index(
                ideal_profit, actual_profit, risk_reward_ratio, 
                trend_strength, volatility, duration_hours
            )
            
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
                'confidence_score': confidence_score,
                'confidence_level': get_confidence_level(confidence_score),
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
            
            # 置信指数计算
            confidence_score = calculate_confidence_index(
                ideal_profit, actual_profit, risk_reward_ratio, 
                trend_strength, volatility, duration_hours
            )
            
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
                'confidence_score': confidence_score,
                'confidence_level': get_confidence_level(confidence_score),
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

def calculate_confidence_index(ideal_profit, actual_profit, risk_reward_ratio, 
                              trend_strength, volatility, duration_hours):
    """
    计算趋势置信指数
    基于多个维度的综合评估
    """
    # 1. 收益效率因子 (0-30分)
    profit_efficiency = (actual_profit / ideal_profit * 100) if ideal_profit > 0 else 0
    profit_score = min(30, profit_efficiency * 0.3)
    
    # 2. 风险收益比因子 (0-25分)
    risk_score = min(25, risk_reward_ratio * 12.5) if risk_reward_ratio > 0 else 0
    
    # 3. 趋势强度因子 (0-20分)
    strength_score = min(20, trend_strength * 2)
    
    # 4. 波动率因子 (0-15分) - 适中波动率得分更高
    optimal_volatility = 5.0  # 理想波动率
    volatility_diff = abs(volatility - optimal_volatility)
    volatility_score = max(0, 15 - volatility_diff * 1.5)
    
    # 5. 持续时间因子 (0-10分) - 适中持续时间得分更高
    optimal_duration = 72  # 理想持续时间(小时)
    duration_diff = abs(duration_hours - optimal_duration)
    duration_score = max(0, 10 - duration_diff * 0.1)
    
    # 综合置信指数
    confidence_score = profit_score + risk_score + strength_score + volatility_score + duration_score
    
    return round(confidence_score, 2)

def get_confidence_level(confidence_score):
    """根据置信指数确定置信等级"""
    if confidence_score >= 80:
        return "高置信"
    elif confidence_score >= 60:
        return "中置信"
    else:
        return "低置信"

def create_interactive_data_table(df):
    """创建交互式数据表格"""
    st.markdown("### 📊 原始数据展示区域")
    
    # 数据概览
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("总趋势数", f"{len(df):,}")
    with col2:
        st.metric("平均置信指数", f"{df['confidence_score'].mean():.2f}")
    with col3:
        st.metric("高置信趋势", f"{len(df[df['confidence_level'] == '高置信']):,}")
    with col4:
        st.metric("平均收益", f"{df['actual_profit'].mean():.2f}%")
    
    # 高级筛选器
    st.markdown("#### 🔍 高级筛选器")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # 时间范围筛选
        min_date = df['start_time'].min().date()
        max_date = df['start_time'].max().date()
        date_range = st.date_input(
            "📅 时间范围",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
    
    with col2:
        # 趋势类型筛选
        trend_types = st.multiselect(
            "📊 趋势类型",
            options=['uptrend', 'downtrend'],
            default=['uptrend', 'downtrend']
        )
    
    with col3:
        # 置信等级筛选
        confidence_levels = st.multiselect(
            "🎯 置信等级",
            options=['高置信', '中置信', '低置信'],
            default=['高置信', '中置信', '低置信']
        )
    
    with col4:
        # 收益范围筛选
        profit_range = st.slider(
            "💰 收益范围 (%)",
            min_value=float(df['actual_profit'].min()),
            max_value=float(df['actual_profit'].max()),
            value=(float(df['actual_profit'].min()), float(df['actual_profit'].max()))
        )
    
    # 应用筛选
    filtered_df = df[
        (df['start_time'].dt.date >= date_range[0]) &
        (df['start_time'].dt.date <= date_range[1]) &
        (df['trend_type'].isin(trend_types)) &
        (df['confidence_level'].isin(confidence_levels)) &
        (df['actual_profit'] >= profit_range[0]) &
        (df['actual_profit'] <= profit_range[1])
    ]
    
    # 排序选项
    st.markdown("#### 📈 排序选项")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        sort_by = st.selectbox(
            "排序字段",
            options=['confidence_score', 'actual_profit', 'ideal_profit', 'risk_reward_ratio', 'start_time'],
            index=0
        )
    
    with col2:
        sort_order = st.selectbox(
            "排序顺序",
            options=['降序', '升序'],
            index=0
        )
    
    with col3:
        if st.button("🔄 应用排序"):
            ascending = sort_order == '升序'
            filtered_df = filtered_df.sort_values(sort_by, ascending=ascending)
    
    # 显示筛选后的数据
    st.markdown(f"#### 📋 筛选结果 ({len(filtered_df)} 条记录)")
    
    # 选择显示的列
    display_columns = [
        'trend_id', 'trend_type', 'start_time', 'end_time',
        'start_price', 'end_price', 'price_change_pct', 'volatility',
        'trend_strength', 'duration_hours', 'ideal_profit', 'actual_profit',
        'risk_loss', 'risk_reward_ratio', 'confidence_score', 'confidence_level'
    ]
    
    # 交互式数据表格
    st.dataframe(
        filtered_df[display_columns],
        use_container_width=True,
        height=400
    )
    
    return filtered_df

def create_interactive_charts(df):
    """创建交互式图表"""
    st.markdown("### 📊 交互式图表分析")
    
    # 1. 置信指数分布图
    fig1 = px.histogram(df, x='confidence_score', color='trend_type',
                       title='趋势置信指数分布',
                       labels={'confidence_score': '置信指数', 'count': '频次'},
                       nbins=20)
    fig1.update_layout(height=400)
    st.plotly_chart(fig1, use_container_width=True)
    
    # 2. 风险收益关系图
    # 确保size值为正数
    df_plot = df.copy()
    df_plot['size_normalized'] = df_plot['confidence_score'].abs() + 1  # 加1确保最小值为1
    
    fig2 = px.scatter(df_plot, x='risk_loss', y='ideal_profit', 
                      color='confidence_level', size='size_normalized',
                      title='风险收益关系分析',
                      labels={'risk_loss': '风险损失 (%)', 'ideal_profit': '理想收益 (%)'},
                      hover_data=['trend_id', 'actual_profit', 'risk_reward_ratio', 'confidence_score'])
    fig2.update_layout(height=400)
    st.plotly_chart(fig2, use_container_width=True)
    
    # 3. 时间序列分析图
    fig3 = make_subplots(
        rows=2, cols=1,
        subplot_titles=('置信指数时间序列', '收益时间序列'),
        vertical_spacing=0.1
    )
    
    # 置信指数时间序列
    fig3.add_trace(
        go.Scatter(x=df['start_time'], y=df['confidence_score'],
                  mode='lines+markers', name='置信指数',
                  line=dict(color='blue', width=2)),
        row=1, col=1
    )
    
    # 收益时间序列
    fig3.add_trace(
        go.Scatter(x=df['start_time'], y=df['actual_profit'],
                  mode='lines+markers', name='实际收益',
                  line=dict(color='green', width=2)),
        row=2, col=1
    )
    
    fig3.update_layout(height=600, title_text="时间序列分析")
    st.plotly_chart(fig3, use_container_width=True)
    
    # 4. 置信指数vs收益散点图
    fig4 = px.scatter(df, x='confidence_score', y='actual_profit',
                     color='trend_type', size='risk_reward_ratio',
                     title='置信指数vs实际收益',
                     labels={'confidence_score': '置信指数', 'actual_profit': '实际收益 (%)'},
                     hover_data=['trend_id', 'ideal_profit', 'risk_reward_ratio'])
    fig4.update_layout(height=400)
    st.plotly_chart(fig4, use_container_width=True)
    
    # 5. 置信等级分布饼图
    confidence_counts = df['confidence_level'].value_counts()
    fig5 = px.pie(values=confidence_counts.values, names=confidence_counts.index,
                  title='置信等级分布',
                  color_discrete_map={'高置信': '#2ed573', '中置信': '#ffa502', '低置信': '#ff6b6b'})
    fig5.update_layout(height=400)
    st.plotly_chart(fig5, use_container_width=True)

def create_confidence_analysis(df):
    """创建置信指数分析"""
    st.markdown("### 🎯 置信指数深度分析")
    
    # 置信指数统计
    confidence_stats = df.groupby('confidence_level').agg({
        'confidence_score': ['mean', 'std', 'count'],
        'actual_profit': ['mean', 'std'],
        'ideal_profit': ['mean', 'std'],
        'risk_reward_ratio': ['mean', 'std'],
        'duration_hours': ['mean', 'std']
    }).round(2)
    
    st.markdown("#### 📊 置信等级统计表")
    st.dataframe(confidence_stats, use_container_width=True)
    
    # 置信指数分析图表
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('置信指数分布', '置信指数vs收益', '置信指数vs风险收益比', '置信指数vs持续时间'),
        specs=[[{"type": "histogram"}, {"type": "scatter"}],
               [{"type": "scatter"}, {"type": "scatter"}]]
    )
    
    # 置信指数分布
    fig.add_trace(
        go.Histogram(x=df['confidence_score'], name='置信指数分布'),
        row=1, col=1
    )
    
    # 置信指数vs收益
    fig.add_trace(
        go.Scatter(x=df['confidence_score'], y=df['actual_profit'],
                  mode='markers', name='置信指数vs收益',
                  marker=dict(color=df['confidence_score'], colorscale='Viridis')),
        row=1, col=2
    )
    
    # 置信指数vs风险收益比
    fig.add_trace(
        go.Scatter(x=df['confidence_score'], y=df['risk_reward_ratio'],
                  mode='markers', name='置信指数vs风险收益比',
                  marker=dict(color=df['confidence_score'], colorscale='Plasma')),
        row=2, col=1
    )
    
    # 置信指数vs持续时间
    fig.add_trace(
        go.Scatter(x=df['confidence_score'], y=df['duration_hours'],
                  mode='markers', name='置信指数vs持续时间',
                  marker=dict(color=df['confidence_score'], colorscale='Inferno')),
        row=2, col=2
    )
    
    fig.update_layout(height=800, title_text="置信指数综合分析")
    st.plotly_chart(fig, use_container_width=True)
    
    # 置信指数洞察
    st.markdown("#### 🔍 置信指数洞察")
    
    high_confidence_count = len(df[df['confidence_level'] == '高置信'])
    high_confidence_ratio = high_confidence_count / len(df) * 100
    avg_confidence = df['confidence_score'].mean()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("高置信趋势数", f"{high_confidence_count}", delta=f"{high_confidence_ratio:.1f}%")
    with col2:
        st.metric("平均置信指数", f"{avg_confidence:.2f}")
    with col3:
        st.metric("置信指数标准差", f"{df['confidence_score'].std():.2f}")

def create_performance_metrics(df):
    """创建表现指标分析"""
    st.markdown("### 📈 表现指标分析")
    
    # 关键指标计算
    total_trends = len(df)
    profitable_trends = len(df[df['actual_profit'] > 0])
    high_confidence_trends = len(df[df['confidence_level'] == '高置信'])
    
    avg_confidence = df['confidence_score'].mean()
    avg_profit = df['actual_profit'].mean()
    avg_risk_reward = df['risk_reward_ratio'].mean()
    
    # 表现指标表格
    performance_data = {
        '指标': [
            '总趋势数', '盈利趋势数', '高置信趋势数', '平均置信指数',
            '平均实际收益', '平均风险收益比', '盈利比例', '高置信比例'
        ],
        '数值': [
            f"{total_trends}",
            f"{profitable_trends}",
            f"{high_confidence_trends}",
            f"{avg_confidence:.2f}",
            f"{avg_profit:.2f}%",
            f"{avg_risk_reward:.2f}",
            f"{profitable_trends/total_trends*100:.1f}%",
            f"{high_confidence_trends/total_trends*100:.1f}%"
        ]
    }
    
    performance_df = pd.DataFrame(performance_data)
    st.dataframe(performance_df, use_container_width=True)
    
    # 表现指标图表
    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=('收益分布', '置信指数分布', '风险收益比分布')
    )
    
    # 收益分布
    fig.add_trace(
        go.Histogram(x=df['actual_profit'], name='收益分布'),
        row=1, col=1
    )
    
    # 置信指数分布
    fig.add_trace(
        go.Histogram(x=df['confidence_score'], name='置信指数分布'),
        row=1, col=2
    )
    
    # 风险收益比分布
    fig.add_trace(
        go.Histogram(x=df['risk_reward_ratio'], name='风险收益比分布'),
        row=1, col=3
    )
    
    fig.update_layout(height=400, title_text="表现指标分布分析")
    st.plotly_chart(fig, use_container_width=True)

def main():
    """主函数"""
    # 页面标题
    st.markdown('<h1 class="main-header">📊 ETH HMA 高级专业分析终端</h1>', unsafe_allow_html=True)
    
    # 数据状态显示
    st.markdown('<div class="data-section">🔍 正在加载最新分析数据...</div>', unsafe_allow_html=True)
    
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
    
    # 主要功能区域
    tab1, tab2, tab3, tab4 = st.tabs(["📊 原始数据", "📈 交互图表", "🎯 置信分析", "📈 表现指标"])
    
    with tab1:
        filtered_df = create_interactive_data_table(df)
    
    with tab2:
        create_interactive_charts(df)
    
    with tab3:
        create_confidence_analysis(df)
    
    with tab4:
        create_performance_metrics(df)
    
    # 侧边栏补充信息
    st.sidebar.markdown("### 📊 数据概览")
    st.sidebar.metric("总趋势数", f"{len(df):,}")
    st.sidebar.metric("平均置信指数", f"{df['confidence_score'].mean():.2f}")
    st.sidebar.metric("高置信趋势", f"{len(df[df['confidence_level'] == '高置信']):,}")
    st.sidebar.metric("平均收益", f"{df['actual_profit'].mean():.2f}%")
    
    st.sidebar.markdown("### 🎯 置信指数算法")
    st.sidebar.markdown("""
    **置信指数计算公式：**
    
    1. **收益效率因子** (0-30分)
    - 实际收益/理想收益 × 30
    
    2. **风险收益比因子** (0-25分)
    - 风险收益比 × 12.5
    
    3. **趋势强度因子** (0-20分)
    - 趋势强度 × 2
    
    4. **波动率因子** (0-15分)
    - 15 - |波动率 - 5| × 1.5
    
    5. **持续时间因子** (0-10分)
    - 10 - |持续时间 - 72| × 0.1
    
    **置信等级：**
    - 高置信：≥80分
    - 中置信：60-79分
    - 低置信：<60分
    """)

if __name__ == "__main__":
    main()
