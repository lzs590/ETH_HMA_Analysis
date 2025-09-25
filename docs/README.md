# ETH HMA 分析器

一个自动化工具，用于从币安下载以太坊（ETH）历史价格数据，计算Hull移动平均（HMA）技术指标，并将结果高效存储。

## 🎯 项目目标

- 自动从币安获取ETH过去3年的价格数据
- 计算HMA技术指标
- 将原始数据和处理后数据分别存储为高效的Parquet格式
- 支持1小时和4小时两种时间间隔

## 🏗️ 项目架构

项目采用模块化设计，分为四个核心部门：

### 📥 数据采集部 (DataCollector)
- 负责从币安API获取原始K线数据
- 支持批量获取大量历史数据
- 自动处理API限制和重试机制

### 🧮 分析计算部 (MathBrain)
- 计算Hull移动平均（HMA）指标
- 提供数据质量验证
- 支持额外技术指标计算

### 📚 档案管理部 (Librarian)
- 使用Parquet格式高效存储数据
- 管理文件元数据和版本控制
- 提供数据加载和文件管理功能

### 🎯 项目总指挥 (ProjectManager)
- 协调各个部门按顺序工作
- 管理整个分析流程
- 生成详细的执行报告

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行分析

```bash
# 运行完整分析（1小时 + 4小时数据）
python main.py

# 仅分析1小时数据
python main.py --interval 1h

# 仅分析4小时数据
python main.py --interval 4h

# 获取过去2年数据
python main.py --years 2

# 使用30周期HMA
python main.py --hma-period 30

# 显示详细日志
python main.py --verbose

# 查看数据概览
python main.py --overview
```

### 3. 查看结果

分析完成后，数据将保存在 `data/` 目录中：
- `ETHUSDT_1h_raw_*.parquet` - 原始1小时数据
- `ETHUSDT_1h_processed_*.parquet` - 包含HMA的1小时数据
- `ETHUSDT_4h_raw_*.parquet` - 原始4小时数据
- `ETHUSDT_4h_processed_*.parquet` - 包含HMA的4小时数据

## 📊 数据格式

### 原始数据列
- `open_time` - 开盘时间（索引）
- `open` - 开盘价
- `high` - 最高价
- `low` - 最低价
- `close` - 收盘价
- `volume` - 成交量
- `close_time` - 收盘时间
- `quote_asset_volume` - 成交额
- `trades_count` - 成交笔数

### 处理后数据额外列
- `HMA_45` - Hull移动平均（默认45周期）
- `SMA_20` - 20期简单移动平均
- `SMA_50` - 50期简单移动平均
- `price_change` - 价格变化率
- `price_change_abs` - 绝对价格变化
- `volatility` - 20期波动率
- `hma_deviation` - HMA与价格的偏离度

## ⚙️ 配置选项

在 `config.py` 中可以修改以下配置：

```python
# 交易对符号
SYMBOL = "ETHUSDT"

# 时间间隔
INTERVALS = ["1h", "4h"]

# HMA周期
HMA_PERIOD = 45

# 获取历史数据年数
YEARS_BACK = 3

# 数据存储目录
DATA_DIR = "./data"
```

## 🔧 高级用法

### 单独使用各个模块

```python
from data_collector import DataCollector
from math_brain import MathBrain
from librarian import Librarian

# 数据采集
collector = DataCollector()
raw_data = collector.collect_historical_data("ETHUSDT", "1h", 3)

# 计算HMA
math_brain = MathBrain(hma_period=45)
processed_data = math_brain.add_hma_to_dataframe(raw_data)

# 保存数据
librarian = Librarian("./data")
librarian.save_processed_data(processed_data, "ETHUSDT", "1h", 45)
```

### 加载已保存的数据

```python
from librarian import Librarian
import pandas as pd

librarian = Librarian("./data")
df = librarian.load_dataframe("ETHUSDT_1h_processed_20231201_120000.parquet")
print(df.head())
```

## 📈 HMA指标说明

Hull移动平均（Hull Moving Average）是一种先进的技术分析指标，由Alan Hull开发。它通过以下步骤计算：

1. 计算两个不同周期的加权移动平均
2. 创建原始HMA信号
3. 对原始信号进行平滑处理

HMA的优势：
- 减少滞后性
- 更好地跟踪价格趋势
- 减少假信号

## 📝 日志文件

程序运行时会生成 `eth_hma_analysis.log` 日志文件，记录详细的执行过程。

## 🛠️ 故障排除

### 常见问题

1. **网络连接问题**
   - 检查网络连接
   - 确认币安API可访问

2. **数据获取失败**
   - 检查交易对符号是否正确
   - 确认时间间隔格式正确

3. **内存不足**
   - 减少获取的历史数据年数
   - 分批处理数据

4. **文件权限问题**
   - 确保对data目录有写权限

### 调试模式

使用 `--verbose` 参数启用详细日志：

```bash
python main.py --verbose
```

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📞 支持

如有问题，请查看日志文件或提交Issue。
