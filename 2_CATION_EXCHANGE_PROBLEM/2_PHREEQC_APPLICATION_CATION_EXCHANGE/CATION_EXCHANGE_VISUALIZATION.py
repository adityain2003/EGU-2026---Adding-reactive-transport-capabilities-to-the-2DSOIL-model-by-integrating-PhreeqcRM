
import pandas as pd
import matplotlib.pyplot as PLT
import os
import textwrap
os.system('cls')
import matplotlib
import numpy as NP

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

print(DF_TIME_0_IPHREEQC.head())
print(DF_TIME_0_IPHREEQC.columns)

# DataFrame for time = 86400 seconds (1 day)
DF_TIME_86400_2DSOIL_PHREEQCRM = DATA_FRAME_2DSOIL_PHREEQCRM[DATA_FRAME_2DSOIL_PHREEQCRM['Time ABS 2DSoil-PhreeqcRM'] == 86400]
DF_TIME_86400_IPHREEQC = DATA_FRAME_IPHREEQC[DATA_FRAME_IPHREEQC['time Iphreeqc'] == 86400]

print(DF_TIME_86400_2DSOIL_PHREEQCRM.head())
print(DF_TIME_86400_2DSOIL_PHREEQCRM.columns)

print(DF_TIME_86400_IPHREEQC.head())
print(DF_TIME_86400_IPHREEQC.columns)

# DataFrame for time = 172800 seconds (7 days)
DF_TIME_172800_2DSOIL_PHREEQCRM = DATA_FRAME_2DSOIL_PHREEQCRM[DATA_FRAME_2DSOIL_PHREEQCRM['Time ABS 2DSoil-PhreeqcRM'] == 172800]
DF_TIME_172800_IPHREEQC = DATA_FRAME_IPHREEQC[DATA_FRAME_IPHREEQC['time Iphreeqc'] == 172800]

# Dataframe for time = 259200 seconds (2 days)
DF_TIME_259200_2DSOIL_PHREEQCRM = DATA_FRAME_2DSOIL_PHREEQCRM[DATA_FRAME_2DSOIL_PHREEQCRM['Time ABS 2DSoil-PhreeqcRM'] == 259200]
DF_TIME_259200_IPHREEQC = DATA_FRAME_IPHREEQC[DATA_FRAME_IPHREEQC['time Iphreeqc'] == 259200]

# Dataframe for time = 345600 seconds (3 days)
DF_TIME_345600_2DSOIL_PHREEQCRM = DATA_FRAME_2DSOIL_PHREEQCRM[DATA_FRAME_2DSOIL_PHREEQCRM['Time ABS 2DSoil-PhreeqcRM'] == 345600]
DF_TIME_345600_IPHREEQC = DATA_FRAME_IPHREEQC[DATA_FRAME_IPHREEQC['time Iphreeqc'] == 345600]

PLT.rcParams['font.family'] = 'Times New Roman'
FIGURE,AXES = PLT.subplots(nrows=1, ncols=3, figsize=(19.2, 10.8))
PLT.subplots_adjust(top=0.960, bottom=0.125)

#PLT.subplots_adjust(wspace=0.5)

AX_1 = AXES[0]
AX_2 = AXES[1]
AX_3 = AXES[2]

# Plotting Ca2+ for time = 0 seconds
AX_1.plot(DF_TIME_0_2DSOIL_PHREEQCRM['Ca2+ 2DSoil-PhreeqcRM'], DF_TIME_0_2DSOIL_PHREEQCRM['Y_ABS 2DSoil_PhreeqcRM'], label=' ',color = 'red',linestyle='--')
#AX_1.plot(DF_TIME_0_2DSOIL_PHREEQCRM['Ca2+ 2DSoil-PhreeqcRM'], DF_TIME_0_2DSOIL_PHREEQCRM['Y_ABS 2DSoil_PhreeqcRM'], label='Time = 0, Source: 2DSoil-PhreeqcRM',color = 'red',linestyle='--')
AX_1.scatter(DF_TIME_0_IPHREEQC['Ca2+ IPhreeqc'].iloc[::2], DF_TIME_0_IPHREEQC['Y Iphreeqc'].iloc[::2], label=' ', color = 'red', s = 25)
# AX_1.scatter(DF_TIME_0_IPHREEQC['Ca2+ IPhreeqc'].iloc[::2], DF_TIME_0_IPHREEQC['Y Iphreeqc'].iloc[::2], label='Time = 0, Source: IPhreeqc', color = 'red', s = 25)
AX_1.set_xlabel(r'Ca$^{2+}$ Concentration (mmols/l)',fontsize=20)
AX_1.set_ylabel('Height above the column base (cm)',fontsize=20)
LONG_TITLE = '(a)'
WRAPPED_TITLE = textwrap.fill(LONG_TITLE, width=40)
AX_1.set_title(WRAPPED_TITLE,fontsize=20,x=0.5, y=1.01)
AX_1.set_xlim(-0.0025, 0.6)
AX_1.set_ylim(0, 100)
x = DF_TIME_0_2DSOIL_PHREEQCRM['Ca2+ 2DSoil-PhreeqcRM'].iloc[10]
y = DF_TIME_0_2DSOIL_PHREEQCRM['Y_ABS 2DSoil_PhreeqcRM'].iloc[10]
AX_1.text(x+0.015, y, 'Time = 0 Day', color='black', fontsize=12, bbox=dict(facecolor='white', edgecolor='black', alpha=0.8))

