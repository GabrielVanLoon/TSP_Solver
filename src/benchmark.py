"""
    Benchmark generate stats for the solvers
"""
import time 
from alltours import alltours

NUM_CITIES = 3

def timeit(callback):
    t0 = time.perf_counter()
    tour_length = callback(NUM_CITIES)
    t1 = time.perf_counter()
    return tour_length

@functools.lru_cache(None)
def benchmark(callback, inputs):
    "Run function on all the inputs; return pair of (average_time_taken, results)."
    t0           = time.clock()
    results      = [callback(x) for x in inputs]
    t1           = time.clock()
    average_time = (t1 - t0) / len(inputs)
    return (average_time, results)

print(timeit(alltours.tsp_alltours))