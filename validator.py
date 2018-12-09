import sys
import random
import os
import math

def main():

    if sys.argv[1] == "-g":
        split()

    elif sys.argv[1] == "-e":
        validation()

    elif sys.argv[1] == "-v":
        evaluation()

def split():
    setfile = sys.argv[2]
    setj=[]
    with open(setfile, "r") as set:
        for line in set:
            if line != '\n':
                l = [float(x) for x in line.replace('\n', '').replace('\r', '').strip().split(' ')]
                setj.append(l)

    outdir = sys.argv[4]
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    number_of_split= 2
    set_length = len(setj)

    #random subsampling

    totalsubset= int(number_of_split)*2
    len_of_each= set_length/totalsubset
    for i in range (0, number_of_split):
        op= outdir+"/training_set"+str(i+1)+".txt"
        f = open(op,"w")
        for j in range(0,int(len_of_each)):
            #select random index
            string = ""
            x=random.randint(0,len(setj)-1)
            for a in range (len(setj[0])):
                string += str(setj[x][a]) + " "
            f.write(string)
            f.write("\n")
            setj.remove(setj[x][:])

    for i in range(0, number_of_split):
        op = outdir + "/validation_set" + str(i + 1) +".txt"
        f = open(op, "w")
        for j in range(0, int(len_of_each)):
            # select random index
            string = ""
            x = random.randint(0, len(setj) - 1)
            for a in range (len(setj[0])):
                string += str(setj[x][a]) + " "
            f.write(string)
            f.write("\n")
            setj.remove(setj[x][:])

    print (number_of_split)

def validation():
    validation_file= sys.argv[2]

    val_array = []
    out_array = []

    with open(validation_file,"r") as val:
        for line in val:
            if line != '\n':
                l = [float (x) for x in line.replace('\n', '').replace('\r', '').strip().split()]
                val_array.append(l)

    for line in sys.stdin:
        out_array.append(float(line))

    q = 0
    sum =0
    length = len(val_array)
    for i in range(length):
        sum += pow((val_array[i][len(val_array[0])-1] - out_array[i]), 2)

    q = math.sqrt(sum)/(2*length)

    print(q)

def evaluation():
    inp_file = sys.argv[2]
    inp_arr = []

    with open(inp_file,"r") as val:
        for line in val:
            if line != '\n':
                l = [float (x) for x in line.replace('\n', '').replace('\r', '').strip().split()]
                inp_arr.append(l)

    avg = []
    m_split= len(inp_arr[0])
    for i in range(len(inp_arr)):
        sum_avg = 0
        for j in range (1, m_split):
            sum_avg += inp_arr[i][j]
        avg.append(float(sum_avg))

    #find min

    print (int(inp_arr[avg.index(min(avg))][0]))

main()
