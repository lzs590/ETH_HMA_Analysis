"""
数据采集部 (The Data Collector)
专门负责从币安交易所获取原始数据
"""
import requests
import pandas as pd
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any
import logging
from ..utils.config import *

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataCollector:
    """数据采集部 - 负责从币安获取ETH历史数据"""
    
    def __init__(self):
        self.base_url = BINANCE_BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'ETH-HMA-Analyzer/1.0'
        })
        
        # 配置代理服务器（如果需要）
        self.proxies = None
        # 取消注释以下行并填入代理信息
        # self.proxies = {
        #     'http': 'http://proxy-server:port',
        #     'https': 'https://proxy-server:port'
        # }
    
    def get_klines_data(self, symbol: str, interval: str, start_time: int, end_time: int) -> List[List]:
        """
        从币安获取K线数据
        
        Args:
            symbol: 交易对符号 (如 'ETHUSDT')
            interval: 时间间隔 (如 '1h', '4h')
            start_time: 开始时间戳 (毫秒)
            end_time: 结束时间戳 (毫秒)
            
        Returns:
            K线数据列表
        """
        # 尝试多个API端点
        urls = [
            f"{self.base_url}{BINANCE_KLINES_ENDPOINT}",
            f"{BINANCE_ALT_URL}{BINANCE_KLINES_ENDPOINT}",
            f"{BINANCE_ALT_URL2}{BINANCE_KLINES_ENDPOINT}"
        ]
        params = {
            'symbol': symbol,
            'interval': interval,
            'startTime': start_time,
            'endTime': end_time,
            'limit': 1000  # 币安单次最大返回1000条数据
        }
        
        # 尝试每个URL
        for url in urls:
            for attempt in range(MAX_RETRIES):
                try:
                    logger.info(f"尝试API端点: {url}")
                    response = self.session.get(url, params=params, timeout=30, proxies=self.proxies)
                    response.raise_for_status()
                    data = response.json()
                    
                    if not data:
                        logger.warning(f"未获取到数据: {symbol} {interval} {start_time}-{end_time}")
                        continue
                    
                    logger.info(f"✅ 成功从 {url} 获取 {len(data)} 条数据: {symbol} {interval}")
                    return data
                    
                except requests.exceptions.RequestException as e:
                    logger.error(f"请求失败 (尝试 {attempt + 1}/{MAX_RETRIES}): {e}")
                    if attempt < MAX_RETRIES - 1:
                        time.sleep(REQUEST_DELAY * (2 ** attempt))  # 指数退避
                    else:
                        logger.warning(f"端点 {url} 失败，尝试下一个端点")
                        break
        
        return []
    
    def collect_historical_data(self, symbol: str, interval: str, years_back: int = 3) -> pd.DataFrame:
        """
        收集历史数据的主方法
        
        Args:
            symbol: 交易对符号
            interval: 时间间隔
            years_back: 获取多少年的历史数据
            
        Returns:
            包含历史数据的DataFrame
        """
        logger.info(f"开始收集 {symbol} {interval} 历史数据")
        
        # 计算时间范围
        if START_DATE:
            # 使用配置中的特定开始时间
            start_dt = datetime.fromisoformat(START_DATE.replace('Z', '+00:00'))
            start_time = int(start_dt.timestamp() * 1000)
            logger.info(f"使用配置的开始时间: {START_DATE}")
        else:
            # 使用years_back计算开始时间
            start_time = int((datetime.now() - timedelta(days=years_back * 365)).timestamp() * 1000)
            logger.info(f"使用years_back计算开始时间: 过去 {years_back} 年")
        
        if END_DATE:
            end_dt = datetime.fromisoformat(END_DATE.replace('Z', '+00:00'))
            end_time = int(end_dt.timestamp() * 1000)
            logger.info(f"使用配置的结束时间: {END_DATE}")
        else:
            end_time = int(datetime.now().timestamp() * 1000)
            logger.info(f"使用当前时间作为结束时间")
        
        all_data = []
        current_start = start_time
        
        while current_start < end_time:
            # 计算当前批次的结束时间 - 使用更小的批次
            batch_size = 500  # 减少批次大小
            current_end = min(current_start + batch_size * self._get_interval_ms(interval), end_time)
            
            logger.info(f"获取数据批次: {datetime.fromtimestamp(current_start/1000)} - {datetime.fromtimestamp(current_end/1000)}")
            
            # 获取数据
            batch_data = self.get_klines_data(symbol, interval, current_start, current_end)
            
            if not batch_data:
                break
                
            all_data.extend(batch_data)
            
            # 更新下一个批次的开始时间
            current_start = batch_data[-1][6] + 1  # 使用最后一条数据的结束时间
            
            # 避免请求过于频繁 - 增加延迟
            time.sleep(REQUEST_DELAY * 2)  # 增加延迟时间
        
        # 转换为DataFrame
        df = self._convert_to_dataframe(all_data)
        logger.info(f"数据收集完成，共获取 {len(df)} 条记录")
        
        return df
    
    def _get_interval_ms(self, interval: str) -> int:
        """将时间间隔转换为毫秒"""
        interval_map = {
            '1m': 60 * 1000,
            '5m': 5 * 60 * 1000,
            '15m': 15 * 60 * 1000,
            '30m': 30 * 60 * 1000,
            '1h': 60 * 60 * 1000,
            '4h': 4 * 60 * 60 * 1000,
            '1d': 24 * 60 * 60 * 1000
        }
        return interval_map.get(interval, 60 * 60 * 1000)
    
    def _convert_to_dataframe(self, klines_data: List[List]) -> pd.DataFrame:
        """
        将币安K线数据转换为DataFrame
        
        币安K线数据格式:
        [
            [开盘时间, 开盘价, 最高价, 最低价, 收盘价, 成交量, 收盘时间, 成交额, 成交笔数, 主动买入成交量, 主动买入成交额, 忽略]
        ]
        """
        if not klines_data:
            return pd.DataFrame()
        
        df = pd.DataFrame(klines_data, columns=[
            'open_time', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_asset_volume', 'trades_count',
            'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
        ])
        
        # 转换数据类型
        df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
        df['close_time'] = pd.to_datetime(df['close_time'], unit='ms')
        
        numeric_columns = ['open', 'high', 'low', 'close', 'volume', 'quote_asset_volume']
        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # 设置时间索引
        df.set_index('open_time', inplace=True)
        df.sort_index(inplace=True)
        
        return df


if __name__ == "__main__":
    # 测试数据采集部
    collector = DataCollector()
    
    # 测试获取1小时数据（最近7天）
    test_df = collector.collect_historical_data("ETHUSDT", "1h", years_back=1)
    print(f"测试结果: 获取到 {len(test_df)} 条记录")
    print(test_df.head())
