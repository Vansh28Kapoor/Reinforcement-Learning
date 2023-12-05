import argparse
import numpy as np
#no. of balls remaining is b-i
#no. of runs remaining is r-j
def recur(d2_shape,i,j,b,r,q):
    x=np.zeros(d2_shape,dtype=float)
    x[-2]+=q
    if((b-i-1) % 6!=0):
        x+=(1-q)*recur(d2_shape,i+1,j,b,r,q)*0.5
        if(j!=r-1):
            x[(i+1)*r+j+1]+=0.5*(1-q)
        else:
            x[-1]+=0.5*(1-q)
    elif(i==b-1):
        if(j==r-1):
            x[-1]+=0.5*(1-q)
            x[-2]+=0.5*(1-q)
        else:
            x[-2]+=1-q
    else:
        if(j!=r-1):
            x+=(1-q)*recur(d2_shape,i+1,j+1,b,r,q)*0.5
        else:
            x[-1]+=(1-q)*0.5
        x[(i+1)*r+j]+=(1-q)*0.5
    return x
parser=argparse.ArgumentParser()
parser.add_argument('--states',type=str,required=True,help="Invalid Path")
parser.add_argument('--parameters',type=str,required=True,help="Invalid Path")
parser.add_argument('--q',type=float,required=True,help="Invalid value")
args=parser.parse_args()
dic={}
q=args.q
with open(str(args.parameters),'r') as reading:
    read=reading.readlines()
    for i in range(1,len(read)):
        lines=read[i].strip()
        splt=lines.split(' ')
        lst=[]
        for j in range(1,len(splt)):
            lst.append(float(splt[j]))
        dic[i-1]=lst    
with open(str(args.states),'r') as reading:
    read=reading.readlines()
    line=read[0].strip()
    b=int(line[0:2])
    r=int(line[2:])
    T=np.zeros((b*r+2,b*r+2,5),dtype=float)
    R=T.copy()
for k in range(5):
    l=dic[k][0]
    m0=dic[k][1]
    m1=dic[k][2]
    m2=dic[k][3]
    m3=dic[k][4]
    m4=dic[k][5]
    m6=dic[k][6]
    #no. of balls remaining is b-i
    #no. of runs remaining is r-j
    for i in range(b):
        for j in range(r):
            T[i*r+j,-2,k]+=l
            if((b-i-1)%6!=0):
                T[i*r+j,(i+1)*r+j,k]+=m0
                if(j<r-2):
                    T[i*r+j,(i+1)*r+j+2,k]+=m2
                else:
                    T[i*r+j,-1,k]+=m2
                if(j<r-4):
                    T[i*r+j,(i+1)*r+j+4,k]+=m4
                else:
                    T[i*r+j,-1,k]+=m4
                if(j<r-6):
                    T[i*r+j,(i+1)*r+j+6,k]+=m6
                else:
                    T[i*r+j,-1,k]+=m6
                if(j<r-3):
                    T[i*r+j,:,k]+=m3*recur(T.shape[0],i+1,j+3,b,r,q)
                else:
                    T[i*r+j,-1,k]+=m3
                if(j<r-1):
                    T[i*r+j,:,k]+=m1*recur(T.shape[0],i+1,j+1,b,r,q)
                else:
                    T[i*r+j,-1,k]+=m1
            elif(i==b-1):
                if(j>=r-1):
                    T[i*r+j,-1,k]+=m1
                if(j>=r-2):
                    T[i*r+j,-1,k]+=m2
                if(j>=r-3):
                    T[i*r+j,-1,k]+=m3
                if(j>=r-4):
                    T[i*r+j,-1,k]+=m4
                if(j>=r-6):
                    T[i*r+j,-1,k]+=m6
                sum=np.sum(T[i*r+j,:,k])
                T[i*r+j,-2,k]+=1-sum
            else:
                T[i*r+j,:,k]+=m0*recur(T.shape[0],i+1,j,b,r,q)
                if(j<r-2):
                    T[i*r+j,:,k]+=m2*recur(T.shape[0],i+1,j+2,b,r,q)
                else:
                    T[i*r+j,-1,k]+=m2
                if(j<r-4):
                    T[i*r+j,:,k]+=m4*recur(T.shape[0],i+1,j+4,b,r,q)
                else:
                    T[i*r+j,-1,k]+=m4
                if(j<r-6):
                    T[i*r+j,:,k]+=m6*recur(T.shape[0],i+1,j+6,b,r,q)
                else:
                    T[i*r+j,-1,k]+=m6
                if(j<r-3):
                    T[i*r+j,(i+1)*r+j+3,k]+=m3
                else:
                    T[i*r+j,-1,k]+=m3
                if(j<r-1):
                    T[i*r+j,(i+1)*r+j+1,k]+=m1
                else:
                    T[i*r+j,-1,k]+=m1
T[-1,-1]=1
T[-2,-2]=1
R[:-1,-1]=1
R[-1:-1]=0
R[:,-2]=0
# ones=np.ones(T.shape[0])
# for i in range(T.shape[-1]):
#     print(T[0,:,i])
print('numStates '+str(T.shape[0]))
print('numActions ' + str(T.shape[-1]))
print('end '+ str(T.shape[0]-1) +" " +str(T.shape[0]-2))
for i in range(T.shape[0]):
    for j in range(T.shape[1]):
        for k in range(T.shape[2]):
            if(not np.allclose(T[i,j,k],0, rtol=1e-12)):
                print('transition '+ str(i) + ' '+str(k) +' '+ str(j)+ ' '+str(R[i,j,k])+' ' +str(T[i,j,k]))
print('mdptype '+  'episodic')
print('discount 1')


            
                







