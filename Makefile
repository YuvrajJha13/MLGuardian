.PHONY: all clean build test install example

PYTHON := python
PYTEST := pytest

all: build

build:
    @echo "Building C++ Extension..."
    $(PYTHON) setup.py build_ext --inplace

test: build
    @echo "Running Test Suite..."
    $(PYTEST) tests/ -v

clean:
    @echo "Cleaning build artifacts..."
    rm -rf build/ dist/ *.egg-info
    rm -rf __pycache__ tests/__pycache__
    find . -name "*.so" -delete
    find . -name "*.pyc" -delete

example: build
    $(PYTHON) examples/demo.py