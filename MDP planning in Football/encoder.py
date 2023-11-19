import random,argparse,sys,subprocess,os
import numpy as np
def dist(r1,r2):
    if(r1%4==0):
        x1 = 4
    else:
        x1=r1 %4
    if(r2 % 4==0):
        x2=4
    else:
        x2=r2 %4
    y1=np.ceil(r1/4)
    y2=np.ceil(r2/4)
    return np.abs(x1-x2),np.abs(y1-y2)
def pos(i):
    lst=[]
    if(i%4==1):
        lst.append(-1)
    else:
        lst.append(i-1)
    if(i%4==0):
        lst.append(-1)
    else:
        lst.append(i+1)
    if(i<5):
        lst.append(-1)
    else:
        lst.append(i-4)
    if(i>12):
        lst.append(-1)
    else:
        lst.append(i+4)
    return lst
    
def prob_pass(striker,receiver,q,r):
    x1,y1=dist(r,striker)
    x2,y2=dist(r,receiver)
    x3,y3=dist(receiver,striker)
    condition1=np.abs(np.sqrt(x1**2+y1**2)+np.sqrt(x2**2+y2**2)-np.sqrt(x3**2+y3**2))<1e-8
    condition2= (x3==0 or y3==0 or x3==y3) 
    if(condition1 and condition2):
        return (q-0.1*np.max([x3,y3]))/2
    else:
        return q-0.1*np.max([x3,y3])
def shoot(striker,q,r):
    x1,y1=dist(4,striker)
    if(r==8 or r==12):
        return (q-0.2*x1)/2
    else:
        return (q-0.2*x1)
# python encoder.py --opponent data/football/test-1.txt --p 0.1 --q 0.7 
#B1, B2, R, ball
#state P(L) P(R) P(U) P(D)
dic={}
states=[]
parser=argparse.ArgumentParser()
parser.add_argument('--opponent',type=str,required=True)
parser.add_argument('--p',type=float,required=True)
parser.add_argument('--q',type=float,required=True)
args=parser.parse_args()
p=args.p
q=args.q
with open(str(args.opponent),'r') as reading:
    read=reading.readlines()
    for i in range(1,len(read)):
        splt=read[i].strip().split(' ')
        state=str(splt[0])
        states.append(state)
        prob=np.float16(splt[1:])
        dic[state]=prob
j=0
T=np.zeros((len(states)+2,10,len(states)+2))
Reward=np.zeros((len(states)+2,10,len(states)+2))
Reward[:-2,:,-1]=1

# for i in states[0:9]:
#     B=list([int(i[0:2]),int(i[2:4])]) #list of positions of B1, B2 in int
#     prob=dic[i]
#     R=int(i[4:6])
#     index=i[-1]
#     b=int(i[-1])-1 #index of B with ball
#     nb=int(i[-1])%2 # index of B without ball
#     ball_i=B[b]
#     ball_f=pos(B[b])
#     opp_i=R
#     opp_f=pos(R)
#     noball_f=pos(B[nb])
#     print(B,R,b,nb)


for i in states:
    B=list([int(i[0:2]),int(i[2:4])]) #list of positions of B1, B2 in int
    prob=dic[i]
    R=int(i[4:6])
    index=i[-1]
    b=int(i[-1])-1 #index of B with ball
    nb=int(i[-1])%2 # index of B without ball
    ball_i=B[b]
    ball_f=pos(B[b])
    opp_i=R
    opp_f=pos(R)
    noball_f=pos(B[nb])
    swap=[]
    same=[]
    for x in range(4): #ball
        for y in range(4): #opponent
            if(ball_f[x]==opp_f[y]):
               same.append([x,y]) #player_action, opponent_action
            elif(ball_f[x]==opp_i and opp_f[y]==ball_i):
               swap.append([x,y])
    for x in range(4):
        if(noball_f[x]==-1):
            T[j,4*nb+x,-2]=1
        else:
            for y in range(4):
                if(opp_f[y]!=-1):
                    B_copy=B.copy()
                    B_copy[nb]=noball_f[x]
                    s=str(B_copy[0]).zfill(2)+str(B_copy[1]).zfill(2)+str(opp_f[y]).zfill(2)+str(b+1)
                    final_state=states.index(s)
                    T[j,nb*4+x,final_state]+=(1-p)*prob[y]
                    T[j,nb*4+x,-2]+=p*prob[y]

        if(ball_f[x]==-1):
                T[j,4*b+x,-2]=1
        else:
            for y in range(4):
                if(opp_f[y]!=-1):
                    B_copy=B.copy()
                    B_copy[b]=ball_f[x]
                    s=str(B_copy[0]).zfill(2)+str(B_copy[1]).zfill(2)+str(opp_f[y]).zfill(2)+str(b+1)
                    final_state=states.index(s)
                    if (([x,y] not in swap) and ([x,y] not in same)):
                        T[j,4*b+x,final_state]+=(1-2*p)*prob[y]
                        T[j,4*b+x,-2]+=2*p*prob[y]
                    else:
                        T[j,4*b+x,final_state]+=(0.5-p)*prob[y]
                        T[j,4*b+x,-2]+=(0.5+p)*prob[y]

    for y in range(4):
        if(opp_f[y]!=-1):
            B_copy=B.copy()
            prob_p=prob_pass(B_copy[b],B_copy[nb],q,opp_f[y])
            s=str(B_copy[0]).zfill(2)+str(B_copy[1]).zfill(2)+str(opp_f[y]).zfill(2)+str(nb+1)
            final_state=states.index(s)
            T[j,8,final_state]+=prob_p*prob[y]
            T[j,8,-2]+=(1-prob_p)*prob[y]
            
            B_copy=B.copy()
            prob_shoot=shoot(B_copy[b],q,opp_f[y])
            T[j,9,-1]+=prob_shoot*prob[y]
            T[j,9,-2]+=(1-prob_shoot)*prob[y]
    j+=1 
print('numStates '+str(T.shape[0]))
print('numActions ' + str(T.shape[-2]))
print('end '+ str(T.shape[0]-1) +" " +str(T.shape[0]-2))
for i in range(T.shape[0]):
    for j in range(T.shape[1]):
        for k in range(T.shape[2]):
            if(T[i,j,k]!=0):
                print('transition '+ str(i) + ' '+str(j) +' '+ str(k)+ ' '+str(Reward[i,j,k])+' ' +str(T[i,j,k]))
print('mdptype '+  'episodic')
print('discount 1')

