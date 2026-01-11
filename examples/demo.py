import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
import matplotlib.pyplot as plt
import time
import mlguardian

NUM_EPOCHS = 100
TENSOR_SIZE = 1_000_000

plt.style.use('ggplot')

print("--- ML Guardian Visualization (Matplotlib Only) ---")
print(f"Dataset Size: {TENSOR_SIZE:,} elements")
print("-" * 40)

epochs = []
mean_gradients = []
max_gradients = []
failure_flags = []

start_time = time.time()
current_gradients = np.random.randn(TENSOR_SIZE).astype(np.float32) * 0.01

for epoch in range(NUM_EPOCHS):
    if epoch == 30:
        print(f"Epoch {epoch}: Injecting VANISHING GRADIENTS...")
        current_gradients = np.random.randn(TENSOR_SIZE).astype(np.float32) * 1e-6
    elif epoch == 60:
        print(f"Epoch {epoch}: Injecting EXPLODING GRADIENTS...")
        current_gradients = np.random.randn(TENSOR_SIZE).astype(np.float32) * 1e6
    elif epoch == 90:
        print(f"Epoch {epoch}: Injecting NaN CORRUPTION...")
        current_gradients = np.random.randn(TENSOR_SIZE).astype(np.float32)
        current_gradients[0:100] = np.nan
    else:
        current_gradients *= 0.99

    report = mlguardian.analyze(current_gradients)
    epochs.append(epoch)
    
    is_failure = (report["nan_count"] > 0) or (report["inf_count"] > 0)
    if is_failure:
        failure_flags.append(1)
        print(f"   >>> FAIL at Epoch {epoch}: {report['nan_count']} NaNs")
        mean_gradients.append(0.0) 
        max_gradients.append(0.0)
    else:
        failure_flags.append(0)
        mean_gradients.append(report["mean"])
        max_gradients.append(report["max_val"])

# --- Visualization ---
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# Plot 1: Statistics
ax1.plot(epochs, mean_gradients, label="Mean Gradient", color="blue", linewidth=2)
ax1.plot(epochs, max_gradients, label="Max Gradient", color="orange", linewidth=2, alpha=0.7)
ax1.set_title(f"Training Gradient Statistics ({TENSOR_SIZE:,} Parameters)", fontsize=14)
ax1.set_ylabel("Magnitude")
ax1.set_yscale("symlog") 
ax1.legend()
ax1.grid(True)

# Plot 2: Failures
ax2.plot(epochs, np.zeros(NUM_EPOCHS), color="gray", linewidth=1)
failed_epochs = [e for e, flag in zip(epochs, failure_flags) if flag == 1]

if failed_epochs:
    ax2.scatter(failed_epochs, [0]*len(failed_epochs), color="red", s=100, zorder=10, label="Failure Detected")
    for e in failed_epochs:
        ax2.text(e, 0.05, "FAIL", ha='center', color='red', fontweight='bold')

ax2.set_title("System Health Log", fontsize=14)
ax2.set_xlabel("Epoch")
ax2.set_yticks([])
ax2.set_ylim(-0.1, 0.2)
ax2.legend()

plt.tight_layout()
print("\nOpening plot window...")
plt.show()
