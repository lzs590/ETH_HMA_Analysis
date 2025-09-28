# AI Coding Agent 技术指南

## 🤖 为AI代理准备的完整技术手册

### 📋 项目概述

这是一个基于Hull移动平均(HMA)技术指标的ETH/USDT价格趋势分析系统，包含数据采集、趋势分析、风险评估和可视化功能。

### 🏗️ 项目架构

```
ETH_HMA_Analysis/
├── src/                          # 核心源代码
│   ├── collectors/               # 数据采集模块
│   ├── analyzers/                # 分析计算模块
│   ├── managers/                 # 项目管理模块
│   ├── visualizers/             # 可视化模块
│   ├── reporters/                # 报告生成模块
│   └── utils/                    # 工具模块
├── scripts/                      # 执行脚本
├── assets/                       # 资源文件
│   ├── data/                     # 数据文件
│   ├── charts/                   # 图表文件
│   └── reports/                  # 报告文件
└── docs/                         # 文档
    └── technical_manual/          # 技术手册
```

## 🔧 核心模块说明

### 1. 数据采集模块 (DataCollector)

**文件位置**: `src/collectors/data_collector.py`

**核心功能**:
- 从币安API获取K线数据
- 支持多种时间间隔 (1m, 5m, 15m, 30m, 1h, 4h, 1d)
- 自动处理API限制和重试机制

**关键方法**:
```python
class DataCollector:
    def collect_historical_data(self, symbol, interval, years_back):
        """采集历史数据的主方法"""
        
    def get_klines_data(self, symbol, interval, start_time, end_time):
        """获取K线数据"""
        
    def _convert_to_dataframe(self, klines_data):
        """转换数据格式"""
```

**使用示例**:
```python
from src.collectors.data_collector import DataCollector

collector = DataCollector()
data = collector.collect_historical_data("ETHUSDT", "4h", 3)
```

### 2. 数学计算模块 (MathBrain)

**文件位置**: `src/eth_hma_analysis/core/math_brain.py`

**核心功能**:
- 计算Hull移动平均(HMA)
- 计算技术指标 (SMA, 波动率等)
- 数据质量验证

**关键方法**:
```python
class MathBrain:
    def add_hma_to_dataframe(self, df):
        """添加HMA指标到数据框"""
        
    def calculate_additional_indicators(self, df):
        """计算额外指标"""
        
    def validate_data(self, df):
        """验证数据质量"""
```

**HMA计算算法**:
```python
def calculate_hma(prices, period):
    # 步骤1: 计算加权移动平均
    wma_half = prices.rolling(window=period//2).mean()
    wma_full = prices.rolling(window=period).mean()
    
    # 步骤2: 计算原始HMA
    raw_hma = 2 * wma_half - wma_full
    
    # 步骤3: 平滑处理
    hma = raw_hma.rolling(window=int(np.sqrt(period))).mean()
    
    return hma
```

### 3. 趋势分析模块 (TrendAnalyzer)

**文件位置**: `src/eth_hma_analysis/core/trend_analyzer.py`

**核心功能**:
- 识别趋势转换点
- 计算PFE/MAE指标
- 分析风险收益比

**关键方法**:
```python
class TrendAnalyzer:
    def identify_turning_points(self, df):
        """识别趋势转换点"""
        
    def analyze_trend_intervals(self, df, turning_points):
        """分析趋势区间"""
        
    def calculate_pfe_mae(self, interval_data, trend_direction):
        """计算PFE和MAE"""
        
    def run_complete_analysis(self, df):
        """运行完整分析"""
```

**趋势识别算法**:
```python
def identify_trends(df, hma_col='HMA_45'):
    # 计算HMA斜率
    df['HMA_slope'] = df[hma_col].diff()
    
    # 计算斜率符号变化
    df['slope_sign'] = np.sign(df['HMA_slope'])
    df['slope_change'] = df['slope_sign'].diff().fillna(0)
    
    # 识别趋势转换点
    df['turning_point'] = 0
    
    # 上涨趋势开始：斜率由负转正
    uptrend_start = df['slope_change'] == 2.0
    df.loc[uptrend_start, 'turning_point'] = 1
    
    # 下跌趋势开始：斜率由正转负
    downtrend_start = df['slope_change'] == -2.0
    df.loc[downtrend_start, 'turning_point'] = -1
    
    return df
```

