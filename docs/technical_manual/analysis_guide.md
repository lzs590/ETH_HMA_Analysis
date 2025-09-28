# 数据分析指南

## 🧮 数据分析完整流程

### 🚀 快速开始

```bash
# 运行趋势分析
python scripts/trend_analysis.py --interval 4h --english

# 生成详细报告
python scripts/trend_analysis.py --interval 4h --verbose
```

### 🔧 分析配置

#### 核心参数设置
文件位置: `src/utils/config.py`

```python
# HMA参数
HMA_PERIOD = 45                    # Hull移动平均周期
SLOPE_THRESHOLD = 0.001            # 斜率阈值

# 趋势分析参数
EVENT_WINDOW = 5                   # 事件窗口期
MIN_TREND_DURATION = 1             # 最小趋势持续时间

# 风险指标参数
PFE_THRESHOLD = 5.0               # PFE阈值
MAE_THRESHOLD = 3.0               # MAE阈值
```

### 📊 分析算法详解

#### 1. Hull移动平均(HMA)计算

```python
def calculate_hma(prices, period):
    """计算Hull移动平均"""
    # 步骤1: 计算加权移动平均
    wma_half = prices.rolling(window=period//2).mean()
    wma_full = prices.rolling(window=period).mean()
    
    # 步骤2: 计算原始HMA
    raw_hma = 2 * wma_half - wma_full
    
    # 步骤3: 平滑处理
    hma = raw_hma.rolling(window=int(np.sqrt(period))).mean()
    
    return hma
```

#### 2. 趋势识别算法

```python
def identify_trends(df, hma_col='HMA_45'):
    """识别趋势转换点"""
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

#### 3. PFE/MAE计算

```python
def calculate_pfe_mae(interval_data, trend_direction):
    """计算PFE和MAE"""
    start_price = interval_data['open'].iloc[0]
    high_price = interval_data['high'].max()
    low_price = interval_data['low'].min()
    
    if trend_direction == 'up':
        # 上涨趋势（做多策略）
        pfe = (high_price / start_price - 1) * 100  # 最大涨幅
        mae = (start_price / low_price - 1) * 100   # 最大跌幅
    else:
        # 下跌趋势（做空策略）
        pfe = (start_price / low_price - 1) * 100   # 最大跌幅
        mae = (high_price / start_price - 1) * 100  # 最大涨幅
    
    return pfe, mae
```

### 📈 分析指标说明

#### 核心指标

| 指标 | 含义 | 计算公式 | 策略意义 |
|------|------|----------|----------|
| **PFE** | 最大有利偏移 | 趋势方向最大价格变化 | 理想收益潜力 |
| **MAE** | 最大不利偏移 | 反向最大价格变化 | 最大风险损失 |
| **Risk Ratio** | 风险收益比 | MAE / PFE | 风险控制指标 |
| **Duration** | 持续时间 | 趋势区间长度 | 趋势稳定性 |

#### 策略指标

| 指标 | 含义 | 计算方式 | 应用场景 |
|------|------|----------|----------|
| **Ideal Profit** | 理想收益 | 趋势方向最大收益 | 策略收益评估 |
| **Actual Profit** | 实际收益 | 趋势结束净收益 | 实际表现评估 |
| **Risk Loss** | 风险损失 | 反向最大损失 | 风险控制 |
| **Risk-Reward Ratio** | 风险收益比 | 风险/收益比率 | 策略优化 |

### 🔄 分析执行流程

#### 步骤1: 数据预处理
```python
from src.analyzers.trend_analyzer import TrendAnalyzer

# 初始化分析器
analyzer = TrendAnalyzer()

# 加载数据
data = pd.read_parquet('src/utils/data/ETHUSDT_4h_processed_*.parquet')
```

#### 步骤2: 趋势识别
```python
# 识别转折点
turning_points = analyzer.identify_turning_points(data)

# 分析趋势区间
trend_intervals = analyzer.analyze_trend_intervals(data, turning_points)
```

#### 步骤3: 风险分析
```python
# 计算PFE/MAE
pfe_mae_results = analyzer.calculate_pfe_mae(trend_intervals)

