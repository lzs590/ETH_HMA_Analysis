# ETH HMA Trend Analysis

A comprehensive quantitative analysis tool for Ethereum (ETH) price data using Hull Moving Average (HMA) technical indicators and advanced trend analysis algorithms.

## 🎯 Overview

This project provides automated data collection, technical analysis, and trend identification for ETH/USDT trading pairs. It implements sophisticated algorithms to identify turning points, analyze price behavior, and quantify trend performance metrics.

## ✨ Key Features

- **Automated Data Collection**: Fetches historical ETH price data from Binance API
- **HMA Technical Analysis**: Calculates Hull Moving Average with customizable periods
- **Trend Analysis**: Identifies turning points and analyzes trend intervals
- **Event Analysis**: Studies price behavior around slope changes
- **Performance Metrics**: Quantifies maximum favorable/adverse excursions (PFE/MAE)
- **Multi-timeframe Support**: 1-hour and 4-hour intervals
- **Bilingual Interface**: Chinese and English language support
- **Comprehensive Visualizations**: Professional charts and reports

## 🏗️ Architecture

### Core Components

- **Data Collector**: Fetches raw price data from Binance API
- **Math Brain**: Calculates HMA and technical indicators
- **Trend Analyzer**: Identifies turning points and trend intervals
- **Event Analyzer**: Analyzes price behavior around signals
- **Visualizer**: Generates professional charts and reports
- **Librarian**: Manages data storage and retrieval

### Project Structure

```
ETH_HMA_Analysis/
├── src/
│   ├── collectors/     # Data collection modules
│   ├── analyzers/      # Analysis and visualization
│   ├── managers/       # Data management
│   └── utils/          # Configuration and utilities
├── scripts/            # Command-line tools
├── notebooks/          # Jupyter notebooks
├── assets/             # Data and charts
└── docs/              # Documentation
```

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/lzs590/ETH_HMA_Analysis.git
cd ETH_HMA_Analysis

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```bash
# Run comprehensive trend analysis
python scripts/trend_analysis.py

# English interface
python scripts/trend_analysis.py --english

# Skip visualization (analysis only)
python scripts/trend_analysis.py --no-viz

# Verbose output
python scripts/trend_analysis.py --verbose
```

### Data Collection

```bash
# Collect and process data
python scripts/main.py

# Specific intervals
python scripts/main.py --interval 1h
python scripts/main.py --interval 4h

# Custom HMA period
python scripts/main.py --hma-period 30
```

## 📊 Analysis Features

### Trend Analysis

- **Turning Point Detection**: Identifies HMA slope changes
- **Trend Intervals**: Quantifies price movements between turning points
- **Performance Metrics**: Calculates PFE, MAE, and win rates
- **Event Analysis**: Studies price behavior around signals

### Key Metrics

- **Maximum Favorable Excursion (PFE)**: Best possible profit in a trend
- **Maximum Adverse Excursion (MAE)**: Worst possible loss in a trend
- **Win Rate**: Percentage of profitable trend intervals
- **Consistency**: Signal prediction accuracy
- **Volatility**: Price volatility around events

### Visualizations

- Turning point identification charts
- Trend interval analysis
- Event analysis plots
- Comprehensive summary reports
- Performance distribution histograms

## 📈 Technical Indicators

### Hull Moving Average (HMA)

The Hull Moving Average is calculated using:
1. Two weighted moving averages of different periods
2. Raw HMA signal generation
3. Smoothing of the raw signal

**Advantages:**
- Reduced lag compared to traditional moving averages
- Better trend following capability
- Fewer false signals

### Additional Metrics

- Price change rates
- HMA deviation percentages
- Volatility measurements
- Trend direction indicators

## ⚙️ Configuration

Key parameters in `src/utils/config.py`:

```python
# Trading pair
SYMBOL = "ETHUSDT"

# Time intervals
INTERVALS = ["1h", "4h"]

# HMA period
HMA_PERIOD = 45

# Historical data years
YEARS_BACK = 3

# Data directory
DATA_DIR = "./assets/data"
```

## 📁 Data Format

### Raw Data Columns
- `open_time`: Opening timestamp (index)
- `open`, `high`, `low`, `close`: OHLC prices
- `volume`: Trading volume
- `close_time`: Closing timestamp
- `quote_asset_volume`: Quote asset volume
- `trades_count`: Number of trades

### Processed Data Additional Columns
- `HMA_45`: Hull Moving Average (45-period)
- `price_change`: Price change rate
- `hma_deviation`: HMA deviation percentage

## 🔧 Advanced Usage

### Custom Analysis

```python
from src.analyzers.trend_analyzer import TrendAnalyzer
from src.analyzers.trend_visualizer import TrendVisualizer

# Initialize analyzer
analyzer = TrendAnalyzer(hma_period=45, slope_threshold=0.001)

# Load data
df = pd.read_parquet('assets/data/ETHUSDT_1h_processed_*.parquet')

# Perform analysis
results = analyzer.generate_analysis_report(df, '1h')

# Generate visualizations
visualizer = TrendVisualizer(use_chinese=False)
visualizer.plot_comprehensive_analysis(df, intervals, events)
```

### Jupyter Notebooks

```bash
# Start Jupyter
python scripts/start_jupyter.py

# Or directly
jupyter notebook notebooks/ETH_HMA_Analysis.ipynb
```

## 📊 Output Files

### Data Files
- `assets/data/ETHUSDT_*_raw_*.parquet`: Raw price data
- `assets/data/ETHUSDT_*_processed_*.parquet`: Processed data with indicators

### Analysis Reports
- `assets/reports/trend_analysis_*.json`: Detailed analysis results
- `assets/charts/*.png`: Visualization charts

### Logs
- `assets/logs/eth_hma_analysis.log`: Execution logs

## 🛠️ Troubleshooting

### Common Issues

1. **Font Display Issues**
   ```bash
   # Use English interface
   python scripts/trend_analysis.py --english
   ```

2. **Memory Issues**
   - Reduce `YEARS_BACK` in config
   - Process data in smaller batches

3. **API Rate Limits**
   - The tool includes automatic retry mechanisms
   - Check network connectivity

4. **File Permissions**
   - Ensure write access to `assets/` directory

### Debug Mode

```bash
# Enable verbose logging
python scripts/trend_analysis.py --verbose
```

## 📄 License

MIT License - see LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📞 Support

- Check the logs in `assets/logs/`
- Review the documentation in `docs/`
- Open an issue on GitHub

## 🔬 Research Applications

This tool is designed for:
- Quantitative trading research
- Technical analysis studies
- Market microstructure analysis
- Algorithm development
- Academic research

---

**Disclaimer**: This tool is for educational and research purposes only. Not financial advice.
