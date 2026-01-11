from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup
import sys

# Compiler Flags
if sys.platform == "win32":
    copt, lopt = ['/O2', '/std:c++17', '/openmp'], []
else:
    copt, lopt = ['-O3', '-std=c++17', '-fopenmp'], ['-fopenmp']

ext_modules = [
    Pybind11Extension(
        "mlguardian",  # The C++ Library
        sources=["src/module.cpp", "src/stats.cpp"],
        include_dirs=["include"],
        extra_compile_args=copt,
        extra_link_args=lopt,
    ),
]

setup(
    name="mlguardian",
    version="1.1.0",
    author="Yuvraj Jha",
    description="High-performance ML failure discovery with IDE debugging",
    ext_modules=ext_modules,
    py_modules=["debugger"],  # <--- Adds the Python Wrapper to the package
    setup_requires=["pybind11"],
    install_requires=["numpy", "rich"], # <--- Adds Rich UI dependency
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=["Programming Language :: Python :: 3"],
    zip_safe=False,
)