# API参考文档

## 📚 数据处理API参考

### 🔧 核心模块API

#### 1. 数据采集模块 (`src/collectors/data_collector.py`)

##### `DataCollector` 类

```python
class DataCollector:
    """币安API数据采集器"""
    
    def __init__(self, symbol='ETHUSDT', interval='4h'):
        """
        初始化数据采集器
        
        参数:
        - symbol: 交易对符号 (默认: 'ETHUSDT')
        - interval: 时间间隔 (默认: '4h')
        """
    
    def fetch_klines(self, start_time, end_time, limit=1000):
        """
        获取K线数据
        
        参数:
        - start_time: 开始时间戳 (毫秒)
        - end_time: 结束时间戳 (毫秒)
        - limit: 单次请求限制 (默认: 1000)
        
        返回:
        - DataFrame: K线数据
        """
    
    def fetch_historical_data(self, years_back=1):
        """
        获取历史数据
        
        参数:
        - years_back: 回溯年数 (默认: 1)
        
        返回:
        - DataFrame: 历史K线数据
        """
```

#### 2. 数学计算模块 (`src/eth_hma_analysis/core/math_brain.py`)

##### `MathBrain` 类

```python
class MathBrain:
    """数学计算引擎"""
    
    def calculate_hma(self, prices, period=45):
        """
        计算Hull Moving Average
        
        参数:
        - prices: 价格序列
        - period: HMA周期 (默认: 45)
        
        返回:
        - Series: HMA值
        """
    
    def calculate_wma(self, prices, period):
        """
        计算加权移动平均
        
        参数:
        - prices: 价格序列
        - period: 周期
        
        返回:
        - Series: WMA值
        """
    
    def calculate_slope(self, series):
        """
        计算斜率
        
        参数:
        - series: 数据序列
        
        返回:
        - Series: 斜率值
        """
```

#### 3. 趋势分析模块 (`src/eth_hma_analysis/core/trend_analyzer.py`)

##### `TrendAnalyzer` 类

```python
class TrendAnalyzer:
    """趋势分析器"""
    
    def __init__(self, hma_period=45):
        """
        初始化趋势分析器
        
        参数:
        - hma_period: HMA周期 (默认: 45)
        """
    
    def identify_turning_points(self, df):
        """
        识别转折点
        
        参数:
        - df: 包含HMA数据的DataFrame
        
        返回:
        - DataFrame: 包含转折点标记的数据
        """
    
    def analyze_trend_intervals(self, df):
        """
        分析趋势区间
        
        参数:
        - df: 包含转折点的DataFrame
        
        返回:
        - dict: 趋势分析结果
        """
    
    def calculate_pfe_mae(self, start_price, high_price, low_price, trend_direction):
        """
        计算PFE和MAE
        
        参数:
        - start_price: 起始价格
        - high_price: 最高价格
        - low_price: 最低价格
        - trend_direction: 趋势方向 ('up'/'down')
        
        返回:
        - tuple: (PFE, MAE)
        """
```

#### 4. 项目管理模块 (`src/managers/project_manager.py`)

##### `ProjectManager` 类

```python
class ProjectManager:
    """项目管理器"""
    
    def __init__(self):
        """初始化项目管理器"""
    
    def collect_data(self, symbol='ETHUSDT', interval='4h', years_back=1):
        """
        采集数据
        
        参数:
        - symbol: 交易对
        - interval: 时间间隔
        - years_back: 回溯年数
        
        返回:
        - str: 数据文件路径
        """
    
    def process_data(self, raw_data_path):
        """
        处理数据
        
        参数:
        - raw_data_path: 原始数据路径
        
        返回:
        - str: 处理后数据路径
        """
    
    def run_analysis(self, processed_data_path):
        """
        运行分析
        
        参数:
        - processed_data_path: 处理后数据路径
        
        返回:
        - dict: 分析结果
        """
```

### 📊 数据处理函数API

#### 数据验证函数

```python
def validate_and_convert_data(raw_data):
    """
    验证和转换数据
    
    参数:
    - raw_data: 原始数据DataFrame
    
    返回:
    - DataFrame: 验证后的数据
    """
    
def data_quality_check(df):
    """
    数据质量检查
    
    参数:
    - df: 数据DataFrame
    
    返回:
    - dict: 质量检查报告
    """
```

#### 技术指标计算函数

```python
def calculate_technical_indicators(df):
    """
    计算技术指标
    
    参数:
    - df: 价格数据DataFrame
    
    返回:
    - DataFrame: 包含技术指标的数据
    """
    
def calculate_hma(prices, period=45):
    """
    计算HMA
    
    参数:
    - prices: 价格序列
    - period: 周期
    
    返回:
    - Series: HMA值
    """
```

#### 数据存储函数

```python
def save_processed_data(df, symbol, interval, timestamp):
    """
    保存处理后数据
    
    参数:
    - df: 处理后数据DataFrame
    - symbol: 交易对
    - interval: 时间间隔
    - timestamp: 时间戳
    
    返回:
    - tuple: (文件路径, 元数据)
    """
    
def load_processed_data(file_path):
    """
    加载处理后数据
    
    参数:
    - file_path: 文件路径
    
    返回:
    - DataFrame: 处理后数据
    """
```

### 🔧 配置参数API

#### 配置文件 (`src/utils/config.py`)

```python
# 交易对配置
SYMBOL = 'ETHUSDT'

# 时间间隔配置
INTERVALS = ['1h', '4h', '1d']

# 回溯年数配置
YEARS_BACK = 1

# HMA参数配置
HMA_PERIOD = 45

# 数据存储路径
DATA_DIR = 'src/utils/data'
REPORTS_DIR = 'assets/reports'
CHARTS_DIR = 'assets/charts'
```

