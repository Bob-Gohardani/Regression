import math
import os
import sys
import re
import random
from itertools import combinations_with_replacement

# python regressor.py -t set.txt < in.txt > out.txt
train_data = []
scaled_data = {}
validation_sets = []
training_sets = []
dim = 0


def findMinMax():
    ran = 0
    dummy = 0
    with open(sys.argv[2], 'r') as f:
        for line in f:
            if line != '\n' and line != '\n\r':
                l = [float(x) for x in line.replace('\n', '').replace('\r', '').strip().split(' ')]
                global dim
                dim = len(l) - 1  # get number of variables in each line
                train_data.append(l)
                if dummy == 0:
                    ran = len(l)  # ran is the length of each line of the training set
                    dummy += 1
    dct = {}
    for i in range(ran):
        dct[i] = []


    with open(sys.argv[2], 'r') as f:
        for line in f:
            if line != '\n' and line != '\n\r':
                l = [float(x) for x in line.replace('\n', '').replace('\r', '').strip().split(' ')]
                for i in range(ran):
                    dct[i].append(l[i])

    for key in dct:
        high = max(dct[key])
        low = min(dct[key])
        dct[key] = []
        dct[key].append(low)
        dct[key].append(high)
    return dct


def ScaleData():
    dct = findMinMax()   # calls findMinMax() function

    for j in range(len(train_data)):
        scaled_data[j] = []
        l = train_data[j]
        for i in range(len(l)):
            # do not scale the y values:
            if i != len(l)-1:
                y = (2 * ((l[i] - dct[i][0]) / (dct[i][1] - dct[i][0]))) - 1
                scaled_data[j].append(y)
            else:
                scaled_data[j].append(l[i])


def chunker_list(list, split):
    L = list[:]
    random.shuffle(L)
    return [L[x::split] for x in range(split)]

def splitData():
    ScaleData()
    number_of_split= 2
    setj = []
    for key, value in scaled_data.iteritems():
        temp = value
        setj.append(temp)

    set_length = len(setj)
    totalsubset= int(number_of_split)*2
    len_of_each= set_length/totalsubset

# create all training sets
    for i in range(0, number_of_split):
        sub_set = []
        for j in range(0,int(len_of_each)):
            #select random index
            sub_line = []
            x=random.randint(0,len(setj)-1)
            for a in range (len(setj[0])):
                sub_line.append(setj[x][a])
            setj.remove(setj[x][:])
            sub_set.append(sub_line)
        training_sets.append(sub_set)

# create all validation sets
    for i in range(0, number_of_split):
        sub_set = []
        for j in range(0, int(len_of_each)):
            # select random index
            sub_line = []
            x = random.randint(0, len(setj) - 1)
            for a in range (len(setj[0])):
                sub_line.append(setj[x][a])
            setj.remove(setj[x][:])
            sub_set.append(sub_line)
        validation_sets.append(sub_set)

