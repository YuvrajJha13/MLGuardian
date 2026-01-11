#ifndef STATS_H
#define STATS_H
#include <cstddef>
#include <limits>

struct DebugReport {
    size_t nan_count;
    size_t inf_count;
    size_t valid_count;
    double mean;
    double variance;
    double l2_norm; // sqrt(sum of squares) - Critical for Gradient Clipping
    double min_val;
    double max_val;
};

// Template support for float32 and float64
template <typename T>
DebugReport compute_statistics(const T* data, size_t size);

template <typename T>
bool check_for_failures(const T* data, size_t size);

#endif