# python regularizer.py -t train_set.txt -i data_in.txt -o data_out.txt < description_in.txt > description_out.txt

import math
import os
import sys
import re

gamma = 0.02 # learning rate
k = 1 # always is 1 (linear regression)
dimension = 0 # dimension of the linear function
max_iters = 0 # read it from file
threshold = 0.01   # when gets to this point stop iterations
params = [] # array of p0.....pn
Y = []
N = 0# length of the train_data array
gradQ = 0
iters = 0

lamda = 0



# reading the description
desc = []
dummy = 0
for line in sys.stdin:
    if dummy == 0:
        dimension = int(line.split()[0])
        k = int(line.split()[1])
        dummy += 1
    elif line != '\n':
        l = [float(x) for x in line.replace('\n', '').replace('\r', '').strip().split(' ')]
        params.append(l[len(l)-1]) # last element of each line is the parameter
        desc.append(l) # always 1 element since k = 1



train_data = sys.argv[2]
# reading the train_set file :
inputz = []
with open(train_data, 'r') as f:
    for line in f:
        if line != '\n' and line != '\n\r':
            l = [float(x) for x in line.replace('\n', '').replace('\r', '').strip().split(' ')]
            Y.append(l[-1])
            l = l[:-1] # remove last element since its the result
            inputz.append(l)
            N += 1

data_in = sys.argv[4]
data_out = sys.argv[6]

with open(data_in, 'r') as f:
     max_iters = int(re.findall('\d+',f.readline())[0])
     lamda = float(re.findall('\d+\.\d+',f.readline())[0])



def calc_f(i):
    line = inputz[i]
    sum = 0
    start = 0
    for l in desc:
        s = float(params[start])
        start += 1
        #for i in range(0, dimension): no use for it since k = 1 here
        if(l[0]) != 0 :
            s *= line[int(l[0]) -1]
        sum += s
    return sum

def find_num(param):
    return desc[param][0]-1


def derivative(num):
    sigma = 0
    for i in range(0, N):
        if num == len(params)-1:   # p = 0 there is no regularizer  (it goes from P4 P3.....P0 so P0 is the last one)
            sigma += (calc_f(i) - Y[i])
        else: # after p = 0 we add regularizer to the gradient
            sigma += (calc_f(i) - Y[i]) * inputz[i][int(find_num(num))]
            
    deltaQ = (1 / float(N)) * sigma + (lamda * params[num]) / float(N)
    return deltaQ


def gradient_descent():
    global gradQ
    x = 0
    for i in range(0, len(params)):
        d = derivative(i)

        params[i] = params[i] - gamma * d
        x += d**2
    x = math.sqrt(x)    # this is the value of gradient for this iteration
    gradQ = x
    return(gradQ)


for i in range(0, max_iters):
    gradient_descent()
    iters += 1
    if (gradQ < threshold):
        break





f = open(data_out, "w")
f.write("iterations="+str(iters))
f.close()

print(str(dimension)+" "+"1")
for i in range(0, len(desc)):
    string = ""
    string += str(int(desc[i][0]))+" "
    string += str(params[i])
    print(string)
