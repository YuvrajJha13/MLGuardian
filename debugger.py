"""
Reinforced IDE Debugger.
Features: Smart Casting (Zero-Copy fallback), List handling, Rich UI.
"""
import functools
import inspect
import numpy as np
from rich.console import Console
from rich.table import Table
from rich import print as rprint

# Import C++ Core
try:
    import mlguardian
    C_CORE_AVAILABLE = True
except ImportError:
    rprint("[yellow]Warning: C++ Core not found. Using Python Fallback.[/yellow]")
    C_CORE_AVAILABLE = False

console = Console()

def _prepare_tensor(tensor):
    """
    Smartly prepares a tensor for C++ analysis.
    - Converts Lists/Arrays to numpy.
    - Converts float64/int -> float32 if needed (with warning).
    - Enforces 1D shape for the C++ engine.
    - Returns None if not a tensor-like object.
    """
    # 1. Handle Lists or Tuples
    if not isinstance(tensor, np.ndarray):
        try:
            # Try to convert list to numpy
            tensor = np.array(tensor)
        except:
            return None

    # 2. Ensure Float32 (C++ Signature)
    # If it's not float32, we MUST convert it. This causes a copy, but is safe.
    # We warn the user for performance awareness.
    if tensor.dtype != np.float32:
        console.print(f"[dim]Casting {tensor.dtype} to float32 (Copy overhead)[/dim]")
        tensor = tensor.astype(np.float32)

    # 3. Ensure 1D (C++ expects contiguous 1D array)
    if tensor.ndim != 1:
        tensor = tensor.flatten()

    return tensor

def _scan_tensor(tensor):
    """Performs the C++ scan safely."""
    # Prepare tensor (Handle types/shapes)
    tensor = _prepare_tensor(tensor)
    if tensor is None: return None

    if C_CORE_AVAILABLE:
        # Call C++ Engine (Fastest path)
        return mlguardian.analyze(tensor)
    else:
        # Python Fallback (For dev environments without C++)
        return {
            "nan_count": np.isnan(tensor).sum(),
            "inf_count": np.isinf(tensor).sum(),
            "valid_count": tensor.size - np.isnan(tensor).sum() - np.isinf(tensor).sum(),
            "mean": float(np.mean(tensor)) if tensor.size > 0 else 0
        }

def watch(drop_into_debugger=False, verbose=True, inspect_args=True, inspect_return=True):
    """
    Enhanced Decorator:
    - inspect_args: Check inputs.
    - inspect_return: Check outputs.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if verbose:
                console.print(f"[dim]🔍 [cyan]{func.__name__}[/cyan] execution started...[/dim]")

            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            
            failure_detected = False
            
            # 1. Scan Inputs
            if inspect_args:
                for name, val in bound_args.arguments.items():
                    rep = _scan_tensor(val)
                    if rep and (rep['nan_count'] > 0 or rep['inf_count'] > 0):
                        _log_error(func.__name__, f"Input '{name}'", rep)
                        failure_detected = True

            # 2. Execute
            result = func(*args, **kwargs)

            # 3. Scan Output
            if inspect_return:
                rep = _scan_tensor(result)
                if rep and (rep['nan_count'] > 0 or rep['inf_count'] > 0):
                    _log_error(func.__name__, "Return Value", rep)
                    failure_detected = True
            
            if verbose and not failure_detected:
                console.print(f"[green]✔[/green] [dim]{func.__name__} finished clean.[/dim]")

            # 4. Breakpoint
            if failure_detected and drop_into_debugger:
                console.print("[bold red]🛑 Halting execution at checkpoint...[/bold red]")
                import pdb; pdb.set_trace()

            return result
        return wrapper
    return decorator

def _log_error(func, source, report):
    console.print(f"\n[bold red]⚠️  FAILURE DETECTED[/bold red]")
    t = Table(show_header=False, header_style="bold magenta")
    t.add_row("[dim]Function:[/dim]", f"[bold]{func}[/bold]")
    t.add_row("[dim]Source:[/dim]", f"[bold]{source}[/bold]")
    t.add_row("[dim]NaN Count:[/dim]", f"[red]{report['nan_count']}[/red]")
    t.add_row("[dim]Inf Count:[/dim]", f"[red]{report['inf_count']}[/red]")
    if report['nan_count'] == 0:
        t.add_row("[dim]Mean:[/dim]", f"{report['mean']:.4e}")
        t.add_row("[dim]L2 Norm:[/dim]", f"{report['l2_norm']:.4e}") # NEW
        t.add_row("[dim]Variance:[/dim]", f"{report['variance']:.4e}") # NEW
    console.print(t)