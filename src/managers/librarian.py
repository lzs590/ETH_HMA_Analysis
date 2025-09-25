"""
档案管理部 (The Librarian)
专门负责把最终的结果安全、高效地保存起来
"""
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from pathlib import Path
from datetime import datetime
import logging
from typing import Optional, Dict, Any
import json

logger = logging.getLogger(__name__)


class Librarian:
    """档案管理部 - 负责数据存储和文件管理"""
    
    def __init__(self, data_dir: Path):
        """
        初始化档案管理系统
        
        Args:
            data_dir: 数据存储目录
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        logger.info(f"档案管理系统初始化，数据目录: {self.data_dir}")
    
    def generate_filename(self, symbol: str, interval: str, data_type: str = "processed") -> str:
        """
        生成标准化的文件名
        
        Args:
            symbol: 交易对符号 (如 'ETHUSDT')
            interval: 时间间隔 (如 '1h', '4h')
            data_type: 数据类型 ('raw' 或 'processed')
            
        Returns:
            标准化的文件名
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{symbol}_{interval}_{data_type}_{timestamp}.parquet"
    
    def save_dataframe(self, df: pd.DataFrame, filename: str, 
                      metadata: Optional[Dict[str, Any]] = None) -> Path:
        """
        将DataFrame保存为Parquet格式
        
        Args:
            df: 要保存的DataFrame
            filename: 文件名
            metadata: 可选的元数据
            
        Returns:
            保存文件的完整路径
        """
        file_path = self.data_dir / filename
        
        try:
            # 确保DataFrame的索引是datetime类型
            if not isinstance(df.index, pd.DatetimeIndex):
                logger.warning("DataFrame索引不是DatetimeIndex，尝试转换")
                df.index = pd.to_datetime(df.index)
            
            # 重置索引，将时间索引作为列保存
            df_to_save = df.reset_index()
            
            # 创建元数据
            file_metadata = {
                'created_at': datetime.now().isoformat(),
                'rows': len(df),
                'columns': list(df.columns),
                'index_name': df.index.name,
                'data_types': {col: str(dtype) for col, dtype in df.dtypes.items()}
            }
            
            if metadata:
                file_metadata.update(metadata)
            
            # 保存为Parquet格式
            table = pa.Table.from_pandas(df_to_save)
            
            # 添加元数据到Parquet文件
            table = table.replace_schema_metadata({
                'metadata': json.dumps(file_metadata, ensure_ascii=False)
            })
            
            pq.write_table(table, file_path, compression='snappy')
            
            logger.info(f"数据保存成功: {file_path}")
            logger.info(f"文件大小: {file_path.stat().st_size / 1024 / 1024:.2f} MB")
            
            return file_path
            
        except Exception as e:
            logger.error(f"保存数据失败: {e}")
            raise
    
    def load_dataframe(self, filename: str) -> pd.DataFrame:
        """
        从Parquet文件加载DataFrame
        
        Args:
            filename: 文件名
            
        Returns:
            加载的DataFrame
        """
        file_path = self.data_dir / filename
        
        if not file_path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        try:
            # 读取Parquet文件
            table = pq.read_table(file_path)
            df = table.to_pandas()
            
            # 恢复时间索引
            if 'open_time' in df.columns:
                df.set_index('open_time', inplace=True)
                df.index = pd.to_datetime(df.index)
            
            logger.info(f"数据加载成功: {file_path}")
            logger.info(f"数据形状: {df.shape}")
            
            return df
            
        except Exception as e:
            logger.error(f"加载数据失败: {e}")
            raise
    
    def save_raw_data(self, df: pd.DataFrame, symbol: str, interval: str) -> Path:
        """
        保存原始数据
        
        Args:
            df: 原始数据DataFrame
            symbol: 交易对符号
            interval: 时间间隔
            
        Returns:
            保存文件的路径
        """
        filename = self.generate_filename(symbol, interval, "raw")
        metadata = {
            'data_type': 'raw',
            'symbol': symbol,
            'interval': interval,
            'description': '从币安获取的原始K线数据'
        }
        
        return self.save_dataframe(df, filename, metadata)
    
    def save_processed_data(self, df: pd.DataFrame, symbol: str, interval: str, 
                          hma_period: int) -> Path:
        """
        保存处理后的数据（包含HMA指标）
        
        Args:
            df: 处理后的数据DataFrame
            symbol: 交易对符号
            interval: 时间间隔
            hma_period: HMA周期
            
        Returns:
            保存文件的路径
        """
        filename = self.generate_filename(symbol, interval, "processed")
        metadata = {
            'data_type': 'processed',
            'symbol': symbol,
            'interval': interval,
            'hma_period': hma_period,
            'description': f'包含HMA_{hma_period}指标的处理后数据'
        }
        
        return self.save_dataframe(df, filename, metadata)
    
    def list_files(self, pattern: str = "*") -> list:
        """
        列出数据目录中的文件
        
        Args:
            pattern: 文件名模式
            
        Returns:
            文件路径列表
        """
        files = list(self.data_dir.glob(f"{pattern}.parquet"))
        logger.info(f"找到 {len(files)} 个文件")
        return files
    
    def get_file_info(self, file_path: Path) -> Dict[str, Any]:
        """
        获取文件信息
        
        Args:
            file_path: 文件路径
            
        Returns:
            文件信息字典
        """
        if not file_path.exists():
            return {}
        
        try:
            # 读取Parquet文件元数据
            parquet_file = pq.ParquetFile(file_path)
            metadata = parquet_file.metadata
            
            # 获取自定义元数据
            custom_metadata = {}
            if metadata.metadata:
                custom_metadata = json.loads(metadata.metadata.get(b'metadata', b'{}').decode('utf-8'))
            
            file_info = {
                'file_size_mb': file_path.stat().st_size / 1024 / 1024,
                'rows': metadata.num_rows,
                'columns': metadata.num_columns,
                'created_at': custom_metadata.get('created_at'),
                'data_type': custom_metadata.get('data_type'),
                'symbol': custom_metadata.get('symbol'),
                'interval': custom_metadata.get('interval'),
                'hma_period': custom_metadata.get('hma_period')
            }
            
            return file_info
            
        except Exception as e:
            logger.error(f"获取文件信息失败: {e}")
            return {}
    
    def cleanup_old_files(self, days_to_keep: int = 30) -> int:
        """
        清理旧文件
        
        Args:
            days_to_keep: 保留多少天的文件
            
        Returns:
            删除的文件数量
        """
        cutoff_time = datetime.now().timestamp() - (days_to_keep * 24 * 3600)
        deleted_count = 0
        
        for file_path in self.data_dir.glob("*.parquet"):
            if file_path.stat().st_mtime < cutoff_time:
                try:
                    file_path.unlink()
                    deleted_count += 1
                    logger.info(f"删除旧文件: {file_path.name}")
                except Exception as e:
                    logger.error(f"删除文件失败 {file_path.name}: {e}")
        
        logger.info(f"清理完成，删除了 {deleted_count} 个文件")
        return deleted_count


