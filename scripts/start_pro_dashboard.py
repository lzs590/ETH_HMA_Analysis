#!/usr/bin/env python3
"""
专业级Dashboard启动脚本
"""

import subprocess
import sys
from pathlib import Path

def start_pro_dashboard():
    """启动专业级Dashboard"""
    dashboard_script = Path("dashboard/financial_dashboard_pro.py")
    
    if not dashboard_script.exists():
        print(f"❌ Dashboard脚本未找到: {dashboard_script}")
        return False
    
    print(f"🚀 启动专业级Dashboard: {dashboard_script}")
    
    try:
        # 启动Streamlit
        subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", 
            str(dashboard_script),
            "--server.port", "8503",
            "--server.headless", "true"
        ])
        
        print("✅ 专业级Dashboard已启动")
        print("🌐 访问地址: http://localhost:8503")
        print("📊 专业功能:")
        print("  - 华尔街级别数据分析")
        print("  - 高级风险收益分析矩阵")
        print("  - 时间序列深度分析")
        print("  - 数据洞察面板")
        print("  - 专业级筛选器")
        print("  - 趋势强度热力图")
        print("  - 波动率分析")
        print("  - 风险收益比分析")
        
        return True
        
    except Exception as e:
        print(f"❌ 启动Dashboard失败: {e}")
        return False

if __name__ == "__main__":
    start_pro_dashboard()