# Plotting Ca2+ for time = 86400 seconds (1 day)
AX_1.plot(DF_TIME_86400_2DSOIL_PHREEQCRM['Ca2+ 2DSoil-PhreeqcRM'], DF_TIME_86400_2DSOIL_PHREEQCRM['Y_ABS 2DSoil_PhreeqcRM'], label=' ',color = 'blue',linestyle='--')
#AX_1.plot(DF_TIME_86400_2DSOIL_PHREEQCRM['Ca2+ 2DSoil-PhreeqcRM'], DF_TIME_86400_2DSOIL_PHREEQCRM['Y_ABS 2DSoil_PhreeqcRM'], label='Time = 1 Day, Source: 2DSoil-PhreeqcRM',color = 'blue',linestyle='--')
AX_1.scatter(DF_TIME_86400_IPHREEQC['Ca2+ IPhreeqc'].iloc[::2], DF_TIME_86400_IPHREEQC['Y Iphreeqc'].iloc[::2], label=' ', color = 'blue', s = 25)
#AX_1.scatter(DF_TIME_86400_IPHREEQC['Ca2+ IPhreeqc'].iloc[::2], DF_TIME_86400_IPHREEQC['Y Iphreeqc'].iloc[::2], label='Time = 1 Day, Source: IPhreeqc', color = 'blue', s = 25)
x = DF_TIME_86400_2DSOIL_PHREEQCRM['Ca2+ 2DSoil-PhreeqcRM'].iloc[28]
y = DF_TIME_86400_2DSOIL_PHREEQCRM['Y_ABS 2DSoil_PhreeqcRM'].iloc[28]
AX_1.text(x, y-2, '1 Day', color='black', fontsize=12, bbox=dict(facecolor='white', edgecolor='black', alpha=0.8))

# Plotting Ca2+ for time = 172800 seconds (2 days)
AX_1.plot(DF_TIME_172800_2DSOIL_PHREEQCRM['Ca2+ 2DSoil-PhreeqcRM'], DF_TIME_172800_2DSOIL_PHREEQCRM['Y_ABS 2DSoil_PhreeqcRM'], label=' ',color = 'green',linestyle='--')
#AX_1.plot(DF_TIME_172800_2DSOIL_PHREEQCRM['Ca2+ 2DSoil-PhreeqcRM'], DF_TIME_172800_2DSOIL_PHREEQCRM['Y_ABS 2DSoil_PhreeqcRM'], label='Time = 2 Days, Source: 2DSoil-PhreeqcRM',color = 'green',linestyle='--')
AX_1.scatter(DF_TIME_172800_IPHREEQC['Ca2+ IPhreeqc'].iloc[::2], DF_TIME_172800_IPHREEQC['Y Iphreeqc'].iloc[::2], label=' ', color = 'green', s = 25)
#AX_1.scatter(DF_TIME_172800_IPHREEQC['Ca2+ IPhreeqc'].iloc[::2], DF_TIME_172800_IPHREEQC['Y Iphreeqc'].iloc[::2], label='Time = 2 Days, Source: IPhreeqc', color = 'green', s = 25)
x = DF_TIME_172800_2DSOIL_PHREEQCRM['Ca2+ 2DSoil-PhreeqcRM'].iloc[53]
y = DF_TIME_172800_2DSOIL_PHREEQCRM['Y_ABS 2DSoil_PhreeqcRM'].iloc[53]
AX_1.text(x-0.025, y-2.25, '2 Days', color='black', fontsize=12, bbox=dict(facecolor='white', edgecolor='black', alpha=0.8))

# Plotting Ca2+ for time = 259200 seconds (3 days)
AX_1.plot(DF_TIME_259200_2DSOIL_PHREEQCRM['Ca2+ 2DSoil-PhreeqcRM'], DF_TIME_259200_2DSOIL_PHREEQCRM['Y_ABS 2DSoil_PhreeqcRM'], label=' ',color = 'orange',linestyle='--')
#AX_1.plot(DF_TIME_259200_2DSOIL_PHREEQCRM['Ca2+ 2DSoil-PhreeqcRM'], DF_TIME_259200_2DSOIL_PHREEQCRM['Y_ABS 2DSoil_PhreeqcRM'], label='Time = 3 Days, Source: 2DSoil-PhreeqcRM',color = 'orange',linestyle='--')
AX_1.scatter(DF_TIME_259200_IPHREEQC['Ca2+ IPhreeqc'].iloc[::2], DF_TIME_259200_IPHREEQC['Y Iphreeqc'].iloc[::2], label=' ', color = 'orange', s = 25)
#AX_1.scatter(DF_TIME_259200_IPHREEQC['Ca2+ IPhreeqc'].iloc[::2], DF_TIME_259200_IPHREEQC['Y Iphreeqc'].iloc[::2], label='Time = 3 Days, Source: IPhreeqc', color = 'orange', s = 25)
x = DF_TIME_259200_2DSOIL_PHREEQCRM['Ca2+ 2DSoil-PhreeqcRM'].iloc[80]
y = DF_TIME_259200_2DSOIL_PHREEQCRM['Y_ABS 2DSoil_PhreeqcRM'].iloc[80]
AX_1.text(x, y-2.5, '3 Days', color='black', fontsize=12, bbox=dict(facecolor='white', edgecolor='black', alpha=0.8))

