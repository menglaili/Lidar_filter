from filter import range_filter, median_filter
# from filter_withnp import range_filter, median_filter
import numpy as np
import time

class test():
    def __init__(self):
        self.rg = range_filter()
        self.med = median_filter(3)
        self.rmin = self.rg.range_min
        self.rmax = self.rg.range_max

    def test_exap(self):
        self.med.reset()
        # check correctness for range filter
        a = [0.029, 10, 50.1]
        scan = self.rg.update(a)
        correct1 = True
        if scan != [0.03, 10, 50]:
            correct1 = False

        # check correctness for median filter
        scan = self.med.update([0, 1, 2, 1, 3])
        correct2 = True
        if scan != [0, 1, 2, 1, 3]:
            correct2 = False
        scan = self.med.update([1, 5, 7, 1, 3])
        if scan != [0.5, 3.0, 4.5, 1.0, 3.0]:
            correct2 = False
        scan = self.med.update([2, 3, 4, 1, 0])
        if scan != [1.0, 3.0, 4.0, 1.0, 3.0]:
            correct2 = False
        scan = self.med.update([3, 3, 3, 1, 3])
        if scan != [1.5, 3.0, 3.5, 1.0, 3.0]:
            correct2 = False
        scan = self.med.update([10, 2, 4, 0, 0])
        if scan != [2.5, 3.0, 4.0, 1.0, 1.5]:
            correct2 = False

        return correct1, correct2

    ## test the correctness of two filters with random values scans
    def test_random(self, N = 100, D = 10, count = 10, extr = True):
        N = int(N)
        self.med.reset(D)
        # create random scans
        data = []
        data_np = np.zeros((count,N))
        for i in range(count):
            if extr == True:
                d1 = np.random.uniform(-1e5, 0, int(count * 0.2))
                d2 = np.random.uniform(self.rmax, self.rmax + 1e5, int(count * 0.2))
            else:
                d1 = np.random.uniform(0, self.rmin, int(count * 0.2))
                d2 = np.random.uniform(self.rmax, self.rmax+20, int(count*0.2))
            d3 = np.random.uniform(self.rmin, self.rmax, N-2*int(count*0.2))
            data_np[i, :] = np.hstack((d3,d1,d2))
            data.append(data_np[i, :].tolist())

        correct1 = True  # if correct1 == True then range_filter is correct
        correct2 = True  # if correct2 == True then median_filter is correct
        time1 = []
        time2 = []
        for i in range(count):
            # test the range filter
            start1 = time.time()
            result1 = self.rg.update(data[i])
            time1.append(time.time() - start1)
            result1 = np.array(result1)
            if np.any(result1<self.rmin) or np.any(result1>self.rmax):
                correct1 = False
            # test the median filter
            start2 = time.time()
            result2 = self.med.update(data[i])
            result2 = np.array(result2)
            time2.append(time.time() - start2)
            gt = np.median(data_np[:i+1, :], axis = 0) if i<= D else np.median(data_np[i-D:i+1, :], axis = 0)
            if np.any(result2!=gt) or np.any(result2!=gt):
                correct2 = False
        time1 = np.mean(time1)
        time2 = np.mean(time2)
        return correct1, correct2, time1, time2

    ## test the case of empty scan input
    def test_empty(self):
        self.med.reset()
        correct1 = True
        result1 = self.rg.update([])
        if result1 != []:
            correct1 = False
        correct2 = True
        result2 = self.med.update([])
        if result2 != []:
            correct2 = False
        return correct1, correct2

    ## test the response for extreme value i.e. Inf, NaN
    def test_extr(self):
        self.med.reset()
        data = [1, 2, float('NaN'), float('Inf'), -float('NaN')]
        correct1 = False
        try:
            self.rg.update(data)
        except AssertionError:
            correct1 = True
        correct2 = False
        try:
            self.med.update(data)
        except AssertionError:
            correct2 = True
        return correct1, correct2

    ## test the response for different scan shape
    def test_shape(self):
        self.med.reset()
        correct1 = True
        try:
            self.rg.update([0, 1, 2, 1, 3])
            self.rg.update([1, 2, 1, 3])
        except AssertionError:
            correct1 = False
        correct2 = False
        try:
            self.med.update([0, 1, 2, 1, 3])
            self.med.update([1, 2, 1, 3])
        except AssertionError:
            correct2 = True
        return correct1, correct2

    def test_result(self):
        ## test the correctness using the example
        correct1, correct2 = self.test_exap()
        if correct1 and correct2:
            print('Example 0: Pass')

        ## test the correctness: N = 100, D = 10, number of scans = 10, no super large/small values (base case)
        correct1, correct2, time1, time2 = self.test_random(extr = False)
        if correct1 and correct2:
            print('Example 1: Pass; Update step average time: %.2e/s for range filter, %.2e/s for median filter' % (time1, time2))

        ## test the correctness: N = 100, D = 10, number of scans = 10, with super large/small values
        correct1, correct2, time1, time2 = self.test_random(extr = True)
        if correct1 and correct2:
            print('Example 2: Pass; Update step average time: %.2e/s for range filter, %.2e/s for median filter' % (time1, time2))

        ## test the correctness when large dimension: N = 1e3, D = 10, number of scans = 10
        correct1, correct2, time1, time2 = self.test_random(N = 1000, extr = False)
        if correct1 and correct2:
            print('Example 3: Pass; Update step average time: %.2e/s for range filter, %.2e/s for median filter' % (time1, time2))

        ## test the correctness when D is large
        correct1, correct2, time1, time2 = self.test_random(N = 1000, D = 800, count = 500, extr=False)
        if correct1 and correct2:
            print('Example 4: Pass; Update step average time: %.2e/s for range filter, %.2e/s for median filter' % (time1, time2))

        ## test the correctness when scan is empty
        correct1, correct2 = self.test_empty()
        if correct1 and correct2:
            print('Example 5: Pass')

        ## test the response for extreme value i.e. Inf, NaN
        correct1, correct2 = self.test_extr()
        if correct1 and correct2:
            print('Example 6: Pass')

        ## test the response for different scan shape
        correct1, correct2 = self.test_shape()
        if correct1 and correct2:
            print('Example 7: Pass')


Test = test()
Test.test_result()

