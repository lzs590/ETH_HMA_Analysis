"""
ETH HMA Analysis Package

A comprehensive toolkit for Ethereum historical data analysis using 
Hull Moving Average (HMA) technical indicators.

This package provides:
- Automated data collection from Binance API
- HMA calculation and analysis
- Data storage and management
- Visualization and reporting tools
- Jupyter notebook integration

Author: ETH HMA Analysis Team
Version: 1.0.0
License: MIT
"""

__version__ = "1.0.0"
__author__ = "ETH HMA Analysis Team"
__email__ = ""
__license__ = "MIT"

# Package imports
from .collectors.data_collector import DataCollector
from .analyzers.math_brain import MathBrain
from .managers.librarian import Librarian
from .managers.project_manager import ProjectManager

__all__ = [
    "DataCollector",
    "MathBrain", 
    "Librarian",
    "ProjectManager",
    "__version__",
    "__author__",
    "__email__",
    "__license__",
]
