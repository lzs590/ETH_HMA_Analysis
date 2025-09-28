# 数据采集指南

## 📥 数据采集完整流程

### 🚀 快速开始

```bash
# 1. 激活虚拟环境
venv\Scripts\activate

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行数据采集
python scripts/main.py
```

### 🔧 配置参数

#### 编辑配置文件
文件位置: `src/utils/config.py`

```python
# 交易对设置
SYMBOL = "ETHUSDT"

# 时间间隔 (支持: 1m, 5m, 15m, 30m, 1h, 4h, 1d)
INTERVALS = ["1h", "4h"]

# HMA周期 (推荐: 45)
HMA_PERIOD = 45

# 历史数据年数
YEARS_BACK = 3

# 币安API配置
BINANCE_BASE_URL = "https://api.binance.com/api/v3"
BINANCE_KLINES_ENDPOINT = "/klines"

# 请求限制
MAX_RETRIES = 3
REQUEST_DELAY = 0.1  # 秒
```

### 📊 数据采集流程

#### 步骤1: 初始化数据采集器
```python
from src.collectors.data_collector import DataCollector

collector = DataCollector()
```

#### 步骤2: 采集历史数据
```python
# 采集4小时数据，过去3年
raw_data = collector.collect_historical_data("ETHUSDT", "4h", 3)
```

#### 步骤3: 数据验证
```python
# 检查数据质量
print(f"数据形状: {raw_data.shape}")
print(f"时间范围: {raw_data.index.min()} 到 {raw_data.index.max()}")
print(f"缺失值: {raw_data.isnull().sum().sum()}")
```

### 🗂️ 数据存储

#### 原始数据文件
- **位置**: `src/utils/data/ETHUSDT_4h_raw_*.parquet`
- **格式**: Parquet (高效压缩)
- **内容**: 币安API原始K线数据

#### 处理后数据文件
- **位置**: `src/utils/data/ETHUSDT_4h_processed_*.parquet`
- **格式**: Parquet
- **内容**: 包含HMA等技术指标的数据

### 📋 数据格式说明

#### 原始K线数据列
```python
columns = [
    'open_time',      # 开盘时间 (UTC)
    'open',           # 开盘价
    'high',           # 最高价
    'low',            # 最低价
    'close',          # 收盘价
    'volume',         # 成交量
    'close_time',     # 收盘时间
    'quote_asset_volume',  # 成交额
    'trades_count',   # 成交笔数
    'taker_buy_base_asset_volume',    # 主动买入成交量
    'taker_buy_quote_asset_volume',   # 主动买入成交额
    'ignore'          # 忽略字段
]
```

#### 处理后数据额外列
```python
additional_columns = [
    f'HMA_{HMA_PERIOD}',  # Hull移动平均
    'HMA_slope',          # HMA斜率
    'SMA_20',             # 20期简单移动平均
    'SMA_50',             # 50期简单移动平均
    'price_change',       # 价格变化率
    'price_change_abs',   # 绝对价格变化
    'volatility',         # 波动率
    'hma_deviation'       # HMA偏离度
]
```

### 🔄 数据采集API详解

#### DataCollector类方法

```python
class DataCollector:
    def __init__(self):
        """初始化数据采集器"""
        
    def get_klines_data(self, symbol, interval, start_time, end_time):
        """获取K线数据"""
        # 参数:
        #   symbol: 交易对 (如 'ETHUSDT')
        #   interval: 时间间隔 (如 '4h')
        #   start_time: 开始时间戳 (毫秒)
        #   end_time: 结束时间戳 (毫秒)
        # 返回: K线数据列表
        
    def collect_historical_data(self, symbol, interval, years_back):
        """采集历史数据"""
        # 参数:
        #   symbol: 交易对
        #   interval: 时间间隔
        #   years_back: 历史年数
        # 返回: DataFrame
        
    def _get_interval_ms(self, interval):
        """时间间隔转毫秒"""
        # 支持: 1m, 5m, 15m, 30m, 1h, 4h, 1d
        
    def _convert_to_dataframe(self, klines_data):
        """转换数据格式"""
        # 将币安API数据转换为DataFrame
```

### ⚠️ 注意事项

#### 1. API限制
- 币安API有请求频率限制
- 单次最多返回1000条数据
- 建议请求间隔0.1秒

#### 2. 数据质量
- 检查时间连续性
- 验证价格数据合理性
- 处理缺失值和异常值

#### 3. 存储管理
- Parquet格式高效压缩
- 定期清理旧数据文件
- 备份重要数据

### 🐛 常见问题

#### 问题1: 网络连接失败
```bash
# 错误: requests.exceptions.ConnectionError
# 解决: 检查网络连接和代理设置
```

#### 问题2: API限制
```bash
# 错误: 429 Too Many Requests
# 解决: 增加请求间隔时间
```

#### 问题3: 数据不完整
```bash
# 错误: 数据缺失或时间不连续
# 解决: 重新采集或补充数据
```

### 📈 性能优化

#### 1. 批量处理
```python
# 分批采集大量数据
batch_size = 1000
for i in range(0, total_records, batch_size):
    batch_data = collector.get_klines_data(...)
    # 处理批次数据
```

#### 2. 并行处理
```python
# 使用多线程加速
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(collect_data, params) for params in param_list]
```

#### 3. 内存管理
```python
# 分块处理大数据
chunk_size = 10000
for chunk in pd.read_parquet(file, chunksize=chunk_size):
    # 处理数据块
```

### 🔍 数据验证

#### 完整性检查
```python
def validate_data(df):
    """验证数据完整性"""
    checks = {
        'shape': df.shape,
        'time_range': (df.index.min(), df.index.max()),
        'missing_values': df.isnull().sum().sum(),
        'duplicates': df.index.duplicated().sum(),
        'price_range': (df['low'].min(), df['high'].max())
    }
    return checks
```

#### 数据质量报告
```python
def generate_quality_report(df):
    """生成数据质量报告"""
    report = {
        'total_records': len(df),
        'time_span': (df.index.max() - df.index.min()).days,
        'missing_rate': df.isnull().sum().sum() / (len(df) * len(df.columns)),
        'price_anomalies': detect_price_anomalies(df),
        'volume_anomalies': detect_volume_anomalies(df)
    }
    return report
```

---

*最后更新: 2025-09-27*
*版本: v1.0.0*
