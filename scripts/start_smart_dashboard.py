#!/usr/bin/env python3
"""
智能Dashboard启动脚本
自动检测最新分析结果并启动Dashboard
"""

import subprocess
import sys
import os
from pathlib import Path
import json
import glob

def find_latest_analysis():
    """查找最新的分析结果"""
    reports_dir = Path("assets/reports")
    
    # 查找所有4h分析结果
    json_files = list(reports_dir.glob("trend_analysis_4h_*.json"))
    
    if not json_files:
        print("❌ 未找到4h分析结果文件")
        print("请先运行分析生成数据:")
        print("  python scripts/trend_analysis.py --interval 4h")
        return False
    
    # 选择最新的文件
    latest_file = max(json_files, key=lambda x: x.stat().st_mtime)
    print(f"✅ 找到最新分析结果: {latest_file.name}")
    
    # 检查数据完整性
    try:
        with open(latest_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 检查关键数据
        has_uptrend = 'uptrend_analysis' in data and 'intervals' in data['uptrend_analysis']
        has_downtrend = 'downtrend_analysis' in data and 'intervals' in data['downtrend_analysis']
        
        if not has_uptrend and not has_downtrend:
            print("❌ 分析结果文件格式不正确")
            return False
        
        uptrend_count = len(data['uptrend_analysis']['intervals']) if has_uptrend else 0
        downtrend_count = len(data['downtrend_analysis']['intervals']) if has_downtrend else 0
        
        print(f"📊 数据统计:")
        print(f"  - 上涨趋势: {uptrend_count} 个")
        print(f"  - 下跌趋势: {downtrend_count} 个")
        print(f"  - 总计: {uptrend_count + downtrend_count} 个趋势")
        
        return True
        
    except Exception as e:
        print(f"❌ 读取分析结果失败: {e}")
        return False

def start_dashboard():
    """启动智能Dashboard"""
    dashboard_script = Path("dashboard/financial_dashboard_v2.py")
    
    if not dashboard_script.exists():
        print(f"❌ Dashboard脚本未找到: {dashboard_script}")
        return False
    
    print(f"🚀 启动智能Dashboard: {dashboard_script}")
    
    try:
        # 启动Streamlit
        subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", 
            str(dashboard_script),
            "--server.port", "8501",
            "--server.headless", "true"
        ])
        
        print("✅ Dashboard已启动")
        print("🌐 访问地址: http://localhost:8501")
        print("📊 功能特点:")
        print("  - 自动检测最新分析结果")
        print("  - 无需手动创建CSV文件")
        print("  - 实时数据状态显示")
        print("  - 智能数据转换")
        
        return True
        
    except Exception as e:
        print(f"❌ 启动Dashboard失败: {e}")
        return False

def main():
    """主函数"""
    print("🔍 智能Dashboard启动器")
    print("=" * 50)
    
    # 检查分析结果
    if not find_latest_analysis():
        print("\n💡 解决方案:")
        print("1. 运行数据收集: python scripts/main.py")
        print("2. 运行趋势分析: python scripts/trend_analysis.py --interval 4h")
        print("3. 重新启动Dashboard: python scripts/start_smart_dashboard.py")
        return
    
    print("\n🚀 启动Dashboard...")
    
    # 启动Dashboard
    if start_dashboard():
        print("\n✅ Dashboard启动成功!")
        print("📱 请在浏览器中访问: http://localhost:8501")
        print("🔄 如需重新分析数据，请运行: python scripts/trend_analysis.py --interval 4h")
    else:
        print("\n❌ Dashboard启动失败")
        print("🔧 请检查Streamlit是否已安装: pip install streamlit")

if __name__ == "__main__":
    main()
