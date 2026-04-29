
import pandas as pd
import matplotlib.pyplot as PLT
import os
import textwrap
os.system('cls')
import matplotlib
import numpy as NP
from sklearn.metrics import r2_score

DF_EXCEL_FILE = pd.read_excel('RESULTS_100cm_1cm_ALL_NODES.xlsx')

print(DF_EXCEL_FILE.head())

print(DF_EXCEL_FILE.columns)

SELECTED_COLUMNS_2DSOIL_PHREEQCRM = ['Time_2DSoil_PhreeqcRM', 'Time ABS 2DSoil-PhreeqcRM',
       'DATE', 'HOUR', 'X', 'Y', 'Y_ABS 2DSoil_PhreeqcRM', 'Ca2+ 2DSoil-PhreeqcRM',
       'Cl- 2DSoil-PhreeqcRM', 'Na+ 2DSoil-PhreeqcRM', 'K+ 2DSoil-PhreeqcRM',
       'NO3- 2DSoil-PhreeqcRM']

SELECTED_COLUMNS_IPHREEQC = ['dist_x', 'Y Iphreeqc',
       'time Iphreeqc', 'step', 'Ca2+ IPhreeqc', 'Cl- IPhreeqc',
       'Na+ IPhreeqc', 'K+ IPhreeqc', 'NO3- IPhreeqc', 'Pore_vol']

DATA_FRAME_2DSOIL_PHREEQCRM = DF_EXCEL_FILE[SELECTED_COLUMNS_2DSOIL_PHREEQCRM]
DATA_FRAME_IPHREEQC = DF_EXCEL_FILE[SELECTED_COLUMNS_IPHREEQC]
print(DATA_FRAME_2DSOIL_PHREEQCRM.head())

# DataFrame for time = 0 seconds
DF_TIME_0_2DSOIL_PHREEQCRM = DATA_FRAME_2DSOIL_PHREEQCRM[DATA_FRAME_2DSOIL_PHREEQCRM['Time ABS 2DSoil-PhreeqcRM'] == 0]
DF_TIME_0_IPHREEQC = DATA_FRAME_IPHREEQC[DATA_FRAME_IPHREEQC['time Iphreeqc'] == 0]

print(DF_TIME_0_2DSOIL_PHREEQCRM.head())
print(DF_TIME_0_2DSOIL_PHREEQCRM.columns)
print(len(DF_TIME_0_2DSOIL_PHREEQCRM))
print(len(DF_TIME_0_IPHREEQC))     

print(DF_TIME_0_IPHREEQC.head())
print(DF_TIME_0_IPHREEQC.columns)

# DataFrame for time = 86400 seconds (1 day)
DF_TIME_86400_2DSOIL_PHREEQCRM = DATA_FRAME_2DSOIL_PHREEQCRM[DATA_FRAME_2DSOIL_PHREEQCRM['Time ABS 2DSoil-PhreeqcRM'] == 86400]
DF_TIME_86400_IPHREEQC = DATA_FRAME_IPHREEQC[DATA_FRAME_IPHREEQC['time Iphreeqc'] == 86400]
print(len(DF_TIME_86400_2DSOIL_PHREEQCRM))
print(len(DF_TIME_86400_IPHREEQC))  

print(DF_TIME_86400_IPHREEQC.head())
print(DF_TIME_86400_IPHREEQC.columns)

# DataFrame for time = 172800 seconds (2 days)
DF_TIME_172800_2DSOIL_PHREEQCRM = DATA_FRAME_2DSOIL_PHREEQCRM[DATA_FRAME_2DSOIL_PHREEQCRM['Time ABS 2DSoil-PhreeqcRM'] == 172800]
DF_TIME_172800_IPHREEQC = DATA_FRAME_IPHREEQC[DATA_FRAME_IPHREEQC['time Iphreeqc'] == 172800]

