"""
ModelAutopsy: Enterprise ML Debugging Library.
"""
from .debugger import watch

# Engine Detection
ENGINE_STATUS = "Unknown"

try:
    import modelautopsy_rust
    ENGINE_STATUS = "Rust Safety Core 🦀"
except ImportError:
    try:
        import _core_cpp
        ENGINE_STATUS = "C++ Speed Core ⚡"
    except ImportError:
        ENGINE_STATUS = "Pure Python (Slow) 🐢"

# Expose Analyze
from .debugger import analyze as _internal_analyze

def analyze(tensor):
    """Public API."""
    return _internal_analyze(tensor)

__all__ = ["watch", "analyze", "ENGINE_STATUS"]