### 📈 可视化API

#### 趋势可视化 (`src/analyzers/trend_visualizer.py`)

```python
class TrendVisualizer:
    """趋势可视化器"""
    
    def __init__(self, use_chinese=True):
        """
        初始化可视化器
        
        参数:
        - use_chinese: 是否使用中文 (默认: True)
        """
    
    def plot_turning_points(self, df, output_path):
        """
        绘制转折点图
        
        参数:
        - df: 包含转折点的数据
        - output_path: 输出路径
        """
    
    def plot_trend_intervals(self, intervals, output_path):
        """
        绘制趋势区间图
        
        参数:
        - intervals: 趋势区间数据
        - output_path: 输出路径
        """
```

#### 策略可视化 (`src/visualizers/strategy_visualizer.py`)

```python
class StrategyVisualizer:
    """策略可视化器"""
    
    def plot_strategy_overview(self, analysis_results, output_path):
        """
        绘制策略概览图
        
        参数:
        - analysis_results: 分析结果
        - output_path: 输出路径
        """
    
    def plot_performance_analysis(self, analysis_results, output_path):
        """
        绘制性能分析图
        
        参数:
        - analysis_results: 分析结果
        - output_path: 输出路径
        """
```

### 📊 Dashboard API

#### Dashboard启动 (`dashboard/financial_dashboard_fixed.py`)

```python
def load_trend_data():
    """
    加载趋势数据
    
    返回:
    - DataFrame: 趋势数据
    """
    
def create_visualizations(df):
    """
    创建可视化图表
    
    参数:
    - df: 趋势数据DataFrame
    
    返回:
    - dict: 图表对象
    """
```

### 🚀 快速启动API

#### 主脚本 (`scripts/main.py`)

```python
def main():
    """
    主函数 - 数据采集和处理
    """
    
def collect_and_process_data():
    """
    采集和处理数据
    
    返回:
    - str: 处理后数据路径
    """
```

#### 趋势分析脚本 (`scripts/trend_analysis.py`)

```python
def run_trend_analysis(data_path):
    """
    运行趋势分析
    
    参数:
    - data_path: 数据文件路径
    
    返回:
    - dict: 分析结果
    """
    
def generate_reports(analysis_results):
    """
    生成报告
    
    参数:
    - analysis_results: 分析结果
    
    返回:
    - str: 报告文件路径
    """
```

### 🔧 工具函数API

#### 数据查看器 (`src/utils/data_viewer.py`)

```python
class DataViewer:
    """数据查看器"""
    
    def display_data_summary(self, df):
        """
        显示数据摘要
        
        参数:
        - df: 数据DataFrame
        """
    
    def check_data_quality(self, df):
        """
        检查数据质量
        
        参数:
        - df: 数据DataFrame
        
        返回:
        - dict: 质量检查结果
        """
```

#### 字体配置 (`src/utils/matplotlib_config.py`)

```python
class MatplotlibConfig:
    """Matplotlib配置类"""
    
    @staticmethod
    def setup_chinese_font():
        """设置中文字体"""
    
    @staticmethod
    def setup_english_font():
        """设置英文字体"""
    
    @staticmethod
    def load_project_config():
        """加载项目配置"""
```

### 📋 错误处理API

#### 异常处理

```python
class DataProcessingError(Exception):
    """数据处理异常"""
    pass

class AnalysisError(Exception):
    """分析异常"""
    pass

class VisualizationError(Exception):
    """可视化异常"""
    pass
```

#### 错误处理函数

```python
def handle_api_error(error):
    """
    处理API错误
    
    参数:
    - error: API错误
    
    返回:
    - bool: 是否重试
    """
    
def handle_data_validation_error(error):
    """
    处理数据验证错误
    
    参数:
    - error: 验证错误
    
    返回:
    - DataFrame: 修复后的数据
    """
```

---

## 📚 使用示例

### 基本使用示例

```python
# 1. 数据采集
from src.collectors.data_collector import DataCollector
collector = DataCollector('ETHUSDT', '4h')
data = collector.fetch_historical_data(years_back=1)

# 2. 数据处理
from src.eth_hma_analysis.core.math_brain import MathBrain
math_brain = MathBrain()
data['HMA'] = math_brain.calculate_hma(data['close'], period=45)

# 3. 趋势分析
from src.eth_hma_analysis.core.trend_analyzer import TrendAnalyzer
analyzer = TrendAnalyzer()
results = analyzer.analyze_trend_intervals(data)

# 4. 可视化
from src.analyzers.trend_visualizer import TrendVisualizer
visualizer = TrendVisualizer()
visualizer.plot_turning_points(data, 'output.png')
```

### 高级使用示例

```python
# 完整的数据处理流程
from src.managers.project_manager import ProjectManager

# 初始化项目管理器
pm = ProjectManager()

# 采集数据
raw_data_path = pm.collect_data('ETHUSDT', '4h', 1)

# 处理数据
processed_data_path = pm.process_data(raw_data_path)

# 运行分析
analysis_results = pm.run_analysis(processed_data_path)

# 生成报告
from src.reporters.strategy_reporter import StrategyReporter
reporter = StrategyReporter()
report_path = reporter.generate_report(analysis_results)
```

---

*此API参考文档提供了完整的数据处理和分析功能的接口说明，任何AI代码代理都可以根据此文档快速理解和使用项目功能。*
