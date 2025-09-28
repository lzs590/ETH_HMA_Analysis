#!/usr/bin/env python3
"""
检查duration_hours计算问题
"""

import json
from pathlib import Path
from datetime import datetime

def check_duration_calculation():
    """检查duration_hours计算问题"""
    print("🔍 检查duration_hours计算问题")
    print("=" * 50)
    
    # 加载最新分析结果
    reports_dir = Path('assets/reports')
    json_files = list(reports_dir.glob('trend_analysis_4h_*.json'))
    latest_file = max(json_files, key=lambda x: x.stat().st_mtime)
    
    with open(latest_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 检查第一个上涨趋势
    if 'uptrend_analysis' in data and 'intervals' in data['uptrend_analysis']:
        trend = data['uptrend_analysis']['intervals'][0]
        print(f"第一个上涨趋势:")
        print(f"  start_time: {trend.get('start_time', 'N/A')}")
        print(f"  end_time: {trend.get('end_time', 'N/A')}")
        print(f"  duration_hours: {trend.get('duration_hours', 'N/A')}")
        
        # 手动计算
        start_time = datetime.fromisoformat(trend.get('start_time', '').replace('Z', '+00:00'))
        end_time = datetime.fromisoformat(trend.get('end_time', '').replace('Z', '+00:00'))
        duration = (end_time - start_time).total_seconds() / 3600
        print(f"  手动计算duration: {duration:.2f} 小时")
        print(f"  差异: {abs(duration - trend.get('duration_hours', 0)):.2f}")
        
        # 检查更多趋势
        print(f"\n检查前5个趋势的duration_hours:")
        for i, trend in enumerate(data['uptrend_analysis']['intervals'][:5]):
            start_time = datetime.fromisoformat(trend.get('start_time', '').replace('Z', '+00:00'))
            end_time = datetime.fromisoformat(trend.get('end_time', '').replace('Z', '+00:00'))
            duration = (end_time - start_time).total_seconds() / 3600
            stored_duration = trend.get('duration_hours', 0)
            print(f"  趋势 {i+1}: 存储={stored_duration:.2f}h, 计算={duration:.2f}h, 差异={abs(duration - stored_duration):.2f}h")

if __name__ == "__main__":
    check_duration_calculation()
