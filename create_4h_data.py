#!/usr/bin/env python3
"""
从1h数据创建4h数据
"""

import pandas as pd
import numpy as np
from datetime import datetime
import sys
import os

# 添加src到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from eth_hma_analysis.core.math_brain import MathBrain

def create_4h_from_1h():
    """从1h数据创建4h数据"""
    print("🔄 从1h数据创建4h数据...")
    
    # 加载1h数据
    df_1h = pd.read_parquet('src/utils/data/ETHUSDT_1h_raw_20250926_214053.parquet')
    print(f"✅ 加载1h数据: {len(df_1h)} 条记录")
    
    # 设置时间索引
    df_1h['open_time'] = pd.to_datetime(df_1h['open_time'])
    df_1h.set_index('open_time', inplace=True)
    
    # 重采样为4h数据
    df_4h = df_1h.resample('4H').agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum',
        'quote_asset_volume': 'sum',
        'trades_count': 'sum',
        'taker_buy_base_asset_volume': 'sum',
        'taker_buy_quote_asset_volume': 'sum'
    }).dropna()
    
    # 添加close_time
    df_4h['close_time'] = df_4h.index + pd.Timedelta(hours=4)
    
    # 重新计算HMA
    math_brain = MathBrain(hma_period=45)
    df_4h['HMA_45'] = math_brain.calculate_hma(df_4h['close'], period=45)
    
    # 计算其他指标
    df_4h['price_change'] = df_4h['close'].pct_change()
    df_4h['hma_deviation'] = (df_4h['close'] - df_4h['HMA_45']) / df_4h['HMA_45'] * 100
    
    # 重置索引
    df_4h.reset_index(inplace=True)
    
    # 保存4h数据
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'ETHUSDT_4h_processed_{timestamp}.parquet'
    filepath = f'src/utils/data/{filename}'
    
    df_4h.to_parquet(filepath, index=False)
    print(f"✅ 保存4h数据: {filepath}")
    print(f"📊 4h数据记录数: {len(df_4h)}")
    print(f"📅 时间范围: {df_4h['open_time'].min()} 到 {df_4h['open_time'].max()}")
    
    return filepath

if __name__ == "__main__":
    create_4h_from_1h()
