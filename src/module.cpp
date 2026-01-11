#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <stdexcept>
#include "../include/stats.h"

namespace py = pybind11;

py::object analyze_tensor(py::array_t<float> input) {
    py::buffer_info buf = input.request();

    // Strict Validation
    if (buf.ndim != 1) {
        throw std::runtime_error("MLGuardian Error: Input must be 1-dimensional. Use tensor.flatten().");
    }
    if (buf.ptr == nullptr) {
        throw std::runtime_error("MLGuardian Error: Input buffer is null.");
    }

    // Safe pointer access
    float *ptr = static_cast<float*>(buf.ptr);
    size_t size = static_cast<size_t>(buf.size);

    // Engine Call
    DebugReport report = compute_statistics(ptr, size);

    // Convert to Dict
    py::dict result;
    result["nan_count"] = report.nan_count;
    result["inf_count"] = report.inf_count;
    result["valid_count"] = report.valid_count;
    result["mean"] = report.mean;
    result["min_val"] = report.min_val;
    result["max_val"] = report.max_val;
    return result;
}

bool has_failure(py::array_t<float> input) {
    py::buffer_info buf = input.request();
    if (buf.ptr == nullptr) return false; // Graceful handling of nulls
    return check_for_failures(static_cast<float*>(buf.ptr), buf.size);
}

PYBIND11_MODULE(mlguardian, m) {
    m.doc() = "MLGuardian v1.2.0: Reinforced Debugging Engine";
    
    m.def("analyze", &analyze_tensor, 
          "Performs full statistical analysis. Expects float32 1D array.");
          
    m.def("has_failure", &has_failure, 
          "Fast check for NaN or Inf.");
}