# Plotting Ca2+ for time = 345600 seconds (4 days)
AX_1.plot(DF_TIME_345600_2DSOIL_PHREEQCRM['Ca2+ 2DSoil-PhreeqcRM'], DF_TIME_345600_2DSOIL_PHREEQCRM['Y_ABS 2DSoil_PhreeqcRM'], label='2DSoil-PhreeqcRM',color = 'purple',linestyle='--')
#AX_1.plot(DF_TIME_345600_2DSOIL_PHREEQCRM['Ca2+ 2DSoil-PhreeqcRM'], DF_TIME_345600_2DSOIL_PHREEQCRM['Y_ABS 2DSoil_PhreeqcRM'], label='Time = 4 Days, Source: 2DSoil-PhreeqcRM',color = 'purple',linestyle='--')
AX_1.scatter(DF_TIME_345600_IPHREEQC['Ca2+ IPhreeqc'].iloc[::2], DF_TIME_345600_IPHREEQC['Y Iphreeqc'].iloc[::2], label='IPhreeqc', color = 'purple', s = 25)
#AX_1.scatter(DF_TIME_345600_IPHREEQC['Ca2+ IPhreeqc'].iloc[::2], DF_TIME_345600_IPHREEQC['Y Iphreeqc'].iloc[::2], label='Time = 4 Days, Source: IPhreeqc', color = 'purple', s = 25)
x = DF_TIME_345600_2DSOIL_PHREEQCRM['Ca2+ 2DSoil-PhreeqcRM'].iloc[94]
y = DF_TIME_345600_2DSOIL_PHREEQCRM['Y_ABS 2DSoil_PhreeqcRM'].iloc[94]
AX_1.text(x-0.1, y-2.5, '4 Days', color='black', fontsize=12, bbox=dict(facecolor='white', edgecolor='black', alpha=0.8))

AX_1.text(x+0.10, y-17, '----  2DSoil-PhreeqcRM            ●  IPhreeqc', color='black', fontsize=22, bbox=dict(facecolor='white', edgecolor='black', alpha=0.8))
#AX_1.legend(loc='lower center',bbox_to_anchor=(1.68, -0.175), ncol=5, fontsize = 16, frameon=False) # Legend outside the plot
AX_1.grid()
AX_1.tick_params(axis='both', labelsize=16)


# Plotting Na+ for time = 0 seconds
AX_2.plot(DF_TIME_0_2DSOIL_PHREEQCRM['Na+ 2DSoil-PhreeqcRM'], DF_TIME_0_2DSOIL_PHREEQCRM['Y_ABS 2DSoil_PhreeqcRM'], label='Time = 0, Source: 2DSoil-PhreeqcRM',color = 'red',linestyle='--')
AX_2.scatter(DF_TIME_0_IPHREEQC['Na+ IPhreeqc'].iloc[::2], DF_TIME_0_IPHREEQC['Y Iphreeqc'].iloc[::2], label='Time = 0, Source: IPhreeqc', color = 'red', s = 25)
AX_2.set_xlabel(r'Na$^{+}$ Concentration (mmols/l)',fontsize=20)
#AX_2.set_ylabel('Distance Above The Column Base (cm)',fontsize=14)
LONG_TITLE = '(b)'
WRAPPED_TITLE = textwrap.fill(LONG_TITLE, width=40)
AX_2.set_title(WRAPPED_TITLE,fontsize=20,x=0.5, y=1.01)
AX_2.set_xlim(0, 1.001)
AX_2.set_ylim(0, 100)
x = DF_TIME_0_2DSOIL_PHREEQCRM['Na+ 2DSoil-PhreeqcRM'].iloc[10]
y = DF_TIME_0_2DSOIL_PHREEQCRM['Y_ABS 2DSoil_PhreeqcRM'].iloc[10]
AX_2.text(x-0.275, y, 'Time = 0 Day', color='black', fontsize=12, bbox=dict(facecolor='white', edgecolor='black', alpha=0.8))

# Plotting Na+ for time = 86400 seconds (1 day)
AX_2.plot(DF_TIME_86400_2DSOIL_PHREEQCRM['Na+ 2DSoil-PhreeqcRM'], DF_TIME_86400_2DSOIL_PHREEQCRM['Y_ABS 2DSoil_PhreeqcRM'], label='Time = 1 Day, Source: 2DSoil-PhreeqcRM',color = 'blue',linestyle='--')
AX_2.scatter(DF_TIME_86400_IPHREEQC['Na+ IPhreeqc'].iloc[::2], DF_TIME_86400_IPHREEQC['Y Iphreeqc'].iloc[::2], label='Time = 1 Day, Source: IPhreeqc', color = 'blue', s = 25)
x = DF_TIME_86400_2DSOIL_PHREEQCRM['Na+ 2DSoil-PhreeqcRM'].iloc[31]
y = DF_TIME_86400_2DSOIL_PHREEQCRM['Y_ABS 2DSoil_PhreeqcRM'].iloc[31]
AX_2.text(x+0.05, y+1, '1 Day', color='black', fontsize=12, bbox=dict(facecolor='white', edgecolor='black', alpha=0.8))

