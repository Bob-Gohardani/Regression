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

# find min / max of the dataset
def findMinMax():
    ran = 0
    dummy = 0
	# open the file, read each line of it, add it to a list object "l" then add "l" to train_data list
    with open(sys.argv[2], 'r') as f:
        for line in f:
            if line != '\n' and line != '\n\r':
                l = [float(x) for x in line.replace('\n', '').replace('\r', '').strip().split(' ')]
				# length of each line-1 is dimension
                global dim
                dim = len(l) - 1 
                train_data.append(l)
				
                if dummy == 0:
                    ran = len(l) 
                    dummy += 1
	# create empty dictionary and give it free space
    dct = {}
    for i in range(ran):
        dct[i] = []

	# we open the file again and this time attach the data to the dictionary that we created earlier
    with open(sys.argv[2], 'r') as f:
        for line in f:
            if line != '\n' and line != '\n\r':
                l = [float(x) for x in line.replace('\n', '').replace('\r', '').strip().split(' ')]
                for i in range(ran):
                    dct[i].append(l[i])
# in this part we try to find min and max for each iteration in the dictioanry, empty the dict and add min/max to it
    for key in dct:
        high = max(dct[key])
        low = min(dct[key])
        dct[key] = []
        dct[key].append(low)
        dct[key].append(high)
    return dct


# in this function we scale the data from 0 to 1
def ScaleData():
    dct = findMinMax() 
	# here we loop through the train_data list and scale each row based on the min/max values that we have from dictionary
    for j in range(len(train_data)):
        scaled_data[j] = []
        l = train_data[j]
        for i in range(len(l)):
            if i != len(l)-1:
                y = (2 * ((l[i] - dct[i][0]) / (dct[i][1] - dct[i][0]))) - 1
                scaled_data[j].append(y)
			# last element of each row is the Y prediction and we dont need to scale it
            else:
                scaled_data[j].append(l[i])


# not used!!!
#def chunker_list(list, split):
   # L = list[:]
   # random.shuffle(L)
   # return [L[x::split] for x in range(split)]

# in this function we split data for the validation / train sets	
def splitData():
    ScaleData()
    number_of_split= 2
    setj = []
	
	# save all scaled data from dictionary into a list :
    for key, value in scaled_data.iteritems():
        temp = value
        setj.append(temp)

	# since split is two, we have four subsets and here we find length of each of them
    set_length = len(setj)
    totalsubset= int(number_of_split)*2
    len_of_each= set_length/totalsubset


	# here we  create the train set based on the repeated random sub_sampling algorithm:
    for i in range(0, number_of_split):
        sub_set = []
		# loop through for length of each subset
        for j in range(0,int(len_of_each)):
           
            sub_line = []
			# find a random number from set and find element related to it
            x=random.randint(0,len(setj)-1)
            for a in range (len(setj[0])):
                sub_line.append(setj[x][a])
			# remove that element
            setj.remove(setj[x][:])
            sub_set.append(sub_line)
        training_sets.append(sub_set)

# same as above but fpr validation subsets:
    for i in range(0, number_of_split):
        sub_set = []
        for j in range(0, int(len_of_each)):
            sub_line = []
            x = random.randint(0, len(setj) - 1)
            for a in range (len(setj[0])):
                sub_line.append(setj[x][a])
            setj.remove(setj[x][:])
            sub_set.append(sub_line)
        validation_sets.append(sub_set)

		
def train(n,k,input_data):
    gamma = 0.09
	# set max iterations of gradient descent to 5000 iterations and set threshold to 0.0001
    max_iters = 5000
    threshold = 0.0001   
    params = [] 
    indiceZ = []
    Y = []
    N = 0
    gradQ = 0
    inputz = []

    k = int(k)
    n = int(n)
    desc = []
	# empty string
    nstring = ""
	# create a string of numbers from 0 to n:
    for i in range(n+1):
        nstring+= str(i)
	#based on the k create all combinations of nstring that is possible and unique then turn it from string to number list:
    l =  list(combinations_with_replacement(nstring, k))
    l = [x for x in l[::-1]]
	
	# create empty list then  join all inner elements of l list to the l2 list except last element from biggest to smallest
    l2 = []
    for i in l:
        l1 = list(i)
        l2.append("".join([x for x in l1[::-1]]))
    l2 = sorted(l2, reverse = True)

	# transform l2 into the description of the linear regression:
    for i in l2:
        string = ""
        string += " ".join(i)
        string += " "+str(round(random.uniform(-1, 1), 1))
        desc.append([float(i) for i in string.split()])

	# from description divide parameters and indices:
    for line in desc:
        params.append(line[len(line) - 1])  
        indiceZ.append(line[:-1])

	# seperate input data and result Y
    input_arr = [line[:-1] for line in input_data]
    Y = [line[-1] for line in input_data]

	# here first we loop through each row of inputs then we go through indices, here our goal is if we have x1*x2*x3 or x2^2 get the full number and save it to a list:
    # this basically means we have one variable for each param (x1,x2,...) so it turns into a linear regression from polynomial regression (lowers degree to 1)
	for it, input in enumerate(input_arr):
        x = []
        for indices in indiceZ[:-1]:
            value = 1.0
            for i in indices:
                if i != 0:
                    value *= input[int(i)-1]
            x.append(value)
        inputz.append(x)

	
	# here we start creating the description again, but this time base it on a k=1 linear regression
    n = len(params)-1
    k =1
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

    params = []
    for line in desc:
        params.append(line[len(line) - 1]) 
        indiceZ.append(line[:-1])

    N = len(inputz)
	
	# we calculate the function f(x,p) 
	# multiplie each parameter by its variable then add them up together
    def calc_f(i):
        line = inputz[i]
        total = 0
        start = 0
        for l in desc:
            s = float(params[start])
            start += 1
            if(l[0]) != 0 :
                s *= line[int(l[0]) -1]
            total += s
        return total

	# this function helps to select which x for derivative 
	# basically (0, N) is the ith parameter and here we find Xj that matches with that
	# we give it id of parameter and it returns it back
    def find_num(param):
        return desc[param][0]-1

	# here we calculate the derivate based on the formula for each parameter, last parameter doesnt have "x" multiplication
    def derivative(num):
        sigma = 0
		# n is how many input variables/parameters we have
        for i in range(0, N):
            if num == len(params)-1:
                sigma += (calc_f(i) - Y[i])
            else:							  # returns variable in the row connected to the param
                sigma += (calc_f(i) - Y[i]) * inputz[i][int(find_num(num))]
        if(N != 0):
            return (1 / float(N)) * sigma


	# in this function we calculate gradient descent for each of the parameters, update the parameter and calculate the quality parameter
    def gradient_descent():
        global gradQ
        x = 0
        for i in range(0, len(params)):
            d = derivative(i)
            params[i] = params[i] - gamma * d
            x += d**2
        x = math.sqrt(x)    
        gradQ = x
        return(gradQ)

	# in this loop we calculate gradient until either we reach max iteration or we have quality smaller than the threshold:
    for u in range(0, max_iters):
        gradQ = gradient_descent()
        if (gradQ < threshold):
            break
    results = []
    results.append([n, 1])

	# at end we add all new parameters as a string and send it for test function:
    for i in range(0, len(desc)):
        string = ""
        for j in range(0, len(desc[i])-1):
            string += str(desc[i][j])+" "
        string += str(params[i])
        x = string.split(" ")
        results.append(x)
    return results

	
