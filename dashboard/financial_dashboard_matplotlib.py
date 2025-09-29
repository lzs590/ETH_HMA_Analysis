#!/usr/bin/env python3
"""
集成Matplotlib图表的专业金融分析Dashboard
将matplotlib图表与Streamlit结合，提供深度数据分析
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import json
import os
import glob
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# 设置matplotlib中文字体
import matplotlib
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
matplotlib.rcParams['axes.unicode_minus'] = False
matplotlib.rcParams['font.size'] = 10

# 页面配置
st.set_page_config(
    page_title="ETH HMA 专业分析终端 - Matplotlib版",
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
    .analysis-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
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
def create_professional_dataframe(analysis_data):
    """创建专业级DataFrame"""
    trends_data = []
    
    # 处理上涨趋势
    if 'uptrend_analysis' in analysis_data and 'intervals' in analysis_data['uptrend_analysis']:
        for interval in analysis_data['uptrend_analysis']['intervals']:
            start_price = interval.get('start_price', 0)
            end_price = interval.get('end_price', 0)
            high_price = interval.get('high_price', 0)
            low_price = interval.get('low_price', 0)
            
            price_change = end_price - start_price if start_price > 0 else 0
            price_change_pct = (price_change / start_price * 100) if start_price > 0 else 0
            volatility = ((high_price - low_price) / start_price * 100) if start_price > 0 else 0
            trend_strength = abs(price_change_pct)
            
            ideal_profit = interval.get('long_ideal_profit', 0)
            risk_loss = interval.get('long_risk_loss', 0)
            risk_reward_ratio = ideal_profit / risk_loss if risk_loss > 0 else 0
            
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
            start_price = interval.get('start_price', 0)
            end_price = interval.get('end_price', 0)
            high_price = interval.get('high_price', 0)
            low_price = interval.get('low_price', 0)
            
            price_change = end_price - start_price if start_price > 0 else 0
            price_change_pct = (price_change / start_price * 100) if start_price > 0 else 0
            volatility = ((high_price - low_price) / start_price * 100) if start_price > 0 else 0
            trend_strength = abs(price_change_pct)
            
            ideal_profit = interval.get('short_ideal_profit', 0)
            risk_loss = interval.get('short_risk_loss', 0)
            risk_reward_ratio = ideal_profit / risk_loss if risk_loss > 0 else 0
            
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
    
    df = pd.DataFrame(trends_data)
    df['start_time'] = pd.to_datetime(df['start_time'])
    df['end_time'] = pd.to_datetime(df['end_time'])
    df = df.sort_values('start_time')
    
    return df

def create_revenue_analysis_table(df):
    """创建收益分析表"""
    st.markdown("### 💰 收益分析表")
    
    # 计算收益指标
    revenue_metrics = {
        '指标': ['平均理想收益', '最大理想收益', '平均实际收益', '最大实际收益', '收益差距', '平均胜率'],
        '上涨趋势': [
            f"{df[df['trend_type'] == 'uptrend']['ideal_profit'].mean():.2f}%",
            f"{df[df['trend_type'] == 'uptrend']['ideal_profit'].max():.2f}%",
            f"{df[df['trend_type'] == 'uptrend']['actual_profit'].mean():.2f}%",
            f"{df[df['trend_type'] == 'uptrend']['actual_profit'].max():.2f}%",
            f"{df[df['trend_type'] == 'uptrend']['ideal_profit'].mean() - df[df['trend_type'] == 'uptrend']['actual_profit'].mean():.2f}%",
            f"{len(df[(df['trend_type'] == 'uptrend') & (df['actual_profit'] > 0)]) / len(df[df['trend_type'] == 'uptrend']) * 100:.1f}%"
        ],
        '下跌趋势': [
            f"{df[df['trend_type'] == 'downtrend']['ideal_profit'].mean():.2f}%",
            f"{df[df['trend_type'] == 'downtrend']['ideal_profit'].max():.2f}%",
            f"{df[df['trend_type'] == 'downtrend']['actual_profit'].mean():.2f}%",
            f"{df[df['trend_type'] == 'downtrend']['actual_profit'].max():.2f}%",
            f"{df[df['trend_type'] == 'downtrend']['ideal_profit'].mean() - df[df['trend_type'] == 'downtrend']['actual_profit'].mean():.2f}%",
            f"{len(df[(df['trend_type'] == 'downtrend') & (df['actual_profit'] > 0)]) / len(df[df['trend_type'] == 'downtrend']) * 100:.1f}%"
        ]
    }
    
    revenue_df = pd.DataFrame(revenue_metrics)
    st.dataframe(revenue_df, use_container_width=True)
    
    # 收益分析洞察
    st.markdown("#### 🔍 收益分析洞察")
    avg_ideal_profit = df['ideal_profit'].mean()
    avg_actual_profit = df['actual_profit'].mean()
    profit_gap = avg_ideal_profit - avg_actual_profit
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("平均理想收益", f"{avg_ideal_profit:.2f}%")
    with col2:
        st.metric("平均实际收益", f"{avg_actual_profit:.2f}%")
    with col3:
        st.metric("收益差距", f"{profit_gap:.2f}%", delta=f"策略优化空间: {profit_gap/avg_ideal_profit*100:.1f}%")

def create_risk_analysis_table(df):
    """创建风险分析表"""
    st.markdown("### ⚠️ 风险分析表")
    
    # 计算风险指标
    risk_metrics = {
        '指标': ['平均风险损失', '最大风险损失', '平均风险收益比', '高风险趋势数', '风险等级分布'],
        '上涨趋势': [
            f"{df[df['trend_type'] == 'uptrend']['risk_loss'].mean():.2f}%",
            f"{df[df['trend_type'] == 'uptrend']['risk_loss'].max():.2f}%",
            f"{df[df['trend_type'] == 'uptrend']['risk_reward_ratio'].mean():.2f}",
            f"{len(df[(df['trend_type'] == 'uptrend') & (df['risk_reward_ratio'] < 1)])}",
            f"低风险: {len(df[(df['trend_type'] == 'uptrend') & (df['risk_reward_ratio'] > 2)])} | 中风险: {len(df[(df['trend_type'] == 'uptrend') & (df['risk_reward_ratio'] >= 1) & (df['risk_reward_ratio'] <= 2)])} | 高风险: {len(df[(df['trend_type'] == 'uptrend') & (df['risk_reward_ratio'] < 1)])}"
        ],
        '下跌趋势': [
            f"{df[df['trend_type'] == 'downtrend']['risk_loss'].mean():.2f}%",
            f"{df[df['trend_type'] == 'downtrend']['risk_loss'].max():.2f}%",
            f"{df[df['trend_type'] == 'downtrend']['risk_reward_ratio'].mean():.2f}",
            f"{len(df[(df['trend_type'] == 'downtrend') & (df['risk_reward_ratio'] < 1)])}",
            f"低风险: {len(df[(df['trend_type'] == 'downtrend') & (df['risk_reward_ratio'] > 2)])} | 中风险: {len(df[(df['trend_type'] == 'downtrend') & (df['risk_reward_ratio'] >= 1) & (df['risk_reward_ratio'] <= 2)])} | 高风险: {len(df[(df['trend_type'] == 'downtrend') & (df['risk_reward_ratio'] < 1)])}"
        ]
    }
    
    risk_df = pd.DataFrame(risk_metrics)
    st.dataframe(risk_df, use_container_width=True)
    
    # 风险分析洞察
    st.markdown("#### 🔍 风险分析洞察")
    avg_risk_loss = df['risk_loss'].mean()
    high_risk_count = len(df[df['risk_reward_ratio'] < 1])
    risk_percentage = high_risk_count / len(df) * 100
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("平均风险损失", f"{avg_risk_loss:.2f}%")
    with col2:
        st.metric("高风险趋势数", f"{high_risk_count}")
    with col3:
        st.metric("高风险比例", f"{risk_percentage:.1f}%")

def create_trend_characteristics_table(df):
    """创建趋势特征表"""
    st.markdown("### 📈 趋势特征表")
    
    # 计算趋势特征
    trend_metrics = {
        '指标': ['平均持续时间', '最大持续时间', '平均趋势强度', '最大趋势强度', '平均波动率', '最大波动率'],
        '上涨趋势': [
            f"{df[df['trend_type'] == 'uptrend']['duration_hours'].mean():.1f}小时",
            f"{df[df['trend_type'] == 'uptrend']['duration_hours'].max():.1f}小时",
            f"{df[df['trend_type'] == 'uptrend']['trend_strength'].mean():.2f}%",
            f"{df[df['trend_type'] == 'uptrend']['trend_strength'].max():.2f}%",
            f"{df[df['trend_type'] == 'uptrend']['volatility'].mean():.2f}%",
            f"{df[df['trend_type'] == 'uptrend']['volatility'].max():.2f}%"
        ],
        '下跌趋势': [
            f"{df[df['trend_type'] == 'downtrend']['duration_hours'].mean():.1f}小时",
            f"{df[df['trend_type'] == 'downtrend']['duration_hours'].max():.1f}小时",
            f"{df[df['trend_type'] == 'downtrend']['trend_strength'].mean():.2f}%",
            f"{df[df['trend_type'] == 'downtrend']['trend_strength'].max():.2f}%",
            f"{df[df['trend_type'] == 'downtrend']['volatility'].mean():.2f}%",
            f"{df[df['trend_type'] == 'downtrend']['volatility'].max():.2f}%"
        ]
    }
    
    trend_df = pd.DataFrame(trend_metrics)
    st.dataframe(trend_df, use_container_width=True)
    
    # 趋势特征洞察
    st.markdown("#### 🔍 趋势特征洞察")
    avg_duration = df['duration_hours'].mean()
    avg_strength = df['trend_strength'].mean()
    avg_volatility = df['volatility'].mean()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("平均持续时间", f"{avg_duration:.1f}小时")
    with col2:
        st.metric("平均趋势强度", f"{avg_strength:.2f}%")
    with col3:
        st.metric("平均波动率", f"{avg_volatility:.2f}%")

def create_matplotlib_charts(df):
    """创建matplotlib图表"""
    st.markdown("### 📊 专业Matplotlib图表分析")
    
    # 创建图表
    fig, axes = plt.subplots(2, 3, figsize=(20, 12))
    fig.suptitle('ETH HMA 专业分析图表', fontsize=16, fontweight='bold')
    
    # 1. 收益分布直方图
    ax1 = axes[0, 0]
    uptrend_profits = df[df['trend_type'] == 'uptrend']['ideal_profit']
    downtrend_profits = df[df['trend_type'] == 'downtrend']['ideal_profit']
    
    ax1.hist(uptrend_profits, bins=20, alpha=0.7, label='上涨趋势收益', color='green')
    ax1.hist(downtrend_profits, bins=20, alpha=0.7, label='下跌趋势收益', color='red')
    ax1.set_title('理想收益分布')
    ax1.set_xlabel('收益百分比 (%)')
    ax1.set_ylabel('频次')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 2. 风险收益散点图
    ax2 = axes[0, 1]
    scatter = ax2.scatter(df['risk_loss'], df['ideal_profit'], 
                         c=df['risk_reward_ratio'], cmap='RdYlGn', 
                         alpha=0.7, s=50)
    ax2.set_title('风险收益关系')
    ax2.set_xlabel('风险损失 (%)')
    ax2.set_ylabel('理想收益 (%)')
    plt.colorbar(scatter, ax=ax2, label='风险收益比')
    ax2.grid(True, alpha=0.3)
    
    # 3. 趋势强度vs持续时间
    ax3 = axes[0, 2]
    uptrend_data = df[df['trend_type'] == 'uptrend']
    downtrend_data = df[df['trend_type'] == 'downtrend']
    
    ax3.scatter(uptrend_data['duration_hours'], uptrend_data['trend_strength'], 
               alpha=0.7, label='上涨趋势', color='green', s=50)
    ax3.scatter(downtrend_data['duration_hours'], downtrend_data['trend_strength'], 
               alpha=0.7, label='下跌趋势', color='red', s=50)
    ax3.set_title('趋势强度vs持续时间')
    ax3.set_xlabel('持续时间 (小时)')
    ax3.set_ylabel('趋势强度 (%)')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # 4. 波动率分析
    ax4 = axes[1, 0]
    ax4.boxplot([uptrend_data['volatility'], downtrend_data['volatility']], 
               labels=['上涨趋势', '下跌趋势'])
    ax4.set_title('波动率分布')
    ax4.set_ylabel('波动率 (%)')
    ax4.grid(True, alpha=0.3)
    
    # 5. 风险收益比分布
    ax5 = axes[1, 1]
    ax5.hist(df['risk_reward_ratio'], bins=20, alpha=0.7, color='purple')
    ax5.axvline(x=1, color='red', linestyle='--', label='风险收益比=1')
    ax5.set_title('风险收益比分布')
    ax5.set_xlabel('风险收益比')
    ax5.set_ylabel('频次')
    ax5.legend()
    ax5.grid(True, alpha=0.3)
    
    # 6. 时间序列分析
    ax6 = axes[1, 2]
    df_sorted = df.sort_values('start_time')
    ax6.plot(df_sorted['start_time'], df_sorted['ideal_profit'], 
             alpha=0.7, label='理想收益', linewidth=2)
    ax6.plot(df_sorted['start_time'], df_sorted['actual_profit'], 
             alpha=0.7, label='实际收益', linewidth=2)
    ax6.set_title('收益时间序列')
    ax6.set_xlabel('时间')
    ax6.set_ylabel('收益 (%)')
    ax6.legend()
    ax6.grid(True, alpha=0.3)
    plt.setp(ax6.xaxis.get_majorticklabels(), rotation=45)
    
    plt.tight_layout()
    st.pyplot(fig)

def create_performance_analysis(df):
    """创建表现分析"""
    st.markdown("### 🎯 策略表现分析")
    
    # 计算关键指标
    total_trends = len(df)
    uptrends = len(df[df['trend_type'] == 'uptrend'])
    downtrends = len(df[df['trend_type'] == 'downtrend'])
    
    avg_ideal_profit = df['ideal_profit'].mean()
    avg_actual_profit = df['actual_profit'].mean()
    avg_risk_loss = df['risk_loss'].mean()
    avg_risk_reward_ratio = df['risk_reward_ratio'].mean()
    
    # 表现分析表格
    performance_data = {
        '指标': [
            '总趋势数', '上涨趋势数', '下跌趋势数', 
            '平均理想收益', '平均实际收益', '平均风险损失',
            '平均风险收益比', '最佳风险收益比', '最差风险收益比'
        ],
        '数值': [
            f"{total_trends}",
            f"{uptrends}",
            f"{downtrends}",
            f"{avg_ideal_profit:.2f}%",
            f"{avg_actual_profit:.2f}%",
            f"{avg_risk_loss:.2f}%",
            f"{avg_risk_reward_ratio:.2f}",
            f"{df['risk_reward_ratio'].max():.2f}",
            f"{df['risk_reward_ratio'].min():.2f}"
        ]
    }
    
    performance_df = pd.DataFrame(performance_data)
    st.dataframe(performance_df, use_container_width=True)
    
    # 表现分析洞察
    st.markdown("#### 🔍 表现分析洞察")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("策略效率", f"{(avg_actual_profit/avg_ideal_profit*100):.1f}%", 
                 delta=f"理想收益的{avg_actual_profit/avg_ideal_profit*100:.1f}%")
    with col2:
        st.metric("风险控制", f"{avg_risk_reward_ratio:.2f}", 
                 delta="风险收益比" if avg_risk_reward_ratio > 1 else "需要优化")
    with col3:
        st.metric("收益稳定性", f"{df['actual_profit'].std():.2f}%", 
                 delta="标准差" if df['actual_profit'].std() < 5 else "波动较大")
    with col4:
        st.metric("趋势捕捉率", f"{len(df[df['actual_profit'] > 0])/len(df)*100:.1f}%", 
                 delta="盈利趋势比例")

def main():
    """主函数"""
    # 页面标题
    st.markdown('<h1 class="main-header">📊 ETH HMA 专业分析终端 - Matplotlib版</h1>', unsafe_allow_html=True)
    
    # 数据状态显示
    st.markdown('<div class="analysis-section">🔍 正在加载最新分析数据...</div>', unsafe_allow_html=True)
    
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
    
    # 风险收益比筛选
    risk_reward_range = st.sidebar.slider(
        "⚠️ 风险收益比范围",
        min_value=float(df['risk_reward_ratio'].min()),
        max_value=float(df['risk_reward_ratio'].max()),
        value=(float(df['risk_reward_ratio'].min()), float(df['risk_reward_ratio'].max()))
    )
    
    # 应用筛选
    filtered_df = df[
        (df['start_time'].dt.date >= date_range[0]) &
        (df['start_time'].dt.date <= date_range[1]) &
        (df['trend_type'].isin(trend_types)) &
        (df['risk_reward_ratio'] >= risk_reward_range[0]) &
        (df['risk_reward_ratio'] <= risk_reward_range[1])
    ]
    
    if filtered_df.empty:
        st.warning("⚠️ 筛选后没有数据")
        st.stop()
    
    # 主要分析内容
    st.markdown("### 📊 专业数据分析表格")
    
    # 收益分析表
    create_revenue_analysis_table(filtered_df)
    
    # 风险分析表
    create_risk_analysis_table(filtered_df)
    
    # 趋势特征表
    create_trend_characteristics_table(filtered_df)
    
    # 策略表现分析
    create_performance_analysis(filtered_df)
    
    # Matplotlib图表
    create_matplotlib_charts(filtered_df)
    
    # 数据洞察
    st.markdown("### 🔍 深度数据洞察")
    
    # 计算洞察指标
    insights = []
    
    # 最佳交易机会
    best_opportunities = filtered_df.nlargest(3, 'ideal_profit')
    insights.append(f"🎯 **最佳交易机会**: 最高理想收益 {best_opportunities['ideal_profit'].iloc[0]:.2f}%")
    
    # 风险分析
    high_risk_trends = filtered_df[filtered_df['risk_reward_ratio'] < 1]
    insights.append(f"⚠️ **高风险趋势**: {len(high_risk_trends)} 个 (风险收益比 < 1)")
    
    # 波动性分析
    high_volatility = filtered_df[filtered_df['volatility'] > filtered_df['volatility'].quantile(0.8)]
    insights.append(f"📊 **高波动趋势**: {len(high_volatility)} 个 (波动率 > {filtered_df['volatility'].quantile(0.8):.2f}%)")
    
    # 时间模式
    avg_duration = filtered_df['duration_hours'].mean()
    insights.append(f"⏱️ **平均趋势持续时间**: {avg_duration:.1f} 小时 ({avg_duration/24:.1f} 天)")
    
    # 收益分布
    profitable_trends = filtered_df[filtered_df['actual_profit'] > 0]
    insights.append(f"💰 **盈利趋势比例**: {len(profitable_trends)/len(filtered_df)*100:.1f}%")
    
    # 风险收益比分析
    good_risk_reward = filtered_df[filtered_df['risk_reward_ratio'] > 1.0]
    insights.append(f"📈 **优质风险收益比**: {len(good_risk_reward)} 个 (比例 > 1.0)")
    
    # 显示洞察
    for insight in insights:
        st.markdown(f'<div class="data-insight">{insight}</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
