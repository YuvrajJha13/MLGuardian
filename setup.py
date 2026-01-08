from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup
import sys

# Define Compiler and Linker Flags based on Operating System
if sys.platform == "win32":
    # Windows (MSVC) Flags
    extra_compile_args = [
        '/O2',           # Maximum Optimization
        '/std:c++17',    # C++17 Standard
        '/openmp'        # Enable OpenMP for Windows
    ]
    extra_link_args = []
else:
    # Linux / macOS (GCC/Clang) Flags
    extra_compile_args = [
        '-O3',           # Aggressive Optimization
        '-march=native', # Optimize for current CPU architecture
        '-std=c++17',    # C++17 Standard
        '-fopenmp',      # Enable OpenMP
        '-Wall',         # Enable all warnings
        '-shared',       # Build shared library
        '-fPIC'          # Position Independent Code
    ]
    extra_link_args = [
        '-fopenmp'       # Link OpenMP library
    ]

# Define the Extension Module
ext_modules = [
    Pybind11Extension(
        "mlguardian",               # The name you import in Python
        sources=[                   # List of C++ files to compile
            "src/module.cpp",       # Python Bindings
            "src/stats.cpp"         # Core Logic
        ],
        include_dirs=[              # Directories to search for header files
            "include"
        ],
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args,
    ),
]

setup(
    name="mlguardian",
    version="0.2.0",
    author="Yuvraj Jha",
    author_email="jhayuvraj08@outlook.com",
    description="A high-performance, multi-threaded ML failure discovery and debugging library.",
    long_description="",
    ext_modules=ext_modules,
    install_requires=[
        "numpy",
        "pytest"
    ],
    extras_require={
        "dev": ["pytest", "matplotlib", "seaborn"],
    },
    zip_safe=False,
    python_requires=">=3.8",
)