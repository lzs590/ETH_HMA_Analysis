#!/usr/bin/env python3
"""
Jupyter启动脚本
自动启动Jupyter Notebook并设置环境
"""

import subprocess
import sys
import os
from pathlib import Path

def start_jupyter():
    """启动Jupyter Notebook"""
    print("🚀 启动ETH HMA分析Jupyter环境...")
    
    # 检查当前目录
    current_dir = Path.cwd()
    print(f"📁 当前目录: {current_dir}")
    
    # 检查notebooks目录
    notebooks_dir = current_dir / "notebooks"
    if not notebooks_dir.exists():
        print("❌ notebooks目录不存在")
        return False
    
    print(f"📂 Notebooks目录: {notebooks_dir}")
    
    # 检查数据文件
    data_dir = current_dir / "src" / "utils" / "data"
    data_files = list(data_dir.glob("*.parquet"))
    print(f"📊 数据文件: {len(data_files)} 个")
    
    if not data_files:
        print("⚠️ 未找到数据文件，请先运行数据收集脚本")
        print("💡 运行命令: python scripts/main.py")
    
    # 启动Jupyter
    try:
        print("🔧 启动Jupyter Notebook...")
        print("📝 建议运行顺序:")
        print("  1. 00_快速开始.ipynb - 环境设置")
        print("  2. 01_数据加载与预处理.ipynb - 数据准备")
        print("  3. 02_4h级别策略分析.ipynb - 深度分析")
        print("\n🌐 Jupyter将在浏览器中打开...")
        
        # 启动Jupyter Notebook
        subprocess.run([
            sys.executable, "-m", "jupyter", "notebook",
            "--notebook-dir=notebooks",
            "--ip=127.0.0.1",
            "--port=8888",
            "--no-browser"
        ])
        
    except KeyboardInterrupt:
        print("\n👋 Jupyter已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        return False
    
    return True

if __name__ == "__main__":
    start_jupyter()