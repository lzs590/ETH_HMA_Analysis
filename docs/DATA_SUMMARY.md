# ETH HMA Analysis - Data Summary

## Latest Analysis Results (2025-09-26)

### 4H Data Analysis
- **Total Records**: 6,570
- **Analysis Period**: 3 years
- **Trend Intervals**: 403 (202 up, 201 down)
- **Turning Points**: 404 (202 up, 202 down)

#### Upward Trends
- **Average Duration**: 16.6 periods
- **Average Price Change**: 0.79%
- **Maximum Price Change**: 33.98%
- **Average PFE**: 5.06%
- **Maximum PFE**: 42.89%
- **Win Rate**: 38.1%

#### Downward Trends
- **Average Duration**: 15.5 periods
- **Average Price Change**: 0.09%
- **Maximum Price Change**: 10.36%
- **Average PFE**: 5.27%
- **Maximum PFE**: 54.72%
- **Win Rate**: 31.3%

#### Event Analysis
- **Up Turn Volatility**: 0.867
- **Down Turn Volatility**: 0.842
- **Up Turn Consistency**: 48.9%
- **Down Turn Consistency**: 46.8%
- **Profit/Loss Ratio**: 1.18

### 1H Data Analysis
- **Total Records**: 26,279
- **Analysis Period**: 3 years
- **Trend Intervals**: 1546 (772 up, 774 down)
- **Turning Points**: 1547 (772 up, 775 down)

#### Upward Trends
- **Average Duration**: 17.2 periods
- **Average Price Change**: 0.26%
- **Maximum Price Change**: 22.97%
- **Average PFE**: 2.42%
- **Maximum PFE**: 31.02%
- **Win Rate**: 35.0%

#### Downward Trends
- **Average Duration**: 16.7 periods
- **Average Price Change**: -0.04%
- **Maximum Price Change**: 6.25%
- **Average PFE**: 2.54%
- **Maximum PFE**: 55.34%
- **Win Rate**: 33.9%

#### Event Analysis
- **Up Turn Volatility**: 0.414
- **Down Turn Volatility**: 0.424
- **Up Turn Consistency**: 50.8%
- **Down Turn Consistency**: 46.1%
- **Profit/Loss Ratio**: 1.16

## Key Metrics Definitions

- **PFE (Potential Favorable Excursion)**: Maximum profit possible in a trend
- **MAE (Maximum Adverse Excursion)**: Maximum loss possible in a trend
- **Win Rate**: Percentage of profitable trend intervals
- **Consistency**: Signal prediction accuracy
- **Volatility**: Price volatility around events

## Technical Parameters

- **HMA Period**: 45
- **Slope Threshold**: 0.001
- **Event Window**: 5 periods before/after
- **Data Source**: Binance API
- **Storage Format**: Parquet

## File Locations

- **Raw Data**: `assets/data/ETHUSDT_*_raw_*.parquet`
- **Processed Data**: `assets/data/ETHUSDT_*_processed_*.parquet`
- **Analysis Reports**: `assets/reports/trend_analysis_*.json`
- **Charts**: `assets/charts/*.png`
- **Logs**: `assets/logs/eth_hma_analysis.log`
