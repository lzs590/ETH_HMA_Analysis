#!/usr/bin/env python3
"""
智能金融数据分析仪表板 V2.0
自动检测最新分析结果，无需手动创建CSV文件
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os
import glob
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# 页面配置
st.set_page_config(
    page_title="ETH HMA 智能分析仪表板",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .trend-up {
        color: #2ca02c;
        font-weight: bold;
    }
    .trend-down {
        color: #d62728;
        font-weight: bold;
    }
    .risk-high {
        background-color: #ffebee;
        border-left-color: #d62728;
    }
    .risk-low {
        background-color: #e8f5e8;
        border-left-color: #2ca02c;
    }
    .data-status {
        padding: 0.5rem;
        border-radius: 0.25rem;
        margin: 0.5rem 0;
    }
    .status-success {
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    .status-warning {
        background-color: #fff3cd;
        color: #856404;
        border: 1px solid #ffeaa7;
    }
    .status-error {
        background-color: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def find_latest_analysis():
    """自动查找最新的分析结果文件"""
    # 获取项目根目录
    current_dir = Path(__file__).parent
    project_root = current_dir.parent
    reports_dir = project_root / "assets" / "reports"
    
    # 查找所有4h分析结果
    json_files = list(reports_dir.glob("trend_analysis_4h_*.json"))
    
    # 调试信息
    print(f"🔍 搜索路径: {reports_dir}")
    print(f"📁 目录是否存在: {reports_dir.exists()}")
    if reports_dir.exists():
        all_files = list(reports_dir.glob("*"))
        print(f"📄 目录中的所有文件: {[f.name for f in all_files]}")
    
    if not json_files:
        return None, f"未找到4h分析结果文件 (搜索路径: {reports_dir})"
    
    # 选择最新的文件
    latest_file = max(json_files, key=lambda x: x.stat().st_mtime)
    
    try:
        with open(latest_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data, f"✅ 已加载最新分析结果: {latest_file.name}"
    except Exception as e:
        return None, f"❌ 加载分析结果失败: {str(e)}"

@st.cache_data
def convert_analysis_to_dataframe(analysis_data):
    """将JSON分析结果转换为DataFrame"""
    trends_data = []
    
    # 处理上涨趋势
    if 'uptrend_analysis' in analysis_data and 'intervals' in analysis_data['uptrend_analysis']:
        for interval in analysis_data['uptrend_analysis']['intervals']:
            trend_data = {
                'trend_id': f"UPTREND_{interval.get('interval_id', '')}",
                'trend_type': 'uptrend',
                'start_time': interval.get('start_time', ''),
                'end_time': interval.get('end_time', ''),
                'start_price': interval.get('start_price', 0),
                'end_price': interval.get('end_price', 0),
                'price_change': interval.get('price_change', 0),
                'price_change_pct': interval.get('price_change_pct', 0),
                'max_rally': interval.get('max_rally', 0),
                'max_decline': interval.get('max_decline', 0),
                'pfe': interval.get('pfe', 0),
                'mae': interval.get('mae', 0),
                'duration_4h': interval.get('duration_4h', 0),
                'duration_hours': interval.get('duration_hours', 0),
                'long_ideal_profit': interval.get('long_ideal_profit', 0),
                'long_actual_profit': interval.get('long_actual_profit', 0),
                'long_risk_loss': interval.get('long_risk_loss', 0),
                'risk_reward_ratio': interval.get('risk_reward_ratio', 0)
            }
            trends_data.append(trend_data)
    
    # 处理下跌趋势
    if 'downtrend_analysis' in analysis_data and 'intervals' in analysis_data['downtrend_analysis']:
        for interval in analysis_data['downtrend_analysis']['intervals']:
            trend_data = {
                'trend_id': f"DOWNTREND_{interval.get('interval_id', '')}",
                'trend_type': 'downtrend',
                'start_time': interval.get('start_time', ''),
                'end_time': interval.get('end_time', ''),
                'start_price': interval.get('start_price', 0),
                'end_price': interval.get('end_price', 0),
                'price_change': interval.get('price_change', 0),
                'price_change_pct': interval.get('price_change_pct', 0),
                'max_rally': interval.get('max_rally', 0),
                'max_decline': interval.get('max_decline', 0),
                'pfe': interval.get('pfe', 0),
                'mae': interval.get('mae', 0),
                'duration_4h': interval.get('duration_4h', 0),
                'duration_hours': interval.get('duration_hours', 0),
                'short_ideal_profit': interval.get('short_ideal_profit', 0),
                'short_actual_profit': interval.get('short_actual_profit', 0),
                'short_risk_loss': interval.get('short_risk_loss', 0),
                'risk_reward_ratio': interval.get('risk_reward_ratio', 0)
            }
            trends_data.append(trend_data)
    
    if not trends_data:
        return None
    
    # 创建DataFrame
    df = pd.DataFrame(trends_data)
    
    # 转换时间列
    df['start_time'] = pd.to_datetime(df['start_time'])
    df['end_time'] = pd.to_datetime(df['end_time'])
    
    # 按时间排序
    df = df.sort_values('start_time')
    
    return df

def create_metrics_row(df):
    """创建关键指标行"""
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="📈 总趋势数",
            value=f"{len(df):,}",
            delta=None
        )
    
    with col2:
        uptrends = len(df[df['trend_type'] == 'uptrend'])
        st.metric(
            label="📈 上涨趋势",
            value=f"{uptrends:,}",
            delta=f"{uptrends/len(df)*100:.1f}%"
        )
    
    with col3:
        downtrends = len(df[df['trend_type'] == 'downtrend'])
        st.metric(
            label="📉 下跌趋势", 
            value=f"{downtrends:,}",
            delta=f"{downtrends/len(df)*100:.1f}%"
        )
    
    with col4:
        # 计算高风险趋势（风险损失 > 理想收益）
        high_risk_count = 0
        for _, row in df.iterrows():
            if row['trend_type'] == 'uptrend':
                if row.get('long_risk_loss', 0) > row.get('long_ideal_profit', 0):
                    high_risk_count += 1
            elif row['trend_type'] == 'downtrend':
                if row.get('short_risk_loss', 0) > row.get('short_ideal_profit', 0):
                    high_risk_count += 1
        
        st.metric(
            label="⚠️ 高风险趋势",
            value=f"{high_risk_count:,}",
            delta=f"{high_risk_count/len(df)*100:.1f}%"
        )
    
    with col5:
        avg_duration = df['duration_hours'].mean()
        st.metric(
            label="⏱️ 平均持续时间",
            value=f"{avg_duration:.1f}h",
            delta=None
        )

def create_trend_distribution_chart(df):
    """创建趋势分布图表"""
    fig = px.pie(
        df, 
        names='trend_type',
        title="趋势类型分布",
        color_discrete_map={'uptrend': '#2ca02c', 'downtrend': '#d62728'}
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig

def create_performance_chart(df):
    """创建性能分析图表"""
    # 准备数据
    chart_data = []
    
    for _, row in df.iterrows():
        if row['trend_type'] == 'uptrend':
            ideal_profit = row.get('long_ideal_profit', 0)
            actual_profit = row.get('long_actual_profit', 0)
            risk_loss = row.get('long_risk_loss', 0)
        else:
            ideal_profit = row.get('short_ideal_profit', 0)
            actual_profit = row.get('short_actual_profit', 0)
            risk_loss = row.get('short_risk_loss', 0)
        
        chart_data.append({
            'trend_id': row['trend_id'],
            'trend_type': row['trend_type'],
            'start_time': row['start_time'],
            'ideal_profit': ideal_profit,
            'actual_profit': actual_profit,
            'risk_loss': risk_loss
        })
    
    chart_df = pd.DataFrame(chart_data)
    
    # 创建散点图
    fig = go.Figure()
    
    # 上涨趋势
    uptrend_data = chart_df[chart_df['trend_type'] == 'uptrend']
    if not uptrend_data.empty:
        fig.add_trace(go.Scatter(
            x=uptrend_data['start_time'],
            y=uptrend_data['ideal_profit'],
            mode='markers',
            name='上涨趋势-理想收益',
            marker=dict(color='green', size=8),
            hovertemplate='<b>%{text}</b><br>时间: %{x}<br>理想收益: %{y:.2f}%<extra></extra>',
            text=uptrend_data['trend_id']
        ))
    
    # 下跌趋势
    downtrend_data = chart_df[chart_df['trend_type'] == 'downtrend']
    if not downtrend_data.empty:
        fig.add_trace(go.Scatter(
            x=downtrend_data['start_time'],
            y=downtrend_data['ideal_profit'],
            mode='markers',
            name='下跌趋势-理想收益',
            marker=dict(color='red', size=8),
            hovertemplate='<b>%{text}</b><br>时间: %{x}<br>理想收益: %{y:.2f}%<extra></extra>',
            text=downtrend_data['trend_id']
        ))
    
    fig.update_layout(
        title="趋势收益分析",
        xaxis_title="时间",
        yaxis_title="收益百分比 (%)",
        hovermode='closest'
    )
    
    return fig

def create_risk_analysis_chart(df):
    """创建风险分析图表"""
    # 计算风险收益比
    risk_data = []
    
    for _, row in df.iterrows():
        if row['trend_type'] == 'uptrend':
            ideal_profit = row.get('long_ideal_profit', 0)
            risk_loss = row.get('long_risk_loss', 0)
        else:
            ideal_profit = row.get('short_ideal_profit', 0)
            risk_loss = row.get('short_risk_loss', 0)
        
        risk_ratio = risk_loss / ideal_profit if ideal_profit > 0 else 0
        
        risk_data.append({
            'trend_id': row['trend_id'],
            'trend_type': row['trend_type'],
            'start_time': row['start_time'],
            'risk_ratio': risk_ratio,
            'ideal_profit': ideal_profit,
            'risk_loss': risk_loss
        })
    
    risk_df = pd.DataFrame(risk_data)
    
    # 创建风险收益比分布图
    fig = px.histogram(
        risk_df,
        x='risk_ratio',
        color='trend_type',
        title="风险收益比分布",
        labels={'risk_ratio': '风险收益比', 'count': '频次'},
        color_discrete_map={'uptrend': '#2ca02c', 'downtrend': '#d62728'}
    )
    
    return fig

def main():
    """主函数"""
    # 页面标题
    st.markdown('<h1 class="main-header">📊 ETH HMA 智能分析仪表板</h1>', unsafe_allow_html=True)
    
    # 数据状态显示
    st.markdown("### 📊 数据状态")
    
    # 查找最新分析结果
    analysis_data, status_message = find_latest_analysis()
    
    if analysis_data is None:
        st.markdown(f'<div class="data-status status-error">{status_message}</div>', unsafe_allow_html=True)
        st.stop()
    else:
        st.markdown(f'<div class="data-status status-success">{status_message}</div>', unsafe_allow_html=True)
    
    # 转换数据
    df = convert_analysis_to_dataframe(analysis_data)
    
    if df is None or df.empty:
        st.error("❌ 无法转换分析数据")
        st.stop()
    
    # 显示数据概览
    st.markdown("### 📈 数据概览")
    create_metrics_row(df)
    
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
    
    # 应用筛选
    filtered_df = df[
        (df['start_time'].dt.date >= date_range[0]) &
        (df['start_time'].dt.date <= date_range[1]) &
        (df['trend_type'].isin(trend_types))
    ]
    
    if filtered_df.empty:
        st.warning("⚠️ 筛选后没有数据")
        st.stop()
    
    # 主要图表区域
    st.markdown("### 📊 趋势分析图表")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(create_trend_distribution_chart(filtered_df), use_container_width=True)
    
    with col2:
        st.plotly_chart(create_performance_chart(filtered_df), use_container_width=True)
    
    # 风险分析
    st.markdown("### ⚠️ 风险分析")
    st.plotly_chart(create_risk_analysis_chart(filtered_df), use_container_width=True)
    
    # 数据表格
    st.markdown("### 📋 详细数据")
    
    # 选择显示的列
    display_columns = [
        'trend_id', 'trend_type', 'start_time', 'end_time',
        'start_price', 'end_price', 'price_change_pct',
        'duration_hours', 'long_ideal_profit', 'long_actual_profit',
        'long_risk_loss', 'short_ideal_profit', 'short_actual_profit',
        'short_risk_loss', 'risk_reward_ratio'
    ]
    
    # 过滤存在的列
    available_columns = [col for col in display_columns if col in filtered_df.columns]
    
    st.dataframe(
        filtered_df[available_columns],
        use_container_width=True,
        height=400
    )
    
    # 数据统计
    st.markdown("### 📊 数据统计")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("筛选后趋势数", f"{len(filtered_df):,}")
    
    with col2:
        avg_profit = filtered_df['long_ideal_profit'].mean() if 'long_ideal_profit' in filtered_df.columns else 0
        st.metric("平均理想收益", f"{avg_profit:.2f}%")
    
    with col3:
        avg_risk = filtered_df['long_risk_loss'].mean() if 'long_risk_loss' in filtered_df.columns else 0
        st.metric("平均风险损失", f"{avg_risk:.2f}%")

if __name__ == "__main__":
    main()
