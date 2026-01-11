from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup
import sys

# Optimization Flags for Production Release
if sys.platform == "win32":
    copt, lopt = ['/O2', '/std:c++17', '/openmp'], []
else:
    # -O3: Maximum Optimization
    # -march=native: Optimize for your specific CPU (SIMD)
    copt, lopt = ['-O3', '-march=native', '-std=c++17', '-fopenmp'], ['-fopenmp']

ext_modules = [
    Pybind11Extension(
        "mlguardian",
        sources=["src/module.cpp", "src/stats.cpp"],
        include_dirs=["include"],
        extra_compile_args=copt,
        extra_link_args=lopt,
    ),
]

setup(
    name="mlguardian",
    version="1.2.0", # Reinforced Version
    author="Yuvraj Jha",
    description="Reinforced High-Performance ML Debugging Engine v1.2.0",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/YuvrajJha13/MLGuardian",
    ext_modules=ext_modules,
    py_modules=["debugger"],
    setup_requires=["pybind11"],
    install_requires=["numpy", "rich"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    zip_safe=False,
)