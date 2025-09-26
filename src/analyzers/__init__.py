"""
Analysis Module

This module contains all analysis components for processing
and analyzing cryptocurrency data using technical indicators.
"""

from .math_brain import MathBrain
from .trend_analyzer import TrendAnalyzer, TrendInterval, EventAnalysis
from .trend_visualizer import TrendVisualizer

__all__ = [
    "MathBrain",
    "TrendAnalyzer",
    "TrendInterval", 
    "EventAnalysis",
    "TrendVisualizer",
]
