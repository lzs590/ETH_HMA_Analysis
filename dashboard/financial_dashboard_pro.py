#!/usr/bin/env python3
"""
华尔街级别专业金融分析仪表板
深度挖掘数据背后的隐藏事实
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
    page_title="ETH HMA 专业分析终端",
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
    .terminal-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        font-family: 'Courier New', monospace;
    }
    .metric-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .risk-high {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        color: white;
    }
    .risk-medium {
        background: linear-gradient(135deg, #feca57 0%, #ff9ff3 100%);
        color: white;
    }
    .risk-low {
        background: linear-gradient(135deg, #48dbfb 0%, #0abde3 100%);
        color: white;
    }
    .profit-high {
        background: linear-gradient(135deg, #00d2ff 0%, #3a7bd5 100%);
        color: white;
    }
    .data-insight {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_analysis_data():
    """加载分析数据"""
    # 获取项目根目录
    current_dir = Path(__file__).parent
    project_root = current_dir.parent
    reports_dir = project_root / "assets" / "reports"
    
    # 查找所有4h分析结果
    json_files = list(reports_dir.glob("trend_analysis_4h_*.json"))
    
    if not json_files:
        return None, "未找到4h分析结果文件"
    
    # 选择最新的文件
    latest_file = max(json_files, key=lambda x: x.stat().st_mtime)
    
    try:
        with open(latest_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data, f"✅ 已加载最新分析结果: {latest_file.name}"
    except Exception as e:
        return None, f"❌ 加载分析结果失败: {str(e)}"

@st.cache_data
def create_professional_dataframe(analysis_data):
    """创建专业级DataFrame"""
    trends_data = []
    
    # 处理上涨趋势
    if 'uptrend_analysis' in analysis_data and 'intervals' in analysis_data['uptrend_analysis']:
        for interval in analysis_data['uptrend_analysis']['intervals']:
            # 计算专业指标
            start_price = interval.get('start_price', 0)
            end_price = interval.get('end_price', 0)
            high_price = interval.get('high_price', 0)
            low_price = interval.get('low_price', 0)
            
            # 基础指标
            price_change = end_price - start_price if start_price > 0 else 0
            price_change_pct = (price_change / start_price * 100) if start_price > 0 else 0
            
            # 波动性指标
            volatility = ((high_price - low_price) / start_price * 100) if start_price > 0 else 0
            
            # 趋势强度
            trend_strength = abs(price_change_pct)
            
            # 风险收益比
            ideal_profit = interval.get('long_ideal_profit', 0)
            risk_loss = interval.get('long_risk_loss', 0)
            risk_reward_ratio = ideal_profit / risk_loss if risk_loss > 0 else 0
            
            # 持续时间
            duration_hours = interval.get('duration_hours', 0)
            
            trend_data = {
                'trend_id': f"UPTREND_{interval.get('interval_id', '')}",
                'trend_type': 'uptrend',
                'start_time': interval.get('start_time', ''),
                'end_time': interval.get('end_time', ''),
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
                'actual_profit': interval.get('long_actual_profit', 0),
                'risk_loss': risk_loss,
                'risk_reward_ratio': risk_reward_ratio,
                'max_rally': interval.get('max_rally', 0),
                'max_decline': interval.get('max_decline', 0),
                'pfe': interval.get('pfe', 0),
                'mae': interval.get('mae', 0)
            }
            trends_data.append(trend_data)
    
    # 处理下跌趋势
    if 'downtrend_analysis' in analysis_data and 'intervals' in analysis_data['downtrend_analysis']:
        for interval in analysis_data['downtrend_analysis']['intervals']:
            # 计算专业指标
            start_price = interval.get('start_price', 0)
            end_price = interval.get('end_price', 0)
            high_price = interval.get('high_price', 0)
            low_price = interval.get('low_price', 0)
            
            # 基础指标
            price_change = end_price - start_price if start_price > 0 else 0
            price_change_pct = (price_change / start_price * 100) if start_price > 0 else 0
            
            # 波动性指标
            volatility = ((high_price - low_price) / start_price * 100) if start_price > 0 else 0
            
            # 趋势强度
            trend_strength = abs(price_change_pct)
            
            # 风险收益比
            ideal_profit = interval.get('short_ideal_profit', 0)
            risk_loss = interval.get('short_risk_loss', 0)
            risk_reward_ratio = ideal_profit / risk_loss if risk_loss > 0 else 0
            
            # 持续时间
            duration_hours = interval.get('duration_hours', 0)
            
            trend_data = {
                'trend_id': f"DOWNTREND_{interval.get('interval_id', '')}",
                'trend_type': 'downtrend',
                'start_time': interval.get('start_time', ''),
                'end_time': interval.get('end_time', ''),
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
                'actual_profit': interval.get('short_actual_profit', 0),
                'risk_loss': risk_loss,
                'risk_reward_ratio': risk_reward_ratio,
                'max_rally': interval.get('max_rally', 0),
                'max_decline': interval.get('max_decline', 0),
                'pfe': interval.get('pfe', 0),
                'mae': interval.get('mae', 0)
            }
            trends_data.append(trend_data)
    
    if not trends_data:
        return None
    
    # 创建DataFrame
    df = pd.DataFrame(trends_data)
    
    # 转换时间列
    df['start_time'] = pd.to_datetime(df['start_time'])
    df['end_time'] = pd.to_datetime(df['end_time'])
    
    # 添加专业分类
    df['risk_level'] = pd.cut(df['risk_reward_ratio'], 
                             bins=[0, 0.5, 1.0, float('inf')], 
                             labels=['高风险', '中风险', '低风险'])
    
    df['profit_level'] = pd.cut(df['ideal_profit'], 
                               bins=[0, 2, 5, 10, float('inf')], 
                               labels=['低收益', '中收益', '高收益', '超高收益'])
    
    df['volatility_level'] = pd.cut(df['volatility'], 
                                   bins=[0, 5, 10, 20, float('inf')], 
                                   labels=['低波动', '中波动', '高波动', '极高波动'])
    
    # 按时间排序
    df = df.sort_values('start_time')
    
    return df

def create_professional_metrics(df):
    """创建专业级指标面板"""
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        st.metric(
            label="📊 总趋势数",
            value=f"{len(df):,}",
            delta=f"覆盖 {df['start_time'].min().strftime('%Y-%m')} 至 {df['start_time'].max().strftime('%Y-%m')}"
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
        avg_profit = df['ideal_profit'].mean()
        st.metric(
            label="💰 平均理想收益",
            value=f"{avg_profit:.2f}%",
            delta=f"最高: {df['ideal_profit'].max():.2f}%"
        )
    
    with col5:
        avg_risk = df['risk_loss'].mean()
        st.metric(
            label="⚠️ 平均风险损失",
            value=f"{avg_risk:.2f}%",
            delta=f"最高: {df['risk_loss'].max():.2f}%"
        )
    
    with col6:
        avg_volatility = df['volatility'].mean()
        st.metric(
            label="📊 平均波动率",
            value=f"{avg_volatility:.2f}%",
            delta=f"最高: {df['volatility'].max():.2f}%"
        )

def create_advanced_analytics_charts(df):
    """创建高级分析图表"""
    
    # 1. 趋势强度分布热力图
    fig1 = go.Figure()
    
    # 按月份和趋势类型分组
    df['month'] = df['start_time'].dt.to_period('M')
    monthly_data = df.groupby(['month', 'trend_type']).agg({
        'trend_strength': 'mean',
        'volatility': 'mean',
        'ideal_profit': 'mean',
        'risk_loss': 'mean'
    }).reset_index()
    
    # 创建热力图
    fig1.add_trace(go.Heatmap(
        z=monthly_data['trend_strength'],
        x=monthly_data['month'].astype(str),
        y=monthly_data['trend_type'],
        colorscale='Viridis',
        showscale=True
    ))
    
    fig1.update_layout(
        title="趋势强度热力图 (按月份)",
        xaxis_title="月份",
        yaxis_title="趋势类型",
        height=400
    )
    
    # 2. 风险收益散点图矩阵
    fig2 = make_subplots(
        rows=2, cols=2,
        subplot_titles=('理想收益 vs 风险损失', '波动率 vs 趋势强度', 
                       '持续时间 vs 收益', '风险收益比分布'),
        specs=[[{"type": "scatter"}, {"type": "scatter"}],
               [{"type": "scatter"}, {"type": "histogram"}]]
    )
    
    # 散点图1: 理想收益 vs 风险损失
    fig2.add_trace(
        go.Scatter(
            x=df['risk_loss'],
            y=df['ideal_profit'],
            mode='markers',
            marker=dict(
                color=df['trend_strength'],
                size=8,
                colorscale='RdYlGn',
                showscale=True,
                colorbar=dict(title="趋势强度")
            ),
            text=df['trend_id'],
            name='风险收益关系'
        ),
        row=1, col=1
    )
    
    # 散点图2: 波动率 vs 趋势强度
    fig2.add_trace(
        go.Scatter(
            x=df['volatility'],
            y=df['trend_strength'],
            mode='markers',
            marker=dict(
                color=df['ideal_profit'],
                size=8,
                colorscale='Blues',
                showscale=True,
                colorbar=dict(title="理想收益")
            ),
            text=df['trend_id'],
            name='波动率关系'
        ),
        row=1, col=2
    )
    
    # 散点图3: 持续时间 vs 收益
    fig2.add_trace(
        go.Scatter(
            x=df['duration_hours'],
            y=df['ideal_profit'],
            mode='markers',
            marker=dict(
                color=df['risk_reward_ratio'],
                size=8,
                colorscale='Reds',
                showscale=True,
                colorbar=dict(title="风险收益比")
            ),
            text=df['trend_id'],
            name='时间收益关系'
        ),
        row=2, col=1
    )
    
    # 直方图4: 风险收益比分布
    fig2.add_trace(
        go.Histogram(
            x=df['risk_reward_ratio'],
            nbinsx=20,
            name='风险收益比分布'
        ),
        row=2, col=2
    )
    
    fig2.update_layout(
        title="高级风险收益分析矩阵",
        height=800,
        showlegend=False
    )
    
    # 3. 时间序列分析
    fig3 = make_subplots(
        rows=3, cols=1,
        subplot_titles=('价格变化时间序列', '波动率时间序列', '风险收益比时间序列'),
        vertical_spacing=0.1
    )
    
    # 价格变化时间序列
    fig3.add_trace(
        go.Scatter(
            x=df['start_time'],
            y=df['price_change_pct'],
            mode='lines+markers',
            name='价格变化%',
            line=dict(color='blue', width=2)
        ),
        row=1, col=1
    )
    
    # 波动率时间序列
    fig3.add_trace(
        go.Scatter(
            x=df['start_time'],
            y=df['volatility'],
            mode='lines+markers',
            name='波动率%',
            line=dict(color='red', width=2)
        ),
        row=2, col=1
    )
    
    # 风险收益比时间序列
    fig3.add_trace(
        go.Scatter(
            x=df['start_time'],
            y=df['risk_reward_ratio'],
            mode='lines+markers',
            name='风险收益比',
            line=dict(color='green', width=2)
        ),
        row=3, col=1
    )
    
    fig3.update_layout(
        title="时间序列深度分析",
        height=900,
        showlegend=True
    )
    
    return fig1, fig2, fig3

def create_insights_panel(df):
    """创建数据洞察面板"""
    st.markdown("### 🔍 深度数据洞察")
    
    # 计算关键洞察
    insights = []
    
    # 1. 最佳交易机会
    best_opportunities = df.nlargest(5, 'ideal_profit')
    insights.append(f"🎯 **最佳交易机会**: 最高理想收益 {best_opportunities['ideal_profit'].iloc[0]:.2f}%")
    
    # 2. 风险分析
    high_risk_trends = df[df['risk_reward_ratio'] < 0.5]
    insights.append(f"⚠️ **高风险趋势**: {len(high_risk_trends)} 个 (风险收益比 < 0.5)")
    
    # 3. 波动性分析
    high_volatility = df[df['volatility'] > df['volatility'].quantile(0.8)]
    insights.append(f"📊 **高波动趋势**: {len(high_volatility)} 个 (波动率 > {df['volatility'].quantile(0.8):.2f}%)")
    
    # 4. 时间模式
    avg_duration = df['duration_hours'].mean()
    insights.append(f"⏱️ **平均趋势持续时间**: {avg_duration:.1f} 小时 ({avg_duration/24:.1f} 天)")
    
    # 5. 收益分布
    profitable_trends = df[df['ideal_profit'] > 0]
    insights.append(f"💰 **盈利趋势比例**: {len(profitable_trends)/len(df)*100:.1f}%")
    
    # 6. 风险收益比分析
    good_risk_reward = df[df['risk_reward_ratio'] > 1.0]
    insights.append(f"📈 **优质风险收益比**: {len(good_risk_reward)} 个 (比例 > 1.0)")
    
    # 显示洞察
    for insight in insights:
        st.markdown(f'<div class="data-insight">{insight}</div>', unsafe_allow_html=True)

def main():
    """主函数"""
    # 页面标题
    st.markdown('<h1 class="main-header">📊 ETH HMA 专业分析终端</h1>', unsafe_allow_html=True)
    
    # 终端风格状态显示
    st.markdown('<div class="terminal-header">🔍 正在加载最新分析数据...</div>', unsafe_allow_html=True)
    
    # 加载数据
    analysis_data, status_message = load_analysis_data()
    
    if analysis_data is None:
        st.error(f"❌ {status_message}")
        st.stop()
    else:
        st.success(f"✅ {status_message}")
    
    # 转换数据
    df = create_professional_dataframe(analysis_data)
    
    if df is None or df.empty:
        st.error("❌ 无法转换分析数据")
        st.stop()
    
    # 专业指标面板
    st.markdown("### 📊 专业指标面板")
    create_professional_metrics(df)
    
    # 侧边栏高级筛选
    st.sidebar.markdown("### 🔍 高级筛选器")
    
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
        options=['高风险', '中风险', '低风险'],
        default=['高风险', '中风险', '低风险']
    )
    
    # 收益等级筛选
    profit_levels = st.sidebar.multiselect(
        "💰 收益等级",
        options=['低收益', '中收益', '高收益', '超高收益'],
        default=['低收益', '中收益', '高收益', '超高收益']
    )
    
    # 波动率筛选
    volatility_range = st.sidebar.slider(
        "📊 波动率范围 (%)",
        min_value=float(df['volatility'].min()),
        max_value=float(df['volatility'].max()),
        value=(float(df['volatility'].min()), float(df['volatility'].max()))
    )
    
    # 应用筛选
    filtered_df = df[
        (df['start_time'].dt.date >= date_range[0]) &
        (df['start_time'].dt.date <= date_range[1]) &
        (df['trend_type'].isin(trend_types)) &
        (df['risk_level'].isin(risk_levels)) &
        (df['profit_level'].isin(profit_levels)) &
        (df['volatility'] >= volatility_range[0]) &
        (df['volatility'] <= volatility_range[1])
    ]
    
    if filtered_df.empty:
        st.warning("⚠️ 筛选后没有数据")
        st.stop()
    
    # 数据洞察面板
    create_insights_panel(filtered_df)
    
    # 高级分析图表
    st.markdown("### 📈 高级分析图表")
    
    # 创建图表
    fig1, fig2, fig3 = create_advanced_analytics_charts(filtered_df)
    
    # 显示图表
    st.plotly_chart(fig1, use_container_width=True)
    st.plotly_chart(fig2, use_container_width=True)
    st.plotly_chart(fig3, use_container_width=True)
    
    # 专业数据表格
    st.markdown("### 📋 专业数据表格")
    
    # 选择显示的列
    display_columns = [
        'trend_id', 'trend_type', 'start_time', 'end_time',
        'start_price', 'end_price', 'price_change_pct', 'volatility',
        'trend_strength', 'duration_hours', 'ideal_profit', 'actual_profit',
        'risk_loss', 'risk_reward_ratio', 'risk_level', 'profit_level', 'volatility_level'
    ]
    
    # 过滤存在的列
    available_columns = [col for col in display_columns if col in filtered_df.columns]
    
    st.dataframe(
        filtered_df[available_columns],
        use_container_width=True,
        height=400
    )
    
    # 数据统计摘要
    st.markdown("### 📊 数据统计摘要")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("筛选后趋势数", f"{len(filtered_df):,}")
    
    with col2:
        st.metric("平均理想收益", f"{filtered_df['ideal_profit'].mean():.2f}%")
    
    with col3:
        st.metric("平均风险损失", f"{filtered_df['risk_loss'].mean():.2f}%")
    
    with col4:
        st.metric("平均波动率", f"{filtered_df['volatility'].mean():.2f}%")

if __name__ == "__main__":
    main()
