#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <stdexcept>
#include "../include/stats.h"

namespace py = pybind11;

py::object analyze_tensor(py::array_t<float> input) {
    py::buffer_info buf = input.request();
    if (buf.ndim != 1) throw std::runtime_error("Input must be 1-dimensional. Use tensor.flatten().");
    if (buf.size == 0) throw std::runtime_error("Input is empty.");
    
    float *ptr = static_cast<float*>(buf.ptr);
    DebugReport report = compute_statistics(ptr, buf.size);

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
    return check_for_failures(static_cast<float*>(buf.ptr), buf.size);
}

PYBIND11_MODULE(mlguardian, m) {
    m.doc() = "High-Performance ML Debugging Engine";
    m.def("analyze", &analyze_tensor, "Returns dict of stats");
    m.def("has_failure", &has_failure, "Returns True if NaN/Inf found");
}