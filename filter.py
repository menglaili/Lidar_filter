from bisect import insort
import math

class range_filter():
    def __init__(self, range_min = 0.03, range_max=50):
        self.range_min = range_min
        self.range_max = range_max

    def update(self, scan):
        '''
        input: measurements in list in one step
        output: filtered scan
        Using for-loop to check whether each element satisfying the condition, and eliminate outliers
        '''
        scan_new = []
        for i in range(len(scan)):
            assert (scan[i] not in [-float('Inf'), float('Inf')]) and (not math.isnan(scan[i])), \
                'The %dth element of the scan is Inf or NaN!' % i
            if scan[i] > self.range_max:
                scan_new.append(self.range_max)
            elif scan[i] < self.range_min:
                scan_new.append(self.range_min)
            else:
                scan_new.append(scan[i])
        return scan_new


class median_filter():
    def __init__(self, D):
        self.D = D
        self.time = 0  # counting the input times
        self.rmax = 50
        self.rmin = 0.03

    def update(self, scan):
        '''
        input: measurements in list in one step
        output: filtered scan
        Create N empty list and using Python build-in bisect function to insert element to each list,
        while keeping the sorted order in O(M) time where M is the number of element in one list
        '''
        filtered = []
        if self.time == 0:
            self.N = len(scan)
            self.prev_list = [[] for i in range(self.N)]
            self.stored = [[] for i in range(self.N)]
        # make sure the self.N matches with len(scan)
        assert len(scan) == self.N, 'The %dth scan\'s shape changes!' % self.time

        for ind in range(self.N):
            # check extreme values
            assert (scan[ind] not in [-float('Inf'), float('Inf')]) and (not math.isnan(scan[ind])), \
                    'The %dth element in %dth scan is Inf or NaN!' % (ind, self.time)
            # store previous values
            self.prev_list[ind].append(scan[ind])
            # insert value to list and maintain the order
            insort(self.stored[ind], scan[ind])
            if self.time>self.D: # after D times, delete the earliest element
                prev = self.prev_list[ind].pop(0)
                self.stored[ind].remove(prev)
                # find median
                if (self.D + 1) % 2 == 0:
                    avg = 0.5*(self.stored[ind][self.D//2] + self.stored[ind][self.D//2+1])
                    filtered.append(avg)
                else:
                    filtered.append(self.stored[ind][((self.D+1)//2)])
            else:
                # find median
                if (self.time + 1) % 2 == 0:
                    avg = 0.5 * (self.stored[ind][self.time//2] + self.stored[ind][self.time//2+1])
                    filtered.append(avg)
                else:
                    filtered.append(self.stored[ind][((self.time+1)//2)])

        self.time += 1
        return filtered

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
    scan = a.update([1, 2, float('NaN'), float('Inf'), -float('NaN')])

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