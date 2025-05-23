# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 16:21:00 2024

@author: alber
"""
import numpy as np
from scipy.linalg import hadamard, subspace_angles

import matplotlib.pyplot as plt
plt.close()
#ortogonalidade


x=np.array([1,1,0])

y=np.array([0,1,1])
x1=y-x

s=np.transpose(x)@y

s_xy=np.dot(x,y)
s_xx=np.dot(x,x)


#|X|=np.sqrt(np.dot(x)) or
#|X|=np.linalg.norm(x)
x=np.array([3*np.sqrt(3),0])
y=np.array([3*np.sqrt(3),3])

#xt*y=|x||y|cos(theta)
##cos(theta)=c.o/hip= 3/5
#C2=np.sqrt(np.dot(x,x))*np.sqrt(np.dot(y,y))*3/5
#ou
#cos(theta)=xT*y/( |x||y|)

costheta=np.dot(x,y)/(np.linalg.norm(x)*np.linalg.norm(y))
angulo=np.arccos(costheta)*180/np.pi
# print('--------------------------------')
# print('angulo:',angulo, 'graus')

Xo=0
Yo=0
plt.figure('vetores ',tight_layout=True)
plt.quiver(Xo,Yo,x[0],x[1], angles='xy', scale_units='xy', scale=1, color='r',width=1/300)
plt.text(x[0],x[1],' x',color='r')
plt.quiver(Xo,Yo,y[0],y[1], angles='xy', scale_units='xy', scale=1, color='b',width=1/300)
plt.text(y[0],y[1],' y',color='b')

k=x/8+y/8
plt.text(k[0],k[1],str(np.round(angulo)))


#plt.axis('equal')

plt.xlim([-2-np.linalg.norm(x), np.linalg.norm(x)+2])
plt.ylim([-2-np.linalg.norm(y), np.linalg.norm(y)+2])
plt.grid()

dx=np.linspace(-1.0*np.pi,np.pi,100)
f=np.sin(dx)
f2=np.sin(dx-np.pi/6)
g=np.cos(dx)
print('<f,g>=',np.round(np.dot(f,g)))
plt.figure('seno x cosseno ',tight_layout=True)
plt.plot(dx,f,'r',dx,g,'b')
plt.plot(dx,f2,'--r')

plt.grid()



    
    
    
