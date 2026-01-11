"""
IDE-Style Python Debugger.
Imports the C++ 'mlguardian' core for speed.
"""
import functools
import inspect
import numpy as np
from rich.console import Console
from rich.table import Table
from rich import print as rprint

# Import the compiled C++ library
try:
    import mlguardian
    C_CORE_AVAILABLE = True
except ImportError:
    rprint("[yellow]Warning: C++ core not found. Using numpy fallback.[/yellow]")
    C_CORE_AVAILABLE = False

console = Console()

def _scan_tensor(tensor):
    """Bridge between Python object and C++ Logic."""
    if not isinstance(tensor, np.ndarray): return None
    
    # 1. Use C++ Engine if available
    if C_CORE_AVAILABLE:
        # mlguardian.analyze expects float32 1D array
        if tensor.dtype != np.float32:
            tensor = tensor.astype(np.float32)
        if tensor.ndim != 1:
            tensor = tensor.flatten()
        return mlguardian.analyze(tensor)
    
    # 2. Fallback (Python)
    return {
        "nan_count": np.isnan(tensor).sum(),
        "inf_count": np.isinf(tensor).sum(),
        "valid_count": tensor.size - np.isnan(tensor).sum() - np.isinf(tensor).sum(),
        "mean": float(np.mean(tensor)) if tensor.size > 0 else 0
    }

def watch(drop_into_debugger=False, verbose=True):
    """
    Decorator: Automatically monitors function inputs/outputs.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if verbose:
                console.print(f"[dim]🔍 Running [cyan]{func.__name__}[/cyan]...[/dim]")

            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            
            failure_detected = False
            
            # Scan Inputs
            for name, val in bound_args.arguments.items():
                if isinstance(val, np.ndarray):
                    rep = _scan_tensor(val)
                    if rep and (rep['nan_count'] > 0 or rep['inf_count'] > 0):
                        _print_failure(func.__name__, name, rep)
                        failure_detected = True

            # Execute
            result = func(*args, **kwargs)

            # Scan Output
            if isinstance(result, np.ndarray):
                rep = _scan_tensor(result)
                if rep and (rep['nan_count'] > 0 or rep['inf_count'] > 0):
                    _print_failure(func.__name__, "Return Value", rep)
                    failure_detected = True
            
            if verbose and not failure_detected:
                console.print(f"[green]✔[/green] [dim]{func.__name__} OK.[/dim]")

            # Debugger Breakpoint
            if failure_detected and drop_into_debugger:
                console.print("[bold red]🛑 Pausing for inspection...[/bold red]")
                import pdb; pdb.set_trace()

            return result
        return wrapper
    return decorator

def _print_failure(func_name, arg_name, report):
    """Pretty print failure details."""
    console.print(f"\n[bold red]⚠️  FAILURE in {func_name}[/bold red]")
    t = Table(show_header=True)
    t.add_column("Metric", style="cyan")
    t.add_column("Value", style="bold red")
    t.add_row("Target", arg_name)
    t.add_row("NaN Count", str(report['nan_count']))
    t.add_row("Inf Count", str(report['inf_count']))
    console.print(t)