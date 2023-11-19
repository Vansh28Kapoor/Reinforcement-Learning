import os
import sys
import random 
import json
import math
import utils
import time
import config
import numpy
random.seed(73)

def angle(ball,holes,hole_radius):
    t=[]
    for i in holes:
        d=numpy.sqrt((ball[0]-i[0])**2 + (ball[1]-i[1])**2 )
        alpha=numpy.arcsin(hole_radius/d)
        theta=numpy.arctan( (ball[0]-i[0]+1e-12)/(ball[1]-i[1] +1e-12) )
        if(ball[1]<i[1]):
            theta=theta-math.pi
        t.append([theta-alpha,theta+alpha])
    return t


def tangent(striker,ball,radius):
    d=numpy.sqrt((striker[0]-ball[0])**2 + (striker[1]-ball[1])**2 )
    alpha=numpy.arcsin(2*radius/d)
    #remove

    theta=numpy.arctan((striker[0]-ball[0]+1e-12)/(striker[1]-ball[1]+1e-12))
    if(striker[1]<ball[1]):
        theta=theta-math.pi
    angles=[theta+alpha-(math.pi/2),theta-alpha+(math.pi/2)] #Will have to deal with [-1.3,-0.7] later

    return(angles)


def overlap(ang1,ang2): #send striker angles in ang1
    section1=[]
    section2=[] 
    a1=ang1
    len1=0
    len2=0
    for i in range(2):
        ang1[i]=ang1[i]%(2*math.pi)
        ang2[i]=ang2[i]%(2*math.pi)

    if ang1[0]<ang1[1]:
        s11=ang1
        s12=[]
    else:
        s11=[ang1[0],2*math.pi]
        s12=[0,ang1[1]]
    if ang2[0]<ang2[1]:
        s21=ang2
        s22=[]
    else:
        s21=[ang2[0],2*math.pi]
        s22=[0,ang2[1]]
    
    if(len(s12)==0 and len(s22)==0):
        if (s11[0]< s21[1] and s21[0]<s11[1]):
            section1= [max(s11[0],s21[0]),min(s11[1],s21[1])]

    elif(len(s12)==0 and len(s22)==2): 
        if (s11[0]< s21[1] and s21[0]<s11[1]):
            section1= [max(s11[0],s21[0]),min(s11[1],s21[1])]

        elif (s11[0]< s22[1] and s22[0]<s11[1]):
            section1= [max(s11[0],s22[0]),min(s11[1],s22[1])]
    
    elif(len(s12)==2 and len(s22)==0):

        if (s11[0]< s21[1] and s21[0]<s11[1]):
            section1= [max(s11[0],s21[0]),min(s11[1],s21[1])]

        elif (s12[0]< s21[1] and s21[0]<s12[1]):
            section1= [max(s12[0],s21[0]),min(s12[1],s21[1])]

    else:

        section1= [max(s11[0],s21[0]),2*math.pi]
        
        section2= [0,min(s22[1],s12[1])]
    
    if len(section1)!=0 :
        len1=section1[1]-section1[0]
    if len(section2)!=0:
        len2=section2[1]-section2[0]
    
    ovrlp=len1+len2

    if ovrlp==0:
        return 0,(a1[0]+a1[1])/2

    elif len2==0:
        return ovrlp,(section1[1]+section1[0])/2
    else:
        return ovrlp,(section1[0]+section2[1]+2*math.pi)/2
    
# def overlap(ang1,ang2): #send striker angles in ang1
#     section1=[]
#     section2=[] 
#     a1=numpy.array(ang1)
#     len1=0
#     len2=0
#     for i in range(2):
#         ang1[i]=ang1[i]%(2*math.pi)
#         ang2[i]=ang2[i]%(2*math.pi)

#     if ang1[0]<ang1[1]:
#         s11=ang1
#         s12=[]
#     else:
#         s11=[ang1[0],2*math.pi]
#         s12=[0,ang1[1]]
#     if ang2[0]<ang2[1]:
#         s21=ang2
#         s22=[]
#     else:
#         s21=[ang2[0],2*math.pi]
#         s22=[0,ang2[1]]
    
#     if(len(s12)==0 and len(s22)==0):
#         if (s11[0]< s21[1] and s21[0]<s11[1]):
#             section1= [max(s11[0],s21[0]),min(s11[1],s21[1])]

#     elif(len(s12)==0 and len(s22)==2): 
#         if (s11[0]< s21[1] and s21[0]<s11[1]):
#             section1= [max(s11[0],s21[0]),min(s11[1],s21[1])]

