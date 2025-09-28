#!/usr/bin/env python3
"""
专业金融数据分析仪表板
使用Streamlit构建实时交互式金融数据查看器
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# 页面配置
st.set_page_config(
    page_title="ETH HMA 趋势分析仪表板",
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
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_trend_data():
    """加载趋势数据"""
    try:
        df = pd.read_csv('../assets/reports/trends_4h_chronological.csv')
        df['start_time'] = pd.to_datetime(df['start_time'])
        df['end_time'] = pd.to_datetime(df['end_time'])
        return df
    except FileNotFoundError:
        st.error("❌ 找不到趋势数据文件，请先运行分析生成数据")
        return None

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
        uptrends = len(df[df['trend_type'] == '上升趋势'])
        st.metric(
            label="📈 上升趋势",
            value=f"{uptrends:,}",
            delta=f"{uptrends/len(df)*100:.1f}%"
        )
    
    with col3:
        downtrends = len(df[df['trend_type'] == '下降趋势'])
        st.metric(
            label="📉 下降趋势", 
            value=f"{downtrends:,}",
            delta=f"{downtrends/len(df)*100:.1f}%"
        )
    
    with col4:
        risk_trends = len(df[df['is_risk_greater'] == True])
        st.metric(
            label="⚠️ 高风险趋势",
            value=f"{risk_trends:,}",
            delta=f"{risk_trends/len(df)*100:.1f}%"
        )
    
    with col5:
        avg_duration = df['duration_hours'].mean()
        st.metric(
            label="⏱️ 平均持续时间",
            value=f"{avg_duration:.1f}h",
            delta=None
        )

def create_filters(df):
    """创建数据筛选器"""
    st.sidebar.header("🔍 数据筛选器")
    
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
        options=['上升趋势', '下降趋势'],
        default=['上升趋势', '下降趋势']
    )
    
    # 风险筛选
    risk_filter = st.sidebar.selectbox(
        "⚠️ 风险等级",
        options=['全部', '高风险', '低风险'],
        index=0
    )
    
    # 持续时间筛选
    duration_range = st.sidebar.slider(
        "⏱️ 持续时间 (小时)",
        min_value=int(df['duration_hours'].min()),
        max_value=int(df['duration_hours'].max()),
        value=(int(df['duration_hours'].min()), int(df['duration_hours'].max()))
    
    # 价格变化筛选
    price_change_range = st.sidebar.slider(
        "💰 价格变化 (%)",
        min_value=float(df['price_change_pct'].min()),
        max_value=float(df['price_change_pct'].max()),
        value=(float(df['price_change_pct'].min()), float(df['price_change_pct'].max()))
    
    return {
        'date_range': date_range,
        'trend_types': trend_types,
        'risk_filter': risk_filter,
        'duration_range': duration_range,
        'price_change_range': price_change_range
    }

def apply_filters(df, filters):
    """应用筛选条件"""
    filtered_df = df.copy()
    
    # 时间范围筛选
    if len(filters['date_range']) == 2:
        start_date, end_date = filters['date_range']
        filtered_df = filtered_df[
            (filtered_df['start_time'].dt.date >= start_date) &
            (filtered_df['start_time'].dt.date <= end_date)
        ]
    
    # 趋势类型筛选
    if filters['trend_types']:
        filtered_df = filtered_df[filtered_df['trend_type'].isin(filters['trend_types'])]
    
    # 风险筛选
    if filters['risk_filter'] == '高风险':
        filtered_df = filtered_df[filtered_df['is_risk_greater'] == True]
    elif filters['risk_filter'] == '低风险':
        filtered_df = filtered_df[filtered_df['is_risk_greater'] == False]
    
    # 持续时间筛选
    filtered_df = filtered_df[
        (filtered_df['duration_hours'] >= filters['duration_range'][0]) &
        (filtered_df['duration_hours'] <= filters['duration_range'][1])
    ]
    
    # 价格变化筛选
    filtered_df = filtered_df[
        (filtered_df['price_change_pct'] >= filters['price_change_range'][0]) &
        (filtered_df['price_change_pct'] <= filters['price_change_range'][1])
    ]
    
    return filtered_df

def create_charts(df):
    """创建图表"""
    col1, col2 = st.columns(2)
    
    with col1:
        # 趋势类型分布饼图
        fig_pie = px.pie(
            df, 
            names='trend_type', 
            title="📊 趋势类型分布",
            color_discrete_map={'上升趋势': '#2ca02c', '下降趋势': '#d62728'}
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # 风险分布饼图
        risk_labels = df['is_risk_greater'].map({True: '高风险', False: '低风险'})
        fig_risk = px.pie(
            values=df['is_risk_greater'].value_counts().values,
            names=['低风险', '高风险'],
            title="⚠️ 风险分布",
            color_discrete_map={'低风险': '#2ca02c', '高风险': '#d62728'}
        )
        st.plotly_chart(fig_risk, use_container_width=True)
    
    # 时间序列图
    st.subheader("📈 趋势时间序列分析")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 价格变化时间序列
        fig_price = px.line(
            df, 
            x='start_time', 
            y='price_change_pct',
            color='trend_type',
            title="💰 价格变化时间序列",
            color_discrete_map={'上升趋势': '#2ca02c', '下降趋势': '#d62728'}
        )
        fig_price.add_hline(y=0, line_dash="dash", line_color="gray")
        st.plotly_chart(fig_price, use_container_width=True)
    
    with col2:
        # 持续时间分布
        fig_duration = px.histogram(
            df,
            x='duration_hours',
            color='trend_type',
            title="⏱️ 持续时间分布",
            color_discrete_map={'上升趋势': '#2ca02c', '下降趋势': '#d62728'}
        )
        st.plotly_chart(fig_duration, use_container_width=True)
    
    # 风险收益散点图
    st.subheader("📊 风险收益分析")
    
    fig_scatter = px.scatter(
        df,
        x='max_rally',
        y='max_decline',
        color='trend_type',
        size='duration_hours',
        hover_data=['trend_id', 'price_change_pct', 'risk_ratio'],
        title="🎯 风险收益散点图",
        color_discrete_map={'上升趋势': '#2ca02c', '下降趋势': '#d62728'}
    )
    fig_scatter.add_trace(go.Scatter(
        x=[0, df['max_rally'].max()],
        y=[0, df['max_decline'].max()],
        mode='lines',
        line=dict(dash='dash', color='gray'),
        name='风险收益平衡线'
    ))
    st.plotly_chart(fig_scatter, use_container_width=True)

def create_data_table(df):
    """创建数据表格"""
    st.subheader("📋 详细数据表格")
    
    # 选择显示的列
    display_columns = st.multiselect(
        "选择显示的列",
        options=df.columns.tolist(),
        default=['trend_id', 'trend_type', 'start_time', 'end_time', 'start_price', 'end_price', 'price_change_pct', 'max_rally', 'max_decline', 'risk_ratio', 'is_risk_greater', 'duration_hours']
    )
    
    if display_columns:
        # 格式化数据
        display_df = df[display_columns].copy()
        
        # 格式化数值列
        if 'price_change_pct' in display_df.columns:
            display_df['price_change_pct'] = display_df['price_change_pct'].round(2)
        if 'max_rally' in display_df.columns:
            display_df['max_rally'] = display_df['max_rally'].round(2)
        if 'max_decline' in display_df.columns:
            display_df['max_decline'] = display_df['max_decline'].round(2)
        if 'risk_ratio' in display_df.columns:
            display_df['risk_ratio'] = display_df['risk_ratio'].round(2)
        
        # 显示表格
        st.dataframe(
            display_df,
            use_container_width=True,
            height=400
        )
        
        # 下载按钮
        csv = display_df.to_csv(index=False)
        st.download_button(
            label="📥 下载筛选后的数据",
            data=csv,
            file_name=f"filtered_trends_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

def main():
    """主函数"""
    # 标题
    st.markdown('<h1 class="main-header">📊 ETH HMA 趋势分析仪表板</h1>', unsafe_allow_html=True)
    
    # 加载数据
    df = load_trend_data()
    if df is None:
        return
    
    # 创建筛选器
    filters = create_filters(df)
    
    # 应用筛选
    filtered_df = apply_filters(df, filters)
    
    # 显示筛选结果
    st.info(f"🔍 筛选结果: {len(filtered_df)} 个趋势 (原始数据: {len(df)} 个)")
    
    # 关键指标
    create_metrics_row(filtered_df)
    
    # 创建图表
    create_charts(filtered_df)
    
    # 数据表格
    create_data_table(filtered_df)
    
    # 统计摘要
    st.subheader("📊 统计摘要")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("平均价格变化", f"{filtered_df['price_change_pct'].mean():.2f}%")
        st.metric("最大价格上涨", f"{filtered_df['price_change_pct'].max():.2f}%")
        st.metric("最大价格下跌", f"{filtered_df['price_change_pct'].min():.2f}%")
    
    with col2:
        st.metric("平均持续时间", f"{filtered_df['duration_hours'].mean():.1f}小时")
        st.metric("最长持续时间", f"{filtered_df['duration_hours'].max()}小时")
        st.metric("最短持续时间", f"{filtered_df['duration_hours'].min()}小时")
    
    with col3:
        st.metric("平均风险收益比", f"{filtered_df['risk_ratio'].mean():.2f}")
        st.metric("最大风险收益比", f"{filtered_df['risk_ratio'].max():.2f}")
        st.metric("高风险趋势占比", f"{len(filtered_df[filtered_df['is_risk_greater']])/len(filtered_df)*100:.1f}%")

if __name__ == "__main__":
    main()
