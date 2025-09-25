#!/usr/bin/env python3
"""
数据查看器 - 方便查看和分析生成的ETH HMA数据
"""
import pandas as pd
import numpy as np
from pathlib import Path
import argparse
import sys

def list_data_files(data_dir="data"):
    """列出所有数据文件"""
    data_path = Path(data_dir)
    if not data_path.exists():
        print(f"❌ 数据目录不存在: {data_path}")
        return []
    
    files = list(data_path.glob("*.parquet"))
    print(f"📁 找到 {len(files)} 个数据文件:")
    for i, file in enumerate(files, 1):
        file_size = file.stat().st_size / 1024 / 1024  # MB
        print(f"  {i}. {file.name} ({file_size:.2f} MB)")
    
    return files

def load_data(file_path):
    """加载Parquet数据文件"""
    try:
        df = pd.read_parquet(file_path)
        # 设置时间索引
        if 'open_time' in df.columns:
            df.set_index('open_time', inplace=True)
        return df
    except Exception as e:
        print(f"❌ 加载文件失败: {e}")
        return None

def show_basic_info(df, file_name):
    """显示数据基本信息"""
    print(f"\n📄 文件: {file_name}")
    print("=" * 60)
    print(f"📊 数据形状: {df.shape[0]:,} 行 × {df.shape[1]} 列")
    
    if isinstance(df.index, pd.DatetimeIndex):
        print(f"📅 时间范围: {df.index.min()} 到 {df.index.max()}")
        print(f"⏰ 时间跨度: {(df.index.max() - df.index.min()).days} 天")
    
    print(f"\n📋 列名:")
    for i, col in enumerate(df.columns, 1):
        print(f"  {i:2d}. {col}")
    
    print(f"\n📊 数据类型:")
    for col, dtype in df.dtypes.items():
        print(f"  {col:25s}: {dtype}")

def show_price_stats(df):
    """显示价格统计信息"""
    if 'close' not in df.columns:
        return
    
    print(f"\n💰 价格统计信息:")
    print("-" * 40)
    close_prices = df['close'].dropna()
    print(f"📈 最高价: ${close_prices.max():,.2f}")
    print(f"📉 最低价: ${close_prices.min():,.2f}")
    print(f"📊 平均价: ${close_prices.mean():,.2f}")
    print(f"📊 中位数: ${close_prices.median():,.2f}")
    print(f"📊 标准差: ${close_prices.std():,.2f}")
    
    # 价格变化统计
    if 'price_change' in df.columns:
        price_changes = df['price_change'].dropna()
        print(f"\n📈 价格变化统计:")
        print(f"  最大涨幅: {price_changes.max()*100:.2f}%")
        print(f"  最大跌幅: {price_changes.min()*100:.2f}%")
        print(f"  平均变化: {price_changes.mean()*100:.2f}%")

def show_technical_indicators(df):
    """显示技术指标信息"""
    technical_cols = [col for col in df.columns if any(x in col.lower() for x in ['hma', 'sma', 'volatility', 'deviation'])]
    
    if not technical_cols:
        print("\n🔍 未找到技术指标列")
        return
    
    print(f"\n🔍 技术指标信息:")
    print("-" * 40)
    
    for col in technical_cols:
        if col in df.columns:
            values = df[col].dropna()
            if len(values) > 0:
                print(f"  {col:15s}: 有效值 {len(values):,} 个")
                print(f"    {'':15s}  范围: {values.min():.2f} ~ {values.max():.2f}")
                print(f"    {'':15s}  平均: {values.mean():.2f}")

def show_sample_data(df, n=10):
    """显示样本数据"""
    print(f"\n🔍 前 {n} 行数据:")
    print("-" * 60)
    
    # 选择重要的列显示
    important_cols = ['open', 'high', 'low', 'close', 'volume']
    if 'HMA_45' in df.columns:
        important_cols.append('HMA_45')
    if 'SMA_20' in df.columns:
        important_cols.append('SMA_20')
    
    # 只显示存在的列
    display_cols = [col for col in important_cols if col in df.columns]
    
    if display_cols:
        print(df[display_cols].head(n).to_string())
    else:
        print(df.head(n).to_string())

def compare_raw_vs_processed():
    """比较原始数据和处理后数据"""
    data_dir = Path("data")
    
    # 找到1小时数据
    raw_1h = data_dir / "ETHUSDT_1h_raw_20250926_070421.parquet"
    processed_1h = data_dir / "ETHUSDT_1h_processed_20250926_070422.parquet"
    
    if raw_1h.exists() and processed_1h.exists():
        print("\n🔄 原始数据 vs 处理后数据对比 (1小时):")
        print("=" * 60)
        
        df_raw = load_data(raw_1h)
        df_processed = load_data(processed_1h)
        
        if df_raw is not None and df_processed is not None:
            print(f"原始数据列数: {df_raw.shape[1]}")
            print(f"处理后列数: {df_processed.shape[1]}")
            print(f"新增列数: {df_processed.shape[1] - df_raw.shape[1]}")
            
            new_cols = set(df_processed.columns) - set(df_raw.columns)
            if new_cols:
                print(f"新增列: {', '.join(new_cols)}")

def main():
    parser = argparse.ArgumentParser(description='ETH HMA 数据查看器')
    parser.add_argument('--file', '-f', help='指定要查看的文件名')
    parser.add_argument('--list', '-l', action='store_true', help='列出所有数据文件')
    parser.add_argument('--compare', '-c', action='store_true', help='比较原始数据和处理后数据')
    parser.add_argument('--rows', '-r', type=int, default=10, help='显示的行数 (默认: 10)')
    
    args = parser.parse_args()
    
    print("🔍 ETH HMA 数据查看器")
    print("=" * 50)
    
    if args.list:
        files = list_data_files()
        return
    
    if args.compare:
        compare_raw_vs_processed()
        return
    
    # 如果没有指定文件，列出所有文件让用户选择
    if not args.file:
        files = list_data_files()
        if not files:
            return
        
        print(f"\n请选择要查看的文件 (1-{len(files)}):")
        try:
            choice = int(input("输入文件编号: ")) - 1
            if 0 <= choice < len(files):
                selected_file = files[choice]
            else:
                print("❌ 无效选择")
                return
        except (ValueError, KeyboardInterrupt):
            print("❌ 取消操作")
            return
    else:
        selected_file = Path("data") / args.file
        if not selected_file.exists():
            print(f"❌ 文件不存在: {selected_file}")
            return
    
    # 加载并显示数据
    df = load_data(selected_file)
    if df is not None:
        show_basic_info(df, selected_file.name)
        show_price_stats(df)
        show_technical_indicators(df)
        show_sample_data(df, args.rows)

if __name__ == "__main__":
    main()
