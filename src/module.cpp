#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <stdexcept>
#include "../include/stats.h"

namespace py = pybind11;

// Wrapper for compute_statistics
py::object analyze_tensor(py::array_t<float> input) {
    py::buffer_info buf = input.request();

    if (buf.ndim != 1) {
        throw std::runtime_error("Number of dimensions must be 1. Please flatten your tensor (tensor.flatten()).");
    }

    if (buf.size == 0) {
        throw std::runtime_error("Input tensor is empty (size 0).");
    }

    float *ptr = static_cast<float*>(buf.ptr);
    size_t size = static_cast<size_t>(buf.size);

    DebugReport report = compute_statistics(ptr, size);

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
    float *ptr = static_cast<float*>(buf.ptr);
    size_t size = static_cast<size_t>(buf.size);
    return check_for_failures(ptr, size);
}

PYBIND11_MODULE(mlguardian, m) {
    m.doc() = "MLGuardian: Production-grade ML Failure Discovery Library";
    m.def("analyze", &analyze_tensor, "Performs full statistical analysis (NaN/Inf/Mean/Min/Max). Returns a dictionary.");
    m.def("has_failure", &has_failure, "Fast check if tensor contains NaN or Inf. Returns True/False.");
}
