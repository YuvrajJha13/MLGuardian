#include "stats.h"
#include <cmath>
#include <algorithm>
#include <limits>

#ifdef _OPENMP
#include <omp.h>
#endif

template <typename T>
DebugReport compute_statistics(const T* data, size_t size) {
    if (size == 0) {
        DebugReport report = {0, 0, 0, 0.0, 0.0, 0.0, 0.0};
        return report;
    }

    size_t nan_count = 0, inf_count = 0, valid_count = 0;
    double sum = 0.0;
    double sum_sq = 0.0;
    double min_v = std::numeric_limits<double>::infinity();
    double max_v = -std::numeric_limits<double>::infinity();

    // Removed #pragma omp simd due to compiler incompatibility.
    // #pragma omp parallel for is sufficient for Multi-threading.
    // -O3 -march=native handles SIMD automatically.
    #pragma omp parallel for reduction(+:nan_count, inf_count, valid_count, sum, sum_sq) reduction(min:min_v) reduction(max:max_v)
    for (size_t i = 0; i < size; ++i) {
        double val = static_cast<double>(data[i]);
        
        if (std::isnan(val)) {
            nan_count++;
        } else if (std::isinf(val)) {
            inf_count++;
        } else {
            if (val < min_v) min_v = val;
            if (val > max_v) max_v = val;
            sum += val;
            sum_sq += (val * val);
            valid_count++;
        }
    }

    DebugReport report;
    report.nan_count = nan_count;
    report.inf_count = inf_count;
    report.valid_count = valid_count;
    report.mean = (valid_count > 0) ? (sum / valid_count) : 0.0;
    report.l2_norm = std::sqrt(sum_sq);
    
    if (valid_count > 1) {
        double mean_sq = report.mean * report.mean;
        double avg_sq = sum_sq / valid_count;
        report.variance = avg_sq - mean_sq;
        if (report.variance < 0.0) report.variance = 0.0; 
    } else {
        report.variance = 0.0;
    }

    report.min_val = (min_v == std::numeric_limits<double>::infinity()) ? 0.0 : min_v;
    report.max_val = (max_v == -std::numeric_limits<double>::infinity()) ? 0.0 : max_v;

    return report;
}

template <typename T>
bool check_for_failures(const T* data, size_t size) {
    if (size == 0) return false;

    bool fail = false;
    
    // Removed #pragma omp simd (handled by -O3)
    #pragma omp parallel for reduction(||:fail)
    for (size_t i = 0; i < size; ++i) {
        double val = static_cast<double>(data[i]);
        if (std::isnan(val) || std::isinf(val)) {
            fail = true;
        }
    }
    return fail;
}

// Explicit Template Instantiation
template DebugReport compute_statistics<float>(const float*, size_t);
template DebugReport compute_statistics<double>(const double*, size_t);
template bool check_for_failures<float>(const float*, size_t);
template bool check_for_failures<double>(const double*, size_t);
