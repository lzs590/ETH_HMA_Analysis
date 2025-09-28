# Financial Dashboard 使用指南

## 🚀 Dashboard 启动指南

### 快速启动

```bash
# 方法1: 直接启动
streamlit run dashboard/financial_dashboard_fixed.py

# 方法2: 后台启动
streamlit run dashboard/financial_dashboard_fixed.py --server.headless true
```

### 访问地址

- **本地访问**: http://localhost:8501
- **网络访问**: http://[您的IP]:8501
- **默认端口**: 8501

### 🔧 环境配置

#### 依赖安装
```bash
# 安装Dashboard依赖
pip install -r requirements_dashboard.txt

# 或单独安装
pip install streamlit plotly pandas numpy
```

#### 数据准备
```bash
# 确保数据文件存在
ls assets/reports/trends_4h_chronological.csv

# 如果不存在，先运行分析
python scripts/trend_analysis.py --interval 4h
```

## 📊 Dashboard 功能详解

### 🎛️ 控制面板 (左侧)

#### 1. 时间范围筛选器
```python
# 功能: 选择分析时间段
date_range = st.sidebar.date_input(
    "📅 时间范围",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)
```

**使用方法**:
- 点击日期选择器
- 选择开始和结束日期
- 实时更新图表和数据

#### 2. 趋势类型筛选器
```python
# 功能: 筛选上升/下降趋势
trend_types = st.sidebar.multiselect(
    "📊 趋势类型",
    options=['上升趋势', '下降趋势'],
    default=['上升趋势', '下降趋势']
)
```

**选项**:
- ✅ 上升趋势: 显示所有上升趋势
- ✅ 下降趋势: 显示所有下降趋势
- 可多选或单选

#### 3. 风险等级筛选器
```python
# 功能: 筛选风险等级
risk_filter = st.sidebar.selectbox(
    "⚠️ 风险等级",
    options=['全部', '高风险', '低风险'],
    index=0
)
```

**选项**:
- **全部**: 显示所有趋势
- **高风险**: 只显示风险大于收益的趋势
- **低风险**: 只显示风险小于收益的趋势

#### 4. 持续时间滑块
```python
# 功能: 设置趋势持续时间范围
duration_range = st.sidebar.slider(
    "⏱️ 持续时间 (小时)",
    min_value=duration_min,
    max_value=duration_max,
    value=(duration_min, duration_max)
)
```

**使用方法**:
- 拖动滑块设置最小/最大持续时间
- 实时筛选数据

#### 5. 价格变化滑块
```python
# 功能: 设置价格变化幅度范围
price_change_range = st.sidebar.slider(
    "💰 价格变化 (%)",
    min_value=price_min,
    max_value=price_max,
    value=(price_min, price_max)
)
```

### 📈 关键指标面板

#### 指标说明
```python
# 总趋势数
st.metric("📈 总趋势数", value=f"{len(df):,}")

# 上升趋势
uptrends = len(df[df['trend_type'] == '上升趋势'])
st.metric("📈 上升趋势", value=f"{uptrends:,}", delta=f"{uptrends/len(df)*100:.1f}%")

# 下降趋势
downtrends = len(df[df['trend_type'] == '下降趋势'])
st.metric("📉 下降趋势", value=f"{downtrends:,}", delta=f"{downtrends/len(df)*100:.1f}%")

# 高风险趋势
risk_trends = len(df[df['is_risk_greater'] == True])
st.metric("⚠️ 高风险趋势", value=f"{risk_trends:,}", delta=f"{risk_trends/len(df)*100:.1f}%")

# 平均持续时间
avg_duration = df['duration_hours'].mean()
st.metric("⏱️ 平均持续时间", value=f"{avg_duration:.1f}h")
```

### 📊 专业图表

#### 1. 趋势类型分布饼图
```python
fig_pie = px.pie(
    df, 
    names='trend_type', 
    title="📊 趋势类型分布",
    color_discrete_map={'上升趋势': '#2ca02c', '下降趋势': '#d62728'}
)
```

**功能**:
- 显示上升/下降趋势占比
- 颜色编码: 绿色=上升，红色=下降
- 交互式图表，可点击查看详情

#### 2. 风险分布饼图
```python
fig_risk = px.pie(
    values=df['is_risk_greater'].value_counts().values,
    names=['低风险', '高风险'],
    title="⚠️ 风险分布",
    color_discrete_map={'低风险': '#2ca02c', '高风险': '#d62728'}
)
```

**功能**:
- 显示高风险/低风险趋势占比
- 风险警示功能

#### 3. 价格变化时间序列
```python
fig_price = px.line(
    df, 
    x='start_time', 
    y='price_change_pct',
    color='trend_type',
    title="💰 价格变化时间序列",
    color_discrete_map={'上升趋势': '#2ca02c', '下降趋势': '#d62728'}
)
```

**功能**:
- 显示价格变化的时间趋势
- 区分上升/下降趋势
- 添加零线参考

#### 4. 持续时间分布直方图
```python
fig_duration = px.histogram(
    df,
    x='duration_hours',
    color='trend_type',
    title="⏱️ 持续时间分布",
    color_discrete_map={'上升趋势': '#2ca02c', '下降趋势': '#d62728'}
)
```

**功能**:
- 显示趋势持续时间分布
- 分析趋势稳定性

#### 5. 风险收益散点图
```python
fig_scatter = px.scatter(
    df,
    x='max_rally',
    y='max_decline',
    color='trend_type',
    size='duration_hours',
    hover_data=['trend_id', 'price_change_pct', 'risk_ratio'],
    title="🎯 风险收益散点图"
)
```

