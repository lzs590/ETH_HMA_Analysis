# 数据流程图解

## 📊 完整数据流程图

```mermaid
graph TD
    A[币安API] --> B[原始K线数据]
    B --> C[数据验证与清洗]
    C --> D[技术指标计算]
    D --> E[数据标准化]
    E --> F[处理后数据存储]
    F --> G[趋势分析]
    G --> H[分析结果生成]
    H --> I[Dashboard显示]
    
    subgraph "数据采集阶段"
        A
        B
    end
    
    subgraph "数据处理阶段"
        C
        D
        E
        F
    end
    
    subgraph "分析应用阶段"
        G
        H
        I
    end
```

## 🔄 详细数据流说明

### 1. 数据采集阶段

```mermaid
graph LR
    A[币安API请求] --> B[K线数据获取]
    B --> C[原始数据验证]
    C --> D[时间戳转换]
    D --> E[数据类型转换]
    E --> F[原始数据存储]
    
    F --> G[ETHUSDT_4h_raw_*.parquet]
    F --> H[ETHUSDT_1h_raw_*.parquet]
```

### 2. 数据处理阶段

```mermaid
graph TD
    A[原始数据加载] --> B[数据质量检查]
    B --> C[HMA计算]
    C --> D[斜率计算]
    D --> E[其他技术指标]
    E --> F[数据标准化]
    F --> G[处理后数据存储]
    
    G --> H[ETHUSDT_4h_processed_*.parquet]
    G --> I[ETHUSDT_1h_processed_*.parquet]
```

### 3. 分析应用阶段

```mermaid
graph TD
    A[处理后数据] --> B[趋势识别]
    B --> C[转折点检测]
    C --> D[趋势区间分析]
    D --> E[风险收益计算]
    E --> F[分析结果生成]
    
    F --> G[trends_4h_chronological.csv]
    F --> H[trend_analysis_*.json]
    F --> I[risk_trends_detailed_report.txt]
    
    G --> J[Dashboard显示]
    H --> J
    I --> J
```

## 📁 数据存储结构图

```
ETH_HMA_Analysis/
├── 📁 src/utils/data/                    # 核心数据存储
│   ├── 📄 ETHUSDT_1h_raw_*.parquet      # 1小时原始数据
│   ├── 📄 ETHUSDT_1h_processed_*.parquet # 1小时处理后数据
│   ├── 📄 ETHUSDT_4h_raw_*.parquet      # 4小时原始数据
│   └── 📄 ETHUSDT_4h_processed_*.parquet # 4小时处理后数据
├── 📁 assets/reports/                   # 分析结果存储
│   ├── 📄 trends_4h_chronological.csv   # 趋势数据CSV
│   ├── 📄 trend_analysis_*.json         # 趋势分析JSON
│   └── 📄 risk_trends_detailed_report.txt # 风险趋势报告
└── 📁 assets/charts/                    # 图表文件存储
    └── 📄 *.png                         # 分析图表
```

## 🔧 技术指标计算流程

```mermaid
graph TD
    A[价格数据] --> B[WMA计算]
    B --> C[WMA(n/2)计算]
    C --> D[WMA(n)计算]
    D --> E[HMA计算]
    E --> F[斜率计算]
    F --> G[其他指标计算]
    
    G --> H[价格变化率]
    G --> I[成交量指标]
    G --> J[波动率指标]
```

## 📊 数据转换对比表

| 处理阶段 | 数据量 | 文件大小 | 主要变化 | 存储位置 |
|----------|--------|----------|----------|----------|
| 原始数据 | 8,760条(1年4h) | ~2MB | 基础K线数据 | `src/utils/data/` |
| 处理后数据 | 8,760条(1年4h) | ~3MB | +技术指标字段 | `src/utils/data/` |
| 分析结果 | 趋势数量 | ~1MB | 趋势分析结果 | `assets/reports/` |
| 图表文件 | 多个图表 | ~5MB | 可视化图表 | `assets/charts/` |

## 🎯 关键处理参数配置

```yaml
数据处理配置:
  HMA设置:
    周期: 45
    计算方式: WMA(2*WMA(n/2) - WMA(n))
  
  成交量指标:
    移动平均窗口: 20
    计算方式: volume / volume_ma
  
  波动率指标:
    计算窗口: 20
    计算方式: rolling_std
  
  数据存储:
    格式: Parquet
    压缩: snappy
    精度: float32
```

## 🔄 数据更新流程

```mermaid
graph TD
    A[定时任务触发] --> B[检查数据完整性]
    B --> C[获取最新数据]
    C --> D[数据验证]
    D --> E[技术指标计算]
    E --> F[更新处理后数据]
    F --> G[重新分析趋势]
    G --> H[更新Dashboard]
```

## 🚨 错误处理流程

```mermaid
graph TD
    A[数据处理异常] --> B[错误类型判断]
    B --> C[数据质量问题]
    B --> D[计算错误]
    B --> E[存储错误]
    
    C --> F[数据修复]
    D --> G[参数调整]
    E --> H[存储重试]
    
    F --> I[继续处理]
    G --> I
    H --> I
```

## 📈 性能优化建议

### 1. 数据存储优化
- 使用Parquet格式提高读写性能
- 启用数据压缩减少存储空间
- 优化数据类型减少内存占用

### 2. 计算性能优化
- 使用向量化操作替代循环
- 实现增量计算减少重复计算
- 添加缓存机制提高响应速度

### 3. 内存管理优化
- 分批处理大数据集
- 及时释放不需要的数据
- 使用内存映射文件处理大文件

---

*此文档提供了完整的数据流程图解，帮助理解整个数据处理和分析的流程。*
