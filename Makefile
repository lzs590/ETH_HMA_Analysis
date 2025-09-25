# ETH HMA Analysis - Makefile
# Google-style project management

.PHONY: help install install-dev clean test lint format run analyze visualize jupyter

# Default target
help:
	@echo "ETH HMA Analysis - Available Commands:"
	@echo ""
	@echo "Setup:"
	@echo "  install      Install production dependencies"
	@echo "  install-dev  Install development dependencies"
	@echo "  clean        Clean build artifacts and cache"
	@echo ""
	@echo "Development:"
	@echo "  test         Run tests"
	@echo "  lint         Run linting checks"
	@echo "  format       Format code with black"
	@echo ""
	@echo "Analysis:"
	@echo "  run          Run main analysis pipeline"
	@echo "  analyze      Run data analysis"
	@echo "  visualize    Generate visualization charts"
	@echo "  jupyter      Start Jupyter notebook server"
	@echo ""
	@echo "Data Management:"
	@echo "  data-clean   Clean old data files"
	@echo "  data-backup  Backup data to archive"

# Installation
install:
	pip install -e .

install-dev:
	pip install -e ".[dev,jupyter]"

# Development
test:
	python -m pytest tests/ -v

lint:
	flake8 src/ scripts/ tests/
	mypy src/ scripts/

format:
	black src/ scripts/ tests/

# Analysis
run:
	python scripts/main.py

analyze:
	python -m src.analyzers.analyze_data

visualize:
	python -m src.analyzers.quick_visualization

jupyter:
	python scripts/start_jupyter.py

# Data management
data-clean:
	find assets/data -name "*.parquet" -mtime +30 -delete
	find assets/logs -name "*.log" -mtime +7 -delete

data-backup:
	tar -czf "backup_$(shell date +%Y%m%d_%H%M%S).tar.gz" assets/data/

# Cleanup
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/ dist/ .pytest_cache/ .mypy_cache/