# Dataframe for time = 259200 seconds (3 days)
DF_TIME_259200_2DSOIL_PHREEQCRM = DATA_FRAME_2DSOIL_PHREEQCRM[DATA_FRAME_2DSOIL_PHREEQCRM['Time ABS 2DSoil-PhreeqcRM'] == 259200]
DF_TIME_259200_IPHREEQC = DATA_FRAME_IPHREEQC[DATA_FRAME_IPHREEQC['time Iphreeqc'] == 259200]

# Dataframe for time = 345600 seconds (4 days)
DF_TIME_345600_2DSOIL_PHREEQCRM = DATA_FRAME_2DSOIL_PHREEQCRM[DATA_FRAME_2DSOIL_PHREEQCRM['Time ABS 2DSoil-PhreeqcRM'] == 345600]
DF_TIME_345600_IPHREEQC = DATA_FRAME_IPHREEQC[DATA_FRAME_IPHREEQC['time Iphreeqc'] == 345600]

###################################
       ######## Ca2+ #########
################################### 
# DAY_1
series1 = NP.array(DF_TIME_86400_2DSOIL_PHREEQCRM[['Ca2+ 2DSoil-PhreeqcRM']])
series2 = NP.array(DF_TIME_86400_IPHREEQC[['Ca2+ IPhreeqc']])
mask = (series1 > 0.01) & (series2 > 0.01)
series1 = series1[mask]
series2 = series2[mask]

# print(series1)
# print(series2)
# print(type(series1))
# print(type(series2))
rmse_DAY_1 = NP.sqrt(NP.mean((series1 - series2) ** 2))
mae_DAY_1 = NP.mean(NP.abs(series1 - series2))
mape_DAY_1 = NP.mean(NP.abs((series1 - series2) / series2)) * 100
smape_DAY_1 = NP.mean(2.0 * NP.abs(series1 - series2) / 
                 (NP.abs(series1) + NP.abs(series2))) * 100
RAE_DAY_1 = NP.sum(NP.abs(series1 - series2)) / NP.sum(NP.abs(series2 - NP.mean(series2)))
MAX_ABS_ERROR_DAY_1 = NP.max(NP.abs(series1 - series2))
r2 = r2_score(series1, series2)
print('Ca2+ RMSE DAY 1:', rmse_DAY_1)
print('Ca2+ MAE DAY 1:', mae_DAY_1)
print(f"Ca2+ SMAPE DAY 1: {smape_DAY_1:.2f}%")
print('Ca2+ MAX_ABS_ERROR_DAY_1:', MAX_ABS_ERROR_DAY_1)
print('Ca2+ R2 DAY 1:', r2)
print('Ca2+ RAE DAY 1:', RAE_DAY_1)
print('Ca2+ MAPE DAY 1:', mape_DAY_1, '%')


# DAY_2
series1 = NP.array(DF_TIME_172800_2DSOIL_PHREEQCRM[['Ca2+ 2DSoil-PhreeqcRM']])
series2 = NP.array(DF_TIME_172800_IPHREEQC[['Ca2+ IPhreeqc']])
mask = (series1 > 0.01) & (series2 > 0.01)
series1 = series1[mask]
series2 = series2[mask]

rmse_DAY_2 = NP.sqrt(NP.mean((series1 - series2) ** 2))
mae_DAY_2 = NP.mean(NP.abs(series1 - series2))
mape_DAY_2 = NP.mean(NP.abs((series1 - series2) / series2)) * 100
smape_DAY_2 = NP.mean(2.0 * NP.abs(series1 - series2) / 
                 (NP.abs(series1) + NP.abs(series2))) * 100
