#!/usr/bin/env python3
"""
多版本Dashboard启动器
同时启动多个版本的Dashboard，使用不同端口
"""

import subprocess
import sys
import time
import psutil
from pathlib import Path

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

def start_dashboard(dashboard_type, port):
    """启动指定类型的Dashboard"""
    dashboard_scripts = {
        "pro": "dashboard/financial_dashboard_pro.py",
        "matplotlib": "dashboard/financial_dashboard_matplotlib.py",
        "v2": "dashboard/financial_dashboard_v2.py",
        "insights": "dashboard/financial_dashboard_insights.py",
        "advanced": "dashboard/financial_dashboard_advanced.py"
    }
    
    dashboard_script = dashboard_scripts.get(dashboard_type, "dashboard/financial_dashboard_pro.py")
    script_path = Path(dashboard_script)
    
    if not script_path.exists():
        print(f"❌ Dashboard脚本未找到: {script_path}")
        return False
    
    print(f"🚀 启动 {dashboard_type.upper()} Dashboard: {script_path} (端口: {port})")
    
    try:
        # 启动Streamlit
        subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", 
            str(script_path),
            "--server.port", str(port),
            "--server.headless", "true"
        ])
        
        print(f"✅ {dashboard_type.upper()} Dashboard已启动")
        return True
        
    except Exception as e:
        print(f"❌ 启动{dashboard_type.upper()} Dashboard失败: {e}")
        return False

def start_all_dashboards():
    """启动所有版本的Dashboard"""
    print("🔍 多版本Dashboard启动器")
    print("=" * 60)
    
    # Dashboard配置
    dashboards = {
        "pro": {"port": 8501, "name": "专业版", "desc": "华尔街级别数据分析"},
        "matplotlib": {"port": 8502, "name": "Matplotlib版", "desc": "专业数据分析表格"},
        "v2": {"port": 8503, "name": "智能版", "desc": "自动检测最新分析结果"},
        "insights": {"port": 8504, "name": "深度分析版", "desc": "策略效率深度分析"},
        "advanced": {"port": 8505, "name": "高级专业版", "desc": "原始数据展示+置信指数算法"}
    }
    
    # 关闭可能占用的端口
    print("🔍 检查并关闭占用端口...")
    for dashboard_type, config in dashboards.items():
        kill_process_on_port(config["port"])
    
    time.sleep(3)
    
    # 启动所有Dashboard
    print(f"\n🚀 启动所有Dashboard...")
    success_count = 0
    
    for dashboard_type, config in dashboards.items():
        if start_dashboard(dashboard_type, config["port"]):
            success_count += 1
            time.sleep(2)  # 避免端口冲突
    
    # 显示访问信息
    print(f"\n✅ 成功启动 {success_count}/{len(dashboards)} 个Dashboard")
    print("\n🌐 访问地址:")
    print("=" * 60)
    
    for dashboard_type, config in dashboards.items():
        print(f"📊 {config['name']} ({config['desc']})")
        print(f"   地址: http://localhost:{config['port']}")
        print()
    
    print("💡 使用建议:")
    print("- 专业版: 适合华尔街级别分析")
    print("- Matplotlib版: 适合数据分析表格")
    print("- 智能版: 适合自动数据检测")
    print("- 深度分析版: 适合策略效率分析")
    print("- 高级专业版: 适合原始数据展示和置信指数分析")
    
    print(f"\n🔄 如需单独启动某个版本，请运行:")
    print("  python scripts/start_unified_dashboard.py [版本名]")

def start_selected_dashboards(selected_types):
    """启动选定的Dashboard版本"""
    print("🔍 选定版本Dashboard启动器")
    print("=" * 60)
    
    # Dashboard配置
    dashboards = {
        "pro": {"port": 8501, "name": "专业版", "desc": "华尔街级别数据分析"},
        "matplotlib": {"port": 8502, "name": "Matplotlib版", "desc": "专业数据分析表格"},
        "v2": {"port": 8503, "name": "智能版", "desc": "自动检测最新分析结果"},
        "insights": {"port": 8504, "name": "深度分析版", "desc": "策略效率深度分析"},
        "advanced": {"port": 8505, "name": "高级专业版", "desc": "原始数据展示+置信指数算法"}
    }
    
    # 关闭可能占用的端口
    print("🔍 检查并关闭占用端口...")
    for dashboard_type in selected_types:
        if dashboard_type in dashboards:
            kill_process_on_port(dashboards[dashboard_type]["port"])
    
    time.sleep(3)
    
    # 启动选定的Dashboard
    print(f"\n🚀 启动选定的Dashboard...")
    success_count = 0
    
    for dashboard_type in selected_types:
        if dashboard_type in dashboards:
            config = dashboards[dashboard_type]
            if start_dashboard(dashboard_type, config["port"]):
                success_count += 1
                time.sleep(2)
    
    # 显示访问信息
    print(f"\n✅ 成功启动 {success_count}/{len(selected_types)} 个Dashboard")
    print("\n🌐 访问地址:")
    print("=" * 60)
    
    for dashboard_type in selected_types:
        if dashboard_type in dashboards:
            config = dashboards[dashboard_type]
            print(f"📊 {config['name']} ({config['desc']})")
            print(f"   地址: http://localhost:{config['port']}")
            print()

def main():
    """主函数"""
    if len(sys.argv) > 1:
        # 启动选定的版本
        selected_types = sys.argv[1:]
        start_selected_dashboards(selected_types)
    else:
        # 启动所有版本
        start_all_dashboards()

if __name__ == "__main__":
    main()
