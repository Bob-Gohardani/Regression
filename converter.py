import sys
import random
from itertools import combinations_with_replacement

def main():
    if (sys.argv[1] == '-n'):
        dimension = sys.argv[2]
        degree = sys.argv[4]
        degree = int(degree)
        dimension = int(dimension)

        print dimension, degree
        input_it = reversed(xrange(dimension + 1))
        combinations = list(combinations_with_replacement(input_it, degree))

        for combination in combinations:
            row = list(combination)
            row.append(round(random.uniform(-1.0, 1.0),1))
            for i in xrange(len(row)):
                print row[i],
            print

    if (sys.argv[1] == '-d'):

        with open(sys.argv[2], "r") as description:
            dimension, degree = [int(x) for x in next(description).split()]
            description_indices = [[int(x) for x in line.split()[:-1]] for line in description]

        input = sys.stdin
        input_arr = [[float(x) for x in line.split()] for line in input]

        for it, input in enumerate(input_arr):
            for indices in description_indices[:-1]:
                value = 1.0
                for i in indices:
                    if i != 0:
                        value *= input[i - 1]
                print value,
            print

if __name__ == '__main__':
    main()