RAE_DAY_2 = NP.sum(NP.abs(series1 - series2)) / NP.sum(NP.abs(series2 - NP.mean(series2)))
MAX_ABS_ERROR_DAY_2 = NP.max(NP.abs(series1 - series2))
r2 = r2_score(series1, series2)
print('Ca2+ RMSE DAY 2:', rmse_DAY_2)
print('Ca2+ MAE DAY 2:', mae_DAY_2)
print(f"Ca2+ SMAPE DAY 2: {smape_DAY_2:.2f}%")
print('Ca2+ MAX_ABS_ERROR_DAY_2:', MAX_ABS_ERROR_DAY_2)
print('Ca2+ R2 DAY 2:', r2)
print('Ca2+ RAE DAY 2:', RAE_DAY_2)
print('Ca2+ MAPE DAY 2:', mape_DAY_2, '%')

# DAY_3
series1 = NP.array(DF_TIME_259200_2DSOIL_PHREEQCRM[['Ca2+ 2DSoil-PhreeqcRM']])
series2 = NP.array(DF_TIME_259200_IPHREEQC[['Ca2+ IPhreeqc']])
mask = (series1 > 0.01) & (series2 > 0.01)
series1 = series1[mask]
series2 = series2[mask]

rmse_DAY_3 = NP.sqrt(NP.mean((series1 - series2) ** 2))
mae_DAY_3 = NP.mean(NP.abs(series1 - series2))
mape_DAY_3 = NP.mean(NP.abs((series1 - series2) / series2)) * 100
smape_DAY_3 = NP.mean(2.0 * NP.abs(series1 - series2) / 
                 (NP.abs(series1) + NP.abs(series2))) * 100
RAE_DAY_3 = NP.sum(NP.abs(series1 - series2)) / NP.sum(NP.abs(series2 - NP.mean(series2)))
MAX_ABS_ERROR_DAY_3 = NP.max(NP.abs(series1 - series2))
r2 = r2_score(series1, series2)
print('Ca2+ RMSE DAY 3:', rmse_DAY_3)
print('Ca2+ MAE DAY 3:', mae_DAY_3)
print(f"Ca2+ SMAPE DAY 3: {smape_DAY_3:.2f}%")
print('Ca2+ MAX_ABS_ERROR_DAY_3:', MAX_ABS_ERROR_DAY_3)
print('Ca2+ R2 DAY 3:', r2)
print('Ca2+ RAE DAY 3:', RAE_DAY_3)
print('Ca2+ MAPE DAY 3:', mape_DAY_3, '%')


AVERAGE_RMSE_CA2 = (rmse_DAY_1 + rmse_DAY_2 + rmse_DAY_3) / 3
print('Ca2+ AVERAGE_RMSE (DAY 1 to DAY 3):', AVERAGE_RMSE_CA2)
AVERAGE_MAPE_CA2 = (mape_DAY_1 + mape_DAY_2 + mape_DAY_3) / 3
print('Ca2+ AVERAGE_MAPE (DAY 1 to DAY 3):', AVERAGE_MAPE_CA2, '%')

# DAY_4     # CONCENTRATIONS ARE LOW ON DAY 4, SO NOT CONSIDERED IN THE ANALYSIS
# series1 = NP.array(DF_TIME_345600_2DSOIL_PHREEQCRM[['Ca2+ 2DSoil-PhreeqcRM']])
# series2 = NP.array(DF_TIME_345600_IPHREEQC[['Ca2+ IPhreeqc']])
# mask = (series1 > 0.01) & (series2 > 0.01)
# series1 = series1[mask]
# series2 = series2[mask]

# rmse_DAY_4 = NP.sqrt(NP.mean((series1 - series2) ** 2))
# mae_DAY_4 = NP.mean(NP.abs(series1 - series2))
# mape_DAY_4 = NP.mean(NP.abs((series1 - series2) / series2)) * 100
# smape_DAY_4 = NP.mean(2.0 * NP.abs(series1 - series2) / 
#                  (NP.abs(series1) + NP.abs(series2))) * 100
# RAE_DAY_4 = NP.sum(NP.abs(series1 - series2)) / NP.sum(NP.abs(series2 - NP.mean(series2)))
# MAX_ABS_ERROR_DAY_4 = NP.max(NP.abs(series1 - series2))
# r2 = r2_score(series1, series2)
# print('Ca2+ RMSE DAY 4:', rmse_DAY_4)
# print('Ca2+ MAE DAY 4:', mae_DAY_4)
# print(f"Ca2+ SMAPE DAY 4: {smape_DAY_4:.2f}%")
# print('Ca2+ MAX_ABS_ERROR_DAY_4:', MAX_ABS_ERROR_DAY_4)
# print('Ca2+ R2 DAY 4:', r2)
# print('Ca2+ RAE DAY 4:', RAE_DAY_4)
# print('Ca2+ MAPE DAY 4:', mape_DAY_4, '%')