# Plotting Na+ for time = 172800 seconds (2 days)
AX_2.plot(DF_TIME_172800_2DSOIL_PHREEQCRM['Na+ 2DSoil-PhreeqcRM'], DF_TIME_172800_2DSOIL_PHREEQCRM['Y_ABS 2DSoil_PhreeqcRM'], label='Time = 2 Days, Source: 2DSoil-PhreeqcRM',color = 'green',linestyle='--')
AX_2.scatter(DF_TIME_172800_IPHREEQC['Na+ IPhreeqc'].iloc[::2], DF_TIME_172800_IPHREEQC['Y Iphreeqc'].iloc[::2], label='Time = 2 Days, Source: IPhreeqc', color = 'green', s = 25)
x = DF_TIME_172800_2DSOIL_PHREEQCRM['Na+ 2DSoil-PhreeqcRM'].iloc[62]
y = DF_TIME_172800_2DSOIL_PHREEQCRM['Y_ABS 2DSoil_PhreeqcRM'].iloc[62]
AX_2.text(x-0.025, y+2.5, '2 Days', color='black', fontsize=12, bbox=dict(facecolor='white', edgecolor='black', alpha=0.8))

# Plotting Na+ for time = 259200 seconds (3 days)
AX_2.plot(DF_TIME_259200_2DSOIL_PHREEQCRM['Na+ 2DSoil-PhreeqcRM'], DF_TIME_259200_2DSOIL_PHREEQCRM['Y_ABS 2DSoil_PhreeqcRM'], label='Time = 3 Days, Source: 2DSoil-PhreeqcRM',color = 'orange',linestyle='--')
AX_2.scatter(DF_TIME_259200_IPHREEQC['Na+ IPhreeqc'].iloc[::2], DF_TIME_259200_IPHREEQC['Y Iphreeqc'].iloc[::2], label='Time = 3 Days, Source: IPhreeqc', color = 'orange', s = 25)
x = DF_TIME_259200_2DSOIL_PHREEQCRM['Na+ 2DSoil-PhreeqcRM'].iloc[80]
y = DF_TIME_259200_2DSOIL_PHREEQCRM['Y_ABS 2DSoil_PhreeqcRM'].iloc[80]
AX_2.text(x+0.075, y-2.5, '3 Days', color='black', fontsize=12, bbox=dict(facecolor='white', edgecolor='black', alpha=0.8))

# Plotting Na+ for time = 345600 seconds (4 days)
AX_2.plot(DF_TIME_345600_2DSOIL_PHREEQCRM['Na+ 2DSoil-PhreeqcRM'], DF_TIME_345600_2DSOIL_PHREEQCRM['Y_ABS 2DSoil_PhreeqcRM'], label='Time = 4 Days, Source: 2DSoil-PhreeqcRM',color = 'purple',linestyle='--')
AX_2.scatter(DF_TIME_345600_IPHREEQC['Na+ IPhreeqc'].iloc[::2], DF_TIME_345600_IPHREEQC['Y Iphreeqc'].iloc[::2], label='Time = 4 Days, Source: IPhreeqc', color = 'purple', s = 25)
x = DF_TIME_345600_2DSOIL_PHREEQCRM['Na+ 2DSoil-PhreeqcRM'].iloc[94]
y = DF_TIME_345600_2DSOIL_PHREEQCRM['Y_ABS 2DSoil_PhreeqcRM'].iloc[94]
AX_2.text(x+0.04, y-2.5, '4 Days', color='black', fontsize=12, bbox=dict(facecolor='white', edgecolor='black', alpha=0.8))
AX_2.grid()
AX_2.tick_params(axis='both', labelsize=15)


# Plotting K+ for time = 0 seconds
AX_3.plot(DF_TIME_0_2DSOIL_PHREEQCRM['K+ 2DSoil-PhreeqcRM'], DF_TIME_0_2DSOIL_PHREEQCRM['Y_ABS 2DSoil_PhreeqcRM'], label='Time = 0, Source: 2DSoil-PhreeqcRM',color = 'red',linestyle='--')
AX_3.scatter(DF_TIME_0_IPHREEQC['K+ IPhreeqc'].iloc[::2], DF_TIME_0_IPHREEQC['Y Iphreeqc'].iloc[::2], label='Time = 0, Source: IPhreeqc', color = 'red', s = 25)
AX_3.set_xlabel(r'K$^{+}$ Concentration (mmols/l)',fontsize=20)
#AX_3.set_ylabel('Distance Above The Column Base (cm)',fontsize=14)
LONG_TITLE = '(c)'
WRAPPED_TITLE = textwrap.fill(LONG_TITLE, width=40)
AX_3.set_title(WRAPPED_TITLE,fontsize=20,x=0.5, y=1.01)
AX_3.set_xlim(0, 1.2)
AX_3.set_ylim(0, 100)
x = DF_TIME_0_2DSOIL_PHREEQCRM['K+ 2DSoil-PhreeqcRM'].iloc[10]
y = DF_TIME_0_2DSOIL_PHREEQCRM['Y_ABS 2DSoil_PhreeqcRM'].iloc[10]
AX_3.text(x+0.05, y, 'Time = 0 Day', color='black', fontsize=12, bbox=dict(facecolor='white', edgecolor='black', alpha=0.8))

