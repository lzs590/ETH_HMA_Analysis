#!/usr/bin/env python3
"""
数据分析脚本 - 分析ETH HMA数据的统计特征和趋势
"""
import pandas as pd
import numpy as np
from pathlib import Path

def load_processed_data():
    """加载处理后的数据"""
    data_dir = Path("data")
    
    # 加载1小时和4小时的处理后数据
    # 自动查找最新的处理文件
    processed_files = list(data_dir.glob("ETHUSDT_*_processed_*.parquet"))
    
    files = {}
    for file_path in processed_files:
        if '1h' in file_path.name:
            files['1h'] = file_path
        elif '4h' in file_path.name:
            files['4h'] = file_path
    
    data = {}
    for interval, file_path in files.items():
        if file_path.exists():
            df = pd.read_parquet(file_path)
            df.set_index('open_time', inplace=True)
            data[interval] = df
            print(f"✅ 加载 {interval} 数据: {len(df):,} 条记录")
        else:
            print(f"❌ 文件不存在: {file_path}")
    
    return data

def analyze_price_trends(data):
    """分析价格趋势"""
    print("\n📈 价格趋势分析")
    print("=" * 50)
    
    for interval, df in data.items():
        print(f"\n⏰ {interval} 数据:")
        print("-" * 30)
        
        # 基本价格统计
        close_prices = df['close'].dropna()
        print(f"📊 价格范围: ${close_prices.min():,.2f} - ${close_prices.max():,.2f}")
        print(f"📊 平均价格: ${close_prices.mean():,.2f}")
        print(f"📊 价格标准差: ${close_prices.std():,.2f}")
        
        # 价格变化统计
        if 'price_change' in df.columns:
            price_changes = df['price_change'].dropna()
            print(f"📈 最大涨幅: {price_changes.max()*100:.2f}%")
            print(f"📉 最大跌幅: {price_changes.min()*100:.2f}%")
            print(f"📊 平均变化: {price_changes.mean()*100:.4f}%")
        
        # 价格变化分析
        if 'price_change' in df.columns:
            price_changes = df['price_change'].dropna()
            print(f"📊 平均价格变化: {price_changes.mean()*100:.4f}%")
            print(f"📊 价格变化标准差: {price_changes.std()*100:.4f}%")

def analyze_technical_indicators(data):
    """分析技术指标"""
    print("\n🔍 技术指标分析")
    print("=" * 50)
    
    for interval, df in data.items():
        print(f"\n⏰ {interval} 数据:")
        print("-" * 30)
        
        # HMA分析
        if 'HMA_45' in df.columns:
            hma = df['HMA_45'].dropna()
            print(f"🔢 HMA_45 统计:")
            print(f"   有效值: {len(hma):,} 个")
            print(f"   范围: {hma.min():.2f} - {hma.max():.2f}")
            print(f"   平均: {hma.mean():.2f}")
            
            # HMA与价格的关系
            if 'hma_deviation' in df.columns:
                deviation = df['hma_deviation'].dropna()
                print(f"   与价格偏离度: {deviation.mean():.2f}% (平均)")
                print(f"   最大正偏离: {deviation.max():.2f}%")
                print(f"   最大负偏离: {deviation.min():.2f}%")

def analyze_trading_volume(data):
    """分析交易量"""
    print("\n📊 交易量分析")
    print("=" * 50)
    
    for interval, df in data.items():
        print(f"\n⏰ {interval} 数据:")
        print("-" * 30)
        
        volume = df['volume'].dropna()
        print(f"📊 平均交易量: {volume.mean():,.2f}")
        print(f"📊 最大交易量: {volume.max():,.2f}")
        print(f"📊 最小交易量: {volume.min():,.2f}")
        print(f"📊 交易量标准差: {volume.std():,.2f}")
        
        # 交易量趋势
        if len(volume) > 100:
            recent_volume = volume.tail(100).mean()
            early_volume = volume.head(100).mean()
            volume_change = (recent_volume - early_volume) / early_volume * 100
            print(f"📈 交易量变化: {volume_change:+.2f}% (最近100期 vs 最早100期)")

def find_significant_events(data):
    """找出重要事件"""
    print("\n🎯 重要事件分析")
    print("=" * 50)
    
    for interval, df in data.items():
        print(f"\n⏰ {interval} 数据:")
        print("-" * 30)
        
        # 最大价格变化
        if 'price_change' in df.columns:
            price_changes = df['price_change'].dropna()
            max_gain_idx = price_changes.idxmax()
            max_loss_idx = price_changes.idxmin()
            
            print(f"📈 最大涨幅: {price_changes.max()*100:.2f}%")
            print(f"   时间: {max_gain_idx}")
            print(f"   价格: ${df.loc[max_gain_idx, 'close']:.2f}")
            
            print(f"📉 最大跌幅: {price_changes.min()*100:.2f}%")
            print(f"   时间: {max_loss_idx}")
            print(f"   价格: ${df.loc[max_loss_idx, 'close']:.2f}")
        
        # 最高和最低价格
        close_prices = df['close'].dropna()
        highest_idx = close_prices.idxmax()
        lowest_idx = close_prices.idxmin()
        
        print(f"🏔️  历史最高: ${close_prices.max():.2f}")
        print(f"   时间: {highest_idx}")
        
        print(f"🏔️  历史最低: ${close_prices.min():.2f}")
        print(f"   时间: {lowest_idx}")

def generate_summary_report(data):
    """生成总结报告"""
    print("\n📋 数据总结报告")
    print("=" * 50)
    
    total_records = sum(len(df) for df in data.values())
    print(f"📊 总记录数: {total_records:,}")
    print(f"📁 数据文件: {len(data)} 个")
    
    # 时间跨度
    all_dates = []
    for df in data.values():
        all_dates.extend([df.index.min(), df.index.max()])
    
    if all_dates:
        min_date = min(all_dates)
        max_date = max(all_dates)
        print(f"📅 时间跨度: {min_date} 到 {max_date}")
        print(f"⏰ 总天数: {(max_date - min_date).days} 天")
    
    # 数据质量
    for interval, df in data.items():
        missing_data = df.isnull().sum().sum()
        total_cells = df.shape[0] * df.shape[1]
        completeness = (1 - missing_data / total_cells) * 100
        print(f"✅ {interval} 数据完整性: {completeness:.2f}%")

def main():
    """主函数"""
    print("🔍 ETH HMA 数据分析器")
    print("=" * 50)
    
    # 加载数据
    data = load_processed_data()
    
    if not data:
        print("❌ 没有找到可分析的数据文件")
        return
    
    # 执行各种分析
    analyze_price_trends(data)
    analyze_technical_indicators(data)
    analyze_trading_volume(data)
    find_significant_events(data)
    generate_summary_report(data)
    
    print("\n✅ 分析完成！")
    print("\n💡 提示: 您可以使用以下命令查看详细数据:")
    print("   python3 data_viewer.py --list")
    print("   python3 data_viewer.py --file <文件名>")

if __name__ == "__main__":
    main()
