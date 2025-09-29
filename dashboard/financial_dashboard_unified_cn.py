#!/usr/bin/env python3
"""
统一金融分析仪表板 - 中文版
整合专业版、深度分析版、高级专业版功能
加入偏离值分析和详细数据统计
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from pathlib import Path
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# 页面配置
st.set_page_config(
    page_title="ETH HMA 统一分析仪表板",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS
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
    .deviation-positive {
        color: #2E8B57;
        font-weight: bold;
    }
    .deviation-negative {
        color: #DC143C;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_analysis_data():
    """加载最新的4h分析结果"""
    reports_dir = Path("assets/reports")
    json_files = list(reports_dir.glob("trend_analysis_4h_*.json"))
    
    if not json_files:
        return None, "未找到4h分析结果"
    
    latest_file = max(json_files, key=lambda f: f.stat().st_mtime)
    
    try:
        with open(latest_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data, latest_file.name
    except Exception as e:
        return None, f"数据加载错误: {e}"

@st.cache_data
def load_raw_data():
    """加载原始4h数据"""
    data_dir = Path("assets/data")
    data_files = list(data_dir.glob("ETHUSDT_4h_processed_*.parquet"))
    
    if not data_files:
        return None, "未找到4h数据"
    
    latest_file = max(data_files, key=lambda f: f.stat().st_mtime)
    
    try:
        df = pd.read_parquet(latest_file)
        df['open_time'] = pd.to_datetime(df['open_time'])
        df.set_index('open_time', inplace=True)
        
        # 计算偏离值指标
        df['deviation'] = df['close'] - df['HMA_45']
        df['deviation_pct'] = (df['close'] - df['HMA_45']) / df['HMA_45'] * 100
        df['deviation_ma'] = df['deviation'].rolling(window=20).mean()
        df['deviation_std'] = df['deviation'].rolling(window=20).std()
        df['deviation_zscore'] = (df['deviation'] - df['deviation_ma']) / df['deviation_std']
        df['deviation_momentum'] = df['deviation'].diff()
        df['deviation_acceleration'] = df['deviation_momentum'].diff()
        
        return df, latest_file.name
    except Exception as e:
        return None, f"数据加载错误: {e}"

def create_deviation_analysis(df):
    """创建偏离值分析图表"""
    st.subheader("📊 偏离值分析 (价格与HMA差值)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 偏离值时间序列
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=df.index, y=df['deviation'], 
                                 mode='lines', name='偏离值',
                                 line=dict(color='#2E86AB', width=2)))
        fig1.add_trace(go.Scatter(x=df.index, y=df['deviation_ma'], 
                                 mode='lines', name='偏离值MA(20)',
                                 line=dict(color='#F24236', width=2, dash='dash')))
        fig1.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
        fig1.update_layout(
            title="价格偏离HMA值",
            xaxis_title="时间",
            yaxis_title="偏离值 (USDT)",
            height=400
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # 偏离值百分比
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=df.index, y=df['deviation_pct'], 
                                 mode='lines', name='偏离百分比',
                                 line=dict(color='#A23B72', width=2)))
        fig2.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
        fig2.update_layout(
            title="价格偏离HMA百分比",
            xaxis_title="时间",
            yaxis_title="偏离百分比 (%)",
            height=400
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    # 偏离值分布
    col3, col4 = st.columns(2)
    
    with col3:
        fig3 = px.histogram(df, x='deviation_pct', nbins=50, 
                           title="偏离值分布",
                           labels={'deviation_pct': '偏离百分比 (%)', 'count': '频次'})
        fig3.update_layout(height=400)
        st.plotly_chart(fig3, use_container_width=True)
    
    with col4:
        fig4 = px.box(df, y='deviation_pct', 
                      title="偏离值箱线图",
                      labels={'deviation_pct': '偏离百分比 (%)'})
        fig4.update_layout(height=400)
        st.plotly_chart(fig4, use_container_width=True)

def create_advanced_statistics(df, analysis_data):
    """创建高级统计分析"""
    st.subheader("📈 高级统计分析")
    
    # 计算综合统计数据
    stats_data = {
        '指标': [],
        '数值': [],
        '描述': []
    }
    
    # 价格统计
    stats_data['指标'].extend([
        '价格均值', '价格标准差', '价格偏度', '价格峰度',
        '价格最小值', '价格最大值', '价格极差', '价格变异系数'
    ])
    stats_data['数值'].extend([
        f"{df['close'].mean():.2f}",
        f"{df['close'].std():.2f}",
        f"{df['close'].skew():.3f}",
        f"{df['close'].kurtosis():.3f}",
        f"{df['close'].min():.2f}",
        f"{df['close'].max():.2f}",
        f"{df['close'].max() - df['close'].min():.2f}",
        f"{df['close'].std() / df['close'].mean() * 100:.2f}%"
    ])
    stats_data['描述'].extend([
        '期间平均价格',
        '价格波动性度量',
        '价格分布不对称性',
        '价格分布尾部厚重性',
        '期间最低价格',
        '期间最高价格',
        '总价格范围',
        '变异系数'
    ])
    
    # 偏离值统计
    stats_data['指标'].extend([
        '偏离值均值', '偏离值标准差', '偏离值偏度', '偏离值峰度',
        '偏离值最小值', '偏离值最大值', '偏离值极差', '偏离值变异系数'
    ])
    stats_data['数值'].extend([
        f"{df['deviation'].mean():.2f}",
        f"{df['deviation'].std():.2f}",
        f"{df['deviation'].skew():.3f}",
        f"{df['deviation'].kurtosis():.3f}",
        f"{df['deviation'].min():.2f}",
        f"{df['deviation'].max():.2f}",
        f"{df['deviation'].max() - df['deviation'].min():.2f}",
        f"{df['deviation'].std() / abs(df['deviation'].mean()) * 100:.2f}%"
    ])
    stats_data['描述'].extend([
        '偏离HMA的平均值',
        '偏离值波动性度量',
        '偏离值分布不对称性',
        '偏离值分布尾部厚重性',
        '最大负偏离值',
        '最大正偏离值',
        '总偏离值范围',
        '偏离值变异系数'
    ])
    
    # 成交量统计
    stats_data['指标'].extend([
        '成交量均值', '成交量标准差', '成交量偏度', '成交量峰度',
        '成交量最小值', '成交量最大值', '成交量极差', '成交量变异系数'
    ])
    stats_data['数值'].extend([
        f"{df['volume'].mean():.2f}",
        f"{df['volume'].std():.2f}",
        f"{df['volume'].skew():.3f}",
        f"{df['volume'].kurtosis():.3f}",
        f"{df['volume'].min():.2f}",
        f"{df['volume'].max():.2f}",
        f"{df['volume'].max() - df['volume'].min():.2f}",
        f"{df['volume'].std() / df['volume'].mean() * 100:.2f}%"
    ])
    stats_data['描述'].extend([
        '平均交易量',
        '成交量波动性度量',
        '成交量分布不对称性',
        '成交量分布尾部厚重性',
        '期间最低成交量',
        '期间最高成交量',
        '总成交量范围',
        '成交量变异系数'
    ])
    
    # 创建统计表格
    stats_df = pd.DataFrame(stats_data)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.dataframe(stats_df, use_container_width=True)
    
    with col2:
        # 关键洞察
        st.markdown("### 🔍 关键洞察")
        
        # 价格洞察
        price_volatility = df['close'].std() / df['close'].mean() * 100
        if price_volatility > 20:
            st.markdown("⚠️ **高价格波动性** - 市场非常波动")
        elif price_volatility > 10:
            st.markdown("📊 **中等价格波动性** - 正常市场条件")
        else:
            st.markdown("✅ **低价格波动性** - 稳定市场条件")
        
        # 偏离值洞察
        deviation_mean = df['deviation'].mean()
        if deviation_mean > 0:
            st.markdown("📈 **正偏离** - 价格普遍高于HMA")
        else:
            st.markdown("📉 **负偏离** - 价格普遍低于HMA")
        
        # 成交量洞察
        volume_trend = df['volume'].rolling(50).mean().iloc[-1] / df['volume'].rolling(50).mean().iloc[-50]
        if volume_trend > 1.2:
            st.markdown("🔥 **成交量增加** - 市场兴趣增长")
        elif volume_trend < 0.8:
            st.markdown("❄️ **成交量减少** - 市场兴趣下降")
        else:
            st.markdown("📊 **成交量稳定** - 市场活动一致")

def create_correlation_analysis(df):
    """创建相关性分析"""
    st.subheader("🔗 相关性分析")
    
    # 选择相关列
    corr_data = df[['close', 'volume', 'deviation', 'deviation_pct', 'HMA_45']].copy()
    corr_data['price_change'] = df['close'].pct_change()
    corr_data['volume_change'] = df['volume'].pct_change()
    
    # 计算相关性矩阵
    corr_matrix = corr_data.corr()
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 相关性热力图
        fig = px.imshow(corr_matrix, 
                       text_auto=True, 
                       aspect="auto",
                       title="相关性矩阵",
                       color_continuous_scale='RdBu_r')
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # 主要相关性
        st.markdown("### 🔍 主要相关性")
        
        # 获取相关性矩阵的上三角
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
        corr_pairs = []
        
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_pairs.append({
                    '配对': f"{corr_matrix.columns[i]} vs {corr_matrix.columns[j]}",
                    '相关性': corr_matrix.iloc[i, j]
                })
        
        corr_df = pd.DataFrame(corr_pairs)
        corr_df = corr_df.sort_values('相关性', key=abs, ascending=False)
        corr_df['相关性'] = corr_df['相关性'].round(3)
        
        st.dataframe(corr_df.head(10), use_container_width=True)

def create_trend_analysis(analysis_data):
    """从分析数据创建趋势分析"""
    st.subheader("📊 趋势分析")
    
    # 提取趋势数据
    uptrend_intervals = analysis_data.get('uptrend_analysis', {}).get('intervals', [])
    downtrend_intervals = analysis_data.get('downtrend_analysis', {}).get('intervals', [])
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("总上涨趋势", len(uptrend_intervals))
        st.metric("总下跌趋势", len(downtrend_intervals))
    
    with col2:
        if uptrend_intervals:
            avg_uptrend_profit = np.mean([interval.get('long_ideal_profit', 0) for interval in uptrend_intervals])
            st.metric("平均上涨收益", f"{avg_uptrend_profit:.2f}%")
        
        if downtrend_intervals:
            avg_downtrend_profit = np.mean([interval.get('short_ideal_profit', 0) for interval in downtrend_intervals])
            st.metric("平均下跌收益", f"{avg_downtrend_profit:.2f}%")
    
    with col3:
        if uptrend_intervals:
            avg_uptrend_duration = np.mean([interval.get('duration_hours', 0) for interval in uptrend_intervals])
            st.metric("平均上涨持续时间", f"{avg_uptrend_duration:.1f}小时")
        
        if downtrend_intervals:
            avg_downtrend_duration = np.mean([interval.get('duration_hours', 0) for interval in downtrend_intervals])
            st.metric("平均下跌持续时间", f"{avg_downtrend_duration:.1f}小时")
    
    # 趋势分布图表
    col1, col2 = st.columns(2)
    
    with col1:
        # 趋势计数
        trend_counts = [len(uptrend_intervals), len(downtrend_intervals)]
        trend_labels = ['上涨趋势', '下跌趋势']
        colors = ['#2E8B57', '#DC143C']
        
        fig = px.bar(x=trend_labels, y=trend_counts, 
                    title="趋势分布",
                    color=trend_labels, color_discrete_sequence=colors)
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # 收益分布
        uptrend_profits = [interval.get('long_ideal_profit', 0) for interval in uptrend_intervals]
        downtrend_profits = [interval.get('short_ideal_profit', 0) for interval in downtrend_intervals]
        all_profits = uptrend_profits + downtrend_profits
        
        fig = px.histogram(x=all_profits, nbins=20, 
                          title="收益分布",
                          labels={'x': '收益 (%)', 'y': '频次'})
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

def create_raw_data_display(df):
    """创建HMA趋势区间数据展示 - 基于项目核心思想"""
    st.subheader("📋 HMA趋势区间数据展示")
    st.markdown("基于Hull移动平均(HMA)技术指标识别的趋势区间，展示趋势开始时间、结束时间、价格变化、理想收益、风险损失等核心信息")
    
    # 计算HMA趋势分析指标 - 基于项目核心算法
    df_analysis = df.copy()
    
    # 1. HMA斜率计算（趋势方向识别）
    df_analysis['hma_slope'] = df_analysis['HMA_45'].diff()
    df_analysis['hma_slope_pct'] = (df_analysis['HMA_45'].pct_change() * 100)
    
    # 2. 趋势转换点识别（基于斜率变化）
    df_analysis['slope_sign'] = np.sign(df_analysis['hma_slope'])
    df_analysis['slope_change'] = df_analysis['slope_sign'].diff().fillna(0)
    df_analysis['turning_point'] = 0
    
    # 上涨趋势开始：斜率由负转正
    uptrend_start = df_analysis['slope_change'] == 2.0
    df_analysis.loc[uptrend_start, 'turning_point'] = 1
    
    # 下跌趋势开始：斜率由正转负
    downtrend_start = df_analysis['slope_change'] == -2.0
    df_analysis.loc[downtrend_start, 'turning_point'] = -1
    
    # 3. 识别趋势区间
    trend_intervals = []
    current_trend = None
    trend_start_idx = None
    trend_start_time = None
    trend_start_price = None
    
    for idx, row in df_analysis.iterrows():
        if row['turning_point'] == 1:  # 上涨趋势开始
            if current_trend == 'down' and trend_start_idx is not None:
                # 结束前一个下跌趋势
                trend_end_idx = idx
                trend_end_time = idx
                trend_end_price = row['close']
                
                # 计算趋势区间数据
                trend_data = df_analysis.loc[trend_start_time:trend_end_time]
                
                # 计算PFE/MAE
                high_price = trend_data['high'].max()
                low_price = trend_data['low'].min()
                
                # 下跌趋势（做空策略）
                pfe = (trend_start_price / low_price - 1) * 100  # 最大跌幅（理想收益）
                mae = (high_price / trend_start_price - 1) * 100  # 最大涨幅（风险损失）
                
                trend_intervals.append({
                    'trend_id': f"TREND_{len(trend_intervals)+1:03d}",
                    'trend_type': '下跌趋势',
                    'start_time': trend_start_time,
                    'end_time': trend_end_time,
                    'start_price': trend_start_price,
                    'end_price': trend_end_price,
                    'price_change_pct': (trend_end_price / trend_start_price - 1) * 100,
                    'ideal_profit': pfe,
                    'risk_loss': mae,
                    'risk_reward_ratio': mae / (pfe + 0.001),
                    'duration_hours': (trend_end_time - trend_start_time).total_seconds() / 3600,
                    'max_price': high_price,
                    'min_price': low_price,
                    'volatility': trend_data['close'].std(),
                    'hma_start': trend_data['HMA_45'].iloc[0],
                    'hma_end': trend_data['HMA_45'].iloc[-1]
                })
            
            # 开始新的上涨趋势
            current_trend = 'up'
            trend_start_idx = idx
            trend_start_time = idx
            trend_start_price = row['close']
            
        elif row['turning_point'] == -1:  # 下跌趋势开始
            if current_trend == 'up' and trend_start_idx is not None:
                # 结束前一个上涨趋势
                trend_end_idx = idx
                trend_end_time = idx
                trend_end_price = row['close']
                
                # 计算趋势区间数据
                trend_data = df_analysis.loc[trend_start_time:trend_end_time]
                
                # 计算PFE/MAE
                high_price = trend_data['high'].max()
                low_price = trend_data['low'].min()
                
                # 上涨趋势（做多策略）
                pfe = (high_price / trend_start_price - 1) * 100  # 最大涨幅（理想收益）
                mae = (trend_start_price / low_price - 1) * 100  # 最大跌幅（风险损失）
                
                trend_intervals.append({
                    'trend_id': f"TREND_{len(trend_intervals)+1:03d}",
                    'trend_type': '上涨趋势',
                    'start_time': trend_start_time,
                    'end_time': trend_end_time,
                    'start_price': trend_start_price,
                    'end_price': trend_end_price,
                    'price_change_pct': (trend_end_price / trend_start_price - 1) * 100,
                    'ideal_profit': pfe,
                    'risk_loss': mae,
                    'risk_reward_ratio': mae / (pfe + 0.001),
                    'duration_hours': (trend_end_time - trend_start_time).total_seconds() / 3600,
                    'max_price': high_price,
                    'min_price': low_price,
                    'volatility': trend_data['close'].std(),
                    'hma_start': trend_data['HMA_45'].iloc[0],
                    'hma_end': trend_data['HMA_45'].iloc[-1]
                })
            
            # 开始新的下跌趋势
            current_trend = 'down'
            trend_start_idx = idx
            trend_start_time = idx
            trend_start_price = row['close']
    
    # 转换为DataFrame
    if trend_intervals:
        df_trends = pd.DataFrame(trend_intervals)
        df_trends['start_time'] = pd.to_datetime(df_trends['start_time'])
        df_trends['end_time'] = pd.to_datetime(df_trends['end_time'])
        
        # 计算置信度
        df_trends['confidence_score'] = (
            (df_trends['ideal_profit'] - df_trends['risk_loss']) * 
            df_trends['duration_hours'] / (df_trends['volatility'] + 0.001)
        )
        
        # 风险等级分类
        df_trends['risk_level'] = pd.cut(
            df_trends['risk_reward_ratio'], 
            bins=[0, 0.5, 1.0, 2.0, float('inf')], 
            labels=['低风险', '中风险', '高风险', '极高风险']
        )
        
        # 收益等级分类
        df_trends['profit_level'] = pd.cut(
            df_trends['ideal_profit'], 
            bins=[0, 2, 5, 10, float('inf')], 
            labels=['低收益', '中收益', '高收益', '极高收益']
        )
    else:
        st.warning("⚠️ 未识别到任何趋势区间，请检查数据或调整HMA参数")
        return
    
    # 筛选器
    st.markdown("### 🔍 趋势区间筛选器")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # 日期范围筛选
        min_date = df_trends['start_time'].min().date()
        max_date = df_trends['start_time'].max().date()
        date_range = st.date_input(
            "📅 趋势开始日期范围",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
        
        # 趋势类型筛选
        trend_types = st.multiselect(
            "📈 趋势类型",
            options=['上涨趋势', '下跌趋势'],
            default=['上涨趋势', '下跌趋势']
        )
        
        # 风险等级筛选
        risk_levels = st.multiselect(
            "⚠️ 风险等级",
            options=['低风险', '中风险', '高风险', '极高风险'],
            default=['低风险', '中风险', '高风险', '极高风险']
        )
    
    with col2:
        # 理想收益筛选
        ideal_profit_range = st.slider(
            "💰 理想收益范围 (%)",
            min_value=float(df_trends['ideal_profit'].min()),
            max_value=float(df_trends['ideal_profit'].max()),
            value=(float(df_trends['ideal_profit'].min()), float(df_trends['ideal_profit'].max()))
        )
        
        # 风险损失筛选
        risk_loss_range = st.slider(
            "⚠️ 风险损失范围 (%)",
            min_value=float(df_trends['risk_loss'].min()),
            max_value=float(df_trends['risk_loss'].max()),
            value=(float(df_trends['risk_loss'].min()), float(df_trends['risk_loss'].max()))
        )
        
        # 持续时间筛选
        duration_range = st.slider(
            "⏱️ 持续时间范围 (小时)",
            min_value=float(df_trends['duration_hours'].min()),
            max_value=float(df_trends['duration_hours'].max()),
            value=(float(df_trends['duration_hours'].min()), float(df_trends['duration_hours'].max()))
        )
    
    with col3:
        # 价格变化筛选
        price_change_range = st.slider(
            "📊 价格变化范围 (%)",
            min_value=float(df_trends['price_change_pct'].min()),
            max_value=float(df_trends['price_change_pct'].max()),
            value=(float(df_trends['price_change_pct'].min()), float(df_trends['price_change_pct'].max()))
        )
        
        # 风险收益比筛选
        risk_reward_range = st.slider(
            "⚖️ 风险收益比范围",
            min_value=float(df_trends['risk_reward_ratio'].min()),
            max_value=float(df_trends['risk_reward_ratio'].max()),
            value=(float(df_trends['risk_reward_ratio'].min()), float(df_trends['risk_reward_ratio'].max()))
        )
        
        # 置信度筛选
        confidence_range = st.slider(
            "🎯 置信度范围",
            min_value=float(df_trends['confidence_score'].min()),
            max_value=float(df_trends['confidence_score'].max()),
            value=(float(df_trends['confidence_score'].min()), float(df_trends['confidence_score'].max()))
        )
    
    # 应用筛选
    filtered_df = df_trends.copy()
    
    if len(date_range) == 2:
        filtered_df = filtered_df[
            (filtered_df['start_time'].dt.date >= date_range[0]) & 
            (filtered_df['start_time'].dt.date <= date_range[1])
        ]
    
    filtered_df = filtered_df[
        (filtered_df['trend_type'].isin(trend_types)) &
        (filtered_df['risk_level'].isin(risk_levels)) &
        (filtered_df['ideal_profit'] >= ideal_profit_range[0]) & 
        (filtered_df['ideal_profit'] <= ideal_profit_range[1]) &
        (filtered_df['risk_loss'] >= risk_loss_range[0]) & 
        (filtered_df['risk_loss'] <= risk_loss_range[1]) &
        (filtered_df['duration_hours'] >= duration_range[0]) & 
        (filtered_df['duration_hours'] <= duration_range[1]) &
        (filtered_df['price_change_pct'] >= price_change_range[0]) & 
        (filtered_df['price_change_pct'] <= price_change_range[1]) &
        (filtered_df['risk_reward_ratio'] >= risk_reward_range[0]) & 
        (filtered_df['risk_reward_ratio'] <= risk_reward_range[1]) &
        (filtered_df['confidence_score'] >= confidence_range[0]) & 
        (filtered_df['confidence_score'] <= confidence_range[1])
    ]
    
    # 显示筛选后的数据
    st.write(f"📊 显示 {len(filtered_df)} 个趋势区间 (从 {len(df_trends)} 个总趋势中筛选)")
    
    # 排序选项
    sort_by = st.selectbox(
        "排序方式:",
        ['开始时间', '结束时间', '理想收益', '风险损失', '价格变化', '持续时间', '风险收益比', '置信度', '趋势ID']
    )
    
    ascending = st.checkbox("升序排列", value=True)
    
    # 根据选择进行排序
    if sort_by == '开始时间':
        filtered_df = filtered_df.sort_values('start_time', ascending=ascending)
    elif sort_by == '结束时间':
        filtered_df = filtered_df.sort_values('end_time', ascending=ascending)
    elif sort_by == '理想收益':
        filtered_df = filtered_df.sort_values('ideal_profit', ascending=ascending)
    elif sort_by == '风险损失':
        filtered_df = filtered_df.sort_values('risk_loss', ascending=ascending)
    elif sort_by == '价格变化':
        filtered_df = filtered_df.sort_values('price_change_pct', ascending=ascending)
    elif sort_by == '持续时间':
        filtered_df = filtered_df.sort_values('duration_hours', ascending=ascending)
    elif sort_by == '风险收益比':
        filtered_df = filtered_df.sort_values('risk_reward_ratio', ascending=ascending)
    elif sort_by == '置信度':
        filtered_df = filtered_df.sort_values('confidence_score', ascending=ascending)
    elif sort_by == '趋势ID':
        filtered_df = filtered_df.sort_values('trend_id', ascending=ascending)
    
    # 显示趋势区间数据 - 基于项目核心指标
    display_columns = [
        'trend_id', 'trend_type', 'start_time', 'end_time', 'start_price', 'end_price',
        'price_change_pct', 'ideal_profit', 'risk_loss', 'risk_reward_ratio',
        'duration_hours', 'max_price', 'min_price', 'volatility', 'confidence_score',
        'risk_level', 'profit_level'
    ]
    display_columns_cn = [
        '趋势ID', '趋势类型', '开始时间', '结束时间', '开始价格', '结束价格',
        '价格变化%', '理想收益%', '风险损失%', '风险收益比',
        '持续时间(小时)', '最高价', '最低价', '波动率', '置信度',
        '风险等级', '收益等级'
    ]
    
    # 重命名列
    display_df = filtered_df[display_columns].copy()
    display_df.columns = display_columns_cn
    
    # 格式化数值显示
    st.dataframe(display_df, use_container_width=True)
    
    # 多空双吃策略统计摘要
    st.subheader("📊 多空双吃策略统计摘要")
    st.markdown("**核心策略：上涨趋势做多，下跌趋势做空，多空双吃，风险收益并重**")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("总趋势数", len(display_df))
        uptrends = display_df[display_df['趋势类型'] == '上涨趋势']
        downtrends = display_df[display_df['趋势类型'] == '下跌趋势']
        st.metric("上涨趋势(做多)", len(uptrends))
        st.metric("下跌趋势(做空)", len(downtrends))
        st.metric("多空比例", f"{len(uptrends)}:{len(downtrends)}" if len(downtrends) > 0 else "N/A")
    
    with col2:
        st.metric("平均理想收益", f"{display_df['理想收益%'].mean():.2f}%")
        st.metric("平均风险损失", f"{display_df['风险损失%'].mean():.2f}%")
        st.metric("平均价格变化", f"{display_df['价格变化%'].mean():.2f}%")
        st.metric("平均风险收益比", f"{display_df['风险收益比'].mean():.2f}")
    
    with col3:
        st.metric("最高理想收益", f"{display_df['理想收益%'].max():.2f}%")
        st.metric("最大风险损失", f"{display_df['风险损失%'].max():.2f}%")
        st.metric("最长持续时间", f"{display_df['持续时间(小时)'].max():.1f}小时")
        st.metric("最高置信度", f"{display_df['置信度'].max():.2f}")
    
    with col4:
        st.metric("高风险趋势", len(display_df[display_df['风险等级'].isin(['高风险', '极高风险'])]))
        st.metric("高收益趋势", len(display_df[display_df['收益等级'].isin(['高收益', '极高收益'])]))
        st.metric("风险>收益趋势", len(display_df[display_df['风险收益比'] > 1.0]))
        st.metric("平均置信度", f"{display_df['置信度'].mean():.2f}")
    
    # 多空策略详细对比
    if len(uptrends) > 0 and len(downtrends) > 0:
        st.subheader("⚖️ 多空策略详细对比")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("#### 🟢 做多策略表现")
            st.metric("做多趋势数量", len(uptrends))
            st.metric("做多平均收益", f"{uptrends['理想收益%'].mean():.2f}%")
            st.metric("做多平均风险", f"{uptrends['风险损失%'].mean():.2f}%")
            st.metric("做多风险收益比", f"{uptrends['风险收益比'].mean():.2f}")
        
        with col2:
            st.markdown("#### 🔴 做空策略表现")
            st.metric("做空趋势数量", len(downtrends))
            st.metric("做空平均收益", f"{downtrends['理想收益%'].mean():.2f}%")
            st.metric("做空平均风险", f"{downtrends['风险损失%'].mean():.2f}%")
            st.metric("做空风险收益比", f"{downtrends['风险收益比'].mean():.2f}")
        
        with col3:
            st.markdown("#### 📊 策略对比")
            st.metric("做多占比", f"{len(uptrends)/(len(uptrends)+len(downtrends))*100:.1f}%")
            st.metric("做空占比", f"{len(downtrends)/(len(uptrends)+len(downtrends))*100:.1f}%")
            st.metric("收益差异", f"{abs(uptrends['理想收益%'].mean() - downtrends['理想收益%'].mean()):.2f}%")
            st.metric("风险差异", f"{abs(uptrends['风险损失%'].mean() - downtrends['风险损失%'].mean()):.2f}%")
        
        with col4:
            st.markdown("#### 🎯 策略平衡性")
            balance_score = 1 - abs(len(uptrends) - len(downtrends)) / (len(uptrends) + len(downtrends))
            st.metric("策略平衡性", f"{balance_score:.2f}")
            st.metric("做多最高收益", f"{uptrends['理想收益%'].max():.2f}%")
            st.metric("做空最高收益", f"{downtrends['理想收益%'].max():.2f}%")
            st.metric("做多最大风险", f"{uptrends['风险损失%'].max():.2f}%")
            st.metric("做空最大风险", f"{downtrends['风险损失%'].max():.2f}%")
    
    # 多空双吃策略表现分析
    st.subheader("📈 多空双吃策略表现分析")
    st.markdown("**核心策略：上涨趋势做多，下跌趋势做空，多空双吃，风险收益并重**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 上涨趋势表现（做多策略）
        uptrends = display_df[display_df['趋势类型'] == '上涨趋势']
        if len(uptrends) > 0:
            st.markdown("#### 🟢 上涨趋势表现（做多策略）")
            st.metric("上涨趋势数量", len(uptrends))
            st.metric("平均理想收益", f"{uptrends['理想收益%'].mean():.2f}%")
            st.metric("平均风险损失", f"{uptrends['风险损失%'].mean():.2f}%")
            st.metric("平均风险收益比", f"{uptrends['风险收益比'].mean():.2f}")
            st.metric("平均持续时间", f"{uptrends['持续时间(小时)'].mean():.1f}小时")
            st.metric("最高理想收益", f"{uptrends['理想收益%'].max():.2f}%")
            st.metric("最大风险损失", f"{uptrends['风险损失%'].max():.2f}%")
        else:
            st.markdown("#### 🟢 上涨趋势表现（做多策略）")
            st.info("暂无上涨趋势数据")
    
    with col2:
        # 下跌趋势表现（做空策略）
        downtrends = display_df[display_df['趋势类型'] == '下跌趋势']
        if len(downtrends) > 0:
            st.markdown("#### 🔴 下跌趋势表现（做空策略）")
            st.metric("下跌趋势数量", len(downtrends))
            st.metric("平均理想收益", f"{downtrends['理想收益%'].mean():.2f}%")
            st.metric("平均风险损失", f"{downtrends['风险损失%'].mean():.2f}%")
            st.metric("平均风险收益比", f"{downtrends['风险收益比'].mean():.2f}")
            st.metric("平均持续时间", f"{downtrends['持续时间(小时)'].mean():.1f}小时")
            st.metric("最高理想收益", f"{downtrends['理想收益%'].max():.2f}%")
            st.metric("最大风险损失", f"{downtrends['风险损失%'].max():.2f}%")
        else:
            st.markdown("#### 🔴 下跌趋势表现（做空策略）")
            st.info("暂无下跌趋势数据")
    
    # 多空策略对比分析
    st.subheader("⚖️ 多空策略对比分析")
    
    if len(uptrends) > 0 and len(downtrends) > 0:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("做多vs做空数量比", f"{len(uptrends)}:{len(downtrends)}")
            st.metric("做多占比", f"{len(uptrends)/(len(uptrends)+len(downtrends))*100:.1f}%")
        
        with col2:
            st.metric("做多平均收益", f"{uptrends['理想收益%'].mean():.2f}%")
            st.metric("做空平均收益", f"{downtrends['理想收益%'].mean():.2f}%")
        
        with col3:
            st.metric("做多平均风险", f"{uptrends['风险损失%'].mean():.2f}%")
            st.metric("做空平均风险", f"{downtrends['风险损失%'].mean():.2f}%")
        
        with col4:
            st.metric("做多风险收益比", f"{uptrends['风险收益比'].mean():.2f}")
            st.metric("做空风险收益比", f"{downtrends['风险收益比'].mean():.2f}")
    
    # 策略综合表现
    st.subheader("🎯 策略综合表现")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # 整体策略表现
        st.markdown("#### 📊 整体策略表现")
        st.metric("总趋势数量", len(display_df))
        st.metric("平均理想收益", f"{display_df['理想收益%'].mean():.2f}%")
        st.metric("平均风险损失", f"{display_df['风险损失%'].mean():.2f}%")
        st.metric("平均风险收益比", f"{display_df['风险收益比'].mean():.2f}")
    
    with col2:
        # 高收益趋势分析
        st.markdown("#### 💰 高收益趋势分析")
        high_profit_trends = display_df[display_df['理想收益%'] > 5.0]
        st.metric("高收益趋势数量", len(high_profit_trends))
        st.metric("高收益趋势占比", f"{len(high_profit_trends)/len(display_df)*100:.1f}%")
        
        if len(high_profit_trends) > 0:
            uptrend_high = high_profit_trends[high_profit_trends['趋势类型'] == '上涨趋势']
            downtrend_high = high_profit_trends[high_profit_trends['趋势类型'] == '下跌趋势']
            st.metric("高收益做多趋势", len(uptrend_high))
            st.metric("高收益做空趋势", len(downtrend_high))
    
    with col3:
        # 风险控制分析
        st.markdown("#### ⚠️ 风险控制分析")
        high_risk_trends = display_df[display_df['风险收益比'] > 1.0]
        st.metric("高风险趋势数量", len(high_risk_trends))
        st.metric("高风险趋势占比", f"{len(high_risk_trends)/len(display_df)*100:.1f}%")
        
        if len(high_risk_trends) > 0:
            uptrend_risk = high_risk_trends[high_risk_trends['趋势类型'] == '上涨趋势']
            downtrend_risk = high_risk_trends[high_risk_trends['趋势类型'] == '下跌趋势']
            st.metric("高风险做多趋势", len(uptrend_risk))
            st.metric("高风险做空趋势", len(downtrend_risk))
    
    # 风险分析
    st.subheader("⚠️ 风险分析")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # 高风险趋势
        high_risk_trends = display_df[display_df['风险收益比'] > 1.0]
        st.metric("高风险趋势数量", len(high_risk_trends))
        st.metric("高风险趋势占比", f"{len(high_risk_trends)/len(display_df)*100:.1f}%")
    
    with col2:
        # 高收益趋势
        high_profit_trends = display_df[display_df['理想收益%'] > 5.0]
        st.metric("高收益趋势数量", len(high_profit_trends))
        st.metric("高收益趋势占比", f"{len(high_profit_trends)/len(display_df)*100:.1f}%")
    
    with col3:
        # 高置信度趋势
        high_confidence_trends = display_df[display_df['置信度'] > display_df['置信度'].quantile(0.8)]
        st.metric("高置信度趋势数量", len(high_confidence_trends))
        st.metric("高置信度趋势占比", f"{len(high_confidence_trends)/len(display_df)*100:.1f}%")

def main():
    """主仪表板函数"""
    st.markdown('<h1 class="main-header">📊 ETH HMA 统一分析仪表板</h1>', unsafe_allow_html=True)
    
    # 加载数据
    analysis_data, analysis_file = load_analysis_data()
    raw_data, data_file = load_raw_data()
    
    if analysis_data is None or raw_data is None:
        st.error("❌ 无法加载数据。请确保已运行分析。")
        return
    
    st.success(f"✅ 已加载分析: {analysis_file}")
    st.success(f"✅ 已加载数据: {data_file}")
    
    # 侧边栏
    st.sidebar.title("🎛️ 仪表板控制")
    
    # 导航
    page = st.sidebar.selectbox(
        "📄 选择分析页面:",
        ["🏠 总览", "📊 偏离值分析", "📈 高级统计", 
         "🔗 相关性分析", "📊 趋势分析", "📋 原始数据显示"]
    )
    
    if page == "🏠 总览":
        st.subheader("📊 仪表板总览")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("总记录数", len(raw_data))
            st.metric("时间范围", f"{(raw_data.index.max() - raw_data.index.min()).days} 天")
        
        with col2:
            st.metric("当前价格", f"${raw_data['close'].iloc[-1]:.2f}")
            st.metric("当前HMA", f"${raw_data['HMA_45'].iloc[-1]:.2f}")
        
        with col3:
            current_deviation = raw_data['deviation'].iloc[-1]
            current_deviation_pct = raw_data['deviation_pct'].iloc[-1]
            st.metric("当前偏离值", f"${current_deviation:.2f}")
            st.metric("偏离百分比", f"{current_deviation_pct:.2f}%")
        
        with col4:
            st.metric("当前成交量", f"{raw_data['volume'].iloc[-1]:,.0f}")
            st.metric("平均成交量", f"{raw_data['volume'].mean():,.0f}")
        
        # 快速图表
        col1, col2 = st.columns(2)
        
        with col1:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=raw_data.index, y=raw_data['close'], 
                                   mode='lines', name='价格', line=dict(color='#2E86AB')))
            fig.add_trace(go.Scatter(x=raw_data.index, y=raw_data['HMA_45'], 
                                   mode='lines', name='HMA', line=dict(color='#F24236')))
            fig.update_layout(title="价格 vs HMA", height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=raw_data.index, y=raw_data['deviation_pct'], 
                                   mode='lines', name='偏离百分比', line=dict(color='#A23B72')))
            fig.add_hline(y=0, line_dash="dash", line_color="gray")
            fig.update_layout(title="价格偏离HMA", height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    elif page == "📊 偏离值分析":
        create_deviation_analysis(raw_data)
    
    elif page == "📈 高级统计":
        create_advanced_statistics(raw_data, analysis_data)
    
    elif page == "🔗 相关性分析":
        create_correlation_analysis(raw_data)
    
    elif page == "📊 趋势分析":
        create_trend_analysis(analysis_data)
    
    elif page == "📋 原始数据显示":
        create_raw_data_display(raw_data)

if __name__ == "__main__":
    main()