### 4. 可视化模块 (TrendVisualizer)

**文件位置**: `src/analyzers/trend_visualizer.py`

**核心功能**:
- 生成趋势分析图表
- 支持中英文显示
- 多种图表类型

**关键方法**:
```python
class TrendVisualizer:
    def plot_turning_points(self, df, turning_points):
        """绘制转折点图表"""
        
    def plot_trend_intervals(self, df, trend_intervals):
        """绘制趋势区间图表"""
        
    def plot_event_analysis(self, df, events):
        """绘制事件分析图表"""
```

### 5. 项目管理模块 (ProjectManager)

**文件位置**: `src/managers/project_manager.py`

**核心功能**:
- 协调各个模块工作
- 管理数据流程
- 生成分析报告

**关键方法**:
```python
class ProjectManager:
    def process_single_interval(self, symbol, interval, years_back):
        """处理单个时间间隔的数据"""
        
    def run_complete_analysis(self, symbol, interval):
        """运行完整分析"""
```

## 📊 数据分析流程

### 1. 数据采集流程

```python
# 步骤1: 初始化数据采集器
collector = DataCollector()

# 步骤2: 采集原始数据
raw_data = collector.collect_historical_data("ETHUSDT", "4h", 3)

# 步骤3: 数据验证
if not collector.validate_data(raw_data):
    raise ValueError("数据质量验证失败")
```

### 2. 数据处理流程

```python
# 步骤1: 初始化数学计算引擎
math_brain = MathBrain(hma_period=45)

# 步骤2: 计算HMA指标
processed_data = math_brain.add_hma_to_dataframe(raw_data)

# 步骤3: 计算额外指标
processed_data = math_brain.calculate_additional_indicators(processed_data)
```

### 3. 趋势分析流程

```python
# 步骤1: 初始化趋势分析器
analyzer = TrendAnalyzer()

# 步骤2: 识别转折点
turning_points = analyzer.identify_turning_points(processed_data)

# 步骤3: 分析趋势区间
trend_intervals = analyzer.analyze_trend_intervals(processed_data, turning_points)

# 步骤4: 计算风险指标
risk_analysis = analyzer.calculate_risk_metrics(trend_intervals)
```

### 4. 可视化流程

```python
# 步骤1: 初始化可视化器
visualizer = TrendVisualizer(use_chinese=True)

# 步骤2: 生成图表
visualizer.plot_turning_points(processed_data, turning_points)
visualizer.plot_trend_intervals(processed_data, trend_intervals)
visualizer.plot_event_analysis(processed_data, events)
```

## 🔧 配置参数

### 核心配置 (src/utils/config.py)

```python
# 交易对设置
SYMBOL = "ETHUSDT"

# 时间间隔
INTERVALS = ["1h", "4h"]

# HMA参数
HMA_PERIOD = 45
SLOPE_THRESHOLD = 0.001

# 数据采集参数
YEARS_BACK = 3
MAX_RETRIES = 3
REQUEST_DELAY = 0.1

# 币安API配置
BINANCE_BASE_URL = "https://api.binance.com/api/v3"
BINANCE_KLINES_ENDPOINT = "/klines"
```

### 分析参数

```python
# 趋势分析参数
EVENT_WINDOW = 5
MIN_TREND_DURATION = 1

# 风险指标参数
PFE_THRESHOLD = 5.0
MAE_THRESHOLD = 3.0
```

## 📈 关键指标说明

### 1. Hull移动平均 (HMA)
- **用途**: 识别趋势方向
- **计算**: 基于加权移动平均的平滑处理
- **优势**: 减少滞后性，更好跟踪趋势

### 2. PFE (Maximum Favorable Excursion)
- **含义**: 最大有利偏移
- **计算**: 趋势方向的最大价格变化
- **用途**: 衡量理想收益潜力