###################################
       ######## Na+ #########
################################### 
# DAY_1
series1 = NP.array(DF_TIME_86400_2DSOIL_PHREEQCRM[['Na+ 2DSoil-PhreeqcRM']])
series2 = NP.array(DF_TIME_86400_IPHREEQC[['Na+ IPhreeqc']])
mask = (series1 > 0.01) & (series2 > 0.01)
series1 = series1[mask]
series2 = series2[mask]

# print(series1)
# print(series2)
# print(type(series1))
# print(type(series2))
rmse_DAY_1 = NP.sqrt(NP.mean((series1 - series2) ** 2))
mae_DAY_1 = NP.mean(NP.abs(series1 - series2))
mape_DAY_1 = NP.mean(NP.abs((series1 - series2) / series2)) * 100
smape_DAY_1 = NP.mean(2.0 * NP.abs(series1 - series2) / 
                 (NP.abs(series1) + NP.abs(series2))) * 100
RAE_DAY_1 = NP.sum(NP.abs(series1 - series2)) / NP.sum(NP.abs(series2 - NP.mean(series2)))
MAX_ABS_ERROR_DAY_1 = NP.max(NP.abs(series1 - series2))
r2 = r2_score(series1, series2)
print('Na+ RMSE DAY 1:', rmse_DAY_1)
print('Na+ MAE DAY 1:', mae_DAY_1)
print(f"Na+ SMAPE DAY 1: {smape_DAY_1:.2f}%")
print('Na+ MAX_ABS_ERROR_DAY_1:', MAX_ABS_ERROR_DAY_1)
print('Na+ R2 DAY 1:', r2)
print('Na+ RAE DAY 1:', RAE_DAY_1)
print('Na+ MAPE DAY 1:', mape_DAY_1, '%')


# DAY_2
series1 = NP.array(DF_TIME_172800_2DSOIL_PHREEQCRM[['Na+ 2DSoil-PhreeqcRM']])
series2 = NP.array(DF_TIME_172800_IPHREEQC[['Na+ IPhreeqc']])
mask = (series1 > 0.01) & (series2 > 0.01)
series1 = series1[mask]
series2 = series2[mask]

rmse_DAY_2 = NP.sqrt(NP.mean((series1 - series2) ** 2))
mae_DAY_2 = NP.mean(NP.abs(series1 - series2))
mape_DAY_2 = NP.mean(NP.abs((series1 - series2) / series2)) * 100
smape_DAY_2 = NP.mean(2.0 * NP.abs(series1 - series2) / 
                 (NP.abs(series1) + NP.abs(series2))) * 100
RAE_DAY_2 = NP.sum(NP.abs(series1 - series2)) / NP.sum(NP.abs(series2 - NP.mean(series2)))
MAX_ABS_ERROR_DAY_2 = NP.max(NP.abs(series1 - series2))
r2 = r2_score(series1, series2)
print('Na+ RMSE DAY 2:', rmse_DAY_2)
print('Na+ MAE DAY 2:', mae_DAY_2)
print(f"Na+ SMAPE DAY 2: {smape_DAY_2:.2f}%")
print('Na+ MAX_ABS_ERROR_DAY_2:', MAX_ABS_ERROR_DAY_2)
print('Na+ R2 DAY 2:', r2)
print('Na+ RAE DAY 2:', RAE_DAY_2)
print('Na+ MAPE DAY 2:', mape_DAY_2, '%')

