#include "stats.h"
#include <cmath>
#include <algorithm>
#include <limits>
#ifdef _OPENMP
#include <omp.h>
#endif

DebugReport compute_statistics(const float* data, size_t size) {
    size_t nan_count = 0, inf_count = 0, valid_count = 0;
    double sum = 0.0;
    double min_v = std::numeric_limits<double>::infinity();
    double max_v = -std::numeric_limits<double>::infinity();

    #pragma omp parallel for reduction(+:nan_count, inf_count, valid_count, sum) reduction(min:min_v) reduction(max:max_v)
    for (size_t i = 0; i < size; ++i) {
        float val = data[i];
        if (std::isnan(val)) nan_count++;
        else if (std::isinf(val)) inf_count++;
        else {
            if (val < min_v) min_v = val;
            if (val > max_v) max_v = val;
            sum += val;
            valid_count++;
        }
    }

    DebugReport report;
    report.nan_count = nan_count; report.inf_count = inf_count; report.valid_count = valid_count;
    report.mean = (valid_count > 0) ? (sum / valid_count) : 0.0;
    report.min_val = (valid_count > 0) ? min_v : 0.0;
    report.max_val = (valid_count > 0) ? max_v : 0.0;
    return report;
}

bool check_for_failures(const float* data, size_t size) {
    bool fail = false;
    #pragma omp parallel for reduction(||:fail)
    for (size_t i = 0; i < size; ++i) {
        if (std::isnan(data[i]) || std::isinf(data[i])) fail = true;
    }
    return fail;
}