# Plotting K+ for time = 86400 seconds (1 day)
AX_3.plot(DF_TIME_86400_2DSOIL_PHREEQCRM['K+ 2DSoil-PhreeqcRM'], DF_TIME_86400_2DSOIL_PHREEQCRM['Y_ABS 2DSoil_PhreeqcRM'], label='Time = 1 Day, Source: 2DSoil-PhreeqcRM',color = 'blue',linestyle='--')
AX_3.scatter(DF_TIME_86400_IPHREEQC['K+ IPhreeqc'].iloc[::2], DF_TIME_86400_IPHREEQC['Y Iphreeqc'].iloc[::2], label='Time = 1 Day, Source: IPhreeqc', color = 'blue', s = 25)
x = DF_TIME_86400_2DSOIL_PHREEQCRM['K+ 2DSoil-PhreeqcRM'].iloc[30]
y = DF_TIME_86400_2DSOIL_PHREEQCRM['Y_ABS 2DSoil_PhreeqcRM'].iloc[30]
AX_3.text(x-0.15, y+2, '1 Day', color='black', fontsize=12, bbox=dict(facecolor='white', edgecolor='black', alpha=0.8))

# Plotting K+ for time = 172800 seconds (2 days)
AX_3.plot(DF_TIME_172800_2DSOIL_PHREEQCRM['K+ 2DSoil-PhreeqcRM'], DF_TIME_172800_2DSOIL_PHREEQCRM['Y_ABS 2DSoil_PhreeqcRM'], label='Time = 2 Days, Source: 2DSoil-PhreeqcRM',color = 'green',linestyle='--')
AX_3.scatter(DF_TIME_172800_IPHREEQC['K+ IPhreeqc'].iloc[::2], DF_TIME_172800_IPHREEQC['Y Iphreeqc'].iloc[::2], label='Time = 2 Days, Source: IPhreeqc', color = 'green', s = 25)
x = DF_TIME_172800_2DSOIL_PHREEQCRM['K+ 2DSoil-PhreeqcRM'].iloc[55]
y = DF_TIME_172800_2DSOIL_PHREEQCRM['Y_ABS 2DSoil_PhreeqcRM'].iloc[55]
AX_3.text(x-0.1, y+1.5, '2 Days', color='black', fontsize=12, bbox=dict(facecolor='white', edgecolor='black', alpha=0.8))

# Plotting K+ for time = 259200 seconds (3 days)
AX_3.plot(DF_TIME_259200_2DSOIL_PHREEQCRM['K+ 2DSoil-PhreeqcRM'], DF_TIME_259200_2DSOIL_PHREEQCRM['Y_ABS 2DSoil_PhreeqcRM'], label='Time = 3 Days, Source: 2DSoil-PhreeqcRM',color = 'orange',linestyle='--')
AX_3.scatter(DF_TIME_259200_IPHREEQC['K+ IPhreeqc'].iloc[::2], DF_TIME_259200_IPHREEQC['Y Iphreeqc'].iloc[::2], label='Time = 3 Days, Source: IPhreeqc', color = 'orange', s = 25)
x = DF_TIME_259200_2DSOIL_PHREEQCRM['K+ 2DSoil-PhreeqcRM'].iloc[80]
y = DF_TIME_259200_2DSOIL_PHREEQCRM['Y_ABS 2DSoil_PhreeqcRM'].iloc[80]
AX_3.text(x+0.075, y-2.5, '3 Days', color='black', fontsize=12, bbox=dict(facecolor='white', edgecolor='black', alpha=0.8))

# Plotting K+ for time = 345600 seconds (4 days)
AX_3.plot(DF_TIME_345600_2DSOIL_PHREEQCRM['K+ 2DSoil-PhreeqcRM'], DF_TIME_345600_2DSOIL_PHREEQCRM['Y_ABS 2DSoil_PhreeqcRM'], label='Time = 4 Days, Source: 2DSoil-PhreeqcRM',color = 'purple',linestyle='--')
AX_3.scatter(DF_TIME_345600_IPHREEQC['K+ IPhreeqc'].iloc[::2], DF_TIME_345600_IPHREEQC['Y Iphreeqc'].iloc[::2], label='Time = 4 Days, Source: IPhreeqc', color = 'purple', s = 25)
x = DF_TIME_345600_2DSOIL_PHREEQCRM['K+ 2DSoil-PhreeqcRM'].iloc[94]
y = DF_TIME_345600_2DSOIL_PHREEQCRM['Y_ABS 2DSoil_PhreeqcRM'].iloc[94]
AX_3.text(x-0.05, y-2.5, '4 Days', color='black', fontsize=12, bbox=dict(facecolor='white', edgecolor='black', alpha=0.8))
AX_3.grid()
AX_3.tick_params(axis='both', labelsize=16)
PLT.show()




# SECTION 2 : PLOTTING Cl- AND NO3- CONCENTRATION PROFILES
FIGURE_2,AXES_2 = PLT.subplots(nrows=1, ncols=2, figsize=(10, 10))
PLT.subplots_adjust(top=0.90, bottom=0.125)
#PLT.subplots_adjust(wspace=0.5)

AX_1 = AXES_2[0]
AX_2 = AXES_2[1]

