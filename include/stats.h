#ifndef STATS_H
#define STATS_H

#include <cstddef>
#include <limits>

struct DebugReport {
    size_t nan_count;
    size_t inf_count;
    size_t valid_count;
    double mean;
    double min_val;
    double max_val;
};


DebugReport compute_statistics(const float* data, size_t size);

bool check_for_failures(const float* data, size_t size);

#endif // STATS_H