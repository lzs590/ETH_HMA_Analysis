"""
分析计算部 (The Math Brain)
专门负责进行复杂的数学计算，计算HMA指标
"""
import pandas as pd
import numpy as np
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class MathBrain:
    """分析计算部 - 负责计算HMA技术指标"""
    
    def __init__(self, hma_period: int = 45):
        """
        初始化计算引擎
        
        Args:
            hma_period: HMA周期参数
        """
        self.hma_period = hma_period
        logger.info(f"数学计算引擎初始化，HMA周期: {hma_period}")
    
    def calculate_wma(self, data: pd.Series, period: int) -> pd.Series:
        """
        计算加权移动平均 (Weighted Moving Average)
        
        Args:
            data: 价格数据序列
            period: 周期
            
        Returns:
            WMA序列
        """
        if len(data) < period:
            return pd.Series(index=data.index, dtype=float)
        
        weights = np.arange(1, period + 1)
        wma = data.rolling(window=period).apply(
            lambda x: np.average(x, weights=weights), raw=True
        )
        
        return wma
    
    def calculate_hma(self, data: pd.Series, period: int) -> pd.Series:
        """
        计算Hull移动平均 (Hull Moving Average)
        
        HMA公式:
        1. WMA1 = WMA(close, period/2)
        2. WMA2 = WMA(close, period)
        3. RawHMA = 2 * WMA1 - WMA2
        4. HMA = WMA(RawHMA, sqrt(period))
        
        Args:
            data: 价格数据序列
            period: HMA周期
            
        Returns:
            HMA序列
        """
        if len(data) < period:
            logger.warning(f"数据长度 {len(data)} 小于HMA周期 {period}")
            return pd.Series(index=data.index, dtype=float)
        
        # 步骤1: 计算WMA1 (周期为period/2)
        half_period = max(1, period // 2)
        wma1 = self.calculate_wma(data, half_period)
        
        # 步骤2: 计算WMA2 (周期为period)
        wma2 = self.calculate_wma(data, period)
        
        # 步骤3: 计算RawHMA = 2 * WMA1 - WMA2
        raw_hma = 2 * wma1 - wma2
        
        # 步骤4: 计算最终HMA = WMA(RawHMA, sqrt(period))
        sqrt_period = max(1, int(np.sqrt(period)))
        hma = self.calculate_wma(raw_hma, sqrt_period)
        
        return hma
    
    def add_hma_to_dataframe(self, df: pd.DataFrame, price_column: str = 'close') -> pd.DataFrame:
        """
        为DataFrame添加HMA列
        
        Args:
            df: 包含价格数据的DataFrame
            price_column: 用于计算HMA的价格列名
            
        Returns:
            添加了HMA列的DataFrame
        """
        if price_column not in df.columns:
            raise ValueError(f"价格列 '{price_column}' 不存在于DataFrame中")
        
        logger.info(f"开始计算HMA指标，使用列: {price_column}")
        
        # 计算HMA
        hma_values = self.calculate_hma(df[price_column], self.hma_period)
        
        # 添加HMA列到DataFrame
        hma_column_name = f"HMA_{self.hma_period}"
        df[hma_column_name] = hma_values
        
        # 统计有效HMA值的数量
        valid_hma_count = hma_values.notna().sum()
        logger.info(f"HMA计算完成，有效值数量: {valid_hma_count}/{len(df)}")
        
        return df
    
    def calculate_additional_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        计算HMA相关的必要指标
        
        Args:
            df: 包含价格数据的DataFrame
            
        Returns:
            添加了HMA相关指标的DataFrame
        """
        logger.info("计算HMA相关指标")
        
        # 计算价格变化率
        df['price_change'] = df['close'].pct_change()
        
        # 计算HMA与价格的偏离度
        if f'HMA_{self.hma_period}' in df.columns:
            hma_col = f'HMA_{self.hma_period}'
            df['hma_deviation'] = ((df['close'] - df[hma_col]) / df[hma_col] * 100)
        
        logger.info("HMA相关指标计算完成")
        return df
    
    def validate_data(self, df: pd.DataFrame) -> bool:
        """
        验证数据质量
        
        Args:
            df: 要验证的DataFrame
            
        Returns:
            数据是否有效
        """
        if df.empty:
            logger.error("DataFrame为空")
            return False
        
        # 检查必要的列
        required_columns = ['open', 'high', 'low', 'close', 'volume']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            logger.error(f"缺少必要的列: {missing_columns}")
            return False
        
        # 检查数据完整性
        null_counts = df[required_columns].isnull().sum()
        if null_counts.any():
            logger.warning(f"发现空值: {null_counts[null_counts > 0].to_dict()}")
        
        # 检查价格数据的合理性
        if (df['high'] < df['low']).any():
            logger.error("发现高价低于低价的异常数据")
            return False
        
        if (df['close'] <= 0).any():
            logger.error("发现非正数的收盘价")
            return False
        
        logger.info("数据验证通过")
        return True


if __name__ == "__main__":
    # 测试数学计算部
    import numpy as np
    
    # 创建测试数据
    dates = pd.date_range('2023-01-01', periods=100, freq='1H')
    test_data = pd.DataFrame({
        'open': 100 + np.random.randn(100) * 5,
        'high': 105 + np.random.randn(100) * 5,
        'low': 95 + np.random.randn(100) * 5,
        'close': 100 + np.random.randn(100) * 5,
        'volume': np.random.randint(1000, 10000, 100)
    }, index=dates)
    
    # 确保高价>=低价
    test_data['high'] = np.maximum(test_data['high'], test_data['low'])
    test_data['low'] = np.minimum(test_data['high'], test_data['low'])
    
    # 测试HMA计算
    math_brain = MathBrain(hma_period=45)
    result_df = math_brain.add_hma_to_dataframe(test_data)
    
    print("测试结果:")
    print(result_df[['close', 'HMA_45']].tail(10))