# DAY_3
series1 = NP.array(DF_TIME_259200_2DSOIL_PHREEQCRM[['Na+ 2DSoil-PhreeqcRM']])
series2 = NP.array(DF_TIME_259200_IPHREEQC[['Na+ IPhreeqc']])
mask = (series1 > 0.01) & (series2 > 0.01)
series1 = series1[mask]
series2 = series2[mask]

rmse_DAY_3 = NP.sqrt(NP.mean((series1 - series2) ** 2))
mae_DAY_3 = NP.mean(NP.abs(series1 - series2))
mape_DAY_3 = NP.mean(NP.abs((series1 - series2) / series2)) * 100
smape_DAY_3 = NP.mean(2.0 * NP.abs(series1 - series2) / 
                 (NP.abs(series1) + NP.abs(series2))) * 100
RAE_DAY_3 = NP.sum(NP.abs(series1 - series2)) / NP.sum(NP.abs(series2 - NP.mean(series2)))
MAX_ABS_ERROR_DAY_3 = NP.max(NP.abs(series1 - series2))
r2 = r2_score(series1, series2)
print('Na+ RMSE DAY 3:', rmse_DAY_3)
print('Na+ MAE DAY 3:', mae_DAY_3)
print(f"Na+ SMAPE DAY 3: {smape_DAY_3:.2f}%")
print('Na+ MAX_ABS_ERROR_DAY_3:', MAX_ABS_ERROR_DAY_3)
print('Na+ R2 DAY 3:', r2)
print('Na+ RAE DAY 3:', RAE_DAY_3)
print('Na+ MAPE DAY 3:', mape_DAY_3, '%')

AVERAGE_RMSE_NA = (rmse_DAY_1 + rmse_DAY_2 + rmse_DAY_3) / 3
print('Na+ AVERAGE_RMSE (DAY 1 to DAY 3):', AVERAGE_RMSE_NA)
AVERAGE_MAPE_NA = (mape_DAY_1 + mape_DAY_2 + mape_DAY_3) / 3
print('Na+ AVERAGE_MAPE (DAY 1 to DAY 3):', AVERAGE_MAPE_NA, '%')

# # DAY_4 
# series1 = NP.array(DF_TIME_345600_2DSOIL_PHREEQCRM[['Na+ 2DSoil-PhreeqcRM']])
# series2 = NP.array(DF_TIME_345600_IPHREEQC[['Na+ IPhreeqc']])
# mask = (series1 > 0.01) & (series2 > 0.01)
# series1 = series1[mask]
# series2 = series2[mask]

# if len(series1) > 0 and len(series2) > 0:
#     rmse_DAY_4 = NP.sqrt(NP.mean((series1 - series2) ** 2))
#     mae_DAY_4 = NP.mean(NP.abs(series1 - series2))
#     mape_DAY_4 = NP.mean(NP.abs((series1 - series2) / series2)) * 100
#     smape_DAY_4 = NP.mean(2.0 * NP.abs(series1 - series2) / 
#                  (NP.abs(series1) + NP.abs(series2))) * 100
#     RAE_DAY_4 = NP.sum(NP.abs(series1 - series2)) / NP.sum(NP.abs(series2 - NP.mean(series2)))
#     MAX_ABS_ERROR_DAY_4 = NP.max(NP.abs(series1 - series2))
#     r2 = r2_score(series1, series2)
#     print('Na+ RMSE DAY 4:', rmse_DAY_4)
#     print('Na+ MAE DAY 4:', mae_DAY_4)
#     print(f"Na+ SMAPE DAY 4: {smape_DAY_4:.2f}%")
#     print('Na+ MAX_ABS_ERROR_DAY_4:', MAX_ABS_ERROR_DAY_4)
#     print('Na+ R2 DAY 4:', r2)
#     print('Na+ RAE DAY 4:', RAE_DAY_4)
#     print('Na+ MAPE DAY 4:', mape_DAY_4, '%')
# else:
#     print('Na+ DAY 4: No data available after filtering')