#         elif (s11[0]< s22[1] and s22[0]<s11[1]):
#             section1= [max(s11[0],s22[0]),min(s11[1],s22[1])]
    
#     elif(len(s12)==2 and len(s22)==0):

#         if (s11[0]< s21[1] and s21[0]<s11[1]):
#             section1= [max(s11[0],s21[0]),min(s11[1],s21[1])]

#         elif (s12[0]< s21[1] and s21[0]<s12[1]):
#             section1= [max(s12[0],s21[0]),min(s12[1],s21[1])]

#     else:

#         section1= [max(s11[0],s21[0]),2*math.pi]
        
#         section2= [0,min(s22[1],s12[1])]
    
#     if len(section1)!=0 :
#         len1=section1[1]-section1[0]
#     if len(section2)!=0:
#         len2=section2[1]-section2[0]
    
#     ovrlp=len1+len2

#     if ovrlp==0:
#         return 0,a1

#     elif len2==0:
#         return ovrlp,numpy.array(section1)
#     else:
#         return ovrlp,numpy.array([section1[0],section2[1]+2*math.pi])

    


    


def convert(angle):
    angle=angle%(2*math.pi)
    if angle<= math.pi:
        return angle
    else:
        return angle-2*math.pi


def control(theta,str,ball,radius):
    new=[]
    new.append(ball[0]+2*radius*math.sin(theta))
    new.append(ball[1]+2*radius*math.cos(theta))
    ang=numpy.arctan( (str[0]-new[0]+1e-12)/(str[1]-new[1]+1e-12 ) )
    if(str[1]<new[1]):
        ang=ang-math.pi
    return ang

def dist(striker,ball):
    return numpy.sqrt((ball[0]-striker[0])**2 + (ball[1]-striker[1])**2 )

