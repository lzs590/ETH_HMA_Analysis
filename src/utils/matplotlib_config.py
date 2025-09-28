"""
matplotlib配置文件管理器
统一管理项目中的matplotlib设置
"""

import matplotlib
import matplotlib.pyplot as plt
import os
from pathlib import Path

class MatplotlibConfig:
    """matplotlib配置管理器"""
    
    @staticmethod
    def setup_chinese_font():
        """设置中文字体支持"""
        # 强制设置中文字体
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
        plt.rcParams['axes.unicode_minus'] = False
        plt.rcParams['font.size'] = 12
        
        # 确保matplotlib全局设置也生效
        matplotlib.rcParams['font.family'] = 'sans-serif'
        matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
        matplotlib.rcParams['axes.unicode_minus'] = False
        matplotlib.rcParams['font.size'] = 12
        
        print("✅ 中文字体设置完成")
    
    @staticmethod
    def setup_english_font():
        """设置英文字体"""
        plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Liberation Sans', 'sans-serif']
        matplotlib.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Liberation Sans', 'sans-serif']
        plt.rcParams['axes.unicode_minus'] = False
        plt.rcParams['font.size'] = 10
        
        print("✅ 英文字体设置完成")
    
    @staticmethod
    def load_project_config():
        """加载项目专用配置文件"""
        project_root = Path(__file__).parent.parent.parent
        config_file = project_root / "matplotlibrc"
        
        if config_file.exists():
            matplotlib.rc_file(str(config_file))
            print(f"✅ 已加载项目配置文件: {config_file}")
            print(f"📊 当前字体设置: {plt.rcParams['font.sans-serif']}")
        else:
            print(f"⚠️ 项目配置文件不存在: {config_file}")
            MatplotlibConfig.setup_chinese_font()
    
    @staticmethod
    def reset_to_defaults():
        """重置为默认设置"""
        matplotlib.rcdefaults()
        print("✅ matplotlib设置已重置为默认值")
    
    @staticmethod
    def get_current_config():
        """获取当前配置信息"""
        config = {
            'font.family': plt.rcParams['font.family'],
            'font.sans-serif': plt.rcParams['font.sans-serif'],
            'font.size': plt.rcParams['font.size'],
            'axes.unicode_minus': plt.rcParams['axes.unicode_minus'],
            'figure.dpi': plt.rcParams['figure.dpi'],
            'figure.figsize': plt.rcParams['figure.figsize']
        }
        return config
    
    @staticmethod
    def print_config():
        """打印当前配置"""
        config = MatplotlibConfig.get_current_config()
        print("📊 当前matplotlib配置:")
        for key, value in config.items():
            print(f"  {key}: {value}")

# 自动加载项目配置
if __name__ == "__main__":
    MatplotlibConfig.load_project_config()
    MatplotlibConfig.print_config()
