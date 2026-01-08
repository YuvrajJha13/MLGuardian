#!/bin/bash

case "$1" in
    build)
        echo "Building C++ Extension..."
        python setup.py build_ext --inplace
        ;;
    test)
        echo "Running Test Suite..."
        pytest tests/ -v
        ;;
    clean)
        echo "Cleaning build artifacts..."
        rm -rf build/ dist/ *.egg-info __pycache__ tests/__pycache__
        find . -name "*.so" -delete
        find . -name "*.pyc" -delete
        ;;
    example)
        echo "Running Example..."
        python examples/demo.py
        ;;
    *)
        echo "Usage: ./build.sh {build|test|clean|example}"
        ;;
esac
