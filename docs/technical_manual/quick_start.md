# 快速开始指南

## 🚀 5分钟快速上手

### 第一步: 环境准备

```bash
# 1. 克隆项目 (如果还没有)
git clone https://github.com/lzs590/ETH_HMA_Analysis.git
cd ETH_HMA_Analysis

# 2. 创建虚拟环境
python -m venv venv

# 3. 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 4. 安装依赖
pip install -r requirements.txt
```

### 第二步: 数据采集

```bash
# 运行数据采集 (自动采集过去3年的4小时数据)
python scripts/main.py
```

**等待时间**: 约2-5分钟 (取决于网络速度)

### 第三步: 趋势分析

```bash
# 运行趋势分析
python scripts/trend_analysis.py --interval 4h
```

**等待时间**: 约1-2分钟

### 第四步: 启动Dashboard

```bash
# 启动Financial Dashboard
streamlit run dashboard/financial_dashboard_fixed.py
```

**访问地址**: http://localhost:8501

## 📊 查看结果

### 1. 数据文件位置
- **原始数据**: `src/utils/data/ETHUSDT_4h_raw_*.parquet`
- **处理后数据**: `src/utils/data/ETHUSDT_4h_processed_*.parquet`
- **分析结果**: `assets/reports/trend_analysis_4h_*.json`
- **CSV数据**: `assets/reports/trends_4h_chronological.csv`

### 2. 图表文件
- **趋势图表**: `assets/charts/turning_points_4h_*.png`
- **策略图表**: `assets/charts/strategy_*.png`
- **综合分析**: `assets/charts/comprehensive_analysis_4h_*.png`

### 3. 报告文件
- **详细报告**: `assets/reports/ETH_HMA_4h_Detailed_Research_Report.md`
- **风险报告**: `assets/reports/risk_trends_detailed_report.txt`

## 🎯 核心功能使用

### 数据采集
```python
from src.managers.project_manager import ProjectManager

# 初始化
manager = ProjectManager()

# 采集数据
result = manager.process_single_interval("ETHUSDT", "4h", 3)
print(f"采集完成: {result}")
```

### 趋势分析
```python
from src.analyzers.trend_analyzer import TrendAnalyzer
import pandas as pd

# 加载数据
data = pd.read_parquet('src/utils/data/ETHUSDT_4h_processed_*.parquet')

# 分析趋势
analyzer = TrendAnalyzer()
results = analyzer.run_complete_analysis(data)
```

### 可视化
```python
from src.analyzers.trend_visualizer import TrendVisualizer

# 创建可视化
visualizer = TrendVisualizer(use_chinese=True)
visualizer.plot_turning_points(data, results['turning_points'])
```

## 🔧 常用命令

### 数据相关
```bash
# 采集1小时数据
python scripts/main.py --interval 1h

# 采集4小时数据
python scripts/main.py --interval 4h

# 采集指定年数数据
python scripts/main.py --years 5
```

### 分析相关
```bash
# 运行1小时分析
python scripts/trend_analysis.py --interval 1h

# 运行4小时分析
python scripts/trend_analysis.py --interval 4h

# 生成英文报告
python scripts/trend_analysis.py --interval 4h --english

# 详细输出
python scripts/trend_analysis.py --interval 4h --verbose
```

### Dashboard相关
```bash
# 启动Dashboard
streamlit run dashboard/financial_dashboard_fixed.py

# 指定端口
streamlit run dashboard/financial_dashboard_fixed.py --server.port 8502

# 后台运行
streamlit run dashboard/financial_dashboard_fixed.py --server.headless true
```

## 📋 检查清单

### ✅ 环境检查
- [ ] Python 3.8+ 已安装
- [ ] 虚拟环境已创建并激活
- [ ] 依赖包已安装
- [ ] 网络连接正常

### ✅ 数据检查
- [ ] 原始数据文件存在
- [ ] 处理后数据文件存在
- [ ] 数据时间范围正确
- [ ] 数据质量良好

### ✅ 分析检查
- [ ] 趋势分析完成
- [ ] JSON报告生成
- [ ] CSV数据导出
- [ ] 图表文件生成

### ✅ Dashboard检查
- [ ] Dashboard启动成功
- [ ] 数据加载正常
- [ ] 图表显示正确
- [ ] 筛选功能工作

## 🐛 快速故障排除

### 问题1: 数据采集失败
```bash
# 检查网络连接
ping api.binance.com

# 检查API状态
curl https://api.binance.com/api/v3/ping
```

### 问题2: 分析失败
```bash
# 检查数据文件
ls -la src/utils/data/

# 检查数据格式
python -c "import pandas as pd; print(pd.read_parquet('src/utils/data/ETHUSDT_4h_processed_*.parquet').head())"
```

### 问题3: Dashboard不显示
```bash
# 检查数据文件
ls -la assets/reports/trends_4h_chronological.csv

# 检查端口占用
netstat -an | findstr 8501
```

### 问题4: 中文显示问题
```bash
# 检查字体配置
python -c "import matplotlib.pyplot as plt; print(plt.rcParams['font.sans-serif'])"
```

## 📞 获取帮助

### 查看日志
```bash
# 查看分析日志
tail -f assets/logs/eth_hma_analysis.log

# 查看趋势分析日志
tail -f assets/logs/trend_analysis.log
```

### 调试模式
```bash
# 启用调试输出
python scripts/trend_analysis.py --interval 4h --verbose

# 检查数据质量
python -c "
import pandas as pd
df = pd.read_parquet('src/utils/data/ETHUSDT_4h_processed_*.parquet')
print(f'数据形状: {df.shape}')
print(f'时间范围: {df.index.min()} 到 {df.index.max()}')
print(f'缺失值: {df.isnull().sum().sum()}')
"
```

### 重置环境
```bash
# 清理缓存
rm -rf __pycache__ src/__pycache__

# 重新安装依赖
pip install -r requirements.txt --force-reinstall

# 重新运行分析
python scripts/trend_analysis.py --interval 4h
```

## 🎯 下一步

### 深入学习
1. 阅读 [数据分析指南](analysis_guide.md)
2. 了解 [Dashboard使用指南](dashboard_guide.md)
3. 掌握 [数据采集指南](data_collection_guide.md)

### 自定义配置
1. 修改 `src/utils/config.py` 中的参数
2. 调整HMA周期和阈值
3. 自定义可视化样式

### 扩展功能
1. 添加新的技术指标
2. 实现策略回测
3. 集成实时数据

---

*最后更新: 2025-09-27*
*版本: v1.0.0*
