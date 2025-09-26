# AI Assistant Quick Reference Guide

## Project Overview
This is an ETH HMA Trend Analysis project that implements quantitative analysis using Hull Moving Average (HMA) technical indicators. The project analyzes ETH price data to identify turning points, trend intervals, and price behavior patterns.

## Quick Start for New AI Assistant

### 1. Understand the Project Structure
```
ETH_HMA_Analysis/
├── src/                    # Source code
│   ├── collectors/         # Data collection from Binance
│   ├── analyzers/         # Analysis modules (trend_analyzer.py, trend_visualizer.py)
│   ├── managers/          # Data management
│   └── utils/             # Configuration
├── scripts/               # Command-line tools
│   ├── main.py           # Data collection
│   └── trend_analysis.py # Main analysis script
├── assets/                # Data and outputs
│   ├── data/             # Parquet files
│   ├── charts/           # PNG visualizations
│   └── reports/          # JSON results
└── docs/                  # Documentation
```

### 2. Key Files to Understand
- **`src/analyzers/trend_analyzer.py`**: Core analysis logic
- **`src/analyzers/trend_visualizer.py`**: Visualization tools
- **`scripts/trend_analysis.py`**: Main analysis script
- **`src/utils/config.py`**: Configuration parameters

### 3. Main Commands
```bash
# Run comprehensive analysis
python scripts/trend_analysis.py

# English interface
python scripts/trend_analysis.py --english

# Skip visualization
python scripts/trend_analysis.py --no-viz

# Collect data
python scripts/main.py
```

### 4. Core Algorithm
1. **HMA Calculation**: Hull Moving Average with 45-period default
2. **Slope Analysis**: `df['HMA_slope'] = df['HMA_45'].diff()`
3. **Turning Points**: Sign changes in slope
4. **Event Analysis**: Price behavior around turning points
5. **Trend Intervals**: Quantify price changes between turning points

### 5. Key Metrics
- **PFE**: Potential Favorable Excursion (max profit)
- **MAE**: Maximum Adverse Excursion (max loss)
- **Win Rate**: Percentage of profitable trends
- **Consistency**: Signal prediction accuracy

### 6. Recent Analysis Results
- **4H Data**: 403 trend intervals, 38.1% win rate for up trends
- **1H Data**: 1546 trend intervals, 35.0% win rate for up trends
- **Profit/Loss Ratio**: 1.18 (4H), 1.16 (1H)

### 7. Common Issues and Solutions
- **Chinese Font Display**: Use `--english` flag or check font configuration
- **Memory Issues**: Reduce data period in config
- **API Errors**: Check network connectivity

### 8. Development History
- Started as basic HMA calculator
- Added trend analysis and turning point detection
- Implemented event analysis and performance metrics
- Added bilingual support and professional visualizations
- Fixed font display issues for Chinese characters

### 9. Current Status
- **Production Ready**: All core features implemented
- **Bilingual Support**: Chinese and English interfaces
- **Professional Documentation**: Complete README and guides
- **GitHub Repository**: Fully uploaded and documented

### 10. Next Steps for Enhancement
- Add more technical indicators
- Implement real-time data feeds
- Add machine learning integration
- Create web interface
- Add more asset support

## Important Notes
- The project uses Parquet format for efficient data storage
- All analysis results are saved as JSON files
- Charts are generated as PNG files
- The system supports both 1H and 4H timeframes
- Font issues have been resolved with dynamic font selection
