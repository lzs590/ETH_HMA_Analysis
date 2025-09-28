# ETH HMA 策略分析 - Jupyter使用指南

## 🚀 快速开始

### 1. 环境准备
```bash
# 安装Jupyter依赖
pip install -r requirements_jupyter.txt

# 启动Jupyter环境
python scripts/start_jupyter.py
```

### 2. 使用流程
1. **00_快速开始.ipynb** - 环境设置和系统检查
2. **01_数据加载与预处理.ipynb** - 数据加载和预处理
3. **02_4h级别策略分析.ipynb** - 深度策略分析

## 📊 Notebook功能说明

### 00_快速开始.ipynb
- 环境设置和库导入
- 系统状态检查
- 数据文件验证
- 快速数据预览

### 01_数据加载与预处理.ipynb
- 加载ETH历史数据（1h和4h级别）
- 数据质量检查
- HMA指标验证
- 数据预处理

### 02_4h级别策略分析.ipynb
- 趋势识别和拐点分析
- 做多/做空策略表现
- 风险收益分析
- 策略优化建议

## 🛠️ 核心模块

### JupyterDataLoader
```python
from utils.jupyter_utils import JupyterDataLoader

# 加载数据
loader = JupyterDataLoader()
df_4h = loader.load_4h_data()
df_1h = loader.load_1h_data()
```

### JupyterVisualizer
```python
from visualizers.jupyter_visualizer import JupyterVisualizer

# 创建可视化
viz = JupyterVisualizer()
fig, ax = viz.plot_price_and_hma(df_4h)
```

### JupyterAnalyzer
```python
from utils.jupyter_utils import JupyterAnalyzer

# 快速分析
analyzer = JupyterAnalyzer()
fig1, fig2 = analyzer.quick_price_analysis(df_4h)
```

## 📈 可视化功能

### 1. 价格走势分析
- ETH价格曲线
- HMA指标叠加
- 拐点识别
- 趋势区间标注

### 2. 策略表现分析
- 做多/做空策略对比
- 理想收益 vs 实际收益
- 风险收益比分析
- 胜率统计

### 3. 风险分析
- 风险损失分布
- 收益风险散点图
- 风险收益比分布
- 策略胜率分析

### 4. 综合仪表板
- 多维度指标展示
- 交互式图表
- 实时数据更新
- 策略建议

## 🔧 高级功能

### 自定义分析
```python
# 自定义时间范围
fig, ax = jupyter_viz.plot_price_and_hma(
    df_4h, 
    start_date='2024-01-01',
    end_date='2024-12-31'
)

# 自定义HMA参数
analysis_result = trend_analyzer.run_complete_analysis(
    df_4h, 
    hma_period=30,  # 自定义HMA周期
    slope_threshold=0.002  # 自定义斜率阈值
)
```

### 数据导出
```python
# 导出分析结果
analysis_result.to_csv('analysis_results.csv')
intervals_df = pd.DataFrame(intervals)
intervals_df.to_excel('trend_intervals.xlsx')
```

## 🎯 策略分析要点

### 1. 趋势识别
- **上涨趋势**: HMA斜率由负转正 → 做多信号
- **下跌趋势**: HMA斜率由正转负 → 做空信号

### 2. 收益计算
- **理想收益 (PFE)**: 趋势期间最大价格变动
- **实际收益**: 趋势起始到结束的价格变动
- **风险损失 (MAE)**: 趋势期间最大不利变动

### 3. 风险控制
- 风险收益比分析
- 最大回撤控制
- 胜率统计
- 风险分布分析

## 🚨 注意事项

### 1. 数据质量
- 确保数据文件存在
- 检查数据完整性
- 验证HMA指标计算

### 2. 中文字体
- 系统需要支持中文字体
- 图表标题和标签使用中文
- 字体设置已自动配置

### 3. 内存管理
- 大数据集可能占用较多内存
- 建议使用数据采样
- 及时清理不需要的变量

## 🔍 故障排除

### 1. 导入错误
```python
# 确保路径正确
import sys
sys.path.append('../src')
```

### 2. 数据加载失败
```python
# 检查数据文件
data_dir = Path("../src/utils/data")
data_files = list(data_dir.glob("*.parquet"))
print(f"找到 {len(data_files)} 个数据文件")
```

### 3. 图表显示问题
```python
# 重新设置字体
from utils.jupyter_utils import JupyterConfig
JupyterConfig.setup_matplotlib()
```

## 📚 扩展功能

### 1. 自定义指标
```python
# 添加自定义技术指标
df['custom_indicator'] = your_calculation(df)
```

### 2. 策略回测
```python
# 运行策略回测
backtest_result = strategy_backtest(df, signals)
```

### 3. 实时分析
```python
# 实时数据更新
def update_analysis():
    # 更新数据和分析
    pass
```

## 🎉 开始使用

1. 运行 `python scripts/start_jupyter.py`
2. 在浏览器中打开Jupyter
3. 按顺序运行notebook
4. 开始您的策略分析之旅！

---

**Happy Trading! 📈🚀**
