import numpy as np

class range_filter():
    def __init__(self, range_min=0.03, range_max=50):
        self.range_min = range_min
        self.range_max = range_max

    def update(self, scan):
        '''
        input: measurements in list in one step
        output: filtered scan
        Using numpy's vectorization method to create boolean mask and eliminate outliers
        '''
        # check extreme values
        assert np.all(np.isfinite(scan)), 'The scan contains Inf or NaN!'
        scan1 = np.array(scan).astype(float)
        scan1[scan1<self.range_min] = self.range_min
        scan1[scan1>self.range_max] = self.range_max
        return scan1.tolist()


class median_filter():
    def __init__(self, D=3):
        self.D = D
        self.time = 0


    def update(self, scan):
        '''
        input: measurements in list in one step
        output: filtered scan
        Using Python build-in bisect function to insert element to a list,
        while keeping the sorted order in O(M) time where M is the number of element
        '''
        scan = np.array(scan).astype(float)
        # check extreme values
        assert np.all(np.isfinite(scan)), 'The %dth scan contains Inf or NaN!' % self.time
        if len(scan.shape) == 1:
            scan = scan[np.newaxis, ...]
        if self.time == 0:
            self.time += 1
            self.N = scan.shape[1]
            self.stored = scan
            return scan[0, :].tolist()
        # make sure the self.N matches with len(scan)
        assert scan.shape[1] == self.N, 'The %dth scan\'s shape changes!' % self.time

        self.stored = np.append(self.stored, scan, axis = 0)
        if self.time > self.D:
            self.stored = self.stored[1:, :]
        self.time += 1
        return np.median(self.stored, axis = 0).tolist()

    def reset(self, D=3):
        self.time = 0
        self.D = D

if __name__ == '__main__':
    # check correctness for range filter
    a = [0.029, 10, 50.1]
    b = range_filter()
    scan = b.update(a)
    print(scan==[0.03, 10, 50])

    # check correctness for median filter
    a = median_filter(3)  # different shape input
    scan = a.update([0, 1, 2, 1, 3])
    scan = a.update([1, 2, 1, 3])

    a = median_filter(3)  # extreme values
    scan = a.update([1,2, float('NaN'), float('Inf'), -float('NaN')])

    a = median_filter(3)
    scan = a.update([0, 1, 2, 1, 3])
    print(scan==[0, 1, 2, 1, 3])
    scan = a.update([1, 5, 7, 1, 3])
    print(scan==[0.5, 3.0, 4.5, 1.0, 3.0])
    scan = a.update([2, 3, 4, 1, 0])
    print(scan==[1.0, 3.0, 4.0, 1.0, 3.0])
    scan = a.update([3, 3, 3, 1, 3])
    print(scan == [1.5, 3.0, 3.5, 1.0, 3.0])
    scan = a.update([10, 2, 4, 0, 0])
    print(scan == [2.5, 3.0, 4.0, 1.0, 1.5])
