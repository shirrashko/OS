// OS 24 Project1

#include "memory_latency.h"
#include "measure.h"

#define GALOIS_POLYNOMIAL ((1ULL << 63) | (1ULL << 62) | (1ULL << 60) | (1ULL << 59))

/**
 * Measures the average latency of accessing a given array.
 * @param repeat - the number of times to repeat the measurement for and average on.
 * @param arr - an allocated (not empty) array to preform measurement on.
 * @param arr_size - the length of the array arr.
 * @param zero - a variable containing zero in a way that the compiler doesn't "know" it in compilation time.
 * @return struct measurement containing the measurement with the following fields:
 *      double baseline - the average time (ns) taken to preform the measured operation without memory access.
 *      double access_time - the average time (ns) taken to preform the measured operation with memory access.
 *      uint64_t rnd - the variable used to randomly access the array, returned to prevent compiler optimizations.
 */
struct measurement measure_latency(uint64_t repeat, array_element_t* arr, uint64_t arr_size, uint64_t zero){
    // Ensure the repeat count is at least as large as the array size to avoid index out of bounds.
    repeat = arr_size > repeat ? arr_size:repeat; // Make sure repeat >= arr_size

    // Baseline measurement setup: no memory access involved
    struct timespec t0;
    timespec_get(&t0, TIME_UTC);
    register uint64_t rnd=12345; // Initial seed for the pseudo-random number generator

    // Baseline measurement: perform pseudo-random calculations without accessing the array
    for (register uint64_t i = 0; i < repeat; i++)
    {
        register uint64_t index = rnd % arr_size; // Calculate a random index in the array
        rnd ^= index & zero; // XOR operation with zero doesn't change anything. This operation is done with zero,
        // which the compiler is unaware of the fact it is zero, to prevent the compiler from optimizing it out.
        rnd = (rnd >> 1) ^ ((0-(rnd & 1)) & GALOIS_POLYNOMIAL);  // Advance rnd pseudo-randomly (using Galois LFSR)
    }
    struct timespec t1;
    timespec_get(&t1, TIME_UTC); // Get the time after the baseline measurement

    // Memory access measurement:
    struct timespec t2;
    timespec_get(&t2, TIME_UTC); // Get the time before the memory access measurement
    rnd=(rnd & zero) ^ 12345; // Reset rnd for memory access measurement to 12345
    for (register uint64_t i = 0; i < repeat; i++)
    {
        register uint64_t index = rnd % arr_size;
        rnd ^= arr[index] & zero; // This time access the array as well
        rnd = (rnd >> 1) ^ ((0-(rnd & 1)) & GALOIS_POLYNOMIAL);  // Advance rnd pseudo-randomly (using Galois LFSR)
    }
    struct timespec t3;
    timespec_get(&t3, TIME_UTC); // Get the time after the memory access measurement

    // Calculate baseline and memory access times:
    double baseline_per_cycle=(double)(nanosectime(t1)- nanosectime(t0))/(repeat);
    double memory_per_cycle=(double)(nanosectime(t3)- nanosectime(t2))/(repeat);
    struct measurement result;

    result.baseline = baseline_per_cycle;
    result.access_time = memory_per_cycle;
    result.rnd = rnd; // Return the last used rnd value to ensure it is not optimized out
    return result;
}
