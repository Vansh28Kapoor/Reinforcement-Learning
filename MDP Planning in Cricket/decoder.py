import argparse
import numpy as np
parser=argparse.ArgumentParser()
parser.add_argument('--states',type=str,required=True,help="Invalid Path")
parser.add_argument('--value-policy',type=str,help="Invalid Path")
args=parser.parse_args()
dic={}
replacements={'3':'4','4':'6'}
with open(str(args.states),'r') as reading:
    read=reading.readlines()
    line=read[0].strip()
    b=int(float(line[0:2]))
    r=int(float(line[2:]))
with open(str(args.value_policy),'r') as reading:
    read=reading.readlines()
    index=0
    for i in range(b,0,-1):
        for j in range(r,0,-1):
            lines=read[index].strip()
            splt=lines.split('\t')
            value=splt[0].strip()
            action=str(int(splt[1]))
            for key in replacements.keys():
                if key in action:
                    action=replacements[key]
                    break
            print(str(i).zfill(2)+str(j).zfill(2)+" "+ str(action)+ " "+value)
            index+=1 