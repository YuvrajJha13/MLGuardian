import numpy as np
import modelautopsy

print(f"Engine Status: {modelautopsy.ENGINE_STATUS}")

# Test Analyze
data = np.array([1.0, 2.0, np.nan], dtype=np.float32)
report = modelautopsy.analyze(data)

print(f"Report: {report}")

# Test Decorator
@modelautopsy.watch()
def step(x):
    return x * 2

print(step(np.array([1.0, 2.0])))
