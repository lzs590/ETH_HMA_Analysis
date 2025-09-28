#!/usr/bin/env python3
"""
Dashboard启动脚本
从项目根目录启动Streamlit Dashboard
"""

import subprocess
import sys
import os
from pathlib import Path

def start_dashboard():
    """启动Dashboard"""
    # 获取项目根目录
    project_root = Path(__file__).parent.parent
    
    # Dashboard文件路径
    dashboard_file = project_root / "dashboard" / "financial_dashboard_fixed.py"
    
    if not dashboard_file.exists():
        print(f"❌ 找不到Dashboard文件: {dashboard_file}")
        return False
    
    print(f"🚀 启动Dashboard: {dashboard_file}")
    print("📊 访问地址: http://localhost:8501")
    print("⏹️  按 Ctrl+C 停止服务")
    
    try:
        # 切换到项目根目录
        os.chdir(project_root)
        
        # 启动Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            str(dashboard_file),
            "--server.port", "8501",
            "--server.headless", "false"
        ])
    except KeyboardInterrupt:
        print("\n⏹️  Dashboard已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        return False
    
    return True

if __name__ == "__main__":
    start_dashboard()
