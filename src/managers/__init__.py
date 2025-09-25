"""
Management Module

This module contains all management components for coordinating
data collection, analysis, and storage operations.
"""

from .librarian import Librarian
from .project_manager import ProjectManager

__all__ = ["Librarian", "ProjectManager"]
