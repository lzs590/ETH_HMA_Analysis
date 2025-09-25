#!/usr/bin/env python3
"""
启动Jupyter Notebook的辅助脚本
"""
import subprocess
import sys
import os
from pathlib import Path

def check_jupyter():
    """检查Jupyter是否已安装"""
    try:
        import jupyter
        return True
    except ImportError:
        return False

def install_jupyter():
    """安装Jupyter"""
    print("📦 正在安装Jupyter Notebook...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "jupyter", "matplotlib", "seaborn"])
        print("✅ Jupyter安装完成")
        return True
    except subprocess.CalledProcessError:
        print("❌ Jupyter安装失败")
        return False

def start_jupyter():
    """启动Jupyter Notebook"""
    print("🚀 启动Jupyter Notebook...")
    print("📝 请在浏览器中打开显示的URL")
    print("📁 打开 ETH_HMA_Analysis.ipynb 文件开始分析")
    print("=" * 50)
    
    try:
        # 切换到项目目录
        project_dir = Path(__file__).parent
        os.chdir(project_dir)
        
        # 启动Jupyter
        subprocess.run(["jupyter", "notebook"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ 启动Jupyter失败: {e}")
    except KeyboardInterrupt:
        print("\n⏹️  Jupyter已停止")

def main():
    print("🔍 ETH HMA 数据分析 - Jupyter启动器")
    print("=" * 50)
    
    # 检查Jupyter是否已安装
    if not check_jupyter():
        print("❌ Jupyter未安装")
        choice = input("是否安装Jupyter? (y/n): ").lower().strip()
        if choice == 'y':
            if not install_jupyter():
                return
        else:
            print("请手动安装Jupyter: pip install jupyter matplotlib seaborn")
            return
    
    # 检查Notebook文件是否存在
    notebook_file = Path("ETH_HMA_Analysis.ipynb")
    if not notebook_file.exists():
        print("❌ 找不到ETH_HMA_Analysis.ipynb文件")
        return
    
    print("✅ 环境检查通过")
    print("📊 准备启动数据分析环境...")
    
    # 启动Jupyter
    start_jupyter()

if __name__ == "__main__":
    main()
