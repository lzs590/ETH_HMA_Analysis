#!/usr/bin/env python3
"""
Unified Financial Dashboard
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

# Page configuration
st.set_page_config(
    page_title="ETH HMA 统一分析仪表板",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
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
    """Load the latest 4h analysis results"""
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
        return None, f"Error loading data: {e}"

@st.cache_data
def load_raw_data():
    """Load raw 4h data"""
    data_dir = Path("assets/data")
    data_files = list(data_dir.glob("ETHUSDT_4h_processed_*.parquet"))
    
    if not data_files:
        return None, "No 4h data found"
    
    latest_file = max(data_files, key=lambda f: f.stat().st_mtime)
    
    try:
        df = pd.read_parquet(latest_file)
        df['open_time'] = pd.to_datetime(df['open_time'])
        df.set_index('open_time', inplace=True)
        
        # Calculate deviation metrics
        df['deviation'] = df['close'] - df['HMA_45']
        df['deviation_pct'] = (df['close'] - df['HMA_45']) / df['HMA_45'] * 100
        df['deviation_ma'] = df['deviation'].rolling(window=20).mean()
        df['deviation_std'] = df['deviation'].rolling(window=20).std()
        df['deviation_zscore'] = (df['deviation'] - df['deviation_ma']) / df['deviation_std']
        df['deviation_momentum'] = df['deviation'].diff()
        df['deviation_acceleration'] = df['deviation_momentum'].diff()
        
        return df, latest_file.name
    except Exception as e:
        return None, f"Error loading data: {e}"

def create_deviation_analysis(df):
    """Create deviation analysis charts"""
    st.subheader("📊 Deviation Analysis (Price vs HMA)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Deviation time series
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=df.index, y=df['deviation'], 
                                 mode='lines', name='Deviation',
                                 line=dict(color='#2E86AB', width=2)))
        fig1.add_trace(go.Scatter(x=df.index, y=df['deviation_ma'], 
                                 mode='lines', name='Deviation MA(20)',
                                 line=dict(color='#F24236', width=2, dash='dash')))
        fig1.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
        fig1.update_layout(
            title="Price Deviation from HMA",
            xaxis_title="Time",
            yaxis_title="Deviation (USDT)",
            height=400
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Deviation percentage
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=df.index, y=df['deviation_pct'], 
                                 mode='lines', name='Deviation %',
                                 line=dict(color='#A23B72', width=2)))
        fig2.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
        fig2.update_layout(
            title="Price Deviation Percentage from HMA",
            xaxis_title="Time",
            yaxis_title="Deviation (%)",
            height=400
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    # Deviation distribution
    col3, col4 = st.columns(2)
    
    with col3:
        fig3 = px.histogram(df, x='deviation_pct', nbins=50, 
                           title="Deviation Distribution",
                           labels={'deviation_pct': 'Deviation (%)', 'count': 'Frequency'})
        fig3.update_layout(height=400)
        st.plotly_chart(fig3, use_container_width=True)
    
    with col4:
        fig4 = px.box(df, y='deviation_pct', 
                      title="Deviation Box Plot",
                      labels={'deviation_pct': 'Deviation (%)'})
        fig4.update_layout(height=400)
        st.plotly_chart(fig4, use_container_width=True)

def create_advanced_statistics(df, analysis_data):
    """Create advanced statistical analysis"""
    st.subheader("📈 Advanced Statistical Analysis")
    
    # Calculate comprehensive statistics
    stats_data = {
        'Metric': [],
        'Value': [],
        'Description': []
    }
    
    # Price statistics
    stats_data['Metric'].extend([
        'Price Mean', 'Price Std', 'Price Skewness', 'Price Kurtosis',
        'Price Min', 'Price Max', 'Price Range', 'Price CV'
    ])
    stats_data['Value'].extend([
        f"{df['close'].mean():.2f}",
        f"{df['close'].std():.2f}",
        f"{df['close'].skew():.3f}",
        f"{df['close'].kurtosis():.3f}",
        f"{df['close'].min():.2f}",
        f"{df['close'].max():.2f}",
        f"{df['close'].max() - df['close'].min():.2f}",
        f"{df['close'].std() / df['close'].mean() * 100:.2f}%"
    ])
    stats_data['Description'].extend([
        'Average price over period',
        'Price volatility measure',
        'Price distribution asymmetry',
        'Price distribution tail heaviness',
        'Lowest price in period',
        'Highest price in period',
        'Total price range',
        'Coefficient of variation'
    ])
    
    # Deviation statistics
    stats_data['Metric'].extend([
        'Deviation Mean', 'Deviation Std', 'Deviation Skewness', 'Deviation Kurtosis',
        'Deviation Min', 'Deviation Max', 'Deviation Range', 'Deviation CV'
    ])
    stats_data['Value'].extend([
        f"{df['deviation'].mean():.2f}",
        f"{df['deviation'].std():.2f}",
        f"{df['deviation'].skew():.3f}",
        f"{df['deviation'].kurtosis():.3f}",
        f"{df['deviation'].min():.2f}",
        f"{df['deviation'].max():.2f}",
        f"{df['deviation'].max() - df['deviation'].min():.2f}",
        f"{df['deviation'].std() / abs(df['deviation'].mean()) * 100:.2f}%"
    ])
    stats_data['Description'].extend([
        'Average deviation from HMA',
        'Deviation volatility measure',
        'Deviation distribution asymmetry',
        'Deviation distribution tail heaviness',
        'Maximum negative deviation',
        'Maximum positive deviation',
        'Total deviation range',
        'Deviation coefficient of variation'
    ])
    
    # Volume statistics
    stats_data['Metric'].extend([
        'Volume Mean', 'Volume Std', 'Volume Skewness', 'Volume Kurtosis',
        'Volume Min', 'Volume Max', 'Volume Range', 'Volume CV'
    ])
    stats_data['Value'].extend([
        f"{df['volume'].mean():.2f}",
        f"{df['volume'].std():.2f}",
        f"{df['volume'].skew():.3f}",
        f"{df['volume'].kurtosis():.3f}",
        f"{df['volume'].min():.2f}",
        f"{df['volume'].max():.2f}",
        f"{df['volume'].max() - df['volume'].min():.2f}",
        f"{df['volume'].std() / df['volume'].mean() * 100:.2f}%"
    ])
    stats_data['Description'].extend([
        'Average trading volume',
        'Volume volatility measure',
        'Volume distribution asymmetry',
        'Volume distribution tail heaviness',
        'Lowest volume in period',
        'Highest volume in period',
        'Total volume range',
        'Volume coefficient of variation'
    ])
    
    # Create statistics table
    stats_df = pd.DataFrame(stats_data)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.dataframe(stats_df, use_container_width=True)
    
    with col2:
        # Key insights
        st.markdown("### 🔍 Key Insights")
        
        # Price insights
        price_volatility = df['close'].std() / df['close'].mean() * 100
        if price_volatility > 20:
            st.markdown("⚠️ **High Price Volatility** - Market is very volatile")
        elif price_volatility > 10:
            st.markdown("📊 **Moderate Price Volatility** - Normal market conditions")
        else:
            st.markdown("✅ **Low Price Volatility** - Stable market conditions")
        
        # Deviation insights
        deviation_mean = df['deviation'].mean()
        if deviation_mean > 0:
            st.markdown("📈 **Positive Deviation** - Price generally above HMA")
        else:
            st.markdown("📉 **Negative Deviation** - Price generally below HMA")
        
        # Volume insights
        volume_trend = df['volume'].rolling(50).mean().iloc[-1] / df['volume'].rolling(50).mean().iloc[-50]
        if volume_trend > 1.2:
            st.markdown("🔥 **Increasing Volume** - Growing market interest")
        elif volume_trend < 0.8:
            st.markdown("❄️ **Decreasing Volume** - Declining market interest")
        else:
            st.markdown("📊 **Stable Volume** - Consistent market activity")

def create_correlation_analysis(df):
    """Create correlation analysis"""
    st.subheader("🔗 Correlation Analysis")
    
    # Select relevant columns
    corr_data = df[['close', 'volume', 'deviation', 'deviation_pct', 'HMA_45']].copy()
    corr_data['price_change'] = df['close'].pct_change()
    corr_data['volume_change'] = df['volume'].pct_change()
    
    # Calculate correlation matrix
    corr_matrix = corr_data.corr()
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Correlation heatmap
        fig = px.imshow(corr_matrix, 
                       text_auto=True, 
                       aspect="auto",
                       title="Correlation Matrix",
                       color_continuous_scale='RdBu_r')
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Top correlations
        st.markdown("### 🔍 Top Correlations")
        
        # Get upper triangle of correlation matrix
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
        corr_pairs = []
        
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_pairs.append({
                    'Pair': f"{corr_matrix.columns[i]} vs {corr_matrix.columns[j]}",
                    'Correlation': corr_matrix.iloc[i, j]
                })
        
        corr_df = pd.DataFrame(corr_pairs)
        corr_df = corr_df.sort_values('Correlation', key=abs, ascending=False)
        corr_df['Correlation'] = corr_df['Correlation'].round(3)
        
        st.dataframe(corr_df.head(10), use_container_width=True)

def create_trend_analysis(analysis_data):
    """Create trend analysis from analysis data"""
    st.subheader("📊 Trend Analysis")
    
    # Extract trend data
    uptrend_intervals = analysis_data.get('uptrend_analysis', {}).get('intervals', [])
    downtrend_intervals = analysis_data.get('downtrend_analysis', {}).get('intervals', [])
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Uptrends", len(uptrend_intervals))
        st.metric("Total Downtrends", len(downtrend_intervals))
    
    with col2:
        if uptrend_intervals:
            avg_uptrend_profit = np.mean([interval.get('long_ideal_profit', 0) for interval in uptrend_intervals])
            st.metric("Avg Uptrend Profit", f"{avg_uptrend_profit:.2f}%")
        
        if downtrend_intervals:
            avg_downtrend_profit = np.mean([interval.get('short_ideal_profit', 0) for interval in downtrend_intervals])
            st.metric("Avg Downtrend Profit", f"{avg_downtrend_profit:.2f}%")
    
    with col3:
        if uptrend_intervals:
            avg_uptrend_duration = np.mean([interval.get('duration_hours', 0) for interval in uptrend_intervals])
            st.metric("Avg Uptrend Duration", f"{avg_uptrend_duration:.1f}h")
        
        if downtrend_intervals:
            avg_downtrend_duration = np.mean([interval.get('duration_hours', 0) for interval in downtrend_intervals])
            st.metric("Avg Downtrend Duration", f"{avg_downtrend_duration:.1f}h")
    
    # Trend distribution charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Trend count
        trend_counts = [len(uptrend_intervals), len(downtrend_intervals)]
        trend_labels = ['Uptrends', 'Downtrends']
        colors = ['#2E8B57', '#DC143C']
        
        fig = px.bar(x=trend_labels, y=trend_counts, 
                    title="Trend Distribution",
                    color=trend_labels, color_discrete_sequence=colors)
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Profit distribution
        uptrend_profits = [interval.get('long_ideal_profit', 0) for interval in uptrend_intervals]
        downtrend_profits = [interval.get('short_ideal_profit', 0) for interval in downtrend_intervals]
        all_profits = uptrend_profits + downtrend_profits
        
        fig = px.histogram(x=all_profits, nbins=20, 
                          title="Profit Distribution",
                          labels={'x': 'Profit (%)', 'y': 'Frequency'})
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

def create_raw_data_display(df):
    """Create raw data display with filters"""
    st.subheader("📋 Raw Data Display")
    
    # Filters
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Date range filter
        min_date = df.index.min().date()
        max_date = df.index.max().date()
        date_range = st.date_input(
            "📅 Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
    
    with col2:
        # Price range filter
        price_range = st.slider(
            "💰 Price Range (USDT)",
            min_value=float(df['close'].min()),
            max_value=float(df['close'].max()),
            value=(float(df['close'].min()), float(df['close'].max()))
        )
    
    with col3:
        # Deviation range filter
        deviation_range = st.slider(
            "📊 Deviation Range (%)",
            min_value=float(df['deviation_pct'].min()),
            max_value=float(df['deviation_pct'].max()),
            value=(float(df['deviation_pct'].min()), float(df['deviation_pct'].max()))
        )
    
    with col4:
        # Volume range filter
        volume_range = st.slider(
            "📈 Volume Range",
            min_value=float(df['volume'].min()),
            max_value=float(df['volume'].max()),
            value=(float(df['volume'].min()), float(df['volume'].max()))
        )
    
    # Apply filters
    filtered_df = df.copy()
    
    if len(date_range) == 2:
        filtered_df = filtered_df[
            (filtered_df.index.date >= date_range[0]) & 
            (filtered_df.index.date <= date_range[1])
        ]
    
    filtered_df = filtered_df[
        (filtered_df['close'] >= price_range[0]) & 
        (filtered_df['close'] <= price_range[1]) &
        (filtered_df['deviation_pct'] >= deviation_range[0]) & 
        (filtered_df['deviation_pct'] <= deviation_range[1]) &
        (filtered_df['volume'] >= volume_range[0]) & 
        (filtered_df['volume'] <= volume_range[1])
    ]
    
    # Display filtered data
    st.write(f"📊 Showing {len(filtered_df)} records (filtered from {len(df)} total)")
    
    # Sort options
    sort_by = st.selectbox(
        "Sort by:",
        ['Time', 'Price', 'Deviation %', 'Volume', 'HMA']
    )
    
    sort_columns = {
        'Time': 'index',
        'Price': 'close',
        'Deviation %': 'deviation_pct',
        'Volume': 'volume',
        'HMA': 'HMA_45'
    }
    
    ascending = st.checkbox("Ascending order", value=True)
    filtered_df = filtered_df.sort_values(sort_columns[sort_by], ascending=ascending)
    
    # Display data
    display_columns = ['close', 'volume', 'HMA_45', 'deviation', 'deviation_pct', 'deviation_zscore']
    st.dataframe(filtered_df[display_columns], use_container_width=True)

def main():
    """Main dashboard function"""
    st.markdown('<h1 class="main-header">📊 ETH HMA Unified Analysis Dashboard</h1>', unsafe_allow_html=True)
    
    # Load data
    analysis_data, analysis_file = load_analysis_data()
    raw_data, data_file = load_raw_data()
    
    if analysis_data is None or raw_data is None:
        st.error("❌ Unable to load data. Please ensure analysis has been run.")
        return
    
    st.success(f"✅ Loaded analysis: {analysis_file}")
    st.success(f"✅ Loaded data: {data_file}")
    
    # Sidebar
    st.sidebar.title("🎛️ Dashboard Controls")
    
    # Navigation
    page = st.sidebar.selectbox(
        "📄 Select Analysis Page:",
        ["🏠 Overview", "📊 Deviation Analysis", "📈 Advanced Statistics", 
         "🔗 Correlation Analysis", "📊 Trend Analysis", "📋 Raw Data Display"]
    )
    
    if page == "🏠 Overview":
        st.subheader("📊 Dashboard Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Records", len(raw_data))
            st.metric("Time Range", f"{(raw_data.index.max() - raw_data.index.min()).days} days")
        
        with col2:
            st.metric("Current Price", f"${raw_data['close'].iloc[-1]:.2f}")
            st.metric("Current HMA", f"${raw_data['HMA_45'].iloc[-1]:.2f}")
        
        with col3:
            current_deviation = raw_data['deviation'].iloc[-1]
            current_deviation_pct = raw_data['deviation_pct'].iloc[-1]
            st.metric("Current Deviation", f"${current_deviation:.2f}")
            st.metric("Deviation %", f"{current_deviation_pct:.2f}%")
        
        with col4:
            st.metric("Current Volume", f"{raw_data['volume'].iloc[-1]:,.0f}")
            st.metric("Avg Volume", f"{raw_data['volume'].mean():,.0f}")
        
        # Quick charts
        col1, col2 = st.columns(2)
        
        with col1:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=raw_data.index, y=raw_data['close'], 
                                   mode='lines', name='Price', line=dict(color='#2E86AB')))
            fig.add_trace(go.Scatter(x=raw_data.index, y=raw_data['HMA_45'], 
                                   mode='lines', name='HMA', line=dict(color='#F24236')))
            fig.update_layout(title="Price vs HMA", height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=raw_data.index, y=raw_data['deviation_pct'], 
                                   mode='lines', name='Deviation %', line=dict(color='#A23B72')))
            fig.add_hline(y=0, line_dash="dash", line_color="gray")
            fig.update_layout(title="Price Deviation from HMA", height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    elif page == "📊 Deviation Analysis":
        create_deviation_analysis(raw_data)
    
    elif page == "📈 Advanced Statistics":
        create_advanced_statistics(raw_data, analysis_data)
    
    elif page == "🔗 Correlation Analysis":
        create_correlation_analysis(raw_data)
    
    elif page == "📊 Trend Analysis":
        create_trend_analysis(analysis_data)
    
    elif page == "📋 Raw Data Display":
        create_raw_data_display(raw_data)

if __name__ == "__main__":
    main()