**功能**:
- 风险vs收益关系分析
- 气泡大小表示持续时间
- 悬停显示详细信息

### 📋 交互式数据表格

#### 表格功能
```python
# 列选择器
display_columns = st.multiselect(
    "选择显示的列",
    options=df.columns.tolist(),
    default=['trend_id', 'trend_type', 'start_time', 'end_time', 'start_price', 'end_price', 'price_change_pct', 'max_rally', 'max_decline', 'risk_ratio', 'is_risk_greater', 'duration_hours']
)

# 数据表格
st.dataframe(
    display_df,
    use_container_width=True,
    height=400
)
```

**功能**:
- 自定义显示列
- 实时数据筛选
- 排序和搜索
- 数据下载

#### 数据下载
```python
# CSV下载按钮
csv = display_df.to_csv(index=False)
st.download_button(
    label="📥 下载筛选后的数据",
    data=csv,
    file_name=f"filtered_trends_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
    mime="text/csv"
)
```

### 📊 统计摘要

#### 价格统计
```python
st.metric("平均价格变化", f"{filtered_df['price_change_pct'].mean():.2f}%")
st.metric("最大价格上涨", f"{filtered_df['price_change_pct'].max():.2f}%")
st.metric("最大价格下跌", f"{filtered_df['price_change_pct'].min():.2f}%")
```

#### 时间统计
```python
st.metric("平均持续时间", f"{filtered_df['duration_hours'].mean():.1f}小时")
st.metric("最长持续时间", f"{filtered_df['duration_hours'].max()}小时")
st.metric("最短持续时间", f"{filtered_df['duration_hours'].min()}小时")
```

#### 风险统计
```python
st.metric("平均风险收益比", f"{filtered_df['risk_ratio'].mean():.2f}")
st.metric("最大风险收益比", f"{filtered_df['risk_ratio'].max():.2f}")
st.metric("高风险趋势占比", f"{len(filtered_df[filtered_df['is_risk_greater']])/len(filtered_df)*100:.1f}%")
```

## 🔧 自定义配置

### 修改数据源
```python
# 在 financial_dashboard_fixed.py 中修改
data_file = 'assets/reports/trends_4h_chronological.csv'  # 修改为您的数据文件
```

### 添加新筛选器
```python
# 添加新的筛选器
new_filter = st.sidebar.selectbox(
    "新筛选器",
    options=['选项1', '选项2', '选项3'],
    index=0
)

# 应用筛选
if new_filter != '全部':
    filtered_df = filtered_df[filtered_df['column'] == new_filter]
```

### 添加新图表
```python
# 添加新的图表
fig_new = px.bar(
    df,
    x='category',
    y='value',
    title="新图表"
)
st.plotly_chart(fig_new, use_container_width=True)
```

### 修改页面配置
```python
# 页面配置
st.set_page_config(
    page_title="自定义标题",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)
```

## 🐛 故障排除

### 常见问题

#### 1. 数据文件找不到
```bash
# 错误: FileNotFoundError
# 解决: 检查数据文件路径
```

**解决方案**:
```python
# 检查文件是否存在
import os
if not os.path.exists('assets/reports/trends_4h_chronological.csv'):
    print("数据文件不存在，请先运行分析")
```

#### 2. 图表不显示
```bash
# 错误: 图表空白或错误
# 解决: 检查数据格式和依赖
```

**解决方案**:
```bash
# 重新安装依赖
pip install plotly streamlit

# 检查数据格式
print(df.dtypes)
print(df.head())
```

#### 3. 筛选器不工作
```bash
# 错误: 筛选后数据为空
# 解决: 检查筛选逻辑
```

**解决方案**:
```python
# 调试筛选逻辑
print(f"原始数据: {len(df)}")
print(f"筛选后数据: {len(filtered_df)}")
print(f"筛选条件: {filters}")
```

### 性能优化

#### 1. 数据缓存
```python
@st.cache_data
def load_trend_data():
    """缓存数据加载"""
    return pd.read_csv('assets/reports/trends_4h_chronological.csv')
```

#### 2. 分页显示
```python
# 分页显示大数据
page_size = 100
total_pages = len(df) // page_size
page = st.selectbox("选择页面", range(total_pages))
start_idx = page * page_size
end_idx = start_idx + page_size
display_df = df.iloc[start_idx:end_idx]
```

#### 3. 异步加载
```python
# 异步加载图表
with st.spinner("加载图表中..."):
    fig = create_chart(data)
    st.plotly_chart(fig)
```

## 📱 移动端适配

### 响应式设计
```python
# 检测设备类型
def is_mobile():
    return st.session_state.get('is_mobile', False)

# 根据设备调整布局
if is_mobile():
    st.columns(1)  # 单列布局
else:
    st.columns(2)  # 双列布局
```

### 触摸优化
```python
# 增大按钮尺寸
st.button("大按钮", key="large_button", help="移动端友好")

# 简化界面
if st.checkbox("简化模式"):
    # 显示简化版界面
    pass
```

## 🔒 安全配置

### 访问控制
```python
# 添加密码保护
password = st.sidebar.text_input("密码", type="password")
if password != "your_password":
    st.error("密码错误")
    st.stop()
```

### 数据保护
```python
# 敏感数据脱敏
def mask_sensitive_data(df):
    """脱敏处理"""
    if 'sensitive_column' in df.columns:
        df['sensitive_column'] = df['sensitive_column'].apply(lambda x: '***' if pd.notna(x) else x)
    return df
```

---

*最后更新: 2025-09-27*
*版本: v1.0.0*
