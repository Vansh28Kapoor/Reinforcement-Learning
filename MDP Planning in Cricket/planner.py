from email import policy
import random,argparse,sys,subprocess,os
import numpy as np
import pulp as p

def Belman_Optimality_Operator(V,T,R,alpha,ter):
    x=np.zeros((V.shape[0],T.shape[-1]))
    for i in range(T.shape[0]):
        if(i not in ter):
            x[i]=np.sum(T[i]*R[i],axis=0)+ alpha*T[i].T@ V
    v=np.max(x,axis=1)
    pol=np.argmax(x,axis=1)
    return v,pol
def Belman_Operator(V,T,R,alpha,pol):
    v=np.zeros(V.shape,dtype=float)
    for i in range(T.shape[0]):
        v[i]=np.sum(T[i,:,pol[i]]*R[i,:,pol[i]] + alpha*T[i,:,pol[i]]*V)
    return v

def Value_iteration(T,R,alpha,ter=[]):
    V0=np.zeros(shape=T.shape[0])
    B=Belman_Optimality_Operator(V0,T,R,alpha,ter)
    V1=B[0]
    policy=B[1]
    while(not np.allclose(V0,V1, rtol=1e-12)):
        V0=V1.copy()
        B=Belman_Optimality_Operator(V0,T,R,alpha,ter)
        V1=B[0]
        policy=B[1]
    return V1,policy

# def Pol_eval(pol,T,R,alpha,ter):
#     pol1=np.delete(pol,ter)
#     T2= np.delete(T,ter, axis=1)
#     T1=np.delete(T2,ter,axis=0)
#     R2= np.delete(R,ter, axis=1)
#     R1=np.delete(R2,ter,axis=0)
#     s=np.zeros((T1.shape[0],T1.shape[0]))
#     for i in range(T1.shape[0]):
#         s[i]=alpha*T1[i,:,pol1[i]]
#     b=np.zeros(T1.shape[0])
#     for i in range(T1.shape[0]):
#         b[i]=np.sum(T1[i,:,pol[i]]*R1[i,:,pol[i]])
#     I = np.identity(T1.shape[0])
#     A=I-s
#     x = np.linalg.solve(A, b)
#     return np.insert(x,ter,0.0)
def Pol_eval(pol,T,R,alpha,ter=[]):
    V0=np.zeros(shape=T.shape[0])
    B=Belman_Operator(V0,T,R,alpha,pol)
    V1=B
    while(not np.allclose(V0,V1, rtol=1e-12)):
        V0=V1.copy()
        B=Belman_Operator(V0,T,R,alpha,pol)
        V1=B
    return V1   


def HPI(T,R,alpha,ter):
    pol=np.zeros(T.shape[0],dtype=int)
    k=0
    while(True):
        dic={}
        V=Pol_eval(pol,T,R,alpha,ter)
        for i in range(T.shape[0]):
            for j in range(T.shape[-1]):
                if(j!=pol[i] and (i not in ter)):
                    Q=np.sum(T[i,:,j]*R[i,:,j]+ alpha*T[i,:,j]*V)
                    if(Q>V[i]):
                        dic[i]=j
                        break
        if(len(dic)==0):
            break
        else:
            for i in dic.keys():
                pol[i]=dic[i]
    return Pol_eval(pol,T,R,alpha,ter),pol
def LP(T,R,alpha,ter):
    #Refered to Geeks for Geeks
    Lp=p.LpProblem('Linear_problem',p.LpMaximize)
    V=[]
    for i in range(T.shape[0]):
        string='V'+str(i)
        if i not in ter:
            V.append(p.LpVariable(string))
        else:
            V.append(p.LpVariable(string,lowBound=0,upBound=0))
    Lp+= -1*sum(V)
    for i in range(T.shape[0]):
        if i not in ter:
            cond=np.sum(T[i]*R[i],axis=0) + alpha* T[i].T @ V
            for j in range(T.shape[-1]):
                Lp+= V[i]>= cond[j]
    sol=Lp.solve(p.PULP_CBC_CMD(msg=0))
    soln=[]
    for i in V:
        soln.append(p.value(i))
    pol=np.zeros(T.shape[0],dtype=int)
    for i in range(T.shape[0]):
        pol[i]=np.argmax(np.sum(T[i]*R[i],axis=0)+ alpha*T[i].T @ soln)
    return soln,pol
random.seed(0)
parser=argparse.ArgumentParser()
parser.add_argument('--mdp',type=str,required=True,help="Invalid path")
parser.add_argument('--algorithm',type=str,default='lp',required=False,help="mention a valid algorithm")
parser.add_argument('--policy',type=str,required=False,default=None,help="mention a valid file name")
args=parser.parse_args()
with open(str(args.mdp),'r') as reading:
    read=reading.readlines()
    lst=[]
    self=[]
    for i in range(3):
        splt=read[i].replace('\n','').split(' ')
        if i!=2:
            lst.append(int(splt[-1]))
        else:
            if int(splt[-1])!= -1:
                for j in range(1,len(splt)):
                    self.append(int(splt[j]))
    i+=1
    T=np.zeros((lst[0],lst[0],lst[-1]),dtype=float)
    R=np.zeros((lst[0],lst[0],lst[-1]),dtype=float)
    while(i<len(read)):
        if 'transition' in str(read[i]):
            splt=read[i].replace('\n','').split(' ')
            s1=int(splt[1])
            a=int(splt[2])
            s2=int(splt[3])
            r=float(splt[4])
            prob=float(splt[5])
            T[s1,s2,a]=prob
            R[s1,s2,a]=r
        elif 'discount' in str(read[i]):
           splt=read[i].replace('\n','').split(' ')
           alpha=float(splt[-1])
        i+=1
    for i in self:
        T[i,i]=1
        R[i,i]=0
pol=[]
if args.policy != None:
    with open(args.policy,'r') as reading:
        read=reading.readlines()
        for i in read:
            i=i.strip()
            if len(i)!=0:
                pol.append(int(i))
    eval=Pol_eval(pol,T,R,alpha,self)
    for i in range(len(eval)):
        print(str(eval[i]) + '\t' + str(pol[i]))
elif args.algorithm=='vi':
    eval=Value_iteration(T,R,alpha,self)
    for i in range(len(eval[0])):
        print(str(eval[0][i]) + '\t' + str(eval[1][i]))
elif args.algorithm=='hpi':
    eval=HPI(T,R,alpha,self)
    for i in range(len(eval[0])):
        print(str(eval[0][i]) + "\t" + str(eval[1][i]))
elif args.algorithm=='lp':  
    eval=LP(T,R,alpha,self)
    for i in range(len(eval[0])):
        print(str(eval[0][i]) + '\t' + str(eval[1][i]))

