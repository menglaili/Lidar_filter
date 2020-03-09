from filter import range_filter, median_filter
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--filter", "-f", help="filter type: 'r' for range and 'm' for median")
args = parser.parse_args()

if args.filter:
    if args.filter == 'r':
        ra = input("Please enter the range_min and range_max split by comma:")
        rmin, rmax = [float(num) for num in ra.split(',')]
        rg = range_filter(rmin, rmax)
        while True:
            scan = input("Please enter one scan in list form:")
            # enter s would stop the program
            if scan == 's':
                break
            scan = list(map(float, scan.strip('[]').split(',')))
            print(rg.update(scan))

    elif args.filter == 'm':
        D = int(input("Please enter the number D:"))
        med = median_filter(D)
        while True:
            scan = input("please enter one scan in list form:")
            # enter s would stop the program
            if scan == 's':
                break
            scan = list(map(float, scan.strip('[]').split(',')))
            print(med.update(scan))