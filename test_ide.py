import numpy as np
from debugger import watch

@watch(drop_into_debugger=True, verbose=True)
def model_layer(data):
    # Simulate a corrupt layer
    if np.random.rand() > 0.5:
        data[0] = np.nan
    return data * 0.99

print("--- Starting Simulation ---")
tensor = np.random.randn(1000).astype(np.float32)
result = model_layer(tensor)