if __name__ == "__main__":
    # 测试档案管理部
    from pathlib import Path
    import pandas as pd
    import numpy as np
    
    # 创建测试数据
    dates = pd.date_range('2023-01-01', periods=100, freq='1H')
    test_data = pd.DataFrame({
        'open': 100 + np.random.randn(100) * 5,
        'high': 105 + np.random.randn(100) * 5,
        'low': 95 + np.random.randn(100) * 5,
        'close': 100 + np.random.randn(100) * 5,
        'volume': np.random.randint(1000, 10000, 100),
        'HMA_45': 100 + np.random.randn(100) * 2
    }, index=dates)
    
    # 测试档案管理
    librarian = Librarian(Path("./test_data"))
    
    # 保存原始数据
    raw_file = librarian.save_raw_data(test_data, "ETHUSDT", "1h")
    print(f"原始数据保存到: {raw_file}")
    
    # 保存处理后数据
    processed_file = librarian.save_processed_data(test_data, "ETHUSDT", "1h", 45)
    print(f"处理后数据保存到: {processed_file}")
    
    # 列出文件
    files = librarian.list_files()
    print(f"数据目录中的文件: {[f.name for f in files]}")
    
    # 获取文件信息
    for file_path in files:
        info = librarian.get_file_info(file_path)
        print(f"文件信息 {file_path.name}: {info}")