class Agent:
    def __init__(self, table_config) -> None:
        self.table_config = table_config
        self.prev_action = None
        self.curr_iter = 0
        self.state_dict = {}
        self.holes =[]
        self.ns = utils.NextState()


    def set_holes(self, holes_x, holes_y, radius):
        for x in holes_x:
            for y in holes_y:
                self.holes.append((x[0], y[0]))
        self.ball_radius = radius


    # def best(self,state):


    def action(self, ball_pos=None):

        dic={}
        num=len(ball_pos)
        ball_radius=config.ball_radius
        hole_radius=config.hole_radius

        striker=ball_pos['white']

        max_overlap={}
        hole=[]
        for i in ball_pos.keys():
            if(i != "white" and i != 0):
                ball=ball_pos[i]
                possible_angles=tangent(striker,ball,ball_radius)

                hole_angles=angle(ball,self.holes,hole_radius)
                ovrlp=[]
                for j in hole_angles:
                    ovrlp.append(overlap(j,possible_angles)[0])

                arg=numpy.argmax(ovrlp)
                hole.append([ovrlp[arg],arg,i])

        hole=numpy.array(hole)
        indices=numpy.argsort(-hole[:,0])
        new=hole[indices]
        select=[]
        maxim=min(3,hole.shape[0])
        if maxim==3:
            c1=0.2
            c2=8
            c3=0.05
            k=3
        if maxim==2:
            
            # c1=0.2
            # c2=8
            # c3=0.05
            # k=3
            c1=0.18 #or c1=0.16
            c2=8
            c3=0.05
            k=3



        if maxim==1:
            print
            # c1=0.2
            # c2=6
            # c3=0.08 #needs 0.08*4+0.2 (arg=3), case =41 && 0.05*4+0.16
            # k=2
            c1=0.2
            c2=8
            c3=0.05 #needs 0.08*4+0.2 (arg=3), case =41 && 0.05*4+0.16
            k=2


                # remove below for nested without any
            bst_ball=ball_pos[new[0,2]] #hole[bst,2] is a key always
            bst_hole=self.holes[int(new[0,1])]
            possible_angles=tangent(striker,bst_ball,ball_radius) #actual
            
            # if(dist(striker,bst_ball)<ball_radius):
            #     print(dist(striker,bst_ball),ball_radius)
            d=(dist(bst_ball,striker)/115.34)*0.1+c1

            # d=(dist(bst_ball,striker)/115.34)*0.1+c1

            array=numpy.arange(0,c2)*c3+d
            hole_angles=angle(bst_ball,[bst_hole],hole_radius)[0]
            best_angle=control(overlap(possible_angles,hole_angles)[1],striker,bst_ball,ball_radius)
            #best_angle=(control(overlap(possible_angles,hole_angles)[1][0],striker,bst_ball,ball_radius)+control(overlap(possible_angles,hole_angles)[1][1],striker,bst_ball,ball_radius))/2
            best_angle=convert(best_angle)/math.pi
            l=[]

            for j in range(len(array)):
                sum=0
                for xyz in range(k):


                    r=numpy.random.randint(1,100)
                    next_state=self.ns.get_next_state(ball_pos, (best_angle, array[j]), r)
                    sum+=num-len(next_state)

                    if len(next_state)==3:

                        striker_1=next_state['white']
                        hole_1=[]
                        for ii in next_state.keys():
                            if(ii != "white" and ii != 0):
                                ball_1=next_state[ii]
                                possible_angles_1=tangent(striker_1,ball_1,ball_radius)

                                if(dist(striker_1,ball_1)<ball_radius):
                                    print(dist(striker_1,ball_1),ball_radius)

                                hole_angles_1=angle(ball_1,self.holes,hole_radius)
                                ovrlp_1=[]
                                for j_1 in hole_angles_1:
                                    ovrlp_1.append(overlap(j_1,possible_angles_1)[0])

                                arg_1=numpy.argmax(ovrlp_1)
                                hole_1.append([ovrlp_1[arg_1],arg_1,ii])

                        hole_1=numpy.array(hole_1)

                        bst_hole_1=self.holes[int(hole_1[0,1])]
                        possible_angles_1=tangent(striker_1,ball_1,ball_radius) #actual

                        d_1=(dist(ball_1,striker_1)/115.34)*0.1+c1

                        # d=(dist(bst_ball,striker)/115.34)*0.1+c1
                        array_1=numpy.arange(0,c2)*c3+d_1
                        hole_angles_1=angle(ball_1,[bst_hole_1],hole_radius)[0]
                        best_angle_1=control(overlap(possible_angles_1,hole_angles_1)[1],striker_1,ball_1,ball_radius)
                        #best_angle_1=(control(overlap(possible_angles_1,hole_angles_1)[1][0],striker_1,ball_1,ball_radius)+control(overlap(possible_angles_1,hole_angles_1)[1][1],striker_1,ball_1,ball_radius))/2
                        best_angle_1=convert(best_angle_1)/math.pi
                        l_1=[]


                        for jj in range(len(array_1)):
                            r=numpy.random.randint(1,100)
                            next_state2=self.ns.get_next_state(next_state, (best_angle_1, array_1[jj]), r)
                            sum+=(len(next_state)-len(next_state2))*0.25
                            if((len(next_state)-len(next_state2))==1):
                                break


                l.append(sum)
                if sum>(0.9*k):
                    l.extend([0]*(len(array)-1-j))   
                    break 
            l=numpy.array(l)
            force=[max(l),array[numpy.argmax(l)],best_angle,numpy.argmax(l)]
            select.append(force)
            select=numpy.array(select)
            bst=numpy.argmax(select[:,0],axis=0)
            print(select[bst,0],select[bst,-1])
            return (select[bst,2], select[bst,1])
        for i in range(maxim):

            bst_ball=ball_pos[new[i,2]] #hole[bst,2] is a key always
            bst_hole=self.holes[int(new[i,1])]
            possible_angles=tangent(striker,bst_ball,ball_radius) #actual

            d=(dist(bst_ball,striker)/115.34)*0.1+c1

            # d=(dist(bst_ball,striker)/115.34)*0.1+c1
            array=numpy.arange(0,c2)*c3+d
            hole_angles=angle(bst_ball,[bst_hole],hole_radius)[0]
            best_angle=control(overlap(possible_angles,hole_angles)[1],striker,bst_ball,ball_radius)
            
            #best_angle=(control(overlap(possible_angles,hole_angles)[1][0],striker,bst_ball,ball_radius)+control(overlap(possible_angles,hole_angles)[1][1],striker,bst_ball,ball_radius))/2
            best_angle=convert(best_angle)/math.pi
            l=[]
            for j in range(len(array)):
                sum=0
                for xyz in range(k):
                    r=numpy.random.randint(1,100)
                    next_state=self.ns.get_next_state(ball_pos, (best_angle, array[j]), r)
                    sum+=num-len(next_state)
                l.append(sum)
                if sum>(0.9*k):
                    l.extend([0]*(len(array)-1-j))   
                    break 
            l=numpy.array(l)
            force=[max(l),array[numpy.argmax(l)],best_angle,numpy.argmax(l)]
            if max(l)>(0.9*k):
                print(force[0],force[-1])
                return (force[2],force[1])
            select.append(force)
        select=numpy.array(select)
        
        bst=numpy.argmax(select[:,0],axis=0)
        print(select[bst,0],select[bst,-1])
        return (select[bst,2], select[bst,1])