# 风险收益分析
risk_analysis = analyzer.analyze_risk_reward(trend_intervals)
```

#### 步骤4: 策略评估
```python
# 做多策略分析
long_strategy = analyzer.analyze_uptrend_metrics(trend_intervals)

# 做空策略分析
short_strategy = analyzer.analyze_downtrend_metrics(trend_intervals)
```

### 📊 分析结果输出

#### 1. JSON报告格式
```json
{
    "analysis_summary": {
        "total_trends": 126,
        "uptrends": 63,
        "downtrends": 63,
        "high_risk_trends": 61
    },
    "uptrend_analysis": {
        "intervals": [...],
        "metrics": {...}
    },
    "downtrend_analysis": {
        "intervals": [...],
        "metrics": {...}
    }
}
```

#### 2. CSV数据格式
```csv
trend_id,trend_type,start_time,end_time,start_price,end_price,price_change_pct,max_rally,max_decline,risk_ratio,is_risk_greater,duration_hours
TREND_001,下降趋势,2024-10-09 04:00:00,2024-10-09T12:00:00,2436.01,2461.30,1.04,1.48,0.53,2.79,True,8
```

### 🎯 分析应用场景

#### 1. 趋势跟踪策略
```python
# 识别趋势转换点
turning_points = analyzer.identify_turning_points(data)

# 生成交易信号
signals = analyzer.generate_trading_signals(turning_points)
```

#### 2. 风险管理
```python
# 计算风险指标
risk_metrics = analyzer.calculate_risk_metrics(trend_intervals)

# 设置止损点
stop_loss = analyzer.calculate_stop_loss(risk_metrics)
```

#### 3. 策略优化
```python
# 参数优化
best_params = analyzer.optimize_parameters(data, param_range)

# 回测分析
backtest_results = analyzer.run_backtest(data, best_params)
```

### 🔍 高级分析功能

#### 1. 事件分析
```python
# 分析转折点前后的事件
event_analysis = analyzer.analyze_events(data, turning_points)

# 事件统计
event_stats = analyzer.calculate_event_statistics(event_analysis)
```

#### 2. 相关性分析
```python
# 趋势与市场指标相关性
correlation = analyzer.calculate_correlation(data, market_indicators)

# 时间序列相关性
time_correlation = analyzer.calculate_time_correlation(data)
```

#### 3. 预测分析
```python
# 趋势预测
trend_forecast = analyzer.forecast_trends(data, horizon=24)

# 风险预测
risk_forecast = analyzer.forecast_risk(data, horizon=24)
```

### ⚠️ 分析注意事项

#### 1. 数据质量
- 确保数据完整性
- 处理异常值和缺失值
- 验证时间序列连续性

#### 2. 参数调优
- HMA周期选择
- 斜率阈值设置
- 风险参数调整

#### 3. 结果验证
- 交叉验证分析结果
- 敏感性分析
- 稳健性测试

### 🐛 常见问题

#### 问题1: 趋势识别不准确
```python
# 解决: 调整HMA参数和斜率阈值
HMA_PERIOD = 30  # 减小周期
SLOPE_THRESHOLD = 0.005  # 增大阈值
```

#### 问题2: 计算性能问题
```python
# 解决: 优化计算算法
# 使用向量化操作
# 分块处理大数据
# 并行计算
```

#### 问题3: 内存不足
```python
# 解决: 内存管理
# 分块处理数据
# 及时释放内存
# 使用高效数据结构
```

### 📈 性能优化

#### 1. 算法优化
```python
# 使用NumPy向量化操作
def vectorized_calculation(data):
    return np.vectorize(calculation_function)(data)

# 使用Pandas内置函数
def pandas_optimized(data):
    return data.rolling(window=period).apply(calculation_function)
```

#### 2. 并行计算
```python
# 使用多进程
from multiprocessing import Pool

def parallel_analysis(data_chunks):
    with Pool(processes=4) as pool:
        results = pool.map(analyze_chunk, data_chunks)
    return results
```

#### 3. 内存优化
```python
# 分块处理
def chunked_analysis(data, chunk_size=10000):
    for chunk in data.groupby(data.index // chunk_size):
        yield analyze_chunk(chunk)
```

---

*最后更新: 2025-09-27*
*版本: v1.0.0*
