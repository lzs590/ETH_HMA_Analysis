# ETH HMA 数据分析 - Jupyter Notebook 使用指南

## 🚀 快速开始

### 方法1: 使用启动脚本（推荐）
```bash
python3 start_jupyter.py
```

### 方法2: 手动启动
```bash
# 安装Jupyter依赖
pip3 install -r requirements_jupyter.txt

# 启动Jupyter Notebook
jupyter notebook
```

## 📊 Notebook功能说明

### 1. 数据加载和概览
- 自动加载1小时和4小时ETH数据
- 显示数据基本信息和统计
- 检查数据质量

### 2. 价格走势可视化
- ETH价格历史走势图
- 价格与HMA指标对比
- 成交量和波动率分析

### 3. 技术指标分析
- HMA、SMA等移动平均线对比
- 技术指标有效性分析
- 指标与价格关系研究

### 4. 价格变化分析
- 价格变化分布统计
- 波动率分析
- 价格与波动率关系

### 5. 交易信号分析
- 基于HMA的交易信号生成
- 信号有效性验证
- 买卖点标记

### 6. 相关性分析
- 各变量间相关性热力图
- 关键指标相关性分析

### 7. 时间序列分析
- 月度价格表现分析
- 季节性特征识别
- 时间模式分析

### 8. 策略回测
- 简单HMA策略回测
- 策略表现评估
- 与买入持有策略对比

## 🔧 使用技巧

### 1. 交互式分析
- 修改参数重新运行单元格
- 添加新的分析代码
- 实时查看结果

### 2. 数据探索
```python
# 查看特定时间段数据
df_1h['2024-01-01':'2024-12-31'].head()

# 计算自定义指标
df_1h['custom_indicator'] = df_1h['close'] / df_1h['HMA_45']

# 筛选特定条件的数据
high_volatility = df_1h[df_1h['volatility'] > df_1h['volatility'].quantile(0.9)]
```

### 3. 自定义可视化
```python
# 创建自定义图表
plt.figure(figsize=(12, 6))
plt.plot(df_1h.index, df_1h['close'], label='价格')
plt.plot(df_1h.index, df_1h['HMA_45'], label='HMA')
plt.title('自定义分析')
plt.legend()
plt.show()
```

### 4. 策略开发
```python
# 实现自定义策略
def my_strategy(df):
    # 您的策略逻辑
    signals = []
    for i in range(len(df)):
        if df.iloc[i]['close'] > df.iloc[i]['HMA_45']:
            signals.append(1)  # 买入
        else:
            signals.append(-1)  # 卖出
    return signals
```

## 📈 分析建议

### 1. 基础分析
- 先运行所有单元格了解数据
- 观察价格走势和技术指标
- 分析交易信号的有效性

### 2. 深入分析
- 修改HMA参数测试不同周期
- 添加更多技术指标
- 实现更复杂的交易策略

### 3. 策略优化
- 调整买卖信号条件
- 添加止损止盈机制
- 考虑交易成本

### 4. 风险管理
- 分析最大回撤
- 计算夏普比率
- 评估策略稳定性

## 🛠️ 故障排除

### 1. 导入错误
```bash
pip3 install --upgrade pandas numpy matplotlib seaborn
```

### 2. 数据文件找不到
确保data目录中有以下文件：
- ETHUSDT_1h_processed_*.parquet
- ETHUSDT_4h_processed_*.parquet

### 3. 图表不显示
```python
# 在Notebook中添加
%matplotlib inline
```

### 4. 内存不足
```python
# 使用更少的数据
df_sample = df_1h.iloc[::10]  # 每10条取1条
```

## 📚 扩展功能

### 1. 添加更多数据源
- 其他交易所数据
- 宏观经济数据
- 新闻情绪数据

### 2. 机器学习预测
- 使用scikit-learn
- 实现LSTM预测
- 集成学习模型

### 3. 实时数据
- 连接实时API
- 自动更新数据
- 实时策略执行

### 4. 回测框架
- 使用backtrader
- 实现更复杂的回测
- 多策略组合

## 💡 最佳实践

1. **定期保存**: 经常保存Notebook
2. **版本控制**: 使用Git管理代码
3. **文档记录**: 添加详细注释
4. **测试验证**: 验证策略逻辑
5. **风险控制**: 始终考虑风险管理

开始您的量化分析之旅吧！🚀
