#!/usr/bin/env python3
"""
Unified Dashboard Launcher
启动整合的统一Dashboard
"""

import subprocess
import sys
from pathlib import Path
import psutil
import time

def kill_process_on_port(port):
    """关闭占用指定端口的进程"""
    try:
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                for conn in proc.connections():
                    if conn.laddr.port == port:
                        print(f"🔍 发现占用端口 {port} 的进程: {proc.info['name']} (PID: {proc.info['pid']})")
                        proc.kill()
                        print(f"✅ 已关闭进程 PID: {proc.info['pid']}")
                        time.sleep(2)
                        return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
    except Exception as e:
        print(f"⚠️ 关闭进程时出错: {e}")
    
    return False

def start_unified_dashboard():
    """启动统一Dashboard"""
    print("🔍 统一Dashboard启动器")
    print("=" * 60)
    
    # 关闭可能占用的端口
    print("🔍 检查并关闭占用端口...")
    kill_process_on_port(8501)
    kill_process_on_port(8504)
    kill_process_on_port(8505)
    
    time.sleep(3)
    
    # 启动统一Dashboard
    dashboard_script = Path(__file__).parent.parent / "dashboard" / "financial_dashboard_unified_cn.py"
    if not dashboard_script.exists():
        print(f"❌ Dashboard脚本未找到: {dashboard_script}")
        return False
    
    print(f"🚀 启动统一Dashboard: {dashboard_script}")
    print("📊 功能特点:")
    print("  - 整合专业版、深度分析版、高级专业版功能")
    print("  - 新增偏离值分析模块")
    print("  - 详细的数据统计分析")
    print("  - 原始数据展示和筛选")
    print("  - 相关性分析")
    print("  - 趋势分析")
    
    try:
        subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", 
            str(dashboard_script),
            "--server.port", "8501",
            "--server.headless", "true"
        ])
        
        print("✅ 统一Dashboard已启动")
        print("🌐 访问地址: http://localhost:8501")
        print("\n🎯 主要功能模块:")
        print("  📊 Overview - 总览和快速图表")
        print("  📊 Deviation Analysis - 偏离值分析")
        print("  📈 Advanced Statistics - 详细数据统计")
        print("  🔗 Correlation Analysis - 相关性分析")
        print("  📊 Trend Analysis - 趋势分析")
        print("  📋 Raw Data Display - 原始数据展示")
        
        return True
        
    except Exception as e:
        print(f"❌ 启动Dashboard失败: {e}")
        print("请确保Streamlit已安装 (pip install streamlit) 并且在您的PATH中。")
        return False

if __name__ == "__main__":
    if start_unified_dashboard():
        print(f"\n✅ 统一Dashboard启动成功!")
        print(f"📱 请在浏览器中访问: http://localhost:8501")
        print("🔄 如需重新分析数据，请运行: python scripts/trend_analysis.py --interval 4h")
    else:
        print(f"\n❌ 统一Dashboard启动失败")
        print("🔧 请检查Streamlit是否已安装: pip install streamlit")