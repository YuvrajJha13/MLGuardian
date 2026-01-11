#include "stats.h"
#include <cmath>
#include <algorithm>
#include <limits>
#include <cfloat>

#ifdef _OPENMP
#include <omp.h>
#endif

DebugReport compute_statistics(const float* data, size_t size) {
    // 1. Defensive Coding: Handle empty arrays immediately
    if (size == 0) {
        DebugReport report = {0, 0, 0, 0.0, 0.0, 0.0};
        return report;
    }

    // 2. Initialize counters and stats variables
    size_t nan_count = 0, inf_count = 0, valid_count = 0;
    double sum = 0.0;
    double min_v = std::numeric_limits<double>::infinity();
    double max_v = -std::numeric_limits<double>::infinity();

    // 3. Parallel Loop with Reduction (Thread-Safe)
    // reduction clause ensures variables are merged correctly at the end
    #pragma omp parallel for reduction(+:nan_count, inf_count, valid_count, sum) reduction(min:min_v) reduction(max:max_v)
    for (size_t i = 0; i < size; ++i) {
        float val = data[i];
        
        // Check for failure cases
        if (std::isnan(val)) {
            nan_count++;
        } else if (std::isinf(val)) {
            inf_count++;
        } else {
            // Update Stats for Valid Values
            if (val < min_v) min_v = val;
            if (val > max_v) max_v = val;
            // Explicit cast to double to avoid precision loss in sum
            sum += static_cast<double>(val);
            valid_count++;
        }
    }

    // 4. Construct Result Report
    DebugReport report;
    report.nan_count = nan_count;
    report.inf_count = inf_count;
    report.valid_count = valid_count;
    
    // Safe division: avoid NaN from 0/0
    report.mean = (valid_count > 0) ? (sum / valid_count) : 0.0;
    
    // Handle cases where min/max were never updated (all NaNs/Infs)
    report.min_val = (min_v == std::numeric_limits<double>::infinity()) ? 0.0 : min_v;
    report.max_val = (max_v == -std::numeric_limits<double>::infinity()) ? 0.0 : max_v;

    return report;
}

bool check_for_failures(const float* data, size_t size) {
    // 1. Defensive Coding: Empty array is healthy
    if (size == 0) return false;

    bool fail = false;
    
    // 2. Parallel Short-Circuit Evaluation
    // reduction(||:fail): If ANY thread finds fail=true, the final result is true.
    #pragma omp parallel for reduction(||:fail)
    for (size_t i = 0; i < size; ++i) {
        if (std::isnan(data[i]) || std::isinf(data[i])) {
            fail = true;
        }
    }
    return fail;
}