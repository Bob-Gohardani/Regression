import math
import os
import sys
import re

sign = sys.argv[1]

def first():
    # program -a file1.txt [file2.txt ...] > data.txt
    ran = 0
    dummy = 0
    with open(sys.argv[2], 'r') as f:
        for line in f:
            if dummy == 0:
                l = [float(x) for x in line.replace('\n', '').replace('\r', '').strip().split(' ')]
                ran = len(l)

    dct = {}
    for i in range(ran):
        dct[i] = []

    dummy = 0
    for file in sys.argv:
        if dummy == 0 or dummy == 1 or dummy == len(sys.argv)-1:
            dummy += 1
            continue
        if dummy == 3:
            file = file.replace('[','')
        dummy += 1
        with open(file, 'r') as f:
            for line in f:
                if line != '\n' and line != '\n\r':
                    l = [float(x) for x in line.replace('\n', '').replace('\r', '').strip().split(' ')]
                    for i in range(ran):
                        dct[i].append(l[i])


    for key in dct:
        high = max(dct[key])
        low = min(dct[key])
        print (str(low) + " " + str(high))

def second():
    #   program -s data.txt < in.txt > out.txt
    dct = {}
    with open(sys.argv[2], 'r') as f:
        b=0
        for line in f:
            if line != '\n':
                dct[b] = [float(x) for x in line.replace('\n', '').replace('\r', '').strip().split(' ')]
                b+=1

    for line in sys.stdin:
        string = ""
        if line != '\n' and line != '\n\r':
            l = [float(x) for x in line.replace('\n', '').replace('\r', '').strip().split(' ')]
            for i in range(len(l)):
                y = (2 * ((l[i] - dct[i][0]) / (dct[i][1] - dct[i][0]))) -1
                string += str(y) + " "
            print (string)

def third():
    #program -u data.txt < in.txt > out.txt
    dct = {}
    with open(sys.argv[2], 'r') as f:
        b=0
        for line in f:
            if line != '\n':
                dct[b] = [float(x) for x in line.replace('\n', '').replace('\r', '').strip().split(' ')]
                b+=1
    for line in sys.stdin:
        string = ""
        if line != '\n' and line != '\n\r':
            l = [float(x) for x in line.replace('\n', '').replace('\r', '').strip().split(' ')]
            for i in range(len(l)):
                max = dct[i][1]
                min = dct[i][0]
                y = l[i]
                x = (((y + 1) / 2) * (max - min)) + min
                string += str(x) + " "
            print (string)


if sign == "-a":
    first()
if sign == "-s":
    second()
if sign == "-u":
    third()
