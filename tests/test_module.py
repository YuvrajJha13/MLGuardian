import pytest
import numpy as np
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import mlguardian

def test_empty_tensor():
    with pytest.raises(RuntimeError):
        mlguardian.analyze(np.array([], dtype=np.float32))

def test_healthy_tensor():
    data = np.random.randn(1000).astype(np.float32)
    assert not mlguardian.has_failure(data)
    
    report = mlguardian.analyze(data)
    assert report["nan_count"] == 0
    assert report["inf_count"] == 0
    assert report["valid_count"] == 1000

def test_nan_detection():
    data = np.array([1.0, 2.0, np.nan, 4.0], dtype=np.float32)
    assert mlguardian.has_failure(data) == True
    
    report = mlguardian.analyze(data)
    assert report["nan_count"] == 1
    assert report["valid_count"] == 3

def test_inf_detection():
    data = np.array([1.0, np.inf, -np.inf], dtype=np.float32)
    assert mlguardian.has_failure(data) == True
    
    report = mlguardian.analyze(data)
    assert report["inf_count"] == 2
    # Mean should ignore inf
    assert report["mean"] == 1.0 

def test_mixed_failures():
    # Large dataset test
    size = 1000000
    data = np.random.randn(size).astype(np.float32)
    data[0] = np.nan
    data[500] = np.inf
    data[-1] = np.nan
    
    assert mlguardian.has_failure(data) == True
    report = mlguardian.analyze(data)
    
    assert report["nan_count"] == 2
    assert report["inf_count"] == 1
    assert report["valid_count"] == size - 3

def test_wrong_dimensions():
    # 2D tensor should fail or require flattening
    data = np.random.randn(10, 10).astype(np.float32)
    with pytest.raises(RuntimeError):
        mlguardian.analyze(data)

if __name__ == "__main__":
    pytest.main([__file__, "-v"])