# Plotting Cl- for time = 0 seconds
AX_1.plot(DF_TIME_0_2DSOIL_PHREEQCRM['Cl- 2DSoil-PhreeqcRM'], DF_TIME_0_2DSOIL_PHREEQCRM['Y_ABS 2DSoil_PhreeqcRM'], label=' ',color = 'red',linestyle='--')
#AX_1.plot(DF_TIME_0_2DSOIL_PHREEQCRM['Cl- 2DSoil-PhreeqcRM'], DF_TIME_0_2DSOIL_PHREEQCRM['Y_ABS 2DSoil_PhreeqcRM'], label='Time = 0, Source: 2DSoil-PhreeqcRM',color = 'red',linestyle='--')
AX_1.scatter(DF_TIME_0_IPHREEQC['Cl- IPhreeqc'].iloc[::2], DF_TIME_0_IPHREEQC['Y Iphreeqc'].iloc[::2], label=' ', color = 'red', s = 25)
# AX_1.scatter(DF_TIME_0_IPHREEQC['Cl- IPhreeqc'].iloc[::2], DF_TIME_0_IPHREEQC['Y Iphreeqc'].iloc[::2], label='Time = 0, Source: IPhreeqc', color = 'red', s = 25)
AX_1.set_xlabel(r'Cl$^{-}$ Concentration (mmols/l)',fontsize=14)
AX_1.set_ylabel('Distance above the column base (cm)',fontsize=14)
LONG_TITLE = '(a)'
WRAPPED_TITLE = textwrap.fill(LONG_TITLE, width=40)
AX_1.set_title(WRAPPED_TITLE,fontsize=16,x=0.5, y=1.05)
AX_1.set_xlim(-0.0025, 1.2)
AX_1.set_ylim(0, 100)
x = DF_TIME_0_2DSOIL_PHREEQCRM['Cl- 2DSoil-PhreeqcRM'].iloc[10]
y = DF_TIME_0_2DSOIL_PHREEQCRM['Y_ABS 2DSoil_PhreeqcRM'].iloc[10]
AX_1.text(x+0.0175, y, 'Time = 0 Day', color='black', fontsize=12, bbox=dict(facecolor='white', edgecolor='black', alpha=0.8))

# Plotting Cl- for time = 86400 seconds (1 day)
AX_1.plot(DF_TIME_86400_2DSOIL_PHREEQCRM['Cl- 2DSoil-PhreeqcRM'], DF_TIME_86400_2DSOIL_PHREEQCRM['Y_ABS 2DSoil_PhreeqcRM'], label=' ',color = 'blue',linestyle='--')
#AX_1.plot(DF_TIME_86400_2DSOIL_PHREEQCRM['Cl- 2DSoil-PhreeqcRM'], DF_TIME_86400_2DSOIL_PHREEQCRM['Y_ABS 2DSoil_PhreeqcRM'], label='Time = 1 Day, Source: 2DSoil-PhreeqcRM',color = 'blue',linestyle='--')
AX_1.scatter(DF_TIME_86400_IPHREEQC['Cl- IPhreeqc'].iloc[::2], DF_TIME_86400_IPHREEQC['Y Iphreeqc'].iloc[::2], label=' ', color = 'blue', s = 25)
#AX_1.scatter(DF_TIME_86400_IPHREEQC['Cl- IPhreeqc'].iloc[::2], DF_TIME_86400_IPHREEQC['Y Iphreeqc'].iloc[::2], label='Time = 1 Day, Source: IPhreeqc', color = 'blue', s = 25)
x = DF_TIME_86400_2DSOIL_PHREEQCRM['Cl- 2DSoil-PhreeqcRM'].iloc[45]
y = DF_TIME_86400_2DSOIL_PHREEQCRM['Y_ABS 2DSoil_PhreeqcRM'].iloc[45]
AX_1.text(x-0.1, y+0.1, '1 Day', color='black', fontsize=12, bbox=dict(facecolor='white', edgecolor='black', alpha=0.8))

# Plotting Cl- for time = 172800 seconds (2 days)
AX_1.plot(DF_TIME_172800_2DSOIL_PHREEQCRM['Cl- 2DSoil-PhreeqcRM'], DF_TIME_172800_2DSOIL_PHREEQCRM['Y_ABS 2DSoil_PhreeqcRM'], label=' ',color = 'green',linestyle='--')
#AX_1.plot(DF_TIME_172800_2DSOIL_PHREEQCRM['Cl- 2DSoil-PhreeqcRM'], DF_TIME_172800_2DSOIL_PHREEQCRM['Y_ABS 2DSoil_PhreeqcRM'], label='Time = 2 Days, Source: 2DSoil-PhreeqcRM',color = 'green',linestyle='--')
AX_1.scatter(DF_TIME_172800_IPHREEQC['Cl- IPhreeqc'].iloc[::2], DF_TIME_172800_IPHREEQC['Y Iphreeqc'].iloc[::2], label=' ', color = 'green', s = 25)
#AX_1.scatter(DF_TIME_172800_IPHREEQC['Cl- IPhreeqc'].iloc[::2], DF_TIME_172800_IPHREEQC['Y Iphreeqc'].iloc[::2], label='Time = 2 Days, Source: IPhreeqc', color = 'green', s = 25)
x = DF_TIME_172800_2DSOIL_PHREEQCRM['Cl- 2DSoil-PhreeqcRM'].iloc[75]
y = DF_TIME_172800_2DSOIL_PHREEQCRM['Y_ABS 2DSoil_PhreeqcRM'].iloc[75]
AX_1.text(x-0.125, y, '2 Days', color='black', fontsize=12, bbox=dict(facecolor='white', edgecolor='black', alpha=0.8))