# this is the method to test our data :
def testIt(n1,k1, description, a, data=None):
# get n/k/description from program:
    n = description[0][0]
    k = description[0][1]
    desc = description[1:] # first line is n and k

# if num is zero means just ignore that variable otherwise return variable related to the number from description
    def power(num, line):
        if num == 0:
            return 1
        else:
            return line[int(num)-1]
	
	# if it is a validation test there is no need for scaling otherwise we scale the test data:
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

        for j in range(len(test_data)): 
            l_testData = test_data[j]
            for i in range(len(l_testData)): 
                y = (2 * ((l_testData[i] - dct[i][0]) / (dct[i][1] - dct[i][0]))) - 1
                scaled_data_test[j].append(y)
				
# here we create a new description file so we can transform our scaled data from polynomial to linear (description from train function is linear)
    indiceZ = []
    k1 = int(k1)
    n1 = int(n1)
    desc1 = []
    nstring = ""
    for i in range(n1+1):
        nstring+= str(i)
    l =  list(combinations_with_replacement(nstring, k1))
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
        desc1.append([float(i) for i in string.split()])

    for line in desc1:
        indiceZ.append(line[:-1])

    input_arr = scaled_data_test
    inputz = []
    for it, input in enumerate(input_arr):
        x = []
        for indices in indiceZ[:-1]:
            value = 1.0
            for i in indices:
                if i != 0:
                    value *= input[int(i)-1]
            x.append(value)
        inputz.append(x)
    scaled_data_test = inputz

	# here we multiplie the parameters by the variables and return the results:
    results = []
    for line in scaled_data_test:
        total = 0
        for m in desc:
            s = float(m[k]) # parameter is last element in each description row
            for i in range(0, k):
                s *= power(float(m[i]), line)
            total += s
        results.append(total)
    if a == "final":
        for res in results:
            print(res)

    elif a == "valid":
        return results


		
# call split function and make an evaluations list
splitData()
evaluations = []
# loop through k from 1 to 6:
for k in range(1, 6):
    qualityList = []
    qualityList.append(k)
	
	#loop through length of our training/validation subsets:
    for i in range(len(training_sets)):
        train_set = training_sets[i]
		# create description from the training function :
        desc_valid = train(dim, k, train_set)
        validation_set = validation_sets[i]
		# test out validation data based on the description we got and the k we give it :
        out_arr = testIt(dim, k, desc_valid, "valid", validation_set)

		# get the results from the validation test :
        lines_1 = []
        lines_1 = [line[-1] for line in validation_set]  
        total = 0
		# loop through all results and compare them with real results then add the quality based on that to evaluation set:
        for i in range(len(out_arr)):
            total += pow((out_arr[i] - lines_1[i]), 2)
        Quality =  total / (2 * len(out_arr))
        qualityList.append(Quality)
    evaluations.append(qualityList)
# first element is K :
eva_1 =[line[1:] for line in evaluations]
# get averge of each subset of evaluation :
eva_1 =[sum(line)/len(line) for line in eva_1]
eva_2 =[line[0] for line in evaluations]

# find the k with lowest value of error:
hyper = eva_2[eva_1.index(min(eva_1))]

#scaled_full = []
#for key, value in scaled_data.iteritems():
#    temp = value
#    scaled_full.append(temp)


#get final description from train program based on final K then test it to get results:
description_final = train(dim, hyper, scaled_full) 
testIt(dim, hyper, description_final, "final")
