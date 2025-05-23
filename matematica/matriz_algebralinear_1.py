# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 15:32:09 2024

@author: alberto akel
"""

import numpy as np
#método de gauss steven leon 4th ed. 
#cap1
#ex2
A=np.array([[-3,1],[2,5],[4,2]])
   
B=2.1*A            
C=A-B

X=np.array([[2],[4]])

S=A@X #multiplicção matrizes
#print(S)

#ex4

A=np.array([[-2,1,3],[4,1,6]])
B=np.array([[3,-2],[2,4],[1,-3]])

S1=A@B
S2=B@A

C=np.zeros((3,3))
D=np.ones((3,3))
D3=np.ones((3,2,2)) #cubo de dados (3x[2x2])
D3[0]=np.ones((2,2))*0
D3[2]=np.ones((2,2))*2
D4=D3.reshape(3,4)


E=np.arange(16)+1
E3=E.reshape(4,2,2)
E4=E.reshape(4,4)

# print(E4)
# dg=np.diag(E4)
# print('----')


F=np.diag(np.diag(E4))
F1=np.diag(np.diag(E4))
F2=np.diag(np.diag(E4,2),2)

# print(F1)
# print('----')
# print(F2)


G=np.transpose(E4)
inv=np.linalg.inv(E4) ##matriz inversa
I=np.identity(4)

print
"""
#ex8
  x1 + 4x2 +3x3 =+12
- x1 - 2x2 +0   =-12
 2x1 + 2x2 +3x3 =+8
 to solve
 x=A^-1*b
"""
A=np.array([[1,4,3],[-1,-2,0],[2,2,3]])
b=np.array([[12],[-12],[8]])
           

A=np.array([[1,3,1],[2,1,1],[-2,2,-1]])
b=np.array([[1],[5],[-8]])


A=np.array([[1,10],[1,12]])
b=np.array([[236],[281]])
# Ainv=np.linalg.inv(A)
# x=Ainv@b

x= np.linalg.solve(A, b)
print(x)




