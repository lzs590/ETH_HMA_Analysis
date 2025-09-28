"""
Analysis Module

This module contains all analysis components for processing
and analyzing cryptocurrency data using technical indicators.
"""

# 文件已移动到 src/eth_hma_analysis/core/
# 保持向后兼容性
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'eth_hma_analysis', 'core'))

from math_brain import MathBrain
from trend_analyzer import TrendAnalyzer, TrendInterval, EventAnalysis
from .trend_visualizer import TrendVisualizer

__all__ = [
    "MathBrain",
    "TrendAnalyzer",
    "TrendInterval", 
    "EventAnalysis",
    "TrendVisualizer",
]
