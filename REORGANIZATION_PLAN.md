# ETH HMA Analysis - 项目重构计划

## 🎯 重构目标
按照Google项目规范，重新组织项目结构，提高代码可维护性和可读性。

## 📁 新的项目结构

```
ETH_HMA_Analysis/
├── README.md                          # 项目主文档
├── requirements.txt                   # 生产环境依赖
├── requirements-dev.txt               # 开发环境依赖
├── pyproject.toml                     # 项目配置
├── setup.py                          # 安装脚本
├── Makefile                          # 构建脚本
│
├── src/                              # 源代码目录
│   ├── __init__.py
│   ├── eth_hma_analysis/             # 主包名
│   │   ├── __init__.py
│   │   ├── core/                     # 核心模块
│   │   │   ├── __init__.py
│   │   │   ├── data_collector.py     # 数据收集
│   │   │   ├── trend_analyzer.py     # 趋势分析
│   │   │   └── math_brain.py         # 数学计算
│   │   ├── visualizers/              # 可视化模块
│   │   │   ├── __init__.py
│   │   │   ├── base.py               # 基础可视化器
│   │   │   ├── trend_visualizer.py   # 趋势可视化
│   │   │   ├── strategy_visualizer.py # 策略可视化
│   │   │   └── jupyter_visualizer.py # Jupyter可视化
│   │   ├── utils/                    # 工具模块
│   │   │   ├── __init__.py
│   │   │   ├── config.py             # 配置管理
│   │   │   ├── font_fixer.py         # 字体修复
│   │   │   └── data_viewer.py        # 数据查看器
│   │   └── managers/                 # 管理器模块
│   │       ├── __init__.py
│   │       ├── project_manager.py    # 项目管理器
│   │       └── librarian.py          # 数据管理
│   │
├── scripts/                          # 脚本目录
│   ├── collect_data.py               # 数据收集脚本
│   ├── run_analysis.py               # 分析脚本
│   └── start_jupyter.py              # Jupyter启动脚本
│
├── notebooks/                        # Jupyter Notebooks
│   ├── 01_data_loading.ipynb        # 数据加载
│   ├── 02_trend_analysis.ipynb      # 趋势分析
│   └── 03_strategy_analysis.ipynb    # 策略分析
│
├── tests/                           # 测试目录
│   ├── __init__.py
│   ├── test_data_collector.py       # 数据收集测试
│   ├── test_trend_analyzer.py       # 趋势分析测试
│   ├── test_visualizers.py          # 可视化测试
│   └── fixtures/                     # 测试数据
│       └── sample_data.parquet
│
├── assets/                          # 资源目录
│   ├── data/                        # 数据文件
│   ├── charts/                      # 图表文件
│   ├── reports/                     # 报告文件
│   └── logs/                        # 日志文件
│
├── docs/                           # 文档目录
│   ├── README.md                    # 项目说明
│   ├── API.md                      # API文档
│   ├── CONTRIBUTING.md             # 贡献指南
│   └── CHANGELOG.md                # 更新日志
│
└── .github/                        # GitHub配置
    └── workflows/                   # CI/CD配置
        └── ci.yml
```

## 🧹 清理计划

### 1. 删除临时文件
- 所有 `*_test.py` 文件
- 所有 `test_*.py` 文件
- 所有 `*_test.png` 文件
- 所有 `font_*.py` 文件
- 所有 `simple_*.py` 文件
- 所有 `force_*.py` 文件

### 2. 重新组织源代码
- 将 `src/` 下的模块重新组织到 `src/eth_hma_analysis/`
- 统一命名规范
- 清理重复文件

### 3. 标准化文档
- 合并重复的README文件
- 统一文档格式
- 添加API文档

### 4. 测试规范化
- 创建 `tests/` 目录
- 移动所有测试文件
- 添加测试配置

## ✅ 执行步骤

1. **备份当前项目**
2. **创建新的目录结构**
3. **移动和重命名文件**
4. **更新导入路径**
5. **清理临时文件**
6. **更新文档**
7. **运行测试验证**
