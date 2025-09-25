# ETH HMA Analysis - Project Structure

## 📁 Google-Style Project Organization

This project follows Google's recommended project structure for Python applications, providing clear separation of concerns and maintainable code organization.

```
ETH_HMA_Analysis/
├── 📁 src/                          # Source code package
│   ├── 📁 collectors/               # Data collection modules
│   │   ├── __init__.py
│   │   └── data_collector.py        # Binance API data collection
│   ├── 📁 analyzers/                # Analysis and computation modules
│   │   ├── __init__.py
│   │   ├── math_brain.py            # HMA calculation engine
│   │   ├── analyze_data.py          # Data analysis functions
│   │   ├── hma_analysis_report.py   # HMA-specific analysis
│   │   ├── visualize_hma.py         # Visualization tools
│   │   └── quick_visualization.py   # Quick analysis charts
│   ├── 📁 managers/                 # Management and coordination modules
│   │   ├── __init__.py
│   │   ├── librarian.py             # Data storage management
│   │   └── project_manager.py       # Main orchestration
│   └── 📁 utils/                    # Utility functions and configuration
│       ├── __init__.py
│       ├── config.py                # Configuration settings
│       └── data_viewer.py           # Data viewing utilities
├── 📁 scripts/                      # Executable scripts
│   ├── main.py                      # Main CLI entry point
│   └── start_jupyter.py             # Jupyter notebook launcher
├── 📁 notebooks/                    # Jupyter notebooks
│   └── ETH_HMA_Analysis.ipynb       # Main analysis notebook
├── 📁 tests/                        # Test files
│   ├── __init__.py
│   ├── test_collectors.py
│   ├── test_analyzers.py
│   └── test_managers.py
├── 📁 docs/                         # Documentation
│   ├── README.md                    # Main documentation
│   ├── README_Jupyter.md            # Jupyter usage guide
│   └── PROJECT_STRUCTURE.md         # This file
├── 📁 assets/                       # Static assets and data
│   ├── 📁 data/                     # Data files
│   │   ├── ETHUSDT_1h_raw_*.parquet
│   │   ├── ETHUSDT_1h_processed_*.parquet
│   │   ├── ETHUSDT_4h_raw_*.parquet
│   │   └── ETHUSDT_4h_processed_*.parquet
│   ├── 📁 charts/                   # Generated charts
│   │   ├── ETH_HMA_Comprehensive_Analysis.png
│   │   ├── hma_price_comparison.png
│   │   ├── hma_deviation_analysis.png
│   │   └── ...
│   └── 📁 logs/                     # Log files
│       └── eth_hma_analysis.log
├── 📁 .github/                      # GitHub workflows
│   └── 📁 workflows/
│       └── ci.yml                   # CI/CD pipeline
├── 📄 setup.py                      # Package setup configuration
├── 📄 pyproject.toml                # Modern Python project configuration
├── 📄 Makefile                      # Build and development commands
├── 📄 requirements.txt              # Production dependencies
├── 📄 requirements_jupyter.txt      # Jupyter-specific dependencies
├── 📄 .gitignore                    # Git ignore rules
└── 📄 README.md                     # Project overview
```

## 🏗️ Architecture Overview

### Core Components

1. **Collectors** (`src/collectors/`)
   - Data collection from external APIs
   - Handles rate limiting and error recovery
   - Converts raw data to standardized format

2. **Analyzers** (`src/analyzers/`)
   - Technical indicator calculations
   - Data analysis and statistics
   - Visualization generation
   - Report generation

3. **Managers** (`src/managers/`)
   - Data storage and retrieval
   - Project orchestration
   - Workflow coordination

4. **Utils** (`src/utils/`)
   - Configuration management
   - Common utilities
   - Helper functions

### Data Flow

```
External APIs → Collectors → Managers → Analyzers → Assets/Charts
                     ↓
                Utils/Config
```

## 🚀 Usage

### Development Setup

```bash
# Install in development mode
make install-dev

# Run tests
make test

# Format code
make format

# Run linting
make lint
```

### Analysis Commands

```bash
# Run full analysis
make run

# Generate visualizations
make visualize

# Start Jupyter
make jupyter

# Data management
make data-clean
make data-backup
```

### Direct Script Usage

```bash
# Main analysis
python scripts/main.py --years 1 --verbose

# Jupyter notebook
python scripts/start_jupyter.py

# Data analysis
python -m src.analyzers.analyze_data
```

## 📦 Package Structure

The project is organized as a Python package with the following key features:

- **Modular Design**: Clear separation between data collection, analysis, and management
- **Extensible**: Easy to add new collectors, analyzers, or managers
- **Testable**: Comprehensive test coverage for all components
- **Configurable**: Centralized configuration management
- **Documented**: Extensive documentation and type hints

## 🔧 Configuration

All configuration is centralized in `src/utils/config.py`:

- API endpoints and credentials
- Data storage paths
- Analysis parameters
- Logging configuration

## 📊 Data Management

- **Raw Data**: Stored in `assets/data/` as Parquet files
- **Charts**: Generated visualizations in `assets/charts/`
- **Logs**: Application logs in `assets/logs/`
- **Backup**: Automated backup functionality available

## 🧪 Testing

- Unit tests for all modules
- Integration tests for data flow
- Performance tests for large datasets
- CI/CD pipeline with automated testing

## 📈 Monitoring

- Comprehensive logging
- Performance metrics
- Error tracking
- Data quality monitoring

This structure provides a solid foundation for scalable cryptocurrency analysis applications while maintaining code quality and developer productivity.
