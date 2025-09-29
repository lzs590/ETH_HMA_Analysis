#!/usr/bin/env python3
"""
4h K-line Data Matplotlib Report Generator
Generate professional English matplotlib reports for 4h K-line data analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import json
from pathlib import Path
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Set matplotlib style for professional reports
try:
    plt.style.use('seaborn-v0_8')
except OSError:
    plt.style.use('seaborn')
plt.rcParams.update({
    'font.family': 'Arial',
    'font.size': 10,
    'axes.titlesize': 12,
    'axes.labelsize': 10,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'figure.titlesize': 14,
    'axes.grid': True,
    'grid.alpha': 0.3,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight'
})

class KlineReportGenerator:
    """Professional 4h K-line Data Report Generator"""
    
    def __init__(self, data_dir="assets/data", reports_dir="assets/reports"):
        self.data_dir = Path(data_dir)
        self.reports_dir = Path(reports_dir)
        self.reports_dir.mkdir(exist_ok=True)
        
    def load_4h_data(self):
        """Load the latest 4h processed data"""
        print("📊 Loading 4h K-line data...")
        
        # Find latest 4h processed data
        data_files = list(self.data_dir.glob("ETHUSDT_4h_processed_*.parquet"))
        if not data_files:
            raise FileNotFoundError("No 4h processed data found")
        
        latest_file = max(data_files, key=lambda f: f.stat().st_mtime)
        print(f"✅ Loading: {latest_file.name}")
        
        df = pd.read_parquet(latest_file)
        df['open_time'] = pd.to_datetime(df['open_time'])
        df.set_index('open_time', inplace=True)
        
        print(f"📈 Data loaded: {len(df)} records")
        print(f"📅 Time range: {df.index.min()} to {df.index.max()}")
        
        return df
    
    def load_analysis_data(self):
        """Load the latest 4h analysis results"""
        print("📊 Loading 4h analysis results...")
        
        # Find latest 4h analysis JSON
        json_files = list(self.reports_dir.glob("trend_analysis_4h_*.json"))
        if not json_files:
            raise FileNotFoundError("No 4h analysis results found")
        
        latest_file = max(json_files, key=lambda f: f.stat().st_mtime)
        print(f"✅ Loading analysis: {latest_file.name}")
        
        with open(latest_file, 'r', encoding='utf-8') as f:
            analysis_data = json.load(f)
        
        return analysis_data
    
    def create_price_analysis_plot(self, df):
        """Create comprehensive price analysis plot"""
        fig, axes = plt.subplots(3, 1, figsize=(15, 12))
        fig.suptitle('ETH 4h K-line Price Analysis', fontsize=16, fontweight='bold')
        
        # 1. Price and HMA
        ax1 = axes[0]
        ax1.plot(df.index, df['close'], label='Close Price', linewidth=1.5, color='#2E86AB')
        ax1.plot(df.index, df['HMA_45'], label='HMA(45)', linewidth=2, color='#F24236')
        ax1.fill_between(df.index, df['low'], df['high'], alpha=0.1, color='gray', label='Price Range')
        ax1.set_title('Price Movement and Hull Moving Average')
        ax1.set_ylabel('Price (USDT)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. Volume Analysis
        ax2 = axes[1]
        ax2.bar(df.index, df['volume'], alpha=0.7, color='#A23B72', width=0.8)
        ax2.set_title('Trading Volume')
        ax2.set_ylabel('Volume')
        ax2.grid(True, alpha=0.3)
        
        # 3. Price Deviation from HMA
        ax3 = axes[2]
        deviation = ((df['close'] - df['HMA_45']) / df['HMA_45'] * 100)
        ax3.plot(df.index, deviation, color='#F18F01', linewidth=1.5)
        ax3.axhline(y=0, color='black', linestyle='--', alpha=0.5)
        ax3.fill_between(df.index, deviation, 0, alpha=0.3, color='#F18F01')
        ax3.set_title('Price Deviation from HMA (%)')
        ax3.set_ylabel('Deviation (%)')
        ax3.set_xlabel('Time')
        ax3.grid(True, alpha=0.3)
        
        # Format x-axis
        for ax in axes:
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
            ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        
        plt.tight_layout()
        return fig
    
    def create_trend_analysis_plot(self, analysis_data):
        """Create trend analysis visualization"""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('4h Trend Analysis Report', fontsize=16, fontweight='bold')
        
        # Extract trend data
        uptrend_intervals = analysis_data.get('uptrend_analysis', {}).get('intervals', [])
        downtrend_intervals = analysis_data.get('downtrend_analysis', {}).get('intervals', [])
        
        # 1. Trend Distribution
        ax1 = axes[0, 0]
        trend_counts = [len(uptrend_intervals), len(downtrend_intervals)]
        trend_labels = ['Uptrends', 'Downtrends']
        colors = ['#2E8B57', '#DC143C']
        
        bars = ax1.bar(trend_labels, trend_counts, color=colors, alpha=0.8)
        ax1.set_title('Trend Distribution')
        ax1.set_ylabel('Number of Trends')
        
        # Add value labels on bars
        for bar, count in zip(bars, trend_counts):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                    str(count), ha='center', va='bottom', fontweight='bold')
        
        # 2. Profit Distribution
        ax2 = axes[0, 1]
        uptrend_profits = [interval.get('long_ideal_profit', 0) for interval in uptrend_intervals]
        downtrend_profits = [interval.get('short_ideal_profit', 0) for interval in downtrend_intervals]
        
        all_profits = uptrend_profits + downtrend_profits
        ax2.hist(all_profits, bins=20, alpha=0.7, color='#4A90E2', edgecolor='black')
        ax2.axvline(np.mean(all_profits), color='red', linestyle='--', 
                   label=f'Mean: {np.mean(all_profits):.2f}%')
        ax2.set_title('Profit Distribution')
        ax2.set_xlabel('Profit (%)')
        ax2.set_ylabel('Frequency')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 3. Risk vs Reward
        ax3 = axes[1, 0]
        uptrend_risks = [interval.get('long_risk_loss', 0) for interval in uptrend_intervals]
        downtrend_risks = [interval.get('max_rally', 0) for interval in downtrend_intervals]
        
        all_risks = uptrend_risks + downtrend_risks
        ax3.scatter(all_risks, all_profits, alpha=0.6, s=50, color='#FF6B6B')
        ax3.set_title('Risk vs Reward Analysis')
        ax3.set_xlabel('Risk Loss (%)')
        ax3.set_ylabel('Ideal Profit (%)')
        ax3.grid(True, alpha=0.3)
        
        # Add correlation line
        if len(all_risks) > 1:
            z = np.polyfit(all_risks, all_profits, 1)
            p = np.poly1d(z)
            ax3.plot(all_risks, p(all_risks), "r--", alpha=0.8, linewidth=2)
        
        # 4. Duration Analysis
        ax4 = axes[1, 1]
        uptrend_durations = [interval.get('duration_hours', 0) for interval in uptrend_intervals]
        downtrend_durations = [interval.get('duration_hours', 0) for interval in downtrend_intervals]
        
        all_durations = uptrend_durations + downtrend_durations
        ax4.hist(all_durations, bins=15, alpha=0.7, color='#9B59B6', edgecolor='black')
        ax4.axvline(np.mean(all_durations), color='red', linestyle='--',
                   label=f'Mean: {np.mean(all_durations):.1f}h')
        ax4.set_title('Trend Duration Distribution')
        ax4.set_xlabel('Duration (hours)')
        ax4.set_ylabel('Frequency')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def create_performance_metrics_table(self, analysis_data):
        """Create performance metrics table"""
        fig, ax = plt.subplots(figsize=(14, 8))
        fig.suptitle('4h Strategy Performance Metrics', fontsize=16, fontweight='bold')
        
        # Extract metrics
        uptrend_analysis = analysis_data.get('uptrend_analysis', {})
        downtrend_analysis = analysis_data.get('downtrend_analysis', {})
        
        # Prepare data for table
        metrics_data = {
            'Metric': [
                'Total Uptrends',
                'Total Downtrends',
                'Average Uptrend Profit (%)',
                'Average Downtrend Profit (%)',
                'Average Uptrend Risk (%)',
                'Average Downtrend Risk (%)',
                'Average Uptrend Duration (h)',
                'Average Downtrend Duration (h)',
                'Win Rate (Uptrends)',
                'Win Rate (Downtrends)',
                'Risk-Reward Ratio (Uptrends)',
                'Risk-Reward Ratio (Downtrends)'
            ],
            'Value': [
                uptrend_analysis.get('total_intervals', 0),
                downtrend_analysis.get('total_intervals', 0),
                f"{uptrend_analysis.get('avg_ideal_profit', 0):.2f}",
                f"{downtrend_analysis.get('avg_ideal_profit', 0):.2f}",
                f"{uptrend_analysis.get('avg_risk_loss', 0):.2f}",
                f"{downtrend_analysis.get('avg_risk_loss', 0):.2f}",
                f"{uptrend_analysis.get('avg_duration_hours', 0):.1f}",
                f"{downtrend_analysis.get('avg_duration_hours', 0):.1f}",
                f"{uptrend_analysis.get('win_rate', 0):.1f}%",
                f"{downtrend_analysis.get('win_rate', 0):.1f}%",
                f"{uptrend_analysis.get('avg_risk_reward_ratio', 0):.2f}",
                f"{downtrend_analysis.get('avg_risk_reward_ratio', 0):.2f}"
            ]
        }
        
        # Create table
        table_data = list(zip(metrics_data['Metric'], metrics_data['Value']))
        table = ax.table(cellText=table_data,
                        colLabels=['Performance Metric', 'Value'],
                        cellLoc='left',
                        loc='center',
                        bbox=[0, 0, 1, 1])
        
        # Style the table
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 2)
        
        # Color code the header
        for i in range(2):
            table[(0, i)].set_facecolor('#4A90E2')
            table[(0, i)].set_text_props(weight='bold', color='white')
        
        # Color code alternating rows
        for i in range(1, len(table_data) + 1):
            for j in range(2):
                if i % 2 == 0:
                    table[(i, j)].set_facecolor('#F0F0F0')
        
        ax.axis('off')
        return fig
    
    def create_volatility_analysis_plot(self, df):
        """Create volatility analysis plot"""
        fig, axes = plt.subplots(2, 2, figsize=(16, 10))
        fig.suptitle('4h Volatility Analysis', fontsize=16, fontweight='bold')
        
        # Calculate volatility metrics
        df['returns'] = df['close'].pct_change()
        df['volatility_24h'] = df['returns'].rolling(window=6).std() * np.sqrt(6) * 100  # 24h volatility
        df['volatility_7d'] = df['returns'].rolling(window=42).std() * np.sqrt(42) * 100  # 7d volatility
        
        # 1. Price vs Volatility
        ax1 = axes[0, 0]
        scatter = ax1.scatter(df.index, df['close'], c=df['volatility_24h'], 
                            cmap='viridis', alpha=0.6, s=20)
        ax1.set_title('Price vs 24h Volatility')
        ax1.set_ylabel('Price (USDT)')
        plt.colorbar(scatter, ax=ax1, label='Volatility (%)')
        
        # 2. Volatility Time Series
        ax2 = axes[0, 1]
        ax2.plot(df.index, df['volatility_24h'], label='24h Volatility', alpha=0.8, color='#E74C3C')
        ax2.plot(df.index, df['volatility_7d'], label='7d Volatility', alpha=0.8, color='#3498DB')
        ax2.set_title('Volatility Over Time')
        ax2.set_ylabel('Volatility (%)')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 3. Volatility Distribution
        ax3 = axes[1, 0]
        ax3.hist(df['volatility_24h'].dropna(), bins=30, alpha=0.7, color='#9B59B6', edgecolor='black')
        ax3.axvline(df['volatility_24h'].mean(), color='red', linestyle='--',
                   label=f'Mean: {df["volatility_24h"].mean():.2f}%')
        ax3.set_title('24h Volatility Distribution')
        ax3.set_xlabel('Volatility (%)')
        ax3.set_ylabel('Frequency')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # 4. Volume vs Volatility
        ax4 = axes[1, 1]
        ax4.scatter(df['volume'], df['volatility_24h'], alpha=0.6, color='#F39C12', s=20)
        ax4.set_title('Volume vs Volatility')
        ax4.set_xlabel('Volume')
        ax4.set_ylabel('24h Volatility (%)')
        ax4.grid(True, alpha=0.3)
        
        # Format x-axis
        for ax in axes.flat:
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
            ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        
        plt.tight_layout()
        return fig
    
    def create_correlation_heatmap(self, df):
        """Create correlation heatmap"""
        fig, ax = plt.subplots(figsize=(10, 8))
        fig.suptitle('4h K-line Data Correlation Matrix', fontsize=16, fontweight='bold')
        
        # Select relevant columns for correlation
        correlation_data = df[['open', 'high', 'low', 'close', 'volume', 'HMA_45']].copy()
        correlation_data['price_change'] = df['close'].pct_change()
        correlation_data['hma_deviation'] = (df['close'] - df['HMA_45']) / df['HMA_45']
        
        # Calculate correlation matrix
        corr_matrix = correlation_data.corr()
        
        # Create heatmap
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
        sns.heatmap(corr_matrix, mask=mask, annot=True, cmap='RdBu_r', center=0,
                   square=True, linewidths=0.5, cbar_kws={"shrink": 0.8})
        
        ax.set_title('Correlation Analysis')
        plt.tight_layout()
        return fig
    
    def generate_complete_report(self):
        """Generate complete 4h K-line report"""
        print("🚀 Generating 4h K-line Matplotlib Report...")
        print("=" * 60)
        
        try:
            # Load data
            df = self.load_4h_data()
            analysis_data = self.load_analysis_data()
            
            # Generate timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Create all plots
            print("📊 Creating price analysis plot...")
            fig1 = self.create_price_analysis_plot(df)
            fig1.savefig(self.reports_dir / f"4h_price_analysis_{timestamp}.png", dpi=300, bbox_inches='tight')
            plt.close(fig1)
            
            print("📊 Creating trend analysis plot...")
            fig2 = self.create_trend_analysis_plot(analysis_data)
            fig2.savefig(self.reports_dir / f"4h_trend_analysis_{timestamp}.png", dpi=300, bbox_inches='tight')
            plt.close(fig2)
            
            print("📊 Creating performance metrics table...")
            fig3 = self.create_performance_metrics_table(analysis_data)
            fig3.savefig(self.reports_dir / f"4h_performance_metrics_{timestamp}.png", dpi=300, bbox_inches='tight')
            plt.close(fig3)
            
            print("📊 Creating volatility analysis plot...")
            fig4 = self.create_volatility_analysis_plot(df)
            fig4.savefig(self.reports_dir / f"4h_volatility_analysis_{timestamp}.png", dpi=300, bbox_inches='tight')
            plt.close(fig4)
            
            print("📊 Creating correlation heatmap...")
            fig5 = self.create_correlation_heatmap(df)
            fig5.savefig(self.reports_dir / f"4h_correlation_heatmap_{timestamp}.png", dpi=300, bbox_inches='tight')
            plt.close(fig5)
            
            print("✅ Report generation completed!")
            print(f"📁 Reports saved in: {self.reports_dir}")
            print(f"🕒 Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error generating report: {e}")
            return False

def main():
    """Main function"""
    print("🔍 ETH 4h K-line Matplotlib Report Generator")
    print("=" * 60)
    
    # Initialize generator
    generator = KlineReportGenerator()
    
    # Generate complete report
    success = generator.generate_complete_report()
    
    if success:
        print("\n🎉 4h K-line Matplotlib Report Generated Successfully!")
        print("📊 Generated Reports:")
        print("  - Price Analysis Plot")
        print("  - Trend Analysis Plot") 
        print("  - Performance Metrics Table")
        print("  - Volatility Analysis Plot")
        print("  - Correlation Heatmap")
    else:
        print("\n❌ Report generation failed!")

if __name__ == "__main__":
    main()