### 3. MAE (Maximum Adverse Excursion)
- **含义**: 最大不利偏移
- **计算**: 反向的最大价格变化
- **用途**: 衡量最大风险损失

### 4. 风险收益比
- **计算**: MAE / PFE
- **用途**: 评估风险控制效果
- **目标**: 值越小越好

## 🚀 快速执行命令

### 数据采集
```bash
# 采集4小时数据
python scripts/main.py

# 采集1小时数据
python scripts/main.py --interval 1h
```

### 趋势分析
```bash
# 运行4小时分析
python scripts/trend_analysis.py --interval 4h

# 生成英文报告
python scripts/trend_analysis.py --interval 4h --english

# 详细输出
python scripts/trend_analysis.py --interval 4h --verbose
```

### 启动Dashboard
```bash
# 启动Financial Dashboard
streamlit run dashboard/financial_dashboard_fixed.py

# 指定端口
streamlit run dashboard/financial_dashboard_fixed.py --server.port 8502
```

## 📁 文件结构说明

### 数据文件
- **原始数据**: `src/utils/data/ETHUSDT_4h_raw_*.parquet`
- **处理后数据**: `src/utils/data/ETHUSDT_4h_processed_*.parquet`
- **分析结果**: `assets/reports/trend_analysis_4h_*.json`
- **CSV数据**: `assets/reports/trends_4h_chronological.csv`

### 图表文件
- **转折点图表**: `assets/charts/turning_points_4h_*.png`
- **趋势区间图表**: `assets/charts/trend_intervals_4h_*.png`
- **事件分析图表**: `assets/charts/event_analysis_4h_*.png`
- **策略图表**: `assets/charts/strategy_*.png`

### 报告文件
- **详细报告**: `assets/reports/ETH_HMA_4h_Detailed_Research_Report.md`
- **风险报告**: `assets/reports/risk_trends_detailed_report.txt`
- **策略报告**: `assets/reports/ETH_HMA_Strategy_Report_*.md`

## 🐛 常见问题解决

### 1. 数据采集失败
```python
# 检查网络连接
import requests
response = requests.get("https://api.binance.com/api/v3/ping")
print(response.status_code)

# 检查API限制
# 增加请求间隔时间
REQUEST_DELAY = 0.2  # 增加到0.2秒
```

### 2. 中文字体显示问题
```python
# 设置中文字体
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
```

### 3. 内存不足
```python
# 分块处理大数据
chunk_size = 10000
for chunk in pd.read_parquet(file, chunksize=chunk_size):
    # 处理数据块
    pass
```

### 4. 计算性能问题
```python
# 使用向量化操作
def vectorized_calculation(data):
    return np.vectorize(calculation_function)(data)

# 使用并行计算
from multiprocessing import Pool
with Pool(processes=4) as pool:
    results = pool.map(analyze_chunk, data_chunks)
```

## 🔍 调试技巧

### 1. 启用详细日志
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 2. 数据验证
```python
def validate_data(df):
    print(f"数据形状: {df.shape}")
    print(f"缺失值: {df.isnull().sum().sum()}")
    print(f"数据类型: {df.dtypes}")
    print(f"时间范围: {df.index.min()} 到 {df.index.max()}")
```

### 3. 性能监控
```python
import time
start_time = time.time()
# 执行操作
end_time = time.time()
print(f"执行时间: {end_time - start_time:.2f}秒")
```

## 📚 扩展开发

### 1. 添加新指标
```python
def calculate_new_indicator(df):
    """计算新指标"""
    # 实现指标计算逻辑
    return df
```

### 2. 自定义可视化
```python
def create_custom_chart(data):
    """创建自定义图表"""
    # 实现图表逻辑
    pass
```

### 3. 集成新数据源
```python
class NewDataCollector:
    """新数据源采集器"""
    def collect_data(self):
        # 实现数据采集逻辑
        pass
```

---

*最后更新: 2025-09-27*
*版本: v1.0.0*
