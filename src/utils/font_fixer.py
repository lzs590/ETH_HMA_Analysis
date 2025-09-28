"""
字体修复工具
强制解决matplotlib中文字体显示问题
"""

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

def force_chinese_font():
    """强制设置中文字体 - 根本性解决方案"""
    
    # 1. 重置所有matplotlib设置
    matplotlib.rcdefaults()
    
    # 2. 强制设置中文字体
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['font.size'] = 12
    
    # 3. 确保matplotlib全局设置也生效
    matplotlib.rcParams['font.family'] = 'sans-serif'
    matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
    matplotlib.rcParams['axes.unicode_minus'] = False
    matplotlib.rcParams['font.size'] = 12
    
    # 4. 验证设置
    print(f"✅ 中文字体已强制设置: {plt.rcParams['font.sans-serif']}")
    print(f"✅ 负号显示设置: {plt.rcParams['axes.unicode_minus']}")

def ensure_chinese_font():
    """确保中文字体设置生效"""
    # 每次调用都重新设置
    force_chinese_font()

# 自动执行字体设置
if __name__ == "__main__":
    force_chinese_font()
else:
    # 当作为模块导入时自动设置
    force_chinese_font()
