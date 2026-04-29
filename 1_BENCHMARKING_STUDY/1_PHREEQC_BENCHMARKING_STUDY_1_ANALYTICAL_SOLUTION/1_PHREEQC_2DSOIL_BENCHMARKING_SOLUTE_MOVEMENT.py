# NOTES: PLOTTING : https://stackoverflow.com/questions/77212040/get-seperate-plots-and-one-accumulated-in-matplotlib-pyplot


import numpy as NP
import pandas as PD
import matplotlib.pyplot as PLT
import math
from scipy import special

T_LIST = [0,1,2,3,4]

FIGURE,AXES = PLT.subplots()

# CALCULATION OF ANALYTICAL SOLUTION
U_DARCY = 25.648 # 45.7 #DARCY FLOW VELOCITY cm/day
THETA_SATURATED = 0.2817 # SATURATED MOISTURE CONTENT = POROSITY
U_PORE = U_DARCY/THETA_SATURATED # PORE VELOCITY
X_ARRAY = NP.linspace(749.999,0.001,num = 50) #DISTANCE FROM INLET in cm
DX = DX = 75*U_PORE #12.8*U_PORE #DISPERSITIVITY in cm
C_INJECTED = 1.0 # CONCENTRATION OF INJECTED LIQUID
C_X_T = 0 # CONCENTRATION AT A GIVEN POINT (X) AT A GIVEN TIME (T)
COLUMN_LENGTH = 750 # LENGTH OF COLUMN (in cm)

for TIME in T_LIST:

    T = TIME #TIME ELAPSED SINCE BEGINNNING OF INJECTION IN day

    def ANALYTICAL_SOLUTION_FUNCTION(X_ARRAY):
        # CALCULATES ANALYTICAL SOLUTION 
        C_ANALYTICAL = [] # CRETATE AN EMPTY LIST AND THE VALUES ARE APPENDED TO IT AFTER CALCULATION
    #print(EPSILON)
    #print(ETA)
        print('Time=',TIME)
        for X in X_ARRAY:
            X_LOCAL = COLUMN_LENGTH-X
            EPSILON = U_PORE*T/X_LOCAL
            ETA = DX/(U_PORE*X_LOCAL)
            FIRST_TERM = special.erfc((1-EPSILON)/(2*(math.sqrt(EPSILON*ETA))))
            SECOND_TERM = math.exp(1/ETA)*(special.erfc((1+EPSILON)/(2*(math.sqrt(EPSILON*ETA)))))
            C_ANALYTICAL_X_T = 0.5*C_INJECTED*(FIRST_TERM+SECOND_TERM)
            C_ANALYTICAL.append(C_ANALYTICAL_X_T)
            print(X,C_ANALYTICAL_X_T)
        return C_ANALYTICAL

    C_ANALYTICAL_ARRAY = ANALYTICAL_SOLUTION_FUNCTION(X_ARRAY)
    #print(C_ANALYTICAL_ARRAY)

    #C_X_DATAFRAMME = PD.DataFrame({'X_ARRAY':X_ARRAY,'C_ANALYTICAL_ARRAY':C_ANALYTICAL_ARRAY})
    #print(C_X_DATAFRAMME)

    #C_X_DATAFRAMME.plot(x='C_ANALYTICAL_ARRAY',y='X_ARRAY',kind = 'scatter')

    X_LOCAL = C_ANALYTICAL_ARRAY
    Y_LOCAL = X_ARRAY
    PLT.scatter(X_LOCAL,Y_LOCAL, label = f'{TIME} days')
    PLT.legend()


PLT.show()