###################################
       ######## K+ #########
################################### 
# DAY_1
series1 = NP.array(DF_TIME_86400_2DSOIL_PHREEQCRM[['K+ 2DSoil-PhreeqcRM']])
series2 = NP.array(DF_TIME_86400_IPHREEQC[['K+ IPhreeqc']])
mask = (series1 > 0.01) & (series2 > 0.01)
series1 = series1[mask]
series2 = series2[mask]

# print(series1)
# print(series2)
# print(type(series1))
# print(type(series2))

if len(series1) > 0 and len(series2) > 0:
    rmse_DAY_1 = NP.sqrt(NP.mean((series1 - series2) ** 2))
    mae_DAY_1 = NP.mean(NP.abs(series1 - series2))
    mape_DAY_1 = NP.mean(NP.abs((series1 - series2) / series2)) * 100
    smape_DAY_1 = NP.mean(2.0 * NP.abs(series1 - series2) / 
                     (NP.abs(series1) + NP.abs(series2))) * 100
    RAE_DAY_1 = NP.sum(NP.abs(series1 - series2)) / NP.sum(NP.abs(series2 - NP.mean(series2)))
    MAX_ABS_ERROR_DAY_1 = NP.max(NP.abs(series1 - series2))
    r2 = r2_score(series1, series2)
    print('K+ RMSE DAY 1:', rmse_DAY_1)
    print('K+ MAE DAY 1:', mae_DAY_1)
    print(f"K+ SMAPE DAY 1: {smape_DAY_1:.2f}%")
    print('K+ MAX_ABS_ERROR_DAY_1:', MAX_ABS_ERROR_DAY_1)
    print('K+ R2 DAY 1:', r2)
    print('K+ RAE DAY 1:', RAE_DAY_1)
    print('K+ MAPE DAY 1:', mape_DAY_1, '%')
else:
    print('K+ DAY 1: No data available after filtering')


# DAY_2
series1 = NP.array(DF_TIME_172800_2DSOIL_PHREEQCRM[['K+ 2DSoil-PhreeqcRM']])
series2 = NP.array(DF_TIME_172800_IPHREEQC[['K+ IPhreeqc']])
mask = (series1 > 0.01) & (series2 > 0.01)
series1 = series1[mask]
series2 = series2[mask]

if len(series1) > 0 and len(series2) > 0:
    rmse_DAY_2 = NP.sqrt(NP.mean((series1 - series2) ** 2))
    mae_DAY_2 = NP.mean(NP.abs(series1 - series2))
    mape_DAY_2 = NP.mean(NP.abs((series1 - series2) / series2)) * 100
    smape_DAY_2 = NP.mean(2.0 * NP.abs(series1 - series2) / 
                     (NP.abs(series1) + NP.abs(series2))) * 100
    RAE_DAY_2 = NP.sum(NP.abs(series1 - series2)) / NP.sum(NP.abs(series2 - NP.mean(series2)))
    MAX_ABS_ERROR_DAY_2 = NP.max(NP.abs(series1 - series2))
    r2 = r2_score(series1, series2)
    print('K+ RMSE DAY 2:', rmse_DAY_2)
    print('K+ MAE DAY 2:', mae_DAY_2)
    print(f"K+ SMAPE DAY 2: {smape_DAY_2:.2f}%")
    print('K+ MAX_ABS_ERROR_DAY_2:', MAX_ABS_ERROR_DAY_2)
    print('K+ R2 DAY 2:', r2)
    print('K+ RAE DAY 2:', RAE_DAY_2)
    print('K+ MAPE DAY 2:', mape_DAY_2, '%')
else:
    print('K+ DAY 2: No data available after filtering')

