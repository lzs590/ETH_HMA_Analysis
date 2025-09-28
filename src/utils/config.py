"""
ETH HMA 分析器配置文件
"""
import os
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent

# 数据存储目录
DATA_DIR = PROJECT_ROOT / "data"

# 确保数据目录存在
DATA_DIR.mkdir(exist_ok=True)

# HMA参数配置
HMA_PERIOD = 45  # HMA周期，可根据需要调整

# 币安API配置
BINANCE_BASE_URL = "https://api.binance.com"
BINANCE_KLINES_ENDPOINT = "/api/v3/klines"

# 备用API端点（如果主端点被限制）
BINANCE_ALT_URL = "https://api1.binance.com"
BINANCE_ALT_URL2 = "https://api2.binance.com"

# 数据获取配置
SYMBOL = "ETHUSDT"
INTERVALS = ["4h"]  # 只做4小时级别分析
YEARS_BACK = 4  # 获取过去4年的数据（从2022年1月1日开始）

# 特定时间范围配置
START_DATE = "2023-01-01T00:00:00Z"  # 开始时间：2023年1月1日0:00 UTC（测试用）
END_DATE = None  # 结束时间：现在（None表示当前时间）

# 请求配置
REQUEST_DELAY = 0.5  # 请求间隔，避免触发限制（增加延迟）
MAX_RETRIES = 3  # 最大重试次数
