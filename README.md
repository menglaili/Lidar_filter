# Lidar_filter
Python 3 implementation of range filter and temporal median filter for Lidar scans input

## Methods
Two different implementations are applied to solve the problem. One use purely Python build-in functions and libraries (bisect, math), the other one use Numpy library. The space complexity for the second method would be better since Numpy data structures take up less space. However, for the midian filter, the first method has better time complexity than the second one since it maintains the sorted list, not sorts the list in each update step.

### Range filter
#### Method 1.
For each scan input, use for-loop to check each element. If the element value is larger than range_max, then set the value to range_max; If the element value is smaller than range_min, then set the value to range_min; If the element value is Inf, -Inf or NaN, then throw an assertion error.

Time complexity is O(N)

#### Method 2.
Use vectorization of Numpy array. Create two 1D boolean maskes for finding out indices where value is larger than range_max  or smaller than range_min. Assign range_max and range_min respectively to these outlier. If any element value is Inf, -Inf or NaN, then throw an assertion error.

Time complexity is O(N)

### Temporal median filter
#### Method 1.
The bisect.insort function can insert element to a list while maintaining the sorted order of it. For a N-dimensional scan, a list of N lists L1 are created. For each update step, insert each element of the new scan to its corresponding list using bisect.insort i.e. receive scan = [1,2,3], L1 changes from [[0],[1],[2]] to [[0,1],[1,2],[2,3]]. For each dimension, given the sorted list, the median is the middle value if N is odd, or the average of two middle values if N is even. 

Create another list of N lists L2 to store every scan since the first one. If no more than D scans are received, compute the median of each list in L1 and return them as a new list. If D scans are received, then pop out the first element in each of the N lists in L2, i.e. D = 1, receive scan = [2,3,4], L2 changes from [[0,1],[1,2],[2,3]] to [[1,2],[2,3],[3,4]], pop out 0,1,2 from corresponding lists; Remove the poped element from corresponding list in L1 and the sorted order won't break; Compute the median of each list in L1 and return them as a new list.

Time complexity is O(DN) since insert to a sorted list is O(D) and we have to do it for N lists.

#### Method 2.
Create a Numpy array L1(one row is one scan) to store the scans store every scan since the first one. If no more than D scans are received, compute the median of each column of L1 using np.median and return them as a new list. If D scans are received, then delete the first row of L1, compute the median of each column of the remaining L1.

Time complexity is O(DNlogD) since in each update step, each column needs to be sorted in O(DlogD) and there are N columns.