# DAY_3
series1 = NP.array(DF_TIME_259200_2DSOIL_PHREEQCRM[['K+ 2DSoil-PhreeqcRM']])
series2 = NP.array(DF_TIME_259200_IPHREEQC[['K+ IPhreeqc']])
mask = (series1 > 0.01) & (series2 > 0.01)
series1 = series1[mask]
series2 = series2[mask]

if len(series1) > 0 and len(series2) > 0:
    rmse_DAY_3 = NP.sqrt(NP.mean((series1 - series2) ** 2))
    mae_DAY_3 = NP.mean(NP.abs(series1 - series2))
    mape_DAY_3 = NP.mean(NP.abs((series1 - series2) / series2)) * 100
    smape_DAY_3 = NP.mean(2.0 * NP.abs(series1 - series2) / 
                     (NP.abs(series1) + NP.abs(series2))) * 100
    RAE_DAY_3 = NP.sum(NP.abs(series1 - series2)) / NP.sum(NP.abs(series2 - NP.mean(series2)))
    MAX_ABS_ERROR_DAY_3 = NP.max(NP.abs(series1 - series2))
    r2 = r2_score(series1, series2)
    print('K+ RMSE DAY 3:', rmse_DAY_3)
    print('K+ MAE DAY 3:', mae_DAY_3)
    print(f"K+ SMAPE DAY 3: {smape_DAY_3:.2f}%")
    print('K+ MAX_ABS_ERROR_DAY_3:', MAX_ABS_ERROR_DAY_3)
    print('K+ R2 DAY 3:', r2)
    print('K+ RAE DAY 3:', RAE_DAY_3)
    print('K+ MAPE DAY 3:', mape_DAY_3, '%')
else:
    print('K+ DAY 3: No data available after filtering')


AVERAGE_RMSE_K = (rmse_DAY_1 + rmse_DAY_2 + rmse_DAY_3) / 3
print('K+ AVERAGE_RMSE (DAY 1 to DAY 3):', AVERAGE_RMSE_K)
AVERAGE_MAPE_K = (mape_DAY_1 + mape_DAY_2 + mape_DAY_3) / 3
print('K+ AVERAGE_MAPE (DAY 1 to DAY 3):', AVERAGE_MAPE_K, '%')

# # DAY_4
# series1 = NP.array(DF_TIME_345600_2DSOIL_PHREEQCRM[['K+ 2DSoil-PhreeqcRM']])
# series2 = NP.array(DF_TIME_345600_IPHREEQC[['K+ IPhreeqc']])
# mask = (series1 > 0.01) & (series2 > 0.01)
# series1 = series1[mask]
# series2 = series2[mask]

# if len(series1) > 0 and len(series2) > 0:
#     rmse_DAY_4 = NP.sqrt(NP.mean((series1 - series2) ** 2))
#     mae_DAY_4 = NP.mean(NP.abs(series1 - series2))
#     mape_DAY_4 = NP.mean(NP.abs((series1 - series2) / series2)) * 100
#     smape_DAY_4 = NP.mean(2.0 * NP.abs(series1 - series2) / 
#                      (NP.abs(series1) + NP.abs(series2))) * 100
#     RAE_DAY_4 = NP.sum(NP.abs(series1 - series2)) / NP.sum(NP.abs(series2 - NP.mean(series2)))
#     MAX_ABS_ERROR_DAY_4 = NP.max(NP.abs(series1 - series2))
#     r2 = r2_score(series1, series2)
#     print('K+ RMSE DAY 4:', rmse_DAY_4)
#     print('K+ MAE DAY 4:', mae_DAY_4)
#     print(f"K+ SMAPE DAY 4: {smape_DAY_4:.2f}%")
#     print('K+ MAX_ABS_ERROR_DAY_4:', MAX_ABS_ERROR_DAY_4)
#     print('K+ R2 DAY 4:', r2)
#     print('K+ RAE DAY 4:', RAE_DAY_4)
#     print('K+ MAPE DAY 4:', mape_DAY_4, '%')
# else:
#     print('K+ DAY 4: No data available after filtering')



