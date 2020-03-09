# Lidar_filter
Python 3 implementation of range filter and temporal median filter for Lidar scans input

## Methods
Two different implementations are applied to solve the problem. One use purely Python build-in functions and libraries, the other one use Numpy library. The first method in general has better time complexity than the second one since it maintains the sorted list, not sorts the list in each update step of the median filter. However, the space complexity for the second method would be better since Numpy data structures take up less space.

### Range filter
#### Method 1.
For each scan input, use for-loop to check each element. If the element value is larger than range_max, then set the value to range_max; If the element value is smaller than range_min, then set the value to range_min; If the element value is Inf, -Inf or NaN, then throw an assertion error to remind the user to check the input data.
Time complexity is $O$
#### Method 2.

### Temporal median filter
#### Method 1.


#### Method 2.

