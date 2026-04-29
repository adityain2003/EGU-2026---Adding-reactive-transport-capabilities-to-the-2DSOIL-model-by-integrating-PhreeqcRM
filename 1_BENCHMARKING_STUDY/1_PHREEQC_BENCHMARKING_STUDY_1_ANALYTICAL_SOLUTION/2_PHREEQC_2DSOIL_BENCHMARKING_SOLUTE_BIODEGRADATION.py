# NOTES: PLOTTING : https://stackoverflow.com/questions/77212040/get-seperate-plots-and-one-accumulated-in-matplotlib-pyplot


import numpy as NP
import pandas as PD
import matplotlib.pyplot as PLT
import math
from scipy import special
import os

T_LIST = [0,1,2,3]

FIGURE,AXES = PLT.subplots()

# CALCULATION OF ANALYTICAL SOLUTION
U_DARCY = 25.648 # 45.7 #DARCY FLOW VELOCITY cm/day
THETA_SATURATED = 0.2817 # SATURATED MOISTURE CONTENT = POROSITY
U_PORE = U_DARCY/THETA_SATURATED # PORE VELOCITY
X_ARRAY = NP.linspace(749.999,0.001,num = 50) #DISTANCE FROM INLET in cm
DX = 75*U_PORE #12.8*U_PORE #DISPERSITIVITY in cm
C_INJECTED = 1.0 # CONCENTRATION OF INJECTED LIQUID
C_X_T = 0 # CONCENTRATION AT A GIVEN POINT (X) AT A GIVEN TIME (T)
COLUMN_LENGTH = 750 # LENGTH OF COLUMN (in cm)
RATE_OF_REACTION = 0.001
MU = 3*(1e-6)*86400
GAMMA = 0.0*1*(1e-6)*86400

os.system('cls')
# ANALYTICAL SOLUTION FOR ZERO ORDER PRODUCTION (OR DECAY)

for TIME in T_LIST:
    DX = 75*U_PORE #12.8*U_PORE
    U_PORE = U_PORE

    T = TIME #TIME ELAPSED SINCE BEGINNNING OF INJECTION IN day

    def ANALYTICAL_SOLUTION_FUNCTION(X_ARRAY):
        # CALCULATES ANALYTICAL SOLUTION 
        C_ANALYTICAL = [] # CRETATE AN EMPTY LIST AND THE VALUES ARE APPENDED TO IT AFTER CALCULATION
    #print(EPSILON)
    #print(ETA)
        print('Time=',TIME)
        for X in X_ARRAY:
            X_LOCAL = COLUMN_LENGTH-X

            U_TERM = U_PORE*math.sqrt(1+4*MU*DX/(U_PORE*U_PORE))
            GAMMA_BY_MU = GAMMA/MU

            H_X_T_1_1 = 0.5*math.exp(((U_PORE-U_TERM)*X_LOCAL)/(2*DX))
            H_X_T_1_2 = math.erfc((X_LOCAL - U_TERM*T)/(2*math.sqrt(DX*T)))
            H_X_T_2_1 = 0.5*math.exp(((U_PORE+U_TERM)*X_LOCAL)/(2*DX))
            H_X_T_2_2 = math.erfc((X_LOCAL + U_TERM*T)/(2*math.sqrt(DX*T)))
            H_TERM = (H_X_T_1_1*H_X_T_1_2+H_X_T_2_1*H_X_T_2_2)


            M_X_T_1_1 = GAMMA_BY_MU*math.exp(-1*MU*T)
            M_X_T_1_2 = 0.5*math.erfc((X_LOCAL-U_PORE*T)/(2*math.sqrt(DX*T)))
            M_X_T_2_1 = 0.5*(math.exp(U_PORE*X_LOCAL/DX))
            M_X_T_2_2 = math.erfc((X_LOCAL+U_PORE*T)/(2*math.sqrt(DX*T)))
            M_X_T_3_1 = GAMMA_BY_MU
            M_X_T_4_2 = (0-GAMMA_BY_MU)
            M_X_T_5_3 = math.exp(-1*MU*T)
            M_TERM = M_X_T_1_1*(M_X_T_1_2+M_X_T_2_1*M_X_T_2_2)+M_X_T_3_1+M_X_T_4_2*M_X_T_5_3

            C_ANALYTICAL_X_T = (1-GAMMA_BY_MU)*H_TERM + M_TERM

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