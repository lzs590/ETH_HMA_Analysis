#!/usr/bin/env python3
"""
4h K-line Summary Report Generator
Generate a comprehensive single-page matplotlib report for 4h K-line data
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import json
from pathlib import Path
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Set matplotlib style
try:
    plt.style.use('seaborn-v0_8')
except OSError:
    plt.style.use('seaborn')

plt.rcParams.update({
    'font.family': 'Arial',
    'font.size': 9,
    'axes.titlesize': 11,
    'axes.labelsize': 9,
    'xtick.labelsize': 8,
    'ytick.labelsize': 8,
    'legend.fontsize': 8,
    'figure.titlesize': 14,
    'axes.grid': True,
    'grid.alpha': 0.3,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight'
})

def load_data():
    """Load 4h data and analysis results"""
    data_dir = Path("assets/data")
    reports_dir = Path("assets/reports")
    
    # Load 4h data
    data_files = list(data_dir.glob("ETHUSDT_4h_processed_*.parquet"))
    if not data_files:
        raise FileNotFoundError("No 4h processed data found")
    
    latest_file = max(data_files, key=lambda f: f.stat().st_mtime)
    df = pd.read_parquet(latest_file)
    df['open_time'] = pd.to_datetime(df['open_time'])
    df.set_index('open_time', inplace=True)
    
    # Load analysis results
    json_files = list(reports_dir.glob("trend_analysis_4h_*.json"))
    if not json_files:
        raise FileNotFoundError("No 4h analysis results found")
    
    latest_json = max(json_files, key=lambda f: f.stat().st_mtime)
    with open(latest_json, 'r', encoding='utf-8') as f:
        analysis_data = json.load(f)
    
    return df, analysis_data

def create_comprehensive_report(df, analysis_data):
    """Create comprehensive 4h K-line report"""
    fig = plt.figure(figsize=(20, 16))
    fig.suptitle('ETH 4h K-line Comprehensive Analysis Report', fontsize=18, fontweight='bold', y=0.98)
    
    # Create a complex grid layout
    gs = fig.add_gridspec(4, 4, hspace=0.3, wspace=0.3)
    
    # 1. Price and HMA (top row, spans 2 columns)
    ax1 = fig.add_subplot(gs[0, :2])
    ax1.plot(df.index, df['close'], label='Close Price', linewidth=1.5, color='#2E86AB')
    ax1.plot(df.index, df['HMA_45'], label='HMA(45)', linewidth=2, color='#F24236')
    ax1.fill_between(df.index, df['low'], df['high'], alpha=0.1, color='gray', label='Price Range')
    ax1.set_title('Price Movement and Hull Moving Average', fontweight='bold')
    ax1.set_ylabel('Price (USDT)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 2. Volume (top row, right)
    ax2 = fig.add_subplot(gs[0, 2:])
    ax2.bar(df.index, df['volume'], alpha=0.7, color='#A23B72', width=0.8)
    ax2.set_title('Trading Volume', fontweight='bold')
    ax2.set_ylabel('Volume')
    ax2.grid(True, alpha=0.3)
    
    # 3. Trend Distribution (second row, left)
    ax3 = fig.add_subplot(gs[1, 0])
    uptrend_intervals = analysis_data.get('uptrend_analysis', {}).get('intervals', [])
    downtrend_intervals = analysis_data.get('downtrend_analysis', {}).get('intervals', [])
    
    trend_counts = [len(uptrend_intervals), len(downtrend_intervals)]
    trend_labels = ['Uptrends', 'Downtrends']
    colors = ['#2E8B57', '#DC143C']
    
    bars = ax3.bar(trend_labels, trend_counts, color=colors, alpha=0.8)
    ax3.set_title('Trend Distribution', fontweight='bold')
    ax3.set_ylabel('Count')
    
    for bar, count in zip(bars, trend_counts):
        ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                str(count), ha='center', va='bottom', fontweight='bold')
    
    # 4. Profit Distribution (second row, middle)
    ax4 = fig.add_subplot(gs[1, 1])
    uptrend_profits = [interval.get('long_ideal_profit', 0) for interval in uptrend_intervals]
    downtrend_profits = [interval.get('short_ideal_profit', 0) for interval in downtrend_intervals]
    all_profits = uptrend_profits + downtrend_profits
    
    ax4.hist(all_profits, bins=15, alpha=0.7, color='#4A90E2', edgecolor='black')
    ax4.axvline(np.mean(all_profits), color='red', linestyle='--', 
               label=f'Mean: {np.mean(all_profits):.2f}%')
    ax4.set_title('Profit Distribution', fontweight='bold')
    ax4.set_xlabel('Profit (%)')
    ax4.set_ylabel('Frequency')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    # 5. Risk vs Reward (second row, right)
    ax5 = fig.add_subplot(gs[1, 2:])
    uptrend_risks = [interval.get('long_risk_loss', 0) for interval in uptrend_intervals]
    downtrend_risks = [interval.get('max_rally', 0) for interval in downtrend_intervals]
    all_risks = uptrend_risks + downtrend_risks
    
    scatter = ax5.scatter(all_risks, all_profits, alpha=0.6, s=50, color='#FF6B6B')
    ax5.set_title('Risk vs Reward Analysis', fontweight='bold')
    ax5.set_xlabel('Risk Loss (%)')
    ax5.set_ylabel('Ideal Profit (%)')
    ax5.grid(True, alpha=0.3)
    
    # Add correlation line
    if len(all_risks) > 1:
        z = np.polyfit(all_risks, all_profits, 1)
        p = np.poly1d(z)
        ax5.plot(all_risks, p(all_risks), "r--", alpha=0.8, linewidth=2)
    
    # 6. Volatility Analysis (third row, left)
    ax6 = fig.add_subplot(gs[2, 0])
    df['returns'] = df['close'].pct_change()
    df['volatility_24h'] = df['returns'].rolling(window=6).std() * np.sqrt(6) * 100
    
    ax6.plot(df.index, df['volatility_24h'], alpha=0.8, color='#E74C3C', linewidth=1.5)
    ax6.set_title('24h Volatility', fontweight='bold')
    ax6.set_ylabel('Volatility (%)')
    ax6.grid(True, alpha=0.3)
    
    # 7. Price Deviation from HMA (third row, middle)
    ax7 = fig.add_subplot(gs[2, 1])
    deviation = ((df['close'] - df['HMA_45']) / df['HMA_45'] * 100)
    ax7.plot(df.index, deviation, color='#F18F01', linewidth=1.5)
    ax7.axhline(y=0, color='black', linestyle='--', alpha=0.5)
    ax7.fill_between(df.index, deviation, 0, alpha=0.3, color='#F18F01')
    ax7.set_title('Price Deviation from HMA', fontweight='bold')
    ax7.set_ylabel('Deviation (%)')
    ax7.grid(True, alpha=0.3)
    
    # 8. Duration Analysis (third row, right)
    ax8 = fig.add_subplot(gs[2, 2:])
    uptrend_durations = [interval.get('duration_hours', 0) for interval in uptrend_intervals]
    downtrend_durations = [interval.get('duration_hours', 0) for interval in downtrend_intervals]
    all_durations = uptrend_durations + downtrend_durations
    
    ax8.hist(all_durations, bins=15, alpha=0.7, color='#9B59B6', edgecolor='black')
    ax8.axvline(np.mean(all_durations), color='red', linestyle='--',
               label=f'Mean: {np.mean(all_durations):.1f}h')
    ax8.set_title('Trend Duration Distribution', fontweight='bold')
    ax8.set_xlabel('Duration (hours)')
    ax8.set_ylabel('Frequency')
    ax8.legend()
    ax8.grid(True, alpha=0.3)
    
    # 9. Performance Metrics Table (bottom row)
    ax9 = fig.add_subplot(gs[3, :])
    ax9.axis('off')
    
    # Extract key metrics
    uptrend_analysis = analysis_data.get('uptrend_analysis', {})
    downtrend_analysis = analysis_data.get('downtrend_analysis', {})
    
    metrics_data = [
        ['Metric', 'Uptrends', 'Downtrends', 'Overall'],
        ['Total Trends', uptrend_analysis.get('total_intervals', 0), 
         downtrend_analysis.get('total_intervals', 0), 
         uptrend_analysis.get('total_intervals', 0) + downtrend_analysis.get('total_intervals', 0)],
        ['Avg Profit (%)', f"{uptrend_analysis.get('avg_ideal_profit', 0):.2f}",
         f"{downtrend_analysis.get('avg_ideal_profit', 0):.2f}",
         f"{(uptrend_analysis.get('avg_ideal_profit', 0) + downtrend_analysis.get('avg_ideal_profit', 0))/2:.2f}"],
        ['Avg Risk (%)', f"{uptrend_analysis.get('avg_risk_loss', 0):.2f}",
         f"{downtrend_analysis.get('avg_risk_loss', 0):.2f}",
         f"{(uptrend_analysis.get('avg_risk_loss', 0) + downtrend_analysis.get('avg_risk_loss', 0))/2:.2f}"],
        ['Avg Duration (h)', f"{uptrend_analysis.get('avg_duration_hours', 0):.1f}",
         f"{downtrend_analysis.get('avg_duration_hours', 0):.1f}",
         f"{(uptrend_analysis.get('avg_duration_hours', 0) + downtrend_analysis.get('avg_duration_hours', 0))/2:.1f}"],
        ['Win Rate (%)', f"{uptrend_analysis.get('win_rate', 0):.1f}",
         f"{downtrend_analysis.get('win_rate', 0):.1f}",
         f"{(uptrend_analysis.get('win_rate', 0) + downtrend_analysis.get('win_rate', 0))/2:.1f}"],
        ['Risk-Reward Ratio', f"{uptrend_analysis.get('avg_risk_reward_ratio', 0):.2f}",
         f"{downtrend_analysis.get('avg_risk_reward_ratio', 0):.2f}",
         f"{(uptrend_analysis.get('avg_risk_reward_ratio', 0) + downtrend_analysis.get('avg_risk_reward_ratio', 0))/2:.2f}"]
    ]
    
    table = ax9.table(cellText=metrics_data[1:],
                     colLabels=metrics_data[0],
                     cellLoc='center',
                     loc='center',
                     bbox=[0, 0, 1, 1])
    
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2)
    
    # Style the table
    for i in range(len(metrics_data[0])):
        table[(0, i)].set_facecolor('#4A90E2')
        table[(0, i)].set_text_props(weight='bold', color='white')
    
    for i in range(1, len(metrics_data)):
        for j in range(len(metrics_data[0])):
            if i % 2 == 0:
                table[(i, j)].set_facecolor('#F0F0F0')
    
    # Format x-axis for time series plots
    for ax in [ax1, ax2, ax6, ax7]:
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
    
    return fig

def main():
    """Main function"""
    print("🔍 ETH 4h K-line Summary Report Generator")
    print("=" * 60)
    
    try:
        # Load data
        print("📊 Loading data...")
        df, analysis_data = load_data()
        print(f"✅ Data loaded: {len(df)} records")
        print(f"📅 Time range: {df.index.min()} to {df.index.max()}")
        
        # Create comprehensive report
        print("📊 Creating comprehensive report...")
        fig = create_comprehensive_report(df, analysis_data)
        
        # Save report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"assets/reports/4h_comprehensive_report_{timestamp}.png"
        fig.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close(fig)
        
        print(f"✅ Report saved: {output_path}")
        print("🎉 4h K-line Comprehensive Report Generated Successfully!")
        
    except Exception as e:
        print(f"❌ Error generating report: {e}")

if __name__ == "__main__":
    main()
