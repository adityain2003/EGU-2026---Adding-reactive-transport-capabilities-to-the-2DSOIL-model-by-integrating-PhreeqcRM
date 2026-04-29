# NOTES: PLOTTING : https://stackoverflow.com/questions/77212040/get-seperate-plots-and-one-accumulated-in-matplotlib-pyplot


import numpy as NP
import pandas as PD
import matplotlib.pyplot as PLT
import math
from scipy import special
import os

T_LIST = [1,2,3]

FIGURE,AXES = PLT.subplots()

# CALCULATION OF ANALYTICAL SOLUTION
U_DARCY = 25.648 # 45.7 #DARCY FLOW VELOCITY cm/day
THETA_SATURATED = 0.2817 # SATURATED MOISTURE CONTENT = POROSITY
U_PORE = U_DARCY/THETA_SATURATED # PORE VELOCITY
#X_ARRAY = NP.linspace(749.999,0.001,num = 50) #DISTANCE FROM INLET in cm
X_SERIES = PD.read_excel('COLUMN_SAMPLED_COORDINATES.xlsx')
print(X_SERIES)
print(type(X_SERIES))
X_ARRAY = X_SERIES.to_numpy().flatten()
DX = 75*U_PORE #12.8*U_PORE #DISPERSITIVITY in cm
C_INJECTED = 1.0 # CONCENTRATION OF INJECTED LIQUID
C_X_T = 0 # CONCENTRATION AT A GIVEN POINT (X) AT A GIVEN TIME (T)
COLUMN_LENGTH = 750 # LENGTH OF COLUMN (in cm)
RATE_OF_REACTION = 0.001
MU = 3*(1e-6)*86400
GAMMA = 0.0*1*(1e-6)*86400

data = {'X_ARRAY': X_ARRAY}

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
    data[f'C_{TIME}_days'] = C_ANALYTICAL_ARRAY
    #print(C_ANALYTICAL_ARRAY)

    #C_X_DATAFRAMME = PD.DataFrame({'X_ARRAY':X_ARRAY,'C_ANALYTICAL_ARRAY':C_ANALYTICAL_ARRAY})
    #print(C_X_DATAFRAMME)

    #C_X_DATAFRAMME.plot(x='C_ANALYTICAL_ARRAY',y='X_ARRAY',kind = 'scatter')

    X_LOCAL = C_ANALYTICAL_ARRAY
    Y_LOCAL = X_ARRAY
    PLT.scatter(X_LOCAL,Y_LOCAL, label = f'{TIME} days')
    PLT.legend()

DATA_FRAME = PD.DataFrame(data)    
PLT.show()


DATAFRAME_CASE_2 = PD.read_excel('RESULTS_BENCHMARKING_ANALYTICAL_SOLUTION_750CM.xlsx', sheet_name='CASE_2')
DATAFRAME_CASE_2_DAY_1 = DATAFRAME_CASE_2[DATAFRAME_CASE_2['DAY'] == 1]


series1 = DATA_FRAME['C_1_days']
series2 = DATAFRAME_CASE_2_DAY_1['CONC_RATIO_SIMULATED'].to_numpy().flatten()
rmse_DAY_1 = NP.sqrt(NP.mean((series1 - series2) ** 2))
mae_DAY_1 = NP.mean(NP.abs(series1 - series2))
smape_DAY_1 = NP.mean(2.0 * NP.abs(series1 - series2) / 
                 (NP.abs(series1) + NP.abs(series2))) * 100
mape_DAY_1 = NP.mean(NP.abs((series1 - series2) / series1)) * 100
print('RMSE DAY 1:', rmse_DAY_1)
print('MAE DAY 1:', mae_DAY_1)
print(f"SMAPE DAY 1: {smape_DAY_1:.2f}%")
print(f"MAPE DAY 1: {mape_DAY_1:.2f}%")
PLT.figure()

PLT.plot(series1, X_ARRAY, color='blue')
PLT.plot(series2, X_ARRAY, color='red', linestyle='--')

PLT.show()

DATAFRAME_CASE_2_DAY_2 = DATAFRAME_CASE_2[DATAFRAME_CASE_2['DAY'] == 2]
series1 = DATA_FRAME['C_2_days']
series2 = DATAFRAME_CASE_2_DAY_2['CONC_RATIO_SIMULATED'].to_numpy().flatten()
rmse_DAY_2 = NP.sqrt(NP.mean((series1 - series2) ** 2))
mae_DAY_2 = NP.mean(NP.abs(series1 - series2))
smape_DAY_2 = NP.mean(2.0 * NP.abs(series1 - series2) / 
                 (NP.abs(series1) + NP.abs(series2))) * 100
mape_DAY_2 = NP.mean(NP.abs((series1 - series2) / series1)) * 100
print('RMSE DAY 2:', rmse_DAY_2)
print('MAE DAY 2:', mae_DAY_2)
print(f"SMAPE_DAY_2: {smape_DAY_2:.2f}%")
print(f"MAPE_DAY_2: {mape_DAY_2:.2f}%")
PLT.figure()
PLT.plot(series1, X_ARRAY, color='blue')
PLT.plot(series2, X_ARRAY, color='red', linestyle='--')
PLT.show()


DATAFRAME_CASE_2_DAY_3 = DATAFRAME_CASE_2[DATAFRAME_CASE_2['DAY'] == 3] 
series1 = DATA_FRAME['C_3_days']
series2 = DATAFRAME_CASE_2_DAY_3['CONC_RATIO_SIMULATED'].to_numpy().flatten()
rmse_DAY_3 = NP.sqrt(NP.mean((series1 - series2) ** 2))
mae_DAY_3 = NP.mean(NP.abs(series1 - series2))
smape_DAY_3 = NP.mean(2.0 * NP.abs(series1 - series2) / 
                 (NP.abs(series1) + NP.abs(series2))) * 100
mape_DAY_3 = NP.mean(NP.abs((series1 - series2) / series1)) * 100
print('RMSE DAY 3:', rmse_DAY_3)
print('MAE DAY 3:', mae_DAY_3)
print(f"SMAPE_DAY_3: {smape_DAY_3:.2f}%")
print(f"MAPE_DAY_3: {mape_DAY_3:.2f}%")
PLT.figure()
PLT.plot(series1, X_ARRAY, color='blue')
PLT.plot(series2, X_ARRAY, color='red', linestyle='--')
PLT.show()

AVERAGE_RMSE = (rmse_DAY_1 + rmse_DAY_2 + rmse_DAY_3) / 3
print('AVERAGE_RMSE (DAY 1 to DAY 3):', AVERAGE_RMSE)
AVERAGE_MAPE = (mape_DAY_1 + mape_DAY_2 + mape_DAY_3) / 3
print('AVERAGE_MAPE (DAY 1 to DAY 3):', AVERAGE_MAPE, '%')