# Plotting Cl- for time = 259200 seconds (3 days)
AX_1.plot(DF_TIME_259200_2DSOIL_PHREEQCRM['Cl- 2DSoil-PhreeqcRM'], DF_TIME_259200_2DSOIL_PHREEQCRM['Y_ABS 2DSoil_PhreeqcRM'], label=' 2DSoil-PhreeqcRM',color = 'orange',linestyle='--')
#AX_1.plot(DF_TIME_259200_2DSOIL_PHREEQCRM['Cl- 2DSoil-PhreeqcRM'], DF_TIME_259200_2DSOIL_PHREEQCRM['Y_ABS 2DSoil_PhreeqcRM'], label='Time = 3 Days, Source: 2DSoil-PhreeqcRM',color = 'orange',linestyle='--')
AX_1.scatter(DF_TIME_259200_IPHREEQC['Cl- IPhreeqc'].iloc[::2], DF_TIME_259200_IPHREEQC['Y Iphreeqc'].iloc[::2], label=' IPhreeqc', color = 'orange', s = 25)
#AX_1.scatter(DF_TIME_259200_IPHREEQC['Cl- IPhreeqc'].iloc[::2], DF_TIME_259200_IPHREEQC['Y Iphreeqc'].iloc[::2], label='Time = 3 Days, Source: IPhreeqc', color = 'orange', s = 25)
x = DF_TIME_259200_2DSOIL_PHREEQCRM['Cl- 2DSoil-PhreeqcRM'].iloc[90]
y = DF_TIME_259200_2DSOIL_PHREEQCRM['Y_ABS 2DSoil_PhreeqcRM'].iloc[90]
AX_1.text(x-0.125, y, '3 Days', color='black', fontsize=12, bbox=dict(facecolor='white', edgecolor='black', alpha=0.8))

# NOT PLOTTING BECAUSE ANIONS LEFT THE COLUMN BY 3rd DAY
# Plotting Cl- for time = 345600 seconds (4 days)
# AX_1.plot(DF_TIME_345600_2DSOIL_PHREEQCRM['Cl- 2DSoil-PhreeqcRM'], DF_TIME_345600_2DSOIL_PHREEQCRM['Y_ABS 2DSoil_PhreeqcRM'], label='2DSoil-PhreeqcRM',color = 'purple',linestyle='--')
# #AX_1.plot(DF_TIME_345600_2DSOIL_PHREEQCRM['Cl- 2DSoil-PhreeqcRM'], DF_TIME_345600_2DSOIL_PHREEQCRM['Y_ABS 2DSoil_PhreeqcRM'], label='Time = 4 Days, Source: 2DSoil-PhreeqcRM',color = 'purple',linestyle='--')
# AX_1.scatter(DF_TIME_345600_IPHREEQC['Cl- IPhreeqc'].iloc[::2], DF_TIME_345600_IPHREEQC['Y Iphreeqc'].iloc[::2], label='IPhreeqc', color = 'purple', s = 25)
# #AX_1.scatter(DF_TIME_345600_IPHREEQC['Cl- IPhreeqc'].iloc[::2], DF_TIME_345600_IPHREEQC['Y Iphreeqc'].iloc[::2], label='Time = 4 Days, Source: IPhreeqc', color = 'purple', s = 25)
# x = DF_TIME_345600_2DSOIL_PHREEQCRM['Cl- 2DSoil-PhreeqcRM'].iloc[94]
# y = DF_TIME_345600_2DSOIL_PHREEQCRM['Y_ABS 2DSoil_PhreeqcRM'].iloc[94]
# AX_1.text(x-0.1, y-2.5, '4 Days', color='black', fontsize=12, bbox=dict(facecolor='white', edgecolor='black', alpha=0.8))

AX_1.legend(loc='lower center',bbox_to_anchor=(1.1, -0.175), ncol=4, fontsize = 12) # Legend outside the plot
AX_1.grid()
AX_1.tick_params(axis='both', labelsize=12)


# Plotting NO3- for time = 0 seconds
AX_2.plot(DF_TIME_0_2DSOIL_PHREEQCRM['NO3- 2DSoil-PhreeqcRM'], DF_TIME_0_2DSOIL_PHREEQCRM['Y_ABS 2DSoil_PhreeqcRM'], label='Time = 0, Source: 2DSoil-PhreeqcRM',color = 'red',linestyle='--')
AX_2.scatter(DF_TIME_0_IPHREEQC['NO3- IPhreeqc'].iloc[::2], DF_TIME_0_IPHREEQC['Y Iphreeqc'].iloc[::2], label='Time = 0, Source: IPhreeqc', color = 'red', s = 25)
AX_2.set_xlabel(r'NO$_{3}^{-}$ Concentration (mmols/l)',fontsize=14)
#AX_2.set_ylabel('Distance Above The Column Base (cm)',fontsize=14)
LONG_TITLE = '(b)'
WRAPPED_TITLE = textwrap.fill(LONG_TITLE, width=40)
AX_2.set_title(WRAPPED_TITLE,fontsize=16,x=0.5, y=1.05)
AX_2.set_xlim(0, 1.2001)
AX_2.set_ylim(0, 100)
x = DF_TIME_0_2DSOIL_PHREEQCRM['NO3- 2DSoil-PhreeqcRM'].iloc[10]
y = DF_TIME_0_2DSOIL_PHREEQCRM['Y_ABS 2DSoil_PhreeqcRM'].iloc[10]
AX_2.text(x-0.22, y, 'Time = 0 Day', color='black', fontsize=12, bbox=dict(facecolor='white', edgecolor='black', alpha=0.8))

