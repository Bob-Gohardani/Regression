import os
import sys

desc = []
n = 0
k = 0

def power(num, line):
    if num == 0:
        return 1
    else:
        return line[int(num)-1]

desc_file = sys.argv[2]

with open(desc_file, 'r') as f:
    first_line = f.readline()
    n = int(first_line.split()[0])
    k = int(first_line.split()[1])
    for line in f:
        if line != '\n':
            l = [float(x) for x in line.replace('\n', '').replace('\r', '').strip().split(' ')]
            desc.append(l)


inputz = []
for line in sys.stdin:
    if line != '\n' and line != '\n\r':
        l = [float(x) for x in line.replace('\n', '').replace('\r', '').strip().split(' ')]
        inputz.append(l)

for line in inputz:
    sum = 0
    for l in desc:
        s = float(l[k])
        for i in range(0, k):
            s *= power(l[i], line)
        sum += s
    print(sum)
