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

# 数据获取配置
SYMBOL = "ETHUSDT"
INTERVALS = ["1h", "4h"]  # 1小时和4小时数据
YEARS_BACK = 3  # 获取过去3年的数据

# 请求配置
REQUEST_DELAY = 0.1  # 请求间隔，避免触发限制
MAX_RETRIES = 3  # 最大重试次数
