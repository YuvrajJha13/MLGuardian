# MLGuardian

MLGuardian is a high-performance Machine Learning debugging library written in C++ and wrapped in Python. It utilizes OpenMP to perform multi-threaded analysis of gradient tensors, instantly detecting NaN, Infinity, Vanishing, and Exploding values in massive datasets.

## Features

*   **Lightning Fast:** Analyzes 1M parameters in milliseconds using C++ OpenMP.
*   **Reliable:** Detects NaN (Not a Number) and Infinity corruption instantly.
*   **Developer Friendly:** Returns standard Python Dictionaries for easy integration.
*   **Visual:** Includes visualization tools to track training health over time.

## Installation Prerequisites

*   C++ Compiler (GCC/Clang) with OpenMP support.
*   Python 3.8+
*   NumPy

## Build from Source

```bash
git clone https://github.com/YuvrajJha13/MLGuardian.git
cd MLGuardian

# Install dependencies
pip install -r requirements.txt

# Build the C++ extension
python setup.py build_ext --inplace