# Plotting NO3- for time = 86400 seconds (1 day)
AX_2.plot(DF_TIME_86400_2DSOIL_PHREEQCRM['NO3- 2DSoil-PhreeqcRM'], DF_TIME_86400_2DSOIL_PHREEQCRM['Y_ABS 2DSoil_PhreeqcRM'], label='Time = 1 Day, Source: 2DSoil-PhreeqcRM',color = 'blue',linestyle='--')
AX_2.scatter(DF_TIME_86400_IPHREEQC['NO3- IPhreeqc'].iloc[::2], DF_TIME_86400_IPHREEQC['Y Iphreeqc'].iloc[::2], label='Time = 1 Day, Source: IPhreeqc', color = 'blue', s = 25)
x = DF_TIME_86400_2DSOIL_PHREEQCRM['NO3- 2DSoil-PhreeqcRM'].iloc[45]
y = DF_TIME_86400_2DSOIL_PHREEQCRM['Y_ABS 2DSoil_PhreeqcRM'].iloc[45]
AX_2.text(x+0.1, y-1.5, '1 Day', color='black', fontsize=12, bbox=dict(facecolor='white', edgecolor='black', alpha=0.8))

# Plotting NO3- for time = 172800 seconds (2 days)
AX_2.plot(DF_TIME_172800_2DSOIL_PHREEQCRM['NO3- 2DSoil-PhreeqcRM'], DF_TIME_172800_2DSOIL_PHREEQCRM['Y_ABS 2DSoil_PhreeqcRM'], label='Time = 2 Days, Source: 2DSoil-PhreeqcRM',color = 'green',linestyle='--')
AX_2.scatter(DF_TIME_172800_IPHREEQC['NO3- IPhreeqc'].iloc[::2], DF_TIME_172800_IPHREEQC['Y Iphreeqc'].iloc[::2], label='Time = 2 Days, Source: IPhreeqc', color = 'green', s = 25)
x = DF_TIME_172800_2DSOIL_PHREEQCRM['NO3- 2DSoil-PhreeqcRM'].iloc[75]
y = DF_TIME_172800_2DSOIL_PHREEQCRM['Y_ABS 2DSoil_PhreeqcRM'].iloc[75]
AX_2.text(x+0.025, y, '2 Days', color='black', fontsize=12, bbox=dict(facecolor='white', edgecolor='black', alpha=0.8))

# Plotting NO3- for time = 259200 seconds (3 days)
AX_2.plot(DF_TIME_259200_2DSOIL_PHREEQCRM['NO3- 2DSoil-PhreeqcRM'], DF_TIME_259200_2DSOIL_PHREEQCRM['Y_ABS 2DSoil_PhreeqcRM'], label='Time = 3 Days, Source: 2DSoil-PhreeqcRM',color = 'orange',linestyle='--')
AX_2.scatter(DF_TIME_259200_IPHREEQC['NO3- IPhreeqc'].iloc[::2], DF_TIME_259200_IPHREEQC['Y Iphreeqc'].iloc[::2], label='Time = 3 Days, Source: IPhreeqc', color = 'orange', s = 25)
x = DF_TIME_259200_2DSOIL_PHREEQCRM['NO3- 2DSoil-PhreeqcRM'].iloc[90]
y = DF_TIME_259200_2DSOIL_PHREEQCRM['Y_ABS 2DSoil_PhreeqcRM'].iloc[90]
AX_2.text(x+0.025, y, '3 Days', color='black', fontsize=12, bbox=dict(facecolor='white', edgecolor='black', alpha=0.8))

# Plotting NO3- for time = 345600 seconds (4 days)
# AX_2.plot(DF_TIME_345600_2DSOIL_PHREEQCRM['NO3- 2DSoil-PhreeqcRM'], DF_TIME_345600_2DSOIL_PHREEQCRM['Y_ABS 2DSoil_PhreeqcRM'], label='Time = 4 Days, Source: 2DSoil-PhreeqcRM',color = 'purple',linestyle='--')
# AX_2.scatter(DF_TIME_345600_IPHREEQC['NO3- IPhreeqc'].iloc[::2], DF_TIME_345600_IPHREEQC['Y Iphreeqc'].iloc[::2], label='Time = 4 Days, Source: IPhreeqc', color = 'purple', s = 25)
# x = DF_TIME_345600_2DSOIL_PHREEQCRM['NO3- 2DSoil-PhreeqcRM'].iloc[94]
# y = DF_TIME_345600_2DSOIL_PHREEQCRM['Y_ABS 2DSoil_PhreeqcRM'].iloc[94]
# AX_2.text(x+0.04, y-2.5, '4 Days', color='black', fontsize=12, bbox=dict(facecolor='white', edgecolor='black', alpha=0.8))
AX_2.grid()
AX_2.tick_params(axis='both', labelsize=12)



PLT.show()