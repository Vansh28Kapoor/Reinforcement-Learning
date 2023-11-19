#decoder
import numpy as np
import argparse 
parser=argparse.ArgumentParser()
parser.add_argument('--value-policy',type=str,required=True)
parser.add_argument('--opponent',type=str,required=True)
args=parser.parse_args()
states=[]
with open(args.opponent,"r") as reading:
    read=reading.readlines()
    for i in range(1,len(read)):
        splt=read[i].strip().split(' ')
        state=str(splt[0])
        states.append(state)
j=0
with open(args.value_policy,"r") as reading:
    read=reading.readlines()
    for lines in read[:-2]:
        var=str(lines.strip())
        splt=var.split()
        print(str(states[j]) + ' ' + str(int(splt[-1])) + ' ' + str(float(splt[0])) )
        j+=1



        