def train(n,k,input_data):
    gamma = 0.02 # learning rate
    dimension = n # dimension of the linear function
    max_iters = 1000
    threshold = 0.04   # when gets to this point stop iterations
    params = [] # array of p0.....pn
    indiceZ = []
    Y = []
    N = 0# length of the train_data array
    gradQ = 0
    inputz = []

    k = int(k)
    n = int(n)
    desc = []
    nstring = ""
    for i in range(n+1):
        nstring+= str(i)


    l =  list(combinations_with_replacement(nstring, k))
    l = [x for x in l[::-1]]
    l2 = []
    for i in l:
        l1 = list(i)
        l2.append("".join([x for x in l1[::-1]]))
    l2 = sorted(l2, reverse = True)

    for i in l2:
        string = ""
        string += " ".join(i)
        string += " "+str(round(random.uniform(-1, 1), 1))
        desc.append([float(i) for i in string.split()])

    for line in desc:
        params.append(line[len(line) - 1])  # last element of each line is the parameter
        indiceZ.append(line[:-1])

    input_arr = [line[:-1] for line in input_data]
    Y = [line[-1] for line in input_data]

    for it, input in enumerate(input_arr):
        x = []
        for indices in indiceZ[:-1]:
            value = 1.0
            for i in indices:
                if i != 0:
                    value *= input[int(i)-1]
            x.append(value)
        inputz.append(x)

    N = len(inputz)

    def calc_f(i):
        line = inputz[i]
        total = 0
        start = 0
        for l in desc:
            s = float(params[start])
            start += 1
            for j in l[:-1]:  # we multiplie each element in list with related number in input data
                if(j) != 0 :
                    s *= line[int(j) -1]
                total += s
        return total

    def find_num(param):
        return desc[param][0]-1

    def derivative(num):
        sigma = 0
        for i in range(0, N):
            if num == len(params)-1:
                sigma += (calc_f(i) - Y[i])
            else:
                sigma += (calc_f(i) - Y[i]) * inputz[i][int(find_num(num))]
        if(N != 0):
            return (1 / float(N)) * sigma


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

    for u in range(0, max_iters):
        gradQ = gradient_descent()
        if (gradQ < threshold):
            break
    results = []
    for i in range(0, len(desc)):
        string = ""
        for j in range(0, len(desc[i])-1):
            string += str(desc[i][j])+" "
        string += str(params[i])
        x = string.split(" ")
        results.append(x)
    return results

def testIt(dimz, hyper, description, a, data=None):
    desc = description
    n = dimz
    k = hyper

    def power(num, line):
        if num == 0:
            return 1
        else:
            return line[int(num)-1]

    scaled_data_test = []
    if data:
        scaled_data_test = [line[:-1] for line in data]

    else:
        # scale the data:
        dct = findMinMax()
        test_data = []

        for line in sys.stdin:
            if line != '\n' and line != '\n\r':
                l = [float(x) for x in line.replace('\n', '').replace('\r', '').strip().split(' ')]
                test_data.append(l)

        for i in range(len(test_data)):
            scaled_data_test.append([])

        for j in range(len(test_data)): # for each line of the input numbers
            l_testData = test_data[j]
            for i in range(len(l_testData)): # then for each number inside this line(based on column1 or 2 or ...)
                y = (2 * ((l_testData[i] - dct[i][0]) / (dct[i][1] - dct[i][0]))) - 1
                scaled_data_test[j].append(y)

    results = []
    for line in scaled_data_test:
        total = 0
        for m in desc:
            s = float(m[k])
            for i in range(0, k):
                s *= power(float(m[i]), line)
            total += s
        results.append(total)

    # results are always one line - each of them is one number
    if a == "final":
        for res in results:
            print(res)

    elif a == "valid":
        return results


splitData()
evaluations = []
for k in range(1, 6):
    # we train training set then use the parameters for validation set then based on errors choose Hyper Parameter
    # when you train with a train_set, you need to test it with validation_set of same set
    qualityList = []
    qualityList.append(k)
    for i in range(len(training_sets)):
        train_set = training_sets[i]
        desc_valid = train(dim, k, train_set)
        validation_set = validation_sets[i]
        out_arr = testIt(dim, k, desc_valid, "valid", validation_set) # get result of test with validatio set X
        lines_1 = []
        lines_1 = [line[-1] for line in validation_set]   # select Y input from validation_set
        total = 0
        for i in range(len(out_arr)):
            total += pow((out_arr[i] - lines_1[i]), 2)
        #Quality =  math.sqrt(total) / (2 * len(out_arr))
        Quality =  total / (2 * len(out_arr))
        qualityList.append(Quality)
    evaluations.append(qualityList) # each number in each line is the error of one split of evaluation set

eva_1 =[line[1:] for line in evaluations]
eva_1 =[sum(line)/len(line) for line in eva_1]
eva_2 =[line[0] for line in evaluations]

hyper = eva_2[eva_1.index(min(eva_1))]
scaled_full = []
for key, value in scaled_data.iteritems():
    temp = value
    scaled_full.append(temp)

description_final = train(dim, hyper, scaled_full) # final training of the full data to get correct parameters
testIt(dim, hyper, description_final, "final")